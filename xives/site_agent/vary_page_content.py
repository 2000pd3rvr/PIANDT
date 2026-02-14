#!/usr/bin/env python3
"""
Vary page content paragraphs to eliminate monotonic patterns
Updates the actual visible content, not just meta descriptions
"""
import re
from pathlib import Path
from html import escape

BASE_DIR = Path(__file__).parent.parent

# Varied opening phrases for content paragraphs
IN_CONTENT_OPENINGS = [
    "The {name} incoming signals section functions as the primary reception interface within the triadic information framework",
    "Operating within the In stage of the PIANDT triadic information system, the {name} incoming signals section serves as the specialized gateway",
    "Serving as the specialized reception interface, the {name} incoming signals component captures and documents",
    "As the primary reception stage for {topic}, the {name} incoming signals section systematically receives",
    "The {name} component represents the initial reception point within the triadic information flow",
    "Within the triadic information framework, the {name} incoming signals section operates as the dedicated reception mechanism",
]

PROC_CONTENT_OPENINGS = [
    "Serving as the specialized analytical engine, the {name} processing component evaluates, synthesizes, and refines",
    "Within the triadic information framework, the {name} processing component functions as the analytical transformation engine",
    "The {name} processing section operates as the dedicated transformation mechanism within the PIANDT triadic information system",
    "As the primary transformation stage for {topic}, the {name} processing section systematically evaluates",
    "The {name} component represents the analytical transformation point within the triadic information flow",
    "Operating within the Processing stage of the PIANDT triadic information system, the {name} processing section serves as the specialized analytical engine",
]

OUT_CONTENT_OPENINGS = [
    "Within the triadic information framework, the {name} delivered outputs component functions as the final delivery stage",
    "The {name} delivered outputs section operates as the dedicated delivery mechanism within the PIANDT triadic information system",
    "Serving as the specialized delivery interface, the {name} delivered outputs component packages, formats, and delivers",
    "As the primary delivery stage for {topic}, the {name} delivered outputs section systematically formats",
    "The {name} component represents the final delivery point within the triadic information flow",
    "Operating within the Out stage of the PIANDT triadic information system, the {name} delivered outputs section serves as the specialized delivery mechanism",
]

def get_stage_info(file_path):
    """Determine stage"""
    path_str = str(file_path)
    if '/in/' in path_str:
        return 'in', IN_CONTENT_OPENINGS
    elif '/processing/' in path_str or '/proc/' in path_str:
        return 'proc', PROC_CONTENT_OPENINGS
    elif '/out/' in path_str:
        return 'out', OUT_CONTENT_OPENINGS
    return None, None

def extract_page_name(file_path):
    """Extract clean page name"""
    filename = file_path.stem
    filename = re.sub(r'^(in_|proc_|out_)', '', filename)
    name = filename.replace('_', ' ').title()
    name = name.replace('Miu', 'MIU').replace('Rd', 'R&D')
    # Clean up
    name = re.sub(r'\s+', ' ', name)
    # Remove "Units MIU Vision" -> "Vision"
    name = re.sub(r'^Units\s+MIU\s+Vision', 'Vision', name)
    name = re.sub(r'^Units\s+MIU', 'Machine Intelligence', name)
    return name

def extract_topic(file_path):
    """Extract topic"""
    path_str = str(file_path)
    if 'about_piandt' in path_str:
        if 'mission_vision' in path_str:
            return 'our organizational purpose and long-term aspirations'
        elif 'charitable_purposes' in path_str:
            return 'our charitable activities and public benefit objectives'
        elif 'our_approach' in path_str:
            return 'our operational methodologies and evidence-based practices'
        elif 'trustees' in path_str:
            return 'our trustee recruitment, composition, and diversity frameworks'
        elif 'governance' in path_str:
            return 'our governance structures, processes, and inclusive practices'
        else:
            return 'our organizational identity, strategic direction, and operational methodologies'
    elif 'units' in path_str:
        if 'miu' in path_str:
            if 'vision' in path_str:
                if 'products' in path_str:
                    if 'software' in path_str:
                        return 'machine intelligence software product development'
                    elif 'hardware' in path_str:
                        return 'machine intelligence hardware product development'
                    else:
                        return 'machine intelligence product development and vision'
                elif 'services' in path_str:
                    if 'rd' in path_str or 'r&d' in path_str.lower():
                        return 'machine intelligence research and development services'
                    elif 'consultancy' in path_str:
                        return 'machine intelligence consultancy services'
                    elif 'education' in path_str:
                        return 'machine intelligence educational services'
                    else:
                        return 'machine intelligence service development and vision'
                else:
                    return 'the Machine Intelligence Unit\'s vision and strategic direction'
            else:
                return 'machine intelligence research, development, and applications'
        else:
            return 'our operational units, their capabilities, and methodologies'
    return 'organizational information flow'

