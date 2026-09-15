import os
import re
from pathlib import Path

workspace = r"C:\Users\ADMIN\.jvs\.openclaw\workspace\kunde-website"

# Compact inline copy button — no line break, tight spacing
NEW_EMAIL = "sales@kdelec.com"
EMAIL_WITH_COPY_COMPACT = f'''<span class="email-with-copy" style="display: inline-flex; align-items: center; gap: 6px; white-space: nowrap;">
            <a href="mailto:{NEW_EMAIL}" style="color: inherit; text-decoration: none;">{NEW_EMAIL}</a>
            <button type="button" onclick="navigator.clipboard.writeText('{NEW_EMAIL}'); this.innerHTML='<i class=&quot;fas fa-check&quot;></i>'; setTimeout(()=>this.innerHTML='<i class=&quot;far fa-copy&quot;></i>', 1500);" style="background: none; border: none; cursor: pointer; color: var(--primary-blue, #1a73e8); padding: 2px 4px; font-size: 13px; line-height: 1;" title="Copy email address" aria-label="Copy email address"><i class="far fa-copy"></i></button>
          </span>'''

def process_html(filepath):
    """Replace the bloated email+copy block with compact inline version"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Find and replace the old email-with-copy span (which had display: inline-flex but caused line breaks)
    # Pattern: the entire span block we inserted earlier
    old_pattern = r'<span class="email-with-copy"[^>]*>.*?</span>'
    
    def replace_match(match):
        old_span = match.group(0)
        # Only replace if it contains our new email (to avoid touching other spans)
        if NEW_EMAIL in old_span:
            return EMAIL_WITH_COPY_COMPACT
        return old_span
    
    content = re.sub(old_pattern, replace_match, content, flags=re.DOTALL)
    
    return content if content != original else None

# ============================================
# MAIN EXECUTION
# ============================================

print("=" * 60)
print("🔧 Fixing email copy button layout...")
print("=" * 60)

html_files = []
for root, dirs, files in os.walk(workspace):
    if any(skip in root for skip in ['node_modules', '.git', 'tmp']):
        continue
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

print(f"\n📁 Scanning {len(html_files)} HTML files\n")

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
print(f" Layout Fix Summary:")
print(f"   ✅ Updated: {updated_count} files")
print(f"   ⏭️ Skipped: {skipped_count} files")
print(f"   ❌ Errors: {len(errors)} files")

if errors:
    print(f"\n⚠️ Error details:")
    for path, err in errors[:5]:
        print(f"   - {os.path.basename(path)}: {err}")
