#!/usr/bin/env python3
"""
Apply nav-menu and breadcrumb logic from proc_units.html to all pages.
Logic: 
- Breadcrumb shows path hierarchy
- Nav-menu shows the section nav-link (units or about_piandt) with its children
"""

from pathlib import Path
import re

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
        # Add triad
        triad_name = 'In' if triad == 'in' else 'Proc' if triad == 'processing' else 'Out'
        if depth == 1:
            triad_href = f"{triad}.html"
        else:
            triad_href = '../' * (depth - 1) + f"{triad}/{triad}.html"
        parts.append((triad_name, triad_href))
        
        # Add section if exists
        if page_info['section']:
            section_name = 'about PIANDT' if page_info['section'] == 'about_piandt' else 'units'
            if depth == 2:
                section_href = f"{triad}_{page_info['section']}.html"
            else:
                section_href = '../' * (depth - 2) + f"{triad}_{page_info['section']}.html"
            parts.append((section_name, section_href))
    
    # Build breadcrumb HTML
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
    
    if page_info['is_main_page']:
        # Main page: Show triad nav-link with all children
        prefix = '' if depth == 1 else '../' * (depth - 1)
        triad_name = 'In' if triad == 'in' else 'Proc' if triad == 'processing' else 'Out'
        return f'''            <ul class="nav-menu">
                <li class="dropdown">
                    <a href="{triad}.html" class="nav-link">{triad_name} <span class="dropdown-arrow">▼</span></a>
                    <ul class="dropdown-menu">
                        <li>
                            <a href="{prefix}about_piandt/{triad}_about_piandt.html" class="dropdown-link">about PIANDT <span class="dropdown-arrow">▶</span></a>
                            <ul>
                                <li><a href="{prefix}about_piandt/{triad}_mission_vision.html" class="submenu-link">our mission and vision</a></li>
                                <li><a href="{prefix}about_piandt/{triad}_charitable_purposes.html" class="submenu-link">charitable purposes</a></li>
                                <li><a href="{prefix}about_piandt/{triad}_our_approach.html" class="submenu-link">our approach</a></li>
                                <li><a href="{prefix}about_piandt/{triad}_trustees.html" class="submenu-link">trustees</a></li>
                                <li><a href="{prefix}about_piandt/{triad}_governance.html" class="submenu-link">governance</a></li>
                            </ul>
                        </li>
                        <li>
                            <a href="{prefix}units/{triad}_units.html" class="dropdown-link">units <span class="dropdown-arrow">▶</span></a>
                        </li>
                    </ul>
                </li>
            </ul>'''
    
    elif section == 'about_piandt' and depth == 2:
        # about_piandt section page: Show "about PIANDT" nav-link
        # Use correct file prefix: in_, proc_, out_
        file_prefix = 'in_' if triad == 'in' else 'proc_' if triad == 'processing' else 'out_'
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
        # Units main page: Show "units" nav-link (like proc_units.html)
        # Use correct file prefix: in_, proc_, out_
        file_prefix = 'in_' if triad == 'in' else 'proc_' if triad == 'processing' else 'out_'
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
    
    else:
        # Deep pages: Use the same logic but adjust paths
        # For now, preserve existing structure but we'll need to handle this case
        return None

