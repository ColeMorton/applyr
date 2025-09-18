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
- `applyr/styles/` - 6 professional CSS templates with SVG brand integration
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
- **6 professional PDF templates**: sensylate, executive, ats, professional, minimal, heebo-premium
- **SVG brand text integration** with centered, 2x-sized "Cole Morton" branding
- **Market intelligence** on technology demand and company hiring patterns

## PDF Generation System

applyr includes a comprehensive PDF generation system built on WeasyPrint with professional styling capabilities:

### PDF Templates Available

1. **sensylate.css**: Brand-consistent design mirroring colemorton.com with perfect color/typography alignment
2. **executive.css**: High-impact design with modern typography and visual elements 
3. **ats.css**: ATS-optimized format for applicant tracking systems
4. **professional.css**: Balanced professional styling for general use
5. **minimal.css**: Clean, simple formatting for minimalist preference
6. **heebo-premium.css**: Premium design showcasing variable Heebo font features

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
applyr pdf resume.md --css-file applyr/styles/executive.css

# Validate PDF quality
applyr validate-pdf resume_executive.pdf --detailed
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