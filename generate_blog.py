#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kunde Electric Blog Generator
自动生成电力行业专业博文，同步更新索引和 Sitemap

功能：
1. 读取 content_plan.txt 中的文章标题/关键词
2. 调用 Gemini API 生成专业英文博文（500+ 字）
3. 填充 article-template.html 模板
4. 生成 HTML 文件到 /blog/ 目录
5. 更新 articles.json 和 sitemap.xml

安全提示：
- API Key 从环境变量 GEMINI_API_KEY 读取
- 不要将 API Key 直接写入代码
"""

import os
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

# 尝试导入 google-generativeai 库
try:
    import google.generativeai as genai
except ImportError:
    print("❌ 缺少依赖库，请执行：pip install google-generativeai")
    sys.exit(1)


# ==================== 配置区域 ====================

# 路径配置
BASE_DIR = Path(__file__).parent
BLOG_DIR = BASE_DIR / "blog"
TEMPLATE_FILE = BLOG_DIR / "article-template.html"
CONTENT_PLAN_FILE = BASE_DIR / "content_plan.txt"
ARTICLES_JSON_FILE = BASE_DIR / "articles.json"
SITEMAP_FILE = BASE_DIR / "sitemap.xml"

# SEO 配置
SITE_URL = "https://kdelec.com"
COMPANY_NAME = "Kunde Electric"
COMPANY_ADDRESS = "A0-033~035, Binwang Market, Yiwu, Zhejiang, China"

# 电力行业关键词库（用于增强 SEO）
POWER_INDUSTRY_KEYWORDS = [
    "electrical connections", "cable lugs", "power fittings", "terminals",
    "electrical safety", "IEC standards", "ISO 9001", "quality assurance",
    "power distribution", "electrical infrastructure", "crimping technology",
    "bimetallic connectors", "copper aluminum terminals", "voltage systems"
]


# ==================== Gemini API 配置 ====================

def configure_gemini_api():
    """
    配置 Gemini API
    API Key 从环境变量读取，确保安全
    """
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ 错误：未找到 GEMINI_API_KEY 环境变量")
        print("\n📋 设置方法：")
        print("  Windows PowerShell: $env:GEMINI_API_KEY='your-api-key'")
        print("  Linux/Mac: export GEMINI_API_KEY='your-api-key'")
        print("\n🔑 获取 API Key: https://makersuite.google.com/app/apikey")
        sys.exit(1)
    
    try:
        genai.configure(api_key=api_key)
        print("✅ Gemini API 配置成功")
        return True
    except Exception as e:
        print(f"❌ API 配置失败：{e}")
        sys.exit(1)


def get_gemini_model():
    """获取 Gemini 模型实例"""
    return genai.GenerativeModel('gemini-pro')


# ==================== 内容生成 ====================

def generate_article_content(title: str, keywords: List[str] = None) -> Optional[str]:
    """
    调用 Gemini API 生成博文内容
    
    Args:
        title: 文章标题
        keywords: 关键词列表（可选）
    
    Returns:
        生成的文章内容（HTML 格式），失败返回 None
    """
    if keywords is None:
        keywords = POWER_INDUSTRY_KEYWORDS[:5]
    
    # 构建专业的提示词
    prompt = f"""You are a professional technical writer for Kunde Electric, a leading manufacturer of electrical fittings and power connection solutions based in Yiwu, China.

Write a comprehensive, professional blog article about: "{title}"

Requirements:
1. Length: Minimum 500 words
2. Language: Professional English
3. Tone: Authoritative, informative, industry-focused
4. Target Audience: Electrical engineers, procurement managers, B2B buyers
5. Format: HTML format with proper tags (<h2>, <h3>, <p>, <ul>, <li>)

Content Structure:
- Start with an engaging introduction (2-3 paragraphs)
- Include 3-4 main sections with <h2> headings
- Add technical details and industry insights
- Include practical tips or best practices
- End with a conclusion that reinforces expertise

SEO Keywords to naturally incorporate: {', '.join(keywords)}

Company Context (mention naturally where relevant):
- Company: Kunde Electric (KDELEC)
- Location: Yiwu, Zhejiang, China (A0-033~035, Binwang Market)
- Experience: 12+ years in electrical fittings manufacturing
- Certifications: ISO 9001:2015, IEC, UL, CE compliant
- Export: 60+ countries worldwide

Important:
- Do NOT include <html>, <head>, <body> tags (content only)
- Do NOT include markdown code blocks
- Write in clear, professional English
- Focus on providing genuine value to readers
- Position Kunde Electric as a trusted industry expert

