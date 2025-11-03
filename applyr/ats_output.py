#!/usr/bin/env python3
"""Rich output formatter for ATS analysis results"""

from rich import box
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


class ATSOutputFormatter:
    """Rich console output formatter for ATS analysis"""

    def __init__(self, console: Console):
        self.console = console

    def display_results(self, result, detailed: bool = False):
        """Display ATS analysis results in rich format"""

        # Overall score header
        self._display_overall_score(result)

        # Category scores table
        self._display_category_scores(result)

        # Critical issues
        if result.critical_issues:
            self._display_critical_issues(result.critical_issues)

        # Recommendations
        if result.recommendations:
            self._display_recommendations(result.recommendations)

        # Detailed analysis
        if detailed:
            self._display_detailed_analysis(result)

    def _display_overall_score(self, result):
        """Display overall score with grade and color coding"""
        score = result.overall_score
        grade = result.grade

        # Color coding based on score
        if score >= 90:
            color = "green"
            emoji = "🎉"
            status = "Excellent"
        elif score >= 80:
            color = "blue"
            emoji = "✅"
            status = "Good"
        elif score >= 70:
            color = "yellow"
            emoji = "⚠️"
            status = "Fair"
        elif score >= 60:
            color = "orange3"
            emoji = "🔶"
            status = "Poor"
        else:
            color = "red"
            emoji = "❌"
            status = "Critical"

        # Create score panel
        score_text = Text(f"{score:.1f}/100", style=f"bold {color}")
        grade_text = Text(f"Grade: {grade}", style=color)
        status_text = Text(f"{emoji} {status}", style=color)

        panel_content = f"{score_text}\n{grade_text}\n{status_text}"

        self.console.print(
            Panel(panel_content, title="[bold]ATS Compatibility Score[/bold]", border_style=color, padding=(1, 2))
        )

    def _display_category_scores(self, result):
        """Display category breakdown table"""
        table = Table(title="📊 Category Breakdown", show_header=True, box=box.ROUNDED)
        table.add_column("Category", style="bold cyan", width=20)
        table.add_column("Score", justify="center", width=10)
        table.add_column("Grade", justify="center", width=8)
        table.add_column("Status", width=15)

        categories = [
            ("Contact Information", result.contact_info_score, 15),
            ("Keywords & Skills", result.keywords_score, 25),
            ("Format & Structure", result.format_score, 20),
            ("Content Quality", result.content_score, 20),
            ("Experience", result.experience_score, 15),
            ("ATS Compatibility", result.compatibility_score, 5),
        ]

        for category, score, max_score in categories:
            percentage = (score / max_score) * 100
            grade = self._get_grade(percentage)
            status = self._get_status(percentage)
            color = self._get_score_color(percentage)

            table.add_row(
                category,
                f"[{color}]{score:.1f}/{max_score}[/{color}]",
                f"[{color}]{grade}[/{color}]",
                f"[{color}]{status}[/{color}]",
            )

        self.console.print(table)

    def _display_critical_issues(self, issues: list[str]):
        """Display critical issues that block ATS parsing"""
        if not issues:
            return

        issue_text = "\n".join(f"• {issue}" for issue in issues)

        self.console.print(
            Panel(issue_text, title="[bold red]🚨 Critical Issues[/bold red]", border_style="red", padding=(1, 2))
        )

    def _display_recommendations(self, recommendations: list[str]):
        """Display actionable recommendations"""
        if not recommendations:
            return

        # Group recommendations by category
        contact_recs = [r for r in recommendations if any(word in r.lower() for word in ["contact", "email", "phone"])]
        format_recs = [
            r for r in recommendations if any(word in r.lower() for word in ["format", "structure", "html", "pdf"])
        ]
        keyword_recs = [r for r in recommendations if any(word in r.lower() for word in ["keyword", "skill"])]
        content_recs = [
            r for r in recommendations if any(word in r.lower() for word in ["content", "achievement", "verb"])
        ]
        other_recs = [
            r
            for r in recommendations
            if not any(r in " ".join(contact_recs + format_recs + keyword_recs + content_recs) for r in [r])
        ]

        # Create columns for different recommendation types
        columns = []

        if contact_recs:
            contact_text = "\n".join(f"• {rec}" for rec in contact_recs[:3])
            columns.append(Panel(contact_text, title="[bold blue]📞 Contact Info[/bold blue]", border_style="blue"))

        if format_recs:
            format_text = "\n".join(f"• {rec}" for rec in format_recs[:3])
            columns.append(Panel(format_text, title="[bold green]📄 Format[/bold green]", border_style="green"))

        if keyword_recs:
            keyword_text = "\n".join(f"• {rec}" for rec in keyword_recs[:3])
            columns.append(Panel(keyword_text, title="[bold yellow]🔑 Keywords[/bold yellow]", border_style="yellow"))

        if content_recs:
            content_text = "\n".join(f"• {rec}" for rec in content_recs[:3])
            columns.append(Panel(content_text, title="[bold magenta]📝 Content[/bold magenta]", border_style="magenta"))

        if other_recs:
            other_text = "\n".join(f"• {rec}" for rec in other_recs[:3])
            columns.append(Panel(other_text, title="[bold cyan]💡 Other[/bold cyan]", border_style="cyan"))

        if columns:
            self.console.print(
                Panel(
                    Columns(columns, equal=True, expand=True),
                    title="[bold]💡 Recommendations[/bold]",
                    border_style="blue",
                    padding=(1, 2),
                )
            )

    def _display_detailed_analysis(self, result):
        """Display detailed analysis information"""

        # Keyword analysis
        if result.keyword_analysis:
            self._display_keyword_analysis(result.keyword_analysis)

        # File analysis
        if result.file_analysis:
            self._display_file_analysis(result.file_analysis)

    def _display_keyword_analysis(self, keyword_analysis):
        """Display keyword analysis details"""
        table = Table(title="🔍 Keyword Analysis", show_header=True, box=box.ROUNDED)
        table.add_column("Metric", style="bold cyan")
        table.add_column("Value", style="green")
        table.add_column("Assessment", style="yellow")

        # Keyword density
        density = keyword_analysis.get("keyword_density", {})
        if density:
            avg_density = sum(density.values()) / len(density) if density else 0
            density_status = "Excellent" if avg_density >= 3 else "Good" if avg_density >= 2 else "Needs Improvement"
            table.add_row("Average Density", f"{avg_density:.1f}%", density_status)

        # Found keywords
        found_keywords = keyword_analysis.get("found_keywords", {})
        if found_keywords:
            tech_count = len(found_keywords.get("technical", []))
            soft_count = len(found_keywords.get("soft_skills", []))
            table.add_row("Technical Keywords", str(tech_count), "Good" if tech_count >= 5 else "Needs More")
            table.add_row("Soft Skills", str(soft_count), "Good" if soft_count >= 3 else "Needs More")

        # Job match
        job_match = keyword_analysis.get("job_match", {})
        if job_match:
            match_pct = job_match.get("match_percentage", 0)
            match_status = "Excellent" if match_pct >= 80 else "Good" if match_pct >= 60 else "Needs Improvement"
            table.add_row("Job Match", f"{match_pct:.1f}%", match_status)

        self.console.print(table)

    def _display_file_analysis(self, file_analysis):
        """Display file format analysis"""
        table = Table(title="📁 File Analysis", show_header=True, box=box.ROUNDED)
        table.add_column("Property", style="bold cyan")
        table.add_column("Value", style="green")
        table.add_column("Status", style="yellow")

        # File type
        file_type = file_analysis.get("file_type", "unknown")
        type_status = "Good" if file_type in [".txt", ".docx", ".html", "txt", "docx", "html"] else "Poor"
        table.add_row("File Type", file_type.upper(), type_status)

        # File size
        size_kb = file_analysis.get("file_size_kb", 0)
        size_status = "Good" if size_kb < 500 else "Large" if size_kb < 1000 else "Oversized"
        table.add_row("File Size", f"{size_kb:.1f} KB", size_status)

        # ATS compatibility
        compatible = file_analysis.get("ats_compatible", True)
        compat_status = "Compatible" if compatible else "Issues"
        table.add_row("ATS Compatible", "Yes" if compatible else "No", compat_status)

        # Parsing issues
        issues = file_analysis.get("parsing_issues", [])
        table.add_row("Parsing Issues", str(len(issues)), "None" if not issues else "Found")

        self.console.print(table)

    def _get_grade(self, percentage: float) -> str:
        """Convert percentage to letter grade"""
        if percentage >= 90:
            return "A"
        elif percentage >= 80:
            return "B"
        elif percentage >= 70:
            return "C"
        elif percentage >= 60:
            return "D"
        else:
            return "F"

    def _get_status(self, percentage: float) -> str:
        """Get status text based on percentage"""
        if percentage >= 90:
            return "Excellent"
        elif percentage >= 80:
            return "Good"
        elif percentage >= 70:
            return "Fair"
        elif percentage >= 60:
            return "Poor"
        else:
            return "Critical"

    def _get_score_color(self, percentage: float) -> str:
        """Get color based on percentage"""
        if percentage >= 90:
            return "green"
        elif percentage >= 80:
            return "blue"
        elif percentage >= 70:
            return "yellow"
        elif percentage >= 60:
            return "orange3"
        else:
            return "red"
