# Architecture — Propagation d'une onde lumineuse (`phys_ch3_ondes_lumineuses`)

Revue de logique du 18 novembre 2026 (skill `logique-de-cours`). Point de départ : le cours en ligne
`backend/data/courses/phys_ch3_ondes_lumineuses.json` (55 diapositives, audit rythme du 14 novembre, relations du
prisme déjà retirées, toutes les voix faites). Il n'y avait pas de copie en attente. La nouvelle version est dans
`backend/data/courses/en_attente/phys_ch3_ondes_lumineuses.json`. **Une seule piste à refaire** (`ol_c5_cuve`).

## Sources consultées

- **Cadre** : `cadre_reference_2bac_pc.json` → `ondes_lumineuses` (OL1–OL10) ; notion officielle « Propagation d'une
  onde lumineuse (diffraction, aspect ondulatoire, milieux dispersifs, indice de réfraction, relation θ = λ/a) » ;
  `perimetre.json`, `physique.json`. Hors cadre : relations du prisme, Snell-Descartes en calcul, sin θ = λ/a.
- **Profs (vidéos)** : `exploration/ondes_lumineuses.json` (10 cours, dont Laksabi, TOP Physique Chimie…).
- **Cours écrits en ligne (5)** :
  1. Sbiro, moutamadris (PDF 2022) : laser + fente → nature ondulatoire → θ → relation θ–a par des mesures de L(a)
     (coefficient directeur) → L → onde électromagnétique, c, mono / polychromatique, λ₀ = c/ν → indice, réfraction →
     prisme et ses relations → dispersion.
  2. Mahajar & Tabit, moutamadris : activité laser → diffraction → θ = λ/a = L/2D → c, V = λν, visible → indice →
     Descartes → 4 relations du prisme → dispersion. (Erreur dans ce texte : « onde longitudinale électromagnétique ».)
  3. Ahmed Hakim (lycée Ibn Arabi), moutamadris : diffraction → nature électromagnétique, spectre → diffraction
     qualitative puis quantitative (TP, tan θ = d/D, θ = λ/a) → indice, λ dans le milieu → réfraction → prisme →
     dispersion.
  4. Nidal Naceiri Mrabti (livre, tome 1) : activité diffraction → facteurs → θ = f(1/a) → L, trou, fil → mono /
     polychromatique → indice → réfraction → relations du prisme → dispersion (et loi de Cauchy, hors cadre).
  5. Ismaili-Alaoui (2 Bac SM, kezakoo) : même ordre ; relations du prisme démontrées.
  Les cinq traitent les relations du prisme : nous ne les prenons pas (hors cadre PC, 0 national 2016-2025).
- **National** (exploration, `cas_types`) : établir L (2017 R, 2021 N, 2023 R, 2025 R) ; QCM de cours (7 sessions) ;
  milieu, v = c/n, λ = λ₀/n (2021 N, 2023 R, 2025 R) ; fil ou cheveu (2017 R, 2021 N) ; calcul direct (2017 R, 2019 R,
  2023 R) ; variation d'un paramètre (2017 R, 2019 R) ; rapport de deux expériences (2023 R ; 2025 R avec l'indice) ;
  courbe (2021 N L = f(D)) ; dispersion (2021 N, QCM 2023 R, 2024 N) ; indice par diffraction (2025 R) ; calculs
  d'angles du prisme : aucun.

## Ordre commun des profs, et le nôtre

Ordre commun : expérience laser / fente AVANT les relations → la lumière est une onde → θ = λ/a (souvent tirée de
mesures, θ = f(1/a)) → tan θ ≈ θ → L = 2λD/a démontrée → (la lumière, onde électromagnétique : c, mono /
polychromatique, visible, λ₀ = c/ν) → indice n = c/v, λ = λ₀/n → prisme, dispersion.

