import os
import re
from pathlib import Path

workspace = r"C:\Users\ADMIN\.jvs\.openclaw\workspace\kunde-website"

# ============================================
# PART 1: Google Ads Conversion Tracking Code
# ============================================
# TODO: Replace AW-XXXXXXXXX with actual conversion ID from Google Ads
CONVERSION_ID = "AW-XXXXXXXXX"  # ← 需要你替换为实际的转化 ID

conversion_code = f'''<!-- Google Ads Conversion Tracking -->
<script async src="https://www.googletagmanager.com/gtag/js?id={CONVERSION_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{CONVERSION_ID}');
</script>'''

# ============================================
# PART 2: HTML Optimization (lazy loading + font-display)
# ============================================

def optimize_html(filepath):
    """Add lazy loading to images and fix font display"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 1. Add lazy loading to all <img> tags that don't have it
    # Skip images in hero/above-fold sections by checking context
    if '<img' in content:
        # Add loading="lazy" to img tags without explicit loading attribute
        # But skip the first few images (likely above fold)
        img_pattern = r'<img([^>]*?)src="([^"]+)"([^>]*?)>'
        
        def add_lazy_loading(match):
            attrs_before = match.group(1)
            src = match.group(2)
            attrs_after = match.group(3)
            
            # Skip if already has loading attribute
            if 'loading=' in attrs_before or 'loading=' in attrs_after:
                return match.group(0)
            
            # Skip logo and banner images (likely above fold)
            skip_keywords = ['logo', 'banner', 'hero']
            if any(kw in src.lower() for kw in skip_keywords):
                return match.group(0)
            
            # Add loading="lazy" and decoding="async"
            return f'<img{attrs_before}src="{src}"{attrs_after} loading="lazy" decoding="async">'
        
        content = re.sub(img_pattern, add_lazy_loading, content)
    
    # 2. Add width/height attributes to prevent CLS (layout shift)
    # This is a simplified approach - ideally you'd set explicit dimensions
    # For now, we add style="aspect-ratio" as a fallback
    
    # 3. Fix font-display for Google Fonts
    if 'fonts.googleapis.com' in content:
        content = content.replace(
            'fonts.googleapis.com/css2?',
            'fonts.googleapis.com/css2?display=swap&'
        )
    
    # 4. Add preconnect hints for third-party origins
    if '<head>' in content:
        preconnect_hints = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://www.googletagmanager.com">'''
        
        # Check if preconnect already exists
        if 'rel="preconnect"' not in content:
            content = content.replace('<head>', '<head>\n' + preconnect_hints, 1)
    
    # 5. Add conversion code after GA4 (if conversion ID is set)
    if CONVERSION_ID != "AW-XXXXXXXXX" and 'googletagmanager.com/gtag' in content:
        if CONVERSION_ID not in content:
            # Insert right after GA4 script block
            ga4_end_pattern = r"(gtag\('config', 'G-[A-Z0-9]+'\);)\s*</script>"
            match = re.search(ga4_end_pattern, content)
            if match:
                insert_pos = match.end()
                content = content[:insert_pos] + '\n' + conversion_code + content[insert_pos:]
    
    return content if content != original else None

# ============================================
# MAIN EXECUTION
# ============================================

print("=" * 60)
print("🚀 Starting comprehensive optimization...")
print("=" * 60)

# Collect all HTML files
html_files = []
for root, dirs, files in os.walk(workspace):
    if any(skip in root for skip in ['node_modules', '.git', 'tmp']):
        continue
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

print(f"\n📁 Found {len(html_files)} HTML files\n")

# Process HTML files
updated_count = 0
skipped_count = 0
errors = []

for filepath in html_files:
    try:
        result = optimize_html(filepath)
        if result:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(result)
            updated_count += 1
            print(f"✅ {os.path.relpath(filepath, workspace)}")
        else:
            skipped_count += 1
    except Exception as e:
        errors.append((filepath, str(e)))
        print(f"❌ {os.path.basename(filepath)}: {e}")

print(f"\n{'=' * 60}")
print(f"📊 HTML Optimization Summary:")
print(f"   ✅ Updated: {updated_count} files")
print(f"   ️ Skipped (no changes needed): {skipped_count} files")
print(f"   ❌ Errors: {len(errors)} files")

if errors:
    print(f"\n⚠️ Error details:")
    for path, err in errors[:5]:  # Show first 5 errors
        print(f"   - {os.path.basename(path)}: {err}")

print(f"\n💡 Next steps:")
print(f"   1. Replace CONVERSION_ID in this script with your actual AW-XXXXXXXXX")
print(f"   2. Run again to install conversion tracking")
print(f"   3. Convert product images to WebP format (separate script)")
print(f"   4. Commit and push all changes together")
