# Voix du prof — relancer le tunnel Colab

La voix de l'application vient d'un modèle fine-tuné qui tourne **sur Colab**,
pas sur le serveur. Le serveur l'atteint par un tunnel `trycloudflare.com`
dont **l'URL change à chaque exécution du notebook**. Quand le notebook se
déconnecte, le tunnel meurt (Cloudflare *error 1033*) et les élèves n'ont
plus de voix : `/api/v1/tts/speak` répond `503`.

Ce dossier existe pour rendre cette rotation mécanique.

## La procédure

1. Ouvrir le notebook Colab **avec GPU** (Exécution → Modifier le type
   d'exécution → T4) et exécuter [cellule_colab_api.py](cellule_colab_api.py)
   dans une cellule unique. Elle attend que `/health` réponde `ok` — le
   modèle met ~1 min à charger — puis affiche l'URL et le jeton.

2. Reporter les deux valeurs dans **les deux** fichiers, qui sont ignorés par
   git et ne se synchronisent pas entre eux :

   | Fichier | Sert à |
   |---|---|
   | `backend/.env` | le développement local |
   | `deploy/backend.env` | **la production** — c'est celui qu'envoie `-UpdateEnv` |

3. Déployer :

   ```powershell
   powershell -ExecutionPolicy Bypass -Command "& { .\deploy\remote-deploy.ps1 -UpdateEnv }"
   ```

   `-UpdateEnv` suffit : seul le `.env` a changé, pas le code. `-UpdateOnly`
   ne ferait qu'un `git pull` + rebuild et **laisserait l'ancien tunnel mort**
   en place — c'est le piège classique.

4. Vérifier :

   ```powershell
   curl -X POST https://moalim.online/api/v1/tts/speak -H "Content-Type: application/json" -d '{\"text\":\"salam\",\"language\":\"mixed\"}' -D - -o NUL
   ```

   `200` + `x-tts-provider: academy` = la voix est revenue.

## Ce que ce dossier ne contient pas

`serveur_tts.py` et `normaliser_texte_darija.py` vivent sur le Drive
(`MyDrive/academy_tts/`). La cellule les copie à côté du notebook au
lancement. Ils portent le contrat de l'API (`/health`, `/voices`, `/tts`) et
restent la référence — si tu veux les versionner ici, colle-les et ils
seront ajoutés tels quels.

Les fichiers de `voix/*.wav` sont des **données de production** : la voix
vient de ces clips de 6 s, pas des poids. En changer s'entend immédiatement.

## Si la voix retombe alors que le tunnel est vivant

Les replis sont dans l'ordre : Academy → Gradio → Gemini → Google Cloud
(voir `_route()` dans `app/services/tts_service.py`). Un `provider=failed`
signifie que **tous** ont échoué. Les logs du backend disent lequel a lâché
et pourquoi :

```bash
journalctl -u moalim-backend -n 50 | grep TTS
```

Deux causes déjà rencontrées : le tunnel mort (`HTTP 530`), et une clé API
révoquée par Google pour fuite (`403 … reported as leaked`) parce qu'elle
était écrite en dur dans `app/config.py`, dépôt public. **Aucune clé ne doit
revenir dans le code** — elles vivent toutes dans les `.env`.
