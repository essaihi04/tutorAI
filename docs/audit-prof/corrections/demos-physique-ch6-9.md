## Physique ch6 à ch9 — démonstrations

Règles appliquées : 37 (une étape par ligne, jusqu'au bout), 38 (condition et « car »), 10 (relation → application numérique → résultat avec unité, chaque conversion sur sa ligne). Aucune démonstration ne dépasse 8 lignes. Copies écrites dans `backend/data/courses/en_attente/` (aucune copie en attente n'existait pour ces 4 cours : départ du cours en ligne). Seuls les champs `demonstration` et quelques `bullets` d'exemples travaillés ont changé.

### phys_ch6_dipole_RC
- Relues : 46. Réécrites : 44 (gardées : `rc_s8_quatre q`, `rc_s3_b0 bloc`, déjà complètes).
- Exemples :
  - `rc_s0_b2` : « u_R = R·i | u_R = 100 × 30·10⁻³ | u_R = 3 V » → « Loi d'Ohm : u_R = R·i | i = 30 mA = 30·10⁻³ A | u_R = 100 × 30·10⁻³ | u_R = 3 V ».
  - `rc_l5_pente f1` : se terminait sur une ligne de vérification (« E/(RC) = … = 1000 V/s ») → finit maintenant sur « E = 12 V », avec la raison (du_C/dt = 0 ⇒ régime permanent ⇒ u_C = E).
- Exemples travaillés sur diapo (bullets, voix inchangée) : relation ajoutée devant le calcul sur `rc_t3_C`, `rc_l2_pourcent`, `rc_l3_descente`, `rc_l8_calcul` (E_e = ½ × 220·10⁻⁶ × 12²).
- Douteux : `rc_e8_national e0` / bloc `rc_s2_b3` : Q_max = 12 µC, C = 10 µF ⇒ E = 1,2 V. C'est cohérent avec « correct », mais le sujet 2023 R a q_max = 120 µC (audit du 15 novembre). L'énoncé n'est pas daté, donc pas changé : à vérifier. `rc_s3_b3` : 0,37 × 12 = 4,44 V (« correct »), alors que E·e⁻¹ donne 4,41 V : c'est l'arrondi du cours, ce n'est pas une erreur.

### phys_ch7_dipole_RL
- Relues : 46. Réécrites : 43 (gardées : `rl_rp4_exponentielle f0`, `rl_s0_b1`, `rl_s2_b1`).
- Exemples :
  - `rl_b10_national e0` : « di/dt = 0 | u_b = L·di/dt = 0 | u_b = 0 V | u_b = E − u_R = … = 0 » → « bobine idéale : u_b = L·di/dt | régime permanent, i constante ⇒ di/dt = 0 | u_b = L × 0 | vérification E − R·I₀ = 0 | u_b = 0 V » (la réponse est la dernière ligne).
  - `rl_e8_2019R q` : « U_R = R·E/(R + r) | r = R·(E/U_R − 1) | … » (formule sortie de tête) → « Loi d'Ohm I₀ = U_R/R | I₀ = 0,2 A | E = (R + r)·I₀ ⇒ r = E/I₀ − R | E/I₀ = 50 Ω | r = 50 − 40 | r = 10 Ω ».
- Bullets : relation ajoutée sur `rl_m4_I0`, `rl_s4_A`, `rl_s7_L`, `rl_s8_R`, `rl_l4_L`, `rl_l2_pourcent`, `rl_n2_2024N` (pente puis τ).
- Douteux : aucun calcul faux. Toutes les réponses « correct » ont été vérifiées.

### phys_ch8_circuit_RLC
- Relues : 47. Réécrites : 37 (gardées, déjà complètes : `lc_rp2_bobine q`, `lc_p4_national q`, `lc_c1_depart q`, `lc_l1_mesure q`, `lc_l1_mesure e0`, `lc_n2_2025N q`, `lc_n2_2025N e0`, `lc_a5_courbes f0`, `lc_a5_courbes f1`, `lc_s2_b2a`).
- Exemples :
  - `lc_n2_2025N f0` : 3 lignes, la dérivée et la substitution de i = C₀·du_C/dt faites de tête → 6 lignes : E_T, dE_T/dt, i = C₀·du_C/dt, loi d'additivité, substitution, dE_T/dt = −r·i².
  - `lc_a4_perdue e0` : « ½ × 2,2·10⁻¹⁰ × (6² − 4,4²) ≈ 1,83·10⁻⁹ J » → conversion 0,22 nF = 2,2·10⁻¹⁰ F, puis 36 − 19,36 = 16,64 sur sa ligne, puis le produit et le résultat.
