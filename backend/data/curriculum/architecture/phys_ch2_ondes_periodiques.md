# Architecture — Ondes mécaniques progressives périodiques (`phys_ch2_ondes_periodiques`)

Revue de logique du 18 novembre 2026 (skill `logique-de-cours`). Point de départ : le cours en ligne
`backend/data/courses/phys_ch2_ondes_periodiques.json` (53 diapositives, audit rythme du 14 novembre et avis du prof
d'ondes du 17 novembre déjà intégrés, toutes les voix faites). Il n'y avait pas de copie en attente. La nouvelle
version est dans `backend/data/courses/en_attente/phys_ch2_ondes_periodiques.json`. À la 1ʳᵉ passe, aucune
diapositive n'avait besoin d'une voix nouvelle (ordre, blocs, animations posés sur les mots déjà dits). **La 2ᵉ passe
(section « 2ᵉ passe » plus bas) réécrit 11 voix et ajoute 4 diapositives** : 88 pistes à faire.

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

## 2ᵉ passe (18 novembre 2026) : chaque cas type joué pas à pas, l'élève répond avant la correction

**Ce qui n'allait pas.** La 1ʳᵉ passe avait surtout réordonné. Dans presque toutes les diapositives de méthode et de cas
type, la voix faisait elle-même la lecture et le calcul, puis posait la question dont elle venait de donner la réponse
(`op_t7`, `op_l6`, `op_c4`, `op_p4`, `op_m6b`, `op_d3`, `op_r3b`, `op_x2`, `op_x3`) ; `op_x1` (national 2017) faisait les
quatre questions sans rien demander ; les figures du national (`figures.html`) étaient des figures finies qui
s'écrivaient, pas le phénomène (professeur règle 41) ; les calculs étaient écrits au tableau avant la réponse.

**La règle appliquée partout** (logique-de-cours règles 3 et 5, professeur règles 30, 33, 37, 41) : la voix pose la
situation et la méthode, s'arrête avant le résultat (« دابا نتا : … »), l'élève répond (ardoise « À toi » avec sa
démonstration écrite comme le barème, ou question d'observation quand c'est une lecture sur la simulation), puis la
correction. Une seule consigne à la fois. La scène se fige avant tout résultat : les valeurs et les conclusions ont
chacune leur moment, jamais joué avant la réponse, et la page accepte `conclusions: false` pendant une observation.
Une seule ardoise par bloc : quand un exercice a plus de deux calculs, les lectures passent en question d'observation.

### Nouvelle simulation `ondes-periodiques-tableau/national.html` (fichier du cours, aucun fichier partagé touché)
Quatre vues, avec les valeurs de l'examen, ouvrables figées sur un instant (`?depart=<moment>`, `reset` y revient) :
| Vue | Le phénomène d'abord | Moments (un par étape du raisonnement) |
|---|---|---|
| `oscillo` | le spot trace la voie 1 puis la voie 2 (0,1 ms/div) | `trace`, `cretes`, `divisions` (comptées une à une), `relation`, `periode`, `frequence` |
| `2017` | S vibre, l'onde part des deux côtés, puis la photo ; ensuite M bouge et y_S(t), y_M(t) se tracent | `onde_part`, `photo`, `regle`, `cretes` (« λ = ? »), `lambda`, `front`, `v`, `t`, `graphes`, `m_demarre`, `m_suit`, `relation` |
| `2020` | les rides circulaires partent de S, puis la photo ; ensuite une ouverture a ≈ λ, l'onde la traverse | `onde_part`, `photo`, `intervalles`, `lambda`, `n`, `retard`, `obstacle`, `ouverture_atteinte`, `diffractee`, `meme_lambda` |
| `2022` | l'onde part de S, atteint M (L = 2,5 cm) ; le spot trace y_M(t) en même temps | `depart`, `m_demarre`, `trace`, `retard`, `cretes` (« T = ? »), `periode`, `amplitude`, `n`, `v`, `lambda` |

Vérifiée dans Chromium (Playwright) : chaque moment atteint à sa date, aucune erreur de console, encre sur le canevas,
captures à 1024 × 560 et 724 × 350 (téléphone en paysage) sans chevauchement après corrections (étiquettes des voies
dans l'écran, « 1 cm » sous la cuve, règle peinte sans texte peint de 11 px : ses nombres sont écrits à la craie).
**Un objet, un dessin** (logique-de-cours règle 10, simulations-au-tableau règle 15) : l'eau, la pointe, la paroi, la
tige sont peintes par `eau.js` comme dans `cuve.html` et `fente.html` ; l'écran d'oscilloscope et le spot sont ceux de
`sons.html`. Le lexique visuel partagé (`docs/lexique-visuel/`, `shared/lexique/`) n'existe pas encore dans le dépôt :
ces objets (eau en coupe et vue de dessus, oscilloscope, spot) sont à y verser quand il sera créé (fichiers partagés,
hors de cette passe).

### Diapositives
| Diapositive | Changement | Pourquoi |
|---|---|---|
| `op_t7_oscillo` | `national.html?vue=oscillo` : le spot trace, deux crêtes, les 5 divisions comptées, la relation ; la voix s'arrête avant T (« احسب T ») ; N retiré de la voix | La voix donnait T et N avant la question ; lecture d'oscilloscope animée (cas type `periode_elongation`). |
| `op_l6_source` | La voix donne la méthode et s'arrête avant « SM = 5λ » ; la figure reste à `trace` (les intervalles numérotés étaient la réponse) | Ne pas donner la réponse. |
| `op_c4_photo_datee` | La voix s'arrête à « t = 2,5 T » ; « T = 20 ms » retiré du tableau | L'élève fait la division. |
| `op_p4_troisieme` | La voix fait k = 0 et k = 1, demande k du 3ᵉ point ; la formule générale au tableau au lieu de « k = 2, SM = 5 cm » | Le piège (k commence à 0) est trouvé par l'élève. |
| `op_m6b_deja_ecartes` | Arrêt sur `en_phase_2` (le moment `mesure` écrivait λ) ; la voix donne d = d₂ − d₁ et d = 2λ, l'élève calcule | Idem. |
| `op_d3_justifier` | Figée sur `ouverture_atteinte` (les arcs étaient la réponse) ; la condition « a ≤ λ » est la méthode, l'élève compare 10 mm et 15 mm | Cas type `diffraction_justifier`. |
| `op_r3_trois_lectures` | National 2022 R rejoué (`national.html?vue=2022`) : l'onde atteint M, la courbe se trace ; **observation** : « à quelle date M démarre ? » (τ) | Lecture faite par l'élève avant d'être dite. |
| `op_r3c_periode` **nouvelle** | Même courbe (`&depart=retard`) : **observation** « que vaut T ? » entre deux crêtes marquées « T = ? » ; puis l'amplitude ; τ ≠ T redit | Une lecture par diapositive ; T et τ confondus = l'erreur la plus fréquente du cas. |
| `op_r3b_calculs` | (`&depart=amplitude`) La voix donne les relations, l'élève calcule N (question) puis v (exercice) ; λ = v·T reste en fin de cours | La voix faisait les trois calculs. |
| `op_x1_national_2017` | `national.html?vue=2017` : l'onde part de S, la photo ; **observation** λ sur la règle ; ardoise **nouvelle** : v (QCM aux distracteurs du sujet : 200 m/s = λ en cm, 8 × 10⁻⁴ = λ/N) puis t = SM/v (3 s, 0,3 s) ; réactions préparées écrites | Les quatre questions étaient dites sans que l'élève réponde. |
| `op_x1b_national_2017_retard` **nouvelle** | (`&depart=t`) La 4ᵉ question du sujet : y_S(t) et y_M(t) se tracent, M ne bouge qu'à 30 ms ; **observation** y_M(t) = y_S(t ∓ …) | C'est la vraie 4ᵉ question du national 2017 (l'ancienne voix comparait les phases, ce que le sujet ne demande pas). |
| `op_x2_national_2020` | `national.html?vue=2020` : les rides partent, la photo ; **observation** « combien de λ dans 1 cm ? » (le piège : compter les cercles) ; ardoise : N (nouvelle QCM, réactions écrites) puis τ (exercice gardé avec sa voix) | La voix faisait tout puis demandait λ et N. |
| `op_x2b_national_2020_diffraction` **nouvelle** | (`&depart=retard`) La paroi et l'ouverture a ≈ λ, l'onde la traverse ; **observation** = la QCM du sujet (« N, λ, v ne sont pas modifiées ») ; puis les λ égales avant et après | Cas type diffraction du national, vu se produire. |
| `op_x3_devoir` | Arrêt sur `regle_posee` (v n'est pas encore écrite) ; la voix donne la méthode, l'élève calcule v puis compare A et B (ardoise gardée avec ses voix) | Idem. |
| `op_x3b_dispersif` **nouvelle** | `cuve.html?vue=frequence&etape=30` (paramètre ignoré par la page : il ne sert qu'à recharger l'iframe) : passage à 30 Hz, nouvelle mesure ; **observation** « l'eau est-elle dispersive ? » avant la conclusion (le moment `conclusion` de la page n'est pas joué) | Cas type `dispersif`, la conclusion trouvée par l'élève. |

Observations : 2 → 9 dans le cours. C'est plus que « 0 à 2 » de la règle 30 ; c'est voulu par cette passe (chaque
lecture d'un cas type du national est faite par l'élève avant la correction), comme la chimie ch13 (10). Aucune n'est
sur une définition ; deux (`op_x1b`, `op_x3b`) portent sur une petite comparaison que la simulation montre.

### Blocs et séances
- `op_s5_b1` (séance 3) = `op_r1`, `op_r2`, `op_r3` ; **nouveau `op_s5_b1b`** = `op_r3c`, `op_r3b` (ardoise sur `op_r3b`).
  La séance 3 a quatre blocs, mais le dernier ne fait que deux diapositives : ≈ 45 min.
- `op_s5_b2` = `op_r4_source`, `op_x1`, `op_x1b` (ardoise sur `op_x1`) ; `op_s5_b3` = `op_x2`, `op_x2b` (ardoise sur `op_x2`).
- **Nouvelle séance 6** : `op_s6_b1` = `op_x3`, `op_x3b` ; `op_s6_b2` = le bilan et la carte (leur cahier, leur retrouver).
- Une ardoise au plus par bloc (vérifié) ; l'ordre des diapositives suit l'ordre des blocs (vérifié).

### Mots (scripts/voix/verifier_mots.py + même contrôle sur les observations, réactions et démonstrations nouvelles)
Remplacés : « spot » (0) → « la courbe … كتبان بشوية » ; كتتحرك (0) → كتحرك ; كيرسم (0) ; كنختارو (1) → ناخدو ; للجهتين (1)
→ « لليمين، وكتمشي حتى لليسار » ; « la pointe » (0) → النقطة S ; ما كتبدلش (0) → كتبقى هي هي ; ثالثا (2) → التالتة ;
طلعة (0) → قيمة ; تقربو (0) → ولاو قراب ; تحكم (1) → تجاوب ; فراغات (0) → les intervalles ; creux (0), معلمين, متأخرة retirés.
Résultat : 0 mot rare dans les 15 pistes de diapositive réécrites ou nouvelles, 0 dans les observations, réactions et
démonstrations nouvelles. (Les mots rares qui restent sont dans des réactions déjà enregistrées, non modifiées.)

### Vérifications
- JSON chargé ; `pytest -k "course or cours or concentration"` : 88 passés, 1 échec préexistant (cours SVT ch1).
- `verifier_pointage_simulations.py --ecarts` : 0 « introuvable » (copie en attente et cours en ligne, avant comme après) ;
  DEPART 34 → 26, IFRAME 9 → 8 ; les GESTE nouveaux viennent des diapositives sans voix (durée 0 : tous les gestes à
  0 s) — avec une durée estimée (75 ms par caractère), il n'en reste aucun sur les diapositives réécrites sauf un
  préexistant (`op_c4`, 0,8 s).
- `verifier_formules.py` (cours et dossier) : rien ; `verifier_figures_cahier.py` : 0 erreur.
- Cours en ligne et pages existantes non modifiés (`national.html` est un fichier nouveau).

### Ce qui reste
- Les voix (88 pistes, `phys_ch2_ondes_periodiques_voix.json`) ; d'ici là les observations sont dites par la voix en direct.
- Rejouer les diapositives dans le lecteur avec leur voix (`verifier-pointage-navigateur.mjs`) quand les pistes existeront.
- `op_r4_source` (dessiner y_S(t)) reste une démonstration sans réponse de l'élève : à transformer en exercice à la
  prochaine passe (l'élève dit où commence la courbe de S avant qu'elle se trace).
- `op_s3_dispersif` garde sa question de définition après la voix ; la décision « dispersif » est maintenant trouvée par
  l'élève sur `op_x3b`.
- Verser l'eau, l'oscilloscope et le spot dans le lexique visuel partagé quand il existera.

## Voix à faire

88 pistes dans `phys_ch2_ondes_periodiques_voix.json` : 15 diapositives (11 réécrites, 4 nouvelles), 49 morceaux de
questions d'observation (7 × énoncé, 2 indices, 3 retours, solution), 15 réactions préparées (ardoises nouvelles de
`op_x1` et `op_x2`), 3 démonstrations, 6 énoncés (dont 3 « retrouver » de bloc, pas joués pour le moment). Les autres
pistes du cours existent et sont gardées (questions inchangées, même texte).

## Défauts anciens corrigés (18 novembre 2026, après la 2ᵉ passe)
- **26 diapositives pilotées par la voix démarraient en `start`** (la scène courait seule, devant ou derrière la voix).
  Elles passent en `reset`. Dans `corde`, `cuve`, `fente`, `stroboscope`, `recepteurs`, `air` et `figures`, `reset` était
  un autre nom de `start` : il fige maintenant la scène, sur zéro ou sur `?depart=<moment>` ; les `play_until` repartent
  de l'instant figé. `bilan.html` n'a pas changé (son `reset` ne lance rien).
- **Huit scènes reprises** sans rechargement s'ouvrent figées : `op_o2b` (`vibreur_demarre`), `op_t2` (`vibreur_demarre`),
  `op_t3` (`m_premier_sommet`), `op_l2` (`photo`, et `reset` : la photo de `op_l1` reste, sans rejouer), `op_c2`
  (`vibreur_demarre`), `op_p2` (`front_atteint_p`), `op_r2` (`vibreur_demarre`), `op_m6` (`opposition`) ; chaque moment
  de départ est avant le premier `play_until` de la diapositive.
- `recepteurs`, `air` et `figures` n'ont pas `set_time` : le kit fige `?depart=` par un `play_until` vers ce moment ; déjà
  figée dessus, la page y reste au lieu de tout rejouer depuis zéro.
- Le cours en ligne ne change pas : sans `?depart=` les pages démarrent comme avant, et aucune diapositive en ligne n'envoie
  `reset` à ces pages. Vérifié dans Chromium (figée, puis arrêtée sur le moment suivant, sans erreur).
- Vérificateur de pointage, copie en attente : 0 « introuvable », 0 DEPART, 0 IFRAME (avant : 0, 26, 8) ; cours en ligne :
  rapport identique.
- **Fiche `bilan.html` illisible au téléphone et sourde à la voix** (18 novembre 2026) : tous ses moments valaient 1, le
  time_s de la fiche, donc le kit jetait chaque `play_until {moment: <bloc>}` ; ils valent maintenant 1,1 à 1,9 (fiche
  1,05, `fin` 1,95, lacunes 2, noms inchangés). La page garde son propre plancher de 15 px (indices compris) et, sur un
  petit écran, se partage en parties (« partie n sur N · touche : la suite ») ; à l'impression, toute la fiche.
- **`op_s1_frequence`, passage à 30 Hz** : dans `cuve.html` (vue `frequence`), `set_parameters {frequence_hz: 30}` plaçait
  la scène sur la mesure finie (`nouvelle_mesure`) ; le `play_until frequence_changee` dit juste après tombait dans le
  passé et était refusé, et le résultat à 30 Hz était à l'écran avant que la voix le montre. Demandé avant la bascule, le
  réglage place maintenant la scène sur l'instant de la bascule : la voix montre les rides se resserrer, puis la nouvelle
  mesure. Vérifié dans Chromium (0,8 s → 1,0 s → 1,15 s → 1,79 s). Corrige aussi le cours en ligne (même page, mêmes moments).
