#!/usr/bin/env bash
# =============================================================
# Moalim — déploiement natif Ubuntu 24.04 (VPS 217.160.128.247)
# Équivalent Ubuntu de deploy.sh (AlmaLinux) ; rejouable.
#
# Pré-requis (envoyés depuis le PC, hors Git) :
#   /etc/moalim/backend.env                      secrets de prod (SUPABASE_URL=https://sb.moalim.online)
#   backend/data/rag_cache/, tts_cache/          index RAG + voix déjà générées
#   cours 2bac pc/cadres de references 2BAC PC/*.json
#   frontend/.env.production
#
# Usage : bash /opt/moalim/deploy/deploy-ubuntu.sh
#
# Tant que /etc/letsencrypt/live/moalim.online n'existe pas, nginx sert le
# site en HTTP (domaine + IP) pour tester avant la bascule DNS. Ensuite :
#   certbot certonly --webroot -w /var/www/certbot -d moalim.online -d www.moalim.online
#   puis relancer ce script (il installe alors deploy/nginx.conf, HTTPS).
# =============================================================
set -euo pipefail

DOMAIN="moalim.online"
APP_DIR="/opt/moalim"
WEB_DIR="/var/www/moalim"
ENV_FILE="/etc/moalim/backend.env"
SERVICE_NAME="moalim-backend"
SERVICE_USER="moalim"
NGINX_CONF="/etc/nginx/conf.d/moalim.conf"
BRANCH="main"

log()  { echo -e "\n\033[1;36m▶ $*\033[0m"; }
warn() { echo -e "\033[1;33m⚠ $*\033[0m"; }
err()  { echo -e "\033[1;31m✖ $*\033[0m"; exit 1; }

[[ $EUID -eq 0 ]] || err "À lancer en root."
[[ -f "$ENV_FILE" ]] || err "$ENV_FILE absent — envoie deploy/backend.env depuis le PC."
grep -q '^SUPABASE_URL=https://sb\.moalim\.online' "$ENV_FILE" \
    || warn "SUPABASE_URL ne pointe pas vers https://sb.moalim.online dans $ENV_FILE"

# ── 1. Paquets système ──
log "Paquets système"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq \
    git curl rsync build-essential pkg-config \
    python3.12 python3.12-venv python3.12-dev \
    libpq-dev libffi-dev libssl-dev libjpeg-dev zlib1g-dev \
    poppler-utils redis-server nginx > /dev/null

if ! command -v node > /dev/null || [[ "$(node -v)" != v20* ]]; then
    log "Node.js 20 LTS"
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - > /dev/null
    apt-get install -y -qq nodejs > /dev/null
fi
systemctl enable --now redis-server > /dev/null

# ── 2. Utilisateur dédié ──
if ! id "$SERVICE_USER" &> /dev/null; then
    log "Création de l'utilisateur système $SERVICE_USER"
    useradd --system --home /var/lib/moalim --shell /usr/sbin/nologin "$SERVICE_USER"
fi
install -d -o "$SERVICE_USER" -g "$SERVICE_USER" /var/lib/moalim /var/cache/moalim
chown root:"$SERVICE_USER" "$ENV_FILE"
chmod 640 "$ENV_FILE"

# ── 3. Code ──
log "Code source ($BRANCH)"
if [[ -d "$APP_DIR/.git" ]]; then
    git -C "$APP_DIR" fetch -q origin
    git -C "$APP_DIR" reset -q --hard "origin/$BRANCH"   # garde les fichiers non suivis (caches, secrets)
else
    git clone -q -b "$BRANCH" https://github.com/essaihi04/tutorAI.git "$APP_DIR"
fi
git -C "$APP_DIR" log --oneline -1

