# Audit du national — chimie (ch9 à ch13)

19 novembre 2026. Demandes de l'utilisateur du 18/11/2026 : (1) compter en allumant chaque élément tour à tour ;
(2) un exercice du national commence par la page du sujet telle qu'à l'examen, lue par le tuteur ; (3) la
démonstration se joue sur la figure de l'examen ou la simulation. Règles : skill `simulations-au-tableau` 16-17,
`professeur` 44-46, `logique-de-cours` 5.

## Comment l'énoncé est montré

Précision de l'utilisateur du 19/11/2026 (skill `professeur` règle 46, commit af73de66) : l'énoncé n'est PAS la
photo du sujet. Il est reproduit en code comme la vraie feuille d'examen (fond blanc, en-tête officiel, questions
numérotées, barème à droite, textes, données et figures redessinés), avec le gabarit commun
`frontend/public/media/simulations/shared/examen/feuille.html?sujet=physique/<année>-<session>&exercice=<n>`
(fait par la session « feuille-examen »). Le texte et les points viennent de `exam.json` ; les scans
`pages/sujet_pN.jpg` ne servent que de modèle. La première page « scan » (`chimie/shared/enonce-examen.html`,
commit d19b81e3) est retirée. `scripts/examens/lignes_page.py` reste un outil pour relire les scans.

## Exercices du national joués et moments où l'on compte (relevé de départ)

Relevé automatique des cours (titres et voix) au 19/11/2026, avant les changements. « Page » et l'état après
travail sont dans la section « Ce qui a été fait » plus bas.

## phys_ch9_transformations_lentes_rapides

| diapositive | titre | sujet | simulation |
|---|---|---|---|
| `tl_np0_sujet` | Un exercice type national : lire le sujet deux fois | ? | `chimie/transformations-lentes-rapides-tableau/national-pas-a-pas.html?sujet=iodure&etape=sujet` |
| `tl_n1_lecture` | National 2025 N : trois expériences, trois courbes | 2025-normale | `chimie/transformations-lentes-rapides-tableau/courbes.html?vue=lecture` |
| `tl_n2_glacee` | National 2017 R : l'eau glacée et deux facteurs | 2017-rattrapage | `chimie/transformations-lentes-rapides-tableau/facteurs.html?vue=trempe` |

Moments où l’on compte ou parcourt un à un (mots de la voix) :

- `tl_rp2_conservation` Rappel : une équation conserve tout — on compte
- `tl_x10_verifier` Vérifier une équation — on compte
- `tl_rp3_mole` Rappel : la quantité de matière, la mole — compte , on compte
- `tl_f1_facteur` Un facteur cinétique — une par une
- `tl_f8_variable` Une seule variable à la fois — colonne
- `tl_np3_initial` Étape 3 : le tableau, l'état initial — première ligne
- `tl_np4_encours` Étape 4 : le tableau, en cours — deuxième ligne, première ligne
- `tl_np5_limitant` Étape 5 : x_max et le réactif limitant — deuxième ligne

## phys_ch10_cinetique

| diapositive | titre | sujet | simulation |
|---|---|---|---|
| `ci_p4_2016R` | Au national : la conductimétrie (2016 R) | 2016-rattrapage | `chimie/cinetique-tableau/figures.html?fig=fig_2016R` |
| `ci_p6_2024N` | Au national : un suivi par dosage (2024 N) | 2024-normale | `chimie/cinetique-tableau/figures.html?fig=fig_2024N` |
| `ci_n1_aspirine` | National 2019 R : x_max, vitesse, t₁/₂ | 2019-rattrapage | `chimie/cinetique-tableau/figures.html?fig=fig_2019R` |
| `ci_n2_diminue` | National 2025 R : la vitesse diminue-t-elle ? | 2025-rattrapage | `chimie/cinetique-tableau/figures.html?fig=fig_2025R` |
| `ci_n3_deux` | National 2017 N : deux t₁/₂ | 2017-normale | `chimie/cinetique-tableau/figures.html?fig=fig_2017N` |
| `ci_n4_reactif` | National 2023 N : une courbe de réactif | 2023-normale | `chimie/cinetique-tableau/figures.html?fig=fig_2023N` |
| `ci_n5_trois` | National 2025 N : trois courbes, un seul x_f | 2025-normale | `chimie/cinetique-tableau/figures.html?fig=fig_2025N` |
| `ci_n7_conductance` | National 2018 R : la conductance G(t) | 2018-rattrapage | `chimie/cinetique-tableau/figures.html?fig=fig_2018R` |
| `ci_n8_trempe` | National 2017 R : trempe et état final | 2017-rattrapage | `chimie/cinetique-tableau/figures.html?fig=fig_2017R` |
| `ci_n6a_tableau` | National 2021 N, question 1 : tableau d’avancement et x_f | 2021-normale | `chimie/cinetique-tableau/national.html?vue=2021N_q1` |
| `ci_n6b_demi` | National 2021 N, question 2 : σ(t) et t₁/₂ | 2021-normale | `chimie/cinetique-tableau/national.html?vue=2021N_q2` |
| `ci_n6c_montrer` | National 2021 N, question 3 : montrer v = −(1/(160·V₀))·dσ/dt | 2021-normale | `chimie/cinetique-tableau/national.html?vue=2021N_q3` |
| `ci_n6d_vitesse` | National 2021 N, question 4 : v₁ par la tangente | 2021-normale | `chimie/cinetique-tableau/national.html?vue=2021N_q4` |

