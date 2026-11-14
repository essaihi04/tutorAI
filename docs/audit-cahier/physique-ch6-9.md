# Audit des dessins du cahier — physique ch6 à ch9

14 novembre 2026. Format : `docs/audit-cahier/FORMAT.md`. Vérification : `verifier_figures_cahier.py` → 0 erreur, 0 avertissement
sur les quatre cours. Rendu contrôlé dans le navigateur (FigureCahier.tsx).

Règle suivie : au plus un dessin par bloc (deux quand le bloc enseigne deux lectures de courbe distinctes), seulement des
notions déjà enseignées. Pas de dessin pour les cartes, les prérequis, les équations à établir, les définitions verbales,
les sujets du national (qui reprennent une courbe déjà dessinée) ni les bilans.

## Ch6 — Dipôle RC (`phys_ch6_dipole_RC`)

| Bloc | Diapo retenue | Dessin | Pourquoi / pourquoi pas |
|---|---|---|---|
| rc_s1_b1 | rc_c1_plaques | Croquis : armatures A, B, isolant → symbole | La structure et le symbole se retiennent en les dessinant. Carte, prérequis, aiguilles : non. |
| rc_s1_b2 | rc_c5_intensite | q(t) et sa tangente : pente = i | i = dq/dt se comprend par la pente. q = C·u_C, électrons : verbal. |
| rc_s1_b3 | rc_g2_pente | Droite u_C(t), triangle Δt, Δu_C | Lecture de k puis C = I₀/k (2025 N). Associations série/parallèle : formules. |
| rc_s2_b1 | rc_m2_acquisition | Schéma RC fléché (E, R, C, i, u_R, u_C) | Convention récepteur : tombe à l'examen. La courbe de charge vient en s3_b2. |
| rc_s2_b2 | — | — | Établir l'équation : calcul, rien à dessiner. |
| rc_s2_b3 | — | — | Équations de u_R, i, décharge : calcul. |
| rc_s3_b1 | — | — | Trouver la solution : calcul. |
| rc_s3_b2 | rc_s6_tableau | Courbe de charge : τ, 0,63·E = 7,56 V, 5τ | Le point remarquable et le régime permanent. Les quatre courbes : redit. |
| rc_s3_b3 | rc_d1_decharge | Courbe de décharge : 0,37·E | La décharge n'a pas d'autre dessin. Dimension, influence : texte. |
| rc_s4_b1 | rc_l1_tangente + rc_l3_descente | Tangente à l'origine ∩ asymptote ; i(t) qui descend, tangente ∩ axe, 0,37·I₀ | Les deux méthodes de lecture de τ (8 sujets sur 20). |
| rc_s4_b2 | rc_l5_pente | Droite du_C/dt = f(u_C) (2021 N) | Courbe sans le temps : piège classique. Énergie : formule. |
| rc_s4_b3 | — | — | Deux nationaux (courbes déjà dessinées) et le bilan. |

## Ch7 — Dipôle RL (`phys_ch7_dipole_RL`)

