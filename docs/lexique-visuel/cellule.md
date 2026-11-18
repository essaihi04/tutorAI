# Cellule, hyaloplasme, noyau

**Cellule en coupe peinte** : hyaloplasme vert d'eau granuleux, membrane plasmique dorée (liseré net + trait fin), noyau violet avec nucléole.

## Les formes

| Forme | Dessin | Couleurs | Étiquette | Quand l'utiliser | Appel |
|---|---|---|---|---|---|
| peinte (défaut) | ellipse, ombre portée, granulations, reflet | hyaloplasme [96,200,150], membrane [250,204,96], noyau [150,110,220] | « hyaloplasme » vert, « noyau » blanc à la craie | animations | `Lexique.cellule(ctx, cx, cy, rx, ry, { noyau: {x, y, r}, grains, graine, angle })` |

## Où il apparaît

SVT ch1 : toutes les pages (via `SVTPeinture`). SVT ch3/ch4 (génétique) : cellule ROSE (`Etapes.Peint.cellule`, `Molecules.cytoplasme`), noyau violet OU BLEU — à unifier (reste à faire).

## Pourquoi ce choix

Forme de SVT ch1, déjà peinte selon la règle 32.

Module : `frontend/public/media/simulations/shared/lexique/lexique.js` (`window.Lexique`). Index et code des couleurs : [README](README.md).
