#!/usr/bin/env python3
"""
Restore corrupted HTML files by reading from a working template and fixing only nav-menu and breadcrumb
"""

from pathlib import Path
import re
import shutil

def restore_file(corrupted_file, template_file, page_info, base_dir):
    """Restore a corrupted file from template"""
    try:
        # Read template
        with open(template_file, 'r', encoding='utf-8') as f:
            template = f.read()
        
        # Read corrupted file to see what nav-menu it has
        with open(corrupted_file, 'r', encoding='utf-8') as f:
            corrupted_nav = f.read()
        
        # Extract nav-menu from corrupted file if it exists
        nav_match = re.search(r'<ul class="nav-menu">.*?</ul>', corrupted_nav, re.DOTALL)
        if nav_match:
            new_nav_menu = nav_match.group(0)
        else:
            # Build nav-menu based on page_info
            new_nav_menu = build_correct_nav_menu(page_info)
        
        # Replace nav-menu in template
        template_nav_match = re.search(r'<ul class="nav-menu">.*?</ul>', template, re.DOTALL)
        if template_nav_match:
            template = template.replace(template_nav_match.group(0), new_nav_menu)
        
        # Fix breadcrumb
        breadcrumb = build_correct_breadcrumb(page_info)
        breadcrumb_match = re.search(r'<span class="logo-suffix">.*?</span>', template, re.DOTALL)
        if breadcrumb_match:
            template = template.replace(breadcrumb_match.group(0), breadcrumb)
        else:
            # Insert breadcrumb before nav-menu
            template = template.replace('<ul class="nav-menu">', breadcrumb + '\n            <ul class="nav-menu">', 1)
        
        # Update title and paths in template
        triad = page_info['triad']
        filename = page_info['filename']
        
        # Update title
        title_match = re.search(r'<title>(.*?)</title>', template)
        if title_match:
            # Extract page name from filename
            page_name = filename.replace(f"{triad}_", "").replace(".html", "").replace("_", " ").title()
            if page_info['section'] == 'about_piandt':
                new_title = f"about PIANDT - {triad.title()} - PIANDT"
            elif page_info['section'] == 'units':
                new_title = f"Units - {triad.title()} - PIANDT"
            else:
                new_title = f"{page_name} - {triad.title()} - PIANDT"
            template = template.replace(title_match.group(0), f'<title>{new_title}</title>')
        
        # Update CSS/JS paths based on depth
        depth = page_info['depth']
        if depth > 1:
            path_prefix = '../' * (depth - 1)
            template = re.sub(r'href=["\'](\.\./)*styles\.css', f'href="{path_prefix}styles.css', template)
            template = re.sub(r'src=["\'](\.\./)*', f'src="{path_prefix}', template)
        
        return template
    except Exception as e:
        print(f"Error restoring {corrupted_file}: {e}")
        return None

