#!/usr/bin/env python3
"""
Comprehensive fix for all links and breadcrumbs in HTML files
"""
import re
from pathlib import Path

base_dir = Path(__file__).parent.parent

def calculate_relative_path(from_file, to_file):
    """Calculate relative path from one file to another"""
    from_path = Path(from_file).parent
    to_path = Path(to_file)
    
    try:
        rel_path = Path(to_path).relative_to(from_path)
        return str(rel_path).replace('\\', '/')
    except ValueError:
        # If files are in different trees, calculate from base
        from_rel = Path(from_file).relative_to(base_dir)
        to_rel = Path(to_file).relative_to(base_dir)
        
        # Count how many levels up needed
        from_depth = len(from_rel.parent.parts)
        to_depth = len(to_rel.parent.parts)
        
        # Go up to common ancestor
        ups = ['..'] * from_depth
        # Then down to target
        if to_depth == 0:
            return '../'.join(ups) + str(to_rel)
        else:
            return '../'.join(ups) + str(to_rel)

def fix_breadcrumbs(content, file_path):
    """Fix breadcrumb links based on file location"""
    rel_path = file_path.relative_to(base_dir)
    parts = rel_path.parts
    
    fixes = 0
    
    # Determine which triad this file belongs to
    if 'in/' in str(rel_path) or str(rel_path).startswith('in'):
        triad = 'in'
        triad_page = 'in.html'
    elif 'processing/' in str(rel_path) or str(rel_path).startswith('processing'):
        triad = 'proc'
        triad_page = 'processing.html'
    elif 'out/' in str(rel_path) or str(rel_path).startswith('out'):
        triad = 'out'
        triad_page = 'out.html'
    else:
        return content, fixes
    
    # Fix wrong breadcrumb links in in/units/miu files
    # They incorrectly point to out/units/out_units.html
    if 'in/units/miu' in str(rel_path):
        # Calculate correct paths
        depth = len(parts) - 1  # minus filename
        ups = '../' * depth
        
        # Fix units link - should point to in/units/in_units.html
        wrong_pattern = r'href="[^"]*out/units/out_units\.html"'
        correct_units_path = ups + 'in_units.html' if depth <= 3 else '../' * (depth - 2) + 'in_units.html'
        
        # More precise: find the units link in breadcrumb
        pattern = r'(<a href=")[^"]*out/units/out_units\.html("[^>]*>units</a>)'
        replacement = r'\1' + correct_units_path + r'\2'
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            fixes += 1
    
    # Fix breadcrumbs that point to wrong triad pages
    # Each file should link to its own triad's main page
    if triad == 'in':
        # Fix links to out.html or processing.html in in/ files
        wrong_triad_patterns = [
            (r'href="[^"]*out\.html"', f'href="../{triad_page}"'),
            (r'href="[^"]*processing\.html"', f'href="../{triad_page}"'),
        ]
        for pattern, replacement in wrong_triad_patterns:
            if re.search(pattern, content):
                # Only replace in breadcrumb context
                breadcrumb_pattern = r'(<span class="logo-suffix">[^<]*<a )' + pattern[6:]  # Remove 'href='
                if re.search(breadcrumb_pattern, content):
                    content = re.sub(breadcrumb_pattern, r'\1' + replacement, content)
                    fixes += 1
    
    return content, fixes

def fix_navigation_links(content, file_path):
    """Fix navigation menu links"""
    rel_path = file_path.relative_to(base_dir)
    fixes = 0
    
    # Already fixed in index.html, but check other files
    # Proc dropdown should point to proc_units
    if 'processing' in str(rel_path) or 'index' in str(rel_path):
        pattern = r'(<li>\s*<a href="processing/about_piandt/proc_about_piandt\.html"[^>]*>about PIANDT[^<]*</a>\s*<ul>.*?</ul>\s*</li>\s*<li>\s*<a href=")in/units/in_units\.html(" class="dropdown-link">units)'
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, r'\1processing/units/proc_units.html\2', content, flags=re.DOTALL)
            fixes += 1
    
    # Out dropdown should point to out_units
    if 'out' in str(rel_path) or 'index' in str(rel_path):
        pattern = r'(<li>\s*<a href="out/about_piandt/out_about_piandt\.html"[^>]*>about PIANDT[^<]*</a>\s*<ul>.*?</ul>\s*</li>\s*<li>\s*<a href=")in/units/in_units\.html(" class="dropdown-link">units)'
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, r'\1out/units/out_units.html\2', content, flags=re.DOTALL)
            fixes += 1
    
    return content, fixes

# Get all HTML files
html_files = list(base_dir.rglob("*.html"))
html_files = [f for f in html_files if 'site_agent' not in str(f)]

total_fixes = 0

for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    file_fixes = 0
    
    # Fix breadcrumbs
    content, breadcrumb_fixes = fix_breadcrumbs(content, html_file)
    file_fixes += breadcrumb_fixes
    
    # Fix navigation links
    content, nav_fixes = fix_navigation_links(content, html_file)
    file_fixes += nav_fixes
    
    if content != original:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        total_fixes += file_fixes
        rel_path = html_file.relative_to(base_dir)
        print(f"✓ Fixed {file_fixes} issue(s) in {rel_path}")

print(f"\n✓ Total fixes: {total_fixes}")



