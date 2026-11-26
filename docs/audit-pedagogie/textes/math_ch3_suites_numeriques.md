# math_ch3_suites_numeriques — Suites numériques

## I. Une suite, ses termes ; arithmétique et géométrique

### Diapo 1 `su_ouverture_cours` — Suites numériques
VOIX (fr) : Bienvenue dans un nouveau cours : Suites numériques. Dans ce cours, nous allons apprendre les suites arithmétiques et géométriques, le raisonnement par récurrence, et comment trouver la limite d'une suite. Au national, il y a presque chaque année un exercice sur les suites, qui fait partie de l'analyse : cinquante-cinq pour cent de la note. Comment allons-nous travailler ? Tu écoutes bien, tu réponds aux questions au tableau, et quand le cours s'arrête, tu écris dans ton cahier. Allons-y !
ÉCRAN : On apprend : Suites arithmétiques et géométriques, récurrence, limites | Au bac : un exercice de suites presque chaque année | Écouter · répondre au tableau · écrire dans le cahier

### Diapo 2 `su_o1_questions` — La carte du chapitre : une liste de nombres et cinq questions
VOIX (fr) : Bienvenue dans le chapitre des suites numériques. Regarde en haut : une rangée de cases, u indice zéro, u indice un, u indice deux. Une suite, c'est une liste de nombres numérotés. Dans un exercice de suites, on te pose presque toujours les mêmes questions, dans le même ordre. Première question : une inégalité pour tout n, c'est la récurrence. Deuxième : est-ce que la suite monte ou descend, c'est le sens de variation. Troisième : a-t-elle une limite finie, est-elle convergente. Quatrième : la formule de u indice n, avec une suite auxiliaire. Cinquième : la limite. Et au national, il y a un exercice de suites dans chaque sujet.
ÉCRAN : Une suite : une liste de nombres numérotés u₀, u₁, u₂… | Au national, un exercice de suites dans chaque sujet. | Cinq questions, presque toujours dans cet ordre : récurrence, sens de variation, convergence, suite auxiliaire, limite.

### Diapo 3 `su_a1_liste` — Une suite, c'est une liste numérotée
VOIX (fr) : Regarde les cases numérotées zéro, un, deux, trois, quatre. Ces numéros, ce sont les rangs n. Dans la case zéro, on écrit dix-sept : u indice zéro égale dix-sept. Puis les autres cases se remplissent : seize virgule vingt-cinq, seize virgule zéro six, et ainsi de suite. Retiens : n, c'est le numéro de la case ; u indice n, c'est le nombre dedans. Et regarde toujours où commence n : parfois la première case est u un.
ÉCRAN : n : le rang, le numéro de la case. | uₙ : le terme de rang n, le nombre dans la case. | Exemple : u₀ = 17 ; u₁ = 16,25 ; u₂ = 16,06… | Regarde où commence n : u₀ si n ∈ ℕ, u₁ si n ∈ ℕ*. | Une suite qui commence au rang 1 se note (uₙ)ₙ≥₁ ou (uₙ)ₙ∈ℕ* ; au rang p : (uₙ)ₙ≥ₚ.

### Diapo 4 `su_a2_indice` — uₙ₊₁ n'est pas uₙ + 1
VOIX (fr) : Deux écritures qui se ressemblent. Regarde la case u indice n. La flèche jaune va vers la case d'à côté : u indice n plus un, le terme suivant ; le petit n plus un en bas change de case. La flèche orange reste sous la même case : u indice n, plus un ; le plus un en ligne change seulement la valeur. Exemple : si u deux égale cinq, u deux plus un égale six. Mais u trois, on ne le connaît pas sans la relation. Si u deux égale cinq, que vaut u deux plus un, et connaît-on u trois ?
ÉCRAN : uₙ₊₁ : le terme suivant (on change de case). | uₙ + 1 : la valeur de uₙ augmentée de 1 (même case). | u₂ = 5 donne u₂ + 1 = 6, mais pas u₃.
QUESTION : Si u₂ = 5, que vaut u₂ + 1 ? Connaît-on u₃ ? OPTIONS : ['u₂ + 1 = 6 et u₃ = 6, le terme qui suit u₂', 'u₂ + 1 = 6 ; u₃ est inconnu sans la relation', 'u₂ + 1 = u₃ (le + 1 change de case), donc u₃ = 6']

### Diapo 5 `su_a3_termes` — Une suite donnée par une formule en n
VOIX (fr) : Deux façons de donner une suite. La première : u indice n égale trois n plus deux, u indice n est écrite en fonction de n. On remplace n par zéro, on trouve deux ; par un, cinq. Chaque case se calcule seule, sans la précédente.
ÉCRAN : Suite explicite uₙ = f(n) : on remplace n par 0, 1, 2… | uₙ = 3n + 2 : u₀ = 2, u₁ = 5.

### Diapo 6 `su_a3b_recurrence` — Une suite par récurrence : la machine
VOIX (fr) : La deuxième façon : une suite définie par récurrence, u indice n plus un égale un quart u indice n plus douze. C'est une machine : u indice n entre, on multiplie par un quart, on ajoute douze, u indice n plus un sort. Dix-sept entre : u un égale seize virgule vingt-cinq. Puis la sortie revient à l'entrée : u deux, puis u trois. Ici, pas de u trois sans u deux.
ÉCRAN : uₙ₊₁ = ¼uₙ + 12 : on remplace uₙ par le terme qu'on connaît. | La sortie devient l'entrée suivante : u₁, puis u₂, puis u₃.

### Diapo 7 `su_a4_arithmetique` — Suite arithmétique : on ajoute toujours la même chose
VOIX (fr) : Regarde l'axe : u zéro égale deux, u un égale cinq, puis huit, onze, quatorze. Au-dessus, des arcs : à chaque pas, on ajoute trois. Le pas ne change jamais. Pour le montrer, on calcule u indice n plus un moins u indice n, et on trouve une constante. Ici trois. On écrit la phrase : donc la suite est arithmétique, de raison r égale trois.
ÉCRAN : On calcule uₙ₊₁ − uₙ. | Si c'est une constante r : (uₙ) est arithmétique de raison r. | Sur l'axe : des pas tous égaux.

### Diapo 8 `su_a5_terme_arith` — Le terme général d'une suite arithmétique
VOIX (fr) : Pour aller directement à la case n, sans calculer toutes les cases. La formule : u indice n égale u indice p plus, n moins p, fois r. Si le premier terme est u zéro, p égale zéro : u indice n égale u zéro plus n r. Si le premier terme est u un, p égale un : u indice n égale u un plus, n moins un, fois r. Exemple : u zéro égale deux, r égale trois, alors u indice n égale deux plus trois n. À toi : u un égale quatre, r égale trois. Écris u indice n.
QUESTION : u₁ = 4 et r = 3 : écris uₙ en fonction de n. OPTIONS : ['uₙ = 4 + 3n', 'uₙ = 3n + 1', 'uₙ = 3 + 4n']

### Diapo 9 `su_z1_puissances` — Rappel : les puissances
VOIX (fr) : Que veut dire q puissance n ? On multiplie q par lui-même, n fois. Deux puissance un, c'est deux. Deux puissance deux, deux fois deux, quatre. Deux puissance trois, deux fois deux fois deux, huit : à chaque fois le nombre de blocs double. Autrement : on recule. De huit à quatre, on divise par deux ; de quatre à deux, encore ; de deux, on trouve un. Donc deux puissance zéro égale un, pas zéro. D'où la règle : q puissance n plus un égale q puissance n fois q. Je relis : q puissance zéro égale un, et q puissance n plus un égale q puissance n fois q.
ÉCRAN : qⁿ = q × q × … × q (n facteurs). | q⁰ = 1 (et non 0). | qⁿ⁺¹ = qⁿ × q : une puissance de plus, une multiplication de plus.

### Diapo 10 `su_a6_geometrique` — Suite géométrique : on multiplie toujours par le même nombre
VOIX (fr) : Sur l'axe : cinq, dix, vingt, quarante. Regarde les arcs : on ne rajoute pas la même chose, on multiplie toujours par deux. Les pas grandissent. Pour le montrer, on écrit u indice n plus un et on cherche à faire apparaître q fois u indice n. On vise q fois u indice n, on ne calcule pas le quotient, parce qu'il faudrait que u indice n ne soit pas nul. Ici u indice n plus un égale deux u indice n : raison q égale deux. u indice n égale cinq fois deux puissance n : écris u indice n plus un en fonction de u indice n.
ÉCRAN : On écrit uₙ₊₁ et on fait apparaître q × uₙ. | Si uₙ₊₁ = q·uₙ : (uₙ) est géométrique de raison q. | On vise q fois uₙ, pas le quotient (il faudrait uₙ ≠ 0).

### Diapo 11 `su_a7_terme_geo` — Le terme général d'une suite géométrique
VOIX (fr) : La même idée pour une suite géométrique. La formule : u indice n égale u indice p fois q puissance n moins p. Si le premier terme est u zéro : u indice n égale u zéro fois q puissance n. Si c'est u un : u indice n égale u un fois q puissance n moins un. Et vérifie toujours ta formule avec n égale zéro : q puissance zéro égale un, pas zéro. Donc on retrouve bien u zéro. v zéro égale un demi et q égale un septième : écris v indice n, et calcule v zéro avec ta formule.

### Diapo 12 `su_a8_nombre_termes` — Combien de termes dans une somme ?
VOIX (fr) : Une question qui revient dans chaque somme : combien de termes ? Regarde ces arbres le long de la route, numérotés cinq, six, sept. Combien d'arbres ? Trois. Pourtant sept moins cinq égale deux. Il faut ajouter un : sept moins cinq plus un égale trois. La règle : de u indice p à u indice n, il y a n moins p plus un termes. Dernier moins premier, plus un. De u zéro à u deux mille vingt et un, deux mille vingt-deux termes.
ÉCRAN : De uₚ à uₙ : n − p + 1 termes. | Trois arbres numérotés 5, 6, 7 : 7 − 5 + 1 = 3. | De u₀ à u₂₀₂₁ : 2022 termes.

### Diapo 13 `su_a9_sommes` — La somme arithmétique
VOIX (fr) : Pour additionner beaucoup de termes sans tout écrire, on a des formules. D'abord la somme arithmétique : le nombre de termes fois, premier terme plus dernier terme, sur deux. Un plus deux jusqu'à dix : dix termes, premier un, dernier dix : dix fois onze sur deux, cinquante-cinq. Autrement : le premier avec le dernier, un plus dix, onze ; deux plus neuf, onze encore ; cinq paires, cinq fois onze, cinquante-cinq.
ÉCRAN : S = (nombre de termes) × (premier + dernier)/2. | 1 + 2 + … + 10 = 10 × 11/2 = 55. | La somme uₚ + uₚ₊₁ + … + uₙ se note aussi Σ uₖ, pour k allant de p à n.

### Diapo 14 `su_a9b_somme_geo` — La somme géométrique
VOIX (fr) : Maintenant la somme géométrique, avec q différent de un : le premier terme fois, un moins q puissance le nombre de termes, sur un moins q. Attention : la puissance, c'est le nombre de termes, pas le dernier indice. Calcule un plus deux plus quatre, jusqu'à deux puissance dix.
ÉCRAN : Géométrique (q ≠ 1) : S = (premier terme) × (1 − q puissance (nombre de termes))/(1 − q). | La puissance, c'est le nombre de termes. | En symboles : uₚ + … + uₙ = uₚ·(1 − qⁿ⁻ᵖ⁺¹)/(1 − q) ; 1 + q + q² + … + qⁿ = (1 − qⁿ⁺¹)/(1 − q).
QUESTION : Calcule 1 + 2 + 4 + … + 2¹⁰. OPTIONS : ['2¹⁰ − 1 = 1023', '2¹¹ = 2048', '2¹¹ − 1 = 2047']
## II. Le raisonnement par récurrence

