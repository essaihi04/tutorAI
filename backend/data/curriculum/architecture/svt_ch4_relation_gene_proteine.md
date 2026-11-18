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

## 5. Animations et besoins notés (fichiers non modifiés)

- `rg_p4b_albinisme`, `rg_p5_beadle_tatum`, `rg_a5_in_vitro`, `rg_t2b_arbre_noel`, `rg_c1b_nirenberg` sont encore
  des tableaux de document sans animation (`visual.kind: none`). Règle 35 : leurs données devraient **naître d'une
  animation** — boîtes de culture des mutants de Neurospora qui poussent ou non selon le milieu (un curseur : la
  substance ajoutée), tube in vitro dont le compteur d'acides aminés incorporés monte après chaque injection d'ARNm,
  ARNm poly-U lu par trois et qui sort Phe – Phe – Phe. À faire dans `svt/relation_gene_proteine-tableau/` (nouvelles
  vues), puis remplacer `visual` et le `pointage` sur les mots déjà dits.
- `mutation.html` : pour les observations de `rg_m2` et `rg_m3`, la simulation devrait accepter
  `{conclusions: false}` pour masquer « silencieuse » / « stop » tant que l'élève n'a pas répondu.
- `adn_arnm_proteine.png` (ouverture) : une version sans légendes ni flèches suffirait comme « image à expliquer ».

## 6. Voix

`svt_ch4_relation_gene_proteine_voix.json` : 24 pistes — 3 diapositives réécrites (`rg_o1_caracteres`, `rg_a2_usine`,
`rg_a1_arn`) et 21 champs des 3 nouvelles questions d'observation. Les 55 autres diapositives gardent leur id et leur
texte : leur voix reste.

Mots vérifiés (même règle que `verifier_mots.py`) ; darija rare remplacé (تشرحها, كنخرجوش, تبدلاتش, كتحبس, كورات,
وكتنتقل, البرتقالي). Restent, mots du programme à écouter : anticodon, redondance, redondant, silencieuse, faux-sens,
méthionine, observables, ribose, l'uracile, marquage (« hématies » est déjà réécrit par une règle de prononciation).

## 7. Reproduire

`python3 scripts/logique/refaire_svt_ch4.py` (relit le cours en ligne, écrit la version en attente, contrôle chaque
`mot` et chaque `apres_mot`), puis `python3 -X utf8 scripts/logique/lister_voix.py svt_ch4_relation_gene_proteine`.
Vérifications : `cd backend && python -m pytest -q app/tests -k "course or cours or concentration"`,
`python backend/scripts/verifier_figures_cahier.py backend/data/courses/en_attente/svt_ch4_relation_gene_proteine.json`
(0 erreur), `python backend/scripts/verifier_pointage_simulations.py backend/data/courses/en_attente/svt_ch4_relation_gene_proteine.json --ecarts`
(aucun écart nouveau ; les « gestes trop serrés » des 3 diapositives sans voix disparaîtront avec leur durée réelle).
