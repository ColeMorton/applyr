#!/usr/bin/env python3
"""Data migration script to populate advertisements.csv with existing scraped job data"""

from datetime import datetime
from pathlib import Path
import re
import sys
from typing import Optional

# Add parent directory to path to import applyr modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from rich.console import Console
from rich.progress import BarColumn, Progress, SpinnerColumn, TaskProgressColumn, TextColumn
from rich.table import Table

from applyr.database import ApplicationDatabase, JobStatus, Priority


class DataMigrator:
    """Migrate existing job data into the application tracking database"""

    def __init__(self):
        self.console = Console()
        self.database = ApplicationDatabase(console=self.console)
        self.project_root = Path(__file__).parent.parent

        # Data directories
        self.job_desc_dirs = [
            self.project_root / "data" / "outputs" / "job_descriptions",
            self.project_root / "data" / "outputs" / "job_descriptions_1",
        ]
        self.cover_letters_dir = self.project_root / "data" / "outputs" / "cover_letters"

        # Migration statistics
        self.stats = {
            "total_files_processed": 0,
            "jobs_migrated": 0,
            "jobs_applied": 0,
            "jobs_discovered": 0,
            "duplicates_found": 0,
            "errors": 0,
            "cover_letters_found": 0,
        }

    def extract_job_metadata(self, md_file: Path) -> Optional[dict]:
        """Extract job metadata from markdown file"""
        try:
            with open(md_file, encoding="utf-8") as f:
                content = f.read()

            # Extract metadata using regex patterns
            metadata = {}

            # Job title from first heading
            title_match = re.search(r"^# (.+)$", content, re.MULTILINE)
            if title_match:
                metadata["job_title"] = title_match.group(1).strip()

            # Company from metadata section
            company_match = re.search(r"\*\*Company:\*\* (.+)", content)
            if company_match:
                metadata["company_name"] = company_match.group(1).strip()

            # Job ID from metadata section
            job_id_match = re.search(r"\*\*Job ID:\*\* (\d+)", content)
            if job_id_match:
                metadata["job_id"] = job_id_match.group(1).strip()

            # Source from metadata section
            source_match = re.search(r"\*\*Source:\*\* (.+)", content)
            if source_match:
                metadata["source"] = source_match.group(1).strip()
            else:
                metadata["source"] = "SEEK"  # Default

            # Scraped date from metadata section
            scraped_match = re.search(r"\*\*Scraped:\*\* (.+)", content)
            if scraped_match:
                scraped_str = scraped_match.group(1).strip()
                try:
                    # Parse date format: 2025-09-12 14:07:37
                    scraped_date = datetime.strptime(scraped_str.split()[0], "%Y-%m-%d")
                    metadata["date_discovered"] = scraped_date.strftime("%Y-%m-%d")
                except ValueError:
                    self.console.print(f"[yellow]⚠️  Could not parse date '{scraped_str}' in {md_file.name}[/yellow]")
                    metadata["date_discovered"] = datetime.now().strftime("%Y-%m-%d")

            # Generate URL from job ID if available
            if "job_id" in metadata:
                metadata["url"] = f"https://www.seek.com.au/job/{metadata['job_id']}"

            # Validate required fields
            required_fields = ["job_id", "company_name", "job_title"]
            if all(field in metadata for field in required_fields):
                return metadata
            else:
                missing = [field for field in required_fields if field not in metadata]
                self.console.print(f"[red]❌ Missing required fields {missing} in {md_file.name}[/red]")
                return None

        except Exception as e:
            self.console.print(f"[red]❌ Error processing {md_file.name}: {e}[/red]")
            return None

    def normalize_company_name(self, company_name: str) -> str:
        """Normalize company name for cover letter matching"""
        # Remove common suffixes and normalize
        normalized = company_name.lower()

        # Remove company type suffixes
        suffixes_to_remove = [
            " pty ltd",
            " ltd",
            " inc",
            " corporation",
            " corp",
            " australia",
            " au",
            " limited",
            " group",
            " software",
            " technologies",
            " tech",
            " solutions",
            " services",
        ]

        for suffix in suffixes_to_remove:
            if normalized.endswith(suffix):
                normalized = normalized[: -len(suffix)].strip()

        # Remove special characters and spaces for matching
        normalized = re.sub(r"[^a-z0-9]", "", normalized)

        return normalized

    def find_cover_letter_files(self) -> set[str]:
        """Find all cover letter files and extract company names"""
        cover_letter_companies = set()

        if not self.cover_letters_dir.exists():
            self.console.print(f"[yellow]⚠️  Cover letters directory not found: {self.cover_letters_dir}[/yellow]")
            return cover_letter_companies

        for cover_letter_file in self.cover_letters_dir.glob("*.md"):
            # Extract company name from filename (remove .md extension)
            company_filename = cover_letter_file.stem.lower()

            # Handle special cases in filenames
            company_mapping = {
                "trilogy_care": "trilogycare",
                "linkedin reach out": "linkedin",
                "dappleos": "dapple",
                "examplecorp": "examplecorp",
                "acme": "acme",
                "techsolutions": "techsolutions",
            }

            normalized_name = company_mapping.get(company_filename, company_filename.replace(" ", "").replace("_", ""))
            cover_letter_companies.add(normalized_name)

        self.stats["cover_letters_found"] = len(cover_letter_companies)
        return cover_letter_companies

    def determine_job_status(self, company_name: str, cover_letter_companies: set[str]) -> JobStatus:
        """Determine job status based on cover letter existence"""
        normalized_company = self.normalize_company_name(company_name)

        # Check if any cover letter company matches this job's company
        for cover_letter_company in cover_letter_companies:
            if (
                normalized_company in cover_letter_company
                or cover_letter_company in normalized_company
                or
                # Special cases
                (cover_letter_company == "examplecorp" and "example" in normalized_company)
                or (cover_letter_company == "acme" and "acme" in normalized_company)
                or (cover_letter_company == "techsolutions" and "tech" in normalized_company)
                or (cover_letter_company == "trilogycare" and "trilogy" in normalized_company)
                or (cover_letter_company == "foundu" and "foundu" in normalized_company)
                or (cover_letter_company == "fsoft" and "fsoft" in normalized_company)
                or (cover_letter_company == "aurion" and "aurion" in normalized_company)
                or (cover_letter_company == "dapple" and "dapple" in normalized_company)
            ):
                return JobStatus.APPLIED

        return JobStatus.DISCOVERED

    def process_job_descriptions(self) -> list[dict]:
        """Process all job description files and extract metadata"""
        all_jobs = []
        job_ids_seen = set()

        self.console.print("[blue]📂 Processing job description files...[/blue]")

        for job_desc_dir in self.job_desc_dirs:
            if not job_desc_dir.exists():
                continue

            md_files = list(job_desc_dir.glob("*.md"))
            # Filter out aggregate files
            md_files = [f for f in md_files if not f.name.endswith("_aggregate.md")]

            self.console.print(f"[dim]Processing {len(md_files)} files in {job_desc_dir.name}[/dim]")

            for md_file in md_files:
                self.stats["total_files_processed"] += 1

                metadata = self.extract_job_metadata(md_file)
                if metadata:
                    job_id = metadata["job_id"]

                    # Check for duplicates
                    if job_id in job_ids_seen:
                        self.console.print(f"[yellow]⚠️  Duplicate job ID {job_id} found, skipping[/yellow]")
                        self.stats["duplicates_found"] += 1
                        continue

                    job_ids_seen.add(job_id)
                    all_jobs.append(metadata)

                    self.console.print(f"[green]✅ Extracted: {job_id} - {metadata['company_name']}[/green]")
                else:
                    self.stats["errors"] += 1

        return all_jobs

    def migrate_jobs_to_database(self, jobs: list[dict], cover_letter_companies: set[str]) -> None:
        """Migrate extracted jobs to the application database"""
        self.console.print("[blue]💾 Migrating jobs to database...[/blue]")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=self.console,
        ) as progress:
            task = progress.add_task("Migrating jobs...", total=len(jobs))

            for job_data in jobs:
                # Determine status based on cover letter existence
                status = self.determine_job_status(job_data["company_name"], cover_letter_companies)

                # Set date_applied if job was applied to
                date_applied = None
                if status == JobStatus.APPLIED:
                    # Use discovery date as a placeholder for application date
                    # In reality, application date would be later than discovery date
                    date_applied = job_data.get("date_discovered")

                # Add job to database
                success = self.database.add_job(
                    job_id=job_data["job_id"],
                    company_name=job_data["company_name"],
                    job_title=job_data["job_title"],
                    source=job_data.get("source", "SEEK"),
                    status=status,
                    priority=Priority.MEDIUM,  # Default priority
                    url=job_data.get("url"),
                    notes=f"Migrated from {job_data.get('source', 'SEEK')} scraping on {job_data.get('date_discovered', 'unknown date')}",
                )

                if success:
                    self.stats["jobs_migrated"] += 1
                    if status == JobStatus.APPLIED:
                        self.stats["jobs_applied"] += 1
                        # Update date_applied if we have it
                        if date_applied:
                            self.database.update_job(job_data["job_id"], date_applied=date_applied)
                    else:
                        self.stats["jobs_discovered"] += 1
                else:
                    self.stats["errors"] += 1

                progress.advance(task)

    def generate_migration_report(self) -> None:
        """Generate and display migration report"""
        self.console.print("\n[bold blue]📊 Migration Report[/bold blue]")

        # Summary table
        summary_table = Table(title="Migration Summary")
        summary_table.add_column("Metric", style="cyan")
        summary_table.add_column("Count", style="green")

        summary_table.add_row("Files Processed", str(self.stats["total_files_processed"]))
        summary_table.add_row("Jobs Migrated", str(self.stats["jobs_migrated"]))
        summary_table.add_row("Applied Status", str(self.stats["jobs_applied"]))
        summary_table.add_row("Discovered Status", str(self.stats["jobs_discovered"]))
        summary_table.add_row("Cover Letters Found", str(self.stats["cover_letters_found"]))
        summary_table.add_row("Duplicates Skipped", str(self.stats["duplicates_found"]))
        summary_table.add_row("Errors", str(self.stats["errors"]))

        self.console.print(summary_table)

        # Show database statistics
        self.console.print("\n[bold blue]📈 Database Statistics After Migration[/bold blue]")
        self.database.display_statistics()

    def run_migration(self) -> bool:
        """Execute the complete data migration process"""
        self.console.print("[bold green]🚀 Starting Data Migration for applyr[/bold green]")
        self.console.print(f"[dim]Project root: {self.project_root}[/dim]\n")

        try:
            # Step 1: Find cover letter files
            self.console.print("[bold]Step 1: Analyzing cover letters...[/bold]")
            cover_letter_companies = self.find_cover_letter_files()
            self.console.print(f"[green]✅ Found {len(cover_letter_companies)} cover letters[/green]")

            # Step 2: Process job descriptions
            self.console.print("\n[bold]Step 2: Processing job descriptions...[/bold]")
            jobs = self.process_job_descriptions()
            self.console.print(f"[green]✅ Extracted {len(jobs)} unique jobs[/green]")

            if not jobs:
                self.console.print("[red]❌ No jobs found to migrate[/red]")
                return False

            # Step 3: Migrate to database
            self.console.print("\n[bold]Step 3: Migrating to database...[/bold]")
            self.migrate_jobs_to_database(jobs, cover_letter_companies)

            # Step 4: Generate report
            self.console.print("\n[bold]Step 4: Generating migration report...[/bold]")
            self.generate_migration_report()

            # Success message
            success_rate = (self.stats["jobs_migrated"] / len(jobs)) * 100 if jobs else 0
            self.console.print("\n[bold green]🎉 Migration completed successfully![/bold green]")
            self.console.print(
                f"[green]Success rate: {success_rate:.1f}% ({self.stats['jobs_migrated']}/{len(jobs)} jobs)[/green]"
            )

            return True

        except Exception as e:
            self.console.print(f"\n[red]❌ Migration failed: {e}[/red]")
            return False


def main():
    """Main function to run the migration"""
    migrator = DataMigrator()
    success = migrator.run_migration()

    if success:
        print("\n" + "=" * 60)
        print("📋 Next Steps:")
        print("1. Run 'applyr status' to view migrated jobs")
        print("2. Run 'applyr stats' to see application statistics")
        print("3. Use 'applyr jobs --company <name>' to search specific companies")
        print("4. Update job statuses with 'applyr update-status <job_id> <status>'")
        print("=" * 60)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
