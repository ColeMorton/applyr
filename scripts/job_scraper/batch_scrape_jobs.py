#!/usr/bin/env python3
"""
Batch scrape all SEEK job postings from the provided URLs file.
"""

import sys
from pathlib import Path

# Add the parent directory to the path so we can import the scraper
sys.path.insert(0, str(Path(__file__).parent.parent))

from job_scraper.seek_scraper import SEEKScraper


def batch_scrape_jobs():
    """Scrape all jobs from the URLs file."""
    # URLs file
    urls_file = Path(__file__).parent / "job_urls.txt"
    
    # Output directory
    output_dir = Path("data/outputs/job_descriptions")
    
    # Read URLs
    try:
        with open(urls_file, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print("Error reading URLs file: {e}")
        return False
    
    print("Found {len(urls)} URLs to process")
    print("Output directory: {output_dir}")
    
    # Initialize scraper with respectful delay
    scraper = SEEKScraper(delay_between_requests=3.0)  # 3 second delay to be respectful
    
    print("Starting batch scraping...")
    print("=" * 50)
    
    # Scrape all jobs
    results = scraper.scrape_multiple_jobs(urls, output_dir)
    
    # Summary
    successful = sum(1 for success in results.values() if success)
    failed = len(results) - successful
    
    print("\n" + "=" * 50)
    print("SCRAPING SUMMARY")
    print("=" * 50)
    print("Total jobs: {len(results)}")
    print("Successful: {successful}")
    print("Failed: {failed}")
    
    if failed > 0:
        print("\nFailed URLs:")
        for url, success in results.items():
            if not success:
                print("  ❌ {url}")
    
    print("\nJob descriptions saved to: {output_dir}")
    
    return failed == 0

if __name__ == "__main__":
    success = batch_scrape_jobs()
    sys.exit(0 if success else 1)