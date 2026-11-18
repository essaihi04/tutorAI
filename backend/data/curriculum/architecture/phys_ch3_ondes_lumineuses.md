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


## 2ᵉ passe (18 novembre 2026) : le national joué pas à pas

Demande : simple, animé, expliqué ; ne pas tout donner au départ ; laisser l'élève trouver seul ; une raison derrière
chaque choix. Ce qui n'allait pas après la 1ʳᵉ passe : `ol_x2_national_2023` faisait tout le calcul de a à la voix
(l'élève n'avait rien à faire) ; `ol_x3_national_2021` lisait la pente k à la voix avant toute question ; les trois
nationaux étaient des énoncés écrits (`figures.html`), pas des montages animés ; la voix de `ol_c5_cuve` disait la
conclusion (« la longueur d'onde diminue ») avant que l'élève voie la tache se resserrer.

### Une nouvelle simulation : `national.html` (dossier du cours)
Une page neuve plutôt qu'une page modifiée : le cours en ligne ne la voit pas, rien n'y change. Quatre vues, les
valeurs des énoncés, un moment par étape du raisonnement (professeur règle 41, simulations-au-tableau règle 14) :
- `?vue=2023` : laser jaune, fente horizontale (taches sur une ligne verticale), D = 1,4 m, L = 2,7 cm, le triangle
  θ, L/2, D ; puis la source rouge (la tache s'élargit à 3,4 cm). a et λ₀R ne sont jamais écrits.
- `?vue=2021p` : la lumière blanche → spectre ; la radiation jaune, puis la rouge, dans deux barres de verre (λ dans
  le prisme à l'échelle) ; les deux fronts avancent à leur célérité exacte (v = λ·ν), le rouge un peu devant. Les
  célérités ne s'écrivent qu'au moment `vitesses`, jamais joué avant la réponse (`conclusions=0`).
- `?vue=2021c` : l'écran recule (50, 100, 150, 200 cm), chaque mesure pose son point ; la droite par l'origine ; ΔL et
  ΔD en pointillés ; k ne s'écrit qu'au moment `pente_valeur`, joué par la diapositive SUIVANTE (après la réponse) ;
  puis le cheveu (D₁ = 2 m, L₁ = 3 cm).
- `?vue=2025` : la tache dans l'air (2,4 cm), la cuve se remplit, la tache se resserre (1,8 cm, l'ancienne en
  pointillé) ; n n'est écrit qu'au moment `indice`.
`?depart=<moment>` ouvre la scène figée là où la diapositive précédente s'est arrêtée ; `reset` y revient. Dessins
repris de `diffraction.html` et `prisme-dispersion.html` (même boîtier de laser, même fente, même écran, même cuve,
même prisme, le cheveu comme le fil : règle « un objet, un dessin »). Tableau large (téléphone en paysage, lecteur
large) : les lignes écrites sous la figure passent dans une colonne à droite, plus grandes, coupées en deux si besoin.
Texte jamais sous 15 px à l'écran, même à 724 × 350 : la page garde son plancher de 15 px (le kit le baisserait sur un
petit tableau), les puissances de dix sont écrites en trois morceaux (l'exposant garde 15 px), les indices évités
quand la couleur suffit (« λ = 355 nm » sous « jaune »), k écrit 0,02. Vérifiée dans Chromium : aucune erreur, encre
présente, chaque moment atteint, rien hors cadre, chaque texte mesuré ≥ 15 px à tous les moments des quatre vues à
724 × 350 ; captures aussi à 1024 × 560, 1280 × 640 et 1596 × 700, sans chevauchement.

**Réactions préparées** des 7 nouvelles questions (`concentration.reponses.q`) écrites à la main, une par option
(`juste` pour la bonne, `1` indice sans réponse et `2` réponse justifiée pour chaque mauvaise), clés vérifiées contre
`correct` ; chaque mauvaise réaction nomme l'erreur qui donne vraiment ce nombre (L en cm, le 2 oublié, rapport à
l'envers, λ en nm, λ/c, c au lieu de v, ΔD/ΔL, cm sur m, 2·a·k, a en mm, différence au lieu d'un rapport, L'/L).

### Les diapositives : une consigne par bloc, la réponse avant la correction
Chaque exercice du national est coupé en étapes ; chaque étape a sa diapositive, son animation et UNE ardoise « À toi »
(sa question + au plus un exercice), donc son bloc. La correction (`demonstration`) est écrite comme le barème la lit :
relation avec les symboles de l'énoncé, conversion sur sa ligne, une seule application numérique, résultat et unité ;
les unités sont dites en mots. Les distracteurs sont les erreurs réelles (L laissée en cm, le 2 oublié, rapport à
l'envers, λ en nm, ΔD/ΔL à l'envers, unités mélangées, a en mm, L'/L, une différence au lieu d'un rapport).

| Diapo | Animation | L'élève fait | Pourquoi |
|---|---|---|---|
| `ol_x2_national_2023` (réécrite) | montage 2023, mesure de L, triangle | calcule a (60 µm) | la voix ne fait plus le calcul : première lecture, données, figure, puis la consigne |
| `ol_x2b_2023_rouge` (nouvelle) | source rouge : la tache s'élargit, L_R = 3,4 cm | λ₀R par le rapport (730 nm), puis λ dans le milieu (387 nm, exercice repris de la fin de cours) | cas « rapport » (2023 R) et « milieu » joués après le calcul de a |
| `ol_x3_national_2021` (réécrite) | prisme : spectre, puis la radiation jaune | calcule ν_j (5,09·10¹⁴ Hz) | la 1ʳᵉ partie du sujet (prisme, fréquence) n'était pas jouée |
| `ol_x3b_2021_prisme` (nouvelle) | les deux ondes dans le verre, le front rouge devant | calcule v_j et v_r, puis nomme la dispersion (exercice repris) | le cas « dispersion » : la conclusion vient de ses deux calculs, pas d'une phrase |
| `ol_x3c_2021_courbe` (nouvelle) | la courbe L = f(D) se construit point par point | calcule la pente k (2·10⁻²) | la courbe n'est plus un dessin fini : chaque point vient d'une mesure ; k n'est plus dit |
| `ol_x3d_2021_lambda` (nouvelle) | k s'écrit (après la réponse), puis le cheveu | identifie et calcule λ (600 nm), puis d (80 µm, exercice repris) | identification puis fil/cheveu, deux cas types |
| `ol_x4_national_2025` (voix gardée) | air, cuve, liquide, la tache se resserre | QCM 1 et « nommer » (inchangés) | seule la figure change : le montage animé remplace l'énoncé écrit |
| `ol_x4b_2025_indice` (nouvelle) | les deux taches | montre n = L/L' et calcule n (1,33), puis v (exercice repris) | le cas « indice par diffraction » était en fin de cours, non joué |

`ol_c5_cuve` : voix revue (besoin noté à la 1ʳᵉ passe). La voix montre d'abord (« شوف la tache مزيان »), la tache se
resserre sous les yeux de l'élève, puis le chiffre, puis le pourquoi (λ diminue, a et D ne changent pas) ; mots rares
remplacés (« كنعمرو », « صغرات », « ما تبدلاتش » → « كنحطو الما », « ولات صغيرة », « هي هي »).

Séance 7 de la 1ʳᵉ passe coupée en deux (7 : 2023 R et le prisme de 2021 N ; 8 : la courbe de 2021 N, 2025 R, le
bilan) : un bloc par étape, chaque bloc avec son cahier (les lignes du barème) et un `retrouver`. Le cahier de la
diapositive donne la méthode, sans le résultat (il s'ouvre à la demande, avant la réponse) ; le cahier du bloc, montré
après l'ardoise, donne le résultat. 60 diapositives, 26 blocs, 8 séances. Compétences mises à jour (C3–C8).

Les réactions préparées des exercices repris de la fin de cours ont été relues : celles de 2.3 (dispersion) et 3.3
(cheveu) disaient les nombres en arabe, avaient des mots rares (« تقلقش », « فيرجيل », « ميكرومتر ») et un verdict
mal placé ; elles sont réécrites (darija simple, nombres en français, écrit = parole).

### Ce qui avait déjà été fait
Les voix qui invitaient à un exercice absent (`ol_l6`, `ol_c3`, `ol_g3`, notées plus haut) ne finissent plus sur une
consigne dans la copie en attente : rien à faire.

### Ce qui reste
- **Voix** : 75 pistes (8 diapositives, 11 démonstrations, 56 énoncés et réactions, dont les 35 réactions
  préparées des 7 nouvelles questions), liste dans
  `phys_ch3_ondes_lumineuses_voix.json` ; 5 réactions déplacées gardent leur voix. Voix à écouter : les nombres de
  l'énoncé (« quatre-vingt-neuf », « quatre-vingt-onze », « quatre-vingt-cinq », « quatre-vingt-un »,
  « quatre-vingt-sept ») et « violet », « radiations », termes gardés.
- Rejouer les diapositives dans le lecteur avec leur voix (`verifier-pointage-navigateur.mjs`) : quand les voix
  existeront. Sans durée de piste, le contrôle de pointage signale des gestes « trop serrés » (toutes les phrases à
  t = 0) ; avec une durée estimée, aucun écart sur les diapositives nationales.

## Défauts anciens corrigés (18 novembre 2026, après la 2ᵉ passe)
- **50 diapositives démarraient en `start`** (49 pilotées par `play_until` : la scène courait seule, devant ou derrière
  la voix ; plus `ol_t4_relation`). Elles passent en `reset`. Dans `diffraction`, `figures`, `rappels`, `ecart-angulaire`,
  `courbe`, `spectre`, `prisme-dispersion` et `milieu`, `reset` était un autre nom de `start` : il fige maintenant la
  scène, sur zéro ou sur `?depart=<moment>`, et `play_until` repart de là. `indice`, `bilan` et `national` figeaient déjà.
- **Huit scènes reprises** sans rechargement (même adresse que la diapositive d'avant) s'ouvrent figées, chaque moment
  de départ avant le premier `play_until` de la diapositive : `ol_d2_fente_fine` (`point_sur_ecran`), `ol_t4_relation`
  (`mesure_L`, sans `play_until` : la mesure reste à l'écran), `ol_c2_haut_bas` (`tache_centrale`), `ol_c2b_en_bas`
  (`extinctions`), `ol_g4_identifier` (`droite`), `ol_n2_frequence` (`front_entre`), `ol_n3_resserre` (`onde_dans_air`),
  `ol_p2_violet` (`spectre_sur_ecran`). En plus, la vue triangle d'`ecart-angulaire` reprend où la diapositive d'avant
  s'est arrêtée au lieu de tout réécrire depuis zéro : `ol_l3_tan` (`triangle_isole`), `ol_l5_egalite` (`petit_angle`).
- Fractions écrites à plat dans le cahier et les légendes (7) : `k = (26 mm)/(10 mm⁻¹)`, `k = (4 cm)/(200 cm)`,
  `θ = (6,5·10⁻⁷)/(1,0·10⁻⁴)`. La voix ne change pas.
- Le cours en ligne ne change pas : sans `?depart=` les pages démarrent comme avant, et aucune diapositive en ligne n'envoie
  `reset` à ces pages (seul « réécouter » l'envoie, suivi de `start`). Vérifié dans Chromium (figée, puis arrêtée sur le
  moment suivant, sans erreur).
- Vérificateur de pointage, copie en attente : 0 « introuvable », 0 DEPART, 0 IFRAME (avant : 0, 49, 8) ; cours en
  ligne inchangé (52 DEPART, 8 IFRAME, 3 GESTE avant comme après). Vérificateur de formules : 0 (avant : 7).
- **Fiche « Ce qu’il faut retenir » (`bilan.html`) sur téléphone en paysage** : texte à 6 px, la page suivait le plancher
  du kit (abaissé jusqu’à 45 %). Elle garde son plancher de 15 px (indices et exposants compris) et se coupe en parties
  (« partie n sur N · touche : la suite », la voix montre la partie du bloc qu’elle dit) ; ordinateur : une page, comme
  avant ; impression : la fiche entière. Les `play_until {moment: <bloc>}` étaient ignorés par le kit (tous les moments
  à 1 = time_s) : moments 1,01 à 2, noms inchangés. Mesuré : 15 px au moins, 0 chevauchement, de 568 × 300 à 1596 × 700.
