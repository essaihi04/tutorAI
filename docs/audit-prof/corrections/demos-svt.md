## SVT ch1 à ch4 — démonstrations

Copies écrites (aucune copie en attente n'existait, parti du cours en ligne) : `backend/data/courses/en_attente/<deck>.json` pour les 4 cours. Seuls changent : `demonstration` (lignes + parole, audio retiré) et 5 `concentration.centre` d'exemples travaillés (lignes découpées, mots pris dans la voix existante : voix de diapo inchangée, audio de diapo gardé).

### ch1 — réactions de libération d'énergie
- Relues 9, réécrites 6 (+ centre de 3 diapos : le_r1_compteur, le_r2_rendement, le_r3_comparer). Gardées : le_t2_reduit (FAD réduit), le_c10b_vesicules_cas (pH égaux, pas de gradient), le_s3_b3 (O2 accepteur final).
- Ex. : rendement le_r2 « r = (38 × 30,5)/2860 × 100 → r = 40,5 % » → données / relation / substitution / 38 × 30,5 = 1159 kJ / r = 1159/2860 × 100 / ≈ 0,405 / r = 40,5 % (même plan pour la fermentation, 2,13 %).
- Ex. : A/B « B : acide lactique élevé → fermentation » (sans conclusion) → valeurs O2 (3,5 / 2,0 L/min) et acide lactique (2 / 9 mmol/L) comparées, raison (la respiration utilise O2 dans les mitochondries ; la fermentation produit l'acide lactique), phrase de conclusion = réponse « correct ».
### ch2 — muscle strié squelettique
- Relues 6, réécrites 3. Gardées : ms_r8_inhibiteurs (glycolyse bloquée voie alactique), ms_s4_b3 (rigidité cadavérique), ms_s4_b4 (2,5 s).
- Ex. : myogramme « 0,05 − 0,01 = 0,04 s » → bornes lues, t_c = 0,05 − 0,01, t_c = 0,04 s ; idem relâchement (0,06 s).
- Ex. : demi-bande claire « 2,4 = 1,6 + 2 × d → d = 0,4 µm » → 2 × d = 2,4 − 1,6 / 2 × d = 0,8 µm / d = 0,8/2 / d = 0,4 µm.
### ch3 — notion d'information génétique
- Relues 12, réécrites 9 (+ centre ig_c6_durees). Gardées : ig_n3_chromatides, ig_r3_g1 (conservative G1 2 bandes), ig_s3_b2 (télophase).
- Ex. : brin complémentaire « T → A ; A → T… → 3' AATCG 5' » → règle, base par base, « les deux brins sont antiparallèles : en face de 5' il y a 3' », résultat (idem 5' GATTCA 3' et brin ancien 3' TACGGA 5').
- Ex. : Meselson 3 générations → réplication semi-conservative nommée, 2 × 2 × 2 = 8, 2 hybrides, 8 − 2 = 6 légères, conclusion.
### ch4 — relation gène–protéine
- Relues 8, réécrites 6 (+ centre rg_c1_codon : 4 < 20, 4 × 4 = 16 < 20, 4 × 4 × 4 = 64 ≥ 20). Gardées : rg_p4_document (LDL), rg_s3_b3 (traduction Met – Ala – Gly – Lys).
- Ex. : délétion « ARNm muté : AUG CUG AAU CA… » → ARNm normal / C supprimé (AUG CU GAA UCA) / relecture par 3 / code / séquence / décalage du cadre de lecture.
- Ex. : drépanocytose → CTC → CAC (substitution T par A) / GAG / GUG / code : Glu, Val / hémoglobine S / faucille → drépanocytose.

### Démonstrations douteuses
Aucun calcul faux ni « correct » faux trouvé (tout recalculé en python : 1159 kJ, 40,5 %, 61 kJ, 2,13 %, 0,04 s, 0,06 s, 0,4 µm, 20 h, 6 h, 4 chromatides, 8/2/6 molécules, compléments et ARNm, AUG CUG AAU). À signaler, non modifié :
- ch2 rappel « La voie aérobie produit 36 ATP » alors que ch1 compte 38 (36 « si l'énoncé le dit ») : vérifier la cohérence.
- Questions de calcul/justification SANS démonstration (non créées, hors tâche) : ch2 ms_s2_b3 (dosages), ms_s3_b3 (sarcomère 2,6 → 2,2 µm) ; ch3 ig_s2_b1 (2n = 46 en G2), ig_s2_b2 (6 UA → G2), ig_s4_b3 (30 % de A) ; ch4 rg_s3_b2 (AUG GCA UAG CCU), rg_s6_b1 (GGA → GGT, Pro).
- ig_r3_g1 : d(hybride) = (1,710 + 1,724)/2 = 1,717 sans la ligne 3,434/2 (la voix ne la dit pas : laissé).

### Pistes voix à enregistrer (demonstration.parole)
ch1 : le_g3_bilan (question), le_r2_rendement (question), le_x2_qui_respire (exercises[0]), blocs le_s3_b1, le_s5_b1, le_s5_b2.
ch2 : ms_t4_consomme (question), blocs ms_s1_b2, ms_s3_b2.
ch3 : ig_c6_durees, ig_m7_schema, ig_s5_complementaire, ig_x2_exercice (questions), blocs ig_s1_b2, ig_s2_b3, ig_s5_b1, ig_s5_b3, ig_s6_b2.
ch4 : rg_t6_bareme, rg_e6_drepanocytose (questions), blocs rg_s2_b3, rg_s3_b1, rg_s4_b3, rg_s5_b3.
(Aucune voix de diapo modifiée.)

### Vérifications faites
- json.load des 4 copies : OK ; LF, ensure_ascii=False, indent=2 (diff = seulement les changements).
- Chaque `mot` de demonstration.lignes est dans sa parole, dans l'ordre ; chaque `mot` de pointage/centre est dans speech_text.mixed : 0 erreur.
- Chaque diapo dans exactement un bloc, chaque competence_id existe : 0 erreur.
- Paroles nouvelles : aucun chiffre ni symbole (+, =, %, →, ×, /).
- verifier_figures_cahier.py (ch1) : 0 erreur. Notions utilisées déjà enseignées (antiparallèles, semi-conservative, non-sens, cadre de lecture : avant les blocs concernés).
