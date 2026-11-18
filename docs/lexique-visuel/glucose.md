# Glucose

Le nutriment de référence du site (SVT ch1 énergie, SVT ch2 muscle, chimie). **Un seul dessin d'animation : la chaîne DROITE de 6 billes jaunes liées.** Ce qu'il devient se dessine à partir de lui : la chaîne se coupe au milieu → 2 × 3 billes = les deux acides pyruviques.

## Les formes

| Forme | Dessin | Couleurs | Étiquette | Quand l'utiliser | Appel |
|---|---|---|---|---|---|
| billes (défaut) | chaîne droite de 6 billes, liaisons peintes (bâtonnets gris clair) | carbone jaune [250,204,21] #facc15 ; liaison [200,200,190] | « glucose » à la craie jaune, à côté (au-dessus) ; « (6 C) » si utile | toute animation, carte du chapitre, compteur, schéma du cahier | `Lexique.glucose(ctx, x, y, { echelle, alpha, angle, etat, coupe, ecart })` — échelle 1 : billes de 12 px, pas de 28 px ; `coupe` 0→1 rompt la liaison du milieu ; `etat: 'degrade'` pâlit (règle 13) |
| brute | C₆H₁₂O₆ | craie jaune | — | équation écrite (« C₆H₁₂O₆ + 6 O₂ → … ») | `Lexique.glucose(ctx, x, y, { forme: 'brute' })` ; au tableau préférer `craie.texte('C_{6}H_{12}O_{6}')` |
| semi-développée | CH₂OH–(CHOH)₄–CHO | craie jaune | — | rappel de structure, comme au manuel | `{ forme: 'semi_developpee' }` |
| développée | chaîne linéaire de Fischer (C en jaune, O rose pâle, H blanc) | idem | — | une seule fois, en introduction | `{ forme: 'developpee' }` |
| cyclique | hexagone (5 C + 1 O) et le CH₂OH, en billes | C jaune, O rouge | « forme cyclique (manuel) » | une seule fois, puis dire « on le dessinera comme une chaîne de six carbones » | `{ forme: 'cyclique' }` |

## Où il apparaît

SVT ch1 : glycolyse.html (référence), carrefour.html (carte du chapitre), depart.html (vue glucose, et les petits glucoses du sang en `echelle: .26`), comparer.html (`echelle: .5`), atp.html (la source d'énergie, `echelle: .5`). SVT ch2 : absent (seulement à la craie, barres). Chimie : absent.

## Pourquoi ce choix

La chaîne droite est la forme de la diapositive de référence (« La glycolyse : où ? », `glycolyse.html`) et la seule qui montre la coupure en 2 × 3 : l'élève voit d'où viennent les deux acides pyruviques. Le jaune est le carbone partout (il n'est jamais l'acide pyruvique seul, ni l'électron).

## Dessins remplacés (inventaire du 18 novembre 2026)

- `carrefour.html` : deux rangées de 3 billes de 9 px → chaîne droite (`echelle: .7`) ;
- `depart.html` : anneau de 6 billes + petits hexagones au trait dans le sang → chaîne droite ; la chaîne se casse (les carbones s'écartent) ; « six carbones en anneau » → « en chaîne » (craie, `explication`, `ce_qui_se_voit`) ;
- `comparer.html` : billes BLANCHES (le jaune y était l'acide pyruvique, l'orange l'acide lactique) → billes jaunes ;
- `atp.html` : ellipse de 6 billes → chaîne droite ;
- `taxi.html` : la « molécule organique » était un anneau de 6 billes jaunes (le glucose de `depart`) → chaîne de 4 carbones (`moleculeOrganique`).

Module : `frontend/public/media/simulations/shared/lexique/lexique.js` (`window.Lexique`). Index et code des couleurs : [README](README.md).
