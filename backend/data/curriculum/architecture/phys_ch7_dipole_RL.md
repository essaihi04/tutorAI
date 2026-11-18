# Architecture du cours `phys_ch7_dipole_RL` — Dipôle RL

Refaite le 18 novembre 2026 (skill `logique-de-cours`). Le cours en ligne n'est pas touché. La nouvelle version est dans `backend/data/courses/en_attente/phys_ch7_dipole_RL.json`. Les pistes à mettre en voix sont dans `phys_ch7_dipole_RL_voix.json`.

## La logique avant

Le cours en ligne compte 55 diapositives en 5 séances :

1. outils, bobine, deux lampes ;
2. u_b = L·di/dt + r·i ;
3. montage et établissement ;
4. l'équation (`rl_e1`, `rl_e2`, `rl_e3` expliquent chacune une ligne) ;
5. la solution, τ, l'effet de L et de R ;
6. la rupture ;
7. la **lecture de τ** (tangente, 63 %), r, L, la droite, u_b(t) ;
8. l'énergie ;
9. les nationaux ;
10. le bilan.

Il y avait trois défauts :

1. **L'effet de L et de R n'était vu qu'après la solution** (`rl_s7`, `rl_s8`). Il n'était jamais manipulé avant l'équation.
2. **τ était lu (tangente, 63 %), puis r et L étaient trouvés, seulement après la rupture.** Les cours écrits et le RC refait le font juste après τ. Or « lire τ, puis trouver L » est le cas le plus fréquent du chapitre : 9 sessions sur 10 avec RL.
3. **L'équation était dite par la voix**, une ligne par diapositive, sans que l'élève l'écrive.

La séance 2 mêlait aussi u_b et le montage. Les coupures de séance laissaient `rl_s1_forme` (« la séance d'avant ») bien placé : c'est gardé.

## La logique après

Le cours compte 59 diapositives (4 nouvelles) en 6 séances. C'est **la même ossature que le RC refait** :

- outils, bobine et lampes ;
- tension de la bobine ;
- **III. Le montage** : ce qu'on voit (`rl_m1`–`rl_m4`), puis ce qu'on règle (**`rl_m5_observer`**, curseurs L et R) ;
- **IV. L'équation, écrite par l'élève** : `rl_e0a` → `rl_e1`, `rl_e0b` → `rl_e2`, `rl_e0c` → `rl_e3`. Chaque étape est écrite par l'élève, puis corrigée et expliquée par la diapositive qui existait. Viennent ensuite les formes, u_R, u_b et deux questions du national ;
- **V. La solution** (la séance 4 commence à `rl_rp4`, car `rl_s1` dit « la séance d'avant ») ;
- **VI. τ : le calculer, puis le lire** : dimension, 63 % calculé, tangente, 63 % lu, L puis R chiffrés, r, L, la droite, u_b(t) ;
- **VII. La rupture : la voir, l'écrire, la résoudre** ;
- puis l'énergie, les nationaux, le bilan.

**Ce qui reste, et pourquoi.**
- L'expérience des deux lampes et le courant triangulaire (pour voir que u_b suit la pente) restent avant le montage, comme dans tous les cours écrits.
- La solution sous ses deux formes (A(1 − e^(−t/τ)) et A + B·e^(−t/τ)) reste, avec la condition initiale.
- La rupture reste après l'établissement, comme partout.
- Les diapositives déplacées gardent leur voix. Aucune voix existante n'est réécrite.
- `rl_s8_R` perd seulement son observation, qui passe à `rl_m5` (même énoncé, mêmes indices et mêmes voix). Le repère `courbe_R` y devient `courbe_2`.

## Fréquence au national (10 sessions RL sur 20, exploration `cas_types`)

| Cas type | Sessions | Où |
|---|---|---|
| lire τ sur la courbe | 9 | `rl_s6`, `rl_l1`, `rl_l2` (juste après τ) |
| trouver L à partir de τ | 9 | `rl_l4`, `rl_e7`, `rl_n1` |
| établir l'équation en i | 6 | `rl_e0a`–`rl_e0c` (écrite par l'élève), `rl_e1`–`rl_e3`, `rl_e7` |
| régime permanent I₀ ou U_R | 6 | `rl_m4`, `rl_e8` |
| trouver r | 5 | `rl_b10`, `rl_e8`, `rl_l3` |
| équation en u_R ; vérifier la solution, A et τ | 4 chacun | `rl_e5` ; `rl_s1`–`rl_s4c` |
| énergie ; schéma et branchement | 4 chacun | `rl_l7`, `rl_l8` ; `rl_m1` |
| identifier une courbe | 3 | `rl_e8`, `rl_s7` |
| rupture, diode | 2 | `rl_t1`–`rl_t4` |
| droite di/dt = f(i), u_b(t) | 1 à 2 | `rl_l5`, `rl_l6` |

## Animations et exercices animés

- **`dipole-rl-tableau/observer.html`** (nouveau) : circuit peint (générateur, interrupteur, résistor, bobine de cuivre). Deux curseurs, L (0,06–0,24 H) et R (20–110 Ω). La courbe i(t) se trace au ralenti vers le palier I₀ écrit, et la courbe d'avant reste en pointillés. Les moments sont `courbe`, `L_double` et `R_double`. `conclusions: false` tait la comparaison écrite. Rien de τ n'est écrit.
- **Étapes de l'équation** : `circuit-rl.html?vue=montage&etape=1|2|3`, arrêtées sur `fleches`.
- **Nationaux** (2020 N, 2021 R, 2019 R, 2025 R, 2016 R, 2022 R, 2024 N) : déjà joués par `figures.html`, un moment par question. Ils sont gardés.

## Les trois cours se répondent

RC, RL et RLC suivent maintenant la même ossature. L'élève reconnaît chaque étape d'un chapitre à l'autre :

| Étape | Dipôle RC | Dipôle RL | Circuit RLC |
|---|---|---|---|
| 1. Les outils, puis le dipôle | rappels, condensateur, q = C·u_C, i = C·du_C/dt | rappels, bobine, deux lampes, u_b = L·di/dt + r·i | rappels q = C·u_C et u_b, décharge dans une bobine |
| 2. Le montage : ce qu'on voit, **ce qu'on règle** | `rc_m1`–`rc_m4`, puis **`rc_m5_observer`** (curseurs R, C) | `rl_m1`–`rl_m4`, puis **`rl_m5_observer`** (curseurs L, R) | `lc_r1`–`lc_r4` (curseur R + r), puis **`lc_r5_observer`** (curseurs L, C) |
| 3. L'équation, **écrite par l'élève ligne par ligne** | `rc_e2a`, `rc_e2b`, `rc_e2c`, puis la rédaction complète `rc_e2` | `rl_e0a`→`rl_e1`, `rl_e0b`→`rl_e2`, `rl_e0c`→`rl_e3` | `lc_e0a`→`lc_e1`, `lc_e0b`→`lc_e2`, `lc_e0c`→`lc_e3` |
| 4. La solution | dériver, remplacer, factoriser, condition initiale | idem | cosinus, T₀ = 2π√(LC), U_m et φ |
| 5. La constante de temps (période propre) : **la calculer, puis la lire** | τ = RC, puis la tangente et les 63 % juste après | τ = L/(R + r), puis la tangente et les 63 % juste après | T₀, sa dimension, L et C ; lecture sur l'oscillogramme |
| 6. Le retour à zéro : **voir, écrire, résoudre** | la décharge | la rupture | l'amortissement (dE/dt), puis l'entretien |
| 7. L'énergie, le national, le bilan | ½·C·u_C² | ½·L·i² | échange, perte, entretien |

Les trois scènes « ce qu'on règle » ont la même allure : le circuit peint à gauche, la courbe à droite, deux curseurs, et la courbe précédente en pointillés.

**L'élève écrit chaque ligne de l'équation.** La voix nomme l'outil (additivité ; loi d'Ohm et relation du dipôle ; on range). L'élève écrit la ligne dans son cahier, puis au tableau. C'est une question libre, jugée sur l'`attendu`. La démonstration corrige ensuite ligne par ligne. Puis vient la diapositive qui existait déjà et qui explique la même ligne autrement. Dans le RC, c'est la rédaction complète `rc_e2_etablir`. Dans le RL et le RLC, ce sont `e1`, `e2` et `e3`.

