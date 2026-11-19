# Audit national — Physique ch1 à ch8

Demandes de l'utilisateur du 18/11/2026, précisées le 19/11 : (1) compter en allumant chaque élément tour à tour ; (2) un exercice du national
commence par son **énoncé reproduit en code comme la vraie feuille d'examen** (fond blanc, en-tête officiel, barème à droite, figures
redessinées ; gabarit commun `frontend/public/media/simulations/shared/examen/feuille.html?sujet=physique/<année>-<session>&exercice=<n>`,
texte et points pris dans `exam.json`, scans `pages/` seulement comme modèle), lu par le tuteur ; (3) la démonstration se joue sur la figure
(lignes `allume`, contrat du lecteur).

Règles : skill `simulations-au-tableau` 16-17, `professeur` 44-46, `logique-de-cours` 5.

## Comment l'énoncé est posé dans ces cours

- Une diapositive `<préfixe>_<clé>_enonce` avant la première diapositive de chaque exercice : `visual.kind = "simulation"`,
  url `feuille.html?sujet=physique/<année>-<session>&exercice=<n>` (numéro = rang de l'exercice dans `exam.json`), pointage `start` au
  premier mot, texte dit = phrase de liaison en darija + l'énoncé lu en français tel qu'à l'examen (contexte et questions jouées, nombres
  et unités en mots), pas d'`audio` : piste ajoutée dans `backend/data/curriculum/architecture/<deck>_voix.json`.
- Le gabarit `feuille.html` n'est pas encore poussé (session « feuille-examen ») : la colonne « figures à redessiner » ci-dessous lui
  donne, pour chaque exercice, les documents de `exam.json` (titre et image de référence `assets/…`).

## Exercices du national joués

### phys_ch1_waves_exemple

| énoncé | sujet | exercice | page(s) | questions lues | figures à redessiner (exam.json) | diapositives jouées |
|---|---|---|---|---|---|---|
| `wx_n1_enonce` | 2022 normale | 2 — Ondes sonores et désintégration de l'iode 131 | p4 | 1.1, 1.2, 3 | Figure 2 (`assets/fig2p4.png`); Figure 3 (`assets/fig3p4.png`) | `wx_n1_national_2022n`, `wx_n1c_correction_2022n` |
| `wx_n2_enonce` | 2024 rattrapage | 2 — Propagation d'une onde mécanique | p6 | 3, 4 | Figure 1 (`assets/fig1p6.png`); Figure 2 (`assets/fig2p6.png`) | `wx_n2_national_2024r`, `wx_n2c_correction_2024r` |
| `wx_n3_enonce` | 2024 normale | 2 — Propagation d'un signal mécanique à la surface de l'eau | p3 | 2, 2 | Figure suivante (`assets/figsuivantep3.png`) | `wx_n3_national_2024n`, `wx_n3c_correction_2024n` |
| `wx_n7_enonce` | 2022 rattrapage | 2 — Ondes mécaniques et datation au carbone 14 | ? | 1, 3, 4 | Figure 1 — Élongation y_M du point M en fonction du temps (`assets/fig1_onde_ym_t.jpg`) | `wx_n7_national_2022r`, `wx_n7c_correction_2022r` |
| `wx_n4_enonce` | 2021 rattrapage | 2 — Les ondes sonores | p4 | 2 | Figure 1 (`assets/fig1p4.png`); Figure 2 (`assets/fig2p4.png`) | `wx_n4_national_2021r`, `wx_n4c_correction_2021r` |
| `wx_n5_enonce` | 2020 rattrapage | 2 — Les ultrasons au service de la médecine | p3, p4 | 2.1, 2.2, 2.3 | Figure 1 (bis) (`assets/fig11p3.png`); Figure 2 (`assets/fig2p4.png`) | `wx_n5_national_2020r`, `wx_n5c_correction_2020r` |
| `wx_n6_enonce` | 2018 normale | 2 — Célérité des ultrasons | p4 | 2, 3, 4 | Figure 1 (`assets/fig1p4.png`); Figure 2 (`assets/fig2p4.png`) | `wx_n6_national_2018n`, `wx_n6c_correction_2018n` |

