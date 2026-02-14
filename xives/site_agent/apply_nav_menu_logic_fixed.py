#!/usr/bin/env python3
"""
Apply nav-menu and breadcrumb logic from proc_units.html to all pages - FIXED VERSION
This version has proper change detection and safety limits to prevent infinite loops
"""

from pathlib import Path
import re
import sys

def get_page_info(file_path, base_dir):
    """Extract page information"""
    rel_path = file_path.relative_to(base_dir)
    path_parts = str(rel_path).split('/')
    filename = path_parts[-1]
    
    triad = None
    section = None
    is_main_page = False
    
    if 'in/' in str(rel_path):
        triad = 'in'
        if len(path_parts) == 2 and filename == 'in.html':
            is_main_page = True
        elif 'about_piandt' in str(rel_path):
            section = 'about_piandt'
        elif 'units' in str(rel_path):
            section = 'units'
    elif 'processing/' in str(rel_path):
        triad = 'processing'
        if len(path_parts) == 2 and filename == 'processing.html':
            is_main_page = True
        elif 'about_piandt' in str(rel_path):
            section = 'about_piandt'
        elif 'units' in str(rel_path):
            section = 'units'
    elif 'out/' in str(rel_path):
        triad = 'out'
        if len(path_parts) == 2 and filename == 'out.html':
            is_main_page = True
        elif 'about_piandt' in str(rel_path):
            section = 'about_piandt'
        elif 'units' in str(rel_path):
            section = 'units'
    
    depth = len(path_parts) - 1
    
    return {
        'triad': triad,
        'section': section,
        'is_main_page': is_main_page,
        'filename': filename,
        'path': rel_path,
        'depth': depth,
        'path_parts': path_parts
    }

def build_breadcrumb(page_info):
    """Build breadcrumb based on page info"""
    parts = []
    depth = page_info['depth']
    triad = page_info['triad']
    
    if triad:
        triad_name = 'In' if triad == 'in' else 'Proc' if triad == 'processing' else 'Out'
        if depth == 1:
            triad_href = f"{triad}.html"
        else:
            triad_href = '../' * (depth - 1) + f"{triad}/{triad}.html"
        parts.append((triad_name, triad_href))
        
        if page_info['section']:
            section_name = 'about PIANDT' if page_info['section'] == 'about_piandt' else 'units'
            if depth == 2:
                section_href = f"{triad}_{page_info['section']}.html"
            else:
                section_href = '../' * (depth - 2) + f"{triad}_{page_info['section']}.html"
            parts.append((section_name, section_href))
    
    breadcrumb_links = []
    for i, (name, href) in enumerate(parts):
        if i == 0:
            breadcrumb_links.append(f'<a href="{href}" style="text-decoration: none; color: inherit;">{name}</a>')
        else:
            breadcrumb_links.append(f'-&gt;<a href="{href}" style="text-decoration: none; color: inherit;">{name}</a>')
    
    return f'<span class="logo-suffix">{"".join(breadcrumb_links)}</span>'

