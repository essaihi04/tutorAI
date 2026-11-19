# Audit national — mathématiques ch1 à ch6

Demandes de l'utilisateur du 18/11/2026 : (1) compter ou parcourir en allumant chaque élément tour à tour (termes d'une
suite, points, carreaux, lignes d'un tableau…), jamais de chiffres griffonnés ; (2) un exercice du national commence par
la page du sujet telle qu'à l'examen (feuille reproduite en code, en-tête officiel, barème), lue par le tuteur, puis l'explication ;
(3) la démonstration se joue sur la figure (courbe, tableau de
variations, plan complexe) : chaque ligne allume ce qu'elle utilise (contrat du lecteur, skill `simulations-au-tableau`
règle 17), seulement les données de l'exercice.

Règles : skill `simulations-au-tableau` 16-17, `professeur` 44-46, `logique-de-cours` 5.

L'énoncé n'est pas le scan (précision de l'utilisateur, 19/11/2026, professeur règle 46) : c'est la feuille reproduite
en code, `shared/examen/feuille.html?sujet=mathematiques/<année>-<session>&exercice=<n>` (texte et barème de
`exam.json`, copiés par `scripts/examens/copier_sujets.py`), avec les réglages des vraies feuilles de maths :
`bareme=gauche&titre=souligne&entete=courte&page=<p>/4` (2025 R : `bareme=inline&entete=complete`, ses pages 2-4 n'ont
pas d'en-tête). Les scans `pages/sujet_pN.jpg` ont servi de modèle : page et zone de chaque exercice ci-dessous
(fraction de la hauteur, 0 = haut). Aucun de ces exercices n'a de figure à redessiner (texte seul).

## (a) Exercices du national joués

| Cours | Sujet | Exercice | Page | Zone | Diapositives qui le jouent | Énoncé d'abord |
|---|---|---|---|---|---|---|
| ch1 | — | aucun sujet réel : `lc_t6_rediger`, `lc_r4_deux_lignes`, `lc_r7_construire`, `lc_e1_probleme` sont « comme au national » (f(x) = x³ + x − 1, inventée) | — | — | — | sans objet |
| ch2 | — | aucun sujet réel : `df_dt6_morceaux`, `df_va8_aux_a`, `df_rec5_national`… « comme au national » (fonctions inventées) | — | — | — | sans objet |
| ch3 | 2016 R | Ex. 1 suites (u₀ = 2, uₙ₊₁ = uₙ/16 + 15/16) | p2 | 0,155 → 0,60 | `su_r3_heredite_affine`, `su_m2_difference` | `su_enonce_2016r` avant `su_r3` |
| ch3 | 2023 R | Ex. 1 suites (u₀ = 0, uₙ₊₁ = (uₙ − 2)/(2uₙ + 5)) | p2 | 0,095 → 0,415 | `su_r8_national` | `su_enonce_2023r` avant `su_r8` |
| ch3 | 2016 N | Ex. 1 suites (vₙ = (uₙ − 1)/(3 − uₙ)) | p2 | 0,135 → 0,525 | `su_x3_fraction` | `su_enonce_2016n` avant `su_x3` |
| ch3 | 2021 N | Ex. 2 suites (uₙ₊₁ = uₙ/(3 − 2uₙ)) | p2 | 0,24 → 0,605 | `su_x5_arithmetique` | `su_enonce_2021n` avant `su_x5` |
| ch3 | 2020 N | Ex. 1 suites (uₙ₊₁ = 2uₙ/(2uₙ + 5)) | p2 | 0,085 → 0,45 | `su_c5_deux_cinquiemes` | `su_enonce_2020n` avant `su_c5` |
| ch3 | 2025 R | Ex. 1 suites (0 < 2 − uₙ ≤ ½(2/7)ⁿ) — dit « 2025 » dans le cours | p1 en-tête + p2 | 0,01 → 0,30 | `su_c8_ecart` | `su_enonce_2025r` avant `su_c8` |
| ch3 | 2022 R | Ex. 1 suites (vₙ = uₙ − 1, somme jusqu'à u₂₀₂₁) — dit « 2022 » dans le cours | p2 | 0,09 → 0,395 | `su_p2_somme_mixte` | `su_enonce_2022r` avant `su_p2` |
| ch3 | 2024 N | Ex. 1 suites (u₀ = 4, uₙ₊₁ = (4uₙ − 2)/(1 + uₙ)) | p2 | 0,105 → 0,565 | `su_r6_ecriture_donnee`, `su_m3_egalite_donnee` (exemples de méthode), puis `su_e1_complet`, `su_e1_q2`, `su_e1_q3`, `su_e1_q4`, `su_e1_q5a`, `su_e1_q5` | `su_enonce_2024n` avant `su_e1_complet` |
| ch3 | (fin de problème) | `su_f7_national`, `su_f7b_limite` : g(x) = (4x + 3)/(x + 2), choisie par le cours (note du deck), pas un sujet réel | — | — | — | sans objet |
| ch4 | — | aucun sujet réel : `pr_x1`, `pr_x1_b`, `pr_x2`, `pr_x2_b` « type national » | — | — | — | sans objet |
| ch5 | 2019 N | Problème, première partie (f(x) = x + ½ − ln x + ½(ln x)²) | p3 | 0,095 → 0,985 | `ln_v2_b` (exemple), `ln_e3`, `ln_e3_b`, `ln_e3_c`, `ln_e3_d`, `ln_e4`, `ln_e4_b`, `ln_e4_c`, `ln_e4_d` | `ln_enonce_2019n` avant `ln_e3` |
| ch5 | 2021 N | Problème (f(x) = 2x ln x − 2x, f(0) = 0) | p3 | 0,385 → 0,985 | `ln_q5`, `ln_l8` (exemples), `ln_e5`, `ln_e5_b`, `ln_e5_q`, `ln_e5_c` | `ln_enonce_2021n` avant `ln_e5` |
| ch6 | 2017 N | Ex. 3 complexes (a = √3 + i, b = (1 + i)a) | p3 | 0,13 → 0,485 | `nc_m3`, `nc_r4` | `nc_enonce_2017n` avant `nc_m3` |
| ch6 | 2023 N | Ex. 2 complexes (a = √2 + i√2, b, c = b̄, d = 2i) | p2 | 0,485 → 0,955 | `nc_t2` (exemple), `nc_n1`, `nc_n1_b`, `nc_n1_alignes`, `nc_n1_c` | `nc_enonce_2023n` avant `nc_n1` |
| ch6 | 2024 N | Ex. 3 complexes (a = √3(1 − i), b = 2 + √3 + i) | p3 | 0,095 → 0,585 | `nc_t6`, `nc_n2` | `nc_enonce_2024n` avant `nc_t6` |
| ch6 | 2020 R | Ex. 2 complexes (a = √2/2 + i√2/2, a²⁰²⁰ réel) | p2 | 0,355 → 0,935 | `nc_r7` | `nc_enonce_2020r` avant `nc_r7` |
| ch6 | 2023 R | Ex. 3 complexes (a = √3/2 + 3i/2) | p3 | 0,095 → 0,565 | `nc_r8` | `nc_enonce_2023r` avant `nc_r8` |
| ch6 | 2025 N | Ex. 2 complexes (a = 1 + 2i, b = ā, ω = 5/2) | p2 | 0,50 → 0,96 | `nc_i2` | `nc_enonce_2025n` avant `nc_i2` |

## (b) Moments où l'on compte ou parcourt un à un

Outil commun : `maths/commun/compter.js` (`MathsCompte.compter`) — chaque élément s'allume (anneau lumineux, léger fond),
sa pastille porte son numéro courant, il reste allumé ; un moment et un repère par élément (`<prefixe>_1…`).

| Cours | Diapositive | Ce qu'on compte / parcourt | Simulation | Avant | Après |
|---|---|---|---|---|---|
| ch1 | `lc_t4_au_moins_une` | les rencontres de la courbe avec l'axe | `traversee.html?vue=vague` | trois points posés d'un coup | allumées 1, 2, 3 (`croise_1..3`), pointage sur « مرة، جوج، ثلاثة » |
| ch2 | `df_tr6_lire` | les points d'intersection avec y = 3 | `trace.html?vue=lecture` | entourés ensemble | allumés 1, 2 (`solution_1..2`), pointage sur « كتقطع la courbe ف جوج نقط » |
| ch2 | `df_ec3_etude_d` | les points placés depuis le tableau | `trace.html?vue=etude_pas` | déjà un par un, un moment par point | inchangé |
| ch3 | `su_a8_nombre_termes` | les arbres 5, 6, 7 | `arbres.html?vue=arbres` | dessinés ensemble | allumés 1, 2, 3 (`arbre_1..3`) avant « 7 − 5 + 1 = 3 » |
| ch3 | `su_p2_somme_mixte` | les 1 de la colonne | `arbres.html?vue=colonne` | entourés ensemble | allumés 1, 2, 3, …, 2022 (`un_1..4`) |
| ch3 | `su_x1_pourquoi` | les termes calculés un par un | `axe.html?vue=colonnes` | déjà fabriqués un par un (barres) | inchangé |
| ch6 | `nc_a6` | le cycle des puissances de i | `nombre-i.html?vue=cycle` | quarts de tour un par un, compteur | inchangé |
| ch6 | `nc_r7` | les puissances qui tombent sur l'axe réel | `moivre.html?vue=reel` | « elles s'allument » | inchangé |
| ch6 | `nc_n2` | 24 × π/12 jusqu'au tour complet | `moivre.html?vue=national` | spirale tracée d'un coup | 24 graduations allumées une à une, compteur « k × π/12 » |
| ch4 | — | aucun moment de comptage | — | — | — |

## (c) Fait, pistes à mettre en voix, reste à faire

### Corrections de `exam.json` (la feuille en dépend)
2016 N ex. 1 (2. séparée en a, b, c ; barème), 2019 N problème (numérotation de la feuille 1, 2.a-d, 3.a-c, 4.a-b,
5.a-b, 6.a-c, deuxième partie II.1.a-c, II.2), 2022 R ex. 1 (1.a u_n > 1 manquante ; barème), 2023 R ex. 3 (1.a et 1.b
à 0,25). Identifiants existants gardés. Les titres de ch5 citaient l'ancienne numérotation de 2019 : corrigés
(1, 2.b, 4.b, 5.a, 5.b), et la voix de `ln_e3_d` (« السؤال الرابع ») et `ln_e4_d` (« السؤال deux d »).

### Par cours
- **ch1** — pas d'exercice d'un vrai sujet (exercices « comme au national ») ; comptage `lc_t4`. 0 piste.
- **ch2** — pas d'exercice d'un vrai sujet ; comptage `df_tr6`. 0 piste.
- **ch3** — 8 énoncés `su_enonce_*` (feuille reproduite, lue, chaque question surlignée quand la voix la lit) ;
  `allume` sur les lignes de `su_r8`, `su_x3`, `su_c8`, `su_e1_complet`, `su_e1_q2` … `su_e1_q5` ; comptages `su_a8`,
  `su_p2`. **8 pistes** (`mixed` des `su_enonce_*`).
- **ch4** — pas d'exercice d'un vrai sujet (`pr_x1` … « type national »), pas de comptage. 0 piste.
- **ch5** — 2 énoncés (`ln_enonce_2019n` avant `ln_e3`, `ln_enonce_2021n` avant `ln_e5`) ; `allume` sur `ln_q5`,
  `ln_v2_b`, `ln_e3` … `ln_e5_c`. **2 pistes nouvelles** + 2 textes changés de pistes déjà à poser (`ln_e3_d`, `ln_e4_d`).
- **ch6** — 6 énoncés `nc_enonce_*` ; `allume` sur `nc_t2`, `nc_i2`, `nc_n1`, `nc_n1_b`, `nc_n1_c` ; comptage `nc_n2`.
  **6 pistes**.

### Reste à faire
- Démonstrations encore jouées sur un tableau de calcul (pas de figure) : `su_e1_complet`, `su_e1_q2`, `su_e1_q4`,
  `su_r8_national`, `su_x3_fraction` (`calculs.html`), `ln_v2_b`, `ln_e3_d`, `ln_e5_q`, `nc_t2` : leurs lignes allument
  les moments du tableau, pas une figure. À redessiner sur une figure (tableau de signes, suite sur un axe, plan complexe).
- Diapositives d'exercice du national sans `demonstration` (rien à allumer) : `su_r3`, `su_x5`, `su_c5`, `ln_l8`,
  `nc_m3`, `nc_r4`, `nc_r7`, `nc_r8`, `nc_t6`, `nc_n1_alignes`, `nc_n2`.
- Certaines simulations écrivent encore dans la figure ce que la colonne de démonstration écrit (ex. `national.html
  ?vue=n24_points` : « (uₙ) décroissante (question 2) ») : la figure devrait seulement allumer.
- Les copies `frontend/public/media/examens/mathematiques/*.json` (lues par la feuille) sont suivies par git ; celles de
  2016 N, 2019 N, 2022 R et 2023 R ont été recopiées après la correction d'`exam.json` (`scripts/examens/copier_sujets.py`).
- ch3 2021 N : la feuille montre et la voix lit la question 4.b (ln) avant le chapitre ln (tel qu'à l'examen).
- Énoncés lus en entier sauf la fin des problèmes 2019 N et 2021 N et la question 3 de 2024 N ex. 3 / 2023 R ex. 3
  (« on la lira plus tard ») ; la feuille, elle, montre tout l'exercice.
