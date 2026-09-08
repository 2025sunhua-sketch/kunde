import os
import re

workspace = r"C:\Users\ADMIN\.jvs\.openclaw\workspace\kunde-website"

# GA4 tracking code
ga4_code = '''<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-GBP1X70205"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-GBP1X70205');
</script>'''

# Find all HTML files in root and product directories
html_files = []
for root, dirs, files in os.walk(workspace):
    # Skip node_modules, .git, etc.
    if any(skip in root for skip in ['node_modules', '.git', 'tmp']):
        continue
    
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

print(f"Found {len(html_files)} HTML files to process\n")

updated_count = 0
skipped_count = 0

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if GA4 already exists
    if 'G-GBP1X70205' in content or 'googletagmanager.com/gtag' in content:
        print(f"️  Already has GA4: {os.path.basename(filepath)}")
        skipped_count += 1
        continue
    
    # Insert GA4 code right after <head> tag
    if '<head>' in content:
        new_content = content.replace('<head>', '<head>\n' + ga4_code, 1)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ Added GA4: {os.path.basename(filepath)}")
        updated_count += 1
    else:
        print(f"⚠️  No <head> tag found: {os.path.basename(filepath)}")
        skipped_count += 1

print(f"\n Summary:")
print(f"   ✅ Updated: {updated_count} files")
print(f"   ️ Skipped (already has GA4): {skipped_count} files")
print(f"    Total processed: {len(html_files)} files")
print(f"\n💡 Measurement ID: G-GBP1X70205")