def build_nav_menu(page_info):
    """Build nav-menu based on page info - using logic from proc_units.html"""
    triad = page_info['triad']
    section = page_info['section']
    depth = page_info['depth']
    
    file_prefix = 'in_' if triad == 'in' else 'proc_' if triad == 'processing' else 'out_'
    
    if page_info['is_main_page']:
        prefix = '' if depth == 1 else '../' * (depth - 1)
        triad_name = 'In' if triad == 'in' else 'Proc' if triad == 'processing' else 'Out'
        return f'''            <ul class="nav-menu">
                <li class="dropdown">
                    <a href="{triad}.html" class="nav-link">{triad_name} <span class="dropdown-arrow">▼</span></a>
                    <ul class="dropdown-menu">
                        <li>
                            <a href="{prefix}about_piandt/{file_prefix}about_piandt.html" class="dropdown-link">about PIANDT <span class="dropdown-arrow">▶</span></a>
                            <ul>
                                <li><a href="{prefix}about_piandt/{file_prefix}mission_vision.html" class="submenu-link">our mission and vision</a></li>
                                <li><a href="{prefix}about_piandt/{file_prefix}charitable_purposes.html" class="submenu-link">charitable purposes</a></li>
                                <li><a href="{prefix}about_piandt/{file_prefix}our_approach.html" class="submenu-link">our approach</a></li>
                                <li><a href="{prefix}about_piandt/{file_prefix}trustees.html" class="submenu-link">trustees</a></li>
                                <li><a href="{prefix}about_piandt/{file_prefix}governance.html" class="submenu-link">governance</a></li>
                            </ul>
                        </li>
                        <li>
                            <a href="{prefix}units/{file_prefix}units.html" class="dropdown-link">units <span class="dropdown-arrow">▶</span></a>
                        </li>
                    </ul>
                </li>
            </ul>'''
    
    elif section == 'about_piandt' and depth == 2:
        return f'''            <ul class="nav-menu">
                <li class="dropdown">
                    <a href="{file_prefix}about_piandt.html" class="nav-link">about PIANDT <span class="dropdown-arrow">▼</span></a>
                    <ul class="dropdown-menu">
                        <li><a href="{file_prefix}mission_vision.html" class="dropdown-link">our mission and vision</a></li>
                        <li><a href="{file_prefix}charitable_purposes.html" class="dropdown-link">charitable purposes</a></li>
                        <li><a href="{file_prefix}our_approach.html" class="dropdown-link">our approach</a></li>
                        <li><a href="{file_prefix}trustees.html" class="dropdown-link">trustees</a></li>
                        <li><a href="{file_prefix}governance.html" class="dropdown-link">governance</a></li>
                    </ul>
                </li>
            </ul>'''
    
    elif section == 'units' and depth == 2:
        return f'''            <ul class="nav-menu">
                <li class="dropdown">
                    <a href="{file_prefix}units.html" class="nav-link">units <span class="dropdown-arrow">▼</span></a>
                    <ul class="dropdown-menu">
                        <li>
                            <a href="../about_piandt/{file_prefix}about_piandt.html" class="dropdown-link">about PIANDT <span class="dropdown-arrow">▶</span></a>
                            <ul>
                                <li><a href="../about_piandt/{file_prefix}mission_vision.html" class="submenu-link">our mission and vision</a></li>
                                <li><a href="../about_piandt/{file_prefix}charitable_purposes.html" class="submenu-link">charitable purposes</a></li>
                                <li><a href="../about_piandt/{file_prefix}our_approach.html" class="submenu-link">our approach</a></li>
                                <li><a href="../about_piandt/{file_prefix}trustees.html" class="submenu-link">trustees</a></li>
                                <li><a href="../about_piandt/{file_prefix}governance.html" class="submenu-link">governance</a></li>
                            </ul>
                        </li>
                        <li>
                            <a href="miu/{file_prefix}miu.html" class="dropdown-link">machine intelligence <span class="dropdown-arrow">▶</span></a>
                        </li>
                    </ul>
                </li>
            </ul>'''
    
    elif section == 'units' and depth > 2:
        prefix = '../' * (depth - 2)
        return f'''            <ul class="nav-menu">
                <li class="dropdown">
                    <a href="{prefix}{file_prefix}units.html" class="nav-link">units <span class="dropdown-arrow">▼</span></a>
                    <ul class="dropdown-menu">
                        <li>
                            <a href="{prefix}../about_piandt/{file_prefix}about_piandt.html" class="dropdown-link">about PIANDT <span class="dropdown-arrow">▶</span></a>
                            <ul>
                                <li><a href="{prefix}../about_piandt/{file_prefix}mission_vision.html" class="submenu-link">our mission and vision</a></li>
                                <li><a href="{prefix}../about_piandt/{file_prefix}charitable_purposes.html" class="submenu-link">charitable purposes</a></li>
                                <li><a href="{prefix}../about_piandt/{file_prefix}our_approach.html" class="submenu-link">our approach</a></li>
                                <li><a href="{prefix}../about_piandt/{file_prefix}trustees.html" class="submenu-link">trustees</a></li>
                                <li><a href="{prefix}../about_piandt/{file_prefix}governance.html" class="submenu-link">governance</a></li>
                            </ul>
                        </li>
                        <li>
                            <a href="{prefix}miu/{file_prefix}miu.html" class="dropdown-link">machine intelligence <span class="dropdown-arrow">▶</span></a>
                        </li>
                    </ul>
                </li>
            </ul>'''
    
    return None