**Exception à la règle « un tableau par bloc », validée par l'utilisateur le 18 novembre 2026 (« une question par ligne »).** Dans le bloc de l'équation différentielle, chaque ligne que l'élève écrit lui-même garde sa propre question au tableau : `rl_e0a_additivite`, `rl_e0b_remplacer`, `rl_e0c_ranger`. Raison : laisser l'élève trouver seul, une étape à la fois, sa réponse avant la correction (demande du 18/11, plus récente que la règle du 13 novembre). Ailleurs dans le cours, la règle « un tableau par bloc » ne change pas.

**Rien de ce qui vient plus tard n'est écrit avant l'équation** (règle 27) :
- `tau-rc.html?avant=1` n'écrit ni τ, ni les 63 %, ni 5τ. Il dit seulement « charge plus lente / plus rapide, même E ».
- `dipole-rl-tableau/observer.html` écrit le palier I₀ (vu en `rl_m4`), mais pas τ.
- `circuit-rlc-tableau/observer.html` écrit T, la pseudo-période vue en `lc_r1`, mais pas la formule 2π√(LC).

## Sources consultées (communes)

- **Profs en vidéo.** Exploration `backend/data/curriculum/exploration/dipole_RC.json` : 9 professeurs audités, avec les convergences, les cas types et les commentaires d'élèves. Exploration `dipole_RL.json` : aucune vidéo auditée (YouTube bloqué), mais les 10 sessions nationales RL y sont analysées. Le RLC n'a pas d'exploration.
- **Cours écrits marocains**, lus le 18/11 (texte extrait des PDF) :
  - Naceiri Mrabti (cours P6, P7 et fin du RLC) ;
  - El Founani (TelmidTice, RC et RL) ;
  - Ismaili-Alaoui (kezakoo, RC, RL, RLC) ;
  - Chriki (Moutamadris, résumés 6, 7, 8) ;
  - Hajji (Moutamadris, RL, RLC) ;
  - Aryani (physiqueacademy, RC) ;
  - Moutamadris (cours RC n° 2, RLC n° 5) ;
  - kezakoo (leçon 8 RLC) ;
  - comparaison française : physagreg (TS chap. 6 et 7).
  - Pas lisibles : AlloSchool (PDF scannés), dreamjob, monstrepc.
  - Audits déjà faits sur 5 cours écrits par chapitre : `docs/audit-prof/physique.md` (Naceiri, Chriki, Delahi, manuel TS, Sbiro, Hajji).
