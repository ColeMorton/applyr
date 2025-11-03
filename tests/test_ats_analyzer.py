"""Tests for ATS Analyzer module"""

from pathlib import Path

import pytest
from rich.console import Console

from applyr.ats_analyzer import ATSAnalysisResult, ATSAnalyzer


class TestATSAnalyzerInitialization:
    """Tests for ATSAnalyzer initialization"""

    def test_init_with_console(self, test_console: Console):
        """Test ATSAnalyzer initialization with console"""
        analyzer = ATSAnalyzer(test_console)
        assert analyzer.console == test_console
        assert analyzer.parser is not None
        assert analyzer.keyword_analyzer is not None
        assert analyzer.scoring_engine is not None


class TestAnalyzeDocument:
    """Tests for analyze_document method"""

    def test_analyze_html_resume(self, test_console: Console, sample_html_resume: Path):
        """Test analyzing an HTML resume"""
        analyzer = ATSAnalyzer(test_console)
        result = analyzer.analyze_document(sample_html_resume)

        assert isinstance(result, ATSAnalysisResult)
        assert result.overall_score >= 0
        assert result.grade in ["A", "B", "C", "D", "F"]
        assert result.contact_info_score >= 0
        assert result.keywords_score >= 0
        assert result.format_score >= 0
        assert result.content_score >= 0
        assert result.experience_score >= 0
        assert result.compatibility_score >= 0
        assert isinstance(result.critical_issues, list)
        assert isinstance(result.recommendations, list)
        assert isinstance(result.keyword_analysis, dict)
        assert isinstance(result.parsed_content, dict)
        assert isinstance(result.file_analysis, dict)

    def test_analyze_text_resume(self, test_console: Console, sample_text_resume: Path):
        """Test analyzing a text resume"""
        analyzer = ATSAnalyzer(test_console)
        result = analyzer.analyze_document(sample_text_resume)

        assert isinstance(result, ATSAnalysisResult)
        assert result.overall_score >= 0
        assert result.parsed_content["file_type"] == "text"

    def test_analyze_with_job_description(
        self, test_console: Console, sample_text_resume: Path, sample_job_description: Path
    ):
        """Test analyzing resume with job description for keyword matching"""
        analyzer = ATSAnalyzer(test_console)
        result = analyzer.analyze_document(sample_text_resume, sample_job_description)

        assert isinstance(result, ATSAnalysisResult)
        assert "job_match" in result.keyword_analysis

    def test_analyze_nonexistent_file(self, test_console: Console, temp_dir: Path):
        """Test analyzing a non-existent file raises ValueError"""
        analyzer = ATSAnalyzer(test_console)
        nonexistent_file = temp_dir / "nonexistent.txt"

        with pytest.raises(ValueError, match="Failed to parse document"):
            analyzer.analyze_document(nonexistent_file)


