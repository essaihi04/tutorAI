# Lumière : couleur d'une radiation, faisceau

**Une seule fonction donne la couleur d'une longueur d'onde** (et son nom : violet < 445 nm, bleu < 490, vert < 570, jaune < 590, orange < 620, rouge).

## Les formes

| Forme | Dessin | Couleurs | Étiquette | Quand l'utiliser | Appel |
|---|---|---|---|---|---|
| couleur de λ | spectre visible 400–800 nm | — | nom de la couleur | diffraction, dispersion, spectre | `Lexique.physique.lumiere.couleurDe(λ, alpha, blanc)`, `rgbDe(λ)`, `nomCouleur(λ)` |

## Où il apparaît

Ondes lumineuses (7 copies de couleurDe avec des seuils différents).

## Pourquoi ce choix

La version de spectre.html ; les 6 autres copies sont à remplacer (reste à faire).

Module : `frontend/public/media/simulations/shared/lexique/lexique-physique.js`. Index et code des couleurs : [README](README.md).
