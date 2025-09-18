#!/usr/bin/env python3
"""applyr CLI - Main command line interface using Typer and Rich"""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.progress import track
from rich.table import Table
from rich import print as rprint

from . import __version__

app = typer.Typer(
    name="applyr",
    help="🚀 Intelligent Job Market Analysis Toolkit",
    rich_markup_mode="rich"
)
console = Console()

def version_callback(value: bool):
    if value:
        rprint(f"[bold blue]applyr[/bold blue] version [green]{__version__}[/green]")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None, "--version", "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit"
    ),
):
    """🚀 Intelligent Job Market Analysis Toolkit
    
    Extract job market intelligence, scrape postings, and generate targeted cover letters.
    """
    pass

@app.command("scrape")
def scrape_command(
    url: Optional[str] = typer.Option(
        None, "--url", "-u", 
        help="Single SEEK job URL to scrape"
    ),
    urls_file: Optional[Path] = typer.Option(
        None, "--urls-file", "-f",
        help="File containing SEEK URLs (one per line)"
    ),
    output_dir: Path = typer.Option(
        "data/outputs/job_descriptions", "--output-dir", "-o",
        help="Output directory for markdown files"
    ),
    delay: float = typer.Option(
        2.0, "--delay", "-d",
        help="Delay between requests in seconds"
    ),
):
    """🔍 Scrape job descriptions from SEEK URLs
    
    Extract structured job data with anti-bot measures and respectful rate limiting.
    """
    from .scraper import scrape_jobs
    from .database import ApplicationDatabase
    
    if not url and not urls_file:
        console.print("[red]❌ Error: Must provide either --url or --urls-file[/red]")
        raise typer.Exit(1)
    
    console.print(f"[bold blue]🚀 Starting job scraping with {delay}s delay[/bold blue]")
    
    urls = []
    if url:
        urls = [url]
    elif urls_file:
        try:
            with open(urls_file, 'r') as f:
                urls = [line.strip() for line in f if line.strip()]
        except Exception as e:
            console.print(f"[red]❌ Error reading URLs file: {e}[/red]")
            raise typer.Exit(1)
    
    if not urls:
        console.print("[red]❌ Error: No URLs to process[/red]")
        raise typer.Exit(1)
    
    # Initialize database for job tracking
    database = ApplicationDatabase(console=console)
    
    results = scrape_jobs(urls, output_dir, delay, console, database)
    
    successful = sum(1 for success in results.values() if success)
    failed = len(results) - successful
    
    table = Table(title="📊 Scraping Results")
    table.add_column("Metric", style="cyan")
    table.add_column("Count", style="green")
    
    table.add_row("Total Jobs", str(len(results)))
    table.add_row("Successful", str(successful))
    table.add_row("Failed", str(failed))
    
    console.print(table)
    
    if failed > 0:
        console.print("\n[red]❌ Failed URLs:[/red]")
        for url, success in results.items():
            if not success:
                console.print(f"  • [red]{url}[/red]")
    
    if successful > 0:
        console.print(f"\n[green]✅ Job descriptions saved to: {output_dir}[/green]")
    
    if failed > 0:
        raise typer.Exit(1)

@app.command("batch")
def batch_command(
    urls_file: Path = typer.Option(
        "scripts/job_scraper/job_urls.txt", "--urls-file", "-f",
        help="File containing SEEK URLs (one per line)"
    ),
    output_dir: Path = typer.Option(
        "data/outputs/job_descriptions", "--output-dir", "-o",
        help="Output directory for markdown files"
    ),
    delay: float = typer.Option(
        3.0, "--delay", "-d",
        help="Delay between requests in seconds (respectful scraping)"
    ),
):
    """📦 Batch process multiple job URLs from file
    
    Process all job URLs with progress tracking and summary reporting.
    """
    from .batch import batch_process_jobs
    
    if not urls_file.exists():
        console.print(f"[red]❌ Error: URLs file not found: {urls_file}[/red]")
        raise typer.Exit(1)
    
    console.print(f"[bold blue]📦 Starting batch processing from {urls_file}[/bold blue]")
    
    success = batch_process_jobs(urls_file, output_dir, delay, console)
    
    if not success:
        raise typer.Exit(1)

