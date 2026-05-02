# 📊 Moalim Analytics — Umami self-hosted

> Installation d'**Umami** (analytics privacy-first, alternative à Google Analytics) sur le VPS Moalim, sur le sous-domaine `analytics.moalim.online`.

---

## 🎯 Ce que tu auras après installation

- ✅ **Dashboard analytics complet** : visites par jour / semaine / mois / année
- ✅ **Sources de trafic** : Instagram, Facebook, Google, direct…
- ✅ **Pays / villes** : qui visite depuis Casablanca, Rabat…
- ✅ **Appareils** : mobile vs desktop vs tablette
- ✅ **Pages les plus consultées** : home, blog, signup…
- ✅ **Heures de pic** : quand poster sur les réseaux
- ✅ **100% RGPD** : pas de cookie banner nécessaire
- ✅ **0 MAD/mois** : tout chez toi sur ton VPS
- ✅ **Données privées** : aucune fuite vers Google ou autres tiers

---

## 📋 Pré-requis

- VPS avec Docker + Docker Compose v2 installés (le script les installe sinon)
- nginx natif déjà en place (avec config `moalim.online` existante)
- Certbot installé (pour SSL Let's Encrypt)
- Accès root (sudo)

---

## 🚀 Installation pas-à-pas

### Phase 1 — DNS (5 minutes, à faire d'abord)

Chez ton registrar de domaine (où tu as acheté `moalim.online`) :

1. Ajoute un enregistrement DNS de type **A** :
   - **Nom** : `analytics`
   - **Type** : `A`
   - **Valeur** : `<IP de ton VPS>` (la même que pour `moalim.online`)
   - **TTL** : `3600` (1 heure)

2. Vérifie la propagation (peut prendre 5-60 minutes) :
   ```bash
   dig analytics.moalim.online
   # ou en ligne : https://dnschecker.org/#A/analytics.moalim.online
   ```

3. Quand `analytics.moalim.online` répond avec l'IP du VPS → Phase 2.

### Phase 2 — Installation sur le VPS (30 minutes)

#### Option A — Via remote-deploy (recommandé)

Sur ta machine Windows, dans PowerShell :

```powershell
# 1) Push le code à jour
git push

# 2) SSH vers le VPS et lance l'install
ssh root@<IP_VPS> "cd /opt/moalim/ai-tutor-bac && git pull && cd deploy/umami && chmod +x install.sh && ./install.sh"
```

Adapte le chemin `/opt/moalim/ai-tutor-bac` au chemin réel de ton repo sur le VPS (regarde dans `deploy/remote-deploy.ps1`).

#### Option B — Manuel sur le VPS

```bash
# 1) SSH vers le VPS
ssh root@<IP_VPS>

# 2) Va dans le dossier du repo
cd /opt/moalim/ai-tutor-bac    # adapte le chemin si besoin
git pull origin main

# 3) Lance l'installation
cd deploy/umami
chmod +x install.sh
./install.sh
```

Le script va :
1. Vérifier que Docker est installé (sinon il l'installe)
2. Générer un `.env` avec mots de passe aléatoires sécurisés
3. Lancer Umami + Postgres dédié dans Docker
4. Installer la config nginx pour `analytics.moalim.online`
5. Demander un certificat SSL Let's Encrypt
6. Reload nginx

⏱️ **Durée totale** : ~5-10 minutes (selon la vitesse du VPS).

### Phase 3 — Configuration Umami (5 minutes)

1. Ouvre **https://analytics.moalim.online** dans ton navigateur
2. Login avec les credentials par défaut :
   - **Username** : `admin`
   - **Password** : `umami`
3. **🚨 IMPORTANT** : change immédiatement le mot de passe :
   - Profile → Change password → mets un mot de passe fort (min. 16 caractères)
4. **Crée le site** :
   - Settings → Websites → **Add website**
   - **Name** : `Moalim`
   - **Domain** : `moalim.online`
   - Clique **Save**
5. Tu vois apparaître ton site dans la liste. Clique dessus, puis **Tracking code**.
6. **Copie le `Website ID`** (un UUID type `12345678-1234-...`).

### Phase 4 — Injection du tracking dans le frontend

**Communique le `Website ID` à Cascade**, qui s'occupera d'ajouter le script dans :
- `frontend/index.html` (la SPA React)
- `frontend/public/blog/*.html` (tous les articles)
- `frontend/public/about.html`, `contact.html`, `mentions-legales.html`

Après ça, redéploie avec :
```powershell
powershell -ExecutionPolicy Bypass -File deploy/remote-deploy.ps1 -UpdateOnly
```

Et c'est tout ! Les visites commenceront à s'afficher dans Umami en temps réel (latence < 5 secondes).

---

## 🛠️ Commandes utiles

### Logs en temps réel
```bash
docker compose -f /opt/moalim/ai-tutor-bac/deploy/umami/docker-compose.yml logs -f umami
```

### Redémarrer Umami
```bash
cd /opt/moalim/ai-tutor-bac/deploy/umami
docker compose restart
```

### Mettre à jour Umami (nouvelle version)
```bash
cd /opt/moalim/ai-tutor-bac/deploy/umami
docker compose pull
docker compose up -d
```

### Backup de la base
```bash
docker exec moalim-umami-db pg_dump -U umami umami > umami-backup-$(date +%Y%m%d).sql
```

### Restore
```bash
cat umami-backup-20260502.sql | docker exec -i moalim-umami-db psql -U umami -d umami
```

### Arrêter complètement Umami
```bash
cd /opt/moalim/ai-tutor-bac/deploy/umami
docker compose down
# Pour supprimer aussi les données (irréversible !) :
# docker compose down -v
```

---

## 📊 Utiliser le dashboard

Une fois quelques visites enregistrées :

### Vues principales
- **Dashboard** : vue d'ensemble (jour, semaine, mois)
- **Realtime** : qui est sur ton site MAINTENANT
- **Sessions** : parcours détaillé par utilisateur anonyme
- **Events** : actions personnalisées (ex: "diagnostic_complete")

### Filtres puissants
- Par **période** : aujourd'hui / 24h / 7j / 30j / 90j / année
- Par **source** : referrer (Instagram, Facebook…)
- Par **pays** : voir uniquement les visiteurs du Maroc
- Par **device** : seulement mobile / desktop
- Par **page** : voir le trafic d'une page spécifique

### Métriques clés à surveiller chaque semaine
1. **Unique visitors** (la métrique #1)
2. **Bounce rate** : % qui partent sans interaction (objectif < 60%)
3. **Average visit time** : temps moyen sur le site (objectif > 90s)
4. **Top pages** : quelles pages convertissent
5. **Top referrers** : quel canal fonctionne

---

## 🎯 Tracker les conversions Moalim

Une fois Umami en place, tu peux tracker des **événements custom** :
- Visiteur clique « Tester mon niveau » → event `diagnostic_started`
- Visiteur termine le quiz → event `diagnostic_completed`
- Visiteur clique « Créer un compte » → event `signup_clicked`
- Visiteur s'inscrit avec succès → event `signup_success`

Cela demande quelques lignes de JavaScript dans les composants React. Demande à Cascade de les ajouter une fois Umami opérationnel.

---

## 🔒 Sécurité

- Le mot de passe Umami est dans `deploy/umami/.env` — **jamais commit** (déjà gitignored).
- Sauvegarde ce `.env` ailleurs (gestionnaire de mots de passe).
- Le port `3001` n'est **PAS** ouvert sur l'extérieur — uniquement nginx peut y accéder.
- Postgres Umami est sur un network Docker isolé — pas accessible de l'extérieur.
- HTTPS forcé via Let's Encrypt (renouvellement auto par certbot).

---

## 🐛 Troubleshooting

### Umami ne démarre pas
```bash
docker compose logs umami
docker compose logs umami-db
```

### Erreur SSL Let's Encrypt
- Vérifie que le DNS est bien propagé : `dig analytics.moalim.online`
- Vérifie que le port 80 est ouvert (firewall)
- Lance manuellement : `certbot --nginx -d analytics.moalim.online`

### Le tracking ne marche pas
- Ouvre la console DevTools du navigateur sur moalim.online
- Cherche des erreurs sur `analytics.moalim.online/script.js` (CORS, 404…)
- Vérifie que le Website ID dans le tag `<script>` correspond à celui dans Umami

### Reset complet
```bash
cd /opt/moalim/ai-tutor-bac/deploy/umami
docker compose down -v   # ⚠️ supprime toutes les données analytics
rm .env
./install.sh             # repart de zéro
```
