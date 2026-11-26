# math_ch1_limites_continuite — Limites et continuité

## Ouverture — six questions sur une courbe

### Diapo 1 `lc_ouverture_cours` — Limites et continuité
VOIX (fr) : Bienvenue dans un nouveau cours : Limites et continuité. Dans ce cours, nous allons apprendre comment calculer une limite, ce qu'est la continuité, un théorème très important : le théorème des valeurs intermédiaires, puis la fonction réciproque. Ce cours est la base de l'analyse, et au national l'analyse compte pour cinquante-cinq pour cent de la note. Comment allons-nous travailler ? Tu écoutes bien, tu réponds aux questions au tableau, et quand le cours s'arrête, tu écris dans ton cahier. Allons-y !
ÉCRAN : On apprend : Limites, continuité, TVI, fonction réciproque | Au bac : l'analyse = 55 % de la note | Écouter · répondre au tableau · écrire dans le cahier

### Diapo 2 `lc_o1_carte` — La carte du chapitre : six questions sur une courbe
VOIX (fr) : Bienvenue dans le premier chapitre d'analyse. Au centre du tableau, une courbe. Sur cette courbe, on va apprendre à répondre à six questions. Où va-t-elle ? C'est la limite. Est-elle soudée ? C'est la continuité. Quelles hauteurs atteint-elle ? C'est l'image d'un intervalle. Coupe-t-elle l'axe ? C'est le théorème des valeurs intermédiaires. Peut-on revenir en arrière ? C'est la fonction réciproque. Et que défait la racine n-ième ? Regarde en orange : les limites tombent dans vingt sujets sur vingt au national, la réciproque dans huit, la solution unique dans six.
ÉCRAN : Où va la courbe ? → la limite. | Est-elle soudée ? → la continuité. | Quelles hauteurs atteint-elle ? → l'image d'un intervalle. | Coupe-t-elle l'axe ? → le théorème des valeurs intermédiaires. | Peut-on revenir en arrière ? → la fonction réciproque. | Que défait ⁿ√ ? → la racine n-ième. | Au national : les limites tombent dans 20 sujets sur 20, la réciproque dans 8, la solution unique dans 6.
## I. Calculer une limite (rappel de 1re bac)

### Diapo 3 `lc_l1_chemin` — Où mène le chemin ?
VOIX (fr) : Regarde la courbe de f de x égale x carré moins un, sur x moins un. C'est une droite avec un trou au point d'abscisse un. Le point M part de zéro virgule cinq, à gauche de un. Il s'approche de un : zéro virgule neuf, puis zéro virgule quatre-vingt-dix-neuf. Regarde la valeur de f de x écrite à côté. Par la droite, pareil : un virgule zéro un. Mais le trou reste vide : f de un n'existe pas. La limite, c'est là où mène le chemin, pas ce qu'il y a au bout. Autrement : une route avec un trou ; tu ne peux pas t'arrêter dans le trou, mais tu sais où mène la route. On écrit : la limite de f de x, quand x tend vers un, égale ce nombre. Question : de quel nombre f de x s'approche-t-il ?
ÉCRAN : f(x) = (x² − 1)/(x − 1) : f(1) n'existe pas (« 0/0 »). | À gauche : x = 0,99 ; à droite : x = 1,01 : lis la valeur de f(x). | La limite, c'est là où mène le chemin, même si f(1) n'existe pas.
QUESTION : Quand x s'approche de 1, f(x) = (x² − 1)/(x − 1) s'approche de : OPTIONS : ['0', '2', '1']
EXERCICE : f(x) se rapproche de 3 quand x devient très grand : quelle écriture ? OPTIONS : ['lim f(x) = 3 quand x → +∞', 'f(+∞) = 3', 'lim f(x) = +∞ quand x → 3']

### Diapo 4 `lc_l2_remplacer` — Je remplace d'abord
VOIX (fr) : Toute limite commence par le même geste : je remplace x par a. Deux chemins. Si j'obtiens un nombre, c'est le résultat : on dit forme déterminée. Si j'obtiens zéro sur zéro, l'infini sur l'infini, plus l'infini moins l'infini, ou zéro fois l'infini, c'est une forme indéterminée : je transforme l'écriture. Exemple : la limite de x carré plus trois x plus un, quand x tend vers un. Je remplace : un plus trois plus un, cinq. C'est fini.
ÉCRAN : On remplace x par a. | On obtient un nombre : c'est le résultat (forme déterminée). | On obtient « 0/0 », « ∞/∞ », « +∞ − ∞ » ou « 0 × ∞ » : forme indéterminée, on transforme l'écriture. | Exemple : lim_{x→1} (x² + 3x + 1) = 1 + 3 + 1 = 5.

### Diapo 5 `lc_l3_zero_sur_zero` — 0/0 n'est pas une réponse
VOIX (fr) : Trois quotients, et dans les trois, quand je remplace, j'obtiens zéro sur zéro. Le premier : sa courbe arrive à deux. Le deuxième : elle arrive à quatre. Le troisième : elle arrive à un quart. Trois fois zéro sur zéro, et trois limites différentes. Donc zéro sur zéro ne vaut ni zéro, ni un : c'est une forme indéterminée. Elle dit seulement : transforme l'écriture.
ÉCRAN : (x² − 1)/(x − 1) en 1 : « 0/0 », la limite vaut 2. | (x² − 4)/(x − 2) en 2 : « 0/0 », la limite vaut 4. | (√(x + 3) − 2)/(x − 1) en 1 : « 0/0 », la limite vaut 1/4. | Une forme indéterminée ne vaut ni 0 ni 1 : elle dit seulement « transforme l'écriture ».

### Diapo 6 `lc_l4_formes` — Les quatre formes indéterminées
VOIX (fr) : Retiens quatre formes indéterminées, pas plus : zéro sur zéro, l'infini sur l'infini, plus l'infini moins l'infini, et zéro fois l'infini. Pourquoi indéterminées ? On a vu zéro sur zéro donner deux, quatre ou un quart : le résultat n'est pas connu d'avance. Autrement, avec un exemple : x sur x donne un, et x carré sur x donne plus l'infini ; les deux sont l'infini sur l'infini, avec deux résultats différents. Donc quand on trouve l'une de ces quatre, on transforme l'écriture.
ÉCRAN : Formes indéterminées : 0/0 ; ∞/∞ ; +∞ − ∞ ; 0 × ∞. | Indéterminée : le résultat n'est pas connu d'avance (0/0 a donné 2, 4 ou 1/4). | Devant l'une d'elles : on transforme l'écriture.

### Diapo 7 `lc_l4_formes_b` — Ce qui n'est pas indéterminé
VOIX (fr) : Tout le reste, on en connaît le résultat. Plus l'infini plus plus l'infini donne plus l'infini : les deux tirent du même côté. Pour un produit, on applique la règle des signes : moins l'infini fois moins l'infini donne plus l'infini, car moins fois moins donne plus. Un nombre sur l'infini tend vers zéro. Un nombre non nul sur zéro : l'infini, mais son signe se cherche à droite et à gauche. Question : plus l'infini fois moins l'infini, forme indéterminée ou résultat ?
ÉCRAN : +∞ + ∞ → +∞. | Un produit d'infinis : règle des signes, (−∞) × (−∞) → +∞. | k/∞ → 0 ; k/0 (k ≠ 0) : un infini, le signe à droite et à gauche.
QUESTION : (+∞) × (−∞) : OPTIONS : ['Forme indéterminée', '−∞', '0']
EXERCICE : Vrai ou faux ? OPTIONS : None

### Diapo 8 `lc_l4c_usuelles` — Les limites usuelles : xⁿ, 1/xⁿ, √x
VOIX (fr) : Voici des limites à connaître sans calcul. Première : x puissance n, quand x tend vers plus l'infini, tend vers plus l'infini. Deuxième : en moins l'infini, on regarde n. Si n est pair, comme x carré, moins fois moins donne plus : plus l'infini. Si n est impair, comme x cube : moins l'infini. Troisième : un sur x puissance n tend vers zéro, en plus l'infini et en moins l'infini. Quatrième : racine de x tend vers plus l'infini en plus l'infini. Autrement, avec des nombres : moins dix au carré, cent ; moins dix au cube, moins mille ; un sur mille, zéro virgule zéro zéro un. Un nombre non nul fois l'infini : on applique la règle des signes. Exemple : la limite de moins deux x cube quand x tend vers moins l'infini : x cube tend vers moins l'infini, et moins deux fois moins l'infini donne plus l'infini. Je relis : un nombre non nul, fois l'infini, égale l'infini, avec la règle des signes.
ÉCRAN : En +∞ : lim_{x→+∞} xⁿ = +∞ (n ∈ ℕ*) et lim_{x→+∞} √x = +∞. | En −∞ : lim_{x→−∞} xⁿ = +∞ si n est pair ; −∞ si n est impair. | En +∞ et en −∞ : lim_{x→±∞} 1/xⁿ = 0 (n ∈ ℕ*). | ℓ ≠ 0 : ℓ × (±∞) = ±∞ et (±∞)/ℓ = ±∞, le signe par la règle des signes. | Exemple : lim_{x→−∞} x³ = −∞ et −2 < 0, donc lim_{x→−∞} (−2x³) = +∞.

### Diapo 9 `lc_z1_factoriser` — Rappel : a² − b², une identité qui se voit
VOIX (fr) : On part de la base, pas à pas. Regarde ce grand carré : son côté est a, donc sa surface est a carré. On enlève en haut un petit carré de côté b : sa surface est b carré. Il reste a carré moins b carré. Le morceau de droite descend et se couche en bas. On obtient un rectangle : sa largeur est a moins b, sa longueur a plus b. Donc a carré moins b carré égale a moins b, fois a plus b. Exemple : x carré moins neuf, c'est x carré moins trois carré, donc x moins trois, fois x plus trois. Autrement, avec des nombres : dix carré moins trois carré, cent moins neuf, quatre-vingt-onze ; et sept fois treize, quatre-vingt-onze aussi. Je relis : a carré moins b carré, égale a moins b, fois a plus b.
ÉCRAN : Un carré de côté a, on enlève un carré de côté b : il reste a² − b². | Le reste se range en un rectangle (a − b) × (a + b). | a² − b² = (a − b)(a + b) ; exemple : x² − 9 = (x − 3)(x + 3).

### Diapo 10 `lc_z5_racine_facteur` — Rappel : une racine a donne le facteur (x − a)
VOIX (fr) : Une autre base : comment factoriser un polynôme du second degré. Regarde la courbe de P de x égale x carré moins quatre x plus trois. Elle coupe l'axe en trois : P de trois égale neuf moins douze plus trois, zéro. Comme trois annule P, x moins trois sort en facteur. Elle coupe aussi l'axe en un : P de un égale zéro, donc x moins un est aussi un facteur. Donc x carré moins quatre x plus trois égale x moins trois, fois x moins un. Autrement : on développe pour vérifier ; on retrouve x carré moins quatre x plus trois. Je relis : si P de a égale zéro, alors x moins a est un facteur de P de x.
ÉCRAN : P(3) = 9 − 12 + 3 = 0 : (x − 3) est un facteur de x² − 4x + 3. | P(1) = 0 : (x − 1) est un autre facteur. | x² − 4x + 3 = (x − 3)(x − 1) ; on vérifie en développant.
QUESTION : x² − 5x + 6 s'annule pour x = 2 et pour x = 3. Sa factorisation est : OPTIONS : ['(x − 5)(x + 6)', '(x + 2)(x + 3)', '(x − 2)(x − 3)']

