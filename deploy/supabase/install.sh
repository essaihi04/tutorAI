#!/usr/bin/env bash
# =============================================================
# Moalim — Installation de Supabase auto-hébergé sur le VPS
# À lancer depuis deploy/supabase/ une fois sur le VPS :
#   cp secrets.env.example secrets.env   # puis remplir
#   chmod +x *.sh && sudo ./install.sh
#
# Résultat :
#   /opt/supabase               stack Docker officielle (version figée)
#   127.0.0.1:54321             API Supabase (Kong) — jamais exposée
#   https://sb.moalim.online    fichiers publics du Storage uniquement
# Le script est rejouable : .env et données existants sont conservés.
# =============================================================
set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log()  { echo -e "${GREEN}▶${NC} $1"; }
warn() { echo -e "${YELLOW}⚠${NC} $1"; }
err()  { echo -e "${RED}✗${NC} $1"; exit 1; }

SUPABASE_VERSION="v1.26.08"          # tag du repo supabase/supabase (dossier docker/)
SB_DIR="/opt/supabase"
SB_DOMAIN="${SB_DOMAIN:-sb.moalim.online}"
SITE_URL="${SITE_URL:-https://moalim.online}"
KONG_PORT=54321
CERT_EMAIL="${CERT_EMAIL:-contact@moalim.online}"

if [[ $EUID -ne 0 ]]; then
   err "Ce script doit être lancé en root (sudo)."
fi

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# ── 0) Secrets de l'ancien projet ──
[[ -f secrets.env ]] || err "secrets.env absent. Copie secrets.env.example → secrets.env et remplis-le."
# shellcheck disable=SC1091
source secrets.env
[[ -n "${JWT_SECRET:-}" && -n "${ANON_KEY:-}" && -n "${SERVICE_ROLE_KEY:-}" ]] \
    || err "JWT_SECRET, ANON_KEY et SERVICE_ROLE_KEY doivent être remplis dans secrets.env."

# Vérifie que la clé service_role est bien signée par ce secret (sinon tout le backend casse)
b64url() { openssl base64 -A | tr '+/' '-_' | tr -d '='; }
SIG=$(printf %s "${SERVICE_ROLE_KEY%.*}" | openssl dgst -sha256 -hmac "$JWT_SECRET" -binary | b64url)
[[ "$SIG" == "${SERVICE_ROLE_KEY##*.}" ]] || err "SERVICE_ROLE_KEY n'est pas signée par JWT_SECRET — mauvaise paire de secrets."
log "Secrets de l'ancien projet vérifiés"

# ── 1) Docker ──
log "Vérification de Docker"
. /etc/os-release
DISTRO_ID="${ID:-unknown}"
DISTRO_LIKE="${ID_LIKE:-}"

if ! command -v docker &> /dev/null; then
    warn "Docker non installé. Installation…"
    if [[ "$DISTRO_ID" =~ ^(almalinux|rocky|centos|rhel|ol)$ || "$DISTRO_LIKE" == *"rhel"* ]]; then
        dnf install -y dnf-plugins-core
        dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
        dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    else
        curl -fsSL https://get.docker.com | sh
    fi
    systemctl enable --now docker
fi

