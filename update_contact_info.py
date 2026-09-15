import os
import re
from pathlib import Path

workspace = r"C:\Users\ADMIN\.jvs\.openclaw\workspace\kunde-website"

# ============================================
# Configuration
# ============================================
OLD_EMAIL = "kundelec@126.com"
NEW_EMAIL = "sales@kdelec.com"
JOTFORM_IFRAME_PATTERN = r'<iframe\s+src="https://form\.jotform\.com/[^"]*"[^>]*>.*?</iframe>'
GOOGLE_FORMS_IFRAME = '''<iframe src="https://docs.google.com/forms/d/e/1FAIpQLSdc4gNKSWBA6E/viewform?embedded=true" width="100%" height="720" frameborder="0" marginheight="0" marginwidth="0">Loading…</iframe>'''

# Email with copy button HTML
EMAIL_WITH_COPY = f'''<span class="email-with-copy" style="display: inline-flex; align-items: center; gap: 8px;">
            <a href="mailto:{NEW_EMAIL}" style="color: inherit; text-decoration: none;">{NEW_EMAIL}</a>
            <button type="button" onclick="navigator.clipboard.writeText('{NEW_EMAIL}'); this.innerHTML='<i class=&quot;fas fa-check&quot;></i>'; setTimeout(()=>this.innerHTML='<i class=&quot;far fa-copy&quot;></i>', 1500);" style="background: none; border: none; cursor: pointer; color: var(--primary-blue, #1a73e8); padding: 4px; font-size: 14px;" title="Copy email address" aria-label="Copy email address"><i class="far fa-copy"></i></button>
          </span>'''

# ============================================
# Processing Functions
# ============================================

def process_html(filepath):
    """Process a single HTML file: replace email, add copy button, replace Jotform"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 1. Replace old email with new email + copy button (only in display contexts)
    # Pattern: mailto links and plain text displays
    if OLD_EMAIL in content:
        # Replace mailto links
        content = content.replace(f'mailto:{OLD_EMAIL}', f'mailto:{NEW_EMAIL}')
        
        # Replace displayed email addresses (not inside mailto)
        # Match patterns like >kundelec@126.com< or : kundelec@126.com
        content = re.sub(
            r'>(?:\s*)' + re.escape(OLD_EMAIL) + r'(?:\s*)<',
            f'>{EMAIL_WITH_COPY}<',
            content
        )
        content = re.sub(
            r':\s*' + re.escape(OLD_EMAIL),
            f': {EMAIL_WITH_COPY}',
            content
        )
    
    # 2. Replace Jotform iframe with Google Forms (only on contact.html)
    if 'contact.html' in filepath or 'Contact' in filepath:
        content = re.sub(JOTFORM_IFRAME_PATTERN, GOOGLE_FORMS_IFRAME, content, flags=re.DOTALL)
    
    return content if content != original else None

# ============================================
# MAIN EXECUTION
# ============================================

print("=" * 60)
print("🚀 Starting comprehensive site update...")
print("=" * 60)
print(f" Email: {OLD_EMAIL} → {NEW_EMAIL}")
print(f"📋 Form: Jotform → Google Forms (contact page only)")
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
        result = process_html(filepath)
        if result:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(result)
            updated_count += 1
            rel_path = os.path.relpath(filepath, workspace)
            print(f"✅ {rel_path}")
        else:
            skipped_count += 1
    except Exception as e:
        errors.append((filepath, str(e)))
        print(f"❌ {os.path.basename(filepath)}: {e}")

print(f"\n{'=' * 60}")
print(f"📊 Update Summary:")
print(f"   ✅ Updated: {updated_count} files")
print(f"   ⏭️ Skipped (no changes needed): {skipped_count} files")
print(f"   ❌ Errors: {len(errors)} files")

if errors:
    print(f"\n⚠️ Error details:")
    for path, err in errors[:5]:
        print(f"   - {os.path.basename(path)}: {err}")

print(f"\n Next steps:")
print(f"   1. Review changes locally")
print(f"   2. Commit and push to GitHub")
print(f"   3. Verify Cloudflare Pages deployment")
