Add-Type -AssemblyName System.Drawing

$root      = "C:\Users\victo\cyberpunk mod"
$assetsDir = Join-Path $root 'assets'
$flagsDir  = Join-Path $root 'mod\gfx\flags'

if (-not (Test-Path $assetsDir)) { New-Item -ItemType Directory -Force $assetsDir | Out-Null }

function StarPoly([float]$cx, [float]$cy, [float]$outerR, [float]$innerR, [int]$n, [float]$rotDeg) {
    $pts = New-Object 'System.Drawing.PointF[]' ($n * 2)
    $rot = $rotDeg * [Math]::PI / 180.0
    for ($i = 0; $i -lt ($n * 2); $i++) {
        $ang = [Math]::PI * $i / $n - [Math]::PI / 2.0 + $rot
        $rd  = if ($i % 2 -eq 0) { $outerR } else { $innerR }
        $pts[$i] = [System.Drawing.PointF]::new(
            [float]($cx + $rd * [Math]::Cos($ang)),
            [float]($cy + $rd * [Math]::Sin($ang)))
    }
    return ,$pts
}

function Save-Tga([System.Drawing.Bitmap]$src, [int]$tw, [int]$th, [string]$path) {
    $dir = Split-Path $path
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force $dir | Out-Null }
    $dst = [System.Drawing.Bitmap]::new($tw, $th, [System.Drawing.Imaging.PixelFormat]::Format24bppRgb)
    $gx = [System.Drawing.Graphics]::FromImage($dst)
    $gx.InterpolationMode = 'HighQualityBicubic'
    $gx.PixelOffsetMode   = 'HighQuality'
    $gx.DrawImage($src, 0, 0, $tw, $th)
    $gx.Dispose()
    $hdr = New-Object byte[] 18
    $hdr[2]  = 2
    $hdr[12] = $tw -band 0xFF; $hdr[13] = ($tw -shr 8) -band 0xFF
    $hdr[14] = $th -band 0xFF; $hdr[15] = ($th -shr 8) -band 0xFF
    # HOI4 expects bottom-origin TGA pixel storage, matching vanilla flags.
    $hdr[16] = 24; $hdr[17] = 0
    $px  = New-Object byte[] ($tw * $th * 3)
    $idx = 0
    for ($y = $th - 1; $y -ge 0; $y--) {
        for ($x = 0; $x -lt $tw; $x++) {
            $c = $dst.GetPixel($x, $y)
            $px[$idx++] = $c.B; $px[$idx++] = $c.G; $px[$idx++] = $c.R
        }
    }
    $dst.Dispose()
    [System.IO.File]::WriteAllBytes($path, $hdr + $px)
}

function Install-Flags([System.Drawing.Bitmap]$bmp, [string]$tag) {
    $szs = @(
        @{ f = '';       w = 82; h = 52 },
        @{ f = 'medium'; w = 41; h = 26 },
        @{ f = 'small';  w = 10; h = 7  }
    )
    foreach ($s in $szs) {
        $d = if ($s.f) { Join-Path $flagsDir $s.f } else { $flagsDir }
        Save-Tga $bmp $s.w $s.h (Join-Path $d "$tag.tga")
        foreach ($ideo in @('neutrality','democratic','fascism','communism')) {
            Save-Tga $bmp $s.w $s.h (Join-Path $d "${tag}_$ideo.tga")
        }
    }
}

# ================================================================
#  NUSA FLAG
#  Red/white stripes, dark-blue chevron, large central star,
#  13 smaller stars in a circle
# ================================================================
Write-Host "Creating NUSA flag..."

