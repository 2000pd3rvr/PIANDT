#!/usr/bin/env python3
"""
Comprehensively fix all menu link paths
Calculates correct relative paths for all menu links
"""
from pathlib import Path
import re

base_dir = Path(__file__).parent.parent

# Get all valid HTML files
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
    # to_path is already relative to base_dir, so just split it
    to_parts = Path(to_path).parts
    
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

print("Fixing all menu link paths...\n")
total_fixes = 0
files_fixed = set()

for html_file in html_files:
    rel_path = str(html_file.relative_to(base_dir))
    file_dir = html_file.parent
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    file_fixes = [0]  # Use list to allow modification in nested function
    
    # Find all href attributes in <a> tags
    def fix_link(match):
        href = match.group(2)  # The actual href value
        quote = match.group(1)  # The quote character
        
        # Skip external links
        if href.startswith(('http://', 'https://', 'mailto:', '#', 'data:', 'javascript:')):
            return match.group(0)
        
        if not href or href.strip() == '':
            return match.group(0)
        
        # Resolve the path
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
        
        # Try to find correct file by matching filename
        filename = Path(resolved).name
        
        # Find matching file in valid_paths
        matching_path = None
        for valid_path in valid_paths:
            if valid_path.endswith(filename):
                # Check if it's the right file (same directory structure)
                # For example: in/about_piandt/in_about_piandt.html
                if filename.startswith('in_') and 'in/' in valid_path:
                    matching_path = valid_path
                    break
                elif filename.startswith('proc_') and 'processing/' in valid_path:
                    matching_path = valid_path
                    break
                elif filename.startswith('out_') and 'out/' in valid_path:
                    matching_path = valid_path
                    break
        
        if matching_path:
            correct_rel = calculate_relative_path(html_file, matching_path)
            file_fixes[0] += 1
            files_fixed.add(rel_path)
            print(f"  Fixed: {href} -> {correct_rel} in {rel_path}")
            return f'href={quote}{correct_rel}{quote}'
        
        return match.group(0)
    
    # Fix all href attributes (not just menu links, but prioritize menu links)
    # Pattern: href="..." or href='...'
    pattern = r'href=(["\'])([^"\']+)\1'
    content = re.sub(pattern, fix_link, content)
    
    if content != original:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        total_fixes += file_fixes[0]
        if file_fixes[0] > 0:
            print(f"✓ Updated {rel_path} ({file_fixes[0]} fixes)")

print(f"\n✓ Fixed {total_fixes} broken links in {len(files_fixed)} files")
