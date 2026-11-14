# Audit des dessins du cahier — SVT (14 novembre 2026)

Fichiers : `backend/data/courses/svt_ch1…ch4_*.json` (pas les `*_course_v1.json`). Un dessin au plus par bloc ; la
figure de la diapo est reprise telle quelle dans `blocs[].cahier_figures`. Valeurs prises dans le `cahier`, le
`screen_content` et les modèles des simulations du cours (`frontend/public/media/simulations/svt/...`).
Vérification : `verifier_figures_cahier.py` → 0 erreur, 0 avertissement ; aucun texte ne se chevauche ni ne sort du
dessin (boîtes des textes mesurées dans le rendu réel `FigureCahier`).

## Ch. 1 — Libération de l'énergie (`svt_ch1_reactions_responsables_liberation_energie`)

| Bloc | Diapo dessinée | Dessin | Pourquoi / pourquoi pas |
|---|---|---|---|
| le_s1_b1 | le_a2_recharge | Cycle ATP ⇄ ADP + Pi (hydrolyse / phosphorylation) | retenir les deux sens et d'où vient l'énergie ; o1, o2, a1 : verbal |
| le_s1_b2 | le_e3_sans_o2 | Courbe [O₂] (mg/L) – t (min) des levures : 7,5 → baisse après glucose → 0 ; zones respiration / fermentation | courbe ExAO type examen (e1, e2 préparent la lecture) |
| le_s1_b3 | — | — | carte du chapitre, transporteurs : équations, verbal |
| le_s2_b1 | — | — | glycolyse : une équation-bilan, le texte suffit |
| le_s2_b2 | le_m2_legender | Mitochondrie en coupe, 6 légendes | schéma à légender à l'examen ; m4 (deux courbes O₂/ATP à deux échelles) écarté : un dessin par bloc |
| le_s2_b3 | le_k4_sorties | Roue de Krebs : acétyl-CoA entre, 2 CO₂, 3 NADH,H⁺, 1 FADH₂, 1 ATP sortent | « on retient ce qui sort » : se mémorise en image |
| le_s3_b1 | le_c1_pulse | Courbe [H⁺] (×10⁻⁹ mol/L) – t (s) : 20 → pic 44 à 75 s → 20 vers 300 s | document du national, réutilisé en c6/c7 |
| le_s3_b2 | le_c6_protons | Membrane interne, T1…T4, trajet des e⁻ jusqu'à O₂, pompage des H⁺ | sens des protons : erreur fréquente aux QCM |
| le_s3_b3 | le_c7_sphere | Sphère pédonculée : retour des H⁺, ADP + Pi → ATP | suite logique de c6 ; c8–c10 : méthode, verbal |
| le_s4_b1 | — | — | équations et calcul des 38 ATP |
| le_s4_b2 | le_r3_comparer | Barres de rendement : 40,5 % (38 ATP) / 2,13 % (2 ATP) | comparer deux valeurs d'un coup d'œil |
| le_s4_b3 | — | — | méthode, synthèse et bilan : pas de dessin |

## Ch. 2 — Rôle du muscle strié squelettique (`svt_ch2_role_muscle_strie_squelettique`)

| Bloc | Diapo dessinée | Dessin | Pourquoi / pourquoi pas |
|---|---|---|---|
| ms_s1_b1 | — | — | myographe : vocabulaire ; la secousse est dessinée au bloc suivant avec ses valeurs |
| ms_s1_b2 | ms_s5_mesures | Myogramme d'une secousse : latence 0,01 s, contraction 0,04 s, relâchement 0,05 s, 20 mm | tracé n° 1 de l'examen |
| ms_s1_b3 | ms_i2_recrutement | Amplitude (mm) – intensité (mV) : seuil 4 mV, maximum à 9 mV (20 mm) | seuil + recrutement en une courbe |
| ms_s2_b1 | ms_f2_fusion_incomplete | Fusion incomplète : sommets 20 puis 31 mm, E2 à 0,07 s | reconnaître le tracé |
| ms_s2_b2 | ms_f5_tetanos_parfait | Tétanos imparfait (15 exc./s, dentelé) et parfait (40 exc./s, lisse ≈ 60 mm) | comparer les deux plateaux ; f6 méthode, f7 fatigue (verbal) |
| ms_s2_b3 | ms_t2_chaleur_retardee | Chaleur initiale (pic bref) et retardée (bosse basse, ~2 min) | document classique |
| ms_s3_b1 | — | — | hiérarchie muscle → fibre : verbal ; le sarcomère est dessiné au bloc suivant |
| ms_s3_b2 | ms_u5_bandes | Sarcomère : stries Z, actine, myosine, bandes A, ½ I, zone H | structure à légender |
| ms_s3_b3 | ms_g2_mesures | Sarcomère relâché (2,5 µm) et contracté (2,0 µm), bande A constante | ce qui raccourcit / ne change pas |
| ms_s4_b1 | ms_c4_rotation | Tête de myosine : ATP → ADP + Pi, rotation, glissement de l'actine | mécanisme en une image |
| ms_s4_b2 | — | — | liste d'étapes, conversion d'énergie : verbal |
| ms_s4_b3 | — | — | équations (phosphocréatine, fermentation) |
| ms_s5_b1 | ms_r6_relais | Parts des trois voies (%) selon la durée de l'effort (s) | relais sans frontière nette ; r7 est un tableau |
| ms_s5_b2, ms_s5_b3 | — | — | méthode de rédaction, restitution, bilan |

