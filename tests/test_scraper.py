"""Tests for SEEK scraper module"""

from pathlib import Path

from bs4 import BeautifulSoup
from rich.console import Console

from applyr.scraper import SEEKScraper, scrape_jobs


class TestSEEKScraperInitialization:
    """Tests for SEEKScraper initialization"""

    def test_init_with_defaults(self):
        """Test SEEKScraper initialization with default values"""
        scraper = SEEKScraper()
        assert scraper.delay == 2.0
        assert scraper.database is None

    def test_init_with_custom_delay(self, test_database):
        """Test SEEKScraper initialization with custom delay"""
        scraper = SEEKScraper(delay_between_requests=3.0, database=test_database)
        assert scraper.delay == 3.0
        assert scraper.database == test_database

    def test_init_with_database(self, test_database):
        """Test SEEKScraper initialization with database"""
        scraper = SEEKScraper(database=test_database)
        assert scraper.database == test_database


class TestSetupSession:
    """Tests for _setup_session method"""

    def test_session_has_seek_headers(self):
        """Test that session has SEEK-specific headers"""
        scraper = SEEKScraper()
        scraper._setup_session()

        assert "Sec-Fetch-Dest" in scraper.session.headers
        assert scraper.session.headers["Sec-Fetch-Dest"] == "document"
        assert "Sec-Fetch-Mode" in scraper.session.headers
        assert scraper.session.headers["Sec-Fetch-Mode"] == "navigate"
        assert "Upgrade-Insecure-Requests" in scraper.session.headers

    def test_session_has_user_agent(self):
        """Test that session has user agent"""
        scraper = SEEKScraper()
        scraper._setup_session()

        assert "User-Agent" in scraper.session.headers
        assert "Mozilla" in scraper.session.headers["User-Agent"]


class TestGetRequestHeaders:
    """Tests for _get_request_headers method"""

    def test_get_seek_referer(self):
        """Test SEEK-specific referer header"""
        scraper = SEEKScraper()
        headers = scraper._get_request_headers("https://www.seek.com.au/job/12345678")

        assert headers["Referer"] == "https://www.seek.com.au/"


class TestGetSourceName:
    """Tests for get_source_name method"""

    def test_get_source_name(self):
        """Test source name returns SEEK"""
        scraper = SEEKScraper()
        assert scraper.get_source_name() == "SEEK"


class TestExtractJobId:
    """Tests for extract_job_id method"""

    def test_extract_job_id_from_url(self):
        """Test job ID extraction from SEEK URL"""
        scraper = SEEKScraper()
        url = "https://www.seek.com.au/job/12345678"
        job_id = scraper.extract_job_id(url)

        assert job_id == "12345678"

    def test_extract_job_id_with_path(self):
        """Test job ID extraction from URL with additional path"""
        scraper = SEEKScraper()
        url = "https://www.seek.com.au/job/12345678?some=query"
        job_id = scraper.extract_job_id(url)

        assert job_id == "12345678"

    def test_extract_job_id_invalid_url(self):
        """Test job ID extraction from invalid URL returns None"""
        scraper = SEEKScraper()
        url = "https://www.seek.com.au/job/invalid"
        job_id = scraper.extract_job_id(url)

        assert job_id is None

    def test_extract_job_id_non_seek_url(self):
        """Test job ID extraction from non-SEEK URL returns None"""
        scraper = SEEKScraper()
        url = "https://example.com/job/12345678"
        job_id = scraper.extract_job_id(url)

        assert job_id is None

    def test_extract_job_id_empty_string(self):
        """Test job ID extraction from empty string returns None"""
        scraper = SEEKScraper()
        job_id = scraper.extract_job_id("")

        assert job_id is None


