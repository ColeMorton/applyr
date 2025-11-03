# Testing Documentation

**Last Updated**: 2025-01-15  
**Status**: ✅ **Comprehensive Test Suite Complete** | 🎯 **Target: 50%+ Coverage**

## Overview

applyr has a comprehensive test suite covering all core modules, including ATS analysis, web scraping, PDF conversion, and integration workflows. The test suite uses pytest with coverage reporting and follows best practices for maintainable, reliable tests.

### Test Coverage Goals

- **Current Target**: 50%+ overall coverage
- **Focus Areas**: ATS modules (highest priority), scraper modules, utilities
- **Coverage Reporting**: HTML, terminal, and XML formats for CI integration

## Test Suite Structure

### Test Organization

```
tests/
├── conftest.py                    # Shared fixtures and test utilities
├── test_utils.py                  # Helper functions for test data
│
├── ATS Module Tests
│   ├── test_ats_analyzer.py       # ATSAnalyzer comprehensive tests
│   ├── test_ats_scoring.py        # ScoringEngine score calculation tests
│   ├── test_ats_parsers.py        # DocumentParser format tests (HTML, PDF, DOCX, TXT, MD)
│   ├── test_ats_keywords.py       # KeywordAnalyzer extraction tests
│   └── test_ats_output.py         # ATSOutputFormatter Rich console tests
│
├── Scraper Module Tests
│   ├── test_scraper.py            # SEEKScraper scraping and parsing tests
│   ├── test_scraper_base.py       # JobScraper base class functionality
│   ├── test_scraper_factory.py    # Scraper factory and detection tests
│   ├── test_scraper_linkedin_manual.py  # LinkedInManualParser tests
│   ├── test_employment_hero_scraper.py  # EmploymentHeroScraper tests
│   └── test_indeed_manual_parser.py     # IndeedManualParser tests
│
├── Core Module Tests
│   ├── test_database.py           # ApplicationDatabase operation tests
│   ├── test_cli.py                # CLI command tests with exact validation
│   ├── test_pdf_converter.py      # PDFConverter comprehensive tests
│   ├── test_aggregator.py         # JobDescriptionAggregator tests
│   ├── test_batch.py              # Batch processing tests
│   └── test_config.py             # PersonalConfig singleton pattern tests
│
└── Integration Tests
    └── test_integration.py         # End-to-end workflow tests
```

## Running Tests

### Local Development

**Run all tests:**
```bash
pytest
```

**Run with coverage report:**
```bash
pytest --cov=applyr --cov-report=html --cov-report=term-missing
```

**Run specific test file:**
```bash
pytest tests/test_ats_analyzer.py -v
```

**Run specific test class:**
```bash
pytest tests/test_ats_analyzer.py::TestATSAnalyzer -v
```

**Run specific test method:**
```bash
pytest tests/test_ats_analyzer.py::TestATSAnalyzer::test_analyze_resume_basic -v
```

**Run tests matching pattern:**
```bash
pytest -k "test_analyze" -v
```

**Run with verbose output:**
```bash
pytest -v
```

**Run with extra verbose output (show print statements):**
```bash
pytest -vv -s
```

### Continuous Integration

Tests run automatically on every push via GitHub Actions (`.github/workflows/tests.yml`):

- **Trigger**: All branches, on every push
- **Python Version**: 3.9
- **Quality Checks**: Linting (Ruff), type checking (mypy), security (Bandit), tests (pytest)
- **Coverage Reports**: HTML and XML artifacts uploaded for 30 days
- **Status Badge**: See README.md for workflow status

### Make Commands

```bash
make test          # Run tests with coverage
make all            # Run all quality checks (lint, type-check, security, test)
```

## Test Fixtures

### Core Fixtures (conftest.py)

**`runner`**: Typer CLI test runner
```python
def test_cli_command(runner):
    result = runner.invoke(app, ["command", "arg"])
    assert result.exit_code == 0
```

**`temp_dir`**: Temporary directory for test files (auto-cleanup)
```python
def test_file_operations(temp_dir):
    test_file = temp_dir / "test.txt"
    test_file.write_text("content")
    assert test_file.exists()
```

**`test_console`**: Rich console for testing
```python
def test_console_output(test_console):
    test_console.print("Test message")
```

**`test_database`**: ApplicationDatabase instance with temporary CSV
```python
def test_database_operations(test_database):
    test_database.add_job("12345678", "Company", "Title", "SEEK")
    assert test_database.get_job("12345678") is not None
```

**`mock_responses`**: HTTP request mocking with responses library
```python
def test_scraper(mock_responses, sample_seek_html):
    mock_responses.add(responses.GET, url, body=sample_seek_html, status=200)
    # Test scraping logic
```

### ATS Test Fixtures

**`sample_html_resume`**: HTML resume content
**`sample_text_resume`**: Plain text resume content
**`sample_resume_with_emojis`**: Resume with special characters
**`sample_resume_missing_sections`**: Incomplete resume for edge case testing
**`sample_resume_complex_html`**: Complex HTML structure
**`sample_job_description`**: Sample job description for matching tests

See `tests/conftest.py` for complete fixture definitions.

## Test Categories

### ATS Module Tests

**Priority**: Highest (core functionality)

**Coverage:**
- `test_ats_analyzer.py`: ATSAnalyzer class with full workflow tests
- `test_ats_scoring.py`: Score calculation for all categories (content, keywords, format, structure)
- `test_ats_parsers.py`: Document parsing for HTML, PDF, DOCX, TXT, MD formats
- `test_ats_keywords.py`: Keyword extraction and analysis
- `test_ats_output.py`: Rich console output formatting

