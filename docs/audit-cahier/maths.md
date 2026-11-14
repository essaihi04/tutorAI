# Audit des dessins du cahier — Mathématiques (14 novembre 2026)

Six cours (`backend/data/courses/math_ch1…ch6_*.json`). Règle suivie : un dessin par bloc au plus, seulement là où la
notion se lit sur une courbe, un axe ou le plan ; rien pour les cartes, les rappels, les règles de calcul purement
algébriques, les rédactions et les bilans. Le bloc reçoit la figure de sa diapo (`blocs[].cahier_figures`).
Vérification : `python backend/scripts/verifier_figures_cahier.py` → 0 erreur, 0 avertissement sur les six fichiers ;
rendu contrôlé visuellement avec `FigureCahier.tsx`. Axes de maths : `"unite": ""` (grandeurs sans dimension).

**Le format ne permet pas (rapporté, rendu non modifié)**
- Le filtre « craie » de `FigureCahier.tsx` a sa région en *objectBoundingBox* (`x=-5% … height=110%`) : un `ligne` ou
  une `fleche` **parfaitement horizontal ou vertical** (boîte de hauteur ou de largeur nulle) **n'apparaît pas**.
  Contournement dans ces figures : petit pied perpendiculaire, pointe dessinée à la main, ou `rect` fin (bande). Un
  `filterUnits="userSpaceOnUse"` (ou une région en pixels) réglerait le problème pour tous les groupes.
