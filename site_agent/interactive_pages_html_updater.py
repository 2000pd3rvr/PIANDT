#!/usr/bin/env python3
"""
Interactive updater for pages.html Page Content column.
Shows each page and allows you to update the Page Content column.

Enhancement:
- If the provided content is a direct image URL, the script will:
  - Download the image into the global images folder
  - Name the file to reflect the page URL
  - Insert an <img> tag into the Page Content column, styled to fit the column
"""
import re
import sys
from pathlib import Path
from html import escape, unescape
from urllib.parse import urlparse
from urllib.request import urlretrieve

BASE_DIR = Path(__file__).parent.parent
PAGES_HTML = Path(__file__).parent / "pages.html"
IMAGES_DIR = BASE_DIR / "images"

def parse_pages_html():
    """Parse pages.html and extract all page data"""
    with open(PAGES_HTML, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all table rows (skip header)
    # Updated pattern to handle empty content-col
    pattern = r'<tr>\s*<td class="num-col">(\d+)</td>\s*<td class="url-col"><a[^>]*>([^<]+)</a></td>\s*<td class="heading-col">([^<]*)</td>\s*<td class="desc-col">([^<]*(?:<[^>]+>[^<]*</[^>]+>[^<]*)*)</td>\s*<td class="content-col">([^<]*(?:<[^>]+>[^<]*</[^>]+>[^<]*)*)</td>\s*<td class="faq-col">'
    matches = re.findall(pattern, content, re.DOTALL)
    
    pages = []
    for match in matches:
        row_num, url, heading, description, page_content = match
        # Clean HTML from description and content
        desc_clean = re.sub(r'<[^>]+>', '', description)
        desc_clean = unescape(desc_clean).strip()
        content_clean = re.sub(r'<[^>]+>', '', page_content)
        content_clean = unescape(content_clean).strip()
        
        pages.append({
            'row': int(row_num),
            'url': url.strip(),
            'heading': heading.strip(),
            'description': desc_clean,
            'content': content_clean
        })
    
    return pages, content

def update_page_content_in_html(html_content, row_num, new_content):
    """Update the Page Content column for a specific row in pages.html"""
    # Find the row - match up to content-col, then replace content
    pattern = rf'(<tr>\s*<td class="num-col">{row_num}</td>\s*<td class="url-col"><a[^>]*>[^<]+</a></td>\s*<td class="heading-col">[^<]*</td>\s*<td class="desc-col">[^<]*(?:<[^>]+>[^<]*</[^>]+>[^<]*)*</td>\s*<td class="content-col">)([^<]*(?:<[^>]+>[^<]*</[^>]+>[^<]*)*)(</td>\s*<td class="faq-col">)'
    
    def replace_content(match):
        before = match.group(1)
        after = match.group(3)
        # If new_content looks like HTML (e.g. <img>), don't escape
        if "<" in new_content and ">" in new_content:
            safe_content = new_content
        else:
            # Escape plain text content
            safe_content = escape(new_content)
        return before + safe_content + after
def is_image_url(text: str) -> bool:
    """Check if the provided text is a direct image URL."""
    text = text.strip()
    if not text.lower().startswith(("http://", "https://")):
        return False
    return text.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"))


def generate_image_filename(page_url: str, image_url: str) -> str:
    """Generate a descriptive image filename based on the page URL and original extension."""
    # Use page URL path as base name
    slug = page_url.replace("/", "_").replace(".html", "")
    # Get extension from image URL
    parsed = urlparse(image_url)
    ext = Path(parsed.path).suffix or ".png"
    return f"{slug}_content{ext}"


def download_image_for_page(image_url: str, page_url: str, heading: str) -> str:
    """
    Download an image for the given page and return the relative src to use in pages.html.
    The image is saved into the global images folder and named to reflect the page.
    """
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    filename = generate_image_filename(page_url, image_url)
    dest_path = IMAGES_DIR / filename

    try:
        print(f"\n  🌐 Downloading image for {page_url} ...")
        urlretrieve(image_url, dest_path)
        print(f"  ✅ Image saved to {dest_path}")
    except Exception as e:
        print(f"  ❌ Failed to download image: {e}")
        return ""

    # From pages.html (in site_agent/) to images folder (at root), use ../images/...
    rel_src = f"../images/{filename}"
    alt_text = heading or page_url

    # Inline style to make it fit the content column
    img_html = (
        f'<img src="{rel_src}" alt="{escape(alt_text)}" '
        f'style="max-width:100%; height:auto; display:block; margin:0 auto;" />'
    )
    return img_html

    
    new_html = re.sub(pattern, replace_content, html_content, flags=re.DOTALL)
    return new_html

def main():
    print("="*70)
    print("INTERACTIVE PAGES.HTML CONTENT UPDATER")
    print("="*70)
    
    # Parse pages.html
    pages, html_content = parse_pages_html()
    total = len(pages)
    
    print(f"\nFound {total} pages in pages.html")
    print("\nThis script will show each page and allow you to update")
    print("the 'Page Content' column in pages.html")
    print("\nCommands:")
    print("  - Type your content (can be multiple paragraphs, separated by blank lines)")
    print("  - Type 'skip' to skip this page")
    print("  - Type 'quit' to exit and save progress")
    print("  - Type 'prev' to go back to previous page")
    print("="*70)
    
    current_index = 0
    original_html = html_content  # Keep original for safety
    
    while current_index < total:
        page = pages[current_index]
        
        print(f"\n\n{'='*70}")
        print(f"PAGE {current_index + 1} of {total}")
        print(f"{'='*70}")
        print(f"\n📄 URL: {page['url']}")
        print(f"📋 Heading: {page['heading']}")
        print(f"\n📝 Current Description (from descriptions.json):")
        desc_preview = page['description'][:300] + "..." if len(page['description']) > 300 else page['description']
        print(f"   {desc_preview}")
        
        print(f"\n📦 Current Page Content:")
        if page['content']:
            content_preview = page['content'][:200] + "..." if len(page['content']) > 200 else page['content']
            print(f"   {content_preview}")
        else:
            print("   (empty)")
        
        print("\n" + "-"*70)
        print("Enter new Page Content for this page:")
        print("  (Type your content - press Enter for new paragraph, blank line to finish)")
        print("  (Type 'skip' to skip, 'quit' to exit, 'prev' to go back)")
        print("-"*70)
        
        lines = []
        empty_line_count = 0
        command_entered = False
        
        while True:
            try:
                line = input()
                line_lower = line.strip().lower()
                
                if line_lower == 'quit':
                    # Save progress before exiting
                    with open(PAGES_HTML, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    print("\n" + "="*70)
                    print("EXITING - Your changes have been saved")
                    print("="*70)
                    print(f"\nCompleted: {current_index} of {total} pages")
                    sys.exit(0)
                elif line_lower == 'skip':
                    print(f"\n⏭️  Skipping {page['url']}")
                    command_entered = True
                    break
                elif line_lower == 'prev':
                    if current_index > 0:
                        current_index -= 1
                        print(f"\n⏮️  Going back to previous page...")
                        command_entered = True
                        break
                    else:
                        print("  ⚠️  Already at first page")
                        continue
                elif not line.strip():
                    # Empty line - if we have content, finish; otherwise continue
                    if lines:
                        empty_line_count += 1
                        if empty_line_count >= 1:  # One blank line finishes input
                            break
                else:
                    lines.append(line)
                    empty_line_count = 0
            except EOFError:
                if lines:
                    break
                else:
                    print("\nExiting...")
                    sys.exit(0)
            except KeyboardInterrupt:
                # Save progress before exiting
                with open(PAGES_HTML, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                print("\n\nExiting - changes saved...")
                sys.exit(0)
        
        if command_entered:
            if line_lower == 'skip':
                # Ask for confirmation before next page
                if current_index < total - 1:
                    next_page = pages[current_index + 1]
                    print(f"\nNext page: {next_page['url']}")
                    next_action = input("\nContinue to next page? (Enter/quit): ").strip().lower()
                    if next_action == 'quit':
                        with open(PAGES_HTML, 'w', encoding='utf-8') as f:
                            f.write(html_content)
                        print("\nExiting - changes saved...")
                        sys.exit(0)
                current_index += 1
            continue
        
        if not lines:
            print("  ⚠️  No content provided, skipping...")
            if current_index < total - 1:
                next_page = pages[current_index + 1]
                print(f"\nNext page: {next_page['url']}")
                next_action = input("\nContinue to next page? (Enter/quit): ").strip().lower()
                if next_action == 'quit':
                    with open(PAGES_HTML, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    print("\nExiting - changes saved...")
                    sys.exit(0)
            current_index += 1
            continue
        
        # Join lines into content
        new_content_raw = '\n\n'.join([line.strip() for line in lines if line.strip()])

        # Check if this is an image URL-only input
        new_content = new_content_raw
        if is_image_url(new_content_raw) and '\n' not in new_content_raw.strip():
            print("\n🖼  Detected image URL as Page Content.")
            img_html = download_image_for_page(new_content_raw.strip(), page['url'], page['heading'])
            if img_html:
                new_content = img_html
            else:
                print("  ❌ Image download failed. Keeping raw URL as text.")
        
        # Confirm
        print(f"\n📝 New Page Content preview (first 200 chars):")
        print(f"   {new_content[:200]}...")
        print(f"\n⚠️  This will update Page Content for: {page['url']}")
        confirm = input("   Continue? (y/n): ").strip().lower()
        
        if confirm != 'y':
            print("   Cancelled. Skipping...")
            if current_index < total - 1:
                next_page = pages[current_index + 1]
                print(f"\nNext page: {next_page['url']}")
                next_action = input("\nContinue to next page? (Enter/quit): ").strip().lower()
                if next_action == 'quit':
                    with open(PAGES_HTML, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    print("\nExiting - changes saved...")
                    sys.exit(0)
            current_index += 1
            continue
        
        # Update pages.html
        html_content = update_page_content_in_html(html_content, page['row'], new_content)
        
        # Save immediately
        with open(PAGES_HTML, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"\n  ✅ Updated Page Content for {page['url']}")
        print(f"  ✅ Saved to pages.html")
        
        # Ask for confirmation before moving to next page
        print("\n" + "="*70)
        print(f"✅ PAGE {current_index + 1} COMPLETED")
        print("="*70)
        
        if current_index < total - 1:
            next_page = pages[current_index + 1]
            print(f"\nNext page: {next_page['url']}")
            print(f"Next heading: {next_page['heading']}")
            print("\nOptions:")
            print("  - Press Enter to continue to next page")
            print("  - Type 'quit' to exit and save progress")
            print("  - Type 'prev' to go back and redo this page")
            
            next_action = input("\nContinue to next page? (Enter/quit/prev): ").strip().lower()
            
            if next_action == 'quit':
                print("\n" + "="*70)
                print("EXITING - Your changes have been saved")
                print("="*70)
                print(f"\nCompleted: {current_index + 1} of {total} pages")
                print(f"Remaining: {total - current_index - 1} pages")
                sys.exit(0)
            elif next_action == 'prev':
                # Stay on current page
                print(f"\n⏮️  Staying on current page. You can update it again.")
                continue
            else:
                current_index += 1
        else:
            # Last page completed
            print("\n" + "="*70)
            print("🎉 ALL PAGES COMPLETED!")
            print("="*70)
            current_index += 1
    
    print("\n" + "="*70)
    print("✅ ALL PAGES PROCESSED!")
    print("="*70)
    print(f"\n✅ Updated pages.html with Page Content for all {total} pages")
    print(f"✅ File saved: {PAGES_HTML}")

if __name__ == '__main__':
    main()

