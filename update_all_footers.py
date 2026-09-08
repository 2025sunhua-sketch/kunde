import os
import re

workspace = r"C:\Users\ADMIN\.jvs\.openclaw\workspace\kunde-website"

# 需要更新的核心页面(排除 product/ 子目录和 blog/ 子目录中的文章)
core_pages = [
    "index.html",
    "about.html",
    "contact.html",
    "products.html",
    "production.html",
    "faq.html",
    "blog.html",
    "privacy-policy.html",
    "warranty-policy.html"
]

# 页脚底部要添加的链接代码
footer_links_html = '''        <p style="margin-top: 8px; font-size: 14px;">
          <a href="privacy-policy.html" style="color: #ccc; margin-right: 16px;">Privacy Policy</a>
          <a href="warranty-policy.html" style="color: #ccc;">Warranty & After-sales Policy</a>
        </p>'''

updated_count = 0
skipped_count = 0

for filename in core_pages:
    filepath = os.path.join(workspace, filename)
    
    if not os.path.exists(filepath):
        print(f"⚠️ File not found: {filename}")
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已存在 footer-bottom 区域
    if '<div class="footer-bottom">' in content:
        # 查找 footer-bottom 的结束标签
        pattern = r'(<div class="footer-bottom">.*?<p>&copy;.*?</p>)'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            # 在 copyright 后插入新链接
            original_text = match.group(1)
            new_text = original_text + '\n' + footer_links_html
            
            new_content = content.replace(original_text, new_text)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ Updated: {filename}")
            updated_count += 1
        else:
            print(f"⚠️ Could not find pattern in: {filename}")
            skipped_count += 1
    else:
        print(f"⚠️ No footer-bottom found in: {filename}")
        skipped_count += 1

print(f"\n📊 Summary:")
print(f"   ✅ Updated: {updated_count} files")
print(f"   ⏭️ Skipped: {skipped_count} files")
print(f"   🎯 Total processed: {len(core_pages)} files")
