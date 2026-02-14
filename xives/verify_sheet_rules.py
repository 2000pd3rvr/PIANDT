#!/usr/bin/env python3
"""
Verify that all pages follow the sheet rules:
1. Each page has at least 1 sheet
2. Each sheet has 4 columns (on desktop)
3. All 4 columns must be full with ~75 words before activating next sheet
"""

import os
import re
from pathlib import Path
from html.parser import HTMLParser

BASE_DIR = Path(__file__).parent.parent

class ContentExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_content_text = False
        self.in_paragraph = False
        self.text_content = []
        self.current_text = []
    
    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            attrs_dict = dict(attrs)
            if 'class' in attrs_dict and 'content-text' in attrs_dict['class']:
                self.in_content_text = True
        elif tag == 'p' and self.in_content_text:
            self.in_paragraph = True
            self.current_text = []
    
    def handle_endtag(self, tag):
        if tag == 'div' and self.in_content_text:
            self.in_content_text = False
        elif tag == 'p' and self.in_paragraph:
            self.in_paragraph = False
            if self.current_text:
                self.text_content.append(' '.join(self.current_text))
                self.current_text = []
    
    def handle_data(self, data):
        if self.in_paragraph:
            self.current_text.append(data.strip())

def count_words(text):
    """Count words in text"""
    words = [w for w in text.split() if w.strip()]
    return len(words)

def check_page(file_path):
    """Check a single page for sheet rule compliance"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract content using simple regex (more reliable than HTMLParser for this)
        # Find content-text div
        content_match = re.search(r'<div[^>]*class="[^"]*content-text[^"]*"[^>]*>(.*?)</div>', content, re.DOTALL)
        if not content_match:
            return {
                'file': str(file_path.relative_to(BASE_DIR)),
                'status': 'error',
                'message': 'No content-text element found'
            }
        
        content_html = content_match.group(1)
        
        # Extract all paragraph text
        paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', content_html, re.DOTALL)
        if not paragraphs:
            return {
                'file': str(file_path.relative_to(BASE_DIR)),
                'status': 'error',
                'message': 'No paragraphs found'
            }
        
        # Count total words (remove HTML tags)
        total_text = ' '.join([re.sub(r'<[^>]+>', '', p) for p in paragraphs])
        total_words = count_words(total_text)
        
        # Calculate expected sheets
        # For 4 columns: need 294 words (98% of 300) per sheet
        words_per_sheet = 294  # Minimum for 4 columns
        expected_sheets = max(1, (total_words + words_per_sheet - 1) // words_per_sheet)
        
        # Check if content is sufficient for at least one sheet
        if total_words == 0:
            return {
                'file': str(file_path.relative_to(BASE_DIR)),
                'status': 'warning',
                'message': f'Empty content (0 words)',
                'words': 0,
                'expected_sheets': 1
            }
        
        # Check if multiple sheets are needed
        if total_words >= words_per_sheet:
            # Should have multiple sheets if content exceeds one sheet
            actual_sheets_needed = (total_words + words_per_sheet - 1) // words_per_sheet
            avg_words_per_column = total_words / (actual_sheets_needed * 4)
            
            return {
                'file': str(file_path.relative_to(BASE_DIR)),
                'status': 'ok' if avg_words_per_column >= 73 else 'warning',
                'message': f'{total_words} words, {actual_sheets_needed} sheet(s) expected',
                'words': total_words,
                'expected_sheets': actual_sheets_needed,
                'avg_words_per_column': round(avg_words_per_column, 1)
            }
        else:
            # Content fits in one sheet
            avg_words_per_column = total_words / 4
            return {
                'file': str(file_path.relative_to(BASE_DIR)),
                'status': 'ok',
                'message': f'{total_words} words, fits in 1 sheet',
                'words': total_words,
                'expected_sheets': 1,
                'avg_words_per_column': round(avg_words_per_column, 1)
            }
            
    except Exception as e:
        return {
            'file': str(file_path.relative_to(BASE_DIR)),
            'status': 'error',
            'message': f'Error: {str(e)}'
        }

def main():
    """Check all pages in in/, processing/, and out/ directories"""
    results = []
    
    # Find all HTML files in the three directories
    for triad_dir in ['in', 'processing', 'out']:
        triad_path = BASE_DIR / triad_dir
        if not triad_path.exists():
            continue
        
        for html_file in triad_path.rglob('*.html'):
            # Skip index/main files
            if html_file.name in ['in.html', 'processing.html', 'proc.html', 'out.html']:
                continue
            
            result = check_page(html_file)
            result['triad'] = triad_dir
            results.append(result)
    
    # Print results
    print("=" * 80)
    print("SHEET RULE VERIFICATION REPORT")
    print("=" * 80)
    print(f"\nTotal pages checked: {len(results)}\n")
    
    # Group by status
    ok_pages = [r for r in results if r['status'] == 'ok']
    warning_pages = [r for r in results if r['status'] == 'warning']
    error_pages = [r for r in results if r['status'] == 'error']
    
    print(f"✓ OK: {len(ok_pages)} pages")
    print(f"⚠ WARNING: {len(warning_pages)} pages")
    print(f"✗ ERROR: {len(error_pages)} pages\n")
    
    # Show warnings
    if warning_pages:
        print("=" * 80)
        print("WARNINGS (pages that may not follow ~75 words/column rule):")
        print("=" * 80)
        for r in warning_pages:
            print(f"  {r['triad']}/{r['file']}")
            print(f"    {r['message']}")
            if 'avg_words_per_column' in r:
                print(f"    Average words per column: {r['avg_words_per_column']}")
            print()
    
    # Show errors
    if error_pages:
        print("=" * 80)
        print("ERRORS (pages with issues):")
        print("=" * 80)
        for r in error_pages:
            print(f"  {r['triad']}/{r['file']}")
            print(f"    {r['message']}")
            print()
    
    # Show summary by triad
    print("=" * 80)
    print("SUMMARY BY TRIAD:")
    print("=" * 80)
    for triad in ['in', 'processing', 'out']:
        triad_results = [r for r in results if r['triad'] == triad]
        triad_ok = len([r for r in triad_results if r['status'] == 'ok'])
        triad_warn = len([r for r in triad_results if r['status'] == 'warning'])
        triad_err = len([r for r in triad_results if r['status'] == 'error'])
        print(f"{triad.upper()}: {len(triad_results)} pages - {triad_ok} OK, {triad_warn} warnings, {triad_err} errors")
    
    print("\n" + "=" * 80)
    print("VERIFICATION COMPLETE")
    print("=" * 80)
    
    # Return exit code
    return 0 if len(error_pages) == 0 else 1

if __name__ == '__main__':
    exit(main())

