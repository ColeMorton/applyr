"""Tests for LinkedIn manual parser module"""

from pathlib import Path

from applyr.scraper_linkedin_manual import LinkedInManualParser


class TestLinkedInManualParserInitialization:
    """Tests for LinkedInManualParser initialization"""

    def test_init_with_default_directory(self):
        """Test initialization with default directory"""
        parser = LinkedInManualParser()
        assert parser.raw_jobs_dir == Path("data/raw/jobs/linked_in")

    def test_init_with_custom_directory(self, temp_dir: Path):
        """Test initialization with custom directory"""
        parser = LinkedInManualParser(raw_jobs_dir=temp_dir)
        assert parser.raw_jobs_dir == temp_dir


class TestExtractJobId:
    """Tests for extract_job_id method"""

    def test_extract_id_from_numeric_id(self):
        """Test extraction from numeric ID"""
        parser = LinkedInManualParser()
        job_id = parser.extract_job_id("3871589110")

        assert job_id == "li-3871589110"

    def test_extract_id_from_url(self):
        """Test extraction from LinkedIn URL"""
        parser = LinkedInManualParser()
        url = "https://www.linkedin.com/jobs/view/3871589110/"
        job_id = parser.extract_job_id(url)

        assert job_id == "li-3871589110"

    def test_extract_id_from_url_with_query(self):
        """Test extraction from URL with query parameters"""
        parser = LinkedInManualParser()
        url = "https://www.linkedin.com/jobs/view/3871589110?some=param"
        job_id = parser.extract_job_id(url)

        assert job_id == "li-3871589110"

    def test_extract_id_invalid_format(self):
        """Test extraction from invalid format returns None"""
        parser = LinkedInManualParser()
        job_id = parser.extract_job_id("invalid-id")

        assert job_id is None

    def test_extract_id_non_linkedin_url(self):
        """Test extraction from non-LinkedIn URL returns None"""
        parser = LinkedInManualParser()
        job_id = parser.extract_job_id("https://example.com/job/123")

        assert job_id is None

    def test_extract_id_empty_string(self):
        """Test extraction from empty string returns None"""
        parser = LinkedInManualParser()
        job_id = parser.extract_job_id("")

        assert job_id is None

    def test_extract_id_whitespace(self):
        """Test extraction handles whitespace"""
        parser = LinkedInManualParser()
        job_id = parser.extract_job_id("  3871589110  ")

        assert job_id == "li-3871589110"


class TestGetRawJobId:
    """Tests for get_raw_job_id method"""

    def test_get_raw_id_from_numeric(self):
        """Test getting raw ID from numeric string"""
        parser = LinkedInManualParser()
        raw_id = parser.get_raw_job_id("3871589110")

        assert raw_id == "3871589110"

    def test_get_raw_id_from_url(self):
        """Test getting raw ID from URL"""
        parser = LinkedInManualParser()
        url = "https://www.linkedin.com/jobs/view/3871589110/"
        raw_id = parser.get_raw_job_id(url)

        assert raw_id == "3871589110"

    def test_get_raw_id_invalid_format(self):
        """Test getting raw ID from invalid format returns None"""
        parser = LinkedInManualParser()
        raw_id = parser.get_raw_job_id("invalid")

        assert raw_id is None


class TestLoadJobText:
    """Tests for load_job_text method"""

    def test_load_existing_file(self, temp_dir: Path):
        """Test loading existing text file"""
        parser = LinkedInManualParser(raw_jobs_dir=temp_dir)
        job_id = "3871589110"
        text_file = temp_dir / f"{job_id}.txt"
        text_file.write_text("Job description content")

        content = parser.load_job_text(job_id)

        assert content == "Job description content"

    def test_load_nonexistent_file(self, temp_dir: Path):
        """Test loading non-existent file returns None"""
        parser = LinkedInManualParser(raw_jobs_dir=temp_dir)
        content = parser.load_job_text("nonexistent")

        assert content is None

    def test_load_empty_file(self, temp_dir: Path):
        """Test loading empty file returns None"""
        parser = LinkedInManualParser(raw_jobs_dir=temp_dir)
        job_id = "empty"
        text_file = temp_dir / f"{job_id}.txt"
        text_file.write_text("")

        content = parser.load_job_text(job_id)

        assert content is None

    def test_load_file_with_whitespace_only(self, temp_dir: Path):
        """Test loading file with only whitespace returns None"""
        parser = LinkedInManualParser(raw_jobs_dir=temp_dir)
        job_id = "whitespace"
        text_file = temp_dir / f"{job_id}.txt"
        text_file.write_text("   \n\n  \t  ")

        content = parser.load_job_text(job_id)

        assert content is None


