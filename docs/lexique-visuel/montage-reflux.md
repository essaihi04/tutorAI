# Montage du chauffage à reflux : ballon, réfrigérant à boules, chauffe-ballon, potence, support élévateur

**Un seul montage, assemblé de bas en haut, peint en verre net et métal.** Le réfrigérant à boules est vertical, ses deux
tubulures à droite : l'eau froide (bleue) **entre en bas et sort en haut**. Le ballon a un col droit et une panse ronde ;
son contenu est peint en couches (huile dorée, mélange jaune pâle…), avec la pierre ponce au fond et les bulles de
l'ébullition. Pendant le reflux, les vapeurs blanches montent, se condensent en gouttelettes sur les boules et retombent.

## Les formes

| Forme | Dessin | Couleurs | Étiquette | Quand l'utiliser | Appel |
|---|---|---|---|---|---|
| montage assemblé | potence, élévateur, chauffe-ballon, ballon, réfrigérant, tuyaux ; `k` fait paraître chaque pièce | eau froide bleue, cuvette qui rougeoie | légendes à la craie à côté (`G.ancres`), repères `G.boites` | toute synthèse chauffée à reflux | `Lexique.chimie.montageReflux(ctx, cx, yTable, { s, k, couches, ponce, bulles, agite, chaud, phase, vapeur, ouvert })` |
| sans réfrigérant | `ouvert: true` : le col reste ouvert, les vapeurs s'échappent | vapeurs blanches | — | comparer « chauffage sans réfrigérant » | idem |
| ballon seul | col droit, panse ronde, reflet en arc | contenu en `couches` | — | contenu d'un ballon | `ballon(ctx, x, y, r, { couches, ponce, bulles, agite, flocons })` |
| réfrigérant à boules | manchon + tube à 5 boules | eau `[37,99,235]` → `[147,197,253]` | « entrée de l'eau froide » en bas, « sortie de l'eau » en haut | — | `refrigerant(ctx, x, yHaut, yBas, { w, eau, phase, boules })` |
| chauffe-ballon | coque sombre, cuvette orange quand `chaud` → 1, voyant rouge | — | — | chauffer | `chauffeBallon(ctx, x, y, w, h, chaud)` |
| potence, élévateur, tuyau | socle + tige + noix et pinces ; ciseaux ; caoutchouc rouge sombre (bleu quand l'eau coule) | — | — | — | `potence`, `elevateur`, `tuyau` |
| pierre ponce, vapeur, gouttelette | caillou gris poreux ; volute blanche ; goutte bleutée | — | — | ébullition, reflux | `ponce`, `vapeur`, `gouttelette` |

Les teintes des liquides : `Lexique.chimie.LIQUIDES` (huile `[234,179,8,.72]`, éthanol, soude, mélange `[250,224,140,.6]`,
eau salée, éluant, eau…).

## Où il apparaît

Cours /TCF « Synthèse d'une espèce chimique » (`chimie/tc_synthese-tableau/` : montage, reflux, traitement, application).

## Pourquoi ce choix

Le ballon est celui de la chimie de 2ᵉ Bac (`chimie/shared/chem-lab.js`) ; l'entrée de l'eau en bas est la règle du
laboratoire (le réfrigérant reste plein d'eau froide).

Module : `frontend/public/media/simulations/shared/lexique/lexique-chimie.js`. Index et code des couleurs : [README](README.md).