def update_content_paragraph(file_path):
    """Update the first content paragraph"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        stage, openings = get_stage_info(file_path)
        if not stage:
            return False
        
        page_name = extract_page_name(file_path)
        topic = extract_topic(file_path)
        
        # Use hash for consistent selection
        import hashlib
        hash_val = int(hashlib.md5(str(file_path).encode()).hexdigest(), 16)
        opening_template = openings[hash_val % len(openings)]
        
        # Find first paragraph in content-text
        pattern = r'(<div class="content-text"[^>]*>)\s*<p>(In the sophisticated architecture of organizational information flow,|Within the triadic information framework,|Serving as the specialized|Operating within|As the primary|The [^<]+ (incoming signals|processing component|delivered outputs))'
        
        match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
        if match:
            # Find the full first paragraph
            para_pattern = r'<div class="content-text"[^>]*>\s*<p>([^<]+(?:<[^>]+>[^<]*)*)</p>'
            para_match = re.search(para_pattern, content, re.IGNORECASE | re.DOTALL)
            
            if para_match:
                old_para = para_match.group(1)
                # Extract the rest of the paragraph after the opening
                # Find where the actual content starts (after the opening phrase)
                rest_match = re.search(r'(This (?:focused )?component|Grounded in|The [^<]+ (?:incoming signals|processing|output))', old_para, re.IGNORECASE)
                
                if rest_match:
                    rest_of_para = old_para[rest_match.start():]
                    
                    # Build new opening
                    if '{topic}' in opening_template:
                        new_opening = opening_template.format(name=page_name, topic=topic)
                    else:
                        new_opening = opening_template.format(name=page_name)
                    
                    # Add continuation based on stage
                    if stage == 'in':
                        continuation = f"that captures and documents all communications, requests, and initiatives related to {topic}. This component operates within the In stage of the PIANDT triadic information system, systematically receiving and cataloging signals that exhibit bidirectional interaction patterns"
                    elif stage == 'proc':
                        continuation = f"incoming signals related to {topic} into actionable outputs. This component operates within the Processing stage of the PIANDT triadic information system, systematically analyzing and transforming signals that exhibit bidirectional interaction patterns"
                    else:
                        continuation = f"where processed signals related to {topic} are systematically formatted, verified, and delivered to stakeholders with unwavering integrity. Grounded in the scientific principle of signal proportionality (S_In ∝ S_Proc ∝ S_Out), this component ensures that every signal received at the In stage and processed at the Proc stage generates a corresponding, verifiable output"
                    
                    # Combine
                    new_para_start = f"{new_opening} {continuation}"
                    
                    # Find where to insert (after "patterns" or similar)
                    if rest_match:
                        # Replace the old opening with new one
                        new_para = new_para_start + ". " + rest_of_para
                        
                        # Update in content
                        content = content.replace(f'<p>{old_para}</p>', f'<p>{new_para}</p>', 1)
                        
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        return True
    except Exception as e:
        print(f"Error: {file_path}: {e}")
    return False

def main():
    html_files = list(BASE_DIR.rglob("*.html"))
    html_files = [f for f in html_files if 'site_agent' not in str(f) and '.git' not in str(f)]
    
    updated = 0
    for html_file in sorted(html_files):
        if update_content_paragraph(html_file):
            updated += 1
            print(f"✓ Updated: {html_file.relative_to(BASE_DIR)}")
    
    print(f"\n✅ Updated {updated} pages with varied content openings")

if __name__ == '__main__':
    main()

