# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**applyr** is an intelligent job market analysis toolkit designed to scrape job postings, generate market insights, and build targeted cover letters. The system extracts structured data from job boards, analyzes hiring trends, and optimizes job search processes with data-driven intelligence.

## Current State

applyr is a **fully implemented** job market analysis toolkit with:

- **25+ job postings** scraped and analyzed from SEEK across 23 Australian companies
- **Complete Python scraping infrastructure** with anti-bot measures and content filtering
- **Dual data storage system**: Markdown files for full content + CSV database for application tracking
- **9+ personalized cover letters** generated for target companies
- **Market intelligence reports** with technology trend analysis and hiring patterns
- **Application tracking system** managing the full job search lifecycle
- **Professional PDF export system** with 6 custom CSS templates, SVG brand text, and WeasyPrint engine

### Key Implementation Files

- `scripts/job_scraper/seek_scraper.py` - Core scraping engine (435 lines)
- `scripts/job_scraper/aggregate_jobs.py` - Market intelligence generation (420 lines)
- `applyr/pdf_converter.py` - Professional PDF generation with WeasyPrint (534 lines)
- `applyr/cli.py` - Complete CLI interface with 11 commands (787 lines)
- `applyr/styles/` - 2 professional CSS templates with SVG brand integration
- `data/outputs/job_descriptions/` - 25+ individual job postings in markdown format
- `data/raw/advertisements.csv` - Central application tracking database
- `data/outputs/cover_letters/` - Company-specific personalized cover letters

## Development Setup

### Prerequisites

- **Python 3.8+** with Poetry for dependency management
- **Poetry Installation**: `pip install poetry`

### Dependencies

Key Python packages already configured in `pyproject.toml`:

```python
# Core scraping dependencies
requests>=2.31.0         # HTTP requests for web scraping
beautifulsoup4>=4.12.0   # HTML parsing and content extraction  
lxml>=4.9.0             # Fast XML/HTML processing

# Data processing
pandas>=2.0.0           # CSV manipulation and data analysis
markdown>=3.5.0         # Markdown processing and conversion

# PDF generation
weasyprint>=60.0        # HTML/CSS to PDF conversion with font support
rich>=13.0.0           # CLI interface with progress and tables
typer>=0.9.0           # Type-driven CLI framework
```

### Project Setup

```bash
# Install dependencies
poetry install

# Activate virtual environment  
poetry shell

# Run scraper
python scripts/job_scraper/seek_scraper.py --url "https://www.seek.com.au/job/87066700"

# Generate market analysis
python scripts/job_scraper/aggregate_jobs.py

# Convert documents to PDF
applyr pdf data/raw/resume.md
applyr resume-formats data/raw/resume.md

# Use CLI for all operations
applyr --help
```

## Architecture Notes

applyr implements a **dual data storage architecture** with the following core components:

### Data Storage Pattern

- **Job Descriptions** (`data/outputs/job_descriptions/*.md`): Full job posting content in markdown format
- **Application Database** (`data/raw/advertisements.csv`): Structured tracking database for application lifecycle
- **Critical Relationship**: Both linked by `job_id` (8-digit SEEK identifier) as primary key

### Implemented Modules

- **Web Scraping Module** (`scripts/job_scraper/seek_scraper.py`): SEEK job board extraction with anti-bot measures
- **Data Processing Pipeline** (`scripts/job_scraper/aggregate_jobs.py`): Market analysis and trend identification  
- **PDF Generation Engine** (`applyr/pdf_converter.py`): WeasyPrint-based conversion with professional styling
- **CLI Interface** (`applyr/cli.py`): Comprehensive command-line interface with 11 commands
- **Professional Styling System** (`applyr/styles/`): 6 CSS templates with SVG brand integration
- **Market Analysis Engine**: Technology trend analysis, company hiring patterns, role level distribution
- **Cover Letter Generator** (`data/outputs/cover_letters/`): Company-specific personalized letters
- **Application Tracking** (`advertisements.csv`): Status workflow management (discovered → applied → interviewed → closed)

### Key Design Principles

1. **job_id as Primary Key**: Ensures 1:1 correspondence between markdown content and CSV tracking
2. **Immutable Content**: Job description files preserve original content; only CSV status updates
3. **Dual Access Pattern**: Rich content access via markdown, structured queries via CSV
4. **Data Integrity**: Every scraped job creates both markdown file and CSV entry

## Data Relationship Guide for Claude Instances

When working with applyr data, **always** respect the job_id relationship:

### File Lookup Pattern
```
CSV Entry: 87066700,iSelect Ltd,Software Engineer,SEEK,applied,...
↓ (job_id = 87066700)
Markdown File: 87066700_iSelect_Ltd_Software_Engineer.md
```

