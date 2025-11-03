# applyr

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Poetry](https://img.shields.io/badge/poetry-1.0+-blue.svg)](https://python-poetry.org/)
[![CI Tests](https://github.com/ColeMorton/applyr/actions/workflows/tests.yml/badge.svg)](https://github.com/ColeMorton/applyr/actions/workflows/tests.yml)
[![Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![mypy](https://img.shields.io/badge/type%20checker-mypy-blue.svg)](https://github.com/python/mypy)
[![bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![pytest](https://img.shields.io/badge/test-pytest-green.svg)](https://docs.pytest.org/)

**Intelligent Job Market Analysis Toolkit** — Scrape job postings, generate market insights, and build targeted cover letters. Extract structured data from job boards, analyze hiring trends, and optimize your job search with data-driven intelligence.

Perfect for developers and job seekers looking to gain competitive advantage through market intelligence and personalized application strategies.

## 🚀 What applyr Does

applyr transforms job hunting from guesswork into data-driven strategy by:

- **🔍 Market Intelligence**: Scrapes and analyzes job postings to identify hiring trends, in-demand technologies, and salary patterns
- **📊 Technology Insights**: Tracks which skills are most sought-after across companies and roles
- **💼 Company Analysis**: Identifies active hiring companies, job volumes, and preferred tech stacks
- **✍️ Personalized Cover Letters**: Generates company-specific cover letters based on job requirements and research
- **📈 Career Optimization**: Provides data-driven insights to optimize your job search strategy

## 📋 Current Features

### Job Market Data Collection
- **Multi-platform support**: SEEK, Employment Hero, and Indeed job boards
- **30+ job postings analyzed** from multiple job boards across 25 Australian companies
- **Automated scraping** with anti-bot measures and respectful rate limiting (SEEK, Employment Hero)
- **Manual import support** for Indeed jobs via text file processing (bypasses 403 blocking)
- **Structured data extraction** with metadata preservation and timestamps
- **Batch processing** capabilities for efficient data collection
- **Flexible input**: Accepts SEEK job IDs (8 digits), Indeed hex IDs (16 chars), or full URLs
- **ToS compliance**: Built-in warnings and responsible scraping practices (personal use only)

### Market Intelligence & Analytics
- **Technology trend analysis**: Identifies most in-demand skills (React, TypeScript, Node.js, AWS)
- **Job level distribution**: Analyzes role seniority patterns (Senior 28%, Mid-level 60%, Junior 4%)
- **Company hiring patterns**: Tracks which companies are actively hiring and job volumes
- **Geographic insights**: Geographic analysis across major tech hubs
- **Salary intelligence**: Limited salary data extraction where available

### Cover Letter Generation
- **12+ personalized cover letters** generated for target companies
- **Company-specific research**: Each letter references specific company details and tech stacks
- **Technical skill mapping**: Direct alignment of candidate skills to job requirements
- **Professional branding**: Consistent personal narrative with portfolio links
- **Template-based approach**: Structured format ensuring quality and consistency

### Data Processing Pipeline
- **Python-based infrastructure** with comprehensive CLI interfaces
- **Markdown output format** for human-readable and processable data
- **Aggregation engine**: Combines individual job data into market intelligence reports
- **Quality assurance**: Content filtering, metadata validation, error handling
- **Testing utilities**: Comprehensive test scripts for validation

### Professional PDF Export System
- **2 custom CSS templates**: ats (applicant tracking system optimized), ats_docx (DOCX conversion optimized)
- **SVG brand text integration** with configurable branding (2x size, perfect font consistency)
- **WeasyPrint engine** for professional HTML/CSS to PDF conversion with font support
- **Batch processing capabilities** for entire directories with progress tracking
- **Quality validation system** with file size analysis and optimization recommendations
- **Clickable links preserved** in PDF output with proper link handling
- **Print optimization** with proper page breaks, margins, and professional formatting

### Application Tracking System
- **Centralized job database** with CSV backend for application management
- **Status workflow tracking** from discovery → applied → interviewed → closed
- **Automated job registration** during scraping with metadata capture
- **Application statistics** and success rate analytics
- **Company targeting insights** and hiring pattern analysis

## 🚀 Quick Start

### Requirements

```bash
# Install Poetry (if not already installed)
pip install poetry

# Install project dependencies
poetry install
```

**Dependencies:**
- `requests>=2.31.0`
- `beautifulsoup4>=4.12.0`
- `lxml>=4.9.0`
- `markdown>=3.5.0`
- `weasyprint>=60.0`
- `pyyaml>=6.0.1`

### First-Time Setup

Before using applyr, you need to configure it with your personal information:

1. **Copy the configuration template:**
   ```bash
   cp config.template.yaml config.yaml
   ```

2. **Edit `config.yaml` with your personal information:**
   ```yaml
   personal_info:
     name: "Your Name"
     email: "your-email@example.com"
     phone: "Your Phone"
     website: "yourwebsite.com"
     github: "yourusername"
     linkedin: "linkedin.com/in/your-profile"
     location: "Your City, State"

   branding:
     svg_text: "{{YOUR_BRAND_TEXT}}"  # SVG data URI for brand text
     footer_text: "yourwebsite.com"  # Text for PDF footers
   ```

3. **The `config.yaml` file is gitignored** - your personal information stays private.

See `docs/TEMPLATE_SETUP.md` for detailed personalization instructions.

**Additional Dependencies:**
- `pandas>=2.0.0`

### Basic Usage

#### 1. Scrape Individual Job Posting
```bash
python scripts/job_scraper/seek_scraper.py --url "https://www.seek.com.au/job/86524100"
```

#### 2. Batch Process Multiple Jobs
```bash
python scripts/job_scraper/batch_scrape_jobs.py
```

#### 3. Generate Market Intelligence Report
```bash
python scripts/job_scraper/aggregate_jobs.py
```

#### 4. Test Single Job Processing
```bash
python scripts/job_scraper/test_single_job.py
```

#### 5. Convert Markdown to PDF
```bash
# Convert single file
applyr pdf README.md

# Generate all resume formats at once
applyr resume-formats data/raw/resume.md

# Convert with specific template
applyr pdf resume.md --style ats

# Batch convert entire directory
applyr pdf data/outputs/cover_letters --batch --output output_pdfs/

# Validate PDF quality
applyr validate-pdf resume_executive.pdf --detailed
```

## 📁 Data Structure

applyr organizes all outputs under `data/` with clear separation:

```
data/
├── raw/                        # Raw data and application database
│   └── advertisements.csv      # Central job application tracking database
└── outputs/
    ├── job_descriptions/       # Latest batch (Sept 12, 2025)
    │   ├── 20250912_job_descriptions_aggregate.md
    │   └── [individual job files]
    ├── job_descriptions_1/     # Previous batch (Sept 2, 2025)
    │   ├── 20250902_job_descriptions_aggregate.md
    │   └── [individual job files]
    └── cover_letters/          # Personalized cover letters
        └── [company-specific letters]
```

### Data Relationship Model

The system maintains a **1:1 correspondence** between job descriptions and advertisement tracking records:

- **Job Descriptions** (`data/outputs/job_descriptions/*.md`): Full job posting content in markdown format
- **Advertisements** (`data/raw/advertisements.csv`): Application tracking database with status management

**Key Relationship**: Both are linked by `job_id` - the 8-digit SEEK identifier that serves as the primary key across both data sources.

**Example**:
- Job Description: `12345678_Example_Corp_Software_Engineer.md`
- CSV Record: `12345678,Example Corp,Software Engineer,SEEK,applied,medium,...`

This dual storage pattern enables:
- **Rich Content Access**: Full job descriptions for analysis and cover letter generation
- **Application Tracking**: Status management and lifecycle tracking in structured CSV format
- **Data Integrity**: Guaranteed 1:1 mapping through job_id primary key

### Application Database Schema

The core application tracking database (`data/raw/advertisements.csv`) uses this schema:

```csv
job_id,company_name,job_title,source,status,priority,date_discovered,date_applied,date_closed,notes,salary_min,salary_max,location,url
```

**Field Descriptions:**
- `job_id`: 8-digit SEEK job identifier (Primary Key)
- `company_name`: Company name (normalized for cover letter matching)
- `job_title`: Job position title
- `source`: Job board source (SEEK, LinkedIn, etc.)
- `status`: Application status (discovered, interested, applied, interviewed, rejected, closed)
- `priority`: Target priority (high, medium, low)
- `date_discovered`: Date job was scraped (YYYY-MM-DD)
- `date_applied`: Date application was submitted (YYYY-MM-DD)
- `date_closed`: Date position was closed/filled (YYYY-MM-DD)
- `notes`: Free-text notes about application/company
- `salary_min/max`: Salary range if available
- `location`: Job location
- `url`: Original job posting URL

### File Naming Conventions

- **Individual Jobs**: `{job_id}_{company}_{title}.md`
  - `job_id`: 8-digit SEEK identifier (links to advertisements.csv)
  - Example: `12345678_Example_Corp_Software_Engineer.md`
- **Aggregate Reports**: `YYYYMMDD_job_descriptions_aggregate.md`
- **Cover Letters**: `{company_name}.md`

**Critical**: The `job_id` prefix in job description filenames **must match** the `job_id` field in `advertisements.csv` to maintain data integrity across the dual storage system.

### Data Integrity & Workflow

The applyr system maintains strict data integrity through its dual storage architecture:

1. **Scraping Phase**: When a job is scraped from SEEK:
   - Creates markdown file: `{job_id}_{company}_{title}.md`
   - Adds CSV entry: `{job_id},company,title,SEEK,discovered,...`

2. **Application Tracking**: Status updates modify CSV only:
   - `status` field: discovered → applied → interviewed → rejected/closed
   - Markdown files remain unchanged (preserve original job content)

3. **Data Lookup**: Any operation requiring full job details:
   - Use `job_id` from CSV to locate corresponding markdown file
   - Example: CSV shows job 12345678 → Read `12345678_Example_Corp_Software_Engineer.md`

**Validation**: The system ensures every CSV entry has a matching markdown file and vice versa.

## 💼 Usage Examples

### Supported Job Boards

applyr supports multiple job boards with automatic source detection:

| Job Board | Input Format | Import Method | Example |
|-----------|--------------|---------------|---------|
| **SEEK** | 8-digit job ID or full URL | Automatic web scraping | `12345678` or `https://www.seek.com.au/job/12345678` |
| **Employment Hero** | Full URL | Automatic web scraping | `https://jobs.employmenthero.com/AU/job/company-position-id` |
| **Indeed** | 16-char hex job ID or full URL | Manual import from text file | `cc76be5d850127ec` or `https://au.indeed.com/viewjob?jk=cc76be5d850127ec` |

**Job ID Format:**
- SEEK: 8-digit numeric ID (e.g., `12345678`)
- Employment Hero: Prefixed slug format (e.g., `eh-axcelerate-senior-software-engineer-a5y43`)
- Indeed: 16-character hexadecimal ID with `ind-` prefix (e.g., `ind-cc76be5d850127ec`)

**Indeed Manual Import:**

Indeed actively blocks web scraping (403 Forbidden errors). To add Indeed jobs, use manual import:

1. Visit the Indeed job page in your browser
2. Copy the entire page content (`Cmd+A, Cmd+C` on Mac or `Ctrl+A, Ctrl+C` on Windows/Linux)
3. Save to `data/raw/jobs/{job_id}.txt` (e.g., `data/raw/jobs/cc76be5d850127ec.txt`)
4. Run `applyr add-job {job_id}` or `applyr add-job "{url}"`

Example workflow:
```bash
# 1. Visit https://au.indeed.com/viewjob?jk=cc76be5d850127ec in browser
# 2. Press Cmd+A (Mac) or Ctrl+A (Windows/Linux) to select all
# 3. Press Cmd+C (Mac) or Ctrl+C (Windows/Linux) to copy
# 4. Save to data/raw/jobs/cc76be5d850127ec.txt
# 5. Run command:
applyr add-job cc76be5d850127ec
# or
applyr add-job "https://au.indeed.com/viewjob?jk=cc76be5d850127ec"
```

The system will parse the text file and extract job title, company, and description automatically.

### Job Market Scraping

**Single Job Analysis:**
```bash
# Scrape SEEK job by ID
applyr add-job 12345678

# Scrape SEEK job by URL
applyr add-job https://www.seek.com.au/job/12345678

# Scrape Employment Hero job
applyr add-job https://jobs.employmenthero.com/AU/job/axcelerate-senior-software-engineer-a5y43

# Add multiple jobs at once (mixed sources)
applyr add-job 12345678,https://jobs.employmenthero.com/AU/job/company-position-xyz
```

**Legacy scripts (SEEK only):**
```bash
# Scrape specific SEEK job posting
python scripts/job_scraper/seek_scraper.py --url "https://www.seek.com.au/job/12345678"

# Custom output directory
python scripts/job_scraper/seek_scraper.py --url "https://www.seek.com.au/job/12345678" --output-dir custom_analysis
```

**Batch Processing:**
```bash
# Process all URLs in job_urls.txt
python scripts/job_scraper/batch_scrape_jobs.py

# With custom delay between requests
python scripts/job_scraper/seek_scraper.py --urls-file scripts/job_scraper/job_urls.txt --delay 5.0
```

### Market Intelligence Generation

**Create Aggregate Analysis:**
```bash
# Generate today's market report
python scripts/job_scraper/aggregate_jobs.py

# Specify custom date
python scripts/job_scraper/aggregate_jobs.py --date 20250915

# Custom input/output paths
python scripts/job_scraper/aggregate_jobs.py --input-dir custom_jobs --output-file market_analysis.md
```

### Professional PDF Generation

**Resume Format Generation:**
```bash
# Generate all professional resume formats
applyr resume-formats data/raw/resume.md

# Generate specific formats only
applyr resume-formats resume.md --formats "ats"

# Custom output directory
applyr resume-formats resume.md --output-dir pdfs/resumes/
```

**Individual File Conversion:**
```bash
# Basic conversion with automatic template
applyr pdf data/outputs/cover_letters/example_company.md

# ATS-optimized styling
applyr pdf cover_letter.md --style ats

# ATS-optimized format
applyr pdf resume.md --style ats

# Custom output location
applyr pdf README.md --output docs/README.pdf
```

**Batch Processing:**
```bash
# Convert all cover letters with progress tracking
applyr pdf data/outputs/cover_letters --batch

# Convert job descriptions with ATS styling
applyr pdf data/outputs/job_descriptions --batch --style ats

# Custom output directory with specific template
applyr pdf data/outputs/cover_letters --batch --output pdfs/cover_letters/ --style ats
```

**Quality Validation:**
```bash
# Basic PDF validation
applyr validate-pdf resume_ats.pdf

# Detailed analysis with optimization recommendations
applyr validate-pdf resume_ats.pdf --detailed
```

### Application Tracking

**View Application Status:**
```bash
# View all jobs in pipeline
applyr status

# Filter by status
applyr status --filter applied
applyr status --filter discovered

# Limit results
applyr status --limit 20
```

**Update Job Status:**
```bash
# Mark job as applied
applyr update-status 12345678 applied

# Mark job as rejected
applyr update-status 12345678 rejected

# Mark as interviewed
applyr update-status 12345678 interviewed
```

**Search and Filter Jobs:**
```bash
# Search by company
applyr jobs --company "Example Corp"

# Filter by status
applyr jobs --status applied

# Combined filters
applyr jobs --company "Tech Solutions Ltd" --status discovered

# Show more results
applyr jobs --limit 100
```

**Application Statistics:**
```bash
# View comprehensive stats
applyr stats

# Clean up old jobs (30+ days old, closed/rejected)
applyr cleanup --days 30

# Skip confirmation
applyr cleanup --days 30 --confirm
```

## 📊 Market Intelligence Features

### Technology Trend Analysis
Current market insights from 25+ analyzed positions:

**Most In-Demand Technologies:**
- **React**: 20+ mentions (80% of positions)
- **TypeScript**: 14+ mentions (56% of positions)
- **Node.js**: 15+ mentions (60% of positions)
- **AWS**: 15+ mentions (60% of positions)
- **JavaScript**: 16+ mentions (64% of positions)

### Job Market Insights

**Role Level Distribution:**
- **Senior Level**: 7 positions (28%)
- **Mid-Level**: 15 positions (60%)
- **Junior**: 1 position (4%)
- **Lead/Principal**: 2 positions (8%)

**Active Hiring Companies:**
- Example Corp, Acme Inc, Tech Solutions Ltd (leading volume)
- Strong presence in SaaS, Fintech, Healthcare Tech
- Geographic concentration in Brisbane/Sydney/Melbourne

**Emerging Trends:**
- AI/ML integration capabilities increasingly mentioned
- Cloud-native architecture emphasis (AWS dominance)
- Modern frontend preferences (React + TypeScript)
- DevOps and automation skills in high demand

## 📝 Sample Outputs

### Aggregate Report Structure
```markdown
# Job Descriptions Aggregate - 2025-09-12

**Generated:** 2025-09-12 14:09:56  
**Total Jobs:** 7  
**Unique Companies:** 7  
**Source:** SEEK Job Scraper  

## Summary Statistics
- **Total Job Postings:** 7
- **Unique Companies:** 7

### Technology Mentions
- **React:** 5 mentions
- **Node:** 4 mentions
- **TypeScript:** 3 mentions

## Table of Contents
[Indexed list of all positions with anchor links]

## Job Descriptions
[Complete job descriptions with preserved metadata]
```

### Individual Job Format
```markdown
# Software Engineer

**Company:** Example Corp  
**Job ID:** 12345678  
**Source:** SEEK  
**Scraped:** 2025-01-15 10:30:00

---

[Clean job description content without headers, footers, or unwanted sections]
```

### Cover Letter Example
```markdown
Dear Example Corp Hiring Team,

I am excited to apply for the Software Engineer position. Your focus on modern web technologies and innovative solutions aligns perfectly with my experience and interests.

[Personalized content based on company research and job requirements]

John Smith
johnsmith.dev
```

## 🛠 Technical Details

### Python Architecture
- **Core Engine**: `seek_scraper.py` (435 lines) - Main scraping logic
- **Aggregation**: `aggregate_jobs.py` (420 lines) - Market intelligence generation
- **PDF Converter**: `pdf_converter.py` (534 lines) - WeasyPrint-based PDF generation with quality validation
- **CLI Interface**: `cli.py` (787 lines) - Comprehensive command-line interface with 11 commands
- **Batch Processing**: `batch_scrape_jobs.py` - Automated workflow execution
- **Testing Suite**: `test_single_job.py`, `test_aggregator.py`, `test_pdf_converter.py` - Quality assurance

### PDF Generation Architecture
- **WeasyPrint Engine**: Professional HTML/CSS to PDF conversion with font embedding support
- **Template System**: 6 custom CSS templates with consistent brand integration
- **SVG Brand Text**: Vector-based configurable brand text ensuring perfect font consistency
- **Link Preservation**: Maintains clickable links in PDF output with proper href handling
- **Quality Metrics**: File size analysis, optimization recommendations, and quality scoring
- **Font Integration**: Support for Google Fonts, system fonts, and custom font files
- **Print Optimization**: Proper page breaks, margins, headers, footers for professional printing

### Anti-Bot Measures
- Custom browser headers and user-agent spoofing
- Respectful scraping with 2-3 second delays between requests
- 403 detection and graceful error handling
- Content filtering and cleaning algorithms

### Data Processing Features
- **Metadata Extraction**: Job titles, company names, IDs, timestamps
- **Content Filtering**: Removes headers, footers, ads, warning sections
- **Quality Assurance**: Duplicate detection, content validation
- **Error Handling**: Network failures, parsing errors, file save issues

## 📂 Project Structure

```
applyr/
├── README.md                   # This comprehensive documentation
├── docs/CLAUDE.md             # AI assistant guidance with PDF implementation details
├── LICENSE                     # Project license
├── pyproject.toml              # Poetry configuration
├── poetry.lock                 # Poetry lock file
├── applyr/                     # Main application package
│   ├── __init__.py
│   ├── cli.py                  # CLI interface with Typer (11 commands, 787 lines)
│   ├── database.py             # Application tracking database
│   ├── pdf_converter.py        # PDF conversion module (534 lines)
│   ├── scraper.py              # Job scraping functionality
│   ├── batch.py                # Batch processing
│   ├── aggregator.py           # Market intelligence
│   └── styles/                 # Professional CSS templates with SVG brand integration
│       ├── ats.css             # ATS-optimized format
│       └── technical.css       # Technical documentation style (if exists)
├── tests/                      # Comprehensive test suite
│   ├── __init__.py
│   ├── conftest.py             # Shared fixtures and test utilities
│   ├── test_utils.py            # Helper functions for test data
│   ├── test_database.py        # Database operation tests
│   ├── test_cli.py             # CLI command tests
│   ├── test_pdf_converter.py   # PDF converter tests
│   ├── test_ats_analyzer.py    # ATS analyzer comprehensive tests
│   ├── test_ats_scoring.py      # ATS scoring engine tests
│   ├── test_ats_parsers.py     # Document parser tests
│   ├── test_ats_keywords.py    # Keyword analyzer tests
│   ├── test_ats_output.py      # ATS output formatter tests
│   ├── test_scraper.py         # SEEK scraper tests
│   ├── test_scraper_base.py    # Base scraper tests
│   ├── test_scraper_factory.py # Scraper factory tests
│   ├── test_scraper_linkedin_manual.py  # LinkedIn parser tests
│   ├── test_employment_hero_scraper.py  # Employment Hero tests
│   ├── test_indeed_manual_parser.py     # Indeed parser tests
│   ├── test_aggregator.py      # Job aggregator tests
│   ├── test_batch.py            # Batch processing tests
│   ├── test_config.py           # Configuration tests
│   └── test_integration.py      # End-to-end integration tests
├── data/                       # All output data
│   └── outputs/
│       ├── job_descriptions/   # Latest job analysis
│       ├── job_descriptions_1/ # Previous batch
│       └── cover_letters/      # Personalized letters
└── scripts/                    # Processing tools
    └── job_scraper/
        ├── README.md           # Detailed scraper docs
        ├── seek_scraper.py     # Core scraping engine
        ├── aggregate_jobs.py   # Market intelligence
        ├── batch_scrape_jobs.py# Batch processing
        ├── test_single_job.py  # Single job testing
        ├── test_aggregator.py  # Aggregation testing
        └── job_urls.txt        # URL queue management
```

## 🔧 Development

### Getting Started
1. **Clone the repository**
2. **Install Poetry** (if not already installed): `pip install poetry`
3. **Install dependencies**: `poetry install`
4. **Activate virtual environment**: `poetry shell`
5. **Add job URLs** to `scripts/job_scraper/job_urls.txt`
6. **Run batch processing**: `applyr batch` or `python scripts/job_scraper/batch_scrape_jobs.py`
7. **Generate analysis**: `applyr aggregate` or `python scripts/job_scraper/aggregate_jobs.py`
8. **Convert to PDF**: `applyr pdf <markdown-file>` or `applyr resume-formats <resume.md>`
9. **Validate PDF quality**: `applyr validate-pdf <pdf-file> --detailed`

### Testing

applyr has a comprehensive test suite covering all core modules. See [docs/TESTING.md](docs/TESTING.md) for detailed testing documentation.

**Quick Test Commands:**
```bash
# Run all tests with coverage
pytest

# Run tests with verbose output
pytest -v

# Run specific test file
pytest tests/test_ats_analyzer.py -v

# Run with coverage report
pytest --cov=applyr --cov-report=html

# Test specific module
pytest tests/test_pdf_converter.py -v
pytest tests/test_database.py -v
```

**Test Coverage:**
- **Target**: 50%+ overall coverage
- **Coverage Reports**: Generated in HTML, terminal, and XML formats
- **CI Integration**: Tests run automatically on every push via GitHub Actions
- **Test Suite**: Comprehensive coverage of ATS modules, scrapers, utilities, and integration workflows

**Test Organization:**
- **ATS Tests**: `test_ats_*.py` (analyzer, scoring, parsers, keywords, output)
- **Scraper Tests**: `test_scraper*.py` (SEEK, base, factory, LinkedIn, Employment Hero, Indeed)
- **Core Tests**: `test_database.py`, `test_cli.py`, `test_pdf_converter.py`, `test_aggregator.py`, `test_batch.py`, `test_config.py`
- **Integration Tests**: `test_integration.py` (end-to-end workflows)

See [docs/TESTING.md](docs/TESTING.md) for complete test documentation and [docs/CI_CD.md](docs/CI_CD.md) for CI workflow details.

### Code Quality & Formatting

applyr uses **Ruff** for linting and formatting, **mypy** for type checking, and **bandit** for security scanning. Pre-commit hooks automatically enforce code quality standards.

**Quick Commands:**
```bash
# Format all code
make format

# Run all quality checks
make all

# Individual checks
make lint          # Lint with Ruff
make type-check    # Type checking with mypy
make security      # Security scan with bandit
make test          # Run tests with coverage

# Install pre-commit hooks (runs on every commit)
make install
```

**Pre-commit Hooks:**
Pre-commit hooks automatically run on every commit:
- ✅ Format code with Ruff
- ✅ Run linting checks
- ✅ Type checking with mypy
- ✅ Security scanning with bandit
- ✅ Validate YAML/JSON/TOML files
- ✅ Check for merge conflicts and trailing whitespace

**Manual Checks:**
```bash
# Format code
ruff format .

# Lint code (auto-fix where possible)
ruff check --fix .

# Type checking
mypy applyr/

# Security scanning
bandit -r applyr/

# Run pre-commit on all files
pre-commit run --all-files
```

**Configuration:**
- **Ruff**: Configured in `pyproject.toml` (line length: 120, Python 3.9+)
- **mypy**: Gradual typing approach (strict mode for new code)
- **bandit**: Security scanning with test exclusions
- **Pre-commit**: Hook configuration in `.pre-commit-config.yaml`

## ⚠️ Terms of Service & Legal Compliance

**Important**: Web scraping may violate website Terms of Service. applyr is designed for **personal, non-commercial use only** with respectful scraping practices:

### Responsible Use Guidelines
- ✅ **Personal job tracking**: Individual applications and career research
- ✅ **Respectful rate limiting**: 2+ second delays between requests (configurable)
- ✅ **Minimal impact**: Small-scale scraping for personal applications
- ✅ **Transparency**: Standard headers, no circumvention of security
- ❌ **No bulk scraping**: Not for creating job databases or commercial use
- ❌ **No republishing**: Do not redistribute or sell scraped content
- ❌ **No circumvention**: Respect 403/blocking responses

### Legal Considerations
All supported job boards have Terms of Service that may restrict automated scraping:
- **SEEK**: Restricts automated access; offers partner APIs
- **Employment Hero**: Likely restricts automated access
- **Indeed**: Prohibits automated scraping (see manual import method below)

**You use this tool at your own risk.** See `docs/TERMS_OF_SERVICE.md` for detailed legal information, ToS summaries, and official API alternatives.

### Indeed Manual Import Support

Indeed actively blocks web scraping attempts (403 errors) and explicitly prohibits automated scraping in their Terms of Service. applyr supports Indeed via **manual import** instead:

**How it works:**
1. **No automated scraping**: User manually copies job page content in their browser
2. **Text file processing**: System parses the copied text to extract job data
3. **ToS compliant**: Manual copying by the user is not prohibited
4. **Bypasses blocking**: No HTTP requests to Indeed, so no 403 errors

**Why official API isn't used:**
- **No job search/retrieval API**: APIs only support posting jobs TO Indeed (not retrieving listings)
- **Partner-only access**: Requires business partnership agreements (not available to individuals)
- **Commercial pricing**: Undisclosed pricing, designed for ATS/recruitment platforms at enterprise scale
- **ATS focus**: Built for employers and recruitment platforms, not job seekers

**Trade-offs:**
- ✅ **Pros**: ToS compliant, no blocking, integrates with applyr's job tracking
- ⚠️ **Cons**: Requires manual copy/paste step (not fully automated)

See the "Indeed Manual Import" section above for detailed usage instructions.

### Built-in Protections
- **ToS warnings**: Displayed on first use per source
- **Rate limiting**: Enforced delays between requests
- **Error handling**: Graceful handling of blocking/403 responses
- **Logging**: Transparent activity tracking

For commercial use or large-scale operations, contact job boards about official API access.

---

### Extension Points
- **Additional Job Boards**: Extend scraping to LinkedIn, Stack Overflow Jobs (with ToS compliance)
- **Enhanced Analytics**: Machine learning for salary prediction, skill matching
- **API Integration**: RESTful API for programmatic access
- **Real-time Alerts**: Notification system for new matching positions
- **Cover Letter Optimization**: A/B testing and response rate tracking
- **Additional PDF Templates**: Industry-specific templates (tech, finance, creative)
- **Interactive PDFs**: Form fields and interactive elements for digital applications
- **Multi-language Support**: PDF generation with international character sets

## 🎯 Application Workflow

applyr provides an integrated workflow from job discovery to application tracking:

### 1. Discovery Phase
```bash
# Scrape new jobs (automatically added to database)
applyr scrape --url "https://www.seek.com.au/job/12345678"

# View discovered jobs
applyr status --filter discovered
```

### 2. Research & Prioritization
```bash
# Review jobs and set priorities
applyr jobs --company "Example Corp"

# Search and filter opportunities
applyr jobs --status discovered --company "Tech Solutions Ltd"
```

### 3. Application Phase
```bash
# Generate targeted cover letter using existing tools
# (covers company research and customization)

# Mark as applied when submitted
applyr update-status 12345678 applied
```

### 4. Follow-up & Tracking
```bash
# Update status as you progress through interviews
applyr update-status 12345678 interviewed
applyr update-status 12345678 rejected

# Analyze success rates and patterns
applyr stats
```

### 5. Continuous Optimization
```bash
# Export reports to PDF for review meetings
applyr pdf README.md --style ats

# Clean up old applications periodically
applyr cleanup --days 30
```

## 📖 Complete CLI Reference

applyr provides 11 comprehensive commands for complete job search workflow management:

### Core Commands

| Command | Purpose | Example |
|---------|---------|----------|
| `scrape` | Scrape individual or batch job URLs | `applyr scrape --url https://seek.com.au/job/12345678` |
| `batch` | Process multiple jobs from file | `applyr batch --urls-file job_urls.txt --delay 3.0` |
| `aggregate` | Generate market intelligence reports | `applyr aggregate --input-dir job_descriptions/` |
| `add-job` | Add job by ID or URL (SEEK/Employment Hero) | `applyr add-job 12345678` or `applyr add-job https://jobs.employmenthero.com/...` |

### PDF Generation Commands

| Command | Purpose | Example |
|---------|---------|----------|
| `pdf` | Convert markdown to PDF with templates | `applyr pdf resume.md --style ats` |
| `resume-formats` | Generate resume formats | `applyr resume-formats resume.md --formats "ats"` |
| `validate-pdf` | Analyze PDF quality and optimization | `applyr validate-pdf resume.pdf --detailed` |

### Application Management Commands

| Command | Purpose | Example |
|---------|---------|----------|
| `status` | View application pipeline | `applyr status --filter applied --limit 20` |
| `update-status` | Change job application status | `applyr update-status 12345678 interviewed` |
| `jobs` | Search and filter job database | `applyr jobs --company "Tech Solutions Ltd" --status discovered` |
| `stats` | Application success rates and analytics | `applyr stats` |
| `cleanup` | Remove old closed/rejected jobs | `applyr cleanup --days 30 --confirm` |

### Template Options

The `resume-formats` command supports these professional templates:

- **ats**: Applicant Tracking System optimized format
- **ats_docx**: DOCX conversion optimized format

### Quality Validation Features

The PDF validation system provides:

- **File Size Analysis**: Optimal (200KB), Good (500KB), Large (1MB+) classifications
- **Quality Scoring**: 0-10 scale based on size, structure, and metadata
- **Optimization Recommendations**: Template suggestions and size reduction tips
- **Metadata Extraction**: Page count, encryption status, embedded fonts
- **Print Readiness**: Margin, page break, and formatting validation

---

**applyr** provides powerful job market intelligence to optimize your career strategy. Transform your job search from reactive to proactive with data-driven insights, automated application tracking, and personalized cover letter generation.
