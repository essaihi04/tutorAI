# Audit des dessins du cahier — CHIMIE (14 novembre 2026)

Cours : `phys_ch10_cinetique`, `phys_ch11_transformations_deux_sens`, `phys_ch12_etat_equilibre`,
`phys_ch13_acides_bases` (dossier `backend/data/courses/`). Seuls `concentration.cahier_figures` et
`blocs[].cahier_figures` ont été posés. Vérifié : `verifier_figures_cahier.py` → 0 erreur, 0 avertissement sur les
quatre fichiers ; rendu contrôlé avec `FigureCahier.tsx` (rendu statique React + capture Chrome).

Règle suivie : un dessin là où la notion se dessine (courbe d'évolution, axe des pH / des pKa, montage, courbe de
dosage) ; rien pour une définition verbale, une formule, un calcul, une carte ou un bilan.

## Ch. 10 — Suivi temporel, vitesse de réaction (9 dessins, 6 blocs)

| Bloc / diapo | Dessin | Pourquoi |
|---|---|---|
| s1_b1 (carte, méthodes, mesures, trempe) | non | carte, méthodes verbales ; le tableau de mesures se dessine au bloc suivant |
| s1_b2 (titrage, tableau, x_max, n(I₂) = x) | non | calculs et tableau d'avancement : du texte |
| s1_b3 — `ci_a5_lecture` | **oui** : points de mesure + courbe + lecture à 8 min | geste « axe des t → courbe → axe des x » à retenir |
| s1_b3 — `ci_a7_palier` (→ bloc) | **oui** : courbe x(t), palier x_f = x_max | allure + état final, base de tout le chapitre |
| s2_b1 (cellule, σ = Σλ[X]) | non | formules, unités |
| s2_b2 — `ci_g5_droite` (→ bloc) | **oui** : droite σ(x) de σ₀ à σ_f | fonction affine, x_max/2 au milieu |
| s2_b2 — ballon/pression | non | relation de calcul ; méthode absente du national 2016-2025 |
| s2_b3 (volume de gaz, 2016 R, choisir, 2024 N) | non | calculs et lectures de sujets (pas de figure complète dans le cours) |
| s3_b1 — `ci_v3_tangente` (→ bloc) | **oui** : tangente à t = 0 par A (0 ; 0) et B (8 ; 2,0) | la pente de la tangente = dx/dt, tombe au national (5 sessions) |
| s3_b2 — `ci_v5_diminue` (→ bloc) | **oui** : tangentes à 0, 8, 20 min | la vitesse diminue : tangentes de plus en plus plates |
| s3_b2 — `ci_v8_temperature` (→ bloc) | **oui** : 20 °C et 40 °C, même palier | facteur cinétique : plus vite, même x_f |
| s3_b3 — `ci_h2_lecture` (→ bloc) | **oui** : lecture de t₁/₂ (x_f/2 = 1,0 mmol → 5,5 min) | t₁/₂ au national dans 9 sessions sur 10 |
| s3_b3 — `ci_h4_comparer` (→ bloc) | **oui** : deux t₁/₂ (1,8 et 5,5 min) | comparer deux transformations |
| s4_b1 — `ci_n4_reactif` (→ bloc) | **oui** : n_A(t) qui descend, t₁/₂ à n_A = 0,6 mol | piège 2023 N (ni 0,45 ni 0,3 mol) |
| s4_b2 (2025 N, 2021 N, 2018 R, 2017 R) | non | même idée que s3_b2/s3_b3 ; déjà 2 dessins de ce type |
| s4_b3 (unités, fiche, carte) | non | bilan |

Courbe de l'exemple A : x = 2,0·(1 − e^(−0,124·t)) passe par toutes les mesures du cours (0,44 ; 0,79 ; 1,06 ; 1,26 ;
1,43 ; 1,69 ; 1,84 ; 1,95 ; 1,99 mmol), donne (dx/dt)₀ = 0,25 mmol/min, v(8) = 0,92, v(20) = 0,21 mmol·L⁻¹·min⁻¹ et
t₁/₂ = 5,6 min. À 40 °C : k = 0,375 min⁻¹ → v(0) = 7,5 mmol·L⁻¹·min⁻¹ et t₁/₂ = 1,85 min.

