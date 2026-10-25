# Voix du prof sur Kaggle, à la demande

Le modèle Academy v3 (étape 1600, entraîné dans le kernel `academy-entrainement-v3`) parle avec la voix d'Amine. Il tourne sur un GPU Kaggle (2 × T4) **seulement pendant que le prof parle**, comme un GPU loué à l'heure.

```
séance ouverte ─► backend pousse le kernel academy-tts-direct (jeton + clé neufs)
                    │  file Kaggle + chargement : ~1 à 3 min (voix de secours en attendant)
                    ▼
                  kernel : tunnel cloudflared + 1 modèle par T4
                    │  POST /api/v1/tts-kaggle/annonce {etat:"pret", url, jeton}
                    ▼
                  la voix du prof passe par le kernel (même contrat que l'ancien Colab)
                    │  5 min sans parler
                    ▼
                  le kernel s'éteint SEUL  ─►  annonce « eteint », plus de quota consommé
```

- **Moustache du tuteur 3D** : rien à brancher. L'audio arrive par le même flux `audio_stream_*` qu'avant. `Professor3D.tsx` en mesure l'amplitude syllabe par syllabe et fait pivoter l'os `Moustache` du modèle.
- **Fichiers** :
  - `serveur.py` : le kernel. `CONF` et la référence Amine sont injectées à chaque lancement.
  - `socle.py` : la préparation unique.
  - `app/services/kaggle_tts.py` : le pilote côté backend.
  - `app/api/v1/endpoints/kaggle_tts.py` : l'annonce.
  - `scripts/kaggle_tts.py` : les outils.

## Économie de quota (30 h GPU / semaine chez Kaggle)

| Mesure | Effet |
|---|---|
| Extinction après `KAGGLE_TTS_VEILLE_S` (300 s) sans requête, décidée par le kernel lui-même | aucune minute payée à attendre |
| `-t duree_max+600` au push et `KAGGLE_TTS_DUREE_MAX_S` (3 h) | même si la veille échouait, Kaggle coupe |
| `KAGGLE_TTS_BUDGET_H_SEMAINE` (25 h) sur 7 jours glissants | au-delà, plus de réveil : voix de secours |
| Pause de 3 min après un lancement raté | pas de boucle de relances |
| Socle préparé **sur CPU** | les installations ne coûtent pas de minutes GPU |
| Cache disque des phrases (clé `kaggle-v3-amine`) | une phrase déjà dite ne réveille pas de calcul |

## Démarrage le plus court

1. Le **socle** (roues pip, code lahgtna, poids de base, cloudflared) évite pip en ligne, `git clone` et le téléchargement HF à chaque réveil.
2. Le tunnel s'ouvre **pendant** le chargement des modèles.
3. Les deux T4 se chargent **en parallèle**.
4. Le réveil part **dès l'ouverture de la séance**, pas au premier mot.
5. En service :
   - la référence d'Amine n'est analysée qu'une fois ;
   - la première phrase est coupée court (≤ 90 caractères) ;
   - les deux cartes calculent les phrases suivantes pendant que la première est jouée ;
   - pas d'étirement Rubber Band, contrairement aux cours enregistrés.

Kaggle ne permet ni de garder un GPU allumé gratuitement en attente, ni d'arrêter un kernel à distance. Un démarrage à froid reste donc de l'ordre de la minute. Pendant ce temps, l'élève entend la voix de secours.

## Mise en route

1. Créer un jeton API sur https://www.kaggle.com/settings/api.
2. Dans `/etc/moalim/backend.env` (et `deploy/backend.env`), ajouter :
   ```
   KAGGLE_TTS_ACTIF=1
   KAGGLE_USERNAME=zouhairessaihi
   KAGGLE_API_TOKEN=…
   ACADEMY_TTS_URL=
   ```
   Vider `ACADEMY_TTS_URL` est voulu : l'ancien tunnel Colab est mort, et sa voix n'est pas celle d'Amine.
3. Préparer le socle une fois, sur le serveur :
   ```
   cd /opt/moalim/backend && .venv/bin/python -m scripts.kaggle_tts socle
   ```
   Attendre que `python -m scripts.kaggle_tts statut` affiche `complete`, puis ajouter `KAGGLE_TTS_SOCLE=academy-tts-socle`.
4. Redémarrer : `systemctl restart moalim-backend`.

## Suivi

- `GET /api/v1/tts-kaggle/etat` (connecté) renvoie l'état et les heures consommées sur 7 jours.
- `journalctl -u moalim-backend | grep KaggleTTS` montre le réveil, la voix prête et l'extinction.
- `python -m scripts.kaggle_tts journal` affiche les dernières lignes du kernel, dont le temps de démarrage.
