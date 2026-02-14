#!/usr/bin/env python3
"""
Update all menu and child menu links across all HTML pages to use the new hierarchical filenames.
"""

import os
from pathlib import Path
import re

BASE_DIR = Path(__file__).parent.parent

# Define the correct filename mappings
FILENAME_MAPPINGS = {
    'in': {
        'about_piandt': {
            'parent': 'in_about_piandt.html',
            'children': {
                'in_mission_vision.html': 'in_about_piandt_mission_vision.html',
                'in_charitable_purposes.html': 'in_about_piandt_charitable_purposes.html',
                'in_our_approach.html': 'in_about_piandt_our_approach.html',
                'in_trustees.html': 'in_about_piandt_trustees.html',
                'in_governance.html': 'in_about_piandt_governance.html',
            }
        },
        'units': {
            'parent': 'in_units.html',
            'children': {
                'in_miu.html': 'in_units_miu.html',
                'in_miu_vision.html': 'in_units_miu_vision.html',
                'in_miu_vision_products.html': 'in_units_miu_vision_products.html',
                'in_miu_vision_products_hardware.html': 'in_units_miu_vision_products_hardware.html',
                'in_miu_vision_products_software.html': 'in_units_miu_vision_products_software.html',
                'in_miu_vision_services.html': 'in_units_miu_vision_services.html',
                'in_miu_vision_services_consultancy.html': 'in_units_miu_vision_services_consultancy.html',
                'in_miu_vision_services_education.html': 'in_units_miu_vision_services_education.html',
                'in_miu_vision_services_rd.html': 'in_units_miu_vision_services_rd.html',
            }
        }
    },
    'processing': {
        'about_piandt': {
            'parent': 'proc_about_piandt.html',
            'children': {
                'proc_mission_vision.html': 'proc_about_piandt_mission_vision.html',
                'proc_charitable_purposes.html': 'proc_about_piandt_charitable_purposes.html',
                'proc_our_approach.html': 'proc_about_piandt_our_approach.html',
                'proc_trustees.html': 'proc_about_piandt_trustees.html',
                'proc_governance.html': 'proc_about_piandt_governance.html',
            }
        },
        'units': {
            'parent': 'proc_units.html',
            'children': {
                'proc_miu.html': 'proc_units_miu.html',
                'proc_miu_vision.html': 'proc_units_miu_vision.html',
                'proc_miu_vision_products.html': 'proc_units_miu_vision_products.html',
                'proc_miu_vision_products_hardware.html': 'proc_units_miu_vision_products_hardware.html',
                'proc_miu_vision_products_software.html': 'proc_units_miu_vision_products_software.html',
                'proc_miu_vision_services.html': 'proc_units_miu_vision_services.html',
                'proc_miu_vision_services_consultancy.html': 'proc_units_miu_vision_services_consultancy.html',
                'proc_miu_vision_services_education.html': 'proc_units_miu_vision_services_education.html',
                'proc_miu_vision_services_rd.html': 'proc_units_miu_vision_services_rd.html',
            }
        }
    },
    'out': {
        'about_piandt': {
            'parent': 'out_about_piandt.html',
            'children': {
                'out_mission_vision.html': 'out_about_piandt_mission_vision.html',
                'out_charitable_purposes.html': 'out_about_piandt_charitable_purposes.html',
                'out_our_approach.html': 'out_about_piandt_our_approach.html',
                'out_trustees.html': 'out_about_piandt_trustees.html',
                'out_governance.html': 'out_about_piandt_governance.html',
            }
        },
        'units': {
            'parent': 'out_units.html',
            'children': {
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
    }
}

def calculate_relative_path(from_file, to_file, triad_name):
    """Calculate relative path from one file to another"""
    from_path = Path(from_file).parent
    to_path = Path(to_file).parent
    
    # Get relative path
    try:
        rel_path = os.path.relpath(to_path, from_path)
        if rel_path == '.':
            return ''
        return rel_path.replace('\\', '/') + '/'
    except:
        # Fallback: calculate based on depth
        from_depth = len(str(from_path).replace(str(BASE_DIR / triad_name), '').strip('/').split('/'))
        to_depth = len(str(to_path).replace(str(BASE_DIR / triad_name), '').strip('/').split('/'))
        
        if to_depth < from_depth:
            return '../' * (from_depth - to_depth)
        elif to_depth > from_depth:
            # Need to go into subdirectories
            parts = str(to_path).replace(str(BASE_DIR / triad_name), '').strip('/').split('/')
            return '/'.join(parts[from_depth:]) + '/' if parts else ''
        return ''

def update_menu_links_in_file(file_path, triad_name, mappings):
    """Update all menu links in a single HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Update links for about_piandt section
        about_mapping = mappings['about_piandt']
        
        # Update child links - replace old names with new names
        for old_name, new_name in about_mapping['children'].items():
            # Pattern 1: href="about_piandt/old_name" or any path with about_piandt/
            content = re.sub(
                rf'href=["\']([^"\']*about_piandt/){re.escape(old_name)}["\']',
                rf'href="\1{new_name}"',
                content
            )
            
            # Pattern 2: href="old_name" (direct reference, likely in same directory)
            # Only replace if we're sure it's a menu link
            content = re.sub(
                rf'href=["\']{re.escape(old_name)}["\']',
                rf'href="{new_name}"',
                content
            )
        
        # Update links for units section
        units_mapping = mappings['units']
        
        # Update child links for units
        for old_name, new_name in units_mapping['children'].items():
            # Replace old_name with new_name in all href attributes
            # This will catch all variations: units/miu/vision/products/old_name, etc.
            content = re.sub(
                rf'href=["\']([^"\']*){re.escape(old_name)}["\']',
                rf'href="\1{new_name}"',
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

def update_all_menu_links():
    """Update all menu links across all HTML files"""
    print("="*60)
    print("UPDATING ALL MENU AND CHILD MENU LINKS")
    print("="*60)
    print("\nThis will update all navigation menu links to use the new hierarchical filenames")
    print("\n" + "="*60)
    
    total_updated = 0
    
    for triad_name, mappings in FILENAME_MAPPINGS.items():
        print(f"\n{'='*60}")
        print(f"Processing {triad_name.upper()} triad")
        print(f"{'='*60}")
        
        triad_dir = BASE_DIR / triad_name
        if not triad_dir.exists():
            print(f"  ⚠️  Directory {triad_dir} does not exist")
            continue
        
        updated_count = 0
        
        # Find all HTML files in the triad
        html_files = list(triad_dir.rglob('*.html'))
        print(f"  Found {len(html_files)} HTML files in {triad_name}")
        
        for html_file in html_files:
            if update_menu_links_in_file(html_file, triad_name, mappings):
                updated_count += 1
                print(f"  ✓ Updated {html_file.relative_to(BASE_DIR)}")
        
        # Also check root level files (index.html, etc.) - but only once
        if triad_name == 'in':  # Only process root files once
            for html_file in BASE_DIR.glob('*.html'):
                if update_menu_links_in_file(html_file, triad_name, mappings):
                    updated_count += 1
                    print(f"  ✓ Updated {html_file.relative_to(BASE_DIR)}")
        
        print(f"\n  ✓ Updated {updated_count} files in {triad_name}")
        total_updated += updated_count
    
    print("\n" + "="*60)
    print(f"✅ ALL MENU LINKS UPDATED!")
    print(f"   Total files updated: {total_updated}")
    print("="*60)
    print("\nPlease test the pages to ensure:")
    print("- All navigation menus work correctly")
    print("- All dropdown menus work correctly")
    print("- All links point to correct files")

if __name__ == '__main__':
    update_all_menu_links()

