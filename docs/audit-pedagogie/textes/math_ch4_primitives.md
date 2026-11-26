# math_ch4_primitives — Fonctions primitives

## Ouverture — dériver, puis revenir ; la pente

### Diapo 1 `pr_ouverture_cours` — Fonctions primitives
VOIX (fr) : Bienvenue dans un nouveau cours : Fonctions primitives. Dans ce cours, nous allons apprendre ce qu'est une primitive, le tableau des primitives usuelles, et comment reconnaître les formes comme u prime u puissance n. Les primitives reviennent au national, dans l'étude des fonctions puis dans le calcul intégral : c'est l'analyse, cinquante-cinq pour cent de la note. Comment allons-nous travailler ? Tu écoutes bien, tu réponds aux questions au tableau, et quand le cours s'arrête, tu écris dans ton cahier. Allons-y !
ÉCRAN : On apprend : Primitive, tableau des primitives usuelles, formes composées | Au bac : l'analyse = 55 % de la note | Écouter · répondre au tableau · écrire dans le cahier

### Diapo 2 `pr_o1` — La carte du chapitre : dériver, puis revenir
VOIX (fr) : Regarde le centre : F à gauche, f à droite. La flèche rouge du haut, c'est ce que tu sais déjà : dériver, de F vers f. La flèche verte du bas va dans l'autre sens : primitiver, revenir de f vers F. Autour, les questions du chapitre. La première bulle : vérifier que F est une primitive de f. Elle est tombée dans onze sujets nationaux sur vingt. Ensuite, toutes les primitives : F de x plus k. Puis la primitive qui passe par un point. Puis le tableau des primitives usuelles, et les formes avec u prime. Et en bas, en jaune : au semestre deux, l'intégrale, dans vingt sujets sur vingt, et elle se calcule avec une primitive.
ÉCRAN : Dériver : de F vers f. Primitiver : revenir de f vers F. | Vérifier que F est une primitive de f : 11 sujets nationaux sur 20. | Toutes les primitives : F(x) + k ; la primitive qui vérifie F(x₀) = y₀. | Le tableau des primitives usuelles et les formes u′uⁿ, u′/u², u′/√u, u′cos u… | Au semestre 2, l'intégrale (20 sujets sur 20) se calcule avec une primitive.
EXERCICE : Ce que tu sais déjà sur la dérivée : vrai ou faux ? OPTIONS : None

### Diapo 3 `pr_z1_pente` — Rappel : la dérivée, c'est la pente
VOIX (fr) : Avant de commencer, revenons à une notion de l'an dernier : la dérivée. Regarde la courbe de f de x égale x carré. Un point se déplace sur la courbe, avec sa tangente. La dérivée, c'est la pente de cette tangente. En x égale un, la courbe monte, la pente est positive : f prime de un égale deux. En x égale moins un, la courbe descend, la pente est négative : f prime de moins un égale moins deux. Voyons-le autrement : comme une route. Si la route monte, la pente est positive ; si elle descend, négative ; si elle est plate, la pente est zéro. Regarde cette droite plate : g de x égale cinq. Sa pente est zéro : c'est la dérivée d'une constante. Je relis : la dérivée d'une constante est zéro.
ÉCRAN : f′(a) est la pente de la tangente à la courbe de f au point d'abscisse a. | La courbe monte : pente positive ; elle descend : pente négative. | Une constante est une droite plate : (k)′ = 0.
## I. Définition et vérification (chaque rappel juste avant son usage)

### Diapo 4 `pr_d1` — La marche arrière : de la dérivée vers la fonction
VOIX (fr) : Tu sais déjà avancer. En haut : x carré, la flèche rouge, on dérive, et on obtient deux x. Maintenant la marche arrière, comme au permis : on sait avancer, on apprend à reculer. En bas, on part de deux x, à droite, et la flèche verte repart vers la gauche. À gauche, un point d'interrogation : quelle fonction, une fois dérivée, donne deux x ? C'est x au carré, car la dérivée de x au carré est deux x.
ÉCRAN : Aller : x² → 2x (on dérive). | Retour : 2x → ? On cherche une fonction dont la dérivée est 2x. | Comme pour une voiture : on sait avancer, on apprend la marche arrière.

### Diapo 5 `pr_d2` — Définition : une primitive de f sur un intervalle
VOIX (fr) : Le point d'interrogation devient x carré, et on vérifie à côté : la dérivée de x carré est deux x, coche verte. Donnons un nom. Sur la flèche verte s'écrit le mot primitive. Sous la gauche, F majuscule. Sous la droite, f minuscule. Trois questions construisent la définition. Que fait-on à F ? On la dérive. Que doit-on trouver ? f. Pour quels x ? Pour tous les x d'un intervalle I. Voici la définition : F est une primitive de f sur I, si F est dérivable sur I, et F prime de x égale f de x, pour tout x de l'intervalle I. Voyons-la autrement : F est la route, et f est la pente de la route en chaque point. Si on connaît la pente partout, on peut redessiner la route : c'est primitiver. Attention, en rouge : on n'écrit jamais que f est égale à F, on dit F prime égale f. Je relis : F est une primitive de f sur I, si F prime de x égale f de x, pour tout x de I.
ÉCRAN : On dérive F ; on doit trouver f ; pour tous les x d'un intervalle I. | F est une primitive de f sur I si F est dérivable sur I et F′(x) = f(x) pour tout x ∈ I. | On écrit F′ = f, jamais « f égale F » : F et f sont deux fonctions différentes.

### Diapo 6 `pr_z2_puissances` — Rappel : dériver une puissance
VOIX (fr) : Maintenant, la dérivée d'une puissance. Regarde x cube. Le trois du haut descend devant, puis l'exposant baisse de un : trois devient deux. Donc la dérivée de x cube est trois x carré. De même, la dérivée de x carré est deux x, et celle de x puissance quatre est quatre x cube. La règle : la dérivée de x puissance n est n x puissance n moins un. Voyons-le autrement : marche par marche. À chaque dérivée, l'exposant descend d'une marche : x puissance quatre, puis quatre x cube, puis douze x carré. Je relis : la dérivée de x puissance n est n x puissance n moins un. Question : quelle est la dérivée de x puissance cinq ?
ÉCRAN : (x³)′ = 3x² : l'exposant descend devant, puis il baisse de 1. | (xⁿ)′ = n xⁿ⁻¹. | À chaque dérivée, l'exposant descend d'une marche.
QUESTION : Quelle est la dérivée de x⁵ ? OPTIONS : ['x⁶/6', '5x⁴', '5x⁵']

### Diapo 7 `pr_z3_ecrire` — Rappel : écrire en puissance
VOIX (fr) : Pour primitiver des fractions et des racines, il faudra les écrire en puissance. Un sur x, c'est x puissance moins un. Regarde un sur x carré : x carré monte du bas vers le haut, et l'exposant prend un moins. Donc un sur x carré, c'est x puissance moins deux. La règle : ce qui était en bas monte en haut avec un exposant négatif. Maintenant la racine : racine de x, c'est x puissance un demi. Pourquoi un demi ? Voyons-le autrement : racine de x fois racine de x donne x. Et x puissance un demi fois x puissance un demi donne x puissance un demi plus un demi, soit x puissance un, soit x. Deux moitiés font un. De même, racine cubique de x, c'est x puissance un tiers. Cette écriture permet de dériver avec la règle des puissances : la dérivée de un sur x est moins un sur x carré, et la dérivée de racine de x est un sur deux racine de x. Je relis : racine de x égale x puissance un demi.
ÉCRAN : 1/x = x⁻¹ ; 1/x² = x⁻² : ce qui est en bas monte en haut avec un exposant négatif. | √x = x^(1/2), car x^(1/2) × x^(1/2) = x ; ∛x = x^(1/3). | La règle des puissances redonne (1/x)′ = −1/x² et (√x)′ = 1/(2√x).

### Diapo 8 `pr_d3` — Vérifier une primitive : on dérive
VOIX (fr) : Au national, on te donne F, et on te demande de montrer qu'elle est une primitive de f. On ne cherche rien : on dérive. Au tableau, F de x égale x cube moins un sur x plus un, et f de x égale trois x carré plus un sur x carré, sur l'intervalle zéro, plus l'infini. Première ligne : F est dérivable sur cet intervalle, somme de fonctions dérivables. Deuxième ligne : on dérive. Trois x carré, moins la dérivée de un sur x, plus zéro. Et on arrive à trois x carré plus un sur x carré, c'est f de x. Troisième ligne, la conclusion : donc F est une primitive de f.
ÉCRAN : Ligne 1 : F est dérivable sur I (somme, produit… de fonctions dérivables). | Ligne 2 : pour tout x de I, F′(x) = … = f(x). | Ligne 3 : donc F est une primitive de f sur I. | On ne cherche pas F : elle est donnée. On la dérive.

### Diapo 9 `pr_z5_cos_sin` — Rappel : cos, sin et leurs dérivées
VOIX (fr) : Une autre notion des années d'avant : cosinus et sinus. Regarde le cercle, de rayon un. Le point M tourne d'un angle x. Cosinus x est l'abscisse de M, en bleu. Sinus x est l'ordonnée de M, en jaune. Et maintenant les dérivées : la dérivée de sinus x est cosinus x. Et la dérivée de cosinus x est moins sinus x, attention au moins. Voyons-le autrement, sur la courbe de sinus. En zéro, la courbe monte, la pente vaut un, et cosinus de zéro vaut aussi un. Au sommet, en pi sur deux, la courbe est plate, la pente vaut zéro, et cosinus de pi sur deux vaut zéro. Donc la pente de sinus, c'est cosinus. Je relis : la dérivée de sinus x est cosinus x, la dérivée de cosinus x est moins sinus x. Question : quelle est la pente de la courbe de sinus en pi ?
ÉCRAN : Sur le cercle de rayon 1 : cos x est l'abscisse du point M, sin x son ordonnée. | (sin x)′ = cos x ; (cos x)′ = −sin x. | Au sommet de la courbe de sin, la pente est 0 : cos(π/2) = 0.
QUESTION : Quelle est la pente de la courbe de sin au point d'abscisse π ? OPTIONS : ['+1', '−1', '0']

