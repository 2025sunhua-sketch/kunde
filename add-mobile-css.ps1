# Add mobile-optimized.css to all HTML files
# 在所有 HTML 文件中添加移动端优化 CSS 引用

$htmlFiles = Get-ChildItem -Path "." -Filter "*.html" -File

foreach ($file in $htmlFiles) {
    Write-Host "Processing: $($file.Name)" -ForegroundColor Cyan
    
    $content = Get-Content $file.FullName -Raw -Encoding UTF8
    
    # Check if already has mobile-optimized.css
    if ($content -like "*mobile-optimized.css*") {
        Write-Host "  ✓ Already has mobile CSS, skipping" -ForegroundColor Gray
        continue
    }
    
    # Add mobile CSS link before </head>
    $mobileCssLink = @"
  
  <!-- Mobile Optimization -->
  <link rel="stylesheet" href="css/mobile-optimized.css">
"@
    
    $newContent = $content -replace '</head>', "$mobileCssLink`n</head>"
    
    # Save file
    Set-Content -Path $file.FullName -Value $newContent -Encoding UTF8 -NoNewline
    
    Write-Host "  ✓ Added mobile CSS" -ForegroundColor Green
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "DONE! Updated $($htmlFiles.Count) HTML files" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
