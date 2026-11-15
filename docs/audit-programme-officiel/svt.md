# Audit SVT : notre programme face au cadre officiel (15 novembre 2026)

Référence : cadre de référence de l'examen national du baccalauréat, SVT, filière **Sciences Physiques** (CNEEO/MEN, octobre 2015), transcrit dans `backend/cours 2bac pc/cadres de references 2BAC PC/cadre-de-reference-de-l-examen-national-svt-sciences-physiques (1).json`. Abréviation dans nos fichiers : **CDR-SVT-SP**.

Le cadre PC a **4 domaines de 25 %** :

| Domaine officiel | Sous-domaines | Nos clés (`perimetre.json`) | Cours |
|---|---|---|---|
| 1. Consommation de la matière organique et flux d'énergie | 1.1 réactions libérant l'énergie ; 1.2 muscle strié squelettique ; 1.3 schéma de synthèse | `reactions_responsables_liberation_energie` (1.1), `role_muscle_strie_squelettique` (1.2 + 1.3) | svt_ch1, svt_ch2 |
| 2. Nature de l'information génétique, expression, transmission par la reproduction sexuée | 2.1 notion d'information génétique ; 2.2 synthèse des protéines ; 2.3 méiose, caryotypes, brassages ; 2.4 lois statistiques (Mendel, gènes liés, lié au sexe, carte factorielle) | `notion_information_genetique` (2.1), `relation_gene_proteine` (2.1 fin + 2.2), `mutations_maladies` (2.1 mutation), **`meiose_fecondation` (2.3, nouvelle)**, `lois_mendel` (2.4), `heredite_liee_sexe` (2.4) | svt_ch3, svt_ch4 ; **2.3 et 2.4 sans cours** |
| 3. Utilisation des matières organiques et inorganiques | 3.1 ordures ménagères ; 3.2 pollution ; 3.3 matières radioactives et énergie nucléaire ; 3.4 contrôle de la qualité et de la salubrité | **`ordures_menageres`, `pollution_matieres`, `matieres_radioactives_nucleaire`, `controle_qualite_milieux` (nouvelles, remplacent `pollution_eau`, `pollution_sol_air`, `developpement_durable`)** | aucun cours |
| 4. Phénomènes géologiques des chaînes de montagnes et tectonique des plaques | 4.1 chaînes récentes (subduction, obduction, collision) ; 4.2 déformations ; 4.3 métamorphisme ; 4.4 granitisation ; 4.5 bilan | `chaines_subduction`, `chaines_collision`, `chaines_obduction` (4.1 + 4.2), `metamorphisme` (4.3), **`granitisation` (4.4 + 4.5, nouvelle)** | aucun cours |

Ce que la filière PC n'a PAS (alors que la filière SVT l'a) : génie génétique, génétique humaine (arbres généalogiques, anomalies chromosomiques humaines), génétique des populations, immunologie, physiologie nerveuse.

## Étape 1 — Écarts trouvés dans notre programme

### (a) Ce que nous avions en trop (hors cadre PC)

1. `perimetre.json`, `heredite_liee_sexe` : arbre généalogique, pedigree, conseil génétique, daltonisme, hémophilie, « femme conductrice », hérédité holandrique. La génétique humaine n'est pas au cadre PC (elle est au cadre de la filière SVT) et aucun des 20 sujets PC 2016-2025 n'a d'arbre généalogique (les exemples sont la drosophile, le Diamant mandarin, le poulet, le lapin). **Retiré** ; ajouté comme terme hors programme de la matière.
2. `svt.json`, `heredite_liee_sexe` : « Exemples : daltonisme, hémophilie » et le document type « Arbre généalogique ». **Retiré.**
3. `svt.json`, `level` : « (PC & SVT) » : le programme est celui de la seule filière PC. **Corrigé.**
4. `perimetre.json`, `mutations_maladies` : « mutation germinale transmissible / mutation somatique » (pas dans le cadre). **Retiré.**
5. `perimetre.json`, `reactions_responsables_liberation_energie` : « effet Pasteur » (le cadre dit seulement « déduire les conditions de la respiration et de la fermentation »). **Reformulé** en « conditions : respiration en présence de dioxygène, fermentation en son absence ».
6. `perimetre.json`, `developpement_durable` : la notion « développement durable (trois volets) » n'est pas dans le cadre ; le cadre parle d'« alternatives » et de « préservation ». **Fiche supprimée**, son contenu utile réparti dans 3.2, 3.3 et 3.4.
7. `programme_semestre1.json` : `genie_genetique` figurait dans la liste de travail SVT avec une « décision à valider ». Le cadre officiel confirme qu'il est hors cadre PC. **Sorti de la liste** (`SVT_hors_cadre`, décision confirmée).

### (b) Ce qui manquait

