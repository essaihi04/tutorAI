# Architecture — `math_ch5_fonctions_ln` (Fonction logarithme népérien, 2e Bac PC BIOF)

Refonte de la logique du 18 novembre 2026 (skill `logique-de-cours`). Cours en ligne inchangé ; nouvelle version dans `backend/data/courses/en_attente/math_ch5_fonctions_ln.json` (partie de la version en attente, plus récente). Pistes à mettre en voix : `math_ch5_fonctions_ln_voix.json` (51 pistes, dont 32 ajoutées et 4 mises à jour par la 2ᵉ passe). Légende supplémentaire du plan : ✎² réécrite et ＋² nouvelle à la 2ᵉ passe (§ 8).

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
| ✎² | `ln_n2` 1/x a quand même des primitives | I. La naissance de ln : la primitive de 1/x qui s'annule en 1 | ❓ x ↦ 1/x est continue sur ]0 ; +∞[ : que peut-on en déduire ? | 2ᵉ PASSE : la voix et la vue s'arrêtent sur la courbe continue (`inverse`) ; « continue ⇒ des primitives » (moment `existe`) et la famille ne sont plus montrés avant la réponse ; `variante` retirée (elle rejouait `existe` pendant la question). |

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
| ＋² | `ln_q3_b` À toi : une inéquation avec deux ln | V. Équations, inéquations, systèmes | ❓ Résous ln(x − 2) ≤ ln(4 − x). | 2ᵉ PASSE (cas type inéquation) : conditions → règle ln a ≤ ln b ⇔ a ≤ b, vue `calculs.html?vue=q3b` arrêtée sur `regle` ; l'élève résout et croise avec le domaine. |
|  | `ln_q4` Second degré en ln x : poser X = ln x | V. Équations, inéquations, systèmes | — | Second degré en ln x : poser X = ln x. |
|  | `ln_q5` Produit nul avec ln (national 2021) | V. Équations, inéquations, systèmes | ❓ Résous dans ]0 ; +∞[ : 2x ln x − 2x = 0. · ✏️ National 2017 : résous dans ]0 ; +∞[ : (1 − 2/x) ln x = 0. | Produit nul (national 2021) : l'élève trie. |

**Bloc `ln_s3_b2` — Système, plus petit entier n ; ln en +∞ et en 0** · fin de bloc : cahier (4 lignes, 2 figure(s)), retrouver « Cahier fermé : écris les limites de ln x en +∞ et en 0 à droite. », exercice « Résous : ln x + ln y = 1 et ln x − ln y = 1. »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `ln_q6` Un système : changer d'inconnues | V. Équations, inéquations, systèmes | — | Système : changer d'inconnues (LN4). |
|  | `ln_q7` Le plus petit entier n : passer au ln | V. Équations, inéquations, systèmes | — | Plus petit entier n (suites avec ln, 7 sujets) : diviser par un négatif. |
| ＋² | `ln_q7_b` À toi : le plus petit entier n | V. Équations, inéquations, systèmes | ❓ Plus petit entier n tel que (1/3)ⁿ < 10⁻² | 2ᵉ PASSE (cas type plus petit n) : passer au ln, la puissance descend ; vue `calculs.html?vue=q7b` arrêtée sur `descendre`, avant la division par un négatif. |
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
| ✎² | `ln_v2_b` Au national 2019 : dériver terme par terme | VII. La dérivée de ln u | ❓ f′(x) = ? (2019 N) | 2ᵉ PASSE (cas type dérivée, 13 sujets) : la voix ne donne plus f′ ; vue arrêtée sur `enonce` ; l'élève dérive, la correction écrit les lignes du barème. |
|  | `ln_v3` Le signe de f' : celui de ln x, de 1 − ln x | VII. La dérivée de ln u | — | Le signe de f′ : celui de 1 − ln x. |
|  | `ln_p1` À l'envers : u'/u a pour primitive ln u | VIII. Les primitives u'/u | ❓ Une primitive de f(x) = 2x/(x² + 1) sur ℝ est : · ✏️ Une primitive de 3x²/(x³ + 1) sur ]−1 ; +∞[ est : | u′/u → ln u : la ligne qui manquait au tableau du chapitre précédent ; l'élève finit. |

### Séance 6 — Primitives u′/u, ln x ≤ x − 1, le problème de 2019 : tableau et limites


**Bloc `ln_s4_b3` — ln|u| ; vérifier une primitive ; ln x ≤ x − 1** · fin de bloc : cahier (3 lignes), retrouver « Cahier fermé : écris l'inégalité entre ln x et x − 1. », exercice « Une primitive de f(x) = x/(x² + 4) sur ℝ est : »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `ln_p2` Faire apparaître u' ; ln|u| si u < 0 | VIII. Les primitives u'/u | — | Faire apparaître u′ ; ln|u| (miroir de la courbe). |
|  | `ln_p3` Vérifier une primitive avec ln | VIII. Les primitives u'/u | — | Vérifier une primitive avec ln (5 sujets). |
| ✎² | `ln_e1` Prouver ln x ≤ x − 1 par une fonction auxiliaire | IX. Étude de fonction et inégalités, type national | ❓ Quelle conclusion est juste ? | 2ᵉ PASSE (cas type fonction auxiliaire) : la voix s'arrête après les variations de g ; la vue s'arrête sur `tableau` (le moment `minimum` écrivait « g(1) = 0 minimum ⇒ g(x) ≥ 0 ⇒ ln x ≤ x − 1 ») ; l'encadré central qui donnait l'inégalité est retiré. |

**Bloc `ln_s5_b1` — Le problème 2019 : g donne f′, le tableau, le minimum, les limites aux bornes** · cahier (3 lignes, 1 figure), retrouver et exercice inchangés

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `ln_e2` La partie I donne le signe de f′ | IX. Étude de fonction et inégalités, type national | — | La partie I donne le signe de f′ : la logique du problème du national. |
| ✎² | `ln_e3` Le tableau de variations, puis le minimum | IX. Étude de fonction et inégalités, type national | ❓ f(1) = ? | 2ᵉ PASSE : nouvelle vue `signe.html?vue=variations_pas` : les flèches (`fleches`) puis, après la réponse, la valeur (`minimum`) ; l'ancienne vue écrivait « f(1) = 3/2 » au moment `fleches`, juste avant la question. |
| ✎² | `ln_e3_b` La limite en 0 à droite et son interprétation (2019, 1.a) | IX. Étude de fonction et inégalités, type national | ❓ lim_{x→0⁺} f(x) et interprétation | 2ᵉ PASSE (cas type limite en 0⁺, 7 sujets) : la vue s'arrête au minimum ; l'élève trouve +∞ et la phrase « x = 0 asymptote verticale ». |
| ＋² | `ln_e3_c` La limite en +∞ : l'écriture donnée (2019, 1.b) | IX. Étude de fonction et inégalités, type national | ❓ lim_{x→+∞} f(x) | 2ᵉ PASSE (cas type limite en +∞, 9 sujets) : forme indéterminée, puis l'écriture du sujet (½ ln x − 1) ln x ; vue arrêtée sur `asymptote`, borne +∞ vide. |

### Séance 7 — Le problème de 2019 : inflexion, position, construction pas à pas (NOUVELLE séance, 2ᵉ passe)

Pourquoi : la séance 6 aurait compté 12 diapositives ; le problème de 2019 joué question par question se partage en deux séances de 40 à 50 min (règle 7).

**Bloc `ln_s5_b1e` — Le problème 2019 : le point d'inflexion, puis la position (NOUVEAU)** · cahier (3 lignes, 1 figure), retrouver et exercice repris de l'ancien `ln_s5_b1d` (position)

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
| ＋² | `ln_e3_d` Le point d'inflexion (2019, 3.b) | IX. Étude de fonction et inégalités, type national | ❓ Coordonnées de I | 2ᵉ PASSE (cas type inflexion, 4 sujets) : f″ donnée → signe de 2 − ln x → s'annule en e² en changeant de signe, ligne par ligne (`calculs.html?vue=e3d`), arrêt sur `change` ; l'élève calcule f(e²) = e² + ½. |
| ✎ | `ln_e4` Position par rapport à y = x : le signe de f(x) − x | IX. Étude de fonction et inégalités, type national | ❓ f(x) − x = ? | Inchangée (coquille « la signe » → « le signe », voix pas encore faite). |
| ✎² | `ln_e4_b` La position par rapport à y = x (2019, 4.a) | IX. Étude de fonction et inégalités, type national | ❓ Position de (C) par rapport à (Δ) | 2ᵉ PASSE (cas type position) : la voix ne donne plus « au-dessus, contact en e » ; vue arrêtée sur `droite` (le moment `ecart` écrivait « ≥ 0 : (C) au-dessus de (Δ) »). La construction part en e4_c/e4_d. |

**Bloc `ln_s5_b1d` — Le problème 2019 : construire la courbe pas à pas** · cahier (2 lignes), retrouver « Cahier fermé : que place-t-on dans le repère avant de tracer la courbe ? », exercice « f′(2) = 0 et f(2) = 3 : la tangente au point d'abscisse 2 ? » (nouveaux)

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
| ＋² | `ln_e4_c` Construire (C) pas à pas : ce qu'on place d'abord (2019, 4.b) | IX. Étude de fonction et inégalités, type national | ❓ La tangente en A(e ; e) | 2ᵉ PASSE (cas types construction, 10 sujets, et tangente) : nouvelle vue `construire.html?vue=c19` ; ① asymptote ② (Δ) ③ minimum et sa tangente horizontale ④ A(e ; e), un `play_until` chacun ; arrêt sur `contact` ; l'élève trouve f′(e) = 1, donc la tangente est (Δ). |
| ＋² | `ln_e4_d` Construire (C) : l'inflexion, la branche, puis la courbe | IX. Étude de fonction et inégalités, type national | — | 2ᵉ PASSE : ⑤ (Δ) tangente ⑥ I ⑦ branche parabolique, puis la courbe tracée EN DERNIER, en suivant tout ce qui est placé (règle 41 : jamais une courbe finie d'emblée). |


