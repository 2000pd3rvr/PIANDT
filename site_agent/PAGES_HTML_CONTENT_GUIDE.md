# Interactive Pages.html Content Updater Guide

## Overview

This system allows you to fill the **Page Content** column in `pages.html` interactively, page by page. The content you provide will later be used to update the actual HTML pages.

## Workflow

### Step 1: Fill pages.html Page Content Column

Run the interactive script:
```bash
python3 site_agent/interactive_pages_html_updater.py
```

This will:
1. Show each page from `pages.html` one by one
2. Display the current URL, heading, and description
3. Ask you to provide Page Content
4. Update `pages.html` immediately after each page
5. Ask for confirmation before moving to next page

### Step 2: Update Actual HTML Pages

After filling all Page Content in `pages.html`, update the actual HTML pages:
```bash
python3 site_agent/update_html_pages_from_pages_html.py
```

This reads `pages.html` and updates all HTML pages with the content from the Page Content column.

## How It Works

### Interactive Script Flow

```
PAGE 1 of 52
======================================================================

📄 URL: in/about_piandt/in_about_piandt.html
📋 Heading: about PIANDT

📝 Current Description (from descriptions.json):
   [Shows description preview]

📦 Current Page Content:
   (empty)

----------------------------------------------------------------------
Enter new Page Content for this page:
  (Type your content - press Enter for new paragraph, blank line to finish)
  (Type 'skip' to skip, 'quit' to exit, 'prev' to go back)
----------------------------------------------------------------------

[You type your content]
Paragraph 1 here.

Paragraph 2 here.

[Press Enter on blank line]

📝 New Page Content preview (first 200 chars):
   Paragraph 1 here. Paragraph 2 here...
   
⚠️  This will update Page Content for: in/about_piandt/in_about_piandt.html
   Continue? (y/n): y

  ✅ Updated Page Content for in/about_piandt/in_about_piandt.html
  ✅ Saved to pages.html

======================================================================
✅ PAGE 1 COMPLETED
======================================================================

Next page: in/about_piandt/in_about_piandt_charitable_purposes.html
Next heading: charitable purposes

Options:
  - Press Enter to continue to next page
  - Type 'quit' to exit and save progress
  - Type 'prev' to go back and redo this page

Continue to next page? (Enter/quit/prev): [You decide]
```

## Commands

- **Type content** → Provide Page Content (multiple paragraphs separated by blank lines)
- **Blank line** → Finish input for current page
- **`skip`** → Skip current page
- **`quit`** → Exit and save progress
- **`prev`** → Go back to previous page
- **`y`** → Confirm update
- **`n`** → Cancel and skip

## Important Notes

1. **Auto-save**: Each update is saved immediately to `pages.html`
2. **Safe exit**: You can quit anytime; all changes are saved
3. **Progress tracking**: Shows completed/remaining pages
4. **Redo option**: Use `prev` to go back and redo a page

## After Completing All Pages

Once you've filled Page Content for all pages in `pages.html`, run:

```bash
python3 site_agent/update_html_pages_from_pages_html.py
```

This will:
- Read Page Content from `pages.html`
- Update all HTML pages with that content
- Replace paragraph content in `<div class="content-text">` sections

## Summary

```
Fill pages.html → Update HTML pages → Done!
```

The system ensures that `pages.html` is the single source of truth for Page Content.