**Key Test Patterns:**
- Resume analysis with various formats
- Score calculation accuracy
- Keyword matching and extraction
- Output formatting and console display
- Edge cases (missing sections, special characters, malformed documents)

### Scraper Module Tests

**Coverage:**
- `test_scraper.py`: SEEKScraper HTTP requests, HTML parsing, error handling
- `test_scraper_base.py`: JobScraper base class functionality
- `test_scraper_factory.py`: Factory pattern and source detection
- `test_scraper_linkedin_manual.py`: LinkedInManualParser text parsing
- `test_employment_hero_scraper.py`: EmploymentHeroScraper specific tests
- `test_indeed_manual_parser.py`: IndeedManualParser text file processing

**Key Test Patterns:**
- HTTP request mocking with `responses` library
- HTML parsing with BeautifulSoup
- Error handling (403, 404, network errors)
- Manual import text file processing
- Factory pattern and scraper detection

### Core Module Tests

**Coverage:**
- `test_database.py`: CSV operations, job tracking, status updates
- `test_cli.py`: CLI commands with exact output validation
- `test_pdf_converter.py`: PDF generation, templates, quality validation
- `test_aggregator.py`: Job aggregation and market intelligence
- `test_batch.py`: Batch processing workflows
- `test_config.py`: Configuration loading and singleton pattern

**Key Test Patterns:**
- File operations with temporary directories
- CLI command execution and output validation
- PDF generation and content validation
- Data aggregation and statistics
- Configuration management

### Integration Tests

**Coverage:**
- `test_integration.py`: End-to-end workflows

**Test Scenarios:**
- Full job scraping workflow (scrape → save → generate)
- ATS analysis workflow (load resume → analyze → generate report)
- PDF generation workflow (markdown → HTML → PDF)
- Batch processing workflow (multiple jobs → aggregate → report)

## Test Utilities

### Helper Functions (test_utils.py)

**`create_sample_resume()`**: Generate sample resume content
**`create_sample_job_description()`**: Generate sample job description
**`assert_pdf_valid()`**: Validate PDF file structure
**`assert_markdown_valid()`**: Validate markdown file structure

See `tests/test_utils.py` for complete utility functions.

## Best Practices

### Test Organization

1. **One test file per module**: `test_<module_name>.py`
2. **Test classes group related tests**: `TestClassName`
3. **Descriptive test names**: `test_<feature>_<scenario>_<expected_result>`
4. **Use fixtures for common setup**: Reuse `temp_dir`, `test_console`, etc.

### Assertions

1. **Exact validation**: Check specific output, not just exit codes
2. **File existence**: Verify files are created in expected locations
3. **Content validation**: Check file contents, not just presence
4. **Error handling**: Test both success and failure scenarios

### Mocking

1. **HTTP requests**: Use `mock_responses` fixture for all network calls
2. **File system**: Use `temp_dir` fixture for file operations
3. **Console output**: Use `test_console` fixture for Rich output
4. **External dependencies**: Mock external services and libraries

### Coverage

1. **Aim for 50%+ overall coverage**
2. **Focus on critical paths**: ATS analysis, scraping, PDF generation
3. **Test edge cases**: Missing data, malformed input, errors
4. **Integration tests**: Verify end-to-end workflows

### Maintainability

1. **DRY principle**: Use fixtures and utilities for common patterns
2. **Clear test names**: Describe what is being tested
3. **Isolated tests**: Each test should be independent
4. **Fast execution**: Tests should run quickly for rapid feedback

## Coverage Reporting

### Local Reports

**HTML Report:**
```bash
pytest --cov=applyr --cov-report=html
# Open htmlcov/index.html in browser
```

**Terminal Report:**
```bash
pytest --cov=applyr --cov-report=term-missing
```

**XML Report:**
```bash
pytest --cov=applyr --cov-report=xml
# coverage.xml for CI integration
```

### Coverage Configuration

Coverage is configured in `pyproject.toml`:

```toml
[tool.coverage.run]
source = ["applyr"]
omit = ["tests/*", "*/__pycache__/*", "applyr/__init__.py"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
    "pass"
]
```

### CI Coverage Reports

GitHub Actions generates and uploads coverage reports:

- **HTML Report**: `htmlcov/` directory (artifact)
- **XML Report**: `coverage.xml` (artifact)
- **Terminal Report**: Printed in workflow logs

Download artifacts from GitHub Actions workflow runs to view detailed coverage reports.

## Troubleshooting

### Common Issues

**Import Errors:**
- Ensure `poetry install` has been run
- Activate virtual environment: `poetry shell`
- Check PYTHONPATH if running tests outside poetry

**Fixture Not Found:**
- Verify fixture is defined in `conftest.py`
- Check fixture name matches exactly
- Ensure pytest can find conftest.py

**Coverage Not Working:**
- Install pytest-cov: `poetry add --group dev pytest-cov`
- Check coverage configuration in `pyproject.toml`
- Verify source paths are correct

**Tests Failing in CI:**
- Check Python version matches (3.9)
- Verify dependencies are installed
- Review workflow logs for specific errors

### Debugging Tips

**Run single test with debugging:**
```bash
pytest tests/test_ats_analyzer.py::TestATSAnalyzer::test_analyze_resume_basic -vv -s
```

**Print statements:**
```bash
pytest -s  # Show print output
```

**Pytest debugging:**
```bash
pytest --pdb  # Drop into debugger on failure
```

## Related Documentation

- **[CI_CD.md](./CI_CD.md)**: Continuous Integration workflow documentation
- **[LINTING_FORMATTING_STATUS.md](./LINTING_FORMATTING_STATUS.md)**: Code quality standards
- **[README.md](../README.md)**: Project overview and quick start

---

**Last Updated**: 2025-01-15
