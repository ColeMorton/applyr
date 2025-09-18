#!/usr/bin/env python3
"""
Generate test PDFs with updated brand text styling to validate centering and 2x size increase.

This script generates PDFs using all 6 CSS templates to verify:
1. SVG brand text is horizontally centered
2. Brand text dimensions are 2x larger (280pt x 40pt)
"""

import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table

# Add the applyr module to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from applyr.pdf_converter import PDFConverter
except ImportError:
    print("❌ Error: Could not import PDFConverter. Please ensure you're running from the applyr directory.")
    sys.exit(1)


def main():
    """Generate test PDFs for all CSS templates"""
    console = Console()
    
    # Paths
    project_root = Path(__file__).parent.parent
    resume_md = project_root / "data" / "raw" / "resume.md"
    styles_dir = project_root / "applyr" / "styles"
    output_dir = project_root / "data" / "outputs" / "brand-text-test"
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # CSS templates to test
    css_templates = [
        "executive.css",
        "sensylate.css", 
        "heebo-premium.css",
        "professional.css",
        "minimal.css",
        "ats.css"
    ]
    
    console.print("[blue]🎯 Generating test PDFs to validate brand text centering and 2x size increase...[/blue]")
    console.print(f"[dim]Resume source: {resume_md}[/dim]")
    console.print(f"[dim]Output directory: {output_dir}[/dim]")
    console.print()
    
    # Check if resume file exists
    if not resume_md.exists():
        console.print(f"[red]❌ Error: Resume file not found: {resume_md}[/red]")
        return 1
    
    # Initialize PDF converter
    pdf_converter = PDFConverter(console)
    
    # Results tracking
    results = []
    successful_conversions = 0
    
    # Generate PDFs for each template
    for template_name in css_templates:
        css_file = styles_dir / template_name
        output_pdf = output_dir / f"resume_{template_name.replace('.css', '')}.pdf"
        
        if not css_file.exists():
            console.print(f"[yellow]⚠️  CSS template not found: {css_file}[/yellow]")
            results.append({
                'template': template_name,
                'status': 'CSS not found',
                'output': str(output_pdf),
                'file_size': 'N/A'
            })
            continue
        
        console.print(f"[blue]🔄 Generating PDF with {template_name}...[/blue]")
        
        # Convert to PDF
        success = pdf_converter.convert_markdown_to_pdf(
            resume_md,
            output_pdf,
            css_file=css_file
        )
        
        if success:
            successful_conversions += 1
            # Get file size
            try:
                file_size_kb = round(output_pdf.stat().st_size / 1024, 1)
                file_size_str = f"{file_size_kb} KB"
            except:
                file_size_str = "Unknown"
                
            results.append({
                'template': template_name,
                'status': '✅ Success',
                'output': str(output_pdf),
                'file_size': file_size_str
            })
        else:
            results.append({
                'template': template_name,
                'status': '❌ Failed',
                'output': str(output_pdf),
                'file_size': 'N/A'
            })
    
    console.print()
    
    # Create results table
    table = Table(title="PDF Generation Results", show_header=True, header_style="bold magenta")
    table.add_column("Template", style="cyan", no_wrap=True)
    table.add_column("Status", no_wrap=True)
    table.add_column("File Size", justify="right")
    table.add_column("Output Path", style="dim")
    
    for result in results:
        table.add_row(
            result['template'],
            result['status'],
            result['file_size'],
            result['output']
        )
    
    console.print(table)
    console.print()
    
    # Summary
    total_templates = len(css_templates)
    if successful_conversions == total_templates:
        console.print(f"[green]🎉 All {successful_conversions}/{total_templates} PDFs generated successfully![/green]")
    else:
        console.print(f"[yellow]⚠️  {successful_conversions}/{total_templates} PDFs generated successfully.[/yellow]")
    
    console.print(f"\n[blue]📁 Test PDFs saved to: {output_dir}[/blue]")
    
    # Instructions for manual verification
    console.print("\n[bold]Manual Verification Steps:[/bold]")
    console.print("1. Open each generated PDF")
    console.print("2. Verify 'Cole Morton' brand text is horizontally centered in the header")
    console.print("3. Verify brand text appears 2x larger than before (should be quite prominent)")
    console.print("4. Compare across different templates for consistency")
    
    # Expected specifications
    console.print("\n[bold]Expected Brand Text Specifications:[/bold]")
    console.print("• Position: Horizontally centered (background-position: center center)")
    console.print("• Dimensions: 280pt × 40pt (doubled from 140pt × 20pt)")  
    console.print("• Aspect Ratio: 7:1 (maintained from original SVG)")
    console.print("• Implementation: SVG background image with hidden text for accessibility")
    
    return 0 if successful_conversions == total_templates else 1


if __name__ == "__main__":
    sys.exit(main())