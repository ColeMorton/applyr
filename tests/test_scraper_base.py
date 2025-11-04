"""Tests for scraper base class"""

from pathlib import Path
import time

from bs4 import BeautifulSoup
from rich.console import Console

from applyr.database import JobStatus, Priority
from applyr.scraper_base import JobScraper


class ConcreteScraper(JobScraper):
    """Concrete implementation of JobScraper for testing"""

    def extract_job_id(self, _url: str):
        """Extract job ID from URL"""
        return "test-id"

    def extract_job_metadata(self, _soup: BeautifulSoup) -> dict[str, str]:
        """Extract job metadata"""
        return {"title": "Test Job", "company": "Test Company"}

    def clean_job_description(self, _soup: BeautifulSoup):
        """Clean job description"""
        return "Test job description content"

    def get_source_name(self) -> str:
        """Return source name"""
        return "Test Source"


class TestJobScraperInitialization:
    """Tests for JobScraper initialization"""

    def test_init_with_defaults(self):
        """Test JobScraper initialization with default values"""
        scraper = ConcreteScraper()
        assert scraper.delay == 2.0
        assert scraper.database is None
        assert scraper.session is not None

    def test_init_with_custom_delay(self, test_database):
        """Test JobScraper initialization with custom delay"""
        scraper = ConcreteScraper(delay_between_requests=3.0, database=test_database)
        assert scraper.delay == 3.0
        assert scraper.database == test_database

    def test_init_with_database(self, test_database):
        """Test JobScraper initialization with database"""
        scraper = ConcreteScraper(database=test_database)
        assert scraper.database == test_database


class TestSetupSession:
    """Tests for _setup_session method"""

    def test_session_has_user_agent(self):
        """Test that session has user agent"""
        scraper = ConcreteScraper()
        scraper._setup_session()

        assert "User-Agent" in scraper.session.headers
        assert "Mozilla" in scraper.session.headers["User-Agent"]

    def test_session_has_accept_headers(self):
        """Test that session has accept headers"""
        scraper = ConcreteScraper()
        scraper._setup_session()

        assert "Accept" in scraper.session.headers
        assert "Accept-Language" in scraper.session.headers


class TestGetRequestHeaders:
    """Tests for _get_request_headers method"""

    def test_default_headers_empty(self):
        """Test that default request headers are empty"""
        scraper = ConcreteScraper()
        headers = scraper._get_request_headers("https://example.com")

        assert headers == {}


class TestFetchPage:
    """Tests for fetch_page method"""

    def test_fetch_page_success(self, mock_responses):
        """Test successful page fetch"""
        scraper = ConcreteScraper()
        url = "https://example.com/job"
        html_content = "<html><body><h1>Test</h1></body></html>"

        mock_responses.add(mock_responses.GET, url, body=html_content, status=200)

        soup = scraper.fetch_page(url)

        assert soup is not None
        assert isinstance(soup, BeautifulSoup)
        assert soup.find("h1") is not None

    def test_fetch_page_403_error(self, mock_responses):
        """Test page fetch with 403 error"""
        scraper = ConcreteScraper()
        url = "https://example.com/job"

        mock_responses.add(mock_responses.GET, url, body="Forbidden", status=403)

        soup = scraper.fetch_page(url)

        assert soup is None

    def test_fetch_page_404_error(self, mock_responses):
        """Test page fetch with 404 error"""
        scraper = ConcreteScraper()
        url = "https://example.com/job"

        mock_responses.add(mock_responses.GET, url, body="Not Found", status=404)

        soup = scraper.fetch_page(url)

        assert soup is None

    def test_fetch_page_network_error(self, mock_responses):  # noqa: ARG002
        """Test page fetch with network error"""
        scraper = ConcreteScraper()
        url = "https://example.com/job"

        # Simulate network error by not adding a response
        # This will cause a connection error
        soup = scraper.fetch_page(url)

        assert soup is None

    def test_fetch_page_timeout(self, mocker):
        """Test page fetch timeout handling"""
        import requests

        scraper = ConcreteScraper()

        # Mock requests to raise Timeout exception
        mocker.patch.object(scraper.session, "get", side_effect=requests.Timeout("Connection timeout"))

        url = "https://httpbin.org/delay/10"
        soup = scraper.fetch_page(url)

        # Should return None on timeout
        assert soup is None


class TestSanitizeFilename:
    """Tests for sanitize_filename method"""

    def test_sanitize_simple_text(self):
        """Test sanitization of simple text"""
        scraper = ConcreteScraper()
        result = scraper.sanitize_filename("Software Engineer")

        assert result == "Software_Engineer"

    def test_sanitize_special_characters(self):
        """Test sanitization of special characters"""
        scraper = ConcreteScraper()
        result = scraper.sanitize_filename("Job: <Title> | Company/Name?")

        assert ":" not in result
        assert "<" not in result
        assert ">" not in result
        assert "|" not in result
        assert "/" not in result
        assert "?" not in result

    def test_sanitize_max_length(self):
        """Test filename length limitation"""
        scraper = ConcreteScraper()
        long_text = "A" * 150
        result = scraper.sanitize_filename(long_text, max_length=100)

        assert len(result) <= 100

    def test_sanitize_removes_leading_trailing_underscores(self):
        """Test removal of leading/trailing underscores"""
        scraper = ConcreteScraper()
        result = scraper.sanitize_filename("_test_")

        assert not result.startswith("_")
        assert not result.endswith("_")

    def test_sanitize_multiple_spaces(self):
        """Test that multiple spaces are collapsed"""
        scraper = ConcreteScraper()
        result = scraper.sanitize_filename("Multiple    Spaces")

        assert "  " not in result


