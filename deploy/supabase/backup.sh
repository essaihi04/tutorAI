#!/usr/bin/env bash
# =============================================================
# Moalim — Sauvegarde Supabase auto-hébergé
# Installé par install.sh dans /usr/local/bin/moalim-supabase-backup
# et lancé chaque nuit par /etc/cron.d/moalim-supabase-backup.
#
# Produit dans $BACKUP_DIR :
#   db-AAAAMMJJ-HHMM.dump.gz     pg_dumpall complet (rôles + auth + public + storage)
#   storage-AAAAMMJJ-HHMM.tar.gz fichiers du Storage
# Garde $KEEP_DAYS jours. Copie ces fichiers HORS du serveur régulièrement.
# =============================================================
set -euo pipefail

SB_DIR="${SB_DIR:-/opt/supabase}"
BACKUP_DIR="${BACKUP_DIR:-/var/backups/moalim-supabase}"
KEEP_DAYS="${KEEP_DAYS:-14}"
STAMP=$(date +%Y%m%d-%H%M)

mkdir -p "$BACKUP_DIR"
chmod 700 "$BACKUP_DIR"

echo "[$(date -Is)] Sauvegarde Supabase → $BACKUP_DIR"

# Écrit dans un .part puis renomme : un fichier final n'est jamais tronqué
DB_OUT="$BACKUP_DIR/db-$STAMP.dump.gz"
docker exec supabase-db pg_dumpall -U supabase_admin --clean --if-exists \
    | gzip -6 > "$DB_OUT.part"
gzip -t "$DB_OUT.part"
mv "$DB_OUT.part" "$DB_OUT"

ST_OUT="$BACKUP_DIR/storage-$STAMP.tar.gz"
tar -C "$SB_DIR/volumes" -czf "$ST_OUT.part" storage
mv "$ST_OUT.part" "$ST_OUT"

find "$BACKUP_DIR" -maxdepth 1 -type f \( -name 'db-*.dump.gz' -o -name 'storage-*.tar.gz' \) \
    -mtime +"$KEEP_DAYS" -delete

echo "[$(date -Is)] OK : $(du -h "$DB_OUT" | cut -f1) base, $(du -h "$ST_OUT" | cut -f1) storage"
