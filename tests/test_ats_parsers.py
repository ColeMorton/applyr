"""Tests for ATS Document Parser module"""

from pathlib import Path

from rich.console import Console

from applyr.ats_parsers import DocumentParser


class TestDocumentParserInitialization:
    """Tests for DocumentParser initialization"""

    def test_init_with_console(self, test_console: Console):
        """Test DocumentParser initialization with console"""
        parser = DocumentParser(test_console)
        assert parser.console == test_console


class TestParseDocument:
    """Tests for parse_document method"""

    def test_parse_html_file(self, test_console: Console, sample_html_resume: Path):
        """Test parsing HTML file"""
        parser = DocumentParser(test_console)
        result = parser.parse_document(sample_html_resume)

        assert result is not None
        assert result["file_type"] == "html"
        assert "raw_text" in result
        assert "contact_info" in result
        assert "sections" in result
        assert "skills" in result
        assert "html_structure" in result

    def test_parse_text_file(self, test_console: Console, sample_text_resume: Path):
        """Test parsing text file"""
        parser = DocumentParser(test_console)
        result = parser.parse_document(sample_text_resume)

        assert result is not None
        assert result["file_type"] == "text"
        assert "raw_text" in result
        assert "contact_info" in result
        assert "sections" in result
        assert "skills" in result

    def test_parse_markdown_file(self, test_console: Console, temp_dir: Path):
        """Test parsing markdown file"""
        parser = DocumentParser(test_console)
        md_file = temp_dir / "resume.md"
        md_file.write_text("# Resume\n\n## Experience\n\nWorked at company")

        result = parser.parse_document(md_file)

        assert result is not None
        assert result["file_type"] == "text"

    def test_parse_nonexistent_file(self, test_console: Console, temp_dir: Path):
        """Test parsing non-existent file returns None"""
        parser = DocumentParser(test_console)
        nonexistent = temp_dir / "nonexistent.txt"

        result = parser.parse_document(nonexistent)
        assert result is None

    def test_parse_unsupported_format(self, test_console: Console, temp_dir: Path):
        """Test parsing unsupported file format returns None"""
        parser = DocumentParser(test_console)
        unsupported = temp_dir / "file.xyz"
        unsupported.write_text("Content")

        result = parser.parse_document(unsupported)
        assert result is None

    def test_parse_htm_extension(self, test_console: Console, temp_dir: Path):
        """Test parsing .htm extension (alternative HTML)"""
        parser = DocumentParser(test_console)
        htm_file = temp_dir / "resume.htm"
        htm_file.write_text("<html><body><h1>Resume</h1></body></html>")

        result = parser.parse_document(htm_file)

        assert result is not None
        assert result["file_type"] == "html"


class TestParseHTML:
    """Tests for _parse_html method"""

    def test_parse_simple_html(self, test_console: Console, temp_dir: Path):
        """Test parsing simple HTML"""
        parser = DocumentParser(test_console)
        html_file = temp_dir / "simple.html"
        html_file.write_text("<html><body><p>Simple content</p></body></html>")

        result = parser._parse_html(html_file)

        assert result is not None
        assert result["file_type"] == "html"
        assert "Simple content" in result["raw_text"]

    def test_extract_contact_from_html(self, test_console: Console, sample_html_resume: Path):
        """Test contact info extraction from HTML"""
        parser = DocumentParser(test_console)
        result = parser._parse_html(sample_html_resume)

        assert result["contact_info"]["email"] == "john.doe@example.com"
        assert result["contact_info"]["phone"] == "555-123-4567"

    def test_extract_sections_from_html(self, test_console: Console, sample_html_resume: Path):
        """Test section extraction from HTML"""
        parser = DocumentParser(test_console)
        result = parser._parse_html(sample_html_resume)

        assert "sections" in result
        assert isinstance(result["sections"], dict)

    def test_analyze_html_structure(self, test_console: Console, sample_html_resume: Path):
        """Test HTML structure analysis"""
        parser = DocumentParser(test_console)
        result = parser._parse_html(sample_html_resume)

        assert "html_structure" in result
        assert "has_tables" in result["html_structure"]
        assert "has_complex_divs" in result["html_structure"]
        assert "nested_depth" in result["html_structure"]


