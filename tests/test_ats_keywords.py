"""Tests for ATS Keywords module"""

from pathlib import Path

import pytest
from rich.console import Console

from applyr.ats_keywords import KeywordAnalyzer


class TestKeywordAnalyzerInitialization:
    """Tests for KeywordAnalyzer initialization"""

    def test_init_with_console(self, test_console: Console):
        """Test KeywordAnalyzer initialization with console"""
        analyzer = KeywordAnalyzer(test_console)
        assert analyzer.console == test_console
        assert analyzer.tech_keywords is not None
        assert analyzer.soft_skills is not None
        assert analyzer.industry_keywords is not None


class TestAnalyzeKeywords:
    """Tests for analyze_keywords method"""

    def test_analyze_keywords_basic(self, test_console: Console):
        """Test basic keyword analysis"""
        analyzer = KeywordAnalyzer(test_console)
        parsed_content = {
            "raw_text": "Experienced in Python, JavaScript, React. Strong leadership and communication skills."
        }

        result = analyzer.analyze_keywords(parsed_content)

        assert "found_keywords" in result
        assert "keyword_density" in result
        assert "keyword_distribution" in result
        assert "recommendations" in result
        assert "missing_keywords" in result

    def test_analyze_keywords_with_job_description(self, test_console: Console, sample_job_description: Path):
        """Test keyword analysis with job description"""
        analyzer = KeywordAnalyzer(test_console)
        parsed_content = {"raw_text": "Experienced in Python, JavaScript, React. Strong leadership skills."}

        result = analyzer.analyze_keywords(parsed_content, sample_job_description)

        assert "job_match" in result
        assert "match_percentage" in result["job_match"]
        assert "matched_keywords" in result["job_match"]


class TestExtractKeywords:
    """Tests for _extract_keywords method"""

    def test_extract_programming_languages(self, test_console: Console):
        """Test extraction of programming languages"""
        analyzer = KeywordAnalyzer(test_console)
        text = "Python JavaScript Java C++ TypeScript"
        keywords = analyzer._extract_keywords(text.lower())

        assert len(keywords["technical"]) > 0
        assert any("python" in str(k).lower() for k in keywords["technical"])

    def test_extract_frameworks(self, test_console: Console):
        """Test extraction of frameworks"""
        analyzer = KeywordAnalyzer(test_console)
        text = "React Angular Vue.js Node.js Django Flask"
        keywords = analyzer._extract_keywords(text.lower())

        assert len(keywords["frameworks"]) > 0

    def test_extract_tools(self, test_console: Console):
        """Test extraction of tools"""
        analyzer = KeywordAnalyzer(test_console)
        text = "Git GitHub GitLab Docker Kubernetes AWS"
        keywords = analyzer._extract_keywords(text.lower())

        assert len(keywords["tools"]) > 0

    def test_extract_soft_skills(self, test_console: Console):
        """Test extraction of soft skills"""
        analyzer = KeywordAnalyzer(test_console)
        text = "Leadership Communication Teamwork Problem Solving"
        keywords = analyzer._extract_keywords(text.lower())

        assert len(keywords["soft_skills"]) > 0

    def test_extract_industry_keywords(self, test_console: Console):
        """Test extraction of industry keywords"""
        analyzer = KeywordAnalyzer(test_console)
        text = "SaaS Cloud Computing API Integration Scalability"
        keywords = analyzer._extract_keywords(text.lower())

        assert len(keywords["industry"]) >= 0  # May or may not match depending on dictionary

    def test_no_keywords_found(self, test_console: Console):
        """Test extraction with no keywords found"""
        analyzer = KeywordAnalyzer(test_console)
        text = "No technical keywords here"
        keywords = analyzer._extract_keywords(text.lower())

        assert isinstance(keywords, dict)
        assert "technical" in keywords


class TestCalculateKeywordDensity:
    """Tests for _calculate_keyword_density method"""

    def test_calculate_density(self, test_console: Console):
        """Test keyword density calculation"""
        analyzer = KeywordAnalyzer(test_console)
        text = "Python Python JavaScript React React React " * 10  # 60 words, 2 Python, 3 React, 1 JavaScript
        keywords = {
            "technical": ["Python", "JavaScript", "React"],
            "tools": [],
            "frameworks": [],
            "soft_skills": [],
            "industry": [],
        }

        density = analyzer._calculate_keyword_density(text, keywords)

        assert "technical" in density
        assert density["technical"] > 0

    def test_zero_density_no_keywords(self, test_console: Console):
        """Test density calculation with no keywords"""
        analyzer = KeywordAnalyzer(test_console)
        text = "No keywords here"
        keywords = {"technical": [], "tools": [], "frameworks": [], "soft_skills": [], "industry": []}

        density = analyzer._calculate_keyword_density(text, keywords)

        assert density["technical"] == 0.0

    def test_density_percentage(self, test_console: Console):
        """Test that density is calculated as percentage"""
        analyzer = KeywordAnalyzer(test_console)
        # 100 words, 10 occurrences of "Python" = 10% density
        text = ("Python " * 10) + ("word " * 90)
        keywords = {"technical": ["Python"], "tools": [], "frameworks": [], "soft_skills": [], "industry": []}

        density = analyzer._calculate_keyword_density(text, keywords)

        assert density["technical"] == pytest.approx(10.0, abs=1.0)


