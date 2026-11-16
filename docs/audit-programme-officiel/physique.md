# Audit physique : notre programme et nos cours face au cadre officiel

Date : 15 novembre 2026.
Référence : cadre de référence officiel de l'examen national, physique-chimie, filière Sciences physiques, options internationales (CNEEO, 2015), transcrit dans `backend/cours 2bac pc/cadres de references 2BAC PC/cadre-de-reference-de-l-examen-national-physique-chimie-spc-2.json` (partie `content_structure_physics`, poids, annexe 2 des TP).

Le PDF officiel n'a pas pu être ouvert depuis la session cloud (`www.tawjihnet.net` est bloqué par le réseau). Le JSON officiel est un résumé : il donne les notions de chaque chapitre, pas le détail de l'annexe 1. Les points ambigus ont été tranchés dans le sens le plus strict : ce que le JSON officiel ne cite pas est retiré. Les points qui mériteraient une relecture sur le PDF sont listés à la fin de l'étape 1.

## Le cadre officiel, partie physique (67 % de la note)

| Sous-domaine officiel | Poids | Notions officielles | Notre cours |
|---|---|---|---|
| 1. Ondes | 11 % | Ondes mécaniques progressives (définitions, célérité, retard temporel) ; ondes mécaniques progressives périodiques (période, fréquence, longueur d'onde, diffraction) ; propagation d'une onde lumineuse (diffraction, aspect ondulatoire, milieux dispersifs, indice de réfraction, θ = λ/a) | ch1, ch2, ch3 |
| 2. Transformations nucléaires | 8 % | Décroissance radioactive (composition du noyau, isotope, diagramme N/Z, α, β⁺, β⁻, γ, loi de décroissance, demi-vie) ; noyaux, masse et énergie (défaut de masse, énergie de liaison, fission, fusion, bilan énergétique) | ch4, ch5 |
| 3. Électricité | 21 % | Dipôle RC ; dipôle RL ; circuit RLC série (amortissement, régimes périodique / pseudo-périodique / apériodique, oscillations libres, entretien) ; applications (transmission d'informations, modulation d'amplitude, démodulation) | ch6, ch7, ch8 ; **modulation : aucun cours** |
| 4. Mécanique | 27 % | Lois de Newton ; applications (chute verticale avec frottement, chute libre, projectile, particules chargées dans un champ magnétique, lois de Kepler, satellites et planètes) ; rotation d'un solide autour d'un axe fixe ; systèmes oscillants (solide-ressort, torsion, pendule pesant, pendule simple, amortissement, résonance) ; aspects énergétiques ; atome et mécanique de Newton (quantification de l'énergie, spectre de raies) | **aucun cours** |

TP officiels de physique : célérité d'une onde mécanique ; diffraction d'une onde sonore ou ultrasonore ; diffraction de la lumière ; dispersion de la lumière blanche ; charge d'un condensateur ; tension aux bornes d'une bobine ; oscillations libres RLC ; modulation et démodulation ; lois de Newton ; chute verticale avec frottement ; projectile ; pendules et résonance.

## Étape 1 — Notre programme face au cadre officiel

Fichiers comparés : `perimetre.json` (clés de physique), `physique.json` (domaines ondes, nucléaire, électricité, mécanique), `physique_blueprint.json`, `programme_semestre1.json` (ordres 1 à 8), `cadre_reference_2bac_pc.json` (fiches `ondes_mecaniques`, `ondes_mecaniques_periodiques`, `ondes_lumineuses`, `radioactivite`, `energie_nucleaire`, `dipole_RC`, `dipole_RL`, `circuit_RLC`). Les parties chimie de ces fichiers n'ont pas été touchées (session chimie).

### (a) Ce que nous avions en trop (hors cadre officiel)

| Fichier | Avant | Après | Raison |
|---|---|---|---|
| `perimetre.json`, `ondes_lumineuses` (notions, méthodes, démonstrations, source) | « lois de Snell-Descartes n₁·sin i₁ = n₂·sin i₂ », « appliquer Snell-Descartes aux deux faces d'un prisme », « calcul des angles de réfraction dans un prisme » | dispersion par le prisme **interprétée qualitativement** (l'indice dépend de la fréquence, le violet est le plus dévié) | Les relations du prisme sont hors cadre (retirées du cours et de la fiche OL11 le 15/11, commit `01d8a70c`) ; le périmètre les gardait encore. |
| `perimetre.json`, `ondes_lumineuses`, terme hors programme « minimum de déviation » | « on applique les lois de Snell-Descartes sur chaque face du prisme » | « relations du prisme, minimum de déviation, Snell-Descartes en calcul » : le motif attrape aussi `A = r + r'`, `D = i + i' − A`, `sin i = n·sin r`, « Snell » | La phrase « à dire à la place » enseignait justement la notion retirée. |
| `physique.json`, `ondes_lumineuses` | « Lois de Snell-Descartes » | retiré ; remplacé par λ₀ = c/ν, fréquence invariante, λ = λ₀/n | Même raison. |
| `cadre_reference_2bac_pc.json`, `ondes_lumineuses` | 4 formules du prisme (capacité OL11 retirée) encore dans `formules`, mot-clé « angle de déviation », décision « partie finale C9 pour le devoir » | formules et mot-clé retirés, décision réécrite | Une fiche ne garde que les formules de capacités officielles. |
| `physique.json`, `ondes_sonores` | « Niveau d'intensité sonore L = 10 log(I/I₀) », « Effet Doppler (qualitative) » | retirés (écho, mesure de λ et v aux ultrasons, diffraction des ultrasons) | Ni le niveau sonore ni l'effet Doppler ne sont dans le cadre ; `perimetre.json` les avait déjà en hors programme : les deux fichiers se contredisaient. |
| `perimetre.json`, `ondes_sonores` | « hauteur d'un son liée à sa fréquence, intensité liée à l'amplitude », terme « hauteur d'un son » | retirés ; hauteur et timbre ajoutés aux termes hors programme | Pas dans le cadre. |
| `perimetre.json`, `mouvement_projectile` | « particule chargée dans un champ électrique uniforme, déflexion électrique » (notion, méthode, terme, source, niveau) | retiré ; ajouté aux termes hors programme | Le cadre PC ne cite que « particules chargées dans un champ magnétique ». |
| `physique.json` et `perimetre.json`, `circuit_RLC` | « régime critique » (régimes, termes du programme, méthodes) | trois régimes officiels : périodique, pseudo-périodique, apériodique ; « régime critique » ajouté au terme hors programme de la résistance critique | Le cadre cite exactement trois régimes. |
| `cadre_reference_2bac_pc.json`, `circuit_RLC` | RLC2 « le régime critique étant la frontière, sans calcul », mot-clé « régime critique » | phrase et mot-clé retirés ; « régime critique » dans `hors_cadre` (mot et motif) | Même raison. |
| `perimetre.json`, `oscillateur_mecanique` | amortissement « pseudo-périodique, apériodique, critique » | sans « critique » ; terme hors programme ajouté | Le cadre dit « amortissement ». |
| `perimetre.json` et `physique.json`, `champ_magnetique` | « cyclotron : accélération entre les dees… », « spectromètre de masse, cyclotron » comme applications | contextes d'énoncé dont le fonctionnement est décrit par l'énoncé ; on garde la séparation de deux isotopes par R = m·v/(|q|·B) | Le cadre cite le mouvement de la particule, pas les appareils. |
| `perimetre.json`, `modulation_AM` | termes « filtre passe-bas », « filtre passe-haut » | « élimination de la composante continue » | Les notions du cadre parlent de démodulation ; les noms de filtres sont hors programme dans le RC et n'étaient pas dans nos propres notions. |

### (b) Ce qui manquait

| Fichier | Ajout | Raison |
|---|---|---|
| `perimetre.json`, `physique.json` | Chapitre **`ondes_mecaniques_periodiques`** (fiche complète : double périodicité, λ = v·T, points en phase, stroboscope, diffraction, milieu dispersif) ; `ondes_mecaniques` ne garde que les ondes progressives (définitions, célérité, retard, L = v·θ) | Deux chapitres officiels distincts ; `programme_semestre1.json` citait déjà la clé `ondes_mecaniques_periodiques`, qui n'existait pas dans le périmètre. |
| `perimetre.json`, `physique.json` | Chapitre **`rotation_solide`** (grandeurs angulaires, moment, J_Δ donné, Σ M_Δ = J_Δ·θ̈) | Chapitre officiel ; il n'existait que comme une ligne dans les oscillateurs. |
| `perimetre.json`, `physique.json` | Chapitre **`aspects_energetiques`** (travail, théorème de l'énergie cinétique, énergies potentielles, énergie mécanique) | Chapitre officiel absent de `physique.json`. |
| `perimetre.json`, `physique.json` | Chapitre **`atome_mecanique_newton`** (niveaux d'énergie, photon ΔE = h·ν, spectres de raies) | Chapitre officiel totalement absent. |
| `perimetre.json`, `dipole_RC` | associations de condensateurs et charge à courant constant | Capacité RC3 de la fiche, demandée au national (2018 N), absente du périmètre. |
| `physique.json` | RC : q = C·u_C, i = dq/dt, associations ; RL : u = L·di/dt + r·i, I₀ = E/(R+r), τ = L/(R+r) ; RLC : énergie totale, effet Joule, u_G = k·i ; modulation : circuit d'accord ; oscillateurs : amortissement et résonance (qualitatif) ; ondes lumineuses : lumière monochromatique, λ₀ = c/ν, spectre visible, λ = λ₀/n | Notions officielles qui manquaient à la liste du programme. |
| `physique_blueprint.json` | poids officiels de la physique et liste des sujets à ne jamais poser | Le blueprint ne citait pas le cadre. |
| `programme_semestre1.json` | ch1 → cours `phys_ch1_waves_exemple` ; ch2 → statut `en_ligne`, cours `phys_ch2_ondes_periodiques` ; note des chapitres de physique sans cours (semestre 2) | Le ch2 est publié mais était marqué « à explorer ». |

**Chapitres officiels sans cours** : modulation et démodulation d'amplitude ; toute la mécanique (lois de Newton et chute verticale, projectile, particule dans un champ magnétique, satellites et Kepler, rotation, systèmes oscillants, aspects énergétiques, atome et mécanique de Newton). Ils n'ont pas non plus de fiche dans `cadre_reference_2bac_pc.json` ; une fiche est à créer avant chaque cours (skill `cours-concentration`, étape 8). La mécanique pèse 27 % de la note et l'électricité 21 % (la modulation tombe dans 10 sessions sur 20 du national) : ce sont les prochains cours à faire.

### (c) Ce qui était mal formulé ou mal classé

| Fichier | Avant | Après | Raison |
|---|---|---|---|
| `physique.json`, `ondes_lumineuses` | « Relation sin(θ) = λ/a » (topic et question type) | « θ = λ/a (θ en rad) » | Le cadre écrit θ = λ/a. |
| `physique.json`, `ondes_mecaniques` | « diffraction : condition a ≈ λ » | « nette quand a est de l'ordre de λ ou plus petite » (au chapitre périodique) | Le barème attend la comparaison a ≤ λ ; « a ≈ λ » laissait croire qu'une fente plus fine ne diffracte pas. |
| `physique.json`, `modulation_AM` | « Taux de modulation : m = U_m/U_p (condition m ≤ 1) » | « m = U_m/U₀ ; bonne modulation si m < 1 et f_p ≫ f_m » | **Erreur scientifique** : le taux se rapporte à la tension de décalage U₀, pas à l'amplitude de la porteuse ; m = 1 est déjà la limite. |
| `physique.json`, `modulation_AM` | « Démodulation : détection d'enveloppe + filtre passe-bas » | « détection d'enveloppe (diode + RC parallèle, T_p ≪ RC < T_m) puis élimination de la composante continue » | **Erreur** : la seconde étape enlève la composante continue (dipôle RC série), ce n'est pas un passe-bas. |
| `physique.json`, `nucleaire` | « ΔE = \|Δm_produits − Δm_réactifs\| × c² » | « E_lib = \|Σm(produits) − Σm(réactifs)\|·c² » | Notation fausse : on soustrait des masses, pas des défauts de masse. |
| `physique.json`, `dipole_RL` | « i(t) = (E/R)(1 − e^(−t/τ)), τ = L/R » | « I₀ = E/(R + r), τ = L/(R + r) » | La bobine a une résistance r dans tous les nationaux. |
| `perimetre.json`, `ondes_lumineuses` | « demi-largeur angulaire θ = λ/a (petits angles) » | « écart angulaire θ = λ/a (θ en rad) » | Mot du cadre. |
| `perimetre.json`, `radioactivite` | « le noyau fils émet un photon γ » | « émet un rayonnement γ (onde électromagnétique) » | Le photon et E = h·ν appartiennent au chapitre « Atome et mécanique de Newton » ; la fiche du chapitre dit déjà « rayonnement γ ». |
| `perimetre.json`, `circuit_RLC` | entretien par « montage à amplificateur opérationnel, résistance négative, u = R·i » | « générateur u_G = k·i, k = R + r » | Écriture des sujets nationaux et de la fiche ; l'amplificateur opérationnel n'est pas au cadre. |
| `perimetre.json`, `ondes_sonores` | f pour la fréquence | N | Notation de la fiche et des nationaux. |
| `perimetre.json`, `oscillateur_mecanique` | rotation et énergies mêlées aux oscillateurs | rotation et énergies dans leurs propres chapitres | Trois notions officielles distinctes. |
| `cadre_reference_2bac_pc.json`, fiches de physique | « Le texte officiel du cadre n'a pas été relu : capacités à confirmer » | note de collationnement avec la notion officielle de chaque fiche | Collationnement fait ; chaque capacité relève d'une notion officielle. |
| `cadre_reference_2bac_pc.json`, `radioactivite`, `energie_nucleaire`, `ondes_lumineuses` | « E = hν », « photon » listés hors cadre sans précision | précisé : au programme dans « Atome et mécanique de Newton », hors de ces chapitres | Mal classé : ce n'est pas hors programme, c'est un autre chapitre. |

### Points à relire sur le PDF officiel (non tranchés par le JSON résumé)

- Méthode d'Euler (chute verticale) et repère de Frenet : gardés, ils figurent dans les orientations pédagogiques et les nationaux ; le JSON résumé ne les nomme pas.
- Spectre à trois raies du signal modulé et méthode du trapèze : gardés au périmètre de la modulation, à confirmer.
- Plan incliné avec frottement (coefficient de frottement) : gardé comme application des lois de Newton.

## Étape 2 — Les cours de physique

Huit cours audités, chacun par rapport à sa fiche du cadre et à son périmètre : correspondance au cadre, hors programme (écran, voix, questions, réactions préparées, cahier, simulations), exactitude scientifique (tous les calculs refaits), organisation. Toutes les compétences des huit cours relèvent d'une capacité officielle ; aucune partie n'est hors cadre après correction.

| Cours | Corrections | Voix à refaire |
|---|---|---|
| ch1 Ondes mécaniques progressives (`phys_ch1_waves_exemple`) | 14 | 12 |
| ch2 Ondes mécaniques progressives périodiques | 21 | 16 |
| ch3 Propagation d'une onde lumineuse | 29 | 19 |
| ch4 Décroissance radioactive | 31 | 9 |
| ch5 Noyaux, masse et énergie | 27 | 17 |
| ch6 Dipôle RC | 18 | 6 |
| ch7 Dipôle RL | 14 | 10 |
| ch8 Circuit RLC série | 23 | 24 |
| **Total** | **177** | **113** |

Les erreurs les plus fréquentes étaient dans les **réactions préparées aux mauvaises réponses** : elles attribuaient la mauvaise réponse à une erreur que l'élève n'avait pas faite (ou se trompaient de calcul). Les écrans, les questions et les bonnes réponses des QCM étaient justes, sauf les points listés ci-dessous (données fausses de deux nationaux en RC, figure fausse en ch2, régime critique en ch8, traces du prisme en ch3, diagnostics faux). Aucun `speech_text.mixed` de diapositive n'a été modifié ; seules les voix françaises de 3 diapositives (ol_n1_ralentit, en_d4_carbone, en_m4_931) ont changé. Les chemins audio n'ont pas été touchés : chaque texte listé « voix à refaire » ne correspond plus à sa piste actuelle.

Fichier supprimé : `ondes-lumineuses-tableau/prisme-angles.html` (simulation des relations du prisme, utilisée par aucune diapositive ; seule `exploration/ondes_lumineuses.json` la cite encore, comme historique). Diapositive retirée : `lc_r2b_critique` (ch8, régime critique) ; sa piste `lc_r2b_critique_v12.mp3` ne sert plus.

### phys_ch1_waves_exemple — Ondes mécaniques progressives
Notions officielles couvertes : « Ondes mécaniques progressives (définitions, célérité, retard temporel) » (fiche `chapitres.ondes_mecaniques`, OMP1 à OMP8 toutes travaillées) ; exemples sonores du périmètre `ondes_sonores` (son longitudinal, pas dans le vide, ultrasons au-delà de 20 kHz, écho). Compétences → capacités : C1 → OMP1 ; C2 → OMP2 ; C3 → OMP3, OMP6 ; C4 → OMP4, OMP5 ; C5 → OMP8 ; C6 → OMP7 ; C7 → OMP6 ; C8 → OMP6 ; C9 → OMP6.
Tous les calculs des diapositives, exercices, rappels et simulations ont été refaits : ils sont justes (340 m/s, 345 m/s, 300 m/s, 0,25 s, 2 m, 3 ms, 17 m, 0,3 s, L = 0,2 m, acier 0,2 s / eau 0,67 s, sonar, oscilloscope). Toutes les bonnes réponses des QCM et des vrai/faux sont justes. Les erreurs trouvées sont dans les réactions préparées : l'explication donnée pour une mauvaise réponse ne correspondait pas au calcul qui donne cette valeur.
Nombre de corrections : 14
| Diapositive / élément | Avant → après | Raison |
|---|---|---|
| C3_r2, réaction à l'option 0 « 0,12 m/s », niveau 1 (ecrit + parole) | « 0,12 vient de la division inversée (Δt / d) » → « 0,12 vient de la multiplication d × Δt = 6 × 0,02 » | Faux : 0,02 / 6 ≈ 0,003 ; 0,12 = 6 × 0,02 (le niveau 2 le disait déjà). |
| C7_r2, réaction à l'option 0 « 0,33 ms », niveau 1 (ecrit + parole) | « une division (3 ÷ 1) » / « قسمتي trois divisions على la sensibilité » → « (1 ÷ 3) » / « قسمتي la sensibilité على trois divisions » | Faux : 3 ÷ 1 = 3 ; 0,33 = 1 ÷ 3. |
| C8_r2, réaction à l'option 2 « 3400 m », niveau 1 (ecrit + parole) | « Tu as bien calculé v · τ, c'est la distance parcourue » → « 3400 m ne vient pas de v · τ : 340 × 0,1 = 34. Tu as sans doute divisé par τ (340 / 0,1 = 3400)… » | Faux : v · τ = 34 m, pas 3400 m. |
| C8_r2, réaction à l'option 2 « 3400 m », niveau 2 (ecrit + parole) | « 3400 m est trop grand : tu as oublié de diviser par 2 » → « 3400 m vient d'une division par τ (340 / 0,1)… 2d = 34 m, d = 17 m » | Faux : oublier le /2 donne 34 m (option A), pas 3400 m. |
| C4_r2, réaction à l'option 1 « 1 s », niveau 2 (ecrit + parole) | « on divise la distance par la célérité (et non l'inverse) » → « 1 s vient de la multiplication v × SM = 2 × 0,5 : il faut diviser » | Mauvais diagnostic : l'inverse (v / SM) donne 4 s, pas 1 s. |
| C8_r3, réaction « Vrai » juste (ecrit + parole) | « Les ultrasons ont une fréquence supérieure à 20 kHz » / « la fréquence ديالها » → « Les ultrasons sont au-delà de 20 kHz » | « fréquence » est dans `hors_cadre` (chapitre suivant, non annoncé). |
| C8_r3, réaction « Faux », niveau 1 (ecrit + parole) | « Une fréquence qui dépasse cette valeur » / « ترددات » → « Un son au-delà de cette valeur » / « الصوت اللي كيفوت » | Même raison. |
| C8_r3, réaction « Faux », niveau 2 (ecrit + parole) | « ondes sonores de fréquence supérieure à 20 kHz » / « الفريكونس ديالهم » → « sons au-delà de 20 kHz » | Même raison. |
| C1_r3, réaction « Vrai », niveau 2 (ecrit + parole) | « …alors que la lumière, qui n'est pas une onde mécanique, si » → « Par exemple, le son ne se propage pas dans le vide. » | La lumière et sa propagation dans le vide, c'est le chapitre 3 (ondes lumineuses), non annoncé. |
| wx_s2_b1, exercice, réaction à l'option 2 « 3,06 m/s », niveau 1 (ecrit + parole) | « Ta relation v = d / τ est la bonne… erreur d'unité » → « 3,06 ne vient pas de v = d / τ : c'est le produit d × τ = 1,02 × 3… » | Mauvais diagnostic : 3,06 = 1,02 × 3 (une multiplication), ce n'est pas une erreur de conversion. |
| wx_s2_b1, exercice, réaction à l'option 2 « 3,06 m/s », niveau 2 (ecrit + parole) | « 3,06 m/s vient d'une erreur de conversion » → « vient d'une multiplication (1,02 × 3) au lieu d'une division » | Même raison. |
| wx_b2_national, exercice e0, réaction à l'option 2 « 0,29 m/s », niveau 2 (ecrit + parole) | « L'élève a donné la pente elle-même au lieu de son inverse » / « واحد على tau » → « 0,29 m/s ne correspond pas à 1/pente : il fallait inverser la pente » | Faux : la pente elle-même est l'option B (2,9 × 10⁻³) ; « 1/τ » était une notation fausse. |
| Simulation `ondes-tableau/milieux.html`, texte de présentation envoyé au tuteur (`protocole.texte`) | « (v ≈ 331·√(1+θ/273)) » → « (l'air chaud transmet le son plus vite) » | Formule hors cadre (la célérité du son est une donnée ; le périmètre exclut les formules de célérité en racine) : le tuteur pouvait la lire à voix haute. |
| Simulation `ondes-tableau/milieux.html`, `ce_qui_se_voit` après la course | chaîne entre apostrophes droites : le tuteur recevait littéralement « ${fr(arrivee(...))} s (${vAir()} m/s… » ; « eau 0,7 s » → chaîne entre accents graves (valeurs remplacées) ; « eau 0,67 s » | Texte affiché faux (les valeurs n'étaient pas calculées) ; 0,67 s pour avoir le même arrondi que l'écran. |

Voix à refaire (les textes ont été corrigés, les chemins `audio` n'ont pas été touchés et ne correspondent plus au texte) :
- C3_r2 (reponses.0.1.parole)
- C7_r2 (reponses.0.1.parole)
- C8_r2 (reponses.2.1.parole, reponses.2.2.parole)
- C4_r2 (reponses.1.2.parole)
- C8_r3 (reponses.0.juste.parole, reponses.1.1.parole, reponses.1.2.parole)
- C1_r3 (reponses.0.2.parole)
- wx_s2_b1, exercice du bloc (exercice.reponses.2.1.parole, exercice.reponses.2.2.parole)
- wx_b2_national (concentration.reponses.e0.2.2.parole)
Aucun `speech_text` de diapositive n'a été modifié : les `mot` / `apres_mot` restent valides.

Signalé sans correction (organisation, doutes) :
- wx_b2_national : la voix dit « Au tableau, deux exercices du même type que le national », mais le tableau n'en montre qu'un (`exercises[0]`, le vrai/faux est dans la réserve `exercices_fin_de_cours`). Règle du skill : une voix n'invite jamais à un exercice qui n'est pas au tableau. Il faut corriger la voix (à refaire) ou remettre le vrai/faux au tableau ; je n'ai pas tranché.
- C9 « Rédiger comme le barème » est rattachée à OMP6. C'est défendable (pente = 1/v et reconnaissance des documents relèvent d'OMP6), mais la partie « méthode de rédaction » n'est pas une capacité du cadre. Elle reste acceptable comme méthode transversale ; à confirmer.
- wx_c2_facteurs, réactions e0.1.2 et e0.2.2 : pour une corde, « elle dépend de la nature du milieu et de la température » est incomplet (pour une corde, c'est la tension et la masse linéique), mais ce n'est pas faux. Je l'ai laissé.
- milieux.html : à 20 °C, l'écran affiche v ≈ 343 m/s pour l'air (formule interne), alors que le cours dit ≈ 340 m/s. C'est cohérent avec « ≈ 340 » ; je l'ai laissé.
- Ancien cours `phys_ch1_waves_course_v1.json` (non modifié) : il contient une partie hors programme « superposition » (diapositives waves_overlap_lab et waves_overlap_summary, rappel au début de waves_tp_report, ligne « Expliquer la superposition » de waves_selfassessment, titre d'activité et catalogue) et les séismes « ondes S / ondes P » (waves_a01_s02, écran et voix). Il contient aussi des `feedback_incorrect` hors sujet (« Compare les directions… ») sur waves_sound_trace et waves_medium_summary. Je ne l'ai pas modifié pour trois raisons : il n'est pas servi tant que `remplace_la_base` est vrai sur le cours exemple ; le test `backend/app/tests/test_waves_reference.py` exige la variante de simulation `superposition` ; et retirer ces diapositives demande aussi de modifier le script et le test. C'est à décider : retirer la partie et adapter le test, ou dépublier l'ancien cours. Aucune erreur de calcul dans v1 (40 m/s, 3 m/s, 340 m/s, 10 ms vérifiés).
- Script `phys_ch1_waves_mixed_script_v3.json` (non modifié) : séismes dans `waves_a01_s02`, superposition dans `waves_overlap_lab` / `waves_overlap_summary`. « Périodiques » dans `waves_transition` est annoncé comme le chapitre suivant : toléré. Calculs justes.
- Le dossier `simulations/physics/progressive/` n'est pas utilisé par le cours exemple : je ne l'ai pas audité.

### phys_ch2_ondes_periodiques — Ondes mécaniques progressives périodiques
Notions officielles couvertes : Ondes mécaniques progressives périodiques (période, fréquence, longueur d'onde, diffraction) ; milieux dispersifs ; exemple des ondes sonores et ultrasonores (perimetre `ondes_sonores` : ultrasons, 20 Hz – 20 kHz, célérité du son ≈ 340 m/s). Compétences → capacités : C1 → OPP1, C2 → OPP2, C3 → OPP3 + OPP5, C4 → OPP4, C5 → OPP6, C6 → OPP7, C7 → OPP9, C8 → OPP10, C9 → OPP8. Toutes les capacités OPP1 à OPP10 sont travaillées et évaluées (question, exercice ou rappel). Aucune partie hors cadre (rien sur θ = λ/a, l'indice de réfraction, les interférences, les ondes stationnaires, les grandeurs apparentes du stroboscope ou l'effet Doppler ; le ralenti du stroboscope est seulement montré, « on ne calcule rien »).
Nombre de corrections : 21 (1 dans la simulation, 1 énoncé lu, 19 réactions préparées ; une réaction compte une fois, qu'on ait corrigé l'écrit seul ou l'écrit et la voix)
| Diapositive / élément | Avant → après | Raison |
|---|---|---|
| op_l6_source, simulation `figures.html?fig=fig_enonce_cuve` (dessin, calcul écrit, description) | M sur le 6e trait, cote partant du 2e trait, « depuis S : SM = 6 λ = 9 cm », intervalles 1 à 6 → M sur le 5e trait, cote partant du 1er trait, « depuis S : SM = 1 λ + 4 λ = 5 λ = 7,5 cm », intervalles 1 à 5 | La figure contredisait l'écran, la voix, la question et la démonstration de la diapositive (1 λ avant la cote + 4 λ dans la cote = 5 λ). La figure n'est utilisée que par ce cours. |
| op_s3_dispersif, question.enonce_dit | « … la célérité … , il manque la fin de la phrase dans l'énoncé que j'ai reçu, envoie-moi le texte complet… » → la question lue avec ses trois choix | Texte parasite d'une génération, lu à l'élève. |
| op_t6_film, réaction e0 option 0 (0,05 Hz), niveau 2 (écrit + voix) | « 0,05 Hz est la valeur de T en secondes » → « 0,05 Hz vient de 1/20 : T laissée en ms » | Faux : T = 0,02 s ; 0,05 = 1/20. |
| op_m6b_deja_ecartes, réaction q option 1 (5,85 cm), niveau 1 (écrit + voix) | « tu as divisé par 2 sans justifier » → « tu as divisé 11,7 cm (la position de R₂) et non le déplacement » | Mauvais diagnostic : 5,85 = 11,7 / 2. |
| op_r3b_calculs, réaction q option 0 (100 Hz), niveau 1 (écrit + voix) | « N a été calculée à l'envers » → « tu as utilisé 10 ms, c'est le retard τ, pas T » | Mauvais diagnostic : 100 Hz = 1/(10 ms). |
| op_r3b_calculs, réaction q option 0, niveau 2 (écrit + voix) | « l'erreur vient de la division : 1/0,02 = 50, pas 100 » → « 100 Hz vient de 1/(10×10⁻³) : 10 ms est le retard τ » | Même raison. |
| op_r3b_calculs, réaction q option 2 (33 Hz), niveau 1 (écrit + voix) | « il faut convertir T en secondes » → « tu as pris T = 30 ms ; T = 20 ms entre deux crêtes voisines, sans ajouter τ » | Mauvais diagnostic : 33 Hz = 1/(30 ms). |
| op_r3b_calculs, réaction e0 option 1 (0,25 m/s), niveau 2 (écrit + voix) | « L'élève a inversé la division (τ / SM) » → « 0,25 vient de 2,5 / 10 : SM et τ non convertis » | Faux : τ/SM = 0,4 s/m ; et « L'élève » au lieu de « tu ». |
| op_x2_national_2020, réaction e0 option 1 (20 s), niveau 2 (écrit + voix) | « diviser d par v, pas l'inverse » ; voix « 0,05 / 0,25 donne 0,5 s » → « 20 s vient de 5 / 0,25 : d restée en cm » ; voix 0,05 / 0,25 = 0,2 s | Faux diagnostic, et un calcul faux dans la voix. |
| op_x2_national_2020, réaction e0 option 2 (1,25 s), niveau 1 (écrit + voix) | « la distance doit être en mètres » → « tu as multiplié d par v (5 × 0,25 = 1,25) » | Mauvais diagnostic. |
| op_x2_national_2020, réaction e0 option 2, niveau 2 (écrit + voix) | « division inversée » ; voix « 0,5 / 0,25 donne 0,5 s » → « 1,25 s vient de 5 × 0,25 » ; voix 0,05 / 0,25 = 0,2 s | Mauvais diagnostic, et calcul faux dans la voix. |
| op_x2_national_2020, réserve e1, énoncé 1, réaction « faux » niveau 2 (écrit + voix) | « λ (propriété de la source) » → « N imposée par la source, v par le milieu, donc λ = v/N ne change pas » | Faux : λ dépend aussi du milieu. |
| op_x2_national_2020, réserve e1, énoncé 1, réaction juste (écrit + voix) | « λ… c'est une propriété de la source » → même justification que ci-dessus | Même raison. |
| op_x3_devoir, réaction q option 0 (0,9 m/s), niveau 2 (écrit + voix) | « 0,9 m/s vient de 0,015 × 30 » → « 0,9 m/s vient de 0,045 × 20 : AB pris pour λ » | Calcul faux (0,015 × 30 = 0,45). |
| op_x3_devoir, réaction e0 option 1, niveau 2 (écrit + voix) | « AB/λ = 3, donc pas de retard » → « B reproduit le mouvement de A avec un retard de 3 T, donc en phase » | Faux : il y a un retard (3 T). |
| op_x3_devoir, réaction e0 option 2, niveau 2 (écrit) | « Réponse de l'élève (…) : fausse. » → « « Ni en phase ni en opposition de phase » est donc faux. » | Texte adressé à l'élève à la 3e personne. |
| op_t4_inverse, réaction q option 0, niveau 1 (écrit) | « L'élève a recopié… » → « Tu as recopié… » | Même raison. |
| op_x1_national_2017, réserve e0 option 2, niveau 1 (écrit) | « L'élève a bien posé… » → « Tu as bien posé… » | Même raison. |
| Séance 3, bloc 3, exercice (stroboscope), réaction option 0 niveau 1 (écrit) | « la fréquence de la lumière égale celle du vibreur » → « la fréquence des éclairs… » | Faux en physique : la fréquence de la lumière n'est pas celle des éclairs. Voix gardée (« الضوء » y veut dire l'éclair, comme dans la voix de op_m2_immobile). |
| Rappel C9_r2, réaction option 2 (0,05 s), niveau 2 (écrit + voix) | « l'erreur vient de la conversion » → « 0,05 s vient de 0,1 × 0,5 : on divise d par v » | Mauvais diagnostic. |
| Rappel C6_r4, réaction option 2 (0,34 m/s), niveau 2 (écrit + voix) | « Votre… (mm et kHz non convertis) » → « Ton… (40 kHz non converti en 40 000 Hz) » | Faux : sans aucune conversion on trouve 340. 0,34 = 8,5×10⁻³ × 40. |

Voix à refaire : op_s3_dispersif (question.enonce_dit / enonce_audio) ; op_t6_film (reponses_fin_de_cours.e0.0.2.parole) ; op_m6b_deja_ecartes (reponses.q.1.1.parole) ; op_r3b_calculs (reponses.q.0.1.parole, reponses.q.0.2.parole, reponses.q.2.1.parole, reponses.e0.1.2.parole) ; op_x2_national_2020 (reponses.e0.1.2.parole, reponses.e0.2.1.parole, reponses.e0.2.2.parole, reponses_fin_de_cours.e1s0.0.2.parole, reponses_fin_de_cours.e1s0.1.juste.parole) ; op_x3_devoir (reponses.q.0.2.parole, reponses.e0.1.2.parole) ; rappel C9_r2 (reponses.2.2.parole) ; rappel C6_r4 (reponses.2.2.parole). Total : 16 pistes. Aucun `speech_text` de diapositive n'a été modifié, donc aucun `mot` de pointage n'est touché. Les chemins audio n'ont pas été changés.

Signalé sans correction (organisation, doutes) :
- Séance 4, bloc 3, exercice : λ₂ = 0,6 cm à 40 Hz donne v₂ = 0,24 m/s, plus petit que 0,30 m/s à 20 Hz. Or le cours (et la cuve) montrent 0,33 m/s à 30 Hz. Pour des rides de cuve (20 à 40 Hz), la célérité augmente avec la fréquence. La conclusion (« dispersif ») reste juste, mais la valeur est peu réaliste et contredit le reste du cours. Proposition : λ₂ = 0,9 cm (v₂ = 0,36 m/s). Il faudrait alors changer l'option, l'explication, la démonstration et les 6 réactions, voix comprises.
- op_s2_air, speech_text.fr : « les graves et les aigus arrivent ensemble » touche à la hauteur d'un son (hors cadre). La voix jouée (`mixed`) ne le dit pas : seul le texte `fr` est en cause. Rien n'a été changé.
- op_m2_immobile, voix `mixed` : « la fréquence ديال الضوء » (au sens de l'éclair). L'écran dit bien « fréquence des éclairs ». C'est acceptable, à surveiller lors d'un nouvel enregistrement.
- Réactions dont le diagnostic est vague mais pas faux (par exemple C5_r4 option 4,7 m/s, qui vient de 40 / 8,5 alors que la réaction parle d'unités ; op_t7 option 5 ms ; op_x3 e0 option 1 « l'idée de milieu dispersif ») : laissées telles quelles.
- Organisation : l'ordre est logique et les prérequis sont enseignés avant d'être utilisés. Les rappels du chapitre 1 (v = d/Δt, τ = d/v) ouvrent le cours et sont rattachés à C9. Les deux diapositives de bilan sont rattachées à C1 : il n'y a pas de compétence « bilan » séparée, comme dans les autres cours. La fiche et la carte reprennent bien les 9 compétences.
- Contrôle : tous les calculs des diapositives, exercices, rappels et réactions ont été refaits ; les `correct` des QCM et vrai/faux sont justes. Les simulations ont été relues (textes et valeurs : cuve, fente, stroboscope, récepteurs, air, dispersif, corde, figures, méthode-phase, bilan, carte) : rien d'autre de faux ni hors cadre.

### phys_ch3_ondes_lumineuses — Propagation d'une onde lumineuse
Notions officielles couvertes : diffraction (fente, fil), aspect ondulatoire, relation θ = λ/a, exploitation L = 2λD/a et courbes, lumière monochromatique / polychromatique, λ₀ = c/ν, spectre visible, indice de réfraction n = c/v, λ = λ₀/n, milieux dispersifs, dispersion par le prisme (qualitative) ; compétences → capacités : C1 → OL1, OL2 ; C2 → OL3, OL2 ; C3 → OL4 ; C4 → OL4, OL2, OL9 ; C5 → OL5 ; C6 → OL6, OL7, OL8 ; C7 → OL8, OL9 ; C8 → OL6, OL10. Aucune compétence sans capacité officielle ; pas de partie « pour le devoir ».
Nombre de corrections : 29

| Diapositive / élément | Avant → après | Raison |
|---|---|---|
| `note` du cours | « Relations du prisme en partie finale courte « pour le devoir » (décision à valider). » → phrase retirée | Trace de la partie prisme retirée (C9) |
| Activité bilan, titre | « XI. Bilan du chapitre » → « X. Bilan du chapitre » | La numérotation sautait le X (trace de la partie retirée) |
| ol_g1_points, titre | « Cinq fentes, cinq mesures » → « Quatre fentes, quatre mesures » | L'écran, la voix et courbe.html ont 4 fentes (0,40 ; 0,20 ; 0,10 ; 0,05 mm) |
| ol_g1_points, réaction q0 (écrit + voix) | « la distance L entre les taches » → « la largeur L de la tache centrale » | Mauvaise définition de L |
| ol_l1_metre, réaction e0.0.1 (voix) | « multiplier 6,5 par 10⁻⁹ » → « multiplier 650 par 10⁻⁹ » | 6,5 × 10⁻⁹ redonne la mauvaise réponse |
| ol_l9_etablir, réaction e0s0.0.1 (écrit) | « relation entre teta et lambda sur a… au premier ligne… Quel ligne » → « θ = λ/a… à la première ligne… Quelle ligne » | Fautes de français ; notation θ à l'écran |
| ol_l9_etablir, réaction e0s0.1.juste (écrit) | « Vrai : la réponse est fausse… teta = λ/a » → « Juste : l'affirmation est fausse… θ = λ/a » | Phrase contradictoire ; notation |
| ol_g5_autres, réactions q1.2 (écrit + voix) et q2.2 (voix) | a = 0,06 mm = 6·10⁻⁴ m → 6·10⁻⁵ m | Conversion fausse (le résultat 600 nm affiché n'était pas cohérent avec 6·10⁻⁴) |
| ol_n1_ralentit, `speech_text.fr` | « les compteurs: كنحسبو بيهم les crêtes » → « les compteurs, qui comptent les crêtes » | Darija dans la voix française |
| ol_n3_resserre, réactions q0 et q1 (écrit + voix) | λ = v/f, f constante → λ = v/ν, ν constante | Notation de la fiche (ν) |
| ol_r4_spectre, réaction e0s1.1.1 (voix) | « la longueur d'onde dans le vide change avec le milieu » → « la longueur d'onde change avec le milieu » | Erreur : c'est λ dans le milieu qui change, λ₀ ne change pas |
| ol_p2_violet, `visual.alt` | « Le rayon rouge et son angle de déviation… » → « Le rayon rouge, le moins dévié, puis le rayon violet, le plus dévié » | Mot-clé « angle de déviation » retiré de la fiche |
| ol_x2_national_2023, réaction e1.1.1 (écrit + voix) | « en divisant / tu as divisé par n » → « en multipliant c par n » | 4,5·10⁸ m/s vient de c × n, pas d'une division |
| ol_x3_national_2021, réaction e0.0.juste (écrit + voix) | d = λL/a (avec a) → d = 2λD₁/L₁ = 2 × 6·10⁻⁷ × 2 / 3·10⁻² = 8·10⁻⁵ m | Formule et données fausses |
| ol_x3_national_2021, réaction e0.1.1 (écrit + voix) | L = λD/a, « vérifie le sens de la division » → L = 2λD/a, « oubli du facteur 2 » | 4·10⁻⁵ m = oubli du facteur 2 ; relation sans le 2 fausse |
| ol_x3_national_2021, réaction e0.1.2 (écrit + voix) | d = λD₁/L₁ = 600 nm × 2 / 0,03 = 8·10⁻⁵ m → d = 2λD₁/L₁ = 8·10⁻⁵ m, « oubli du facteur 2 » | Calcul faux (λD₁/L₁ = 4·10⁻⁵ m) |
| ol_x3_national_2021, réaction e0.2.1 (écrit) | « d = λ·D/L » → « d = 2λD₁/L₁ » | Formule fausse |
| ol_x3_national_2021, réaction e0.2.2 (écrit + voix) | λ = aL/D ; d = λD₁/L₁ = (6·10⁻⁷ × 2)/(3·10⁻²) = 8·10⁻⁵ → λ = aL/(2D) ; d = 2λD₁/L₁ = (2 × 6·10⁻⁷ × 2)/(3·10⁻²) | Formule et calcul faux |
| ol_x4_national_2025, réaction q2.2 (écrit + voix) | visible « 400 nm à 700 nm » → « 400 nm à 800 nm » | Contredit le cours et la fiche |
| C1_r3, réaction 1.2 (écrit + voix) | « (principe de Babinet) » → retiré | Hors cadre |
| C3_r3, réaction 0.2 (voix) | « θ est la moitié de l'écart angulaire » → « θ va du centre de la tache jusqu'au bord » | θ EST l'écart angulaire |
| Séance 3, bloc ol_s3_b1, réaction 2.1 (voix) | « cent cinquante nanomètres » → « six cent cinquante nanomètres » | Valeur fausse (λ₁ = 650 nm) |
| Simulation prisme-angles.html | fichier supprimé | Simulation entière des relations du prisme (sin i = n·sin r, A = r + r', D = i + i' − A), aucune diapositive ne l'utilise |
| Simulation prisme-dispersion.html, texte du protocole | « Réfraction aux deux faces : sin i = n·sin r, sin i' = n·sin r' » → retiré | Relations du prisme |
| Simulation prisme-dispersion.html, description (ceQuiSeVoit) | « déviation D (≈ …° pour 700/400 nm) », « dévié (D ≈ …°) » → qualitatif (le moins dévié / le plus dévié) | Angle de déviation calculé |
| Simulation prisme-dispersion.html, dessin | lettre « D » sur l'arc de déviation → retirée (l'arc reste) | Angle de déviation D du prisme (et D = distance fente – écran dans ce chapitre) |
| Simulation prisme-dispersion.html, commentaires du code | formules du prisme → « calcul interne du dessin, jamais affiché » | Aucune trace (texte non affiché) |
| Simulations bilan.html et carte.html, schéma de commande | « C1..C9 » → « C1..C8 » | Trace de C9 |
| Simulation figures.html, commentaire | « sin i = n·sin r » → « calcul interne non affiché » | Aucune trace (non affiché) |

Voix à refaire : ol_n1_ralentit (speech_text.fr) ; ol_l1_metre (reponses_fin_de_cours.e0.0.1.parole) ; ol_g1_points (concentration.reponses.q.0.1.parole) ; ol_g5_autres (concentration.reponses.q.1.2.parole, q.2.2.parole) ; ol_n3_resserre (concentration.reponses.q.0.1.parole, q.1.1.parole) ; ol_r4_spectre (concentration.reponses.e0s1.1.1.parole) ; ol_x2_national_2023 (reponses_fin_de_cours.e1.1.1.parole) ; ol_x3_national_2021 (reponses_fin_de_cours.e0.0.juste.parole, e0.1.1.parole, e0.1.2.parole, e0.2.2.parole) ; ol_x4_national_2025 (concentration.reponses.q.2.2.parole) ; rappel C1_r3 (reponses.1.2.parole) ; rappel C3_r3 (reponses.0.2.parole) ; séance ol_s3, bloc ol_s3_b1 (exercice.reponses.2.1.parole). Aucun `speech_text.mixed` modifié : les `mot` des pointages restent valides ; chemins audio inchangés.

Signalé sans correction (organisation, doutes) :
- ol_c5_cuve (partie IV) utilise n = L/L' avant que l'indice soit défini (partie VII) ; la diapo l'annonce (« la raison viendra plus tard ») et ol_n5 y revient. Acceptable, mais reconstruire l'ordre serait plus propre.
- ol_l8 utilise le spectre visible 400–800 nm avant la partie VI ; c'est expliqué sur place.
- Les `speech_text.fr` de ol_l7, ol_r3, ol_c3, ol_c4, ol_c5, ol_g3, ol_g4, ol_n5 se terminent par une question de calcul que la diapo ne pose pas (la voix mixed ne la pose pas non plus). Rien n'est faux, mais il y a une incohérence entre fr et mixed.
- ol_t4_relation (voix) : « la seule relation de ce chapitre qu'on écrit sans démonstration ». C'est discutable : n = c/v et λ₀ = c/ν sont aussi admises comme définitions. Laissé tel quel.
- Ex. 2025 R : v = c/n ≈ 2,26·10⁸ m/s avec n = 1,33 arrondi (2,25·10⁸ avec n = 4/3). Cohérent avec l'énoncé, gardé.
- Réactions ol_x4 e0.2.1 / e0.2.2 (voix) : on dit « des franges » pour les taches de diffraction. Ce n'est pas faux, mais c'est du vocabulaire d'interférences : à remplacer par « taches » lors de la prochaine génération des voix.
- `backend/data/curriculum/exploration/ondes_lumineuses.json` (hors de mon périmètre) cite encore prisme-angles.html.
- Valeurs du national 2021 N (v rouge = 1,85·10⁸ ; v jaune = 1,81·10⁸ m/s) et 2023 R non vérifiables sur l'énoncé original ; les calculs qui en découlent sont justes.
- Tous les autres calculs ont été refaits et sont justes : θ = 6,5·10⁻³ rad, λ = 650 nm, a = 60 µm, λ₀R = 730 nm, λ = 387 nm, λ = 600 nm (2021 N), d = 80 µm, 532/1,33 = 400 nm, k = 2,6·10⁻⁶ m², rappels et séances. Les QCM et les vrai/faux ont des `correct` justes.

### phys_ch4_radioactivite — Décroissance radioactive
Notions officielles couvertes : composition du noyau, isotope, diagramme N/Z, radioactivités α, β⁻, β⁺, désexcitation γ, famille radioactive, loi de décroissance, constante radioactive λ et constante de temps τ, demi-vie, activité, datation (annexe 3 : carbone 14, rapport fils/père d'une roche) ; compétences → capacités : C1 → RA1, C2 → RA2, C3 → RA3, C4 → RA4 (+ RA2), C5 → RA5, C6 → RA6 + RA9, C7 → RA7 + RA9, C8 → RA8 + RA9, C9 → RA10. Toutes les parties, compétences et diapositives relèvent d'une capacité de la fiche `radioactivite` ; aucune partie hors programme.

Tous les calculs ont été refaits avec Python et sont justes : λ(Po 210) = 5,8·10⁻⁸ s⁻¹ ; N₀(I 131, 2022 N) = 4,0·10¹² ; N₀(Pu 238, 2021 N) = 4,0·10²⁰ et t(30 %) = 45 ans ; âge du bois (2022 R) = 2,26·10³ ans ; t½(P 32) = 14,3 j ; t(95 %, I 131) = 34,6 j (et 0,59 j pour l'option piège) ; N₀(Cd 107) = 4,5·10¹⁶ et N₀/8 = 5,6·10¹⁵ ; tritium 4,0·10¹⁷ ; 1 g d'iode 131 = 4,6·10²¹ ; τ = 11,5 j ; λ(C 14) = 1,21·10⁻⁴ an⁻¹ = 3,8·10⁻¹² s⁻¹ ; λ(I 131) = 1,0·10⁻⁶ s⁻¹ ; 8 % par jour pour l'iode ; familles U 238 (8 α, 6 β⁻), Th 232 (6 α, 4 β⁻), Ra 226 (5 α, 4 β⁻). Toutes les bonnes réponses des QCM et des vrai/faux sont justes.

Nombre de corrections : 31 (28 dans le JSON du cours, 3 dans les simulations)

| Diapositive / élément | Avant → après | Raison |
|---|---|---|
| ra_x4_2025N, réaction e0s2.0.juste (ecrit + parole) | « avec émission d'un positon et d'un neutrino » → « avec émission d'un positon » | Le neutrino est hors programme |
| ra_x4_2025N, réaction e0s2.1.2 (ecrit + parole) | « (avec émission d'un positon et d'un neutrino) » / « positon و neutrino » → sans neutrino | Le neutrino est hors programme |
| ra_x3_2022N, réaction e0.2.2.ecrit | « ¹³¹₅₃I → ¹³¹₅₄Xe + ⁰₋₁e + antineutrino » → « … + ⁰₋₁e » | L'antineutrino est hors programme |
| C4_r3 (rappel γ), réactions 0.1, 0.2, juste (ecrit) | « Le photon γ n'a ni charge ni masse » → « Le rayonnement γ (onde électromagnétique) ne porte ni charge ni nucléon » | « photon » est hors de ce chapitre ; la fiche dit « rayonnement γ » |
| C4_r3, réaction 0.2.parole | « الفوطون gamma » (photon) → « le rayonnement gamma » | Même raison (le mot était écrit en arabe) |
| ra_x2_2021N, reponses_fin_de_cours e0.0.1.parole | « trente pour cent ديال la durée de vie ديال la source » → « trente pour cent ديال t un demi » | Faux : 26 ans, c'est 30 % de t½, pas d'une « durée de vie » (notion hors programme et ambiguë) |
| ra_a5_masse, réaction q.0.2 (ecrit + parole) | « tu as oublié n / tu as donné N_A seul » → « tu as gardé m = 2 g au lieu de convertir 2 µg en grammes » | Diagnostic faux : 4,0·10²³ = (2/3)·N_A vient de l'oubli de la conversion des µg |
| ra_a5_masse, réaction q.2.1 (ecrit + parole) | « Convertis 2 µg en grammes » → « as-tu bien divisé la masse par M = 3 g/mol ? » | Diagnostic faux : 1,2·10¹⁸ = 2·10⁻⁶ × N_A, c'est un oubli de la division par M |
| ra_a5_masse, réaction q.2.2 (ecrit + parole) | « vient d'une masse mal convertie » → « tu as multiplié m par N_A sans diviser par M » | Même erreur de diagnostic |
| ra_x4_2025N, réaction q.1.2.parole | « N₀/4, عدد les noyaux désintégrés قبل deux demi-vies » → « عدد les noyaux اللي بقاو ف deux demi-vies » | Faux : N₀/4 est le nombre de noyaux restants à 2t½ (l'écrit le disait bien) |
| ra_x4_2025N, réaction q.2.2.parole | « ٣٩ فالمية ديال les noyaux » (39 %) → « trois virgule neuf fois dix puissance seize » | Faux : 3,9·10¹⁶ est un nombre de noyaux, pas un pourcentage |
| ra_a2_definition, réaction q.2.1.ecrit | « proportionnelle au nombre de noyaux (A = λ·N) » → « L'activité suit le nombre de noyaux : moins de noyaux, moins de désintégrations par seconde. » | Notation A (réservée au nombre de nucléons ; la fiche écrit a) et relation pas encore vue (a = λ·N vient à la diapositive suivante) |
| ra_s5_b3, exercice, réactions 0.2, 1.1, 1.2, juste (ecrit) | « A = A0/4, A0/A, A/A₀ » → « a = a₀/4, a₀/a, a/a₀ » | Notation de la fiche : activité a minuscule (A est le nombre de nucléons) |
| ra_s5_b3, exercice, réaction 0.1 (ecrit) | « t_{1/2} » → « t½ » | Notation de la fiche |
| ra_s5_b3, exercice, réaction 1.2 (ecrit) | « Vous avez » → « Tu as » | Tutoiement, comme dans tout le cours |
| C4_r4, réaction 0.1.ecrit | « positron » → « positon » | Mot de la fiche |
| ra_s2_b1, exercice, réaction 2.1.ecrit | « pense-tu » → « penses-tu » | Faute d'orthographe |
| Simulation segre.html, vue famille2024 (textes, flèches, repères, description) | flèche (1) β⁻, flèche (2) α → flèche (1) α (Bi 212 → Tl 208), flèche (2) β⁻ (Bi 212 → Po 212) | La voix de ra_f3_famille2024 dit « flèche un : alpha, flèche deux : bêta moins », avec un pointage sur fleche_1 puis fleche_2 : la simulation montrait l'inverse au même moment. Seuls les numéros changent, les flèches et les équations restent les mêmes. |
| Simulation desintegration.html, explication gamma | « un rayonnement γ, une onde lumineuse invisible » → « un rayonnement γ, une onde électromagnétique » | Inexact ; la fiche dit « onde électromagnétique » |

Voix à refaire (champs `parole` des réactions préparées, texte déjà corrigé dans le JSON) :
- ra_a5_masse (concentration.reponses.q.0.2.parole)
- ra_a5_masse (concentration.reponses.q.2.1.parole)
- ra_a5_masse (concentration.reponses.q.2.2.parole)
- ra_x4_2025N (concentration.reponses.q.1.2.parole)
- ra_x4_2025N (concentration.reponses.q.2.2.parole)
- ra_x4_2025N (concentration.reponses.e0s2.0.juste.parole)
- ra_x4_2025N (concentration.reponses.e0s2.1.2.parole)
- ra_x2_2021N (reponses_fin_de_cours.e0.0.1.parole)
- C4_r3, rappel de la compétence C4 (competences[C4].rappels[2].reponses.0.2.parole)

Aucun `speech_text` de diapositive n'a été modifié : les pointages restent valables.

Signalé sans correction (organisation, doutes) :
- ra_t4_pourcentages (séance 4) affiche « Puis t = (1/λ)·ln(N₀/N) » alors que cette relation n'est établie qu'à ra_c2_demo (séance 5). Elle se déduit vite de la loi et de ln (déjà vus), mais il vaudrait mieux la montrer ici ou retirer la puce.
- C3_r2 (rappel sur les lois de Soddy), réaction 0.2 : l'écrit dit « La masse n'est pas conservée dans une réaction nucléaire » et la voix ajoute « il y a une perte de masse, on le verra plus tard ». C'est vrai et annoncé, mais c'est la notion du chapitre suivant (défaut de masse). On pourrait dire seulement « les lois de Soddy ne portent pas sur la masse ». Non corrigé, pour ne pas refaire la voix.
- C4_r3, réaction 0.1.parole : « la particule gamma » (le cours dit « rayonnement γ »), et C4_r4, réaction 0.1.parole : « positron » (au lieu de « positon »). Ce sont des écarts de vocabulaire, pas des erreurs : laissés en l'état.
- segre.html, vue zones : « les noyaux lourds, au-delà du plomb, sont émetteurs α ». La fiche demande « noyaux lourds, sans seuil chiffré ». Le plomb n'est pas un chiffre : gardé.
- Numérotation des flèches du national 2024 R : l'exploration ne donne pas l'ordre de l'énoncé original. J'ai aligné la simulation sur la voix ; à vérifier sur le sujet si on veut respecter sa numérotation (il faudrait alors refaire la voix de ra_f3_famille2024).

### phys_ch5_energie_nucleaire — Noyaux, masse et énergie
Notions officielles couvertes : Noyaux - Masse et énergie (défaut de masse, énergie de liaison, fission, fusion, bilan énergétique), en entier ; compétences → capacités : C1 → EN1, C2 → EN2, C3 → EN3, C4 → EN4, C5 → EN5, C6 → EN6, C7 → EN7, C8 → EN8, C9 → EN3, EN4, EN6, EN7 (méthode du barème et bilan). Chaque diapositive relève d'une capacité. Il n'y a pas de partie hors cadre. Aucun terme de `hors_cadre` ni des `termes_hors_programme` n'apparaît, ni dans le cours ni dans les simulations : pas de photon, de E = hν, d'interaction forte, de modérateur, de masse critique, d'exo/endothermique ni de neutrino. Tous les calculs ont été refaits en Python. Ils sont justes et conformes aux corrigés des nationaux 2016 N, 2017 R, 2019 N, 2020 N, 2022 N, 2022 R, 2023 N et 2025 N : Δm et E_ℓ de He-4, C-14, C-12, Ni-60, Fe-56 et U-235 ; énergies libérées de la fusion (17,6 MeV), de la fission (184,8 MeV), de Co-60 (2,82 MeV), I-131 (0,46 MeV), Cd-107 (0,402 MeV), Rn-222 (6,24 MeV) et Po-210 (5,4 MeV) ; diagrammes ; conversions u/MeV/J ; 1 g d'U-235 ; comparaison fission/fusion. Les bonnes réponses (`correct`) des QCM et des vrai/faux sont toutes justes.
Nombre de corrections : 27 (champs modifiés)
| Diapositive / élément | Avant → après | Raison |
|---|---|---|
| en_d4_carbone : speech_text.fr, speech_text.mixed, question.demonstration.parole, reponses q.0.2, q.1.juste, q.2.2, e0s0.0.2, e0s0.1.juste (parole) — 8 champs | « treize virgule neuf mille neuf cent quatre-vingt-quinze » → « treize virgule quatre-vingt-dix-neuf mille neuf cent quatre-vingt-quinze » | La voix disait 13,9995 au lieu de 13,99995 u (masse du C-14, national 2022 R) |
| en_d4_carbone reponses e0s0.0.2 (ecrit) | « m(noyau) = 13,9995 u » → « 13,99995 u » | Même faute de frappe |
| en_m4_931 speech_text.fr et .mixed | « On divise par un virgule six fois dix puissance moins treize » → « un virgule six zéro deux fois… » | 1,4924·10⁻¹⁰ / 1,6·10⁻¹³ = 933, pas 931,5. L'écran utilise bien 1,60218·10⁻¹³ |
| en_m4_931 exercises[0].enonce_dit | « L'énergie de liaison du noyau d'hélium quatre vaut… » → « Une énergie vaut… » | L'énergie de liaison n'est enseignée qu'en C3. L'écrit de la question disait déjà « Une énergie vaut 28,30 MeV » |
| séance en_s1, bloc en_s1_b1b, exercice (prompt + enonce_dit) | « L'énergie de liaison du noyau d'hélium 4 vaut 28,30 MeV » → « Une énergie vaut 28,30 MeV » | Même raison : ce bloc de la séance 1 précède la séance 2, où l'énergie de liaison est enseignée |
| en_l4_par_nucleon reponses_fin_de_cours e0.1.2 (ecrit + parole) | « Δm ≈ 0,5658 u » / « zéro virgule cinq six cinq huit » → « 0,56553 u » / « zéro virgule cinq six cinq cinq trois » | Valeur fausse : 28 × 1,00728 + 32 × 1,00866 − 59,91543 = 0,56553 u |
| en_a3_comparer reponses e0s2.1.2 (ecrit + parole) | « environ 8,76 MeV » → « environ 8,79 MeV/nucléon » | Le cours (et la fiche) donne 8,79 pour Fe-56 |
| en_e4_polonium reponses q.2.1 (ecrit + parole) | « le nombre que tu donnes est l'énergie de liaison du polonium » → « 1650,2 MeV est l'écart entre les nucléons séparés et les produits, E_ℓ(Pb) + E_ℓ(He) » | Faux : E_ℓ(Po) = 1644,8 MeV. 1650,2 = 1,971820·10⁵ − 1,955318·10⁵ (la simulation diagramme.html le dit aussi) |
| en_e4_polonium reponses q.2.2 (ecrit + parole) | « c'est un autre niveau du diagramme » / « l'énergie de liaison du polonium » → « l'écart nucléons séparés → produits, E_ℓ(Pb) + E_ℓ(He) » | Même erreur |
| en_n3_2025 reponses q.2.2 (ecrit + parole) | « dix fois trop grande environ » / « tu as multiplié… » → « vient d'une division (5,62·10¹⁵ / 0,402) : il faut multiplier » | 1,40·10¹⁶ / 2,26·10¹⁵ ≈ 6, pas 10. Cette valeur vient en fait d'une division |
| en_n3_2025 reponses e0.1.2 (ecrit) | « 7,5·10⁴² vient d'une erreur sur le signe de l'exposant » → « a un exposant faux : 23 + (−13) = 10 » | Une erreur de signe donnerait 10³⁶, pas 10⁴² |
| C8_r2 options[2] + reponses 2.2 (ecrit) | « 9,3·10¹⁹ MeV » / « 185 / 2·10²¹ ≠ 9,3·10¹⁹ » → « 9,3·10⁻²⁰ MeV » / « 185 / 2·10²¹ = 9,3·10⁻²⁰ MeV » | Ce distracteur doit être l'erreur « division », comme le disent les réactions. 185 / 2·10²¹ = 9,25·10⁻²⁰ |

Simulations (energie-nucleaire-tableau/) : tous les textes et valeurs affichés ont été vérifiés (balance, liaison, aston, diagramme, comparaison, figures, bilan, carte, rappels). Il n'y a ni erreur ni terme hors programme. Aucune modification.

Voix à refaire : en_d4_carbone (speech_text.fr, speech_text.mixed, question.demonstration.parole, reponses q.0.2 parole, q.1.juste parole, q.2.2 parole, e0s0.0.2 parole, e0s0.1.juste parole) ; en_m4_931 (speech_text.fr, speech_text.mixed, exercises[0].enonce_dit) ; en_s1_b1b (exercice.enonce_dit) ; en_l4_par_nucleon (reponses_fin_de_cours e0.1.2 parole) ; en_a3_comparer (reponses e0s2.1.2 parole) ; en_e4_polonium (reponses q.2.1 parole, q.2.2 parole) ; en_n3_2025 (reponses q.2.2 parole). Les mots de pointage (`mot`) de en_m4_931 et en_d4_carbone restent des extraits exacts de la voix.

Signalé sans correction (organisation, doutes) :
- en_e4_polonium e0 et bloc en_s3_b3 : l'énoncé est présenté comme « National 2020 N » avec 1 u = 931,5 MeV/c², alors que le sujet donne 931,41. Le résultat (2,93·10⁻²⁷ kg) ne change pas. Cela contredit pourtant la règle du cours « prendre la valeur de 1 u de l'énoncé du jour » (en_n3_2025). Pour corriger, il faudrait refaire plusieurs voix.
- ²H : le cours utilise E_ℓ = 2,366 MeV, la donnée du national 2023 (1,183 MeV/nucléon). La simulation liaison.html affiche 2,23 MeV, et la fiche donne 1,11 MeV/nucléon (valeur réelle). Ce sont deux valeurs différentes dans le même cours, toutes deux légitimes : à harmoniser éventuellement en disant « valeur de l'énoncé 2023 ».
- en_n3_2025 e0 / en_s4_b1 : l'explanation écrit « 4,7·10²³ × 1,6·10⁻¹³ = 7,6·10¹⁰ J ». Le calcul strict donne 7,52·10¹⁰ J ; 7,6 vient de la valeur non arrondie 4,74·10²³. Les réactions le précisent déjà.
- en_s1_stabilite dit « pour le nickel soixante, on a calculé 8,78 ». Ce calcul n'est fait que dans l'exercice de fin de cours de en_l4_par_nucleon, que l'élève n'a pas forcément fait.
- Organisation : l'ordre est logique, les prérequis (énergie, puissances de dix, charges) sont rappelés juste avant d'être utilisés, et chaque compétence a 3 ou 4 rappels plus questions et exercices. Le bilan (8 blocs) et la carte correspondent aux compétences C1 à C8.

### phys_ch6_dipole_RC — Dipôle RC
Notions officielles couvertes : Dipôle RC (charge, décharge, équation différentielle, constante de temps, énergie emmagasinée), en entier ; compétences → capacités : C1 → RC1, RC2 ; C2 → RC3 ; C3 → RC4 ; C4 → RC5 ; C5 → RC6 ; C6 → RC7 ; C7 → RC8 ; C8 → RC9. Toutes les diapositives relèvent d'une de ces capacités ; chaque compétence est travaillée puis évaluée (questions, exercices, 3 ou 4 rappels chacune) ; le bilan (rc_b1, rc_b2) reprend les 8 compétences. Rien de hors cadre trouvé (filtre, sinusoïdal, impédance, Laplace, séparation des variables, permittivité, C = εS/e, second ordre…), ni dans le cours ni dans les simulations. Tous les calculs ont été refaits avec Python (τ, 63 %/37 %, 4,44 mA, énergies, C_eq, C = I₀/k, pente −83,3 s⁻¹, R₁, C…) : ils sont justes. Les données des nationaux ont été comparées aux sujets du dépôt (backend/data/exams/physique/, figures lues) : 2017 R, 2018 N, 2019 N, 2021 N, 2021 R, 2022 N et 2025 N sont exactes ; 2023 R et 2024 R ne l'étaient pas (voir ci-dessous).
Nombre de corrections : 18
| Diapositive / élément | Avant → après | Raison |
|---|---|---|
| rc_l4_deduire, exercice de fin 2 (prompt) | « 2024 R : u_R(t) décroît depuis u_R(0) = 5 V ; … 5 ms … » → « Charge : u_R(t) décroît depuis u_R(0) = 5 V ; … 5 ms … » | Fausse attribution : dans le vrai 2024 R, l'axe est en µs (τ = 5 µs) et le sujet demande de vérifier C = 0,10 µF. Le cours disait même « pas 0,10 µF ». Les valeurs (5 ms, 100 µF) restent justes comme exercice d'entraînement. |
| rc_l4_deduire, exercice de fin 2 (enonce_dit) | « deux mille vingt-quatre, session normale. La tension … » → « pendant la charge, la tension … » | Même raison (et c'était un rattrapage, pas une session normale). |
| rc_e8_national, exercises[0] (prompt) | « Suite (2023 R) : au régime permanent, q = Q_max = 12 µC … » → « Au régime permanent de la charge, q = Q_max = 12 µC … » | Dans le vrai 2023 R, la figure 2 donne q_max = 120 µC (E = 12 V, E_e = 0,72 mJ). On retire l'attribution, les valeurs 12 µC / 1,2 V restent justes. |
| rc_e8_national, exercises[0] (enonce_dit) | « Suite de l'exercice de la session de rattrapage deux mille vingt-trois. Au régime permanent, … » → « Au régime permanent de la charge, … » | Même raison. |
| Séance 3, bloc rc_s2_b3, exercice (prompt + enonce_dit) | « Suite (2023 R) … » / « suite de l'exercice de la session de rattrapage deux mille vingt-trois … » → « Au régime permanent de la charge, … » | Même raison (copie de l'exercice d'e8). |
| rc_l8_calcul, exercice de fin 2 (prompt) | « 2023 R : on garde Q_max = 12 µC … » → « On garde Q_max = 12 µC … » | Même raison. |
| rc_l8_calcul, exercice de fin 2 (explanation) | « … le même résultat qu'avec ½·C·E² (le corrigé qui écrit 0,72 mJ se trompe). » → « … le même résultat qu'avec ½·C·E². » | Faux : avec la vraie valeur q_max = 120 µC, 0,72 mJ est juste. |
| rc_l3_descente, réaction e1/0/juste (parole + écrit) | « i كتهبط، يعني هادي décharge » / « Le courant décroît (décharge) » → « i كتهبط، واخا حنا ف la charge » / « Le courant décroît (même pendant la charge) » | La courbe i(t) de 2021 R est une charge (condensateur déchargé, E = 6 V). Le cours lui-même enseigne que i décroît pendant la charge. |
| rc_l3_descente, réaction e1/1/1 (parole, 2 phrases + écrit) | « هادي la décharge، ماشي الشحن … كتخص تكون فالطلوع، يعني la charge » / « (décharge) » → « i كتنقص من cinquante milliampères نحو zéro … كتخص courbe كتطلع، بحال u C » / « (pendant la charge, i diminue) » | Même raison (la réaction disait que 63 % = la charge, ce qui laissait croire que i monte en charge). |
| rc_l3_descente, réaction e1/2/2 (écrit) | « Pendant la décharge, à t = τ » → « Pour cette courbe qui descend, à t = τ » | Même raison. |
| rc_s5_verifier, réaction e0/2/2 (parole + écrit) | « E/R … c'est la valeur initiale de i » → « c'est la valeur absolue de i à t = 0 (en décharge i(0) = −E/R) » | L'exercice porte sur la décharge : i(0) = −E/R. |
| Rappel C1_r3, réaction 0/2 (écrit) | « une armature en accumule (q_A = q), l'autre en perd (q_B = −q) » → « une armature en perd (q_A = q), l'autre en accumule (q_B = −q) » | Signe inversé : l'armature qui gagne des électrons porte −q (cf. rc_c3_electrons). |
| Simulation figures.html, vue fig_energie_2023R (11 textes) | « Q_max = 12 µC ; E = 1,2 V ; E_e = 7,2·10⁻⁶ J » → « Q_max = 120 µC ; E = 12 V ; E_e = ½ × 10⁻⁵ × 12² = 7,2·10⁻⁴ J » (et q²/(2C) = (120·10⁻⁶)²/(2 × 10⁻⁵)) | La vue s'intitule « national 2023 R » : valeurs du vrai sujet (figure 2). Cette vue n'est utilisée par aucune diapositive. |
Voix à refaire : rc_l4_deduire (exercices_fin_de_cours[1].enonce_dit) ; rc_e8_national (exercises[0].enonce_dit) ; séance rc_s3, bloc rc_s2_b3 (exercice.enonce_dit) ; rc_l3_descente (reponses_fin_de_cours.e1.0.juste.parole) ; rc_l3_descente (reponses_fin_de_cours.e1.1.1.parole) ; rc_s5_verifier (reponses_fin_de_cours.e0.2.2.parole)
Signalé sans correction (organisation, doutes) :
- 2023 R et 2024 R : j'ai retiré l'attribution plutôt que réécrire les exercices (les réactions vocales reposent toutes sur 12 µC / 1,2 V et 5 ms / 100 µF). Si on veut un exercice fidèle au sujet : 2023 R → Q_max = 120 µC, C = 10 µF, E = 12 V, E_e = 7,2·10⁻⁴ J = 0,72 mJ ; 2024 R → u_R(0) = 5 V, τ = 5 µs, R = 50 Ω, C = 0,10 µF. L'exploration (backend/data/curriculum/exploration/dipole_RC.json) dit à tort que les corrigés de ces deux sujets se trompent ; c'est le transcrit (exam.json 2023 R « q_max = 12 µC ») qui est faux.
- rc_s7_q_i : la voix s'arrête sur « u C monte, on est d'accord. » ; i(t) = (E/R)·e^(−t/τ) et i(0) = 12 mA sont à l'écran et au cahier sans être dérivés à voix haute (le rappel C5_r3 le demande ensuite).
- rc_s6_tableau, rc_l2_pourcent : u_C(τ) = 0,63 × 12 = 7,56 V (avec e⁻¹ exact : 7,59 V). Cohérent avec la fiche (0,63) ; pas changé.
- rc_l3_descente, réaction q/2/2 : « Les 50 % correspondent au temps de demi-vie » — notion de la radioactivité, pas du RC ; pas faux, mais à reformuler à la prochaine génération de voix.
- rc_c6_relation (réactions q.2.x) : parle de i = E/R « au premier instant » avant que la réponse à un échelon soit vue (rc_m4) ; prérequis un peu anticipé.
- rc_b2_carte : « le dipôle RL (τ = L/R) » est toléré par la fiche (annonce), mais le chapitre RL écrit τ = L/(R + r).
- Rappel C7_r1 : la valeur initiale de décharge s'écrit U₀ alors que tout le cours écrit E.

### phys_ch7_dipole_RL — Dipôle RL
Notions officielles couvertes : Dipôle RL (inductance, équation différentielle, retard à l'établissement du courant, énergie magnétique), TP « tension aux bornes d'une bobine » ; compétences → capacités : C1 → RL1, C2 → RL2, C3 → RL3, C4 → RL4, C5 → RL5, C6 → RL6, C7 → RL7, C8 → RL8 (chaque partie I à X relève d'une de ces capacités ; aucune partie hors cadre).
Nombre de corrections : 14
| Diapositive / élément | Avant → après | Raison |
|---|---|---|
| Séance 1, bloc rl_s1_b1, exercice, réaction juste (ecrit) | « La bobine s'oppose à l'établissement du courant (loi de Lenz) » → « La bobine s'oppose à l'établissement du courant » | Loi de Lenz hors cadre (fiche `hors_cadre`, périmètre). |
| C2_r2 (rappel vrai/faux) : prompt, enonce_dit, ecrit des réactions 0.2 et 1.juste | « Une bobine diminue la valeur finale du courant. » (Faux) → « L'inductance L d'une bobine diminue la valeur finale du courant. » (Faux) ; réactions : « I₀ = E/(R + r) ne contient pas L » | L'ancien énoncé est le motif interdit de la fiche (« bobine diminue le courant final ») et il est discutable : une bobine réelle de résistance r abaisse bien I₀ = E/(R + r). Seule L n'agit pas. |
| rl_bl_fiche, puce 7 (écran) | « une diode en parallèle sur la bobine évite la surtension » → « une diode (en série avec R₁) en parallèle sur la bobine évite l'étincelle : u_b = −R₁·I₀ » | Contradiction avec rl_t4 (2025 R) : avec la diode, il reste une surtension u_b = −100 V. |
| rl_s8_R, exercice fin de cours 2, explanation | « 2,4 ms vient de L/R en oubliant r » → « 2,4 ms = 0,12/50 : l'ancienne valeur de R, et r oublié » | Avec R = 20 Ω, L/R = 6 ms, pas 2,4 ms. |
| rl_s8_R, même exercice, réaction juste (ecrit + parole) | ecrit « (et non 1,7 ms) » supprimé ; voix « R plus r = soixante-dix… une virgule sept milliseconde… plus petite » → « trente ohms… quatre millisecondes… plus grande » | Calcul faux dans la voix : R + r = 30 Ω, τ = 0,12/30 = 4 ms. |
| rl_e8_2019R, vrai/faux « I₀ = 8/40 = 0,2 A », réaction 2e essai sur « Faux » (ecrit + parole) | « Verdict : la réponse « Faux » est conforme à la clé imposée… » → « Faux : la bonne réponse est Vrai. I₀ = U_R/R = 0,2 A = E/(R + r) » | Texte de réaction faux (l'affirmation est vraie) et texte parasite (« clé imposée »). |
| rl_b10_national, vrai/faux « E = u_R + u_L = 10 V », réaction 2e essai (ecrit + parole) | « Faux… L'énoncé de l'affirmation est donc incorrect » / voix « الجواب هو Faux… E ماشي égale u R زائد u L » → « Faux : la bonne réponse est Vrai… E = 9 + 1 = 10 V » | L'affirmation est vraie (correct = true). La réaction disait le contraire. |
| rl_t4_national, vrai/faux « second membre = E », réaction 2e essai (ecrit + parole) | « L di/dt + (R + R1) i = 0 » / voix « la charge » → « maille bobine, diode, R₁ : L·di/dt + R₁·i = 0 » ; « l'établissement du courant » | R n'est pas dans la maille bobine, diode et R₁ (bobine idéale). « Charge » est un mot du RC. |
| rl_t4_national, exercice I₀ et L, indice option A (ecrit + parole) | « après l'ouverture, regarde quelle résistance totale voit la bobine (avec la diode)… τ = L/R_totale » → « τ = 1 ms est lu pendant l'établissement : τ = L/R » | L'indice menait à une méthode fausse : τ est lu avant l'ouverture, avec R = 100 Ω. |
| rl_t4_national, même exercice, réaction juste (ecrit + parole) | « τ = L/R₁ avec R₁ = 1000 Ω, donc L = 1×10⁻³ × 1000 = 0,1 H » → « τ = L/R donne L = 10⁻³ × 100 = 0,1 H » | Relation fausse, et calcul faux (10⁻³ × 1000 = 1 H). |
| rl_l8_double, exercice 2016 R, indice option C (ecrit + parole) | ecrit « Je n'ai que ton retour, sans l'énoncé… Envoie-moi les données… » ; voix sur l'erreur « u_R pris pour i » → indice sur le facteur ½ et le carré (i = 0,1 A juste) | Texte parasite affiché à l'élève. La voix ne correspondait pas à l'option C (1,44·10⁻² J = L·i : ni ½ ni carré). |
| rl_n1_2022R, vrai/faux « doubler L ne change pas u_R final », réaction 2e essai (ecrit + parole) | « la bobine se comporte comme un fil » → « comme une résistance r » | Bobine de 2022 R : r = 10 Ω, ce n'est pas un fil. |
| rl_n1_2022R, exercice équation en u_R, indice option C (ecrit) | « correspond à une décharge sans générateur » → « ressemble à une rupture du courant, sans générateur » | « Décharge » est un mot du RC. |
| rl_l6_ub, exercice 2018 R, réaction 2e essai option B (parole) | « كتخص la charge، ماشي la décharge » → « كتخص la courbe اللي كتطلع، ماشي اللي كتهبط » | Mots du condensateur dans le chapitre RL (l'ecrit était juste). |

Calculs refaits avec Python (tous justes sauf ceux corrigés ci-dessus) : τ = 0,12/60 = 2 ms ; I₀ = 6/60 = 0,1 A ; 2016 R A = 12/48 = 0,25 A, τ = 0,144/48 = 3 ms ; 2019 R r = 40 × (10/8 − 1) = 10 Ω ; 2020 N r = 1/0,1 = 10 Ω ; 2021 R r = 6/0,06 − 95 = 5 Ω, L = 5,1·10⁻³ × 100 = 0,51 H ; 2022 R I₀ = 0,02 A, r = 10 Ω, L₀ = 0,5 H, 0,63 × 9,8 ≈ 6,2 V ; 2023 N R = 500 Ω, L = 1 H ; 2024 N L = 2 mH, τ = 2 µs, R₁ + r = 1 kΩ ; 2025 R I₀ = 0,1 A, L = 0,1 H, u_b = −100 V ; énergies : 6·10⁻⁴ J, 5·10⁻⁴ J, 7,2·10⁻⁴ J, 1,22·10⁻⁴ J (2017 N), 0,025 J → 0,1 J (× 4), 0,05 J (L double) ; rappels, triangle (L = 0,02 H), segments (u_b = 2 V, 1 V, 7 V), tous les distracteurs. Bonnes réponses des QCM et des vrai/faux vérifiées. Simulations du dossier dipole-rl-tableau relues (textes affichés, valeurs, figures des nationaux) : rien de faux ni hors cadre, aucune modification.

Voix à refaire : C2_r2 (enonce_dit) ; rl_s8_R (reponses_fin_de_cours.e1.1.juste.parole) ; rl_e8_2019R (reponses_fin_de_cours.e1s1.1.2.parole) ; rl_b10_national (reponses_fin_de_cours.e1s2.1.2.parole) ; rl_t4_national (reponses_fin_de_cours.e1s2.0.2.parole) ; rl_t4_national (concentration.reponses.e0.0.1.parole) ; rl_t4_national (concentration.reponses.e0.2.juste.parole) ; rl_l8_double (concentration.reponses.e0.2.1.parole) ; rl_n1_2022R (reponses_fin_de_cours.e2s2.1.2.parole) ; rl_l6_ub (reponses_fin_de_cours.e1.1.2.parole). Les chemins audio n'ont pas été touchés.

Signalé sans correction (organisation, doutes) :
- Sujet 2016 R présenté de deux façons : rl_s4_A dit « un conducteur ohmique r = 8 Ω, bobine idéale », alors que l'exercice de la séance 2 (bloc rl_s2_b1 : explanation, réactions 0.2 et 1.2) parle de « la résistance r de la bobine », et que sa voix dit en même temps « la bobine se comporte comme un fil ». Les chiffres sont justes (I₀ = 0,25 A). Il faut choisir une version d'après le sujet original, puis harmoniser l'écrit et les voix.
- Séance 1, bloc rl_s1_b1 (exercice des deux lampes) : les réactions 0.2 et 1.2 citent τ = L/(R + r), et la réaction 1.1 cite u_b = L·di/dt + r·i. Ces notions ne sont enseignées qu'aux séances 2 et 3 (prérequis non vus). À simplifier quand ces voix seront refaites.
- Les phrases « la bobine retarde le courant, elle ne change pas sa valeur finale » (rl_m4_I0, rl_s7_L, réactions de rl_n1) parlent de L dans leur contexte : justes, mais à lire comme « L ne change pas I₀ ».
- Organisation correcte : prérequis (loi d'Ohm, additivité, dérivée, exponentielle) avant usage ; chaque compétence a 3 ou 4 rappels et au moins une question ou un exercice ; fiche et carte cohérentes avec C1 à C8. Le circuit RLC est seulement annoncé comme chapitre suivant (carte, bilan).

### phys_ch8_circuit_RLC — Oscillations libres d'un circuit RLC série
Notions officielles couvertes : Circuit RLC série (amortissement, régimes périodique / pseudo-périodique / apériodique, oscillations libres, entretien des oscillations) ; TP « Oscillations libres dans un circuit RLC série ». Compétences → capacités : C1 → RLC1, C2 → RLC2, C3 → RLC3, C4 → RLC4, C5 → RLC5, C6 → RLC6, C7 → RLC7, C8 → RLC8 (chaque compétence a 4 rappels et au moins une question ou un exercice).
Nombre de corrections : 23
| Diapositive / élément | Avant → après | Raison |
|---|---|---|
| lc_r2b_critique (diapositive entière) | « La frontière : le régime critique » → diapositive retirée ; retirée aussi de `competences[C2].slide_ids`, de `seances[1].blocs[0].slide_ids` et de son `cahier` (« Régime critique : la frontière… ») | Hors cadre (décision du 15/11 : trois régimes seulement) |
| lc_r2_aperiodique (visual.caption) | « R = 1 kΩ : … ; à 300 Ω, la frontière » → « R = 1 kΩ : u_C revient vers 0 sans osciller » | Idée du régime critique |
| lc_r4_national (exercices_fin_de_cours[0], énoncé 3 + enonce_dit) | « Le régime critique est la frontière entre… » (vrai) → « Avec une très grande résistance totale, u_C revient vers 0 sans osciller : c'est le régime apériodique. » (vrai) | Hors cadre |
| lc_r4_national (reponses_fin_de_cours.e1s2 : 0.juste, 1.1, 1.2, ecrit + parole) | réactions sur le régime critique → réactions sur le régime apériodique (expérience à 1 kΩ) | Suit le nouvel énoncé |
| Rappel C2_r1 (options) | 4e option « critique » + ses réactions → retirées (bonne réponse inchangée : index 2) | Hors cadre |
| Rappel C2_r1 (reponses 0.2) | « En apériodique ou critique, u_C revient… » → « En apériodique, u_C revient… » | Hors cadre |
| Rappel C2_r3 (options[1] + reponses 0.2, 1.juste, 2.2) | « apériodique (ou critique) » → « apériodique » | Hors cadre |
| Rappel C3_r4 (reponses 3.juste) | « l'équation d'un oscillateur harmonique » → « l'équation du circuit LC » | `hors_cadre` (oscillateur harmonique) |
| Rappel C8_r2 (reponses 0.2) | « oscillateur harmonique de période T₀ » → « l'équation du circuit LC, de période T₀ » | Idem |
| lc_k3_T0 (reponses_fin_de_cours.e2s2.1.juste.ecrit) | « la résistance négative du générateur doit compenser… » → « le générateur doit compenser… » | Entretien : u_G = k·i, sans « résistance négative » |
| lc_e8_T0 (reponses_fin_de_cours e0.0.1) | « l'as-tu converti en farads ? » → 1,6·10⁻⁵ est T₀² : la racine est oubliée | Diagnostic faux (la conversion était juste) |
| lc_e8_T0 (e0.2.1, e0.2.2) | « 6,3 هو deux pi بوحدو / نسيتي pi deux égale dix » → 6,3·10⁻⁴ s = √(LC) : 2π oublié | Affirmation fausse (Python : √(0,1×4·10⁻⁶) = 6,32·10⁻⁴ s) |
| lc_p4_national (concentration.reponses e0.0.1, e0.0.2) | pour 5 H : « l'erreur vient des unités » → « T₀ non élevée au carré : 10⁻²/(2·10⁻³) = 5 H » | Diagnostic contraire à l'`explanation` |
| lc_p4_national (reponses_fin_de_cours e1.1.1, e1.1.2) | pour 25 H : « unités / facteur 4 » → « T₀ non élevée au carré : 2,5·10⁻³/10⁻⁴ = 25 H » | Idem |
| lc_en2_depart (reponses_fin_de_cours e0.2.1, e0.2.2) | « 6 J = la tension de charge E » → « 6 J = q/(2C) : le carré de q est oublié » | Faux (ici u_C = 12 V ; q/(2C) = 6) |
| lc_a4_perdue (concentration.reponses e0.0.2) | « proche de E initiale seule » → « 2,8·10⁻¹⁰ J vient de (6 − 4,4)² » | Faux (E initiale = 3,96·10⁻⁹ J) |
| lc_l3_carre (reponses_fin_de_cours e0.0.2) | pour 50 H : « conversion oubliée » → « T₀ non élevée au carré » | Diagnostic contraire à l'`explanation` |
| lc_k3_T0 (concentration.reponses e0.1.2) | « Attention aux puissances de dix » → « 25 H : T₀ non élevée au carré » | Idem |
| lc_e1_additivite (reponses q.2.2) | « déterminer la constante d'intégration » → « servira plus tard pour écrire la solution » | Imprécis (deux constantes au second ordre, et pas encore vues) |
| note du cours | « régime apériodique et régime critique chacun sur sa diapo » → mention du retrait de la diapo critique | Cohérence |
| Simulation bilan.html (bloc régimes) | « … Régime critique : la frontière. » → texte retiré | Hors cadre |
| Simulation regimes.html (nom écrit près de 316 Ω) | « frontière : régime critique » / « critique » → « régime apériodique » / « apériodique » | Hors cadre (pas d'oscillation → apériodique) |
| Simulation oscillogramme.html (textes affichés et textes du tuteur : vue apériodique étape « frontiere », vue « critique », titre, conclusions, motifs, description) | « régime critique : la frontière », « retour le plus rapide sans oscillation », « la frontière est vers R ≈ 300 Ω » → « toujours le régime apériodique », « retour plus rapide, sans oscillation », « sans oscillation » | Hors cadre ; comportement inchangé |

Calculs refaits avec Python (tous justes) : T₀ = 2π√(0,1 × 4·10⁻⁶) = 3,97 ms ≈ 4 ms (π² = 10 : 4 ms) ; sommets 6 ; 4,0 ; 2,7 ; 1,8 V et creux −4,9 V ; T₀(2021 R) = 44,9 ms ; L(2022 N) = 0,05 H ; L(2018 N) = 63 mH ; L(2019 N) = 1 H ; C(2020 N) = 2,5 µF ; C(2023 N) = 0,1 µF ; E = 72 µJ, I_m ≈ 38 mA ; 2016 N : 7,2·10⁻⁴ J et 6,4·10⁻⁴ J perdus ; 4·10⁻⁵ J entre 6 V et 4 V ; 2024 N : 1,83·10⁻⁹ J ; 2025 N : 2,55·10⁻⁵ J ; 2020 N : 3,2·10⁻⁵ J et 2,05·10⁻⁵ J ; 1/(LC) = 2,5·10⁶ s⁻² ; rappels (6,3 ms ; 9,36·10⁻⁵ J ; 1,8·10⁻⁴ J ; 10⁻⁴ J ; k = 18 Ω) ; figures des cahiers (pseudo-périodique et apériodique) cohérentes. Les distracteurs des QCM correspondent bien aux erreurs annoncées dans les `explanation`.

Voix à refaire : lc_r4_national (exercices_fin_de_cours[0].enonce_dit ; reponses_fin_de_cours.e1s2.0.juste.parole, e1s2.1.1.parole, e1s2.1.2.parole) ; rappel C2_r1 (reponses.0.2.parole) ; rappel C2_r3 (reponses.0.2.parole, 1.juste.parole, 2.2.parole) ; rappel C3_r4 (reponses.3.juste.parole) ; rappel C8_r2 (reponses.0.2.parole) ; lc_e8_T0 (reponses_fin_de_cours.e0.0.1.parole, e0.2.1.parole, e0.2.2.parole) ; lc_p4_national (concentration.reponses.e0.0.1.parole, e0.0.2.parole ; reponses_fin_de_cours.e1.1.1.parole, e1.1.2.parole) ; lc_en2_depart (reponses_fin_de_cours.e0.2.1.parole, e0.2.2.parole) ; lc_a4_perdue (concentration.reponses.e0.0.2.parole) ; lc_l3_carre (reponses_fin_de_cours.e0.0.2.parole) ; lc_k3_T0 (concentration.reponses.e0.1.2.parole) ; lc_e1_additivite (concentration.reponses.q.2.2.parole). Chemins audio laissés tels quels ; l'audio lc_r2b_critique_v12.mp3 n'est plus utilisé.

Signalé sans correction (organisation, doutes) :
- lc_r3_ordre : la voix dit « on a trois écrans, à la même échelle » alors que la simulation regimes.html montre un seul écran avec un curseur R + r (les moments pseudo / apériodique / périodique / ordre existent). La voix est juste sur le fond ; à reformuler lors du prochain enregistrement.
- oscillogramme.html : la vue `?vue=critique` et l'identifiant interne « critique » (dans `regime()`, `command_schema`, `moments`) restent, ainsi que des commentaires de code. Aucun texte affiché ne dit plus « critique », et aucune diapositive n'utilise cette vue. Renommer la vue changerait le comportement, donc ce n'est pas fait.
- lc_n1_2020N, reponses_fin_de_cours.e0.1.1.ecrit : écrit « −I_m·ω·sin(ωt + φ) » avec un ω jamais défini (le cours écrit 2π/T₀). Ce n'est pas faux, mais c'est à harmoniser.
- Organisation : l'ordre est logique, les prérequis (rappels de q = C·u_C, de u_b, du cosinus et de sa dérivée) viennent avant leur usage, et la fiche bilan et la carte sont cohérentes avec C1 à C8. lc_r4_national garde ses trois énoncés vrai/faux ; la partie II garde 4 diapositives.

### Décisions à prendre (non corrigées)

- **Ancien cours ch1 `phys_ch1_waves_course_v1.json`** (publié, remplacé par le cours exemple) : il contient une partie « superposition » et les ondes sismiques S/P, hors cadre ; le test `backend/app/tests/test_waves_reference.py` exige la variante `superposition`. À dépublier, ou à nettoyer en adaptant le test. Même contenu dans `phys_ch1_waves_mixed_script_v3.json`.
- **ch6** : le cours recopiait mal les nationaux 2023 R et 2024 R (les vraies valeurs sont τ = 5 µs et C = 0,10 µF en 2024 R ; q_max = 120 µC en 2023 R) ; l'attribution au national a été retirée plutôt que de réécrire les exercices et leurs voix. La transcription `backend/data/exams/…/2023 R` (12 µC) et l'exploration `dipole_RC.json` portent la même erreur.
- **ch2** : exercice séance 4 bloc 3, v₂ = 0,24 m/s à 40 Hz contredit les autres valeurs (rides plus rapides à haute fréquence) ; proposition λ₂ = 0,9 cm, qui demande de refaire 6 réactions.
- **ch4** : `ra_t4_pourcentages` utilise t = (1/λ)·ln(N₀/N) avant `ra_c2_demo` (ordre des diapositives).
