# Acide pyruvique

La moitié du glucose : **3 billes jaunes liées, coupées dans la chaîne du glucose.**

## Les formes

| Forme | Dessin | Couleurs | Étiquette | Quand l'utiliser | Appel |
|---|---|---|---|---|---|
| billes (défaut) | chaîne droite de 3 billes | carbone jaune | « acide pyruvique (3 C) » à la craie jaune | animations | `Lexique.acidePyruvique(ctx, x, y, { echelle, alpha, alphas, liaisons })` — `alphas` pour le 3e carbone qui part en CO₂ |
| semi-développée | CH₃–CO–COOH | craie jaune | — | équation écrite comme au bac | `{ forme: 'semi_developpee' }` |
| brute | C₃H₄O₃ | craie jaune | — | bilan | `{ forme: 'brute' }` |

## Où il apparaît

SVT ch1 : glycolyse, carrefour, comparer, pyruvate, fermentations, krebs (avant décarboxylation).

## Pourquoi ce choix

Dessiné à partir du glucose (règle 15) : mêmes billes, même pas.

## Dessins remplacés (inventaire du 18 novembre 2026)

- `comparer.html` : les acides pyruviques étaient la SEULE molécule jaune (le glucose était blanc) → le carbone est jaune partout.

Module : `frontend/public/media/simulations/shared/lexique/lexique.js` (`window.Lexique`). Index et code des couleurs : [README](README.md).