- **Cadre :** `cadre_reference_2bac_pc.json` (fiches `dipole_RC`, `dipole_RL`, `circuit_RLC`), `physique.json`, `perimetre.json`.
- **National :** les 20 sujets PC 2016-2025 (`backend/data/exams/physique/`). Leurs fréquences sont dans les `cas_types` des explorations et dans les fiches du cadre.

## Ordre commun des profs, et nos écarts

- **La courbe d'abord, l'équation ensuite.** C'est le cas chez Aryani, El Founani, Naceiri, Moutamadris, physagreg, Hajji et kezakoo (RLC). Ismaili-Alaoui va directement aux équations. Nous suivons la majorité. Nous ajoutons la manipulation au curseur (demande du 18/11) : chez Naceiri, l'influence de R et de C est déjà vue dès l'étude expérimentale.
- **Puis l'équation, la solution, τ et sa lecture**, la tangente et les 63 % venant juste après τ (tous les cours écrits). Le RC et le RL en ligne lisaient τ seulement après la décharge ou la rupture : c'est corrigé.
- **La décharge ou la rupture « même schéma »** : on la voit, on l'écrit, on la résout, puis on lit les 37 % (El Founani, Naceiri, Chriki, Ismaili-Alaoui).
- **L'énergie à la fin** (majorité). Moutamadris n° 2 la met avant le RC : c'est une variante, pas suivie.
- **RLC :** expérience, régimes, équation, LC idéal (solution, T₀, dimension, U_m et φ), énergie (LC puis RLC), entretien (Hajji, kezakoo, Ismaili-Alaoui, Moutamadris n° 5). Notre cours avait déjà cet ordre.
- **Hors cadre, laissé de côté :**
  - le régime critique et les « sous-régimes » apériodiques (Hajji, kezakoo, Moutamadris n° 5) ;
  - la « résistance négative » et le montage de l'amplificateur (Naceiri, Moutamadris) ;
  - la durée 5τ démontrée par ln 0,01 (Aryani) ;
  - le cas τ = L/R traité seul avant r ≠ 0 (El Founani) : le cadre écrit directement τ = L/(R + r).

## Séances (40 à 50 min, trois blocs)

| Séance | Blocs (diapositives) |
|---|---|
| Séance 1 — Les outils, la bobine, l’expérience des deux lampes | **Les outils : loi d’Ohm et additivité** (o1_carte, rp1_ohm, rp2_additivite) ; **La dérivée ; la bobine ; le principe des deux lampes** (rp3_derivee, b1_bobine, b2a_principe) ; **Les deux lampes : retard, régime permanent, continuité de i** (b2_lampes, b3_egal, b4_ouverture, b5_continuite) |
| Séance 2 — u_b = L·di/dt + r·i ; voir l’établissement, régler L et R | **u_b = L·di/dt + r·i** (b6_triangle, b7_inductance, b8_reelle, b9_segments, b10_national) ; **Le dipôle RL soumis à un échelon : ce qu’on voit, ce qu’on règle** (m1_montage, m2_fermeture, m3_regimes, m4_I0, m5_observer) ; **L’équation, une ligne à la fois : additivité et remplacement** (e0a_additivite, e1_additivite, e0b_remplacer, e2_remplacer) |
| Séance 3 — Ranger l’équation, ses formes, u_R, u_b, deux nationaux | **Ranger l’équation et la reconnaître dans les énoncés** (e0c_ranger, e3_equation, e4_formes) ; **L’équation en u_R, u_b au début et à la fin** (e5_uR, e6_ub) ; **Deux questions du national** (e7_2021R, e8_2019R) |
| Séance 4 — L’exponentielle, la solution, τ : le calculer et le lire | **L’exponentielle, la forme de la solution, sa dérivée, τ** (rp4_exponentielle, s1_forme, s2_deriver, s3_tau) ; **A = I₀, l’autre écriture A + B·e^(−t/τ) et la condition initiale** (s4_A, s4b_forme, s4c_condition) ; **τ est un temps ; 63 % ; le lire par la tangente et les 63 %** (s5_dimension, s6_pourcent, l1_tangente, l2_pourcent) |
| Séance 5 — L et R, trouver r et L, les courbes, puis la rupture | **L puis R ; trouver r et L** (s7_L, s8_R, l3_r, l4_L) ; **La droite di/dt = f(i) et la courbe u_b(t)** (l5_droite, l6_ub) ; **La rupture : la voir, l’écrire, la résoudre** (t1_rupture, t2a_verifier, t2_descente) |
| Séance 6 — Étincelle et diode, l’énergie, puis le national 2023 N joué pas à pas | **Étincelle, diode et le national 2025 R** (t3_diode, t4_national) ; **L’énergie magnétique** (l7_energie, l8_double) ; **2023 N : le sujet, l’équation, la solution** (np0_sujet, np1_equation, np2_remplacer, np3_constantes) |
| Séance 7 — La fin du 2023 N, deux sujets complets, le bilan | **2023 N : I₀, puis τ par la tangente et par les 63 %, L** (np4_lire, np5_tangente, np6_pourcent, np7_L) ; **2023 N : u_b(t), l’énergie, la copie complète** (np8_ub, np9_energie, np10_copie) ; **Deux sujets du national, puis le bilan** (n1_2022R, n2_2024N, bl_fiche, cr_carte) |