Moments où l’on compte (relevé automatique sur le texte dit et l’écrit — quelques lignes peuvent être de simples mentions, à vérifier) :

| diapositive | titre | état |
|---|---|---|
| `wx_l1_aspect` | IV.1 Avant de lire, regarde l'axe | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `wx_m1b_lecture` | V.2 TP : lire τ sur l’oscilloscope | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `wx_n1_national_2022n` | VII.1 National 2022 normale : célérité du son dans l'air | fait (simulation) : la question s’arrête avant ; la démonstration allume `divisions` |
| `wx_n1c_correction_2022n` | VII.1 b Correction jouée : Δt, puis v | fait : la voix compte « une, deux, trois, quatre, cinq », chaque division s’allume (div_1…div_5), total « 5 divisions » |
| `wx_n2_national_2024r` | VII.2 National 2024 rattrapage : un émetteur entre deux micros | idem |
| `wx_n2c_correction_2024r` | VII.2 b Correction jouée : τ, puis les deux chemins et ℓ | fait : 4 divisions comptées et allumées une à une |
| `wx_n4_national_2021r` | VII.5 National 2021 rattrapage : la droite Δt = f(d) | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `wx_n6_national_2018n` | VII.7 National 2018 normale : air et pétrole, même distance | idem |
| `wx_n6c_correction_2018n` | VII.7 b Correction jouée : τ, la relation, puis V_p | fait : 2 divisions comptées et allumées une à une |
| `wx_b3_bilan` | Ce qu'il faut retenir | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `wx_b4_carte` | La carte du chapitre | à faire : comptage à allumer élément par élément (non traité dans cette passe) |


### phys_ch2_ondes_periodiques

| énoncé | sujet | exercice | page(s) | questions lues | figures à redessiner (exam.json) | diapositives jouées |
|---|---|---|---|---|---|---|
| `op_r3_enonce` | 2022 rattrapage | 2 — Ondes mécaniques et datation au carbone 14 | ? | 1, 3, 4 | Figure 1 — Élongation y_M du point M en fonction du temps (`assets/fig1_onde_ym_t.jpg`) | `op_r3_trois_lectures`, `op_r3c_periode`, `op_r3b_calculs` |
| `op_x1_enonce` | 2017 normale | 2 — Propagation d'une onde mécanique à la surface de l'eau | p4 | 1, 2, 3, 4 | Figure ci-dessous (`assets/figcidessousp4.png`) | `op_x1_national_2017`, `op_x1b_national_2017_retard` |
| `op_x2_enonce` | 2020 normale | 2 — Propagation des ondes | p4 | II.1, II.2, II.3 | Figure ci-contre (`assets/figcicontrep4.png`) | `op_x2_national_2020`, `op_x2b_national_2020_diffraction` |

Moments où l’on compte (relevé automatique sur le texte dit et l’écrit — quelques lignes peuvent être de simples mentions, à vérifier) :

| diapositive | titre | état |
|---|---|---|
| `op_o3_periodique` | Le mot « périodique » | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `op_o4_definition` | Onde progressive périodique | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `op_t3_frequence` | La fréquence N | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `op_t4_inverse` | N = 1/T | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `op_t7_oscillo` | Lire T sur un oscillogramme | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `op_t8_non_sinusoidale` | Périodique, mais pas sinusoïdale | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `op_l5_intervalles` | Compter les intervalles | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `op_l6_source` | Depuis la source | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `op_c1_avance` | Pendant une période, l'onde avance de λ | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `op_c4_photo_datee` | Une photo datée | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `op_p3_methode` | La méthode : d sur λ | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `op_r2_relation` | M refait ce que S a fait | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `op_r3b_calculs` | National 2022 R : de la courbe aux calculs, N et v | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `op_m2_immobile` | L'immobilité apparente | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `op_m4_microsecondes` | Lire T en microsecondes | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `op_m6_nieme` | Pour la n-ième fois | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `op_d4_ultrasons` | Le son et les ultrasons se diffractent aussi | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `op_s1_frequence` | On change la fréquence du vibreur | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `op_s2_air` | Et dans l'air ? | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `op_x2_national_2020` | National 2020 : les rides circulaires, λ, N et le retard | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `op_b1_bilan` | Ce qu'il faut retenir | à faire : comptage à allumer élément par élément (non traité dans cette passe) |