### Critical Operations
1. **When analyzing applications**: Use CSV for status/metadata, locate full details via job_id markdown file
2. **When scraping new jobs**: Create both markdown file AND CSV entry with identical job_id
3. **When generating cover letters**: Reference both CSV (company info) and markdown (job requirements)
4. **When validating data**: Ensure every CSV job_id has matching markdown file

### Data Lookup Examples
- Find applied jobs: Query CSV `status='applied'` → Use job_ids to read markdown files
- Analyze job requirements: Extract job_id from filename → Cross-reference with CSV for context
- Update application status: Modify CSV only (preserve original job content in markdown)

**Never assume file existence** - always validate both CSV entry and corresponding markdown file exist.

## Key Considerations

- **Ethical Scraping**: Implement respectful scraping practices with appropriate rate limiting and robots.txt compliance
- **Data Privacy**: Handle job seeker data responsibly and securely
- **Scalability**: Design for processing large volumes of job posting data
- **API Integration**: Consider integration with job board APIs where available
- **Content Quality**: Ensure generated cover letters maintain professional quality and personalization

## Current Implementation Status

applyr is **production-ready** with the following completed components:

### ✅ Completed Features
1. **Python scraping infrastructure** with anti-bot measures and error handling
2. **Dual data storage system** with job_id integrity enforcement  
3. **Market analysis pipeline** generating technology trends and hiring insights
4. **Application tracking system** with CSV-based status management
5. **Cover letter generation** with company-specific personalization
6. **Professional PDF export system** with 6 custom CSS templates and SVG brand text
7. **Comprehensive CLI interface** with 11 commands for complete workflow management

### 🔧 Extension Opportunities  
1. **Additional job boards** (LinkedIn, Indeed, Stack Overflow Jobs)
2. **API integration** for programmatic access to job data
3. **Machine learning** for salary prediction and skill matching
4. **Real-time notifications** for new matching positions
5. **Advanced analytics** with predictive hiring trend analysis

### 📊 Current Data Scale
- **25+ job postings** across 23 companies
- **9+ cover letters** for targeted applications  
- **2 professional PDF templates**: ats, ats_docx
- **SVG brand text integration** with centered, 2x-sized "Cole Morton" branding
- **Market intelligence** on technology demand and company hiring patterns

## PDF Generation System

applyr includes a comprehensive PDF generation system built on WeasyPrint with professional styling capabilities:

### PDF Templates Available

1. **ats.css**: ATS-optimized format for applicant tracking systems
2. **technical.css**: Technical documentation style (if exists)

### SVG Brand Text Implementation

All templates include sophisticated brand text rendering:
- **SVG-based "Cole Morton" text** for perfect font consistency across all environments
- **Horizontal centering** with `background-position: center center`
- **2x size increase** (280pt × 40pt) for prominent header presence
- **Accessibility-compliant**: Hidden text preserved for screen readers
- **WeasyPrint optimized**: Perfect rendering in PDF generation engine

### CLI Commands for PDF Operations

```bash
# Convert single file
applyr pdf resume.md

# Generate all resume formats
applyr resume-formats resume.md

# Batch convert directory
applyr pdf cover_letters/ --batch

# Custom styling
applyr pdf resume.md --css-file applyr/styles/ats.css

# Validate PDF quality
applyr validate-pdf resume_ats.pdf --detailed
```

### PDF Quality Validation

The system includes comprehensive PDF quality validation:
- **File size analysis** with optimization recommendations
- **Quality scoring** (0-10 scale) based on multiple metrics
- **Metadata extraction** including page count and encryption status
- **Optimization suggestions** for file size and rendering quality

### Implementation Architecture

- **WeasyPrint Engine**: Professional HTML/CSS to PDF conversion
- **Font Integration**: Supports system fonts and custom font embedding
- **Link Preservation**: Clickable links maintained in PDF output
- **Print Optimization**: Page breaks, margins, and print-specific CSS
- **Error Handling**: Graceful fallbacks and comprehensive error reporting

### Brand Text Technical Details

The SVG brand text implementation solves font rendering inconsistencies:

```css
.brand-text {
    /* Hide text visually while preserving accessibility */
    font-size: 0 !important;
    text-indent: -9999px !important;
    
    /* Display SVG as centered background */
    background-image: url("data:image/svg+xml,...);
    background-position: center center;
    background-size: contain;
    
    /* 2x dimensions maintaining 7:1 aspect ratio */
    width: 280pt;
    height: 40pt;
}
```

This approach ensures:
- **Perfect visual consistency** between browser preview and PDF output
- **Scalable vector rendering** at any resolution
- **Brand compliance** with exact typography matching
- **Cross-platform compatibility** across all PDF viewers

