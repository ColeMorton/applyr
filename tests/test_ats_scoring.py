"""Tests for ATS Scoring module"""

import pytest
from rich.console import Console

from applyr.ats_scoring import ScoringEngine


class TestScoringEngineInitialization:
    """Tests for ScoringEngine initialization"""

    def test_init_with_console(self, test_console: Console):
        """Test ScoringEngine initialization with console"""
        engine = ScoringEngine(test_console)
        assert engine.console == test_console


class TestCalculateScores:
    """Tests for calculate_scores method"""

    def test_calculate_all_scores(self, test_console: Console):
        """Test calculation of all score categories"""
        engine = ScoringEngine(test_console)
        parsed_content = {
            "raw_text": "Email: test@example.com Phone: 555-1234 Location: San Francisco, CA",
            "contact_info": {"email": "test@example.com", "phone": "555-1234", "location": "San Francisco, CA"},
        }
        content_analysis = {
            "has_contact_info": True,
            "has_skills_section": True,
            "has_experience_section": True,
            "has_education_section": True,
        }
        keyword_analysis = {
            "found_keywords": {"technical": ["Python", "JavaScript", "React"]},
            "keyword_density": {"technical": 2.5},
            "job_match": {"match_percentage": 75, "has_job_description": True},
        }
        file_analysis = {"file_type": ".txt", "ats_compatible": True, "parsing_issues": []}

        scores = engine.calculate_scores(parsed_content, content_analysis, keyword_analysis, file_analysis)

        assert "contact_info" in scores
        assert "keywords" in scores
        assert "format" in scores
        assert "content" in scores
        assert "experience" in scores
        assert "compatibility" in scores
        assert all(0 <= score <= 100 for score in scores.values())


class TestScoreContactInfo:
    """Tests for _score_contact_info method"""

    def test_perfect_contact_info(self, test_console: Console):
        """Test perfect contact info score (15 points)"""
        engine = ScoringEngine(test_console)
        parsed_content = {
            "contact_info": {
                "email": "test@example.com",
                "phone": "555-123-4567",
                "location": "San Francisco, CA",
                "linkedin": "linkedin.com/in/test",
            },
            "raw_text": "Email: test@example.com Phone: 555-123-4567",
        }

        score = engine._score_contact_info(parsed_content)
        assert score == 15.0

    def test_email_only(self, test_console: Console):
        """Test contact info with email only (5 points)"""
        engine = ScoringEngine(test_console)
        parsed_content = {
            "contact_info": {"email": "test@example.com"},
            "raw_text": "test@example.com",
        }

        score = engine._score_contact_info(parsed_content)
        assert score == 5.0

    def test_email_in_text_only(self, test_console: Console):
        """Test email found in text but not parsed (4 points)"""
        engine = ScoringEngine(test_console)
        parsed_content = {
            "contact_info": {},
            "raw_text": "Contact me at test@example.com",
        }

        score = engine._score_contact_info(parsed_content)
        assert score == 4.0

    def test_phone_in_text(self, test_console: Console):
        """Test phone found in text (3-4 points)"""
        engine = ScoringEngine(test_console)
        parsed_content = {
            "contact_info": {"phone": "555-123-4567"},
            "raw_text": "Phone: 555-123-4567",
        }

        score = engine._score_contact_info(parsed_content)
        assert score >= 4.0

    def test_location_in_text(self, test_console: Console):
        """Test location found in text (2-3 points)"""
        engine = ScoringEngine(test_console)
        parsed_content = {
            "contact_info": {"location": "San Francisco, CA"},
            "raw_text": "Location: San Francisco, CA",
        }

        score = engine._score_contact_info(parsed_content)
        assert score >= 3.0

    def test_linkedin_in_text(self, test_console: Console):
        """Test LinkedIn found in text (2-3 points)"""
        engine = ScoringEngine(test_console)
        parsed_content = {
            "contact_info": {"linkedin": "linkedin.com/in/test"},
            "raw_text": "LinkedIn: linkedin.com/in/test",
        }

        score = engine._score_contact_info(parsed_content)
        assert score >= 3.0

    def test_no_contact_info(self, test_console: Console):
        """Test no contact information (0 points)"""
        engine = ScoringEngine(test_console)
        parsed_content = {"contact_info": {}, "raw_text": "No contact information here"}

        score = engine._score_contact_info(parsed_content)
        assert score == 0.0

    def test_score_capped_at_15(self, test_console: Console):
        """Test that score is capped at 15 points"""
        engine = ScoringEngine(test_console)
        parsed_content = {
            "contact_info": {
                "email": "test@example.com",
                "phone": "555-123-4567",
                "location": "San Francisco, CA",
                "linkedin": "linkedin.com/in/test",
            },
            "raw_text": "Email: test@example.com Phone: 555-123-4567 Location: San Francisco, CA",
        }

        score = engine._score_contact_info(parsed_content)
        assert score <= 15.0