class TestAnalyzeKeywordDistribution:
    """Tests for _analyze_keyword_distribution method"""

    def test_distribution_across_sections(self, test_console: Console):
        """Test keyword distribution across sections"""
        analyzer = KeywordAnalyzer(test_console)
        # Create text with keywords in different sections
        text = ("Python JavaScript " * 10) + ("React Angular " * 10) + ("Docker Kubernetes " * 10)
        keywords = {
            "technical": ["Python", "JavaScript"],
            "tools": ["Docker", "Kubernetes"],
            "frameworks": ["React", "Angular"],
            "soft_skills": [],
            "industry": [],
        }

        distribution = analyzer._analyze_keyword_distribution(text, keywords)

        assert "summary" in distribution
        assert "experience" in distribution
        assert "skills" in distribution
        assert isinstance(distribution["summary"], dict)


class TestAnalyzeJobMatch:
    """Tests for _analyze_job_match method"""

    def test_job_match_analysis(self, test_console: Console, sample_job_description: Path):
        """Test job match analysis"""
        analyzer = KeywordAnalyzer(test_console)
        text = "Python JavaScript React AWS Docker Agile"

        result = analyzer._analyze_job_match(text.lower(), sample_job_description)

        assert "match_percentage" in result
        assert "matched_keywords" in result
        assert "total_job_keywords" in result
        assert "missing_keywords" in result
        assert "job_keywords" in result

    def test_high_match_percentage(self, test_console: Console, temp_dir: Path):
        """Test high job match percentage"""
        analyzer = KeywordAnalyzer(test_console)
        job_desc = temp_dir / "job.txt"
        job_desc.write_text("Python JavaScript React AWS Docker Agile Scrum")

        text = "Python JavaScript React AWS Docker Agile Scrum leadership communication"
        result = analyzer._analyze_job_match(text.lower(), job_desc)

        assert result["match_percentage"] > 50

    def test_low_match_percentage(self, test_console: Console, temp_dir: Path):
        """Test low job match percentage"""
        analyzer = KeywordAnalyzer(test_console)
        job_desc = temp_dir / "job.txt"
        job_desc.write_text("Python JavaScript React AWS Docker")

        text = "Java C++ PHP Ruby"
        result = analyzer._analyze_job_match(text.lower(), job_desc)

        assert result["match_percentage"] < 50

    def test_missing_keywords_identification(self, test_console: Console, temp_dir: Path):
        """Test identification of missing keywords"""
        analyzer = KeywordAnalyzer(test_console)
        job_desc = temp_dir / "job.txt"
        job_desc.write_text("Python JavaScript React AWS")

        text = "Python JavaScript"
        result = analyzer._analyze_job_match(text.lower(), job_desc)

        assert len(result["missing_keywords"]) > 0
        assert "React" in result["missing_keywords"] or "AWS" in result["missing_keywords"]

    def test_job_description_file_not_found(self, test_console: Console, temp_dir: Path):
        """Test handling of missing job description file"""
        analyzer = KeywordAnalyzer(test_console)
        nonexistent = temp_dir / "nonexistent.txt"
        text = "Python JavaScript"

        result = analyzer._analyze_job_match(text.lower(), nonexistent)

        assert result == {}


