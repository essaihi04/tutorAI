# Déploiement Moalim sur VPS — Guide complet

Ce dossier contient tout ce qu'il faut pour déployer **moalim.online** en mode natif (sans Docker) sur un VPS Ubuntu/Debian.

## Pré-requis

- VPS Ubuntu 22.04+ ou Debian 12+ (au moins 4 Go RAM, 20 Go disque)
- Accès `root` SSH : `ssh root@87.106.1.128`
- Domaine `moalim.online` qui pointe vers l'IP du VPS

## Étape 1 — DNS

Dans ton panel DNS (Hostinger), corrige le record A :

| Type  | Nom | Valeur          | TTL |
|-------|-----|-----------------|-----|
| **A** | `@` | `87.106.1.128`  | 300 |
| CNAME | `www` | `moalim.online` | 300 |

⚠️ Actuellement le record A pointe vers `2.57.91.91` — **change-le** vers `87.106.1.128`.

Vérifie la propagation :
```bash
dig +short moalim.online
# doit retourner 87.106.1.128
```

## Étape 2 — Premier déploiement

Connecte-toi au VPS et lance le script :

```bash
ssh root@87.106.1.128

# Cloner ce dossier deploy/ ou le repo entier
cd /tmp
git clone https://github.com/essaihi04/tutorAI.git
cd tutorAI/deploy
chmod +x deploy.sh update.sh
bash deploy.sh
```

Le script s'occupe de tout :

1. Met à jour le système, installe Python 3.12, Node.js 20, Nginx, Redis, Certbot
2. Configure le pare-feu UFW (SSH + HTTP/HTTPS)
3. Clone le repo dans `/var/www/moalim`
4. Crée un venv Python, installe les dépendances backend
5. Build le frontend Vite (`npm run build` → `frontend/dist/`)
6. Installe le service systemd `moalim-backend.service`
7. Configure Nginx avec un upstream local 127.0.0.1:8000
8. Émet un certificat SSL Let's Encrypt via certbot
9. Active le renouvellement automatique du certificat

Durée : ~5-10 minutes selon la connexion.

## Étape 3 — Vérification

```bash
# Backend
curl https://moalim.online/health
# → {"status":"ok","service":"ai-tutor-bac"}

# Frontend
curl -I https://moalim.online
# → HTTP/2 200

# Logs en direct
journalctl -u moalim-backend -f
journalctl -u nginx -f
```

## Étape 4 — Mises à jour

Pour pousser une nouvelle version :

```bash
ssh root@87.106.1.128
bash /var/www/moalim/deploy/update.sh
```

Le script :
- pull la dernière version sur `main`
- réinstalle les deps Python si requirements.txt a changé
- rebuild le frontend
- redémarre `moalim-backend`
- recharge Nginx

## Architecture

```
                  ┌─────────────────────────────────┐
   Internet ───▶  │ Nginx :80/:443 (SSL via certbot)│
                  │  • / → static SPA dist/         │
                  │  • /api/ → 127.0.0.1:8000       │
                  │  • /ws/  → 127.0.0.1:8000 (WS)  │
                  │  • /static/ → 127.0.0.1:8000    │
                  └────────────┬────────────────────┘
                               │
                  ┌────────────▼────────────────────┐
                  │ FastAPI (uvicorn 2 workers)     │
                  │ systemd: moalim-backend         │
                  │ /var/www/moalim/backend         │
                  └────────────┬────────────────────┘
                               │
              ┌────────────────┼─────────────────────┐
              ▼                ▼                     ▼
       ┌─────────┐    ┌────────────────┐    ┌──────────────┐
       │ Redis   │    │ Supabase cloud │    │ APIs LLM     │
       │ local   │    │ (Postgres+Auth)│    │ Gemini/      │
       │ :6379   │    │                │    │ DeepSeek/    │
       └─────────┘    └────────────────┘    │ Mistral      │
                                             └──────────────┘
```

## Fichiers

| Fichier | Rôle |
|---|---|
| `deploy.sh` | Premier déploiement (full setup) |
| `update.sh` | Mise à jour après push git |
| `nginx.conf` | Reverse proxy + SSL + WebSocket |
| `moalim-backend.service` | Unit systemd uvicorn |
| `backend.env` | Variables d'env prod (clés API) |

## Sécurité importante

- ⚠️ `deploy/backend.env` contient des **clés réelles**. Il est dans `.gitignore`. **Ne jamais le commit.**
- Pour rotation des clés (recommandé après le premier déploiement) :
  - `SECRET_KEY` JWT : remplacer par une nouvelle valeur aléatoire
  - Régénérer les API keys côté Gemini/DeepSeek/Mistral si nécessaire

## Commandes utiles

```bash
# Statut backend
systemctl status moalim-backend

# Redémarrer juste le backend (sans rebuild)
systemctl restart moalim-backend

# Tester la config Nginx avant reload
nginx -t

# Voir les requêtes en cours
tail -f /var/log/nginx/access.log

# Renouveler le certificat manuellement (test)
certbot renew --dry-run

# Espace disque
df -h /var/www/moalim
```

## Dépannage

**WebSocket ne se connecte pas**
- Vérifier `proxy_read_timeout 3600s` dans nginx.conf
- Vérifier qu'on est en HTTPS (le frontend utilise `wss://` quand `https`)

**500 sur /api/**
- `journalctl -u moalim-backend -n 100`
- Vérifier que `.env` a bien toutes les variables (Supabase + LLM keys)

**Frontend affiche page blanche**
- Vérifier que `/var/www/moalim/frontend/dist/index.html` existe
- Permissions : `chown -R www-data:www-data /var/www/moalim/frontend/dist`

**SSL ne s'émet pas**
- Vérifier que le DNS pointe bien vers le VPS : `dig +short moalim.online`
- Le port 80 doit être ouvert dans UFW
