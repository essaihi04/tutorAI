# Eau H₂O

**Un oxygène rouge et deux hydrogènes blancs en V.**

## Les formes

| Forme | Dessin | Couleurs | Étiquette | Quand l'utiliser | Appel |
|---|---|---|---|---|---|
| billes (défaut) | O + 2 H en V | O [235,85,70], H [235,240,245] | « H₂O » à la craie bleue | animations, loupes | `Lexique.h2o(ctx, x, y, { echelle, alpha })` |

## Où il apparaît

SVT ch1 : chaine.html (formation de l'eau), comparer.html. Chimie : `Rendu.MODELES.H2O` (commun.js) — même code (O rouge, H blanc), reste à brancher sur le lexique.

## Pourquoi ce choix

C'est le code atomique déjà utilisé par la chimie (O rouge, H blanc).

## Dessins remplacés (inventaire du 18 novembre 2026)

- `chaine.html` : une bille BLEUE [60,130,200] → O + 2 H ;
- `comparer.html` : O bleu [70,150,210] → O rouge.

Module : `frontend/public/media/simulations/shared/lexique/lexique.js` (`window.Lexique`). Index et code des couleurs : [README](README.md).
