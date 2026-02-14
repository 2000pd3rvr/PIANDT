#!/usr/bin/env python3
"""
Archive redundant files to xives directory
"""
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
ARCHIVE_DIR = BASE_DIR / "xives"
SITE_AGENT_ARCHIVE = ARCHIVE_DIR / "site_agent"
PATENTS_ARCHIVE = ARCHIVE_DIR / "patents"

# Files to archive
redundant_files = {
    "multisheet": [
        "site_agent/apply_multisheet_all_directories.py",
        "site_agent/apply_multisheet_interactive.py",
        "site_agent/apply_multisheet_one_by_one.py",
        "site_agent/apply_multisheet_to_all.py",
        "site_agent/apply_multisheet_to_all_pages.py",
    ],
    "navigation": [
        "site_agent/apply_nav_menu_logic.py",
        "site_agent/apply_nav_menu_logic_fixed.py",
        "site_agent/apply_nav_menu_logic_safe.py",
        "site_agent/fix_all_menu_links.py",
        "site_agent/fix_all_menu_relative_paths.py",
        "site_agent/fix_all_navigation_comprehensive.py",
        "site_agent/fix_menu_paths_comprehensive.py",
        "site_agent/fix_navigation_paths.py",
        "site_agent/update_all_menu_links.py",
        "site_agent/update_all_navigation_menus.py",
        "site_agent/verify_and_fix_all_menu_links.py",
        "site_agent/verify_and_fix_navigation.py",
    ],
    "links": [
        "site_agent/check_links.py",
        "site_agent/fix_all_broken_links.py",
        "site_agent/fix_all_links.py",
        "site_agent/fix_all_old_links.py",
        "site_agent/fix_broken_links_comprehensive.py",
        "site_agent/fix_favicon_and_verify_links.py",
        "site_agent/fix_links.py",
        "site_agent/update_triad_links.py",
        "site_agent/verify_and_fix_all_links.py",
    ],
    "descriptions": [
        "site_agent/add_descriptions_to_all_pages.py",
        "site_agent/check_and_update_descriptions.py",
        "site_agent/check_descriptions.py",
        "site_agent/fix_duplicate_descriptions.py",
        "site_agent/sync_descriptions.py",
        "site_agent/update_descriptions.py",
        "site_agent/update_pages_with_triad_descriptions.py",
        "site_agent/vary_page_descriptions.py",
    ],
    "pages_html": [
        "site_agent/extract_content.py",
        "site_agent/update_pages_html_comprehensive.py",
    ],
    "content_variation": [
        "site_agent/fix_all_content_openings.py",
        "site_agent/vary_page_content.py",
    ],
    "latex_aux": [
        "patents/background_literature_related_patents.aux",
        "patents/background_literature_related_patents.log",
        "patents/background_literature_related_patents.out",
        "patents/triad_information_architecture_patent.aux",
        "patents/triad_information_architecture_patent.log",
        "patents/triad_information_architecture_patent.out",
    ],
}

def archive_files():
    """Archive all redundant files"""
    print("=" * 70)
    print("ARCHIVING REDUNDANT FILES TO xives/")
    print("=" * 70)
    
    # Create archive directories
    SITE_AGENT_ARCHIVE.mkdir(parents=True, exist_ok=True)
    PATENTS_ARCHIVE.mkdir(parents=True, exist_ok=True)
    
    total_archived = 0
    total_size = 0
    
    for category, files in redundant_files.items():
        print(f"\n📦 Archiving {category} files:")
        print("-" * 70)
        
        for file_path_str in files:
            file_path = BASE_DIR / file_path_str
            
            if file_path.exists():
                try:
                    # Determine destination
                    if file_path_str.startswith("site_agent/"):
                        dest = SITE_AGENT_ARCHIVE / file_path.name
                    elif file_path_str.startswith("patents/"):
                        dest = PATENTS_ARCHIVE / file_path.name
                    else:
                        dest = ARCHIVE_DIR / file_path.name
                    
                    # Move file
                    shutil.move(str(file_path), str(dest))
                    size = dest.stat().st_size
                    total_size += size
                    total_archived += 1
                    print(f"  ✓ Archived: {file_path_str} ({size:,} bytes)")
                except Exception as e:
                    print(f"  ✗ Error archiving {file_path_str}: {e}")
            else:
                print(f"  - Not found: {file_path_str}")
    
    print("\n" + "=" * 70)
    print(f"✅ ARCHIVING COMPLETE!")
    print(f"   Total files archived: {total_archived}")
    print(f"   Total size: {total_size:,} bytes ({total_size / 1024:.1f} KB)")
    print(f"   Archive location: {ARCHIVE_DIR}")
    print("=" * 70)

if __name__ == '__main__':
    archive_files()