### phys_ch3_ondes_lumineuses

| énoncé | sujet | exercice | page(s) | questions lues | figures à redessiner (exam.json) | diapositives jouées |
|---|---|---|---|---|---|---|
| `ol_x2_enonce` | 2023 rattrapage | 2 — Diffraction de la lumière | ? | 2, 3 | — | `ol_x2_national_2023`, `ol_x2b_2023_rouge` |
| `ol_x3_enonce` | 2021 normale | 2 — Propagation des ondes lumineuses | p4 | 1, 2.1, 2.2, 2.3, 3.1, 3.2, 3.3 | Figure 2 (`assets/fig2p4.png`); Figure 3 (`assets/fig3p4.png`) | `ol_x3_national_2021`, `ol_x3b_2021_prisme`, `ol_x3c_2021_courbe`, `ol_x3d_2021_lambda` |
| `ol_x4_enonce` | 2025 rattrapage | 2 — Diffraction et détermination de l'indice de réfraction | p3 | 2.1, 2.2, 3.1, 3.2 | Figure ci-contre (`assets/figcicontrep3.png`) | `ol_x4_national_2025`, `ol_x4b_2025_indice` |

Moments où l’on compte (relevé automatique sur le texte dit et l’écrit — quelques lignes peuvent être de simples mentions, à vérifier) :

| diapositive | titre | état |
|---|---|---|
| `ol_d5_montage` | Les mots du montage | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `ol_p1_radian` | Rappel : l'angle en radian | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `ol_p2_tangente` | Rappel : la tangente d'un angle | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `ol_l7_calcul_lambda` | Je mesure, je calcule λ | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `ol_g1_points` | Quatre fentes, quatre mesures | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `ol_g3_pente` | Le coefficient directeur et ses unités | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `ol_g6_theta` | Vérifier θ = λ/a par des mesures | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `ol_n1_ralentit` | Dans le verre, la lumière ralentit | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `ol_n2_frequence` | La fréquence ne change pas | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `ol_c5_cuve` | La même expérience dans l'eau | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `ol_p3_deux_celerites` | Deux couleurs, deux célérités | à faire : comptage à allumer élément par élément (non traité dans cette passe) |


### phys_ch4_radioactivite