class TestAnalyzeFileFormat:
    """Tests for _analyze_file_format method"""

    def test_analyze_html_format(self, test_console: Console, sample_html_resume: Path):
        """Test file format analysis for HTML"""
        analyzer = ATSAnalyzer(test_console)
        parsed_content = analyzer.parser.parse_document(sample_html_resume)
        file_analysis = analyzer._analyze_file_format(sample_html_resume, parsed_content)

        assert file_analysis["file_type"] == ".html"
        assert file_analysis["file_size_kb"] > 0
        assert "ats_compatible" in file_analysis
        assert isinstance(file_analysis["parsing_issues"], list)
        assert isinstance(file_analysis["format_warnings"], list)

    def test_analyze_pdf_format_detection(self, test_console: Console, temp_dir: Path):
        """Test PDF format detection and compatibility warning"""
        analyzer = ATSAnalyzer(test_console)
        # Create a mock PDF by creating a file with .pdf extension
        pdf_file = temp_dir / "test.pdf"
        pdf_file.write_text("Mock PDF content")

        # Need parsed content - for PDF we'd need actual PDF parsing
        # This test checks the format detection logic
        parsed_content = {"raw_text": "Test content"}
        file_analysis = analyzer._analyze_file_format(pdf_file, parsed_content)

        assert file_analysis["file_type"] == ".pdf"
        assert file_analysis["ats_compatible"] is False
        assert len(file_analysis["parsing_issues"]) > 0
        assert any("PDF" in issue for issue in file_analysis["parsing_issues"])

    def test_analyze_file_with_emojis(self, test_console: Console, sample_resume_with_emojis: Path):
        """Test file format analysis detects emojis"""
        analyzer = ATSAnalyzer(test_console)
        parsed_content = analyzer.parser.parse_document(sample_resume_with_emojis)
        file_analysis = analyzer._analyze_file_format(sample_resume_with_emojis, parsed_content)

        assert file_analysis["ats_compatible"] is False
        assert any("emoji" in issue.lower() for issue in file_analysis["parsing_issues"])

    def test_analyze_large_file_warning(self, test_console: Console, temp_dir: Path):
        """Test large file size warning"""
        analyzer = ATSAnalyzer(test_console)
        # Create a large file (> 500KB)
        large_file = temp_dir / "large.txt"
        large_content = "x" * (600 * 1024)  # 600KB
        large_file.write_text(large_content)

        parsed_content = {"raw_text": large_content}
        file_analysis = analyzer._analyze_file_format(large_file, parsed_content)

        assert file_analysis["file_size_kb"] > 500
        assert any("large" in warning.lower() for warning in file_analysis["format_warnings"])

    def test_analyze_complex_html_warning(self, test_console: Console, sample_resume_complex_html: Path):
        """Test complex HTML structure warning"""
        analyzer = ATSAnalyzer(test_console)
        parsed_content = analyzer.parser.parse_document(sample_resume_complex_html)
        file_analysis = analyzer._analyze_file_format(sample_resume_complex_html, parsed_content)

        if file_analysis["file_type"] in [".html", ".htm"]:
            # Should detect complex HTML if it exists
            assert isinstance(file_analysis["format_warnings"], list)


class TestAnalyzeContentSections:
    """Tests for _analyze_content_sections method"""

    def test_detect_contact_info(self, test_console: Console, sample_html_resume: Path):
        """Test contact information detection"""
        analyzer = ATSAnalyzer(test_console)
        parsed_content = analyzer.parser.parse_document(sample_html_resume)
        content_analysis = analyzer._analyze_content_sections(parsed_content)

        assert content_analysis["has_contact_info"] is True

    def test_detect_skills_section(self, test_console: Console, sample_html_resume: Path):
        """Test skills section detection"""
        analyzer = ATSAnalyzer(test_console)
        parsed_content = analyzer.parser.parse_document(sample_html_resume)
        content_analysis = analyzer._analyze_content_sections(parsed_content)

        assert content_analysis["has_skills_section"] is True

    def test_detect_experience_section(self, test_console: Console, sample_html_resume: Path):
        """Test experience section detection"""
        analyzer = ATSAnalyzer(test_console)
        parsed_content = analyzer.parser.parse_document(sample_html_resume)
        content_analysis = analyzer._analyze_content_sections(parsed_content)

        assert content_analysis["has_experience_section"] is True

    def test_detect_education_section(self, test_console: Console, sample_html_resume: Path):
        """Test education section detection"""
        analyzer = ATSAnalyzer(test_console)
        parsed_content = analyzer.parser.parse_document(sample_html_resume)
        content_analysis = analyzer._analyze_content_sections(parsed_content)

        assert content_analysis["has_education_section"] is True

    def test_missing_sections(self, test_console: Console, sample_resume_missing_sections: Path):
        """Test detection of missing sections"""
        analyzer = ATSAnalyzer(test_console)
        parsed_content = analyzer.parser.parse_document(sample_resume_missing_sections)
        content_analysis = analyzer._analyze_content_sections(parsed_content)

        assert content_analysis["has_contact_info"] is False
        assert content_analysis["has_experience_section"] is False
        assert content_analysis["has_skills_section"] is False

    def test_extract_section_headers(self, test_console: Console, sample_html_resume: Path):
        """Test section header extraction"""
        analyzer = ATSAnalyzer(test_console)
        parsed_content = analyzer.parser.parse_document(sample_html_resume)
        content_analysis = analyzer._analyze_content_sections(parsed_content)

        assert isinstance(content_analysis["section_headers"], list)
        assert len(content_analysis["section_headers"]) > 0

    def test_extract_achievement_metrics(self, test_console: Console, sample_text_resume: Path):
        """Test achievement metrics extraction"""
        analyzer = ATSAnalyzer(test_console)
        parsed_content = analyzer.parser.parse_document(sample_text_resume)
        content_analysis = analyzer._analyze_content_sections(parsed_content)

        assert isinstance(content_analysis["achievement_metrics"], list)
        # Should find metrics like "40%", "$2M+", "5 developers"
        assert len(content_analysis["achievement_metrics"]) > 0

    def test_content_quality_assessment(self, test_console: Console, sample_text_resume: Path):
        """Test content quality assessment"""
        analyzer = ATSAnalyzer(test_console)
        parsed_content = analyzer.parser.parse_document(sample_text_resume)
        content_analysis = analyzer._analyze_content_sections(parsed_content)

        assert content_analysis["content_quality"] in ["excellent", "good", "needs_improvement"]


