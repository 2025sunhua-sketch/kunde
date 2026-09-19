#!/usr/bin/env python3
"""Batch fix header layout across all HTML files in kunde-website."""
import os
import re
from pathlib import Path

BASE_DIR = Path(r"C:\Users\ADMIN\.jvs\.openclaw\workspace\kunde-website")

# Pattern to match header-main div.container without flex style
OLD_CONTAINER_PATTERN = r'<div class="container">\s*<a href="index\.html" class="logo">'
NEW_CONTAINER = '<div class="container" style="display: flex; align-items: center; justify-content: space-between;">\n <a href="index.html" class="logo">'

# Pattern to remove [Copy] span from copy button
OLD_COPY_SPAN = r'<span class="copy-text">\[Copy\]</span>'
NEW_COPY_SPAN = ''

# Pattern to normalize header-contact inline style (remove excessive properties)
OLD_CONTACT_STYLE = r'style="display: flex; align-items: center; justify-content: flex-end; gap: 12px; white-space: nowrap; font-size: 15px; overflow: visible; min-width: 0; flex: 1; padding-right: 60px;"'
NEW_CONTACT_STYLE = 'style="display: flex; align-items: center; gap: 12px; white-space: nowrap; font-size: 15px;"'

# Pattern to normalize copy button font-size from 16px to 15px
OLD_BTN_FONT = r'font-size: 16px; line-height: 1;'
NEW_BTN_FONT = 'font-size: 15px; line-height: 1;'

fixed_count = 0
skipped_count = 0

for html_file in BASE_DIR.rglob("*.html"):
    try:
        content = html_file.read_text(encoding='utf-8')
        original = content
        
        # Fix container flex layout
        if OLD_CONTAINER_PATTERN in content and 'justify-content: space-between' not in content:
            content = re.sub(OLD_CONTAINER_PATTERN, NEW_CONTAINER, content)
        
        # Remove [Copy] text span
        if '[Copy]' in content:
            content = re.sub(OLD_COPY_SPAN, NEW_COPY_SPAN, content)
        
        # Normalize header-contact style
        if OLD_CONTACT_STYLE in content:
            content = content.replace(OLD_CONTACT_STYLE, NEW_CONTACT_STYLE)
        
        # Normalize copy button font size
        if OLD_BTN_FONT in content and 'copy-email-btn' in content:
            # Only replace in copy button context
            content = content.replace(OLD_BTN_FONT, NEW_BTN_FONT)
        
        if content != original:
            html_file.write_text(content, encoding='utf-8')
            fixed_count += 1
            print(f"Fixed: {html_file.relative_to(BASE_DIR)}")
        else:
            skipped_count += 1
            
    except Exception as e:
        print(f"Error processing {html_file}: {e}")

print(f"\nDone. Fixed: {fixed_count}, Skipped: {skipped_count}")
