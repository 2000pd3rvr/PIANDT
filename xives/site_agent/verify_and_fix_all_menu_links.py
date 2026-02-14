#!/usr/bin/env python3
"""
Comprehensive verification and fixing of all menu links
Ensures all menus are linked and each link is traceable in folder structure
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

print("=" * 60)
print("COMPREHENSIVE MENU LINK VERIFICATION AND FIXING")
print("=" * 60)
print(f"\nFound {len(valid_paths)} valid HTML files\n")

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

def find_matching_file(filename, from_file):
    """Find the correct file matching the filename in the folder structure"""
    # Try to find file by matching filename
    for valid_path in valid_paths:
        if valid_path.endswith(filename):
            # Check if it's in the right location based on context
            # For example, if looking for in_about_piandt.html, should be in in/about_piandt/
            if filename.startswith('in_') and 'in/' in valid_path:
                return valid_path
            elif filename.startswith('proc_') and 'processing/' in valid_path:
                return valid_path
            elif filename.startswith('out_') and 'out/' in valid_path:
                return valid_path
            # If no prefix match, return first match
            return valid_path
    return None

total_issues = 0
total_fixes = 0
files_fixed = set()

for html_file in html_files:
    rel_path = str(html_file.relative_to(base_dir))
    file_dir = html_file.parent
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    file_issues = []
    file_fixes = 0
    
    # Find all menu-related links (nav-link, dropdown-link, submenu-link)
    # Pattern: <a ... class="...nav-link..." ... href="..." ...>
    # or class="...dropdown-link..." or class="...submenu-link..."
    
    def fix_menu_link(match):
        nonlocal file_fixes, file_issues
        full_tag = match.group(0)
        href_match = re.search(r'href=["\']([^"\']*)["\']', full_tag)
        
        if not href_match:
            # No href attribute - this is an issue
            file_issues.append((rel_path, "Missing href attribute", full_tag[:100]))
            return full_tag
        
        href = href_match.group(1)
        quote_char = href_match.group(0)[5]  # Get the quote character used
        
        # Skip external links
        if href.startswith(('http://', 'https://', 'mailto:', '#', 'data:', 'javascript:')):
            return full_tag
        
        if not href or href.strip() == '':
            file_issues.append((rel_path, "Empty href", full_tag[:100]))
            return full_tag
        
        # Resolve the path
        if href.startswith('/'):
            resolved = href[1:]
        else:
            resolved_file = (file_dir / href).resolve()
            try:
                resolved = str(resolved_file.relative_to(base_dir)).replace('\\', '/')
            except ValueError:
                file_issues.append((rel_path, f"Path outside base_dir: {href}", full_tag[:100]))
                return full_tag
        
        # Check if file exists
        target = base_dir / resolved
        if target.exists() or resolved in valid_paths:
            # Link is valid
            return full_tag
        
        # Try to find the correct file
        filename = Path(resolved).name
        matching_file = find_matching_file(filename, html_file)
        
        if matching_file:
            correct_rel = calculate_relative_path(html_file, matching_file)
            file_fixes += 1
            files_fixed.add(rel_path)
            # Replace the href in the tag
            new_tag = re.sub(
                r'href=["\'][^"\']*["\']',
                f'href={quote_char}{correct_rel}{quote_char}',
                full_tag
            )
            print(f"  Fixed: {href} -> {correct_rel} in {rel_path}")
            return new_tag
        else:
            file_issues.append((rel_path, f"Broken link: {href} -> {resolved} (file not found)", full_tag[:100]))
            return full_tag
    
    # Find all <a> tags with menu classes
    # Match the entire tag including href
    pattern = r'<a[^>]*(?:nav-link|dropdown-link|submenu-link)[^>]*>'
    content = re.sub(pattern, fix_menu_link, content)
    
    # Also check for <a> tags without href that should have one
    # Pattern: <a ... class="...menu-class..." ...> (without href)
    no_href_pattern = r'<a((?![^>]*href=)[^>]*(?:nav-link|dropdown-link|submenu-link)[^>]*)>'
    def add_missing_href(match):
        nonlocal file_issues
        attrs = match.group(1)
        # Try to determine what the href should be from context
        # For now, just log it
        file_issues.append((rel_path, "Menu link without href attribute", match.group(0)[:100]))
        return match.group(0)
    
    content = re.sub(no_href_pattern, add_missing_href, content)
    
    if content != original:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        total_fixes += file_fixes
        if file_fixes > 0:
            print(f"✓ Fixed {file_fixes} links in {rel_path}")
    
    if file_issues:
        total_issues += len(file_issues)
        for file, issue, tag in file_issues:
            print(f"  ⚠ {file}: {issue}")

print("\n" + "=" * 60)
print("VERIFICATION SUMMARY")
print("=" * 60)
print(f"✓ Fixed {total_fixes} broken links in {len(files_fixed)} files")
if total_issues > 0:
    print(f"⚠ Found {total_issues} remaining issues (see above)")
else:
    print("✓ All menu links are properly connected and traceable!")

# Now verify all menu items have links
print("\n" + "=" * 60)
print("VERIFYING ALL MENU ITEMS HAVE LINKS")
print("=" * 60)

menu_items_without_links = []

for html_file in html_files:
    rel_path = str(html_file.relative_to(base_dir))
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all <li> elements that contain menu links
    # Pattern: <li>...<a class="...menu-class...">...</a>...</li>
    li_pattern = r'<li[^>]*>.*?<a[^>]*(?:nav-link|dropdown-link|submenu-link)[^>]*>'
    li_matches = re.finditer(li_pattern, content, re.DOTALL)
    
    for match in li_matches:
        li_content = match.group(0)
        # Check if the <a> tag has an href
        if 'href=' not in li_content:
            line_num = content[:match.start()].count('\n') + 1
            menu_items_without_links.append((rel_path, line_num, li_content[:150]))

if menu_items_without_links:
    print(f"\n⚠ Found {len(menu_items_without_links)} menu items without href attributes:")
    for file, line, content in menu_items_without_links[:10]:  # Show first 10
        print(f"  {file}:{line}")
        print(f"    {content}...")
    if len(menu_items_without_links) > 10:
        print(f"  ... and {len(menu_items_without_links) - 10} more")
else:
    print("✓ All menu items have href attributes!")

print("\n" + "=" * 60)
print("FINAL VERIFICATION: ALL LINKS TRACEABLE")
print("=" * 60)

broken_links = []
for html_file in html_files:
    rel_path = str(html_file.relative_to(base_dir))
    file_dir = html_file.parent
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all href attributes in menu links
    pattern = r'<a[^>]*(?:nav-link|dropdown-link|submenu-link)[^>]*href=["\']([^"\']+)["\']'
    matches = re.finditer(pattern, content)
    
    for match in matches:
        href = match.group(1)
        
        # Skip external
        if href.startswith(('http://', 'https://', 'mailto:', '#', 'data:', 'javascript:')):
            continue
        
        if not href or href.strip() == '':
            broken_links.append((rel_path, "Empty href", href))
            continue
        
        # Resolve path
        if href.startswith('/'):
            resolved = href[1:]
        else:
            resolved_file = (file_dir / href).resolve()
            try:
                resolved = str(resolved_file.relative_to(base_dir)).replace('\\', '/')
            except ValueError:
                broken_links.append((rel_path, "Path outside base_dir", href))
                continue
        
        # Check if file exists
        target = base_dir / resolved
        if not target.exists() and resolved not in valid_paths:
            broken_links.append((rel_path, f"File not found: {resolved}", href))

if broken_links:
    print(f"\n⚠ Found {len(broken_links)} broken menu links:")
    for file, issue, href in broken_links[:20]:  # Show first 20
        print(f"  {file}: {issue} (href='{href}')")
    if len(broken_links) > 20:
        print(f"  ... and {len(broken_links) - 20} more")
else:
    print("✓ All menu links are traceable to actual files in the folder structure!")

print("\n" + "=" * 60)
print("VERIFICATION COMPLETE")
print("=" * 60)



