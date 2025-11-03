"""Tests for job aggregator module"""

from pathlib import Path

import pytest
from rich.console import Console

from applyr.aggregator import JobDescriptionAggregator, aggregate_job_data


class TestJobDescriptionAggregator:
    """Tests for JobDescriptionAggregator class"""

    def test_discover_job_files(self, temp_dir: Path):
        """Test discovery of job files"""
        aggregator = JobDescriptionAggregator()
        job_dir = temp_dir / "jobs"
        job_dir.mkdir()

        # Create job files with numeric prefix
        (job_dir / "12345678_company_title.md").write_text("# Job Title")
        (job_dir / "12345679_company2_title2.md").write_text("# Job Title 2")
        (job_dir / "invalid_file.md").write_text("# Invalid")

        files = aggregator.discover_job_files(job_dir)

        assert len(files) == 2
        assert all(f.name.startswith("1234567") for f in files)

    def test_discover_job_files_empty_directory(self, temp_dir: Path):
        """Test discovery with empty directory"""
        aggregator = JobDescriptionAggregator()
        empty_dir = temp_dir / "empty"
        empty_dir.mkdir()

        files = aggregator.discover_job_files(empty_dir)

        assert len(files) == 0

    def test_discover_job_files_nonexistent_directory(self, temp_dir: Path):
        """Test discovery with non-existent directory raises ValueError"""
        aggregator = JobDescriptionAggregator()
        nonexistent = temp_dir / "nonexistent"

        with pytest.raises(ValueError, match="does not exist"):
            aggregator.discover_job_files(nonexistent)

    def test_parse_job_file(self, temp_dir: Path):
        """Test parsing of job file"""
        aggregator = JobDescriptionAggregator()
        job_file = temp_dir / "12345678_test.md"
        job_content = """# Software Engineer

**Company:** Tech Company
**Job ID:** 12345678
**Source:** SEEK
**Scraped:** 2025-01-15 10:30:00

---

Job description content here.
"""
        job_file.write_text(job_content)

        job_data = aggregator.parse_job_file(job_file)

        assert job_data is not None
        assert job_data["job_id"] == "12345678"
        assert job_data["title"] == "Software Engineer"
        assert job_data["company"] == "Tech Company"
        assert job_data["source"] == "SEEK"
        assert job_data["scraped_date"] == "2025-01-15 10:30:00"
        assert "Job description content" in job_data["description"]

    def test_parse_job_file_without_metadata(self, temp_dir: Path):
        """Test parsing file with minimal content"""
        aggregator = JobDescriptionAggregator()
        job_file = temp_dir / "12345678_minimal.md"
        job_file.write_text("Minimal content")

        job_data = aggregator.parse_job_file(job_file)

        assert job_data is not None
        assert job_data["job_id"] == "12345678"
        assert job_data["title"] == "Unknown Job"
        assert job_data["company"] == "Unknown Company"

    def test_parse_job_file_invalid_file(self, temp_dir: Path):
        """Test parsing invalid file returns None"""
        aggregator = JobDescriptionAggregator()
        # Create a file that might cause parsing issues
        invalid_file = temp_dir / "invalid.txt"
        # Don't create it - test non-existent file
        # Or test with binary content
        job_data = aggregator.parse_job_file(invalid_file)

        assert job_data is None

    def test_generate_unique_title(self):
        """Test generation of unique title"""
        aggregator = JobDescriptionAggregator()
        job_data = {
            "title": "Software Engineer",
            "company": "Tech Company",
            "job_id": "12345678",
        }

        title = aggregator.generate_unique_title(job_data)

        assert "Software Engineer" in title
        assert "Tech Company" in title
        assert "12345678" in title

    def test_generate_anchor_link(self):
        """Test generation of anchor link"""
        aggregator = JobDescriptionAggregator()
        title = "Software Engineer at Tech Company (ID: 12345678)"

        anchor = aggregator.generate_anchor_link(title)

        assert "software-engineer" in anchor
        assert "tech-company" in anchor
        assert "12345678" in anchor
        assert " " not in anchor
        assert "(" not in anchor
        assert ")" not in anchor

    def test_generate_summary_stats(self):
        """Test generation of summary statistics"""
        aggregator = JobDescriptionAggregator()
        jobs_data = [
            {
                "title": "Senior Software Engineer",
                "company": "Tech Company A",
                "description": "Python, JavaScript, React, AWS",
            },
            {
                "title": "Junior Developer",
                "company": "Tech Company A",
                "description": "Python, TypeScript",
            },
            {
                "title": "Lead Engineer",
                "company": "Tech Company B",
                "description": "JavaScript, Node.js",
            },
        ]

        stats = aggregator.generate_summary_stats(jobs_data)

        assert stats["total_jobs"] == 3
        assert stats["unique_companies"] == 2
        assert "Tech Company A" in stats["company_counts"]
        assert stats["company_counts"]["Tech Company A"] == 2
        assert "Senior" in stats["job_level_distribution"]
        assert len(stats["technology_mentions"]) > 0

    def test_generate_summary_stats_empty(self):
        """Test statistics generation with empty list"""
        aggregator = JobDescriptionAggregator()
        stats = aggregator.generate_summary_stats([])

        assert stats == {}

    def test_generate_aggregate_content(self, _temp_dir: Path):
        """Test generation of aggregate content"""
        aggregator = JobDescriptionAggregator()
        jobs_data = [
            {
                "title": "Software Engineer",
                "company": "Tech Company",
                "job_id": "12345678",
                "source": "SEEK",
                "scraped_date": "2025-01-15 10:30:00",
                "filename": "12345678_test.md",
                "description": "Job description content",
            }
        ]
        stats = {
            "total_jobs": 1,
            "unique_companies": 1,
            "company_counts": {"Tech Company": 1},
            "job_level_distribution": {"Mid-level": 1},
            "technology_mentions": {},
        }

        content = aggregator.generate_aggregate_content(jobs_data, stats)

        assert "Job Descriptions Aggregate" in content
        assert "Software Engineer" in content
        assert "Tech Company" in content
        assert "12345678" in content
        assert "Table of Contents" in content

    def test_aggregate_jobs_success(self, test_console: Console, temp_dir: Path):
        """Test successful job aggregation"""
        aggregator = JobDescriptionAggregator()
        job_dir = temp_dir / "jobs"
        job_dir.mkdir()
        output_file = temp_dir / "aggregated.md"

        # Create sample job files
        job1 = job_dir / "12345678_test1.md"
        job1.write_text("""# Software Engineer
**Company:** Tech Company A
**Job ID:** 12345678
**Source:** SEEK
**Scraped:** 2025-01-15 10:30:00

---
Job description 1.
""")

        job2 = job_dir / "12345679_test2.md"
        job2.write_text("""# Developer
**Company:** Tech Company B
**Job ID:** 12345679
**Source:** SEEK
**Scraped:** 2025-01-15 11:00:00

---
Job description 2.
""")

        success, stats = aggregator.aggregate_jobs(job_dir, output_file, test_console)

        assert success is True
        assert output_file.exists()
        assert stats["total_jobs"] == 2
        assert stats["unique_companies"] == 2

        # Verify content
        content = output_file.read_text()
        assert "Software Engineer" in content
        assert "Developer" in content

    def test_aggregate_jobs_empty_directory(self, test_console: Console, temp_dir: Path):
        """Test aggregation with empty directory"""
        aggregator = JobDescriptionAggregator()
        empty_dir = temp_dir / "empty"
        empty_dir.mkdir()
        output_file = temp_dir / "aggregated.md"

        success, stats = aggregator.aggregate_jobs(empty_dir, output_file, test_console)

        assert success is False
        assert stats == {}

    def test_aggregate_jobs_creates_output_directory(self, test_console: Console, temp_dir: Path):
        """Test that output directory is created if needed"""
        aggregator = JobDescriptionAggregator()
        job_dir = temp_dir / "jobs"
        job_dir.mkdir()
        job_file = job_dir / "12345678_test.md"
        job_file.write_text("# Job Title\n**Company:** Company\n---\nDescription")
        output_file = temp_dir / "nested" / "output" / "aggregated.md"

        success, stats = aggregator.aggregate_jobs(job_dir, output_file, test_console)

        assert success is True
        assert output_file.exists()
        assert output_file.parent.exists()


