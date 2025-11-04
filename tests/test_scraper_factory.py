"""Tests for scraper factory module"""

import pytest

from applyr.scraper import SEEKScraper
from applyr.scraper_employment_hero import EmploymentHeroScraper
from applyr.scraper_factory import create_scraper, detect_job_source, normalize_to_url


class TestDetectJobSource:
    """Tests for job source detection"""

    def test_detect_seek_id(self):
        """Test SEEK 8-digit ID detection"""
        assert detect_job_source("12345678") == "seek"
        assert detect_job_source("12345678") == "seek"
        assert detect_job_source("99999999") == "seek"

    def test_detect_seek_url(self):
        """Test SEEK URL detection"""
        assert detect_job_source("https://www.seek.com.au/job/12345678") == "seek"
        assert detect_job_source("http://www.seek.com.au/job/12345678") == "seek"
        assert detect_job_source("https://seek.com.au/job/12345678") == "seek"

    def test_detect_employment_hero_url(self):
        """Test Employment Hero URL detection"""
        url = "https://jobs.employmenthero.com/AU/job/axcelerate-senior-software-engineer-a5y43"
        assert detect_job_source(url) == "employment_hero"

        url2 = "https://jobs.employmenthero.com/job/test-position-slug"
        assert detect_job_source(url2) == "employment_hero"

    def test_detect_indeed_id(self):
        """Test Indeed 16-char hex ID detection"""
        assert detect_job_source("cc76be5d850127ec") == "indeed"
        assert detect_job_source("a1b2c3d4e5f6a7b8") == "indeed"
        assert detect_job_source("0123456789abcdef") == "indeed"

    def test_detect_indeed_url(self):
        """Test Indeed URL detection"""
        url1 = "https://au.indeed.com/viewjob?jk=cc76be5d850127ec"
        assert detect_job_source(url1) == "indeed"

        url2 = "https://au.indeed.com/viewjob?jk=cc76be5d850127ec&from=shareddesktop_copy"
        assert detect_job_source(url2) == "indeed"

        url3 = "https://indeed.com/viewjob?jk=a1b2c3d4e5f6a7b8"
        assert detect_job_source(url3) == "indeed"

    def test_detect_invalid_id_length(self):
        """Test invalid ID length raises ValueError"""
        with pytest.raises(ValueError, match="Could not determine"):
            detect_job_source("123")

        with pytest.raises(ValueError, match="Could not determine"):
            detect_job_source("1234567")  # 7 digits

        with pytest.raises(ValueError, match="Could not determine"):
            detect_job_source("123456789")  # 9 digits

    def test_detect_unsupported_domain(self):
        """Test unsupported domain raises ValueError"""
        # LinkedIn is detected but requires manual import (error raised in create_scraper)
        assert detect_job_source("https://linkedin.com/job/12345") == "linkedin"

        # Truly unsupported domains should raise ValueError
        with pytest.raises(ValueError, match="Unsupported job board domain"):
            detect_job_source("https://glassdoor.com/job/abc123")

    def test_detect_malformed_url(self):
        """Test malformed URL raises ValueError"""
        with pytest.raises(ValueError):
            detect_job_source("not-a-url")

        with pytest.raises(ValueError):
            detect_job_source("abc123def")  # Not 8 digits, not URL

    def test_detect_empty_string(self):
        """Test empty string raises ValueError"""
        with pytest.raises(ValueError):
            detect_job_source("")

        with pytest.raises(ValueError):
            detect_job_source("   ")  # Whitespace only