@app.command("aggregate")
def aggregate_command(
    input_dir: Path = typer.Option(
        "data/outputs/job_descriptions", "--input-dir", "-i",
        help="Input directory containing job description files"
    ),
    output_file: Optional[Path] = typer.Option(
        None, "--output-file", "-o",
        help="Output file path (default: auto-generated with date)"
    ),
    date: Optional[str] = typer.Option(
        None, "--date", "-d",
        help="Date for filename in YYYYMMDD format (default: today)"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v",
        help="Enable verbose logging"
    ),
):
    """📈 Generate market intelligence from job descriptions
    
    Analyze scraped jobs to create comprehensive market reports with technology trends and statistics.
    """
    from .aggregator import aggregate_job_data
    
    if not input_dir.exists():
        console.print(f"[red]❌ Error: Input directory not found: {input_dir}[/red]")
        raise typer.Exit(1)
    
    console.print(f"[bold blue]📈 Aggregating job data from {input_dir}[/bold blue]")
    
    success = aggregate_job_data(input_dir, output_file, date, verbose, console)
    
    if not success:
        raise typer.Exit(1)

@app.command("pdf")
def pdf_command(
    input_path: Path = typer.Argument(
        ...,
        help="Input markdown/HTML file or directory containing markdown/HTML files"
    ),
    output: Optional[Path] = typer.Option(
        None, "--output", "-o",
        help="Output PDF file or directory (default: same name as input with .pdf extension)"
    ),
    css_file: Optional[Path] = typer.Option(
        None, "--css-file", "-c",
        help="Custom CSS file for styling the PDF"
    ),
    css_string: Optional[str] = typer.Option(
        None, "--css", "-s",
        help="Inline CSS string for styling the PDF"
    ),
    batch: bool = typer.Option(
        False, "--batch", "-b",
        help="Process all markdown and HTML files in a directory"
    ),
):
    """📄 Convert markdown and HTML files to PDF with custom CSS styling
    
    Supports single file conversion or batch processing of entire directories.
    """
    from .pdf_converter import PDFConverter
    
    converter = PDFConverter(console)
    
    if batch or input_path.is_dir():
        # Batch conversion
        if not input_path.is_dir():
            console.print(f"[red]❌ Error: {input_path} is not a directory[/red]")
            raise typer.Exit(1)
            
        output_dir = output or input_path.parent / f"{input_path.name}_pdfs"
        
        console.print(f"[bold blue]📦 Batch converting markdown and HTML files from {input_path}[/bold blue]")
        
        results = converter.batch_convert(
            input_path,
            output_dir,
            css_file,
            css_string
        )
        
        successful = sum(1 for success in results.values() if success)
        failed = len(results) - successful
        
        table = Table(title="📊 Conversion Results")
        table.add_column("Metric", style="cyan")
        table.add_column("Count", style="green")
        
        table.add_row("Total Files", str(len(results)))
        table.add_row("Successful", str(successful))
        table.add_row("Failed", str(failed))
        
        console.print(table)
        
        if successful > 0:
            console.print(f"\n[green]✅ PDFs saved to: {output_dir}[/green]")
            
        if failed > 0:
            raise typer.Exit(1)
    else:
        # Single file conversion
        if not input_path.exists():
            console.print(f"[red]❌ Error: File not found: {input_path}[/red]")
            raise typer.Exit(1)
            
        if input_path.suffix.lower() not in ['.md', '.html']:
            console.print(f"[red]❌ Error: Input must be a markdown (.md) or HTML (.html) file[/red]")
            raise typer.Exit(1)
            
        output_pdf = output or input_path.with_suffix('.pdf')
        
        console.print(f"[bold blue]📄 Converting {input_path} to PDF[/bold blue]")
        
        success = converter.convert_to_pdf(
            input_path,
            output_pdf,
            css_file,
            css_string
        )
        
        if not success:
            raise typer.Exit(1)