def fix_page(file_path, base_dir):
    """Fix nav-menu and breadcrumb for a single page"""
    page_info = get_page_info(file_path, base_dir)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes = []
    
    # Find nav-container
    nav_container_match = re.search(r'(<div class="nav-container">.*?</div>)', content, re.DOTALL)
    if not nav_container_match:
        return False, []
    
    nav_container_content = nav_container_match.group(1)
    
    # Fix breadcrumb inside nav-container
    breadcrumb_pattern = r'(<span class="logo-suffix">.*?</span>)'
    breadcrumb_match = re.search(breadcrumb_pattern, nav_container_content, re.DOTALL)
    
    if breadcrumb_match:
        new_breadcrumb = build_breadcrumb(page_info)
        nav_container_content = nav_container_content.replace(breadcrumb_match.group(0), new_breadcrumb)
        changes.append('breadcrumb')
    
    # Remove ALL existing nav-menus from nav-container
    # Find all nav-menu occurrences and remove them
    while True:
        nav_menu_match = re.search(r'<ul class="nav-menu">.*?</ul>', nav_container_content, re.DOTALL)
        if not nav_menu_match:
            break
        # Find complete nav-menu by counting ul tags
        nav_start = nav_container_content.find('<ul class="nav-menu">')
        if nav_start != -1:
            depth = 0
            i = nav_start
            nav_end = -1
            while i < len(nav_container_content):
                if nav_container_content[i:i+4] == '<ul ' or (i < len(nav_container_content) - 4 and nav_container_content[i:i+4] == '<ul>'):
                    depth += 1
                elif nav_container_content[i:i+5] == '</ul>':
                    depth -= 1
                    if depth == 0:
                        nav_end = i + 5
                        break
                i += 1
            
            if nav_end != -1:
                nav_container_content = nav_container_content[:nav_start] + nav_container_content[nav_end:]
            else:
                break
        else:
            break
    
    # Add new nav-menu after breadcrumb
    new_nav_menu = build_nav_menu(page_info)
    if new_nav_menu:
        # Find breadcrumb position in nav-container
        breadcrumb_pos = nav_container_content.find('</span>', nav_container_content.find('<span class="logo-suffix">'))
        if breadcrumb_pos != -1:
            breadcrumb_end = breadcrumb_pos + 7  # Include </span>
            # Insert nav-menu after breadcrumb
            nav_container_content = (nav_container_content[:breadcrumb_end] + 
                                   '\n            ' + new_nav_menu + 
                                   nav_container_content[breadcrumb_end:])
            changes.append('nav-menu')
    
    # Replace nav-container in original content
    content = content.replace(nav_container_match.group(0), nav_container_content)
    
    # Also remove any nav-menus outside nav-container
    while True:
        nav_start = content.find('<ul class="nav-menu">')
        if nav_start == -1:
            break
        
        # Check if it's inside nav-container
        nav_container_start = content.rfind('<div class="nav-container">', 0, nav_start)
        nav_container_end = content.find('</div>', nav_container_start) if nav_container_start != -1 else -1
        
        if nav_container_start != -1 and nav_container_end != -1 and nav_start < nav_container_end:
            # It's inside nav-container, skip it
            nav_start = nav_container_end
            continue
        
        # It's outside nav-container, remove it
        depth = 0
        i = nav_start
        nav_end = -1
        while i < len(content):
            if content[i:i+4] == '<ul ' or (i < len(content) - 4 and content[i:i+4] == '<ul>'):
                depth += 1
            elif content[i:i+5] == '</ul>':
                depth -= 1
                if depth == 0:
                    nav_end = i + 5
                    break
            i += 1
        
        if nav_end != -1:
            content = content[:nav_start] + content[nav_end:]
        else:
            break
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, changes
    return False, []

def main():
    base_dir = Path('.').resolve()
    
    # Get all HTML files except index.html
    html_files = [f for f in base_dir.rglob('*.html') 
                  if 'site_agent' not in str(f) and f.name != 'index.html']
    
    print(f"Applying nav-menu and breadcrumb logic to {len(html_files)} pages...")
    print("=" * 70)
    print("Reference: processing/units/proc_units.html")
    print("=" * 70)
    
    fixed_count = 0
    issues = []
    
    for html_file in sorted(html_files):
        try:
            fixed, changes = fix_page(html_file, base_dir)
            if fixed:
                fixed_count += 1
                print(f"✓ Fixed {html_file.relative_to(base_dir)}: {', '.join(changes)}")
        except Exception as e:
            issues.append((html_file, str(e)))
            print(f"✗ Error: {html_file.relative_to(base_dir)} - {e}")
    
    print("=" * 70)
    print(f"\n✓ Fixed {fixed_count} pages")
    if issues:
        print(f"✗ {len(issues)} errors")
        for file, error in issues[:5]:
            print(f"  - {file}: {error}")
    
    print("\nDone!")

if __name__ == '__main__':
    main()

