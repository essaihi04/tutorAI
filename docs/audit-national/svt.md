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

Audit du 19 novembre 2026. Simulations : `frontend/public/media/simulations/svt/notion_information_genetique-tableau/`.

### (a) Les exercices du national joués dans le cours

L'énoncé d'abord (professeur, règle 46, addendum du 19/11) : **pas encore fait**. Le gabarit commun
`shared/examen/feuille.html` n'est pas sur main ; aucune diapositive « énoncé » n'a été créée (et aucune ne montre un scan).
Ce qu'il faudra reproduire en code, exercice par exercice :

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
- **Pistes ajoutées au `_voix.json` : 0** (aucun texte dit nouveau ni changé).
- **Pas fait** : les diapositives « énoncé d'abord » (gabarit `feuille.html` absent de main) ; le comptage allumé un à un
  avec numéro (règle 16) : aucun des moments du tableau (b) n'a encore « 1, 2, 3… » écrits à la craie à côté d'une lueur
  — à faire en priorité sur `ig_m7_schema` (4 chromosomes, 8 chromatides), `ig_n3_chromatides` et le chromosome du QCM
  2018 R (`ig_x1d`, il faudra un dessin et une voix nouvelle).
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
