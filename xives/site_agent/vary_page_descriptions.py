#!/usr/bin/env python3
"""
Vary page descriptions to eliminate monotonic patterns
Creates unique, engaging descriptions while maintaining meaning
"""
import re
from pathlib import Path
from html import escape

BASE_DIR = Path(__file__).parent.parent

# Varied opening phrases for each stage
IN_OPENINGS = [
    "Within the triadic information framework, the {name} incoming signals component functions as the primary reception interface, capturing and documenting all communications, requests, and initiatives related to {topic}.",
    "The {name} incoming signals section operates as the dedicated reception mechanism within the PIANDT triadic information system, systematically collecting and cataloging all communications, requests, and initiatives related to {topic}.",
    "Serving as the specialized reception interface, the {name} incoming signals component captures and documents all communications, requests, and initiatives related to {topic} within the PIANDT triadic information architecture.",
    "As the primary reception stage for {topic}, the {name} incoming signals section systematically receives, documents, and catalogs all communications, requests, and initiatives flowing into the organization.",
    "The {name} component represents the initial reception point within the triadic information flow, where all communications, requests, and initiatives related to {topic} are captured and documented.",
    "Operating within the In stage of the PIANDT triadic information system, the {name} incoming signals section serves as the specialized gateway that captures and documents all communications, requests, and initiatives related to {topic}.",
]

PROC_OPENINGS = [
    "Within the triadic information framework, the {name} processing component functions as the analytical transformation engine, where incoming signals related to {topic} undergo systematic evaluation, synthesis, and refinement into actionable outputs.",
    "The {name} processing section operates as the dedicated transformation mechanism within the PIANDT triadic information system, systematically analyzing and refining signals related to {topic} into actionable outputs.",
    "Serving as the specialized analytical stage, the {name} processing component evaluates, synthesizes, and refines incoming signals related to {topic} within the PIANDT triadic information architecture.",
    "As the primary transformation stage for {topic}, the {name} processing section systematically evaluates, analyzes, and refines incoming signals into actionable outputs within the triadic information flow.",
    "The {name} component represents the analytical transformation point within the triadic information flow, where signals related to {topic} are systematically evaluated, synthesized, and refined into actionable outputs.",
    "Operating within the Processing stage of the PIANDT triadic information system, the {name} processing section serves as the specialized analytical engine that transforms signals related to {topic} into actionable outputs.",
]

OUT_OPENINGS = [
    "Within the triadic information framework, the {name} delivered outputs component functions as the final delivery stage, where processed signals related to {topic} are systematically formatted, verified, and delivered to stakeholders with unwavering integrity.",
    "The {name} delivered outputs section operates as the dedicated delivery mechanism within the PIANDT triadic information system, systematically formatting, verifying, and delivering processed signals related to {topic} to stakeholders.",
    "Serving as the specialized delivery interface, the {name} delivered outputs component packages, formats, and delivers processed signals related to {topic} within the PIANDT triadic information architecture.",
    "As the primary delivery stage for {topic}, the {name} delivered outputs section systematically formats, verifies, and delivers processed signals to stakeholders with complete integrity and quality assurance.",
    "The {name} component represents the final delivery point within the triadic information flow, where processed signals related to {topic} are systematically formatted, verified, and delivered to stakeholders.",
    "Operating within the Out stage of the PIANDT triadic information system, the {name} delivered outputs section serves as the specialized delivery mechanism that formats, verifies, and delivers processed signals related to {topic} to stakeholders.",
]

# Common continuation phrases (varied)
CONTINUATIONS = [
    "This component operates within the {stage} stage of the PIANDT triadic information system, systematically {action} signals that exhibit bidirectional interaction patterns.",
    "Grounded in the scientific principle of signal proportionality (S_In ∝ S_Proc ∝ S_Out), this component ensures that every signal {stage_action} generates a corresponding {next_stage} mechanism.",
    "This focused component operates within the {stage} stage of the PIANDT triadic information system, systematically {action} signals that demonstrate bidirectional interaction capabilities.",
    "Built upon the triadic information architecture, this component maintains proportional signal relationships, ensuring that every {stage_action} generates appropriate {next_stage} responses.",
]

