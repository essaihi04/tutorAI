# Audit des cours de SVT face aux cours de professeurs

17 novembre 2026. Nos 4 cours de SVT sont comparés au cours de SVT du dépôt (`backend/cours 2bac pc/SVT/`, lu en image) et aux cours de 2 bac « Sciences Physiques et SVT » de moutamadris (français et arabe), avec le cadre officiel de la filière PC. Un manque est confirmé s'il est chez au moins deux professeurs, ou chez un seul et exigé par le cadre. Les corrections sont dans `corrections/svt-ch1..4.md`.

## Détail par chapitre

### Réactions responsables de la libération de l’énergie emmagasinée dans la matière organique

Sources lues :
- **Notre cours** : copie en attente `backend/data/courses/en_attente/svt_ch1_reactions_responsables_liberation_energie.json` (48 diapos, écran, cahier, voix, questions, démonstrations, exercices de fin de cours, blocs des séances) et son extrait `nos-cours/svt_ch1_….txt` ; simulations `frontend/public/media/simulations/svt/reactions_responsables_liberation_energie-tableau/` (recherche ciblée).
- **P1, Y. Alandaloussi** (dépôt, `Cours-Unit1-1.pdf`, scan) : p. 1-18 lues en image. `Cours-Unit1-2.pdf` = chapitre 2 (muscle), p. 1 vue en image, hors sujet ici.
- **P2, M. el Kaoune** (`m_energie_1`, 23 p.) : texte lu en entier ; p. 6, 9, 20 lues en image.
- **P3, M. Jaouani** (`m_energie_2`, 12 p.) : texte lu en entier ; p. 2, 3, 9 lues en image.
- **P4, M. Kammah** (`m_energie_3`, 18 p., équations en image seulement) : p. 1-18 lues en image.
- **Cadre** : JSON officiel (CNEEO 2015), sous-domaine 1.1 (connaissances et objectifs) ; fiche `cadre_reference_2bac_pc.json` (LE1-LE10, formules, mots exigés, hors_cadre, décisions) ; `docs/audit-programme-officiel/svt.md` ; SKILL cours-concentration (section SVT) ; règle 37 du SKILL professeur. `experience_profs.json` n’a pas de clé pour ce chapitre.

#### Plan comparé

| Partie chez les professeurs | Où chez nous | Remarque |
|---|---|---|
| Introduction : autotrophes / hétérotrophes, photosynthèse (P1 p1, P3 p1) ; catabolisme / anabolisme (P1 p2) | le_o1, le_p1, le_p2, le_o2 | Rappels présents ; catabolisme / anabolisme absents (un seul prof) |
| ATP : structure, hydrolyse, phosphorylation (P1 p6, P2 p2-3, P4 p8, p13) | le_a1, le_a2 | Pas de « adénine + ribose » ni d’ATPase |
| Mise en évidence respiration / fermentation : ExAO, levures (P1 p2-4, P2 p3-5, P3 p1, P4 p1-2, p15) | le_e1, le_e2, le_e3 | Présent ; pas de tableau masse des levures, pas d’eau de chaux / alcootest |
| Mitochondries en aérobiose / anaérobiose (P1 p5, P2 p4-5, P3 p2, P4 p2-3) | le_m1 | Présent |
| Glucose marqué au ¹⁴C : localisation des étapes (P2 p10, P3 p4, P4 p3-4) | — | **Absent** |
| Glycolyse : lieu, étapes, bilan, équation (P1 p6-8, P2 p5-7, P3 p5, P4 p4-5) | le_g1, le_g2, le_g3 | Présent (étapes sans intermédiaires nommés, décision du cadre) |
| Mitochondries isolées + glucose / pyruvate / ADP+Pi (P1 p8, P2 p7-8, P3 p4) | le_m3, le_m4 | Présent ; protocole d’isolement absent |
| Ultrastructure + composition chimique de la mitochondrie (P1 p9-10, P2 p9, P3 p3, P4 p6-8) | le_m2, le_m2b | Ultrastructure présente ; **composition chimique absente** |
| Matrice : acétyl-CoA, cycle de Krebs, équations (P1 p10-11, P2 p11-12, P3 p6, P4 p8-9) | le_k1 à le_k5 | Bilans en listes ; **équation du cycle et équation par pyruvate absentes** |
| Chaîne respiratoire, pulse d’O₂, vésicules, phosphorylation oxydative (P1 p12-15, P2 p12-16, P3 p7-9, P4 p9-13) | le_c1 à le_c10b | Présent et riche ; définition de la phosphorylation oxydative (couplage) absente |
| Bilan 38 ATP (P1 p18, P2 p16, P3 p9, P4 p13) | le_r1 | Présent |
| Fermentations alcoolique et lactique, étapes, équations (P1 p15-16, P2 p17-19, P3 p10, P4 p14-16) | le_f1, le_f2 | Équations globales présentes ; éthanal et 2ᵉ étape non écrits |
| Rendements, chaleur, comparaison (P1 p16-18, P2 p19-20, P3 p11, P4 p16-18) | le_r2, le_r3 | Rendements présents ; chaleur et énergie du résidu non calculées au cahier |
| Schéma de synthèse (P1 p17) / tableau comparatif (P3 p2, P4 p16) | le_e4, le_x4, le_b1, le_b2, le_r3 (simulation comparer.html) | Présent |
| Exercice national 2016 (entraîné / non entraîné, CO et tabac) (P2 p21-23) | le_x2 | Présent sous une autre forme (sans le CO) |

#### Manques confirmés

| Priorité | Catégorie | Ce que disent les professeurs | Chez nous | Où l’ajouter |
|---|---|---|---|---|
| haute | Définition | **Respiration cellulaire** : « oxydation (dégradation) complète du glucose en CO₂ et H₂O, en milieu aérobie, dans le hyaloplasme puis la mitochondrie, grande quantité d’énergie (38 ATP) » (P1 p4-5, P2 p5 et p16, P3 p2, P4 p17 ; cadre : « notion de respiration ») | Définitions écrites pour glycolyse (le_g3), chaîne (le_c4), fermentation (le_f2), mais aucune « Définition : la respiration cellulaire est… » | le_x4_synthese (ou le_r3_comparer), écran + cahier |
| haute | Équation bilan | **Équation du cycle de Krebs** : CH3-CO-CoA + 3 NAD+ + FAD + ADP + Pi + 3 H2O → 2 CO2 + 3 NADH,H+ + FADH2 + ATP + CoA-H (P1 p11, P3 p6 ; fiche cadre, formule LE5) | Seulement la liste « un tour : 2 CO2, 3 NADH,H+, 1 FADH2, 1 ATP » (le_k4) | le_k4_sorties (écran, cahier, CENTRE) |
| haute | Équation bilan | **Oxydation d’un acide pyruvique dans la matrice** : CH3-CO-COOH + 4 NAD+ + FAD + ADP + Pi (+ 3 H2O) → 3 CO2 + 4 NADH,H+ + FADH2 + ATP ; par glucose : 6 CO2 + 8 NADH,H+ + 2 FADH2 + 2 ATP (P1 p11, P2 p11-12, P3 p6, P4 p9) | Absente des diapos ; « 4 NADH,H+ par pyruvate, 8 par glucose » seulement dans l’exercice de bloc le_s3_b1 | le_k5_fois_deux |
| haute | Structure (cadre : « décrire les constituants ») | **Composition chimique** : membrane externe ≈ 40-60 % lipides / protéines, comparable à la membrane plasmique ; membrane interne 20 % lipides / 80 % protéines (transporteurs, ATP synthases) ; matrice : pas de glucose, acide pyruvique, ATP, NAD+, FAD, décarboxylases et déshydrogénases (P1 p9-10, P2 p9, P3 p3, P4 p7-8) | Aucun mot « lipides », « protéines », « composition », « enzymes de la matrice » | après le_m2_legender (nouvelle diapo ou bullet + cahier) |
| haute | Expérience de référence | **Glucose marqué au ¹⁴C** : tableau milieu extracellulaire / hyaloplasme / mitochondrie au cours du temps → glycolyse dans le hyaloplasme, pyruvate puis acides du cycle de Krebs dans la mitochondrie, CO₂ rejeté (P2 p10, P3 p4, P4 p3-4 ; cadre : « relation… structures cellulaires ») | Absent (0 occurrence de radioactif, ¹⁴C, marqué) | entre le_m3_isolees et le_k1_pyruvate (ou après le_e4_carte) |
| haute | Définition | **Phosphorylation oxydative** = couplage de l’oxydation des transporteurs réduits (chaîne, réduction de O₂) et de la phosphorylation de l’ADP par le gradient de protons : d’où son nom (P1 p15, P2 p15-16, P3 p9, P4 p13 ; fiche, mots exigés) | le_c7 nomme « phosphorylation oxydative » sans la définir ; le_m4 dit seulement « O₂ consommé et ATP produit sont couplés » | le_c7_sphere (bullet « Définition : … » + cahier) |
| moyenne | Équation bilan / bilan énergétique | Respiration avec ATP : C6H12O6 + 6 O2 + 38 ADP + 38 Pi → 6 CO2 + 6 H2O + 38 ATP (P3 p9, P4 p17 « + 38 ATP », P2 p16 « énergie (36 ou 38 ATP) » ; variante admise de la fiche) | Seulement « … + énergie » (le_e2, le_b1) et 38 ATP à part (le_r1) | le_r1_compteur (dernière ligne) |
| moyenne | Calcul / ordre de grandeur | Énergie perdue en **chaleur** : 2860 − 1159 = 1701 kJ (≈ 60 %) ; fermentation : l’essentiel reste dans le **résidu organique** (2 × 1346,5 kJ chez P1, 2 × 1360 kJ chez P2) (P1 p18, P2 p19-20, P4 p18) | Écran le_r2 : « le reste est libéré sous forme de chaleur », sans calcul ; 1701 kJ seulement dans la simulation rendement.html | le_r2_rendement et le_r3_comparer (ligne de calcul écrite + cahier) |
| moyenne | Étapes de la fermentation | Fermentation alcoolique : pyruvate **décarboxylé en éthanal (CH3-CHO)**, puis éthanal réduit en éthanol par NADH,H+ ; l’accepteur final des hydrogènes est l’éthanal (alcoolique) ou l’acide pyruvique (lactique) ; NAD+ régénéré (P1 p15-16, P2 p17-18, P4 p14-16) | le_f2 : « perd d’abord un CO₂ (il reste 2 C) », sans nom ni formule ; 2ᵉ étape jamais écrite comme réaction | le_f2_alcoolique, le_f1_lactique |
| moyenne | Document expérimental | **Masse de levures formées et glucose consommé** en aérobiose (1,970 g ; 150 g) contre anaérobiose (0,255 g ; 45 g ; test alcool +) → peu d’énergie en fermentation (P1 p5, P2 p3-5, P3 p2) | Absent (0 « masse », « poids » ; « multipli » seulement dans une réaction de calcul) | le_e3_sans_o2 ou le_m1_deux_levures |
| moyenne | Protocole (cadre : « proposer un protocole ») | **Isolement des mitochondries** : broyage, centrifugations (noyaux puis mitochondries) (P1 p8, P2 p7) | le_m3 : « suspension de mitochondries », sans protocole | le_m3_isolees |
| basse | Document expérimental | Mise en évidence de la **fermentation lactique** : lait frais, pH qui baisse (6,8 → 4,8), yaourt, lactose → glucose + galactose → acide lactique (P1 p3-4, P2 p17-18) | Seulement « muscle, bactéries du lait » (le_f1) | le_f1_lactique |
| basse | Conditions | Synthèse d’ATP par les vésicules : il faut aussi **ADP + Pi** dans le milieu (P1 p14, P2 p13, P3 p8, P4 p11) | Écran / cahier le_c10 et le_c10b sans ADP + Pi (seulement dans le texte de vesicules.html) | le_c10_vesicules |
| basse | Mise en évidence | Fermentation sans ExAO : CO₂ trouble l’**eau de chaux**, alcootest positif, glucose qui disparaît (bandelettes), légère **élévation de température** (P1 p3, P4 p15 ; chaleur aussi P2 p3) | Absent | le_e3_sans_o2 |
| basse | Notion | ATP = **adénine + ribose** + 3 phosphates ; hydrolyse par l’**ATPase** (P1 p6, P2 p2, P4 p13 et p18) | « adénosine + trois phosphates » (le_a1) | le_a1_monnaie |
| basse | Ordre de grandeur | 2860 kJ = énergie libérée par la combustion d’une mole de glucose dans une **bombe calorimétrique** (P2 p20, P4 p17) | « valeur donnée par l’énoncé » (le_r2) | le_r2_rendement |
| basse | Relation entre étapes | La chaîne **réoxyde NADH,H+ et FADH₂** : sans elle (sans O₂), NAD+ et FAD ne sont plus régénérés, la glycolyse et le cycle de Krebs s’arrêtent (P1 p11, P2 p7 et p16, P3 p6) | Dit pour la fermentation (le_f1) et dans le bloc le_s3_b3 ; jamais écrit pour la respiration | le_c3_decharge ou le_x4_synthese |