## Diapositive par diapositive
#### I. Les outils, la bobine et les deux lampes

| Diapositive | Titre | Visuel | À toi | Pourquoi ici |
|---|---|---|---|---|
| `rl_o1_carte` | La carte du chapitre : une bobine qui freine le courant | carte.html |  | Plan du chapitre, même ossature que le RC. |
| `rl_rp1_ohm` | Rappel : la loi d’Ohm | rappels.html?vue=ohm |  | Départ de zéro : Ohm, additivité, dérivée servent dans l'équation (règle 6). |
| `rl_rp2_additivite` | Rappel : la loi d’additivité des tensions | rappels.html?vue=additivite&dipole=bobine | QCM | 1re ligne de toute équation du RL. |
| `rl_rp3_derivee` | Rappel : la dérivée, c’est une pente | rappels.html?vue=derivee |  | di/dt : la bobine est bâtie sur la dérivée. |
| `rl_b1_bobine` | La bobine : un fil enroulé | bobine.html?vue=objet |  | Définition de la bobine (L, r), cadre RL1, tous les profs. |
| `rl_b2a_principe` | Deux branches presque pareilles | lampes.html | QCM | Règle 33 : principe des deux lampes avant l'expérience. |
| `rl_b2_lampes` | Deux lampes, une surprise | lampes.html | observation | Expérience des deux lampes (tous les cours écrits) ; observation de la lampe en retard. |
| `rl_b3_egal` | À la fin, le même éclat | lampes.html | QCM | Régime permanent : la bobine = sa résistance r. |
| `rl_b4_ouverture` | On ouvre K : un retard aussi | lampes.html |  | Le retard aussi à l'ouverture (rupture préparée). |
| `rl_b5_continuite` | Auto-induction et continuité de i | lampes.html |  | Auto-induction, continuité de i (RL2). |

#### II. La tension aux bornes d'une bobine

| Diapositive | Titre | Visuel | À toi | Pourquoi ici |
|---|---|---|---|---|
| `rl_b6_triangle` | Un courant en triangle | triangle.html |  | Courant triangulaire : VOIR que u_b suit la pente (Hajji, physagreg ; TP officiel). |
| `rl_b7_inductance` | u_b = L·di/dt | triangle.html |  | u_b = L·di/dt tiré de la manip. |
| `rl_b8_reelle` | La bobine réelle : u_b = L·di/dt + r·i | bobine.html?vue=mesure |  | Bobine réelle u_b = L·di/dt + r·i (RL1). |
| `rl_b9_segments` | Calculer u_b sur une courbe | figures.html?fig=fig_segments |  | Calculer u_b sur une courbe i(t). |
| `rl_b10_national` | Exercice du national : la bobine en régime permanent | figures.html?fig=fig_2020N | QCM | 2020 N : r par u_b en régime permanent. |

#### III. Le montage : ce qu'on voit, ce qu'on règle

| Diapositive | Titre | Visuel | À toi | Pourquoi ici |
|---|---|---|---|---|
| `rl_m1_montage` | Le montage RL | circuit-rl.html?vue=montage | QCM | Le montage RL ; i vu par u_R (RL3). |
| `rl_m2_fermeture` | On ferme K : ce qu'on voit | circuit-rl.html?vue=etablissement |  | Première vue de l'établissement, AVANT l'équation (ordre des cours écrits). |
| `rl_m3_regimes` | Régime transitoire, régime permanent | courbe.html?vue=trace |  | Régimes nommés sur la courbe. |
| `rl_m4_I0` | La valeur finale I₀ | courbe.html?vue=trace |  | La valeur finale I₀ = E/(R + r) (6 sujets). |
| `rl_m5_observer` | L et R au curseur : le courant plus lent ou plus rapide ? | observer.html | observation | NOUVELLE. Demande du 18/11 : L et R au curseur avant l'équation, comme rc_m5 ; l'observation « R augmente » (venue de rl_s8) laisse l'élève trouver le palier plus bas. τ pas encore écrit. |

#### IV. L'équation différentielle, écrite pas à pas

