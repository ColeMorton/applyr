# applyr

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
- **25+ job postings analyzed** from SEEK across 23 Australian companies
- **Automated scraping** with anti-bot measures and respectful rate limiting
- **Structured data extraction** with metadata preservation and timestamps
- **Batch processing** capabilities for efficient data collection

### Market Intelligence & Analytics
- **Technology trend analysis**: Identifies most in-demand skills (React, TypeScript, Node.js, AWS)
- **Job level distribution**: Analyzes role seniority patterns (Senior 28%, Mid-level 60%, Junior 4%)
- **Company hiring patterns**: Tracks which companies are actively hiring and job volumes
- **Geographic insights**: Brisbane, Sydney, Melbourne market analysis
- **Salary intelligence**: Limited salary data extraction where available

### Cover Letter Generation
- **9+ personalized cover letters** generated for target companies
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

### PDF Export Capabilities
- **Markdown to PDF conversion** with professional formatting
- **Custom CSS styling** support for personalized document appearance
- **Batch PDF generation** for entire directories of markdown files
- **Pre-built style templates** including professional and minimal themes
- **Page numbering and formatting** optimized for printing and sharing

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

# Convert with custom CSS
applyr pdf README.md --css-file applyr/styles/professional.css

# Batch convert entire directory
applyr pdf data/outputs/cover_letters --batch --output output_pdfs/
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
        ├── squiz.md
        ├── trilogy_care.md
        └── [company-specific letters]
