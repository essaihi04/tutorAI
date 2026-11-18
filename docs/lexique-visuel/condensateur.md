# Condensateur

**Réaliste : condensateur chimique bleu debout, bande claire « − », deux pattes.** **Symbole : deux traits parallèles (craie blanche)**. Les charges des armatures : + en sphères rouges, − en sphères bleues (`armatures`) ; à la craie : + rose, − bleu (code des grandeurs).

## Les formes

| Forme | Dessin | Couleurs | Étiquette | Quand l'utiliser | Appel |
|---|---|---|---|---|---|
| réaliste | cylindre bleu #0b2a6b→#2f6fe0, chapeau #9aa3ad | bleu | « C = 220 µF » à la craie | montages | `Lexique.physique.condensateur(ctx, x, y, w, h)` (= `chimique`) |
| armatures chargées | deux plaques métal + charges qui apparaissent | + rouge, − bleu | A, B | charge / décharge | `armatures(ctx, x, yA, yB, f)` |
| symbole | deux traits de 40 px | craie blanche (épaisseur 3,4) | C, A et B | schéma, cahier | `Lexique.physique.symboleCondo(c, x, y1, yA, yB, y2)` |

## Où il apparaît

RC, RLC.

## Pourquoi ce choix

Le cylindre bleu de `Peint.chimique` était dans 8 pages ; `condensateurPeint`/`condoPeint` (carte, figures, energie) en sont des copies d'un autre bleu, à brancher (reste à faire).

Module : `frontend/public/media/simulations/shared/lexique/lexique-physique.js`. Index et code des couleurs : [README](README.md).
