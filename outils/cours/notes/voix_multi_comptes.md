# Voix du tuteur sur plusieurs comptes Kaggle (11 novembre 2026)

## Plan

**Déclaration des comptes**
- Le compte principal reste `KAGGLE_USERNAME` / `KAGGLE_API_TOKEN`.
- Les comptes de secours sont des variables numérotées `KAGGLE2_USERNAME` / `KAGGLE2_API_TOKEN` … jusqu'à `KAGGLE10_…`.
  On les lit dans l'environnement : en prod, systemd charge `/etc/moalim/backend.env`. En local, on les lit dans `backend/.env`.
  Un numéro qui manque n'empêche pas de lire les suivants. L'ordre des numéros donne l'ordre de secours.
- Les poids (`academy-v5-bodi`) et le socle appartiennent à `KAGGLE_SOURCES_PROPRIETAIRE`, ou à défaut au compte principal.
  Chaque compte pousse son propre kernel `<compte>/academy-tts-direct` et lit ces notebooks partagés.

**État de chaque compte** (`CompteKaggle`, dans un seul fichier `data/kaggle_tts_etat.json`, rubrique `comptes`)
- `etat` : eteint / demarrage / pret, comme avant.
- Ce qu'on retient en plus : heures de la semaine (`sessions`), dernière erreur, pause après un échec, `repos_jusqua` (saturé, 503),
  `quota_jusqua` (quota épuisé), `pleines_jusqua` (« Maximum batch GPU session count »), `file` (morceaux en attente lus sur /health),
  URL et jeton du tunnel, clé et numéro de lancement.
- `statut()` donne un mot lisible pour l'admin : eteint, demarrage, pret, sature, quota, sessions_pleines, erreur.
- Un ancien fichier d'état (format plat) est repris comme l'état du compte principal.

**Choix du compte qui parle** (`cible()`)
- On ne garde que les comptes prêts qui ne sont pas au repos (pas de 503 récent).
- Le principal passe d'abord, sauf si sa file d'attente atteint `kaggle_tts_file_max` (6 morceaux).
- Sinon, on prend le moins chargé : la file la plus courte, puis le moins d'heures dans la semaine.
- Si tous les comptes sont chargés, on prend quand même le moins chargé : une voix lente vaut mieux que la voix de secours.

