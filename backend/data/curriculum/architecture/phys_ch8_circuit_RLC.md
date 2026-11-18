# Architecture du cours `phys_ch8_circuit_RLC` — Oscillations libres d'un circuit RLC série

Refaite le 18 novembre 2026 (skill `logique-de-cours`). Le cours en ligne n'est pas touché. La nouvelle version est dans `backend/data/courses/en_attente/phys_ch8_circuit_RLC.json`. Les pistes à mettre en voix sont dans `phys_ch8_circuit_RLC_voix.json`.

Ce chapitre n'a pas d'exploration en vidéo. L'ordre commun vient donc des cours écrits lus le 18/11 :
- Hajji, « circuit RLC libre et amorti » ;
- Chriki, résumé n° 8 ;
- kezakoo, leçon 8 ;
- Ismaili-Alaoui (2 SM) ;
- Moutamadris, fiche n° 5 ;
- Naceiri, fin de chapitre ;
- et de l'audit `docs/audit-prof/physique.md` (Naceiri, Sbiro).

## La logique avant

Le cours en ligne compte 52 diapositives en 5 séances :

1. rappels, puis décharge dans une bobine (observée) ;
2. les trois régimes (curseur R + r dans `regimes.html`) ;
3. l'équation (dite par la voix) ;
4. la solution du LC et T₀ ;
5. U_m et φ ;
6. l'oscillogramme ;
7. l'échange d'énergie ;
8. l'amortissement ;
9. l'entretien ;
10. les nationaux ;
11. le bilan.

**L'ordre était déjà celui des profs.** Les écarts étaient ailleurs :

1. **L et C n'étaient manipulés qu'après la formule de T₀** (`lc_p3_influence`). Seul R + r l'était avant l'équation.
2. **L'équation était dite par la voix** (`lc_e1`–`lc_e3`), pas écrite par l'élève.
3. **Une coupure de séance était fausse.** `lc_c1_depart` dit « la séance d'avant, on a trouvé la solution ». Pourtant la solution (`lc_e8`) et `lc_c1` étaient dans la même séance 3.

## La logique après

Le cours compte 56 diapositives (4 nouvelles) en 7 séances, avec la même ossature que le RC et le RL :

- **I.** Les outils et la décharge dans une bobine.
- **II. Ce qu'on voit, ce qu'on règle** : les régimes (R + r), puis **`lc_r5_observer`** (curseurs L et C : « C × 4 → T × 2 »). Sa question QCM (« C ÷ 4 ») fait déduire l'élève lui-même.
- **III. L'équation, écrite par l'élève** : `lc_e0a` → `lc_e1`, `lc_e0b` → `lc_e2`, `lc_e0c` → `lc_e3`. Puis l'équation en u_C et le LC idéal.
- **IV.** La solution et T₀.
- **V.** U_m et φ : la **séance 5 commence à `lc_c1`**.
- **VI–XI** : sans changement (oscillogramme, énergie, amortissement, entretien, nationaux, bilan).

**Ce qui reste, et pourquoi.**
- La lecture de l'oscillogramme (`lc_l1`–`lc_l4`) reste après U_m et φ. Les cours écrits mettent U_m et φ juste après la solution (Chriki, kezakoo, Ismaili-Alaoui). La carte du chapitre (`lc_o1`, voix enregistrée) annonce aussi cet ordre.
- L'énergie (échange LC, puis perte dans le RLC), puis l'entretien en dernier, comme dans tous les cours écrits.
- Trois régimes seulement : le cadre RLC2 ne compte pas le régime critique.
- Aucune voix existante n'est réécrite. Les diapositives déplacées gardent la leur.

## Fréquence au national (17 sessions RLC sur 20, fiche du cadre et carte du chapitre)

- **Lire la période, puis trouver L ou C** : 13 sessions → `lc_l1`–`lc_l4`, `lc_p4`, `lc_n1`, `lc_n2`.
- **Calculer une énergie** (à un instant, perdue entre deux sommets) : 14 sessions → `lc_en2`–`lc_en4`, `lc_a4`.
- **Établir l'équation (q ou u_C)** : très fréquent → `lc_e0a`–`lc_e4` (écrite par l'élève).
- **Reconnaître le régime, rôle de R** : `lc_r1`–`lc_r4` (2021 R, 2020 R).
- **Entretien, k = R + r** : 2018 N, 2020 N → `lc_k1`–`lc_k3`, `lc_n1`.

## Animations et exercices animés