#### Manques chez un seul professeur

| Priorité | Catégorie | Ce que dit le professeur | Chez nous | Où l’ajouter |
|---|---|---|---|---|
| moyenne | Lecture de document | pHi (intérieur de la vésicule) représente l’espace intermembranaire, pHe la matrice (P2 p14) | Non dit | le_c10_vesicules |
| basse | Document national | Effet du monoxyde de carbone (tabac) sur la chaîne, national PC 2016 (P2 p21-23) | Cyanure seulement (le_c9) | à lire dans le document, pas à apprendre |
| basse | Vocabulaire | Catabolisme / anabolisme / métabolisme (P1 p2) | Absent | facultatif (le_o1) |
| basse | Notion | ATP, intermédiaire entre réactions exoénergétiques et endoénergétiques (P1 p6) | Absent | facultatif (le_a2) |
| basse | Schéma | Dessin d’observation annoté de la mitochondrie (P3 p3) | Étiquettes à glisser (le_m2b) | rien à faire |

#### Présent seulement à l’oral (à écrire)

- **le_c7_sphere** : « la membrane ne les laisse pas passer » = la membrane interne est **imperméable aux H⁺** (P1 p15, P2 p14, P4 p11) : à écrire à l’écran et au cahier.
- **le_k5_fois_deux** et **le_r1_compteur** : l’origine des 10 NADH,H+ (2 glycolyse + 2 acétyl-CoA + 6 Krebs) n’est que dans la voix ; l’écran dit « 10 NADH,H+ » sans la somme.
- **le_r3_comparer** : « dégradation complète : il ne reste que des **déchets minéraux**, CO₂ et H₂O » (mot clé de la fiche) : seulement dans la voix.
- **le_x3_chaine_en_panne** : l’exemple traité (O₂ stable à 40 % après le cyanure, ATP stable, hypothèse « le cyanure bloquerait… », « hypothèse vérifiée car… ») n’est que dans la voix ; l’écran ne donne que la méthode.
- **le_k2_acetyl** : « le coenzyme A est un transporteur du groupement acétyl, pas une enzyme » : voix seulement.
- Dans la simulation seulement (ni écran ni cahier) : chaleur 1701 kJ / 59,5 % (rendement.html, le_r2) ; ADP + Pi dans le milieu des vésicules (vesicules.html, le_c10).

#### Démonstrations qui sautent des étapes

- **le_e2_decrire** (écran, cahier) : la méthode dit « avec des valeurs » et la fiche exige « diminue de… à… », mais l’écrit dit « [O₂] diminue rapidement ; le CO₂ augmente » sans valeur d’arrivée ni valeur de CO₂.
- **le_r1_compteur** : la ligne de calcul part de « 10 NADH,H+ » sans écrire 2 + 2 + 6 = 10 ni « 2 FADH₂ = 2 tours × 1 » ; à ajouter avant (10 × 3).
- **le_r3_comparer** (écran, CENTRE) : r = (2 × 30,5)/2860 × 100 = 2,13 % saute « 61/2860 ≈ 0,0213 » (la démonstration du bloc le_s5_b2 est, elle, complète).
- **le_x3_chaine_en_panne** : exercice type sans correction écrite (description par périodes avec valeurs, déduction, flèches, vérification de l’hypothèse) ; voir oral ci-dessus.
- **le_t2_reduit** (DÉMO) : « il gagne des électrons ⏎ donc FAD est réduit » : la règle utilisée (« gagner des électrons, c’est être réduit ») n’est pas écrite comme outil.
- **le_c10b_vesicules_cas** (DÉMO) : ne dit pas « les sphères sont présentes, ADP + Pi présents », donc seule la condition manquante est examinée.
- **le_x2_qui_respire** (démo de l’exercice) : la conclusion ne cite pas le rendement, alors que le cahier demande « conclure par la voie dominante et son rendement ».
- Correctes jusqu’au bout : le_g3 (2 NAD+), le_r2 (40,5 %), le_s3_b1 (8 NADH,H+), le_s3_b3, le_s5_b2 (2,13 %).

#### Différences de notation ou de convention

| Nous | Eux | Garder |
|---|---|---|
| NADH,H+ | NADH+H+ (P1, P2), NADH₂ (P4), R’H₂ / RH₂ (P1, P2) | NADH,H+ (fiche, nationaux) ; RH₂ seulement à lire (le_c8) |
| ADP + Pi + énergie → ATP | … → ATP + H₂O (P4 p8, p12 ; P1 p14 schéma) | la nôtre (fiche) |
| 2860 kJ, r = 40,5 % / 2,13 % | 2840 kJ, 40,8 % / 2,15-2,24 % (P2, P3) ; 2860 kJ arrondi à 40 % / 2 % (P4) | la valeur de l’énoncé (décision de la fiche) |
| ½ O2 + 2 H+ + 2 e− → H2O | O2 + 4 H+ + 4 e− → 2 H2O (P4 p11) | la nôtre ; l’autre est une variante admise |
| « dégradation complète / incomplète » | « oxydation complète / incomplète » (P1, P3, P4) | la nôtre ; dire que les deux se valent |
| transporteurs T1-T4, sphère pédonculée | CI-CIV, CV, « sphérules pédonculées » (P4), « ATP synthétase » | la nôtre (décision de la fiche) |
| rendement en toutes lettres | r = E’/E × 100 (P1), r = e/R × 100 (P2) | la nôtre, avec les symboles en variante |
| Pi = phosphate inorganique | « phosphore inorganique » (P4 p8) | la nôtre (P4 se trompe) |
| fermentation alcoolique : 2 CO2 | « 2 CH3-CH2OH + CO2 » (P1 p4, coefficient oublié) ; P2 p18 recopie l’équation alcoolique pour la lactique | la nôtre (erreurs des professeurs) |

#### Hors cadre chez les professeurs (ne pas ajouter)

- Intermédiaires et enzymes de la glycolyse (glucose-6-phosphate, fructose diphosphate, glycéraldéhyde phosphate, hexokinase…) : P1 p7, P2 p6, P3 p5, P4 p5 (fiche : hors cadre).
- Intermédiaires du cycle de Krebs (acide oxaloacétique, citrique, succinate…) et GTP : P1 p10-11, P2 p11, P4 p9.
- Complexes I-IV nommés, ubiquinone (Q), cytochrome c, nombre de protons par complexe : P1 p12 et p14, P2 p15, P4 p8 et p12-13 (à lire seulement : le_c8).
- Potentiels d’oxydoréduction (mV), sens des potentiels croissants : P1 p12, P2 p13, P3 p7.
- Navettes malate-aspartate / glycérol-phosphate, 36 ou 38 ATP expliqués : P1 p18, P2 p16, P3 p9 (on garde « 36 si l’énoncé le dit »).
- FCCP (découplant) : P2 p14 ; force protonmotrice, chimiosmose, Mitchell : P4 p12 ; porine, ADN mitochondrial : P1 p10 ; ½ O2 + 2 e− → O²⁻ : P2 p15.
- Phases claire et sombre de la photosynthèse : P1 p1 ; formule développée du glucose, isomères (fructose) : P1 p6.

### Rôle du muscle strié squelettique dans la conversion de l’énergie

Version auditée : `backend/data/courses/en_attente/svt_ch2_role_muscle_strie_squelettique.json` (55 diapos ; écran, cahier, voix, questions, réactions, figures du cahier, exercices de fin).

Sources lues :
- **A = Alandaloussi** (dépôt, `Cours-Unit1-2.pdf`, titre vérifié : « Chapitre 2 : Rôle du muscle squelettique strié dans la conversion de l’énergie »). Scan sans texte : **pages 1 à 17 lues en image** (numérotation imprimée 19 à 35). Les pages citées ci-dessous sont celles du PDF (p1 = imprimée 19).
- **K = Kaoune** (`m_muscle_1`, BIOF PC/SVT, 19 p.) : texte en entier, **p11 à 17 en image** (équations, schémas du cycle, schéma de synthèse doc 21, examen 2016 N).
- **J = Jaouani** (`m_muscle_2`, 11 p.) : texte en entier, **p6 à 9 en image**.
- **M = Kammah** (`m_muscle_3`, 15 p.) : texte en entier, **p7 à 12 en image** (équations, chaleurs, équorine, structure).
- Cadre PC 1.2 / 1.3 (JSON officiel) ; fiche `cadre_reference_2bac_pc.json` (MSS1 à MSS13, `hors_cadre`) ; `docs/audit-programme-officiel/svt.md` ; `experience_profs.json` (pas de clé pour ce chapitre).

#### Plan comparé

