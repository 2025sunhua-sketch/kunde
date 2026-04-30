# 产品一键更新脚本 - 最快版本
# One-Click Product Update - Fastest Version

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "产品一键更新工具" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "说明：直接覆盖产品文件夹后运行此脚本" -ForegroundColor Gray
Write-Host ""

$basePath = "C:\Users\ADMIN\.jvs\.openclaw\workspace\kunde-website\images\products\product"

# 类别配置
$categoryFolders = @(
    @{ Path = "1Cable Lugs and Connectors"; Name = "Cable Lugs and Connectors" },
    @{ Path = "02-2insulated-terminals"; Name = "Insulated Terminals" },
    @{ Path = "03-3cable-clamps"; Name = "Cable Clamps" }
)

# 更新所有类别
foreach ($category in $categoryFolders) {
    Write-Host "`n[$($category.Name)]" -ForegroundColor Cyan
    Write-Host "  扫描文件夹..." -ForegroundColor Gray
    
    $categoryPath = Join-Path $basePath $category.Path
    
    if (-not (Test-Path $categoryPath)) {
        Write-Host "  ⚠ 文件夹不存在，跳过" -ForegroundColor Yellow
        continue
    }
    
    # 扫描产品文件夹
    $productFolders = Get-ChildItem -Path $categoryPath -Directory | Where-Object { $_.Name -match '^\d+' }
    Write-Host "  找到 $($productFolders.Count) 个产品" -ForegroundColor Green
    
    # 生成产品数据
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
        $name = ($nameParts | Where-Object { $_ -match '^[A-Za-z0-9\(\)]' }) -join ' '
        if (-not $name) { $name = $folder.Name }
        
        # 优化产品名称格式
        $name = $name -replace '\s+', ' '
        $name = $name.Trim()
        
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
    
    Write-Host "  ✓ 已更新 product-list.json" -ForegroundColor Green
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "产品数据更新完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan

# 询问是否立即推送
Write-Host "`n是否立即推送到 GitHub？" -ForegroundColor Yellow
Write-Host "  Y - 是，立即推送" -ForegroundColor Gray
Write-Host "  N - 否，稍后手动推送" -ForegroundColor Gray

$choice = Read-Host "`n输入 Y 或 N"

if ($choice -eq 'Y' -or $choice -eq 'y') {
    Write-Host "`n开始推送..." -ForegroundColor Cyan
    
    $commitMessage = Read-Host "输入更新说明 (默认：Update products)"
    if (-not $commitMessage) { $commitMessage = "Update products" }
    
    # 执行 Git 命令
    Set-Location "C:\Users\ADMIN\.jvs\.openclaw\workspace\kunde-website"
    
    Write-Host "  git add ..." -ForegroundColor Gray
    git add . | Out-Null
    
    Write-Host "  git commit ..." -ForegroundColor Gray
    git commit -m $commitMessage | Out-Null
    
    Write-Host "  git push ..." -ForegroundColor Gray
    git push origin main | Out-Null
    
    Write-Host "`n✓ 推送成功！" -ForegroundColor Green
    Write-Host "  Cloudflare 将自动部署（1-2 分钟）" -ForegroundColor Gray
} else {
    Write-Host "`n稍后请手动推送：" -ForegroundColor Yellow
    Write-Host "  cd C:\Users\ADMIN\.jvs\.openclaw\workspace\kunde-website" -ForegroundColor Gray
    Write-Host "  git add ." -ForegroundColor Gray
    Write-Host "  git commit -m `"Update products`"" -ForegroundColor Gray
    Write-Host "  git push origin main" -ForegroundColor Gray
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan

Read-Host "`n按回车键退出"
