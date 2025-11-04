"""Tests for the application database module"""

from datetime import datetime, timedelta

import pandas as pd
import pytest
from rich.console import Console

from applyr.database import ApplicationDatabase, JobStatus, Priority


@pytest.fixture
def sample_jobs():
    """Sample job data for testing"""
    return [
        {
            "job_id": "12345",
            "company_name": "Test Company A",
            "job_title": "Software Engineer",
            "source": "SEEK",
            "url": "https://seek.com.au/job/12345",
            "location": "Sydney",
            "salary_min": 80000,
            "salary_max": 100000,
        },
        {
            "job_id": "67890",
            "company_name": "Test Company B",
            "job_title": "Frontend Developer",
            "source": "SEEK",
            "url": "https://seek.com.au/job/67890",
            "location": "Melbourne",
            "salary_min": 70000,
            "salary_max": 90000,
        },
    ]


class TestApplicationDatabase:
    """Test cases for ApplicationDatabase class"""

    def test_database_initialization(self, test_database, temp_dir):  # noqa: ARG002
        """Test database initialization creates CSV with proper schema"""
        csv_path = temp_dir / "test_advertisements.csv"

        assert csv_path.exists()

        # Check CSV has correct headers
        df = pd.read_csv(csv_path)
        expected_columns = {
            "job_id",
            "company_name",
            "job_title",
            "source",
            "status",
            "priority",
            "date_discovered",
            "date_applied",
            "date_closed",
            "notes",
            "salary_min",
            "salary_max",
            "location",
            "url",
        }
        assert set(df.columns) == expected_columns
        assert len(df) == 0  # Should be empty initially

    def test_add_job_basic(self, test_database):
        """Test adding a basic job to database"""
        success = test_database.add_job(job_id="12345", company_name="Test Company", job_title="Software Engineer")

        assert success is True
        assert test_database.job_exists("12345") is True

        job = test_database.get_job("12345")
        assert job is not None
        assert job["job_id"] == "12345"
        assert job["company_name"] == "Test Company"
        assert job["job_title"] == "Software Engineer"
        assert job["status"] == JobStatus.DISCOVERED.value
        assert job["priority"] == Priority.MEDIUM.value

    def test_add_job_with_all_fields(self, test_database):
        """Test adding a job with all fields populated"""
        success = test_database.add_job(
            job_id="67890",
            company_name="Full Company",
            job_title="Senior Developer",
            source="LinkedIn",
            status=JobStatus.INTERESTED,
            priority=Priority.HIGH,
            url="https://linkedin.com/job/67890",
            location="Brisbane",
            salary_min=90000,
            salary_max=120000,
            notes="Great opportunity with good benefits",
        )

        assert success is True

        job = test_database.get_job("67890")
        assert job["source"] == "LinkedIn"
        assert job["status"] == JobStatus.INTERESTED.value
        assert job["priority"] == Priority.HIGH.value
        assert job["location"] == "Brisbane"
        assert job["salary_min"] == 90000
        assert job["salary_max"] == 120000
        assert job["notes"] == "Great opportunity with good benefits"

    def test_add_duplicate_job(self, test_database):
        """Test that adding duplicate job fails gracefully"""
        # Add first job
        success1 = test_database.add_job(job_id="12345", company_name="Test Company", job_title="Software Engineer")

        # Try to add same job again
        success2 = test_database.add_job(job_id="12345", company_name="Different Company", job_title="Different Title")

        assert success1 is True
        assert success2 is False  # Should fail for duplicate

        # Original job should be unchanged
        job = test_database.get_job("12345")
        assert job["company_name"] == "Test Company"

    def test_update_status(self, test_database):
        """Test updating job status"""
        # Add a job first
        test_database.add_job(job_id="12345", company_name="Test Company", job_title="Software Engineer")

        # Update status to applied
        success = test_database.update_status("12345", JobStatus.APPLIED)
        assert success is True

        job = test_database.get_job("12345")
        assert job["status"] == JobStatus.APPLIED.value
        assert job["date_applied"] == datetime.now().strftime("%Y-%m-%d")

        # Update status to rejected
        success = test_database.update_status("12345", JobStatus.REJECTED)
        assert success is True

        job = test_database.get_job("12345")
        assert job["status"] == JobStatus.REJECTED.value
        assert job["date_closed"] == datetime.now().strftime("%Y-%m-%d")

    def test_update_status_nonexistent_job(self, test_database):
        """Test updating status for non-existent job"""
        success = test_database.update_status("99999", JobStatus.APPLIED)
        assert success is False

    def test_update_job_fields(self, test_database):
        """Test updating various job fields"""
        # Add a job first
        test_database.add_job(job_id="12345", company_name="Test Company", job_title="Software Engineer")

        # Update multiple fields
        success = test_database.update_job(
            "12345", priority=Priority.HIGH, notes="Updated notes", salary_min=85000, location="Sydney"
        )

        assert success is True

        job = test_database.get_job("12345")
        assert job["priority"] == Priority.HIGH.value
        assert job["notes"] == "Updated notes"
        assert job["salary_min"] == 85000
        assert job["location"] == "Sydney"

    def test_get_jobs_by_status(self, test_database, sample_jobs):
        """Test filtering jobs by status"""
        # Add sample jobs with different statuses
        test_database.add_job(**sample_jobs[0], status=JobStatus.DISCOVERED)
        test_database.add_job(**sample_jobs[1], status=JobStatus.APPLIED)

        # Get jobs by status
        discovered_jobs = test_database.get_jobs_by_status(JobStatus.DISCOVERED)
        applied_jobs = test_database.get_jobs_by_status(JobStatus.APPLIED)

        assert len(discovered_jobs) == 1
        assert len(applied_jobs) == 1
        assert discovered_jobs.iloc[0]["job_id"] == "12345"
        assert applied_jobs.iloc[0]["job_id"] == "67890"

    def test_get_jobs_by_company(self, test_database, sample_jobs):
        """Test filtering jobs by company"""
        # Add sample jobs
        for job in sample_jobs:
            test_database.add_job(**job)

        # Search by company
        company_a_jobs = test_database.get_jobs_by_company("Test Company A")
        company_b_jobs = test_database.get_jobs_by_company("Company B")

        assert len(company_a_jobs) == 1
        assert len(company_b_jobs) == 1  # Should match partial name
        assert company_a_jobs.iloc[0]["job_id"] == "12345"

    def test_statistics(self, test_database, sample_jobs):
        """Test application statistics generation"""
        # Add jobs with different statuses
        test_database.add_job(**sample_jobs[0], status=JobStatus.DISCOVERED, priority=Priority.HIGH)
        test_database.add_job(**sample_jobs[1], status=JobStatus.APPLIED, priority=Priority.MEDIUM)

        stats = test_database.get_statistics()

        assert stats["total_jobs"] == 2
        assert stats["by_status"]["discovered"] == 1
        assert stats["by_status"]["applied"] == 1
        assert stats["by_priority"]["high"] == 1
        assert stats["by_priority"]["medium"] == 1
        assert stats["by_company"]["Test Company A"] == 1
        assert stats["by_company"]["Test Company B"] == 1
        assert stats["application_rate"] == 50.0  # 1 applied out of 2 total

    def test_cleanup_old_jobs(self, test_database):
        """Test cleaning up old closed/rejected jobs"""
        # Add jobs with different statuses and dates
        test_database.add_job(
            job_id="12345", company_name="Old Company", job_title="Old Job", status=JobStatus.REJECTED
        )

        test_database.add_job(
            job_id="67890", company_name="Current Company", job_title="Current Job", status=JobStatus.APPLIED
        )

        # Manually update the first job's date to be old
        df = test_database.load_data()
        old_date = (datetime.now() - timedelta(days=35)).strftime("%Y-%m-%d")
        df.loc[df["job_id"] == "12345", "date_discovered"] = old_date
        test_database.save_data(df)

        # Update status to rejected for the old job
        test_database.update_status("12345", JobStatus.REJECTED)

        # Cleanup jobs older than 30 days
        removed_count = test_database.cleanup_old_jobs(days_old=30)

        assert removed_count == 1
        assert not test_database.job_exists("12345")  # Should be removed
        assert test_database.job_exists("67890")  # Should remain

    def test_empty_database_operations(self, test_database):
        """Test operations on empty database"""
        # Test operations on empty database don't crash
        assert test_database.job_exists("12345") is False
        assert test_database.get_job("12345") is None

        stats = test_database.get_statistics()
        assert stats["total_jobs"] == 0
        assert stats["by_status"] == {}

        discovered_jobs = test_database.get_jobs_by_status(JobStatus.DISCOVERED)
        assert len(discovered_jobs) == 0

        company_jobs = test_database.get_jobs_by_company("Test Company")
        assert len(company_jobs) == 0

        removed_count = test_database.cleanup_old_jobs()
        assert removed_count == 0

    def test_database_persistence(self, temp_dir):
        """Test that database persists data across instances"""
        csv_path = temp_dir / "persistence_test.csv"
        console = Console()

        # Create first database instance and add job
        db1 = ApplicationDatabase(csv_path=csv_path, console=console)
        success = db1.add_job(job_id="12345", company_name="Persistent Company", job_title="Persistent Job")
        assert success is True

        # Create second database instance pointing to same file
        db2 = ApplicationDatabase(csv_path=csv_path, console=console)

        # Should be able to retrieve job added by first instance
        assert db2.job_exists("12345") is True
        job = db2.get_job("12345")
        assert job["company_name"] == "Persistent Company"

    def test_invalid_csv_path(self, temp_dir):
        """Test handling of invalid CSV path"""
        # Try to create database in non-existent directory
        invalid_path = temp_dir / "nonexistent" / "subdir" / "test.csv"
        console = Console()

        # Should create directory structure automatically
        ApplicationDatabase(csv_path=invalid_path, console=console)
        assert invalid_path.exists()
        assert invalid_path.parent.exists()

    def test_job_status_enum_values(self):
        """Test that JobStatus enum has expected values"""
        assert JobStatus.DISCOVERED.value == "discovered"
        assert JobStatus.INTERESTED.value == "interested"
        assert JobStatus.APPLIED.value == "applied"
        assert JobStatus.INTERVIEWED.value == "interviewed"
        assert JobStatus.REJECTED.value == "rejected"
        assert JobStatus.CLOSED.value == "closed"

    def test_priority_enum_values(self):
        """Test that Priority enum has expected values"""
        assert Priority.HIGH.value == "high"
        assert Priority.MEDIUM.value == "medium"
        assert Priority.LOW.value == "low"
