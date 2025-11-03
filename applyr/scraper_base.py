"""Abstract base class for job board scrapers"""

from abc import ABC, abstractmethod
import logging
from pathlib import Path
import re
import time
from typing import Dict, Optional, Set

from bs4 import BeautifulSoup
import requests
from rich.console import Console

from .database import ApplicationDatabase, JobStatus, Priority

logger = logging.getLogger(__name__)

# Global set to track which sources have shown ToS warnings
_TOS_WARNINGS_SHOWN: Set[str] = set()


class JobScraper(ABC):
    """Abstract base class for job board scrapers with common functionality."""

    def __init__(self, delay_between_requests: float = 2.0, database: Optional[ApplicationDatabase] = None):
        """Initialize scraper with delay and optional database.

        Args:
            delay_between_requests: Seconds to wait between requests
            database: Optional ApplicationDatabase instance for tracking jobs
        """
        self.delay = delay_between_requests
        self.database = database
        self.session = requests.Session()
        self._setup_session()
        self._show_tos_warning_if_needed()

    def _setup_session(self) -> None:
        """Configure session with headers. Override in subclass for custom headers."""
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "en-AU,en;q=0.9,en-US;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Cache-Control": "max-age=0",
            }
        )

    def _show_tos_warning_if_needed(self) -> None:
        """Display Terms of Service warning for this scraper source (once per session).

        Shows a warning about web scraping restrictions and responsible use.
        Only displays once per source per session to avoid spam.
        """
        source_name = self.get_source_name()

        # Check if we've already shown warning for this source
        if source_name in _TOS_WARNINGS_SHOWN:
            return

        # Mark as shown
        _TOS_WARNINGS_SHOWN.add(source_name)

        # Display warning (will only appear once per source per run)
        logger.warning(f"⚠️  {source_name} Scraping Notice: Web scraping may violate Terms of Service.")
        logger.warning("   This tool is for personal use only with respectful rate limiting.")
        logger.warning("   For commercial use, please use official APIs where available.")
        logger.warning("   See docs/TERMS_OF_SERVICE.md for detailed information.")

    @abstractmethod
    def extract_job_id(self, url: str) -> Optional[str]:
        """Extract job ID from URL.

        Args:
            url: Job posting URL

        Returns:
            Job ID string or None if extraction fails
        """

    @abstractmethod
    def extract_job_metadata(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract job metadata (title, company) from parsed HTML.

        Args:
            soup: BeautifulSoup object of the job page

        Returns:
            Dictionary with 'title' and 'company' keys
        """

    @abstractmethod
    def clean_job_description(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract and clean job description content.

        Args:
            soup: BeautifulSoup object of the job page

        Returns:
            Cleaned job description text or None if extraction fails
        """

    @abstractmethod
    def get_source_name(self) -> str:
        """Return the name of the job board source.

        Returns:
            Source name (e.g., "SEEK", "Employment Hero")
        """

    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch a webpage and return BeautifulSoup object.

        Args:
            url: URL to fetch

        Returns:
            BeautifulSoup object or None if fetch fails
        """
        try:
            headers = self._get_request_headers(url)
            response = self.session.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            return soup
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                logger.error(f"Access forbidden (403) for {url}. Site may be blocking the request.")
            else:
                logger.error(f"HTTP error {e.response.status_code} for {url}: {e}")
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
        return None

    def _get_request_headers(self, url: str) -> Dict[str, str]:
        """Get additional headers for request. Override in subclass if needed.

        Args:
            url: URL being requested

        Returns:
            Dictionary of additional headers
        """
        return {}

    def sanitize_filename(self, text: str, max_length: int = 100) -> str:
        """Sanitize text for use as filename.

        Args:
            text: Text to sanitize
            max_length: Maximum length of resulting filename

        Returns:
            Sanitized filename string
        """
        text = re.sub(r'[<>:"/\\|?*]', "_", text)
        text = re.sub(r"[^\w\s\-_]", "", text)
        text = re.sub(r"[-\s]+", "_", text)
        text = text.strip("_")

        if len(text) > max_length:
            text = text[:max_length].rstrip("_")

        return text

    def save_job_description(self, job_id: str, metadata: Dict[str, str], description: str, output_dir: Path) -> bool:
        """Save job description to markdown file.

        Args:
            job_id: Job identifier
            metadata: Dictionary with 'title' and 'company' keys
            description: Job description content
            output_dir: Directory to save the file

        Returns:
            True if save successful, False otherwise
        """
        try:
            output_dir.mkdir(parents=True, exist_ok=True)

            company = self.sanitize_filename(metadata["company"])
            title = self.sanitize_filename(metadata["title"])
            filename = f"{job_id}_{company}_{title}.md"

            filepath = output_dir / filename

            markdown_content = f"""# {metadata['title']}

**Company:** {metadata['company']}
**Job ID:** {job_id}
**Source:** {self.get_source_name()}
**Scraped:** {time.strftime('%Y-%m-%d %H:%M:%S')}

---

{description}
"""

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(markdown_content)

            return True
        except Exception as e:
            logger.error(f"Error saving job description: {e}")
            return False

    def scrape_job(self, url: str, output_dir: Path, console: Optional[Console] = None) -> bool:
        """Scrape a single job posting with Rich console output.

        Args:
            url: Job posting URL
            output_dir: Directory to save the job description
            console: Optional Rich console for output

        Returns:
            True if scraping successful, False otherwise
        """
        job_id = self.extract_job_id(url)
        if not job_id:
            if console:
                console.print(f"[red]❌ Could not extract job ID from: {url}[/red]")
            return False

        soup = self.fetch_page(url)
        if not soup:
            if console:
                console.print(f"[red]❌ Failed to fetch: {url}[/red]")
            return False

        metadata = self.extract_job_metadata(soup)
        if console:
            console.print(f"[green]📄 Found: {metadata['title']} at {metadata['company']}[/green]")

        description = self.clean_job_description(soup)
        if not description:
            if console:
                console.print(f"[red]❌ No description extracted from: {url}[/red]")
            return False

        success = self.save_job_description(job_id, metadata, description, output_dir)
        if success and console:
            console.print(f"[green]✅ Saved job {job_id}[/green]")

        # Add job to database if available
        if success and self.database:
            self.database.add_job(
                job_id=job_id,
                company_name=metadata["company"],
                job_title=metadata["title"],
                source=self.get_source_name(),
                url=url,
                status=JobStatus.DISCOVERED,
                priority=Priority.MEDIUM,
            )

        time.sleep(self.delay)
        return success
