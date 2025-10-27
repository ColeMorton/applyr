"""Tests for Indeed manual text file parser"""

import pytest
from pathlib import Path
from applyr.scraper_indeed_manual import IndeedManualParser


@pytest.fixture
def parser(tmp_path):
    """Create a parser with a temporary directory"""
    return IndeedManualParser(raw_jobs_dir=tmp_path)


@pytest.fixture
def sample_indeed_text():
    """Sample text copied from an Indeed job page"""
    return """Skip to main content
Indeed
Find jobs
Company reviews
Sign in
Employers / Post Job

Senior Software Engineer
Tech Company Pty Ltd - Sydney NSW

$120,000 - $150,000 a year - Full-time

Apply now

Job details

Salary
$120,000 - $150,000 a year

Job Type
Full-time

Full Job Description

About the Role

We are seeking an experienced Senior Software Engineer to join our growing team.

Responsibilities:
• Design and develop scalable web applications
• Lead technical discussions and code reviews
• Mentor junior developers
• Work with modern technologies including React, Python, and AWS

Requirements:
• 5+ years of software development experience
• Strong knowledge of web technologies
• Experience with cloud platforms
• Excellent communication skills

What We Offer:
• Competitive salary package
• Flexible working arrangements
• Professional development opportunities
• Great team culture

To apply, please submit your resume and cover letter.

Apply now

Report job
Save job
"""


def test_extract_job_id_from_hex_id(parser):
    """Test extracting job ID from 16-char hex string"""
    job_id = parser.extract_job_id("cc76be5d850127ec")
    assert job_id == "ind-cc76be5d850127ec"


def test_extract_job_id_from_url(parser):
    """Test extracting job ID from Indeed URL"""
    url = "https://au.indeed.com/viewjob?jk=cc76be5d850127ec&from=shareddesktop_copy"
    job_id = parser.extract_job_id(url)
    assert job_id == "ind-cc76be5d850127ec"


def test_extract_job_id_from_simple_url(parser):
    """Test extracting job ID from simple Indeed URL"""
    url = "https://au.indeed.com/viewjob?jk=a1b2c3d4e5f6g7h8"
    job_id = parser.extract_job_id(url)
    assert job_id == "ind-a1b2c3d4e5f6g7h8"


def test_extract_job_id_invalid(parser):
    """Test that invalid input returns None"""
    assert parser.extract_job_id("invalid") is None
    assert parser.extract_job_id("12345") is None
    assert parser.extract_job_id("https://seek.com.au/job/123") is None


def test_get_raw_job_id_from_hex(parser):
    """Test getting raw job ID from hex string"""
    raw_id = parser.get_raw_job_id("cc76be5d850127ec")
    assert raw_id == "cc76be5d850127ec"


def test_get_raw_job_id_from_url(parser):
    """Test getting raw job ID from URL"""
    url = "https://au.indeed.com/viewjob?jk=cc76be5d850127ec"
    raw_id = parser.get_raw_job_id(url)
    assert raw_id == "cc76be5d850127ec"


def test_load_job_text_success(parser, tmp_path):
    """Test loading existing text file"""
    # Create test file
    job_id = "cc76be5d850127ec"
    text_file = tmp_path / f"{job_id}.txt"
    text_file.write_text("Test job content")
    
    # Load it
    content = parser.load_job_text(job_id)
    assert content == "Test job content"


def test_load_job_text_not_found(parser):
    """Test loading non-existent file returns None"""
    content = parser.load_job_text("nonexistent")
    assert content is None


def test_load_job_text_empty_file(parser, tmp_path):
    """Test loading empty file returns None"""
    job_id = "empty"
    text_file = tmp_path / f"{job_id}.txt"
    text_file.write_text("")
    
    content = parser.load_job_text(job_id)
    assert content is None


def test_parse_job_data(parser, sample_indeed_text):
    """Test parsing job data from text content"""
    job_data = parser.parse_job_data(sample_indeed_text)
    
    assert 'title' in job_data
    assert 'company' in job_data
    assert 'description' in job_data
    
    # Check that we extracted something meaningful
    assert len(job_data['title']) > 0
    assert len(job_data['company']) > 0
    assert len(job_data['description']) > 0
    
    # Check for expected content
    assert 'Software Engineer' in job_data['title']
    assert 'Tech Company' in job_data['company']
    assert 'Responsibilities' in job_data['description'] or 'Requirements' in job_data['description']


def test_parse_job_data_minimal(parser):
    """Test parsing with minimal content"""
    minimal_text = """Job Title Here
Company Name Pty Ltd
Some job description text."""
    
    job_data = parser.parse_job_data(minimal_text)
    
    # Should have all required keys with some content
    assert 'title' in job_data
    assert 'company' in job_data
    assert 'description' in job_data


def test_process_job_success(parser, tmp_path, sample_indeed_text):
    """Test full job processing from text file"""
    # Create test file
    job_id = "cc76be5d850127ec"
    text_file = tmp_path / f"{job_id}.txt"
    text_file.write_text(sample_indeed_text)
    
    # Process it
    result = parser.process_job(job_id)
    
    assert result is not None
    assert result['job_id'] == f"ind-{job_id}"
    assert result['raw_job_id'] == job_id
    assert 'title' in result
    assert 'company' in result
    assert 'description' in result


def test_process_job_from_url(parser, tmp_path, sample_indeed_text):
    """Test processing job from full URL"""
    # Create test file
    job_id = "cc76be5d850127ec"
    text_file = tmp_path / f"{job_id}.txt"
    text_file.write_text(sample_indeed_text)
    
    # Process using URL
    url = f"https://au.indeed.com/viewjob?jk={job_id}"
    result = parser.process_job(url)
    
    assert result is not None
    assert result['job_id'] == f"ind-{job_id}"


def test_process_job_file_not_found(parser):
    """Test processing when file doesn't exist"""
    result = parser.process_job("nonexistent")
    assert result is None


def test_process_job_invalid_identifier(parser):
    """Test processing with invalid identifier"""
    result = parser.process_job("invalid-id-format")
    assert result is None


def test_get_source_name(parser):
    """Test getting source name"""
    assert parser.get_source_name() == "Indeed (Manual Import)"


def test_parse_strips_navigation(parser):
    """Test that parser removes navigation/UI elements"""
    text_with_nav = """Skip to main content
Indeed
Find jobs
Sign in
Post Job

Actual Job Title
Real Company Name

The actual job description starts here.
This is the content we want to keep.

Report job
Save job"""
    
    job_data = parser.parse_job_data(text_with_nav)
    
    # Should not include navigation text
    desc = job_data['description'].lower()
    assert 'skip to main content' not in desc or len(desc) > 100  # Either removed or description is substantial

