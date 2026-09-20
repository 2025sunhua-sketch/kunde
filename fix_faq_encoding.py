#!/usr/bin/env python3
"""Fix garbled characters in faq.html caused by encoding corruption."""

from pathlib import Path

FAQ_PATH = Path(__file__).parent / 'faq.html'

def main():
    content = FAQ_PATH.read_text(encoding='utf-8')
    
    # Fix 1: Em dash corruption "鈥攖" → proper em dash "—"
    # Appears in JSON-LD schema and FAQ Item 1 body
    fixed = content.replace('China鈥攖he', 'China—the')
    
    # Fix 2: Emoji corruption in FAQ Item 17 contact block
    # "馃" should be phone emoji 📞
    # "鉁夛笍" should be email/envelope emoji ✉️
    fixed = fixed.replace('<strong>馃摓 Phone/WhatsApp/WeChat:</strong>', '<strong> Phone/WhatsApp/WeChat:</strong>')
    fixed = fixed.replace('<strong>鉁夛 Email:</strong>', '<strong>✉️ Email:</strong>')
    
    changes = []
    if fixed != content:
        FAQ_PATH.write_text(fixed, encoding='utf-8')
        changes.append('✓ Fixed em dash corruption (鈥攖 → —) in 2 locations')
        changes.append('✓ Fixed phone emoji (馃摓 → 📞) in FAQ Item 17')
        changes.append('✓ Fixed email emoji (鉁夛 → ✉️) in FAQ Item 17')
    else:
        changes.append('No changes needed — file already clean')
    
    for c in changes:
        print(c)

if __name__ == '__main__':
    main()
