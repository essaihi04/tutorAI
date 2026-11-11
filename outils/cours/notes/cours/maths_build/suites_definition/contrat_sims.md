# Contrat des simulations — cours « Suites numériques » (math_ch3_suites_numeriques)

Dossier : `frontend\public\media\simulations\maths\suites-tableau\`
URL servie : `/media/simulations/maths/suites-tableau/<page>.html?vue=<vue>`

Le cours (écrit en parallèle) cite EXACTEMENT ces noms de vues, de moments (`K.marque('…')`) et de repères
(`c.repere('…', …)`). Ne les renomme pas ; tu peux AJOUTER des moments/repères, jamais en retirer. Chaque moment a sa
phrase dans `decrire`. `fin` est ajouté par le kit.

## Règles communes (toutes les pages)
- Forme EXACTE de la page modèle `frontend/public/media/simulations/maths/limites-continuite-tableau/traversee.html` :
  mêmes balises, même ordre de scripts (tableau.js → exposants.js → maths-tableau.js), `MathsTableau.page({ id, titre, texte, vues })`,
  un seul bouton `#run`, `#feedback`, `professor-locate.js` à la fin. Lis l'en-tête de `maths/commun/maths-tableau.js` (aide K).
  Ne modifie PAS le kit (commun/), ni rien d'autre que tes pages.
