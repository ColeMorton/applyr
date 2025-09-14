"""Job scraper module for SEEK with Rich console integration"""

import logging
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import parse_qs, urlparse

import requests
from bs4 import BeautifulSoup, Tag
from rich.console import Console
from rich.progress import track, Progress, SpinnerColumn, TextColumn

from .database import ApplicationDatabase, JobStatus, Priority

logger = logging.getLogger(__name__)


class SEEKScraper:
    """SEEK job description scraper with anti-bot measures."""

    def __init__(self, delay_between_requests: float = 2.0, database: Optional[ApplicationDatabase] = None):
        self.delay = delay_between_requests
        self.database = database
        self.session = requests.Session()
        
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-AU,en;q=0.9,en-US;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cache-Control': 'max-age=0',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
        })

    def extract_job_id(self, url: str) -> Optional[str]:
        """Extract job ID from SEEK URL."""
        try:
            path = urlparse(url).path
            match = re.search(r'/job/(\d+)', path)
            return match.group(1) if match else None
        except Exception as e:
            logger.error(f"Error extracting job ID from {url}: {e}")
            return None

    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch a webpage and return BeautifulSoup object."""
        try:
            headers = {'Referer': 'https://www.seek.com.au/'}
            response = self.session.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                logger.error(f"Access forbidden (403) for {url}. SEEK may be blocking the request.")
            else:
                logger.error(f"HTTP error {e.response.status_code} for {url}: {e}")
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
        return None

    def extract_job_metadata(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract job metadata (title, company) from the page."""
        metadata = {
            'title': 'Unknown Job',
            'company': 'Unknown Company',
        }
        
        try:
            title_selectors = [
                'h1[data-automation="job-detail-title"]',
                'h1.jobtitle',
                'h1',
                '[data-automation="job-detail-title"]'
            ]
            
            for selector in title_selectors:
                title_elem = soup.select_one(selector)
                if title_elem:
                    metadata['title'] = title_elem.get_text(strip=True)
                    break
            
            company_selectors = [
                '[data-automation="advertiser-name"]',
                '.advertiser-name',
                '[data-automation="job-company"]',
                '.company-name'
            ]
            
            for selector in company_selectors:
                company_elem = soup.select_one(selector)
                if company_elem:
                    metadata['company'] = company_elem.get_text(strip=True)
                    break
        except Exception as e:
            logger.error(f"Error extracting metadata: {e}")
        
        return metadata

    def clean_job_description(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract and clean job description content, excluding unwanted sections."""
        try:
            job_desc_selectors = [
                '[data-automation="jobAdDetails"]',
                '.jobAdDetails',
                '[data-automation="job-detail-description"]',
                '.job-description',
                '.jobDescription',
                '.adDetails'
            ]
            
            job_desc_elem = None
            for selector in job_desc_selectors:
                job_desc_elem = soup.select_one(selector)
                if job_desc_elem:
                    break
            
            if not job_desc_elem:
                content_areas = soup.find_all(['div', 'section'], 
                                            string=lambda text: text and 
                                            any(keyword in text.lower() for keyword in 
                                                ['responsibilities', 'requirements', 'experience', 'role', 'position']))
                if content_areas:
                    job_desc_elem = content_areas[0].parent
            
            if not job_desc_elem:
                logger.error("Could not find job description content")
                return None
            
            unwanted_selectors = [
                '[data-automation="company-profile"]',
                '.company-profile',
                '.advertiser-profile',
                '.safety-warning',
                '[data-automation="safety-warning"]',
                '*:contains("Be Careful")',
                '*:contains("What can I earn")',
                '.navigation',
                '.nav',
                'nav',
                '.advertisement',
                '.ad',
                '[data-automation="jobsearch-JobseekerHeaderLinks"]',
                'footer',
                '.footer',
                '.page-footer'
            ]
            
            for selector in unwanted_selectors:
                for elem in job_desc_elem.select(selector):
                    elem.decompose()
            
            warning_texts = ['be careful', 'what can i earn', 'company profile', 'scam', 'fraud']
            for elem in job_desc_elem.find_all(text=True):
                if any(warning in elem.lower() for warning in warning_texts):
                    parent = elem.parent
                    if parent:
                        parent.decompose()
            
            text_content = job_desc_elem.get_text(separator='\n', strip=True)
            lines = [line.strip() for line in text_content.split('\n') if line.strip()]
            
            cleaned_lines = []
            prev_line = ""
            for line in lines:
                if line != prev_line:
                    cleaned_lines.append(line)
                    prev_line = line
            
            return '\n\n'.join(cleaned_lines)
        except Exception as e:
            logger.error(f"Error cleaning job description: {e}")
            return None

    def sanitize_filename(self, text: str, max_length: int = 100) -> str:
        """Sanitize text for use as filename."""
        text = re.sub(r'[<>:"/\\|?*]', '_', text)
        text = re.sub(r'[^\w\s\-_]', '', text)
        text = re.sub(r'[-\s]+', '_', text)
        text = text.strip('_')
        
        if len(text) > max_length:
            text = text[:max_length].rstrip('_')
        
        return text

    def save_job_description(self, job_id: str, metadata: Dict[str, str], 
                           description: str, output_dir: Path) -> bool:
        """Save job description to markdown file."""
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            
            company = self.sanitize_filename(metadata['company'])
            title = self.sanitize_filename(metadata['title'])
            filename = f"{job_id}_{company}_{title}.md"
            
            filepath = output_dir / filename
            
            markdown_content = f"""# {metadata['title']}

**Company:** {metadata['company']}  
**Job ID:** {job_id}  
**Source:** SEEK  
**Scraped:** {time.strftime('%Y-%m-%d %H:%M:%S')}

---

{description}
"""
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            return True
        except Exception as e:
            logger.error(f"Error saving job description: {e}")
            return False

    def scrape_job(self, url: str, output_dir: Path, console: Optional[Console] = None) -> bool:
        """Scrape a single job posting with Rich console output."""
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
                company_name=metadata['company'],
                job_title=metadata['title'],
                source="SEEK",
                url=url,
                status=JobStatus.DISCOVERED,
                priority=Priority.MEDIUM
            )
        
        time.sleep(self.delay)
        return success


def scrape_jobs(urls: List[str], output_dir: Path, delay: float, console: Console, 
                database: Optional[ApplicationDatabase] = None) -> Dict[str, bool]:
    """Scrape multiple jobs with Rich progress tracking."""
    scraper = SEEKScraper(delay_between_requests=delay, database=database)
    results = {}
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        task = progress.add_task(f"Scraping {len(urls)} jobs...", total=len(urls))
        
        for url in urls:
            progress.update(task, description=f"Processing {url[:50]}...")
            try:
                results[url] = scraper.scrape_job(url, output_dir, console)
                progress.advance(task)
            except Exception as e:
                console.print(f"[red]❌ Error processing {url}: {e}[/red]")
                results[url] = False
                progress.advance(task)
    
    return results