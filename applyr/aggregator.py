"""Job description aggregator with Rich console integration"""

import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from rich.console import Console
from rich.progress import track
from rich.table import Table

import logging
logger = logging.getLogger(__name__)


class JobDescriptionAggregator:
    """Aggregates individual job description files into a single markdown file."""

    def discover_job_files(self, input_dir: Path) -> List[Path]:
        """Discover all job description markdown files in the input directory."""
        try:
            if not input_dir.exists():
                raise ValueError(f"Input directory does not exist: {input_dir}")
            
            job_files = []
            for file_path in input_dir.glob("*.md"):
                if re.match(r'^\d+_', file_path.name):
                    job_files.append(file_path)
            
            job_files.sort(key=lambda x: x.name)
            return job_files
        except Exception as e:
            logger.error(f"Error discovering job files: {e}")
            raise

    def parse_job_file(self, file_path: Path) -> Optional[Dict]:
        """Parse a single job description file and extract metadata and content."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            job_data = {
                'file_path': file_path,
                'filename': file_path.name,
                'title': 'Unknown Job',
                'company': 'Unknown Company',
                'job_id': 'Unknown',
                'source': 'SEEK',
                'scraped_date': 'Unknown',
                'content': content
            }
            
            id_match = re.match(r'^(\d+)_', file_path.name)
            if id_match:
                job_data['job_id'] = id_match.group(1)
            
            title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
            if title_match:
                job_data['title'] = title_match.group(1).strip()
            
            company_match = re.search(r'\*\*Company:\*\* (.+)$', content, re.MULTILINE)
            if company_match:
                job_data['company'] = company_match.group(1).strip()
            
            scraped_match = re.search(r'\*\*Scraped:\*\* (.+)$', content, re.MULTILINE)
            if scraped_match:
                job_data['scraped_date'] = scraped_match.group(1).strip()
            
            content_match = re.search(r'^---\n\n(.+)', content, re.MULTILINE | re.DOTALL)
            if content_match:
                job_data['description'] = content_match.group(1).strip()
            else:
                job_data['description'] = content
            
            return job_data
        except Exception as e:
            logger.error(f"Error parsing job file {file_path}: {e}")
            return None

    def generate_unique_title(self, job_data: Dict) -> str:
        """Generate a unique title for the job in the aggregated file."""
        return f"{job_data['title']} at {job_data['company']} (ID: {job_data['job_id']})"

    def generate_anchor_link(self, title: str) -> str:
        """Generate a markdown anchor link from a title."""
        anchor = re.sub(r'[^\w\s-]', '', title.lower())
        anchor = re.sub(r'[\s_]+', '-', anchor)
        return anchor.strip('-')

    def generate_summary_stats(self, jobs_data: List[Dict]) -> Dict:
        """Generate summary statistics for the job descriptions."""
        if not jobs_data:
            return {}
        
        companies = [job['company'] for job in jobs_data]
        company_counts = Counter(companies)
        
        job_levels = []
        for job in jobs_data:
            title = job['title'].lower()
            if 'senior' in title:
                job_levels.append('Senior')
            elif 'junior' in title or 'graduate' in title:
                job_levels.append('Junior')
            elif 'lead' in title or 'principal' in title:
                job_levels.append('Lead/Principal')
            else:
                job_levels.append('Mid-level')
        
        level_counts = Counter(job_levels)
        
        tech_keywords = ['typescript', 'javascript', 'react', 'node', 'aws', 'python', 'java', 'php', 'wordpress']
        tech_mentions = Counter()
        
        for job in jobs_data:
            title_lower = job['title'].lower()
            description_lower = job['description'].lower() if 'description' in job else ''
            combined_text = f"{title_lower} {description_lower}"
            
            for tech in tech_keywords:
                if tech in combined_text:
                    tech_mentions[tech.title()] += 1
        
        return {
            'total_jobs': len(jobs_data),
            'unique_companies': len(company_counts),
            'company_counts': dict(company_counts.most_common(5)),
            'job_level_distribution': dict(level_counts),
            'technology_mentions': dict(tech_mentions.most_common(10))
        }

    def generate_aggregate_content(self, jobs_data: List[Dict], stats: Dict) -> str:
        """Generate the aggregated markdown content."""
        current_date = datetime.now()
        date_str = current_date.strftime('%Y-%m-%d')
        
        markdown_content = []
        
        markdown_content.extend([
            f"# Job Descriptions Aggregate - {date_str}",
            "",
            f"**Generated:** {current_date.strftime('%Y-%m-%d %H:%M:%S')}  ",
            f"**Total Jobs:** {stats['total_jobs']}  ",
            f"**Unique Companies:** {stats['unique_companies']}  ",
            f"**Source:** SEEK Job Scraper  ",
            "",
            "---",
            ""
        ])
        
        if stats:
            markdown_content.extend([
                "## Summary Statistics",
                "",
                f"- **Total Job Postings:** {stats['total_jobs']}",
                f"- **Unique Companies:** {stats['unique_companies']}",
                ""
            ])
            
            if stats['job_level_distribution']:
                markdown_content.append("### Job Level Distribution")
                for level, count in stats['job_level_distribution'].items():
                    markdown_content.append(f"- **{level}:** {count}")
                markdown_content.append("")
            
            if stats['company_counts']:
                markdown_content.append("### Top Companies (by job count)")
                for company, count in stats['company_counts'].items():
                    markdown_content.append(f"- **{company}:** {count} job{'s' if count > 1 else ''}")
                markdown_content.append("")
            
            if stats['technology_mentions']:
                markdown_content.append("### Technology Mentions")
                for tech, count in stats['technology_mentions'].items():
                    markdown_content.append(f"- **{tech}:** {count} mention{'s' if count > 1 else ''}")
                markdown_content.append("")
            
            markdown_content.extend(["---", ""])
        
        markdown_content.extend([
            "## Table of Contents",
            ""
        ])
        
        for i, job_data in enumerate(jobs_data, 1):
            unique_title = self.generate_unique_title(job_data)
            anchor = self.generate_anchor_link(unique_title)
            markdown_content.append(f"{i}. [{unique_title}](#{anchor})")
        
        markdown_content.extend(["", "---", ""])
        
        markdown_content.append("## Job Descriptions")
        markdown_content.append("")
        
        for i, job_data in enumerate(jobs_data, 1):
            unique_title = self.generate_unique_title(job_data)
            anchor = self.generate_anchor_link(unique_title)
            
            markdown_content.extend([
                f"### {i}. {unique_title} {{#{anchor}}}",
                "",
                f"**Company:** {job_data['company']}  ",
                f"**Job ID:** {job_data['job_id']}  ",
                f"**Source:** {job_data['source']}  ",
                f"**Scraped:** {job_data['scraped_date']}  ",
                f"**Original File:** `{job_data['filename']}`",
                "",
                "---",
                "",
                job_data['description'],
                "",
                "---",
                ""
            ])
        
        markdown_content.extend([
            "",
            f"*Aggregated from {len(jobs_data)} individual job description files*  ",
            f"*Generated by Job Description Aggregator on {date_str}*"
        ])
        
        return '\n'.join(markdown_content)

    def aggregate_jobs(self, input_dir: Path, output_file: Path, console: Console) -> Tuple[bool, Dict]:
        """Aggregate all job descriptions into a single markdown file with Rich output."""
        try:
            job_files = self.discover_job_files(input_dir)
            if not job_files:
                console.print("[red]❌ No job description files found[/red]")
                return False, {}
            
            console.print(f"[blue]📂 Found {len(job_files)} job files[/blue]")
            
            jobs_data = []
            failed_files = []
            
            for file_path in track(job_files, description="Parsing job files..."):
                job_data = self.parse_job_file(file_path)
                if job_data:
                    jobs_data.append(job_data)
                else:
                    failed_files.append(file_path.name)
            
            if not jobs_data:
                console.print("[red]❌ No job files could be parsed successfully[/red]")
                return False, {}
            
            console.print(f"[green]✅ Successfully parsed {len(jobs_data)} job descriptions[/green]")
            if failed_files:
                console.print(f"[yellow]⚠️ Failed to parse {len(failed_files)} files[/yellow]")
            
            stats = self.generate_summary_stats(jobs_data)
            
            markdown_content = self.generate_aggregate_content(jobs_data, stats)
            
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            console.print(f"[green]✅ Aggregated {len(jobs_data)} job descriptions to: {output_file}[/green]")
            return True, stats
            
        except Exception as e:
            console.print(f"[red]❌ Error during aggregation: {e}[/red]")
            return False, {}


def aggregate_job_data(input_dir: Path, output_file: Optional[Path], date: Optional[str], 
                      verbose: bool, console: Console) -> bool:
    """Main aggregation function called from CLI."""
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    if not input_dir.exists():
        console.print(f"[red]❌ Input directory not found: {input_dir}[/red]")
        return False
    
    if not output_file:
        if date:
            try:
                datetime.strptime(date, '%Y%m%d')
                date_str = date
            except ValueError:
                console.print("[red]❌ Invalid date format. Use YYYYMMDD format.[/red]")
                return False
        else:
            date_str = datetime.now().strftime('%Y%m%d')
        
        output_filename = f"{date_str}_job_descriptions_aggregate.md"
        output_file = input_dir / output_filename
    
    console.print(f"[blue]📁 Input directory: {input_dir}[/blue]")
    console.print(f"[blue]📄 Output file: {output_file}[/blue]")
    
    aggregator = JobDescriptionAggregator()
    success, stats = aggregator.aggregate_jobs(input_dir, output_file, console)
    
    if success and stats:
        table = Table(title="📊 Aggregation Summary")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Total Jobs", str(stats['total_jobs']))
        table.add_row("Unique Companies", str(stats['unique_companies']))
        
        if stats['technology_mentions']:
            top_tech = list(stats['technology_mentions'].items())[0]
            table.add_row("Top Technology", f"{top_tech[0]} ({top_tech[1]} mentions)")
        
        console.print(table)
    
    return success