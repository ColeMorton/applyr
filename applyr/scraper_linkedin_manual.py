"""Manual LinkedIn job parser - processes text files instead of web scraping"""

import logging
from pathlib import Path
import re
from typing import Optional
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class LinkedInManualParser:
    """Parse LinkedIn job data from manually copied text files.

    This parser reads text files containing manually copied LinkedIn job page content
    (saved by user) instead of web scraping, avoiding 999 errors and ToS violations.
    """

    def __init__(self, raw_jobs_dir: Path = Path("data/raw/jobs/linked_in")):
        """Initialize the manual parser.

        Args:
            raw_jobs_dir: Directory where manual LinkedIn job text files are stored
        """
        self.raw_jobs_dir = Path(raw_jobs_dir)

    def extract_job_id(self, url_or_id: str) -> Optional[str]:
        """Extract job ID from LinkedIn URL or ID string.

        Args:
            url_or_id: Either a full LinkedIn URL or a numeric job ID

        Returns:
            Job ID in format 'li-{job_id}' or None if extraction fails
        """
        try:
            url_or_id = url_or_id.strip()

            # If it's already a numeric ID, add prefix
            if re.match(r"^\d+$", url_or_id):
                return f"li-{url_or_id}"

            # If it's a URL, extract job ID from path
            if url_or_id.startswith(("http://", "https://")):
                parsed = urlparse(url_or_id)
                # Match pattern: /jobs/view/{job_id}/
                match = re.search(r"/jobs/view/(\d+)/?", parsed.path)
                if match:
                    job_id = match.group(1)
                    return f"li-{job_id}"

            logger.error(f"Could not extract job ID from: {url_or_id}")
            return None
        except Exception as e:
            logger.error(f"Error extracting job ID from {url_or_id}: {e}")
            return None

    def get_raw_job_id(self, url_or_id: str) -> Optional[str]:
        """Get the raw job ID without 'li-' prefix for file lookup.

        Args:
            url_or_id: Either a full LinkedIn URL or a numeric job ID

        Returns:
            Raw job ID (numeric) or None
        """
        try:
            url_or_id = url_or_id.strip()

            # If it's a numeric ID, return as-is
            if re.match(r"^\d+$", url_or_id):
                return url_or_id

            # If it's a URL, extract job ID from path
            if url_or_id.startswith(("http://", "https://")):
                parsed = urlparse(url_or_id)
                match = re.search(r"/jobs/view/(\d+)/?", parsed.path)
                if match:
                    return match.group(1)

            return None
        except Exception as e:
            logger.error(f"Error getting raw job ID from {url_or_id}: {e}")
            return None

    def load_job_text(self, raw_job_id: str) -> Optional[str]:
        """Load manually saved job text file.

        Args:
            raw_job_id: Raw job ID (without 'li-' prefix)

        Returns:
            Text content of the job file or None if not found
        """
        try:
            text_file = self.raw_jobs_dir / f"{raw_job_id}.txt"

            if not text_file.exists():
                logger.warning(f"Text file not found: {text_file}")
                return None

            with open(text_file, encoding="utf-8") as f:
                content = f.read()

            if not content.strip():
                logger.warning(f"Text file is empty: {text_file}")
                return None

            return content
        except Exception as e:
            logger.error(f"Error reading text file for {raw_job_id}: {e}")
            return None

    def parse_job_data(self, text_content: str) -> dict[str, str]:
        """Parse job title, company, location, and description from copied text.

        Uses LinkedIn-specific heuristics to extract job information from plain text.

        Args:
            text_content: Raw text content from copied LinkedIn page

        Returns:
            Dictionary with 'title', 'company', 'location', and 'description' keys
        """
        lines = [line.strip() for line in text_content.split("\n") if line.strip()]

        metadata = {
            "title": "Unknown Job",
            "company": "Unknown Company",
            "location": "Unknown Location",
            "description": "",
        }

        try:
            # Job title is usually the first substantial line
            # Look for lines that aren't navigation/UI text
            skip_patterns = [
                r"^(skip to|sign in|employers|post job|linkedin|home|jobs)",
                r"^(menu|search|find jobs|saved|messages|profile|company reviews?)",
                r"^(cookie|privacy|terms|help|feedback)",
                r"^\d+\s*(reviews?|ratings?)",
                r"^(companies|apply now|save job|report job|apply|save|share)",
                r"^(follow|unfollow|message|connect)",
                r"^(show more|show less)",
            ]

            title_candidates = []
            for i, line in enumerate(lines[:20]):  # Check first 20 lines
                # Skip short lines and navigation
                if len(line) < 5 or any(re.match(pattern, line, re.IGNORECASE) for pattern in skip_patterns):
                    continue
                # Skip if it looks like a URL or email
                if "@" in line or line.startswith("http"):
                    continue
                # Skip if it's just a location or date
                if re.match(r"^[A-Z]{2,3}$", line):  # State codes
                    continue
                # Skip single words that are likely UI elements
                if len(line.split()) == 1 and len(line) < 15:
                    continue
                title_candidates.append((i, line))

            # First substantial line is usually the title
            if title_candidates:
                metadata["title"] = title_candidates[0][1]
                # Clean up common suffixes
                metadata["title"] = re.sub(r"\s*-\s*job\s*post\s*$", "", metadata["title"], flags=re.IGNORECASE)

            # Company name often appears near the title
            # Look for patterns like "Company Name" or "Company hiring Title"
            company_candidates = []
            for i, line in enumerate(lines[:20]):
                # Skip if it's likely the title we just found
                if line == metadata["title"]:
                    continue
                # Look for company indicators
                if " hiring " in line.lower():
                    # Extract company part before "hiring"
                    parts = line.split(" hiring ")
                    if len(parts) > 0:
                        company_candidates.append(parts[0].strip())
                elif "Pty" in line or "Ltd" in line or "Inc" in line or "LLC" in line:
                    company_candidates.append(line)
                # Check for standalone substantial lines after title
                elif len(line) > 3 and not any(re.match(pattern, line, re.IGNORECASE) for pattern in skip_patterns):
                    # Skip if it looks like a location
                    if not re.match(r"^[A-Z][a-z]+,\s*[A-Z][a-z]+", line):
                        company_candidates.append(line)

            if company_candidates:
                metadata["company"] = company_candidates[0]

            # Extract location: look for City, State/Country patterns
            location_candidates = []
            for i, line in enumerate(lines[:20]):
                # Look for location patterns
                if (
                    re.match(r"^[A-Z][a-z]+,\s*[A-Z][a-z]+", line)
                    or re.match(r"^[A-Z][a-z]+,\s*[A-Z][a-z]+,\s*[A-Z][a-z]+", line)
                    or re.match(r"^[A-Z][a-z]+\s+[A-Z][a-z]+$", line)
                    and len(line.split()) == 2
                ):  # City, State
                    location_candidates.append(line)

            if location_candidates:
                metadata["location"] = location_candidates[0]

            # Extract description: look for job-related keywords
            description_start = None
            job_keywords = [
                "about",
                "description",
                "role",
                "position",
                "responsibilities",
                "requirements",
                "qualifications",
                "skills",
                "experience",
                "what you",
                "we are looking",
                "seeking",
                "ideal candidate",
                "job description",
                "about the job",
                "about the role",
            ]

            for i, line in enumerate(lines):
                if any(keyword in line.lower() for keyword in job_keywords):
                    description_start = i
                    break

            if description_start is not None:
                # Take substantial content after the start
                description_lines = []
                for line in lines[description_start:]:
                    # Skip very short lines and navigation
                    if len(line) > 10 and not any(re.match(pattern, line, re.IGNORECASE) for pattern in skip_patterns):
                        description_lines.append(line)
                    # Stop if we hit footer-like content
                    if any(
                        keyword in line.lower()
                        for keyword in ["report job", "save job", "apply now", "linkedin may", "show more", "show less"]
                    ):
                        break

                metadata["description"] = "\n\n".join(description_lines)
            # Fallback: take middle portion of text as description
            elif len(lines) > 40:
                metadata["description"] = "\n\n".join(lines[20:-20])
            elif len(lines) > 10:
                metadata["description"] = "\n\n".join(lines[5:])
            else:
                metadata["description"] = "\n\n".join(lines)

            # Clean up description
            metadata["description"] = metadata["description"].strip()

        except Exception as e:
            logger.error(f"Error parsing job data: {e}")

        return metadata

    def process_job(self, url_or_id: str) -> Optional[dict[str, str]]:
        """Process a manual LinkedIn job from text file.

        Args:
            url_or_id: Either a full LinkedIn URL or a numeric job ID

        Returns:
            Dictionary with 'job_id', 'title', 'company', 'location', 'description' keys
            or None if processing fails
        """
        try:
            # Extract job IDs
            job_id = self.extract_job_id(url_or_id)
            raw_job_id = self.get_raw_job_id(url_or_id)

            if not job_id or not raw_job_id:
                logger.error(f"Could not extract job ID from: {url_or_id}")
                return None

            # Load text file
            text_content = self.load_job_text(raw_job_id)
            if not text_content:
                return None

            # Parse job data
            job_data = self.parse_job_data(text_content)
            job_data["job_id"] = job_id
            job_data["raw_job_id"] = raw_job_id

            return job_data
        except Exception as e:
            logger.error(f"Error processing job {url_or_id}: {e}")
            return None

    def get_source_name(self) -> str:
        """Return the name of the job board source."""
        return "LinkedIn (Manual Import)"
