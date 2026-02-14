#!/usr/bin/env python3
"""
Apply multi-sheet pagination rules to all HTML pages:
1. Ensure multi-sheet-pagination.js is included
2. Split content into paragraphs with ~75 words each
3. Ensure 4 paragraphs per sheet
4. Remove inline column-count from content-text div
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
    # Remove HTML tags for word counting
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
    
    # Add remaining words
    if current_para:
        paragraphs.append(' '.join(current_para))
    
    return paragraphs

def process_html_file(file_path):
    """Process a single HTML file to apply sheet rules"""
    print(f"\nProcessing: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changes_made = []
    
    # 1. Check if multi-sheet-pagination.js is included
    if 'multi-sheet-pagination.js' not in content:
        # Find where script.js is included
        script_pattern = r'(<script src="[^"]*script\.js[^"]*"></script>)'
        match = re.search(script_pattern, content)
        if match:
            # Add multi-sheet-pagination.js before script.js
            pagination_script = '<script src="../../multi-sheet-pagination.js"></script>\n    '
            # Calculate relative path depth
            depth = str(file_path.relative_to(base_dir)).count('/')
            if depth > 0:
                pagination_script = '<script src="' + '../' * depth + 'multi-sheet-pagination.js"></script>\n    '
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
        div_start = match.group(1)
        div_content = match.group(2)
        div_end = match.group(3)
        
        # Remove inline column-count from div_start
        if 'column-count' in div_start:
            div_start = re.sub(r'\s*column-count:\s*[^;]+;?', '', div_start)
            changes_made.append("Removed inline column-count")
        
        # Extract text from paragraphs
        paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', div_content, re.DOTALL)
        
        if paragraphs:
            # Combine all paragraph text
            all_text = ' '.join([re.sub(r'<[^>]+>', ' ', p).strip() for p in paragraphs])
            all_text = re.sub(r'\s+', ' ', all_text).strip()
            
            # Split into paragraphs of ~75 words
            new_paragraphs = split_text_into_paragraphs(all_text, TARGET_WORDS_PER_PARAGRAPH)
            
            # Ensure we have multiples of 4 paragraphs (4 per sheet)
            # Pad with empty paragraphs if needed
            while len(new_paragraphs) % 4 != 0 and len(new_paragraphs) > 0:
                new_paragraphs.append('')
            
            # Create new paragraph HTML
            new_paragraphs_html = '\n                        '.join([f'<p>{p}</p>' if p else '<p></p>' for p in new_paragraphs])
            
            # Replace content
            new_content_text = div_start + '\n                        ' + new_paragraphs_html + '\n                    ' + div_end
            content = content[:match.start()] + new_content_text + content[match.end():]
            
            changes_made.append(f"Split content into {len(new_paragraphs)} paragraphs (~{TARGET_WORDS_PER_PARAGRAPH} words each)")
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
        print(f"  - No changes needed")
        return False

# Get all HTML files with content-text
html_files = []
for html_file in base_dir.rglob("*.html"):
    # Skip site_agent and other non-content directories
    if 'site_agent' in str(html_file) or 'index.html' in str(html_file):
        continue
    
    # Check if file has content-text
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            if 'class="content-text"' in f.read():
                html_files.append(html_file)
    except:
        pass

print(f"Found {len(html_files)} HTML files with content-text")
print("\nStarting with a few key pages for testing...")

# Start with a few key pages
key_pages = [
    'in/about_piandt/in_about_piandt.html',
    'in/about_piandt/in_mission_vision.html',
    'in/about_piandt/in_charitable_purposes.html',
]

for page in key_pages:
    file_path = base_dir / page
    if file_path.exists():
        process_html_file(file_path)
    else:
        print(f"\n⚠️  File not found: {page}")

print("\n✓ Initial batch complete. Test these pages and let me know if they look good!")