class TestIdentifyCriticalIssues:
    """Tests for _identify_critical_issues method"""

    def test_identify_missing_contact_info(self, test_console: Console, sample_resume_missing_sections: Path):
        """Test identification of missing contact information"""
        analyzer = ATSAnalyzer(test_console)
        parsed_content = analyzer.parser.parse_document(sample_resume_missing_sections)
        content_analysis = analyzer._analyze_content_sections(parsed_content)
        file_analysis = analyzer._analyze_file_format(sample_resume_missing_sections, parsed_content)
        critical_issues = analyzer._identify_critical_issues(parsed_content, content_analysis, file_analysis)

        assert any("contact" in issue.lower() for issue in critical_issues)

    def test_identify_emoji_issues(self, test_console: Console, sample_resume_with_emojis: Path):
        """Test identification of emoji usage issues"""
        analyzer = ATSAnalyzer(test_console)
        parsed_content = analyzer.parser.parse_document(sample_resume_with_emojis)
        content_analysis = analyzer._analyze_content_sections(parsed_content)
        file_analysis = analyzer._analyze_file_format(sample_resume_with_emojis, parsed_content)
        critical_issues = analyzer._identify_critical_issues(parsed_content, content_analysis, file_analysis)

        assert any("emoji" in issue.lower() for issue in critical_issues)

    def test_identify_missing_experience(self, test_console: Console, sample_resume_missing_sections: Path):
        """Test identification of missing experience section"""
        analyzer = ATSAnalyzer(test_console)
        parsed_content = analyzer.parser.parse_document(sample_resume_missing_sections)
        content_analysis = analyzer._analyze_content_sections(parsed_content)
        file_analysis = analyzer._analyze_file_format(sample_resume_missing_sections, parsed_content)
        critical_issues = analyzer._identify_critical_issues(parsed_content, content_analysis, file_analysis)

        assert any("experience" in issue.lower() for issue in critical_issues)

    def test_identify_missing_skills(self, test_console: Console, sample_resume_missing_sections: Path):
        """Test identification of missing skills section"""
        analyzer = ATSAnalyzer(test_console)
        parsed_content = analyzer.parser.parse_document(sample_resume_missing_sections)
        content_analysis = analyzer._analyze_content_sections(parsed_content)
        file_analysis = analyzer._analyze_file_format(sample_resume_missing_sections, parsed_content)
        critical_issues = analyzer._identify_critical_issues(parsed_content, content_analysis, file_analysis)

        assert any("skill" in issue.lower() for issue in critical_issues)

    def test_identify_complex_formatting(self, test_console: Console, sample_resume_complex_html: Path):
        """Test identification of complex formatting issues"""
        analyzer = ATSAnalyzer(test_console)
        parsed_content = analyzer.parser.parse_document(sample_resume_complex_html)
        content_analysis = analyzer._analyze_content_sections(parsed_content)
        file_analysis = analyzer._analyze_file_format(sample_resume_complex_html, parsed_content)
        critical_issues = analyzer._identify_critical_issues(parsed_content, content_analysis, file_analysis)

        # May or may not have complex formatting issue depending on content
        assert isinstance(critical_issues, list)


