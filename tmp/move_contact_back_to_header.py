import os
import glob
import re

# 遍历所有HTML文件
html_files = glob.glob('*.html') + glob.glob('product/**/*.html', recursive=True) + glob.glob('blog/*.html')

count = 0
for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否有header-contact在nav-bar中
    if '<nav class="nav-bar">' not in content or 'class="header-contact"' not in content:
        continue
    
    # 提取header-contact完整HTML块
    contact_match = re.search(r'<div class="header-contact"[^>]*>.*?</div>\s*</div>\s*</nav>', content, re.DOTALL)
    if not contact_match:
        print(f"未找到联系方式块: {filepath}")
        continue
    
    contact_html = contact_match.group(0)
    
    # 从nav-bar中删除联系方式
    content_without_contact = content.replace(contact_html, '</div>\n </nav>')
    
    # 在header-main的</div></header>前插入联系方式
    header_main_pattern = r'(</a>\s*</div></header>)'
    replacement = contact_html.strip() + '\n\\1'
    new_content = re.sub(header_main_pattern, replacement, content_without_contact)
    
    # 修改header-main的container为flex布局，让logo和联系方式左右分布
    new_content = new_content.replace(
        '<header class="header-main">\n <div class="container">',
        '<header class="header-main">\n <div class="container" style="display: flex; align-items: center; justify-content: space-between;">'
    )
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1
        print(f"已更新: {filepath}")
    else:
        print(f"无变化: {filepath}")

print(f"\n共更新 {count} 个HTML文件")
