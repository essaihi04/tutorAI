# =============================================================
# Moalim — Installation Umami end-to-end depuis Windows
# Usage :
#   powershell -ExecutionPolicy Bypass -File deploy\umami\launch-install.ps1
#
# Ce script :
#   1) Vérifie que le DNS analytics.moalim.online est propagé
#   2) Déploie le code à jour sur le VPS (git pull + rebuild frontend)
#   3) Lance l'install Umami sur le VPS (Docker + nginx + SSL)
#   4) Ouvre https://analytics.moalim.online dans le navigateur
#
# Mot de passe SSH root : demandé 2-3 fois (une par étape)
# =============================================================

param(
    [string]$ServerIp = "87.106.1.128",
    [string]$User     = "root",
    [string]$Domain   = "analytics.moalim.online",
    [switch]$SkipDnsCheck,
    [switch]$SkipDeploy
)

$ErrorActionPreference = "Stop"

function Step($msg) {
    Write-Host ""
    Write-Host "▶ $msg" -ForegroundColor Cyan
}
function Ok($msg)  { Write-Host "  ✓ $msg" -ForegroundColor Green }
function Warn($msg){ Write-Host "  ⚠ $msg" -ForegroundColor Yellow }
function Err($msg) { Write-Host "  ✗ $msg" -ForegroundColor Red }

$repoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Push-Location $repoRoot

try {
    # ── Prérequis ───────────────────────────────────────────────
    Step "Vérification des outils locaux"
    if (-not (Get-Command ssh -ErrorAction SilentlyContinue)) {
        Err "ssh introuvable. Installe OpenSSH Client (Settings > Apps > Optional Features)."
        exit 1
    }
    Ok "ssh OK"

    # ── 1) Vérifier DNS ────────────────────────────────────────
    if (-not $SkipDnsCheck) {
        Step "Vérification de la propagation DNS pour $Domain"
        try {
            $result = Resolve-DnsName -Name $Domain -Type A -ErrorAction Stop
            $ip = ($result | Where-Object { $_.Type -eq 'A' } | Select-Object -First 1).IPAddress
            if ($ip -eq $ServerIp) {
                Ok "$Domain → $ip (correct)"
            } else {
                Warn "$Domain → $ip (attendu: $ServerIp)"
                Write-Host ""
                Write-Host "  Le DNS pointe vers une mauvaise IP. Vérifie ton registrar." -ForegroundColor Yellow
                Write-Host "  Si tu viens de modifier le DNS, attends 10-30 min puis relance." -ForegroundColor Yellow
                Write-Host ""
                $answer = Read-Host "  Continuer quand même ? (y/N)"
                if ($answer -ne "y" -and $answer -ne "Y") { exit 1 }
            }
        } catch {
            Err "$Domain n'est pas résolu par DNS."
            Write-Host ""
            Write-Host "  Ajoute chez ton registrar :" -ForegroundColor Yellow
            Write-Host "    Type  : A" -ForegroundColor Gray
            Write-Host "    Nom   : analytics" -ForegroundColor Gray
            Write-Host "    Valeur: $ServerIp" -ForegroundColor Gray
            Write-Host "    TTL   : 3600" -ForegroundColor Gray
            Write-Host ""
            Write-Host "  Attends 10-30 min la propagation puis relance ce script." -ForegroundColor Yellow
            Write-Host "  Pour skip cette vérif : -SkipDnsCheck" -ForegroundColor Gray
            exit 1
        }
    } else {
        Warn "DNS check skipped"
    }

    # ── 2) Déploiement du code (git pull + rebuild frontend) ────
    if (-not $SkipDeploy) {
        Step "Déploiement du code à jour sur le VPS"
        Write-Host "  (mot de passe SSH demandé)" -ForegroundColor Gray
        & powershell -ExecutionPolicy Bypass -File (Join-Path $repoRoot "deploy\remote-deploy.ps1") -UpdateOnly
        if ($LASTEXITCODE -ne 0) {
            Err "Le déploiement a échoué"
            exit 1
        }
        Ok "Code déployé sur le VPS"
    } else {
        Warn "Deploy skipped"
    }

    # ── 3) Installation Umami sur le VPS ───────────────────────
    Step "Installation Umami sur le VPS via SSH"
    Write-Host "  (mot de passe SSH demandé)" -ForegroundColor Gray
    Write-Host ""

    $remoteScript = @"
set -e
cd /root/moalim

echo ''
echo '── Git pull (s''assurer d''avoir les scripts Umami) ──'
git pull origin main || true

echo ''
echo '── Lancement de install.sh ──'
cd deploy/umami
chmod +x install.sh

# On injecte 'y' automatiquement pour la question certbot
# puisqu'on a déjà vérifié le DNS côté Windows
yes y | ./install.sh
"@

    # Force LF line endings
    $remoteScript = $remoteScript -replace "`r`n", "`n"
    $remoteScript | ssh "$User@$ServerIp" "bash -s"

    if ($LASTEXITCODE -ne 0) {
        Err "L'installation Umami a échoué"
        Write-Host "  Logs : ssh $User@$ServerIp 'docker compose -f /root/moalim/deploy/umami/docker-compose.yml logs umami'" -ForegroundColor Gray
        exit 1
    }

    # ── 4) Récap & ouverture du dashboard ──────────────────────
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
    Write-Host "  ✅ UMAMI INSTALLÉ AVEC SUCCÈS" -ForegroundColor Green
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
    Write-Host ""
    Write-Host "  📊 Dashboard : https://$Domain" -ForegroundColor Cyan
    Write-Host "  👤 Login par défaut :" -ForegroundColor White
    Write-Host "     Username : admin" -ForegroundColor Gray
    Write-Host "     Password : umami" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  🚨 CHANGE LE MOT DE PASSE IMMÉDIATEMENT après login" -ForegroundColor Red
    Write-Host ""
    Write-Host "  Étapes suivantes :" -ForegroundColor White
    Write-Host "  1) Ouvre le dashboard (va s'ouvrir automatiquement)" -ForegroundColor Gray
    Write-Host "  2) Login → Profile → Change password" -ForegroundColor Gray
    Write-Host "  3) Settings → Websites → Add website" -ForegroundColor Gray
    Write-Host "       Name   : Moalim" -ForegroundColor Gray
    Write-Host "       Domain : moalim.online" -ForegroundColor Gray
    Write-Host "  4) Copie le 'Website ID' (UUID)" -ForegroundColor Gray
    Write-Host "  5) Lance : powershell .\deploy\umami\activate-tracking.ps1 -WebsiteId <UUID>" -ForegroundColor Yellow
    Write-Host ""

    # Ouvre le navigateur
    Start-Sleep -Seconds 2
    Start-Process "https://$Domain"

} finally {
    Pop-Location
}
