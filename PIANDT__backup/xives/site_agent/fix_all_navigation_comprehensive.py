#!/usr/bin/env python3
"""
Comprehensive fix for navigation menus and breadcrumbs for all 52 pages.
Navigation logic: When a menu item is clicked, display the child menus in place of the nav-menu.
"""

from pathlib import Path
import re
import os

def get_page_info(file_path, base_dir):
    """Extract page information from file path"""
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

def get_expected_nav_menu(page_info, base_dir):
    """Determine what nav-menu should be shown based on navigation logic"""
    # Navigation logic: When a menu item is clicked, display the child menus in place of the nav-menu
    
    if page_info['is_main_page']:
        # Main triad page: Show triad nav-link with all children
        return {
            'type': 'triad_main',
            'nav_link_text': 'In' if page_info['triad'] == 'in' else 'Proc' if page_info['triad'] == 'processing' else 'Out',
            'nav_link_href': f"{page_info['triad']}.html"
        }
    elif page_info['section'] == 'about_piandt' and page_info['depth'] == 2:
        # about_piandt section page: Show "about PIANDT" nav-link
        return {
            'type': 'section_about',
            'nav_link_text': 'about PIANDT',
            'nav_link_href': f"{page_info['triad']}_about_piandt.html"
        }
    elif page_info['section'] == 'units' and page_info['depth'] == 2:
        # Units main page: Show "units" nav-link
        return {
            'type': 'section_units',
            'nav_link_text': 'units',
            'nav_link_href': f"{page_info['triad']}_units.html"
        }
    elif page_info['section'] == 'units' and page_info['depth'] > 2:
        # Deep unit pages: Need to determine from the actual file
        # Check if there's a unit-specific nav-link in the file
        try:
            with open(base_dir / page_info['path'], 'r') as f:
                content = f.read()
            
            # Look for existing nav-link to see what it should be
            nav_match = re.search(r'<a[^>]*class="nav-link"[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', content, re.DOTALL)
            if nav_match:
                existing_href = nav_match.group(1)
                existing_text = re.sub(r'<[^>]+>', '', nav_match.group(2)).strip()
                
                # If it's a self-referential link (points to current page), use it
                if existing_href == page_info['filename'] or existing_href.endswith(page_info['filename']):
                    return {
                        'type': 'unit_specific',
                        'nav_link_text': existing_text,
                        'nav_link_href': existing_href
                    }
        except:
            pass
        
        # Fallback: show units nav-link
        units_href = '../' * (page_info['depth'] - 2) + f"{page_info['triad']}_units.html"
        return {
            'type': 'section_units',
            'nav_link_text': 'units',
            'nav_link_href': units_href
        }
    else:
        # Fallback
        return {
            'type': 'section',
            'nav_link_text': 'units',
            'nav_link_href': f"../{page_info['triad']}_units.html"
        }

def build_nav_menu_html(expected_nav, page_info):
    """Build the correct nav-menu HTML"""
    triad = page_info['triad']
    depth = page_info['depth']
    
    if expected_nav['type'] == 'triad_main':
        # Main page: Show triad with all children
        prefix = '' if depth == 1 else '../' * (depth - 1)
        return f'''            <ul class="nav-menu">
                <li class="dropdown">
                    <a href="{expected_nav['nav_link_href']}" class="nav-link">{expected_nav['nav_link_text']} <span class="dropdown-arrow">▼</span></a>
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
    
    elif expected_nav['type'] == 'section_about':
        # about_piandt section: Show about PIANDT with children
        return f'''            <ul class="nav-menu">
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
    
    elif expected_nav['type'] == 'section_units':
        # Units section: Show units nav-link
        # For units pages, we need to preserve the existing structure but fix the nav-link
        # This is complex, so we'll read the existing menu and just fix the nav-link
        return None  # Signal to preserve existing structure but fix nav-link
    
    else:
        # Unit-specific: Preserve existing structure
        return None

