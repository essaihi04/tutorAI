#!/usr/bin/env bash
# =============================================================
# Moalim — update script (run after first deploy.sh)
# Pulls latest code, rebuilds frontend, reinstalls backend deps,
# and reloads services.
#
# Usage:  bash /var/www/moalim/deploy/update.sh
# =============================================================

set -euo pipefail

APP_DIR="/var/www/moalim"
BRANCH="main"

log() { echo -e "\n\033[1;36m▶ $*\033[0m"; }

cd "$APP_DIR"

log "Pull du dernier code"
sudo -u www-data git fetch --all
sudo -u www-data git reset --hard "origin/$BRANCH"

log "Mise à jour des dépendances Python"
cd "$APP_DIR/backend"
sudo -u www-data .venv/bin/pip install -r requirements.txt

log "Rebuild du frontend"
cd "$APP_DIR/frontend"
sudo -u www-data npm ci
sudo -u www-data npm run build

log "Redémarrage du backend"
systemctl restart moalim-backend
sleep 2
systemctl status moalim-backend --no-pager | head -n 10

log "Reload de Nginx"
nginx -t && systemctl reload nginx

log "✅ Mise à jour terminée."
