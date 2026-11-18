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

## 5. Animations et besoins notés (fichiers non modifiés)

- `noyau.html?vue=gurdon` sert aussi à `ig_l6_definition` (arrêt sur `adulte_albinos`) ; une vue « trois expériences
  côte à côte » (amibe, chapeau greffé, grenouille) serait meilleure : à faire dans la simulation du cours.
- `meselson.html` : pour les observations de G1 et G2, la simulation devrait accepter `{conclusions: false}` pour
  masquer « conservative rejetée » / « dispersive rejetée » tant que l'élève n'a pas répondu (comme
  `bacteries.html?conclusions=false`). En attendant, ces mentions apparaissent sur leurs moments, après la question.
- `documents.html?vue=durees` : `ig_c6b_phases` démarre au moment `duree_cycle` ; si la simulation repart de zéro,
  ajouter `&diapo=c6b_phases` à son départ.
- `mitose.html?vue=animale&diapo=m4_anaphase` sert aux deux diapositives `ig_m4` et `ig_m4b` (départ à 13,2 s).

## 6. Voix

`svt_ch3_notion_information_genetique_voix.json` : 64 pistes — 9 diapositives réécrites ou nouvelles (`ig_l5`,
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

`python3 scripts/logique/refaire_svt_ch3.py` (relit le cours en ligne, écrit la version en attente : déplacements,
réécritures, observations, séances recoupées, contrôle de chaque `mot` de pointage et de chaque `apres_mot`), puis
`python3 -X utf8 scripts/logique/lister_voix.py svt_ch3_notion_information_genetique` (liste des voix et mots rares).
Vérifications : `cd backend && python -m pytest -q app/tests -k "course or cours or concentration"`,
`python backend/scripts/verifier_figures_cahier.py backend/data/courses/en_attente/svt_ch3_notion_information_genetique.json`
(0 erreur), `python backend/scripts/verifier_pointage_simulations.py backend/data/courses/en_attente/svt_ch3_notion_information_genetique.json --ecarts`
(aucun écart nouveau par rapport au cours en ligne ; les « gestes trop serrés » des 9 diapositives sans voix
disparaîtront avec leur durée réelle).
