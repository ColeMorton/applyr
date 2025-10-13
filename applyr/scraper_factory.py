"""Factory for creating appropriate job scrapers based on URL or job ID"""

import re
from typing import Optional
from urllib.parse import urlparse

from .database import ApplicationDatabase
from .scraper_base import JobScraper
from .scraper import SEEKScraper
from .scraper_employment_hero import EmploymentHeroScraper


def detect_job_source(url_or_id: str) -> str:
    """Detect which job board a URL or ID belongs to.
    
    Args:
        url_or_id: Either a full URL or a SEEK job ID (8 digits)
        
    Returns:
        Source identifier: "seek" or "employment_hero"
        
    Raises:
        ValueError: If source cannot be determined
    """
    url_or_id = url_or_id.strip()
    
    # Check if it's a SEEK job ID (8 digits only)
    if re.match(r'^\d{8}$', url_or_id):
        return "seek"
    
    # Check if it's a URL
    if url_or_id.startswith('http://') or url_or_id.startswith('https://'):
        parsed = urlparse(url_or_id)
        domain = parsed.netloc.lower()
        
        if 'seek.com.au' in domain:
            return "seek"
        elif 'employmenthero.com' in domain:
            return "employment_hero"
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
    if url_or_id.startswith('http://') or url_or_id.startswith('https://'):
        return url_or_id
    
    # Convert SEEK job ID to URL
    if source == "seek" and re.match(r'^\d{8}$', url_or_id):
        return f"https://www.seek.com.au/job/{url_or_id}"
    
    # If we get here, something is wrong
    raise ValueError(f"Cannot normalize {url_or_id} with source {source}")


def create_scraper(url_or_id: str, delay: float = 2.0, 
                   database: Optional[ApplicationDatabase] = None) -> tuple[JobScraper, str]:
    """Create appropriate scraper instance based on URL or job ID.
    
    Args:
        url_or_id: Either a full URL or a SEEK job ID (8 digits)
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
    else:
        raise ValueError(f"Unsupported job board source: {source}")
    
    return scraper, url

