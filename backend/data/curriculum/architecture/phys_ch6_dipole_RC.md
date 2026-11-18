# Architecture du cours `phys_ch6_dipole_RC` — Dipôle RC

Refaite le 18 novembre 2026 (skill `logique-de-cours`). Le cours en ligne `backend/data/courses/phys_ch6_dipole_RC.json` n'est pas touché. La nouvelle version est dans `backend/data/courses/en_attente/phys_ch6_dipole_RC.json`. Les pistes à mettre en voix sont dans `phys_ch6_dipole_RC_voix.json`.

## La logique avant

Le cours en ligne compte 57 diapositives en 6 séances :

1. outils et condensateur ;
2. associations, charge à courant constant ;
3. montage et courbe de charge ;
4. **toutes les équations** : charge, puis **décharge** (`rc_e6`), puis le tableau des huit équations (`rc_e7`) ;
5. la solution ;
6. τ, puis **la solution de la décharge et sa continuité** ;
7. la **lecture de τ** (tangente, 63 %, 37 %) ;
8. l'énergie ;
9. les nationaux ;
10. le bilan.

Il y avait quatre défauts de logique :

1. **La décharge était mise en équation avant d'être vue.** `rc_e6` écrit RC·du_C/dt + u_C = 0 en séance 3. La bascule n'était montrée qu'en séance 5 (`rc_d2_continuite`). Cela va contre la règle 4 : l'expérience vient avant ce qu'elle prouve.
2. **L'effet de R et de C n'était vu qu'après la solution** (`rc_t2`, `rc_t3`), jamais avant l'équation. Cela va contre la demande du 18/11 : chaque courbe est manipulée avant l'équation.
3. **τ était calculé en séance 4-5, mais lu sur la courbe seulement en séance 6**, après la décharge. Chez tous les profs, la tangente et les 63 % viennent juste après τ = RC.
4. **L'équation différentielle était donnée par la voix** (`rc_e2` : « quatre lignes, toujours dans le même ordre »). L'élève ne l'écrivait pas lui-même.

## La logique après

Le cours compte 61 diapositives (4 nouvelles) en 7 séances.

- Les outils et le condensateur, puis les associations : sans changement.
- **III. Le montage** : ce qu'on voit (`rc_m1`–`rc_m4`), puis ce qu'on règle (**`rc_m5_observer`**, curseurs R et C).
- **IV. L'équation, écrite pas à pas par l'élève** : `rc_e2a`, `rc_e2b`, `rc_e2c`, puis la rédaction complète `rc_e2`. Ensuite les autres formes et les autres grandeurs, puis le national 2023 R.
- **V. La solution.**
- **VI. τ : le calculer, puis le lire** : dimension, tangente, 63 %, effet de R puis de C chiffré, de τ à R et C, courbes sans le temps.
- **VII. La décharge : la voir, l'écrire, la résoudre** : `rc_d2`, puis `rc_e6`, `rc_d1`, `rc_d3`, les 37 % (`rc_l3`), et enfin le tableau des huit équations (`rc_e7`).
- Puis l'énergie, les nationaux, le bilan.

**Ce qui reste, et pourquoi.**
- Les rappels de départ (règle 6) sont gardés.
- Les associations et la charge à courant constant restent avant le dipôle RC : la majorité des profs fait ainsi, et le cadre RC3 et 3 sujets (2018 N, 2020 R, 2025 N) les demandent.
- La méthode « dériver, remplacer, factoriser, condition initiale » reste : 7 profs sur 9 l'utilisent.
- Les deux sujets complets restent à la fin, avant le bilan.
- Toutes les diapositives seulement déplacées gardent leur id, leur texte et leur voix.

**Ce qui est réécrit.**
- `rc_e2_etablir` : seulement le titre et le sous-titre (« La rédaction complète, comme le corrigé »). La voix ne change pas.
- `rc_t2_influence` : son observation « R a doublé » passe à `rc_m5`, où l'élève voit l'effet pour la première fois. La voix ne change pas.

## Fréquence au national (20 sujets PC 2016-2025, exploration `cas_types`)

