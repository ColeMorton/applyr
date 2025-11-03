#!/usr/bin/env python3
"""
SEEK Job Description Scraper

A reusable web scraper to extract job descriptions from SEEK URLs
and save them as markdown files, excluding unwanted sections.
"""

import logging
from pathlib import Path
import re
import sys
import time
from typing import Optional
from urllib.parse import urlparse

from bs4 import BeautifulSoup
import requests

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class SEEKScraper:
    """SEEK job description scraper with anti-bot measures."""

    def __init__(self, delay_between_requests: float = 2.0):
        """
        Initialize the scraper with configurable settings.

        Args:
            delay_between_requests: Delay in seconds between requests (respectful scraping)
        """
        self.delay = delay_between_requests
        self.session = requests.Session()

        # Setup headers to mimic a real browser
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Language": "en-AU,en;q=0.9,en-US;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Cache-Control": "max-age=0",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
            }
        )

    def extract_job_id(self, url: str) -> Optional[str]:
        """Extract job ID from SEEK URL."""
        try:
            # SEEK URLs format: https://www.seek.com.au/job/86524100
            path = urlparse(url).path
            match = re.search(r"/job/(\d+)", path)
            return match.group(1) if match else None
        except Exception as e:
            logger.error(f"Error extracting job ID from {url}: {e}")
            return None

    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Fetch a webpage and return BeautifulSoup object.

        Args:
            url: The URL to fetch

        Returns:
            BeautifulSoup object or None if failed
        """
        try:
            logger.info(f"Fetching: {url}")

            # Add referer header for this request
            headers = {"Referer": "https://www.seek.com.au/"}

            response = self.session.get(url, headers=headers, timeout=30)
            response.raise_for_status()

            # Parse HTML
            soup = BeautifulSoup(response.content, "html.parser")
            return soup

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                logger.error(f"Access forbidden (403) for {url}. SEEK may be blocking the request.")
            else:
                logger.error(f"HTTP error {e.response.status_code} for {url}: {e}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed for {url}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error fetching {url}: {e}")

        return None

    def extract_job_metadata(self, soup: BeautifulSoup) -> dict[str, str]:
        """
        Extract job metadata (title, company) from the page.

        Args:
            soup: BeautifulSoup object of the page

        Returns:
            Dictionary with job metadata
        """
        metadata = {
            "title": "Unknown Job",
            "company": "Unknown Company",
        }

        try:
            # Try to find job title
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

            # Try to find company name
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
        """
        Extract and clean job description content, excluding unwanted sections.

        Args:
            soup: BeautifulSoup object of the page

        Returns:
            Cleaned job description text or None if extraction failed
        """
        try:
            # Common job description selectors for SEEK
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
                # Fallback: try to find the main content area
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

            # Remove unwanted sections
            unwanted_selectors = [
                # Company profile sections
                '[data-automation="company-profile"]',
                ".company-profile",
                ".advertiser-profile",
                # Warning/safety sections
                ".safety-warning",
                '[data-automation="safety-warning"]',
                '*:contains("Be Careful")',
                '*:contains("What can I earn")',
                # Navigation and ads
                ".navigation",
                ".nav",
                "nav",
                ".advertisement",
                ".ad",
                '[data-automation="jobsearch-JobseekerHeaderLinks"]',
                # Footer content
                "footer",
                ".footer",
                ".page-footer",
            ]

            for selector in unwanted_selectors:
                for elem in job_desc_elem.select(selector):
                    elem.decompose()

            # Also remove elements that contain specific warning text
            warning_texts = ["be careful", "what can i earn", "company profile", "scam", "fraud"]
            for elem in job_desc_elem.find_all(text=True):
                if any(warning in elem.lower() for warning in warning_texts):
                    parent = elem.parent
                    if parent:
                        parent.decompose()

            # Extract text content
            text_content = job_desc_elem.get_text(separator="\n", strip=True)

            # Clean up the text
            lines = [line.strip() for line in text_content.split("\n") if line.strip()]

            # Remove duplicate consecutive lines
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

    def sanitize_filename(self, text: str, max_length: int = 100) -> str:
        """
        Sanitize text for use as filename.

        Args:
            text: Text to sanitize
            max_length: Maximum filename length

        Returns:
            Sanitized filename
        """
        # Remove or replace invalid characters
        text = re.sub(r'[<>:"/\\|?*]', "_", text)
        text = re.sub(r"[^\w\s\-_]", "", text)
        text = re.sub(r"[-\s]+", "_", text)
        text = text.strip("_")

        # Truncate if too long
        if len(text) > max_length:
            text = text[:max_length].rstrip("_")

        return text

    def save_job_description(self, job_id: str, metadata: dict[str, str], description: str, output_dir: Path) -> bool:
        """
        Save job description to markdown file.

        Args:
            job_id: Job ID
            metadata: Job metadata
            description: Job description content
            output_dir: Output directory

        Returns:
            True if saved successfully, False otherwise
        """
        try:
            output_dir.mkdir(parents=True, exist_ok=True)

            # Create filename
            company = self.sanitize_filename(metadata["company"])
            title = self.sanitize_filename(metadata["title"])
            filename = f"{job_id}_{company}_{title}.md"

            filepath = output_dir / filename

            # Create markdown content
            markdown_content = f"""# {metadata['title']}

