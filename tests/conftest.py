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
