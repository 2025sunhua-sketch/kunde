$baseUrl = "https://kunde-electric.pages.dev "  
$outputPath = "C:\Users\ADMIN\.jvs\.openclaw\workspace\kunde-website\sitemap.xml"  
  
# 基础页面  
$pages = @(  
    @{ loc = ""; changefreq = "weekly"; priority = "1.0" },  
    @{ loc = "products.html"; changefreq = "weekly"; priority = "0.9" },  
    @{ loc = "about.html"; changefreq = "monthly"; priority = "0.7" },  
    @{ loc = "production.html"; changefreq = "monthly"; priority = "0.7" },  
    @{ loc = "contact.html"; changefreq = "monthly"; priority = "0.7" }  
)  
  
# 分类页面  
$categories = @(  
    "cable-lugs-and-connectors",  
    "insulated-terminals",  
    "cable-clamps"  
)  
  
# 产品页面（读取目录）  
$products = Get-ChildItem "C:\Users\ADMIN\.jvs\.openclaw\workspace\kunde-website\product" -Directory | Select-Object -ExpandProperty Name  
  
# 生成 XML  
$xml = '<?xml version="1.0" encoding="UTF-8"?>'  
$xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9 ">'  
  
# 添加基础页面  
foreach ($page in $pages) {  
    $today = Get-Date -Format "yyyy-MM-dd"  
    $xml += '<url>'  
    $xml += "<loc>$baseUrl/$($page.loc)</loc>"  
    $xml += "<lastmod>$today</lastmod>"  
    $xml += "<changefreq>$($page.changefreq)</changefreq>"  
    $xml += "<priority>$($page.priority)</priority>"  
    $xml += '</url>'  
}  
  
# 添加分类页面  
foreach ($cat in $categories) {  
    $today = Get-Date -Format "yyyy-MM-dd"  
    $xml += '<url>'  
    $xml += "<loc>$baseUrl/category/$cat</loc>"  
    $xml += "<lastmod>$today</lastmod>"  
    $xml += "<changefreq>weekly</changefreq>"  
    $xml += "<priority>0.8</priority>"  
    $xml += '</url>'  
}  
  
# 添加产品页面（前 100 个，避免文件过大）  
foreach ($prod in $products | Select-Object -First 100) {  
    $today = Get-Date -Format "yyyy-MM-dd"  
    $xml += '<url>'  
    $xml += "<loc>$baseUrl/product/$prod</loc>"  
    $xml += "<lastmod>$today</lastmod>"  
    $xml += "<changefreq>monthly</changefreq>"  
    $xml += "<priority>0.6</priority>"  
    $xml += '</url>'  
}  
  
$xml += '</urlset>'  
  
# 保存文件  
$xml | Out-File -FilePath $outputPath -Encoding UTF8  
  
Write-Host "Sitemap 已更新！"  
Write-Host "包含："  
Write-Host "  - 基础页面：$($pages.Count) 个"  
Write-Host "  - 分类页面：$($categories.Count) 个"  
Write-Host "  - 产品页面：$($products.Count) 个（已限制前 100 个）"  
