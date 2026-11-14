# Audit des dessins du cahier : physique, chapitres 1 à 5

14 novembre 2026. Fichiers : `phys_ch1_waves_exemple`, `phys_ch2_ondes_periodiques`, `phys_ch3_ondes_lumineuses`,
`phys_ch4_radioactivite`, `phys_ch5_energie_nucleaire` (dans `backend/data/courses/`). Seuls les champs `cahier_figures`
ont été posés. Vérification : `verifier_figures_cahier.py` donne 0 erreur et 0 avertissement sur les 5 fichiers. Les
28 dessins ont aussi été rendus avec `FigureCahier.tsx` (Chrome headless) et relus à l'œil.

Règle suivie : au plus un dessin par bloc (deux quand le bloc enseigne une paire qui se compare). Pas de dessin pour
une définition seulement verbale, une conversion, un calcul rédigé, un énoncé du national, un bilan ou une carte.
Les valeurs et les notations sont celles du `cahier`, du `screen_content` et des simulations du cours.

## Ch. 1 : Ondes mécaniques progressives (`phys_ch1_waves_exemple`)

| Bloc / diapo | Dessin | Pourquoi |
|---|---|---|
| wx_s1_b1 / wx_o1_bouee | non | Question d'ouverture |
| wx_s1_b1 / **wx_i1_corde** | **oui** : corde secouée en S, perturbation, élongation y, M qui monte et descend sur place | Le vocabulaire (source, perturbation, élongation) se voit sur un seul croquis : « M ne suit pas la perturbation » |
| wx_s1_b1 / wx_i2_definition | non | Définition verbale |
| wx_s1_b2 / **wx_i3_types** | **oui** : corde (⊥) et ressort (∥), avec la direction de M et celle de la propagation | Distinction classique au bac, qu'on retient par les flèches |
| wx_s1_b2 / wx_c1_celerite, wx_c2_facteurs | non | Formule et liste de facteurs (la simulation milieux.html suffit) |
| wx_s1_b3 / wx_r1_retard | non | Le retard se lit sur le dessin de wx_l1 (τ en abscisse) |
| wx_s1_b3 / **wx_r2_duree_longueur** | **oui** : aspect y(x) avec S, la queue, le front, L cotée, le sens de v | La « photo de la corde » est le premier cas type du national |
| wx_s1_b3 / **wx_l1_aspect** | **oui** : film y_M(t) avec τ, θ cotée, le front à gauche | Le « miroir » photo/film, le piège n° 1 : même bosse, mais front à gauche |
| wx_s1_b3 / wx_l2_sens | non | Le bloc a déjà 2 dessins, et la règle tient en une phrase |
| wx_s2_b1 / **wx_m1_micros** | **oui** : oscillogramme de deux micros, τ entre les deux débuts | Mesure de τ « début avec début », un cas du national |
| wx_s2_b1 / wx_m2_sonar, wx_b1_redaction | non | Formule de l'écho, méthode de rédaction |
| wx_s2_b2 (national, bilan, carte) | non | Synthèses |

## Ch. 2 : Ondes progressives périodiques (`phys_ch2_ondes_periodiques`)

