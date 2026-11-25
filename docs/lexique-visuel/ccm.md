# CCM : plaque, cuve de chromatographie, capillaire, lampe UV, diiode

**La plaque est blanche (gel de silice), la ligne de dépôt au crayon, le front en pointillé.** Les taches sont des
ellipses peintes (couleur de l'espèce, ou violet-gris une fois révélées) ; une tache entourée au crayon reçoit un cerne.
La cuve est un bocal de verre avec l'éluant au fond (bleuté pâle `[191,219,254,.45]`) ; son devant et son couvercle se
peignent APRÈS la plaque, pour qu'elle paraisse dedans.

## Les formes

| Forme | Dessin | Couleurs | Étiquette | Quand l'utiliser | Appel |
|---|---|---|---|---|---|
| plaque | rectangle blanc grenu, `ligne`, `front`, zone `mouille`, `taches: [{ u, v, col, a, r, croix, cerne }]` | blanc, ligne grise | lettres des dépôts à la craie SOUS la plaque | toute CCM | `Lexique.chimie.plaque(ctx, x, y, w, h, o)` |
| cuve | verre, éluant au fond (hauteur `he`) | éluant bleuté | — | élution | `cuve(ctx, x, y, w, h, he)` puis `cuveDevant(ctx, x, y, w, h, { couvercle })` |
| capillaire | tube fin incliné, une trace du liquide | — | — | dépôts | `capillaire(ctx, x, y, l, col)` |
| lampe UV | boîtier sombre, tube violet qui brille, faisceau | violet `[167,139,250]` | — | révélation | `lampeUV(ctx, x, y, w, allume)` |
| diiode | bocal, cristaux violet-noir, vapeurs brunes | brun `[146,64,14]` | — | révélation | `diiode(ctx, x, y, w, h, k)` |

## Où il apparaît

Cours /TCF « Synthèse d'une espèce chimique » (`chimie/tc_synthese-tableau/ccm.html`, 10 vues).

## Pourquoi ce choix

Le geste du laboratoire, pas à pas : la ligne au crayon (le graphite ne migre pas), l'éluant sous la ligne, la cuve
fermée. Les hauteurs h et H se mesurent depuis la ligne de dépôt.

Module : `frontend/public/media/simulations/shared/lexique/lexique-chimie.js`. Index et code des couleurs : [README](README.md).