### Diapo 10 `pr_z4_produit` — Rappel : dériver un produit
VOIX (fr) : Maintenant la dérivée d'un produit. La règle dans le cadre : u fois v, prime, égale u prime v plus u v prime. On dérive le premier en gardant le second, puis on garde le premier en dérivant le second, et on additionne. Voyons-le autrement, avec un exemple : x fois x, c'est x carré, et sa dérivée est deux x. Si on dérive facteur par facteur : un fois un, ça donne un. Et un n'est pas deux x : c'est faux. Avec la règle : un fois x plus x fois un, ça donne deux x. C'est juste. Je relis : la dérivée de u fois v égale u prime v plus u v prime.
ÉCRAN : (uv)′ = u′v + uv′. | Pas facteur par facteur : (x)′·(x)′ = 1, alors que (x²)′ = 2x. | Avec la règle : 1·x + x·1 = 2x.

### Diapo 11 `pr_d4` — Vérifier quand F est un produit
VOIX (fr) : Quand F est un produit, on ne dérive pas de tête. Au tableau : H de x égale x sinus x, et h de x égale sinus x plus x cosinus x. D'abord : H est dérivable sur R, produit de fonctions dérivables. Ensuite, dans le cadre orange, on écrit à part : u de x égale x, u prime égale un ; v de x égale sinus x, v prime égale cosinus x. La formule : u v prime égale u prime v plus u v prime. On remplace : un fois sinus x, plus x fois cosinus x. C'est h de x. Donc H est une primitive de h sur R. À toi : G de x égale x cosinus x. G est une primitive de quelle fonction ?
ÉCRAN : On écrit à part : u(x), u′(x), v(x), v′(x). | (uv)′ = u′v + uv′. | H(x) = x sin x : u = x, u′ = 1 ; v = sin x, v′ = cos x. | H′(x) = sin x + x cos x.
QUESTION : G(x) = x cos x est une primitive sur ℝ de : OPTIONS : ['cos x − x sin x', '−sin x', 'cos x + x sin x']
## II. Existence, famille F + k et condition

### Diapo 12 `pr_e1` — Quand une fonction a-t-elle des primitives ?
VOIX (fr) : Avant de chercher une primitive, une question : est-ce qu'elle existe ? La propriété, encadrée en jaune : si f est continue sur l'intervalle I, alors f admet des primitives sur I. On l'admet. C'est pour cela qu'on étudie la continuité. Exemple : f de x égale x carré moins trois x plus un. f est une fonction polynôme, donc f est continue sur R. Donc f admet des primitives sur R. Deux lignes, c'est tout.
ÉCRAN : Propriété (admise) : toute fonction continue sur un intervalle I admet des primitives sur I. | Pour l'utiliser, on justifie la continuité : polynôme, rationnelle, racine, cos, sin, somme, produit, quotient. | C'est pour cela qu'on étudie la continuité avant de primitiver.

### Diapo 13 `pr_e2` — Toujours sur un intervalle
VOIX (fr) : Regarde l'axe gradué. En zéro, un rond rouge vide : un sur x carré n'existe pas en zéro. L'axe est coupé en deux morceaux. À gauche, en orange, l'intervalle moins l'infini, zéro. À droite, en vert, l'intervalle zéro, plus l'infini. Maintenant la phrase. R privé de zéro, écrit puis barré en rouge : ce n'est pas un intervalle. On écrit à la place, en vert : sur zéro, plus l'infini, les primitives sont moins un sur x plus k.
ÉCRAN : 1/x² n'existe pas en 0 : l'axe a un trou. | ℝ* n'est pas un intervalle : il est fait de deux intervalles, ]−∞ ; 0[ et ]0 ; +∞[. | On primitive sur UN intervalle : sur ]0 ; +∞[, les primitives de 1/x² sont x ↦ −1/x + k, k ∈ ℝ.

### Diapo 14 `pr_e3` — Une infinité de primitives
VOIX (fr) : Regarde la parabole x carré : c'est une primitive de deux x. Maintenant deux autres courbes, plus fines : x carré plus deux, au-dessus, et x carré moins deux, en dessous. Dérive-les : la dérivée d'une constante est zéro, donc elles donnent aussi deux x. Et regarde la courbe épaisse : elle glisse vers le haut d'un bloc, x carré plus k. Pour chaque nombre k, c'est encore une primitive. Il y en a une infinité. Question : quelle est la dérivée de x carré plus dix ?
ÉCRAN : (x²)′ = 2x ; (x² + 10)′ = 2x ; (x² − 7)′ = 2x. | La dérivée d'une constante est 0 : on peut ajouter n'importe quel nombre k. | x² + k est une primitive de 2x, pour tout k ∈ ℝ.
QUESTION : Quelle est la dérivée de x² + 10 ? OPTIONS : ['2x + 10', '2x', 'x³/3 + 10x']
EXERCICE : Laquelle de ces fonctions n'est PAS une primitive de 2x sur ℝ ? OPTIONS : ['x² − 7', 'x² + π', '2x² ']

### Diapo 15 `pr_e4` — F + k est encore une primitive
VOIX (fr) : Il y a deux choses à montrer, on les voit une par une. La première : si F est une primitive de f, F plus k en est une aussi. Sa dérivée, c'est F prime plus la dérivée de k. Et la dérivée d'une constante est zéro, on l'a vu au début. Donc F prime plus zéro, c'est f. Autrement dit : k monte ou descend la courbe, mais ne change pas sa pente. Donc la dérivée ne change pas. Je relis : si F est une primitive de f, alors F plus k est une primitive de f.
ÉCRAN : (F(x) + k)′ = F′(x) + 0 = f(x). | Ajouter k monte ou descend la courbe, sans changer sa pente.

### Diapo 16 `pr_e4_b` — Toutes les primitives : F + k, et pas d'autres
VOIX (fr) : Maintenant la deuxième chose : il n'y en a pas d'autres. Si G est une autre primitive, la dérivée de G moins F, c'est f moins f, soit zéro. Une fonction dont la dérivée est nulle sur un intervalle est constante. Donc G moins F égale k. Voyons-le autrement : deux personnes marchent toujours à la même vitesse. La distance entre elles ne change pas, elle reste constante. G et F ont la même dérivée, donc leur écart est fixe. La ligne encadrée : G de x égale F de x plus k, k appartient à R. Je relis : les primitives de f sur I sont les fonctions F de x plus k, k appartient à R.
ÉCRAN : Si G est une autre primitive : (G − F)′ = f − f = 0 sur I. | Dérivée nulle sur un intervalle : G − F est constante, G(x) = F(x) + k. | Rédaction : les primitives de f sur I sont les fonctions x ↦ F(x) + k, k ∈ ℝ. | La constante se note k ou C (k ∈ ℝ, C ∈ ℝ) : au bac, on écrit souvent F(x) + C.

### Diapo 17 `pr_e5` — Ce qu'on voit : des courbes translatées, mêmes pentes
VOIX (fr) : Regarde encore la courbe épaisse : elle glisse verticalement, d'un bloc, sans se déformer. C'est une translation verticale. Maintenant le pointillé vertical en x égale un. Sur chaque courbe, un petit segment de tangente : ils sont tous parallèles. Même pente : deux. Normal : la pente, c'est la dérivée, et toutes ces courbes ont la même dérivée, deux x. À droite, la légende : la dérivée de x carré plus k est deux x, et les primitives de deux x sont les fonctions x carré plus k, k appartient à R.
ÉCRAN : Les courbes des primitives se déduisent l'une de l'autre par une translation verticale. | Au même x, toutes les tangentes sont parallèles : même pente f(x). | En x = 1, pour x² + k : pente 2 sur chaque courbe. | (x² + k)′ = 2x ; les primitives de 2x : x ↦ x² + k, k ∈ ℝ.
OBSERVATION : En x = 1, compare les petites tangentes des courbes. Que remarques-tu ?

### Diapo 18 `pr_e6` — La primitive qui passe par un point
VOIX (fr) : Toute la famille est là, en traits très fins. On veut une seule primitive : celle qui passe par le point A, un, trois, en jaune. Une courbe épaisse part d'un essai et glisse vers le haut. Elle passe par A : c'est elle, k égale deux. Le calcul, à droite : F de un égale trois. On remplace x par un : un au carré plus k égale trois. Donc k égale deux. Les autres courbes pâlissent : une seule primitive passe par A. F de x égale x carré plus deux.
ÉCRAN : Les primitives de 2x sur ℝ : x ↦ x² + k, k ∈ ℝ. | Condition F(1) = 3 : la courbe passe par A(1 ; 3). | On remplace x par 1 : 1² + k = 3, donc k = 2. | Une seule primitive vérifie la condition : F(x) = x² + 2.

