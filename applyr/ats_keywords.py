#!/usr/bin/env python3
"""Keyword analysis engine for ATS compatibility"""

from pathlib import Path
import re
from typing import Any, Optional

from rich.console import Console


class KeywordAnalyzer:
    """Keyword analysis engine for ATS optimization"""

    def __init__(self, console: Console):
        self.console = console
        self.tech_keywords = self._load_tech_keywords()
        self.soft_skills = self._load_soft_skills()
        self.industry_keywords = self._load_industry_keywords()

    def analyze_keywords(self, parsed_content: dict, job_description_path: Optional[Path] = None) -> dict[str, Any]:
        """
        Analyze keywords in document

        Args:
            parsed_content: Parsed document content
            job_description_path: Optional path to job description

        Returns:
            Keyword analysis results
        """
        text = parsed_content.get("raw_text", "").lower()

        # Extract keywords from document
        found_keywords = self._extract_keywords(text)

        # Analyze keyword density
        keyword_density = self._calculate_keyword_density(text, found_keywords)

        # Analyze keyword distribution
        keyword_distribution = self._analyze_keyword_distribution(text, found_keywords)

        # Job description matching
        job_match_analysis = {}
        if job_description_path:
            job_match_analysis = self._analyze_job_match(text, job_description_path)

        # Generate recommendations
        recommendations = self._generate_keyword_recommendations(found_keywords, keyword_density, job_match_analysis)

        return {
            "found_keywords": found_keywords,
            "keyword_density": keyword_density,
            "keyword_distribution": keyword_distribution,
            "job_match": job_match_analysis,
            "recommendations": recommendations,
            "missing_keywords": self._identify_missing_keywords(found_keywords, job_match_analysis),
        }

    def _extract_keywords(self, text: str) -> dict[str, list[str]]:
        """Extract keywords from text"""
        keywords = {"technical": [], "soft_skills": [], "industry": [], "tools": [], "frameworks": []}

        # Technical keywords - categorize by type
        for category, words in self.tech_keywords.items():
            for word in words:
                if re.search(r"\b" + re.escape(word.lower()) + r"\b", text):
                    if category == "programming_languages":
                        keywords["technical"].append(word)
                    elif category == "tools":
                        keywords["tools"].append(word)
                    elif category == "frameworks":
                        keywords["frameworks"].append(word)
                    else:
                        keywords["technical"].append(word)

        # Soft skills
        for skill in self.soft_skills:
            if re.search(r"\b" + re.escape(skill.lower()) + r"\b", text):
                keywords["soft_skills"].append(skill)

        # Industry keywords
        for _industry, words in self.industry_keywords.items():
            for word in words:
                if re.search(r"\b" + re.escape(word.lower()) + r"\b", text):
                    keywords["industry"].append(word)

        return keywords

    def _calculate_keyword_density(self, text: str, keywords: dict[str, list[str]]) -> dict[str, float]:
        """Calculate keyword density"""
        word_count = len(text.split())
        density = {}

        for category, words in keywords.items():
            if words:
                total_occurrences = sum(text.count(word.lower()) for word in words)
                density[category] = (total_occurrences / word_count) * 100 if word_count > 0 else 0
            else:
                density[category] = 0.0

        return density

    def _analyze_keyword_distribution(self, text: str, keywords: dict[str, list[str]]) -> dict[str, Any]:
        """Analyze how keywords are distributed across sections"""
        # Split text into sections (basic approach)
        sections = {
            "summary": text[: len(text) // 4],  # First quarter
            "experience": text[len(text) // 4 : 3 * len(text) // 4],  # Middle half
            "skills": text[3 * len(text) // 4 :],  # Last quarter
        }

        distribution = {}
        for section_name, section_text in sections.items():
            section_keywords = {}
            for category, words in keywords.items():
                section_keywords[category] = [
                    word for word in words if re.search(r"\b" + re.escape(word.lower()) + r"\b", section_text)
                ]
            distribution[section_name] = section_keywords

        return distribution

    def _analyze_job_match(self, text: str, job_description_path: Path) -> dict[str, Any]:
        """Analyze keyword match with job description"""
        try:
            with open(job_description_path, encoding="utf-8") as f:
                job_text = f.read().lower()
        except Exception as e:
            self.console.print(f"[yellow]⚠️  Could not read job description: {e}[/yellow]")
            return {}

        # Extract keywords from job description
        job_keywords = self._extract_keywords(job_text)

        # Calculate match percentage
        total_job_keywords = sum(len(words) for words in job_keywords.values())
        matched_keywords = 0

        for _category, words in job_keywords.items():
            for word in words:
                if re.search(r"\b" + re.escape(word.lower()) + r"\b", text):
                    matched_keywords += 1

        match_percentage = (matched_keywords / total_job_keywords * 100) if total_job_keywords > 0 else 0

        # Identify missing keywords
        missing_keywords = []
        for _category, words in job_keywords.items():
            for word in words:
                if not re.search(r"\b" + re.escape(word.lower()) + r"\b", text):
                    missing_keywords.append(word)

        return {
            "match_percentage": match_percentage,
            "matched_keywords": matched_keywords,
            "total_job_keywords": total_job_keywords,
            "missing_keywords": missing_keywords[:20],  # Limit to top 20
            "job_keywords": job_keywords,
        }

    def _generate_keyword_recommendations(
        self, found_keywords: dict, keyword_density: dict, job_match: dict
    ) -> list[str]:
        """Generate keyword-specific recommendations"""
        recommendations = []

        # Low keyword density
        for category, density in keyword_density.items():
            if density < 1.0 and found_keywords.get(category):
                recommendations.append(f"Increase {category} keyword density (current: {density:.1f}%)")

        # Missing critical keywords
        if job_match.get("missing_keywords"):
            missing = job_match["missing_keywords"][:5]
            recommendations.append(f"Add missing job-relevant keywords: {', '.join(missing)}")

        # Low job match
        if job_match.get("match_percentage", 0) < 60:
            recommendations.append(
                f"Improve job description match (current: {job_match.get('match_percentage', 0):.1f}%)"
            )

        # Missing technical skills
        if not found_keywords.get("technical"):
            recommendations.append("Add more technical keywords and programming languages")

        # Missing soft skills
        if not found_keywords.get("soft_skills"):
            recommendations.append("Include relevant soft skills (leadership, communication, etc.)")

        return recommendations

    def _identify_missing_keywords(self, found_keywords: dict, job_match: dict) -> list[str]:
        """Identify missing keywords"""
        missing = []

        # Add missing job-specific keywords
        if job_match.get("missing_keywords"):
            missing.extend(job_match["missing_keywords"][:10])

        # Add common missing technical keywords
        common_tech = ["JavaScript", "Python", "SQL", "Git", "Agile"]
        for tech in common_tech:
            if not any(tech.lower() in str(found_keywords).lower() for _ in [1]):
                missing.append(tech)

        return missing[:15]  # Limit to 15 missing keywords

    def _load_tech_keywords(self) -> dict[str, list[str]]:
        """Load technical keywords database"""
        return {
            "programming_languages": [
                "JavaScript",
                "Python",
                "Java",
                "C++",
                "C#",
                "TypeScript",
                "Go",
                "Rust",
                "PHP",
                "Ruby",
                "Swift",
                "Kotlin",
                "Scala",
                "R",
                "MATLAB",
                "Perl",
            ],
            "frameworks": [
                "React",
                "Angular",
                "Vue.js",
                "Node.js",
                "Express",
                "Django",
                "Flask",
                "Spring",
                "Laravel",
                "Rails",
                "ASP.NET",
                "jQuery",
                "Bootstrap",
                "Tailwind",
            ],
            "databases": [
                "MySQL",
                "PostgreSQL",
                "MongoDB",
                "Redis",
                "Oracle",
                "SQLite",
                "Cassandra",
                "Elasticsearch",
                "DynamoDB",
                "Neo4j",
                "InfluxDB",
            ],
            "cloud_platforms": [
                "AWS",
                "Azure",
                "Google Cloud",
                "Docker",
                "Kubernetes",
                "Terraform",
                "Jenkins",
                "GitLab CI",
                "GitHub Actions",
                "CircleCI",
            ],
            "tools": [
                "Git",
                "GitHub",
                "GitLab",
                "Bitbucket",
                "Jira",
                "Confluence",
                "Slack",
                "Trello",
                "Asana",
                "Figma",
                "Sketch",
                "Photoshop",
            ],
            "methodologies": [
                "Agile",
                "Scrum",
                "Kanban",
                "TDD",
                "BDD",
                "CI/CD",
                "DevOps",
                "Microservices",
                "REST",
                "GraphQL",
                "API",
                "MVC",
                "SOLID",
                "Clean Code",
            ],
        }

    def _load_soft_skills(self) -> list[str]:
        """Load soft skills database"""
        return [
            "Leadership",
            "Communication",
            "Teamwork",
            "Problem Solving",
            "Time Management",
            "Adaptability",
            "Creativity",
            "Critical Thinking",
            "Emotional Intelligence",
            "Negotiation",
            "Presentation",
            "Mentoring",
            "Collaboration",
            "Innovation",
            "Strategic Thinking",
            "Project Management",
            "Customer Service",
            "Analytical",
            "Detail Oriented",
            "Self Motivated",
            "Results Driven",
            "Cross Functional",
        ]

    def _load_industry_keywords(self) -> dict[str, list[str]]:
        """Load industry-specific keywords"""
        return {
            "fintech": [
                "Financial Services",
                "Banking",
                "Payments",
                "Blockchain",
                "Cryptocurrency",
                "Risk Management",
                "Compliance",
                "Regulatory",
                "Trading",
                "Investment",
            ],
            "healthcare": [
                "HIPAA",
                "Medical",
                "Healthcare",
                "Clinical",
                "Patient",
                "EMR",
                "EHR",
                "Healthcare IT",
                "Medical Devices",
                "Pharmaceutical",
            ],
            "ecommerce": [
                "E-commerce",
                "Online Retail",
                "Payment Processing",
                "Inventory Management",
                "Supply Chain",
                "Customer Experience",
                "Digital Marketing",
                "Analytics",
            ],
            "saas": [
                "SaaS",
                "Software as a Service",
                "Cloud Computing",
                "Subscription",
                "API Integration",
                "Scalability",
                "Multi-tenant",
                "User Experience",
            ],
            "ai_ml": [
                "Machine Learning",
                "Artificial Intelligence",
                "Data Science",
                "Deep Learning",
                "Neural Networks",
                "Natural Language Processing",
                "Computer Vision",
                "TensorFlow",
                "PyTorch",
                "Scikit-learn",
                "Pandas",
                "NumPy",
            ],
        }
