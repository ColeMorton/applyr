#!/usr/bin/env python3
"""
Test script to scrape a single SEEK job posting.
"""

import sys
from pathlib import Path

# Add the parent directory to the path so we can import the scraper
sys.path.insert(0, str(Path(__file__).parent.parent))

from job_scraper.seek_scraper import SEEKScraper


def test_single_job():
    """Test scraping a single job."""
    # Test URL (first one from the provided list)
    test_url = "https://www.seek.com.au/job/86524100"
    
    # Output directory
    output_dir = Path("data/outputs/job_descriptions")
    
    # Initialize scraper
    scraper = SEEKScraper(delay_between_requests=1.0)  # Shorter delay for testing
    
    print("Testing single job scrape: {test_url}")
    print("Output directory: {output_dir}")
    
    # Scrape the job
    success = scraper.scrape_job(test_url, output_dir)
    
    if success:
        print("✅ Test successful! Job description saved.")
    else:
        print("❌ Test failed! Check logs for details.")
    
    return success

if __name__ == "__main__":
    success = test_single_job()
    sys.exit(0 if success else 1)