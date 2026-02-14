# Quick Reference: Updating Pages & Keeping Descriptions in Sync

## The Key Point

**`pages.html` descriptions are ALWAYS extracted from the actual web pages.** You never lose descriptions because they're regenerated from the source files.

## Simple Workflow

### 1. Update Your Page
Edit any HTML page (e.g., `in/about_piandt/in_about_piandt.html`)

### 2. Regenerate pages.html
```bash
python3 site_agent/update_pages_html.py
```

That's it! Descriptions automatically update.

## Three Ways to Regenerate

### Option 1: Single Page (Interactive)
```bash
python3 site_agent/update_page_and_sync.py <page-path>
```
Example:
```bash
python3 site_agent/update_page_and_sync.py in/about_piandt/in_about_piandt.html
```

### Option 2: All Pages (Recommended)
```bash
python3 site_agent/update_pages_html.py
```
Regenerates descriptions for ALL pages.

### Option 3: Check Before Regenerating
```bash
# Preview what will be extracted
python3 site_agent/check_page_extraction.py <page-path>

# Then regenerate
python3 site_agent/update_pages_html.py
```

## What Gets Extracted

The "Page Description" column in `pages.html` contains:
- ✅ All paragraph text from `<div class="content-text">`
- ✅ Text from `<main>`, `<article>`, `<section>` tags
- ✅ Automatically excludes scripts, styles, navigation

## Important Notes

- ⚠️ **Always regenerate after updating page content**
- ✅ Descriptions are never manually edited - always extracted
- ✅ You can't "lose" descriptions - they're regenerated from pages
- ✅ Update pages freely, then regenerate `pages.html`

## Example Workflow

```bash
# 1. Edit a page
vim in/about_piandt/in_about_piandt.html

# 2. Save your changes

# 3. Regenerate pages.html
python3 site_agent/update_pages_html.py

# 4. Check the result
open site_agent/pages.html
```

## Troubleshooting

**Q: My changes aren't showing in pages.html**
- Make sure you saved the file
- Run `update_pages_html.py` again
- Check if content is in `<div class="content-text">` sections

**Q: Can I edit descriptions directly?**
- No need! Descriptions are auto-extracted
- Just update the page content and regenerate

**Q: What if I update multiple pages?**
- Update all pages first
- Then run `update_pages_html.py` once
- It processes all pages automatically

## Summary

```
Update Page → Save → Regenerate pages.html → Done!
```

The system is designed so descriptions are **always in sync** with page content because they're extracted fresh each time.

