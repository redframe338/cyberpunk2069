$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing

$root = Split-Path -Parent $PSScriptRoot
$source = Join-Path $root 'assets\fsa.png'
$flags = Join-Path $root 'mod\gfx\flags'
$sizes = @{
	'' = @(82, 52)
	'medium' = @(41, 26)
	'small' = @(10, 7)
}
$variants = @('', '_communism', '_democratic', '_fascism', '_neutrality')

function Save-Hoi4Tga($image, [int]$width, [int]$height, [string]$path) {
	$bitmap = New-Object System.Drawing.Bitmap $width, $height, ([System.Drawing.Imaging.PixelFormat]::Format24bppRgb)
	$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
	$graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
	$graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
	$graphics.CompositingQuality = [System.Drawing.Drawing2D.CompositingQuality]::HighQuality
	$graphics.DrawImage($image, 0, 0, $width, $height)
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
	for ($y = $height - 1; $y -ge 0; $y--) {
		for ($x = 0; $x -lt $width; $x++) {
			$color = $bitmap.GetPixel($x, $y)
			$pixels[$index++] = $color.B
			$pixels[$index++] = $color.G
			$pixels[$index++] = $color.R
		}
	}
	$bitmap.Dispose()
	[System.IO.File]::WriteAllBytes($path, ($header + $pixels))
}

$bytes = [System.IO.File]::ReadAllBytes($source)
$stream = New-Object System.IO.MemoryStream (,$bytes)
$image = [System.Drawing.Image]::FromStream($stream)

foreach ($folder in $sizes.Keys) {
	$dimensions = $sizes[$folder]
	$outputDirectory = if ($folder) { Join-Path $flags $folder } else { $flags }
	foreach ($suffix in $variants) {
		Save-Hoi4Tga $image $dimensions[0] $dimensions[1] (Join-Path $outputDirectory "FSA$suffix.tga")
	}
}

$image.Dispose()
$stream.Dispose()
Write-Host 'Installed 15 Free States Of West America flag files.'
