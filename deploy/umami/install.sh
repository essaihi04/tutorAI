#!/usr/bin/env bash
# =============================================================
# Moalim — Installation Umami Analytics sur le VPS
# À lancer depuis le dossier deploy/umami/ une fois sur le VPS :
#   chmod +x install.sh && sudo ./install.sh
# =============================================================
set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log()  { echo -e "${GREEN}▶${NC} $1"; }
warn() { echo -e "${YELLOW}⚠${NC} $1"; }
err()  { echo -e "${RED}✗${NC} $1"; exit 1; }

# ── Vérifie qu'on est root ──
if [[ $EUID -ne 0 ]]; then
   err "Ce script doit être lancé en root (sudo)."
fi

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# ── 1) Vérifier Docker ──
log "Vérification de Docker"
if ! command -v docker &> /dev/null; then
    warn "Docker non installé. Installation…"
    curl -fsSL https://get.docker.com | sh
    systemctl enable --now docker
fi

if ! docker compose version &> /dev/null; then
    err "Docker Compose v2 manquant. Installe-le avec : apt install docker-compose-plugin"
fi

log "Docker OK : $(docker --version)"

# ── 2) Générer le fichier .env si absent ──
if [[ ! -f .env ]]; then
    log "Génération du fichier .env (mots de passe aléatoires)"
    UMAMI_DB_PASSWORD=$(openssl rand -base64 24 | tr -d '/+=' | cut -c1-24)
    UMAMI_APP_SECRET=$(openssl rand -base64 48 | tr -d '/+=' | cut -c1-48)
    cat > .env <<EOF
# Umami secrets — générés le $(date)
UMAMI_DB_PASSWORD=${UMAMI_DB_PASSWORD}
UMAMI_APP_SECRET=${UMAMI_APP_SECRET}
EOF
    chmod 600 .env
    log "Fichier .env créé : $SCRIPT_DIR/.env (sauvegarde-le !)"
else
    log "Fichier .env existant — réutilisé"
fi

# ── 3) Lancer la stack Docker ──
log "Lancement de la stack Umami (peut prendre 1-2 min au premier run)"
docker compose --env-file .env up -d

# ── 4) Vérifier que Umami répond ──
log "Attente du démarrage de Umami…"
for i in {1..30}; do
    if curl -sf http://127.0.0.1:3001 > /dev/null 2>&1; then
        log "Umami est UP sur 127.0.0.1:3001 ✓"
        break
    fi
    if [[ $i -eq 30 ]]; then
        err "Umami n'a pas démarré après 30 essais. Vérifie : docker compose logs umami"
    fi
    sleep 2
done

# ── 5) Configurer nginx ──
log "Installation de la config nginx"
cp nginx-analytics.conf /etc/nginx/conf.d/moalim-analytics.conf

# Test syntaxe nginx
if ! nginx -t 2>&1; then
    err "Erreur de syntaxe nginx. Restaure /etc/nginx/conf.d/moalim-analytics.conf manuellement."
fi

# ── 6) Obtenir le certificat SSL ──
log "Demande du certificat SSL Let's Encrypt pour analytics.moalim.online"
warn "ASSURE-TOI que le DNS analytics.moalim.online → IP de ce VPS est déjà propagé !"
echo ""
read -p "Le DNS est-il configuré et propagé ? (vérifie avec : dig analytics.moalim.online) [y/N] " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    warn "Setup SSL ignoré. Lance plus tard :"
    echo "  certbot --nginx -d analytics.moalim.online"
    echo ""
    log "Installation Umami terminée (sans HTTPS pour l'instant)."
    exit 0
fi

certbot --nginx -d analytics.moalim.online --non-interactive --agree-tos --email contact@moalim.online --redirect

# ── 7) Reload nginx ──
log "Reload nginx"
systemctl reload nginx

# ── 8) Récap ──
echo ""
echo "════════════════════════════════════════════════════════════"
log "✅ Umami installé avec succès !"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "  📊 Accès admin     : https://analytics.moalim.online"
echo "  👤 Login par défaut : admin / umami"
echo ""
echo "  ⚠️  CHANGE LE MOT DE PASSE IMMÉDIATEMENT après ton premier login."
echo ""
echo "  Étapes suivantes :"
echo "  1) Login → Profile → Change password"
echo "  2) Settings → Websites → Add website"
echo "       Name : Moalim"
echo "       Domain : moalim.online"
echo "  3) Copie le 'Website ID' (UUID) qui s'affiche"
echo "  4) Communique cet ID à Cascade pour qu'il l'injecte dans le frontend"
echo ""
echo "  📁 Fichiers importants :"
echo "  - $SCRIPT_DIR/.env         (mots de passe — SAUVEGARDE-LE)"
echo "  - $SCRIPT_DIR/docker-compose.yml"
echo "  - /etc/nginx/conf.d/moalim-analytics.conf"
echo ""
echo "  🛠️  Commandes utiles :"
echo "  - Logs Umami     : docker compose -f $SCRIPT_DIR/docker-compose.yml logs -f umami"
echo "  - Redémarrer     : docker compose -f $SCRIPT_DIR/docker-compose.yml restart"
echo "  - Backup DB      : docker exec moalim-umami-db pg_dump -U umami umami > backup.sql"
echo ""