### Diapo 11 `lc_l5_facteur` — Polynômes : le facteur (x − a)
VOIX (fr) : Calculons la limite de x carré moins neuf, sur x carré moins quatre x plus trois, quand x tend vers trois. Je remplace : zéro sur zéro. Pourquoi ? Parce que trois annule le haut et le bas. Donc x moins trois se met en facteur en haut et en bas. En haut : x moins trois, fois x plus trois. En bas : x moins trois, fois x moins un. Je barre x moins trois en haut et en bas. Il reste x plus trois sur x moins un. Je remplace : six sur deux, trois. La limite égale trois. Pas besoin de division : on cherche le facteur x moins a.
ÉCRAN : En remplaçant x par 3 : « 0/0 ». | 3 annule le haut et le bas : (x − 3) se met en facteur en haut et en bas. | x² − 9 = (x − 3)(x + 3) ; x² − 4x + 3 = (x − 3)(x − 1). | On simplifie (x − 3), puis on remplace : 6/2 = 3.

### Diapo 12 `lc_l6_conjugue` — Racine carrée : l'expression conjuguée
VOIX (fr) : La limite de racine de x plus trois, moins deux, sur x moins un, quand x tend vers un. Je remplace : zéro sur zéro. La racine nous gêne. On multiplie en haut et en bas par l'expression conjuguée : racine de x plus trois, plus deux. En haut ET en bas : on multiplie par un. En haut, a moins b, fois a plus b, égale a carré moins b carré. Donc x plus trois moins quatre, x moins un. La racine est partie. Je simplifie x moins un, il reste un sur racine de x plus trois, plus deux. Je remplace : un sur deux plus deux, un quart.
ÉCRAN : En remplaçant x par 1 : « 0/0 ». | On multiplie en haut ET en bas par l'expression conjuguée √(x + 3) + 2. | (a − b)(a + b) = a² − b² : en haut, x + 3 − 4 = x − 1, la racine s'en va. | On simplifie (x − 1) : la limite vaut 1/(2 + 2) = 1/4.

### Diapo 13 `lc_l7_plus_lourd` — À l'infini : le terme le plus lourd
VOIX (fr) : Maintenant x tend vers plus l'infini. La limite de trois x carré plus un, sur x carré moins x. Je remplace : l'infini sur l'infini, forme indéterminée. Quand x est très grand, trois x carré écrase un, et x carré écrase x. Autrement : pour x égale cent, trois x carré vaut trente mille, et un ne se voit plus à côté. Dans un quotient de polynômes, on garde le terme de plus haut degré en haut et en bas. Attention : cette règle ne vaut qu'à l'infini ; en un point, on remplace. Question : calcule cette limite.
ÉCRAN : En +∞, un polynôme a la limite de son terme de plus haut degré. | Un quotient de polynômes a la limite du quotient des termes de plus haut degré.
QUESTION : lim (3x² + 1)/(x² − x) quand x → +∞ vaut : OPTIONS : ['+∞', '1', '3']

### Diapo 14 `lc_z4_valeur_absolue` — Rappel : la valeur absolue et √(x²)
VOIX (fr) : Maintenant la valeur absolue. La valeur absolue d'un nombre, c'est sa distance à zéro. Trois est à trois de zéro : valeur absolue de trois égale trois. Moins trois est aussi à trois de zéro : valeur absolue de moins trois égale trois. La valeur absolue enlève le signe. Autrement, avec une machine : on entre moins trois ; au carré, neuf ; puis la racine, trois. On revient à trois, pas à moins trois. Donc racine de x carré n'est pas toujours x : c'est valeur absolue de x. Si x est positif, cela donne x ; si x est négatif, moins x. Je relis : racine de x carré égale valeur absolue de x.
ÉCRAN : |3| = 3 et |−3| = 3 : la distance à 0, sans signe. | Au carré puis racine : √((−3)²) = √9 = 3, pas −3. | √(x²) = |x| : x si x ≥ 0, −x si x ≤ 0.

### Diapo 15 `lc_l8_racine_infini` — Racine à l'infini : même poids, le conjugué
VOIX (fr) : Deux courbes : la droite y égale x, et la courbe de racine de x carré plus x. En x égale dix, l'écart est zéro virgule quatre cent quatre-vingt-huit. Quand x grandit, en cent, zéro virgule quatre cent quatre-vingt-dix-neuf : il s'approche de un demi. Ici plus l'infini moins l'infini, et les deux ont le même poids : racine de x carré, c'est x. Quand les poids sont égaux, on prend le conjugué, comme on l'a fait avec la racine.
ÉCRAN : √(x² + x) − x en +∞ : « +∞ − ∞ ». | Les deux termes ont le même poids (√(x²) = x en +∞) : on prend le conjugué. | L'écart se rapproche de 1/2.

### Diapo 16 `lc_l8_racine_infini_b` — Racine à l'infini : poids différents, le facteur x
VOIX (fr) : Mais racine de x carré plus un, moins trois x : les poids ne sont pas égaux. Racine de x carré plus un ressemble à x, et trois x pèse trois fois plus. Rappel : racine de x carré égale valeur absolue de x, et en plus l'infini x est positif, donc c'est x. On met x en facteur : il reste x, fois racine de un plus un sur x carré, moins trois. La racine tend vers un, la parenthèse vers moins deux, et x vers plus l'infini : la limite est moins l'infini. La règle : poids différents, le facteur ; même poids, le conjugué.
ÉCRAN : √(x² + 1) − 3x en +∞ : « +∞ − ∞ », mais 3x pèse trois fois plus. | √(x² + 1) = |x| √(1 + 1/x²) = x √(1 + 1/x²) car x > 0. | = x(√(1 + 1/x²) − 3) : la parenthèse → −2, donc la limite est −∞.

### Diapo 17 `lc_l9_deux_cotes` — Par la droite, par la gauche
VOIX (fr) : La courbe de f de x égale un sur x moins un. Un point arrive par la droite de un : un virgule un, puis un virgule zéro un. x moins un est un petit nombre positif, et f de x devient dix, puis cent. La courbe monte. Maintenant par la gauche : zéro virgule neuf, puis zéro virgule quatre-vingt-dix-neuf. x moins un est un petit nombre négatif, et f de x devient moins dix, puis moins cent. La courbe plonge. Deux côtés, deux chemins. Par la droite, on écrit x tend vers un plus. Par la gauche, x tend vers un moins.
ÉCRAN : f(x) = 1/(x − 1) : 1 est une valeur interdite. | À droite de 1 : x − 1 est un petit nombre positif, f(x) devient très grand. | À gauche de 1 : x − 1 est un petit nombre négatif, f(x) devient très grand en négatif. | On distingue x → 1⁺ (par la droite) et x → 1⁻ (par la gauche).
OBSERVATION : Par la gauche de 1, que devient f(x) ?

### Diapo 18 `lc_l10_signe` — Un nombre sur 0⁺, un nombre sur 0⁻
VOIX (fr) : Écrivons-le proprement. Le tableau de signe de x moins un : négatif avant un, positif après un. Donc à droite, x moins un tend vers zéro plus, et à gauche vers zéro moins. Un, qui est positif, sur zéro plus : plus l'infini. Un sur zéro moins : moins l'infini. Voilà les deux limites. La limite de un sur x moins un, quand x tend vers un plus, égale plus l'infini. Quand x tend vers un moins, moins l'infini. Ne jamais écrire nombre sur zéro sans le signe. Calcule la limite de deux sur x plus un, quand x tend vers moins un moins.
ÉCRAN : Tableau de signe de x − 1 : négatif avant 1, positif après. | x → 1⁺ : x − 1 → 0⁺, donc 1/(x − 1) → +∞. | x → 1⁻ : x − 1 → 0⁻, donc 1/(x − 1) → −∞. | Un nombre positif sur 0⁺ → +∞ ; sur 0⁻ → −∞ (règle des signes). | ⚠ Ne jamais écrire « un nombre sur 0 » sans son signe : on écrit 0⁺ ou 0⁻. | Limite usuelle : lim_{x→0⁺} 1/x = +∞ et lim_{x→0⁻} 1/x = −∞.
QUESTION : lim 2/(x + 1) quand x → −1⁻ : OPTIONS : ['+∞', '−∞', '0']

### Diapo 19 `lc_l11_interpreter` — Interpréter géométriquement : nommer la droite
VOIX (fr) : Interpréter géométriquement une limite, c'est nommer une droite. Regarde la courbe de deux x plus un, sur x plus un. Quand x devient très grand, elle longe la droite y égale deux, sans la toucher. La limite de f de x en plus l'infini égale deux. On écrit : la droite d'équation y égale deux est une asymptote horizontale à la courbe en plus l'infini. Autrement dit : l'écart entre la courbe et la droite tend vers zéro. Et si la limite est infinie quand x tend vers un nombre a, la droite d'équation x égale a est une asymptote verticale. Le conseil : regarde ce qui reste fixe.
ÉCRAN : lim_{x→a} f(x) = ±∞ (ou seulement à droite / à gauche de a) : la droite d'équation x = a est une asymptote verticale à (C_f). | lim_{x→±∞} f(x) = ℓ : la droite d'équation y = ℓ est une asymptote horizontale à (C_f) en ±∞. | Regarde ce qui reste fixe : a pour une verticale, ℓ pour une horizontale. | Les autres branches (oblique, parabolique) : au chapitre dérivation et étude de fonctions.

### Diapo 20 `lc_l12_sinus` — La limite de référence sin(x)/x
VOIX (fr) : Une limite à connaître : la limite de sinus x sur x en zéro. Regarde deux courbes : celle de sinus x, et la droite y égale x. Le point M s'approche de zéro. En x égale un, sinus x sur x vaut zéro virgule quatre-vingt-quatre ; en zéro virgule cinq, zéro virgule quatre-vingt-seize : cela s'approche de un. Autrement : près de zéro, la courbe du sinus colle à la droite y égale x ; sinus x est très proche de x, et un nombre divisé par lui-même donne un. Je relis : la limite de sinus x sur x, quand x tend vers zéro, égale un.
ÉCRAN : Près de 0 : sin(1)/1 ≈ 0,84 ; sin(0,5)/0,5 ≈ 0,96 ; cela s'approche de 1. | Près de 0, la courbe de sin colle à la droite y = x : sin x ≈ x. | Limite de référence : lim_{x→0} sin(x)/x = 1. | Deux autres limites de référence à connaître : lim_{x→0} tan(x)/x = 1 et lim_{x→0} (1 − cos x)/x² = 1/2.

### Diapo 21 `lc_l12_sinus_b` — sin(3x)/(2x) : on pose t = 3x
VOIX (fr) : Maintenant sinus de trois x sur deux x. En zéro : zéro sur zéro. Pour utiliser la limite du sinus, il faut la même chose sous le sinus et en bas : trois x. On écrit trois sur deux, fois sinus de trois x sur trois x. On pose t égale trois x : quand x tend vers zéro, t tend vers zéro aussi. Donc sinus de t sur t tend vers un. Il reste trois sur deux.
ÉCRAN : sin(3x)/(2x) = (3/2) × sin(3x)/(3x). | On pose t = 3x : quand x → 0, t → 0, et sin(t)/t → 1. | Donc lim_{x→0} sin(3x)/(2x) = 3/2.

### Diapo 22 `lc_l13_devoir` — À toi : calculer des limites
VOIX (fr) : À toi. Pour chaque limite, trois gestes : je remplace, je nomme la forme, je choisis l'outil. Regarde : un sur x moins un, moins deux sur x carré moins un, quand x tend vers un. Je remplace : plus l'infini moins l'infini. L'outil : le même dénominateur, car x carré moins un égale x moins un, fois x plus un. En haut : x plus un moins deux, c'est-à-dire x moins un. Termine : simplifie, puis remplace. Question : calcule cette limite.
ÉCRAN : 1/(x − 1) − 2/(x² − 1) en 1 : « +∞ − ∞ » → même dénominateur. | = (x + 1 − 2)/(x² − 1) = (x − 1)/((x − 1)(x + 1)) : à toi de simplifier, puis de remplacer. | Chaque limite : je remplace, je nomme la forme, je choisis l'outil. | Outils : facteur (x − a), conjugué, plus haut degré, sin(ax)/(ax).
QUESTION : lim [1/(x − 1) − 2/(x² − 1)] quand x → 1 vaut : OPTIONS : ['0', '+∞', '1/2']
EXERCICE : lim (x² − 4)/(x − 2) quand x → 2 ? OPTIONS : ['4', '0', '2']
## II. Continuité en un point

