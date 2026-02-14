#!/usr/bin/env python3
"""
Fix all href attributes in HTML files to use consistent relative paths.
Option 1: Relative paths from current file (recommended)
"""

from pathlib import Path
import re
import os

def calculate_relative_path(from_file, to_file, base_dir):
    """Calculate relative path from from_file to to_file"""
    from_path = Path(from_file).resolve()
    to_path = (base_dir / to_file).resolve()
    
    try:
        # Calculate relative path
        rel_path = os.path.relpath(to_path, from_path.parent)
        # Normalize the path (handle .. and .)
        rel_path = Path(rel_path).as_posix()
        # Ensure it doesn't start with .. if it's in the same directory
        if rel_path.startswith('../') and to_path.parent == from_path.parent:
            rel_path = Path(to_file).name
        return rel_path
    except ValueError:
        # If paths are on different drives (Windows), return as-is
        return to_file

def find_target_file(href, file_dir, base_dir):
    """Find the actual target file for a given href"""
    # Handle absolute paths from root (starting with /)
    if href.startswith('/'):
        href = href[1:]
    
    # Resolve the target file path
    if href.startswith('../') or href.startswith('./'):
        # Already a relative path - resolve it
        target_path = (file_dir / href).resolve()
    elif '/' in href:
        # Absolute path from root
        target_path = (base_dir / href).resolve()
    else:
        # Filename only - same directory
        target_path = (file_dir / href).resolve()
    
    # Check if target file exists
    if target_path.exists() and target_path.is_file():
        return target_path
    
    # Try to find the file by name
    if href.endswith('.html'):
        filename = Path(href).name
        found = list(base_dir.rglob(filename))
        if found:
            return found[0].resolve()
    
    return None

def fix_hrefs_in_file(file_path, base_dir):
    """Fix all href attributes in a single HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        file_dir = file_path.parent if isinstance(file_path, Path) else Path(file_path).parent
        file_relative = file_path.relative_to(base_dir) if file_path.is_absolute() else file_path
        
        # Find all href attributes
        def replace_href(match):
            quote = match.group(1)  # " or '
            href = match.group(2)
            
            # Skip external links, anchors, data URIs
            if (href.startswith('http://') or href.startswith('https://') or 
                href.startswith('#') or href.startswith('data:') or
                href.startswith('mailto:') or href.startswith('tel:') or
                href.startswith('javascript:')):
                return match.group(0)  # Keep as is
            
            # Only process HTML files and directory references
            is_html = href.endswith('.html')
            is_directory = href.endswith('/') or (not '.' in Path(href).name and '/' in href)
            
            if not is_html and not is_directory:
                # Check if it's a relative path to a resource file
                if not href.startswith('../') and not href.startswith('./') and '/' not in href:
                    # Likely a resource file in same directory (styles.css, script.js, etc.)
                    return match.group(0)  # Keep as is
            
            # Find the target file
            target_path = find_target_file(href, file_dir, base_dir)
            
            if not target_path:
                # File not found - keep original
                return match.group(0)
            
            # Calculate correct relative path
            try:
                correct_path = os.path.relpath(target_path, file_dir)
                correct_path = Path(correct_path).as_posix()
                
                # Normalize: if same directory, use just filename
                if correct_path.startswith('../') and target_path.parent == file_dir:
                    correct_path = target_path.name
                elif correct_path == '.':
                    correct_path = target_path.name
                
                return f'href={quote}{correct_path}{quote}'
            except ValueError:
                # Different drives (Windows) - keep original
                return match.group(0)
        
        # Replace all href attributes
        pattern = r'href=(["\'])([^"\']+)\1'
        content = re.sub(pattern, replace_href, content)
        
        return content, content != original_content
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        import traceback
        traceback.print_exc()
        return None, False

def main():
    base_dir = Path('.').resolve()
    
    # Get all HTML files
    html_files = list(base_dir.rglob('*.html'))
    
    # Exclude site_agent directory
    html_files = [f for f in html_files if 'site_agent' not in str(f)]
    
    print(f"Found {len(html_files)} HTML files to process")
    print("=" * 70)
    
    fixed_count = 0
    error_count = 0
    
    for html_file in html_files:
        try:
            new_content, changed = fix_hrefs_in_file(html_file, base_dir)
            
            if changed:
                # Write the fixed content
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                fixed_count += 1
                print(f"✓ Fixed: {html_file.relative_to(base_dir)}")
        except Exception as e:
            error_count += 1
            print(f"✗ Error: {html_file.relative_to(base_dir)} - {e}")
    
    print("=" * 70)
    print(f"\n✓ Fixed {fixed_count} files")
    if error_count > 0:
        print(f"✗ {error_count} errors")
    print("\nDone!")

if __name__ == '__main__':
    main()



