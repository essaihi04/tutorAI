#!/usr/bin/env bash
# =============================================================
# Moalim — first-time deployment script for Ubuntu/Debian VPS
# Run as root on the VPS:
#   ssh root@87.106.1.128
#   bash deploy.sh
# =============================================================

set -euo pipefail

DOMAIN="moalim.online"
EMAIL="contact@moalim.online"          # used by certbot — change if needed
APP_DIR="/var/www/moalim"
REPO_URL="https://github.com/essaihi04/tutorAI.git"
BRANCH="main"
PY_BIN="python3.12"

log() { echo -e "\n\033[1;36m▶ $*\033[0m"; }

# ── 1. System packages ──────────────────────────────────────────────
log "Mise à jour du système et installation des paquets"
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get upgrade -y
apt-get install -y \
    curl wget git build-essential pkg-config \
    python3.12 python3.12-venv python3.12-dev \
    nginx certbot python3-certbot-nginx \
    redis-server \
    libpq-dev libjpeg-dev zlib1g-dev libffi-dev \
    poppler-utils \
    ufw

# ── 2. Node.js 20 ───────────────────────────────────────────────────
if ! command -v node >/dev/null 2>&1 || [[ "$(node -v)" != v20* ]]; then
    log "Installation de Node.js 20 LTS"
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
    apt-get install -y nodejs
fi

# ── 3. Firewall ─────────────────────────────────────────────────────
log "Configuration du pare-feu UFW"
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw --force enable

# ── 4. Redis ────────────────────────────────────────────────────────
log "Activation de Redis"
systemctl enable --now redis-server

# ── 5. Code source ──────────────────────────────────────────────────
log "Récupération du code source"
mkdir -p "$APP_DIR"
if [ -d "$APP_DIR/.git" ]; then
    cd "$APP_DIR" && git fetch --all && git reset --hard "origin/$BRANCH"
else
    git clone -b "$BRANCH" "$REPO_URL" "$APP_DIR"
fi
chown -R www-data:www-data "$APP_DIR"

# ── 6. Backend Python venv + deps ───────────────────────────────────
log "Installation du backend Python"
cd "$APP_DIR/backend"
sudo -u www-data $PY_BIN -m venv .venv
sudo -u www-data .venv/bin/pip install --upgrade pip wheel setuptools
sudo -u www-data .venv/bin/pip install -r requirements.txt
sudo -u www-data .venv/bin/pip install gunicorn

# ── 7. Backend .env ─────────────────────────────────────────────────
if [ ! -f "$APP_DIR/backend/.env" ]; then
    log "Copie du fichier .env (à compléter manuellement si besoin)"
    cp "$APP_DIR/deploy/backend.env" "$APP_DIR/backend/.env"
    chown www-data:www-data "$APP_DIR/backend/.env"
    chmod 600 "$APP_DIR/backend/.env"
fi

# ── 8. Frontend build ───────────────────────────────────────────────
log "Build du frontend Vite"
cd "$APP_DIR/frontend"
sudo -u www-data npm ci
sudo -u www-data npm run build
chown -R www-data:www-data "$APP_DIR/frontend/dist"

# ── 9. systemd service ──────────────────────────────────────────────
log "Installation du service systemd"
cp "$APP_DIR/deploy/moalim-backend.service" /etc/systemd/system/moalim-backend.service
systemctl daemon-reload
systemctl enable moalim-backend
systemctl restart moalim-backend
sleep 3
systemctl status moalim-backend --no-pager || true

# ── 10. Nginx ───────────────────────────────────────────────────────
log "Configuration Nginx"
mkdir -p /var/www/certbot
cp "$APP_DIR/deploy/nginx.conf" /etc/nginx/sites-available/moalim
ln -sf /etc/nginx/sites-available/moalim /etc/nginx/sites-enabled/moalim
rm -f /etc/nginx/sites-enabled/default

# Temporary HTTP-only config so certbot can issue cert
cat > /etc/nginx/sites-available/moalim-http <<EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    location /.well-known/acme-challenge/ { root /var/www/certbot; }
    location / { return 200 'Moalim deployment in progress'; add_header Content-Type text/plain; }
}
EOF
rm -f /etc/nginx/sites-enabled/moalim
ln -sf /etc/nginx/sites-available/moalim-http /etc/nginx/sites-enabled/moalim-http
nginx -t && systemctl reload nginx

# ── 11. SSL via certbot ─────────────────────────────────────────────
log "Émission du certificat SSL Let's Encrypt"
if [ ! -d "/etc/letsencrypt/live/$DOMAIN" ]; then
    certbot certonly --webroot -w /var/www/certbot \
        -d "$DOMAIN" -d "www.$DOMAIN" \
        --email "$EMAIL" --agree-tos --non-interactive --no-eff-email
fi

# Switch to full HTTPS config
rm -f /etc/nginx/sites-enabled/moalim-http
ln -sf /etc/nginx/sites-available/moalim /etc/nginx/sites-enabled/moalim
nginx -t && systemctl reload nginx

# Auto-renew (already a systemd timer, just verify)
systemctl enable --now certbot.timer

log "✅ Déploiement terminé."
echo
echo "  Site     : https://$DOMAIN"
echo "  Health   : https://$DOMAIN/health"
echo "  Logs     : journalctl -u moalim-backend -f"
echo "  Nginx    : journalctl -u nginx -f"
echo