@app.command("resume-formats")
def resume_formats_command(
    input_path: Path = typer.Argument(
        ...,
        help="Input resume markdown or HTML file"
    ),
    output_dir: Optional[Path] = typer.Option(
        None, "--output-dir", "-o",
        help="Output directory for all formats (default: data/outputs/pdf/)"
    ),
    formats: Optional[str] = typer.Option(
        "sensylate,executive,ats,professional", "--formats", "-f",
        help="Comma-separated list of formats: sensylate,executive,ats,professional,minimal,technical,heebo-premium"
    ),
):
    """📄 Generate multiple professional resume formats from a single markdown or HTML file
    
    Creates high-quality resume PDFs in 6 professional formats optimized for different use cases.
    All formats include centered SVG brand text (2x size) for perfect font consistency.
    
    Available formats:
    - sensylate: Brand-consistent design matching colemorton.com aesthetic with perfect color alignment
    - executive: High-impact presentation with modern typography and visual elements  
    - ats: ATS-optimized format for applicant tracking systems with clean structure
    - professional: Balanced professional styling suitable for general applications
    - minimal: Clean, simple formatting for minimalist preference
    - heebo-premium: Premium design showcasing variable Heebo font features
    
    All templates feature:
    • SVG brand text integration for perfect font consistency
    • Professional page layouts with proper margins and spacing
    • Clickable links preserved in PDF output
    • Print-optimized formatting and page breaks
    • Accessibility-compliant markup with hidden text for screen readers
    """
    from .pdf_converter import PDFConverter
    
    if not input_path.exists():
        console.print(f"[red]❌ Error: Input file not found: {input_path}[/red]")
        raise typer.Exit(1)
    
    if input_path.suffix.lower() not in ['.md', '.html']:
        console.print(f"[red]❌ Error: Input must be a markdown (.md) or HTML (.html) file[/red]")
        raise typer.Exit(1)
    
    # Default output directory
    if not output_dir:
        output_dir = Path("data/outputs/pdf")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Parse formats
    format_list = [f.strip() for f in formats.split(',')]
    
    # Style mapping
    style_mapping = {
        'sensylate': Path('applyr/styles/sensylate.css'),
        'executive': Path('applyr/styles/executive.css'),
        'ats': Path('applyr/styles/ats.css'), 
        'professional': Path('applyr/styles/professional.css'),
        'minimal': Path('applyr/styles/minimal.css'),
        'technical': Path('applyr/styles/technical.css') if Path('applyr/styles/technical.css').exists() else Path('applyr/styles/professional.css'),
        'heebo-premium': Path('applyr/styles/heebo-premium.css')
    }
    
    converter = PDFConverter(console)
    console.print(f"[bold blue]📄 Generating {len(format_list)} resume formats from {input_path.name}[/bold blue]")
    
    results = {}
    base_name = input_path.stem
    
    for format_name in track(format_list, description="Generating formats..."):
        if format_name not in style_mapping:
            console.print(f"[yellow]⚠️  Unknown format: {format_name}, skipping[/yellow]")
            continue
            
        css_file = style_mapping[format_name]
        if not css_file.exists():
            console.print(f"[yellow]⚠️  CSS file not found: {css_file}, skipping {format_name}[/yellow]")
            continue
            
        output_pdf = output_dir / f"{base_name}_{format_name}.pdf"
        
        console.print(f"[blue]  → {format_name}: {output_pdf.name}[/blue]")
        
        success = converter.convert_to_pdf(
            input_path,
            output_pdf,
            css_file=css_file
        )
        
        results[format_name] = {
            'success': success,
            'file': output_pdf,
            'size': output_pdf.stat().st_size if success and output_pdf.exists() else 0
        }
    
    # Summary table
    console.print(f"\n[bold green]✅ Resume Format Generation Complete[/bold green]")
    
    table = Table(title="Generated Formats", show_header=True)
    table.add_column("Format", style="bold blue")
    table.add_column("Status", justify="center")
    table.add_column("File Size", justify="right")
    table.add_column("Output File", style="dim")
    
    for format_name, result in results.items():
        status = "[green]✅ Success[/green]" if result['success'] else "[red]❌ Failed[/red]"
        size = f"{result['size']:,} bytes" if result['size'] > 0 else "—"
        table.add_row(format_name.title(), status, size, result['file'].name)
    
    console.print(table)
    
    success_count = sum(1 for r in results.values() if r['success'])
    if success_count == 0:
        console.print(f"[red]❌ All conversions failed[/red]")
        raise typer.Exit(1)
    elif success_count < len(format_list):
        console.print(f"[yellow]⚠️  {success_count}/{len(format_list)} formats generated successfully[/yellow]")
    else:
        console.print(f"[green]🎉 All {success_count} formats generated successfully in {output_dir}[/green]")

