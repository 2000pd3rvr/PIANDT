#!/usr/bin/env python3
"""
Fix duplicate descriptions in meta tags
"""
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

def fix_description(file_path):
    """Fix duplicate text in meta description"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find meta description
        pattern = r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']'
        match = re.search(pattern, content, re.IGNORECASE)
        
        if match:
            desc = match.group(1)
            # Check for duplicate patterns (look for repeated phrases)
            # Split by common sentence endings
            sentences = re.split(r'([.!?])\s+', desc)
            
            # Look for duplicate sentences
            seen = set()
            clean_sentences = []
            for i in range(0, len(sentences), 2):
                if i < len(sentences):
                    sentence = sentences[i]
                    if i + 1 < len(sentences):
                        sentence += sentences[i + 1]
                    
                    # Normalize and check for duplicates
                    normalized = sentence.strip().lower()[:50]  # First 50 chars
                    if normalized not in seen and len(sentence.strip()) > 10:
                        seen.add(normalized)
                        clean_sentences.append(sentence.strip())
            
            if len(clean_sentences) < len(sentences) // 2:
                # Reconstruct description
                new_desc = ' '.join(clean_sentences)
                # Remove any remaining obvious duplicates
                new_desc = re.sub(r'(.{20,}?)\1+', r'\1', new_desc)
                
                # Update in file
                new_content = re.sub(
                    pattern,
                    f'<meta name="description" content="{new_desc}"',
                    content,
                    flags=re.IGNORECASE
                )
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                return True
    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
    return False

def main():
    html_files = list(BASE_DIR.rglob("*.html"))
    html_files = [f for f in html_files if 'site_agent' not in str(f) and '.git' not in str(f)]
    
    fixed = 0
    for html_file in sorted(html_files):
        if fix_description(html_file):
            fixed += 1
            print(f"✓ Fixed: {html_file.relative_to(BASE_DIR)}")
    
    print(f"\n✅ Fixed {fixed} pages")

if __name__ == '__main__':
    main()

