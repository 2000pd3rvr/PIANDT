#!/usr/bin/env python3
"""
Preserve current page descriptions before updating pages, then restore them.

This allows you to update page content without losing the current descriptions
in pages.html.
"""
import json
import re
from pathlib import Path
from html import escape, unescape

BASE_DIR = Path(__file__).parent.parent
DESCRIPTIONS_BACKUP = BASE_DIR / 'site_agent' / 'descriptions_backup.json'

def extract_meta_description(content):
    """Extract meta description from HTML content"""
    match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', content)
    if match:
        return match.group(1)
    return None

def extract_all_page_content(content):
    """Extract all visible text content from the page"""
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
    
    return full_content if full_content else "No content found"

def backup_current_descriptions():
    """Backup current descriptions from pages.html"""
    pages_html = BASE_DIR / 'site_agent' / 'pages.html'
    
    if not pages_html.exists():
        print("❌ pages.html not found. Run update_pages_html.py first.")
        return False
    
    with open(pages_html, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract descriptions from pages.html table
    pattern = r'<tr>\s*<td[^>]*>(\d+)</td>\s*<td[^>]*><a[^>]*>([^<]+)</a></td>\s*<td[^>]*>([^<]*)</td>\s*<td[^>]*>([^<]*(?:<[^>]+>[^<]*</[^>]+>[^<]*)*)</td>'
    matches = re.findall(pattern, content, re.DOTALL)
    
    descriptions = {}
    for match in matches:
        row_num, url, heading, description = match
        # Clean HTML from description
        desc_clean = re.sub(r'<[^>]+>', '', description)
        desc_clean = unescape(desc_clean).strip()
        descriptions[url] = {
            'row': int(row_num),
            'heading': heading.strip(),
            'description': desc_clean
        }
    
    # Save backup
    with open(DESCRIPTIONS_BACKUP, 'w', encoding='utf-8') as f:
        json.dump(descriptions, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Backed up {len(descriptions)} descriptions to {DESCRIPTIONS_BACKUP.name}")
    return True

def restore_descriptions_to_pages_html():
    """Update pages.html to use backed-up descriptions instead of extracting new ones"""
    if not DESCRIPTIONS_BACKUP.exists():
        print("❌ No backup found. Run backup first.")
        return False
    
    with open(DESCRIPTIONS_BACKUP, 'r', encoding='utf-8') as f:
        descriptions = json.load(f)
    
    # Import the update script's functions
    import sys
    sys.path.insert(0, str(BASE_DIR / 'site_agent'))
    from update_pages_html import (
        get_all_html_pages, extract_h1, extract_title, 
        extract_metadata, generate_faq_from_description,
        extract_page_name_from_url
    )
    
    html_files = get_all_html_pages()
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
            
            # Use backed-up description if available, otherwise extract new
            if url in descriptions:
                description = descriptions[url]['description']
                print(f"  ✅ Using preserved description for: {url}")
            else:
                # Extract new description as fallback
                full_content = extract_all_page_content(content)
                meta_desc = extract_meta_description(content)
                description = full_content if full_content else (meta_desc if meta_desc else "No content found")
                print(f"  ⚠️  No backup for {url}, using extracted description")
            
            # Generate FAQ
            page_name = h1 if h1 and h1 != "No heading found" else extract_page_name_from_url(url)
            faq = generate_faq_from_description(description, page_name, url)
            
            if not h1:
                h1 = "No heading found"
            
            pages_data.append({
                'url': url,
                'description': description,
                'content': '',  # Page content - empty for now
                'h1': h1,
                'title': title,
                'metadata': metadata,
                'faq': faq
            })
            
        except Exception as e:
            print(f"  ⚠️  Error processing {rel_path}: {e}")
            pages_data.append({
                'url': url,
                'description': f"Error reading file: {e}",
                'content': '',
                'h1': "Error",
                'title': None,
                'metadata': "Error reading metadata",
                'faq': "Error reading FAQ"
            })
    
    # Generate HTML (same as update_pages_html.py)
    from html import escape
    PAGES_HTML = BASE_DIR / 'site_agent' / 'pages.html'
    
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
        .num-col {
            width: 5%;
            min-width: 50px;
            text-align: right;
            font-weight: bold;
            color: #666;
            padding-right: 15px;
        }
        th.num-col {
            color: white;
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
            width: 25%;
        }
        th.desc-col {
            color: white;
        }
        .content-col {
            width: 20%;
            font-size: 0.85em;
            color: #555;
        }
        th.content-col {
            color: white;
        }
        .faq-col {
            width: 10%;
            font-size: 0.85em;
            color: #555;
        }
        th.faq-col {
            color: white;
        }
        .metadata-col {
            width: 5%;
            font-size: 0.85em;
            color: #555;
        }
        th.metadata-col {
            color: white;
            font-size: 1em;
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
        <br><strong>Note:</strong> Descriptions preserved from backup
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
        content_escaped = escape(page['content'])
        faq_html = page.get('faq', 'No FAQ found')
        metadata_html = page['metadata']
        
        html_content += f'''            <tr>
                <td class="num-col">{idx}</td>
                <td class="url-col"><a href="{url_escaped}">{url_escaped}</a></td>
                <td class="heading-col">{h1_escaped}</td>
                <td class="desc-col">{desc_escaped}</td>
                <td class="content-col">{content_escaped}</td>
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
    
    print(f"\n✅ Updated pages.html with {len(pages_data)} pages (descriptions preserved)")
    return True

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 site_agent/preserve_descriptions.py backup    # Backup current descriptions")
        print("  python3 site_agent/preserve_descriptions.py restore   # Restore descriptions to pages.html")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'backup':
        print("="*60)
        print("BACKING UP CURRENT DESCRIPTIONS")
        print("="*60)
        backup_current_descriptions()
    elif command == 'restore':
        print("="*60)
        print("RESTORING DESCRIPTIONS TO PAGES.HTML")
        print("="*60)
        restore_descriptions_to_pages_html()
    else:
        print(f"❌ Unknown command: {command}")
        print("Use 'backup' or 'restore'")
        sys.exit(1)

if __name__ == '__main__':
    main()