class TestSaveJobDescription:
    """Tests for save_job_description method"""

    def test_save_job_description_success(self, temp_dir: Path):
        """Test successful job description save"""
        scraper = ConcreteScraper()
        job_id = "12345678"
        metadata = {"title": "Software Engineer", "company": "Tech Company"}
        description = "Job description content"
        output_dir = temp_dir / "jobs"

        success = scraper.save_job_description(job_id, metadata, description, output_dir)

        assert success is True
        assert output_dir.exists()
        job_files = list(output_dir.glob("*.md"))
        assert len(job_files) == 1

        # Verify file content
        job_file = job_files[0]
        content = job_file.read_text()
        assert "Software Engineer" in content
        assert "Tech Company" in content
        assert "12345678" in content
        assert "Job description content" in content

    def test_save_job_description_creates_directory(self, temp_dir: Path):
        """Test that output directory is created if it doesn't exist"""
        scraper = ConcreteScraper()
        job_id = "12345678"
        metadata = {"title": "Software Engineer", "company": "Tech Company"}
        description = "Job description"
        output_dir = temp_dir / "nested" / "jobs"

        success = scraper.save_job_description(job_id, metadata, description, output_dir)

        assert success is True
        assert output_dir.exists()

    def test_save_job_description_sanitizes_filename(self, temp_dir: Path):
        """Test that filename is properly sanitized"""
        scraper = ConcreteScraper()
        job_id = "12345678"
        metadata = {"title": "Job: <Title>", "company": "Company/Name"}
        description = "Description"
        output_dir = temp_dir / "jobs"

        success = scraper.save_job_description(job_id, metadata, description, output_dir)

        assert success is True
        job_files = list(output_dir.glob("*.md"))
        assert len(job_files) == 1
        # Filename should not contain special characters
        assert ":" not in job_files[0].name
        assert "<" not in job_files[0].name


class TestScrapeJob:
    """Tests for scrape_job method"""

    def test_scrape_job_success(self, test_console: Console, temp_dir: Path, mock_responses):
        """Test successful job scraping"""
        scraper = ConcreteScraper(delay_between_requests=0.1)
        url = "https://example.com/job"
        output_dir = temp_dir / "jobs"
        html_content = "<html><body><h1>Test Job</h1></body></html>"

        mock_responses.add(mock_responses.GET, url, body=html_content, status=200)

        success = scraper.scrape_job(url, output_dir, test_console)

        assert success is True
        assert output_dir.exists()
        job_files = list(output_dir.glob("*.md"))
        assert len(job_files) > 0

    def test_scrape_job_invalid_id(self, test_console: Console, temp_dir: Path):
        """Test scraping with invalid job ID"""

        # Create scraper that returns None for job ID
        class InvalidIdScraper(ConcreteScraper):
            def extract_job_id(self, _url: str):
                return None

        scraper = InvalidIdScraper(delay_between_requests=0.1)
        url = "https://example.com/job"
        output_dir = temp_dir / "jobs"

        success = scraper.scrape_job(url, output_dir, test_console)

        assert success is False

    def test_scrape_job_fetch_failure(self, test_console: Console, temp_dir: Path, mock_responses):
        """Test scraping when page fetch fails"""
        scraper = ConcreteScraper(delay_between_requests=0.1)
        url = "https://example.com/job"
        output_dir = temp_dir / "jobs"

        mock_responses.add(mock_responses.GET, url, body="Error", status=500)

        success = scraper.scrape_job(url, output_dir, test_console)

        assert success is False

    def test_scrape_job_no_description(self, test_console: Console, temp_dir: Path, mock_responses):
        """Test scraping when description extraction fails"""

        class NoDescScraper(ConcreteScraper):
            def clean_job_description(self, _soup: BeautifulSoup):
                return None

        scraper = NoDescScraper(delay_between_requests=0.1)
        url = "https://example.com/job"
        output_dir = temp_dir / "jobs"
        html_content = "<html><body></body></html>"

        mock_responses.add(mock_responses.GET, url, body=html_content, status=200)

        success = scraper.scrape_job(url, output_dir, test_console)

        assert success is False

    def test_scrape_job_with_database(self, test_console: Console, temp_dir: Path, mock_responses, test_database):
        """Test scraping with database integration"""
        scraper = ConcreteScraper(delay_between_requests=0.1, database=test_database)
        url = "https://example.com/job"
        output_dir = temp_dir / "jobs"
        html_content = "<html><body><h1>Test</h1></body></html>"

        mock_responses.add(mock_responses.GET, url, body=html_content, status=200)

        success = scraper.scrape_job(url, output_dir, test_console)

        assert success is True
        # Check that job was added to database
        assert test_database.job_exists("test-id") is True
        job = test_database.get_job("test-id")
        assert job["job_title"] == "Test Job"
        assert job["company_name"] == "Test Company"
        assert job["status"] == JobStatus.DISCOVERED.value
        assert job["priority"] == Priority.MEDIUM.value

    def test_scrape_job_delay_between_requests(self, test_console: Console, temp_dir: Path, mock_responses):
        """Test that delay is respected between requests"""
        scraper = ConcreteScraper(delay_between_requests=0.5)
        url = "https://example.com/job"
        output_dir = temp_dir / "jobs"
        html_content = "<html><body><h1>Test</h1></body></html>"

        mock_responses.add(mock_responses.GET, url, body=html_content, status=200)

        start_time = time.time()
        scraper.scrape_job(url, output_dir, test_console)
        elapsed = time.time() - start_time

        # Should have at least the delay time
        assert elapsed >= 0.5