| énoncé | sujet | exercice | page(s) | questions lues | figures à redessiner (exam.json) | diapositives jouées |
|---|---|---|---|---|---|---|
| `ra_f3_enonce` | 2024 rattrapage | 3 — Désintégration en chaîne | p4 | 1, 2 | Diagramme ci-contre (`assets/diagcicontrep4.png`) | `ra_f3_famille2024` |
| `ra_a6_enonce` | 2022 normale | 2 — Ondes sonores et désintégration de l'iode 131 | p4 | 2, 6.1 | Figure 2 (`assets/fig2p4.png`); Figure 3 (`assets/fig3p4.png`) | `ra_a6_courbe_a` |
| `ra_a7_enonce` | 2021 rattrapage | 3 — Désintégration du phosphore 32 | p5 | 2, 2.1, 2.2 | Figure ci-contre (`assets/figcicontrep5.png`) | `ra_a7_droite_ln` |
| `ra_c4b_enonce` | 2020 rattrapage | 3 — Désintégration de l'uranium 234 | ? | 3, 4.1, 4.2, 4.3 | — | `ra_c4b_rapport` |
| `ra_c3_enonce` | 2022 rattrapage | 2 — Ondes mécaniques et datation au carbone 14 | ? | 2, 3 | Figure 1 — Élongation y_M du point M en fonction du temps (`assets/fig1_onde_ym_t.jpg`) | `ra_c3_calcul`, `ra_c3b_lambda`, `ra_c3c_age`, `ra_c3d_verif` |
| `ra_x2_enonce` | 2021 normale | 3 — Désintégration du plutonium 238 | p5 | 1, 2.1, 2.2, 2.3, 3 | Figure ci-contre (`assets/figcicontrep5.png`) | `ra_x2_2021N`, `ra_x2b_2021N`, `ra_x2c_2021N`, `ra_x2d_2021N`, `ra_x2e_2021N` |
| `ra_x3_enonce` | 2022 normale | 2 — Ondes sonores et désintégration de l'iode 131 | p4 | 2, 4, 6.1, 6.2, 6.3 | Figure 2 (`assets/fig2p4.png`); Figure 3 (`assets/fig3p4.png`) | `ra_x3_2022N`, `ra_x3b_2022N`, `ra_x3c_2022N` |
| `ra_x4_enonce` | 2025 normale | 2 — Désintégration du cadmium 107 | ? | 2, 3.1, 3.2, 3.3 | — | `ra_x4_2025N`, `ra_x4b_2025N`, `ra_x4c_2025N` |

Moments où l’on compte (relevé automatique sur le texte dit et l’écrit — quelques lignes peuvent être de simples mentions, à vérifier) :

| diapositive | titre | état |
|---|---|---|
| `ra_n2_atome` | De l'atome au noyau | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `ra_n3_compter` | Compter les nucléons | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `ra_n4_notation` | La notation ᴬ_Z X | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `ra_n6_isotopes` | Nucléides et isotopes | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `ra_r2b_spontanee` | Spontanée et inéluctable : chauffer n'y change rien | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `ra_r3_soddy` | Les lois de Soddy | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `ra_s4b_alpha` | La flèche α : deux protons et deux neutrons en moins | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `ra_f2_systeme` | Combien de α, combien de β⁻ ? | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `ra_p3_puissances` | Rappel : les puissances de dix | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `ra_l1_echantillon` | Beaucoup de noyaux : que devient l'échantillon ? | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `ra_l1b_moitie` | Compter les noyaux tous les 8 jours | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `ra_l2_proportion` | Chaque jour, la même proportion | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `ra_l7_tau` | La constante de temps τ | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `ra_l7b_037` | Lire τ à 0,37·N₀ | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `ra_t3_paliers` | N₀/2, N₀/4, N₀/8 | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `ra_a1_compteur` | Le compteur Geiger compte les désintégrations | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `ra_a2_definition` | L'activité a, en becquerel | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `ra_a3b_loi_activite` | a₀ = λ·N₀ et a(t) = a₀·e^(−λt) | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `ra_p4_mole` | Rappel : la mole, un paquet d'entités | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `ra_a7_droite_ln` | La droite ln N = f(t) (national 2021 R) | à faire : comptage à allumer élément par élément (non traité dans cette passe) |


### phys_ch5_energie_nucleaire