| Diapositive | Titre | Visuel | À toi | Pourquoi ici |
|---|---|---|---|---|
| `rl_e0a_additivite` | À toi : la première ligne | circuit-rl.html?vue=montage&etape=1 | écrit | NOUVELLE. L'élève écrit la 1re ligne ; rl_e1 la corrige juste après. |
| `rl_e1_additivite` | Loi d'additivité | circuit-rl.html?vue=montage |  | Gardée : correction expliquée de la 1re ligne (flèches, convention récepteur). |
| `rl_e0b_remplacer` | À toi : remplacer u_R et u_b | circuit-rl.html?vue=montage&etape=2 | écrit | NOUVELLE. L'élève remplace u_R et u_b (piège : oublier r·i, 1re perte de points selon les corrigés). |
| `rl_e2_remplacer` | Remplacer chaque tension | circuit-rl.html?vue=montage | QCM | Gardée : correction expliquée ; sa question sur r·i reste (la voix la pose). |
| `rl_e0c_ranger` | À toi : ranger l'équation | circuit-rl.html?vue=montage&etape=3 | écrit | NOUVELLE. L'élève range l'équation ; rl_e3 corrige. |
| `rl_e3_equation` | L'équation différentielle | figures.html?fig=fig_ed |  | Gardée : l'équation de l'établissement, rangée (6 sujets). |
| `rl_e4_formes` | Les formes des énoncés | figures.html?fig=fig_ed_formes |  | Les formes des énoncés (2021 R, 2024 N). |
| `rl_e5_uR` | L'équation en u_R | figures.html?fig=fig_ed_uR |  | Équation en u_R (4 sujets). |
| `rl_e6_ub` | u_b au début et à la fin | courbe.html?vue=ub |  | u_b au début (E) et à la fin (r·I₀) : continuité de i. |
| `rl_e7_2021R` | Exercice du national : établir l'équation | figures.html?fig=fig_2021R |  | National 2021 R joué : établir l'équation. |
| `rl_e8_2019R` | Exercice du national : quelle courbe est u_R ? | figures.html?fig=fig_2019R | QCM | National 2019 R : quelle courbe est u_R. |

#### V. La solution

