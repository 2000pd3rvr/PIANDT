#!/usr/bin/env python3
"""
Apply multi-sheet pagination to ALL pages in in/, out/, and processing/ directories
- Add multi-sheet-pagination.js script
- Split content into ~75 word paragraphs
- Ensure 4 paragraphs per sheet
- Add chat agent HTML if missing
- Remove inline column-count styles
"""

import os
import re
from pathlib import Path

base_dir = Path(__file__).parent.parent
TARGET_WORDS_PER_PARAGRAPH = 75

def get_script_path(html_file_path):
    """Calculate relative path to multi-sheet-pagination.js from HTML file"""
    html_path = Path(html_file_path)
    depth = len(html_path.parts) - 1  # Subtract filename
    return '../' * depth + 'multi-sheet-pagination.js'

def split_text_into_paragraphs(text, target_words=75):
    """Split text into paragraphs of approximately target_words each"""
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
    
    if current_para:
        paragraphs.append(' '.join(current_para))
    
    return paragraphs

def process_file(file_path):
    """Process a single HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file has content-text
        if 'content-text' not in content:
            return False, "No content-text found"
        
        modified = False
        
        # 1. Add multi-sheet-pagination.js script if missing
        script_path = get_script_path(file_path)
        if 'multi-sheet-pagination.js' not in content:
            # Find where to insert script (before script.js or before </body>)
            script_pattern = r'(<script src="[^"]*script\.js[^"]*"></script>)'
            match = re.search(script_pattern, content)
            if match:
                content = content.replace(match.group(1), 
                    f'<script src="{script_path}"></script>\n    {match.group(1)}')
                modified = True
            else:
                # Insert before </body>
                if '</body>' in content:
                    content = content.replace('</body>', 
                        f'    <script src="{script_path}"></script>\n</body>')
                    modified = True
        
        # 2. Process content-text: split into paragraphs
        pattern = r'(<div class="content-text"[^>]*>)(.*?)(</div>\s*</div>\s*</div>\s*</section>)'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            div_start = match.group(1)
            div_content = match.group(2)
            div_end = match.group(3)
            
            # Remove inline column-count if present
            div_start = re.sub(r'\s*column-count:\s*[^;]+;?', '', div_start)
            div_start = re.sub(r'style=";', 'style="', div_start)
            
            # Extract all text from paragraphs
            para_matches = re.findall(r'<p[^>]*>(.*?)</p>', div_content, re.DOTALL)
            if para_matches:
                # Combine all paragraph text
                all_text = ' '.join([p.strip() for p in para_matches if p.strip()])
                
                # Split into ~75 word paragraphs
                paragraphs = split_text_into_paragraphs(all_text, TARGET_WORDS_PER_PARAGRAPH)
                
                # Ensure multiples of 4
                while len(paragraphs) % 4 != 0 and len(paragraphs) > 0:
                    paragraphs.append('')
                
                # Create HTML
                paras_html = '\n                        '.join([f'<p>{p}</p>' if p else '<p></p>' for p in paragraphs])
                
                # Replace content
                new_content_text = div_start + '\n                        ' + paras_html + '\n                    ' + div_end
                content = content[:match.start()] + new_content_text + content[match.end():]
                modified = True
        
        # 3. Add chat agent HTML if missing
        if 'chat-agent-btn' not in content:
            # Find </main> or </body> to insert before
            chat_html = '''
    <!-- Chat Agent Button -->
    <img src="../../../images/agent.png" alt="Speak to an agent" class="chat-agent-btn" id="chatAgentBtn">

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
            # Calculate correct image path depth
            html_path = Path(file_path)
            depth = len(html_path.parts) - 1
            image_path = '../' * depth + 'images/agent.png'
            chat_html = chat_html.replace('../../../images/agent.png', image_path)
            
            if '</main>' in content:
                content = content.replace('</main>', '</main>' + chat_html)
                modified = True
            elif '</body>' in content:
                # Insert before script tags
                script_match = re.search(r'(<script[^>]*>)', content)
                if script_match:
                    content = content[:script_match.start()] + chat_html + '\n\n' + content[script_match.start():]
                    modified = True
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, "Processed successfully"
        
        return False, "No changes needed"
        
    except Exception as e:
        return False, f"Error: {str(e)}"

# Process all files
files_to_process = [
    'in/in.html',
    'out/about_piandt/out_about_piandt.html',
    'out/about_piandt/out_charitable_purposes.html',
    'out/about_piandt/out_governance.html',
    'out/about_piandt/out_mission_vision.html',
    'out/about_piandt/out_our_approach.html',
    'out/about_piandt/out_trustees.html',
    'out/miu/out_miu.html',
    'out/miu/out_miu_products.html',
    'out/miu/out_miu_services.html',
    'out/miu/out_miu_vision.html',
    'out/miu/out_miu_vision_products.html',
    'out/miu/out_miu_vision_products_hardware.html',
    'out/miu/out_miu_vision_products_software.html',
    'out/miu/out_miu_vision_services.html',
    'out/miu/out_miu_vision_services_consultancy.html',
    'out/miu/out_miu_vision_services_education.html',
    'out/miu/out_miu_vision_services_rd.html',
    'out/piandt/about_piandt.html',
    'out/piandt/charitable_purposes.html',
    'out/piandt/mission_vision.html',
    'out/piandt/our_approach.html',
    'out/units/miu/out_miu.html',
    'out/units/miu/vision/out_miu_vision.html',
    'out/units/miu/vision/products/out_miu_vision_products.html',
    'out/units/miu/vision/products/out_miu_vision_products_hardware.html',
    'out/units/miu/vision/products/out_miu_vision_products_software.html',
    'out/units/miu/vision/services/out_miu_vision_services.html',
    'out/units/miu/vision/services/out_miu_vision_services_consultancy.html',
    'out/units/miu/vision/services/out_miu_vision_services_education.html',
    'out/units/miu/vision/services/out_miu_vision_services_rd.html',
    'out/units/out_units.html',
]

print(f"Processing {len(files_to_process)} files...\n")

success_count = 0
for file_rel_path in files_to_process:
    file_path = base_dir / file_rel_path
    if file_path.exists():
        success, message = process_file(file_path)
        if success:
            print(f"✓ {file_rel_path}: {message}")
            success_count += 1
        else:
            print(f"  {file_rel_path}: {message}")
    else:
        print(f"✗ {file_rel_path}: File not found")

print(f"\n✓ Processed {success_count}/{len(files_to_process)} files successfully!")