class TestScoreKeywords:
    """Tests for _score_keywords method"""

    def test_high_technical_keywords(self, test_console: Console):
        """Test high technical keyword score (10 points for 10+ keywords)"""
        engine = ScoringEngine(test_console)
        keyword_analysis = {
            "found_keywords": {"technical": ["Python", "JavaScript", "TypeScript", "React", "Node.js"] * 2},
            "keyword_density": {"technical": 3.5},
            "job_match": {"match_percentage": 0, "has_job_description": False},
        }

        score = engine._score_keywords(keyword_analysis)
        assert score >= 10.0

    def test_medium_keyword_density(self, test_console: Console):
        """Test medium keyword density score"""
        engine = ScoringEngine(test_console)
        keyword_analysis = {
            "found_keywords": {"technical": ["Python", "JavaScript"]},
            "keyword_density": {"technical": 2.0},
            "job_match": {"match_percentage": 0, "has_job_description": False},
        }

        score = engine._score_keywords(keyword_analysis)
        assert score >= 6.0

    def test_high_job_match(self, test_console: Console):
        """Test high job match percentage"""
        engine = ScoringEngine(test_console)
        keyword_analysis = {
            "found_keywords": {"technical": ["Python", "JavaScript"]},
            "keyword_density": {"technical": 1.0},
            "job_match": {"match_percentage": 85, "has_job_description": True},
        }

        score = engine._score_keywords(keyword_analysis)
        assert score >= 7.0

    def test_no_job_description(self, test_console: Console):
        """Test scoring when no job description provided"""
        engine = ScoringEngine(test_console)
        keyword_analysis = {
            "found_keywords": {"technical": ["Python", "JavaScript"]},
            "keyword_density": {"technical": 1.0},
            "job_match": {"has_job_description": False},
        }

        score = engine._score_keywords(keyword_analysis)
        # Should get full points for job match component (7 points)
        assert score >= 7.0

    def test_score_capped_at_25(self, test_console: Console):
        """Test that keyword score is capped at 25 points"""
        engine = ScoringEngine(test_console)
        keyword_analysis = {
            "found_keywords": {"technical": ["Python"] * 20},
            "keyword_density": {"technical": 5.0},
            "job_match": {"match_percentage": 100, "has_job_description": True},
        }

        score = engine._score_keywords(keyword_analysis)
        assert score <= 25.0


