#!/usr/bin/env python3
"""
Fix all old filename references to use new hierarchical filenames.
This will update all HTML and JS files to use the correct filenames.
"""

import re
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

# Mapping of old filenames to new filenames
OLD_TO_NEW_MAPPINGS = {
    # about_piandt children
    'in_mission_vision.html': 'in_about_piandt_mission_vision.html',
    'in_charitable_purposes.html': 'in_about_piandt_charitable_purposes.html',
    'in_our_approach.html': 'in_about_piandt_our_approach.html',
    'in_trustees.html': 'in_about_piandt_trustees.html',
    'in_governance.html': 'in_about_piandt_governance.html',
    
    'proc_mission_vision.html': 'proc_about_piandt_mission_vision.html',
    'proc_charitable_purposes.html': 'proc_about_piandt_charitable_purposes.html',
    'proc_our_approach.html': 'proc_about_piandt_our_approach.html',
    'proc_trustees.html': 'proc_about_piandt_trustees.html',
    'proc_governance.html': 'proc_about_piandt_governance.html',
    
    'out_mission_vision.html': 'out_about_piandt_mission_vision.html',
    'out_charitable_purposes.html': 'out_about_piandt_charitable_purposes.html',
    'out_our_approach.html': 'out_about_piandt_our_approach.html',
    'out_trustees.html': 'out_about_piandt_trustees.html',
    'out_governance.html': 'out_about_piandt_governance.html',
    
    # units/miu files
    'in_miu.html': 'in_units_miu.html',
    'in_miu_vision.html': 'in_units_miu_vision.html',
    'in_miu_vision_products.html': 'in_units_miu_vision_products.html',
    'in_miu_vision_products_hardware.html': 'in_units_miu_vision_products_hardware.html',
    'in_miu_vision_products_software.html': 'in_units_miu_vision_products_software.html',
    'in_miu_vision_services.html': 'in_units_miu_vision_services.html',
    'in_miu_vision_services_consultancy.html': 'in_units_miu_vision_services_consultancy.html',
    'in_miu_vision_services_education.html': 'in_units_miu_vision_services_education.html',
    'in_miu_vision_services_rd.html': 'in_units_miu_vision_services_rd.html',
    
    'proc_miu.html': 'proc_units_miu.html',
    'proc_miu_vision.html': 'proc_units_miu_vision.html',
    'proc_miu_vision_products.html': 'proc_units_miu_vision_products.html',
    'proc_miu_vision_products_hardware.html': 'proc_units_miu_vision_products_hardware.html',
    'proc_miu_vision_products_software.html': 'proc_units_miu_vision_products_software.html',
    'proc_miu_vision_services.html': 'proc_units_miu_vision_services.html',
    'proc_miu_vision_services_consultancy.html': 'proc_units_miu_vision_services_consultancy.html',
    'proc_miu_vision_services_education.html': 'proc_units_miu_vision_services_education.html',
    'proc_miu_vision_services_rd.html': 'proc_units_miu_vision_services_rd.html',
    
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

def fix_links_in_file(file_path):
    """Fix all old filename references in a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = []
        
        # Replace all old filenames with new ones
        for old_name, new_name in OLD_TO_NEW_MAPPINGS.items():
            # Pattern 1: href="old_name" or href="path/old_name"
            pattern1 = rf'href=["\']([^"\']*/)?{re.escape(old_name)}["\']'
            if re.search(pattern1, content):
                content = re.sub(
                    pattern1,
                    lambda m: f'href="{m.group(1) or ""}{new_name}"',
                    content
                )
                changes_made.append(f'{old_name} -> {new_name}')
            
            # Pattern 2: src="old_name" or src="path/old_name"
            pattern2 = rf'src=["\']([^"\']*/)?{re.escape(old_name)}["\']'
            if re.search(pattern2, content):
                content = re.sub(
                    pattern2,
                    lambda m: f'src="{m.group(1) or ""}{new_name}"',
                    content
                )
                changes_made.append(f'{old_name} -> {new_name} (src)')
            
            # Pattern 3: Direct filename reference (for JS files)
            pattern3 = rf'["\']{re.escape(old_name)}["\']'
            if re.search(pattern3, content) and file_path.suffix == '.js':
                content = re.sub(
                    pattern3,
                    f'"{new_name}"',
                    content
                )
                changes_made.append(f'{old_name} -> {new_name} (string)')
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, changes_made
        return False, []
    except Exception as e:
        print(f"  ⚠️  Error processing {file_path}: {e}")
        return False, []

def main():
    """Fix all old links in HTML and JS files"""
    print("="*60)
    print("FIXING ALL OLD FILENAME REFERENCES")
    print("="*60)
    
    # Get all HTML and JS files
    files_to_check = []
    for ext in ['*.html', '*.js']:
        for file_path in BASE_DIR.rglob(ext):
            if 'site_agent' not in str(file_path) and 'node_modules' not in str(file_path):
                files_to_check.append(file_path)
    
    files_to_check.sort()
    
    total_fixed = 0
    total_changes = 0
    
    for file_path in files_to_check:
        fixed, changes = fix_links_in_file(file_path)
        if fixed:
            total_fixed += 1
            total_changes += len(changes)
            rel_path = file_path.relative_to(BASE_DIR)
            print(f"  ✓ Fixed {rel_path}")
            for change in changes:
                print(f"     - {change}")
    
    print("\n" + "="*60)
    print(f"✅ COMPLETE!")
    print(f"   Files updated: {total_fixed}")
    print(f"   Total changes: {total_changes}")
    print("="*60)

if __name__ == '__main__':
    main()

