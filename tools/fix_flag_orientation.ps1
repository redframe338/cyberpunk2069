$flagsDir = "C:\Users\victo\cyberpunk mod\mod\gfx\flags"
$fixed = 0

Get-ChildItem -LiteralPath $flagsDir -Recurse -File -Filter "*.tga" | ForEach-Object {
    $bytes = [System.IO.File]::ReadAllBytes($_.FullName)
    if ($bytes.Length -lt 18 -or $bytes[2] -ne 2) { return }

    $width = $bytes[12] + ($bytes[13] -shl 8)
    $height = $bytes[14] + ($bytes[15] -shl 8)
    $bytesPerPixel = [int]($bytes[16] / 8)
    $topOrigin = ($bytes[17] -band 0x20) -ne 0
    if (-not $topOrigin -or $bytesPerPixel -lt 3) { return }

    $imageOffset = 18 + $bytes[0]
    $rowSize = $width * $bytesPerPixel
    $copy = New-Object byte[] $bytes.Length
    [Array]::Copy($bytes, $copy, $bytes.Length)

    for ($row = 0; $row -lt $height; $row++) {
        $sourceOffset = $imageOffset + ($row * $rowSize)
        $destinationOffset = $imageOffset + (($height - 1 - $row) * $rowSize)
        [Array]::Copy($bytes, $sourceOffset, $copy, $destinationOffset, $rowSize)
    }

    # Preserve alpha-depth bits but clear the top-origin bit.
    $copy[17] = $copy[17] -band 0x0F
    [System.IO.File]::WriteAllBytes($_.FullName, $copy)
    $fixed++
}

Write-Host "Corrected orientation for $fixed custom flag files."
