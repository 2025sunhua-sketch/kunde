import re

# 读取index.html
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 从header-main中提取.header-contact的HTML
contact_match = re.search(r'<div class="header-contact"[^>]*>.*?</div>\s*</header>', content, re.DOTALL)
if not contact_match:
    print("未找到header-contact")
    exit(1)

contact_html = contact_match.group(0).replace('</header>', '').strip()

# 将联系方式文字改为白色（适配深蓝导航栏背景）
contact_html = contact_html.replace('color: inherit;', 'color: #fff;')
contact_html = contact_html.replace('color: var(--primary-blue, #1a73e8);', 'color: #fff;')
# 移除多余的padding-right和flex:1等旧样式
contact_html = contact_html.replace('justify-content: flex-end; gap: 12px; white-space: nowrap; font-size: 15px; overflow: visible; min-width: 0; flex: 1; padding-right: 60px;', 'gap: 12px; white-space: nowrap; font-size: 14px; color: #fff;')

# 移除header-main中的.header-contact
content = re.sub(r'\s*<div class="header-contact"[^>]*>.*?</div>\s*', '\n', content, flags=re.DOTALL)

# 在nav-bar的container添加flex布局
old_nav_container = '<div class="container">\n <ul class="nav-menu">'
new_nav_container = '<div class="container" style="display: flex; align-items: center; justify-content: space-between;">\n <ul class="nav-menu">'
content = content.replace(old_nav_container, new_nav_container)

# 在</ul>后插入联系方式
old_ul_end = ''' </ul>
 </div>
 </nav>'''

new_ul_end = f''' </ul>
 {contact_html}
 </div>
 </nav>'''

content = content.replace(old_ul_end, new_ul_end)

# 写回文件
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("index.html修改完成 - 联系方式已移至nav-bar右侧，文字改为白色")
