#!/usr/bin/env python3
"""
Interactive page-by-page content updater.
Allows you to replace content on each page, updating all paragraphs in all sheets/columns.
"""
import re
import sys
from pathlib import Path
from html import unescape

BASE_DIR = Path(__file__).parent.parent

def get_all_html_pages():
    """Get all HTML files excluding site_agent and .git directories"""
    html_files = []
    for html_file in BASE_DIR.rglob("*.html"):
        rel_path = html_file.relative_to(BASE_DIR)
        if 'site_agent' not in str(rel_path) and '.git' not in str(rel_path) and 'xives' not in str(rel_path):
            html_files.append(html_file)
    return sorted(html_files)

def extract_current_content(file_path):
    """Extract all current paragraph content from a page"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all content-text divs
    content_text_pattern = r'<div[^>]*class=["\'][^"\']*content-text[^"\']*["\'][^>]*>(.*?)</div>'
    matches = re.findall(content_text_pattern, content, re.DOTALL | re.IGNORECASE)
    
    all_paragraphs = []
    for match in matches:
        # Extract all paragraphs
        paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', match, re.DOTALL | re.IGNORECASE)
        for para in paragraphs:
            # Clean HTML tags
            para_text = re.sub(r'<[^>]+>', '', para)
            para_text = unescape(para_text)
            para_text = re.sub(r'\s+', ' ', para_text).strip()
            if para_text:
                all_paragraphs.append(para_text)
    
    return all_paragraphs, content

def replace_content_in_page(file_path, new_content_text):
    """Replace all paragraph content in a page with new content"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find content-text div
    content_text_pattern = r'(<div[^>]*class=["\'][^"\']*content-text[^"\']*["\'][^>]*>)(.*?)(</div>)'
    match = re.search(content_text_pattern, content, re.DOTALL | re.IGNORECASE)
    
    if not match:
        print(f"  ⚠️  No content-text div found in {file_path.name}")
        return False
    
    div_start = match.group(1)
    div_end = match.group(3)
    
    # Split new content into paragraphs (by double newlines or single newlines)
    if '\n\n' in new_content_text:
        new_paragraphs = [p.strip() for p in new_content_text.split('\n\n') if p.strip()]
    else:
        new_paragraphs = [p.strip() for p in new_content_text.split('\n') if p.strip()]
    
    # Create new paragraph HTML
    new_paragraphs_html = '\n                        '.join([f'<p>{p}</p>' for p in new_paragraphs])
    
    # Replace content
    new_content_text_block = div_start + '\n                        ' + new_paragraphs_html + '\n                    ' + div_end
    new_content = content[:match.start()] + new_content_text_block + content[match.end():]
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def show_current_content(paragraphs):
    """Display current content in a readable format"""
    print("\n" + "="*70)
    print("CURRENT PAGE CONTENT:")
    print("="*70)
    if not paragraphs:
        print("  (No paragraphs found)")
    else:
        for i, para in enumerate(paragraphs, 1):
            preview = para[:150] + "..." if len(para) > 150 else para
            print(f"\n  Paragraph {i}:")
            print(f"  {preview}")
    print("="*70)

