#!/usr/bin/env bash
# =============================================================
# Moalim — déploiement natif AlmaLinux 9 / RHEL 9
# ISOLATION TOTALE — ne touche jamais aux autres apps du serveur.
#
# Usage:
#   ssh root@87.106.1.128
#   cd /root/moalim
#   bash deploy/deploy.sh
# =============================================================

set -euo pipefail

# ── Paramètres uniques pour Moalim ─────────────────────────────────
DOMAIN="moalim.online"
EMAIL="contact@moalim.online"
APP_DIR="/root/moalim"
WEB_DIR="/var/www/moalim"
BACKEND_PORT="8000"
SERVICE_NAME="moalim-backend"
NGINX_CONF="/etc/nginx/conf.d/moalim.conf"
REPO_URL="https://github.com/essaihi04/tutorAI.git"
BRANCH="main"
PY_BIN="python3.12"

log()  { echo -e "\n\033[1;36m▶ $*\033[0m"; }
warn() { echo -e "\033[1;33m⚠ $*\033[0m"; }
err()  { echo -e "\033[1;31m✖ $*\033[0m"; }

# ── 0. Vérifications préalables ────────────────────────────────────
log "Vérification de l'environnement"
if ! grep -qi "almalinux\|rhel\|rocky\|centos" /etc/os-release; then
    warn "Cet OS n'est pas RHEL/AlmaLinux. Le script peut nécessiter des adaptations."
fi

# Vérifier que le port backend est libre (n'écrase aucune autre app)
if ss -ltnp | grep -q ":${BACKEND_PORT}\b"; then
    err "Le port ${BACKEND_PORT} est déjà utilisé par une autre app !"
    ss -ltnp | grep ":${BACKEND_PORT}\b" || true
    err "Modifie BACKEND_PORT dans ce script (et dans nginx.conf + service) puis relance."
    exit 1
fi

# ── 1. Repos & paquets système ─────────────────────────────────────
log "Activation des dépôts EPEL et CodeReady Builder"
dnf install -y epel-release || true
dnf config-manager --set-enabled crb 2>/dev/null || \
    dnf config-manager --enable powertools 2>/dev/null || true

log "Installation des paquets de base"
dnf install -y \
    git curl wget tar gcc gcc-c++ make pkgconfig \
    libpq-devel openssl-devel libffi-devel \
    libjpeg-turbo-devel zlib-devel \
    poppler-utils \
    nginx redis \
    policycoreutils-python-utils

# Python 3.12 (disponible directement dans AlmaLinux 9)
log "Installation de Python 3.12"
dnf install -y python3.12 python3.12-devel python3.12-pip || {
    warn "python3.12 non dispo, tentative via dnf module"
    dnf module install -y python3.12 || true
}

# Node.js 20 LTS depuis NodeSource (n'affecte que ce serveur globalement, OK)
if ! command -v node >/dev/null 2>&1 || [[ "$(node -v 2>/dev/null)" != v20* ]]; then
    log "Installation de Node.js 20 LTS"
    curl -fsSL https://rpm.nodesource.com/setup_20.x | bash -
    dnf install -y nodejs
fi

# certbot pour SSL (via EPEL)
log "Installation de certbot"
dnf install -y certbot python3-certbot-nginx

# ── 2. Redis (peut déjà être actif pour une autre app — on le réutilise) ──
log "Activation de Redis (DB 0 partagée si déjà en service)"
systemctl enable --now redis || systemctl enable --now redis-server || true

# ── 3. SELinux : autoriser Nginx à se connecter au backend ─────────
log "Configuration SELinux pour Nginx → backend"
setsebool -P httpd_can_network_connect 1 || warn "setsebool a échoué (SELinux désactivé ?)"
# Autoriser Nginx à servir /var/www/moalim
mkdir -p "$WEB_DIR"
chcon -R -t httpd_sys_content_t "$WEB_DIR" 2>/dev/null || true

# ── 4. Code source ──────────────────────────────────────────────────
log "Récupération du code source dans $APP_DIR"
mkdir -p "$APP_DIR"
if [ -d "$APP_DIR/.git" ]; then
    cd "$APP_DIR"
    git fetch --all
    git reset --hard "origin/$BRANCH"
else
    git clone -b "$BRANCH" "$REPO_URL" "$APP_DIR"
fi

# ── 5. Backend Python ──────────────────────────────────────────────
log "Création du venv Python et installation des dépendances"
cd "$APP_DIR/backend"
if [ ! -d .venv ]; then
    $PY_BIN -m venv .venv
fi
.venv/bin/pip install --upgrade pip wheel setuptools
.venv/bin/pip install -r requirements.txt

