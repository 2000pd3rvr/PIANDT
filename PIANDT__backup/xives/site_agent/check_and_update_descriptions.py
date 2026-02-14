#!/usr/bin/env python3
"""
Check and update page descriptions from pages.html
Ensures both meta description and content match pages.html
"""

import re
from pathlib import Path
from html import unescape

base_dir = Path(__file__).parent.parent
pages_html = base_dir / 'site_agent' / 'pages.html'

# Read pages.html
with open(pages_html, 'r', encoding='utf-8') as f:
    pages_content = f.read()

# Extract URL and description pairs
url_pattern = r'<td class="url-col">(.*?)</td>\s*<td class="desc-col">(.*?)</td>'
matches = re.findall(url_pattern, pages_content, re.DOTALL)

# Create mapping
url_to_description = {}
for url, desc in matches:
    url = unescape(url.strip())
    desc = unescape(desc.strip())
    desc = desc.replace('&amp;', '&').replace('&quot;', '"').replace('&#x27;', "'")
    desc = re.sub(r'\s+', ' ', desc).strip()
    url_to_description[url] = desc

print(f"Loaded {len(url_to_description)} descriptions from pages.html\n")

# Get HTML files from batch 1
batch1_files = [
    'in/about_piandt/in_about_piandt.html',
    'in/about_piandt/in_charitable_purposes.html',
    'in/about_piandt/in_governance.html',
    'in/about_piandt/in_mission_vision.html',
    'in/about_piandt/in_our_approach.html',
    'in/about_piandt/in_trustees.html',
    'in/in.html',
    'in/miu/in_miu.html',
    'in/miu/in_miu_products.html',
    'in/miu/in_miu_services.html',
]

for file_path_str in batch1_files:
    file_path = base_dir / file_path_str
    if not file_path.exists():
        continue
    
    url_key = file_path_str
    expected_desc = url_to_description.get(url_key, '')
    
    if not expected_desc:
        print(f"⚠️  No description in pages.html for: {url_key}")
        continue
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check meta description
    meta_desc_pattern = r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']'
    meta_match = re.search(meta_desc_pattern, content, re.IGNORECASE)
    
    # Extract first 160 chars for meta description
    meta_desc = expected_desc[:160] + ('...' if len(expected_desc) > 160 else '')
    
    if meta_match:
        if meta_match.group(1) != meta_desc:
            # Update meta description
            content = re.sub(meta_desc_pattern, f'<meta name="description" content="{re.escape(meta_desc)}"', content, flags=re.IGNORECASE)
            print(f"✓ Updated meta description: {url_key}")
    else:
        # Add meta description in head
        head_pattern = r'(<head[^>]*>)'
        if re.search(head_pattern, content):
            meta_tag = f'    <meta name="description" content="{meta_desc}">\n'
            content = re.sub(head_pattern, r'\1\n' + meta_tag, content, count=1)
            print(f"✓ Added meta description: {url_key}")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("\n✓ Description check complete for batch 1")

