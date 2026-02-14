#!/usr/bin/env python3
"""
Comprehensive link verification and fixing
Checks ALL links (href and src) in ALL HTML files and fixes broken ones
"""
import re
from pathlib import Path

base_dir = Path(__file__).parent.parent

# Get all valid HTML files
html_files = list(base_dir.rglob("*.html"))
html_files = [f for f in html_files if 'site_agent' not in str(f)]
valid_paths = {str(f.relative_to(base_dir)).replace('\\', '/') for f in html_files}
valid_paths.add('index.html')
valid_paths.add('in/in.html')
valid_paths.add('processing/processing.html')
valid_paths.add('out/out.html')

print(f"Found {len(valid_paths)} valid HTML files")
print("\nVerifying and fixing all links...\n")

def resolve_path(from_file, href):
    """Resolve a relative or absolute path to an absolute path relative to base_dir"""
    file_dir = from_file.parent
    
    if href.startswith('/'):
        # Absolute from root
        return href[1:]
    elif href.startswith('../') or href.startswith('./') or not '/' in href:
        # Relative path
        resolved = (file_dir / href).resolve()
        try:
            return str(resolved.relative_to(base_dir)).replace('\\', '/')
        except ValueError:
            return None
    else:
        # Relative from current directory
        resolved = (file_dir / href).resolve()
        try:
            return str(resolved.relative_to(base_dir)).replace('\\', '/')
        except ValueError:
            return None

def calculate_relative_path(from_file, to_path):
    """Calculate relative path from from_file to to_path"""
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

fixes_made = 0
files_fixed = set()

for html_file in html_files:
    rel_path = str(html_file.relative_to(base_dir))
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Find all href and src attributes
    for attr in ['href', 'src']:
        pattern = rf'{attr}=["\']([^"\']+)["\']'
        matches = list(re.finditer(pattern, content))
        
        for match in reversed(matches):  # Reverse to maintain positions
            href = match.group(1)
            full_match = match.group(0)
            
            # Skip external links
            if href.startswith(('http://', 'https://', 'mailto:', '#', 'data:', 'javascript:')):
                continue
            
            if not href or href.strip() == '':
                continue
            
            # Resolve the path
            resolved_path = resolve_path(html_file, href)
            
            if resolved_path is None:
                continue
            
            # Check if file exists
            target_file = base_dir / resolved_path
            if not target_file.exists() or resolved_path not in valid_paths:
                # Try to find correct file
                # Common fixes:
                
                # Fix 1: in/units/in.html -> in/in.html
                if resolved_path == 'in/units/in.html' or 'units/in.html' in resolved_path:
                    correct_path = 'in/in.html'
                    new_href = calculate_relative_path(html_file, correct_path)
                    content = content[:match.start()] + f'{attr}="{new_href}"' + content[match.end():]
                    fixes_made += 1
                    files_fixed.add(rel_path)
                    print(f"  Fixed {attr}: {href} -> {new_href} in {rel_path}")
                    continue
                
                # Fix 2: processing/units/processing.html -> processing/processing.html
                if resolved_path == 'processing/units/processing.html' or 'units/processing.html' in resolved_path:
                    correct_path = 'processing/processing.html'
                    new_href = calculate_relative_path(html_file, correct_path)
                    content = content[:match.start()] + f'{attr}="{new_href}"' + content[match.end():]
                    fixes_made += 1
                    files_fixed.add(rel_path)
                    print(f"  Fixed {attr}: {href} -> {new_href} in {rel_path}")
                    continue
                
                # Fix 3: out/units/out.html -> out/out.html
                if resolved_path == 'out/units/out.html' or 'units/out.html' in resolved_path:
                    correct_path = 'out/out.html'
                    new_href = calculate_relative_path(html_file, correct_path)
                    content = content[:match.start()] + f'{attr}="{new_href}"' + content[match.end():]
                    fixes_made += 1
                    files_fixed.add(rel_path)
                    print(f"  Fixed {attr}: {href} -> {new_href} in {rel_path}")
                    continue
                
                # Fix 4: Wrong triad prefix in filename
                filename = Path(resolved_path).name
                parent_dir = Path(resolved_path).parent
                
                if 'units' in str(parent_dir) or 'about_piandt' in str(parent_dir):
                    # Determine correct prefix
                    if 'in/' in str(parent_dir) or str(parent_dir).startswith('in'):
                        prefix = 'in_'
                    elif 'processing/' in str(parent_dir) or str(parent_dir).startswith('processing'):
                        prefix = 'proc_'
                    elif 'out/' in str(parent_dir) or str(parent_dir).startswith('out'):
                        prefix = 'out_'
                    else:
                        prefix = None
                    
                    if prefix:
                        # Try to fix filename
                        if filename.startswith(('in_', 'proc_', 'out_')):
                            parts = filename.split('_', 1)
                            if len(parts) > 1:
                                correct_filename = prefix + parts[1]
                            else:
                                correct_filename = prefix + filename
                        else:
                            correct_filename = prefix + filename
                        
                        correct_path = str(parent_dir / correct_filename).replace('\\', '/')
                        if correct_path in valid_paths:
                            new_href = calculate_relative_path(html_file, correct_path)
                            content = content[:match.start()] + f'{attr}="{new_href}"' + content[match.end():]
                            fixes_made += 1
                            files_fixed.add(rel_path)
                            print(f"  Fixed {attr}: {href} -> {new_href} in {rel_path}")
                            continue
    
    if content != original:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Fixed links in {rel_path}")

print(f"\n✓ Fixed {fixes_made} broken links in {len(files_fixed)} files")