@app.command("validate-pdf")
def validate_pdf_command(
    pdf_path: Path = typer.Argument(
        ...,
        help="PDF file to validate and analyze"
    ),
    detailed: bool = typer.Option(
        False, "--detailed", "-d",
        help="Show detailed quality analysis"
    ),
):
    """🔍 Validate PDF quality and provide optimization recommendations
    
    Analyzes PDF file size, structure, and quality metrics to identify
    optimization opportunities and potential issues.
    """
    from .pdf_converter import PDFConverter
    
    if not pdf_path.exists():
        console.print(f"[red]❌ Error: PDF file not found: {pdf_path}[/red]")
        raise typer.Exit(1)
    
    if not pdf_path.suffix.lower() == '.pdf':
        console.print(f"[red]❌ Error: File must be a PDF (.pdf)[/red]")
        raise typer.Exit(1)
    
    converter = PDFConverter(console)
    console.print(f"[bold blue]🔍 Validating PDF: {pdf_path.name}[/bold blue]")
    
    validation = converter.validate_pdf_quality(pdf_path)
    
    if not validation['valid']:
        console.print(f"[red]❌ Validation failed: {validation.get('error', 'Unknown error')}[/red]")
        raise typer.Exit(1)
    
    metrics = validation['metrics']
    recommendations = validation['recommendations']
    
    # Summary
    quality_score = metrics.get('quality_score', 0)
    if quality_score >= 8:
        quality_color = "green"
        quality_emoji = "🎉"
    elif quality_score >= 6:
        quality_color = "yellow"
        quality_emoji = "⚠️"
    else:
        quality_color = "red"
        quality_emoji = "❌"
    
    console.print(f"\n[{quality_color}]{quality_emoji} Quality Score: {quality_score}/10[/{quality_color}]")
    
    # Basic metrics table
    table = Table(title="PDF Metrics", show_header=True)
    table.add_column("Metric", style="bold blue")
    table.add_column("Value", justify="right")
    table.add_column("Assessment", style="dim")
    
    # File size info
    size_rating = metrics.get('size_rating', 'unknown')
    size_note = metrics.get('size_note', '')
    size_color = {
        'optimal': 'green',
        'good': 'blue', 
        'large': 'yellow',
        'oversized': 'red',
        'minimal': 'yellow'
    }.get(size_rating, 'white')
    
    table.add_row(
        "File Size", 
        f"{metrics.get('file_size_kb', 0):.1f} KB", 
        f"[{size_color}]{size_rating.title()}[/{size_color}] - {size_note}"
    )
    
    if metrics.get('page_count', 'unknown') != 'unknown':
        pages = metrics.get('page_count', 0)
        pages_per_mb = metrics.get('pages_per_mb', 'N/A')
        table.add_row("Pages", str(pages), f"Density: {pages_per_mb} pages/MB" if pages_per_mb != 'N/A' else "")
    
    if detailed:
        table.add_row("Encrypted", str(metrics.get('encrypted', 'Unknown')), "")
        table.add_row("Has Metadata", str(metrics.get('has_metadata', 'Unknown')), "")
        
        if 'pdf_error' in metrics:
            table.add_row("PDF Status", "Error", f"[red]{metrics['pdf_error']}[/red]")
    
    console.print(table)
    
    # Recommendations
    if recommendations:
        console.print(f"\n[bold yellow]💡 Optimization Recommendations:[/bold yellow]")
        for i, rec in enumerate(recommendations, 1):
            console.print(f"  {i}. {rec}")
    else:
        console.print(f"\n[green]✅ No optimization recommendations - PDF looks good![/green]")
    
    # File path info
    console.print(f"\n[dim]📁 File: {pdf_path.absolute()}[/dim]")

@app.command("status")
def status_command(
    job_filter: Optional[str] = typer.Option(
        None, "--filter", "-f",
        help="Filter by status: discovered, interested, applied, interviewed, rejected, closed"
    ),
    limit: int = typer.Option(
        50, "--limit", "-l",
        help="Maximum number of jobs to display"
    ),
):
    """📊 View application status pipeline
    
    Display jobs and their current application status with filtering options.
    """
    from .database import ApplicationDatabase, JobStatus
    
    database = ApplicationDatabase(console=console)
    
    # Parse status filter
    status_filter = None
    if job_filter:
        try:
            status_filter = JobStatus(job_filter.lower())
        except ValueError:
            console.print(f"[red]❌ Invalid status: {job_filter}[/red]")
            console.print("Valid statuses: discovered, interested, applied, interviewed, rejected, closed")
            raise typer.Exit(1)
    
    database.display_jobs(status_filter=status_filter, limit=limit)

