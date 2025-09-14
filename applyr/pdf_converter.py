"""PDF converter module for converting markdown files to PDF with custom CSS styling"""

from pathlib import Path
from typing import Optional, Union
import markdown
from rich.console import Console

# Try to import weasyprint, fall back to reportlab if it fails
try:
    from weasyprint import HTML, CSS
    WEASYPRINT_AVAILABLE = True
    # WeasyPrint 66.0+ has integrated font handling
    try:
        from weasyprint.fonts import FontConfiguration
        FONT_CONFIG_AVAILABLE = True
    except ImportError:
        # WeasyPrint 66.0+ integrated font handling
        FontConfiguration = None
        FONT_CONFIG_AVAILABLE = False
except ImportError:
    WEASYPRINT_AVAILABLE = False
    FONT_CONFIG_AVAILABLE = False
    FontConfiguration = None

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import inch
    import html
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


class PDFConverter:
    """Convert markdown files to PDF with custom CSS styling support"""
    
    def __init__(self, console: Optional[Console] = None):
        """Initialize PDF converter with optional console for output"""
        self.console = console or Console()
        self.md = markdown.Markdown(extensions=['extra', 'codehilite', 'toc', 'tables'])
        self.font_config = FontConfiguration() if FONT_CONFIG_AVAILABLE else None
        
    def convert_markdown_to_pdf(
        self, 
        markdown_file: Path,
        output_pdf: Path,
        css_file: Optional[Path] = None,
        css_string: Optional[str] = None
    ) -> bool:
        """
        Convert a markdown file to PDF with optional CSS styling
        
        Args:
            markdown_file: Path to the input markdown file
            output_pdf: Path for the output PDF file
            css_file: Optional path to a CSS file for styling
            css_string: Optional CSS string for inline styling
            
        Returns:
            bool: True if conversion successful, False otherwise
        """
        # Read markdown content
        if not markdown_file.exists():
            self.console.print(f"[red]❌ Error: Markdown file not found: {markdown_file}[/red]")
            return False
            
        with open(markdown_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Try WeasyPrint first if available
        if WEASYPRINT_AVAILABLE:
            try:
                return self._convert_with_weasyprint(markdown_file, markdown_content, output_pdf, css_file, css_string)
            except Exception as e:
                self.console.print(f"[yellow]⚠️  WeasyPrint failed: {e}[/yellow]")
                self.console.print("[blue]🔄 Trying fallback method with ReportLab...[/blue]")
        
        # Fall back to ReportLab
        if REPORTLAB_AVAILABLE:
            try:
                return self._convert_with_reportlab(markdown_file, markdown_content, output_pdf)
            except Exception as e:
                self.console.print(f"[red]❌ ReportLab fallback failed: {e}[/red]")
                return False
        
        self.console.print("[red]❌ No PDF conversion libraries available. Please install weasyprint or reportlab[/red]")
        return False
    
    def _convert_with_weasyprint(
        self, 
        markdown_file: Path, 
        markdown_content: str, 
        output_pdf: Path, 
        css_file: Optional[Path] = None, 
        css_string: Optional[str] = None
    ) -> bool:
        """Convert using WeasyPrint with enhanced link and font handling"""
        # Convert markdown to HTML
        html_content = self.md.convert(markdown_content)
        
        # Enhanced HTML structure for WeasyPrint link compatibility
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <base href="https://colemorton.com/">
            <title>{markdown_file.stem}</title>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        # Create HTML object with proper base_url for link resolution
        html = HTML(string=full_html, base_url='https://colemorton.com/')
        
        # Prepare CSS with WeasyPrint link optimization
        css_objects = []
        
        # Add WeasyPrint-specific link handling CSS
        weasyprint_css = self._get_weasyprint_optimized_css()
        
        # Add default CSS for better formatting
        if self.font_config:
            # WeasyPrint with FontConfiguration
            css_objects.append(CSS(string=weasyprint_css, font_config=self.font_config))
            css_objects.append(CSS(string=self._get_default_css(), font_config=self.font_config))
            
            # Add custom CSS from file if provided
            if css_file and css_file.exists():
                css_objects.append(CSS(filename=str(css_file), font_config=self.font_config))
            
            # Add inline CSS if provided
            if css_string:
                css_objects.append(CSS(string=css_string, font_config=self.font_config))
        else:
            # WeasyPrint 66.0+ integrated font handling
            css_objects.append(CSS(string=weasyprint_css))
            css_objects.append(CSS(string=self._get_default_css()))
            
            # Add custom CSS from file if provided
            if css_file and css_file.exists():
                css_objects.append(CSS(filename=str(css_file)))
            
            # Add inline CSS if provided
            if css_string:
                css_objects.append(CSS(string=css_string))
        
        # Generate PDF with optimization settings
        output_pdf.parent.mkdir(parents=True, exist_ok=True)
        
        # Write PDF with enhanced settings for links and fonts
        write_options = {
            'stylesheets': css_objects,
            'optimize_images': True,
            'presentational_hints': True
        }
        
        if self.font_config:
            write_options['font_config'] = self.font_config
            
        html.write_pdf(output_pdf, **write_options)
        
        self.console.print(f"[green]✅ PDF created with WeasyPrint: {output_pdf}[/green]")
        return True
    
    def _convert_with_reportlab(self, markdown_file: Path, markdown_content: str, output_pdf: Path) -> bool:
        """Simple conversion using ReportLab"""
        # Convert markdown to HTML first
        html_content = self.md.convert(markdown_content)
        
        # Create PDF
        output_pdf.parent.mkdir(parents=True, exist_ok=True)
        doc = SimpleDocTemplate(str(output_pdf), pagesize=A4, 
                               rightMargin=72, leftMargin=72, 
                               topMargin=72, bottomMargin=18)
        
        # Get styles
        styles = getSampleStyleSheet()
        story = []
        
        # Parse HTML and convert to reportlab paragraphs
        # This is a simple implementation - strip HTML tags and create paragraphs
        import re
        
        # Remove HTML tags for simple text extraction
        text_content = re.sub('<[^<]+?>', '', html_content)
        text_content = html.unescape(text_content)
        
        # Split into paragraphs and add to story
        paragraphs = text_content.split('\n\n')
        for para_text in paragraphs:
            if para_text.strip():
                # Determine style based on content
                if para_text.startswith('#'):
                    style = styles['Heading1']
                    para_text = para_text.lstrip('#').strip()
                elif para_text.strip().startswith('-') or para_text.strip().startswith('*'):
                    style = styles['Normal']
                else:
                    style = styles['Normal']
                
                para = Paragraph(para_text.strip(), style)
                story.append(para)
                story.append(Spacer(1, 12))
        
        # Build PDF
        doc.build(story)
        
        self.console.print(f"[green]✅ PDF created with ReportLab: {output_pdf}[/green]")
        return True
    
    def batch_convert(
        self,
        input_dir: Path,
        output_dir: Path,
        css_file: Optional[Path] = None,
        css_string: Optional[str] = None
    ) -> dict:
        """
        Convert all markdown files in a directory to PDFs
        
        Args:
            input_dir: Directory containing markdown files
            output_dir: Directory for output PDF files
            css_file: Optional CSS file for styling all PDFs
            css_string: Optional CSS string for styling all PDFs
            
        Returns:
            dict: Dictionary of {markdown_file: success_bool}
        """
        results = {}
        
        if not input_dir.exists():
            self.console.print(f"[red]❌ Error: Input directory not found: {input_dir}[/red]")
            return results
            
        markdown_files = list(input_dir.glob("*.md"))
        
        if not markdown_files:
            self.console.print(f"[yellow]⚠️  No markdown files found in: {input_dir}[/yellow]")
            return results
        
        self.console.print(f"[blue]🔄 Converting {len(markdown_files)} markdown files to PDF...[/blue]")
        
        for md_file in markdown_files:
            output_pdf = output_dir / f"{md_file.stem}.pdf"
            success = self.convert_markdown_to_pdf(
                md_file,
                output_pdf,
                css_file,
                css_string
            )
            results[md_file] = success
            
        return results
    
    def _get_weasyprint_optimized_css(self) -> str:
        """Get WeasyPrint-specific CSS for enhanced link and font handling"""
        return """
        /* WeasyPrint Link Optimization - Force clickable links */
        a[href] {
            -weasy-link: attr(href) !important;
            cursor: pointer !important;
            text-decoration: underline;
            color: inherit;
        }
        
        /* Ensure proper link rendering */
        a:link, a:visited {
            color: inherit;
            text-decoration: underline;
        }
        
        /* Remove any interfering print CSS */
        a[href]:after {
            content: "" !important;
        }
        
        @media print {
            a[href]:after {
                content: "" !important;
            }
        }
        
        /* Font rendering optimization */
        body {
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            font-feature-settings: "liga" 1, "kern" 1;
        }
        """
    
    def _get_default_css(self) -> str:
        """Get default CSS for basic PDF styling with Heebo font support"""
        return """
        /* Heebo font family declarations */
        @font-face {
            font-family: 'Heebo';
            src: url('file:///Users/colemorton/Library/Fonts/Heebo[wght].ttf') format('truetype-variations');
            font-weight: 100 900;
            font-style: normal;
        }
        
        body {
            font-family: 'Heebo', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 
                         'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        
        h1, h2, h3, h4, h5, h6 {
            margin-top: 24px;
            margin-bottom: 16px;
            font-weight: 600;
            line-height: 1.25;
        }
        
        h1 { font-size: 2em; border-bottom: 1px solid #eee; padding-bottom: 0.3em; }
        h2 { font-size: 1.5em; }
        h3 { font-size: 1.25em; }
        
        p {
            margin-top: 0;
            margin-bottom: 16px;
        }
        
        code {
            background-color: #f6f8fa;
            padding: 0.2em 0.4em;
            border-radius: 3px;
            font-size: 85%;
        }
        
        pre {
            background-color: #f6f8fa;
            padding: 16px;
            overflow: auto;
            font-size: 85%;
            line-height: 1.45;
            border-radius: 6px;
        }
        
        blockquote {
            padding: 0 1em;
            color: #6a737d;
            border-left: 0.25em solid #dfe2e5;
            margin: 0 0 16px 0;
        }
        
        ul, ol {
            padding-left: 2em;
            margin-top: 0;
            margin-bottom: 16px;
        }
        
        table {
            border-collapse: collapse;
            margin-bottom: 16px;
            width: 100%;
        }
        
        table th, table td {
            padding: 6px 13px;
            border: 1px solid #dfe2e5;
        }
        
        table tr:nth-child(2n) {
            background-color: #f6f8fa;
        }
        
        a {
            color: #0366d6;
            text-decoration: none;
        }
        
        a:hover {
            text-decoration: underline;
        }
        
        img {
            max-width: 100%;
            box-sizing: content-box;
        }
        
        hr {
            height: 0.25em;
            padding: 0;
            margin: 24px 0;
            background-color: #e1e4e8;
            border: 0;
        }
        """
        
    def validate_pdf_quality(self, pdf_path: Path) -> dict:
        """
        Validate PDF quality and provide optimization metrics
        
        Args:
            pdf_path: Path to the PDF file to validate
            
        Returns:
            dict: Quality metrics and validation results
        """
        if not pdf_path.exists():
            return {
                'valid': False,
                'error': 'PDF file not found',
                'metrics': {}
            }
        
        try:
            import os
            file_size = os.path.getsize(pdf_path)
            
            # Basic quality metrics
            metrics = {
                'file_size_bytes': file_size,
                'file_size_kb': round(file_size / 1024, 2),
                'file_size_mb': round(file_size / (1024 * 1024), 2),
            }
            
            # File size assessment
            if file_size < 50 * 1024:  # Less than 50KB
                size_rating = 'minimal'
                size_note = 'Very compact, may lack styling'
            elif file_size < 200 * 1024:  # Less than 200KB
                size_rating = 'optimal'
                size_note = 'Good balance of quality and file size'
            elif file_size < 500 * 1024:  # Less than 500KB
                size_rating = 'good'
                size_note = 'Rich styling with reasonable file size'
            elif file_size < 1024 * 1024:  # Less than 1MB
                size_rating = 'large'
                size_note = 'High-quality styling, larger file size'
            else:
                size_rating = 'oversized'
                size_note = 'Very large file, consider optimization'
            
            metrics.update({
                'size_rating': size_rating,
                'size_note': size_note,
            })
            
            # Try to get PDF metadata if PyPDF2 is available
            try:
                import PyPDF2
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    metrics.update({
                        'page_count': len(pdf_reader.pages),
                        'has_metadata': bool(pdf_reader.metadata),
                        'encrypted': pdf_reader.is_encrypted,
                    })
                    
                    # Calculate pages per MB for density assessment
                    if metrics['file_size_mb'] > 0:
                        metrics['pages_per_mb'] = round(metrics['page_count'] / metrics['file_size_mb'], 1)
                    
            except ImportError:
                self.console.print("[yellow]💡 Install PyPDF2 for enhanced PDF validation: pip install PyPDF2[/yellow]")
                metrics.update({
                    'page_count': 'unknown',
                    'has_metadata': 'unknown',
                    'encrypted': 'unknown',
                })
                
            except Exception as e:
                metrics.update({
                    'pdf_error': str(e),
                    'page_count': 'error',
                })
            
            # Quality score calculation (0-10)
            quality_score = 10
            
            # Deduct points for various issues
            if size_rating == 'minimal':
                quality_score -= 3
            elif size_rating == 'oversized':
                quality_score -= 2
                
            if file_size < 10 * 1024:  # Less than 10KB is suspicious
                quality_score -= 5
                
            metrics['quality_score'] = max(0, quality_score)
            
            return {
                'valid': True,
                'metrics': metrics,
                'recommendations': self._get_optimization_recommendations(metrics)
            }
            
        except Exception as e:
            return {
                'valid': False,
                'error': str(e),
                'metrics': {}
            }
    
    def _get_optimization_recommendations(self, metrics: dict) -> list:
        """Generate optimization recommendations based on metrics"""
        recommendations = []
        
        size_mb = metrics.get('file_size_mb', 0)
        size_rating = metrics.get('size_rating', '')
        
        if size_rating == 'oversized':
            recommendations.extend([
                "Consider using minimal.css or ats.css for smaller file size",
                "Remove unused CSS rules and optimize images",
                "Use system fonts instead of embedded fonts"
            ])
        elif size_rating == 'minimal':
            recommendations.extend([
                "File may lack proper styling - consider using professional.css",
                "Verify that WeasyPrint is being used instead of ReportLab fallback"
            ])
        elif size_rating == 'optimal':
            recommendations.append("File size is optimal for most use cases")
        
        quality_score = metrics.get('quality_score', 0)
        if quality_score < 7:
            recommendations.append("Consider regenerating PDF with different template")
        
        return recommendations