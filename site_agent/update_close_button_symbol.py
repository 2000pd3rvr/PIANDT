#!/usr/bin/env python3
"""
Update chat close button from × to - (minus sign).
"""
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

def update_close_button(file_path):
    """Update close button symbol from × to -."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if close button exists
        if 'id="chatClose"' not in content:
            return False
        
        # Replace × with - in the close button
        old_pattern = r'(<button class="chat-close" id="chatClose"[^>]*>)×</button>'
        new_content = re.sub(old_pattern, r'\1-</button>', content)
        
        # Also handle if there are any variations
        if '×' in content and 'chatClose' in content:
            # More flexible pattern
            old_pattern2 = r'(id="chatClose"[^>]*>)\s*×\s*(</button>)'
            new_content = re.sub(old_pattern2, r'\1-\2', new_content)
        
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
        
        if update_close_button(html_file):
            updated_count += 1
            print(f"✅ Updated: {html_file.relative_to(BASE_DIR)}")
    
    print(f"\n{'='*60}")
    print(f"✅ Updated {updated_count} files with minus sign")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()