class TestParseText:
    """Tests for _parse_text method"""

    def test_parse_simple_text(self, test_console: Console, temp_dir: Path):
        """Test parsing simple text file"""
        parser = DocumentParser(test_console)
        text_file = temp_dir / "simple.txt"
        text_file.write_text("Simple text content")

        result = parser._parse_text(text_file)

        assert result is not None
        assert result["file_type"] == "text"
        assert "Simple text content" in result["raw_text"]

    def test_process_markdown_in_text(self, test_console: Console, temp_dir: Path):
        """Test markdown processing in text parser"""
        parser = DocumentParser(test_console)
        md_file = temp_dir / "markdown.txt"
        md_file.write_text("# Header\n**Bold** text and [link](url)")

        result = parser._parse_text(md_file)

        # Markdown should be processed (headers, bold, links removed)
        assert "Header" in result["raw_text"]
        assert "Bold" in result["raw_text"]

    def test_extract_contact_from_text(self, test_console: Console, sample_text_resume: Path):
        """Test contact info extraction from text"""
        parser = DocumentParser(test_console)
        result = parser._parse_text(sample_text_resume)

        assert result["contact_info"]["email"] == "john.doe@example.com"
        assert result["contact_info"]["phone"] == "555-123-4567"


class TestExtractContactInfo:
    """Tests for _extract_contact_info method"""

    def test_extract_email(self, test_console: Console):
        """Test email extraction"""
        parser = DocumentParser(test_console)
        text = "Contact: test@example.com"
        contact = parser._extract_contact_info(text)

        assert contact["email"] == "test@example.com"

    def test_extract_phone_us_format(self, test_console: Console):
        """Test US phone format extraction"""
        parser = DocumentParser(test_console)
        text = "Phone: 555-123-4567"
        contact = parser._extract_contact_info(text)

        assert contact["phone"] == "555-123-4567"

    def test_extract_phone_australian_format(self, test_console: Console):
        """Test Australian phone format extraction"""
        parser = DocumentParser(test_console)
        text = "Phone: 0412 345 678"
        contact = parser._extract_contact_info(text)

        assert contact["phone"] == "0412 345 678"

    def test_extract_phone_parentheses_format(self, test_console: Console):
        """Test phone with parentheses format extraction"""
        parser = DocumentParser(test_console)
        text = "Phone: (555) 123-4567"
        contact = parser._extract_contact_info(text)

        assert contact["phone"] == "(555) 123-4567"

    def test_extract_linkedin(self, test_console: Console):
        """Test LinkedIn URL extraction"""
        parser = DocumentParser(test_console)
        text = "LinkedIn: linkedin.com/in/johndoe"
        contact = parser._extract_contact_info(text)

        assert contact["linkedin"] == "linkedin.com/in/johndoe"

    def test_extract_location_city_state(self, test_console: Console):
        """Test location extraction (City, State)"""
        parser = DocumentParser(test_console)
        text = "Location: San Francisco, CA"
        contact = parser._extract_contact_info(text)

        assert contact["location"] == "San Francisco, CA"

    def test_extract_location_with_zip(self, test_console: Console):
        """Test location extraction with ZIP code"""
        parser = DocumentParser(test_console)
        text = "Location: San Francisco, CA 94102"
        contact = parser._extract_contact_info(text)

        assert contact["location"] == "San Francisco, CA 94102"

    def test_extract_all_contact_info(self, test_console: Console):
        """Test extraction of all contact information"""
        parser = DocumentParser(test_console)
        text = """
        Email: test@example.com
        Phone: 555-123-4567
        Location: San Francisco, CA
        LinkedIn: linkedin.com/in/test
        """
        contact = parser._extract_contact_info(text)

        assert contact["email"] == "test@example.com"
        assert contact["phone"] == "555-123-4567"
        assert contact["location"] == "San Francisco, CA"
        assert contact["linkedin"] == "linkedin.com/in/test"

    def test_no_contact_info(self, test_console: Console):
        """Test extraction with no contact information"""
        parser = DocumentParser(test_console)
        text = "No contact information here"
        contact = parser._extract_contact_info(text)

        assert contact["email"] == ""
        assert contact["phone"] == ""
        assert contact["location"] == ""
        assert contact["linkedin"] == ""


