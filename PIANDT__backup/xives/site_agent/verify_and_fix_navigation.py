#!/usr/bin/env python3
"""
Verify and fix navigation menus and breadcrumbs for all pages.
Navigation logic: When a menu item is clicked, display the child menus in place of the nav-menu.
"""

from pathlib import Path
import re
import os

def get_page_info(file_path, base_dir):
    """Extract page information from file path"""
    rel_path = file_path.relative_to(base_dir)
    path_parts = str(rel_path).split('/')
    
    # Determine triad, section, and page type
    triad = None
    section = None
    page_type = None
    filename = path_parts[-1]
    
    if 'in/' in str(rel_path):
        triad = 'in'
        if 'about_piandt' in str(rel_path):
            section = 'about_piandt'
        elif 'units' in str(rel_path):
            section = 'units'
    elif 'processing/' in str(rel_path):
        triad = 'processing'
        if 'about_piandt' in str(rel_path):
            section = 'about_piandt'
        elif 'units' in str(rel_path):
            section = 'units'
    elif 'out/' in str(rel_path):
        triad = 'out'
        if 'about_piandt' in str(rel_path):
            section = 'about_piandt'
        elif 'units' in str(rel_path):
            section = 'units'
    
    # Determine if it's a main page (triad root)
    is_main_page = (len(path_parts) == 2 and 
                   (filename == 'in.html' or filename == 'processing.html' or filename == 'out.html'))
    
    return {
        'triad': triad,
        'section': section,
        'is_main_page': is_main_page,
        'filename': filename,
        'path': rel_path,
        'depth': len(path_parts) - 1
    }

def calculate_breadcrumb_path(page_info, base_dir):
    """Calculate correct breadcrumb path"""
    parts = []
    
    if page_info['triad']:
        # Add triad
        triad_name = 'In' if page_info['triad'] == 'in' else 'Proc' if page_info['triad'] == 'processing' else 'Out'
        triad_href = '../' * (page_info['depth'] - 1) + f"{page_info['triad']}/{page_info['triad']}.html" if page_info['depth'] > 1 else f"{page_info['triad']}.html"
        parts.append((triad_name, triad_href))
        
        # Add section if exists
        if page_info['section']:
            section_name = 'about PIANDT' if page_info['section'] == 'about_piandt' else 'units'
            if page_info['is_main_page']:
                section_href = f"{page_info['section']}/{page_info['triad']}_{page_info['section']}.html"
            else:
                section_href = f"{page_info['triad']}_{page_info['section']}.html" if page_info['depth'] == 2 else f"../{page_info['triad']}_{page_info['section']}.html"
            parts.append((section_name, section_href))
    
    return parts

def get_expected_nav_menu(page_info):
    """Determine what nav-menu should be shown based on navigation logic"""
    # Navigation logic: When a menu item is clicked, display the child menus in place of the nav-menu
    
    if page_info['is_main_page']:
        # Main page: Show the triad nav-link with all child menus
        return {
            'type': 'triad_main',
            'nav_link_text': 'In' if page_info['triad'] == 'in' else 'Proc' if page_info['triad'] == 'processing' else 'Out',
            'nav_link_href': f"{page_info['triad']}.html"
        }
    elif page_info['section'] == 'about_piandt':
        # Section page: Show the section nav-link (child of triad)
        return {
            'type': 'section',
            'nav_link_text': 'about PIANDT',
            'nav_link_href': f"{page_info['triad']}_about_piandt.html" if page_info['depth'] == 2 else f"../{page_info['triad']}_about_piandt.html"
        }
    elif page_info['section'] == 'units':
        # Units page: Show the units nav-link (child of triad)
        return {
            'type': 'section',
            'nav_link_text': 'units',
            'nav_link_href': f"{page_info['triad']}_units.html" if page_info['depth'] == 2 else f"../{page_info['triad']}_units.html"
        }
    else:
        # Deep page (e.g., units/miu/vision): Show parent section nav-link
        return {
            'type': 'section',
            'nav_link_text': 'units',
            'nav_link_href': f"../../{page_info['triad']}_units.html" if page_info['depth'] > 3 else f"../{page_info['triad']}_units.html"
        }