| énoncé | sujet | exercice | page(s) | questions lues | figures à redessiner (exam.json) | diapositives jouées |
|---|---|---|---|---|---|---|
| `en_d4_enonce` | 2022 rattrapage | 2 — Ondes mécaniques et datation au carbone 14 | ? | 2, 1.1, 2 | Figure 1 — Élongation y_M du point M en fonction du temps (`assets/fig1_onde_ym_t.jpg`) | `en_d4_carbone` |
| `en_a3_enonce` | 2023 normale | 2 — Étude de quelques transformations nucléaires du tritium | ? | 5.a, 5.b | — | `en_a3_comparer` |
| `en_b3_enonce` | 2016 normale | 2 — Fusion nucléaire | ? | 1, 2, 3 | — | `en_b3_fusion_calcul` |
| `en_b5_enonce` | 2017 rattrapage | 2 — Diffraction d'une onde lumineuse et noyau du cobalt 60 | ? | 2.1, 2.2, 2.3 | — | `en_b5_beta` |
| `en_e3_enonce` | 2023 normale | 2 — Étude de quelques transformations nucléaires du tritium | ? | 6 | — | `en_e3_2023` |
| `en_e4_enonce` | 2020 normale | 3 — Désintégration du polonium 210 | p4 | 1, 2.1, 2.2 | Diagramme ci-contre (`assets/diagcicontrep4.png`) | `en_e4_polonium` |
| `en_n3_enonce` | 2025 normale | 2 — Désintégration du cadmium 107 | ? | 3.1, 3.2, 3.3 | — | `en_n3_2025` |
| `en_c2_enonce` | 2019 normale | 2 — Ondes mécaniques et désintégration nucléaire | p3 | 2.1, 2.2, 2.3 | Figure ci-contre (`assets/figcicontrep3.png`) | `en_c2_qcm2019` |

Moments où l’on compte (relevé automatique sur le texte dit et l’écrit — quelques lignes peuvent être de simples mentions, à vérifier) :

| diapositive | titre | état |
|---|---|---|
| `en_p2_puissances` | Rappel : les puissances de dix | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `en_m2b_un_gramme` | Un gramme de masse : combien d'énergie ? | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `en_m3_unites` | L'unité de masse du noyau : u | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `en_m3b_electronvolt` | L'électronvolt et le MeV | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `en_d1_composition` | Le noyau ᴬ_ZX : Z protons, N neutrons | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `en_d2_balance` | On pèse le noyau et ses nucléons | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `en_d3_formule` | Le défaut de masse Δm | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `en_d4_carbone` | Calculer un défaut de masse (national 2022 R) | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `en_l1_separer` | Séparer un noyau coûte de l'énergie | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `en_l2_former` | Former un noyau libère de l'énergie : E_ℓ = Δm·c² | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `en_l3_calcul` | Calculer une énergie de liaison | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `en_l4_par_nucleon` | L'énergie de liaison par nucléon E_ℓ/A | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `en_s2_piege` | Le piège : la plus grande E_ℓ n'est pas la plus stable | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `en_a1_courbe` | La courbe d'Aston | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `en_a3_comparer` | Lire deux noyaux : le deutérium et le tritium (national 2023 N) | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `en_r1_spontanee` | Réaction spontanée, réaction provoquée | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `en_b5_beta` | Énergie libérée par une désintégration β⁻ (national 2017 R) | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `en_e1_diagramme` | Le diagramme énergétique | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `en_e2_formule` | ΔE à partir des énergies de liaison | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `en_e4_polonium` | Lire un diagramme du national (2020 N) | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `en_n1_echantillon` | Combien de noyaux dans un échantillon ? | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `en_n2_comparaison` | Fission ou fusion : laquelle libère le plus ? | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `en_z1_bilan` | Ce qu'il faut retenir | à faire : comptage à allumer élément par élément (non traité dans cette passe) |


### phys_ch6_dipole_RC

