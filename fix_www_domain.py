import re
import os

workspace = r"C:\Users\ADMIN\.jvs\.openclaw\workspace\kunde-website"

# Files to fix (core pages with www.kdelec.com)
files_to_fix = [
    "index.html",
    "about.html", 
    "contact.html",
    "production.html",
    "products.html"
]

for filename in files_to_fix:
    filepath = os.path.join(workspace, filename)
    
    if not os.path.exists(filepath):
        print(f"⚠️ File not found: {filename}")
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace www.kdelec.com with kdelec.com
    new_content = content.replace('https://www.kdelec.com/', 'https://kdelec.com/')
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ Fixed: {filename}")
    else:
        print(f"⏭️ No changes needed: {filename}")

print("\n🎉 All core pages now use https://kdelec.com/")
