# Oscilloscope

**Coffret gris, écran vert sombre quadrillé (10 × 8), prises voie 1 / voie 2 (jaunes) et masse (noire).** La trace est lumineuse, de la couleur de la grandeur (u_C rouge, i / u_R vert, u_b violet ; en ondes : voie 1 cyan, voie 2 orange).

## Les formes

| Forme | Dessin | Couleurs | Étiquette | Quand l'utiliser | Appel |
|---|---|---|---|---|---|
| électricité | #59636d→#23292f, écran #0d3a22→#03160c | gris, vert | « voie 1 : u_C » | RL, RLC | `Lexique.physique.oscillo(ctx, x, y, w, h, ecran, prises)` |
| ondes | écran seul avec boîtier, grille nx × ny | idem | voies | ondes | `Lexique.physique.ondes.oscillo(ctx, x, y, w, h, nx, ny)` ; trace : `ondes.trace(ctx, pts, couleur)` |

## Où il apparaît

RL, RLC, ondes (micros, national), ondes périodiques.

## Pourquoi ce choix

L'écran vert est le plus répandu ; celui de dipole-rc/circuit-rc (bleu-noir) est à remplacer (reste à faire).

Module : `frontend/public/media/simulations/shared/lexique/lexique-physique.js`. Index et code des couleurs : [README](README.md).
