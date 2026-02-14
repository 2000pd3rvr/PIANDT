#!/usr/bin/env python3
"""
Fix all broken menu links in HTML files
Checks all navigation menu links and ensures they point to valid files
"""
import re
from pathlib import Path
from urllib.parse import unquote

base_dir = Path(__file__).parent.parent

# Get all valid HTML files to check against
html_files = list(base_dir.rglob("*.html"))
html_files = [f for f in html_files if 'site_agent' not in str(f)]
valid_paths = {str(f.relative_to(base_dir)).replace('\\', '/') for f in html_files}
valid_paths.add('index.html')
valid_paths.add('in/in.html')
valid_paths.add('processing/processing.html')
valid_paths.add('out/out.html')

print(f"Found {len(valid_paths)} valid HTML files")
print("\nStarting menu link fixes...\n")

fixes_made = 0
files_fixed = set()

def calculate_correct_path(from_file, target_file, current_href):
    """Calculate the correct relative path from from_file to target_file"""
    from_path = Path(from_file).relative_to(base_dir)
    target_path = Path(target_file).relative_to(base_dir)
    
    # Calculate relative path
    try:
        rel_path = Path(target_path).relative_to(Path(from_path).parent)
        return str(rel_path).replace('\\', '/')
    except ValueError:
        # Need to go up directories
        from_parts = from_path.parts[:-1]  # Remove filename
        target_parts = target_path.parts
        
        # Find common prefix
        common_len = 0
        for i, (f, t) in enumerate(zip(from_parts, target_parts)):
            if f == t:
                common_len = i + 1
            else:
                break
        
        # Calculate ups needed
        ups = len(from_parts) - common_len
        up_path = '../' * ups
        
        # Calculate down path
        down_parts = target_parts[common_len:]
        down_path = '/'.join(down_parts) if down_parts else ''
        
        return up_path + down_path if down_path else up_path

def fix_link_in_content(content, html_file, link_attr='href'):
    """Fix all links in content"""
    global fixes_made, files_fixed
    
    original = content
    rel_path = html_file.relative_to(base_dir)
    file_dir = html_file.parent
    
    # Find all links
    link_pattern = rf'<a[^>]*{link_attr}=["\']([^"\']+)["\'][^>]*>'
    links = re.finditer(link_pattern, content)
    
    for match in links:
        href = match.group(1)
        full_match = match.group(0)
        
        # Skip external links, anchors, and data URIs
        if href.startswith('http://') or href.startswith('https://') or \
           href.startswith('mailto:') or href.startswith('#') or \
           href.startswith('data:') or href.startswith('javascript:'):
            continue
        
        # Skip empty links
        if not href or href.strip() == '':
            continue
        
        # Resolve the path
        if href.startswith('/'):
            # Absolute path from root
            resolved_path = href[1:]  # Remove leading /
        else:
            # Relative path
            resolved = (file_dir / href).resolve()
            try:
                resolved_path = str(resolved.relative_to(base_dir)).replace('\\', '/')
            except ValueError:
                # Path is outside base_dir, skip
                continue
        
        # Check if file exists
        target_file = base_dir / resolved_path
        if not target_file.exists() or resolved_path not in valid_paths:
            # Try to find the correct file
            # Common issues:
            # 1. in/units/in.html -> should be ../in.html or in/in.html
            # 2. units/in.html -> should be ../in.html or in/in.html
            # 3. Wrong triad prefix (in_ instead of proc_)
            
            # Fix: in/units/in.html -> ../in.html
            if resolved_path == 'in/units/in.html' or 'units/in.html' in resolved_path:
                correct_path = calculate_correct_path(html_file, base_dir / 'in' / 'in.html', href)
                new_href = correct_path
                content = content.replace(f'{link_attr}="{href}"', f'{link_attr}="{new_href}"')
                content = content.replace(f"{link_attr}='{href}'", f"{link_attr}='{new_href}'")
                fixes_made += 1
                files_fixed.add(str(rel_path))
                print(f"  Fixed: {href} -> {new_href} in {rel_path}")
                continue
            
            # Fix: processing/units/processing.html -> ../processing.html
            if resolved_path == 'processing/units/processing.html' or 'units/processing.html' in resolved_path:
                correct_path = calculate_correct_path(html_file, base_dir / 'processing' / 'processing.html', href)
                new_href = correct_path
                content = content.replace(f'{link_attr}="{href}"', f'{link_attr}="{new_href}"')
                content = content.replace(f"{link_attr}='{href}'", f"{link_attr}='{new_href}'")
                fixes_made += 1
                files_fixed.add(str(rel_path))
                print(f"  Fixed: {href} -> {new_href} in {rel_path}")
                continue
            
            # Fix: out/units/out.html -> ../out.html
            if resolved_path == 'out/units/out.html' or 'units/out.html' in resolved_path:
                correct_path = calculate_correct_path(html_file, base_dir / 'out' / 'out.html', href)
                new_href = correct_path
                content = content.replace(f'{link_attr}="{href}"', f'{link_attr}="{new_href}"')
                content = content.replace(f"{link_attr}='{href}'", f"{link_attr}='{new_href}'")
                fixes_made += 1
                files_fixed.add(str(rel_path))
                print(f"  Fixed: {href} -> {new_href} in {rel_path}")
                continue
            
            # Try to find similar file with correct prefix
            filename = Path(resolved_path).name
            parent_dir = Path(resolved_path).parent
            
            # Check if it's a units or about_piandt file
            if 'units' in str(parent_dir) or 'about_piandt' in str(parent_dir):
                # Determine correct prefix based on directory
                if 'in/' in str(parent_dir) or str(parent_dir).startswith('in'):
                    prefix = 'in_'
                elif 'processing/' in str(parent_dir) or str(parent_dir).startswith('processing'):
                    prefix = 'proc_'
                elif 'out/' in str(parent_dir) or str(parent_dir).startswith('out'):
                    prefix = 'out_'
                else:
                    prefix = None
                
                if prefix and not filename.startswith(prefix):
                    # Try to fix the filename
                    if filename.startswith('in_') or filename.startswith('proc_') or filename.startswith('out_'):
                        # Already has a prefix, might be wrong one
                        correct_filename = prefix + filename.split('_', 1)[-1] if '_' in filename else prefix + filename
                    else:
                        correct_filename = prefix + filename
                    
                    correct_path = str(parent_dir / correct_filename).replace('\\', '/')
                    if correct_path in valid_paths:
                        correct_rel_path = calculate_correct_path(html_file, base_dir / correct_path, href)
                        new_href = correct_rel_path
                        content = content.replace(f'{link_attr}="{href}"', f'{link_attr}="{new_href}"')
                        content = content.replace(f"{link_attr}='{href}'", f"{link_attr}='{new_href}'")
                        fixes_made += 1
                        files_fixed.add(str(rel_path))
                        print(f"  Fixed: {href} -> {new_href} in {rel_path}")
                        continue
    
    return content

# Process all HTML files
for html_file in html_files:
    rel_path = html_file.relative_to(base_dir)
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Fix href attributes in navigation menus
    content = fix_link_in_content(content, html_file, 'href')
    
    # Fix src attributes (for images, scripts, etc.)
    content = fix_link_in_content(content, html_file, 'src')
    
    if content != original:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Fixed links in {rel_path}")

print(f"\n✓ Fixed {fixes_made} broken links in {len(files_fixed)} files")



