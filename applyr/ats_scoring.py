#!/usr/bin/env python3
"""Scoring engine for ATS analysis"""

import re

from rich.console import Console


class ScoringEngine:
    """Comprehensive scoring engine for ATS analysis"""

    def __init__(self, console: Console):
        self.console = console

    def calculate_scores(
        self, parsed_content: dict, content_analysis: dict, keyword_analysis: dict, file_analysis: dict
    ) -> dict[str, float]:
        """
        Calculate comprehensive ATS scores

        Args:
            parsed_content: Parsed document content
            content_analysis: Content structure analysis
            keyword_analysis: Keyword analysis results
            file_analysis: File format analysis

        Returns:
            Dictionary of scores for each category
        """
        scores = {}

        # Contact Information Score (15 points)
        scores["contact_info"] = self._score_contact_info(parsed_content)

        # Keywords & Skills Score (25 points)
        scores["keywords"] = self._score_keywords(keyword_analysis)

        # Format & Structure Score (20 points)
        scores["format"] = self._score_format(parsed_content, content_analysis, file_analysis)

        # Content Quality Score (20 points)
        scores["content"] = self._score_content_quality(parsed_content, content_analysis)

        # Experience Presentation Score (15 points)
        scores["experience"] = self._score_experience(parsed_content, content_analysis)

        # Overall ATS Compatibility Score (5 points)
        scores["compatibility"] = self._score_compatibility(file_analysis, parsed_content)

        return scores

    def _score_contact_info(self, parsed_content: dict) -> float:
        """Score contact information completeness and format (15 points)"""
        score = 0.0
        contact_info = parsed_content.get("contact_info", {})

        # Email (5 points)
        if contact_info.get("email"):
            score += 5.0
        elif re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", parsed_content.get("raw_text", "")):
            score += 4.0  # Found in text but not parsed

        # Phone (4 points)
        if contact_info.get("phone"):
            score += 4.0
        elif re.search(
            r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b|\b\d{4}\s?\d{3}\s?\d{3}\b", parsed_content.get("raw_text", "")
        ):
            score += 3.0  # Found in text but not parsed

        # Location (3 points)
        if contact_info.get("location"):
            score += 3.0
        elif re.search(r"\b[A-Z][a-z]+,\s*[A-Z]{2}\b", parsed_content.get("raw_text", "")):
            score += 2.0

        # LinkedIn (3 points)
        if contact_info.get("linkedin"):
            score += 3.0
        elif re.search(r"linkedin\.com/in/[\w-]+", parsed_content.get("raw_text", ""), re.IGNORECASE):
            score += 2.0

        return min(score, 15.0)

    def _score_keywords(self, keyword_analysis: dict) -> float:
        """Score keyword density and relevance (25 points)"""
        score = 0.0

        # Technical keywords (10 points)
        tech_keywords = keyword_analysis.get("found_keywords", {}).get("technical", [])
        if len(tech_keywords) >= 10:
            score += 10.0
        elif len(tech_keywords) >= 5:
            score += 7.0
        elif len(tech_keywords) >= 3:
            score += 5.0
        elif len(tech_keywords) >= 1:
            score += 3.0

        # Keyword density (8 points)
        density = keyword_analysis.get("keyword_density", {})
        avg_density = sum(density.values()) / len(density) if density else 0

        if avg_density >= 3.0:
            score += 8.0
        elif avg_density >= 2.0:
            score += 6.0
        elif avg_density >= 1.0:
            score += 4.0
        elif avg_density >= 0.5:
            score += 2.0

        # Job match (7 points) - only penalize if job description provided but no match
        job_match = keyword_analysis.get("job_match", {})
        match_percentage = job_match.get("match_percentage", 0)
        has_job_description = job_match.get("has_job_description", False)

        if has_job_description:
            # Job description provided - score based on match
            if match_percentage >= 80:
                score += 7.0
            elif match_percentage >= 60:
                score += 5.0
            elif match_percentage >= 40:
                score += 3.0
            elif match_percentage >= 20:
                score += 1.0
        else:
            # No job description - give full points for job match component
            score += 7.0

        return min(score, 25.0)

    def _score_format(self, parsed_content: dict, content_analysis: dict, file_analysis: dict) -> float:
        """Score format and structure (20 points)"""
        score = 20.0  # Start with full points, deduct for issues

        # File format penalties
        if file_analysis.get("file_type") == "pdf":
            score -= 5.0  # PDF format penalty

        # Emoji usage penalty
        if file_analysis.get("parsing_issues"):
            for issue in file_analysis["parsing_issues"]:
                if "emoji" in issue.lower():
                    score -= 3.0

        # Complex HTML structure penalty
        html_structure = parsed_content.get("html_structure", {})
        if html_structure.get("has_tables"):
            score -= 2.0
        if html_structure.get("has_complex_divs"):
            score -= 2.0
        if html_structure.get("nested_depth", 0) > 5:
            score -= 1.0

        # Missing section headers
        if not content_analysis.get("has_skills_section"):
            score -= 2.0
        if not content_analysis.get("has_experience_section"):
            score -= 3.0
        if not content_analysis.get("has_education_section"):
            score -= 1.0

        # Section header quality
        section_headers = content_analysis.get("section_headers", [])
        standard_headers = ["experience", "skills", "education", "summary"]
        found_standard = sum(1 for header in section_headers if any(std in header.lower() for std in standard_headers))

        if found_standard < 2:
            score -= 2.0

        return max(score, 0.0)

    def _score_content_quality(self, parsed_content: dict, content_analysis: dict) -> float:
        """Score content quality and clarity (20 points)"""
        score = 0.0
        text = parsed_content.get("raw_text", "")

        # Content length (5 points)
        word_count = len(text.split())
        if word_count >= 300 and word_count <= 800:
            score += 5.0
        elif word_count >= 200 and word_count <= 1000:
            score += 3.0
        elif word_count >= 100:
            score += 1.0

        # Quantified achievements (8 points)
        metrics = re.findall(r"\b\d+%|\b\d+\+|\$\d+|\d+x\b|\d+\s*(years?|months?)", text)
        if len(metrics) >= 5:
            score += 8.0
        elif len(metrics) >= 3:
            score += 6.0
        elif len(metrics) >= 1:
            score += 4.0

        # Action verbs (4 points)
        action_verbs = [
            "developed",
            "created",
            "implemented",
            "managed",
            "led",
            "increased",
            "improved",
            "designed",
            "built",
            "optimized",
            "delivered",
            "achieved",
        ]
        verb_count = sum(1 for verb in action_verbs if verb in text.lower())

        if verb_count >= 8:
            score += 4.0
        elif verb_count >= 5:
            score += 3.0
        elif verb_count >= 3:
            score += 2.0
        elif verb_count >= 1:
            score += 1.0

        # Content quality assessment (3 points)
        quality = content_analysis.get("content_quality", "needs_improvement")
        if quality == "excellent":
            score += 3.0
        elif quality == "good":
            score += 2.0
        elif quality == "needs_improvement":
            score += 1.0

        return min(score, 20.0)

    def _score_experience(self, parsed_content: dict, content_analysis: dict) -> float:
        """Score experience presentation (15 points)"""
        score = 0.0
        text = parsed_content.get("raw_text", "")

        # Experience section presence (5 points)
        if content_analysis.get("has_experience_section"):
            score += 5.0

        # Job titles and companies (5 points)
        # Look for patterns like "Software Engineer at Company Name"
        job_patterns = [
            r"\b(?:Senior|Junior|Lead|Principal)?\s*(?:Software|Web|Frontend|Backend|Full.?Stack|DevOps|Data|Machine Learning|AI)\s*(?:Engineer|Developer|Architect|Scientist|Analyst)\b",
            r"\b(?:Manager|Director|VP|CTO|CEO|Founder|Co.?founder)\b",
        ]

        job_title_count = 0
        for pattern in job_patterns:
            job_title_count += len(re.findall(pattern, text, re.IGNORECASE))

        if job_title_count >= 3:
            score += 5.0
        elif job_title_count >= 2:
            score += 3.0
        elif job_title_count >= 1:
            score += 1.0

        # Employment dates (3 points)
        date_patterns = [
            r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}\b",
            r"\b\d{4}\s*[-–]\s*\d{4}\b",
            r"\b\d{4}\s*[-–]\s*(?:Present|Current)\b",
        ]

        date_count = 0
        for pattern in date_patterns:
            date_count += len(re.findall(pattern, text, re.IGNORECASE))

        if date_count >= 4:
            score += 3.0
        elif date_count >= 2:
            score += 2.0
        elif date_count >= 1:
            score += 1.0

        # Experience achievements (2 points)
        achievement_metrics = content_analysis.get("achievement_metrics", [])
        if len(achievement_metrics) >= 3:
            score += 2.0
        elif len(achievement_metrics) >= 1:
            score += 1.0

        return min(score, 15.0)

    def _score_compatibility(self, file_analysis: dict, parsed_content: dict) -> float:
        """Score overall ATS compatibility (5 points)"""
        score = 5.0  # Start with full points

        # File format compatibility
        if file_analysis.get("file_type") == "pdf":
            score -= 2.0
        # HTML format is fine if structure is simple - no automatic penalty

        # Parsing issues
        parsing_issues = file_analysis.get("parsing_issues", [])
        score -= len(parsing_issues) * 0.5

        # Format warnings
        format_warnings = file_analysis.get("format_warnings", [])
        score -= len(format_warnings) * 0.3

        # Emoji usage
        if any("emoji" in issue.lower() for issue in parsing_issues):
            score -= 1.0

        # Complex formatting
        html_structure = parsed_content.get("html_structure", {})
        if html_structure.get("has_tables") or html_structure.get("has_complex_divs"):
            score -= 1.0

        return max(score, 0.0)