1. **2.3 Méiose et fécondation** (phases de la méiose, caryotypes d'espèces diploïdes, brassages inter- et intrachromosomique, maintien du caryotype, diversité génétique) : pas de clé propre (quelques lignes dans `lois_mendel`) et **pas de cours**. Nouvelle clé `meiose_fecondation` (fiche complète) ; ajoutée à `svt.json`, `prerequis.json`, `programme_semestre1.json` (statut `a_explorer`).
2. **2.4 Lois statistiques** : `lois_mendel` et `heredite_liee_sexe` existaient sans cours. Manquaient dans la fiche : lignée sauvage, hybridation, gène létal (2/3 – 1/3) comme notion. **Ajouté** ; les deux clés ajoutées à `programme_semestre1.json` (`a_explorer`).
3. **3.3 Matières radioactives et énergie nucléaire** : absent de `svt.json`, noyé dans `developpement_durable`. Nouvelle clé `matieres_radioactives_nucleaire`.
4. **3.1 Ordures ménagères** (tri, recyclage, compostage, méthanisation, incinération) : mêlé à la pollution du sol et de l'air. Nouvelle clé `ordures_menageres`.
5. **3.4 Contrôle de la qualité et de la salubrité des milieux** (normes) : mêlé à la pollution des eaux. Nouvelle clé `controle_qualite_milieux`.
6. **4.4 Granitisation** (granite d'anatexie, granite intrusif, métamorphisme de contact) et **4.5 bilan** : absents de `svt.json`, mêlés au métamorphisme. Nouvelle clé `granitisation`.
7. **4.3 Métamorphisme dynamique et thermodynamique**, minéral index, série métamorphique : absents des `topics` de `svt.json`. **Ajouté.**
8. **1.3 Schéma de synthèse du domaine 1** : absent. **Ajouté** à la fiche `role_muscle_strie_squelettique`.
9. `svt.json` n'avait pas le chapitre `notion_information_genetique` (le test `test_chaque_chapitre_du_programme_a_sa_fiche` échouait). **Ajouté** ; le test passe.
10. Domaine 3 et domaine 4 : **aucun cours** ; domaine 2 : 2.3 et 2.4 **sans cours**. C'est la moitié du programme de l'examen (le domaine 3 et le domaine 4 valent chacun 25 %). Ils sont listés pour la suite ; le semestre (S1 ou S2) est à confirmer par l'utilisateur.

### (c) Mal formulé ou mal classé

1. `svt.json`, format d'examen : « Part1 couvre 1 à 3 domaines », « Part2 couvre au moins 3 domaines parmi les 5 », troisième exercice « environnement OU géologie ». Le cadre dit : partie I sur UN domaine, partie II un exercice par domaine restant, donc **les quatre domaines à chaque sujet**. **Corrigé** (`regle_cadre`, `rotation_analysis`) ; ajout du type de question « sériation / classification » prévu par le cadre. Même correction dans `svt_blueprint.json` (`domain_coverage`, `domain_rotation`, `domain_constraint`).
2. `svt.json`, noms des domaines : « Les problèmes environnementaux et la santé humaine » → nom officiel « Utilisation des matières organiques et inorganiques » ; génétique coupée en deux domaines → les deux portent `domaine_officiel: 2`. Les identifiants (`environnement_sante`, `genetique_expression`…) sont gardés car le code des examens blancs les utilise.
3. `svt.json`, `mutations_maladies` : xeroderma et BRCA1 donnés comme exemples à connaître alors que `perimetre.json` les classait hors programme. Ce sont des **documents du national** (xeroderma 2017 R et 2023 R, BRCA1 2019 N) : on les lit dans le document, on ne les apprend pas. Classés ainsi dans `svt.json`, et **retirés des motifs hors programme** de `perimetre.json` (sinon le tuteur était signalé quand il corrigeait ces sujets).
4. `perimetre.json`, `relation_gene_proteine` : contenait la localisation dans le noyau, l'ADN, la réplication et Meselson-Stahl « cité, non refait » — c'est `notion_information_genetique` qui l'enseigne en entier. **Doublon retiré.**
5. `perimetre.json`, `metamorphisme` : granite d'anatexie, granite intrusif et métamorphisme de contact relèvent de 4.4 → **déplacés** dans `granitisation`.
6. `perimetre.json`, `lois_mendel` : la méiose (2.3) et la régulation du cycle cellulaire y étaient rangées → **déplacées** (`meiose_fecondation`, `notion_information_genetique`).
7. `perimetre.json`, `mutations_maladies` : « trisomie, translocation » classés comme « relève de la méiose » → la trisomie relève de la génétique humaine, hors cadre PC : **terme générique de la matière**.
8. `perimetre.json`, `notion_information_genetique` : quatre motifs écrits avec `\b` en JSON (caractère « retour arrière ») au lieu de `\\b` : « ligase », « SSB », « C1' », « CDK » n'étaient **jamais détectés**. **Corrigé.**
9. `perimetre.json`, valeur de l'énergie d'une mole de glucose : 2 870 kJ alors que la fiche du cadre et le cours prennent 2 860 kJ. **Aligné** sur 2 860 kJ (« donnée par l'énoncé »).
10. Termes hors programme de la matière **ajoutés** : génie génétique, génétique humaine, immunologie (avec `dire_plutot`).
11. `cadre_reference_2bac_pc.json`, fiches SVT : leurs notes disaient « texte officiel du cadre absent du dépôt, capacités reconstruites, à confirmer ». Les capacités LE1-LE10, MSS1-MSS13, NIG1-NIG11 et RGP1-RGP10 ont été **relues contre le texte officiel** : toutes y correspondent. Notes et sources mises à jour.
12. `curriculum_svt_2bac_pc.yaml` : poids 30 % (génétique) et 20 % (environnement) → **25 % chacun** ; leçons 2.4 (lois statistiques) et 3.4 (contrôle de la qualité) ajoutées.
13. `prerequis.json` : carte des chapitres SVT alignée sur les nouvelles clés (et `notion_information_genetique` ajoutée).

Contrôle : `pytest app/tests/test_perimetre.py app/tests/test_prerequis.py` → 18 passés (un échec existait avant l'audit).

## Étape 2 — Les cours de SVT, une fois le programme conforme

Quatre cours relus diapositive par diapositive (écran, voix, questions, réactions préparées, cahier, rappels, séances, schémas à légender, simulations). Toutes les clés `correct` ont été vérifiées par script contre les réactions « juste ». Aucun `speech_text.mixed` (voix des diapositives) n'a été changé ; aucun texte de schéma à légender n'a été changé.

| Cours | Notions du cadre | Corrections | Pistes de voix à refaire |
|---|---|---|---|
| svt_ch1 Libération de l'énergie | 1.1, 1.3 | 22 | 1 |
| svt_ch2 Muscle strié squelettique | 1.2 | 27 | 5 |
| svt_ch3 Notion de l'information génétique | 2.1 | 54 (28 de fond + 26 préfixes « Bonne réponse » dans des réactions de mauvaise réponse) | 4 |
| svt_ch4 Expression de l'information génétique | 2.1 fin, 2.2 | 14 (dont 1 dans la simulation `paire_homologues.html`) | 3 |

Aucun cours ne sort du cadre officiel PC : pas de méiose ni de Mendel enseignés (la simulation `paire_homologues.html` écrivait « A et B dominent O ; codominants » : retiré, c'est 2.4), pas de génie génétique, pas de génétique humaine, pas de physiologie nerveuse, complexes I-IV seulement « à lire » dans un document. Les erreurs trouvées étaient surtout dans les **réactions préparées** (verdicts inversés, mauvais mécanisme), rarement à l'écran.

### Voix à refaire (pistes Bodi existantes dont le texte a changé)

- **svt_ch1** : `le_e3_sans_o2` réaction `q.1.2` (`le_e3_sans_o2__q_1_2_v12.mp3`).
- **svt_ch2** : `ms_g3_glissement` réaction `q.1.juste` ; `ms_x4_restitution` réactions `q.1.2` et `q.2.1` ; compétence C9 rappel r3 réaction `0.2` (`rappel_C9_r3_0_2_v12.mp3`) ; `ms_r4_fermentation` énoncé lu (`enonce_audio`).
- **svt_ch3** : `ig_r3_g1` réaction `q.2.2` ; `ig_m7_schema` réaction `q.0.2` ; `ig_l5_gurdon` réaction `q.2.1` ; `ig_r12_conservation` réaction `q.0.1`.
- **svt_ch4** : `rg_t6_bareme` réactions `q.2.juste` et `q.1.1` ; séance `rg_s6_b1` exercice réaction `0.1` (piste `bloc_rg_s5_b2__ex_0_1_v10.mp3`).

Soit **13 pistes**. D'autres `parole` ont changé dans la réserve de fin de cours et des exercices de bloc, qui n'ont pas encore de piste (détail par cours ci-dessous).

### Cours Audit : cours SVT 1, « Libération de l'énergie emmagasinée dans la matière organique »

Fichier : `backend/data/courses/svt_ch1_reactions_responsables_liberation_energie.json` (56 diapositives, 10 compétences, 5 séances).
Références : cadre officiel PC, sous-domaines 1.1 et 1.3 ; fiches `perimetre.json` et `cadre_reference_2bac_pc.json` (LE1 à LE10, hors_cadre, decisions) ; examens nationaux PC 2016-2025.
Simulations relues : `frontend/public/media/simulations/svt/reactions_responsables_liberation_energie-tableau/*.html` (17 pages, plus commun.js et peinture.js).


#### (a) Correspondance avec le cadre officiel

| Partie / compétence | Diapositives | Notion du cadre officiel (1.1 / 1.3) |
|---|---|---|
| Ouverture (C1) | le_o1, le_p1, le_p2, le_o2 | Rappel des prérequis (cellule, glucose, photosynthèse : règle 34 « départ de zéro »). Ces diapositives introduisent « consommation de la matière organique et flux d'énergie » (domaine 1). Elles ne posent pas de notion nouvelle hors cadre. |
| I. ATP (C1, LE1) | le_a1, le_a2 | Le rôle de l'ATP, exigé par l'objectif « bilan énergétique » (ATP = unité des bilans). Le point clé du domaine 1 parle aussi du « rôle de l'ATP ». |
| II. Respiration / fermentation (C2, LE2) | le_e1, le_e2, le_e3, le_e4 | Notion de respiration ; notion de fermentation ; « comparer… », « déduire les conditions… » |
| III. Transporteurs et glycolyse (C3, LE3) | le_t1, le_t2, le_g1, le_g2, le_g3 | Étapes essentielles de la glycolyse ; bilan énergétique de la glycolyse |
| IV. Mitochondrie (C4, LE4) | le_m1, le_m2, le_m2b, le_m3, le_m4 | Structure et ultrastructure de la mitochondrie ; « relation respiration / structures cellulaires » |
| V. Matrice (C5, LE5) | le_k1 à le_k5 | Étapes essentielles du cycle de Krebs ; bilan du cycle de Krebs |
| VI. Chaîne respiratoire (C6, LE6) | le_c1 à le_c10b | Chaîne respiratoire et phosphorylation oxydative ; « appliquer le raisonnement scientifique » (cyanure, vésicules) |
| VII. Fermentations (C7, LE7) | le_f1, le_f2 | Étapes essentielles de la fermentation ; bilan énergétique de la fermentation |
| VIII. Bilans et rendements (C8, LE8) | le_r1, le_r2, le_r3 | Bilan énergétique de la respiration ; rendement énergétique ; comparer les bilans |
| IX. Cas types (C9, LE9) | le_x1 à le_x3 (et e2, m1, m4, c1, c10) | Objectifs : exploiter des données, raisonnement scientifique |
| X. Bilan (C10, LE10) | le_e4, le_x4, le_b1, le_b2 | 1.3 : schéma de synthèse ; « représenter graphiquement », « schéma de synthèse du bilan » |

Aucune partie n'est hors cadre. Aucun terme de `hors_cadre` / `termes_hors_programme` n'apparaît dans l'écrit, la voix, les réactions ou les simulations : j'ai cherché par regex complexes I-IV, ubiquinone, cytochrome, intermédiaires de Krebs, navettes, 30/32 ATP, rotor, force proton-motrice, GTP, lactate, fructose, hexokinase, découplants. Les noms CI à CV n'apparaissent que dans le_c8_national et dans la vue « examen » de chaine.html, présentés comme « donnés par le sujet, on ne les apprend pas ». C'est conforme à la décision de la fiche.

Les bilans chiffrés sont justes partout (écran, cahier, voix, simulations) :
- glycolyse : 4 − 2 = 2 ATP, 2 NADH,H+ ;
- acétyl-CoA : 1 NADH,H+ et 1 CO2 par acide pyruvique ;
- Krebs : 2 CO2, 3 NADH,H+, 1 FADH2 et 1 ATP par tour, × 2 par glucose ;
- au total 10 NADH,H+ et 2 FADH2, soit 38 = 2 + 2 + 30 + 4 (36 « si l'énoncé le dit ») ;
- fermentation : 2 ATP ;
- rendements : 40,5 % et 2,13 % (2860 kJ, 30,5 kJ).

Les légendes de la mitochondrie sont justes : membranes externe et interne, crêtes, espace intermembranaire, matrice, sphères pédonculées tête côté matrice. Les sens des protons et l'expérience des vésicules (sphères vers l'extérieur, intérieur acide → ATP) sont justes. Toutes les clés `correct` des QCM et vrai/faux concordent avec les réactions préparées « juste » (vérifié par script).

#### (b) Corrections

| Diapositive (id) | Champ | Avant → après | Raison |
|---|---|---|---|
| le_e3_sans_o2 | concentration.reponses.q.1.2.ecrit | « L'eau est produite dans la respiration comme dans la fermentation, donc elle ne prouve rien » → « L'eau est un produit de la respiration, pas de la fermentation : elle ne prouve donc pas que la levure fermente » | Erreur scientifique : la fermentation alcoolique ne produit pas d'eau (C6H12O6 → 2 C2H5OH + 2 CO2). |
| le_e3_sans_o2 | concentration.reponses.q.1.2.parole | « l'eau كتخرج في la respiration وفي la fermentation بجوج » → « l'eau كتخرج في la respiration، ماشي في la fermentation » | Même erreur, dans la voix (piste audio à refaire). |
| le_g3_bilan | concentration.reponses.e0s2.1.juste.ecrit | « Vrai : la glycolyse produit 4 ATP… La réponse « Faux » est correcte. » → « Juste : … » | La réaction commençait par « Vrai » alors que l'affirmation (« 4 ATP nets ») est fausse et que la bonne réponse est Faux. C'était contradictoire. La voix était juste. |
| le_c3_decharge | reponses.q.0.1.ecrit | « à T un » → « à T1 » | Le nombre était écrit en toutes lettres (forme orale) dans un texte affiché. |
| le_c3_decharge | reponses.q.0.2.ecrit | « cédés à T un » → « cédés à T1 » | Même raison. |
| le_c3_decharge | reponses.q.1.1.ecrit | « au complexe T un » → « au transporteur T1 » | Même raison. Le cours dit « transporteur T1 » : le mot « complexe » associé à un numéro est la forme que la fiche demande de ne pas faire apprendre. |
| le_c3_decharge | reponses.q.1.2.ecrit | « au complexe T un » → « au transporteur T1 » | Même raison. |
| le_k5_fois_deux | screen_content.bullets[3] | « L'énergie n'est pas encore dans l'ATP : elle est portée par NADH,H+ et FADH₂. » → « Seuls 4 ATP sont formés jusque-là : l'essentiel de l'énergie est porté par NADH,H+ et FADH₂. » | Inexact : 4 ATP sont déjà formés (2 glycolyse + 2 Krebs). La phrase est alignée sur le cahier (« surtout portée »). |
| le_x1_restitution | reponses_fin_de_cours.e2s0.1.2.ecrit | « La bonne réponse est Faux : … mais le verdict imposé est Faux. » → « La bonne réponse est Vrai : … seule porte de retour… ne confonds pas avec la chaîne respiratoire… » | Le verdict était inversé : l'affirmation « au niveau de la sphère, les protons vont de l'espace vers la matrice » est VRAIE (clé correct: true). |
| le_x1_restitution | reponses_fin_de_cours.e2s0.1.2.parole | « الجواب الصحيح هو faux… » → « الجواب الصحيح هو vrai… » | Même erreur, dans la parole (pas encore de piste audio : réserve). |
| le_x1_restitution | reponses_fin_de_cours.e2s0.1.1.ecrit | « Mais le verdict est faux. » → « Mais l'affirmation est juste, et tu as répondu Faux. » | La phrase était ambiguë : on pouvait la lire comme « l'affirmation est fausse ». |
| le_x1_restitution | reponses_fin_de_cours.e2s0.1.1.parole | « ولكن الverdict هنا هو faux » → « ولكن l'affirmation صحيحة، ونتا جاوبتي faux » | Même ambiguïté (pas de piste audio). |
| le_x1_restitution | reponses_fin_de_cours.e2s1.0.1.ecrit | « réduit en NADH » → « réduit en NADH,H+ » | Notation du cadre (NADH,H+), employée partout ailleurs dans le cours. |
| le_x1_restitution | reponses_fin_de_cours.e2s1.0.2.ecrit | « réduit en NADH » → « réduit en NADH,H+ » | Même raison. |
| le_x1_restitution | reponses_fin_de_cours.e2s1.1.juste.ecrit | « réduit en NADH » → « réduit en NADH,H+ » | Même raison. |
| le_x1_restitution | reponses_fin_de_cours.e2s2.0.2.ecrit | « en pyruvate… le pyruvate » → « en acide pyruvique… l'acide pyruvique » | Cohérence : le cours n'enseigne que « acide pyruvique » (mot du cadre et des corrigés) ; « pyruvate » n'est jamais introduit. |
| le_x1_restitution | reponses_fin_de_cours.e2s2.1.juste.ecrit | « le pyruvate » → « l'acide pyruvique » | Même raison. |
| compétence C5 (rappel C5_r2) | rappels[1].reponses.0.2.ecrit | « décarboxylation du pyruvate » → « décarboxylation de l'acide pyruvique » | Même raison. L'écrit seul est modifié : la voix ne dit pas « pyruvate ». |
| le_e2_decrire | reponses_fin_de_cours.e0.0.1.ecrit | « Regarde le tableau » → « Regarde la courbe » | Le document de la diapositive est une courbe ExAO, pas un tableau. |
| le_e2_decrire | reponses_fin_de_cours.e0.0.1.parole | « رجع لجدول القياسات » → « رجع ل la courbe » | Même raison (pas de piste audio : réserve). |
| le_f2_alcoolique | speech_text.fr | « Le CO2 n'existe que dans la fermentation alcoolique. » → « Des deux fermentations, seule l'alcoolique dégage du CO2 ; la lactique n'en dégage pas. » | Faux tel qu'écrit, puisque la respiration rejette du CO2. La voix (mixed) est juste (« ماشي فla lactique »). Le hash de la piste porte sur `mixed`, donc aucune voix n'est à refaire. |
| le_e1_mesurer | speech_text.fr | « On va injecter du glucose : prédis ce que devient le dioxygène. » → « On va injecter du glucose avec la seringue. » | Règle « pas de prédiction » (13 novembre 2026). La voix (mixed) ne demande pas de prédiction : le texte écrit est aligné sur la voix. Aucune voix n'est à refaire. |

#### (c) Voix à refaire

- **le_e3_sans_o2, réaction préparée `concentration.reponses.q.1.2`** : la `parole` a changé ; la piste `/media/audio/courses/svt_ch1_reactions_responsables_liberation_energie/reponses/le_e3_sans_o2__q_1_2_v12.mp3` dit encore « l'eau dans la respiration et dans la fermentation ». Il faut la régénérer. Le champ audio est conservé.
- Paroles modifiées **sans piste audio** (réserve `reponses_fin_de_cours`, non voisée aujourd'hui), à voiser le jour où la réserve le sera :
  - le_x1_restitution e2s0.1.1 et e2s0.1.2 ;
  - le_e2_decrire e0.0.1.
- Aucun `speech_text.mixed` n'a été modifié. Les deux changements de `speech_text.fr` ne touchent aucune piste.

#### (d) Points à trancher (non modifiés)

1. **le_k5_fois_deux, voix** : « l'énergie باقي ماشي فl'ATP، راها فles transporteurs ». C'est une simplification (4 ATP sont déjà formés). L'écrit est corrigé (« l'essentiel »). Faut-il refaire la voix ?
2. **le_e1_mesurer, titre** : « Des levures et du glucose : que va-t-il se passer ? » est une formulation de prédiction, alors que la règle est « pas de prédiction ». Le classifieur de questions lit ce titre. Il pourrait devenir « Des levures et du glucose : ce qu'on mesure ».
3. **C7 (fermentations) n'est jamais évaluée pendant le cours** : le bloc le_s4_b3 (f1, f2, r1, r2) porte sa seule question sur le_r2 (rendement). C7 n'est évaluée que par la réserve (le_f2), les rappels et l'exercice de bloc, qui n'est pas joué aujourd'hui. Faut-il déplacer la question du bloc, ou ajouter une question sur le_f2 ?
4. **« ATP synthase » employé avant d'être enseigné** : les réactions de l'exercice du bloc le_s3_b2 (sphère tête en bas) disent « (ATP synthase) » alors que le terme n'est introduit qu'à le_c7. Ce ne sont que des réactions, et l'exercice de bloc n'est pas joué. C'est à corriger si cet exercice est un jour joué avant le_c7.
5. **Exercice de bloc en double** : le_s4_b2 (vésicules) reprend mot pour mot l'exercice de le_s4_b1 (substance X qui bloque les sphères). Ce n'est pas faux, mais c'est redondant. Un exercice sur les vésicules (pH égaux, sans sphères) serait plus cohérent.
6. **le_c6_protons, énoncé « (national 2024) »** : la question sur le sens des protons vient du sujet 2024 **rattrapage**. On peut préciser « 2024 R », ce qui demanderait de vérifier `enonce_dit` et sa piste.
7. **Diapositives d'ouverture (le_o1, le_p1, le_p2, le_o2) rattachées à C1 / LE1 (ATP)** : ce sont des rappels de prérequis (cellule, glucose, photosynthèse), autorisés par la règle 34. Leur cadre_id n'est pourtant pas l'ATP. Il n'y a pas d'erreur de contenu, seulement un rattachement de suivi discutable.
8. **le_x2_qui_respire** : les données (3,5 / 2,0 L/min ; 2 / 9 mmol/L) sont construites pour l'exercice et ne sont pas tirées d'un sujet. C'est acceptable comme exercice type ; je le signale seulement.

#### (e) Total

**22 corrections** (22 champs modifiés) :
- 3 erreurs scientifiques : eau dans la fermentation, verdict vrai/faux inversé, « énergie pas encore dans l'ATP » ;
- 4 contradictions ou ambiguïtés de réaction ou de texte : « Vrai : » sur une réponse Faux, « verdict est faux », « tableau » au lieu de « courbe », « CO2 n'existe que… » ;
- les autres corrections portent sur la notation et la cohérence (T1, NADH,H+, acide pyruvique) et sur la règle « pas de prédiction ».

Les champs touchent 8 diapositives (le_e3, le_g3, le_c3, le_k5, le_x1, le_e2, plus le_f2 et le_e1 pour `speech_text.fr`) et 1 rappel (C5_r2). Il y a **1 piste audio à refaire**. Les simulations ne contiennent ni erreur ni terme hors programme : aucune n'a été modifiée.

### Cours Audit : svt_ch2_role_muscle_strie_squelettique

Fichier corrigé : `backend/data/courses/svt_ch2_role_muscle_strie_squelettique.json`. Aucune simulation n'a été modifiée.
Référence : cadre officiel PC, sous-domaines 1.2 et 1.3, plus les fiches `perimetre.json` et `cadre_reference_2bac_pc.json` (MSS1 à MSS13).

Ce qui a été vérifié :
- les 59 diapositives (titre, écran, voix fr et mixed, questions, réactions, cahier, figures, légendes, observation) ;
- les 9 compétences et leurs rappels ;
- les 16 blocs (cahier, figures, retrouver, exercice et leurs réactions) ;
- les 14 simulations HTML/JS (textes affichés, `ce_qui_se_voit`, valeurs).

Toutes les clés `correct` et `bonne` (questions, exercices, rappels, blocs, fin de cours) sont justes.

Aucun terme hors programme n'apparaît. Ont été cherchés : nerf, synapse, potentiel d'action, jonction neuromusculaire, acétylcholine, ryanodine, titine, rigor, VO₂max, et les autres mots `hors_cadre` / `termes_hors_programme`. Le muscle est bien excité par des électrodes et un excitateur. Les autres mots relevés sont autorisés :
- glycolyse : vue au chapitre 1 ;
- cyanure : `donne_par_le_document`.

#### (a) Correspondance parties / compétences → cadre officiel

| Partie (diapositives) | Compétence | Notion du cadre officiel PC (1.2 / 1.3) |
|---|---|---|
| Ouverture (o1, o2) | C6 | 1.2 « origine de l'énergie nécessaire à la contraction » (rappel ATP du 1.1) |
| I. Secousse (s1–s6) | C1 (MSS1) | « Le myogramme : la secousse musculaire » ; objectif « analyser et interpréter les myogrammes » |
| II. Intensité (i1, i2) | C2 (MSS2) | myogramme, analyser les myogrammes (seuil, recrutement) |
| III. Fusion, tétanos, fatigue (f1–f7) | C2 (MSS2) | « tétanos parfait et tétanos imparfait » |
| IV. Chaleur et consommation (t1–t4) | C3 (MSS3, MSS4) | « phénomènes thermiques et chimiques (consommation du O₂ et du glucose…) » ; « déterminer / relier ces phénomènes à la contraction » |
| V. Du muscle au sarcomère (u1–u8) | C4 (MSS5, MSS6) | « structure et ultrastructure du muscle » ; « structure moléculaire des myofilaments » |
| VI. Glissement (g1–g3) | C5 (MSS7) | « comparer l'état d'une fibre au repos et au cours d'une contraction » |
| VII. Mécanisme Ca²⁺ / ATP (c1–c8) | C6 (MSS8, 9, 12) | « mécanisme de la contraction » ; « origine de l'énergie » ; raisonnement scientifique ; « schémas du mécanisme » |
| VIII. Régénération de l'ATP (r1–r8) | C7 (MSS10), C8 (MSS11) | « voies métaboliques de régénération de l'ATP » ; « relation voies de régénération / type d'effort » |
| IX. Rédiger comme au bac (x1–x4) | C9 (MSS13) | objectif « appliquer le raisonnement scientifique » (décrire, comparer, hypothèse, vérifier) |
| X. Bilan (b1, b2) | C9 | fiche « Ce qu'il faut retenir » et carte du chapitre ; 1.3 seulement en partie (voir le point 6 de la partie d) |

Le bilan (9 blocs) et la carte (8 branches) reprennent bien les compétences C1 à C9. Chaque compétence est travaillée puis évaluée :
- C1 : s2, s6 ;
- C2 : f1, f4, f7 ;
- C3 : t3 (observation), t4 ;
- C4 : u3, u7 et deux schémas à légender ;
- C5 : g3 ;
- C6 : c1b, c4, c8 ;
- C7 : r4 ;
- C8 : r8 ;
- C9 : x3, x4.

#### (b) Corrections

| Diapositive (id) | Champ | Avant → après | Raison |
|---|---|---|---|
| ms_f1_isolees | reponses.q.1.2.ecrit | « Les deux **excitations** ont la même amplitude : la seconde arrive après la fin de la première » → « Les deux **secousses** ont la même amplitude : la seconde excitation arrive après la fin de la première secousse » | Une excitation a une intensité, pas une amplitude. La voix disait juste. |
| ms_u7_molecules | reponses.q.1.2.ecrit | « Le Ca²⁺ et la troponine se fixent sur la troponine du filament fin » → « Le Ca²⁺ se fixe sur la troponine, une protéine du filament fin : ni l'un ni l'autre ne se fixe sur la tête de myosine » | Phrase fausse (la troponine ne se fixe pas sur elle-même). |
| ms_g3_glissement | reponses.q.1.juste.ecrit | « la zone H raccourcit car **les filaments de myosine se rapprochent** » → « …car les extrémités des filaments d'actine se rapprochent du centre du sarcomère » | Erreur : la myosine ne bouge pas, c'est l'actine qui avance (le cours le dit en g3). |
| ms_g3_glissement | reponses.q.1.juste.parole | « les filaments د la myosine كيتقربو لبعضياتهم » → « les filaments d'actine كيتقربو من الوسط ديال le sarcomère » | Même erreur dans la voix. |
| ms_x4_restitution | reponses.q.1.2.ecrit | « c'est la chaleur **immédiate** » → « elle est liée à la chaleur initiale, pas à la chaleur retardée » | Le terme du cours et du cadre est « chaleur initiale ». |
| ms_x4_restitution | reponses.q.1.2.parole | « كيسمى la chaleur immédiate » → « مرتبط ب la chaleur initiale » | Même raison. |
| ms_x4_restitution | reponses.q.2.1.ecrit | « La fermentation lactique **consomme l'ATP** » → « La fermentation lactique régénère l'ATP sans dioxygène : elle n'est pas à l'origine de la chaleur retardée » | Faux : la fermentation produit 2 ATP par glucose. |
| ms_x4_restitution | reponses.q.2.1.parole | « كتستعمل ATP » → « كتجدد l'ATP بلا dioxygène » | Même erreur dans la voix. |
| ms_r8_inhibiteurs | reponses.q.0.1.ecrit | La réaction de niveau 1 donnait la réponse (« Réponse B… ») → un indice sans la réponse (glycolyse bloquée → pas de fermentation ; quelle réserve chute ?) | Le niveau 1 ne doit pas donner la réponse. Le texte écrit ne correspondait pas à la voix, qui donnait un indice. |
| ms_x4_restitution | reponses_fin_de_cours.e1.0.2.ecrit | « fusion complète… quand la 2ᵉ excitation tombe **avant la fin du relâchement**, pendant la contraction » → « …tombe pendant la phase de contraction de la première » | « Avant la fin du relâchement » décrit la fusion incomplète : contradiction. |
| ms_x4_restitution | reponses_fin_de_cours.e1.0.2.parole | « قبل ما يسالي le relâchement » → « قبل ما يبدا le relâchement » | Même erreur. |
| ms_x4_restitution | reponses_fin_de_cours.e1.1.1.ecrit | « Vérifie si la première a déjà atteint le tétanos… » → indice : compter les excitations (deux, alors qu'un tétanos demande une série) | Texte sans sens scientifique. |
| ms_x4_restitution | reponses_fin_de_cours.e1.1.1.parole | Même texte en darija → nouvel indice : compter les excitations | Même raison. |
| ms_x4_restitution | reponses_fin_de_cours.e1.1.2.ecrit | « Le tétanos imparfait correspond à des excitations très rapprochées, avant la fin du relâchement » → « …demande une série d'excitations, chacune pendant le relâchement de la précédente. Ici deux excitations : fusion incomplète » | Définition fausse : elle omet la série, et c'est le piège enseigné par le cours. |
| ms_x4_restitution | reponses_fin_de_cours.e1.1.2.parole | Même erreur (« la deuxième excitation… ») → version juste en darija | Même raison. |
| ms_x4_restitution | reponses_fin_de_cours.e3s0.1.juste.ecrit | « **Vrai** : la bande sombre ne raccourcit pas » → « Bonne réponse, l'affirmation est fausse : … » | L'élève a répondu Faux, qui est la bonne réponse. Commencer par « Vrai » contredisait la clé. |
| ms_x4_restitution | reponses_fin_de_cours.e3s1.1.1.ecrit | « Faux. Ce qui est juste… » → « Ce n'est pas la bonne réponse. Ce qui est juste… » | L'affirmation est vraie : « Faux. » en tête était ambigu et contraire à la clé. |
| ms_x4_restitution | reponses_fin_de_cours.e3s1.1.2.ecrit | « La bonne réponse est **Faux** » → « La bonne réponse est **Vrai** … » | Contraire à la clé (`correct: true`). |
| ms_x4_restitution | reponses_fin_de_cours.e3s1.1.2.parole | « الجواب الصحيح هو faux، يعني غالط » → « الجواب الصحيح هو vrai، يعني صحيح » | Même erreur. |
| bloc ms_s2_b2 | exercice.reponses.0.2.ecrit | « C'est une fusion incomplète : un tétanos imparfait… il faudrait une excitation avant 0,05 s » → « Chaque excitation de la série tombe pendant le relâchement de la précédente : tétanos imparfait, plateau dentelé… chaque excitation devrait tomber pendant la contraction de la précédente (avant 0,05 s) » | Confondait fusion (deux excitations) et tétanos (série), le piège même que le cours enseigne. |
| bloc ms_s2_b2 | exercice.reponses.1.juste.ecrit | « fusion incomplète = tétanos imparfait » → « c'est une série : tétanos imparfait (plateau dentelé) » | Même raison. |
| bloc ms_s2_b2 | exercice.reponses.1.juste.parole | « السمية هي la fusion incomplète، يعني tétanos imparfait » → « …و هي série، السمية هي le tétanos imparfait، plateau dentelé » | Même raison. |
| bloc ms_s2_b2 | exercice.reponses.2.2.ecrit | « tétanos imparfait (fusion incomplète) » → « tétanos imparfait (plateau dentelé) » | Même raison. |
| bloc ms_s2_b2 | exercice.reponses.2.2.parole | « يعني la fusion incomplète » → « plateau dentelé » | Même raison. |
| compétence C9, rappel r3 | reponses.0.2.ecrit | Exemple de déduction « donc l'organisme consomme plus de dioxygène à l'effort » → « donc la respiration augmente à l'effort » | L'exemple redisait le constat : c'était une description, pas une déduction (faux dans une compétence de méthode). |
| compétence C9, rappel r3 | reponses.0.2.parole | Même remplacement | Même raison. |
| ms_r4_fermentation | question.enonce_dit | « …combien de molécules d'ATP, **et quel est le produit final de cette réaction** ? » → « …combien de molécules d'ATP ? » | L'énoncé lu demandait une seconde chose, absente des options (36 / 1 / 2 ATP). |

#### (c) Voix à refaire

Pistes Bodi existantes dont le texte a changé :
1. `ms_g3_glissement` : `concentration.reponses.q.1.juste` (piste `ms_g3_glissement__q_1_juste_v12.mp3`)
2. `ms_x4_restitution` : `concentration.reponses.q.1.2` (piste `ms_x4_restitution__q_1_2_v12.mp3`)
3. `ms_x4_restitution` : `concentration.reponses.q.2.1` (piste `ms_x4_restitution__q_2_1_v12.mp3`)
4. Compétence C9, `rappels[2].reponses.0.2` (piste `rappel_C9_r3_0_2_v12.mp3`)
5. `ms_r4_fermentation` : `question.enonce_dit`, à revoicer dans `enonce_audio` (`enonce_ms_r4_fermentation_q_v11.mp3`)

Paroles modifiées sans piste audio (à voicer quand l'étape de fin de cours le sera) :
- `ms_x4_restitution.reponses_fin_de_cours` : `e1.0.2`, `e1.1.1`, `e1.1.2`, `e3s1.1.2` ;
- `seances[1].blocs[1]` (ms_s2_b2) : `exercice.reponses.1.juste` et `2.2`.

Aucun `speech_text` n'a été modifié.

#### (d) Points à trancher (non modifiés)

1. **ms_x4_restitution, `q.2.2` (écrit et voix)** : la réaction dit « la fermentation lactique correspond à la chaleur initiale ». Le cours (r3, `chaleur.html`) attribue la chaleur initiale à l'hydrolyse de l'ATP et à la phosphocréatine. Certains manuels parlent de « réactions anaérobies » en général. C'est défendable, mais ce n'est pas cohérent avec le cours. À harmoniser si l'on veut, par exemple : « la fermentation est anaérobe : elle ne produit pas la chaleur retardée ».
2. **ms_f7_fatigue, `q.1.2`, et rappels C2** : « la latence n'est pas un critère de fatigue ». Certains documents montrent une latence qui s'allonge avec la fatigue. Ce n'est pas faux pour ce cours (les deux signes retenus sont l'amplitude et le relâchement), mais la phrase est absolue.
3. **ms_r2_phosphocreatine** : « (myokinase) » est écrit sur l'écran sans être présenté. Le mot est `tolere_si_annonce` dans le cadre : soit l'annoncer, soit le retirer de la puce.
4. **Unité des intensités d'excitation en mV** (ms_i1, `intensite.html`, exercice du bloc ms_s1_b3) : les documents de manuels utilisent souvent le volt. Ce n'est pas faux, à vérifier sur les documents d'examen.
5. **Durée de la chaleur retardée** « 1 à 2 minutes » (t2, cahier, `chaleur.html`) : le cadre ne donne pas de valeur, les documents classiques disent « plusieurs minutes ». Ordre de grandeur acceptable.
6. **Sous-domaine 1.3** (schéma de synthèse consommation de matière organique et flux d'énergie dans la cellule) : la carte ms_b2 ne couvre que le chapitre, sans relier respiration/fermentation (ch1) et contraction (ch2). Il faut décider si ce schéma bilan doit vivre ici ou dans un bilan du domaine 1.
7. **Organisation** :
   - la séance 4 compte 4 blocs (la règle est 3) ;
   - le bloc ms_s3_b2 compte 5 diapositives ;
   - l'exercice du bloc ms_s4_b2 est identique à celui de ms_s4_b1 (fibres glycérinées). Le rôle du Ca²⁺ et la rotation n'y sont pas évalués, même si la question de c4 le fait ;
   - la ligne de cahier 0 de ms_s4_b2 répète la conclusion du bloc précédent.
8. **Détails de réactions** :
   - « tout ou rien » (C2, `rappels[2].reponses.1.1`) et « ponts d'union » (C4, `rappels[2].reponses.1.2`) ne sont pas enseignés dans le cours ;
   - les réactions de niveau 2 de ms_c1b commencent par « Bonne réponse : … » après une mauvaise réponse. C'est la convention « la bonne réponse est », mais on peut la lire comme un compliment ;
   - `ms_g3_glissement.question.enonce_dit` est formulé bizarrement (« la phrase continue sur la diapositive qui s'appelle… »).
9. **Fichiers hors de mon périmètre** : `git diff --stat` montre d'autres fichiers modifiés que je n'ai pas touchés (svt_ch1, svt_ch4, `perimetre.json`, `svt.json`, `paire_homologues.html`). Ils viennent d'autres agents. Mon diff ne touche que les 27 lignes ci-dessus.

#### (e) Total

**27 champs corrigés**, dans 1 seul fichier :
- 16 réactions (écrit, parole ou les deux) ;
- 1 énoncé dit.

Voix : 5 pistes existantes à refaire, 6 paroles modifiées sans piste. Aucune simulation n'a été modifiée.

### Cours Audit du cours SVT ch3 : Notion de l'information génétique (2e Bac PC BIOF)

Fichier corrigé : `backend/data/courses/svt_ch3_notion_information_genetique.json`. Simulations relues, sans modification : `frontend/public/media/simulations/svt/notion_information_genetique-tableau/*.html`.
Référence : cadre officiel SVT PC, sous-domaine 2.1 « Notion de l'information génétique ».

#### (a) Correspondance parties / compétences → cadre officiel 2.1

| Partie (activité) | Compétence | Connaissance du cadre 2.1 |
|---|---|---|
| Ouverture, I (amibe, acétabulaire : section et greffe, Gurdon) | C1 | « La localisation de l'information génétique dans le noyau de la cellule » ; objectif « Déduire la localisation... à partir de l'analyse de données » |
| II (chromosomes, mitose depuis zéro, noyau, chromatine, nucléosome, chromatides) | C2 (et C4 pour p2, p3) | « Composition et structure des chromosomes » ; « relation entre les chromosomes et la molécule d'ADN » |
| III (cycle, q → 2q → q, durées) | C3 | « Le cycle cellulaire » ; « Construire et représenter le cycle cellulaire et déduire son rôle dans la stabilité de l'information génétique » |
| IV (phases de la mitose, animale/végétale, photo, schéma 2n = 4, légender) | C4 | « Les phases de la mitose chez la cellule végétale et la cellule animale » ; « Décrire et identifier les phases » ; « Réaliser des schémas en relation avec les phases de la mitose » |
| V (Griffith, Avery) | C5 | « La nature chimique du matériel génétique » ; « Déterminer la nature chimique... à partir de l'exploitation de données expérimentales » |
| VI (nucléotide, Chargaff, brins antiparallèles, double hélice, brin complémentaire, légender l'ADN) | C6 | « Composition et structure... de l'ADN » ; « schémas en relation avec la nature chimique du matériel génétique » |
| VII (Meselson et Stahl, thymidine, yeux, ADN polymérase, conservation) | C7 | « Mécanisme de réplication de l'ADN » ; « rôle de la réplication de l'ADN dans la stabilité de l'information génétique » |
| VIII (comme à l'examen), bilan, carte | C8 | Méthode de l'épreuve (restitution, exploitation de documents, schéma) appliquée aux notions ci-dessus |

Rien ne sort du cadre. La méiose, le brassage, Mendel, le génie génétique et la génétique humaine ne sont pas enseignés. Le « 46 chromosomes = 23 paires » est un rappel du caryotype, toléré par la fiche (`tolere_si_annonce`). Caractère, gène, allèle, mutation et code génétique sont laissés à svt_ch4. La carte se termine sur « au prochain chapitre, les protéines ».

#### (b) Corrections

| Diapositive / emplacement | Champ | Avant → après | Raison |
|---|---|---|---|
| ig_l3_section | screen_content.lead | « Seul le morceau avec le rhizoïde refait un chapeau. » → « Seul le morceau avec le rhizoïde, qui contient le noyau, régénère une algue complète. » | Faux : la tige (sans noyau) peut faire un petit chapeau avant de mourir. La voix et la simulation le disent, l'écran le niait. |
| ig_n3_chromatides | screen_content.bullets[1] | « Après la réplication (réplication) » → « Après la réplication (phase S) » | Mot répété par erreur |
| ig_r3_g1 | screen_content.bullets[2] | « … 1,717 : chaque molécule a un brin lourd et un brin léger. » → « … 1,717 : ADN hybride, à moitié lourd et à moitié léger. » | En génération 1, la bande à 1,717 ne prouve pas encore « un brin lourd + un brin léger » : l'hypothèse dispersive donne la même bande. La diapositive suivante et l'exercice de la séance 5 disent eux-mêmes qu'il faut la génération 2. |
| ig_r3_g1 | concentration.reponses.q.0.1.ecrit | (vide) → « Ta réponse contient une bonne idée : en génération 1, on observe bien une seule bande hybride. Mais la question porte sur ce que prévoyait l'hypothèse conservative… Réessaie. » | La réaction écrite était vide. Le texte reprend la voix existante. |
| ig_r3_g1 | reponses.q.2.2 ecrit + parole | « …la bande hybride n'apparaît qu'avec l'hypothèse semi-conservative » → « …Aucune des trois hypothèses ne prévoit trois bandes en génération un. » | Faux : la dispersive donne elle aussi une bande unique intermédiaire en G1. |
| ig_m7_schema | reponses.q.0.2 ecrit + parole | « chaque pôle reçoit 2 chromosomes (un de chaque paire), et chaque chromosome a 2 chromatides, donc 2 × 2 = 4 » → « 4 chromosomes à deux chromatides = 8 chromatides ; en anaphase, les chromatides de chaque chromosome se séparent : chaque pôle reçoit une chromatide de chaque chromosome, donc 4 » | Erreur grave : l'ancien texte décrit l'anaphase I de la méiose (homologues séparés), qui est hors chapitre, et non l'anaphase de mitose. |
| ig_l5_gurdon | reponses.q.2.1 ecrit + parole | « la grenouille montre des traits des deux » → « l'ovule et le noyau ont tous les deux servi dans l'expérience » | Faux : la grenouille est albinos et n'a que les caractères du donneur du noyau. |
| ig_r12_conservation | reponses.q.0.1 ecrit + parole | « tu as compris que la quantité d'ADN change sans réplication… combien de q dans chaque chromosome » → « la quantité d'ADN ne passe à 2q que par la réplication, en phase S ; sans phase S, la cellule a toujours q… combien chaque cellule fille peut-elle recevoir ? » | La réaction félicitait une idée fausse : la quantité d'ADN ne change pas sans réplication. |
| ig_x1_restitution | reponses_fin_de_cours.e0.2.1 ecrit + parole | « la réplication a bien lieu pendant la division, mais pas à l'anaphase » → « la réplication n'a pas lieu à l'anaphase, ni à aucun autre moment de la division » | Faux : la réplication a lieu en interphase (phase S). |
| ig_x1_restitution | e2s1.1.2 ecrit + parole | « Faux. Le nucléosome est formé d'ADN enroulé autour d'un octamère de huit histones, plus une région de liaison. La phrase est donc incomplète. » → « Vrai. Le nucléosome est formé d'ADN enroulé autour de protéines, les histones : nucléosome = ADN + histones. La phrase est juste. » | La réaction contredisait la clé (l'énoncé est VRAI) et validait la mauvaise réponse de l'élève. « Octamère » et « région de liaison » sont hors cadre (`hors_cadre.mots`). |
| ig_x1_restitution | e2s2.1.1 ecrit | « (Griffith) montre bien que l'ADN… » → « (Griffith, puis Avery) montre bien… et ce qui empêche la transformation chez Avery » | Griffith seul ne montre pas que le principe est l'ADN : c'est Avery qui le montre. |
| ig_x1_restitution | e2s3.0.1 ecrit + parole | « A et G sont bien liés par des liaisons hydrogène » → « les bases des deux brins sont bien reliées par des liaisons hydrogène. Mais A s'associe-t-il vraiment à G ? » | Faux : A ne s'apparie pas à G. |
| ig_x1_restitution | e2s3.1.juste ecrit + parole | « Vrai : A s'associe à G par deux liaisons hydrogène, pas trois… » → « Bonne réponse : la proposition est fausse. A ne s'associe pas à G : A–T par deux liaisons hydrogène, C–G par trois. » | Erreur scientifique (A–G). La réaction commençait aussi par « Vrai » alors que la clé est Faux. |
| competences C1, rappel C1_r4 | reponses 0.juste, 1.2, 2.2 (ecrit) | « caractères de / ressemble à l'**espèce** qui a donné le noyau » → « …l'**individu** qui a donné le noyau » | Chez Gurdon, donneur et receveur sont de la même espèce (têtard albinos, grenouille pigmentée). La voix dit déjà « l'individu ». |
| competences C7, rappel C7_r2 | reponses.0.2.ecrit | « Une seule bande hybride en G2 correspondrait à l'hypothèse dispersive » → « L'hypothèse dispersive prévoyait une seule bande, intermédiaire, en G2 : elle est donc rejetée. » | La dispersive prévoit en G2 une bande entre l'hybride et la légère, pas une bande hybride (voir ig_r6_rediger). |
| competences C7, rappel C7_r2 | reponses.1.juste.ecrit | « les brins nouveaux s'associent entre eux : molécules légères » → « chaque brin lourd (¹⁵N) sert de modèle à un brin nouveau : hybride ; chaque brin léger (¹⁴N) sert de modèle à un brin nouveau : légère » | Mécanisme faux : les brins ne s'associent pas librement, chaque brin sert de modèle. |
| seances ig_s2_b2 | exercice.reponses.0.2 ecrit + parole | « Les 3 UA correspondraient à une cellule fille après la mitose » → « Les 3 UA ne correspondent à aucune phase : même après la mitose, chaque cellule fille revient à 6 UA (q). » | Faux : avec q = 6 UA en G1, une cellule fille a 6 UA et non 3. |
| 26 réactions « mauvaise réponse, 2e essai » : ig_l1_amibe 0.2 et 1.2 ; ig_l5_gurdon 0.2 et 2.2 ; ig_p3_mitose_corps 0.2 et 2.2 ; ig_n3_chromatides 0.2 et 2.2 ; ig_c6_durees 2.2 ; ig_m4_anaphase 0.2 et 1.2 ; ig_m7_schema 2.2 ; ig_t1_griffith 0.2 et 2.2 ; ig_t3_support 0.2 et 2.2 ; ig_s1_nucleotide 0.2 ; ig_s5_complementaire 1.2 et 2.2 ; ig_r3_g1 0.2 ; ig_r6_rediger 0.2 ; ig_r9_yeux 0.2 et 2.2 ; ig_r12_conservation 1.2 ; C1_r2 0.2 ; C5_r2 2.2 | ecrit (début du texte) | « Bonne réponse : X… » / « Réponse correcte : X… » → « La bonne réponse : X… » | Ces textes s'affichent quand l'élève s'est trompé. « Bonne réponse : C » laissait croire qu'il avait juste, contrairement à la clé. La voix dit déjà « الجواب الصحيح هو » (« la réponse juste est… »). |

Vérifications sans problème :
- Pour chaque QCM, vrai/faux, rappel et exercice de séance, `correct` désigne la bonne option, et la réaction « juste » est bien sur l'option de la clé (vérifié par script).
- Les calculs sont justes : 25 % × 24 h = 6 h ; G1 45 % × 20 h = 9 h ; S = 6 h ; brins complémentaires (5' TTAGC 3' → 3' AATCG 5', 5' GATTCA 3' → 3' CTAAGT 5', 3' TACGGA 5' → 5' ATGCCT 3', 5' CGTA 3' → 3' GCAT 5') ; Chargaff 20 % C → G 20, A 30, T 30 ; Meselson 1,710 / 1,724 / 1,717, G1 100 % hybride, G2 50/50, G3 25/75 ; 92 molécules d'ADN en G2 ; 8 cellules à 46 chromosomes.
- Les simulations sont justes : noyau, zoom, cycle, documents, mitose, bacteries, adn, meselson, thymidine (conforme au national 2017 rattrapage), replication (le sens 5'→3' des deux brins nouveaux à chaque fourche est cohérent), bilan et carte. Aucun terme hors cadre n'apparaît (pas de centriole, kinétochore, hélicase, Okazaki ni phragmoplaste).

#### (c) Voix à refaire (pistes audio existantes dont la `parole` a changé)

1. `ig_r3_g1` → concentration.reponses.q.2.2 (audio `ig_r3_g1__q_2_2_v12.mp3`)
2. `ig_m7_schema` → concentration.reponses.q.0.2 (audio `ig_m7_schema__q_0_2_v12.mp3`)
3. `ig_l5_gurdon` → concentration.reponses.q.2.1 (audio `ig_l5_gurdon__q_2_1_v12.mp3`)
4. `ig_r12_conservation` → concentration.reponses.q.0.1 (audio `ig_r12_conservation__q_0_1_v12.mp3`)

`parole` modifiées sans piste audio actuelle, à générer si ces réactions doivent être dites :
- `ig_x1_restitution` reponses_fin_de_cours : e0.2.1, e2s1.1.2, e2s3.0.1, e2s3.1.juste
- seances `ig_s2_b2` exercice.reponses.0.2

Aucun `speech_text` n'a été modifié. Aucune légende de schéma à légender n'a été modifiée.

#### (d) Points à trancher (laissés tels quels)

1. **ig_r3_g1, voix** (`speech_text` et piste mixed) : « Donc chaque molécule a un brin lourd et un brin léger » dès la génération 1. Même réserve que pour l'écran corrigé (la dispersive donne aussi 1,717). La simulation `meselson.html` affiche « En G1, une seule bande à 1,717 : un brin lourd, un brin léger ». Faut-il refaire la voix et ce texte de la simulation ?
2. **C7_r2 reponses.1.juste, parole** : « les brins nouveaux كيتجمعو بيناتهم » (« s'associent entre eux »). L'écrit est corrigé, la voix est approximative mais décrit bien la composition (deux brins ¹⁴N). Faut-il la refaire ?
3. **ig_c1_cycle, voix** : « Astuce : G comme croissance ». C'est un moyen mnémotechnique, pas l'origine du sigle (G = gap, intervalle). Il est courant chez les professeurs.
4. **seances ig_s2_b1, réactions 1.1 et 1.2** : « 23 est le nombre de chromosomes d'un gamète (n) ». C'est une mention de la notion de gamète (cadre 2.3), utilisée seulement pour écarter un leurre. On peut la garder ou la remplacer par « 23 est le nombre de paires ».
5. **Ordre** : ig_n3_chromatides parle de « phase S » avant que la partie III (ig_c1_cycle) la définisse. Une simple mention en avance, sans conséquence grave.
6. **C2_r2 reponses.0.2** : « le nucléole fabrique les ribosomes ». Ce rôle n'est pas demandé au cadre 2.1, mais les ribosomes apparaissent dans svt_ch4. C'est une remarque en passant.
7. **Avery avec des souris** : historiquement, Avery a travaillé surtout en culture (in vitro). La présentation avec injection aux souris est celle des manuels marocains : à garder.

#### (e) Nombre total de corrections

- 28 champs corrigés pour des erreurs scientifiques, des contenus hors cadre, une contradiction avec la clé, une réaction vide ou une coquille (dont 9 `parole`).
- 26 préfixes « Bonne réponse » remplacés sur des réactions à une réponse fausse.
- **Total : 54 champs modifiés**, tous dans `svt_ch3_notion_information_genetique.json`. `git diff --stat` : 54 insertions, 54 suppressions. Le JSON est valide et le format a été gardé (`ensure_ascii=False, indent=2`). Les simulations n'ont pas été modifiées.

### Cours Audit SVT ch4 : Expression de l'information génétique (`svt_ch4_relation_gene_proteine`)

Référence : cadre officiel de l'examen national SVT, filière PC. Sous-domaine 2.1 (fin) : caractère héréditaire, gène, allèle, mutation ; relation caractère-protéine et gène-protéine ; signification génétique de la mutation ; code génétique. Sous-domaine 2.2 : structure de l'ARN, transcription, traduction (initiation, élongation, terminaison), schéma résumant la synthèse des protéines. J'ai aussi utilisé les fiches `perimetre.json` (`relation_gene_proteine`, `mutations_maladies`) et `cadre_reference_2bac_pc.json` (`relation_gene_proteine`).

Ce que j'ai vérifié : les 53 diapositives (titre, écran, voix fr et darija, questions, réactions préparées, observation, schémas à légender, cahier, `cahier_figures`), les 8 compétences et leurs rappels, les 6 séances et leurs blocs, les 13 simulations HTML et `molecules.js`. Il n'y a pas d'`exercices_fin_de_cours`.

Contrôles automatiques :
- Le tableau du code génétique de `molecules.js` est conforme au code standard (64 codons, 3 stop).
- Toutes les séquences « codons → acides aminés » du cours ont été recalculées : aucune erreur.

Contrôles faits à la main :
- Brins complémentaires : rg_t1, rg_t4, rg_t6, C4_r2, exercices des séances 2, 3, 4 et 6.
- Anticodons : UAC, GCG, UCA, GUC, CGA.
- Drépanocytose : CTC → CAC, GAG → GUG, Glu → Val, chaîne β Val-His-Leu-Thr-Pro-Glu-Glu.
- Données des nationaux cités, comparées aux `exam.json` : 2017 N (caille, triplet 228), 2018 R (allèle ; trois schémas de la traduction), 2023 N (LDLR, triplet 33, UAG), 2024 N (AMELX, CCC → CUC ; vrai/faux sur l'ARN polymérase), 2025 N (ABCD1, triplet 149, AGU → AGA).
- Toutes les clés `correct` des QCM et vrai/faux sont justes.

#### (a) Correspondance avec le cadre officiel

| Partie / compétence | Diapositives | Notion du cadre officiel PC |
|---|---|---|
| I. Gène, allèle, mutation (C1) | rg_d1 à rg_g3b | 2.1 « notions de caractère héréditaire, gène, allèle et mutation ». Les rappels ADN et protéine sont des prérequis du ch3. |
| II. Caractère et protéine (C2) | rg_d2, rg_p1 à rg_p4 | 2.1 « relation caractère-protéine » : les trois échelles et la drépanocytose ; document LDL du national 2023 N. |
| III. L'ARN et le marquage (C3) | rg_a1 à rg_a4 | 2.2 « structure de l'ARN » ; uracile et acides aminés marqués pour localiser transcription et traduction (RGP3, RGP4). |
| IV. La transcription (C4) | rg_t1 à rg_t6 | 2.2 « la transcription » : ARN polymérase, brin transcrit lu 3'→5', ARNm 5'→3'. |
| V. Le code génétique (C5) | rg_c1 à rg_c5 | 2.1 « le code génétique » ; 2.2 « relation ADN, ARNm, protéine en utilisant le code génétique ». |
| VI. La traduction (C6) | rg_r1 à rg_r6, rg_s2 à rg_s5 | 2.2 « la traduction : initiation, élongation, terminaison » et « schéma résumant les étapes de la synthèse des protéines ». |
| VII. Les mutations (C7) | rg_m1 à rg_m6 | 2.1 « signification génétique de la mutation », objectif « déduire la signification génétique de la mutation en utilisant le code génétique ». |
| VIII–IX. Du gène au caractère, rédiger (C8) | rg_s1, rg_e1 à rg_e6 | 2.1 « relation gène-protéine » ; restitution et exploitation de documents comme au barème (RGP10). |
| Bilan | rg_b1, rg_b2 | Huit blocs, cohérents avec C1 à C8. |

Aucune partie n'est hors cadre. La phrase « au prochain semestre, tu verras comment ces allèles se transmettent » (rg_b2) est une simple annonce, ce qui est acceptable.

#### (b) Corrections faites

| Diapositive / lieu | Champ | Avant → après | Raison |
|---|---|---|---|
| rg_t6_bareme | reponses.q.2.juste.ecrit | « On lit le brin transcrit de 5' vers 3' » → « Le brin transcrit est lu de 3' vers 5' » | Erreur scientifique : le brin transcrit se lit de 3' vers 5' (le cours le dit lui-même en rg_t4). |
| rg_t6_bareme | reponses.q.2.juste.parole | « كاتقراه ف الاتجاه ديال cinq prime نحو trois prime » → « كيتقرا ف الاتجاه ديال trois prime نحو cinq prime » | Même erreur dans la voix. **Voix à refaire.** |
| rg_t6_bareme | reponses.q.1.1.ecrit | « la séquence écrite est identique au brin transcrit » → « la complémentarité est juste ; mais tu as écrit des bases d'ADN (c'est la séquence du brin non transcrit) » | Faux : l'option B (5' ATG GGG TAG 3') n'est pas le brin transcrit (3' TAC CCC ATC 5') mais son complémentaire en ADN. |
| rg_t6_bareme | reponses.q.1.1.parole | « اللي كتبتيه هو نفس le brin transcrit » → « اللي كتبتيه فيه des bases ديال l'ADN، بحال le brin non transcrit » | Même erreur dans la voix. **Voix à refaire.** |
| rg_e6_drepanocytose | reponses.q.2.2.ecrit | « la glutamine est remplacée par la valine » → « l'acide glutamique est remplacé par la valine » | Erreur scientifique : Glu est l'acide glutamique ; la glutamine est Gln. La voix était juste. |
| rg_m6_juger | reponses.q.2.2.ecrit | « La substitution sur la troisième base du codon donne le même acide aminé » → « La substitution (souvent sur la troisième base du codon) donne un codon qui code le même acide aminé » | Généralisation fausse : une substitution de la 3e base ne donne pas toujours le même acide aminé (UGG → UGA donne un stop). |
| rg_e1_restitution | reponses.e0s0.1.2.ecrit | « on change un « caractère » de l'ADN » → « on change un ou plusieurs nucléotides (des « lettres ») de l'ADN » | Le mot « caractère » est ambigu, puisqu'il désigne le caractère héréditaire dans ce même chapitre. |
| competences C4_r2 | reponses.2.2.ecrit | « 3' TAC CTG 5' donne 3' AUG GAC 5', soit 5' AUG GAC 3' » → « 3' TAC CTG 5' donne l'ARNm 5' AUG GAC 3' (antiparallèle au brin transcrit…) » | Orientation fausse : l'ARNm complémentaire de 3' TAC CTG 5' s'écrit 5' AUG GAC 3', pas 3' AUG GAC 5'. |
| competences C4_r2 | reponses.1.2.ecrit | « le premier nucléotide devait être U (venant de A) et non A » → « le 2e nucléotide devait être U (en face du A de TAC) et non T » | Faux : dans l'option B (ATG GAC), l'erreur porte sur le 2e nucléotide (T au lieu de U) ; le 1er (A) est juste. |
| seances rg_s6_b1 | exercice.reponses.0.1.ecrit | « substitution (G devient T) » → « substitution (A devient T, 3e nucléotide) » | Faux : GGA → GGT, c'est A qui devient T. |
| seances rg_s6_b1 | exercice.reponses.0.1.parole | « G ولات T » → « A ولات T » | Même erreur dans la voix. **Voix à refaire.** |
| seances rg_s1_b2 | retrouver (prompt, attendu, enonce_dit) | « donne la définition d'une mutation » → « donne la définition d'un allèle » (attendu : définition de l'allèle) | Organisation : la mutation n'est enseignée qu'au bloc suivant (rg_s1_b3, qui la redemande). Ce retrouver portait sur une notion pas encore vue. Pas de piste audio. |
| seances rg_s5 | titre | « Séance 5 — Le cadre de lecture et le schéma bilan » → « Séance 5 — Le schéma bilan et la rédaction du barème » | Le cadre de lecture est traité en séance 4 (rg_s4_b3), pas en séance 5. |
| Simulation `paire_homologues.html` (vue `paire`, rg_g2_allele) | texte écrit à t = 13,2 s, ligne `voit`, champ `texte` (+ 2 commentaires) | « A et B dominent O ; A et B sont codominants » → supprimé | Hors cadre : dominance et codominance relèvent des lois de Mendel (sous-domaines 2.3-2.4). La voix ne le dit pas. Syntaxe JS vérifiée (`node --check`). |


#### (c) Voix à refaire

1. **rg_t6_bareme**, réaction `q.2.juste`. Fichier `rg_t6_bareme__q_2_juste_v*.mp3` : sens de lecture du brin transcrit corrigé.
2. **rg_t6_bareme**, réaction `q.1.1`. Fichier `rg_t6_bareme__q_1_1_v*.mp3` : l'option B, c'est le brin non transcrit en ADN.
3. **Séance rg_s6_b1**, exercice, réaction `0.1`. La piste actuelle s'appelle `bloc_rg_s5_b2__ex_0_1_v10.mp3` : « A ولات T ».

Aucun `speech_text` ni aucun texte de schéma à légender n'a été modifié.

#### (d) Points à trancher (non modifiés)

1. **Groupe sanguin [A] pour A/O** (`paire_homologues.html`, rg_g2 avec la variante `allele_mere: B` qui donne [AB]). La simulation écrit le phénotype entre crochets, calculé avec la dominance (AO → [A]), sans nommer la dominance. C'est une dominance implicite :
   - option 1 : la garder ;
   - option 2 : remplacer le phénotype par « caractère : groupe sanguin » sans valeur.
2. **rg_m6_juger, voix des réactions `q.1.2` et `q.2.2`.** La voix dit que la substitution silencieuse « se produit sur la troisième base du codon ». C'est souvent vrai, mais ce n'est pas une règle. J'ai corrigé l'écrit, pas la voix.
3. **rg_g1_gene.** La voix darija dit « باللون الصفر » (jaune), alors que l'image et l'écran montrent une accolade orange. Ce n'est pas une erreur scientifique ; à reprendre seulement si on réenregistre la voix.
4. **« Toute protéine commence par la méthionine »** (rg_c3, rg_r2). C'est l'usage du bac marocain ; la méthionine est parfois retirée ensuite, mais c'est hors programme. Je l'ai laissé tel quel.
5. **Noms des pistes audio des blocs de séance.** Ils sont décalés d'un bloc : rg_s1_b2 utilise `bloc_rg_s1_b1__*`, …, rg_s6_b1 utilise `bloc_rg_s5_b2__*`. Il s'agit probablement d'une ancienne numérotation, et la `parole` correspond bien à son bloc. Il faut quand même vérifier que chaque mp3 prononce la bonne réaction (je n'ai pas pu l'écouter).
6. **Expérience bactéries et streptomycine** (rg_g3) : c'est un support pour introduire la mutation, compatible avec le cadre (mutation « spontanée ») ; je n'ai rien changé.

Rien d'autre n'est hors programme : il n'y a ni épissage, ni promoteur détaillé, ni sites A/P/E, ni aminoacyl-ARNt synthétase, ni structures secondaire/tertiaire/quaternaire, ni Mendel. Les simulations `traduction.html`, `transcription.html` et `molecules.js` déclarent d'ailleurs exclure ces notions.

#### (e) Nombre total de corrections

**14** : 13 dans le cours (dont 3 voix à refaire) et 1 dans la simulation `paire_homologues.html`.

## Étape 3 — Le skill

Ajouté à `.agents/skills/exploration-de-cours/SKILL.md` et `.agents/skills/cours-concentration/SKILL.md` : la section obligatoire « Conformité au cadre officiel du ministère » (partir du JSON officiel de la filière PC, chaque partie cite sa notion officielle, un mot d'un document d'examen se lit sans s'apprendre) et sa sous-partie « SVT » (les 4 domaines, ce que la filière PC n'a pas, la règle de l'examen, les pièges trouvés dans cet audit).
