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

_à remplir_
<!-- ch4 : fin -->