### Diapo 15 `su_r1_dominos` — Les dominos : le principe de récurrence
VOIX (fr) : Pour montrer une propriété pour tout n, on ne peut pas vérifier les termes un par un, il y en a une infinité. Regarde la rangée de dominos. On pousse le premier : il tombe, c'est l'initialisation. Maintenant regarde un domino quelconque, numéro n : s'il tombe, il fait tomber le n plus un. C'est l'hérédité. Alors ils tombent tous, l'un après l'autre : c'est la conclusion. Deux choses à vérifier : le premier, et le passage d'un domino au suivant. Autrement : une échelle. Si tu peux monter sur le premier barreau, et si de chaque barreau tu peux monter au suivant, tu atteins n'importe quel barreau. Je relis : initialisation, hérédité, conclusion.
ÉCRAN : Initialisation : le premier domino tombe. | Hérédité : si un domino tombe, le suivant tombe. | Conclusion : tous les dominos tombent. | S'il manque un passage, la chaîne s'arrête.

### Diapo 16 `su_r2_trois_titres` — Les trois titres d'une récurrence : l'annonce et l'initialisation
VOIX (fr) : Avant de calculer, on écrit trois titres, un par un. On annonce : montrons par récurrence que pour tout n, u indice n est plus grand que seize. Premier titre, Initialisation : pour n égale zéro, u zéro égale dix-sept, plus grand que seize. La propriété est vraie au premier rang : c'est le premier domino qui tombe.
ÉCRAN : On annonce : montrons par récurrence que pour tout n ∈ ℕ, uₙ > 16. | Initialisation : on vérifie au premier rang (n = 0 : u₀ = 17 > 16).

### Diapo 17 `su_r2b_heredite` — Hérédité : supposer pour UN n, montrer au rang n + 1
VOIX (fr) : Deuxième titre, Hérédité : soit n. On suppose, pour ce n, u indice n plus grand que seize : c'est le joker, la seule carte qu'on a. Et la cible, en orange : montrons que u indice n plus un est plus grand que seize. Autrement : si le domino numéro n tombe, le suivant tombe-t-il ? C'est la question de l'hérédité.
ÉCRAN : Hérédité : soit n ∈ ℕ ; supposons uₙ > 16 (pour UN n). | Montrons que uₙ₊₁ > 16.

### Diapo 18 `su_r2c_conclusion` — Conclusion, et la phrase interdite
VOIX (fr) : Troisième titre, Conclusion : d'après le principe de récurrence, pour tout n, u indice n est plus grand que seize. Regarde la phrase barrée en bas : supposer pour tout n. C'est faux : on supposerait ce qu'on veut montrer. Dans l'hérédité, on suppose pour un seul n.
ÉCRAN : Conclusion : d'après le principe de récurrence, pour tout n ∈ ℕ, uₙ > 16. | Jamais « supposons que pour tout n » : c'est ce qu'on veut montrer.

### Diapo 19 `su_z2_ordre_garde` — Rappel : ce qui garde le sens d'une inégalité
VOIX (fr) : Une inégalité : deux nombres, l'un plus petit que l'autre. Sur l'axe, a égale un, avant b égale trois. On ajoute deux aux deux : un devient trois, trois devient cinq ; les deux ont bougé de la même distance, l'ordre reste : trois plus petit que cinq. On multiplie par deux, positif : deux et six, l'ordre ne change pas. Autrement : deux élèves dans une file ; s'ils avancent du même nombre de pas, le premier reste le premier. Je relis : on peut ajouter un même nombre, ou multiplier par un nombre positif, le sens de l'inégalité ne change pas.
ÉCRAN : a < b ⇒ a + c < b + c. | Si k > 0 : a < b ⇒ ka < kb.

### Diapo 20 `su_z3_ordre_inverse` — Rappel : ce qui change le sens d'une inégalité
VOIX (fr) : Deux cas où l'ordre se retourne. Premier cas : on multiplie par moins un. Un devient moins un, trois devient moins trois : le miroir en zéro les fait passer de l'autre côté. Moins trois est maintenant le plus petit : moins un est plus grand que moins trois. Deuxième cas : l'inverse de deux nombres positifs. Deux est plus petit que quatre, mais un demi est plus grand qu'un quart. Autrement : coupe un pain en deux, ou en quatre ; la grande part est celle du pain coupé en deux. Je relis : multiplier par un nombre négatif, ou passer à l'inverse de deux nombres positifs, change le sens de l'inégalité. Question : deux est plus petit que cinq ; on multiplie par moins trois : quelle inégalité obtient-on ?
ÉCRAN : Si k < 0 : a < b ⇒ ka > kb. | Si 0 < a < b : 1/a > 1/b.
QUESTION : On sait que 2 < 5. On multiplie les deux membres par −3 : quelle inégalité obtient-on ? OPTIONS : ['−6 < −15', '−6 > −15', '6 > 15']

### Diapo 21 `su_enonce_2016r` — National 2016 R : l’énoncé, tel qu’à l’examen
VOIX (fr) : Maintenant, nous allons lire l'énoncé de l'examen national deux mille seize, la session de rattrapage, tel qu'il est à l'examen. Exercice un, trois points. On considère la suite u n, définie par : u zéro égale deux, et u indice n plus un, égale un seizième u indice n, plus quinze seizièmes. Un a : montrer par récurrence, que u indice n est plus grand que un. Maintenant, comprenons cette question.

### Diapo 22 `su_r3_heredite_affine` — National 2016 R, exercice 1 : question 1-a, l'hérédité affine
VOIX (fr) : Comment passer de u indice n à u indice n plus un ? Question un a du national deux mille seize, rattrapage : l'hérédité. u indice n plus un égale un seizième u indice n plus quinze seizièmes : u indice n apparaît une seule fois. On part de l'hypothèse, u indice n plus grand que un. La formule multiplie par un seizième : on multiplie l'inégalité par un seizième, qui est positif, donc le sens ne change pas. Puis la formule ajoute quinze seizièmes : on les ajoute des deux côtés. On arrive à u indice n plus un plus grand que un. On fait à l'inégalité ce que la formule fait à u indice n, dans l'ordre.
ÉCRAN : 1-a : uₙ₊₁ = (1/16)uₙ + 15/16 : uₙ apparaît une seule fois. | On part de l'hypothèse et on applique les opérations de la formule, dans l'ordre. | Multiplier par un nombre positif garde le sens de l'inégalité.

### Diapo 23 `su_z4_difference` — Rappel : comparer avec le signe de la différence
VOIX (fr) : Pour comparer a et b, on calcule a moins b. a égale cinq, b égale deux : a moins b égale trois, positif, donc a est plus grand que b. a égale un, b égale quatre : a moins b égale moins trois, négatif, donc a est plus petit que b. Autrement : a moins b, c'est le chemin de b vers a, avec son signe ; positif, a est à droite de b. Dans ce chapitre : pour montrer que u indice n plus un est plus grand que un, on étudie le signe de u indice n plus un moins un. Je relis : a est plus grand que b si et seulement si a moins b est positif.
ÉCRAN : a − b > 0 ⇔ a > b. | a − b < 0 ⇔ a < b. | Dans le cours : uₙ₊₁ > 1 ⇔ uₙ₊₁ − 1 > 0.

### Diapo 24 `su_z5_denominateur` — Rappel : le même dénominateur
VOIX (fr) : Pour additionner deux fractions, il faut le même dénominateur. Un demi d'une barre, un tiers de la même barre : on ne peut pas les ajouter tout de suite, les parts n'ont pas la même taille. On coupe tout en six : un demi devient trois sixièmes, un tiers deux sixièmes ; ensemble, cinq sixièmes. Autrement, avec des lettres : quatre moins six sur un plus x. Quatre s'écrit quatre fois un plus x, sur un plus x ; on regroupe en haut : quatre x moins deux, sur un plus x. Je relis : pour additionner deux fractions, on les écrit avec le même dénominateur, puis on additionne les numérateurs.
ÉCRAN : 1/2 + 1/3 = 3/6 + 2/6 = 5/6. | 4 − 6/(1 + x) = (4(1 + x) − 6)/(1 + x) = (4x − 2)/(1 + x).

### Diapo 25 `su_r4_heredite_fraction` — Hérédité avec une fraction : pourquoi ça bloque, et l'idée
VOIX (fr) : Maintenant u indice n plus un égale quatre u indice n plus trois, sur trois u indice n plus quatre : u indice n est en haut et en bas. La ligne barrée : on peut encadrer le haut et le bas, mais on ne sait pas diviser deux inégalités. Ça ne marche pas. L'idée : montrer que u indice n plus un est plus grand que un, c'est montrer que u indice n plus un moins un est positif. C'est la règle qu'on vient de voir : on compare par le signe de la différence.
ÉCRAN : uₙ apparaît deux fois : on ne peut pas « diviser deux inégalités ». | Montrer uₙ₊₁ > 1, c'est montrer uₙ₊₁ − 1 > 0.

### Diapo 26 `su_r4b_calcul` — Le calcul : même dénominateur, puis deux signes
VOIX (fr) : Le calcul. Même dénominateur : il reste u indice n moins un, sur trois u indice n plus quatre. Signe du haut : positif, par l'hypothèse. Signe du bas : positif. Donc u indice n plus un moins un est positif. Question : avec une fraction comme celle-ci, qu'étudie-t-on pour montrer que u indice n plus un est plus grand que un ?
ÉCRAN : uₙ₊₁ − 1 = (uₙ − 1)/(3uₙ + 4). | uₙ − 1 > 0 (hypothèse) et 3uₙ + 4 > 0. | Donc uₙ₊₁ − 1 > 0 : uₙ₊₁ > 1.
QUESTION : u₀ = 3 et uₙ₊₁ = (4uₙ + 3)/(3uₙ + 4) : pour montrer uₙ₊₁ > 1 dans l'hérédité, on étudie : OPTIONS : ['le signe de uₙ₊₁ − 1', '4uₙ + 3 > 7, puis on divise par 3uₙ + 4 > 7', 'le quotient uₙ₊₁/uₙ']

### Diapo 27 `su_r5_choisir` — Choisir sa méthode d'hérédité
VOIX (fr) : Avant l'hérédité, regarde combien de fois u indice n apparaît dans la relation. Une fois, comme un quart u indice n plus douze : on fait les opérations sur l'hypothèse. Deux fois, comme une fraction avec u indice n en haut et en bas : on étudie le signe de u indice n plus un moins a. Et quand u indice n plus un égale f de u indice n, avec f croissante : on utilise f, on le verra plus loin. u indice n plus un égale trois u indice n moins huit, sur deux u indice n moins cinq.
ÉCRAN : Une fois (uₙ₊₁ = auₙ + b) : opérations sur l'hypothèse. | Deux fois (fraction) : signe de uₙ₊₁ − a. | uₙ₊₁ = f(uₙ) avec f croissante : f(a) ≤ f(uₙ) ≤ f(b) (on le verra plus loin).

### Diapo 28 `su_r6_ecriture_donnee` — Encadrement avec l'écriture donnée par l'énoncé
VOIX (fr) : Au national, on te demande souvent de vérifier une écriture. Ce n'est pas un calcul pour rien : c'est l'outil. u indice n plus un égale quatre u indice n moins deux, sur u indice n plus un. On vérifie : quatre moins six sur un plus u indice n, au même dénominateur, redonne u indice n plus un. Dans cette écriture, u indice n n'apparaît plus qu'une fois : on peut faire les opérations. Attention à deux pièges. Quand on passe à l'inverse de nombres positifs, l'ordre change. Et quand on multiplie par moins six, l'ordre change encore. u zéro égale quatre : tu as trois inférieur ou égal à un plus u indice n inférieur ou égal à cinq.
ÉCRAN : La question « vérifier » donne l'outil : uₙ n'apparaît plus qu'une fois. | On encadre pas à pas : 1 + uₙ, puis l'inverse, puis × (−6), puis + 4. | Passer à l'inverse (nombres positifs) ou multiplier par un négatif change l'ordre.

### Diapo 29 `su_r7_strict_large` — Strict ou large : ce que la conclusion doit dire
VOIX (fr) : Une petite question qui fait perdre des points. Si tu as trouvé u indice n plus un strictement plus petit que trois, alors il est aussi inférieur ou égal à trois. Le strict entraîne le large. Mais l'inverse est faux : inférieur ou égal n'entraîne pas strictement inférieur. Donc relis l'énoncé avant d'écrire ta conclusion. Et regarde l'erreur barrée : supposer supérieur ou égal, et conclure strictement supérieur, sans raison.
ÉCRAN : < entraîne ≤ : uₙ₊₁ < 3 donne uₙ₊₁ ≤ 3. | ≤ n'entraîne pas < . | Relis l'énoncé avant d'écrire la conclusion.

