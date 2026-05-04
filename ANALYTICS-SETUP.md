# 📊 网站分析工具配置指南

---

## 🎯 推荐方案：百度统计

**最适合国内使用的网站分析工具**

---

## 📝 第 1 步：注册百度统计

### 访问官网
```
https://tongji.baidu.com/
```

### 注册/登录
- 使用百度账号登录
- 没有账号先注册（免费）

### 添加网站
1. 登录后点击 **"添加网站"**
2. 填写网站信息：
   ```
   网站域名：kunde-electric.pages.dev（或你的自定义域名）
   网站名称：KUNDE ELECTRIC 官网
   网站类别：工业/制造业
   ```
3. 点击 **"确定"**

### 获取统计代码
1. 添加成功后，进入管理页面
2. 找到 **"代码获取"** 或 **"安装代码"**
3. 复制统计代码

**代码格式类似：**
```html
<script>
var _hmt = _hmt || [];
(function() {
  var hm = document.createElement("script");
  hm.src = "https://hm.baidu.com/hm.js?xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx";
  var s = document.getElementsByTagName("script")[0]; 
  s.parentNode.insertBefore(hm, s);
})();
</script>
```

**记住你的统计 ID**（hm.js? 后面的字符串）

---

## 🔧 第 2 步：集成到网站

### 方法 A：修改 analytics.js（推荐）

**1. 打开文件：**
```
js/analytics.js
```

**2. 替换统计 ID：**
```javascript
// 原代码：
hm.src = "https://hm.baidu.com/hm.js?YOUR_BAIDU_TONGJI_ID";

// 替换为你的统计 ID：
hm.src = "https://hm.baidu.com/hm.js?xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx";
```

**3. 保存文件**

---

### 方法 B：直接添加到 HTML

**在所有 HTML 页面的 `<head>` 标签内添加：**

```html
<head>
  <!-- 其他代码... -->
  
  <!-- 百度统计 -->
  <script>
  var _hmt = _hmt || [];
  (function() {
    var hm = document.createElement("script");
    hm.src = "https://hm.baidu.com/hm.js?你的统计 ID";
    var s = document.getElementsByTagName("script")[0]; 
    s.parentNode.insertBefore(hm, s);
  })();
  </script>
  
  <!-- 其他代码... -->
</head>
```

**需要添加的页面：**
- ✅ index.html
- ✅ products.html
- ✅ products-category-1.html
- ✅ products-category-2.html
- ✅ products-category-3.html
- ✅ product-detail.html
- ✅ about.html
- ✅ contact.html
- ✅ production.html

---

## 🚀 第 3 步：部署更新

### 使用 Wrangler 部署

```powershell
cd C:\Users\ADMIN\.jvs\.openclaw\workspace\kunde-website

wrangler pages deploy . --project-name=你的项目名称
```

**等待部署完成（1-2 分钟）**

---

## 📊 第 4 步：查看数据

### 访问百度统计后台

```
https://tongji.baidu.com/
```

### 可以查看的数据

| 数据类型 | 说明 |
|---------|------|
| **实时访客** | 当前在线人数 |
| **来源分析** | 用户从哪里来（Google、百度、直接访问等） |
| **页面分析** | 哪些页面最受欢迎 |
| **访客分析** | 用户地区、设备、浏览器等 |
| **转化跟踪** | 询盘表单提交等 |

---

## 📈 其他分析工具（可选）

### 1. 友盟+
```
官网：https://www.umeng.com/
特点：阿里巴巴旗下，功能丰富
```

### 2. 51.la
```
官网：https://www.51.la/
特点：简单好用，数据实时
```

### 3. Google Analytics（国际版）
```
官网：https://analytics.google.com/
特点：功能最强大，但国内访问慢
```

---

## ⚠️ 注意事项

1. **只选一个**：不要同时添加多个统计工具，会影响网站速度
2. **统计 ID 保密**：不要公开你的统计 ID
3. **数据延迟**：数据通常有 15-30 分钟延迟
4. **隐私合规**：确保符合当地数据隐私法规

---

## 🎯 推荐配置

**对于 B2B 企业官网，重点关注：**

| 指标 | 说明 | 目标值 |
|------|------|--------|
| 日访问量 | 每天独立访客 | 100+ |
| 平均停留时间 | 用户在网站停留多久 | >2 分钟 |
| 跳出率 | 只看一页就离开的比例 | <50% |
| 询盘转化率 | 访问 → 询盘的比例 | 3-5% |
| 热门页面 | 哪些产品最受欢迎 | - |

---

## 💡 高级用法

### 1. 设置转化目标

**跟踪询盘表单提交：**
```javascript
// 在联系表单提交成功后添加
_hmt.push(['_trackEvent', 'contact', 'submit', 'Inquiry Form']);
```

### 2. 跟踪产品详情页

**自动跟踪产品浏览：**
```javascript
// product-detail.html 中添加
_hmt.push(['_trackEvent', 'product', 'view', '产品名称']);
```

### 3. 设置访问深度

**查看用户平均访问几个页面**
```
百度统计后台 → 访客分析 → 访问深度
```

---

## 📞 需要帮助？

**百度统计官方文档：**
```
https://tongji.baidu.com/web/help/
```

**常见问题：**
- 代码安装后看不到数据？→ 等待 15-30 分钟
- 数据不准确？→ 检查代码是否正确安装
- 如何过滤内部访问？→ 设置 IP 排除

---

**配置完成后，就可以实时监控网站流量了！** 📊