| Bloc / diapo | Dessin | Pourquoi |
|---|---|---|
| op_s1_b1 (vibreur, acquis, « périodique ») | non | Introduction, rappels |
| op_s1_b2 / op_o4, op_o5 | non | Définitions ; la sinusoïde se dessine sur la diapo suivante |
| op_s1_b2 / **op_t1_periode** | **oui** : y_M(t) sinusoïdale, deux crêtes, T = 0,5 s cotée | Lire T entre deux crêtes voisines |
| op_s1_b3 (même période, N, N = 1/T) | non | Énoncés et formule |
| op_s2_b1 (convertir, film, oscillo) | non | Conversions ; la lecture de T est déjà dessinée en op_t1 |
| op_s2_b2 / **op_l2_lambda** | **oui** : photo y(x) jusqu'au front, λ = 0,5 m cotée de crête à crête | La double périodicité : à comparer avec op_t1 (axe en m et non en s) |
| op_s2_b2 / op_l1_photo, op_l3_axe | non | Couvert par le dessin de op_l2 |
| op_s2_b3 / **op_l5_intervalles** | **oui** : cuve vue de dessus, 5 crêtes, règle d = 4,5 cm sur 3 intervalles, λ | Le piège « traits ou intervalles » |
| op_s2_b3 / op_l4_rides, op_l6_source | non | Un dessin suffit pour le bloc |
| op_s3_b1 (λ = v·T, rédaction, photo datée) | non | Relations et calcul |
| op_s3_b2 / **op_p2_opposition** | **oui** : sinusoïde, M et P en phase (λ), M et Q en opposition (λ/2) | d = kλ ou (2k+1)λ/2, à voir sur la corde |
| op_s3_b2 / op_p1, op_p3, op_p4 | non | Couvert par le dessin, ou méthode de calcul |
| op_s3_b3, op_s4_b1 (stroboscope, récepteurs) | non | Montages : le texte suffit, les simulations montrent l'expérience |
| op_s4_b2 / **op_d3_justifier** | **oui** : ondes planes, paroi percée (a), arcs centrés sur l'ouverture, espacés de λ | La diapo demande explicitement le dessin (question type du bac) |
| op_s4_b3 (fréquence, air, dispersif) | non | Calculs et définition |
| op_s5_b1 / **op_r3_trois_lectures** | **oui** : y_M(t) qui démarre à τ = 10 ms, T = 20 ms, l'amplitude | Ne pas confondre τ et T (national 2022) |
| op_s5_b2 (y_S, national 2017, 2020) | non | Les énoncés ont leurs propres figures |
| op_s5_b3 (devoir, bilan, carte) | non | Synthèses |

## Ch. 3 : Propagation d'une onde lumineuse (`phys_ch3_ondes_lumineuses`)

| Bloc / diapo | Dessin | Pourquoi |
|---|---|---|
| ol_s1_b1 / **ol_d3_figure** | **oui** : écran vu de face, la tache centrale deux fois plus large, la figure étalée à l'horizontale (fente verticale) | Allure à reconnaître et à dessiner |
| ol_s1_b1 / ol_d1, ol_d2 | non | Constats |
| ol_s1_b2 (onde, a/D/L, fil) | non | Mots du montage ; ils figurent sur les dessins suivants |
| ol_s1_b3 / **ol_t1_theta** | **oui** : fente, écran, rayons vers le centre et vers les bords, l'angle θ | Où est θ : du centre au bord, pas d'un bord à l'autre |
| ol_s1_b3 / ol_t2–t4 | non | Variations et formule |
| ol_s2_b1 / **ol_l2_triangle** | **oui** : triangle rectangle, D côté adjacent, L/2 côté opposé, angle droit sur l'écran | Base de tan θ = L/(2D), que le bac demande d'établir |
| ol_s2_b1 / ol_l1, l3, l4 | non | Conversions, formules |
| ol_s2_b2, ol_s2_b3 (égalité, isoler, calcul, établir, qui change) | non | Algèbre et rédaction |
| ol_s3_b1 (rapport, cheveu, cuve, 5 fentes) | non | Calculs ; la courbe se dessine dans le bloc suivant |
| ol_s3_b2 / **ol_g3_pente** | **oui** : L = f(1/a), une droite par l'origine, 4 points (2,5 ; 5 ; 10 ; 20 mm⁻¹), k = 2,6 mm² | Exploiter une courbe, un cas du national |
| ol_s3_b3 / **ol_r4_spectre** | **oui** : bande du visible de 400 à 800 nm, l'UV et l'IR de part et d'autre | Bornes à retenir |
| ol_s3_b3 / ol_r1–r3 | non | Définitions et formule |
| ol_s4_b1 / **ol_n3_resserre** | **oui** : onde dans l'air (λ₀ = 600 nm) puis dans le verre (λ = 400 nm) | λ diminue, ν reste la même |
| ol_s4_b2 (n = c/v, λ = λ₀/n, prisme) | non | Formules ; le prisme est dessiné en ol_p2 |
| ol_s4_b3 / **ol_p2_violet** | **oui** : prisme, lumière blanche, rouge le moins dévié, violet le plus dévié | Dispersion (seule partie du prisme au national) |
| ol_s5_b1 (cas types, national) | non | Énoncés |
| ol_s5_b2 / **ol_q3_dans_verre** | **oui** : trajet d'un rayon, normales en pointillé, i, r, r′, i′, A | « Tous les angles depuis la normale » (devoirs) |
| ol_s5_b3 (déviation, bilan, carte) | non | Formule et synthèses |