- Bullets : relation ajoutée sur `lc_l3_carre` (C = T₀²/(4π²·L)) et `lc_en2_depart` (E = ½·C·E²).
- Douteux : aucun calcul faux (T₀ = 2π√(0,1 × 4·10⁻⁶) = 3,97 ms ≈ 4 ms, comme dans le cours avec π² = 10).

### phys_ch9_transformations_lentes_rapides
- Relues : 17. Réécrites : 4 (`tl_f7_palier f0` et bloc `tl_s3_b1`, `tl_n1_lecture f0` et bloc `tl_s3_b3`). Les demi-équations et les équations bilans étaient déjà faites pas à pas.
- Exemples :
  - `tl_f7_palier f0` : « n(I₂) au palier = n(H₂O₂)₀ » sans raison → « I⁻ en excès : H₂O₂ est le réactif limitant | le réactif limitant fixe le palier : n(I₂) = n(H₂O₂)₀ | n(H₂O₂)₀ = 4 mmol | n(I₂) au palier = 4 mmol ».
  - `tl_n1_lecture f0` : on ajoute les deux facteurs (température basse ⇒ plus lent ; le catalyseur accélère) avant la conclusion « (c) ↔ expérience 1 ».
- Douteux : aucun.

### Pistes voix à enregistrer (démonstrations réécrites qui avaient un audio, retiré)
- ch6 (14) : rc_rp4_additivite__demo_q, rc_c6_relation__demo_q, rc_a1_parallele__demo_q, rc_e8_national__demo_q, rc_e8_national__demo_e0, rc_s4_condition__demo_q, rc_s4_condition__demo_e0, rc_t3_C__demo_q, rc_d2_continuite__demo_q, rc_l3_descente__demo_q, rc_l3_descente__demo_e0, rc_l7_energie__demo_q, rc_n1_2019__demo_q, rc_n1_2019__demo_e0.
- ch7 (15) : rl_rp2_additivite__demo_q, rl_b3_egal__demo_q, rl_b10_national__demo_q, rl_b10_national__demo_e0, rl_e8_2019R__demo_q, rl_s1_forme__demo_q, rl_s5_dimension__demo_q, rl_t4_national__demo_q, rl_t4_national__demo_e0, rl_l4_L__demo_q, rl_l4_L__demo_e0, rl_l8_double__demo_q, rl_l8_double__demo_e0, rl_n2_2024N__demo_q, rl_n2_2024N__demo_e0.
- ch8 (10) : lc_d6_depart__demo_q, lc_d6_depart__demo_e0, lc_r4_national__demo_q, lc_e5_lc_ideal__demo_q, lc_p4_national__demo_e0, lc_en3_echange__demo_q, lc_a4_perdue__demo_q, lc_a4_perdue__demo_e0, lc_k3_T0__demo_q, lc_k3_T0__demo_e0.
- ch9 : aucune. Ses 4 démonstrations réécrites (comme les 85 autres de `exercices_fin_de_cours` et des blocs en ch6 à ch8) n'avaient jamais eu d'audio : elles seront voisées à l'étape de fin de cours.

### Vérifications faites
- `json.load` sur les 4 copies : OK. Fichiers en LF, `ensure_ascii=False`, `indent=2`.
- Pour chaque démonstration, chaque `mot` est un extrait exact de sa `parole`, et chaque `mot` de pointage ou du centre est dans `speech_text.mixed` : 0 erreur.
- Chaque diapo est dans un seul bloc, et chaque `competence_id` existe : 0 erreur.
- `verifier_figures_cahier.py` : 0 erreur, 0 avertissement sur les 4 copies.
- Comparaison avec le cours en ligne : à part les `demonstration` et les `bullets` cités, rien n'a changé. Aucune démonstration réécrite ne garde son `audio`.
- Paroles : aucun chiffre, aucun symbole, pas de tachkil (contrôle automatique). Unités et nombres dits en mots.
- Calculs refaits en Python (42 résultats) : tous égaux à la réponse « correct ».
- Remarque : `en_attente/phys_ch6_dipole_RC.json` a été commité par un autre processus (commit « wip(physique en attente)… », 394c1782) juste après mon écriture. Son contenu est identique au mien. Je n'ai rien commité.
