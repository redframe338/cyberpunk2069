Add-Type -AssemblyName System.Drawing

$root = "C:\Users\victo\cyberpunk mod"
$flagsDir = Join-Path $root "mod\gfx\flags"
$sourcePath = "C:\Users\victo\Downloads\IMG_6601.jpeg"

function Save-Tga([System.Drawing.Bitmap]$source, [int]$width, [int]$height, [string]$path) {
    $directory = Split-Path $path
    if (-not (Test-Path -LiteralPath $directory)) {
        New-Item -ItemType Directory -Force -Path $directory | Out-Null
    }

    $output = [System.Drawing.Bitmap]::new($width, $height, [System.Drawing.Imaging.PixelFormat]::Format24bppRgb)
    $graphics = [System.Drawing.Graphics]::FromImage($output)
    $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $graphics.DrawImage($source, 0, 0, $width, $height)
    $graphics.Dispose()

    $header = New-Object byte[] 18
    $header[2] = 2
    $header[12] = $width -band 0xFF
    $header[13] = ($width -shr 8) -band 0xFF
    $header[14] = $height -band 0xFF
    $header[15] = ($height -shr 8) -band 0xFF
    $header[16] = 24
    $header[17] = 0

    $pixels = New-Object byte[] ($width * $height * 3)
    $index = 0
    # HOI4/vanilla flags use bottom-origin TGA storage.
    for ($y = $height - 1; $y -ge 0; $y--) {
        for ($x = 0; $x -lt $width; $x++) {
            $color = $output.GetPixel($x, $y)
            $pixels[$index++] = $color.B
            $pixels[$index++] = $color.G
            $pixels[$index++] = $color.R
        }
    }
    $output.Dispose()
    [System.IO.File]::WriteAllBytes($path, $header + $pixels)
}

$source = [System.Drawing.Image]::FromFile($sourcePath)
$bitmap = [System.Drawing.Bitmap]::new(820, 520, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
$g = [System.Drawing.Graphics]::FromImage($bitmap)
$g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
$g.Clear([System.Drawing.Color]::Black)

# Preserve the supplied square logo without stretching it to HOI4's flag ratio.
$scale = [Math]::Min(820.0 / $source.Width, 520.0 / $source.Height)
$drawWidth = [int][Math]::Round($source.Width * $scale)
$drawHeight = [int][Math]::Round($source.Height * $scale)
$drawX = [int]((820 - $drawWidth) / 2)
$drawY = [int]((520 - $drawHeight) / 2)
$g.DrawImage($source, $drawX, $drawY, $drawWidth, $drawHeight)

$g.Dispose()
$source.Dispose()

$sizes = @(
    @{ directory = $flagsDir; width = 82; height = 52 },
    @{ directory = (Join-Path $flagsDir "medium"); width = 41; height = 26 },
    @{ directory = (Join-Path $flagsDir "small"); width = 10; height = 7 }
)
foreach ($size in $sizes) {
    foreach ($suffix in @("", "_neutrality", "_democratic", "_fascism", "_communism")) {
        Save-Tga $bitmap $size.width $size.height (Join-Path $size.directory "MLT$suffix.tga")
    }
}

$bitmap.Dispose()
Write-Host "Installed 15 bottom-origin Militech flag files."