## Ch. 4 : Décroissance radioactive (`phys_ch4_radioactivite`)

| Bloc / diapo | Dessin | Pourquoi |
|---|---|---|
| ra_s1_b1, ra_s1_b2 (noyau, notation, isotopes, axes N–Z) | non | Notation et définitions ; le diagramme est dessiné complet dans le bloc suivant |
| ra_s1_b3 / **ra_s3_zones** | **oui** : diagramme (N, Z), droite N = Z, vallée, zones β⁻ (au-dessus), β⁺ (au-dessous), α (lourds) | La carte de la stabilité |
| ra_s1_b3 / **ra_s4_fleches** | **oui** : un noyau père et ses trois flèches β⁻ (Z+1, N−1), β⁺ (Z−1, N+1), α (Z−2, N−2) | Pour lire une famille sur un diagramme (national 2024) |
| ra_s2_* (définition, Soddy, α, β, γ, famille) | non | Équations : le texte du cahier est la bonne forme |
| ra_s3_b1 (échantillon, équation différentielle, rappel ln) | non | Algèbre |
| ra_s3_b2 / **ra_l7_tau** | **oui** : N(t), la tangente à l'origine qui coupe l'axe en τ, N(τ) ≈ 0,37·N₀ | Lecture graphique de τ |
| ra_s3_b3 / **ra_t3_paliers** | **oui** : N(t), N₀/2, N₀/4, N₀/8 à t½, 2t½, 3t½ (t½ = 8 jours) | Lecture de t½, la plus fréquente au national |
| ra_s4_b1 (activité, Bq, unités) | non | Définition et conversions |
| ra_s4_b2 / **ra_a7_droite_ln** | **oui** : ln N = f(t), une droite (33 ; pente −λ = −0,0485 j⁻¹) | La pente donne −λ (national 2021) |
| ra_s4_b3 / **ra_c1_principe** | **oui** : activité constante tant que l'arbre est vivant, puis a₀·exp(−λt) après sa mort (a₀/2 à 5730 ans) | Le principe de la datation |
| ra_s5_* (cas types, national, bilan, carte) | non | Synthèses |

## Ch. 5 : Noyaux, masse et énergie (`phys_ch5_energie_nucleaire`)

| Bloc / diapo | Dessin | Pourquoi |
|---|---|---|
| en_s1_b1, en_s1_b2 (E = mc², unités, défaut de masse) | non | Formules et calculs |
| en_s1_b3 / **en_l2_former** | **oui** : deux niveaux (nucléons séparés en haut, noyau en bas), séparer ↑, former ↓, E_ℓ = Δm·c² | Sens de l'énergie de liaison (fournie ou libérée) |
| en_s2_b1 (E_ℓ/A, stabilité, piège) | non | Comparaisons chiffrées |
| en_s2_b2 / **en_a2_zones** | **oui** : courbe d'Aston −E_ℓ/A = f(A), creux vers Fe (A ≈ 56), bornes 20 et 190, flèches fusion et fission vers le creux | Courbe à reconnaître et à exploiter |
| en_s2_b3 (spontanée/provoquée, fission, chaîne, fusion) | non | Équations ; le croquis de la fission aurait demandé 12 éléments pour rien de plus que l'équation |
| en_s3_b1, en_s3_b2 (Soddy, bilans par les masses) | non | Calculs |
| en_s3_b3 / **en_e1_diagramme** | **oui** : diagramme énergétique de la fusion : nucléons, ²H + ³H, ⁴He + n ; 10,841 et 28,296 MeV, ΔE = −17,455 MeV | Diagramme du national 2023 et 2020 |
| en_s4_* (échantillon, comparaison, cas types, bilan, carte) | non | Calculs et synthèses |

