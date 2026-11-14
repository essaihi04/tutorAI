# Audit « rythme et départ de zéro » — Physique, chapitres 1 à 5 (14 novembre 2026)

Règles appliquées : professeur 33 (une chose à la fois, le résultat décisif trouvé par l'élève) et 34 (départ de zéro, deux explications), avec 27, 28, 30, 32 ; skills `cours-concentration` et `voix-du-cours`. Consignes : `docs/audit-rythme/BRIEF.md`.

Les cours en ligne ne sont pas modifiés. Les nouvelles versions complètes sont dans `backend/data/courses/en_attente/<deck>.json`. Ce dossier n'est servi ni par le site ni par le lien libre. Sur chaque diapo dont la voix change, ou qui est nouvelle, `audio.mixed` est retiré. Rien n'est commité, poussé ni déployé.

## Résumé

| Cours | Diapos (en ligne → en attente) | Rappels enseignés de zéro | Diapos coupées | Questions d'observation ajoutées | Simulations | Pistes à enregistrer |
|---|---|---|---|---|---|---|
| ch1 `phys_ch1_waves_exemple` (servi aux élèves) | 16 → 22 | la vitesse ; la milliseconde et 10⁻³ | I.3, II.2, V.1, V.3 | 1 (sonar : 2d) | `ondes-tableau/rappels.html` (nouvelle) ; `sonar.html` + `conclusions` | 30 |
| ch2 `phys_ch2_ondes_periodiques` | 47 → 52 | la sinusoïde ; 10⁻³, milli, micro | o2, m6, r3 | 2 (diffraction ; même période) | `ondes-periodiques-tableau/rappels.html` (nouvelle) ; `fente.html` + `conclusions` | 22 |
| ch3 `phys_ch3_ondes_lumineuses` | 53 → 57 | le radian ; la tangente ; c (ordre de grandeur) | c2 | 1 (couleur : tache bleue) | `ondes-lumineuses-tableau/rappels.html` (nouvelle) ; `diffraction.html` + `conclusions`, `trace_precedente` | 33 |
| ch4 `phys_ch4_radioactivite` | 52 → 59 | l'atome refait de zéro ; l'exponentielle ; puissances de dix ; la mole | s4, r2, l4, a3, c4 | 2 (proportion constante ; arbre coupé) | `radioactivite-tableau/rappels.html`, `chauffer.html` (nouvelles) ; `population.html`, `datation.html` + `conclusions` | 27 |
| ch5 `phys_ch5_energie_nucleaire` | 38 → 46 | l'énergie et le joule ; puissances de dix ; charges qui se repoussent | m2, m3, a2, b2, n1 | 2 (balance ; fusion) | `energie-nucleaire-tableau/rappels.html` (nouvelle) ; `balance.html`, `reactions.html` + `conclusions` | 45 |

Total : **157 pistes Bodi**. Elles se répartissent en diapos, énoncés, démonstrations, textes des questions d'observation et réactions des nouvelles questions. Le détail est dans chaque chapitre, à la section « Voix à enregistrer ».

Les simulations existantes ont été enrichies sans rien casser : chaque nouveau paramètre vaut par défaut le comportement d'aujourd'hui, car le cours en ligne les utilise encore.

### Ce qui reste à vérifier pour les cinq cours

- Jouer chaque copie en attente dans le lecteur, panneau visible : arrêts sur les mots, arrêt de la voix sur `apres_mot`, envoi de `conclusions`, bande « 👀 Observe ».
- Enregistrer les voix Bodi, puis passer `detecter_murmures.py`.
- Lancer `controler_cadre.py` (fait seulement pour le ch5) et `preparer_reponses.py verifier`.
- Les exercices de bloc nouveaux n'ont pas tous leurs réactions préparées (ch1, ch3 et ch5 en partie). Ces exercices ne sont pas joués aujourd'hui.
- Trois blocs du ch4 n'ont aucune « À toi » (`ra_s2_b3`, `ra_s3_b2`, `ra_s5_b2`) ; deux d'entre eux portent une question d'observation.
- Le vérificateur signale encore trois repères absents : `dim_corde` et `dim_son` (ch1), `lambda_carbone` (ch4). Ce sont de fausses alertes : ces repères sont construits par le code des simulations.

## Chapitre 1 — Ondes mécaniques progressives (`phys_ch1_waves_exemple`)

**Ce cours est servi aux élèves connectés** (`remplace_la_base: true`). Le fichier en ligne n'est pas touché. La copie en attente, `backend/data/courses/en_attente/phys_ch1_waves_exemple.json`, est complète : elle passe de 16 à 22 diapos et de 2 à 3 séances. Elle est produite par `scratchpad/phys15/build_phys_ch1_waves_exemple.py`, qui repart toujours de la copie en ligne. Toutes les diapos non citées gardent leur voix et leur piste.

Constat général : le cours exemple avait déjà ses arrêts sur image et une question d'observation (II.2). Trois problèmes restaient :
- quatre diapos enchaînaient plusieurs idées ou expériences ;
- deux prérequis étaient utilisés comme connus : la vitesse v = d / Δt, et la milliseconde avec 10⁻³ ;
- le résultat décisif du sonar (l'onde parcourt deux fois d) était dit par la voix au lieu d'être trouvé par l'élève.

### Diapo par diapo

| Diapo | Ce qui n'allait pas | Ce qui a été fait |
|---|---|---|
| `wx_o1_bouee` | La voix finit par « dis-moi ce que tu prédis », alors que l'étape de prédiction est supprimée (règle du 13 novembre). | Laissée : changer la voix demande une nouvelle piste. **À revoir** au prochain enregistrement. |
| `wx_i3_types` (I.3) | Trop vite : cinq idées d'un coup (transversale, longitudinale, le son, le vide, les dimensions). Chaque notion n'est dite qu'une fois. | Coupée. `wx_i3_types` ne garde que l'onde **transversale**, dite deux fois : la corde, puis une personne debout dans l'eau qui monte et descend sur place quand la vague passe. La définition est relue. Un arrêt sur la corde. |
| — nouvelle `wx_i3b_longitudinale` (I.4) | — | Le ressort, puis le son dans l'air (longitudinal, pas dans le vide). Deuxième façon : l'air devant la bouche quand on parle. Puis la dimension (1, 2, 3). Un arrêt par phase (`ressort`, `son`, `fin`), même simulation `types.html`. Elle porte la « À toi » du bloc : « Le son dans l'air est une onde… », avec les réactions juste / faux 1 / faux 2. |
| `wx_c1_celerite` | Prérequis supposé : la vitesse v = d / Δt, donnée comme connue. | Nouvelle diapo avant, `wx_p1_vitesse` « Rappel : la vitesse ». Une voiture peinte parcourt 100 m en 5 s, chronomètre à l'appui : v = d / Δt = 20 m/s. Deuxième façon : un trait par seconde, « chaque seconde elle avance de 20 m ». Puis le lien avec le son (340 m en une seconde). Nouvelle simulation `rappels.html?vue=vitesse`. |
| `wx_c2_facteurs` (II.2) | Trop vite : nature du milieu, température, corde (tension, masse) et force de la frappe dans une seule voix. Une seule explication de « pourquoi plus vite dans un solide ». | Coupée. `wx_c2_facteurs` garde la nature du milieu et sa question d'observation, inchangée (`apres_mot` identique). La voix ajoute une deuxième explication (parties de la matière proches ou éloignées) et la valeur de l'acier. |
| — nouvelle `wx_c2b_temperature` (II.3) | — | La température : le tuteur règle l'air à 40 °C, le son arrive plus tôt. Puis la corde (tension, masse). Puis la frappe plus forte : piste du bas, même arrivée, la célérité reste la même. La relecture finale dit que la célérité dépend du milieu, pas de la source. Simulation `milieux.html`, sans modification. |
| `wx_m1_micros` (V.1) | Prérequis supposé : la milliseconde et 10⁻³ (la conversion ms → s est exigée sans être enseignée). | Nouvelle diapo avant, `wx_p2_milli` « Rappel : la milliseconde ». Un chronomètre peint, une barre d'une seconde coupée en mille : 1 ms = 10⁻³ s, puis 2 ms = 2 × 10⁻³ s. Deuxième façon : la virgule recule de trois rangs, 0,002 s. Elle porte la « À toi » du bloc : « 3 ms en seconde ? », avec sa démonstration et les réactions des trois options. Nouvelle simulation `rappels.html?vue=milli`. |
| `wx_m1_micros` (V.1) | Trop vite : le principe du TP et toute la lecture de l'oscilloscope (sensibilité, divisions, τ, v, vérification) dans une seule voix. Repère cassé : le mot « بدل البلاصة ديال M deux » n'était pas dans la voix. | Coupée. `wx_m1_micros` = le **principe**, sans calcul : le son arrive à M₁ puis à M₂, ce retard est τ. Un arrêt par étape (`son_part`, `m1_atteint`, `m2_atteint`, `mesure`). Deuxième façon : deux amis au bord d'une route et une voiture qui passe. |
| — nouvelle `wx_m1b_lecture` (V.2) | — | La lecture pas à pas : sensibilité, divisions, τ, v, puis la vérification (340 m/s). Deuxième façon : une division est un morceau de règle. Elle reprend la variante, le centre et la figure du cahier d'origine. Le repère cassé est réparé : la phrase « بدل البلاصة ديال M deux » est maintenant dans la voix. |
| `wx_m2_sonar` (V.3) | Deux idées d'un coup : les ultrasons, puis le sonar avec la formule. Le résultat décisif (deux fois d) était dit par la voix ; la simulation écrivait « 2d = v·τ » dès l'écho. « Hertz » n'était jamais expliqué. | Coupée. `wx_m2_sonar` = ultrasons (le hertz dit en une phrase), puis la salve descend, se réfléchit et remonte. **Question d'observation** après « دابا تبع الطريق ديال le signal كامل. » : « Entre l'émission et l'écho, combien de fois l'onde a-t-elle parcouru la profondeur d ? ». Le tuteur joue l'écho ; 2 indices, le second pointe la cote d ; 3 cartes (d, 2d, d/2) ; `sim_avant: {conclusions: false}`. La voix confirme ensuite, avec une deuxième image (aller à l'épicerie et rentrer). |
| — nouvelle `wx_m2b_formule` (V.4) | — | 2d = v·τ, puis d = v·τ / 2, écrits au centre quand ils sont dits. Deuxième façon : l'aller seul dure τ/2. Puis le piège du « / 2 » et la manip (glisser le fond). Reprend la variante d'origine. |
| `wx_l1_aspect`, `wx_l2_sens`, `wx_r1_retard`, `wx_r2_duree_longueur` | Une idée par diapo, arrêts déjà posés. | Laissées. |
| `wx_b1_redaction`, `wx_b2_national`, `wx_b3_bilan`, `wx_b4_carte` | Méthode et bilan. Le bilan reprend toutes les notions, ce qui est son rôle. | Laissées. |

### Séances et blocs

Les ids des blocs dont le contenu ne change pas sont gardés, pour que la progression des élèves reste valable.

- **Séance 1** (`wx_s1`), L'onde, ses deux types et sa célérité :
  - `wx_s1_b1` (inchangé) : o1, i1, i2 ;
  - `wx_s1_b2` : i3, **i3b** (« À toi »), **p1** ;
  - **`wx_s1_b2b`** : c1 (« À toi »), c2 (observation), **c2b**.
- **Séance 2** (`wx_s2`), Le retard, lire une onde, mesurer :
  - `wx_s1_b3` (inchangé, déplacé) : r1, r2, l1, l2 ;
  - `wx_s2_b1` : **p2** (« À toi »), m1, **m1b** ;
  - **`wx_s2_b1b`** : m2 (observation), **m2b**, b1 (« À toi »).
- **Séance 3** (`wx_s3`, nouvelle) : `wx_s2_b2` (inchangé) : b2, b3, b4.

Toujours une seule diapo avec « À toi » par bloc. Le cahier, `retrouver` et l'exercice sont réécrits pour `wx_s1_b2`, `wx_s2_b1` et `wx_s2_b1b`. Le nouvel exercice du sonar (`wx_s2_b1b`) a sa démonstration, mais pas de réactions préparées : les exercices de bloc ne sont pas joués aujourd'hui.

Compétences :
- i3b → C2 ;
- p1 et c2b → C3 ;
- p2 et m1b → C7 ;
- m2b → C8.

### Simulations

- **Nouvelle** : `ondes-tableau/rappels.html`, avec deux vues.
  - `vitesse` : route, voiture et chronomètre peints. Moments `depart`, `une_seconde`, `arrivee`, `formule`, `par_seconde`, `son`. Paramètre `set_parameters {duree_s: 4|5|10}`.
  - `milli` : chronomètre peint, barre d'une seconde coupée en mille. Moments `chrono`, `mille`, `une_ms`, `deux_ms`, `virgule`.
  - Les deux vues ont leurs repères, `ce_qui_se_voit` et le protocole complet.
- **Enrichie sans rien casser** : `ondes-tableau/sonar.html` accepte `conclusions` (vrai par défaut).
  - À faux : ni « 2d = v·τ », ni « d = v·τ / 2 », ni l'avertissement ne s'écrivent.
  - La bulle et `ce_qui_se_voit` taisent aussi la formule.
  - Les flèches aller et retour restent, puisque c'est ce qu'il faut regarder.

### Vérification

- `verifier.py` passe : JSON, fins de ligne LF, chaque `mot` du pointage et du centre est dans sa voix, `apres_mot` est trouvé une seule fois, les moments et les repères cités existent, une seule « À toi » par bloc, `audio.mixed` est retiré des 10 diapos dont la voix change, pas de chiffre ni de tachkil dans les voix.
  - Deux fausses alertes : `dim_corde` et `dim_son`. Ces repères sont construits par `types.html` (`'dim_' + id`) ; ils étaient déjà dans le cours en ligne.
- `node --check` passe sur `rappels.html` et `sonar.html`.
- Playwright avec Chrome sans écran : les deux vues de `rappels.html` jusqu'au dernier moment, et `sonar.html` avec `conclusions: false`, puis `true`, puis par défaut. Aucune erreur console, rien hors cadre. Pendant la question, la formule n'est pas écrite ; elle revient à `true`.
- `verifier_texte_corpus.py` : les mots darija rares des nouvelles voix ont été remplacés. Il reste :
  - des termes du programme gardés exprès : spire, perpendiculaires, Celsius, piste, signaux ;
  - trois mots repris de la voix déjà enregistrée du sonar : الودن, كتسمعش, كيصيفط ;
  - « كيحرك » (2 occurrences dans le corpus).

### Voix à enregistrer (Bodi) — chapitre 1

**Diapos (10 pistes)** : `wx_i3_types`, `wx_i3b_longitudinale`, `wx_p1_vitesse`, `wx_c2_facteurs`, `wx_c2b_temperature`, `wx_p2_milli`, `wx_m1_micros`, `wx_m1b_lecture`, `wx_m2_sonar`, `wx_m2b_formule`.

**Énoncés et démonstration (3 pistes)** :
- `wx_i3b_longitudinale` : énoncé « شوف هاد السؤال: le son dans l'air est une onde، شنو هي؟ » ;
- `wx_p2_milli` : énoncé « شوف هاد السؤال: une durée vaut trois millisecondes. en seconde، شحال كتساوي؟ » ;
- `wx_p2_milli` : sa démonstration (`question.demonstration.parole`).

**Réactions préparées (10 pistes)** :
- `wx_i3b_longitudinale` : option 0 → 1 et 2 ; option 1 → juste ; option 2 → 1 et 2 ;
- `wx_p2_milli` : même découpage.

Les textes sont dans `concentration.reponses.q`.

**Question d'observation de `wx_m2_sonar` (7 pistes)** :
- énoncé « شوف مزيان الطريق ديال le signal، من le bateau حتى رجع. شحال من مرة قطع la profondeur d؟ » ;
- indice 1 « تبع le signal: فين مشا اللول؟ ومن بعد فين مشا؟ » ;
- indice 2 « شوف جوج ديال les flèches حدا la profondeur d: ملي مشا، وملي رجع. » ;
- trois retours (d / 2d / d÷2) et la solution, dans `concentration.observation`.

Total chapitre 1 : **30 pistes**.


## Chapitre 2 — Ondes mécaniques progressives périodiques (`phys_ch2_ondes_periodiques`)

Copie en attente : `backend/data/courses/en_attente/phys_ch2_ondes_periodiques.json` (47 → 52 diapos). Script : `scratchpad/phys15/build_phys_ch2_ondes_periodiques.py` (repart de la copie en ligne). Le cours en ligne n'est pas modifié.

Constat général : ce cours avait déjà été construit pas à pas (une idée par diapo presque partout, un `play_until` par phase). Les défauts restants sont des diapos de rappel ou de méthode qui enchaînent plusieurs idées, deux prérequis de collège / tronc commun utilisés sans être enseignés, et deux résultats décisifs dits par la voix alors que la simulation permet à l'élève de les trouver.

### Diapo par diapo

| Diapo | Ce qui n'allait pas | Ce qui a été fait |
|---|---|---|
| `op_o2_acquis` « Ce qu'on sait déjà » | Trop vite : trois rappels (front, célérité, retard) **plus** la photo et le film, cinq idées d'un coup ; la célérité dite une seule fois. | Coupée en deux. `op_o2_acquis` = le front et la célérité seulement, expliquée deux fois (v = d / Δt, puis « le nombre de mètres que le front avance en une seconde », la voiture à 90 km/h). Nouvelle `op_o2b_retard` = le retard (deux façons : τ = d / v, puis « plus M est loin, plus il attend »), puis la photo et le film ; un arrêt sur image par phase (M au repos, front arrivé, M monte, M revenu). |
| `op_o5_sinusoidale` | Prérequis supposé : « la corde prend une forme connue, la sinusoïde ». Beaucoup d'élèves ne savent plus ce qu'est une sinusoïde. | Nouvelle diapo avant : `op_pr1_sinusoide` « Rappel : la sinusoïde, un dessin qui se répète » — une grande roue peinte, la hauteur de la cabine rouge tracée en fonction du temps (un tour = un motif, le deuxième tour refait le même dessin), puis la deuxième façon : une vague régulière, l'enfant sur la balançoire. Nouvelle simulation `rappels.html?vue=sinusoide`. |
| `op_t2_meme_periode` | Résultat décisif donné : « le chrono indique encore zéro virgule cinq seconde » alors que l'élève peut le lire lui-même. | Question d'observation (règle 30) après « وكترجع لنفس الحالة. » : « M est deux fois plus loin de la source : que vaut sa période ? » (le tuteur pointe le chrono ; 2 indices ; 3 cartes). La phrase suivante de la voix confirme la réponse. Voix inchangée, piste gardée. |
| `op_t5_convertir` | Prérequis supposé : dix puissance moins trois, milli, micro donnés comme une liste à retenir, sans dire ce qu'ils veulent dire. | Nouvelle diapo avant : `op_pr2_puissances` « Rappel : dix puissance moins trois, milli et micro » — une règle d'un mètre peinte coupée en mille (loupe sur les millimètres), puis la deuxième façon (10⁻³ = 0,001, la virgule recule de trois rangs), puis le chronomètre : la seconde coupée en mille (ms), la milliseconde coupée encore en mille (µs). Nouvelle simulation `rappels.html?vue=puissances`. `op_t5_convertir` garde son rôle (centi, et « on convertit sur la ligne où on lit »). |
| `op_m6_nieme` | Trop vite : le n-ième retour en phase, puis les récepteurs déjà écartés, le calcul de λ, puis v, dans la même voix. | Coupée en deux. `op_m6_nieme` = n retours en phase, n λ, λ = d / n, dit deux fois (la deuxième avec l'escalier : chaque retour est une marche de λ), sur `recepteurs.html?vue=reculer` (arrêts `en_phase_1`, `en_phase_2`). Nouvelle `op_m6b_deja_ecartes` = récepteurs déjà écartés, le déplacement d₂ − d₁, λ puis v ; elle porte la question du bloc (déplacée telle quelle avec ses réactions et pistes). |
| `op_d1_ouverture` | Résultat décisif donné : la voix dit « des arcs de cercle partent » au moment où l'élève pourrait le voir ; la simulation écrit aussi « onde diffractée » et la phrase de la diffraction. | Question d'observation après « دابا نديرو الفتحة صغيرة. » : « L'ouverture est maintenant étroite : que fait l'onde après l'ouverture ? » (gestes : a = 1 cm, jusqu'à `quatre_arcs` ; 2 indices, le second pointe `onde_diffractee` ; 3 cartes). `fente.html` accepte maintenant `conclusions: false` (n'écrit ni « onde diffractée / diaphragmée », ni la phrase verte, ni le message final) ; par défaut rien ne change. Voix inchangée, piste gardée. |
| `op_r3_trois_lectures` | Trop vite : τ, T, l'amplitude, puis N, v et λ calculés dans la même diapo (six résultats). | Coupée en deux. `op_r3_trois_lectures` = les trois lectures seules, un arrêt de la figure par lecture (`retard`, `periode`, `amplitude`). Nouvelle `op_r3b_calculs` = les trois calculs, une ligne à la fois, avec « τ sert pour v, T pour N et λ » ; elle porte la question et l'exercice du bloc (déplacés avec leurs réactions et pistes). |
| `op_s1_frequence` | Repère cassé : le mot `كتبناها فالجدول. سؤال:` n'est pas dans la voix. | Corrigé en `كتبناها فالجدول.` (voix inchangée). |
| `op_s1_frequence`, `op_s2_air` | Deux mesures chacune, mais chaque mesure a déjà son propre arrêt (`regle_posee` / `nouvelle_mesure`, `mesure_lambda` / `comparaison`) et son calcul écrit au moment où il est dit. | Laissées telles quelles (pas de deuxième question d'observation : le cours en a deux, le maximum). |
| `op_x1`, `op_x2`, `op_x3` (cas du national) | Quatre lectures chacune, mais ce sont des corrections d'exercice déjà vues une par une dans le cours ; la figure s'écrit étape par étape. | Laissées. |

Blocs : `op_s1_b1` = o1, o2, **o2b**, o3 ; `op_s1_b2` = o4, **pr1**, o5, t1 ; `op_s2_b1` = **pr2**, t5, t6, t7 ; `op_s4_b1` = m4, m5, m6, **m6b** ; `op_s5_b1` = r1, r2, r3, **r3b**. Toujours une seule diapo avec « À toi » par bloc. Lignes de cahier ajoutées (sinusoïde ; milli / micro ; déplacement d₂ − d₁ ; N, v, λ). Compétences : pr1 → C1, pr2 → C2, m6b → C6, o2b et r3b → C9.

Vérification : `verifier.py` OK (JSON, LF, chaque `mot` dans sa voix, `apres_mot` trouvé une fois, moments et repères présents, blocs, pas de chiffre ni de tachkil dans les nouvelles voix, `node --check`). `rappels.html` (deux vues) et `fente.html` (`conclusions: false`) ouverts dans Chrome sans écran (Playwright) : aucune erreur, aucun texte hors cadre, rien d'écrit sur la diffraction pendant la question. Non vérifié : la lecture dans le lecteur du cours (le tuteur, les arrêts sur les mots), le corpus de la voix (`verifier_texte_corpus.py` non lancé) — mots à surveiller : « الروضة » (grande roue), « المرجوحة », « الدروج ».

### Voix à enregistrer (Bodi) — chapitre 2

Diapos (8 pistes) : `op_o2_acquis`, `op_o2b_retard`, `op_pr1_sinusoide`, `op_pr2_puissances`, `op_m6_nieme`, `op_m6b_deja_ecartes`, `op_r3_trois_lectures`, `op_r3b_calculs`.

Questions d'observation (pistes `enonce_audio`, `indices[].audio`, `retours[].audio`, `solution.audio`) :
- `op_d1_ouverture` — énoncé dit : « دابا الفتحة صغيرة. شوف مزيان l'onde من بعد الفتحة. شنو كدير؟ » ; indices : « قارن مع الفتحة الكبيرة: واش l'onde باقا كتمشي نيشان؟ », « شوف الشكل ديال الموجات من ورا الحاجز، دايرين بالفتحة. » ; retours (3) et solution : voir `concentration.observation`.
- `op_t2_meme_periode` — énoncé dit : « M دابا بعيدة جوج مرات. شوف le chrono. شحال كتساوي la période ديالها؟ » ; indices : « قبل، قريب من la source، le chrono كان كيقول zéro virgule cinq seconde. », « قرا le chrono ملي M كترجع لنفس الحالة: نفس العلو، ونفس الاتجاه. » ; retours (3) et solution.

Questions : aucune nouvelle. Les questions de `op_r3b_calculs` (et son exercice) et de `op_m6b_deja_ecartes` sont celles de `op_r3_trois_lectures` et `op_m6_nieme`, déplacées avec leur énoncé, leur démonstration et leurs réactions déjà voixées : rien à réenregistrer.

Total : 8 pistes de diapo + 2 × (1 énoncé + 2 indices + 3 retours + 1 solution) = 8 + 14 = **22 pistes**.


## Chapitre 3 — Les ondes lumineuses (`phys_ch3_ondes_lumineuses`)

Copie en attente : `backend/data/courses/en_attente/phys_ch3_ondes_lumineuses.json` (57 diapos au lieu de 53), fabriquée par `build_phys_ch3_ondes_lumineuses.py` à partir de la copie en ligne (jamais modifiée). Vérifications : `verifier.py` OK (pointage dans la voix, `apres_mot` trouvé une fois, moments et repères présents dans les simulations, une seule « À toi » par bloc, audio retiré là où la voix change, `node --check`), `verifier_figures_cahier.py` 0 erreur 0 avertissement, `verifier_texte_corpus.py` : dans les nouvelles voix, il ne reste que des termes du programme (adjacent, opposé, radian, triangle, nanomètres…) et « pizza », « tours », « l'arc », « violet ».

### Diapo par diapo

| Diapo | Ce qui n'allait pas | Ce qui a été fait |
|---|---|---|
| ol_d1 → ol_d3 | Rythme correct ; ol_d2 a déjà sa question d'observation (la tache s'élargit). | Rien. |
| ol_d4_onde | « seules les ondes se diffractent » donné, mais il s'appuie sur la cuve du ch2 déjà vue. | Rien. |
| ol_d5_montage | Trois longueurs a, D, L d'un coup (dites une fois). | Gardée : chaque longueur revient seule dans la suite (t2, c2, c2b). Noté. |
| **ol_t1_theta** | **Prérequis supposé : l'angle en radian.** θ est dit « en radian » dès ici et dans tout le chapitre (θ = λ/a, tan θ ≈ θ), alors que l'élève ne sait plus ce qu'est un radian. | **Nouvelle diapo avant : `ol_p1_radian`** « Rappel : l'angle en radian » — une pizza peinte (`rappels.html?vue=radian`) : le rayon, un arc de croûte égal au rayon = 1 rad ≈ 57°, θ = s/R, le demi-tour = π rad = 180°, puis une part très fine (θ ≈ 0,0065 rad comme en diffraction). Deux explications : la règle θ = s/R, puis « le radian compte combien de rayons tiennent sur l'arc ». Une question (arc = 2R → 2 rad) avec démonstration. |
| ol_t2_fente_plus_fine | Une expérience, une conclusion : correct. | Rien. |
| **ol_t3_couleur** | **Résultat décisif donné** : « la tache bleue est plus étroite » est dit par la voix ; l'élève ne compare rien lui-même. Notion dite une seule fois. | **Question d'observation ajoutée** (2ᵉ du cours) : la voix s'arrête après « الخط ديال النقط، هو la tache الحمرا اللي كانت قبل », la tache bleue se dessine à côté du pointillé de la tache rouge, l'élève dit si elle est plus large, plus étroite ou pareille. Voix réécrite (même déroulé) + deuxième explication : « plus la longueur d'onde est grande, plus la lumière s'écarte du centre derrière la fente ». `diffraction.html` enrichi (additif) : `trace_precedente` (la tache d'avant reste en pointillé, repère `tache_avant`) et `conclusions: false` (les valeurs L et θ ne s'écrivent pas pendant la question). |
| ol_t4_relation | Correct (résume les deux expériences). | Rien. |
| ol_l1_metre | Puissances de dix supposées connues (nm, µm…) ; elles sont redites en une ligne chacune. Virgule arabe parasite dans la voix (« nanomètres، égale »). | Non réécrite (piste gardée). Noté pour la prochaine voix. |
| **ol_l2_triangle / ol_l3_tan** | **Prérequis supposé : la tangente** (opposé, adjacent, triangle rectangle) — ol_l3 dit « quel rapport relie l'opposé et l'adjacent ? c'est la tangente » comme si c'était connu. | **Nouvelle diapo avant : `ol_p2_tangente`** « Rappel : la tangente d'un angle » — une échelle en bois contre un mur de briques (`rappels.html?vue=tangente`) : le triangle rectangle, θ au pied, le côté adjacent (collé), le côté opposé (en face), tan θ = opposé/adjacent = 3/4 ; deuxième explication : « de combien l'échelle monte pour un mètre au sol » ; on éloigne le pied : θ et tan θ diminuent. Question : pied à 2 m, mur 3 m → 1,5 (démonstration). |
| ol_l4_petit_angle | Tan θ ≈ θ affirmé « prends la calculatrice » ; acceptable après le rappel du radian (la part très fine). | Rien. |
| ol_l6_isoler | Quatre isolements (L, λ, a, D) d'un coup. | Non coupée (piste gardée) : seul « isole λ » est demandé ; noté comme à reprendre. |
| ol_l9_etablir | Quatre lignes de démonstration, chacune pointée : correct. | Rien. |
| **ol_c2_haut_bas** | **Deux expériences enchaînées** sur la même diapo (D doublée, puis a divisée par deux) **puis la question**. | **Coupée en deux** : `ol_c2_haut_bas` (D seule : l'écran recule de 1 à 2 m, L double ; deuxième explication : la lampe du téléphone qu'on éloigne du mur) et **`ol_c2b_en_bas`** (a seule : la fente deux fois plus fine, L double ; deuxième explication : « plus le passage est étroit, plus la lumière s'écarte ») qui porte la question du laser violet (énoncé, démonstration et réactions repris tels quels, leurs pistes restent valables). |
| ol_c3 → ol_c5 | Un cas par diapo. ol_c5 annonce l'indice n avant qu'il soit enseigné, mais le dit (« on le verra plus tard »). | Rien. |
| ol_g1_points | Cinq fentes enchaînées. | Non coupée : la courbe se construit point par point (pointage par fente). Noté. |
| ol_g2 → ol_g5 | Correct. | Rien. |
| ol_r2_vide | Soleil + cloche à vide + « pas mécanique » + c en une diapo ; **c = 3·10⁸ m/s dite une seule fois**, nombre impossible à se représenter. | Gardée telle quelle (piste valable) ; **nouvelle diapo après : `ol_r2b_celerite`** — deuxième explication de c : un éclair qui fait 7,5 fois le tour de la Terre en une seconde (`rappels.html?vue=terre`, Terre peinte, chrono ralenti), puis le Soleil à 8 minutes. Porte la question du bloc (la lumière n'a pas besoin de milieu matériel). |
| ol_r3 → ol_p5 | Une idée par diapo, sauf ol_p4 (diffraction / réfraction / dispersion), qui est une mise en ordre de mots déjà vus. | Rien. |
| ol_x*, ol_q*, bilan, carte | Cas du national et prisme : déroulés ligne par ligne. Le prisme utilise **le sinus** (sin i = n·sin r) sans rappel. | Non traité : partie « pour le devoir » ; un rappel du sinus (même échelle, opposé/hypoténuse) serait à ajouter (vue à créer dans `rappels.html`). |

### Séances et blocs (une seule « À toi » par bloc)

Six séances au lieu de cinq (18 blocs de 3–4 diapos) : S1 diffraction + radian ; S2 θ = λ/a, tangente, petit angle ; S3 calculer L, en haut / en bas ; S4 courbes, radiation, c ; S5 milieu et dispersion ; S6 national, prisme, bilan. Blocs nouveaux : `ol_s1_b3r` (radian, θ), `ol_s2_bt` (tangente, triangle), `ol_s3_b3r` (radiation, vide, c), avec cahier, `retrouver` et exercice (et leurs réactions). Les blocs recoupés reprennent le cahier et les figures de leurs diapos. Compétences : `ol_p1_radian` → C2, `ol_p2_tangente` → C3, `ol_c2b_en_bas` → C4, `ol_r2b_celerite` → C6.

### Simulations

- **Nouvelle** : `frontend/public/media/simulations/physics/ondes-lumineuses-tableau/rappels.html` — vues `radian` (pizza peinte, poignée sur l'arc, `set_parameters {theta_rad}`), `tangente` (échelle et mur peints, pied glissable, `{adjacent_m}`), `terre` (Terre peinte, éclair qui tourne, chrono). Moments, repères, `play_until`, `set_time`, `pause/resume/reset`, `ce_qui_se_voit`, protocole du kit.
- **Enrichie (additif, défaut inchangé)** : `diffraction.html` — paramètres `conclusions` (défaut `true`) et `trace_precedente` (défaut `false`), repère `tache_avant`.
- Contrôle : `node --check` OK ; ouvertes sans écran (Playwright + Chrome) : aucune erreur console, rien hors cadre.

### Voix à enregistrer (Bodi) — 6 pistes de diapo

`ol_p1_radian`, `ol_p2_tangente`, `ol_r2b_celerite` (nouvelles), `ol_t3_couleur`, `ol_c2_haut_bas`, `ol_c2b_en_bas` (réécrites ; audio retiré).

Énoncés de question à voixer (`enonce_dit`) : `ol_p1_radian` (« سؤال: un arc deux fois plus long que le rayon… »), `ol_p2_tangente` (« سؤال: التحت ديال l'échelle بعيد على الحيط ب deux mètres… »), `ol_r2b_celerite` (« سؤال: الضو ديال الشمس كيوصل للأرض… »). La question de `ol_c2b_en_bas` garde ses pistes (énoncé, démonstration, réactions).

Démonstrations à voixer : `ol_p1_radian` (« teta égale s sur R. s égale deux R… »), `ol_p2_tangente` (« tangente teta égale l'opposé sur l'adjacent… »).

Observation `ol_t3_couleur` : énoncé « Avec le laser bleu, la tache centrale est-elle plus large ou plus étroite que la rouge ? » (dit : « دابا le laser زرق. قارن la tache الزرقا مع الخط ديال النقط ديال الحمرا. واش كبيرة ولا صغيرة؟ ») ; 2 indices (pointillé → `tache_avant`, règle → `regle`) ; 3 retours (plus large / **plus étroite** / même largeur) ; solution.

Réactions préparées (sans audio) : `concentration.reponses.q` de `ol_p1_radian`, `ol_p2_tangente`, `ol_r2b_celerite` (juste + 1 + 2 pour chaque option fausse = 5 textes chacune) ; exercices des blocs `ol_s1_b3r`, `ol_s2_bt`, `ol_s3_b3r` (5 textes chacun, joués seulement en fin de cours).

Total : 6 pistes de diapo + 3 énoncés + 2 démonstrations + 7 textes d'observation (énoncé, 2 indices, 3 retours, solution) + 15 réactions de question (+ 15 réactions d'exercices de bloc, non jouées aujourd'hui).

### Non vérifié

Le cours n'a pas été joué dans le lecteur (gel des moments sur les mots, question d'observation dans `CourseFocusStage`) ; l'envoi de `sim_avant` avant la question n'est pas testé avec `trace_precedente` (la trace est posée par le premier pointage, pas par `sim_avant`). Pas de voix générée, pas de contrôle du cadre (`controler_cadre.py`). Mots rares gardés dans les voix : « pizza » (0 dans le corpus), « l'échelle » (23), « tours » ; à écouter.


## Chapitre 4 — Radioactivité (`phys_ch4_radioactivite`)

Copie en attente : `backend/data/courses/en_attente/phys_ch4_radioactivite.json` (52 → 59 diapos, 5 → 6 séances, 14 → 17 blocs). Script : `scratchpad/phys15/build_phys_ch4_radioactivite.py` (part de la copie en ligne, ne la modifie pas).

### Diapo par diapo

| Diapo | Ce qui va trop vite / résultat donné / prérequis / notion dite une fois | Ce qui a été fait |
|---|---|---|
| ra_n1_ouverture | Rien de trop : une question d'ouverture. | Inchangée. |
| ra_n2_atome | **Prérequis supposé** : l'atome était réduit à « un noyau au centre » ; les électrons (pourtant peints dans `noyau.html`) et la notion de charge n'étaient pas dits ; « très petit » dit une seule fois. | Voix réécrite : noyau + électrons (charge −), l'image du stade et du pois chiche, puis une 2ᵉ façon (« dehors léger, dedans lourd »). Repère `atome` pointé sur les électrons. |
| ra_n3_compter, ra_n4_notation, ra_n5_composition, ra_n6_isotopes | Une idée par diapo, avec exemple ; acceptable. | Inchangées. |
| ra_s1_diagramme, ra_s2_vallee | Une idée par diapo. | Inchangées. |
| ra_s3_zones | Trois zones dans une voix de 20 s, mais déjà une immobilisation par zone (`zone_beta_moins`, `zone_beta_plus`, `zone_alpha`). | Inchangée (le rythme est porté par les arrêts). |
| ra_s4_fleches | **Trop d'un coup** : les trois flèches β⁻, β⁺, α apparaissaient et étaient dites ensemble. | Coupée en deux : `ra_s4_fleches` (β⁻ puis β⁺, un repère pointé par flèche, β⁺ travaillé en exemple, β⁻ laissé à trouver par la question « À toi » existante) et **nouvelle** `ra_s4b_alpha` (la flèche α seule, dite deux fois : Z − 2, N − 2, puis « un noyau trop lourd jette un bloc de quatre nucléons »). La figure du cahier (trois flèches) passe sur α. |
| ra_s5_isotopes_ligne | Une idée. | Inchangée (passe au bloc suivant). |
| ra_r1_definition | Une idée + question. | Inchangée. |
| ra_r2_caracteres | **Trop d'un coup** : aléatoire, spontanée, inéluctable, et « chauffer n'y change rien » dits en une phrase chacun, sans rien montrer pour les deux derniers. | Coupée : `ra_r2_caracteres` = aléatoire seul (animation des douze noyaux, une immobilisation de plus, deuxième façon : le tirage au sort, puis « je relis ») ; **nouvelle** `ra_r2b_spontanee` = spontanée et inéluctable, montrées par la **nouvelle simulation `chauffer.html`** (flacon peint sur un bec de gaz, thermomètre, compteur Geiger : ≈ 40/s à 20 °C, ≈ 40/s à 800 °C) ; deuxième façon : le sablier. |
| ra_r3_soddy, ra_d1_alpha … ra_d6_type | Une désintégration par diapo, équation vérifiée : rythme correct. | Inchangées. |
| ra_f1_famille, ra_f2_systeme, ra_f3_famille2024 | Méthode en étapes, déjà immobilisée flèche par flèche. | Inchangées. |
| ra_l1_echantillon | Une idée. | Inchangée. |
| ra_l2_proportion | **Résultat décisif donné** : « tu trouves toujours le même nombre » était dit, l'élève ne le cherchait pas. | **Question d'observation** ajoutée (après « ولكن قسم اللي مشاو على اللي كاينين: ») : le tableau se remplit jusqu'au jour 3, la phrase verte « la même proportion » est tue (`conclusions: false`, paramètre **ajouté** à `population.html`, défaut inchangé), l'élève compare la colonne « proportion ». Voix inchangée : sa phrase suivante confirme. |
| ra_l3_equation | Une idée. | Inchangée. |
| ra_l4_rappel | **Quatre idées d'un coup** (e⁰ = 1, e^(−x) décroît, ln enlève e, ln(1/2) = −ln2) ; **prérequis** de maths seulement énoncés, sans image. | Coupé en deux rappels enseignés dès zéro, sur la **nouvelle simulation `rappels.html`** : **nouvelle** `ra_l4a_exp` (`?vue=exp` : la courbe, e⁰ = 1, « jamais zéro », un point à glisser ; deuxième façon : un verre d'eau peint qui perd la moitié de ce qui reste chaque minute) ; `ra_l4_rappel` réécrite (`?vue=ln` : deux machines peintes e puis ln, un jeton qui les traverse ; deuxième façon : la calculatrice, ln(0,5) = −0,693). La question « ln(e^(−3)) » et ses réactions sont gardées. |
| ra_l5_loi … ra_l8_restants | Une idée par diapo. | Inchangées (`ra_l6_lambda` : le repère `lambda_carbone` existe — il est construit `'lambda_' + e.id` dans `lambda.html` ; le vérificateur ne voit pas les noms construits). |
| ra_t1_definition … ra_t4_pourcentages | Une idée par diapo, démonstration ligne par ligne. | Inchangées. |
| ra_a1_compteur, ra_a2_definition | Une idée. | Inchangées. |
| ra_a3_demo | **Trop d'un coup** : définition, dérivée, a = λN, a₀ = λN₀, a(t) et « moitié/moitié » dans une voix. | Coupée : `ra_a3_demo` = a = −dN/dt (pourquoi le signe moins) → dérivée → a = λN, dit ensuite autrement (« plus de noyaux, plus de désintégrations par seconde ») ; **nouvelle** `ra_a3b_loi_activite` = a₀ = λN₀ puis a(t) = a₀·e^(−λt), dit autrement (« la moitié des noyaux, la moitié des tic-tac du compteur »). |
| ra_a4_unites | **Prérequis supposé** : la notation scientifique (1,19·10⁷ s, 5,8·10⁻⁸ s⁻¹) utilisée comme connue. | **Nouvelle** diapo avant elle : `ra_p3_puissances` (`rappels.html?vue=puissances` : 1 suivi de n zéros, puis la virgule qui saute 7 fois, puissances négatives, 2·10⁻⁶ g). |
| ra_a5_masse | **Prérequis supposé** : la mole, n = m/M et le nombre d'Avogadro, jamais enseignés dans le cours. | **Nouvelle** diapo avant elle : `ra_p4_mole` (`rappels.html?vue=mole` : une boîte de 12 œufs peinte = une douzaine ; 12 g de charbon peint = une mole = 6,02·10²³ atomes ; n = m/M, N = n·N_A ; deuxième façon : compter les œufs par douzaines). |
| ra_a6_courbe_a, ra_a7_droite_ln | Méthodes de lecture, une par diapo. | Inchangées. |
| ra_c1_principe | **Résultat décisif donné** : « l'activité diminue » dit avant que l'élève regarde la jauge du bois coupé. | **Question d'observation** ajoutée (après « كنقطعو الشجرة: هادشي كيوقف. ») : la scène va jusqu'à `desintegration`, la jauge peinte du bois baisse, « a diminue » et « le ¹⁴C se désintègre » sont tus (`conclusions: false`, paramètre **ajouté** à `datation.html`, défaut inchangé). Voix inchangée. |
| ra_c2_demo, ra_c3_calcul | Démonstration et calcul en lignes. | `ra_c3_calcul` : un mot de pointage cassé (« حسب العمر », absent de la voix) remplacé par « fois ln de quatre cent dix-huit sur trois cent dix-huit » (voix inchangée). |
| ra_c4_fils_pere | **Trop d'un coup** : père, fils, rapport, isolement de t et question dans une voix. | Coupée : `ra_c4_fils_pere` = père et fils (N fils = N₀ − N père), dit autrement (100 pères, il en reste 60 → 40 fils) ; **nouvelle** `ra_c4b_rapport` = r = e^(λt) − 1, t = (1/λ)·ln(1 + r), et la question « r = 1 : combien de demi-vies ? » (déplacée avec ses réactions et sa démonstration). |
| ra_x1 … ra_x4, ra_z1_bilan, ra_z2_carte | Cas types et bilan : rythme de méthode, une question par bloc. | Inchangées. |

### Séances et blocs (une seule « À toi » par bloc)

Séance 1 : `n1 n2 n3 n4` (Q n4) · `n5 n6 s1` (Q s1) · `s2 s3 s4 s4b` (Q s4).
Séance 2 : `s5 r1 r2 r2b` (Q r1) · `r3 d1 d2 d3` (Q d2) · `d4 d5 d6` (aucune).
Séance 3 : `f1 f2 f3` (Q f3) · `l1 l2 l3` (observation l2, pas de « À toi ») · `l4a l4 l5` (Q l4).
Séance 4 : `l6 l7 l8` (Q l8) · `t1 t2 t3 t4` (Q t3) · `a1 a2 a3 a3b` (Q a2).
Séance 5 : `p3 a4 p4 a5` (Q a5) · `a6 a7 c1` (observation c1) · `c2 c3 c4 c4b` (Q c4b).
Séance 6 : `x1 x2 x3` (Q x3) · `x4 z1 z2` (Q x4).
Cahier de chaque bloc reconstruit depuis les diapos ; `retrouver`/`exercice` repris des anciens blocs correspondants ; trois blocs nouveaux ont un `retrouver` et un `exercice` neufs avec leurs réactions écrites (chauffer l'échantillon ; que représente N(t) ; l'arbre coupé). Compétences : C2 + `ra_s4b_alpha`, C3 + `ra_r2b_spontanee`, C6 + `ra_l4a_exp`, C8 + `ra_a3b_loi_activite`, `ra_p3_puissances`, `ra_p4_mole`, C9 + `ra_c4b_rapport`.

### Simulations

- **Nouvelle** `radioactivite-tableau/rappels.html` (`?vue=exp|ln|puissances|mole`) : verre d'eau, machines, jeton, calculatrice, boîte d'œufs, charbon peints ; moments, `play_until`, `set_time`, `set_parameters {vue, x, x_ln, m_g}`, point glissable (vue exp), repères, `ce_qui_se_voit`.
- **Nouvelle** `radioactivite-tableau/chauffer.html` : flacon, bec de gaz et flamme, thermomètre glissable, compteur Geiger peints ; moments `froid`, `chauffe`, `chaud`, `compare` ; `set_parameters {temperature_c, conclusions}`.
- `population.html` et `datation.html` : paramètre **ajouté** `conclusions` (vrai par défaut, comportement d'aujourd'hui inchangé).

### Voix à enregistrer (voix Bodi)

Pistes de diapo (13) : `ra_n2_atome`, `ra_s4_fleches`, `ra_s4b_alpha`, `ra_r2_caracteres`, `ra_r2b_spontanee`, `ra_l4a_exp`, `ra_l4_rappel`, `ra_a3_demo`, `ra_a3b_loi_activite`, `ra_p3_puissances`, `ra_p4_mole`, `ra_c4_fils_pere`, `ra_c4b_rapport` (leur `audio.mixed` est retiré).

Questions d'observation (2 × : énoncé, 2 indices, 3 retours, 1 solution = 7 pistes chacune) :
- `ra_l2_proportion` — énoncé dit « شوف الخانة الأخيرة: اللي مشاو، قسمناهم على اللي كانو. نهار بنهار، شنو كتلاحظ؟ » ; cartes : « Elle diminue chaque jour, comme les désintégrés » / **« Elle reste presque la même chaque jour »** / « Elle double chaque jour ».
- `ra_c1_principe` — énoncé dit « قطعنا الشجرة. شوف la jauge ديال le carbone quatorze فالخشب. شنو كيوقع ليها؟ » ; cartes : « Elle reste pleine… » / « Elle remonte… » / **« Elle baisse : le carbone 14 n'est plus remplacé »**.

Questions déplacées : `ra_c4b_rapport.question` (pistes existantes `enonce`, réactions et démonstration réutilisables telles quelles, le texte n'a pas changé). `ra_s4_fleches` et `ra_l4_rappel` gardent leur question et leurs pistes.

Exercices de bloc neufs (non joués aujourd'hui, `FIN_DE_BLOC_COMPLETE = False`) : `ra_s2_b1`, `ra_s3_b3`, `ra_s5_b2` — énoncé + 5 réactions chacun, à voixer seulement quand la fin de bloc sera rejouée.

### Non vérifié

- Le passage par `verifier_texte_corpus.py` (mots rares du corpus) et la détection de murmures : à faire au moment de l'enregistrement. Mots à surveiller : « التيران », « الحمص », « الكرطونة », « الفاصلة », « كتنقز », « الطقطقات ».
- Le lecteur du cours (`CourseFocusStage`) n'a pas été rejoué sur la copie en attente (elle n'est pas servie).


## Chapitre 5 — Noyaux, masse et énergie (`phys_ch5_energie_nucleaire`)

Copie en attente : `backend/data/courses/en_attente/phys_ch5_energie_nucleaire.json` (38 → 46 diapos, 4 → 5 séances, 14 blocs de 3–4 diapos, une seule « ✏️ À toi » par bloc). Script de construction : `scratchpad/phys15/build_phys_ch5_energie_nucleaire.py` (repart toujours de la copie en ligne, qui n'est pas modifiée).

### Constat général

- Le chapitre suppose connus trois prérequis des années précédentes qui ne sont jamais enseignés : **l'énergie et le joule** (le mot « énergie » arrive dès `en_m1_soleil`), **les puissances de dix et la notation scientifique** (10⁻²⁷, 10¹⁶, 10⁻¹³ dans presque chaque diapo, et le calcul « on additionne les exposants » fait sans le dire dans `en_m2_einstein`), **deux charges de même signe se repoussent** (`en_r4_fusion` dit « deux charges positives » comme une évidence). La mole est rappelée en une phrase dans `en_n1_echantillon`.
- Plusieurs diapos enchaînent trois ou quatre idées : `en_m2_einstein` (relation + unités + exemple d'un gramme + ΔE), `en_m3_unites` (u, eV, MeV, MeV/c² en une diapo), `en_a2_zones` (fusion ET fission ET zone stable), `en_b2_methode` (quatre lignes de méthode + le piège liaison/libérée + la question), `en_n1_echantillon` (la mole, N = m·N_A/M, E = N·E_lib, la conversion en joule, le pétrole).
- Résultats décisifs donnés au lieu d'être trouvés : la balance de `en_d2_balance` (« le noyau est plus léger que ses nucléons séparés », fondement de tout le chapitre) est dite par la voix pendant que la simulation l'écrit ; dans `en_r4_fusion`, la voix demande « que vont-ils faire ? » puis répond aussitôt, et la simulation écrit « ils se repoussent ».

### Diapo par diapo

| Diapo | Constat | Fait |
|---|---|---|
| `en_m1_soleil` | Accroche, une idée. Repère cassé : le mot « قبل ما نكملو: » n'existe pas dans la voix, le geste `question` ne partait jamais. | Repère reposé sur « هاد la masse ماشي غاز » (voix inchangée). |
| — | Prérequis « énergie, joule » supposé connu. | **Nouvelle** `en_p1_energie` : une pile allume une lampe (l'énergie change de forme), puis une pomme de 100 g levée d'un mètre ≈ 1 J ; dit deux fois (définition + « ce qu'il faut pour éclairer, chauffer, soulever »). Animation `rappels.html?vue=energie`, la pomme se glisse jusqu'à 3 m. |
| — | Prérequis « puissances de dix, notation scientifique » supposé connu. | **Nouvelle** `en_p2_puissances` : l'exposant compte les zéros, la virgule qui saute (4 000 000 = 4·10⁶), 10⁻³ = on divise, notation scientifique, 10⁸ × 10⁸ = 10¹⁶ ; deuxième façon : « × 10 → l'exposant monte de un ». Animation `rappels.html?vue=puissances` (curseur de l'exposant n). Question « À toi » du bloc : 5 000 000 J en notation scientifique (réactions écrites). |
| `en_m2_einstein` | Quatre idées d'un coup ; « on additionne les exposants » fait sans être dit. | Réécrite : la relation seule, ses termes, et une deuxième lecture (c² énorme → petite masse, grande énergie). |
| — | (suite de `en_m2_einstein`) | **Nouvelle** `en_m2b_un_gramme` : l'exemple d'un gramme (exposants additionnés à voix haute, ≈ 2 000 t de pétrole), puis ΔE = Δm·c². Question « À toi » du bloc : ΔE = Δm·c² parmi trois écritures (réactions écrites). |
| `en_m3_unites` | u, eV, MeV, MeV/c² en une diapo. | Réécrite : l'unité u seule, avec deux images (le grain de sable pesé en tonnes ; 1 u ≈ un nucléon, donc ⁴He ≈ 4 u). |
| — | (suite de `en_m3_unites`) | **Nouvelle** `en_m3b_electronvolt` : eV, puis méga = 10⁶, puis MeV/c² ; l'exposant −19 + 6 = −13 dit. |
| `en_m4_931` | Démonstration en une diapo, déjà découpée par la figure ; question + exercice. | Inchangée (garde sa question, bloc `en_s1_b1b`). |
| `en_d1_composition` | Rappel du chapitre 4, bien fait. | Inchangée ; passe dans le bloc `en_s1_b1b`. |
| `en_d2_balance` | Résultat décisif donné par la voix et écrit par la balance. | **Question d'observation** : la voix s'arrête après la masse du noyau, la balance penche sans rien écrire (`conclusions: false`), « qui est le plus lourd, le noyau ou ses nucléons séparés ? », 2 indices, 3 cartes ; la voix reprend « الميزان كيهبط… » et confirme. Voix inchangée. |
| `en_d3_formule`, `en_d4_carbone` | Une idée chacune ; d4 porte la question du bloc. | Inchangées. |
| `en_l1_separer` … `en_l3_calcul` | Une idée par diapo, sens « séparer » puis « former » : déjà dit deux fois. | Inchangées. |
| `en_l4_par_nucleon`, `en_s1_stabilite`, `en_s2_piege` | Une idée chacune, le piège E_ℓ / E_ℓ/A traité seul. | Inchangées. |
| `en_a1_courbe` | Axes, points, courbe, creux : écrit pas à pas par la simulation. | Inchangée. |
| `en_a2_zones` | Fusion, fission, zone stable et bilan d'un coup. | Réécrite : les noyaux légers et la fusion seuls, avec une deuxième image (deux billes en haut d'une pente). |
| — | (suite de `en_a2_zones`) | **Nouvelle** `en_a2b_fission` : les lourds et la fission, puis le creux (fer), puis « deux chemins vers le creux » ; reprend la figure du cahier. |
| `en_a3_comparer` | Question du bloc. | Inchangée. |
| `en_r1_spontanee` … `en_r3_chaine` | Une idée par diapo ; r3 porte la question. | Inchangées ; la ligne « fusion » du cahier du bloc part dans le bloc suivant (règle 27). |
| — | Prérequis « deux charges positives se repoussent » supposé connu. | **Nouvelle** `en_p3_charges` : boules suspendues, même signe → elles s'écartent ; signes contraires → elles s'attirent ; puis deux protons ; deuxième façon : « une charge fuit celle qui lui ressemble ». Animation `rappels.html?vue=charges`. |
| `en_r4_fusion` | La voix pose « que vont-ils faire ? » et répond aussitôt. | **Question d'observation** : arrêt après « le deutérium و le tritium كيقربو. », les noyaux rebondissent sans que « ils se repoussent » s'écrive (`conclusions: false`), 2 indices, 3 cartes ; la voix reprend « كيرجعو اللور » et confirme. Voix inchangée. |
| `en_r5_soddy` | Pas de question, bloc sans « À toi ». | L'exercice de réserve (²H + ³H → ᴬ_ZHe + n, réactions déjà écrites) devient la question du bloc `en_s2_b4`. |
| `en_b1_masse_diminue` | Une idée, la balance. | Inchangée. |
| `en_b2_methode` | Quatre lignes de méthode + piège + question en une diapo. | Réécrite : lignes 1 et 2 seulement (l'équation, Δm « ce qu'on obtient moins ce qu'on avait »). |
| — | (suite de `en_b2_methode`) | **Nouvelle** `en_b2b_energie` : lignes 3 et 4 (ΔE < 0, E_lib = |ΔE|) et le piège liaison/libérée ; reçoit la question d'origine (même énoncé, même piste d'énoncé, mêmes réactions voixées). |
| `en_b3` … `en_b5`, `en_e1` … `en_e4` | Calculs de type national, un cas par diapo, déjà découpés en lignes par les figures. | Inchangées. |
| `en_n1_echantillon` | La mole, N = m·N_A/M, E = N·E_lib, la conversion et le pétrole d'un coup ; la mole supposée connue. | Réécrite : compter les noyaux seulement, la mole enseignée (« comme les œufs achetés par douze »), N = m·N_A/M. |
| — | (suite de `en_n1_echantillon`) | **Nouvelle** `en_n1b_energie_totale` : E = N·E_lib (une part par enfant), la conversion en joule, le pétrole. |
| `en_n2_comparaison`, `en_n3_2025`, `en_c1_cas_types`, `en_c2_qcm2019`, `en_z1_bilan`, `en_z2_carte` | Bilans et cas types : une liste par nature, déjà écrite ligne par ligne. | Inchangées. |

Notions dites une seule fois et maintenant dites deux fois : l'énergie, les puissances de dix, E = m·c², l'unité u, la fusion (zone d'Aston), la fission (zone d'Aston), la mole, la répulsion de deux charges.

### Séances et blocs

- S1 « Les outils, puis E = m·c² » : `en_s1_b0` (m1, p1, **p2**), `en_s1_b1` (m2, **m2b**, m3), `en_s1_b1b` (m3b, **m4**, d1).
- S2 « Défaut de masse, énergie de liaison, stabilité » : `en_s1_b2` (d2, d3, **d4**), `en_s1_b3` (l1, l2, **l3**), `en_s2_b1` (l4, s1, **s2**).
- S3 « La courbe d'Aston, la fission, la fusion » : `en_s2_b2` (a1, a2, a2b, **a3**), `en_s2_b3` (r1, r2, **r3**), `en_s2_b4` (p3, r4, **r5**).
- S4 « L'énergie libérée » : `en_s3_b1` (b1, b2, **b2b**), `en_s3_b2` (b3, b4, **b5**), `en_s3_b3` (e1, e2, e3, **e4**).
- S5 « L'échantillon, les cas types et le bilan » : `en_s4_b1` (n1, n1b, n2, **n3**), `en_s4_b2` (c1, **c2**, z1, z2).
(en gras : la diapo qui porte la question « À toi » du bloc.) Les ids de blocs anciens sont gardés quand le contenu correspond ; `cahier`, `retrouver` et `exercice` sont réécrits pour les blocs nouveaux ou déplacés. Compétences : p1, p2, m2b, m3b → C1 ; a2b → C4 ; p3 → C5 ; b2b → C6 ; n1b → C8.

### Simulations

- **Nouvelle** `frontend/public/media/simulations/physics/energie-nucleaire-tableau/rappels.html` (`?vue=energie | puissances | charges`) : pile, lampe, pomme et main, boules sur une potence en bois, protons peints ; craie pour les mots et les nombres ; `moments` par vue, `play_until`, `set_time`, `set_parameters {vue, hauteur_m, n}`, `pause/resume/reset`, `repere`, `ce_qui_se_voit`, poignées de l'élève (la pomme, l'exposant).
- `balance.html` et `reactions.html` : nouveau paramètre `conclusions` (URL ou `set_parameters`, vrai par défaut : rien ne change pour le cours en ligne). À `false`, la balance penche mais « m(noyau) < masse des nucléons séparés » n'est pas écrit ; les noyaux de la fusion rebondissent sans « ils se repoussent » ; la bulle d'arrêt dit « observe bien » au lieu de donner la réponse ; `ce_qui_se_voit` ne la dit pas non plus.

### Voix à enregistrer (Bodi)

**13 pistes de diapo** (voix nouvelle ou changée, `audio.mixed` retiré) : `en_p1_energie`, `en_p2_puissances`, `en_m2_einstein`, `en_m2b_un_gramme`, `en_m3_unites`, `en_m3b_electronvolt`, `en_a2_zones`, `en_a2b_fission`, `en_p3_charges`, `en_b2_methode`, `en_b2b_energie`, `en_n1_echantillon`, `en_n1b_energie_totale`.

**2 questions d'observation** (énoncé, 2 indices, 3 retours, la solution : 7 pistes chacune, 14 en tout) :
- `en_d2_balance` — énoncé dit « شوف الميزان مزيان. شكون اللي تقيل كثر: النواة، ولا les nucléons بعاد على بعضياتهم؟ » ; indices « شوف شمن plateau اللي هبط. », « قارن حتى بين جوج les masses المكتوبين ف la colonne. » ; cartes : le noyau plus lourd / **les nucléons séparés plus lourds** / même masse.
- `en_r4_fusion` — énoncé dit « شوف مزيان جوج les noyaux. شنو دارو ملي تقربو؟ » ; indices « شوف واش وصلو يتلاقاو. », « تفكر: جوج charges positives، شنو كيديرو؟ » ; cartes : ils fusionnent / **ils se repoussent sans se toucher** / ils s'attirent.

**Questions nouvelles** (énoncé dit + réactions juste / faux 1 / faux 2, sans piste) :
- `en_p2_puissances` : « Écris 5 000 000 J en notation scientifique » — 1 énoncé + 5 réactions.
- `en_m2b_un_gramme` : « La masse d'un système diminue de Δm. L'énergie libérée vaut : » — 1 énoncé + 5 réactions.
- `en_r5_soddy` : question sortie de la réserve, 5 réactions déjà écrites mais jamais voixées + 1 énoncé.
- `en_b2b_energie` : question déplacée depuis `en_b2_methode`, énoncé et réactions déjà voixés (rien à refaire).

Total : 13 pistes de diapo + 14 pistes d'observation + 3 énoncés + 15 réactions = **45 pistes**. Les exercices des blocs nouveaux (`en_s1_b0`, `en_s1_b1`, `en_s2_b3`, `en_s3_b1`) n'ont pas de réactions : ils ne sont ni joués ni voixés aujourd'hui (étape de fin de cours).

### Vérification

- `verifier.py` : JSON valide, LF, chaque `mot` du pointage et du centre dans sa voix, `apres_mot` trouvé une fois, moments / repères / paramètres présents dans les simulations, blocs couvrant les diapos dans l'ordre, une question par bloc, `node --check` des scripts des simulations citées : **OK**. Aucun chiffre ni tachkil dans les voix, énoncés dits et réactions nouveaux.
- `verifier_figures_cahier.py` : 3 figures, 0 erreur.
- `verifier_texte_corpus.py` : les mots darija rares des nouvelles voix ont été remplacés par des mots du corpus quand c'était possible (lampe → la lampe, باكية → مجموعة, ضدها → ماشي بحالها…) ; il reste des termes du programme rares (repoussent, s'attirent, méga, notation scientifique) et « تفاحة » (5 occurrences).
- `rappels.html` (3 vues), `balance.html?conclusions=0`, `reactions.html?vue=fusion&conclusions=0` ouverts dans Chromium sans écran (Playwright, serveur Vite) : rendu correct, aucune erreur JavaScript (un 404 de ressource annexe, sans effet).
- **Non vérifié** : le parcours dans le lecteur du cours (arrêt de la voix sur `apres_mot`, envoi de `conclusions` par le lecteur, bande « 👀 Observe »), la voix Bodi des nouvelles pistes, le contrôle du cadre (`controler_cadre.py`).