class TestParseJobData:
    """Tests for parse_job_data method"""

    def test_parse_standard_linkedin_text(self):
        """Test parsing standard LinkedIn job text"""
        parser = LinkedInManualParser()
        text = """Skip to main content
LinkedIn
Sign in

Senior Software Engineer
Tech Company Inc - Sydney NSW

$120,000 - $150,000 a year

Apply now

Job details

About the Role

We are seeking an experienced Senior Software Engineer to join our team.

Responsibilities:
• Design and develop scalable applications
• Lead technical discussions
• Mentor junior developers

Requirements:
• 5+ years of experience
• Python, JavaScript knowledge
• Strong communication skills
"""
        job_data = parser.parse_job_data(text)

        assert "title" in job_data
        assert "company" in job_data
        assert "location" in job_data
        assert "description" in job_data
        assert job_data["title"] != "Unknown Job"
        assert job_data["company"] != "Unknown Company"

    def test_parse_title_extraction(self):
        """Test title extraction from text"""
        parser = LinkedInManualParser()
        text = """Skip to main content
LinkedIn

Senior Software Engineer
Tech Company Inc
Sydney, NSW

About the Role
Job description here.
"""
        job_data = parser.parse_job_data(text)

        assert "Senior Software Engineer" in job_data["title"]

    def test_parse_company_extraction(self):
        """Test company extraction from text"""
        parser = LinkedInManualParser()
        text = """Job Title
Tech Company Pty Ltd
Location

Job description
"""
        job_data = parser.parse_job_data(text)

        assert "Tech Company" in job_data["company"] or job_data["company"] != "Unknown Company"

    def test_parse_location_extraction(self):
        """Test location extraction from text"""
        parser = LinkedInManualParser()
        text = """Job Title
Company Name
Sydney, NSW

Job description
"""
        job_data = parser.parse_job_data(text)

        assert "Sydney" in job_data["location"] or job_data["location"] != "Unknown Location"

    def test_parse_description_extraction(self):
        """Test description extraction from text"""
        parser = LinkedInManualParser()
        text = """Job Title
Company Name

About the Role

This is a great opportunity for a software engineer.
You will work on exciting projects.
Responsibilities include development and testing.
"""
        job_data = parser.parse_job_data(text)

        assert len(job_data["description"]) > 0
        assert "About the Role" in job_data["description"] or "opportunity" in job_data["description"]

    def test_parse_skips_navigation_text(self):
        """Test that navigation text is skipped"""
        parser = LinkedInManualParser()
        text = """Skip to main content
LinkedIn
Sign in
Post Job

Actual Job Title
Real Company Name
Real Location

About the Role
Real job description content here.
"""
        job_data = parser.parse_job_data(text)

        assert "Skip to main content" not in job_data["title"]
        assert "Sign in" not in job_data["title"]

    def test_parse_returns_defaults_when_empty(self):
        """Test parsing empty text returns defaults"""
        parser = LinkedInManualParser()
        text = ""
        job_data = parser.parse_job_data(text)

        assert job_data["title"] == "Unknown Job"
        assert job_data["company"] == "Unknown Company"
        assert job_data["location"] == "Unknown Location"

    def test_parse_handles_exceptions(self):
        """Test that parsing handles exceptions gracefully"""
        parser = LinkedInManualParser()
        # Create text that might cause issues
        text = "Some text"
        job_data = parser.parse_job_data(text)

        assert isinstance(job_data, dict)
        assert "title" in job_data
        assert "company" in job_data
        assert "location" in job_data
        assert "description" in job_data


class TestProcessJob:
    """Tests for process_job method"""

    def test_process_job_success(self, temp_dir: Path):
        """Test successful job processing"""
        parser = LinkedInManualParser(raw_jobs_dir=temp_dir)
        job_id = "3871589110"
        text_file = temp_dir / f"{job_id}.txt"
        text_file.write_text("""Senior Software Engineer
Tech Company Inc
Sydney, NSW

About the Role
Job description content.
""")

        result = parser.process_job(job_id)

        assert result is not None
        assert result["job_id"] == "li-3871589110"
        assert result["raw_job_id"] == job_id
        assert "title" in result
        assert "company" in result
        assert "location" in result
        assert "description" in result

    def test_process_job_from_url(self, temp_dir: Path):
        """Test processing job from URL"""
        parser = LinkedInManualParser(raw_jobs_dir=temp_dir)
        job_id = "3871589110"
        text_file = temp_dir / f"{job_id}.txt"
        text_file.write_text("Job content")
        url = f"https://www.linkedin.com/jobs/view/{job_id}/"

        result = parser.process_job(url)

        assert result is not None
        assert result["job_id"] == "li-3871589110"
        assert result["raw_job_id"] == job_id

    def test_process_job_file_not_found(self, temp_dir: Path):
        """Test processing when file doesn't exist"""
        parser = LinkedInManualParser(raw_jobs_dir=temp_dir)
        result = parser.process_job("nonexistent")

        assert result is None

    def test_process_job_invalid_id(self, temp_dir: Path):
        """Test processing with invalid ID"""
        parser = LinkedInManualParser(raw_jobs_dir=temp_dir)
        result = parser.process_job("invalid-id")

        assert result is None

    def test_process_job_empty_file(self, temp_dir: Path):
        """Test processing with empty file"""
        parser = LinkedInManualParser(raw_jobs_dir=temp_dir)
        job_id = "empty"
        text_file = temp_dir / f"{job_id}.txt"
        text_file.write_text("")

        result = parser.process_job(job_id)

        assert result is None


class TestGetSourceName:
    """Tests for get_source_name method"""

    def test_get_source_name(self):
        """Test source name returns correct value"""
        parser = LinkedInManualParser()
        assert parser.get_source_name() == "LinkedIn (Manual Import)"
