# 测试PowerShell构建脚本
Write-Host "Testing PowerShell build script..."

# 获取所有目录
$directories = Get-ChildItem -Directory
Write-Host "Found directories: $($directories.Name -join ', ')"

foreach ($dir in $directories) {
    $pyFiles = Get-ChildItem -Path $dir.FullName -Filter "*.py"
    
    if ($pyFiles.Count -gt 0) {
        Write-Host "=== Found Python files in $($dir.Name) ==="
        Write-Host "Python files: $($pyFiles.Name -join ', ')"
        
        # 检查requirements.txt
        if (Test-Path "$($dir.FullName)/requirements.txt") {
            Write-Host "Found requirements.txt"
        } else {
            Write-Host "No requirements.txt found"
        }
    }
}

Write-Host "Test completed successfully!"