#!/usr/bin/env python3
"""
Generate pages.json with all page information for dynamic menu generation
"""
import json
import re
from pathlib import Path
from html import escape

base_dir = Path(__file__).parent.parent

# Get all HTML files
html_files = sorted(base_dir.rglob("*.html"))
html_files = [f for f in html_files if 'site_agent' not in str(f)]

pages_data = {}

def extract_page_info(html_file):
    """Extract page information from HTML file"""
    rel_path = html_file.relative_to(base_dir)
    url = str(rel_path).replace('\\', '/')
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract title
    title_match = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
    title = title_match.group(1).strip() if title_match else ''
    
    # Extract h1
    h1_match = re.search(r'<h1>(.*?)</h1>', content)
    h1 = h1_match.group(1).strip() if h1_match else ''
    
    # Determine triad and category
    triad = None
    category = None
    
    if 'in/' in url:
        triad = 'in'
    elif 'processing/' in url:
        triad = 'proc'
    elif 'out/' in url:
        triad = 'out'
    
    if 'about_piandt' in url:
        category = 'about_piandt'
    elif 'units' in url:
        category = 'units'
    
    return {
        'url': url,
        'title': title,
        'h1': h1,
        'triad': triad,
        'category': category
    }

# Organize pages by triad and category
for html_file in html_files:
    info = extract_page_info(html_file)
    
    if info['triad'] and info['category']:
        if info['triad'] not in pages_data:
            pages_data[info['triad']] = {}
        if info['category'] not in pages_data[info['triad']]:
            pages_data[info['triad']][info['category']] = []
        
        pages_data[info['triad']][info['category']].append({
            'url': info['url'],
            'title': info['title'],
            'h1': info['h1']
        })

# Write JSON file
json_file = base_dir / 'pages.json'
with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(pages_data, f, indent=2, ensure_ascii=False)

print(f"Generated {json_file}")
print(f"Triads: {list(pages_data.keys())}")
for triad, categories in pages_data.items():
    print(f"  {triad}: {list(categories.keys())}")

