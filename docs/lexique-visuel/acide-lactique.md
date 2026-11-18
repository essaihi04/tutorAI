# Acide lactique

Fermentation lactique : **les 3 billes jaunes de l'acide pyruvique + 2 hydrogènes blancs** (rendus par le NADH,H⁺) sur le carbone du milieu.

## Les formes

| Forme | Dessin | Couleurs | Étiquette | Quand l'utiliser | Appel |
|---|---|---|---|---|---|
| billes (défaut) | 3 billes jaunes + 2 petites billes blanches au-dessus du milieu | C jaune, H blanc [235,240,245] | « acide lactique (3 C) » à la craie orange | animations | `Lexique.acideLactique(ctx, x, y, { echelle, alpha })` |
| semi-développée | CH₃–CHOH–COOH | craie | — | équation | `{ forme: 'semi_developpee' }` |
| brute | C₃H₆O₃ | craie | — | bilan | `{ forme: 'brute' }` |

## Où il apparaît

SVT ch1 : fermentations.html (référence), comparer.html, rendement.html (résidu organique). SVT ch2 : barres de jauge seulement (voies.html rose, consommation.html orange — à unifier, voir README).

## Pourquoi ce choix

C'est la forme de `fermentations.html` : l'élève voit que l'acide lactique est l'acide pyruvique qui a reçu 2 H.

## Dessins remplacés (inventaire du 18 novembre 2026)

- `comparer.html` : billes ORANGE → billes jaunes + 2 H ;
- `rendement.html` : 3 billes en arc → `acideLactique`.

Module : `frontend/public/media/simulations/shared/lexique/lexique.js` (`window.Lexique`). Index et code des couleurs : [README](README.md).
