#!/usr/bin/env python3
"""
Create missing files in in/miu/ and in/piandt/ directories
Based on processing/ structure but adapted for "Incoming Signals"
"""

import os
import re
import shutil
from pathlib import Path

base_dir = Path(__file__).parent.parent

def create_in_file_from_template(source_file, target_file, title_suffix="Incoming Signals"):
    """Create an IN file from a processing template"""
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace title
    content = re.sub(r'<title>([^<]*)</title>', r'<title>\1 - In - PIANDT</title>', content)
    content = re.sub(r'<h1>([^<]*) - Proc</h1>', rf'<h1>\1 - {title_suffix}</h1>', content)
    content = re.sub(r'<h1>([^<]*)</h1>', rf'<h1>\1 - {title_suffix}</h1>', content)
    
    # Replace content-text to be about incoming signals
    # This is a simplified version - you may need to customize content
    content = re.sub(
        r'(<div class="content-text"[^>]*>)(.*?)(</div>)',
        lambda m: m.group(1) + '\n                        <p>This section captures and documents all incoming signals, requests, and new initiatives related to this area. These signals represent community needs, stakeholder input, and emerging opportunities. As part of the In component of the PIANDT triadic information architecture, this area receives and collects all external communications, suggestions, feedback, and proposals.</p>\n                        <p>Incoming signals may include: community requests, stakeholder feedback, suggestions for improvements, proposals for new initiatives, research findings, and emerging needs. Each incoming signal is documented, categorized, and prepared for evaluation.</p>\n                        <p>Signals that align with our core values and demonstrate potential for positive impact are routed to the processing stage for further analysis and development.</p>\n                        <p></p>\n                    ' + m.group(3),
        content,
        flags=re.DOTALL
    )
    
    # Fix script paths (processing is 1 level deeper than in)
    content = content.replace('../../multi-sheet-pagination.js', '../multi-sheet-pagination.js')
    content = content.replace('../../../images/agent.png', '../images/agent.png')
    content = content.replace('../../script.js', '../script.js')
    content = content.replace('../../pages-data.js', '../pages-data.js')
    content = content.replace('../../dynamic-menu.js', '../dynamic-menu.js')
    content = content.replace('../../contextual-nav.js', '../contextual-nav.js')
    content = content.replace('../../menu-hover-control.js', '../menu-hover-control.js')
    
    # Fix CSS path
    content = content.replace('../../styles.css', '../styles.css')
    
    # Fix navigation paths
    content = re.sub(r'href="\.\./\.\./index\.html"', 'href="../index.html"', content)
    
    # Ensure multi-sheet script is included
    if 'multi-sheet-pagination.js' not in content:
        # Add before script.js
        content = re.sub(
            r'(<script src="[^"]*script\.js[^"]*"></script>)',
            r'<script src="../multi-sheet-pagination.js"></script>\n    \1',
            content
        )
    
    # Ensure chat agent is included
    if 'chat-agent-btn' not in content:
        chat_html = '''
    <!-- Chat Agent Button -->
    <img src="../images/agent.png" alt="Speak to an agent" class="chat-agent-btn" id="chatAgentBtn">

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
        if '</main>' in content:
            content = content.replace('</main>', '</main>' + chat_html)
        elif '</body>' in content:
            content = re.sub(r'(</body>)', chat_html + '\n\n\\1', content)
    
    # Write file
    target_file.parent.mkdir(parents=True, exist_ok=True)
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

# Create MIU files (11 files)
miu_files = [
    'miu.html',
    'miu_products.html',
    'miu_services.html',
    'miu_vision.html',
    'miu_vision_products.html',
    'miu_vision_products_hardware.html',
    'miu_vision_products_software.html',
    'miu_vision_services.html',
    'miu_vision_services_consultancy.html',
    'miu_vision_services_education.html',
    'miu_vision_services_rd.html',
]

print("Creating MIU files in in/miu/...")
for filename in miu_files:
    source = base_dir / 'processing' / 'miu' / f'processing_{filename}'
    target = base_dir / 'in' / 'miu' / f'in_{filename}'
    
    if source.exists():
        create_in_file_from_template(source, target)
        print(f"  ✓ Created {target.relative_to(base_dir)}")
    else:
        print(f"  ✗ Source not found: {source}")

# Create PIANDT files (4 files)
piandt_files = [
    'about_piandt.html',
    'charitable_purposes.html',
    'mission_vision.html',
    'our_approach.html',
]

print("\nCreating PIANDT files in in/piandt/...")
for filename in piandt_files:
    source = base_dir / 'processing' / 'piandt' / filename
    target = base_dir / 'in' / 'piandt' / f'in_{filename}'
    
    if source.exists():
        create_in_file_from_template(source, target)
        print(f"  ✓ Created {target.relative_to(base_dir)}")
    else:
        print(f"  ✗ Source not found: {source}")

print("\n✓ Done! Now processing these files with multi-sheet logic...")

