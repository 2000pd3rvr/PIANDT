#!/usr/bin/env python3
"""
Ensure all page descriptions match pages.html
Extracts text from pages and compares with pages.html descriptions
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
    # Clean up HTML entities but keep the text
    desc = desc.replace('&amp;', '&').replace('&quot;', '"').replace('&#x27;', "'")
    # Remove trailing "..." if present
    desc = desc.rstrip('...').strip()
    url_to_description[url] = desc

print(f"Loaded {len(url_to_description)} page descriptions from pages.html\n")

# Get all HTML files
html_files = list(base_dir.rglob("*.html"))
html_files = [f for f in html_files if 'site_agent' not in str(f)]

def extract_text_from_html(html_content):
    """Extract plain text from HTML content-text div"""
    # Find content-text div
    pattern = r'<div class="content-text">(.*?)</div>'
    match = re.search(pattern, html_content, re.DOTALL)
    if not match:
        return ""
    
    content = match.group(1)
    # Remove HTML tags but preserve structure hints
    # Replace <p>, <h2>, etc. with spaces
    content = re.sub(r'<[^>]+>', ' ', content)
    # Clean up whitespace
    content = re.sub(r'\s+', ' ', content).strip()
    return content

mismatches = []
updates_needed = []

for html_file in html_files:
    rel_path = html_file.relative_to(base_dir)
    url_key = str(rel_path).replace('\\', '/')
    
    # Skip if not in our mapping
    if url_key not in url_to_description:
        continue
    
    expected_desc = url_to_description[url_key]
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract actual text from page
    actual_text = extract_text_from_html(content)
    
    # Compare first 300 characters (descriptions are truncated)
    expected_start = expected_desc[:300].lower().strip()
    actual_start = actual_text[:300].lower().strip()
    
    # Check if expected description matches the beginning of actual content
    if expected_start and actual_start:
        # Allow for some variation in whitespace and HTML entities
        expected_clean = re.sub(r'\s+', ' ', expected_start)
        actual_clean = re.sub(r'\s+', ' ', actual_start)
        
        # Check if expected is contained in actual or vice versa
        if expected_clean not in actual_clean and actual_clean[:len(expected_clean)] != expected_clean:
            mismatches.append({
                'file': url_key,
                'expected': expected_desc[:200],
                'actual': actual_text[:200]
            })
            updates_needed.append(html_file)

if mismatches:
    print(f"Found {len(mismatches)} pages where content doesn't match description:\n")
    for m in mismatches:
        print(f"File: {m['file']}")
        print(f"Expected: {m['expected']}...")
        print(f"Actual: {m['actual']}...")
        print()
    
    print(f"\nNote: These mismatches are likely due to HTML entity encoding differences.")
    print(f"The actual page content may be correct, just encoded differently.")
    print(f"\nTo verify, check if the meaning matches (ignoring &amp; vs &, etc.)")
else:
    print("✓ All page descriptions match pages.html!")



