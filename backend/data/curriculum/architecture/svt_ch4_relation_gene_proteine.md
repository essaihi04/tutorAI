# Architecture — SVT ch4 « Relation gène – protéine » (`svt_ch4_relation_gene_proteine`)

Refaite le 18 novembre 2026 avec la skill `logique-de-cours`. Version en attente :
`backend/data/courses/en_attente/svt_ch4_relation_gene_proteine.json` (le cours en ligne n'est pas touché).
Script : `scripts/logique/refaire_svt_ch4.py`. Pistes à mettre en voix : `svt_ch4_relation_gene_proteine_voix.json`.

## 1. Sources consultées

- **Profs (vidéos)** : l'exploration `backend/data/curriculum/exploration/relation_gene_proteine.json` (10 vidéos) :
  ordre commun de 8 profs sur 10 « notions (caractère, gène, allèle, mutation) → relation gène – protéine – caractère
  → mécanisme (transcription puis traduction) → mutations et conséquences → exercice type national » ; schéma
  ADN → ARNm → protéine écrit au début par 6 profs sur 10 ; NC1 à NC8.
- **Cours écrits en ligne (plans relevés)** :
  1. Moutamadris, « Expression de l'information génétique », 2 Bac SP international : I caractère, gène, allèle,
     mutation (l'expérience des bactéries et de la streptomycine, puis gène et allèle) → II relation gène – protéine
     – caractère (drépanocytose : frottis, hémoglobine, acide aminé n° 6 ; puis relation gène – protéine) → III
     mécanisme : 1 mise en évidence d'un intermédiaire, l'ARNm → 2 structure et composition de l'ARNm → 3
     transcription → 4 traduction.
  2. Moutamadris, cours SP (37 p.) : … 3-5 gène, allèle, mutation → 4-1 relation gène – protéine – caractère → 4-2-1
     nécessité d'un intermédiaire entre l'ADN et les ribosomes → 4-2-2 nécessité d'un code génétique → 4-2-3
     traduction.
  3. AlloSchool, M. Bahsina, « Expression de l'information génétique », partie 1 : introduction (l'ADN support,
     l'expression = le décryptage) → notion de caractère (héréditaire ou non) → transformation bactérienne →
     gène, allèle, mutation → relation gène – protéine / protéine – caractère → conclusion.
  4. AlloSchool, M. Bahsina, devoir 2 modèle 1 (QCM : mutation, traduction dans le cytoplasme, nombre de molécules
     d'ADN).
- **Cadre** : `svt.json` (domaine 2, 2.1 et 2.2 : caractère, gène, allèle ; ARN ; transcription ; code ; traduction ;
  schéma gène → ARNm → protéine → caractère), `perimetre.json`, capacités de l'exploration.
- **National** (`cas_types`) : écrire l'ARNm et les acides aminés **17 sessions sur 20** ; origine génétique de la
  maladie **17 sur 20** (substitution faux-sens 10, non-sens 3, délétion 3, addition 1) ; relation protéine –
  caractère à partir d'un document **14** ; relation gène – protéine – caractère 4 ; étapes de la traduction sur
  schémas 1 (2018 R) ; restitution 2.

## 2. La logique avant (cours en ligne)

I : rappel ADN, **la protéine** (rappel), puis l'ouverture « d'où viennent tes caractères ? », gène, allèle, mutation
(7) → II drépanocytose aux trois échelles, LDL, albinisme, Beadle et Tatum (6) → III l'ARN (tableau ADN/ARN), « l'usine
au cytoplasme », uracile, acides aminés radioactifs, in vitro (5) → IV transcription (8) → V code (6) → VI traduction (6)
→ VII mutations (7) → VIII schéma (5) → IX examen (6) → bilan (2). 58 diapositives, 6 séances de ~60 min.

Ce qui n'allait pas :

| Diapositive | Problème | Règle |
|---|---|---|
| `rg_o1_caracteres` | l'ouverture vient **après** deux rappels, et elle **décrit le mécanisme entier** sur l'image (« une molécule orange sort du noyau… ce n'est pas l'ADN, c'est une copie ») : la réponse des parties III à VI est donnée avant la question, et l'ARNm « copie » est affirmé avant les marquages qui le prouvent | 3, 4 |
| `rg_d2_proteine` en tête du cours | la protéine est enseignée cinq diapositives avant qu'elle serve (`rg_p3`), au milieu des notions gène/allèle qui n'en ont pas besoin | 6 |
| `rg_a1_arn` avant `rg_a2_usine` | la molécule est donnée (« la cellule utilise l'ARN pour aller du noyau au caractère ») avant le problème qui la rend nécessaire | 3, 4 |
| `rg_a2_usine` | « les ribosomes : c'est là que se fabriquent les protéines » est affirmé **avant** l'expérience des acides aminés radioactifs (`rg_a4`) qui le montre | 4 |
| `rg_r3_elongation` | l'ARNt du codon suivant est donné par la voix ; l'élève ne cherche jamais lui-même un anticodon | 3, 5 |
| `rg_m2_substitution`, `rg_m3_non_sens` | l'effet de la mutation (même acide aminé ; codon stop) est dit avant que l'élève le lise dans le code — or c'est exactement la compétence des 17 sessions sur 20 | 3, 5 |
| séances de ~60 min | au-dessus de la limite de 40 à 50 min | 7 |

Ce qui était juste et reste : la mutation des bactéries posée en question avant sa conclusion (`rg_g3` puis `rg_g3b`,
comme Moutamadris), la drépanocytose descendue échelle par échelle, Beadle et Tatum avec le mutant 3 posé avant la
réponse, les acides aminés radioactifs déjà en observation, la transcription et la traduction animées étape par étape
(`transcription.html`, `traduction.html` : initiation, élongation, terminaison, polysome), Nirenberg après le
raisonnement 4³ = 64, les trois schémas à légender (`legende_*` : transcription, traduction, schéma bilan), les
mutations jugées par le code, la partie examen calquée sur le national (2023, 2024, 2025).

## 3. La logique après — séances, blocs, diapositives et pourquoi

Ordre des parties inchangé : c'est celui des 8 profs sur 10, des deux cours Moutamadris et du cadre (2.1 puis 2.2).
58 diapositives, **7 séances** de 3 blocs (365 min, ~52 min par séance au lieu de ~61).

Légende : ▶ animation ; 👀 question d'observation (cas décisif, la voix s'arrête avant le résultat) ; ✏️ question « À
toi » du bloc ; ✱ diapositive réécrite (voix à refaire).

### Séance 1 — Caractère, gène, allèle, mutation (C1)

**Bloc 1 — La question du chapitre ; l'ADN**
1. `rg_o1_caracteres` ✱ — *avancée en tête et réécrite* : caractère héréditaire et phénotype (définitions mot pour
   mot, 2018 R), le rappel « l'information est dans le noyau, dans l'ADN », puis **la question du chapitre** :
   « comment l'information du noyau devient-elle un caractère ? ». L'image reste à l'écran mais n'est plus
   expliquée : « à la fin du chapitre, c'est toi qui l'expliqueras ». Les 6 profs qui écrivent le schéma au début
   donnent la réponse avant la question ; on garde leur image comme fil rouge, pas comme réponse (règles 3 et 4).
2. `rg_d1_adn` ▶ — le rappel de l'ADN au moment où il sert : le gène est une portion d'ADN (diapositive suivante).

**Bloc 2 — Le gène et l'allèle** (NC1)
3. `rg_g1_gene` — gène = portion d'ADN à un locus ; 4. `rg_g2_allele` ▶ ✏️ — locus et allèles sur la paire n° 9.

**Bloc 3 — Une mutation crée un nouvel allèle**
5. `rg_g3_mutation` ▶ ✏️ — l'expérience des bactéries (streptomycine) avant la notion, la question avant la
   conclusion (Moutamadris, I-2) ; 6. `rg_g3b_mutation` ▶ — la définition, dite deux fois (une lettre change).

### Séance 2 — La protéine et le caractère (C2)

**Bloc 1 — Une protéine ; la drépanocytose, de l'organisme à la cellule**
7. `rg_d2_proteine` ▶ ✏️ — *déplacée au début de la partie II* : la protéine (perles, l'ordre fait la protéine)
   enseignée juste avant la partie qui en a besoin (règle 6) ; elle sera redite autrement en `rg_p3` (le collier,
   l'hémoglobine) : deux explications de deux façons.
8. `rg_p1_organisme` ▶, 9. `rg_p2_cellule` ▶ — phénotype macroscopique puis cellulaire.

**Bloc 2 — La protéine en cause ; lire un document**
10. `rg_p3_proteine` ▶ — phénotype moléculaire (Glu 6 → Val) ; 11. `rg_p4_document` ▶ ✏️ — lire un document
    (LDL, national 2023) : le cas type `proteine_caractere`, 14 sessions sur 20.

**Bloc 3 — Albinisme, Beadle et Tatum**
12. `rg_p4b_albinisme`, 13. `rg_p5_beadle_tatum` ✏️ — un gène, une enzyme ; le mutant 3 posé avant la réponse.

### Séance 3 — L'ARN messager, puis la transcription (C3, C4)

**Bloc 1 — Le problème, l'ARN, l'uracile radioactif** (NC3)
14. `rg_a2_usine` ✱ ▶ — *avancée et réécrite* : le problème d'abord (Moutamadris : « mise en évidence d'un
    intermédiaire » avant « structure de l'ARNm ») : l'ADN ne sort pas du noyau ; **les protéines, où sont-elles
    fabriquées ?** — la voix ne l'affirme plus, elle le demande ; la photocopie devient une hypothèse (« la cellule
    fait-elle pareil ? »).
15. `rg_a1_arn` ✱ ▶ — la molécule candidate, présentée avant les expériences parce que l'uracile marqué n'a de sens
    que si l'on sait que U n'est que dans l'ARN ; seule la première phrase change (« avant les expériences, une
    molécule à connaître »), au lieu d'affirmer que la cellule s'en sert pour aller au caractère.
16. `rg_a3_uracile` ▶ — l'ARN fabriqué au noyau migre au cytoplasme.

**Bloc 2 — Les protéines au cytoplasme : l'ARNm est nécessaire**
17. `rg_a4_acides_amines` ▶ 👀 ✏️ — les protéines se font sur les ribosomes : la réponse à la question de `rg_a2`
    vient de l'expérience (observation déjà en ligne) ; 18. `rg_a5_in_vitro` ✏️ — sans ARNm, pas de protéine.

**Bloc 3 — La transcription : définition et arbre de Noël** (NC4)
19. `rg_t1_rappel` ▶, 20. `rg_t2_definition` ▶, 21. `rg_t2b_arbre_noel` ✏️.

### Séance 4 — La transcription comme le barème, puis le code (C4, C5)

**Bloc 1** — 22. `rg_t3_bases` ▶ ✏️ (A → U, jamais T), 23. `rg_t4_sens` ▶ (3' → 5' lu, ARNm 5' → 3'),
24. `rg_t5_non_transcrit` ▶ (la question qui fait perdre le plus de points).
**Bloc 2** — 25. `rg_t5b_legender` ▶ (`legende_*`), 26. `rg_t6_bareme` ✏️ (écrire l'ARNm : 17 sessions sur 20).
**Bloc 3** (NC5) — 27. `rg_c1_codon` ▶ (le raisonnement 4, 16, 64 avant le mot codon), 28. `rg_c1b_nirenberg` ✏️ (la
preuve expérimentale), 29. `rg_c2_tableau` ▶ (lire le tableau).

### Séance 5 — Le code, puis la traduction (C5, C6)

**Bloc 1** — 30. `rg_c3_initiation_stop` ▶ ✏️, 31. `rg_c4_traduire` ▶, 32. `rg_c5_proprietes` ▶ (redondance,
universalité : elles serviront aux mutations).
**Bloc 2** (NC6) — 33. `rg_r1_acteurs` ▶ ✏️ (les acteurs arrivent un par un), 34. `rg_r2_initiation` ▶,
35. `rg_r3_elongation` ▶ 👀 — **nouvelle question d'observation** : « le codon suivant est CGC : quel ARNt vient ? »
avant que la voix ne nomme l'anticodon GCG ; la traduction est ainsi jouée pas à pas *par l'élève* (codon → anticodon
→ acide aminé), pas seulement montrée.
**Bloc 3** — 36. `rg_r4_terminaison` ▶, 37. `rg_r5_polysome` ▶ ✏️, 38. `rg_r6_legender` ▶ (`legende_*`).

### Séance 6 — Les mutations, et le schéma bilan (C7, C8, C6)

**Bloc 1 — Comparer les allèles ; silencieuse, faux-sens, non-sens** (NC7)
39. `rg_m1_comparer` ▶ ; 40. `rg_m2_substitution` ▶ 👀 — **nouvelle question d'observation** : « CUG devient CUA :
quel acide aminé ? » (l'élève lit le tableau, découvre la redondance) ; 41. `rg_m2b_faux_sens` ▶ ;
42. `rg_m3_non_sens` ▶ 👀 ✏️ — **nouvelle question d'observation** : « UGG devient UAG : que se passe-t-il ? » avant
que la voix ne dise « codon stop » (cas du national 2018 N, 2023 N, 2024 R).
**Bloc 2** — 43. `rg_m4_decalage` ▶, 44. `rg_m5_trois` ▶, 45. `rg_m6_juger` ▶ ✏️ (l'élève change une base lui-même).
**Bloc 3** — 46. `rg_s1_gpc` ▶, 47. `rg_s2_schema` ▶, 48. `rg_s3_construire` ▶ ✏️ (construire le schéma : l'image
de l'ouverture est maintenant expliquée par l'élève).

### Séance 7 — Rédiger comme le barème, l'exercice national et le bilan (C8)

**Bloc 1** — 49. `rg_s4_trans_trad` ▶, 50. `rg_s5_etapes` ▶ (2018 R), 51. `rg_e1_restitution` ▶ ✏️.
**Bloc 2** — 52. `rg_e2_reperages` ▶, 53. `rg_e3_lignes` ▶, 54. `rg_e4_phrase` ▶ ✏️.
**Bloc 3** — 55. `rg_e5_national` ▶ ✏️ (national 2024), 56. `rg_e6_drepanocytose` ▶ ✏️ (retour à l'exemple du
début), 57. `rg_b1_bilan`, 58. `rg_b2_carte`.

## 4. Ce qui change, en bref

| Avant | Après | Raison |
|---|---|---|
| d1, d2, o1, g… | o1, d1, g… ; d2 en tête de la partie II | la question avant les rappels ; la protéine là où elle sert |
| o1 explique l'image (copie orange, machine, chaîne) | o1 pose la question ; l'image est expliquée par l'élève en `rg_s3` | ne pas donner la réponse au départ |
| a1 (ARN) puis a2 (usine : « les protéines se font sur les ribosomes ») | a2 (problème, sans réponse) puis a1 (la molécule) | le problème d'abord (Moutamadris) ; le lieu de synthèse prouvé par `rg_a4`, pas affirmé |
| élongation, silencieuse, non-sens : le résultat est dit | trois questions d'observation | le code et la traduction joués par l'élève, pas à pas |
| 6 séances (~61 min) | 7 séances (~52 min) | règle 7 |

Questions d'observation : 4 (1 en ligne + 3 nouvelles), sur des voix **inchangées** pour `rg_r3`, `rg_m2`, `rg_m3`.

## 5. Animations et besoins notés

- **Fait en 2ᵉ passe** (voir § 8) : les cinq documents lus en tableau naissent d'une animation (`documents.html`) ;
  `mutation.html` accepte `{conclusions: false}` et les observations de `rg_m2`, `rg_m3` s'en servent.
- `adn_arnm_proteine.png` (ouverture) : une version sans légendes ni flèches suffirait comme « image à expliquer »
  (image, pas une simulation : non fait).
- `traduction.html` (observation de `rg_r3`) : relue — au moment `elongation` où la voix s'arrête, l'ARNt GCG n'est pas
  encore arrivé (moment `arnt_2_arrive`, plus loin) ; rien à cacher. `marquage.html` (`rg_a4`) tait déjà sa conclusion.

## 6. Voix

`svt_ch4_relation_gene_proteine_voix.json` (régénéré après la 2ᵉ passe) : **80 pistes** — 10 diapositives (les 3 de la
1re passe, `rg_e5_national` réécrite, 6 nouvelles `rg_e5a`, `rg_e7`, `rg_e7b`, `rg_e7c`, `rg_e8`, `rg_e8b`), 35 réactions,
7 démonstrations, 7 énoncés, 21 champs d'observation (1re passe). Les cinq documents animés (`rg_p4b`, `rg_p5`, `rg_a5`,
`rg_t2b`, `rg_c1b`) et `rg_m2`, `rg_m3` gardent leur texte, donc leur voix ; la question et l'exercice de
`rg_e5_national` gardent les leurs (même texte).

Mots vérifiés (même règle que `verifier_mots.py`, lancé sur `en_attente/svt_ch4_relation_gene_proteine`). 1re passe :
darija rare remplacé (تشرحها, كنخرجوش, تبدلاتش, كتحبس, كورات, وكتنتقل, البرتقالي). 2ᵉ passe : السنان → الأسنان,
كيفرزو → كيخرجو, كتموت / كتبداش / تموت → « la mortalité كتوصل cent pour cent », ما بقاتش كتخدم → كتوقف, تبدلاتش →
ثابتة, كتتكتب → كنكتبو, كيحددها → هو اللي كيحدد, كتفسر → كتبين, سطور → سطر, كنساليو → ف اللخر, صحيحين → مزيانين,
ضاع → مشى, يدخلش → ما بقاش كيدخل, الموستيك → les moustiques, كيخدموش → ما كيديرو والو ; les abréviations Ile, Phe,
Gly ne sont plus lues (« la glycine », « la sérine »). Aucun mot darija rare dans les pistes nouvelles.
Restent, mots du programme ou des sujets à écouter (skill prononciation) : anticodon, redondance, redondant,
silencieuse, faux-sens, méthionine, observables, ribose, l'uracile, marquage ; et en 2ᵉ passe : amélogénèse,
acétylcholinestérase, acétylcholine, carbamate, Culex, synapses, insecticide, moustiques, mortalité, milligrammes,
résistants, conditionnel, Blackfan-Diamond, anémie, globules, hémoglobine, sous-unité(s), fonctionnels, complémentarité,
barème, quarante-trois, quarante-sept.

## 7. Reproduire

`python3 scripts/logique/refaire_svt_ch4.py` (relit le cours en ligne, écrit la version en attente, contrôle chaque
`mot` et chaque `apres_mot`), puis `python3 scripts/logique/passe2_svt_ch4.py` (2ᵉ passe, sur la version en attente), puis `python3 -X utf8 scripts/logique/lister_voix.py svt_ch4_relation_gene_proteine`.
Vérifications : `cd backend && python -m pytest -q app/tests -k "course or cours or concentration"`,
`python backend/scripts/verifier_figures_cahier.py backend/data/courses/en_attente/svt_ch4_relation_gene_proteine.json`
(0 erreur), `python backend/scripts/verifier_pointage_simulations.py backend/data/courses/en_attente/svt_ch4_relation_gene_proteine.json --ecarts`
(aucun écart nouveau ; les « gestes trop serrés » des 3 diapositives sans voix disparaîtront avec leur durée réelle).

## 8. 2ᵉ passe (18 novembre 2026) — chaque cas type du national joué pas à pas

Demande : « simple, animé, expliqué ; ne pas tout donner au départ ; laisser à l'élève le temps de trouver seul ; une
raison derrière chaque choix ». Script : `scripts/logique/passe2_svt_ch4.py`.

### Les cas types du national (exploration `relation_gene_proteine.json`, `cas_types`) et où ils sont joués

| Cas type (fréquence) | Déjà joué en animation, pas à pas | Ajouté en 2ᵉ passe |
|---|---|---|
| `arn_aa` (17/20) | `rg_t6_bareme`, `rg_c4_traduire` (tableau du code animé), `rg_e3_lignes` (méthode) | la consigne 2 du 2024 N (`rg_e5_national`) : les deux brins seuls, l'élève écrit l'ARNm et l'acide aminé avant la correction ; le triplet 247 du 2020 N (`rg_e7c_verifier`) |
| `origine_genetique` (17/20) | `rg_e4_phrase` (la phrase maillon par maillon) | l'exercice de `rg_e5_national` (consigne 3, après la consigne 2) ; la vérification du 2020 N (`rg_e7c_verifier`, exercice) |
| `proteine_caractere` (14) | `rg_p4_document` (2023 N, LDL, `examen.html?vue=document_ldl`, maillon par maillon) | la consigne 1 du 2024 N (`rg_e5a_document`) : le document d'abord, la réponse de l'élève, puis la correction en deux lignes |
| `relation_gpc` | `rg_s1_gpc`, `rg_e6_drepanocytose` | — (elle termine chaque phrase d'origine génétique) |
| `hypothese_verification` (2020 N, 2020 R) | aucun | **2020 N, moustiques résistants** : `rg_e7_moustiques` (documents 1 et 2 animés → relation), `rg_e7b_hypothese` (proposer, au conditionnel), `rg_e7c_verifier` (document 3 → ARNm, acide aminé → vérifier) |
| `etapes_traduction` (2018 R) | `rg_r2`…`rg_r4` (initiation, élongation, terminaison jouées), `rg_s5_etapes` (`traduction.html?vue=trois_schemas`) | — |
| `restitution` | `rg_e1_restitution` (cartes écrites une à une, QCM, vrai / faux) | — |
| `ribosome_document` (2022 N) | aucun | **2022 N, Blackfan-Diamond** : `rg_e8_ribosomes` (histogramme qui pousse → comparer), `rg_e8b_hemoglobine` (assemblage des ribosomes → expliquer) |

**Pourquoi rejouer le 2024 N** : `rg_e5_national` lisait les trois réponses dans la voix, puis posait la question 2 dont
la réponse venait d'être dite (règle 3 : ne pas tout donner au départ). Il devient deux diapositives sur une nouvelle vue
`examen.html?vue=amelogenine_pas` qui écrit une consigne à la fois et sa réponse seulement au moment suivant :
`rg_e5a_document` (document → consigne 1 → QCM, la correction en deux lignes comme le barème) puis `rg_e5_national`
(la réponse 1 écrite, les deux brins seuls → consigne 2 → QCM ; puis l'exercice de la consigne 3, dont la démonstration
écrit la phrase du barème). La question et l'exercice gardent leur texte et leur voix.

**Pourquoi ces deux sujets** : `hypothese_verification` et `ribosome_document` étaient les deux cas types sans aucun
exercice dans le cours. 2020 N (moustiques) est le seul sujet qui enchaîne relation → hypothèse → vérification par les
séquences, la démarche entière ; 2022 N (Blackfan-Diamond) est le seul document du national sur le ribosome. Valeurs
lues sur les figures des sujets (`backend/data/exams/svt/2020-normale/assets/doc2p6.png`, `doc3p6.png` ; corrigé 2022 N) :
activité de l'AChE S 97, 8, 0 % et R 32, 32, 28 % (0, 10⁻², 1 mg/L) ; mortalité S 0 → 100 % de 0,1 à 1 mg/L, R de
2·10² à environ 1,2·10³ mg/L ; triplets 243 à 251, GGC → AGC au triplet 247 ; sous-unités 46 / 46 UA (sain), 46 / 23 UA
(malade). Chaque consigne a sa diapositive, sa question posée après la voix, une réaction préparée pour chaque option
(juste ; 1er essai : un indice ; 2e essai : la réponse et pourquoi), et la correction écrite comme le barème la lit
(`question.demonstration.lignes`). Rien de la réponse n'est au tableau avant la question : `moustiques_seq` n'écrit
l'ARNm et les acides aminés qu'aux moments `arnm` / `acides_amines`, que les diapositives n'atteignent pas.

### Les documents lus en tableau naissent d'une animation (règle 35) — voix gardées

Nouveau fichier `svt/relation_gene_proteine-tableau/documents.html`, une vue par document ; la diapositive garde son texte
(et donc sa voix), seuls `visual` et `pointage` changent, sur des mots déjà dits :
- `rg_p4b_albinisme` → `?vue=albinisme` : deux cellules de la peau peintes ; la tyrosine (billes jaunes) devient mélanine
  (grains bruns) chez la personne saine, s'entasse devant la tyrosinase déformée chez l'albinos ; peau et cheveux peints ;
  le tableau s'écrit ligne par ligne sur « السطر اللول / الثاني / الثالث ».
- `rg_p5_beadle_tatum` → `?vue=beadle` : la chaîne précurseur → ornithine → citrulline → arginine, puis seize boîtes de
  culture où Neurospora (feutrage orangé) pousse ou non ; « E1 bloquée », « E2 bloquée » écrits quand la voix les déduit ;
  **rien pour le mutant 3** : c'est la question de la diapositive.
- `rg_a5_in_vitro` → `?vue=in_vitro` : le tube peint (ribosomes, acides aminés radioactifs, ni ADN ni ARNm), la seringue
  d'ARNm, les deux courbes tracées au fil du temps, puis les trois lignes du tableau.
- `rg_t2b_arbre_noel` → `?vue=arbre_noel` : l'électronographie se développe, puis tronc, branches et points sont teintés
  et nommés une ligne à la fois ; « début du gène » et le glissement des polymérases ne viennent qu'au moment `sens`,
  après la question (« où est le début du gène ? »).
- `rg_c1b_nirenberg` → `?vue=nirenberg` : le ribosome lit l'ARNm poly-U puis UG répété par trois (codons entourés), la
  chaîne sort ; « lu par deux » barré ; pour le poly-C, ni codon entouré ni « CCC → Pro » : c'est la question.

### Rien de décisif avant la réponse

`mutation.html` : nouveau réglage `conclusions` (défaut `true` : le cours en ligne voit la page comme avant ; aussi
`?conclusions=false`). À `false`, l'allèle muté s'arrête à son ARNm : acides aminés, « arrêt », type de mutation,
conséquence et décalage restent cachés ; repasser à `true` ne rejoue pas la scène (la réponse s'écrit sur place).
Branché sur les observations de `rg_m2_substitution` (« CUA donne quel acide aminé ? ») et `rg_m3_non_sens`
(« que se passe-t-il à ce codon ? ») : `sim_avant {conclusions: false}`, `sim_apres {conclusions: true}`.

### Séances

Séance 7 : b1, b2 inchangés ; b3 « Le sujet 2024 N, une consigne à la fois » (`rg_e5a`, `rg_e5`). Nouvelle séance 8 :
b1 « 2020 N : la relation, l'hypothèse, la vérification » (`rg_e7`, `rg_e7b`, `rg_e7c`), b2 « 2022 N : un document sur le
ribosome » (`rg_e8`, `rg_e8b`), b3 « Retour à la drépanocytose, et le bilan » (`rg_e6`, `rg_b1`, `rg_b2`, cahier,
« retrouver » et exercice repris de l'ancien bloc). Partie IX : 75 min ; cours : 395 min.

### Ce qui reste, et pourquoi

- Voix : 80 pistes à faire sur le VPS (quota Kaggle épuisé ici).
- Les diapositives nouvelles ont des « gestes trop serrés » au contrôle de pointage : leur durée n'est connue qu'avec la
  voix ; à revoir quand elle sera faite.
- La vue `blackfan` montre l'hémoglobine produite pendant la consigne « expliquez » : c'est la figure b du sujet
  elle-même (le document donné), l'élève doit écrire la chaîne causale ; le QCM porte sur cette chaîne.
- Le test `test_pointage_simulations.py::test_le_cours_de_svt_liberation_de_l_energie_est_sans_ecart` échoue : il porte
  sur le cours SVT ch1, que cette session n'a pas touché.

