# Audit national — SVT ch1 à ch4

Demandes de l'utilisateur du 18/11/2026 : (1) compter en allumant chaque élément tour à tour ; (2) un exercice du
national commence par la page du sujet telle qu'à l'examen (scan `/static/exams/svt/<année>-<session>/pages/sujet_pN.jpg`,
visuel `kind: "examen"`), lue par le tuteur ; (3) la démonstration se joue sur le document de l'examen ou la simulation
(lignes `allume`, contrat de la skill `simulations-au-tableau`, règle 17).

Règles : skill `simulations-au-tableau` 16-17, `professeur` 44-46, `logique-de-cours` 5.

Scans disponibles : seuls les sujets 2019 R à 2025 R ont un dossier `pages/` ; 2016 N à 2019 N et 2021 N, 2021 R
n'ont que les documents extraits (`assets/document_N.png`) : pas de page d'examen photographiée pour eux.

Pour chaque cours : (a) les exercices du national joués (sujet, année, session, page, documents, diapositives) ;
(b) les moments où l'on compte ou parcourt un à un ; (c) ce qui a été fait, les pistes à mettre en voix, ce qui reste.

<!-- ch1 : début -->
## Ch1 — Libération de l'énergie (`svt_ch1_reactions_responsables_liberation_energie`)

État au 19 novembre 2026. Simulations : `frontend/public/media/simulations/svt/reactions_responsables_liberation_energie-tableau/`.

### (a) Exercices du national joués — préparation de « l'énoncé d'abord » (feuille refaite en code)

**Fait** : une diapositive « l'énoncé d'abord » avant chaque exercice joué, sur la feuille d'examen refaite en code
(`reactions_responsables_liberation_energie-tableau/enonce.html?n=2024r|2022n|2020r|2016n|2017n`, gabarit commun
`shared/examen/feuille.js`) : ids `le_x0_enonce_2024r`, `le_x1c0_enonce_2022n`, `le_x1d0_enonce_2020r`, `le_x20_enonce_2016n`,
`le_c8a_enonce_2017n` ; le texte de l'examen dans l'ordre du scan, les figures de 2016 N (tableau, barres) et 2017 N (schéma
de la chaîne) redessinées en SVG ; chaque phrase lue est surlignée (repères `q-…`, `prop-…`, `phen-…`, `reac-…`, `fig-…`).
Les scans `pages/` et `assets/` ci-dessous ont servi de modèle (fractions mesurées par profil des lignes sombres).

