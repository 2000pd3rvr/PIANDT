
#!/usr/bin/env python3
"""
Systematically vary page content across In, Proc, Out for each menu item
Ensures each triad set has distinct, varied openings
"""
import re
from pathlib import Path
import hashlib

BASE_DIR = Path(__file__).parent.parent

# Varied opening phrases - more diverse
IN_OPENINGS = [
    "The {name} incoming signals section functions as the primary reception interface within the triadic information framework",
    "Operating within the In stage of the PIANDT triadic information system, the {name} incoming signals section serves as the specialized gateway",
    "Serving as the specialized reception interface, the {name} incoming signals component captures and documents",
    "As the primary reception stage for {topic}, the {name} incoming signals section systematically receives",
    "The {name} component represents the initial reception point within the triadic information flow",
    "Within the triadic information framework, the {name} incoming signals section operates as the dedicated reception mechanism",
    "The {name} incoming signals section acts as the primary gateway within the PIANDT triadic information architecture",
    "Functioning as the specialized reception mechanism, the {name} incoming signals section captures and documents",
]

PROC_OPENINGS = [
    "Serving as the specialized analytical engine, the {name} processing component evaluates, synthesizes, and refines",
    "Within the triadic information framework, the {name} processing component functions as the analytical transformation engine",
    "The {name} processing section operates as the dedicated transformation mechanism within the PIANDT triadic information system",
    "As the primary transformation stage for {topic}, the {name} processing section systematically evaluates",
    "The {name} component represents the analytical transformation point within the triadic information flow",
    "Operating within the Processing stage of the PIANDT triadic information system, the {name} processing section serves as the specialized analytical engine",
    "The {name} processing component acts as the analytical transformation engine within the PIANDT triadic information architecture",
    "Functioning as the specialized transformation mechanism, the {name} processing section evaluates, analyzes, and refines",
]

OUT_OPENINGS = [
    "Within the triadic information framework, the {name} delivered outputs component functions as the final delivery stage",
    "The {name} delivered outputs section operates as the dedicated delivery mechanism within the PIANDT triadic information system",
    "Serving as the specialized delivery interface, the {name} delivered outputs component packages, formats, and delivers",
    "As the primary delivery stage for {topic}, the {name} delivered outputs section systematically formats",
    "The {name} component represents the final delivery point within the triadic information flow",
    "Operating within the Out stage of the PIANDT triadic information system, the {name} delivered outputs section serves as the specialized delivery mechanism",
    "The {name} delivered outputs component acts as the final delivery stage within the PIANDT triadic information architecture",
    "Functioning as the specialized delivery mechanism, the {name} delivered outputs section formats, verifies, and delivers",
]

def get_menu_item_id(file_path):
    """Extract menu item identifier (removes stage prefix from path and filename)"""
    rel_path = str(file_path.relative_to(BASE_DIR))
    # Remove stage prefix from path
    menu_id = re.sub(r'^(in|processing|proc|out)/', '', rel_path)
    # Remove .html
    menu_id = re.sub(r'\.html$', '', menu_id)
    # Remove stage prefix from filename (e.g., "about_piandt/in_about_piandt" -> "about_piandt/about_piandt")
    # Match stage prefix after last slash or at start
    menu_id = re.sub(r'(^|/)(in_|proc_|out_)', r'\1', menu_id)
    return menu_id

def get_stage(file_path):
    """Get stage (in, proc, out)"""
    path_str = str(file_path)
    if '/in/' in path_str:
        return 'in'
    elif '/processing/' in path_str or '/proc/' in path_str:
        return 'proc'
    elif '/out/' in path_str:
        return 'out'
    return None

def extract_page_name(file_path):
    """Extract clean page name"""
    filename = file_path.stem
    filename = re.sub(r'^(in_|proc_|out_)', '', filename)
    name = filename.replace('_', ' ').title()
    name = name.replace('Miu', 'MIU').replace('Rd', 'R&D')
    name = re.sub(r'\s+', ' ', name)
    # Clean up
    name = re.sub(r'^Units\s+MIU\s+Vision', 'Vision', name)
    name = re.sub(r'^Units\s+MIU', 'Machine Intelligence', name)
    name = re.sub(r'^About\s+Piandt', 'About PIANDT', name, flags=re.I)
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

def clean_paragraph(text):
    """Remove duplicate sentences and clean up"""
    # Remove obvious duplicate patterns
    text = re.sub(r'(the [^<]+?\.)\s+\1+', r'\1', text, flags=re.I)
    text = re.sub(r'(This component[^<]+?\.)\s+\1+', r'\1', text, flags=re.I)
    text = re.sub(r'(Grounded in[^<]+?\.)\s+\1+', r'\1', text, flags=re.I)
    text = re.sub(r'(The [^<]+ (?:incoming signals|processing|output)[^<]+?\.)\s+\1+', r'\1', text, flags=re.I)
    return text

