#!/usr/bin/env python3
"""
Batch add WhatsApp pre-filled message to all HTML files.
Old: https://wa.me/8613566954989
New: https://wa.me/8613566954989?text=Hi%20Kunde%20Electric%2C%20I%20visited%20your%20website%20and%20I%27d%20like%20to%20get%20a%20catalog%20and%20quote.
"""

import os
import re
from pathlib import Path

# Pre-filled message (URL-encoded)
WA_MESSAGE = "Hi%20Kunde%20Electric%2C%20I%20visited%20your%20website%20and%20I%27d%20like%20to%20get%20a%20catalog%20and%20quote."

# Old pattern (without query string)
OLD_LINK = 'https://wa.me/8613566954989'
NEW_LINK = f'https://wa.me/8613566954989?text={WA_MESSAGE}'

def process_html_files(root_dir):
    """Process all HTML files under root_dir."""
    html_files = []
    for ext in ['*.html', '*.htm']:
        html_files.extend(Path(root_dir).rglob(ext))
    
    modified_count = 0
    skipped_count = 0
    
    for file_path in sorted(html_files):
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Count occurrences before replacement
            old_count = content.count(OLD_LINK)
            
            if old_count == 0:
                skipped_count += 1
                continue
            
            # Replace all occurrences
            new_content = content.replace(OLD_LINK, NEW_LINK)
            
            # Write back
            file_path.write_text(new_content, encoding='utf-8')
            
            modified_count += 1
            print(f"✓ {file_path.relative_to(root_dir)} ({old_count} link(s) updated)")
            
        except Exception as e:
            print(f"✗ {file_path.relative_to(root_dir)}: {e}")
    
    return modified_count, skipped_count

if __name__ == '__main__':
    workspace = Path(__file__).parent
    print(f"Processing HTML files in: {workspace}\n")
    
    modified, skipped = process_html_files(workspace)
    
    print(f"\n{'='*60}")
    print(f"Done! Modified: {modified} files | Skipped: {skipped} files")
    print(f"{'='*60}")
