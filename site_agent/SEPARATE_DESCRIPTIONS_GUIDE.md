# Separate Descriptions System

## Overview

This system allows you to **permanently separate** page descriptions from page content extraction. Descriptions are stored in `descriptions.json` and can be manually edited, while page content is extracted separately.

## How It Works

1. **Descriptions**: Stored in `descriptions.json` (manually editable)
2. **Page Content**: Extracted from actual pages (auto-updates)
3. **pages.html**: Uses descriptions from JSON, content from pages

## Setup

### Step 1: Export Current Descriptions

First, export your current descriptions to a JSON file:

```bash
python3 site_agent/preserve_descriptions.py backup
```

This creates `descriptions_backup.json`. Rename it:

```bash
mv site_agent/descriptions_backup.json site_agent/descriptions.json
```

Or manually create `descriptions.json` with this structure:

```json
{
  "in/about_piandt/in_about_piandt.html": "Your description here...",
  "processing/about_piandt/proc_about_piandt.html": "Another description...",
  ...
}
```

### Step 2: Generate pages.html with Separate Descriptions

```bash
python3 site_agent/use_separate_descriptions.py
```

This generates `pages.html` using:
- **Page Description**: From `descriptions.json`
- **Page Content**: Extracted from actual pages

## Workflow

### Update Page Content

1. Edit your HTML pages freely
2. Run: `python3 site_agent/use_separate_descriptions.py`
3. Descriptions stay the same, content updates

### Update Descriptions

1. Edit `descriptions.json` manually
2. Run: `python3 site_agent/use_separate_descriptions.py`
3. Descriptions update, content stays extracted

## Benefits

✅ **Descriptions never change** unless you edit them  
✅ **Content auto-updates** from pages  
✅ **Full control** over descriptions  
✅ **No backup needed** - descriptions are the source of truth  

## Example descriptions.json

```json
{
  "in/about_piandt/in_about_piandt.html": "Operating within the In stage of the PIANDT triadic information system, the About PIANDT incoming signals section serves as the specialized reception interface...",
  "processing/about_piandt/proc_about_piandt.html": "Serving as the specialized analytical engine, the About PIANDT processing component evaluates, synthesizes, and refines...",
  "out/about_piandt/out_about_piandt.html": "Operating within the Out stage of the PIANDT triadic information system, the About PIANDT delivered outputs section serves as the specialized delivery mechanism..."
}
```

## Comparison

| Method | Descriptions | Content | Use Case |
|--------|-------------|---------|----------|
| **Extract** (default) | Auto from pages | Auto from pages | Descriptions should match content |
| **Backup/Restore** | Preserved | Auto from pages | One-time preservation |
| **Separate** (this) | Manual JSON | Auto from pages | Permanent separation |

## Recommendation

- **Use Separate System** if you want descriptions to be independent summaries
- **Use Extract System** if descriptions should always match content
- **Use Backup/Restore** for temporary preservation

Choose the system that fits your workflow!

