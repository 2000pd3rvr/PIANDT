#!/usr/bin/env python3
"""
Apply multi-sheet pagination to all pages that don't have it yet.
Ensure:
- 4 columns per sheet
- Each page has at least one sheet
- Each paragraph fits into one column only
- ~75 words per paragraph per column
- Each sheet contains 4 columns (1 paragraph per column)
"""

import re
import os
from pathlib import Path

# Base directory
base_dir = Path(__file__).parent.parent

# Target: 75 words per paragraph
TARGET_WORDS_PER_PARAGRAPH = 75

def count_words(text):
    """Count words in text (excluding HTML tags)"""
    text_only = re.sub(r'<[^>]+>', ' ', text)
    words = text_only.split()
    return len([w for w in words if w.strip()])

def split_text_into_paragraphs(text, target_words=75):
    """Split text into paragraphs of approximately target_words each"""
    text_only = re.sub(r'<[^>]+>', ' ', text)
    words = text_only.split()
    
    if not words:
        return []
    
    paragraphs = []
    current_para = []
    current_count = 0
    
    for word in words:
        current_para.append(word)
        current_count += 1
        
        if current_count >= target_words:
            paragraphs.append(' '.join(current_para))
            current_para = []
            current_count = 0
    
    if current_para:
        paragraphs.append(' '.join(current_para))
    
    return paragraphs

def calculate_relative_path_depth(file_path):
    """Calculate relative path depth from base_dir"""
    rel_path = file_path.relative_to(base_dir)
    depth = len(rel_path.parts) - 1
    return '../' * depth if depth > 0 else './'

