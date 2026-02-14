#!/usr/bin/env python3
"""
Fix navigation menu links that incorrectly include directory prefixes
when files are already within those directories
"""
import re
from pathlib import Path

base_dir = Path(__file__).parent.parent

# Get all HTML files
html_files = list(base_dir.rglob("*.html"))
html_files = [f for f in html_files if 'site_agent' not in str(f)]

fixes_made = 0

for html_file in html_files:
    rel_path = html_file.relative_to(base_dir)
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Fix links in files within in/ directory
    if 'in/' in str(rel_path) and not str(rel_path) == 'in/in.html':
        # Remove "in/" prefix from links since we're already in in/
        content = re.sub(r'href=["\']in/(about_piandt/[^"\']+)["\']', r'href="\1"', content)
        content = re.sub(r'href=["\']in/(units/[^"\']+)["\']', r'href="\1"', content)
        # Fix relative paths that incorrectly add in/
        content = re.sub(r'href=["\']\.\./in/(about_piandt/[^"\']+)["\']', r'href="../about_piandt/\1"', content)
        content = re.sub(r'href=["\']\.\./in/(units/[^"\']+)["\']', r'href="../units/\1"', content)
    
    # Fix links in files within processing/ directory
    if 'processing/' in str(rel_path) and not str(rel_path) == 'processing/processing.html':
        # Remove "processing/" prefix from links since we're already in processing/
        content = re.sub(r'href=["\']processing/(about_piandt/[^"\']+)["\']', r'href="\1"', content)
        content = re.sub(r'href=["\']processing/(units/[^"\']+)["\']', r'href="\1"', content)
        # Fix relative paths
        content = re.sub(r'href=["\']\.\./processing/(about_piandt/[^"\']+)["\']', r'href="../about_piandt/\1"', content)
        content = re.sub(r'href=["\']\.\./processing/(units/[^"\']+)["\']', r'href="../units/\1"', content)
    
    # Fix links in files within out/ directory
    if 'out/' in str(rel_path) and not str(rel_path) == 'out/out.html':
        # Remove "out/" prefix from links since we're already in out/
        content = re.sub(r'href=["\']out/(about_piandt/[^"\']+)["\']', r'href="\1"', content)
        content = re.sub(r'href=["\']out/(units/[^"\']+)["\']', r'href="\1"', content)
        # Fix relative paths
        content = re.sub(r'href=["\']\.\./out/(about_piandt/[^"\']+)["\']', r'href="../about_piandt/\1"', content)
        content = re.sub(r'href=["\']\.\./out/(units/[^"\']+)["\']', r'href="../units/\1"', content)
    
    if content != original:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        fixes_made += 1
        print(f"✓ Fixed navigation paths in {rel_path}")

print(f"\n✓ Updated {fixes_made} files")



