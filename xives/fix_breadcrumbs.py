#!/usr/bin/env python3
"""
Fix all breadcrumb links to point to correct units pages
"""
import re
from pathlib import Path

base_dir = Path(__file__).parent.parent

# Fix breadcrumbs in in/units/miu files
in_miu_files = list((base_dir / 'in' / 'units' / 'miu').rglob("*.html"))

for html_file in in_miu_files:
    rel_path = html_file.relative_to(base_dir)
    depth = len(rel_path.parts) - 1  # minus filename
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Calculate correct path to in_units.html
    # From in/units/miu/vision/... we need to go up to in/units/
    if 'vision' in str(rel_path):
        # in/units/miu/vision/... -> ../../in_units.html
        correct_path = '../../in_units.html'
    elif 'miu' in str(rel_path) and 'vision' not in str(rel_path):
        # in/units/miu/... -> ../in_units.html
        correct_path = '../in_units.html'
    else:
        # Shouldn't happen, but just in case
        correct_path = '../in_units.html'
    
    # Replace all incorrect paths
    content = re.sub(r'href="[^"]*out/units/out_units\.html"', f'href="{correct_path}"', content)
    
    if content != original:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Fixed breadcrumb in {rel_path}")

print("\n✓ All breadcrumbs fixed!")



