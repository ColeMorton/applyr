# SEEK Job Description Scraper

A reusable web scraper to extract job descriptions from SEEK URLs and save them as markdown files, excluding unwanted sections like headers, footers, company profiles, and warning sections.

## Features

- **Anti-bot measures**: Uses proper headers and user agents to bypass SEEK's basic protection
- **Content filtering**: Automatically removes headers, footers, Company Profile, "Be Careful", and "What can I earn" sections
- **Respectful scraping**: Configurable delays between requests (default: 2 seconds)
- **Error handling**: Comprehensive error handling for network failures and parsing issues
- **Markdown output**: Clean, formatted markdown files with job metadata
- **Batch processing**: Process multiple URLs from a file
- **Flexible CLI**: Command-line interface with multiple options

## Requirements

The following dependencies are required (already added to `requirements.txt`):

```
requests>=2.31.0,<3.0.0
beautifulsoup4>=4.12.0,<5.0.0
lxml>=4.9.0,<6.0.0
```

Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### CLI Interface

#### Scrape a single job:
```bash
python scripts/job_scraper/seek_scraper.py --url "https://www.seek.com.au/job/86524100"
```

#### Scrape multiple jobs from a file:
```bash
python scripts/job_scraper/seek_scraper.py --urls-file scripts/job_scraper/job_urls.txt
```

#### Custom output directory:
```bash
python scripts/job_scraper/seek_scraper.py --urls-file job_urls.txt --output-dir custom_output
```

#### Custom delay between requests:
```bash
python scripts/job_scraper/seek_scraper.py --urls-file job_urls.txt --delay 5.0
```

### Test Scripts

#### Test single job scraping:
```bash
python scripts/job_scraper/test_single_job.py
```

#### Batch scrape all provided URLs:
```bash
python scripts/job_scraper/batch_scrape_jobs.py
```

### Python API

```python
from pathlib import Path
from scripts.job_scraper.seek_scraper import SEEKScraper

# Initialize scraper
scraper = SEEKScraper(delay_between_requests=2.0)

# Scrape single job
output_dir = Path("output")
success = scraper.scrape_job("https://www.seek.com.au/job/86524100", output_dir)

# Scrape multiple jobs
urls = ["https://www.seek.com.au/job/86524100", "https://www.seek.com.au/job/86398474"]
results = scraper.scrape_multiple_jobs(urls, output_dir)
```

## Output Format

Job descriptions are saved as markdown files with the following naming convention:
```
{job_id}_{company_name}_{job_title}.md
```

Example: `86524100_Squiz_Australia_Pty_Ltd_Tech_Principal_Lead_Engineer.md`

### File Structure

```markdown
# Job Title

**Company:** Company Name  
**Job ID:** 86524100  
**Source:** SEEK  
**Scraped:** 2025-09-02 14:06:20

---

[Clean job description content without headers, footers, or unwanted sections]
```

## File Structure

```
scripts/job_scraper/
├── README.md                 # This documentation
├── seek_scraper.py          # Main scraper script
├── job_urls.txt             # List of SEEK job URLs
├── test_single_job.py       # Test single job scraping
└── batch_scrape_jobs.py     # Batch scraping test
```

## Content Filtering

The scraper automatically removes:

- Site headers and navigation
- Page footers
- Company profile sections
- "Be Careful" warning sections
- "What can I earn" salary sections  
- Advertisement content
- Duplicate consecutive lines

## Error Handling

- **403 Forbidden**: SEEK blocking requests (logged with specific message)
- **Network errors**: Connection failures, timeouts
- **Parsing errors**: Invalid HTML or missing content
- **File errors**: Issues saving markdown files

Failed jobs are logged and reported in batch processing summary.

## Best Practices

1. **Respectful scraping**: Default 2-second delay between requests
2. **Error handling**: Continue processing remaining jobs if some fail
3. **Clean output**: Sanitized filenames and structured content
4. **Logging**: Comprehensive logging for debugging and monitoring

## Limitations

- SEEK may implement additional anti-bot measures over time
- Some job postings may have unique layouts that require content selector updates
- Rate limiting may be required for large-scale scraping

## Job Description Aggregator

The scraper also includes an aggregator script that combines all individual job description files into a single consolidated markdown file.

### Aggregator Usage

#### Default aggregation (uses today's date):
```bash
python scripts/job_scraper/aggregate_jobs.py
```

#### Specify custom date:
```bash
python scripts/job_scraper/aggregate_jobs.py --date 20250901
```

#### Custom input/output paths:
```bash
python scripts/job_scraper/aggregate_jobs.py --input-dir custom_jobs --output-file my_aggregate.md
```

### Aggregator Features

- **Date-based naming**: Files named like `20250902_job_descriptions_aggregate.md`
- **Summary statistics**: Job level distribution, top companies, technology mentions
- **Table of contents**: Quick navigation to any job posting
- **Unique titles**: Each job gets a descriptive title with company and ID
- **Metadata preservation**: All original job metadata included
- **Clean formatting**: Professional markdown structure with proper sections

### Aggregator Scripts

- `aggregate_jobs.py` - Main aggregation script with CLI interface
- `test_aggregator.py` - Test the aggregator functionality

## Troubleshooting

### 403 Forbidden Errors
- SEEK has detected automated scraping
- Try increasing delay between requests
- Headers may need updating

### Missing Job Content
- Job posting may have unusual HTML structure
- Check logs for parsing errors
- Content selectors may need updating

### File Save Errors
- Check output directory permissions
- Ensure sufficient disk space
- Verify filename sanitization for special characters