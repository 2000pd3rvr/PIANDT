# Interactive Page Content Updater Guide

## Overview

This tool allows you to update page content one by one, interactively. You provide new content for each page, and it replaces all paragraphs in all sheets/columns.

## How to Run

```bash
python3 site_agent/interactive_page_content_updater.py
```

## How It Works

1. **Shows current page**: Displays the current page number, file path, and existing content
2. **Shows current content**: Lists all current paragraphs
3. **You provide new content**: Type your new content (can be multiple paragraphs)
4. **Replaces content**: Updates all paragraphs in the page
5. **Moves to next page**: Automatically proceeds to the next page

## Input Format

### Multiple Paragraphs

Type your content, pressing Enter after each paragraph. To finish, press Enter twice (blank line):

```
First paragraph of new content.

Second paragraph of new content.

Third paragraph of new content.

[Press Enter on blank line to finish]
```

### Single Paragraph

Just type and press Enter twice:

```
Your single paragraph content here.

[Press Enter on blank line to finish]
```

## Commands

- **`skip`** - Skip the current page and move to next
- **`prev`** - Go back to the previous page
- **`quit`** - Exit the script
- **Ctrl+C** - Exit the script

## Example Session

```
======================================================================
PAGE 1 of 52
File: in/about_piandt/in_about_piandt.html
======================================================================

CURRENT PAGE CONTENT:
======================================================================

  Paragraph 1:
  The About PIANDT component represents the initial reception point...

  Paragraph 2:
  the organization proactively sharing mission and vision details...

======================================================================
Page Heading: about PIANDT

----------------------------------------------------------------------
Enter new content for this page:
  (Type your content - press Enter for new paragraph, blank line to finish)
  (Type 'skip' to skip, 'quit' to exit, 'prev' to go back)
----------------------------------------------------------------------

[You type your new content here]
Your new first paragraph.

Your new second paragraph.

[Press Enter on blank line]

📝 New content preview (first 200 chars):
   Your new first paragraph. Your new second paragraph...
   
⚠️  This will replace ALL paragraphs in in_about_piandt.html
   Continue? (y/n): y

  ✅ Updated in_about_piandt.html
  ✅ Replaced 4 old paragraphs with 2 new paragraphs
```

## What Gets Replaced

- ✅ All paragraphs in `<div class="content-text">` sections
- ✅ Content in all sheets (if multi-sheet)
- ✅ Content in all columns (if multi-column)
- ✅ Preserves HTML structure (divs, classes, etc.)
- ✅ Only replaces paragraph text content

## What Gets Preserved

- ✅ HTML structure (divs, classes, attributes)
- ✅ Page metadata (title, meta tags)
- ✅ Navigation menus
- ✅ Scripts and styles
- ✅ Chat agent button
- ✅ All other page elements

## After Updating Pages

After you've updated pages, regenerate `pages.html`:

```bash
python3 site_agent/use_separate_descriptions.py
```

This will:
- Keep your descriptions from `descriptions.json`
- Update page content from your edits
- Regenerate FAQs based on new content

## Tips

1. **Review before confirming**: The script shows a preview before replacing
2. **Use 'prev' to go back**: If you make a mistake, you can go back
3. **Save your work**: The script saves immediately after confirmation
4. **Take breaks**: You can quit and resume later (it will start from page 1)

## Troubleshooting

**Q: I accidentally skipped a page**
- Use 'prev' to go back, or restart and skip to that page

**Q: The content didn't update**
- Check that you confirmed with 'y'
- Verify the file was saved (check modification time)

**Q: I want to edit just one paragraph**
- You still need to provide all paragraphs (the script replaces all)
- You can copy existing paragraphs and modify one

## Summary

```
Run script → Review page → Type new content → Confirm → Next page
```

The script makes it easy to update all pages systematically!

