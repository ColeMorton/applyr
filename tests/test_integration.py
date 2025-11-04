"""Integration tests for end-to-end workflows"""

from pathlib import Path

import responses
from rich.console import Console

from applyr.aggregator import JobDescriptionAggregator
from applyr.ats_analyzer import ATSAnalyzer
from applyr.pdf_converter import PDFConverter
from applyr.scraper import scrape_jobs


class TestFullJobScrapingWorkflow:
    """Integration tests for full job scraping workflow"""

    def test_scrape_save_generate_workflow(
        self, test_console: Console, temp_dir: Path, mock_responses, sample_seek_html: str
    ):
        """Test complete workflow: scrape job → save to database → generate markdown → verify files"""
        job_id = "12345678"
        url = f"https://www.seek.com.au/job/{job_id}"
        output_dir = temp_dir / "job_descriptions"

        mock_responses.add(responses.GET, url, body=sample_seek_html, status=200)

        # Scrape job
        results = scrape_jobs([url], output_dir, delay=0.1, console=test_console)

        assert results[url] is True
        assert output_dir.exists()

        # Verify markdown file was created
        job_files = list(output_dir.glob("*.md"))
        assert len(job_files) > 0
        assert any(job_id in f.name for f in job_files)

        # Verify file content
        job_file = job_files[0]
        content = job_file.read_text()
        assert "Software Engineer" in content or "Test Company" in content


class TestATSAnalysisWorkflow:
    """Integration tests for ATS analysis workflow"""

    def test_load_resume_analyze_workflow(
        self, test_console: Console, sample_text_resume: Path, sample_job_description: Path
    ):
        """Test workflow: load resume → analyze with job description → verify scores → check recommendations"""
        analyzer = ATSAnalyzer(test_console)

        # Analyze resume with job description
        result = analyzer.analyze_document(sample_text_resume, sample_job_description)

        # Verify analysis completed
        assert result.overall_score >= 0
        assert result.grade in ["A", "B", "C", "D", "F"]
        assert isinstance(result.critical_issues, list)
        assert isinstance(result.recommendations, list)
        assert isinstance(result.keyword_analysis, dict)

        # Verify scores are calculated
        assert result.contact_info_score >= 0
        assert result.keywords_score >= 0
        assert result.format_score >= 0

        # Verify job match was performed
        if "job_match" in result.keyword_analysis:
            assert "match_percentage" in result.keyword_analysis["job_match"]


class TestBatchProcessingWorkflow:
    """Integration tests for batch processing workflow"""

    def test_batch_process_aggregate_workflow(
        self, test_console: Console, temp_dir: Path, mock_responses, sample_seek_html: str
    ):
        """Test workflow: load URLs file → process all jobs → aggregate results → verify output"""
        urls_file = temp_dir / "urls.txt"
        urls = [
            "https://www.seek.com.au/job/12345678",
            "https://www.seek.com.au/job/12345679",
        ]
        urls_file.write_text("\n".join(urls))

        output_dir = temp_dir / "job_descriptions"

        for url in urls:
            mock_responses.add(responses.GET, url, body=sample_seek_html, status=200)

        # Process jobs
        from applyr.batch import batch_process_jobs

        success = batch_process_jobs(urls_file, output_dir, delay=0.1, console=test_console)

        assert success is True
        assert output_dir.exists()

        # Verify multiple files were created
        job_files = list(output_dir.glob("*.md"))
        assert len(job_files) >= 2

        # Aggregate results
        aggregator = JobDescriptionAggregator()
        aggregate_file = temp_dir / "aggregated.md"
        success, stats = aggregator.aggregate_jobs(output_dir, aggregate_file, test_console)

        assert success is True
        assert aggregate_file.exists()
        assert stats["total_jobs"] >= 2

        # Verify aggregate content
        content = aggregate_file.read_text()
        assert "Job Descriptions Aggregate" in content
        assert "Table of Contents" in content


class TestPDFGenerationWorkflow:
    """Integration tests for PDF generation workflow"""

    def test_generate_markdown_convert_pdf_workflow(self, test_console: Console, temp_dir: Path, mock_pdf_libraries):  # noqa: ARG002
        """Test workflow: generate markdown → convert to PDF → validate PDF → check formatting"""
        # Create markdown file
        md_file = temp_dir / "test.md"
        md_content = """# Test Document

This is a test document for PDF conversion.

## Section 1

Content for section 1.

## Section 2

Content for section 2.
"""
        md_file.write_text(md_content)

        # Convert to PDF
        pdf_converter = PDFConverter(test_console)
        pdf_file = temp_dir / "output.pdf"

        result = pdf_converter.convert_markdown_to_pdf(md_file, pdf_file)

        assert result is True
        assert pdf_file.exists()

        # Validate PDF structure
        assert pdf_file.stat().st_size > 100
        with open(pdf_file, "rb") as f:
            header = f.read(4)
            assert header.startswith(b"%PDF")


class TestMultiModuleIntegration:
    """Integration tests for multi-module workflows"""

    def test_scrape_analyze_generate_convert_workflow(
        self,
        test_console: Console,
        temp_dir: Path,
        mock_responses,
        sample_seek_html: str,
        sample_text_resume: Path,
        mock_pdf_libraries,  # noqa: ARG002
    ):
        """Test full pipeline: Scrape → Analyze → Generate → Convert"""
        # Step 1: Scrape job
        job_id = "12345678"
        url = f"https://www.seek.com.au/job/{job_id}"
        output_dir = temp_dir / "job_descriptions"

        mock_responses.add(responses.GET, url, body=sample_seek_html, status=200)

        results = scrape_jobs([url], output_dir, delay=0.1, console=test_console)
        assert results[url] is True

        # Step 2: Analyze resume with scraped job
        analyzer = ATSAnalyzer(test_console)
        job_file = list(output_dir.glob("*.md"))[0]

        analysis_result = analyzer.analyze_document(sample_text_resume, job_file)

        assert analysis_result.overall_score >= 0
        assert analysis_result.grade in ["A", "B", "C", "D", "F"]

        # Step 3: Convert aggregate to PDF
        aggregator = JobDescriptionAggregator()
        aggregate_file = temp_dir / "aggregated.md"
        success, stats = aggregator.aggregate_jobs(output_dir, aggregate_file, test_console)

        assert success is True
        assert aggregate_file.exists()

        # Step 4: Convert aggregate to PDF
        pdf_converter = PDFConverter(test_console)
        pdf_file = temp_dir / "aggregated.pdf"

        result = pdf_converter.convert_markdown_to_pdf(aggregate_file, pdf_file)

        assert result is True
        assert pdf_file.exists()

    def test_ats_analysis_with_multiple_formats(
        self, test_console: Console, sample_html_resume: Path, sample_text_resume: Path, sample_job_description: Path
    ):
        """Test ATS analysis with multiple resume formats"""
        analyzer = ATSAnalyzer(test_console)

        # Analyze HTML resume
        html_result = analyzer.analyze_document(sample_html_resume, sample_job_description)
        assert html_result.overall_score >= 0
        assert html_result.file_analysis["file_type"] in [".html", ".htm"]

        # Analyze text resume
        text_result = analyzer.analyze_document(sample_text_resume, sample_job_description)
        assert text_result.overall_score >= 0
        assert text_result.file_analysis["file_type"] == ".txt" or text_result.parsed_content["file_type"] == "text"

        # Both should produce valid scores
        assert isinstance(html_result.overall_score, (int, float))
        assert isinstance(text_result.overall_score, (int, float))
