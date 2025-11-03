"""Shared pytest fixtures for applyr tests"""

from collections.abc import Generator
from pathlib import Path
import shutil
import tempfile

import pytest
import responses
from rich.console import Console
from typer.testing import CliRunner

from applyr.database import ApplicationDatabase


@pytest.fixture
def runner() -> CliRunner:
    """Create Typer CLI test runner"""
    return CliRunner()


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test files"""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def test_console() -> Console:
    """Create a Rich console for testing"""
    return Console()


@pytest.fixture
def test_database(temp_dir: Path, test_console: Console) -> ApplicationDatabase:
    """Create a test database instance with temporary CSV"""
    csv_path = temp_dir / "test_advertisements.csv"
    return ApplicationDatabase(csv_path=csv_path, console=test_console)


@pytest.fixture
def mock_responses():
    """Setup responses mock for HTTP requests"""
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        yield rsps


@pytest.fixture
def sample_seek_html() -> str:
    """Sample SEEK job HTML for testing"""
    return """
    <html>
        <head>
            <title>Software Engineer - Test Company</title>
        </head>
        <body>
            <h1 data-automation="job-detail-title">Software Engineer</h1>
            <span data-automation="advertiser-name">Test Company Pty Ltd</span>
            <div data-automation="jobAdDetails">
                <h2>About the Role</h2>
                <p>We are looking for a talented Software Engineer to join our team.</p>
                <h3>Requirements</h3>
                <ul>
                    <li>5+ years of experience</li>
                    <li>Python, JavaScript knowledge</li>
                    <li>Strong communication skills</li>
                </ul>
            </div>
        </body>
    </html>
    """


@pytest.fixture
def sample_eh_html() -> str:
    """Sample Employment Hero job HTML for testing"""
    return """
    <html>
        <head>
            <title>Senior Developer - aXcelerate</title>
        </head>
        <body>
            <h1 class="job-title">Senior Software Engineer</h1>
            <div class="company-name">aXcelerate</div>
            <div class="job-description">
                <h2>About us</h2>
                <p>aXcelerate is a leading SaaS provider.</p>
                <h2>The role</h2>
                <p>As a Senior Software Engineer, you will lead development.</p>
                <h3>Requirements</h3>
                <ul>
                    <li>React experience</li>
                    <li>TypeScript expertise</li>
                    <li>Team leadership</li>
                </ul>
            </div>
        </body>
    </html>
    """


@pytest.fixture
def sample_job_data() -> dict:
    """Sample job data for testing"""
    return {
        "job_id": "12345678",
        "company_name": "Test Company",
        "job_title": "Software Engineer",
        "source": "SEEK",
        "url": "https://www.seek.com.au/job/12345678",
    }


@pytest.fixture
def sample_html_resume(temp_dir: Path) -> Path:
    """Create a sample HTML resume file"""
    resume_content = """<!DOCTYPE html>
<html>
<head>
    <title>John Doe - Software Engineer</title>
</head>
<body>
    <h1>John Doe</h1>
    <p>Email: john.doe@example.com</p>
    <p>Phone: 555-123-4567</p>
    <p>Location: San Francisco, CA</p>
    <p>LinkedIn: linkedin.com/in/johndoe</p>

    <h2>Experience</h2>
    <h3>Senior Software Engineer</h3>
    <p>Tech Company Inc. - Jan 2020 - Present</p>
    <ul>
        <li>Developed scalable web applications using Python and React</li>
        <li>Increased system performance by 40% through optimization</li>
        <li>Led team of 5 developers</li>
    </ul>

    <h2>Skills</h2>
    <ul>
        <li>Python, JavaScript, TypeScript</li>
        <li>React, Node.js, Django</li>
        <li>AWS, Docker, Kubernetes</li>
    </ul>

    <h2>Education</h2>
    <p>BS Computer Science, University of California, 2015</p>
</body>
</html>"""
    resume_file = temp_dir / "resume.html"
    resume_file.write_text(resume_content)
    return resume_file


@pytest.fixture
def sample_text_resume(temp_dir: Path) -> Path:
    """Create a sample text/markdown resume file"""
    resume_content = """# John Doe

Email: john.doe@example.com
Phone: 555-123-4567
Location: San Francisco, CA
LinkedIn: linkedin.com/in/johndoe

## Experience

### Senior Software Engineer
Tech Company Inc. - Jan 2020 - Present

- Developed scalable web applications using Python and React
- Increased system performance by 40% through optimization
- Led team of 5 developers
- Managed $2M+ budget projects

## Skills

- Python, JavaScript, TypeScript
- React, Node.js, Django
- AWS, Docker, Kubernetes
- Agile, Scrum, TDD

## Education

BS Computer Science, University of California, 2015
"""
    resume_file = temp_dir / "resume.txt"
    resume_file.write_text(resume_content)
    return resume_file


@pytest.fixture
def sample_resume_with_emojis(temp_dir: Path) -> Path:
    """Create a sample resume with emojis"""
    resume_content = """# John Doe 😊

Email: john.doe@example.com 📧
Phone: 555-123-4567

## Experience ✨

Senior Software Engineer at Tech Company
"""
    resume_file = temp_dir / "resume_emoji.txt"
    resume_file.write_text(resume_content)
    return resume_file


@pytest.fixture
def sample_resume_missing_sections(temp_dir: Path) -> Path:
    """Create a sample resume missing critical sections"""
    resume_content = """# John Doe

Some basic information here.
No contact info, no experience section, no skills.
"""
    resume_file = temp_dir / "resume_incomplete.txt"
    resume_file.write_text(resume_content)
    return resume_file


@pytest.fixture
def sample_resume_complex_html(temp_dir: Path) -> Path:
    """Create a sample resume with complex HTML structure"""
    resume_content = """<!DOCTYPE html>
<html>
<head><title>Resume</title></head>
<body>
    <div class="skills-grid">
        <span class="skill-tag">Python</span>
        <span class="skill-tag">JavaScript</span>
    </div>
    <table>
        <tr><td>Experience</td><td>5 years</td></tr>
    </table>
    <div class="grid">
        <div>Complex layout</div>
    </div>
</body>
</html>"""
    resume_file = temp_dir / "resume_complex.html"
    resume_file.write_text(resume_content)
    return resume_file


@pytest.fixture
def sample_job_description(temp_dir: Path) -> Path:
    """Create a sample job description file"""
    job_desc = """Software Engineer Position

Requirements:
- Python, JavaScript, React
- 5+ years of experience
- AWS, Docker experience
- Agile methodologies
- Strong communication skills
- Team leadership
"""
    job_file = temp_dir / "job_description.txt"
    job_file.write_text(job_desc)
    return job_file
