# Architecture — `math_ch5_fonctions_ln` (Fonction logarithme népérien, 2e Bac PC BIOF)

Refonte de la logique du 18 novembre 2026 (skill `logique-de-cours`). Cours en ligne inchangé ; nouvelle version dans `backend/data/courses/en_attente/math_ch5_fonctions_ln.json` (partie de la version en attente, plus récente). Pistes à mettre en voix : `math_ch5_fonctions_ln_voix.json` (19 pistes).

## 1. La logique avant

Ouverture, puis **cinq rappels d'affilée en séance 0** (primitive, puissances, signe de x − 1, sens d'une inégalité, second degré) → I. naissance de ln → II. courbe, e, tangente → III. domaine → IV. règles de calcul → V. équations → VI. limites → VII. dérivée de ln u → VIII. primitives u′/u → IX. étude de fonction, type national → X. log décimal → bilan.

Ce qui allait déjà :
- **ln est construite, pas donnée** (la demande de l'utilisateur) : la règle des puissances bute sur 1/x (n1) ; 1/x est continue donc la famille existe (n2) ; la courbe qui passe par (1 ; 0) reçoit son nom (n3) ; ln 1 = 0 et la pente 1/x sont lues sur les tangentes (n4) ; la croissance et le signe se voient (c1, c2, observation) ; e est lu sur la courbe (c3).
- Les règles de calcul naissent d'une observation : ln 3 posé sur ln 2 arrive à ln 6 (a1), et ln(ax) monte de ln a (a2).

Ce qui n'allait pas :
1. **Trois rappels étaient loin de leur usage** : le sens d'une inégalité (sert au domaine), le tableau de signe (sert au quotient dans ln), le second degré (sert à la première équation). Ils étaient en séance 0, une à trois séances avant leur usage.
2. **Le problème du national 2019 était dit, pas joué** : le minimum f(1) = 3/2 et f(x) − x = ½(ln x − 1)² étaient donnés par la voix, sans aucune réponse de l'élève.
3. **Le problème du national 2021** demandait l'inégalité finale dans un exercice de e5, avant que le minimum ne soit établi (e5_b), puis la voix de e5_c la donnait de toute façon.

## 2. Les sources et ce qu'elles disent
- **Profs en vidéo** (`exploration/fonctions_ln.json`) :
  - chaque ln donne une condition « > 0 » (10 profs) ;
  - ln 1 = 0 et ln e = 1 (9 profs) ;
  - produit → somme (10 profs) ;
  - le domaine avant de résoudre (8 profs) ;
  - ln est croissante, donc ln a < ln b ⇔ a < b (8 profs).
- **Cours écrits en ligne** (lus le 18/11) :
  - Benmoussa (moutamadris, PC-SVT) : définition par la primitive de 1/x qui s'annule en 1 → conséquences (dérivée, croissance, ln a = ln b, ln a < ln b, signe) → propriétés algébriques → limites → ln(u) et u′/u → étude → log.
  - Atmani (moutamadris, BIOF) : définition et propriétés, avec les équations dès la page 1 → limites → étude → ln u → primitives u′/u → log.
  - Cheddadi (AlloSchool, séance 8) : même ordre que Benmoussa.
  - Atlasmaths (fiche SE) : même ordre.
  - Les quatre définissent ln comme une primitive, jamais par une aire ni comme réciproque de exp. Le log décimal vient toujours en dernier.
  - **Ordre commun** : définition → conséquences → algèbre → limites → étude → ln u → log. Notre ordre est le même. Le domaine est placé avant l'algèbre parce que chaque règle demande a, b > 0 ; les équations viennent juste après l'algèbre, comme chez Atmani.
- **Cadre** : LN1 à LN10, tous travaillés. Rien hors cadre : pas de développement limité, de log de base a, ni de convexité au sens de Jensen.
- **National** : dérivée 13 sujets sur 20, fonction auxiliaire 11, variations 10, construction 10, limites 9, équations 5, position 5, domaine 1, log décimal 0 (mais le pH chaque année en chimie). Le temps du cours va au problème : 13 diapositives d'étude, dont deux problèmes nationaux maintenant joués pas à pas.

## 3. Les décisions et leurs raisons

| Décision | Raison |
|---|---|
| z1 (primitive) et z2 (puissances) restent juste avant la naissance de ln | Leur usage est la diapositive suivante (n1). |
| z4 (sens) juste avant d1 ; z3 (signe) juste avant d2 ; z5 (second degré) entre q1 et q1_b | Règle 6 : le rappel au moment où il sert. La séance 0, qui n'enseignait que des rappels, disparaît. |
| q1_b : une phrase changée | Sinon la voix dirait « revu au début ». |
| e3 : l'élève calcule le minimum f(1) | Règle 5. La question et ses réactions viennent des exercices de fin de cours. |
| e4 coupé en deux | e4 : l'élève écrit f(x) − x comme un carré (question). e4_b (nouvelle) : la position, le contact en e et la construction, sur les mêmes moments de l'animation. Une idée par diapositive (règle 7). |
| L'inégalité de 2021 déplacée de e5 vers e5_c | Elle est demandée après le minimum, et la voix s'arrête avant la réponse. La question garde ses réactions déjà écrites. |
| Bloc nouveau `ln_s5_b1d` | Il accueille e4 et e4_b, avec un « retrouver » et un exercice écrits pour lui (position par le signe de f(x) − x). |
| Bloc `ln_s2_b1` : un exercice nouveau sur ln\|x + 1\| | Il colle à ses diapositives (d3, d4, a1). L'ancien exercice suit d2 dans le bloc précédent. |

## 4. Ce qui ne change pas, et pourquoi
65 diapositives gardent leur texte et leur voix. La construction de ln, les règles de calcul démontrées, les équations, les limites animées et la dérivée suivent déjà l'ordre des profs et les règles 3 et 4.

v1 énonce la règle (ln u)′ = u′/u avant de la contrôler sur ln(2x). On la garde : l'élève fait aussitôt l'exemple suivant (ln(x² + 1)), et la refaire coûterait la voix d'une diapositive qui marche. C'est noté comme piste d'amélioration.

## 5. Animations
Aucun fichier de simulation n'est modifié. e4 s'arrête au moment `droite` de `etude.html?vue=position`. e4_b rejoue `droite`, puis `ecart`, `contact` et `courbe`. e5_c ne joue plus `inegalite` : ce moment écrivait la réponse avant la question.

## 6. Mots et voix
Chaque texte réécrit a été vérifié par `scripts/voix/verifier_mots.py`.
- Mots rares remplacés : « كننشروه بالمتطابقة الهامة » → « كنبسطو هاد le carré بـ l'identité remarquable » ; « كيبينوها » → « كيبينو هادشي » ; « نقطة التلاقي » → « النقطة فين كيتلاقاو » (pointage mis à jour) ; « trois demis » → « trois sur deux ».
- Gardé et à écouter : « inégalité », terme du programme (LN9).
- Pistes à faire : 5 diapositives (q1_b, e3, e4, e4_b, e5_c), 2 démonstrations, 12 réactions et énoncés.

## 7. Le plan, diapositive par diapositive
Légende : ↕ déplacée (texte et voix gardés) · ✎ réécrite (voix à refaire) · ＋ nouvelle.

### Séance 1 — Une fonction nouvelle : la naissance de ln


**Bloc `ln_s0_b1` — Une fonction nouvelle ; rappels : primitive et puissances** · fin de bloc : cahier (3 lignes), retrouver « Cahier fermé : écris la définition d'une primitive. », exercice « Une primitive de x⁵ sur ℝ est : »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `ln_o1` La carte du chapitre : une fonction qui transforme les produits | Ouverture | — | Le but avant le détail : la carte du chapitre et sa place au national (18 sujets sur 20, un problème dans 12). |
|  | `ln_z1_primitive` Rappel : une primitive, c'est la dérivée à l'envers | Ouverture | — | Rappel juste avant n1–n3 : ln est définie comme une primitive (définition commune à tous les cours écrits lus). |
|  | `ln_z2_puissances` Rappel : les puissances, 2⁰ = 1 et x⁻¹ = 1/x | Ouverture | — | Rappel juste avant n1 : 1/x = x⁻¹, c'est là que la règle des puissances bute. |

**Bloc `ln_s1_b1` — Pourquoi une fonction nouvelle** · fin de bloc : cahier (2 lignes), retrouver « Cahier fermé : pourquoi la règle xⁿ → xⁿ⁺¹/(n + 1) ne donne pas de primitive de 1/x ? », exercice « Vrai ou faux ? »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `ln_n1` La règle des puissances bute sur 1/x | I. La naissance de ln : la primitive de 1/x qui s'annule en 1 | — | Construire plutôt que donner : la règle xⁿ → xⁿ⁺¹/(n + 1) donne une division par zéro pour 1/x ; l'élève voit pourquoi il faut une fonction nouvelle. |
|  | `ln_n2` 1/x a quand même des primitives | I. La naissance de ln : la primitive de 1/x qui s'annule en 1 | ❓ x ↦ 1/x est continue sur ]0 ; +∞[ : que peut-on en déduire ? · ✏️ Vrai ou faux ? | 1/x est continue, donc elle a des primitives (chapitre précédent) : la famille F + k se voit. Question : que peut-on déduire ? |

**Bloc `ln_s1_b2` — ln 1 = 0, (ln x)′ = 1/x ; croissance et signe** · fin de bloc : cahier (4 lignes, 1 figure(s)), retrouver « Cahier fermé : écris ln 1 et la dérivée de ln. », exercice « La pente de la tangente à la courbe de ln au point d'abscisse 4 est : »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `ln_n3` La primitive qui passe par (1 ; 0) s'appelle ln | I. La naissance de ln : la primitive de 1/x qui s'annule en 1 | — | Parmi la famille, celle qui passe par (1 ; 0) reçoit son nom : la définition du cadre (LN1) naît de la figure. |
|  | `ln_n4` Deux faits tout de suite : ln 1 = 0 et (ln x)' = 1/x | I. La naissance de ln : la primitive de 1/x qui s'annule en 1 | — | ln 1 = 0 et (ln x)′ = 1/x lus sur la courbe (pentes 1 ; 0,5 ; 0,25) avant d'être encadrés. |
|  | `ln_c1` ln monte toujours | II. La courbe de ln : croissance, signe, e, tangente | — | Croissance : vue (points placés, point qui glisse), puis justifiée par 1/x > 0. |
|  | `ln_c2` Négatif avant 1, positif après 1 | II. La courbe de ln : croissance, signe, e, tangente | ❓ ln(3/4) est : · ✏️ ln 0,3 est : · 👀 observation | Signe : l'élève le trouve (observation), puis question ln(3/4). |

### Séance 2 — e, la tangente, puis le domaine


**Bloc `ln_s1_b3` — Le nombre e, comparer, la tangente** · fin de bloc : cahier (3 lignes, 1 figure(s)), retrouver « Cahier fermé : écris la valeur de ln e et une valeur approchée de e. », exercice « ln(2x) = ln 6 a pour solution : »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `ln_c3` Le nombre e : là où ln vaut 1 | II. La courbe de ln : croissance, signe, e, tangente | — | e défini sur la courbe (ln e = 1), situé entre 2 et 3 par ln 2 et ln 3 (9 profs : ln e = 1, e ≈ 2,7). |
|  | `ln_c4` ln compare comme x compare | II. La courbe de ln : croissance, signe, e, tangente | — | ln a < ln b ⇔ a < b vu par les hauteurs : prépare équations et inéquations (convergence de 8 profs). |
|  | `ln_c5` La tangente en 1 : y = x − 1 | II. La courbe de ln : croissance, signe, e, tangente | — | Tangente en 1 : y = x − 1 (3 sujets) ; la position annonce e1. |

**Bloc `ln_s0_b2` — Rappels : sens d'une inégalité, tableau de signe ; une condition, un quotient** · fin de bloc : cahier (4 lignes), retrouver « Cahier fermé : résous −2x > 4. », exercice « f(x) = ln((x − 1)/(x + 2)) : quel est D_f ? »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
| ↕ | `ln_z4_sens` Rappel : multiplier par un négatif change le sens | III. L'ensemble de définition : u(x) > 0 | ❓ −3x < 6 ⇔ ? | DÉPLACÉE (était en séance 0) : multiplier par un négatif change le sens sert dans d1 (exercice 4 − x > 0) et en q7. |
|  | `ln_d1` Une condition par ln : u(x) > 0 | III. L'ensemble de définition : u(x) > 0 | ❓ f(x) = ln(2x − 6) : quel est D_f ? · ✏️ f(x) = ln(4 − x) : quel est D_f ? | Une condition par ln (convergence de 10 profs) ; l'élève trouve D_f. |
| ↕ | `ln_z3_signe` Rappel : le signe de x − 1 | III. L'ensemble de définition : u(x) > 0 | — | DÉPLACÉE : le tableau de signe sert juste après, en d2 (quotient dans ln). |
|  | `ln_d2` Un quotient dans ln : tableau de signe | III. L'ensemble de définition : u(x) > 0 | — | Quotient dans ln : tableau de signe sur les seuls x permis (LN2). |

**Bloc `ln_s2_b1` — « et », ln|u| ; ln 6 = ln 2 + ln 3** · fin de bloc : cahier (3 lignes), retrouver « Cahier fermé : écris la condition d'existence de ln(u(x)). », exercice « f(x) = ln|x + 1| : quel est D_f ? »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `ln_d3` Plusieurs conditions : « et » | III. L'ensemble de définition : u(x) > 0 | — | Plusieurs conditions, « et ». |
|  | `ln_d4` ln|u| demande seulement u ≠ 0 | III. L'ensemble de définition : u(x) > 0 | — | ln|u| : seulement u ≠ 0 (piège). |
|  | `ln_a1` ln 6 = ln 2 + ln 3 ? | IV. Les règles de calcul | ❓ ln 2 ≈ 0,69 et ln 5 ≈ 1,61 : que vaut ln 10 environ ? · ✏️ ln 2 ≈ 0,69 et ln 3 ≈ 1,10 : que vaut ln 18 environ ? (18 = 2 × 3 × 3) · 👀 observation | La règle du produit découverte : ln 3 posé sur ln 2 arrive à ln 6 (observation), puis question ln 10. |

### Séance 3 — Les règles de calcul


**Bloc `ln_s2_b2` — Produit, inverse, quotient** · fin de bloc : cahier (2 lignes, 1 figure(s)), retrouver « Cahier fermé : écris la règle du logarithme d'un produit. », exercice « Pour x > 0, ln(5x) − ln x = ? »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `ln_a2` Multiplier x par a, c'est monter la courbe de ln a | IV. Les règles de calcul | — | Pourquoi : ln(ax) − ln x a une dérivée nulle (preuve par ce que l'élève connaît : dérivée, constante). |
|  | `ln_a3` L'inverse donne un moins | IV. Les règles de calcul | — | L'inverse tiré du produit (a × 1/a = 1). |
|  | `ln_a3_b` Le quotient donne une différence | IV. Les règles de calcul | — | Le quotient tiré de l'inverse. |

**Bloc `ln_s2_b2b` — Puissance, racine ; simplifier** · fin de bloc : cahier (2 lignes), retrouver « Cahier fermé : que valent ln(aⁿ) et ln √a ? », exercice « Simplifie C = ln 8 + ln 9 − ln 6. »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `ln_a4` La puissance descend devant | IV. Les règles de calcul | — | La puissance tirée du produit répété. |
|  | `ln_a4_b` La racine donne un demi | IV. Les règles de calcul | — | La racine tirée de √a × √a = a. |
|  | `ln_a5` Simplifier : d'abord les nombres premiers | IV. Les règles de calcul | ❓ A = ln 12 − ln 27 + ln √2 = ? · ✏️ Simplifie C = ln 8 + ln 9 − ln 6. | Simplifier (« vérifier que f(x) = … », 4 sujets) : étapes, l'élève regroupe. |

**Bloc `ln_s2_b3` — Les pièges ; trouver l'erreur** · fin de bloc : cahier (3 lignes), retrouver « Cahier fermé : écris ln(x²) pour x ≠ 0. », exercice « D = 2 ln 6 − ln 4 : quelle est la bonne valeur ? »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `ln_a6` ln ne casse pas les sommes | IV. Les règles de calcul | — | Piège n° 1 : ln(a + b). |
|  | `ln_a6_b` ln(x²) = 2 ln|x| | IV. Les règles de calcul | — | Piège n° 2 : ln(x²) = 2 ln|x|. |
|  | `ln_a7` Trouve l'erreur | IV. Les règles de calcul | — | Trouver l'erreur dans le calcul d'un élève. |

### Séance 4 — Équations, inéquations, systèmes ; ln en +∞ et en 0


**Bloc `ln_s2_b4` — ln(eʳ) = r ; la première équation ; rappel : le second degré** · fin de bloc : cahier (3 lignes), retrouver « Cahier fermé : que vaut ln(eʳ) ? », exercice « Résous ln(x + 3) = ln(2x − 1). »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `ln_a8` ln(eʳ) = r | IV. Les règles de calcul | — | ln(eʳ) = r : prépare ln x = r ⇔ x = eʳ (q2). |
|  | `ln_q1` ln a = ln b : d'abord le domaine | V. Équations, inéquations, systèmes | — | Équation (5 sujets) : d'abord le domaine (8 profs), puis un seul ln. |
| ↕ | `ln_z5_second_degre` Rappel : l'équation du second degré | V. Équations, inéquations, systèmes | — | DÉPLACÉE (était en séance 0) : le second degré sert à la diapositive suivante (q1_b), puis en q4. |
| ✎ | `ln_q1_b` Le second degré, puis trier les solutions | V. Équations, inéquations, systèmes | ❓ Résous ln(x − 1) + ln(x + 2) = ln 4. · ✏️ Résous ln(x + 3) = ln(2x − 1). | RÉÉCRITE (une phrase) : « le second degré revu au début » devient « qu'on vient de revoir ». L'élève trie les solutions. |

**Bloc `ln_s3_b1` — ln x = r, inéquation, second degré, produit nul** · fin de bloc : cahier (4 lignes), retrouver « Cahier fermé : écris les deux règles qui permettent d'enlever les ln. », exercice « Résous ln x = −1. »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `ln_q2` ln x = r ⇔ x = eʳ | V. Équations, inéquations, systèmes | — | ln x = r ⇔ x = eʳ sur un exemple, puis la règle. |
|  | `ln_q3` Inéquation : ln garde le sens | V. Équations, inéquations, systèmes | — | Inéquation : ln garde le sens ; croiser avec le domaine. |
|  | `ln_q4` Second degré en ln x : poser X = ln x | V. Équations, inéquations, systèmes | — | Second degré en ln x : poser X = ln x. |
|  | `ln_q5` Produit nul avec ln (national 2021) | V. Équations, inéquations, systèmes | ❓ Résous dans ]0 ; +∞[ : 2x ln x − 2x = 0. · ✏️ National 2017 : résous dans ]0 ; +∞[ : (1 − 2/x) ln x = 0. | Produit nul (national 2021) : l'élève trie. |

**Bloc `ln_s3_b2` — Système, plus petit entier n ; ln en +∞ et en 0** · fin de bloc : cahier (4 lignes, 2 figure(s)), retrouver « Cahier fermé : écris les limites de ln x en +∞ et en 0 à droite. », exercice « Résous : ln x + ln y = 1 et ln x − ln y = 1. »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `ln_q6` Un système : changer d'inconnues | V. Équations, inéquations, systèmes | — | Système : changer d'inconnues (LN4). |
|  | `ln_q7` Le plus petit entier n : passer au ln | V. Équations, inéquations, systèmes | — | Plus petit entier n (suites avec ln, 7 sujets) : diviser par un négatif. |
|  | `ln_l1` ln x → +∞, mais lentement | VI. Les limites de base | — | ln x → +∞ vu en reculant (10, 100, 1000) ; branche parabolique. |
|  | `ln_l2` En 0 à droite : ln x → −∞, asymptote verticale | VI. Les limites de base | ❓ La courbe de ln coupe-t-elle l'axe des ordonnées ? · ✏️ lim_{x→0⁺} (x + ln x) = ? | En 0⁺ : asymptote verticale (7 sujets). |

### Séance 5 — Les limites, la dérivée de ln u


**Bloc `ln_s3_b3` — x l'emporte ; le nombre dérivé ; factoriser** · fin de bloc : cahier (4 lignes, 1 figure(s)), retrouver « Cahier fermé : écris les deux croissances comparées de base. », exercice « lim_{x→+∞} (ln x + 1)/x = ? »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `ln_l3` (ln x)/x → 0 : x l'emporte | VI. Les limites de base | — | (ln x)/x → 0 : la course des trois courbes. |
|  | `ln_l4` x ln x → 0 en 0 à droite | VI. Les limites de base | — | x ln x → 0 : le rectangle de plus en plus fin. |
|  | `ln_l5` Deux limites qui sont un nombre dérivé | VI. Les limites de base | — | Les deux limites « nombre dérivé » : la sécante qui devient tangente. |
|  | `ln_l6` Une forme ∞ − ∞ : factoriser | VI. Les limites de base | ❓ Calcule lim_{x→+∞} (x − ln x). · ✏️ Calcule lim_{x→+∞} (ln x − 2x). | ∞ − ∞ : factoriser ; l'élève finit. |

**Bloc `ln_s4_b1` — t = √x ; continuité en 0 ; (ln u)' = u'/u ; limite de ln(u(x))** · fin de bloc : cahier (4 lignes), retrouver « Cahier fermé : écris la dérivée de ln u. », exercice « Pour calculer lim_{x→+∞} (ln x)/√x, on pose t = √x. On obtient : »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `ln_l7` Limite déguisée : poser t = √x | VI. Les limites de base | — | Limite déguisée t = √x (2023 N, 2 points). |
|  | `ln_l8` En 0 à droite : continuité et branche | VI. Les limites de base | — | Continuité et dérivabilité en 0 (2021 N) : prépare e5. |
|  | `ln_l9` Limite de ln(u(x)) : d'abord la limite de u(x) | VI. Les limites de base | — | Limite de ln(u(x)) : d'abord la limite de u(x). |
|  | `ln_v1` (ln u)' = u'/u | VII. La dérivée de ln u | ❓ Dérive f(x) = ln(x² + 1) sur ℝ. · ✏️ Sur ]2/3 ; +∞[, la dérivée de ln(3x − 2) est : | (ln u)′ = u′/u (13 sujets) ; contrôlée sur ln(2x) connu ; l'élève finit ln(x² + 1). |

**Bloc `ln_s4_b2` — (ln x)², le signe de f' ; à l'envers : u'/u** · fin de bloc : cahier (4 lignes, 1 figure(s)), retrouver « Cahier fermé : écris une primitive de u'/u. », exercice « Sur ]0 ; +∞[, (x ln x)' = ? »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `ln_v2` Dériver (ln x)² et x ln x | VII. La dérivée de ln u | — | (ln x)² et x ln x : les dérivées des problèmes. |
|  | `ln_v2_b` Au national 2019 : dériver terme par terme | VII. La dérivée de ln u | — | National 2019 : dériver terme par terme. |
|  | `ln_v3` Le signe de f' : celui de ln x, de 1 − ln x | VII. La dérivée de ln u | — | Le signe de f′ : celui de 1 − ln x. |
|  | `ln_p1` À l'envers : u'/u a pour primitive ln u | VIII. Les primitives u'/u | ❓ Une primitive de f(x) = 2x/(x² + 1) sur ℝ est : · ✏️ Une primitive de 3x²/(x³ + 1) sur ]−1 ; +∞[ est : | u′/u → ln u : la ligne qui manquait au tableau du chapitre précédent ; l'élève finit. |

### Séance 6 — Primitives u′/u, ln x ≤ x − 1, le problème de 2019 pas à pas


**Bloc `ln_s4_b3` — ln|u| ; vérifier une primitive ; ln x ≤ x − 1** · fin de bloc : cahier (3 lignes), retrouver « Cahier fermé : écris l'inégalité entre ln x et x − 1. », exercice « Une primitive de f(x) = x/(x² + 4) sur ℝ est : »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `ln_p2` Faire apparaître u' ; ln|u| si u < 0 | VIII. Les primitives u'/u | — | Faire apparaître u′ ; ln|u| (miroir de la courbe). |
|  | `ln_p3` Vérifier une primitive avec ln | VIII. Les primitives u'/u | — | Vérifier une primitive avec ln (5 sujets). |
|  | `ln_e1` Prouver ln x ≤ x − 1 par une fonction auxiliaire | IX. Étude de fonction et inégalités, type national | ❓ Pour montrer que ln x ≤ x − 1 pour tout x > 0, on étudie g(x) = x − 1 − ln x. Quelle concl · ✏️ g(x) = x − 1 − ln x. Que vaut g′(x) ? | ln x ≤ x − 1 par une fonction auxiliaire (11 sujets lisent g, 4 inégalités). |

**Bloc `ln_s5_b1` — Le problème 2019 : g donne f′, le tableau, le minimum, les bornes** · fin de bloc : cahier (2 lignes, 1 figure(s)), retrouver « Cahier fermé : écris l'équation de la tangente à la courbe de ln au point d'abscisse 1. », exercice « f′(x) = g(x)/x et g(x) > 0 sur ]0 ; +∞[. Alors f est sur ]0 ; +∞[ : »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `ln_e2` La partie I donne le signe de f′ | IX. Étude de fonction et inégalités, type national | — | La partie I donne le signe de f′ : la logique du problème du national. |
| ✎ | `ln_e3` Le tableau de variations, puis le minimum | IX. Étude de fonction et inégalités, type national | ❓ f(x) = x + ½ − ln x + ½(ln x)² : que vaut le minimum f(1) ? | RÉÉCRITE : national 2019 — le tableau et les flèches sont dits, puis l'élève calcule le minimum f(1) (question + réactions déjà écrites) ; avant, la voix le donnait. |
|  | `ln_e3_b` Les limites aux bornes, et ce qu'elles disent | IX. Étude de fonction et inégalités, type national | — | Les limites aux bornes et leur phrase (asymptote). |

**Bloc `ln_s5_b1d` — Le problème 2019 : f(x) − x, la position, le tracé** · fin de bloc : cahier (2 lignes, 1 figure(s)), retrouver « Cahier fermé : comment trouve-t-on la position de (C) par rapport à la droite (Δ) : y = x ? », exercice « f(x) − x = (ln x)² sur ]0 ; +∞[. Par rapport à (Δ) : y = x, la courbe (C) est : »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
| ✎ | `ln_e4` Position par rapport à y = x : le signe de f(x) − x | IX. Étude de fonction et inégalités, type national | ❓ f(x) = x + ½ − ln x + ½(ln x)² : f(x) − x est égal à : | RÉÉCRITE : la position commence par la question « que vaut f(x) − x ? » (l'élève l'écrit comme un carré) ; la suite passe en e4_b. |
| ＋ | `ln_e4_b` Au-dessus de y = x, puis construire la courbe | IX. Étude de fonction et inégalités, type national | — | NOUVELLE (suite de e4) : le carré ≥ 0, la courbe au-dessus, le contact en e, puis la construction ; sur les mêmes moments de l'animation (ecart, contact, courbe). |

### Séance 7 — Le problème de 2021 pas à pas, ln(u(x)), log et bilan


**Bloc `ln_s5_b1b` — Un problème du national, pas à pas** · fin de bloc : cahier (2 lignes), retrouver « Cahier fermé : pour f(x) = 2x ln x − 2x, écris f′(x). », exercice « Avec f′(x) = 2 ln x et f(1) = −2 minimum, on déduit pour x > 0 : »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `ln_e5` Un problème du national : f et sa dérivée | IX. Étude de fonction et inégalités, type national | ❓ f(x) = 2x ln x − 2x sur ]0 ; +∞[. Que vaut f′(x) ? | National 2021 pas à pas : O, puis l'élève dérive (question). L'exercice sur l'inégalité, posé ici trop tôt (avant le minimum), part en e5_c. |
|  | `ln_e5_b` Le signe de f′ et le minimum | IX. Étude de fonction et inégalités, type national | — | Correction de f′, le signe, le minimum −2, f(e) = 0. |
| ✎ | `ln_e5_c` Tracer, puis l'inégalité | IX. Étude de fonction et inégalités, type national | ❓ Avec f′(x) = 2 ln x et f(1) = −2 minimum, on déduit pour x > 0 : | RÉÉCRITE : la courbe tracée, puis l'élève tire l'inégalité ln x ≥ (x − 1)/x (question) ; avant, la voix la donnait. |

**Bloc `ln_s5_b1c` — Étude complète d'une fonction ln(u(x))** · fin de bloc : cahier (3 lignes, 2 figure(s)), retrouver « Cahier fermé : comment lit-on la concavité de (C_f) avec f″ ? », exercice « g(x) = ln((x + 1)/(3 − x)) : quel est D_g ? »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `ln_e6` Étudier ln(u(x)) : le domaine et les limites aux bornes | IX. Étude de fonction et inégalités, type national | — | Étudier ln(u(x)) : domaine et bornes (étude de fonctions du cadre, 1.2.22). |
|  | `ln_e6_b` Étudier ln(u(x)) : f′ = u′/u, puis le tableau | IX. Étude de fonction et inégalités, type national | — | f′ = u′/u puis le tableau. |
|  | `ln_e6_c` Étudier ln(u(x)) : la concavité par le signe de f″ | IX. Étude de fonction et inégalités, type national | ❓ La courbe de ln, sur ]0 ; +∞[, est : | Concavité par f″ (4 sujets demandent l'inflexion). |

**Bloc `ln_s5_b2` — log et pH ; ce qu'il faut retenir ; la carte** · fin de bloc : cahier (4 lignes), retrouver « Cahier fermé : écris log x en fonction de ln. », exercice « log 20 − log 2 = ? »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `ln_g1` Le logarithme décimal : log 10 = 1 | X. Le logarithme décimal | — | Logarithme décimal (LN10) : 0 sujet de maths, mais pH en chimie chaque année ; vient en dernier, comme chez tous les profs. |
|  | `ln_g2` 10ˣ = a ⇔ x = log a ; le pH | X. Le logarithme décimal | — | 10ˣ = a et le pH. |
|  | `ln_b1` Ce qu'il faut retenir | XI. Bilan et carte du chapitre | — | Ce qu'il faut retenir. |
|  | `ln_b2` La carte du chapitre | XI. Bilan et carte du chapitre | ❓ Par quel point passe toujours la courbe de ln ? | La carte du chapitre. |