---

## Multi-Platform Job Scraper Architecture

### Supported Job Boards

applyr implements a factory pattern for multi-platform job processing with automatic source detection:

| Job Board | Job ID Format | URL Format | Implementation | Method |
|-----------|---------------|------------|----------------|--------|
| **SEEK** | 8-digit numeric (e.g., `87066700`) | `https://www.seek.com.au/job/{job_id}` | `SEEKScraper` | Web scraping |
| **Employment Hero** | URL-based slugs | `https://jobs.employmenthero.com/AU/job/{slug}` | `EmploymentHeroScraper` | Web scraping |
| **Indeed** | 16-char hex (e.g., `cc76be5d850127ec`) | `https://au.indeed.com/viewjob?jk={job_id}` | `IndeedManualParser` | Manual text import |

### Architecture Overview

```
JobScraper (Abstract Base Class)
├── SEEKScraper              (SEEK job board - web scraping)
└── EmploymentHeroScraper    (Employment Hero - web scraping)

IndeedManualParser           (Indeed - text file parsing, separate from scrapers)

ScraperFactory
├── detect_job_source()      (Automatic source detection from ID or URL)
├── normalize_to_url()       (Convert job IDs to full URLs)
└── create_scraper()         (Instantiate appropriate scraper/parser)

CLI Integration (add-job command)
├── Web scraping path        (SEEK, Employment Hero)
└── Manual import path       (Indeed via IndeedManualParser)
```

### Indeed Manual Import Implementation

**Status**: Supported via manual text file import (bypasses 403 blocking)

Indeed uses a **manual import** approach instead of web scraping:

#### Why Manual Import?
Indeed was investigated for web scraping but faced these challenges:
- **Active Blocking (403 Errors)**: Indeed actively detects and blocks automated scraping attempts
- Sophisticated fingerprinting detects non-browser clients
- More aggressive anti-bot measures than SEEK or Employment Hero

#### Official API Limitations
Indeed's official APIs are not suitable for personal job tracking applications:
- **No job search/retrieval API**: APIs only support posting jobs TO Indeed (not retrieving listings)
- **Partner-only access**: Requires business partnership agreements (not available to individuals)
- **Commercial pricing**: Undisclosed pricing, designed for ATS/recruitment platforms at enterprise scale
- **ATS focus**: Built for employers and recruitment platforms, not job seekers

#### Available APIs (Partner-Only)
1. **Job Sync API**: Post jobs TO Indeed (for employers/ATS)
2. **Disposition Sync API**: Sync candidate status updates
3. **Indeed Apply**: Integration for application process

All require:
- Business partnership agreement with Indeed
- OAuth 2.0 authentication
- Commercial-scale pricing (not disclosed publicly)
- Approval as an ATS or recruitment technology partner

#### Manual Import Solution

To support Indeed while remaining ToS compliant and bypassing blocking, applyr implements **manual text file import**:

**Implementation**: `applyr/scraper_indeed_manual.py` - `IndeedManualParser`

**User Workflow**:
1. User visits Indeed job page in browser
2. User copies entire page content (Cmd+A, Cmd+C / Ctrl+A, Ctrl+C)
3. User saves to `data/raw/jobs/{job_id}.txt`
4. User runs `applyr add-job {job_id}` or `applyr add-job "{url}"`
5. System detects Indeed, reads text file, parses job data

**Key Methods**:
```python
class IndeedManualParser:
    def extract_job_id(self, url_or_id: str) -> Optional[str]:
        """Extract job ID from URL or 16-char hex ID"""
        # Returns 'ind-{job_id}' format
    
    def load_job_text(self, job_id: str) -> Optional[str]:
        """Load text file from data/raw/jobs/{job_id}.txt"""
    
    def parse_job_data(self, text_content: str) -> Dict[str, str]:
        """Parse title, company, description from copied text"""
        # Uses heuristics to extract job details from plain text
    
    def process_job(self, url_or_id: str) -> Optional[Dict]:
        """Main processing method - combines all steps"""
```

**Benefits**:
- ✅ No web scraping (bypasses 403 errors)
- ✅ ToS compliant (user manually copies content)
- ✅ Integrates with applyr's job tracking system
- ✅ No Indeed API required

**Trade-offs**:
- ⚠️ Requires manual copy/paste step (not fully automated)
- ⚠️ Text parsing may be less robust than HTML parsing

**File Structure**:
```
data/raw/jobs/
├── .gitignore           # Ignore *.txt files (privacy)
├── README.md            # Instructions for manual import
└── {job_id}.txt         # User-created text files (gitignored)
```

