#!/usr/bin/env python3
"""
Split a single paragraph into multiple paragraphs, each sized to fill one column (20 lines).
Each paragraph should contain approximately 70 words.
"""

import re

def split_content_into_paragraphs(html_content, words_per_paragraph=70):
    """
    Split HTML content into multiple paragraphs, preserving <strong> tags.
    Each paragraph should contain approximately words_per_paragraph words.
    """
    html_content = html_content.strip()
    
    # Extract plain text to count words
    text_only = re.sub(r'<[^>]+>', '', html_content)
    total_words = len(text_only.split())
    
    # Split by sentences first (preserving HTML)
    # Pattern: sentence ending followed by space and optional strong tag
    sentence_pattern = r'([^.!?]+[.!?]+)\s*(?=<strong|$)'
    sentences = []
    
    # First, extract strong tags and their positions
    strong_tags = []
    for match in re.finditer(r'<strong[^>]*>.*?</strong>', html_content, re.DOTALL):
        strong_tags.append({
            'start': match.start(),
            'end': match.end(),
            'html': match.group(0)
        })
    
    # Split text by sentences, preserving strong tags
    current_pos = 0
    segments = []
    
    # Split by periods, exclamation marks, and question marks
    text_parts = re.split(r'([.!?]+\s+)', html_content)
    
    # Reconstruct sentences with their HTML
    current_sentence = []
    current_word_count = 0
    
    for part in text_parts:
        if not part.strip():
            continue
            
        # Count words in this part (excluding HTML tags)
        part_text = re.sub(r'<[^>]+>', '', part)
        part_words = len(part_text.split())
        
        current_sentence.append(part)
        current_word_count += part_words
        
        # If we've reached a sentence boundary and have enough words, consider splitting
        if part.strip().endswith(('.', '!', '?')) and current_word_count >= 30:
            # Check if adding next part would exceed limit
            segments.append({
                'html': ''.join(current_sentence),
                'words': current_word_count
            })
            current_sentence = []
            current_word_count = 0
    
    # Add remaining
    if current_sentence:
        segments.append({
            'html': ''.join(current_sentence),
            'words': current_word_count
        })
    
    # Now group segments into paragraphs of ~70 words
    paragraphs = []
    current_para = []
    current_words = 0
    
    for segment in segments:
        if current_words + segment['words'] > words_per_paragraph * 1.1 and current_para and current_words >= 50:
            # Start new paragraph
            paragraphs.append(' '.join(seg['html'] for seg in current_para))
            current_para = [segment]
            current_words = segment['words']
        else:
            current_para.append(segment)
            current_words += segment['words']
    
    if current_para:
        paragraphs.append(' '.join(seg['html'] for seg in current_para))
    
    return paragraphs

# Read the HTML file
html_file = '/Users/pd3rvr/Documents/pubs/THESIS/thetex/PIANDT/in/about_piandt/in_trustees.html'

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the paragraph content - get everything between content-text div tags
match = re.search(r'<div class="content-text"[^>]*>(.*?)</div>', content, flags=re.DOTALL)
if match:
    content_html = match.group(1).strip()
    
    # Remove all existing <p> tags
    content_html = re.sub(r'</?p>', '', content_html).strip()
    
    # Split into paragraphs
    paragraphs = split_content_into_paragraphs(content_html, words_per_paragraph=70)
    
    # Filter out empty paragraphs and clean up
    paragraphs = [p.strip() for p in paragraphs if p.strip() and len(re.sub(r'<[^>]+>', '', p).split()) > 0]
    
    # Reconstruct the HTML
    paragraphs_html = '\n                        '.join(f'<p>{p}</p>' for p in paragraphs)
    
    # Replace the content
    new_content = re.sub(
        r'(<div class="content-text"[^>]*>).*?(</div>)',
        r'\1\n                        ' + paragraphs_html + '\n                    \2',
        content,
        flags=re.DOTALL
    )
    
    # Write back
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Split content into {len(paragraphs)} paragraphs")
    for i, para in enumerate(paragraphs, 1):
        word_count = len(re.sub(r'<[^>]+>', '', para).split())
        print(f"Paragraph {i}: {word_count} words")
else:
    print("Could not find content-text div")
