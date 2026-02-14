#!/usr/bin/env python3
"""
Clean duplicate descriptions and ensure varied, engaging text
"""
import re
from pathlib import Path
from html import escape

BASE_DIR = Path(__file__).parent.parent

# Varied opening phrases - more diverse
IN_OPENINGS = [
    "Within the triadic information framework, the {name} incoming signals component functions as the primary reception interface",
    "The {name} incoming signals section operates as the dedicated reception mechanism within the PIANDT triadic information system",
    "Serving as the specialized reception interface, the {name} incoming signals component captures and documents",
    "As the primary reception stage for {topic}, the {name} incoming signals section systematically receives",
    "The {name} component represents the initial reception point within the triadic information flow",
    "Operating within the In stage of the PIANDT triadic information system, the {name} incoming signals section serves as the specialized gateway",
]

PROC_OPENINGS = [
    "Within the triadic information framework, the {name} processing component functions as the analytical transformation engine",
    "The {name} processing section operates as the dedicated transformation mechanism within the PIANDT triadic information system",
    "Serving as the specialized analytical stage, the {name} processing component evaluates, synthesizes, and refines",
    "As the primary transformation stage for {topic}, the {name} processing section systematically evaluates",
    "The {name} component represents the analytical transformation point within the triadic information flow",
    "Operating within the Processing stage of the PIANDT triadic information system, the {name} processing section serves as the specialized analytical engine",
]

OUT_OPENINGS = [
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
        return 'in', IN_OPENINGS
    elif '/processing/' in path_str or '/proc/' in path_str:
        return 'proc', PROC_OPENINGS
    elif '/out/' in path_str:
        return 'out', OUT_OPENINGS
    return None, None

def extract_page_name(file_path):
    """Extract clean page name"""
    filename = file_path.stem
    filename = re.sub(r'^(in_|proc_|out_)', '', filename)
    name = filename.replace('_', ' ').title()
    name = name.replace('Miu', 'MIU').replace('Rd', 'R&D')
    # Clean up common patterns
    name = re.sub(r'\s+', ' ', name)
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

def clean_description(desc):
    """Remove duplicate text from description"""
    # Remove obvious duplicates - look for repeated long phrases
    # Split into sentences
    sentences = re.split(r'([.!?])\s+', desc)
    seen = {}
    clean = []
    
    for i in range(0, len(sentences), 2):
        if i >= len(sentences):
            break
        sentence = sentences[i]
        if i + 1 < len(sentences):
            sentence += sentences[i + 1]
        
        sentence = sentence.strip()
        if not sentence:
            continue
            
        # Create a signature (first 60 chars normalized)
        sig = re.sub(r'\s+', ' ', sentence.lower())[:60]
        
        # Check if we've seen something very similar
        is_duplicate = False
        for seen_sig in seen:
            # If 80% similar, consider duplicate
            similarity = sum(a == b for a, b in zip(sig, seen_sig)) / max(len(sig), len(seen_sig), 1)
            if similarity > 0.8:
                is_duplicate = True
                break
        
        if not is_duplicate and len(sentence) > 20:
            seen[sig] = True
            clean.append(sentence)
    
    result = ' '.join(clean)
    # Remove any remaining obvious duplicates
    result = re.sub(r'(.{30,}?)\1+', r'\1', result)
    return result

def create_description(file_path):
    """Create a clean, varied description"""
    stage, openings = get_stage_info(file_path)
    if not stage:
        return None
    
    page_name = extract_page_name(file_path)
    topic = extract_topic(file_path)
    
    # Use consistent hash for same file
    import hashlib
    hash_val = int(hashlib.md5(str(file_path).encode()).hexdigest(), 16)
    opening_template = openings[hash_val % len(openings)]
    
    # Build opening
    if '{topic}' in opening_template:
        opening = opening_template.format(name=page_name, topic=topic)
    else:
        opening = opening_template.format(name=page_name)
    
    # Add continuation based on stage
    if stage == 'in':
        continuation = f"that captures and documents all communications, requests, and initiatives related to {topic}. This component operates within the In stage of the PIANDT triadic information system, systematically receiving and cataloging signals that exhibit bidirectional interaction patterns."
        automation = f"The structured nature of {page_name} incoming signals, organized into discrete, categorizable signal units with explicit triadic mapping, enables full automation of business transactions through machine-readable formats, standardized reception protocols, and programmable routing mechanisms."
    elif stage == 'proc':
        continuation = f"where incoming signals related to {topic} undergo systematic evaluation, synthesis, and refinement into actionable outputs. This component operates within the Processing stage of the PIANDT triadic information system, systematically analyzing and transforming signals that exhibit bidirectional interaction patterns."
        automation = f"The structured nature of {page_name} processing information, organized into discrete, analyzable signal units with explicit triadic mapping, enables full automation of business transactions through machine-readable formats, standardized processing protocols, and programmable transformation mechanisms."
    else:  # out
        continuation = f"where processed signals related to {topic} are systematically formatted, verified, and delivered to stakeholders with unwavering integrity. Grounded in the scientific principle of signal proportionality (S_In ∝ S_Proc ∝ S_Out), this component ensures that every signal received at the In stage and processed at the Proc stage generates a corresponding, verifiable output."
        automation = f"The structured nature of {page_name} output information, organized into discrete, verifiable output units with explicit triadic mapping, enables full automation of business transactions through machine-readable formats, standardized delivery protocols, and programmable verification mechanisms."
    
    full_desc = f"{opening} {continuation} {automation}"
    return clean_description(full_desc)

def update_page(file_path):
    """Update a single page"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_desc = create_description(file_path)
        if not new_desc:
            return False
        
        # Update meta description
        pattern = r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']'
        if re.search(pattern, content):
            content = re.sub(
                pattern,
                f'<meta name="description" content="{escape(new_desc)}"',
                content,
                flags=re.IGNORECASE
            )
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
        if update_page(html_file):
            updated += 1
            print(f"✓ Updated: {html_file.relative_to(BASE_DIR)}")
    
    print(f"\n✅ Updated {updated} pages with clean, varied descriptions")

if __name__ == '__main__':
    main()