### Diapo 30 `su_enonce_2023r` — National 2023 R : l’énoncé, tel qu’à l’examen
VOIX (fr) : Maintenant, nous allons lire l'énoncé de l'examen national deux mille vingt-trois, la session de rattrapage, tel qu'il est à l'examen. Exercice un, trois points. On considère la suite u n, définie par u zéro égale zéro, et u indice n plus un, égale u indice n moins deux, sur deux u indice n plus cinq. Un : montrer que pour tout n, u indice n est plus grand que moins un. Maintenant, comprenons cette question.

### Diapo 31 `su_r8_national` — National 2023 R, exercice 1 : question 1 (à toi)
VOIX (fr) : À toi, avec la question un du national deux mille vingt-trois, rattrapage. u zéro égale zéro, et u indice n plus un égale u indice n moins deux, sur deux u indice n plus cinq. On demande de montrer que pour tout n, u indice n est plus grand que moins un. u indice n apparaît deux fois : on étudie le signe de u indice n plus un plus un. Et on écrit les trois titres : Initialisation, Hérédité, Conclusion. Prends ton cahier et rédige. Puis réponds : dans l'hérédité, u indice n plus un plus un égale quoi ?
ÉCRAN : National 2023 R : u₀ = 0, uₙ₊₁ = (uₙ − 2)/(2uₙ + 5). | Question 1 : montrer que pour tout n ∈ ℕ, uₙ > −1. | uₙ apparaît deux fois : signe de uₙ₊₁ + 1. | Initialisation · Hérédité · Conclusion.
QUESTION : Dans l'hérédité, uₙ₊₁ + 1 = ? OPTIONS : ['(uₙ − 1)/(2uₙ + 5)', '3(uₙ + 1)/(2uₙ + 5)', '3(uₙ + 1)/(uₙ + 5)']
## III. Majorée, minorée, bornée ; sens de variation

### Diapo 32 `su_b1_plancher` — Majorée, minorée : un plafond, un plancher
VOIX (fr) : Voici les points de la suite u indice n égale seize plus un quart puissance n, dans un repère : n en abscisse, u indice n en ordonnée. Les points sont isolés, on ne les relie pas. Regarde la droite verte y égale seize : aucun point dessous. C'est un plancher : pour tout n, u indice n supérieur ou égal à seize, la suite est minorée par seize. La droite orange y égale dix-sept : aucun point au-dessus. C'est un plafond : la suite est majorée par dix-sept. Minorée et majorée : elle est bornée.
ÉCRAN : Minorée par m : pour tout n, uₙ ≥ m (un plancher). | Majorée par M : pour tout n, uₙ ≤ M (un plafond). | Bornée : minorée et majorée. | On écrit aussi « ∀n ∈ ℕ » pour « pour tout n ∈ ℕ ». | Sur le graphique, les points (n ; uₙ) sont isolés : on ne les relie pas.

### Diapo 33 `su_b2_bornee` — Bornée : coincée entre deux
VOIX (fr) : Une autre suite : u indice n égale cinq n carré sur n carré plus deux. Regarde les points : zéro, un virgule six, trois virgule trois, et ils montent vers cinq sans jamais l'atteindre. La droite orange y égale cinq est un plafond jamais touché : u indice n strictement plus petit que cinq. La droite verte y égale zéro : u indice n positif. Coincée entre les deux : la suite est bornée. Pour le montrer par le calcul, on étudie le signe de u indice n moins cinq.
ÉCRAN : Bornée : il existe m et M avec m ≤ uₙ ≤ M pour tout n. | Pour montrer uₙ < 5 : étudier le signe de uₙ − 5. | Le plafond y = 5 peut ne jamais être atteint. | Exemples : −1 ≤ (−1)ⁿ ≤ 1 et −1 ≤ cos n ≤ 1 : ces deux suites sont bornées.

### Diapo 34 `su_m1_pour_tout_n` — Croissante, décroissante : pour tout n
VOIX (fr) : Regarde seulement deux points : u zéro égale deux, u un égale trois. La flèche monte. Est-ce que la suite est croissante ? Attends. Voici les points suivants : deux virgule cinq, deux, un virgule cinq… ils redescendent. Donc u un plus grand que u zéro, et pourtant la suite n'est pas croissante. Croissante, c'est u indice n plus un supérieur ou égal à u indice n, pour tout n, pas seulement au début. Si u indice n plus un est strictement plus grand que u indice n pour tout n, la suite est strictement croissante ; strictement plus petit : strictement décroissante ; égal pour tout n : la suite est constante. u zéro égale deux et u un égale trois : la suite est-elle forcément croissante ?
ÉCRAN : Croissante : pour tout n, uₙ₊₁ ≥ uₙ. | Décroissante : pour tout n, uₙ₊₁ ≤ uₙ. | Strictement croissante : ∀n, uₙ₊₁ > uₙ ; strictement décroissante : ∀n, uₙ₊₁ < uₙ ; constante : ∀n, uₙ₊₁ = uₙ. | u₁ > u₀ ne suffit pas : une suite peut monter puis redescendre.
QUESTION : u₀ = 2 et u₁ = 3 : la suite est-elle forcément croissante ? OPTIONS : ['Oui, car u₁ > u₀ : le premier pas monte', 'Non : il faut uₙ₊₁ ≥ uₙ pour tout n', 'Oui, si en plus u₂ > u₁ (trois termes qui montent)']
EXERCICE : Pour montrer qu'une suite est décroissante, il faut : OPTIONS : ['calculer u₁ − u₀ et vérifier que u₁ − u₀ ≤ 0', 'montrer uₙ ≤ u₀ pour tout n ∈ ℕ', 'montrer uₙ₊₁ − uₙ ≤ 0 pour tout n']

### Diapo 35 `su_enonce_2016r_p2` — National 2016 R : la suite de l’énoncé
VOIX (fr) : Même exercice du national deux mille seize : la suite u n, avec u indice n plus un, égale un seizième u indice n, plus quinze seizièmes. Voici la suite de l'énoncé. Un b : vérifier que u indice n plus un, moins u indice n, égale moins quinze seizièmes, fois u indice n moins un, puis montrer que la suite est décroissante. Maintenant, comprenons cette question.

### Diapo 36 `su_m2_difference` — National 2016 R, exercice 1 : question 1-b, le signe de uₙ₊₁ − uₙ
VOIX (fr) : Premier outil pour le sens de variation : le signe de u indice n plus un moins u indice n. Question un b du national deux mille seize, rattrapage : on remplace u indice n plus un par la formule et on soustrait u indice n. On factorise : moins quinze seizièmes, fois u indice n moins un. Et le signe ? On l'a déjà : la récurrence a montré u indice n plus grand que un, donc u indice n moins un est positif. Avec le moins devant, la différence est négative : la suite est décroissante.
ÉCRAN : 1-b : uₙ₊₁ − uₙ = −(15/16)(uₙ − 1) : on calcule, on factorise. | On lit son signe avec ce qu'on a prouvé par récurrence. | uₙ₊₁ − uₙ ≥ 0 : croissante ; ≤ 0 : décroissante.

### Diapo 37 `su_m3_egalite_donnee` — Outil 1 avec une égalité donnée
VOIX (fr) : Au national, l'énoncé fait souvent le calcul pour toi. Ici on te donne : u indice n plus un moins u indice n égale, u indice n moins un, fois deux moins u indice n, sur un plus u indice n. Il reste à lire le signe. On sait déjà, par la récurrence, que u indice n est entre deux et quatre. Alors on écrit un signe sous chaque facteur, puis le signe du tout.
ÉCRAN : L'énoncé donne uₙ₊₁ − uₙ déjà factorisé. | Un signe sous chaque facteur, tiré de l'encadrement 2 ≤ uₙ ≤ 4. | Puis le signe du tout, et la phrase de conclusion.

### Diapo 38 `su_m4_quotient` — Outil 2 : le quotient, si les termes sont positifs
VOIX (fr) : Deuxième outil : le quotient u indice n plus un sur u indice n, comparé à un. Mais d'abord la condition, en jaune : tous les termes doivent être strictement positifs. Si le quotient est inférieur ou égal à un, on multiplie par u indice n, positif : u indice n plus un inférieur ou égal à u indice n, la suite est décroissante. S'il est supérieur ou égal à un : croissante. Attention, si u indice n est négatif, multiplier par u indice n change l'ordre. u indice n positif et u indice n plus un sur u indice n inférieur ou égal à un demi : que conclus-tu ?
ÉCRAN : Seulement si uₙ > 0 pour tout n. | uₙ₊₁/uₙ ≤ 1 : décroissante ; uₙ₊₁/uₙ ≥ 1 : croissante. | Si uₙ < 0, multiplier par uₙ change l'ordre.
QUESTION : uₙ > 0 pour tout n et uₙ₊₁/uₙ ≤ 1/2 : que conclus-tu ? OPTIONS : ['(uₙ) est strictement croissante, car uₙ > 0', 'On ne peut rien dire sans le signe de uₙ₊₁ − uₙ', '(uₙ) est strictement décroissante']
## IV. La suite auxiliaire

### Diapo 39 `su_x1_pourquoi` — Pourquoi une suite auxiliaire ?
VOIX (fr) : Avec u indice n plus un égale un quart u indice n plus douze, on calcule les termes un par un, mais on n'a pas de formule de u indice n en fonction de n. Regarde la colonne u indice n : dix-sept, seize virgule vingt-cinq, seize virgule zéro six. Rien de simple. Maintenant la colonne v indice n égale u indice n moins seize : un, zéro virgule vingt-cinq, zéro virgule zéro six. Regarde les flèches vertes : chaque terme est le quart du précédent. v indice n est géométrique, on connaît sa formule. C'est un détour : v indice n fait le travail, u indice n en profite.
ÉCRAN : uₙ₊₁ = ¼uₙ + 12 ne donne pas uₙ en fonction de n. | vₙ = uₙ − 16 : chaque vₙ est le quart du précédent. | vₙ est géométrique, on connaît sa formule, et uₙ = vₙ + 16.

### Diapo 40 `su_enonce_2016r_p3` — National 2016 R : la suite de l’énoncé
VOIX (fr) : Même exercice du national deux mille seize : la suite u n, avec u zéro égale deux, et u indice n plus un, égale un seizième u indice n, plus quinze seizièmes. Voici la suite de l'énoncé. Deux : soit v n la suite, telle que v indice n, égale u indice n moins un. a : montrer que v n est géométrique, de raison un seizième, puis écrire v indice n en fonction de n. Maintenant, comprenons cette question.

### Diapo 41 `su_x2_geometrique` — National 2016 R, exercice 1 : question 2-a, vₙ est géométrique
VOIX (fr) : Question deux a du national deux mille seize, rattrapage : comment montrer que v indice n est géométrique ? On écrit la cible en haut : v indice n plus un égale q fois v indice n. Puis on part de la définition au rang n plus un : v indice n plus un égale u indice n plus un moins un. On remplace u indice n plus un par la relation de l'énoncé. On simplifie, on factorise, et on voit apparaître v indice n : un seizième fois v indice n. On ne calcule pas le quotient : on vise q fois v indice n. Puis v zéro égale u zéro moins un, égale un : donc v indice n égale un seizième puissance n.
ÉCRAN : 2-a : la cible : vₙ₊₁ = q × vₙ. | On écrit vₙ₊₁ avec la définition, on remplace uₙ₊₁ par la relation. | On simplifie jusqu'à voir vₙ, sans calculer de quotient.

### Diapo 42 `su_enonce_2016n` — National 2016 N : l’énoncé, tel qu’à l’examen
VOIX (fr) : Maintenant, nous allons lire l'énoncé de l'examen national deux mille seize, la session normale, tel qu'il est à l'examen. Exercice un, deux points et demi. On considère la suite u n, définie par u zéro égale deux, et u indice n plus un, égale trois plus u indice n, sur cinq moins u indice n. Deux : soit v n la suite définie par, v indice n égale u indice n moins un, sur trois moins u indice n. a : montrer que v n est géométrique, de raison un demi, puis en déduire, que v indice n égale un demi puissance n. b : montrer que u indice n égale, un plus trois v indice n, sur un plus v indice n, puis écrire u indice n en fonction de n. Maintenant, comprenons l'exercice, question par question.

