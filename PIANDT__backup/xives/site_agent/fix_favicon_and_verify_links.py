#!/usr/bin/env python3
"""
1. Add favicon to all HTML files
2. Verify all child menu links are properly connected
"""
from pathlib import Path
import re

base_dir = Path(__file__).parent.parent

favicon_link = '<link rel="icon" href="data:image/svg+xml,<svg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 100 100\'><text y=\'.9em\' font-size=\'90\'>📊</text></svg>">'

html_files = list(base_dir.rglob("*.html"))
html_files = [f for f in html_files if 'site_agent' not in str(f)]

print("Adding favicon to all HTML files...")
favicon_fixed = 0

for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Check if favicon already exists
    if 'favicon' in content.lower() or 'rel="icon"' in content or "rel='icon'" in content:
        continue
    
    # Find the </head> tag to insert before
    if '</head>' in content:
        # Insert before </head>
        content = content.replace('</head>', f'    {favicon_link}\n</head>', 1)
        favicon_fixed += 1
        print(f"  Added favicon to {html_file.relative_to(base_dir)}")
    
    if content != original:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)

print(f"\n✓ Added favicon to {favicon_fixed} files\n")

# Now verify all menu links have proper href attributes
print("Verifying all child menu links...")

valid_paths = {str(f.relative_to(base_dir)).replace('\\', '/') for f in html_files}
valid_paths.add('index.html')
valid_paths.add('in/in.html')
valid_paths.add('processing/processing.html')
valid_paths.add('out/out.html')

issues = []

for html_file in html_files:
    rel_path = str(html_file.relative_to(base_dir))
    file_dir = html_file.parent
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all <a> tags with submenu-link or dropdown-link classes
    # Better pattern: match the entire <a> tag, including multi-line
    # First, normalize by removing newlines within tags
    normalized = re.sub(r'<a([^>]*)>', lambda m: '<a' + m.group(1).replace('\n', ' ') + '>', content)
    
    # Now find all <a> tags with menu classes
    pattern = r'<a([^>]*(?:submenu-link|dropdown-link)[^>]*)>'
    matches = re.finditer(pattern, normalized)
    
    for match in matches:
        attrs = match.group(1)
        
        # Extract href attribute
        href_match = re.search(r'href=["\']([^"\']*)["\']', attrs)
        if not href_match:
            # No href found - this is a real issue
            line_num = content[:match.start()].count('\n') + 1
            issues.append((rel_path, line_num, "Missing href attribute", match.group(0)[:100]))
            continue
        
        href = href_match.group(1)
        
        # Skip anchors and external links
        if href.startswith(('#', 'http://', 'https://', 'mailto:', 'data:', 'javascript:')):
            continue
        
        if not href or href.strip() == '':
            line_num = content[:match.start()].count('\n') + 1
            issues.append((rel_path, line_num, "Empty href", match.group(0)[:100]))
            continue
        
        # Verify the link resolves to a valid file
        if href.startswith('/'):
            resolved = href[1:]
        else:
            resolved_file = (file_dir / href).resolve()
            try:
                resolved = str(resolved_file.relative_to(base_dir)).replace('\\', '/')
            except ValueError:
                resolved = None
        
        if resolved:
            target = base_dir / resolved
            if not target.exists() and resolved not in valid_paths:
                line_num = content[:match.start()].count('\n') + 1
                issues.append((rel_path, line_num, f"Broken link: {href} -> {resolved}", match.group(0)[:100]))

if issues:
    print(f"\n⚠ Found {len(issues)} menu link issues:")
    for file, line, issue, link in issues[:20]:  # Show first 20
        print(f"  {file}:{line} - {issue}")
    if len(issues) > 20:
        print(f"  ... and {len(issues) - 20} more issues")
else:
    print("✓ All child menu links are properly connected!")

print(f"\n✓ Complete! Fixed favicon in {favicon_fixed} files")



