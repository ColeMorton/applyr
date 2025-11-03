"""Tests for ATS Output Formatter module"""

import pytest
from rich.console import Console

from applyr.ats_analyzer import ATSAnalysisResult
from applyr.ats_output import ATSOutputFormatter


@pytest.fixture
def sample_analysis_result_excellent() -> ATSAnalysisResult:
    """Create a sample ATS analysis result with excellent score"""
    return ATSAnalysisResult(
        overall_score=95.0,
        grade="A",
        contact_info_score=15.0,
        keywords_score=25.0,
        format_score=20.0,
        content_score=20.0,
        experience_score=15.0,
        compatibility_score=5.0,
        critical_issues=[],
        recommendations=[],
        keyword_analysis={"found_keywords": {"technical": ["Python", "JavaScript"]}, "keyword_density": {}},
        parsed_content={"raw_text": "Sample content"},
        file_analysis={"file_type": ".txt", "ats_compatible": True},
    )


@pytest.fixture
def sample_analysis_result_poor() -> ATSAnalysisResult:
    """Create a sample ATS analysis result with poor score"""
    return ATSAnalysisResult(
        overall_score=45.0,
        grade="F",
        contact_info_score=5.0,
        keywords_score=10.0,
        format_score=8.0,
        content_score=10.0,
        experience_score=7.0,
        compatibility_score=2.0,
        critical_issues=["Missing contact information", "Emoji usage detected"],
        recommendations=["Add contact information", "Remove emojis"],
        keyword_analysis={"found_keywords": {}, "keyword_density": {}},
        parsed_content={"raw_text": "Content"},
        file_analysis={"file_type": ".pdf", "ats_compatible": False},
    )


class TestATSOutputFormatterInitialization:
    """Tests for ATSOutputFormatter initialization"""

    def test_init_with_console(self, test_console: Console):
        """Test ATSOutputFormatter initialization with console"""
        formatter = ATSOutputFormatter(test_console)
        assert formatter.console == test_console


class TestDisplayResults:
    """Tests for display_results method"""

    def test_display_basic_results(self, test_console: Console, sample_analysis_result_excellent: ATSAnalysisResult):
        """Test basic results display"""
        formatter = ATSOutputFormatter(test_console)
        # Should not raise exception
        formatter.display_results(sample_analysis_result_excellent, detailed=False)

    def test_display_detailed_results(self, test_console: Console, sample_analysis_result_excellent: ATSAnalysisResult):
        """Test detailed results display"""
        formatter = ATSOutputFormatter(test_console)
        # Should not raise exception
        formatter.display_results(sample_analysis_result_excellent, detailed=True)

    def test_display_with_critical_issues(self, test_console: Console, sample_analysis_result_poor: ATSAnalysisResult):
        """Test display with critical issues"""
        formatter = ATSOutputFormatter(test_console)
        # Should not raise exception
        formatter.display_results(sample_analysis_result_poor, detailed=False)

    def test_display_with_recommendations(self, test_console: Console, sample_analysis_result_poor: ATSAnalysisResult):
        """Test display with recommendations"""
        formatter = ATSOutputFormatter(test_console)
        # Should not raise exception
        formatter.display_results(sample_analysis_result_poor, detailed=False)


class TestDisplayOverallScore:
    """Tests for _display_overall_score method"""

    def test_display_excellent_score(self, test_console: Console, sample_analysis_result_excellent: ATSAnalysisResult):
        """Test display of excellent score (A grade)"""
        formatter = ATSOutputFormatter(test_console)
        # Should not raise exception
        formatter._display_overall_score(sample_analysis_result_excellent)

    def test_display_poor_score(self, test_console: Console, sample_analysis_result_poor: ATSAnalysisResult):
        """Test display of poor score (F grade)"""
        formatter = ATSOutputFormatter(test_console)
        # Should not raise exception
        formatter._display_overall_score(sample_analysis_result_poor)

    def test_display_score_grades(self, test_console: Console):
        """Test display of different score grades"""
        formatter = ATSOutputFormatter(test_console)

        # Test A grade
        result_a = ATSAnalysisResult(
            overall_score=95.0,
            grade="A",
            contact_info_score=15.0,
            keywords_score=25.0,
            format_score=20.0,
            content_score=20.0,
            experience_score=15.0,
            compatibility_score=5.0,
            critical_issues=[],
            recommendations=[],
            keyword_analysis={},
            parsed_content={},
            file_analysis={},
        )
        formatter._display_overall_score(result_a)

        # Test B grade
        result_b = ATSAnalysisResult(
            overall_score=85.0,
            grade="B",
            contact_info_score=15.0,
            keywords_score=20.0,
            format_score=18.0,
            content_score=18.0,
            experience_score=12.0,
            compatibility_score=4.0,
            critical_issues=[],
            recommendations=[],
            keyword_analysis={},
            parsed_content={},
            file_analysis={},
        )
        formatter._display_overall_score(result_b)

        # Test F grade
        result_f = ATSAnalysisResult(
            overall_score=45.0,
            grade="F",
            contact_info_score=5.0,
            keywords_score=10.0,
            format_score=8.0,
            content_score=10.0,
            experience_score=7.0,
            compatibility_score=2.0,
            critical_issues=[],
            recommendations=[],
            keyword_analysis={},
            parsed_content={},
            file_analysis={},
        )
        formatter._display_overall_score(result_f)


