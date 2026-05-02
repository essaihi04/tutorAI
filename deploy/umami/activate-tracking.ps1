# =============================================================
# Moalim — Activation du tracking Umami
# Usage :
#   powershell -ExecutionPolicy Bypass -File deploy\umami\activate-tracking.ps1 -WebsiteId <UUID>
#
# Étapes :
#   1) Valide le format du UUID
#   2) Remplace WEBSITE_ID_PLACEHOLDER dans frontend/public/js/umami.js
#   3) Commit + push
#   4) Redéploie sur le VPS
# =============================================================

param(
    [Parameter(Mandatory = $true)]
    [string]$WebsiteId
)

$ErrorActionPreference = "Stop"

function Step($msg) { Write-Host ""; Write-Host "▶ $msg" -ForegroundColor Cyan }
function Ok($msg)   { Write-Host "  ✓ $msg" -ForegroundColor Green }
function Err($msg)  { Write-Host "  ✗ $msg" -ForegroundColor Red }

$repoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Push-Location $repoRoot

try {
    # ── 1) Validation du format UUID ──
    Step "Validation du Website ID"
    $uuidRegex = '^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
    if ($WebsiteId -notmatch $uuidRegex) {
        Err "Le Website ID ne ressemble pas à un UUID valide : $WebsiteId"
        Write-Host "  Format attendu : xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" -ForegroundColor Gray
        exit 1
    }
    Ok "UUID valide : $WebsiteId"

    # ── 2) Remplacement dans umami.js ──
    Step "Injection du Website ID dans frontend/public/js/umami.js"
    $umamiJs = Join-Path $repoRoot "frontend\public\js\umami.js"
    if (-not (Test-Path $umamiJs)) {
        Err "Fichier introuvable : $umamiJs"
        exit 1
    }

    $content = Get-Content -Path $umamiJs -Raw -Encoding UTF8
    if ($content -notmatch "WEBSITE_ID_PLACEHOLDER") {
        Write-Host "  ⚠ Placeholder non trouvé. Le tracking est peut-être déjà activé." -ForegroundColor Yellow
        $answer = Read-Host "  Forcer le remplacement ? (y/N)"
        if ($answer -ne "y" -and $answer -ne "Y") { exit 0 }

        # Remplace n'importe quelle valeur WEBSITE_ID = "..."
        $content = $content -replace 'var WEBSITE_ID = "[^"]*";', "var WEBSITE_ID = `"$WebsiteId`";"
    } else {
        $content = $content -replace "WEBSITE_ID_PLACEHOLDER", $WebsiteId
    }

    Set-Content -Path $umamiJs -Value $content -Encoding UTF8 -NoNewline
    Ok "Website ID injecté"

    # ── 3) Commit + push ──
    Step "Commit & push sur le repo"
    git add frontend/public/js/umami.js
    git commit -m "feat(analytics): activate Umami tracking"
    if ($LASTEXITCODE -ne 0) {
        Err "Git commit a échoué (peut-être rien à committer ?)"
    } else {
        Ok "Commit créé"
    }

    git push
    if ($LASTEXITCODE -ne 0) {
        Err "Git push a échoué"
        exit 1
    }
    Ok "Push OK"

    # ── 4) Redéploiement ──
    Step "Redéploiement sur le VPS (git pull + rebuild frontend)"
    Write-Host "  (mot de passe SSH demandé)" -ForegroundColor Gray
    & powershell -ExecutionPolicy Bypass -File (Join-Path $repoRoot "deploy\remote-deploy.ps1") -UpdateOnly
    if ($LASTEXITCODE -ne 0) {
        Err "Redéploiement a échoué"
        exit 1
    }

    # ── Succès ──
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
    Write-Host "  🎉 TRACKING UMAMI ACTIVÉ" -ForegroundColor Green
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
    Write-Host ""
    Write-Host "  ✅ Website ID    : $WebsiteId" -ForegroundColor Gray
    Write-Host "  ✅ Frontend      : déployé avec tracking actif" -ForegroundColor Gray
    Write-Host "  📊 Dashboard     : https://analytics.moalim.online" -ForegroundColor Cyan
    Write-Host "  🌐 Site tracké   : https://moalim.online" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  Pour vérifier que ça marche :" -ForegroundColor White
    Write-Host "  1) Ouvre https://moalim.online dans un onglet privé" -ForegroundColor Gray
    Write-Host "  2) Navigue un peu (clique sur le diagnostic, quelques pages)" -ForegroundColor Gray
    Write-Host "  3) Ouvre https://analytics.moalim.online → Realtime" -ForegroundColor Gray
    Write-Host "  4) Tu devrais te voir toi-même (latence < 10 secondes)" -ForegroundColor Gray
    Write-Host ""

    Start-Sleep -Seconds 2
    Start-Process "https://analytics.moalim.online"

} finally {
    Pop-Location
}
