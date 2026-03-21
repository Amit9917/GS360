$mainPath = "e:\git hub\gs360\GS360_Product_Journey.md"
$addPath = "C:\tmp\gs360_smart_features.md"

$main = [System.IO.File]::ReadAllText($mainPath, [System.Text.Encoding]::UTF8)
$add = [System.IO.File]::ReadAllText($addPath, [System.Text.Encoding]::UTF8)

$combined = $main + $add

$utf8 = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($mainPath, $combined, $utf8)

$lines = ($combined -split "`n").Count
Write-Host "Lines: $lines"
