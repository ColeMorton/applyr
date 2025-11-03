"""Tests for the PDF converter module"""

from pathlib import Path
import shutil
import tempfile

import pytest
from rich.console import Console

from applyr.pdf_converter import PDFConverter


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files"""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_markdown_file(temp_dir):
    """Create a sample markdown file for testing"""
    md_file = temp_dir / "test.md"
    md_content = """# Test Document

This is a **test** markdown document.

## Features

- Bullet point 1
- Bullet point 2
- Bullet point 3

### Code Example

```python
def hello_world():
    print("Hello, World!")
```

| Column 1 | Column 2 |
|----------|----------|
| Data 1   | Data 2   |
| Data 3   | Data 4   |

> This is a blockquote

[Link to somewhere](https://example.com)
"""
    md_file.write_text(md_content)
    return md_file


@pytest.fixture
def sample_css_file(temp_dir):
    """Create a sample CSS file for testing"""
    css_file = temp_dir / "custom.css"
    css_content = """
    body {
        background-color: #f0f0f0;
        font-family: Georgia, serif;
    }

    h1 {
        color: #2c3e50;
        text-align: center;
    }

    code {
        background-color: #e8e8e8;
        color: #d14;
    }
    """
    css_file.write_text(css_content)
    return css_file


@pytest.fixture
def pdf_converter():
    """Create a PDFConverter instance"""
    console = Console()
    return PDFConverter(console)


class TestPDFConverter:
    """Test cases for PDFConverter class"""

    def test_convert_markdown_to_pdf_basic(self, pdf_converter, sample_markdown_file, temp_dir):
        """Test basic markdown to PDF conversion"""
        output_pdf = temp_dir / "output.pdf"

        result = pdf_converter.convert_markdown_to_pdf(sample_markdown_file, output_pdf)

        assert result is True
        assert output_pdf.exists()
        assert output_pdf.stat().st_size > 0

    def test_convert_markdown_to_pdf_with_css_file(
        self, pdf_converter, sample_markdown_file, sample_css_file, temp_dir
    ):
        """Test markdown to PDF conversion with custom CSS file"""
        output_pdf = temp_dir / "output_with_css.pdf"

        result = pdf_converter.convert_markdown_to_pdf(sample_markdown_file, output_pdf, css_file=sample_css_file)

        assert result is True
        assert output_pdf.exists()
        assert output_pdf.stat().st_size > 0

    def test_convert_markdown_to_pdf_with_css_string(self, pdf_converter, sample_markdown_file, temp_dir):
        """Test markdown to PDF conversion with inline CSS string"""
        output_pdf = temp_dir / "output_with_inline_css.pdf"
        css_string = "body { color: blue; } h1 { font-size: 24px; }"

        result = pdf_converter.convert_markdown_to_pdf(sample_markdown_file, output_pdf, css_string=css_string)

        assert result is True
        assert output_pdf.exists()
        assert output_pdf.stat().st_size > 0

    def test_convert_nonexistent_file(self, pdf_converter, temp_dir):
        """Test conversion with non-existent markdown file"""
        nonexistent_file = temp_dir / "nonexistent.md"
        output_pdf = temp_dir / "output.pdf"

        result = pdf_converter.convert_markdown_to_pdf(nonexistent_file, output_pdf)

        assert result is False
        assert not output_pdf.exists()

    def test_batch_convert(self, pdf_converter, temp_dir):
        """Test batch conversion of multiple markdown files"""
        # Create multiple markdown files
        md_files = []
        for i in range(3):
            md_file = temp_dir / f"test_{i}.md"
            md_file.write_text(f"# Document {i}\n\nThis is document number {i}.")
            md_files.append(md_file)

        output_dir = temp_dir / "pdfs"

        results = pdf_converter.batch_convert(temp_dir, output_dir)

        assert len(results) == 3
        assert all(results.values())

        # Check that all PDFs were created
        for i in range(3):
            pdf_file = output_dir / f"test_{i}.pdf"
            assert pdf_file.exists()
            assert pdf_file.stat().st_size > 0

    def test_batch_convert_empty_directory(self, pdf_converter, temp_dir):
        """Test batch conversion with empty directory"""
        empty_dir = temp_dir / "empty"
        empty_dir.mkdir()
        output_dir = temp_dir / "pdfs"

        results = pdf_converter.batch_convert(empty_dir, output_dir)

        assert len(results) == 0

    def test_batch_convert_nonexistent_directory(self, pdf_converter, temp_dir):
        """Test batch conversion with non-existent directory"""
        nonexistent_dir = temp_dir / "nonexistent"
        output_dir = temp_dir / "pdfs"

        results = pdf_converter.batch_convert(nonexistent_dir, output_dir)

        assert len(results) == 0

    def test_batch_convert_with_custom_css(self, pdf_converter, temp_dir, sample_css_file):
        """Test batch conversion with custom CSS"""
        # Create a markdown file
        md_file = temp_dir / "test.md"
        md_file.write_text("# Test\n\nContent with custom CSS")

        output_dir = temp_dir / "pdfs"

        results = pdf_converter.batch_convert(temp_dir, output_dir, css_file=sample_css_file)

        assert len(results) == 1
        assert all(results.values())

        pdf_file = output_dir / "test.pdf"
        assert pdf_file.exists()

    def test_output_directory_creation(self, pdf_converter, sample_markdown_file, temp_dir):
        """Test that output directory is created if it doesn't exist"""
        nested_output = temp_dir / "nested" / "output" / "output.pdf"

        result = pdf_converter.convert_markdown_to_pdf(sample_markdown_file, nested_output)

        assert result is True
        assert nested_output.exists()
        assert nested_output.parent.exists()
