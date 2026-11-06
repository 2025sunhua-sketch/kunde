/**
 * scripts/gen-sitemap.mjs — 从仓库真实文件生成 sitemap.xml。
 *
 * URL 形态规则（与 Cloudflare Pages 的实际服务形态对齐，保证 sitemap 里 0 条需要重定向）：
 *   目录型页面 → 带尾斜杠：/category/<slug>/、/product/product-XXXX/
 *   平铺页面   → 带 .html ：/about.html、/blog/<slug>.html（Semantic URLs 关闭后无跳转）
 *   站点首页   → 只用 /，绝不重复出现
 * lastmod 取文件真实 mtime，不再全站同一天。
 *
 *   node scripts/gen-sitemap.mjs             # 预览（打印到 stdout）
 *   node scripts/gen-sitemap.mjs --write     # 写入仓库根 sitemap.xml
 */
import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve(import.meta.dirname, '..');
const SITE = 'https://kdelec.com';
const WRITE = process.argv.includes('--write');

const pad = (n) => String(n).padStart(2, '0');
const lm = (p) => {
  const d = new Date(fs.statSync(p).mtime);
  return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate());
};

const urls = [];
const push = (loc, p, pr) => urls.push({ loc, lastmod: lm(p), pr });

const flat = ['index.html', 'about.html', 'products.html', 'contact.html', 'faq.html',
  'production.html', 'blog.html', 'privacy-policy.html', 'warranty-policy.html'];
for (const f of flat) {
  const p = path.join(ROOT, f);
  if (!fs.existsSync(p)) continue;
  push(SITE + (f === 'index.html' ? '/' : '/' + f), p, f === 'index.html' ? '1.0' : '0.8');
}

const blogDir = path.join(ROOT, 'blog');
if (fs.existsSync(blogDir)) {
  for (const f of fs.readdirSync(blogDir).filter((x) => /\.html$/i.test(x) && x !== 'article-template.html')) {
    push(SITE + '/blog/' + f, path.join(blogDir, f), '0.6');
  }
}

for (const dir of ['category', 'product']) {
  const base = path.join(ROOT, dir);
  if (!fs.existsSync(base)) continue;
  for (const d of fs.readdirSync(base)) {
    const p = path.join(base, d, 'index.html');
    if (!fs.existsSync(p)) continue;
    push(SITE + '/' + dir + '/' + d + '/', p, dir === 'product' ? '0.9' : '0.8');
  }
}

urls.sort((a, b) => a.loc.localeCompare(b.loc));
const xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
  + '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
  + urls.map((u) => '  <url><loc>' + u.loc + '</loc><lastmod>' + u.lastmod
    + '</lastmod><changefreq>monthly</changefreq><priority>' + u.pr + '</priority></url>').join('\n')
  + '\n</urlset>\n';

if (WRITE) fs.writeFileSync(path.join(ROOT, 'sitemap.xml'), xml);

const uniq = new Set(urls.map((u) => u.loc));
const home = urls.filter((u) => u.loc === SITE + '/').length;
const lastmods = new Set(urls.map((u) => u.lastmod)).size;
const badForm = urls.filter((u) => /\/(category|product)\/[^/]+$/.test(u.loc)).length;
console.error(`条数 ${urls.length} | 唯一 ${uniq.size} | 首页出现 ${home} 次 | lastmod 种类 ${lastmods} | 缺尾斜杠(会308) ${badForm}`);
process.stdout.write(xml);