### Diapo 43 `su_x3_fraction` — National 2016 N, exercice 1 : question 2-a, une suite auxiliaire en fraction
VOIX (fr) : Question deux a du national deux mille seize, session normale : v indice n est une fraction : u indice n moins un, sur trois moins u indice n. Et u indice n plus un égale trois plus u indice n, sur cinq moins u indice n. On écrit v indice n plus un avec la définition. On remplace u indice n plus un en haut et en bas. Chaque morceau se met au même dénominateur : cinq moins u indice n. Et la règle en orange : a sur b, divisé par c sur b, égale a sur c. Les dénominateurs se simplifient. On vise un demi fois v indice n. Après simplification, v indice n plus un égale quoi ?
ÉCRAN : 2-a : on remplace uₙ₊₁ en haut et en bas. | On met chaque morceau au même dénominateur 5 − uₙ. | (a/b)/(c/b) = a/c : les dénominateurs se simplifient.
QUESTION : Après simplification, vₙ₊₁ = ? OPTIONS : ['(8uₙ − 8)/(12 − 4uₙ), soit 2vₙ', '(uₙ − 1)/(3 − uₙ) = vₙ', '(2uₙ − 2)/(12 − 4uₙ) = (1/2)vₙ']

### Diapo 44 `su_x4_retour` — De vₙ à uₙ : le cas simple
VOIX (fr) : On revient à u indice n. Le cas simple : v indice n égale u indice n moins seize. On ajoute seize des deux côtés : u indice n égale v indice n plus seize. Et comme v indice n égale un quart puissance n, u indice n égale seize plus un quart puissance n. C'est la formule qu'on cherchait.
ÉCRAN : D'abord v₀, puis vₙ = v₀·qⁿ. | vₙ = uₙ − 16 : uₙ = vₙ + 16 = 16 + (¼)ⁿ.

### Diapo 45 `su_x4b_fraction` — National 2016 N, exercice 1 : question 2-b, revenir à uₙ
VOIX (fr) : Question deux b du national deux mille seize : revenir à u indice n quand v indice n est une fraction. Ici v indice n égale u indice n moins un, sur trois moins u indice n. Produit en croix, puis tous les u indice n du même côté, on factorise u indice n et on divise : u indice n égale un plus trois v indice n, sur un plus v indice n. Il reste à remplacer v indice n par un demi puissance n : u indice n égale un plus trois fois un demi puissance n, sur un plus un demi puissance n.
ÉCRAN : 2-b : produit en croix : vₙ(3 − uₙ) = uₙ − 1. | Tous les uₙ du même côté, puis on factorise uₙ. | uₙ = (1 + 3vₙ)/(1 + vₙ) = (1 + 3(½)ⁿ)/(1 + (½)ⁿ).

### Diapo 46 `su_enonce_2021n` — National 2021 R : l’énoncé, tel qu’à l’examen
VOIX (fr) : Maintenant, nous allons lire l'énoncé de l'examen national deux mille vingt et un, la session de rattrapage, tel qu'il est à l'examen. Exercice un, quatre points. Soit u n la suite définie par, u zéro égale un tiers, et u indice n plus un, égale un plus u indice n, sur trois moins u indice n. Trois a : on pose v indice n, égale un sur, un moins u indice n. Montrer que v n est une suite arithmétique, et déterminer sa raison, et son premier terme. Maintenant, comprenons cette question.

### Diapo 47 `su_x5_arithmetique` — National 2021 R, exercice 1 : question 3-a, une suite auxiliaire arithmétique
VOIX (fr) : La suite auxiliaire n'est pas toujours géométrique. Deux natures, deux calculs. Arithmétique : on calcule la différence v indice n plus un moins v indice n, et on trouve une constante r. Géométrique : on trouve v indice n plus un égale q fois v indice n. Question trois a du national deux mille vingt et un, rattrapage : v indice n égale un sur un moins u indice n, et le calcul donne une différence égale à un demi. Donc arithmétique, de raison un demi : v indice n égale v zéro plus n r. v indice n plus un moins v indice n égale un demi et v zéro égale trois demis : écris v indice n.
ÉCRAN : Arithmétique : vₙ₊₁ − vₙ = r (constante). | Géométrique : vₙ₊₁ = q × vₙ. | Arithmétique : vₙ = v₀ + nr.
## V. Limites d'une suite

### Diapo 48 `su_l1_converge` — Une suite qui se rapproche d'un nombre
VOIX (fr) : Regarde l'axe et le pointillé jaune en seize. Les termes se placent un à un : dix-sept, seize virgule vingt-cinq, seize virgule zéro six… Ils se serrent vers seize, de plus en plus près. On dit que la suite converge vers seize, et on écrit : la limite de u indice n égale seize. Une suite qui a une limite finie est convergente. Sinon, si elle part vers l'infini ou n'a pas de limite, elle est divergente. Ces termes se rapprochent de quel nombre ?
ÉCRAN : Les termes se serrent autant qu'on veut autour de 16 : lim_{n→+∞} uₙ = 16. | Convergente : elle a une limite finie. | Divergente : sinon (limite infinie, ou pas de limite). | Autrement dit : tout intervalle ouvert de centre 16 contient tous les termes à partir d'un certain rang. | Limite infinie : lim_{n→+∞} uₙ = −∞ ⇔ lim_{n→+∞} (−uₙ) = +∞.
QUESTION : Les termes 17 ; 16,25 ; 16,06 ; 16,02… se rapprochent de quel nombre ? OPTIONS : ['17', '0', '16']

### Diapo 49 `su_l2_reference` — Les suites de référence : nᵅ
VOIX (fr) : Trois suites de référence sur le même repère. En cyan, n carré : zéro, un, quatre, et elle sort tout de suite par le haut, vers plus l'infini. En vert, racine de n : elle monte lentement, mais elle monte sans fin, vers plus l'infini aussi. En orange, un sur n : un, un demi, un tiers… elle tombe vers zéro. La règle, à droite : la limite de n puissance alpha est plus l'infini si alpha est positif, zéro si alpha est négatif. Un sur racine de n, c'est n puissance moins un demi.
ÉCRAN : lim_{n→+∞} n = lim_{n→+∞} n² = lim_{n→+∞} √n = +∞. | lim_{n→+∞} 1/n = lim_{n→+∞} 1/n² = lim_{n→+∞} 1/√n = 0. | lim_{n→+∞} nᵅ = +∞ si α > 0 ; lim_{n→+∞} nᵅ = 0 si α < 0. | 1/√n = n^(−1/2) : α = −1/2 < 0, donc lim_{n→+∞} 1/√n = 0.

### Diapo 50 `su_l3_qn_positif` — qⁿ quand q est entre 0 et 1, puis plus grand que 1
VOIX (fr) : Les puissances d'un nombre q. En cyan, q égale un demi : un, zéro virgule cinq, zéro virgule vingt-cinq… Chaque multiplication par un demi coupe en deux ce qui reste : les points tombent vers zéro. En orange, q égale deux : un, deux, quatre, huit, ça grossit sans fin et ça sort du tableau, vers plus l'infini. En vert, q égale un : tous les points restent à un. Le bilan est écrit à droite.
ÉCRAN : 0 < q < 1 : lim_{n→+∞} qⁿ = 0 (chaque fois, on garde une fraction de ce qui reste). | q > 1 : lim_{n→+∞} qⁿ = +∞. | q = 1 : qⁿ = 1.

### Diapo 51 `su_l4_qn_negatif` — qⁿ quand q est négatif
VOIX (fr) : Et si q est négatif ? Les termes changent de signe à chaque pas. En cyan, q égale moins un demi : un, moins zéro virgule cinq, zéro virgule vingt-cinq, moins zéro virgule cent vingt-cinq. Regarde bien où vont les points. Les sauts rapetissent, les points se rapprochent de zéro : même avec q négatif, la limite est zéro. En vert, q égale moins un : un, moins un, un, moins un… pas de limite. En orange, q égale moins deux : les sauts grandissent, pas de limite. Ce qui compte : q strictement entre moins un et un.
ÉCRAN : q = −1/2 : les termes changent de signe, les sauts rapetissent. | q = −1 : 1, −1, 1, −1… pas de limite. | q = −2 : les sauts grandissent, pas de limite.
OBSERVATION : q = −1/2 : où vont les points quand n grandit ?

### Diapo 52 `su_l4c_quatre_cas` — Les quatre cas de qⁿ
VOIX (fr) : On range tout dans un tableau, quatre cas. Premier : q strictement entre moins un et un, la limite de q puissance n est zéro, même si q est négatif. Deuxième : q égale un, la limite est un. Troisième : q plus grand que un, plus l'infini. Quatrième : q inférieur ou égal à moins un, pas de limite. Moins un tiers puissance n a-t-elle une limite ? Et moins deux puissance n ?
ÉCRAN : −1 < q < 1 : lim_{n→+∞} qⁿ = 0. | q = 1 : lim_{n→+∞} qⁿ = 1. | q > 1 : lim_{n→+∞} qⁿ = +∞. | q ≤ −1 : (qⁿ) n'a pas de limite.
QUESTION : (−1/3)ⁿ a-t-elle une limite ? Et (−2)ⁿ ? OPTIONS : ['(−1/3)ⁿ → 0 ; (−2)ⁿ → −∞', "Aucune des deux n'a de limite", "(−1/3)ⁿ → 0 ; (−2)ⁿ n'a pas de limite"]

### Diapo 53 `su_l4b_glisse_q` — Glisse q : le bon cas en un coup d'œil
VOIX (fr) : À toi de jouer avec q. En haut à droite, une règle de q, de moins deux à deux. La zone jaune, c'est q strictement entre moins un et un. Le rond bleu est sur q égale zéro virgule cinq : les points tombent vers zéro, et le cas s'écrit dans le cadre. Glisse le rond : dans la zone jaune, toujours zéro. À un : un. Après un : plus l'infini. À moins un ou avant : pas de limite.
ÉCRAN : La règle de q : la zone jaune −1 < q < 1. | Dans la zone : lim_{n→+∞} qⁿ = 0. | À −1 ou à gauche : pas de limite ; à droite de 1 : +∞.

### Diapo 54 `su_l5_avec_qn` — Limite d'une suite écrite avec qⁿ
VOIX (fr) : Maintenant la suite a une formule : u indice n égale seize plus un quart puissance n. On écrit la phrase complète. D'abord la condition : car un quart est strictement entre moins un et un. Alors la limite de un quart puissance n égale zéro. Puis les opérations : la limite de u indice n égale seize plus zéro, seize. Retiens : on écrit toujours la condition avant la limite. u indice n égale un plus un sur, un moins deux tiers puissance n plus un : calcule la limite de u indice n.
ÉCRAN : On écrit d'abord la condition : « car −1 < ¼ < 1 ». | Puis lim_{n→+∞} (¼)ⁿ = 0. | Puis les opérations sur les limites.

### Diapo 55 `su_l5b_formes_indeterminees` — Opérations sur les limites et formes indéterminées
VOIX (fr) : Les opérations sur les limites des suites suivent les mêmes règles que pour les fonctions. Exemple : moins cinq fois quatre puissance n. Quatre est plus grand que un, donc quatre puissance n tend vers plus l'infini ; moins cinq est négatif, donc le produit tend vers moins l'infini. Mais il y a quatre cas où les règles ne donnent pas la réponse : les formes indéterminées. Plus l'infini moins l'infini, zéro fois l'infini, l'infini sur l'infini, et zéro sur zéro. Exemple : deux puissance n moins trois puissance n. Les deux tendent vers plus l'infini : forme indéterminée. L'idée : on factorise par la plus grande puissance, trois puissance n. On obtient trois puissance n, fois, deux tiers puissance n moins un. Comme deux tiers est strictement entre moins un et un, deux tiers puissance n tend vers zéro, et la parenthèse tend vers moins un. Trois puissance n tend vers plus l'infini. Donc la limite est moins l'infini. Autrement : trois puissance n grandit beaucoup plus vite que deux puissance n. Pour n égale dix : deux puissance dix, mille vingt-quatre ; trois puissance dix, cinquante-neuf mille quarante-neuf. La différence est négative et très grande. Je relis : dans une forme indéterminée, on factorise par la plus grande puissance.
ÉCRAN : Somme, produit, quotient : mêmes règles que pour les fonctions (chapitre « Limites »). | Exemple : 4 > 1, donc lim_{n→+∞} 4ⁿ = +∞ ; −5 < 0, donc lim_{n→+∞} (−5 × 4ⁿ) = −∞. | Quatre formes indéterminées : « +∞ − ∞ », « 0 × ∞ », « ∞/∞ », « 0/0 » : on change l'écriture. | 2ⁿ − 3ⁿ (« +∞ − ∞ ») : on factorise par la plus grande puissance : 2ⁿ − 3ⁿ = 3ⁿ((2/3)ⁿ − 1). | −1 < 2/3 < 1, donc (2/3)ⁿ − 1 → −1 ; 3 > 1, donc 3ⁿ → +∞ ; donc lim_{n→+∞} (2ⁿ − 3ⁿ) = −∞.

