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

# 移除header-main中的.header-contact
content = re.sub(r'\s*<div class="header-contact"[^>]*>.*?</div>\s*', '\n', content, flags=re.DOTALL)

# 在nav-bar的</ul>后、</div></nav>前插入联系方式
# 将container改为flex布局，并在</ul>后添加联系方式
old_nav = ''' <!-- Navigation Bar -->
 <nav class="nav-bar">
 <div class="container">
 <ul class="nav-menu">'''

new_nav = ''' <!-- Navigation Bar -->
 <nav class="nav-bar">
 <div class="container" style="display: flex; align-items: center; justify-content: space-between;">
 <ul class="nav-menu">'''

content = content.replace(old_nav, new_nav)

# 在</ul>后插入联系方式（注意保留原有的</div></nav>）
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

print("index.html修改完成")
