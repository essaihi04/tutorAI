# math_ch5_fonctions_ln — Fonctions logarithmiques

## Ouverture — une fonction qui transforme les produits ; primitive et puissances

### Diapo 1 `ln_ouverture_cours` — Fonctions logarithmiques
VOIX (fr) : Bienvenue dans un nouveau cours : Fonctions logarithmiques. Dans ce cours, nous allons apprendre la fonction logarithme népérien : le domaine, les règles de calcul, les limites, la dérivée, et le logarithme décimal. La fonction ln est presque dans chaque problème d'analyse du national, et l'analyse compte pour cinquante-cinq pour cent de la note. Comment allons-nous travailler ? Tu écoutes bien, tu réponds aux questions au tableau, et quand le cours s'arrête, tu écris dans ton cahier. Allons-y !
ÉCRAN : On apprend : ln : domaine, règles de calcul, limites, dérivée, log | Au bac : ln dans presque chaque problème d'analyse | Écouter · répondre au tableau · écrire dans le cahier

### Diapo 2 `ln_o1` — La carte du chapitre : une fonction qui transforme les produits
VOIX (fr) : Regarde le centre : un petit repère, et une courbe rouge qui s'appelle ln. Elle passe par le point un, zéro. C'est une fonction nouvelle. Autour, les questions du chapitre. D'abord, où existe-t-elle ? Il faut que u de x soit strictement positif. Ensuite les règles : ln de a fois b, égale ln a plus ln b. Puis les équations et les inéquations. Puis les limites. Puis la dérivée de ln u. Et le gros morceau : l'étude d'une fonction, le problème du national. Puis les primitives, et enfin log et le pH. En bas, en jaune : ln est dans dix-huit sujets sur vingt, et un problème avec ln dans douze.
ÉCRAN : Au centre : la courbe de ln, qui passe par le point (1 ; 0). | Autour, les questions du national : domaine, règles, équations, limites, dérivée, étude, primitives, log. | ln transforme un produit en somme : ln(ab) = ln a + ln b. | ln est dans 18 sujets nationaux sur 20 ; un problème avec ln dans 12.

### Diapo 3 `ln_z1_primitive` — Rappel : une primitive, c'est la dérivée à l'envers
VOIX (fr) : Rappel du chapitre précédent : une primitive. Sur la courbe de F(x) = x², la pente de la tangente vaut 2x : F′(x) = 2x, donc F est une primitive de f(x) = 2x. Autrement : montée de 3, la courbe garde les mêmes pentes ; x² + 3 est aussi une primitive de 2x. Je relis : F est une primitive de f sur I si F′(x) = f(x) pour tout x de I.
ÉCRAN : F(x) = x² : la pente de la tangente vaut 2x, donc F′(x) = 2x. | F′ = f : F est une primitive de f(x) = 2x. | x² + 3 a les mêmes pentes : c'est aussi une primitive de 2x.

### Diapo 4 `ln_z2_puissances` — Rappel : les puissances, 2⁰ = 1 et x⁻¹ = 1/x
VOIX (fr) : Les puissances. 2³ = 2 × 2 × 2 = 8. Sur les barres : 8, 4, 2 ; une puissance de moins, on divise par 2 ; donc 2⁰ = 1 et 2⁻¹ = 1/2. Autrement, par la règle : on multiplie, on ajoute les puissances ; x × x⁻¹ = x⁰ = 1, donc x⁻¹ = 1/x ; de même √x = x^(1/2). Je relis : x⁻¹ = 1/x et √x = x^(1/2).
ÉCRAN : 2³ = 2 × 2 × 2 = 8 ; une puissance de moins : on divise par 2. | 2⁰ = 1, 2⁻¹ = 1/2 ; de même x⁻¹ = 1/x. | On multiplie : on ajoute les puissances ; √x = x^(1/2).
## I. La naissance de ln : la primitive de 1/x qui s'annule en 1

### Diapo 5 `ln_n1` — La règle des puissances bute sur 1/x
VOIX (fr) : En haut, encadrée, la règle des puissances du chapitre précédent : x puissance n a pour primitive, x puissance n plus un, sur n plus un. On l'applique. x carré donne x cube sur trois. x donne x carré sur deux. Un sur x carré, c'est x puissance moins deux : il donne x puissance moins un, sur moins un, donc moins un sur x. Et maintenant un sur x, c'est x puissance moins un. La règle donne x puissance zéro, sur zéro. Regarde le zéro entouré en rouge : on doit diviser par zéro ! La ligne est barrée.
ÉCRAN : xⁿ → xⁿ⁺¹/(n + 1) : x² → x³/3 ; x → x²/2. | 1/x² = x⁻² → x⁻¹/(−1) = −1/x. | 1/x = x⁻¹ → x⁰/0 : division par zéro, la règle ne marche pas. | Il manque une primitive de 1/x : c'est elle qui va naître.