class TestScoreFormat:
    """Tests for _score_format method"""

    def test_perfect_format(self, test_console: Console):
        """Test perfect format score (20 points)"""
        engine = ScoringEngine(test_console)
        parsed_content = {"raw_text": "Simple text content", "html_structure": {}}
        content_analysis = {
            "has_skills_section": True,
            "has_experience_section": True,
            "has_education_section": True,
            "section_headers": ["Experience", "Skills", "Education"],
        }
        file_analysis = {"file_type": ".txt", "parsing_issues": []}

        score = engine._score_format(parsed_content, content_analysis, file_analysis)
        assert score == 20.0

    def test_pdf_format_penalty(self, test_console: Console):
        """Test PDF format penalty (-5 points)"""
        engine = ScoringEngine(test_console)
        parsed_content = {"raw_text": "Content", "html_structure": {}}
        content_analysis = {
            "has_skills_section": True,
            "has_experience_section": True,
            "has_education_section": True,
            "section_headers": ["Experience", "Skills"],
        }
        file_analysis = {"file_type": "pdf", "parsing_issues": []}

        score = engine._score_format(parsed_content, content_analysis, file_analysis)
        assert score == 15.0

    def test_emoji_penalty(self, test_console: Console):
        """Test emoji usage penalty (-3 points)"""
        engine = ScoringEngine(test_console)
        parsed_content = {"raw_text": "Content 😊", "html_structure": {}}
        content_analysis = {
            "has_skills_section": True,
            "has_experience_section": True,
            "has_education_section": True,
            "section_headers": ["Experience", "Skills"],
        }
        file_analysis = {"file_type": ".txt", "parsing_issues": ["Emoji usage detected"]}

        score = engine._score_format(parsed_content, content_analysis, file_analysis)
        assert score == 17.0

    def test_missing_sections_penalty(self, test_console: Console):
        """Test missing section penalties"""
        engine = ScoringEngine(test_console)
        parsed_content = {"raw_text": "Content", "html_structure": {}}
        content_analysis = {
            "has_skills_section": False,
            "has_experience_section": False,
            "has_education_section": False,
            "section_headers": [],
        }
        file_analysis = {"file_type": ".txt", "parsing_issues": []}

        score = engine._score_format(parsed_content, content_analysis, file_analysis)
        # Should lose points for missing sections
        assert score < 20.0

    def test_complex_html_penalty(self, test_console: Console):
        """Test complex HTML structure penalty"""
        engine = ScoringEngine(test_console)
        parsed_content = {
            "raw_text": "Content",
            "html_structure": {"has_tables": True, "has_complex_divs": True, "nested_depth": 6},
        }
        content_analysis = {
            "has_skills_section": True,
            "has_experience_section": True,
            "has_education_section": True,
            "section_headers": ["Experience", "Skills"],
        }
        file_analysis = {"file_type": ".html", "parsing_issues": []}

        score = engine._score_format(parsed_content, content_analysis, file_analysis)
        # Should lose points for complex HTML
        assert score < 20.0

    def test_score_not_negative(self, test_console: Console):
        """Test that format score cannot be negative"""
        engine = ScoringEngine(test_console)
        parsed_content = {
            "raw_text": "Content",
            "html_structure": {"has_tables": True, "has_complex_divs": True, "nested_depth": 10},
        }
        content_analysis = {
            "has_skills_section": False,
            "has_experience_section": False,
            "has_education_section": False,
            "section_headers": [],
        }
        file_analysis = {"file_type": "pdf", "parsing_issues": ["Emoji usage detected"]}

        score = engine._score_format(parsed_content, content_analysis, file_analysis)
        assert score >= 0.0