## Les dessins faits (28 diapos, 25 blocs)

- **Ch. 1 (5 diapos, 4 blocs)** : wx_i1_corde « Une corde secouée en S » ; wx_i3_types « Transversale ou longitudinale ? » ;
  wx_r2_duree_longueur « Aspect de la corde à un instant t » ; wx_l1_aspect « Le film d'un point M » (bloc wx_s1_b3 : les
  deux) ; wx_m1_micros « Oscillogramme : deux micros ».
- **Ch. 2 (6 diapos, 6 blocs)** : op_t1_periode « Le film d'un point : la période T » ; op_l2_lambda « La photo de la corde :
  la longueur d'onde λ » ; op_l5_intervalles « Cuve à ondes vue de dessus » ; op_p2_opposition « En phase, en opposition de
  phase » ; op_d3_justifier « Diffraction par une ouverture (a ≤ λ) » ; op_r3_trois_lectures « Trois lectures sur le film de M ».
- **Ch. 3 (8 diapos, 8 blocs)** : ol_d3_figure « Figure de diffraction (écran vu de face) » ; ol_t1_theta « L'écart angulaire
  θ » ; ol_l2_triangle « Le triangle rectangle du montage » ; ol_g3_pente « L en fonction de 1/a » ; ol_r4_spectre « Le
  spectre visible » ; ol_n3_resserre « L'onde lumineuse entre dans le verre » ; ol_p2_violet « Le prisme disperse la lumière
  blanche » ; ol_q3_dans_verre « Le trajet d'un rayon dans le prisme ».
- **Ch. 4 (6 diapos, 5 blocs)** : ra_s3_zones « Le diagramme (N, Z) et ses zones » ; ra_s4_fleches « Le noyau redescend vers la
  vallée » (bloc ra_s1_b3 : les deux) ; ra_l7_tau « La tangente à l'origine donne τ » ; ra_t3_paliers « N₀/2, N₀/4, N₀/8 » ;
  ra_a7_droite_ln « La droite ln N = f(t) » ; ra_c1_principe « Le carbone 14 : vivant, puis mort ».
- **Ch. 5 (3 diapos, 3 blocs)** : en_l2_former « Séparer ou former le noyau » ; en_a2_zones « La courbe d'Aston » ;
  en_e1_diagramme « Diagramme énergétique de la fusion ».

## Remarques

- **Rendu** : le filtre « craie » de `FigureCahier.tsx` (unités objectBoundingBox par défaut) **efface tout trait strictement
  horizontal ou vertical** (`ligne`, `fleche`, dont la boîte englobante est de hauteur ou de largeur nulle). Contournement
  posé dans ces cours : ces traits sont inclinés de 1,5 px (lignes) ou de 4 px (flèches), ce qui ne se voit pas. La vraie
  correction est côté rendu (`filterUnits="userSpaceOnUse"` sur le filtre, ou pas de filtre sur les lignes).
- Les titres (`figcaption`) n'interprètent pas `_` : on y évite `y_M`. Les légendes n'interprètent pas `^` : on écrit `exp(−λt)`.
- Croquis schématiques, sans échelle : la vallée de stabilité est approchée par N = Z + 0,0065·Z², la courbe d'Aston est
  lissée sur les valeurs E_ℓ/A de la simulation aston.html (sans le pic de ⁴He), et l'écart rouge/violet du prisme est
  exagéré (indices 1,40 et 1,52) pour qu'on le voie.
