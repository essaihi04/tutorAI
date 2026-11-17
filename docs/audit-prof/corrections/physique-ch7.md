## Dipôle RL

Fichier : `backend/data/courses/en_attente/phys_ch7_dipole_RL.json` (repris de la copie en attente du matin, rien de perdu). Cours en ligne non touché. Script de correction : `scratchpad/ch7/corriger.py` ; copie d'avant : `scratchpad/ch7/avant.json`.

### Manques corrigés
| Constat (audit) | Ce qui a été fait | Diapo(s) |
|---|---|---|
| Haute : à la rupture, la solution est donnée sans être vérifiée | Nouvelle diapo : i = A·e^(−t/τ) + B, dérivée, remplacement, regroupement, B = 0, A ≠ 0 donc τ = L/(R + r) (7 lignes au centre, une par mot). Sur rl_t2, condition initiale i(0) = I₀ donc A = I₀ (voix réécrite) | rl_t2a_verifier (nouvelle, vue `figures.html?fig=fig_ed_rupture`, qui existait mais n'était pas utilisée), rl_t2_descente |
| Haute : forme A + B·e^(−t/τ) absente, condition initiale jamais utilisée | Deux nouvelles diapos : (1) A et τ trouvés par l'équation (6 lignes) ; (2) condition initiale i(0) = 0, donc B = −A = −I₀ (4 lignes). Nouvel exercice de bloc chiffré (B = −0,25 A) avec démonstration et réactions juste / faux 1 / faux 2 | rl_s4b_forme, rl_s4c_condition (vue `courbe.html?vue=trace`), bloc rl_s3_b1b |
| Haute : u_R(t) jamais écrit | u_R(t) = R·I₀(1 − e^(−t/τ)), avec R·I₀ = 5 V : écran, centre, cahier, voix | rl_s4_A |
| Haute : u_b(t) pour r ≠ 0 absent ; idéale sans calcul | Établi ligne par ligne : u_b = E − R·i, puis E − R·I₀ = r·I₀, donc u_b(t) = r·I₀ + R·I₀·e^(−t/τ) ; u_b(0) = E ; u_b → r·I₀ ; cas idéal E·e^(−t/τ) (8 lignes au centre, voix réécrite) | rl_l6_ub |
| Moyenne : TP (GBF + R, voies Y₁/Y₂, u_Y2 = −R·i) | Écrit : montage du TP, masse commune, i = −u_Y2/R, L = u_b/(di/dt) ; schéma du montage au cahier (cahier_figures) | rl_b6_triangle, rl_b7_inductance |
| Moyenne : schéma équivalent | Bobine idéale L en série avec r, ajouté à l'écran, au centre, à la voix et au cahier (2ᵉ figure : le schéma équivalent) | rl_b8_reelle |
| Moyenne : équation en u_R à la rupture | (L/R)·du_R/dt + ((R + r)/R)·u_R = 0, puis (L/(R + r))·du_R/dt + u_R = 0 (écran, cahier, bloc) | rl_t1_rupture |
| Basse : bougie, lampe au néon | Ajoutés à l'écran et au cahier | rl_t3_diode |
| Basse : 5τ à la rupture | i(5τ) = I₀·e⁻⁵ ≈ 0,007·I₀ calculé (écran, centre, voix) | rl_t2_descente |
| Basse : acquisition informatisée | « oscilloscope ou acquisition informatisée » (écran, cahier) | rl_m1_montage |
| Basse : moteur qui soulève une masse | Ajouté à l'écran et au cahier | rl_l7_energie |
| Basse : u_b(t) à la rupture | u_b = −u_R = −R·I₀·e^(−t/τ) ; idéale −E·e^(−t/τ) (écran, cahier, voix) | rl_t2_descente |
| Oral seulement : « car le fil est long » | Écrit | rl_b1_bobine |
| Oral seulement : u_b saute à E « car la pente est grande » | Écrit : (di/dt)(0) = E/L, donc u_b(0) = L·(di/dt)(0) = E | rl_e6_ub |
| Oral seulement : 5τ, i ≈ A | Écrit : e⁻⁵ ≈ 0,007, donc i ≈ 0,99·A | rl_s1_forme |
| Oral seulement : « sache écrire ces trois lignes » | Écrit (phrase du bac « montrer que τ a la dimension d'un temps ») | rl_s5_dimension |
| Oral seulement : u_b grande et négative | Écrit | rl_t3_diode |
| Démonstration : « A ≠ 0 » manquait | A ≠ 0 et e^(−t/τ) ≠ 0 dans la voix, à l'écran et au cahier ; 4 lignes au centre au lieu de 2 | rl_s3_tau |
| Démonstration : pourquoi la tangente coupe l'asymptote à τ (exigé par la règle 37 : tangente écrite comme une équation) | (di/dt)(0) = I₀/τ ; i = (I₀/τ)·t ; (I₀/τ)·t = I₀ donc t = τ (centre, voix, cahier). Même chose à la rupture : i = I₀ − (I₀/τ)·t | rl_l1_tangente, rl_t2_descente |
| Notations | R_T = R + r (rl_e3) ; τ·di/dt + i = I₀ écrit (rl_e4) ; u_AB ajouté (rl_b8, rl_l6) | rl_e3_equation, rl_e4_formes, rl_b8_reelle, rl_l6_ub |
| Règle 38 (phrases du bac, valeurs calculées) | « le régime permanent est atteint au bout de 5τ » ; e⁻¹ ≈ 0,37 et e⁻⁵ ≈ 0,007 calculés ; r = (E − U₀)/I₀ avec son « car » ; fiche : conditions initiales, u_R(t), u_b(t) | rl_s6_pourcent, rl_n1_2022R, rl_bl_fiche |
| Masse commune (vu en corrigeant le TP) | rl_m1 : une des deux voies affiche l'opposé de sa tension (on l'inverse) | rl_m1_montage |

Blocs : rl_s3_b1 coupé en deux (3 à 4 diapos chacun) : rl_s3_b1 = [rp4, s1, s2, s3_tau] (exercice : dérivée de e^(−t/τ), reprise de rl_rp4/e0 ; retrouver : dérivée de i(t)) ; rl_s3_b1b = [s4_A, s4b, s4c] (exercice nouveau sur B ; retrouver d'avant). rl_t2a ajoutée au bloc rl_s3_b3 (5 diapos). Le bloc rl_s3_b2 passe en séance 4 (3 blocs par séance). Compétence C5 : + rl_s4b_forme, rl_s4c_condition, rl_t2a_verifier.

### Non corrigés et pourquoi
- Manques chez un seul professeur : non ajoutés (influence de E, tableau des inductances, droite u_L = f(I), E_m = L·u_R²/(2R²), t½ hors cadre). Exception : la tangente à l'origine écrite comme une équation, exigée par la règle 37.
- Le bloc rl_s3_b1b n'a pas de question « À toi » sur une diapo : la question sur B est son exercice de bloc. Une question sur rl_s4c serait collée à celle de rl_s5 (règle d'espacement). **À décider.**
- La simulation triangle.html ne dessine ni R ni l'oscilloscope (pas de nouvelle simulation) : le TP est écrit et dessiné au cahier seulement ; la voix de rl_b6/rl_b7 n'est pas changée.
- Équation en u_R à la rupture : écrite (écran, cahier), pas dite dans la voix de rl_t1 (voix enregistrée gardée).
- Réactions préparées existantes : non réécrites (l'audit n'y signale pas d'erreur).

### Démonstrations
Relues : toutes (questions, exercices et énoncés, exercices de fin de cours, exercices de bloc, preuves sur diapo, cahiers). Réécrites ou complétées : 8 preuves sur diapo (rl_s3_tau, rl_s4_A, rl_s4b, rl_s4c, rl_t2a, rl_t2, rl_l1, rl_l6), 6 démonstrations (exercice 2022 R de rl_s8 et sa copie au bloc rl_s3_b2 ; 2018 R de rl_l6 ; exercice « quelle courbe est u_R ? » de rl_e8, qui n'en avait pas ; exercice 2025 R de rl_b10 et sa copie au bloc rl_s1_b3, vérification coupée en deux lignes ; 1ʳᵉ ligne du bloc rl_s2_b1), 1 nouvelle (exercice du bloc rl_s3_b1b). Le reste était déjà complet (repris ce matin) et n'a pas changé.
- rl_t2_descente : « Solution : i(t) = I₀·e^(−t/τ) » donnée → vérifiée (rl_t2a : dérivée, remplacement, B = 0, A ≠ 0 donc τ) puis i(0) = I₀ donc A = I₀.
- 2018 R : « u_L(τ) = E·e^(−1) = 0,37·E » → u_L(0) = E·e⁰ = E donc E = 9 V ; e⁻¹ ≈ 0,37 sur sa ligne ; 0,37 × 9 ; 3,3 V.
- 2022 R : « U₀ = 490 × 10/500 = 9,8 V » avant d'avoir calculé R + r → R + r = 500 Ω d'abord, puis la relation, la substitution et le résultat chacun sur sa ligne.

### Voix à enregistrer (id)
- Diapos (audio retiré) : rl_b8_reelle, rl_s3_tau, rl_s4_A, rl_s4b_forme (nouvelle), rl_s4c_condition (nouvelle), rl_t2a_verifier (nouvelle), rl_t2_descente, rl_l1_tangente, rl_l6_ub.
- Démonstrations (parole nouvelle, sans audio) : rl_s8_R exercices_fin_de_cours[0] et bloc rl_s3_b2 ; rl_l6_ub exercices_fin_de_cours[1] ; rl_e8_2019R exercises[0] ; bloc rl_s3_b1b exercice. (Celles déjà sans audio depuis ce matin le restent.)
- Énoncé et réactions du nouvel exercice de bloc rl_s3_b1b : enonce_dit + 5 réactions (0/1, 0/2, 1/juste, 2/1, 2/2).

### Vérifications faites (résultats)
- JSON valide, LF, `ensure_ascii=False`, indent 2 ; relu juste avant chaque écriture.
- `verif_attente.py` : 55 diapos, 0 mot absent, 0 hors bloc, 0 doublon, 0 compétence inconnue, 9 diapos sans voix (celles listées plus haut).
- Chaque slide dans exactement un bloc, blocs dans l'ordre du cours ; chaque competence_id existe ; chaque diapo est dans une compétence.
- Ordre des mots : chaque ligne de démonstration et chaque entrée du centre apparaît dans l'ordre de la voix (un défaut d'avant corrigé : 2024 N, ligne « τ = −1/a » qui sortait trop tôt, sur l'exercice de rl_n2 et sa copie de bloc).
- `verifier_figures_cahier.py` : 12 figures, 0 erreur, 0 avertissement (2 nouvelles : montage du TP, schéma équivalent).
- Voix nouvelles : aucun chiffre ni symbole, pas de tachkil.
- Calculs refaits en Python : e⁻¹ = 0,368 ; 1 − e⁻¹ = 0,632 ; e⁻⁵ = 0,0067 ; 1 − e⁻⁵ = 0,993 ; 12/48 = 0,25 ; 0,37 × 9 = 3,33 (9·e⁻¹ = 3,31) ; 490 × 10/500 = 9,8 ; 1/500 = 2·10⁻³ ; E/L = 6/0,12 = 50 A/s ; R·I₀ = 5 V ; r·I₀ = 1 V ; r·I₀ + R·I₀ = 6 V = E.
