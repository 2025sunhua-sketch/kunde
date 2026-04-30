# 产品批量更新工具
# Product Batch Update Tool

param(
    [string]$CategoryPath,
    [string]$SourcePath
)

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "产品批量更新工具" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# 配置
$categoryFolders = @(
    @{ Path = "1Cable Lugs and Connectors"; Name = "Cable Lugs" },
    @{ Path = "02-2insulated-terminals"; Name = "Insulated Terminals" },
    @{ Path = "03-3cable-clamps"; Name = "Cable Clamps" }
)

$basePath = "C:\Users\ADMIN\.jvs\.openclaw\workspace\kunde-website\images\products\product"

Write-Host "`n请选择要更新的类别：" -ForegroundColor Yellow
for ($i = 0; $i -lt $categoryFolders.Count; $i++) {
    Write-Host "  $($i+1). $($categoryFolders[$i].Name)" -ForegroundColor Gray
}

$choice = Read-Host "`n输入序号 (1-$($categoryFolders.Count))"
$selectedCategory = $categoryFolders[$choice-1]

Write-Host "`n选定类别：$($selectedCategory.Name)" -ForegroundColor Green
Write-Host "路径：$($selectedCategory.Path)" -ForegroundColor Gray

# 扫描产品文件夹
$categoryPath = Join-Path $basePath $selectedCategory.Path
Write-Host "`n扫描产品文件夹..." -ForegroundColor Cyan

$productFolders = Get-ChildItem -Path $categoryPath -Directory | Where-Object { $_.Name -match '^\d+' }
Write-Host "  找到 $($productFolders.Count) 个产品" -ForegroundColor Green

# 生成 product-list.json
Write-Host "`n生成 product-list.json..." -ForegroundColor Cyan

$products = @()

foreach ($folder in $productFolders) {
    $images = @()
    $detailImage = $null
    
    $files = Get-ChildItem -Path $folder.FullName -File -Include *.jpg,*.jpeg,*.png
    
    foreach ($file in $files) {
        if ($file.Name -match '^\d+\.') {
            $images += $file.Name
        } else {
            $detailImage = $file.Name
        }
    }
    
    # 排序图片
    $images = $images | Sort-Object { if ($_ -match '^(\d+)') { [int]$matches[1] } else { 9999 } }
    
    # 提取产品名称
    $nameParts = $folder.Name -split '-'
    $name = ($nameParts | Where-Object { $_ -match '^[A-Za-z0-9]' }) -join ' '
    if (-not $name) { $name = $folder.Name }
    
    $products += [PSCustomObject]@{
        folder = $folder.Name
        name = $name
        images = $images
        detailImage = $detailImage
        imageCount = $images.Count
    }
}

# 保存 JSON
$jsonPath = Join-Path $categoryPath "product-list.json"
$products | ConvertTo-Json -Depth 10 | Out-File -FilePath $jsonPath -Encoding UTF8

Write-Host "  ✓ 已生成 product-list.json" -ForegroundColor Green
Write-Host "  产品数量：$($products.Count)" -ForegroundColor Gray

# 提示推送
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "更新完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "`n下一步：推送到 GitHub" -ForegroundColor Yellow
Write-Host "  cd C:\Users\ADMIN\.jvs\.openclaw\workspace\kunde-website" -ForegroundColor Gray
Write-Host "  git add ." -ForegroundColor Gray
Write-Host "  git commit -m `"Update products: $($selectedCategory.Name)`"" -ForegroundColor Gray
Write-Host "  git push origin main" -ForegroundColor Gray

Read-Host "`n按回车键退出"