# ── 4. Backend Python ──
log "Dépendances Python (premier run : 5-10 min)"
cd "$APP_DIR/backend"
[[ -d .venv ]] || python3.12 -m venv .venv
.venv/bin/pip install -q --upgrade pip wheel setuptools
# PyTorch CPU d'abord : la roue PyPI par défaut tire ~3 Go de CUDA inutile ici
.venv/bin/pip install -q torch --index-url https://download.pytorch.org/whl/cpu
.venv/bin/pip install -q -r requirements.txt

# Le service écrit uniquement dans data/ et frontend/public (cf. ReadWritePaths)
chown -R "$SERVICE_USER":"$SERVICE_USER" "$APP_DIR/backend/data" "$APP_DIR/frontend/public"

# ── 5. Frontend ──
log "Build du frontend"
cd "$APP_DIR/frontend"
npm ci --no-audit --no-fund --loglevel=error
npm run build:prod
mkdir -p "$WEB_DIR"
rm -rf "$WEB_DIR/assets" "$WEB_DIR/blog"
cp -r "$APP_DIR/frontend/dist/." "$WEB_DIR/"

# ── 6. Service systemd ──
log "Service $SERVICE_NAME"
sed "s#/root/moalim#${APP_DIR}#g" "$APP_DIR/deploy/moalim-backend.service" \
    > "/etc/systemd/system/${SERVICE_NAME}.service"
systemctl daemon-reload
systemctl enable -q "$SERVICE_NAME"
systemctl restart "$SERVICE_NAME"

log "Attente du backend (chargement du modèle RAG)…"
for i in {1..60}; do
    curl -sf http://127.0.0.1:8000/health > /dev/null && { log "Backend répond ✓"; break; }
    if ! systemctl is-active --quiet "$SERVICE_NAME"; then
        journalctl -u "$SERVICE_NAME" -n 40 --no-pager
        err "$SERVICE_NAME s'est arrêté."
    fi
    [[ $i -eq 60 ]] && { journalctl -u "$SERVICE_NAME" -n 40 --no-pager; err "Pas de réponse sur /health après 5 min."; }
    sleep 5
done

# ── 7. Nginx ──
mkdir -p /var/www/certbot
if [[ -f "/etc/letsencrypt/live/${DOMAIN}/fullchain.pem" ]]; then
    log "Nginx HTTPS (certificat présent)"
    cp "$APP_DIR/deploy/nginx.conf" "$NGINX_CONF"
else
    # Même config que la prod, servie en HTTP sur le domaine ET l'IP publique,
    # avec le challenge ACME pour pouvoir émettre le certificat après bascule DNS.
    PUBLIC_IP=$(curl -s4 --max-time 5 https://api.ipify.org || hostname -I | awk '{print $1}')
    log "Nginx HTTP provisoire (pas encore de certificat) — test : http://${PUBLIC_IP}"
    sed -e '/# ── HTTP → HTTPS redirect/,/^}/d' \
        -e 's/listen 443 ssl http2;/listen 80 default_server;/' \
        -e 's/listen \[::\]:443 ssl http2;/listen [::]:80 default_server;/' \
        -e '/ssl_certificate/d; /options-ssl-nginx/d; /ssl_dhparam/d; /Strict-Transport-Security/d' \
        -e "s/server_name ${DOMAIN} www.${DOMAIN};/server_name ${DOMAIN} www.${DOMAIN} ${PUBLIC_IP};\n\n    location \/.well-known\/acme-challenge\/ { root \/var\/www\/certbot; }/" \
        "$APP_DIR/deploy/nginx.conf" > "$NGINX_CONF"
    rm -f /etc/nginx/sites-enabled/default
fi
nginx -t
systemctl reload nginx

log "✅ Moalim déployé"
echo "  Code     : $APP_DIR ($(git -C "$APP_DIR" log --oneline -1))"
echo "  Frontend : $WEB_DIR"
echo "  Backend  : $SERVICE_NAME → 127.0.0.1:8000  (journalctl -u $SERVICE_NAME -f)"
echo "  Nginx    : $NGINX_CONF"