### Séance 8 — Le problème de 2021 pas à pas, ln(u(x)), log et bilan


**Bloc `ln_s5_b1b` — Le problème 2021 pas à pas : f′, les variations, f(x) = x, la courbe, l'inégalité** · cahier (2 lignes), retrouver « Cahier fermé : pour f(x) = 2x ln x − 2x, écris f′(x). », exercice « Avec f′(x) = 2 ln x et f(1) = −2 minimum, on déduit pour x > 0 : »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `ln_e5` Un problème du national : f et sa dérivée | IX. Étude de fonction et inégalités, type national | ❓ f(x) = 2x ln x − 2x sur ]0 ; +∞[. Que vaut f′(x) ? | National 2021 pas à pas : O, puis l'élève dérive (question). L'exercice sur l'inégalité, posé ici trop tôt (avant le minimum), part en e5_c. |
| ✎² | `ln_e5_b` Le signe de f′ et les variations (2021, 3.c) | IX. Étude de fonction et inégalités, type national | ❓ Les variations de f | 2ᵉ PASSE (cas type variations, 10 sujets) : correction de f′ = 2 ln x, puis l'élève tire les variations et le minimum ; vue `etude.html?vue=national&etape=2` arrêtée sur `origine` (le minimum était écrit avant). |
| ＋² | `ln_e5_q` f(x) = 0 et f(x) = x : des équations avec ln (2021, 4.a) | IX. Étude de fonction et inégalités, type national | ❓ Résous f(x) = x | 2ᵉ PASSE (cas type équation) : rappel f(x) = 0 ⇔ x = e (q5), puis f(x) = x ramenée à x(2 ln x − 3) = 0 (`calculs.html?vue=e5q`, arrêt sur `factoriser`) ; l'élève écarte x = 0 et trouve e^(3/2). |
| ✎² | `ln_e5_c` Construire (C) pas à pas, puis l'inégalité (2021, 4.b et 6) | IX. Étude de fonction et inégalités, type national | ❓ L'inégalité déduite du minimum | 2ᵉ PASSE : nouvelle vue `construire.html?vue=c21` : O, minimum, (e ; 0), y = x et e^(3/2), branche (Oy), puis la courbe ; l'inégalité n'est pas écrite par la vue. |

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