### Terms of Service Compliance System

**Global ToS Warning Implementation**

All scrapers now include ToS compliance warnings:

```python
# Global tracking in scraper_base.py
_TOS_WARNINGS_SHOWN: Set[str] = set()

def _show_tos_warning_if_needed(self) -> None:
    """
    Display warning once per source per session
    Warns about ToS restrictions and personal use only
    """
```

**Warning Display**:
```
⚠️  Indeed Scraping Notice: Web scraping may violate Terms of Service.
   This tool is for personal use only with respectful rate limiting.
   For commercial use, please use official APIs where available.
   See docs/TERMS_OF_SERVICE.md for detailed information.
```

### Responsible Scraping Practices

All scrapers implement consistent rate limiting and respectful practices:

1. **Rate Limiting**:
   - Default delay: 2.0 seconds between requests
   - Configurable via CLI `--delay` flag
   - Enforced in `scraper_base.py`

2. **Anti-Bot Headers**:
   - Standard browser User-Agent
   - Sec-Fetch-* headers for legitimacy
   - Referer and Origin headers per domain

3. **Error Handling**:
   - Graceful 403/blocking detection
   - Logging of all failed requests
   - No retry bombing on failures

4. **Content Respect**:
   - Only extracts job description content
   - Removes ads and promotional content
   - Does not republish or redistribute

### Factory Pattern Usage

**Automatic Source Detection**:
```python
# Supports multiple input formats
detect_job_source("87066700")                    # → "seek"
detect_job_source("cc76be5d850127ec")            # → "indeed"
detect_job_source("https://au.indeed.com/...")   # → "indeed"

# Creates appropriate scraper
scraper, url = create_scraper("cc76be5d850127ec")
# Returns: (IndeedScraper instance, normalized URL)
```

### Testing Strategy

**Comprehensive test coverage** in `tests/`:

1. **`test_scraper_factory.py`**: Factory pattern integration
   - Source detection for SEEK and Employment Hero
   - URL normalization
   - Scraper instantiation
   - Mixed-source batch processing
   - Validation that Indeed URLs are rejected

### CLI Integration

**Command**: `applyr add-job`

Supports SEEK and Employment Hero with automatic detection:
```bash
# SEEK
applyr add-job 87066700

# Employment Hero
applyr add-job https://jobs.employmenthero.com/AU/job/company-position

# Mixed batch
applyr add-job 87066700,https://jobs.employmenthero.com/AU/job/company-position-xyz
```

### Documentation

**Terms of Service Documentation**: `docs/TERMS_OF_SERVICE.md`

Comprehensive legal guidance covering:
- Legal considerations for web scraping
- ToS summaries for each job board
- Official API alternatives
- Responsible use guidelines
- User responsibilities and warnings

**Key Points**:
- Personal use only (not commercial)
- Respect rate limits (2+ second delays)
- No bulk scraping or database creation
- No content republishing
- Official APIs recommended for commercial use

### Extension Points

To add a new job board:

1. **Create scraper class** (`applyr/scraper_newboard.py`):
   ```python
   class NewBoardScraper(JobScraper):
       def get_source_name(self) -> str: ...
       def extract_job_id(self, url: str) -> Optional[str]: ...
       def extract_job_metadata(self, soup: BeautifulSoup) -> Dict[str, str]: ...
       def clean_job_description(self, soup: BeautifulSoup) -> Optional[str]: ...
   ```

2. **Update factory** (`applyr/scraper_factory.py`):
   - Add domain/ID pattern detection in `detect_job_source()`
   - Add URL normalization in `normalize_to_url()`
   - Add scraper instantiation in `create_scraper()`

3. **Add tests** (`tests/test_newboard_scraper.py`):
   - Job ID extraction tests
   - Metadata extraction tests
   - Factory integration tests

4. **Update documentation**:
   - Add to README.md supported boards table
   - Update CLI help text with examples
   - Add ToS summary to docs/TERMS_OF_SERVICE.md

### Known Limitations

1. **Indeed Not Supported**: Active blocking and API limitations
   - Indeed returns 403 errors to automated scrapers
   - No official API for job retrieval (only for posting jobs)
   - Users must track Indeed jobs manually

2. **DOM Selector Fragility**: Job boards update their HTML regularly
   - Multiple fallback selectors implemented
   - Monitor for scraping failures
   - Update selectors as needed

3. **Rate Limiting**: Balance between speed and respect
   - 2-second delay is conservative
   - Can be increased but not decreased
   - No automatic retry on 403

4. **Personal Use Only**: Not designed for commercial scraping
   - No bulk harvesting features
   - Individual job tracking focus
   - Users responsible for ToS compliance