@app.command("update-status")
def update_status_command(
    job_id: str = typer.Argument(..., help="Job ID to update"),
    status: str = typer.Argument(..., help="New status: discovered, interested, applied, interviewed, rejected, closed"),
):
    """🔄 Update job application status
    
    Change the status of a specific job application.
    """
    from .database import ApplicationDatabase, JobStatus
    
    try:
        new_status = JobStatus(status.lower())
    except ValueError:
        console.print(f"[red]❌ Invalid status: {status}[/red]")
        console.print("Valid statuses: discovered, interested, applied, interviewed, rejected, closed")
        raise typer.Exit(1)
    
    database = ApplicationDatabase(console=console)
    success = database.update_status(job_id, new_status)
    
    if not success:
        raise typer.Exit(1)

@app.command("stats")
def stats_command():
    """📈 Application statistics and success rates
    
    Display comprehensive statistics about your job applications.
    """
    from .database import ApplicationDatabase
    
    database = ApplicationDatabase(console=console)
    database.display_statistics()

@app.command("jobs")
def jobs_command(
    company: Optional[str] = typer.Option(
        None, "--company", "-c",
        help="Filter by company name"
    ),
    status: Optional[str] = typer.Option(
        None, "--status", "-s",
        help="Filter by status"
    ),
    limit: int = typer.Option(
        50, "--limit", "-l",
        help="Maximum number of jobs to display"
    ),
):
    """💼 List and search jobs in database
    
    Search and filter jobs by company, status, or other criteria.
    """
    from .database import ApplicationDatabase, JobStatus
    
    database = ApplicationDatabase(console=console)
    df = database.load_data()
    
    if df.empty:
        console.print("[yellow]No jobs in database[/yellow]")
        return
    
    # Apply filters
    if company:
        df = df[df['company_name'].str.contains(company, case=False, na=False)]
    
    if status:
        try:
            status_enum = JobStatus(status.lower())
            df = df[df['status'] == status_enum.value]
        except ValueError:
            console.print(f"[red]❌ Invalid status: {status}[/red]")
            raise typer.Exit(1)
    
    if df.empty:
        console.print("[yellow]No jobs match the specified filters[/yellow]")
        return
    
    # Display results
    df_limited = df.head(limit)
    
    table = Table(title="🔍 Job Search Results")
    table.add_column("Job ID", style="cyan")
    table.add_column("Company", style="green")
    table.add_column("Title", style="blue")
    table.add_column("Status", style="yellow")
    table.add_column("Priority", style="red")
    table.add_column("Discovered", style="dim")
    
    for _, row in df_limited.iterrows():
        table.add_row(
            str(row['job_id']),
            row['company_name'][:30] + "..." if len(row['company_name']) > 30 else row['company_name'],
            row['job_title'][:40] + "..." if len(row['job_title']) > 40 else row['job_title'],
            row['status'],
            row['priority'],
            row['date_discovered']
        )
    
    console.print(table)
    
    if len(df) > limit:
        console.print(f"\n[dim]Showing {limit} of {len(df)} results. Use --limit to show more.[/dim]")

@app.command("cleanup")
def cleanup_command(
    days: int = typer.Option(
        30, "--days", "-d",
        help="Remove closed/rejected jobs older than this many days"
    ),
    confirm: bool = typer.Option(
        False, "--confirm", "-y",
        help="Skip confirmation prompt"
    ),
):
    """🧹 Clean up old closed/rejected jobs
    
    Remove old job entries to keep the database manageable.
    """
    from .database import ApplicationDatabase
    
    database = ApplicationDatabase(console=console)
    
    if not confirm:
        # Preview what would be removed
        df = database.load_data()
        if not df.empty:
            import pandas as pd
            cutoff_date = pd.Timestamp.now() - pd.Timedelta(days=days)
            df['date_discovered'] = pd.to_datetime(df['date_discovered'], errors='coerce')
            
            old_closed_jobs = df[
                (df['date_discovered'] < cutoff_date) & 
                df['status'].isin(['closed', 'rejected'])
            ]
            
            if len(old_closed_jobs) > 0:
                console.print(f"[yellow]Would remove {len(old_closed_jobs)} jobs older than {days} days[/yellow]")
                if not typer.confirm("Continue with cleanup?"):
                    console.print("Cleanup cancelled")
                    return
            else:
                console.print("[green]No jobs to clean up[/green]")
                return
    
    removed_count = database.cleanup_old_jobs(days)
    
    if removed_count > 0:
        console.print(f"[green]✅ Cleaned up {removed_count} old jobs[/green]")
    else:
        console.print("[blue]No jobs needed cleanup[/blue]")