class TestNormalizeToUrl:
    """Tests for URL normalization"""

    def test_normalize_seek_id(self):
        """Test SEEK ID normalization to URL"""
        result = normalize_to_url("12345678", "seek")
        assert result == "https://www.seek.com.au/job/12345678"

    def test_normalize_seek_url_passthrough(self):
        """Test SEEK URL passes through unchanged"""
        url = "https://www.seek.com.au/job/12345678"
        result = normalize_to_url(url, "seek")
        assert result == url

    def test_normalize_employment_hero_url_passthrough(self):
        """Test Employment Hero URL passes through unchanged"""
        url = "https://jobs.employmenthero.com/AU/job/test-slug"
        result = normalize_to_url(url, "employment_hero")
        assert result == url

    def test_normalize_indeed_id(self):
        """Test Indeed ID normalization to URL"""
        result = normalize_to_url("cc76be5d850127ec", "indeed")
        assert result == "https://au.indeed.com/viewjob?jk=cc76be5d850127ec"

    def test_normalize_indeed_url_passthrough(self):
        """Test Indeed URL passes through unchanged"""
        url = "https://au.indeed.com/viewjob?jk=cc76be5d850127ec"
        result = normalize_to_url(url, "indeed")
        assert result == url

        url2 = "https://au.indeed.com/viewjob?jk=cc76be5d850127ec&from=shareddesktop_copy"
        result2 = normalize_to_url(url2, "indeed")
        assert result2 == url2

    def test_normalize_invalid_source(self):
        """Test normalization with invalid source raises ValueError"""
        with pytest.raises(ValueError):
            normalize_to_url("12345678", "invalid_source")

    def test_normalize_non_url_non_seek_id(self):
        """Test normalization of invalid input raises ValueError"""
        with pytest.raises(ValueError):
            normalize_to_url("not-a-url", "seek")


class TestCreateScraper:
    """Tests for scraper factory"""

    def test_create_seek_scraper_from_id(self, test_database):
        """Test creating SEEK scraper from 8-digit ID"""
        scraper, url = create_scraper("12345678", delay=2.0, database=test_database)

        assert isinstance(scraper, SEEKScraper)
        assert url == "https://www.seek.com.au/job/12345678"
        assert scraper.delay == 2.0
        assert scraper.database == test_database

    def test_create_seek_scraper_from_url(self, test_database):
        """Test creating SEEK scraper from full URL"""
        url = "https://www.seek.com.au/job/12345678"
        scraper, norm_url = create_scraper(url, delay=3.0, database=test_database)

        assert isinstance(scraper, SEEKScraper)
        assert norm_url == url
        assert scraper.delay == 3.0

    def test_create_employment_hero_scraper(self, test_database):
        """Test creating Employment Hero scraper from URL"""
        url = "https://jobs.employmenthero.com/AU/job/test-slug"
        scraper, norm_url = create_scraper(url, delay=2.5, database=test_database)

        assert isinstance(scraper, EmploymentHeroScraper)
        assert norm_url == url
        assert scraper.delay == 2.5
        assert scraper.database == test_database

    def test_create_scraper_without_database(self):
        """Test creating scraper without database parameter"""
        scraper, url = create_scraper("12345678")

        assert isinstance(scraper, SEEKScraper)
        assert scraper.database is None

    def test_create_scraper_default_delay(self):
        """Test scraper created with default delay"""
        scraper, _ = create_scraper("12345678")
        assert scraper.delay == 2.0

    def test_create_scraper_unsupported_source(self):
        """Test creating scraper with unsupported source raises ValueError"""
        with pytest.raises(ValueError):
            create_scraper("https://linkedin.com/job/12345")

    def test_create_scraper_invalid_id(self):
        """Test creating scraper with invalid ID raises ValueError"""
        with pytest.raises(ValueError):
            create_scraper("123")  # Not 8 digits

    def test_scraper_has_source_name(self):
        """Test scrapers have correct source names"""
        seek_scraper, _ = create_scraper("12345678")
        assert seek_scraper.get_source_name() == "SEEK"

        eh_url = "https://jobs.employmenthero.com/AU/job/test"
        eh_scraper, _ = create_scraper(eh_url)
        assert eh_scraper.get_source_name() == "Employment Hero"
