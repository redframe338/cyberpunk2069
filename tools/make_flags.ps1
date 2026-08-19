# Converts source flag images (any PNG/JPG/BMP) into HOI4 .tga flags at the
# three required sizes and installs them into the mod's gfx/flags folders.
#
# Place source images in  ..\assets\  named (any extension):
#   nusa.*   -> NUS.tga
#   ussr.*   -> USR.tga
# Then run:  & ".\tools\make_flags.ps1"

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing

$root   = Split-Path -Parent $PSScriptRoot   # repo root (…\cyberpunk mod)
$assets = Join-Path $root 'assets'
$flags  = Join-Path $root 'mod\gfx\flags'

# tag -> source basename (without extension) to look for in assets\
$map = @{ NUS = 'nusa'; USR = 'ussr' }
$sizes = @{ ''='82x52'; 'medium'='41x26'; 'small'='10x7' }  # folder -> WxH

function Save-Tga($bmp, $w, $h, $path) {
  # high-quality resize into 24bpp
  $dst = New-Object System.Drawing.Bitmap $w, $h, ([System.Drawing.Imaging.PixelFormat]::Format24bppRgb)
  $g = [System.Drawing.Graphics]::FromImage($dst)
  $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
  $g.PixelOffsetMode   = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
  $g.DrawImage($bmp, 0, 0, $w, $h)
  $g.Dispose()
  # TGA header: uncompressed true-color, 24bpp, top-left origin
  $hdr = New-Object byte[] 18
  $hdr[2] = 2
  $hdr[12] = $w -band 0xFF; $hdr[13] = ($w -shr 8) -band 0xFF
  $hdr[14] = $h -band 0xFF; $hdr[15] = ($h -shr 8) -band 0xFF
  $hdr[16] = 24
  # HOI4 expects bottom-origin TGA pixel storage, matching vanilla flags.
  $hdr[17] = 0
  $data = New-Object byte[] ($w * $h * 3)
  $i = 0
  for ($y = $h - 1; $y -ge 0; $y--) {
    for ($x = 0; $x -lt $w; $x++) {
      $c = $dst.GetPixel($x, $y)
      $data[$i++] = $c.B; $data[$i++] = $c.G; $data[$i++] = $c.R
    }
  }
  $dst.Dispose()
  [System.IO.File]::WriteAllBytes($path, ($hdr + $data))
  "  wrote $path ($w x $h)"
}

foreach ($tag in $map.Keys) {
  $base = $map[$tag]
  $src = Get-ChildItem $assets -Filter "$base.*" -ErrorAction SilentlyContinue |
         Where-Object { $_.Extension -match '\.(png|jpg|jpeg|bmp|gif|tga)$' } | Select-Object -First 1
  if (-not $src) { Write-Warning "No source image '$base.*' found in $assets — skipping $tag"; continue }
  "== $tag  <-  $($src.Name) =="
  $bytes = [System.IO.File]::ReadAllBytes($src.FullName)
  $ms = New-Object System.IO.MemoryStream (,$bytes)
  $img = [System.Drawing.Image]::FromStream($ms)
  foreach ($folder in $sizes.Keys) {
    $wh = $sizes[$folder] -split 'x'
    $outDir = if ($folder) { Join-Path $flags $folder } else { $flags }
    if (-not (Test-Path $outDir)) { New-Item -ItemType Directory -Force $outDir | Out-Null }
    Save-Tga $img ([int]$wh[0]) ([int]$wh[1]) (Join-Path $outDir "$tag.tga")
  }
  $img.Dispose(); $ms.Dispose()
}
"done."