### Diapo 19 `pr_e7` — À toi : une condition avec un calcul plus long
VOIX (fr) : À toi, avec un calcul un peu plus long. f de x égale deux x carré plus x plus un, plus un sur x carré, sur zéro, plus l'infini. D'abord toutes les primitives : deux tiers x cube, plus un demi x carré, plus x, moins un sur x, plus k. Puis la condition F de un égale trois : on remplace x par un, terme par terme. Deux tiers, plus un demi, plus un, moins un, plus k égale trois. Il te reste à regrouper les nombres et à résoudre l'équation en k. À la fin, on écrit toujours F complète. Question : combien trouves-tu pour k ?
ÉCRAN : On écrit d'abord toutes les primitives, avec + k. | On remplace x par x₀ dans F(x), terme par terme. | On regroupe les nombres, on résout en k. | On écrit F complète à la fin, avec la valeur de k.
QUESTION : f(x) = 2x² + x + 1 + 1/x² sur ]0 ; +∞[ et F(1) = 3. La constante k vaut : OPTIONS : ['k = 3', 'k = 7/6', 'k = 11/6']
EXERCICE : f(x) = 4x³ − 2x + 3 sur ℝ : la primitive F telle que F(1) = 0 est : OPTIONS : ['F(x) = x⁴ − x² + 3x − 3', 'F(x) = x⁴ − x² + 3x', 'F(x) = x⁴ − x² + 3x + 3']
## III. Le tableau des primitives usuelles

### Diapo 20 `pr_u1` — Le tableau des primitives : les dérivées à l'envers
VOIX (fr) : Regarde à gauche : des fonctions et leurs dérivées. x carré donne deux x, x cube donne trois x carré, x puissance quatre donne quatre x cube. Les flèches rouges, c'est dériver. Maintenant à droite, on lit les mêmes lignes à l'envers, avec des flèches vertes : deux x donne x carré. Chaque ligne du tableau des dérivées, devient une ligne du tableau des primitives. Regarde la ligne entourée : une primitive de quatre x cube, est x puissance quatre.
ÉCRAN : À gauche, F → F′ : x² → 2x ; x³ → 3x² ; x⁴ → 4x³ (dériver). | À droite, les mêmes lignes lues à l'envers (primitiver) : 2x → x² ; 3x² → x³ ; 4x³ → x⁴. | Chaque ligne du tableau des dérivées donne une ligne du tableau des primitives.

### Diapo 21 `pr_u2` — k et xⁿ : monter l'exposant, diviser
VOIX (fr) : Regarde la règle encadrée : une primitive de x puissance n, est x puissance n plus un, sur n plus un. On monte l'exposant de un, puis on divise par le nouvel exposant. Exemple : x puissance cinq. L'exposant monte à six, entouré en orange, et on divise par six : x puissance six sur six. On vérifie toujours en dérivant : la dérivée de x puissance six sur six, c'est six x puissance cinq sur six, donc x puissance cinq. Et pour une constante : une primitive de k est k x. Par exemple, une primitive de sept est sept x.
ÉCRAN : xⁿ → xⁿ⁺¹/(n + 1) (n ∈ ℕ*) : on monte l'exposant de 1, on divise par le nouvel exposant. | Exemple : x⁵ → x⁶/6. | On vérifie en dérivant : (x⁶/6)′ = 6x⁵/6 = x⁵. | Une constante : k → kx ; 7 → 7x.
QUESTION : Une primitive de x² sur ℝ est : OPTIONS : ['x³/3', '2x', 'x³']

### Diapo 22 `pr_u3` — Le coefficient reste devant
VOIX (fr) : Au tableau : deux x cube, c'est-à-dire deux fois x cube. Le deux est un coefficient, il reste devant, on n'y touche pas. On primitive seulement x cube, avec la règle des puissances, puis on multiplie par deux. Autrement dit, c'est comme pour la dérivée : la dérivée de deux x cube est deux fois trois x carré, le deux est resté devant. La primitive fait pareil. Attention à l'erreur : le deux ne se primitive pas, il ne devient pas deux x. Question : quelle est une primitive de deux x cube ?
ÉCRAN : 2x³ = 2 × x³ : le 2 est un coefficient, il reste devant. | On primitive seulement x³ : 2 × x⁴/4 = x⁴/2. | Vérification : (x⁴/2)′ = 4x³/2 = 2x³. | Erreur : primitiver le coefficient (2 → 2x) dans un produit.
QUESTION : Une primitive de 2x³ sur ℝ est : OPTIONS : ['x⁴/2', '6x²', '2x⁴']
EXERCICE : Une primitive de (1/4)x³ sur ℝ est : OPTIONS : ['(1/4)x + x⁴/4', 'x⁴/16', '3x²/4']

### Diapo 23 `pr_u4` — 1/x² : le moins qui apparaît
VOIX (fr) : Un sur x carré, on l'écrit d'abord en puissance, comme on l'a vu au début : x puissance moins deux. On applique la même règle : l'exposant monte de un, il devient moins un, et on divise par moins un. Regarde le pont rouge : le moins apparaît, et on trouve moins un sur x. On vérifie autrement : la dérivée de moins un sur x est un sur x carré. C'est juste. Toujours sur un intervalle, zéro, plus l'infini, ou moins l'infini, zéro. Je relis : une primitive de un sur x carré est moins un sur x.
ÉCRAN : On écrit en puissance : 1/x² = x⁻². | x⁻² → x⁻¹/(−1) = −1/x : en divisant par −1, le moins apparaît. | Vérification : (−1/x)′ = 1/x².

### Diapo 24 `pr_u4_b` — 1/xⁿ : la règle générale
VOIX (fr) : Même méthode avec un sur x puissance quatre. C'est x puissance moins quatre. L'exposant monte de un : il devient moins trois, et on divise par moins trois. Soit moins un sur trois x cube. La règle encadrée : une primitive de un sur x puissance n est moins un sur, n moins un fois x puissance n moins un, avec n plus grand que un. Toujours sur un intervalle, par exemple zéro, plus l'infini.
ÉCRAN : 1/x⁴ = x⁻⁴ → x⁻³/(−3) = −1/(3x³). | 1/xⁿ → −1/((n − 1)xⁿ⁻¹) (n ≥ 2), sur ]0 ; +∞[ ou sur ]−∞ ; 0[.

### Diapo 25 `pr_u5` — 1/√x : deux racine de x
VOIX (fr) : On part de la dérivée de racine de x : un sur deux racine de x. Donc la dérivée de deux racine de x est un sur racine de x, car le deux se simplifie. Voici la ligne encadrée : une primitive de un sur racine de x est deux racine de x, sur zéro, plus l'infini. Autrement, avec les puissances : un sur racine de x, c'est x puissance moins un demi. L'exposant monte de un : un demi, et on divise par un demi, c'est-à-dire qu'on multiplie par deux. On trouve deux x puissance un demi, soit deux racine de x. Même résultat. Je relis : une primitive de un sur racine de x est deux racine de x.
ÉCRAN : (√x)′ = 1/(2√x), donc (2√x)′ = 1/√x. | 1/√x → 2√x sur ]0 ; +∞[. | En puissance : x^(−1/2) → x^(1/2)/(1/2) = 2√x.

### Diapo 26 `pr_u5_b` — xʳ et les racines : passer en puissance
VOIX (fr) : Pour les autres racines, on les remet en puissance, comme au début. Une primitive de x puissance r est x puissance r plus un, sur r plus un, avec r rationnel différent de moins un, et x strictement positif. Exemple : racine cubique de x, c'est x puissance un tiers. L'exposant devient quatre tiers, et on divise par quatre tiers. On trouve trois quarts, racine cubique de x puissance quatre.
ÉCRAN : xʳ → xʳ⁺¹/(r + 1) (r ∈ ℚ*, r ≠ −1, x > 0). | ∛x = x^(1/3) → x^(4/3)/(4/3) = (3/4)x^(4/3) = (3/4)∛(x⁴).

### Diapo 27 `pr_u6` — cos et sin : le cercle
VOIX (fr) : Regarde le cercle : sinus x en haut, cosinus x à droite, moins sinus x en bas, moins cosinus x à gauche. Pour dériver, on tourne dans le sens des aiguilles d'une montre : c'est la flèche rouge. La dérivée de sinus x est cosinus x, et la dérivée de cosinus x est moins sinus x. Pour primitiver, on tourne dans l'autre sens : c'est la flèche verte. Par exemple, depuis cosinus x, la flèche verte va vers sinus x : une primitive de cosinus x est sinus x. On vérifie : la dérivée de sinus x est cosinus x. À toi : pars de sinus x, en haut, et suis la flèche verte. Question : quelle est une primitive de sinus x ?
ÉCRAN : Le cercle : sin x en haut, cos x à droite, −sin x en bas, −cos x à gauche. | Dériver : on tourne dans le sens des aiguilles d'une montre. | Primitiver : on tourne dans l'autre sens. | cos x → sin x ; sin x → −cos x.
QUESTION : Une primitive de sin x sur ℝ est : OPTIONS : ['cos x', '−cos x', '−sin x']
EXERCICE : Vrai ou faux ? OPTIONS : None

### Diapo 28 `pr_u7` — cos(ax + b) : diviser par le nombre collé à x
VOIX (fr) : Au tableau : cosinus de deux x moins un. On entoure le nombre collé à x, c'est deux. Le moins un, on ne divise pas par lui. On divise par deux : une primitive est un demi sinus de deux x moins un. On vérifie : la dérivée de un demi sinus de deux x moins un, c'est un demi fois deux cosinus de deux x moins un, donc cosinus de deux x moins un. Attention : sinus de deux x moins un est un bloc, on ne le simplifie pas. L'écriture barrée en rouge est fausse.
ÉCRAN : cos(2x − 1) : le nombre collé à x est 2 (pas −1). | On divise par 2 : cos(2x − 1) → (1/2)sin(2x − 1). | Vérification : ((1/2)sin(2x − 1))′ = (1/2) × 2cos(2x − 1) = cos(2x − 1). | sin(2x − 1) est un bloc : on ne le « simplifie » pas.

### Diapo 29 `pr_u8` — Pour mémoire : 1 + tan²x
VOIX (fr) : Pour mémoire, une ligne de plus. La dérivée de tangente x est un plus tangente carré de x, et c'est aussi un sur cosinus carré de x. On lit à l'envers, flèche verte : une primitive de un plus tangente carré de x est tangente x. Et une primitive de un sur cosinus carré de x, est aussi tangente x. Tout ça sur l'intervalle moins pi sur deux, pi sur deux, où tangente est définie. Attention au sens : c'est un plus tangente carré qu'on primitive, et on trouve tangente.
ÉCRAN : (tan x)′ = 1 + tan²x = 1/cos²x. | Lu à l'envers : 1 + tan²x → tan x ; 1/cos²x → tan x. | Sur ]−π/2 ; π/2[ (tan x est définie). | Attention au sens : on primitive 1 + tan²x, on trouve tan x.
## IV. Somme, produit, transformer l'écriture

### Diapo 30 `pr_l1` — Une somme : chaque terme sa primitive, une seule constante
VOIX (fr) : Regarde le début de l'organigramme : je regarde f. Première branche : une somme de fonctions du tableau ? Alors chaque terme prend sa primitive, et on ajoute une seule constante k à la fin. Petit exemple : deux x plus trois. Une primitive de deux x est x carré, et de trois, trois x. Donc les primitives sont x carré plus trois x plus k. Une seule constante, pas deux. Pourquoi une seule ? Autrement dit : deux constantes k un et k deux, leur somme est encore une constante, donc une seule suffit. Question : quelles sont les primitives de cinq x puissance quatre, plus trois x, plus un ?
ÉCRAN : Si F et G sont des primitives de f et g sur un même intervalle I, et α ∈ ℝ : F + G est une primitive de f + g sur I, et αF une primitive de αf sur I. | Car (F + G)′ = F′ + G′ = f + g et (αF)′ = αF′ = αf. | Chaque terme prend sa primitive du tableau. | Une seule constante k, à la fin. | 5x⁴ + 3x + 1 → x⁵ + (3/2)x² + x + k.
QUESTION : Les primitives de f(x) = 5x⁴ + 3x + 1 sur ℝ sont les fonctions : OPTIONS : ['x ↦ 20x³ + 3 + k, k ∈ ℝ', 'x ↦ x⁵ + (3/2)x² + x + k, k ∈ ℝ', 'x ↦ x⁵ + 3x² + x + k, k ∈ ℝ']
EXERCICE : Les primitives de f(x) = 4x³ − 2x + 3 sur ℝ sont les fonctions : OPTIONS : ['x ↦ x⁴ − x² + 3x + k, k ∈ ℝ', 'x ↦ x⁴ − 2x² + 3x + k, k ∈ ℝ', 'x ↦ 12x² − 2 + k, k ∈ ℝ']

### Diapo 31 `pr_l2` — Un produit : la primitive ne se fait pas facteur par facteur
VOIX (fr) : Au tableau : x cosinus x. Tentation : on primitive chaque facteur. x donne x carré sur deux, cosinus x donne sinus x. Essai : x carré sur deux, fois sinus x. On vérifie en dérivant, avec la dérivée d'un produit. On trouve x sinus x, plus x carré sur deux cosinus x. Ce n'est pas x cosinus x ! Donc l'essai est faux, il est barré. La règle encadrée : un produit ne se primitive pas facteur par facteur.
ÉCRAN : x cos x : x → x²/2 et cos x → sin x donne (x²/2)·sin x ? | On dérive pour vérifier : ((x²/2)·sin x)′ = x·sin x + (x²/2)·cos x. | Ce n'est pas x cos x : la réponse est fausse. | Un produit ne se primitive pas facteur par facteur.

### Diapo 32 `pr_l3` — Transformer l'écriture avant de primitiver
VOIX (fr) : Au tableau : x carré plus un, sur x carré, sur zéro, plus l'infini. Cette fonction n'est pas dans le tableau, alors on transforme l'écriture. On sépare la fraction : x carré sur x carré, plus un sur x carré, donc un plus un sur x carré. Maintenant chaque terme est dans le tableau. Un donne x, un sur x carré donne moins un sur x. Les primitives sont x moins un sur x plus k. D'autres gestes possibles : développer un carré, ou écrire une racine en puissance.
ÉCRAN : Séparer une fraction : (x² + 1)/x² = 1 + 1/x². | Développer un carré : (x + 1)² = x² + 2x + 1. | Écrire une racine en puissance : √x = x^(1/2). | Puis chaque terme sa primitive, une seule constante.
## V. Les formes composées u′uⁿ, u′/u², u′/√u, u′cos u

### Diapo 33 `pr_c1` — Rappel : dériver une puissance d'une expression
VOIX (fr) : Avant une nouvelle forme, il faut revoir une dérivée : celle d'une puissance d'une expression. Regarde : x carré plus un, le tout au cube. D'abord, la puissance descend devant : trois, fois x carré plus un au carré. Puis, on n'oublie pas : on multiplie par la dérivée de ce qui est dedans, c'est-à-dire deux x. Donc la dérivée est six x, fois x carré plus un au carré. La règle : la dérivée de u puissance n égale n fois u prime fois u puissance n moins un. Voyons-le autrement : comme une boîte dans une boîte. On dérive d'abord la boîte du dehors, le cube. Puis celle du dedans, x carré plus un. Je relis : la dérivée de u puissance n égale n u prime u puissance n moins un. Question : quelle est la dérivée de x carré plus un, puissance quatre ?
ÉCRAN : La puissance descend devant, puis on multiplie par la dérivée de ce qui est dedans. | ((x² + 1)³)′ = 3(x² + 1)² × 2x = 6x(x² + 1)². | (uⁿ)′ = n · u′ · uⁿ⁻¹.
QUESTION : Quelle est la dérivée de (x² + 1)⁴ ? OPTIONS : ['4(x² + 1)³', '8x(x² + 1)³', '2x(x² + 1)⁴']

### Diapo 34 `pr_c1_b` — La forme u′uⁿ : la dérivée lue à l'envers
VOIX (fr) : Maintenant, on retourne cette dérivée. Au tableau : la dérivée de u puissance n plus un. La puissance descend, et u prime apparaît : n plus un, fois u prime, fois u puissance n. On divise par n plus un. La dérivée de u puissance n plus un, sur n plus un, égale u prime fois u puissance n. On lit cette ligne à l'envers, et voici la règle dans le cadre jaune : une primitive de u prime fois u puissance n est u puissance n plus un, sur n plus un. Autrement dit : pour revenir en arrière, on monte la puissance de un et on divise par la nouvelle puissance, comme pour x puissance n, mais u prime doit être là. Je relis : une primitive de u prime u puissance n est u puissance n plus un sur n plus un.
ÉCRAN : On dérive uⁿ⁺¹ : (uⁿ⁺¹)′ = (n + 1)u′uⁿ. | On divise par n + 1 : (uⁿ⁺¹/(n + 1))′ = u′uⁿ. | Donc une primitive de u′uⁿ est uⁿ⁺¹/(n + 1) (n ∈ ℕ*).
EXERCICE : Une primitive de u′u⁴ est : OPTIONS : ['u⁵/5', 'u⁵', '4u′u³']

### Diapo 35 `pr_c2` — Repérer u et sa dérivée : la bulle
VOIX (fr) : Regarde l'expression au tableau : deux x plus un, fois x carré plus x moins quatre, puissance trois. Ce qui est à la puissance, je le souligne en rouge : c'est u. Maintenant, la bulle : je calcule à part la dérivée de u. La dérivée de x carré plus x moins quatre égale deux x plus un. La flèche montre : c'est exactement le facteur devant. Alors je réécris f de x : u prime, fois u puissance trois, et j'écris la forme en face, u prime u puissance n, avec n égale trois. Il reste à appliquer la règle : une primitive est x carré plus x moins quatre, puissance quatre, sur quatre.
ÉCRAN : On souligne ce qui est à la puissance : c'est u. | Dans une bulle, on calcule u′. | Si u′ est déjà là, on réécrit f(x) = u′(x)u(x)ⁿ et on écrit la forme en face. | Une primitive : uⁿ⁺¹/(n + 1).

### Diapo 36 `pr_c3` — Il manque un nombre : multiplier et diviser
VOIX (fr) : Même méthode, mais regarde la bulle : la dérivée de x carré plus deux x moins six égale deux x plus deux, c'est-à-dire deux fois x plus un. Devant, on a seulement x plus un : il manque le deux. Donc, en vert, on multiplie et on divise par deux. On garde un demi devant, et dedans on a u prime. On réécrit : f de x égale un demi, fois u prime, fois u carré. La primitive dans le cadre : un demi, fois u cube sur trois, soit un sixième de x carré plus deux x moins six, au cube. Autrement dit : multiplier et diviser par deux, c'est comme ajouter puis enlever la même chose : f ne change pas.
ÉCRAN : (x² + 2x − 6)′ = 2x + 2 = 2(x + 1) : il manque le facteur 2. | On multiplie et on divise par 2 : on garde ½ devant. | f(x) = ½(x² + 2x − 6)′(x² + 2x − 6)² → (1/6)(x² + 2x − 6)³.

### Diapo 37 `pr_c3_b` — On ne prête qu'un nombre
VOIX (fr) : Maintenant un cas piège. Regarde le petit cadre seul : x carré plus un, au cube. La dérivée de x carré plus un est deux x. Et ici, devant, il n'y a rien : il manque deux x entier. Le deux, on peut le prêter, c'est un nombre : on multiplie et on divise. Mais x, non : x n'est pas un nombre, si on divise par x il reste dans la primitive et tout est faux. Donc ici, la forme u prime u puissance n ne marche pas. Je relis : on multiplie et on divise seulement par un nombre, jamais par x.
ÉCRAN : (x² + 1)³ seul : la dérivée de x² + 1 est 2x, il manque 2x entier. | On peut prêter un nombre (multiplier et diviser), jamais x. | Ici la forme u′uⁿ ne marche pas.

### Diapo 38 `pr_c4` — (ax + b)ⁿ : le cas le plus fréquent
VOIX (fr) : Le cas le plus fréquent : deux x moins un, au cube. Pas besoin de développer. La bulle : la dérivée de deux x moins un est deux, un nombre simple. Il manque ce deux devant, donc on multiplie et on divise par deux : f de x égale un demi, fois u prime, fois u cube. C'est la forme u prime u puissance n, avec n égale trois. Il ne reste qu'à appliquer la règle. Attention, le un demi devant reste, ne l'oublie pas. Question : quelle est une primitive de deux x moins un, au cube ?
ÉCRAN : u(x) = 2x − 1, u′(x) = 2 : un nombre. | On multiplie et on divise par 2 : f(x) = ½(2x − 1)′(2x − 1)³. | Une primitive : ½ × (2x − 1)⁴/4 = (2x − 1)⁴/8. | Pas besoin de développer ; ne pas oublier le ½.
QUESTION : Une primitive de f(x) = (2x − 1)³ sur ℝ est : OPTIONS : ['(2x − 1)⁴/4', '(2x − 1)⁴/8', '2(2x − 1)⁴']
EXERCICE : Une primitive de (3x + 2)⁴ sur ℝ est : OPTIONS : ['(3x + 2)⁵/5', '(3x + 2)⁵/15', '3(3x + 2)⁵/5']

### Diapo 39 `pr_c5` — u′uʳ : avec une racine
VOIX (fr) : Cette fois il y a une racine cubique : six x, fois racine cubique de trois x carré plus un. La bulle : la dérivée de trois x carré plus un égale six x, c'est exactement le facteur devant. Et trois x carré plus un est strictement positif, c'est nécessaire pour une puissance rationnelle. On écrit la racine en puissance : racine cubique de u, c'est u puissance un tiers. Alors f est de la forme u prime u puissance r, avec r égale un tiers. On ajoute un à l'exposant : un tiers plus un égale quatre tiers, et on divise par quatre tiers. Donc une primitive est trois quarts, fois racine cubique de u puissance quatre.
ÉCRAN : On écrit la racine en puissance : ∛u = u^(1/3). | Il faut u > 0 sur l'intervalle. | u′uʳ → uʳ⁺¹/(r + 1) (r ∈ ℚ*, r ≠ −1). | Exemple : 6x·∛(3x² + 1) = (3x² + 1)′(3x² + 1)^(1/3) → (3x² + 1)^(4/3)/(4/3) = (3/4)∛((3x² + 1)⁴).

### Diapo 40 `pr_c6` — u′/u² : un carré en bas
VOIX (fr) : En haut, la règle encadrée : la dérivée de moins un sur u égale u prime sur u carré. Donc une primitive de u prime sur u carré est moins un sur u. N'oublie pas le moins. Exemple : x sur x carré plus un, au carré. Un carré en bas, c'est cette forme. La bulle : la dérivée de x carré plus un égale deux x. En haut, on a seulement x : il manque le deux. On multiplie et on divise par deux, et on garde un demi devant. Alors une primitive : un demi fois moins un sur x carré plus un, c'est-à-dire moins un, sur deux fois x carré plus un. Ici x carré plus un ne s'annule jamais, donc on travaille sur R.
ÉCRAN : (−1/u)′ = u′/u² : donc u′/u² → −1/u. | u ne doit pas s'annuler sur l'intervalle. | Exemple : x/(x² + 1)² = ½ × (x² + 1)′/(x² + 1)². | Une primitive : ½ × (−1/(x² + 1)) = −1/(2(x² + 1)), sur ℝ car x² + 1 ≠ 0.

### Diapo 41 `pr_c6_b` — u′/uⁿ : la règle générale
VOIX (fr) : On a vu u prime sur u carré. Et si u est en bas à la puissance trois, ou quatre ? Même méthode que pour un sur x puissance n. On monte u en haut : u prime sur u puissance n, c'est u prime fois u puissance moins n. C'est la forme u prime u puissance n, avec un exposant négatif. On ajoute un à l'exposant, et on divise par le nouvel exposant. La règle encadrée : une primitive de u prime sur u puissance n est moins un, sur, n moins un fois u puissance n moins un, avec n supérieur ou égal à deux, et u ne s'annule pas sur I. Exemple : deux x, sur x carré plus un, puissance trois. La bulle : la dérivée de x carré plus un est deux x, elle est en haut. Ici n égale trois : une primitive est moins un, sur deux fois x carré plus un, au carré. Autrement : on dérive cette primitive, et on retrouve deux x, sur x carré plus un puissance trois. Et quand u est x, on retrouve la règle de un sur x puissance n. Je relis : une primitive de u prime sur u puissance n est moins un, sur, n moins un fois u puissance n moins un.
ÉCRAN : u′/uⁿ = u′·u⁻ⁿ : c'est la forme u′uⁿ avec un exposant entier négatif (≠ −1), sur un intervalle I où u ≠ 0. | On monte l'exposant de 1 et on divise : u⁻ⁿ⁺¹/(−n + 1) = −1/((n − 1)uⁿ⁻¹). | u′/uⁿ → −1/((n − 1)uⁿ⁻¹) (n ≥ 2), u ≠ 0 sur I. | Exemple : 2x/(x² + 1)³ = (x² + 1)′/(x² + 1)³, n = 3 → −1/(2(x² + 1)²), sur ℝ car x² + 1 ≠ 0. | Vérification : (−½(x² + 1)⁻²)′ = −½ × (−2) × 2x(x² + 1)⁻³ = 2x/(x² + 1)³. | Avec u = x, on retrouve 1/xⁿ → −1/((n − 1)xⁿ⁻¹).

### Diapo 42 `pr_c7` — u′/√u : une racine en bas
VOIX (fr) : On part de la dérivée de racine de u : u prime sur deux racine de u. On multiplie par deux : la dérivée de deux racine de u égale u prime sur racine de u. Voici la règle dans le cadre : une primitive de u prime sur racine de u est deux racine de u, avec u strictement positif. Exemple : x sur racine de x carré plus un. La bulle : la dérivée de x carré plus un égale deux x, et x carré plus un est positif. En haut il manque le deux : on garde un demi devant. C'est la forme u prime sur racine de u. Il ne reste qu'à appliquer la règle, et regarder ce que deviennent le un demi et le deux. Question : quelle est une primitive de x sur racine de x carré plus un ?
ÉCRAN : D'abord : (√u)′ = u′/(2√u). | Donc (2√u)′ = u′/√u : u′/√u → 2√u. | Il faut u > 0 sur l'intervalle. | Exemple : x/√(x² + 1) → √(x² + 1).
QUESTION : Une primitive de f(x) = x/√(x² + 1) sur ℝ est : OPTIONS : ['2√(x² + 1)', '√(x² + 1)', 'x√(x² + 1)']
EXERCICE : Vrai ou faux ? OPTIONS : None

### Diapo 43 `pr_c8` — Même numérateur, trois dénominateurs
VOIX (fr) : Trois fractions au tableau, avec le même numérateur deux x plus trois. Une seule bulle pour les trois : la dérivée de x carré plus trois x moins quatre égale deux x plus trois. C'est le bas qui choisit la forme, regarde au-dessus de chaque colonne. Première colonne : u carré en bas, forme u prime sur u carré, résultat moins un sur u. Deuxième colonne : racine de u en bas, forme u prime sur racine de u, résultat deux racine de u. Troisième colonne : u seul en bas, c'est la forme u prime sur u, un rideau dit plus tard, dans le chapitre ln. Et en bas, le petit axe : les racines moins quatre et un. Sur l'intervalle un, plus l'infini, u est strictement positif.
ÉCRAN : Même numérateur 2x + 3 = (x² + 3x − 4)′. | En bas u² : forme u′/u² → −1/u. | En bas √u : forme u′/√u → 2√u (u > 0). | En bas u : forme u′/u, plus tard (chapitre ln). | x² + 3x − 4 > 0 sur ]1 ; +∞[.

### Diapo 44 `pr_c9` — u′·cos u et u′·sin u
VOIX (fr) : En haut, deux règles encadrées. Une primitive de u prime cosinus u est sinus u. Une primitive de u prime sinus u est moins cosinus u. C'est le cercle de tout à l'heure, avec u à la place de x. Exemple : pi x, fois cosinus de pi x carré plus trois. Dans le cosinus, ce n'est pas a x plus b : on fait la bulle. La dérivée de pi x carré plus trois égale deux pi x. Devant, on a seulement pi x : il manque le deux. On multiplie et on divise par deux, on garde un demi devant, et c'est la forme u prime cosinus u. Une primitive : un demi sinus de pi x carré plus trois.
ÉCRAN : u′·cos u → sin u ; u′·sin u → −cos u. | Même bulle : on calcule u′ à part. | Exemple : πx·cos(πx² + 3) : (πx² + 3)′ = 2πx, il manque 2. | Une primitive : ½ sin(πx² + 3).
## VI. Reconnaître une dérivée ; choisir la méthode

### Diapo 45 `pr_r1` — Reconnaître la dérivée d'un produit
VOIX (fr) : La dérivée d'un produit u v égale u prime v plus u v prime. Lue à l'envers : une primitive de u prime v plus u v prime est u v. Exemple au tableau : f de x égale sinus x plus x cosinus x. Primitiver chaque terme ne marche pas avec x cosinus x : il n'est pas dans le tableau. Mais regarde le premier terme : sinus x, c'est la dérivée de x, fois sinus x. Et le deuxième terme : x cosinus x, c'est x, fois la dérivée de sinus x. Donc avec u égale x et v égale sinus x, f est u prime v plus u v prime. Il ne reste qu'à lire la règle à l'envers. Question : quelles sont les primitives de sinus x plus x cosinus x ?
ÉCRAN : (uv)′ = u′v + uv′ : lue à l'envers, u′v + uv′ → uv. | On cherche deux fonctions u et v et leurs dérivées dans les deux termes. | Exemple : sin x + x cos x = (x)′·sin x + x·(sin x)′. | Les primitives : x sin x + k, k ∈ ℝ.
QUESTION : Les primitives de f(x) = sin x + x cos x sur ℝ sont les fonctions : OPTIONS : ['x ↦ −cos x + (x²/2)sin x + k', 'x ↦ x sin x + k', 'x ↦ x cos x + k']
EXERCICE : Une primitive de f(x) = 2x·cos x − x²·sin x sur ℝ est : OPTIONS : ['x² cos x', 'x² sin x', '2 sin x + x² cos x']

### Diapo 46 `pr_r2` — Reconnaître la dérivée d'un quotient
VOIX (fr) : En haut, la dérivée d'un quotient lue à l'envers : une primitive de, u prime v moins u v prime, sur v carré, est u sur v. Exemple : x carré plus deux x, sur x plus un au carré, sur l'intervalle moins un, plus l'infini. Le carré en bas fait penser à un quotient. On essaie u égale x carré, et v égale x plus un. On écrit à part u prime égale deux x et v prime égale un. Calcul : deux x fois x plus un, moins x carré, sur x plus un au carré. On trouve exactement x carré plus deux x en haut. Donc une primitive est x carré sur x plus un. En vert, une autre méthode donne x plus un sur x plus un. C'est x carré sur x plus un, plus un : même famille, une constante d'écart.
ÉCRAN : (u/v)′ = (u′v − uv′)/v² : lue à l'envers, (u′v − uv′)/v² → u/v. | Un carré v² en bas fait penser à un quotient. | Exemple : (x² + 2x)/(x + 1)² avec u = x², v = x + 1 : u′v − uv′ = 2x(x + 1) − x² × 1 = x² + 2x. | Une autre méthode peut donner x + 1/(x + 1) : même famille, à une constante près.

### Diapo 47 `pr_r3` — Choisir la méthode : l'organigramme
VOIX (fr) : Devant une fonction, on se pose les questions dans l'ordre. En haut : je regarde f. Première branche : est-ce une somme de fonctions du tableau ? Alors chaque terme sa primitive, et une seule constante k à la fin. Deuxième branche : est-ce une forme composée, u prime u puissance n, u prime sur u carré, u prime sur racine de u, u prime cosinus u ou u prime sinus u ? On accepte u prime à un nombre près. Troisième branche : u prime v plus u v prime donne u v, et le quotient donne u sur v. Quatrième branche : sinon, je transforme l'écriture, je développe, je sépare, j'écris en puissance. En bas, un exemple : trois fois trois x plus un, puissance quatre. Trois, c'est la dérivée de trois x plus un.
ÉCRAN : 1. Une somme de fonctions du tableau ? → chaque terme sa primitive, une seule constante k. | 2. Une forme u′uⁿ, u′/u², u′/√u, u′cos u, u′sin u (u′ à un nombre près) ? → la forme. | 3. u′v + uv′ ? → uv ; (u′v − uv′)/v² ? → u/v. | 4. Sinon : transformer l'écriture (développer, séparer, puissance). | Exemple : 3(3x + 1)⁴ = (3x + 1)′(3x + 1)⁴ → (3x + 1)⁵/5.
## VII. La courbe de f est la pente de F

### Diapo 48 `pr_g1` — La courbe de f est la pente de F
VOIX (fr) : Deux repères, l'un au-dessus de l'autre, avec la même échelle en x. En haut, la courbe de F, x cube sur trois moins x. En bas, la courbe de f, x carré moins un. f est la dérivée de F. Maintenant regarde le trait vertical : il traverse les deux repères au même x, et il glisse. En haut, la tangente à F suit le trait. En bas, le trait jaune, c'est la valeur de f. En x égale un virgule cinq, f vaut un virgule vingt-cinq : c'est la pente de la tangente à F. Donc la courbe de f, c'est la pente de F, point par point.
ÉCRAN : En haut la courbe de F(x) = x³/3 − x, en bas celle de f(x) = x² − 1 = F′(x). | Au même x, f(x) est la pente de la tangente à la courbe de F. | En x = 1,5 : f(1,5) = 1,25 : la tangente à F monte avec la pente 1,25. | Si f(a) = 0, la tangente à la courbe de F en a est horizontale.

### Diapo 49 `pr_g2` — Signe de f, variations de F
VOIX (fr) : Même construction, et maintenant on colorie. Sur la courbe de f, les morceaux au-dessus de l'axe sont en vert, et en dessous en orange. Regarde en haut : la courbe de F est repassée avec les mêmes couleurs. Là où f est positive, F monte. Là où f est négative, F descend. C'est la règle : F prime égale f, donc le signe de f donne le sens de variation de F. Maintenant regarde x égale moins un et x égale un : f s'annule. En haut, F a un sommet en moins un, c'est un maximum, et un creux en un, c'est un minimum. Les tangentes y sont horizontales. Dans l'exercice suivant, c'est toi qui finis le tableau de variations de F.
ÉCRAN : F′ = f : le signe de f donne le sens de variation de F. | f ≥ 0 sur I ⇒ F croissante sur I ; f ≤ 0 sur I ⇒ F décroissante sur I. | f(x) = x² − 1 = (x − 1)(x + 1) : f ≤ 0 sur [−1 ; 1], f ≥ 0 ailleurs. | f s'annule en changeant de signe : F a un maximum en −1 et un minimum en 1.
OBSERVATION : Là où la courbe de f est orange (sous l'axe), que fait la courbe de F, en haut ?

### Diapo 50 `pr_g3` — Type devoir : le tableau de variations de F
VOIX (fr) : Maintenant un exercice comme ceux des devoirs. f de x égale trois moins x, et F est une primitive de f. D'abord : F prime égale f, donc on lit le signe de f. La courbe de f est une droite qui descend. Trois moins x égale zéro, donc x égale trois. Maintenant le tableau. Première ligne : x, de moins l'infini à plus l'infini, avec trois au milieu. Deuxième ligne : le signe de f de x. Avant trois, f est positive, plus. Après trois, f est négative, moins. Troisième ligne, à toi : les variations de F. Question : sur quel intervalle F est-elle croissante ?
ÉCRAN : f(x) = 3 − x sur ℝ ; F est une primitive de f. | F′(x) = f(x) = 3 − x ; 3 − x = 0 ⇔ x = 3. | Le signe de f(x) : + avant 3, − après. | À toi : la ligne des variations de F.
QUESTION : f(x) = 3 − x et F est une primitive de f sur ℝ. F est croissante sur : OPTIONS : ['[3 ; +∞[', ']−∞ ; 3]', 'ℝ']
## VIII. Exercices type national

### Diapo 51 `pr_x1` — Type national : montrer que H est une primitive de h
VOIX (fr) : Voici la question qui tombe une année sur deux au national. H de x égale, x carré plus un, fois racine de x. Il faut montrer que H est une primitive de h sur zéro, plus l'infini. Première ligne : H est dérivable sur cet intervalle, c'est un produit de fonctions dérivables. Attention, racine de x n'est pas dérivable en zéro, d'où l'intervalle ouvert. Deuxième ligne, à toi : H est un produit. Écris à part u, u prime, v, v prime, puis calcule H prime de x. Question : que vaut H prime de x ?
ÉCRAN : Énoncé : montrer que H(x) = (x² + 1)√x est une primitive de h(x) = (5x² + 1)/(2√x) sur ]0 ; +∞[. | 1) H est dérivable sur ]0 ; +∞[ (produit de fonctions dérivables sur cet intervalle). | 2) À toi : u, u′, v, v′ à part, puis H′(x) = u′v + uv′.
QUESTION : H(x) = (x² + 1)√x sur ]0 ; +∞[ : que vaut H′(x) ? OPTIONS : ['H′(x) = 2x√x + (x² + 1)/(2√x)', 'H′(x) = 2x · 1/(2√x) = x/√x', 'H′(x) = 2x√x']

### Diapo 52 `pr_x1_b` — Type national : tout sur le même dénominateur
VOIX (fr) : On continue. Deuxième ligne : H prime de x égale deux x racine de x, plus, x carré plus un, sur deux racine de x. Ce n'est pas encore h de x. Troisième ligne, à toi : on met tout sur le même dénominateur, deux racine de x. Rappel : racine de x fois racine de x égale x. À la fin, on écrit la conclusion avec l'intervalle. Question : que donne cette somme sur deux racine de x ?
ÉCRAN : H′(x) = 2x√x + (x² + 1)/(2√x) : ce n'est pas encore h(x). | 3) À toi : tout sur le dénominateur 2√x (√x·√x = x). | 4) La conclusion, avec l'intervalle ]0 ; +∞[.
QUESTION : Sur le dénominateur 2√x : 2x√x + (x² + 1)/(2√x) = ? OPTIONS : ['(5x² + 1)/(2√x)', '(3x² + 1)/(2√x)', '(2x + x² + 1)/(2√x)']

### Diapo 53 `pr_x2` — Type national : reconnaître la forme u′uⁿ
VOIX (fr) : Un exercice qui enchaîne deux choses. f de x égale, deux x plus un, fois, x carré plus x plus un, au carré. On cherche la primitive F telle que F de zéro égale un. D'abord la bulle : la dérivée de x carré plus x plus un, c'est deux x plus un. Elle est déjà là, devant. À toi : quelle forme est-ce, et combien vaut n ? Puis applique la règle. Question : quelle est une primitive de f ?
ÉCRAN : f(x) = (2x + 1)(x² + x + 1)² sur ℝ ; ensuite on cherchera F telle que F(0) = 1. | 1) La bulle : (x² + x + 1)′ = 2x + 1, déjà devant. | 2) À toi : quelle forme, quel n, puis une primitive de f.
QUESTION : f(x) = (2x + 1)(x² + x + 1)² sur ℝ. Une primitive de f est : OPTIONS : ['F(x) = (x² + x + 1)³/3', 'F(x) = (x² + x + 1)³', 'F(x) = (2x + 1)(x² + x + 1)³/3']

