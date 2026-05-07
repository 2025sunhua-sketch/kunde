# 如何添加博客文章

## 方法 1：直接创建 HTML 文件（最简单）

1. 在 `/blog/` 目录下创建 HTML 文件，如 `post-001.html`
2. 复制以下模板：

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>文章标题 | Kunde Electric</title>
  <link rel="stylesheet" href="../css/style.css">
  <link rel="stylesheet" href="../css/mobile-optimized.css">
</head>
<body>
  <!-- 导航栏 -->
  <nav class="nav-bar">
    <div class="container">
      <ul class="nav-menu">
        <li><a href="../index.html">HOME</a></li>
        <li><a href="../about.html">ABOUT US</a></li>
        <li><a href="../products.html">PRODUCT</a></li>
        <li><a href="index.html">BLOG</a></li>
        <li><a href="../contact.html">CONTACT US</a></li>
      </ul>
    </div>
  </nav>

  <!-- 文章内容 -->
  <main class="faq-container">
    <div class="container" style="max-width: 800px; padding: 60px 20px;">
      <h1 style="font-size: 36px; color: #1a3d6e; margin-bottom: 16px;">文章标题</h1>
      <p style="color: #666; margin-bottom: 40px;">发布日期：2026-05-07</p>
      
      <div style="font-size: 16px; line-height: 1.8; color: #333;">
        <p>这里是文章内容...</p>
      </div>
    </div>
  </main>

  <!-- 页脚 -->
  <footer class="footer">
    <div class="container">
      <p>&copy; 2024 KUNDE ELECTRIC. All rights reserved.</p>
    </div>
  </footer>
</body>
</html>
```

3. 在 `blog/index.html` 中添加文章链接

---

## 方法 2：使用 Markdown（推荐）

1. 在 `/blog/posts/` 目录创建 `.md` 文件
2. 使用 GitHub Actions 自动转换为 HTML

### 示例文章结构

```markdown
---
title: 文章标题
date: 2026-05-07
author: Kunde Electric
excerpt: 文章摘要...
---

# 文章标题

这里是文章内容...
```

---

## 方法 3：使用第三方服务

- **Medium** - 创建文章后嵌入
- **Dev.to** - 技术博客平台
- **Hashnode** - 开发者博客平台

---

## 当前建议

**先使用方法 1**，手动创建几篇 HTML 文章，后续可以再自动化。

需要我帮你创建文章模板吗？
