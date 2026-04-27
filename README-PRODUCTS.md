# 产品列表生成工具
# Product List Generator for KUNDE ELECTRIC Website

## 使用方法 / Usage

### 方法 1：手动创建 product-list.json

在每个类别文件夹中创建 `product-list.json` 文件：

**路径 / Path:**
```
images/products/product/1 电缆端子 Cable Lugs and Connectors/product-list.json
images/products/product/2 绝缘端子 Insulated Terminals/product-list.json
images/products/product/3 电缆夹具 Cable Clamps/product-list.json
```

**格式 / Format:**
```json
[
  {
    "folder": "1 DTL-1 铜铝过渡 DTL-1 Bimetal Cable Lugs",
    "name": "DTL-1 Bimetal Cable Lugs",
    "images": ["1.jpg", "2.jpg", "3.jpg"],
    "detailImage": "detail.jpg",
    "imageCount": 3
  },
  {
    "folder": "2 Product Name",
    "name": "Product Name",
    "images": ["1.jpg", "2.jpg"],
    "detailImage": "parameter.jpg",
    "imageCount": 2
  }
]
```

### 方法 2：使用 PowerShell 脚本自动生成

运行 PowerShell 脚本自动扫描所有产品文件夹：

```powershell
cd C:\Users\ADMIN\.jvs\.openclaw\workspace\kunde-website
powershell -ExecutionPolicy Bypass -File "generate-product-lists.ps1"
```

---

## 文件夹结构 / Folder Structure

```
images/products/product/
├── 1 电缆端子 Cable Lugs and Connectors/
│   ├── product-list.json          ← 需要生成这个文件
│   ├── 1 DTL-1 铜铝过渡 DTL-1 Bimetal Cable Lugs/
│   │   ├── 1.jpg
│   │   ├── 2.jpg
│   │   └── detail.jpg
│   └── ...
├── 2 绝缘端子 Insulated Terminals/
│   ├── product-list.json
│   └── ...
└── 3 电缆夹具 Cable Clamps/
    ├── product-list.json
    └── ...
```

---

## 产品详情页 / Product Detail Page

访问产品详情页：
```
product-detail.html?category=1&product=产品文件夹名
```

**示例 / Example:**
```
product-detail.html?category=1&product=1 DTL-1 铜铝过渡 DTL-1 Bimetal Cable Lugs
```

---

## 注意事项 / Notes

1. **图片命名 / Image Naming:**
   - 主图使用数字命名：`1.jpg`, `2.jpg`, `3.jpg`...
   - 详情图使用非数字命名：`detail.jpg`, `parameter.jpg`, `specs.jpg`

2. **文件夹命名 / Folder Naming:**
   - 保持原有中文 + 英文格式
   - 不要修改文件夹名称

3. **编码 / Encoding:**
   - JSON 文件使用 UTF-8 编码
   - 包含中文字符时确保正确编码

---

## 已完成 / Completed

✅ 产品类别选择页：`products.html`
✅ 类别 1 列表页：`products-category-1.html`
✅ 类别 2 列表页：`products-category-2.html`
✅ 类别 3 列表页：`products-category-3.html`
✅ 产品详情页：`product-detail.html`
✅ JavaScript 加载脚本：`js/products-category-1.js`, `products-category-2.js`, `products-category-3.js`
✅ 产品详情脚本：`js/product-detail.js`

## 待完成 / To Do

⏳ 生成 3 个 `product-list.json` 文件（使用 PowerShell 脚本）
⏳ 测试产品列表页
⏳ 测试产品详情页
⏳ 部署到 GitHub/Vercel
