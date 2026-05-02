# =============================================================
# Moalim - Activation du tracking Umami
# Usage:
#   powershell -ExecutionPolicy Bypass -File deploy\umami\activate-tracking.ps1 -WebsiteId UUID
# =============================================================

param(
    [Parameter(Mandatory = $true)]
    [string]$WebsiteId
)

$ErrorActionPreference = "Stop"

function Step($msg) { Write-Host ""; Write-Host ">> $msg" -ForegroundColor Cyan }
function Ok($msg)   { Write-Host "   [OK] $msg" -ForegroundColor Green }
function Err($msg)  { Write-Host "   [X] $msg" -ForegroundColor Red }

$repoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Push-Location $repoRoot

try {
    Step "Validation du Website ID"
    $uuidRegex = '^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
    if ($WebsiteId -notmatch $uuidRegex) {
        Err "Le Website ID ne ressemble pas a un UUID valide: $WebsiteId"
        Write-Host "   Format attendu: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" -ForegroundColor Gray
        exit 1
    }
    Ok "UUID valide: $WebsiteId"

    Step "Injection du Website ID dans frontend/public/js/umami.js"
    $umamiJs = Join-Path $repoRoot "frontend\public\js\umami.js"
    if (-not (Test-Path $umamiJs)) {
        Err "Fichier introuvable: $umamiJs"
        exit 1
    }

    # IMPORTANT : on remplace UNIQUEMENT la ligne `var WEBSITE_ID = "..."` pour
    # preserver la sentinelle "WEBSITE_ID_PLACEHOLDER" dans le garde de securite.
    $content = Get-Content -Path $umamiJs -Raw -Encoding UTF8
    $newContent = $content -replace 'var WEBSITE_ID = "[^"]*";', "var WEBSITE_ID = `"$WebsiteId`";"
    if ($newContent -eq $content) {
        Err "Impossible de trouver la ligne 'var WEBSITE_ID = ...' dans $umamiJs"
        exit 1
    }
    $content = $newContent

    Set-Content -Path $umamiJs -Value $content -Encoding UTF8 -NoNewline
    Ok "Website ID injecte"

    Step "Commit et push sur le repo"
    git add frontend/public/js/umami.js
    git commit -m "feat(analytics): activate Umami tracking"
    if ($LASTEXITCODE -ne 0) {
        Err "Git commit a echoue (peut-etre rien a committer)"
    } else {
        Ok "Commit cree"
    }

    git push
    if ($LASTEXITCODE -ne 0) {
        Err "Git push a echoue"
        exit 1
    }
    Ok "Push OK"

    Step "Redeploiement sur le VPS"
    Write-Host "   (mot de passe SSH demande)" -ForegroundColor Gray
    & powershell -ExecutionPolicy Bypass -File (Join-Path $repoRoot "deploy\remote-deploy.ps1") -UpdateOnly
    if ($LASTEXITCODE -ne 0) {
        Err "Redeploiement a echoue"
        exit 1
    }

    Write-Host ""
    Write-Host "===========================================================" -ForegroundColor Green
    Write-Host "  TRACKING UMAMI ACTIVE" -ForegroundColor Green
    Write-Host "===========================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "   Website ID    : $WebsiteId" -ForegroundColor Gray
    Write-Host "   Frontend      : deploye avec tracking actif" -ForegroundColor Gray
    Write-Host "   Dashboard     : https://analytics.moalim.online" -ForegroundColor Cyan
    Write-Host "   Site track    : https://moalim.online" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "   Verification:" -ForegroundColor White
    Write-Host "   1. Ouvre https://moalim.online dans un onglet prive" -ForegroundColor Gray
    Write-Host "   2. Navigue (clic diagnostic, plusieurs pages)" -ForegroundColor Gray
    Write-Host "   3. Va sur https://analytics.moalim.online -> Realtime" -ForegroundColor Gray
    Write-Host "   4. Tu dois te voir en live (latence < 10s)" -ForegroundColor Gray
    Write-Host ""

    Start-Sleep -Seconds 2
    Start-Process "https://analytics.moalim.online"

} finally {
    Pop-Location
}