- **`circuit-rlc-tableau/observer.html`** (nouveau) : maille de décharge peinte (condensateur, résistor, bobine), R + r = 20 Ω fixe. Deux curseurs, L (0,025–0,4 H) et C (1–16 µF). u_C(t) se trace au ralenti, et T (la pseudo-période vue en `lc_r1`) est cotée entre deux sommets. La courbe d'avant reste en pointillés. Les moments sont `courbe`, `C_fois_4` et `L_fois_4`. La formule 2π√(LC) n'est pas écrite.
- **Étapes de l'équation** : `equation.html?etape=1|2|3`, arrêtées sur `fleches`.
- **Nationaux** (2021 R, 2022 N, 2023 N, 2025 N, 2020 N, 2016 N, 2024 N, 2018 N) : déjà joués par `figures.html`, `oscillogramme.html` et `energie.html`, un moment par question. Ils sont gardés.

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
| Séance 1 — Les relations de base ; le condensateur se vide dans une bobine | **Les relations du condensateur et de la bobine** (o1_carte, rp1_condensateur, rp2_bobine) ; **Le condensateur se vide dans une bobine** (d1_rc, d2_bobine, d3_courant) ; **Oscillations libres, signe de i, u_b au départ** (d4_libres, d5_signe, d6_depart) |
| Séance 2 — Ce qu’on voit, ce qu’on règle ; l’équation écrite soi-même | **Les régimes : une expérience à la fois** (r1_pseudo, r2_aperiodique, r3_ordre, r4_national) ; **L et C au curseur ; la première ligne de l’équation** (r5_observer, e0a_additivite, e1_additivite) ; **Remplacer chaque tension, puis tout écrire avec q** (e0b_remplacer, e2_remplacer, e0c_tout_en_q, e3_equation_q) |
| Séance 3 — L’équation en u_C, le LC, le cosinus et sa dérivée, T₀ | **L’équation en u_C ; le circuit LC idéal** (e4_equation_uc, e5_lc_ideal) ; **Le cosinus, la sinusoïde, sa dérivée** (rp3_cosinus, e6_sinusoide, rp4_dcos) ; **Dériver deux fois ; la période propre** (e7_deriver, e8_T0) |
| Séance 4 — Ce qui fixe T₀ : L et C, pas E | **T₀ est un temps ; la tension de charge ne change pas T₀** (p1_unites, p2_charge) ; **Si C ou L est multipliée par 4 ; le national 2022** (p3_influence, p4_national) |
| Séance 5 — U_m et φ, q(t) et i(t) ; lire un oscillogramme | **Trouver U_m et φ** (c1_depart, c2_amplitude, c3_angles) ; **Le sens de départ ; q(t) et i(t)** (c4_sens, c5_courant) ; **Lire T et trouver L ou C** (l1_mesure, l2_voisine, l3_carre, l4_2023) |
| Séance 6 — Échange d’énergie, amortissement, entretien | **L’échange d’énergie dans le circuit LC** (en1_reservoirs, en2_depart, en3_echange, en4_somme) ; **L’énergie diminue : effet Joule et dE/dt** (a1_joule, a2_derivee, a3_dEdt, a4_perdue) ; **Lire les courbes d’énergie, puis entretenir les oscillations** (a5_courbes, k1_entretien, k2_k, k3_T0) |
| Séance 7 — Deux sujets du national, puis le bilan | **Deux sujets du national** (n1_2020N, n2_2025N) ; **Le bilan et la carte** (bl_fiche, cr_carte) |


## Diapositive par diapositive
#### I. Les outils, puis un condensateur qui se vide dans une bobine

| Diapositive | Titre | Visuel | À toi | Pourquoi ici |
|---|---|---|---|---|
| `lc_o1_carte` | La carte du chapitre : un condensateur qui se vide dans une bobine | carte.html |  | Plan du chapitre : d'où l'on vient (RC, RL) et où l'on va. |
| `lc_rp1_condensateur` | Rappel : la charge et le courant du condensateur | intensite.html |  | Départ de zéro : q = C·u_C et i = dq/dt revus juste avant usage. |
| `lc_rp2_bobine` | Rappel : la tension de la bobine | triangle.html | QCM | u_b = L·di/dt + r·i revu. |
| `lc_d1_rc` | Rappel : décharge dans une résistance | circuit-lc.html?vue=bascule |  | On part du connu : la décharge dans R (pont avec le RC). |
| `lc_d2_bobine` | On remplace R par une bobine | circuit-lc.html?vue=bascule | observation | On remplace R par une bobine : l'observation clé (u_C change de signe), AVANT toute équation (ordre des cours A, C, D, E). |
| `lc_d3_courant` | Condensateur vide, courant maximal | circuit-lc.html?vue=bascule | QCM | Pourquoi u_C dépasse 0 : courant maximal quand le condensateur est vide. |
| `lc_d4_libres` | Oscillations libres | circuit-lc.html?vue=bascule |  | Oscillations libres nommées. |
| `lc_d5_signe` | i = dq/dt et son signe | solution.html?vue=cos |  | Signe de i = dq/dt sur les courbes. |
| `lc_d6_depart` | u_b juste après la bascule | equation.html | QCM | u_b juste après la bascule (2024 R). |

