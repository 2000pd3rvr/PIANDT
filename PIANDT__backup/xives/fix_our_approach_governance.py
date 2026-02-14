#!/usr/bin/env python3
"""
Fix in_our_approach.html and in_governance.html:
- Split text into paragraphs with ~75 words each
- Ensure 4 paragraphs per sheet
- Add spaces where missing
"""

import re
from pathlib import Path

base_dir = Path(__file__).parent.parent
TARGET_WORDS_PER_PARAGRAPH = 75

def add_spaces_to_text(text):
    """Add spaces between words that are concatenated"""
    # Add space before capital letters that follow lowercase (word boundaries)
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    # Add space after periods, colons, etc. if missing
    text = re.sub(r'([.:,])([A-Za-z])', r'\1 \2', text)
    return text

def split_text_into_paragraphs(text, target_words=75):
    """Split text into paragraphs of approximately target_words each"""
    # Clean up text
    text = re.sub(r'\s+', ' ', text).strip()
    words = text.split()
    
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

# Process in_our_approach.html
file1 = base_dir / 'in/about_piandt/in_our_approach.html'
with open(file1, 'r', encoding='utf-8') as f:
    content1 = f.read()

# Extract the paragraph text
match1 = re.search(r'<div class="content-text"[^>]*>(.*?)</div>\s*</div>\s*</div>\s*</section>', content1, re.DOTALL)
if match1:
    para_text = re.search(r'<p[^>]*>(.*?)</p>', match1.group(1), re.DOTALL)
    if para_text:
        text = para_text.group(1)
        # Add spaces
        text = add_spaces_to_text(text)
        # Split into paragraphs
        paragraphs = split_text_into_paragraphs(text, TARGET_WORDS_PER_PARAGRAPH)
        
        # Ensure multiples of 4
        while len(paragraphs) % 4 != 0 and len(paragraphs) > 0:
            paragraphs.append('')
        
        # Create HTML
        paragraphs_html = '\n                        '.join([f'<p>{p}</p>' if p else '<p></p>' for p in paragraphs])
        
        # Replace
        div_start = re.search(r'(<div class="content-text"[^>]*>)', content1).group(1)
        # Remove inline column-count if present
        div_start = re.sub(r'\s*column-count:\s*[^;]+;?', '', div_start)
        
        new_content = content1[:match1.start()] + div_start + '\n                        ' + paragraphs_html + '\n                    </div>\n                </div>\n            </div>\n        </section>'
        
        with open(file1, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✓ Fixed in_our_approach.html: {len(paragraphs)} paragraphs")

# Process in_governance.html
file2 = base_dir / 'in/about_piandt/in_governance.html'
with open(file2, 'r', encoding='utf-8') as f:
    content2 = f.read()

# Check if multi-sheet-pagination.js is included
if 'multi-sheet-pagination.js' not in content2:
    script_pattern = r'(<script src="[^"]*script\.js[^"]*"></script>)'
    match_script = re.search(script_pattern, content2)
    if match_script:
        content2 = content2.replace(match_script.group(1), '<script src="../../multi-sheet-pagination.js"></script>\n    ' + match_script.group(1))
        print("✓ Added multi-sheet-pagination.js to in_governance.html")

# Extract the paragraph text
match2 = re.search(r'<div class="content-text"[^>]*>(.*?)</div>\s*</div>\s*</div>\s*</section>', content2, re.DOTALL)
if match2:
    para_text = re.search(r'<p[^>]*>(.*?)</p>', match2.group(1), re.DOTALL)
    if para_text:
        text = para_text.group(1)
        # Add spaces
        text = add_spaces_to_text(text)
        # Split into paragraphs
        paragraphs = split_text_into_paragraphs(text, TARGET_WORDS_PER_PARAGRAPH)
        
        # Ensure multiples of 4
        while len(paragraphs) % 4 != 0 and len(paragraphs) > 0:
            paragraphs.append('')
        
        # Create HTML
        paragraphs_html = '\n                        '.join([f'<p>{p}</p>' if p else '<p></p>' for p in paragraphs])
        
        # Replace
        div_start = re.search(r'(<div class="content-text"[^>]*>)', content2).group(1)
        # Remove inline column-count if present
        div_start = re.sub(r'\s*column-count:\s*[^;]+;?', '', div_start)
        
        new_content = content2[:match2.start()] + div_start + '\n                        ' + paragraphs_html + '\n                    </div>\n                </div>\n            </div>\n        </section>'
        
        with open(file2, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✓ Fixed in_governance.html: {len(paragraphs)} paragraphs")

print("\n✓ Both files processed. Test them now!")

