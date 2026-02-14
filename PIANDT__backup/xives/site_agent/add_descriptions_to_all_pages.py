#!/usr/bin/env python3
"""
Add meta descriptions to all pages that are missing them.
Extract descriptions from page content (first paragraph from content-text).
"""

import re
from pathlib import Path
from html import escape, unescape

BASE_DIR = Path(__file__).parent.parent

def extract_content_text(html_content):
    """Extract text from content-text div"""
    pattern = r'<div[^>]*class=["\']content-text[^>]*>(.*?)</div>'
    match = re.search(pattern, html_content, re.DOTALL | re.IGNORECASE)
    if match:
        content = match.group(1)
        # Extract text from paragraphs
        para_pattern = r'<p[^>]*>(.*?)</p>'
        paragraphs = re.findall(para_pattern, content, re.DOTALL)
        # Clean HTML tags and get text
        text_paragraphs = []
        for para in paragraphs:
            text = re.sub(r'<[^>]+>', '', para)
            text = unescape(text).strip()
            if text and len(text) > 20:  # Only non-empty paragraphs
                text_paragraphs.append(text)
        return ' '.join(text_paragraphs[:2])  # First 2 paragraphs
    return None

def extract_meta_description(html_content):
    """Check if meta description exists"""
    pattern = r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']'
    match = re.search(pattern, html_content, re.IGNORECASE)
    return match is not None

def add_meta_description(html_content, description):
    """Add or update meta description tag"""
    # Limit description to 160 characters for SEO
    if len(description) > 160:
        description = description[:157] + '...'
    
    description_escaped = escape(description)
    
    # Check if meta description already exists
    pattern = r'<meta\s+name=["\']description["\']\s+content=["\'][^"\']+["\']'
    if re.search(pattern, html_content, re.IGNORECASE):
        # Update existing
        html_content = re.sub(
            pattern,
            f'<meta name="description" content="{description_escaped}"',
            html_content,
            flags=re.IGNORECASE
        )
    else:
        # Add new meta description after charset/viewport
        # Find the position after viewport meta tag
        viewport_pattern = r'(<meta\s+name=["\']viewport["\'][^>]+>)'
        if re.search(viewport_pattern, html_content, re.IGNORECASE):
            html_content = re.sub(
                viewport_pattern,
                f'\\1\n    <meta name="description" content="{description_escaped}">',
                html_content,
                flags=re.IGNORECASE
            )
        else:
            # Fallback: add after charset
            charset_pattern = r'(<meta\s+charset=["\']UTF-8["\']>)'
            if re.search(charset_pattern, html_content, re.IGNORECASE):
                html_content = re.sub(
                    charset_pattern,
                    f'\\1\n    <meta name="description" content="{description_escaped}">',
                    html_content,
                    flags=re.IGNORECASE
                )
            else:
                # Last resort: add after <head>
                html_content = re.sub(
                    r'(<head[^>]*>)',
                    f'\\1\n    <meta name="description" content="{description_escaped}">',
                    html_content,
                    flags=re.IGNORECASE
                )
    
    return html_content

def process_all_pages():
    """Process all HTML pages to add descriptions"""
    print("="*60)
    print("ADDING DESCRIPTIONS TO ALL PAGES")
    print("="*60)
    
    html_files = []
    for html_file in BASE_DIR.rglob('*.html'):
        if 'site_agent' in str(html_file):
            continue
        html_files.append(html_file)
    
    html_files.sort(key=lambda x: str(x.relative_to(BASE_DIR)))
    
    updated_count = 0
    skipped_count = 0
    error_count = 0
    
    for html_file in html_files:
        rel_path = html_file.relative_to(BASE_DIR)
        
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if already has description
            if extract_meta_description(content):
                skipped_count += 1
                continue
            
            # Extract description from content
            description = extract_content_text(content)
            
            if not description:
                # Try to get from title or h1
                title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
                h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
                
                if h1_match:
                    h1_text = re.sub(r'<[^>]+>', '', h1_match.group(1)).strip()
                    # Generate description based on h1 and triad
                    if 'Incoming Signals' in h1_text or 'In' in str(rel_path):
                        description = f"{h1_text}. This section captures and documents all incoming signals, requests, and new initiatives related to this topic."
                    elif 'In Progress' in h1_text or 'processing' in str(rel_path):
                        description = f"{h1_text}. This section documents the processing, analysis, and development of initiatives related to this topic."
                    elif 'Delivered Outputs' in h1_text or 'Out' in str(rel_path):
                        description = f"{h1_text}. This section presents the delivered outputs, results, and outcomes related to this topic."
                    else:
                        description = f"{h1_text}. Information about this topic in the PIANDT triadic information architecture."
                elif title_match:
                    title_text = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
                    description = f"{title_text}. Information about this topic in the PIANDT triadic information architecture."
                else:
                    description = "PIANDT - People, Innovation, and Technology for public benefit."
            
            # Add meta description
            content = add_meta_description(content, description)
            
            # Write back
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            updated_count += 1
            print(f"  ✓ Added description to {rel_path}")
            
        except Exception as e:
            error_count += 1
            print(f"  ⚠️  Error processing {rel_path}: {e}")
    
    print("\n" + "="*60)
    print(f"✅ COMPLETE!")
    print(f"   Updated: {updated_count} pages")
    print(f"   Skipped (already had): {skipped_count} pages")
    print(f"   Errors: {error_count} pages")
    print("="*60)

if __name__ == '__main__':
    process_all_pages()