Moments où l’on compte ou parcourt un à un (mots de la voix) :

- `ci_z1_mole` Rappel : la mole, compter par paquets — compte , compter
- `ci_a1_tableau` Le tableau d’avancement : l’état initial — première ligne
- `ci_a1b_en_cours` Le tableau d’avancement : en cours et état final — deuxième ligne
- `ci_a3_lien` Mesurer n(I₂), c'est connaître x — colonne
- `ci_m1_mesures` Des mesures à des dates — première ligne
- `ci_g3_formule` σ = Σ λᵢ·[Xᵢ] — on compte
- `ci_v5_diminue` La vitesse diminue — colonne
- `ci_n6a_tableau` National 2021 N, question 1 : tableau d’avancement et x_f — ligne par ligne
- `ci_r1_litres` Piège de rédaction : V en litres — deuxième ligne, première ligne

## phys_ch11_transformations_deux_sens

| diapositive | titre | sujet | simulation |
|---|---|---|---|
| `td_e6_national` | National 2017 N : totale ou limitée ? | 2017-normale | `chimie/transformations-deux-sens-tableau/figures.html?fig=fig_2017N` |
| `td_n1a_equation` | National 2021 R (1) : l’acide méthanoïque et l’eau | 2021-rattrapage | `chimie/transformations-deux-sens-tableau/national.html?ex=2021R&vue=q1` |
| `td_n1b_montrer` | National 2021 R (2) : montrer que τ = 10^(−pH)/C | 2021-rattrapage | `chimie/transformations-deux-sens-tableau/national.html?ex=2021R&vue=q2` |
| `td_n1c_courbe` | National 2021 R (3) : lire τ sur la courbe | 2021-rattrapage | `chimie/transformations-deux-sens-tableau/national.html?ex=2021R&vue=q3` |
| `td_n1d_dilution` | National 2021 R (4) : C, puis l’effet de la dilution | 2021-rattrapage | `chimie/transformations-deux-sens-tableau/national.html?ex=2021R&vue=q4` |
| `td_n2_conductivite` | National 2019 N : τ par la conductivité | 2019-normale | `chimie/transformations-deux-sens-tableau/conductimetrie.html?vue=national` |
| `td_n3_proportion` | National 2023 N : α = 1 − τ | 2023-normale | `chimie/transformations-deux-sens-tableau/avancement.html?vue=proportion` |
| `td_n4_dosage` | National 2024 R : un dosage est total (la méthode) | 2024-rattrapage | `chimie/transformations-deux-sens-tableau/avancement.html?vue=dosage` |
| `td_n4b_calcul` | National 2024 R : le calcul de τ | 2024-rattrapage | `chimie/transformations-deux-sens-tableau/avancement.html?vue=dosage&depart=x_max` |

Moments où l’on compte ou parcourt un à un (mots de la voix) :

- `td_z3_puissance` Rappel : les puissances de dix et le log — compte 
- `td_a1_tableau` Le tableau d'avancement — colonne, deuxième ligne, première ligne
- `td_a3_xf` L'avancement final se mesure — colonne
- `td_e6_national` National 2017 N : totale ou limitée ? — compte 
- `td_c2_relation` σ et [H₃O⁺] — on compte
- `td_d2_taux` La dilution augmente τ — colonne, deuxième ligne, première ligne
- `td_n4b_calcul` National 2024 R : le calcul de τ — ligne par ligne

## phys_ch12_etat_equilibre

