# =============================================================
# Moalim — Inject Umami tracking script in all static HTML pages
# Usage : powershell -ExecutionPolicy Bypass -File deploy/umami/inject-tracking.ps1
# Idempotent : peut être lancé plusieurs fois sans dupliquer le tag
# =============================================================

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$blogDir  = Join-Path $repoRoot "frontend\public\blog"

if (-not (Test-Path $blogDir)) {
    Write-Error "Blog directory not found: $blogDir"
    exit 1
}

$scriptTag = '<script src="/js/umami.js" defer></script>'

$files = Get-ChildItem -Path $blogDir -Filter *.html -File -Recurse
Write-Host "Scanning $($files.Count) HTML file(s) in $blogDir" -ForegroundColor Cyan

$injected = 0
$skipped  = 0

foreach ($file in $files) {
    $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8

    # Skip si déjà injecté
    if ($content -match [regex]::Escape($scriptTag)) {
        Write-Host "  - $($file.Name) : déjà injecté" -ForegroundColor Yellow
        $skipped++
        continue
    }

    # Injecte juste avant </head>
    if ($content -notmatch "</head>") {
        Write-Host "  - $($file.Name) : pas de </head>, ignoré" -ForegroundColor Red
        $skipped++
        continue
    }

    $newContent = $content -replace "</head>", "$scriptTag`r`n</head>"
    Set-Content -Path $file.FullName -Value $newContent -Encoding UTF8 -NoNewline
    Write-Host "  + $($file.Name) : injecté" -ForegroundColor Green
    $injected++
}

Write-Host ""
Write-Host "Done. Injected: $injected | Skipped: $skipped" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor White
Write-Host "  1) Edit frontend/public/js/umami.js → replace WEBSITE_ID_PLACEHOLDER" -ForegroundColor Gray
Write-Host "  2) Redeploy: powershell -ExecutionPolicy Bypass -File deploy/remote-deploy.ps1 -UpdateOnly" -ForegroundColor Gray
