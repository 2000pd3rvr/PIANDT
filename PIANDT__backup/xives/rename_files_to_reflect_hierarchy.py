#!/usr/bin/env python3
"""
Rename files to reflect clear hierarchy in their names.
e.g., proc_miu.html -> proc_units_miu.html
      proc_miu_vision.html -> proc_units_miu_vision.html
"""

import os
import shutil
from pathlib import Path
import re

BASE_DIR = Path(__file__).parent.parent

# Define the renaming mappings for each triad
RENAME_MAPPINGS = {
    'in': {
        'in_miu.html': 'in_units_miu.html',
        'in_miu_vision.html': 'in_units_miu_vision.html',
        'in_miu_vision_products.html': 'in_units_miu_vision_products.html',
        'in_miu_vision_products_hardware.html': 'in_units_miu_vision_products_hardware.html',
        'in_miu_vision_products_software.html': 'in_units_miu_vision_products_software.html',
        'in_miu_vision_services.html': 'in_units_miu_vision_services.html',
        'in_miu_vision_services_consultancy.html': 'in_units_miu_vision_services_consultancy.html',
        'in_miu_vision_services_education.html': 'in_units_miu_vision_services_education.html',
        'in_miu_vision_services_rd.html': 'in_units_miu_vision_services_rd.html',
    },
    'processing': {
        'proc_miu.html': 'proc_units_miu.html',
        'proc_miu_vision.html': 'proc_units_miu_vision.html',
        'proc_miu_vision_products.html': 'proc_units_miu_vision_products.html',
        'proc_miu_vision_products_hardware.html': 'proc_units_miu_vision_products_hardware.html',
        'proc_miu_vision_products_software.html': 'proc_units_miu_vision_products_software.html',
        'proc_miu_vision_services.html': 'proc_units_miu_vision_services.html',
        'proc_miu_vision_services_consultancy.html': 'proc_units_miu_vision_services_consultancy.html',
        'proc_miu_vision_services_education.html': 'proc_units_miu_vision_services_education.html',
        'proc_miu_vision_services_rd.html': 'proc_units_miu_vision_services_rd.html',
    },
    'out': {
        'out_miu.html': 'out_units_miu.html',
        'out_miu_vision.html': 'out_units_miu_vision.html',
        'out_miu_vision_products.html': 'out_units_miu_vision_products.html',
        'out_miu_vision_products_hardware.html': 'out_units_miu_vision_products_hardware.html',
        'out_miu_vision_products_software.html': 'out_units_miu_vision_products_software.html',
        'out_miu_vision_services.html': 'out_units_miu_vision_services.html',
        'out_miu_vision_services_consultancy.html': 'out_units_miu_vision_services_consultancy.html',
        'out_miu_vision_services_education.html': 'out_units_miu_vision_services_education.html',
        'out_miu_vision_services_rd.html': 'out_units_miu_vision_services_rd.html',
    }
}

def find_and_rename_files(triad_name, rename_mapping):
    """Find and rename files in the units/miu structure"""
    triad_dir = BASE_DIR / triad_name
    units_dir = triad_dir / 'units'
    miu_dir = units_dir / 'miu'
    
    renamed_files = []
    
    # Rename MIU main file (in miu/ directory)
    for old_name, new_name in rename_mapping.items():
        if 'miu' in old_name and 'vision' not in old_name and 'products' not in old_name and 'services' not in old_name:
            old_path = miu_dir / old_name
            new_path = miu_dir / new_name
            if old_path.exists():
                print(f"  Renaming {old_path.relative_to(BASE_DIR)} -> {new_path.relative_to(BASE_DIR)}")
                shutil.move(str(old_path), str(new_path))
                renamed_files.append((old_name, new_name, old_path, new_path))
            break
    
    # Rename vision files
    vision_dir = miu_dir / 'vision'
    if vision_dir.exists():
        for old_name, new_name in rename_mapping.items():
            if 'vision' in old_name and 'products' not in old_name and 'services' not in old_name:
                old_path = vision_dir / old_name
                new_path = vision_dir / new_name
                if old_path.exists():
                    print(f"  Renaming {old_path.relative_to(BASE_DIR)} -> {new_path.relative_to(BASE_DIR)}")
                    shutil.move(str(old_path), str(new_path))
                    renamed_files.append((old_name, new_name, old_path, new_path))
                break
        
        # Rename products files
        products_dir = vision_dir / 'products'
        if products_dir.exists():
            for old_name, new_name in rename_mapping.items():
                if 'products' in old_name:
                    old_path = products_dir / old_name
                    new_path = products_dir / new_name
                    if old_path.exists():
                        print(f"  Renaming {old_path.relative_to(BASE_DIR)} -> {new_path.relative_to(BASE_DIR)}")
                        shutil.move(str(old_path), str(new_path))
                        renamed_files.append((old_name, new_name, old_path, new_path))
        
        # Rename services files
        services_dir = vision_dir / 'services'
        if services_dir.exists():
            for old_name, new_name in rename_mapping.items():
                if 'services' in old_name:
                    old_path = services_dir / old_name
                    new_path = services_dir / new_name
                    if old_path.exists():
                        print(f"  Renaming {old_path.relative_to(BASE_DIR)} -> {new_path.relative_to(BASE_DIR)}")
                        shutil.move(str(old_path), str(new_path))
                        renamed_files.append((old_name, new_name, old_path, new_path))
    
    return renamed_files

def update_links_in_html(file_path, old_name, new_name):
    """Update all references to old filename in HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Update href attributes
        content = re.sub(
            rf'href=["\']([^"\']*){re.escape(old_name)}["\']',
            rf'href="\1{new_name}"',
            content
        )
        
        # Update src attributes (if any)
        content = re.sub(
            rf'src=["\']([^"\']*){re.escape(old_name)}["\']',
            rf'src="\1{new_name}"',
            content
        )
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"    ⚠️  Error updating {file_path}: {e}")
        return False

def update_all_html_files(triad_name, renamed_files):
    """Update all HTML files in the triad to reference new filenames"""
    triad_dir = BASE_DIR / triad_name
    
    print(f"\n  Updating links in all HTML files...")
    updated_count = 0
    
    # Find all HTML files in the triad
    for html_file in triad_dir.rglob('*.html'):
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
    print("RENAMING FILES TO REFLECT HIERARCHY")
    print("="*60)
    print("\nThis will:")
    print("1. Rename files to include full hierarchy path in filename")
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