| Partie chez les professeurs | Où chez nous | Remarque |
|---|---|---|
| Montage du myographe : grenouille, électrodes, stylet, cylindre ; tracés M (myogramme), S (signal d’excitation), T (temps) (A p1-2, M p1-2, K p2) | ms_s1_myographe, ms_s3_latence, ms_s5_mesures | Signal d’excitation et « ligne du temps » présents ; le nom « chronographe / signal du temps » manque (basse). |
| Excitabilité et contractilité (A p2, K p3, M p1) | — | Manque (moyenne). |
| Secousse : latence, contraction, relâchement, amplitude (A p2, J p1, K p3, M p2) | ms_s2 à ms_s6 | Complet, avec mesures chiffrées. |
| Intensité : inefficace, seuil, recrutement, amplitude max (A p3, J p2, K p3-4, M p2-3) | ms_i1_seuil, ms_i2_recrutement | Complet. |
| Deux excitations : isolées, fusion incomplète, complète ; **sommation** (A p3-4, J p2, K p4, M p3) | ms_f1 à ms_f3 | Le mot et l’idée « sommation » manquent à l’écrit. |
| Série : tétanos imparfait / parfait (A p4, J p2-3, K p4-5, M p4) | ms_f4, ms_f5, ms_f6 | Complet. |
| Fatigue : amplitude ↓, relâchement ↑, courbe de fatigue jusqu’à l’arrêt, cause (acide lactique, pH) (A p4-5, J p3, M p4-5, K p17) | ms_f7_fatigue, ms_x2 | Les deux signes y sont ; courbe de fatigue et cause manquent. |
| Chaleur : thermopile ; chaleur initiale (= de contraction + de relâchement) ; chaleur retardée ; anaérobiose (A p5-6, K p5-7, J p3, M p5-8) | ms_t1, ms_t2, ms_t3, ms_r3 | Subdivision de la chaleur initiale absente. |
| Chauveau et Kaufmann (sang entrant / sortant : O₂, CO₂, glucose, lipides 0, protides 0) (A p6-7, K p6, J p4, M p7) | ms_t4_consomme (dosage du muscle, pas du sang) | Glucose, lipides, protides, débit sanguin absents. |
| Effort d’intensité croissante : O₂ plafonne, puis acide lactique (A p6-7, K p6-7) | — (x1/x2 : entraîné / non entraîné) | Manque (moyenne). |
| Structure : muscle → faisceau → fibre (sarcolemme, sarcoplasme, noyaux, mitochondries, glycogène, RS, myoglobine) → myofibrille (A p7-10, K p7-9, J p4, M p11) | ms_u1, ms_u2, ms_u3 | Contenu de la fibre et schéma de la fibre à légender absents. |
| Ultrastructure : sarcomère, bandes A / I, zone (bande) H, stries Z ; actine / myosine (A p9-10, K p9, J p5, M p11-12) | ms_u3 à ms_u6 | Complet ; « unité structurale et fonctionnelle » seulement à l’oral. |
| Molécules : actine + troponine + tropomyosine ; myosine = tige + 2 têtes (site ATP, site actine) (A p10, K p10, J p5-6, M p12) | ms_u7, ms_u8 | « Deux têtes / tige » absent ; la voix dit « une tête ». |
| Relâché / contracté → glissement ; sarcomère unité fonctionnelle (A p10-11, K p10, J p7, M p12-13) | ms_g1, ms_g2, ms_g3 | Complet (valeurs en µm). |
| Exigences : myofibrilles isolées + Ca²⁺ + ATP, puis salyrgan / chélateur ; Ca²⁺ libéré après excitation (A p11, J p7-8, K p10-11) ; équorine (M p9-10) ; ⁴⁵Ca, examen 2016 N (K p17-18) | ms_c1_exigences, ms_c1b_essais (fibre glycérinée reconstituée) | Expériences d’inhibiteurs et preuve du Ca²⁺ libéré absentes. |
| Rôle du Ca²⁺ (troponine, tropomyosine) (A p12, J p8, K p10, M p14) | ms_c2_calcium | Complet. |
| Activité ATPase de la myosine, renforcée par l’actomyosine (K p10-11 et p18, M p14) | — | Manque (haute). |
| Cycle : attachement, pivotement, détachement ; schéma du cycle ; retour du Ca²⁺ par transport actif (A p12-13, J p7-8, K p12-14, M p14-15) | ms_c3 à ms_c7 | Cycle complet ; transport actif absent. |
| Conversion : énergie chimique → mécanique + chaleur (K p16, J p8, M p15) | ms_c8_conversion | Complet. |
| Nécessité du renouvellement : réserves d’ATP en mmol/kg et kJ face à la dépense (A p13, J p9, K p14-16) | ms_r1_reserve | Qualitatif seulement. |
| Expériences A / B / C (glycolyse bloquée, puis + PC bloquée) (A p14, J p9, K p15-16) | ms_r8_inhibiteurs | Présent (2020 R). |
| Trois voies et équations ; glycogène → glucose ; reconstitution de la PC (A p14-15, J p9-10, K p16-17, M p8-9) | ms_r2, ms_r4, ms_r5, ms_r7 | Équation du glycogène et ATP + C → PC + ADP absentes. |
| Voie dominante et effort (A p15-17, J p10, K p17) | ms_r6_relais | Complet. |
| Fibres de type I / II (A p15-17, J p10, M p13-14) | — | Donné par le document (voir hors cadre). |
| Schéma de synthèse (K p16 doc 21 ; cadre 1.3) | ms_b2_carte (carte conceptuelle) | Le schéma de synthèse du cadre 1.3 manque. |
| Exercices types d’examen (K p17-19 : 2016 N, 2016 R) | ms_x1 à ms_x4 (2016 N, 2017 R, 2020 R reconstitués) | Bonne couverture rédactionnelle. |

#### Manques confirmés

| Priorité | Catégorie | Ce que disent les professeurs | Chez nous | Où l’ajouter |
|---|---|---|---|---|
| haute | Expérience de référence | Myofibrilles isolées dans un milieu Ca²⁺ + ATP : la tension monte ; on ajoute le **salyrgan** (bloque l’hydrolyse de l’ATP) puis un **chélateur** (fixe le Ca²⁺) : la tension chute → ATP et Ca²⁺ indispensables (A p11 doc 14 ; J p7-8 doc 16 ; K p11 doc 16). Cadre MSS9 : « myofibrilles isolées… inhibiteurs ». | Seulement la fibre glycérinée reconstituée (ms_c1, ms_c1b). Aucun inhibiteur. | Nouvelle diapo après ms_c1b_essais (ex. `ms_c1c_inhibiteurs`), courbes de tension. |
| haute | Expérience de référence | Preuve que l’excitation libère le Ca²⁺ : Ca²⁺ du sarcoplasme ↑ juste après l’excitation, avant la tension (A p11 doc 14 fig. 1) ; équorine lumineuse pendant la contraction (M p9-10) ; ⁴⁵Ca : radioactivité dans le RS au repos, dans le sarcoplasme en contraction (K p17-18, examen 2016 N). | ms_c2_calcium affirme la libération du Ca²⁺, sans document à analyser. | ms_c2_calcium (document avant l’explication) ou une variante. |
| haute | Notion / expérience | La tête de myosine est une **ATPase** ; l’hydrolyse est faible avec la myosine seule, forte avec le complexe actomyosine (K p10-11 tableau 1, et p18 examen 2016 N Q3 ; M p14 « activation des enzymes ATPase des têtes de myosine » ; A p16 « myosine ATPase » dans un document). | ms_u7 : « site de fixation de l’ATP » seulement ; ms_c4 : « l’ATP est hydrolysé », sans dire par qui. | ms_u7_molecules (écrire « site ATPasique ») + ms_c4_rotation (tableau actine / myosine / actomyosine). |
| haute | Document de référence | Chauveau et Kaufmann : sang à l’entrée et à la sortie du muscle, au repos et en activité. Débit sanguin, O₂ et glucose consommés, CO₂ rejeté ↑ ; **lipides et protides : 0 g** → le glucose est le métabolite du muscle (A p6-7 doc 8 ; K p6 ; J p4 doc 8 ; M p7). Cadre 1.2 : « consommation du O₂ et du glucose ». | ms_t4 : dosage dans le muscle (glycogène, O₂, CO₂, acide lactique, ATP, PC) ; ni glucose, ni lipides ou protides, ni débit sanguin. | ms_t4_consomme (ajouter ce tableau ou une diapo juste avant). |
| haute | Schéma attendu | Schéma de synthèse : Ca²⁺ → hydrolyse de l’ATP ; ADP régénéré par PC, myokinase, glycogène → glucose → acide pyruvique → acide lactique, mitochondrie (O₂ → CO₂ + H₂O) (K p16 doc 21). Cadre 1.3 et MSS12 « schéma bilan ». | ms_b2_carte est une carte conceptuelle, pas le schéma cellulaire. svt.md le note déjà comme « en partie ». | Nouvelle diapo après ms_b2_carte (ex. `ms_b3_synthese`) avec cahier_figures. |
| haute | Raisonnement chiffré | Réserves d’ATP de 4 à 6 mmol/kg, soit 0,17 à 0,25 kJ/kg, face à 4,4 kJ/kg pour un 100 m → renouvellement obligatoire (A p13 doc 17 ; J p9 doc 19 ; K p14-15 doc 19 : 5,1 à 7,5 kJ face à 35 kJ ; K p16 : 2 à 3 s). | ms_r1 : « quelques secondes », sans valeur ni comparaison. | ms_r1_reserve (tableau et phrase de comparaison chiffrée). |
| moyenne | Définition | La chaleur initiale comprend une **chaleur de contraction** et une **chaleur de relâchement** (deux bosses sur la courbe) (A p6 ; K p5-6 ; J p3 ; M p6). | ms_t1, figure de ms_t2 : une seule bosse, sans subdivision. | ms_t1_chaleur_initiale (bullet, cahier, figure). |
| moyenne | Vocabulaire / notion | **Sommation** : l’effet de la 2ᵉ excitation s’ajoute à celui de la 1ʳᵉ (K p4 ; J p2 ; M p3). | Absent à l’écrit (seule la voix de ms_f2 dit « part de plus haut »). | ms_f2_fusion_incomplete, ms_f3_fusion_complete. |
| moyenne | Définition | Deux propriétés du muscle : **excitabilité** et **contractilité** (A p2 ; K p3 ; M p1). | Absent. | ms_s2_secousse (ou ms_s6_definition). |
| moyenne | Structure / schéma | Contenu de la fibre : sarcolemme, sarcoplasme, noyaux périphériques, myofibrilles, mitochondries, glycogène, réticulum sarcoplasmique (+ myoglobine), avec un schéma de fibre à légender (A p8-10 ; K p9 ; J p4 ; M p11). | ms_u2 : cellule longue, noyaux, stries. Mitochondrie seulement en ms_r5 ; RS seulement en ms_c2. | ms_u2_fibre (légende de la fibre) ou étiquettes en plus dans ms_u6_legender. |
| moyenne | Structure | Molécule de myosine = **une tige (bâtonnet) + deux têtes** (A p10 ; K p10 ; J p6). | ms_u7 : la voix dit « Chaque molécule a une tête ». C’est inexact. | ms_u7_molecules (écran, voix, cahier), ms_u8 (étiquette « tige »). |
| moyenne | Mécanisme | Relâchement : le Ca²⁺ est repompé dans le RS par **transport actif** (pompe, consomme de l’ATP) (A p13 étape 5 ; J p8 ; M p15). | ms_c6 : « retournent dans le réticulum », sans dire comment. | ms_c6_relachement. |
| moyenne | Équation | Hydrolyse du glycogène : (C₆H₁₀O₅)ₙ + n H₂O → n C₆H₁₂O₆ ; le glucose vient du sang et du glycogène (A p15 ; K p7 ; M p9 ; J p4). | Seule la voix de ms_t4 dit « glycogène = glucose mis en réserve ». Aucune équation. | ms_r4_fermentation (ligne avant l’équation) ou ms_t4. |
| moyenne | Équation | Reconstitution de la PC après l’effort : ATP + C → PC + ADP, l’ATP venant de la respiration (K p17 ; J p9). | Seule la voix de ms_r6 dit « à l’arrêt, la phosphocréatine se reconstitue ». | ms_r6_relais ou ms_r7_tableau (+ bilan ms_b1). |
| moyenne | Document type | Effort d’intensité croissante : O₂ consommé ↑ puis plafonne (3,04 L/min) ; alors l’acide lactique apparaît → la fermentation s’ajoute à la respiration (A p6-7 doc 8 ; K p6-7 tableau 2). | Absent (ms_x1 et ms_x2 comparent entraîné et non entraîné). | ms_r6_relais ou ms_x1. Ne pas écrire « VO₂max » ni « seuil anaérobie » (hors cadre). |
| moyenne | Myogramme | Courbe de fatigue (tétanos qui baisse jusqu’à l’arrêt) ; cause : accumulation d’acide lactique, baisse du pH et faible rendement (2 ATP) (A p4-5 ; J p3 ; M p4-5 ; K p17). | ms_f7 : deux signes sur des secousses ; cause seulement dans la chaîne de ms_x2. | ms_f7_fatigue. |
| basse | Vocabulaire | Pivotement (A, J, K, M), pont actomyosine (A p12, J p7-8, M p14), phases attachement / pivotement / détachement (J p7, K p13, M p14-15), angle ≈ 45° (J p6, K p13-14, A p13). | « rotation », « complexe actomyosine », « détachement ». | ms_c4_rotation, ms_c7_ordre (synonymes entre parenthèses). |
| basse | Vocabulaire | Excitation supraliminaire / infraliminaire (A p2 ; K p3 ; J p1) : mots des énoncés d’examen. | « efficace / inefficace » seulement. | ms_i1_seuil (synonymes). |
| basse | Structure | Striation **longitudinale** (myofibrilles parallèles), en plus de la striation transversale (A p8 ; K p9). | Transversale seulement. | ms_u2_fibre. |
| basse | Ordres de grandeur | Fibre : 10 à 100 µm de diamètre, jusqu’à plusieurs cm de long (A p8 ; K p9) ; myosine 16 nm, actine 5 nm de diamètre (A p9 ; J p5). | Faisceau 1 mm (voix), myofibrille 1-2 µm, sarcomère 2,5 µm ; la fibre n’a pas de taille. | ms_u2_fibre, ms_u4_filaments. |
| basse | Myographe | Les trois tracés nommés : myogramme (M), signal d’excitation (S), signal du temps / chronographe / diapason (T) (A p1-2 doc 1-2 ; M p1-2). | « signal d’excitation » (ms_s3), « ligne du temps » (ms_s5). | ms_s1_myographe ou ms_s5_mesures. |