- Cadre 760 × 420 ; rien d'écrit sous y = 360 (la barre du lecteur couvre le bas) ; aucun texte hors cadre (`window.__horsCadre` vide).
- Texte du tableau en français ; apostrophe typographique ’ dans toutes les chaînes JS (jamais ' dans une chaîne '…').
- Indices : écris `u_n`, `u_{n+1}`, `u_0`, `v_{n+1}`, `S_n` (le kit les rend en indice, jamais de « _ » visible).
  Exposants : `q^{n}`, `(2/5)^{n+1}`, `n^{2}` ou les caractères ² ³ (exposants.js). `ℓ` pour la limite.
- Les points d'une suite (n ; uₙ) restent des points ISOLÉS (jamais reliés par une courbe). Couleurs : la suite en cyan,
  bornes / plafond orange, plancher vert, limite jaune, texte blanc. Écriture pas à pas (`K.anime`, `c.pause`).
- Seulement le programme 2BAC PC : n'écris jamais « toile d’araignée », « point fixe », « attractif », « série »,
  « somme infinie », « epsilon », « Cauchy », « borne supérieure », « récurrence forte », « télescopage », « arithmético-géométrique ».
- Chaque vue : `titre`, `dessiner`, `decrire` (une phrase par moment, ce qui se voit, valeurs exactes), `motifs` (facultatif),
  `explication` [{repere, texte}] ; `params` + `poignees` + `lecture` quand un paramètre est indiqué.
- Vérifications (OBLIGATOIRES avant de rendre) :
  `python <maths_build>/check_js.py <page>` ;
  `python <maths_build>/test_page.py --shot <dossier temporaire> /media/simulations/maths/suites-tableau/<page>.html?vue=<vue> …`
  (serveur statique déjà lancé sur 127.0.0.1:8898 ; s'il ne répond pas : `python -m http.server 8898 -d frontend/public --bind 127.0.0.1` en arrière-plan) ;
  lis CHAQUE capture avec Read (fond blanc = transparent) : rien ne se chevauche, tout est lisible, rien dans les 60 px du bas.
  Teste aussi les paramètres aux extrêmes (URL `?vue=…&u0=0.2`, `&u0=4`, `&q=-2`…) : rien ne sort du cadre.
  Supprime ensuite tes captures (disque presque plein).
  `<maths_build>` = `outils\cours\notes\cours\maths_build`

## axe.html — termes sur un axe, cases, machine (id `su_axe`)
- `questions` (o1, ouverture) : titre « Une suite : une liste de nombres ». Moments : `cases` (rangée de cases u₀ u₁ u₂ u₃ … dessinée au centre-haut),
  `q1_recurrence` (« ① une inégalité pour tout n → la récurrence »), `q2_monotonie` (« ② monte ou descend → le sens de variation »),
  `q3_convergence` (« ③ a-t-elle une limite finie → convergente »), `q4_formule` (« ④ la formule de u_n → la suite auxiliaire »),
  `q5_limite` (« ⑤ où va-t-elle → la limite »), `national` (petite note : « au national : un exercice de suites dans chaque sujet »).
  Repères : `cases`, `q1`, `q2`, `q3`, `q4`, `q5`.
- `cases` (a1) : cases numérotées 0 1 2 3 4 (« rang n » sous les numéros). Moments `cases_vides`, `u0` (17 écrit dans la case 0, étiquette u₀ = 17),
  `remplies` (16,25 ; 16,06 ; 16,02 ; 16,004 dans les cases 1 à 4, étiquettes u₁…u₄), `n_et_un` (deux flèches : « n : le numéro de la case », « u_n : le nombre dedans »).
  Repères : `case_2`, `rang`, `valeur`.
- `indices` (a2) : deux cases côte à côte « u_n » et « u_{n+1} ». Moments `case_n`, `fleche_case` (flèche horizontale vers la case suivante, libellé
  « u_{n+1} : le terme suivant »), `fleche_valeur` (flèche vers le haut, libellé « u_n + 1 : la valeur plus 1 »), `exemple` (« u_2 = 5 → u_2 + 1 = 6 ; u_3 = ? on ne sait pas sans la relation »).
  Repères : `suivante`, `plus_un`, `exemple`.
- `machine` (a3) : Moments `explicite` (« u_n = 3n + 2 : on remplace n → u_0 = 2, u_1 = 5 »), `machine` (une boîte « × ¼ puis + 12 », entrée u_n à gauche, sortie u_{n+1} à droite),
  `u1` (17 entre, sort 65/4 = 16,25 = u_1), `u2_u3` (la sortie revient à l’entrée par une flèche en boucle : 16,0625 = u_2 puis u_3).
  Repères : `explicite`, `machine`, `sortie`.
- `arith` (a4) : axe gradué, termes de u_n = 3n + 2 : 2, 5, 8, 11, 14 (points + étiquettes u₀…u₄). Moments `termes`, `pas` (un arc « + 3 » au-dessus de chaque pas), `raison`
  (« u_{n+1} − u_n = 3 : raison r = 3 »). Repères : `pas`, `raison`.
- `geom` (a6) : axe gradué, termes de u_n = 5 × 2^{n} : 5, 10, 20, 40. Moments `termes`, `fois` (arcs « × 2 »), `raison` (« u_{n+1} = 2 u_n : raison q = 2 »). Repères : `fois`, `raison`.
- `serrement` (l1) : axe horizontal gradué de 0 à 30 ; u_{n+1} = ¼u_n + 12 ; PARAMÈTRE `u0` (0..30, pas 0,5, défaut 17) avec une poignée sur l’axe.
  Moments `axe` (axe + trait pointillé vertical en 16 libellé « 16 »), `termes` (u₀, u₁, u₂, u₃, u₄… placés un à un, étiquettes des trois premiers),
  `serrement` (une accolade ou flèches « les termes se serrent vers 16 »), `conclusion` (« (u_n) converge vers 16 : lim u_n = 16 »).
  Avec u0 = 16 : tous les termes valent 16 (le dire dans decrire/lecture). Repères : `seize`, `termes`, `u0`.
- `colonnes` (x1) : deux colonnes de 4 lignes : n | u_n | v_n = u_n − 16 ; u : 17 ; 16,25 ; 16,0625 ; 16,015625 — v : 1 ; 0,25 ; 0,0625 ; 0,015625.
  Moments `colonne_u`, `colonne_v`, `fois_quart` (flèches « × ¼ » entre deux v successifs), `detour` (« v_n géométrique → v_n = (¼)^{n} → u_n = 16 + (¼)^{n} »).
  Repères : `colonne_u`, `colonne_v`, `fois`.
- `image_f` (l7) : deux axes horizontaux l’un sous l’autre. Haut : u_n = 2 + 1/(n + 1) (3 ; 2,5 ; 2,33 ; 2,25 ; …) qui se serrent vers 2. Bas : v_n = √(u_n + 7)
  (≈ 3,16 ; 3,08 ; 3,06 ; 3,04 …) qui se serrent vers 3. Moments `u_tend` (haut, « u_n → 2 »), `f_applique` (flèches verticales de chaque u_n vers son image, « f(x) = √(x + 7) »),
  `f_tend` (bas, « v_n → f(2) = √9 = 3 »), `regle` (« lim u_n = a et f continue en a ⇒ lim f(u_n) = f(a) »). Repères : `a`, `fa`, `regle`.

## dominos.html — le principe de récurrence (id `su_dominos`)
- `principe` (r1) : rangée de 8 dominos numérotés 0…7 (rectangles debout, un peu de relief). Moments `rangee`, `premier_tombe` (le 0 bascule ; « Initialisation : le premier tombe »),
  `passage` (un domino quelconque numéroté n entouré, flèche vers n + 1 ; « Hérédité : si le domino n tombe, le n + 1 tombe »),
  `tous` (les dominos tombent l’un après l’autre jusqu’au 7, « … » après ; « Conclusion : tous tombent »). Repères : `premier`, `passage`, `tous`.
- `trou` (r1, variante) : même rangée mais un grand écart entre 5 et 6. Moments `rangee`, `premier_tombe`, `chute` (0 à 5 tombent), `arret` (6 et 7 restent debout ;
  « le passage de 5 à 6 manque : la chaîne s’arrête »). Repères : `trou`, `debout`.

## arbres.html — nombre de termes (id `su_arbres`)
- `arbres` (a8) : trois arbres à la craie numérotés 5, 6, 7 le long d’une route. Moments `arbres`, `compte` (« 7 − 5 + 1 = 3 arbres »),
  `regle` (« de u_p à u_n : n − p + 1 termes », encadré), `exemple` (« de u_0 à u_{2021} : 2021 − 0 + 1 = 2022 termes »). Repères : `arbres`, `regle`, `exemple`.
- `colonne` (p2) : colonne « u_0 = 1 + v_0 », « u_1 = 1 + v_1 », « u_2 = 1 + v_2 », « ⋮ », « u_{2021} = 1 + v_{2021} » ; les 1 en vert, les v en jaune.
  Moments `colonne`, `les_un` (les 1 entourés en vert : « 2022 fois 1 = 2022 »), `les_v` (accolade jaune : « v_0 + … + v_{2021} : somme géométrique »),
  `somme` (« S = 2022 + (v_0 + v_1 + … + v_{2021}) »). Repères : `les_un`, `les_v`, `somme`.

## nuage.html — nuage de points (n ; uₙ) (id `su_nuage`)
Repère : n en abscisse (0 à 10), u_n en ordonnée ; points isolés.
- `plancher` (b1) : u_n = 16 + (¼)^{n} (17 ; 16,25 ; 16,06 …). Échelle verticale lisible (de 15,5 à 17,5 par ex.). Moments `repere`, `points`,
  `plancher` (droite y = 16 verte pointillée, « plancher : u_n ≥ 16, minorée par 16 »), `plafond` (droite y = 17 orange, « plafond : u_n ≤ 17, majorée par 17 »),
  `bornee` (« minorée et majorée : bornée »). Repères : `plancher`, `plafond`, `points`.
- `bornee` (b2) : u_n = 5n²/(n² + 2) (0 ; 1,67 ; 3,33 ; 4,09 ; 4,44 …). Moments `repere`, `points`, `plafond` (y = 5 orange : « jamais atteint : u_n < 5 »),
  `plancher` (y = 0 vert : « u_n ≥ 0 »), `bornee` (« 0 ≤ u_n < 5 : (u_n) est bornée »). Repères : `plafond`, `plancher`.
- `monotonie` (m1) : Moments `repere`, `deux_points` (u_0 = 2 et u_1 = 3 seulement), `fleche` (flèche qui monte de u_0 à u_1 avec « ? »),
  `suite` (les points suivants : 2 ; 3 ; 2,5 ; 2 ; 1,5 ; 1 ; 0,5 … qui redescendent), `contre_exemple` (« u_1 > u_0, et pourtant la suite n’est pas croissante » ;
  « croissante : u_{n+1} ≥ u_n POUR TOUT n »). Repères : `deux_points`, `suite`, `regle`.
- `reference` (l2) : trois séries de points sur le même repère (couleurs différentes, légende) : n² (sort vite par le haut, flèche « +∞ »), √n (monte lentement, « +∞ »),
  1/n pour n ≥ 1 (tombe vers 0, « 0 »). Moments `repere`, `carre`, `racine`, `inverse`, `regle` (« lim n^{α} = +∞ si α > 0 ; lim n^{α} = 0 si α < 0 »).
  Repères : `carre`, `racine`, `inverse`, `regle`.
- `fraction` (l6) : u_n = (n + 1)/(n + 3) (0,33 ; 0,5 ; 0,6 ; 0,67 …). Moments `repere`, `points`, `asymptote` (y = 1 jaune pointillée), `limite`
  (« lim (n + 1)/(n + 3) = 1 »). Repères : `un`, `points`.

## qn.html — les points (n ; qⁿ) (id `su_qn`)
Repère n de 0 à 10 ; ordonnée adaptée (−4 à 4 par ex., les points qui sortent marqués par une flèche au bord).
- `positif` (l3) : Moments `repere`, `q_demi` (q = 1/2 : 1 ; 0,5 ; 0,25 … vers 0, cyan, « q = 1/2 → 0 »), `q_deux` (q = 2 : 1 ; 2 ; 4 ; puis hors du cadre, orange, « q = 2 → +∞ »),
  `q_un` (q = 1 : tous à 1, vert, « q = 1 → 1 »), `bilan` (trois lignes : « 0 < q < 1 : lim q^{n} = 0 », « q > 1 : lim q^{n} = +∞ », « q = 1 : lim q^{n} = 1 »).
  Repères : `q_demi`, `q_deux`, `q_un`.
- `negatif` (l4) : Moments `repere`, `q_moins_demi` (q = −1/2 : sauts de part et d’autre de l’axe qui se rapprochent de 0), `q_moins_un` (q = −1 : 1, −1, 1, −1 …),
  `q_moins_deux` (q = −2 : sauts de plus en plus grands, sortent du cadre), `tableau_quatre_cas` (un tableau à la craie, 4 colonnes :
  « q ≤ −1 : pas de limite » | « −1 < q < 1 : 0 » | « q = 1 : 1 » | « q > 1 : +∞ »). Repères : `q_moins_demi`, `q_moins_un`, `q_moins_deux`, `tableau`.
- `libre` (variante) : PARAMÈTRE `q` (−2..2, pas 0,1, défaut 0,5) ; une règle de q (segment horizontal en haut à droite ou à gauche) avec la zone −1 < q < 1 colorée
  et la poignée q dessus. Moments `regle_q`, `points`, `verdict` (le cas lu : « −1 < q < 1 : lim q^{n} = 0 » / « q > 1 : +∞ » / « q = 1 : 1 » / « q ≤ −1 : pas de limite »).
  `lecture` donne le cas. Repères : `regle_q`, `points`, `verdict`.

## plafond.html — monter avec un plafond (id `su_plafond`)
- `monte` (c1) : u_n = 4 − 3 × 0,6^{n} (1 ; 2,2 ; 2,92 …) sous un plafond y = 5. Moments `repere`, `monte` (points qui montent, cyan), `plafond` (y = 5 orange,
  « plafond : majorée par 5 »), `tasse` (pointillés jaunes en y = 4 : « elle se tasse sous ℓ : elle converge »), `sans_plafond` (une autre série grise, n², qui sort
  par le haut : « sans plafond, elle peut partir vers +∞ »). Repères : `plafond`, `tasse`, `sans_plafond`.
- `couple` (c2) : deux petits repères côte à côte. Moments `croissante_majoree` (gauche : points qui montent sous un plafond, « ↗ + plafond »), `miroir_decroissante`
  (droite : points qui descendent au-dessus d’un plancher, « ↘ + plancher »), `mauvais_couple` (en bas : « croissante et minorée : on ne peut rien conclure, ex. n² »),
  `regle` (« croissante et majorée ⇒ convergente ; décroissante et minorée ⇒ convergente »). Repères : `gauche`, `droite`, `mauvais`, `regle`.
- `sous_plafond` (c3) : même suite que `monte` (limite 4) ; PARAMÈTRE `M` (4..8, pas 0,5, défaut 6) = hauteur du plafond, poignée sur la droite du plafond.
  Moments `repere`, `points`, `plafond` (y = M), `limite_sous_plafond` (y = 4 jaune : « majorée par M, mais ℓ = 4 : le plafond n’est pas forcément la limite »).
  Si M = 4, le dire. Repères : `plafond`, `limite`.

## gendarmes.html — comparaison (id `su_gendarmes`)
- `membre` (c6, image) : lignes empilées écrites l’une après l’autre : « u_1 ≤ (2/5) u_0 », « u_2 ≤ (2/5) u_1 ≤ (2/5)² u_0 », « u_3 ≤ (2/5) u_2 ≤ (2/5)³ u_0 », « ⋮ », « u_n ≤ (2/5)^{n} u_0 = (3/2)(2/5)^{n} ».
  Moments `ligne1`, `ligne2`, `recolle` (flèche courbe qui montre que u_1 de la ligne 1 se recolle dans la ligne 2, « on recolle »), `ligne3`, `ligne_n` (dernière ligne encadrée jaune,
  avec la note « la preuve propre : une récurrence »). Repères : `recolle`, `ligne_n`.
- `encadre` (c4, c7) : trois rangées de points : bas 0 (vert), haut w_n = (3/2) k^{n} (orange), la suite entre les deux (cyan) — par défaut celle du national 2020 :
  u_0 = 3/2, u_{n+1} = 2u_n/(2u_n + 5). PARAMÈTRE `k` (0,2..0,9, pas 0,05, défaut 0,4) : la borne du haut est (3/2)k^{n} ; pour k ≠ 0,4 la suite du milieu est
  une suite quelconque toujours entre 0 et la borne (ex. (3/2)k^{n}/(1 + 0,3n)). Moments `repere`, `bas`, `haut`, `entre`, `resserre` (flèches qui se resserrent
  vers 0 : « les deux bornes → 0, donc u_n → 0 »). Repères : `bas`, `haut`, `entre`, `resserre`.
- `bande` (c8) : ℓ = 2 ; u_n = 2 − (1/2)(2/7)^{n} × 0,8 (sous 2) ; la bande [2 − (1/2)(2/7)^{n} ; 2] dessinée pour chaque n (petits segments orange) qui se resserre.
  Moments `repere`, `limite_l` (y = 2 jaune), `points`, `bande_l`, `conclusion` (« 0 < 2 − u_n ≤ (1/2)(2/7)^{n} → 0, donc lim u_n = 2 »). Repères : `ligne_l`, `bande`.

## escalier.html — représentation des termes avec la courbe et y = x (id `su_escalier`)
f(x) = 2x/(x + 1) ; repère 0..4 en x, 0..2,5 en y (au choix, lisible). Les traits de l’escalier : vertical jusqu’à la courbe, horizontal jusqu’à y = x,
vertical jusqu’à l’axe (pointillés de lecture en craie), les termes u₀, u₁, u₂ marqués sur l’axe des abscisses. JAMAIS le mot « toile d’araignée ».
- `escalier` (f1, f2) : PARAMÈTRE `u0` (0,2..4, pas 0,1, défaut 2), poignée sur l’axe des abscisses. Moments `courbe_et_droite` (courbe de f cyan + droite y = x blanche, libellées),
  `placer_u0`, `monter_courbe` (trait vertical de u₀ à la courbe, point (u₀ ; f(u₀))), `aller_droite` (horizontal jusqu’à y = x), `descendre_u1` (vertical jusqu’à l’axe : u₁ = f(u₀)),
  `repeter` (u₂, u₃, u₄ … l’escalier continue et se tasse), `conjecture` (« les termes descendent vers 1 » ou « montent vers 1 » selon u0 ; point (1 ; 1) entouré).
  Repères : `courbe`, `droite`, `u0`, `u1`, `intersection`.
- `boite` (f3) : Moments `courbe` (courbe de f sur [0 ; 4]), `boite_x` ([1 ; 2] en couleur sur l’axe des abscisses), `images` (projections : f(1) = 1, f(2) = 4/3),
  `boite_y` ([1 ; 4/3] sur l’axe des ordonnées : « ⊂ [1 ; 2] », « f croissante garde l’ordre »). Repères : `boite_x`, `boite_y`.
- `zone` (f4) : Moments `courbe_et_droite`, `zone_sous_droite` (la bande entre la droite et la courbe au-dessus de [1 ; 2] hachurée/colorée : « f(x) ≤ x »),
  `escalier` (escalier depuis u₀ = 2 qui descend), `conclusion` (« f(x) − x ≤ 0 sur [1 ; 2] et u_n ∈ [1 ; 2] ⇒ u_{n+1} ≤ u_n »). Repères : `zone`, `escalier`.
- `point` (f5, f6) : Moments `courbe_et_droite`, `escalier` (depuis 2), `point_intersection` (les deux points où la courbe coupe y = x : (0 ; 0) et (1 ; 1), entourés),
  `intervalle` (I = [1 ; 2] marqué sur l’axe), `choix` (0 barré : « 0 ∉ [1 ; 2] » ; « ℓ = 1 »). Repères : `point_zero`, `point_un`, `intervalle`.
- `national` (f7) : g(x) = (4x + 3)/(x + 2), u₀ = 1, I = [1 ; 3] ; repère 0..4. Moments `courbe_et_droite`, `escalier` (monte de 1 vers 3), `point_intersection`
  (point (3 ; 3) entouré), `conjecture` (« croissante, vers 3 »). Repères : `point_trois`, `escalier`.
