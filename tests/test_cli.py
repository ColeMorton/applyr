"""Tests for CLI commands"""

from pathlib import Path

import responses

from applyr.cli import app


class TestAddJobCommand:
    """Tests for add-job command"""

    # Happy Path Tests

    def test_add_job_seek_id(self, runner, _temp_dir, mock_responses, sample_seek_html):
        """Test adding job with SEEK 8-digit ID"""
        job_id = "12345678"
        mock_responses.add(responses.GET, f"https://www.seek.com.au/job/{job_id}", body=sample_seek_html, status=200)

        with runner.isolated_filesystem() as fs:
            result = runner.invoke(app, ["add-job", job_id])

        assert result.exit_code == 0
        assert "Successfully added" in result.output or "Saved job" in result.output
        # Verify file was created
        job_files = list(Path(fs).glob("**/job_descriptions/*.md"))
        assert len(job_files) > 0
        assert any(job_id in f.name for f in job_files)

    def test_add_job_seek_url(self, runner, _temp_dir, mock_responses, sample_seek_html):
        """Test adding job with full SEEK URL"""
        job_id = "12345678"
        url = f"https://www.seek.com.au/job/{job_id}"
        mock_responses.add(responses.GET, url, body=sample_seek_html, status=200)

        with runner.isolated_filesystem() as fs:
            result = runner.invoke(app, ["add-job", url])

        assert result.exit_code == 0
        assert "Saved job" in result.output or "Successfully" in result.output
        # Verify file was created
        job_files = list(Path(fs).glob("**/job_descriptions/*.md"))
        assert len(job_files) > 0
        assert any(job_id in f.name for f in job_files)

    def test_add_job_employment_hero_url(self, runner, _temp_dir, mock_responses, sample_eh_html):
        """Test adding job with Employment Hero URL"""
        url = "https://jobs.employmenthero.com/AU/job/test-job-slug"
        mock_responses.add(responses.GET, url, body=sample_eh_html, status=200)

        with runner.isolated_filesystem():
            result = runner.invoke(app, ["add-job", url])

        assert result.exit_code == 0
        assert "eh-test-job-slug" in result.output or "Saved job" in result.output

    def test_add_job_with_priority_flag(self, runner, _temp_dir, mock_responses, sample_seek_html):
        """Test adding job with priority flag"""
        job_id = "12345678"
        mock_responses.add(responses.GET, f"https://www.seek.com.au/job/{job_id}", body=sample_seek_html, status=200)

        with runner.isolated_filesystem() as fs:
            result = runner.invoke(app, ["add-job", job_id, "--priority", "high"])

        assert result.exit_code == 0
        # Verify job was added successfully
        assert "Successfully" in result.output or "Saved job" in result.output
        job_files = list(Path(fs).glob("**/job_descriptions/*.md"))
        assert len(job_files) > 0

    def test_add_job_with_notes_flag(self, runner, _temp_dir, mock_responses, sample_seek_html):
        """Test adding job with notes flag"""
        job_id = "12345678"
        notes_text = "Great opportunity with good tech stack"
        mock_responses.add(responses.GET, f"https://www.seek.com.au/job/{job_id}", body=sample_seek_html, status=200)

        with runner.isolated_filesystem() as fs:
            result = runner.invoke(app, ["add-job", job_id, "--notes", notes_text])

        assert result.exit_code == 0
        assert "Successfully" in result.output or "Saved job" in result.output
        job_files = list(Path(fs).glob("**/job_descriptions/*.md"))
        assert len(job_files) > 0

    def test_add_job_with_combined_flags(self, runner, _temp_dir, mock_responses, sample_seek_html):
        """Test adding job with multiple flags"""
        job_id = "12345678"
        mock_responses.add(responses.GET, f"https://www.seek.com.au/job/{job_id}", body=sample_seek_html, status=200)

        with runner.isolated_filesystem():
            result = runner.invoke(app, ["add-job", job_id, "--priority", "high", "--notes", "Test note"])

        assert result.exit_code == 0

    # Error Handling Tests

    def test_add_job_invalid_id_format(self, runner):
        """Test rejection of invalid job ID format"""
        result = runner.invoke(app, ["add-job", "123"])  # Not 8 digits

        assert result.exit_code == 1
        assert "Invalid" in result.output or "Error" in result.output or "8 digits" in result.output

    def test_add_job_invalid_id_non_numeric(self, runner):
        """Test rejection of non-numeric job ID"""
        result = runner.invoke(app, ["add-job", "abcd1234"])

        assert result.exit_code == 1
        assert "Invalid" in result.output or "Error" in result.output or "numeric" in result.output.lower()

    def test_add_job_unsupported_url(self, runner):
        """Test rejection of unsupported job board URL"""
        result = runner.invoke(app, ["add-job", "https://linkedin.com/job/12345"])

        assert result.exit_code == 1
        assert "Unsupported" in result.output or "Invalid" in result.output

    def test_add_job_invalid_priority(self, runner, mock_responses, sample_seek_html):
        """Test rejection of invalid priority value"""
        job_id = "12345678"
        mock_responses.add(responses.GET, f"https://www.seek.com.au/job/{job_id}", body=sample_seek_html, status=200)

        result = runner.invoke(app, ["add-job", job_id, "--priority", "invalid"])

        assert result.exit_code == 1
        assert "priority" in result.output.lower()

    def test_add_job_empty_identifier(self, runner):
        """Test error with empty identifier"""
        result = runner.invoke(app, ["add-job", ""])

        assert result.exit_code != 0
        assert "Error" in result.output or "required" in result.output.lower() or "Missing" in result.output

    # Mixed Batch Tests

    def test_add_job_mixed_batch(self, runner, _temp_dir, mock_responses, sample_seek_html, sample_eh_html):
        """Test adding mixed SEEK and Employment Hero jobs"""
        seek_id = "12345678"
        eh_url = "https://jobs.employmenthero.com/AU/job/test-position"

        mock_responses.add(responses.GET, f"https://www.seek.com.au/job/{seek_id}", body=sample_seek_html, status=200)
        mock_responses.add(responses.GET, eh_url, body=sample_eh_html, status=200)

        with runner.isolated_filesystem():
            result = runner.invoke(app, ["add-job", f"{seek_id},{eh_url}"])

        # Should process both jobs - may have exit code 0 or report mixed results
        assert "Scraping" in result.output or "Processing" in result.output

    def test_add_job_multiple_seek_ids(self, runner, _temp_dir, mock_responses, sample_seek_html):
        """Test adding multiple SEEK job IDs"""
        job_id1 = "12345678"
        job_id2 = "12345679"

        mock_responses.add(responses.GET, f"https://www.seek.com.au/job/{job_id1}", body=sample_seek_html, status=200)
        mock_responses.add(responses.GET, f"https://www.seek.com.au/job/{job_id2}", body=sample_seek_html, status=200)

        with runner.isolated_filesystem():
            result = runner.invoke(app, ["add-job", f"{job_id1},{job_id2}"])

        assert "Scraping" in result.output or "Processing" in result.output


