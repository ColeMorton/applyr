# Manual Job Import Directory

This directory stores manually copied job page content for import into applyr. Jobs are organized by source in subdirectories.

## Why Manual Import?

Some job boards actively block web scraping or have restrictive APIs. Manual import bypasses these restrictions while remaining compliant with Terms of Service:

- **Indeed**: Blocks web scraping (403 Forbidden errors)
- **LinkedIn**: Blocks automated requests (999 status code)
- **Manual Import**: Reliable, compliant, and works 100% of the time

## Directory Structure

```
data/raw/jobs/
├── indeed/           # Indeed job text files
│   ├── cc76be5d850127ec.txt
│   └── a1b2c3d4e5f6g7h8.txt
├── linked_in/        # LinkedIn job text files
│   ├── 4258805835.txt
│   └── 4258805836.txt
└── README.md
```

## How to Import an Indeed Job

### Step 1: Visit the Job Page

Open the Indeed job posting in your browser, for example:
```
https://au.indeed.com/viewjob?jk=cc76be5d850127ec
```

### Step 2: Copy the Entire Page Content

**On Mac:**
- Press `Cmd+A` to select all
- Press `Cmd+C` to copy

**On Windows/Linux:**
- Press `Ctrl+A` to select all
- Press `Ctrl+C` to copy

### Step 3: Save to Text File

Create a text file named with the job ID (the `jk` parameter from the URL) in the `indeed/` subdirectory:

```
data/raw/jobs/indeed/cc76be5d850127ec.txt
```

Paste the copied content into this file and save it.

### Step 4: Import via CLI

Run the applyr command with the job ID or full URL:

```bash
# Using job ID
applyr add-job cc76be5d850127ec

# Using full URL (remember to quote it)
applyr add-job "https://au.indeed.com/viewjob?jk=cc76be5d850127ec"
```

## How to Import a LinkedIn Job

### Step 1: Visit the Job Page

Open the LinkedIn job posting in your browser, for example:
```
https://www.linkedin.com/jobs/view/4258805835/
```

### Step 2: Copy the Entire Page Content

**On Mac:**
- Press `Cmd+A` to select all
- Press `Cmd+C` to copy

**On Windows/Linux:**
- Press `Ctrl+A` to select all
- Press `Ctrl+C` to copy

### Step 3: Save to Text File

Create a text file named with the job ID in the `linked_in/` subdirectory:

```
data/raw/jobs/linked_in/4258805835.txt
```

Paste the copied content into this file and save it.

### Step 4: Import via CLI

Run the applyr command with the job ID or full URL:

```bash
# Using job ID
applyr add-job 4258805835

# Using full URL
applyr add-job https://www.linkedin.com/jobs/view/4258805835/
```

## File Naming Convention

Text files must be named using the job ID and placed in the appropriate subdirectory:

**Indeed jobs:**
```
indeed/{job_id}.txt
```
Examples:
- `indeed/cc76be5d850127ec.txt`
- `indeed/a1b2c3d4e5f6g7h8.txt`

**LinkedIn jobs:**
```
linked_in/{job_id}.txt
```
Examples:
- `linked_in/4258805835.txt`
- `linked_in/4258805836.txt`

## What Gets Extracted

The parsers extract:

**Indeed jobs:**
- **Job Title** - Usually the first substantial text on the page
- **Company Name** - Often appears near the title with location info
- **Job Description** - Main body of the job posting

**LinkedIn jobs:**
- **Job Title** - First substantial line, skipping navigation text
- **Company Name** - Extracted from early lines or "Company hiring Title" patterns
- **Location** - City, State, Country format
- **Job Description** - Complete "About the job" section with requirements, responsibilities, and benefits

## Privacy Note

Text files in this directory are automatically ignored by Git (see `.gitignore`). Your manually saved job content will not be committed to version control.

## Alternative: Automated Job Boards

For SEEK and Employment Hero jobs, web scraping works normally without manual steps:

```bash
# SEEK - fully automated
applyr add-job 87066700

# Employment Hero - fully automated
applyr add-job https://jobs.employmenthero.com/AU/job/company-position-id
```

### LinkedIn Manual Import Only

LinkedIn has strong anti-scraping measures and blocks automated requests with a 999 status code. **LinkedIn jobs require manual import only** - there is no automated scraping option.

**LinkedIn URL formats supported:**
- Full URL: `https://www.linkedin.com/jobs/view/4258805835/`
- Job ID only: `4258805835` (will be converted to full URL)

**When you try to add a LinkedIn job without a manual import file, the CLI will show:**
```
❌ LinkedIn requires manual import. Please save the job page to data/raw/jobs/linked_in/{job_id}.txt and run the command again.
```