- Tableau de variations : une double barre au milieu ne porte qu'une valeur (impossible d'écrire −∞ à gauche et +∞ à
  droite de 0 pour x + 1/x sur ℝ*). Les tableaux à double barre sont donc faits sur ]0 ; +∞[ (barre en tête).
- Les `titre` ne lisent pas la notation `C_f` (texte brut) : les titres l'évitent.

## Ch. 1 — Limites et continuité (12 dessins, 12 blocs)

| Bloc | Diapos | Dessin | Pourquoi |
|---|---|---|---|
| s1_b1 | carte, bases, l1_chemin | **l1** : droite y = x + 1 trouée en (1 ; 2), deux chemins | la limite sans f(1) : l'image fonde tout le chapitre |
| s1_b2 | l2, l3, l4 | — | méthode et liste de formes indéterminées (verbal) |
| s1_b3 | l5, l6, l7 | — | calcul algébrique (facteur, conjugué, degré) |
| s2_b1 | l8, l9, l10_signe | **l10** : 1/(x − 1), +∞ à droite, −∞ à gauche | signe de 0⁺ / 0⁻ : se voit aux deux branches |
| s2_b2 | l11_interpreter, l12, l13 | **l11** : 2 + 1/(x − 1), asymptotes x = 1, y = 2 | interprétation géométrique, tombe au national |
| s2_b3 | c1_soudee, c2, c3 | **c1** : courbe qui saute en a (ℓ ≠ f(a)) | « soudée ou coupée » : la définition en image |
| s3_b1 | c4_parametre, c5, i1 | **c4** : 3x − 1 et x² + 1 soudées en (1 ; 2) | la valeur de m qui soude, exercice type |
| s3_b2 | i2, i3, i4 | — | opérations sur la continuité (verbal) |
| s3_b3 | j1, j2_croissante, j3 | **j2** : f([1 ; 3]) = [2 ; 7] en jaune sur les axes | image d'un intervalle, valeurs du cours |
| s4_b1 | j4, j5, t1_couper_axe, t2 | **t1** : f(a) < 0, f(b) > 0, la courbe coupe en α | TVI : l'idée à retenir |
| s4_b2 | t3, t4_au_moins_une, t5 | **t4** : trois solutions α₁, α₂, α₃ | « au moins une » ≠ « une seule » |
| s4_b3 | t6, t7_valeur_k, t8, t9 | **t7** : la droite y = k coupe la courbe en c | f(x) = k, cas fréquent en devoir |
| s5_b1 | d1…d4 | **d3** : x³ + 2x − 1, f(0) = −1, f(1/2) = 1/8, moitié [0 ; 1/2] | dichotomie : quelle moitié garder |
| s5_b2 | r1, r2_strictement_monotone, r3, r4 | **r2** : x² et y = 4, antécédents −2 et 2 | pourquoi « strictement monotone » |
| s5_b3 | r5, r6_miroir, r7 | **r6** : x² + 1 et √(x − 1) symétriques / y = x, M(2 ; 5) ↔ M′(5 ; 2) | construire C_f⁻¹ : tombe au national |
| s6_b1…s7_b3 | r8, r9, racines n-ièmes, puissances, limites avec racines, bilan, carte | — | calcul algébrique ; bilan et carte exclus ; ⁿ√ / xⁿ redirait r6 |

## Ch. 2 — Dérivation et étude de fonctions (15 dessins, 15 blocs)

| Bloc | Diapos | Dessin | Pourquoi |
|---|---|---|---|
| s1_b1 | carte, bases, nd1_secante | **nd1** : parabole, A(1 ; 1), M(2 ; 4), sécante de pente 3 | le taux = une pente |
| s1_b2 | nd2, nd3_nombre_derive, nd4 | **nd3** : la sécante devient la tangente (pente 2) | le nombre dérivé en image |
| s1_b3 | tg1, tg2_ecrire, tg3 | **tg2** : x + 1/x, tangente y = (3/4)x + 1 en A(2 ; 5/2) | tangente : question du national |
| s2_b1 | dt1, dt2, dt3_anguleux | **dt3** : \|x² − 1\| en A(1 ; 0), demi-tangentes de pentes 2 et −2 | point anguleux |
| s2_b2 | dt4_infini, dt5, dt6 | **dt4** : √x, demi-tangente verticale en 0 | non dérivable ≠ rien à dessiner |
| s2_b3, s3_b1 | dérivées usuelles, composées | — | formules (verbal) |
| s3_b2 | va1…va4_tableau | **va4** : tableau de variations de x³ − 3x | le tableau, dessin type |
| s3_b3 | va5_double_barre, va6, va7 | **va5** : tableau de x + 1/x sur ]0 ; +∞[, double barre en 0 | valeur exclue ≠ zéro |
| s4_b1 | co1, co2_traverse, co3, co4 | **co2** : x³ − 3x, tangente y = −3x en I, concave / convexe | point d'inflexion |
| s4_b2 | bi1…bi4 | **bi3** : 2x + 1 + 1/x et (Δ) : y = 2x + 1, écart 1/x | asymptote oblique (les asymptotes horizontale/verticale sont déjà dessinées au ch. 1) |
| s4_b3 | bi5_direction, bi6, bi7 | **bi5** : x + √x et y = x, écart √x qui grandit | branche parabolique de direction y = ax |
| s5_b1 | pr1, pr2_signe, pr3 | **pr2** : x + 1/x au-dessus / en dessous de y = x | position relative par le signe |
| s5_b2 | sy1…sy4 | **sy3** : (x + 1)/(x − 2), Ω(2 ; 1), M(3 ; 4) et M′(1 ; −2) | centre de symétrie |
| s5_b3 | tr1, tr2, tr3 | — | ordre du tracé (méthode) ; la courbe complète est en s6_b1 |
| s6_b1 | tr4, tr5, tr6_lire | **tr6** : y = 3 coupe x + 1/x en deux points | lecture graphique f(x) = m |
| s6_b2 | rec1, rec2_pente, rec3 | **rec2** : x² + 1 et sa réciproque, pentes 4 et 1/4 | (f⁻¹)′(y₀) = 1/f′(x₀) en image |
| s6_b3 | rec4, rec5, rec6 | — | même figure que rec2 / ch. 1 r6 |
| s7_b1 | ec1, ec2, ec3_etude | **ec3** : x√(x + 1), demi-tangente verticale vers le bas, minimum en −2/3 | l'étude complète, en une courbe |
| s7_b2 | ec4, bilan, carte | — | rappel, bilan, carte |

## Ch. 3 — Suites numériques (7 dessins, 7 blocs)

| Bloc | Diapos | Dessin | Pourquoi |
|---|---|---|---|
| s1_b1 | questions, bases, a1, a2 | — | définitions verbales |
| s1_b2 | a3, a4_arithmetique, a5 | **a4** : uₙ = 3n + 2 sur un axe, pas de +3 | « des pas égaux » |
| s1_b3 | a6…a9 | — | formules (terme général, sommes) |
| s2_b1, s2_b2 | récurrence | — | rédaction et méthodes (verbal) |
| s2_b3 | b1, b2_bornee, m1 | **b2** : uₙ = 5n²/(n² + 2) sous le plafond 5 | bornée, plafond jamais atteint |
| s3_b1, s3_b2 | sens de variation, suite auxiliaire | — | calcul algébrique |
| s3_b3 | x4, x5, l1_converge | **l1** : uₙ = 16 + (1/4)ⁿ se serre sur 16 | convergence en image |
| s4_b1 | l2, l3, l4 | — | la « règle de q » du bloc suivant résume mieux |
| s4_b2 | l4b_glisse_q, l5, l6, l7 | **l4b** : axe de q, zone ]−1 ; 1[ → 0, +∞, pas de limite | lim qⁿ : tombe à chaque sujet |
| s4_b3 | c1, c2, c3_plafond_limite, c4 | **c3** : suite croissante sous M, limite ℓ < M | ℓ ≤ M, pas forcément M (piège) |
| s5_b1 | c5, c6, c7_conclure, c8 | **c7** : uₙ (u₀ = 3/2, uₙ₊₁ = 2uₙ/(2uₙ + 5)) sous (3/2)(2/5)ⁿ | comparaison, national 2020 |
| s5_b2 | f1_escalier, f2, f3 | **f1** : escalier de f(x) = 2x/(x + 1), u₀ = 2, vers (1 ; 1) | représentation des termes, classique |
| s5_b3, s6_b1, s6_b2 | f4…f7, problèmes, bilan, carte | — | l'escalier dit déjà « courbe sous y = x » ; bilan exclu |

## Ch. 4 — Primitives (3 dessins, 3 blocs)

| Bloc | Diapos | Dessin | Pourquoi |
|---|---|---|---|
| s1_b1…s1_b3 | carte, définition, existence, F + k | — | définitions et rédaction ; la famille F + k se dessine en s2_b1 |
| s2_b1 | e4, e5, e6, e7 | **e6** : x² − 1, x², x² + 2, la seule par A(1 ; 3) | translation verticale + condition initiale |
| s2_b2 | u1, u2, u3 | — | tableau de formules |
| s2_b3 | u4, u5, u6 | **u6** : le cercle sin / cos / −sin / −cos, sens dériver / primitiver | moyen mnémotechnique du cours pour le signe |
| s3_b1…s4_b2 | linéarité, formes u′uⁿ, u′/u², u′/√u, dérivées reconnues | — | calcul algébrique (aucune courbe) |
| s4_b3 | r2, r3, g1, g2 | **g1** : F = x³/3 − x et f = x² − 1, tangentes horizontales en ±1 | f est la pente de F |
| s5_b1, s5_b2 | types national, intégrale à venir, bilan, carte | — | l'intégrale (aire) n'est pas enseignée dans ce cours |

## Ch. 5 — Fonction ln (8 dessins, 7 blocs)

| Bloc | Diapos | Dessin | Pourquoi |
|---|---|---|---|
| s1_b1 | carte, rappels, n1, n2 | — | la courbe de ln n'est pas encore définie |
| s1_b2 | n3, n4, c1, c2 | **c2** : courbe de ln, rose sous l'axe, verte au-dessus, (1 ; 0) | signe de ln x |
| s1_b3 | c3, c4, c5, d1 | **c5** : ln, point (e ; 1), tangente y = x − 1 | e et la tangente en 1 |
| s2_b1 | d2, d3, d4, a1 | — | domaines (tableaux de signe, verbal) |
| s2_b2 | a2, a3, a4, a5 | **a2** : ln(2x) = ln x montée de ln 2 | la règle du produit vue sur la courbe |
| s2_b3, s3_b1 | pièges, équations, inéquations | — | calcul |
| s3_b2 | q6, q7, l1, l2 | **l2** : asymptote x = 0, branche parabolique (Ox) | les deux limites de référence |
| s3_b3 | l3, l4, l5, l6 | **l4** : x ln x → 0 en 0⁺, négatif sur ]0 ; 1[ | limite de base du national 2021 |
| s4_b1 | l7, l8, v1 | — | calcul (limite déguisée, dérivée) |
| s4_b2 | v2, v3, p1 | **v3** : signe de f′ = (1 − ln x)/x², double barre en 0 (valeurs de f non écrites : le cours ne les donne pas) | tableau de signe avec ln |
| s4_b3 | p2, p3, e1 | — | ln x ≤ x − 1 est déjà dessiné en c5 |
| s5_b1 | e2, e3, e4, e5 | **e3** : tableau de variations (+∞ ↘ 3/2 ↗ +∞) **+ e4** : (C) au-dessus de y = x, contact en x = e | problème national 2019 : les deux dessins de la copie |
| s5_b2 | log, pH, bilan, carte | — | formules, bilan |

## Ch. 6 — Nombres complexes (8 dessins, 8 blocs)

Tous les repères sont orthonormés (`ratio` calculé pour la même échelle en x et y : angles et cercles justes).

| Bloc | Diapos | Dessin | Pourquoi |
|---|---|---|---|
| s1_b1 | carte, rappels, a1, a2 | **a2** : 1, i, −1, −i, deux quarts de tour | i² = −1 en image |
| s1_b2, s1_b3 | forme algébrique, calculs | — | calcul (le plan n'est pas encore introduit) |
| s2_b1 | p1, p2, p3, p4 | **p1** : M(3 ; 2) image de 3 + 2i, vecteurs u, v | le plan complexe |
| s2_b2 | j1, j2, j3, j4 | **j1** : M(3 + 2i) et M′(3 − 2i) | conjugué = symétrie / axe réel |
| s2_b3 | m1, m2, m3, m4 | **m1** : triangle OHM, \|3 + 4i\| = 5 | module = distance |
| s3_b1 | g1, g2, g3, g4 | **g1** : angle θ de u vers OM, \|z\| = OM | argument |
| s3_b2 | t1, t2, t3, t4 | **t3** : −√3 + i, θ = π − π/6 = 5π/6 | le quart choisit l'angle (piège fréquent) |
| s3_b3 | t5, t6, r1, r2 | **r2** : 3 + i → −1 + 3i, quart de tour | multiplier par i |
| s4_b1 | r3…r6 | — | modules et arguments calculés (Moivre) |
| s4_b2 | r7, r8, i1, i2 | **i2** : A(1 + 2i), B(1 − 2i), Ω(5/2), ΩA = ΩB = 5/2 | distances, national 2025 |
| s4_b3 | sujets 2023, 2024, bilan, carte | — | rédaction, bilan |

## Dessins faits (53 sur les diapos, 52 blocs illustrés)

- **Ch. 1** : lc_l1_chemin, lc_l10_signe, lc_l11_interpreter, lc_c1_soudee, lc_c4_parametre, lc_j2_croissante,
  lc_t1_couper_axe, lc_t4_au_moins_une, lc_t7_valeur_k, lc_d3_bonne_moitie, lc_r2_strictement_monotone, lc_r6_miroir.
- **Ch. 2** : df_nd1_secante, df_nd3_nombre_derive, df_tg2_ecrire, df_dt3_anguleux, df_dt4_infini, df_va4_tableau,
  df_va5_double_barre, df_co2_traverse, df_bi3_oblique, df_bi5_direction, df_pr2_signe, df_sy3_centre, df_tr6_lire,
  df_rec2_pente, df_ec3_etude.
- **Ch. 3** : su_a4_arithmetique, su_b2_bornee, su_l1_converge, su_l4b_glisse_q, su_c3_plafond_limite, su_c7_conclure,
  su_f1_escalier.
- **Ch. 4** : pr_e6, pr_u6, pr_g1.
- **Ch. 5** : ln_c2, ln_c5, ln_a2, ln_l2, ln_l4, ln_v3, ln_e3, ln_e4.
- **Ch. 6** : nc_a2, nc_p1, nc_j1, nc_m1, nc_g1, nc_t3, nc_r2, nc_i2.

**Points à relire** : lc_c1 et lc_t1/t4/t7, lc_j2 utilisent une courbe d'allure choisie (le cours parle de f
générique ; j2 passe bien par (1 ; 2) et (3 ; 7)). su_c3 : suite d'exemple 1,5 − 1,5·(1/2)ⁿ, graduations « ℓ » et « M »
sans valeurs. pr2 / tr6 (ch. 2) supposent f(x) = x + 1/x, cohérent avec les écarts donnés en pr1/pr2 et la courbe des
diapos tr. ln_v3 : le cours ne nomme pas f, le tableau laisse les valeurs vides.
