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

# Détection de la distribution
if [[ -f /etc/os-release ]]; then
    . /etc/os-release
    DISTRO_ID="${ID:-unknown}"
    DISTRO_LIKE="${ID_LIKE:-}"
else
    DISTRO_ID="unknown"
    DISTRO_LIKE=""
fi
log "Distribution détectée : $DISTRO_ID"

if ! command -v docker &> /dev/null; then
    warn "Docker non installé. Installation…"
    case "$DISTRO_ID" in
        almalinux|rocky|centos|rhel|ol)
            # RHEL family : utilise le repo Docker CE officiel pour CentOS
            dnf install -y dnf-plugins-core
            dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
            dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
            ;;
        ubuntu|debian)
            curl -fsSL https://get.docker.com | sh
            ;;
        *)
            # Fallback : essaye get.docker.com, sinon tente le repo CentOS si ID_LIKE contient rhel
            if [[ "$DISTRO_LIKE" == *"rhel"* || "$DISTRO_LIKE" == *"fedora"* ]]; then
                dnf install -y dnf-plugins-core
                dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
                dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
            else
                curl -fsSL https://get.docker.com | sh
            fi
            ;;
    esac
    systemctl enable --now docker
fi

if ! docker compose version &> /dev/null; then
    warn "Docker Compose v2 manquant. Installation du plugin…"
    case "$DISTRO_ID" in
        almalinux|rocky|centos|rhel|ol)
            dnf install -y docker-compose-plugin
            ;;
        ubuntu|debian)
            apt install -y docker-compose-plugin
            ;;
    esac
fi

if ! docker compose version &> /dev/null; then
    err "Docker Compose v2 toujours manquant. Vérifie l'installation."
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

# S'assure que certbot est installé
if ! command -v certbot &> /dev/null; then
    warn "certbot non installé. Installation…"
    case "$DISTRO_ID" in
        almalinux|rocky|centos|rhel|ol)
            dnf install -y epel-release
            dnf install -y certbot python3-certbot-nginx
            ;;
        ubuntu|debian)
            apt install -y certbot python3-certbot-nginx
            ;;
        *)
            if [[ "$DISTRO_LIKE" == *"rhel"* || "$DISTRO_LIKE" == *"fedora"* ]]; then
                dnf install -y epel-release
                dnf install -y certbot python3-certbot-nginx
            else
                apt install -y certbot python3-certbot-nginx || true
            fi
            ;;
    esac
fi

# Ouvre les ports 80/443 si firewalld est actif
if systemctl is-active --quiet firewalld 2>/dev/null; then
    log "Ouverture des ports 80/443 dans firewalld"
    firewall-cmd --permanent --add-service=http  2>/dev/null || true
    firewall-cmd --permanent --add-service=https 2>/dev/null || true
    firewall-cmd --reload 2>/dev/null || true
fi

# Étape 5a : déploie une config HTTP-only temporaire pour permettre le challenge ACME
CERT_PATH="/etc/letsencrypt/live/analytics.moalim.online/fullchain.pem"
NGINX_CONF="/etc/nginx/conf.d/moalim-analytics.conf"

if [[ ! -f "$CERT_PATH" ]]; then
    log "Certificat SSL absent — deploiement d'une config HTTP-only pour le challenge ACME"
    mkdir -p /var/www/certbot
    cat > "$NGINX_CONF" <<'EONGINX'
server {
    listen 80;
    listen [::]:80;
    server_name analytics.moalim.online;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 200 'Umami bootstrap - SSL pending';
        add_header Content-Type text/plain;
    }
}
EONGINX

    if ! nginx -t 2>&1; then
        err "Erreur syntaxe nginx (bootstrap HTTP). Aborting."
    fi
    systemctl reload nginx || systemctl start nginx

    # ── 6a) Demande du certificat via webroot ──
    log "Demande du certificat SSL Let's Encrypt (webroot challenge)"
    certbot certonly --webroot -w /var/www/certbot \
        -d analytics.moalim.online \
        --non-interactive --agree-tos \
        --email contact@moalim.online \
        || err "Echec certbot. Verifie que analytics.moalim.online pointe vers ce VPS (DNS propage)."

    # S'assure que les options SSL recommandees existent
    if [[ ! -f /etc/letsencrypt/options-ssl-nginx.conf ]]; then
        curl -fsSL https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf \
             -o /etc/letsencrypt/options-ssl-nginx.conf
    fi
    if [[ ! -f /etc/letsencrypt/ssl-dhparams.pem ]]; then
        log "Generation des parametres DH (peut prendre 1-2 min)..."
        openssl dhparam -out /etc/letsencrypt/ssl-dhparams.pem 2048
    fi
else
    log "Certificat SSL deja present — skip certbot"
fi

# ── 5b) Deploie la config HTTPS finale ──
log "Deploiement de la config HTTPS finale"
cp nginx-analytics.conf "$NGINX_CONF"

if ! nginx -t 2>&1; then
    err "Erreur syntaxe nginx (HTTPS). Inspecte $NGINX_CONF"
fi

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
