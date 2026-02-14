#!/usr/bin/env python3
"""
Interactive script to update pages with unique triad descriptions.
Updates pages one by one, ensuring:
1. Unique descriptions according to triad (In, Proc, Out)
2. Bidirectionality consideration
3. Automation of business transactions
4. Visible first few words in description
5. Heading matches menu item name
6. Responsive formatting included
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
import html

# Base directory
BASE_DIR = Path(__file__).parent.parent

# Stage-specific content templates
STAGE_TEMPLATES = {
    'in': {
        'description_start': 'In the sophisticated architecture of organizational information flow, the {page_name} incoming signals section serves as the specialized reception mechanism that captures and documents all communications, requests, and initiatives related to {topic}. This focused component operates within the In stage of the PIANDT triadic information system, systematically receiving and cataloging signals that exhibit bidirectional interaction patterns.',
        'content_start': 'In the sophisticated architecture of organizational information flow, the {page_name} incoming signals section serves as the specialized reception mechanism that captures and documents all communications, requests, and initiatives related to {topic}. This focused component operates within the In stage of the PIANDT triadic information system, systematically receiving and cataloging signals that exhibit bidirectional interaction patterns, where communications flow seamlessly in both directions between the organization and external stakeholders regarding {topic}. Grounded in the elegant scientific principle of signal proportionality (S_In ∝ S_Proc ∝ S_Out), this section ensures that every incoming signal related to {topic} generates a corresponding processing pathway and output mechanism, regardless of interaction direction.'
    },
    'proc': {
        'description_start': 'In the sophisticated architecture of organizational information flow, the {page_name} processing component represents the analytical transformation stage where incoming signals related to {topic} undergo systematic evaluation, synthesis, and refinement into actionable outputs. This focused component operates within the Processing stage of the PIANDT triadic information system, systematically analyzing and transforming signals that exhibit bidirectional interaction patterns.',
        'content_start': 'In the sophisticated architecture of organizational information flow, the {page_name} processing component represents the analytical transformation stage where incoming signals related to {topic} undergo systematic evaluation, synthesis, and refinement into actionable outputs. This focused component operates within the Processing stage of the PIANDT triadic information system, systematically analyzing and transforming signals that exhibit bidirectional interaction patterns, where communications flow seamlessly in both directions between the organization and external stakeholders regarding {topic}. Grounded in the elegant scientific principle of signal proportionality (S_In ∝ S_Proc ∝ S_Out), this component ensures that every incoming signal related to {topic} generates a corresponding processing pathway and output mechanism, regardless of interaction direction.'
    },
    'out': {
        'description_start': 'In the elegant architecture of organizational information flow, the {page_name} delivered outputs component represents the refined culmination of the triadic information system, where processed signals related to {topic} are systematically formatted, verified, and delivered to stakeholders with unwavering integrity. Grounded in the scientific principle of signal proportionality (S_In ∝ S_Proc ∝ S_Out), this component ensures that every signal received at the In stage and processed at the Proc stage generates a corresponding, verifiable output.',
        'content_start': 'In the elegant architecture of organizational information flow, the {page_name} delivered outputs component represents the refined culmination of the triadic information system, where processed signals related to {topic} are systematically formatted, verified, and delivered to stakeholders with unwavering integrity. Grounded in the scientific principle of signal proportionality (S_In ∝ S_Proc ∝ S_Out), this component ensures that every signal received at the In stage and processed at the Proc stage generates a corresponding, verifiable output. This component packages, formats, and delivers signals through established delivery protocols that maintain the integrity of the triadic matrix structure, ensuring that each communication reaches its destination with appropriate verification and quality assurance while preserving the proportional relationships that characterize effective organizational information systems.'
    }
}

def get_stage_from_path(file_path):
    """Determine stage (in, proc, out) from file path."""
    path_str = str(file_path)
    if '/in/' in path_str or path_str.startswith('in/'):
        return 'in'
    elif '/processing/' in path_str or '/proc/' in path_str or path_str.startswith('processing/'):
        return 'proc'
    elif '/out/' in path_str or path_str.startswith('out/'):
        return 'out'
    return None

def get_page_name_from_menu(menu_item):
    """Extract page name from menu item text."""
    # Remove common suffixes
    menu_item = menu_item.lower().strip()
    if menu_item.endswith(' - incoming signals'):
        return menu_item.replace(' - incoming signals', '')
    elif menu_item.endswith(' - in progress'):
        return menu_item.replace(' - in progress', '')
    elif menu_item.endswith(' - delivered outputs'):
        return menu_item.replace(' - delivered outputs', '')
    return menu_item

def update_page_description_and_content(file_path, stage, page_name, topic):
    """Update a single page with triad-appropriate description and content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Update meta description
        meta_desc = soup.find('meta', {'name': 'description'})
        if meta_desc:
            template = STAGE_TEMPLATES[stage]['description_start']
            new_desc = template.format(page_name=page_name, topic=topic)
            # Add automation info
            new_desc += f' The structured nature of {page_name} {stage} information, organized into discrete, categorizable signal units with explicit triadic mapping, enables full automation of business transactions through machine-readable formats, standardized {stage} protocols, and programmable routing mechanisms.'
            meta_desc['content'] = new_desc[:500] + '...' if len(new_desc) > 500 else new_desc
        
        # Update h1 heading to match menu item
        h1 = soup.find('h1')
        if h1:
            h1.string = page_name
        
        # Update content text
        content_div = soup.find('div', class_='content-text')
        if content_div:
            # Get template for content start
            content_template = STAGE_TEMPLATES[stage]['content_start']
            content_start = content_template.format(page_name=page_name, topic=topic)
            
            # Create full content with bidirectionality and automation
            full_content = generate_full_content(stage, page_name, topic, content_start)
            
            # Clear existing paragraphs and add new ones
            content_div.clear()
            for para_text in full_content:
                p = soup.new_tag('p')
                p.string = para_text
                content_div.append(p)
            
            # Add empty paragraph at end
            p_empty = soup.new_tag('p')
            p_empty.string = ''
            content_div.append(p_empty)
        
        # Write updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        return True
    except Exception as e:
        print(f"Error updating {file_path}: {e}")
        return False