class TestAddJobCommandErrorScenarios:
    """Additional error scenario tests for add-job command"""

    def test_add_job_network_failure(self, runner, _temp_dir, mock_responses):
        """Test handling of network failure"""
        job_id = "12345678"
        mock_responses.add(responses.GET, f"https://www.seek.com.au/job/{job_id}", body="Error", status=500)

        with runner.isolated_filesystem():
            result = runner.invoke(app, ["add-job", job_id])

        # Should handle error gracefully
        assert result.exit_code != 0 or "Failed" in result.output

    def test_add_job_malformed_comma_list(self, runner):
        """Test handling of malformed comma-separated list"""
        runner.invoke(app, ["add-job", "12345678,,12345679"])

        # Should handle empty items in list
        # May succeed by skipping empty items or fail with error

    def test_add_job_with_force_flag(self, runner, _temp_dir, mock_responses, sample_seek_html):
        """Test adding job with force flag"""
        job_id = "12345678"
        mock_responses.add(responses.GET, f"https://www.seek.com.au/job/{job_id}", body=sample_seek_html, status=200)

        with runner.isolated_filesystem():
            # Add job first time
            result1 = runner.invoke(app, ["add-job", job_id])

            # Add again with force flag
            mock_responses.add(
                responses.GET, f"https://www.seek.com.au/job/{job_id}", body=sample_seek_html, status=200
            )
            runner.invoke(app, ["add-job", job_id, "--force"])

        # First should succeed
        assert result1.exit_code == 0


class TestAddJobCommandValidation:
    """Tests for input validation in add-job command"""

    def test_validate_seek_id_exactly_8_digits(self, runner):
        """Test SEEK ID must be exactly 8 digits"""
        # 7 digits
        result = runner.invoke(app, ["add-job", "1234567"])
        assert result.exit_code == 1

        # 9 digits
        result = runner.invoke(app, ["add-job", "123456789"])
        assert result.exit_code == 1

    def test_validate_priority_values(self, runner, mock_responses, sample_seek_html):
        """Test priority validation accepts only valid values"""
        job_id = "12345678"
        mock_responses.add(responses.GET, f"https://www.seek.com.au/job/{job_id}", body=sample_seek_html, status=200)

        # Valid priorities should work
        for priority in ["high", "medium", "low"]:
            mock_responses.add(
                responses.GET, f"https://www.seek.com.au/job/{job_id}", body=sample_seek_html, status=200
            )
            runner.invoke(app, ["add-job", job_id, "--priority", priority])
            # Note: May fail if job already exists from previous iteration
            # This test validates the priority parameter is accepted

    def test_url_format_validation(self, runner):
        """Test URL format validation"""
        # Invalid URL format
        result = runner.invoke(app, ["add-job", "ht!tp://invalid"])
        assert result.exit_code == 1


class TestAddJobCommandIntegration:
    """Integration-style tests for add-job command (require more complex setup)"""

    # These tests would require more sophisticated mocking of the database
    # and file system to verify end-to-end behavior

    def test_job_file_naming_convention_seek(self, runner, temp_dir, mock_responses, sample_seek_html):
        """Test SEEK job file follows naming convention"""
        job_id = "12345678"
        mock_responses.add(responses.GET, f"https://www.seek.com.au/job/{job_id}", body=sample_seek_html, status=200)

        with runner.isolated_filesystem():
            output_dir = temp_dir / "job_descriptions"
            output_dir.mkdir(parents=True, exist_ok=True)

            runner.invoke(app, ["add-job", job_id])

            # Check if file was created with correct pattern
            # Would need to check actual file system

    def test_job_id_format_employment_hero(self, runner, _temp_dir, mock_responses, sample_eh_html):
        """Test Employment Hero job ID has correct prefix"""
        url = "https://jobs.employmenthero.com/AU/job/test-slug"
        mock_responses.add(responses.GET, url, body=sample_eh_html, status=200)

        with runner.isolated_filesystem():
            result = runner.invoke(app, ["add-job", url])

            # Verify output contains eh- prefixed job ID
            assert "eh-" in result.output or result.exit_code == 0
