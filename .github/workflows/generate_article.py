import os
import requests
import json
from datetime import datetime

# 1. 获取下个标题
plan_file = 'content_plan.txt'
if not os.path.exists(plan_file):
    exit(0)

with open(plan_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

topic = ""
remaining_lines = []
found = False

for line in lines:
    clean_line = line.strip()
    if not found and clean_line and not clean_line.startswith('#'):
        topic = clean_line
        found = True
    else:
        remaining_lines.append(line)

if not topic:
    print("没有发现待处理的标题")
    exit(0)

# 2. 生成文件名 (Slug)
slug = topic.lower().replace(' ', '-').replace('/', '-').strip('-')
filename = f"blog/{slug}.html"

# 3. 调用 AI 生成内容
api_key = os.getenv('GEMINI_API_KEY')
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
prompt = f"Write a professional 800-word technical blog article about: {topic} for the power fittings industry. Use HTML tags like <h2>, <p>, <ul>. Write in English."

payload = {"contents": [{"parts": [{"text": prompt}]}]}
response = requests.post(url, json=payload)
ai_text = response.json()['candidates'][0]['content']['parts'][0]['text']
ai_content = ai_text.replace('\n', '<br>')

# 4. 读取模板并生成文件
template_path = 'blog/article-template.html'
with open(template_path, 'r', encoding='utf-8') as f:
    template = f.read()

final_html = template.replace('{{TITLE}}', topic).replace('{{DATE}}', datetime.now().strftime('%Y-%m-%d')).replace('{{CONTENT}}', ai_content)

with open(filename, 'w', encoding='utf-8') as f:
    f.write(final_html)

# 5. 更新 content_plan.txt (删除已用标题)
with open(plan_file, 'w', encoding='utf-8') as f:
    f.writelines(remaining_lines)

# 6. 更新 index.html 列表
index_path = 'index.html'
if os.path.exists(index_path):
    with open(index_path, 'r', encoding='utf-8') as f:
        index_content = f.read()
    
    new_link = f'\n<a href="{filename}" class="blog-card"><h2>{topic}</h2><p>Published on {datetime.now().strftime("%Y-%m-%d")}</p></a>'
    if '' in index_content:
        updated_index = index_content.replace('', '' + new_link)
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(updated_index)

print(f"✅ 成功生成: {filename}")