#!/usr/bin/env python3
"""
Batch optimize all HTML files with precise logic:
1. Inject WhatsApp floating button (CSS + <a> tag) before </body>
2. Linkify bare email/phone ONLY if not already inside <a> tag
"""

import os
import re
import glob

SITE_ROOT = r"C:\Users\ADMIN\.jvs\.openclaw\workspace\kunde-website"

# Complete WhatsApp button block (CSS + anchor as single string)
WHATSAPP_BLOCK = '''<!-- WhatsApp Floating Button -->
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


def is_inside_anchor(content, match_start, match_end):
    """Check if the matched text is already inside an <a> tag."""
    # Look backward for opening <a without closing </a> in between
    before = content[:match_start]
    last_open_a = before.rfind('<a ')
    last_close_a = before.rfind('</a>')
    # If there's an unclosed <a> tag, we're inside a link
    if last_open_a > last_close_a:
        return True
    
    # Also check forward: is this text part of an <a ...>TEXT</a> structure?
    after = content[match_end:]
    next_close_a = after.find('</a>')
    next_open_a = after.find('<a ')
    # If </a> comes before next <a>, we might be inside a link
    if next_close_a >= 0 and (next_open_a < 0 or next_close_a < next_open_a):
        # Check if there's an opening <a> before our match that pairs with this </a>
        # Simple heuristic: look at the text around our match
        context = content[max(0, match_start-50):min(len(content), match_end+50)]
        if '<a ' in context and '</a>' in context:
            # More precise: find the nearest <a> before match_start
            nearest_open = before.rfind('<a ')
            if nearest_open >= 0:
                # Find corresponding </a> after nearest_open
                segment_after_open = content[nearest_open:]
                close_pos = segment_after_open.find('</a>')
                if close_pos >= 0 and nearest_open < match_start < nearest_open + close_pos + 5:
                    return True
    return False


def linkify_email(content):
    """Wrap bare sales@kdelec.com in mailto link if not already linked."""
    result = []
    last_end = 0
    for m in re.finditer(r'sales@kdelec\.com', content):
        start, end = m.start(), m.end()
        if is_inside_anchor(content, start, end):
            result.append(content[last_end:end])
        else:
            result.append(content[last_end:start])
            result.append('<a href="mailto:sales@kdelec.com">sales@kdelec.com</a>')
        last_end = end
    result.append(content[last_end:])
    return ''.join(result)


def linkify_phone(content):
    """Wrap bare +86-13566954989 in tel link if not already linked."""
    result = []
    last_end = 0
    for m in re.finditer(r'\+86[-\s]?13566954989', content):
        start, end = m.start(), m.end()
        if is_inside_anchor(content, start, end):
            result.append(content[last_end:end])
        else:
            clean_num = m.group().replace('-', '').replace(' ', '')
            result.append(content[last_end:start])
            result.append(f'<a href="tel:{clean_num}">{m.group()}</a>')
        last_end = end
    result.append(content[last_end:])
    return ''.join(result)


def process_html(filepath):
    """Process a single HTML file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  SKIP read: {filepath} ({e})")
        return False

    original = content

    # 1. Add WhatsApp button before </body> (only if not already present)
    if '</body>' in content and 'whatsapp-float' not in content:
        content = content.replace('</body>', WHATSAPP_BLOCK + '\n</body>')

    # 2. Linkify email and phone (only bare occurrences)
    content = linkify_email(content)
    content = linkify_phone(content)

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
    unchanged = 0

    print(f"Processing {total} HTML files...")
    for i, filepath in enumerate(html_files, 1):
        if process_html(filepath):
            modified += 1
        else:
            unchanged += 1
        if i % 50 == 0:
            print(f"  Progress: {i}/{total} ({modified} modified, {unchanged} unchanged)")

    print(f"\nDone! {modified} files modified, {unchanged} files unchanged.")


if __name__ == '__main__':
    main()
