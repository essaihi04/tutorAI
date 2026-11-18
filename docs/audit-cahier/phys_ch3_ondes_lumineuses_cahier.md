# Le cahier de l'élève — Propagation d'une onde lumineuse (`phys_ch3_ondes_lumineuses`)

18 novembre 2026, skill `cahier-de-l-eleve` (étapes 1 à 5). Sources lues : les deux cours (en ligne et
`en_attente/`), l'architecture `backend/data/curriculum/architecture/phys_ch3_ondes_lumineuses.md`, l'exploration
`backend/data/curriculum/exploration/ondes_lumineuses.json` (`cas_types`, `pieges`, `erreurs_examen`) et l'audit des
dessins `docs/audit-cahier/physique-ch1-5.md`. Seuls `blocs[].cahier`, `blocs[].cahier_figures`,
`concentration.cahier` et `concentration.cahier_figures` ont été écrits.

## Comment le plan s'affiche

L'écran du cahier (`TableauCahier`, `CycleBloc.tsx`) écrit déjà le titre de la partie (I. … X., les
`activities[].title`) quand un bloc y entre. Le cahier numérote donc à l'intérieur de chaque partie (1., 2., …),
de façon continue d'un bloc à l'autre ; « Définition : », « Méthode : », « Attention : », « Remarque : »,
« Exemple : » marquent les compléments. Quand un bloc a autant de lignes que de diapositives, l'écran met chaque
ligne sous le titre de sa diapositive : on l'évite partout (une ligne de plus ou de moins), sauf dans les quatre blocs
du cours en ligne où une partie commence au milieu du bloc (voir plus bas) — là, ce rangement par diapositive met le
titre de la nouvelle partie à sa place.

## Le cahier idéal du chapitre (version en attente, l'ordre de référence)

Chaque ligne « - » est une ligne du cahier ; le commentaire donne le bloc qui la porte.

### I. La diffraction de la lumière

