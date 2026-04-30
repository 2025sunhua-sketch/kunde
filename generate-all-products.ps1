# Generate product-list.json for all 3 categories

$basePath = "C:\Users\ADMIN\.jvs\.openclaw\workspace\kunde-website\images\products\product"

$categoryFolders = @(
    "1 Cable Lugs and Connectors",
    "2 Insulated Terminals",
    "3 Cable Clamps"
)

foreach ($categoryPath in $categoryFolders) {
    Write-Host "`nProcessing: $categoryPath" -ForegroundColor Cyan
    
    $fullPath = Join-Path $basePath $categoryPath
    
    if (-not (Test-Path $fullPath)) {
        Write-Host "  Folder not found!" -ForegroundColor Red
        continue
    }
    
    $productFolders = Get-ChildItem -Path $fullPath -Directory | Sort-Object Name
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
        
        $name = $folder.Name
        
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
    
    Write-Host "  Generated product-list.json with $($products.Count) products" -ForegroundColor Green
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "All product lists updated!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
