Add-Type -AssemblyName System.Drawing

$sourcePath = "C:\Users\victo\Downloads\IMG_6602.jpeg"
$flagsDir = "C:\Users\victo\cyberpunk mod\mod\gfx\flags"

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
    # Use the same bottom-origin TGA storage as vanilla HOI4 flags.
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
$canvas = [System.Drawing.Bitmap]::new(820, 520, [System.Drawing.Imaging.PixelFormat]::Format32bppArgb)
$graphics = [System.Drawing.Graphics]::FromImage($canvas)
$graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality

# Center-crop only the excess blue field, preserving the circular emblem.
$targetRatio = 820.0 / 520.0
$sourceRatio = $source.Width / [double]$source.Height
if ($sourceRatio -gt $targetRatio) {
    $cropHeight = $source.Height
    $cropWidth = [int][Math]::Round($source.Height * $targetRatio)
    $cropX = [int](($source.Width - $cropWidth) / 2)
    $cropY = 0
} else {
    $cropWidth = $source.Width
    $cropHeight = [int][Math]::Round($source.Width / $targetRatio)
    $cropX = 0
    $cropY = [int](($source.Height - $cropHeight) / 2)
}
$destination = [System.Drawing.Rectangle]::new(0, 0, 820, 520)
$crop = [System.Drawing.Rectangle]::new($cropX, $cropY, $cropWidth, $cropHeight)
$graphics.DrawImage($source, $destination, $crop, [System.Drawing.GraphicsUnit]::Pixel)
$graphics.Dispose()
$source.Dispose()

$sizes = @(
    @{ directory = $flagsDir; width = 82; height = 52 },
    @{ directory = (Join-Path $flagsDir "medium"); width = 41; height = 26 },
    @{ directory = (Join-Path $flagsDir "small"); width = 10; height = 7 }
)
foreach ($size in $sizes) {
    foreach ($suffix in @("", "_neutrality", "_democratic", "_fascism", "_communism")) {
        Save-Tga $canvas $size.width $size.height (Join-Path $size.directory "OAS$suffix.tga")
    }
}

$canvas.Dispose()
Write-Host "Installed 15 bottom-origin OAS flag files."
