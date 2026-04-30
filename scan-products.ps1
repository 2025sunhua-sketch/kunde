# Quick Product Update Script - Simple Version

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Product Update Scanner" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$basePath = "C:\Users\ADMIN\.jvs\.openclaw\workspace\kunde-website\images\products\product"

$categoryFolders = @(
    "1Cable Lugs and Connectors",
    "02-2insulated-terminals",
    "03-3cable-clamps"
)

foreach ($categoryPath in $categoryFolders) {
    Write-Host "`nProcessing: $categoryPath" -ForegroundColor Cyan
    
    $fullPath = Join-Path $basePath $categoryPath
    
    if (-not (Test-Path $fullPath)) {
        Write-Host "  Folder not found, skipping" -ForegroundColor Yellow
        continue
    }
    
    $productFolders = Get-ChildItem -Path $fullPath -Directory | Where-Object { $_.Name -match '^\d+' }
    Write-Host "  Found $($productFolders.Count) products" -ForegroundColor Green
    
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
        
        $images = $images | Sort-Object { if ($_ -match '^(\d+)') { [int]$matches[1] } else { 9999 } }
        
        $nameParts = $folder.Name -split '-'
        $name = ($nameParts | Where-Object { $_ -match '^[A-Za-z0-9\(\)]' }) -join ' '
        if (-not $name) { $name = $folder.Name }
        
        $products += [PSCustomObject]@{
            folder = $folder.Name
            name = $name
            images = $images
            detailImage = $detailImage
            imageCount = $images.Count
        }
    }
    
    $jsonPath = Join-Path $fullPath "product-list.json"
    $products | ConvertTo-Json -Depth 10 | Out-File -FilePath $jsonPath -Encoding UTF8
    
    Write-Host "  Updated product-list.json" -ForegroundColor Green
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Update Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "`nPush to GitHub:" -ForegroundColor Yellow
Write-Host "  git add ." -ForegroundColor Gray
Write-Host "  git commit -m 'Update products'" -ForegroundColor Gray
Write-Host "  git push origin main" -ForegroundColor Gray