def find_complete_nav_menu(content, start_pos):
    """Find complete nav-menu by counting ul tags - with safety limit"""
    depth = 0
    i = start_pos
    max_iterations = 50000  # Safety limit
    iterations = 0
    
    while i < len(content) and iterations < max_iterations:
        iterations += 1
        if i + 4 <= len(content) and content[i:i+4] == '<ul ':
            depth += 1
        elif i + 4 <= len(content) and content[i:i+4] == '<ul>':
            depth += 1
        elif i + 5 <= len(content) and content[i:i+5] == '</ul>':
            depth -= 1
            if depth == 0:
                return i + 5
        i += 1
    
    return -1  # Not found or exceeded limit

def fix_page(file_path, base_dir):
    """Fix nav-menu and breadcrumb for a single page - FIXED VERSION"""
    try:
        page_info = get_page_info(file_path, base_dir)
        sys.stdout.write(f"Processing: {file_path.relative_to(base_dir)}... ")
        sys.stdout.flush()
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes = []
        
        # Find nav-container
        nav_container_match = re.search(r'(<div class="nav-container">.*?</div>)', content, re.DOTALL)
        if not nav_container_match:
            print("✗ No nav-container")
            return False, []
        
        nav_container_content = nav_container_match.group(1)
        
        # Fix breadcrumb
        breadcrumb_match = re.search(r'(<span class="logo-suffix">.*?</span>)', nav_container_content, re.DOTALL)
        expected_breadcrumb = build_breadcrumb(page_info)
        
        if breadcrumb_match:
            current_breadcrumb = breadcrumb_match.group(0)
            if current_breadcrumb != expected_breadcrumb:
                nav_container_content = nav_container_content.replace(breadcrumb_match.group(0), expected_breadcrumb)
                changes.append('breadcrumb')
        else:
            # Breadcrumb missing - add it after logo-subtitle
            logo_subtitle_match = re.search(r'(<p class="logo-subtitle">.*?</p>)', nav_container_content, re.DOTALL)
            if logo_subtitle_match:
                logo_end = nav_container_content.find('</p>', nav_container_content.find('<p class="logo-subtitle">')) + 4
                nav_container_content = nav_container_content[:logo_end] + '\n                ' + expected_breadcrumb + nav_container_content[logo_end:]
                changes.append('breadcrumb')
        
        # Remove ALL nav-menus from nav-container (with safety limit)
        removed = 0
        max_removals = 20  # Safety limit
        while removed < max_removals:
            nav_start = nav_container_content.find('<ul class="nav-menu">')
            if nav_start == -1:
                break
            
            nav_end = find_complete_nav_menu(nav_container_content, nav_start)
            if nav_end == -1:
                # Couldn't find end - try to find next nav-menu start as fallback
                next_start = nav_container_content.find('<ul class="nav-menu">', nav_start + 1)
                if next_start != -1:
                    nav_container_content = nav_container_content[:nav_start] + nav_container_content[next_start:]
                    removed += 1
                    continue
                else:
                    # Remove everything from nav_start to end of container (last resort)
                    nav_container_end = nav_container_content.find('</div>', nav_start)
                    if nav_container_end != -1:
                        nav_container_content = nav_container_content[:nav_start] + nav_container_content[nav_container_end:]
                    break
            
            nav_container_content = nav_container_content[:nav_start] + nav_container_content[nav_end:]
            removed += 1
        
        if removed > 0:
            changes.append(f'removed-{removed}-nav-menus')
        
        # Add new nav-menu after breadcrumb
        expected_nav_menu = build_nav_menu(page_info)
        if expected_nav_menu:
            # Check if nav-menu already exists and is correct
            existing_nav_count = len(re.findall(r'<ul class="nav-menu">', nav_container_content))
            
            if existing_nav_count == 0:
                # No nav-menu - add it after breadcrumb
                breadcrumb_pos = nav_container_content.find('</span>', nav_container_content.find('<span class="logo-suffix">'))
                if breadcrumb_pos != -1:
                    breadcrumb_end = breadcrumb_pos + 7
                    nav_container_content = (nav_container_content[:breadcrumb_end] + 
                                           '\n            ' + expected_nav_menu + 
                                           nav_container_content[breadcrumb_end:])
                    changes.append('nav-menu')
            elif existing_nav_count == 1:
                # Check if existing nav-menu matches expected
                existing_nav_match = re.search(r'<ul class="nav-menu">.*?</ul>', nav_container_content, re.DOTALL)
                if existing_nav_match:
                    existing_nav = existing_nav_match.group(0)
                    # Simple check: does it have the right nav-link text?
                    expected_nav_link = 'about PIANDT' if page_info['section'] == 'about_piandt' else 'units' if page_info['section'] == 'units' else ('In' if page_info['triad'] == 'in' else 'Proc' if page_info['triad'] == 'processing' else 'Out')
                    if expected_nav_link not in existing_nav:
                        # Replace existing nav-menu
                        nav_start = existing_nav_match.start()
                        nav_end = existing_nav_match.end()
                        nav_container_content = nav_container_content[:nav_start] + expected_nav_menu + nav_container_content[nav_end:]
                        changes.append('nav-menu')
            else:
                # Multiple nav-menus - remove all and add one
                # (Already removed above, so just add)
                breadcrumb_pos = nav_container_content.find('</span>', nav_container_content.find('<span class="logo-suffix">'))
                if breadcrumb_pos != -1:
                    breadcrumb_end = breadcrumb_pos + 7
                    nav_container_content = (nav_container_content[:breadcrumb_end] + 
                                           '\n            ' + expected_nav_menu + 
                                           nav_container_content[breadcrumb_end:])
                    changes.append('nav-menu')
        
        # Replace nav-container in original content
        content = content.replace(nav_container_match.group(0), nav_container_content)
        
        # Remove nav-menus outside nav-container (with safety limit)
        removed_outside = 0
        max_removals = 20
        while removed_outside < max_removals:
            nav_start = content.find('<ul class="nav-menu">')
            if nav_start == -1:
                break
            
            # Check if it's inside nav-container
            nav_container_start = content.rfind('<div class="nav-container">', 0, nav_start)
            if nav_container_start != -1:
                nav_container_end = content.find('</div>', nav_container_start)
                if nav_container_end != -1 and nav_start < nav_container_end:
                    # It's inside nav-container, skip it by moving search position
                    nav_start = nav_container_end + 6
                    continue
            
            # It's outside nav-container, remove it
            nav_end = find_complete_nav_menu(content, nav_start)
            if nav_end == -1:
                # Couldn't find end - try next nav-menu as fallback
                next_start = content.find('<ul class="nav-menu">', nav_start + 1)
                if next_start != -1:
                    content = content[:nav_start] + content[next_start:]
                    removed_outside += 1
                    continue
                else:
                    break
            
            content = content[:nav_start] + content[nav_end:]
            removed_outside += 1
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Fixed: {', '.join(changes)}")
            return True, changes
        else:
            print("✓ No changes needed")
            return False, []
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False, []

def main():
    base_dir = Path('.').resolve()
    
    html_files = [f for f in base_dir.rglob('*.html') 
                  if 'site_agent' not in str(f) and f.name != 'index.html']
    
    print(f"Applying nav-menu and breadcrumb logic to {len(html_files)} pages...")
    print("=" * 70)
    print("Reference: processing/units/proc_units.html")
    print("=" * 70)
    print()
    
    fixed_count = 0
    
    for i, html_file in enumerate(sorted(html_files), 1):
        fixed, changes = fix_page(html_file, base_dir)
        if fixed:
            fixed_count += 1
    
    print()
    print("=" * 70)
    print(f"\n✓ Fixed {fixed_count} pages")
    print("\nDone!")

if __name__ == '__main__':
    main()



