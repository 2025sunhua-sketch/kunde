import os
import re

base_dir = r"C:\Users\ADMIN\.jvs\.openclaw\workspace\kunde-website"
old_style = 'class="header-contact" style="display: flex; align-items: center; justify-content: flex-end; gap: 12px; white-space: nowrap; font-size: 15px; overflow: visible; min-width: 0; flex: 1;">'
new_style = 'class="header-contact" style="display: flex; align-items: center; justify-content: flex-end; gap: 12px; white-space: nowrap; font-size: 15px; overflow: visible; min-width: 0; flex: 1; padding-right: 20px;">'

count = 0
for root, dirs, files in os.walk(base_dir):
    # Skip tmp directory and .git
    if 'tmp' in root or '.git' in root:
        continue
    for file in files:
        if not file.endswith('.html'):
            continue
        filepath = os.path.join(root, file)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            if old_style in content:
                new_content = content.replace(old_style, new_style)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                count += 1
                print(f"Updated: {filepath}")
        except Exception as e:
            print(f"Error processing {filepath}: {e}")

print(f"\nTotal files updated: {count}")