**Company:** {metadata['company']}
**Job ID:** {job_id}
**Source:** SEEK
**Scraped:** {time.strftime('%Y-%m-%d %H:%M:%S')}

---

{description}
"""

            # Write to file
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(markdown_content)

            logger.info(f"Saved job description to: {filepath}")
            return True

        except Exception as e:
            logger.error(f"Error saving job description: {e}")
            return False

    def scrape_job(self, url: str, output_dir: Path) -> bool:
        """
        Scrape a single job posting.

        Args:
            url: SEEK job URL
            output_dir: Directory to save the markdown file

        Returns:
            True if successful, False otherwise
        """
        job_id = self.extract_job_id(url)
        if not job_id:
            logger.error(f"Could not extract job ID from URL: {url}")
            return False

        # Fetch page
        soup = self.fetch_page(url)
        if not soup:
            return False

        # Extract metadata
        metadata = self.extract_job_metadata(soup)
        logger.info(f"Extracted: {metadata['title']} at {metadata['company']}")

        # Extract and clean job description
        description = self.clean_job_description(soup)
        if not description:
            logger.error(f"Could not extract job description from {url}")
            return False

        # Save to file
        success = self.save_job_description(job_id, metadata, description, output_dir)

        # Respectful delay
        time.sleep(self.delay)

        return success

    def scrape_multiple_jobs(self, urls: list[str], output_dir: Path) -> dict[str, bool]:
        """
        Scrape multiple job postings.

        Args:
            urls: List of SEEK job URLs
            output_dir: Directory to save markdown files

        Returns:
            Dictionary mapping URLs to success status
        """
        results = {}

        logger.info(f"Starting to scrape {len(urls)} job postings...")

        for i, url in enumerate(urls, 1):
            logger.info(f"Processing job {i}/{len(urls)}: {url}")
            try:
                results[url] = self.scrape_job(url, output_dir)
            except Exception as e:
                logger.error(f"Unexpected error processing {url}: {e}")
                results[url] = False

        # Summary
        successful = sum(1 for success in results.values() if success)
        logger.info(f"Scraping completed: {successful}/{len(urls)} jobs successful")

        return results


def main():
    """Main CLI interface."""
    import argparse

    parser = argparse.ArgumentParser(description="Scrape job descriptions from SEEK URLs")
    parser.add_argument("--url", "-u", type=str, help="Single SEEK job URL to scrape")
    parser.add_argument("--urls-file", "-f", type=str, help="File containing SEEK URLs (one per line)")
    parser.add_argument(
        "--output-dir",
        "-o",
        type=str,
        default="data/outputs/job_descriptions",
        help="Output directory for markdown files",
    )
    parser.add_argument(
        "--delay", "-d", type=float, default=2.0, help="Delay between requests in seconds (default: 2.0)"
    )

    args = parser.parse_args()

    if not args.url and not args.urls_file:
        logger.error("Must provide either --url or --urls-file")
        sys.exit(1)

    # Initialize scraper
    scraper = SEEKScraper(delay_between_requests=args.delay)
    output_dir = Path(args.output_dir)

    urls = []

    if args.url:
        urls = [args.url]
    elif args.urls_file:
        try:
            with open(args.urls_file) as f:
                urls = [line.strip() for line in f if line.strip()]
        except Exception as e:
            logger.error(f"Error reading URLs file: {e}")
            sys.exit(1)

    if not urls:
        logger.error("No URLs to process")
        sys.exit(1)

    # Start scraping
    results = scraper.scrape_multiple_jobs(urls, output_dir)

    # Exit with error code if any jobs failed
    failed_jobs = sum(1 for success in results.values() if not success)
    if failed_jobs > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
