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
    skip_lint: bool = typer.Option(
        False, "--skip-lint",
        help="Skip HTML processing and validation"
    ),
    no_css: bool = typer.Option(
        False, "--no-css",
        help="Disable default CSS styling (forces unstyled output)"
    ),
):
    """📄 Convert markdown and HTML files to PDF with automatic CSS styling
    
    Automatically applies sensylate.css styling for resume/CV files. Use --no-css to disable.
    Supports single file conversion or batch processing of entire directories.
    
    Examples:
      pdf resume.html                    # Auto-styled with sensylate.css
      pdf resume.html --no-css           # Unstyled output
      pdf document.html                  # No styling (general content)
      pdf resume.html -c executive.css   # Custom styling
    """
    from .pdf_converter import PDFConverter
    
    def _get_default_css_for_file(input_path: Path) -> Optional[Path]:
        """Determine appropriate default CSS based on file content/name"""
        # Check if this appears to be a resume/CV file
        path_str = str(input_path).lower()
        if any(keyword in path_str for keyword in ['resume', 'cv']):
            default_css = Path("applyr/styles/sensylate.css")
            if default_css.exists():
                return default_css
        return None
    
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
            css_string,
            skip_lint
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
        
        # Implement CSS precedence logic: explicit CSS > default CSS > no CSS
        final_css_file = css_file
        final_css_string = css_string
        
        if not no_css and not css_file and not css_string:
            # No explicit CSS provided and default styling not disabled
            default_css = _get_default_css_for_file(input_path)
            if default_css:
                final_css_file = default_css
                console.print(f"[blue]🎨 Applying default styling: {default_css.name}[/blue]")
                console.print("[dim]   Use --no-css to disable default styling[/dim]")
        elif no_css:
            # Explicit disable of styling
            final_css_file = None
            final_css_string = None
            console.print("[dim]🚫 Default styling disabled[/dim]")
        
        console.print(f"[bold blue]📄 Converting {input_path} to PDF[/bold blue]")
        
        success = converter.convert_to_pdf(
            input_path,
            output_pdf,
            final_css_file,
            final_css_string,
            skip_lint
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
    skip_lint: bool = typer.Option(
        False, "--skip-lint",
        help="Skip HTML processing and validation"
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
            css_file=css_file,
            skip_lint=skip_lint
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

@app.command("format-html")
def format_html_command(
    input_path: Path = typer.Argument(
        ...,
        help="HTML file or directory containing HTML files to format and validate"
    ),
    output: Optional[Path] = typer.Option(
        None, "--output", "-o",
        help="Output file or directory (default: overwrites input)"
    ),
    skip_lint: bool = typer.Option(
        False, "--skip-lint", 
        help="Skip all formatting and validation"
    ),
    show_capabilities: bool = typer.Option(
        False, "--capabilities",
        help="Show available HTML processing capabilities"
    ),
):
    """🔧 Format and validate HTML files for WeasyPrint compatibility
    
    Requires professional tools: Prettier for formatting and html-eslint for validation.
    Fails fast if dependencies are missing - install with npm to enable processing.
    """
    from .html_processor import HTMLProcessor
    
    processor = HTMLProcessor(console)
    
    if show_capabilities:
        capabilities = processor.get_processing_capabilities()
        console.print("[bold blue]🔧 HTML Processing Capabilities[/bold blue]")
        
        cap_table = Table(show_header=True)
        cap_table.add_column("Tool", style="bold")
        cap_table.add_column("Available", justify="center")
        cap_table.add_column("Features")
        
        cap_table.add_row(
            "Node.js", 
            "[green]✅[/green]" if capabilities['node_js'] else "[red]❌[/red]",
            "Required for html-eslint and Prettier"
        )
        cap_table.add_row(
            "html-eslint", 
            "[green]✅[/green]" if capabilities['html_eslint'] else "[red]❌[/red]",
            "Auto-fixing HTML validation issues"
        )
        cap_table.add_row(
            "Prettier", 
            "[green]✅[/green]" if capabilities['prettier'] else "[red]❌[/red]",
            "Professional HTML formatting"
        )
        cap_table.add_row(
            "Fail-Fast Mode", 
            "[green]✅[/green]",
            "Professional tools required (no fallbacks)"
        )
        cap_table.add_row(
            "WeasyPrint Rules", 
            "[green]✅[/green]",
            "PDF generation compatibility checks"
        )
        
        console.print(cap_table)
        
        if not capabilities['node_js'] or not capabilities['html_eslint']:
            console.print(f"\n[yellow]💡 {processor.install_instructions()}[/yellow]")
        
        return
    
    if not input_path.exists():
        console.print(f"[red]❌ Error: Path not found: {input_path}[/red]")
        raise typer.Exit(1)
    
    if input_path.is_file():
        # Single file processing
        if input_path.suffix.lower() != '.html':
            console.print(f"[red]❌ Error: Input must be an HTML (.html) file[/red]")
            raise typer.Exit(1)
        
        output_file = output or input_path
        
        console.print(f"[bold blue]🔧 Processing HTML file: {input_path.name}[/bold blue]")
        
        # Read input file
        with open(input_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Process HTML
        processed_content, changes = processor.process_html(
            html_content, 
            input_path, 
            skip_lint=skip_lint
        )
        
        # Write output
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(processed_content)
        
        if changes:
            console.print("[green]✨ HTML processing completed:[/green]")
            for change in changes:
                console.print(f"[green]  • {change}[/green]")
            console.print(f"[green]📄 Formatted HTML saved to: {output_file}[/green]")
        else:
            console.print("[green]✅ HTML is already well-formatted[/green]")
    
    else:
        # Directory processing
        if not input_path.is_dir():
            console.print(f"[red]❌ Error: {input_path} is not a valid file or directory[/red]")
            raise typer.Exit(1)
        
        html_files = list(input_path.glob("*.html"))
        if not html_files:
            console.print(f"[yellow]⚠️  No HTML files found in {input_path}[/yellow]")
            return
        
        output_dir = output or input_path
        if output != input_path:
            output_dir.mkdir(parents=True, exist_ok=True)
        
        console.print(f"[bold blue]📦 Processing {len(html_files)} HTML files from {input_path}[/bold blue]")
        
        results = {}
        
        for html_file in track(html_files, description="Processing HTML files..."):
            try:
                # Read file
                with open(html_file, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                # Process HTML
                processed_content, changes = processor.process_html(
                    html_content, 
                    html_file, 
                    skip_lint=skip_lint
                )
                
                # Write output
                output_file = output_dir / html_file.name
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(processed_content)
                
                results[html_file.name] = {
                    'success': True,
                    'changes': len(changes),
                    'changes_list': changes
                }
                
            except Exception as e:
                console.print(f"[red]❌ Error processing {html_file.name}: {e}[/red]")
                results[html_file.name] = {
                    'success': False,
                    'changes': 0,
                    'error': str(e)
                }
        
        # Summary
        successful = sum(1 for r in results.values() if r['success'])
        total_changes = sum(r.get('changes', 0) for r in results.values())
        
        summary_table = Table(title="HTML Processing Summary")
        summary_table.add_column("Metric", style="cyan")
        summary_table.add_column("Count", style="green")
        
        summary_table.add_row("Files Processed", str(len(html_files)))
        summary_table.add_row("Successful", str(successful))
        summary_table.add_row("Failed", str(len(results) - successful))
        summary_table.add_row("Total Changes", str(total_changes))
        
        console.print(summary_table)
        
        if successful > 0:
            console.print(f"\n[green]✅ HTML files processed and saved to: {output_dir}[/green]")

@app.command("format-export")
def format_export_command(
    input_path: Path = typer.Argument(
        ...,
        help="HTML file to format and export with WeasyPrint-optimized processing"
    ),
):
    """🔧 Format HTML file and export to data/outputs/ with WeasyPrint compatibility
    
    Applies professional HTML formatting and validation using WeasyPrint-optimized
    configurations, then exports the processed file to data/outputs/ preserving
    the original directory structure.
    
    Examples:
      format-export data/raw/personal/resume.html    # → data/outputs/personal/resume.html
      format-export path/to/document.html           # → data/outputs/path/to/document.html
      format-export file.html                       # → data/outputs/file.html
    """
    from .html_processor import HTMLProcessor
    
    def _calculate_output_path(input_path: Path) -> Path:
        """Calculate output path preserving directory structure under data/outputs/"""
        # Convert input path to absolute to normalize it
        abs_input = input_path.resolve()
        
        # If the input is under data/raw/, strip the data/raw/ prefix
        try:
            rel_to_raw = abs_input.relative_to(Path.cwd() / "data" / "raw")
            return Path("data/outputs") / rel_to_raw
        except ValueError:
            # Input is not under data/raw/, preserve full relative structure
            return Path("data/outputs") / input_path
    
    # Validate input file
    if not input_path.exists():
        console.print(f"[red]❌ Error: HTML file not found: {input_path}[/red]")
        raise typer.Exit(1)
    
    if not input_path.is_file():
        console.print(f"[red]❌ Error: Path is not a file: {input_path}[/red]")
        raise typer.Exit(1)
    
    if input_path.suffix.lower() != '.html':
        console.print(f"[red]❌ Error: Input must be an HTML (.html) file[/red]")
        raise typer.Exit(1)
    
    # Calculate output path
    output_path = _calculate_output_path(input_path)
    
    # Create output directory
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    console.print(f"[bold blue]🔧 Processing HTML with WeasyPrint optimization[/bold blue]")
    console.print(f"[blue]📁 Input:  {input_path}[/blue]")
    console.print(f"[blue]📁 Output: {output_path}[/blue]")
    
    # Read input file
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        console.print(f"[red]❌ Error reading input file: {e}[/red]")
        raise typer.Exit(1)
    
    # Process HTML with forced WeasyPrint mode
    processor = HTMLProcessor(console, weasyprint_mode=True)
    
    try:
        processed_content, changes = processor.process_html(
            html_content, 
            input_path, 
            skip_lint=False
        )
    except RuntimeError as e:
        console.print(f"[red]❌ Processing failed: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]❌ Unexpected error during processing: {e}[/red]")
        raise typer.Exit(1)
    
    # Write output file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(processed_content)
    except Exception as e:
        console.print(f"[red]❌ Error writing output file: {e}[/red]")
        raise typer.Exit(1)
    
    # Report results
    if changes:
        console.print("\n[green]✨ HTML processing completed with changes:[/green]")
        for change in changes:
            console.print(f"[green]  • {change}[/green]")
    else:
        console.print("\n[green]✅ HTML processed (no changes needed)[/green]")
    
    console.print(f"[green]📄 Formatted HTML exported to: {output_path}[/green]")

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
    job_ids: str = typer.Argument(..., help="8-digit SEEK job ID(s) - single or comma-separated"),
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
    """📋 Add job(s) by SEEK job ID

    Scrape and add one or more jobs to the database using job IDs.
    Accepts single ID or comma-separated list of IDs.

    Examples:
        applyr add-job 87066700
        applyr add-job 87278332,87277607,87066700
    """
    import re
    from .database import ApplicationDatabase, Priority
    from .scraper import scrape_jobs
    from rich.progress import Progress, SpinnerColumn, TextColumn

    # Parse comma-separated job IDs
    job_id_list = [jid.strip() for jid in job_ids.split(',')]

    # Validate all job IDs
    invalid_ids = []
    for job_id in job_id_list:
        if not re.match(r'^\d{8}$', job_id):
            invalid_ids.append(job_id)

    if invalid_ids:
        console.print("[red]❌ Error: Invalid job ID format[/red]")
        for invalid_id in invalid_ids:
            console.print(f"[red]   Invalid: '{invalid_id}' (must be exactly 8 digits)[/red]")
        console.print("[yellow]💡 Example: applyr add-job 87066700 or applyr add-job 87278332,87277607[/yellow]")
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

    # Process multiple jobs
    if len(job_id_list) > 1:
        console.print(f"[bold blue]📋 Processing {len(job_id_list)} jobs[/bold blue]")

    # Check for duplicates and prepare URLs
    urls_to_process = []
    duplicate_jobs = []

    for job_id in job_id_list:
        if database.job_exists(job_id) and not force:
            existing_job = database.get_job(job_id)
            if existing_job:
                duplicate_jobs.append((job_id, existing_job['company_name'], existing_job['job_title'], existing_job['status']))
        else:
            urls_to_process.append(f"https://www.seek.com.au/job/{job_id}")

    # Handle duplicates confirmation for multiple jobs
    if duplicate_jobs and not force:
        console.print(f"[yellow]⚠️  {len(duplicate_jobs)} job(s) already exist in database:[/yellow]")
        for job_id, company, title, status in duplicate_jobs:
            console.print(f"[dim]  {job_id}: {company} - {title} ({status})[/dim]")

        if not typer.confirm("\nDo you want to re-scrape these existing jobs?"):
            console.print("[blue]Skipping existing jobs...[/blue]")
        else:
            # Add duplicate URLs to processing list
            for job_id, _, _, _ in duplicate_jobs:
                urls_to_process.append(f"https://www.seek.com.au/job/{job_id}")
    elif duplicate_jobs and force:
        # Force mode - add all duplicates
        for job_id, _, _, _ in duplicate_jobs:
            urls_to_process.append(f"https://www.seek.com.au/job/{job_id}")

    if not urls_to_process:
        console.print("[yellow]No new jobs to process[/yellow]")
        return

    # Process all jobs with existing scraper infrastructure
    console.print(f"[blue]🔍 Scraping {len(urls_to_process)} job(s)...[/blue]")

    try:
        results = scrape_jobs(urls_to_process, Path("data/outputs/job_descriptions"), 2.0, console, database)

        # Process results and update database
        successful_jobs = []
        failed_jobs = []

        for url in urls_to_process:
            job_id = url.split('/')[-1]
            success = results.get(url, False)

            if success:
                # Update priority and notes if provided
                update_kwargs = {}
                if priority != "medium":  # Only update if not default
                    update_kwargs['priority'] = priority_enum
                if notes:
                    update_kwargs['notes'] = notes

                if update_kwargs:
                    database.update_job(job_id, **update_kwargs)

                # Fetch job details for summary
                job = database.get_job(job_id)
                if job:
                    successful_jobs.append({
                        'job_id': job_id,
                        'company': job['company_name'],
                        'title': job['job_title'],
                        'status': job['status'],
                        'priority': job['priority']
                    })
                else:
                    successful_jobs.append({
                        'job_id': job_id,
                        'company': 'Unknown',
                        'title': 'Unknown',
                        'status': 'discovered',
                        'priority': priority_enum.value
                    })
            else:
                failed_jobs.append(job_id)

        # Display results summary
        if len(job_id_list) == 1 and successful_jobs:
            # Single job - use original detailed output
            job = successful_jobs[0]
            console.print(f"\n[bold green]✅ Successfully added job {job['job_id']}![/bold green]")
            console.print(f"[green]Company:[/green] {job['company']}")
            console.print(f"[green]Title:[/green] {job['title']}")
            console.print(f"[green]Status:[/green] {job['status']}")
            console.print(f"[green]Priority:[/green] {job['priority']}")
            if notes:
                console.print(f"[green]Notes:[/green] {notes}")
            console.print(f"\n[dim]💡 Use 'applyr update-status {job['job_id']} applied' when you apply to this job[/dim]")
        elif len(job_id_list) > 1:
            # Multiple jobs - display summary table
            console.print("\n[bold]📊 Processing Results[/bold]")

            if successful_jobs:
                table = Table(title=f"✅ Successfully Added ({len(successful_jobs)} jobs)")
                table.add_column("Job ID", style="cyan")
                table.add_column("Company", style="blue")
                table.add_column("Title", style="white")
                table.add_column("Status", style="green")
                table.add_column("Priority", style="yellow")

                for job in successful_jobs:
                    table.add_row(
                        job['job_id'],
                        job['company'][:30] + '...' if len(job['company']) > 30 else job['company'],
                        job['title'][:40] + '...' if len(job['title']) > 40 else job['title'],
                        job['status'],
                        job['priority']
                    )

                console.print(table)

            if failed_jobs:
                console.print(f"\n[red]❌ Failed to scrape {len(failed_jobs)} job(s):[/red]")
                for job_id in failed_jobs:
                    console.print(f"[red]   • {job_id}[/red]")
                console.print("[yellow]💡 Failures could be due to:[/yellow]")
                console.print("[yellow]   • Invalid job ID[/yellow]")
                console.print("[yellow]   • Job posting has been removed[/yellow]")
                console.print("[yellow]   • Network connectivity issues[/yellow]")

            # Summary stats
            console.print(f"\n[bold blue]Summary:[/bold blue]")
            console.print(f"[green]✓ Successful: {len(successful_jobs)}[/green]")
            console.print(f"[red]✗ Failed: {len(failed_jobs)}[/red]")

            if successful_jobs:
                console.print(f"\n[dim]💡 Use 'applyr update-status <job-id> applied' when you apply to these jobs[/dim]")
        elif failed_jobs:
            # All jobs failed
            console.print(f"\n[red]❌ Failed to scrape all {len(failed_jobs)} job(s)[/red]")
            console.print("[yellow]💡 This could be due to:[/yellow]")
            console.print("[yellow]   • Invalid job IDs[/yellow]")
            console.print("[yellow]   • Job postings have been removed[/yellow]")
            console.print("[yellow]   • Network connectivity issues[/yellow]")
            console.print("[yellow]   • SEEK anti-bot measures[/yellow]")
            raise typer.Exit(1)
            
    except Exception as e:
        console.print(f"[red]❌ Error during scraping operation: {e}[/red]")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()