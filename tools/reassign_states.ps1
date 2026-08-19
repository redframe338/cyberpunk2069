$modStates = "C:\Users\victo\cyberpunk mod\mod\history\states"

function Set-StateOwner([string]$file, [string]$newTag, [string]$comment) {
    $path = Join-Path $modStates $file
    if (-not (Test-Path $path)) { Write-Warning "Not found: $path"; return }
    $content = Get-Content $path -Raw
    $content = $content -replace '(?m)(owner\s*=\s*)\w+', "`$1$newTag"
    $content = $content -replace '(?m)(add_core_of\s*=\s*)\w+', "`$1$newTag"
    $content = $content -replace '^#.*\r?\n', ''
    $content = "# $comment`n" + $content
    Set-Content -Path $path -Value $content -Encoding utf8 -NoNewline
    Write-Host "  $file -> $newTag"
}

Write-Host "=== IRAN NORTH -> NIR (People's Republic of Iran) ==="
$northIran = @(
    "266-Persia.txt", "419-Azerbaijan.txt", "1000-East Azerbaijan.txt",
    "420-Gilan.txt", "417-Golestan.txt", "1001-Kurdistan.txt",
    "421-Kurdistan.txt", "416-Razavi Khorasan.txt", "1004-North Khorasan.txt",
    "418-Semnan.txt"
)
foreach ($f in $northIran) { Set-StateOwner $f "NIR" "Cyberpunk: People's Republic of Iran (North Iran)" }

Write-Host "`n=== IRAN SOUTH -> SIR (Republic of Iran) ==="
$southIran = @(
    "411-Hormozgan.txt", "412-Fars.txt", "413-Khuzestan.txt",
    "414-Kerman.txt", "410-Sistan.txt", "1002-Yazd.txt", "1003-South Khorasan.txt"
)
foreach ($f in $southIran) { Set-StateOwner $f "SIR" "Cyberpunk: Republic of Iran (South Iran)" }

Write-Host "`n=== SWITZERLAND -> SWI ==="
$swiss = @("3-Swiss Plateau.txt", "151-Eastern Swiss Alps.txt", "847-Western Swiss Alps.txt")
foreach ($f in $swiss) { Set-StateOwner $f "SWI" "Cyberpunk: Switzerland (independent, outside EEC)" }

Write-Host "`nDone."
