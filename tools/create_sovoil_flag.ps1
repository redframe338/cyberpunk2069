Add-Type -AssemblyName System.Drawing

$sourcePath = "C:\Users\victo\cyberpunk mod\assets\sovoil_flag_source.jpeg"
$flagsDir = "C:\Users\victo\cyberpunk mod\mod\gfx\flags"

function Save-Tga([System.Drawing.Bitmap]$source, [int]$width, [int]$height, [string]$path) {
    $directory = Split-Path $path
    if (-not (Test-Path $directory)) {
        New-Item -ItemType Directory -Force $directory | Out-Null
    }

    $scaled = [System.Drawing.Bitmap]::new($width, $height, [System.Drawing.Imaging.PixelFormat]::Format24bppRgb)
    $graphics = [System.Drawing.Graphics]::FromImage($scaled)
    $graphics.InterpolationMode = 'HighQualityBicubic'
    $graphics.PixelOffsetMode = 'HighQuality'
    $graphics.DrawImage($source, 0, 0, $width, $height)
    $graphics.Dispose()

    $header = New-Object byte[] 18
    $header[2] = 2
    $header[12] = $width -band 0xFF
    $header[13] = ($width -shr 8) -band 0xFF
    $header[14] = $height -band 0xFF
    $header[15] = ($height -shr 8) -band 0xFF
    $header[16] = 24
    # HOI4 expects bottom-origin TGA pixel storage, matching vanilla flags.
    $header[17] = 0

    $pixels = New-Object byte[] ($width * $height * 3)
    $index = 0
    for ($y = $height - 1; $y -ge 0; $y--) {
        for ($x = 0; $x -lt $width; $x++) {
            $color = $scaled.GetPixel($x, $y)
            $pixels[$index++] = $color.B
            $pixels[$index++] = $color.G
            $pixels[$index++] = $color.R
        }
    }
    $scaled.Dispose()
    [System.IO.File]::WriteAllBytes($path, $header + $pixels)
}

if (-not (Test-Path -LiteralPath $sourcePath)) {
    throw "SovOil source image not found: $sourcePath"
}

$original = [System.Drawing.Bitmap]::FromFile($sourcePath)
$targetRatio = 82.0 / 52.0
$sourceRatio = $original.Width / [double]$original.Height

# Center-crop to HOI4's flag ratio so the supplied logo is not stretched.
if ($sourceRatio -gt $targetRatio) {
    $cropHeight = $original.Height
    $cropWidth = [int][Math]::Round($cropHeight * $targetRatio)
    $cropX = [int](($original.Width - $cropWidth) / 2)
    $cropY = 0
} else {
    $cropWidth = $original.Width
    $cropHeight = [int][Math]::Round($cropWidth / $targetRatio)
    $cropX = 0
    $cropY = [int](($original.Height - $cropHeight) / 2)
}

$cropped = [System.Drawing.Bitmap]::new($cropWidth, $cropHeight, [System.Drawing.Imaging.PixelFormat]::Format24bppRgb)
$cropGraphics = [System.Drawing.Graphics]::FromImage($cropped)
$sourceRectangle = [System.Drawing.Rectangle]::new($cropX, $cropY, $cropWidth, $cropHeight)
$destinationRectangle = [System.Drawing.Rectangle]::new(0, 0, $cropWidth, $cropHeight)
$cropGraphics.DrawImage($original, $destinationRectangle, $sourceRectangle, [System.Drawing.GraphicsUnit]::Pixel)
$cropGraphics.Dispose()
$original.Dispose()

foreach ($size in @(
    @{ folder = ''; width = 82; height = 52 },
    @{ folder = 'medium'; width = 41; height = 26 },
    @{ folder = 'small'; width = 10; height = 7 }
)) {
    $destination = if ($size.folder) { Join-Path $flagsDir $size.folder } else { $flagsDir }
    foreach ($suffix in @('', '_neutrality', '_communism', '_democratic', '_fascism')) {
        Save-Tga $cropped $size.width $size.height (Join-Path $destination "SVO$suffix.tga")
    }
}

$cropped.Dispose()
Write-Host "Installed IMG_5900.jpeg as 15 SovOil flag variants."