### Diapo 54 `pr_x2_b` — Type national : la condition F(0) = 1
VOIX (fr) : On continue. C'est la forme u prime u carré, donc une primitive est u cube sur trois. Et toutes les primitives : x carré plus x plus un, au cube, sur trois, plus k. Ensuite la condition F de zéro égale un. À toi : remplace x par zéro, et trouve k. À la fin, écris F complète. Question : combien vaut k ?
ÉCRAN : f(x) = (2x + 1)(x² + x + 1)² : forme u′u², n = 2. | Les primitives : F(x) = (x² + x + 1)³/3 + k, k ∈ ℝ. | 3) À toi : F(0) = 1 donne k ; puis écris F(x) complète.
QUESTION : F(x) = (x² + x + 1)³/3 + k et F(0) = 1. Alors : OPTIONS : ['k = 2/3', 'k = 1', 'k = 4/3']

### Diapo 55 `pr_x3` — Exercice bilan : l'existence, puis la forme u′/u²
VOIX (fr) : Un exercice qui reprend tout le chapitre. f de x égale, x sur, x carré plus un au carré, plus cosinus de deux x. On cherche la primitive F telle que F de zéro égale zéro. Première ligne, l'existence : x carré plus un ne s'annule jamais, donc f est continue sur R, et elle admet des primitives sur R. Deuxième ligne, à toi : le premier terme. La dérivée de x carré plus un, c'est deux x, et en haut il y a seulement x. Quelle forme, et que manque-t-il ? Question : quelle est une primitive de x sur x carré plus un au carré ?
ÉCRAN : f(x) = x/(x² + 1)² + cos(2x) sur ℝ ; on cherchera F telle que F(0) = 0. | 1) x² + 1 ≠ 0 : f est continue sur ℝ, donc elle admet des primitives sur ℝ. | 2) À toi : (x² + 1)′ = 2x ; quelle forme, et quelle primitive pour x/(x² + 1)² ?
QUESTION : Une primitive de x/(x² + 1)² sur ℝ est : OPTIONS : ['−1/(x² + 1)', '−1/(2(x² + 1))', '1/(2(x² + 1)²)']

