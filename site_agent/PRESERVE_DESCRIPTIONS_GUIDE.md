# Preserve Descriptions While Updating Page Content

## The Problem

You want to update page content, but you're worried about losing the current descriptions in `pages.html` because they're extracted from the pages.

## The Solution

**Backup your descriptions first, then update pages, then restore descriptions.**

## Workflow

### Step 1: Backup Current Descriptions

Before making any changes, backup the current descriptions:

```bash
python3 site_agent/preserve_descriptions.py backup
```

This creates `descriptions_backup.json` with all current descriptions.

### Step 2: Update Your Pages

Now you can safely update page content:

- Edit HTML files
- Add new content
- Modify paragraphs
- Change structure

**The descriptions are safely backed up!**

### Step 3: Restore Descriptions

After updating pages, restore the preserved descriptions:

```bash
python3 site_agent/preserve_descriptions.py restore
```

This regenerates `pages.html` but uses the **backed-up descriptions** instead of extracting new ones from the updated pages.

## Complete Example

```bash
# 1. Backup current descriptions
python3 site_agent/preserve_descriptions.py backup

# 2. Update your pages (edit HTML files)
# ... make your changes ...

# 3. Restore descriptions (preserves old descriptions)
python3 site_agent/preserve_descriptions.py restore

# 4. Now pages.html has:
#    - Updated page content (from your edits)
#    - Preserved descriptions (from backup)
```

## How It Works

1. **Backup**: Extracts descriptions from current `pages.html` and saves to JSON
2. **Update Pages**: You edit pages freely
3. **Restore**: Regenerates `pages.html` but uses backed-up descriptions instead of extracting new ones

## Important Notes

### ✅ What Gets Preserved

- **Page Descriptions**: The full text in the "Page Description" column
- **Headings**: Still extracted from pages (can be updated)
- **Metadata**: Still extracted from pages (can be updated)
- **FAQs**: Regenerated from preserved descriptions

### ⚠️ What Gets Updated

- **Page Content**: New content from your edits (goes to "Page Content" column if you populate it)
- **Headings**: Extracted fresh from pages
- **Metadata**: Extracted fresh from pages

### 🔄 When to Use

Use this workflow when:
- You want to update page content but keep current descriptions
- Descriptions are carefully crafted and shouldn't change
- You're doing major content restructuring

### ❌ When NOT to Use

Don't use this if:
- You want descriptions to reflect new content
- You're making minor updates
- You want descriptions to auto-update

## Alternative: Separate Description Storage

If you want to permanently separate descriptions from content extraction, you could:

1. Store descriptions in a separate JSON file
2. Manually edit descriptions
3. Use descriptions as a separate "summary" field

Would you like me to create a system for that?

## Troubleshooting

**Q: What if I update a page that wasn't in the backup?**
- The restore function will extract a new description for that page
- You'll see a warning message

**Q: Can I edit the backup file?**
- Yes! Edit `descriptions_backup.json` to manually adjust descriptions
- Then run `restore` to apply changes

**Q: What if I want to update some descriptions but not others?**
- Edit `descriptions_backup.json` before restoring
- Or restore, then manually edit `pages.html`

## Summary

```
Backup → Update Pages → Restore = Preserved Descriptions + Updated Content
```

This gives you full control over descriptions while allowing content updates!