class TestDisplayCategoryScores:
    """Tests for _display_category_scores method"""

    def test_display_category_scores(self, test_console: Console, sample_analysis_result_excellent: ATSAnalysisResult):
        """Test category scores display"""
        formatter = ATSOutputFormatter(test_console)
        # Should not raise exception
        formatter._display_category_scores(sample_analysis_result_excellent)

    def test_display_all_categories(self, test_console: Console):
        """Test display of all category scores"""
        formatter = ATSOutputFormatter(test_console)
        result = ATSAnalysisResult(
            overall_score=80.0,
            grade="B",
            contact_info_score=15.0,
            keywords_score=25.0,
            format_score=20.0,
            content_score=20.0,
            experience_score=15.0,
            compatibility_score=5.0,
            critical_issues=[],
            recommendations=[],
            keyword_analysis={},
            parsed_content={},
            file_analysis={},
        )
        formatter._display_category_scores(result)


class TestDisplayCriticalIssues:
    """Tests for _display_critical_issues method"""

    def test_display_with_issues(self, test_console: Console, sample_analysis_result_poor: ATSAnalysisResult):
        """Test display with critical issues"""
        formatter = ATSOutputFormatter(test_console)
        # Should not raise exception
        formatter._display_critical_issues(sample_analysis_result_poor.critical_issues)

    def test_display_no_issues(self, test_console: Console):
        """Test display with no critical issues"""
        formatter = ATSOutputFormatter(test_console)
        # Should not raise exception (should handle empty list)
        formatter._display_critical_issues([])

    def test_display_multiple_issues(self, test_console: Console):
        """Test display with multiple critical issues"""
        formatter = ATSOutputFormatter(test_console)
        issues = [
            "Missing contact information",
            "Emoji usage detected",
            "Missing experience section",
            "Complex formatting detected",
        ]
        formatter._display_critical_issues(issues)


class TestDisplayRecommendations:
    """Tests for _display_recommendations method"""

    def test_display_with_recommendations(self, test_console: Console, sample_analysis_result_poor: ATSAnalysisResult):
        """Test display with recommendations"""
        formatter = ATSOutputFormatter(test_console)
        # Should not raise exception
        formatter._display_recommendations(sample_analysis_result_poor.recommendations)

    def test_display_no_recommendations(self, test_console: Console):
        """Test display with no recommendations"""
        formatter = ATSOutputFormatter(test_console)
        # Should not raise exception (should handle empty list)
        formatter._display_recommendations([])

    def test_display_contact_recommendations(self, test_console: Console):
        """Test display of contact-related recommendations"""
        formatter = ATSOutputFormatter(test_console)
        recommendations = [
            "Ensure contact information is clearly formatted",
            "Add email and phone number",
        ]
        formatter._display_recommendations(recommendations)

    def test_display_format_recommendations(self, test_console: Console):
        """Test display of format-related recommendations"""
        formatter = ATSOutputFormatter(test_console)
        recommendations = [
            "Use standard section headers",
            "Avoid complex HTML structures",
        ]
        formatter._display_recommendations(recommendations)

    def test_display_keyword_recommendations(self, test_console: Console):
        """Test display of keyword-related recommendations"""
        formatter = ATSOutputFormatter(test_console)
        recommendations = [
            "Add missing keywords: Python, React",
            "Increase keyword density",
        ]
        formatter._display_recommendations(recommendations)


