#!/usr/bin/env python3
"""Document parsers for various file formats"""

from pathlib import Path
import re
from typing import Any, Optional

from rich.console import Console

try:
    from bs4 import BeautifulSoup

    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False

try:
    import pdfplumber
    import PyPDF2

    HAS_PDF_LIBS = True
except ImportError:
    HAS_PDF_LIBS = False

try:
    from docx import Document

    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False


class DocumentParser:
    """Multi-format document parser for ATS analysis"""

    def __init__(self, console: Console):
        self.console = console

    def parse_document(self, file_path: Path) -> Optional[dict[str, Any]]:  # noqa: PLR0911
        """
        Parse document based on file extension

        Args:
            file_path: Path to document

        Returns:
            Parsed content dictionary or None if parsing fails
        """
        if not file_path.exists():
            self.console.print(f"[red]❌ File not found: {file_path}[/red]")
            return None

        file_ext = file_path.suffix.lower()

        try:
            if file_ext in [".html", ".htm"]:
                return self._parse_html(file_path)
            elif file_ext == ".pdf":
                return self._parse_pdf(file_path)
            elif file_ext in [".txt", ".md"]:
                return self._parse_text(file_path)
            elif file_ext == ".docx":
                return self._parse_docx(file_path)
            else:
                self.console.print(f"[red]❌ Unsupported file format: {file_ext}[/red]")
                return None
        except Exception as e:
            self.console.print(f"[red]❌ Error parsing {file_path.name}: {e}[/red]")
            return None

    def _parse_html(self, file_path: Path) -> dict[str, Any]:
        """Parse HTML document"""
        if not HAS_BS4:
            self.console.print("[yellow]⚠️  BeautifulSoup not available, using basic text extraction[/yellow]")
            return self._parse_text(file_path)

        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        soup = BeautifulSoup(content, "html.parser")

        # Extract text content
        text_content = soup.get_text(separator=" ", strip=True)

        # Extract structured data
        contact_info = self._extract_contact_info(text_content)
        sections = self._extract_sections(soup)
        skills = self._extract_skills(text_content)

        return {
            "file_type": "html",
            "raw_text": text_content,
            "contact_info": contact_info,
            "sections": sections,
            "skills": skills,
            "html_structure": self._analyze_html_structure(soup),
        }

    def _parse_pdf(self, file_path: Path) -> Optional[dict[str, Any]]:
        """Parse PDF document"""
        if not HAS_PDF_LIBS:
            self.console.print("[red]❌ PDF parsing libraries not available[/red]")
            return None

        text_content = ""
        parsing_issues = []

        try:
            # Try pdfplumber first (better text extraction)
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_content += page_text + "\n"
        except Exception as e:
            parsing_issues.append(f"pdfplumber failed: {e}")

            # Fallback to PyPDF2
            try:
                with open(file_path, "rb") as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    for page in pdf_reader.pages:
                        text_content += page.extract_text() + "\n"
            except Exception as e2:
                parsing_issues.append(f"PyPDF2 failed: {e2}")
                return None

        if not text_content.strip():
            parsing_issues.append("No text content extracted from PDF")
            return None

        # Extract structured data
        contact_info = self._extract_contact_info(text_content)
        sections = self._extract_sections_from_text(text_content)
        skills = self._extract_skills(text_content)

        return {
            "file_type": "pdf",
            "raw_text": text_content,
            "contact_info": contact_info,
            "sections": sections,
            "skills": skills,
            "parsing_issues": parsing_issues,
        }

    def _parse_text(self, file_path: Path) -> dict[str, Any]:
        """Parse plain text or markdown document"""
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        # Basic markdown processing
        text_content = self._process_markdown(content)

        # Extract structured data
        contact_info = self._extract_contact_info(text_content)
        sections = self._extract_sections_from_text(text_content)
        skills = self._extract_skills(text_content)

        return {
            "file_type": "text",
            "raw_text": text_content,
            "contact_info": contact_info,
            "sections": sections,
            "skills": skills,
        }

    def _parse_docx(self, file_path: Path) -> Optional[dict[str, Any]]:
        """Parse DOCX document"""
        if not HAS_DOCX:
            self.console.print("[red]❌ python-docx not available[/red]")
            return None

        try:
            doc = Document(str(file_path))
            text_content = ""

            for paragraph in doc.paragraphs:
                text_content += paragraph.text + "\n"

            # Extract structured data
            contact_info = self._extract_contact_info(text_content)
            sections = self._extract_sections_from_text(text_content)
            skills = self._extract_skills(text_content)

            return {
                "file_type": "docx",
                "raw_text": text_content,
                "contact_info": contact_info,
                "sections": sections,
                "skills": skills,
            }
        except Exception as e:
            self.console.print(f"[red]❌ Error parsing DOCX: {e}[/red]")
            return None

    def _extract_contact_info(self, text: str) -> dict[str, str]:
        """Extract contact information from text"""
        contact = {"email": "", "phone": "", "location": "", "linkedin": ""}

        # Email pattern
        email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        email_match = re.search(email_pattern, text)
        if email_match:
            contact["email"] = email_match.group()

        # Phone pattern (various formats)
        phone_patterns = [
            r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b",  # US format
            r"\b\d{4}\s?\d{3}\s?\d{3}\b",  # Australian format
            r"\(\d{3}\)\s?\d{3}[-.\s]?\d{4}",  # (xxx) xxx-xxxx
        ]

        for pattern in phone_patterns:
            phone_match = re.search(pattern, text)
            if phone_match:
                contact["phone"] = phone_match.group()
                break

        # LinkedIn pattern
        linkedin_pattern = r"linkedin\.com/in/[\w-]+"
        linkedin_match = re.search(linkedin_pattern, text, re.IGNORECASE)
        if linkedin_match:
            contact["linkedin"] = linkedin_match.group()

        # Location pattern (handles multi-word city names)
        location_patterns = [
            r"\b(?:[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),\s*[A-Z]{2}\s*\d{5}\b",  # City, State ZIP
            r"\b(?:[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),\s*[A-Z]{2}\b",  # City, State
        ]

        for pattern in location_patterns:
            location_match = re.search(pattern, text)
            if location_match:
                contact["location"] = location_match.group()
                break

        return contact

    def _extract_sections(self, soup: BeautifulSoup) -> dict[str, str]:
        """Extract sections from HTML using BeautifulSoup"""
        sections = {}

        # Look for common section headers
        section_patterns = {
            "experience": ["experience", "employment", "work history", "professional"],
            "skills": ["skills", "technologies", "competencies", "technical"],
            "education": ["education", "academic", "qualifications"],
            "summary": ["summary", "objective", "profile", "about"],
        }

        # Find all headers
        headers = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])

        for header in headers:
            header_text = header.get_text().strip().lower()

            for section_type, patterns in section_patterns.items():
                if any(pattern in header_text for pattern in patterns):
                    # Extract content until next header
                    content = []
                    current = header.next_sibling
                    while current and current.name not in ["h1", "h2", "h3", "h4", "h5", "h6"]:
                        if hasattr(current, "get_text"):
                            content.append(current.get_text().strip())
                        current = current.next_sibling

                    sections[section_type] = " ".join(content)
                    break

        return sections

    def _extract_sections_from_text(self, text: str) -> dict[str, str]:
        """Extract sections from plain text"""
        sections = {}

        # Split text into lines
        lines = text.split("\n")

        # Look for section headers (lines that are all caps or title case)
        section_headers = []
        for i, line in enumerate(lines):
            stripped_line = line.strip()
            if (
                len(stripped_line) > 3
                and len(stripped_line) < 50
                and (stripped_line.isupper() or stripped_line.istitle())
                and not any(char.isdigit() for char in stripped_line)
            ):
                # Check if line looks like a section header
                section_headers.append((i, stripped_line))

        # Extract content for each section
        for i, (line_num, header) in enumerate(section_headers):
            start_line = line_num + 1
            end_line = section_headers[i + 1][0] if i + 1 < len(section_headers) else len(lines)

            content = "\n".join(lines[start_line:end_line]).strip()

            # Map header to section type
            header_lower = header.lower()
            if any(word in header_lower for word in ["experience", "employment", "work"]):
                sections["experience"] = content
            elif any(word in header_lower for word in ["skills", "technologies", "competencies"]):
                sections["skills"] = content
            elif any(word in header_lower for word in ["education", "academic"]):
                sections["education"] = content
            elif any(word in header_lower for word in ["summary", "objective", "profile"]):
                sections["summary"] = content

        return sections

    def _extract_skills(self, text: str) -> list[str]:
        """Extract skills from text"""
        # Common technical skills patterns
        skill_patterns = [
            r"\b(?:JavaScript|Python|Java|C\+\+|React|Angular|Vue|Node\.?js|TypeScript)\b",
            r"\b(?:HTML|CSS|SQL|MongoDB|PostgreSQL|MySQL|Redis)\b",
            r"\b(?:AWS|Azure|Docker|Kubernetes|Git|GitHub|GitLab)\b",
            r"\b(?:Agile|Scrum|TDD|CI/CD|REST|API|GraphQL)\b",
        ]

        skills = set()
        for pattern in skill_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            skills.update(matches)

        return list(skills)

    def _analyze_html_structure(self, soup: BeautifulSoup) -> dict[str, Any]:
        """Analyze HTML structure for ATS compatibility"""
        structure = {
            "has_tables": bool(soup.find("table")),
            "has_complex_divs": len(soup.find_all("div", class_=True)) > 10,
            "has_images": bool(soup.find("img")),
            "has_forms": bool(soup.find("form")),
            "nested_depth": self._calculate_nesting_depth(soup),
            "css_classes": len(soup.find_all(class_=True)),
        }

        return structure

    def _calculate_nesting_depth(self, soup: BeautifulSoup) -> int:
        """Calculate maximum nesting depth in HTML"""
        max_depth = 0

        def get_depth(element, current_depth=0):
            nonlocal max_depth
            max_depth = max(max_depth, current_depth)
            for child in element.find_all(recursive=False):
                get_depth(child, current_depth + 1)

        get_depth(soup)
        return max_depth

    def _process_markdown(self, content: str) -> str:
        """Basic markdown processing"""
        # Remove markdown headers
        content = re.sub(r"^#+\s*", "", content, flags=re.MULTILINE)

        # Remove markdown bold/italic
        content = re.sub(r"\*\*(.*?)\*\*", r"\1", content)
        content = re.sub(r"\*(.*?)\*", r"\1", content)

        # Remove markdown links
        content = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", content)

        # Remove markdown lists
        content = re.sub(r"^\s*[-*+]\s*", "", content, flags=re.MULTILINE)
        content = re.sub(r"^\s*\d+\.\s*", "", content, flags=re.MULTILINE)

        return content
