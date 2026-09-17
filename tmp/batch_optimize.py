#!/usr/bin/env python3
"""Batch optimize all HTML files: add WhatsApp floating button + fix contact links."""

import os
import re
import glob

SITE_ROOT = r"C:\Users\ADMIN\.jvs\.openclaw\workspace\kunde-website"

# WhatsApp floating button HTML (injected before </body>)
WHATSAPP_BUTTON = '''
<!-- WhatsApp Floating Button -->
<a href="https://wa.me/8613566954989?text=Hi%20Kunde%20Electric%2C%20I%20am%20interested%20in%20your%20power%20fittings%20and%20would%20like%20to%20get%20more%20information." 
   class="whatsapp-float" target="_blank" rel="noopener noreferrer" aria-label="Chat on WhatsApp">
  <i class="fab fa-whatsapp"></i>
</a>
<style>
.whatsapp-float {
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 56px;
  height: 56px;
  background-color: #25D366;
  color: #fff;
  border-radius: 50%;
  text-align: center;
  font-size: 28px;
  line-height: 56px;
  box-shadow: 0 4px 12px rgba(37,211,102,0.4);
  z-index: 9999;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}
.whatsapp-float:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 20px rgba(37,211,102,0.6);
}
@media (max-width: 768px) {
  .whatsapp-float {
    bottom: 16px;
    right: 16px;
    width: 48px;
    height: 48px;
    font-size: 24px;
    line-height: 48px;
  }
}
</style>
'''

def process_html(filepath):
    """Process a single HTML file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  SKIP read: {filepath} ({e})")
        return False

    original = content

    # 1. Add WhatsApp button before </body>
    if '</body>' in content and 'whatsapp-float' not in content:
        content = content.replace('</body>', WHATSAPP_BUTTON + '\n</body>')

    # 2. Fix email links: wrap bare sales@kdelec.com in <a href="mailto:...">
    # Match patterns like: >sales@kdelec.com< or just sales@kdelec.com not already inside <a>
    def fix_email(match):
        full = match.group(0)
        # Skip if already inside an <a> tag
        before = content[:match.start()]
        after_open_a = before.rfind('<a ')
        after_close_a = before.rfind('</a>')
        if after_open_a > after_close_a:
            return full  # Already inside a link
        return f'<a href="mailto:sales@kdelec.com">{full}</a>'

    # Only replace emails NOT already wrapped in <a href="mailto:...">
    content = re.sub(
        r'(?<!href="mailto:)sales@kdelec\.com(?!")',
        lambda m: f'<a href="mailto:sales@kdelec.com">{m.group(0)}</a>' if '<a ' not in content[max(0,m.start()-20):m.start()+len(m.group(0))+20] else m.group(0),
        content
    )

    # 3. Fix phone/WhatsApp number links
    # Pattern: +86-13566954989 or +8613566954989 not already in <a href="tel:...">
    def fix_phone(match):
        full = match.group(0)
        before = content[:match.start()]
        after_open_a = before.rfind('<a ')
        after_close_a = before.rfind('</a>')
        if after_open_a > after_close_a:
            return full
        clean_num = full.replace('-', '').replace(' ', '')
        return f'<a href="tel:{clean_num}">{full}</a>'

    content = re.sub(
        r'\+86[-\s]?13566954989',
        lambda m: f'<a href="tel:+8613566954989">{m.group(0)}</a>' if '<a ' not in content[max(0,m.start()-20):m.start()+len(m.group(0))+20] else m.group(0),
        content
    )

    if content != original:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"  FAIL write: {filepath} ({e})")
            return False
    return False


def main():
    html_files = glob.glob(os.path.join(SITE_ROOT, '**', '*.html'), recursive=True)
    total = len(html_files)
    modified = 0
    skipped = 0

    print(f"Processing {total} HTML files...")
    for i, filepath in enumerate(html_files, 1):
        result = process_html(filepath)
        if result:
            modified += 1
        else:
            skipped += 1
        if i % 50 == 0:
            print(f"  Progress: {i}/{total} ({modified} modified, {skipped} unchanged)")

    print(f"\nDone! {modified} files modified, {skipped} files unchanged (already optimized or no changes needed).")


if __name__ == '__main__':
    main()