def build_correct_nav_menu(page_info):
    """Build correct nav-menu HTML"""
    triad = page_info['triad']
    depth = page_info['depth']
    
    if page_info['is_main_page']:
        # Main page
        return f'''            <ul class="nav-menu">
                <li class="dropdown">
                    <a href="{triad}.html" class="nav-link">{"In" if triad == "in" else "Proc" if triad == "processing" else "Out"} <span class="dropdown-arrow">▼</span></a>
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
    elif page_info['section'] == 'about_piandt':
        # about_piandt section
        return f'''            <ul class="nav-menu">
                <li class="dropdown">
                    <a href="{triad}_about_piandt.html" class="nav-link">about PIANDT <span class="dropdown-arrow">▼</span></a>
                    <ul class="dropdown-menu">
                        <li><a href="{triad}_mission_vision.html" class="dropdown-link">our mission and vision</a></li>
                        <li><a href="{triad}_charitable_purposes.html" class="dropdown-link">charitable purposes</a></li>
                        <li><a href="{triad}_our_approach.html" class="dropdown-link">our approach</a></li>
                        <li><a href="{triad}_trustees.html" class="dropdown-link">trustees</a></li>
                        <li><a href="{triad}_governance.html" class="dropdown-link">governance</a></li>
                    </ul>
                </li>
            </ul>'''
    elif page_info['section'] == 'units':
        # Units section - need to determine based on depth
        if depth == 2:
            # Units main page
            return f'''            <ul class="nav-menu">
                <li class="dropdown">
                    <a href="{triad}_units.html" class="nav-link">units <span class="dropdown-arrow">▼</span></a>
                    <ul class="dropdown-menu">
                        <li>
                            <a href="../about_piandt/{triad}_about_piandt.html" class="dropdown-link">about PIANDT <span class="dropdown-arrow">▶</span></a>
                            <ul>
                                <li><a href="../about_piandt/{triad}_mission_vision.html" class="submenu-link">our mission and vision</a></li>
                                <li><a href="../about_piandt/{triad}_charitable_purposes.html" class="submenu-link">charitable purposes</a></li>
                                <li><a href="../about_piandt/{triad}_our_approach.html" class="submenu-link">our approach</a></li>
                                <li><a href="../about_piandt/{triad}_trustees.html" class="submenu-link">trustees</a></li>
                                <li><a href="../about_piandt/{triad}_governance.html" class="submenu-link">governance</a></li>
                            </ul>
                        </li>
                        <li>
                            <a href="miu/{triad}_miu.html" class="dropdown-link">machine intelligence <span class="dropdown-arrow">▶</span></a>
                        </li>
                    </ul>
                </li>
            </ul>'''
        else:
            # Deep unit pages - preserve existing structure but we need to read from a working file
            return None  # Will be handled differently
    return None

def build_correct_breadcrumb(page_info):
    """Build correct breadcrumb"""
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

def main():
    base_dir = Path('.').resolve()
    
    # Find corrupted files (very short)
    corrupted_files = []
    for html_file in base_dir.rglob('*.html'):
        if 'site_agent' in str(html_file) or html_file.name == 'index.html':
            continue
        try:
            with open(html_file, 'r') as f:
                content = f.read()
            if len(content) < 2000:  # Corrupted
                corrupted_files.append(html_file)
        except:
            pass
    
    print(f"Found {len(corrupted_files)} corrupted files to restore")
    
    # Find a working template for each type
    template = base_dir / 'in/about_piandt/in_about_piandt.html'
    if not template.exists() or len(open(template).read()) < 5000:
        print("ERROR: Template file not found or corrupted!")
        return
    
    restored = 0
    for corrupted_file in corrupted_files:
        try:
            # Get page info
            rel_path = corrupted_file.relative_to(base_dir)
            path_parts = str(rel_path).split('/')
            
            triad = None
            section = None
            is_main = False
            
            if 'in/' in str(rel_path):
                triad = 'in'
                if len(path_parts) == 2 and path_parts[-1] == 'in.html':
                    is_main = True
                elif 'about_piandt' in str(rel_path):
                    section = 'about_piandt'
                elif 'units' in str(rel_path):
                    section = 'units'
            elif 'processing/' in str(rel_path):
                triad = 'processing'
                if len(path_parts) == 2 and path_parts[-1] == 'processing.html':
                    is_main = True
                elif 'about_piandt' in str(rel_path):
                    section = 'about_piandt'
                elif 'units' in str(rel_path):
                    section = 'units'
            elif 'out/' in str(rel_path):
                triad = 'out'
                if len(path_parts) == 2 and path_parts[-1] == 'out.html':
                    is_main = True
                elif 'about_piandt' in str(rel_path):
                    section = 'about_piandt'
                elif 'units' in str(rel_path):
                    section = 'units'
            
            page_info = {
                'triad': triad,
                'section': section,
                'is_main_page': is_main,
                'filename': path_parts[-1],
                'path': rel_path,
                'depth': len(path_parts) - 1
            }
            
            # Restore file
            restored_content = restore_file(corrupted_file, template, page_info, base_dir)
            if restored_content:
                with open(corrupted_file, 'w', encoding='utf-8') as f:
                    f.write(restored_content)
                restored += 1
                print(f"✓ Restored: {corrupted_file.relative_to(base_dir)}")
        except Exception as e:
            print(f"✗ Error restoring {corrupted_file}: {e}")
    
    print(f"\n✓ Restored {restored} files")

if __name__ == '__main__':
    main()