| énoncé | sujet | exercice | page(s) | questions lues | figures à redessiner (exam.json) | diapositives jouées |
|---|---|---|---|---|---|---|
| `rc_e8_enonce` | 2023 rattrapage | 3 — Circuits RC, RLC et détection AM | p6 | 1.1 | Figure 2 (`assets/fig2p6.png`); Figure 3 (`assets/fig3p6.png`) | `rc_e8_national` |
| `rc_np_enonce` | 2022 normale | 3 — Dipôle RC et oscillations RLC | p7, p8 | 1.1, 1.2.1, 1.2.2, 1.2.3 | Figure 1 (`assets/fig1p7.png`); Figure 2 (`assets/fig2p7.png`); Figure 3 (`assets/fig3p8.png`) | `rc_np0_sujet`, `rc_np1_equation`, `rc_np2_courant`, `rc_np3_lire`, `rc_np4_R`, `rc_np5_tangente`, `rc_np6_pourcent`, `rc_np7_C`, `rc_np8_energie`, `rc_np9_copie` |
| `rc_n1_enonce` | 2019 normale | 3 — Charge et décharge d'un condensateur | p4, p5 | I.1, I.2, I.3.1, I.3.2, I.4, I.5 | Figure 1 (`assets/fig1p4.png`); Figure 2 (`assets/fig2p4.png`); Figure 3 (`assets/fig3p5.png`) | `rc_n1_2019` |
| `rc_n2_enonce` | 2021 rattrapage | 4 — Réponse des dipôles RC, RL et oscillations dans un circuit RLC | p5, p6, p7 | I.1, I.2, I.3, I.4 | Figure 1 (`assets/fig1p5.png`); Figure 2 (`assets/fig2p5.png`); Figure 3 (`assets/fig3p6.png`); Figure 4 (`assets/fig4p6.png`); Figure 5 (`assets/fig5p6.png`); Figure 6 (`assets/fig6p7.png`) | `rc_n2_2021R` |

Moments où l’on compte (relevé automatique sur le texte dit et l’écrit — quelques lignes peuvent être de simples mentions, à vérifier) :

| diapositive | titre | état |
|---|---|---|
| `rc_rp6_derivee` | Rappel : la dérivée, c’est une pente | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `rc_s6_tableau` | Le tableau avant la courbe | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `rc_l3_descente` | Courbes qui descendent : 37 % | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `rc_l8_calcul` | Calculer l'énergie | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `rc_n2_2021R` | Un sujet complet : l'intensité (2021 R) | à faire : comptage à allumer élément par élément (non traité dans cette passe) |


### phys_ch7_dipole_RL

| énoncé | sujet | exercice | page(s) | questions lues | figures à redessiner (exam.json) | diapositives jouées |
|---|---|---|---|---|---|---|
| `rl_b10_enonce` | 2020 normale | 4 — Réponse d'un dipôle RL, décharge d'un condensateur et entretien des oscillations | p5, p6 | I.1, I.2, I.3 | Figure 1 (`assets/fig1p5.png`); Figure 2 (`assets/fig2p5.png`); Figure 3 (`assets/fig3p5.png`); Figure 4 (`assets/fig4p6.png`); Figure 5 (`assets/fig5p6.png`); Figure 6 (`assets/fig6p6.png`) | `rl_b10_national` |
| `rl_e7_enonce` | 2021 rattrapage | 4 — Réponse des dipôles RC, RL et oscillations dans un circuit RLC | p5, p6, p7 | II.1, II.2, II.3, II.4, II.5 | Figure 1 (`assets/fig1p5.png`); Figure 2 (`assets/fig2p5.png`); Figure 3 (`assets/fig3p6.png`); Figure 4 (`assets/fig4p6.png`); Figure 5 (`assets/fig5p6.png`); Figure 6 (`assets/fig6p7.png`) | `rl_e7_2021R` |
| `rl_e8_enonce` | 2019 rattrapage | 3 — Dipôle RL, circuit RLC et modulation d'amplitude | p5, p6 | 1.1, 1.2, 1.3, 1.4, 1.5, 1.6 | Figure 1 (`assets/fig1p5.png`); Figure 2 (`assets/fig2p5.png`); Figure 4 (`assets/fig4p5.png`); Figure 5 (`assets/fig5p6.png`) | `rl_e8_2019R` |
| `rl_t4_enonce` | 2025 rattrapage | 3 — Circuit RL, circuit LC et modulation d'amplitude | p4, p5 | 1.1, 2.1, 2.2, 2.3 | Figure 1 (`assets/fig1p4.png`); Figure 2 (`assets/fig2p4.png`); Figure 4 (`assets/fig4p5.png`) | `rl_t4_national` |
| `rl_np_enonce` | 2023 normale | 3 — Réponse d'un dipôle RL, circuit LC et modulation d'amplitude | p4, p5 | 1.1, 1.2.1, 1.2.2, 1.3 | Figure 1 (`assets/fig1p4.png`); Figure 2 (`assets/fig2p4.png`); Figure 3 (`assets/fig3p4.png`); Figure 4 (`assets/fig4p4.png`); Figure 5 (`assets/fig5p5.png`) | `rl_np0_sujet`, `rl_np1_equation`, `rl_np2_remplacer`, `rl_np3_constantes`, `rl_np4_lire`, `rl_np5_tangente`, `rl_np6_pourcent`, `rl_np7_L`, `rl_np8_ub`, `rl_np9_energie`, `rl_np10_copie` |
| `rl_n1_enonce` | 2022 rattrapage | 3 — Circuits électriques et ondes modulées | p6, p7 | 1.1, 1.2, 1.3, 1.4, 1.5, 1.6 | Figure 4 (`assets/fig4p6.png`); Figure 5 (`assets/fig5p6.png`); Figure 6 (`assets/fig6p6.png`); Figure 1 (`assets/fig1p7.png`); Figure 2 (`assets/fig2p7.png`) | `rl_n1_2022R` |
| `rl_n2_enonce` | 2024 normale | 4 — Décharge d'un condensateur dans un dipôle RL et réponse d'un dipôle RL à un échelon de tension | p5 | 2.1, 2.2.1, 2.2.2 | Figure 1 (`assets/fig1p5.png`); Figure 3 (`assets/fig3p5.png`); Figure 4 (`assets/fig4p5.png`) | `rl_n2_2024N` |

