#!/usr/bin/env bash
# =============================================================
# Moalim — mise à jour rapide (après deploy.sh initial)
# Ne touche QUE Moalim. Aucun autre service du serveur n'est impacté.
#
# Usage:  bash /root/moalim/deploy/update.sh
# =============================================================

set -euo pipefail

APP_DIR="/root/moalim"
WEB_DIR="/var/www/moalim"
SERVICE_NAME="moalim-backend"
BRANCH="main"

log() { echo -e "\n\033[1;36m▶ $*\033[0m"; }

cd "$APP_DIR"

log "Pull du dernier code"
git fetch --all
git reset --hard "origin/$BRANCH"

log "Mise à jour des dépendances Python (si requirements.txt a changé)"
cd "$APP_DIR/backend"
.venv/bin/pip install -q -r requirements.txt

log "Rebuild du frontend (mode prod)"
cd "$APP_DIR/frontend"
if [ -f package-lock.json ]; then
    npm ci
else
    npm install
fi
npm run build:prod

log "Déploiement du build vers $WEB_DIR (isolé)"
rm -rf "$WEB_DIR/assets"
cp "$APP_DIR/frontend/dist/index.html" "$WEB_DIR/index.html"
cp -r "$APP_DIR/frontend/dist/assets" "$WEB_DIR/assets"
find "$APP_DIR/frontend/dist" -maxdepth 1 -type f ! -name 'index.html' \
    -exec cp {} "$WEB_DIR/" \;
chown -R nginx:nginx "$WEB_DIR"
chcon -R -t httpd_sys_content_t "$WEB_DIR" 2>/dev/null || true

log "Redémarrage du service backend"
systemctl restart "$SERVICE_NAME"
sleep 2
systemctl is-active --quiet "$SERVICE_NAME" && echo "  $SERVICE_NAME actif ✓" || {
    echo "  $SERVICE_NAME en erreur — voir : journalctl -u $SERVICE_NAME -n 30"
    exit 1
}

log "Reload Nginx (sans toucher aux autres sites)"
nginx -t && systemctl reload nginx

log "✅ Mise à jour Moalim terminée."
