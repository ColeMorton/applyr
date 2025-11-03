"""Batch job processing with Rich console integration"""

import logging
from pathlib import Path

from rich.console import Console
from rich.table import Table

from .scraper import scrape_jobs

logger = logging.getLogger(__name__)


def batch_process_jobs(urls_file: Path, output_dir: Path, delay: float, console: Console) -> bool:
    """Batch process multiple job URLs from file with Rich progress tracking."""
    try:
        with open(urls_file) as f:
            urls = [line.strip() for line in f if line.strip()]
    except Exception as e:
        console.print(f"[red]❌ Error reading URLs file: {e}[/red]")
        return False

    if not urls:
        console.print("[red]❌ No URLs found in file[/red]")
        return False

    console.print(f"[blue]📦 Found {len(urls)} URLs to process[/blue]")
    console.print(f"[blue]📁 Output directory: {output_dir}[/blue]")
    console.print(f"[blue]⏱️ Using {delay}s delay between requests[/blue]")

    console.print("\n[bold blue]Starting batch processing...[/bold blue]")

    results = scrape_jobs(urls, output_dir, delay, console)

    successful = sum(1 for success in results.values() if success)
    failed = len(results) - successful

    table = Table(title="📊 Batch Processing Results")
    table.add_column("Metric", style="cyan")
    table.add_column("Count", style="green" if failed == 0 else "yellow")

    table.add_row("Total URLs", str(len(results)))
    table.add_row("Successful", str(successful))
    table.add_row("Failed", str(failed))

    console.print(table)

    if failed > 0:
        console.print(f"\n[red]❌ Failed URLs ({failed}):[/red]")
        for url, success in results.items():
            if not success:
                console.print(f"  • [red]{url}[/red]")

    if successful > 0:
        console.print(f"\n[green]✅ Job descriptions saved to: {output_dir}[/green]")
        console.print("[green]💡 Next step: Run 'applyr aggregate' to generate market intelligence[/green]")

    return failed == 0
