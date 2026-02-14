#!/usr/bin/env python3
"""
Update a single page and automatically regenerate pages.html to keep descriptions in sync.

Usage:
    python3 site_agent/update_page_and_sync.py <page_path>
    
Example:
    python3 site_agent/update_page_and_sync.py in/about_piandt/in_about_piandt.html
"""
import sys
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

def update_pages_html():
    """Run the update_pages_html.py script to regenerate pages.html"""
    script_path = BASE_DIR / 'site_agent' / 'update_pages_html.py'
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✅ Successfully regenerated pages.html")
            print(result.stdout)
            return True
        else:
            print("❌ Error regenerating pages.html:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error running update script: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 site_agent/update_page_and_sync.py <page_path>")
        print("\nExample:")
        print("  python3 site_agent/update_page_and_sync.py in/about_piandt/in_about_piandt.html")
        print("\nAfter you update a page, run this script to regenerate pages.html")
        sys.exit(1)
    
    page_path = Path(sys.argv[1])
    
    if not page_path.exists():
        print(f"❌ Error: Page not found: {page_path}")
        sys.exit(1)
    
    print("="*60)
    print("PAGE UPDATE WORKFLOW")
    print("="*60)
    print(f"\n📄 Page: {page_path}")
    print("\n⚠️  IMPORTANT: Make sure you've saved your changes to the page first!")
    print("\nThis script will regenerate pages.html with updated descriptions")
    print("from all pages, including your changes.\n")
    
    input("Press Enter to continue (or Ctrl+C to cancel)...")
    
    print("\n🔄 Regenerating pages.html...")
    success = update_pages_html()
    
    if success:
        print("\n" + "="*60)
        print("✅ COMPLETE!")
        print("="*60)
        print(f"\n✅ Page {page_path.name} updated")
        print("✅ pages.html regenerated with new descriptions")
        print("\nThe 'Page Description' column in pages.html now reflects")
        print("the updated content from your page.")
    else:
        print("\n❌ Failed to regenerate pages.html")
        sys.exit(1)

if __name__ == '__main__':
    main()