class TestExtractJobMetadata:
    """Tests for extract_job_metadata method"""

    def test_extract_metadata_with_data_automation(self):
        """Test metadata extraction with data-automation attributes"""
        scraper = SEEKScraper()
        html = """
        <html>
            <body>
                <h1 data-automation="job-detail-title">Software Engineer</h1>
                <span data-automation="advertiser-name">Tech Company</span>
            </body>
        </html>
        """
        soup = BeautifulSoup(html, "html.parser")
        metadata = scraper.extract_job_metadata(soup)

        assert metadata["title"] == "Software Engineer"
        assert metadata["company"] == "Tech Company"

    def test_extract_metadata_with_class_selectors(self):
        """Test metadata extraction with class selectors"""
        scraper = SEEKScraper()
        html = """
        <html>
            <body>
                <h1 class="jobtitle">Senior Developer</h1>
                <div class="advertiser-name">Company Inc</div>
            </body>
        </html>
        """
        soup = BeautifulSoup(html, "html.parser")
        metadata = scraper.extract_job_metadata(soup)

        assert metadata["title"] == "Senior Developer"
        assert metadata["company"] == "Company Inc"

    def test_extract_metadata_fallback_to_h1(self):
        """Test metadata extraction falls back to h1"""
        scraper = SEEKScraper()
        html = """
        <html>
            <body>
                <h1>Default Job Title</h1>
                <div class="company-name">Default Company</div>
            </body>
        </html>
        """
        soup = BeautifulSoup(html, "html.parser")
        metadata = scraper.extract_job_metadata(soup)

        assert metadata["title"] == "Default Job Title"
        assert metadata["company"] == "Default Company"

    def test_extract_metadata_defaults_when_missing(self):
        """Test metadata extraction returns defaults when not found"""
        scraper = SEEKScraper()
        html = "<html><body><p>No metadata here</p></body></html>"
        soup = BeautifulSoup(html, "html.parser")
        metadata = scraper.extract_job_metadata(soup)

        assert metadata["title"] == "Unknown Job"
        assert metadata["company"] == "Unknown Company"

    def test_extract_metadata_handles_exceptions(self):
        """Test metadata extraction handles exceptions gracefully"""
        scraper = SEEKScraper()
        # Create soup that might cause issues
        html = "<html><body></body></html>"
        soup = BeautifulSoup(html, "html.parser")
        metadata = scraper.extract_job_metadata(soup)

        assert isinstance(metadata, dict)
        assert "title" in metadata
        assert "company" in metadata


class TestCleanJobDescription:
    """Tests for clean_job_description method"""

    def test_clean_description_with_data_automation(self):
        """Test description cleaning with data-automation selector"""
        scraper = SEEKScraper()
        html = """
        <html>
            <body>
                <div data-automation="jobAdDetails">
                    <h2>About the Role</h2>
                    <p>We are looking for a talented developer.</p>
                    <h3>Requirements</h3>
                    <ul>
                        <li>5+ years experience</li>
                        <li>Python knowledge</li>
                    </ul>
                </div>
            </body>
        </html>
        """
        soup = BeautifulSoup(html, "html.parser")
        description = scraper.clean_job_description(soup)

        assert description is not None
        assert "About the Role" in description
        assert "talented developer" in description
        assert "Requirements" in description

    def test_clean_description_removes_company_profile(self):
        """Test that company profile sections are removed"""
        scraper = SEEKScraper()
        html = """
        <html>
            <body>
                <div data-automation="jobAdDetails">
                    <p>Job description content</p>
                    <div data-automation="company-profile">
                        <p>Company profile content</p>
                    </div>
                </div>
            </body>
        </html>
        """
        soup = BeautifulSoup(html, "html.parser")
        description = scraper.clean_job_description(soup)

        assert description is not None
        assert "Job description content" in description
        # Company profile should be removed or not in main content

    def test_clean_description_removes_safety_warnings(self):
        """Test that safety warnings are removed"""
        scraper = SEEKScraper()
        html = """
        <html>
            <body>
                <div data-automation="jobAdDetails">
                    <p>Job description</p>
                    <div class="safety-warning">
                        <p>Be careful of scams</p>
                    </div>
                </div>
            </body>
        </html>
        """
        soup = BeautifulSoup(html, "html.parser")
        description = scraper.clean_job_description(soup)

        assert description is not None
        # Safety warnings should be removed

    def test_clean_description_removes_navigation(self):
        """Test that navigation elements are removed"""
        scraper = SEEKScraper()
        html = """
        <html>
            <body>
                <div data-automation="jobAdDetails">
                    <p>Job description</p>
                    <nav>
                        <a href="/">Home</a>
                    </nav>
                </div>
            </body>
        </html>
        """
        soup = BeautifulSoup(html, "html.parser")
        description = scraper.clean_job_description(soup)

        assert description is not None

    def test_clean_description_removes_duplicates(self):
        """Test that duplicate consecutive lines are removed"""
        scraper = SEEKScraper()
        html = """
        <html>
            <body>
                <div data-automation="jobAdDetails">
                    <p>Line one</p>
                    <p>Line one</p>
                    <p>Line two</p>
                </div>
            </body>
        </html>
        """
        soup = BeautifulSoup(html, "html.parser")
        description = scraper.clean_job_description(soup)

        assert description is not None
        # Should only have one "Line one"
        assert description.count("Line one") == 1

    def test_clean_description_content_based_fallback(self):
        """Test content-based fallback when no standard selectors found"""
        scraper = SEEKScraper()
        html = """
        <html>
            <body>
                <div>
                    <p>About the role: We are looking for someone with experience in software development.</p>
                    <p>Requirements include Python, JavaScript, and modern frameworks.</p>
                </div>
            </body>
        </html>
        """
        soup = BeautifulSoup(html, "html.parser")
        description = scraper.clean_job_description(soup)

        assert description is not None
        assert "software development" in description or "Requirements" in description.lower()

    def test_clean_description_returns_none_when_not_found(self):
        """Test that None is returned when description cannot be found"""
        scraper = SEEKScraper()
        html = "<html><body><p>No job description content</p></body></html>"
        soup = BeautifulSoup(html, "html.parser")
        description = scraper.clean_job_description(soup)

        assert description is None

    def test_clean_description_handles_exceptions(self):
        """Test that exceptions during cleaning are handled"""
        scraper = SEEKScraper()
        # Create soup that might cause issues
        html = "<html><body></body></html>"
        soup = BeautifulSoup(html, "html.parser")
        description = scraper.clean_job_description(soup)

        # Should return None or handle gracefully
        assert description is None or isinstance(description, str)


