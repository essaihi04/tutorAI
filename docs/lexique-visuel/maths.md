# Maths : une couleur par rôle

En maths, les objets sont des rôles ; chacun a sa couleur de craie dans les six cours.

## Les formes

| Forme | Dessin | Couleurs | Étiquette | Quand l'utiliser | Appel |
|---|---|---|---|---|---|
| courbe | tracé lumineux | cyan (2ᵉ courbe : violet) | C_f | partout | `Lexique.maths.ROLES.courbe` |
| point | rond plein / évidé | jaune | M, A | partout | `K.rond(G, x, y, plein, ROLES.point)` |
| tangente | segment | orange | (T), pente | dérivation, ln, primitives | `Lexique.maths.tangente(c, G, x0, y0, pente)` |
| asymptote | droite en pointillé [8, 6] | blanc | x = a, y = b | limites, dérivation, ln | `Lexique.maths.asymptote(c, G, {x}|{y}|{a,b})` |
| signes | + / −, zones | vert / rouge | — | tableaux, aires | `Lexique.maths.couleurSigne(s)` |
| repère | axes, graduations, projections | faible | O, x, y | partout | `K.axes` |

## Où il apparaît

Limites, dérivation, suites, primitives, ln, complexes.

## Pourquoi ce choix

La couleur la plus répandue de chaque rôle, sauf la tangente : orange plutôt que jaune, pour ne jamais se confondre avec le point (jaune dans 63 appels). Exception gardée : la courbe de ln est rouge dans tout le cours ln (objet nommé).

Module : `frontend/public/media/simulations/shared/lexique/lexique-maths.js`. Index et code des couleurs : [README](README.md).
