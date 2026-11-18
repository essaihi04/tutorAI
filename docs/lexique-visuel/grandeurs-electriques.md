# Couleurs des grandeurs électriques

Une grandeur garde sa couleur de craie partout (flèche, nom, courbe, barre d'énergie). Code dit par la voix des cours d'électricité (ch6 à ch8).

## Les formes

| Forme | Dessin | Couleurs | Étiquette | Quand l'utiliser | Appel |
|---|---|---|---|---|---|
| condensateur | u_C, q, E_e | rouge | — | flèches, courbes, barres | `Lexique.physique.GRANDEURS.u_C` |
| courant | i, u_R (= R·i), E_m (∝ i²) | vert | — | idem | `GRANDEURS.i` |
| bobine | u_b | violet | — | idem | `GRANDEURS.u_b` |
| générateur, total | E, u_G, E totale | blanc | — | idem | `GRANDEURS.E` |
| charges | + / − | rose / bleu | — | armatures | `GRANDEURS.plus` |

## Où il apparaît

RC, RL, RLC.

## Pourquoi ce choix

La voix dit « la courbe rouge, c'est u C », « la courbe verte de i / de u R », « la barre rouge (condensateur), la verte (bobine) », « la courbe blanche, E ». Exceptions dites par la voix et gardées : ch6, colonne « charge » rouge / « décharge » bleue et flèche de i qui s'allume en rouge. À aligner (reste à faire) : i blanc, bleu ou rose et u_C jaune dans quelques pages de RC/RL.

Module : `frontend/public/media/simulations/shared/lexique/lexique-physique.js`. Index et code des couleurs : [README](README.md).