# "!override" dans docker-compose.moalim.yml exige Compose ≥ 2.24
COMPOSE_VERSION=$(docker compose version --short 2>/dev/null || echo "0")
if [[ "$(printf '%s\n' "2.24.0" "${COMPOSE_VERSION#v}" | sort -V | head -1)" != "2.24.0" ]]; then
    err "Docker Compose ${COMPOSE_VERSION} trop ancien (≥ 2.24 requis). Mets à jour docker-compose-plugin."
fi
log "Docker OK : $(docker --version) / Compose ${COMPOSE_VERSION}"

# ── 2) Mémoire ──
MEM_MB=$(awk '/MemTotal/ {print int($2/1024)}' /proc/meminfo)
if (( MEM_MB < 7000 )); then
    warn "Seulement ${MEM_MB} Mo de RAM (8 Go recommandés). Ça tourne, mais surveille : free -h"
    # Filet de sécurité : sans swap, un pic mémoire fait tuer Postgres ou le backend
    if [[ $(awk '/SwapTotal/ {print $2}' /proc/meminfo) -lt 1000000 && ! -f /swapfile ]]; then
        log "Création d'un swap de 4 Go (/swapfile)"
        fallocate -l 4G /swapfile || dd if=/dev/zero of=/swapfile bs=1M count=4096
        chmod 600 /swapfile
        mkswap /swapfile
        swapon /swapfile
        grep -q '^/swapfile' /etc/fstab || echo '/swapfile none swap sw 0 0' >> /etc/fstab
        sysctl -w vm.swappiness=10 > /dev/null
        echo 'vm.swappiness=10' > /etc/sysctl.d/99-moalim-swap.conf
    fi
fi

# ── 3) Fichiers Docker officiels (version figée) ──
if [[ ! -f "$SB_DIR/docker-compose.yml" ]]; then
    log "Récupération de supabase/docker @ ${SUPABASE_VERSION}"
    command -v git &> /dev/null || { dnf install -y git 2>/dev/null || apt install -y git; }
    TMP_CLONE=$(mktemp -d)
    git clone --depth 1 --branch "$SUPABASE_VERSION" --filter=blob:none --sparse \
        https://github.com/supabase/supabase "$TMP_CLONE"
    git -C "$TMP_CLONE" sparse-checkout set docker
    mkdir -p "$SB_DIR"
    cp -a "$TMP_CLONE/docker/." "$SB_DIR/"
    rm -rf "$TMP_CLONE"
else
    log "$SB_DIR déjà présent — réutilisé"
fi
cp docker-compose.moalim.yml "$SB_DIR/docker-compose.moalim.yml"

# ── 4) .env ──
set_env() {  # set_env CLE VALEUR — remplace la ligne CLE=… ou l'ajoute
    local key="$1" val="$2" file="$SB_DIR/.env"
    if grep -q "^${key}=" "$file"; then
        # délimiteur | : les clés base64 contiennent / et +
        sed -i "s|^${key}=.*|${key}=${val//|/\\|}|" "$file"
    else
        echo "${key}=${val}" >> "$file"
    fi
}
rand_hex() { openssl rand -hex "$1"; }

if [[ ! -f "$SB_DIR/.env" ]]; then
    log "Génération de $SB_DIR/.env"
    cp "$SB_DIR/.env.example" "$SB_DIR/.env"
    chmod 600 "$SB_DIR/.env"

    set_env COMPOSE_FILE                  "docker-compose.yml:docker-compose.moalim.yml"
    # Anciennes clés : le backend et les sessions en cours restent valides
    set_env JWT_SECRET                    "$JWT_SECRET"
    set_env ANON_KEY                      "$ANON_KEY"
    set_env SERVICE_ROLE_KEY              "$SERVICE_ROLE_KEY"
    # Nouveaux secrets internes (hex : pas de caractère spécial dans les URLs postgres)
    set_env POSTGRES_PASSWORD             "$(rand_hex 24)"
    set_env DASHBOARD_USERNAME            "moalim"
    set_env DASHBOARD_PASSWORD            "$(rand_hex 16)"
    set_env SECRET_KEY_BASE               "$(rand_hex 32)"
    set_env REALTIME_DB_ENC_KEY           "$(rand_hex 8)"
    set_env VAULT_ENC_KEY                 "$(rand_hex 16)"
    set_env PG_META_CRYPTO_KEY            "$(rand_hex 16)"
    set_env LOGFLARE_PUBLIC_ACCESS_TOKEN  "$(rand_hex 24)"
    set_env LOGFLARE_PRIVATE_ACCESS_TOKEN "$(rand_hex 24)"
    set_env S3_PROTOCOL_ACCESS_KEY_ID     "$(rand_hex 16)"
    set_env S3_PROTOCOL_ACCESS_KEY_SECRET "$(rand_hex 32)"
    set_env MINIO_ROOT_PASSWORD           "$(rand_hex 16)"
    set_env POOLER_TENANT_ID              "moalim"
    # URLs publiques
    set_env SITE_URL                      "$SITE_URL"
    set_env SUPABASE_PUBLIC_URL           "https://${SB_DOMAIN}"
    set_env API_EXTERNAL_URL              "https://${SB_DOMAIN}/auth/v1"
    set_env KONG_HTTP_PORT                "$KONG_PORT"
    # Les comptes sont créés par le backend (admin API) : pas d'inscription publique
    set_env DISABLE_SIGNUP                "true"
    set_env ENABLE_PHONE_SIGNUP           "false"
    set_env ENABLE_ANONYMOUS_USERS        "false"
    set_env STUDIO_DEFAULT_ORGANIZATION   "Moalim"
    set_env STUDIO_DEFAULT_PROJECT        "Moalim"
    log ".env créé — SAUVEGARDE $SB_DIR/.env hors du serveur"
else
    log "$SB_DIR/.env existant — réutilisé"
fi

# ── 5) Démarrage ──
cd "$SB_DIR"
log "Téléchargement des images (quelques minutes au premier run)"
docker compose pull --quiet
log "Démarrage de la stack Supabase"
docker compose up -d

log "Attente de l'API (auth via Kong)…"
for i in {1..60}; do
    if curl -sf -H "apikey: ${ANON_KEY}" "http://127.0.0.1:${KONG_PORT}/auth/v1/health" > /dev/null 2>&1; then
        log "Supabase répond sur 127.0.0.1:${KONG_PORT} ✓"
        break
    fi
    [[ $i -eq 60 ]] && err "Supabase n'a pas démarré. Vérifie : cd $SB_DIR && docker compose ps && docker compose logs --tail 50"
    sleep 5
done

# ── 6) Le backend joint Supabase en local, sans sortir sur Internet ──
if ! grep -qE "^127\.0\.0\.1[[:space:]]+.*\b${SB_DOMAIN}\b" /etc/hosts; then
    echo "127.0.0.1 ${SB_DOMAIN}" >> /etc/hosts
    log "/etc/hosts : ${SB_DOMAIN} → 127.0.0.1"
fi

# ── 7) Nginx + certificat ──
cd "$SCRIPT_DIR"
CERT_PATH="/etc/letsencrypt/live/${SB_DOMAIN}/fullchain.pem"
NGINX_CONF="/etc/nginx/conf.d/moalim-supabase.conf"

if [[ ! -f "$CERT_PATH" ]]; then
    log "Certificat absent — config HTTP temporaire pour le challenge ACME"
    mkdir -p /var/www/certbot
    cat > "$NGINX_CONF" <<EONGINX
server {
    listen 80;
    listen [::]:80;
    server_name ${SB_DOMAIN};
    location /.well-known/acme-challenge/ { root /var/www/certbot; }
    location / { return 404; }
}
EONGINX
    nginx -t || err "Erreur syntaxe nginx (bootstrap HTTP)."
    systemctl reload nginx

    certbot certonly --webroot -w /var/www/certbot \
        -d "$SB_DOMAIN" --non-interactive --agree-tos --email "$CERT_EMAIL" \
        || err "Échec certbot. Vérifie que ${SB_DOMAIN} pointe vers ce VPS (enregistrement A)."
else
    log "Certificat SSL déjà présent — skip certbot"
fi

# Déjà présents si moalim.online / analytics ont été installés ; sinon on les crée
if [[ ! -f /etc/letsencrypt/options-ssl-nginx.conf ]]; then
    curl -fsSL https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf \
         -o /etc/letsencrypt/options-ssl-nginx.conf
fi
if [[ ! -f /etc/letsencrypt/ssl-dhparams.pem ]]; then
    log "Génération des paramètres DH (1-2 min)…"
    openssl dhparam -out /etc/letsencrypt/ssl-dhparams.pem 2048
fi

sed "s/sb\.moalim\.online/${SB_DOMAIN}/g" nginx-supabase.conf > "$NGINX_CONF"
nginx -t || err "Erreur syntaxe nginx. Inspecte $NGINX_CONF"
systemctl reload nginx

# ── 8) Sauvegarde nocturne ──
install -m 700 backup.sh /usr/local/bin/moalim-supabase-backup
cat > /etc/cron.d/moalim-supabase-backup <<'EOCRON'
# Sauvegarde Supabase (base + fichiers) chaque nuit à 3h15
15 3 * * * root /usr/local/bin/moalim-supabase-backup >> /var/log/moalim-supabase-backup.log 2>&1
EOCRON
log "Sauvegarde nocturne installée (/etc/cron.d/moalim-supabase-backup)"

# ── 9) Récap ──
DASH_USER=$(grep '^DASHBOARD_USERNAME=' "$SB_DIR/.env" | cut -d= -f2-)
echo ""
echo "════════════════════════════════════════════════════════════"
log "✅ Supabase auto-hébergé installé"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "  Étapes suivantes :"
echo "  1) Restaurer les données :"
echo "       sudo ./restore.sh <db_cluster-….backup.gz> <….storage.zip>"
echo "  2) Dans le .env du backend :"
echo "       SUPABASE_URL=https://${SB_DOMAIN}"
echo "     (clés inchangées) puis : systemctl restart moalim-backend"
echo ""
echo "  Studio (depuis ton PC) :"
echo "       ssh -L ${KONG_PORT}:127.0.0.1:${KONG_PORT} root@<ip-du-vps>"
echo "       puis http://localhost:${KONG_PORT}  — login : ${DASH_USER}"
echo "       mot de passe : grep DASHBOARD_PASSWORD $SB_DIR/.env"
echo ""
echo "  Fichiers importants :"
echo "  - $SB_DIR/.env                     (secrets — SAUVEGARDE-LE)"
echo "  - $SB_DIR/volumes/db/data          (données Postgres)"
echo "  - $SB_DIR/volumes/storage          (fichiers du Storage)"
echo "  - /var/backups/moalim-supabase     (sauvegardes nocturnes)"
echo ""
echo "  Commandes utiles :"
echo "  - État   : cd $SB_DIR && docker compose ps"
echo "  - Logs   : cd $SB_DIR && docker compose logs -f auth storage rest"
echo "  - Backup : /usr/local/bin/moalim-supabase-backup"
echo ""