<!-- bloc ol_s1_b1 — La lumière ne va pas toujours tout droit -->
- 1. Sans obstacle, le laser donne un point net : la lumière se propage en ligne droite.
- 2. Définition : quand la lumière traverse une fente très fine, elle s'étale : c'est la diffraction.
- Condition : l'ouverture doit être très petite (≈ 0,1 mm ou moins).
- 3. La figure : une tache centrale très lumineuse, deux fois plus large que les taches secondaires.
- Elle s'étale perpendiculairement à la fente (fente verticale → figure horizontale).
- 🖍 *Dessin* : **Figure de diffraction (écran vu de face)** — Fente verticale : la figure s'étale à l'horizontale ; la tache centrale est deux fois plus large que les secondaires.
<!-- bloc ol_s1_b2 — L'aspect ondulatoire, le montage, le fil -->
- 4. Seules les ondes se diffractent (comme l'onde à la surface de l'eau).
- Donc : la diffraction de la lumière met en évidence l'aspect ondulatoire de la lumière.
- Attention : on écrit « aspect ondulatoire », pas « lumière monochromatique ».
- 5. Montage : a = largeur de la fente ; D = distance fente – écran ; L = largeur de la tache centrale.
- L : d'une extinction à l'autre. Exemple : a = 0,10 mm ; D = 2,0 m ; L = 2,6 cm.
- 6. Un fil fin de diamètre d donne la même figure qu'une fente de largeur a = d.
- 🖍 *Dessin* : **Le montage de diffraction** — Laser → fente de largeur a → écran à la distance D ; L : largeur de la tache centrale, d'une extinction à l'autre (l'étalement est exagéré).

### II. L'écart angulaire : θ = λ/a

<!-- bloc ol_s1_b3r — L'angle en radian, puis l'écart angulaire θ -->
- 1. Rappel : angle en radian : θ = s/R (arc sur rayon) ; 180° = π rad ; 1 rad ≈ 57°.
- 2. Définition : l'écart angulaire θ est l'angle entre la direction du centre de la tache centrale et la direction de la première extinction.
- Attention : θ va du centre de la tache à son bord, pas d'un bord à l'autre.
- 3. Quand la largeur a de la fente diminue, θ augmente : la diffraction est plus marquée.
- 🖍 *Dessin* : **L'angle en radian** — θ = s/R : l'arc s divisé par le rayon R ; si s = R, θ = 1 rad.
- 🖍 *Dessin* : **L'écart angulaire θ** — θ va du centre de la tache centrale à son bord (la première extinction) ; l'angle est exagéré sur le dessin.
<!-- bloc ol_s1_b3 — Tout en mètre, la couleur, puis θ = λ/a -->
- 4. Tout en mètre : 1 cm = 10⁻² m ; 1 mm = 10⁻³ m ; 1 µm = 10⁻⁶ m ; 1 nm = 10⁻⁹ m.
- 5. Même fente : plus la longueur d'onde λ est grande, plus θ est grand (rouge plus étalé que bleu).
- 6. Relation (admise) : θ = λ/a ; θ en rad, λ et a en m ; θ petit.
- Remarque : diffraction nette si a est de l'ordre de λ (au plus quelques centaines de λ).
- Exemple : λ = 650 nm ; a = 0,10 mm : θ = 6,5·10⁻⁷ / 1,0·10⁻⁴ = 6,5·10⁻³ rad.

### III. La largeur de la tache : L = 2λD/a

<!-- bloc ol_s2_bt — La tangente, puis le triangle du montage -->
- 1. Rappel : dans un triangle rectangle, tan θ = côté opposé / côté adjacent.
- Adjacent : le côté de l'angle droit collé à θ ; opposé : le côté en face de θ.
- 2. Triangle du montage (fente, centre et bord de la tache) : adjacent D ; opposé L/2.
- D'après la figure : tan θ = (L/2)/D = L/(2D).
- Attention : le côté opposé est L/2, pas L.
- 🖍 *Dessin* : **La tangente** — tan θ = opposé / adjacent : le côté en face de θ sur le côté collé à θ.
- 🖍 *Dessin* : **Le triangle rectangle du montage** — D est le côté adjacent à θ, L/2 le côté opposé ; l'angle droit est au centre de la tache (angle exagéré).
<!-- bloc ol_s2_b1 — Le petit angle, l'égalité, isoler -->
- 3. Petit angle : θ petit et en radian, tan θ ≈ θ, donc θ = L/(2D).
- 4. Même angle écrit deux fois : θ = λ/a et θ = L/(2D), donc λ/a = L/(2D).
- 5. On isole (produit en croix : λ·2D = a·L) :
- L = 2λD/a ; λ = aL/(2D) ; a = 2λD/L ; D = aL/(2λ).
- Remarque : calculatrice en mode radian.
<!-- bloc ol_s2_b2 — Calculer λ, contrôler, établir L -->
- 6. Méthode (calcul) : relation → longueurs en mètre → application numérique → résultat et unité.
- Exemple : λ = aL/(2D) = (1,0·10⁻⁴ × 2,6·10⁻²)/(2 × 2,0) = 6,5·10⁻⁷ m = 650 nm.
- Contrôle : lumière visible : 400 nm ≤ λ ≤ 800 nm ; sinon, chercher l'erreur de conversion.
- 7. Méthode « établir L » : 1) d'après la figure, tan θ = L/(2D) ; 2) θ petit : tan θ ≈ θ ;
- 3) or θ = λ/a ; 4) donc λ/a = L/(2D) et L = 2λD/a.
- Attention : la relation finale écrite seule ne rapporte rien : écrire les quatre lignes.

### IV. Comparer deux expériences

