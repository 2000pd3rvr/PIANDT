#!/usr/bin/env python3
"""
Update all links to in.html, processing.html, and out.html after moving them
"""
import re
from pathlib import Path

base_dir = Path(__file__).parent.parent

# Get all HTML files
html_files = list(base_dir.rglob("*.html"))
html_files = [f for f in html_files if 'site_agent' not in str(f)]

updates_made = 0

for html_file in html_files:
    rel_path = html_file.relative_to(base_dir)
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    file_updates = 0
    
    # Determine depth for relative paths
    depth = len(rel_path.parts) - 1
    
    # Update links based on file location
    if 'in/' in str(rel_path):
        # Files in in/ directory
        # in.html -> in.html (same directory)
        content = re.sub(r'href=["\'](\.\./)*in\.html["\']', 'href="in.html"', content)
        # processing.html -> ../processing/processing.html
        content = re.sub(r'href=["\'](\.\./)*processing\.html["\']', 'href="../processing/processing.html"', content)
        # out.html -> ../out/out.html
        content = re.sub(r'href=["\'](\.\./)*out\.html["\']', 'href="../out/out.html"', content)
    elif 'processing/' in str(rel_path):
        # Files in processing/ directory
        # in.html -> ../in/in.html
        content = re.sub(r'href=["\'](\.\./)*in\.html["\']', 'href="../in/in.html"', content)
        # processing.html -> processing.html (same directory)
        content = re.sub(r'href=["\'](\.\./)*processing\.html["\']', 'href="processing.html"', content)
        # out.html -> ../out/out.html
        content = re.sub(r'href=["\'](\.\./)*out\.html["\']', 'href="../out/out.html"', content)
    elif 'out/' in str(rel_path):
        # Files in out/ directory
        # in.html -> ../in/in.html
        content = re.sub(r'href=["\'](\.\./)*in\.html["\']', 'href="../in/in.html"', content)
        # processing.html -> ../processing/processing.html
        content = re.sub(r'href=["\'](\.\./)*processing\.html["\']', 'href="../processing/processing.html"', content)
        # out.html -> out.html (same directory)
        content = re.sub(r'href=["\'](\.\./)*out\.html["\']', 'href="out.html"', content)
    else:
        # Files in root directory (like index.html)
        # in.html -> in/in.html
        content = re.sub(r'href=["\'](\.\./)*in\.html["\']', 'href="in/in.html"', content)
        # processing.html -> processing/processing.html
        content = re.sub(r'href=["\'](\.\./)*processing\.html["\']', 'href="processing/processing.html"', content)
        # out.html -> out/out.html
        content = re.sub(r'href=["\'](\.\./)*out\.html["\']', 'href="out/out.html"', content)
    
    # Also update breadcrumb links
    # Fix breadcrumbs that reference these pages
    content = re.sub(r'href=["\']\.\./in\.html["\']', 'href="../in/in.html"', content)
    content = re.sub(r'href=["\']\.\./processing\.html["\']', 'href="../processing/processing.html"', content)
    content = re.sub(r'href=["\']\.\./out\.html["\']', 'href="../out/out.html"', content)
    
    content = re.sub(r'href=["\']\.\./\.\./in\.html["\']', 'href="../../in/in.html"', content)
    content = re.sub(r'href=["\']\.\./\.\./processing\.html["\']', 'href="../../processing/processing.html"', content)
    content = re.sub(r'href=["\']\.\./\.\./out\.html["\']', 'href="../../out/out.html"', content)
    
    content = re.sub(r'href=["\']\.\./\.\./\.\./in\.html["\']', 'href="../../../in/in.html"', content)
    content = re.sub(r'href=["\']\.\./\.\./\.\./processing\.html["\']', 'href="../../../processing/processing.html"', content)
    content = re.sub(r'href=["\']\.\./\.\./\.\./out\.html["\']', 'href="../../../out/out.html"', content)
    
    if content != original:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        updates_made += 1
        print(f"✓ Updated {rel_path}")

print(f"\n✓ Updated {updates_made} files")