### Diapo 23 `lc_c1_soudee` — Soudée ou coupée ?
VOIX (fr) : Trois dessins, trois courbes, et le même point a. Premier dessin : la courbe passe d'un seul trait par le point a, f de a. Elle est soudée. Deuxième dessin : la courbe saute en a. Elle est coupée. Troisième dessin : la courbe a un trou en a, et le point a, f de a est posé plus haut, ailleurs. Elle est coupée aussi. Continue en a veut dire : la courbe arrive exactement sur le point a, f de a.
ÉCRAN : Premier dessin : la courbe passe d'un seul trait par le point (a ; f(a)) : continue en a. | Deuxième dessin : la courbe saute en a : pas continue en a. | Troisième dessin : la courbe a un trou et le point (a ; f(a)) est ailleurs : pas continue en a. | Continue en a : la courbe arrive exactement sur le point (a ; f(a)).

### Diapo 24 `lc_c2_limite_image` — La limite égale l'image
VOIX (fr) : Sans la courbe, on compare deux nombres. Ici, f de x égale x plus un pour x différent de un. La courbe arrive à la hauteur deux : la limite en un égale deux. Mais le point un, f de un est posé à la hauteur trois. Deux et trois : pas égaux. Donc f n'est pas continue en un. Je relis la définition : f est continue en a si la limite de f de x, quand x tend vers a, égale f de a. Quelle valeur donner à f de un pour que f soit continue en un ? La valeur de la limite, deux.
ÉCRAN : Deux nombres à comparer : la limite de f en a (où arrive la courbe) et f(a) (où est le point). | Définition : f est définie sur un intervalle ouvert I contenant a ; f est continue en a si lim_{x→a} f(x) = f(a). | Ici lim f(x) = 2 et f(1) = 3 : f n'est pas continue en 1. | Quelle valeur donner à f(1) pour que f soit continue en 1 ? La valeur de la limite : 2.

### Diapo 25 `lc_c3_deux_branches` — Deux expressions : chaque côté sa branche
VOIX (fr) : Une fonction avec deux expressions. f de x égale trois x moins un si x est plus petit que un, et x carré plus m si x est plus grand ou égal à un. À gauche de un, je prends trois x moins un : la branche rouge arrive à la hauteur deux. À droite de un, je prends x carré plus m : la branche verte part de un plus m. Et f de un ? Je cherche le signe plus grand ou égal : c'est la branche x carré plus m. f de un égale un plus m. Pour la limite à droite de un, quelle expression prends-tu ?
ÉCRAN : f(x) = 3x − 1 si x < 1 ; f(x) = x² + m si x ≥ 1. | À droite de 1 (x > 1) : on prend x² + m. À gauche (x < 1) : on prend 3x − 1. | f(1) se calcule avec la branche qui porte l'égalité (x ≥ 1). | Lis la condition écrite à côté de chaque expression.
QUESTION : f(x) = 3x − 1 si x < 1 ; x² + m si x ≥ 1. Pour la limite à droite de 1, on prend : OPTIONS : ['3x − 1', 'x² + m', 'les deux']

### Diapo 26 `lc_c4_parametre` — Quelle valeur de m soude la courbe ?
VOIX (fr) : Même fonction, avec m égale trois. La branche gauche arrive à deux. La branche droite part de un plus m, quatre. Il y a un saut de deux : la courbe est coupée. Pour souder, il faut que la limite à gauche, la limite à droite et f de un soient égales. Deux égale un plus m, donc m égale un. Glisse toi-même le départ de la branche droite, et regarde la courbe se souder.
ÉCRAN : Limite à gauche en 1 : lim (3x − 1) = 2. | Limite à droite et f(1) : 1 + m. | f est continue en 1 si 1 + m = 2, donc m = 1. | Glisse le départ de la branche droite : avec m = 3, il y a un saut de 2.

### Diapo 27 `lc_c4b_droite_gauche` — Continue à droite, continue à gauche
VOIX (fr) : Même fonction, avec m égale trois. Regardons chaque côté séparément. f de un, avec la branche qui porte l'égalité : un plus trois, quatre. À droite de un, la branche verte part de quatre : la limite à droite vaut quatre, c'est f de un. On dit : f est continue à droite en un. À gauche, la branche rouge arrive à deux, et deux n'est pas quatre : f n'est pas continue à gauche en un. Je relis : f est continue à droite en a si la limite de f de x, quand x tend vers a plus, égale f de a. Même chose à gauche, avec a moins. Autrement dit : la courbe doit arriver au point des deux côtés. f est continue en a si elle est continue à droite et à gauche en a. Ici un seul côté arrive, donc f n'est pas continue en un. On écrit aussi : continue à droite de a, c'est la même chose.
ÉCRAN : f définie sur [a ; a + r[ (r > 0) : f est continue à droite en a si lim_{x→a⁺} f(x) = f(a). | f définie sur ]a − r ; a] (r > 0) : f est continue à gauche en a si lim_{x→a⁻} f(x) = f(a). | Propriété : f est continue en a ⇔ f est continue à droite et à gauche en a. | Avec m = 3 : f(1) = 1 + 3 = 4 ; lim_{x→1⁺} f(x) = 4 = f(1), donc f est continue à droite en 1. | lim_{x→1⁻} f(x) = 2 ≠ f(1), donc f n'est pas continue à gauche en 1 : f n'est pas continue en 1. | On dit aussi « continue à droite de a » : c'est la même chose.

### Diapo 28 `lc_c5_redaction` — La rédaction : f(a), ①, ②, conclusion
VOIX (fr) : Voici la rédaction qui prend tous les points. f de x égale racine de x plus trois si x est plus grand ou égal à un, et x plus un si x est plus petit que un. Ligne un : f de un, avec la branche qui porte l'égalité. Racine de quatre, deux. Ligne deux : la limite à droite. Racine de x plus trois tend vers deux, égale f de un. On note un. Ligne trois : la limite à gauche. x plus un tend vers deux, égale f de un. On note deux. Ligne quatre : d'après un et deux, f est continue en un.
ÉCRAN : f(1) avec la branche qui porte l'égalité : f(1) = √(1 + 3) = 2. | ① lim_{x→1⁺} f(x) = f(1), donc f est continue à droite en 1. | ② lim_{x→1⁻} f(x) = f(1), donc f est continue à gauche en 1. | « D'après ① et ②, f est continue en 1 » (continue à droite et à gauche en 1). | Une seule expression : lim_{x→a} f(x) = f(a), donc f est continue en a.

### Diapo 29 `lc_c5b_parametre` — À toi : la valeur de m
VOIX (fr) : À toi maintenant. f de x égale x carré plus un si x est inférieur ou égal à deux, et trois x plus m si x est supérieur à deux. Même méthode. f de deux : on prend la branche inférieur ou égal : deux au carré plus un, cinq. La limite à gauche : x carré plus un tend vers cinq. La limite à droite : trois x plus m tend vers six plus m. Question : quelle valeur de m rend f continue en deux ?
ÉCRAN : f(x) = x² + 1 si x ≤ 2 ; f(x) = 3x + m si x > 2. | f(2) = 5 ; limite à gauche : 5 ; limite à droite : 6 + m. | Quelle valeur de m rend f continue en 2 ?
QUESTION : f(x) = x² + 1 si x ≤ 2 ; f(x) = 3x + m si x > 2. f est continue en 2 pour : OPTIONS : ['m = −1', 'm = 1', 'm = 5']
## III. Continuité sur un intervalle