| Diapositive | Titre | Visuel | À toi | Pourquoi ici |
|---|---|---|---|---|
| `rl_rp4_exponentielle` | Rappel : la fonction exponentielle | rappels.html?vue=exponentielle |  | Ouvre la séance de la solution (sa voix suit « la séance d'avant » de rl_s1) : l'exponentielle juste avant son usage. |
| `rl_s1_forme` | La forme de la solution | courbe.html?vue=trace | QCM | Forme de la solution lue sur la courbe ; dit « la séance d'avant » : la séance 4 commence à rl_rp4. |
| `rl_s2_deriver` | Dériver la solution | figures.html?fig=fig_derivee_exp |  | Dériver la solution. |
| `rl_s3_tau` | Remplacer et identifier τ | figures.html?fig=fig_resolution |  | Remplacer, identifier τ = L/(R + r). |
| `rl_s4_A` | Identifier A | figures.html?fig=fig_resolution |  | Identifier A = I₀. |
| `rl_s4b_forme` | L'autre écriture : i(t) = A + B·e^(−t/τ) | courbe.html?vue=trace |  | Forme A + B·e^(−t/τ) des corrigés. |
| `rl_s4c_condition` | La condition initiale donne B | courbe.html?vue=trace |  | La condition initiale i(0) = 0 donne B. |

#### VI. La constante de temps : la calculer, la lire

| Diapositive | Titre | Visuel | À toi | Pourquoi ici |
|---|---|---|---|---|
| `rl_s5_dimension` | τ est un temps | figures.html?fig=fig_dimension | QCM | Ouvre la partie τ : τ est un temps. |
| `rl_s6_pourcent` | 63 % à τ, presque tout à 5τ | courbe.html?vue=pourcent |  | 63 % calculé à τ (règle 37). |
| `rl_l1_tangente` | τ par la tangente à l'origine | courbe.html?vue=tangente |  | DÉPLACÉE ici (était après la rupture) : τ lu à la tangente aussitôt calculé ; 9 sujets demandent τ. |
| `rl_l2_pourcent` | τ par les 63 % | courbe.html?vue=pourcent |  | DÉPLACÉE : τ lu à 63 %, juste après la tangente. |
| `rl_s7_L` | Si L double | influence.html?vue=L |  | Gardée : effet de L chiffré par τ (2e explication ; la 1re est rl_m5). |
| `rl_s8_R` | Si R augmente | influence.html?vue=R |  | Gardée : effet de R chiffré ; son observation est passée à rl_m5. |
| `rl_l3_r` | Trouver r | figures.html?fig=fig_r_L |  | DÉPLACÉE : trouver r (5 sujets) une fois τ et I₀ lus. |
| `rl_l4_L` | Trouver L | figures.html?fig=fig_r_L | QCM | DÉPLACÉE : trouver L = τ·(R + r) (9 sujets). |
| `rl_l5_droite` | La droite di/dt = f(i) | droite.html |  | DÉPLACÉE : la droite di/dt = f(i) (2024 N). |
| `rl_l6_ub` | La courbe u_b(t) | courbe.html?vue=ub |  | DÉPLACÉE : la courbe u_b(t) (2018 R, 2023 N). |

#### VII. La rupture du courant : voir, écrire, résoudre

| Diapositive | Titre | Visuel | À toi | Pourquoi ici |
|---|---|---|---|---|
| `rl_t1_rupture` | La rupture du courant | circuit-rl.html?vue=rupture |  | Rupture vue et mise en équation après l'établissement, comme tous les cours écrits. |
| `rl_t2a_verifier` | Vérifier la solution de la rupture | figures.html?fig=fig_ed_rupture |  | Vérifier la solution de la rupture (audit des cours écrits). |
| `rl_t2_descente` | i descend : 37 % à τ | rupture.html?vue=descente |  | 37 % sur la descente. |
| `rl_t3_diode` | Étincelle et diode | rupture.html?vue=diode |  | Étincelle et diode (2025 R). |
| `rl_t4_national` | Exercice du national : la rupture avec diode | figures.html?fig=fig_2025R | QCM | National 2025 R joué. |

#### VIII. L'énergie magnétique

| Diapositive | Titre | Visuel | À toi | Pourquoi ici |
|---|---|---|---|---|
| `rl_l7_energie` | L'énergie de la bobine | energie.html?vue=barre |  | Énergie à la fin (RL8), comme partout. |
| `rl_l8_double` | Si I₀ double | energie-carre.html | QCM | Si I₀ double : manip energie-carre.html. |

#### IX. Deux sujets du national

| Diapositive | Titre | Visuel | À toi | Pourquoi ici |
|---|---|---|---|---|
| `rl_n1_2022R` | Sujet national 2022 R | figures.html?fig=fig_2022R |  | Sujet complet 2022 R. |
| `rl_n2_2024N` | Sujet national 2024 N : la droite | figures.html?fig=fig_2024N | QCM | Sujet complet 2024 N (la droite). |

#### X. Bilan du chapitre

| Diapositive | Titre | Visuel | À toi | Pourquoi ici |
|---|---|---|---|---|
| `rl_bl_fiche` | Ce qu'il faut retenir | bilan.html |  | Fiche bilan avec les trous de l'élève. |
| `rl_cr_carte` | La carte du dipôle RL | carte.html |  | Carte du dipôle RL. |

## Vérifications faites

- La copie en attente se charge. `docs/audit-prof/outils/verif_attente.py` donne : 0 mot de pointage absent, 0 diapositive hors bloc, 0 doublon. Les 4 diapositives sans voix sont les nouvelles.
- `scripts/voix/verifier_mots.py` sur chaque piste nouvelle : aucun mot darija rare. Il reste seulement des mots du programme et des unités, que les cours en ligne disent déjà (liste `a_ecouter` du fichier des voix).
- `scripts/verifier_formules.py` : 0 relation écrite à plat.
- `backend/scripts/verifier_pointage_simulations.py` sur les diapositives nouvelles : aucun écart de repère, de moment, d'iframe ni de départ. Les avertissements « GESTE » viennent seulement de l'absence de piste : sans durée, tous les gestes tombent à 0 s. Ils sont à relancer après la voix.
- Les trois animations : chargées dans Chromium, sans erreur console, avec la comparaison écrite après un `play_until`.

## Ce qui reste à faire (hors de cette session)

- **Les voix**, sur le VPS (voix Bodi), une fois le quota Kaggle revenu : les pistes `pistes` du fichier `_voix.json`. Ensuite, poser les pistes, relancer le contrôle du pointage avec les vraies durées, puis remplacer le cours en ligne par la copie en attente.
- **Les réactions préparées** des questions écrites : aucune. Une réponse libre est jugée en direct, sur l'`attendu`.
- **Aucun fichier partagé n'a été modifié** (ni `shared/`, ni `frontend/src/`). Il n'y a aucun besoin côté lecteur.

<!-- 2e passe : début -->
## 2ᵉ passe (18 novembre 2026) : le national joué pas à pas

### Ce qui manquait (évaluation de la 1ʳᵉ passe)
Les sujets du national (`rl_n1_2022R`, `rl_n2_2024N`, `rl_e7`, `rl_e8`, `rl_t4`) se jouaient avec la voix qui donnait
chaque réponse ; aucun n'était fait par l'élève étape par étape, en particulier « vérifier la solution, trouver A, B et τ »
(4 sessions) et la lecture de τ (9 sessions).

### Ce qui est ajouté : le national 2023 N, partie 1, joué pas à pas (11 diapositives)
Corrigé lu le 18/11 : E = 24 V, r négligeable, I₀ = 48 mA, τ = 2 ms, R = 500 Ω, L = 1 H, u_L(t) = 24·e^(−500·t)
(écrite u_b, la notation du cours, « notée u_L dans le sujet »). Le cours ne l'utilisait pas (le RLC n'en garde que la
partie LC, `lc_l4_2023`). Mêmes étapes, dans le même ordre, que le RC 2022 N ; deux questions ajoutées : les 63 % et
l'énergie ½·L·I₀² ≈ 1,2 mJ. Placé après l'énergie magnétique, avant les deux sujets complets.

**La règle suivie à chaque étape** (demande du 18 novembre : « simple, animé, expliqué ; ne pas tout donner au départ ; laisser
à l'élève le temps de trouver seul ») :
1. la voix confirme la correction de l'étape d'avant pendant qu'elle se construit au tableau (moment `rappel` : la tangente
   se trace, la ligne du tableau d'avancement s'écrit, la réponse s'ajoute dans « Ta copie ») ;
2. elle pose UNE question (moment `question`) en nommant l'outil, jamais le résultat ; la simulation écrit la question
   et « … à toi d'abord » : la réponse reste cachée (`conclusions` faux par défaut) ;
3. l'élève répond (question ouverte jugée sur l'`attendu`, ou QCM avec ses réactions préparées) ;
4. la démonstration écrit la correction ligne par ligne, comme le barème la lit (relation, conversion, application
   numérique, résultat avec son unité) ; la diapositive suivante la redessine au tableau (étape 1).
