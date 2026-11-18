# Verrerie : bécher, bain, goutte, pipette, compte-gouttes

**Bécher en verre net à bord ourlé, eau claire et lumineuse, ménisque, reflets, graduations.** Une solution incolore se peint comme une eau un peu bleutée `[112,194,248,.36]`.

## Les formes

| Forme | Dessin | Couleurs | Étiquette | Quand l'utiliser | Appel |
|---|---|---|---|---|---|
| bécher | verre + solution (couleur passée) | solution | — | partout | `Lexique.chimie.becher(ctx, {x,y,w,h}, niveau, [r,g,b,a])` |
| bain | eau d'un cristallisoir par-dessus | — | — | température | `bain(ctx, B, ySurf, col)` |
| goutte, filet | goutte qui tombe, filet versé | couleur de la solution | — | ajouts | `goutte(ctx, x, y, col)`, `filet(ctx, x, y1, y2, col)` |
| pipette, compte-gouttes | poire rouge | — | — | prélèvements | `pipette(ctx, x, yp, rempli, col)`, `compteGouttes(ctx, x, yp, col)` |

## Où il apparaît

Toute la chimie : le bécher était recopié dans 25 pages.

## Pourquoi ce choix

La copie la plus répandue (20 pages, + 5 identiques au commentaire près).

Module : `frontend/public/media/simulations/shared/lexique/lexique-chimie.js`. Index et code des couleurs : [README](README.md).
