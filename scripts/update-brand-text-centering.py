#!/usr/bin/env python3
"""
Brand Text Centering and Sizing Update Script
Horizontally centers SVG brand text and increases size by 100% (2x) across all CSS templates.
Clean, maintainable implementation following software engineering best practices.
"""

from pathlib import Path
import re

# CSS template files to update
TEMPLATE_FILES = ["applyr/styles/ats.css"]

# CSS property updates - single source of truth
CSS_UPDATES = {
    "background-position": {"old": "left center", "new": "center center"},
    "width": {
        "old": "140pt",
        "new": "280pt",  # 100% increase (2x)
    },
    "height": {
        "old": "20pt",
        "new": "40pt",  # 100% increase (2x), maintains 7:1 aspect ratio
    },
}


def update_css_property(content: str, property_name: str, old_value: str, new_value: str) -> tuple[str, bool]:
    """
    Update a specific CSS property value within .brand-text selector.

    Args:
        content: CSS file content
        property_name: CSS property to update (e.g., 'background-position')
        old_value: Current property value to replace
        new_value: New property value

    Returns:
        Tuple of (updated_content, was_changed)
    """
    # Pattern to match property within .brand-text selector
    pattern = rf"(\.brand-text\s*\{{[^}}]*?)({property_name}\s*:\s*){re.escape(old_value)}(\s*[!;][^}}]*?\}})"

    def replacement(match):
        return f"{match.group(1)}{match.group(2)}{new_value}{match.group(3)}"

    updated_content, count = re.subn(pattern, replacement, content, flags=re.DOTALL | re.IGNORECASE)

    return updated_content, count > 0


def update_brand_text_css(css_file: Path) -> dict[str, bool]:
    """
    Update .brand-text CSS properties in a template file.

    Args:
        css_file: Path to CSS template file

    Returns:
        Dictionary of property_name -> was_updated status
    """
    try:
        content = css_file.read_text(encoding="utf-8")
        original_content = content
        results = {}

        # Apply each CSS property update
        for property_name, values in CSS_UPDATES.items():
            content, was_updated = update_css_property(content, property_name, values["old"], values["new"])
            results[property_name] = was_updated

        # Only write if content changed
        if content != original_content:
            css_file.write_text(content, encoding="utf-8")
            print(f"✅ Updated: {css_file.name}")
            for prop, updated in results.items():
                status = "✓" if updated else "⚠"
                print(f'   {status} {prop}: {CSS_UPDATES[prop]["old"]} → {CSS_UPDATES[prop]["new"]}')
        else:
            print(f"ℹ️  No changes needed: {css_file.name}")

        return results

    except Exception as e:
        print(f"❌ Error updating {css_file.name}: {e}")
        return {prop: False for prop in CSS_UPDATES}


def validate_updates() -> None:
    """Validate that all templates have consistent .brand-text properties."""
    print("\n🔍 Validating consistency across templates...")

    expected_properties = {"background-position": "center center", "width": "280pt", "height": "40pt"}

    for template_path in TEMPLATE_FILES:
        css_file = Path(template_path)
        if not css_file.exists():
            print(f"⚠️  File not found: {template_path}")
            continue

        content = css_file.read_text()

        # Check for .brand-text selector
        if ".brand-text" not in content:
            print(f"⚠️  No .brand-text selector found in {css_file.name}")
            continue

        # Validate each expected property
        inconsistencies = []
        for prop, expected_value in expected_properties.items():
            pattern = rf"{prop}\s*:\s*{re.escape(expected_value)}"
            if not re.search(pattern, content):
                inconsistencies.append(f"{prop} ≠ {expected_value}")

        if inconsistencies:
            print(f'⚠️  {css_file.name}: {", ".join(inconsistencies)}')
        else:
            print(f"✅ {css_file.name}: All properties consistent")


def main():
    """Main execution function."""
    print("🎯 SVG Brand Text Centering & Sizing Update")
    print("=" * 50)
    print("📋 Changes:")
    for prop, values in CSS_UPDATES.items():
        print(f'   • {prop}: {values["old"]} → {values["new"]}')
    print("📂 Templates:", len(TEMPLATE_FILES))
    print("=" * 50)

    success_count = 0
    total_count = len(TEMPLATE_FILES)

    # Update each template file
    for template_path in TEMPLATE_FILES:
        css_file = Path(template_path)

        if not css_file.exists():
            print(f"❌ File not found: {template_path}")
            continue

        results = update_brand_text_css(css_file)

        # Check if all updates were successful
        if all(results.values()):
            success_count += 1

    print("=" * 50)
    print(f"📊 Summary: {success_count}/{total_count} templates updated successfully")

    # Validate consistency
    validate_updates()

    print("\n🎉 Brand text centering and sizing update complete!")
    print("📐 New dimensions: 280pt × 40pt (2x increase)")
    print("🎯 Positioning: Horizontally centered")
    print("📏 Aspect ratio: 7:1 maintained")


if __name__ == "__main__":
    main()