class TestExtractSections:
    """Tests for _extract_sections method (HTML)"""

    def test_extract_experience_section(self, test_console: Console, temp_dir: Path):
        """Test experience section extraction from HTML"""
        parser = DocumentParser(test_console)
        html_content = """
        <html>
            <body>
                <h2>Experience</h2>
                <p>Software Engineer at Company</p>
                <p>5 years of experience</p>
            </body>
        </html>
        """
        html_file = temp_dir / "test.html"
        html_file.write_text(html_content)

        from bs4 import BeautifulSoup

        with open(html_file) as f:
            soup = BeautifulSoup(f.read(), "html.parser")

        sections = parser._extract_sections(soup)

        assert "experience" in sections
        assert "Software Engineer" in sections["experience"]

    def test_extract_skills_section(self, test_console: Console, temp_dir: Path):
        """Test skills section extraction from HTML"""
        parser = DocumentParser(test_console)
        html_content = """
        <html>
            <body>
                <h2>Skills</h2>
                <ul>
                    <li>Python</li>
                    <li>JavaScript</li>
                </ul>
            </body>
        </html>
        """
        html_file = temp_dir / "test.html"
        html_file.write_text(html_content)

        from bs4 import BeautifulSoup

        with open(html_file) as f:
            soup = BeautifulSoup(f.read(), "html.parser")

        sections = parser._extract_sections(soup)

        assert "skills" in sections
        assert "Python" in sections["skills"] or "JavaScript" in sections["skills"]


class TestExtractSectionsFromText:
    """Tests for _extract_sections_from_text method"""

    def test_extract_sections_from_text(self, test_console: Console):
        """Test section extraction from plain text"""
        parser = DocumentParser(test_console)
        text = """
        EXPERIENCE
        Software Engineer at Company
        5 years of experience

        SKILLS
        Python, JavaScript

        EDUCATION
        BS Computer Science
        """
        sections = parser._extract_sections_from_text(text)

        assert "experience" in sections
        assert "skills" in sections
        assert "education" in sections

    def test_extract_sections_title_case(self, test_console: Console):
        """Test section extraction with title case headers"""
        parser = DocumentParser(test_console)
        text = """
        Experience
        Worked at company

        Skills
        Python, JavaScript
        """
        sections = parser._extract_sections_from_text(text)

        assert "experience" in sections
        assert "skills" in sections


class TestExtractSkills:
    """Tests for _extract_skills method"""

    def test_extract_programming_languages(self, test_console: Console):
        """Test extraction of programming languages"""
        parser = DocumentParser(test_console)
        text = "Proficient in Python, JavaScript, and TypeScript"
        skills = parser._extract_skills(text)

        assert "Python" in skills or "python" in [s.lower() for s in skills]
        assert "JavaScript" in skills or "javascript" in [s.lower() for s in skills]

    def test_extract_databases(self, test_console: Console):
        """Test extraction of database technologies"""
        parser = DocumentParser(test_console)
        text = "Experience with MySQL, PostgreSQL, and MongoDB"
        skills = parser._extract_skills(text)

        assert len(skills) > 0

    def test_extract_cloud_platforms(self, test_console: Console):
        """Test extraction of cloud platforms"""
        parser = DocumentParser(test_console)
        text = "AWS, Azure, Docker, Kubernetes"
        skills = parser._extract_skills(text)

        assert len(skills) > 0

    def test_extract_methodologies(self, test_console: Console):
        """Test extraction of methodologies"""
        parser = DocumentParser(test_console)
        text = "Agile, Scrum, TDD, CI/CD"
        skills = parser._extract_skills(text)

        assert len(skills) > 0

    def test_no_skills_found(self, test_console: Console):
        """Test extraction with no skills in text"""
        parser = DocumentParser(test_console)
        text = "No technical skills mentioned here"
        skills = parser._extract_skills(text)

        assert isinstance(skills, list)


