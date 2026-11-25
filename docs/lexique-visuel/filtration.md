# Filtration : entonnoir, papier filtre, précipité (flocons), éprouvette, flacons

**L'entonnoir de verre porte un papier filtre blanc plissé ; le solide retenu est en flocons blancs, le filtrat coule
goutte à goutte.** Le précipité (le savon dans l'eau salée) se peint en flocons blancs à crème, partout le même.

## Les formes

| Forme | Dessin | Couleurs | Étiquette | Quand l'utiliser | Appel |
|---|---|---|---|---|---|
| entonnoir + filtre | cône de verre, papier blanc plissé, `solide` retenu, `goutte` qui tombe | filtrat = eau salée | — | filtrer | `Lexique.chimie.entonnoir(ctx, x, y, w, h, { solide, goutte, chute })` |
| précipité | flocons blancs | `#ffffff` → `#e7e1c8` | — | un solide qui apparaît | `flocons(ctx, x, y, w, h, n, f)` |
| éprouvette graduée | verre, graduations, liquide | teinte du liquide | — | mesurer un volume | `eprouvette(ctx, x, y, w, h, niveau, col)` |
| tube à essais | verre arrondi, couches | — | — | solubilité, chauffage | `tube(ctx, x, y, w, h, { couches })` |
| flacon de produit | verre, bouchon, étiquette écrite en sombre, pictogramme corrosif | — | le nom sur l'étiquette | réactifs | `flacon(ctx, x, y, w, h, { nom, col, niveau, danger: 'corrosif' })`, `picto` |
| thermomètre, balance | colonne rouge ; afficheur vert sur fond sombre | — | la valeur sur l'afficheur | mesures | `thermometre(ctx, x, y, h, frac)`, `balance(ctx, x, y, w, h, '8 g')` |
| ion d'une eau minérale | bille, charge écrite dessus | Ca²⁺ gris bleuté (celui du lexique), Mg²⁺ turquoise, Na⁺ lilas, Cl⁻ vert clair | sa formule | eau minérale, solutions | `ion(ctx, x, y, r, 'Na⁺')` |

## Où il apparaît

Cours /TCF « Synthèse d'une espèce chimique » (traitement du savon, constantes physiques, notions).

## Pourquoi ce choix

Le dessin du cours, copié tel quel ; le bécher reste celui de [becher.md](becher.md).

Module : `frontend/public/media/simulations/shared/lexique/lexique-chimie.js`. Index et code des couleurs : [README](README.md).