class TestDisplayDetailedAnalysis:
    """Tests for _display_detailed_analysis method"""

    def test_display_detailed_analysis(
        self, test_console: Console, sample_analysis_result_excellent: ATSAnalysisResult
    ):
        """Test detailed analysis display"""
        formatter = ATSOutputFormatter(test_console)
        # Should not raise exception
        formatter._display_detailed_analysis(sample_analysis_result_excellent)

    def test_display_keyword_analysis(self, test_console: Console):
        """Test keyword analysis display"""
        formatter = ATSOutputFormatter(test_console)
        keyword_analysis = {
            "keyword_density": {"technical": 2.5, "tools": 1.0},
            "found_keywords": {"technical": ["Python", "JavaScript"], "soft_skills": ["Leadership"]},
            "job_match": {"match_percentage": 75.0, "has_job_description": True},
        }
        formatter._display_keyword_analysis(keyword_analysis)

    def test_display_file_analysis(self, test_console: Console):
        """Test file analysis display"""
        formatter = ATSOutputFormatter(test_console)
        file_analysis = {
            "file_type": ".txt",
            "file_size_kb": 25.5,
            "ats_compatible": True,
            "parsing_issues": [],
        }
        formatter._display_file_analysis(file_analysis)


class TestGetGrade:
    """Tests for _get_grade method"""

    def test_grade_a(self, test_console: Console):
        """Test grade A (90+)"""
        formatter = ATSOutputFormatter(test_console)
        assert formatter._get_grade(95.0) == "A"
        assert formatter._get_grade(90.0) == "A"
        assert formatter._get_grade(100.0) == "A"

    def test_grade_b(self, test_console: Console):
        """Test grade B (80-89)"""
        formatter = ATSOutputFormatter(test_console)
        assert formatter._get_grade(85.0) == "B"
        assert formatter._get_grade(80.0) == "B"
        assert formatter._get_grade(89.9) == "B"

    def test_grade_c(self, test_console: Console):
        """Test grade C (70-79)"""
        formatter = ATSOutputFormatter(test_console)
        assert formatter._get_grade(75.0) == "C"
        assert formatter._get_grade(70.0) == "C"
        assert formatter._get_grade(79.9) == "C"

    def test_grade_d(self, test_console: Console):
        """Test grade D (60-69)"""
        formatter = ATSOutputFormatter(test_console)
        assert formatter._get_grade(65.0) == "D"
        assert formatter._get_grade(60.0) == "D"
        assert formatter._get_grade(69.9) == "D"

    def test_grade_f(self, test_console: Console):
        """Test grade F (<60)"""
        formatter = ATSOutputFormatter(test_console)
        assert formatter._get_grade(50.0) == "F"
        assert formatter._get_grade(0.0) == "F"
        assert formatter._get_grade(59.9) == "F"


class TestGetStatus:
    """Tests for _get_status method"""

    def test_status_excellent(self, test_console: Console):
        """Test excellent status (90+)"""
        formatter = ATSOutputFormatter(test_console)
        assert formatter._get_status(95.0) == "Excellent"

    def test_status_good(self, test_console: Console):
        """Test good status (80-89)"""
        formatter = ATSOutputFormatter(test_console)
        assert formatter._get_status(85.0) == "Good"

    def test_status_fair(self, test_console: Console):
        """Test fair status (70-79)"""
        formatter = ATSOutputFormatter(test_console)
        assert formatter._get_status(75.0) == "Fair"

    def test_status_poor(self, test_console: Console):
        """Test poor status (60-69)"""
        formatter = ATSOutputFormatter(test_console)
        assert formatter._get_status(65.0) == "Poor"

    def test_status_critical(self, test_console: Console):
        """Test critical status (<60)"""
        formatter = ATSOutputFormatter(test_console)
        assert formatter._get_status(45.0) == "Critical"


class TestGetScoreColor:
    """Tests for _get_score_color method"""

    def test_color_green(self, test_console: Console):
        """Test green color for excellent scores (90+)"""
        formatter = ATSOutputFormatter(test_console)
        assert formatter._get_score_color(95.0) == "green"

    def test_color_blue(self, test_console: Console):
        """Test blue color for good scores (80-89)"""
        formatter = ATSOutputFormatter(test_console)
        assert formatter._get_score_color(85.0) == "blue"

    def test_color_yellow(self, test_console: Console):
        """Test yellow color for fair scores (70-79)"""
        formatter = ATSOutputFormatter(test_console)
        assert formatter._get_score_color(75.0) == "yellow"

    def test_color_orange(self, test_console: Console):
        """Test orange color for poor scores (60-69)"""
        formatter = ATSOutputFormatter(test_console)
        assert formatter._get_score_color(65.0) == "orange3"

    def test_color_red(self, test_console: Console):
        """Test red color for critical scores (<60)"""
        formatter = ATSOutputFormatter(test_console)
        assert formatter._get_score_color(45.0) == "red"
