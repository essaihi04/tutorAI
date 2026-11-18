# Architecture — SVT ch3 « Notion de l'information génétique » (`svt_ch3_notion_information_genetique`)

Refaite le 18 novembre 2026 avec la skill `logique-de-cours`. Version en attente :
`backend/data/courses/en_attente/svt_ch3_notion_information_genetique.json` (le cours en ligne n'est pas touché).
Script : `scripts/logique/refaire_svt_ch3.py` (§ 7). Pistes à mettre en voix : `svt_ch3_notion_information_genetique_voix.json`.

## 1. Sources consultées

- **Profs (vidéos)** : l'exploration `backend/data/curriculum/exploration/notion_information_genetique.json` (10 vidéos :
  Faress, Aouragh, Ikram, Lamsaf, Maison Des Sciences, Ouissam, Wessal, Driss, Sarah, Mousstaid) — convergences,
  cas types, notions complexes NC1 à NC9, pièges, commentaires d'élèves.
- **Cours écrits en ligne (plans relevés)** :
  1. Moutamadris, « Notion de l'information génétique », 2 Bac SP international (cours, 15 p.) : I localisation
     (expériences, ultrastructure du noyau) → II transmission (mitose animale, végétale, cycle cellulaire, caryotype)
     → III nature chimique (Griffith, Avery, Hershey-Chase, l'ADN constituant des chromosomes) → IV composition et
     structure de l'ADN → V réplication (Meselson et Stahl, mécanisme, complémentarité réplication-mitose).
  2. Moutamadris, même chapitre (cours 16 p., 8 h) : I localisation (unicellulaires, pluricellulaires) → II transfert
     (étapes de la mitose, cycle cellulaire) → III nature chimique (Griffith, composition et structure, réplication,
     autoradiographie).
  3. AlloSchool, M. Bahsina, « Nature de l'information génétique » parties 1 et 2 : introduction par la cellule-œuf
     et trois questions (où ? de quoi ? comment se transmet-elle ?) → mérotomie de l'amibe → section et greffe
     d'acétabulaire → Gurdon → conclusion ; puis mitose (racine d'oignon) → cycle cellulaire → nature chimique.
  4. AlloSchool, M. Bahsina, devoir 2 modèle 1 (QCM « phase G1 », « nombre de molécules d'ADN », vrai/faux).
  5. Dyrassa, série d'exercices n° 7 (L. Amane) : courbe de la quantité d'ADN, Meselson et Stahl, Chargaff.
- **Cadre** : `backend/data/curriculum/svt.json` (domaine 2, 2.1), `perimetre.json` (clé `notion_information_genetique`),
  capacités NIG1 à NIG11 de l'exploration.
- **National** (`cas_types` de l'exploration) : QCM cycle/chromatides/réplication (2018 R, 2024 N, 2024 R),
  caractéristiques d'une phase (2018 R), thymidine radioactive (2017 R, 1,5 pt), définitions (2024 N) ; courbe d'ADN,
  photos de mitose, Griffith/Avery, Meselson, Chargaff, durées : très fréquents aux contrôles, rares au national PC.

## 2. La logique avant (cours en ligne)

Ouverture (2) → I noyau : amibe, acétabulaire, section, greffe, Gurdon + définition (5) → II « chromosomes » : 46
chromosomes et ADN porteur de l'information, mitose simple, mitose et corps, **puis** le noyau en interphase, Feulgen,
condensation, chromatides (7) → III cycle, « pourquoi doubler » (q → 2q affirmé), courbe, aspect, décrire, durées (6)
→ IV mitose (8) → V Griffith en cinq diapositives, Avery (9) → VI ADN (6) → VII réplication (13) → VIII examen (2) →
bilan (2). 61 diapositives, 6 séances.

Ce qui n'allait pas, au regard des règles :

| Diapositive | Problème | Règle |
|---|---|---|
| `ig_l3_section`, `ig_l4_greffe` | la voix donne le résultat de la greffe (« à gauche, un chapeau crénelé ») sans laisser l'élève le chercher ; « preuve ou hypothèse ? » n'est jamais demandé alors que c'est l'erreur la plus fréquente (NC1, piège « conclut dès la section ») | 3 |
| `ig_l5_gurdon` | le résultat est dit, puis la question « à qui ressemble la grenouille ? » est posée **après** ; la même diapositive construit aussi la définition (deux idées) | 3, 7 |
| `ig_p1_chromosomes` | « Entrons dans le noyau » deux fois (p1 et n1) ; le chromosome est montré **avant** la chromatine (ordre inverse des 10 profs) ; « l'ADN, c'est sur lui que l'information est écrite » est affirmé **avant** Griffith et Avery qui le prouvent | 4 |
| `ig_c2_pourquoi` avant `ig_c3_courbe` | q → 2q est affirmé une diapositive avant la courbe qui le montre | 4 |
| `ig_c6_durees` | tout le calcul (deux cycles, 20 h, les quatre phases) est dit, puis on demande « combien dure un cycle ? » : la réponse est déjà donnée | 3 |
| `ig_m4_anaphase` | anaphase et télophase sur une diapositive (deux idées) ; « Attention : pas vers le même pôle » est dit avant la question « vont-elles au même pôle ? » | 3, 7 |
| `ig_t1f_bilan` | commence par « La troisième question : de quoi est faite l'information ? Expérience de Griffith… » : reste de l'ancienne version, redit l'ouverture de `ig_t1_griffith` | 1 |
| `ig_s2_chargaff` | la déduction A–T, C–G est dite par la voix sans que l'élève la tire des rapports | 3, 4 |
| `ig_r3_g1`, `ig_r4_g2` | chaque génération est dite d'emblée (« bande unique au milieu », « deux bandes ») ; la génération 2, cas décisif (dispersive contre semi-conservative), n'est pas posée en question | 3 |

Ce qui était déjà juste et reste : le départ de zéro (`ig_o2_rappel`, la cellule), Griffith joué une expérience par
diapositive avec la souris 4 posée en question d'observation, Avery avec le tube 3 posé en question, la courbe d'ADN et
les durées produites par une animation (`documents.html?vue=durees` : culture, lame, cellules triées puis tableau),
Chargaff produit par l'animation des bocaux (`adn.html?vue=chargaff`, modèle de la règle 35), les trois schémas à
légender (`legende_*` : anaphase, ADN, réplication), l'expérience toujours avant le mécanisme en réplication
(Meselson, thymidine, puis yeux et ADN polymérase).

## 3. La logique après — séances, blocs, diapositives et pourquoi

Ordre des parties : celui des 10 profs et des 3 cours écrits (où ? → transmission d'une cellule à l'autre → de quoi
est-elle faite ? → comment se copie-t-elle ?) et du cadre (NIG1 → NIG10). 63 diapositives, **7 séances** de 3 blocs
(325 → 340 min, ~48 min par séance : la règle 7 interdit des séances plus longues, d'où la 7ᵉ).

Légende : ▶ animation pilotée par la voix ; 👀 question d'observation (le cas décisif, la voix s'arrête avant le
résultat) ; ✏️ la question « À toi » du bloc ; ✱ diapositive nouvelle ou réécrite (voix à refaire).

### Séance 1 — Où est l'information génétique ? Le noyau (NIG1, C1)

**Bloc 1 — Une information transmise ; la cellule ; l'amibe**
1. `ig_o1_ressemblance` — *pourquoi ici* : la question de départ des 10 profs sur 10 et de Bahsina (« pourquoi
   ressembles-tu à tes parents ? »), les quatre questions du chapitre posées sans réponse (règle 3).
2. `ig_o2_rappel` ▶ — la cellule (membrane, cytoplasme, noyau) enseignée de zéro, dite deux fois (la maison) : elle
   sert à la diapositive suivante (règle 6).
3. `ig_l1_amibe` ▶ ✏️ — la mérotomie : première expérience de Bahsina et Moutamadris ; le résultat est demandé.

**Bloc 2 — L'acétabulaire : une hypothèse, puis sa vérification** (NC1, 4 marches)
4. `ig_l2_acetabulaire` ▶ — l'être vivant présenté avant l'expérience (marche 1) ; la forme du chapeau = caractère.
5. `ig_l3_section` ▶ 👀 — la section ; **nouvelle question d'observation** « preuve ou hypothèse ? » après la
   régénération du rhizoïde, avant que la voix ne dise « hypothèse » : c'est le piège n° 1 de l'exploration
   (« conclut dès la section ») et la marche 2 de NC1.
6. `ig_l4_greffe` ▶ 👀 — la greffe croisée ; **nouvelle question d'observation** « quel chapeau repousse ? » posée
   après l'échange des noyaux, avant le chapeau (cas décisif, règle 3) ; la voix confirme ensuite et rédige
   « on observe que… on déduit donc que… » (méthode du barème, cas type `localisation`).

**Bloc 3 — Gurdon, et la définition**
7. `ig_l5_gurdon` ✱ ▶ 👀 — Gurdon seul : la voix s'arrête après l'injection du noyau ; **question d'observation**
   « que donne cet œuf ? » ; la définition est retirée de cette diapositive (une idée par diapositive, règle 7).
8. `ig_l6_definition` ✱ ✏️ — **nouvelle** : les trois expériences rassemblées (le bilan après la dernière, règle 3),
   la définition construite par trois questions puis dite mot pour mot (cadre, NIG1), puis **dite une deuxième fois
   autrement** (le chef de l'usine : image validée de l'exploration, règle 6). Question : « le caractère suit
   toujours… le noyau ».

### Séance 2 — Dans le noyau : chromatine, chromosomes, mitose (NIG2, C2 ; C4 en une idée)

**Bloc 1 — Chromatine et chromosome : le même ADN**
9. `ig_n1_noyau` ▶ — *déplacée en tête* : le noyau en interphase (enveloppe à pores, nucléole, chromatine,
   nucléosome) est ce que les 10 profs montrent d'abord après la localisation (Moutamadris : « ultrastructure du
   noyau » juste après I) ; on entre dans le noyau qu'on vient de prouver.
10. `ig_n2_condensation` ▶ — la chromatine se condense en chromosome (NC2 marche 2) : le chromosome naît sous les
    yeux de l'élève au lieu d'être supposé connu.
11. `ig_n1b_feulgen` — *déplacée après la condensation* : la réaction de Feulgen colore à la fois les noyaux en
    interphase et les chromosomes en division ; placée ici, elle prouve d'un coup ce que les deux diapositives
    précédentes viennent de nommer (« chromatine = ADN déroulé », « le même ADN ») — l'expérience juste après le mot,
    plus jamais un chromosome avant la chromatine.

**Bloc 2 — 46 chromosomes, et la mitose en une idée**
12. `ig_p1_chromosomes` ✱ ▶ — réécrite : le nombre (46, 23 paires, homologues, 2n = 46, diploïde) ; le chromosome
    déroulé = ADN + protéines (ce que Feulgen vient de montrer) ; **la phrase « l'information est écrite sur l'ADN »
    est retirée** et remplacée par la question ouverte « ADN ou protéines ? » à laquelle Griffith et Avery répondront
    (règle 4 ; Moutamadris place aussi « l'ADN, constituant des chromosomes » sans en faire le support avant Avery).
    Dite deux fois (la bibliothèque de 46 livres).
13. `ig_p2_mitose` ▶ — la mitose en une idée (copier puis partager), au moment où elle sert : juste avant les
    chromatides et le cycle (règle 6).
14. `ig_p3_mitose_corps` ▶ ✏️ — la même idée autrement (de la cellule-œuf au corps) ; question « combien de
    chromosomes dans une cellule fille ? ».

**Bloc 3 — Une ou deux chromatides ; le cycle cellulaire**
15. `ig_n3_chromatides` ▶ ✏️ — *déplacée après la mitose simple* : la « copie » de `ig_p2` devient la deuxième
    chromatide ; question jumelle du QCM national 2018 R (molécules d'ADN par chromosome).
16. `ig_c1_cycle` ▶ — le cycle (G1, S, G2, M), deuxième question du chapitre.

### Séance 3 — La quantité d'ADN au cours du cycle (NIG3, NIG5, C3), puis la mitose (C4)

**Bloc 1 — La courbe, et pourquoi doubler**
17. `ig_c3_courbe` ▶ ✏️ — *avancée avant « pourquoi doubler »* : la courbe se trace pendant que le point tourne sur le
    cycle (NC3 marches 1-4) ; l'élève lit lui-même dans quelle phase la quantité double (règle 4 : le document avant
    l'affirmation).
18. `ig_c2_pourquoi` ▶ — l'explication vient après la lecture : copier avant de partager (le livre pour deux
    enfants) ; la question restera ouverte jusqu'à `ig_r12`.
19. `ig_c4_aspect` ▶ — la courbe reliée à l'aspect du chromosome (NC3, 9 profs sur 10).

**Bloc 2 — Comme à l'examen : décrire, calculer**
20. `ig_c5_decrire` ▶ — décrire avec les valeurs puis expliquer (cas type `courbe_adn`, le plus fréquent aux
    contrôles ; piège « explique quand on demande de décrire »).
21. `ig_c6_durees` ✱ ▶ ✏️ — réécrite : les données naissent de l'animation (culture, minuteur), la voix dit
    seulement que le nombre double à chaque cycle, puis **demande** « combien de cycles, combien dure un cycle ? »
    (la question, ses réactions et sa démonstration sont gardées) ; avant, la réponse était dite avant la question.
    Piège visé : « ×4 » au lieu de deux doublements.
22. `ig_c6b_phases` ✱ ▶ 👀 — **nouvelle** (la deuxième moitié de l'ancienne `ig_c6`) : durée d'une phase par le
    pourcentage ; **question d'observation** sur la phase S (« son pourcentage n'est pas donné : comment ? ») avant
    la soustraction, avec le piège « oublier M ».

**Bloc 3 — La mitose : définition, prophase, métaphase**
23. `ig_m1_mitose` ▶ — définition construite par trois questions (deuxième explication de la mitose, après
    `ig_p2` : règle 6).
24. `ig_m2_prophase` ▶, 25. `ig_m3_metaphase` ▶ — une phase par diapositive, les critères du barème.

### Séance 4 — La mitose, puis Griffith

**Bloc 1 — Anaphase, télophase, cellule végétale**
26. `ig_m4_anaphase` ✱ ▶ ✏️ — réécrite, **anaphase seule** : le centromère se coupe, la migration est jouée, la voix
    dit « regarde où part chaque chromatide » et pose la question **sans la réponse** (avant : « pas vers le même
    pôle » était dit avant de demander). Question et réactions gardées.
27. `ig_m4b_telophase` ✱ ▶ — **nouvelle** : la télophase, une idée par diapositive (règle 7) ; garde le croquis du
    cahier « Télophase (2n = 4) ».
28. `ig_m5_vegetale` ▶ — la comparaison animale/végétale après les quatre phases (8 profs sur 10 ; les photos
    d'examen sont des racines d'oignon).

**Bloc 2 — Reconnaître, dessiner, légender**
29. `ig_m6_photo` ▶ — nom + « car » + critère (cas type `identifier_phase`).
30. `ig_m7_schema` ✏️ — schéma titré 2n = 4 (cas type `schematiser`).
31. `ig_m7b_legender` ▶ — schéma à légender (contrat `legende_*`), l'élève pose les étiquettes.

**Bloc 3 — Griffith : le principe, puis deux expériences** (NIG6)
32. `ig_t1_griffith` ▶ ✏️ — le principe et la question de contrôle (S/R) avant toute expérience (règle 33).
33. `ig_t1b_exp1` ▶, 34. `ig_t1c_exp2` ▶ — une expérience par diapositive, chacune arrêtée avec son résultat.

### Séance 5 — L'ADN porte l'information ; sa composition (NIG6, NIG7)

**Bloc 1 — Les S tués, puis la souris 4**
35. `ig_t1d_exp3` ▶ — la troisième expérience ; le tableau des trois résultats se remplit à droite.
36. `ig_t1e_exp4` ▶ 👀 — le cas décisif posé en question d'observation (déjà en ligne, gardé).
37. `ig_t1f_bilan` ✱ ▶ — réécrite : seulement le bilan des quatre expériences, **après** la dernière (« Mettons les
    quatre expériences ensemble »), sans la redite de l'ouverture.

**Bloc 2 — Avery : l'ADN est le support**
38. `ig_t2_avery` ▶ — trois tubes, trois enzymes (le protocole avant les résultats).
39. `ig_t2b_avery_resultats` ▶ 👀 — tube par tube ; le tube 3 posé en question (gardé).
40. `ig_t3_support` ▶ ✏️ — la transformation expliquée étape par étape ; elle répond à la question laissée ouverte en
    `ig_p1` (« ADN ou protéines ? »).

**Bloc 3 — Le nucléotide, Chargaff, deux brins**
41. `ig_s1_nucleotide` ▶ ✏️ — hydrolyse → trois constituants → nucléotide (9 profs sur 10).
42. `ig_s2_chargaff` ▶ 👀 — les pourcentages naissent de l'animation (bocaux comptés, règle 35) ; **nouvelle question
    d'observation** après les trois espèces : « A/T ≈ 1, C/G ≈ 1 : qu'en déduis-tu ? » ; la voix confirme A–T, C–G
    ensuite (règle 4 : l'élève tire la complémentarité des données avant qu'on la lui dise en `ig_s4`).
43. `ig_s3_antiparalleles` ▶ — deux brins tête-bêche (les deux stylos).

### Séance 6 — La double hélice, et Meselson et Stahl (NIG8, NIG9)

**Bloc 1 — La double hélice et le brin complémentaire**
44. `ig_s4_helice` ▶ — A–T (2 liaisons), C–G (3), double hélice : la structure après les données de Chargaff.
45. `ig_s5_complementaire` ▶ ✏️ — écrire le brin complémentaire (extrémités d'abord, piège n° 10).
46. `ig_s5b_legender` ▶ — schéma de l'ADN à légender (`legende_*`).

**Bloc 2 — Les hypothèses, la génération 1**
47. `ig_r1_hypotheses` ▶ — les trois hypothèses avant l'expérience.
48. `ig_r2_experience` ▶ — le protocole (¹⁵N puis ¹⁴N, centrifugation, tubes repères).
49. `ig_r3_g1` ▶ 👀 ✏️ — **nouvelle question d'observation** « combien de bandes en génération 1, et où ? » après la
    génération 0 ; la voix confirme (une bande hybride), calcule la moyenne 1,717, rejette la conservative.

**Bloc 3 — Génération 2 : semi-conservative**
50. `ig_r4_g2` ✱ ▶ 👀 — début réécrit : « après la génération 1, deux hypothèses restent ; pour les départager, il
    faut la génération 2 » (piège « conclut dès G1 ») ; **question d'observation** sur le cas décisif (deux bandes →
    la dispersive est rejetée), puis l'explication molécule par molécule déjà enregistrée.
51. `ig_r5_semi` ▶ — génération 3 et conclusion.
52. `ig_r6_rediger` ▶ ✏️ — rédiger l'exploitation (tableau des prévisions, comparaison) comme le barème.

### Séance 7 — Le mécanisme de la réplication, et l'examen (NIG9, NIG10, NIG11)

**Bloc 1** — 53. `ig_r7_thymidine1` ▶, 54. `ig_r8_thymidine2` ▶ (national 2017 R, une génération par diapositive),
55. `ig_r9_yeux` ▶ ✏️ (le mécanisme après les deux expériences qui le prouvent, règle 4).
**Bloc 2** — 56. `ig_r10_polymerase` ▶, 57. `ig_r11_deux_molecules` ▶, 58. `ig_r11b_legender` ▶ (`legende_*`),
59. `ig_r12_conservation` ▶ ✏️ (referme « pourquoi doubler avant de partager ? » ouverte en `ig_c2`).
**Bloc 3** — 60. `ig_x1_restitution` ▶, 61. `ig_x2_exercice` ▶ ✏️ (restitution puis exercice rédigé),
62. `ig_b1_bilan`, 63. `ig_b2_carte` (bilan et carte, inchangés).

## 4. Ce qui change, en bref

| Avant | Après | Raison |
|---|---|---|
| p1, p2, p3 (chromosomes, mitose) puis n1, n1b, n2, n3 | n1, n2, n1b, p1, p2, p3, n3 | chromatine avant chromosome (10/10 profs) ; Feulgen juste après les mots qu'il prouve ; mitose simple juste avant son usage |
| « l'information est écrite sur l'ADN » (p1) | « ADN ou protéines ? on le saura par des expériences » | l'expérience (Avery) avant le résultat |
| c2 « pourquoi doubler » puis c3 courbe | c3 puis c2 | la courbe montre q → 2q avant qu'on l'affirme |
| c6 : calcul complet puis question | c6 question avant le calcul ; c6b phases avec la phase S en observation | ne pas donner la réponse avant la question |
| m4 anaphase + télophase | m4 anaphase, m4b télophase | une idée par diapositive |
| l5 Gurdon + définition | l5 Gurdon (👀), l6 définition après les trois expériences, dite deux fois | bilan après la dernière expérience ; deux explications |
| greffe, section, Chargaff, Meselson G1 et G2 : résultat dit | question d'observation avant le résultat | le cas décisif posé en question |
| 6 séances | 7 séances (~48 min) | deux diapositives de plus, séances ≤ 50 min |

Questions d'observation : 9 dans le cours (2 déjà en ligne + 7 nouvelles). La skill `cours-concentration` en conseille
0 à 2 ; on en met plus parce que la demande du 18 novembre (« le cas décisif posé en question, la conclusion après la
réponse de l'élève ») porte précisément sur ces cas, et que chacune est posée sur une voix **inchangée** (le texte
s'arrête après `apres_mot` et la phrase suivante confirme) : elles ne coûtent aucune voix de diapositive.
Les « À toi » restent à une question par bloc au plus.

## 5. Animations et besoins notés

Faits à la 2ᵉ passe (18 novembre 2026, détail en § 5 bis) : la vue « trois expériences côte à côte »
(`noyau.html?vue=trois`), `meselson.html {conclusions: false}`, le départ d'`ig_c6b_phases`.

- `mitose.html?vue=animale&diapo=m4_anaphase` sert aux deux diapositives `ig_m4` et `ig_m4b` (départ à 13,2 s).
- `ig_c6b_phases` : la page est rechargée (`&diapo=c6b_phases`) ; son premier geste est maintenant un `set_time` sur
  `duree_cycle` (19,6 s), écrit d'un coup (déjà vu en `ig_c6_durees`), au lieu de rejouer 20 s d'animation sous la voix.

## 5 bis. 2ᵉ passe (18 novembre 2026) : les cas types joués pas à pas, rien de décisif avant la réponse

Demande : « simple, animé, expliqué, ne pas tout donner au départ, laisser à l'élève le temps de trouver seul ». Script :
`python3 scripts/logique/passe2_svt_ch3.py` (idempotent, sur la copie en attente).

### Les cas types de l'exploration, un par un

| Cas type (fréquence) | Où il est joué | État après la 2ᵉ passe |
|---|---|---|
| `localisation` (contrôles) | `ig_l1` → `ig_l5` (chaque expérience jouée seule, résultat en question d'observation), puis `ig_l6` | déjà joué ; **ajouté** : la vue « trois expériences côte à côte » pour `ig_l6_definition` (règle 33 : le récapitulatif après la dernière). Texte inchangé : la voix reste ; le pointage suit les mots déjà dits. |
| `nature_chimique` (contrôles) | Griffith `ig_t1` → `ig_t1f` (la souris 4 en observation, `conclusions=false`), Avery `ig_t2`, `ig_t2b` | déjà joué, rien à refaire |
| `meselson` (QCM 2018 R sur les modèles) | `ig_r1` → `ig_r6` | déjà joué ; **corrigé** : pendant les observations de G1 et G2, « conservative / dispersive rejetée » et la conclusion se taisent (`sim_avant {conclusions: false}`, `sim_apres {conclusions: true}`) ; en G2, la conservative (rejetée en G1) reste barrée |
| `chargaff` (contrôles) | `ig_s2_chargaff` (bases comptées en animation, puis le tableau ; observation sur A/T et C/G) | déjà joué |
| `duree_cycle` (agronomie 2015 R) | `ig_c6_durees` (question), `ig_c6b_phases` (observation sur la phase S) | déjà joué ; départ d'`ig_c6b` réglé (§ 5) |
| `identifier_phase` (contrôles) | `ig_m6_photo` : une cellule rédigée par la voix (méthode), la suivante laissée à l'élève | déjà joué |
| `schematiser` (contrôles, 2016 N) | `ig_m7_schema` (question 2n = 4 avant la démonstration), `ig_m7b_legender` (légender soi-même) | déjà joué |
| `caracteriser_phase` (2018 R, 0,5 pt) | `ig_m4_anaphase` : la question vient avant la réponse | **ajouté** : la phrase du barème (deux caractéristiques : une chromatide par chromosome après la division du centromère ; les chromatides vers les pôles opposés) en démonstration de la question |
| `qcm_cycle` (2018 R, 2024 N/R) | `ig_x1_restitution` | **refait** : avant, la voix barrait elle-même a, c, d puis donnait b — l'élève n'avait rien à trouver. Maintenant `ig_x1_restitution` pose le QCM de 2024 R (G1) et s'arrête ; l'élève répond (une réaction préparée par option) ; **puis** `ig_x1b_corrige` joue le corrigé leurre par leurre (l'ancien texte et sa voix, déplacés). Même schéma pour le QCM du national 2018 R (« durant la métaphase, chaque chromosome est formé… », réponse c) : `ig_x1c_metaphase` (posé), `ig_x1d_corrige_metaphase` (corrigé joué, nouvelle vue `documents.html?vue=metaphase`). |
| `courbe_adn` (très fréquente aux contrôles) | `ig_c5_decrire` (la méthode montrée une fois), `ig_x2…` | **refait** : avant, `ig_x2_exercice` expliquait la chute de 2q à q puis posait la question dont il venait de donner la réponse. Maintenant une consigne par diapositive : `ig_x2_exercice` = **décrire** (la courbe seule, `?reponse=rien` ; question « de 8 à 14 h, la description comme le barème » : la réponse sans valeurs et l'explication donnée à la place de la description sont les deux pièges, chacun avec sa réaction) ; `ig_x2b_expliquer` = **expliquer** (la description écrite, l'explication cachée, `?reponse=decrire` ; l'ancienne question 2q → q, ses réactions et sa démonstration gardent leurs voix). |
| `thymidine` (2017 R, 1,5 pt) | `ig_r7`, `ig_r8` (la leçon) | **ajouté** : l'exercice du national joué en quatre temps sur une nouvelle vue `thymidine.html?vue=document` (le document seul : plantule, chromosome métaphasique après chaque cycle, ni molécules ni brins) : `ig_x3_thymidine_doc` **décrire** le 2ᵉ résultat (sa légende se tait, `conclusions=false`) ; `ig_x3b_cycle1` **expliquer** le 1er cycle (question, puis la chaîne en flèches du barème) ; `ig_x3c_cycle2` **expliquer** le 2ᵉ (idem) ; `ig_x3d_schema` le **schéma** demandé (vue `experience`, brins en couleur, arrêtée avant la conclusion écrite) puis la **conclusion** demandée à l'élève (semi-conservative). |
| `definir` (2024 N, association) | — | **reste** : l'association de 2024 N (ADN polymérase, centromère, nucléosome, ribosome) n'a pas de diapositive jouée ; le ribosome est du chapitre 4. Le vrai/faux du bloc (`ig_s8_b3`) reprend le nucléosome. À faire si l'on veut la jouer : une vue « associer » (étiquettes à poser, comme `?vue=legender`). |

### Simulations : ce qui a été ajouté (le cours en ligne voit tout comme avant)

- `noyau.html?vue=trois` : nouvelle vue (amibe, acétabulaire greffée, grenouille de Gurdon peintes ; moments `amibe`,
  `acetabulaire`, `gurdon`, `commun` ; repères `exp_amibe`, `exp_acetabulaire`, `exp_gurdon`, `commun`).
- `meselson.html` : paramètre `conclusions` (défaut `true`, aussi `?conclusions=false`) ; `false` tait l'hypothèse
  rejetée à la génération en cours et la conclusion finale ; ne relance pas la scène.
- `thymidine.html?vue=document` : nouvelle vue (moments `cycle_1`, `metaphase_1`, `transfert`, `metaphase_2`) ;
  paramètre `conclusions` (défaut `true`) qui tait « une chromatide marquée sur deux ». La vue `experience` est inchangée.
- `documents.html` : paramètre `reponse` de la vue `courbe` (`tout` par défaut ; `rien` = la courbe seule ;
  `decrire` = la description sans l'explication) ; nouvelle vue `metaphase` (QCM 2018 R, moments `carte`, `elimine_a`,
  `elimine_b`, `elimine_d`, `reponse`).
- `etapes.js` : **`Peint.courbe` manquait** — `documents.html?vue=courbe` et `cycle.html?vue=courbe` l'appelaient et
  s'arrêtaient sur une erreur (« Peint.courbe is not a function ») : la courbe de l'ADN ne se dessinait pas, ni ses
  légendes (cours en ligne compris, `ig_c3`, `ig_c4`, `ig_c5`, `ig_x2`). Ajoutée (morceaux colorés par phase, aire douce).
- Vérifié dans Chromium à 1024 × 560, 724 × 350 et 1366 × 613 : aucune erreur console, chaque moment atteint par
  `postMessage {simulation_control, play_until}`, `ce_qui_se_voit` conforme, textes ≥ 15 px (le kit agrandit).

### Séances

La séance 7 finit par la restitution (`ig_s7_b3` : `ig_x1`, `ig_x1b`, `ig_x1c`, `ig_x1d`). Une **séance 8** « Les
exercices du national pas à pas, et le bilan » : `ig_s8_b1` la courbe (décrire, expliquer), `ig_s8_b2` la thymidine
(quatre temps), `ig_s8_b3` le bilan (`ig_b1`, `ig_b2`). Partie VIII : 50 min ; cours : 345 min. Compétences : C3
(courbe), C7 (thymidine) et C8 (toutes les diapositives d'examen).

### Ce qui reste, et pourquoi

- `definir` (association 2024 N) : voir le tableau.
- Les questions d'observation du cours sont déjà nombreuses (8) ; les nouveaux exercices utilisent des **questions**
  (posées après la voix), jamais une observation de plus.
- Les écarts « gestes trop serrés » des diapositives nouvelles ou réécrites viennent de l'absence de voix (durée
  inconnue) ; les 20 « introuvable » du contrôle de pointage existent déjà, identiques, dans le cours en ligne (repères
  et moments calculés de `bacteries.html` et `mitose.html`, que le contrôle ne lit pas).

## 6. Voix

**2ᵉ passe** : `svt_ch3_notion_information_genetique_voix.json` compte maintenant **123 pistes** (59 de plus) : les
diapositives réécrites `ig_x1_restitution`, `ig_x2_exercice` et les nouvelles `ig_x1c`, `ig_x1d`, `ig_x2b`, `ig_x3`,
`ig_x3b`, `ig_x3c`, `ig_x3d` ; leurs réactions préparées (une par option, deux essais) ; leurs énoncés ; trois
démonstrations du barème (`ig_m4_anaphase`, `ig_x3b`, `ig_x3c`) et celle d'`ig_x2_exercice`. Gardent leur voix :
`ig_x1b_corrige` (l'ancien texte d'`ig_x1`), l'ancienne question d'`ig_x2` passée sur `ig_x2b` (énoncé, réactions,
démonstration), `ig_l6_definition` (texte inchangé). Mots vérifiés (`verifier_mots.py`) : darija rare remplacé
(الجيهتين → بيناتهم, تجاوبش → خود الوقت ديالك, تهدم → مشا, قديمة → القدام, كتحتفظ → كيبقى فيها, كتضاعف → كتولي جوج
مرات, كتمشيش/كيمشيش → كتبقى/كيبقى, كنكتبوه → نكتبو هادشي, كيتفرقو → كل وحدة كتمشي ل pôle, كيتكثف → كيولي condensé,
consigne → سؤال, le bleu / le rouge / le blanc → الزرق / الأحمر / الأبيض, montée → augmentation). Restent, mots du
programme ou du sujet **à écouter** : barème, thymidine, plantule, fève, marquée(s), métaphasique, molécule fille,
conservative, dispersive, semi-conservative, condensé, formé.

1re passe : 64 pistes — 9 diapositives réécrites ou nouvelles (`ig_l5`,
`ig_l6`, `ig_p1`, `ig_c6`, `ig_c6b`, `ig_m4`, `ig_m4b`, `ig_t1f`, `ig_r4`), 5 réactions et 1 énoncé (question de
`ig_l6`), 49 champs des 7 nouvelles questions d'observation. Les 54 autres diapositives gardent leur id et leur texte :
leur voix reste.

Mots vérifiés par la règle de `verifier_mots.py` (fréquence dans le corpus de la voix) : les mots darija rares ont été
remplacés (كيصاوب → كيدير, حلينا → شفنا داخل, كيختفي → كيمشي, تأكدات → صحيحة, كتفسر, كيتفرقو, نبنيو, ما معطيش…).
Restent, gardés parce que ce sont des mots du programme que l'élève doit entendre — **à écouter** (skill
prononciation) : Gurdon, rhizoïde, mediterranea, crenulata, crénelé, têtard, pigmentée, ovule, l'acétabulaire,
l'amibe, instructions, portées, commandent (définition mot pour mot), diploïde, homologues, décondensation, fuseau,
dispersive, semi-conservative, léger/légères.

## 7. Reproduire

`python3 scripts/logique/refaire_svt_ch3.py` (1re passe ; relit le cours en ligne, écrit la version en attente : déplacements,
réécritures, observations, séances recoupées, contrôle de chaque `mot` de pointage et de chaque `apres_mot`), puis
`python3 scripts/logique/passe2_svt_ch3.py` (2ᵉ passe, sur la copie en attente, idempotent), puis
`python3 -X utf8 scripts/logique/lister_voix.py svt_ch3_notion_information_genetique` (liste des voix et mots rares).
Vérifications : `cd backend && python -m pytest -q app/tests -k "course or cours or concentration"`,
`python backend/scripts/verifier_figures_cahier.py backend/data/courses/en_attente/svt_ch3_notion_information_genetique.json`
(0 erreur), `python backend/scripts/verifier_pointage_simulations.py backend/data/courses/en_attente/svt_ch3_notion_information_genetique.json --ecarts`
(aucun écart nouveau par rapport au cours en ligne ; les « gestes trop serrés » des 9 diapositives sans voix
disparaîtront avec leur durée réelle).