def generate_full_content(stage, page_name, topic, content_start):
    """Generate full content paragraphs with bidirectionality and automation."""
    paragraphs = []
    
    # First paragraph - start with visible text
    paragraphs.append(content_start)
    
    # Second paragraph - bidirectionality examples
    if stage == 'in':
        para2 = f"The {page_name} incoming signals encompass diverse categories that demonstrate bidirectional interaction capabilities: {topic} inquiries may represent external stakeholders seeking information about our {topic} or the organization proactively sharing {topic} details with external parties; {topic} requests may involve external entities proposing new {topic} activities or the organization initiating discussions about {topic} expansions; {topic} feedback may include external suggestions for refining our {topic} methodologies or organizational requests for external input on {topic} improvements."
    elif stage == 'proc':
        para2 = f"The {page_name} processing stage encompasses diverse signal categories that demonstrate bidirectional interaction capabilities: {topic} evaluations may involve external requests for {topic} refinement or organizational initiatives to refine {topic} frameworks for external stakeholders; {topic} analyses may include external {topic} proposals or organizational {topic} development for external markets; {topic} syntheses may represent external {topic} suggestions being integrated or organizational {topic} processes for external stakeholders."
    else:  # out
        para2 = f"The {page_name} output stage encompasses diverse signal categories that demonstrate bidirectional interaction capabilities: {topic} outputs may represent organizational {topic} statements delivered to external stakeholders or external {topic} responses to organizational inquiries; {topic} documentation may include organizational {topic} information delivered to external parties or external {topic} confirmations to organizational requests; {topic} frameworks may involve organizational {topic} structures delivered to external entities or external {topic} acknowledgments of organizational methodologies."
    
    paragraphs.append(para2)
    
    # Third paragraph - triadic mapping and automation
    para3 = f"Each {'incoming signal' if stage == 'in' else 'processed signal' if stage == 'proc' else 'processed signal'} undergoes systematic {'reception' if stage == 'in' else 'processing' if stage == 'proc' else 'formatting and verification'} procedures that maintain the triadic mapping, ensuring that every {'signal category received' if stage == 'in' else 'processed signal' if stage == 'proc' else 'output'} can be traced back to its corresponding {'input signal and processing pathway' if stage == 'in' else 'incoming signal (In) and resulting output (Out)' if stage == 'proc' else 'input signal and processing pathway'}, regardless of interaction direction. The structured nature of {page_name} {'incoming signals' if stage == 'in' else 'processing information' if stage == 'proc' else 'output information'}, organized into discrete, {'categorizable signal units' if stage == 'in' else 'analyzable signal units' if stage == 'proc' else 'verifiable output units'} with explicit triadic mapping, enables full automation of business transactions through machine-readable formats, standardized {'reception' if stage == 'in' else 'processing' if stage == 'proc' else 'delivery'} protocols, and programmable {'routing' if stage == 'in' else 'transformation' if stage == 'proc' else 'verification'} mechanisms."
    
    paragraphs.append(para3)
    
    # Fourth paragraph - automation details
    para4 = f"The four-column sheet structure, with each column representing a distinct {'signal' if stage == 'in' else 'processing' if stage == 'proc' else 'output'} component, provides a natural framework for automated parsing, validation, and {'routing' if stage == 'in' else 'transformation' if stage == 'proc' else 'routing'} of transactional information related to {topic}. Automated agents can extract structured data from each column, verify triadic relationships, execute {'routing protocols to appropriate processing pathways' if stage == 'in' else 'transformation protocols' if stage == 'proc' else 'delivery protocols'}, and generate {'acknowledgments' if stage == 'in' else 'processed outputs' if stage == 'proc' else 'confirmations'}, all while maintaining the proportional signal relationships that ensure organizational balance."
    
    paragraphs.append(para4)
    
    # Fifth paragraph - strategic advantages
    para5 = f"For modern organizations, the {page_name} {'incoming signals' if stage == 'in' else 'processing' if stage == 'proc' else 'output'} component provides strategic advantages including enhanced operational transparency through explicit signal {'lifecycle mapping' if stage == 'in' else 'transformation mapping' if stage == 'proc' else 'delivery mapping'} for {topic} communications, scalable architecture enabling incremental expansion of {'reception' if stage == 'in' else 'processing' if stage == 'proc' else 'output'} capabilities, and optimized resource allocation through stage-specific performance metrics that account for bidirectional interaction patterns. The systematic {'reception' if stage == 'in' else 'processing' if stage == 'proc' else 'delivery'} frameworks reduce cognitive load for {'both internal stakeholders and external senders' if stage == 'in' else 'internal stakeholders' if stage == 'proc' else 'both internal stakeholders and external recipients'} while maintaining compatibility with contemporary technology stacks including automated {'routing' if stage == 'in' else 'workflows, agentic systems capable of executing up to 80% of automatic tasks, and 24/7 operation capabilities' if stage == 'proc' else 'distribution'} systems, quality assurance protocols, and comprehensive audit trails."
    
    paragraphs.append(para5)
    
    return paragraphs