Generate the article content now:"""

    try:
        model = get_gemini_model()
        response = model.generate_content(prompt)
        
        if response and response.text:
            content = response.text.strip()
            
            # 清理可能的 markdown 标记
            content = re.sub(r'^```html\s*', '', content)
            content = re.sub(r'\s*```$', '', content)
            content = content.strip()
            
            # 验证字数（简单估算）
            word_count = len(content.split())
            if word_count < 500:
                print(f"⚠️  生成内容字数不足 ({word_count} 字)，但将继续处理")
            
            print(f"✅ 内容生成成功 ({word_count} 字)")
            return content
        else:
            print("❌ API 返回空响应")
            return None
            
    except Exception as e:
        print(f"❌ 生成失败：{e}")
        return None


# ==================== 模板处理 ====================

def load_template() -> Optional[str]:
    """加载文章模板"""
    try:
        if not TEMPLATE_FILE.exists():
            print(f"❌ 模板文件不存在：{TEMPLATE_FILE}")
            return None
        
        with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"❌ 读取模板失败：{e}")
        return None


def fill_template(template: str, title: str, content: str, slug: str, 
                  description: str, keywords: str, published_date: str) -> str:
    """
    填充模板占位符
    
    Args:
        template: 模板内容
        title: 文章标题
        content: 文章内容
        slug: URL 友好标识
        description: SEO 描述
        keywords: 关键词
        published_date: 发布日期
    
    Returns:
        填充后的 HTML 内容
    """
    # 生成修改日期（7 天后）
    modified_date = datetime.now().strftime("%Y-%m-%d")
    
    # 替换所有占位符
    replacements = {
        '{{TITLE}}': title,
        '{{SLUG}}': slug,
        '{{DESCRIPTION}}': description,
        '{{KEYWORDS}}': keywords,
        '{{PUBLISHED_DATE}}': published_date,
        '{{MODIFIED_DATE}}': modified_date,
        '{{CONTENT}}': content
    }
    
    filled_content = template
    for placeholder, value in replacements.items():
        filled_content = filled_content.replace(placeholder, value)
    
    return filled_content


def save_article(html_content: str, slug: str) -> bool:
    """
    保存文章到 /blog/ 目录
    
    Args:
        html_content: HTML 内容
        slug: URL 标识
    
    Returns:
        保存成功返回 True
    """
    try:
        output_file = BLOG_DIR / f"{slug}.html"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ 文章已保存：{output_file.name}")
        return True
    except Exception as e:
        print(f"❌ 保存失败：{e}")
        return False


# ==================== 索引更新 ====================

def update_articles_json(title: str, slug: str, excerpt: str, date: str) -> bool:
    """
    更新 articles.json 索引
    
    Args:
        title: 文章标题
        slug: URL 标识
        excerpt: 摘要
        date: 发布日期
    """
    try:
        # 读取现有数据
        articles = []
        if ARTICLES_JSON_FILE.exists():
            with open(ARTICLES_JSON_FILE, 'r', encoding='utf-8') as f:
                articles = json.load(f)
        
        # 添加新文章（添加到开头）
        new_article = {
            "title": title,
            "slug": slug,
            "excerpt": excerpt,
            "date": date,
            "url": f"{SITE_URL}/blog/{slug}.html"
        }
        
        articles.insert(0, new_article)
        
        # 写回文件
        with open(ARTICLES_JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(articles, f, indent=2, ensure_ascii=False)
        
        print(f"✅ articles.json 已更新")
        return True
    except Exception as e:
        print(f"❌ 更新索引失败：{e}")
        return False


def update_sitemap(slug: str, date: str) -> bool:
    """
    更新 sitemap.xml，添加新文章 URL
    
    Args:
        slug: URL 标识
        date: 发布日期
    """
    try:
        if not SITEMAP_FILE.exists():
            print("⚠️  sitemap.xml 不存在，跳过更新")
            return False
        
        # 读取 sitemap
        with open(SITEMAP_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 创建新的 URL 条目
        new_entry = f"""
  <!-- Blog Article -->
  <url>
    <loc>{SITE_URL}/blog/{slug}.html</loc>
    <lastmod>{date}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>
