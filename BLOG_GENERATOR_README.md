# 🔖 博客自动化生成脚本使用说明

## 📋 功能概述

`generate_blog.py` 是一个 Python 脚本，用于自动生成电力行业专业博文，并同步更新网站索引和 Sitemap。

### 主要功能

1. ✅ 读取 `content_plan.txt` 中的文章标题
2. ✅ 调用 Gemini AI 生成 500+ 字专业英文博文
3. ✅ 自动填充 HTML 模板
4. ✅ 生成文章到 `/blog/` 目录
5. ✅ 更新 `articles.json` 索引
6. ✅ 更新 `sitemap.xml`

---

## 🚀 快速开始

### 第 1 步：安装依赖

```bash
pip install google-generativeai
```

### 第 2 步：设置 API Key

**Windows PowerShell:**
```powershell
$env:GEMINI_API_KEY='your-api-key-here'
```

**Linux/Mac:**
```bash
export GEMINI_API_KEY='your-api-key-here'
```

**获取 API Key:** https://makersuite.google.com/app/apikey

### 第 3 步：准备内容计划

编辑 `content_plan.txt`，每行一个文章标题：

```
How to Choose the Right Cable Lugs for Your Project
Understanding IEC Standards for Electrical Connections
Best Practices for Crimping Copper-Aluminum Terminals
```

### 第 4 步：运行脚本

```bash
python generate_blog.py
```

---

## 📁 生成的文件

| 文件/目录 | 说明 |
|-----------|------|
| `blog/{slug}.html` | 生成的文章页面 |
| `articles.json` | 文章索引（自动更新） |
| `sitemap.xml` | Sitemap（自动添加新 URL） |

---

## 🔧 配置选项

### 环境变量

| 变量名 | 说明 | 必需 |
|--------|------|------|
| `GEMINI_API_KEY` | Gemini API 密钥 | ✅ 是 |

### 脚本配置（可编辑）

在 `generate_blog.py` 中修改：

```python
# 路径配置
BASE_DIR = Path(__file__).parent
BLOG_DIR = BASE_DIR / "blog"

# SEO 配置
SITE_URL = "https://kdelec.com"
COMPANY_NAME = "Kunde Electric"
```

---

## 📊 输出示例

```
============================================================
🚀 Kunde Electric 博客自动生成器
============================================================
📂 工作目录：/path/to/kunde-website
📅 当前时间：2026-05-07 17:30:00

✅ Gemini API 配置成功
📋 找到 10 个文章主题

============================================================
📝 生成文章：How to Choose the Right Cable Lugs...
============================================================
🔖 Slug: how-to-choose-the-right-cable-lugs
🤖 调用 AI 生成内容...
✅ 内容生成成功 (650 字)
📄 填充模板...
✅ 文章已保存：how-to-choose-the-right-cable-lugs.html
✅ articles.json 已更新
✅ sitemap.xml 已更新

✅ 文章生成完成！
📄 文件：how-to-choose-the-right-cable-lugs.html
🔗 URL: https://kdelec.com/blog/how-to-choose-the-right-cable-lugs.html

⏳ 等待 5 秒，避免 API 限流...

============================================================
📊 生成总结
============================================================
✅ 成功：10 篇
❌ 失败：0 篇
📁 输出目录：/path/to/kunde-website/blog
📄 索引文件：articles.json
🗺️  Sitemap: sitemap.xml

💡 下一步：
   1. 检查生成的文章质量
   2. 执行：git add -A && git commit -m '新增博客文章' && git push
   3. 访问：https://kdelec.com/blog.html 查看
```

---

## ⚠️ 注意事项

### API 限制

- Gemini API 有速率限制，脚本已内置 5 秒延迟
- 如需批量生成大量文章，建议分批执行

### 内容审核

- **重要**：生成的内容应人工审核后再发布
- 检查技术准确性
- 确保符合品牌语调

### SEO 最佳实践

- 每篇文章应有独特的标题和关键词
- 避免重复内容
- 定期更新博客（每周 1-2 篇）

---

## 🐛 故障排除

### 问题 1：API Key 错误

```
❌ 错误：未找到 GEMINI_API_KEY 环境变量
```

**解决**：确保已设置环境变量，重启终端后重试。

### 问题 2：缺少依赖库

```
❌ 缺少依赖库，请执行：pip install google-generativeai
```

**解决**：安装依赖库。

### 问题 3：内容生成失败

```
❌ 生成失败：...
```

**解决**：
- 检查网络连接
- 验证 API Key 是否有效
- 查看 Gemini API 状态

---

## 📞 技术支持

如有问题，请联系：
- 邮箱：sales@kdelec.com
- 电话：+86-13566954989

---

**📍 公司地址**: A0-033~035, Binwang Market, Yiwu, Zhejiang, China