### Diapo 30 `lc_i1_usuelles` — Les fonctions usuelles se tracent d'un trait
VOIX (fr) : Quatre fonctions que tu connais. Un polynôme, x carré moins deux x : il se trace d'un seul trait, il est continu sur R. La fonction un sur x : la craie se lève en zéro, donc elle est continue sur moins l'infini, zéro ouvert, et sur zéro, plus l'infini. La racine carrée : elle naît en zéro, continue sur zéro, plus l'infini. Le sinus : d'un seul trait, continue sur R. La règle : une fonction usuelle est continue sur chaque intervalle de son domaine de définition. Sur quel ensemble la fonction racine est-elle continue ?
ÉCRAN : Continue sur ]a ; b[ : continue en chaque point de ]a ; b[. Continue sur [a ; b] : continue sur ]a ; b[, à droite en a et à gauche en b. | Une fonction polynôme est continue sur ℝ. | x ↦ 1/x est continue sur ]−∞ ; 0[ et sur ]0 ; +∞[. | x ↦ √x est continue sur [0 ; +∞[ ; x ↦ |x| est continue sur ℝ. | sin et cos sont continues sur ℝ ; tan est continue sur chaque intervalle où x ≠ π/2 + kπ (k ∈ ℤ). | Une fonction usuelle est continue sur chaque intervalle de son domaine de définition.
QUESTION : Sur quel ensemble x ↦ √x est-elle continue ? OPTIONS : ['ℝ', ']0 ; +∞[ seulement', '[0 ; +∞[']

### Diapo 31 `lc_i2_operations` — Somme, produit, quotient
VOIX (fr) : Avec des fonctions continues, on fabrique d'autres fonctions continues : la somme, le produit, et le quotient, si le dénominateur ne s'annule pas. Regarde f de x égale deux x sur x moins trois. x moins trois s'annule en trois : valeur interdite, la croix rouge. Sur quatre, plus l'infini, il n'y a pas trois : f est continue. C'est comme une ville et un quartier : continue sur la ville, donc sur le quartier. Mais zéro, cinq contient trois : f n'est pas continue sur zéro, cinq.
ÉCRAN : Somme, produit de fonctions continues sur I, et αf (α ∈ ℝ) : continues sur I. | Quotient u/v : continu sur I si u et v sont continues sur I et (∀x ∈ I) v(x) ≠ 0. | f(x) = 2x/(x − 3) : 3 est une valeur interdite. | f est continue sur [4 ; +∞[ (3 n'y est pas), mais pas sur [0 ; 5] (qui contient 3).

### Diapo 32 `lc_i3_racine_u` — √u : continue ET positive
VOIX (fr) : Une racine, c'est deux machines à la suite. x entre dans la première machine u : trois x moins six. Le résultat entre dans la deuxième machine : la racine. Mais la racine n'accepte que du positif. x égale quatre : u égale six, la racine donne racine de six. x égale un : u égale moins trois, refusé. Donc pour racine de u, il faut deux lignes : u est continue sur I, et u est positive sur I. Ici, x plus grand ou égal à deux, donc trois x moins six plus grand ou égal à zéro.
ÉCRAN : x ↦ √(3x − 6) : d'abord u(x) = 3x − 6, ensuite la racine. | La racine n'accepte que du positif : il faut (∀x ∈ I) u(x) ≥ 0. | Rédaction : u est une fonction polynôme, donc u est continue sur ℝ, en particulier sur I = [2 ; +∞[. | (∀x ∈ I) x ≥ 2, donc 3x ≥ 6, donc 3x − 6 ≥ 0. Donc x ↦ √(3x − 6) est continue sur I.

### Diapo 33 `lc_i4_composee` — Deux machines à la suite
VOIX (fr) : La limite passe d'une machine à l'autre. Racine de quatre plus un sur x, quand x tend vers plus l'infini. Première machine : u de x égale quatre plus un sur x ; un sur x tend vers zéro, donc u tend vers quatre. Deuxième machine : la racine prend ce qui sort de la première. La règle : on calcule d'abord la limite de u, puis on prend sa racine. Question : calcule la limite de racine de quatre plus un sur x, en plus l'infini.
ÉCRAN : √(4 + 1/x) : d'abord u(x) = 4 + 1/x, ensuite la racine. | Quand x → +∞ : 1/x → 0, donc u(x) → 4. | La racine est continue : on prend la racine de la limite de u.
QUESTION : lim √(4 + 1/x) quand x → +∞ vaut : OPTIONS : ['4', '+∞', '2']
## IV. Image d'un intervalle

### Diapo 34 `lc_z3_derivee` — Rappel : le signe de f′ donne le sens de variation
VOIX (fr) : Maintenant la dérivée, et comment elle dit si la courbe monte ou descend. Regarde la courbe de f de x égale x cube plus x moins un. Un point se déplace dessus, avec la tangente. La pente de la tangente, c'est f prime de x. Ici f prime de x égale trois x carré plus un : la pente est toujours positive, et la courbe monte toujours. Donc quand f prime est positive, f est strictement croissante ; quand f prime est négative, f est strictement décroissante. Autrement : comme une route ; si elle monte, la pente est positive ; si elle descend, la pente est négative. Dans le tableau de variations, on écrit plus dans la ligne de f prime, et la flèche monte dans la ligne de f. Je relis : si f prime est strictement positive sur I, alors f est strictement croissante sur I.
ÉCRAN : f′(x) est la pente de la tangente au point d'abscisse x. | f′ > 0 sur I : la courbe monte, f est strictement croissante sur I. | f′ < 0 sur I : la courbe descend, f est strictement décroissante sur I.

### Diapo 35 `lc_j1_hauteurs` — Les hauteurs atteintes
VOIX (fr) : Regarde la courbe de f de x égale x carré moins quatre x plus un. Sur l'axe des abscisses, le segment de deux à cinq : x parcourt ce segment. De a, les pointillés montent à la courbe, puis vont à l'axe des ordonnées : f de a égale moins trois. De b, la même chose : f de b égale six. Sur l'axe des ordonnées, la partie colorée, ce sont toutes les hauteurs atteintes. C'est l'image de l'intervalle : f de deux, cinq.
ÉCRAN : x parcourt le segment [a ; b] sur l'axe des abscisses. | Des pointillés montent à la courbe, puis vont à l'axe des ordonnées. | f([a ; b]) : l'ensemble de toutes les valeurs f(x) quand x parcourt [a ; b]. | f(x) = x² − 4x + 1 sur [2 ; 5] : les hauteurs vont de −3 à 6.

### Diapo 36 `lc_j2_croissante` — Croissante : même ordre
VOIX (fr) : Quand f est continue et strictement croissante, l'ordre est gardé. Ici a égale trois, b égale quatre virgule cinq. f de a est en bas, f de b est en haut. Donc l'image est le segment f de a, f de b. Je relis : si f est continue et strictement croissante sur a, b, l'image du segment a b est le segment f de a, f de b. Glisse a ou b toi-même : les images suivent dans le même ordre.
ÉCRAN : f continue et strictement croissante sur [a ; b] : f(a) est la plus petite valeur, f(b) la plus grande. | f([a ; b]) = [f(a) ; f(b)]. | Glisse a et b : les images suivent dans le même ordre. | Exemple : f croissante, f(1) = 2, f(3) = 7 : f([1 ; 3]) = [2 ; 7].

### Diapo 37 `lc_j3_decroissante` — Décroissante : l'ordre s'inverse
VOIX (fr) : Maintenant g de x égale quatre sur x, strictement décroissante sur un, quatre. De a égale un, les pointillés montent : g de un égale quatre, en haut. De b égale quatre : g de quatre égale un, en bas. Regarde : les pointillés se croisent. L'image de a est au-dessus de celle de b. Un intervalle s'écrit toujours du plus petit au plus grand. Donc l'image est g de b, g de a : un, quatre. Pour une fonction strictement décroissante, on inverse les bornes. g est décroissante, g de un égale cinq, g de quatre égale moins un : que vaut g de un, quatre ?
ÉCRAN : g(x) = 4/x est strictement décroissante sur [1 ; 4]. | g(1) = 4 est en haut, g(4) = 1 est en bas : les pointillés se croisent. | Un intervalle s'écrit du plus petit au plus grand : g([1 ; 4]) = [g(4) ; g(1)] = [1 ; 4]. | Strictement décroissante : f([a ; b]) = [f(b) ; f(a)].
QUESTION : g est continue et strictement décroissante, g(1) = 5, g(4) = −1. g([1 ; 4]) = OPTIONS : ['[5 ; −1]', '[−1 ; 5]', '[1 ; 4]']

### Diapo 38 `lc_j4_borne_ouverte` — Borne ouverte : une limite
VOIX (fr) : g de x égale quatre sur x, sur zéro, quatre, ouvert en zéro. Le rond vide : zéro est exclu, g de zéro n'existe pas. Alors, à la borne ouverte, on prend la limite. Zéro est la borne de gauche : on s'en approche par la droite, zéro plus. La limite de g de x, quand x tend vers zéro plus, égale plus l'infini. À la borne fermée quatre, on prend l'image, g de quatre égale un. L'image est un, plus l'infini, avec un crochet ouvert. Ouvert, limite. Fermé, image.
ÉCRAN : g(x) = 4/x sur ]0 ; 4] : 0 est exclu, g(0) n'existe pas. | À la borne ouverte, on prend la limite : lim_{x→0⁺} g(x) = +∞. | La borne de gauche s'approche par la droite (0⁺), celle de droite par la gauche (b⁻). | g(]0 ; 4]) = [1 ; +∞[ : le crochet suit son nombre.

### Diapo 39 `lc_j5_non_monotone` — Ni croissante ni décroissante
VOIX (fr) : h de x égale x cube moins trois x, sur moins deux, deux. Elle monte, redescend, puis remonte. Les formules avec f de a et f de b ne marchent plus. On cherche la plus grande hauteur, la bosse : M égale deux. Et la plus petite, le creux : m égale moins deux. On les lit dans le tableau de variations. L'image est m, M : moins deux, deux.
ÉCRAN : h(x) = x³ − 3x sur [−2 ; 2] monte, redescend, puis remonte. | On lit dans le tableau de variations la plus petite valeur m et la plus grande M. | Ici m = −2 (le creux) et M = 2 (la bosse). | f continue sur [a ; b], non monotone : f([a ; b]) = [m ; M]. | Propriété (admise) : l'image d'un segment par une fonction continue est un segment ; l'image d'un intervalle par une fonction continue est un intervalle.
## V. Le théorème des valeurs intermédiaires

### Diapo 40 `lc_t1_couper_axe` — Couper l'axe sans résoudre
VOIX (fr) : Résoudre f de x égale zéro, c'est chercher où la courbe coupe l'axe des abscisses. Mais x cube plus x moins un égale zéro, tu ne sais pas le résoudre. On demande seulement : y a-t-il une solution, et où ? Regarde. La courbe se trace d'un seul trait de a à b. f de a est sous l'axe. f de b est au-dessus. Pour passer de dessous à dessus sans lever la craie, la courbe doit couper l'axe. Là, en un point qu'on appelle alpha : f de alpha égale zéro. C'est comme traverser l'oued à pied : on a forcément les pieds dans l'eau.
ÉCRAN : Résoudre f(x) = 0, c'est chercher où la courbe coupe l'axe des abscisses. | Parfois on ne sait pas résoudre (x³ + x − 1 = 0) : on demande seulement s'il y a une solution, et où. | La courbe continue part sous l'axe en a (f(a) < 0) et arrive au-dessus en b (f(b) > 0). | Sans lever la craie, elle coupe l'axe en un point α : f(α) = 0.

### Diapo 41 `lc_t2_continue` — Sans continuité, la courbe saute
VOIX (fr) : Même départ sous l'axe, même arrivée au-dessus. Mais regarde : la courbe s'arrête sous l'axe, et elle repart au-dessus. Elle saute. Elle passe de l'autre côté sans couper l'axe. C'est comme un pont : on traverse l'oued au sec. Donc la première condition : f est continue sur a, b. Ici, y a-t-il forcément une solution ?
ÉCRAN : Ici f(a) < 0 et f(b) > 0, mais la courbe est coupée en deux morceaux. | Elle passe au-dessus de l'axe sans le couper : aucune solution. | Première condition du théorème : f est continue sur [a ; b].
QUESTION : La courbe saute par-dessus l'axe (f n'est pas continue). Y a-t-il forcément une solution ? OPTIONS : ['Oui', 'Non']

### Diapo 42 `lc_t3_produit` — Une image dessous, une dessus
VOIX (fr) : Cette fois, la courbe est continue, mais f de a et f de b sont tous les deux positifs. La courbe reste au-dessus de l'axe : rien ne l'oblige à le couper. Il faut une image dessous et une image dessus : des signes contraires. Et deux nombres de signes contraires, leur produit est négatif. Voilà pourquoi on écrit : f de a fois f de b est strictement négatif.
ÉCRAN : Ici f(a) > 0 et f(b) > 0 : la courbe peut rester au-dessus de l'axe. | Il faut f(a) et f(b) de signes contraires. | Signes contraires ⇔ produit négatif : f(a) × f(b) < 0. | On calcule f(a), on calcule f(b), on écrit le signe du produit.

### Diapo 43 `lc_t4_au_moins_une` — Au moins une solution
VOIX (fr) : Avec les deux conditions, la courbe coupe l'axe. Mais combien de fois ? Regarde cette courbe en vague : continue, f de a négatif, f de b positif. Elle coupe l'axe une, deux, trois fois. Le théorème dit au moins une solution, pas une seule. Je relis : f est continue sur a, b, et f de a fois f de b est strictement négatif, donc, d'après le théorème des valeurs intermédiaires, l'équation f de x égale zéro admet au moins une solution, dans a, b ouvert.
ÉCRAN : Théorème des valeurs intermédiaires : f continue sur [a ; b] et f(a) × f(b) < 0, donc f(x) = 0 admet au moins une solution dans ]a ; b[. | « Au moins une » : la courbe peut couper plusieurs fois (ici trois). | Le théorème ne donne pas la valeur de la solution : il dit qu'elle existe et où.

### Diapo 44 `lc_t5_unique` — Unique : la courbe ne revient pas
VOIX (fr) : Pour dire unique, il faut une troisième condition. Regarde la courbe de x cube plus x moins un. Sa dérivée, trois x carré plus un, est positive : f est strictement croissante. La flèche verte : elle monte sans jamais redescendre. Donc elle coupe l'axe une seule fois, en alpha. Je relis : f est continue et strictement croissante sur a, b, et f de a fois f de b est négatif, donc l'équation f de x égale zéro admet une solution unique alpha, dans a, b ouvert. Attention au mot strictement : monotone seul ne suffit pas. Quelle condition faut-il ajouter pour dire unique ?
ÉCRAN : Troisième condition pour « unique » : f strictement monotone sur [a ; b]. | Strictement croissante : la courbe monte sans jamais revenir, elle coupe l'axe une seule fois. | f′(x) = 3x² + 1 > 0 : x³ + x − 1 est strictement croissante. | « Strictement » compte : un palier sur l'axe donnerait une infinité de solutions.
QUESTION : Pour dire « solution unique », on ajoute : OPTIONS : ['f(a) + f(b) < 0 aux bornes de [a ; b]', 'f strictement monotone sur [a ; b]', 'f(a) = 0 à une borne de [a ; b]']

### Diapo 45 `lc_t6_rediger` — Rédiger comme au national
VOIX (fr) : Voici la rédaction qui prend tous les points au national. Montrer que x cube plus x moins un égale zéro admet une solution unique dans zéro, un. Ligne un : Posons f de x égale x cube plus x moins un. Ligne deux : f est une fonction polynôme, donc continue sur zéro, un fermé. Ligne trois : f prime de x égale trois x carré plus un, positif, donc f est strictement croissante. Ligne quatre : f de zéro égale moins un, f de un égale un, donc le produit est négatif. Conclusion : donc, d'après le théorème des valeurs intermédiaires, l'équation admet une solution unique alpha, dans zéro, un ouvert.
ÉCRAN : « Posons f(x) = … » (tout passé dans un membre). | f est continue sur [a ; b] car … (polynôme, somme de fonctions continues…). | f est strictement croissante sur [a ; b] car f′(x) > 0 sur [a ; b] (ou décroissante car f′(x) < 0). | f(a) et f(b) calculés chacun sur sa ligne, puis f(a) × f(b) < 0. | Donc, d'après le théorème des valeurs intermédiaires, l'équation admet une solution unique α dans ]a ; b[.

### Diapo 46 `lc_t7_valeur_k` — Toute valeur entre f(a) et f(b)
VOIX (fr) : Et si l'équation est f de x égale k ? On trace la droite horizontale y égale k. Ici k égale zéro virgule cinq, entre f de a égale moins un et f de b égale un. La droite coupe la courbe : f de x égale k a une solution c. Si k est en dehors, la droite ne coupe pas la courbe au-dessus de a, b. Pour le rédiger, on pose h de x égale f de x moins k, et on applique le théorème à h. Glisse la droite toi-même.
ÉCRAN : f continue sur [a ; b] : toute valeur k comprise entre f(a) et f(b) est atteinte. | La droite y = k coupe la courbe quand k est entre f(a) et f(b). | Méthode : poser h(x) = f(x) − k et appliquer le théorème à h(x) = 0, ou vérifier que k est entre f(a) et f(b). | En dehors, la droite peut ne pas couper la courbe au-dessus de [a ; b].

### Diapo 47 `lc_t8_intervalle_ouvert` — Sur ℝ ou sur ]0 ; +∞[ : 0 ∈ f(I)
VOIX (fr) : Quand l'intervalle est R, il n'y a pas de f de a : on ne multiplie pas une limite infinie. On passe par l'image. f de x égale x cube plus x moins un. En moins l'infini, la limite est moins l'infini. En plus l'infini, plus l'infini. f est continue et strictement croissante, donc f de R égale moins l'infini, plus l'infini, c'est R. Zéro appartient à f de R. Donc l'équation f de x égale zéro admet une solution unique alpha dans R. Ensuite on la localise : f de zéro est négatif, f de un est positif, donc alpha est entre zéro et un.
ÉCRAN : Pas de f(a) quand la borne est infinie : on utilise les limites. | f continue et strictement croissante sur ℝ, lim_{x→−∞} f(x) = −∞ et lim_{x→+∞} f(x) = +∞ : f(ℝ) = ]−∞ ; +∞[ = ℝ. | 0 ∈ f(ℝ), donc l'équation f(x) = 0 admet une solution unique α dans ℝ. | Puis on localise α avec deux images de signes contraires : f(0) = −1 < 0 et f(1) = 1 > 0, donc 0 < α < 1. | Cas général : f continue et strictement monotone sur I et k ∈ f(I) (k réel, noté aussi λ) : l'équation f(x) = k admet une solution unique dans I. Exemple : 1 ∈ ℝ = f(ℝ), donc x³ + x − 1 = 1 admet une solution unique dans ℝ.

### Diapo 48 `lc_t9_f_alpha` — Se servir de f(α) = 0
VOIX (fr) : On ne connaît pas la valeur de alpha, mais on sait une chose : f de alpha égale zéro. Regarde la courbe, et le point alpha. Je remplace x par alpha : alpha cube plus alpha moins un égale zéro. Donc alpha cube égale un moins alpha. Et le signe de f : avant alpha, la courbe est sous l'axe, f est négative. Après alpha, elle est au-dessus, f est positive. C'est une question qui tombe au national. Alpha est solution de x cube plus x moins un égale zéro : quelle égalité est vérifiée par alpha ?
ÉCRAN : α est solution de f(x) = 0 : donc f(α) = 0. | x³ + x − 1 = 0 donne α³ + α − 1 = 0, donc α³ = 1 − α. | f strictement croissante : f(x) < 0 avant α et f(x) > 0 après α. | Au national : « montrer que α vérifie… », « en déduire le signe de f ».
QUESTION : α est solution de x³ + x − 1 = 0. Quelle égalité est vraie ? OPTIONS : ['α³ = 1 − α', 'α = 1', 'α³ = α − 1']
## VI. La fonction réciproque

### Diapo 49 `lc_r1_aller_retour` — Le chemin aller, le chemin retour
VOIX (fr) : f de x égale x carré plus un, pour x positif. Le chemin aller : je pars de deux sur l'axe des abscisses, je monte à la courbe, je vais lire cinq sur l'axe des ordonnées. f de deux égale cinq. Le chemin retour, en orange : je pars de cinq, je reviens à la courbe, je descends à deux. C'est la fonction réciproque, notée f moins un : f moins un de cinq égale deux. f moins un défait ce que f a fait, comme le taxi du retour. Attention : f moins un, ce n'est pas un sur f.
ÉCRAN : f(x) = x² + 1 sur [0 ; +∞[ : f(2) = 5 (chemin aller). | La fonction réciproque f⁻¹ ramène 5 à 2 : f⁻¹(5) = 2 (chemin retour). | f⁻¹ défait ce que f a fait. | f⁻¹ n'est pas 1/f : f⁻¹ se dit « f moins un » ou « la réciproque de f ».

### Diapo 50 `lc_r2_strictement_monotone` — Un seul antécédent : strictement monotone
VOIX (fr) : Pourquoi x carré n'a-t-elle pas de réciproque sur R ? Regarde la droite y égale quatre. Elle coupe la parabole en deux points : moins deux et deux. Quatre a deux antécédents : le chemin retour hésite. Alors on garde seulement zéro, plus l'infini : la moitié gauche pâlit. Là, x carré est strictement croissante, un seul antécédent : deux. On change de nom : la restriction g. La règle : f est continue et strictement monotone sur I, donc f admet une fonction réciproque.
ÉCRAN : Sur ℝ, x² donne 4 pour x = −2 et pour x = 2 : deux antécédents, le retour hésite. | Sur [0 ; +∞[, x² est strictement croissante : un seul antécédent. | On réduit le domaine : la restriction g de x ↦ x² à [0 ; +∞[ (nouveau nom). | f continue et strictement monotone sur I, donc f admet une fonction réciproque.
OBSERVATION : Combien de nombres x ont pour image 4 par x ↦ x² ?

### Diapo 51 `lc_r3_J` — f⁻¹ est définie sur J = f(I)
VOIX (fr) : f va de I vers J, et f moins un fait le chemin inverse, de J vers I. Ici f de x égale x carré moins quatre x plus un, sur I égale deux, plus l'infini. I est coloré sur l'axe des abscisses. f est strictement croissante, f de deux égale moins trois, et la limite en plus l'infini est plus l'infini. Donc J égale f de I, égale moins trois, plus l'infini : coloré sur l'axe des ordonnées. J se calcule avec l'image d'un intervalle.
ÉCRAN : f va de I vers J ; f⁻¹ va de J vers I. | J = f(I) se calcule avec l'image d'un intervalle. | f(x) = x² − 4x + 1 sur I = [2 ; +∞[ : strictement croissante, f(2) = −3, limite +∞. | J = f(I) = [−3 ; +∞[. | Aller puis retour : (∀x ∈ I) f⁻¹(f(x)) = x ; retour puis aller : (∀x ∈ J) f(f⁻¹(x)) = x.

### Diapo 52 `lc_r4_deux_lignes` — Deux lignes, comme au national
VOIX (fr) : Au national, la question dit : montrer que g admet une fonction réciproque définie sur un intervalle J à déterminer. Deux lignes suffisent. Ici g de x égale x carré moins deux x moins un, sur un, plus l'infini. Ligne un : g est continue sur I, c'est un polynôme. Ligne deux : g prime de x égale deux x moins deux, positif sur I, donc g est strictement croissante. Conclusion : donc g admet une fonction réciproque, définie sur J égale g de I. Et J : g de un égale moins deux, la limite est plus l'infini, J égale moins deux, plus l'infini. Attention : ni produit, ni théorème des valeurs intermédiaires ici. Quelles sont les deux conditions pour qu'une fonction admette une réciproque ?
ÉCRAN : g est continue sur I car c'est un polynôme ; g est strictement croissante (ou décroissante) sur I car signe de g′. | Donc g admet une fonction réciproque g⁻¹ définie sur un intervalle J = g(I). | J par l'image d'un intervalle : J = [−2 ; +∞[ pour g(x) = x² − 2x − 1 sur [1 ; +∞[. | « Il n'est pas demandé de déterminer g⁻¹(x) » : on s'arrête là.
QUESTION : Pour montrer que f admet une fonction réciproque sur I, il faut : OPTIONS : ['f continue sur I et f(a) × f(b) < 0', 'f continue et strictement monotone sur I', 'f dérivable et f(0) = 0']

### Diapo 53 `lc_r5_sens` — Même sens de variation
VOIX (fr) : Faut-il dériver f moins un pour connaître son sens de variation ? Non. Regarde le tableau de f, strictement décroissante sur a, b. Et celui de f moins un sur f de b, f de a. Les deux lignes s'échangent : la ligne des x devient la ligne des images. Et la flèche descend toujours. f moins un a le même sens de variation que f. Et f continue, donc f moins un continue sur J. Rien à calculer.
ÉCRAN : f⁻¹ a le même sens de variation que f : rien à dériver. | Le tableau de f⁻¹ s'obtient en échangeant les lignes du tableau de f. | f strictement décroissante sur I = [a ; b] : f⁻¹ strictement décroissante sur J = [f(b) ; f(a)]. | f continue sur I, donc f⁻¹ continue sur J.

### Diapo 54 `lc_r6_miroir` — Le miroir y = x
VOIX (fr) : Où est la courbe de f moins un ? Traçons d'abord la droite y égale x, en pointillés : c'est le miroir. Le point M de coordonnées un, deux est sur la courbe de f. Son reflet M prime a les coordonnées échangées : deux, un. Maintenant M glisse sur la courbe de f, et son reflet M prime trace la courbe de f moins un. Je relis : la courbe de f moins un est la symétrique de la courbe de f par rapport à la droite y égale x.
ÉCRAN : M(a ; b) sur (C_f) donne M′(b ; a) sur (C_f⁻¹) : on échange les coordonnées. | M et M′ sont symétriques par rapport à la droite d'équation y = x. | Dans un repère orthonormé, (C_f⁻¹) et (C_f) sont symétriques par rapport à la droite d'équation y = x (la première bissectrice). | Exemple : f(x) = x² + 1, x ≥ 0 ; (C_f⁻¹) : y = √(x − 1).

### Diapo 55 `lc_r7_construire` — Construire la courbe de f⁻¹ au national
VOIX (fr) : Au national, construire la courbe de g moins un rapporte presque un point. Le correcteur regarde trois choses. Un : la droite y égale x, tracée d'abord. Deux : les points échangés. Trois : les asymptotes. Ici, f de x égale deux plus un sur x, avec l'asymptote horizontale y égale deux. Son reflet est la courbe de f moins un. Et l'asymptote horizontale y égale deux devient l'asymptote verticale x égale deux. L'axe des ordonnées, x égale zéro, devient l'axe des abscisses, y égale zéro. La droite x égale deux est asymptote à la courbe de f : quelle droite est asymptote à la courbe de f moins un ?
ÉCRAN : Tracer d'abord la droite d'équation y = x. | Reporter les points connus de (C_f) en échangeant leurs coordonnées. | Une asymptote verticale x = a devient l'asymptote horizontale y = a, et inversement. | Les tangentes viennent au chapitre dérivation.
QUESTION : La droite d'équation x = 2 est asymptote à (C_f). Quelle droite est asymptote à (C_f⁻¹) ? OPTIONS : ['x = −2', 'y = 2', 'y = x']

### Diapo 56 `lc_r8_expression` — L'expression : la ligne pivot
VOIX (fr) : Pour trouver l'expression de f moins un, une ligne pivot. Ici f de x égale racine de x moins un, sur un, plus l'infini, et J égale zéro, plus l'infini. On prend x dans J et y dans I. f moins un de x égale y équivaut à f de y égale x. Attention à l'ordre : c'est f de y, pas f de x. Donc racine de y moins un égale x. Ai-je le droit d'élever au carré ? Oui, x est positif car x est dans J. y moins un égale x carré, donc y égale x carré plus un. On conclut avec x seul : f moins un de x égale x carré plus un.
ÉCRAN : f(x) = √(x − 1) sur I = [1 ; +∞[ ; J = f(I) = [0 ; +∞[. | Ligne pivot : pour x ∈ J et y ∈ I, f⁻¹(x) = y ⇔ f(y) = x. | √(y − 1) = x ⇔ y − 1 = x² (on a le droit d'élever au carré : x ≥ 0) ⇔ y = x² + 1. | Donc, pour tout x de [0 ; +∞[, f⁻¹(x) = x² + 1.

### Diapo 57 `lc_r9_valeur_absolue` — L'expression : la forme canonique d'abord
VOIX (fr) : Un exemple complet. f de x égale x carré plus deux x moins trois, sur moins un, plus l'infini, et J égale moins quatre, plus l'infini. La ligne pivot : f de y égale x, donc y carré plus deux y moins trois égale x. Maintenant la forme canonique : y carré plus deux y, c'est le début de y plus un, au carré, car y plus un au carré égale y carré plus deux y plus un. Donc y carré plus deux y moins trois égale y plus un au carré, moins quatre. Autrement : on a ajouté un et retiré un, le nombre n'a pas changé. Donc y plus un, au carré, égale x plus quatre.
ÉCRAN : f(x) = x² + 2x − 3 sur I = ]−1 ; +∞[ ; J = f(I) = ]−4 ; +∞[. | f(y) = x ⇔ y² + 2y − 3 = x. | Forme canonique : y² + 2y − 3 = (y + 1)² − 4, donc (y + 1)² = x + 4.

### Diapo 58 `lc_r9_valeur_absolue_b` — Racine et valeur absolue
VOIX (fr) : Maintenant je veux prendre la racine de y plus un, au carré. Ai-je le droit ? Oui : x plus quatre est positif, car x est dans J. Rappel : la racine d'un carré, c'est une valeur absolue. Donc valeur absolue de y plus un égale racine de x plus quatre. Et comme y est dans I, y plus un est positif : la valeur absolue s'en va. Donc f moins un de x égale racine de x plus quatre, moins un.
ÉCRAN : On a le droit de prendre la racine : x + 4 > 0 car x ∈ J ; √((y + 1)²) = |y + 1|. | y ∈ I donc y + 1 > 0 : |y + 1| = y + 1. Donc f⁻¹(x) = √(x + 4) − 1.
## VII. Racine n-ième et puissances rationnelles

### Diapo 59 `lc_n1_defaire` — Défaire la puissance n
VOIX (fr) : Tu connais la racine carrée : elle défait le carré. Racine de neuf égale trois, parce que trois au carré égale neuf. En fait, la racine carrée a un indice deux qu'on n'écrit pas. Regarde la courbe de x cube. L'aller : deux au cube égale huit. Maintenant on part de huit sur l'axe des ordonnées. Le retour mène à deux. C'est la racine cubique : racine cubique de huit égale deux, car deux au cube égale huit. La racine n-ième défait la puissance n. Que vaut la racine cubique de vingt-sept ?
ÉCRAN : La racine carrée défait le carré : √9 = 3 car 3² = 9 (√ est la racine d'indice 2). | La racine cubique défait le cube : ∛8 = 2 car 2³ = 8. | La racine n-ième défait la puissance n : ⁿ√a = b car bⁿ = a (a et b positifs).
QUESTION : ∛27 = OPTIONS : ['9', '3', '27/3']

### Diapo 60 `lc_n2_reciproque_xn` — ⁿ√ : la réciproque de xⁿ sur [0 ; +∞[
VOIX (fr) : x puissance n est continue et strictement croissante sur zéro, plus l'infini. Donc elle a une fonction réciproque : c'est la racine n-ième. Regarde la courbe de x cube, puis la droite y égale x. Le reflet est la courbe de la racine cubique. Je relis : racine n-ième de x égale y équivaut à x égale y puissance n, pour x et y positifs. Change n toi-même : deux, trois, quatre. Toutes passent par zéro, zéro et un, un. Au programme, on ne met rien de négatif sous la racine n-ième.
ÉCRAN : Pour n ∈ ℕ* : x ↦ xⁿ est continue et strictement croissante sur [0 ; +∞[ : elle admet une fonction réciproque. | Cette réciproque est la racine n-ième, définie sur [0 ; +∞[ : ⁿ√x = y ⇔ x = yⁿ (x ≥ 0, y ≥ 0). | Sa courbe est le reflet de celle de xⁿ par rapport à y = x ; toutes passent par (0 ; 0) et (1 ; 1). | Au programme, rien de négatif sous la racine n-ième, même si n est impair.

### Diapo 61 `lc_n3_regles` — Les règles de la racine carrée, en grand
VOIX (fr) : Bonne nouvelle : les règles de la racine carrée restent vraies pour la racine n-ième. À gauche, ce que tu connais. À droite, la même chose en grand. Le produit : racine n-ième de x fois racine n-ième de y égale racine n-ième de x y. Le quotient, avec y strictement positif. La puissance : racine n-ième de x, puissance n, égale x. Et deux racines emboîtées : on multiplie les indices. Toujours avec des nombres positifs. Exemple : racine cubique de cinq fois racine cubique de sept égale racine cubique de trente-cinq.
ÉCRAN : ⁿ√x × ⁿ√y = ⁿ√(x·y) (x ≥ 0, y ≥ 0). | ⁿ√x/ⁿ√y = ⁿ√(x/y) (x ≥ 0, y > 0). | (ⁿ√x)ⁿ = x et ⁿ√(xⁿ) = x (x ≥ 0). | ⁿ√(ᵐ√x) = ⁿᵐ√x : on multiplie les indices ; ⁿᵐ√(xᵐ) = ⁿ√x. | ⁿ√x = ⁿ√y ⇔ x = y (x ≥ 0, y ≥ 0) ; ¹√x = x.

### Diapo 62 `lc_n4_simplifier` — Simplifier en quatre étapes
VOIX (fr) : Simplifions B égale racine quatrième de neuf, fois racine de neuf, sur racine huitième de quatre-vingt-un. Étape un : tout en puissances de trois. Neuf égale trois au carré. Quatre-vingt-un égale neuf fois neuf, donc trois puissance quatre, pas trois au cube. Étape deux : racine quatrième de trois au carré, on divise l'indice et l'exposant par deux, racine de trois. Racine de neuf, trois. Racine huitième de trois puissance quatre, racine de trois. Étape trois : racine de trois en haut et en bas se simplifie. Il reste trois. Simplifie racine huitième de quatre-vingt-un.
ÉCRAN : B = (⁴√9 × √9)/⁸√81. | Tout en puissances de 3 : 9 = 3², 81 = 9 × 9 = 3⁴ (pas 3³). | ⁴√9 = ⁴√(3²) = √3 ; √9 = 3 ; ⁸√81 = ⁸√(3⁴) = √3. | B = (√3 × 3)/√3 = 3.
QUESTION : ⁸√81 = OPTIONS : ['√3', '3', '∛3']

### Diapo 63 `lc_n6_equation` — L'équation xⁿ = a : n pair
VOIX (fr) : Pour résoudre x puissance n égale a, on regarde d'abord n, puis a. À gauche, n pair : x puissance quatre. La droite y égale seize coupe la courbe en deux points : x égale deux ou x égale moins deux. La droite y égale moins seize ne la coupe pas : aucune solution, une puissance paire n'est jamais négative. Autrement : deux puissance quatre, seize ; moins deux puissance quatre, seize aussi, car moins fois moins donne plus.
ÉCRAN : n pair, a > 0 : deux solutions, x = ⁿ√a ou x = −ⁿ√a (x⁴ = 16 : x = 2 ou x = −2). | n pair, a < 0 : aucune solution (x⁴ = −16).

### Diapo 64 `lc_n6_equation_b` — L'équation xⁿ = a : n impair
VOIX (fr) : À droite, n impair : x cube. La courbe monte toujours, donc chaque droite horizontale la coupe une seule fois. y égale huit : une solution, deux. y égale moins vingt-sept : une solution aussi, moins racine cubique de vingt-sept, c'est-à-dire moins trois. Le tableau en bas réunit les quatre cas : d'abord la parité de n, ensuite le signe de a.
ÉCRAN : n impair, a > 0 : x = ⁿ√a ; a < 0 : x = −ⁿ√(−a) (x³ = −27 : x = −3). | D'abord la parité de n, ensuite le signe de a.

### Diapo 65 `lc_p1_exposant` — x^(1/n) : une autre écriture de ⁿ√x
VOIX (fr) : Une autre façon d'écrire une racine : avec un exposant en fraction. Toujours pour x strictement positif. Regarde : x puissance un demi, au carré, égale x puissance deux sur deux, donc x. Et racine de x, au carré, égale x aussi. Donc x puissance un demi, c'est racine de x. En général, x puissance un sur n égale racine n-ième de x. Exemple : huit puissance un tiers égale racine cubique de huit, deux. Attention : x puissance un sur n n'est pas un sur x puissance n.
ÉCRAN : Pour x > 0 : x^(1/n) = ⁿ√x. | Pourquoi : (x^(1/2))² = x^(2/2) = x, comme (√x)² = x. | 8^(1/3) = ∛8 = 2. | Attention : x^(1/n) n'est pas 1/xⁿ.

### Diapo 66 `lc_p2_pq` — x^(p/q), pour x strictement positif
VOIX (fr) : Et un exposant p sur q ? Pour x strictement positif, x puissance p sur q égale la racine q-ième de x puissance p. Le dénominateur est l'indice, le numérateur est l'exposant. Exemple : huit puissance deux tiers. Première façon : racine cubique de huit au carré, racine cubique de soixante-quatre, quatre. Deuxième façon : racine cubique de huit, au carré, deux au carré, quatre. Même résultat. Et dans l'autre sens : racine cinquième de x cube égale x puissance trois cinquièmes.
ÉCRAN : Pour x > 0, p ∈ ℤ et q ∈ ℕ* : x^(p/q) = ᑫ√(xᵖ) : le dénominateur q est l'indice, le numérateur p est l'exposant. | 8^(2/3) = ∛(8²) = ∛64 = 4, ou bien (∛8)² = 2² = 4. | ⁵√(x³) = x^(3/5) (x > 0).

### Diapo 67 `lc_p3_regles_puissances` — Les règles des puissances restent vraies
VOIX (fr) : Les règles des puissances que tu connais restent vraies avec des exposants en fraction, pour x positif. Pour un produit, on additionne les exposants. Exemple : A égale racine cubique de quatre, fois deux puissance un tiers, fois racine de deux. Tout en puissances de deux : deux puissance deux tiers, fois deux puissance un tiers, fois deux puissance un demi. On additionne : deux tiers plus un tiers plus un demi, trois demis. Deux puissance trois demis, c'est deux fois racine de deux. Deux puissance un demi, fois deux puissance un tiers, égale deux puissance combien ?
ÉCRAN : x^r × x^s = x^(r+s) ; (x^r)^s = x^(rs) ; x^r/x^s = x^(r−s) ; (xy)^r = x^r × y^r (x > 0, y > 0). | 1/x^r = x^(−r) (x > 0). | A = ∛4 × 2^(1/3) × √2 = 2^(2/3) × 2^(1/3) × 2^(1/2). | = 2^(2/3 + 1/3 + 1/2) = 2^(3/2) = 2√2. | Choisis l'écriture qui rend le calcul facile : racine ou exposant.
QUESTION : 2^(1/2) × 2^(1/3) = 2 puissance… OPTIONS : ['1/6', '5/6', '1/5']
## VIII. Limites et continuité avec ⁿ√u

### Diapo 68 `lc_lr1_continuite` — ⁿ√u : continuité et limite directe
VOIX (fr) : La racine n-ième se comporte comme la racine carrée. Deux machines : u de x égale x plus un, puis la racine cubique. Si u est continue et positive sur I, alors racine n-ième de u est continue sur I. Et pour la limite : x tend vers plus l'infini, u tend vers plus l'infini, et la racine cubique de u aussi. Exemple : racine cubique de x plus un, plus racine de x. Les deux termes tendent vers plus l'infini : plus l'infini plus plus l'infini, ce n'est pas indéterminé. On conclut directement : plus l'infini.
ÉCRAN : ⁿ√u est continue sur I si u est continue et positive sur I. | lim_{x→+∞} ⁿ√x = +∞ ; si lim u = ℓ ≥ 0, alors lim ⁿ√u = ⁿ√ℓ ; si lim u = +∞, alors lim ⁿ√u = +∞. | lim_{x→+∞} (∛(x + 1) + √x) : « +∞ + ∞ », pas d'indétermination : +∞. | On écrit sous chaque terme sa limite, puis on conclut.

### Diapo 69 `lc_lr4_infini` — ∞ − ∞ avec racines : le plus lourd
VOIX (fr) : Dernière limite : racine cubique de x carré moins x, moins x, en plus l'infini. Je remplace : plus l'infini moins l'infini. Le conjugué serait long. On compare d'abord les poids : racine cubique de x carré, c'est x puissance deux tiers, plus léger que x. Le plus lourd gagne : on met x en facteur. Il reste x, fois racine cubique de un sur x moins un sur x carré, moins un. Regarde chaque morceau : où va la racine, où va la parenthèse, où va x. Question : calcule cette limite.
ÉCRAN : ∛(x² − x) − x en +∞ : « +∞ − ∞ ». | Poids : ∛(x² − x) se comporte comme x^(2/3), plus léger que x. | Le plus lourd en facteur : x(∛(x² − x)/x − 1) = x(∛(1/x − 1/x²) − 1) : à toi de conclure.
QUESTION : lim [∛(x² − x) − x] quand x → +∞ : OPTIONS : ['0', '+∞', '−∞']
## IX. Un problème national, question par question, et le bilan

### Diapo 70 `lc_e1_probleme` — Un problème national : ce chapitre dedans
VOIX (fr) : Un problème comme au national, avec tout le chapitre dedans. f de x égale x cube plus x moins un. Quatre questions : les limites, le sens de variation, la solution unique, et la fonction réciproque. On avance question par question. Question un : les limites. Rappel : à l'infini, on garde le terme de plus haut degré. Question : quelle est la limite de f en plus l'infini ?
ÉCRAN : f(x) = x³ + x − 1 sur ℝ. | Quatre questions, une à la fois : limites, sens de variation, solution unique α, réciproque. | Question 1 : à l'infini, le terme de plus haut degré.
QUESTION : f(x) = x³ + x − 1. lim f(x) quand x → +∞ : OPTIONS : ['−∞', '+∞', '1']

### Diapo 71 `lc_e1_probleme_b` — Question 2 : le sens de variation
VOIX (fr) : Question deux : le sens de variation. Pour savoir si f monte ou descend, on calcule sa dérivée. f prime de x égale trois x carré plus un. Regarde x carré : peut-il être négatif ? Réfléchis. Question : quel est le signe de f prime de x ?
ÉCRAN : f′(x) = 3x² + 1. | x² ≥ 0 : quel est le signe de 3x² + 1 ?
QUESTION : f′(x) = 3x² + 1. Sur ℝ : OPTIONS : ['f′(x) < 0', 'f′(x) > 0', 'f′ change de signe en 0']

### Diapo 72 `lc_e1_probleme_b2` — Question 2 : le tableau de variations
VOIX (fr) : Maintenant on construit le tableau de variations, ligne par ligne. Première ligne : x, de moins l'infini à plus l'infini. Deuxième ligne : le signe de f prime, plus, car f prime est positive. Troisième ligne : f, une flèche qui monte. Il reste les deux bouts de la flèche. En plus l'infini, on l'a trouvée à la question un. En moins l'infini, même méthode : le terme de plus haut degré. Question : qu'écrit-on aux deux bouts de la flèche ?
ÉCRAN : x : de −∞ à +∞. | f′(x) : + (question précédente). | f : une flèche qui monte. Que met-on à ses deux bouts ?
QUESTION : Tableau de variations de f(x) = x³ + x − 1 : aux deux bouts de la flèche de f, on écrit : OPTIONS : ['−∞ à gauche, +∞ à droite', '−1 à gauche, 1 à droite', '+∞ à gauche, −∞ à droite']

### Diapo 73 `lc_e1_probleme_unique` — Question 3 : une solution unique dans ℝ
VOIX (fr) : Question trois : montrer que l'équation f de x égale zéro admet une solution unique dans R. On rassemble ce qu'on a. f est continue sur R, car c'est un polynôme. f est strictement croissante sur R : on l'a trouvé à la question deux. Et les limites : moins l'infini en moins l'infini, plus l'infini en plus l'infini. Il reste un argument pour dire unique. Question : quel est cet argument ?
ÉCRAN : f est continue sur ℝ (polynôme). | f est strictement croissante sur ℝ (question 2). | lim_{x→−∞} f(x) = −∞ ; lim_{x→+∞} f(x) = +∞. | Quel argument permet de dire : une solution unique ?
QUESTION : f est continue et strictement croissante sur ℝ, lim_{x→−∞} f(x) = −∞ et lim_{x→+∞} f(x) = +∞. Quel argument donne une solution unique de f(x) = 0 dans ℝ ? OPTIONS : ['0 ∈ f(ℝ) = ℝ', 'f(0) = −1 < 0', 'f′(0) = 1 > 0']

### Diapo 74 `lc_e1_probleme_tvi` — Question 3 : où est α ?
VOIX (fr) : Question trois, suite : où est alpha ? f est continue et strictement croissante. On nous donne deux valeurs. f de un demi égale moins trois sur huit : un point sous l'axe. f de un égale un : un point au-dessus de l'axe. Question : où est alpha ?
ÉCRAN : f est continue et strictement croissante sur [1/2 ; 1]. | f(1/2) = −3/8 < 0 ; f(1) = 1 > 0. | Quel encadrement de α écrit-on ?
QUESTION : f(1/2) = −3/8 et f(1) = 1. Quel encadrement de α écrit-on ? OPTIONS : ['1/2 < α < 1', '1/2 ≤ α ≤ 1', '0 < α < 1/2']

### Diapo 75 `lc_e1_probleme_c` — Question 4 : la fonction réciproque
VOIX (fr) : Question quatre : la fonction réciproque. f est continue et strictement croissante sur R. Pour trouver J, on prend les limites : en moins l'infini, moins l'infini ; en plus l'infini, plus l'infini. Question : sur quel ensemble la réciproque de f est-elle définie ?
ÉCRAN : f est continue et strictement croissante sur ℝ. | lim_{x→−∞} f(x) = −∞ ; lim_{x→+∞} f(x) = +∞ : J = ?
QUESTION : f admet une fonction réciproque définie sur : OPTIONS : ['[0 ; +∞[', 'ℝ', ']0 ; 1[']

### Diapo 76 `lc_e1_probleme_d` — Question 4 : construire la courbe de f⁻¹
VOIX (fr) : Suite de la question quatre : tracer la courbe de f moins un, dans le même repère. Voici la courbe de f. On trace la droite y égale x. La règle : dans un repère orthonormé, la courbe de f moins un est la symétrique de la courbe de f, par rapport à la droite y égale x. On prend deux points de la courbe de f : A zéro, moins un, et B un, un. Question : le point A devient quel point sur la courbe de f moins un ?
ÉCRAN : Dans un repère orthonormé, (C_f⁻¹) est la symétrique de (C_f) par rapport à la droite d'équation y = x. | A(0 ; −1) et B(1 ; 1) sont sur (C_f). | Quel point de (C_f⁻¹) vient de A ?
QUESTION : A(0 ; −1) est sur (C_f). Quel point est sur (C_f⁻¹) ? OPTIONS : ['A′(−1 ; 0)', 'A′(0 ; 1)', 'A′(1 ; 0)']

### Diapo 77 `lc_e2_bilan` — Ce qu'il faut retenir
VOIX (fr) : Faisons le bilan sur une seule fiche, bloc par bloc, et écris avec moi. Un : les limites. On remplace d'abord. Quatre formes indéterminées, et un outil pour chacune. Attention au signe de zéro. Deux : la continuité en a. Je relis : f est continue en a si la limite de f de x, quand x tend vers a, égale f de a. Trois : la continuité sur un intervalle. Pour racine de u, u continue et u positive. Quatre : l'image d'un intervalle. Croissante, même ordre. Décroissante, on inverse. Ouvert, une limite. Cinq : les valeurs intermédiaires. Continue, produit négatif : au moins une solution. Strictement monotone en plus : une seule. Six : la fonction réciproque. Continue et strictement monotone, définie sur J égale f de I. Sept : sa courbe, symétrique par rapport à la droite y égale x. Huit : la racine n-ième, rien de négatif dessous. La deuxième page est la tienne : ce qu'il te reste à retravailler. Je te le dis tout de suite.
ÉCRAN : 1. Limites : on remplace d'abord. Formes indéterminées 0/0, ∞/∞, +∞ − ∞, 0 × ∞ : facteur (x − a), conjugué, plus haut degré. Usuelles : lim_{x→+∞} xⁿ = +∞ ; en −∞ : +∞ si n pair, −∞ si n impair ; lim_{x→±∞} 1/xⁿ = 0 ; ℓ × (±∞) (ℓ ≠ 0) : règle des signes. √(x²) = |x| ; lim_{x→0} sin(x)/x = 1. ⚠ k/0 : signe à droite et à gauche. | 2. Continuité en a : lim_{x→a} f(x) = f(a) ; continue à droite en a : lim_{x→a⁺} f(x) = f(a) ; à gauche : lim_{x→a⁻} f(x) = f(a) ; continue en a ⇔ continue à droite et à gauche en a. ⚠ f(a) avec la branche qui porte l'égalité. | 3. Continuité sur I : fonctions usuelles, somme, produit, quotient ((∀x ∈ I) v(x) ≠ 0) ; √u : u continue et (∀x ∈ I) u(x) ≥ 0. ⚠ La positivité se prouve. | 4. Image d'un intervalle (par une fonction continue : un intervalle ; d'un segment : un segment) : f continue strictement croissante : f([a ; b]) = [f(a) ; f(b)] ; décroissante : [f(b) ; f(a)] ; non monotone : [m ; M]. ⚠ Ouvert → limite, fermé → image. | 5. Valeurs intermédiaires : f continue sur [a ; b], f(a) × f(b) < 0 : au moins une solution dans ]a ; b[ ; strictement monotone en plus : solution unique α. f continue et strictement monotone sur I, k ∈ f(I) : f(x) = k admet une solution unique dans I. ⚠ α dans ]a ; b[. | 6. Fonction réciproque : f continue et strictement monotone sur I : f⁻¹ définie sur J = f(I), même sens de variation ; f⁻¹(x) = y ⇔ f(y) = x ; (∀x ∈ I) f⁻¹(f(x)) = x ; (∀x ∈ J) f(f⁻¹(x)) = x. ⚠ f⁻¹ n'est pas 1/f. | 7. Courbe de f⁻¹ : dans un repère orthonormé, symétrique de (C_f) par rapport à la droite d'équation y = x ; M(a ; b) → M′(b ; a). ⚠ Asymptote verticale ↔ horizontale. | 8. Racine n-ième (n ∈ ℕ*) : ⁿ√x = y ⇔ x = yⁿ (x, y ≥ 0) ; ⁿ√x × ⁿ√y = ⁿ√(x·y) ; x^(p/q) = ᑫ√(xᵖ) (x > 0) ; ⁿ√u continue si u est continue et positive. ⚠ Rien de négatif sous ⁿ√. | Page 2, ta page : ce qu'il te reste à retravailler, d'après tes réponses du cours (repris en mode libre, avec la méthode qui marche pour toi).

### Diapo 78 `lc_e3_carte` — La carte et tes points à revoir
VOIX (fr) : Dessinons la carte de tout le chapitre, en une seule image. Au centre : la continuité en a, la limite égale l'image. Première branche : les limites, on remplace d'abord. Deuxième branche : la continuité, en un point et sur un intervalle. Troisième branche : l'image d'un intervalle. Quatrième branche : les valeurs intermédiaires ; si l'énoncé dit solution unique, c'est elle, avec strictement monotone. Cinquième branche : la fonction réciproque ; si l'énoncé dit admet une fonction réciproque, deux conditions et J égale f de I. Sixième branche : sa courbe, le miroir y égale x. Et la dernière branche : la racine n-ième. Voilà la carte du chapitre. Au chapitre suivant, la dérivation, on s'en servira tout le temps. Les branches entourées en rouge, ce sont celles qu'on va reprendre ensemble.
ÉCRAN : Au centre : la continuité en a, lim_{x→a} f(x) = f(a). | Limites : remplacer d'abord ; 0/0, ∞/∞, +∞ − ∞, 0 × ∞. | Continuité : en a, lim_{x→a} f(x) = f(a) (à droite et à gauche) ; sur I, usuelles, opérations, √u. | Image d'un intervalle : f([a ; b]) = [f(a) ; f(b)] ; ouvert → limite. | « Admet une solution unique » → valeurs intermédiaires + strictement monotone. | « Admet une fonction réciproque définie sur J » → continue, strictement monotone, J = f(I). | « Construire la courbe de f⁻¹ » → symétrie par rapport à la droite d'équation y = x (repère orthonormé). | Racine n-ième : ⁿ√x = y ⇔ x = yⁿ ; x^(1/n) = ⁿ√x (x > 0).

### Diapo 79 `lc_fermeture_cours` — Ce qu'il faut retenir, et comment réviser
VOIX (fr) : Nous arrivons à la fin du cours : Limites et continuité. Que faut-il retenir ? Trois idées. Première : f est continue en a si la limite de f quand x tend vers a est égale à f de a. Deuxième : f continue et strictement monotone sur a b, f de a fois f de b négatif : f de x égale zéro a une solution unique. Troisième : une fonction continue et strictement monotone a une fonction réciproque, dont la courbe est symétrique par rapport à la droite y égale x. Maintenant quelques conseils pour réviser. Relis ton cahier, et refais seul les exercices du national. Quand tu réponds, écris chaque étape, et chaque résultat avec sa justification, car chaque étape a ses points. Le jour de l'examen, partage ton temps, et commence par la question qui te paraît facile. La veille, dors bien. Écris ces conseils dans ton cahier. Tu as bien travaillé, bon courage ! Le prochain cours : Dérivation et étude des fonctions. On s'y retrouve !
ÉCRAN : Retenir : lim_{x→a} f(x) = f(a) · TVI : f(a)·f(b) < 0 · f⁻¹ : symétrie (y = x) | Réviser : relire le cahier, refaire les exercices du national | Rédiger : chaque étape, et sa justification (car…) | Jour J : gérer son temps · bien dormir la veille

## Questions de bloc (posées après la dernière diapo du bloc)
- après diapo 4 `lc_s1_b1` RETROUVER : Cahier fermé : par quoi commence le calcul de toute limite ?
- après diapo 4 `lc_s1_b1` EXERCICE : f(x) se rapproche de 3 quand x devient très grand : quelle écriture ? OPTIONS : ['lim f(x) = 3 quand x → +∞', 'f(+∞) = 3', 'lim f(x) = +∞ quand x → 3']
- après diapo 7 `lc_s1_b2` RETROUVER : Cahier fermé : écris les quatre formes indéterminées.
- après diapo 7 `lc_s1_b2` EXERCICE : Vrai ou faux ? OPTIONS : None
- après diapo 10 `lc_s1_b3` RETROUVER : Cahier fermé : factorise x² − 9.
- après diapo 10 `lc_s1_b3` EXERCICE : P(x) = x² − 5x + 6 et P(2) = 0. Alors : OPTIONS : ['P(x) = (x + 2)(x + 3)', 'P(x) = (x − 2)(x − 3)', 'P(x) = (x − 2)(x + 3)']
- après diapo 13 `lc_s1_b4` RETROUVER : Cahier fermé : calcule lim (x² − 9)/(x² − 4x + 3) quand x → 3, en écrivant l'étape où l'on simplifie.
- après diapo 13 `lc_s1_b4` EXERCICE : lim (x³ − 1)/(x − 1) quand x → 1 ? (x³ − 1 = (x − 1)(x² + x + 1)) OPTIONS : ['3', '1', '0']
- après diapo 16 `lc_s2_b1` RETROUVER : Cahier fermé : à quoi est égal √(x²) ?
- après diapo 16 `lc_s2_b1` EXERCICE : x² − 5x + 6 s'annule pour x = 2 et pour x = 3. Sa factorisation est : OPTIONS : ['(x − 5)(x + 6)', '(x + 2)(x + 3)', '(x − 2)(x − 3)']
- après diapo 19 `lc_s2_b2` RETROUVER : Cahier fermé : à quoi est égal √(x²) pour un réel x quelconque ?
- après diapo 19 `lc_s2_b2` EXERCICE : Vrai ou faux ? OPTIONS : None
- après diapo 22 `lc_s2_b3` RETROUVER : Cahier fermé : écris la limite de référence avec sin(x).
- après diapo 22 `lc_s2_b3` EXERCICE : lim (x² − 4)/(x − 2) quand x → 2 ? OPTIONS : ['4', '0', '2']
- après diapo 25 `lc_s2_b4` RETROUVER : Cahier fermé : écris la relation qui dit que f est continue en a.
- après diapo 25 `lc_s2_b4` EXERCICE : f(x) = x + 1 si x < 2 ; f(x) = x² − 1 si x ≥ 2. La limite de f à gauche de 2 vaut… OPTIONS : ['3', '1', '5']
- après diapo 29 `lc_s3_b0` RETROUVER : Cahier fermé : f est définie par deux expressions autour de a. Écris la double égalité qui prouve que f est continue en a.
- après diapo 29 `lc_s3_b0` EXERCICE : Pour f définie par deux expressions en a, que faut-il écrire avant de conclure « continue en a » ? OPTIONS : ["Seulement f(a), calculée avec l'expression valable en a", 'f(a), la limite à droite et la limite à gauche, égales à f(a)', "Seulement la limite à droite, calculée avec l'expression valable pour x > a"]
- après diapo 32 `lc_s3_b1` RETROUVER : Cahier fermé : à quelles deux conditions √u est-elle continue sur un intervalle I ?
- après diapo 32 `lc_s3_b1` EXERCICE : Sur quel intervalle la fonction x ↦ √(4 − 2x) est-elle continue ? OPTIONS : ['[2 ; +∞[', ']−∞ ; 2]', 'ℝ']
- après diapo 35 `lc_s3_b2` RETROUVER : Cahier fermé : à quoi est égal √(x²) ?
- après diapo 35 `lc_s3_b2` EXERCICE : x² − 5x + 6 s'annule pour x = 2 et pour x = 3. Sa factorisation est : OPTIONS : ['(x − 5)(x + 6)', '(x + 2)(x + 3)', '(x − 2)(x − 3)']
- après diapo 39 `lc_s3_b3` RETROUVER : Cahier fermé : f est continue et strictement croissante sur [a ; b]. Écris f([a ; b]).
- après diapo 39 `lc_s3_b3` EXERCICE : f(x) = x² + 1 est continue et strictement croissante sur [1 ; 3]. Détermine f([1 ; 3]). OPTIONS : None
- après diapo 42 `lc_s4_b1` RETROUVER : Cahier fermé : f est continue sur [a ; b] sans être monotone, de minimum m et de maximum M. Écris f([a ; b]).
- après diapo 42 `lc_s4_b1` EXERCICE : h est continue et strictement décroissante sur ]0 ; 2], lim h(x) = +∞ quand x → 0⁺, h(2) = 1. h(]0 ; 2]) = OPTIONS : [']1 ; +∞[', '[1 ; +∞[', ']−∞ ; 1]']
- après diapo 45 `lc_s4_b2` RETROUVER : Cahier fermé : énonce le théorème des valeurs intermédiaires pour l'équation f(x) = 0.
- après diapo 45 `lc_s4_b2` EXERCICE : Vrai ou faux ? OPTIONS : None
- après diapo 48 `lc_s4_b3` RETROUVER : Cahier fermé : écris les conditions qui donnent une solution UNIQUE α de f(x) = 0 dans ]a ; b[, puis la conclusion.
- après diapo 48 `lc_s4_b3` EXERCICE : Montre que l'équation x³ + x − 3 = 0 admet une solution unique α dans ]1 ; 2[. OPTIONS : None
- après diapo 51 `lc_s5_b1` RETROUVER : Cahier fermé : à quelles conditions f admet-elle une fonction réciproque, et sur quel ensemble est-elle définie ?
- après diapo 51 `lc_s5_b1` EXERCICE : f(x) = x + 1. Que vaut f⁻¹(x) ? OPTIONS : ['1/(x + 1)', 'x − 1', 'x + 1']
- après diapo 54 `lc_s5_b2` RETROUVER : Cahier fermé : quelle est la relation entre la courbe de f et celle de f⁻¹ ?
- après diapo 54 `lc_s5_b2` EXERCICE : Le point A(2 ; 5) est sur (C_f). Quel point est sur (C_f⁻¹) ? OPTIONS : ['(2 ; 5)', '(−2 ; −5)', '(5 ; 2)']
- après diapo 58 `lc_s5_b3` RETROUVER : Cahier fermé : écris l'équivalence qui sert à trouver l'expression de f⁻¹(x).
- après diapo 58 `lc_s5_b3` EXERCICE : f(x) = 2x + 3 est continue et strictement croissante sur ℝ, et f(ℝ) = ℝ. Détermine f⁻¹(x) pour tout x ∈ ℝ. OPTIONS : None
- après diapo 61 `lc_s6_b1` RETROUVER : Cahier fermé : écris la définition de ⁿ√x par une équivalence, avec les conditions.
- après diapo 61 `lc_s6_b1` EXERCICE : ∛2 × ∛4 = ? OPTIONS : ['∛6', '2', '8']
- après diapo 64 `lc_s6_b2` RETROUVER : Cahier fermé : x et y sont positifs. Écris le lien entre x < y et leurs racines n-ièmes.
- après diapo 64 `lc_s6_b2` EXERCICE : Résous dans ℝ l'équation x⁴ = 81. OPTIONS : None
- après diapo 67 `lc_s6_b3` RETROUVER : Cahier fermé : x > 0. Écris x^(p/q) avec une racine.
- après diapo 67 `lc_s6_b3` EXERCICE : 27^(2/3) = ? OPTIONS : ['18', '3', '9']
- après diapo 69 `lc_s6_b4` RETROUVER : Cahier fermé : à quelle condition ⁿ√u est-elle continue sur I ?
- après diapo 69 `lc_s6_b4` EXERCICE : lim_{x→+∞} ∛(x + 8) = ? OPTIONS : ['2', '+∞', '0']
- après diapo 76 `lc_s7_b1` RETROUVER : Cahier fermé : f est continue sur [a ; b] et k est compris entre f(a) et f(b). Que dit le théorème des valeurs intermédiaires ?
- après diapo 76 `lc_s7_b1` EXERCICE : f(1/2) = −3/8 et f(1) = 1. Quel encadrement de α écrit-on ? OPTIONS : ['1/2 < α < 1', '1/2 ≤ α ≤ 1', '0 < α < 1/2']
- après diapo 78 `lc_s7_b4` RETROUVER : Cahier fermé : écris les trois conditions qui donnent une solution unique de f(x) = 0 sur ]a ; b[.
- après diapo 78 `lc_s7_b4` EXERCICE : f est continue et strictement croissante sur [0 ; 1], f(0) = −1 et f(1) = 1. L'équation f(x) = 0 : OPTIONS : ["n'a pas de solution dans ]0 ; 1[", 'a une solution unique dans ]0 ; 1[', 'a au moins deux solutions dans ]0 ; 1[']
