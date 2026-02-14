#!/usr/bin/env python3
"""
Generate pages.html using separate descriptions file instead of extracting from pages.

This allows you to:
1. Manually edit descriptions in descriptions.json
2. Update page content freely
3. Descriptions never change unless you edit them
"""
import json
import re
from pathlib import Path
from html import escape, unescape

BASE_DIR = Path(__file__).parent.parent
DESCRIPTIONS_FILE = BASE_DIR / 'site_agent' / 'descriptions.json'
PAGES_HTML = BASE_DIR / 'site_agent' / 'pages.html'

def load_descriptions():
    """Load descriptions from JSON file"""
    if DESCRIPTIONS_FILE.exists():
        with open(DESCRIPTIONS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def extract_h1(content):
    """Extract h1 heading from HTML content"""
    match = re.search(r'<h1>(.*?)</h1>', content, re.DOTALL)
    if match:
        h1 = match.group(1).strip()
        h1 = re.sub(r'\s+', ' ', h1)
        return h1
    return None

def extract_title(content):
    """Extract title from HTML content"""
    match = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def extract_metadata(content):
    """Extract page metadata"""
    metadata = []
    
    title = extract_title(content)
    if title:
        metadata.append(f"Title: {title}")
    
    charset_match = re.search(r'<meta\s+charset=["\']([^"\']+)["\']', content, re.I)
    if charset_match:
        metadata.append(f"Charset: {charset_match.group(1)}")
    
    viewport_match = re.search(r'<meta\s+name=["\']viewport["\']\s+content=["\']([^"\']+)["\']', content, re.I)
    if viewport_match:
        metadata.append(f"Viewport: {viewport_match.group(1)}")
    
    keywords_match = re.search(r'<meta\s+name=["\']keywords["\']\s+content=["\']([^"\']+)["\']', content, re.I)
    if keywords_match:
        metadata.append(f"Keywords: {keywords_match.group(1)[:50]}...")
    
    author_match = re.search(r'<meta\s+name=["\']author["\']\s+content=["\']([^"\']+)["\']', content, re.I)
    if author_match:
        metadata.append(f"Author: {author_match.group(1)}")
    
    return "<br>".join(metadata) if metadata else "No metadata found"

def extract_all_page_content(content):
    """Extract all visible text content from the page (for Page Content column)"""
    from html import unescape
    
    content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL | re.IGNORECASE)
    
    content_text_pattern = r'<div[^>]*class=["\'][^"\']*content-text[^"\']*["\'][^>]*>(.*?)</div>'
    content_matches = re.findall(content_text_pattern, content, re.DOTALL | re.IGNORECASE)
    
    all_text_parts = []
    
    for content_block in content_matches:
        paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', content_block, re.DOTALL | re.IGNORECASE)
        for para in paragraphs:
            para_text = re.sub(r'<[^>]+>', '', para)
            para_text = unescape(para_text)
            para_text = re.sub(r'\s+', ' ', para_text).strip()
            if para_text and len(para_text) > 10:
                all_text_parts.append(para_text)
    
    main_content_patterns = [
        r'<main[^>]*>(.*?)</main>',
        r'<article[^>]*>(.*?)</article>',
        r'<section[^>]*>(.*?)</section>',
    ]
    
    for pattern in main_content_patterns:
        matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
        for match in matches:
            if 'content-text' not in match.lower():
                paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', match, re.DOTALL | re.IGNORECASE)
                for para in paragraphs:
                    para_text = re.sub(r'<[^>]+>', '', para)
                    para_text = unescape(para_text)
                    para_text = re.sub(r'\s+', ' ', para_text).strip()
                    if para_text and len(para_text) > 10:
                        all_text_parts.append(para_text)
    
    full_content = ' '.join(all_text_parts)
    full_content = re.sub(r'\s+', ' ', full_content).strip()
    
    return full_content if full_content else ""

def generate_faq_from_description(description, page_name, url):
    """Generate FAQs from description"""
    if not description or description == "No content found":
        return "No FAQ available"
    
    faq_items = []
    
    if page_name:
        faq_items.append(f"Q: What is {page_name}?<br>A: {page_name} is part of the PIANDT triadic information architecture. {description[:200]}...")
    
    if "triadic" in description.lower() or "signal" in description.lower():
        faq_items.append("Q: How does this component work within the triadic information system?<br>A: This component operates within the PIANDT triadic information framework, which ensures that every signal follows a structured pathway from reception (In) through processing (Proc) to delivery (Out), maintaining proportional relationships and enabling full automation.")
    
    if "automation" in description.lower() or "automated" in description.lower():
        faq_items.append("Q: What are the automation benefits?<br>A: The structured nature of this information, organized into discrete signal units with explicit triadic mapping, enables full automation of business transactions through machine-readable formats, standardized protocols, and programmable routing mechanisms.")
    
    if "bidirectional" in description.lower() or "both directions" in description.lower():
        faq_items.append("Q: Does this support bidirectional interactions?<br>A: Yes, this component supports bidirectional interaction patterns, where communications flow seamlessly in both directions between the organization and external stakeholders.")
    
    return "<br><br>".join(faq_items[:5]) if faq_items else "No FAQ available"

def extract_page_name_from_url(url):
    """Extract page name from URL"""
    parts = url.split('/')
    filename = parts[-1].replace('.html', '')
    filename = re.sub(r'^(in_|proc_|out_)', '', filename)
    name = filename.replace('_', ' ').title()
    return name

