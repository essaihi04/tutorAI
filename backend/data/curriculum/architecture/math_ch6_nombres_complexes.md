# Architecture — `math_ch6_nombres_complexes` (Nombres complexes, partie 1 : opérations et formes, 2e Bac PC BIOF)

Refonte de la logique du 18 novembre 2026 (skill `logique-de-cours`). Cours en ligne inchangé ; nouvelle version dans `backend/data/courses/en_attente/math_ch6_nombres_complexes.json` (partie de la version en attente, plus récente). Pistes à mettre en voix : `math_ch6_nombres_complexes_voix.json` (52 pistes après la 2ᵉ passe du 18 novembre 2026, voir § 8).

## 1. La logique avant

Ouverture puis **cinq rappels d'affilée** (repère, vecteur, Pythagore, cercle trigonométrique, développer) → I. le nombre i et la forme algébrique → II. calcul algébrique → III. plan complexe, affixes → IV. conjugué → V. module, distance, ensembles de points → VI. argument → VII. forme trigonométrique → VIII. produit, quotient, Moivre → IX. géométrie → X. deux sujets nationaux → bilan.

Ce qui allait déjà : la figure est partout (demande de l'utilisateur). i est un quart de tour (a2) ; a + ib est lu sur le point (a3) ; le conjugué est un reflet (j1) ; le module est la distance OM par Pythagore (m1) ; l'argument est l'angle du point qui tourne (g1) ; le produit fait tourner (r1), multiplier par i est un quart de tour (r2), Moivre est une spirale (r6) ; l'alignement se voit en tirant C hors de la droite (i1). L'ordre des parties est celui des profs.

Ce qui n'allait pas :
1. **Les cinq rappels arrivaient avant le premier nombre complexe**. Pythagore était vu deux séances avant le module, le cercle trigonométrique quatre séances avant l'argument. Le bloc d'ouverture comptait quatre diapositives de rappels.
2. **La forme trigonométrique du national (t2, 2023 N) était dite en entier**, alors qu'elle tombe dans 17 sujets sur 20.
3. **Le sujet 2023 N entier (n1) tenait sur une diapositive** : quatre questions et leurs réponses dites d'un bloc (« on remplace, et on regroupe les i »), sans une seule réponse de l'élève.
4. **L'alignement (9 sujets sur 20)** : i1 posait les données du national 2021 R sans rien demander.
5. **Le cadre** : la compétence K8 couvrait l'angle de deux vecteurs (NC11) et les ensembles de points (NC12) sans les citer.

## 2. Les sources et ce qu'elles disent
- **Profs en vidéo** (`exploration/operations_formes.json`) :
  - i² = −1 et l'écriture unique a + ib (10 profs) ;
  - le quotient par le conjugué (7 profs) ;
  - le module √(a² + b²) sans le i, c'est la distance OM (10 profs) ;
  - la forme trigonométrique en trois temps (9 profs) ;
  - le produit : modules multipliés, arguments additionnés (6 profs) ;
  - AB = |z_B − z_A| (7 profs).
- **Cours écrits en ligne** (lus le 18/11) :
  - Atmani (moutamadris, parties 1 et 2, et résumé) : ℂ → opérations → interprétation géométrique (affixes, milieu, alignement) → conjugué → module → forme trigonométrique et argument → angles et alignement. Moivre en partie 2.
  - Benmoussa (moutamadris) : approche → opérations → représentation → conjugué → module → argument → forme trigonométrique → opérations et Moivre.
  - Cheddadi (AlloSchool, séance 9) : introduction → représentation → conjugué → module → argument → forme trigonométrique → opérations et Moivre ; la partie 2 contient l'exponentielle, le second degré et les transformations.
  - Atlasmaths (fiche SE) : ordre différent (géométrie à la fin, après l'exponentielle).
  - **Ordre commun** : forme algébrique → plan → conjugué → module → argument → forme trigonométrique → opérations et Moivre → géométrie. Notre ordre est le même. L'exponentielle et le second degré restent en partie 2, comme chez tous.
- **Cadre** : NC1 à NC12, tous travaillés. Rien hors cadre : pas de racines n-ièmes, pas de coefficients complexes, pas d'exponentielle ici (annoncée pour la partie 2).
- **National** : forme trigonométrique 17 sujets sur 20, forme algébrique 13, quotient 10, conjugué 10, distance 10, alignement 9, opérations sur les arguments 6, puissance 6, milieu 3, égalité 0. Les exercices animés sont donc mis sur la forme trigonométrique (t2), l'alignement (i1, n1_b) et un sujet entier (n1 à n1_c).

## 3. Les décisions et leurs raisons

| Décision | Raison |
|---|---|
| Chaque rappel juste avant la diapositive qui s'en sert | Repère avant a3, développer avant c1, vecteur avant p3, Pythagore avant m1, cercle avant g1. C'est la règle 6. La première phrase de chaque rappel est réécrite pour dire à quoi il sert : avant, elles disaient « un, deux, trois… ». |
| t2 : l'élève fait les lignes 2 à 4 | 17 sujets sur 20. La voix fait la ligne du module ; la question demande la forme complète ; la démonstration est écrite comme le barème. |
| n1 coupé en trois diapositives | n1 : données, puis l'élève calcule b − d. n1_b : la correction, puis l'élève conclut à l'alignement. n1_c : la correction, puis l'élève passe aux arguments. Une consigne à la fois (règle 5), sur les moments déjà présents de `calculs.html?vue=n1` (donnees, q1, q2, q3, alignes, q4). Les deux questions 3 et 4 reprennent les exercices de fin de cours, avec leurs réactions déjà écrites. |
| i1 : l'élève calcule le quotient du national 2021 R | La voix posait déjà les données sans les traiter ; la question vient au bon moment, et la voix de la diapositive est gardée. L'exercice de fin de cours A(1), B(2 + i), C(4 + 3i) devient l'exemple jumeau. |
| K8 cite NC11 et NC12 | Règle 8 : chaque capacité travaillée est citée. |
| Blocs recoupés | Au plus quatre diapositives par bloc. Trois « retrouver » ou exercices sont écrits pour coller aux nouveaux blocs (i², puissances de i, quotient, alignement) ; le bloc final est séparé en « sujet 2023 » et « 2024, bilan, carte ». |

## 4. Ce qui ne change pas, et pourquoi
57 diapositives gardent leur texte et leur voix. Les cinq rappels sont aussi déplacés, mais leur première phrase change, donc leur voix est à refaire. Les animations du plan (point, module, argument, rotation, spirale) servent déjà chacune une étape, et chaque partie suit l'ordre commun des profs.

## 5. Animations
Aucun fichier de simulation n'est modifié. Les nouvelles diapositives n1_b et n1_c rejouent `calculs.html?vue=n1` jusqu'aux moments utiles. Les moments `conclusion` et `partie2`, qui écrivaient la réponse de la question 4, ne sont plus joués avant la réponse.

Besoin noté à la 1ʳᵉ passe (`n1` en figure) : FAIT à la 2ᵉ passe, voir § 8.

## 6. Mots et voix
Chaque texte réécrit a été vérifié par `scripts/voix/verifier_mots.py`.
- Mots rares remplacés : « وقارنو » → « وقارن » ; « تنقصو » → « تحيدو » ; « كيمنع » → « كيخلي … ماشي alignés » ; « بالأزرق » → « بلون bleu » (pointage mis à jour).
- Gardés et à écouter :
  - dans les rappels, déjà dits par la voix : « كنكتبوها », « كنقسموه », « كيتحيدو », « حاطينها » ;
  - termes du programme : « côtés », « Pythagore », « carrés », « congru », « modulo », « arguments ».
- Pistes à faire : 9 diapositives, 6 démonstrations, 36 réactions et énoncés.

## 7. Le plan, diapositive par diapositive
Légende : ↕✎ déplacée, première phrase réécrite (voix à refaire) · ✎ réécrite · ＋ nouvelle · ＋❓ question ajoutée (voix de la diapositive gardée).

### Séance 1 — Le nombre i et la forme algébrique


**Bloc `nc_s1_b0` — Une équation sans solution réelle ; le nombre i** · fin de bloc : cahier (3 lignes, 1 figure(s)), retrouver « Cahier fermé : quel est le carré de i ? », exercice « (2i)² = ? »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `nc_o1` La carte du chapitre : le nombre qui fait tourner | Ouverture | — | Le but : chaque complexe est un point du plan ; la carte suit l'ordre du national (un exercice de complexes dans 20 sujets sur 20). |
|  | `nc_a1` Une équation sans solution réelle | I. Le nombre i et la forme algébrique | — | Le besoin d'abord : x² = −1 n'a pas de solution sur la droite (les carrés sont tous ≥ 0, vus sur la droite graduée). |
|  | `nc_a2` Le nombre i : un quart de tour | I. Le nombre i et la forme algébrique | ❓ (√2 i)² = ? · ✏️ (3i)² = ? | i construit par la figure : × (−1) est un demi-tour, donc i est un quart de tour ; i² = −1 en découle. L'élève calcule (√2 i)². |

**Bloc `nc_s1_b1` — Rappel : le repère ; la forme algébrique, réels et imaginaires purs** · fin de bloc : cahier (3 lignes), retrouver « Cahier fermé : écris la forme algébrique d'un complexe z et nomme ses parties. », exercice « Re(−2 + 7i) et Im(−2 + 7i) valent : »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
| ↕✎ | `nc_z1_repere` Rappel : un point, deux coordonnées | I. Le nombre i et la forme algébrique | — | DÉPLACÉE (était dans les cinq rappels du début) : le repère sert à la diapositive suivante, où 3 + 2i devient le point M(3 ; 2). Première phrase réécrite (« Pour placer un nombre complexe… »). |
|  | `nc_a3` La forme algébrique z = a + ib | I. Le nombre i et la forme algébrique | — | La forme algébrique a + ib lue sur le point du plan (Re en vert, Im en orange) : la figure avant l'écriture. |
|  | `nc_a4` Réels et imaginaires purs | I. Le nombre i et la forme algébrique | — | Réels et imaginaires purs : les deux axes. |

**Bloc `nc_s1_b2` — Égalité, puissances de i ; rappel : développer ; somme et produit** · fin de bloc : cahier (4 lignes), retrouver « Cahier fermé : que vaut i⁴, et comment calcule-t-on i²⁰²⁶ ? », exercice « (1 + 2i)(3 − i) = ? »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `nc_a5` Égalité de deux complexes : deux équations | I. Le nombre i et la forme algébrique | — | Égalité de deux complexes (0 sujet au national, mais nécessaire pour j5 et m6 : équations avec z̄, ensembles de points). |
|  | `nc_a6` Les puissances de i reviennent tous les quatre | I. Le nombre i et la forme algébrique | ❓ i²⁰²⁶ = ? · ✏️ i¹⁵ = ? · 👀 observation | Les puissances de i : le quart de tour répété (observation), puis i²⁰²⁶. |
| ↕✎ | `nc_z5_identites` Rappel : développer, les identités remarquables | II. Calculer sous forme algébrique | — | DÉPLACÉE : développer et les identités servent à la diapositive suivante (produit) et en c2–c3. Première phrase réécrite. |
|  | `nc_c1` Somme et produit : on développe, i² = −1 | II. Calculer sous forme algébrique | — | Somme et produit : développer, i² = −1 (forme algébrique, 13 sujets sur 20). |

### Séance 2 — Calcul algébrique, affixes, parallélogramme


**Bloc `nc_s1_b3` — Carré, conjugué, quotient** · fin de bloc : cahier (3 lignes), retrouver « Cahier fermé : que vaut (a + ib)(a − ib) ? », exercice « (2 + i)/(1 − i) = ? »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `nc_c2` Carré et puissance : (1 + i)² = 2i | II. Calculer sous forme algébrique | — | (1 ± i)² = ±2i : une identité, puis les puissances. |
|  | `nc_c3` Un complexe fois son conjugué : un réel | II. Calculer sous forme algébrique | — | z·z̄ = a² + b², trouvé sur un exemple avant la formule. |
|  | `nc_c4` Le quotient : multiplier par le conjugué du dénominateur | II. Calculer sous forme algébrique | ❓ (1 + 3i)/(1 − i) = ? · ✏️ 1/(1 + i) = ? | Le quotient par le conjugué du dénominateur (10 sujets sur 20, 7 profs). |

**Bloc `nc_s2_b1` — Un complexe, un point ; rappel : le vecteur ; l'affixe d'un vecteur** · fin de bloc : cahier (4 lignes, 1 figure(s)), retrouver « Cahier fermé : écris l'affixe du vecteur AB⃗. », exercice « Le point B(0 ; −3) a pour affixe : »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `nc_p1` Le plan complexe : un complexe, un point | III. Le plan complexe : affixes, parallélogramme | — | Le plan complexe, repère orthonormé direct (O, u⃗, v⃗). |
|  | `nc_p2` L'affixe d'un point | III. Le plan complexe : affixes, parallélogramme | — | L'affixe d'un point. |
| ↕✎ | `nc_z2_vecteur` Rappel : un vecteur, un déplacement | III. Le plan complexe : affixes, parallélogramme | — | DÉPLACÉE : les coordonnées d'un vecteur (arrivée − départ) servent à la diapositive suivante. Première phrase réécrite. |
|  | `nc_p3` L'affixe d'un vecteur : arrivée moins départ | III. Le plan complexe : affixes, parallélogramme | — | L'affixe d'un vecteur : la flèche glisse jusqu'à O (7 profs : z_B − z_A). |

**Bloc `nc_s2_b1b` — Le milieu ; le parallélogramme** · fin de bloc : cahier (2 lignes, 1 figure(s)), retrouver « Cahier fermé : quand ABCD est-il un parallélogramme ? Écris-le avec les affixes. », exercice « Vrai ou faux ? »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `nc_p4` L'affixe du milieu | III. Le plan complexe : affixes, parallélogramme | ❓ a = 1 + 2i et b = 1 − 2i : quelle est l'affixe p du milieu P de [AB] ? (2025 N) · ✏️ A(2 + 3i), B(4 − i) : l'affixe du milieu I de [AB] est : | Le milieu (3 sujets, dont 2025 N) ; l'élève calcule p. |
|  | `nc_p5` Le parallélogramme : deux vecteurs égaux | III. Le plan complexe : affixes, parallélogramme | — | Le parallélogramme : deux vecteurs égaux. |

### Séance 3 — Conjugué, équation avec z̄, module


**Bloc `nc_s2_b2` — Le conjugué : le reflet ; reconnaître un réel** · fin de bloc : cahier (3 lignes, 1 figure(s)), retrouver « Cahier fermé : écris le conjugué de z = a + ib, et quand z est réel. », exercice « z = 1 + i : quel est le conjugué de z² ? »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `nc_j1` Le conjugué : le reflet dans l'axe réel | IV. Le conjugué | — | Le conjugué : le reflet dans l'axe réel (la figure avant le calcul). |
|  | `nc_j2` Le conjugué passe à travers les opérations | IV. Le conjugué | — | Le conjugué passe à travers les opérations, vérifié sur un exemple d'abord. |
|  | `nc_j3` z̄ = z : reconnaître un réel | IV. Le conjugué | — | z̄ = z ⇔ z réel : le point posé sur l'axe miroir. |

**Bloc `nc_s2_b2b` — z + z̄, z − z̄ et z·z̄** · fin de bloc : cahier (2 lignes), retrouver « Cahier fermé : écris z + z̄ et z − z̄. », exercice « z = 3 − 4i : combien vaut z + z̄ ? »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `nc_j3_b` z + z̄ et z − z̄ | IV. Le conjugué | — | z + z̄ et z − z̄. |
|  | `nc_j4` z·z̄ = a² + b² | IV. Le conjugué | ❓ c = √2 + i√2 : combien vaut c·c̄ ? (2020 N) · ✏️ (3 + 4i)(3 − 4i) = ? | z·z̄ = a² + b² (national 2020) ; l'élève calcule c·c̄. |

**Bloc `nc_s2_b3` — Une équation avec z̄ ; rappel : Pythagore ; le module, une distance** · fin de bloc : cahier (3 lignes, 1 figure(s)), retrouver « Cahier fermé : écris le module de z = a + ib. », exercice « |−3 + 4i| = ? »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `nc_j5` Résoudre une équation avec z̄ | IV. Le conjugué | — | Équation avec z̄ (se ramène à l'égalité de a5). |
| ↕✎ | `nc_z3_pythagore` Rappel : Pythagore et la distance OM | V. Le module, la distance et les ensembles de points | — | DÉPLACÉE : Pythagore sert à la diapositive suivante (le module = OM). m1 reprend la même figure pour lui donner son nom : deux passages, deux façons (règle 6). Première phrase réécrite. |
|  | `nc_m1` Le module : une distance | V. Le module, la distance et les ensembles de points | — | Le module, une distance (10 profs : √(a² + b²) sans le i). |

### Séance 4 — Propriétés du module, distance, ensembles de points


**Bloc `nc_s2_b3b` — Le module sans le i ; produit, quotient, puissance, somme ; la distance AB** · fin de bloc : cahier (4 lignes), retrouver « Cahier fermé : écris la distance AB avec les affixes. », exercice « Vrai ou faux ? »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `nc_m2` Calculer un module sans le i | V. Le module, la distance et les ensembles de points | — | Calculer un module sans le i : le cercle de rayon fixe. |
|  | `nc_m3` Le module d'un produit | V. Le module, la distance et les ensembles de points | — | |zz′| = |z|·|z′| sur le national 2017 : on ne développe pas. |
|  | `nc_m3_b` Quotient, puissance… et le piège de la somme | V. Le module, la distance et les ensembles de points | — | Quotient, puissance… et le piège de la somme. |
|  | `nc_m4` La distance AB = |z_B − z_A| | V. Le module, la distance et les ensembles de points | ❓ a = 3 − 2i et b = 1 + 4i : calcule AB. · ✏️ A(1 + i), B(4 + 5i) : AB = ? | La distance AB = |z_B − z_A| (10 sujets sur 20) ; l'élève calcule. |

**Bloc `nc_s2_b3c` — Ensembles de points : cercle, médiatrice, droite** · fin de bloc : cahier (2 lignes, 1 figure(s)), retrouver « Cahier fermé : quel est l'ensemble des points M(z) tels que |z − z_A| = r (r > 0) ? », exercice « L'ensemble des points M(z) tels que |z − 1 + i| = 2 est : »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `nc_m5` Ensembles de points : le cercle et la médiatrice | V. Le module, la distance et les ensembles de points | — | Ensembles de points : cercle, médiatrice (NC12). |
|  | `nc_m6` Ensemble des points M tels que Z soit réel | V. Le module, la distance et les ensembles de points | ❓ Même Z = (1 + i)z − 2i, avec z = x + iy : Z est imaginaire pur ⇔ | Z réel → une droite (NC12) ; question sur Z imaginaire pur. |

### Séance 5 — Argument et forme trigonométrique


**Bloc `nc_s3_b1` — Rappel : le cercle trigonométrique ; l'argument, un angle à 2π près** · fin de bloc : cahier (4 lignes, 1 figure(s)), retrouver « Cahier fermé : pourquoi écrit-on [2π] après un argument ? », exercice « arg z ≡ π/4 [2π]. Lequel est aussi un argument de z ? »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
| ↕✎ | `nc_z4_cercle` Rappel : le cercle trigonométrique | VI. L'argument | — | DÉPLACÉE : π, cos θ et sin θ sur le cercle servent à la diapositive suivante (l'argument est un angle). Première phrase réécrite. |
|  | `nc_g1` L'argument : l'angle de u vers OM | VI. L'argument | — | L'argument : l'angle de u⃗ vers OM⃗, vu sur le point qui tourne. |
|  | `nc_g2` Un tour de plus, le même point : [2π] | VI. L'argument | — | Un tour de plus, le même point : [2π]. |
|  | `nc_g3` Arguments des réels et des imaginaires purs | VI. L'argument | — | Arguments des réels et des imaginaires purs. |

**Bloc `nc_s3_b1b` — cos θ = a/r, sin θ = b/r ; le tableau des angles** · fin de bloc : cahier (2 lignes), retrouver « Cahier fermé : écris cos θ et sin θ avec a, b et |z|. », exercice « Quel angle a pour cosinus 1/2 et pour sinus √3/2 ? »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `nc_g4` a = r cos θ, b = r sin θ | VI. L'argument | — | a = r cos θ, b = r sin θ : du cercle de rayon 1 au rayon r. |
|  | `nc_g4_b` Le tableau des angles remarquables | VI. L'argument | ❓ Quel angle θ a pour cosinus √2/2 et pour sinus √2/2 ? · ✏️ r = 2 et a = 1 : combien vaut cos θ ? | Le tableau des angles remarquables ; l'élève reconnaît π/4. |

**Bloc `nc_s3_b2` — La forme trigonométrique ; le quart à gauche en haut** · fin de bloc : cahier (3 lignes, 1 figure(s)), retrouver « Cahier fermé : écris la forme trigonométrique de z. », exercice « Écris 1 + i sous forme trigonométrique. »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `nc_t1` La forme trigonométrique z = r(cos θ + i sin θ) | VII. La forme trigonométrique | — | La forme trigonométrique en trois temps (9 profs : module, r en facteur, angle) sur √3 + i. |
| ✎ | `nc_t2` Au national : a = √2 + i√2 (2023 N) | VII. La forme trigonométrique | ❓ 2023 N : a = √2 + i√2 et |a| = 2. La forme trigonométrique de a est : | RÉÉCRITE : 2023 N (forme trigonométrique, 17 sujets sur 20) — la voix fait la ligne du module, puis l'élève met 2 en facteur et lit l'angle (question, démonstration au barème, réactions préparées). |
|  | `nc_t3` Les signes choisissent le quart : π − θ, π + θ, −θ | VII. La forme trigonométrique | — | Les signes choisissent le quart : π − θ. |

### Séance 6 — Les signes, le retour, le produit


**Bloc `nc_s3_b2b` — Les trois autres quarts ; le module jamais négatif** · fin de bloc : cahier (2 lignes), retrouver « Cahier fermé : a < 0 et b < 0, l'angle du tableau est α : quel argument ? », exercice « Vrai ou faux ? »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `nc_t3_b` Les trois autres quarts : π − θ, π + θ, −θ | VII. La forme trigonométrique | — | Les trois autres quarts. |
|  | `nc_t4` Deux fausses formes trigonométriques | VII. La forme trigonométrique | ❓ −2(cos π/3 + i sin π/3) est-elle une forme trigonométrique ? Corrige-la. · ✏️ Corrige 2(−cos π/6 + i sin π/6). | Deux fausses formes (module négatif, moins devant cos) : l'élève corrige. |

**Bloc `nc_s3_b3` — Le moins devant cos ; retour à a + ib** · fin de bloc : cahier (3 lignes), retrouver « Cahier fermé : comment revient-on de r(cos θ + i sin θ) à a + ib ? », exercice « Écris √2(cos 3π/4 + i sin 3π/4) sous forme algébrique. »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `nc_t4_b` Le moins devant le cosinus seul | VII. La forme trigonométrique | — | Le moins devant cos seul. |
|  | `nc_t5` Retour : de la forme trigonométrique à la forme algébrique | VII. La forme trigonométrique | — | Retour à a + ib (2 sujets). |
|  | `nc_t6` Au national : vérifier |a| et arg a (2024 N) | VII. La forme trigonométrique | — | Vérifier |a| et arg a (2024 N). |

**Bloc `nc_s3_b3b` — Le produit fait tourner ; multiplier par i** · fin de bloc : cahier (2 lignes, 1 figure(s)), retrouver « Cahier fermé : écris l'argument d'un produit. », exercice « i(1 + 2i) = ? »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `nc_r1` Le produit : modules multipliés, arguments additionnés | VIII. Produit, quotient et Moivre | 👀 observation | Le produit : modules multipliés, arguments additionnés — vu sur (1 + i)² (observation des deux arcs) avant la règle. |
|  | `nc_r2` Multiplier par i : un quart de tour | VIII. Produit, quotient et Moivre | ❓ Où arrive le point d'affixe 3 + i quand on multiplie par i ? · ✏️ Où arrive le point d'affixe 2 quand on multiplie par i ? | Multiplier par i : un quart de tour (la rotation de la partie 2 annoncée) ; l'élève place le point. |

### Séance 7 — Quotient, Moivre, géométrie


**Bloc `nc_s4_b1` — Conjugué, inverse, quotient ; déduire un produit** · fin de bloc : cahier (3 lignes), retrouver « Cahier fermé : écris l'argument d'un quotient. », exercice « z = 4(cos π/2 + i sin π/2) et z′ = 2(cos π/6 + i sin π/6). Alors z/z′ = »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `nc_r3` Le conjugué et l'inverse : l'angle change de signe | VIII. Produit, quotient et Moivre | — | Conjugué et inverse : l'angle change de signe (figure). |
|  | `nc_r3_b` Le quotient et l'opposé | VIII. Produit, quotient et Moivre | — | Quotient et opposé. |
|  | `nc_r4` Au national : b = (1 + i)a (2017 N) | VIII. Produit, quotient et Moivre | — | b = (1 + i)a (2017 N) : déduire |b| et arg b. |

**Bloc `nc_s4_b1b` — Identifier deux écritures ; Moivre** · fin de bloc : cahier (2 lignes), retrouver « Cahier fermé : écris la formule de Moivre. », exercice « Vrai ou faux ? »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `nc_r5` Identifier deux écritures : cos 5π/12 | VIII. Produit, quotient et Moivre | — | Identifier deux écritures : cos 5π/12 (2017 N, 1 sujet). |
|  | `nc_r6` Moivre : la puissance multiplie l'angle | VIII. Produit, quotient et Moivre | ❓ D'après la formule de Moivre, (√3 + i)⁶ = ? · ✏️ 1 + i√3 = 2(cos π/3 + i sin π/3). Alors (1 + i√3)⁶ = | Moivre : la puissance multiplie l'angle (spirale), puis la formule ; l'élève calcule (√3 + i)⁶ (6 sujets sur 20). |

**Bloc `nc_s4_b2` — Puissances réelles ; alignement ; égalité de distances** · fin de bloc : cahier (4 lignes, 1 figure(s)), retrouver « Cahier fermé : quand trois points A, B, C sont-ils alignés ? », exercice « (cos π/6 + i sin π/6)⁶ = ? »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `nc_r7` Une puissance réelle (2020 R) | VIII. Produit, quotient et Moivre | — | Une puissance réelle (2020 R) : les puissances qui tombent sur l'axe réel s'allument. |
|  | `nc_r8` Moivre plutôt que développer (2023 R) | VIII. Produit, quotient et Moivre | — | Moivre plutôt que développer (2023 R). |
| ＋❓ | `nc_i1` Trois points alignés : un quotient réel | IX. Géométrie : alignement, distances, angles, nature d'un triangle | ❓ 2021 R : a = 3 + 2i, c = −1 − 2i, d = −3 − 4i. Que vaut (d − a)/(c − a), et que conclure ? · ✏️ A(1), B(2 + i), C(4 + 3i) : que vaut (c − a)/(b − a) ? | Alignement (9 sujets sur 20) : vu en tirant C hors de la droite, puis le national 2021 R posé. AJOUT : l'élève fait le calcul (d − a)/(c − a) = 3/2 et conclut (question avec démonstration au barème) ; l'exercice A(1), B(2 + i), C(4 + 3i) le suit (réactions déjà écrites). Avant, le national était posé sans rien demander. |
|  | `nc_i2` Égalité de distances (2025 N) | IX. Géométrie : alignement, distances, angles, nature d'un triangle | ❓ ω = 5/2, a = 1 + 2i, b = 1 − 2i : sans calculer, pourquoi ΩA = ΩB ? · ✏️ 2025 N : P est le milieu de [AB], avec a = 1 + 2i et b = 1 − 2i. Alors | Égalité de distances (2025 N) : sans calculer, par la symétrie. |

### Séance 8 — Angles et nature d'un triangle ; deux sujets nationaux pas à pas ; le bilan


**Bloc `nc_s4_b2b` — Angle de deux vecteurs, orthogonalité, nature d'un triangle** · fin de bloc : cahier (2 lignes, 1 figure(s)), retrouver « Cahier fermé : écris une mesure de l'angle (AB⃗, AC⃗) avec les affixes a, b, c. », exercice « A(1), B(2 + i), C(i) : que vaut (c − a)/(b − a), et que peut-on dire ? »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `nc_i3` L'angle de deux vecteurs : l'argument du quotient | IX. Géométrie : alignement, distances, angles, nature d'un triangle | — | L'angle de deux vecteurs : l'argument du quotient (NC11). |
| ⟳ | `nc_i4` La nature d'un triangle | IX. Géométrie : alignement, distances, angles, nature d'un triangle | ❓ (c − a)/(b − a) = 2i : quelle est la nature du triangle ABC ? | La nature d'un triangle (NC10–NC11). 2ᵉ passe : voix gardée, nouvelle vue `alignement.html?vue=triangle` (avant : la figure de la distance AB, sans triangle) : l'exemple 1 se dessine et ses trois côtés se marquent « 2 », puis l'exemple 2 (c − a)/(b − a) = i : AB et AC codés égaux, l'angle droit en A, la conclusion, chaque moment au mot qui le dit. Le cas 2i (la question) n'est pas dessiné. |

**Bloc `nc_s4_b3` — Le sujet 2023 N, une question à la fois** (4 diapositives depuis la 2ᵉ passe) · fin de bloc : cahier (3 lignes), retrouver « Cahier fermé : (b − d)/(b − a) est un réel : que peut-on dire de A, B et D ? », exercice « (c − a)/(b − a) = −3 : les points A, B, C sont : »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
| ✎ | `nc_n1` Un sujet entier pas à pas : 2023 N (questions 1 et 2) | X. Deux sujets nationaux, une question à la fois | ❓ 2023 N : b = 1 + √2 + i et d = 2i. Que vaut b − d ? | RÉÉCRITE (2ᵉ passe) : `alignement.html?vue=n2023` — A, B, D placés avec leurs affixes, la question 1 relue sur la figure (OA = 2, angle π/4), puis « 2) b − d = ? » ; la vue s'arrête là (`question2`). |
| ＋ | `nc_n1_b` Un sujet entier pas à pas : 2023 N (question 3, l'alignement) | X. Deux sujets nationaux, une question à la fois | ❓ 2023 N : (√2 + 1)(b − a) = b − d. Que peut-on conclure ? | 2ᵉ passe : `?vue=n2023&depart=question2` — correction de la question 2 sur la figure (retirer 2i, c'est descendre de 2 : B tombe sur C = b̄), puis la question 3 posée ; la vue s'arrête sur `question3` (AVANT : le moment `q3` de `calculs.html?vue=n1` écrivait déjà le quotient réel, la moitié de la réponse). |
| ＋ | `nc_n1_alignes` Un sujet entier pas à pas : 2023 N (question 3 corrigée, la droite) | X. Deux sujets nationaux, une question à la fois | — | NOUVELLE (2ᵉ passe) : la correction de la question 3, seulement après la réponse : le quotient (b − d)/(b − a) = √2 + 1 réel (`quotient`), la droite (AB) qui se trace et passe par D (`droite`), la conclusion (`alignes`). Moments séparés (règle 33). |
| ✎ | `nc_n1_c` Un sujet entier pas à pas : 2023 N (question 4, les arguments) | X. Deux sujets nationaux, une question à la fois | ❓ 2023 N : ac = 2b, c = b̄ et arg a ≡ π/4 [2π]. Alors 2 arg b ≡ | 2ᵉ passe : la correction de la question 3 part dans `nc_n1_alignes` ; ici seulement la question 4, sur `?vue=n2023_arg` : arg a = π/4 lu sur la figure, C reflet de B donc arg c = −arg b, « 4) 2 arg b ≡ ? [2π] » ; la vue s'arrête sur `question4` (AVANT : le moment `q4` écrivait déjà « arg a + arg c ≡ arg 2 + arg b », la 1ʳᵉ ligne de la réponse). Les puces d'écran ne donnent plus que les deux propriétés (argument d'un produit, du conjugué). La réaction « π/2 » (`q_0_2`), confuse (« trois arg b »), est réécrite. |

**Bloc `nc_s4_b4` — 2024 N ; ce qu'il faut retenir ; la carte** · fin de bloc : cahier (3 lignes), retrouver « Cahier fermé : comment écrit-on un quotient sous forme algébrique ? », exercice « Même b : b¹² = ? »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `nc_n2` Un sujet entier : 2024 N (puissance) | X. Deux sujets nationaux, une question à la fois | — | 2024 N : une puissance réelle en deux lignes. |
|  | `nc_b1_bilan` Ce qu'il faut retenir | XI. Bilan et carte du chapitre | — | Ce qu'il faut retenir. |
|  | `nc_b2_carte` La carte du chapitre et la suite | XI. Bilan et carte du chapitre | ❓ Pour multiplier deux complexes, quelle écriture est la plus rapide ? · ✏️ Vrai ou faux ? | La carte du chapitre et la suite (partie 2 : exponentielle, second degré, rotations). |

## 8. Deuxième passe (18 novembre 2026) : le national joué pas à pas, rien de décisif avant la réponse

### Inventaire cas type → diapositive (fréquence au national 2016-2025)
| Cas type | Fréquence | Avant | Après |
|---|---|---|---|
| Forme trigonométrique | 17/20 | `nc_t1` (figure `trig.html?vue=passage`), `nc_t2` (2023 N, question, vue arrêtée sur `module`), `nc_t6` | inchangé (déjà joué, la vue s'arrête avant la forme) |
| Forme algébrique (produit, carré) | 13/20 | `nc_c1`, `nc_c2` (calcul ligne à ligne) | inchangé |
| Quotient | 10/20 | `nc_c4` (question ; la vue calcule un autre exemple) | inchangé |
| Conjugué | 10/20 | `nc_j1` (reflet), `nc_j4` (question, vue arrêtée sur `donnees_c`) | inchangé ; c = b̄ revu en figure dans `nc_n1_b` (B descend sur son reflet) |
| Distance, égalité de distances | 10/20 | `nc_m4` (question, vue arrêtée avant `module`), `nc_i2` (2025 N) | inchangé |
| Alignement | 9/20 | `nc_i1` (figure + 2021 R en question), `nc_n1_b` (texte seul, le moment `q3` écrivait le quotient) | `nc_n1` → `nc_n1_b` → `nc_n1_alignes` en figure (`n2023`) : points, b − d = c, question 3, puis seulement après : quotient, droite (AB) qui passe par D, conclusion |
| Arguments d'un produit / du conjugué | 6/20 | `nc_r4`, `nc_n1_c` (texte, le moment `q4` écrivait la 1ʳᵉ ligne de la réponse) | `nc_n1_c` en figure (`n2023_arg`) : arcs arg a, arg b, arg c = −arg b ; la vue s'arrête sur la question |
| Puissance, Moivre | 6/20 | `nc_r6` (spirale, question), `nc_r7`, `nc_r8`, `nc_n2` | inchangé |
| Nature d'un triangle (angle, quotient) | (NC10–NC11) | `nc_i4` lu sur la figure de la distance AB | `nc_i4` sur `?vue=triangle` (voix gardée) |
| Milieu | 3/20 | `nc_p4` (question, vue arrêtée avant `milieu`) | inchangé |
| Équation avec z̄, ensembles de points | 0/20 et NC12 | `nc_j5` (`calculs.html?vue=a5`, seul le moment `regle`), `nc_m5` (cercle seul) | NON FAIT (voir « reste à faire ») |

### Questions dont la vue montrait la réponse (revue de chaque diapositive à question)
- `nc_n1_b` : `play_until q3` écrivait « (b − d)/(b − a) = √2 + 1 ∈ ℝ » → maintenant arrêt sur `question3` (seulement la relation donnée).
- `nc_n1_c` : `play_until q4` écrivait « arg a + arg c ≡ arg 2 + arg b [2π] » → arrêt sur `question4` (« 2 arg b ≡ ? [2π] ») ; les puces d'écran donnaient aussi les deux premières lignes : remplacées par les propriétés générales.
- Les autres (a2, a6, c4, p4, j4, m4, m6, g4_b, t2, t4, r2, r6, i1, i2, i4) s'arrêtent avant le résultat demandé ou montrent un autre exemple. `nc_g4_b` montre le tableau des angles (la question demande d'y lire π/4 : c'est l'outil, gardé). `nc_i2` : la vue écrit « B reflet de A » et « ω réel », que la voix dit aussi ; la question demande de les relier (gardé).

### Vues ajoutées (fichier `frontend/public/media/simulations/maths/operations-formes-tableau/alignement.html`, vues existantes `alignes` et `national` inchangées)
- `n2023` : moments `donnees`, `q1`, `question2`, `b_moins_d`, `question3`, `quotient`, `droite`, `alignes` ; repères `points`, `donnees`, `oa`, `q1`, `question2`, `vecteur`, `point_c`, `b_moins_d`, `question3`, `quotient`, `droite`, `alignes`.
- `n2023_arg` : moments `donnees`, `angle_a`, `angle_c`, `question4`, `produit`, `egalite`, `conclusion` (même nom de repère, plus `points`).
- `triangle` : moments `distance`, `exemple1`, `cotes`, `equilateral`, `exemple2`, `isocele`, `droit`, `nature` (+ repère `quotient`).
- `?depart=<moment>` (vues n2023 et n2023_arg) : ce qui précède ce moment s'écrit en moins d'une seconde ; c'est ainsi que `nc_n1_b` (`depart=question2`) et `nc_n1_alignes` (`depart=question3`) s'ouvrent là où la diapositive précédente s'est arrêtée, avec une URL distincte et `demarrer: reset` (plus de ligne IFRAME/DEPART pour ces diapositives ni pour `nc_i4`). `calculs.html?vue=n1` reste en place pour le cours en ligne.

### Rejeu après la réponse
- `nc_n1` — `alignement.html?vue=n2023` — `b_moins_d` (la correction de la question 2 ; elle est aussi jouée au début de `nc_n1_b`).
- `nc_n1_b` — `alignement.html?vue=n2023&depart=question2` — `quotient`, `droite`, `alignes` (aussi joués par `nc_n1_alignes`).
- `nc_n1_c` — `alignement.html?vue=n2023_arg` — `produit`, `egalite` (depuis OA, reculer de arg b ramène sur OB), `conclusion`.
- `nc_i4` — `alignement.html?vue=triangle` — rien encore : le cas 2i (AC = 2AB, angle droit) n'est pas dessiné (reste à faire).

**Écrit dans le cours (18 novembre 2026)** : chaque diapositive de cette liste porte `concentration.apres_reponse` (une étape `play_until` par moment, dans l'ordre), débloqué par sa première question (`q`). Le lecteur ne joue ces moments qu'après la réponse, même si un pointage les demandait ; contrôle : `python -I backend/scripts/verifier_parcours.py` (rien d'imprimé). Chaque moment a été vérifié dans Chromium : présent dans la vue de la diapositive, après le dernier moment de son pointage.

### Mots (2ᵉ passe)
Remplacés : « وكتطيح على C » → « وكتوصل لـ C » ; « كتدوز من A » → « كتمشي من A ». Gardés, à écouter : « symétrique » (programme, 2 fois), « colinéaires » (programme, 1 fois), « bleu » (déjà là), « arguments », « modulo » (déjà notés).

### Voix
`math_ch6_nombres_complexes_voix.json` : 52 pistes. Réécrites : `nc_n1`, `nc_n1_b`, `nc_n1_c`, la réaction `nc_n1_c__q_0_2` ; ajoutée : `nc_n1_alignes`. `nc_i4` garde sa voix (seul le pointage change). Les lignes GESTE de ces diapositives viennent de l'absence de piste (durée 0) ; avec une durée estimée (13 caractères/s), le vérificateur ne signale aucun écart.

### Reste à faire
- `calculs-vues.js` n'est pas touché (les vues nouvelles sont dans `alignement.html`, rien à reporter dans les sources du build).
- `nc_i4` : dessiner le cas de la question (2i : AC = 2AB, angle droit, pas isocèle) comme moment de rejeu.
- `nc_j5` (équation avec z̄) et `nc_m5` (médiatrice |z − a| = |z − b|) : pas encore joués pas à pas en figure.
- Une figure de cahier (`cahier_figures`) pour l'alignement 2023 N.