#### Manques chez un seul professeur

| Priorité | Catégorie | Ce que dit le professeur | Chez nous | Où l’ajouter |
|---|---|---|---|---|
| basse | Myogramme | À intensité maximale, deux excitations rapprochées donnent la même amplitude (A p4, remarque). | Absent. | ms_f2 (remarque). |
| basse | Ultrastructure | Coupes transversales de la myofibrille en H, I, A : myosine seule, actine seule, les deux (A p9 doc 11). | Absent (déduit en ms_u5). | ms_u5_bandes (variante). |
| basse | Expérience | Hopkins et Fletcher : muscle en anaérobiose + acide monoiodoacétique + peu d’ATP → il se contracte un court moment puis s’arrête : l’ATP est la source directe (K p6). | Idée couverte par ms_r8 (muscle 3). | — |
| basse | Métabolisme | Glycogène → glucose → acide pyruvique → acide lactique ; l’acide lactique est repris par le foie et le cœur au repos (K p16-17). | « l’acide lactique baisse lentement » (voix ms_r6). | ms_r6_relais. |
| basse | Tableau | Tableau des trois voies : substrats utilisés / produits formés (J p9). | ms_r7 : O₂, acide lactique, rapidité, ATP. | ms_r7_tableau (2 lignes). |
| basse | Document | Glucose consommé ↑ et glycogène ↓ d’autant plus vite que l’exercice est intense (A p6 doc 8 fig. 1-2). | Absent. | ms_t4 (variante). |

#### Présent seulement à l’oral (à écrire)

- ms_u3_myofibrille : « le sarcomère est l’**unité structurale et fonctionnelle** de la myofibrille » (voix et réaction). Le cahier dit seulement « unité de la myofibrille ». Les 4 professeurs l’écrivent (A p10-11, J p5 et p7, K p9-10, M p12).
- ms_t4_consomme : « le glycogène, le glucose mis en réserve dans le muscle » et « la phosphocréatine, une molécule du muscle qui porte un phosphate ». Les valeurs (glycogène 1,08 → 0,80 ; O₂ 0,3 → 2,5 L/min ; acide lactique 1,1 → 12 ; ATP 5,0 → 4,8 ; PC 17 → 10) sont dans la voix et la simulation, mais pas au cahier.
- ms_t1_chaleur_initiale : « pince thermoélectrique piquée dans le muscle » (la thermopile de A p5, K p5, M p5).
- ms_c2_calcium : définition du réticulum sarcoplasmique (« réseau de petits sacs dans la fibre où le calcium est gardé »).
- ms_r6_relais : « à l’arrêt, la phosphocréatine se reconstitue et l’acide lactique baisse lentement ».
- ms_s6_definition : « excitation efficace : assez forte pour faire répondre le muscle » (l’écran dit seulement « efficace »).
- ms_f5_tetanos_parfait : « le tétanos parfait, la contraction la plus forte du muscle ».
- ms_u1_ouvrir : ordres de grandeur (muscle de quelques cm, faisceau ≈ 1 mm).
- ms_o2_atp : « la liaison du dernier phosphate se rompt » (origine de l’énergie de l’hydrolyse).

#### Démonstrations qui sautent des étapes

- **ms_t4_consomme (DÉMO)** : la 1ʳᵉ ligne « le muscle a travaillé : il a consommé de l’ATP » est posée sans le « car » (la contraction utilise l’énergie de l’hydrolyse de l’ATP, vue en o2). La ligne « phosphocréatine 17 → 10 » n’est reliée à aucune conclusion. Les lignes glycogène ↓ + acide lactique ↑ (→ fermentation) et O₂ ↑ + CO₂ ↑ (→ respiration) ne sont pas traitées : la démonstration s’arrête à « régénéré ».
- **ms_r8_inhibiteurs (DÉMO)** : il manque la comparaison au témoin, les valeurs et le muscle 3 (glycolyse + créatine kinase bloquées → ATP épuisé → la contraction s’arrête → l’ATP est la source directe et sa régénération est indispensable). Il manque aussi le « car » de la conclusion : « car PC + ADP → C + ATP ». Glycogène et acide lactique inchangés (preuve que la glycolyse est bien bloquée) : non écrits.
- **ms_s5_mesures** : l’écran donne les durées sans les soustractions. Il faut écrire chaque ligne : début 0,01 s, sommet 0,05 s, fin 0,10 s ; latence = 0,01 − 0 = 0,01 s ; contraction = 0,05 − 0,01 = 0,04 s ; relâchement = 0,10 − 0,05 = 0,05 s ; durée de la secousse = 0,10 s. Seule la voix donne les instants lus.
- **ms_g2_mesures → ms_g3_glissement** : pas de calcul des raccourcissements (sarcomère 2,5 − 2,0 = 0,5 µm ; I : 1,0 − 0,5 = 0,5 µm ; H : 0,5 − 0 = 0,5 µm ; A : 1,5 − 1,5 = 0). La chaîne n’est pas écrite : A constante = longueur de la myosine constante ; I et H raccourcissent du même 0,5 µm = le chevauchement augmente, donc les filaments glissent sans raccourcir.
- **ms_x3_hypothese** : on passe des valeurs à « l’hypothèse est vérifiée » sans l’étape d’interprétation. Il manque : « acide lactique 1,1 → 30,5 : fermentation lactique ; PC 17 → 10 : voie alactique ; donc voies anaérobies ; au 1500 m, acide lactique 3 et PC 16 : surtout respiration ».
- **ms_r1_reserve** : « elle suffit pour quelques secondes » est affirmé, sans calcul ni comparaison (voir le manque haute ci-dessus).
- **ms_c1b_essais** : chaque essai est constaté, mais il n’y a pas de ligne de comparaison avec l’essai complet (« l’essai 2 diffère de l’essai 1 par l’absence de Ca²⁺ seulement → le Ca²⁺ est nécessaire »). La conclusion arrive directement.

#### Différences de notation ou de convention

| Nous | Eux | Garder |
|---|---|---|
| zone H | « bande H » (A p10, J p5, K p9) | zone H (cadre), en ajoutant « (ou bande H) ». |
| fusion incomplète / complète | « fusion partielle / totale » (A p3-4, J p2, M p3) | les nôtres, avec les synonymes entre parenthèses. |
| chaleur initiale / retardée | « chaleur primaire / secondaire » (M p6-8) | les nôtres (cadre). |
| PC + ADP → C + ATP | « CP + ADP → ATP + C » (K p15-16) | PC (cadre) ; CP est une variante admise. |
| respiration à 36 ATP (38 accepté) | 38 ATP (A p15, M p7 et p9) ; « 36 ou 38 » (K p17) ; 36 (J p10) | 36, avec la mention « 38 accepté » déjà présente. |
| Fermentation avec 2 ADP + 2 Pi | Sans ADP ni Pi (A p15, K p16, M p9) ; avec (J p10) | la nôtre (cadre). |
| rotation, complexe actomyosine | pivotement, pont actomyosine | les nôtres (cadre MSS8), avec les synonymes. |
| Origine de la chaleur initiale : hydrolyse de l’ATP + PC (sans O₂) | « fermentation lactique » (A p6, J p3) : **erreur**. K p16 et M p8 la relient aux réactions anaérobies rapides (myokinase, PC). | la nôtre. |
| Ca²⁺ se fixe sur la troponine | « sur les troponines et les tropomyosines » (M p14) : erreur | la nôtre. |

