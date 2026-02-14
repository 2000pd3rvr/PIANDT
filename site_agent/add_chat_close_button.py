#!/usr/bin/env python3
"""
Add chat close button to all HTML pages that have a chat window.
"""
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

def add_chat_close_button(file_path):
    """Add close button to chat window if it's missing."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if chat window exists
        if 'id="chatWindow"' not in content:
            return False
        
        # Check if close button already exists
        if 'id="chatClose"' in content:
            return False
        
        # Pattern to find the chat window opening tag
        # We want to add the header right after <div class="chat-window" id="chatWindow">
        pattern = r'(<div class="chat-window" id="chatWindow">)'
        
        if re.search(pattern, content):
            # Add the chat header with close button
            chat_header = '''        <div class="chat-header">
            <h3 class="chat-header-title">Chat Assistant</h3>
            <button class="chat-close" id="chatClose" aria-label="Close chat">×</button>
        </div>
'''
            # Replace the pattern with pattern + header
            new_content = re.sub(pattern, r'\1\n' + chat_header, content)
            
            # Only write if content changed
            if new_content != content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                return True
        
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Process all HTML files."""
    html_files = list(BASE_DIR.rglob('*.html'))
    updated_count = 0
    
    for html_file in html_files:
        # Skip pages.html and any files in xives
        if 'pages.html' in str(html_file) or 'xives' in str(html_file):
            continue
        
        if add_chat_close_button(html_file):
            updated_count += 1
            print(f"✅ Added close button to: {html_file.relative_to(BASE_DIR)}")
    
    print(f"\n{'='*60}")
    print(f"✅ Updated {updated_count} files with chat close button")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()