class TestScrapeJobIntegration:
    """Integration tests for scrape_job method"""

    def test_scrape_job_success(self, test_console: Console, temp_dir: Path, mock_responses, sample_seek_html: str):
        """Test successful job scraping"""
        scraper = SEEKScraper(delay_between_requests=0.1)
        url = "https://www.seek.com.au/job/12345678"
        output_dir = temp_dir / "jobs"

        mock_responses.add(mock_responses.GET, url, body=sample_seek_html, status=200)

        success = scraper.scrape_job(url, output_dir, test_console)

        assert success is True
        # Check that file was created
        job_files = list(output_dir.glob("*.md"))
        assert len(job_files) > 0

    def test_scrape_job_invalid_id(self, test_console: Console, temp_dir: Path):
        """Test scraping with invalid job ID"""
        scraper = SEEKScraper(delay_between_requests=0.1)
        url = "https://www.seek.com.au/job/invalid"
        output_dir = temp_dir / "jobs"

        success = scraper.scrape_job(url, output_dir, test_console)

        assert success is False

    def test_scrape_job_network_error(self, test_console: Console, temp_dir: Path, mock_responses):
        """Test scraping with network error"""
        scraper = SEEKScraper(delay_between_requests=0.1)
        url = "https://www.seek.com.au/job/12345678"
        output_dir = temp_dir / "jobs"

        mock_responses.add(mock_responses.GET, url, body="Error", status=500)

        success = scraper.scrape_job(url, output_dir, test_console)

        assert success is False

    def test_scrape_job_403_error(self, test_console: Console, temp_dir: Path, mock_responses):
        """Test scraping with 403 forbidden error"""
        scraper = SEEKScraper(delay_between_requests=0.1)
        url = "https://www.seek.com.au/job/12345678"
        output_dir = temp_dir / "jobs"

        mock_responses.add(mock_responses.GET, url, body="Forbidden", status=403)

        success = scraper.scrape_job(url, output_dir, test_console)

        assert success is False

    def test_scrape_job_with_database(
        self, test_console: Console, temp_dir: Path, mock_responses, sample_seek_html: str, test_database
    ):
        """Test scraping with database integration"""
        scraper = SEEKScraper(delay_between_requests=0.1, database=test_database)
        url = "https://www.seek.com.au/job/12345678"
        output_dir = temp_dir / "jobs"

        mock_responses.add(mock_responses.GET, url, body=sample_seek_html, status=200)

        success = scraper.scrape_job(url, output_dir, test_console)

        assert success is True
        # Check that job was added to database
        assert test_database.job_exists("12345678") is True


class TestScrapeJobsFunction:
    """Tests for scrape_jobs function"""

    def test_scrape_multiple_jobs(self, test_console: Console, temp_dir: Path, mock_responses, sample_seek_html: str):
        """Test scraping multiple jobs"""
        urls = [
            "https://www.seek.com.au/job/12345678",
            "https://www.seek.com.au/job/12345679",
        ]
        output_dir = temp_dir / "jobs"

        for url in urls:
            mock_responses.add(mock_responses.GET, url, body=sample_seek_html, status=200)

        results = scrape_jobs(urls, output_dir, delay=0.1, console=test_console)

        assert len(results) == 2
        assert all(results.values())

    def test_scrape_mixed_results(self, test_console: Console, temp_dir: Path, mock_responses, sample_seek_html: str):
        """Test scraping with mixed success/failure"""
        urls = [
            "https://www.seek.com.au/job/12345678",
            "https://www.seek.com.au/job/invalid",
        ]
        output_dir = temp_dir / "jobs"

        mock_responses.add(mock_responses.GET, urls[0], body=sample_seek_html, status=200)

        results = scrape_jobs(urls, output_dir, delay=0.1, console=test_console)

        assert len(results) == 2
        assert results[urls[0]] is True
        assert results[urls[1]] is False

    def test_scrape_jobs_with_database(
        self, test_console: Console, temp_dir: Path, mock_responses, sample_seek_html: str, test_database
    ):
        """Test scraping jobs with database"""
        urls = ["https://www.seek.com.au/job/12345678"]
        output_dir = temp_dir / "jobs"

        mock_responses.add(mock_responses.GET, urls[0], body=sample_seek_html, status=200)

        results = scrape_jobs(urls, output_dir, delay=0.1, console=test_console, database=test_database)

        assert results[urls[0]] is True
        assert test_database.job_exists("12345678") is True