def fix_nav_menu(content, page_info, base_dir):
    """Fix the nav-menu to show correct navigation"""
    expected_nav = get_expected_nav_menu(page_info, base_dir)
    
    # Find the nav-menu
    nav_menu_pattern = r'(<ul class="nav-menu">.*?</ul>)'
    nav_menu_match = re.search(nav_menu_pattern, content, re.DOTALL)
    
    if not nav_menu_match:
        return content, False
    
    current_nav_menu = nav_menu_match.group(1)
    
    # Check if nav-menu is correct
    nav_link_match = re.search(r'<a[^>]*class="nav-link"[^>]*>(.*?)</a>', current_nav_menu, re.DOTALL)
    if nav_link_match:
        current_text = re.sub(r'<[^>]+>', '', nav_link_match.group(1)).strip()
        if expected_nav['nav_link_text'].lower() in current_text.lower():
            # Nav-menu is correct
            return content, False
    
    # Need to fix nav-menu
    # Build the correct nav-menu HTML
    triad = page_info['triad']
    
    if expected_nav['type'] == 'triad_main':
        # Main page: Show triad with all child menus
        new_nav_menu = f'''            <ul class="nav-menu">
                <li class="dropdown">
                    <a href="{expected_nav['nav_link_href']}" class="nav-link">{expected_nav['nav_link_text']} <span class="dropdown-arrow">▼</span></a>
                    <ul class="dropdown-menu">
                        <li>
                            <a href="about_piandt/{triad}_about_piandt.html" class="dropdown-link">about PIANDT <span class="dropdown-arrow">▶</span></a>
                            <ul>
                                <li><a href="about_piandt/{triad}_mission_vision.html" class="submenu-link">our mission and vision</a></li>
                                <li><a href="about_piandt/{triad}_charitable_purposes.html" class="submenu-link">charitable purposes</a></li>
                                <li><a href="about_piandt/{triad}_our_approach.html" class="submenu-link">our approach</a></li>
                                <li><a href="about_piandt/{triad}_trustees.html" class="submenu-link">trustees</a></li>
                                <li><a href="about_piandt/{triad}_governance.html" class="submenu-link">governance</a></li>
                            </ul>
                        </li>
                        <li>
                            <a href="units/{triad}_units.html" class="dropdown-link">units <span class="dropdown-arrow">▶</span></a>
                        </li>
                    </ul>
                </li>
            </ul>'''
    else:
        # Section page: Show section nav-link with its child menus
        if expected_nav['nav_link_text'] == 'about PIANDT':
            new_nav_menu = f'''            <ul class="nav-menu">
                <li class="dropdown">
                    <a href="{expected_nav['nav_link_href']}" class="nav-link">about PIANDT <span class="dropdown-arrow">▼</span></a>
                    <ul class="dropdown-menu">
                        <li><a href="{triad}_mission_vision.html" class="dropdown-link">our mission and vision</a></li>
                        <li><a href="{triad}_charitable_purposes.html" class="dropdown-link">charitable purposes</a></li>
                        <li><a href="{triad}_our_approach.html" class="dropdown-link">our approach</a></li>
                        <li><a href="{triad}_trustees.html" class="dropdown-link">trustees</a></li>
                        <li><a href="{triad}_governance.html" class="dropdown-link">governance</a></li>
                    </ul>
                </li>
            </ul>'''
        else:  # units
            # For units pages, we need to check what child units exist
            # This is more complex, so we'll preserve the existing structure but fix paths
            new_nav_menu = current_nav_menu  # Keep existing for now, just fix paths
    
    # Replace nav-menu
    content = content.replace(current_nav_menu, new_nav_menu)
    return content, True

def fix_breadcrumb(content, page_info, base_dir):
    """Fix breadcrumb to show correct path"""
    breadcrumb_parts = calculate_breadcrumb_path(page_info, base_dir)
    
    # Find breadcrumb
    breadcrumb_pattern = r'(<span class="logo-suffix">.*?</span>)'
    breadcrumb_match = re.search(breadcrumb_pattern, content, re.DOTALL)
    
    if not breadcrumb_match:
        return content, False
    
    # Build correct breadcrumb
    breadcrumb_links = []
    for i, (name, href) in enumerate(breadcrumb_parts):
        if i == 0:
            breadcrumb_links.append(f'<a href="{href}" style="text-decoration: none; color: inherit;">{name}</a>')
        else:
            breadcrumb_links.append(f'-&gt;<a href="{href}" style="text-decoration: none; color: inherit;">{name}</a>')
    
    # Add current page if not already in breadcrumb
    current_page_name = page_info['filename'].replace(f"{page_info['triad']}_", "").replace(".html", "").replace("_", " ")
    if current_page_name not in ' '.join(breadcrumb_parts[-1][0] if breadcrumb_parts else []):
        breadcrumb_links.append(f'-&gt;<a href="{page_info["filename"]}" style="text-decoration: none; color: inherit;">{current_page_name}</a>')
    
    new_breadcrumb = f'<span class="logo-suffix">{"".join(breadcrumb_links)}</span>'
    
    # Replace breadcrumb
    content = content.replace(breadcrumb_match.group(1), new_breadcrumb)
    return content, True

def main():
    base_dir = Path('.').resolve()
    
    # Get all HTML files except index.html
    html_files = [f for f in base_dir.rglob('*.html') 
                  if 'site_agent' not in str(f) and f.name != 'index.html']
    
    print(f"Checking {len(html_files)} pages...")
    print("=" * 70)
    
    fixed_count = 0
    issues = []
    
    for html_file in sorted(html_files):
        try:
            page_info = get_page_info(html_file, base_dir)
            
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            nav_fixed = False
            breadcrumb_fixed = False
            
            # Fix nav-menu
            content, nav_fixed = fix_nav_menu(content, page_info, base_dir)
            
            # Fix breadcrumb
            content, breadcrumb_fixed = fix_breadcrumb(content, page_info, base_dir)
            
            if nav_fixed or breadcrumb_fixed:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed_count += 1
                changes = []
                if nav_fixed:
                    changes.append('nav-menu')
                if breadcrumb_fixed:
                    changes.append('breadcrumb')
                print(f"✓ Fixed {html_file.relative_to(base_dir)}: {', '.join(changes)}")
        except Exception as e:
            issues.append((html_file, str(e)))
            print(f"✗ Error: {html_file.relative_to(base_dir)} - {e}")
    
    print("=" * 70)
    print(f"\n✓ Fixed {fixed_count} pages")
    if issues:
        print(f"✗ {len(issues)} errors")
    
    print("\nDone!")

if __name__ == '__main__':
    main()