## 8. Deuxième passe (18 novembre 2026) : les exercices du national joués pas à pas

Demande : « simple, animé, expliqué, ne pas tout donner au départ, laisser à l'élève le temps de trouver seul ». Chaque cas type du national (exploration, `cas_types`) a maintenant un exercice où une seule question est posée, la vue arrêtée AVANT la réponse, la correction écrite comme le barème dans `question.demonstration`.

### 8.1 Inventaire : cas type → diapositive(s)

| Cas type (fréquence) | Avant | Après |
|---|---|---|
| domaine (1 + tous les exercices) | d1 (question, vue arrêtée sur `entoure`) | inchangé |
| équation (5) | q1_b, q5 (questions) | + `ln_e5_q` (2021 4.a, f(x) = x) |
| inéquation (signe de f′ dans 12) | q3 lu d'un bloc | + `ln_q3_b` (question, arrêt sur `regle`) |
| limite en 0⁺ (7) | e3_b lu | `ln_e3_b` question (2019 1.a) |
| limite en +∞ (9) | e3_b lu | `ln_e3_c` nouvelle (2019 1.b) |
| dérivée et forme donnée (13) | v1 (question), v2_b lu | `ln_v2_b` question (2019 2.b), e5 (2021 3.b) |
| signe de f′, variations (10) | e3 (question mais réponse écrite par la vue), e5_b lu | e3 vue `variations_pas` ; `ln_e5_b` question |
| fonction auxiliaire et inégalité (11) | e1 (la voix donnait la conclusion), e5_c | e1 arrêtée avant la conclusion ; e5_c inchangée (question) |
| position (5) | e4 (question), e4_b lu | `ln_e4_b` question (2019 4.a) |
| point d'inflexion (4) | e6_c (autre fonction, lu) | + `ln_e3_d` (2019 3.b, question) |
| tangente (3) | c5 lu | + question de `ln_e4_c` (tangente en A(e ; e) = (Δ)) |
| construction (10) | e4_b et e5_c : courbe tracée d'un coup | `ln_e4_c` + `ln_e4_d` (2019) et `ln_e5_c` (2021) : vue `construire.html`, un moment par élément, la courbe en dernier |
| primitive u′/u (2) | p1 (question) | inchangé |
| plus petit n (1) | q7 lu | + `ln_q7_b` (question, arrêt avant la division par un négatif) |
| suite uₙ₊₁ = f(uₙ) (7) | — (chapitre des suites) | reste à faire, hors de ce chapitre |