$W = 820; $H = 520
$bmp = [System.Drawing.Bitmap]::new($W, $H, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
$g   = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = 'HighQuality'

$nusaRed   = [System.Drawing.Color]::FromArgb(178, 34, 52)
$nusaBlue  = [System.Drawing.Color]::FromArgb(44,  55, 100)
$nusaWhite = [System.Drawing.Color]::White

# 13 alternating stripes (red first and last)
$sh = [float]($H / 13.0)
for ($i = 0; $i -lt 13; $i++) {
    $c = if ($i % 2 -eq 0) { $nusaRed } else { $nusaWhite }
    $br = New-Object System.Drawing.SolidBrush $c
    $g.FillRectangle($br, 0.0, [float]($i * $sh), [float]$W, [float]($sh + 2))
    $br.Dispose()
}

# Blue chevron (triangle from left edge, apex at ~40% width)
$apex = [float]($W * 0.40)
$triPts = @(
    [System.Drawing.PointF]::new(0, 0),
    [System.Drawing.PointF]::new($apex, [float]($H / 2.0)),
    [System.Drawing.PointF]::new(0, [float]$H)
)
$br = New-Object System.Drawing.SolidBrush $nusaBlue
$g.FillPolygon($br, $triPts)
$br.Dispose()

# Clip subsequent drawing to the triangle region
$clipPath = New-Object System.Drawing.Drawing2D.GraphicsPath
$clipPath.AddPolygon($triPts)
$g.SetClip($clipPath)

$wb = New-Object System.Drawing.SolidBrush $nusaWhite

# Large central star
$scx = $apex * 0.42;  $scy = [float]($H / 2.0)
$bigR = $H * 0.14;    $bigIR = $bigR * 0.382
$pts = StarPoly $scx $scy $bigR $bigIR 5 0
$g.FillPolygon($wb, $pts)

# 13 smaller stars in a circle around the central star
$circR = $H * 0.25
$smR   = $H * 0.042;  $smIR = $smR * 0.382
for ($j = 0; $j -lt 13; $j++) {
    $a  = 2.0 * [Math]::PI * $j / 13.0 - [Math]::PI / 2.0
    $sx = [float]($scx + $circR * [Math]::Cos($a))
    $sy = [float]($scy + $circR * [Math]::Sin($a))
    $pts = StarPoly $sx $sy $smR $smIR 5 0
    $g.FillPolygon($wb, $pts)
}

$wb.Dispose()
$g.ResetClip()
$clipPath.Dispose()
$g.Dispose()

$bmp.Save("$assetsDir\nusa.png", [System.Drawing.Imaging.ImageFormat]::Png)
Install-Flags $bmp 'NUS'
$bmp.Dispose()
Write-Host "  NUSA done: 3 sizes x 5 variants = 15 TGA files"

# ================================================================
#  USSR FLAG
#  Solid red, gold orbital-hammer symbol + sparkle
# ================================================================
Write-Host "Creating USSR flag..."

$W = 820; $H = 520
$bmp = [System.Drawing.Bitmap]::new($W, $H, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
$g   = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = 'HighQuality'

# Solid red background
$br = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(204, 0, 0))
$g.FillRectangle($br, 0, 0, $W, $H)
$br.Dispose()

$gold   = [System.Drawing.Color]::FromArgb(255, 205, 0)
$goldBr = New-Object System.Drawing.SolidBrush $gold

# Symbol center (lower-left quadrant)
$symX = [float]($W * 0.20)
$symY = [float]($H * 0.58)

# --- Orbital ring (tilted ellipse with arrow end) ---
$state = $g.Save()
$g.TranslateTransform($symX, $symY)
$g.RotateTransform(-15)

$eW = [float]($W * 0.26)
$eH = [float]($H * 0.48)

# Draw arc (slightly less than full circle) with arrow cap
$ringPen = New-Object System.Drawing.Pen $gold, 18
$ringPen.StartCap = 'Round'
try {
    $arrow = New-Object System.Drawing.Drawing2D.AdjustableArrowCap(5, 4, $true)
    $ringPen.CustomEndCap = $arrow
} catch { }
$g.DrawArc($ringPen, [float](-$eW/2), [float](-$eH/2), $eW, $eH, 250.0, 330.0)
$ringPen.Dispose()

$g.Restore($state)

# --- Hammer handle (diagonal line from lower-left to upper-right) ---
$hAng  = -55.0 * [Math]::PI / 180.0
$hLen  = $H * 0.32
$hx1   = [float]($symX - $hLen * 0.35 * [Math]::Cos($hAng))
$hy1   = [float]($symY - $hLen * 0.35 * [Math]::Sin($hAng))
$hx2   = [float]($symX + $hLen * 0.65 * [Math]::Cos($hAng))
$hy2   = [float]($symY + $hLen * 0.65 * [Math]::Sin($hAng))

$hPen = New-Object System.Drawing.Pen $gold, 14
$hPen.StartCap = 'Round'
$hPen.EndCap   = 'Round'
$g.DrawLine($hPen, $hx1, $hy1, $hx2, $hy2)
$hPen.Dispose()

# --- Hammer head (small rotated rectangle at the upper end) ---
$state2 = $g.Save()
$g.TranslateTransform($hx2, $hy2)
$g.RotateTransform(35)    # perpendicular to handle angle (-55 + 90 = 35)
$g.FillRectangle($goldBr, -22.0, -10.0, 44.0, 20.0)
$g.Restore($state2)

# --- 4-pointed sparkle star above the symbol ---
$spkX = [float]($symX + 15)
$spkY = [float]($symY - $H * 0.33)
$pts  = StarPoly $spkX $spkY 26.0 5.0 4 0
$g.FillPolygon($goldBr, $pts)

$goldBr.Dispose()
$g.Dispose()

$bmp.Save("$assetsDir\ussr.png", [System.Drawing.Imaging.ImageFormat]::Png)
Install-Flags $bmp 'USR'
$bmp.Dispose()
Write-Host "  USSR done: 3 sizes x 5 variants = 15 TGA files"

Write-Host "`nAll flags created and installed into mod\gfx\flags\"