### Diapo 56 `su_l6_fraction` — Limite d'une fraction en n
VOIX (fr) : Regarde les points de u indice n égale n plus un sur n plus trois : zéro virgule trente-trois, zéro virgule cinq, zéro virgule six… Ils montent de moins en moins, et se serrent sous la droite jaune y égale un. Pour le calcul : on factorise par n en haut et en bas. Il reste un plus un sur n, sur un plus trois sur n. Un sur n tend vers zéro, donc la fraction tend vers un sur un.
ÉCRAN : On factorise par n en haut et en bas. | 1/n → 0 et 3/n → 0. | lim_{n→+∞} (n + 1)/(n + 3) = 1/1 = 1. | Polynôme en n (« +∞ − ∞ ») : n² − 5n + 1 = n²(1 − 5/n + 1/n²) → +∞ : même limite que n².

### Diapo 57 `su_l7_f_un` — La limite de f(uₙ)
VOIX (fr) : Deux axes. En haut, les termes u indice n se serrent vers deux. Des flèches descendent de chaque u indice n vers son image par f de x égale racine de x plus sept. En bas, les images se serrent vers racine de neuf, trois. La règle encadrée : si u indice n tend vers a et f est continue en a, alors f de u indice n tend vers f de a. La limite de u indice n égale deux, et v indice n égale racine de u indice n plus sept : quelle est la limite de v indice n ?
ÉCRAN : Si lim_{n→+∞} uₙ = a et f est continue en a, alors lim_{n→+∞} f(uₙ) = f(a). | Exemple : uₙ → 2 et f(x) = √(x + 7) continue en 2 : f(uₙ) → √9 = 3.
QUESTION : lim uₙ = 2 et vₙ = √(uₙ + 7) : lim vₙ = ? OPTIONS : ['3', '√2', '9']
## VI. Convergence et comparaison

### Diapo 58 `su_c1_plafond` — Monter avec un plafond, c'est converger
VOIX (fr) : Regarde les points : un, deux virgule deux, deux virgule neuf… la suite monte. Au-dessus, la droite orange y égale cinq : un plafond. Aucun point ne passe au-dessus : la suite est majorée par cinq. Elle monte, mais elle ne peut pas traverser le plafond : alors elle se tasse sous un nombre, ici quatre, en pointillé jaune. Elle converge. Et regarde les points gris : n carré monte aussi, mais sans plafond, elle part vers plus l'infini.
ÉCRAN : Une suite croissante monte ; majorée, elle ne traverse pas son plafond. | Elle se tasse sous un nombre ℓ : elle converge. | Sans plafond, elle peut partir vers +∞ (exemple : n²).
OBSERVATION : Les points montent sans traverser y = 5. Que font-ils quand n grandit ?

### Diapo 59 `su_c2_couple` — Le bon couple : monte + plafond, descend + plancher
VOIX (fr) : Deux images en miroir. À gauche, une suite qui monte sous un plafond : croissante et majorée. À droite, une suite qui descend au-dessus d'un plancher : décroissante et minorée. Les deux convergent : le plafond freine celle qui monte, le plancher freine celle qui descend. Attention au mauvais couple, écrit en rouge : une suite croissante a déjà un plancher, son premier terme. Croissante et minorée, ça ne dit rien de nouveau. Exemple : n carré.
ÉCRAN : Croissante et majorée : convergente. | Décroissante et minorée : convergente. | Croissante et minorée : on ne peut rien conclure (exemple : n²).

