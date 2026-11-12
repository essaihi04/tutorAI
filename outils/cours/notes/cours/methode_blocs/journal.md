# Méthode des blocs — journal (11 novembre 2026)

Outil : `blocs.py` (base / apercu / appliquer / verifier / items) dans ce dossier.
- `base/<deck>.json` : photo des textes protégés prise AVANT toute modification (les 10 cours). Ne pas la refaire.
- `sauvegarde/<deck>.json.gz` : copie des cours avant modification (fichiers non suivis par git !). phys_ch1 : pas de copie (déjà modifié, ajouts seulement).
- `ajouts/<deck>.json` : ce qu'on ajoute (séances, rappels, prédictions, énoncés réécrits) ; `appliquer` relit le cours et n'écrit que ça.
- `<deck>_items.json` : réactions à écrire (rappels QCM/VF + exercices de blocs non repris) ; `<deck>_demos.json` : démonstrations nouvelles à dire.
- `seances` est posé à la racine du cours (là où sont `competences`) ; vrai/faux de rappel : `correct` booléen ; exercice repris : `reprend: "<slide>/e<i>"`.

## phys_ch1_waves_exemple — FAIT
2 séances (3 + 2 blocs : 16 diapositives ne permettent pas 6 blocs de 3), 5 blocs, 28 rappels (9 compétences), 6 prédictions / 16.
verifier : blocs OK, cadre OK. Items : 87 réactions, 2 démonstrations.

