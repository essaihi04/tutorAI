#!/usr/bin/env bash
# =============================================================
# Moalim — Restauration de la sauvegarde Supabase Cloud
# dans le Supabase auto-hébergé installé par install.sh.
#
#   sudo ./restore.sh db_cluster-….backup.gz ldeifdnczkzgtxctjlel.storage.zip
#
# Fichiers téléchargés depuis le dashboard Supabase
# (projet en pause → Download backups).
#
# Déroulé :
#  1) la sauvegarde (pg_dumpall) est rejouée dans un Postgres 17
#     JETABLE, pour ne pas mélanger ses schémas auth/storage (version
#     cloud) avec ceux de la nouvelle instance ;
#  2) on en extrait : comptes (auth.*), tout le schéma public
#     (structure + données + RLS), définitions des buckets ;
#  3) on charge dans supabase-db, colonne par colonne pour auth/storage
#     (tolère un léger écart de version de GoTrue / storage-api) ;
#  4) les fichiers du Storage sont renvoyés via l'API ;
#  5) comptage ligne à ligne source ↔ cible.
# =============================================================
set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log()  { echo -e "${GREEN}▶${NC} $1"; }
warn() { echo -e "${YELLOW}⚠${NC} $1"; }
err()  { echo -e "${RED}✗${NC} $1"; exit 1; }

DUMP="${1:-}"
STORAGE_ZIP="${2:-}"
SB_DIR="${SB_DIR:-/opt/supabase}"
OLD_REF="${OLD_REF:-ldeifdnczkzgtxctjlel}"
TMP_PG="moalim-restore-pg"
TMP_IMAGE="postgres:17"   # même version majeure que la sauvegarde (PG 17.6)

[[ -f "$DUMP" ]] || err "Usage : $0 <db_cluster-….backup.gz> [<….storage.zip>]"
[[ -z "$STORAGE_ZIP" || -f "$STORAGE_ZIP" ]] || err "Archive storage introuvable : $STORAGE_ZIP"
[[ -f "$SB_DIR/.env" ]] || err "$SB_DIR/.env absent — lance install.sh d'abord."
gzip -t "$DUMP" || err "Sauvegarde corrompue (gzip -t)."

env_get() { grep "^$1=" "$SB_DIR/.env" | cut -d= -f2-; }
SERVICE_ROLE_KEY=$(env_get SERVICE_ROLE_KEY)
PUBLIC_URL=$(env_get SUPABASE_PUBLIC_URL)
KONG_PORT=$(env_get KONG_HTTP_PORT)
OLD_URL="https://${OLD_REF}.supabase.co"

WORK=$(mktemp -d /tmp/moalim-restore.XXXXXX)
cleanup() {
    docker rm -f "$TMP_PG" > /dev/null 2>&1 || true
    rm -rf "$WORK"
}
trap cleanup EXIT

# psql source (Postgres jetable) et cible (supabase-db)
src_psql() { docker exec -i "$TMP_PG" psql -U restore_admin -d postgres -X -qAt -v ON_ERROR_STOP=1 "$@"; }
dst_psql() { docker exec -i supabase-db psql -U supabase_admin -d postgres -X -qAt -v ON_ERROR_STOP=1 "$@"; }

# ── 0) La cible doit être vierge ──
docker inspect -f '{{.State.Health.Status}}' supabase-db 2>/dev/null | grep -q healthy \
    || err "supabase-db n'est pas healthy. cd $SB_DIR && docker compose ps"
EXISTING_USERS=$(dst_psql -c "select count(*) from auth.users")
EXISTING_TABLES=$(dst_psql -c "select count(*) from pg_tables where schemaname='public'")
if [[ "$EXISTING_USERS" != "0" || "$EXISTING_TABLES" != "0" ]]; then
    [[ "${FORCE:-0}" == "1" ]] || err "La cible contient déjà ${EXISTING_USERS} comptes / ${EXISTING_TABLES} tables public. Refus (FORCE=1 pour forcer)."
    warn "FORCE=1 : la cible n'est pas vierge, des doublons peuvent échouer."
fi