| diapositive | titre | sujet | simulation |
|---|---|---|---|
| `ee_n4_pile` | National 2017 N : Qr,i d'une pile | 2017-normale | `chimie/etat-equilibre-tableau/quotient.html?vue=pile` |
| `ee_n3_melange` | National 2020 R : Qr,i d'un mélange | 2020-rattrapage | `chimie/etat-equilibre-tableau/quotient.html?vue=national` |
| `ee_n1_national` | National 2017 N : Qr,éq avec C et pH | 2017-normale | `chimie/etat-equilibre-tableau/equilibre.html?vue=national_2017` |
| `ee_n6_taux` | National 2021 N : τ puis Qr,éq | 2021-normale | `chimie/etat-equilibre-tableau/equilibre.html?vue=national_2021` |
| `ee_n2_base` | National 2022 R : une base avec l'eau | 2022-rattrapage | `chimie/etat-equilibre-tableau/equilibre.html?vue=base` |
| `ee_x1_equation` | National 2019 N (1/5) : l’équation avec l’eau | 2019-normale | `chimie/etat-equilibre-tableau/national.html?vue=q1&depart=debut` |
| `ee_x2_tableau` | National 2019 N (2/5) : le tableau d’avancement | 2019-normale | `chimie/etat-equilibre-tableau/national.html?vue=q2&depart=debut` |
| `ee_x3_sigma` | National 2019 N (3/5) : σ et [H₃O⁺]éq | 2019-normale | `chimie/etat-equilibre-tableau/national.html?vue=q3&depart=debut` |
| `ee_x4_taux` | National 2019 N (4/5) : τ = σ/(C·(λ₁ + λ₂)) | 2019-normale | `chimie/etat-equilibre-tableau/national.html?vue=q4&depart=debut` |
| `ee_x5_constante` | National 2019 N (5/5) : K en fonction de C et τ | 2019-normale | `chimie/etat-equilibre-tableau/national.html?vue=q5&depart=debut` |
| `ee_n5_courbe` | National 2017 R : K = 4 | 2017-rattrapage | `chimie/etat-equilibre-tableau/figures.html?fig=fig_2017R` |

Moments où l’on compte ou parcourt un à un (mots de la voix) :

- `ee_z2_puissance` Rappel : les puissances de dix et le log — compte 
- `ee_k1_trois` Trois concentrations, un même Qr,éq — colonne, deuxième ligne, première ligne
- `ee_m3_calcul` De σ à K — ligne par ligne
- `ee_f4_bilan` Quand on dilue : ce qui change, ce qui reste — deuxième ligne, première ligne

## phys_ch13_acides_bases

| diapositive | titre | sujet | simulation |
|---|---|---|---|
| `ab_b3_national` | National 2022 R : la méthylamine | 2022-rattrapage | `chimie/acides-bases-tableau/base.html?vue=national` |
| `ab_k4_national` | National 2020 R : K = 10 | 2020-rattrapage | `chimie/acides-bases-tableau/comparer.html?vue=national` |
| `ab_p4_national` | National 2025 R : lire un pKa sur la distribution | 2025-rattrapage | `chimie/acides-bases-tableau/figures.html?fig=fig_2025R` |
| `ab_n1_2016n` | National 2016 N : tangentes et indicateur | 2016-normale | `chimie/acides-bases-tableau/figures.html?fig=fig_2016N` |
| `ab_n2_2022r` | National 2022 R : doser la méthylamine | 2022-rattrapage | `chimie/acides-bases-tableau/figures.html?fig=fig_2022R` |
| `ab_n3_2022n` | National 2022 N : la dérivée et le pourcentage | 2022-normale | `chimie/acides-bases-tableau/figures.html?fig=fig_2022N` |
| `ab_n4_2024r` | National 2024 R : distribution d'une amine | 2024-rattrapage | `chimie/acides-bases-tableau/figures.html?fig=fig_2024R` |
| `ab_n5_2023r` | National 2023 R : la demi-équivalence | 2023-rattrapage | `chimie/acides-bases-tableau/exploiter.html?vue=national_2023` |
| `ab_x1_equation` | National 2018 N, question 1.1 : l’équation de dosage | 2018-normale | `chimie/acides-bases-tableau/national.html?ex=2018N&vue=q1` |
| `ab_x2_tangentes` | National 2018 N, question 1.2 : V_BE et pH_E | 2018-normale | `chimie/acides-bases-tableau/national.html?ex=2018N&vue=q2` |
| `ab_x3_concentration` | National 2018 N, question 1.3 : la concentration C_A | 2018-normale | `chimie/acides-bases-tableau/national.html?ex=2018N&vue=q3` |
| `ab_x4_indicateur` | National 2018 N, question 1.4 : l’indicateur coloré | 2018-normale | `chimie/acides-bases-tableau/national.html?ex=2018N&vue=q4` |
| `ab_x5_predominance` | National 2018 N, question 1.5 : l’espèce qui prédomine | 2018-normale | `chimie/acides-bases-tableau/national.html?ex=2018N&vue=q5` |
| `ab_x6_pka` | National 2018 N, en plus : le pKa à la demi-équivalence | 2018-normale | `chimie/acides-bases-tableau/national.html?ex=2018N&vue=q6` |

Moments où l’on compte ou parcourt un à un (mots de la voix) :

- `ab_z1_puissance` Rappel : les puissances de dix et le log — compte 
- `ab_w2a_mesures` Mesurer [H₃O⁺] et [HO⁻] dans trois solutions — colonne, deuxième ligne, première ligne

## Ce qui a été fait

(à compléter cours par cours)
