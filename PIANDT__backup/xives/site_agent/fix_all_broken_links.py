#!/usr/bin/env python3
"""
Thoroughly search and fix all broken links to in.html, processing.html, and out.html
"""
import re
from pathlib import Path

base_dir = Path(__file__).parent.parent

# Get all HTML files
html_files = list(base_dir.rglob("*.html"))
html_files = [f for f in html_files if 'site_agent' not in str(f)]

broken_links_found = []
fixes_made = 0

for html_file in html_files:
    rel_path = html_file.relative_to(base_dir)
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Calculate relative path depth
    depth = len(rel_path.parts) - 1
    
    # Find all href attributes that might contain broken links
    # Pattern to match href="..." with in.html, processing.html, or out.html
    patterns_to_fix = [
        # Direct references like href="in.html" or href="../in.html"
        (r'href=["\']([^"\']*?)(?<!in/)in\.html["\']', 'in.html', 'in/in.html'),
        (r'href=["\']([^"\']*?)(?<!processing/)processing\.html["\']', 'processing.html', 'processing/processing.html'),
        (r'href=["\']([^"\']*?)(?<!out/)out\.html["\']', 'out.html', 'out/out.html'),
    ]
    
    for pattern, old_name, new_name in patterns_to_fix:
        matches = re.finditer(pattern, content)
        for match in matches:
            full_match = match.group(0)
            prefix = match.group(1) if match.groups() else ''
            
            # Skip if it's already correct (e.g., in/in.html, processing/processing.html, out/out.html)
            if new_name.split('/')[0] in prefix:
                continue
            
            # Determine correct path based on file location
            if 'in/' in str(rel_path):
                # File is in in/ directory
                if old_name == 'in.html':
                    replacement = 'href="in.html"'  # Same directory
                elif old_name == 'processing.html':
                    replacement = 'href="../processing/processing.html"'
                elif old_name == 'out.html':
                    replacement = 'href="../out/out.html"'
            elif 'processing/' in str(rel_path):
                # File is in processing/ directory
                if old_name == 'in.html':
                    replacement = 'href="../in/in.html"'
                elif old_name == 'processing.html':
                    replacement = 'href="processing.html"'  # Same directory
                elif old_name == 'out.html':
                    replacement = 'href="../out/out.html"'
            elif 'out/' in str(rel_path):
                # File is in out/ directory
                if old_name == 'in.html':
                    replacement = 'href="../in/in.html"'
                elif old_name == 'processing.html':
                    replacement = 'href="../processing/processing.html"'
                elif old_name == 'out.html':
                    replacement = 'href="out.html"'  # Same directory
            else:
                # File is in root directory
                if old_name == 'in.html':
                    replacement = 'href="in/in.html"'
                elif old_name == 'processing.html':
                    replacement = 'href="processing/processing.html"'
                elif old_name == 'out.html':
                    replacement = 'href="out/out.html"'
            
            # Preserve the prefix if it exists (like ../ or ../../)
            if prefix:
                # Calculate how many ../ we need
                if prefix.startswith('../'):
                    # Keep the relative path structure
                    replacement = f'href="{prefix}{new_name}"'
                else:
                    replacement = f'href="{prefix}{new_name}"'
            
            content = content.replace(full_match, replacement)
            broken_links_found.append((str(rel_path), full_match, replacement))
    
    # Also fix any remaining patterns with different quote styles or paths
    # Fix patterns like href='in.html' or href="../in.html" in subdirectories
    replacements = [
        # In subdirectories, fix relative paths
        (r'href=["\']\.\./in\.html["\']', lambda m: 'href="../in/in.html"' if 'in/' not in str(rel_path) else 'href="in.html"'),
        (r'href=["\']\.\./processing\.html["\']', lambda m: 'href="../processing/processing.html"' if 'processing/' not in str(rel_path) else 'href="processing.html"'),
        (r'href=["\']\.\./out\.html["\']', lambda m: 'href="../out/out.html"' if 'out/' not in str(rel_path) else 'href="out.html"'),
        
        # Fix deeper nested paths
        (r'href=["\']\.\./\.\./in\.html["\']', lambda m: 'href="../../in/in.html"'),
        (r'href=["\']\.\./\.\./processing\.html["\']', lambda m: 'href="../../processing/processing.html"'),
        (r'href=["\']\.\./\.\./out\.html["\']', lambda m: 'href="../../out/out.html"'),
        
        (r'href=["\']\.\./\.\./\.\./in\.html["\']', lambda m: 'href="../../../in/in.html"'),
        (r'href=["\']\.\./\.\./\.\./processing\.html["\']', lambda m: 'href="../../../processing/processing.html"'),
        (r'href=["\']\.\./\.\./\.\./out\.html["\']', lambda m: 'href="../../../out/out.html"'),
    ]
    
    for pattern, replacement_func in replacements:
        matches = list(re.finditer(pattern, content))
        for match in matches:
            replacement = replacement_func(match)
            content = content.replace(match.group(0), replacement)
            if match.group(0) != replacement:
                broken_links_found.append((str(rel_path), match.group(0), replacement))
    
    if content != original:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        fixes_made += 1
        print(f"✓ Fixed links in {rel_path}")

if broken_links_found:
    print(f"\n=== Broken Links Found and Fixed ===")
    for file, old_link, new_link in broken_links_found[:20]:  # Show first 20
        print(f"  {file}: {old_link} → {new_link}")
    if len(broken_links_found) > 20:
        print(f"  ... and {len(broken_links_found) - 20} more")
else:
    print("\n✓ No broken links found!")

print(f"\n✓ Updated {fixes_made} files")