Moments où l’on compte (relevé automatique sur le texte dit et l’écrit — quelques lignes peuvent être de simples mentions, à vérifier) :

| diapositive | titre | état |
|---|---|---|
| `rl_rp3_derivee` | Rappel : la dérivée, c’est une pente | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `rl_t3_diode` | Étincelle et diode | à faire : comptage à allumer élément par élément (non traité dans cette passe) |


### phys_ch8_circuit_RLC

| énoncé | sujet | exercice | page(s) | questions lues | figures à redessiner (exam.json) | diapositives jouées |
|---|---|---|---|---|---|---|
| `lc_r4_enonce` | 2021 rattrapage | 4 — Réponse des dipôles RC, RL et oscillations dans un circuit RLC | p5, p6, p7 | III.1, III.2, III.3 | Figure 1 (`assets/fig1p5.png`); Figure 2 (`assets/fig2p5.png`); Figure 3 (`assets/fig3p6.png`); Figure 4 (`assets/fig4p6.png`); Figure 5 (`assets/fig5p6.png`); Figure 6 (`assets/fig6p7.png`) | `lc_r4_national` |
| `lc_p4_enonce` | 2022 normale | 3 — Dipôle RC et oscillations RLC | p7, p8 | 2.1.1, 2.1.2, 2.1.3.a, 2.1.3.b | Figure 1 (`assets/fig1p7.png`); Figure 2 (`assets/fig2p7.png`); Figure 3 (`assets/fig3p8.png`) | `lc_p4_national` |
| `lc_l4_enonce` | 2023 normale | 3 — Réponse d'un dipôle RL, circuit LC et modulation d'amplitude | p4, p5 | 2.1, 2.2.1, 2.2.2 | Figure 1 (`assets/fig1p4.png`); Figure 2 (`assets/fig2p4.png`); Figure 3 (`assets/fig3p4.png`); Figure 4 (`assets/fig4p4.png`); Figure 5 (`assets/fig5p5.png`) | `lc_l4_2023` |
| `lc_np_enonce` | 2022 normale | 3 — Dipôle RC et oscillations RLC | p7, p8 | 2.1.1, 2.1.2, 2.1.3.a, 2.1.3.b, 2.2.1, 2.2.2 | Figure 1 (`assets/fig1p7.png`); Figure 2 (`assets/fig2p7.png`); Figure 3 (`assets/fig3p8.png`) | `lc_np0_sujet`, `lc_np1_equation`, `lc_np2_choix`, `lc_np3_T0`, `lc_np4_lire`, `lc_np5_L`, `lc_np6_energie`, `lc_np7_lectures`, `lc_np8_dissipee`, `lc_np9_entretien`, `lc_np10_copie` |
| `lc_n1_enonce` | 2020 normale | 4 — Réponse d'un dipôle RL, décharge d'un condensateur et entretien des oscillations | p5, p6 | II.1, II.2, II.3, III.1, III.2, III.3, III.4 | Figure 1 (`assets/fig1p5.png`); Figure 2 (`assets/fig2p5.png`); Figure 3 (`assets/fig3p5.png`); Figure 4 (`assets/fig4p6.png`); Figure 5 (`assets/fig5p6.png`); Figure 6 (`assets/fig6p6.png`) | `lc_n1_2020N` |
| `lc_n2_enonce` | 2025 normale | 3 — Charge/décharge d'un condensateur et démodulation d'onde AM | p4, p5 | 2.1, 2.2.1, 2.2.2, 2.3, 2.4 | Figure 1 (`assets/fig1p4.png`); Figure 2 (`assets/fig2p4.png`); Figure 3 (`assets/fig3p5.png`); Figure 4 (`assets/fig4p5.png`) | `lc_n2_2025N` |