Une diapositive par étape (`?etape=k`) : l'iframe se recharge et s'ouvre sur son état (règle 39). Les formules sont écrites
en notation (fractions superposées au tableau), les unités dites en mots dans la voix.

**Règle « un tableau par bloc ».** Dans cette partie, chaque étape porte sa question : c'est la demande du 18 novembre
(« la réponse de l'élève avant la correction »), plus récente que la règle du 13 novembre. Ailleurs, elle ne change pas.
Les questions ouvertes n'ont pas de réaction préparée : elles sont jugées en direct sur l'`attendu`, comme `rc_e2a`.

**La simulation** `national-pas-a-pas.html` (nouvelle, dans le dossier du cours) et son moteur `pas-a-pas.js` (une copie
par dossier de cours, aucun fichier partagé modifié) : figure du sujet à gauche (circuit peint avec les flèches de la
convention récepteur, courbes tracées à la craie, tableau d'avancement), « Ta copie » à droite. Moments : `enonce`,
`courbe`, `rappel`, `question`, `correction` ; vue `sujet` : `donnees`, `questions` ; `?etape=fin` : la copie complète.
Vérifiée dans Chromium à 1280 × 640 et 724 × 350 (téléphone en paysage) : aucune erreur, aucun texte hors cadre, texte ≥ 15 px
(plancher du kit), fractions sans chevauchement.

#### IX. Le national 2023 N, joué pas à pas

| Diapositive | Titre | Visuel | À toi | Pourquoi ici |
|---|---|---|---|---|
| `rl_np0_sujet` | Le national 2023 N : lire le sujet deux fois | national-pas-a-pas.html?sujet=rl2023n&etape=sujet |  | Règle 6 du professeur : le sujet lu deux fois (de quoi parle-t-il ? puis les données et ce qu'on cherche) avant tout calcul ; aucune question notée. |
| `rl_np1_equation` | 2023 N, étape 1 : l'équation différentielle | national-pas-a-pas.html?sujet=rl2023n&etape=1 | écrit | Cas type « établir l'équation en i » (6 sessions), la démarche de `rl_e0a`–`rl_e0c` sur un sujet. |
| `rl_np2_remplacer` | 2023 N, étape 2 : dériver et remplacer | national-pas-a-pas.html?sujet=rl2023n&etape=2 | écrit | Cas type « vérifier la solution » (4 sessions) : dériver, remplacer, regrouper — une étape seule. |
| `rl_np3_constantes` | 2023 N, étape 3 : τ, A et B | national-pas-a-pas.html?sujet=rl2023n&etape=3 | écrit | Identifier « pour tout t », puis la condition initiale : B séparé de A (corrigé du sujet, règle 37). |
| `rl_np4_lire` | 2023 N, étape 4 : lire I₀ | national-pas-a-pas.html?sujet=rl2023n&etape=4 | écrit | Régime permanent I₀ (6 sessions), lu seul avant le calcul de L. |
| `rl_np5_tangente` | 2023 N, étape 5 : τ par la tangente | national-pas-a-pas.html?sujet=rl2023n&etape=5 | écrit | τ graphiquement (9 sessions) : la tangente (T) du sujet, comme dans le RC. |
| `rl_np6_pourcent` | 2023 N, étape 6 : τ par les 63 % | national-pas-a-pas.html?sujet=rl2023n&etape=6 | écrit | Seconde méthode, comme dans le RC (règle 11). |
| `rl_np7_L` | 2023 N, étape 7 : montrer que L = 1 H | national-pas-a-pas.html?sujet=rl2023n&etape=7 | écrit | Trouver L à partir de τ (9 sessions) : L = τ·E/I₀. |
| `rl_np8_ub` | 2023 N, étape 8 : l'expression de u_b(t) | national-pas-a-pas.html?sujet=rl2023n&etape=8 | écrit | Question 1-3 du sujet (u_b(t), « u_L » dans le sujet) : dériver, simplifier L/(R·τ) = 1, écrire en SI. |
| `rl_np9_energie` | 2023 N, étape 9 : l'énergie de la bobine | national-pas-a-pas.html?sujet=rl2023n&etape=9 | écrit | Question ajoutée (énergie : 4 sessions, cadre RL8), parallèle au RC. |
| `rl_np10_copie` | 2023 N : la copie complète | national-pas-a-pas.html?sujet=rl2023n&etape=fin |  | Règle 33 : la copie complète vient après la dernière étape, jamais avant ; chaque réponse se relit comme le barème la lit (relation, application numérique, résultat et unité). |

### Les mots
`python -X utf8 scripts/voix/verifier_mots.py en_attente/phys_ch7_dipole_RL` sur chaque piste nouvelle ou réécrite : plus aucun mot
rare évitable. Remplacés : « milliampères » (0 fois dans le corpus de la voix) → « milliampère » ; « kiloohm(s) » (0) →
« mille ohm » ; « microfarads » (0) → « micro farad » ; « millijoules » (1) → « millijoule » ; « palier » (0) → « la valeur
finale » ; « sommets » (0) → « l'amplitude » ; « quarante-huit », « cinquante-six », « trente-neuf » écrits sans trait
d'union (« quarante huit ») ; en darija, « فارغ » → « خاوي », « نرتبو » → « نكتبو l'équation », « كتوافق » → « كيكون عند »,
« ضاعت » → « dissipée », « كيصحح / كيقراها » → « فالتصحيح » ; au ch9, les réactions de `tl_r6_classer` (« portail », « الراسب »,
« كنحكمو »…) et de `tl_f8_variable` (« تقلقش », « فالتابلو », « quelles »…) sont réécrites. Restent, parce que ce sont des
termes du programme : anri (henry, règle de prononciation : unité du programme), henry (lu « anri » par la règle de prononciation), milliampères, ohms, palier (liste `a_ecouter` du fichier des voix).
Pistes à mettre en voix : 39, dont 30 de la 2ᵉ passe (`phys_ch7_dipole_RL_voix.json`, champ « passe »).

### Vérifications faites (2ᵉ passe)
- Les copies en attente se chargent ; chaque `mot` du pointage et des démonstrations est un extrait exact de sa voix
  (`scripts/logique/outils.py`, `verifier_mots`) ; les blocs suivent l'ordre du cours.
- `python backend/scripts/verifier_pointage_simulations.py <cours> --ecarts` : aucune erreur « introuvable », ni sur la copie
  en attente ni sur le cours en ligne. Les seuls avertissements des nouvelles diapositives sont des « GESTE » : sans piste,
  la durée vaut 0 et tous les gestes tombent au même instant ; à relancer après la voix.
- `cd backend && python -m pytest -q app/tests -k "course or cours or concentration"` (résultat dans le rapport du commit).
- Simulations : Chromium, 1280 × 640 et 724 × 350, chaque étape à `question` puis `correction` : pas d'erreur console,
  aucun texte hors cadre (`__horsCadre` vide), la réponse invisible avant `correction`.

### Ce qui reste à faire (hors de cette session)
- Les voix (Bodi, VPS, quota Kaggle épuisé aujourd'hui) des pistes du fichier `_voix.json`, puis relancer le contrôle du
  pointage avec les vraies durées.
- Les questions ouvertes de l'exercice joué n'ont pas de réaction préparée (jugées en direct sur l'`attendu`).
- Aucun fichier partagé n'a été modifié (`shared/`, `frontend/src/`).
<!-- 2e passe : fin -->

## Fiche bilan lisible au téléphone (18 novembre 2026)

**Défaut ancien corrigé : la fiche « Ce qu’il faut retenir » (`dipole-rl-tableau/bilan.html`, `rl_bl_fiche`).** Sur un
téléphone en paysage, les neuf blocs restaient sur une page en trois colonnes, textes à 4–9 px et blocs les uns sur les
autres : le kit (`shared/tableau/tableau.js`) baisse son plancher jusqu'à 45 % sur un petit tableau et écrit indices et
exposants à 62 % (u_b, I_0, e^{−t/τ} restaient à 9 px même sur ordinateur). La page garde maintenant son propre plancher
de 15 px (sa craie : `tailleMin` à 15, 0 à l'impression ; `_largeur` et `_texteIndices` pour indices et exposants) et se
mesure à la taille vraiment écrite (cadres des formules, interlignes, fractions). Bureau : la disposition d'avant (3 + 3 + 3,
sur toute la largeur), ou toute la hauteur, ou 4 colonnes ; sinon la fiche se partage en parties (autant qu'il faut,
1 à 4 colonnes, chaque partie grossit son texte pour remplir le tableau), compteur « partie n sur N · touche : la suite »
(15 px) ; toucher le tableau passe à la suite, puis à la page de l'élève ; `play_until` vers un bloc ouvre sa partie et
l'éclaire. La page de l'élève montre moins de lignes « à reprendre » (« … et n autre(s) ») si elle ne tient pas.
L'impression passe le canvas en 1280 × 600 le temps des images : la fiche entière sur une feuille.
**Défaut des moments** : tous les blocs valaient 1 et `time_s` vaut 1 sur la fiche ; le kit ignore un `play_until` vers
un moment ≤ `time_s`, donc la voix n'écrivait ni n'éclairait aucun bloc après `start` (vérifié dans Chromium). Valeurs :
`fiche` 1,01, blocs 1,1 à 1,9, `fin` 1,95 (sa dernière partie), `lacunes` 2 (noms, repères, `set_parameters` inchangés).
Mesuré dans Chromium (568 × 300, 724 × 350, 1024 × 560, 1280 × 640, 1596 × 700 ; chaque bloc, `fin`, des lacunes,
la page 2) : avant 4,2 / 4,8 / 9,3 / 9,3 / 16,4 px au plus petit et 104 / 198 / 34 / 0 / 28 chevauchements ; après
15 px au moins partout, aucun chevauchement, rien hors du cadre, chaque bloc s'allume. Parties : 3 (5 avec l'état de
l'élève) à 568, 3 à 724, 2 à 1024, 1 à 1280, 2 à 1596. Pointage et formules : rien de nouveau.
