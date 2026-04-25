#!/usr/bin/env bash
# =============================================================
# Moalim — update script (run after first deploy.sh)
# Pulls latest code, rebuilds frontend, reinstalls backend deps,
# and reloads services.
#
# Usage:  bash /var/www/moalim/deploy/update.sh
# =============================================================

set -euo pipefail

APP_DIR="/root/moalim"
WEB_DIR="/var/www/moalim"
BRANCH="main"

log() { echo -e "\n\033[1;36m▶ $*\033[0m"; }

cd "$APP_DIR"

log "Pull du dernier code"
git fetch --all
git reset --hard "origin/$BRANCH"

log "Mise à jour des dépendances Python"
cd "$APP_DIR/backend"
.venv/bin/pip install -r requirements.txt

log "Rebuild du frontend"
cd "$APP_DIR/frontend"
npm ci
npm run build

log "Déploiement vers $WEB_DIR"
rm -rf "$WEB_DIR/assets"
cp "$APP_DIR/frontend/dist/index.html" "$WEB_DIR/index.html"
cp -r "$APP_DIR/frontend/dist/assets" "$WEB_DIR/assets"
find "$APP_DIR/frontend/dist" -maxdepth 1 -type f ! -name 'index.html' -exec cp {} "$WEB_DIR/" \;
chown -R www-data:www-data "$WEB_DIR"

log "Redémarrage du backend"
systemctl restart moalim-backend
sleep 2
systemctl status moalim-backend --no-pager | head -n 10

log "Reload de Nginx"
nginx -t && systemctl reload nginx

log "✅ Mise à jour terminée."