def main():
    html_files = get_all_html_pages()
    total = len(html_files)
    
    print("="*70)
    print("INTERACTIVE PAGE CONTENT UPDATER")
    print("="*70)
    print(f"\nTotal pages: {total}")
    print("\nThis script will go through each page one by one.")
    print("For each page, you can provide new content to replace all paragraphs.")
    print("\nCommands:")
    print("  - Type new content (can be multiple paragraphs, separated by blank lines)")
    print("  - Type 'skip' to skip this page")
    print("  - Type 'quit' to exit")
    print("  - Type 'prev' to go back to previous page")
    print("="*70)
    
    current_index = 0
    last_index = -1
    
    while current_index < total:
        html_file = html_files[current_index]
        rel_path = html_file.relative_to(BASE_DIR)
        
        print(f"\n\n{'='*70}")
        print(f"PAGE {current_index + 1} of {total}")
        print(f"File: {rel_path}")
        print(f"{'='*70}")
        
        # Extract current content
        paragraphs, full_content = extract_current_content(html_file)
        show_current_content(paragraphs)
        
        # Get H1 for context
        h1_match = re.search(r'<h1>(.*?)</h1>', full_content, re.DOTALL)
        h1 = h1_match.group(1).strip() if h1_match else "No heading"
        print(f"\nPage Heading: {h1}")
        
        # Get user input
        print("\n" + "-"*70)
        print("Enter new content for this page:")
        print("  (Type your content - press Enter for new paragraph, blank line to finish)")
        print("  (Type 'skip' to skip, 'quit' to exit, 'prev' to go back)")
        print("-"*70)
        
        lines = []
        empty_line_count = 0
        command_entered = False
        
        while True:
            try:
                line = input()
                line_lower = line.strip().lower()
                
                if line_lower == 'quit':
                    print("\nExiting...")
                    sys.exit(0)
                elif line_lower == 'skip':
                    print(f"\n⏭️  Skipping {rel_path.name}")
                    command_entered = True
                    # Will ask for confirmation after break
                    break
                elif line_lower == 'prev':
                    if current_index > 0:
                        current_index -= 1
                        print(f"\n⏮️  Going back to previous page...")
                        command_entered = True
                        break
                    else:
                        print("  ⚠️  Already at first page")
                        continue
                elif not line.strip():
                    # Empty line - if we have content, finish; otherwise continue
                    if lines:
                        empty_line_count += 1
                        if empty_line_count >= 1:  # One blank line finishes input
                            break
                    # If no content yet, just continue
                else:
                    lines.append(line)
                    empty_line_count = 0  # Reset empty line count when content is entered
            except EOFError:
                # User pressed Ctrl+D
                if lines:
                    break
                else:
                    print("\nExiting...")
                    sys.exit(0)
            except KeyboardInterrupt:
                print("\n\nExiting...")
                sys.exit(0)
        
        if command_entered:
            # Handle skip command - ask for confirmation before next page
            if line.strip().lower() == 'skip':
                if current_index < total - 1:
                    next_file = html_files[current_index + 1]
                    next_rel_path = next_file.relative_to(BASE_DIR)
                    print(f"\nNext page: {next_rel_path}")
                    next_action = input("\nContinue to next page? (Enter/quit): ").strip().lower()
                    if next_action == 'quit':
                        print("\nExiting...")
                        sys.exit(0)
                current_index += 1
            continue
        
        if not lines:
            print("  ⚠️  No content provided, skipping...")
            # Still ask for confirmation before next page
            if current_index < total - 1:
                next_file = html_files[current_index + 1]
                next_rel_path = next_file.relative_to(BASE_DIR)
                print(f"\nNext page: {next_rel_path}")
                next_action = input("\nContinue to next page? (Enter/quit): ").strip().lower()
                if next_action == 'quit':
                    print("\nExiting...")
                    sys.exit(0)
            current_index += 1
            continue
        
        # Join lines into content (preserve paragraph structure)
        # Group consecutive non-empty lines into paragraphs
        new_content = '\n\n'.join([line.strip() for line in lines if line.strip()])
        
        # Confirm
        print(f"\n📝 New content preview (first 200 chars):")
        print(f"   {new_content[:200]}...")
        print(f"\n⚠️  This will replace ALL paragraphs in {rel_path.name}")
        confirm = input("   Continue? (y/n): ").strip().lower()
        
        if confirm != 'y':
            print("   Cancelled. Skipping...")
            # Ask for confirmation before next page
            if current_index < total - 1:
                next_file = html_files[current_index + 1]
                next_rel_path = next_file.relative_to(BASE_DIR)
                print(f"\nNext page: {next_rel_path}")
                next_action = input("\nContinue to next page? (Enter/quit): ").strip().lower()
                if next_action == 'quit':
                    print("\nExiting...")
                    sys.exit(0)
            current_index += 1
            continue
        
        # Replace content
        if replace_content_in_page(html_file, new_content):
            new_para_count = len([p for p in new_content.split('\n\n') if p.strip()])
            print(f"\n  ✅ Updated {rel_path.name}")
            print(f"  ✅ Replaced {len(paragraphs)} old paragraphs with {new_para_count} new paragraphs")
            print(f"\n  📄 File saved: {html_file}")
        else:
            print(f"\n  ❌ Failed to update {rel_path.name}")
        
        # Ask for confirmation before moving to next page
        print("\n" + "="*70)
        print(f"✅ PAGE {current_index + 1} COMPLETED")
        print("="*70)
        
        if current_index < total - 1:
            print(f"\nNext page: {html_files[current_index + 1].relative_to(BASE_DIR).name}")
            print("\nOptions:")
            print("  - Press Enter to continue to next page")
            print("  - Type 'quit' to exit")
            print("  - Type 'prev' to go back and redo this page")
            
            next_action = input("\nContinue to next page? (Enter/quit/prev): ").strip().lower()
            
            if next_action == 'quit':
                print("\n" + "="*70)
                print("EXITING - Your changes have been saved")
                print("="*70)
                print(f"\nCompleted: {current_index + 1} of {total} pages")
                print(f"Remaining: {total - current_index - 1} pages")
                sys.exit(0)
            elif next_action == 'prev':
                # Stay on current page (don't increment)
                print(f"\n⏮️  Staying on current page. You can update it again.")
                continue
            else:
                # Continue to next page
                current_index += 1
        else:
            # Last page completed
            print("\n" + "="*70)
            print("🎉 ALL PAGES COMPLETED!")
            print("="*70)
            current_index += 1
    
    print("\n" + "="*70)
    print("✅ ALL PAGES PROCESSED!")
    print("="*70)
    print("\nNext steps:")
    print("  1. Review your changes")
    print("  2. Run: python3 site_agent/use_separate_descriptions.py")
    print("     (This updates pages.html with new content)")

if __name__ == '__main__':
    main()