#### II. Ce qu'on voit, ce qu'on règle : les régimes, puis L et C

| Diapositive | Titre | Visuel | À toi | Pourquoi ici |
|---|---|---|---|---|
| `lc_r1_pseudo` | Une petite résistance : les sommets baissent | oscillogramme.html?vue=pseudo |  | Régime pseudo-périodique, pseudo-période T (cadre RLC2). |
| `lc_r2_aperiodique` | Une grande résistance : plus d'oscillation | oscillogramme.html?vue=aperiodique | observation | Régime apériodique ; observation (règle 30). |
| `lc_r3_ordre` | La résistance totale décide du régime | regimes.html |  | regimes.html : R + r au curseur, les trois régimes rangés. |
| `lc_r4_national` | Exercice du national : à chaque courbe sa résistance | figures.html?fig=fig_2021R | QCM | 2021 R : à chaque courbe sa résistance. |
| `lc_r5_observer` | L et C au curseur : des oscillations plus lentes ou plus rapides ? | observer.html | QCM | NOUVELLE. Demande du 18/11 : L et C au curseur avant l'équation (R + r l'était déjà en lc_r3), parallèle à rc_m5 et rl_m5 ; question : C ÷ 4, déduite par l'élève. |

#### III. L'équation différentielle, écrite pas à pas

| Diapositive | Titre | Visuel | À toi | Pourquoi ici |
|---|---|---|---|---|
| `lc_e0a_additivite` | À toi : la première ligne | equation.html?etape=1 | écrit | NOUVELLE. L'élève écrit l'additivité sans générateur ; lc_e1 corrige. |
| `lc_e1_additivite` | La loi d'additivité, sans générateur | equation.html | QCM | Gardée : correction expliquée (pourquoi 0 et pas E). |
| `lc_e0b_remplacer` | À toi : remplacer chaque tension | equation.html?etape=2 | écrit | NOUVELLE. L'élève remplace u_C, u_R, u_b ; lc_e2 corrige. |
| `lc_e2_remplacer` | Remplacer chaque tension | equation.html |  | Gardée : correction expliquée. |
| `lc_e0c_tout_en_q` | À toi : tout écrire avec q | equation.html?etape=3 | écrit | NOUVELLE. L'élève écrit tout avec q (i = dq/dt) ; lc_e3 corrige. |
| `lc_e3_equation_q` | Tout écrire avec q : on dérive deux fois | equation.html |  | Gardée : l'équation en q. |
| `lc_e4_equation_uc` | La même équation en u_C | equation.html |  | Équation en u_C (sujets). |
| `lc_e5_lc_ideal` | Le circuit LC idéal | equation.html | QCM | Circuit LC idéal : le terme d'amortissement disparaît. |

#### IV. La solution du circuit LC et la période propre

| Diapositive | Titre | Visuel | À toi | Pourquoi ici |
|---|---|---|---|---|
| `lc_rp3_cosinus` | Rappel : le cosinus et la sinusoïde | rappels.html?vue=sinusoide |  | Prérequis : le cosinus et la sinusoïde, juste avant la solution. |
| `lc_e6_sinusoide` | Une sinusoïde comme solution | solution.html?vue=cos |  | La solution reconnue sur la courbe. |
| `lc_rp4_dcos` | Rappel : la dérivée d’un cosinus | rappels.html?vue=derivee_cos | QCM | Dérivée d'un cosinus, juste avant d'en avoir besoin. |
| `lc_e7_deriver` | Dériver deux fois un cosinus | solution.html?vue=cos |  | Dériver deux fois. |
| `lc_e8_T0` | Identifier : T₀ = 2π√(LC) | solution.html?vue=cos |  | Identifier T₀ = 2π√(LC) (RLC4). |
| `lc_p1_unites` | √(LC) est un temps | periode.html?vue=T0 |  | √(LC) est un temps. |
| `lc_p2_charge` | T₀ ne dépend pas de la charge de départ | periode.html?vue=T0 |  | T₀ ne dépend pas de E (manip periode.html). |
| `lc_p3_influence` | Si C (ou L) est multipliée par 4 | periode.html?vue=influence_C |  | C ou L × 4 → T₀ × 2, maintenant chiffré par la formule (2e explication ; la 1re est lc_r5). |
| `lc_p4_national` | Exercice du national : choisir la courbe, trouver L | figures.html?fig=fig_2022N | QCM | 2022 N : choisir la courbe, trouver L. |

