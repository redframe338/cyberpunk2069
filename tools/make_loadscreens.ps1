Add-Type -AssemblyName System.Drawing

$root    = "C:\Users\victo\cyberpunk mod"
$srcDir  = Join-Path $root "assets\loadingscreens"
$outDir  = Join-Path $root "mod\gfx\loadingscreens"
$gameDir = "E:\SteamLibrary\steamapps\common\Hearts of Iron IV\gfx\loadingscreens"

if (-not (Test-Path $outDir)) { New-Item -ItemType Directory -Force $outDir | Out-Null }

$bigHeader   = [byte[]]([System.IO.File]::ReadAllBytes("$gameDir\load_1.dds")[0..127])
$smallHeader = [byte[]]([System.IO.File]::ReadAllBytes("$gameDir\load_1_small.dds")[0..127])

function Write-DdsFromBitmap([System.Drawing.Bitmap]$src, [int]$tw, [int]$th, [byte[]]$hdr, [string]$path) {
    $dst = [System.Drawing.Bitmap]::new($tw, $th, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
    $g = [System.Drawing.Graphics]::FromImage($dst)
    $g.InterpolationMode = 'HighQualityBicubic'
    $g.PixelOffsetMode   = 'HighQuality'
    $g.DrawImage($src, 0, 0, $tw, $th)
    $g.Dispose()

    $pixels = New-Object byte[] ($tw * $th * 4)
    $idx = 0
    for ($y = 0; $y -lt $th; $y++) {
        for ($x = 0; $x -lt $tw; $x++) {
            $c = $dst.GetPixel($x, $y)
            $pixels[$idx++] = $c.B
            $pixels[$idx++] = $c.G
            $pixels[$idx++] = $c.R
            $pixels[$idx++] = $c.A
        }
    }
    $dst.Dispose()
    [System.IO.File]::WriteAllBytes($path, $hdr + $pixels)
}

$files = Get-ChildItem $srcDir -Filter "*.png" -ErrorAction SilentlyContinue
$files += Get-ChildItem $srcDir -Filter "*.jpg" -ErrorAction SilentlyContinue
$files += Get-ChildItem $srcDir -Filter "*.bmp" -ErrorAction SilentlyContinue
$files = $files | Sort-Object Name

if ($files.Count -eq 0) {
    Write-Host "ERROR: No images found in $srcDir"
    Write-Host "Save the loading screen images there as 1.png, 2.png, etc."
    exit 1
}

Write-Host "Found $($files.Count) source images in $srcDir"

$i = 1
foreach ($f in $files) {
    Write-Host "  [$i] $($f.Name)..."
    $bytes = [System.IO.File]::ReadAllBytes($f.FullName)
    $ms = New-Object System.IO.MemoryStream (,$bytes)
    $img = [System.Drawing.Image]::FromStream($ms)

    Write-DdsFromBitmap $img 1920 1440 $bigHeader   (Join-Path $outDir "load_$i.dds")
    Write-DdsFromBitmap $img 192  144  $smallHeader  (Join-Path $outDir "load_${i}_small.dds")
    Write-Host "      -> load_$i.dds (1920x1440) + load_${i}_small.dds (192x144)"

    $img.Dispose(); $ms.Dispose()
    $i++
}

Write-Host "`nInstalled $($files.Count) loading screens to $outDir"
Write-Host "The replace_path directive in descriptor.mod ensures ONLY these appear."
