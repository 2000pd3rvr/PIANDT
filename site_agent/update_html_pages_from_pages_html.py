#!/usr/bin/env python3
"""
Update actual HTML pages with content from pages.html Page Content column.
This script reads pages.html and updates the paragraph content in each HTML page.
"""
import re
from pathlib import Path
from html import unescape

BASE_DIR = Path(__file__).parent.parent
PAGES_HTML = Path(__file__).parent / "pages.html"

def parse_pages_html():
    """Parse pages.html and extract Page Content for each page"""
    with open(PAGES_HTML, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all table rows
    pattern = r'<tr>\s*<td class="num-col">(\d+)</td>\s*<td class="url-col"><a[^>]*>([^<]+)</a></td>\s*<td class="heading-col">[^<]*</td>\s*<td class="desc-col">[^<]*(?:<[^>]+>[^<]*</[^>]+>[^<]*)*</td>\s*<td class="content-col">([^<]*(?:<[^>]+>[^<]*</[^>]+>[^<]*)*)</td>'
    matches = re.findall(pattern, content, re.DOTALL)
    
    pages_content = {}
    for match in matches:
        row_num, url, page_content = match
        # Clean HTML from content
        content_clean = re.sub(r'<[^>]+>', '', page_content)
        content_clean = unescape(content_clean).strip()
        pages_content[url.strip()] = content_clean
    
    return pages_content

def update_html_page(file_path, new_content):
    """Update paragraph content in an HTML page"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find content-text div
    content_text_pattern = r'(<div[^>]*class=["\'][^"\']*content-text[^"\']*["\'][^>]*>)(.*?)(</div>)'
    match = re.search(content_text_pattern, content, re.DOTALL | re.IGNORECASE)
    
    if not match:
        return False
    
    div_start = match.group(1)
    div_end = match.group(3)
    
    # Split new content into paragraphs
    if '\n\n' in new_content:
        paragraphs = [p.strip() for p in new_content.split('\n\n') if p.strip()]
    else:
        paragraphs = [p.strip() for p in new_content.split('\n') if p.strip()]
    
    # Create new paragraph HTML
    new_paragraphs_html = '\n                        '.join([f'<p>{p}</p>' for p in paragraphs])
    
    # Replace content
    new_content_text_block = div_start + '\n                        ' + new_paragraphs_html + '\n                    ' + div_end
    new_content_html = content[:match.start()] + new_content_text_block + content[match.end():]
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content_html)
    
    return True

def main():
    print("="*70)
    print("UPDATING HTML PAGES FROM PAGES.HTML")
    print("="*70)
    
    # Parse pages.html
    pages_content = parse_pages_html()
    print(f"\nLoaded {len(pages_content)} pages from pages.html")
    
    # Get all HTML files
    html_files = []
    for html_file in BASE_DIR.rglob("*.html"):
        rel_path = html_file.relative_to(BASE_DIR)
        if 'site_agent' not in str(rel_path) and '.git' not in str(rel_path) and 'xives' not in str(rel_path):
            url = str(rel_path).replace('\\', '/')
            html_files.append((html_file, url))
    
    updated_count = 0
    skipped_count = 0
    
    for html_file, url in html_files:
        if url in pages_content:
            content = pages_content[url]
            if content:  # Only update if content is not empty
                if update_html_page(html_file, content):
                    updated_count += 1
                    print(f"  ✅ Updated: {url}")
                else:
                    print(f"  ⚠️  Failed to update: {url}")
            else:
                skipped_count += 1
                print(f"  ⏭️  Skipped (empty content): {url}")
        else:
            print(f"  ⚠️  No content found in pages.html for: {url}")
    
    print("\n" + "="*70)
    print(f"✅ Updated {updated_count} pages")
    print(f"⏭️  Skipped {skipped_count} pages (empty content)")
    print("="*70)

if __name__ == '__main__':
    main()

