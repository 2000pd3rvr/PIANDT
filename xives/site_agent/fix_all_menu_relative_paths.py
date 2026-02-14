#!/usr/bin/env python3
"""
Fix all broken relative paths in menu links
Calculates correct relative paths based on file locations
"""
from pathlib import Path
import re

base_dir = Path(__file__).parent.parent

html_files = list(base_dir.rglob("*.html"))
html_files = [f for f in html_files if 'site_agent' not in str(f)]

valid_paths = {str(f.relative_to(base_dir)).replace('\\', '/') for f in html_files}
valid_paths.add('index.html')
valid_paths.add('in/in.html')
valid_paths.add('processing/processing.html')
valid_paths.add('out/out.html')

def calculate_relative_path(from_file, to_path):
    """Calculate correct relative path from from_file to to_path"""
    from_parts = from_file.relative_to(base_dir).parts[:-1]  # Remove filename
    to_parts = Path(to_path).relative_to(base_dir).parts
    
    # Find common prefix
    common_len = 0
    for i, (f, t) in enumerate(zip(from_parts, to_parts)):
        if f == t:
            common_len = i + 1
        else:
            break
    
    # Calculate ups
    ups = len(from_parts) - common_len
    up_path = '../' * ups
    
    # Calculate down path
    down_parts = to_parts[common_len:]
    down_path = '/'.join(down_parts) if down_parts else ''
    
    return up_path + down_path if down_path else up_path

print("Fixing broken menu links...\n")
fixes = 0
files_fixed = set()

for html_file in html_files:
    rel_path = str(html_file.relative_to(base_dir))
    file_dir = html_file.parent
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Find all href attributes in menu links
    # Pattern: href="..." in <a> tags with submenu-link or dropdown-link
    def fix_href(match):
        href = match.group(1)
        
        # Skip external links
        if href.startswith(('http://', 'https://', 'mailto:', '#', 'data:', 'javascript:')):
            return match.group(0)
        
        if not href or href.strip() == '':
            return match.group(0)
        
        # Resolve current path
        if href.startswith('/'):
            resolved = href[1:]
        else:
            resolved_file = (file_dir / href).resolve()
            try:
                resolved = str(resolved_file.relative_to(base_dir)).replace('\\', '/')
            except ValueError:
                return match.group(0)
        
        # Check if file exists
        target = base_dir / resolved
        if target.exists() or resolved in valid_paths:
            return match.group(0)  # Link is valid
        
        # Try to find the correct file
        # Extract filename from resolved path
        filename = Path(resolved).name
        parent_dir = Path(resolved).parent
        
        # Check if it's a valid file in a different location
        for valid_path in valid_paths:
            if valid_path.endswith(filename):
                # Found a file with same name, calculate correct relative path
                correct_rel = calculate_relative_path(html_file, valid_path)
                fixes += 1
                files_fixed.add(rel_path)
                print(f"  Fixed: {href} -> {correct_rel} in {rel_path}")
                return f'href="{correct_rel}"'
        
        return match.group(0)  # Couldn't fix, leave as is
    
    # Fix hrefs in <a> tags with menu classes
    # Match: <a ... href="..." ... class="...submenu-link..." ...>
    pattern = r'(<a[^>]*(?:submenu-link|dropdown-link)[^>]*href=)["\']([^"\']+)["\']'
    content = re.sub(pattern, lambda m: m.group(1) + '"' + fix_href(m).split('"')[1] + '"', content)
    
    if content != original:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Fixed {rel_path}")

print(f"\n✓ Fixed {fixes} broken links in {len(files_fixed)} files")