### Diapo 60 `su_c3_plafond_limite` — Le plafond n'est pas forcément la limite
VOIX (fr) : Ici la suite monte, sous un plafond orange : y égale six. Elle est majorée par six. Mais regarde où elle se tasse : sous quatre, en jaune. Le plafond, ce n'est pas la limite. Si tu glisses le plafond à huit, ou à cinq, la suite est toujours majorée, et sa limite reste quatre. Le théorème dit seulement qu'elle converge, pas vers quoi. Règle importante : si la suite converge et si tous les termes sont entre a et b, la limite aussi est entre a et b. C'est le passage à la limite. Attention : l'inégalité stricte devient large. Exemple : un sur n est strictement positif, mais sa limite est zéro.
ÉCRAN : Le théorème dit que la suite converge, pas vers quoi. | Si elle converge, une suite majorée par M a une limite ℓ ≤ M, souvent plus petite. | La limite se calcule ensuite (formule, ou ℓ = f(ℓ)). | Passage à la limite : si (uₙ) converge vers ℓ et a ≤ uₙ ≤ b pour tout n (ou à partir d'un certain rang), alors a ≤ ℓ ≤ b. | ⚠ Une inégalité stricte devient large : 1/n > 0, mais lim_{n→+∞} 1/n = 0.

### Diapo 61 `su_c4_comparaison` — Coincée entre deux : le critère de comparaison
VOIX (fr) : Trois rangées de points. En bas, en vert : zéro. En haut, en orange : trois demis fois deux cinquièmes puissance n, qui descend vers zéro. Entre les deux, en cyan, notre suite. Elle a deux camarades, un de chaque côté, et les deux vont vers zéro. Coincée entre eux, elle va vers zéro aussi : les flèches se resserrent. C'est le critère de comparaison : si v indice n inférieur ou égal à u indice n, inférieur ou égal à w indice n, et v et w ont la même limite, alors u indice n a cette limite. Même idée avec l'infini : si u indice n est inférieur ou égal à v indice n, et que v indice n tend vers moins l'infini, alors u indice n tend vers moins l'infini. Et ces inégalités peuvent n'être vraies qu'à partir d'un certain rang. Zéro plus petit que u indice n, inférieur ou égal à un sur n : quelle est la limite de u indice n ?
ÉCRAN : Critère de comparaison (théorème des gendarmes) : vₙ ≤ uₙ ≤ wₙ et lim_{n→+∞} vₙ = lim_{n→+∞} wₙ = ℓ ⇒ lim_{n→+∞} uₙ = ℓ. | |uₙ − ℓ| ≤ vₙ et lim_{n→+∞} vₙ = 0 ⇒ lim_{n→+∞} uₙ = ℓ. | uₙ ≥ vₙ et lim_{n→+∞} vₙ = +∞ ⇒ lim_{n→+∞} uₙ = +∞ ; uₙ ≤ vₙ et lim_{n→+∞} vₙ = −∞ ⇒ lim_{n→+∞} uₙ = −∞. | Il suffit que les inégalités soient vraies à partir d'un certain rang. | Exemples : −1/n ≤ (−1)ⁿ/n ≤ 1/n, donc lim_{n→+∞} (−1)ⁿ/n = 0 ; n² + (−1)ⁿ ≥ n² − 1, donc lim_{n→+∞} (n² + (−1)ⁿ) = +∞.
QUESTION : 0 < uₙ ≤ 1/n pour tout n ≥ 1 : lim uₙ = ? OPTIONS : ['On ne peut pas savoir', '1', '0']

### Diapo 62 `su_enonce_2020n` — National 2020 N : l’énoncé, tel qu’à l’examen
VOIX (fr) : Maintenant, nous allons lire l'énoncé de l'examen national deux mille vingt, la session normale, tel qu'il est à l'examen. Exercice un, quatre points. Soit u n la suite définie par, u zéro égale trois demis, et u indice n plus un, égale deux u indice n, sur deux u indice n plus cinq. Trois a : montrer que u indice n plus un, est entre zéro, et deux cinquièmes de u indice n, puis en déduire que u indice n, est plus petit que trois demis, fois deux cinquièmes puissance n. b : calculer la limite de u n. Maintenant, comprenons l'exercice, question par question.

### Diapo 63 `su_c5_deux_cinquiemes` — National 2020 N, exercice 1 : question 3-a, 0 < uₙ₊₁ ≤ (2/5)uₙ
VOIX (fr) : Question trois a du national deux mille vingt, session normale : u indice n plus un égale deux u indice n, sur deux u indice n plus cinq, avec u indice n positif. On veut montrer que chaque terme est au plus les deux cinquièmes du précédent. Première méthode : minorer le dénominateur. Deux u indice n plus cinq est plus grand que cinq, donc un sur, deux u indice n plus cinq, est plus petit que un cinquième. Deuxième méthode : le signe de u indice n plus un moins deux cinquièmes u indice n.
ÉCRAN : 3-a (2020 N) : uₙ₊₁ = 2uₙ/(2uₙ + 5) et uₙ > 0. | Minorer le dénominateur : 2uₙ + 5 ≥ 5. | Ou étudier le signe de uₙ₊₁ − (2/5)uₙ.

### Diapo 64 `su_c6_recurrence_kn` — National 2020 N, exercice 1 : question 3-a (suite), en déduire uₙ ≤ (3/2)(2/5)ⁿ
VOIX (fr) : Question trois a, deuxième partie : en déduire. Comment passer de chaque terme au plus les deux cinquièmes du précédent, à une formule au rang n ? Regarde : u un inférieur ou égal à deux cinquièmes u zéro. Puis u deux inférieur ou égal à deux cinquièmes u un. Et ce u un, on le remplace par ce qu'on sait déjà de lui : on recolle. On obtient deux cinquièmes au carré, u zéro. Puis au cube pour u trois. Au rang n : deux cinquièmes puissance n, u zéro, c'est-à-dire trois demis fois deux cinquièmes puissance n. Mais cette image n'est pas une preuve : la preuve propre est une récurrence.
ÉCRAN : On recolle : u₁ ≤ (2/5)u₀, u₂ ≤ (2/5)²u₀… (l'image). | La preuve propre : une récurrence courte. | « En déduire » après uₙ₊₁ ≤ k·uₙ, c'est une récurrence.

### Diapo 65 `su_c7_conclure` — National 2020 N, exercice 1 : question 3-b, la limite par comparaison
VOIX (fr) : Question trois b : calculer la limite de u indice n. On a l'encadrement : zéro plus petit que u indice n, inférieur ou égal à trois demis fois deux cinquièmes puissance n. Regarde les deux bornes. En haut, en orange : car deux cinquièmes est strictement entre moins un et un, la limite de deux cinquièmes puissance n égale zéro. En bas, en vert : zéro. Les deux bornes vont vers zéro, les flèches se resserrent : d'après le critère de comparaison, la limite de u indice n égale zéro.
ÉCRAN : La borne du haut : comme −1 < 2/5 < 1, lim_{n→+∞} (3/2)(2/5)ⁿ = 0. | La borne du bas : 0. | 3-b : les deux bornes tendent vers 0 : d'après le critère de comparaison, lim_{n→+∞} uₙ = 0.

### Diapo 66 `su_enonce_2025r` — National 2025 R : l’énoncé, tel qu’à l’examen
VOIX (fr) : Maintenant, nous allons lire l'énoncé de l'examen national deux mille vingt-cinq, la session de rattrapage, tel qu'il est à l'examen. Exercice un, trois points. On considère la suite u n définie par, u zéro égale trois demis, et u indice n plus un, égale trois u indice n plus deux, sur deux plus u indice n. Deux d : déduire que deux moins u indice n, est plus petit que un demi, fois deux septièmes puissance n. e : déterminer la limite de la suite. Maintenant, comprenons l'exercice, question par question.

### Diapo 67 `su_c8_ecart` — National 2025 R, exercice 1 : question 2-e, l'écart à la limite se resserre
VOIX (fr) : Question deux e du national deux mille vingt-cinq, rattrapage : une autre forme du critère. La droite jaune, c'est la limite deux. Les points montent sous elle. Pour chaque n, le trait orange montre l'écart permis, deux moins u indice n : il est de plus en plus petit. Car un demi fois deux septièmes puissance n tend vers zéro. Si l'écart à deux tend vers zéro, la suite tend vers deux. Zéro plus petit que deux moins u indice n, inférieur ou égal à un demi fois deux septièmes puissance n : calcule la limite de u indice n.
ÉCRAN : 2-d (donné) : l'écart 2 − uₙ est coincé entre 0 et (1/2)(2/7)ⁿ. | Comme −1 < 2/7 < 1, la borne tend vers 0. | 2-e : donc 2 − uₙ → 0 : lim_{n→+∞} uₙ = 2.
QUESTION : 0 < 2 − uₙ ≤ (1/2)(2/7)ⁿ : lim uₙ = ? OPTIONS : ['2', '0', '2/7']
## VII. La suite uₙ₊₁ = f(uₙ)

### Diapo 68 `su_f1_escalier` — Voir les termes sur la courbe : l'escalier
VOIX (fr) : Une suite définie par u indice n plus un égale f de u indice n, avec f de x égale deux x sur x plus un. On peut voir ses termes sur le dessin. En cyan, la courbe de f ; en blanc, la droite y égale x. On place u zéro égale deux sur l'axe des abscisses. On monte jusqu'à la courbe : on lit f de u zéro, c'est u un. On va horizontalement jusqu'à la droite y égale x. On redescend sur l'axe : u un est placé. La droite sert à reporter la valeur sur l'axe. Et on recommence : u deux, u trois. Les marches se tassent.
ÉCRAN : uₙ₊₁ = f(uₙ), f(x) = 2x/(x + 1), u₀ = 2. | De u₀, on monte à la courbe : f(u₀) = u₁. | On va à la droite y = x, on redescend sur l'axe : u₁ est placé. | On recommence : les marches se tassent vers le point (1 ; 1).

### Diapo 69 `su_f2_place_u0` — La place de u₀ change l'escalier
VOIX (fr) : Le dessin aide aussi à deviner. Le point orange, c'est u zéro : tu peux le glisser sur l'axe. À deux, l'escalier descend vers un. Si tu le glisses à gauche de un, l'escalier change : il monte, toujours vers le point un un. Et si u zéro égale un : tous les termes valent un. C'est la place de u zéro par rapport au point où la courbe coupe la droite qui décide. Le dessin donne une conjecture ; la preuve, c'est la récurrence et le théorème.
ÉCRAN : u₀ > 1 : l'escalier descend vers 1. | 0 < u₀ < 1 : l'escalier monte vers 1. | u₀ = 1 : tous les termes valent 1. | Le dessin aide à conjecturer ; la preuve reste la récurrence et le théorème.

### Diapo 70 `su_f3_encadrement_f` — L'encadrement vient des variations de f
VOIX (fr) : Pour la récurrence avec une fonction, on utilise ses variations. Regarde la courbe de f, croissante. En vert, l'intervalle de un à deux sur l'axe des abscisses. On projette : f de un égale un, f de deux égale quatre tiers. Rappel : une fonction croissante garde l'ordre ; si a est plus petit que b, alors f de a est plus petit que f de b. u zéro égale deux : dans l'hérédité de un inférieur ou égal à u indice n inférieur ou égal à deux, que donne f croissante ?
ÉCRAN : f(x) = 2x/(x + 1) est croissante sur [1 ; 2] (f′(x) = 2/(x + 1)² > 0). | 1 ≤ uₙ ≤ 2 donne f(1) ≤ f(uₙ) ≤ f(2), soit 1 ≤ uₙ₊₁ ≤ 4/3. | f est continue et strictement croissante sur [1 ; 2], donc f([1 ; 2]) = [f(1) ; f(2)] = [1 ; 4/3]. | Et [1 ; 4/3] ⊂ [1 ; 2] : f(I) ⊂ I.
QUESTION : u₀ = 2 : dans l'hérédité de 1 ≤ uₙ ≤ 2, que donne f croissante ? OPTIONS : ['f(1) ≤ f(uₙ) ≤ f(2), soit 1 ≤ uₙ₊₁ ≤ 4/3', 'f(2) ≤ uₙ₊₁ ≤ f(1)', '1 ≤ uₙ₊₁ ≤ 2 directement, sans f']

### Diapo 71 `su_f4_sens_f` — Le sens de variation vient de f(x) − x
VOIX (fr) : Le sens de variation se lit sur le dessin. Au-dessus de l'intervalle de un à deux, la bande en orange : la courbe est sous la droite y égale x. Donc f de x inférieur ou égal à x. Et regarde l'escalier depuis deux : chaque marche descend. Par le calcul : f de x moins x est négatif sur cet intervalle, et tous les u indice n y sont, grâce à la récurrence. Donc u indice n plus un, qui est f de u indice n, est inférieur ou égal à u indice n. Attention : f est croissante, et pourtant la suite décroît.
ÉCRAN : Sur [1 ; 2], la courbe de f est sous la droite y = x : f(x) ≤ x. | Tous les uₙ sont dans [1 ; 2] (récurrence). | Donc uₙ₊₁ = f(uₙ) ≤ uₙ : la suite est décroissante. | f croissante n'oblige pas la suite à croître.

### Diapo 72 `su_f5_conditions` — Les conditions avant ℓ = f(ℓ)
VOIX (fr) : Avant d'écrire l égale f de l, on pose les conditions, une à une, comme des ingrédients sur la table. Un : la suite est convergente, on note l sa limite. Deux : f est continue sur l'intervalle I, de un à deux, car elle est dérivable sur I. Trois : f de I est inclus dans I. f est continue et strictement croissante, donc f de I est l'intervalle de f de un à f de deux, c'est-à-dire de un à quatre tiers, inclus dans I. Quatre : u zéro est dans I. Alors seulement : l est solution de l'équation f de x égale x dans I. Sans une de ces conditions, le correcteur refuse.
ÉCRAN : (uₙ) est convergente ; on note ℓ sa limite. | f est continue sur I = [1 ; 2] car elle est dérivable sur I (fonction rationnelle, x + 1 ≠ 0). | f(I) ⊂ I : f est continue et strictement croissante sur I, donc f(I) = [f(1) ; f(2)] = [1 ; 4/3] ⊂ I. | u₀ = 2 ∈ I. | Alors ℓ est solution de l'équation f(x) = x dans I. Sans une de ces conditions, la réponse n'est pas acceptée.

### Diapo 73 `su_f6_choisir` — Choisir la bonne solution
VOIX (fr) : L'équation f de x égale x a deux solutions. Sur le dessin, la courbe coupe la droite en deux points : zéro zéro, en rouge, et un un, en vert. Laquelle est la limite ? Regarde l'intervalle en vert : tous les termes sont entre un et deux, donc la limite aussi. Zéro n'est pas dans l'intervalle : on le barre. La limite est un. Une erreur vue dans une vidéo : choisir zéro.
ÉCRAN : f(x) = x ⇔ x = 0 ou x = 1. | Pour tout n, 1 ≤ uₙ ≤ 2 ; par passage à la limite, 1 ≤ ℓ ≤ 2. | 0 ∉ [1 ; 2], donc ℓ = 1.

### Diapo 74 `su_f7_national` — À toi : la suite du problème du national, étape 1 : le sens de variation
VOIX (fr) : À toi, avec la fin d'un problème du national. g de x égale quatre x plus trois, sur x plus deux. u zéro égale un, et u indice n plus un égale g de u indice n. On a déjà montré que tous les termes sont entre un et trois. Première étape : le sens de variation. Regarde la courbe de g et la droite y égale x. On calcule g de x moins x, au même dénominateur. Puis on factorise le haut : trois moins x, fois x plus un, sur x plus deux. Le tableau de signes est prêt, sur l'intervalle de un à trois. Question : quel est le signe de g de x moins x, et que fait la suite ?
ÉCRAN : g(x) = (4x + 3)/(x + 2), u₀ = 1, uₙ₊₁ = g(uₙ) ; on a montré 1 ≤ uₙ ≤ 3. | g(x) − x = (−x² + 2x + 3)/(x + 2) = (3 − x)(x + 1)/(x + 2). | Le signe de chaque facteur sur [1 ; 3], puis celui de g(x) − x.
QUESTION : Sur [1 ; 3], g(x) − x = (3 − x)(x + 1)/(x + 2) et 1 ≤ uₙ ≤ 3. Que conclus-tu ? OPTIONS : ['g(x) − x ≤ 0 : (uₙ) est décroissante', 'g(x) − x ≥ 0 : (uₙ) est croissante', 'g(x) − x ≥ 0 : (uₙ) est décroissante']

### Diapo 75 `su_f7b_limite` — À toi : la suite du problème du national, étape 2 : la limite
VOIX (fr) : Deuxième étape : la limite. La suite est croissante, et majorée par trois : donc elle est convergente. On appelle l sa limite. Maintenant, les conditions, une par une. g est continue sur l'intervalle de un à trois, car elle est dérivable. g est croissante, donc l'image de l'intervalle va de g de un à g de trois : de sept tiers à trois. Elle reste dans l'intervalle. Et u zéro égale un, dans l'intervalle. Donc l égale g de l, avec l entre un et trois. Question : combien vaut l ?
ÉCRAN : (uₙ) est croissante et majorée par 3 : elle est convergente ; ℓ sa limite. | g est continue sur I = [1 ; 3] car elle est dérivable sur I (x + 2 ≠ 0). | g′(x) = 5/(x + 2)² > 0 : g(I) = [g(1) ; g(3)] = [7/3 ; 3] ⊂ I ; u₀ = 1 ∈ I. | Donc ℓ = g(ℓ) et ℓ ∈ [1 ; 3].
QUESTION : ℓ = g(ℓ) et ℓ ∈ [1 ; 3], avec g(x) − x = (3 − x)(x + 1)/(x + 2). lim uₙ = ? OPTIONS : ['1', '−1', '3']
## VIII. Problèmes : rang, somme ; un exercice national question par question

### Diapo 76 `su_p1_rang` — À partir de quel rang ?
VOIX (fr) : Une question de problème : à partir de quel rang la suite dépasse un seuil ? On remplace u indice n par sa formule : n plus un sur n plus trois, supérieur ou égal à quatre-vingt-dix-neuf centièmes. Les dénominateurs sont positifs, donc on peut faire le produit en croix. On développe, on regroupe : n supérieur ou égal à cent quatre-vingt-dix-sept. n est un entier : le plus petit qui convient est cent quatre-vingt-dix-sept.
ÉCRAN : On remplace uₙ par sa formule et on résout l'inéquation. | Dénominateurs positifs : on peut faire le produit en croix. | n est un entier : on prend le plus petit entier qui convient.

### Diapo 77 `su_enonce_2022r` — National 2022 R : l’énoncé, tel qu’à l’examen
VOIX (fr) : Maintenant, nous allons lire l'énoncé de l'examen national deux mille vingt-deux, la session de rattrapage, tel qu'il est à l'examen. Exercice un, deux points et demi. Soit u n la suite définie par, u zéro égale deux, et u indice n plus un, égale racine de deux sur deux, u indice n, plus, deux moins racine de deux, sur deux. Deux c : calculer la somme S, égale u zéro, plus u un, plus u deux, jusqu’à u deux mille vingt et un. Maintenant, comprenons cette question.

### Diapo 78 `su_p2_somme_mixte` — National 2022 R, exercice 1 : question 2-c, la somme S
VOIX (fr) : Question deux c du national deux mille vingt-deux, rattrapage : u indice n égale un plus v indice n, avec v géométrique. La somme des u n'est pas géométrique. Regarde la colonne : chaque terme est un plus v. On sépare. Les un, entourés en vert : il y en a autant que de termes, deux mille vingt-deux. Les v, réunis par l'accolade jaune : c'est une somme géométrique. Donc la somme égale deux mille vingt-deux, plus la somme des v. Avec v zéro égale un et la raison racine de deux sur deux : S égale deux mille vingt-deux, plus, un moins racine de deux sur deux puissance deux mille vingt-deux, sur un moins racine de deux sur deux.
ÉCRAN : 2-c (2022 R) : uₖ = 1 + vₖ : on sépare les 1 et les vₖ. | Autant de 1 que de termes : n − p + 1. | Les vₖ forment une somme géométrique.

### Diapo 79 `su_p3_limite_somme` — La limite d'une somme
VOIX (fr) : Une somme de plus en plus longue peut avoir une limite finie. Exemple : w zéro égale un, raison un demi. S indice n, c'est w zéro plus jusqu'à w indice n, avec n plus un termes. La formule : un fois, un moins un demi puissance n plus un, sur un moins un demi. Car un demi est strictement entre moins un et un, la puissance tend vers zéro. Donc la limite de S indice n égale un sur un moins un demi, deux. On étudie toujours la limite de la somme S indice n. Raison un tiers et w zéro égale un : quelle est la limite de S indice n ?
QUESTION : (wₙ) géométrique de raison 1/3, w₀ = 1, Sₙ = w₀ + … + wₙ : lim Sₙ = ? OPTIONS : ['3', '3/2', '+∞']

### Diapo 80 `su_enonce_2024n` — National 2024 N : l’énoncé, tel qu’à l’examen
VOIX (fr) : Maintenant, nous allons lire l'énoncé de l'examen national deux mille vingt-quatre, la session normale, tel qu'il est à l'examen. Exercice un, trois points. On considère la suite u n, définie par, u zéro égale quatre, et u indice n plus un, égale quatre u indice n moins deux, sur un plus u indice n. Un b : montrer par récurrence, que u indice n est entre deux et quatre. Deux a : montrer que u indice n plus un moins u indice n, égale u indice n moins un, fois deux moins u indice n, sur un plus u indice n. b : montrer que la suite est décroissante, et en déduire qu’elle est convergente. Maintenant, comprenons l'exercice, question par question.

### Diapo 81 `su_e1_complet` — National 2024 N, exercice 1 : question 1-b, l'encadrement par récurrence
VOIX (fr) : Un exercice du national deux mille vingt-quatre, joué question par question. u zéro égale quatre, et u indice n plus un égale quatre u indice n moins deux, sur u indice n plus un. Question un b : montrer par récurrence que u indice n est entre deux et quatre. Initialisation : u zéro égale quatre, il est entre deux et quatre. Hérédité : on suppose deux inférieur ou égal à u indice n, inférieur ou égal à quatre. On calcule u indice n plus un moins deux : on trouve deux fois, u indice n moins deux, sur u indice n plus un. Question : quel est le signe de cette différence ?
ÉCRAN : National 2024 N : u₀ = 4, uₙ₊₁ = (4uₙ − 2)/(1 + uₙ). | 1-b : montrer par récurrence que 2 ≤ uₙ ≤ 4. | Hérédité : uₙ₊₁ − 2 = 2(uₙ − 2)/(1 + uₙ) : son signe ?
QUESTION : Si 2 ≤ uₙ ≤ 4, le signe de uₙ₊₁ − 2 = 2(uₙ − 2)/(uₙ + 1) est : OPTIONS : ['négatif', 'positif ou nul', 'on ne peut pas savoir']

### Diapo 82 `su_e1_q2` — National 2024 N, exercice 1 : questions 2-a et 2-b, le sens de variation
VOIX (fr) : Question deux a : montrer l'égalité donnée. On calcule u indice n plus un moins u indice n. Au même dénominateur, on trouve moins u indice n au carré, plus trois u indice n, moins deux, sur un plus u indice n. Et c'est bien u indice n moins un, fois deux moins u indice n, sur un plus u indice n. Question deux b : le sens de variation. On sait, par la question un b, que u indice n est entre deux et quatre. Question : la suite est-elle croissante ou décroissante ?
ÉCRAN : 2-a : uₙ₊₁ − uₙ = (−uₙ² + 3uₙ − 2)/(1 + uₙ) = (uₙ − 1)(2 − uₙ)/(1 + uₙ). | 2-b : avec 2 ≤ uₙ ≤ 4 (1-b) : croissante ou décroissante ?
QUESTION : uₙ₊₁ − uₙ = −(uₙ − 1)(uₙ − 2)/(uₙ + 1) et 2 ≤ uₙ ≤ 4. La suite (uₙ) est : OPTIONS : ['croissante', 'décroissante', 'ni croissante ni décroissante']

### Diapo 83 `su_e1_q3` — National 2024 N, exercice 1 : question 2-b (fin), la convergence
VOIX (fr) : Question deux b, la fin : en déduire que la suite est convergente. Regarde les termes de notre suite sur le repère. Ils descendent : on vient de le montrer, la suite est décroissante. Et la droite verte, y égale deux : tous les points restent au-dessus. C'est la question un b : u indice n est plus grand que deux, la suite est minorée par deux. Question : que peut-on dire de la suite ?
ÉCRAN : 1-b : uₙ ≥ 2 (minorée). | 2-b : décroissante. | 2-b, fin : donc ?
QUESTION : (uₙ) est décroissante et minorée par 2. Donc : OPTIONS : ['(uₙ) est convergente', 'lim uₙ = −∞', 'on ne peut rien dire']

### Diapo 84 `su_enonce_2024n_p2` — National 2024 N : la suite de l’énoncé
VOIX (fr) : Même exercice du national deux mille vingt-quatre : la suite u n, avec u zéro égale quatre, et u indice n plus un, égale quatre u indice n moins deux, sur un plus u indice n. Voici la suite de l'énoncé. Trois : soit v n la suite définie par, v indice n égale deux moins u indice n, sur un moins u indice n. a : montrer que v n est une suite géométrique, de raison deux tiers. b : montrer que u indice n égale un, plus un sur, un moins deux tiers, puissance n plus un. c : calculer la limite de la suite. Maintenant, comprenons l'exercice, question par question.

### Diapo 85 `su_e1_q4` — National 2024 N, exercice 1 : question 3-a, la suite auxiliaire
VOIX (fr) : Question trois a : la suite auxiliaire. L'énoncé pose v indice n égale deux moins u indice n, sur un moins u indice n. On remplace u indice n plus un par sa formule, au même dénominateur : deux moins u indice n plus un égale deux fois, deux moins u indice n, sur un plus u indice n. Et un moins u indice n plus un égale trois fois, un moins u indice n, sur un plus u indice n. Question : v indice n plus un égale quoi ?
ÉCRAN : 3-a : vₙ = (2 − uₙ)/(1 − uₙ). | On calcule : 2 − uₙ₊₁ = 2(2 − uₙ)/(1 + uₙ) ; 1 − uₙ₊₁ = 3(1 − uₙ)/(1 + uₙ). | vₙ₊₁ = ?
QUESTION : Question 4 : vₙ₊₁ = ? (avec uₙ₊₁ − 2 = 2(uₙ − 2)/(uₙ + 1) et uₙ₊₁ − 1 = 3(uₙ − 1)/(uₙ + 1)) OPTIONS : ['(2/3)vₙ', '(3/2)vₙ', 'vₙ + 2/3']

### Diapo 86 `su_e1_q5a` — National 2024 N, exercice 1 : question 3-b, uₙ en fonction de n
VOIX (fr) : Question trois b : montrer la formule de u indice n. D'abord v indice n : v zéro égale deux moins u zéro, sur un moins u zéro : deux moins quatre, sur un moins quatre, deux tiers. La suite v est géométrique de raison deux tiers. Donc v indice n égale v zéro fois deux tiers puissance n : deux tiers puissance n plus un. Maintenant, il faut revenir à u indice n. On part de v indice n égale deux moins u indice n, sur un moins u indice n. Question : u indice n égale quoi ?
ÉCRAN : 3-b : vₙ = (2 − uₙ)/(1 − uₙ), (vₙ) géométrique de raison 2/3 (3-a). | v₀ = (2 − 4)/(1 − 4) = 2/3 ; vₙ = v₀ × (2/3)ⁿ = (2/3)ⁿ⁺¹. | On isole uₙ : uₙ = ?
QUESTION : vₙ = (uₙ − 2)/(uₙ − 1). On isole uₙ : uₙ = ? OPTIONS : ['(2 − vₙ)/(1 − vₙ)', '(1 − vₙ)/(2 − vₙ)', '(2 + vₙ)/(1 + vₙ)']

### Diapo 87 `su_e1_q5` — National 2024 N, exercice 1 : question 3-c, la limite
VOIX (fr) : Question trois c : la limite. On a trouvé u indice n égale un, plus un sur, un moins v indice n. Et v indice n égale deux tiers puissance n plus un : regarde ses points, ils descendent vers l'axe. La raison deux tiers est strictement entre moins un et un. Question : quelle est la limite de u indice n ?
ÉCRAN : 3-c : uₙ = 1 + 1/(1 − vₙ) et vₙ = (2/3)ⁿ⁺¹. | −1 < 2/3 < 1. | lim uₙ = ?
QUESTION : Question 5 : lim uₙ = ? OPTIONS : ['1', '4', '2']
## IX. Bilan du chapitre

### Diapo 88 `su_e2_bilan` — Ce qu'il faut retenir
VOIX (fr) : Faisons le bilan sur une seule fiche, et écris avec moi. Un : arithmétique et géométrique. u indice n égale u indice p plus, n moins p, fois r ; u indice n égale u indice p fois q puissance n moins p. Attention, q puissance zéro égale un. Deux : la récurrence, trois titres, Initialisation, Hérédité, Conclusion. Trois : je relis, une suite est majorée par M, si pour tout n, u indice n est inférieur ou égal à M. Quatre : le sens de variation, le signe de u indice n plus un moins u indice n. Cinq : la suite auxiliaire, on vise q fois v indice n. Six : les limites, la limite de q puissance n est zéro quand q est strictement entre moins un et un. Sept : une suite croissante et majorée est convergente. Huit : u indice n plus un égale f de u indice n, l égale f de l, avec les conditions. Neuf : le plus petit rang et la somme. La deuxième page est la tienne : ce qu'il te reste à retravailler.
ÉCRAN : 1. Arithmétique : uₙ₊₁ − uₙ = r, uₙ = uₚ + (n − p)r. Géométrique : uₙ₊₁ = q·uₙ, uₙ = uₚ·qⁿ⁻ᵖ. ⚠ q⁰ = 1 ; de uₚ à uₙ : n − p + 1 termes. | 2. Récurrence : Initialisation, Hérédité (supposons pour UN n, montrons au rang n + 1), Conclusion « d'après le principe de récurrence ». ⚠ uₙ une fois : opérations ; deux fois : signe de uₙ₊₁ − a. | 3. Majorée par M : pour tout n, uₙ ≤ M ; minorée par m : uₙ ≥ m ; bornée : les deux. ⚠ « pour tout n ». | 4. Sens de variation : signe de uₙ₊₁ − uₙ ; uₙ₊₁/uₙ comparé à 1 si uₙ > 0 ; strictement croissante : uₙ₊₁ > uₙ, constante : uₙ₊₁ = uₙ. ⚠ Deux termes ne suffisent pas. | 5. Suite auxiliaire : vₙ₊₁ = q·vₙ (ou vₙ₊₁ − vₙ = r), vₙ en fonction de n, puis uₙ. ⚠ On vise q·vₙ. | 6. Limites : lim qⁿ = 0 si −1 < q < 1 ; +∞ si q > 1 ; pas de limite si q ≤ −1. lim nᵅ. lim f(uₙ) = f(a) si f continue en a. Formes indéterminées : on factorise. ⚠ La condition avant la limite. | 7. Croissante et majorée, ou décroissante et minorée ⇒ convergente. Critère de comparaison (gendarmes). Passage à la limite : a ≤ uₙ ≤ b ⇒ a ≤ ℓ ≤ b. ⚠ Croissante et minorée : rien ; le plafond n'est pas forcément la limite. | 8. uₙ₊₁ = f(uₙ) : f continue sur I (car dérivable sur I), f(I) ⊂ I (f([a ; b]) = [f(a) ; f(b)] si f est continue et strictement croissante), u₀ ∈ I, (uₙ) convergente ⇒ ℓ = f(ℓ). ⚠ Garder la solution qui est dans I. | 9. Problèmes : plus petit rang (inéquation, n entier) ; somme géométrique : la puissance est le nombre de termes. | Page 2, ta page : ce qu'il te reste à retravailler, d'après tes réponses du cours (repris en mode libre).

### Diapo 89 `su_e3_carte` — La carte du chapitre
VOIX (fr) : Dessinons la carte de tout le chapitre, en une seule image. Au centre : la suite numérique, une liste de nombres numérotés. Première branche : arithmétique et géométrique, les rappels. Deuxième branche : la récurrence, et les suites majorées, minorées, bornées. Troisième branche : le sens de variation. Quatrième branche : la suite auxiliaire, le premier chemin vers la formule de u indice n. Cinquième branche : les limites, q puissance n et n puissance alpha. Sixième branche : convergence et comparaison. Septième branche : u indice n plus un égale f de u indice n, le deuxième chemin vers la limite. Et la dernière branche : les problèmes, le rang et la somme. Voilà la carte du chapitre. Les branches entourées en rouge, ce sont celles qu'on va reprendre ensemble.
ÉCRAN : Au centre : la suite numérique (uₙ). | Arithmétique, géométrique ; récurrence et bornes ; sens de variation. | Suite auxiliaire ; limites (qⁿ, nᵅ, f(uₙ)) ; convergence et comparaison. | uₙ₊₁ = f(uₙ) et ℓ = f(ℓ) ; problèmes : rang et somme.

### Diapo 90 `su_fermeture_cours` — Ce qu'il faut retenir, et comment réviser
VOIX (fr) : Nous arrivons à la fin du cours : Suites numériques. Que faut-il retenir ? Trois idées. Première : le raisonnement par récurrence : initialisation, hérédité, conclusion. Deuxième : une suite géométrique : u n égale u p fois q puissance n moins p. Troisième : une suite croissante et majorée, ou décroissante et minorée, est convergente. Maintenant quelques conseils pour réviser. Relis ton cahier, et refais seul les exercices du national. Quand tu réponds, écris chaque étape, et chaque résultat avec sa justification, car chaque étape a ses points. Le jour de l'examen, partage ton temps, et commence par la question qui te paraît facile. La veille, dors bien. Écris ces conseils dans ton cahier. Tu as bien travaillé, bon courage ! Le prochain cours : Fonctions primitives. On s'y retrouve !
ÉCRAN : Retenir : Récurrence · uₙ = uₚ·qⁿ⁻ᵖ · monotone et bornée ⇒ convergente | Réviser : relire le cahier, refaire les exercices du national | Rédiger : chaque étape, et sa justification (car…) | Jour J : gérer son temps · bien dormir la veille

## Questions de bloc (posées après la dernière diapo du bloc)
- après diapo 4 `su_n1_b1` RETROUVER : Cahier fermé : écris ce qu'est une suite (uₙ), avec les mots « rang » et « terme ».
- après diapo 4 `su_n1_b1` EXERCICE : uₙ = 1/n est définie pour n ∈ ℕ* : quel est son premier terme ? OPTIONS : ['u₁ = 1', 'u₀', 'u₂ = 1/2']
- après diapo 8 `su_n1_b2` RETROUVER : Cahier fermé : écris le terme général d'une suite arithmétique (uₙ) de raison r, en fonction de uₚ.
- après diapo 8 `su_n1_b2` EXERCICE : (uₙ) est une suite arithmétique de raison r = 3 et u₂ = 7. Calcule u₁₀. OPTIONS : None
- après diapo 11 `su_n1_b3` RETROUVER : Cahier fermé : écris uₙ en fonction de n pour une suite géométrique de premier terme u₀ et de raison q.
- après diapo 11 `su_n1_b3` EXERCICE : (uₙ) géométrique, u₀ = 3 et q = 2 : u₄ = ? OPTIONS : ['24', '48', '11']
- après diapo 14 `su_n1_b4` RETROUVER : Cahier fermé : écris la somme uₚ + … + uₙ de termes consécutifs d'une suite arithmétique.
- après diapo 14 `su_n1_b4` EXERCICE : (uₙ) est géométrique de premier terme u₀ = 3 et de raison 2. La somme u₀ + u₁ + u₂ + u₃ + u₄ vaut… OPTIONS : ['45', '93', '96']
- après diapo 17 `su_n2_b1` RETROUVER : Cahier fermé : énonce le principe de récurrence avec ses trois étapes.
- après diapo 17 `su_n2_b1` EXERCICE : Vrai ou faux ? OPTIONS : None
- après diapo 20 `su_n2_b2` RETROUVER : Cahier fermé : on multiplie une inégalité par un nombre négatif. Que devient son sens ?
- après diapo 20 `su_n2_b2` EXERCICE : Que vaut 5⁰ ? OPTIONS : ['0', '1', '5']
- après diapo 24 `su_n2_b3` RETROUVER : Cahier fermé : écris ce qu'est une suite (uₙ), avec les mots « rang » et « terme ».
- après diapo 24 `su_n2_b3` EXERCICE : uₙ = 1/n est définie pour n ∈ ℕ* : quel est son premier terme ? OPTIONS : ['u₁ = 1', 'u₀', 'u₂ = 1/2']
- après diapo 27 `su_n2_b4` RETROUVER : Cahier fermé : uₙ apparaît deux fois dans la relation (fraction). Que fait-on, dans l'hérédité, pour montrer uₙ₊₁ > a ?
- après diapo 27 `su_n2_b4` EXERCICE : uₙ₊₁ = 3uₙ − 2. Hérédité de « uₙ > 2 » : quelle ligne est juste ? OPTIONS : ['uₙ > 2 ⇒ 3uₙ > 6 ⇒ 3uₙ − 2 > 4 > 2', 'uₙ₊₁ > 2 car 3 > 0', 'on étudie le quotient uₙ₊₁/uₙ']
- après diapo 31 `su_n3_b1` RETROUVER : Cahier fermé : dans l'hérédité, comment choisis-tu ta méthode ? Donne les trois cas.
- après diapo 31 `su_n3_b1` EXERCICE : u₀ = 1 et uₙ₊₁ = ½uₙ + 1. Montre par récurrence que, pour tout n ∈ ℕ, uₙ < 2. OPTIONS : None
- après diapo 34 `su_n3_b2` RETROUVER : Cahier fermé : écris ce que veut dire « (uₙ) est majorée », « minorée », « bornée ».
- après diapo 34 `su_n3_b2` EXERCICE : Pour montrer qu'une suite est décroissante, il faut : OPTIONS : ['calculer u₁ − u₀ et vérifier que u₁ − u₀ ≤ 0', 'montrer uₙ ≤ u₀ pour tout n ∈ ℕ', 'montrer uₙ₊₁ − uₙ ≤ 0 pour tout n']
- après diapo 38 `su_s3_b1` RETROUVER : Cahier fermé : écris l'inégalité qu'il faut montrer pour tout n pour conclure que (uₙ) est croissante.
- après diapo 38 `su_s3_b1` EXERCICE : uₙ = n² + n pour n ∈ ℕ. Étudie le sens de variation de la suite (uₙ). OPTIONS : None
- après diapo 43 `su_s3_b2` RETROUVER : Cahier fermé : écris la relation qu'il faut obtenir pour conclure que (uₙ) est une suite géométrique de raison q.
- après diapo 43 `su_s3_b2` EXERCICE : uₙ₊₁ = 3uₙ − 4 et vₙ = uₙ − 2. Que vaut vₙ₊₁ ? OPTIONS : ['vₙ₊₁ = vₙ − 4 : (vₙ) est arithmétique', 'vₙ₊₁ = 3vₙ : (vₙ) est géométrique de raison 3', 'vₙ₊₁ = 3vₙ − 2 : ni arithmétique ni géométrique']
- après diapo 48 `su_s3_b3` RETROUVER : Cahier fermé : écris le terme général d'une suite géométrique (uₙ) de raison q, en fonction de uₚ.
- après diapo 48 `su_s3_b3` EXERCICE : (vₙ) est géométrique de raison 1/2 et v₀ = 4 ; uₙ = vₙ + 3. Écris uₙ en fonction de n, puis calcule u₂. OPTIONS : None
- après diapo 52 `su_s4_b1` RETROUVER : Cahier fermé : écris la limite de qⁿ quand q est strictement entre −1 et 1.
- après diapo 52 `su_s4_b1` EXERCICE : lim (3 + (−0,5)ⁿ) = ? OPTIONS : ['+∞', '3', 'pas de limite, car q < 0']
- après diapo 57 `su_s4_b2` RETROUVER : Cahier fermé : écris la règle qui donne la limite de f(uₙ).
- après diapo 57 `su_s4_b2` EXERCICE : Calcule lim (2n + 1)/(n + 5). OPTIONS : None
- après diapo 61 `su_s4_b3` RETROUVER : Cahier fermé : écris le critère de convergence d'une suite croissante.
- après diapo 61 `su_s4_b3` EXERCICE : La suite (uₙ) est décroissante et minorée par 1. Que conclut-on ? OPTIONS : ['Elle est convergente', 'Elle tend vers 1', 'Elle tend vers −∞']
- après diapo 67 `su_s5_b1` RETROUVER : Cahier fermé : de 0 < uₙ₊₁ ≤ k·uₙ, qu'obtient-on par récurrence ?
- après diapo 67 `su_s5_b1` EXERCICE : Pour tout n, 0 < uₙ ≤ 2(1/3)ⁿ. Calcule lim uₙ en justifiant. OPTIONS : None
- après diapo 70 `su_s5_b2` RETROUVER : Cahier fermé : f est croissante sur [a ; b] et a ≤ uₙ ≤ b. Qu'écris-tu pour uₙ₊₁ = f(uₙ) ?
- après diapo 70 `su_s5_b2` EXERCICE : f(x) = √(x + 2) est croissante sur [0 ; 2] et uₙ₊₁ = f(uₙ). Si 0 ≤ uₙ ≤ 2, alors… OPTIONS : ['f(2) ≤ uₙ₊₁ ≤ f(0), donc 2 ≤ uₙ₊₁ ≤ √2', '√2 ≤ uₙ₊₁ ≤ 2, donc 0 ≤ uₙ₊₁ ≤ 2', '0 ≤ uₙ₊₁ ≤ 4, car uₙ + 2 ≤ 4']
- après diapo 75 `su_s5_b3` RETROUVER : Cahier fermé : (uₙ) converge vers ℓ, f est continue sur I, f(I) ⊂ I et u₀ ∈ I. Écris l'équation que vérifie ℓ.
- après diapo 75 `su_s5_b3` EXERCICE : u₀ = 0 et uₙ₊₁ = √(uₙ + 2). La suite converge vers ℓ et tous les uₙ sont dans [0 ; 2] (f(x) = √(x + 2) est continue sur [0 ; 2] et f([0 ; 2]) ⊂ [0 ; 2]). Calcule ℓ. OPTIONS : None
- après diapo 79 `su_s6_b1` RETROUVER : Cahier fermé : écris la somme uₚ + … + uₙ de termes consécutifs d'une suite géométrique de raison q ≠ 1.
- après diapo 79 `su_s6_b1` EXERCICE : uₙ = (2n + 1)/(n + 1). Détermine le plus petit entier n tel que uₙ ≥ 1,99. OPTIONS : None
- après diapo 87 `su_n8_b1` RETROUVER : Cahier fermé : écris le critère de comparaison (une suite coincée entre deux suites).
- après diapo 87 `su_n8_b1` EXERCICE : Question 4 : vₙ₊₁ = ? (avec uₙ₊₁ − 2 = 2(uₙ − 2)/(uₙ + 1) et uₙ₊₁ − 1 = 3(uₙ − 1)/(uₙ + 1)) OPTIONS : ['(2/3)vₙ', '(3/2)vₙ', 'vₙ + 2/3']
- après diapo 89 `su_n8_b2` RETROUVER : Cahier fermé : écris le critère de comparaison (une suite coincée entre deux suites).
- après diapo 89 `su_n8_b2` EXERCICE : Question 4 : vₙ₊₁ = ? (avec uₙ₊₁ − 2 = 2(uₙ − 2)/(uₙ + 1) et uₙ₊₁ − 1 = 3(uₙ − 1)/(uₙ + 1)) OPTIONS : ['(2/3)vₙ', '(3/2)vₙ', 'vₙ + 2/3']
