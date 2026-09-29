# Supabase auto-hébergé — migration depuis Supabase Cloud

Remplace le projet Supabase Cloud `ldeifdnczkzgtxctjlel`, mis en pause (offre gratuite),
par une instance Supabase sur le même VPS que le frontend et le backend.

```
Internet ──► nginx ──► moalim.online          → frontend (dist/) + backend FastAPI :8000
                   └─► sb.moalim.online        → Kong :54321 (lecture des fichiers publics seulement)
backend ──► sb.moalim.online (/etc/hosts → 127.0.0.1) ──► Kong ──► auth / rest / storage ──► Postgres 17
```

- **Mêmes clés** : on réutilise le `JWT_SECRET`, l'`ANON_KEY` et la `SERVICE_ROLE_KEY` de l'ancien projet.
  Côté backend, seul `SUPABASE_URL` change, et les élèves restent connectés.
- **Rien d'exposé** : Kong et Postgres écoutent sur `127.0.0.1`. Le sous-domaine public ne sert
  que les fichiers des buckets publics (`/storage/v1/object/public/…`) ; le reste n'est accessible que depuis le serveur.
- **Version figée** : `supabase/supabase` tag `v1.26.08` (Postgres 17.6, comme la sauvegarde).

## Fichiers

| Fichier | Rôle |
|---|---|
| `install.sh` | Installe Docker si besoin, récupère la stack officielle dans `/opt/supabase`, génère `.env`, démarre, configure nginx + certificat, installe la sauvegarde nocturne |
| `docker-compose.moalim.yml` | Surcouche : lie les ports à `127.0.0.1` (Kong 54321, pooler 55432/56543) |
| `nginx-supabase.conf` | Vhost `sb.moalim.online` (public : fichiers publics ; privé : tout le reste) |
| `restore.sh` | Restaure la sauvegarde Cloud (comptes, schéma public, buckets, fichiers) et compare les volumes |
| `backup.sh` | Sauvegarde nocturne → `/var/backups/moalim-supabase` (14 jours) |
| `secrets.env.example` | Modèle pour les 3 clés de l'ancien projet |

## Pré-requis

- VPS **Ubuntu 24.04** (pas Alma/Rocky : SELinux a déjà causé un 502 de 8 jours), ~20 Go de disque libre.
- RAM : **4 Go suffisent pour démarrer** (Realtime, Edge Functions et le pooler sont coupés,
  `install.sh` ajoute 4 Go de swap). Passer à 8 Go quand la charge monte (`free -h`, swap utilisé en continu).
- DNS : enregistrement **A `sb` → IP du VPS** (chez Hostinger), propagé avant `install.sh`.
- Les deux fichiers téléchargés depuis le dashboard Supabase :
  `db_cluster-16-09-2026@17-37-20.backup.gz` et `ldeifdnczkzgtxctjlel.storage.zip`.

## Procédure

```bash
# Depuis le PC : envoyer les sauvegardes
scp "db_cluster-16-09-2026@17-37-20.backup.gz" ldeifdnczkzgtxctjlel.storage.zip root@<ip>:/root/

# Sur le VPS
cd /var/www/moalim && git pull          # ou /root/moalim selon le serveur
cd deploy/supabase
cp secrets.env.example secrets.env && chmod 600 secrets.env
nano secrets.env                        # coller les 3 valeurs depuis le .env du backend
chmod +x *.sh
sudo ./install.sh
sudo ./restore.sh /root/db_cluster-16-09-2026@17-37-20.backup.gz /root/ldeifdnczkzgtxctjlel.storage.zip
```

`restore.sh` se termine par un tableau source → cible pour chaque table. Tout doit être ✓
(30 comptes, 25 élèves, 139 sessions, 7 634 lignes `token_usage`…).

### Basculer le backend

Dans le `.env` du backend sur le serveur :

```
SUPABASE_URL=https://sb.moalim.online
```

Les clés restent identiques. Puis :

```bash
systemctl restart moalim-backend
curl -s https://moalim.online/health
journalctl -u moalim-backend -n 50 --no-pager
```

Vérifier ensuite : connexion d'un élève, connexion admin, création d'un compte depuis l'admin,
affichage d'une image de ressource pédagogique.

## Studio (tableau de bord)

Pas exposé sur Internet. Depuis le PC :

```bash
ssh -L 54321:127.0.0.1:54321 root@<ip>
```

Puis http://localhost:54321, utilisateur `moalim`, mot de passe : `grep DASHBOARD_PASSWORD /opt/supabase/.env`.

## Sauvegardes

- Automatique chaque nuit à 3h15 : `/var/backups/moalim-supabase/db-*.dump.gz` + `storage-*.tar.gz`.
- Manuelle : `/usr/local/bin/moalim-supabase-backup`.
- **Copier régulièrement hors du serveur** (`scp` vers le PC ou un Drive). Une sauvegarde qui reste sur la même machine ne protège pas d'une panne du VPS.
- Restaurer une sauvegarde nocturne :
  `gunzip -c db-….dump.gz | docker exec -i supabase-db psql -U supabase_admin -d postgres`
  et `tar -C /opt/supabase/volumes -xzf storage-….tar.gz`.

## À garder en tête

- `/opt/supabase/.env` contient tous les secrets : le sauvegarder hors du serveur.
- Serveur SELinux (el9) : la stack vit dans `/opt/supabase`, pas sous `/root`,
  et les volumes officiels portent déjà les labels `:z`/`:Z`.
- Mise à jour de Supabase : changer `SUPABASE_VERSION` dans `install.sh` et suivre les
  notes de version (`/opt/supabase/CHANGELOG.md`) ; toujours sauvegarder avant.
- Le projet Cloud reste restaurable jusqu'au **22/10/2027**. Ne pas le supprimer avant
  quelques semaines de fonctionnement sans souci en auto-hébergé.