"""
        
        # 在 </urlset> 前插入
        if '</urlset>' in content:
            content = content.replace('</urlset>', new_entry + '\n</urlset>')
            
            # 写回文件
            with open(SITEMAP_FILE, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ sitemap.xml 已更新")
            return True
        else:
            print("❌ sitemap.xml 格式错误")
            return False
            
    except Exception as e:
        print(f"❌ 更新 sitemap 失败：{e}")
        return False


# ==================== 工具函数 ====================

def read_content_plan() -> List[str]:
    """
    读取内容计划文件
    
    Returns:
        标题/关键词列表
    """
    if not CONTENT_PLAN_FILE.exists():
        print(f"❌ 内容计划文件不存在：{CONTENT_PLAN_FILE}")
        print("\n📝 请创建 content_plan.txt，每行一个文章标题，例如：")
        print("   How to Choose the Right Cable Lugs for Your Project")
        print("   Understanding IEC Standards for Electrical Connections")
        print("   Best Practices for Crimping Copper-Aluminum Terminals")
        return []
    
    try:
        with open(CONTENT_PLAN_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 过滤空行和注释
        titles = [line.strip() for line in lines 
                  if line.strip() and not line.strip().startswith('#')]
        
        print(f"📋 找到 {len(titles)} 个文章主题")
        return titles
    except Exception as e:
        print(f"❌ 读取内容计划失败：{e}")
        return []


def generate_slug(title: str) -> str:
    """
    从标题生成 URL 友好的 slug
    
    Args:
        title: 文章标题
    
    Returns:
        slug 字符串
    """
    # 转小写
    slug = title.lower()
    # 替换非字母数字字符为连字符
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    # 移除首尾连字符
    slug = slug.strip('-')
    # 限制长度
    slug = slug[:60]
    
    return slug


def generate_excerpt(content: str, max_length: int = 160) -> str:
    """
    从内容生成摘要
    
    Args:
        content: HTML 内容
        max_length: 最大长度
    
    Returns:
        摘要文本
    """
    # 移除 HTML 标签
    text = re.sub(r'<[^>]+>', ' ', content)
    # 移除多余空白
    text = re.sub(r'\s+', ' ', text).strip()
    # 截断
    if len(text) > max_length:
        text = text[:max_length-3] + '...'
    
    return text


# ==================== 主流程 ====================

def generate_single_article(title: str) -> bool:
    """
    生成单篇文章的完整流程
    
    Args:
        title: 文章标题
    
    Returns:
        成功返回 True
    """
    print(f"\n{'='*60}")
    print(f"📝 生成文章：{title}")
    print(f"{'='*60}")
    
    # 1. 生成 slug
    slug = generate_slug(title)
    print(f"🔖 Slug: {slug}")
    
    # 检查是否已存在
    existing_file = BLOG_DIR / f"{slug}.html"
    if existing_file.exists():
        print(f"⚠️  文章已存在，跳过：{existing_file.name}")
        return False
    
    # 2. 调用 API 生成内容
    print("🤖 调用 AI 生成内容...")
    content = generate_article_content(title)
    
    if not content:
        print("❌ 内容生成失败，跳过此文章")
        return False
    
    # 3. 加载模板
    template = load_template()
    if not template:
        return False
    
    # 4. 生成 SEO 元数据
    description = generate_excerpt(content, 160)
    keywords = ", ".join(POWER_INDUSTRY_KEYWORDS[:10])
    published_date = datetime.now().strftime("%Y-%m-%d")
    
    # 5. 填充模板
    print("📄 填充模板...")
    html_content = fill_template(
        template=template,
        title=title,
        content=content,
        slug=slug,
        description=description,
        keywords=keywords,
        published_date=published_date
    )
    
    # 6. 保存文章
    if not save_article(html_content, slug):
        return False
    
    # 7. 更新索引
    excerpt = generate_excerpt(content, 200)
    update_articles_json(title, slug, excerpt, published_date)
    
    # 8. 更新 sitemap
    update_sitemap(slug, published_date)
    
    print(f"\n✅ 文章生成完成！")
    print(f"📄 文件：{slug}.html")
    print(f"🔗 URL: {SITE_URL}/blog/{slug}.html")
    
    return True


def main():
    """主函数"""
    print("="*60)
    print("🚀 Kunde Electric 博客自动生成器")
    print("="*60)
    print(f"📂 工作目录：{BASE_DIR}")
    print(f"📅 当前时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 1. 配置 API
    configure_gemini_api()
    
    # 2. 读取内容计划
    titles = read_content_plan()
    if not titles:
        return
    
    # 3. 生成文章
    success_count = 0
    for title in titles:
        if generate_single_article(title):
            success_count += 1
        
        # 避免 API 限流，添加延迟
        if titles.index(title) < len(titles) - 1:
            print("\n⏳ 等待 5 秒，避免 API 限流...")
            import time
            time.sleep(5)
    
    # 4. 总结
    print("\n" + "="*60)
    print("📊 生成总结")
    print("="*60)
    print(f"✅ 成功：{success_count} 篇")
    print(f"❌ 失败：{len(titles) - success_count} 篇")
    print(f"📁 输出目录：{BLOG_DIR}")
    print(f"📄 索引文件：{ARTICLES_JSON_FILE}")
    print(f"🗺️  Sitemap: {SITEMAP_FILE}")
    print()
    print("💡 下一步：")
    print("   1. 检查生成的文章质量")
    print("   2. 执行：git add -A && git commit -m '新增博客文章' && git push")
    print("   3. 访问：https://kdelec.com/blog.html 查看")
    print()


if __name__ == "__main__":
    main()