class TestAggregateJobDataFunction:
    """Tests for aggregate_job_data function"""

    def test_aggregate_with_default_output(self, test_console: Console, temp_dir: Path):
        """Test aggregation with default output file"""
        job_dir = temp_dir / "jobs"
        job_dir.mkdir()
        job_file = job_dir / "12345678_test.md"
        job_file.write_text("# Job\n**Company:** Company\n---\nDescription")

        success = aggregate_job_data(job_dir, None, None, False, test_console)

        assert success is True
        # Should create file with date prefix
        output_files = list(job_dir.glob("*_job_descriptions_aggregate.md"))
        assert len(output_files) > 0

    def test_aggregate_with_custom_output(self, test_console: Console, temp_dir: Path):
        """Test aggregation with custom output file"""
        job_dir = temp_dir / "jobs"
        job_dir.mkdir()
        job_file = job_dir / "12345678_test.md"
        job_file.write_text("# Job\n**Company:** Company\n---\nDescription")
        output_file = temp_dir / "custom_output.md"

        success = aggregate_job_data(job_dir, output_file, None, False, test_console)

        assert success is True
        assert output_file.exists()

    def test_aggregate_with_date(self, test_console: Console, temp_dir: Path):
        """Test aggregation with date parameter"""
        job_dir = temp_dir / "jobs"
        job_dir.mkdir()
        job_file = job_dir / "12345678_test.md"
        job_file.write_text("# Job\n**Company:** Company\n---\nDescription")

        success = aggregate_job_data(job_dir, None, "20250115", False, test_console)

        assert success is True
        output_file = job_dir / "20250115_job_descriptions_aggregate.md"
        assert output_file.exists()

    def test_aggregate_invalid_date_format(self, test_console: Console, temp_dir: Path):
        """Test aggregation with invalid date format"""
        job_dir = temp_dir / "jobs"
        job_dir.mkdir()

        success = aggregate_job_data(job_dir, None, "invalid-date", False, test_console)

        assert success is False

    def test_aggregate_nonexistent_directory(self, test_console: Console, temp_dir: Path):
        """Test aggregation with non-existent directory"""
        nonexistent = temp_dir / "nonexistent"

        success = aggregate_job_data(nonexistent, None, None, False, test_console)

        assert success is False
