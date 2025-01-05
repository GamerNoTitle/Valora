# 计算文件的行数
function Get-LineCount {
    param (
        [string]$filePath
    )
    try {
        $lineCount = (Get-Content $filePath | Measure-Object -Line).Lines
        return $lineCount
    } catch {
        Write-Warning "无法读取文件: $filePath"
        return 0
    }
}

# 初始化计数器
$totalLineCount = 0
$cAndHLineCount = 0
$pyLineCount = 0
$htmlLineCount = 0
$readmeLineCount = 0
$ps1LineCount = 0


#  .py 文件行数
$pyFiles = Get-ChildItem -Recurse -Filter "*.py"
foreach ($file in $pyFiles) {
    $pyLineCount += Get-LineCount -filePath $file.FullName
}

# 计算 templates 目录及子目录下的 .html 文件行数
$templatesDir = "templates"
if (Test-Path $templatesDir) {
    $htmlFiles = Get-ChildItem -Path $templatesDir -Recurse -Filter "*.html"
    foreach ($file in $htmlFiles) {
        $htmlLineCount += Get-LineCount -filePath $file.FullName
    }
}

# 计算当前目录下的 README.md 文件行数
$readmeFile = "README.md"
if (Test-Path $readmeFile) {
    $readmeLineCount = Get-LineCount -filePath $readmeFile
}

# 计算当前目录下的 .ps1 文件行数
$ps1Files = Get-ChildItem -Path . -Filter "*.ps1" | Where-Object { $_.PSIsContainer -eq $false }
foreach ($file in $ps1Files) {
    $ps1LineCount += Get-LineCount -filePath $file.FullName
}

# 计算总行数
$totalLineCount = $cAndHLineCount + $pyLineCount + $htmlLineCount + $readmeLineCount + $ps1LineCount

# 输出结果
Write-Host "======== 文件行数统计 ========"
Write-Host "ui 目录下的 .py 文件总行数: $pyLineCount"
Write-Host "ui/templates 目录下的 .html 文件总行数: $htmlLineCount"
Write-Host "当前目录下的 README.md 文件总行数: $readmeLineCount"
Write-Host "当前目录下的 .ps1 文件总行数: $ps1LineCount"
Write-Host "总行数: $totalLineCount"