def process_html_file(file_path):
    """Process a single HTML file to apply sheet rules"""
    rel_path = str(file_path.relative_to(base_dir))
    print(f"\n{'='*80}")
    print(f"Processing: {rel_path}")
    print(f"{'='*80}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changes_made = []
    
    # 1. Check if multi-sheet-pagination.js is included
    has_pagination_script = 'multi-sheet-pagination.js' in content
    
    if not has_pagination_script:
        # Find where script.js is included
        script_pattern = r'(<script src="[^"]*script\.js[^"]*"></script>)'
        match = re.search(script_pattern, content)
        if match:
            # Calculate relative path
            depth = len(file_path.relative_to(base_dir).parts) - 1
            if depth == 0:
                pagination_path = 'multi-sheet-pagination.js'
            else:
                pagination_path = '../' * depth + 'multi-sheet-pagination.js'
            
            pagination_script = f'<script src="{pagination_path}"></script>\n    '
            content = content.replace(match.group(1), pagination_script + match.group(1))
            changes_made.append("Added multi-sheet-pagination.js")
        else:
            print(f"  ⚠️  Could not find script.js to add multi-sheet-pagination.js")
    
    # 2. Find content-text div and process its content
    content_text_pattern = r'(<div class="content-text"[^>]*>)(.*?)(</div>\s*</div>\s*</div>\s*</section>)'
    match = re.search(content_text_pattern, content, re.DOTALL)
    
    if not match:
        # Try simpler pattern
        content_text_pattern = r'(<div class="content-text"[^>]*>)(.*?)(</div>)'
        match = re.search(content_text_pattern, content, re.DOTALL)
        if match:
            # Find the closing tags
            remaining = content[match.end():]
            # Look for closing divs and section
            end_match = re.search(r'(</div>\s*</div>\s*</div>\s*</section>)', remaining)
            if end_match:
                match = re.search(content_text_pattern + r'.*?' + re.escape(end_match.group(1)), content, re.DOTALL)
    
    if match:
        div_start = match.group(1)
        div_content = match.group(2)
        div_end = match.group(3) if len(match.groups()) > 2 else '</div>'
        
        # Remove inline column-count from div_start
        if 'column-count' in div_start:
            div_start = re.sub(r'\s*column-count:\s*[^;]+;?', '', div_start)
            changes_made.append("Removed inline column-count")
        
        # Extract text from paragraphs
        paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', div_content, re.DOTALL)
        
        if paragraphs:
            # Combine all paragraph text (preserve strong tags)
            all_text_parts = []
            for para in paragraphs:
                # Keep HTML structure but extract text for word counting
                text_only = re.sub(r'<[^>]+>', ' ', para).strip()
                text_only = re.sub(r'\s+', ' ', text_only)
                if text_only:
                    all_text_parts.append(para)  # Keep original HTML
            
            # Combine and split into ~75 word paragraphs
            combined_text = ' '.join([re.sub(r'<[^>]+>', ' ', p).strip() for p in all_text_parts])
            combined_text = re.sub(r'\s+', ' ', combined_text).strip()
            
            # Split into paragraphs of ~75 words
            new_paragraphs = split_text_into_paragraphs(combined_text, TARGET_WORDS_PER_PARAGRAPH)
            
            # Ensure we have multiples of 4 paragraphs (4 per sheet)
            # Pad with empty paragraphs if needed
            while len(new_paragraphs) % 4 != 0 and len(new_paragraphs) > 0:
                new_paragraphs.append('')
            
            # Ensure at least 4 paragraphs (1 sheet minimum)
            if len(new_paragraphs) == 0:
                new_paragraphs = ['', '', '', '']
            
            # Try to preserve strong tags from original
            # For now, create simple paragraphs
            new_paragraphs_html = []
            for para_text in new_paragraphs:
                if para_text:
                    new_paragraphs_html.append(f'<p>{para_text}</p>')
                else:
                    new_paragraphs_html.append('<p></p>')
            
            new_paragraphs_html_str = '\n                        '.join(new_paragraphs_html)
            
            # Replace content
            new_content_text = div_start + '\n                        ' + new_paragraphs_html_str + '\n                    ' + div_end
            content = content[:match.start()] + new_content_text + content[match.end():]
            
            changes_made.append(f"Split content into {len(new_paragraphs)} paragraphs (~{TARGET_WORDS_PER_PARAGRAPH} words each, {len(new_paragraphs)//4} sheet(s))")
        else:
            print(f"  ⚠️  No paragraphs found in content-text")
    else:
        print(f"  ⚠️  No content-text div found")
    
    if changes_made:
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Changes: {', '.join(changes_made)}")
        return True
    else:
        print(f"  - No changes needed (already has pagination)")
        return False

# Get all HTML files with content-text
html_files = []
for html_file in base_dir.rglob("*.html"):
    # Skip site_agent, index.html, and other non-content directories
    if 'site_agent' in str(html_file) or html_file.name == 'index.html':
        continue
    
    # Check if file has content-text
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            if 'class="content-text"' in f.read():
                html_files.append(html_file)
    except:
        pass

print(f"Found {len(html_files)} HTML files with content-text")
print(f"\nChecking which pages already have multi-sheet-pagination.js...")

# Check which already have pagination
pages_with_pagination = []
pages_without_pagination = []

for html_file in html_files:
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'multi-sheet-pagination.js' in content:
                pages_with_pagination.append(html_file)
            else:
                pages_without_pagination.append(html_file)
    except:
        pass

print(f"Pages WITH pagination: {len(pages_with_pagination)}")
print(f"Pages WITHOUT pagination: {len(pages_without_pagination)}")

if pages_without_pagination:
    print(f"\n{'='*80}")
    print(f"Processing first batch of {min(5, len(pages_without_pagination))} pages for testing...")
    print(f"{'='*80}")
    
    # Process first 5 pages for testing
    for page in pages_without_pagination[:5]:
        process_html_file(page)
    
    print(f"\n✓ First batch complete. Test these pages and let me know if they look good!")
    print(f"Remaining pages: {len(pages_without_pagination) - min(5, len(pages_without_pagination))}")
else:
    print("\n✓ All pages already have pagination!")