### Diapo 6 `ln_n2` — 1/x a quand même des primitives
VOIX (fr) : En haut, la courbe de un sur x, pour x strictement positif. Elle se trace sans lever la craie : elle est continue sur l'intervalle zéro, plus l'infini. Rappelle-toi le chapitre des primitives : que sait-on d'une fonction continue sur un intervalle ? Question : un sur x est continue sur zéro, plus l'infini, que peut-on en déduire ?
ÉCRAN : x ↦ 1/x est continue sur l'intervalle ]0 ; +∞[. | À toi : que dit le chapitre des primitives d'une fonction continue sur un intervalle ?
QUESTION : x ↦ 1/x est continue sur ]0 ; +∞[ : que peut-on en déduire ? OPTIONS : ["Elle n'a aucune primitive sur ]0 ; +∞[", 'Elle admet des primitives sur ]0 ; +∞[', 'Sa primitive est x⁰/0']
EXERCICE : Vrai ou faux ? OPTIONS : None

### Diapo 7 `ln_n3` — La primitive qui passe par (1 ; 0) s'appelle ln
VOIX (fr) : Voici de nouveau la famille F plus k, en traits fins. En jaune, un point : un, zéro. Une courbe épaisse descend doucement. Elle touche le point un, zéro : elle devient rouge, et elle reçoit son nom, ln. C'est exactement la question du chapitre des primitives : la primitive qui vérifie F de un égale zéro. À droite, la définition : ln est la primitive de un sur x, sur zéro, plus l'infini, qui s'annule en un. On lit ln, logarithme népérien. Autrement dit : on connaît la pente de ln en chaque point, 1/x, et son point de départ, (1 ; 0) : cela suffit pour tracer toute la courbe. Je relis : ln est la primitive de 1/x sur ]0 ; +∞[ qui s'annule en 1.
ÉCRAN : Dans la famille F + k, une seule courbe passe par le point (1 ; 0). | Comme au chapitre des primitives : la primitive qui vérifie F(1) = 0. | Définition : ln est la primitive de x ↦ 1/x sur ]0 ; +∞[ qui s'annule en 1. | ln se lit « logarithme népérien ».

### Diapo 8 `ln_n4` — Deux faits tout de suite : ln 1 = 0 et (ln x)' = 1/x
VOIX (fr) : La courbe rouge de ln, et le point un, zéro. Premier fait, écrit près du point : ln de un égale zéro. Ce n'est pas un calcul, c'est la définition : ln s'annule en un. Maintenant les tangentes en un, en deux et en quatre. Leurs pentes sont écrites : un, zéro virgule cinq, zéro virgule vingt-cinq. C'est un sur x ! Deuxième fait, encadré : la dérivée de ln x est un sur x, sur zéro, plus l'infini. Un point glisse sur la courbe avec sa tangente, et la pente vaut toujours un sur x.
ÉCRAN : ln s'annule en 1 : ln 1 = 0. | ln est une primitive de 1/x : (ln x)' = 1/x sur ]0 ; +∞[. | La pente de la tangente en x vaut 1/x : 1 en x = 1, 0,5 en x = 2, 0,25 en x = 4.
## II. La courbe de ln : croissance, signe, e, tangente

### Diapo 9 `ln_c1` — ln monte toujours
VOIX (fr) : On place des points de la courbe. En zéro virgule cinq, ln vaut environ moins zéro virgule soixante-neuf. En un, zéro. En deux, zéro virgule soixante-neuf. En quatre, un virgule trente-neuf. On relie : la courbe se trace. Maintenant un point glisse de gauche à droite. Regarde sa hauteur : elle monte toujours, et sa petite tangente monte aussi. Pourquoi ? Encadré : la dérivée est un sur x, et un sur x est strictement positif, quand x est positif. Donc ln est strictement croissante sur zéro, plus l'infini.
ÉCRAN : (ln x)' = 1/x et 1/x > 0 pour tout x > 0. | Donc ln est strictement croissante sur ]0 ; +∞[. | Points de la courbe : (0,5 ; −0,69), (1 ; 0), (2 ; 0,69), (4 ; 1,39).

### Diapo 10 `ln_c2` — Négatif avant 1, positif après 1
VOIX (fr) : La courbe de ln. Regarde la partie entre 0 et 1 : sous l'axe, ln x est négatif, alors que x est positif. En 1 : ln 1 = 0. Après 1, au-dessus de l'axe : ln x positif. Le tableau de signe le résume. Autrement : ln monte toujours et vaut 0 en 1 ; avant 1 elle est donc sous 0, après 1 au-dessus. Question : ln(3/4) est-il positif ou négatif ?
ÉCRAN : Sur ]0 ; 1[ : la courbe est sous l'axe, ln x < 0. | En 1 : ln 1 = 0. | Sur ]1 ; +∞[ : la courbe est au-dessus de l'axe, ln x > 0. | ln monte toujours et ln 1 = 0 : avant 1 elle est sous 0, après 1 au-dessus.
QUESTION : ln(3/4) est : OPTIONS : ['positif', 'nul', 'négatif']
EXERCICE : ln 0,3 est : OPTIONS : ['négatif', 'positif', 'non défini']
OBSERVATION : Entre 0 et 1, où est la courbe de ln par rapport à l'axe des abscisses ?

### Diapo 11 `ln_c3` — Le nombre e : là où ln vaut 1
VOIX (fr) : La courbe de ln. On trace en pointillés jaunes, la droite horizontale à la hauteur un. Elle coupe la courbe en un seul point, car ln est continue et strictement croissante, sur zéro, plus l'infini. On descend jusqu'à l'axe : on lit un nombre, environ deux virgule sept un huit. Ce nombre s'appelle e. ln de e égale un. Pour le situer : ln deux vaut environ zéro virgule soixante-neuf, plus petit que un. ln trois vaut environ un virgule dix, plus grand que un. Donc e est entre deux et trois. Et e est un nombre irrationnel : on garde l'écriture e.
ÉCRAN : ln est continue (car dérivable) et strictement croissante sur ]0 ; +∞[ : la droite y = 1 coupe la courbe de ln en un seul point. | Son abscisse est le nombre e : ln e = 1, e ≈ 2,718. | ln 2 ≈ 0,69 < 1 et ln 3 ≈ 1,10 > 1, donc 2 < e < 3. | e est un nombre irrationnel : on garde l'écriture e.

### Diapo 12 `ln_c4` — ln compare comme x compare
VOIX (fr) : Sur la courbe, deux points : a égale deux et b égale cinq. Leurs hauteurs en pointillés : ln deux et ln cinq. Sur l'axe, a est avant b ; en hauteur, ln a est sous ln b. Même ordre ! On écrit : ln a inférieur à ln b, équivaut à a inférieur à b. Et si deux hauteurs sont égales, il n'y a qu'un seul x : ln a égale ln b équivaut à a égale b. Exemple : ln x plus petit que ln cinq. Sur l'axe, on colorie en vert de zéro à cinq, avec des ronds vides : x doit rester positif.
ÉCRAN : ln est strictement croissante sur ]0 ; +∞[. | Pour a > 0 et b > 0 : ln a < ln b ⇔ a < b. | ln a = ln b ⇔ a = b : une seule hauteur, un seul x. | Exemple : ln x < ln 5 ⇔ 0 < x < 5 (sans oublier x > 0).

### Diapo 13 `ln_c5` — La tangente en 1 : y = x − 1
VOIX (fr) : La courbe de ln, et le point un, zéro. On trace la tangente en ce point, en jaune. Sa pente, c'est la dérivée en un : un sur un, donc un. L'équation de la tangente : y égale f prime de a, fois x moins a, plus f de a. Ici, un fois x moins un, plus zéro. Encadré : y égale x moins un. Regarde maintenant l'écart entre la droite et la courbe, hachuré : la courbe reste toujours sous sa tangente. On le démontrera plus loin.
ÉCRAN : Tangente en a : y = f'(a)(x − a) + f(a). | En a = 1 : ln 1 = 0 et ln'(1) = 1/1 = 1. | (T) : y = x − 1. | La courbe de ln reste sous (T) : on le démontrera (ln x ≤ x − 1).
## III. L'ensemble de définition : u(x) > 0

### Diapo 14 `ln_z4_sens` — Rappel : multiplier par un négatif change le sens
VOIX (fr) : Les inégalités. 2 < 3. On multiplie par −1 : les points passent de l'autre côté de 0, −3 est à gauche, donc −2 > −3 : le sens a changé. Autrement : sans changer le sens, on écrirait −2 < −3, ce qui est faux. Exemple : −2x > 4 ; on divise par −2, négatif : x < −2. Je relis : multiplier ou diviser par un négatif change le sens. Question : −3x < 6, que vaut x ?
ÉCRAN : 2 < 3 ; fois −1 : −2 et −3 changent de place sur l'axe. | −2 > −3 : le sens a changé. | −2x > 4 ⇔ x < −2 (on divise par −2).
QUESTION : −3x < 6 ⇔ ? OPTIONS : ['x < −2', 'x > −2', 'x > 2']

### Diapo 15 `ln_d1` — Une condition par ln : u(x) > 0
VOIX (fr) : f(x) = ln(2x − 6). On entoure ce qu'il y a dans ln : 2x − 6. ln n'accepte qu'un nombre strictement positif : 2x − 6 > 0. Autrement : ln est une porte qui ne laisse passer que les nombres positifs ; la courbe de ln n'existe pas à gauche de 0, ln(−1) et ln 0 n'existent pas. Je relis : x ∈ D_f ⇔ u(x) > 0. Question : détermine D_f.
ÉCRAN : ln n'accepte qu'un nombre strictement positif. | On entoure ce qu'il y a dans ln : 2x − 6, et on écrit 2x − 6 > 0. | La courbe de ln n'existe pas à gauche de 0 : ln(−1) et ln 0 n'existent pas.
QUESTION : f(x) = ln(2x − 6) : quel est D_f ? OPTIONS : [']−∞ ; 3[', ']3 ; +∞[', '[3 ; +∞[']
EXERCICE : f(x) = ln(4 − x) : quel est D_f ? OPTIONS : [']4 ; +∞[', ']−∞ ; 4[', 'ℝ']

### Diapo 16 `ln_z3_signe` — Rappel : le signe de x − 1
VOIX (fr) : Le signe de x − 1. Un point glisse sur l'axe : en −1, x − 1 = −2, négatif ; après 1, en 3, x − 1 = 2, positif ; en 1, x − 1 = 0 : la racine. Le tableau de signe : −, 0, +. Autrement, la droite y = x − 1 : sous l'axe avant 1, au-dessus après. Je relis : ax + b a le signe de a après la racine, le signe contraire avant.
ÉCRAN : x − 1 s'annule en x = 1 : c'est la racine. | Avant 1 : x − 1 < 0 ; après 1 : x − 1 > 0. | La droite y = x − 1 est sous l'axe avant 1, au-dessus après.

### Diapo 17 `ln_d2` — Un quotient dans ln : tableau de signe
VOIX (fr) : Maintenant, ln contient un quotient : cinq x sur trois moins x. La condition s'écrit : le quotient strictement positif, et trois moins x différent de zéro. On cherche les racines. Cinq x s'annule en zéro. Trois moins x s'annule en trois. Regarde le tableau de signe. Sur la ligne cinq x : moins, zéro, plus. Sur la ligne trois moins x : plus, zéro, moins. Le quotient : moins, puis plus, puis moins. Sous trois, une double barre, car le dénominateur s'annule. La seule colonne positive est entre zéro et trois. Elle se colore en vert. Donc D f égale l'intervalle ouvert zéro, trois.
ÉCRAN : Condition : 5x/(3 − x) > 0 et 3 − x ≠ 0. | 5x s'annule en 0 ; 3 − x s'annule en 3. | Tableau de signe : le quotient est positif seulement entre 0 et 3. | Double barre sous 3 : le dénominateur s'annule.

### Diapo 18 `ln_d3` — Plusieurs conditions : « et »
VOIX (fr) : Ici, f de x égale un plus ln x, sur ln x. Il y a deux conditions. Première condition : ln x existe, donc x strictement positif. Deuxième condition : le dénominateur ne s'annule pas. ln x différent de zéro, c'est-à-dire x différent de un. Sur l'axe, x positif est colorié en vert, et en un, un rond vide rouge : un trou. Les deux conditions doivent être vraies en même temps. Le mot et est entouré. Le mot ou est barré en rouge. Le résultat : D f égale zéro, un, union un, plus l'infini.
ÉCRAN : ln x existe : x > 0. | Le dénominateur ne s'annule pas : ln x ≠ 0 ⇔ x ≠ 1. | Les deux conditions en même temps : « et », jamais « ou ». | D_f = ]0 ; 1[ ∪ ]1 ; +∞[ : un trou en 1.

### Diapo 19 `ln_d4` — ln|u| demande seulement u ≠ 0
VOIX (fr) : Cette fois, ln contient une valeur absolue : ln de valeur absolue de x moins deux. Une valeur absolue est toujours positive ou nulle. Elle est strictement positive, sauf quand x moins deux est nul. Donc la condition devient : x différent de deux. Sur l'axe, tout est vert, sauf un rond vide en deux. Le résultat : D f égale moins l'infini, deux, union deux, plus l'infini. Attention, en orange, le piège : sans valeur absolue, ln de x moins deux, demande x strictement supérieur à deux. Ce n'est pas le même domaine.
ÉCRAN : |x − 2| > 0 ⇔ x − 2 ≠ 0 ⇔ x ≠ 2. | Tout l'axe est permis, sauf 2. | D_f = ]−∞ ; 2[ ∪ ]2 ; +∞[. | Piège : ln(x − 2) (sans valeur absolue) demande x > 2.
## IV. Les règles de calcul

### Diapo 20 `ln_a1` — ln 6 = ln 2 + ln 3 ?
VOIX (fr) : À la calculatrice : ln 2 ≈ 0,69 ; ln 3 ≈ 1,10 ; ln 6 ≈ 1,79. On pose ln 3 sur ln 2 : regarde où arrive la pile. Exactement à la hauteur de ln 6 : 0,69 + 1,10 = 1,79. Et 6 = 2 × 3, donc ln(2 × 3) = ln 2 + ln 3. La règle : ln(ab) = ln a + ln b pour a et b strictement positifs. Autrement : ln change les produits en sommes, comme les zéros : 10 × 100 = 1000, un zéro plus deux zéros donnent trois zéros. Question : ln 2 ≈ 0,69 et ln 5 ≈ 1,61, que vaut ln 10 ?
ÉCRAN : ln 2 et ln 3 empilés arrivent à la hauteur de ln 6, et 6 = 2 × 3. | Le logarithme d'un produit est la somme des logarithmes. | Comme les zéros : 10 × 100 = 1000, 1 zéro + 2 zéros = 3 zéros.
QUESTION : ln 2 ≈ 0,69 et ln 5 ≈ 1,61 : que vaut ln 10 environ ? OPTIONS : ['2,30', '1,11', '0,92']
EXERCICE : ln 2 ≈ 0,69 et ln 3 ≈ 1,10 : que vaut ln 18 environ ? (18 = 2 × 3 × 3) OPTIONS : ['1,79', '2,89', '3,30']
OBSERVATION : ln 3 posé sur ln 2 : jusqu'où arrive la pile ?

### Diapo 21 `ln_a2` — Multiplier x par a, c'est monter la courbe de ln a
VOIX (fr) : Regarde les deux courbes : ln x en rouge, et ln de deux x en cyan. Entre les deux, des flèches verticales, en x égale un, deux et quatre. Elles ont toutes la même longueur : ln deux. En x égale deux, la hauteur ln quatre est faite de deux morceaux empilés : ln deux, puis encore ln deux. Pourquoi ? La dérivée de ln de a x, c'est a sur a x, donc un sur x. C'est la même dérivée que ln x. Les deux fonctions diffèrent donc d'une constante. En x égale un, cette constante vaut ln a. Quand on change a, toute la courbe monte de ln a. Si a est plus petit que un, elle descend. La formule : ln de a fois b, égale ln a plus ln b.
ÉCRAN : La courbe de ln(2x) est celle de ln x montée de ln 2. | Preuve : (ln(ax))' = a/(ax) = 1/x = (ln x)' ; les deux fonctions diffèrent d'une constante. | En x = 1 : ln(a × 1) − ln 1 = ln a. La constante vaut ln a. | Donc ln(ax) = ln a + ln x : c'est la règle du produit.

### Diapo 22 `ln_a3` — L'inverse donne un moins
VOIX (fr) : On part du produit : a × 1/a = 1, donc ln a + ln(1/a) = ln 1 = 0. D'où ln(1/a) = −ln a : l'inverse donne un moins. Autrement : 1/2 est plus petit que 1, son ln est négatif ; ln(1/2) ≈ −0,69 = −ln 2.
ÉCRAN : a × 1/a = 1, donc ln a + ln(1/a) = ln 1 = 0. | ln(1/a) = −ln a : l'inverse donne un moins. | ln(1/2) ≈ −0,69 = −ln 2.

### Diapo 23 `ln_a3_b` — Le quotient donne une différence
VOIX (fr) : Le quotient : a/b = a × 1/b, donc ln(a/b) = ln a + ln(1/b) = ln a − ln b. Le quotient donne une différence. Exemple : ln(1/8) = −ln 8 = −3 ln 2. Ce moins s'oublie souvent : écris-le tout de suite.
ÉCRAN : a/b = a × 1/b, donc ln(a/b) = ln a − ln b. | ln(1/8) = −ln 8 = −3 ln 2. | Le moins s'oublie souvent : on l'écrit tout de suite.

### Diapo 24 `ln_a4` — La puissance descend devant
VOIX (fr) : ln(a²) = ln(a × a) = 2 ln a. De même ln(aⁿ) = n ln a pour n entier : la puissance descend devant. Autrement, avec les blocs : a⁴ = a × a × a × a, donc quatre blocs ln a empilés : 4 ln a.
ÉCRAN : ln(a²) = ln(a × a) = 2 ln a. | ln(aⁿ) = n ln a (n entier) : n blocs ln a empilés.

### Diapo 25 `ln_a4_b` — La racine donne un demi
VOIX (fr) : La racine : √a × √a = a, donc 2 ln √a = ln a et ln √a = ½ ln a. Plus généralement ln(aʳ) = r ln a pour r rationnel. Exemple : ln(√2 × 8) = ½ ln 2 + 3 ln 2 = (7/2) ln 2.
ÉCRAN : √a × √a = a, donc 2 ln √a = ln a. | ln √a = ½ ln a ; plus généralement ln(aʳ) = r ln a (r ∈ ℚ). | ln(√2 × 8) = ½ ln 2 + 3 ln 2 = (7/2) ln 2.

### Diapo 26 `ln_a5` — Simplifier : d'abord les nombres premiers
VOIX (fr) : A = ln 12 − ln 27 + ln √2. Étape 1 : facteurs premiers, 12 = 2² × 3, 27 = 3³. Étape 2 : les règles, A = 2 ln 2 + ln 3 − 3 ln 3 + ½ ln 2. Étape 3, à toi : regroupe les ln 2 ensemble et les ln 3 ensemble. Question : simplifie A.
ÉCRAN : ① On décompose chaque nombre en facteurs premiers : 12 = 2² × 3 ; 27 = 3³. | ② On applique les règles : produit, puissance, racine. | ③ On regroupe les ln 2 ensemble et les ln 3 ensemble.
QUESTION : A = ln 12 − ln 27 + ln √2 = ? OPTIONS : ['(3/2) ln 2 − 2 ln 3', '(5/2) ln 2 − 2 ln 3', '(5/2) ln 2 + 4 ln 3']
EXERCICE : Simplifie C = ln 8 + ln 9 − ln 6. OPTIONS : ['2 ln 2 + ln 3', '3 ln 2 + ln 3', 'ln 11']

### Diapo 27 `ln_a6` — ln ne casse pas les sommes
VOIX (fr) : Premier piège : la somme. ln(1 + 1) = ln 2 ≈ 0,69, mais ln 1 + ln 1 = 0. Donc ln(a + b) n'est pas ln a + ln b ; la règle fausse est barrée. ln transforme un produit, jamais une somme.
ÉCRAN : ln(1 + 1) = ln 2 ≈ 0,69 mais ln 1 + ln 1 = 0 : ln(a + b) ≠ ln a + ln b. | La règle marche pour un produit, jamais pour une somme.

### Diapo 28 `ln_a6_b` — ln(x²) = 2 ln|x|
VOIX (fr) : Deuxième piège : le carré. Pour x = −1 : x² = 1 et ln 1 = 0, mais −1 n'est pas dans ]0 ; +∞[ : 2 ln x n'a pas de sens. La valeur absolue enlève le signe : |−1| = 1. La règle juste : pour x ≠ 0, ln(x²) = 2 ln|x|.
ÉCRAN : Pour x ≠ 0 : ln(x²) = 2 ln|x|. | ln(x²) = 2 ln x seulement si x > 0.

### Diapo 29 `ln_a7` — Trouve l'erreur
VOIX (fr) : Voici un calcul fait par un élève. B égale ln seize, moins ln vingt-sept, plus trois ln trente-six, moins ln racine de deux. La décomposition est juste : quatre ln deux, moins trois ln trois, plus trois ln de deux carré fois trois carré, moins un demi ln deux. Mais regarde la ligne suivante : il a écrit moins trois ln deux. C'est la ligne fausse : elle est barrée en rouge. Trois ln trente-six, c'est trois fois deux ln deux plus deux ln trois. Donc plus six ln deux, plus six ln trois. La ligne corrigée est en vert. On regroupe : quatre plus six moins un demi, dix-neuf demis ln deux. Et moins trois plus six, trois ln trois.
ÉCRAN : 16 = 2⁴ ; 27 = 3³ ; 36 = 2² × 3² ; √2 = 2^(1/2). | Ligne fausse : 3 ln 36 a donné −3 ln 2 au lieu de + 6 ln 2. | 3 ln(2² × 3²) = 3(2 ln 2 + 2 ln 3) = 6 ln 2 + 6 ln 3. | B = (19/2) ln 2 + 3 ln 3.

### Diapo 30 `ln_a8` — ln(eʳ) = r
VOIX (fr) : Sur la courbe de ln, on place des points. D'abord e, à la hauteur un : ln e égale un. Ensuite e carré, environ sept virgule quatre, à la hauteur deux. Car ln de e carré, c'est deux ln e, donc deux. Puis un sur e, environ zéro virgule trente-sept, à la hauteur moins un. Car ln de un sur e, c'est moins ln e. Puis racine de e, environ un virgule six, à la hauteur un demi. La règle : ln de e puissance r, c'est r ln e, donc r. Donc ln de e puissance r égale r. e puissance r, c'est le nombre dont le ln vaut r. La fonction qui le donne viendra au chapitre suivant.
ÉCRAN : ln(eʳ) = r ln e = r × 1 = r. | ln(e²) = 2 : e² ≈ 7,4 ; ln(1/e) = −1 : 1/e ≈ 0,37 ; ln √e = ½ : √e ≈ 1,6. | eʳ est le nombre dont le ln vaut r. | La fonction qui donne eʳ viendra au chapitre suivant.
## V. Équations, inéquations, systèmes

### Diapo 31 `ln_q1` — ln a = ln b : d'abord le domaine
VOIX (fr) : L'équation ln(x − 1) + ln(x + 2) = ln 4. Avant de calculer, le domaine : x > 1 en vert, x > −2 en bleu ; la partie commune est x > 1. Puis on rassemble en un seul ln, et on enlève les ln : ln a = ln b ⇔ a = b. Donc (x − 1)(x + 2) = 4.
ÉCRAN : D'abord D_E, l'ensemble où l'équation a un sens : x − 1 > 0 et x + 2 > 0 ⇔ x > 1, donc D_E = ]1 ; +∞[. | On rassemble en un seul ln : ln((x − 1)(x + 2)) = ln 4.

### Diapo 32 `ln_z5_second_degre` — Rappel : l'équation du second degré
VOIX (fr) : L'équation du second degré x² + x − 6 = 0 : a = 1, b = 1, c = −6. Δ = b² − 4ac = 25, positif : deux solutions (−b ± √Δ)/(2a), x = 2 ou x = −3. Autrement, la parabole coupe l'axe en −3 et en 2. On vérifie : 4 + 2 − 6 = 0. Je relis : si Δ > 0, deux solutions (−b ± √Δ)/(2a).
ÉCRAN : Δ = b² − 4ac = 1 + 24 = 25 > 0 : deux solutions. | x = (−b ± √Δ)/(2a) : x = 2 ou x = −3. | Ce sont les abscisses où la parabole coupe l'axe.

### Diapo 33 `ln_q1_b` — Le second degré, puis trier les solutions
VOIX (fr) : On résout : (x − 1)(x + 2) = 4 donne x² + x − 6 = 0, le second degré qu'on vient de revoir : Δ = 25, deux valeurs 2 et −3. Mais ce n'est pas fini : chaque solution doit être dans le domaine x > 1. Regarde l'axe et trie toi-même. Question : quelles sont les solutions ?
ÉCRAN : (x − 1)(x + 2) = 4 ⇔ x² + x − 2 = 4 ⇔ x² + x − 6 = 0 ; Δ = 25 : x = 2 ou x = −3. | On trie : on ne garde que les solutions de D_E = ]1 ; +∞[, puis on conclut « S = … ».
QUESTION : Résous ln(x − 1) + ln(x + 2) = ln 4. OPTIONS : ['S = {2 ; −3}', 'S = {2}', 'S = {−3}']
EXERCICE : Résous ln(x + 3) = ln(2x − 1). OPTIONS : ['S = {4}', 'S = {−4}', 'Pas de solution']

### Diapo 34 `ln_q2` — ln x = r ⇔ x = eʳ
VOIX (fr) : Au tableau : ln de deux x moins un, égale un. D'abord le domaine : deux x moins un positif, donc x plus grand que un demi. Ensuite l'astuce : un, c'est ln e. On écrit donc ln de deux x moins un, égale ln e. On enlève les ln : deux x moins un égale e. Donc x égale un plus e, sur deux, environ un virgule quatre-vingt-six. Cette valeur est dans le domaine, on la garde. La règle générale : ln x égale r, équivaut à x égale e puissance r.
ÉCRAN : Le domaine : 2x − 1 > 0 ⇔ x > ½. | On écrit le nombre comme un ln : 1 = ln e. | ln(2x − 1) = ln e ⇔ 2x − 1 = e ⇔ x = (1 + e)/2 ≈ 1,86. | En général : ln x = r ⇔ x = eʳ.

### Diapo 35 `ln_q3` — Inéquation : ln garde le sens
VOIX (fr) : L'inéquation : ln de deux x moins un, plus petit que zéro. D'abord le domaine, en cyan sur l'axe : x plus grand que un demi. Puis on écrit zéro comme ln un. ln est strictement croissante, donc elle garde le sens. Deux x moins un plus petit que un, donc x plus petit que un, en vert. Attention, ce n'est pas fini. On croise avec le domaine : la partie commune, en jaune, va de un demi à un. Donc S égale l'intervalle ouvert, un demi, un.
ÉCRAN : D_I, l'ensemble où l'inéquation a un sens : 2x − 1 > 0 ⇔ x > ½. | 0 = ln 1 : ln(2x − 1) < ln 1. | ln est strictement croissante : ln a < ln b ⇔ a < b, le sens est gardé : 2x − 1 < 1 ⇔ x < 1. | On croise avec D_I : x > ½ et x < 1, donc S = ]½ ; 1[.

### Diapo 36 `ln_q3_b` — À toi : une inéquation avec deux ln
VOIX (fr) : À toi : une autre inéquation. ln de x moins deux, inférieur ou égal à ln de quatre moins x. Les mêmes étapes. D'abord le domaine : x moins deux strictement positif, et quatre moins x strictement positif, donc x entre deux et quatre. Puis la règle : ln est strictement croissante, donc elle garde le sens. Termine, et attention : ce n'est pas fini quand on enlève les ln. Question : quel est l'ensemble des solutions ?
ÉCRAN : ① les conditions : x − 2 > 0 et 4 − x > 0 ; | ② ln est strictement croissante : ln a ≤ ln b ⇔ a ≤ b ; | ③ à toi : résoudre, puis croiser avec le domaine.
QUESTION : Résous ln(x − 2) ≤ ln(4 − x). OPTIONS : ['S = ]−∞ ; 3]', 'S = [3 ; 4[', 'S = ]2 ; 3]']

### Diapo 37 `ln_q4` — Second degré en ln x : poser X = ln x
VOIX (fr) : Cette équation contient ln x au carré, et ln x. On reconnaît le second degré. Première ligne : on pose grand X égale ln x. L'équation devient X carré moins X moins deux égale zéro. Le discriminant vaut neuf. Donc X égale moins un, ou X égale deux. Attention, on cherche x, pas X. On revient : ln x égale moins un, donc x égale un sur e. Et ln x égale deux, donc x égale e carré. Les deux sont positifs, on les garde.
ÉCRAN : x > 0 ; on pose X = ln x : X² − X − 2 = 0. | Δ = 9 : X = −1 ou X = 2. | On revient à x : ln x = −1 ⇔ x = 1/e ; ln x = 2 ⇔ x = e². | S = {1/e ; e²}.

### Diapo 38 `ln_q5` — Produit nul avec ln (national 2021)
VOIX (fr) : National 2021 : 2x ln x − 2x = 0 sur ]0 ; +∞[. On factorise : 2x(ln x − 1) = 0. Produit nul : x = 0 ou ln x = 1, c'est-à-dire x = e. Sur l'axe, seuls les x strictement positifs sont permis. Trie toi-même. Question : quelles sont les solutions ?
ÉCRAN : On factorise : 2x(ln x − 1) = 0. | Produit nul : x = 0 ou ln x = 1 ⇔ x = 0 ou x = e. | 0 ∉ ]0 ; +∞[ : on le rejette. | S = {e}.
QUESTION : Résous dans ]0 ; +∞[ : 2x ln x − 2x = 0. OPTIONS : ['S = {e}', 'S = {0 ; e}', 'S = {1}']
EXERCICE : National 2017 : résous dans ]0 ; +∞[ : (1 − 2/x) ln x = 0. OPTIONS : ['S = {2}', 'S = {1 ; 2}', 'S = {1}']

### Diapo 39 `ln_q6` — Un système : changer d'inconnues
VOIX (fr) : Un système avec deux inconnues, x et y. D'abord les conditions : x positif, et y positif. Ensuite on change d'inconnues : grand X égale ln x, grand Y égale ln y. Le système devient X plus Y égale trois, et X moins Y égale un. C'est un système linéaire, comme au collège. On additionne : deux X égale quatre, donc X égale deux, puis Y égale un. On revient : ln x égale deux, donc x égale e carré. ln y égale un, donc y égale e.
ÉCRAN : Conditions : x > 0 et y > 0. | On pose X = ln x et Y = ln y : X + Y = 3 et X − Y = 1. | On additionne : 2X = 4, X = 2 ; puis Y = 1. | x = e² et y = e : S = {(e² ; e)}.

### Diapo 40 `ln_q7` — Le plus petit entier n : passer au ln
VOIX (fr) : Question classique du national, avec les suites : le plus petit entier n, tel que un quart puissance n, soit plus petit que dix puissance moins quatre. ln est strictement croissante : on passe au ln, et le sens reste. La puissance descend devant : n fois ln un quart. Et ln un quart, c'est moins ln quatre. À droite, moins quatre ln dix. Attention, en orange : on divise par moins ln quatre, un nombre négatif, donc le sens change. n plus grand que quatre ln dix sur ln quatre, environ six virgule soixante-quatre. Le plus petit entier, c'est sept.
ÉCRAN : ln est strictement croissante : on passe au ln sans changer le sens. | ln((1/4)ⁿ) = n ln(1/4) = −n ln 4. | ln(10⁻⁴) = −4 ln 10, donc −n ln 4 < −4 ln 10 : on divise par −ln 4 < 0, le sens change. | n > 4 ln 10/ln 4 ≈ 6,64 : le plus petit entier est n = 7.

### Diapo 41 `ln_q7_b` — À toi : le plus petit entier n
VOIX (fr) : À toi : la même question avec d'autres nombres. Le plus petit entier n tel que un tiers puissance n soit inférieur à dix puissance moins deux. ln est strictement croissante : on passe au ln. La puissance descend devant : n fois ln un tiers, c'est-à-dire moins n ln trois. Et à droite, moins deux ln dix. Termine, et attention à la division. Question : quel est le plus petit entier n ?
ÉCRAN : On passe au ln (ln est strictement croissante) ; | la puissance descend : n ln(1/3) = −n ln 3 ; | à toi : diviser, et regarder le sens (ln 10 ≈ 2,30 ; ln 3 ≈ 1,10).
QUESTION : Le plus petit entier n tel que (1/3)ⁿ < 10⁻² (ln 10 ≈ 2,30 ; ln 3 ≈ 1,10) est : OPTIONS : ['n = 4', 'n = 5', 'aucun : on trouve n < 4,19']
## VI. Les limites de base

### Diapo 42 `ln_l1` — ln x → +∞, mais lentement
VOIX (fr) : Regarde la courbe jusqu'à dix : ln dix, environ deux virgule trois. On recule : jusqu'à cent. ln cent, environ quatre virgule six. On recule encore : jusqu'à mille. ln mille, environ six virgule neuf. Tu vois la règle : chaque fois qu'on multiplie x par dix, ln monte seulement de deux virgule trois. Elle ne s'arrête jamais : la limite de ln x, quand x tend vers plus l'infini, égale plus l'infini. Mais elle monte de plus en plus lentement : c'est une branche parabolique, de direction l'axe des abscisses.
ÉCRAN : ln 10 ≈ 2,3 ; ln 100 ≈ 4,6 ; ln 1000 ≈ 6,9. | Multiplier x par 10, c'est ajouter ln 10 ≈ 2,3 à ln x. | lim_{x→+∞} ln x = +∞ : ln dépasse toute hauteur, mais très lentement. | Branche parabolique de direction l'axe des abscisses (pas d'asymptote horizontale).

### Diapo 43 `ln_l2` — En 0 à droite : ln x → −∞, asymptote verticale
VOIX (fr) : Regarde maintenant à gauche, près de zéro. ln zéro virgule un, environ moins deux virgule trois. ln zéro virgule zéro un, environ moins quatre virgule six. La courbe plonge, le long de l'axe des ordonnées. La droite x égale zéro, en pointillés orange : c'est une asymptote verticale. La limite de ln x, quand x tend vers zéro à droite, égale moins l'infini. Et la courbe ne touche jamais cet axe, parce que zéro n'est pas dans l'ensemble de définition. Question : la courbe de ln coupe-t-elle l'axe des ordonnées ?
ÉCRAN : ln 0,1 ≈ −2,3 ; ln 0,01 ≈ −4,6 : la courbe plonge. | lim_{x→0⁺} ln x = −∞. | La droite d'équation x = 0 (l'axe des ordonnées) est asymptote verticale.
QUESTION : La courbe de ln coupe-t-elle l'axe des ordonnées ? OPTIONS : ["Non : 0 n'est pas dans ]0 ; +∞[", 'Oui : elle passe par le point (0 ; 0)', 'Oui : très bas, car ln x → −∞ près de 0']
EXERCICE : lim_{x→0⁺} (x + ln x) = ? OPTIONS : ['−∞', '0', '+∞']

### Diapo 44 `ln_l3` — (ln x)/x → 0 : x l'emporte
VOIX (fr) : Trois courbes au tableau : ln x en rouge, racine de x en cyan, x en blanc. Toutes les trois montent vers plus l'infini. Mais qui va le plus vite ? Le curseur avance. À dix, ln x sur x vaut environ zéro virgule vingt-trois. À mille, environ zéro virgule zéro zéro sept. Le rapport s'écrase vers zéro : x l'emporte sur ln x. La limite de ln x sur x, en plus l'infini, égale zéro. Plus généralement, pour tout n entier naturel non nul, la limite de ln x sur x puissance n, en plus l'infini, égale zéro. Et cela justifie la branche parabolique : ln x tend vers plus l'infini, et ln x sur x tend vers zéro. Donc la courbe de ln admet une branche parabolique, de direction l'axe des abscisses.
ÉCRAN : ln x, √x et x tendent tous vers +∞. | Mais ln x reste très petit devant x : ln 10/10 ≈ 0,23 ; ln 1000/1000 ≈ 0,0069. | lim_{x→+∞} (ln x)/x = 0 : x l'emporte sur ln x. | Pour tout n ∈ ℕ* : lim_{x→+∞} (ln x)/xⁿ = 0, car 0 ≤ (ln x)/xⁿ ≤ (ln x)/x pour x ≥ 1. | lim_{x→+∞} ln x = +∞ et lim_{x→+∞} (ln x)/x = 0, donc la courbe de ln admet une branche parabolique de direction l'axe des abscisses au voisinage de +∞. | C'est une limite de base : on l'utilise sans la refaire.

### Diapo 45 `ln_l4` — x ln x → 0 en 0 à droite
VOIX (fr) : Près de zéro à droite, x tend vers zéro, et ln x vers moins l'infini. Le produit est une forme indéterminée. Regarde le tableau de valeurs : à zéro virgule un, environ moins zéro virgule vingt-trois. À zéro virgule zéro un, environ moins zéro virgule zéro quarante-six. Ça s'écrase. Le rectangle le montre : très haut, mais de plus en plus fin, son aire va vers zéro. Le signe : x est positif, ln x est négatif, donc le produit est négatif. La limite de x ln x, en zéro à droite, égale zéro. De même, pour tout n entier naturel non nul, la limite de x puissance n fois ln x, en zéro à droite, égale zéro.
ÉCRAN : x = 0,1 → x ln x ≈ −0,23 ; x = 0,01 → ≈ −0,046 ; x = 0,001 → ≈ −0,0069. | Le produit s'écrase vers 0 : x l'emporte encore. | Pour 0 < x < 1 : x > 0 et ln x < 0, donc x ln x < 0. | lim_{x→0⁺} x ln x = 0. | Pour tout n ∈ ℕ* : lim_{x→0⁺} xⁿ ln x = 0, car xⁿ ln x = xⁿ⁻¹ × x ln x.

### Diapo 46 `ln_l5` — Deux limites qui sont un nombre dérivé
VOIX (fr) : Regarde la courbe rouge et le point A, de coordonnées un et zéro. Un point M, d'abscisse x, est posé sur la courbe, et on trace la sécante A M. Sa pente, c'est ln x moins ln un, sur x moins un. Maintenant M glisse vers A. La pente de la sécante s'affiche, et elle s'approche de un. La sécante devient la tangente en A. C'est le nombre dérivé de ln en un, un sur un, donc un. Encadré : la limite de ln x sur x moins un, quand x tend vers un, égale un. Dessous, on pose x égale un plus h, et on obtient la deuxième limite : la limite de ln de un plus x sur x, quand x tend vers zéro, égale un.
ÉCRAN : (ln x − ln 1)/(x − 1) est le taux d'accroissement de ln entre 1 et x. | Quand x tend vers 1, il tend vers ln'(1) = 1/1 = 1. | lim_{x→1} (ln x)/(x − 1) = 1. | En posant x = 1 + h : lim_{h→0} ln(1 + h)/h = 1, soit lim_{x→0} ln(1 + x)/x = 1.

### Diapo 47 `ln_l6` — Une forme ∞ − ∞ : factoriser
VOIX (fr) : La limite de x − ln x en +∞ : forme ∞ − ∞. On factorise par le terme le plus fort, x : x − ln x = x(1 − (ln x)/x). La limite de base : (ln x)/x → 0. À toi de finir : que devient la parenthèse, puis x fois la parenthèse ? Question : que vaut cette limite ?
ÉCRAN : lim_{x→+∞} x = +∞ et lim_{x→+∞} ln x = +∞ : forme indéterminée ∞ − ∞. | On factorise par x (x > 0) : x − ln x = x(1 − (ln x)/x). | Limite de base : lim_{x→+∞} (ln x)/x = 0, donc la parenthèse tend vers 1.
QUESTION : Calcule lim_{x→+∞} (x − ln x). OPTIONS : ['0', '+∞', '1']
EXERCICE : Calcule lim_{x→+∞} (ln x − 2x). OPTIONS : ['+∞', '0', '−∞']

### Diapo 48 `ln_l7` — Limite déguisée : poser t = √x
VOIX (fr) : Au tableau : montrer que la limite, de ln x au carré sur x, en plus l'infini, est zéro. Ce n'est pas une limite de base, elle est déguisée. On pose t égale racine de x. Alors x égale t carré, et ln x égale deux ln t. Quand x tend vers plus l'infini, t aussi. On remplace : ln x au carré sur x devient quatre fois, ln t sur t, au carré. Et voilà la limite de base : ln t sur t tend vers zéro. Donc quatre fois zéro au carré, ça fait zéro. Cette question est tombée au national deux mille vingt-trois, sur deux points.
ÉCRAN : (ln x)²/x : forme ∞/∞, ce n'est pas directement une limite de base. | On pose t = √x : x = t², ln x = 2 ln t ; x → +∞ ⇔ t → +∞. | (ln x)²/x = (2 ln t)²/t² = 4((ln t)/t)². | (ln t)/t → 0, donc la limite vaut 0.

### Diapo 49 `ln_l8` — En 0 à droite : continuité et branche
VOIX (fr) : Au tableau, la fonction du national deux mille vingt et un : f de x égale deux x ln x, moins deux x, et f de zéro égale zéro. D'abord la limite de base : x ln x tend vers zéro, quand x tend vers zéro à droite, et deux x aussi. Donc f de x tend vers zéro, qui est f de zéro. En vert : f est continue à droite en zéro. Ensuite le taux d'accroissement : f de x moins f de zéro, sur x, égale deux ln x moins deux. En orange : il tend vers moins l'infini. Donc f n'est pas dérivable à droite en zéro. En jaune, l'interprétation : la courbe a une demi-tangente verticale à l'origine.
ÉCRAN : lim_{x→0⁺} x ln x = 0, donc lim_{x→0⁺} f(x) = 0 = f(0) : f est continue à droite en 0. | (f(x) − f(0))/x = (2x ln x − 2x)/x = 2 ln x − 2 → −∞ quand x → 0⁺, car lim_{x→0⁺} ln x = −∞. | f n'est pas dérivable à droite en 0 : la courbe a une demi-tangente verticale en O. | National 2021, questions 1 et 3.a.

### Diapo 50 `ln_l9` — Limite de ln(u(x)) : d'abord la limite de u(x)
VOIX (fr) : Maintenant la fonction f de x égale ln de x plus un. D'abord le domaine : x plus un strictement positif, donc x supérieur à moins un. Que se passe-t-il quand x tend vers moins un à droite ? x plus un tend vers zéro, en restant positif. Regarde la courbe de ln : quand ce qui est dans ln tend vers zéro à droite, ln plonge vers moins l'infini. Donc la limite de ln de x plus un, quand x tend vers moins un à droite, égale moins l'infini. Interprétation : la droite d'équation x égale moins un, est asymptote verticale. Autrement dit : on pose X égale x plus un. Quand x tend vers moins un à droite, X tend vers zéro à droite, et la limite de ln X est moins l'infini. Et en plus l'infini : x plus un tend vers plus l'infini, donc ln de x plus un tend aussi vers plus l'infini. La règle : d'abord la limite de ce qui est dans ln, puis la limite de ln.
ÉCRAN : Si lim_{x→a} u(x) = 0⁺, alors lim_{x→a} ln(u(x)) = −∞ ; si lim_{x→a} u(x) = +∞, alors lim_{x→a} ln(u(x)) = +∞ (a réel ou ±∞). | D_f : x + 1 > 0 ⇔ x > −1, donc D_f = ]−1 ; +∞[. | lim_{x→−1⁺} (x + 1) = 0⁺ et lim_{X→0⁺} ln X = −∞, donc lim_{x→−1⁺} ln(x + 1) = −∞. | Interprétation : la droite d'équation x = −1 est asymptote verticale à (C_f). | En +∞ : lim_{x→+∞} (x + 1) = +∞, donc lim_{x→+∞} ln(x + 1) = +∞.
## VII. La dérivée de ln u

### Diapo 51 `ln_v1` — (ln u)' = u'/u
VOIX (fr) : La règle : (ln u)' = u'/u, si u est dérivable et strictement positive. Autrement, sur un exemple connu : ln(2x) = ln 2 + ln x, de dérivée 1/x car ln 2 est une constante ; avec la règle, u = 2x, u' = 2, et 2/(2x) = 1/x : le même résultat. Exemple : f(x) = ln(x² + 1) ; u(x) = x² + 1 > 0 et u'(x) = 2x. Finis avec la règle. Attention : (ln u)' n'est pas 1/u. Et quand u ne s'annule pas sur I, même règle : (ln|u|)' = u'/u. Question : dérive ln(x² + 1).
ÉCRAN : ln u est une composée : on dérive l'intérieur u, puis on divise par u. | (ln u)' = u'/u, si u est dérivable et strictement positive sur I. | Si u est dérivable et ne s'annule pas sur I : (ln|u|)' = u'/u. | Vérification : ln(2x) = ln 2 + ln x a pour dérivée 1/x, et 2/(2x) = 1/x. | Piège : (ln u)' n'est pas 1/u.
QUESTION : Dérive f(x) = ln(x² + 1) sur ℝ. OPTIONS : ["f'(x) = 1/(x² + 1)", "f'(x) = 2x", "f'(x) = 2x/(x² + 1)"]
EXERCICE : Sur ]2/3 ; +∞[, la dérivée de ln(3x − 2) est : OPTIONS : ['3/(3x − 2)', '1/(3x − 2)', '3 ln(3x − 2)']

### Diapo 52 `ln_v2` — Dériver (ln x)² et x ln x
VOIX (fr) : Première ligne : (ln x)² est u² avec u = ln x ; (u²)' = 2u'u, donc ((ln x)²)' = 2 ln x / x. Deuxième ligne : x ln x est un produit : 1 × ln x + x × 1/x = ln x + 1.
ÉCRAN : (ln x)² est u² avec u = ln x : (u²)' = 2u'u, donc ((ln x)²)' = 2 ln x/x. | x ln x est un produit : (x ln x)' = 1 × ln x + x × 1/x = ln x + 1.

### Diapo 53 `ln_v2_b` — Au national 2019 : dériver terme par terme
VOIX (fr) : La fonction du national deux mille dix-neuf : f de x égale x plus un demi, moins ln x, plus un demi de ln x au carré. À toi : dérive terme par terme, puis réduis au même dénominateur. Question : combien vaut f prime de x ?
ÉCRAN : Exemple 2019 N : f(x) = x + ½ − ln x + ½(ln x)² sur ]0 ; +∞[. | À toi : dérive terme par terme, puis réduis au même dénominateur.
QUESTION : 2019 N : f(x) = x + ½ − ln x + ½(ln x)² sur ]0 ; +∞[. Que vaut f′(x) ? OPTIONS : ['(x + 1 − ln x)/x', '(x − 1 + ln x)/x', '1 − 1/x + 2 ln x']

### Diapo 54 `ln_v3` — Le signe de f' : celui de ln x, de 1 − ln x
VOIX (fr) : En haut : f prime de x égale un moins ln x, sur x carré. x carré est strictement positif, donc f prime de x, a le signe de un moins ln x. On résout : un moins ln x positif, équivaut à ln x inférieur à un, équivaut à x entre zéro et e. Le tableau se remplit : x de zéro à plus l'infini, avec e au milieu. Un moins ln x : plus, zéro en e, puis moins. Et f prime pareil. En orange, la double barre sous zéro : x est strictement positif, le tableau commence à zéro. Enfin la ligne de f : elle monte jusqu'à e, puis elle descend.
ÉCRAN : x² > 0 : f'(x) a le signe de 1 − ln x. | 1 − ln x > 0 ⇔ ln x < 1 ⇔ 0 < x < e. | Tableau sur ]0 ; +∞[ : + avant e, 0 en e, − après e. | Le tableau commence à 0 (double barre) : x > 0.
## VIII. Les primitives u'/u

### Diapo 55 `ln_p1` — À l'envers : u'/u a pour primitive ln u
VOIX (fr) : Le tableau des primitives du chapitre précédent : il manquait une ligne. Les nouvelles lignes : 1/x a pour primitive ln x (x > 0) ; u'/u a pour primitive ln u (u > 0). Quand le haut est la dérivée du bas, la primitive est ln du bas. Exemple : 2x/(x² + 1) ; u = x² + 1 et u' = 2x, c'est le haut. À toi de finir. Question : donne une primitive de 2x/(x² + 1).
ÉCRAN : Aller : (ln u)' = u'/u. Retour : u'/u a pour primitive ln u (u > 0). | Nouvelle ligne du tableau : 1/x → ln x sur ]0 ; +∞[. | 2x/(x² + 1) : le haut 2x est la dérivée du bas x² + 1.
QUESTION : Une primitive de f(x) = 2x/(x² + 1) sur ℝ est : OPTIONS : ['ln(x² + 1)', '2x ln(x² + 1)', '1/(x² + 1)']
EXERCICE : Une primitive de 3x²/(x³ + 1) sur ]−1 ; +∞[ est : OPTIONS : ['3 ln(x³ + 1)', 'ln(x³ + 1)', 'x³/(x³ + 1)']

### Diapo 56 `ln_p2` — Faire apparaître u' ; ln|u| si u < 0
VOIX (fr) : D'abord le coefficient : x sur x carré plus quatre. La dérivée du bas est deux x, et en haut il n'y a que x. Il manque un deux : on multiplie et on divise par deux. Une primitive est, un demi ln de x carré plus quatre. Maintenant regarde le dessin : la courbe de un sur x, des deux côtés. À droite, la courbe rouge de ln x. À gauche, son miroir par rapport à l'axe des ordonnées : la courbe de ln de moins x. Encadré : un sur x a pour primitive, ln de valeur absolue de x, sur chaque intervalle. Et u prime sur u a pour primitive, ln de valeur absolue de u. Exemple : sur moins l'infini, trois, un sur x moins trois, a pour primitive ln de trois moins x.
ÉCRAN : x/(x² + 4) = ½ × 2x/(x² + 4) : il manque un 2 en haut ; primitive ½ ln(x² + 4). | Si u ne s'annule pas sur I : u'/u a pour primitive ln|u|. | 1/x a pour primitive ln|x| sur chaque intervalle : ln x sur ]0 ; +∞[, ln(−x) sur ]−∞ ; 0[. | Sur ]−∞ ; 3[ : 1/(x − 3) → ln|x − 3| = ln(3 − x).

### Diapo 57 `ln_p3` — Vérifier une primitive avec ln
VOIX (fr) : Question classique du national, en deux mille dix-neuf et deux mille vingt-cinq : montrer que H est une primitive de h. On ne cherche rien, on dérive. Au tableau : H de x égale x ln x moins x, et h de x égale ln x, sur zéro, plus l'infini. Première ligne : H est dérivable sur cet intervalle. Deuxième ligne : on dérive. x ln x est un produit : un fois ln x, plus x fois un sur x. Moins la dérivée de x, moins un. Ça fait ln x plus un moins un, donc ln x, c'est h de x. Troisième ligne, en vert : donc H est une primitive de h.
ÉCRAN : On ne cherche pas H : elle est donnée. On la dérive. | H est dérivable sur ]0 ; +∞[ (produit et somme de fonctions dérivables). | H'(x) = 1 × ln x + x × 1/x − 1 = ln x = h(x). | Donc H est une primitive de h sur ]0 ; +∞[ (2019 N, 2025 N).
## IX. Étude de fonction et inégalités, type national

### Diapo 58 `ln_e1` — Prouver ln x ≤ x − 1 par une fonction auxiliaire
VOIX (fr) : Regarde : la courbe de ln, en rouge, et la tangente en un, y égale x moins un, en jaune. La courbe reste sous la droite. Pour le prouver, on mesure l'écart. Le segment vertical, entre la droite et la courbe, c'est g de x, égale x moins un moins ln x. Maintenant le tableau de g, à droite. g prime de x égale un moins un sur x, c'est-à-dire x moins un, sur x. Négative avant un, positive après un. Donc g décroît, puis croît. À toi : que dit ce tableau de g de x ? Question : quelle est la bonne conclusion ?
ÉCRAN : On pose g(x) = x − 1 − ln x sur ]0 ; +∞[ : c'est l'écart entre la droite et la courbe. | g′(x) = 1 − 1/x = (x − 1)/x : négative sur ]0 ; 1], positive sur [1 ; +∞[. | À toi : que conclure du tableau de g ?
QUESTION : Pour montrer que ln x ≤ x − 1 pour tout x > 0, on étudie g(x) = x − 1 − ln x. Quelle conclusion est juste ? OPTIONS : ['g(1) = 0 est le maximum de g, donc g(x) ≤ 0 et ln x ≥ x − 1', 'g est croissante sur ]0 ; +∞[, donc g(x) ≥ 0 et ln x ≤ x − 1', 'g(1) = 0 est le minimum de g, donc g(x) ≥ 0 et ln x ≤ x − 1']
EXERCICE : g(x) = x − 1 − ln x. Que vaut g′(x) ? OPTIONS : ['1 − 1/x', '1 + 1/x', '−1/x']

### Diapo 59 `ln_e2` — La partie I donne le signe de f′
VOIX (fr) : Au national, le problème commence presque toujours par une partie un, avec une fonction g. Pourquoi ? Regarde. En haut, le tableau de signe de g, déjà trouvé : moins avant un, zéro en un, plus après un. Dans la partie deux, on calcule f prime, et on trouve, f prime de x, égale g de x sur x carré. x carré est strictement positif. Donc f prime de x, a le signe de g de x. On recopie la ligne : moins, zéro, plus. Et les flèches de f : elle descend sur l'intervalle zéro, un, puis elle monte après un. La partie un prépare le signe de f prime.
ÉCRAN : La partie I étudie une fonction g et donne son signe. | Dans la partie II : f′(x) = g(x)/x², et x² > 0. | Donc f′(x) a le signe de g(x) : g ≤ 0 sur ]0 ; 1] ⇒ f décroissante ; g ≥ 0 sur [1 ; +∞[ ⇒ f croissante.

### Diapo 60 `ln_enonce_2019n` — National 2019 N : l’énoncé, tel qu’à l’examen
VOIX (fr) : Maintenant, nous allons lire l'énoncé de l'examen national deux mille dix-neuf, la session normale, tel qu'il est à l'examen. Problème, première partie. Soit f la fonction définie sur zéro, plus l’infini, par : f de x égale x plus un demi, moins ln x, plus un demi de ln x au carré. Et C sa courbe, dans un repère orthonormé. Trois a : montrer que x moins un, plus ln x, est négatif avant un, et positif après un. b : montrer que f prime de x, égale x moins un, plus ln x, sur x. c : dresser le tableau de variations de f. Maintenant, comprenons l'exercice, question par question.

### Diapo 61 `ln_e3` — Le tableau de variations, puis le minimum
VOIX (fr) : La fonction du national 2019. Le tableau est prêt, avec le signe de f′ : −, 0 en 1, +. Les flèches : f décroît jusqu'à 1, puis croît. En 1, il y a le minimum. À toi : calcule f de un. Rappelle-toi : ln un égale zéro. Question : combien vaut f de un ?
ÉCRAN : f(x) = x + ½ − ln x + ½(ln x)² sur ]0 ; +∞[ (national 2019). | f′(x) a le signe de x − 1 + ln x : négatif sur ]0 ; 1[, nul en 1, positif après. | À toi : f(1) = ? (ln 1 = 0)
QUESTION : f(x) = x + ½ − ln x + ½(ln x)² : que vaut le minimum f(1) ? OPTIONS : ['3/2', '1/2', '1']

### Diapo 62 `ln_enonce_2019n_p2` — National 2019 N : la suite de l’énoncé
VOIX (fr) : Même problème du national deux mille dix-neuf : la fonction f, avec f de x égale x plus un demi, moins ln x, plus un demi de ln x au carré. Voici d'autres questions de l'énoncé. Un : calculer la limite de f, en zéro à droite, puis interpréter le résultat. Deux a : vérifier que f de x égale, x plus un demi, plus, un demi ln x moins un, fois ln x. b : en déduire la limite en plus l’infini. Maintenant, comprenons l'exercice, question par question.

### Diapo 63 `ln_e3_b` — La limite en 0 à droite et son interprétation (2019, 1)
VOIX (fr) : Revenons au tableau de f : elle décroît jusqu'au minimum trois sur deux, puis elle croît. Il manque les limites aux bornes. D'abord en zéro à droite. Regarde les termes : moins ln x, et un demi ln x au carré. Où vont-ils quand x s'approche de zéro ? Question : que vaut la limite de f de x en zéro à droite, et que veut-elle dire sur la courbe ?
ÉCRAN : f(x) = x + ½ − ln x + ½(ln x)² ; le tableau : minimum f(1) = 3/2. | En 0⁺ : que deviennent −ln x et ½(ln x)² ? | À toi : la limite, puis la phrase d'interprétation.
QUESTION : 2019 N, question 1 : lim_{x→0⁺} f(x) = ? Interprétation géométrique ? OPTIONS : ["−∞ : la droite d'équation x = 0 est asymptote verticale à (C)", "+∞ : la droite d'équation x = 0 est asymptote verticale à (C)", "+∞ : la droite d'équation y = 0 est asymptote horizontale à (C)"]

### Diapo 64 `ln_e3_c` — La limite en +∞ : l'écriture donnée (2019, 2.b)
VOIX (fr) : En zéro, on a trouvé plus l'infini, et la droite x égale zéro asymptote verticale. Maintenant en plus l'infini. Ici on a une forme indéterminée : moins ln x tend vers moins l'infini, et un demi ln x au carré vers plus l'infini. Le sujet donne une autre écriture : f de x égale x plus un demi, plus, un demi ln x moins un, fois ln x. Regarde où va chaque facteur. Question : que vaut la limite de f de x en plus l'infini ?
ÉCRAN : En +∞ : −ln x → −∞ et ½(ln x)² → +∞ : forme indéterminée. | Le sujet donne : f(x) = x + ½ + (½ ln x − 1) ln x. | À toi : lim_{x→+∞} f(x) = ?
QUESTION : 2019 N, question 2.b : f(x) = x + ½ + (½ ln x − 1) ln x. lim_{x→+∞} f(x) = ? OPTIONS : ['−∞', '+∞', 'on ne peut pas conclure : forme indéterminée']

### Diapo 65 `ln_enonce_2019n_p3` — National 2019 N : la suite de l’énoncé
VOIX (fr) : Même problème du national deux mille dix-neuf : la fonction f, et sa courbe C. Voici la suite de l'énoncé. Quatre a : montrer que f seconde de x, égale deux moins ln x, sur x au carré. b : en déduire que C admet un point d’inflexion. Maintenant, comprenons l'exercice, question par question.

### Diapo 66 `ln_e3_d` — Le point d'inflexion (2019, 4.b)
VOIX (fr) : Question quatre du sujet : on nous donne f seconde de x égale deux moins ln x, sur x au carré. Rappel : un point d'inflexion, c'est là où f seconde s'annule en changeant de signe. x au carré est positif, donc f seconde a le signe de deux moins ln x. Deux moins ln x s'annule quand ln x égale deux, c'est-à-dire x égale e au carré. Avant e au carré, positive ; après e au carré, négative. Donc f seconde s'annule en e au carré en changeant de signe. Il reste les coordonnées. À toi : calcule f de e au carré. Rappelle-toi : ln de e au carré égale deux. Question : quelles sont les coordonnées du point d'inflexion ?
ÉCRAN : Donné : f″(x) = (2 − ln x)/x² sur ]0 ; +∞[. | x² > 0 : f″(x) a le signe de 2 − ln x ; il s'annule en e² en changeant de signe. | À toi : les coordonnées du point d'inflexion (ln(e²) = 2).
QUESTION : 2019 N, question 4.b : f″(x) = (2 − ln x)/x². Le point d'inflexion de (C) est : OPTIONS : ['I(2 ; f(2))', 'I(e² ; e² + ½)', 'I(e² ; e² − 3/2)']

### Diapo 67 `ln_enonce_2019n_p4` — National 2019 N : la suite de l’énoncé
VOIX (fr) : Même problème du national deux mille dix-neuf : la fonction f, sa courbe C, et la droite delta, y égale x. Voici la suite de l'énoncé. Cinq a : montrer que f de x moins x, égale un demi, de ln x moins un au carré, et déduire la position de C et de delta. b : construire delta et C, dans le même repère. Maintenant, comprenons l'exercice, question par question.

### Diapo 68 `ln_e4` — Position par rapport à y = x : le signe de f(x) − x
VOIX (fr) : Toujours la fonction de deux mille dix-neuf. Voici le repère, et l'asymptote x égale zéro, en pointillés. On trace la droite delta, y égale x. Pour la position, on étudie le signe de f de x moins x. À toi : calcule f de x moins x, et écris-le comme un carré. Question : que vaut f de x moins x ?
ÉCRAN : Position de (C) par rapport à (Δ) : y = x : on étudie le signe de f(x) − x. | À toi : f(x) − x = ½ − ln x + ½(ln x)², à écrire comme un carré.
QUESTION : f(x) = x + ½ − ln x + ½(ln x)² : f(x) − x est égal à : OPTIONS : ['½(ln x + 1)²', '½(ln x − 1)²', '(ln x − 1)²']

### Diapo 69 `ln_e4_b` — La position par rapport à y = x (2019, 5.a)
VOIX (fr) : On a trouvé : f de x moins x égale un demi, fois ln x moins un, au carré. Maintenant la position de la courbe par rapport à la droite delta. Rappelle-toi : la position vient du signe de f de x moins x. Un carré, quel est toujours son signe ? Et quand est-il nul ? Question : quelle est la position de la courbe par rapport à delta ?
ÉCRAN : f(x) − x = ½(ln x − 1)². | À toi : le signe de f(x) − x donne la position ; quand est-il nul ?
QUESTION : 2019 N, question 5.a : f(x) − x = ½(ln x − 1)². Position de (C) par rapport à (Δ) : y = x ? OPTIONS : ['(C) est au-dessous de (Δ) sur ]0 ; +∞[', "(C) est au-dessus de (Δ) ; elles se coupent au point d'abscisse 1", '(C) est au-dessus de (Δ) ; elles se rencontrent au point A(e ; e)']

### Diapo 70 `ln_e4_c` — Construire (C) pas à pas : ce qu'on place d'abord (2019, 5.b)
VOIX (fr) : Dernière question de cette partie : construire la courbe. On ne trace pas la courbe tout de suite : on place d'abord tout ce qu'on sait. Un : l'asymptote x égale zéro, en pointillés. Deux : la droite delta, y égale x. Trois : le minimum, un, trois sur deux, avec une tangente horizontale, car f prime de un égale zéro. Quatre : le point e, e, où la courbe rencontre delta. À toi : combien vaut f prime de e ? Et quelle est la tangente en ce point ? Question : quelle est la tangente à la courbe au point e, e ?
ÉCRAN : ① l'asymptote x = 0 ; ② (Δ) : y = x ; | ③ le minimum (1 ; 3/2), tangente horizontale ; ④ le point A(e ; e). | À toi : la tangente à (C) en A(e ; e) ?
QUESTION : 2019 N : f′(x) = (x − 1 + ln x)/x et f(e) = e. La tangente à (C) au point A(e ; e) est : OPTIONS : ['la droite horizontale y = e', 'la droite (Δ) : y = x', 'la droite y = x − 1']

### Diapo 71 `ln_e4_d` — Construire (C) : l'inflexion, la branche, puis la courbe (2019, 5.b)
VOIX (fr) : Cinq : delta est la tangente au point e, e. Six : le point d'inflexion I, e au carré, e au carré plus un demi, environ sept virgule quatre, sept virgule neuf. Sept : en plus l'infini, la courbe a une branche parabolique de direction delta, c'est ce que montre le sujet à la question deux d. Maintenant seulement, on trace la courbe : elle descend d'en haut près de l'asymptote, arrive au minimum, remonte au-dessus de delta, la touche en e, e, passe par I, et monte avec delta. Tout ce qu'on a placé, la courbe le respecte.
ÉCRAN : ⑤ (Δ) est tangente à (C) en A(e ; e). | ⑥ I(e² ; e² + ½) ≈ (7,4 ; 7,9) : point d'inflexion. | ⑦ en +∞ : branche parabolique de direction (Δ) ; puis on trace (C).

### Diapo 72 `ln_enonce_2021n` — National 2021 N : l’énoncé, tel qu’à l’examen
VOIX (fr) : Maintenant, nous allons lire l'énoncé de l'examen national deux mille vingt et un, la session normale, tel qu'il est à l'examen. Problème, neuf points. Soit f la fonction définie sur zéro, plus l’infini, par : f de zéro égale zéro, et f de x égale deux x ln x, moins deux x, si x est positif. Et C sa courbe, dans un repère orthonormé. Trois b : calculer f prime de x. c : dresser le tableau de variations de f. Maintenant, comprenons l'exercice, question par question.

### Diapo 73 `ln_e5` — Un problème du national : f et sa dérivée
VOIX (fr) : Un problème du national 2021, pas à pas. f(x) = 2x ln x − 2x et f(0) = 0. Le repère. D'abord le point O : f est continue à droite en 0 et la courbe part avec une demi-tangente verticale. L'étape suivante est à toi : la dérivée ; attention, 2x ln x est un produit. Question : calcule f′(x).
ÉCRAN : f(x) = 2x ln x − 2x sur ]0 ; +∞[ et f(0) = 0 (national 2021). | En O : continuité à droite, demi-tangente verticale. | Puis la dérivée : 2x ln x est un produit.
QUESTION : f(x) = 2x ln x − 2x sur ]0 ; +∞[. Que vaut f′(x) ? OPTIONS : ['2 ln x − 2', '2 ln x', '2/x − 2']

### Diapo 74 `ln_e5_b` — Le signe de f′ et les variations (2021, 3.c)
VOIX (fr) : La correction : la dérivée de deux x ln x, c'est deux ln x plus deux x fois un sur x, donc deux ln x plus deux. Moins deux : il reste f prime de x égale deux ln x. Maintenant le tableau de variations. Le signe de f prime, c'est le signe de ln x, et on le connaît par la courbe de ln. À toi : comment varie f ? Question : quelles sont les variations de f ?
ÉCRAN : f′(x) = (2x ln x)′ − 2 = 2 ln x + 2x × 1/x − 2 = 2 ln x. | f′(x) a le signe de ln x. | À toi : les variations de f sur ]0 ; +∞[.
QUESTION : 2021 N, question 3.c : f′(x) = 2 ln x sur ]0 ; +∞[. Alors : OPTIONS : ['f est croissante sur ]0 ; 1] et décroissante sur [1 ; +∞[ ; maximum f(1) = −2', 'f est décroissante sur ]0 ; 1] et croissante sur [1 ; +∞[ ; minimum f(1) = −2', "f est croissante sur ]0 ; +∞[ car 2 ln x > 0 ; pas d'extremum"]

### Diapo 75 `ln_enonce_2021n_p2` — National 2021 N : la suite de l’énoncé
VOIX (fr) : Même problème du national deux mille vingt et un : la fonction f, avec f de x égale deux x ln x, moins deux x. Voici la suite de l'énoncé. Quatre a : résoudre les équations, f de x égale zéro, et f de x égale x. Maintenant, comprenons cette question.

### Diapo 76 `ln_e5_q` — f(x) = 0 et f(x) = x : des équations avec ln (2021, 4.a)
VOIX (fr) : Question quatre a : résoudre f de x égale zéro, et f de x égale x. La première, on l'a résolue dans les équations : deux x, fois ln x moins un, égale zéro, donc x égale e. Maintenant f de x égale x, avec x strictement positif. On met tout du même côté : deux x ln x moins trois x égale zéro. On factorise par x : x, fois deux ln x moins trois, égale zéro. À toi : termine, et fais attention au domaine. Question : quelles sont les solutions de f de x égale x ?
ÉCRAN : f(x) = 0 ⇔ 2x(ln x − 1) = 0 ⇔ x = e (déjà résolue). | f(x) = x ⇔ 2x ln x − 3x = 0 ⇔ x(2 ln x − 3) = 0. | À toi : termine, sans oublier x ∈ ]0 ; +∞[.
QUESTION : 2021 N, question 4.a : résous f(x) = x dans ]0 ; +∞[. OPTIONS : ['S = {0 ; e^(3/2)}', 'S = {e^(2/3)}', 'S = {e^(3/2)}']

### Diapo 77 `ln_enonce_2021n_p3` — National 2021 N : la suite de l’énoncé
VOIX (fr) : Même problème du national deux mille vingt et un : la fonction f, et sa courbe C. Voici la suite de l'énoncé. Quatre b : construire la courbe C, on prend e puissance trois demis, égale quatre virgule cinq. Six a : déterminer le minimum de f. b : en déduire que ln x, est plus grand que, x moins un, sur x. Maintenant, comprenons l'exercice, question par question.

### Diapo 78 `ln_e5_c` — Construire (C) pas à pas, puis l'inégalité (2021, 4.b et 6)
VOIX (fr) : Maintenant construire la courbe, pas à pas. Un : le point O, avec une demi-tangente verticale. Deux : le minimum, un, moins deux, avec une tangente horizontale. Trois : f de e égale zéro, la courbe coupe l'axe en e. Quatre : la droite y égale x, et le point e puissance trois sur deux, environ quatre virgule cinq. Cinq : f de x sur x égale deux ln x moins deux, qui tend vers plus l'infini : branche parabolique de direction l'axe des ordonnées. Maintenant seulement la courbe : elle part de O, descend jusqu'au minimum, remonte, coupe l'axe en e, et monte de plus en plus vite. Dernière question : moins deux est le minimum de f. À toi : comment en tirer une inégalité avec ln x ? Question : quelle est la bonne inégalité ?
ÉCRAN : ① O : demi-tangente verticale ; ② minimum (1 ; −2) ; ③ (e ; 0) ; | ④ (C) coupe y = x en e^(3/2) ≈ 4,5 ; ⑤ branche parabolique de direction (Oy). | À toi : f(1) = −2 est le minimum de f ; quelle inégalité avec ln x en déduire ?
QUESTION : Avec f′(x) = 2 ln x et f(1) = −2 minimum, on déduit pour x > 0 : OPTIONS : ['ln x ≥ (x − 1)/x', 'ln x ≤ (x − 1)/x', 'ln x ≥ x − 1']

### Diapo 79 `ln_e6` — Étudier ln(u(x)) : le domaine et les limites aux bornes
VOIX (fr) : Maintenant une nouvelle fonction : f de x égale ln de x plus deux, sur un moins x. D'abord le domaine : le quotient doit être strictement positif. x plus deux s'annule en moins deux, et un moins x s'annule en un. Le tableau de signe donne : le quotient est positif seulement entre moins deux et un. Donc D f égale l'intervalle ouvert moins deux, un. Maintenant les limites aux bornes. Quand x tend vers moins deux à droite, x plus deux tend vers zéro en restant positif, et un moins x tend vers trois. Donc le quotient tend vers zéro à droite, et f de x tend vers moins l'infini. Quand x tend vers un à gauche, un moins x tend vers zéro en restant positif, et x plus deux tend vers trois. Donc le quotient tend vers plus l'infini, et f de x tend vers plus l'infini. Interprétation : la courbe admet deux asymptotes verticales : la droite x égale moins deux, et la droite x égale un. Autrement dit : ln plonge quand ce qui est dedans tend vers zéro, et monte quand ce qui est dedans devient très grand.
ÉCRAN : x ∈ D_f ⇔ (x + 2)/(1 − x) > 0 et 1 − x ≠ 0. | x + 2 s'annule en −2 et 1 − x en 1 ; tableau de signe : le quotient est > 0 seulement sur ]−2 ; 1[, donc D_f = ]−2 ; 1[. | En −2⁺ : x + 2 → 0⁺ et 1 − x → 3, donc (x + 2)/(1 − x) → 0⁺ et lim_{x→−2⁺} f(x) = −∞. | En 1⁻ : x + 2 → 3 et 1 − x → 0⁺, donc (x + 2)/(1 − x) → +∞ et lim_{x→1⁻} f(x) = +∞. | Les droites d'équations x = −2 et x = 1 sont asymptotes verticales à (C_f).

### Diapo 80 `ln_e6_b` — Étudier ln(u(x)) : f′ = u′/u, puis le tableau
VOIX (fr) : Maintenant la dérivée. u de x égale x plus deux sur un moins x, dérivable et strictement positive sur D f, donc f prime égale u prime sur u. La dérivée d'un quotient : un fois un moins x, moins x plus deux fois moins un, sur un moins x au carré. On simplifie : u prime de x égale trois sur un moins x au carré. On divise par u : f prime de x égale trois, sur un moins x, fois x plus deux. Sur D f, un moins x est positif, et x plus deux est positif, donc f prime est positive. Donc f est strictement croissante sur moins deux, un. Le tableau de variations : f monte de moins l'infini jusqu'à plus l'infini, sans s'arrêter.
ÉCRAN : u(x) = (x + 2)/(1 − x) est dérivable et strictement positive sur ]−2 ; 1[, donc f = ln u est dérivable sur ]−2 ; 1[ et f′ = u′/u. | u′(x) = (1 × (1 − x) − (x + 2) × (−1))/(1 − x)² = (1 − x + x + 2)/(1 − x)² = 3/(1 − x)². | f′(x) = u′(x)/u(x) = 3/(1 − x)² × (1 − x)/(x + 2) = 3/((1 − x)(x + 2)). | Sur ]−2 ; 1[ : 1 − x > 0 et x + 2 > 0, donc f′(x) > 0 : f est strictement croissante sur ]−2 ; 1[. | Tableau : f croît de −∞ (en −2⁺) à +∞ (en 1⁻).

### Diapo 81 `ln_e6_c` — Étudier ln(u(x)) : la concavité par le signe de f″
VOIX (fr) : Maintenant la concavité. Rappel du chapitre de la dérivation : si f seconde est négative sur I, la courbe est concave. Si f seconde est positive, la courbe est convexe. Et si f seconde s'annule en changeant de signe en a, on a un point d'inflexion. Ici on écrit f prime de x égale trois sur v de x, avec v de x égale moins x carré moins x plus deux, et v prime de x égale moins deux x moins un. La dérivée de un sur v est moins v prime sur v carré. On obtient f seconde de x égale trois fois deux x plus un, sur un moins x au carré, fois x plus deux au carré. Le dénominateur est positif, donc f seconde a le signe de deux x plus un, qui s'annule en moins un demi. Avant moins un demi, f seconde est négative : la courbe est concave. Après moins un demi, positive : la courbe est convexe. Et f de moins un demi égale ln un, c'est-à-dire zéro. Donc le point I, moins un demi, zéro, est un point d'inflexion. Question : la courbe de ln elle-même, sur zéro, plus l'infini, est-elle concave ou convexe ?
ÉCRAN : Rappel : f″ < 0 sur I ⇒ (C_f) concave sur I ; f″ > 0 sur I ⇒ (C_f) convexe sur I ; f″ s'annule en a en changeant de signe ⇒ point d'inflexion d'abscisse a. | f′(x) = 3/v(x) avec v(x) = (1 − x)(x + 2) = −x² − x + 2 et v′(x) = −2x − 1. | (1/v)′ = −v′/v², donc f″(x) = −3(−2x − 1)/v(x)² = 3(2x + 1)/((1 − x)²(x + 2)²). | Le dénominateur est > 0 : f″(x) a le signe de 2x + 1, qui s'annule en −½. | f″ < 0 sur ]−2 ; −½[ : (C_f) concave ; f″ > 0 sur ]−½ ; 1[ : (C_f) convexe. | f″ s'annule en −½ en changeant de signe et f(−½) = ln((3/2)/(3/2)) = ln 1 = 0 : I(−½ ; 0) est un point d'inflexion de (C_f).
QUESTION : La courbe de ln, sur ]0 ; +∞[, est : OPTIONS : ['convexe sur ]0 ; +∞[', 'concave sur ]0 ; +∞[', "concave, puis convexe : point d'inflexion d'abscisse 1"]
## X. Le logarithme décimal

### Diapo 82 `ln_g1` — Le logarithme décimal : log 10 = 1
VOIX (fr) : Regarde deux courbes : ln en rouge, et une autre, plus aplatie. C'est log, le logarithme décimal. On a divisé ln par ln dix. Les deux passent par un, zéro. Et log passe par le point dix, un : log dix égale un. Maintenant la règle graduée. En haut, un, dix, cent, mille. En bas, zéro, un, deux, trois. Chaque fois qu'on multiplie par dix, le log monte de un. log compte les zéros. La formule, encadrée : log x égale ln x sur ln dix. Et log de dix puissance n égale n. Les règles de ln restent vraies.
ÉCRAN : log x = ln x/ln 10 pour x > 0. | log 1 = 0 ; log 10 = 1 ; log(10ⁿ) = n. | Mêmes règles que ln : log(ab) = log a + log b. | Multiplier x par 10, c'est ajouter 1 au log.

### Diapo 83 `ln_g2` — 10ˣ = a ⇔ x = log a ; le pH
VOIX (fr) : Au tableau : dix puissance x égale cinq. Quel est l'exposant ? Pour trouver l'exposant, on prend le log. x égale log cinq, environ zéro virgule sept. Même chose pour l'inéquation, car log est strictement croissante : dix puissance x supérieur ou égal à cinq, donc x supérieur ou égal à log cinq. Maintenant la chimie. Regarde la règle : dix puissance moins un, moins deux, moins trois, moins quatre. En face, pH un, deux, trois, quatre. Le pH, c'est le log, changé de signe. La formule : pH égale moins log de la concentration en ions oxonium. Donc si le pH vaut trois, la concentration vaut dix puissance moins trois mole par litre.
ÉCRAN : 10ˣ = a ⇔ x = log a (a > 0). | Exemple : 10ˣ = 5 ⇔ x = log 5 ≈ 0,70. | Pour a > 0 : 10ˣ ≤ a ⇔ x ≤ log a et 10ˣ ≥ a ⇔ x ≥ log a, car log est strictement croissante. Exemple : 10ˣ ≥ 5 ⇔ x ≥ log 5. | En chimie : pH = −log[H₃O⁺] et [H₃O⁺] = 10^(−pH). | pH = 3 ⇒ [H₃O⁺] = 10⁻³ mol/L.
## XI. Bilan et carte du chapitre

### Diapo 84 `ln_b1` — Ce qu'il faut retenir
VOIX (fr) : Faisons le bilan sur une seule fiche, bloc par bloc, et écris avec moi. Un : la définition. ln est la primitive de un sur x, sur zéro, plus l'infini, qui s'annule en un. ln un égale zéro, la dérivée de ln x est un sur x, et ln e égale un. Attention, ln x est négatif entre zéro et un. Deux : l'ensemble de définition. Ce qu'il y a dans le ln, doit être strictement positif. Les conditions se relient par et. Trois : les règles. ln de a fois b, égale ln a plus ln b. Mais jamais ln d'une somme. Quatre : les équations. D'abord le domaine, puis on enlève les ln, puis on trie. Cinq : les limites. x l'emporte sur ln x. Six : la dérivée. La dérivée de ln u est u prime sur u. Sept : les primitives. Le haut est la dérivée du bas, la primitive est ln du bas. Huit : l'étude. Le signe de f prime vient de g, et ln x est inférieur ou égal, à x moins un. Neuf : le logarithme décimal. log x égale ln x sur ln dix. La deuxième page est la tienne : ce qu'il te reste à retravailler.
ÉCRAN : 1. Définition, courbe : ln est la primitive de x ↦ 1/x sur ]0 ; +∞[ qui s'annule en 1 ; ln 1 = 0 et (ln x)' = 1/x ; ln e = 1 (e ≈ 2,718) ; tangente en 1 : y = x − 1. ⚠ ln x < 0 sur ]0 ; 1[. ln : ]0 ; +∞[ → ℝ est continue et strictement croissante ; e est l'unique solution de ln x = 1. | 2. Ensemble de définition : x ∈ D_f ⇔ u(x) > 0 ; les conditions se relient par « et ». ⚠ ln|u| : u ≠ 0. | 3. Règles : ln(ab) = ln a + ln b ; ln(a/b) = ln a − ln b ; ln(aⁿ) = n ln a ; ln √a = ½ ln a ; ln(eʳ) = r. ⚠ ln(a + b) ≠ ln a + ln b. | 4. Équations : ln a = ln b ⇔ a = b ; ln a < ln b ⇔ a < b ; ln x = r ⇔ x = eʳ. ⚠ D'abord le domaine, puis trier les solutions. | 5. Limites : lim_{x→+∞} ln x = +∞ ; lim_{x→0⁺} ln x = −∞ ; lim_{x→+∞} (ln x)/x = 0 ; lim_{x→0⁺} x ln x = 0 ; lim_{x→0} ln(1 + x)/x = 1. Pour n ∈ ℕ* : lim_{x→+∞} (ln x)/xⁿ = 0 et lim_{x→0⁺} xⁿ ln x = 0. Si lim u(x) = 0⁺, alors lim ln(u(x)) = −∞ (asymptote verticale). | 6. Dérivée : (ln u)' = u'/u (u > 0 sur I). ⚠ ((ln x)²)' = 2 ln x/x. (ln|u|)' = u'/u (u ≠ 0 sur I). | 7. Primitives : u'/u → ln|u| (u ne s'annule pas sur I) ; 1/x → ln x sur ]0 ; +∞[. | 8. Étude : le signe de f' vient de g ; ln x ≤ x − 1 pour tout x > 0. Concavité : signe de f″ ; (ln x)″ = −1/x² < 0, la courbe de ln est concave. | 9. Logarithme décimal : log x = ln x/ln 10 ; 10ˣ = a ⇔ x = log a (a > 0). 10ˣ ≤ a ⇔ x ≤ log a (a > 0). | Page 2, ta page : ce qu'il te reste à retravailler, d'après tes réponses du cours.

### Diapo 85 `ln_b2` — La carte du chapitre
VOIX (fr) : Dessinons la carte de tout le chapitre, en une seule image. Au centre : ln, la primitive de un sur x qui s'annule en un. Première branche : la courbe, ln un égale zéro, ln e égale un, et elle monte toujours. Deuxième branche : le domaine, u de x strictement positif. Troisième branche : les règles, ln d'un produit égale la somme des ln. Quatrième branche : les équations, ln a égale ln b équivaut à a égale b. Cinquième branche : les limites, ln x sur x tend vers zéro. Sixième branche : la dérivée, u prime sur u. Septième branche : les primitives, ln de valeur absolue de u. Huitième branche : l'étude, ln x inférieur ou égal à x moins un. Et la dernière branche : le logarithme décimal. Voilà la carte du chapitre. Les branches entourées en rouge, ce sont celles qu'on va reprendre ensemble. Question : par quel point passe toujours la courbe de ln ?
ÉCRAN : Au centre : ln, la primitive de 1/x sur ]0 ; +∞[ qui s'annule en 1. | La courbe : ln 1 = 0, ln e = 1, croissante. Le domaine : u(x) > 0. | Les règles : ln(ab) = ln a + ln b. Les équations : ln a = ln b ⇔ a = b. | Les limites : (ln x)/x → 0. La dérivée : (ln u)' = u'/u. Les primitives : u'/u → ln|u| (u ≠ 0 sur I). | L'étude : ln x ≤ x − 1. Le logarithme décimal : log x = ln x/ln 10. | Plus tard : la fonction exponentielle, au chapitre suivant.
QUESTION : Par quel point passe toujours la courbe de ln ? OPTIONS : ['(0 ; 1)', '(e ; 0)', '(1 ; 0)']

### Diapo 86 `ln_fermeture_cours` — Ce qu'il faut retenir, et comment réviser
VOIX (fr) : Nous arrivons à la fin du cours : Fonctions logarithmiques. Que faut-il retenir ? Trois idées. Première : ln de a fois b égale ln a plus ln b. Deuxième : ln de u de x existe seulement si u de x est strictement positif. Troisième : la dérivée de ln u est u prime sur u. Maintenant quelques conseils pour réviser. Relis ton cahier, et refais seul les exercices du national. Quand tu réponds, écris chaque étape, et chaque résultat avec sa justification, car chaque étape a ses points. Le jour de l'examen, partage ton temps, et commence par la question qui te paraît facile. La veille, dors bien. Écris ces conseils dans ton cahier. Tu as bien travaillé, bon courage ! Le prochain cours : Nombres complexes. On s'y retrouve !
ÉCRAN : Retenir : ln(ab) = ln a + ln b (a, b > 0) · u(x) > 0 · (ln u)′ = u′/u | Réviser : relire le cahier, refaire les exercices du national | Rédiger : chaque étape, et sa justification (car…) | Jour J : gérer son temps · bien dormir la veille

## Questions de bloc (posées après la dernière diapo du bloc)
- après diapo 4 `ln_s0_b1` RETROUVER : Cahier fermé : écris la définition d'une primitive.
- après diapo 4 `ln_s0_b1` EXERCICE : Une primitive de x⁵ sur ℝ est : OPTIONS : ['5x⁴', 'x⁶/6', 'x⁶/5']
- après diapo 6 `ln_s1_b1` RETROUVER : Cahier fermé : pourquoi la règle xⁿ → xⁿ⁺¹/(n + 1) ne donne pas de primitive de 1/x ?
- après diapo 6 `ln_s1_b1` EXERCICE : Vrai ou faux ? OPTIONS : None
- après diapo 10 `ln_s1_b2` RETROUVER : Cahier fermé : écris ln 1 et la dérivée de ln.
- après diapo 10 `ln_s1_b2` EXERCICE : La pente de la tangente à la courbe de ln au point d'abscisse 4 est : OPTIONS : ['0,25', '4', 'ln 4']
- après diapo 13 `ln_s1_b3` RETROUVER : Cahier fermé : écris la valeur de ln e et une valeur approchée de e.
- après diapo 13 `ln_s1_b3` EXERCICE : ln(2x) = ln 6 a pour solution : OPTIONS : ['x = 6', 'x = 3', 'x = ln 3']
- après diapo 17 `ln_s0_b2` RETROUVER : Cahier fermé : résous −2x > 4.
- après diapo 17 `ln_s0_b2` EXERCICE : f(x) = ln((x − 1)/(x + 2)) : quel est D_f ? OPTIONS : [']−2 ; 1[', ']−∞ ; −2[ ∪ ]1 ; +∞[', ']−∞ ; −2[ ∪ [1 ; +∞[']
- après diapo 20 `ln_s2_b1` RETROUVER : Cahier fermé : écris la condition d'existence de ln(u(x)).
- après diapo 20 `ln_s2_b1` EXERCICE : f(x) = ln|x + 1| : quel est D_f ? OPTIONS : [']−∞ ; −1[ ∪ ]−1 ; +∞[', ']−1 ; +∞[', ']−∞ ; 1[ ∪ ]1 ; +∞[']
- après diapo 23 `ln_s2_b2` RETROUVER : Cahier fermé : écris la règle du logarithme d'un produit.
- après diapo 23 `ln_s2_b2` EXERCICE : Pour x > 0, ln(5x) − ln x = ? OPTIONS : ['ln 5', '5', 'ln 4x']
- après diapo 26 `ln_s2_b2b` RETROUVER : Cahier fermé : que valent ln(aⁿ) et ln √a ?
- après diapo 26 `ln_s2_b2b` EXERCICE : Simplifie C = ln 8 + ln 9 − ln 6. OPTIONS : ['2 ln 2 + ln 3', '3 ln 2 + ln 3', 'ln 11']
- après diapo 29 `ln_s2_b3` RETROUVER : Cahier fermé : écris ln(x²) pour x ≠ 0.
- après diapo 29 `ln_s2_b3` EXERCICE : D = 2 ln 6 − ln 4 : quelle est la bonne valeur ? OPTIONS : ['2 ln 3', 'ln 3', '2 ln 2 + 2 ln 3']
- après diapo 33 `ln_s2_b4` RETROUVER : Cahier fermé : que vaut ln(eʳ) ?
- après diapo 33 `ln_s2_b4` EXERCICE : Résous ln(x + 3) = ln(2x − 1). OPTIONS : ['S = {4}', 'S = {−4}', 'Pas de solution']
- après diapo 38 `ln_s3_b1` RETROUVER : Cahier fermé : écris les deux règles qui permettent d'enlever les ln.
- après diapo 38 `ln_s3_b1` EXERCICE : Résous ln x = −1. OPTIONS : ['x = −e', 'x = 1/e', 'x = e']
- après diapo 43 `ln_s3_b2` RETROUVER : Cahier fermé : écris les limites de ln x en +∞ et en 0 à droite.
- après diapo 43 `ln_s3_b2` EXERCICE : Résous : ln x + ln y = 1 et ln x − ln y = 1. OPTIONS : ['(x ; y) = (e ; 1)', '(x ; y) = (1 ; e)', '(x ; y) = (e ; 0)']
- après diapo 47 `ln_s3_b3` RETROUVER : Cahier fermé : écris les deux croissances comparées de base.
- après diapo 47 `ln_s3_b3` EXERCICE : lim_{x→+∞} (ln x + 1)/x = ? OPTIONS : ['1', '+∞', '0']
- après diapo 51 `ln_s4_b1` RETROUVER : Cahier fermé : écris la dérivée de ln u.
- après diapo 51 `ln_s4_b1` EXERCICE : Pour calculer lim_{x→+∞} (ln x)/√x, on pose t = √x. On obtient : OPTIONS : ['(ln t)/t', '2(ln t)/t', '(ln t)/t²']
- après diapo 55 `ln_s4_b2` RETROUVER : Cahier fermé : écris une primitive de u'/u.
- après diapo 55 `ln_s4_b2` EXERCICE : Sur ]0 ; +∞[, (x ln x)' = ? OPTIONS : ['ln x + 1', '1 × 1/x', '1 × ln x']
- après diapo 58 `ln_s4_b3` RETROUVER : Cahier fermé : écris l'inégalité entre ln x et x − 1.
- après diapo 58 `ln_s4_b3` EXERCICE : Une primitive de f(x) = x/(x² + 4) sur ℝ est : OPTIONS : ['ln(x² + 4)', '½ ln(x² + 4)', '2 ln(x² + 4)']
- après diapo 64 `ln_s5_b1` RETROUVER : Cahier fermé : écris l'équation de la tangente à la courbe de ln au point d'abscisse 1.
- après diapo 64 `ln_s5_b1` EXERCICE : f′(x) = g(x)/x et g(x) > 0 sur ]0 ; +∞[. Alors f est sur ]0 ; +∞[ : OPTIONS : ['strictement croissante', 'strictement décroissante', 'on ne peut pas savoir']
- après diapo 69 `ln_s5_b1e` RETROUVER : Cahier fermé : comment trouve-t-on la position de (C) par rapport à la droite (Δ) : y = x ?
- après diapo 69 `ln_s5_b1e` EXERCICE : f(x) − x = (ln x)² sur ]0 ; +∞[. Par rapport à (Δ) : y = x, la courbe (C) est : OPTIONS : ['au-dessus, et elles se touchent en x = 1', 'au-dessous, et elles se touchent en x = 1', 'au-dessus, sans aucun point commun avec (Δ)']
- après diapo 71 `ln_s5_b1d` RETROUVER : Cahier fermé : que place-t-on dans le repère avant de tracer la courbe ?
- après diapo 71 `ln_s5_b1d` EXERCICE : f′(2) = 0 et f(2) = 3. La tangente à (C) au point d'abscisse 2 a pour équation : OPTIONS : ['y = 3', 'x = 2', 'y = 3x − 6']
- après diapo 78 `ln_s5_b1b` RETROUVER : Cahier fermé : pour f(x) = 2x ln x − 2x, écris f′(x).
- après diapo 78 `ln_s5_b1b` EXERCICE : Avec f′(x) = 2 ln x et f(1) = −2 minimum, on déduit pour x > 0 : OPTIONS : ['ln x ≥ (x − 1)/x', 'ln x ≤ (x − 1)/x', 'ln x ≥ x − 1']
- après diapo 81 `ln_s5_b1c` RETROUVER : Cahier fermé : comment lit-on la concavité de (C_f) avec f″ ?
- après diapo 81 `ln_s5_b1c` EXERCICE : g(x) = ln((x + 1)/(3 − x)) : quel est D_g ? OPTIONS : [']−∞ ; −1[ ∪ ]3 ; +∞[', ']−1 ; +∞[', ']−1 ; 3[']
- après diapo 85 `ln_s5_b2` RETROUVER : Cahier fermé : écris log x en fonction de ln.
- après diapo 85 `ln_s5_b2` EXERCICE : log 20 − log 2 = ? OPTIONS : ['log 18', '1', '10']