def fix_nav_menu(content, page_info, base_dir):
    """Fix the nav-menu to show correct navigation"""
    expected_nav = get_expected_nav_menu(page_info, base_dir)
    
    # Find the nav-menu
    nav_menu_pattern = r'(<ul class="nav-menu">.*?</ul>)'
    nav_menu_match = re.search(nav_menu_pattern, content, re.DOTALL)
    
    if not nav_menu_match:
        return content, False
    
    current_nav_menu = nav_menu_match.group(1)
    
    # Check if nav-link is correct
    nav_link_match = re.search(r'<a[^>]*class="nav-link"[^>]*>(.*?)</a>', current_nav_menu, re.DOTALL)
    if nav_link_match:
        current_text = re.sub(r'<[^>]+>', '', nav_link_match.group(1)).strip()
        expected_text = expected_nav['nav_link_text']
        
        # Check if it matches (case-insensitive, allow for extra text)
        if expected_text.lower() in current_text.lower() or current_text.lower() in expected_text.lower():
            # Nav-menu is correct - just verify href
            href_match = re.search(r'<a[^>]*class="nav-link"[^>]*href=["\']([^"\']+)["\']', current_nav_menu)
            if href_match:
                current_href = href_match.group(1)
                # Normalize paths for comparison
                if current_href.replace('../', '').replace('./', '') == expected_nav['nav_link_href'].replace('../', '').replace('./', ''):
                    return content, False  # Already correct
    
    # Need to fix nav-menu
    new_nav_menu = build_nav_menu_html(expected_nav, page_info)
    
    if new_nav_menu:
        # Replace entire nav-menu
        content = content.replace(current_nav_menu, new_nav_menu)
        return content, True
    else:
        # Just fix the nav-link href and text
        # Replace nav-link
        new_nav_link = f'<a href="{expected_nav["nav_link_href"]}" class="nav-link">{expected_nav["nav_link_text"]} <span class="dropdown-arrow">▼</span></a>'
        content = re.sub(r'<a[^>]*class="nav-link"[^>]*>.*?</a>', new_nav_link, current_nav_menu, flags=re.DOTALL)
        content = content.replace(current_nav_menu, content)
        return content, True

def calculate_breadcrumb_path(page_info, base_dir):
    """Calculate correct breadcrumb path"""
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
            
            # For deep unit pages, add unit name
            if page_info['section'] == 'units' and depth > 2:
                # Extract unit name from path
                path_parts = page_info['path_parts']
                units_index = path_parts.index('units')
                if len(path_parts) > units_index + 1:
                    unit_part = path_parts[units_index + 1]
                    if unit_part.endswith('.html'):
                        unit_name = unit_part.replace('.html', '').replace(f"{triad}_", "")
                    else:
                        unit_name = unit_part
                    
                    # Get display name from file if possible
                    unit_file = base_dir / page_info['path'].parent / f"{triad}_{unit_name}.html"
                    if unit_file.exists() and depth == 3:
                        parts.append((unit_name, f"{triad}_{unit_name}.html"))
                    elif depth > 3:
                        # Deeper page - add parent unit
                        parent_unit = path_parts[-2] if not path_parts[-1].endswith('.html') else path_parts[-3]
                        parent_name = parent_unit.replace(f"{triad}_", "").replace(".html", "")
                        parts.append((parent_name, f"../{triad}_{parent_name}.html"))
    
    return parts

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
    
    # Add current page name if it's a child page
    if not page_info['is_main_page'] and page_info['section']:
        filename = page_info['filename']
        # Extract page name from filename
        page_name = filename.replace(f"{page_info['triad']}_", "").replace(".html", "").replace("_", " ")
        # Only add if not already in breadcrumb
        if page_name not in ' '.join([p[0] for p in breadcrumb_parts]):
            breadcrumb_links.append(f'-&gt;<a href="{filename}" style="text-decoration: none; color: inherit;">{page_name}</a>')
    
    new_breadcrumb = f'<span class="logo-suffix">{"".join(breadcrumb_links)}</span>'
    
    # Replace breadcrumb
    content = content.replace(breadcrumb_match.group(1), new_breadcrumb)
    return content, True

def main():
    base_dir = Path('.').resolve()
    
    # Get all HTML files except index.html
    html_files = [f for f in base_dir.rglob('*.html') 
                  if 'site_agent' not in str(f) and f.name != 'index.html']
    
    print(f"Checking and fixing {len(html_files)} pages...")
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
            import traceback
            traceback.print_exc()
    
    print("=" * 70)
    print(f"\n✓ Fixed {fixed_count} pages")
    if issues:
        print(f"✗ {len(issues)} errors")
        for file, error in issues[:5]:
            print(f"  - {file}: {error}")
    
    print("\nDone!")

if __name__ == '__main__':
    main()



