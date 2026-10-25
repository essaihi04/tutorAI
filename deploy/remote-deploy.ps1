# =============================================================
# Moalim — Déploiement à distance depuis Windows
# Usage:
#   cd C:\Users\HP\Desktop\ai-tutor-bac
#   ./deploy/remote-deploy.ps1
#
# Cible : nouveau VPS Ubuntu (/opt/moalim, /etc/moalim/backend.env),
# déployé par deploy/deploy-ubuntu.sh (rejouable).
# =============================================================

param(
    # Alias du ~/.ssh/config : nouveau VPS Ubuntu 217.160.128.247 (clé moalim_deploy).
    # 87.106.1.128 est l'ancien serveur AlmaLinux, abandonné depuis la migration.
    [string]$ServerIp = "moalim-vps",
    [string]$User     = "root",
    [string]$Branch   = "main",
    [switch]$UpdateOnly,  # use -UpdateOnly for re-deploys (faster)
    [switch]$UpdateEnv    # use -UpdateEnv to push updated backend.env to server
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

# ── Env-only update mode ─────────────────────────────────────
if ($UpdateEnv) {
    Step "Mise à jour du fichier .env sur le serveur"
    $envFile = Join-Path $PSScriptRoot "backend.env"
    if (-not (Test-Path $envFile)) {
        Write-Host "✖ deploy/backend.env introuvable." -ForegroundColor Red
        exit 1
    }
    $envContent = Get-Content $envFile -Raw
    $envBytes   = [System.Text.Encoding]::UTF8.GetBytes($envContent)
    $envBase64  = [System.Convert]::ToBase64String($envBytes)
    $cmd = "echo '$envBase64' | base64 -d > /etc/moalim/backend.env && chown root:moalim /etc/moalim/backend.env && chmod 640 /etc/moalim/backend.env && systemctl restart moalim-backend && echo 'Backend .env mis à jour et service redémarré'"
    ssh "$User@$ServerIp" $cmd
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✖ .env NON mis à jour (ssh a renvoyé $LASTEXITCODE)." -ForegroundColor Red
        exit $LASTEXITCODE
    }
    Write-Host ""
    Write-Host "✅ .env mis à jour. https://moalim.online" -ForegroundColor Green
    exit 0
}

# ── Update mode (faster, after first deploy) ─────────────────
if ($UpdateOnly) {
    Step "Mode mise à jour (git reset origin/main + rebuild)"
    ssh "$User@$ServerIp" "bash /opt/moalim/deploy/deploy-ubuntu.sh"
    # ssh est un exécutable natif : $ErrorActionPreference ne l'arrête pas.
    # Sans ce test, un accès refusé affichait quand même « terminée ».
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "✖ Mise à jour NON effectuée (ssh/deploy-ubuntu.sh a renvoyé $LASTEXITCODE)." -ForegroundColor Red
        exit $LASTEXITCODE
    }
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

echo '── Décodage du .env ──'
mkdir -p /etc/moalim
echo '$envBase64' | base64 -d > /etc/moalim/backend.env
chmod 640 /etc/moalim/backend.env

echo '── Clone du repo ──'
[ -d /opt/moalim/.git ] || git clone -b $Branch https://github.com/essaihi04/tutorAI.git /opt/moalim

echo '── Lancement de deploy-ubuntu.sh ──'
bash /opt/moalim/deploy/deploy-ubuntu.sh
"@

# Force LF line endings so bash on Linux doesn't choke on CRLF
$remoteScript = $remoteScript -replace "`r`n", "`n"

# One single ssh call → one single password prompt
$remoteScript | ssh "$User@$ServerIp" "bash -s"
if ($LASTEXITCODE -ne 0) {
    Write-Host "✖ Déploiement NON effectué (code $LASTEXITCODE)." -ForegroundColor Red
    exit $LASTEXITCODE
}

Write-Host ""
Write-Host "✅ Déploiement terminé." -ForegroundColor Green
Write-Host "   Site    : https://moalim.online"
Write-Host "   Health  : https://moalim.online/health"
Write-Host ""
Write-Host "Pour les mises à jour futures :"
Write-Host "   ./deploy/remote-deploy.ps1 -UpdateOnly" -ForegroundColor Yellow
