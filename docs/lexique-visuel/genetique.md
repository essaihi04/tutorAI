# Génétique : ADN, ARN, nucléotides, ribosome, ARNt, acides aminés

**ADN : squelette indigo, bases A rouge #dc2626, T jaune #ca8a04, C bleu #2563eb, G vert #16a34a ; ARN : squelette orange, U magenta #c026d3 ; ribosome : deux sous-unités turquoise ; ARNt vert pâle ; acides aminés en perles (méthionine rouge) ; noyau violet, cytoplasme rosé.**

## Les formes

| Forme | Dessin | Couleurs | Étiquette | Quand l'utiliser | Appel |
|---|---|---|---|---|---|
| peint | voir module | voir ci-dessus | lettres des bases dedans | SVT ch3, ch4 | `window.Molecules` : `brin`, `nucleotide`, `ribosome`, `arnt`, `perle`, `chaine`, `noyau`, `milieu`, `cytoplasme`, `hematie`… |

## Les lettres peintes : 15 px à l'écran au moins (19 novembre 2026)

Une lettre peinte SUR un objet (base d'un brin, anticodon d'un ARNt, nom d'un acide aminé dans sa perle, lettre d'un nucléotide libre) fait au moins 15 px une fois affichée dans le lecteur (règle 18 du skill `simulations-au-tableau`), quelle que soit la taille du cadre : `Molecules.lettreSur` mesure l'échelle réelle du contexte (`ctx.getTransform()` ÷ devicePixelRatio, ou `ctx.__echelle` pendant la mesure de la boîte de l'encre) et ne descend jamais sous `Molecules.PLANCHER` px. L'objet grandit avec sa lettre (règle 10, le texte tient dans sa forme), partout de la même façon (règle 15) :

| Objet | Dimensions réelles | Ce que la page doit faire |
|---|---|---|
| base d'un brin | `Molecules.gabarit(ctx, pas, lb)` → `{ t, w, lb, yl }` : bâtonnet plus large (jamais plus de 0,94 × pas) et plus long | dessiner une base isolée avec `Molecules.base(ctx, px, y, L, sens, pas, lb, o)` (pas de copie locale) ; poser ce qui touche le bout des bases (un ARNt sur son codon, le brin d'en face) à `gabarit(...).lb` du squelette ; garder un pas assez grand pour la lettre |
| nucléotide libre | `Molecules.gabaritNucleotide(ctx)` → `{ t, w, l }` | — |
| anticodon d'un ARNt | `Molecules.gabaritAnticodon(ctx, pas)` → `{ t, bw, bh, h }` ; l'acide aminé porté est à `yb − arntHauteur(ctx, pas) − 36` | passer le `pas` des codons ; petite icône : `{ lettres: false }` |
| perle d'acide aminé | `Molecules.perleRayon(ctx, r, nom)` | espacer les perles d'une chaîne d'au moins `2 × perleRayon + 3` |

Sans lettre (`lettres: false`, perle de rayon < 9), l'objet garde ses dimensions d'origine.

## Où il apparaît

SVT ch4 (12 pages) ; à utiliser en SVT ch3 (`Etapes.Peint` de NIG en a une autre version ; `adn.html` et `replication.html` chargent le module pour le plancher des lettres, `Molecules.taillePeinte`).

## Pourquoi ce choix

Le module du cours ch4, devenu celui du site (`shared/lexique/lexique-genetique.js`). Gardé exprès : brins de réplication (ch3) bleu / orange / blanc / rouge, dits par la voix.

Module : `frontend/public/media/simulations/shared/lexique/lexique-genetique.js`. Index et code des couleurs : [README](README.md).
