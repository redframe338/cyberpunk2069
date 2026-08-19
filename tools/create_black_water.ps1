Add-Type -AssemblyName System.Drawing

$root = "C:\Users\victo\cyberpunk mod"
$game = "E:\SteamLibrary\steamapps\common\Hearts of Iron IV"

function Make-BlackTga([int]$w, [int]$h, [string]$path) {
    $dir = Split-Path $path
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force $dir | Out-Null }
    $hdr = New-Object byte[] 18
    $hdr[2] = 2
    $hdr[12] = $w -band 0xFF; $hdr[13] = ($w -shr 8) -band 0xFF
    $hdr[14] = $h -band 0xFF; $hdr[15] = ($h -shr 8) -band 0xFF
    $hdr[16] = 24; $hdr[17] = 0x20
    $data = New-Object byte[] ($w * $h * 3)
    [System.IO.File]::WriteAllBytes($path, $hdr + $data)
    Write-Host "  wrote $path ($w x $h)"
}

function Make-BlackDds([string]$srcPath, [string]$dstPath) {
    $dir = Split-Path $dstPath
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force $dir | Out-Null }
    $src = [System.IO.File]::ReadAllBytes($srcPath)
    for ($i = 128; $i -lt $src.Length; $i++) { $src[$i] = 0 }
    [System.IO.File]::WriteAllBytes($dstPath, $src)
    Write-Host "  wrote $dstPath (zeroed pixel data from vanilla, $($src.Length) bytes)"
}

Write-Host "=== Water color correction TGAs ==="
$worldDir = Join-Path $root "mod\gfx\world"
Make-BlackTga 256 16 (Join-Path $worldDir "colorcorrection_water.tga")
Make-BlackTga 256 16 (Join-Path $worldDir "colorcorrection_water_night.tga")

Write-Host "`n=== Water colormap DDS files ==="
$terrainDir = Join-Path $root "mod\map\terrain"
foreach ($n in @('colormap_water_0.dds', 'colormap_water_1.dds', 'colormap_water_2.dds')) {
    $srcFile = Join-Path $game "map\terrain\$n"
    $dstFile = Join-Path $terrainDir $n
    if (Test-Path $srcFile) {
        Make-BlackDds $srcFile $dstFile
    } else {
        Write-Warning "Vanilla file not found: $srcFile"
    }
}

Write-Host "`n=== Reflection cubemap DDS ==="
$reflSrc = Join-Path $game "map\terrain\reflection.dds"
$reflDst = Join-Path $terrainDir "reflection.dds"
if (Test-Path $reflSrc) {
    Make-BlackDds $reflSrc $reflDst
} else {
    Write-Warning "Vanilla file not found: $reflSrc"
}

Write-Host "`nDone. All water textures replaced with black."
