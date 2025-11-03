# Template Setup Guide

This guide will help you personalize applyr for your own use.

## Quick Start

1. **Copy the configuration template:**
   ```bash
   cp config.template.yaml config.yaml
   ```

2. **Edit `config.yaml` with your personal information:**
   ```yaml
   personal_info:
     name: "Your Name"
     email: "your-email@example.com"
     phone: "Your Phone"
     website: "yourwebsite.com"
     github: "yourusername"
     linkedin: "linkedin.com/in/your-profile"
     location: "Your City, State"

   branding:
     svg_text: "{{YOUR_BRAND_TEXT}}"  # SVG data URI for brand text
     footer_text: "yourwebsite.com"  # Text for PDF footers
   ```

3. **The `config.yaml` file is gitignored** - your personal information stays private.

## Environment Variables

You can also configure applyr using environment variables:

```bash
export APPLYR_PERSONAL_INFO_NAME="Your Name"
export APPLYR_PERSONAL_INFO_EMAIL="your-email@example.com"
export APPLYR_PERSONAL_INFO_WEBSITE="yourwebsite.com"
# ... etc
```

Environment variables take precedence over `config.yaml` values, making them useful for CI/CD environments.

## Brand Text (SVG)

The brand text is displayed in PDFs using SVG. To customize:

1. Create an SVG file of your name/brand text
2. Convert it to a data URI format
3. Add it to `config.yaml`:
   ```yaml
   branding:
     svg_text: "data:image/svg+xml,%3Csvg...%3E%3C/svg%3E"
   ```

Or use an online tool to convert SVG to data URI.

## Verification

After setting up your config, test the system:

```bash
# Generate a test resume
applyr pdf your_resume.md

# Check that your information appears correctly
```

## Files to Personalize

- `config.yaml` - Your personal information (gitignored)
- `data/raw/advertisements.csv` - Your job application tracking
- `data/outputs/` - Your job descriptions and cover letters

All other files are part of the template and should work with your configuration.
