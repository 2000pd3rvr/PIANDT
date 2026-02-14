#!/usr/bin/env python3
"""
Split content into paragraphs where each paragraph has ~80 words to fill one column.
Each column should be one paragraph.
"""

import re

# Read the HTML file
html_file = '/Users/pd3rvr/Documents/pubs/THESIS/thetex/PIANDT/in/about_piandt/in_trustees.html'

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the content-text section
match = re.search(r'<div class="content-text"[^>]*>(.*?)</div>', content, flags=re.DOTALL)
if match:
    content_html = match.group(1).strip()
    
    # Remove all existing <p> tags to get clean text
    content_html = re.sub(r'</?p>', '', content_html).strip()
    
    # Get all text content to count words
    full_text = re.sub(r'<[^>]+>', '', content_html)
    words = full_text.split()
    total_words = len(words)
    
    # Target: 80 words per paragraph
    words_per_paragraph = 80
    target_paragraphs = max(1, round(total_words / words_per_paragraph))
    
    # Split by sentences first (preserving HTML structure)
    # Strategy: Split HTML while preserving strong tags, then group sentences into paragraphs
    
    # First, extract all text segments with their HTML
    segments = []
    current_segment = ''
    
    # Split by strong tags to preserve them
    parts = re.split(r'(<strong[^>]*>.*?</strong>)', content_html, flags=re.DOTALL)
    
    for part in parts:
        if not part.strip():
            continue
        
        # Split part into sentences
        sentences = re.split(r'([.!?]+\s+)', part)
        
        for i in range(0, len(sentences), 2):
            if i < len(sentences):
                sentence = sentences[i]
                if i + 1 < len(sentences):
                    sentence += sentences[i + 1]
                
                if sentence.strip():
                    # Count words in this sentence
                    sentence_text = re.sub(r'<[^>]+>', '', sentence)
                    word_count = len(sentence_text.split())
                    
                    segments.append({
                        'html': sentence,
                        'text': sentence_text,
                        'words': word_count
                    })
    
    # Now group segments into paragraphs of ~80 words
    paragraphs = []
    current_para = []
    current_words = 0
    
    for segment in segments:
        # Check if adding this segment would exceed 80 words
        if current_words + segment['words'] > words_per_paragraph * 1.15 and current_para and current_words >= 60:
            # Save current paragraph
            paragraphs.append(' '.join(seg['html'] for seg in current_para))
            current_para = [segment]
            current_words = segment['words']
        else:
            current_para.append(segment)
            current_words += segment['words']
    
    # Add last paragraph
    if current_para:
        paragraphs.append(' '.join(seg['html'] for seg in current_para))
    
    # Balance paragraphs better - if some are too small or too large, redistribute
    # Recalculate target based on actual paragraphs
    if paragraphs:
        total_para_words = sum(len(re.sub(r'<[^>]+>', '', p).split()) for p in paragraphs)
        avg_words = total_para_words / len(paragraphs)
        
        # If average is far from 80, try to balance better
        if avg_words < 70 or avg_words > 90:
            # Redistribute: merge small paragraphs, split large ones
            balanced = []
            i = 0
            while i < len(paragraphs):
                para = paragraphs[i]
                para_words = len(re.sub(r'<[^>]+>', '', para).split())
                
                if para_words < 60 and i + 1 < len(paragraphs):
                    # Merge with next paragraph if it won't exceed 100 words
                    next_para = paragraphs[i + 1]
                    next_words = len(re.sub(r'<[^>]+>', '', next_para).split())
                    if para_words + next_words <= 100:
                        balanced.append(para + ' ' + next_para)
                        i += 2
                        continue
                
                if para_words > 100:
                    # Split large paragraph
                    para_segments = re.split(r'([.!?]+\s+)', para)
                    current_split = []
                    current_split_words = 0
                    
                    for j in range(0, len(para_segments), 2):
                        if j < len(para_segments):
                            sent = para_segments[j]
                            if j + 1 < len(para_segments):
                                sent += para_segments[j + 1]
                            
                            if sent.strip():
                                sent_words = len(re.sub(r'<[^>]+>', '', sent).split())
                                
                                if current_split_words + sent_words > words_per_paragraph * 1.1 and current_split:
                                    balanced.append(' '.join(current_split))
                                    current_split = [sent]
                                    current_split_words = sent_words
                                else:
                                    current_split.append(sent)
                                    current_split_words += sent_words
                    
                    if current_split:
                        balanced.append(' '.join(current_split))
                else:
                    balanced.append(para)
                
                i += 1
            
            paragraphs = balanced
    
    # Clean up paragraphs
    paragraphs = [p.strip() for p in paragraphs if p.strip() and len(re.sub(r'<[^>]+>', '', p).split()) > 0]
    
    # Reconstruct HTML
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
    
    print(f"Split content into {len(paragraphs)} paragraphs (~80 words each)")
    for i, para in enumerate(paragraphs, 1):
        word_count = len(re.sub(r'<[^>]+>', '', para).split())
        print(f"Paragraph {i}: {word_count} words")
else:
    print("Could not find content-text div")