## phys_ch2_ondes_periodiques — FAIT
5 séances × 3 blocs = 15 blocs (13 de 3 diapositives, 2 de 4 : op_s3_b1 célérité, op_s3_b2 phase), 47 diapositives. Bilan et carte dans le dernier bloc (op_s5_b3, avec le cas type op_x3_devoir : la partie bilan n'a que 2 diapositives).
Coupes hors limites de parties : op_s1_b2 (o4, o5 + t1), op_s2_b1 (t5–t7), op_s5_b2 (r4 + x1, x2), op_s5_b3 (x3 + bilan).
31 rappels (C1–C9, 3 ou 4 chacun, libre + qcm + vrai_faux). 16 prédictions / 47 (au moins une par partie).
1 énoncé réécrit : op_x1_national_2017 « Avant de calculer, prévois l'ordre de grandeur : … » (aucune question de la partie IX ne se prête à une prédiction).
Exercices : 6 repris (t6/e0, p3/e0, m4/e0, r3/e0, x1/e0, x3/e0 — prompt rendu autonome, options/bonne réponse/explication copiées), 9 écrits dont 5 avec démonstration.
Items : 132 réactions, 5 démonstrations nouvelles. verifier : blocs OK, cadre OK (75 « à relire », 72 avant : les 3 de plus sont des lignes de cahier des diapositives reprises telles quelles : t = n·T, SM = k·λ, t = d / v).
À valider : la réécriture de l'énoncé op_x1 ; les prompts autonomes des exercices repris.

## svt_ch3_notion_information_genetique — FAIT
5 séances (3+3+3+3+2 blocs, 14 blocs : 47 diapositives, 9 blocs de 3 et 5 de 4 ; la dernière séance a 2 blocs). Voix par séance 3,0 à 5,3 min.
Coupes aux limites des parties, sauf ig_s1_nucleotide rattachée au bloc de la transformation bactérienne (ig_s3_b2) : la partie VI (5 diapositives) ne se coupe pas en 3/4.
29 rappels (8 compétences, 3 à 4 chacune, libre + QCM + vrai/faux). 18 prédictions / 47 (au moins une par partie).
1 énoncé réécrit : ig_x2_exercice (« Prévois avant la correction : … ») — partie VIII sans question de prédiction ; options et bonne réponse inchangées.
Exercices : 1 repris (ig_x1_restitution/e2, vrai/faux) ; 13 nouveaux (7 QCM, 6 libres avec démonstration : Gurdon inversé, durée de S, télophase végétale, brin complémentaire, Meselson G3, brin nouveau ; séquences vérifiées en python).
Items : 109 réactions, 6 démonstrations nouvelles (svt_ch3_notion_information_genetique_items.json / _demos.json).
verifier : cadre OK (2 points à relire déjà présents avant : « A = T : 2 liaisons hydrogène » et la lecture « A sur T égale un » de ig_s2_chargaff), blocs OK ; avis : séance ig_s5 à 2 blocs, énoncé réécrit.
À valider : l'énoncé réécrit de ig_x2_exercice ; l'exercice Gurdon inversé (ovule albinos, noyau de têtard pigmenté).

## math_ch3_suites_numeriques — FAIT
6 séances (3+3+3+3+3+2 blocs : 59 diapositives = 17 blocs de 3 ou 4, la dernière séance a 2 blocs), 17 blocs, 28 rappels (8 compétences K1–K8), 23 prédictions / 59, 0 énoncé réécrit.
Exercices repris : su_a1_liste/e0, su_r2_trois_titres/e0 (vrai/faux), su_m1_pour_tout_n/e0, su_c2_couple/e0, su_e1_complet/e0 ; 12 exercices nouveaux, tous de calcul avec démonstration (nombres vérifiés avec python).
Items : 97 réactions, 12 démonstrations. verifier : blocs OK, cadre OK (101 points à relire, aucun bloquant).
Coupe à valider : su_l1_converge (début de la partie V) est dans le bloc su_s3_b3 avec x4/x5 (la partie IV a 5 diapositives).
Outil : blocs.py prenait « La carte du chapitre : une liste de nombres… » (diapositive d'OUVERTURE su_o1_questions) pour la carte de fin ; le motif est maintenant « carte du chapitre » en fin de titre seulement (même cas : lc_o1_carte, df_c1_carte).

## math_ch2_derivation_etude_fonctions — FAIT
7 séances (6 × 3 blocs + 1 de 2 blocs), 20 blocs (16 de 3 diapositives, 4 de 4), coupés aux limites des parties ; 64 diapositives, voix 4,3 à 6,6 min par séance. La dernière séance a 2 blocs : 64 diapositives en blocs de 3-4 sans couper une partie donnent 20 blocs ; le bilan et la carte sont dans le dernier bloc avec df_ec4_unique.
Rappels : 39 (K5 : 3, les autres : 4), trois formes, bonne réponse des QCM à des rangs variés. Prédictions : 28 / 64, au moins une par partie. Énoncés réécrits : aucun.
Exercices : 13 repris (reprend), 7 nouveaux avec démonstration (point anguleux par morceaux, minimum de x + 9/x, asymptotes de (2x + 1)/(x − 1), asymptote oblique donnée, deux points d'une tangente, (f⁻¹)'(3) pour x³ + 2x, solution unique de x³ + x − 1 = 0) ; calculs vérifiés avec sympy.
Items : 135 réactions à écrire, 7 démonstrations nouvelles (math_ch2_derivation_etude_fonctions_items.json / _demos.json).
verifier : blocs OK, cadre OK (199 « à relire » non bloquants, surtout des limites écrites « = +∞ » déjà présentes dans le cours) ; avis : séance df_s7 à 2 blocs.
À valider : (1) 7 séances pour ce chapitre (plus que 4-5 : 64 diapositives) ; (2) retrouver sans formule du cadre pour K9 (ordre du tracé, lecture f(x) = m, ordre d'un problème) et K2 demi-tangente verticale : texte du cahier ; (3) dernier bloc : retrouver = théorème de la solution unique (chapitre continuité), repris de df_ec4_unique.

## svt_ch4_relation_gene_proteine — FAIT
5 séances (3+3+3+3+2 blocs, 14 blocs : 47 diapositives, 9 blocs de 3 et 5 de 4 ; la dernière séance a 2 blocs). Voix par séance 4,2 à 7,2 min (séance 1 : trois blocs de 4).
Coupes aux limites des parties, sauf : rg_r1_acteurs avec la fin du code génétique (rg_s3_b1), pour garder initiation-élongation-terminaison-polysome ensemble ; rg_e1_restitution avec la fin de la partie VIII (rg_s4_b3, « transcription ou traduction ? », restitution).
29 rappels (8 compétences, 3 à 4 chacune, libre + QCM + vrai/faux). 18 prédictions / 47 (au moins une par partie ; partie IX : rg_e6_drepanocytose). Aucun énoncé réécrit.
Exercices : 1 repris (rg_e1_restitution/e0, vrai/faux) ; 13 nouveaux (8 QCM, 5 libres avec démonstration : ARNm depuis le brin transcrit, depuis le brin non transcrit, traduction, délétion et décalage, origine génétique d'une mutation non-sens ; tout vérifié en python avec le code génétique).
Items : 114 réactions, 5 démonstrations nouvelles (svt_ch4_relation_gene_proteine_items.json / _demos.json).
verifier : cadre OK (0 point à relire), blocs OK ; avis : séance rg_s5 à 2 blocs.
À valider : séance 1 un peu longue (7,2 min de voix) ; noms d'acides aminés dits dans les démonstrations (alanine, glycine, lysine, leucine, asparagine, cystéine) : à écouter.

## phys_ch3_ondes_lumineuses — FAIT
5 séances × 3 blocs = 15 blocs (7 de 3, 8 de 4), 53 diapositives. Bilan et carte dans le dernier bloc (ol_s5_b3, avec ol_q4_deviation).
Coupes hors limites de parties : ol_s2_b3 (l9 + c1, c2), ol_s3_b1 (c3–c5 + g1), ol_s4_b2 (n4, n5 + p1), ol_s5_b3 (q4 + bilan). Le prisme (« pour le devoir ») est coupé entre ol_s5_b2 et ol_s5_b3.
30 rappels (C1–C9, 3 ou 4 chacun, libre + qcm + vrai_faux). 19 prédictions / 53 (au moins une par partie).
2 énoncés réécrits : ol_x2_national_2023 et ol_q2_premiere_face (« Avant de calculer, prévois… ») : aucune question des parties IX et X ne se prête à une prédiction.
Exercices : 5 repris (l1/e0, l9/e0 vrai/faux, r4/e0 vrai/faux, x2/e1, q3/e0), 10 écrits dont 5 avec démonstration.
Items : 137 réactions, 5 démonstrations nouvelles. verifier : blocs OK, cadre OK (49 « à relire », comme avant).
À valider : les 2 énoncés réécrits ; la fin du prisme (q4) placée avec le bilan.

## svt_ch1_reactions_responsables_liberation_energie — FAIT
4 séances × 3 blocs (12 blocs, 43 diapositives : 7 blocs de 4 et 5 de 3), 34 rappels (10 compétences), 15 prédictions / 43, 1 énoncé réécrit (le_x3_chaine_en_panne, en prédiction : sans lui, la partie IX n'en avait aucune).
Items : 118 réactions, 3 démonstrations nouvelles (NADH,H+ par glucose dans la matrice, accumulation de NADH,H+ sans O2, rendement de la fermentation lactique).
Exercices repris : le_e2_decrire/e0, le_g3_bilan/e0, le_f2_alcoolique/e0, le_x2_qui_respire/e0 (avec sa démonstration). Celui de le_m2_legender (association) n'est pas repris : `verifier` n'accepte pas ce type.
verifier : cadre OK (1 point à relire, déjà présent dans la question de le_r2_rendement : « … = ? »), blocs OK.
blocs.py (choix (a) du coordinateur) : la règle « dernière séance » ne regarde plus que `concentration.acquis`, et plus le titre. le_e4_carte (« La carte du chapitre », carte d'aperçu de la partie II) reste à sa place, dans le bloc le_s1_b3.
Décisions à faire valider : deux coupes entre parties, le_e4_carte avec les transporteurs (le_s1_b3) et le_k5_fois_deux avec la chaîne respiratoire (le_s3_b1), pour avoir 12 blocs de 3 ou 4 ; la séance 4 dure 7,8 min de voix.

## svt_ch2_role_muscle_strie_squelettique — FAIT
5 séances × 3 blocs (15 blocs, 53 diapositives : 8 blocs de 4 et 7 de 3), toutes les coupes aux limites des parties ou à l'intérieur d'une partie. 31 rappels (9 compétences), 18 prédictions / 53, aucun énoncé réécrit.
Items : 140 réactions, 4 démonstrations nouvelles (durées de la secousse, demi-bande claire, muscle raide sans ATP, durée de la réserve d'ATP).
Exercice repris : ms_x4_restitution/e3 (vrai/faux).
verifier : cadre OK (0 point à relire), blocs OK. Deux avis : aucune prédiction dans la partie II (seuil : les deux questions sont des lectures de tracé) ni dans la partie IX (méthodes de rédaction). Je n'ai pas réécrit d'énoncé, car aucune question ne se prête honnêtement à une prédiction.
Décision à faire valider : faut-il quand même une prédiction dans la partie II ? Ce serait possible en réécrivant l'énoncé de ms_i1_seuil.

## math_ch1_limites_continuite — FAIT
7 séances × 3 blocs (21 blocs, 68 diapositives : 5 blocs de 4 et 16 de 3), 32 rappels (10 compétences K1–K10), 29 prédictions / 68 (au moins une par partie, ouverture comprise), 0 énoncé réécrit.
Exercices repris : lc_l1_chemin/e0, lc_l4_formes/e0 (V/F), lc_l5_facteur/e0, lc_l8_racine_infini/e0 (V/F), lc_l13_devoir/e0, lc_c5_redaction/e0, lc_j4_borne_ouverte/e0, lc_t4_au_moins_une/e0 (V/F), lc_d4_recommencer/e0, lc_r1_aller_retour/e0, lc_lr3_zero_sur_zero/e0, lc_e1_probleme/e0 ; 9 exercices nouveaux (8 avec démonstration, le QCM du miroir sans calcul). Nombres vérifiés avec python (sympy).
Items : 115 réactions, 8 démonstrations. verifier : blocs OK, cadre OK (251 points à relire, aucun bloquant).
Coupes à valider (parties de 5 ou 9 diapositives) : lc_i1_usuelles avec c4/c5 ; lc_t1/t2 (début du TVI) avec j4/j5 ; lc_r5/r6/r7 ensemble puis r8/r9 avec lc_n1_defaire.
Note suites : ma retouche du motif « carte du chapitre » dans blocs.py a été remplacée par l'agent principal (seul `acquis: true` compte) ; les deux cours passent avec la version actuelle.

## Bilan (agent principal) — TOUT FAIT
Les 10 cours repassés par verifier : blocs OK et cadre OK partout. Au total : 311 rappels, 190 prédictions, 1 184 réactions à écrire (items), 57 démonstrations nouvelles à dire. Aucun autre cours *_chN_* apparu.
Reste : écrire les réactions sur le VPS (gen_reponses_vps.py, crédit DeepSeek), adapter poser/audio aux cibles rappel_/bloc_, voix des démonstrations, lecteur (seances, rappels, prediction).

## phys_ch5_energie_nucleaire — FAIT
4 séances (3 + 3 + 3 + 2 blocs ; 11 blocs de 3-4 diapositives, la dernière séance a 2 blocs car 38 diapositives), 31 rappels
(3-4 par compétence C1-C9, formes libre/qcm/vrai_faux), 13 prédictions / 38, 2 énoncés réécrits (en_b4_fission_calcul,
en_c1_cas_types). Exercices de blocs : 8 repris des diapositives, 3 écrits (dont 1 avec démonstration). Items : 230 (cours,
energie_nucleaire_build/items_cours.json) + 112 (blocs, items_blocs.json) + 1 démonstration (demos_blocs.json), à faire écrire.
verifier : « cadre : OK », « blocs : OK ». Les seances/rappels/prédictions sont aussi gardés par build.py --garder-reponses.

## phys_ch4_radioactivite — FAIT (routine cloud, 12 novembre 2026)
5 séances (3 + 3 + 3 + 3 + 2 blocs ; 14 blocs de 3-4 diapositives ; la dernière séance a 2 blocs de 3 : cas types 2021 N/2022 N,
puis 2025 N + bilan + carte), 29 rappels (3-4 par compétence C1-C9, formes libre/qcm/vrai_faux), 20 prédictions / 52, aucun
énoncé réécrit (les prédictions sont posées directement dans p*.py et dans ajouts). Exercices de blocs : 2 repris (ra_x2_2021N/e0,
ra_x4_2025N/e0), 12 écrits (9 avec démonstration). Items : 275 (cours, radioactivite_build/items_cours.json) + 142 (blocs,
items_blocs.json) + 9 démonstrations (demos_blocs.json), à faire écrire sur le serveur. verifier : « cadre : OK », « blocs : OK ».
Le cours étant neuf, la photo base/ a été prise après la dernière retouche de la darija (aucune voix encore).