| Sujet | Où dans `exam.json` | Modèle (scan) | Questions et points | Figures à redessiner | Déjà dessiné dans le cours ? | Diapositives (insérer l'énoncé avant) |
|---|---|---|---|---|---|---|
| **2024 R** (RS 34F) | `parts[0]`, question `I`, sous-questions `1`, `2` | `pages/sujet_p1.jpg`, haut 0,278 → bas 0,397 (en-tête de la page 1 jusqu'à 0,25) | I. Répondre sur votre feuille de rédaction aux questions suivantes : 1. Définir la fermentation lactique (0,5 pt) ; 2. Déterminer le sens de déplacement des protons H⁺ dans la mitochondrie au cours : a. du fonctionnement de la chaîne respiratoire (0,25 pt) ; b. du fonctionnement de la sphère pédonculée (0,25 pt) | aucune (texte seul) | — | avant `le_x1_restitution` (sert aussi à `le_x1b_protons` ; `le_c6_protons` réutilise I.2.a dans un QCM « national 2024 ») |
| **2022 N** (NS 34F) | `parts[0]`, question `II`, sous-question `II.1` | `pages/sujet_p1.jpg`, haut 0,368 → bas 0,592 (en-tête jusqu'à 0,237) | II. Pour chacune des données numérotées de 1 à 4, une seule proposition correcte ; recopier les couples (2 pts, 0,5 par donnée). Donnée 1 « Dans la mitochondrie » : a. la sphère pédonculée transporte H⁺ vers l'espace intermembranaire ; b. la sphère pédonculée est responsable de la phosphorylation de l'ADP ; c. la membrane externe contient des protéines qui transportent les électrons vers le dioxygène ; d. la membrane externe contient des enzymes d'oxydoréduction. Réponse (1, b) | le cadre pointillé du QCM (donnée 1, colonne de gauche) | `national.html?vue=restitution` écrit les quatre propositions telles qu'au sujet | avant `le_x1c_qcm` |
| **2020 R** (RS 34F) | `parts[0]`, question `III` (type `association`, `items_left` / `items_right`) | `pages/sujet_p2.jpg`, haut 0,088 → bas 0,302 (en-tête de la page 2 jusqu'à 0,09) | III. Reliez chaque phénomène à la réaction bilan qui lui convient ; recopiez les couples (1 pt) | **tableau à deux cadres** : « Phénomène » (1- La glycolyse ; 2- Le cycle de Krebs ; 3- La fermentation lactique ; 4- La fermentation alcoolique) et « Réaction bilan » (a à e, équations exactes de `items_right`, e sur deux lignes) | oui : `national.html?vue=reactions` écrit les 4 phénomènes et les 5 réactions du sujet (réutilisable pour la mise en page) | avant `le_x1d_reactions` (puis `le_x1e_reactions_c`, `le_x1f_reactions_krebs`) |
| **2016 N** | `parts[1].exercises[0]` (« Sujet 1 »), question `ex1q1`, documents `doc_g1`, `doc_g2` | pas de page scannée : `assets/document_1.png`, `assets/document_2.png` (**page d'examen photographiée manquante**) | Texte : « Afin d'étudier l'effet du manque d'exercices sportifs et du tabagisme (usage du tabac) sur les réactions responsables de la libération de l'énergie au niveau du muscle squelettique strié, on propose l'étude des données suivantes. » Question 1 : « En exploitant les données des documents 1 et 2, expliquez l'augmentation de la fatigabilité observée chez la personne non entraînée. » (1 pt). NB : une seule consigne au sujet ; le cours la joue en deux temps (comparer, `le_x2_qui_respire`, puis expliquer, `le_x2b_fatigue`), comme la correction (comparaison puis explication) | **Document 1, tableau** : colonnes « Personne entraînée » / « Personne non entraînée » ; lignes « Volume total des mitochondries par rapport au volume de la cellule musculaire » 11 % / 5 %, « Activité des enzymes mitochondriales » importante / faible. **Document 2, graphique à barres** : pour « Personne non entraînée » et « Personne entraînée », barres pointillées « Quantité d'acide lactique produit en mmol/L » 12 / 6 et barres pleines « Consommation du dioxygène en L/min » 2.5 / 5.5 (valeurs écrites au-dessus des barres) | en partie : `national.html?vue=sportifs` a les mêmes valeurs (jauges puis tableau), pas la mise en page en barres du document 2 | avant `le_x2_qui_respire` |
| **2017 N** | `parts[0]`, question `IV` (id `p1q4`, type `schema`), document `doc_g1` | pas de page scannée : `assets/document_1.png` (**page d'examen photographiée manquante**) | IV. Le document ci-dessous représente la chaîne respiratoire. Nommez chacune des structures désignées par les numéros 1, 2, 3 et des réactions désignées par les lettres A, B, C (1,5 pt) | **schéma de la chaîne respiratoire** : membrane interne en bicouche, transporteurs T1 à T6 (T3 et T5 mobiles, e⁻ en pointillés), quatre flèches H⁺ vers le haut (T1, T4, T6, sphère), sphère pédonculée à droite ; réaction A (NADH,H⁺ → NAD⁺ ; FADH₂ → FAD), B (O₂ + 4H⁺ → 2H₂O), C (ADP + Pi → ATP) ; repères 1 (accolade, membrane interne), 2 (sphère pédonculée), 3 (espace intermembranaire) | non : `chaine.html?etiquettes=examen` nomme CI…CV et `?vue=construire` a **4** structures (1 à 4), alors que le sujet 2017 N n'en a que **3** et nomme T1…T6 — à aligner sur le sujet | avant `le_c8_national` (puis `le_c8b_construire`, qui dit « comme au national 2017 ») |

**Documents reconstitués ou cités (pas d'énoncé à faire)** :
- `le_x3_chaine_en_panne`, `le_x3b_deduire`, `le_x3c_hypothese` (`exao.html?vue=mitochondries`) : « document type » inspiré de **2020 R,
  exercice 1, document 1** (`pages/sujet_p3.jpg`, haut ≈ 0,09 → 0,35 : figure a, O₂ en % de saturation ; figure b, ATP en UA ;
  ajouts glucose t₁, pyruvate t₂, ADP + Pi t₃, cyanure t₄ ; question 1 « En exploitant le document 1, déduisez les conditions de
  synthèse d'ATP au niveau des mitochondries » 1,25 pt). Les valeurs du cours diffèrent (ATP 10 → 90 UA au lieu de ≈ 30 → 100 ;
  O₂ 96 → 40 % au lieu de ≈ 93 → 35 %) et les trois consignes (décrire, déduire, hypothèse) ne sont pas celles du sujet. À décider :
  en faire le vrai 2020 R (valeurs et consigne du sujet, puis l'énoncé d'abord) ou le garder comme document type.
- `le_c1_pulse` (`exao.html?vue=pulse_o2`) : document de **2016 R** (mitochondries sans membrane externe, [H⁺], injection d'O₂) utilisé
  comme activité du cours, pas comme exercice.
- `le_e3b_masse_levures` (`national.html?vue=levures`) : aucune source trouvée dans `exam.json` 2016-2025 (reconstitué).
- `le_f2_alcoolique` : cite 2023 R seulement dans l'explication d'un vrai/faux de fin de cours.
- `le_m3a_glucose_marque` : « une expérience du bac », sujet non identifié dans `exam.json`.

### (b) Moments où l'on compte ou parcourt un à un

| Diapositive | Simulation | Ce qui est compté / parcouru | État |
|---|---|---|---|
| `le_r1_compteur` | `compteur.html` | les 4 ATP directs de la caisse, les 10 NADH,H⁺, les 2 FADH₂ (un compte par couleur), chaque total écrit dans la ligne « total » à la fin de son compte | **fait** (moments `atp_1…4`, `nadh_1…10`, `fadh_1…2`, `compte_atp|nadh|fadh` ; pointages au rythme de « نجمعو… ») |
| `le_g2_six_carbones` | `glycolyse.html` | les 6 carbones du glucose, avant la coupure 3 + 3 | **fait** (`carbone_1…6`, `compte_carbones`) |
| `le_k4_sorties` | `krebs.html` | les 5 sorties d'un tour, numérotées à leur cran ; « un tour : 5 sorties » écrit une fois | **fait** (repères `sortie_1…5` sur les moments existants) |
| `le_k5_fois_deux` | `krebs.html` | tour 1, tour 2 ; 2 + 4 = 6 CO₂ ; 2 + 2 + 6 = 10 NADH,H⁺ | à faire |
| `le_c4_relais` | `chaine.html` | les transporteurs T1 → T4 parcourus un à un par les électrons | à faire |
| `le_m2_legender` | `mitochondrie.html` | les six mots placés un à un | à faire |
| `le_m3a_glucose_marque` | `glucose-marque.html` | T0 … T4, compartiment par compartiment (moments existants, sans lueur ni numéro) | à faire |
| `le_x1c_qcm` | `national.html` | propositions a, c, d (rayées) puis b | **fait** par `allume` (démonstration) |
| `le_x1d/e/f` | `national.html` | réactions a → e : ce qu'elle donne, le phénomène, le lien | **fait** par `allume` |
| `le_x2_qui_respire`, `le_x2b_fatigue` | `national.html` | les lignes du tableau 2016 N (mitochondries, O₂, acide lactique) | **fait** par `allume` |
| `le_x3*` | `exao.html` | les périodes entre deux ajouts (glucose, acide pyruvique, ADP + Pi, cyanure) | **fait** par `allume` (nouvelles bandes `periode_*`) |

### (c) Fait, pistes, reste à faire

- **Fait** : `SVTTableau.Allumage` dans `commun.js` (commandes `allume {cible}` / `eteins`, lueur qui reste, la dernière plus vive,
  numéro courant ; `reset` éteint ; `allumes` dans l'état) ; `allume`/`eteins` exécutés par `national.html`, `exao.html`,
  `compteur.html`, `glycolyse.html`, `krebs.html`. `allume` posé sur les lignes de démonstration de `le_x1_restitution`,
  `le_x1b_protons`, `le_x1c_qcm`, `le_x1d_reactions`, `le_x1e_reactions_c`, `le_x1f_reactions_krebs`, `le_x2_qui_respire`,
  `le_x2b_fatigue`, `le_x3_chaine_en_panne`, `le_x3b_deduire`, `le_x3c_hypothese`, `le_g3_bilan`. Comptes en allumant : r1, g2, k4.
- **Pistes ajoutées au `_voix.json` : 5** (les cinq diapositives d'énoncé ; aucun texte dit existant n'a changé).
- **Reste à faire** : `allume` des démonstrations de `le_t2_reduit`
  (`taxi.html`), `le_r2_rendement` (`rendement.html`), `le_c10b_vesicules_cas` (`vesicules.html`) ; les comptes de k5, c4, m2, m3a ;
  aligner `le_c8b_construire` sur les 3 structures du sujet 2017 N ; décider du sort de `le_x3*` (vrai 2020 R ou document type).
<!-- ch1 : fin -->

<!-- ch2 : début -->
## Ch2 — Le muscle strié squelettique (`svt_ch2_role_muscle_strie_squelettique`)

### (a) Exercices du national joués

| Sujet | `exam.json` | Modèle (scan / extrait) | Questions jouées (points) | Diapositives |
|---|---|---|---|---|
| **2016 N** (normale) | `parts[1]` « Deuxième partie », `exercises[0]` « Sujet 1 » (5 pts) ; question `ex1q1` | pas de `pages/` : `assets/document_1.png` (doc. 1), `assets/document_2.png` (doc. 2) ; texte exact de l'énoncé dans `extraction.json` (« Le manque d'exercices sportifs… », « Remarque : le phénomène de la fatigue… ») | 1. « En exploitant les données des documents 1 et 2, expliquez l'augmentation de la fatigabilité observée chez la personne non entraînée. » (1 pt) | `ms_x1_decrire_comparer`, `ms_x2_deduire_expliquer`, `ms_x2b_expliquer`, `ms_x2c_rediger` (`national.html?vue=entraine`) |
| **2017 R** (rattrapage) | `parts[1]`, `exercises[0]` « Exercice 1 » (5 pts) ; questions `ex1q1a`, `ex1q1b` | pas de `pages/` : `assets/document_2.png` (doc. 1 du sujet), `assets/document_3.png` (doc. 2) ; énoncé exact dans `extraction.json` (« Certains sportifs trichent… », « La mesure de la concentration de certains métabolites… ») | 1-a. déterminez les variations de la concentration des métabolites chez les deux nageurs (1 pt) ; 1-b. dégagez les voies métaboliques utilisées par chaque nageur (1 pt) | `ms_x3_hypothese` (doc. 1, `?vue=nageurs` ; le texte de la diapositive dit « reconstitué d'après », mais le tableau est celui du sujet), `ms_n1_voies` (doc. 2, `?vue=voies`) |
| **2020 N** (normale) | `parts[1]`, `exercises[0]` « Exercice 1 » (7 pts) ; questions 2 et 3 (`questions[1]`, `questions[2]`, sans id) | `pages/sujet_p3.jpg` (contexte BPCO, bas de page, ~0,46-0,70) et `pages/sujet_p4.jpg` (texte « Afin de déterminer… » 0,16-0,23 ; document 2 0,24-0,47 ; Q2 0,51-0,58 ; Q3 0,59-0,62) ; `assets/doc2p4.png` | 2. Comparez la distribution des types de fibres… et déduisez, en justifiant, la voie métabolique dominante (1,75 pt) ; 3. expliquez la faible activité musculaire chez la personne atteinte de BPCO (1 pt) | `ms_n2_fibres` (`?vue=fibres`, démonstration), `ms_n3_chaine` (`?vue=chaine`) |

Figures à redessiner pour la feuille d'examen (gabarit `shared/examen/feuille.html`, pas encore sur main) :

- **2016 N, document 1** — tableau 2 colonnes (Personne entraînée / Personne non entraînée) × 2 lignes : « Volume total des mitochondries par rapport au volume de la cellule musculaire » 11 % / 5 % ; « Activité des enzymes mitochondriales » importante / faible. Modèle `2016-normale/assets/document_1.png`. Valeurs déjà dans `national.html?vue=entraine` (fibres peintes, 11 % / 5 %, enzymes) : réutilisables, mais dessin différent du tableau du sujet.
- **2016 N, document 2** — histogramme, deux groupes (Personne non entraînée, Personne entraînée), deux barres par groupe : acide lactique produit en mmol/L (barres pointillées) 12 / 6 ; consommation du dioxygène en L/min (barres noires) 2,5 / 5,5 ; légende en haut ; pas d'axe gradué (valeurs écrites au-dessus des barres). Modèle `assets/document_2.png`. Les barres de `?vue=entraine` ont ces valeurs (réutilisables).
- **2017 R, document 1** — tableau « Concentrations des métabolites en 10⁻⁶ mol/g du muscle » : colonnes Acide lactique, Glycogène, Phosphocréatine, ATP ; lignes 1- état de repos 1.1 / 80 / 17 / 4.6 ; 2- nage libre 100 m (1 min) 30.5 / 60 / 10 / 3.4 ; 3- nage libre 1500 m (15 min) 3 / 38 / 16 / 4.7. Modèle `2017-rattrapage/assets/document_2.png`. `?vue=nageurs` dessine ce tableau à la fin (moment `tableau`) : réutilisable.
- **2017 R, document 2** — histogramme empilé « Pourcentage de consommation des métabolites », axe 10 à 100 %, deux barres (nage libre 100 m, nage libre 1500 m) ; légende : blanc = métabolisme aérobie du glucose, hachuré = voie anaérobie de la phosphocréatine, gris = métabolisme anaérobie du glucose ; 100 m : 85 % PC, 10 % anaérobie du glucose, 5 % aérobie ; 1500 m : ~7 % anaérobie, ~93 % aérobie. Modèle `assets/document_3.png`. `?vue=voies` a les mêmes barres (réutilisable).
- **2020 N, document 2, figure a** — histogramme groupé « Pourcentage des fibres musculaires (%) », axe 10 à 60 ; deux groupes (Fibres de type II, Fibres de type I) ; barres blanches = personne saine, hachurées = personne atteinte ; type II : saine 30, atteinte 45 ; type I : saine 58, atteinte 30. Modèle `sujet_p4.jpg` (0,24-0,41) ou `assets/doc2p4.png`. `?vue=fibres` a ces barres (ordre type I puis type II, inverse du sujet).
- **2020 N, document 2, figure b** — tableau « Type de fibres / Caractéristiques », colonnes Fibres de type I / II : Taille Petit / Gros ; Résistance à la fatigue +++ / + ; Nombre de mitochondries +++ / + ; Activité des enzymes oxydatives +++ / + ; Activité des enzymes glycolytiques + / +++ ; Activité de l'enzyme LDH + / +++ ; notes : « Le nombre de signes (+) indique l'importance du caractère. L'enzyme LDH catalyse les réactions de la production de l'acide lactique ». `?vue=fibres` a ce tableau, ligne par ligne (réutilisable).
- (contexte 2020 N, page 3 : le document 1 — électronographies a et b, tableau c : tension de la secousse 60 / 143 N, surface de section 80 / 110 cm² — n'est pas joué dans le cours ; à redessiner seulement si la feuille montre l'exercice entier.)

Documents « reconstitués d'après l'examen » (pas d'exercice joué en entier, pas de feuille d'énoncé) : `ms_c2a_calcium_libere` (d'après 2016 N, calcium radioactif), `ms_r8_inhibiteurs` (d'après 2020 R, inhibiteurs de la glycolyse et de la créatine kinase). `ms_r7_tableau` cite « dégagez sous forme d'un tableau » (2022 R) comme consigne seulement.

### (b) Moments où l'on compte ou parcourt un à un

| Diapositive | Simulation | Ce qu'on parcourt | État |
|---|---|---|---|
| `ms_f6_nomme` | `sommation.html?vue=nomme` | les stimulations d'un tracé (« شحال من excitation ؟ هنا، جوج ») | **fait** : moments `stim_1` … `stim_n`, chaque créneau s'allume, son numéro s'écrit dessous (15 px et plus), il reste allumé, le dernier plus vif ; le total (« 2 stimulations ») s'écrit une fois au moment `stimulations_comptees` ; repères `stim_k` ; pointage « شحال من excitation؟ » → `stim_1` ajouté. Avant : tous les numéros d'un coup, en 12 px. |
| `ms_c7_ordre` | `cycle.html?vue=etapes` | les six étapes du cycle (« un : le calcium… six : ATP ») | **fait** : chaque étape écrite s'allume et reste allumée, la dernière plus vive ; repères `etape_1` … `etape_6` (le numéro était déjà écrit devant chaque étape). |
| `ms_n3_chaine` | `national.html?vue=chaine` | les six cases de la chaîne d'explication (« la case اللولة… اللخرة ») | **fait** : chaque case s'allume, son numéro 1 … 6 s'écrit au-dessus, la dernière plus vive. |
| `ms_n2_fibres` | `national.html?vue=fibres` | le tableau des fibres, « سطر بسطر » | **fait** : chaque ligne lue s'allume et reste allumée, la dernière plus vive (rien d'allumé pendant la démonstration, où seuls les `allume` comptent). |
| `ms_f4_tetanos_imparfait` | `sommation.html?vue=serie` | « Compte les excitations » (consigne à l'élève, la voix ne compte pas) | non fait : le compte en allumant existe dans `?vue=nomme` (tracé n° 5, 12 stimulations, vérifié) ; à brancher si la voix compte un jour. |
| `ms_c1b_essais` | `exigences.html` | quatre essais « un par un » | non fait (chaque essai est déjà un moment ; pas de lueur). |
| `ms_e2_atpase` | `atpase.html` | trois tubes, premier / deuxième / troisième | non fait. |
| `ms_r2_phosphocreatine`, `ms_r4_fermentation`, `ms_r5_respiration` | `voies.html` | les trois voies de régénération de l'ATP, une par diapositive | non fait (une voie par diapositive : pas de compte dans une même scène). |
| `ms_x2c_rediger` | `national.html?vue=entraine` | la chaîne m1 … m5 | non fait (cases écrites une par moment, sans lueur ni numéro). |
| `ms_b1_bilan`, `ms_b2_carte` | `bilan.html`, `carte.html` | neuf points / six branches numérotés | non fait. |
| `ms_u3_myofibrille`, `ms_u4_filaments`, `ms_u7_molecules` | `structure.html`, `sarcomere.html`, `calcium.html` | sarcomères, filaments, « deux têtes » | rien à compter à voix haute (aucun nombre dit) : pas de lueur ajoutée. |

### (c) Fait, pistes, reste

- **Démonstration sur le document** : `allume`/`eteins` implémentés dans `national.html` (toutes les vues) avec l'aide commune du dossier (`commun.js` : `lueur`, `Allumage`) : `allume {cible}` joue jusqu'au moment s'il n'est pas passé, puis met une lueur jaune qui reste sur le repère (la dernière plus vive) ; `eteins`, `reset`, `start` éteignent ; l'état porte `allumes`. Pendant la démonstration, la vue `fibres` n'écrit plus « atteinte : type I ↓, type II ↑ » (la colonne l'écrit). Lignes `allume` posées : `ms_n2_fibres` (4 lignes : barres des fibres, `ligne_mito`+`ligne_oxy`, `ligne_glyco`+`ligne_ldh`, `type2_malade`+`ligne_ldh`), `ms_r6b_intensite` (4 lignes : `pt44`/`pt58`, `pt68`…`palier`, `palier`, `pt68`/`pt101`), `ms_x4b_eliminer` (3 lignes : `affirmation`, `mot_decide`, `mot_decide` — la règle n'est plus au tableau quand l'affirmation est écrite). Vue `intensite` : dans le tableau final, les repères `pt44` … `pt101` (une ligne par mesure) et `palier` (colonne du O₂, 68 à 101 kJ/min) existent aussi, pour que la démonstration allume la ligne qu'elle lit.
- Pas encore : `allume` dans `inhibiteurs.html` (`ms_r8_inhibiteurs`), `atpase.html` (`ms_e2_atpase`), `consommation.html` (`ms_t4_consomme`) et `ms_t4a_sang` (sans simulation) — leurs lignes n'ont pas d'`allume` ; ce ne sont pas des exercices du national joués.
- **Énoncé d'abord** : fait avec le gabarit commun (`shared/examen/feuille.js`, arrivé sur main pendant cette passe) — trois
  feuilles refaites en code, une par exercice joué : `shared/examen/sujets/svt-2016-normale-ex2.html` (sujet 1, Q1 ; document 1
  en tableau, document 2 en SVG), `svt-2017-rattrapage-ex1-nageurs.html` (exercice 1, Q1-a et 1-b ; document 1 en tableau, document 2
  en SVG), `svt-2020-normale-ex3.html` (exercice 1, Q2 et Q3 ; figure a en SVG, figure b en tableau). Texte : `extraction.json`
  (2016 N, 2017 R : `exam.json` y résume l'introduction) et le scan `sujet_p3.jpg`/`sujet_p4.jpg` (2020 N) ; points :
  `exam.json`. Diapositives nouvelles, en tête de leur bloc : `ms_x1_enonce` (`ms_s6_b2`), `ms_x3_enonce` (`ms_s6_b3`),
  `ms_n2_enonce` (`ms_s7_b1`) ; le tuteur lit l'énoncé et la baguette surligne ce qu'il lit (`contexte`, `intro`, `tab-1`,
  `fig-…`, `q-…`). Les documents non joués (2016 N doc. 3-6, 2017 R doc. 3-5, 2020 N doc. 1, 3, 4) ne sont pas sur la feuille.
  Non vérifié dans le lecteur (le backend ne démarre pas dans ce conteneur : fastapi absent) ; les feuilles seules sont
  vérifiées à 1366 × 560 et 724 × 350 (texte ≥ 15 px, repères présents).
- **Voix** : 3 pistes ajoutées au `_voix.json` (`ms_x1_enonce`, `ms_x3_enonce`, `ms_n2_enonce`, type diapositive) ; aucun texte dit existant n'a changé (un `pointage` ajouté sur `ms_f6_nomme`, sans effet sur l'audio).
<!-- ch2 : fin -->

<!-- ch3 : début -->
## Ch3 — L'information génétique (`svt_ch3_notion_information_genetique`)

Audit du 19 novembre 2026. Simulations : `frontend/public/media/simulations/svt/notion_information_genetique-tableau/`.

### (a) Les exercices du national joués dans le cours

L'énoncé d'abord (professeur, règle 46) : **fait** avec le gabarit commun `shared/examen/` (feuille refaite en code, pas
de scan), une diapositive avant chaque exercice, lue par le tuteur (texte de l'examen en français, liaisons en darija),
pointage `surligner` sur chaque question et chaque donnée :

| Diapositive nouvelle | Avant | Feuille |
|---|---|---|
| `ig_x1a_enonce` | `ig_x1_restitution` | `feuille.html?sujet=svt/2024-rattrapage&exercice=1&questions=2&page=1/6&titre=encadre&bareme=inline` (question II entière, ses 4 propositions) |
| `ig_x1c0_enonce` | `ig_x1c_metaphase` | `feuille.html?sujet=svt/2018-rattrapage&exercice=1&questions=4&page=1/6&titre=encadre&bareme=gauche` (question IV entière) |
| `ig_x1e0_enonce` | `ig_x1e_associer` | `sujets/svt-2024-normale-ex1.html` (page à soi : la feuille générique n'affiche pas les tableaux `items_left` / `items_right` d'une question `association` ; tableaux Ensemble A / B recopiés du scan ; repères `ligne-1…4`, `ligne-a…e`) |
| `ig_x3_enonce` | `ig_x3_thymidine_doc` | `sujets/svt-2017-rattrapage-ex2.html` (page à soi : le document 1 redessiné en SVG, la question 1 et son barème ; repères `donnee-cycle1`, `donnee-cycle2`, `donnee-legende`, `donnee-observation`, `donnee-resultat1`, `donnee-resultat2`, `q-1`) |

Manques signalés au kit commun : la feuille générique ne rend pas une question `association` (2024 N IV : seule la consigne
s'affiche) ; le surlignage CSS (`.surligne`, fond) ne se voit pas sur un groupe SVG (la page 2017 R ajoute sa règle) ;
le texte d'introduction de l'exercice 2 de 2017 R manque à `exam.json` (son `context` est un résumé) et la page de cet
exercice dans le sujet (n/N) est inconnue : la feuille commence au document et la case « الصفحة » reste vide.

Le détail de chaque exercice (modèle, figures) :

| Sujet | Où dans `exam.json` | Questions et points | Modèle (scan / document) | Figures à redessiner | Diapositives du cours |
|---|---|---|---|---|---|
| 2024 rattrapage (RS 34F) | `parts[0]` « Première partie : Restitution des connaissances » (5 pts), question `II` (type `qcm`, 2 pts) ; jouée : sous-question `2` | II : « Pour chacune des propositions numérotées de 1 à 4… adresser à chaque numéro la lettre qui correspond à la suggestion correcte. (2 pts) » ; 4 × 0,5 pt ; jouée : 2. « Au cours de la phase G₁ de l'interphase, chaque chromosome est : » a. monochromatidien condensé ; b. monochromatidien non condensé ; c. bichromatidien non condensé ; d. bichromatidien condensé (réponse b) | `backend/data/exams/svt/2024-rattrapage/pages/sujet_p1.jpg`, grand en-tête de la page 1 (0 → 0,25 de la hauteur), question II de 0,392 à 0,565 (énoncé 0,398-0,445 ; case 2 à droite : titre 0,461-0,488, a 0,494, b 0,511, c 0,527, d 0,544) | une seule : le **tableau du QCM** (2 colonnes × 2 lignes de cases encadrées, propositions 1-2 en haut, 3-4 en bas, titre en gras, lettres a-d en gras) ; pas de figure scientifique | `ig_x1_restitution` (posé), `ig_x1b_corrige` (corrigé). La carte de `documents.html?vue=restitution` reformule les choix (« à une chromatide et condensé ») : la feuille d'examen devra garder « monochromatidien / bichromatidien », la carte peut rester (la voix pourra dire « monochromatidien يعني chromatide وحدة »). |
| 2018 rattrapage | `parts[0]` « Première partie : restitution des connaissances », question `p1q4` (IV, `qcm`, 2 pts) ; jouée : `p1q4_2` (0,5 pt) | IV : « Pour chacune des propositions numérotées de 1 à 4, une seule suggestion est correcte. Recopiez les couples (1;…) (2;…) (3;…) (4;…)… » ; jouée : 2. « Durant la métaphase de la mitose, chaque chromosome est formé : » a. d'une seule chromatide constituée de deux brins d'ADN ; b. de deux chromatides constituée chacune d'un brin d'ADN ; c. de deux chromatides constituée chacune de deux brins d'ADN ; d. de deux chromatides, l'une constituée d'un seul brin d'ADN et l'autre de deux brins d'ADN (réponse c) | **pas de page scannée** (2018 R n'a que `exam.json` et `assets/document_N.png` ; aucun document pour cette question) : page d'examen photographiée manquante, la mise en page suivra le gabarit commun | aucune (texte seul) | `ig_x1c_metaphase` (posé ; les options de la question sont celles de l'examen), `ig_x1d_corrige_metaphase` (corrigé). La carte de `documents.html?vue=metaphase` abrège les choix. |
| 2024 normale (NS 34F) | `parts[0]` « Première partie : Restitution des connaissances » (5 pts), question `IV` (type `association`, 1 pt) | IV : « Recopier les couples (1,...), (2,...), (3,...) et (4,...) et adresser à chaque numéro de l'ensemble A la lettre correspondante dans l'ensemble B. (1pt) » ; A : 1. ADN polymérase. 2. Centromère. 3. Nucléosome. 4. Ribosome. ; B : a. Complexe formé par l'association Histones –ADN. b. Complexe moléculaire participant à la synthèse des protéines. c. Complexe protéique assurant la synthèse de l'ARNm. d. Structure reliant les deux chromatides du même chromosome. e. Enzyme qui intervient dans la réplication de l'ADN. Réponse (1, e) ; (2, d) ; (3, a) ; (4, b) | `backend/data/exams/svt/2024-normale/pages/sujet_p1.jpg`, grand en-tête (0 → 0,25), question IV de 0,783 à 0,945 (énoncé 0,788-0,818 ; en-têtes « Ensemble A / Ensemble B » 0,834 ; lignes 1/a 0,851, 2/b 0,868, 3/c 0,885, 4/d-e 0,902-0,932) | une seule : le **tableau d'association** (à gauche « Ensemble A », 4 lignes, la 4 sur deux hauteurs ; à droite « Ensemble B », 5 lignes ; en-têtes grisés) | `ig_x1e_associer`, `ig_x1f_associer_couples`. Le cours joue 3 couples sur 4 (le ribosome, (4, b), au chapitre 4) : la feuille montrera les 4. |
| 2017 rattrapage | `parts[1]` (deuxième partie), « Exercice 2 » (3 pts) ; jouée : question `ex2q1` (1,5 pt), document `doc_g7` (« Document 1 ») | 1. « Expliquez les résultats de l'expérience du document 1, en justifiant votre réponse à l'aide d'un schéma adéquat du phénomène biologique mis en évidence. » (1,5 pt). Le `context` d'`exam.json` est un résumé, pas l'énoncé : le texte d'introduction exact de l'exercice manque (à reprendre du sujet papier si on le retrouve). `ex2q2` (1,5 pt, XPB, documents 2-4) relève du chapitre 4. | **pas de page scannée** ; modèle : `backend/data/exams/svt/2017-rattrapage/assets/document_7.png` (508 × 426) : page d'examen photographiée manquante | **Document 1, schéma** : à gauche une plantule de fève dans un bécher (encadré « Transfert d'une plantule de fève d'un milieu normal à un milieu radioactif pendant un cycle cellulaire »), flèche vers la même plantule (encadré « Transfert de cette plantule à un milieu non radioactif pendant un cycle cellulaire ») ; légendes « Thymidine radioactive » (symbole radioactif), « Thymidine non radioactive » (cercle blanc), « radioactivité » (damier) ; « Observation des chromosomes métaphasiques des cellules de la racine » ; deux dessins de chromosomes métaphasiques : « Premier cycle cellulaire » (les deux chromatides en damier) et « Deuxième cycle cellulaire » (une chromatide en damier sur deux). **Réutilisable** : `thymidine.html?vue=document` redessine déjà ce document avec les données de l'examen (plantule, deux milieux, chromosome métaphasique après chaque cycle, grains noirs = radioactivité). | `ig_x3_thymidine_doc` (décrire), `ig_x3b_cycle1`, `ig_x3c_cycle2` (expliquer), `ig_x3d_schema` (le schéma, la conclusion). `ig_r7_thymidine1`, `ig_r8_thymidine2` : la leçon construite sur le même document (pas l'exercice joué). |

Questions du national reprises sans être un exercice joué (pas de diapositive « énoncé ») : `ig_m4_anaphase` (question jumelle de
2018 R `p1q2` b, « deux caractéristiques de l'anaphase de la mitose », 0,5 pt, en démonstration) ; `ig_r1` → `ig_r6`
(Meselson, en lien avec 2018 R `p1q4_4`) ; `ig_c6_durees` d'après un sujet d'agronomie 2015 R (pas le national PC).
Non joués mais du chapitre : 2024 R II.4 (fin de phase S, yeux de réplication), 2024 N III.b et III.c (réplication en phase S).

### (b) Les moments où l'on compte ou parcourt un à un

| Diapositive | Simulation | Ce qu'on compte | État |
|---|---|---|---|
| `ig_l3_section` | `noyau.html?vue=acetabulaire` | les 3 fragments de l'algue (1 chapeau, 2 tige, 3 rhizoïde) | joué fragment par fragment (moments), sans numéro allumé |
| `ig_p1_chromosomes` | `bases.html?vue=chromosomes` | 46 chromosomes, 23 paires | non allumé un à un |
| `ig_p3_mitose_corps` | `bases.html?vue=oeuf` | 1 → 2 → 4 → 8 cellules → des milliards | une génération par moment (`o_oeuf`, `o_deux`, `o_quatre`, `o_huit`) ; démonstration allumée |
| `ig_n3_chromatides` | `zoom.html?vue=chromosome` | chromatides (1 puis 2), molécules d'ADN (2 × 1 = 2) | démonstration allumée (`deux_chromatides`, `chromatide`, `encadre`) ; pas de numéro 1, 2 |
| `ig_c1_cycle`, `ig_c4_aspect` | `cycle.html` | les phases G1, S, G2, M | parcourues une à une (moments) |
| `ig_c6_durees` | `documents.html?vue=durees` | les cellules (compteur), les doublements (×2, ×2 → 2 cycles) | compteur animé + flèches « ×2 » ; démonstration allumée (`chaine`, `cycle`) |
| `ig_c6b_phases` | `documents.html?vue=durees` | 20 cellules triées par phase (1 cellule = 5 %) | cellules qui volent une à une dans leur colonne, compteurs |
| `ig_m2` → `ig_m4b` | `mitose.html` | les 4 phases de la mitose | une diapositive par phase |
| `ig_m7_schema` | `mitose.html?vue=animale` | 2n = 4 chromosomes, 4 × 2 = 8 chromatides, 4 par pôle | démonstration allumée (`chromosomes`, `fuseau`, `pole_haut`) ; **les chromosomes ne s'allument pas un à un avec leur numéro** |
| `ig_s2_chargaff` | `adn.html?vue=chargaff` | les bases A, T, C, G | « bases comptées en animation, puis le tableau » (2ᵉ passe) |
| `ig_s5_complementaire` | `adn.html?vue=complementaire` | les 5 bases du brin, une à une (T → A, T → A, A → T, G → C, C → G) | posées une à une ; démonstration allumée |
| `ig_r3_g1`, `ig_r4_g2` | `meselson.html` | les bandes (1 en G1, 2 en G2) | démonstration de G1 allumée |
| `ig_x1c_metaphase`, `ig_x1d_corrige_metaphase` | `documents.html?vue=metaphase` | chromatides (2) et brins par chromatide (2) | **pas de dessin du chromosome à compter** (carte de QCM seule) |
| `ig_x3b_cycle1`, `ig_x3c_cycle2` | `thymidine.html?vue=document` | brins radioactifs / non radioactifs par molécule, chromatides marquées | démonstration sur le document : les molécules de chaque chromatide paraissent et s'allument (`brins_1`, `brins_2`, `molecule_marquee`, `molecule_non_marquee`) |

### (c) Ce qui est fait, ce qui reste

- **Fait — démonstration sur le document** : `etapes.js` (moteur de toutes les pages du dossier) exécute lui-même `allume`
  (`cible` : moment de la vue → la scène y joue, jamais en arrière ; repère → lueur jaune qui reste, la dernière plus vive,
  calque recalé à chaque image) et `eteins` (aussi `start` / `reset`) ; l'état porte `allumes`, `ce_qui_se_voit` dit ce
  qui est allumé ; le manifeste liste les deux commandes. `thymidine.html?vue=document` dessine en plus, à l'allumage
  seulement, la molécule d'ADN de chaque chromatide (bleu ancien, rouge radioactif, blanc nouveau, comme la vue
  `experience`) et sa légende. Les 63 lignes des 15 démonstrations du cours portent `allume` (dont les trois exercices du
  national : `ig_x1f_associer_couples`, `ig_x3b_cycle1`, `ig_x3c_cycle2`) ; chaque cible vérifiée dans sa page (repère
  dessiné ou moment), sauf les cibles que l'allumage fait paraître.
- **Fait — l'énoncé d'abord** : 4 diapositives (`ig_x1a_enonce`, `ig_x1c0_enonce`, `ig_x1e0_enonce`, `ig_x3_enonce`), dans
  les blocs `ig_s7_b3` et `ig_s8_b2`, cours en ligne et copie en attente.
- **Pistes ajoutées au `_voix.json` : 4** (les 4 diapositives « énoncé », type `diapositive`) ; aucun texte dit existant changé.
- **Pas fait** : le comptage allumé un à un
  avec numéro (règle 16) : aucun des moments du tableau (b) n'a encore « 1, 2, 3… » écrits à la craie à côté d'une lueur
  — à faire en priorité sur `ig_m7_schema` (4 chromosomes, 8 chromatides), `ig_n3_chromatides` et le chromosome du QCM
  2018 R (`ig_x1d`, il faudra un dessin et une voix nouvelle).
<!-- ch3 : fin -->

<!-- ch4 : début -->
## Ch4 — Du gène à la protéine (`svt_ch4_relation_gene_proteine`)

Simulations : `frontend/public/media/simulations/svt/relation_gene_proteine-tableau/` (moteur commun `etapes.js`).
Audit du 19 novembre 2026.

### (a) Exercices du national joués dans le cours

**Énoncé d'abord : fait** (19/11, après l'arrivée du gabarit `shared/examen/feuille.js`) — une feuille d'examen
reproduite en code par exercice, dans le dossier du cours (le sujet SVT n'a pas de `/media/examens/svt/<sujet>.json`,
le mode direct `feuille.html?sujet=…` ne marche pas pour lui) : `enonce_2025N.html` → `rg_e2a_enonce`,
`enonce_2024N.html` → `rg_e5_enonce`, `enonce_2020N.html` → `rg_e7_enonce`, `enonce_2022N.html` → `rg_e8_enonce`
(outils communs `feuille_svt.js` : code génétique complet, tableaux de séquences, SVG). Aucun scan montré.
Limites : 2025 N et 2022 N s'arrêtent aux questions jouées (partie I de l'exercice) ; le document 1 du 2020 N a ses
formules chimiques simplifiées ; la case « page » de l'en-tête porte la page de la 1re question.

| Sujet | `exam.json` | Pages modèles (scan) | Questions jouées (points) | Diapositives du cours |
|---|---|---|---|---|
| 2025 N, ALD (ALDP, gène ABCD1) | partie II, « Exercice 2 » (5 pts), questions `1`, `2` | `2025-normale/pages/sujet_p3.jpg` (bas : I., donnée 1, doc. 1, Q1), `sujet_p4.jpg` (haut : donnée 2, doc. 2, doc. 3, Q2) | 1. relation protéine-caractère (0,75 pt) ; 2. ARNm, acides aminés, origine génétique (1,75 pt) | `rg_e2_reperages`, `rg_e3_lignes`, `rg_e4_phrase` (questions 3-5 : cobayes, hors chapitre) |
| 2024 N, amélogénèse imparfaite (gène AMELX) | partie II, « Exercice 2 » (6 pts), questions `1`, `2` | `2024-normale/pages/sujet_p3.jpg` (bas : I., donnée 1), `sujet_p4.jpg` (Q1, doc. 1, donnée 2, doc. 2, Q2, doc. 3) | 1. relation protéine – caractère (1 pt) ; 2. ARNm, acides aminés, origine génétique (2 pts) | `rg_e5a_document`, `rg_e5_national` (+ `rg_s4_trans_trad` cite un vrai/faux de la restitution 2024 N) |
| 2020 N, moustiques *Culex* résistants (AChE, gène Ace) | partie II, « Exercice 2 » (4 pts), questions 1, 2, 3 (sans `number`, le texte commence par « 1. », « 2. », « 3. ») | `2020-normale/pages/sujet_p5.jpg` (contexte, doc. 1, Q1), `sujet_p6.jpg` (doc. 2, Q2, doc. 3, doc. 4, Q3) | 2. relation mortalité – activité de l'AChE, hypothèse (1 pt) ; 3. ARNm, acides aminés, vérifier l'hypothèse (2 pts) ; Q1 (1 pt) seulement racontée | `rg_e7_moustiques`, `rg_e7b_hypothese`, `rg_e7c_verifier` |
| 2022 N, anémie de Blackfan-Diamond (ribosomes, RSP19) | partie II, « Exercice 1 » (5 pts), question `1` | `2022-normale/pages/sujet_p2.jpg` (contexte, donnée 1, doc. 1, Q1) | 1. comparer les sous-unités, expliquer le manque d'hémoglobine (1 pt) ; Q2 (séquences, 1,5 pt) non jouée | `rg_e8_ribosomes`, `rg_e8b_hemoglobine` |

Documents reconstitués d'après l'examen (pas un exercice joué en entier : pas de page d'énoncé) : `rg_p4_document`
(2023 N, hypercholestérolémie familiale, récepteur LDL ; `examen.html?vue=document_ldl`), `rg_m3_non_sens` (codon stop
prématuré, idée du 2023 N), `rg_m5_trois` (délétion d'un triplet, idée du 2017 N), `rg_s5_etapes` (trois schémas de la
traduction, 2018 R — pas de scan pour 2018 R), `rg_e1_restitution` (définitions), `rg_e6_drepanocytose` (cours, pas un sujet).

**Figures à redessiner pour la feuille d'examen** (modèles dans `backend/data/exams/svt/<année>-<session>/assets/`) :

- **2025 N, doc. 1** — schéma, `assets/doc1p3.png` : deux panneaux « Personne saine » / « Personne atteinte par l'ALD » ;
  peroxysome (cercle, « Membrane du Peroxysome ») ; « ALDP fonctionnelle » (transporteur, « Entrée », AGLC ✦ qui entrent,
  « Dégradation » → « Produits utilisables par la cellule ») → « Cellule à fonctionnement normal » ; « ALDP non
  fonctionnelle » (transporteur barré) → « Accumulation des AGLC dans le cytoplasme » → « Cellule à fonctionnement anormal ».
  Pas redessiné dans le cours (la vue `reperages` résume le texte).
- **2025 N, doc. 2** — séquence, `assets/doc2p4.png` : « Numéros des triplets : 147 … 152 » ; « Fragment de l'allèle normal :
  GTC AAC AGT GCC ATC CGT » ; « Fragment de l'allèle muté : GTC AAC AGA GCC ATC CGT » ; « → Sens de la lecture ».
  Réutilisable : `examen.html?vue=lignes` (sujet 2025N) l'écrit avec ces valeurs.
- **2025 N, doc. 3** — tableau du code génétique complet (1re lettre en ligne, 2e en colonne, 3e à droite), `assets/doc3p4.png`.
  Réutilisable : `code_genetique.html?vue=tableau`.
- **2024 N, doc. 1** — schéma, `assets/doc1p4.png` : améloblaste (personne saine) / améloblaste (personne atteinte) →
  « Sécrétion » → « Amélogénine normale » / « Amélogénine anormale » → « Calcium + Phosphore » → « Minéralisation normale de
  l'émail » / « Minéralisation faible de l'émail » → dent : « Émail dentaire normal » (« Dent saine ») / « Émail dentaire
  anormal » (« Dent atteinte »). Réutilisable en partie : `examen.html?vue=amelogenine_pas` (améloblastes et dents peints).
- **2024 N, doc. 2** — tableau, `assets/doc2p4.png` : colonnes « Numéros des triplets » / « Sens de lecture → 1 2 3 4 5 » ;
  lignes « Fragment de l'allèle normal : … AAT CAT CCC CGT GCT … », « Fragment de l'allèle muté : … AAT CAT CTC CGT GCT … ».
  Valeurs déjà dans `amelogenine_pas`.
- **2024 N, doc. 3** — code génétique complet, `assets/doc3p4.png` (comme 2025 N).
- **2020 N, doc. 1** — schéma de réaction, `assets/doc1p5.png` : figure a, l'acétylcholine se fixe sur le site actif de
  l'AChE → choline + acétate, l'enzyme libérée ; figure b, le carbamate occupe le site actif. Peint dans
  `national.html?vue=moustiques` (enzyme violette, molécules en sphères).
- **2020 N, doc. 2** — `assets/doc2p6.png` (la page 6 du scan coupe la figure a) : figure a, **tableau** « Concentration de
  l'insecticide en mg·L⁻¹ : 0 ; 10⁻² ; 1 » × « Activité de l'acétylcholinestérase chez la souche (en %) : S "sauvages" 97 ; 8 ;
  0 — R "mutants" 32 ; 32 ; 28 » ; figure b, **courbe** « Pourcentage de mortalité (%) » 0-100 en fonction de la
  « Concentration en insecticide (mg/L) », échelle logarithmique 0,1 → 10⁴ ; souche S de 0 % (0,1) à 100 % (1) ; souche R
  (tirets) de 0 % (≈ 2·10²) à 100 % (≈ 10³). Le cours dessine la figure a en barres : la feuille doit garder le tableau
  (règle 42) ; la courbe b est réutilisable (`moustiques`, mêmes valeurs).
- **2020 N, doc. 3** — séquence, `assets/doc3p6.png` : « Numéro des triplets : 243 … 251 », « Allèle Ace-S de la souche S :
  ATC TTC GGG GGT GGC TTC TAC TCC GGG », « Allèle Ace-R de la souche R : ATC TTC GGG GGT AGC TTC TAC TCC GGG »,
  « → Sens de lecture ». Réutilisable : `national.html?vue=moustiques_seq`.
- **2020 N, doc. 4** — tableau (extrait du code), `assets/doc4p6.png` : Leu UUA UUG ; Gly GGU GGC GGA GGG ; Ser AGU AGC UCU UCC ;
  Ile AUU AUC AUA ; Phe UUU UUC ; Tyr UAU UAC ; Arg CGU CGC CGA CGG ; Pro CCU CCC CCA CCG ; Stop UAA UAG UGA. Pas dessiné.
- **2022 N, doc. 1** — `assets/doc1p2.png` : figure a, **histogramme** « Quantité des sous-unités des ribosomes (UA) » 0-50
  (graduations de 10), « Individu sain » grandes 46 / petites 46, « Individu malade » grandes 46 / petites 23, légende
  barres pleines (grandes) et hachurées (petites) ; figure b, **schéma** : sous-unités libres → ribosomes sur l'« ARNm de
  l'hémoglobine » ; individu sain 5 ribosomes → « Quantité normale d'hémoglobine » (5 molécules) ; individu malade
  2 ribosomes complets, 3 grandes sous-unités seules → « Quantité faible d'hémoglobine » (2 molécules). Réutilisable :
  `national.html?vue=blackfan` (corrigé ce jour : 5 ribosomes et 5 hémoglobines chez le sain, comme le document ; l'axe du
  cours est gradué 0 / 23 / 46, la feuille doit garder 0-50 par 10).

### (b) Moments où l'on compte ou parcourt un à un

| Diapositive | Simulation (vue) | Ce qu'on compte | Fait |
|---|---|---|---|
| `rg_e3_lignes` | `examen.html?vue=lignes` | les 6 acides aminés lus dans le tableau (Val, Asn, Ser, Ala, Ile, Arg) | oui : `aa_1`…`aa_6` allumés sur la voix (pointage `allume`) ; repères `triplet_i`, `codon_i`, `aa_i`, `codonm_i`, `aam_i` disponibles |
| `rg_e5_national` | `examen.html?vue=amelogenine_pas` | les triplets 1 à 5 | oui : ligne 1 de la démonstration allume `brin_1`…`brin_5` un à un ; `brinm_i` disponibles |
| `rg_e7c_verifier` | `national.html?vue=moustiques_seq` | triplet par triplet (243 → 251) | oui : voix « قارن triplet ب triplet » → `tripletR_1`…`9` ; démonstration e0 ligne 1 → `tripletS_1`…`9` ; `num_i` disponibles |
| `rg_e8b_hemoglobine` | `national.html?vue=blackfan` | ribosomes complets : 5 chez le sain, 2 chez le malade | oui : ligne 1 de la démonstration → `ribosain_1`…`5`, `ribomalade_1`…`2` |
| `rg_r5_polysome` | `traduction.html?vue=polysome` | ribosomes 1, 2, 3, 4 du polysome | oui : `ribosome_1`…`4` sur la voix (« الثاني، الثالث، الرابع ») |
| `rg_r2_initiation` … `rg_r4_terminaison` | `traduction.html?vue=traduction` | étapes de la traduction, codon après codon | déjà un moment et un repère par étape (`codon_2`, `arnt_2`…) ; pas de numéro de codon |
| `rg_c4_traduire`, `rg_c2_tableau`, `rg_c3_initiation_stop` | `code_genetique.html?vue=tableau` | codons lus un à un dans le tableau | à faire : repères par codon (`codon_i`) et pointages |
| `rg_m1_comparer` … `rg_m6_juger` | `mutation.html?vue=mutation` | comparer triplet par triplet, nucléotide par nucléotide | à faire : repères par triplet sur les deux allèles |
| `rg_t3_bases`, `rg_t6_bareme` | `transcription.html` | bases ajoutées une à une, triplets TAC → AUG… | à faire |
| `rg_c1b_nirenberg` | `documents.html?vue=nirenberg` | découpage CCC CCC CCC | à faire |
| `rg_s5_etapes` | `traduction.html?vue=trois_schemas` | trois schémas : initiation, élongation, terminaison | à faire (un repère par schéma existe ? non vérifié) |

### (c) Ce qui est fait, ce qui reste

- **Moteur** (`etapes.js`, toutes les pages du dossier sauf `adn_arn`, `bilan`, `carte`) : commandes `allume {cible}` et
  `eteins` ; lueur jaune qui reste, la dernière plus vive ; une liste d'éléments d'un groupe compté (`comptes` de la vue)
  s'allume un à un (0,6 s) avec son numéro courant dans une pastille ; `reset`/`start`/`eteins` éteignent ; l'état porte
  `allumes`, `ce_qui_se_voit` les nomme, le manifeste liste `allume`/`eteins` et les cibles.
- **`allume` sur les lignes de démonstration** : 14 démonstrations (`rg_p4_document`, `rg_p5_beadle_tatum`,
  `rg_a5_in_vitro`, `rg_t2b_arbre_noel`, `rg_t6_bareme`, `rg_c1b_nirenberg`, `rg_e5a_document`, `rg_e5_national` q et e0,
  `rg_e7_moustiques`, `rg_e7b_hypothese`, `rg_e7c_verifier` q et e0, `rg_e8_ribosomes`, `rg_e8b_hemoglobine`,
  `rg_e6_drepanocytose`).
- **Pistes ajoutées au `_voix.json` : 4** (`rg_e2a_enonce`, `rg_e5_enonce`, `rg_e7_enonce`, `rg_e8_enonce`, voix
  nouvelles des énoncés) ; aucun texte dit existant n'a changé.
- **Pas fait** : le canevas écrit encore
  certaines réponses que la colonne de démonstration écrit aussi (`amelogenine_pas` q2_reponse, `moustiques_seq` arnm —
  ces moments ne sont pas joués pendant la démonstration, mais le seraient sur demande) ; les comptages « à faire » ci-dessus.
<!-- ch4 : fin -->