#### Hors cadre chez les professeurs (ne pas ajouter)

- Nerf sciatique, grenouille décérébrée et démédullée, influx nerveux, potentiel d’action, synapse neuromusculaire, motoneurone, latence « temps d’arrivée de l’influx » (A p1-2 et p13, J p1 et p8, K p2, M p1 et p14) : physiologie nerveuse, hors cadre PC.
- Rhéobase (A p2-3, K p3) : dans `hors_cadre.mots`.
- Tubules transverses (A p10, M p11 et p14) : tolérés seulement s’ils sont annoncés.
- Fibres de type I / II, myosine ATPase par type de fibre (A p15-17, J p10, M p13-14) : `donne_par_le_document`. On les lit, on ne les apprend pas.
- Détail du modèle moléculaire : Pi puis ADP libérés, angles 90° → 50° → 45° (A p13, K p14) ; Ca²⁺ ≥ 1 µmol/L (K p14) ; 5 cycles/s, 15 µm/s (J p7) ; chaleur d’activation / de soutien (A p6, M p6).
- Contraction isométrique / isotonique (K p1) ; crampes et douleurs (K p17) ; « capacités maximales d’approvisionnement en O₂ » (K p17) : touche à VO₂max / seuil anaérobie, dans `hors_cadre`.
- QCM sur le cycle de Krebs et la chaîne respiratoire (K p19) : chapitre 1, pas un manque ici.

### Notion de l’information génétique

Version auditée : `backend/data/courses/en_attente/svt_ch3_notion_information_genetique.json` (59 diapos ; écran, cahier, voix, questions, réactions, DÉMO, exercices des séances ig_s1 à ig_s6, figures du tableau lues dans les `visual.alt` et les simulations `notion_information_genetique-tableau/*.html`). Recherches faites dans tous les champs du JSON (plusieurs écritures pour chaque mot).

Sources lues :
- **A = Alandaloussi** (dépôt, `Cours-Unit2-1.pdf`, titre vérifié : « Chapitre 1 : Nature de l’information génétique », pages imprimées 36 à 56). Scan sans texte : **pages 1 à 21 lues en image**. Pages citées = pages du PDF (p1 = imprimée 36). `Cours-Unit2-2.pdf` p1-2 lues en image : c’est le chapitre 2 « Expression de l’information génétique » (gène, mutation…), donc svt_ch4, pas ce chapitre.
- **M = Moussa** (`m_notion_1`, 15 p.) : texte en entier, **p2 à 14 en image**.
- **Y = Yamani** (`m_notion_2`, 8 p.) : texte en entier, **p1 à 5 en image** (p6-8 = gène, allèle, mutation : svt_ch4).
- **B = El Boukhari** (`m_notion_3`, 16 p., « Sc. Ex Opt Fr ») : texte en entier, **p4 à 16 en image**.
- **K = Kammah** (`m_notion_4`, 37 p.) : texte en entier, **p4 à 26 en image** (p27-37 = gène, mutation, transcription, traduction : svt_ch4).
- Cadre officiel PC 2.1 (JSON) ; fiche `cadre_reference_2bac_pc.json` (NIG1 à NIG11, `mots_cles`, `hors_cadre`, `tolere_si_annonce`) ; `docs/audit-programme-officiel/svt.md` (section ch3) ; SKILL cours-concentration (section SVT) ; professeur règle 37. `experience_profs.json` : pas de clé pour ce chapitre.

#### Plan comparé

| Partie chez les professeurs | Où chez nous | Remarque |
|---|---|---|
| Problème : cellule-œuf, où ? quelle nature ? comment transmise ? (A p2, M p1, K p1) | ig_o1, ig_o2 | Complet. |
| Mérotomie de l’amibe / section de l’acétabulaire + conclusion « le noyau est indispensable à la vie et à la régénération » (A p2-3, M p1, B p1, K p1-3) | ig_l1, ig_l2, ig_l3 | Expériences complètes ; la phrase de conclusion de la mérotomie manque au cahier d’ig_l1. |
| Greffe croisée de noyaux (A p3, M p1, Y p1, B p1-2, K p2-3) | ig_l4 | Complet (constater → déduire écrit). |
| Gurdon, xénopes (A p4, M p2, Y p1, K p4) ; clonage reproductif (B p2) | ig_l5 | Complet ; nous disons « grenouille », eux « xénope ». |
| Racine d’oignon : méristème, cellules en interphase / en division (A p5, K p5-6, Y p3, B p3) | ig_m6_photo | Le mot « méristème » (zone où les cellules se divisent) manque. |
| Ultrastructure du noyau ; chromatine = nucléofilaments ; chromosome à deux chromatides et centromère (A p6-7, M p2-3, K p6, p19-21) | ig_n1, ig_n2, ig_n3 | Mots « nucléofilament », « collier de perles » absents. |
| Phases de la mitose, avec un **schéma légendé de chaque phase** (animale 2n = 4, végétale 2n = 6) (A p7-8, M p3-4, Y p3, B p4-5, K p8-11) | ig_m1 à ig_m7b | Télophase incomplète ; un seul schéma titré-légendé (anaphase). |
| Animale / végétale : centrosome-asters / calottes ; étranglement / paroi (A p8, M p4, Y p4, B p5, K p11-12) | ig_m5 | Complet (centrosome non nommé, toléré). |
| Caryotype, 2n, diploïde, homologues, autosomes, gonosomes (M p5-6, K p7-8, Y p5) | ig_p1 (46 = 23 paires) | 2n jamais défini alors qu’on l’utilise (2n = 4) ; le caryotype relève de 2.3 (méiose). |
| Cycle cellulaire (définition, G1, S, G2, M ; deux événements : duplication / partage égal) (A p8-9, M p5, Y p4, B p5-6, K p6) | ig_c1, ig_c2, ig_r12 | Complet ; définition seulement dans le lead écran, pas au cahier. |
| Courbe de la quantité d’ADN, durée du cycle, aspect des chromosomes par phase (A p16-17, M p12, Y p4, B p13, K p22-23) | ig_c3 à ig_c6, ig_x2 | Complet, plus détaillé chez nous (calcul des durées). |
| Griffith : S (smooth, lisse, capsule) / R (rough, rugueux) ; 4 injections ; analyse du sang (A p9-10, M p6, Y p1, B p6-7, K p12-13) | ig_t1 à ig_t1f | Complet ; « lisse / rugueux », colonies, analyse du sang des exp. 2-3 absents. |
| Avery, MacLeod et McCarty 1944 : protéase, ARNase, ADNase (A p10, M p7, Y p1, B p8, K p13) | ig_t2, ig_t2b | Complet. |
| **Schéma de la transformation bactérienne** (ADN de S fragmenté → entre dans R → intégré à l’ADN de R → capsule → caractère héréditaire) (A p10, M p7, Y p1, B p9, K p14) | ig_t3_support | Partiel : ni intégration, ni transmission aux descendantes, ni schéma à légender. |
| Hershey et Chase, cycle du bactériophage (A p11-12, M p8, K p14-15) | — | Hors cadre (voir fin). |
| L’ADN constituant des chromosomes : Feulgen (rouge), chromosome « fantôme » éclaté → chromosome = ADN + protéines (A p12-15, M p9) | — | Absent (objectif du cadre). |
| Constituants de l’ADN, nucléotide ; polymère ; purines / pyrimidines (A p13, M p9-10, Y p2, B p10, K p16) | ig_s1, ig_s5b | Complet sauf « polynucléotide », « purines / pyrimidines », « acide désoxyribonucléique ». |
| Chargaff : A/T, G/C, (A+G)/(T+C) = 1, **(A+T)/(G+C) caractéristique de l’espèce** ; exercice 24 nucléotides, 0,34 nm (A p14, M p10, Y p2, B p11, K p17-18) | ig_s2_chargaff | (A+T)/(G+C) et l’exercice absents. |
| Franklin ; Watson et Crick : double hélice, liaisons H 2/3, antiparallèles, dimensions 0,34 / 3,4 / 2 nm (A p15, M p10-11, Y p2, B p11-12, K p18-19) | ig_s3, ig_s4 | Dimensions et Franklin absentes. |
| Chromatine ↔ chromosome ↔ ADN : nucléosome, histones, condensation (A p15, M p11, Y p5, B p12, K p20-21) | ig_n1, ig_n2 | Complet. |
| Trois hypothèses ; Meselson et Stahl G1, G2, G3, schémas (A p17-19, M p12-13, Y p5-6, K p24-25) | ig_r1 à ig_r6 | Complet (G3 25 / 75 % aussi). |
| Taylor : thymidine ³H, colchicine, **autoradiographie**, 3 cycles (A p19-20, B p13-14, M p13 exercice) | ig_r7, ig_r8 (national 2017 R, 2 cycles) | Mot « autoradiographie », colchicine et 3e cycle absents. |
| Yeux, fourches, séparation des brins (rupture des liaisons H), ADN polymérase 5'→3', matrice (A p20-21, M p13-14, Y p7, B p15-16, K p20, p26) | ig_r9 à ig_r11b | La rupture des liaisons hydrogène n’est pas dite. |
| Réplication + mitose = stabilité de l’information (A p9, M p14, B p6) | ig_r12 | Complet. |
| Gène, allèle, mutation, relation gène-protéine (Y p6-8, K p27-37, A Unit2-2) | — | Dans svt_ch4, pas ici. |
| (chez nous seulement) brin complémentaire, calcul des durées de phase, légender ADN / réplication / anaphase | ig_s5, ig_c6, ig_m7b, ig_s5b, ig_r11b | Plus complet que les professeurs. |

#### Manques confirmés