class TestScoreContentQuality:
    """Tests for _score_content_quality method"""

    def test_optimal_content_length(self, test_console: Console):
        """Test optimal content length (300-800 words, 5 points)"""
        engine = ScoringEngine(test_console)
        parsed_content = {"raw_text": "word " * 500}
        content_analysis = {"content_quality": "excellent"}

        score = engine._score_content_quality(parsed_content, content_analysis)
        assert score >= 5.0

    def test_high_achievement_metrics(self, test_console: Console):
        """Test high achievement metrics score (8 points for 5+ metrics)"""
        engine = ScoringEngine(test_console)
        parsed_content = {
            "raw_text": "Increased by 40%. Reduced costs by 25%. Improved efficiency by 30%. "
            "Saved $100K. Managed 5 years. Optimized 3x."
        }
        content_analysis = {"content_quality": "excellent"}

        score = engine._score_content_quality(parsed_content, content_analysis)
        assert score >= 8.0

    def test_action_verbs_score(self, test_console: Console):
        """Test action verbs score (4 points for 8+ verbs)"""
        engine = ScoringEngine(test_console)
        parsed_content = {
            "raw_text": "Developed created implemented managed led increased improved designed built optimized "
            "delivered achieved"
        }
        content_analysis = {"content_quality": "excellent"}

        score = engine._score_content_quality(parsed_content, content_analysis)
        assert score >= 4.0

    def test_content_quality_assessment(self, test_console: Console):
        """Test content quality assessment score (3 points for excellent)"""
        engine = ScoringEngine(test_console)
        parsed_content = {"raw_text": "Content with metrics and verbs"}
        content_analysis = {"content_quality": "excellent"}

        score = engine._score_content_quality(parsed_content, content_analysis)
        assert score >= 3.0

    def test_score_capped_at_20(self, test_console: Console):
        """Test that content quality score is capped at 20 points"""
        engine = ScoringEngine(test_console)
        parsed_content = {
            "raw_text": (
                "word " * 500 + "Developed created implemented managed led increased improved designed built "
                "optimized delivered achieved " + "40% 50% 60% 70% 80% $1M $2M 2x 3x 4x"
            )
        }
        content_analysis = {"content_quality": "excellent"}

        score = engine._score_content_quality(parsed_content, content_analysis)
        assert score <= 20.0


class TestScoreExperience:
    """Tests for _score_experience method"""

    def test_experience_section_present(self, test_console: Console):
        """Test experience section presence (5 points)"""
        engine = ScoringEngine(test_console)
        parsed_content = {"raw_text": "Senior Software Engineer at Tech Company. Software Engineer at Startup Inc."}
        content_analysis = {
            "has_experience_section": True,
            "achievement_metrics": ["40%", "5 years", "$2M"],
        }

        score = engine._score_experience(parsed_content, content_analysis)
        assert score >= 5.0

    def test_job_titles_score(self, test_console: Console):
        """Test job titles score (5 points for 3+ titles)"""
        engine = ScoringEngine(test_console)
        parsed_content = {
            "raw_text": "Senior Software Engineer at Company. Lead Developer at Startup. "
            "Full Stack Developer at Corp. Software Architect at Tech."
        }
        content_analysis = {
            "has_experience_section": True,
            "achievement_metrics": [],
        }

        score = engine._score_experience(parsed_content, content_analysis)
        assert score >= 5.0

    def test_employment_dates_score(self, test_console: Console):
        """Test employment dates score (3 points for 4+ dates)"""
        engine = ScoringEngine(test_console)
        parsed_content = {
            "raw_text": "Jan 2020 - Present. Jan 2018 - Dec 2019. Jan 2016 - Dec 2017. Jan 2014 - Dec 2015."
        }
        content_analysis = {
            "has_experience_section": True,
            "achievement_metrics": [],
        }

        score = engine._score_experience(parsed_content, content_analysis)
        assert score >= 3.0

    def test_achievement_metrics_score(self, test_console: Console):
        """Test achievement metrics in experience (2 points for 3+ metrics)"""
        engine = ScoringEngine(test_console)
        parsed_content = {"raw_text": "Experience section"}
        content_analysis = {
            "has_experience_section": True,
            "achievement_metrics": ["40%", "5 years", "$2M", "3x"],
        }

        score = engine._score_experience(parsed_content, content_analysis)
        assert score >= 2.0

    def test_score_capped_at_15(self, test_console: Console):
        """Test that experience score is capped at 15 points"""
        engine = ScoringEngine(test_console)
        parsed_content = {
            "raw_text": "Senior Software Engineer at Tech. Lead Developer at Startup. "
            "Full Stack Developer at Corp. Jan 2020 - Present. Jan 2018 - Dec 2019. "
            "Jan 2016 - Dec 2017. Jan 2014 - Dec 2015."
        }
        content_analysis = {
            "has_experience_section": True,
            "achievement_metrics": ["40%", "5 years", "$2M", "3x"],
        }

        score = engine._score_experience(parsed_content, content_analysis)
        assert score <= 15.0

    def test_no_experience_section(self, test_console: Console):
        """Test score without experience section"""
        engine = ScoringEngine(test_console)
        parsed_content = {"raw_text": "No experience section"}
        content_analysis = {
            "has_experience_section": False,
            "achievement_metrics": [],
        }

        score = engine._score_experience(parsed_content, content_analysis)
        assert score < 5.0