**Réveil** (`besoin_de_voix`)
- Un compte prêt et pas saturé existe : on ne réveille rien. Une exception (le réveil à l'avance) :
  - si le compte qui sert est presque saturé (file ≥ moitié du seuil, ou heures de la semaine ≥ budget),
  - et qu'aucun autre compte n'est prêt ni en démarrage,
  - alors on réveille le compte suivant.
- Aucun compte prêt et un compte en démarrage : on attend, on ne fait jamais deux réveils. Une exception :
  - si le kernel n'est toujours pas sorti de la file Kaggle après `kaggle_tts_file_kaggle_max_s` (180 s),
  - alors on réveille UN compte de plus.
- Sinon, on réveille le premier compte disponible dans l'ordre : le principal d'abord.
  Un compte n'est pas disponible s'il est en pause après un échec, au-dessus du budget, en quota épuisé, en sessions pleines ou au repos.
- Un push refusé fait trois choses :
  - il classe l'erreur : quota, sessions pleines ou autre ;
  - il met le compte en pause ;
  - il relance aussitôt `besoin_de_voix`, et le compte suivant part sans attendre la phrase suivante.

**Bascule pendant la séance**
- 503 ou tunnel mort : tts_service appelle déjà `signaler_injoignable(url)`. On retrouve le compte grâce à son URL.
  - Avec plusieurs comptes : le compte est mis au repos 90 s (il ne sert plus), puis un /health décide. S'il répond, il redevient utilisable après le repos. S'il ne répond pas, il passe à éteint. Puis `besoin_de_voix` réveille un autre compte si besoin.
  - Avec un seul compte : on garde le comportement d'avant (éteint tout de suite).
- Avec au moins deux comptes, une sonde lit `/health` des kernels prêts toutes les 20 s.
  - Elle relève `file`, le nombre de morceaux en attente (nouveau champ du kernel).
  - Deux sondes ratées d'affilée font passer le compte à éteint.
- Le compte qui sert garde `derniere_parole` à jour. Les autres s'endorment seuls après 5 min.

**Annonces** : on cherche le compte dont la clé et le numéro de lancement correspondent. L'endpoint ne change pas.

**Admin** : `resume()` garde les clés d'avant (actif, etat, depuis_s, heures_semaine, budget_h_semaine), cette fois pour tous les comptes ensemble.
Il ajoute `comptes` : une ligne par compte (nom, statut, heures, file, dernière erreur, `sert`).

**Compatibilité avec un seul compte** : on garde le même comportement, et les champs du principal restent lisibles sur `pilote`
(`pilote.cle`, `pilote.depuis`…) pour les appels existants.

## Ce qui a été codé
- Dans `backend/app/services/kaggle_tts.py` :
  - `comptes_configures()` lit les comptes ;
  - `_Porte` est un sémaphore de 2 qui compte les requêtes en attente ;
  - `CompteKaggle` porte l'état d'un compte ;
  - `PiloteKaggle` orchestre tous les comptes ;
  - `kaggle_cli(…, compte=)`, `pousser_kernel(…, compte=)` et `construire_kernel(…, compte=)` agissent pour un compte donné.
- La charge d'un compte se mesure côté backend : ce sont les requêtes de voix qui attendent la porte de son kernel.
  `tts_service._academy_sem(base)` rend maintenant la porte du kernel joint. Avant, c'était un seul `Semaphore(2)` pour tout Kaggle.
  On n'a donc plus besoin de sonder /health, et deux comptes prêts travaillent en parallèle.
- Réglages (`config.py`) :
  - `kaggle_tts_comptes_max` = 10 ;
  - `kaggle_tts_attente_max` = 3 : au-delà de 3 requêtes en attente, le compte est saturé ; dès 2, on réveille le secours à l'avance ;
  - `kaggle_tts_file_kaggle_max_s` = 180.
- `kaggle_tts_budget_h_semaine` (25 h) s'applique à chaque compte.

## Ajouter un compte Kaggle (n = 2 … 10)
1. **Créer le compte** sur kaggle.com, avec une adresse mail dédiée.
2. **Vérifier le téléphone** : Settings → Phone verification. Sans cette vérification, pas de GPU ni d'Internet dans le kernel,
   et le push échoue ou le kernel ne démarre pas. Un numéro ne vérifie qu'un seul compte.
3. **Créer le jeton** : Settings → API → « Generate New Token ». Copier la valeur `KGAT_…`, ou le `key` du `kaggle.json`.
4. **Partager les notebooks du compte principal (ferdaous04) avec le nouveau compte**, comme collaborateur
   (sur chaque notebook : Share → Add collaborators → nom du compte, droit « Can view » au moins) :
   - `ferdaous04/academy-v5-bodi` : les poids de la voix (obligatoire) ;
   - `ferdaous04/academy-moulsot-v4` : les poids MoulSot. **Obligatoire aussi**, puisque `kaggle_stt_source` est attaché au kernel ;
     s'il manque, le push est refusé ;
   - `ferdaous04/academy-tts-socle` quand on l'utilise (`KAGGLE_TTS_SOCLE`). Sans le socle, le kernel installe ses dépendances
     par Internet et démarre plus lentement.
5. **Poser le jeton sur le serveur** (moalim-vps), avec le script ci-dessous. Il demande le nom et le jeton sans les afficher,
   les écrit dans `/etc/moalim/backend.env`, puis redémarre le backend. Exemple : `bash /root/poser_kaggle.sh 3`.
6. **Vérifier.** `GET /api/v1/tts-kaggle/etat` (connecté) doit lister le compte dans `comptes`, avec le statut `eteint`.
   Le compte ne se réveille que quand les comptes d'avant sont saturés, en panne ou à court de quota.
   Pour tester : `KAGGLE_USERNAME=… KAGGLE_API_TOKEN=… kaggle kernels list --mine` depuis le serveur.
   Il faut aussi s'assurer que le compte n'a pas déjà 2 sessions GPU qui tournent.

```bash
#!/usr/bin/env bash
# /root/poser_kaggle.sh N — pose KAGGLE<N>_USERNAME / KAGGLE<N>_API_TOKEN dans /etc/moalim/backend.env
set -euo pipefail
N="${1:?usage : poser_kaggle.sh N   (2 à 10)}"
[[ "$N" =~ ^([2-9]|10)$ ]] || { echo "N doit valoir 2 à 10"; exit 1; }
ENV=/etc/moalim/backend.env
read -rp  "Nom du compte Kaggle n°$N : " NOM
read -rsp "Jeton API (KGAT_…, masqué) : " JETON; echo
[[ -n "$NOM" && -n "$JETON" ]] || { echo "nom ou jeton vide"; exit 1; }
cp -a "$ENV" "$ENV.bak.$(date +%s)"
sed -i "/^KAGGLE${N}_USERNAME=/d;/^KAGGLE${N}_API_TOKEN=/d" "$ENV"
printf 'KAGGLE%s_USERNAME=%s\nKAGGLE%s_API_TOKEN=%s\n' "$N" "$NOM" "$N" "$JETON" >> "$ENV"
chmod 600 "$ENV"
# Le jeton marche-t-il ? (sans l'afficher) — python du venv du backend
PY=$(ls /opt/moalim/backend/.venv/bin/python /root/moalim/backend/.venv/bin/python 2>/dev/null | head -1)
if [[ -n "$PY" ]] && KAGGLE_USERNAME="$NOM" KAGGLE_API_TOKEN="$JETON" "$PY" -m kaggle kernels list --mine -v >/dev/null 2>&1; then
  echo "jeton accepté par Kaggle"
else
  echo "⚠ Kaggle refuse ce jeton (ou le chemin du venv diffère) — vérifie avant de compter dessus"
fi
systemctl restart moalim-backend && echo "backend redémarré : compte $NOM en n°$N"
```
(Le venv est cherché dans `/opt/moalim/backend/.venv`, puis dans `/root/moalim/backend/.venv` : c'est le chemin du fichier `deploy/moalim-backend.service`.)
