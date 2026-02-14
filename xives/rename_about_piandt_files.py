#!/usr/bin/env python3
"""
Rename about_piandt child menu files to reflect hierarchy in their names.
e.g., in_mission_vision.html -> in_about_piandt_mission_vision.html
"""

import os
import shutil
from pathlib import Path
import re

BASE_DIR = Path(__file__).parent.parent

# Define the renaming mappings for each triad
RENAME_MAPPINGS = {
    'in': {
        'in_mission_vision.html': 'in_about_piandt_mission_vision.html',
        'in_charitable_purposes.html': 'in_about_piandt_charitable_purposes.html',
        'in_our_approach.html': 'in_about_piandt_our_approach.html',
        'in_trustees.html': 'in_about_piandt_trustees.html',
        'in_governance.html': 'in_about_piandt_governance.html',
    },
    'processing': {
        'proc_mission_vision.html': 'proc_about_piandt_mission_vision.html',
        'proc_charitable_purposes.html': 'proc_about_piandt_charitable_purposes.html',
        'proc_our_approach.html': 'proc_about_piandt_our_approach.html',
        'proc_trustees.html': 'proc_about_piandt_trustees.html',
        'proc_governance.html': 'proc_about_piandt_governance.html',
    },
    'out': {
        'out_mission_vision.html': 'out_about_piandt_mission_vision.html',
        'out_charitable_purposes.html': 'out_about_piandt_charitable_purposes.html',
        'out_our_approach.html': 'out_about_piandt_our_approach.html',
        'out_trustees.html': 'out_about_piandt_trustees.html',
        'out_governance.html': 'out_about_piandt_governance.html',
    }
}

def find_and_rename_files(triad_name, rename_mapping):
    """Find and rename files in the about_piandt directory"""
    triad_dir = BASE_DIR / triad_name
    about_dir = triad_dir / 'about_piandt'
    
    renamed_files = []
    
    if not about_dir.exists():
        print(f"  ⚠️  Directory {about_dir.relative_to(BASE_DIR)} does not exist")
        return renamed_files
    
    # Rename each file
    for old_name, new_name in rename_mapping.items():
        old_path = about_dir / old_name
        new_path = about_dir / new_name
        
        if old_path.exists():
            print(f"  Renaming {old_path.relative_to(BASE_DIR)} -> {new_path.relative_to(BASE_DIR)}")
            shutil.move(str(old_path), str(new_path))
            renamed_files.append((old_name, new_name, old_path, new_path))
        else:
            print(f"  ⚠️  File {old_name} not found in {about_dir.relative_to(BASE_DIR)}")
    
    return renamed_files

def update_links_in_html(file_path, old_name, new_name):
    """Update all references to old filename in HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Pattern 1: href="about_piandt/old_name" or href="../about_piandt/old_name" etc.
        # This handles links from other directories
        content = re.sub(
            rf'href=["\']([^"\']*about_piandt/){re.escape(old_name)}["\']',
            rf'href="\1{new_name}"',
            content
        )
        
        # Pattern 2: href="old_name" - simple relative link (most common case)
        # This handles links from within about_piandt directory
        content = re.sub(
            rf'href=["\']{re.escape(old_name)}["\']',
            rf'href="{new_name}"',
            content
        )
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"    ⚠️  Error updating {file_path}: {e}")
        import traceback
        traceback.print_exc()
        return False

def update_all_html_files(triad_name, renamed_files):
    """Update all HTML files in the triad to reference new filenames"""
    triad_dir = BASE_DIR / triad_name
    
    print(f"\n  Updating links in all HTML files...")
    updated_count = 0
    
    # Find all HTML files in the triad and also check root level files
    search_dirs = [triad_dir]
    # Also check root level for main pages that might link to these
    search_dirs.append(BASE_DIR)
    
    for search_dir in search_dirs:
        if search_dir.exists():
            for html_file in search_dir.rglob('*.html'):
                updated = False
                for old_name, new_name, old_path, new_path in renamed_files:
                    if update_links_in_html(html_file, old_name, new_name):
                        updated = True
                
                if updated:
                    updated_count += 1
    
    print(f"  ✓ Updated {updated_count} HTML files")

def main():
    """Main function to rename files and update links"""
    print("="*60)
    print("RENAMING ABOUT_PIANDT CHILD FILES TO REFLECT HIERARCHY")
    print("="*60)
    print("\nThis will:")
    print("1. Rename child menu files to include 'about_piandt' in filename")
    print("2. Update all links in HTML files to reference new names")
    print("3. Preserve all content, theme, and functionality")
    print("\n" + "="*60)
    
    for triad_name, rename_mapping in RENAME_MAPPINGS.items():
        print(f"\n{'='*60}")
        print(f"Processing {triad_name.upper()} triad")
        print(f"{'='*60}")
        
        # Rename files
        print(f"\n📝 Renaming files...")
        renamed_files = find_and_rename_files(triad_name, rename_mapping)
        
        if renamed_files:
            print(f"  ✓ Renamed {len(renamed_files)} files")
            
            # Update all HTML files
            update_all_html_files(triad_name, renamed_files)
        else:
            print(f"  ⚠️  No files found to rename")
    
    print("\n" + "="*60)
    print("✅ ALL RENAMING COMPLETE!")
    print("="*60)
    print("\nPlease test the pages to ensure:")
    print("- All links work correctly")
    print("- Files are accessible with new names")
    print("- Navigation menus work")

if __name__ == '__main__':
    main()

