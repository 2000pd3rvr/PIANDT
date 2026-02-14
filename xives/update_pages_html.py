#!/usr/bin/env python3
"""
Update pages.html with all pages, including links, descriptions, and headings
"""
import re
from pathlib import Path
from html import escape

BASE_DIR = Path(__file__).parent.parent
PAGES_HTML = Path(__file__).parent / "pages.html"

def extract_meta_description(content):
    """Extract meta description from HTML content"""
    match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', content)
    if match:
        return match.group(1)
    return None

def extract_all_page_content(content):
    """Extract all visible text content from the page - all paragraphs, columns, and sheets"""
    from html import unescape
    
    # Remove script and style tags
    content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL | re.IGNORECASE)
    
    # Extract all text from content-text divs (main content area)
    content_text_pattern = r'<div[^>]*class=["\'][^"\']*content-text[^"\']*["\'][^>]*>(.*?)</div>'
    content_matches = re.findall(content_text_pattern, content, re.DOTALL | re.IGNORECASE)
    
    all_text_parts = []
    
    # Extract text from all content-text divs
    for content_block in content_matches:
        # Extract all paragraphs
        paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', content_block, re.DOTALL | re.IGNORECASE)
        for para in paragraphs:
            # Remove HTML tags but keep text
            para_text = re.sub(r'<[^>]+>', '', para)
            # Decode HTML entities
            para_text = unescape(para_text)
            # Clean up whitespace
            para_text = re.sub(r'\s+', ' ', para_text).strip()
            if para_text and len(para_text) > 10:  # Only add non-empty paragraphs
                all_text_parts.append(para_text)
    
    # Also extract text from any other main content areas (sections, articles, etc.)
    # Look for main, article, section tags
    main_content_patterns = [
        r'<main[^>]*>(.*?)</main>',
        r'<article[^>]*>(.*?)</article>',
        r'<section[^>]*>(.*?)</section>',
    ]
    
    for pattern in main_content_patterns:
        matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
        for match in matches:
            # Skip if already captured in content-text
            if 'content-text' not in match.lower():
                # Extract paragraphs
                paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', match, re.DOTALL | re.IGNORECASE)
                for para in paragraphs:
                    para_text = re.sub(r'<[^>]+>', '', para)
                    para_text = unescape(para_text)
                    para_text = re.sub(r'\s+', ' ', para_text).strip()
                    if para_text and len(para_text) > 10:
                        all_text_parts.append(para_text)
    
    # Combine all text parts
    full_content = ' '.join(all_text_parts)
    
    # Clean up excessive whitespace
    full_content = re.sub(r'\s+', ' ', full_content).strip()
    
    return full_content if full_content else "No content found"

def extract_h1(content):
    """Extract h1 heading from HTML content"""
    match = re.search(r'<h1>(.*?)</h1>', content, re.DOTALL)
    if match:
        # Clean up HTML entities and whitespace
        h1 = match.group(1).strip()
        h1 = re.sub(r'\s+', ' ', h1)  # Normalize whitespace
        return h1
    return None

def extract_title(content):
    """Extract title from HTML content"""
    match = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def extract_metadata(content):
    """Extract page metadata (title, charset, viewport, etc.)"""
    metadata = []
    
    # Extract title
    title = extract_title(content)
    if title:
        metadata.append(f"Title: {title}")
    
    # Extract charset
    charset_match = re.search(r'<meta\s+charset=["\']([^"\']+)["\']', content, re.I)
    if charset_match:
        metadata.append(f"Charset: {charset_match.group(1)}")
    
    # Extract viewport
    viewport_match = re.search(r'<meta\s+name=["\']viewport["\']\s+content=["\']([^"\']+)["\']', content, re.I)
    if viewport_match:
        metadata.append(f"Viewport: {viewport_match.group(1)}")
    
    # Extract keywords if present
    keywords_match = re.search(r'<meta\s+name=["\']keywords["\']\s+content=["\']([^"\']+)["\']', content, re.I)
    if keywords_match:
        metadata.append(f"Keywords: {keywords_match.group(1)[:50]}...")
    
    # Extract author if present
    author_match = re.search(r'<meta\s+name=["\']author["\']\s+content=["\']([^"\']+)["\']', content, re.I)
    if author_match:
        metadata.append(f"Author: {author_match.group(1)}")
    
    return "<br>".join(metadata) if metadata else "No metadata found"

