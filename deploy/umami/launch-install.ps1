# =============================================================
# Moalim - Installation Umami end-to-end depuis Windows
# Usage:
#   powershell -ExecutionPolicy Bypass -File deploy\umami\launch-install.ps1
# =============================================================

param(
    [string]$ServerIp = "87.106.1.128",
    [string]$User     = "root",
    [string]$Domain   = "analytics.moalim.online",
    [switch]$SkipDnsCheck,
    [switch]$SkipDeploy
)

$ErrorActionPreference = "Stop"

function Step($msg) { Write-Host ""; Write-Host ">> $msg" -ForegroundColor Cyan }
function Ok($msg)   { Write-Host "   [OK] $msg" -ForegroundColor Green }
function Warn($msg) { Write-Host "   [!] $msg" -ForegroundColor Yellow }
function Err($msg)  { Write-Host "   [X] $msg" -ForegroundColor Red }

$repoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Push-Location $repoRoot

try {
    Step "Verification des outils locaux"
    if (-not (Get-Command ssh -ErrorAction SilentlyContinue)) {
        Err "ssh introuvable. Installe OpenSSH Client (Settings > Apps > Optional Features)."
        exit 1
    }
    Ok "ssh OK"

    if (-not $SkipDnsCheck) {
        Step "Verification DNS pour $Domain"
        try {
            $result = Resolve-DnsName -Name $Domain -Type A -ErrorAction Stop
            $ip = ($result | Where-Object { $_.Type -eq 'A' } | Select-Object -First 1).IPAddress
            if ($ip -eq $ServerIp) {
                Ok "$Domain pointe vers $ip"
            } else {
                Warn "$Domain pointe vers $ip (attendu: $ServerIp)"
                $answer = Read-Host "   Continuer quand meme ? (y/N)"
                if ($answer -ne "y" -and $answer -ne "Y") { exit 1 }
            }
        } catch {
            Err "$Domain n'est pas resolu par DNS."
            Write-Host ""
            Write-Host "   Ajoute chez ton registrar:" -ForegroundColor Yellow
            Write-Host "     Type   : A" -ForegroundColor Gray
            Write-Host "     Nom    : analytics" -ForegroundColor Gray
            Write-Host "     Valeur : $ServerIp" -ForegroundColor Gray
            Write-Host "     TTL    : 3600" -ForegroundColor Gray
            Write-Host ""
            Write-Host "   Attends 10-30 min puis relance." -ForegroundColor Yellow
            Write-Host "   Pour skip: -SkipDnsCheck" -ForegroundColor Gray
            exit 1
        }
    } else {
        Warn "DNS check skipped"
    }

    if (-not $SkipDeploy) {
        Step "Deploiement du code a jour sur le VPS"
        Write-Host "   (mot de passe SSH demande)" -ForegroundColor Gray
        & powershell -ExecutionPolicy Bypass -File (Join-Path $repoRoot "deploy\remote-deploy.ps1") -UpdateOnly
        if ($LASTEXITCODE -ne 0) {
            Err "Le deploiement a echoue"
            exit 1
        }
        Ok "Code deploye sur le VPS"
    } else {
        Warn "Deploy skipped"
    }

    Step "Installation Umami sur le VPS via SSH"
    Write-Host "   (mot de passe SSH demande)" -ForegroundColor Gray
    Write-Host ""

    $remoteScript = @"
set -e
cd /root/moalim

echo ''
echo '-- Git pull (s'\''assurer d'\''avoir les scripts Umami) --'
git pull origin main || true

echo ''
echo '-- Lancement de install.sh --'
cd deploy/umami
chmod +x install.sh
yes y | ./install.sh
"@

    $remoteScript = $remoteScript -replace "`r`n", "`n"
    $remoteScript | ssh "$User@$ServerIp" "bash -s"

    if ($LASTEXITCODE -ne 0) {
        Err "L'installation Umami a echoue"
        Write-Host "   Logs: ssh $User@$ServerIp 'docker compose -f /root/moalim/deploy/umami/docker-compose.yml logs umami'" -ForegroundColor Gray
        exit 1
    }

    Write-Host ""
    Write-Host "===========================================================" -ForegroundColor Green
    Write-Host "  UMAMI INSTALLE AVEC SUCCES" -ForegroundColor Green
    Write-Host "===========================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "   Dashboard : https://$Domain" -ForegroundColor Cyan
    Write-Host "   Login par defaut:" -ForegroundColor White
    Write-Host "     Username : admin" -ForegroundColor Gray
    Write-Host "     Password : umami" -ForegroundColor Gray
    Write-Host ""
    Write-Host "   ATTENTION: change le mot de passe immediatement apres login" -ForegroundColor Red
    Write-Host ""
    Write-Host "   Etapes suivantes:" -ForegroundColor White
    Write-Host "   1. Ouvre le dashboard (va s'ouvrir automatiquement)" -ForegroundColor Gray
    Write-Host "   2. Login puis Profile, Change password" -ForegroundColor Gray
    Write-Host "   3. Settings, Websites, Add website" -ForegroundColor Gray
    Write-Host "        Name   : Moalim" -ForegroundColor Gray
    Write-Host "        Domain : moalim.online" -ForegroundColor Gray
    Write-Host "   4. Copie le Website ID (UUID)" -ForegroundColor Gray
    Write-Host "   5. Lance: powershell -File deploy\umami\activate-tracking.ps1 -WebsiteId UUID" -ForegroundColor Yellow
    Write-Host ""

    Start-Sleep -Seconds 2
    Start-Process "https://$Domain"

} finally {
    Pop-Location
}