class TestScoreCompatibility:
    """Tests for _score_compatibility method"""

    def test_perfect_compatibility(self, test_console: Console):
        """Test perfect ATS compatibility (5 points)"""
        engine = ScoringEngine(test_console)
        file_analysis = {"file_type": ".txt", "parsing_issues": [], "format_warnings": []}
        parsed_content = {"raw_text": "Simple content", "html_structure": {}}

        score = engine._score_compatibility(file_analysis, parsed_content)
        assert score == 5.0

    def test_pdf_format_penalty(self, test_console: Console):
        """Test PDF format compatibility penalty (-2 points)"""
        engine = ScoringEngine(test_console)
        file_analysis = {"file_type": "pdf", "parsing_issues": [], "format_warnings": []}
        parsed_content = {"raw_text": "Content", "html_structure": {}}

        score = engine._score_compatibility(file_analysis, parsed_content)
        assert score == 3.0

    def test_parsing_issues_penalty(self, test_console: Console):
        """Test parsing issues penalty (-0.5 per issue)"""
        engine = ScoringEngine(test_console)
        file_analysis = {
            "file_type": ".txt",
            "parsing_issues": ["Issue 1", "Issue 2"],
            "format_warnings": [],
        }
        parsed_content = {"raw_text": "Content", "html_structure": {}}

        score = engine._score_compatibility(file_analysis, parsed_content)
        assert score == 4.0

    def test_format_warnings_penalty(self, test_console: Console):
        """Test format warnings penalty (-0.3 per warning)"""
        engine = ScoringEngine(test_console)
        file_analysis = {
            "file_type": ".txt",
            "parsing_issues": [],
            "format_warnings": ["Warning 1", "Warning 2", "Warning 3"],
        }
        parsed_content = {"raw_text": "Content", "html_structure": {}}

        score = engine._score_compatibility(file_analysis, parsed_content)
        # Should lose 0.9 points (3 * 0.3)
        assert score == pytest.approx(4.1, abs=0.1)

    def test_emoji_penalty(self, test_console: Console):
        """Test emoji usage penalty (-1 point)"""
        engine = ScoringEngine(test_console)
        file_analysis = {
            "file_type": ".txt",
            "parsing_issues": ["Emoji usage detected"],
            "format_warnings": [],
        }
        parsed_content = {"raw_text": "Content", "html_structure": {}}

        score = engine._score_compatibility(file_analysis, parsed_content)
        # Should lose 1 point for emoji + 0.5 for parsing issue
        assert score == pytest.approx(3.5, abs=0.1)

    def test_complex_formatting_penalty(self, test_console: Console):
        """Test complex formatting penalty (-1 point)"""
        engine = ScoringEngine(test_console)
        file_analysis = {"file_type": ".html", "parsing_issues": [], "format_warnings": []}
        parsed_content = {
            "raw_text": "Content",
            "html_structure": {"has_tables": True, "has_complex_divs": True},
        }

        score = engine._score_compatibility(file_analysis, parsed_content)
        assert score == 4.0

    def test_score_not_negative(self, test_console: Console):
        """Test that compatibility score cannot be negative"""
        engine = ScoringEngine(test_console)
        file_analysis = {
            "file_type": "pdf",
            "parsing_issues": ["Issue 1", "Issue 2", "Emoji usage detected"],
            "format_warnings": ["Warning 1", "Warning 2", "Warning 3", "Warning 4"],
        }
        parsed_content = {
            "raw_text": "Content",
            "html_structure": {"has_tables": True, "has_complex_divs": True},
        }

        score = engine._score_compatibility(file_analysis, parsed_content)
        assert score >= 0.0