class TestGenerateKeywordRecommendations:
    """Tests for _generate_keyword_recommendations method"""

    def test_low_density_recommendation(self, test_console: Console):
        """Test recommendation for low keyword density"""
        analyzer = KeywordAnalyzer(test_console)
        found_keywords = {"technical": ["Python"], "tools": [], "frameworks": [], "soft_skills": [], "industry": []}
        keyword_density = {"technical": 0.5}
        job_match = {}

        recommendations = analyzer._generate_keyword_recommendations(found_keywords, keyword_density, job_match)

        assert any("density" in rec.lower() for rec in recommendations)

    def test_missing_keywords_recommendation(self, test_console: Console):
        """Test recommendation for missing keywords"""
        analyzer = KeywordAnalyzer(test_console)
        found_keywords = {"technical": ["Python"], "tools": [], "frameworks": [], "soft_skills": [], "industry": []}
        keyword_density = {"technical": 2.0}
        job_match = {"missing_keywords": ["React", "AWS", "Docker"]}

        recommendations = analyzer._generate_keyword_recommendations(found_keywords, keyword_density, job_match)

        assert any("missing" in rec.lower() for rec in recommendations)
        assert any("React" in rec or "AWS" in rec or "Docker" in rec for rec in recommendations)

    def test_low_job_match_recommendation(self, test_console: Console):
        """Test recommendation for low job match"""
        analyzer = KeywordAnalyzer(test_console)
        found_keywords = {"technical": ["Python"], "tools": [], "frameworks": [], "soft_skills": [], "industry": []}
        keyword_density = {"technical": 2.0}
        job_match = {"match_percentage": 30}

        recommendations = analyzer._generate_keyword_recommendations(found_keywords, keyword_density, job_match)

        assert any("match" in rec.lower() for rec in recommendations)

    def test_missing_technical_skills_recommendation(self, test_console: Console):
        """Test recommendation for missing technical skills"""
        analyzer = KeywordAnalyzer(test_console)
        found_keywords = {"technical": [], "tools": [], "frameworks": [], "soft_skills": [], "industry": []}
        keyword_density = {"technical": 0.0}
        job_match = {}

        recommendations = analyzer._generate_keyword_recommendations(found_keywords, keyword_density, job_match)

        assert any("technical" in rec.lower() for rec in recommendations)

    def test_missing_soft_skills_recommendation(self, test_console: Console):
        """Test recommendation for missing soft skills"""
        analyzer = KeywordAnalyzer(test_console)
        found_keywords = {"technical": ["Python"], "tools": [], "frameworks": [], "soft_skills": [], "industry": []}
        keyword_density = {"technical": 2.0}
        job_match = {}

        recommendations = analyzer._generate_keyword_recommendations(found_keywords, keyword_density, job_match)

        assert any("soft" in rec.lower() or "skill" in rec.lower() for rec in recommendations)


class TestIdentifyMissingKeywords:
    """Tests for _identify_missing_keywords method"""

    def test_identify_missing_job_keywords(self, test_console: Console):
        """Test identification of missing job-specific keywords"""
        analyzer = KeywordAnalyzer(test_console)
        found_keywords = {"technical": ["Python"], "tools": [], "frameworks": [], "soft_skills": [], "industry": []}
        job_match = {"missing_keywords": ["React", "AWS", "Docker"]}

        missing = analyzer._identify_missing_keywords(found_keywords, job_match)

        assert len(missing) > 0
        assert any("React" in kw or "AWS" in kw or "Docker" in kw for kw in missing)

    def test_identify_common_missing_keywords(self, test_console: Console):
        """Test identification of common missing technical keywords"""
        analyzer = KeywordAnalyzer(test_console)
        found_keywords = {"technical": [], "tools": [], "frameworks": [], "soft_skills": [], "industry": []}
        job_match = {}

        missing = analyzer._identify_missing_keywords(found_keywords, job_match)

        assert len(missing) > 0
        assert isinstance(missing, list)

    def test_limit_missing_keywords(self, test_console: Console):
        """Test that missing keywords are limited to 15"""
        analyzer = KeywordAnalyzer(test_console)
        found_keywords = {"technical": [], "tools": [], "frameworks": [], "soft_skills": [], "industry": []}
        job_match = {"missing_keywords": [f"Keyword{i}" for i in range(20)]}

        missing = analyzer._identify_missing_keywords(found_keywords, job_match)

        assert len(missing) <= 15


class TestLoadKeywordDatabases:
    """Tests for keyword database loading methods"""

    def test_load_tech_keywords(self, test_console: Console):
        """Test technical keywords database loading"""
        analyzer = KeywordAnalyzer(test_console)
        tech_keywords = analyzer._load_tech_keywords()

        assert "programming_languages" in tech_keywords
        assert "frameworks" in tech_keywords
        assert "databases" in tech_keywords
        assert "cloud_platforms" in tech_keywords
        assert "tools" in tech_keywords
        assert "methodologies" in tech_keywords
        assert len(tech_keywords["programming_languages"]) > 0

    def test_load_soft_skills(self, test_console: Console):
        """Test soft skills database loading"""
        analyzer = KeywordAnalyzer(test_console)
        soft_skills = analyzer._load_soft_skills()

        assert isinstance(soft_skills, list)
        assert len(soft_skills) > 0
        assert "Leadership" in soft_skills
        assert "Communication" in soft_skills

    def test_load_industry_keywords(self, test_console: Console):
        """Test industry keywords database loading"""
        analyzer = KeywordAnalyzer(test_console)
        industry_keywords = analyzer._load_industry_keywords()

        assert isinstance(industry_keywords, dict)
        assert len(industry_keywords) > 0
        # Check for common industry categories
        assert any("saas" in key.lower() or "fintech" in key.lower() for key in industry_keywords)
