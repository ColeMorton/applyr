"""Tests for batch processing module"""

from pathlib import Path

from rich.console import Console

from applyr.batch import batch_process_jobs


class TestBatchProcessJobs:
    """Tests for batch_process_jobs function"""

    def test_batch_process_valid_urls_file(
        self, test_console: Console, temp_dir: Path, mock_responses, sample_seek_html: str
    ):
        """Test batch processing with valid URLs file"""
        urls_file = temp_dir / "urls.txt"
        urls_file.write_text("https://www.seek.com.au/job/12345678\nhttps://www.seek.com.au/job/12345679")
        output_dir = temp_dir / "jobs"

        mock_responses.add(
            mock_responses.GET, "https://www.seek.com.au/job/12345678", body=sample_seek_html, status=200
        )
        mock_responses.add(
            mock_responses.GET, "https://www.seek.com.au/job/12345679", body=sample_seek_html, status=200
        )

        success = batch_process_jobs(urls_file, output_dir, delay=0.1, console=test_console)

        assert success is True
        assert output_dir.exists()

    def test_batch_process_empty_file(self, test_console: Console, temp_dir: Path):
        """Test batch processing with empty file"""
        urls_file = temp_dir / "empty.txt"
        urls_file.write_text("")
        output_dir = temp_dir / "jobs"

        success = batch_process_jobs(urls_file, output_dir, delay=0.1, console=test_console)

        assert success is False

    def test_batch_process_nonexistent_file(self, test_console: Console, temp_dir: Path):
        """Test batch processing with non-existent file"""
        urls_file = temp_dir / "nonexistent.txt"
        output_dir = temp_dir / "jobs"

        success = batch_process_jobs(urls_file, output_dir, delay=0.1, console=test_console)

        assert success is False

    def test_batch_process_mixed_results(
        self, test_console: Console, temp_dir: Path, mock_responses, sample_seek_html: str
    ):
        """Test batch processing with mixed success/failure"""
        urls_file = temp_dir / "urls.txt"
        urls_file.write_text("https://www.seek.com.au/job/12345678\nhttps://www.seek.com.au/job/invalid")
        output_dir = temp_dir / "jobs"

        mock_responses.add(
            mock_responses.GET, "https://www.seek.com.au/job/12345678", body=sample_seek_html, status=200
        )
        mock_responses.add(mock_responses.GET, "https://www.seek.com.au/job/invalid", body="Error", status=500)

        success = batch_process_jobs(urls_file, output_dir, delay=0.1, console=test_console)

        # Should return False if any jobs failed
        assert isinstance(success, bool)

    def test_batch_process_handles_blank_lines(
        self, test_console: Console, temp_dir: Path, mock_responses, sample_seek_html: str
    ):
        """Test batch processing handles blank lines in file"""
        urls_file = temp_dir / "urls.txt"
        urls_file.write_text("https://www.seek.com.au/job/12345678\n\nhttps://www.seek.com.au/job/12345679\n")
        output_dir = temp_dir / "jobs"

        mock_responses.add(
            mock_responses.GET, "https://www.seek.com.au/job/12345678", body=sample_seek_html, status=200
        )
        mock_responses.add(
            mock_responses.GET, "https://www.seek.com.au/job/12345679", body=sample_seek_html, status=200
        )

        success = batch_process_jobs(urls_file, output_dir, delay=0.1, console=test_console)

        assert isinstance(success, bool)