| Cas type | Sujets | Où |
|---|---|---|
| déterminer τ sur une courbe (tangente, 63 %, 37 %) | 8 | `rc_l1`, `rc_l2` (juste après τ), `rc_l3` |
| en déduire R, C ou E | 9 | `rc_l4`, `rc_n1`, `rc_n2` |
| trouver A et τ (ou α, B) | 5 | `rc_s2`–`rc_s5` |
| établir l'équation de u_C | 4 | `rc_e2a`–`rc_e2c` (écrite par l'élève), `rc_e2`, `rc_e3` |
| équation de q, de u_R, de i | 4 | `rc_e4`, `rc_e5`, `rc_e8` |
| charge à courant constant | 3 | `rc_g1`, `rc_g2` |
| expression de i(t) ou de I₀ | 3 | `rc_s7` |
| du_C/dt = f(u_C), q = f(u) | 2 | `rc_l5`, `rc_l6` |
| décharge, association, énergie, branchement de l'acquisition | 1 chacun | `rc_e6`, `rc_a1`, `rc_l8`, `rc_m2` |

Le temps va donc à τ et à sa lecture (le cas le plus fréquent) et à l'équation écrite par l'élève.

## Animations et exercices animés

- **`tau-rc.html?avant=1`** (nouveau mode du fichier du chapitre, sans effet sur `rc_t2` et `rc_t3`) : curseurs R et C. La courbe d'avant reste en pointillés. Rien de τ n'est écrit. `conclusions: false` tait « charge plus lente » pendant l'observation.
- **Étapes de l'équation** : `circuit-rc.html?vue=montage&etape=1|2|3`. Ce sont trois URL distinctes, pour que l'iframe se recharge (règle 39). La scène s'arrête sur `fleches` : le circuit fléché en convention récepteur, sans l'équation.
- **Nationaux** : `rc_g2` (2025 N), `rc_e8` (2023 R), `rc_l5` (2021 N), `rc_l6` (2018 N), `rc_n1` (2019 N) et `rc_n2` (2021 R) se jouent déjà étape par étape. `figures.html` et `generateur-courant.html` ont un moment par question, et la courbe se trace à la craie avant la lecture. Ils sont gardés tels quels.

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

