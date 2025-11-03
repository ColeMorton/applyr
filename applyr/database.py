"""Application tracking database module using CSV backend"""

from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional, Union

import pandas as pd
from rich.console import Console
from rich.table import Table


class JobStatus(Enum):
    """Job application status enumeration"""

    DISCOVERED = "discovered"
    INTERESTED = "interested"
    APPLIED = "applied"
    INTERVIEWED = "interviewed"
    REJECTED = "rejected"
    CLOSED = "closed"


class Priority(Enum):
    """Job priority enumeration"""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ApplicationDatabase:
    """Application tracking database with CSV backend"""

    def __init__(self, csv_path: Union[str, Path] = "data/raw/advertisements.csv", console: Optional[Console] = None):
        """Initialize database with CSV path and optional console"""
        self.csv_path = Path(csv_path)
        self.console = console or Console()
        self._ensure_database_exists()

    def _ensure_database_exists(self) -> None:
        """Ensure CSV file exists with proper schema"""
        if not self.csv_path.exists():
            self.csv_path.parent.mkdir(parents=True, exist_ok=True)
            self._create_empty_database()
        elif not self._validate_schema():
            raise ValueError(f"Invalid schema in {self.csv_path}")

    def _create_empty_database(self) -> None:
        """Create empty CSV with proper schema"""
        schema_headers = [
            "job_id",
            "company_name",
            "job_title",
            "source",
            "status",
            "priority",
            "date_discovered",
            "date_applied",
            "date_closed",
            "notes",
            "salary_min",
            "salary_max",
            "location",
            "url",
        ]
        empty_df = pd.DataFrame(columns=schema_headers)
        empty_df.to_csv(self.csv_path, index=False)

    def _validate_schema(self) -> bool:
        """Validate CSV has required columns"""
        try:
            df = pd.read_csv(self.csv_path)
            required_columns = {
                "job_id",
                "company_name",
                "job_title",
                "source",
                "status",
                "priority",
                "date_discovered",
                "date_applied",
                "date_closed",
                "notes",
                "salary_min",
                "salary_max",
                "location",
                "url",
            }
            return required_columns.issubset(set(df.columns))
        except Exception:
            return False

    def load_data(self) -> pd.DataFrame:
        """Load all data from CSV"""
        try:
            df = pd.read_csv(self.csv_path)
            df["job_id"] = df["job_id"].astype(str)
            return df
        except Exception as e:
            self.console.print(f"[red]❌ Error loading database: {e}[/red]")
            return pd.DataFrame()

    def save_data(self, df: pd.DataFrame) -> bool:
        """Save dataframe to CSV"""
        try:
            df.to_csv(self.csv_path, index=False)
            return True
        except Exception as e:
            self.console.print(f"[red]❌ Error saving database: {e}[/red]")
            return False

    def add_job(
        self,
        job_id: str,
        company_name: str,
        job_title: str,
        source: str = "SEEK",
        status: JobStatus = JobStatus.DISCOVERED,
        priority: Priority = Priority.MEDIUM,
        url: Optional[str] = None,
        location: Optional[str] = None,
        salary_min: Optional[float] = None,
        salary_max: Optional[float] = None,
        notes: Optional[str] = None,
    ) -> bool:
        """Add new job to database"""

        if self.job_exists(job_id):
            self.console.print(f"[yellow]⚠️  Job {job_id} already exists in database[/yellow]")
            return False

        df = self.load_data()

        new_job = {
            "job_id": str(job_id),
            "company_name": company_name,
            "job_title": job_title,
            "source": source,
            "status": status.value,
            "priority": priority.value,
            "date_discovered": datetime.now().strftime("%Y-%m-%d"),
            "date_applied": "",
            "date_closed": "",
            "notes": notes or "",
            "salary_min": salary_min or "",
            "salary_max": salary_max or "",
            "location": location or "",
            "url": url or "",
        }

        df = pd.concat([df, pd.DataFrame([new_job])], ignore_index=True)

        if self.save_data(df):
            self.console.print(f"[green]✅ Added job {job_id} ({company_name}) to database[/green]")
            return True
        return False

    def update_status(self, job_id: str, status: JobStatus) -> bool:
        """Update job status and relevant timestamps"""
        df = self.load_data()

        if df.empty or not self.job_exists(job_id):
            self.console.print(f"[red]❌ Job {job_id} not found in database[/red]")
            return False

        mask = df["job_id"] == str(job_id)
        df.loc[mask, "status"] = status.value

        # Update timestamps based on status
        current_date = datetime.now().strftime("%Y-%m-%d")
        if status == JobStatus.APPLIED:
            df.loc[mask, "date_applied"] = current_date
            # Ensure proper dtype for date columns
            df["date_applied"] = df["date_applied"].astype("object")
        elif status in [JobStatus.REJECTED, JobStatus.CLOSED]:
            df.loc[mask, "date_closed"] = current_date
            # Ensure proper dtype for date columns
            df["date_closed"] = df["date_closed"].astype("object")

        if self.save_data(df):
            company = df.loc[mask, "company_name"].iloc[0]
            self.console.print(f"[green]✅ Updated {job_id} ({company}) status to {status.value}[/green]")
            return True
        return False

    def update_job(self, job_id: str, **kwargs) -> bool:
        """Update job fields"""
        df = self.load_data()

        if df.empty or not self.job_exists(job_id):
            self.console.print(f"[red]❌ Job {job_id} not found in database[/red]")
            return False

        mask = df["job_id"] == str(job_id)

        for field, value in kwargs.items():
            if field in df.columns:
                if isinstance(value, Enum):
                    df.loc[mask, field] = value.value
                else:
                    df.loc[mask, field] = value
                    # Ensure proper dtype for string fields
                    if field in ["notes", "location"]:
                        df[field] = df[field].astype("object")

        if self.save_data(df):
            company = df.loc[mask, "company_name"].iloc[0]
            self.console.print(f"[green]✅ Updated job {job_id} ({company})[/green]")
            return True
        return False

    def job_exists(self, job_id: str) -> bool:
        """Check if job exists in database"""
        df = self.load_data()
        return not df.empty and str(job_id) in df["job_id"].astype(str).values

    def get_job(self, job_id: str) -> Optional[dict]:
        """Get job record by ID"""
        df = self.load_data()

        if df.empty or not self.job_exists(job_id):
            return None

        job_row = df[df["job_id"] == str(job_id)].iloc[0]
        return job_row.to_dict()

    def get_jobs_by_status(self, status: JobStatus) -> pd.DataFrame:
        """Get all jobs with specific status"""
        df = self.load_data()
        if df.empty:
            return df
        return df[df["status"] == status.value]

    def get_jobs_by_company(self, company_name: str) -> pd.DataFrame:
        """Get all jobs for specific company"""
        df = self.load_data()
        if df.empty:
            return df
        return df[df["company_name"].str.contains(company_name, case=False, na=False)]

    def get_statistics(self) -> dict:
        """Get application statistics"""
        df = self.load_data()

        if df.empty:
            return {"total_jobs": 0, "by_status": {}, "by_priority": {}, "by_company": {}, "application_rate": 0.0}

        stats = {
            "total_jobs": len(df),
            "by_status": df["status"].value_counts().to_dict(),
            "by_priority": df["priority"].value_counts().to_dict(),
            "by_company": df["company_name"].value_counts().head(10).to_dict(),
            "application_rate": (df["status"] == JobStatus.APPLIED.value).sum() / len(df) * 100,
        }

        return stats

    def display_jobs(self, status_filter: Optional[JobStatus] = None, limit: int = 50) -> None:
        """Display jobs in a formatted table"""
        df = self.load_data()

        if df.empty:
            self.console.print("[yellow]No jobs in database[/yellow]")
            return

        if status_filter:
            df = df[df["status"] == status_filter.value]
            title = f"Jobs - {status_filter.value.title()}"
        else:
            title = "All Jobs"

        if df.empty:
            self.console.print(f"[yellow]No jobs with status '{status_filter.value}'[/yellow]")
            return

        # Limit results
        df = df.head(limit)

        table = Table(title=title)
        table.add_column("Job ID", style="cyan")
        table.add_column("Company", style="green")
        table.add_column("Title", style="blue")
        table.add_column("Status", style="yellow")
        table.add_column("Priority", style="red")
        table.add_column("Discovered", style="dim")

        for _, row in df.iterrows():
            table.add_row(
                str(row["job_id"]),
                row["company_name"][:30] + "..." if len(row["company_name"]) > 30 else row["company_name"],
                row["job_title"][:40] + "..." if len(row["job_title"]) > 40 else row["job_title"],
                row["status"],
                row["priority"],
                row["date_discovered"],
            )

        self.console.print(table)

    def display_statistics(self) -> None:
        """Display application statistics in formatted tables"""
        stats = self.get_statistics()

        # Overview table
        overview_table = Table(title="📊 Application Statistics Overview")
        overview_table.add_column("Metric", style="cyan")
        overview_table.add_column("Value", style="green")

        overview_table.add_row("Total Jobs", str(stats["total_jobs"]))
        overview_table.add_row("Application Rate", f"{stats['application_rate']:.1f}%")

        self.console.print(overview_table)

        # Status breakdown
        if stats["by_status"]:
            status_table = Table(title="📈 Jobs by Status")
            status_table.add_column("Status", style="yellow")
            status_table.add_column("Count", style="green")
            status_table.add_column("Percentage", style="blue")

            for status, count in stats["by_status"].items():
                percentage = (count / stats["total_jobs"]) * 100
                status_table.add_row(status.title(), str(count), f"{percentage:.1f}%")

            self.console.print(status_table)

        # Top companies
        if stats["by_company"]:
            company_table = Table(title="🏢 Top Companies (by job count)")
            company_table.add_column("Company", style="blue")
            company_table.add_column("Jobs", style="green")

            for company, count in list(stats["by_company"].items())[:10]:
                company_table.add_row(company, str(count))

            self.console.print(company_table)

    def cleanup_old_jobs(self, days_old: int = 30) -> int:
        """Remove jobs older than specified days that are closed/rejected"""
        df = self.load_data()

        if df.empty:
            return 0

        cutoff_date = pd.Timestamp.now() - pd.Timedelta(days=days_old)

        # Convert date columns to datetime
        df["date_discovered"] = pd.to_datetime(df["date_discovered"], errors="coerce")

        # Jobs to remove: old and closed/rejected
        old_closed_jobs = df[
            (df["date_discovered"] < cutoff_date)
            & df["status"].isin([JobStatus.CLOSED.value, JobStatus.REJECTED.value])
        ]

        removed_count = len(old_closed_jobs)

        if removed_count > 0:
            # Keep jobs that don't match the removal criteria
            df_cleaned = df[
                ~(
                    (df["date_discovered"] < cutoff_date)
                    & df["status"].isin([JobStatus.CLOSED.value, JobStatus.REJECTED.value])
                )
            ]

            # Convert dates back to string format using .copy() to avoid SettingWithCopyWarning
            df_cleaned = df_cleaned.copy()
            df_cleaned["date_discovered"] = df_cleaned["date_discovered"].dt.strftime("%Y-%m-%d")

            if self.save_data(df_cleaned):
                self.console.print(f"[green]✅ Cleaned up {removed_count} old jobs[/green]")
                return removed_count

        return 0
