"""Test utility functions for applyr tests"""

from pathlib import Path
from typing import Any


def create_test_resume_html(content: str = None) -> str:
    """Create a test HTML resume file content"""
    if content is None:
        content = """<!DOCTYPE html>
<html>
<head><title>Test Resume</title></head>
<body>
    <h1>John Doe</h1>
    <p>Email: john.doe@example.com</p>
    <p>Phone: 555-123-4567</p>
    <h2>Experience</h2>
    <p>Software Engineer at Tech Company</p>
    <h2>Skills</h2>
    <ul>
        <li>Python</li>
        <li>JavaScript</li>
    </ul>
</body>
</html>"""
    return content


def create_test_resume_text(content: str = None) -> str:
    """Create a test text resume file content"""
    if content is None:
        content = """# John Doe

Email: john.doe@example.com
Phone: 555-123-4567

## Experience

Software Engineer at Tech Company

## Skills

- Python
- JavaScript
"""
    return content


def create_test_job_description(content: str = None) -> str:
    """Create a test job description file content"""
    if content is None:
        content = """Software Engineer Position

Requirements:
- Python, JavaScript, React
- 5+ years of experience
- AWS, Docker experience
"""
    return content


def assert_file_exists(file_path: Path, description: str = "File") -> None:
    """Assert that a file exists with a descriptive error message"""
    assert file_path.exists(), f"{description} should exist at {file_path}"


def assert_file_contains(file_path: Path, text: str, description: str = "File") -> None:
    """Assert that a file contains specific text"""
    assert_file_exists(file_path, description)
    content = file_path.read_text()
    assert text in content, f"{description} should contain '{text}'"


def assert_pdf_valid(pdf_path: Path) -> None:
    """Assert that a PDF file is valid"""
    assert_file_exists(pdf_path, "PDF file")
    assert pdf_path.stat().st_size > 100, "PDF file should be more than 100 bytes"
    with open(pdf_path, "rb") as f:
        header = f.read(4)
        assert header.startswith(b"%PDF"), "PDF file should start with %PDF header"


def assert_job_file_format(file_path: Path, job_id: str) -> None:
    """Assert that a job file follows the expected naming format"""
    assert_file_exists(file_path, "Job file")
    assert job_id in file_path.name, f"Job file name should contain job ID {job_id}"


def create_sample_job_markdown(job_id: str, title: str, company: str, content: str = None) -> str:
    """Create sample job markdown file content"""
    if content is None:
        content = "Job description content here."
    return f"""# {title}

**Company:** {company}
**Job ID:** {job_id}
**Source:** SEEK
**Scraped:** 2025-01-15 10:30:00

---

{content}
"""


def assert_dict_contains_keys(data: dict[str, Any], required_keys: list[str]) -> None:
    """Assert that a dictionary contains all required keys"""
    for key in required_keys:
        assert key in data, f"Dictionary should contain key '{key}'"


def assert_dict_has_type(data: dict[str, Any], key: str, expected_type: type) -> None:
    """Assert that a dictionary value has the expected type"""
    assert key in data, f"Dictionary should contain key '{key}'"
    assert isinstance(data[key], expected_type), f"Value for '{key}' should be {expected_type.__name__}"


def assert_score_range(score: float, min_score: float = 0.0, max_score: float = 100.0) -> None:
    """Assert that a score is within the expected range"""
    assert min_score <= score <= max_score, f"Score {score} should be between {min_score} and {max_score}"


def assert_list_not_empty(items: list, description: str = "List") -> None:
    """Assert that a list is not empty"""
    assert len(items) > 0, f"{description} should not be empty"


def assert_list_contains(items: list, item: Any, description: str = "List") -> None:
    """Assert that a list contains a specific item"""
    assert item in items, f"{description} should contain {item}"