#### V. Les conditions initiales : U_m et φ

| Diapositive | Titre | Visuel | À toi | Pourquoi ici |
|---|---|---|---|---|
| `lc_c1_depart` | U_m et φ dans le cas du cours | solution.html?vue=phase | QCM | U_m et φ ; sa voix dit « la séance d'avant » : la séance 5 commence ici (coupure corrigée). |
| `lc_c2_amplitude` | Lire U_m sur la courbe | solution.html?vue=cos |  | Lire U_m. |
| `lc_c3_angles` | Une équation, deux angles | solution.html?vue=phase |  | Une équation, deux angles. |
| `lc_c4_sens` | Le sens de départ choisit φ | solution.html?vue=phase |  | Le sens de départ choisit φ. |
| `lc_c5_courant` | La charge q(t) et l'intensité i(t) | solution.html?vue=cos |  | q(t) et i(t) (audit des cours écrits). |

#### VI. Lire un oscillogramme

| Diapositive | Titre | Visuel | À toi | Pourquoi ici |
|---|---|---|---|---|
| `lc_l1_mesure` | Lire T sur plusieurs périodes | oscillogramme.html?vue=pseudo | QCM | Lire T sur plusieurs périodes (13 sujets lisent T). |
| `lc_l2_voisine` | La pseudo-période est voisine de T₀ | oscillogramme.html?vue=pseudo |  | T voisine de T₀ (admis). |
| `lc_l3_carre` | Trouver C (ou L) : le carré d'abord | figures.html?fig=fig_carre |  | Trouver C ou L : le carré d'abord. |
| `lc_l4_2023` | Exercice du national : l'échelle en flèches | figures.html?fig=fig_2023N |  | National 2023 N : l'échelle en flèches. |

#### VII. L'échange d'énergie

| Diapositive | Titre | Visuel | À toi | Pourquoi ici |
|---|---|---|---|---|
| `lc_en1_reservoirs` | Deux réservoirs d'énergie | circuit-lc.html?vue=echange |  | Énergie après la solution, comme tous les cours écrits. |
| `lc_en2_depart` | Au départ, tout est dans le condensateur | energie.html?vue=echange |  | Au départ, tout est dans le condensateur. |
| `lc_en3_echange` | L'énergie passe d'un réservoir à l'autre | energie.html?vue=echange | QCM | L'échange d'énergie. |
| `lc_en4_somme` | Sans résistance, la somme ne bouge pas | energie.html?vue=echange |  | Sans résistance, la somme est constante. |

#### VIII. L'amortissement

| Diapositive | Titre | Visuel | À toi | Pourquoi ici |
|---|---|---|---|---|
| `lc_a1_joule` | Avec une résistance, l'énergie diminue | energie.html?vue=amortie |  | Avec R, l'énergie diminue (effet Joule). |
| `lc_a2_derivee` | Dériver chaque énergie | energie.html?vue=amortie |  | Dériver chaque énergie. |
| `lc_a3_dEdt` | dE/dt = −(R + r)·i² | energie.html?vue=amortie |  | dE/dt = −(R + r)·i² (RLC7). |
| `lc_a4_perdue` | L'énergie perdue entre deux sommets | energie.html?vue=amortie | QCM | Énergie perdue entre deux sommets (2016 N, 2024 N). |
| `lc_a5_courbes` | Reconnaître les courbes d'énergie | energie.html?vue=amortie |  | Reconnaître E_e, E_m, E. |

#### IX. L'entretien des oscillations

| Diapositive | Titre | Visuel | À toi | Pourquoi ici |
|---|---|---|---|---|
| `lc_k1_entretien` | Entretenir les oscillations | entretien.html |  | Entretien en dernier (tous les cours écrits). |
| `lc_k2_k` | La bonne valeur de k | entretien.html |  | k = R + r. |
| `lc_k3_T0` | Oscillations entretenues, à la période T₀ | entretien.html | QCM | Entretenues à T₀. |

#### X. Deux sujets du national

| Diapositive | Titre | Visuel | À toi | Pourquoi ici |
|---|---|---|---|---|
| `lc_n1_2020N` | Sujet national 2020 N, en entier | figures.html?fig=fig_2020N |  | Sujet complet 2020 N. |
| `lc_n2_2025N` | Sujet national 2025 N, en entier | figures.html?fig=fig_2025N | QCM | Sujet complet 2025 N. |

#### XI. Bilan du chapitre

| Diapositive | Titre | Visuel | À toi | Pourquoi ici |
|---|---|---|---|---|
| `lc_bl_fiche` | Ce qu'il faut retenir | bilan.html |  | Fiche bilan. |
| `lc_cr_carte` | La carte du circuit RLC | carte.html |  | Carte du chapitre. |

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