# ── 6. Backend .env ────────────────────────────────────────────────
if [ ! -f "$APP_DIR/backend/.env" ]; then
    if [ -f "$APP_DIR/deploy/backend.env" ]; then
        log "Copie de deploy/backend.env vers backend/.env"
        cp "$APP_DIR/deploy/backend.env" "$APP_DIR/backend/.env"
    else
        err "Aucun fichier .env trouvé !"
        err "Copie ton fichier backend.env vers $APP_DIR/backend/.env puis relance."
        exit 1
    fi
fi
chmod 600 "$APP_DIR/backend/.env"

# ── 7. Frontend build + copie isolée ───────────────────────────────
log "Build du frontend Vite (mode prod, sans check TS strict)"
cd "$APP_DIR/frontend"
if [ -f package-lock.json ]; then
    npm ci
else
    npm install
fi
npm run build:prod

log "Déploiement du frontend dans $WEB_DIR (isolé)"
mkdir -p "$WEB_DIR"
rm -rf "$WEB_DIR/assets"
cp "$APP_DIR/frontend/dist/index.html" "$WEB_DIR/index.html"
cp -r "$APP_DIR/frontend/dist/assets" "$WEB_DIR/assets"
find "$APP_DIR/frontend/dist" -maxdepth 1 -type f ! -name 'index.html' \
    -exec cp {} "$WEB_DIR/" \;
chown -R nginx:nginx "$WEB_DIR"
chcon -R -t httpd_sys_content_t "$WEB_DIR" 2>/dev/null || true

# ── 8. Service systemd dédié ───────────────────────────────────────
log "Installation du service systemd $SERVICE_NAME"
cp "$APP_DIR/deploy/moalim-backend.service" "/etc/systemd/system/${SERVICE_NAME}.service"
systemctl daemon-reload
systemctl enable "$SERVICE_NAME"
systemctl restart "$SERVICE_NAME"
sleep 3
if ! systemctl is-active --quiet "$SERVICE_NAME"; then
    err "Le service $SERVICE_NAME n'a pas démarré. Logs :"
    journalctl -u "$SERVICE_NAME" -n 30 --no-pager
    exit 1
fi
log "Service $SERVICE_NAME actif ✓"

# Vérifier que le backend répond localement
log "Vérification du backend (curl http://127.0.0.1:${BACKEND_PORT}/health)"
sleep 2
if curl -sf "http://127.0.0.1:${BACKEND_PORT}/health" >/dev/null; then
    log "Backend répond ✓"
else
    warn "Backend ne répond pas encore — peut prendre quelques secondes au premier démarrage"
fi

# ── 9. Nginx (config dédiée, ne touche aux autres sites) ───────────
log "Installation du fichier Nginx isolé : $NGINX_CONF"
cp "$APP_DIR/deploy/nginx.conf" "$NGINX_CONF"
nginx -t

# ── 10. Certificat SSL Let's Encrypt ───────────────────────────────
if [ ! -d "/etc/letsencrypt/live/$DOMAIN" ]; then
    log "Émission du certificat SSL pour $DOMAIN"
    # Phase 1 : config HTTP only pour valider l'ACME challenge
    cat > "$NGINX_CONF" <<EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }
    location / { return 200 'Moalim deployment in progress'; add_header Content-Type text/plain; }
}
EOF
    mkdir -p /var/www/certbot
    nginx -t && systemctl reload nginx

    certbot certonly --webroot -w /var/www/certbot \
        -d "$DOMAIN" -d "www.$DOMAIN" \
        --email "$EMAIL" --agree-tos --non-interactive --no-eff-email

    # Phase 2 : remettre la config HTTPS finale
    cp "$APP_DIR/deploy/nginx.conf" "$NGINX_CONF"
fi

nginx -t && systemctl reload nginx

# Auto-renew (timer systemd)
systemctl enable --now certbot-renew.timer 2>/dev/null || \
    systemctl enable --now certbot.timer 2>/dev/null || true

# ── 11. Firewall (firewalld — ajoute juste ce qu'il faut) ──────────
if systemctl is-active --quiet firewalld; then
    log "Configuration firewalld (ajoute http/https s'ils manquent)"
    firewall-cmd --permanent --add-service=http  2>/dev/null || true
    firewall-cmd --permanent --add-service=https 2>/dev/null || true
    firewall-cmd --reload 2>/dev/null || true
fi

# ── 12. Récap ──────────────────────────────────────────────────────
log "✅ Déploiement Moalim terminé."
echo
echo "  Code source     : $APP_DIR"
echo "  Static frontend : $WEB_DIR"
echo "  Backend service : $SERVICE_NAME (port 127.0.0.1:$BACKEND_PORT)"
echo "  Nginx config    : $NGINX_CONF"
echo "  Domaine         : https://$DOMAIN"
echo
echo "  Logs backend    : journalctl -u $SERVICE_NAME -f"
echo "  Logs nginx      : tail -f /var/log/nginx/{access,error}.log"
echo "  Mise à jour     : bash $APP_DIR/deploy/update.sh"
echo
