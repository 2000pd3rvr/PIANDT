#!/usr/bin/env python3
"""
Process a single page with multi-sheet rules
Usage: python3 process_single_page.py <page_number>
"""

import re
import sys
from pathlib import Path

base_dir = Path(__file__).parent.parent
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
    """Process a single HTML file"""
    rel_path = file_path.relative_to(base_dir)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changes_made = []
    
    # 1. Add multi-sheet-pagination.js if missing
    if 'multi-sheet-pagination.js' not in content:
        script_pattern = r'(<script src="[^"]*script\.js[^"]*"></script>)'
        match = re.search(script_pattern, content)
        if match:
            depth = str(rel_path).count('/')
            pagination_script = '<script src="' + '../' * depth + 'multi-sheet-pagination.js"></script>\n    ' if depth > 0 else '<script src="multi-sheet-pagination.js"></script>\n    '
            content = content.replace(match.group(1), pagination_script + match.group(1))
            changes_made.append("Added multi-sheet-pagination.js")
    
    # 2. Process content-text
    content_text_pattern = r'(<div class="content-text"[^>]*>)(.*?)(</div>\s*</div>\s*</div>\s*</section>)'
    match = re.search(content_text_pattern, content, re.DOTALL)
    
    if not match:
        content_text_pattern = r'(<div class="content-text"[^>]*>)(.*?)(</div>\s*</div>\s*</div>)'
        match = re.search(content_text_pattern, content, re.DOTALL)
    
    if not match:
        content_text_pattern = r'(<div class="content-text"[^>]*>)(.*?)(</div>)'
        match = re.search(content_text_pattern, content, re.DOTALL)
    
    if match:
        div_start = match.group(1)
        div_content = match.group(2)
        div_end = match.group(3)
        
        if 'column-count' in div_start:
            div_start = re.sub(r'\s*column-count:\s*[^;]+;?', '', div_start)
            changes_made.append("Removed inline column-count")
        
        paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', div_content, re.DOTALL)
        
        if paragraphs:
            all_text = ' '.join([re.sub(r'<[^>]+>', ' ', p).strip() for p in paragraphs])
            all_text = re.sub(r'\s+', ' ', all_text).strip()
            
            new_paragraphs = split_text_into_paragraphs(all_text, TARGET_WORDS_PER_PARAGRAPH)
            
            while len(new_paragraphs) % 4 != 0 and len(new_paragraphs) > 0:
                new_paragraphs.append('')
            
            new_paragraphs_html = '\n                        '.join([f'<p>{p}</p>' if p else '<p></p>' for p in new_paragraphs])
            new_content_text = div_start + '\n                        ' + new_paragraphs_html + '\n                    ' + div_end
            content = content[:match.start()] + new_content_text + content[match.end():]
            
            changes_made.append(f"Split into {len(new_paragraphs)} paragraphs (~{TARGET_WORDS_PER_PARAGRAPH} words each)")
    
    # 3. Add chat agent if missing
    if 'chatAgentBtn' not in content and 'chatButton' not in content:
        body_close_pattern = r'(</body>)'
        if re.search(body_close_pattern, content):
            depth = str(rel_path).count('/')
            image_path = '../' * depth + 'images/agent.png' if depth > 0 else 'images/agent.png'
            chat_agent_html = f'''    <!-- Chat Agent Button -->
    <img src="{image_path}" alt="Speak to an agent" class="chat-agent-btn" id="chatAgentBtn">

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
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, changes_made
    return False, []

# Get all HTML files
html_files = []
for html_file in base_dir.rglob("*.html"):
    if 'site_agent' in str(html_file) or html_file.name == 'index.html':
        continue
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            if 'class="content-text"' in f.read():
                html_files.append(html_file)
    except:
        pass

html_files = sorted(html_files)

# Get page number from command line or default to 1
page_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1

if page_num > len(html_files):
    print(f"Error: Page number {page_num} exceeds total pages ({len(html_files)})")
    sys.exit(1)

file_path = html_files[page_num - 1]
rel_path = file_path.relative_to(base_dir)

print(f"Processing page {page_num} of {len(html_files)}: {rel_path}")

changed, changes = process_html_file(file_path)

if changed:
    print(f"✓ Changes made: {', '.join(changes)}")
else:
    print(f"- No changes needed")

print(f"\nTest URL: http://localhost:8000/{rel_path}")
print(f"Next page command: python3 site_agent/process_single_page.py {page_num + 1}")

