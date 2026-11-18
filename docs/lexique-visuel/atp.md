# ATP, ADP, Pi

L'énergie utilisable de la cellule. **ATP = carte d'énergie DORÉE marquée « ATP » ; ADP = la même carte, GRISE ; Pi = bille orange marquée « Pi ».**

## Les formes

| Forme | Dessin | Couleurs | Étiquette | Quand l'utiliser | Appel |
|---|---|---|---|---|---|
| carte (défaut) | pastille arrondie peinte 50 × 22 | ATP doré [250,190,60] ; ADP gris [150,150,150] | « ATP » / « ADP » sombre et gras dedans | compteurs, bilans, schémas | `Lexique.atp(ctx, x, y, { etat: 'atp' | 'adp', echelle, alpha })` |
| bille | petite bille dorée qui brille (ADP : bille grise + petit Pi orange) | idem | aucune (légende à côté) | foule de molécules (vésicules, compteur de 38) | `{ forme: 'bille' }` |
| développée | adénosine (masse violette) + 3 phosphates orange « P » en chaîne | adénosine [150,120,200], P [240,140,60] | « adénosine », « 3 phosphates » | la structure, une fois (atp.html) | `{ forme: 'developpee' }` |
| Pi | bille orange | [240,140,60] | « Pi » | partout | `Lexique.pi(ctx, x, y, o)` |

## Où il apparaît

SVT ch1 : glycolyse, chaine, compteur, krebs, atp, vesicules, comparer. SVT ch2 (muscle) : `MoleculesPeintes.pastille` en VERT, jauges vertes, barres jaunes — à unifier (reste à faire).

## Pourquoi ce choix

Le doré est la forme la plus répandue (8 pages de SVT ch1) ; il se distingue du jaune des carbones.

## Dessins remplacés (inventaire du 18 novembre 2026)

- `vesicules.html` : ATP en bille JAUNE [250,204,21] (couleur du carbone) → doré ; Pi VIOLET [200,160,230] (couleur des protéines) → orange ;
- `comparer.html` : pastilles locales → `atp({ forme: 'bille' })`.

Module : `frontend/public/media/simulations/shared/lexique/lexique.js` (`window.Lexique`). Index et code des couleurs : [README](README.md).