def get_all_html_pages():
    """Get all HTML files"""
    html_files = []
    for html_file in BASE_DIR.rglob("*.html"):
        rel_path = html_file.relative_to(BASE_DIR)
        if 'site_agent' not in str(rel_path) and '.git' not in str(rel_path):
            html_files.append(html_file)
    return sorted(html_files)

def generate_pages_html():
    """Generate pages.html using separate descriptions file"""
    print("="*60)
    print("GENERATING PAGES.HTML WITH SEPARATE DESCRIPTIONS")
    print("="*60)
    
    descriptions = load_descriptions()
    print(f"\nLoaded {len(descriptions)} descriptions from descriptions.json")
    
    html_files = get_all_html_pages()
    print(f"Found {len(html_files)} HTML pages\n")
    
    pages_data = []
    
    for html_file in html_files:
        rel_path = html_file.relative_to(BASE_DIR)
        url = str(rel_path).replace('\\', '/')
        
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            h1 = extract_h1(content)
            title = extract_title(content)
            metadata = extract_metadata(content)
            
            # Get description from separate file, or extract as fallback
            if url in descriptions:
                # Handle both string and dict formats
                if isinstance(descriptions[url], dict):
                    description = descriptions[url].get('description', 'No description found')
                else:
                    description = descriptions[url]
                print(f"  ✅ Using separate description for: {url}")
            else:
                # Fallback: extract from page
                full_content = extract_all_page_content(content)
                meta_desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', content)
                meta_desc = meta_desc_match.group(1) if meta_desc_match else None
                description = full_content if full_content else (meta_desc if meta_desc else "No description found")
                print(f"  ⚠️  No separate description for {url}, using extracted")
            
            # Extract page content (for Page Content column)
            # For now, keep Page Content empty so it can be filled manually later
            page_content = ''
            
            # Generate FAQ
            page_name = h1 if h1 and h1 != "No heading found" else extract_page_name_from_url(url)
            faq = generate_faq_from_description(description, page_name, url)
            
            if not h1:
                h1 = "No heading found"
            
            pages_data.append({
                'url': url,
                'description': description,  # From separate file
                'content': page_content,      # Extracted from page
                'h1': h1,
                'title': title,
                'metadata': metadata,
                'faq': faq
            })
            
        except Exception as e:
            print(f"  ⚠️  Error processing {rel_path}: {e}")
            pages_data.append({
                'url': url,
                'description': f"Error: {e}",
                'content': '',
                'h1': "Error",
                'title': None,
                'metadata': "Error",
                'faq': "Error"
            })
    
    # Generate HTML (same structure as update_pages_html.py)
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
            text-align: justify;
        }
        tr:hover {
            background-color: #f9f9f9;
        }
        .num-col { width: 5%; min-width: 50px; text-align: right; font-weight: bold; color: #666; padding-right: 15px; }
        th.num-col { color: white; }
        .url-col { width: 20%; font-family: monospace; font-size: 0.9em; word-break: break-all; }
        th.url-col { color: white; font-family: Arial, sans-serif; font-size: 1em; }
        .heading-col { width: 15%; font-weight: bold; color: #1a1a1a; min-width: 120px; }
        th.heading-col { color: white; }
        .desc-col { width: 25%; }
        th.desc-col { color: white; }
        .content-col { width: 20%; font-size: 0.85em; color: #555; }
        th.content-col { color: white; }
        .faq-col { width: 10%; font-size: 0.85em; color: #555; }
        th.faq-col { color: white; }
        .metadata-col { width: 5%; font-size: 0.85em; color: #555; }
        th.metadata-col { color: white; font-size: 1em; }
        a { color: #0066cc; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>PIANDT Website Pages</h1>
    <div class="summary">
        <strong>Total Pages:</strong> ''' + str(len(pages_data)) + '''
        <br><strong>Note:</strong> Descriptions from descriptions.json (separate from page content)
    </div>
    <table>
        <thead>
            <tr>
                <th class="num-col"></th>
                <th class="url-col">Page URL</th>
                <th class="heading-col">Page Heading</th>
                <th class="desc-col">Page Description</th>
                <th class="content-col">Page Content</th>
                <th class="faq-col">FAQ</th>
                <th class="metadata-col">Page Metadata</th>
            </tr>
        </thead>
        <tbody>
'''
    
    for idx, page in enumerate(pages_data, start=1):
        url_escaped = escape(page['url'])
        h1_escaped = escape(page['h1'])
        desc_escaped = escape(page['description'])
        # Keep Page Content column empty for now (user will fill it manually)
        content_escaped = ''
        faq_html = page.get('faq', 'No FAQ found')
        metadata_html = page['metadata']
        
        html_content += f'''            <tr>
                <td class="num-col">{idx}</td>
                <td class="url-col"><a href="{url_escaped}">{url_escaped}</a></td>
                <td class="heading-col">{h1_escaped}</td>
                <td class="desc-col">{desc_escaped}</td>
                <td class="content-col"></td>
                <td class="faq-col">{faq_html}</td>
                <td class="metadata-col">{metadata_html}</td>
            </tr>

'''
    
    html_content += '''        </tbody>
    </table>
</body>
</html>'''
    
    with open(PAGES_HTML, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n✅ Generated pages.html with {len(pages_data)} pages")
    print(f"✅ Descriptions from: descriptions.json")
    print(f"✅ Page Content extracted from: actual pages")
    return True

if __name__ == '__main__':
    generate_pages_html()

