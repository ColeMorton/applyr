#!/usr/bin/env python3
"""ATS Analyzer - Comprehensive resume and cover letter analysis engine"""

import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from rich.console import Console

from .ats_parsers import DocumentParser
from .ats_keywords import KeywordAnalyzer
from .ats_scoring import ScoringEngine


@dataclass
class ATSAnalysisResult:
    """Comprehensive ATS analysis results"""
    overall_score: float
    grade: str
    contact_info_score: float
    keywords_score: float
    format_score: float
    content_score: float
    experience_score: float
    compatibility_score: float
    critical_issues: List[str]
    recommendations: List[str]
    keyword_analysis: Dict[str, Any]
    parsed_content: Dict[str, Any]
    file_analysis: Dict[str, Any]


class ATSAnalyzer:
    """Main ATS analysis engine"""
    
    def __init__(self, console: Console):
        self.console = console
        self.parser = DocumentParser(console)
        self.keyword_analyzer = KeywordAnalyzer(console)
        self.scoring_engine = ScoringEngine(console)
    
    def analyze_document(self, file_path: Path, job_description: Optional[Path] = None) -> ATSAnalysisResult:
        """
        Perform comprehensive ATS analysis on a document
        
        Args:
            file_path: Path to resume/cover letter
            job_description: Optional path to job description for keyword matching
            
        Returns:
            ATSAnalysisResult with comprehensive analysis
        """
        self.console.print(f"[bold blue]🔍 Analyzing document: {file_path.name}[/bold blue]")
        
        # Parse document content
        parsed_content = self.parser.parse_document(file_path)
        if not parsed_content:
            raise ValueError(f"Failed to parse document: {file_path}")
        
        # Analyze file format and structure
        file_analysis = self._analyze_file_format(file_path, parsed_content)
        
        # Extract and analyze content sections
        content_analysis = self._analyze_content_sections(parsed_content)
        
        # Perform keyword analysis
        keyword_analysis = self.keyword_analyzer.analyze_keywords(
            parsed_content, 
            job_description
        )
        
        # Calculate scores for each category
        scores = self.scoring_engine.calculate_scores(
            parsed_content,
            content_analysis,
            keyword_analysis,
            file_analysis
        )
        
        # Identify critical issues
        critical_issues = self._identify_critical_issues(
            parsed_content, 
            content_analysis, 
            file_analysis
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            scores, 
            critical_issues, 
            keyword_analysis,
            content_analysis
        )
        
        # Calculate overall score and grade
        overall_score = self._calculate_overall_score(scores)
        grade = self._calculate_grade(overall_score)
        
        return ATSAnalysisResult(
            overall_score=overall_score,
            grade=grade,
            contact_info_score=scores['contact_info'],
            keywords_score=scores['keywords'],
            format_score=scores['format'],
            content_score=scores['content'],
            experience_score=scores['experience'],
            compatibility_score=scores['compatibility'],
            critical_issues=critical_issues,
            recommendations=recommendations,
            keyword_analysis=keyword_analysis,
            parsed_content=parsed_content,
            file_analysis=file_analysis
        )
    
    def _analyze_file_format(self, file_path: Path, parsed_content: Dict) -> Dict[str, Any]:
        """Analyze file format and ATS compatibility"""
        analysis = {
            'file_type': file_path.suffix.lower(),
            'file_size_kb': file_path.stat().st_size / 1024,
            'ats_compatible': True,
            'parsing_issues': [],
            'format_warnings': []
        }
        
        # Check file format compatibility
        if file_path.suffix.lower() == '.pdf':
            analysis['ats_compatible'] = False
            analysis['parsing_issues'].append("PDF format may cause ATS parsing issues")
            analysis['format_warnings'].append("Consider using .docx format for better ATS compatibility")
        elif file_path.suffix.lower() in ['.html', '.htm']:
            if self._has_complex_html(parsed_content.get('raw_text', '')):
                analysis['format_warnings'].append("Complex HTML structure may confuse ATS systems")
        
        # Check for emoji usage
        if self._has_emojis(parsed_content.get('raw_text', '')):
            analysis['parsing_issues'].append("Emoji usage detected - may break ATS parsing")
            analysis['ats_compatible'] = False
        
        # Check file size
        if analysis['file_size_kb'] > 500:
            analysis['format_warnings'].append("Large file size may slow ATS processing")
        
        return analysis
    
    def _analyze_content_sections(self, parsed_content: Dict) -> Dict[str, Any]:
        """Analyze content sections and structure"""
        analysis = {
            'has_contact_info': False,
            'has_skills_section': False,
            'has_experience_section': False,
            'has_education_section': False,
            'section_headers': [],
            'content_quality': 'unknown',
            'achievement_metrics': []
        }
        
        text = parsed_content.get('raw_text', '').lower()
        
        # Check for standard sections
        section_patterns = {
            'contact_info': [r'email', r'phone', r'@', r'linkedin'],
            'skills_section': [r'skills?', r'technologies?', r'competencies?'],
            'experience_section': [r'experience', r'employment', r'work history', r'professional'],
            'education_section': [r'education', r'degree', r'university', r'college']
        }
        
        for section, patterns in section_patterns.items():
            if any(re.search(pattern, text) for pattern in patterns):
                analysis[f'has_{section}'] = True
        
        # Extract section headers
        headers = re.findall(r'<h[1-6][^>]*>(.*?)</h[1-6]>', parsed_content.get('raw_text', ''), re.IGNORECASE)
        analysis['section_headers'] = [h.strip() for h in headers]
        
        # Analyze content quality
        analysis['content_quality'] = self._assess_content_quality(parsed_content)
        
        # Extract quantified achievements
        analysis['achievement_metrics'] = self._extract_achievement_metrics(parsed_content.get('raw_text', ''))
        
        return analysis
    
    def _identify_critical_issues(self, parsed_content: Dict, content_analysis: Dict, file_analysis: Dict) -> List[str]:
        """Identify critical issues that would block ATS parsing"""
        issues = []
        
        # Check for missing contact information
        if not content_analysis['has_contact_info']:
            issues.append("Missing or unparseable contact information")
        
        # Check for emoji usage
        if file_analysis.get('parsing_issues'):
            issues.extend(file_analysis['parsing_issues'])
        
        # Check for missing critical sections
        if not content_analysis['has_experience_section']:
            issues.append("Missing or unclear experience section")
        
        # Check for complex formatting
        if self._has_complex_formatting(parsed_content.get('raw_text', '')):
            issues.append("Complex formatting may confuse ATS systems")
        
        # Check for missing skills
        if not content_analysis['has_skills_section']:
            issues.append("Missing dedicated skills section")
        
        return issues
    
    def _generate_recommendations(self, scores: Dict, critical_issues: List[str], 
                                keyword_analysis: Dict, content_analysis: Dict) -> List[str]:
        """Generate specific, actionable recommendations"""
        recommendations = []
        
        # Contact information recommendations
        if scores['contact_info'] < 80:
            recommendations.append("Ensure contact information is clearly formatted without emojis")
            recommendations.append("Use standard format: Name, Phone, Email, Location")
        
        # Keyword recommendations
        if scores['keywords'] < 70:
            missing_keywords = keyword_analysis.get('missing_keywords', [])
            if missing_keywords:
                recommendations.append(f"Add missing keywords: {', '.join(missing_keywords[:5])}")
            recommendations.append("Increase keyword density in skills and experience sections")
        
        # Format recommendations
        if scores['format'] < 75:
            recommendations.append("Use standard section headers: 'Experience', 'Skills', 'Education'")
            recommendations.append("Avoid complex HTML structures and tables")
            recommendations.append("Use simple bullet points for achievements")
        
        # Content recommendations
        if scores['content'] < 70:
            recommendations.append("Add quantified achievements with specific metrics")
            recommendations.append("Use action verbs to start bullet points")
            recommendations.append("Ensure consistent formatting throughout")
        
        # Experience recommendations
        if scores['experience'] < 75:
            recommendations.append("Include clear job titles and company names")
            recommendations.append("Add employment dates in standard format")
            recommendations.append("Focus on relevant achievements for target roles")
        
        # Critical issue recommendations
        for issue in critical_issues:
            if "emoji" in issue.lower():
                recommendations.append("Remove all emojis from contact information and content")
            elif "format" in issue.lower():
                recommendations.append("Convert to .docx format for better ATS compatibility")
            elif "contact" in issue.lower():
                recommendations.append("Ensure contact information is in main document body, not headers/footers")
        
        return recommendations
    
    def _calculate_overall_score(self, scores: Dict) -> float:
        """Calculate overall score as sum of category scores"""
        # Scores are already out of their maximum values:
        # contact_info: out of 15, keywords: out of 25, format: out of 20
        # content: out of 20, experience: out of 15, compatibility: out of 5
        # Total possible: 100 points
        return sum(scores.values())
    
    def _calculate_grade(self, score: float) -> str:
        """Convert score to letter grade"""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"
    
    def _has_emojis(self, text: str) -> bool:
        """Check if text contains emojis"""
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE)
        return bool(emoji_pattern.search(text))
    
    def _has_complex_html(self, text: str) -> bool:
        """Check for complex HTML structures that may confuse ATS"""
        complex_patterns = [
            r'<table[^>]*>',  # Tables
            r'<div[^>]*class="[^"]*grid[^"]*"',  # CSS Grid
            r'<span[^>]*class="[^"]*skill-tag[^"]*"',  # Complex spans
            r'<div[^>]*class="[^"]*skills-grid[^"]*"',  # Complex divs
        ]
        return any(re.search(pattern, text, re.IGNORECASE) for pattern in complex_patterns)
    
    def _has_complex_formatting(self, text: str) -> bool:
        """Check for complex formatting elements"""
        complex_elements = [
            r'<table',  # Tables
            r'<div[^>]*class="[^"]*grid',  # CSS Grid
            r'<span[^>]*class="[^"]*tag',  # Tag elements
            r'<div[^>]*class="[^"]*skill',  # Skill containers
        ]
        return any(re.search(pattern, text, re.IGNORECASE) for pattern in complex_elements)
    
    def _assess_content_quality(self, parsed_content: Dict) -> str:
        """Assess overall content quality"""
        text = parsed_content.get('raw_text', '')
        
        # Check for quantified achievements
        metrics = re.findall(r'\b\d+%|\b\d+\+|\$\d+|\d+x\b', text)
        
        # Check for action verbs
        action_verbs = ['developed', 'created', 'implemented', 'managed', 'led', 'increased', 'improved']
        has_action_verbs = any(verb in text.lower() for verb in action_verbs)
        
        if len(metrics) >= 3 and has_action_verbs:
            return 'excellent'
        elif len(metrics) >= 1 and has_action_verbs:
            return 'good'
        else:
            return 'needs_improvement'
    
    def _extract_achievement_metrics(self, text: str) -> List[str]:
        """Extract quantified achievements from text"""
        metrics = re.findall(r'\b\d+%|\b\d+\+|\$\d+|\d+x\b|\d+\s*(years?|months?)', text)
        return metrics[:10]  # Limit to first 10 metrics