# Automation phrases (varied)
AUTOMATION_PHRASES = [
    "The structured nature of {name} {stage} information, organized into discrete, {unit_type} signal units with explicit triadic mapping, enables full automation of business transactions through machine-readable formats, standardized {stage} protocols, and programmable {action_type} mechanisms.",
    "Organized into discrete, {unit_type} signal units with explicit triadic mapping, the {name} {stage} information structure enables comprehensive automation of business transactions through machine-readable formats, standardized {stage} protocols, and programmable {action_type} systems.",
    "The systematic organization of {name} {stage} information into discrete, {unit_type} signal units with explicit triadic mapping facilitates complete automation of business transactions through machine-readable formats, standardized {stage} protocols, and programmable {action_type} mechanisms.",
]

def get_stage_info(file_path):
    """Determine stage and get appropriate opening phrase"""
    path_str = str(file_path)
    if '/in/' in path_str:
        return 'in', IN_OPENINGS, 'receiving', 'receiving', 'processing pathway and output', 'categorizable', 'routing'
    elif '/processing/' in path_str or '/proc/' in path_str:
        return 'proc', PROC_OPENINGS, 'processing', 'processing', 'output mechanism', 'analyzable', 'transformation'
    elif '/out/' in path_str:
        return 'out', OUT_OPENINGS, 'delivering', 'delivery', 'verification and delivery', 'verifiable', 'verification'
    return None, None, None, None, None, None, None

def extract_page_name(file_path):
    """Extract page name from file path"""
    filename = file_path.stem
    # Remove stage prefixes
    filename = re.sub(r'^(in_|proc_|out_)', '', filename)
    # Convert underscores to spaces and title case
    name = filename.replace('_', ' ').title()
    # Handle special cases
    name = name.replace('Miu', 'MIU')
    name = name.replace('Rd', 'R&D')
    return name

def extract_topic(file_path):
    """Extract topic from file path"""
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

def update_page_description(file_path):
    """Update a single page's description"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        stage, openings, action, stage_name, next_stage, unit_type, action_type = get_stage_info(file_path)
        if not stage:
            return False
        
        page_name = extract_page_name(file_path)
        topic = extract_topic(file_path)
        
        # Use hash of filename to consistently select opening phrase
        import hashlib
        hash_val = int(hashlib.md5(str(file_path).encode()).hexdigest(), 16)
        opening_template = openings[hash_val % len(openings)]
        
        # Select continuation
        cont_hash = hash_val // len(openings)
        continuation_template = CONTINUATIONS[cont_hash % len(CONTINUATIONS)]
        
        # Select automation phrase
        auto_hash = cont_hash // len(CONTINUATIONS)
        automation_template = AUTOMATION_PHRASES[auto_hash % len(AUTOMATION_PHRASES)]
        
        # Build description
        opening = opening_template.format(name=page_name, topic=topic)
        continuation = continuation_template.format(
            stage=stage_name,
            action=action,
            stage_action=f"at the {stage_name} stage" if stage == 'in' else f"processed at the {stage_name} stage" if stage == 'proc' else f"received at the In stage and processed at the Proc stage",
            next_stage=next_stage
        )
        automation = automation_template.format(
            name=page_name,
            stage=stage,
            unit_type=unit_type,
            action_type=action_type
        )
        
        new_description = f"{opening} {continuation} {automation}"
        
        # Update meta description
        pattern = r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']'
        if re.search(pattern, content):
            content = re.sub(
                pattern,
                f'<meta name="description" content="{escape(new_description)}"',
                content,
                flags=re.IGNORECASE
            )
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
    except Exception as e:
        print(f"Error updating {file_path}: {e}")
        return False
    return False

def main():
    """Update all HTML pages"""
    html_files = list(BASE_DIR.rglob("*.html"))
    html_files = [f for f in html_files if 'site_agent' not in str(f) and '.git' not in str(f)]
    
    updated = 0
    for html_file in sorted(html_files):
        if update_page_description(html_file):
            updated += 1
            print(f"✓ Updated: {html_file.relative_to(BASE_DIR)}")
    
    print(f"\n✅ Updated {updated} pages with varied descriptions")

if __name__ == '__main__':
    main()

