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

**Bloc `wx_s4_b1` — National : lire l'oscillogramme, dater un aspect** [chaque diapo q + ex] — *refait en 2ᵉ passe : un bloc par exercice, voir la section « 2ᵉ passe »*
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

## 2ᵉ passe (18 novembre 2026) — les exercices du national joués pas à pas

**Ce qui n'allait pas encore.** Les six exercices du national avaient leur figure animée (`national.html`), mais :
1. **la voix donnait la méthode avant la réponse** : « la méthode : on marque les débuts, delta t égale n fois la
   sensibilité, puis v égale L sur delta t », et au 2024 R tout le raisonnement des deux chemins (τ = (d − ℓ)/v − ℓ/v),
   écrits au centre avant que l'élève ait rien fait (règle 3 : ne pas tout donner au départ). La diapositive VII.8
   « reconnaître le cas » demandait ensuite de reconnaître seul ce qu'on lui avait toujours annoncé ;
2. **la correction n'était jamais jouée** : les étapes de lecture et de calcul de `national.html` (divisions, retard,
   chemins, pente, trajets, relation, célérité…) existaient, mais aucune diapositive ne les jouait ; rien n'empêchait
   non plus l'élève d'appuyer sur « Reprendre » pendant sa réponse et de voir la réponse s'écrire ;
3. **trois ardoises « À toi » par bloc** (blocs `wx_s4_b1`, `wx_s4_b2`) contre une seule (règle 27 du professeur) ;
4. **un cas type fréquent manquait** : le retard lu sur la courbe y_M(t) (2017 N, 2019 N, 2020 N, 2022 R ; troisième
   cas du national après l'oscillogramme et l'aspect), travaillé en cours (`wx_r1b_elongation`) mais jamais en exercice.

