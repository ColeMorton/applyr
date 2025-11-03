"""Tests for Employment Hero scraper"""

from bs4 import BeautifulSoup
import pytest

from applyr.scraper_employment_hero import EmploymentHeroScraper


class TestEmploymentHeroScraper:
    """Tests for EmploymentHeroScraper class"""

    @pytest.fixture
    def scraper(self, test_database):
        """Create Employment Hero scraper instance"""
        return EmploymentHeroScraper(delay_between_requests=1.0, database=test_database)


class TestExtractJobId:
    """Tests for extract_job_id method"""

    @pytest.fixture
    def scraper(self, test_database):
        """Create scraper instance"""
        return EmploymentHeroScraper(delay_between_requests=1.0, database=test_database)

    def test_extract_job_id_standard_format(self, scraper):
        """Test job ID extraction from standard URL"""
        url = "https://jobs.employmenthero.com/AU/job/axcelerate-senior-software-engineer-a5y43"
        job_id = scraper.extract_job_id(url)
        assert job_id == "eh-axcelerate-senior-software-engineer-a5y43"

    def test_extract_job_id_without_country(self, scraper):
        """Test job ID extraction from URL without country code"""
        url = "https://jobs.employmenthero.com/job/test-position-slug"
        job_id = scraper.extract_job_id(url)
        assert job_id == "eh-test-position-slug"

    def test_extract_job_id_with_hyphens(self, scraper):
        """Test job ID extraction preserves hyphens in slug"""
        url = "https://jobs.employmenthero.com/AU/job/company-name-position-title-id123"
        job_id = scraper.extract_job_id(url)
        assert job_id == "eh-company-name-position-title-id123"

    def test_extract_job_id_invalid_url(self, scraper):
        """Test job ID extraction from invalid URL returns None"""
        assert scraper.extract_job_id("https://invalid.com/job") is None
        assert scraper.extract_job_id("not-a-url") is None
        assert scraper.extract_job_id("") is None


class TestExtractJobMetadata:
    """Tests for extract_job_metadata method"""

    @pytest.fixture
    def scraper(self, test_database):
        """Create scraper instance"""
        return EmploymentHeroScraper(delay_between_requests=1.0, database=test_database)

    def test_extract_metadata_standard_selectors(self, scraper):
        """Test metadata extraction with standard CSS selectors"""
        html = """
        <html>
            <h1 class="job-title">Senior Software Engineer</h1>
            <div class="company-name">aXcelerate</div>
        </html>
        """
        soup = BeautifulSoup(html, "html.parser")
        metadata = scraper.extract_job_metadata(soup)

        assert metadata["title"] == "Senior Software Engineer"
        assert metadata["company"] == "aXcelerate"

    def test_extract_metadata_alternative_selectors(self, scraper):
        """Test metadata extraction with alternative selectors"""
        html = """
        <html>
            <h1>Frontend Developer</h1>
            <a class="company">Test Company Pty Ltd</a>
        </html>
        """
        soup = BeautifulSoup(html, "html.parser")
        metadata = scraper.extract_job_metadata(soup)

        assert metadata["title"] == "Frontend Developer"
        assert metadata["company"] == "Test Company Pty Ltd"

    def test_extract_metadata_from_meta_tags(self, scraper):
        """Test metadata extraction falls back to meta tags"""
        html = """
        <html>
            <head>
                <meta property="og:site_name" content="Meta Company"/>
            </head>
            <body>
                <h1>Developer Position</h1>
            </body>
        </html>
        """
        soup = BeautifulSoup(html, "html.parser")
        metadata = scraper.extract_job_metadata(soup)

        assert metadata["title"] == "Developer Position"
        assert metadata["company"] == "Meta Company"

    def test_extract_metadata_defaults_when_missing(self, scraper):
        """Test default values when metadata not found"""
        html = "<html><body></body></html>"
        soup = BeautifulSoup(html, "html.parser")
        metadata = scraper.extract_job_metadata(soup)

        assert metadata["title"] == "Unknown Job"
        assert metadata["company"] == "Unknown Company"


