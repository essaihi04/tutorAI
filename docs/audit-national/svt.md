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

_à remplir_
<!-- ch1 : fin -->

<!-- ch2 : début -->
## Ch2 — Le muscle strié squelettique (`svt_ch2_role_muscle_strie_squelettique`)

_à remplir_
<!-- ch2 : fin -->

<!-- ch3 : début -->
## Ch3 — L'information génétique (`svt_ch3_notion_information_genetique`)

_à remplir_
<!-- ch3 : fin -->

<!-- ch4 : début -->
## Ch4 — Du gène à la protéine (`svt_ch4_relation_gene_proteine`)

Simulations : `frontend/public/media/simulations/svt/relation_gene_proteine-tableau/` (moteur commun `etapes.js`).
Audit du 19 novembre 2026.

### (a) Exercices du national joués dans le cours

Les diapositives « énoncé d'abord » ne sont **pas encore faites** : d'après l'addendum du 19/11, l'énoncé est la feuille
d'examen refaite en code (`shared/examen/feuille.html?sujet=…&exercice=…`), gabarit qui n'est pas encore sur main.
Aucune diapositive ne montre de scan. Ce qui suit prépare ce travail.

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
- **Pistes ajoutées au `_voix.json` : 0** (aucun texte dit n'a changé ; les pointages ajoutés utilisent des fragments
  existants).
- **Pas fait** : les diapositives « énoncé d'abord » (gabarit `feuille.html` absent de main) ; le canevas écrit encore
  certaines réponses que la colonne de démonstration écrit aussi (`amelogenine_pas` q2_reponse, `moustiques_seq` arnm —
  ces moments ne sont pas joués pendant la démonstration, mais le seraient sur demande) ; les comptages « à faire » ci-dessus.
<!-- ch4 : fin -->
