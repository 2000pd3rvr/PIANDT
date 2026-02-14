#!/usr/bin/env python3
"""
Update all navigation menus to include trustees and governance links
"""
import re
from pathlib import Path

base_dir = Path(__file__).parent.parent

# Get all HTML files
html_files = list(base_dir.rglob("*.html"))
html_files = [f for f in html_files if 'site_agent' not in str(f)]

fixes_made = 0

for html_file in html_files:
    rel_path = html_file.relative_to(base_dir)
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Determine which triad we're in and calculate relative paths
    if 'in/' in str(rel_path):
        triad = 'in'
        triad_prefix = '' if str(rel_path).startswith('in/in.html') or 'in/about_piandt' in str(rel_path) or 'in/units' in str(rel_path) else '../'
        about_prefix = '' if 'in/about_piandt' in str(rel_path) else 'about_piandt/'
        cross_triad_prefix = '../'
    elif 'processing/' in str(rel_path):
        triad = 'proc'
        triad_prefix = '' if str(rel_path).startswith('processing/processing.html') or 'processing/about_piandt' in str(rel_path) or 'processing/units' in str(rel_path) else '../'
        about_prefix = '' if 'processing/about_piandt' in str(rel_path) else 'about_piandt/'
        cross_triad_prefix = '../'
    elif 'out/' in str(rel_path):
        triad = 'out'
        triad_prefix = '' if str(rel_path).startswith('out/out.html') or 'out/about_piandt' in str(rel_path) or 'out/units' in str(rel_path) else '../'
        about_prefix = '' if 'out/about_piandt' in str(rel_path) else 'about_piandt/'
        cross_triad_prefix = '../'
    else:
        # Root directory (index.html)
        triad = None
        triad_prefix = ''
        about_prefix = ''
        cross_triad_prefix = ''
    
    # Fix "In" dropdown - about PIANDT submenu
    in_about_pattern = r'(<li>\s*<a href="[^"]*in/about_piandt/in_about_piandt\.html"[^>]*>about PIANDT[^<]*</a>\s*<ul>\s*<li><a href="[^"]*in/about_piandt/in_mission_vision\.html"[^>]*>our mission and vision</a></li>\s*<li><a href="[^"]*in/about_piandt/in_charitable_purposes\.html"[^>]*>charitable purposes</a></li>\s*<li><a href="[^"]*in/about_piandt/in_our_approach\.html"[^>]*>Our approach</a></li>\s*</ul>)'
    
    # Calculate correct paths for In dropdown
    if triad == 'in':
        in_about_base = f'{about_prefix}in_about_piandt.html'
        in_mission = f'{about_prefix}in_mission_vision.html'
        in_charitable = f'{about_prefix}in_charitable_purposes.html'
        in_approach = f'{about_prefix}in_our_approach.html'
        in_trustees = f'{about_prefix}in_trustees.html'
        in_governance = f'{about_prefix}in_governance.html'
    elif triad:
        in_about_base = f'{cross_triad_prefix}in/about_piandt/in_about_piandt.html'
        in_mission = f'{cross_triad_prefix}in/about_piandt/in_mission_vision.html'
        in_charitable = f'{cross_triad_prefix}in/about_piandt/in_charitable_purposes.html'
        in_approach = f'{cross_triad_prefix}in/about_piandt/in_our_approach.html'
        in_trustees = f'{cross_triad_prefix}in/about_piandt/in_trustees.html'
        in_governance = f'{cross_triad_prefix}in/about_piandt/in_governance.html'
    else:
        in_about_base = 'in/about_piandt/in_about_piandt.html'
        in_mission = 'in/about_piandt/in_mission_vision.html'
        in_charitable = 'in/about_piandt/in_charitable_purposes.html'
        in_approach = 'in/about_piandt/in_our_approach.html'
        in_trustees = 'in/about_piandt/in_trustees.html'
        in_governance = 'in/about_piandt/in_governance.html'
    
    in_about_replacement = f'''<li>
                            <a href="{in_about_base}" class="dropdown-link">about PIANDT <span class="dropdown-arrow">▶</span></a>
                            <ul>
                                <li><a href="{in_mission}" class="submenu-link">our mission and vision</a></li>
                                <li><a href="{in_charitable}" class="submenu-link">charitable purposes</a></li>
                                <li><a href="{in_approach}" class="submenu-link">Our approach</a></li>
                                <li><a href="{in_trustees}" class="submenu-link">trustees</a></li>
                                <li><a href="{in_governance}" class="submenu-link">governance</a></li>
                            </ul>
                        </li>'''
    
    # Fix Proc dropdown - about PIANDT submenu
    if triad == 'proc':
        proc_about_base = f'{about_prefix}proc_about_piandt.html'
        proc_mission = f'{about_prefix}proc_mission_vision.html'
        proc_charitable = f'{about_prefix}proc_charitable_purposes.html'
        proc_approach = f'{about_prefix}proc_our_approach.html'
        proc_trustees = f'{about_prefix}proc_trustees.html'
        proc_governance = f'{about_prefix}proc_governance.html'
    elif triad:
        proc_about_base = f'{cross_triad_prefix}processing/about_piandt/proc_about_piandt.html'
        proc_mission = f'{cross_triad_prefix}processing/about_piandt/proc_mission_vision.html'
        proc_charitable = f'{cross_triad_prefix}processing/about_piandt/proc_charitable_purposes.html'
        proc_approach = f'{cross_triad_prefix}processing/about_piandt/proc_our_approach.html'
        proc_trustees = f'{cross_triad_prefix}processing/about_piandt/proc_trustees.html'
        proc_governance = f'{cross_triad_prefix}processing/about_piandt/proc_governance.html'
    else:
        proc_about_base = 'processing/about_piandt/proc_about_piandt.html'
        proc_mission = 'processing/about_piandt/proc_mission_vision.html'
        proc_charitable = 'processing/about_piandt/proc_charitable_purposes.html'
        proc_approach = 'processing/about_piandt/proc_our_approach.html'
        proc_trustees = 'processing/about_piandt/proc_trustees.html'
        proc_governance = 'processing/about_piandt/proc_governance.html'
    
    proc_about_replacement = f'''<li>
                            <a href="{proc_about_base}" class="dropdown-link">about PIANDT <span class="dropdown-arrow">▶</span></a>
                            <ul>
                                <li><a href="{proc_mission}" class="submenu-link">our mission and vision</a></li>
                                <li><a href="{proc_charitable}" class="submenu-link">charitable purposes</a></li>
                                <li><a href="{proc_approach}" class="submenu-link">Our approach</a></li>
                                <li><a href="{proc_trustees}" class="submenu-link">trustees</a></li>
                                <li><a href="{proc_governance}" class="submenu-link">governance</a></li>
                            </ul>
                        </li>'''
    
    # Fix Out dropdown - about PIANDT submenu
    if triad == 'out':
        out_about_base = f'{about_prefix}out_about_piandt.html'
        out_mission = f'{about_prefix}out_mission_vision.html'
        out_charitable = f'{about_prefix}out_charitable_purposes.html'
        out_approach = f'{about_prefix}out_our_approach.html'
        out_trustees = f'{about_prefix}out_trustees.html'
        out_governance = f'{about_prefix}out_governance.html'
    elif triad:
        out_about_base = f'{cross_triad_prefix}out/about_piandt/out_about_piandt.html'
        out_mission = f'{cross_triad_prefix}out/about_piandt/out_mission_vision.html'
        out_charitable = f'{cross_triad_prefix}out/about_piandt/out_charitable_purposes.html'
        out_approach = f'{cross_triad_prefix}out/about_piandt/out_our_approach.html'
        out_trustees = f'{cross_triad_prefix}out/about_piandt/out_trustees.html'
        out_governance = f'{cross_triad_prefix}out/about_piandt/out_governance.html'
    else:
        out_about_base = 'out/about_piandt/out_about_piandt.html'
        out_mission = 'out/about_piandt/out_mission_vision.html'
        out_charitable = 'out/about_piandt/out_charitable_purposes.html'
        out_approach = 'out/about_piandt/out_our_approach.html'
        out_trustees = 'out/about_piandt/out_trustees.html'
        out_governance = 'out/about_piandt/out_governance.html'
    
    out_about_replacement = f'''<li>
                            <a href="{out_about_base}" class="dropdown-link">about PIANDT <span class="dropdown-arrow">▶</span></a>
                            <ul>
                                <li><a href="{out_mission}" class="submenu-link">our mission and vision</a></li>
                                <li><a href="{out_charitable}" class="submenu-link">charitable purposes</a></li>
                                <li><a href="{out_approach}" class="submenu-link">Our approach</a></li>
                                <li><a href="{out_trustees}" class="submenu-link">trustees</a></li>
                                <li><a href="{out_governance}" class="submenu-link">governance</a></li>
                            </ul>
                        </li>'''
    
    # Replace In dropdown about PIANDT (various patterns)
    patterns_in = [
        (r'(<li>\s*<a href="[^"]*in/about_piandt/in_about_piandt\.html"[^>]*>about PIANDT[^<]*</a>\s*<ul>\s*<li><a href="[^"]*in/about_piandt/in_mission_vision\.html"[^>]*>our mission and vision</a></li>\s*<li><a href="[^"]*in/about_piandt/in_charitable_purposes\.html"[^>]*>charitable purposes</a></li>\s*<li><a href="[^"]*in/about_piandt/in_our_approach\.html"[^>]*>Our approach</a></li>\s*</ul>\s*</li>)', in_about_replacement),
        (r'(<li>\s*<a href="[^"]*about_piandt/in_about_piandt\.html"[^>]*>about PIANDT[^<]*</a>\s*<ul>\s*<li><a href="[^"]*about_piandt/in_mission_vision\.html"[^>]*>our mission and vision</a></li>\s*<li><a href="[^"]*about_piandt/in_charitable_purposes\.html"[^>]*>charitable purposes</a></li>\s*<li><a href="[^"]*about_piandt/in_our_approach\.html"[^>]*>Our approach</a></li>\s*</ul>\s*</li>)', in_about_replacement),
    ]
    
    for pattern, replacement in patterns_in:
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # Replace Proc dropdown about PIANDT
    patterns_proc = [
        (r'(<li>\s*<a href="[^"]*processing/about_piandt/proc_about_piandt\.html"[^>]*>about PIANDT[^<]*</a>\s*<ul>\s*<li><a href="[^"]*processing/about_piandt/proc_mission_vision\.html"[^>]*>our mission and vision</a></li>\s*<li><a href="[^"]*processing/about_piandt/proc_charitable_purposes\.html"[^>]*>charitable purposes</a></li>\s*<li><a href="[^"]*processing/about_piandt/proc_our_approach\.html"[^>]*>Our approach</a></li>\s*</ul>\s*</li>)', proc_about_replacement),
        (r'(<li>\s*<a href="[^"]*about_piandt/proc_about_piandt\.html"[^>]*>about PIANDT[^<]*</a>\s*<ul>\s*<li><a href="[^"]*about_piandt/proc_mission_vision\.html"[^>]*>our mission and vision</a></li>\s*<li><a href="[^"]*about_piandt/proc_charitable_purposes\.html"[^>]*>charitable purposes</a></li>\s*<li><a href="[^"]*about_piandt/proc_our_approach\.html"[^>]*>Our approach</a></li>\s*</ul>\s*</li>)', proc_about_replacement),
    ]
    
    for pattern, replacement in patterns_proc:
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # Replace Out dropdown about PIANDT
    patterns_out = [
        (r'(<li>\s*<a href="[^"]*out/about_piandt/out_about_piandt\.html"[^>]*>about PIANDT[^<]*</a>\s*<ul>\s*<li><a href="[^"]*out/about_piandt/out_mission_vision\.html"[^>]*>our mission and vision</a></li>\s*<li><a href="[^"]*out/about_piandt/out_charitable_purposes\.html"[^>]*>charitable purposes</a></li>\s*<li><a href="[^"]*out/about_piandt/out_our_approach\.html"[^>]*>Our approach</a></li>\s*</ul>\s*</li>)', out_about_replacement),
        (r'(<li>\s*<a href="[^"]*about_piandt/out_about_piandt\.html"[^>]*>about PIANDT[^<]*</a>\s*<ul>\s*<li><a href="[^"]*about_piandt/out_mission_vision\.html"[^>]*>our mission and vision</a></li>\s*<li><a href="[^"]*about_piandt/out_charitable_purposes\.html"[^>]*>charitable purposes</a></li>\s*<li><a href="[^"]*about_piandt/out_our_approach\.html"[^>]*>Our approach</a></li>\s*</ul>\s*</li>)', out_about_replacement),
    ]
    
    for pattern, replacement in patterns_out:
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    if content != original:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        fixes_made += 1
        print(f"✓ Updated navigation menu in {rel_path}")

print(f"\n✓ Updated {fixes_made} files")