### Diapo 56 `pr_x3_b` — Exercice bilan : une seule constante, puis la condition
VOIX (fr) : On continue. Le premier terme : un demi fois u prime sur u carré, et une primitive est moins un, sur deux fois x carré plus un. Pour cosinus de deux x, on divise par deux : un demi sinus de deux x. Et une seule constante k, à la fin. Troisième ligne, à toi : la condition F de zéro égale zéro. Remplace x par zéro ; attention, sinus zéro égale zéro. Question : quelle est F de x complète ?
ÉCRAN : Une primitive de x/(x² + 1)² : −1/(2(x² + 1)). | Une primitive de cos(2x) : ½ sin(2x). | F(x) = −1/(2(x² + 1)) + ½ sin(2x) + k, k ∈ ℝ : une seule constante. | 3) À toi : F(0) = 0 donne k.
QUESTION : f(x) = x/(x² + 1)² + cos(2x) : la primitive F de f sur ℝ telle que F(0) = 0 est : OPTIONS : ['F(x) = −1/(x² + 1) + sin(2x) + 1', 'F(x) = −1/(2(x² + 1)) + ½ sin(2x) + 1/2', 'F(x) = −1/(2(x² + 1)) + ½ sin(2x)']

### Diapo 57 `pr_x4` — Ce qui viendra : ln, exp et l'intégrale
VOIX (fr) : Pour finir, regarde ce qui viendra. En haut, trois lignes du tableau de ce chapitre : x puissance n, un sur racine de x, cosinus x. Plus tard, au chapitre ln, en orange : la primitive de un sur x sera ln de valeur absolue de x. Et u prime sur u, ce sera ln de valeur absolue de u. Ensuite, au chapitre exp : e puissance x, et u prime e puissance u. Le tableau aura des lignes de plus. Et en bas, encadrée, l'intégrale du semestre deux : l'intégrale de a à b de f, égale F de b moins F de a. Elle tombe dans tous les sujets du national. Et elle commence toujours par une primitive.
ÉCRAN : Le tableau de ce chapitre : xⁿ, 1/√x, cos x, sin x… | Plus tard, chapitre ln : 1/x → ln|x| ; u′/u → ln|u|. | Plus tard, chapitre exp : eˣ → eˣ ; u′eᵘ → eᵘ. | Semestre 2 : ∫ₐᵇ f(x)dx = F(b) − F(a) : chaque intégrale commence par une primitive (20 sujets sur 20).
## IX. Bilan et carte du chapitre

