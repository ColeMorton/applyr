#!/usr/bin/env python3
"""
Job Description Aggregator

Aggregates all individual job description markdown files into a single
consolidated markdown file with date-based naming and unique titles.
"""

import argparse
from collections import Counter
from datetime import datetime
import logging
from pathlib import Path
import re
import sys
from typing import Optional

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class JobDescriptionAggregator:
    """Aggregates individual job description files into a single markdown file."""

    def __init__(self):
        """Initialize the aggregator."""
        self.jobs_data = []

    def discover_job_files(self, input_dir: Path) -> list[Path]:
        """
        Discover all job description markdown files in the input directory.

        Args:
            input_dir: Directory containing job description files

        Returns:
            List of Path objects for job description files
        """
        try:
            if not input_dir.exists():
                logger.error(f"Input directory does not exist: {input_dir}")
                return []

            # Find all .md files that match job description pattern (start with digits)
            job_files = []
            for file_path in input_dir.glob("*.md"):
                if re.match(r"^\d+_", file_path.name):  # Files starting with job ID
                    job_files.append(file_path)

            # Sort by filename for consistent ordering
            job_files.sort(key=lambda x: x.name)

            logger.info(f"Discovered {len(job_files)} job description files")
            return job_files

        except Exception as e:
            logger.error(f"Error discovering job files: {e}")
            return []

    def parse_job_file(self, file_path: Path) -> Optional[dict]:
        """
        Parse a single job description file and extract metadata and content.

        Args:
            file_path: Path to the job description file

        Returns:
            Dictionary with job data or None if parsing failed
        """
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            # Extract metadata using regex patterns
            job_data = {
                "file_path": file_path,
                "filename": file_path.name,
                "title": "Unknown Job",
                "company": "Unknown Company",
                "job_id": "Unknown",
                "source": "SEEK",
                "scraped_date": "Unknown",
                "content": content,
            }

            # Extract job ID from filename
            id_match = re.match(r"^(\d+)_", file_path.name)
            if id_match:
                job_data["job_id"] = id_match.group(1)

            # Extract title from first heading
            title_match = re.search(r"^# (.+)$", content, re.MULTILINE)
            if title_match:
                job_data["title"] = title_match.group(1).strip()

            # Extract company from metadata
            company_match = re.search(r"\*\*Company:\*\* (.+)$", content, re.MULTILINE)
            if company_match:
                job_data["company"] = company_match.group(1).strip()

            # Extract scraped date
            scraped_match = re.search(r"\*\*Scraped:\*\* (.+)$", content, re.MULTILINE)
            if scraped_match:
                job_data["scraped_date"] = scraped_match.group(1).strip()

            # Extract just the job description content (after the metadata section)
            content_match = re.search(r"^---\n\n(.+)", content, re.MULTILINE | re.DOTALL)
            if content_match:
                job_data["description"] = content_match.group(1).strip()
            else:
                job_data["description"] = content

            logger.debug(f"Parsed job: {job_data['title']} at {job_data['company']}")
            return job_data

        except Exception as e:
            logger.error(f"Error parsing job file {file_path}: {e}")
            return None

    def generate_unique_title(self, job_data: dict) -> str:
        """
        Generate a unique title for the job in the aggregated file.

        Args:
            job_data: Job data dictionary

        Returns:
            Unique title string
        """
        title = job_data["title"]
        company = job_data["company"]
        job_id = job_data["job_id"]

        return f"{title} at {company} (ID: {job_id})"

    def generate_anchor_link(self, title: str) -> str:
        """
        Generate a markdown anchor link from a title.

        Args:
            title: Title string

        Returns:
            Anchor link string
        """
        # Convert to lowercase, replace spaces with hyphens, remove special characters
        anchor = re.sub(r"[^\w\s-]", "", title.lower())
        anchor = re.sub(r"[\s_]+", "-", anchor)
        anchor = anchor.strip("-")
        return anchor

    def generate_summary_stats(self, jobs_data: list[dict]) -> dict:
        """
        Generate summary statistics for the job descriptions.

        Args:
            jobs_data: List of job data dictionaries

        Returns:
            Dictionary with summary statistics
        """
        if not jobs_data:
            return {}

        companies = [job["company"] for job in jobs_data]
        company_counts = Counter(companies)

        # Extract job types/levels from titles
        job_levels = []
        for job in jobs_data:
            title = job["title"].lower()
            if "senior" in title:
                job_levels.append("Senior")
            elif "junior" in title or "graduate" in title:
                job_levels.append("Junior")
            elif "lead" in title or "principal" in title:
                job_levels.append("Lead/Principal")
            else:
                job_levels.append("Mid-level")

        level_counts = Counter(job_levels)

        # Extract technologies from titles
        tech_keywords = ["typescript", "javascript", "react", "node", "aws", "python", "java", "php", "wordpress"]
        tech_mentions = Counter()

        for job in jobs_data:
            title_lower = job["title"].lower()
            description_lower = job["description"].lower() if "description" in job else ""
            combined_text = f"{title_lower} {description_lower}"

            for tech in tech_keywords:
                if tech in combined_text:
                    tech_mentions[tech.title()] += 1

        return {
            "total_jobs": len(jobs_data),
            "unique_companies": len(company_counts),
            "company_counts": dict(company_counts.most_common(5)),
            "job_level_distribution": dict(level_counts),
            "technology_mentions": dict(tech_mentions.most_common(10)),
        }

    def aggregate_jobs(self, input_dir: Path, output_file: Path) -> bool:
        """
        Aggregate all job descriptions into a single markdown file.

        Args:
            input_dir: Directory containing job description files
            output_file: Path for the output aggregated file

        Returns:
            True if successful, False otherwise
        """
        try:
            # Discover job files
            job_files = self.discover_job_files(input_dir)
            if not job_files:
                logger.error("No job description files found")
                return False

            # Parse all job files
            jobs_data = []
            failed_files = []

            for file_path in job_files:
                job_data = self.parse_job_file(file_path)
                if job_data:
                    jobs_data.append(job_data)
                else:
                    failed_files.append(file_path.name)

            if not jobs_data:
                logger.error("No job files could be parsed successfully")
                return False

            logger.info(f"Successfully parsed {len(jobs_data)} job descriptions")
            if failed_files:
                logger.warning(f"Failed to parse {len(failed_files)} files: {failed_files}")

            # Generate summary statistics
            stats = self.generate_summary_stats(jobs_data)

            # Generate aggregated markdown content
            current_date = datetime.now()
            date_str = current_date.strftime("%Y-%m-%d")

            markdown_content = []

            # Header
            markdown_content.extend(
                [
                    f"# Job Descriptions Aggregate - {date_str}",
                    "",
                    f"**Generated:** {current_date.strftime('%Y-%m-%d %H:%M:%S')}  ",
                    f"**Total Jobs:** {stats['total_jobs']}  ",
                    f"**Unique Companies:** {stats['unique_companies']}  ",
                    "**Source:** SEEK Job Scraper  ",
                    "",
                    "---",
                    "",
                ]
            )

            # Summary Statistics
            if stats:
                markdown_content.extend(
                    [
                        "## Summary Statistics",
                        "",
                        f"- **Total Job Postings:** {stats['total_jobs']}",
                        f"- **Unique Companies:** {stats['unique_companies']}",
                        "",
                    ]
                )

                # Job level distribution
                if stats["job_level_distribution"]:
                    markdown_content.append("### Job Level Distribution")
                    for level, count in stats["job_level_distribution"].items():
                        markdown_content.append(f"- **{level}:** {count}")
                    markdown_content.append("")

                # Top companies
                if stats["company_counts"]:
                    markdown_content.append("### Top Companies (by job count)")
                    for company, count in stats["company_counts"].items():
                        markdown_content.append(f"- **{company}:** {count} job{'s' if count > 1 else ''}")
                    markdown_content.append("")

                # Technology mentions
                if stats["technology_mentions"]:
                    markdown_content.append("### Technology Mentions")
                    for tech, count in stats["technology_mentions"].items():
                        markdown_content.append(f"- **{tech}:** {count} mention{'s' if count > 1 else ''}")
                    markdown_content.append("")

                markdown_content.extend(["---", ""])

            # Table of Contents
            markdown_content.extend(["## Table of Contents", ""])

            for i, job_data in enumerate(jobs_data, 1):
                unique_title = self.generate_unique_title(job_data)
                anchor = self.generate_anchor_link(unique_title)
                markdown_content.append(f"{i}. [{unique_title}](#{anchor})")

            markdown_content.extend(["", "---", ""])

            # Individual Job Descriptions
            markdown_content.append("## Job Descriptions")
            markdown_content.append("")

            for i, job_data in enumerate(jobs_data, 1):
                unique_title = self.generate_unique_title(job_data)
                anchor = self.generate_anchor_link(unique_title)

                markdown_content.extend(
                    [
                        f"### {i}. {unique_title} {{#{anchor}}}",
                        "",
                        f"**Company:** {job_data['company']}  ",
                        f"**Job ID:** {job_data['job_id']}  ",
                        f"**Source:** {job_data['source']}  ",
                        f"**Scraped:** {job_data['scraped_date']}  ",
                        f"**Original File:** `{job_data['filename']}`",
                        "",
                        "---",
                        "",
                        job_data["description"],
                        "",
                        "---",
                        "",
                    ]
                )

            # Footer
            markdown_content.extend(
                [
                    "",
                    f"*Aggregated from {len(jobs_data)} individual job description files*  ",
                    f"*Generated by Job Description Aggregator on {date_str}*",
                ]
            )

            # Write to file
            output_file.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, "w", encoding="utf-8") as f:
                f.write("\n".join(markdown_content))

            logger.info(f"Successfully aggregated {len(jobs_data)} job descriptions to: {output_file}")

            # Print summary
            print("\n✅ Aggregation Complete!")
            print("📁 Output file: {output_file}")
            print("📊 Jobs processed: {len(jobs_data)}")
            print("🏢 Unique companies: {stats['unique_companies']}")
            if failed_files:
                print("⚠️  Failed files: {len(failed_files)}")

            return True

        except Exception as e:
            logger.error(f"Error during aggregation: {e}")
            return False


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(description="Aggregate job description files into a single markdown file")

    parser.add_argument(
        "--input-dir",
        "-i",
        type=str,
        default="data/outputs/job_descriptions",
        help="Input directory containing job description files",
    )

    parser.add_argument("--output-file", "-o", type=str, help="Output file path (default: auto-generated with date)")

    parser.add_argument("--date", "-d", type=str, help="Date for filename in YYYYMMDD format (default: today)")

    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Setup paths
    input_dir = Path(args.input_dir)

    if args.output_file:
        output_file = Path(args.output_file)
    else:
        # Generate filename with date
        if args.date:
            try:
                date_obj = datetime.strptime(args.date, "%Y%m%d")
                date_str = args.date
            except ValueError:
                logger.error("Invalid date format. Use YYYYMMDD format.")
                sys.exit(1)
        else:
            date_obj = datetime.now()
            date_str = date_obj.strftime("%Y%m%d")

        output_filename = f"{date_str}_job_descriptions_aggregate.md"
        output_file = input_dir / output_filename

    # Initialize aggregator and run
    aggregator = JobDescriptionAggregator()

    logger.info(f"Input directory: {input_dir}")
    logger.info(f"Output file: {output_file}")

    success = aggregator.aggregate_jobs(input_dir, output_file)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