**Règle « un tableau par bloc ».** Dans ce seul bloc de l'équation, chaque ligne a son tableau. C'est la demande du 18 novembre (« l'élève écrit chaque étape avant la correction »), plus récente que la règle du 13 novembre (« un tableau par bloc »). Ailleurs, la règle ne change pas.

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
| Séance 1 — Les bases d’électricité, puis le condensateur | **Les bases : le courant et la tension** (o1_carte, rp1_courant, rp2_tension) ; **Les bases : loi d’Ohm, additivité, puissances de dix** (rp3_ohm, rp4_additivite, rp5_puissances) ; **Le condensateur et sa charge, vue sur les appareils** (c1_plaques, c2a_principe, c2_aiguilles) |
| Séance 2 — q = C·u_C, la dérivée, i = C·du_C/dt, les associations | **Les électrons, q = C·u_C, la dérivée** (c3_electrons, c4_capacite, rp6_derivee) ; **L’intensité : i = C·du_C/dt** (c5_intensite, c6_relation) ; **Associations et charge à courant constant** (a1_parallele, a2_serie, g1_generateur, g2_pente) |
| Séance 3 — Voir la charge, régler R et C, puis écrire l’équation soi-même | **Le montage RC : ce qu’on voit, ce qu’on règle** (m1_montage, m2_acquisition, m3_charge, m4_regimes, m5_observer) ; **L’équation différentielle, une ligne à la fois** (e1_equation, e2a_additivite, e2b_uR, e2c_equation) ; **La rédaction complète, les formes, l’équation de q** (e2_etablir, e3_formes, e4_q) |
| Séance 4 — u_R et i, le national, puis la solution | **Les équations de u_R et de i ; au national** (e5_uR_i, e8_national) ; **L’exponentielle, puis dériver la solution** (rp7_exponentielle, s1_derivee, s2_remplacer) ; **Trouver la solution de la charge** (s3_factoriser, s4_condition, s5_verifier) |
| Séance 5 — Les quatre courbes, puis τ : le calculer et le lire | **Tracer, déduire q, i et u_R** (s6_tableau, s7_q_i, s8_quatre) ; **τ est un temps ; le lire par la tangente et les 63 %** (t1_dimension, l1_tangente, l2_pourcent) ; **R puis C, chacun à son tour ; de τ à R et C** (t2_influence, t3_C, l4_deduire) |
| Séance 6 — Courbes sans le temps, puis la décharge | **Des courbes sans le temps** (l5_pente, l6_capacite) ; **La décharge : la voir, l’écrire, la résoudre** (d2_continuite, e6_decharge, d1_decharge) ; **q, i, u_R de la décharge ; 37 % ; les huit équations** (d3_decharge_qi, l3_descente, e7_tableau) |
| Séance 7 — L’énergie, puis le national 2022 N joué pas à pas | **L’énergie emmagasinée** (l7_energie, l8_calcul) ; **2022 N : le sujet, l’équation, i(t), la lecture** (np0_sujet, np1_equation, np2_courant, np3_lire) ; **2022 N : R, puis τ par la tangente et par les 63 %** (np4_R, np5_tangente, np6_pourcent) |
| Séance 8 — La fin du 2022 N, deux sujets complets, le bilan | **2022 N : C, l’énergie, la copie complète** (np7_C, np8_energie, np9_copie) ; **Deux sujets du national** (n1_2019, n2_2021R) ; **Le bilan et la carte** (b1_bilan, b2_carte) |


## Diapositive par diapositive
#### I. Les outils et le condensateur

| Diapositive | Titre | Visuel | À toi | Pourquoi ici |
|---|---|---|---|---|
| `rc_o1_carte` | La carte du chapitre : un réservoir de charges | carte.html |  | Ouvre sur le plan du chapitre (même carte au bilan) : l'élève sait où il va. Gardée. |
| `rc_rp1_courant` | Rappel : le courant électrique | rappels.html?vue=courant |  | Départ de zéro (règle 6) : courant, tension, Ohm, additivité, puissances de dix servent dans chaque équation ; 4 profs sur 9 commencent par ces rappels (Driss, Ridouan, Atif, TOP). |
| `rc_rp2_tension` | Rappel : la tension électrique | rappels.html?vue=tension | QCM | Idem ; une tension se prend entre deux points, c'est la flèche utilisée en convention récepteur. |
| `rc_rp3_ohm` | Rappel : la loi d’Ohm | rappels.html?vue=ohm |  | u_R = R·i est la 2e ligne de toute équation du chapitre : à revoir juste avant. |
| `rc_rp4_additivite` | Rappel : la loi d’additivité des tensions | rappels.html?vue=additivite | QCM | La 1re ligne de toute équation différentielle (7 profs, tous les corrigés). |
| `rc_rp5_puissances` | Rappel : les puissances de dix | rappels.html?vue=puissances |  | µF, nF, ms : la moitié des erreurs de lecture de τ viennent des unités (commentaires Taousse, Driss). |
| `rc_c1_plaques` | Deux plaques et un isolant | condensateur.html?vue=plaques |  | Cadre RC1 : définition du condensateur, avant toute formule (Mouslim, Taousse). |
| `rc_c2a_principe` | Avant de fermer K : que va-t-on mesurer ? | condensateur.html?vue=charge | QCM | Règle 33 : le principe de l'expérience avant l'expérience. |
| `rc_c2_aiguilles` | Fermons K : que font les aiguilles ? | condensateur.html?vue=charge | observation | « Appareils avant formules » (El Omrani) ; observation de l'aiguille qui revient à 0 (règle 30). |
| `rc_c3_electrons` | Les électrons font le tour | condensateur.html?vue=charge |  | Signe des armatures par le trajet des électrons (Ridouan, El Omrani) : explique +q/−q au lieu de l'imposer. |
| `rc_c4_capacite` | q = C·u_C | figures.html?fig=fig_unites |  | q = C·u_C (9 profs, RC2) : la proportionnalité vue avant le nom C. |
| `rc_rp6_derivee` | Rappel : la dérivée, c’est une pente | rappels.html?vue=derivee | QCM | Prérequis caché de i = dq/dt : la dérivée enseignée juste avant son usage (règle 6). |
| `rc_c5_intensite` | L'intensité, c'est la pente de q(t) | intensite.html |  | i = pente de q(t) : la dérivée appliquée, signe de i en décharge préparé. |
| `rc_c6_relation` | i = C·du_C/dt | figures.html?fig=fig_boite | QCM | i = C·du_C/dt (9 profs) et la boîte des relations qui servira à chaque équation. |

#### II. Associer des condensateurs, charger à courant constant

| Diapositive | Titre | Visuel | À toi | Pourquoi ici |
|---|---|---|---|---|
| `rc_a1_parallele` | Deux condensateurs côte à côte | associations.html?vue=parallele | QCM | Associations : 7 profs sur 9 et 2018 N ; placées avant le RC comme chez la majorité (Naceiri, El Founani, Chriki). |
| `rc_a2_serie` | Deux condensateurs l'un après l'autre | associations.html?vue=serie |  | Idem, série ; manip associations.html (curseurs C₁, C₂). |
| `rc_g1_generateur` | Un générateur qui impose le courant | generateur-courant.html |  | Charge à courant constant : cadre RC3, 3 sujets sur 20 (2018 N, 2020 R, 2025 N). |
| `rc_g2_pente` | Lire C sur la droite | generateur-courant.html |  | Le national 2025 N joué sur la droite u_C(t) : lire C sur la pente. |

#### III. Le montage : ce qu'on voit, ce qu'on règle

| Diapositive | Titre | Visuel | À toi | Pourquoi ici |
|---|---|---|---|---|
| `rc_m1_montage` | Le montage à interrupteur K | circuit-rc.html?vue=montage |  | Le montage à deux positions : charge puis décharge (RC4). |
| `rc_m2_acquisition` | Flécher et brancher l'acquisition | circuit-rc.html?vue=montage | QCM | Brancher l'acquisition (2017 R, RC4) avant de regarder la courbe. |
| `rc_m3_charge` | K en position 1 : que fait u_C ? | circuit-rc.html?vue=charge |  | Première vue de la courbe de charge, AVANT l'équation (ordre de la majorité des cours écrits : Aryani, El Founani, Naceiri, Moutamadris, physagreg). |
| `rc_m4_regimes` | Régime transitoire, régime permanent | circuit-rc.html?vue=charge |  | Régimes transitoire / permanent nommés sur la courbe (plainte TOP : « non définis »). |
| `rc_m5_observer` | R et C au curseur : la charge plus lente ou plus rapide ? | tau-rc.html?avant=1 | observation | NOUVELLE. Demande du 18/11 : chaque courbe manipulée (curseurs R et C) avant l'équation ; l'observation « R doublée » (venue de rc_t2) laisse l'élève trouver seul. τ n'est pas encore écrit (règle 27). |

#### IV. L'équation différentielle, écrite pas à pas

| Diapositive | Titre | Visuel | À toi | Pourquoi ici |
|---|---|---|---|---|
| `rc_e1_equation` | Une équation avec une dérivée | figures.html?fig=fig_boite | QCM | Ce qu'est une équation différentielle : l'inconnue est une fonction (TOP : notion vue ici pour la première fois). |
| `rc_e2a_additivite` | À toi : la première ligne | circuit-rc.html?vue=montage&etape=1 | écrit | NOUVELLE. L'élève écrit la 1re ligne avant la correction (demande du 18/11) ; outil nommé, résultat non donné. |
| `rc_e2b_uR` | À toi : u_R avec u_C | circuit-rc.html?vue=montage&etape=2 | écrit | NOUVELLE. 2e ligne écrite par l'élève : u_R = R·i = RC·du_C/dt. |
| `rc_e2c_equation` | À toi : l'équation de u_C | circuit-rc.html?vue=montage&etape=3 | écrit | NOUVELLE. 3e ligne : l'équation de u_C, écrite par l'élève, corrigée ligne par ligne. |
| `rc_e2_etablir` | La rédaction complète, comme le corrigé | figures.html?fig=fig_ed_charge |  | Gardée, déplacée après les trois étapes : la rédaction complète en quatre lignes, la correction dite une 2e fois et autrement (règle 6). |
| `rc_e3_formes` | Deux écritures de la même équation | figures.html?fig=fig_ed_formes |  | La forme du_C/dt + u_C/(RC) = E/(RC) des corrigés 2021 N, 2022 N, 2023 R. |
| `rc_e4_q` | L'équation de q | figures.html?fig=fig_ed_q |  | ED de q : 2019 N, 2023 R ; même méthode, 2e application. |
| `rc_e5_uR_i` | Les équations de u_R et de i | figures.html?fig=fig_ed_uR_i |  | ED de u_R et de i (2021 R, 2024 R) : dériver toute l'additivité. |
| `rc_e8_national` | Au national : établir une ED | figures.html?fig=fig_ed_q | QCM | La question 2023 R jouée, sur la charge. |

#### V. La solution et les quatre courbes

| Diapositive | Titre | Visuel | À toi | Pourquoi ici |
|---|---|---|---|---|
| `rc_rp7_exponentielle` | Rappel : la fonction exponentielle | rappels.html?vue=exponentielle | QCM | Prérequis caché de la solution : l'exponentielle enseignée juste avant (Atif, Ridouan, Driss). |
| `rc_s1_derivee` | Dériver une exponentielle | figures.html?fig=fig_derivee_exp |  | Dériver e^(at) : le geste qu'il faut pour vérifier une solution. |
| `rc_s2_remplacer` | Trouver A et τ : dériver, remplacer | figures.html?fig=fig_resolution |  | Méthode des 7 profs : dériver, remplacer… |
| `rc_s3_factoriser` | Factoriser et conclure | figures.html?fig=fig_resolution |  | …factoriser, annuler les termes (« l'exponentielle n'est jamais nulle »). |
| `rc_s4_condition` | La forme A + B·e^(−αt) | figures.html?fig=fig_condition_initiale | QCM | Forme A + B·e^(−αt) des corrigés et la condition initiale (audit des cours écrits). |
| `rc_s5_verifier` | Vérifier qu'une expression est solution | figures.html?fig=fig_verifier |  | « Vérifier » n'est pas « trouver » : piège de consigne (cas type, 5 sujets). |
| `rc_s6_tableau` | Le tableau avant la courbe | courbe-charge.html?vue=tableau |  | u_C à 0, τ, 5τ calculés : 63 % calculé avant d'être lu (règle 37). |
| `rc_s7_q_i` | q(t) et i(t) pendant la charge | quatre-courbes.html?vue=q_i |  | q(t) et i(t) déduits de u_C(t) avec toutes les lignes (audit des cours écrits). |
| `rc_s8_quatre` | u_R(t) et les quatre courbes | quatre-courbes.html?vue=uC_uR | QCM | Les quatre courbes reconnues (cas « identifier une courbe »). |

#### VI. La constante de temps : la calculer, la lire

| Diapositive | Titre | Visuel | À toi | Pourquoi ici |
|---|---|---|---|---|
| `rc_t1_dimension` | τ est un temps | figures.html?fig=fig_dimension |  | Ouvre la partie τ : τ = RC est un temps (RC7). |
| `rc_l1_tangente` | τ par la tangente à l'origine | courbe-charge.html?vue=tangente |  | DÉPLACÉE ici (était après la décharge) : τ se lit sur la courbe juste après avoir été calculé, comme chez tous les profs ; 8 sujets sur 20. |
| `rc_l2_pourcent` | τ par les 63 % | courbe-charge.html?vue=pourcent |  | DÉPLACÉE : 63 % lu juste après la tangente (seconde méthode, 7 profs). |
| `rc_t2_influence` | Plus de R, plus lent | tau-rc.html |  | Gardée : 2e explication de l'effet de R, maintenant chiffrée par τ = RC (la 1re, qualitative, est rc_m5). Son observation est passée à rc_m5. |
| `rc_t3_C` | Plus de C, plus lent aussi | tau-rc.html | QCM | Effet de C chiffré ; question du bloc. |
| `rc_l4_deduire` | De τ à R et C | figures.html?fig=fig_r_et_c |  | DÉPLACÉE : de τ à R ou C (9 sujets) aussitôt τ lu. |
| `rc_l5_pente` | Une courbe sans le temps : du_C/dt = f(u_C) | figures.html?fig=fig_du_dt |  | DÉPLACÉE : courbe du_C/dt = f(u_C) (2021 N), exploitation de l'équation de la charge. |
| `rc_l6_capacite` | q = f(u) : la pente est C | figures.html?fig=fig_q_u |  | DÉPLACÉE avec rc_l5 (sa voix dit « une autre courbe sans le temps ») : q = f(u), 2018 N. |

#### VII. La décharge : voir, écrire, résoudre

| Diapositive | Titre | Visuel | À toi | Pourquoi ici |
|---|---|---|---|---|
| `rc_d2_continuite` | u_C ne saute pas, i change de sens | continuite.html?vue=enchaine | QCM | DÉPLACÉE en tête de la décharge : on VOIT la bascule (u_C continue, i change de sens) avant d'écrire son équation (règle 4). |
| `rc_e6_decharge` | La décharge : sans générateur | figures.html?fig=fig_ed_decharge |  | DÉPLACÉE ici (était au milieu des équations de charge) : l'équation de la décharge après l'avoir vue. |
| `rc_d1_decharge` | La décharge : u_C = E·e^(−t/τ) | figures.html?fig=fig_decharge_solution |  | La solution de la décharge, A par la condition initiale (u_C continue, vue en rc_d2). |
| `rc_d3_decharge_qi` | q(t), i(t) et u_R(t) pendant la décharge | continuite.html?vue=decharge |  | q, i, u_R de la décharge (audit des cours écrits). |
| `rc_l3_descente` | Courbes qui descendent : 37 % | quatre-courbes.html?vue=descente | QCM | DÉPLACÉE : 37 % lu sur les courbes qui descendent, une fois la décharge connue. |
| `rc_e7_tableau` | Le tableau des huit équations | figures.html?fig=fig_tableau_ed |  | DÉPLACÉE à la fin de la décharge : le tableau des huit équations range charge ET décharge, il vient après les deux. |

#### VIII. L'énergie emmagasinée

| Diapositive | Titre | Visuel | À toi | Pourquoi ici |
|---|---|---|---|---|
| `rc_l7_energie` | L'énergie du condensateur | energie.html?vue=lampe | QCM | Énergie à la fin, comme chez la majorité (cadre RC9). |
| `rc_l8_calcul` | Calculer l'énergie | energie.html?vue=calcul |  | Calculs d'énergie (2023 R). |

#### IX. Deux sujets du national

| Diapositive | Titre | Visuel | À toi | Pourquoi ici |
|---|---|---|---|---|
| `rc_n1_2019` | Un sujet complet : la charge (2019 N) | figures.html?fig=fig_n1_2019 | QCM | Sujet complet 2019 N, joué étape par étape (figures.html, un moment par question). |
| `rc_n2_2021R` | Un sujet complet : l'intensité (2021 R) | figures.html?fig=fig_n2_2021R |  | Sujet complet 2021 R (équation de i, τ, R, C). |

#### X. Bilan du chapitre

| Diapositive | Titre | Visuel | À toi | Pourquoi ici |
|---|---|---|---|---|
| `rc_b1_bilan` | Ce qu'il faut retenir | bilan.html |  | Fiche « ce qu'il faut retenir » avec les trous de l'élève. |
| `rc_b2_carte` | La carte du chapitre et la suite | carte.html |  | Carte du chapitre et lien vers le RL. |

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
Les deux sujets complets (`rc_n1_2019`, `rc_n2_2021R`) se jouaient question par question, mais la voix donnait tout :
l'équation, A et α, Q, τ, puis « calcule C, puis R » ; l'élève ne répondait qu'à la fin. Aucun exercice du national ne
faisait chercher l'élève étape par étape sur τ (le cas le plus fréquent, 8 sujets sur 20), ni sur l'énergie.

### Ce qui est ajouté : le national 2022 N, partie 1, joué pas à pas (10 diapositives)
Choisi parce qu'il réunit les cas types les plus fréquents avec des valeurs rondes (corrigé lu le 18/11 : E = 12 V,
i(0) = 12 mA, τ = 50 ms, R = 1 kΩ, C = 50 µF) et qu'aucune diapositive du cours ne l'utilisait. Deux questions ajoutées,
signalées comme telles : τ par les 63 % (la seconde méthode, que d'autres sujets demandent) et l'énergie ½·C·E² = 3,6 mJ
(2023 R). Placé après l'énergie et avant les deux sujets complets : tout ce qu'il demande est déjà enseigné (règle 27).
L'ordre des étapes (équation, solution, lecture, τ deux fois, la grandeur cherchée, l'énergie) est le même dans le RL et
le RLC : l'élève reconnaît la démarche.

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

