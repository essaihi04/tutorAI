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
