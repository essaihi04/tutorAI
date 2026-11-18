# Architecture — État d'équilibre d'un système chimique (`phys_ch12_etat_equilibre`)

Logique refaite le 18 novembre 2026, avec la skill `logique-de-cours`. Elle est appliquée dans `backend/data/courses/en_attente/phys_ch12_etat_equilibre.json`. Le cours en ligne n'a pas été touché.

Les pistes à mettre en voix sont dans `phys_ch12_etat_equilibre_voix.json` (49 pistes, toutes des questions d'observation).

## 1. Sources

### Les profs

Ce chapitre n'a pas de fichier d'exploration. J'ai donc relevé le plan de 5 cours complets en ligne :

1. **N. Naceiri Mrabti**, livre 2BAC BIOF, p. 149-158 (PDF).
   - Situation-problème : « quelle grandeur caractérise un état d'équilibre ? ».
   - Ordre : Qr (conventions eau = 1, solides = 1), Qr,éq, K, facteurs de τ.
   - K est amené par une activité : σ de trois solutions d'acide éthanoïque, τ puis Qr,éq ≈ 1,8·10⁻⁵ constant.
   - Facteurs de τ : l'état initial, puis K.
2. **El Goufifa**, AlloSchool, séance 9.
   - Ordre : Qr, Qr,éq (par conductimétrie), K, influence de l'état initial puis de K sur τ, exercices (aspirine, acide méthanoïque, acide benzoïque, méthylamine).
3. **Moutamadris**, cours PC 2BAC SP international.
   - Même plan qu'El Goufifa.
   - K est affirmé (« les études expérimentales ont montré… ») au lieu d'être montré.
4. **Fiche pédagogique 2BAC PC + SM**.
   - Ordre : Qr, Qr,éq (conductimétrie), K, composition initiale puis K.
   - Expériences : étalonnage du pH-mètre, pH de HCl et de CH₃COOH, conductance.
5. **Prof Bazhar**, vidéo « État d'équilibre d'un système chimique 2bac biof ».
   - Chapitres : Qr, Qr à l'état initial, Qr à l'équilibre, K, taux d'avancement final.

**Ordre commun aux 5 sources** : Qr → Qr,éq → K → de quoi dépend τ (état initial, puis K).

La meilleure introduction de K est celle de Naceiri : plusieurs concentrations, le même Qr,éq. C'est déjà notre `ee_k1_trois`.

### Le cadre

`cadre_reference_2bac_pc.json`, clé `etat_equilibre`, capacités EE1 à EE7. `perimetre.json`, clé `acides_bases`, sous-domaine 2 du cadre officiel (« transformations non totales »).

Hors cadre dans ce chapitre : Ka, Ke (au ch13), le critère d'évolution Qr,i/K (sous-domaine 3), Le Chatelier, activité, c°.

### Le national

`backend/data/exams/physique`, 20 sujets de 2016 à 2025, exercice de chimie, recherche par mots-clés :

| Cas type | Sujets |
|---|---|
| K, constante d'équilibre | 11/20 |
| τ, taux d'avancement final | 11/20 |
| Qr ou Qr,éq littéral | 8/20 |
| Qr,i d'un état initial ou d'un mélange | 7/20 |
| K = C·τ²/(1 − τ), exprimer K en fonction de τ | 4/20 |
| Conductimétrie | 3/20 |

Le temps va donc d'abord à Qr,éq et K à partir du pH, puis à Qr,i d'un mélange, puis à K par la conductivité.

## 2. La logique avant

10 parties dans cet ordre :

1. Ouverture : la carte du chapitre, puis deux flacons.
2. Rappels de concentration et de puissances de dix.
3. Rappels de τ et de l'équilibre.
4. Qr.
5. Qr,i.
6. Qr,éq.
7. K.
8. Mesurer K.
9. Facteurs de τ.
10. Six nationaux racontés à la suite, puis le bilan.

Défauts relevés, avec la règle de la skill qu'ils enfreignent :

- **La carte d'ouverture (`ee_o1_carte`) donnait le résultat avant les mesures** (règles 3 et 4). Son titre et sa voix disaient « à l'équilibre, Qr,éq = K » avant que l'élève ait vu un seul Qr,éq.
- **`ee_o2_flacons` utilisait le pH, la concentration et τ = 10^(−pH)/C avant leurs rappels** (règle 6). Il venait avant `ee_z1`, `ee_z2` et `ee_r1`.
- **Le couple acide/base et le pH (pH = −log[H₃O⁺]) n'étaient enseignés nulle part** (règle 6). Pourtant toute la partie Qr,éq lit [H₃O⁺] = 10^(−pH).
- **Les six nationaux étaient racontés d'un bout à l'autre, à la fin, loin de leur notion** (règles 3, 5 et 7). La voix donnait chaque étape : l'élève n'en faisait aucune.
- **Les ardoises étaient trop proches.** `ee_r2_equilibre` (question) puis `ee_q2_generale` (question) n'avaient qu'une diapo entre elles. Le bloc « Qr » avait sa question au milieu (`ee_q2`), pas à la fin.
- **Les blocs avaient jusqu'à 5 diapos**, au-delà de la limite de 3 à 4 (règle 7).

## 3. La logique après

Elle suit l'ordre commun des profs : Qr → Qr,i → Qr,éq → K → mesurer K → de quoi dépend τ.

On s'en écarte seulement là où nos règles le demandent :

- les outils de zéro passent d'abord, chacun juste avant son premier usage ;
- chaque national vient juste après sa notion, et l'élève y fait l'étape décisive avant la voix.

Il y a 4 séances de 3 blocs (40 à 50 min par séance). Notation : **[Q]** = l'ardoise « À toi » du bloc ; **[OBS]** = question d'observation : la voix s'arrête, l'élève répond, puis la voix confirme.

### Séance 1 — Les outils depuis zéro ; τ, l'équilibre et la question du chapitre ; le quotient de réaction

**Bloc ee_b01 — Les outils : concentration, puissances de dix, acide et pH**

| Diapo | Pourquoi ici |
|---|---|
| `ee_z1_concentration` [Q] | La concentration sert à chaque diapo (C, [X]). Elle est enseignée de zéro (n/V, la comparaison avec le sucre), avant tout usage (règle 6). Diapo inchangée, voix gardée. |
| `ee_z2_puissance` | Les puissances de dix et le log servent à lire 10^(−pH). On l'enseigne juste après la concentration, avant le pH. Diapo inchangée. |
| `ee_z4_couple` **(nouvelle place)** | Acide, base, couple AH/A⁻ : sans eux, l'équation de Qr (`ee_q1`) n'a pas de sens. C'est la diapo `ab_r1_rappel` du ch13 : même vue (`acides-bases-tableau/eau.html?vue=rappel`), même texte, même voix (piste déjà enregistrée, aucune voix à refaire). Les cinq profs supposent le couple connu ; notre règle 6 le fait enseigner. |
| `ee_z5_ph` **(nouvelle place)** | L'eau dans deux couples (l'eau base de l'acide) et pH = −log[H₃O⁺], avec l'exemple 3,41 → 3,89·10⁻⁴ mol/L, qui est notre exemple A. C'est la diapo `ab_r1b_eau_ph` du ch13, voix gardée. Le pH est enseigné juste avant `ee_r1`, qui l'utilise. |

**Bloc ee_b02 — τ, deux concentrations, l'équilibre dynamique**

| Diapo | Pourquoi ici |
|---|---|
| `ee_r1_taux` [OBS] | τ = x_f/x_max par le tableau, puis τ = 10^(−pH)/C (rappel du ch11, enseigné pas à pas). **Observation** : la voix s'arrête sur « τ = 0,039 », l'élève dit si la réaction est totale ou limitée, puis la voix confirme « τ < 1 : limitée ». La commande « limitée » de la simulation est déplacée sur « la réaction est limitée » pour qu'elle ne s'écrive pas avant la réponse (texte dit inchangé). |
| `ee_o2_flacons` **(déplacée)** | Les mesures avant la définition : deux concentrations du même acide, deux pH, deux τ (0,039 et 0,117). L'élève voit que τ change avec C, donc qu'il ne caractérise pas la réaction. Placée ici, elle n'utilise plus rien qui n'ait été enseigné (avant : diapo 2 du cours, avant tout rappel). Voix gardée. |
| `ee_r2_equilibre` [Q] | L'équilibre dynamique (deux compteurs, concentrations constantes). Sa dernière phrase pose la question du chapitre : « existe-t-il un nombre qui relie ces trois concentrations ? ». La diapo suivante y répond. Voix gardée. |

**Bloc ee_b03 — Écrire le quotient de réaction Qr**

| Diapo | Pourquoi ici |
|---|---|
| `ee_q1_quotient` | Répond à la question de `ee_r2` (« voici la réponse… »). Qr défini sur l'acide éthanoïque, l'exemple déjà mesuré. Ordre des 5 profs : Qr d'abord. |
| `ee_q2_generale` | La forme générale (coefficients en exposants), une seule idée. **Sa question passe à `ee_q4_solides`**, avec ses réactions enregistrées : une seule ardoise par bloc, en fin de bloc, et l'espacement avec `ee_r2` est rétabli. |
| `ee_q3_eau` | L'eau solvant n'entre pas. Vient avant les solides, comme chez Naceiri (« H₂O = 1, puis solides = 1 »). |
| `ee_q4_solides` [Q] | Les solides n'entrent pas. Elle porte maintenant la question du bloc (le coefficient 2 de I⁻ dans Qr), qui ne demande que ce qui vient d'être vu. |

### Séance 2 — Qr dans un état donné : Qr,i, Qr qui évolue, Qr à l'équilibre

**Bloc ee_b04 — Qr sans unité ; Qr,i d'un mélange**

| Diapo | Pourquoi ici |
|---|---|
| `ee_q5_sans_unite` | Calculer Qr dans un état donné, sans unité (capacité EE2). Premier calcul, juste avant Qr,i. |
| `ee_i1_initial` | Qr,i = 0 quand l'acide touche l'eau (Bazhar isole Qr,i). |
| `ee_i2_melange` [Q] | Les concentrations après mélange : c'est le piège du national (7/20). La question et l'exercice restent. |
| `ee_i2b_calcul` | Le calcul de Qr,i, sur le même mélange. |

**Bloc ee_b05 — Qr évolue ; Qr,i au national**

| Diapo | Pourquoi ici |
|---|---|
| `ee_i3_au_cours` | Qr monte de Qr,i vers Qr,éq : il prépare l'équilibre. |
| `ee_n4_pile` **(déplacée, avant : fin du cours)** [OBS] | National 2017 N, Qr,i d'une pile : appliquer tout de suite « les solides n'entrent pas » et « coefficients en exposants » (règle 7 : l'exercice qui fixe). **Observation** : après l'équation, l'élève choisit les espèces qui entrent dans Qr,i (Al³⁺ et Cu²⁺) ; la voix confirme « les lames sont des solides ». |
| `ee_n3_melange` **(déplacée)** [Q] [OBS] | National 2020 R, Qr,i d'un mélange : la même méthode que `ee_i2`, avec les données du sujet. **Observation** : « on divise par quel volume ? » (V_T = 400 mL) avant que la voix le dise. Puis l'ardoise : le calcul, avec sa démonstration. |

**Bloc ee_b06 — Qr,éq à partir du pH**

| Diapo | Pourquoi ici |
|---|---|
| `ee_e1_concentrations` | Le pH mesuré donne les trois concentrations à l'équilibre (exemple A). La mesure vient avant la grandeur. |
| `ee_e2_quotient` | On les remplace dans Qr : Qr,éq = 1,57·10⁻⁵. |
| `ee_e3_expression` [Q] | Qr,éq = 10^(−2pH)/(C − 10^(−pH)), la forme demandée au national. Elle reste avant K : `ee_k1_trois` et `ee_k2_produits` calculent leurs Qr,éq avec elle (« نفس l'expression »). |
| `ee_n1_national` **(déplacée)** [OBS] | National 2017 N : la même expression, appliquée juste après (acide butanoïque). **Observation** : « que vaut [AH]_éq ? » (C − 10^(−pH)) avant la voix. La commande « relation » est déplacée sur « Q r à l'équilibre égale dix puissance moins deux p H… » pour que l'expression ne s'écrive pas avant la réponse. |

### Séance 3 — La constante d'équilibre K : la voir, l'écrire, la mesurer

**Bloc ee_b07 — Un même Qr,éq : la constante d'équilibre K**

| Diapo | Pourquoi ici |
|---|---|
| `ee_k1_trois` [OBS] | Les mesures avant la définition (demande de l'utilisateur). Trois béchers, le pH-mètre lit 3,41, 3,56 et 3,93, puis le tableau C · pH · τ · Qr,éq naît de l'animation. L'**observation** (déjà là) fait comparer les colonnes : τ change, Qr,éq reste ≈ 1,6·10⁻⁵. C'est l'activité de Naceiri. |
| `ee_k2_produits` | Deuxième façon (règle 6) : en partant des produits, le même Qr,éq. |
| `ee_k3_constante` | Seulement maintenant, le nom : K = Qr,éq, qui ne dépend que de la température. |
| `ee_k4_inverse` | K' = 1/K (capacité EE4). |

**Bloc ee_b08 — K = C·τ²/(1 − τ) et ses nationaux**

| Diapo | Pourquoi ici |
|---|---|
| `ee_k5_tau` [Q] | La relation la plus demandée, établie depuis le tableau. |
| `ee_n6_taux` **(déplacée)** [OBS] | National 2021 N : τ puis Qr,éq. **Observation** : « par quoi commences-tu ? » (calculer τ) avant la voix. La commande « taux » est déplacée plus loin dans la phrase. |
| `ee_n2_base` **(déplacée)** [OBS] | National 2022 R : la même relation pour une base (méthylamine, τ donné). C'est un transfert, sans Ke, qui reste hors du ch12. **Observation** : l'élève choisit Qr,éq = C_b·τ²/(1 − τ) parmi trois expressions. La commande « relation » est déplacée. |

**Bloc ee_b09 — Mesurer K par la conductimétrie**

| Diapo | Pourquoi ici |
|---|---|
| `ee_m2a_conductance` | Rappel de zéro : le conductimètre, G = k·σ, juste avant son usage. « Siemens » est dit « si mènsse » (règle de prononciation en place). |
| `ee_m2_conductimetrie` | σ = (λ₁ + λ₂)·[H₃O⁺]. C'est l'outil des profs (El Goufifa, Moutamadris, la fiche). |
| `ee_m3_calcul` | De σ à K, ligne par ligne, avec la conversion mol/m³ → mol/L. Pas d'observation : la simulation écrit « 0,118 mol/m³ » au moment où la voix commence le calcul ; un arrêt dessus donnerait la réponse (voir § 5). |
| `ee_m4_national` [Q] | National 2019 N (acide benzoïque) : K par la conductivité, avec la démonstration. |

### Séance 4 — De quoi dépend τ ; national et bilan

**Bloc ee_b10 — Diluer : même K, autre τ ; un autre acide, une autre K**

| Diapo | Pourquoi ici |
|---|---|
| `ee_z3_dilution` | Rappel de zéro : diluer (pipette, fiole), juste avant de diluer. |
| `ee_f1_dilution` | Même K, concentrations différentes : τ grandit. L'état initial passe d'abord, comme dans les 4 sources où l'ordre est visible. |
| `ee_m1_methanoique` **(déplacée, avant : bloc « mesurer K »)** | Un autre acide, une autre K (1,8·10⁻⁴). Elle prépare `ee_f2` (même C, K différente). Elle est à sa place comme deuxième facteur de τ, pas comme une méthode de mesure (son pH n'apporte rien de nouveau à la mesure). |

**Bloc ee_b11 — τ dépend de K et de C**

| Diapo | Pourquoi ici |
|---|---|
| `ee_f2_nature` | Même C, K différente → τ différent. |
| `ee_f3_courbe` [Q] | Deux courbes τ(C) avec une poignée : l'élève manipule C (règle 5, ≤ 2 curseurs). |
| `ee_f4_bilan` | Le tableau « quand on dilue » : un tableau de méthode, il reste un tableau (règle 35). |

**Bloc ee_b12 — K lue sur une courbe, puis le bilan**

| Diapo | Pourquoi ici |
|---|---|
| `ee_n5_courbe` [OBS] | National 2017 R : K = 4 lue sur la courbe d'une estérification (annoncée « plus tard »). C'est le seul national qui ne dépend d'aucune notion particulière du chapitre ; il récapitule donc K = Qr,éq avant le bilan. **Observation** : « lis le palier : combien d'acide reste-t-il ? » (0,2 mol) avant la voix. |
| `ee_bl_fiche` | La fiche « Ce qu'il faut retenir ». |
| `ee_cr_carte` [Q] | La carte complète. C'est maintenant la seule carte du cours : elle arrive quand tout a été vu. |

**Retirée** : `ee_o1_carte`, la carte d'ouverture. Elle annonçait Qr,éq = K avant toute mesure (règles 3 et 4), et elle doublait la carte finale.

## 4. Ce qui change, ce qui reste

**Ce qui reste.** Les ids et les textes dits de toutes les diapos gardées sont inchangés : leur voix reste. Les deux diapos reprises du ch13 gardent aussi leur piste.

**Les nouveaux textes à dire.** Il n'y a ni diapo réécrite ni diapo nouvelle à enregistrer. Les seuls textes nouveaux sont ceux des 7 nouvelles questions d'observation (8 avec celle de `ee_k1_trois`, déjà enregistrée) :

- `ee_r1_taux`, `ee_n4_pile`, `ee_n3_melange`, `ee_n1_national`, `ee_n6_taux`, `ee_n2_base`, `ee_n5_courbe` ;
- pour chacune : énoncé dit, 2 indices, 3 retours, la solution.

Cela fait 49 pistes. Leurs mots darija passent `verifier_mots` ; les seuls mots rares gardés sont des nombres dits (« trente-neuf »). « Palier » (mot rare pour la voix) a été évité dans les textes dits : « la courbe ولات ثابتة ».

**Les pointages.** Les mots de 4 commandes sont déplacés plus loin dans la même phrase, pour qu'aucune réponse ne s'écrive avant l'arrêt :

| Diapo | Commande |
|---|---|
| `ee_r1_taux` | limitee |
| `ee_n1_national` | relation |
| `ee_n6_taux` | taux |
| `ee_n2_base` | relation |

Le lecteur lance une commande 0,9 s avant son mot. Un script a vérifié, avec la durée réelle des pistes, qu'aucune commande placée après l'arrêt ne part avant lui. La seule exception est celle de `ee_k1_trois`, déjà en place : elle y est tue par `conclusions: false`.

**Les ardoises.** La question de `ee_q2_generale` passe à `ee_q4_solides`, avec ses réactions enregistrées. Ensuite, chaque bloc a au plus une ardoise, et au moins deux diapos sans rien séparent deux ardoises (vérifié par script).

**Les séances.** Elles passent de 4 séances aux blocs de 3 à 5 diapos à 4 séances de 12 blocs de 3 à 4 diapos. Le cahier de chaque bloc reprend les lignes déjà écrites pour ses diapos. Les `retrouver` et `exercice` de bloc, qui ne sont pas joués, sont repris du bloc d'origine le plus proche. Les compétences gardent leurs ids et leurs rappels ; leurs `slide_ids` suivent le nouvel ordre.

**Les réactions écrites.** J'ai fait aussi une correction hors logique : 7 réactions écrites portaient « tau » en lettres ; il est remplacé par « τ » (`verifier_formules.py` : 0).

## 5. Ce qui n'a pas pu être fait, et les besoins

- **`ee_m3_calcul`.** Une question « dans quelle unité sort [H₃O⁺] ? » aurait fixé le piège mol/m³. Mais la vue `conductimetrie.html?vue=calcul` écrit « 0,118 mol/m³ » dès le moment `concentration`. Il faudrait que cette vue accepte `conclusions: false`, comme `constante.html`, pour taire l'unité pendant la question.
- **Les voix.** Les 49 pistes sont à faire sur le VPS (voix Bodi), avec `scripts/voix/attente_construire.py` puis `attente_poser.py`. Les ids sont ceux de `attente_construire.py` (`enonce_obs_<diapo>_q|i0|i1|r0..r2|s`).
- **Les questions d'observation.** La skill professeur (règle 30) les veut rares, 0 à 2 par cours, et jamais sur un calcul. Ici elles sont 8 (7 nouvelles), à la demande de l'utilisateur du 18 novembre : l'élève doit faire chaque étape avant la correction. Aucune ne demande de calcul. Chacune porte sur une lecture (palier), un choix de méthode (par quoi commencer, quel volume, quelles espèces) ou une expression à reconnaître. Les calculs restent sur l'ardoise du bloc, avec leur démonstration.
- **Fichiers partagés.** Aucun n'a été modifié (`shared/`, lecteur `frontend/src/`).