def get_all_html_pages():
    """Get all HTML files excluding site_agent and .git directories"""
    html_files = []
    for html_file in BASE_DIR.rglob("*.html"):
        rel_path = html_file.relative_to(BASE_DIR)
        # Exclude site_agent and .git directories
        if 'site_agent' not in str(rel_path) and '.git' not in str(rel_path):
            html_files.append(html_file)
    return sorted(html_files)

def generate_pages_html():
    """Generate updated pages.html with all pages"""
    print("="*60)
    print("UPDATING PAGES.HTML")
    print("="*60)
    
    html_files = get_all_html_pages()
    print(f"\nFound {len(html_files)} HTML pages\n")
    
    pages_data = []
    
    for html_file in html_files:
        rel_path = html_file.relative_to(BASE_DIR)
        url = str(rel_path).replace('\\', '/')
        
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract meta description (for reference, but we'll use full content)
            meta_desc = extract_meta_description(content)
            # Extract ALL page content (all paragraphs, columns, sheets)
            full_content = extract_all_page_content(content)
            h1 = extract_h1(content)
            title = extract_title(content)
            metadata = extract_metadata(content)
            
            # Use full content as description (all text from page)
            description = full_content if full_content else (meta_desc if meta_desc else "No content found")
            
            if not h1:
                h1 = "No heading found"
            
            pages_data.append({
                'url': url,
                'description': description,
                'h1': h1,
                'title': title,
                'metadata': metadata
            })
            
        except Exception as e:
            print(f"  ⚠️  Error processing {rel_path}: {e}")
            pages_data.append({
                'url': url,
                'description': f"Error reading file: {e}",
                'h1': "Error",
                'title': None,
                'metadata': "Error reading metadata"
            })
    
    # Generate HTML
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>📊</text></svg>">
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
        .summary {
            background-color: white;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background-color: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-top: 20px;
            table-layout: fixed;
        }
        th {
            background-color: #1a1a1a;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: bold;
            font-size: 1em;
            font-family: Arial, sans-serif;
        }
        td {
            padding: 10px;
            border-bottom: 1px solid #ddd;
            vertical-align: top;
        }
        tr:hover {
            background-color: #f9f9f9;
        }
        .num-col {
            width: 5%;
            min-width: 50px;
            text-align: right;
            font-weight: bold;
            color: #666;
            padding-right: 15px;
        }
        .url-col {
            width: 20%;
            font-family: monospace;
            font-size: 0.9em;
            word-break: break-all;
        }
        th.url-col {
            color: white;
            font-family: Arial, sans-serif;
            font-size: 1em;
        }
        .heading-col {
            width: 15%;
            font-weight: bold;
            color: #1a1a1a;
            min-width: 120px;
        }
        th.heading-col {
            color: white;
        }
        .desc-col {
            width: 35%;
        }
        th.desc-col {
            color: white;
        }
        .metadata-col {
            width: 25%;
            font-size: 0.85em;
            color: #555;
        }
        th.metadata-col {
            color: white;
            font-size: 1em;
        }
        th.num-col {
            color: white;
        }
        a {
            color: #0066cc;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <h1>PIANDT Website Pages</h1>
    <div class="summary">
        <strong>Total Pages:</strong> ''' + str(len(pages_data)) + '''
    </div>
    <table>
        <thead>
            <tr>
                <th class="num-col"></th>
                <th class="url-col">Page URL</th>
                <th class="heading-col">Page Heading</th>
                <th class="desc-col">Page Description</th>
                <th class="metadata-col">Page Metadata</th>
            </tr>
        </thead>
        <tbody>
'''
    
    for idx, page in enumerate(pages_data, start=1):
        url_escaped = escape(page['url'])
        h1_escaped = escape(page['h1'])
        desc_escaped = escape(page['description'])
        # Metadata may contain HTML (br tags), so don't escape it fully
        metadata_html = page.get('metadata', 'No metadata found')
        
        html_content += f'''            <tr>
                <td class="num-col">{idx}</td>
                <td class="url-col"><a href="{url_escaped}">{url_escaped}</a></td>
                <td class="heading-col">{h1_escaped}</td>
                <td class="desc-col">{desc_escaped}</td>
                <td class="metadata-col">{metadata_html}</td>
            </tr>

'''
    
    html_content += '''        </tbody>
    </table>
</body>
</html>'''
    
    # Write to file
    with open(PAGES_HTML, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n✅ Updated pages.html with {len(pages_data)} pages")
    print(f"✅ File saved to: {PAGES_HTML}")
    print("\n" + "="*60)
    print("✅ PAGES.HTML UPDATE COMPLETE!")
    print("="*60)

if __name__ == '__main__':
    generate_pages_html()