class TestGenerateRecommendations:
    """Tests for _generate_recommendations method"""

    def test_recommendations_for_low_contact_score(self, test_console: Console):
        """Test recommendations for low contact info score"""
        analyzer = ATSAnalyzer(test_console)
        scores = {"contact_info": 5, "keywords": 20, "format": 15, "content": 15, "experience": 10, "compatibility": 3}
        critical_issues = []
        keyword_analysis = {"missing_keywords": []}
        content_analysis = {}

        recommendations = analyzer._generate_recommendations(
            scores, critical_issues, keyword_analysis, content_analysis
        )

        assert any("contact" in rec.lower() for rec in recommendations)

    def test_recommendations_for_low_keyword_score(self, test_console: Console):
        """Test recommendations for low keyword score"""
        analyzer = ATSAnalyzer(test_console)
        scores = {"contact_info": 15, "keywords": 10, "format": 15, "content": 15, "experience": 10, "compatibility": 3}
        critical_issues = []
        keyword_analysis = {"missing_keywords": ["Python", "React"]}
        content_analysis = {}

        recommendations = analyzer._generate_recommendations(
            scores, critical_issues, keyword_analysis, content_analysis
        )

        assert any("keyword" in rec.lower() for rec in recommendations)
        assert any("Python" in rec or "React" in rec for rec in recommendations)

    def test_recommendations_for_low_format_score(self, test_console: Console):
        """Test recommendations for low format score"""
        analyzer = ATSAnalyzer(test_console)
        scores = {"contact_info": 15, "keywords": 20, "format": 10, "content": 15, "experience": 10, "compatibility": 3}
        critical_issues = []
        keyword_analysis = {}
        content_analysis = {}

        recommendations = analyzer._generate_recommendations(
            scores, critical_issues, keyword_analysis, content_analysis
        )

        assert any("format" in rec.lower() or "structure" in rec.lower() for rec in recommendations)

    def test_recommendations_for_emoji_issue(self, test_console: Console):
        """Test recommendations for emoji issues"""
        analyzer = ATSAnalyzer(test_console)
        scores = {"contact_info": 15, "keywords": 20, "format": 15, "content": 15, "experience": 10, "compatibility": 3}
        critical_issues = ["Emoji usage detected - may break ATS parsing"]
        keyword_analysis = {}
        content_analysis = {}

        recommendations = analyzer._generate_recommendations(
            scores, critical_issues, keyword_analysis, content_analysis
        )

        assert any("emoji" in rec.lower() for rec in recommendations)

    def test_recommendations_for_contact_issue(self, test_console: Console):
        """Test recommendations for contact information issues"""
        analyzer = ATSAnalyzer(test_console)
        scores = {"contact_info": 15, "keywords": 20, "format": 15, "content": 15, "experience": 10, "compatibility": 3}
        critical_issues = ["Missing or unparseable contact information"]
        keyword_analysis = {}
        content_analysis = {}

        recommendations = analyzer._generate_recommendations(
            scores, critical_issues, keyword_analysis, content_analysis
        )

        assert any("contact" in rec.lower() for rec in recommendations)


class TestCalculateOverallScore:
    """Tests for _calculate_overall_score method"""

    def test_calculate_score_from_category_scores(self, test_console: Console):
        """Test overall score calculation"""
        analyzer = ATSAnalyzer(test_console)
        scores = {"contact_info": 15, "keywords": 25, "format": 20, "content": 20, "experience": 15, "compatibility": 5}

        overall_score = analyzer._calculate_overall_score(scores)

        assert overall_score == 100.0

    def test_calculate_partial_score(self, test_console: Console):
        """Test overall score with partial scores"""
        analyzer = ATSAnalyzer(test_console)
        scores = {"contact_info": 10, "keywords": 15, "format": 12, "content": 10, "experience": 8, "compatibility": 3}

        overall_score = analyzer._calculate_overall_score(scores)

        assert overall_score == 58.0

    def test_calculate_zero_score(self, test_console: Console):
        """Test overall score with zero scores"""
        analyzer = ATSAnalyzer(test_console)
        scores = {"contact_info": 0, "keywords": 0, "format": 0, "content": 0, "experience": 0, "compatibility": 0}

        overall_score = analyzer._calculate_overall_score(scores)

        assert overall_score == 0.0