```

### Data Relationship Model

The system maintains a **1:1 correspondence** between job descriptions and advertisement tracking records:

- **Job Descriptions** (`data/outputs/job_descriptions/*.md`): Full job posting content in markdown format
- **Advertisements** (`data/raw/advertisements.csv`): Application tracking database with status management

**Key Relationship**: Both are linked by `job_id` - the 8-digit SEEK identifier that serves as the primary key across both data sources.

**Example**:
- Job Description: `87066700_iSelect_Ltd_Software_Engineer.md`
- CSV Record: `87066700,iSelect Ltd,Software Engineer,SEEK,applied,medium,...`

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
  - Example: `87066700_iSelect_Ltd_Software_Engineer.md`
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
   - Example: CSV shows job 87066700 → Read `87066700_iSelect_Ltd_Software_Engineer.md`

**Validation**: The system ensures every CSV entry has a matching markdown file and vice versa.

## 💼 Usage Examples

### Job Market Scraping

**Single Job Analysis:**
```bash
# Scrape specific SEEK job posting
python scripts/job_scraper/seek_scraper.py --url "https://www.seek.com.au/job/87066700"

# Custom output directory
python scripts/job_scraper/seek_scraper.py --url "https://www.seek.com.au/job/87066700" --output-dir custom_analysis
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

### PDF Generation

**Convert Individual Files:**
```bash
# Basic conversion
applyr pdf data/outputs/cover_letters/squiz.md

# With professional styling
applyr pdf data/outputs/cover_letters/squiz.md --css-file applyr/styles/professional.css

# Custom output location
applyr pdf README.md --output docs/README.pdf

# Inline CSS styling
applyr pdf README.md --css "body { font-family: Georgia; }"
```

**Batch PDF Conversion:**
```bash
# Convert all cover letters to PDFs
applyr pdf data/outputs/cover_letters --batch

# Convert job descriptions with minimal styling
applyr pdf data/outputs/job_descriptions --batch --css-file applyr/styles/minimal.css

# Custom output directory
applyr pdf data/outputs/cover_letters --batch --output pdfs/cover_letters/
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
applyr update-status 87066700 applied

# Mark job as rejected
applyr update-status 87066700 rejected

# Mark as interviewed
applyr update-status 87066700 interviewed
```

**Search and Filter Jobs:**
```bash
# Search by company
applyr jobs --company "iSelect"

# Filter by status
applyr jobs --status applied

# Combined filters
applyr jobs --company "Squiz" --status discovered

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
- Squiz, iSelect, Felix Software (leading volume)
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

**Company:** Squiz Australia Pty Ltd  
**Job ID:** 86398474  
**Source:** SEEK  
**Scraped:** 2025-09-02 14:06:20

---

[Clean job description content without headers, footers, or unwanted sections]
```

### Cover Letter Example
```markdown
Dear Squiz Hiring Team,

I can see that you're rapidly expanding the DXP team, and seeking people proficient in Node, TypeScript, React, Git and CI/CD. This stack is my bread-and-butter, representing my deepest experience and greatest strengths.

[Personalized content based on company research and job requirements]

Cole Morton
colemorton.com
```

## 🛠 Technical Details

### Python Architecture
- **Core Engine**: `seek_scraper.py` (435 lines) - Main scraping logic
- **Aggregation**: `aggregate_jobs.py` (420 lines) - Market intelligence generation
- **Batch Processing**: `batch_scrape_jobs.py` - Automated workflow execution
- **Testing Suite**: `test_single_job.py`, `test_aggregator.py` - Quality assurance

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
├── README.md                   # This documentation
├── CLAUDE.md                   # AI assistant guidance
├── LICENSE                     # Project license
├── pyproject.toml              # Poetry configuration
├── poetry.lock                 # Poetry lock file
├── applyr/                     # Main application package
│   ├── __init__.py
│   ├── cli.py                  # CLI interface with Typer
│   ├── database.py             # Application tracking database
│   ├── pdf_converter.py        # PDF conversion module
│   ├── scraper.py              # Job scraping functionality
│   ├── batch.py                # Batch processing
│   ├── aggregator.py           # Market intelligence
│   └── styles/                 # CSS templates for PDFs
│       ├── professional.css    # Professional PDF style
│       └── minimal.css         # Minimal PDF style
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── test_database.py        # Database operation tests
│   └── test_pdf_converter.py   # PDF converter tests
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
8. **Convert to PDF**: `applyr pdf <markdown-file>`

### Testing
```bash
# Run all tests with pytest
pytest

# Test PDF converter specifically
pytest tests/test_pdf_converter.py

# Test database operations
pytest tests/test_database.py

# Test single job processing
python scripts/job_scraper/test_single_job.py

# Test aggregation functionality  
python scripts/job_scraper/test_aggregator.py
```

### Extension Points
- **Additional Job Boards**: Extend scraping to Indeed, LinkedIn, Stack Overflow Jobs
- **Enhanced Analytics**: Machine learning for salary prediction, skill matching
- **API Integration**: RESTful API for programmatic access
- **Real-time Alerts**: Notification system for new matching positions
- **Cover Letter Optimization**: A/B testing and response rate tracking

### Current Limitations
- **Single Source**: Currently SEEK-only (Australian market focus)
- **Manual URL Management**: Job URLs added manually to `job_urls.txt`
- **Batch Processing**: No real-time processing capabilities

## 🎯 Application Workflow

applyr provides an integrated workflow from job discovery to application tracking:

### 1. Discovery Phase
```bash
# Scrape new jobs (automatically added to database)
applyr scrape --url "https://www.seek.com.au/job/87066700"

# View discovered jobs
applyr status --filter discovered
```

### 2. Research & Prioritization
```bash
# Review jobs and set priorities
applyr jobs --company "iSelect"

# Search and filter opportunities
applyr jobs --status discovered --company "Squiz"
```

### 3. Application Phase
```bash
# Generate targeted cover letter using existing tools
# (covers company research and customization)

# Mark as applied when submitted
applyr update-status 87066700 applied
```

### 4. Follow-up & Tracking
```bash
# Update status as you progress through interviews
applyr update-status 87066700 interviewed
applyr update-status 87066700 rejected

# Analyze success rates and patterns
applyr stats
```

### 5. Continuous Optimization
```bash
# Export reports to PDF for review meetings
applyr pdf README.md --css-file applyr/styles/professional.css

# Clean up old applications periodically
applyr cleanup --days 30
```

---

**applyr** provides powerful job market intelligence to optimize your career strategy. Transform your job search from reactive to proactive with data-driven insights, automated application tracking, and personalized cover letter generation.