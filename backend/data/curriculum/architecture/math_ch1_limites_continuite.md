# Architecture — Limites et continuité (`math_ch1_limites_continuite`)

Skill `logique-de-cours`, 18 novembre 2026. Cours en ligne : `backend/data/courses/math_ch1_limites_continuite.json`
(inchangé, toujours servi avec ses voix). Nouvelle version : `backend/data/courses/en_attente/math_ch1_limites_continuite.json`,
produite par `scripts/logique/ch1_limites.py` (rejouable) et `scripts/logique/reordonner.py`.

## Le problème posé

Une professeure a jugé le cours **trop long et hors sujet**. Mesure (`docs/audit-prof/maths-longueur.md`) : 3 h 52 prévues
pour 15 h de classe au ministère, donc pas long face à la norme ; mais 77 diapositives, une **séance 0 de cinq rappels**
(18 min) avant toute notion du chapitre, des diapositives qui ne servent qu'aux devoirs, et un problème national
dit d'un trait. La dichotomie était déjà retirée le 15 novembre.

## La logique avant

Séance 0 : carte + cinq rappels de 1re bac à la suite (a² − b², signe de x − 1, signe de f′, valeur absolue, facteur
(x − a)) → I. limites (17) → II. continuité en un point (6) → III. sur un intervalle (4) → IV. image d'un intervalle (5)
→ V. TVI (9) → VI. réciproque (10) → VII. racine n-ième et puissances rationnelles (11, dont comparer et une équation
avec ∛) → VIII. limites avec ⁿ√ (4, dont a³ − b³) → IX. problème national (3 diapositives : les questions 1 à 4 dites
avec leurs réponses, une seule question à l'élève) et bilan.

Défauts : les rappels arrivent 20 à 60 minutes avant leur usage (le signe de f′ est rappelé en séance 0 et sert en
séance 4) ; le rappel « signe de x − 1 » (z2) refait exactement ce que font l9 et l10 ; quatre diapositives de
techniques de devoir (comparer deux racines, équation ∛(2x³ + 11) = 3, a³ − b³, 0/0 avec ∛) absentes du cadre et des
20 sujets ; le problème national ne laisse pas l'élève répondre étape par étape.

## Les sources et ce qu'elles disent

- **Les dix profs de l'exploration** (`exploration/limites_continuite.json`, convergences) : on remplace d'abord ; un
  outil par forme ; continuité « la limite égale l'image » ; ①/② pour deux branches ; image d'un intervalle ; TVI sous
  la forme f(a) × f(b) < 0 ; réciproque « continue et strictement monotone », J = f(I) ; racine n-ième calquée sur √.
- **Cinq cours écrits en ligne** : Benmoussa (Moutamadris / AlloSchool 100210), Cheddadi (AlloSchool 122859-122861),
  Karmim (Moutamadris), Atmani (Moutamadris, cours et résumé), Yahya Asaad (AlloSchool 108186) ; plus le livre du
  Prof Fayssal (audit `docs/audit-prof/maths.md`). **Ordre commun** : (rappel des limites) → continuité en un point, à
  droite, à gauche → sur un intervalle, opérations, composée → image d'un intervalle → TVI et unicité → réciproque →
  racine n-ième et ses limites → puissances rationnelles. Le rappel des limites ouvre le chapitre chez Karmim, Atmani,
  Belkhyr et Cheddadi ; sin x/x est dans le rappel ; puissances rationnelles chez 4 sur 5 ; dichotomie chez 2 sur 6
  seulement ; prolongement par continuité chez 1.
- **Le cadre** (`perimetre.json` : etude_fonction 1.2.1-1.2.4, fonction_reciproque 1.2.11 avec la racine n-ième ;
  `docs/audit-programme-officiel/maths.md` : racine n-ième et puissances rationnelles rattachées à 1.2.22 et gardées).
- **Le national** (`cas_types`, 2016-2025) : limites 20/20 ; réciproque 8/20 ; solution unique 6/20 ; courbe de f⁻¹
  4 sujets ; continuité à deux branches 2 sujets ; techniques ∛ et a³ − b³ : 0 sujet (devoirs seulement).

## Les grandes décisions

1. **Les rappels au moment où ils servent** (règle 6) au lieu d'une séance 0 : a² − b² et « racine → facteur »
   juste avant le facteur (x − a) ; |x| juste avant la racine à l'infini ; le signe de f′ juste avant l'image d'un
   intervalle. L'ordre des profs est gardé : le rappel des limites reste en tête (4 cours écrits sur 5).
2. **Cinq diapositives retirées**, chacune avec sa raison : z2 (doublon de l9-l10), n5 et n7 (exercices de devoir),
   lr2 et lr3 (a³ − b³ : hors périmètre, 0 sujet). Pas de partie « pour les devoirs ».
3. **Puissances rationnelles gardées** (3 diapositives, x > 0) : 4 cours écrits sur 5 les font, l'audit du programme
   officiel les rattache à 1.2.22 et le chapitre des primitives (xʳ) en a besoin. Les limites avec ⁿ√ gardent lr1
   (continuité et limite de ⁿ√u, même règle que √u) et lr4 (le terme le plus lourd).
4. **Le problème national joué question par question** : quatre diapositives, chacune une question posée avant sa
   correction (limites → signe de f′ et tableau → TVI et place de α sur la courbe animée → J = f(ℝ)). Exception
   écrite à « un seul À toi par bloc » : la règle du 18 novembre (« la réponse de l'élève avant la correction ») et la
   règle 41 (national joué pas à pas) priment pour ce bloc seulement.
5. **Une notion par diapositive, l'exemple chiffré avant la règle** : déjà vrai dans ce cours (l1 → l2, l3 → l4,
   c1 → c2, j1 → j2, t1-t3 → t4) ; gardé tel quel, voix comprises.

## L'architecture, diapositive par diapositive

73 diapositives, 7 séances, 24 blocs, durée prévue 219 min. « ✏️ » : la diapositive porte le « À toi » du bloc ; « 🔊 » : sa voix est gardée ; « 🆕 voix » : à enregistrer.

### Séance 1 — Calculer une limite : remplacer, nommer la forme, choisir l'outil

**La carte ; où mène le chemin ; je remplace d'abord** (`lc_s1_b1`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `lc_o1_carte` | La carte du chapitre : six questions sur une courbe | 🔊 | Ouvre le chapitre sur une seule courbe et six questions : l'élève sait où il va et ce qui tombe au national (limites 20/20, réciproque 8/20, solution unique 6/20). |
| `lc_l1_chemin` | Où mène le chemin ? | ✏️ 🔊 | La limite d'abord vue sur une courbe à trou (exploration, marche 1) : l'idée avant le calcul ; l'élève dit lui-même où mène le chemin. |
| `lc_l2_remplacer` | Je remplace d'abord | 🔊 | Le premier geste de tous les profs (convergence 1 : « on remplace d'abord »), juste après l'avoir vu sur la courbe. |

