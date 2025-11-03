"""HTML processing module for auto-formatting and validation before PDF conversion"""

import contextlib
import json
from pathlib import Path
import subprocess
import tempfile
from typing import Any, Optional

from rich.console import Console


class HTMLProcessor:
    """Process HTML files with auto-formatting and validation for WeasyPrint compatibility"""

    def __init__(self, console: Optional[Console] = None, weasyprint_mode: Optional[bool] = None):
        """Initialize HTML processor with optional console for output"""
        self.console = console or Console()
        self._node_available = None
        self._html_eslint_available = None
        self._prettier_available = None
        self._weasyprint_mode = weasyprint_mode  # Explicit mode override

    @property
    def node_available(self) -> bool:
        """Check if Node.js is available in the system"""
        if self._node_available is None:
            try:
                result = subprocess.run(["node", "--version"], capture_output=True, text=True, timeout=5, check=False)
                self._node_available = result.returncode == 0
            except (subprocess.TimeoutExpired, FileNotFoundError):
                self._node_available = False
        return self._node_available

    @property
    def html_eslint_available(self) -> bool:
        """Check if html-eslint is available via npx"""
        if self._html_eslint_available is None:
            if not self.node_available:
                self._html_eslint_available = False
            else:
                try:
                    # Check if eslint and html-eslint plugin are available
                    result = subprocess.run(
                        ["npx", "eslint", "--version"], capture_output=True, text=True, timeout=10, check=False
                    )
                    eslint_available = result.returncode == 0

                    if eslint_available:
                        # Check if @html-eslint/eslint-plugin is installed
                        result = subprocess.run(
                            ["npm", "list", "-g", "@html-eslint/eslint-plugin"],
                            capture_output=True,
                            text=True,
                            timeout=10,
                            check=False,
                        )
                        self._html_eslint_available = result.returncode == 0
                    else:
                        self._html_eslint_available = False

                except (subprocess.TimeoutExpired, FileNotFoundError):
                    self._html_eslint_available = False
        return self._html_eslint_available

    @property
    def prettier_available(self) -> bool:
        """Check if Prettier is available via npx"""
        if self._prettier_available is None:
            if not self.node_available:
                self._prettier_available = False
            else:
                try:
                    result = subprocess.run(
                        ["npx", "prettier", "--version"], capture_output=True, text=True, timeout=10, check=False
                    )
                    self._prettier_available = result.returncode == 0
                except (subprocess.TimeoutExpired, FileNotFoundError):
                    self._prettier_available = False
        return self._prettier_available

    def _detect_weasyprint_context(self, html_content: str, source_path: Optional[Path] = None) -> bool:
        """Detect if HTML is being processed for WeasyPrint/PDF generation"""
        if self._weasyprint_mode is not None:
            return self._weasyprint_mode

        # Check for WeasyPrint-specific indicators
        weasyprint_indicators = [
            "brand-text",  # SVG brand text class
            "page-break-",  # CSS page break properties
            "data:image/svg+xml",  # SVG data URIs
            "@page",  # CSS paged media rules
            "new-page",  # Page break divs
            ".pdf",  # File extension context
        ]

        # Check source path for PDF-related indicators
        if source_path:
            path_str = str(source_path).lower()
            if any(indicator in path_str for indicator in ["resume", "cv", "pdf", "print"]):
                return True

        # Check HTML content for WeasyPrint-specific patterns
        html_lower = html_content.lower()
        indicator_count = sum(1 for indicator in weasyprint_indicators if indicator in html_lower)

        # If we find multiple WeasyPrint indicators, it's likely for PDF generation
        return indicator_count >= 2

    def _get_prettier_config_path(self, weasyprint_context: bool) -> Optional[Path]:
        """Get the appropriate Prettier configuration path based on context"""
        if weasyprint_context:
            config_path = Path(".prettierrc.weasyprint")
            if config_path.exists():
                return config_path.resolve()

        # Fall back to standard config
        standard_config = Path(".prettierrc")
        if standard_config.exists():
            return standard_config.resolve()

        return None

    def _get_eslint_config_path(self, weasyprint_context: bool) -> Optional[Path]:
        """Get the appropriate ESLint configuration path based on context"""
        if weasyprint_context:
            config_path = Path(".eslintrc.weasyprint.js")
            if config_path.exists():
                return config_path.resolve()

        # For non-WeasyPrint context, create standard config
        return None

    def process_html(
        self, html_content: str, source_path: Optional[Path] = None, skip_lint: bool = False
    ) -> tuple[str, list[str]]:
        """
        Process HTML content with auto-formatting and validation using professional tools

        Args:
            html_content: Raw HTML content to process
            source_path: Optional source file path for better error reporting
            skip_lint: Skip linting and formatting if True

        Returns:
            Tuple of (processed_html_content, list_of_changes_made)

        Raises:
            RuntimeError: If required tools (Prettier, html-eslint) are not available
        """
        if skip_lint:
            return html_content, []

        # Fail-fast: Check for required dependencies
        if not self.prettier_available:
            raise RuntimeError(
                "Prettier is required for HTML formatting but not available. " "Install with: npm install -g prettier"
            )

        if not self.html_eslint_available:
            raise RuntimeError(
                "html-eslint is required for HTML validation but not available. "
                "Install with: npm install -g eslint @html-eslint/eslint-plugin"
            )

        # Detect processing context
        weasyprint_context = self._detect_weasyprint_context(html_content, source_path)

        if weasyprint_context:
            self.console.print("[blue]🎯 WeasyPrint context detected - using PDF-optimized processing[/blue]")

        changes_made = []
        processed_content = html_content

        # Phase 1: Auto-formatting with Prettier
        processed_content, prettier_changes = self._format_with_prettier(
            processed_content, source_path, weasyprint_context
        )
        changes_made.extend(prettier_changes)

        # Phase 2: Linting and auto-fixing with html-eslint
        processed_content, eslint_changes = self._lint_with_html_eslint(
            processed_content, source_path, weasyprint_context
        )
        changes_made.extend(eslint_changes)

        # Phase 3: WeasyPrint-specific validation
        weasyprint_issues = self._validate_weasyprint_compatibility(processed_content)
        if weasyprint_issues:
            for issue in weasyprint_issues:
                self.console.print(f"[yellow]⚠️  WeasyPrint compatibility: {issue}[/yellow]")
                changes_made.append(f"WeasyPrint warning: {issue}")

        return processed_content, changes_made

    def _format_with_prettier(
        self, html_content: str, source_path: Optional[Path], weasyprint_context: bool = False
    ) -> tuple[str, list[str]]:
        """Format HTML using Prettier with context-appropriate configuration"""
        changes = []

        # Detect if this is an HTML fragment (missing DOCTYPE, html, body structure)
        is_fragment = self._is_html_fragment(html_content)
        original_content = html_content

        # If it's a fragment, wrap it in complete document structure for proper indentation
        if is_fragment:
            html_content = self._wrap_html_fragment(html_content)
            changes.append("HTML fragment wrapped for proper indentation processing")

        try:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as tmp_file:
                tmp_file.write(html_content)
                tmp_path = Path(tmp_file.name)

            # Get appropriate Prettier configuration
            prettier_config = self._get_prettier_config_path(weasyprint_context)

            if prettier_config:
                cmd = ["npx", "prettier", "--write", "--config", str(prettier_config), str(tmp_path)]
                if weasyprint_context:
                    self.console.print(f"[dim]Using WeasyPrint-optimized Prettier config: {prettier_config.name}[/dim]")
            else:
                cmd = ["npx", "prettier", "--write", str(tmp_path)]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=Path.cwd(),
                check=False,  # Ensure we're in the project directory
            )

            if result.returncode == 0:
                # Read the formatted content
                formatted_content = tmp_path.read_text(encoding="utf-8")

                # If we wrapped a fragment, extract just the body content with preserved indentation
                if is_fragment:
                    formatted_content = self._extract_body_content(formatted_content)

                # Apply WeasyPrint compatibility validation only
                weasyprint_issues = self._validate_weasyprint_compatibility(formatted_content)
                if weasyprint_issues:
                    for issue in weasyprint_issues:
                        self.console.print(f"[yellow]⚠️  WeasyPrint compatibility: {issue}[/yellow]")
                        changes.append(f"WeasyPrint warning: {issue}")

                # Compare without stripping to catch formatting changes
                if formatted_content != original_content:
                    changes.append("HTML formatted with Prettier")
                return formatted_content, changes
            else:
                self.console.print(f"[yellow]⚠️  Prettier formatting failed: {result.stderr}[/yellow]")
                return original_content, changes

        except Exception as e:
            self.console.print(f"[yellow]⚠️  Prettier formatting error: {e}[/yellow]")
            return original_content, changes
        finally:
            # Clean up temp file
            if "tmp_path" in locals():
                with contextlib.suppress(Exception):
                    tmp_path.unlink()

    def _is_html_fragment(self, html_content: str) -> bool:
        """Detect if HTML content is a fragment (missing DOCTYPE, html, body structure)"""
        content_lower = html_content.lower().strip()

        # Check for DOCTYPE declaration
        has_doctype = content_lower.startswith("<!doctype")

        # Check for html tag
        has_html_tag = "<html" in content_lower

        # Check for body tag
        has_body_tag = "<body" in content_lower

        # If missing any of these, it's considered a fragment
        return not (has_doctype and has_html_tag and has_body_tag)

    def _wrap_html_fragment(self, fragment_content: str) -> str:
        """Wrap HTML fragment in complete document structure for proper Prettier processing"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Fragment Processing</title>
</head>
<body>
{fragment_content}
</body>
</html>"""

    def _extract_body_content(self, complete_html: str) -> str:
        """Extract body content from complete HTML document, preserving Prettier's native indentation"""
        import re

        # Find the body content between <body> and </body> tags
        # Use DOTALL flag to match newlines with .
        body_pattern = r"<body[^>]*>(.*?)</body>"
        match = re.search(body_pattern, complete_html, re.DOTALL | re.IGNORECASE)

        if match:
            body_content = match.group(1)

            # Only remove leading/trailing newlines, preserve Prettier's native indentation
            # Strip only newlines from start and end, not spaces
            body_content = body_content.strip("\n\r")

            # Let Prettier handle all indentation - no custom logic needed
            return body_content
        else:
            # Fallback: if we can't find body tags, return original content
            return complete_html

    def _lint_with_html_eslint(
        self, html_content: str, source_path: Optional[Path], weasyprint_context: bool = False
    ) -> tuple[str, list[str]]:
        """Lint and auto-fix HTML using html-eslint"""
        changes = []

        try:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as tmp_file:
                tmp_file.write(html_content)
                tmp_path = Path(tmp_file.name)

            # Get appropriate ESLint configuration
            eslint_config = self._get_eslint_config_path(weasyprint_context)

            if eslint_config:
                # Use the appropriate configuration file
                cmd = ["npx", "eslint", "--fix", "--config", str(eslint_config), str(tmp_path)]
                if weasyprint_context:
                    self.console.print(f"[dim]Using WeasyPrint-optimized ESLint config: {eslint_config.name}[/dim]")
            else:
                # Fall back to inline config for non-WeasyPrint context
                config = {
                    "plugins": ["@html-eslint"],
                    "parser": "@html-eslint/parser",
                    "rules": {
                        "@html-eslint/require-doctype": "error",
                        "@html-eslint/require-lang": "error",
                        "@html-eslint/require-meta-charset": "error",
                        "@html-eslint/require-meta-viewport": "warn",
                        "@html-eslint/no-duplicate-id": "error",
                        "@html-eslint/no-inline-styles": "off",
                        "@html-eslint/require-img-alt": "warn",
                        "@html-eslint/no-obsolete-tags": "error",
                        "@html-eslint/indent": ["error", 2],
                        "@html-eslint/element-newline": ["error", {"skip": ["pre", "code"], "inline": ["$inline"]}],
                        "@html-eslint/no-extra-spacing-attrs": "error",
                        "@html-eslint/no-extra-spacing-text": "error",
                        "@html-eslint/no-multiple-empty-lines": "error",
                        "@html-eslint/no-trailing-spaces": "error",
                    },
                }

                config_path = tmp_path.parent / "eslint.config.js"
                config_content = f"module.exports = {json.dumps(config, indent=2)};"
                config_path.write_text(config_content)
                cmd = ["npx", "eslint", "--fix", "--config", str(config_path), str(tmp_path)]

            # Run ESLint with --fix
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, check=False)

            # Read the potentially fixed content
            fixed_content = tmp_path.read_text(encoding="utf-8")

            # Compare without stripping to catch formatting changes
            if fixed_content != html_content:
                changes.append("HTML auto-fixed with html-eslint")

            # Report any remaining issues
            if result.stderr:
                remaining_issues = [line for line in result.stderr.split("\n") if line.strip()]
                if remaining_issues:
                    self.console.print("[yellow]⚠️  Remaining HTML issues after auto-fix:[/yellow]")
                    for issue in remaining_issues[:5]:  # Limit to first 5 issues
                        self.console.print(f"[yellow]  • {issue}[/yellow]")

            return fixed_content, changes

        except Exception as e:
            self.console.print(f"[yellow]⚠️  html-eslint processing error: {e}[/yellow]")
            return html_content, changes
        finally:
            # Clean up temp files
            for path_var in ["tmp_path", "config_path"]:
                if path_var in locals():
                    with contextlib.suppress(Exception):
                        locals()[path_var].unlink()

    def _validate_weasyprint_compatibility(self, html_content: str) -> list[str]:
        """Validate HTML for WeasyPrint-specific compatibility issues"""
        issues = []

        # Check for unsupported CSS properties in style attributes
        unsupported_properties = ["transform-origin", "animation", "transition", "box-shadow", "text-shadow", "filter"]

        for prop in unsupported_properties:
            if f"{prop}:" in html_content:
                issues.append(f"Unsupported CSS property detected: {prop}")

        # Check for JavaScript (WeasyPrint doesn't support it)
        if "<script" in html_content.lower():
            issues.append("JavaScript detected - not supported in PDF generation")

        # Check for external resources that might not load
        if "http://" in html_content or "https://" in html_content:
            if "background-image: url(" not in html_content:  # Allow data URIs
                issues.append("External resources detected - may not load in PDF")

        return issues

    def get_processing_capabilities(self) -> dict[str, Any]:
        """Get information about available processing capabilities"""
        return {
            "node_js": self.node_available,
            "html_eslint": self.html_eslint_available,
            "prettier": self.prettier_available,
            "weasyprint_validation": True,
            "fail_fast_mode": True,
        }

    def install_instructions(self) -> str:
        """Get installation instructions for required dependencies"""
        instructions = []

        if not self.node_available:
            instructions.append("Install Node.js: https://nodejs.org/")

        if not self.prettier_available:
            instructions.append("Install Prettier: npm install -g prettier")

        if not self.html_eslint_available:
            instructions.append("Install ESLint + html-eslint: npm install -g eslint @html-eslint/eslint-plugin")

        if not instructions:
            return "All required dependencies are available!"

        return "Required dependencies for HTML processing:\n" + "\n".join(f"• {inst}" for inst in instructions)