def main():
    """Main function to process pages interactively."""
    print("Starting interactive page update process...")
    print("This script will update pages one by one with triad-appropriate descriptions.")
    print()
    
    # Find all HTML files in in/, processing/, and out/ directories
    html_files = []
    for stage_dir in ['in', 'processing', 'out']:
        stage_path = BASE_DIR / stage_dir
        if stage_path.exists():
            for html_file in stage_path.rglob('*.html'):
                # Skip main stage pages (in.html, processing.html, out.html)
                if html_file.name in ['in.html', 'processing.html', 'out.html']:
                    continue
                html_files.append(html_file)
    
    print(f"Found {len(html_files)} pages to potentially update.")
    print()
    
    for html_file in html_files:
        stage = get_stage_from_path(html_file)
        if not stage:
            continue
        
        # Extract page name from file path
        # This is a simplified extraction - you may need to customize
        page_name = html_file.stem.replace(f'{stage}_', '').replace('_', ' ').title()
        
        # For now, use a generic topic
        topic = page_name.lower()
        
        print(f"Processing: {html_file.relative_to(BASE_DIR)}")
        print(f"  Stage: {stage}")
        print(f"  Page name: {page_name}")
        print(f"  Topic: {topic}")
        
        response = input(f"  Update this page? (y/n/q to quit): ").strip().lower()
        if response == 'q':
            break
        elif response == 'y':
            if update_page_description_and_content(html_file, stage, page_name, topic):
                print(f"  ✓ Updated successfully")
            else:
                print(f"  ✗ Update failed")
        else:
            print(f"  - Skipped")
        print()

if __name__ == '__main__':
    main()

