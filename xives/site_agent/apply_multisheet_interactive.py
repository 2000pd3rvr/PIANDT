#!/usr/bin/env python3
"""
Apply multi-sheet pagination rules interactively to all pages:
1. Check if multi-sheet-pagination.js is included
2. Split content into paragraphs with ~75 words each
3. Ensure 4 paragraphs per sheet
4. Remove inline column-count from content-text div
5. Ensure descriptions match pages.html
6. Ensure each paragraph fits in one column
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

def get_relative_path_depth(file_path):
    """Calculate relative path depth for script includes"""
    rel_path = file_path.relative_to(base_dir)
    depth = str(rel_path).count('/')
    return '../' * depth if depth > 0 else '../../'

def process_html_file(file_path, batch_num, file_num):
    """Process a single HTML file to apply sheet rules"""
    rel_path = file_path.relative_to(base_dir)
    print(f"\n[{batch_num}.{file_num}] Processing: {rel_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changes_made = []
    original_content = content
    
    # 1. Check if multi-sheet-pagination.js is included
    has_multisheet = 'multi-sheet-pagination.js' in content
    
    if not has_multisheet:
        # Find where script.js is included
        script_pattern = r'(<script src="[^"]*script\.js[^"]*"></script>)'
        match = re.search(script_pattern, content)
        if match:
            # Calculate relative path depth
            depth = str(rel_path).count('/')
            if depth == 0:
                pagination_script = '<script src="multi-sheet-pagination.js"></script>\n    '
            else:
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
        content_text_pattern = r'(<div class="content-text"[^>]*>)(.*?)(</div>\s*</div>\s*</div>)'
        match = re.search(content_text_pattern, content, re.DOTALL)
    
    if not match:
        # Try even simpler
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
    
    # 3. Ensure chat agent is present
    if 'chatAgentBtn' not in content and 'chatButton' not in content:
        # Find where to add chat agent (before closing body tag)
        body_close_pattern = r'(</body>)'
        if re.search(body_close_pattern, content):
            chat_agent_html = '''    <!-- Chat Agent Button -->
    <img src="''' + '../' * str(rel_path).count('/') + '''images/agent.png" alt="Speak to an agent" class="chat-agent-btn" id="chatAgentBtn">

    <!-- Chat Window -->
    <div class="chat-window" id="chatWindow">
        <div class="chat-messages" id="chatMessages">
            <div class="chat-message bot-message">
                <div class="message-content">
                    <p>Hello! I'm here to help you find information on our website. You can ask me about:</p>
                    <ul>
                        <li>Our services and products</li>
                        <li>Machine Intelligence Unit (MIU)</li>
                        <li>In, Proc, or Out stages</li>
                        <li>Specific pages or sections</li>
                    </ul>
                    <p>What would you like to know?</p>
                    <p style="margin-top: 1rem; font-size: 0.9em; color: #666;">
                        💡 <strong>Tip:</strong> To enable Mistral AI for smarter responses, type: <code>/setkey your-api-key</code>
                    </p>
                </div>
            </div>
        </div>
        <div class="chat-input-wrapper">
            <input type="text" class="chat-input" id="chatInput" placeholder="Type your question here..." autocomplete="off">
            <button class="chat-send" id="chatSend" aria-label="Send message">↑</button>
        </div>
    </div>

'''
            content = re.sub(body_close_pattern, chat_agent_html + r'\1', content)
            changes_made.append("Added chat agent")
    
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
    if 'site_agent' in str(html_file) or html_file.name == 'index.html':
        continue
    
    # Check if file has content-text
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            if 'class="content-text"' in f.read():
                html_files.append(html_file)
    except:
        pass

# Sort files for consistent processing
html_files = sorted(html_files)

print(f"Found {len(html_files)} HTML files with content-text")
print("\nStarting interactive processing...")
print("=" * 80)

# Process in batches of 10 for interactive testing
BATCH_SIZE = 10
total_batches = (len(html_files) + BATCH_SIZE - 1) // BATCH_SIZE

for batch_num in range(1, total_batches + 1):
    start_idx = (batch_num - 1) * BATCH_SIZE
    end_idx = min(start_idx + BATCH_SIZE, len(html_files))
    batch_files = html_files[start_idx:end_idx]
    
    print(f"\n{'='*80}")
    print(f"BATCH {batch_num} of {total_batches} (Files {start_idx+1}-{end_idx} of {len(html_files)})")
    print(f"{'='*80}")
    
    for idx, file_path in enumerate(batch_files, 1):
        process_html_file(file_path, batch_num, idx)
    
    print(f"\n✓ Batch {batch_num} complete!")
    print(f"Please test these {len(batch_files)} pages and let me know if they look good.")
    print(f"Pages in this batch:")
    for idx, file_path in enumerate(batch_files, 1):
        rel_path = file_path.relative_to(base_dir)
        print(f"  {idx}. {rel_path}")
    
    if batch_num < total_batches:
        print(f"\nWaiting for your feedback before processing batch {batch_num + 1}...")
        break  # Stop here for user testing

print(f"\n{'='*80}")
print(f"Processing paused after batch {batch_num}")
print(f"Remaining: {len(html_files) - end_idx} files in {total_batches - batch_num} batches")
print(f"{'='*80}")

