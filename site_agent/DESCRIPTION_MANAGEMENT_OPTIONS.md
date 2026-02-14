# Description Management Options

## Your Concern

You want to update page content but are worried about losing current descriptions in `pages.html` because descriptions are extracted from pages.

## Three Solutions

### Option 1: Backup & Restore (Temporary)

**Best for**: One-time updates, preserving descriptions temporarily

**Workflow**:
```bash
# 1. Backup current descriptions
python3 site_agent/preserve_descriptions.py backup

# 2. Update your pages (edit HTML files)

# 3. Restore descriptions
python3 site_agent/preserve_descriptions.py restore
```

**Result**: 
- ✅ Descriptions preserved from backup
- ✅ Page content updated from your edits
- ⚠️ Descriptions won't reflect new content

**Files**: `descriptions_backup.json`

---

### Option 2: Separate Descriptions (Permanent)

**Best for**: Permanent separation, manual description control

**Workflow**:
```bash
# 1. Export current descriptions to JSON
python3 site_agent/preserve_descriptions.py backup
mv site_agent/descriptions_backup.json site_agent/descriptions.json

# 2. Update pages freely
# (Edit HTML files)

# 3. Generate pages.html with separate descriptions
python3 site_agent/use_separate_descriptions.py
```

**Result**:
- ✅ Descriptions from `descriptions.json` (manually editable)
- ✅ Page content extracted from pages (auto-updates)
- ✅ Descriptions never change unless you edit JSON

**Files**: `descriptions.json`

---

### Option 3: Extract Everything (Default)

**Best for**: Descriptions should always match content

**Workflow**:
```bash
# 1. Update pages (edit HTML files)

# 2. Regenerate pages.html
python3 site_agent/update_pages_html.py
```

**Result**:
- ✅ Descriptions extracted from pages (auto-updates)
- ✅ Page content extracted from pages (auto-updates)
- ⚠️ Descriptions change when content changes

**Files**: None (extracts directly)

---

## Comparison Table

| Feature | Backup/Restore | Separate | Extract (Default) |
|---------|---------------|----------|-------------------|
| **Descriptions Source** | Backup file | JSON file | Pages |
| **Content Source** | Pages | Pages | Pages |
| **Description Control** | One-time preserve | Full control | Auto-updates |
| **When Descriptions Change** | Never (from backup) | Only if you edit JSON | When pages change |
| **Best For** | Temporary preservation | Permanent separation | Always in sync |

## Recommendation

### Use **Backup/Restore** if:
- You're doing a one-time major update
- You want to preserve current descriptions temporarily
- You'll eventually want descriptions to match new content

### Use **Separate** if:
- You want descriptions to be independent summaries
- You want full manual control over descriptions
- Descriptions should never auto-update

### Use **Extract** (default) if:
- You want descriptions to always reflect page content
- You're okay with descriptions changing when content changes
- You want the simplest workflow

## Quick Decision Guide

**Q: Do you want descriptions to stay the same when you update content?**
- **Yes** → Use **Separate** or **Backup/Restore**
- **No** → Use **Extract** (default)

**Q: Do you want permanent control over descriptions?**
- **Yes** → Use **Separate**
- **No** → Use **Backup/Restore** or **Extract**

**Q: Should descriptions be summaries or full content?**
- **Summaries** → Use **Separate**
- **Full content** → Use **Extract**

## Example Workflows

### Scenario 1: Major Content Update, Keep Descriptions

```bash
# Backup first
python3 site_agent/preserve_descriptions.py backup

# Update pages
# ... edit HTML files ...

# Restore descriptions
python3 site_agent/preserve_descriptions.py restore
```

### Scenario 2: Permanent Separation

```bash
# One-time setup
python3 site_agent/preserve_descriptions.py backup
mv site_agent/descriptions_backup.json site_agent/descriptions.json

# Then always use:
python3 site_agent/use_separate_descriptions.py
```

### Scenario 3: Keep Everything in Sync

```bash
# Just update and regenerate
python3 site_agent/update_pages_html.py
```

## Summary

You have **three options** to handle descriptions:

1. **Backup/Restore**: Temporary preservation
2. **Separate**: Permanent manual control
3. **Extract**: Always in sync (default)

Choose based on your needs! All options preserve your ability to update page content.

