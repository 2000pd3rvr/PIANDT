#!/usr/bin/env python3
"""
Check and update page descriptions to match pages.html
"""
import re
from pathlib import Path
from html import unescape

base_dir = Path(__file__).parent.parent

# Read pages.html to get all page descriptions
pages_html = base_dir / 'site_agent' / 'pages.html'
with open(pages_html, 'r', encoding='utf-8') as f:
    pages_content = f.read()

# Extract URL and description pairs
url_pattern = r'<td class="url-col">(.*?)</td>\s*<td class="desc-col">(.*?)</td>'
matches = re.findall(url_pattern, pages_content, re.DOTALL)

# Create mapping of URL to description
url_to_description = {}
for url, desc in matches:
    url = unescape(url.strip())
    desc = unescape(desc.strip())
    # Clean up HTML entities and extra whitespace
    desc = re.sub(r'\s+', ' ', desc)
    desc = desc.replace('&amp;', '&').replace('&quot;', '"').replace('&#x27;', "'")
    url_to_description[url] = desc

print(f"Found {len(url_to_description)} page descriptions in pages.html\n")

# Now check each HTML file
html_files = list(base_dir.rglob("*.html"))
html_files = [f for f in html_files if 'site_agent' not in str(f)]

mismatches = []

for html_file in html_files:
    rel_path = html_file.relative_to(base_dir)
    url_key = str(rel_path).replace('\\', '/')
    
    # Skip if not in our mapping
    if url_key not in url_to_description:
        continue
    
    expected_desc = url_to_description[url_key]
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract body text from HTML
    # Look for content-text div or main content
    body_pattern = r'<div class="content-text">(.*?)</div>'
    body_match = re.search(body_pattern, content, re.DOTALL)
    
    if not body_match:
        # Try alternative patterns
        body_pattern = r'<main>(.*?)</main>'
        body_match = re.search(body_pattern, content, re.DOTALL)
    
    if body_match:
        body_text = body_match.group(1)
        # Remove HTML tags
        body_text = re.sub(r'<[^>]+>', ' ', body_text)
        # Clean up whitespace
        body_text = re.sub(r'\s+', ' ', body_text).strip()
        # Get first 500 chars for comparison
        body_text_short = body_text[:500]
        expected_short = expected_desc[:500]
        
        # Compare (allowing for some variation)
        if expected_short.lower() not in body_text_short.lower() and body_text_short.lower() not in expected_short.lower():
            mismatches.append({
                'file': url_key,
                'expected': expected_desc[:200],
                'actual': body_text[:200]
            })

if mismatches:
    print(f"Found {len(mismatches)} pages with description mismatches:\n")
    for m in mismatches[:10]:  # Show first 10
        print(f"File: {m['file']}")
        print(f"Expected start: {m['expected']}...")
        print(f"Actual start: {m['actual']}...")
        print()
else:
    print("✓ All page descriptions match pages.html!")