@app.command("add-job")
def add_job_command(
    job_id: str = typer.Argument(..., help="8-digit SEEK job ID to add"),
    priority: Optional[str] = typer.Option(
        "medium", "--priority", "-p",
        help="Job priority: high, medium, low"
    ),
    notes: Optional[str] = typer.Option(
        None, "--notes", "-n",
        help="Custom notes about this job"
    ),
    force: bool = typer.Option(
        False, "--force", "-f",
        help="Skip duplicate confirmation prompt"
    ),
):
    """📋 Add a new job by SEEK job ID
    
    Scrape and add a job to the database using just the job ID.
    Constructs the SEEK URL automatically and processes the job.
    """
    import re
    from .database import ApplicationDatabase, Priority
    from .scraper import scrape_jobs
    
    # Validate job_id format (8-digit numeric)
    if not re.match(r'^\d{8}$', job_id):
        console.print("[red]❌ Error: Job ID must be exactly 8 digits[/red]")
        console.print(f"[red]   Provided: '{job_id}'[/red]")
        console.print("[yellow]💡 Example: applyr add-job 87066700[/yellow]")
        raise typer.Exit(1)
    
    # Validate priority
    priority_map = {
        'high': Priority.HIGH,
        'medium': Priority.MEDIUM, 
        'low': Priority.LOW
    }
    
    if priority.lower() not in priority_map:
        console.print(f"[red]❌ Error: Invalid priority '{priority}'[/red]")
        console.print("[yellow]Valid priorities: high, medium, low[/yellow]")
        raise typer.Exit(1)
    
    priority_enum = priority_map[priority.lower()]
    
    # Initialize database
    database = ApplicationDatabase(console=console)
    
    # Check for duplicates
    if database.job_exists(job_id):
        console.print(f"[yellow]⚠️  Job {job_id} already exists in database[/yellow]")
        
        if not force:
            # Show existing job details
            existing_job = database.get_job(job_id)
            if existing_job:
                console.print(f"[dim]Existing: {existing_job['company_name']} - {existing_job['job_title']} ({existing_job['status']})[/dim]")
            
            if not typer.confirm("Do you want to re-scrape and update this job?"):
                console.print("[blue]Operation cancelled[/blue]")
                return
        
        console.print("[blue]Proceeding to re-scrape existing job...[/blue]")
    
    # Construct SEEK URL
    seek_url = f"https://www.seek.com.au/job/{job_id}"
    console.print(f"[blue]🔍 Scraping job from: {seek_url}[/blue]")
    
    # Use existing scraper infrastructure
    try:
        results = scrape_jobs([seek_url], Path("data/outputs/job_descriptions"), 2.0, console, database)
        
        success = results.get(seek_url, False)
        
        if success:
            # Update priority and notes if provided
            update_kwargs = {}
            if priority != "medium":  # Only update if not default
                update_kwargs['priority'] = priority_enum
            if notes:
                update_kwargs['notes'] = notes
            
            if update_kwargs:
                database.update_job(job_id, **update_kwargs)
            
            # Show success message with job details
            job = database.get_job(job_id)
            if job:
                console.print(f"\n[bold green]✅ Successfully added job {job_id}![/bold green]")
                console.print(f"[green]Company:[/green] {job['company_name']}")
                console.print(f"[green]Title:[/green] {job['job_title']}")
                console.print(f"[green]Status:[/green] {job['status']}")
                console.print(f"[green]Priority:[/green] {job['priority']}")
                if notes:
                    console.print(f"[green]Notes:[/green] {notes}")
                    
                console.print(f"\n[dim]💡 Use 'applyr update-status {job_id} applied' when you apply to this job[/dim]")
            else:
                console.print(f"[green]✅ Job {job_id} added successfully[/green]")
        else:
            console.print(f"[red]❌ Failed to scrape job {job_id}[/red]")
            console.print("[yellow]💡 This could be due to:[/yellow]")
            console.print("[yellow]   • Invalid job ID[/yellow]")
            console.print("[yellow]   • Job posting has been removed[/yellow]")
            console.print("[yellow]   • Network connectivity issues[/yellow]")
            console.print("[yellow]   • SEEK anti-bot measures[/yellow]")
            raise typer.Exit(1)
            
    except Exception as e:
        console.print(f"[red]❌ Error during scraping operation: {e}[/red]")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()