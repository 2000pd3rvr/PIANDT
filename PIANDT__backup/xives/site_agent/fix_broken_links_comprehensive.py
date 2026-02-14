#!/usr/bin/env python3
"""
Comprehensive fix for all broken links to triad main pages
"""
import re
from pathlib import Path

base_dir = Path(__file__).parent.parent

# Get all HTML files
html_files = list(base_dir.rglob("*.html"))
html_files = [f for f in html_files if 'site_agent' not in str(f)]

fixes_made = 0
broken_links = []

for html_file in html_files:
    rel_path = html_file.relative_to(base_dir)
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Calculate how many levels deep we are
    depth = len(rel_path.parts) - 1
    
    # Determine which triad directory we're in (if any)
    in_in_dir = 'in/' in str(rel_path) and not str(rel_path).startswith('in/in.html')
    in_processing_dir = 'processing/' in str(rel_path) and not str(rel_path).startswith('processing/processing.html')
    in_out_dir = 'out/' in str(rel_path) and not str(rel_path).startswith('out/out.html')
    
    # Fix href="in.html" patterns
    # In files within in/ subdirectories, need to go up to in/in.html
    if in_in_dir:
        # Files in in/ subdirectories (but not in/in.html itself)
        content = re.sub(r'href=["\']in\.html["\']', 'href="../in.html"', content)
        content = re.sub(r'href=["\']\.\./in\.html["\']', 'href="../in.html"', content)
        # Fix deeper nested
        content = re.sub(r'href=["\']\.\./\.\./in\.html["\']', 'href="../../in.html"', content)
        content = re.sub(r'href=["\']\.\./\.\./\.\./in\.html["\']', 'href="../../../in.html"', content)
        content = re.sub(r'href=["\']\.\./\.\./\.\./\.\./in\.html["\']', 'href="../../../../in.html"', content)
        content = re.sub(r'href=["\']\.\./\.\./\.\./\.\./\.\./in\.html["\']', 'href="../../../../../in.html"', content)
    
    # Fix href="processing.html" patterns
    if in_processing_dir:
        content = re.sub(r'href=["\']processing\.html["\']', 'href="../processing.html"', content)
        content = re.sub(r'href=["\']\.\./processing\.html["\']', 'href="../processing.html"', content)
        content = re.sub(r'href=["\']\.\./\.\./processing\.html["\']', 'href="../../processing.html"', content)
        content = re.sub(r'href=["\']\.\./\.\./\.\./processing\.html["\']', 'href="../../../processing.html"', content)
    
    # Fix href="out.html" patterns
    if in_out_dir:
        content = re.sub(r'href=["\']out\.html["\']', 'href="../out.html"', content)
        content = re.sub(r'href=["\']\.\./out\.html["\']', 'href="../out.html"', content)
        content = re.sub(r'href=["\']\.\./\.\./out\.html["\']', 'href="../../out.html"', content)
        content = re.sub(r'href=["\']\.\./\.\./\.\./out\.html["\']', 'href="../../../out.html"', content)
    
    # Fix cross-triad references
    # Files in in/ need ../processing/processing.html and ../out/out.html
    if in_in_dir:
        content = re.sub(r'href=["\']\.\./processing\.html["\']', 'href="../processing/processing.html"', content)
        content = re.sub(r'href=["\']\.\./out\.html["\']', 'href="../out/out.html"', content)
        # Fix deeper nested cross-references
        content = re.sub(r'href=["\']\.\./\.\./processing\.html["\']', 'href="../../processing/processing.html"', content)
        content = re.sub(r'href=["\']\.\./\.\./out\.html["\']', 'href="../../out/out.html"', content)
    
    # Files in processing/ need ../in/in.html and ../out/out.html
    if in_processing_dir:
        content = re.sub(r'href=["\']\.\./in\.html["\']', 'href="../in/in.html"', content)
        content = re.sub(r'href=["\']\.\./out\.html["\']', 'href="../out/out.html"', content)
        content = re.sub(r'href=["\']\.\./\.\./in\.html["\']', 'href="../../in/in.html"', content)
        content = re.sub(r'href=["\']\.\./\.\./out\.html["\']', 'href="../../out/out.html"', content)
    
    # Files in out/ need ../in/in.html and ../processing/processing.html
    if in_out_dir:
        content = re.sub(r'href=["\']\.\./in\.html["\']', 'href="../in/in.html"', content)
        content = re.sub(r'href=["\']\.\./processing\.html["\']', 'href="../processing/processing.html"', content)
        content = re.sub(r'href=["\']\.\./\.\./in\.html["\']', 'href="../../in/in.html"', content)
        content = re.sub(r'href=["\']\.\./\.\./processing\.html["\']', 'href="../../processing/processing.html"', content)
    
    # Fix root directory files (index.html)
    if depth == 0:
        # Already handled by previous script, but ensure they're correct
        content = re.sub(r'href=["\']in\.html["\']', 'href="in/in.html"', content)
        content = re.sub(r'href=["\']processing\.html["\']', 'href="processing/processing.html"', content)
        content = re.sub(r'href=["\']out\.html["\']', 'href="out/out.html"', content)
    
    if content != original:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        fixes_made += 1
        
        # Find what changed
        original_matches = set(re.findall(r'href=["\']([^"\']*?)(in|processing|out)\.html["\']', original))
        new_matches = set(re.findall(r'href=["\']([^"\']*?)(in|processing|out)\.html["\']', content))
        changed = original_matches - new_matches
        if changed:
            broken_links.append((str(rel_path), changed))
        print(f"✓ Fixed {rel_path}")

if broken_links:
    print(f"\n=== Summary of Fixes ===")
    for file, links in broken_links[:10]:
        print(f"  {file}: {len(links)} link(s) fixed")

print(f"\n✓ Updated {fixes_made} files")



