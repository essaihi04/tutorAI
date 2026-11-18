# Architecture — Ondes mécaniques progressives périodiques (`phys_ch2_ondes_periodiques`)

Revue de logique du 18 novembre 2026 (skill `logique-de-cours`). Point de départ : le cours en ligne
`backend/data/courses/phys_ch2_ondes_periodiques.json` (53 diapositives, audit rythme du 14 novembre et avis du prof
d'ondes du 17 novembre déjà intégrés, toutes les voix faites). Il n'y avait pas de copie en attente. La nouvelle
version est dans `backend/data/courses/en_attente/phys_ch2_ondes_periodiques.json`. **Aucune diapositive n'a besoin
d'une voix nouvelle** : tout ce qui change est l'ordre, les blocs, les animations et leurs arrêts, posés sur les mots
déjà dits.

## Sources consultées

- **Cadre** : `cadre_reference_2bac_pc.json` → `ondes_mecaniques_periodiques` (OPP1–OPP10) ; notion officielle
  « Ondes mécaniques progressives périodiques (période, fréquence, longueur d'onde, diffraction) » et « milieux
  dispersifs » ; `perimetre.json`, `physique.json`.
- **Profs (vidéos)** : `exploration/ondes_mecaniques_periodiques.json` (10 cours : TOP, Taousse, Driss, Adrar, Ridouan,
  Laksabi, Kezakoo, bacfacile, Oussama, mouhibi) — convergences, cas types, commentaires des élèves.
- **Cours écrits en ligne (4)** :
  1. Mahajar & Tabit, moutamadris (PDF 2022) : activité deux micros + oscilloscope (instrument contre diapason) →
     définition, double périodicité → activité vibreur + stroboscope → λ = v·T, phase → activité cuve (diffraction) →
     activité fréquence variable (milieu dispersif). L'activité précède toujours la relation.
  2. Bendaoud, moutamadris : définition, double périodicité → sinusoïdale (λ, phase, T, N, v = λ·N) → stroboscope en
     exercice → diffraction → milieu dispersif.
  3. El Founani (lycée Ibn Maja), AlloSchool : définition → λ, T → v → phase → τ à l'oscilloscope → diffraction →
     stroboscopie → dispersif.
  4. Nidal Naceiri Mrabti (livre, tome 1) : définition → double périodicité → oscillogramme (T, N) → sinusoïdale →
     états vibratoires → v → stroboscope → sons et ultrasons, deux micros → diffraction → dispersif.
- **National** (exploration, `cas_types`, 2016-2025) : λ, v, N avec v = λ·N (4 nationaux) ; retard d'un point et
  y_M(t) = y_S(t − τ) (3 nationaux : 2017 N, 2020 N, 2022 R) ; λ sur l'aspect (3) ; diffraction en QCM (2 : 2020 N,
  2024 R) ; T sur y_M(t) (1) ; dispersif (1) ; en phase / opposition, deux récepteurs, stroboscope : 0 au national,
  mais dans tous les devoirs.

## Ordre commun des profs, et le nôtre

Ordre commun : définition → double périodicité (T puis λ) → sinusoïdale → v = λ/T = λ·N → en phase / opposition →
stroboscope → deux récepteurs → diffraction → milieu dispersif. Le retard y_M(t) = y_S(t − τ) n'est traité que par 2
profs sur 10 ; quand il l'est, c'est avec la célérité et la phase.

Notre cours suit cet ordre. Un seul écart de place, justifié : **le retard (partie V) vient juste après « en phase /
opposition »**, au lieu de la fin du cours (voir V).

Rien hors du cadre : ni équation y(t) = a·cos(2πt/T + φ) (Laksabi, Adrar, Kezakoo), ni vitesse apparente du
stroboscope (Taousse), ni interférences.

## Séances, blocs et diapositives

Légende : [q] question « À toi » du bloc, [obs] question d'observation, [ex] exercice. Tous les ids, textes et voix
sont gardés.

### Séance 1 — La source vibre : période et fréquence (inchangée)

- **`op_s1_b1`** : `op_o1_vibreur` (le phénomène d'abord : corde, vibreur, M recommence), `op_o2_acquis`,
  `op_o2b_retard` (rappels du ch1, juste avant leur usage), `op_o3_periodique` [q] (le mot avant l'onde).
- **`op_s1_b2`** : `op_o4_definition`, `op_pr1_sinusoide` (rappel enseigné de zéro), `op_o5_sinusoidale`,
  `op_t1_periode` [q] (T lue au chrono avant sa définition — décision des profs : « la chose avant le mot »).
- **`op_s1_b3`** : `op_t2_meme_periode` [obs], `op_t3_frequence`, `op_t4_inverse` [q] (N = 1/T née de deux nombres
  lus, animation `frequence.html`).

### Séance 2 — Lire T, puis la longueur d'onde λ

**Bloc `op_s2_b1` — Convertir, lire T sur le film, sur l'oscillogramme, et pour un son non sinusoïdal** (OPP1, OPP2)
| Diapo | Pourquoi ici |
|---|---|
| `op_t5_convertir` | Le prof d'ondes : le tableau « convertir d'abord » suffit ; juste avant la première lecture en ms. |
| `op_t6_film` | T entre deux points pareils (même hauteur, même sens) : piège de la demi-période. |
| `op_t7_oscillo` [q] | **Lecture jouée pas à pas** : la figure (`fig_oscillo`) se trace sur « voici l'écran », les cinq divisions d'une période apparaissent sur « d'abord on compte les divisions », le calcul sur « le résultat ». Avant, seule l'étape « trace » était jouée. |
| `op_t8_non_sinusoidale` | **Changée** : elle n'avait aucun visuel (un tableau diapason / instrument). Nouvelle animation `ondes-periodiques-tableau/sons.html` : le diapason (voie 1) puis la guitare (voie 2) tracés par le spot, deux motifs voisins colorés, les divisions d'un motif numérotées, T = 4 × 0,5 ms = 2 ms. Le bouton S_H sous l'écran change la sensibilité : le nombre de divisions change, T reste 2 ms (variante jouée par le tuteur, puis laissée à l'élève). Le tableau est retiré de l'écran (l'animation produit la comparaison). **Rangée dans ce bloc** (elle était dans le bloc de λ) : c'est une lecture de T sur un oscillogramme, la même méthode que `op_t7`, alors que le bloc suivant parle de λ (une idée par bloc, règle 7). Sa ligne de cahier la suit. Source : Mahajar & Tabit ouvrent le chapitre par cette comparaison. |

**Bloc `op_s2_b2` — La longueur d'onde λ, et lire l'axe** (OPP3, OPP5) : `op_l1_photo` (la répétition dans l'espace
vue avant le mot), `op_l2_lambda` (la règle posée, double périodicité), `op_l3_axe` [q] (« regarde l'axe » : 8 profs
sur 10).

**Bloc `op_s2_b3` — Les rides de la cuve** : `op_l4_rides`, `op_l5_intervalles` (intervalles, pas traits),
`op_l6_source` [q] (la cote ne part pas de S). **`op_l6` jouée pas à pas** : la figure d'énoncé se trace, les
intervalles se numérotent sur « ici d couvre », le calcul s'écrit sur « donc SM égale cinq lambda ».

### Séance 3 — λ = v · T, en phase ou en opposition, et le retard

**Bloc `op_s3_b1` — Pendant une période, l'onde avance de λ** (OPP4)
| `op_c1_avance` | Le phénomène : un aller-retour de M, le front avance d'un λ (animation). |
| `op_c2_relation` | **Changée** : elle n'avait aucun visuel. Elle reprend l'animation de `op_c1` (`corde.html?vue=avance`), qui rejoue « une période, un λ » sur « on a vu : pendant une période T, l'onde parcourt λ » : la relation s'écrit à côté de ce qui la prouve. (10 profs sur 10 la tirent de v = d/Δt.) |
| `op_c3_rediger` | Rédaction comme le barème, avec l'exemple du national (20 Hz, 1,5 cm). |
| `op_c4_photo_datee` [q] | Cas type « instant de la photo » (national 2017). |

**Bloc `op_s3_b2` — En phase, en opposition** (OPP6) : `op_p1_en_phase`, `op_p2_opposition` (curseur sur P),
`op_p3_methode` (d/λ animé, `methode-phase.html`), `op_p4_troisieme` [q] (k commence à 0).

**Bloc `op_s5_b1` — Le retard dans une onde périodique** (OPP8) — **déplacé ici** (il était en séance 5) :
`op_r1_retard`, `op_r2_relation`, `op_r3_trois_lectures` (figure du national 2022 R jouée en trois arrêts : retard,
période, amplitude), `op_r3b_calculs` [q][ex].

Pourquoi ici :
- **national** : le retard d'un point est le cas le plus fréquent du chapitre après v = λ·N (3 nationaux). En phase /
  opposition, deux récepteurs et stroboscope : 0. Il était pourtant à la fin, en séance 5, après trois parties qui ne
  tombent pas au national ;
- **logique** : `op_r2_relation` finit sur « si SM = k·λ, alors τ = k·T, et M vibre en phase avec S ». Elle relie le
  retard à la phase qu'on vient de voir. À la fin du cours, cette liaison arrivait deux séances après la phase ;
- **profs** : ceux qui traitent y_M(t) = y_S(t − τ) le font avec la célérité et la phase (Laksabi). Le cadre (OPP8)
  le dit « réinvesti » du ch1 : il sert dès que v = λ·N est connue ;
- **rien ne casse** : aucune voix de ces diapositives ne suppose la mesure, la diffraction ou la dispersion. Leurs
  valeurs (v = 0,30 m/s dans la cuve) viennent de `op_c3_rediger`, qui est avant.

La quatrième diapositive de l'ancienne partie, `op_r4_source` (dessiner y_S(t)), reste en séance 5 en tête des cas
types : c'est un cas type de devoir (« représenter la source »). La garder ici aurait fait un bloc de cinq
diapositives (règle 7).

### Séance 4 — Mesurer λ, puis la diffraction

- **`op_s3_b3` — Stroboscope et deux récepteurs** (OPP7) : `op_m1_strobo`, `op_m2_immobile`, `op_m3_recepteurs` [q].
- **`op_s4_b1` — Mesurer T et λ avec deux récepteurs** : `op_m4_microsecondes` (écran animé `recepteurs.html`),
  `op_m5_premier_retour`, `op_m6_nieme`, `op_m6b_deja_ecartes` [q]. C'est la question la plus posée par les élèves
  (« pourquoi d₂ − d₁ ? ») : quatre petites marches.
- **`op_s4_b2` — La diffraction** (OPP9) : `op_d1_ouverture` [obs] (l'élève voit l'onde se diffracter avant le mot),
  `op_d2_invariants` (λ mesurée avant et après), `op_d3_justifier` [q].

### Séance 5 — Le son diffracté, le milieu dispersif, les cas du bac, le bilan

**Bloc `op_s4_b3` — Le son se diffracte aussi ; milieu dispersif ou non** (OPP9, OPP10)
| `op_d4_ultrasons` | **Changée** : elle n'avait aucun visuel (le montage décrit par des puces). Nouvelle animation `ondes-periodiques-tableau/ultrasons.html` : émetteur de 40 kHz, fente de 5 mm, récepteur promené sur un arc centré sur la fente, oscilloscope du signal reçu. λ = v/N = 8,5 mm s'écrit sur « le résultat », puis la comparaison a < λ. Deux poignées : le bord de la fente (a de 2 à 30 mm) et le récepteur (angle). Variante du tuteur : a = 30 mm, récepteur à 50° → presque plus de signal, puis retour à 5 mm. Le signal suit la figure de diffraction d'une fente (amplitude ∝ |sin u / u|), donc la valeur affichée est juste. |
| `op_s1_frequence` | Eau : deux fréquences, deux λ mesurées, deux v (animation `cuve.html`, curseur fréquence). |
| `op_s2_air` | Air : la fréquence double, v reste 340 m/s (`air.html`). |
| `op_s3_dispersif` [q] | La définition après les deux mesures ; comparaison animée à curseurs (`dispersif.html`), pas de tableau. |

**Bloc `op_s5_b2` — Cas types du bac** : `op_r4_source` (titre « Cas type : dessiner le mouvement de la source » ;
**jouée pas à pas** : la courbe de M, puis y_S(t) qui se trace sur « on trace donc la même courbe »),
`op_x1_national_2017` (coupe de l'eau, quatre arrêts), `op_x2_national_2020` [q][ex] (**jouée pas à pas** : la
figure, puis les λ comptées sur « deux lambda égale un centimètre », puis les calculs).

**Bloc `op_s5_b3`** : `op_x3_devoir` [q][ex] (la cuve à deux fréquences), `op_b1_bilan`, `op_b2_carte`.

Le bilan et la carte gardent leur ordre et leur voix (le retard y est le dernier point) : ce sont des fiches de
révision par notion, et réécrire ces deux longues voix pour suivre l'ordre aurait coûté deux pistes sans rien
apprendre de plus.

## Ce qui change par rapport au cours en ligne

| Changement | Raison |
|---|---|
| Partie « Le retard » placée après « En phase, en opposition » (activités renumérotées V à VIII) ; son bloc passe en séance 3 | Fréquence au national, liaison τ = k·T ↔ en phase, ordre des profs qui la traitent. |
| `op_r4_source` ouvre la partie « Cas types » | Cas type de devoir ; bloc de quatre diapositives au plus. |
| `op_t8_non_sinusoidale` : animation `sons.html`, tableau retiré, rangée dans le bloc de la lecture de T | Phénomène vu, lecture de l'oscilloscope jouée pas à pas, une idée par bloc. |
| `op_d4_ultrasons` : animation `ultrasons.html` (fente et récepteur manipulables) | Diffraction vue et manipulée avant la conclusion (point de l'utilisateur). |
| `op_c2_relation` : l'animation de `op_c1` rejouée sur la phrase qui la cite | La relation s'écrit à côté de son expérience. |
| `op_t7_oscillo`, `op_l6_source`, `op_r4_source`, `op_x2_national_2020` : toutes les étapes de leur figure jouées sur les mots de la voix | Lecture de l'oscilloscope et des figures du national pas à pas (règle 5, professeur règle 41). |
| Séances 3, 4, 5 recomposées (ids des blocs gardés) | Suivent le nouvel ordre ; trois blocs par séance. |
| Une réaction écrite : « tau = d/v » → « τ = d/v » (rappel C9) | Lettre grecque à l'écrit (`verifier_formules.py`). |

Ce qui reste, et pourquoi : l'ordre des parties I à IV (celui des profs), les deux questions d'observation, les
rappels enseignés de zéro (sinusoïde, retard du ch1), le stroboscope et les deux récepteurs (OPP7 : 0 national mais
dans tous les devoirs), les trois cas types, le bilan.

## Besoins notés (fichiers partagés non modifiés)

- Aucun. `sons.html` et `ultrasons.html` sont des fichiers du cours (`ondes-periodiques-tableau/`).

## Voix à faire

Aucune (liste vide : `phys_ch2_ondes_periodiques_voix.json`). La copie en attente peut remplacer le cours en ligne
dès qu'elle est validée : toutes ses pistes existent déjà.
