# =============================================================
# Moalim — Déploiement à distance depuis Windows
# Usage:
#   cd C:\Users\HP\Desktop\ai-tutor-bac
#   ./deploy/remote-deploy.ps1
#
# Tu seras invité à entrer le mot de passe root du serveur
# (deux fois : une pour scp, une pour ssh).
# =============================================================

param(
    [string]$ServerIp = "87.106.1.128",
    [string]$User     = "root",
    [string]$Branch   = "main",
    [switch]$UpdateOnly  # use -UpdateOnly for re-deploys (faster)
)

$ErrorActionPreference = "Stop"

function Step($msg) {
    Write-Host ""
    Write-Host "▶ $msg" -ForegroundColor Cyan
}

# ── Verify prerequisites ─────────────────────────────────────
Step "Vérification des outils locaux"
if (-not (Get-Command ssh -ErrorAction SilentlyContinue)) {
    Write-Host "✖ ssh introuvable. Installe OpenSSH Client (Settings > Apps > Optional Features > OpenSSH Client)." -ForegroundColor Red
    exit 1
}
if (-not (Get-Command scp -ErrorAction SilentlyContinue)) {
    Write-Host "✖ scp introuvable. Installe OpenSSH Client." -ForegroundColor Red
    exit 1
}

$envFile = Join-Path $PSScriptRoot "backend.env"
if (-not (Test-Path $envFile)) {
    Write-Host "✖ deploy/backend.env introuvable." -ForegroundColor Red
    exit 1
}

# ── Update mode (faster, after first deploy) ─────────────────
if ($UpdateOnly) {
    Step "Mode mise à jour (git pull + rebuild)"
    ssh "$User@$ServerIp" "bash /var/www/moalim/deploy/update.sh"
    Write-Host ""
    Write-Host "✅ Mise à jour terminée. https://moalim.online" -ForegroundColor Green
    exit 0
}

# ── First-time deployment ────────────────────────────────────
Step "Préparation du .env (encodé en base64)"
$envBytes  = [System.IO.File]::ReadAllBytes($envFile)
$envBase64 = [System.Convert]::ToBase64String($envBytes)

Step "Lancement du déploiement complet sur le serveur (~5-10 min)"
Write-Host "   Tu seras invité à entrer le mot de passe SSH une seule fois." -ForegroundColor Yellow
Write-Host ""

$remoteScript = @"
set -e

echo '── Clone du repo ──'
rm -rf /tmp/tutorAI
git clone -b $Branch https://github.com/essaihi04/tutorAI.git /tmp/tutorAI

echo '── Décodage du .env ──'
mkdir -p /var/www/moalim/backend
echo '$envBase64' | base64 -d > /var/www/moalim/backend/.env
chmod 600 /var/www/moalim/backend/.env

echo '── Lancement de deploy.sh ──'
chmod +x /tmp/tutorAI/deploy/deploy.sh
bash /tmp/tutorAI/deploy/deploy.sh
"@

# Force LF line endings so bash on Linux doesn't choke on CRLF
$remoteScript = $remoteScript -replace "`r`n", "`n"

# One single ssh call → one single password prompt
$remoteScript | ssh "$User@$ServerIp" "bash -s"

Write-Host ""
Write-Host "✅ Déploiement terminé." -ForegroundColor Green
Write-Host "   Site    : https://moalim.online"
Write-Host "   Health  : https://moalim.online/health"
Write-Host ""
Write-Host "Pour les mises à jour futures :"
Write-Host "   ./deploy/remote-deploy.ps1 -UpdateOnly" -ForegroundColor Yellow
