#!/usr/bin/env python3
"""
Comprehensive update of pages.html:
1. Extract descriptions from all HTML pages (meta description tags)
2. Verify each page is linked in navigation menus
3. Update pages.html with current structure
4. Ensure all pages are included with correct URLs and descriptions
"""

import re
from pathlib import Path
from html import escape
from html import unescape

BASE_DIR = Path(__file__).parent.parent
PAGES_HTML = BASE_DIR / 'site_agent' / 'pages.html'

def extract_meta_description(html_content):
    """Extract meta description from HTML content"""
    # Try meta name="description"
    pattern = r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']'
    match = re.search(pattern, html_content, re.IGNORECASE)
    if match:
        return unescape(match.group(1)).strip()
    
    # Try meta property="og:description"
    pattern = r'<meta\s+property=["\']og:description["\']\s+content=["\']([^"\']+)["\']'
    match = re.search(pattern, html_content, re.IGNORECASE)
    if match:
        return unescape(match.group(1)).strip()
    
    return None

def extract_title(html_content):
    """Extract page title"""
    pattern = r'<title>(.*?)</title>'
    match = re.search(pattern, html_content, re.IGNORECASE | re.DOTALL)
    if match:
        return unescape(match.group(1)).strip()
    return None

def check_page_in_menu(html_file, all_html_files):
    """Check if a page is linked in navigation menus"""
    file_path = html_file.relative_to(BASE_DIR)
    filename = html_file.name
    
    # Check if this page is referenced in other pages' navigation menus
    for other_file in all_html_files:
        if other_file == html_file:
            continue
        
        try:
            with open(other_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for filename in href attributes
            if filename in content:
                # More specific check - look for href with this filename
                pattern = rf'href=["\'][^"\']*{re.escape(filename)}["\']'
                if re.search(pattern, content):
                    return True
        except:
            pass
    
    return False

def get_all_html_pages():
    """Get all HTML pages excluding site_agent and other non-page files"""
    html_files = []
    
    # Get all HTML files
    for html_file in BASE_DIR.rglob('*.html'):
        # Skip site_agent directory
        if 'site_agent' in str(html_file):
            continue
        
        # Skip if it's a page file
        html_files.append(html_file)
    
    # Sort by path for consistent ordering
    html_files.sort(key=lambda x: str(x.relative_to(BASE_DIR)))
    
    return html_files

def generate_pages_html():
    """Generate updated pages.html with all pages"""
    print("="*60)
    print("UPDATING PAGES.HTML")
    print("="*60)
    
    html_files = get_all_html_pages()
    print(f"\nFound {len(html_files)} HTML pages\n")
    
    pages_data = []
    pages_without_desc = []
    pages_not_in_menu = []
    
    for html_file in html_files:
        rel_path = html_file.relative_to(BASE_DIR)
        
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            description = extract_meta_description(content)
            title = extract_title(content)
            
            if not description:
                description = "No description found"
                pages_without_desc.append(str(rel_path))
            
            # Check if page is in menu
            in_menu = check_page_in_menu(html_file, html_files)
            if not in_menu and html_file.name != 'index.html':
                pages_not_in_menu.append(str(rel_path))
            
            pages_data.append({
                'url': str(rel_path),
                'description': description,
                'title': title,
                'in_menu': in_menu
            })
            
        except Exception as e:
            print(f"  ⚠️  Error processing {rel_path}: {e}")
            pages_data.append({
                'url': str(rel_path),
                'description': f"Error reading file: {e}",
                'title': None,
                'in_menu': False
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
        .warning {
            color: #d32f2f;
            font-weight: bold;
        }
        .ok {
            color: #388e3c;
        }
    </style>
</head>
<body>
    <h1>PIANDT Website Pages</h1>
    <div class="summary">
        <strong>Total Pages:</strong> ''' + str(len(pages_data)) + '''<br>
        <strong>Pages with descriptions:</strong> <span class="ok">''' + str(len(pages_data) - len(pages_without_desc)) + '''</span><br>
        <strong>Pages in navigation menus:</strong> <span class="ok">''' + str(len(pages_data) - len(pages_not_in_menu)) + '''</span><br>
        <strong>Pages without descriptions:</strong> <span class="warning">''' + str(len(pages_without_desc)) + '''</span><br>
        <strong>Pages not in menus:</strong> <span class="warning">''' + str(len(pages_not_in_menu)) + '''</span>
    </div>
    <table>
        <thead>
            <tr>
                <th class="url-col">1. Page URL</th>
                <th class="desc-col">2. Page Description</th>
                <th class="content-col">3. Page Content</th>
            </tr>
        </thead>
        <tbody>
'''
    
    for page in pages_data:
        desc_escaped = escape(page['description'])
        url_escaped = escape(page['url'])
        
        html_content += f'''            <tr>
                <td class="url-col">{url_escaped}</td>
                <td class="desc-col">{desc_escaped}</td>
                <td class="content-col"></td>
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
    
    if pages_without_desc:
        print(f"\n⚠️  Pages without descriptions ({len(pages_without_desc)}):")
        for page in pages_without_desc:
            print(f"   - {page}")
    
    if pages_not_in_menu:
        print(f"\n⚠️  Pages not in navigation menus ({len(pages_not_in_menu)}):")
        for page in pages_not_in_menu:
            print(f"   - {page}")
    
    print("\n" + "="*60)
    print("✅ PAGES.HTML UPDATE COMPLETE!")
    print("="*60)

if __name__ == '__main__':
    generate_pages_html()