**0/0 n'est pas une réponse ; les quatre formes** (`lc_s1_b2`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `lc_l3_zero_sur_zero` | 0/0 n'est pas une réponse | 🔊 | Trois 0/0, trois limites différentes : prouve par l'exemple, avant de le dire, que 0/0 n'est pas un résultat. |
| `lc_l4_formes` | Les quatre formes indéterminées | 🔊 | La règle (quatre formes) vient après l'exemple chiffré de l3, pas avant. |
| `lc_l4_formes_b` | Ce qui n'est pas indéterminé | ✏️ 🔊 | Plainte des élèves (+∞ × (−∞) pris pour indéterminé, 6 fois) : ce qui n'est pas indéterminé, tout de suite après. |

**Limites usuelles ; a² − b² ; une racine donne le facteur** (`lc_s1_b3`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `lc_l4c_usuelles` | Les limites usuelles : xⁿ, 1/xⁿ, √x | 🔊 | Les limites usuelles du rappel 1 de Fayssal et des cours écrits (Cheddadi, Atmani) : outils des calculs qui suivent. |
| `lc_z1_factoriser` | Rappel : a² − b², une identité qui se voit | 🔊 | DÉPLACÉ (était en séance 0) : a² − b² est rappelé juste avant le facteur (x − a) et le conjugué qui s'en servent (règle 6). |
| `lc_z5_racine_facteur` | Rappel : une racine a donne le facteur (x − a) | ✏️ 🆕 voix | DÉPLACÉ : « une racine a donne le facteur (x − a) » juste avant l5 qui l'utilise ; ses premiers mots changent (« Une autre base » au lieu de « Dernière base »). |

**Le facteur (x − a), le conjugué, le plus haut degré** (`lc_s1_b4`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `lc_l5_facteur` | Polynômes : le facteur (x − a) | 🔊 | 0/0 avec polynômes : outil 1 de la convergence 2, montré sur x² − 9 sur x² − 4x + 3 (exemple chiffré) avant la règle. |
| `lc_l6_conjugue` | Racine carrée : l'expression conjuguée | 🔊 | 0/0 avec racine : outil 2, l'expression conjuguée, qui réutilise a² − b² vu deux diapositives plus tôt. |
| `lc_l7_plus_lourd` | À l'infini : le terme le plus lourd | ✏️ 🔊 | À l'infini, le terme de plus haut degré : 20 sujets sur 20 (« on pourra écrire f(x) = x[…] »). |

### Séance 2 — À l'infini, à droite, à gauche ; continuité en un point

**√(x²) = |x| ; racine à l'infini** (`lc_s2_b1`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `lc_z4_valeur_absolue` | Rappel : la valeur absolue et √(x²) | 🔊 | DÉPLACÉ : √(x²) = |x| rappelé juste avant la racine à l'infini (l8) qui en a besoin. |
| `lc_l8_racine_infini` | Racine à l'infini : même poids, le conjugué | 🔊 | Racine à l'infini, même poids : l'écart se lit sur deux courbes avant le calcul conjugué. |
| `lc_l8_racine_infini_b` | Racine à l'infini : poids différents, le facteur x | 🔊 | Poids différents : le facteur x et |x| ; deuxième cas du même outil, une idée par diapositive. |

**Par la droite, par la gauche ; interpréter** (`lc_s2_b2`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `lc_l9_deux_cotes` | Par la droite, par la gauche | 🔊 | Par la droite, par la gauche, vu sur 1/(x − 1) : l'élève observe lui-même la branche de gauche (question d'observation). Remplace aussi l'ancien rappel z2 (même signe de x − 1, mêmes nombres). |
| `lc_l10_signe` | Un nombre sur 0⁺, un nombre sur 0⁻ | ✏️ 🔊 | Le tableau de signe et 0⁺ / 0⁻ écrits proprement, après l'avoir vu ; erreur d'examen fréquente (k/0 sans signe). |
| `lc_l11_interpreter` | Interpréter géométriquement : nommer la droite | 🔊 | Interpréter = nommer la droite (asymptote verticale ou horizontale) : demandé avec chaque limite au national. |

**sin(x)/x ; à toi : des limites** (`lc_s2_b3`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `lc_l12_sinus` | La limite de référence sin(x)/x | 🔊 | sin(x)/x : limite de référence du rappel (Fayssal p. 7, Atmani, Cheddadi) ; vue sur deux courbes avant la règle. |
| `lc_l12_sinus_b` | sin(3x)/(2x) : on pose t = 3x | 🔊 | Son usage (sin(3x)/(2x), on pose t = 3x), juste après la règle. |
| `lc_l13_devoir` | À toi : calculer des limites | ✏️ 🔊 | L'élève fait lui-même une limite (+∞ − ∞) : la voix donne les gestes un à un et s'arrête avant le résultat ; correction après sa réponse. |

**Continue en a : la limite égale l'image** (`lc_s2_b4`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `lc_c1_soudee` | Soudée ou coupée ? | 🔊 | Continuité vue avant d'être définie : soudée ou coupée, trois dessins (ordre commun : continuité en un point en premier). |
| `lc_c2_limite_image` | La limite égale l'image | 🔊 | La définition « la limite égale l'image » (6 profs sur 6), sur un exemple chiffré (2 ≠ 3). |
| `lc_c3_deux_branches` | Deux expressions : chaque côté sa branche | ✏️ 🔊 | Fonction à deux expressions (2021 N, 2023 R) : chaque côté sa branche, question à l'élève. |

### Séance 3 — Continuité et image d'un intervalle

**Souder la courbe, à droite et à gauche, rédiger** (`lc_s3_b0`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `lc_c4_parametre` | Quelle valeur de m soude la courbe ? | 🔊 | Trouver m pour souder : même fonction, l'élève voit le saut puis la condition. |
| `lc_c4b_droite_gauche` | Continue à droite, continue à gauche | 🔊 | Continue à droite / à gauche nommés (manque relevé par l'audit Fayssal), sur la même fonction. |
| `lc_c5_redaction` | La rédaction : f(a), ①, ②, conclusion | 🔊 | La rédaction ① ② qui prend les points, après avoir compris ; dernier geste de la partie. |

**Les fonctions usuelles, les opérations, √u** (`lc_s3_b1`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `lc_i1_usuelles` | Les fonctions usuelles se tracent d'un trait | ✏️ 🔊 | Continuité sur un intervalle par les fonctions usuelles (ordre commun) ; 1re ligne de chaque question TVI ou réciproque au national. |
| `lc_i2_operations` | Somme, produit, quotient | 🔊 | Somme, produit, quotient : la phrase « car … » exigée par le barème. |
| `lc_i3_racine_u` | √u : continue ET positive | 🔊 | √u : « continue ET positive » ; l'erreur d'examen (positivité non prouvée) traitée ici. |

**Limite d'une composée ; le signe de f′ ; les hauteurs atteintes** (`lc_s3_b2`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `lc_i4_composee` | Deux machines à la suite | ✏️ 🔊 | Limite d'une composée (machines) : utilisée dans les limites avec √ et ⁿ√ plus loin. |
| `lc_z3_derivee` | Rappel : le signe de f′ donne le sens de variation | 🔊 | DÉPLACÉ : le signe de f′ donne le sens de variation, rappelé juste avant l'image d'un intervalle et le TVI qui demandent « strictement monotone ». |
| `lc_j1_hauteurs` | Les hauteurs atteintes | 🔊 | Image d'un intervalle vue comme des hauteurs atteintes, avant toute règle. |

**Image d'un intervalle : même ordre, ordre inversé, borne ouverte** (`lc_s3_b3`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `lc_j2_croissante` | Croissante : même ordre | 🔊 | Croissante : même ordre (5 profs sur 5). |
| `lc_j3_decroissante` | Décroissante : l'ordre s'inverse | ✏️ 🔊 | Décroissante : l'ordre s'inverse ; question à l'élève sur g(x) = 4/x. |
| `lc_j4_borne_ouverte` | Borne ouverte : une limite | 🔊 | Borne ouverte → limite : la règle des sujets (8/20, dans la question réciproque). |
| `lc_j5_non_monotone` | Ni croissante ni décroissante | 🔊 | Non monotone : [m ; M] lus dans le tableau (cas général du cadre 1.2.2). |

### Séance 4 — Le théorème des valeurs intermédiaires

**Couper l'axe ; continue ; une image dessous, une dessus** (`lc_s4_b1`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `lc_t1_couper_axe` | Couper l'axe sans résoudre | 🔊 | Résoudre sans résoudre : le besoin avant le théorème. |
| `lc_t2_continue` | Sans continuité, la courbe saute | ✏️ 🔊 | Plainte des élèves (« pourquoi f(a) × f(b) < 0 ? », 17 mentions) : d'abord la courbe qui saute. |
| `lc_t3_produit` | Une image dessous, une dessus | 🔊 | Puis une image dessous, une dessus ; le produit seulement à la fin. |

**Au moins une solution, puis unique ; rédiger** (`lc_s4_b2`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `lc_t4_au_moins_une` | Au moins une solution | 🔊 | Au moins une solution : la vague montre trois traversées. |
| `lc_t5_unique` | Unique : la courbe ne revient pas | ✏️ 🔊 | Unique avec strictement monotone (6/20 au national). |
| `lc_t6_rediger` | Rédiger comme au national | 🔊 | La rédaction en quatre lignes du national, sur x³ + x − 1 déjà vu. |

**Toute valeur k ; intervalle ouvert ; f(α) = 0** (`lc_s4_b3`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `lc_t7_valeur_k` | Toute valeur entre f(a) et f(b) | 🔊 | f(x) = k (2020 R, 2025 R) : la droite y = k. |
| `lc_t8_intervalle_ouvert` | Sur ℝ ou sur ]0 ; +∞[ : 0 ∈ f(I) | 🔊 | Sur ℝ ou un intervalle ouvert : 0 ∈ f(I) (2021 R, 2025 N, 2025 R). |
| `lc_t9_f_alpha` | Se servir de f(α) = 0 | ✏️ 🔊 | Se servir de f(α) = 0 : question qui suit le TVI dans 3 sujets. |

### Séance 5 — La fonction réciproque

**Aller et retour ; strictement monotone ; J = f(I)** (`lc_s5_b1`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `lc_r1_aller_retour` | Le chemin aller, le chemin retour | 🔊 | La réciproque vue comme le chemin retour (ordre commun : réciproque après le TVI). |
| `lc_r2_strictement_monotone` | Un seul antécédent : strictement monotone | 🔊 | Pourquoi strictement monotone : l'élève voit lui-même les deux antécédents (observation). |
| `lc_r3_J` | f⁻¹ est définie sur J = f(I) | 🔊 | J = f(I) : réutilise l'image d'un intervalle (partie IV). |

**Deux lignes au national ; même sens ; le miroir** (`lc_s5_b2`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `lc_r4_deux_lignes` | Deux lignes, comme au national | ✏️ 🔊 | La question du national (8/20) en deux lignes ; l'élève répond. |
| `lc_r5_sens` | Même sens de variation | 🔊 | Même sens de variation, sans dériver. |
| `lc_r6_miroir` | Le miroir y = x | 🔊 | La courbe : symétrie par rapport à y = x, point par point. |

**Construire la courbe ; l'expression de f⁻¹** (`lc_s5_b3`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `lc_r7_construire` | Construire la courbe de f⁻¹ au national | ✏️ 🔊 | Construire la courbe de f⁻¹ au national (2020 N, 2021 N, 2021 R, 2025 N). |
| `lc_r8_expression` | L'expression : la ligne pivot | 🔊 | L'expression de f⁻¹ : réclamée 45 fois (la vidéo s'arrête avant) ; la ligne pivot sur un exemple simple. |
| `lc_r9_valeur_absolue` | L'expression : la forme canonique d'abord | 🔊 | Deuxième exemple, forme canonique : celui des devoirs et des profs. |
| `lc_r9_valeur_absolue_b` | Racine et valeur absolue | 🔊 | Fin du même calcul (racine d'un carré = valeur absolue) : une idée par diapositive. |

### Séance 6 — Racine n-ième, puissances rationnelles

**Défaire la puissance n ; ⁿ√ réciproque de xⁿ ; les règles** (`lc_s6_b1`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `lc_n1_defaire` | Défaire la puissance n | ✏️ 🔊 | La racine n-ième comme ce qui défait la puissance n (fonction_reciproque du périmètre). |
| `lc_n2_reciproque_xn` | ⁿ√ : la réciproque de xⁿ sur [0 ; +∞[ | 🔊 | ⁿ√ est la réciproque de xⁿ sur [0 ; +∞[ : le théorème de la partie VI appliqué. |
| `lc_n3_regles` | Les règles de la racine carrée, en grand | 🔊 | Les règles, calquées sur celles de √ (convergence 10). |

**Simplifier ; résoudre xⁿ = a** (`lc_s6_b2`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `lc_n4_simplifier` | Simplifier en quatre étapes | ✏️ 🔊 | Simplifier en puissances de 3 : chaque puissance décomposée (plainte : erreurs de calcul des profs). |
| `lc_n6_equation` | L'équation xⁿ = a : n pair | 🔊 | xⁿ = a, n pair : lu sur la courbe. |
| `lc_n6_equation_b` | L'équation xⁿ = a : n impair | 🔊 | n impair ; le tableau des quatre cas. |

**Puissances rationnelles et leurs règles** (`lc_s6_b3`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `lc_p1_exposant` | x^(1/n) : une autre écriture de ⁿ√x | 🔊 | Puissance rationnelle : dans 4 cours écrits sur 5 (Benmoussa, Cheddadi, Karmim, Atmani) et nécessaire aux primitives de xʳ (ch4) ; toujours x > 0. |
| `lc_p2_pq` | x^(p/q), pour x strictement positif | 🔊 | x^(p/q) = ᑫ√(xᵖ), pour x > 0, sur 8^(2/3). |
| `lc_p3_regles_puissances` | Les règles des puissances restent vraies | ✏️ 🔊 | Les règles des puissances restent vraies ; l'élève calcule. |

**Continuité et limites avec ⁿ√u** (`lc_s6_b4`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `lc_lr1_continuite` | ⁿ√u : continuité et limite directe | 🔊 | ⁿ√u continue si u est continue et positive, et sa limite (Benmoussa X, Cheddadi séance 3) : même règle que √u. |
| `lc_lr4_infini` | ∞ − ∞ avec racines : le plus lourd | ✏️ 🔊 | ∞ − ∞ avec racines, par le terme le plus lourd : applique p1-p3 et l7 ; dernière limite du chapitre. |

### Séance 7 — Un problème national, question par question ; le bilan

**Le problème national : quatre questions, ta réponse avant la correction** (`lc_s7_b1`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `lc_e1_probleme` | Un problème national : ce chapitre dedans | ✏️ 🔊 | Problème type national sur x³ + x − 1 : l'énoncé, puis la question 1 (limites) posée avant sa correction. Son ancien exercice (encadrement de α) passe à la question 3, à sa place. |
| `lc_e1_probleme_b` | Question 2 : le sens de variation | ✏️ 🆕 voix | RÉÉCRIT : la question 2 seule (f′ et son signe) ; la voix s'arrête avant la réponse ; le tableau f : −∞ ↗ +∞ dans la correction. Avant, les questions 1, 2 et 3 étaient dites d'un trait avec leurs réponses. |
| `lc_e1_probleme_tvi` | Question 3 : la solution unique α, et sa place | ✏️ 🆕 voix | NOUVELLE : la question 3 (solution unique et encadrement) jouée sur la courbe qui traverse l'axe une fois ; l'élève place α (question reprise de l'ancien exercice, ses réactions et sa démonstration gardent leur voix). |
| `lc_e1_probleme_c` | Question 4 : la fonction réciproque | ✏️ 🆕 voix | RÉÉCRIT : la question 4 (J = f(ℝ)) posée à l'élève ; avant, la voix donnait la réponse. Question reprise de la réserve, réactions gardées. |

**Ce qu'il faut retenir, la carte** (`lc_s7_b4`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `lc_e2_bilan` | Ce qu'il faut retenir | 🔊 | La fiche du chapitre (règle 9 de cours-concentration) ; la ligne 8 n'a plus a³ − b³. |
| `lc_e3_carte` | La carte et tes points à revoir | 🔊 | La carte du chapitre, branches à reprendre entourées. |

## Retirées, et pourquoi

| Diapositive | Raison |
|---|---|
| `lc_z2_signe` | Doublon de `lc_l9_deux_cotes` et `lc_l10_signe` : même signe de x − 1 près de 1, mêmes nombres (1,1 ; 1,01). |
| `lc_n5_comparer` | Comparer deux racines d'indices différents : exercice de devoir, absent du périmètre et des 20 sujets. |
| `lc_n7_equation_racine` | Équation ∛(2x³ + 11) = 3 : exercice de devoir ; la notion (xⁿ = a) est en n6. |
| `lc_lr2_cle_de_trois` | a³ − b³ : formule hors périmètre, 0 sujet national. |
| `lc_lr3_zero_sur_zero` | 0/0 avec ∛ par a³ − b³ : même raison. |

Les fins de bloc qui renvoyaient à ces diapositives sont refaites : `lc_s1_b3` (exercice : factoriser x² − 5x + 6
avec P(2) = 0, au lieu du signe de x − 3 pas encore vu) ; `lc_s6_b4` (retrouver : condition de continuité de ⁿ√u ;
exercice : lim ∛(x + 8) en +∞). Le rappel de compétence « factorise a³ − b³ » (K10) est retiré ; la fiche
`bilan.html` n'a plus a³ − b³ ni « même indice pour comparer ».

## Animations et exercices animés

- Question 3 du problème : `traversee.html?vue=alpha` (la courbe de x³ + x − 1 se trace, monte, coupe l'axe une fois
  en α), arrêtée sur α avant la question.
- Questions 2 et 4 : deux vues nouvelles de `calculs.html` (`e1_q2`, `e1_q4`, ajoutées à la main dans
  `calculs-donnees.js` : le build du cours n'est pas dans le dépôt ; à reporter dans ses sources).
- Toutes les autres animations sont gardées (elles servent chacune une étape : courbe à trou, deux côtés, raccord,
  projections, traversée, miroir, racine).

## Ce qui reste à faire

- Voix : `math_ch1_limites_continuite_voix.json` (8 pistes : 4 diapositives, 2 démonstrations, 2 énoncés).
- Réactions préparées à écrire pour `lc_e1_probleme_b` (question nouvelle) ; `lc_l4_formes_b/e0` n'en avait déjà pas.
- Les écarts du contrôle `verifier_pointage_simulations.py` sont ceux d'avant (moments des vues de calcul lus dans
  `calculs-donnees.js`, que le contrôle ne lit pas) ; aucun écart nouveau hormis les temps estimés des pistes sans voix.
