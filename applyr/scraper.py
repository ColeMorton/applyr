"""Job scraper module for SEEK with Rich console integration"""

import logging
from pathlib import Path
import re
from typing import Optional
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from .database import ApplicationDatabase
from .scraper_base import JobScraper

logger = logging.getLogger(__name__)


class SEEKScraper(JobScraper):
    """SEEK job description scraper with anti-bot measures."""

    def __init__(self, delay_between_requests: float = 2.0, database: Optional[ApplicationDatabase] = None):
        super().__init__(delay_between_requests, database)

    def _setup_session(self) -> None:
        """Configure session with SEEK-specific headers."""
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
        """Get additional headers for SEEK requests."""
        return {"Referer": "https://www.seek.com.au/"}

    def get_source_name(self) -> str:
        """Return the name of the job board source."""
        return "SEEK"

    def extract_job_id(self, url: str) -> Optional[str]:
        """Extract job ID from SEEK URL."""
        try:
            path = urlparse(url).path
            match = re.search(r"/job/(\d+)", path)
            return match.group(1) if match else None
        except (AttributeError, ValueError, TypeError, re.error) as e:
            logger.error(f"Error extracting job ID from {url}: {e}")
            return None

    def extract_job_metadata(self, soup: BeautifulSoup) -> dict[str, str]:
        """Extract job metadata (title, company) from the page."""
        metadata = {
            "title": "Unknown Job",
            "company": "Unknown Company",
        }

        try:
            title_selectors = [
                'h1[data-automation="job-detail-title"]',
                "h1.jobtitle",
                "h1",
                '[data-automation="job-detail-title"]',
            ]

            for selector in title_selectors:
                title_elem = soup.select_one(selector)
                if title_elem:
                    metadata["title"] = title_elem.get_text(strip=True)
                    break

            company_selectors = [
                '[data-automation="advertiser-name"]',
                ".advertiser-name",
                '[data-automation="job-company"]',
                ".company-name",
            ]

            for selector in company_selectors:
                company_elem = soup.select_one(selector)
                if company_elem:
                    metadata["company"] = company_elem.get_text(strip=True)
                    break
        except Exception as e:
            logger.error(f"Error extracting metadata: {e}")

        return metadata

    def clean_job_description(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract and clean job description content, excluding unwanted sections."""
        try:
            job_desc_selectors = [
                '[data-automation="jobAdDetails"]',
                ".jobAdDetails",
                '[data-automation="job-detail-description"]',
                ".job-description",
                ".jobDescription",
                ".adDetails",
            ]

            job_desc_elem = None
            for selector in job_desc_selectors:
                job_desc_elem = soup.select_one(selector)
                if job_desc_elem:
                    break

            if not job_desc_elem:
                content_areas = soup.find_all(
                    ["div", "section"],
                    string=lambda text: text
                    and any(
                        keyword in text.lower()
                        for keyword in ["responsibilities", "requirements", "experience", "role", "position"]
                    ),
                )
                if content_areas:
                    job_desc_elem = content_areas[0].parent

            if not job_desc_elem:
                logger.error("Could not find job description content")
                return None

            unwanted_selectors = [
                '[data-automation="company-profile"]',
                ".company-profile",
                ".advertiser-profile",
                ".safety-warning",
                '[data-automation="safety-warning"]',
                '*:contains("Be Careful")',
                '*:contains("What can I earn")',
                ".navigation",
                ".nav",
                "nav",
                ".advertisement",
                ".ad",
                '[data-automation="jobsearch-JobseekerHeaderLinks"]',
                "footer",
                ".footer",
                ".page-footer",
            ]

            for selector in unwanted_selectors:
                for elem in job_desc_elem.select(selector):
                    elem.decompose()

            warning_texts = ["be careful", "what can i earn", "company profile", "scam", "fraud"]
            for elem in job_desc_elem.find_all(text=True):
                if any(warning in elem.lower() for warning in warning_texts):
                    parent = elem.parent
                    if parent:
                        parent.decompose()

            text_content = job_desc_elem.get_text(separator="\n", strip=True)
            lines = [line.strip() for line in text_content.split("\n") if line.strip()]

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


def scrape_jobs(
    urls: list[str], output_dir: Path, delay: float, console: Console, database: Optional[ApplicationDatabase] = None
) -> dict[str, bool]:
    """Scrape multiple jobs with Rich progress tracking.

    Automatically detects job board source and uses appropriate scraper.
    Supports SEEK and Employment Hero job boards.

    Args:
        urls: List of job URLs (can be mixed sources)
        output_dir: Directory to save job descriptions
        delay: Delay between requests in seconds
        console: Rich console for output
        database: Optional ApplicationDatabase for tracking

    Returns:
        Dictionary mapping URLs to success status
    """
    from .scraper_factory import create_scraper

    results = {}

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        task = progress.add_task(f"Scraping {len(urls)} jobs...", total=len(urls))

        for url in urls:
            progress.update(task, description=f"Processing {url[:50]}...")
            try:
                # Create appropriate scraper for this URL
                scraper, normalized_url = create_scraper(url, delay=delay, database=database)
                results[url] = scraper.scrape_job(normalized_url, output_dir, console)
                progress.advance(task)
            except ValueError as e:
                console.print(f"[red]❌ Unsupported job board for {url}: {e}[/red]")
                results[url] = False
                progress.advance(task)
            except Exception as e:
                console.print(f"[red]❌ Error processing {url}: {e}[/red]")
                results[url] = False
                progress.advance(task)

    return results