Problèmes nationaux joués une question à la fois :
- **2019** (séances 6 et 7) : v2_b (2.b) → e2 → e3 (2.c, minimum) → e3_b (1.a) → e3_c (1.b) → e3_d (3.b) → e4 (4.a, f(x) − x) → e4_b (4.a, position) → e4_c (4.b, tangente en A) → e4_d (4.b, fin du tracé).
- **2021** (séance 8) : e5 (3.b, f′ ; 1 et 3.a faits en l8) → e5_b (3.c et 6.a) → e5_q (4.a) → e5_c (4.b, puis 6.b).

### 8.2 Questions dont la vue (ou la voix) donnait la réponse
- `ln_n2` : `existe` écrivait « continue sur un intervalle ⇒ des primitives existent » et la voix le disait ; arrêt sur `inverse`, `variante` retirée.
- `ln_e1` : `minimum` écrivait la conclusion encadrée, la voix et l'encadré central la disaient ; arrêt sur `tableau`.
- `ln_e3` : `fleches` écrivait « f(1) = 3/2 » ; nouvelle vue `variations_pas` où la valeur a son propre moment `minimum`.
- `ln_e4_b`, `ln_e5_b` : la voix donnait le résultat ; les vues s'arrêtent sur `droite` / `origine`.
- Contrôlées et laissées : c2, z4_sens, d1, a1, a5, q1_b et q5 (les racines sont posées, le tri reste à l'élève), l2, l6, v1, p1, e4, e5, e5_c, e6_c, b2.

### 8.3 Animations ajoutées (le cours en ligne n'est pas touché : vues AJOUTÉES)
- `signe.html?vue=variations_pas` : moments tableau_vide, fleches, minimum, limite_0, asymptote, limite_inf ; repères fprime, fleches, minimum, limite_0, asymptote, limite_inf. La vue `variations` (en ligne) est inchangée.
- `construire.html` (NOUVEAU fichier, mode large `LnLarge` comme `etude.html`) : `?vue=c19` — repere, asymptote, delta, minimum, contact, tangente_e, inflexion, branche, courbe ; `?vue=c21` — repere, origine, minimum, zero, droite, branche, courbe ; un repère par élément nommé, colonne de droite numérotée ① à ⑦.
- `calculs-vues.js` : vues `e3d` (enonce, signe, racine, tableau, change, image, resultat), `e5q` (zero, enonce, ramener, factoriser, tri, ln, resoudre, resultat), `q3b` (enonce, domaine, regle, resoudre, croiser, resultat), `q7b` (enonce, passer, descendre, sens, calcul, resultat). **Ajoutées à la main : à reporter dans les sources du build** (`maths_build/fonctions_ln/p*.py`).
- `calculs.html` : la description pour le tuteur passe une fraction `⟦num|dén⟧` par `Tableau.lisible` (aucune vue en ligne n'en contient : rendu inchangé).
- Pour que l'iframe se recharge entre deux diapositives de la même vue, les URL suivantes portent `&etape=2`/`&etape=3` (paramètre ignoré par le kit).
- Vérifié : `node --check`, Chromium sans erreur console, captures 1280 × 640 et 724 × 350 au début, à l'arrêt et à la fin.

### 8.4 Rejeu après la réponse
- `ln_n2` — `naissance.html?vue=famille` — existe, famille, glisse
- `ln_v2_b` — `calculs.html?vue=v2` — deriver, resultat
- `ln_e1` — `inegalite.html?vue=ecart` — minimum
- `ln_e3` — `signe.html?vue=variations_pas` — minimum
- `ln_e3_b` — `signe.html?vue=variations_pas&etape=2` — limite_0, asymptote
- `ln_e3_c` — `signe.html?vue=variations_pas&etape=3` — limite_inf
- `ln_e3_d` — `calculs.html?vue=e3d` — image, resultat
- `ln_e4` — `etude.html?vue=position` — (la réponse est écrite par `ecart`) ecart
- `ln_e4_b` — `etude.html?vue=position&etape=2` — ecart, contact
- `ln_e4_c` — `construire.html?vue=c19` — tangente_e
- `ln_e5_b` — `etude.html?vue=national&etape=2` — minimum
- `ln_e5_q` — `calculs.html?vue=e5q` — tri, ln, resoudre, resultat
- `ln_q3_b` — `calculs.html?vue=q3b` — resoudre, croiser, resultat
- `ln_q7_b` — `calculs.html?vue=q7b` — sens, calcul, resultat

**Écrit dans le cours (18 novembre 2026)** : chaque diapositive de cette liste porte `concentration.apres_reponse` (une étape `play_until` par moment, dans l'ordre), débloqué par sa première question (`q`). Le lecteur ne joue ces moments qu'après la réponse, même si un pointage les demandait ; contrôle : `python -I backend/scripts/verifier_parcours.py` (rien d'imprimé). Chaque moment a été vérifié dans Chromium : présent dans la vue de la diapositive, après le dernier moment de son pointage.

### 8.5 Mots
`verifier_mots.py` passé sur les 16 pistes de diapositives, les 10 démonstrations et les 10 énoncés nouveaux.
- Remplacés : « الطباشير » → « نرسموها بلا ما نحبسو » ; « كنقيسو » → « كنحسبو » ; « construire » → « نرسمو » ; « كنرسموش » (phrase refaite) ; « كتحترمها », « كتلمسها », « كتدوز », « حطيناها » → « كتمشي مع كل شي حطينا », « كتلاقى delta », « كتوصل لـ I » ; « كتتبدل » → « كتبدل » ; « حليناها » → « درناها » ; « كنقاطعو » → « كناخدو الجزء المشترك » ; « dérivables » → « كل terme dérivable » ; « كنوحدو المقام » → « كنديرو نفس المقام » ; « كنحلو القوس » → « كنحيدو القوس » ; « وكتلاقاها » → « وكتلاقى معاها ».
- Gardés (termes du programme), **à écouter** : « d'inflexion » (e3_d, e4_d), « entier » (q7_b), « demi-tangente » et « inégalité » (e5_c).

### 8.6 Ce qui reste à faire
- **Voix** : 16 diapositives, 10 démonstrations, 10 énoncés (`_voix.json`) ; **réactions des 10 nouvelles questions** (`concentration.reponses.q`) à générer (`preparer_reponses.py`), ainsi que celles de l'exercice nouveau du bloc `ln_s5_b1d`.
- Le vérificateur de pointage signale des lignes GESTE sur les diapositives sans voix (durée 0 : tous les gestes à 0 s) : elles disparaîtront avec les pistes.
- Kit commun (`maths/commun/exposants.js`, à ne pas toucher ici) : une chaîne qui contient un exposant n'écrit pas les fractions `⟦num|dén⟧` ; les lignes concernées (f″(x) = (2 − ln x)/x², (1/3)ⁿ) restent en barre sans espaces.
- 2021 : les limites en +∞ (2.a, 2.b) sont dites dans la construction, pas posées en question ; 2021 1 et 3.a sont faits en l8 (exemple lu).
- Report des vues `e3d`, `e5q`, `q3b`, `q7b` dans les sources du build de `calculs-vues.js`.