#### IX. Le national 2022 N, joué pas à pas

| Diapositive | Titre | Visuel | À toi | Pourquoi ici |
|---|---|---|---|---|
| `rc_np0_sujet` | Le national 2022 N : lire le sujet deux fois | national-pas-a-pas.html?sujet=rc2022n&etape=sujet |  | Règle 6 du professeur : le sujet lu deux fois (de quoi parle-t-il ? puis les données et ce qu'on cherche) avant tout calcul ; aucune question notée. |
| `rc_np1_equation` | 2022 N, étape 1 : l'équation différentielle | national-pas-a-pas.html?sujet=rc2022n&etape=1 | écrit | Cas type « établir l'équation » (4 sujets) : la démarche des étapes `rc_e2a`–`rc_e2c`, maintenant sur un sujet. |
| `rc_np2_courant` | 2022 N, étape 2 : l'expression de i(t) | national-pas-a-pas.html?sujet=rc2022n&etape=2 | écrit | Cas type « expression de i(t) » (3 sujets) : dériver la solution donnée ; la courbe se trace avant la question. |
| `rc_np3_lire` | 2022 N, étape 3 : lire E et i(0) | national-pas-a-pas.html?sujet=rc2022n&etape=3 | écrit | Règle 12 : lire l'axe avant la courbe ; E et i(0) lus seuls, avant tout calcul (une idée à la fois). |
| `rc_np4_R` | 2022 N, étape 4 : la valeur de R | national-pas-a-pas.html?sujet=rc2022n&etape=4 | écrit | Cas type « en déduire R, C ou E » (9 sujets) : la relation, la conversion, l'application numérique, le résultat. |
| `rc_np5_tangente` | 2022 N, étape 5 : τ par la tangente | national-pas-a-pas.html?sujet=rc2022n&etape=5 | écrit | Cas type le plus fréquent, τ graphiquement (8 sujets) : la tangente (T) du sujet ; sa construction se voit à l'étape suivante. |
| `rc_np6_pourcent` | 2022 N, étape 6 : τ par les 63 % | national-pas-a-pas.html?sujet=rc2022n&etape=6 | écrit | Seconde méthode (règle 11 : vérifier par une deuxième route) ; 0,63·E calculé, pas affirmé (règle 37). |
| `rc_np7_C` | 2022 N, étape 7 : montrer que C = 50 µF | national-pas-a-pas.html?sujet=rc2022n&etape=7 | écrit | Question 1.2.3 du sujet : C = τ/R = 50 µF. |
| `rc_np8_energie` | 2022 N, étape 8 : l'énergie emmagasinée | national-pas-a-pas.html?sujet=rc2022n&etape=8 | écrit | Question ajoutée (énergie : 2023 R, cadre RC9) : ½·C·E² ; même valeur que E₀ de la partie RLC du même sujet. |
| `rc_np9_copie` | 2022 N : la copie complète | national-pas-a-pas.html?sujet=rc2022n&etape=fin |  | Règle 33 : la copie complète vient après la dernière étape, jamais avant ; chaque réponse se relit comme le barème la lit (relation, application numérique, résultat et unité). |

### Les mots
`python -X utf8 scripts/voix/verifier_mots.py en_attente/phys_ch6_dipole_RC` sur chaque piste nouvelle ou réécrite : plus aucun mot
rare évitable. Remplacés : « milliampères » (0 fois dans le corpus de la voix) → « milliampère » ; « kiloohm(s) » (0) →
« mille ohm » ; « microfarads » (0) → « micro farad » ; « millijoules » (1) → « millijoule » ; « palier » (0) → « la valeur
finale » ; « sommets » (0) → « l'amplitude » ; « quarante-huit », « cinquante-six », « trente-neuf » écrits sans trait
d'union (« quarante huit ») ; en darija, « فارغ » → « خاوي », « نرتبو » → « نكتبو l'équation », « كتوافق » → « كيكون عند »,
« ضاعت » → « dissipée », « كيصحح / كيقراها » → « فالتصحيح » ; au ch9, les réactions de `tl_r6_classer` (« portail », « الراسب »,
« كنحكمو »…) et de `tl_f8_variable` (« تقلقش », « فالتابلو », « quelles »…) sont réécrites. Restent, parce que ce sont des
termes du programme : kiloohm, kiloohms, microfarads (liste `a_ecouter` du fichier des voix).
Pistes à mettre en voix : 36, dont 27 de la 2ᵉ passe (`phys_ch6_dipole_RC_voix.json`, champ « passe »).

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