## Ch. 3 — Information génétique (`svt_ch3_notion_information_genetique`)

| Bloc | Diapo dessinée | Dessin | Pourquoi / pourquoi pas |
|---|---|---|---|
| ig_s1_b1, ig_s1_b2 | — | — | expériences (amibe, acétabulaire, Gurdon) : raisonnement verbal ; croquis trop chargés |
| ig_s1_b3 | ig_n3_chromatides | Chromosome à 1 chromatide → (phase S) → 2 chromatides + centromère | 1 chromatide = 1 ADN |
| ig_s2_b1 | ig_c3_courbe | Quantité d'ADN (UA) – t (h) : q, 2q ; G1, S (8–14 h), G2, M (19–20 h) | courbe en marches de l'examen |
| ig_s2_b2 | — | — | lecture de la même courbe, calcul de durées |
| ig_s2_b3 | — | — | phases de la mitose : voir ci-dessous (anaphase non faite) |
| ig_s3_b1 | — | — | anaphase 2n = 4 envisagée sur ig_m7_schema, écartée : 8 chromatides + fuseau + légendes ≈ 20 éléments |
| ig_s3_b2 | ig_s1_nucleotide | Nucléotide : phosphate – désoxyribose – base | structure à savoir |
| ig_s3_b3 | ig_s5_complementaire | Deux brins 5'→3' / 3'→5' : ATCGGA en face de TAGCCT | complémentarité + antiparallélisme |
| ig_s4_b1 | — | — | hypothèses ; les bandes sont dessinées au bloc suivant (G0, G1, G2 ensemble) |
| ig_s4_b2 | ig_r4_g2 | Tubes G0 / G1 / G2 : lourde 1,724, hybride 1,717, légère 1,710 | résultat de Meselson et Stahl |
| ig_s4_b3 | ig_r9_yeux | Œil de réplication : brins anciens, brins nouveaux, deux fourches | réplication semi-conservative vue en image |
| ig_s5_b1, ig_s5_b2 | — | — | conservation (verbal), examen, bilan |

## Ch. 4 — Relation gène – protéine (`svt_ch4_relation_gene_proteine`)

| Bloc | Diapo dessinée | Dessin | Pourquoi / pourquoi pas |
|---|---|---|---|
| rg_s1_b1 | rg_g2_allele | Paire de chromosomes : même locus, allèles A et O | gène / locus / allèle |
| rg_s1_b2, rg_s1_b3 | — | — | drépanocytose (échelles, verbal) ; ARN : le schéma noyau → cytoplasme vient au s4_b2 |
| rg_s2_b1 | — | — | règle de complémentarité : texte |
| rg_s2_b2 | rg_t4_sens | Transcription : brin transcrit 3' TAC GCG TCA 5', ARNm 5' AUG CGC AGU 3' | sens de lecture / de synthèse |
| rg_s2_b3, rg_s3_b1 | — | — | code génétique : tableau, méthode |
| rg_s3_b2 | rg_r3_elongation | Ribosome sur l'ARNm, ARNt (GCG) apportant Arg, Met – Arg, avance vers 3' | élongation |
| rg_s3_b3, rg_s4_b1 | — | — | mutations : séquences écrites, pas de dessin |
| rg_s4_b2 | rg_s3_construire | Noyau (gène, transcription, ARNm), pore, cytoplasme (ribosome : traduction, protéine) | schéma à construire au bac |
| rg_s4_b3, rg_s5_* | — | — | restitution, exercice national, bilan |

## Dessins faits (27 diapos, 27 blocs)

- Ch. 1 (8) : le_a2_recharge, le_e3_sans_o2, le_m2_legender, le_k4_sorties, le_c1_pulse, le_c6_protons, le_c7_sphere, le_r3_comparer.
- Ch. 2 (9) : ms_s5_mesures, ms_i2_recrutement, ms_f2_fusion_incomplete, ms_f5_tetanos_parfait, ms_t2_chaleur_retardee, ms_u5_bandes, ms_g2_mesures, ms_c4_rotation, ms_r6_relais.
- Ch. 3 (6) : ig_n3_chromatides, ig_c3_courbe, ig_s1_nucleotide, ig_s5_complementaire, ig_r4_g2, ig_r9_yeux.
- Ch. 4 (4) : rg_g2_allele, rg_t4_sens, rg_r3_elongation, rg_s3_construire.

## Limites et doutes

- Pas d'élément « groupe » ni de chemin à plusieurs morceaux : l'anaphase (2n = 4) demanderait ~20 éléments ; non faite.
- Pas de double axe y : la courbe O₂ / ATP des mitochondries isolées (le_m4) n'est pas dessinée.
- Chaleur (ms_t2) : le pic initial (0,1 s) est élargi pour être visible sur un axe en minutes (allure, pas d'échelle).
- Relais des voies (ms_r6) : parts « en % » reprises du modèle de la simulation (allures, pas des mesures).
- Courbe d'ADN (ig_c3) : heures prises dans le document de ig_c5 (cycle de 20 h).