<!-- bloc ol_s2_b3 — Qui change ? En haut, puis en bas de la formule -->
- 1. λ dépend de la source, a de la fente, D de la position de l'écran.
- Changer la fente ou l'écran ne change pas λ.
- 2. L = 2λD/a : λ et D en haut : L proportionnelle à λ et à D (D double → L double).
- 3. a en bas : L varie en sens inverse de a (a divisée par 2 → L double).
- Méthode « comment varie L » : écrire L = 2λD/a, dire ce qui reste fixe, conclure par une inégalité.
<!-- bloc ol_s3_b1 — Deux expériences : le rapport, puis le cheveu -->
- 4. Deux expériences, même a et même D : λ₁/a = L₁/(2D) et λ₂/a = L₂/(2D).
- On divise : λ₂/λ₁ = L₂/L₁, donc λ₂ = λ₁·L₂/L₁ (pas de conversion si L₁ et L₂ ont la même unité).
- 5. Fil de diamètre d : d remplace a (pas D) : θ = λ/d = L/(2D), donc d = 2λD/L.
- Exemple : un cheveu mesure de 50 à 100 µm. Attention : certains énoncés notent d = L/2.

### V. Exploiter une courbe

<!-- bloc ol_s3_b2 — Une fente, un point ; pourquoi 1/a ; la pente et ses unités -->
- 1. Mesures : λ = 650 nm et D = 2,0 m fixes ; pour chaque fente, on mesure L et on calcule 1/a.
- 2. L = f(a) n'est pas une droite ; L = f(1/a) est une droite passant par l'origine : L = k·(1/a).
- 3. Coefficient directeur : k = ΔL/Δ(1/a), avec l'origine et un point bien lisible.
- Exemple : point (10 mm⁻¹ ; 26 mm) : k = 26/10 = 2,6 mm² = 2,6·10⁻⁶ m².
- Attention : lire l'unité de chaque axe et la convertir (1 mm⁻¹ = 10³ m⁻¹ ; 1 mm² = 10⁻⁶ m²).
- 🖍 *Dessin* : **L en fonction de 1/a** — Une droite passant par l'origine : L = k·(1/a) ; k = (26 mm)/(10 mm⁻¹) = 2,6 mm² = 2,6·10⁻⁶ m².
<!-- bloc ol_s3_b2b — Identifier k, vérifier θ = λ/a, les autres courbes -->
- 4. Identification : courbe L = k·(1/a) ; cours L = 2λD·(1/a) ; donc k = 2λD et λ = k/(2D).
- Exemple : λ = 2,6·10⁻⁶/(2 × 2,0) = 6,5·10⁻⁷ m = 650 nm (dans le visible).
- 5. Vérifier θ = λ/a : θ = L/(2D) pour chaque fente ; θ = f(1/a) est une droite de pente k = λ.
- 6. L = f(D) : L = (2λ/a)·D, donc k = 2λ/a et λ = a·k/2.
- Méthode (courbe) : droite par l'origine → k avec unités → relation du cours sous la même forme → identifier.
- 🖍 *Dessin* : **θ en fonction de 1/a** — Droite par l'origine : θ = k·(1/a) avec k = λ = 6,5·10⁻⁷ m.
- 🖍 *Dessin* : **L en fonction de D (2021 N)** — Droite par l'origine : L = k·D ; k = 4 cm / 200 cm = 2·10⁻² (sans unité), et k = 2λ/a.

### VI. Radiation, fréquence et spectre