class TestCleanJobDescription:
    """Tests for clean_job_description method"""

    @pytest.fixture
    def scraper(self, test_database):
        """Create scraper instance"""
        return EmploymentHeroScraper(delay_between_requests=1.0, database=test_database)

    def test_clean_description_standard_selector(self, scraper):
        """Test description extraction with standard selector"""
        html = """
        <html>
            <div class="job-description">
                <h2>About the Role</h2>
                <p>We are seeking a talented developer.</p>
                <h3>Requirements</h3>
                <ul>
                    <li>5+ years experience</li>
                    <li>Python knowledge</li>
                </ul>
            </div>
        </html>
        """
        soup = BeautifulSoup(html, "html.parser")
        description = scraper.clean_job_description(soup)

        assert description is not None
        assert "About the Role" in description
        assert "talented developer" in description
        assert "Requirements" in description
        assert "5+ years experience" in description

    def test_clean_description_removes_unwanted_sections(self, scraper):
        """Test unwanted sections are removed"""
        html = """
        <html>
            <div class="job-description">
                <p>Main job content here</p>
                <div class="company-profile">Company profile content</div>
                <nav>Navigation content</nav>
            </div>
        </html>
        """
        soup = BeautifulSoup(html, "html.parser")
        description = scraper.clean_job_description(soup)

        assert "Main job content" in description
        assert "Company profile" not in description
        assert "Navigation" not in description

    def test_clean_description_removes_duplicates(self, scraper):
        """Test consecutive duplicate lines are removed"""
        html = """
        <html>
            <div class="job-description">
                <p>Line one</p>
                <p>Line one</p>
                <p>Line two</p>
            </div>
        </html>
        """
        soup = BeautifulSoup(html, "html.parser")
        description = scraper.clean_job_description(soup)

        # Should only have one "Line one"
        assert description.count("Line one") == 1
        assert "Line two" in description

    def test_clean_description_content_based_fallback(self, scraper):
        """Test content-based fallback when no standard selectors found"""
        html = """
        <html>
            <section>
                <p>About the role: This is a great opportunity with requirements
                including experience in software development and skills in Python, JavaScript,
                and modern frameworks. We are looking for someone with at least 5 years of
                experience in building scalable web applications. The position involves working
                with cross-functional teams to deliver high-quality software solutions.</p>
            </section>
        </html>
        """
        soup = BeautifulSoup(html, "html.parser")
        description = scraper.clean_job_description(soup)

        assert description is not None
        assert "requirements" in description.lower()
        assert "experience" in description.lower()

    def test_clean_description_empty_content_returns_none(self, scraper):
        """Test empty content returns None"""
        html = "<html><body></body></html>"
        soup = BeautifulSoup(html, "html.parser")
        description = scraper.clean_job_description(soup)

        assert description is None


class TestGetSourceName:
    """Tests for get_source_name method"""

    @pytest.fixture
    def scraper(self, test_database):
        """Create scraper instance"""
        return EmploymentHeroScraper(delay_between_requests=1.0, database=test_database)

    def test_get_source_name(self, scraper):
        """Test source name is correctly returned"""
        assert scraper.get_source_name() == "Employment Hero"


class TestSessionSetup:
    """Tests for session configuration"""

    @pytest.fixture
    def scraper(self, test_database):
        """Create scraper instance"""
        return EmploymentHeroScraper(delay_between_requests=1.0, database=test_database)

    def test_session_headers_configured(self, scraper):
        """Test session has proper headers configured"""
        assert "User-Agent" in scraper.session.headers
        assert "Mozilla" in scraper.session.headers["User-Agent"]
        assert "Sec-Fetch-Dest" in scraper.session.headers

    def test_request_headers_include_referer(self, scraper):
        """Test request headers include Employment Hero referer"""
        headers = scraper._get_request_headers("https://jobs.employmenthero.com/AU/job/test")
        assert headers["Referer"] == "https://jobs.employmenthero.com/"
