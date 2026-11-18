# Ampèremètre, voltmètre, ohmmètre

**Appareil à cadran : boîtier sombre, cadran crème gradué, aiguille, lettre A ou V.** Ohmmètre numérique jaune.

## Les formes

| Forme | Dessin | Couleurs | Étiquette | Quand l'utiliser | Appel |
|---|---|---|---|---|---|
| à cadran | #3a3f45, cadran #fffaf0 | sombre, crème | A ou V sur le cadran | montages | `Lexique.physique.cadran(ctx, cx, cy, r, f, 'A')` |
| ohmmètre | coque #f6c84a, afficheur LCD | jaune | — | RL | `ohmmetre(ctx, x, y, w, h, '10 Ω')` |

## Où il apparaît

RC, RL, RLC.

## Pourquoi ce choix

Identique partout.

Module : `frontend/public/media/simulations/shared/lexique/lexique-physique.js`. Index et code des couleurs : [README](README.md).