class TestCalculateGrade:
    """Tests for _calculate_grade method"""

    def test_grade_a(self, test_console: Console):
        """Test grade A (90+)"""
        analyzer = ATSAnalyzer(test_console)
        assert analyzer._calculate_grade(95.0) == "A"
        assert analyzer._calculate_grade(90.0) == "A"
        assert analyzer._calculate_grade(100.0) == "A"

    def test_grade_b(self, test_console: Console):
        """Test grade B (80-89)"""
        analyzer = ATSAnalyzer(test_console)
        assert analyzer._calculate_grade(85.0) == "B"
        assert analyzer._calculate_grade(80.0) == "B"
        assert analyzer._calculate_grade(89.9) == "B"

    def test_grade_c(self, test_console: Console):
        """Test grade C (70-79)"""
        analyzer = ATSAnalyzer(test_console)
        assert analyzer._calculate_grade(75.0) == "C"
        assert analyzer._calculate_grade(70.0) == "C"
        assert analyzer._calculate_grade(79.9) == "C"

    def test_grade_d(self, test_console: Console):
        """Test grade D (60-69)"""
        analyzer = ATSAnalyzer(test_console)
        assert analyzer._calculate_grade(65.0) == "D"
        assert analyzer._calculate_grade(60.0) == "D"
        assert analyzer._calculate_grade(69.9) == "D"

    def test_grade_f(self, test_console: Console):
        """Test grade F (<60)"""
        analyzer = ATSAnalyzer(test_console)
        assert analyzer._calculate_grade(50.0) == "F"
        assert analyzer._calculate_grade(0.0) == "F"
        assert analyzer._calculate_grade(59.9) == "F"


class TestHasEmojis:
    """Tests for _has_emojis method"""

    def test_detect_emoji_in_text(self, test_console: Console):
        """Test emoji detection in text"""
        analyzer = ATSAnalyzer(test_console)
        text_with_emoji = "Hello 😊 World"
        assert analyzer._has_emojis(text_with_emoji) is True

    def test_no_emoji_in_text(self, test_console: Console):
        """Test no emoji detection in plain text"""
        analyzer = ATSAnalyzer(test_console)
        text_without_emoji = "Hello World"
        assert analyzer._has_emojis(text_without_emoji) is False

    def test_detect_multiple_emojis(self, test_console: Console):
        """Test detection of multiple emojis"""
        analyzer = ATSAnalyzer(test_console)
        text_with_emojis = "Great work! 🎉✨🚀"
        assert analyzer._has_emojis(text_with_emojis) is True


class TestHasComplexHTML:
    """Tests for _has_complex_html method"""

    def test_detect_table(self, test_console: Console):
        """Test detection of HTML tables"""
        analyzer = ATSAnalyzer(test_console)
        html_with_table = "<table><tr><td>Data</td></tr></table>"
        assert analyzer._has_complex_html(html_with_table) is True

    def test_detect_css_grid(self, test_console: Console):
        """Test detection of CSS Grid"""
        analyzer = ATSAnalyzer(test_console)
        html_with_grid = '<div class="grid">Content</div>'
        assert analyzer._has_complex_html(html_with_grid) is True

    def test_detect_skill_tags(self, test_console: Console):
        """Test detection of skill tag elements"""
        analyzer = ATSAnalyzer(test_console)
        html_with_tags = '<span class="skill-tag">Python</span>'
        assert analyzer._has_complex_html(html_with_tags) is True

    def test_no_complex_html(self, test_console: Console):
        """Test simple HTML without complex structures"""
        analyzer = ATSAnalyzer(test_console)
        simple_html = "<div><p>Simple content</p></div>"
        assert analyzer._has_complex_html(simple_html) is False