## Ch. 11 — Transformations dans les deux sens (3 dessins, 3 blocs)

| Bloc / diapo | Dessin | Pourquoi |
|---|---|---|
| s1_b1 (flacons, acide, base) | non | définitions verbales |
| s1_b2 — `td_b4_reaction` (→ bloc) | **oui** : schéma du transfert de H⁺ entre deux couples | l'image « le proton passe » fixe la notion de réaction acido-basique |
| s1_b2 — pH, [H₃O⁺] | non | formules |
| s1_b3 (pH-mètre, acide/base avec l'eau, si totale) | non | équations et calculs |
| s2_b1 (tableau, x_max, x_f, τ) | non | τ = 0,040 n'est pas lisible sur un dessin ; la comparaison x_f/x_max est dessinée en s2_b3 |
| s2_b2 (τ = 1, τ = 10^(−pH)/C, deux sens, ⇌) | non | équations |
| s2_b3 — `td_e6_national` (→ bloc) | **oui** : deux courbes x(t), x_max = 0,3 mol, paliers 0,2 et 0,3 mol | totale ou limitée lu sur le palier (2017 N) |
| s3_b1 (conductimétrie, dilution) | non | calculs |
| s3_b2 — `td_n1_figure` (→ bloc) | **oui** : τ = f(pH), lectures pH 2,8 et 3,6 | figure du national 2021 R |
| s3_b3 (rédaction, fiche, carte) | non | bilan |

## Ch. 12 — État d'équilibre (3 dessins, 3 blocs)

| Bloc / diapo | Dessin | Pourquoi |
|---|---|---|
| s1_b1 (rappels τ, équilibre) | non | rappel |
| s1_b2 (écrire Qr) | non | expressions littérales |
| s1_b3 — `ee_i3_au_cours` (→ bloc) | **oui** : Qr en fonction de [H₃O⁺] jusqu'à Qr,éq | Qr évolue puis s'arrête : 1,01 ; 4,08 ; 9,28 ; 15,7 (×10⁻⁶) |
| s2_b1 (Qr,éq par le pH, trois C) | non | calculs (tableau de valeurs) |
| s2_b2 — `ee_k3_constante` (→ bloc) | **oui** : axe de Qr, des réactifs ou des produits vers K | même Qr,éq = K quel que soit l'état initial (exemples A et C) |
| s2_b3 (méthanoïque, conductimétrie) | non | calculs |
| s3_b1 — `ee_f3_courbe` (→ bloc) | **oui** : τ = f(C) pour deux K (C en échelle log) | « deux courbes » de la diapo ; τ dépend de K et de C |
| s3_b2, s3_b3 (nationaux, fiche, carte) | non | calculs ; 2017 R sans échelle de temps dans le cours |

## Ch. 13 — Réactions acide-base (10 dessins, 7 blocs)

| Bloc / diapo | Dessin | Pourquoi |
|---|---|---|
| s1_b1 (rappels) | non | rappel |
| s1_b2 — `ab_w3_solutions` (→ bloc) | **oui** : axe des pH, acide / neutre (7) / basique | repère à 25 °C à retenir |
| s1_b3 (soude, ammoniac, τ d'une base) | non | calculs |
| s2_b1 (Ka, pKa) | non | définitions et formules |
| s2_b2 — `ab_c3_classement` (→ bloc) | **oui** : axe vertical des pKa, 4 couples, acides à gauche | classement de force, tombe au national |
| s2_b3 (K = Ka₁/Ka₂) | non | formules |
| s3_b1 — `ab_p2_domaines` (→ bloc) | **oui** : domaines de prédominance, pKa = 4,8, pH = 3,41 | axe des pH AH / A⁻ |
| s3_b1 — `ab_p3_distribution` (→ bloc) | **oui** : diagramme de distribution, croisement à 50 % | lire pKa (2025 R, 2024 R) |
| s3_b2 — `ab_i2_virage` (→ bloc) | **oui** : zone de virage du BBT (jaune / vert 6,0–7,6 / bleu) | zone de virage |
| s3_b2 — `ab_d1_montage` (→ bloc) | **oui** : croquis du montage (burette, bécher, agitateur, pH-mètre) | schéma demandé au national |
| s3_b3 — `ab_d4_courbe` | **oui** : courbe pH = f(V_B) et le saut de pH | allure de la courbe de dosage |
| s3_b3 — `ab_d5_tangentes` (→ bloc) | **oui** : méthode des tangentes parallèles, E (20,0 mL ; 8,3) | méthode notée au national |
| s3_b3 — `ab_d6_derivee` | non | la hauteur du pic n'est pas donnée dans le cours ; 2 dessins proches suffisent |
| s4_b1 — `ab_e2_demi` (→ bloc) | **oui** : demi-équivalence (10 mL ; 4,8) et E (20 mL ; 8,3) | pH = pKa à V_BE/2, piège pH_E ≠ pKa |
| s4_b2 — `ab_e5_conductimetrie` (→ bloc) | **oui** : σ = f(V_B) en V, rupture de pente à 2,0 mL | dosage conductimétrique |
| s4_b3 (2024 R, 2023 R, fiche, carte) | non | lectures déjà dessinées (distribution, demi-équivalence) ; bilan |

Courbe de dosage (exemple J) : points du cours (3,41 ; 4,34 ; 4,80 ; 5,28 ; 6,08 ; 6,4 ; 8,25 ; 10,1 ; 10,39 ; 11,30)
complétés par pH = pKa + log(V/(20 − V)) avant E et pH = 14 + log(C_B·(V − 20)/(V + 20)) après E. Tangentes de pente
0,5 mL⁻¹ en V = 19,1 mL et 20,85 mL ; la parallèle médiane passe par pH 8,24 en V = 20 mL.

## Dessins faits (diapo → titre)

- ch10 : `ci_a5_lecture` Lire x à une date · `ci_a7_palier` La courbe x(t) et son palier · `ci_g5_droite` σ en fonction
  de x : une droite · `ci_v3_tangente` La tangente à t = 0 · `ci_v5_diminue` Des tangentes de plus en plus plates ·
  `ci_v8_temperature` Plus chaud, plus vite · `ci_h2_lecture` Lire t₁/₂ · `ci_h4_comparer` Comparer deux t₁/₂ ·
  `ci_n4_reactif` t₁/₂ sur une courbe de réactif.
- ch11 : `td_b4_reaction` Le proton passe d'un couple à l'autre · `td_e6_national` Totale ou limitée ? ·
  `td_n1_figure` τ en fonction du pH (2021 R).
- ch12 : `ee_i3_au_cours` Qr évolue jusqu'à l'équilibre · `ee_k3_constante` Qr arrive toujours à K ·
  `ee_f3_courbe` τ dépend de K et de C.
- ch13 : `ab_w3_solutions` Acide, neutre, basique (25 °C) · `ab_c3_classement` Classer les couples sur l'axe des pKa ·
  `ab_p2_domaines` Domaines de prédominance · `ab_p3_distribution` Diagramme de distribution · `ab_i2_virage` Zone de
  virage du BBT · `ab_d1_montage` Le montage du dosage · `ab_d4_courbe` La courbe de dosage · `ab_d5_tangentes` Méthode
  des tangentes parallèles · `ab_e2_demi` Demi-équivalence : pH = pKa · `ab_e5_conductimetrie` Dosage conductimétrique.

## Points d'attention

- Allures illustratives (pas de valeurs dans le cours) : l'échelle de temps de 2017 N (courbes reprises de ch10 :
  t₁/₂ = 8 et 2 min) et la courbe C₁ de 2023 N (seuls le palier, n₀ et t₁/₂ de C₂ sont donnés).
- `td_n1_figure` : la courbe τ = 1/(1 + 10^(3,72 − pH)) donne 0,107 et 0,43 aux lectures du sujet (0,10 et 0,45) ; les
  deux lectures du sujet ne tombent pas exactement sur une même courbe de ce type.
- Rendu : une `fleche` ou une `ligne` parfaitement horizontale ou verticale peut disparaître (le filtre « craie » est
  calculé sur la boîte englobante, de hauteur ou de largeur nulle). Contourné ici : axes avec un petit trait de départ,
  flèches légèrement inclinées, trait du pKa en `rect`. Les `titre` ne lisent pas les indices (`x_f` s'afficherait tel
  quel) : titres écrits sans « _ ».
