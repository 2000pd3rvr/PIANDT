#!/usr/bin/env python3
"""
Restructure directories to match menu hierarchy exactly.
For each triad (In, Processing, Out):
- Main file: {triad}.html
- Subdirectories: about_piandt/ and units/
- Inside about_piandt/: parent page + child pages
- Inside units/: parent page + nested subdirectories (e.g., miu/)
"""

import os
import shutil
from pathlib import Path
import re

BASE_DIR = Path(__file__).parent.parent

# Define the correct structure for each triad
TRIAD_STRUCTURES = {
    'in': {
        'main_file': 'in.html',
        'prefix': 'in_',
        'about_dir': 'about_piandt',
        'units_dir': 'units',
        'about_pages': [
            'in_about_piandt.html',  # Parent page first
            'in_mission_vision.html',
            'in_charitable_purposes.html',
            'in_our_approach.html',
            'in_trustees.html',
            'in_governance.html'
        ],
        'units_structure': {
            'main': 'in_units.html',  # Parent page
            'miu': {
                'main': 'in_miu.html',
                'vision': {
                    'main': 'in_miu_vision.html',
                    'products': [
                        'in_miu_vision_products.html',
                        'in_miu_vision_products_hardware.html',
                        'in_miu_vision_products_software.html'
                    ],
                    'services': [
                        'in_miu_vision_services.html',
                        'in_miu_vision_services_consultancy.html',
                        'in_miu_vision_services_education.html',
                        'in_miu_vision_services_rd.html'
                    ]
                }
            }
        }
    },
    'processing': {
        'main_file': 'processing.html',
        'prefix': 'proc_',
        'about_dir': 'about_piandt',
        'units_dir': 'units',
        'about_pages': [
            'proc_about_piandt.html',
            'proc_mission_vision.html',
            'proc_charitable_purposes.html',
            'proc_our_approach.html',
            'proc_trustees.html',
            'proc_governance.html'
        ],
        'units_structure': {
            'main': 'proc_units.html',
            'miu': {
                'main': 'proc_miu.html',
                'vision': {
                    'main': 'proc_miu_vision.html',
                    'products': [
                        'proc_miu_vision_products.html',
                        'proc_miu_vision_products_hardware.html',
                        'proc_miu_vision_products_software.html'
                    ],
                    'services': [
                        'proc_miu_vision_services.html',
                        'proc_miu_vision_services_consultancy.html',
                        'proc_miu_vision_services_education.html',
                        'proc_miu_vision_services_rd.html'
                    ]
                }
            }
        }
    },
    'out': {
        'main_file': 'out.html',
        'prefix': 'out_',
        'about_dir': 'about_piandt',
        'units_dir': 'units',
        'about_pages': [
            'out_about_piandt.html',
            'out_mission_vision.html',
            'out_charitable_purposes.html',
            'out_our_approach.html',
            'out_trustees.html',
            'out_governance.html'
        ],
        'units_structure': {
            'main': 'out_units.html',
            'miu': {
                'main': 'out_miu.html',
                'vision': {
                    'main': 'out_miu_vision.html',
                    'products': [
                        'out_miu_vision_products.html',
                        'out_miu_vision_products_hardware.html',
                        'out_miu_vision_products_software.html'
                    ],
                    'services': [
                        'out_miu_vision_services.html',
                        'out_miu_vision_services_consultancy.html',
                        'out_miu_vision_services_education.html',
                        'out_miu_vision_services_rd.html'
                    ]
                }
            }
        }
    }
}

def find_file_in_directory(directory, filename, alternate_names=None):
    """Recursively find a file in a directory, checking alternate names too"""
    search_names = [filename]
    if alternate_names:
        search_names.extend(alternate_names)
    
    for root, dirs, files in os.walk(directory):
        for search_name in search_names:
            if search_name in files:
                return Path(root) / search_name
    return None

def calculate_relative_path(from_file, to_file):
    """Calculate relative path from one file to another"""
    from_path = Path(from_file).parent
    to_path = Path(to_file).parent if to_file != Path(to_file) else Path(to_file)
    
    try:
        rel_path = os.path.relpath(to_path, from_path)
        if rel_path == '.':
            return './'
        return rel_path.replace('\\', '/') + '/'
    except:
        # Fallback: count depth difference
        from_depth = len(str(from_path).split('/'))
        to_depth = len(str(to_path).split('/'))
        if to_depth < from_depth:
            return '../' * (from_depth - to_depth)
        return './'