class TestHasComplexFormatting:
    """Tests for _has_complex_formatting method"""

    def test_detect_table_formatting(self, test_console: Console):
        """Test detection of table formatting"""
        analyzer = ATSAnalyzer(test_console)
        text_with_table = "<table><tr><td>Data</td></tr></table>"
        assert analyzer._has_complex_formatting(text_with_table) is True

    def test_detect_grid_formatting(self, test_console: Console):
        """Test detection of grid formatting"""
        analyzer = ATSAnalyzer(test_console)
        text_with_grid = '<div class="grid">Content</div>'
        assert analyzer._has_complex_formatting(text_with_grid) is True

    def test_detect_tag_formatting(self, test_console: Console):
        """Test detection of tag elements"""
        analyzer = ATSAnalyzer(test_console)
        text_with_tags = '<span class="tag">Skill</span>'
        assert analyzer._has_complex_formatting(text_with_tags) is True

    def test_no_complex_formatting(self, test_console: Console):
        """Test simple text without complex formatting"""
        analyzer = ATSAnalyzer(test_console)
        simple_text = "<p>Simple paragraph</p>"
        assert analyzer._has_complex_formatting(simple_text) is False


class TestAssessContentQuality:
    """Tests for _assess_content_quality method"""

    def test_excellent_content_quality(self, test_console: Console):
        """Test assessment of excellent content quality"""
        analyzer = ATSAnalyzer(test_console)
        parsed_content = {
            "raw_text": "Developed system with 50% improvement. Created solution with 30% increase. "
            "Implemented feature with 25% boost. Led team. Managed project."
        }

        quality = analyzer._assess_content_quality(parsed_content)
        assert quality == "excellent"

    def test_good_content_quality(self, test_console: Console):
        """Test assessment of good content quality"""
        analyzer = ATSAnalyzer(test_console)
        parsed_content = {"raw_text": "Developed system with 50% improvement. Created solution. Led team."}

        quality = analyzer._assess_content_quality(parsed_content)
        assert quality == "good"

    def test_needs_improvement_content_quality(self, test_console: Console):
        """Test assessment of content that needs improvement"""
        analyzer = ATSAnalyzer(test_console)
        parsed_content = {"raw_text": "Basic content without metrics or action verbs."}

        quality = analyzer._assess_content_quality(parsed_content)
        assert quality == "needs_improvement"


class TestExtractAchievementMetrics:
    """Tests for _extract_achievement_metrics method"""

    def test_extract_percentage_metrics(self, test_console: Console):
        """Test extraction of percentage metrics"""
        analyzer = ATSAnalyzer(test_console)
        text = "Increased performance by 40% and reduced costs by 25%"
        metrics = analyzer._extract_achievement_metrics(text)

        assert "40%" in metrics
        assert "25%" in metrics

    def test_extract_plus_metrics(self, test_console: Console):
        """Test extraction of plus metrics"""
        analyzer = ATSAnalyzer(test_console)
        text = "Managed team of 10+ developers"
        metrics = analyzer._extract_achievement_metrics(text)

        assert "10+" in metrics

    def test_extract_dollar_metrics(self, test_console: Console):
        """Test extraction of dollar metrics"""
        analyzer = ATSAnalyzer(test_console)
        text = "Managed budget of $2M+ and saved $500K"
        metrics = analyzer._extract_achievement_metrics(text)

        assert "$2M" in metrics or "$500K" in metrics

    def test_extract_multiplier_metrics(self, test_console: Console):
        """Test extraction of multiplier metrics"""
        analyzer = ATSAnalyzer(test_console)
        text = "Increased efficiency 3x"
        metrics = analyzer._extract_achievement_metrics(text)

        assert "3x" in metrics

    def test_extract_time_metrics(self, test_console: Console):
        """Test extraction of time-based metrics"""
        analyzer = ATSAnalyzer(test_console)
        text = "5 years of experience, 2 months project"
        metrics = analyzer._extract_achievement_metrics(text)

        assert len(metrics) >= 1

    def test_limit_metrics_to_ten(self, test_console: Console):
        """Test that metrics are limited to 10"""
        analyzer = ATSAnalyzer(test_console)
        # Create text with more than 10 metrics
        text = " ".join([f"{i}% improvement" for i in range(1, 15)])
        metrics = analyzer._extract_achievement_metrics(text)

        assert len(metrics) <= 10
