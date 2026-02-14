#!/usr/bin/env python3
"""
Add Mistral training config script to all HTML pages.
"""
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

def add_mistral_script(file_path):
    """Add Mistral training config script if missing."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already has the script
        if 'mistral_training_config.js' in content:
            return False
        
        # Find script.js reference
        script_pattern = r'(<script\s+src=["\']([^"\']*script\.js[^"\']*)["\']>)'
        match = re.search(script_pattern, content, re.IGNORECASE)
        
        if match:
            # Calculate relative path to site_agent
            rel_path = file_path.relative_to(BASE_DIR)
            depth = str(rel_path).count('/')
            
            # Build path to mistral_training_config.js
            if depth == 0:
                mistral_path = 'site_agent/mistral_training_config.js'
            else:
                mistral_path = '../' * depth + 'site_agent/mistral_training_config.js'
            
            # Add mistral script before script.js
            mistral_script = f'    <script src="{mistral_path}"></script>\n'
            new_content = content.replace(match.group(0), mistral_script + '    ' + match.group(0))
            
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
        
        if add_mistral_script(html_file):
            updated_count += 1
            print(f"✅ Added Mistral training script to: {html_file.relative_to(BASE_DIR)}")
    
    print(f"\n{'='*60}")
    print(f"✅ Updated {updated_count} files with Mistral training script")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()

