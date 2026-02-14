# PIANDT Site Agent - Pages Table

This directory contains a comprehensive table of all pages in the PIANDT website.

## Files

- **pages.html** - HTML version of the pages table (ready for browser viewing)
- **pages.pdf** - PDF version (to be generated - see instructions below)
- **extract_content.py** - Python script that extracts content from all HTML pages
- **generate_pdf.py** - Python script to generate PDF (requires reportlab library)
- **create_pdf.sh** - Shell script with PDF generation instructions

## Table Structure

The table contains 3 columns:
1. **Page URL** - The relative path/URL of each page
2. **Page Description** - The current body text/content extracted from each page
3. **Page Content** - (Blank column for future use)

## Generating PDF

### Option 1: Using Browser (Recommended)
1. Open `pages.html` in your web browser
2. Press `Cmd+P` (Mac) or `Ctrl+P` (Windows/Linux)
3. Select "Save as PDF" as the destination
4. Choose landscape orientation for better table display
5. Save as `pages.pdf`

### Option 2: Using Python (if reportlab is installed)
```bash
pip3 install reportlab
python3 generate_pdf.py
```

### Option 3: Using Command Line Tools
If you have `wkhtmltopdf` installed:
```bash
wkhtmltopdf --page-size A4 --orientation Landscape pages.html pages.pdf
```

Or with `weasyprint`:
```bash
weasyprint pages.html pages.pdf
```

## Regenerating the Table

To regenerate the table with updated content:
```bash
python3 extract_content.py
```

This will update `pages.html` with the latest content from all pages.

## Notes

- The table includes all 49 HTML pages from the website
- Page descriptions are truncated to 1000 characters for display
- The HTML file is optimized for both screen viewing and PDF printing
- Column 3 (Page Content) is left blank as requested for future use