| Priorité | Catégorie | Ce que disent les professeurs | Chez nous | Où l’ajouter |
|---|---|---|---|---|
| haute | Définition / critères | Télophase : décondensation, **réapparition de l’enveloppe nucléaire et du nucléole**, **disparition du fuseau**, division du cytoplasme (A p8, M p4, Y p3, B p4, K p10) | Écran : « décondensent ; deux noyaux » ; cahier : « étranglement, deux noyaux » ; enveloppe et nucléole seulement à la voix (« se reforment »), fuseau nulle part | ig_m4_anaphase (bullet + cahier) |
| haute | Schéma attendu | Schéma titré et légendé de **chaque phase** (prophase, métaphase, anaphase, télophase), animale et végétale (A p7, M p3-4, Y p3, B p4-5, K p8-11) ; cadre : « Réaliser des schémas en relation avec les phases de la mitose » ; NIG4 | Un seul schéma titré-légendé (anaphase, ig_m7 / ig_m7b) ; les autres phases seulement animées | ig_m2, ig_m3, ig_m4 (titre + légendes au cahier), ig_m5 (une phase végétale 2n = 4) ; un « à toi de légender » de la métaphase |
| haute | Schéma / raisonnement | Mécanisme de la transformation bactérienne en schéma : la chaleur fragmente l’ADN de S → un fragment entre dans R → **s’intègre à l’ADN de R** → R synthétise la capsule → devient S, **caractère héréditaire transmis aux bactéries filles** (A p10, M p7, Y p1, B p9, K p14) ; cadre : « schémas en relation avec la nature chimique du matériel génétique » | ig_t3 : « un fragment entre… fabrique une capsule » ; ni intégration, ni descendance, ni schéma à légender | ig_t3_support (+ diapo « à toi de légender » sur le modèle d’ig_s5b) |
| haute | Expérience de référence | **Relation chromosome–ADN** démontrée : réaction de Feulgen (l’ADN coloré en rouge → les chromosomes contiennent de l’ADN) ; chromosome « fantôme » après digestion des protéines → chromosome = ADN + protéines (A p12-15, M p9) ; cadre : « Mettre en évidence la relation entre les chromosomes et la molécule d’ADN » | Affirmé sans preuve (« un chromosome = un long fil d’ADN », ig_p1 ; ADN + histones, ig_n1) | nouvelle diapo après ig_n1_noyau (ou après ig_t3_support) |
| haute | Expérience de référence | Taylor : thymidine radioactive, colchicine (bloque en métaphase), **autoradiographie** (points noirs), 3e cycle : la moitié des chromosomes non marqués, l’autre moitié une chromatide marquée (A p19-20, B p13-14, M p13) ; « autoradiographie » est dans les `mots_cles` de la fiche ; NIG9 | ig_r7, ig_r8 : 2 cycles, ni le mot autoradiographie, ni le 3e cycle | ig_r7_thymidine1 (mot + technique), ig_r8_thymidine2 (+ 3e cycle) |
| moyenne | Formule / conclusion | Chargaff : (A+G)/(T+C) = 1 constant = caractéristique de l’ADN ; **(A+T)/(G+C) varie d’une espèce à l’autre = caractéristique de l’espèce** (A p14, M p10, Y p2, K p17-18) | Seulement A/T, C/G ; (A+G)/(C+T) au tableau sans explication | ig_s2_chargaff |
| moyenne | Exercice type | Fragment de 24 nucléotides, (A+T)/(G+C) = 1,4 → T = 1,4 G, 2T + 2G = 24 → G = C = 5, A = T = 7 ; longueur 0,34 × 24 = 8,16 nm ≠ 4,08 nm mesurés → deux brins (A p14, K p17-18) | Absent (seul : 30 % de A → 30 % de T, ig_s4_b3) | exercice de séance après ig_s2 / ig_s4 |
| moyenne | Ordres de grandeur | Double hélice : 0,34 nm entre deux paires de bases, 3,4 nm par tour, 2 nm de diamètre (A p15, M p11, B p11, K p19) | Absent | ig_s4_helice |
| moyenne | Mécanisme | Réplication : les deux brins se séparent par **rupture des liaisons hydrogène** entre les bases (sans nommer l’hélicase, hors cadre) ; chaque brin sert de **matrice** (A p21, Y p7, B p15, K p26) | « les deux brins se séparent » (ig_r9) ; « modèle » seulement | ig_r9_yeux |
| moyenne | Notation | 2n : cellule diploïde, n = nombre de paires de chromosomes homologues (M p6, K p7-8, Y p5) ; toléré (`tolere_si_annonce`) | « 2n = 4 » utilisé 55 fois, jamais défini ; « homologue », « diploïde » absents | ig_p1_chromosomes (46 = 2n, n = 23) et rappel dans ig_m1 |
| moyenne | Vocabulaire | Chromatine en interphase = **nucléofilaments**, aspect en **collier de perles** (nucléosomes) (A p6, p15 ; M p2, p11 ; Y p5 ; B p12 ; K p20) | « fins filaments », nucléosome | ig_n1_noyau |
| moyenne | Vocabulaire | ADN = **acide désoxyribonucléique** (sucre désoxyribose, acide phosphorique, dans le noyau) (A p10, M p7, Y p2, K p13) | Le sigle n’est jamais développé | ig_s1_nucleotide (ou ig_t2_avery) |
| moyenne | Légendes | Fuseau = fibres polaires + fibres chromosomiques (A p7-8, K p8-9, B p4-5) ; toléré pour les légendes | « fibres du fuseau » | ig_m3_metaphase, ig_m7b_legender |
| basse | Conclusion écrite | Mérotomie : « le noyau est indispensable à la vie de la cellule, à la régénération et à la division » (A p2, M p1, K p2-3) | Seulement dans l’exercice ig_s1_b1 ; cahier d’ig_l1 sans déduction | ig_l1_amibe (cahier) |
| basse | Vocabulaire | S = smooth (colonies lisses), R = rough (rugueuses) (A p9, M p6, B p6) | « forme S / R » sans le sens des lettres | ig_t1_griffith |
| basse | Document | Analyse du sang : exp. 2 et 3 « absence de tout pneumocoque » (A p9, M p6, K p13 ; B p7 « très peu de R ») | Sang seulement pour l’exp. 4 | ig_t1c_exp2, ig_t1d_exp3 |
| basse | Vocabulaire | ADN = polymère de nucléotides / polynucléotide (A p13, M p10, K p16) | « les nucléotides s’enchaînent en un brin » | ig_s1_nucleotide |
| basse | Vocabulaire | Bases puriques (A, G) / pyrimidiques (T, C) (A p13, B p10, K p16-17) | Absent | ig_s1 ou ig_s2 |
| basse | Histoire | Franklin, diffraction X → double hélice (M p10, Y p2) | Absent | ig_s4_helice (une ligne) |
| basse | Histoire | Avery, MacLeod et McCarty (1944), lipides et glucides retirés de l’extrait (A p10, M p7) ; dates 1928 / 1944 / 1958 (A, M, K) | « Avery » seul ; seule date : 1953 | ig_t2_avery, ig_t1, ig_r2 |
| basse | Document | Méristème : zone de la racine où les cellules se divisent (A p5, K p5, B p3) | « apex de racine d’oignon » | ig_m6_photo |
| basse | Méthode | Classer chronologiquement des photos / schémas de mitose (A p6, B p16 exercice 1) | Identification cellule par cellule seulement | ig_m6_photo ou exercice de séance ig_s3 |
| basse | Schéma | Chromosome métaphasique : chromatides, centromère, bras (+ télomères) (M p3, K p9, p21) | Chromatides et centromère seulement | ig_n3_chromatides |
| basse | Vocabulaire | Centrosome à l’origine des asters chez l’animal (A p8, M p4, Y p4, K p11-12) ; toléré seulement pour le distinguer du centromère | Absent | ig_m5_vegetale (piège centrosome ≠ centromère) |
| basse | Document | Escherichia coli (A p17, M p12, K p24) | « des bactéries » | ig_r2_experience |
| basse | Définition | Définition écrite du cycle cellulaire : « du début d’une interphase au début de la suivante » (A p9, M p5, Y p4, B p5) | Lead écran seulement ; cahier = formule | ig_c1_cycle (cahier) |

#### Manques chez un seul professeur

| Priorité | Catégorie | Ce que dit le professeur | Chez nous | Où l’ajouter |
|---|---|---|---|---|
| basse | TP | Extraction de l’ADN d’oignon (eau + NaCl, filtration, alcool, réactif de Schiff) (A p12) | Absent | facultatif, avec la diapo Feulgen |
| basse | Idée | Gurdon : le noyau d’une cellule différenciée (intestin) garde toute l’information (K p4) | Absent | ig_l5_gurdon |
| basse | Formule | Après n cycles : 2ⁿ cellules (K p11) | Doublements comptés un par un | ig_c6_durees |
| basse | Ordre de grandeur | Interphase 18 h / mitose 2 h (K p22) ; fiche : interphase ≈ 90 % | « la plus longue » | ig_c1_cycle |
| basse | Méthode | Tracer la courbe de l’ADN avec échelles (Y p4) | Courbe donnée | exercice de séance ig_s2 |
| basse | Définition | Extrémité 5' = nucléotide dont le phosphate est libre (Y p3) | 5' / 3' non définis | ig_s3_antiparalleles |

#### Présent seulement à l’oral (à écrire)

- ig_r2_experience : « L’azote est dans les bases, donc leur ADN devient lourd » (voix seule) ; écrit chez A p17, M p12, K p24.
- ig_m4_anaphase : « deux noyaux **se reforment** » (enveloppe nucléaire) : voix seule ; l’écran dit « deux noyaux ».
- ig_r6_rediger : les prédictions de chaque hypothèse (conservative : deux bandes dès G1 ; semi-conservative : hybride, puis hybride + légère ; dispersive : une seule bande) sont dites et montrées au tableau, mais le cahier n’écrit que le résultat et la conclusion.
- ig_s2_chargaff : le calcul 30,9 / 29,4 ≈ 1,05 n’est qu’au tableau (simulation) ; l’écran écrit « A/T ≈ 1 ».
- ig_c6_durees : G2 = 4 h et M = 1 h (20 % et 5 %) ne sont qu’au tableau (simulation).
- ig_m5_vegetale : « pas d’étranglement, **car** il y a la paroi » (justification à l’oral seulement).
- ig_c4_aspect : « à la fin de la phase S, il n’y a plus d’yeux de réplication, car la réplication est terminée ».
- ig_m3_metaphase : « c’est le moment où on compte le mieux les chromosomes ».

#### Démonstrations qui sautent des étapes

- ig_c6_durees : « S = 20 − (9 + 4 + 1) = 6 h » : les lignes G2 = 20/100 × 20 h = 4 h et M = 5/100 × 20 h = 1 h manquent à l’écran et au cahier ; « 45/100 = 0,45 » sauté (alors que ig_s2_b3 écrit « 30/100 = 0,3 ») ; pas de phrase finale « la phase S dure 6 h ».
- ig_s2_chargaff : « (A + G)/(C + T) = 1 » apparaît au centre sans dérivation ni voix (A = T et G = C, donc A + G = T + C) ; la conclusion « chez toutes les espèces » s’appuie sur la seule ligne Homme à l’écran.
- ig_r4_g2 : « Seule la semi-conservative explique : 2 molécules hybrides, 2 légères » sans les étapes : chaque molécule hybride (un brin ¹⁵N + un brin ¹⁴N) se réplique en ¹⁴N → 1 hybride + 1 légère ; × 2 → 2 hybrides + 2 légères → 50 % / 50 % → deux bandes égales.
- ig_r5_semi : « 75 % / 25 % » sans calcul : 8 molécules en G3, 2 hybrides → 2/8 = 25 %, 6/8 = 75 % (ig_s5_b3 donne les nombres, pas les pourcentages).
- ig_r3_g1, ig_s5, ig_m7_schema, ig_x2, ig_n3, ig_s5_b1, ig_s6_b2, ig_s2_b3, ig_s5_b3 : complètes (données → règle → une ligne par étape → conclusion).

#### Différences de notation ou de convention

