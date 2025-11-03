"""Job scraper module for Employment Hero with Rich console integration"""

import logging
import re
from typing import Optional
from urllib.parse import urlparse

from bs4 import BeautifulSoup, Tag

from .database import ApplicationDatabase
from .scraper_base import JobScraper

logger = logging.getLogger(__name__)


class EmploymentHeroScraper(JobScraper):
    """Employment Hero job description scraper with anti-bot measures."""

    def __init__(self, delay_between_requests: float = 2.0, database: Optional[ApplicationDatabase] = None):
        super().__init__(delay_between_requests, database)

    def _setup_session(self) -> None:
        """Configure session with Employment Hero-specific headers."""
        super()._setup_session()
        self.session.headers.update(
            {
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
            }
        )

    def _get_request_headers(self, _url: str) -> dict[str, str]:
        """Get additional headers for Employment Hero requests."""
        return {"Referer": "https://jobs.employmenthero.com/"}

    def get_source_name(self) -> str:
        """Return the name of the job board source."""
        return "Employment Hero"

    def extract_job_id(self, url: str) -> Optional[str]:
        """Extract job ID from Employment Hero URL.

        Employment Hero URLs format: https://jobs.employmenthero.com/AU/job/{company-title-slug}
        Returns: 'eh-{slug}' format

        Args:
            url: Job posting URL

        Returns:
            Job ID in format 'eh-{slug}' or None if extraction fails
        """
        try:
            path = urlparse(url).path
            # Match pattern: /AU/job/{slug} or /job/{slug}
            match = re.search(r"/job/([a-zA-Z0-9\-]+)", path)
            if match:
                slug = match.group(1)
                return f"eh-{slug}"
            return None
        except Exception as e:
            logger.error(f"Error extracting job ID from {url}: {e}")
            return None

    def extract_job_metadata(self, soup: BeautifulSoup) -> dict[str, str]:
        """Extract job metadata (title, company) from the page.

        Args:
            soup: BeautifulSoup object of the job page

        Returns:
            Dictionary with 'title' and 'company' keys
        """
        metadata = {
            "title": "Unknown Job",
            "company": "Unknown Company",
        }

        try:
            # Try multiple selectors for job title
            title_selectors = [
                'h1[class*="job-title"]',
                'h1[class*="JobTitle"]',
                'h1[data-test="job-title"]',
                '[data-automation="job-title"]',
                "h1.title",
                "h1",
            ]

            for selector in title_selectors:
                title_elem = soup.select_one(selector)
                if title_elem:
                    metadata["title"] = title_elem.get_text(strip=True)
                    logger.debug(f"Found title with selector '{selector}': {metadata['title']}")
                    break

            # Try multiple selectors for company name
            company_selectors = [
                '[class*="company-name"]',
                '[class*="CompanyName"]',
                '[data-test="company-name"]',
                '[data-automation="company-name"]',
                ".company",
                "h2.company",
                'a[class*="company"]',
            ]

            for selector in company_selectors:
                company_elem = soup.select_one(selector)
                if company_elem:
                    metadata["company"] = company_elem.get_text(strip=True)
                    logger.debug(f"Found company with selector '{selector}': {metadata['company']}")
                    break

            # If still unknown, try to extract from meta tags
            if metadata["company"] == "Unknown Company":
                og_site = soup.find("meta", property="og:site_name")
                if og_site and isinstance(og_site, Tag) and og_site.get("content"):
                    metadata["company"] = str(og_site["content"])

        except Exception as e:
            logger.error(f"Error extracting metadata: {e}")

        return metadata

    def clean_job_description(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract and clean job description content.

        Args:
            soup: BeautifulSoup object of the job page

        Returns:
            Cleaned job description text or None if extraction fails
        """
        try:
            # Try multiple selectors for job description
            job_desc_selectors = [
                '[class*="job-description"]',
                '[class*="JobDescription"]',
                '[data-test="job-description"]',
                '[data-automation="job-description"]',
                ".description",
                '[class*="job-details"]',
                '[class*="JobDetails"]',
                'section[class*="description"]',
                'div[class*="description"]',
            ]

            job_desc_elem = None
            for selector in job_desc_selectors:
                job_desc_elem = soup.select_one(selector)
                if job_desc_elem:
                    logger.debug(f"Found description with selector '{selector}'")
                    break

            # Fallback: look for content-rich sections
            if not job_desc_elem:
                sections = soup.find_all(["section", "div", "article"])
                for section in sections:
                    text = section.get_text(strip=True)
                    # Look for sections with substantial content and job-related keywords
                    if len(text) > 200 and any(
                        keyword in text.lower()
                        for keyword in [
                            "responsibilities",
                            "requirements",
                            "experience",
                            "role",
                            "position",
                            "about",
                            "skills",
                        ]
                    ):
                        job_desc_elem = section
                        logger.debug("Found description via fallback method")
                        break

            if not job_desc_elem:
                logger.error("Could not find job description content")
                return None

            # Remove unwanted sections
            unwanted_selectors = [
                '[class*="company-profile"]',
                '[class*="advertiser-profile"]',
                '[class*="similar-jobs"]',
                '[class*="recommended"]',
                "nav",
                "footer",
                ".advertisement",
                ".ad",
                '[class*="header"]',
                '[class*="navigation"]',
            ]

            for selector in unwanted_selectors:
                for elem in job_desc_elem.select(selector):
                    elem.decompose()

            # Extract text content
            text_content = job_desc_elem.get_text(separator="\n", strip=True)
            lines = [line.strip() for line in text_content.split("\n") if line.strip()]

            # Remove consecutive duplicate lines
            cleaned_lines = []
            prev_line = ""
            for line in lines:
                if line != prev_line:
                    cleaned_lines.append(line)
                    prev_line = line

            return "\n\n".join(cleaned_lines)
        except Exception as e:
            logger.error(f"Error cleaning job description: {e}")
            return None