### Diapo 58 `pr_b1` — Ce qu'il faut retenir
VOIX (fr) : Faisons le bilan sur une seule fiche, bloc par bloc, et écris avec moi. Un : la définition. F est une primitive de f sur I, si F est dérivable sur I, et F prime de x égale f de x pour tout x de I. Pour vérifier, on dérive. Deux : l'existence et la famille. f continue sur un intervalle, alors elle admet des primitives. Toutes s'écrivent F plus k. Toujours un intervalle. Trois : la condition. F de x zéro égale y zéro donne k, une seule primitive. Quatre : le tableau. Monter l'exposant et diviser, deux racine de x, et attention au signe de sinus. Cinq : les opérations. Une somme, chaque terme sa primitive, une seule constante. Six : les formes. On fait la bulle, on voit u prime, et on ne prête qu'un nombre. Sept : les dérivées reconnues, produit et quotient. Sinon, on transforme l'écriture. Huit : le graphique. f positive, F croissante, et f est la pente de F. La deuxième page est la tienne : ce qu'il te reste à retravailler.
ÉCRAN : 1. Définition : F est une primitive de f sur I : F est dérivable sur I et F′(x) = f(x) pour tout x de I. Vérifier = dériver. ⚠ Jamais « f = F ». | 2. Existence et famille : f continue sur I ⇒ f admet des primitives sur I ; toutes : x ↦ F(x) + k, k ∈ ℝ. ⚠ Toujours un intervalle, jamais ℝ*. | 3. Condition : F(x₀) = y₀ donne k : une seule primitive. | 4. Tableau (k ∈ ℝ ; « f → F » se lit « une primitive de f est F ») : a → ax + k sur ℝ (a ∈ ℝ) ; xⁿ → xⁿ⁺¹/(n + 1) + k sur ℝ (n ∈ ℕ*) ; 1/x² → −1/x + k et 1/xⁿ → −1/((n − 1)xⁿ⁻¹) + k (n ≥ 2), sur ]0 ; +∞[ ou sur ]−∞ ; 0[ ; 1/√x → 2√x + k et xʳ → xʳ⁺¹/(r + 1) + k (r ∈ ℚ*, r ≠ −1), sur ]0 ; +∞[ ; cos x → sin x + k et sin x → −cos x + k, sur ℝ ; cos(ax + b) → (1/a)sin(ax + b) + k et sin(ax + b) → −(1/a)cos(ax + b) + k (a ≠ 0), sur ℝ ; 1 + tan²x = 1/cos²x → tan x + k, sur ]−π/2 ; π/2[. ⚠ Le signe de sin. | 5. Opérations : si F et G sont des primitives de f et g sur I et α ∈ ℝ, F + G est une primitive de f + g et αF une primitive de αf sur I ; une seule constante k. ⚠ Pas facteur par facteur. | 6. Formes (u dérivable sur I, k ∈ ℝ) : u′uⁿ → uⁿ⁺¹/(n + 1) + k (n ∈ ℤ, n ≠ −1 ; u ≠ 0 sur I si n < 0) ; (ax + b)ⁿ → (ax + b)ⁿ⁺¹/(a(n + 1)) + k (a ≠ 0, n ∈ ℕ*) ; u′/u² → −1/u + k et u′/uⁿ → −1/((n − 1)uⁿ⁻¹) + k (n ≥ 2), u ≠ 0 sur I ; u′uʳ → uʳ⁺¹/(r + 1) + k (r ∈ ℚ*, r ≠ −1), u > 0 sur I ; u′/√u → 2√u + k, u > 0 sur I ; u′·cos u → sin u + k ; u′·sin u → −cos u + k. ⚠ On ne prête qu'un nombre. | 7. Dérivées reconnues : u′v + uv′ → uv + k ; (u′v − uv′)/v² → u/v + k (v ≠ 0 sur I) ; sinon transformer l'écriture. | 8. Graphique : f ≥ 0 sur I ⇒ F croissante sur I ; f est la pente de F. | Page 2, ta page : ce qu'il te reste à retravailler, d'après tes réponses du cours (repris en mode libre, avec la méthode qui marche pour toi).

### Diapo 59 `pr_b2` — La carte du chapitre
VOIX (fr) : Dessinons la carte de tout le chapitre, en une seule image. Au centre : F prime égale f. Dériver va de F à f, primitiver revient de f à F. Première branche : vérifier, on dérive F. Deuxième branche : l'existence, f continue sur un intervalle. Troisième branche : la famille, F plus k. Quatrième branche : la condition, qui donne k. Cinquième branche : le tableau des primitives usuelles. Sixième branche : les formes, avec la bulle de u prime. Septième branche : les dérivées reconnues, produit et quotient. Huitième branche : le graphique, f est la pente de F. Et la dernière branche : plus tard, ln, exp, et l'intégrale du semestre deux. Voilà la carte du chapitre. Les branches entourées en rouge, ce sont celles qu'on va reprendre ensemble. Question : quelle est la première chose à faire, pour vérifier qu'une fonction est une primitive ?
ÉCRAN : Au centre : F′ = f ; dériver va de F à f, primitiver revient de f à F. | Vérifier : on dérive F et on retrouve f(x) sur I. | Existence : f continue sur un intervalle I. | Famille : x ↦ F(x) + k, k ∈ ℝ ; condition F(x₀) = y₀ → k. | Tableau des primitives usuelles ; formes u′uⁿ, u′/u², u′/√u, u′·cos u, u′·sin u. | Dérivées reconnues : uv, u/v ; graphique : f est la pente de F. | Plus tard : ln, exp, et l'intégrale du semestre 2.
QUESTION : Pour vérifier que F est une primitive de f sur I, la première chose à faire est : OPTIONS : ['Calculer F(0) et comparer à f(0)', 'Primitiver f, comme pour trouver F', 'Dériver F et comparer à f(x)']

### Diapo 60 `pr_fermeture_cours` — Ce qu'il faut retenir, et comment réviser
VOIX (fr) : Nous arrivons à la fin du cours : Fonctions primitives. Que faut-il retenir ? Trois idées. Première : F est une primitive de f sur I si F prime de x égale f de x pour tout x de I. Deuxième : toutes les primitives de f sont F de x plus k. Troisième : une primitive de u prime u puissance n est u puissance n plus un, sur n plus un. Maintenant quelques conseils pour réviser. Relis ton cahier, et refais seul les exercices du national. Quand tu réponds, écris chaque étape, et chaque résultat avec sa justification, car chaque étape a ses points. Le jour de l'examen, partage ton temps, et commence par la question qui te paraît facile. La veille, dors bien. Écris ces conseils dans ton cahier. Tu as bien travaillé, bon courage ! Le prochain cours : Fonctions logarithmiques. On s'y retrouve !
ÉCRAN : Retenir : F′(x) = f(x) sur I · F(x) + k · u′uⁿ → uⁿ⁺¹/(n + 1) (n ≠ −1) | Réviser : relire le cahier, refaire les exercices du national | Rédiger : chaque étape, et sa justification (car…) | Jour J : gérer son temps · bien dormir la veille

## Questions de bloc (posées après la dernière diapo du bloc)
- après diapo 5 `pr_s1_b1` RETROUVER : Cahier fermé : écris la définition complète de « F est une primitive de f sur I ».
- après diapo 5 `pr_s1_b1` EXERCICE : La dérivée d'une constante k est : OPTIONS : ['k', '0', '1']
- après diapo 8 `pr_s1_b1b` RETROUVER : Cahier fermé : écris la dérivée de xⁿ.
- après diapo 8 `pr_s1_b1b` EXERCICE : G(x) = x⁴ + 5 est-elle une primitive de g(x) = 4x³ sur ℝ ? OPTIONS : ['Oui', 'Non, à cause du 5', 'Non, il faudrait x⁴/4']
- après diapo 11 `pr_s1_b2` RETROUVER : Cahier fermé : écris la dérivée d'un produit u·v.
- après diapo 11 `pr_s1_b2` EXERCICE : Quelle est la dérivée de cos x ? OPTIONS : ['sin x', '−sin x', '−cos x']
- après diapo 14 `pr_s1_b3` RETROUVER : Cahier fermé : écris la propriété qui garantit l'existence de primitives.
- après diapo 14 `pr_s1_b3` EXERCICE : g(x) = √x + cos x admet des primitives sur : OPTIONS : ['ℝ', '[0 ; +∞[', ']−∞ ; 0]']
- après diapo 17 `pr_s2_b1` RETROUVER : Cahier fermé : G et F sont deux primitives de f sur I ; écris G(x) en fonction de F(x).
- après diapo 17 `pr_s2_b1` EXERCICE : F et G sont deux primitives de f sur un intervalle I. Alors : OPTIONS : ['G = F', 'G(x) = k · F(x), k ∈ ℝ', 'G(x) = F(x) + k, k ∈ ℝ']
- après diapo 19 `pr_s2_b1b` RETROUVER : Cahier fermé : comment trouve-t-on k avec la condition F(x₀) = y₀ ?
- après diapo 19 `pr_s2_b1b` EXERCICE : f(x) = 3x² sur ℝ : la primitive F telle que F(0) = 5 est : OPTIONS : ['F(x) = x³ + 5', 'F(x) = x³', 'F(x) = 3x³ + 5']
- après diapo 22 `pr_s2_b2` RETROUVER : Cahier fermé : écris une primitive de xⁿ (n ∈ ℕ*).
- après diapo 22 `pr_s2_b2` EXERCICE : Sachant que (x³)′ = 3x², une primitive de 3x² sur ℝ est : OPTIONS : ['6x', 'x³/3', 'x³']
- après diapo 24 `pr_s2_b3` RETROUVER : Cahier fermé : écris une primitive de 1/x² sur ]0 ; +∞[.
- après diapo 24 `pr_s2_b3` EXERCICE : Une primitive de 1/x³ sur ]0 ; +∞[ est : OPTIONS : ['−3/x⁴', '−1/(2x²)', '1/(2x²)']
- après diapo 27 `pr_s2_b3b` RETROUVER : Cahier fermé : écris une primitive de 1/√x sur ]0 ; +∞[.
- après diapo 27 `pr_s2_b3b` EXERCICE : Une primitive de 1/x² sur ]0 ; +∞[ est : OPTIONS : ['1/x', '−1/x', '−2/x³']
- après diapo 30 `pr_s3_b1` RETROUVER : Cahier fermé : écris la règle des primitives d'une somme et d'un produit par un réel α.
- après diapo 30 `pr_s3_b1` EXERCICE : Une primitive de sin(3x + 2) sur ℝ est : OPTIONS : ['−(1/3)cos(3x + 2)', '(1/3)cos(3x + 2)', '−3cos(3x + 2)']
- après diapo 33 `pr_s3_b2` RETROUVER : Cahier fermé : écris la dérivée de uⁿ.
- après diapo 33 `pr_s3_b2` EXERCICE : Les primitives de f(x) = (x + 1)² sur ℝ, après avoir développé, sont les fonctions : OPTIONS : ['x ↦ x³/3 + x² + x + k, k ∈ ℝ', 'x ↦ 2(x + 1) + k, k ∈ ℝ', 'x ↦ x³ + x² + x + k, k ∈ ℝ']
- après diapo 35 `pr_s3_b2b` RETROUVER : Cahier fermé : écris une primitive de u′uⁿ (n ∈ ℕ*).
- après diapo 35 `pr_s3_b2b` EXERCICE : Vrai ou faux ? OPTIONS : None
- après diapo 38 `pr_s3_b3` RETROUVER : Cahier fermé : quelle forme reconnais-tu quand la dérivée de la parenthèse est devant ? Écris sa primitive.
- après diapo 38 `pr_s3_b3` EXERCICE : f(x) = 2x(x² + 5)⁴ sur ℝ. Une primitive de f est : OPTIONS : ['(x² + 5)⁵/5', 'x²(x² + 5)⁵/5', '(x² + 5)⁵']
- après diapo 42 `pr_s4_b1` RETROUVER : Cahier fermé : écris une primitive de u′/u².
- après diapo 42 `pr_s4_b1` EXERCICE : Sur ]−1/2 ; +∞[, une primitive de f(x) = 1/√(2x + 1) est : OPTIONS : ['2√(2x + 1)', '√(2x + 1)', '(2x + 1)√(2x + 1)']
- après diapo 45 `pr_s4_b2` RETROUVER : Cahier fermé : écris une primitive de u′·cos u et une primitive de u′·sin u.
- après diapo 45 `pr_s4_b2` EXERCICE : Une primitive de f(x) = x·sin(3x²) sur ℝ est : OPTIONS : ['cos(3x²)/6', '−cos(3x²)/6', '−6cos(3x²)']
- après diapo 50 `pr_s4_b3` RETROUVER : Cahier fermé : que dit le signe de f sur les primitives de f ?
- après diapo 50 `pr_s4_b3` EXERCICE : Pour f(x) = x²(x³ + 1)⁴ sur ℝ, une primitive est : OPTIONS : ['(x³ + 1)⁵/5', '(x³ + 1)⁵/15', 'x³(x³ + 1)⁵/15']
- après diapo 56 `pr_s5_b1` RETROUVER : Cahier fermé : comment justifies-tu que f admet des primitives sur I ?
- après diapo 56 `pr_s5_b1` EXERCICE : Montre que G(x) = (x − 1)√x est une primitive de g(x) = (3x − 1)/(2√x) sur ]0 ; +∞[. Quelle expression de G′(x) écris-tu d'abord ? OPTIONS : ['G′(x) = √x + (x − 1)/(2√x)', 'G′(x) = 1/(2√x)', 'G′(x) = (x − 1)/(2√x)']
- après diapo 59 `pr_s5_b2` RETROUVER : Cahier fermé : écris une primitive de sin x (attention au signe).
- après diapo 59 `pr_s5_b2` EXERCICE : Vrai ou faux ? OPTIONS : None