| Nous | Eux | Garder |
|---|---|---|
| q → 2q | Q → 2Q (A p17, M p12, Y p4) | q (variante admise par la fiche) ; dire que Q est accepté. |
| chromatides qui migrent | « chromosomes fils / chromosomes simples » en anaphase (A p8, B p4, K p9, Y p3) | Nos mots ; ajouter le synonyme « chromosome fils (à une chromatide) ». |
| grenouille (Gurdon) | xénope (A p4, M p2, K p4) | « xénope (une grenouille) » : c’est le mot des documents. |
| désoxyribonucléase | ADNase / DNase (M, Y, B, K) | Les deux (la fiche : donné par le document). |
| réplication ; modèle | duplication ; matrice (A, M, B, K) | Réplication ; citer les synonymes. |
| fuseau achromatique | fuseau de division / mitotique (M, K, B) | Les trois, comme synonymes. |
| Dispersive en G2 : une seule bande entre l’hybride et la légère | « que de l’ADN hybride » (A p18, M p13, Y p6) | La nôtre (plus juste) ; accepter « une seule bande intermédiaire ». |
| ADN polymérase : 5' → 3' | K p26 : « sens 3' vers 5' » (faux) | 5' → 3' (A, M, Y d’accord). |
| — | K p26 : « Taylor a montré que la réplication est conservative chez les eucaryotes » (faux) | Ne pas reprendre. |
| Interphase (cellule qui ne se divise pas) | « cellule au repos » (A p5, K p6) | Ne pas dire « repos » : la cellule réplique son ADN. |

#### Hors cadre chez les professeurs (ne pas ajouter)

- Expérience de Hershey et Chase (³²P, ³⁵S) et cycle du bactériophage (A p11-12, M p8, K p14-15) : la fiche tolère le bactériophage comme exemple, sans l’expérience de marquage.
- Hélicase, primase, amorce, fragments d’Okazaki, brin précoce / tardif, réplication asymétrique (A p21, M p14, Y p7, B p15, K p26).
- Formules C₅H₁₀O₄, H₃PO₄, formules développées des bases, carbones 1' à 5', nucléosides (thymidine, adénosine…) (A p13, M p9-10, K p16).
- Niveaux 30 / 300 / 700 / 1400 nm de condensation (K p21, M p11), centriole et microtubules kinétochoriens (M p3, B p5, K p12).
- Caryotype, autosomes / gonosomes, 2n = 44 A + XY, espèces haploïdes (M p5-6, K p7-8) : chapitre méiose (2.3).
- Gène, allèle, mutation, strept R, drépanocytose, code génétique, transcription, traduction (Y p6-8, K p27-37, A Unit2-2) : svt_ch4.
- Clonage reproductif (B p2), rétrovirus (M p8), méiose de l’introduction (B p1).

### Relation gène-protéine (expression de l’information génétique)

Sources lues :
- **Notre cours** : copie en attente `backend/data/courses/en_attente/svt_ch4_relation_gene_proteine.json` (53 diapos : écran, cahier, voix, questions, réactions ; 8 compétences et leurs rappels ; 6 séances, blocs, exercices et démonstrations) et son extrait `nos-cours/svt_ch4_….txt` ; simulations `relation_gene_proteine-tableau/marquage.html` et `mutation.html` (recherche ciblée).
- **P1, Y. Alandaloussi** (dépôt, `Cours-Unit2-2.pdf`, scan, « Chapitre 2 : Expression de l’information génétique ») : 13 p. lues en image (numérotées 57 à 69 ; citées ici avec ces numéros). `Cours-Unit2-3.pdf` p. 1 vue : c’est la méiose (chapitre 3), hors sujet.
- **P2, M. Jaouani** (`m_expression_1`, 11 p.) : texte lu en entier, p. 1-11 lues en image.
- **P3, A. El Yamani** (`m_expression_2`, 5 p., scan, partie 2.2 seulement) : p. 1-5 lues en image.
- **P4, El Boukhari** (`m_expression_3`, 15 p.) : texte lu en entier, p. 2-13 lues en image.
- **Cadre** : JSON officiel (CNEEO 2015), sous-domaines 2.1 (fin) et 2.2 ; fiche `cadre_reference_2bac_pc.json` (RGP1-RGP10, formules, mots_cles, hors_cadre, valeurs_reference) ; `docs/audit-programme-officiel/svt.md` ; SKILL cours-concentration (section SVT) ; règle 37 du SKILL professeur. `experience_profs.json` n’a pas de clé SVT (seulement Physique-Chimie).

#### Plan comparé

| Partie chez les professeurs | Où chez nous | Remarque |
|---|---|---|
| Caractère héréditaire, phénotype(s) d’un caractère (P1 p57, P2 p1, P4 p1-2) | rg_o1_caracteres | Exemples seulement ; **aucune définition** du caractère héréditaire ni du phénotype |
| E. coli et streptomycine → mutation, gène, allèle (P1 p57-59, P2 p1-2, P4 p2-3) | rg_g3_mutation, rg_g3b_mutation, rg_g1_gene, rg_g2_allele | Présent ; agents mutagènes non nommés |
| Types de mutations ponctuelles (P2 p2) | rg_m2 à rg_m5 | Présent (plus complet chez nous : silencieuse, faux-sens, non-sens) |
| Paire de chromosomes homologues et allèles (P2 p3) | rg_g2_allele | « par paires », jamais le mot « homologues » |
| Albinisme : tyrosinase, mélanine (P4 p4) | séance rg_s2_b1 (QCM) | Pas de diapo ni de cahier |
| Drépanocytose : 3 échelles, HbA / HbS, fibres (P1 p60-61, P2 p4-5, P4 p5, p14) | rg_p1, rg_p2, rg_p3 | Présent ; « échelle » au lieu de « phénotype macroscopique / cellulaire / moléculaire » ; fibres d’HbS seulement à l’oral |
| Beadle et Tatum, Neurospora (P1 p59-60, P4 p6-7, p14) | — | **Absent** |
| Séquences HbA / HbS, origine génétique (P1 p60-61, P2 p5, P4 p8, p15) | rg_e6_drepanocytose | Présent |
| Document protéine – caractère de national | rg_p4_document, rg_e5_national | Propre à nous (LDL, amélogénine) : bien |
| Vert de méthyle – pyronine (P1 p61-62) | — | Un seul professeur |
| Marquage uracile / ³²P, greffe de noyau ou chasse (P1 p62, P2 p5-6, P4 p9) | rg_a3_uracile | Présent sans l’étape « milieu non radioactif » |
| Acides aminés marqués : synthèse au cytoplasme (P3 p1) | rg_a4_acides_amines | Présent |
| Synthèse in vitro : injection d’ARNm → incorporation d’acides aminés (P1 p62, P2 p8, P3 p3) | — | **Absent** |
| Structure de l’ARN, comparaison ADN / ARN (P1 p63, P2 p6, P3 p2, P4 p9) | rg_a1_arn | Présent ; composition du nucléotide absente ; colonne ADN seulement à l’oral |
| Électronographie « arbre de Noël » (P1 p64, P2 p7) | — | **Absent** |
| Mécanisme de la transcription (P1 p64, P2 p7, P3 p2, P4 p10, p15) | rg_t1 à rg_t6 | Présent, plus détaillé chez nous (sens, brin non transcrit) |
| Code génétique : 4, 16, 64 (P1 p65, P3 p3, P4 p11) | rg_c1_codon | Présent |
| Nirenberg et Matthaei, poly-U (P1 p65-66, P2 p9, P3 p3) | — | **Absent** |
| Tableau du code, propriétés (P1 p66, P2 p9-10, P3 p3, P4 p11) | rg_c2, rg_c3, rg_c5 | Présent ; « un codon = un seul acide aminé », « 61 codons », « codons synonymes » absents à l’écran |
| Éléments de la traduction : ribosome (ARNr + protéines), ARNt, énergie (P1 p66-67, P2 p8-9, P3 p4, P4 p12) | rg_r1_acteurs | Composition du ribosome et besoin d’énergie absents |
| Étapes de la traduction (P1 p68-69, P2 p10, P3 p4, P4 p12-13) | rg_r2 à rg_r5, rg_s5_etapes | Présent (sans sites A / P : hors cadre, bien) |
| Schéma bilan (P1 —, P2 p11, P3 p1, p5, P4 p13) | rg_s2_schema, rg_s3_construire | Présent |
| Rédaction du barème, mutations jugées avec le code | rg_m1 à rg_m6, rg_e1 à rg_e6 | Propre à nous (aucun professeur ne le fait) : bien |

#### Manques confirmés

