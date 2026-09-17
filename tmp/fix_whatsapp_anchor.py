#!/usr/bin/env python3
"""Fix batch_optimize.py: inject WhatsApp <a> tag where CSS exists but anchor is missing."""

import os
import glob

SITE_ROOT = r"C:\Users\ADMIN\.jvs\.openclaw\workspace\kunde-website"

WHATSAPP_ANCHOR = '''<!-- WhatsApp Floating Button -->
<a href="https://wa.me/8613566954989?text=Hi%20Kunde%20Electric%2C%20I%20am%20interested%20in%20your%20power%20fittings%20and%20would%20like%20to%20get%20more%20information." 
   class="whatsapp-float" target="_blank" rel="noopener noreferrer" aria-label="Chat on WhatsApp">
  <i class="fab fa-whatsapp"></i>
</a>
'''

def fix_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return False

    # Only fix files that have the CSS but not the anchor
    if '.whatsapp-float' in content and 'whatsapp-float"' not in content and '</body>' in content:
        content = content.replace('</body>', WHATSAPP_ANCHOR + '\n</body>')
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception:
            return False
    return False

html_files = glob.glob(os.path.join(SITE_ROOT, '**', '*.html'), recursive=True)
fixed = 0
for fp in html_files:
    if fix_file(fp):
        fixed += 1

print(f"Fixed {fixed} files (added missing WhatsApp anchor tag).")