def update_file_paths_in_html(file_path, old_path, new_path, triad):
    """Update all relative paths in an HTML file after moving"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Calculate new depth (how many levels from BASE_DIR)
        new_depth = len(str(new_path).replace(str(BASE_DIR), '').strip('/').split('/'))
        
        # Update CSS/JS paths (styles.css, script.js, multi-sheet-pagination.js, etc.)
        # These should point to BASE_DIR, so calculate path from new location
        css_js_depth = new_depth
        css_js_path = '../' * css_js_depth
        
        # Update styles.css
        content = re.sub(
            r'(href|src)=["\']([^"\']*styles\.css[^"\']*)["\']',
            lambda m: f'{m.group(1)}="{css_js_path}styles.css"',
            content
        )
        
        # Update script.js
        content = re.sub(
            r'(href|src)=["\']([^"\']*script\.js[^"\']*)["\']',
            lambda m: f'{m.group(1)}="{css_js_path}script.js"',
            content
        )
        
        # Update multi-sheet-pagination.js
        content = re.sub(
            r'(href|src)=["\']([^"\']*multi-sheet-pagination\.js[^"\']*)["\']',
            lambda m: f'{m.group(1)}="{css_js_path}multi-sheet-pagination.js"',
            content
        )
        
        # Update images/agent.png
        content = re.sub(
            r'(href|src)=["\']([^"\']*images/agent\.png[^"\']*)["\']',
            lambda m: f'{m.group(1)}="{css_js_path}images/agent.png"',
            content
        )
        
        # Update index.html links
        content = re.sub(
            r'href=["\']([^"\']*index\.html)["\']',
            lambda m: f'href="{css_js_path}index.html"',
            content
        )
        
        # Update main triad page links (in.html, processing.html, out.html)
        triad_file = f'{triad}.html' if triad != 'processing' else 'processing.html'
        content = re.sub(
            r'href=["\']([^"\']*{})["\']'.format(re.escape(triad_file)),
            lambda m: f'href="{css_js_path}{triad_file}"',
            content
        )
        
        # Update menu links to match new structure
        prefix = TRIAD_STRUCTURES[triad]['prefix']
        
        # Fix about_piandt links - ensure they point to about_piandt/ directory
        about_pattern = r'href=["\']([^"\']*)(?:piandt/|about_piandt/)?({}_about_piandt|{}_mission_vision|{}_charitable_purposes|{}_our_approach|{}_trustees|{}_governance)\.html["\']'.format(prefix, prefix, prefix, prefix, prefix, prefix)
        def fix_about_link(m):
            rel_path = m.group(1) if m.group(1) else ''
            # If already has about_piandt/, keep it, otherwise add it
            if 'about_piandt/' not in rel_path:
                rel_path = rel_path.rstrip('/') + ('about_piandt/' if rel_path else 'about_piandt/')
            return f'href="{rel_path}{m.group(2)}.html"'
        content = re.sub(about_pattern, fix_about_link, content)
        
        # Fix units links - ensure they point to units/ directory structure
        units_pattern = r'href=["\']([^"\']*)(?:units/)?(?:miu/)?(?:vision/)?(?:products/|services/)?({}_units|{}_miu|{}_miu_vision|{}_miu_vision_products|{}_miu_vision_services)\.html["\']'.format(prefix, prefix, prefix, prefix, prefix)
        def fix_units_link(m):
            rel_path = m.group(1) if m.group(1) else ''
            filename = m.group(2)
            
            # Determine correct path based on filename
            if filename.endswith('_units'):
                return f'href="{rel_path.rstrip("/")}/units/{filename}.html"'
            elif filename.endswith('_miu') and not filename.endswith('_miu_vision'):
                return f'href="{rel_path.rstrip("/")}/units/miu/{filename}.html"'
            elif filename.endswith('_miu_vision') and not ('products' in filename or 'services' in filename):
                return f'href="{rel_path.rstrip("/")}/units/miu/vision/{filename}.html"'
            elif 'products' in filename:
                return f'href="{rel_path.rstrip("/")}/units/miu/vision/products/{filename}.html"'
            elif 'services' in filename:
                return f'href="{rel_path.rstrip("/")}/units/miu/vision/services/{filename}.html"'
            return f'href="{rel_path}{filename}.html"'
        content = re.sub(units_pattern, fix_units_link, content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"  ⚠️  Error updating paths in {file_path}: {e}")
        import traceback
        traceback.print_exc()
        return False

def restructure_triad(triad_name, structure):
    """Restructure a single triad directory"""
    print(f"\n{'='*60}")
    print(f"Restructuring {triad_name.upper()} directory")
    print(f"{'='*60}")
    
    triad_dir = BASE_DIR / triad_name
    if not triad_dir.exists():
        print(f"  ⚠️  Directory {triad_dir} does not exist")
        return
    
    prefix = structure['prefix']
    
    # Step 1: Create correct directory structure
    about_dir = triad_dir / structure['about_dir']
    units_dir = triad_dir / structure['units_dir']
    
    about_dir.mkdir(exist_ok=True)
    units_dir.mkdir(exist_ok=True)
    
    # Step 2: Move about_piandt files
    print(f"\n📁 Moving about_piandt files...")
    for page in structure['about_pages']:
        # Try to find the file
        source_file = find_file_in_directory(triad_dir, page)
        if source_file:
            target_file = about_dir / page
            if source_file != target_file:
                print(f"  Moving {source_file.relative_to(BASE_DIR)} -> {target_file.relative_to(BASE_DIR)}")
                shutil.move(str(source_file), str(target_file))
                update_file_paths_in_html(target_file, source_file.parent, target_file.parent, triad_name)
            else:
                print(f"  ✓ {page} already in correct location")
        else:
            print(f"  ⚠️  File {page} not found")
    
    # Step 3: Move units files
    print(f"\n📁 Moving units files...")
    
    # Move main units page
    units_main = structure['units_structure']['main']
    source_file = find_file_in_directory(triad_dir, units_main)
    if source_file:
        target_file = units_dir / units_main
        if source_file != target_file:
            print(f"  Moving {source_file.relative_to(BASE_DIR)} -> {target_file.relative_to(BASE_DIR)}")
            shutil.move(str(source_file), str(target_file))
            update_file_paths_in_html(target_file, source_file.parent, target_file.parent, triad_name)
        else:
            print(f"  ✓ {units_main} already in correct location")
    
    # Move MIU files
    miu_structure = structure['units_structure']['miu']
    miu_dir = units_dir / 'miu'
    miu_dir.mkdir(exist_ok=True)
    
    # Move MIU main page - check for alternate naming (processing_miu vs proc_miu)
    miu_main = miu_structure['main']
    alternate_miu = None
    if triad_name == 'processing':
        # For processing, also check for processing_miu.html
        alternate_miu = 'processing_miu.html'
    source_file = find_file_in_directory(triad_dir, miu_main, [alternate_miu] if alternate_miu else None)
    if source_file:
        target_file = miu_dir / miu_main
        if source_file != target_file:
            print(f"  Moving {source_file.relative_to(BASE_DIR)} -> {target_file.relative_to(BASE_DIR)}")
            # If filename is different, copy and update, then remove old
            if source_file.name != miu_main:
                shutil.copy2(str(source_file), str(target_file))
                update_file_paths_in_html(target_file, source_file.parent, target_file.parent, triad_name)
                os.remove(str(source_file))
            else:
                shutil.move(str(source_file), str(target_file))
                update_file_paths_in_html(target_file, source_file.parent, target_file.parent, triad_name)
        else:
            print(f"  ✓ {miu_main} already in correct location")
    
    # Move vision files
    vision_structure = miu_structure['vision']
    vision_dir = miu_dir / 'vision'
    vision_dir.mkdir(exist_ok=True)
    
    # Move vision main page - check for alternate naming
    vision_main = vision_structure['main']
    alternate_vision = None
    if triad_name == 'processing':
        alternate_vision = 'processing_miu_vision.html'
    source_file = find_file_in_directory(triad_dir, vision_main, [alternate_vision] if alternate_vision else None)
    if source_file:
        target_file = vision_dir / vision_main
        if source_file != target_file:
            print(f"  Moving {source_file.relative_to(BASE_DIR)} -> {target_file.relative_to(BASE_DIR)}")
            if source_file.name != vision_main:
                shutil.copy2(str(source_file), str(target_file))
                update_file_paths_in_html(target_file, source_file.parent, target_file.parent, triad_name)
                os.remove(str(source_file))
            else:
                shutil.move(str(source_file), str(target_file))
                update_file_paths_in_html(target_file, source_file.parent, target_file.parent, triad_name)
        else:
            print(f"  ✓ {vision_main} already in correct location")
    
    # Move products files
    products_dir = vision_dir / 'products'
    products_dir.mkdir(exist_ok=True)
    for product_file in vision_structure['products']:
        # Check for alternate naming (processing_ vs proc_)
        alternate_product = None
        if triad_name == 'processing' and product_file.startswith('proc_'):
            alternate_product = product_file.replace('proc_', 'processing_')
        source_file = find_file_in_directory(triad_dir, product_file, [alternate_product] if alternate_product else None)
        if source_file:
            target_file = products_dir / product_file
            if source_file != target_file:
                print(f"  Moving {source_file.relative_to(BASE_DIR)} -> {target_file.relative_to(BASE_DIR)}")
                if source_file.name != product_file:
                    shutil.copy2(str(source_file), str(target_file))
                    update_file_paths_in_html(target_file, source_file.parent, target_file.parent, triad_name)
                    os.remove(str(source_file))
                else:
                    shutil.move(str(source_file), str(target_file))
                    update_file_paths_in_html(target_file, source_file.parent, target_file.parent, triad_name)
            else:
                print(f"  ✓ {product_file} already in correct location")
    
    # Move services files
    services_dir = vision_dir / 'services'
    services_dir.mkdir(exist_ok=True)
    for service_file in vision_structure['services']:
        # Check for alternate naming (processing_ vs proc_)
        alternate_service = None
        if triad_name == 'processing' and service_file.startswith('proc_'):
            alternate_service = service_file.replace('proc_', 'processing_')
        source_file = find_file_in_directory(triad_dir, service_file, [alternate_service] if alternate_service else None)
        if source_file:
            target_file = services_dir / service_file
            if source_file != target_file:
                print(f"  Moving {source_file.relative_to(BASE_DIR)} -> {target_file.relative_to(BASE_DIR)}")
                if source_file.name != service_file:
                    shutil.copy2(str(source_file), str(target_file))
                    update_file_paths_in_html(target_file, source_file.parent, target_file.parent, triad_name)
                    os.remove(str(source_file))
                else:
                    shutil.move(str(source_file), str(target_file))
                    update_file_paths_in_html(target_file, source_file.parent, target_file.parent, triad_name)
            else:
                print(f"  ✓ {service_file} already in correct location")
    
    # Step 4: Move any remaining files from wrong miu/ directory
    print(f"\n📁 Moving files from incorrect miu/ directory...")
    wrong_miu_dir = triad_dir / 'miu'
    if wrong_miu_dir.exists() and wrong_miu_dir.is_dir():
        # Try to move any remaining files that match our structure
        for root, dirs, files in os.walk(wrong_miu_dir):
            for file in files:
                if file.endswith('.html'):
                    # Check if this file should be in our structure
                    for product_file in vision_structure['products']:
                        if file == product_file or (triad_name == 'processing' and file == product_file.replace('proc_', 'processing_')):
                            target = products_dir / product_file
                            if not target.exists():
                                source = Path(root) / file
                                print(f"  Moving {source.relative_to(BASE_DIR)} -> {target.relative_to(BASE_DIR)}")
                                shutil.move(str(source), str(target))
                                update_file_paths_in_html(target, source.parent, target.parent, triad_name)
                    
                    for service_file in vision_structure['services']:
                        if file == service_file or (triad_name == 'processing' and file == service_file.replace('proc_', 'processing_')):
                            target = services_dir / service_file
                            if not target.exists():
                                source = Path(root) / file
                                print(f"  Moving {source.relative_to(BASE_DIR)} -> {target.relative_to(BASE_DIR)}")
                                shutil.move(str(source), str(target))
                                update_file_paths_in_html(target, source.parent, target.parent, triad_name)
    
    # Step 5: Remove incorrect directories (only if empty or after moving files)
    print(f"\n🗑️  Removing incorrect directories...")
    
    # Remove miu/ at wrong level (if empty or only has non-HTML files)
    if wrong_miu_dir.exists() and wrong_miu_dir.is_dir():
        # Check if directory is empty or only has non-essential files
        has_html = any(f.suffix == '.html' for f in wrong_miu_dir.rglob('*.html'))
        if not has_html:
            print(f"  Removing {wrong_miu_dir.relative_to(BASE_DIR)}")
            shutil.rmtree(str(wrong_miu_dir))
        else:
            print(f"  ⚠️  {wrong_miu_dir.relative_to(BASE_DIR)} still contains HTML files, skipping removal")
    
    # Remove piandt/ directory (should be about_piandt/)
    wrong_piandt_dir = triad_dir / 'piandt'
    if wrong_piandt_dir.exists() and wrong_piandt_dir.is_dir():
        print(f"  Removing {wrong_piandt_dir.relative_to(BASE_DIR)}")
        shutil.rmtree(str(wrong_piandt_dir))
    
    print(f"\n✅ {triad_name.upper()} restructuring complete!")

def main():
    """Main function to restructure all triads"""
    print("="*60)
    print("DIRECTORY RESTRUCTURING TO MATCH MENU HIERARCHY")
    print("="*60)
    print("\nThis will:")
    print("1. Move files to match menu hierarchy exactly")
    print("2. Update all links and paths in HTML files")
    print("3. Remove duplicate/incorrect directories")
    print("4. Preserve theme, chat agent, and content")
    print("\n" + "="*60)
    
    # Restructure each triad
    for triad_name, structure in TRIAD_STRUCTURES.items():
        restructure_triad(triad_name, structure)
    
    print("\n" + "="*60)
    print("✅ ALL RESTRUCTURING COMPLETE!")
    print("="*60)
    print("\nPlease test the pages to ensure:")
    print("- All links work correctly")
    print("- Theme is preserved")
    print("- Chat agent works")
    print("- Navigation menus are correct")

if __name__ == '__main__':
    main()