<!-- bloc ol_s3_b3r — Une radiation, le vide, la célérité c -->
- 1. Définition : une lumière monochromatique est constituée d'une seule radiation, caractérisée par sa fréquence ν.
- Une lumière polychromatique est constituée de plusieurs radiations monochromatiques (ex. : lumière blanche).
- 2. La lumière est une onde électromagnétique : elle se propage dans le vide et les milieux transparents.
- 3. Célérité dans le vide (et dans l'air) : c = 3,00·10⁸ m/s (300 000 km par seconde).
<!-- bloc ol_s3_b3 — λ₀ = c/ν et le spectre visible -->
- 4. Pendant une période T, la lumière parcourt λ₀ dans le vide : λ₀ = c·T = c/ν (ν = 1/T).
- λ₀ en m ; c en m/s ; ν en Hz. Exemple : λ₀ = 589 nm → ν = 3,00·10⁸/5,89·10⁻⁷ ≈ 5,09·10¹⁴ Hz.
- 5. Spectre visible : 400 nm (violet) ≤ λ₀ ≤ 800 nm (rouge), soit 7,50·10¹⁴ Hz ≥ ν ≥ 3,75·10¹⁴ Hz.
- λ₀ < 400 nm : ultraviolet ; λ₀ > 800 nm : infrarouge (invisibles). Attention : nm, pas µm.
- 🖍 *Dessin* : **Le spectre visible** — Visible : de 400 nm (violet, 7,5·10¹⁴ Hz) à 800 nm (rouge, 3,75·10¹⁴ Hz) ; en dessous l'ultraviolet, au-dessus l'infrarouge.

### VII. La lumière dans un milieu d'indice n

<!-- bloc ol_s4_b1 — Dans le verre : la lumière ralentit, même fréquence, l’onde se resserre -->
- 1. Dans un milieu transparent, la célérité v de la lumière est plus petite que c (verre : 2,0·10⁸ m/s).
- 2. La fréquence ν d'une radiation ne dépend pas du milieu : c'est la source qui l'impose (même couleur).
- 3. Même ν, v plus petite : la longueur d'onde λ dans le milieu est plus petite que λ₀ (rappel : λ = v/ν).
- Exemple : λ₀ = 600 nm dans l'air, λ = 400 nm dans le verre.
- 🖍 *Dessin* : **L'onde lumineuse entre dans le verre** — Même fréquence, célérité plus petite : dans le verre, la longueur d'onde diminue (λ = 400 nm < λ₀ = 600 nm).
<!-- bloc ol_s4_b2 — La tache se resserre dans l'eau ; l'indice n = c/v ; λ = λ₀/n ; n = L/L' -->
- 4. Dans un liquide, la tache se resserre (L' < L), car λ y est plus petite et L = 2λD/a.
- 5. Définition : l'indice de réfraction d'un milieu est n = c/v (sans unité) ; v < c, donc n ≥ 1.
- Valeurs : air n ≈ 1,00 ; eau n = 1,33 ; verre n ≈ 1,5.
- 6. ν ne change pas : ν = c/λ₀ = v/λ, donc λ = λ₀·v/c = λ₀/n et v = c/n (n = λ₀/λ).
- 7. Air puis liquide (même a, même D) : L/L' = (2λ₀D/a)/(2λD/a) = λ₀/λ = n. Exemple : 2,4/1,8 ≈ 1,33.
- Attention : dans le milieu, ν ne change pas ; v < c et λ < λ₀.

### VIII. La dispersion de la lumière blanche

<!-- bloc ol_s4_b3 — La lumière blanche dans un prisme : le violet le plus dévié, deux célérités -->
- 1. La lumière blanche est polychromatique : le prisme la décompose en un spectre continu.
- Cette séparation des radiations est la dispersion (arc-en-ciel : les gouttes d'eau).
- 2. Le violet est le plus dévié, le rouge le moins : n dépend de la fréquence, n(rouge) < n(violet).
- 3. Dans le verre, v = λ·ν : deux radiations ont deux célérités différentes (2021 N : 1,85 et 1,81·10⁸ m/s).
- 🖍 *Dessin* : **Le prisme disperse la lumière blanche** — Le prisme décompose la lumière blanche en un spectre : le rouge est le moins dévié, le violet le plus dévié.
<!-- bloc ol_s4_b4 — Milieu dispersif, et la fente en lumière blanche -->
- 4. Définition : un milieu est dispersif si la célérité de la lumière dépend de sa fréquence.
- Phrase type : n dépend de la fréquence ; or v = c/n (c constante), donc v dépend de ν : le verre est dispersif.
- Remarque : le vide n'est pas dispersif ; l'air l'est très peu.
- 5. Fente en lumière blanche : tache centrale blanche (couleurs superposées), bords colorés.
- 🖍 *Dessin* : **Une fente en lumière blanche (écran vu de face)** — Au centre, toutes les couleurs se superposent : la tache est blanche ; sur les bords, les couleurs se séparent (rouge à l'extérieur).

### IX. Le national joué pas à pas

<!-- bloc ol_s5_b1 — Reconnaître le cas ; 2023 R : trouver a -->
- 1. Le mot de la question : « nommer » → diffraction ; « établir » → 4 lignes ; « fil » → d remplace a.
- « mêmes conditions » → diviser ; « courbe » → k ; « milieu » → v = c/n, λ = λ₀/n ; « fréquence » → ν = c/λ₀.
- 2. 2023 R, Q2 : a = 2λ₀D/L = (2 × 5,8·10⁻⁷ × 1,4)/(2,7·10⁻²) ≈ 6,0·10⁻⁵ m = 60 µm.
<!-- bloc ol_s5_b1b — 2023 R : la source rouge, puis le milieu -->
- 3. 2023 R, Q3 (même a, même D) : λ₀R/λ₀ = L_R/L, donc λ₀R = λ₀·L_R/L = 580 × 3,4/2,7 ≈ 730 nm.
- Q4 (n = 1,5) : v = c/n = 3·10⁸/1,5 = 2·10⁸ m/s.
- ν ne change pas, donc λ = λ₀/n = 580/1,5 ≈ 387 nm.
<!-- bloc ol_s5_b1c — 2021 N : le prisme, la fréquence -->
- 4. 2021 N : le prisme décompose la lumière blanche : elle est polychromatique.
- Q2.1 : ν_j = c/λ₀j = 3·10⁸/(589·10⁻⁹) ≈ 5,09·10¹⁴ Hz.
- Attention : λ₀ en mètre ; ν de l'ordre de 10¹⁴ Hz.
<!-- bloc ol_s5_b1d — 2021 N : deux célérités dans le verre -->
- 5. 2021 N, Q2.2 : dans le prisme, v = λ·ν (λ mesurée dans le prisme, ν de la radiation).
- v_j = 355·10⁻⁹ × 5,09·10¹⁴ ≈ 1,81·10⁸ m/s ; v_r = 474·10⁻⁹ × 3,91·10¹⁴ ≈ 1,85·10⁸ m/s.
- Q2.3 : v_j ≠ v_r : la célérité dépend de la fréquence, le verre du prisme est dispersif.
<!-- bloc ol_s5_b1e — 2021 N : la courbe L = f(D), la pente -->
- 6. 2021 N, courbe L = f(D) : droite passant par l'origine, L = k·D.
- Méthode : lire l'unité de chaque axe ; prendre l'origine et un point bien lisible.
- k = ΔL/ΔD = (4 cm)/(200 cm) = 2·10⁻² (sans unité : ΔL et ΔD dans la même unité).
- 🖍 *Dessin* : **L en fonction de D (2021 N)** — Droite par l'origine : L = k·D ; k = 4 cm / 200 cm = 2·10⁻² (sans unité), et k = 2λ/a.
<!-- bloc ol_s5_b1f — 2021 N : identifier λ, puis le cheveu -->
- 7. 2021 N, Q3.2 : L = (2λ/a)·D et L = k·D, donc k = 2λ/a et λ = a·k/2.
- λ = (6·10⁻⁵ × 2·10⁻²)/2 = 6·10⁻⁷ m = 600 nm.
- Q3.3 (cheveu) : d = 2λD₁/L₁ = (2 × 6·10⁻⁷ × 2)/(3·10⁻²) = 8·10⁻⁵ m = 80 µm.
<!-- bloc ol_s5_b1g — 2025 R : dans l'air, puis dans le liquide -->
- 8. 2025 R : des taches derrière une fente fine : c'est la diffraction.
- Elle met en évidence l'aspect ondulatoire de la lumière.
- Montrer L = 2λD/a : les quatre lignes de la méthode III.7.
<!-- bloc ol_s5_b1h — 2025 R : l'indice du liquide -->
- 9. 2025 R, Q3.1 : L = 2λ₀D/a (air) et L' = 2λD/a (liquide), donc L/L' = λ₀/λ = n.
- n = 2,4/1,8 ≈ 1,33.
- Q3.2 : v = c/n = 3·10⁸/1,33 ≈ 2,26·10⁸ m/s.

### X. Bilan du chapitre

<!-- bloc ol_s5_b2 — Le bilan du chapitre -->
- 1. Deux égalités à savoir : λ/a = L/(2D) (θ petit, en rad) et n = c/v = λ₀/λ.
- 2. Une radiation est caractérisée par sa fréquence ν, qui ne change pas d'un milieu à l'autre ; λ₀ = c/ν.
- 3. La diffraction prouve l'aspect ondulatoire ; le verre est dispersif (v dépend de ν).

## Choix et compléments

- **Définitions mot pour mot** (celles du cours) : diffraction, écart angulaire θ, lumière monochromatique /
  polychromatique, indice de réfraction, milieu dispersif.
- **Chaque loi avec ses conditions et unités** : θ = λ/a (admise ; θ en rad, λ et a en m, θ petit) ;
  tan θ ≈ θ (θ petit, en radian, calculatrice en mode radian) ; λ₀ = c·T = c/ν (λ₀ en m, c en m/s, ν en Hz) ;
  n = c/v (sans unité, n ≥ 1) ; λ = λ₀/n (ν inchangée) ; k sans unité pour L = f(D).
- **Une méthode numérotée par cas type du national** (`cas_types`) : calcul direct (III.6), établir L (III.7),
  comment varie L (IV.3), rapport de deux expériences (IV.4), fil ou cheveu (IV.5), exploiter une courbe (V.3 à V.6),
  fréquence (VI.4), milieu (VII.6), indice par diffraction (VII.7), dispersion (VIII.4 : la phrase type), mot-code de
  la question (IX.1).
- **Pièges** (`erreurs_examen`, `pieges`) écrits en « Attention » : aspect ondulatoire et non monochromatique ;
  θ du centre au bord ; côté opposé L/2 ; la relation finale seule ne rapporte rien ; unités des axes ; d remplace a
  (pas D) et « d = L/2 » dans certains énoncés ; nm et non µm ; λ₀ en mètre dans ν = c/λ₀ ; v < c, λ < λ₀.
- **Rien avant d'être écrit** : « tout en mètre » est écrit avant le premier calcul (II.4) ; le visible
  (400–800 nm) est écrit comme contrôle en III.6 avant sa partie (VI.5), comme dans la diapositive `ol_l8` ;
  λ = v/ν est un rappel du chapitre 2 ; dans le cours en ligne, la cuve (`ol_c5_cuve`, partie IV) ne donne plus
  n = L/L' avant l'indice (sa bulle disait « n = L/L' » : corrigé en « s'expliquera avec l'indice, partie VII »).
- **Dessins** : les 11 dessins de l'audit du 14 novembre sont gardés ; deux sont ajoutés :
  « L en fonction de D (2021 N) » (droite par (50 ; 1), (100 ; 2), (150 ; 3), (200 ; 4) en cm, L = 0,02·D, k = 2·10⁻²)
  sur `ol_g5_autres` et sur la diapositive du national 2021 (`ol_x3c_2021_courbe` en attente,
  `ol_x3_national_2021` en ligne) ; « Une fente en lumière blanche » (tache blanche, bords colorés, rouge à
  l'extérieur) sur `ol_p5_fente_blanche`. Au plus 2 dessins par bloc ; aucun pour une définition, une méthode, le
  bilan ou la carte.
- **Calculs vérifiés** : 6,5·10⁻⁷/1,0·10⁻⁴ = 6,5·10⁻³ rad ; (1,0·10⁻⁴ × 2,6·10⁻²)/4,0 = 6,5·10⁻⁷ m ;
  2 × 5,8·10⁻⁷ × 1,4 / 2,7·10⁻² = 6,0·10⁻⁵ m ; 580 × 3,4/2,7 = 730 nm ; 580/1,5 = 387 nm ;
  3·10⁸/5,89·10⁻⁷ = 5,09·10¹⁴ Hz ; 355·10⁻⁹ × 5,09·10¹⁴ = 1,81·10⁸ m/s ; 474·10⁻⁹ × 3,91·10¹⁴ = 1,85·10⁸ m/s ;
  6·10⁻⁵ × 2·10⁻²/2 = 6·10⁻⁷ m ; 2 × 6·10⁻⁷ × 2/3·10⁻² = 8·10⁻⁵ m ; 2,4/1,8 = 1,33 ; 3·10⁸/1,33 = 2,26·10⁸ m/s.

## Découpage — cours en attente (`en_attente/phys_ch3_ondes_lumineuses.json`)

Même cahier que ci-dessus, bloc par bloc (3 à 6 lignes, 0 à 2 dessins).

| Bloc | Diapositives | Lignes | Dessins |
|---|---|---|---|
| `ol_s1_b1` | ol_d1_tout_droit, ol_d2_fente_fine, ol_d3_figure | 5 | Figure de diffraction (écran vu de face) |
| `ol_s1_b2` | ol_d4_onde, ol_d5_montage, ol_d6_fil | 6 | Le montage de diffraction |
| `ol_s1_b3r` | ol_p1_radian, ol_t1_theta, ol_t2_fente_plus_fine | 4 | L'angle en radian ; L'écart angulaire θ |
| `ol_s1_b3` | ol_l1_metre, ol_t3_couleur, ol_t4_relation | 5 | — |
| `ol_s2_bt` | ol_p2_tangente, ol_l2_triangle, ol_l3_tan | 5 | La tangente ; Le triangle rectangle du montage |
| `ol_s2_b1` | ol_l4_petit_angle, ol_l5_egalite, ol_l6_isoler | 5 | — |
| `ol_s2_b2` | ol_l7_calcul_lambda, ol_l8_ordre_grandeur, ol_l9_etablir | 6 | — |
| `ol_s2_b3` | ol_c1_qui_change, ol_c2_haut_bas, ol_c2b_en_bas | 5 | — |
| `ol_s3_b1` | ol_c3_rapport, ol_c4_cheveu | 4 | — |
| `ol_s3_b2` | ol_g1_points, ol_g2_inverse, ol_g3_pente | 5 | L en fonction de 1/a |
| `ol_s3_b2b` | ol_g4_identifier, ol_g6_theta, ol_g5_autres | 5 | θ en fonction de 1/a ; L en fonction de D (2021 N) |
| `ol_s3_b3r` | ol_r1_monochromatique, ol_r2_vide, ol_r2b_celerite | 4 | — |
| `ol_s3_b3` | ol_r3_lambda0, ol_r4_spectre | 4 | Le spectre visible |
| `ol_s4_b1` | ol_n1_ralentit, ol_n2_frequence, ol_n3_resserre | 4 | L'onde lumineuse entre dans le verre |
| `ol_s4_b2` | ol_c5_cuve, ol_n4_indice, ol_n5_lambda_n, ol_n6_cuve | 6 | — |
| `ol_s4_b3` | ol_p1_blanche, ol_p2_violet, ol_p3_deux_celerites | 4 | Le prisme disperse la lumière blanche |
| `ol_s4_b4` | ol_p4_dispersif, ol_p5_fente_blanche | 4 | Une fente en lumière blanche (écran vu de face) |
| `ol_s5_b1` | ol_x1_cas_types, ol_x2_national_2023 | 3 | — |
| `ol_s5_b1b` | ol_x2b_2023_rouge | 3 | — |
| `ol_s5_b1c` | ol_x3_national_2021 | 3 | — |
| `ol_s5_b1d` | ol_x3b_2021_prisme | 3 | — |
| `ol_s5_b1e` | ol_x3c_2021_courbe | 3 | L en fonction de D (2021 N) |
| `ol_s5_b1f` | ol_x3d_2021_lambda | 3 | — |
| `ol_s5_b1g` | ol_x4_national_2025 | 3 | — |
| `ol_s5_b1h` | ol_x4b_2025_indice | 3 | — |
| `ol_s5_b2` | ol_b1_bilan, ol_b2_carte | 3 | — |

## Découpage — cours en ligne (`phys_ch3_ondes_lumineuses.json`)

Le cours en ligne a l'ancien ordre : « tout en mètre » est la première diapositive de la partie III, la cuve est en
partie IV, le bloc des courbes a cinq diapositives, et quatre blocs commencent une partie en leur milieu
(`ol_s1_b3` II→III, `ol_s3_b1` IV→V, `ol_s3_b3` VI→VII, `ol_s4_b2` VII→VIII) : ces quatre-là ont une ligne par
diapositive (l'écran les range sous le titre de leur diapositive, et le titre de la partie tombe à sa place) ; la
numérotation des blocs voisins suit celle des diapositives (par ex. partie III : « 1. Tout en mètre » est le titre
de la diapositive, le bloc suivant commence à « 2. Rappel : … tan θ »). Les quatre nationaux tiennent dans un bloc
(une ligne par sujet).

| Bloc | Diapositives | Lignes | Dessins |
|---|---|---|---|
| `ol_s1_b1` | ol_d1_tout_droit, ol_d2_fente_fine, ol_d3_figure | 5 | Figure de diffraction (écran vu de face) |
| `ol_s1_b2` | ol_d4_onde, ol_d5_montage, ol_d6_fil | 6 | Le montage de diffraction |
| `ol_s1_b3r` | ol_p1_radian, ol_t1_theta, ol_t2_fente_plus_fine | 4 | L'angle en radian ; L'écart angulaire θ |
| `ol_s1_b3` | ol_t3_couleur, ol_t4_relation, ol_l1_metre | 3 | — |
| `ol_s2_bt` | ol_p2_tangente, ol_l2_triangle, ol_l3_tan | 5 | La tangente ; Le triangle rectangle du montage |
| `ol_s2_b1` | ol_l4_petit_angle, ol_l5_egalite, ol_l6_isoler | 5 | — |
| `ol_s2_b2` | ol_l7_calcul_lambda, ol_l8_ordre_grandeur, ol_l9_etablir | 6 | — |
| `ol_s2_b3` | ol_c1_qui_change, ol_c2_haut_bas, ol_c2b_en_bas | 5 | — |
| `ol_s3_b1` | ol_c3_rapport, ol_c4_cheveu, ol_c5_cuve, ol_g1_points | 4 | — |
| `ol_s3_b2` | ol_g2_inverse, ol_g3_pente, ol_g4_identifier, ol_g6_theta, ol_g5_autres | 6 | L en fonction de 1/a ; θ en fonction de 1/a |
| `ol_s3_b3r` | ol_r1_monochromatique, ol_r2_vide, ol_r2b_celerite | 4 | — |
| `ol_s3_b3` | ol_r3_lambda0, ol_r4_spectre, ol_n1_ralentit | 3 | Le spectre visible |
| `ol_s4_b1` | ol_n2_frequence, ol_n3_resserre, ol_n4_indice | 4 | L'onde lumineuse entre dans le verre |
| `ol_s4_b2` | ol_n5_lambda_n, ol_n6_cuve, ol_p1_blanche, ol_p2_violet | 4 | Le prisme disperse la lumière blanche |
| `ol_s4_b3` | ol_p3_deux_celerites, ol_p4_dispersif, ol_p5_fente_blanche | 5 | Une fente en lumière blanche (écran vu de face) |
| `ol_s5_b1` | ol_x1_cas_types, ol_x2_national_2023, ol_x3_national_2021, ol_x4_national_2025 | 5 | L en fonction de D (2021 N) |
| `ol_s5_b2` | ol_b1_bilan, ol_b2_carte | 3 | — |

## Ce qui reste

- Le cas type « analyse dimensionnelle » (2019 R) n'est pas enseigné dans le cours : pas de ligne de cahier.
- Les deux nouveaux dessins sont vérifiés par `verifier_figures_cahier.py` (0 erreur, 0 avertissement) mais n'ont
  pas été rendus dans un navigateur.
- Le bilan (`ol_b1_bilan`) numérote 1 à 8 ; ses titres recoupent ceux des parties I à VIII du cahier.
