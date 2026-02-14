#!/usr/bin/env python3
"""
Extract page content from all HTML files and create a table
"""
import os
import re
from pathlib import Path
from html import escape

# Base directory
base_dir = Path(__file__).parent.parent

# Get all HTML files
html_files = sorted(base_dir.rglob("*.html"))

pages_data = []

def extract_text_from_html(html_content):
    """Extract text content from HTML, focusing on content-text div"""
    # Remove script and style tags
    html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    
    # Try to find content-text div
    content_match = re.search(r'<div[^>]*class="content-text"[^>]*>(.*?)</div>', html_content, re.DOTALL | re.IGNORECASE)
    if content_match:
        content = content_match.group(1)
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', ' ', content)
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    # Fallback: try to find main section
    main_match = re.search(r'<main[^>]*>(.*?)</main>', html_content, re.DOTALL | re.IGNORECASE)
    if main_match:
        content = main_match.group(1)
        text = re.sub(r'<[^>]+>', ' ', content)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    # Last resort: extract all text
    text = re.sub(r'<[^>]+>', ' ', html_content)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

for html_file in html_files:
    # Skip if in site_agent directory
    if 'site_agent' in str(html_file):
        continue
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Get page URL (relative to base)
        rel_path = html_file.relative_to(base_dir)
        page_url = str(rel_path).replace('\\', '/')
        
        # Extract body text
        body_text = extract_text_from_html(content)
        
        # Limit length for table display
        if len(body_text) > 1000:
            body_text = body_text[:1000] + "..."
        
        pages_data.append({
            'url': page_url,
            'description': body_text
        })
        
    except Exception as e:
        print(f"Error processing {html_file}: {e}")
        pages_data.append({
            'url': str(html_file.relative_to(base_dir)),
            'description': f"Error reading file: {str(e)}"
        })

# Generate HTML table
html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PIANDT Site Pages</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #1a1a1a;
            text-align: center;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background-color: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-top: 20px;
        }
        th {
            background-color: #1a1a1a;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: bold;
        }
        td {
            padding: 10px;
            border-bottom: 1px solid #ddd;
            vertical-align: top;
        }
        tr:hover {
            background-color: #f9f9f9;
        }
        .url-col {
            width: 25%;
            font-family: monospace;
            font-size: 0.9em;
            word-break: break-all;
        }
        .desc-col {
            width: 50%;
        }
        .content-col {
            width: 25%;
            color: #999;
            font-style: italic;
        }
    </style>
</head>
<body>
    <h1>PIANDT Website Pages</h1>
    <table>
        <thead>
            <tr>
                <th class="url-col">1. Page URL</th>
                <th class="desc-col">2. Page Description</th>
                <th class="content-col">3. Page Content</th>
            </tr>
        </thead>
        <tbody>
"""

for page in pages_data:
    html_content += f"""
            <tr>
                <td class="url-col">{escape(page['url'])}</td>
                <td class="desc-col">{escape(page['description'])}</td>
                <td class="content-col"></td>
            </tr>
"""

html_content += """
        </tbody>
    </table>
</body>
</html>
"""

# Write HTML file
html_file_path = base_dir / 'site_agent' / 'pages.html'
with open(html_file_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Generated HTML file: {html_file_path}")
print(f"Total pages: {len(pages_data)}")