Notre cours suit cet ordre partie par partie (I diffraction → II θ = λ/a → III L = 2λD/a → IV comparer → V courbes →
VI radiation et spectre → VII milieu d'indice n → VIII dispersion → IX national → X bilan). Écarts gardés ou faits,
avec leur raison :
- rappels enseignés de zéro juste avant leur usage (le radian avant θ, la tangente avant le triangle, **tout en mètre
  avant le premier calcul**) ;
- la cuve du national 2025 ne donne plus n = L/L' avant l'indice : elle passe dans la partie VII (voir plus bas) ;
- prisme seulement qualitatif (cadre).

## Séances, blocs et diapositives

Légende : [q] question « À toi » du bloc, [obs] question d'observation, [ex] exercice. Ids, textes et voix gardés
sauf mention.

### Séance 1 — La lumière se diffracte, l'angle en radian (inchangée)

- **`ol_s1_b1`** : `ol_d1_tout_droit` (le point net d'abord), `ol_d2_fente_fine` [obs] (l'élève voit la lumière
  s'étaler avant le mot « diffraction »), `ol_d3_figure` [q].
- **`ol_s1_b2`** : `ol_d4_onde` (même comportement que l'eau du ch2 → aspect ondulatoire : phrase du national 2025 R),
  `ol_d5_montage` (a, D, L avant toute relation), `ol_d6_fil` [q].
- **`ol_s1_b3r`** : `ol_p1_radian` [q] (rappel juste avant θ), `ol_t1_theta`, `ol_t2_fente_plus_fine` (a varie,
  `diffraction.html` règle a).

### Séance 2 — θ = λ/a, la tangente, le petit angle

**Bloc `ol_s1_b3` — Tout en mètre, la couleur, puis θ = λ/a** (OL2, OL3)
| Diapo | Pourquoi ici |
|---|---|
| `ol_l1_metre` | **Déplacée** (elle était après θ = λ/a, en tête de la partie III) : la question de `ol_t4` (λ = 650 nm, a = 0,10 mm : calcule θ) demande déjà de convertir nm et mm en mètre. Un prérequis juste AVANT son premier usage (règle 6). Elle passe avant `ol_t3` et non entre `ol_t3` et `ol_t4`, pour que « résumons les deux expériences » (`ol_t4`) suive directement la deuxième expérience. |
| `ol_t3_couleur` [obs] | λ varie (rouge, bleu) : l'élève voit la tache bleue plus étroite. |
| `ol_t4_relation` [q] | θ = λ/a après les deux expériences qui la montrent (9 profs sur 10 l'écrivent comme relation du cours). |

**Bloc `ol_s2_bt`** : `ol_p2_tangente` [q] (rappel de zéro, l'échelle contre le mur), `ol_l2_triangle`, `ol_l3_tan`.
**Bloc `ol_s2_b1`** : `ol_l4_petit_angle` [q], `ol_l5_egalite`, `ol_l6_isoler`. Ordre de la démonstration des 10
profs : tan θ = L/2D → θ petit → θ = L/2D → or θ = λ/a → L = 2λD/a.

### Séance 3 — Calculer λ, établir L, comparer deux expériences

- **`ol_s2_b2`** : `ol_l7_calcul_lambda` (rédaction comme le barème), `ol_l8_ordre_grandeur` [q] (contrôle par le
  visible : 8 profs sur 10), `ol_l9_etablir` (« établir L » : 4 nationaux).
- **`ol_s2_b3`** : `ol_c1_qui_change`, `ol_c2_haut_bas`, `ol_c2b_en_bas` [q] (le paramètre varie sur l'animation
  `diffraction.html`, D puis a, avant la règle « en haut / en bas »).
- **`ol_s3_b1` — Deux expériences : le rapport, puis le cheveu** : `ol_c3_rapport` (2023 R), `ol_c4_cheveu` (fil :
  4 nationaux). **Recoupé** : `ol_c5_cuve` et `ol_g1_points` en sortent (voir plus bas).

### Séance 4 — Exploiter une courbe, puis la radiation et c

L'ancien bloc des courbes avait cinq diapositives (`g2, g3, g4, g6, g5`), et la première courbe (`g1`) était rangée
dans le bloc des comparaisons. Règle 7 : au plus quatre diapositives, une idée par bloc. Il est coupé en deux :
- **`ol_s3_b2` — Une fente, un point ; pourquoi 1/a ; la pente et ses unités** : `ol_g1_points` [q] (chaque fente
  donne un point : l'animation `courbe.html` produit les valeurs), `ol_g2_inverse`, `ol_g3_pente`. Nouveau
  `retrouver` et nouvel exercice de bloc (lire k avec ses unités) ; non joués aujourd'hui, pas de voix.
- **`ol_s3_b2b` (nouveau) — Identifier k, vérifier θ = λ/a, les autres courbes** : `ol_g4_identifier`, `ol_g6_theta`,
  `ol_g5_autres` [q] (L = f(D), national 2021 N). Reprend le `retrouver` et l'exercice de l'ancien bloc (k = 2λD).
- **`ol_s3_b3r`** : `ol_r1_monochromatique`, `ol_r2_vide`, `ol_r2b_celerite` [q].

### Séance 5 — Le spectre, la lumière dans un milieu d'indice n

- **`ol_s3_b3` — λ₀ = c/ν et le spectre visible** : `ol_r3_lambda0`, `ol_r4_spectre` [q][ex]. `ol_n1_ralentit` en
  sort : elle ouvre la partie VII et va avec son bloc (une idée par bloc).
- **`ol_s4_b1` — Dans le verre : la lumière ralentit, même fréquence, l'onde se resserre** : `ol_n1_ralentit`,
  `ol_n2_frequence`, `ol_n3_resserre` [q] (`milieu.html` : les compteurs, puis les crêtes resserrées).
- **`ol_s4_b2` — La tache se resserre dans l'eau ; l'indice ; λ = λ₀/n ; n = L/L'** :

| Diapo | |
|---|---|
| `ol_c5_cuve` | **Déplacée et voix réécrite.** Elle était en partie IV et disait : « le rapport des deux largeurs donne un nombre propre au liquide, son indice : n = L/L' ; pourquoi elle se resserre ? on le verra plus tard ». Elle donnait donc une relation et un mot (l'indice) que le cours ne prouve qu'en partie VII (règle 4 : ne jamais affirmer un résultat qu'on montre plus loin). Elle vient maintenant juste après `ol_n3_resserre` : l'élève vient de voir que la longueur d'onde diminue dans un milieu, et l'expérience du national 2025 montre la conséquence (la tache se resserre, L = 2λD/a). Le rapport L/L' est annoncé pour après l'indice. La simulation prend `?vue=cuve&indice=0` : elle n'écrit plus « n = 1,33 », λ = λ₀/n ni n = L/L' (nouveau réglage de `diffraction.html`, sans effet par défaut). |
| `ol_n4_indice` | n = c/v (comparaison à curseur `indice.html`, pas de tableau de valeurs). |
| `ol_n5_lambda_n` | λ = λ₀/n démontrée par la fréquence qui ne change pas. |
| `ol_n6_cuve` | « Retour à la cuve » : n = L/L' démontrée (national 2025 R). Sa voix (« maintenant on sait pourquoi la tache se resserre, et on le montre ») a maintenant son sens : la cuve est vue trois diapositives plus tôt. |

Ce bloc n'a pas de question « À toi » : `ol_n4` à `ol_n6` n'en avaient pas, et en ajouter une demanderait des
réactions et des voix nouvelles. L'exercice de bloc (λ dans l'eau) et le cas national `ol_x4_national_2025` (fin de
cours) le travaillent.

### Séance 6 — La dispersion de la lumière blanche

L'ancien découpage mettait `ol_n5`, `ol_n6` (indice) et `ol_p1`, `ol_p2` (prisme) dans le même bloc. Il est recoupé
par notion :
- **`ol_s4_b3` — La lumière blanche dans un prisme** : `ol_p1_blanche` [q] (2021 N), `ol_p2_violet`,
  `ol_p3_deux_celerites` (deux fronts dans le même verre, `milieu.html?vue=deux`). Nouveau `retrouver` et nouvel
  exercice (la radiation la plus déviée) ; la figure du cahier « le prisme disperse la lumière blanche » suit ces
  diapositives.
- **`ol_s4_b4` (nouveau) — Milieu dispersif, et la fente en lumière blanche** : `ol_p4_dispersif` (la définition après
  les expériences, trois étapes comme au bac), `ol_p5_fente_blanche` [q]. Reprend le `retrouver` (définition) et
  l'exercice de l'ancien bloc.

### Séance 7 — Le national et le bilan

- **`ol_s5_b1`** : `ol_x1_cas_types`, `ol_x2_national_2023`, `ol_x3_national_2021`, `ol_x4_national_2025` [q][ex]
  (figures des énoncés jouées étape par étape par `figures.html`).
- **`ol_s5_b2`** : `ol_b1_bilan`, `ol_b2_carte`.

Sept séances au lieu de six : les blocs recoupés font 19 blocs. Séance 6 (dispersion) est courte (5 diapositives),
mais la mettre avec le national aurait donné une séance de 11 diapositives, dont quatre exercices longs (séances de 40
à 50 min, règle 7).

## Ce qui change par rapport au cours en ligne

| Changement | Raison |
|---|---|
| `ol_l1_metre` avant `ol_t3_couleur` (partie II) | Prérequis avant son premier usage (calcul de θ). |
| `ol_c5_cuve` après `ol_n3_resserre` (partie VII), voix réécrite, simulation `&indice=0` | Plus de relation ni de mot affirmés avant leur preuve ; le phénomène vient juste après ce qui l'explique. |
| `diffraction.html` : réglage `indice=0` pour la vue cuve | La simulation ne doit pas écrire ce que la voix ne dit pas encore. Par défaut rien ne change (`ol_n6_cuve` et le cours en ligne). |
| Blocs recoupés : courbes en deux blocs (`ol_s3_b2`, `ol_s3_b2b`), `ol_n1` avec le milieu, l'indice séparé du prisme, la dispersion en deux blocs (`ol_s4_b3`, `ol_s4_b4`) ; 7 séances | Au plus quatre diapositives et une idée par bloc. Ids des anciens blocs gardés. |
| Explications écrites de `ol_l6_isoler`, `ol_c3_rapport`, `ol_g3_pente` sans consigne finale | Une explication n'invite jamais à un exercice absent du tableau ; la voix ne le disait pas. |
| Réaction écrite de `ol_c2b_en_bas` : « lambda » → λ, « L = 2 lambda D/a » → L = 2λD/a | Lettres grecques et fraction à l'écrit (`verifier_formules.py`). |

## Ce qui reste, et ce qui n'a pas été fait

- Trois explications écrites finissaient par une consigne sans question au tableau (« Isole lambda. » `ol_l6_isoler`,
  « … calcule lambda deux. » `ol_c3_rapport`, « … calcule k en mètre carré. » `ol_g3_pente`). Ces phrases n'étaient que
  dans `speech_text.fr` (« 📖 Explication écrite ») : la voix enregistrée (`speech_text.mixed`) ne les dit pas. **Corrigé** :
  la consigne est retirée du texte écrit, qui suit maintenant ce que dit la voix ; l'écran donne déjà le résultat
  (λ₂ ≈ 730 nm, k = 2,6·10⁻⁶ m², les quatre formes isolées). Aucune piste à refaire.
- `ol_l8_ordre_grandeur` utilise le domaine visible (400–800 nm) avant la partie VI qui l'enseigne. Il est dit comme
  valeur repère avec le spectre animé (`spectre.html`), et repris en `ol_r4_spectre`. C'est gardé : c'est la
  vérification que 8 profs sur 10 font dès le premier calcul de λ.
- Le bilan et la carte gardent leur ordre.

## Voix à faire

Une piste : `mixed/ol_c5_cuve` (liste : `phys_ch3_ondes_lumineuses_voix.json`). Mot rare gardé : « largeurs »
(terme du chapitre, déjà dans l'ancienne voix).