# ── 1) Postgres jetable + rejeu de la sauvegarde ──
log "Démarrage d'un Postgres 17 jetable"
docker rm -f "$TMP_PG" > /dev/null 2>&1 || true
# Superuser nommé restore_admin : la sauvegarde retire SUPERUSER au rôle
# postgres (comme sur Supabase Cloud), il ne faut pas être connecté avec.
docker run -d --name "$TMP_PG" \
    -e POSTGRES_USER=restore_admin -e POSTGRES_PASSWORD="$(openssl rand -hex 16)" \
    -e POSTGRES_DB=restore_admin "$TMP_IMAGE" > /dev/null
for i in {1..60}; do
    docker logs "$TMP_PG" 2>&1 | grep -q "PostgreSQL init process complete" \
        && docker exec "$TMP_PG" pg_isready -U restore_admin -q && break
    [[ $i -eq 60 ]] && err "Postgres jetable n'a pas démarré (docker logs $TMP_PG)."
    sleep 2
done

log "Rejeu de la sauvegarde (1-3 min)"
# ON_ERROR_STOP=0 : les extensions propres à Supabase (vault, graphql, pgsodium…)
# n'existent pas dans postgres:17 ; leurs objets échouent, sans impact sur
# les tables auth/public/storage qu'on extrait ensuite.
gzip -dc "$DUMP" \
    | docker exec -i "$TMP_PG" psql -U restore_admin -d postgres -X -q -v ON_ERROR_STOP=0 \
    > "$WORK/replay.log" 2>&1 || true
log "Rejeu terminé ($(grep -c 'ERROR' "$WORK/replay.log" || true) erreurs attendues d'extensions — détail : replay.log)"

SRC_USERS=$(src_psql -c "select count(*) from auth.users")
SRC_PUBLIC=$(src_psql -c "select count(*) from pg_tables where schemaname='public'")
[[ "$SRC_USERS" -gt 0 && "$SRC_PUBLIC" -gt 0 ]] \
    || { cp "$WORK/replay.log" /tmp/moalim-replay.log; err "Rejeu incomplet (${SRC_USERS} comptes, ${SRC_PUBLIC} tables). Log : /tmp/moalim-replay.log"; }
log "Source : ${SRC_USERS} comptes, ${SRC_PUBLIC} tables public"

# ── 2) Copie table par table sur les colonnes communes ──
cols_of() {  # cols_of src|dst schema table → colonnes non générées, une par ligne
    local q="select column_name from information_schema.columns
             where table_schema='$2' and table_name='$3' and is_generated='NEVER'
             order by column_name"
    if [[ "$1" == src ]]; then src_psql -c "$q"; else dst_psql -c "$q"; fi
}

copy_table() {  # copy_table schema.table
    local t="$1" schema="${1%%.*}" table="${1#*.}"
    cols_of src "$schema" "$table" > "$WORK/src.cols"
    cols_of dst "$schema" "$table" > "$WORK/dst.cols"
    local missing collist n
    missing=$(comm -23 "$WORK/src.cols" "$WORK/dst.cols" | paste -sd, -)
    [[ -n "$missing" ]] && warn "$t : colonnes absentes de la cible, ignorées : $missing"
    collist=$(comm -12 "$WORK/src.cols" "$WORK/dst.cols" | sed 's/.*/"&"/' | paste -sd, -)
    [[ -n "$collist" ]] || err "$t : aucune colonne commune"
    docker exec "$TMP_PG" psql -U restore_admin -d postgres -X -q \
        -c "\\copy (select $collist from $t) to stdout" \
        | dst_psql -c "\\copy $t ($collist) from stdin"
    n=$(dst_psql -c "select count(*) from $t")
    log "  $t : $n lignes"
}

# ── 3) Comptes (avant public : les FK public → auth.users en dépendent) ──
log "Restauration des comptes"
# sessions + refresh_tokens : les élèves connectés le restent (même JWT_SECRET)
for t in auth.users auth.identities auth.mfa_factors auth.sessions auth.mfa_amr_claims auth.refresh_tokens; do
    copy_table "$t"
done
dst_psql -c "select setval('auth.refresh_tokens_id_seq', coalesce((select max(id) from auth.refresh_tokens), 1))" > /dev/null

