#!/usr/bin/env python3
"""
Check and validate all links in HTML files
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

# Also add index.html, in.html, processing.html, out.html
valid_urls.add('index.html')
valid_urls.add('in.html')
valid_urls.add('processing.html')
valid_urls.add('out.html')

print(f"Found {len(valid_urls)} valid URLs")
print("\nValid URLs:")
for url in sorted(valid_urls):
    print(f"  {url}")

# Now check all HTML files for broken links
html_files = list(base_dir.rglob("*.html"))
html_files = [f for f in html_files if 'site_agent' not in str(f)]

broken_links = []
for html_file in html_files:
    rel_path = html_file.relative_to(base_dir)
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all href links
    href_pattern = r'href=["\']([^"\']+)["\']'
    links = re.findall(href_pattern, content)
    
    for link in links:
        # Skip external links, anchors, and javascript
        if link.startswith('http://') or link.startswith('https://') or link.startswith('#') or link.startswith('javascript:') or link.startswith('mailto:'):
            continue
        
        # Skip if it's a relative path that might be valid
        # Need to resolve relative to current file
        if not link.startswith('/'):
            # Relative path - resolve from current file's directory
            current_dir = html_file.parent
            target_path = (current_dir / link).resolve()
            try:
                target_rel = target_path.relative_to(base_dir)
                if str(target_rel) not in valid_urls and not target_path.exists():
                    broken_links.append((str(rel_path), link, "BROKEN"))
            except ValueError:
                # Path outside base directory
                pass
        else:
            # Absolute path from root
            if link.lstrip('/') not in valid_urls:
                broken_links.append((str(rel_path), link, "POTENTIALLY BROKEN"))

if broken_links:
    print(f"\n\nFound {len(broken_links)} potentially broken links:")
    for file, link, status in broken_links:
        print(f"  {file}: {link} - {status}")
else:
    print("\n\nNo broken links found!")