Moments où l’on compte (relevé automatique sur le texte dit et l’écrit — quelques lignes peuvent être de simples mentions, à vérifier) :

| diapositive | titre | état |
|---|---|---|
| `lc_o1_carte` | La carte du chapitre : un condensateur qui se vide dans une bobine | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `lc_r1_pseudo` | Une petite résistance : les sommets baissent | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `lc_r4_national` | Exercice du national : à chaque courbe sa résistance | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `lc_l1_mesure` | Lire T sur plusieurs périodes | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `lc_l2_voisine` | La pseudo-période est voisine de T₀ | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `lc_l4_2023` | Exercice du national : l'échelle en flèches | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `lc_en4_somme` | Sans résistance, la somme ne bouge pas | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `lc_a2_derivee` | Dériver chaque énergie | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `lc_np4_lire` | 2022 N, étape 4 : lire T₀ | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `lc_n2_2025N` | Sujet national 2025 N, en entier | à faire : comptage à allumer élément par élément (non traité dans cette passe) |
| `lc_bl_fiche` | Ce qu'il faut retenir | à faire : comptage à allumer élément par élément (non traité dans cette passe) |



## Bilan de la passe du 19/11/2026

| cours | énoncés posés | pistes nouvelles (énoncés + voix recomptées) | pistes en attente dans le _voix.json |
|---|---|---|---|
| `phys_ch1_waves_exemple` | 7 | 10 | 36 |
| `phys_ch2_ondes_periodiques` | 3 | 3 | 91 |
| `phys_ch3_ondes_lumineuses` | 3 | 3 | 78 |
| `phys_ch4_radioactivite` | 8 | 8 | 115 |
| `phys_ch5_energie_nucleaire` | 8 | 8 | 85 |
| `phys_ch6_dipole_RC` | 4 | 4 | 40 |
| `phys_ch7_dipole_RL` | 7 | 7 | 46 |
| `phys_ch8_circuit_RLC` | 6 | 6 | 57 |

Fait en plus dans ch1 : divisions comptées en s'allumant (VII.1 b, VII.2 b, VII.7 b, voix réécrites), VII.3 joué sur la figure
(plus de tableau à part, r₁, r₂, Δr allumés), lignes `allume` sur les démonstrations des 7 questions, commandes `allume`/`eteins`
dans `ondes-tableau/national.html`.

Reste à faire : les moments de comptage marqués « à faire » ci-dessus (ch1 hors nationaux, ch2 à ch8) et la démonstration allumée
sur la figure pour les exercices du national de ch2 à ch8 (simulations `national.html`, `figures.html`, `national-pas-a-pas.html`).
