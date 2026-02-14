#!/usr/bin/env python3
"""
Check what content will be extracted from a page for pages.html.

Usage:
    python3 site_agent/check_page_extraction.py <page_path>
"""
import sys
from pathlib import Path

# Import extraction functions
BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR / 'site_agent'))

from update_pages_html import extract_all_page_content, extract_h1, extract_meta_description

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 site_agent/check_page_extraction.py <page_path>")
        print("\nExample:")
        print("  python3 site_agent/check_page_extraction.py in/about_piandt/in_about_piandt.html")
        sys.exit(1)
    
    page_path = Path(sys.argv[1])
    
    if not page_path.exists():
        print(f"❌ Error: Page not found: {page_path}")
        sys.exit(1)
    
    print("="*60)
    print(f"EXTRACTION PREVIEW: {page_path.name}")
    print("="*60)
    
    with open(page_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract components
    h1 = extract_h1(content)
    meta_desc = extract_meta_description(content)
    full_content = extract_all_page_content(content)
    
    print(f"\n📋 H1 Heading:")
    print(f"   {h1 if h1 else '❌ No H1 found'}")
    
    print(f"\n📝 Meta Description:")
    if meta_desc:
        print(f"   {meta_desc[:150]}..." if len(meta_desc) > 150 else f"   {meta_desc}")
    else:
        print("   ❌ No meta description found")
    
    print(f"\n📄 Full Content (for Page Description column):")
    if full_content and full_content != "No content found":
        print(f"   Length: {len(full_content)} characters")
        print(f"   Preview (first 300 chars):")
        print(f"   {full_content[:300]}...")
        print(f"\n   Full content will be used as 'Page Description' in pages.html")
    else:
        print("   ❌ No content found!")
        print("   Make sure your content is in:")
        print("   - <div class='content-text'> sections")
        print("   - <main>, <article>, or <section> tags")
    
    print("\n" + "="*60)
    print("💡 TIP: After updating this page, run:")
    print(f"   python3 site_agent/update_page_and_sync.py {page_path}")
    print("="*60)

if __name__ == '__main__':
    main()