| Priorité | Catégorie | Ce que disent les professeurs | Chez nous | Où l’ajouter |
|---|---|---|---|---|
| haute | Définition | **Caractère héréditaire** : trait (comportement vis-à-vis d’un antibiotique, couleur, groupe sanguin…) transmis de génération en génération ; s’oppose aux caractères acquis (P1 p57, P2 p1, P4 p1) ; cadre RGP1 « définir caractère héréditaire » | Seulement des exemples (rg_o1, puce 1) ; absent des « six définitions » de rg_e1 | rg_o1_caracteres (écran + cahier) ; rg_e1_restitution |
| haute | Définition, vocabulaire | **Phénotype** : ensemble des caractères observables (détectables) d’un individu ; un caractère a deux phénotypes ou plus (Strep S / Strep R ; groupes A, B, AB, O) ; phénotype **macroscopique, cellulaire, moléculaire** (P1 p61, P2 p1-2, P4 p2, p5, p14) ; cadre RGP1 et mots_cles « phénotype moléculaire / cellulaire / macroscopique » | Mot « phénotype » une seule fois (rg_p4, « phénotype normal ») ; rg_p1-p3 disent « échelle de l’organisme / cellulaire / moléculaire » sans « phénotype » | rg_p1_organisme, rg_p2_cellule, rg_p3_proteine (titre « phénotype … » dans le cahier) ; rg_g3_mutation (Strep S / Strep R = deux phénotypes) ; rg_e1_restitution |
| moyenne | Expérience historique | **Beadle et Tatum** (Neurospora, mutants arg⁻, milieu minimum + ornithine / citrulline / arginine) : constater quelle souche pousse → déduire l’enzyme non fonctionnelle → conclure « un gène → une enzyme (protéine) » (P1 p59-60, P4 p6-7, p14) ; cadre « relation gène-protéine à partir de l’exploitation de données » | Absent (0 occurrence) | Nouvelle diapo après rg_p4_document (partie II) ou avant rg_s1_gpc |
| moyenne | Expérience, document | **Synthèse in vitro** : extrait sans ADN ni ARNm ; après chaque injection d’ARNm, les acides aminés incorporés augmentent pendant que l’ARNm diminue → l’ARNm est nécessaire à la synthèse des protéines (P1 p62 doc 5, P2 p8 doc 14, P3 p3 III.1) | Absent | Nouvelle diapo après rg_a4_acides_amines |
| moyenne | Expérience historique | **Nirenberg et Matthaei (1961)** : ARNm poly-U → polyphénylalanine (UUU = Phe), poly-C → Pro, poly-GU → Val, Cys : preuve du code en triplets (P1 p65-66, P2 p9 doc 17, P3 p3) ; cadre « signification du code génétique » | Absent | rg_c1_codon (après le calcul 4³) ou nouvelle diapo avant rg_c2_tableau |
| moyenne | Document de référence | **Électronographie de la transcription (« arbre de Noël »)** : tronc = ADN, branches = ARN de plus en plus longs ; plusieurs ARN polymérases transcrivent le même gène ; le début du gène est du côté des ARN les plus courts (P1 p64, P2 p7 doc 11) | Absent | Après rg_t2_definition ou rg_t4_sens |
| moyenne | Démarche expérimentale | **Marquage avec retour au non radioactif** : noyau marqué greffé dans un cytoplasme non marqué (P1 p62, P2 p5 Goldstein et Plaut), ou cellule marquée 15 min puis lavée et placée 90 min en milieu non radioactif (P4 p9) : c’est ce qui prouve que l’ARN **migre** du noyau au cytoplasme | rg_a3_uracile : 5, 15, 30 min sans étape « milieu non radioactif » (marquage continu ; `marquage.html` non plus) | rg_a3_uracile (protocole et conclusion) |
| moyenne | Exemple | **Albinisme** : tyrosinase (enzyme) non fonctionnelle → pas de mélanine → peau et cheveux clairs (P4 p4) ; cadre RGP2 « albinisme et enzyme de la mélanine », mots_cles « albinisme » | Seulement un QCM de séance (rg_s2_b1) ; aucune diapo, aucun cahier | rg_p4_document (deuxième exemple, deux lignes saine / malade) |
| basse | Notion | **Ribosome** = ARNr + protéines (P2 : 80 % / 20 %), deux sous-unités ; rôle : lire l’ARNm et former les liaisons peptidiques (P1 p67, P2 p8, P3 p4) | rg_r1 : « deux sous-unités » ; ARNr cité seulement comme type d’ARN (rg_a1) | rg_r1_acteurs |
| basse | Condition | La traduction **consomme de l’énergie** (ATP, GTP) (P1 p67, P2 p9 doc 17, P4 p12) | Absent (0 « énergie », 0 « ATP ») | rg_r1_acteurs (une puce ; lien avec le ch1) |
| basse | Document | **Hémoglobine = 4 chaînes** (2 α + 2 β) ; la mutation touche la chaîne β (P1 p60, P2 p4, P4 p5) | Seulement « chaîne β » | rg_p3_proteine |
| basse | Propriétés du code | « Un codon ne code qu’un seul acide aminé » (P3 p3, P4 p11) ; « 61 codons pour 20 acides aminés + 3 stop », « codons synonymes » (P1 p66, P3 p3 ; cadre valeurs_reference) | Seulement dans des réactions (rappels C5_r2, C5_r3, rg_m6) ; pas à l’écran ni au cahier | rg_c5_proprietes |
| basse | Structure | **Nucléotide d’ARN** = acide phosphorique + ribose + base (A, U, C, G) (P1 p63, P2 p6 doc 9, P4 p9 doc 14) | rg_a1 : « un seul brin de nucléotides ; ribose ; A, U, C, G » sans la composition du nucléotide | rg_a1_arn |
| basse | Définition | Mutation **aléatoire**, provoquée par des **agents mutagènes** (UV, rayons X, substances chimiques) (P1 p59, P2 p2, P4 p6-7) ; cadre : agents « donnés par le document » | « spontanée ou provoquée » sans agent nommé (les rayons seulement dans une réaction du rappel C1_r2) | rg_g3b_mutation (un exemple entre parenthèses) |
| basse | Vocabulaire | **Chromosomes homologues** portant les deux allèles au même locus (P2 p3, schéma) ; cadre mots_cles | rg_g2 dit « par paires » ; le mot n’est jamais enseigné, mais le rappel **C1_r3** l’emploie | rg_g2_allele (écran + cahier) |

#### Manques chez un seul professeur

| Priorité | Catégorie | Ce que dit le professeur | Chez nous | Où l’ajouter |
|---|---|---|---|---|
| basse | Expérience | Vert de méthyle (ADN, noyau) – pyronine (ARN, cytoplasme) (P1 p61-62) | Absent | rg_a2_usine (facultatif) |
| basse | Notion | Transcription en trois étapes nommées : initiation, élongation, terminaison (P1 p64) | Étapes décrites sans ces noms (rg_t2, rg_t4) | rg_t4_sens (facultatif ; risque de confusion avec la traduction) |
| basse | Expérience | Bactérie + lactose → ARNm puis β-galactosidase ; la synthèse d’ARNm précède celle de la protéine (P3 p1) | Absent | — |
| basse | Notion | ARNm de courte durée de vie (dégradé) (P2 p8) | Absent | avec le document in vitro |
| basse | Notion | Mutation « stable » ; ARN plus courts que l’ADN (P1 p59, p63) | Absent | — |
| basse | Notion | Caractères spécifiques / individuels (P4 p1) ; variabilité génétique (P2 p3 doc 5) | Absent | — |

#### Présent seulement à l’oral (à écrire)

- **rg_p3_proteine** : « l’hémoglobine [S] forme des fibres : l’hématie devient une faucille » n’est que dans la voix. Les trois professeurs l’écrivent (HbS moins soluble, polymérise en fibres → hématie déformée : P1 p60, P2 p5, P4 p5). C’est le lien entre la molécule et la cellule : à mettre à l’écran et au cahier.
- **rg_a1_arn** : la colonne ADN de la comparaison (deux brins, **désoxyribose**, T) n’est que dans la voix et la légende de l’animation ; l’écran n’a qu’un lead, et le cahier ne parle que de l’ARN. Pourtant le « retrouver » de rg_s2_b2 et le rappel C3_r1 attendent « désoxyribose pour l’ADN ». Écrire le tableau ADN / ARN (brins, sucre, bases, localisation : P2 p6, P3 p2).
- **rg_c2_tableau** : « on écrit l’acide aminé sous le codon » n’est dit qu’à l’oral ; le cahier s’arrête à « on cherche le codon de l’ARNm ».

#### Démonstrations qui sautent des étapes

- **séance rg_s3_b3, exercice (démonstration)** : « Codons : AUG GCU GGC AAA UAA » passe directement à « Met – Ala – Gly – Lys ». Il manque la lecture codon par codon dans le tableau (AUG → Met ; GCU → Ala ; GGC → Gly ; AAA → Lys), avec le découpage à partir de AUG.
- **rg_c3_initiation_stop** : « AUG GAA UUU CCG UAA → Met – Glu – Phe – Pro (arrêt) » est écrit en une seule ligne, sans la correspondance codon par codon.
- **rg_e6_drepanocytose** (démo, cahier, « retrouver » de rg_s6_b1) : « substitution de T par A au triplet 6 » ne dit pas le **rang du nucléotide** (2e nucléotide du triplet 6), alors que la phrase type de rg_e4 l’exige (« du nucléotide X… ») ; « CTC → codon GAG » n’écrit pas l’orientation (brin transcrit 3'→5', ARNm 5'→3'), que la démo de rg_t6 écrit.
- **rg_e5_national** (Q2 et Q3) : seules les lignes ARNm et acides aminés sont écrites. Il manque la ligne « brin non transcrit » (CCC → CTC), l’étape « T → U » et les numéros des triplets. Q3 cite pourtant « 2e nucléotide C par T, triplet 3, brin non transcrit » : les lignes alignées de rg_e3 ne sont pas appliquées.
- **rg_m4_decalage** : délétion, le brin muté est écrit, mais pas l’ARNm muté découpé en codons (seulement dans l’animation et à l’oral) ; insertion, ni la séquence mutée (ATG CTG AGA GTG GCA ATA A) ni son ARNm ne sont écrits à l’écran ni au cahier : on donne directement « Met – Leu – Arg – Val – Ala – Ile ».
- **rg_m2_substitution / rg_m2b_faux_sens** : le codon normal et son acide aminé (CUG = Leu ; GAG = Glu) ne sont pas écrits sur la même ligne que le codon muté. La comparaison codon normal → codon muté → acides aminés reste implicite.

#### Différences de notation ou de convention

| Point | Nous | Eux | Laquelle garder |
|---|---|---|---|
| Codons stop | UAA, UAG, UGA | P3 p3 écrit « TAA, TAG, TGA » (lettres de l’ADN) | Nous : le codon est sur l’ARNm |
| Nucléotide muté de la drépanocytose | « T par A, triplet 6, **brin transcrit** » (CTC → CAC) | P1 p61 « T (HbA) → A (HbS) », sans dire le brin ; P2 p5 et P4 p15 « A remplacé par T » (brin non transcrit, non nommé) ; P4 p15 inverse même Glu et Val | Nous : toujours nommer le brin (et ajouter le rang du nucléotide) |
| Sens de progression de l’ARN polymérase | brin transcrit lu 3'→5', ARNm 5'→3' | P1 p64 « suivant le sens 3'→5' » ; P2 p7 « le long de l’ADN (5'→3') » | Nous (formule du cadre) |
| Forme de l’allèle | allèle normal / allèle muté | allèle (ou caractère) **sauvage** / muté (P1 p58, P2 p2, P4 p3) | Nous ; dire une fois que « sauvage » = normal, car les documents l’emploient |
| Brin transcrit | brin transcrit | aussi « brin matrice » (P1 p64, P2 p7, P3 p2) ; « brin codant » = brin non transcrit (P3 p2) | Nous ; citer « brin matrice » comme synonyme (variante admise par le cadre) ; « codant » seulement si un document l’emploie |
| Définition de la mutation | modification de la séquence des nucléotides d’un gène | « modification de l’information / du matériel génétique » (P1 p59, P2 p2) | Nous (cadre RGP1) |
| Abréviations des acides aminés | Val – His – Glu (tableau, tirets) | ronds « val, his, glu » en minuscules (P1 p60, P2 p4) | Nous (barème) |

#### Hors cadre chez les professeurs (ne pas ajouter)

- Sites P et A du ribosome, translocation (P1 p68-69, P2 p8, p10, P4 p12-13) : hors_cadre de la fiche.
- ARNt en trèfle, boucles, extrémité 3' ACC (P1 p67, P2 p9, P4 p12) : hors_cadre.
- Mg²⁺ et détail des conditions in vitro (P1 p67, P2 p9) : simple donnée de document.
- Séquence qui précède le gène, fixation de l’ARN polymérase (promoteur) (P1 p64) : hors_cadre.
- Méthionine initiale détachée, repliement de la chaîne en forme fonctionnelle (P4 p13) ; « ARNm mature » (P3 p4) : hors_cadre (structures, maturation de l’ARN).
- Génotype (a⁺, b⁻, c⁺) et définition du génotype (P1 p59, p61) : relève de 2.4 (lois statistiques).
- Formule du ribose C₅H₁₀O₅ (P1 p63) et pourcentages ARNr / protéines du ribosome (P2 p8) : détails non exigés.
- Transformation bactérienne de Griffith en introduction (P2 p1) : chapitre 3 (notion de l’information génétique).