class TestAnalyzeHTMLStructure:
    """Tests for _analyze_html_structure method"""

    def test_detect_tables(self, test_console: Console, temp_dir: Path):
        """Test detection of HTML tables"""
        parser = DocumentParser(test_console)
        html_content = "<html><body><table><tr><td>Data</td></tr></table></body></html>"
        html_file = temp_dir / "test.html"
        html_file.write_text(html_content)

        from bs4 import BeautifulSoup

        with open(html_file) as f:
            soup = BeautifulSoup(f.read(), "html.parser")

        structure = parser._analyze_html_structure(soup)

        assert structure["has_tables"] is True

    def test_detect_complex_divs(self, test_console: Console, temp_dir: Path):
        """Test detection of complex divs (more than 10)"""
        parser = DocumentParser(test_console)
        html_content = (
            "<html><body>" + "".join([f'<div class="item{i}">Content</div>' for i in range(15)]) + "</body></html>"
        )
        html_file = temp_dir / "test.html"
        html_file.write_text(html_content)

        from bs4 import BeautifulSoup

        with open(html_file) as f:
            soup = BeautifulSoup(f.read(), "html.parser")

        structure = parser._analyze_html_structure(soup)

        assert structure["has_complex_divs"] is True

    def test_detect_images(self, test_console: Console, temp_dir: Path):
        """Test detection of images"""
        parser = DocumentParser(test_console)
        html_content = "<html><body><img src='photo.jpg' alt='Photo'></body></html>"
        html_file = temp_dir / "test.html"
        html_file.write_text(html_content)

        from bs4 import BeautifulSoup

        with open(html_file) as f:
            soup = BeautifulSoup(f.read(), "html.parser")

        structure = parser._analyze_html_structure(soup)

        assert structure["has_images"] is True

    def test_calculate_nesting_depth(self, test_console: Console, temp_dir: Path):
        """Test nesting depth calculation"""
        parser = DocumentParser(test_console)
        html_content = "<html><body><div><div><div><p>Deep</p></div></div></div></body></html>"
        html_file = temp_dir / "test.html"
        html_file.write_text(html_content)

        from bs4 import BeautifulSoup

        with open(html_file) as f:
            soup = BeautifulSoup(f.read(), "html.parser")

        structure = parser._analyze_html_structure(soup)

        assert structure["nested_depth"] >= 3


class TestCalculateNestingDepth:
    """Tests for _calculate_nesting_depth method"""

    def test_simple_nesting(self, test_console: Console, temp_dir: Path):
        """Test simple nesting depth"""
        parser = DocumentParser(test_console)
        html_content = "<html><body><div><p>Content</p></div></body></html>"
        html_file = temp_dir / "test.html"
        html_file.write_text(html_content)

        from bs4 import BeautifulSoup

        with open(html_file) as f:
            soup = BeautifulSoup(f.read(), "html.parser")

        depth = parser._calculate_nesting_depth(soup)

        assert depth >= 2

    def test_deep_nesting(self, test_console: Console, temp_dir: Path):
        """Test deep nesting depth"""
        parser = DocumentParser(test_console)
        html_content = "<html><body>" + "<div>" * 5 + "<p>Deep</p>" + "</div>" * 5 + "</body></html>"
        html_file = temp_dir / "test.html"
        html_file.write_text(html_content)

        from bs4 import BeautifulSoup

        with open(html_file) as f:
            soup = BeautifulSoup(f.read(), "html.parser")

        depth = parser._calculate_nesting_depth(soup)

        assert depth >= 5


class TestProcessMarkdown:
    """Tests for _process_markdown method"""

    def test_remove_headers(self, test_console: Console):
        """Test removal of markdown headers"""
        parser = DocumentParser(test_console)
        content = "# Header\n## Subheader\n### Subsubheader\nContent"
        processed = parser._process_markdown(content)

        assert "Header" in processed
        assert "#" not in processed or processed.count("#") < content.count("#")

    def test_remove_bold(self, test_console: Console):
        """Test removal of markdown bold"""
        parser = DocumentParser(test_console)
        content = "This is **bold** text"
        processed = parser._process_markdown(content)

        assert "bold" in processed
        assert "**" not in processed

    def test_remove_italic(self, test_console: Console):
        """Test removal of markdown italic"""
        parser = DocumentParser(test_console)
        content = "This is *italic* text"
        processed = parser._process_markdown(content)

        assert "italic" in processed
        assert "*italic*" not in processed

    def test_remove_links(self, test_console: Console):
        """Test removal of markdown links"""
        parser = DocumentParser(test_console)
        content = "Check out [this link](https://example.com)"
        processed = parser._process_markdown(content)

        assert "this link" in processed
        assert "https://example.com" not in processed or "[" not in processed

    def test_remove_list_markers(self, test_console: Console):
        """Test removal of markdown list markers"""
        parser = DocumentParser(test_console)
        content = "- Item 1\n- Item 2\n1. Numbered item"
        processed = parser._process_markdown(content)

        assert "Item 1" in processed
        assert "Item 2" in processed
        assert "Numbered item" in processed
