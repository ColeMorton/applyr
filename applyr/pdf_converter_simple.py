"""Simple PDF converter using ReportLab only"""

import html
from pathlib import Path
import re
from typing import Optional

import markdown
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from rich.console import Console


class PDFConverter:
    """Convert markdown files to PDF using ReportLab"""

    def __init__(self, console: Optional[Console] = None):
        """Initialize PDF converter with optional console for output"""
        self.console = console or Console()
        self.md = markdown.Markdown(extensions=["extra", "codehilite", "toc", "tables"])

    def convert_markdown_to_pdf(
        self, markdown_file: Path, output_pdf: Path, _css_file: Optional[Path] = None, _css_string: Optional[str] = None
    ) -> bool:
        """
        Convert a markdown file to PDF

        Args:
            markdown_file: Path to the input markdown file
            output_pdf: Path for the output PDF file
            css_file: Optional (ignored for now)
            css_string: Optional (ignored for now)

        Returns:
            bool: True if conversion successful, False otherwise
        """
        try:
            # Read markdown content
            if not markdown_file.exists():
                self.console.print(f"[red]❌ Error: Markdown file not found: {markdown_file}[/red]")
                return False

            with open(markdown_file, encoding="utf-8") as f:
                markdown_content = f.read()

            # Convert markdown to HTML first
            html_content = self.md.convert(markdown_content)

            # Create PDF
            output_pdf.parent.mkdir(parents=True, exist_ok=True)
            doc = SimpleDocTemplate(
                str(output_pdf), pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18
            )

            # Get styles
            styles = getSampleStyleSheet()
            story = []

            # Parse HTML and convert to reportlab paragraphs
            # Remove HTML tags for simple text extraction
            text_content = re.sub("<[^<]+?>", "", html_content)
            text_content = html.unescape(text_content)

            # Split into paragraphs and add to story
            paragraphs = text_content.split("\n\n")
            for para_text in paragraphs:
                if para_text.strip():
                    # Determine style based on content
                    if para_text.startswith("#"):
                        style = styles["Heading1"]
                        cleaned_text = para_text.lstrip("#").strip()
                    elif para_text.strip().startswith("-") or para_text.strip().startswith("*"):
                        style = styles["Normal"]
                        cleaned_text = para_text.strip()
                    else:
                        style = styles["Normal"]
                        cleaned_text = para_text.strip()

                    para = Paragraph(cleaned_text, style)
                    story.append(para)
                    story.append(Spacer(1, 12))

            # Build PDF
            doc.build(story)

            self.console.print(f"[green]✅ PDF created with ReportLab: {output_pdf}[/green]")
            return True

        except Exception as e:
            self.console.print(f"[red]❌ Error converting to PDF: {e}[/red]")
            return False

    def batch_convert(
        self, input_dir: Path, output_dir: Path, _css_file: Optional[Path] = None, _css_string: Optional[str] = None
    ) -> dict:
        """
        Convert all markdown files in a directory to PDFs

        Args:
            input_dir: Directory containing markdown files
            output_dir: Directory for output PDF files
            css_file: Optional (ignored)
            css_string: Optional (ignored)

        Returns:
            dict: Dictionary of {markdown_file: success_bool}
        """
        results = {}

        if not input_dir.exists():
            self.console.print(f"[red]❌ Error: Input directory not found: {input_dir}[/red]")
            return results

        markdown_files = list(input_dir.glob("*.md"))

        if not markdown_files:
            self.console.print(f"[yellow]⚠️  No markdown files found in: {input_dir}[/yellow]")
            return results

        self.console.print(f"[blue]🔄 Converting {len(markdown_files)} markdown files to PDF...[/blue]")

        for md_file in markdown_files:
            output_pdf = output_dir / f"{md_file.stem}.pdf"
            success = self.convert_markdown_to_pdf(md_file, output_pdf)
            results[md_file] = success

        return results