**Ce qui est fait.**
| Changement | Raison |
|---|---|
| Chaque exercice du national = **un bloc de deux diapositives** : l'énoncé joué (le phénomène, les données, **une** consigne), son ardoise (question puis exercice, une consigne à la fois), puis la **correction jouée** sur la figure | Règles 3 et 5 : la réponse de l'élève avant la correction ; la correction écrite comme le barème (relation, application numérique, résultat, unité dite en mots) et vue sur la figure du sujet. Une ardoise par bloc. |
| Voix des six énoncés réécrite : la méthode retirée (voix, centre, puce « Méthode »), la consigne dite seule à la fin (« قرا delta t », « حسب v »…) ; la puce dit « la méthode et la correction viennent après ta réponse » | Ne pas donner la méthode : l'élève reconnaît le cas (préparation de VII.8). La démonstration de l'ardoise et la réaction préparée de la 1ʳᵉ erreur (indice) restent l'aide. |
| 7 diapositives de correction `wx_n1c…`, `wx_n2c…`, `wx_n3c…`, `wx_n7c…`, `wx_n4c…`, `wx_n5c…`, `wx_n6c…` : un `play_until` par étape déjà écrite dans `national.html` (débuts → divisions → τ → chemins → ℓ, etc.), un repère par objet nommé | Professeur règle 41 et simulations-au-tableau règle 14 : chaque lecture et chaque calcul a son arrêt sur image ; ouvertes figées où l'énoncé s'est arrêté (`&depart=`, `demarrer: reset`, règle 39). |
| `national.html` : deux paramètres d'adresse, `&arret=<étape>` (l'énoncé ne joue pas au-delà, bouton compris : « La suite s'écrit après ta réponse ») et `&depart=<étape>` (la correction s'ouvre figée là) | Rien de décisif montré avant la réponse. Sans paramètre, la page fait exactement ce qu'elle faisait : le cours en ligne n'est pas touché (vérifié). |
| Nouvelle vue `national_2022_rattrapage` et nouvel exercice `wx_n7_national_2022r` (VII.4) : la surface de l'eau vue de côté (la ride va de S à M) et la courbe y_M(t) du sujet tracée en même temps ; M reste sur l'axe jusqu'à 10 ms ; la date, τ et v ne s'écrivent qu'à la correction | Cas type manquant ; valeurs du sujet (L = 2,5 cm, amplitude 6 mm, M démarre à 10 ms, v = 2,5 m/s). Les questions du sujet sur N et λ sont du ch2 : dites « au chapitre suivant », non posées. Réactions préparées écrites à la main pour les 6 choix (erreurs réelles : date où la courbe recoupe l'axe, 10 ms = 0,1 s, 1 cm = 10⁻³ m, 2,5 cm = 0,25 m). |
| Ordre : 2022 N, 2024 R, 2024 N, **2022 R (y_M(t))**, 2021 R, 2020 R, 2018 N, puis VII.8 | Le nouveau cas vient après l'aspect (même famille : le retard et le front). |
| VII.8 : « sept exercices », une ligne de plus dans la table des mots-codes (courbe y_M(t) → τ = date où M démarre), voix réécrite | Le regroupement couvre tous les cas joués. |
| Séances : 3 = écho et rédaction, 2022 N, 2024 R ; 4 = 2024 N, 2022 R, 2021 R ; **5 (nouvelle)** = 2020 R, 2018 N, reconnaître le cas, bilan | Blocs de 8 à 10 min (énoncé + ardoise + correction) ; trois blocs par séance, la dernière garde le bilan court. Les ids des anciens blocs sont gardés (`wx_s4_b1` = 2022 N, `wx_s4_b2` = 2021 R) ; les lignes de cahier suivent leur exercice. |
| Mots : « كيصيفط », « متأخر », « معقولة », « نعلمو », « فالحافة », « كيقطع », « التابلو », « كتبعد », « الفيتوس », « spot », « vue », « كيستقبلو », « reprend » remplacés (« كيعطي », « من بعد », « نحددو », « فالبداية ديال الشاشة », « كيمشي », « الجدول », « الجنين », « الضو », « les récepteurs »…) | `verifier_mots.py` : mots vus moins de 3 fois. Gardés : les nombres dits (quatre-vingt-cinq, soixante-huit…), « ell » (le symbole ℓ, déjà dit sans défaut dans l'ancienne voix), « micros », « salve », « écho », « microsecondes » (termes du programme et des sujets). |

**Vérifié.** JSON chargé ; `node --check` et Chromium (Playwright) sur les sept vues avec `arret` / `depart` : aucune
erreur, l'énoncé s'arrête à son étape même si l'élève appuie, chaque correction atteint sa dernière étape ;
`verifier_pointage_simulations.py --ecarts` : aucun nouvel écart (avec des durées de voix estimées, les pistes n'étant pas
faites), cours en ligne identique ; `verifier_formules.py` vide ; pytest « course or cours or concentration » : seul
l'échec SVT préexistant.

**Ce qui reste.** Les voix (29 pistes, ci-dessous) ; les réactions préparées de `wx_n7_national_2022r` sont écrites à
la main (à relire, puis voix) ; rejouer les diapositives dans le lecteur avec la voix posée
(`verifier-pointage-navigateur.mjs`) ; deux repères annoncés par la voix et absents de `types.html` (`dim_corde`,
`dim_son`, sur `wx_i3b_longitudinale`) et les moments `mesure_1`/`mesure_5` que le vérificateur ne voit pas (créés par
une boucle) : déjà là avant cette passe.

## Voix à faire

29 pistes (liste : `phys_ch1_waves_exemple_voix.json`) : 15 diapositives (`mixed/` : les sept énoncés du national
réécrits ou nouveaux, les sept corrections jouées, `wx_b2_national`), et pour `wx_n7_national_2022r` les deux énoncés,
les deux démonstrations et les dix réactions préparées. Mots rares gardés : voir le tableau ci-dessus.

## Défauts anciens corrigés (18 novembre 2026, après la 2ᵉ passe)
- **Scènes qui couraient seules** : `wx_i1_corde`, `wx_r1_retard`, `wx_r2_duree_longueur`, `wx_b3_bilan` démarraient en
  `start`. Elles passent en `reset`, et dans `corde.html` `reset` fige maintenant la scène (avant, c'était un autre nom de
  `start`) : seule la voix la fait avancer.
- **Scènes reprises d'une diapositive à l'autre** (même adresse, l'iframe n'était pas rechargée et la scène restait finie) :
  `types`, `milieux`, `corde`, `micros` et `sonar` acceptent `?depart=<moment>` et s'ouvrent figées sur ce moment.
  `wx_i3b_longitudinale` (`depart=corde`), `wx_c2b_temperature` (`depart=depart`), `wx_r1b_elongation` (`m_atteint`),
  `wx_r2b_dates` (`source_monte`), `wx_m1b_lecture` (`m2_atteint`), `wx_m2b_formule` (`salve_remonte`).
- **Repères et moments écrits en entier** : `dim_corde`, `dim_son` (`types.html`) et `mesure_1` à `mesure_5`
  (`national.html`) étaient fabriqués par le code (`'dim_' + id`), invisibles pour le vérificateur ; ils sont écrits tels quels.
- Légende de la figure du cahier 2021 R : la fraction écrite à plat devient `k = (8×10⁻⁵ s)/(0,4 m)`.
- Le cours en ligne ne change pas : sans `?depart=` les pages démarrent comme avant, et aucune diapositive en ligne n'envoie
  `reset` à ces pages. Vérifié dans Chromium (figée, puis arrêtée sur le moment suivant, sans erreur).
- Vérificateur de pointage, copie en attente : 0 « introuvable », 0 DEPART, 0 IFRAME (avant : 4, 4, 6).
- **Fiche « Ce qu’il faut retenir » sur téléphone** (`ondes-tableau/bilan.html`, 18 novembre 2026) : la page garde son propre
  plancher de 15 px à l’écran (le kit le baissait jusqu’à 45 %) et mesure chaque bloc à la taille vraiment écrite ; quand la
  fiche ne tient pas, elle se partage en parties (« partie n sur N · touche : la suite », jusqu’à un bloc par écran) et
  `play_until {moment: <bloc>}` montre la partie du bloc. Les moments des blocs valent 1,1 à 1,8 (`fin` 1,9) : avant, le kit
  jetait ces `play_until` (time_s = 1), le bloc n’était jamais allumé. Le tableau large (1596 px), vide à cause d’une erreur
  (`largeurTexte`), s’affiche de nouveau. Mesuré dans Chromium : 15 px au moins, 0 chevauchement, à 568 × 300, 724 × 350,
  1024 × 560, 1280 × 640 et 1596 × 700 ; à l’impression, la fiche entière sur une page.
