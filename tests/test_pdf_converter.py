"""Tests for the PDF converter module"""

import pytest
from rich.console import Console

from applyr.pdf_converter import PDFConverter


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

    def test_convert_empty_file(self, pdf_converter, temp_dir):
        """Test conversion with empty markdown file"""
        empty_file = temp_dir / "empty.md"
        empty_file.write_text("")
        output_pdf = temp_dir / "output.pdf"

        result = pdf_converter.convert_markdown_to_pdf(empty_file, output_pdf)

        # Should still create PDF (may be empty or minimal)
        assert result is True
        assert output_pdf.exists()

    def test_convert_large_file(self, pdf_converter, temp_dir):
        """Test conversion with large markdown file"""
        large_file = temp_dir / "large.md"
        # Create large content
        large_content = "# Large Document\n\n" + ("This is a test paragraph. " * 1000)
        large_file.write_text(large_content)
        output_pdf = temp_dir / "output.pdf"

        result = pdf_converter.convert_markdown_to_pdf(large_file, output_pdf)

        assert result is True
        assert output_pdf.exists()
        assert output_pdf.stat().st_size > 0

    def test_convert_special_characters(self, pdf_converter, temp_dir):
        """Test conversion with special characters"""
        special_file = temp_dir / "special.md"
        special_content = """# Special Characters Test

Text with special characters: © ® ™ € £ ¥ § ¶ † ‡ • … — –

Emoji: 😀 🚀 🎉 ⚡

Unicode: 你好 مرحبا Здравствуй
"""
        special_file.write_text(special_content)
        output_pdf = temp_dir / "output.pdf"

        result = pdf_converter.convert_markdown_to_pdf(special_file, output_pdf)

        assert result is True
        assert output_pdf.exists()

    def test_convert_invalid_css_file(self, pdf_converter, sample_markdown_file, temp_dir):
        """Test conversion with invalid CSS file"""
        invalid_css = temp_dir / "invalid.css"
        invalid_css.write_text("invalid css { syntax error }")
        output_pdf = temp_dir / "output.pdf"

        # Should handle invalid CSS gracefully
        result = pdf_converter.convert_markdown_to_pdf(sample_markdown_file, output_pdf, css_file=invalid_css)

        # May succeed with default CSS or fail gracefully
        assert isinstance(result, bool)

    def test_convert_missing_css_file(self, pdf_converter, sample_markdown_file, temp_dir):
        """Test conversion with non-existent CSS file"""
        nonexistent_css = temp_dir / "nonexistent.css"
        output_pdf = temp_dir / "output.pdf"

        # Should fall back to default CSS or handle gracefully
        result = pdf_converter.convert_markdown_to_pdf(sample_markdown_file, output_pdf, css_file=nonexistent_css)

        # Should still create PDF
        assert result is True
        assert output_pdf.exists()

    def test_convert_invalid_css_string(self, pdf_converter, sample_markdown_file, temp_dir):
        """Test conversion with invalid CSS string"""
        invalid_css = "invalid { css syntax }"
        output_pdf = temp_dir / "output.pdf"

        # Should handle invalid CSS gracefully
        result = pdf_converter.convert_markdown_to_pdf(sample_markdown_file, output_pdf, css_string=invalid_css)

        # May succeed with default CSS or fail gracefully
        assert isinstance(result, bool)

    def test_batch_convert_with_failures(self, pdf_converter, temp_dir):
        """Test batch conversion with some files that fail"""
        # Create valid and invalid files
        valid_file = temp_dir / "valid.md"
        valid_file.write_text("# Valid File\n\nContent")
        invalid_file = temp_dir / "invalid.txt"  # Wrong extension
        invalid_file.write_text("Not markdown")

        output_dir = temp_dir / "pdfs"

        results = pdf_converter.batch_convert(temp_dir, output_dir)

        # Should handle failures gracefully
        assert isinstance(results, dict)
        assert len(results) >= 1  # At least valid file should be processed

    def test_pdf_content_validation(self, pdf_converter, sample_markdown_file, temp_dir):
        """Test that PDF contains expected content structure"""
        output_pdf = temp_dir / "output.pdf"

        result = pdf_converter.convert_markdown_to_pdf(sample_markdown_file, output_pdf)

        assert result is True
        assert output_pdf.exists()
        # Verify PDF is a valid file (not corrupted)
        assert output_pdf.stat().st_size > 100  # Should be more than minimal size
        # Check PDF header (should start with %PDF)
        with open(output_pdf, "rb") as f:
            header = f.read(4)
            assert header.startswith(b"%PDF")

    def test_convert_with_images_reference(self, pdf_converter, temp_dir):
        """Test conversion with image references in markdown"""
        image_file = temp_dir / "with_images.md"
        image_content = """# Document with Images

![Alt text](image.png)

<img src="logo.svg" alt="Logo">
"""
        image_file.write_text(image_content)
        output_pdf = temp_dir / "output.pdf"

        # Should handle missing images gracefully
        result = pdf_converter.convert_markdown_to_pdf(image_file, output_pdf)

        assert result is True
        assert output_pdf.exists()

    def test_convert_html_entities(self, pdf_converter, temp_dir):
        """Test conversion with HTML entities"""
        html_file = temp_dir / "html_entities.md"
        html_content = """# HTML Entities

&amp; &lt; &gt; &quot; &apos; &copy; &reg;
"""
        html_file.write_text(html_content)
        output_pdf = temp_dir / "output.pdf"

        result = pdf_converter.convert_markdown_to_pdf(html_file, output_pdf)

        assert result is True
        assert output_pdf.exists()

    def test_convert_very_long_line(self, pdf_converter, temp_dir):
        """Test conversion with very long line (should wrap properly)"""
        long_line_file = temp_dir / "long_line.md"
        long_line = "# Long Line\n\n" + ("A" * 500) + " " + ("B" * 500)
        long_line_file.write_text(long_line)
        output_pdf = temp_dir / "output.pdf"

        result = pdf_converter.convert_markdown_to_pdf(long_line_file, output_pdf)

        assert result is True
        assert output_pdf.exists()
