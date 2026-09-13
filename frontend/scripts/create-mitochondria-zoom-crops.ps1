Add-Type -AssemblyName System.Drawing

$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$imageDirectory = Join-Path $projectRoot 'frontend\public\media\images\svt\ch1_consommation_matiere_organique\lesson_1_liberation_energie\respiration'
$mainImage = Join-Path $imageDirectory 'mitochondrie_3d_sans_legendes.png'
$membraneImage = Join-Path $imageDirectory 'mitochondrie_double_membrane_zoom.png'

function Export-ZoomCrop {
  param(
    [Parameter(Mandatory = $true)][string]$Source,
    [Parameter(Mandatory = $true)][System.Drawing.Rectangle]$Crop,
    [Parameter(Mandatory = $true)][string]$Destination
  )

  $sourceBitmap = [System.Drawing.Bitmap]::FromFile($Source)
  $outputBitmap = New-Object System.Drawing.Bitmap 1536, 864
  $graphics = [System.Drawing.Graphics]::FromImage($outputBitmap)

  try {
    $graphics.CompositingMode = [System.Drawing.Drawing2D.CompositingMode]::SourceCopy
    $graphics.CompositingQuality = [System.Drawing.Drawing2D.CompositingQuality]::HighQuality
    $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
    $graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
    $destinationRectangle = New-Object System.Drawing.Rectangle 0, 0, 1536, 864
    $graphics.DrawImage($sourceBitmap, $destinationRectangle, $Crop, [System.Drawing.GraphicsUnit]::Pixel)
    $outputBitmap.Save($Destination, [System.Drawing.Imaging.ImageFormat]::Png)
  }
  finally {
    $graphics.Dispose()
    $outputBitmap.Dispose()
    $sourceBitmap.Dispose()
  }
}

# Les recadrages conservent un rapport 16:9 et isolent une seule structure à la fois.
Export-ZoomCrop -Source $mainImage -Crop ([System.Drawing.Rectangle]::new(300, 150, 1100, 619)) -Destination (Join-Path $imageDirectory 'mitochondrie_cretes_zoom.png')
Export-ZoomCrop -Source $membraneImage -Crop ([System.Drawing.Rectangle]::new(230, 105, 1240, 698)) -Destination (Join-Path $imageDirectory 'mitochondrie_espace_intermembranaire_zoom.png')
Export-ZoomCrop -Source $mainImage -Crop ([System.Drawing.Rectangle]::new(455, 205, 960, 540)) -Destination (Join-Path $imageDirectory 'mitochondrie_matrice_zoom.png')

Write-Output 'Zooms mitochondriaux exportes.'
