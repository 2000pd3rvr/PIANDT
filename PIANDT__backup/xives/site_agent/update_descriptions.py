#!/usr/bin/env python3
"""
Update all page descriptions to match pages.html exactly
"""
import re
from pathlib import Path
from html import unescape

base_dir = Path(__file__).parent.parent

# Read pages.html to get all page descriptions
pages_html = base_dir / 'site_agent' / 'pages.html'
with open(pages_html, 'r', encoding='utf-8') as f:
    pages_content = f.read()

# Extract URL and description pairs
url_pattern = r'<td class="url-col">(.*?)</td>\s*<td class="desc-col">(.*?)</td>'
matches = re.findall(url_pattern, pages_content, re.DOTALL)

# Create mapping of URL to description
url_to_description = {}
for url, desc in matches:
    url = unescape(url.strip())
    desc = unescape(desc.strip())
    # Clean up HTML entities
    desc = desc.replace('&amp;', '&').replace('&quot;', '"').replace('&#x27;', "'").replace('&lt;', '<').replace('&gt;', '>')
    # Clean up whitespace but preserve structure
    desc = re.sub(r'\s+', ' ', desc).strip()
    url_to_description[url] = desc

print(f"Loaded {len(url_to_description)} page descriptions from pages.html\n")

# Get all HTML files
html_files = list(base_dir.rglob("*.html"))
html_files = [f for f in html_files if 'site_agent' not in str(f)]

updated_count = 0

for html_file in html_files:
    rel_path = html_file.relative_to(base_dir)
    url_key = str(rel_path).replace('\\', '/')
    
    # Skip if not in our mapping (like index.html, in.html, etc.)
    if url_key not in url_to_description:
        continue
    
    expected_desc = url_to_description[url_key]
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the content-text div
    content_pattern = r'(<div class="content-text">)(.*?)(</div>)'
    match = re.search(content_pattern, content, re.DOTALL)
    
    if match:
        # Extract existing content
        existing_content = match.group(2)
        
        # Get the first paragraph (lead) and main content
        # The description from pages.html is the full body text
        # We need to structure it properly in HTML
        
        # Split description into paragraphs (look for sentence endings)
        # For now, let's update the main paragraphs to match
        
        # Find all <p> tags in content-text
        p_tags = re.findall(r'<p[^>]*>(.*?)</p>', existing_content, re.DOTALL)
        
        if p_tags:
            # The first paragraph should be the lead
            # The rest should contain the full description
            
            # Create new content with proper structure
            # Use the description from pages.html
            # Split into sentences and create paragraphs
            sentences = re.split(r'([.!?]\s+)', expected_desc)
            paragraphs = []
            current_para = ""
            
            for i, part in enumerate(sentences):
                current_para += part
                # Create paragraphs at natural breaks (after 2-3 sentences or at specific markers)
                if i > 0 and (i % 3 == 0 or ':' in part or part.strip().endswith('.')):
                    if current_para.strip():
                        paragraphs.append(current_para.strip())
                    current_para = ""
            
            if current_para.strip():
                paragraphs.append(current_para.strip())
            
            # If we have paragraphs, update the content
            if paragraphs:
                # Keep the first as lead if it exists
                new_content = ""
                if len(paragraphs) > 0:
                    new_content += f'<p class="lead">{paragraphs[0]}</p>\n'
                
                # Add remaining paragraphs
                for para in paragraphs[1:]:
                    # Check if it looks like a heading (starts with number or specific pattern)
                    if re.match(r'^\d+\.\s+', para) or re.match(r'^[A-Z][^:]+:\s*$', para[:50]):
                        # Might be a heading, check if we should make it h2
                        if ':' in para and len(para) < 100:
                            new_content += f'<h2>{para}</h2>\n'
                        else:
                            new_content += f'<p>{para}</p>\n'
                    else:
                        new_content += f'<p>{para}</p>\n'
                
                # Replace the content-text div content
                new_div_content = match.group(1) + '\n' + new_content + '\n' + match.group(3)
                content = content[:match.start()] + new_div_content + content[match.end():]
                
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                updated_count += 1
                print(f"✓ Updated {url_key}")

print(f"\n✓ Updated {updated_count} pages")



