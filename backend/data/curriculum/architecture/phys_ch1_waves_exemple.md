# Architecture — Ondes mécaniques progressives (`phys_ch1_waves_exemple`)

Revue de logique du 18 novembre 2026 (skill `logique-de-cours`). Point de départ : la copie en attente
`backend/data/courses/en_attente/phys_ch1_waves_exemple.json` (31 diapositives, audit rythme du 14 novembre, avis du
prof d'ondes du 17 novembre). C'est le cours exemple du projet : on garde son travail. On ne change que ce qui a
une raison écrite ci-dessous. Le cours en ligne `backend/data/courses/phys_ch1_waves_exemple.json` (16 diapositives) n'est
pas touché.

## Sources consultées

- **Cadre** : `cadre_reference_2bac_pc.json` → `ondes_mecaniques` (OMP1–OMP8) ; `physique.json`, `perimetre.json`
  (clé `ondes_mecaniques`, sous-domaine officiel « 1 Ondes : ondes mécaniques progressives », 11 % de la note pour tout
  le domaine Ondes).
- **Profs (vidéos)** : `experience_profs.json` → `ondes_mecaniques` (10 cours YouTube lus en entier : Laksabi, Driss
  DOTCOM, Taousse, TOP Physique Chimie, Chargui, Noureddine, Maria, AdrarPhysic, bacfacile). Ce chapitre n'a pas de
  fichier `exploration/`.
- **Cours écrits en ligne (5)** :
  1. El Kaouahi, moutamadris (PDF 2022) : expériences qualitatives (pierre dans l'eau, corde, ressort) → définitions →
     transversale / longitudinale → son (cloche à vide, bougie) → propriétés, v = d/Δt, facteurs → retard τ, y_M'(t).
  2. Bendaoud, moutamadris (PDF 2020) : définitions → types → son → propriétés → célérité (facteurs) → retard ; exercices
     résolus : état des points à une date, aspect à deux dates.
  3. Nidal Naceiri Mrabti (livre, tome 1) : activité 1 (trois expériences) → conclusions → son (activité 2) → célérité →
     retard ; série : aspect, deux micros + oscilloscope, chronophotographie, y_M = y_S(t − τ).
  4. Fiche pédagogique 2BAC SP BIOF (4 h, Google Docs) : I ondes → II types → III célérité (mesures du son, des
     ultrasons, de l'eau) → IV retard.
  5. Ancien cours « activités », moutamadris : ébranlement → célérité **mesurée d'abord** (capteurs, tableau d/Δt) puis
     définie → milieu.
- **National** (`backend/data/exams/physique`, 2016-2025) : un exercice « ondes » à chaque session (2 à 3,5 points).
  Ondes mécaniques : 2017 N, 2018 N, 2019 N, 2020 N, 2020 R, 2021 R, 2022 N, 2022 R, 2024 N, 2024 R (10 sessions sur 20,
  souvent mêlées au ch2). Cas types, du plus fréquent au moins fréquent : oscillogramme / deux récepteurs (2018 N,
  2020 R, 2022 R, 2024 R…), photo / aspect de la surface (2017 N, 2019 N, 2022 N, 2024 N), retard y_M(t) (2017 N, 2019 N,
  2020 N, 2022 R), écho (2020 R), deux milieux (2018 N), droite Δt = f(d) (2021 R).

## Ordre commun des profs, et le nôtre

Ordre commun (vidéos et cours écrits) : définition par des observations (corde, eau) → transversale / longitudinale →
le son (bougie, cloche à vide) → célérité (définition, puis facteurs) → retard τ = SM/v et y_M(t) = y_S(t − τ) → (lire
l'aspect et l'élongation, souvent en exercice) → mesure de la célérité (deux micros, écho) en TP ou en exercice.

Notre cours suit cet ordre partie par partie (I → V), avec trois écarts justifiés :
- **un rappel juste avant son usage** (règle 6) : la vitesse avant la célérité, la milliseconde avant l'oscilloscope ;
- **l'expérience avant la relation** (règle 4) : la seule source écrite qui mesure avant de définir (n° 5) est suivie,
  chaque relation vient après une animation qu'on manipule ;
- **la méthode « reconnaître le cas »** vient après les six exercices du national, et non avant (règle 3, voir VII.7).

Rien hors du cadre : ni √(T/μ) ni √(gh) (que les cinq cours écrits donnent), ni superposition, ni λ, T ou fréquence
(sauf le hertz dit une fois pour situer les ultrasons, valeur repère du cadre « au-delà de 20 kHz »).

## Séances, blocs et diapositives

Légende : **[q]** porte la question « À toi » du bloc, **[obs]** une question d'observation, **[ex]** un exercice.
Toutes les diapositives gardent leur id, leur texte et leur voix, sauf mention « voix réécrite ».

### Séance 1 — L'onde, ses deux types et sa célérité

**Bloc `wx_s1_b1` — Une perturbation qui avance sans transporter la matière** (OMP1)
| Diapo | Ce qu'elle apprend | Pourquoi ici |
|---|---|---|
| `wx_o1_bouee` | La question du chapitre : la ride avance, le ballon reste | Les cinq cours écrits ouvrent par l'observation de l'eau (pierre, goutte) ; le phénomène est vu (ballon.html, cinq arrêts) avant tout mot. Le texte écrit finissait par « dis-moi ce que tu prédis » (étape de prédiction supprimée le 13 novembre) : phrase retirée du texte écrit ; la voix ne la disait pas. |
| `wx_i1_corde` | Source, perturbation, milieu ; M revient à sa place | Deuxième milieu (la corde) : la même idée vue une deuxième fois, d'une autre façon (règle 6). |
| `wx_i2_definition` [q] | La définition du cadre, construite par trois questions | La définition vient APRÈS les deux observations qui la prouvent (règle 4). |

**Bloc `wx_s1_b2` — Transversale ou longitudinale, et le son** (OMP2)
| Diapo | | |
|---|---|---|
| `wx_i3_types` | Transversale : comparer deux directions | Ordre commun des profs : les types juste après la définition. Une idée (transversale), dite deux fois. |
| `wx_i3b_longitudinale` | Longitudinale (ressort) ; un ressort peut porter une onde transversale ; dimension | Piège des profs : « le ressort est toujours longitudinal ». |
| `wx_i3c_son` [q] | Le son : bougie (longitudinal), cloche à vide (pas dans le vide) | **Changée** : les deux expériences étaient dites sans être vues (la simulation `types.html` ne montrait que des grains d'air). Nouvelle animation `ondes-tableau/son.html` : la flamme avance et recule devant le haut-parleur, puis la pompe vide la cloche, les arcs de son pâlissent et disparaissent alors que la sonnerie vibre ; une poignée « air » que l'élève tire (set_parameters `air_pct`). Un arrêt par phrase de la voix (8 moments), voix gardée. |

Le rappel de la vitesse sort de ce bloc : il n'a rien à voir avec les types d'ondes (une idée par bloc, règle 7) ;
sa ligne de cahier part avec lui.

**Bloc `wx_s1_b2b` — La vitesse, puis la célérité et ce dont elle dépend** (OMP3)
| Diapo | | |
|---|---|---|
| `wx_p1_vitesse` | Rappel : v = d/Δt sur une voiture | **Déplacée dans ce bloc** : prérequis enseigné juste avant son usage (règle 6). |
| `wx_c1_celerite` [q] | La célérité, mesurée du front au front | Piège n° 1 des profs (mesurer jusqu'à l'arrière). Deux photos de la corde avant la relation. |
| `wx_c2_facteurs` [obs] | Le milieu décide (acier > eau > air) | Valeurs comparées par une course à trois pistes (`milieux.html`), pas par un tableau ; l'élève trouve l'ordre (observation). Pas de « plus dense donc plus rapide » (à ne pas dire). |
| `wx_c2b_temperature` | Température, tension ; la frappe ne change rien | Curseur de température ; la célérité dépend du milieu, pas de la source (OMP3). |

### Séance 2 — Le retard, lire une onde, mesurer la célérité

**Bloc `wx_s1_b3` — Le retard, l'élongation, la durée et la longueur** (OMP4, OMP5, OMP8)
| Diapo | | |
|---|---|---|
| `wx_r1_retard` | τ = SM/v | Après la célérité (ordre commun) ; l'élève glisse M et voit les deux courbes décalées AVANT la relation. |
| `wx_r1b_elongation` | y_M(t) = y_S(t − τ), onde non amortie ; entre deux points | Une idée de plus sur la même figure ; condition « non amortie » écrite (règle 37). |
| `wx_r2_duree_longueur` | θ, L = v·θ | Titre renuméroté « III.3 » (deux diapositives portaient « III.2 »). Ne dit pas « longueur d'onde » (piège). |
| `wx_r2b_dates` [q] | t_M = t₀ + SM/v, retour au repos t_M + θ | Cas type « source qui ne démarre pas à 0 » (OMP4). |

**Bloc `wx_s1_b3b` — Lire une onde : aspect ou élongation** (OMP7)
| `wx_l1_aspect` | Lire l'axe d'abord ; aspect y(x) contre élongation y(t) | Après θ et L, qu'il relie à leurs graphes. Le petit tableau « graphe / axe / front » reste : c'est un tableau de méthode (permis), la simulation montre les deux graphes à côté. |
| `wx_l2_sens` [q] | Quels points montent | Cas type `etat_vibratoire` des profs ; geste « déplacer l'onde un petit peu ». |

Bloc de deux diapositives seulement : le cours de l'aspect est court chez tous les profs ; le grossir aurait mélangé deux idées.

**Bloc `wx_s2_b1` — Mesurer la célérité : la milliseconde et les deux micros** (OMP6)
| `wx_p2_milli` [q] | 1 ms = 10⁻³ s | Rappel juste avant l'oscilloscope (règle 6). |
| `wx_m1_micros` | Le principe : M₁ puis M₂, le retard τ | TP officiel ; cas le plus fréquent au national. Principe sans calcul d'abord. |
| `wx_m1b_lecture` | Lire l'oscilloscope pas à pas : sensibilité, divisions, τ, v | Trois arrêts (`signal_m1`, `signal_m2`, `mesure`). |

### Séance 3 — L'écho, rédiger, puis le national : lire l'oscillogramme

**Bloc `wx_s2_b1b` — L'écho, puis rédiger comme le barème** (OMP6)
| `wx_m2_sonar` [obs] | Ultrasons ; l'onde fait l'aller et le retour | L'élève trouve « 2d » lui-même (observation), la formule n'est pas écrite avant sa réponse. |
| `wx_m2b_formule` | 2d = v·τ, d = v·τ/2 | La relation après le phénomène. |
| `wx_b1_redaction` [q] | Relation → application numérique → résultat → unité | Juste avant les exercices du national, pour que chacun soit rédigé ainsi. |

**Bloc `wx_s4_b1` — National : lire l'oscillogramme, dater un aspect** [chaque diapo q + ex]
`wx_n1_national_2022n`, `wx_n2_national_2024r`, `wx_n3_national_2024n` : la figure de l'examen redessinée et jouée
(`national.html`, 5 arrêts chacune : signal émis, son qui avance, signal reçu, écran complet, débuts), la question avant
le résultat, la démonstration ligne par ligne. **Déplacé en séance 3** : la séance 3 n'avait qu'un bloc et demi (l'écho
et une diapositive de méthode) ; les trois premiers cas du national (les plus fréquents) se travaillent juste après la
méthode de rédaction.

### Séance 4 — National : droite, écho, deux milieux ; reconnaître le cas ; bilan

**Bloc `wx_s4_b2`** : `wx_n4_national_2021r` (droite Δt = f(d), 4 arrêts), `wx_n5_national_2020r` (échographie, 6 arrêts),
`wx_n6_national_2018n` (air et pétrole, 6 arrêts).

**Bloc `wx_s2_b2` — Reconnaître le cas type : les six cas du national revus**
| `wx_b2_national` [ex] | Le mot-code de l'énoncé → le cas → sa relation | **Déplacée après les six exercices du national** (elle était avant). Avant, elle donnait au départ la table des cinq cas que l'élève n'avait encore jamais rencontrés (règle 3 : ne pas tout donner au départ). Après, elle regroupe ce qu'il vient de résoudre, et son exercice (droite Δt = f(d)) demande de reconnaître le cas sans savoir d'avance lequel : c'est une pratique mélangée, qui fixe mieux. **Voix réécrite** : elle commençait par « tu arrives aux exercices du national » ; elle dit maintenant « tu as vu six exercices du national, on les regroupe », et « un exercice au tableau » (il n'y en a qu'un ; elle disait « deux »). |

**Bloc `wx_s4_b3` — Le bilan** : `wx_b3_bilan` (fiche, huit blocs), `wx_b4_carte` (carte, huit branches). Le bilan
vient après tout le reste (règle 3).

## Ce qui change par rapport à la copie en attente du 17 novembre

| Changement | Raison |
|---|---|
| `wx_i3c_son` sur la nouvelle animation `son.html` (pointage réécrit sur la voix existante, variante : la poignée « air » à 100 % puis 0 %) | Règle 5 et point de l'utilisateur : chaque phénomène vu en animation manipulable avant sa conclusion. |
| `wx_p1_vitesse` passe du bloc des types au bloc de la célérité | Une idée par bloc ; le prérequis juste avant son usage. |
| `wx_b2_national` passe après `wx_n6_national_2018n` (activité VII), voix réécrite | Ne pas donner la carte des cas avant les cas ; l'élève reconnaît le cas seul. |
| Séance 3 = écho + rédaction, puis les trois premiers exercices du national ; séance 4 = trois autres, reconnaître le cas, bilan | Séances équilibrées (la séance 3 n'avait qu'un bloc et une diapositive). Les ids des blocs sont gardés : la progression des élèves reste valable. |
| Titre `wx_r2_duree_longueur` « III.3 », titre de l'activité VI | Numérotation (deux « III.2 »). Les titres ne sont pas lus par la voix. |
| Texte écrit de `wx_o1_bouee` sans « dis-moi ce que tu prédis » | Plus d'étape de prédiction (13 novembre). |

Ce qui reste, et pourquoi : les 29 autres diapositives et leurs voix (une idée par diapositive, arrêts sur image
déjà posés, deux questions d'observation, rappels enseignés de zéro) ; le tableau de méthode de `wx_l1_aspect` et la
table des mots-codes de `wx_b2_national` (tableaux de méthode, pas de valeurs) ; les trois blocs du national à trois
exercices (ce sont des corrections jouées une par une, pas des explications).

## Besoins notés (fichiers partagés non modifiés)

- Aucun. `son.html` est un fichier du cours (`ondes-tableau/`), pas un fichier partagé.

## Voix à faire

Une piste : `mixed/wx_b2_national` (liste : `phys_ch1_waves_exemple_voix.json`). Mots rares gardés : « l'écho »,
« micros » (termes du programme, déjà dans l'ancienne voix enregistrée sans défaut).
