#!/usr/bin/env python3
"""
Fix all links and breadcrumbs in HTML files based on valid URLs from pages.html
"""
import re
from pathlib import Path
from html import unescape

base_dir = Path(__file__).parent.parent

# Read pages.html to get all valid URLs
pages_html = base_dir / 'site_agent' / 'pages.html'
with open(pages_html, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract all valid URLs from the table
url_pattern = r'<td class="url-col">(.*?)</td>'
valid_urls = set(re.findall(url_pattern, content))
valid_urls = {unescape(url.strip()) for url in valid_urls if url.strip()}
valid_urls.add('index.html')
valid_urls.add('in.html')
valid_urls.add('processing.html')
valid_urls.add('out.html')

# Map of common incorrect links to correct ones
link_fixes = {
    # Navigation menu fixes - wrong units links
    'href="in/units/in_units.html"': {
        'context': 'in.html or index.html in In dropdown',
        'fix': 'href="in/units/in_units.html"'
    },
    # Proc dropdown should point to proc_units, not in_units
    'href="in/units/in_units.html"': {
        'context': 'processing.html or index.html in Proc dropdown',
        'fix': 'href="processing/units/proc_units.html"'
    },
    # Out dropdown should point to out_units, not in_units
    'href="in/units/in_units.html"': {
        'context': 'out.html or index.html in Out dropdown',
        'fix': 'href="out/units/out_units.html"'
    }
}

print(f"Found {len(valid_urls)} valid URLs")
print("\nStarting link fixes...")

# Get all HTML files
html_files = list(base_dir.rglob("*.html"))
html_files = [f for f in html_files if 'site_agent' not in str(f)]

fixes_made = 0

for html_file in html_files:
    rel_path = html_file.relative_to(base_dir)
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    file_fixes = 0
    
    # Fix 1: Wrong units links in navigation menus
    # In Proc dropdown, units should point to proc_units
    if 'processing.html' in str(html_file) or 'index.html' in str(html_file):
        # Fix Proc dropdown units link
        old_pattern = r'(<li>\s*<a href="processing/about_piandt/proc_about_piandt.html"[^>]*>about PIANDT[^<]*</a>\s*<ul>.*?</ul>\s*</li>\s*<li>\s*<a href=")in/units/in_units.html(" class="dropdown-link">units)'
        new_link = r'\1processing/units/proc_units.html\2'
        if re.search(old_pattern, content, re.DOTALL):
            content = re.sub(old_pattern, new_link, content, flags=re.DOTALL)
            file_fixes += 1
            print(f"  Fixed Proc dropdown units link in {rel_path}")
    
    # Fix Out dropdown units link
    if 'out.html' in str(html_file) or 'index.html' in str(html_file):
        # Fix Out dropdown units link
        old_pattern = r'(<li>\s*<a href="out/about_piandt/out_about_piandt.html"[^>]*>about PIANDT[^<]*</a>\s*<ul>.*?</ul>\s*</li>\s*<li>\s*<a href=")in/units/in_units.html(" class="dropdown-link">units)'
        new_link = r'\1out/units/out_units.html\2'
        if re.search(old_pattern, content, re.DOTALL):
            content = re.sub(old_pattern, new_link, content, flags=re.DOTALL)
            file_fixes += 1
            print(f"  Fixed Out dropdown units link in {rel_path}")
    
    # Fix 2: Breadcrumb links - need to calculate correct relative paths
    # This is complex, so we'll handle it per file based on location
    
    # Fix 3: Broken relative paths in out_units.html
    if 'out/units/out_units.html' in str(html_file):
        # Fix broken links like ../in/about_piandt/... to correct paths
        content = re.sub(r'href="../in/about_piandt/in_about_piandt.html"', 
                        'href="../../in/about_piandt/in_about_piandt.html"', content)
        content = re.sub(r'href="../in/about_piandt/in_mission_vision.html"', 
                        'href="../../in/about_piandt/in_mission_vision.html"', content)
        content = re.sub(r'href="../in/about_piandt/in_charitable_purposes.html"', 
                        'href="../../in/about_piandt/in_charitable_purposes.html"', content)
        content = re.sub(r'href="../in/about_piandt/in_our_approach.html"', 
                        'href="../../in/about_piandt/in_our_approach.html"', content)
        content = re.sub(r'href="../in/units/in_units.html"', 
                        'href="../../in/units/in_units.html"', content)
        content = re.sub(r'href="../in/units/miu/in_miu.html"', 
                        'href="../../in/units/miu/in_miu.html"', content)
        if content != original_content:
            file_fixes += 1
            print(f"  Fixed relative paths in {rel_path}")
    
    # Fix 4: Breadcrumb in out_units.html
    if 'out/units/out_units.html' in str(html_file):
        # Fix breadcrumb: Out->units should link correctly
        old_breadcrumb = r'<span class="logo-suffix"><a href="../../out.html"[^>]*>Out</a>-&gt;<a href="out_units.html"[^>]*>units</a></span>'
        new_breadcrumb = '<span class="logo-suffix"><a href="../../out.html" style="text-decoration: none; color: inherit;">Out</a>-&gt;<a href="out_units.html" style="text-decoration: none; color: inherit;">units</a></span>'
        if re.search(old_breadcrumb, content):
            content = re.sub(old_breadcrumb, new_breadcrumb, content)
            file_fixes += 1
            print(f"  Fixed breadcrumb in {rel_path}")
    
    if content != original_content:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        fixes_made += file_fixes
        print(f"✓ Fixed {file_fixes} issue(s) in {rel_path}")

print(f"\n✓ Total fixes made: {fixes_made}")



