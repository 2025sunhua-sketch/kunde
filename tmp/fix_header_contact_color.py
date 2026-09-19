import os
import glob
import re

# 遍历所有HTML文件
html_files = glob.glob('*.html') + glob.glob('product/**/*.html', recursive=True) + glob.glob('blog/*.html')

count = 0
for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找并替换header-contact中的内联样式颜色
    # 匹配模式：<div class="header-contact" style="..."> 
    # 将style中的color属性改为#fff（如果已有）或添加
    
    old_pattern = r'(<div class="header-contact" style="[^"]*?)color:\s*inherit([^"]*?")'
    new_replacement = r'\1color: #fff\2'
    
    if re.search(old_pattern, content):
        content = re.sub(old_pattern, new_replacement, content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
        print(f"已更新: {filepath}")
    else:
        # 检查是否已经有正确颜色
        if 'class="header-contact"' in content and 'color: #fff' in content:
            pass  # 已经正确
        elif 'class="header-contact"' in content:
            print(f"需手动检查: {filepath}")

print(f"\n共更新 {count} 个HTML文件")
