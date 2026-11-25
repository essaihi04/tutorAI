# Atome : noyau, nuage électronique, couches K L M, ions

Ajouté le 25 novembre 2026 pour le cours de Tronc Commun « Modèle de l'atome » (`chimie/tc_atome-tableau/`) ; à reprendre
tel quel dans tout cours qui montre un atome (physique nucléaire, liaisons chimiques, tableau périodique…).

**Le noyau est un amas serré de billes roses « + » (protons) et grises (neutrons) avec un halo rose ; le nuage est une
brume bleu ciel où sont posés les électrons (billes bleu ciel « e− ») ; une couche K, L ou M est un anneau fin bleu pâle,
jaune quand on la montre ; la charge d'un ion est un anneau pointillé autour de l'atome : rose (cation, +), bleu ciel (anion, −).**
Les couleurs sont celles des particules ([proton](proton.md), [neutron](neutron.md), [électron](electron.md)) : le rose
dit « + », le bleu ciel dit « − », partout.

## Les formes

| Forme | Dessin | Couleurs | Étiquette | Quand l'utiliser | Appel |
|---|---|---|---|---|---|
| noyau | amas en spirale serrée de Z + N billes (r 9 par défaut), protons et neutrons mêlés de façon fixe, halo rose | proton [244,114,182] « + », neutron [160,168,180] | « + » sur les protons ; un numéro quand on compte | partout où l'on montre un noyau | `Lexique.noyau(ctx, cx, cy, Z, N, { r, alpha, pale, numeros, compte })` → `{ pos, R }` |
| noyau compté | le même, les k premiers nucléons (ou protons, ou neutrons) allumés d'un halo jaune avec leur numéro | halo jaune [250,204,21] | numéros 1…k | compter A, Z, N | `noyau(…, { compte: { mode: 'tous' \| 'p' \| 'n', k, palir } })` |
| nuage électronique | brume radiale bleu ciel, plus dense au centre, poussière de points | [96,200,250] | — | le modèle actuel de l'atome | `Lexique.nuage(ctx, cx, cy, R, { alpha, points, graine })` |
| électrons du nuage | places fixes entre 0,42 R et 0,88 R, rotation lente | électron | « e− » | | `Lexique.placesNuage(cx, cy, R, n, { t, graine })` |
| couche K, L, M | anneau fin | [186,230,253] α .6 ; allumée : jaune + lueur | « K », « L », « M » à la craie à côté | structure électronique, modèle de Bohr | `Lexique.couche(ctx, cx, cy, R, { vive, alpha })` |
| places d'une couche | K : 2 (haut, bas) ; L, M : 8 (4 paires aux points cardinaux) ; place vide en pointillé | | | remplir les couches | `Lexique.placesCouche(cx, cy, R, cap)`, `placeVide(ctx, x, y, r)` ; `CAPACITE = [2, 8, 8]`, `repartition(n)` |
| atome entier | noyau + nuage + électrons, ou noyau + couches + électrons | | | | `Lexique.atomeModele(ctx, cx, cy, Z, N, { forme: 'nuage' \| 'couches', R, rn, re, ne, t, charge })` |
| ion | anneau pointillé autour de l'atome + la charge écrite en haut à droite (« + », « 2− ») | cation rose, anion bleu ciel | `+`, `−`, `2+`, `2−` | Na⁺, Cl⁻, O²⁻, Cu²⁺… | `Lexique.charge(ctx, cx, cy, R, q, { texte, alpha })` |

Allumer en comptant : `Lexique.allume(ctx, x, y, r, vive)` (halo jaune doux ; `vive` pour le dernier).

## Pourquoi ce choix

Le halo rose du noyau et la brume bleu ciel du nuage répètent la charge de ce qu'ils contiennent (+ rose, − bleu ciel,
comme H₃O⁺ et HO⁻ du lexique). Les couches restent pâles pour ne pas rivaliser avec les électrons ; le jaune (craie des
mots-clés) les allume quand la voix les nomme.

Module : `frontend/public/media/simulations/shared/lexique/lexique.js` (`window.Lexique`). Index et code des couleurs : [README](README.md).