def update_page_content(file_path, opening_template, page_name, topic, stage):
    """Update the first content paragraph with new opening"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find first paragraph in content-text - use simpler pattern
        pattern = r'<div class="content-text"[^>]*>.*?<p>([^<]+)</p>'
        match = re.search(pattern, content, re.I | re.DOTALL)
        
        if not match:
            return False
        
        old_para = match.group(1)
        
        # Find where unique content continues
        unique_markers = [
            r'where communications flow seamlessly',
            r'Grounded in the (?:elegant )?scientific principle',
            r'The [^<]+ (?:incoming signals|processing stage|output stage) encompass',
            r'This component packages, formats',
            r'Each (?:incoming signal|signal|processed signal)',
        ]
        
        rest_of_content = None
        for marker in unique_markers:
            m = re.search(marker, old_para, re.I)
            if m:
                rest_of_content = old_para[m.start():]
                break
        
        if not rest_of_content:
            # Fallback: take after first 300 chars
            rest_of_content = old_para[300:] if len(old_para) > 300 else ''
        
        # Build new opening
        if '{topic}' in opening_template:
            new_opening = opening_template.format(name=page_name, topic=topic)
        else:
            new_opening = opening_template.format(name=page_name)
        
        # Add stage-specific continuation
        if stage == 'in':
            continuation = f"that captures and documents all communications, requests, and initiatives related to {topic}."
        elif stage == 'proc':
            continuation = f"incoming signals related to {topic} into actionable outputs."
        else:
            continuation = f"where processed signals related to {topic} are systematically formatted, verified, and delivered to stakeholders with unwavering integrity."
        
        # Combine
        if rest_of_content.strip():
            new_para = f"{new_opening} {continuation} {rest_of_content}"
        else:
            new_para = f"{new_opening} {continuation}"
        
        new_para = clean_paragraph(new_para)
        
        # Update - simple replace
        content = content.replace(f'<p>{old_para}</p>', f'<p>{new_para}</p>', 1)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error updating {file_path}: {e}")
        return False

def main():
    # Get all HTML files
    html_files = list(BASE_DIR.rglob("*.html"))
    html_files = [f for f in html_files if 'site_agent' not in str(f) and '.git' not in str(f)]
    
    # Group by menu item
    menu_groups = {}
    for html_file in html_files:
        menu_id = get_menu_item_id(html_file)
        stage = get_stage(html_file)
        if stage:
            if menu_id not in menu_groups:
                menu_groups[menu_id] = {}
            menu_groups[menu_id][stage] = html_file
    
    # Process each menu item group
    print("Processing menu items across In, Proc, Out:")
    print("=" * 70)
    print(f"Total menu groups found: {len(menu_groups)}")
    
    updated_count = 0
    skipped_count = 0
    
    for menu_id, stages in sorted(menu_groups.items()):
        if len(stages) < 2:  # Skip if not a complete triad
            skipped_count += 1
            continue
        
        print(f"\n📋 Menu Item: {menu_id}")
        print("-" * 70)
        
        # Get page info (use first file as reference)
        first_file = list(stages.values())[0]
        page_name = extract_page_name(first_file)
        topic = extract_topic(first_file)
        
        # Assign different openings to each stage
        # Use menu_id hash to ensure consistency but variety
        menu_hash = int(hashlib.md5(menu_id.encode()).hexdigest(), 16)
        
        # Group openings by starting pattern to ensure variety
        def get_opening_pattern(opening):
            """Extract the starting pattern of an opening"""
            if opening.startswith("Serving as"):
                return "Serving"
            elif opening.startswith("The {name}"):
                return "The"
            elif opening.startswith("Operating"):
                return "Operating"
            elif opening.startswith("Within"):
                return "Within"
            elif opening.startswith("As the"):
                return "As"
            elif opening.startswith("Functioning"):
                return "Functioning"
            else:
                return "Other"
        
        # Pre-select distinct openings for each stage
        selected_indices = {}
        selected_patterns = set()
        
        for stage in ['in', 'proc', 'out']:
            if stage not in stages:
                continue
            
            if stage == 'in':
                openings = IN_OPENINGS
            elif stage == 'proc':
                openings = PROC_OPENINGS
            else:
                openings = OUT_OPENINGS
            
            # Try to find an opening with a different starting pattern
            max_attempts = len(openings) * 2
            for attempt in range(max_attempts):
                # Use hash with attempt offset to get different indices
                opening_idx = (menu_hash + hash(stage) + attempt * 7) % len(openings)
                opening_template = openings[opening_idx]
                pattern = get_opening_pattern(opening_template)
                
                # If this pattern hasn't been used yet, use it
                if pattern not in selected_patterns:
                    selected_indices[stage] = opening_idx
                    selected_patterns.add(pattern)
                    break
            
            # If we couldn't find a unique pattern, just use the hash-based selection
            if stage not in selected_indices:
                opening_idx = (menu_hash + hash(stage)) % len(openings)
                selected_indices[stage] = opening_idx
        
        # Now update each stage with its selected opening
        for stage in ['in', 'proc', 'out']:
            if stage not in stages:
                continue
            
            file_path = stages[stage]
            
            if stage == 'in':
                openings = IN_OPENINGS
            elif stage == 'proc':
                openings = PROC_OPENINGS
            else:
                openings = OUT_OPENINGS
            
            opening_idx = selected_indices.get(stage, (menu_hash + hash(stage)) % len(openings))
            opening_template = openings[opening_idx]
            
            result = update_page_content(file_path, opening_template, page_name, topic, stage)
            if result:
                updated_count += 1
                print(f"  ✓ {stage.upper()}: {file_path.relative_to(BASE_DIR)}")
                print(f"    Opening: {opening_template.format(name=page_name, topic=topic)[:80]}...")
            else:
                print(f"  ✗ {stage.upper()}: Failed to update {file_path.relative_to(BASE_DIR)}")
    
    print(f"\n✅ Updated {updated_count} pages with varied content across all menu items")
    print(f"⏭️  Skipped {skipped_count} menu items (incomplete triads)")
    print("=" * 70)

if __name__ == '__main__':
    main()

