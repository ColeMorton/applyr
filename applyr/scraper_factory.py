"""Factory for creating appropriate job scrapers based on URL or job ID"""

import re
from typing import Optional
from urllib.parse import urlparse

from .database import ApplicationDatabase
from .scraper import SEEKScraper
from .scraper_base import JobScraper
from .scraper_employment_hero import EmploymentHeroScraper
from .scraper_indeed_manual import IndeedManualParser
from .scraper_linkedin_manual import LinkedInManualParser


def detect_job_source(url_or_id: str) -> str:
    """Detect which job board a URL or ID belongs to.

    Args:
        url_or_id: Either a full URL, a SEEK job ID (8 digits), an Indeed job ID (16-char hex), or LinkedIn job ID

    Returns:
        Source identifier: "seek", "employment_hero", "indeed", or "linkedin"

    Raises:
        ValueError: If source cannot be determined
    """
    url_or_id = url_or_id.strip()

    # Check if it's a SEEK job ID (8 digits only)
    if re.match(r"^\d{8}$", url_or_id):
        return "seek"

    # Check if it's an Indeed job ID (16-character hexadecimal)
    if re.match(r"^[a-f0-9]{16}$", url_or_id):
        return "indeed"

    # Check if it's a LinkedIn job ID (numeric)
    if re.match(r"^\d+$", url_or_id) and len(url_or_id) > 8:
        return "linkedin"

    # Check if it's a URL
    if url_or_id.startswith(("http://", "https://")):
        parsed = urlparse(url_or_id)
        domain = parsed.netloc.lower()

        if "seek.com.au" in domain:
            return "seek"
        elif "employmenthero.com" in domain:
            return "employment_hero"
        elif "indeed.com" in domain:
            return "indeed"
        elif "linkedin.com" in domain:
            return "linkedin"
        else:
            raise ValueError(f"Unsupported job board domain: {domain}")

    raise ValueError(f"Could not determine job board source from: {url_or_id}")


def normalize_to_url(url_or_id: str, source: str) -> str:
    """Normalize a job ID or URL to a full URL.

    Args:
        url_or_id: Either a full URL or a job ID
        source: Source identifier from detect_job_source()

    Returns:
        Full URL to the job posting
    """
    # If already a URL, return as-is
    if url_or_id.startswith(("http://", "https://")):
        return url_or_id

    # Convert SEEK job ID to URL
    if source == "seek" and re.match(r"^\d{8}$", url_or_id):
        return f"https://www.seek.com.au/job/{url_or_id}"

    # Convert Indeed job ID to URL
    if source == "indeed" and re.match(r"^[a-f0-9]{16}$", url_or_id):
        return f"https://au.indeed.com/viewjob?jk={url_or_id}"

    # Convert LinkedIn job ID to URL
    if source == "linkedin" and re.match(r"^\d+$", url_or_id):
        return f"https://www.linkedin.com/jobs/view/{url_or_id}/"

    # If we get here, something is wrong
    raise ValueError(f"Cannot normalize {url_or_id} with source {source}")


def check_manual_import_available(url_or_id: str) -> tuple[bool, str, str]:
    """Check if manual import text file is available for the job.

    Args:
        url_or_id: Either a full URL or a job ID

    Returns:
        Tuple of (is_available, source_type, file_path)
    """
    try:
        source = detect_job_source(url_or_id)

        if source == "linkedin":
            # Check for LinkedIn manual import
            linkedin_parser = LinkedInManualParser()
            raw_job_id = linkedin_parser.get_raw_job_id(url_or_id)
            if raw_job_id:
                file_path = linkedin_parser.raw_jobs_dir / f"{raw_job_id}.txt"
                if file_path.exists():
                    return True, "linkedin_manual", str(file_path)

        elif source == "indeed":
            # Check for Indeed manual import
            indeed_parser = IndeedManualParser()
            raw_job_id = indeed_parser.get_raw_job_id(url_or_id)
            if raw_job_id:
                file_path = indeed_parser.raw_jobs_dir / f"{raw_job_id}.txt"
                if file_path.exists():
                    return True, "indeed_manual", str(file_path)

        return False, "", ""
    except Exception:
        return False, "", ""


def create_scraper(
    url_or_id: str, delay: float = 2.0, database: Optional[ApplicationDatabase] = None
) -> tuple[JobScraper, str]:
    """Create appropriate scraper instance based on URL or job ID.

    Args:
        url_or_id: Either a full URL or a job ID
        delay: Delay between requests in seconds
        database: Optional ApplicationDatabase instance

    Returns:
        Tuple of (scraper instance, normalized URL)

    Raises:
        ValueError: If source cannot be determined or is unsupported
    """
    source = detect_job_source(url_or_id)
    url = normalize_to_url(url_or_id, source)

    if source == "seek":
        scraper = SEEKScraper(delay_between_requests=delay, database=database)
    elif source == "employment_hero":
        scraper = EmploymentHeroScraper(delay_between_requests=delay, database=database)
    elif source == "linkedin":
        raise ValueError(
            "LinkedIn requires manual import. Please save the job page to data/raw/jobs/linked_in/{job_id}.txt and run the command again."
        )
    else:
        raise ValueError(f"Unsupported job board source: {source}")

    return scraper, url


def create_manual_parser(url_or_id: str) -> tuple[object, str]:
    """Create appropriate manual parser instance based on URL or job ID.

    Args:
        url_or_id: Either a full URL or a job ID

    Returns:
        Tuple of (parser instance, source_type)

    Raises:
        ValueError: If source cannot be determined or is unsupported
    """
    source = detect_job_source(url_or_id)

    if source == "linkedin":
        parser = LinkedInManualParser()
        return parser, "linkedin_manual"
    elif source == "indeed":
        parser = IndeedManualParser()
        return parser, "indeed_manual"
    else:
        raise ValueError(f"Unsupported manual import source: {source}")
