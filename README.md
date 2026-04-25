# KUNDE ELECTRIC Website

KUNDE ELECTRIC 官方企业官网 - 电力金具与输配电设备制造商品牌展示平台

## 📁 项目结构

```
kunde-website/
├── index.html          # 首页
├── about.html          # 关于我们
├── products.html       # 产品列表
├── production.html     # 生产线
├── contact.html        # 联系我们
├── vercel.json         # Vercel 部署配置
├── css/
│   └── style.css       # 全局样式
├── js/
│   └── main.js         # 交互脚本
└── images/
    ├── banner1.jpg     # Banner 图片 1（工厂）
    ├── banner2.jpg     # Banner 图片 2（团队/产品）
    └── banner3.jpg     # Banner 图片 3（产品展示）
```

## 🚀 部署到 Vercel

### 方法一：Vercel CLI（推荐）

1. **安装 Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **登录 Vercel**
   ```bash
   vercel login
   ```

3. **进入项目目录**
   ```bash
   cd kunde-website
   ```

4. **部署**
   ```bash
   vercel
   ```
   
   按提示操作：
   - Set up and deploy? **Y**
   - Which scope? 选择你的账号
   - Link to existing project? **N**
   - What's your project's name? **kunde-electric**
   - In which directory is your code located? **./**
   - Want to override the settings? **N**

5. **生产环境部署**
   ```bash
   vercel --prod
   ```

### 方法二：GitHub + Vercel 自动部署

1. **创建 GitHub 仓库**
   ```bash
   cd kunde-website
   git init
   git add .
   git commit -m "Initial commit - KUNDE ELECTRIC website"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/kunde-electric.git
   git push -u origin main
   ```

2. **在 Vercel 连接 GitHub**
   - 访问 https://vercel.com/new
   - 点击 "Import Git Repository"
   - 选择刚才创建的仓库
   - 点击 "Deploy"

3. **自动部署**
   - 之后每次 push 到 GitHub 都会自动部署

### 方法三：Vercel Dashboard 手动上传

1. 访问 https://vercel.com
2. 点击 "Add New Project"
3. 选择 "Deploy"（不使用 Git）
4. 拖拽 `kunde-website` 文件夹到上传区域
5. 点击 "Deploy"

## 📧 配置联系表单

网站使用 Formspree 处理联系表单提交：

1. **注册 Formspree**
   - 访问 https://formspree.io/
   - 创建免费账号
   - 点击 "New Form"
   - 设置表单名称（如 "KUNDE ELECTRIC Inquiry"）
   - 设置接收邮箱为 `kundelec@126.com`

2. **获取 Form ID**
   - 创建表单后，你会得到一个 URL，格式为：`https://formspree.io/f/xxxxxxxx`
   - 复制最后的 ID（`xxxxxxxx` 部分）

3. **更新配置**
   - 打开 `contact.html`
   - 找到 `<form id="contactForm" action="https://formspree.io/f/YOUR_FORM_ID" method="POST">`
   - 将 `YOUR_FORM_ID` 替换为你的实际 Form ID
   
   - 打开 `js/main.js`
   - 找到 `const formspreeUrl = 'https://formspree.io/f/YOUR_FORM_ID';`
   - 同样替换为你的 Form ID

4. **测试表单**
   - 访问网站，填写联系表单
   - 提交后应该收到确认邮件
   - 检查 `kundelec@126.com` 是否收到询盘

## 🎨 自定义内容

### 替换占位图片

产品图片目前使用占位图，替换方法：

1. 准备产品图片（建议尺寸：400x300px，白底精修图）
2. 放入 `images/` 目录
3. 更新 HTML 中的图片路径，例如：
   ```html
   <img src="images/pg-clamp.jpg" alt="PG Clamp">
   ```

### 修改社交媒体链接

在所有页面的 footer 部分找到：
```html
<div class="footer-social">
  <a href="#" aria-label="Facebook">F</a>
  <a href="#" aria-label="Twitter">T</a>
  <a href="#" aria-label="YouTube">Y</a>
</div>
```

将 `#` 替换为实际的社交媒体主页链接。

### 添加 Google Maps

**当前状态：** 已添加基础地图 embed 代码（ approximate 位置）

**获取精确位置的 embed 代码：**

1. 访问 https://www.google.com/maps
2. 搜索公司地址：`Yiwu Binwang Market A0-033~035, Yiwu, Zhejiang, China`
3. 点击 "分享" 按钮
4. 选择 "嵌入地图" 标签
5. 点击 "复制 HTML"
6. 打开 `contact.html`
7. 找到 `<iframe>` 标签（约第 200 行）
8. 将 `src="..."` 中的 URL 替换为你复制的 embed URL

**提示：** 如果市场位置在 Google Maps 上找不到，可以使用义乌市或义乌国际商贸城作为参考位置。

## 📊 网站特性

- ✅ 响应式设计（支持手机/平板/桌面）
- ✅ 三语轮播图（5 秒自动切换）
- ✅ 移动端底部固定联系栏
- ✅ 图片懒加载优化
- ✅ SEO 优化（meta 标签）
- ✅ 联系表单验证
- ✅ 平滑滚动动画
- ✅ 品牌色彩系统（深蓝 #0A2E5C + 红色 #C41E3A）

## 🌐 域名配置（可选）

如果有自定义域名：

1. 在 Vercel Dashboard 进入项目
2. 点击 "Domains"
3. 添加你的域名（如 `www.kundeelectric.com`）
4. 按照提示配置 DNS 记录

## 📝 维护建议

1. **定期备份**：定期将项目文件备份到 Git 仓库
2. **图片优化**：使用 TinyPNG 等工具压缩图片
3. **表单测试**：每月测试一次联系表单是否正常工作
4. **内容更新**：及时更新产品信息和公司动态

## 🛠️ 技术支持

如遇问题，检查：
- Vercel 部署日志：https://vercel.com/dashboard
- 浏览器控制台错误：F12 → Console
- Formspree 提交记录：https://formspree.io/dashboard

---

**© 2024 KUNDE ELECTRIC. All rights reserved.**
