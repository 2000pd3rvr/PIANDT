#!/usr/bin/env python3
"""
Split all pages to have paragraphs of ~75 words each.
Each sheet will have 4 paragraphs (one per column).
"""

import re
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
TARGET_WORDS_PER_PARAGRAPH = 75

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

def process_html_file(file_path):
    """Process a single HTML file to split paragraphs into ~75 words each"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        changes_made = []
        
        # Pattern to match content-text div
        content_text_pattern = r'(<div[^>]*class="[^"]*content-text[^"]*"[^>]*>)(.*?)(</div>)'
        
        match = re.search(content_text_pattern, content, re.DOTALL)
        
        if match:
            div_start = match.group(1)
            div_content = match.group(2)
            div_end = match.group(3)
            
            # Extract text from paragraphs, preserving images
            paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', div_content, re.DOTALL)
            
            if paragraphs:
                # CRITICAL: Sequential approach - fill paragraph 1 to ~75 words, then paragraph 2, etc.
                # Don't redistribute - just fill sequentially. If last paragraph has 5 words, that's fine.
                
                # Step 1: Collect all words sequentially (preserving images)
                all_words = []
                image_paragraphs = []  # Store image paragraphs with their position
                
                for para_html in paragraphs:
                    # Check if paragraph contains an image
                    if '<img' in para_html:
                        # Store image paragraph - we'll insert it at the right position
                        image_paragraphs.append({'html': para_html, 'position': len(all_words)})
                    else:
                        # Extract words from regular paragraph
                        text_only = re.sub(r'<[^>]+>', ' ', para_html)
                        words = text_only.split()
                        all_words.extend(words)
                
                # Step 2: Build paragraphs sequentially - ~75 words each
                new_paragraphs = []
                current_para_words = []
                
                for word in all_words:
                    current_para_words.append(word)
                    
                    # When we reach ~75 words, finish this paragraph and start next
                    if len(current_para_words) >= TARGET_WORDS_PER_PARAGRAPH:
                        new_paragraphs.append(f'<p>{" ".join(current_para_words)}</p>')
                        current_para_words = []
                
                # Add remaining words as final paragraph (even if less than 75 words - that's fine!)
                if current_para_words:
                    new_paragraphs.append(f'<p>{" ".join(current_para_words)}</p>')
                
                # Step 3: Insert image paragraphs at appropriate positions
                # For now, insert images at the end of the paragraph list
                for img_para in image_paragraphs:
                    new_paragraphs.append(f"<p>{img_para['html']}</p>")
                
                # Step 4: Group into sets of 4 paragraphs per sheet
                # Pad with empty paragraphs to make complete sheets (multiples of 4)
                while len(new_paragraphs) % 4 != 0:
                    new_paragraphs.append('<p></p>')
                
                # Create new paragraph HTML
                new_paragraphs_html = '\n                        '.join(new_paragraphs)
                
                # Replace content
                new_content_text = div_start + '\n                        ' + new_paragraphs_html + '\n                    ' + div_end
                content = content[:match.start()] + new_content_text + content[match.end():]
                
                changes_made.append(f"Split content into {len(new_paragraphs)} paragraphs (~{TARGET_WORDS_PER_PARAGRAPH} words each)")
            else:
                print(f"  ⚠️  No paragraphs found in content-text")
        else:
            print(f"  ⚠️  No content-text div found")
            return False
        
        if changes_made:
            # Write back
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        else:
            return False
            
    except Exception as e:
        print(f"  ✗ Error processing {file_path}: {e}")
        return False

def main():
    """Process all HTML files in in/, processing/, and out/ directories"""
    files_processed = 0
    files_updated = 0
    
    # Find all HTML files in the three directories
    for triad_dir in ['in', 'processing', 'out']:
        triad_path = BASE_DIR / triad_dir
        if not triad_path.exists():
            continue
        
        for html_file in triad_path.rglob('*.html'):
            # Process all HTML files including main pages
            pass
            
            files_processed += 1
            rel_path = html_file.relative_to(BASE_DIR)
            print(f"Processing {rel_path}...")
            
            if process_html_file(html_file):
                files_updated += 1
                print(f"  ✓ Updated")
            else:
                print(f"  - No changes needed")
    
    print(f"\n{'='*60}")
    print(f"Summary: {files_updated}/{files_processed} files updated")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()