# ── 4) Schéma public complet ──
log "Restauration du schéma public (structure, données, RLS, droits)"
docker exec "$TMP_PG" pg_dump -U restore_admin -d postgres --schema=public \
    --no-publications --no-subscriptions > "$WORK/public.sql"
# Liens absolus vers l'ancien projet → nouvelle URL publique
sed -i "s#${OLD_URL}#${PUBLIC_URL}#g" "$WORK/public.sql"
dst_psql -v ON_ERROR_STOP=0 < "$WORK/public.sql" > "$WORK/public.log" 2>&1 || true
# "schema public already exists" est normal ; toute autre erreur est affichée
if grep 'ERROR' "$WORK/public.log" | grep -v 'already exists' > "$WORK/public.errors"; then
    cp "$WORK/public.log" /tmp/moalim-public-restore.log
    warn "Erreurs inattendues pendant le chargement de public (log complet : /tmp/moalim-public-restore.log) :"
    cat "$WORK/public.errors"
fi

# ── 5) Buckets + fichiers ──
log "Restauration des buckets"
copy_table storage.buckets

# PostgREST doit relire le schéma pour voir les nouvelles tables
dst_psql -c "NOTIFY pgrst, 'reload schema'" > /dev/null
dst_psql -c "ANALYZE" > /dev/null

if [[ -n "$STORAGE_ZIP" ]]; then
    log "Envoi des fichiers du Storage"
    command -v unzip &> /dev/null || { dnf install -y unzip 2>/dev/null || apt install -y unzip; }
    command -v file  &> /dev/null || { dnf install -y file  2>/dev/null || apt install -y file; }
    unzip -q "$STORAGE_ZIP" -d "$WORK/storage"
    ROOT="$WORK/storage/$OLD_REF"
    [[ -d "$ROOT" ]] || ROOT="$WORK/storage"
    OK=0; KO=0
    while IFS= read -r -d '' f; do
        rel="${f#"$ROOT"/}"            # bucket/chemin/fichier.ext
        bucket="${rel%%/*}"
        path="${rel#*/}"
        url_path=$(printf %s "$path" | sed 's/ /%20/g')
        if curl -sf -o /dev/null -X POST \
            "http://127.0.0.1:${KONG_PORT}/storage/v1/object/${bucket}/${url_path}" \
            -H "Authorization: Bearer ${SERVICE_ROLE_KEY}" -H "apikey: ${SERVICE_ROLE_KEY}" \
            -H "x-upsert: true" -H "Content-Type: $(file --mime-type -b "$f")" \
            --data-binary @"$f"; then
            OK=$((OK+1))
        else
            KO=$((KO+1)); warn "  échec : $rel"
        fi
    done < <(find "$ROOT" -type f -print0)
    log "  fichiers envoyés : $OK, échecs : $KO"
fi

# ── 6) Vérification : comptage source ↔ cible ──
log "Vérification des volumes (source → cible)"
DIFF=0
while read -r t; do
    # < /dev/null : docker exec -i avalerait sinon la liste des tables de la boucle
    s=$(src_psql -c "select count(*) from $t" < /dev/null)
    d=$(dst_psql -c "select count(*) from $t" < /dev/null 2>/dev/null || echo "ABSENTE")
    if [[ "$s" != "$d" ]]; then
        printf "  ${RED}%-40s %8s → %s${NC}\n" "$t" "$s" "$d"; DIFF=1
    elif [[ "$s" != "0" ]]; then
        printf "  %-40s %8s ✓\n" "$t" "$s"
    fi
done < <(src_psql -c "select schemaname||'.'||tablename from pg_tables
                      where schemaname='public' or (schemaname='auth' and tablename in ('users','identities','sessions'))
                         or (schemaname='storage' and tablename='buckets')
                      order by 1")

echo ""
if [[ $DIFF -eq 0 ]]; then
    log "✅ Restauration complète : toutes les tables ont le même nombre de lignes."
else
    warn "Des écarts sont signalés en rouge ci-dessus — ne bascule pas le backend avant de les comprendre."
fi
echo ""
echo "  Étape suivante : SUPABASE_URL=${PUBLIC_URL} dans le .env du backend,"
echo "  puis systemctl restart moalim-backend && curl -s https://moalim.online/health"