| Bloc | Diapo retenue | Dessin | Pourquoi / pourquoi pas |
|---|---|---|---|
| rl_s1_b1 | — | — | Carte, prérequis, bobine, lampes : le symbole est dessiné en s1_b3 avec les flèches. |
| rl_s1_b2 | rl_b6_triangle | i(t) en triangle + u_b(t) en créneaux (2 figures) | u_b suit la pente de i : l'image vaut le texte. |
| rl_s1_b3 | rl_b8_reelle | Symbole de la bobine (L, r), i et u_b en convention récepteur | Le fléchage tombe à l'examen. |
| rl_s2_b1 | rl_m1_montage | Schéma RL fléché (E, R, bobine, i, u_R, u_b) | Le montage d'étude. |
| rl_s2_b2 | — | — | Établir l'équation : calcul. |
| rl_s2_b3 | rl_e6_ub | u_R(t) de 0 vers 5 V, u_b(t) de E = 6 V vers r·I₀ = 1 V | Reconnaître les deux courbes (question type 2019 R). |
| rl_s3_b1 | — | — | Trouver la solution : calcul. |
| rl_s3_b2 | rl_s6_pourcent + rl_s7_L | i(t) avec 0,63·I₀ = 63 mA à τ = 2 ms ; L puis 2L (même palier) | Point remarquable, puis influence de L. rl_s8_R : laissé (une figure de plus dépasse l'écran). |
| rl_s3_b3 | rl_t2_descente | Rupture : i(t) de 100 mA, 37 mA à τ, tangente | La seule courbe qui descend. Diode : schéma possible mais secondaire. |
| rl_s4_b1 | rl_l1_tangente | Tangente à l'origine ∩ asymptote i = I₀ | Méthode de lecture de τ. Trouver r, L : calcul. |
| rl_s4_b2 | rl_l5_droite | Droite di/dt = f(i) : E/L, I₀, pente −1/τ | Question des nationaux 2024 N. Énergie : formule. |
| rl_s4_b3 | — | — | Nationaux et bilan. |

## Ch8 — Circuit RLC (`phys_ch8_circuit_RLC`)

| Bloc | Diapo retenue | Dessin | Pourquoi / pourquoi pas |
|---|---|---|---|
| lc_s1_b1 | lc_d2_bobine | Décharge dans R seule (pointillé) et dans la bobine (oscillations) | Le contraste qui fonde le chapitre. |
| lc_s1_b2 | — | — | Courant maximal, signe de i, u_b(0⁺) : raisonnement, déjà sur la courbe d'avant. |
| lc_s1_b3 | lc_r2_aperiodique | Pseudo-périodique (R + r = 20 Ω) et apériodique (1 kΩ) | Reconnaître les régimes : question de chaque sujet. |
| lc_s2_b1 | lc_e1_additivite | Maille C, R, (L, r) fléchée | Base de u_C + u_R + u_b = 0. |
| lc_s2_b2 | lc_e6_sinusoide | u_C = 6·cos(2πt/4) avec U_m et T₀ cotés | Lire U_m (pas 2·U_m) et T₀. |
| lc_s2_b3 | lc_p3_influence | C et 4C : T₀ de 4 ms à 8 ms | L'effet de la racine se voit. |
| lc_s3_b1 | lc_c4_sens | Départ à 3 V qui monte (φ = −π/3) et celle qui descend | Le choix de φ par le sens de départ. |
| lc_s3_b2 | lc_l1_mesure | Pseudo-périodique, cote 3T ≈ 12 ms du 1er au 4e sommet | Méthode de mesure de T. |
| lc_s3_b3 | lc_en3_echange | E_e, E_m et E = 72 µJ (LC idéal) | L'échange d'énergie se dessine. |
| lc_s4_b1 | lc_a4_perdue | E(t) en marches, 72 µJ → 32 µJ, |ΔE| = 40 µJ | L'énergie perdue entre deux sommets (calculée sur la solution exacte). |
| lc_s4_b2 | lc_k3_T0 | Entretenues (k = R + r) et amorties (sans G), T₀ ≈ 4 ms | L'effet de l'entretien. Schéma avec G : non (le format ne dessine pas bien le générateur u_G). |
| lc_s4_b3 | — | — | Nationaux et bilan. |

## Ch9 — Transformations lentes et rapides (`phys_ch9_transformations_lentes_rapides`)

| Bloc | Diapo retenue | Dessin | Pourquoi / pourquoi pas |
|---|---|---|---|
| tl_s1_b1 | tl_x1_zinc | Croquis : bécher bleu, lame de zinc, dépôt de cuivre, 2e⁻ vers Cu²⁺ | L'expérience fondatrice de l'oxydoréduction. |
| tl_s1_b2 | — | — | Demi-équations : écriture, pas de dessin. |
| tl_s1_b3 | — | — | Équations d'oxydoréduction : écriture. |
| tl_s2_b1 | — | — | Rapide / lente : définitions verbales ; aucune courbe n'est encore enseignée à ce point. |
| tl_s2_b2 | tl_r5_echelle | Flèche des durées : rapide (< 1 s), lente, très lente | Frise simple à retenir. |
| tl_s2_b3 | tl_f4_courbes | n(I₂) à 20 °C et 40 °C, même palier 2 mmol | Lecture de courbe des nationaux. |
| tl_s3_b1 | tl_f7_palier | [I⁻]₀ = 0,1 et 0,2 (même palier) ; H₂O₂ doublé (palier 4 mmol) | Le piège du réactif limitant. |
| tl_s3_b2 | tl_t4_courbes | C₁ (catalyseur) et C₂, même x_f = 0,3 mol | Question 2023 N. Trempe : texte. |
| tl_s3_b3 | — | — | 2025 N reprend les mêmes courbes ; bilan. |

Pas de t½ : le temps de demi-réaction n'est pas enseigné dans ce cours (il vient au ch10).

## Dessins faits (34 figures de diapo, 31 blocs illustrés : 8 + 8 + 10 + 5)

- RC : rc_c1_plaques, rc_c5_intensite, rc_g2_pente, rc_m2_acquisition, rc_s6_tableau, rc_d1_decharge, rc_l1_tangente,
  rc_l3_descente, rc_l5_pente.
- RL : rl_b6_triangle (2), rl_b8_reelle, rl_m1_montage, rl_e6_ub, rl_s6_pourcent, rl_s7_L, rl_t2_descente, rl_l1_tangente,
  rl_l5_droite.
- RLC : lc_d2_bobine, lc_r2_aperiodique, lc_e1_additivite, lc_e6_sinusoide, lc_p3_influence, lc_c4_sens, lc_l1_mesure,
  lc_en3_echange, lc_a4_perdue, lc_k3_T0.
- Ch9 : tl_x1_zinc, tl_r5_echelle, tl_f4_courbes, tl_f7_palier, tl_t4_courbes.

## Limite du rendu constatée

Dans `FigureCahier.tsx`, le filtre « craie » (`filter` en `objectBoundingBox`) efface tout trait **parfaitement horizontal
ou vertical** dessiné seul (`ligne` à deux points alignés, `fleche` horizontale ou verticale) : sa boîte englobante a une
hauteur ou une largeur nulle. Contournements utilisés : armatures et fils réunis dans une même polyligne, flèches de
tension courbes (`ligne` lissée avec `fleche`), sens de i en pointe de flèche sur le fil, `repere` (sans filtre) pour les
pointillés. À corriger dans le rendu (par ex. `filterUnits="userSpaceOnUse"`).
