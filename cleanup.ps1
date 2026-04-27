# Cleanup temporary files before deploying to GitHub

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Cleaning up temporary files..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$filesToDelete = @(
    # PowerShell scripts
    "fix-all-categories.ps1",
    "fix-category-2.ps1",
    "fix-category-2-sorting.ps1",
    "fix-product-8.ps1",
    "fix-sorting.ps1",
    "generate-all-products.ps1",
    "generate-product-data.ps1",
    "generate-product-lists.ps1",
    "generate-products.ps1",
    "generate-products.py",
    "organize-images.ps1",
    "regenerate-all-json.ps1",
    "regenerate-json.ps1",
    "rename-folders.ps1",
    
    # Old product detail pages (keep only product-detail.html)
    "product-cable-clamps.html",
    "product-dtl-1-bimetal-cable-lugs.html",
    "product-dtl-1-cable-lugs.html",
    "product-insulated-terminals.html",
    
    # Temporary data files
    "products-data.json"
)

$deletedCount = 0

foreach ($file in $filesToDelete) {
    $filePath = Join-Path $PSScriptRoot $file
    if (Test-Path $filePath) {
        Remove-Item -Path $filePath -Force
        Write-Host "✓ Deleted: $file" -ForegroundColor Green
        $deletedCount++
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Cleanup complete!" -ForegroundColor Green
Write-Host "Deleted $deletedCount files" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Ready files for GitHub:" -ForegroundColor Cyan
Write-Host "  - HTML files (11 pages)" -ForegroundColor Gray
Write-Host "  - CSS/JS files" -ForegroundColor Gray
Write-Host "  - Images" -ForegroundColor Gray
Write-Host "  - product-list.json files (3)" -ForegroundColor Gray
Write-Host "  - README.md" -ForegroundColor Gray
Write-Host "  - vercel.json" -ForegroundColor Gray
Write-Host ""
Write-Host "Ready to deploy to GitHub!" -ForegroundColor Green
