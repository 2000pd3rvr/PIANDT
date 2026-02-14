# Page Update Workflow Guide

## Overview

This guide explains how to update page content while keeping `pages.html` descriptions synchronized. Since `pages.html` extracts descriptions directly from the actual web pages, you need to regenerate it after making changes.

## How It Works

1. **You update a page**: Edit the HTML file (e.g., `in/about_piandt/in_about_piandt.html`)
2. **Extract descriptions**: The `update_pages_html.py` script reads all pages and extracts:
   - All paragraph text from `<div class="content-text">` sections
   - Text from `<main>`, `<article>`, and `<section>` tags
   - Meta descriptions, headings, and metadata
3. **Regenerate pages.html**: The extracted content becomes the "Page Description" in `pages.html`

## Workflow Options

### Option 1: Update Single Page (Recommended)

After editing a page, run:

```bash
python3 site_agent/update_page_and_sync.py <page_path>
```

**Example:**
```bash
# 1. Edit the page
# (Make your changes to in/about_piandt/in_about_piandt.html)

# 2. Regenerate pages.html
python3 site_agent/update_page_and_sync.py in/about_piandt/in_about_piandt.html
```

### Option 2: Update All Pages

After making changes to multiple pages:

```bash
python3 site_agent/update_pages_html.py
```

This regenerates `pages.html` with descriptions from **all** pages.

### Option 3: Manual Regeneration

Simply run the update script directly:

```bash
cd /Users/pd3rvr/Documents/pubs/THESIS/thetex/PIANDT
python3 site_agent/update_pages_html.py
```

## Step-by-Step Process

### 1. Edit Your Page

Edit the HTML file directly. For example, update content in:
- `<div class="content-text">` sections
- Paragraphs (`<p>` tags)
- Any text content

**Example:**
```html
<div class="content-text">
    <p>Your updated paragraph content here...</p>
    <p>More updated content...</p>
</div>
```

### 2. Save Your Changes

Make sure to save the file before regenerating `pages.html`.

### 3. Regenerate pages.html

Run the sync script:
```bash
python3 site_agent/update_page_and_sync.py <your-page-path>
```

Or regenerate all:
```bash
python3 site_agent/update_pages_html.py
```

### 4. Verify

Check `site_agent/pages.html` to confirm:
- The "Page Description" column reflects your changes
- The "FAQ" column is updated (generated from new descriptions)
- All other pages are still correct

## What Gets Extracted

The extraction process (`extract_all_page_content()`) captures:

1. **All paragraphs** from `<div class="content-text">` sections
2. **Text from main content areas**: `<main>`, `<article>`, `<section>`
3. **Excludes**: Scripts, styles, navigation, headers, footers
4. **Minimum length**: Only paragraphs longer than 10 characters

## Important Notes

### ✅ Safe to Update

- **Page content** (paragraphs, text)
- **Meta descriptions** (will be extracted)
- **Headings** (H1 tags)
- **Page structure** (columns, sheets)

### ⚠️ What Affects Descriptions

- Adding/removing paragraphs → Description updates
- Changing paragraph text → Description updates
- Adding new content sections → Description updates
- Removing content → Description updates

### 🔄 Always Regenerate After Changes

**Critical**: If you update page content but don't regenerate `pages.html`, the descriptions will be **out of sync** with the actual pages.

## Automation Options

### Watch Mode (Future Enhancement)

You could set up a file watcher to auto-regenerate:

```bash
# Using watchdog (install: pip install watchdog)
watchmedo shell-command \
    --patterns="*.html" \
    --recursive \
    --command='python3 site_agent/update_pages_html.py' \
    --ignore-directories-pattern='xives|site_agent'
```

### Git Hooks

Add a pre-commit hook to auto-regenerate:

```bash
# .git/hooks/pre-commit
#!/bin/bash
python3 site_agent/update_pages_html.py
git add site_agent/pages.html
```

## Troubleshooting

### Descriptions Not Updating

1. **Check file was saved**: Make sure changes are saved
2. **Verify extraction**: Check if your content is in `<div class="content-text">` or `<main>`/`<article>`/`<section>`
3. **Run script manually**: Try running `update_pages_html.py` directly
4. **Check console output**: Look for errors in the script output

### Content Not Being Extracted

- Ensure paragraphs are in `<div class="content-text">` sections
- Check paragraph length (must be > 10 characters)
- Verify HTML structure is valid
- Check for script/style tags interfering

### FAQ Not Updating

FAQs are generated from descriptions. If descriptions update, FAQs should too. If not:
- Check the `generate_faq_from_description()` function
- Verify description contains relevant keywords
- Manually review FAQ generation logic

## Best Practices

1. **Update → Regenerate**: Always regenerate after content changes
2. **Test locally**: Check `pages.html` after regeneration
3. **Version control**: Commit both page changes and `pages.html` updates together
4. **Batch updates**: If updating multiple pages, regenerate once at the end
5. **Verify extraction**: Check that important content is being captured

## Quick Reference

```bash
# Update single page workflow
1. Edit page
2. Save
3. python3 site_agent/update_page_and_sync.py <page-path>

# Update multiple pages workflow
1. Edit all pages
2. Save all
3. python3 site_agent/update_pages_html.py

# Check what will be extracted
python3 -c "
from site_agent.update_pages_html import extract_all_page_content
with open('your-page.html', 'r') as f:
    print(extract_all_page_content(f.read()))
"
```

## Summary

- ✅ Update page content freely
- ✅ Run `update_pages_html.py` after changes
- ✅ Descriptions auto-update from page content
- ✅ No manual description editing needed
- ⚠️ Always regenerate after content changes

The system is designed so you **never lose** description information because it's always extracted fresh from the actual pages!

