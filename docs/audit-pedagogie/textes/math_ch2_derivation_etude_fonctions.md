# math_ch2_derivation_etude_fonctions — Dérivation et étude des fonctions

## I. Pourquoi dériver ; le nombre dérivé

### Diapo 1 `df_ouverture_cours` — Dérivation et étude des fonctions
VOIX (fr) : Bienvenue dans un nouveau cours : Dérivation et étude des fonctions. Dans ce cours, nous allons apprendre le nombre dérivé, la tangente, le calcul des dérivées, puis l'étude complète d'une fonction jusqu'à sa courbe. Le problème d'analyse du national est construit sur ce cours, et l'analyse compte pour cinquante-cinq pour cent de la note. Comment allons-nous travailler ? Tu écoutes bien, tu réponds aux questions au tableau, et quand le cours s'arrête, tu écris dans ton cahier. Allons-y !
ÉCRAN : On apprend : Nombre dérivé, tangente, dérivées, étude complète | Au bac : le problème d'analyse, 55 % de la note | Écouter · répondre au tableau · écrire dans le cahier

### Diapo 2 `df_c1_carte` — La carte du chapitre : cinq questions sur une courbe
VOIX (fr) : Avant de calculer, demandons-nous pourquoi. Devant une courbe, on se pose cinq questions. Un : où penche-t-elle ? C'est la tangente, avec la limite du taux et f prime de x zéro. Deux : monte-t-elle ou descend-elle ? C'est le signe de f prime. Trois : de quel côté est-elle creuse ? C'est le signe de f seconde. Quatre : où part-elle au bout ? Ce sont les limites et les branches infinies. Cinq : se répète-t-elle ? C'est la symétrie. Et tout finit dans le tracé : au national, c'est huit à onze points sur vingt.
ÉCRAN : Où penche la courbe ? → la tangente (limite du taux, f'(x₀)). | Monte-t-elle ou descend-elle ? → le signe de f'. | De quel côté est-elle creuse ? → le signe de f''. | Où part-elle au bout ? → les branches infinies (limites). | Se répète-t-elle ? → axe ou centre de symétrie. | Tout finit dans le tracé de la courbe : 8 à 11 points sur 20 au national.

### Diapo 3 `df_z1_pente` — Rappel 1 : la pente d'une droite
VOIX (fr) : Commençons par une notion de l'an dernier : la pente d'une droite, qu'on appelle aussi le coefficient directeur. La droite passe par A(1 ; 1) et B(3 ; 5). De A à B, on avance de 2 et on monte de 4 : la pente vaut 4 sur 2, soit 2. Autrement dit : à chaque pas de 1 vers la droite, on monte de 2. Si la droite descend, la pente est négative ; si elle est plate, elle est nulle. Je relis : la pente égale y_B moins y_A, sur x_B moins x_A.
ÉCRAN : Pente (coefficient directeur) de (AB) = (y_B − y_A)/(x_B − x_A). | A(1 ; 1), B(3 ; 5) : on avance de 2, on monte de 4 : pente = 4/2 = 2. | Elle monte : pente > 0 ; elle descend : pente < 0 ; plate : pente = 0.

### Diapo 4 `df_nd1_secante` — Entre deux points : la pente d'une sécante
VOIX (fr) : Regarde la parabole y égale x au carré. Le point A, en jaune, est fixe : A de coordonnées un et un. Le point M est un autre point de la courbe, ici en trois, neuf. La droite qui passe par A et M s'appelle une sécante. Sa pente, c'est la différence des ordonnées sur la différence des abscisses : f de x moins f de un, sur x moins un. Ici, neuf moins un sur trois moins un, égale quatre. Ce quotient s'appelle le taux d'accroissement de f entre un et x. Retiens : le taux, c'est la pente d'une sécante, entre deux points. M est en trois, neuf : quelle est la pente de la droite AM ?
ÉCRAN : A(1 ; 1) et M(x ; x²) sur la parabole y = x². | La droite (AM) est une sécante. | Sa pente : (f(x) − f(1))/(x − 1), c'est le taux d'accroissement de f entre 1 et x. | M en (3 ; 9) : pente (9 − 1)/(3 − 1) = 4.
QUESTION : M est en (3 ; 9) et A en (1 ; 1) : quelle est la pente de (AM) ? OPTIONS : ['4', '8', '2']

### Diapo 5 `df_nd2_rapprocher` — M se rapproche de A
VOIX (fr) : Maintenant, M glisse vers A, le long de la courbe. Regarde le petit tableau à droite. M en deux : la pente vaut trois. M en un virgule cinq : deux virgule cinq. La sécante pivote autour de A. M en un virgule un : deux virgule un. M en un virgule zéro un : deux virgule zéro un. M et A sont presque confondus. La pente ne grandit pas sans fin : elle se rapproche d'un nombre. On écrit : la limite, quand x tend vers un, du taux, égale ce nombre.
ÉCRAN : M glisse vers A : 3, puis 2, puis 1,5, puis 1,1, puis 1,01. | La pente de (AM) vaut 4, 3, 2,5, 2,1, 2,01. | La pente se rapproche d'un nombre : 2. | On écrit : lim (f(x) − f(1))/(x − 1) = 2 quand x tend vers 1.

### Diapo 6 `df_nd3_nombre_derive` — Le nombre dérivé et la tangente
VOIX (fr) : Construisons la définition avec trois questions. Que calcule-t-on ? La limite du taux, quand x tend vers x zéro. Que doit-on trouver ? Un réel, l, un nombre fini. Comment l'appelle-t-on ? Le nombre dérivé de f en x zéro, noté f prime de x zéro. Regarde : M arrive sur A, la sécante devient la tangente en A. Sa pente, c'est f prime de un, égale deux. Je relis : f est dérivable en x zéro, si la limite, quand x tend vers x zéro, de f de x moins f de x zéro, sur x moins x zéro, égale l, avec l un réel.
ÉCRAN : Quand M arrive sur A, la sécante devient la tangente en A. | f est définie sur un intervalle ouvert I contenant x₀. | La limite du taux, quand elle est un réel l, est le nombre dérivé f'(x₀). | f est alors dérivable en x₀, et f'(x₀) est la pente de la tangente. | Ici : f'(1) = 2. | Autre écriture (x = x₀ + h) : f′(x₀) = lim_{h→0} (f(x₀ + h) − f(x₀))/h.

### Diapo 7 `df_nd4_calcul` — Le calcul, ligne par ligne : un polynôme
VOIX (fr) : On rédige, pas à pas. Premier exemple : f(x) = x² en 1. D'abord f(1) = 1. Puis le taux (x² − 1)/(x − 1) : en remplaçant, 0/0, forme indéterminée. Polynôme : on factorise par x − 1, il reste x + 1, qui tend vers 2. 2 est un réel : f est dérivable en 1 et f′(1) = 2, la pente vue sur la parabole.
ÉCRAN : On calcule f(x₀) à part. | On écrit le taux ; en remplaçant on trouve « 0/0 » : forme indéterminée. | Polynôme : on factorise par (x − x₀), on simplifie. | On trouve un réel l : « donc f est dérivable en x₀ et f'(x₀) = l ».

### Diapo 8 `df_nd4_calcul_b` — Avec une racine : le conjugué
VOIX (fr) : Deuxième exemple, avec une racine : g(x) = √(x + 1) en 3. g(3) = 2. Le taux (√(x + 1) − 2)/(x − 3) donne 0/0, et il n'y a pas de polynôme à factoriser. On multiplie en haut et en bas par le conjugué √(x + 1) + 2 : le haut devient x − 3, on simplifie, il reste 1/(√(x + 1) + 2), qui tend vers 1/4. g est dérivable en 3 et g′(3) = 1/4.
ÉCRAN : g(x) = √(x + 1) en 3 : g(3) = √4 = 2. | Le taux (√(x + 1) − 2)/(x − 3) donne « 0/0 ». | On multiplie en haut et en bas par le conjugué √(x + 1) + 2. | En haut : (√(x + 1))² − 2² = x + 1 − 4 = x − 3 ; on simplifie par x − 3 (x ≠ 3). | Il reste 1/(√(x + 1) + 2) → 1/(√4 + 2) = 1/4 : g′(3) = 1/4.
QUESTION : Pour une racine, par quoi multiplie-t-on en haut et en bas ? OPTIONS : ['Par le conjugué, ici √(x + 1) + 2', 'Par x − 3', 'Seulement le haut, par √(x + 1) − 2']
EXERCICE : f(x) = x² − 3x + 4 : f est-elle dérivable en 1, et que vaut f'(1) ? OPTIONS : ['Non, le taux donne 0/0', "Oui, f'(1) = 2", "Oui, f'(1) = −1"]
## II. L'équation de la tangente

### Diapo 9 `df_z2_equation_droite` — Rappel 2 : l'équation d'une droite
VOIX (fr) : Maintenant l'équation d'une droite : y = ax + b. a est la pente ; b est l'endroit où la droite coupe l'axe des ordonnées. Exemple : y = 2x − 1. En x = 0, y = −1 ; puis à chaque pas de 1 vers la droite, on monte de 2. Autre façon de la voir : l'équation est un test. (2 ; 3) : 2 × 2 − 1 = 3, le point est sur la droite. (1 ; 3) : 2 × 1 − 1 = 1, pas 3 : il n'y est pas. Je relis : y = ax + b, a la pente, b l'ordonnée à l'origine.
ÉCRAN : y = ax + b : a est la pente, b l'ordonnée à l'origine. | y = 2x − 1 coupe l'axe des ordonnées en −1, et monte de 2 quand on avance de 1. | Un point est sur la droite si ses coordonnées vérifient l'équation : (2 ; 3) oui, (1 ; 3) non.
QUESTION : Quelle est la pente de la droite y = −3x + 2 ? OPTIONS : ['2', '−3', '3']

### Diapo 10 `df_tg1_equation` — L'équation de la tangente
VOIX (fr) : Une droite, il lui faut un point et une pente. Regarde la courbe de x plus un sur x, et le point A d'abscisse deux. La tangente en A passe par A, de coordonnées x zéro et f de x zéro. Sa pente, c'est le nombre dérivé, f prime de x zéro : regarde le petit triangle, un vers la droite, trois quarts vers le haut. Son équation s'écrit : y égale f prime de x zéro, facteur de x moins x zéro, plus f de x zéro. Et regarde dans le petit cercle : près de A, la courbe et sa tangente se confondent.
ÉCRAN : La tangente en A passe par A(x₀ ; f(x₀)). | Sa pente est f'(x₀). | Équation : (T) : y = f'(x₀)(x − x₀) + f(x₀). | Près de A, la courbe se confond avec sa tangente.

### Diapo 11 `df_tg2_ecrire` — Écrire une tangente
VOIX (fr) : Écrivons la tangente au point d'abscisse deux, pour f de x égale x plus un sur x. Il faut trois nombres. Un : f de deux, égale deux plus un demi, égale cinq demis. Deux : la dérivée, f prime de x، égale un moins un sur x au carré. Trois : f prime de deux, égale un moins un quart, égale trois quarts. On remplace dans la formule : y égale trois quarts, facteur de x moins deux, plus cinq demis. On développe : trois quarts x, moins trois demis, plus cinq demis. Donc y égale trois quarts x plus un.
ÉCRAN : f est dérivable en x₀ : on écrit pourquoi (« car … »). | f(x₀), puis f′(x), puis f′(x₀). | On remplace dans y = f′(x₀)(x − x₀) + f(x₀), puis on développe. | Exemple : f(x) = x + 1/x en 2 : f(2) = 5/2, f′(2) = 1 − 1/4 = 3/4, y = (3/4)(x − 2) + 5/2 = (3/4)x + 1. | Pour tracer (T) : un vecteur directeur u⃗(1 ; f′(x₀)) : depuis A, on avance de 1 et on monte de f′(x₀).

### Diapo 12 `df_tg3_verifier` — Vérifier sa tangente ; tangente horizontale
VOIX (fr) : Une erreur de calcul arrive vite. Voici le contrôle : le point de contact doit être sur la droite. On remplace x par deux dans y égale trois quarts x plus un : trois quarts fois deux, plus un, égale cinq demis. C'est bien f de deux : l'équation est juste. Maintenant, glissons A jusqu'à l'abscisse un. Là, f prime de un égale un moins un, égale zéro : la pente est nulle. La tangente est horizontale, d'équation y égale f de un, égale deux. La droite y égale trois quarts x plus un passe-t-elle par le point deux, cinq demis ?
ÉCRAN : Le point de contact doit être sur la droite : (3/4) × 2 + 1 = 5/2 ✓. | Si f'(x₀) = 0, la tangente est horizontale : y = f(x₀). | Pour x + 1/x : f'(1) = 0, tangente horizontale y = 2.
QUESTION : La droite y = (3/4)x + 1 passe-t-elle par le point (2 ; 5/2) ? OPTIONS : ['Oui : (3/4) × 2 + 1 = 5/2', 'Non : (3/4) × 2 + 1 = 7/4', "On ne peut pas savoir sans f'"]
EXERCICE : Vrai ou faux ? OPTIONS : None
## III. À droite, à gauche : demi-tangentes et point anguleux

### Diapo 13 `df_dt1_droite` — Arriver par la droite
VOIX (fr) : Regarde cette courbe, celle de valeur absolue de x au carré moins un. Au point A, d'abscisse un, elle a un coin. Faisons arriver M par la droite, avec x plus grand que un. La sécante pivote, et le taux se rapproche de deux. On dit : f est dérivable à droite en un, et f prime à droite de un égale deux. Sur la courbe, on dessine une demi-tangente, seulement du côté droit de A, avec la pente deux. La phrase : la courbe admet au point A une demi-tangente à droite, de coefficient directeur deux.
ÉCRAN : f(x) = |x² − 1| près de A(1 ; 0) : la courbe a un coin. | M arrive par la droite (x > 1) : le taux tend vers 2. | f est dérivable à droite en 1 : f_d'(1) = 2. | (Cf) admet au point A une demi-tangente à droite de coefficient directeur 2. | Son équation : (T_d) : y = f_d′(1)(x − 1) + f(1) = 2(x − 1), avec x ≥ 1.

### Diapo 14 `df_dt2_gauche` — Arriver par la gauche
VOIX (fr) : Maintenant, M arrive par la gauche, avec x plus petit que un. Regarde le taux : moins un, puis il se rapproche de moins deux. Donc f est dérivable à gauche en un, et f prime à gauche de un égale moins deux. La courbe a une deuxième demi-tangente, du côté gauche de A, de coefficient directeur moins deux.
ÉCRAN : M arrive par la gauche (x < 1) : le taux tend vers −2. | f est dérivable à gauche en 1 : f_g'(1) = −2. | Une autre demi-tangente, à gauche de A, de coefficient directeur −2. | Son équation : (T_g) : y = f_g′(1)(x − 1) + f(1) = −2(x − 1), avec x ≤ 1.

### Diapo 15 `df_dt3_anguleux` — Dérivable ou point anguleux
VOIX (fr) : Mettons les deux côtés ensemble. À droite, la pente vaut deux ; à gauche, moins deux. Les deux demi-tangentes font un angle au point A. Je relis la règle : f est dérivable en x zéro, si elle est dérivable à droite et à gauche, et si f prime à droite، égale f prime à gauche. Ici, deux n'égale pas moins deux : f n'est pas dérivable en un, et A est un point anguleux. Attention : la courbe ne saute pas, f est continue en un. Dérivable donne continue, mais continue ne donne pas dérivable. f prime à droite de un égale deux et f prime à gauche de un égale moins deux : f est-elle dérivable en un ?
ÉCRAN : f est dérivable en x₀ si elle est dérivable à droite et à gauche et si f_d'(x₀) = f_g'(x₀). | Ici f_d'(1) = 2 ≠ f_g'(1) = −2 : f n'est pas dérivable en 1 ; A est un point anguleux. | Dérivable entraîne continue ; continue n'entraîne pas dérivable (|x² − 1| est continue en 1).
QUESTION : f_d'(1) = 2 et f_g'(1) = −2 : f est-elle dérivable en 1 ? OPTIONS : ['Non : les deux nombres sont différents, A est un point anguleux', 'Oui : les deux limites du taux existent, donc f est dérivable en 1', 'Oui : f est continue en 1, donc elle est aussi dérivable en 1']

### Diapo 16 `df_z5_un_sur_x` — Rappel 5 : 1 sur un tout petit nombre
VOIX (fr) : Un rappel : 1/x quand x s'approche de 0. x = 0,1 donne 10 ; x = 0,01 donne 100. Plus x est petit, plus 1/x est grand : quand x tend vers 0⁺, 1/x tend vers +∞ ; à gauche, vers −∞ ; et quand x est très grand, 1/x s'approche de 0. Autre façon : 1/x est le nombre de morceaux de longueur x dans une barre de longueur 1 : 10 morceaux de 0,1, 100 morceaux de 0,01. Je relis : lim 1/x = +∞ quand x tend vers 0⁺.
ÉCRAN : 1/0,1 = 10 ; 1/0,01 = 100 : quand x → 0⁺, 1/x → +∞. | Quand x → 0⁻, 1/x → −∞ ; quand x → +∞, 1/x → 0. | 1/x, c'est le nombre de morceaux de longueur x dans une barre de longueur 1.

### Diapo 17 `df_dt4_infini` — Quand le taux part à l'infini
VOIX (fr) : Prenons racine de x, en zéro. M descend vers O : regarde, la sécante se redresse. Le taux, c'est racine de x sur x, égale un sur racine de x : il vaut un, puis trois virgule seize, puis dix. Il grandit sans fin. Avant de conclure, on écrit vers quoi tend le haut et vers quoi tend le bas : le haut vaut un, le bas tend vers zéro plus, donc le taux tend vers plus l'infini. L'infini n'est pas un réel : f n'est pas dérivable à droite en zéro. Mais il y a quelque chose à dessiner : une demi-tangente verticale en O, dirigée vers le haut.
ÉCRAN : f(x) = √x en 0 : (f(x) − f(0))/(x − 0) = √x/x = 1/√x. | Quand x → 0⁺ : le haut vaut 1 et le bas √x → 0⁺, donc 1/√x → +∞ : ce n'est pas un réel. | f n'est pas dérivable à droite en 0. | Mais (Cf) admet au point O une demi-tangente verticale, dirigée vers le haut.

### Diapo 18 `df_dt5_sens` — Vers le haut ou vers le bas : à droite
VOIX (fr) : Quatre cas, chacun dans un petit repère. D'abord les deux cas à droite. Regarde où est la courbe : la flèche part du point vers elle. À droite, taux vers +∞ : x − x₀ est positif, donc f(x) − f(x₀) aussi : la courbe est au-dessus, la flèche monte. À droite, taux vers −∞ : la courbe est en dessous, la flèche descend.
ÉCRAN : La demi-tangente verticale part du point vers le côté où est la courbe. | À droite : +∞ → la courbe est au-dessus → vers le haut. | À droite : −∞ → la courbe est en dessous → vers le bas.

### Diapo 19 `df_dt5_sens_b` — Vers le haut ou vers le bas : à gauche
VOIX (fr) : Maintenant les deux cas à gauche. Attention : x − x₀ est négatif. À gauche, taux vers +∞ : le bas est négatif, donc pour un taux positif le haut f(x) − f(x₀) est négatif aussi : la courbe est en dessous, la flèche descend. À gauche, taux vers −∞ : la courbe est au-dessus, la flèche monte. Retiens : la demi-tangente part du côté où est la courbe.
ÉCRAN : À gauche, x − x₀ est négatif. | À gauche : +∞ → la courbe est en dessous → vers le bas. | À gauche : −∞ → la courbe est au-dessus → vers le haut. | Phrase : (Cf) admet au point A une demi-tangente verticale dirigée vers le haut (ou le bas).

### Diapo 20 `df_dt6_morceaux` — Une fonction en deux morceaux, comme au national
VOIX (fr) : Au national, la fonction est souvent écrite en deux morceaux. Ici : f de zéro égale zéro, x racine de x moins deux x si x est positif, x au cube plus trois x si x est négatif. La question clé : quelle ligne de quel côté ? À droite de zéro, x est positif : on prend x racine de x moins deux x. Le taux se simplifie en racine de x moins deux, qui tend vers moins deux. Une phrase : demi-tangente à droite de pente moins deux. À gauche, x est négatif : on prend x au cube plus trois x. Le taux devient x au carré plus trois, qui tend vers trois. Moins deux et trois sont différents : f n'est pas dérivable en zéro, O est un point anguleux. Pour x plus petit que zéro, quelle ligne de l'accolade utilise-t-on ?
ÉCRAN : f(0) = 0 ; f(x) = x√x − 2x si x > 0 ; f(x) = x³ + 3x si x ≤ 0. | À droite (x > 0) : la ligne x√x − 2x ; taux = (x√x − 2x)/x = √x − 2 → 0 − 2 = −2. | À gauche (x < 0) : la ligne x³ + 3x ; taux = (x³ + 3x)/x = x² + 3 → 0 + 3 = 3. | −2 ≠ 3 : f n'est pas dérivable en 0 ; O est un point anguleux.
QUESTION : Pour x < 0, quelle ligne de l'accolade utilise-t-on ? OPTIONS : ['x³ + 3x', 'x√x − 2x', 'f(0) = 0']
EXERCICE : Avec cette fonction, f_d'(0) = −2 et f_g'(0) = 3. Conclusion ? OPTIONS : ["f n'est pas continue en 0", "f est dérivable en 0 et f'(0) = 1", "f n'est pas dérivable en 0"]
## IV. Calculer une dérivée

### Diapo 21 `df_z3_deriver_polynome` — Rappel 3 : dériver un polynôme
VOIX (fr) : Dériver un polynôme. La règle : la dérivée de x puissance n est n fois x puissance n moins 1. Pour x³ : l'exposant 3 descend devant, puis on enlève 1 à l'exposant : 3x². Exemple : 3x² − 5x + 4, terme par terme : 6x, −5, et 0 pour la constante : f′(x) = 6x − 5. Autre façon : la dérivée donne la pente. y = 4 est plate, pente 0 ; y = −5x a pour pente −5. Je relis : (xⁿ)′ = n·xⁿ⁻¹.
ÉCRAN : (xⁿ)′ = n·xⁿ⁻¹ : l'exposant descend devant, puis il perd 1. | (k)′ = 0 ; (k·u)′ = k·u′ ; (u + v)′ = u′ + v′. | (3x² − 5x + 4)′ = 6x − 5.

### Diapo 22 `df_dv1_tableau` — Le tableau des dérivées : 1/x, √x, sin, cos
VOIX (fr) : On vient de dériver les polynômes. Deux dérivées de plus, de l'an dernier. (1/x)′ = −1/x² : pourquoi un moins ? Parce que la courbe de 1/x descend toujours, sa pente est négative. (√x)′ = 1/(2√x) pour x > 0 : la courbe de √x monte, mais de plus en plus lentement, sa pente devient petite. De l'an dernier aussi : (sin x)′ = cos x et (cos x)′ = −sin x. On vérifie autrement : en 0, la courbe de sinus monte avec la pente 1, et cos 0 = 1. Et (sin(ax + b))′ = a·cos(ax + b). Ce tableau se révise chaque jour jusqu'à l'examen.
ÉCRAN : Rappel : (k)′ = 0 ; (x)′ = 1 ; (xⁿ)′ = n·xⁿ⁻¹ (n entier, n ≠ 0 ; x ≠ 0 si n < 0). | (1/x)′ = −1/x² : la courbe de 1/x descend, sa pente est négative. | (√x)′ = 1/(2√x) (x > 0) : la courbe de √x monte, de moins en moins vite. | (sin x)′ = cos x ; (cos x)′ = −sin x ; (tan x)′ = 1 + tan²x = 1/cos²x (cos x ≠ 0). | (sin(ax + b))′ = a·cos(ax + b) ; (cos(ax + b))′ = −a·sin(ax + b).

### Diapo 23 `df_dv2_produit_quotient` — La dérivée d'un produit
VOIX (fr) : Commençons par le produit. La dérivée de u·v n'est pas u′·v′ : c'est u′v + uv′. Pourquoi deux termes ? Un rectangle de côtés u et v a pour aire u·v. Quand x avance un peu, u grandit : une bande à droite, u′·v ; v grandit : une bande en haut, u·v′. L'aire grandit de u′v + uv′. Exemple : x²(x + 1) : 2x(x + 1) + x² = 3x² + 2x. Vérification en développant : x³ + x², dérivée 3x² + 2x. Je relis : (u·v)′ = u′v + uv′.
ÉCRAN : (u·v)' = u'v + uv' — et pas u'·v'. | Un rectangle u × v qui grandit : une bande u'·v, une bande u·v'. | Exemple : (x²(x + 1))' = 2x(x + 1) + x² = 3x² + 2x.

### Diapo 24 `df_dv2_produit_quotient_b` — La dérivée d'un quotient
VOIX (fr) : Maintenant le quotient : (u′v − uv′)/v². Attention au moins au milieu, et à l'ordre : u′v d'abord. Et v ne doit pas s'annuler sur l'intervalle. Exemple : (2x + 1)/(x − 3) : u′ = 2, v′ = 1. On remplace avec une parenthèse autour de chaque produit : (2(x − 3) − (2x + 1)·1)/(x − 3)². Le moins entre dans toute la parenthèse : 2x − 6 − 2x − 1 = −7, donc −7/(x − 3)². Le bas reste factorisé. Cas particulier u = 1 : u′ = 0, donc (1/v)′ = −v′/v². Par exemple (1/(x² + 1))′ = −2x/(x² + 1)².
ÉCRAN : (u/v)′ = (u′v − uv′)/v², sur un intervalle où v ne s'annule pas. | Une parenthèse autour de chaque produit ; le dénominateur reste factorisé. | Exemple : ((2x + 1)/(x − 3))′ = (2(x − 3) − (2x + 1)·1)/(x − 3)² = (2x − 6 − 2x − 1)/(x − 3)² = −7/(x − 3)². | Cas u = 1 : (1/v)′ = −v′/v² ; exemple : (1/(x² + 1))′ = −2x/(x² + 1)².

### Diapo 25 `df_dv3_puissance` — Une puissance d'une expression
VOIX (fr) : Comment dériver x au carré moins deux x plus trois, le tout au cube ? Développer serait trop long. On nomme la parenthèse : c'est u. On dérive u à part, dans la marge : u prime égale deux x moins deux. Puis on remplit le gabarit : n fois u prime fois u puissance n moins un. On descend l'exposant trois, on multiplie par u prime, et on enlève un à l'exposant. Ça donne trois, fois deux x moins deux, fois la parenthèse au carré. L'erreur la plus fréquente, barrée en rouge : oublier u prime. Dérive la parenthèse au cube : quelle case oublie-t-on le plus souvent ?
ÉCRAN : (x² − 2x + 3)³ est u³ avec u = x² − 2x + 3. | On dérive u à part, dans la marge : u' = 2x − 2. | (uⁿ)' = n·u'·uⁿ⁻¹ : 3(2x − 2)(x² − 2x + 3)². | La case la plus oubliée : u'.
QUESTION : Dérive (x² − 2x + 3)³ : quelle case oublie-t-on le plus souvent ? OPTIONS : ["u', la dérivée de la parenthèse", "l'exposant 3", 'le carré de la parenthèse']
EXERCICE : Dérivée de g(x) = (3x − 1)⁴ ? OPTIONS : ['12(3x − 1)³', '4(3x − 1)³', '12(3x − 1)⁴']

### Diapo 26 `df_dv4_racine` — La racine d'une expression
VOIX (fr) : Même geste pour une racine. Le gabarit : u prime, sur deux racine de u. Retiens : u prime monte en haut. Exemple : racine de x au carré plus un. u égale x au carré plus un, u prime égale deux x. On remplace : deux x, sur deux racine de x au carré plus un. On simplifie par deux : x, sur racine de x au carré plus un. Le bas est positif, donc le signe de la dérivée est le signe de x. Dérive racine de x au carré plus un.
ÉCRAN : (√u)' = u'/(2√u), là où u > 0. | √(x² + 1) : u = x² + 1, u' = 2x. | (√(x² + 1))' = 2x/(2√(x² + 1)) = x/√(x² + 1). | √(x² + 1) > 0, donc le signe de la dérivée est le signe de x.

### Diapo 27 `df_dv5_racine_n` — La racine n-ième et la composée
VOIX (fr) : Une formule de plus, mais la même idée : u prime en haut. Pour la racine n-ième : u prime, sur n fois racine n-ième de u puissance n moins un. Exemple, racine cubique de x, pour x positif : u égale x, u prime égale un, n égale trois. La dérivée est un, sur trois fois racine cubique de x au carré. Et la règle générale de la composée : g prime de x fois، f prime de g de x. Elle est au programme, même si on la voit peu au national récent. Dérive racine cubique de x, pour x positif.
ÉCRAN : (ⁿ√u)' = u'/(n·(ⁿ√u)ⁿ⁻¹), là où u > 0. | (³√x)' = 1/(3(³√x)²) pour x > 0. | Composée : si g est dérivable en x₀ et f dérivable en g(x₀), alors f∘g est dérivable en x₀ et (f∘g)′(x₀) = g′(x₀)·f′(g(x₀)). | Au programme ; rare au national récent.

### Diapo 28 `df_dv5b_intervalle` — Dérivable sur un intervalle ; la fonction dérivée
VOIX (fr) : Question importante : où f est-elle dérivable ? Pas seulement en un point, mais sur un intervalle. f est dérivable sur l'intervalle ouvert ]a ; b[ si elle est dérivable en chaque point de cet intervalle. Si l'intervalle est fermé, [a ; b], il faut en plus : dérivable à droite en a et dérivable à gauche en b. Regarde la courbe de |x² − 1|. Sur [1 ; 2], aucun coin : f est dérivable sur [1 ; 2]. Mais sur [0 ; 2], il y a le point anguleux en 1 : f n'est pas dérivable sur [0 ; 2]. Autrement dit : dérivable sur l'intervalle, c'est une tangente en chaque point, sans coin et non verticale. Quand f est dérivable sur I, chaque x donne un nombre f′(x) : c'est la fonction dérivée f′. On connaît beaucoup de fonctions dérivables : un polynôme est dérivable sur ℝ ; une fonction rationnelle est dérivable sur chaque intervalle de son ensemble de définition ; √x est dérivable sur ]0 ; +∞[. Je relis : f est dérivable sur [a ; b] si elle est dérivable sur ]a ; b[, à droite en a et à gauche en b.
ÉCRAN : f est dérivable sur ]a ; b[ si elle est dérivable en tout point de ]a ; b[. | f est dérivable sur [a ; b] si elle est dérivable sur ]a ; b[, à droite en a et à gauche en b. | Exemple : |x² − 1| est dérivable sur [1 ; 2], mais pas sur [0 ; 2] (point anguleux en 1). | La fonction f′ : x ↦ f′(x) est la fonction dérivée de f. | Polynôme : dérivable sur ℝ ; fonction rationnelle : sur chaque intervalle de son domaine ; √x : sur ]0 ; +∞[.

### Diapo 29 `df_dv6_montrer` — « Montrer que f'(x) = … »
VOIX (fr) : Au national, cette question est dans tous les sujets : montrer que f prime de x égale une expression donnée. La réponse est déjà là : il faut y arriver. Première ligne, à ne jamais oublier : f est dérivable sur l'intervalle, avec sa raison, « car ». Ici, x + 1 est strictement positif sur ]−1 ; +∞[, donc √(x + 1) y est dérivable ; et x est dérivable sur ℝ. Donc f est dérivable sur ]−1 ; +∞[ car c'est un produit de deux fonctions dérivables. C'est un produit : u prime v plus u v prime. Un fois racine de x plus un, plus x fois un sur deux racine de x plus un. On réduit au même dénominateur, deux racine de x plus un : en haut, deux fois x plus un, plus x. On arrive à trois x plus deux, sur deux racine de x plus un : la forme de l'énoncé. Que doit-on écrire avant de calculer la dérivée ?
ÉCRAN : Première ligne : « f est dérivable sur I car … » : la raison est écrite. | Raisons : polynôme (sur ℝ) ; quotient dont le dénominateur ne s'annule pas sur I ; √u avec u > 0 sur I ; somme ou produit de fonctions dérivables. | On reconnaît la forme (produit, quotient, uⁿ, √u) et on dérive. | On réduit au même dénominateur, on factorise jusqu'à la forme de l'énoncé. | Exemple : f(x) = x√(x + 1) est dérivable sur ]−1 ; +∞[ car c'est le produit de x et de √(x + 1), avec x + 1 > 0 ; f′(x) = 1·√(x + 1) + x·1/(2√(x + 1)) = (2(x + 1) + x)/(2√(x + 1)) = (3x + 2)/(2√(x + 1)).
QUESTION : Que doit-on écrire avant de calculer la dérivée ? OPTIONS : ['« f est dérivable sur … »', '« f est continue en 0 »', 'Rien : on dérive directement']
EXERCICE : f(x) = x√(x + 1) : que vaut f'(0) ? OPTIONS : ['0', '2', '1']
## V. Signe de f' et variations

### Diapo 30 `df_va1_monte` — La courbe monte : f' est positive
VOIX (fr) : Regarde le point P qui glisse sur la courbe de x au cube moins trois x, avec sa tangente. Au début, la courbe monte : la tangente penche vers le haut, sa pente est positive. Sous la courbe, on écrit plus. Puis la courbe descend : la tangente penche vers le bas, la pente est négative, on écrit moins. La pente de la tangente, c'est f prime de x. Donc : dérivée positive, fonction croissante ; dérivée négative, fonction décroissante. C'est comme la route de montagne : on monte, la pente est positive. Et si f′ est nulle sur tout l'intervalle, la tangente est toujours horizontale : f est constante sur l'intervalle, comme une route plate.
ÉCRAN : Un point P glisse sur la courbe de f(x) = x³ − 3x avec sa tangente. | Quand la courbe monte, la tangente penche vers le haut : f'(x) > 0. | Quand la courbe descend, la tangente penche vers le bas : f'(x) < 0. | f' > 0 sur I : f strictement croissante sur I ; f' < 0 sur I : f strictement décroissante sur I. | f′ = 0 sur tout l'intervalle I : f constante sur I.

### Diapo 31 `df_va2_sommet` — Au sommet
VOIX (fr) : Suivons P quand la courbe change de sens. Elle monte, puis elle va descendre ; entre les deux, le sommet, en x = −1. Regarde la tangente au sommet. Elle est horizontale : pente 0, f′(−1) = 0. Avant −1, f′ est positive ; après, négative : f monte puis descend, et f(−1) = 2 est le maximum. Autre image : quand on monte une route et qu'on arrive en haut, la route n'est plus ni montante ni descendante : c'est l'instant où f′ = 0.
ÉCRAN : Au sommet (x = −1), la tangente est horizontale : f'(−1) = 0. | f' passe de + à − : f monte puis descend ; f(−1) = 2 est un maximum. | Image : en haut d'une route qui monte puis descend, la route est plate.
OBSERVATION : Au sommet, comment est la tangente ?

### Diapo 32 `df_va2_sommet_b` — Au creux ; la règle de l'extremum
VOIX (fr) : Continuons avec P jusqu'au creux, en x = 1. Là aussi la tangente est horizontale : f′(1) = 0. Mais à l'envers : avant 1, f′ est négative, après, positive : f descend puis monte, et f(1) = −2 est le minimum. Je relis : si f′ s'annule en x₀ en changeant de signe, f(x₀) est un extremum. Attention : « + 0 + », sans changement de signe, ce n'est pas un extremum. Exemple : x³. f′(x) = 3x² et f′(0) = 0. Mais 3x² est toujours positive : + 0 +. x³ monte toujours : pas d'extremum en 0. Dans l'autre sens, c'est vrai : si f est dérivable sur un intervalle ouvert et admet un extremum en a, alors f′(a) = 0.
ÉCRAN : Au creux (x = 1) : f′(1) = 0 ; f′ passe de − à + : minimum f(1) = −2. | f′ s'annule en x₀ en changeant de signe ⟹ f(x₀) est un extremum. | « + 0 + » : pas d'extremum. Exemple : x³ : f′(x) = 3x², f′(0) = 0, mais 3x² ≥ 0 : pas d'extremum en 0. | Si f est dérivable sur un intervalle ouvert I, a ∈ I, et si f admet un extremum en a, alors f′(a) = 0 (la réciproque est fausse : x³).

### Diapo 33 `df_z4_signe_produit` — Rappel 4 : le signe d'un produit
VOIX (fr) : Le signe d'un produit, pour faire un tableau de signe. x − 1 : négatif avant 1, positif après, nul en 1. De même x + 1 change de signe en −1. Le produit : dans chaque colonne, on multiplie les signes. Autre façon : on essaie des nombres : x = −2 donne 3, positif ; x = 0 donne −1, négatif ; x = 2 donne 3, positif. Les mêmes signes. Je relis : le signe d'un produit se lit dans un tableau, facteur par facteur.
ÉCRAN : x − 1 : négatif avant 1, nul en 1, positif après 1. | Un tableau : une ligne par facteur, puis la ligne du produit (− × − = +). | (x − 1)(x + 1) : + avant −1, − entre −1 et 1, + après 1.

### Diapo 34 `df_va3_factoriser` — Factoriser pour lire le signe
VOIX (fr) : Au national, le signe de f prime ne se voit jamais du premier coup. Le geste : factoriser. Ici, f est dérivable sur R, f prime de x، égale trois x au carré moins trois, égale trois, facteur de x moins un, fois x plus un. Puis on écarte ce qui est positif, en le disant : trois est positif. On écrit la phrase : le signe de f prime de x est le signe de x moins un, fois x plus un. Un carré, une racine, sont positifs aussi : on les écarte de la même façon. Ensuite, le tableau de signe, facteur par facteur.
ÉCRAN : f(x) = x³ − 3x est dérivable sur ℝ car c'est un polynôme ; on factorise f′(x) : 3x² − 3 = 3(x − 1)(x + 1). | On écarte les facteurs positifs en le disant : 3 > 0, un carré, une racine. | On écrit : « le signe de f'(x) est le signe de (x − 1)(x + 1) ». | Puis un tableau de signe.

### Diapo 35 `df_va4_tableau` — Le tableau de variations
VOIX (fr) : Le tableau de variations a toujours trois lignes. La ligne x : les bornes, moins l'infini et plus l'infini, et les valeurs où f prime s'annule, moins un et un. La ligne f prime de x : le signe, plus, zéro, moins, zéro, plus. La ligne f de x : une flèche qui monte là où c'est plus, qui descend là où c'est moins. Au bout de chaque flèche, une valeur : deux au sommet, moins deux au creux. Et aux deux bouts, les limites : moins l'infini à gauche, plus l'infini à droite. Que met-on au bout de la dernière flèche ?
ÉCRAN : Ligne x : les bornes du domaine et les valeurs où f' s'annule. | Ligne f'(x) : le signe. | Ligne f(x) : les flèches, les extremums, et les limites au bout. | x³ − 3x : −∞ ↗ 2 ↘ −2 ↗ +∞.
QUESTION : Que met-on au bout de la dernière flèche ? OPTIONS : ['La limite de f en +∞, ici +∞', "Le nombre dérivé f'(1), ici 0", "Rien : la flèche s'arrête au bord"]

### Diapo 36 `df_va5_double_barre` — La valeur exclue et le contrôle des flèches
VOIX (fr) : Deuxième fonction, notre fil rouge : f de x égale x plus un sur x, définie sauf en zéro. f prime de x، égale un moins un sur x au carré, égale x moins un, fois x plus un, sur x au carré. x au carré est positif : le signe de f prime de x est le signe de x moins un, fois x plus un. Mais zéro n'est pas dans le domaine : dans le tableau, c'est une double barre, sur les trois lignes. Ce n'est pas une racine : la double barre ne change pas forcément le signe. Puis le contrôle : chaque flèche doit aller vers la limite trouvée. En zéro plus, f tend vers plus l'infini, donc la flèche part d'en haut et descend vers deux.
ÉCRAN : f(x) = x + 1/x sur ℝ* : f′(x) = 1 − 1/x² = (x² − 1)/x² = (x − 1)(x + 1)/x². | x² > 0 : le signe de f'(x) est le signe de (x − 1)(x + 1). | 0 n'est pas dans le domaine : une double barre dans les trois lignes. | Chaque flèche va vers la limite trouvée : jamais une flèche qui monte vers −∞.

### Diapo 37 `df_va6_extremum` — Lire un extremum, un signe, une inégalité
VOIX (fr) : Le tableau donne des résultats sans calcul. Sur zéro, plus l'infini, la fonction descend jusqu'à deux, puis remonte. Deux est le minimum, atteint en un. Donc pour tout x positif, f de x est plus grand ou égal à deux. On remplace f de x par son expression : x plus un sur x, plus grand ou égal à deux. Voilà une inégalité démontrée par l'étude d'une fonction. Et si le minimum est positif, la fonction est positive.
ÉCRAN : Un minimum positif donne une fonction positive : f(x) ≥ m ≥ 0.

### Diapo 38 `df_va7_auxiliaire` — Quand le signe vient d'une autre fonction
VOIX (fr) : Au national, dans neuf sujets sur vingt, le signe de f prime vient d'une autre fonction, g, étudiée dans la partie un. Dans la partie un, on lit dans le tableau de g son minimum : ici g de un égale un, positif. Donc g de x est toujours positif. Dans la partie deux, on montre que f prime de x, égale g de x sur x au carré. x au carré est positif : le signe de f prime de x est le signe de g de x. La partie un sert à la partie deux. Si f prime de x, égale g de x sur x au carré, et g de x positive, quel est le sens de variation de f ?
ÉCRAN : Partie I : on étudie g et on montre g(x) ≥ 0 (minimum positif lu dans son tableau). | Partie II : on montre f'(x) = g(x)/x². | x² > 0 : f′ a le signe de g ; quel sens de variation pour f ?
QUESTION : Si f'(x) = g(x)/x² et g(x) ≥ 0, quel est le sens de variation de f ? OPTIONS : ['f est croissante', 'f est décroissante', 'On ne peut pas savoir']

### Diapo 39 `df_va8_aux_a` — Exercice, partie I : le signe de g′
VOIX (fr) : Maintenant un exercice complet, comme au national, une question à la fois. Partie un : g de x égale deux x au cube, moins trois x au carré, plus deux, sur zéro, plus l'infini. Pour connaître le signe de g, on fait son tableau de variations. D'abord la dérivée : g prime de x égale six x au carré moins six x. On factorise : six x, fois x moins un. Sur zéro, plus l'infini, six x est positif : le signe de g prime de x est le signe de x moins un. Voici le tableau : zéro, un, et plus l'infini. Question : entre zéro et un, quel est le signe de g prime de x ?
ÉCRAN : g(x) = 2x³ − 3x² + 2 sur ]0 ; +∞[. | g′(x) = 6x² − 6x = 6x(x − 1). | Sur ]0 ; +∞[, 6x > 0 : g′(x) a le signe de x − 1.
QUESTION : Sur ]0 ; 1[, quel est le signe de g′(x) = 6x(x − 1) ? OPTIONS : ['Négatif', 'Positif', 'Nul']

### Diapo 40 `df_va8_aux_b` — Exercice, partie I : le signe de g, lu dans son tableau
VOIX (fr) : x moins un est négatif avant un, positif après : la ligne de g prime : moins, zéro, plus. Donc g décroît, puis croît : les flèches. En un, g a un minimum. On calcule g de un : deux moins trois plus deux, égale un. Question : g de un égale un est le minimum de g. Quel est le signe de g de x, sur zéro, plus l'infini ?
ÉCRAN : g′ : −, 0, + : g décroît sur ]0 ; 1], croît sur [1 ; +∞[. | g(1) = 2 − 3 + 2 = 1 : le minimum de g. | Quel est le signe de g(x) ?
QUESTION : g(1) = 1 est le minimum de g sur ]0 ; +∞[ : quel est le signe de g(x) ? OPTIONS : ['g(x) > 0 pour tout x > 0', 'g(x) < 0 pour tout x > 0', 'g(x) change de signe en 1']

### Diapo 41 `df_va8_aux_c` — Exercice, partie II : montrer que f′(x) = g(x)/x²
VOIX (fr) : Partie deux : f de x égale x au carré, moins trois x, moins deux sur x, sur zéro, plus l'infini. On demande de montrer que f prime de x, égale g de x sur x au carré. La forme est donnée : il faut y arriver. Première ligne : f est dérivable sur zéro, plus l'infini, car x au carré moins trois x est un polynôme, et un sur x est dérivable sur zéro, plus l'infini. On dérive : deux x moins trois ; et la dérivée de moins deux sur x, c'est plus deux sur x au carré. Question : on met deux x moins trois plus deux sur x au carré, au même dénominateur, x au carré. Quel est le numérateur ?
ÉCRAN : f(x) = x² − 3x − 2/x sur ]0 ; +∞[. | f est dérivable sur ]0 ; +∞[ : f′(x) = 2x − 3 + 2/x². | Au même dénominateur x² : le numérateur ?
QUESTION : f′(x) = 2x − 3 + 2/x² : au même dénominateur x², quel est le numérateur ? OPTIONS : ['2x³ − 3x² + 2', '2x − 1', '2x³ − 3x + 2']

### Diapo 42 `df_va8_aux_d` — Exercice, partie II : le tableau de variations de f
VOIX (fr) : Le numérateur, c'est g de x : f prime de x, égale g de x sur x au carré. x au carré est positif : le signe de f prime est le signe de g, et g est positive, d'après la partie un. Donc, dans le tableau de f, la ligne de f prime : plus. Il reste les limites aux bornes. En plus l'infini, x au carré moins trois x tend vers plus l'infini. Question : et quand x tend vers zéro plus, quelle est la limite de f de x ?
ÉCRAN : f′(x) = g(x)/x² et x² > 0 : f′(x) a le signe de g(x). | g(x) > 0 (partie I) : la ligne f′(x) est +. | Aux bouts des flèches : lim f en 0⁺ et en +∞.
QUESTION : Quelle est la limite de f(x) = x² − 3x − 2/x quand x → 0⁺ ? OPTIONS : ['−∞', '+∞', '0']
## VI. Concavité et point d'inflexion

### Diapo 43 `df_co1_sous` — La courbe sous sa tangente
VOIX (fr) : Faisons rouler une tangente le long de la courbe de x au cube moins trois x. À gauche de O, regarde : la courbe reste sous sa tangente, comme une coupole. On dit qu'elle est concave, tournée vers le bas. À droite de O, c'est l'inverse : la courbe est au-dessus de sa tangente, comme un bol de harira. Elle est convexe, tournée vers le haut. Attention : ce n'est pas le sens de variation, c'est la forme.
ÉCRAN : Une tangente roule le long de la courbe de x³ − 3x. | À gauche de O, la courbe est sous ses tangentes : elle est concave, tournée vers le bas (∩). | À droite de O, la courbe est au-dessus de ses tangentes : elle est convexe, tournée vers le haut (∪). | Image : la coupole (∩) et le bol (∪).

### Diapo 44 `df_co2_traverse` — Le point où la tangente traverse
VOIX (fr) : Entre les deux, il y a un point spécial. Arrêtons la tangente en O. Regarde : la tangente y égale moins trois x traverse la courbe. À gauche, la courbe est en dessous ; à droite, au-dessus. Ce point, où la courbe change de côté et traverse sa tangente, s'appelle le point d'inflexion. Ici I, zéro, zéro. C'est comme le volant d'une voiture : entre un virage à gauche et un virage à droite, il y a un instant où il est droit.
ÉCRAN : En O, la tangente y = −3x traverse la courbe. | La courbe passe d'un côté de sa tangente à l'autre : concave puis convexe. | Ce point I(0 ; 0) est le point d'inflexion. | Image : le volant droit entre deux virages.

### Diapo 45 `df_co3_f_seconde` — Le signe de f''
VOIX (fr) : Le calcul qui donne la forme, c'est la dérivée seconde, la dérivée de la dérivée. Pour x au cube moins trois x : f prime de x، égale trois x au carré moins trois, et f seconde de x égale six x. Regarde la ligne sous la courbe. Pour x négatif, six x est négatif : la courbe est concave. Pour x positif, f seconde est positive : la courbe est convexe. En zéro, f seconde s'annule en changeant de signe : c'est le point d'inflexion. Je relis : f seconde positive, la courbe est tournée vers le haut ; f seconde s'annule en changeant de signe, point d'inflexion.
ÉCRAN : f″(x) = (f′(x))′ : la dérivée seconde. Pour x³ − 3x : f′(x) = 3x² − 3, f″(x) = 6x. | f deux fois dérivable sur I : (∀x ∈ I) f″(x) ≤ 0 : courbe concave (tournée vers le bas) ; (∀x ∈ I) f″(x) ≥ 0 : courbe convexe (tournée vers le haut). | f″ s'annule en x₀ en changeant de signe ⟹ I(x₀ ; f(x₀)) est un point d'inflexion. | Tableau de concavité : x : −∞ … 0 … +∞ ; f″(x) = 6x : − 0 + ; (Cf) : ∩ concave, I(0 ; 0), ∪ convexe.

### Diapo 46 `df_co4_changeant` — « En changeant de signe »
VOIX (fr) : Attention au piège. Prenons x puissance quatre. f seconde de x égale douze x au carré, et f seconde de zéro égale zéro. Est-ce un point d'inflexion ? Regarde la tangente en O : y égale zéro. La courbe reste au-dessus des deux côtés : elle ne traverse pas. La ligne de f seconde : plus, zéro, plus. Elle s'annule sans changer de signe : pas de point d'inflexion. Donc on écrit toujours : f seconde s'annule en x zéro en changeant de signe. Et on donne le point avec ses deux coordonnées. Pour f de x égale x puissance quatre, O est-il un point d'inflexion ?
ÉCRAN : Pour f(x) = x⁴ : f''(x) = 12x², f''(0) = 0 mais f'' ne change pas de signe : pas de point d'inflexion. | On écrit toujours : « f'' s'annule en x₀ en changeant de signe ». | On donne le point avec ses deux coordonnées : I(x₀ ; f(x₀)). | Exemple : f(x) = x³ − 3x² + 2x + 2 : f′(x) = 3x² − 6x + 2 ; f″(x) = 6x − 6 = 6(x − 1), s'annule en 1 en changeant de signe ; f(1) = 1 − 3 + 2 + 2 = 2 ; I(1 ; 2).
QUESTION : Pour f(x) = x⁴, O est-il un point d'inflexion ? OPTIONS : ['Oui : la tangente est horizontale', "Oui : f''(0) = 0", "Non : f'' s'annule sans changer de signe"]
EXERCICE : f(x) = x³ − 6x² : le point d'inflexion ? OPTIONS : ['I(2 ; −16)', 'I(2 ; 0)', 'I(0 ; 0)']
## VII. Branches infinies

### Diapo 47 `df_bi1_verticale` — La courbe longe une droite verticale
VOIX (fr) : Regarde la courbe de un sur x moins deux, plus un. Poussons M vers x égale deux, par la droite. Regarde les valeurs : f de x vaut un virgule six, puis trois, puis onze. M s'envole vers le haut, le long d'une droite verticale. Qui tend vers quoi ? x tend vers deux, un nombre ; f de x part à l'infini. La courbe longe la droite x égale deux. La phrase : la droite d'équation x égale deux est une asymptote verticale à la courbe.
ÉCRAN : f(x) = 1/(x − 2) + 1 : quand x → 2⁺, f(x) → +∞. | x tend vers un réel, f(x) part à l'infini : la courbe longe la droite x = 2. | Phrase : la droite d'équation x = 2 est une asymptote verticale à (Cf). | Ne pas confondre : x = a est verticale, y = b est horizontale.

### Diapo 48 `df_bi2_horizontale` — La courbe longe une droite horizontale
VOIX (fr) : Même courbe, autre direction. Poussons M très loin à droite. Regarde le petit segment entre M et la droite y égale un : l'écart vaut un, puis zéro virgule un, puis encore moins. Il fond. Cette fois, c'est x qui part à l'infini, et f de x tend vers un nombre, un. La courbe longe la droite horizontale y égale un. La phrase complète : la droite d'équation y égale un est une asymptote horizontale à la courbe, au voisinage de plus l'infini. N'oublie jamais le voisinage.
ÉCRAN : Quand x → +∞, f(x) = 1/(x − 2) + 1 → 1. | L'écart f(x) − 1 fond : 1 ; 0,1 ; … | Phrase : la droite d'équation y = 1 est une asymptote horizontale à (Cf) au voisinage de +∞.

### Diapo 49 `df_bi3_oblique` — La courbe longe une droite penchée
VOIX (fr) : Et si la droite est penchée ? Voici f de x égale deux x plus un, plus un sur x, et la droite y égale deux x plus un. M part à droite. Regarde le segment vertical entre la courbe et la droite : l'écart, c'est f de x moins deux x plus un, égale un sur x. Il vaut un, puis zéro virgule cinq, puis zéro virgule deux. Il tend vers zéro. Donc la courbe longe la droite penchée. La phrase : la droite d'équation y égale deux x plus un est une asymptote oblique à la courbe, au voisinage de plus l'infini.
ÉCRAN : f(x) = 2x + 1 + 1/x et la droite (Δ) : y = 2x + 1. | L'écart vertical f(x) − (2x + 1) = 1/x fond : 1 ; 0,5 ; 0,2… | lim [f(x) − (2x + 1)] = 0 quand x → +∞. | Phrase : la droite d'équation y = 2x + 1 est une asymptote oblique à (Cf) au voisinage de +∞.

### Diapo 50 `df_bi4_pente_om` — Aucune droite à longer : la pente de (OM)
VOIX (fr) : Parfois la courbe part à l'infini sans longer aucune droite. Comment décrire sa direction ? On regarde la droite qui relie O à M. Sa pente, c'est f de x sur x : voilà pourquoi on divise par x. Avec x au carré, M part à droite : regarde, la droite O M se redresse, sa pente vaut un, deux, quatre, elle explose. La limite de f de x sur x est plus l'infini : la courbe a une branche parabolique de direction l'axe des ordonnées, comme un avion qui décolle de plus en plus raide. Avec racine de x, c'est l'inverse : la pente fond vers zéro, la droite se couche. C'est une branche parabolique de direction l'axe des abscisses. Pour racine de x, la pente de O M tend vers zéro : direction de quel axe ?
ÉCRAN : x² et √x partent à l'infini sans longer de droite. | On regarde la pente de la droite (OM) : f(x)/x. | x² : f(x)/x = x → +∞ : branche parabolique de direction l'axe des ordonnées. | √x : f(x)/x = 1/√x → 0 : branche parabolique de direction l'axe des abscisses.
QUESTION : Pour √x, la pente de (OM) tend vers 0 : direction de quel axe ? OPTIONS : ["L'axe des abscisses (Ox)", "L'axe des ordonnées (Oy)", 'La droite y = x']

### Diapo 51 `df_bi5_direction` — Une direction sans asymptote
VOIX (fr) : Voici x plus racine de x, et la droite y égale x. M part à droite. La pente de O M, f de x sur x, égale un plus un sur racine de x : elle tend vers un. On pourrait croire que la courbe longe y égale x. Mais regarde le segment entre la courbe et la droite : f de x moins x égale racine de x, il vaut un, deux, presque quatre. Il grandit sans fin. La courbe prend la direction de la droite y égale x, sans la longer. On dit : branche parabolique de direction la droite d'équation y égale x, au voisinage de plus l'infini. Retiens : après la limite de f de x sur x, il reste une limite à calculer.
ÉCRAN : f(x) = x + √x : f(x)/x = 1 + 1/√x → 1. | Mais f(x) − x = √x → +∞ : l'écart avec y = x grandit. | Branche parabolique de direction la droite d'équation y = x au voisinage de +∞. | Si lim f(x)/x = a ≠ 0, il reste toujours à calculer lim [f(x) − ax].

### Diapo 52 `df_bi6_arbre` — L'arbre des branches infinies (1)
VOIX (fr) : Rassemblons les branches infinies dans un arbre, étage par étage. Premier cas : f tend vers l'infini quand x tend vers un réel a : asymptote verticale x = a. Deuxième cas : f tend vers un réel b quand x tend vers l'infini : asymptote horizontale y = b. Troisième cas : f(x) et x tendent vers l'infini : on calcule lim f(x)/x. Infini : direction l'axe des ordonnées ; zéro : direction l'axe des abscisses.
ÉCRAN : lim f(x) = ±∞ en a : asymptote verticale x = a. | lim f(x) = b en ±∞ : asymptote horizontale y = b. | lim f(x) = ±∞ en ±∞ : on calcule lim f(x)/x : ±∞ → direction (Oy) ; 0 → direction (Ox).

### Diapo 53 `df_bi6_arbre_b` — L'arbre des branches infinies (2) : la limite vaut a
VOIX (fr) : Il reste une feuille : lim f(x)/x vaut un réel a non nul. La courbe a la direction de y = ax, mais on ne sait pas encore si elle la longe. On calcule alors lim [f(x) − ax]. Un réel b : asymptote oblique y = ax + b. L'infini : branche parabolique de direction y = ax, comme pour x + √x. Chaque feuille a sa phrase : (Cf) admet … d'équation … au voisinage de …
ÉCRAN : lim f(x)/x = a ≠ 0 : on calcule lim [f(x) − ax]. | b → asymptote oblique y = ax + b. | ±∞ → branche parabolique de direction y = ax. | Phrase : (Cf) admet … d'équation … au voisinage de …

### Diapo 54 `df_bi7_droite_donnee` — Quand l'énoncé donne la droite
VOIX (fr) : Au national, la droite est toujours donnée : montrer que la droite y égale x moins un est asymptote à la courbe. Pas besoin de tout l'arbre : une seule limite suffit. On calcule f de x moins x moins un, avec l'écriture la plus commode, souvent celle que l'énoncé a fait vérifier avant. Ici, f de x، égale x moins un plus un sur x moins un, donc la différence égale un sur x moins un. Sa limite en plus l'infini égale zéro. On conclut : la droite y égale x moins un est une asymptote oblique à la courbe, au voisinage de plus l'infini. Quelle limite calcule-t-on, et que doit-on trouver ?
ÉCRAN : « Montrer que la droite (D) : y = ax + b est asymptote à (Cf) au voisinage de +∞ ». | On calcule f(x) − (ax + b), avec l'écriture commode de f. | On montre que sa limite est 0. | On conclut avec la phrase et le voisinage.
QUESTION : La droite y = ax + b est donnée : quelle limite calcule-t-on, et que doit-on trouver ? OPTIONS : ['lim [f(x) − (ax + b)], et trouver 0', 'lim f(x)/x, et trouver le coefficient a', 'lim f(x), et trouver une limite infinie']
## VIII. Position relative d'une courbe et d'une droite

### Diapo 55 `df_pr1_dessus` — Au-dessus ou en dessous
VOIX (fr) : Voici la courbe de deux x plus un plus un sur x, et la droite delta, y égale deux x plus un. Pour savoir qui est au-dessus, on se place à la même abscisse. En x égale un, on trace le segment vertical entre la droite et la courbe. On compare l'ordonnée sur la courbe, f de x, et l'ordonnée sur la droite, y. La différence, f de x moins y, égale un sur x, ici un. Elle est positive : le segment est vert, la courbe est au-dessus de la droite.
ÉCRAN : À une même abscisse x, on compare f(x) (sur la courbe) et y (sur la droite). | La différence : f(x) − y. | En x = 1 : f(1) − y = 1 > 0 : la courbe est au-dessus de (Δ).

### Diapo 56 `df_pr2_signe` — Le signe de la différence
VOIX (fr) : Passons à gauche de zéro, en x égale moins un. Le segment devient rouge : la courbe est sous la droite. La différence, un sur x, vaut moins un, elle est négative. Voilà la règle : différence positive, courbe au-dessus ; différence négative, courbe en dessous ; différence nulle, la courbe coupe la droite. Le signe de f de x moins y donne la position relative.
ÉCRAN : En x = −1 : f(−1) − y = −1 < 0 : la courbe est en dessous de (Δ). | f(x) − y > 0 : au-dessus ; f(x) − y < 0 : en dessous ; f(x) − y = 0 : la courbe coupe la droite. | Pour x < 0, 1/x < 0.

### Diapo 57 `df_pr3_tableau` — Le tableau de position relative
VOIX (fr) : Pour la position relative, on n'étudie pas une limite, on étudie un signe. On calcule f de x moins y, on factorise, et on fait un tableau. Une ligne pour le facteur, ici x : moins, double barre, plus. Une ligne pour f de x moins y, égale un sur x : le même signe. Et la dernière ligne, la position : la courbe en dessous de delta sur moins l'infini, zéro ; au-dessus sur zéro, plus l'infini. Retiens : pour l'asymptote, une limite ; pour la position, un signe. Pour la position relative, étudie-t-on une limite ou un signe ?
ÉCRAN : On calcule f(x) − y, on factorise, on étudie son SIGNE dans un tableau. | La ligne du facteur (ici x) évite l'erreur de part et d'autre de la double barre. | On conclut par intervalle : (Cf) en dessous de (Δ) sur ]−∞ ; 0[, au-dessus sur ]0 ; +∞[. | Asymptote : une limite ; position : un signe.
QUESTION : Pour la position relative, étudie-t-on une limite ou un signe ? OPTIONS : ['Le signe de f(x) − y', 'La limite de f(x) − y', 'La limite de f(x)/x']
EXERCICE : f(x) = x + 4/x et (Δ) : y = x. Sur ]0 ; +∞[, la courbe est… OPTIONS : ['confondue avec (Δ)', 'en dessous de (Δ)', 'au-dessus de (Δ)']
## IX. Axe et centre de symétrie

### Diapo 58 `df_sy1_symetrique` — Le point de l'autre côté
VOIX (fr) : Regarde la parabole x au carré moins quatre x plus cinq, et la droite verticale x égale deux, en violet. Plaçons x égale trois sur l'axe. De l'autre côté de deux, à la même distance, on trouve un. Un, c'est quatre moins trois. En général, le symétrique de x par rapport à a, c'est deux a moins x : le milieu de x et de deux a moins x, c'est a.
ÉCRAN : La parabole x² − 4x + 5 et la droite x = 2. | Le symétrique de 3 par rapport à 2 est 1 : même distance de 2. | Le symétrique de x par rapport à a est 2a − x : leur milieu est a.

### Diapo 59 `df_sy2_axe` — Un axe de symétrie
VOIX (fr) : Montons sur la courbe. Le point d'abscisse trois et le point d'abscisse un sont à la même hauteur : f de un égale f de trois égale deux. C'est vrai pour tout x : le point d'abscisse x et le point d'abscisse quatre moins x ont la même ordonnée. Donc f de deux a moins x égale f de x : ici, f de quatre moins x égale f de x. La droite x égale deux est un axe de symétrie de la courbe.
ÉCRAN : Les points d'abscisses 3 et 1 sont à la même hauteur : f(1) = f(3) = 2. | Axe x = a : f(2a − x) = f(x). | Ici : f(4 − x) = f(x), donc la droite x = 2 est un axe de symétrie.

### Diapo 60 `df_sy3_centre` — Un centre de symétrie
VOIX (fr) : Autre courbe : x plus un sur x moins deux, et le point oméga, deux, un. Prenons le point M d'abscisse trois, et le point M prime d'abscisse quatre moins trois, égale un. Relions-les : le milieu du segment tombe sur oméga. Déplace M : le milieu reste toujours sur oméga. Le milieu a pour ordonnée la moyenne : f de quatre moins x plus f de x, sur deux, égale un. Donc f de deux a moins x plus f de x, égale deux b : ici, la somme égale deux. Oméga est un centre de symétrie.
ÉCRAN : f(x) = (x + 1)/(x − 2) et Ω(2 ; 1). | Les points d'abscisses x et 4 − x : leur milieu est toujours Ω. | Centre Ω(a ; b) : f(2a − x) + f(x) = 2b ; ici f(4 − x) + f(x) = 2.

### Diapo 61 `df_sy4_rediger` — Rédiger : deux conditions
VOIX (fr) : Pour rédiger, une accolade à deux lignes, et le domaine d'abord. Exemple : f de x، égale x plus un sur x moins deux, définie sauf en deux. Première ligne : si x est différent de deux, alors quatre moins x est différent de deux, donc quatre moins x est dans le domaine. Deuxième ligne : on calcule f de quatre moins x plus f de x. f de quatre moins x égale cinq moins x sur deux moins x, qu'on écrit x moins cinq sur x moins deux. On ajoute : deux x moins quatre sur x moins deux, égale deux, égale deux fois un. Donc oméga deux, un, est un centre de symétrie. Et la parité, c'est le cas a égale zéro. Quelle est la première ligne de l'accolade ?
ÉCRAN : Première ligne de l'accolade : (2a − x) ∈ Df. | Deuxième ligne : f(2a − x) = f(x) (axe) ou f(2a − x) + f(x) = 2b (centre). | Exemple : f(x) = (x + 1)/(x − 2), Df = ℝ∖{2} ; x ≠ 2 ⟹ 4 − x ≠ 2 ; f(4 − x) = (5 − x)/(2 − x) = (x − 5)/(x − 2) ; f(4 − x) + f(x) = (x − 5 + x + 1)/(x − 2) = (2x − 4)/(x − 2) = 2 = 2 × 1. | Parité : a = 0 (paire : f(−x) = f(x), impaire : f(−x) = −f(x)).
QUESTION : Quelle est la première ligne de l'accolade ? OPTIONS : ['(2a − x) ∈ Df', 'f(2a − x) + f(x) = 2b', 'f(x) = f(−x)']
EXERCICE : f(x) = x² − 4x + 5 : que vaut f(4 − x) ? OPTIONS : ['x² − 4x + 5', 'x² + 4x + 5', '−x² + 4x − 5']
## X. Construire et lire la courbe

### Diapo 62 `df_tr1_tableau_lu` — Ce que le tableau annonce
VOIX (fr) : On arrive au tracé, qui vaut jusqu'à deux points au national. Avant de tracer, on lit. À gauche, le tableau de variations de x plus un sur x ; à droite, un repère vide. Chaque limite du tableau annonce quelque chose. Plus l'infini quand x tend vers zéro plus : la courbe monte le long de l'axe des ordonnées, asymptote verticale. Aux deux bouts, on sait déjà que la droite y égale x est une asymptote oblique. Et le tableau donne un minimum, deux en un, et un maximum, moins deux en moins un.
ÉCRAN : Le tableau de variations de x + 1/x à gauche, un repère vide à droite. | Chaque limite annonce une asymptote ou une branche. | lim f(x) = +∞ quand x → 0⁺ : asymptote verticale x = 0. | Avec l'étude : asymptote oblique y = x en ±∞, minimum 2 en 1, maximum −2 en −1.

### Diapo 63 `df_tr2_droites` — D'abord les droites
VOIX (fr) : Par quoi commence-t-on ? Comme le maçon qui tend ses cordeaux avant de monter le mur : par les droites. D'abord l'asymptote verticale, x égale zéro : c'est l'axe des ordonnées, on le repasse en pointillés. Puis l'asymptote oblique, y égale x. Une droite se trace avec deux points : zéro, zéro, et deux, deux. On la trace en pointillés. Retiens l'ordre : les droites, puis les points, et la courbe en dernier.
ÉCRAN : On trace (Cf) dans un repère orthonormé (O ; i⃗ ; j⃗). | On trace d'abord les asymptotes, en pointillés. | x = 0 : l'axe des ordonnées. | y = x : deux points, (0 ; 0) et (2 ; 2). | Ordre : droites, points, courbe.

### Diapo 64 `df_tr3_points` — Puis les points
VOIX (fr) : Après les droites, les points. En un extremum, f prime s'annule : la tangente est horizontale. On place le minimum, un, deux, avec un petit trait horizontal, et le maximum, moins un, moins deux, avec son petit trait. Puis quelques points calculés : f de deux égale deux virgule cinq, f de zéro virgule cinq égale deux virgule cinq. Au national, l'énoncé donne souvent des valeurs approchées entre parenthèses : on les place toutes. Où place-t-on le minimum ?
ÉCRAN : En un extremum, f' s'annule : la tangente est horizontale. | On place (1 ; 2) et (−1 ; −2) avec un petit trait horizontal. | On ajoute quelques points calculés : (2 ; 2,5), (0,5 ; 2,5).
QUESTION : Où place-t-on le minimum ? OPTIONS : ['Au point (1 ; 2), avec une tangente horizontale', 'Au point (2 ; 1), avec une tangente horizontale', 'Au point (0 ; 2), avec une tangente horizontale']

### Diapo 65 `df_tr4_branche` — La courbe, d'un seul trait
VOIX (fr) : Maintenant la courbe, d'un seul trait, pour x positif. Elle arrive d'en haut, le long de l'axe des ordonnées : c'est la limite plus l'infini en zéro plus. Elle descend jusqu'au minimum, un, deux, en touchant son petit trait horizontal. Puis elle remonte, et longe la droite y égale x. De quel côté ? f de x moins x égale un sur x, positif : la courbe est au-dessus de la droite.
ÉCRAN : La branche x > 0 se trace d'un trait : elle descend le long de x = 0, passe au minimum, remonte. | Elle longe y = x par-dessus : f(x) − x = 1/x > 0. | Elle suit les flèches du tableau, la position relative et la concavité.

### Diapo 66 `df_tr5_symetrie` — L'autre moitié par symétrie
VOIX (fr) : Faut-il tout recommencer pour x négatif ? Non. f de moins x égale moins f de x : la fonction est impaire, O est un centre de symétrie. La branche de gauche est la symétrique de celle de droite par rapport à O. Regarde : elle apparaît d'un coup. Le minimum, un, deux, devient le maximum, moins un, moins deux. La courbe est complète.
ÉCRAN : f(−x) = −f(x) : f est impaire, O est un centre de symétrie. | La branche x < 0 est la symétrique de la branche x > 0 par rapport à O. | Le minimum (1 ; 2) donne le maximum (−1 ; −2). | f paire ou impaire : on l'étudie sur D_E = Df ∩ [0 ; +∞[ (ici ]0 ; +∞[), puis on complète par symétrie.

### Diapo 67 `df_tr6_lire` — Lire une courbe déjà tracée
VOIX (fr) : Le chemin inverse : lire une courbe déjà tracée. Pour résoudre f de x égale trois, on trace la droite horizontale y égale trois. Elle coupe la courbe en deux points : l'équation a deux solutions, leurs abscisses. Fais glisser la droite : entre moins deux et deux, elle ne coupe rien, zéro solution. De même, f de x plus grand que zéro, c'est la courbe au-dessus de l'axe des abscisses. Combien de solutions a l'équation f de x égale trois ?
ÉCRAN : Résoudre graphiquement f(x) = m : compter les points d'intersection avec la droite y = m. | f(x) = 3 : deux solutions. | f(x) ≥ 0 : la courbe au-dessus de l'axe des abscisses. | f(x) = x : intersection avec y = x (ici aucune).
QUESTION : Combien de solutions a l'équation f(x) = 3 ? OPTIONS : ['Deux', 'Une', 'Aucune']
EXERCICE : Pour quelles valeurs de m l'équation f(x) = m n'a-t-elle aucune solution ? OPTIONS : ['m ∈ ]−∞ ; −2[', 'm ∈ ]2 ; +∞[', 'm ∈ ]−2 ; 2[']
## XI. Dérivée et courbe de la fonction réciproque

### Diapo 68 `df_rec1_miroir` — Le miroir y = x
VOIX (fr) : Rappel du chapitre d'avant : f de x égale x au carré plus un est continue et strictement croissante sur zéro, plus l'infini, donc elle admet une fonction réciproque, f moins un. Où est sa courbe ? Regarde la droite y égale x, en violet : c'est un miroir. Le point A, deux, cinq, est sur la courbe de f, car f de deux égale cinq. Son reflet, c'est A prime, cinq, deux : les coordonnées s'échangent. Et f moins un de cinq égale deux. Tous les points se reflètent : la courbe de f moins un est la symétrique de celle de f par rapport à y égale x.
ÉCRAN : f(x) = x² + 1 est continue et strictement croissante sur I = [0 ; +∞[ : elle admet une fonction réciproque f⁻¹ sur J = [1 ; +∞[. | f(2) = 5 ⟺ f⁻¹(5) = 2 : le point A(2 ; 5) a pour reflet A'(5 ; 2). | La courbe de f⁻¹ est la symétrique de celle de f par rapport à la droite y = x.

### Diapo 69 `df_rec2_pente` — La pente dans le miroir
VOIX (fr) : Regardons les tangentes. En A, deux, cinq, la tangente a pour pente f prime de deux, égale quatre. Regarde le petit triangle : un vers la droite, quatre vers le haut. Dans le miroir, l'horizontale devient verticale, et la verticale devient horizontale. Le triangle reflet en A prime : quatre vers la droite, un vers le haut. Sa pente est un quart. Ce qui était dressé se couche : la pente quatre devient un sur quatre.
ÉCRAN : En A(2 ; 5), la tangente a pour pente f'(2) = 4 : 1 à l'horizontale, 4 à la verticale. | Dans le miroir, l'horizontale et la verticale s'échangent : 4 à l'horizontale, 1 à la verticale. | La pente en A' est 1/4.
OBSERVATION : Quelle est la pente de la tangente en A′ ?

### Diapo 70 `df_rec3_formule` — La formule
VOIX (fr) : Écrivons la formule. La pente en A prime, c'est la dérivée de f moins un en cinq. La pente en A, c'est f prime de deux. Donc f moins un prime de cinq égale un sur f prime de deux, égale un quart. En général : f moins un prime de y zéro, égale un sur f prime de x zéro, où x zéro est l'antécédent de y zéro, et f prime de x zéro différent de zéro. Et si f′ ne s'annule pas sur tout I, f⁻¹ est dérivable sur J et (f⁻¹)′(x) = 1/f′(f⁻¹(x)). Attention : le nombre donné, cinq, est une image. On dérive f en son antécédent, deux. Et f moins un n'est pas un sur f. Pour f moins un prime de cinq, on calcule f prime en cinq ou en deux ?
ÉCRAN : f continue et strictement monotone sur I, dérivable en x₀, f′(x₀) ≠ 0 : (f⁻¹)′(y₀) = 1/f′(x₀), avec y₀ = f(x₀). | Ici : (f⁻¹)′(5) = 1/f′(2) = 1/4. | On dérive f en x₀ = 2 (l'antécédent), pas en 5. | Sur tout J = f(I) : si f′ ne s'annule pas sur I, (f⁻¹)′(x) = 1/f′(f⁻¹(x)). | f⁻¹ n'est pas 1/f.
QUESTION : Pour (f⁻¹)'(5), on calcule f' en 5 ou en 2 ? OPTIONS : ["En 1/5, l'inverse de 5", "En 5, le nombre de l'énoncé", "En 2, l'antécédent de 5"]

### Diapo 71 `df_rec4_condition` — Pourquoi f'(x₀) ≠ 0
VOIX (fr) : Pourquoi la condition f prime de x zéro différent de zéro ? Glissons A vers le point zéro, un. Là, f prime de zéro égale zéro : la tangente est horizontale. Dans le miroir, l'horizontale devient verticale : en un, zéro, la tangente à la courbe de f moins un est verticale. Une pente verticale, ce n'est pas un nombre : f moins un n'est pas dérivable en un. Voilà pourquoi il faut f prime de x zéro différent de zéro.
ÉCRAN : On glisse A vers (0 ; 1) : f'(0) = 0, tangente horizontale. | Son reflet en (1 ; 0) est vertical : f⁻¹ n'est pas dérivable en 1. | D'où la condition f'(x₀) ≠ 0.

### Diapo 72 `df_rec5_national` — Trois lignes, comme au national
VOIX (fr) : Au national, trois lignes. Exemple : f de x égale x au cube plus x, calculer f moins un prime de deux. Ligne un, l'antécédent : on cherche le x qui donne deux. f de un égale un plus un, égale deux, donc f moins un de deux égale un. Ligne deux, la condition : f est dérivable en un, f prime de x، égale trois x au carré plus un, f prime de un égale quatre, différent de zéro. Ligne trois, la formule : f moins un est dérivable en deux, et f moins un prime de deux égale un sur f prime de un, égale un quart.
ÉCRAN : ① L'antécédent : on cherche x₀ tel que f(x₀) = y₀. | ② f est continue et strictement monotone sur I, dérivable en x₀, et f′(x₀) ≠ 0. | ③ (f⁻¹)′(y₀) = 1/f′(x₀). | Exemple : f(x) = x³ + x, f′(x) = 3x² + 1 > 0 (f continue et strictement croissante sur ℝ) ; f(1) = 1 + 1 = 2, f′(1) = 3 + 1 = 4 ≠ 0 : (f⁻¹)′(2) = 1/f′(1) = 1/4.

### Diapo 73 `df_rec6_courbe` — Tracer la courbe de la réciproque
VOIX (fr) : Pour tracer la courbe de la réciproque, on ne symétrise pas toute la courbe. La parabole entière est là, mais f n'admet une réciproque que sur I, zéro, plus l'infini. On repasse cette partie seulement. Puis on la reflète dans le miroir y égale x. Point par point, les coordonnées s'échangent : zéro, un devient un, zéro ; deux, cinq devient cinq, deux. La tangente horizontale en zéro, un devient verticale en un, zéro. Et une asymptote se reflète aussi : on échange x et y dans son équation. Enfin J égale f de I, égale un, plus l'infini. Le point zéro, trois est sur la courbe de g : quel point est sur celle de g moins un ?
ÉCRAN : Seulement la partie de (Cf) sur I = [0 ; +∞[ (la restriction). | On échange les coordonnées des points : (0 ; 1) → (1 ; 0), (2 ; 5) → (5 ; 2). | La tangente horizontale devient verticale ; une asymptote se symétrise aussi (on échange x et y). | J = f(I) = [1 ; +∞[ : croissante, les bornes dans le même ordre.
QUESTION : Le point (0 ; 3) est sur la courbe de g : quel point est sur celle de g⁻¹ ? OPTIONS : ['(3 ; 0)', '(0 ; −3)', '(−3 ; 0)']
## XII. Le problème d'analyse, étape par étape

### Diapo 74 `df_ec1_ordre` — L'ordre d'un problème d'analyse
VOIX (fr) : Au national, le problème d'analyse suit presque toujours le même ordre. Un : le domaine et les limites aux bornes. Deux : les branches infinies. Trois : la dérivabilité en un point, puis montrer que f prime de x égale une expression. Quatre : le signe de f prime et le tableau de variations. Cinq : la concavité, et souvent la position relative. Six : le tracé. Sept : la fonction réciproque. Chaque question a son cas type et sa phrase : tu les as tous vus.
ÉCRAN : Domaine et limites ; branches infinies ; dérivée (« montrer que f'(x) = … ») ; variations. | Puis concavité ; position relative ; tracé ; réciproque. | Chaque question a son cas type et sa phrase.

### Diapo 75 `df_ec2_forme` — Lire la forme demandée
VOIX (fr) : L'énoncé donne souvent la réponse : montrer que, vérifier que. À quoi sert-elle ? Un : elle montre le chemin. Pour vérifier que f de x، égale x moins un plus un sur x moins un, on part d'un seul membre, le plus facile, et on arrive à l'autre : on réduit au même dénominateur, on retrouve f de x. Deux : cette écriture sert ensuite, par exemple pour l'asymptote oblique. Trois : si une question te bloque, le résultat est écrit dans l'énoncé : utilise-le et continue. Ne passe pas dix minutes sur un quart de point.
ÉCRAN : « Montrer que », « vérifier que » : partir d'un membre et arriver à l'autre. | Un résultat donné par l'énoncé peut être utilisé même sans l'avoir prouvé. | L'écriture vérifiée sert aux questions suivantes (limite, asymptote, signe).

### Diapo 76 `df_ec3_etude` — Une étude complète, pas à pas : l'ensemble de définition
VOIX (fr) : Une étude complète rassemble tout, mais pas à pas. f de x égale x racine de x plus un. Étape un, l'ensemble de définition : ce qui est sous la racine doit être positif ou nul. À toi : quel est l'ensemble de définition de f ?
ÉCRAN : f(x) = x√(x + 1). | Étape 1 : sous la racine, positif ou nul. Df = ?
QUESTION : Première question : quel est l'ensemble de définition de f(x) = x√(x + 1) ? OPTIONS : ['[−1 ; +∞[', ']−1 ; +∞[', 'ℝ']

### Diapo 77 `df_ec3_etude_a2` — Une étude complète, pas à pas : le bord −1
VOIX (fr) : Étape deux, en moins un, à droite. Le taux : f de x moins f de moins un, sur x plus un. f de moins un égale zéro : il reste x racine de x plus un, sur x plus un, c'est-à-dire x sur racine de x plus un. Le haut tend vers moins un, le bas vers zéro plus : le taux tend vers moins l'infini. Question : le taux tend vers moins l'infini. Que conclure en moins un ?
ÉCRAN : Taux en −1 à droite : (f(x) − f(−1))/(x + 1) = x√(x + 1)/(x + 1) = x/√(x + 1). | x → −1 et √(x + 1) → 0⁺, donc le taux → −∞. | Que conclure en −1 ?
QUESTION : Le taux en −1 à droite tend vers −∞ : que conclure ? OPTIONS : ['f est dérivable à droite en −1 et f_d′(−1) = −1 : demi-tangente oblique en A', "f n'est pas dérivable à droite en −1 : demi-tangente verticale en A(−1 ; 0)", "La droite d'équation x = −1 est une asymptote verticale à la courbe (C_f)"]

### Diapo 78 `df_ec3_etude_b` — Une étude complète, pas à pas : le signe de f′
VOIX (fr) : Étape 3, la dérivée : f′(x) = (3x + 2)/(2√(x + 1)). Le bas est toujours positif : le signe de f′(x) est celui de 3x + 2, nul en −2/3. Avant −2/3, par exemple en −1, 3x + 2 vaut −1 ; après, en 0, il vaut 2. À toi de conclure : qu'y a-t-il en −2/3 ?
ÉCRAN : f′(x) = (3x + 2)/(2√(x + 1)) sur ]−1 ; +∞[. | 2√(x + 1) > 0 : le signe de f′(x) est le signe de 3x + 2. | 3x + 2 = 0 pour x = −2/3.
QUESTION : Le signe de f′(x) est celui de 3x + 2 : que se passe-t-il en −2/3 ? OPTIONS : ['f a un maximum en −2/3', 'f a un minimum en −2/3', "f n'a pas d'extremum en −2/3"]

### Diapo 79 `df_ec3_etude_c` — Une étude complète, pas à pas : le minimum, O, la branche infinie
VOIX (fr) : On l'a vu : f prime est négative avant moins deux tiers, et positive après. Donc f de moins deux tiers est le minimum. Étape quatre : f de zéro égale zéro, la courbe passe par O. Étape cinq, en plus l'infini : f de x sur x égale racine de x plus un, qui tend vers plus l'infini. Question : que veut dire cette limite ?
ÉCRAN : f′ négative puis positive : minimum f(−2/3) = (−2/3)·√(1/3) = −2/(3√3) = −2√3/9. | f(0) = 0 : la courbe passe par O. | En +∞ : lim_{x→+∞} f(x)/x = lim_{x→+∞} √(x + 1) = +∞. Quelle branche ?
QUESTION : Interprète lim f(x)/x = +∞ quand x → +∞. OPTIONS : ["Branche parabolique de direction l'axe des abscisses au voisinage de +∞", 'Asymptote verticale, car la courbe part vers +∞ quand x tend vers +∞', "Branche parabolique de direction l'axe des ordonnées au voisinage de +∞"]

### Diapo 80 `df_ec3_etude_d` — Construire la courbe, pas à pas : les points
VOIX (fr) : L'étude est finie : on construit la courbe, dans l'ordre. D'abord le repère. Puis les points, un par un, et chaque point vient du tableau. A, moins un, zéro, avec sa demi-tangente verticale, vers le bas. Le minimum, en moins deux tiers : à peu près moins zéro virgule trente-huit. Puis O, car f de zéro égale zéro. Et un point de plus : f de un égale racine de deux, à peu près un virgule quarante et un. Avant de tracer, une question : au minimum, comment est la tangente ?
ÉCRAN : A(−1 ; 0) et sa demi-tangente verticale, vers le bas. | Le minimum (−2/3 ; −2√3/9), soit environ (−0,67 ; −0,38). | O, et B(1 ; √2), soit environ (1 ; 1,41).
QUESTION : Au minimum (−2/3 ; −2√3/9), comment trace-t-on la tangente ? OPTIONS : ['Verticale, comme au point A(−1 ; 0)', 'Horizontale, car f′(−2/3) = 0', 'Penchée, de pente égale à −2/3']

### Diapo 81 `df_ec3_etude_e` — Construire la courbe, pas à pas : d'un seul trait
VOIX (fr) : Au minimum, la tangente est horizontale : un petit trait. Maintenant la courbe, d'un seul trait, en suivant le tableau. Elle part de A vers le bas, collée à la demi-tangente. Elle descend jusqu'au minimum, où la tangente est horizontale. Puis elle monte, passe par O, puis par B. En plus l'infini, elle monte de plus en plus vite : c'est la branche parabolique de direction l'axe des ordonnées. Retiens l'ordre : d'abord le repère, puis les points et la tangente en chaque point, enfin la courbe.
ÉCRAN : Au minimum, un petit trait horizontal : la tangente. | De A vers le bas, puis le minimum, puis O et B. | En +∞ : de plus en plus raide (direction (Oy)).

### Diapo 82 `df_ec4_unique` — Rappel : une solution unique au milieu de l'étude
VOIX (fr) : Un rappel du chapitre d'avant, qui revient dans sept sujets sur vingt au milieu de l'étude. Montrer que f de x égale zéro admet une solution unique alpha. Trois conditions. f est continue sur l'intervalle. f est strictement monotone : ici, f prime de x، égale trois x au carré plus un, positive, donc f est strictement croissante. Et f de zéro fois f de un est négatif : moins un fois un. Donc l'équation admet une solution unique alpha entre zéro et un. Le tableau de variations donne tout cela d'un coup d'œil. Quelle condition oublie-t-on le plus souvent ?
ÉCRAN : f continue sur I ; f strictement monotone sur I ; 0 ∈ f(I) (ou f(a)·f(b) < 0). | Alors f(x) = 0 admet une solution unique α dans I. | Exemple : f(x) = x³ + x − 1 est continue sur [0 ; 1] car c'est un polynôme ; f′(x) = 3x² + 1 > 0 ; f(0) = −1, f(1) = 1, f(0)·f(1) = −1 < 0 : une solution unique α ∈ ]0 ; 1[. | Interprétation : (Cf) coupe l'axe des abscisses en un point unique d'abscisse α. | On le lit sur le tableau de variations ; la condition oubliée : « strictement ».
QUESTION : Quelle condition oublie-t-on le plus souvent ? OPTIONS : ['« strictement » monotone', '« f continue » sur [a ; b]', 'le signe : f(a)·f(b) < 0']
## XIII. Bilan du chapitre

### Diapo 83 `df_fin1_bilan` — Ce qu'il faut retenir
VOIX (fr) : Faisons le bilan sur une seule fiche, bloc par bloc, et écris avec moi. Un : la dérivabilité. La limite du taux est un réel l : f est dérivable, et l est le nombre dérivé. Si f prime à droite et f prime à gauche sont différents : point anguleux. Deux : la tangente. y égale f prime de x zéro, facteur de x moins x zéro, plus f de x zéro. Un taux infini donne une demi-tangente verticale. Trois : les dérivées. u prime v plus u v prime ; u prime v moins u v prime, sur v au carré ; et n'oublie jamais u prime. Quatre : les variations. Dérivée positive, fonction croissante ; f prime s'annule en changeant de signe : extremum. Cinq : la concavité. f seconde positive, la courbe est tournée vers le haut ; f seconde s'annule en changeant de signe : point d'inflexion. Six : les branches infinies, avec toujours le voisinage. Sept : la position relative, c'est un signe, pas une limite. Huit : la symétrie et le tracé : le domaine d'abord, et les droites avant la courbe. Neuf : la réciproque. f moins un prime de y zéro، égale un sur f prime de x zéro. La deuxième page est la tienne : ce qu'il te reste à retravailler.
ÉCRAN : 1. Dérivabilité : lim (f(x) − f(x₀))/(x − x₀) = l ∈ ℝ ⟹ f dérivable en x₀, f'(x₀) = l. ⚠ f_d' ≠ f_g' : point anguleux. | 2. Tangente : y = f'(x₀)(x − x₀) + f(x₀) ; taux infini : demi-tangente verticale. ⚠ Vérifier A sur (T). | 3. Dérivées : « f est dérivable sur I car … » ; (u·v)′ = u′v + uv′ ; (u/v)′ = (u′v − uv′)/v² (v ≠ 0 sur I) ; (uⁿ)′ = n·u′·uⁿ⁻¹ ; (√u)′ = u′/(2√u) (u > 0). ⚠ Ne pas oublier u′. | 4. Variations : f′ > 0 ⟹ f croissante ; f′ = 0 sur I ⟹ f constante ; f′ s'annule en changeant de signe ⟹ extremum. ⚠ Justifier le signe. | 5. Concavité : f'' ≥ 0 tournée vers le haut ; f'' s'annule en changeant de signe ⟹ point d'inflexion. ⚠ f''(x₀) = 0 ne suffit pas. | 6. Branches infinies : x = a ; y = b ; y = ax + b ; directions (Oy), (Ox), y = ax. ⚠ Le voisinage. | 7. Position relative : signe de f(x) − (ax + b). ⚠ Un signe, pas une limite. | 8. Symétrie et tracé : (2a − x) ∈ Df ; f(2a − x) = f(x) ou f(2a − x) + f(x) = 2b ; droites, points, courbe. | 9. Réciproque : f continue et strictement monotone sur I ; (f⁻¹)′(y₀) = 1/f′(x₀), y₀ = f(x₀), f′(x₀) ≠ 0 ; courbe symétrique par rapport à y = x. | Page 2, ta page : ce qu'il te reste à retravailler, d'après tes réponses du cours.

### Diapo 84 `df_fin2_carte` — La carte du chapitre
VOIX (fr) : Dessinons la carte de tout le chapitre, en une seule image. Au centre : l'étude de la fonction, qui finit dans le tracé de sa courbe. Première branche : la tangente et la dérivabilité, avec la limite du taux. Deuxième branche : les dérivées, produit, quotient, puissance, racine. Troisième branche : les variations, avec le signe de f prime. Quatrième branche : la concavité, avec le signe de f seconde. Cinquième branche : les branches infinies et la position relative. Sixième branche : la symétrie. Septième branche : le tracé, droites, points, courbe. Et la dernière branche : la fonction réciproque et sa dérivée. Les branches entourées en rouge, ce sont celles qu'on va reprendre ensemble.
ÉCRAN : Au centre : la courbe (Cf) et l'étude de f. | Tangente et dérivabilité ; dérivées. | Variations et extremums ; concavité. | Branches infinies et position relative ; symétrie. | Tracé ; fonction réciproque.

### Diapo 85 `df_fermeture_cours` — Ce qu'il faut retenir, et comment réviser
VOIX (fr) : Nous arrivons à la fin du cours : Dérivation et étude des fonctions. Que faut-il retenir ? Trois idées. Première : l'équation de la tangente : y égale f prime de a fois x moins a, plus f de a. Deuxième : le signe de f prime donne les variations de f. Troisième : les branches infinies, asymptotes et branches paraboliques, se trouvent par les limites. Maintenant quelques conseils pour réviser. Relis ton cahier, et refais seul les exercices du national. Quand tu réponds, écris chaque étape, et chaque résultat avec sa justification, car chaque étape a ses points. Le jour de l'examen, partage ton temps, et commence par la question qui te paraît facile. La veille, dors bien. Écris ces conseils dans ton cahier. Tu as bien travaillé, bon courage ! Le prochain cours : Suites numériques. On s'y retrouve !
ÉCRAN : Retenir : y = f′(a)(x − a) + f(a) · signe de f′ · branches infinies | Réviser : relire le cahier, refaire les exercices du national | Rédiger : chaque étape, et sa justification (car…) | Jour J : gérer son temps · bien dormir la veille

## Questions de bloc (posées après la dernière diapo du bloc)
- après diapo 4 `df_n1_b1` RETROUVER : Cahier fermé : écris la pente de la droite (AB).
- après diapo 4 `df_n1_b1` EXERCICE : Dans y = ax + b, que représente a ? OPTIONS : ["L'ordonnée à l'origine", 'La pente', "L'abscisse d'un point"]
- après diapo 8 `df_n1_b2` RETROUVER : Cahier fermé : écris la limite qui définit le nombre dérivé f'(x₀).
- après diapo 8 `df_n1_b2` EXERCICE : Le taux d'accroissement de f entre 1 et x, c'est… OPTIONS : ['La pente de la tangente en A', 'La pente de la sécante (AM)', "L'ordonnée du point M"]
- après diapo 11 `df_n1_b3` RETROUVER : Cahier fermé : écris l'équation de la tangente à (Cf) au point d'abscisse x₀.
- après diapo 11 `df_n1_b3` EXERCICE : Équation de la tangente en 1 à la courbe de f(x) = x² ? OPTIONS : ['y = x', 'y = 2x + 1', 'y = 2x − 1']
- après diapo 14 `df_n1_b4` RETROUVER : Cahier fermé : écris les limites qui définissent f_d'(x₀) et f_g'(x₀).
- après diapo 14 `df_n1_b4` EXERCICE : f(x) = x² + 1 si x ≥ 1 et f(x) = 4x − 2 si x < 1 (f(1) = 2). Calcule f_d'(1) et f_g'(1), puis conclus. OPTIONS : ["f est dérivable en 1 et f'(1) = 2, la dérivée de x² + 1 en 1", "f n'est pas dérivable en 1 : f_d'(1) = 2 et f_g'(1) = 4", "f n'est pas continue en 1 : on change d'expression en x = 1"]
- après diapo 17 `df_n2_b1` RETROUVER : Cahier fermé : dérive 3x² − 5x + 4.
- après diapo 17 `df_n2_b1` EXERCICE : Sur quel intervalle (x − 1)(x + 1) est-il négatif ? OPTIONS : [']1 ; +∞[', ']−∞ ; −1[', ']−1 ; 1[']
- après diapo 20 `df_n2_b2` RETROUVER : Cahier fermé : que conclut-on quand la limite du taux d'accroissement à droite en x₀ est ±∞ ?
- après diapo 20 `df_n2_b2` EXERCICE : Avec cette fonction, f_d'(0) = −2 et f_g'(0) = 3. Conclusion ? OPTIONS : ["f n'est pas continue en 0", "f est dérivable en 0 et f'(0) = 1", "f n'est pas dérivable en 0"]
- après diapo 24 `df_n2_b3` RETROUVER : Cahier fermé : écris la dérivée d'un quotient u/v.
- après diapo 24 `df_n2_b3` EXERCICE : Dérivée de f(x) = (x + 1)/(x − 2) ? OPTIONS : ['1', '3/(x − 2)²', '−3/(x − 2)²']
- après diapo 27 `df_n2_b4` RETROUVER : Cahier fermé : écris la dérivée de √u.
- après diapo 27 `df_n2_b4` EXERCICE : f(x) = x√(x + 1) : que vaut f'(0) ? OPTIONS : ['0', '2', '1']
- après diapo 30 `df_n3_b1` RETROUVER : Cahier fermé : écris la dérivée de √u.
- après diapo 30 `df_n3_b1` EXERCICE : f(x) = x√(x + 1) : que vaut f'(0) ? OPTIONS : ['0', '2', '1']
- après diapo 33 `df_n3_b2` RETROUVER : Cahier fermé : écris le lien entre le signe de f' sur un intervalle I et le sens de variation de f.
- après diapo 33 `df_n3_b2` EXERCICE : f′ s'annule en 2 et passe de − à + : f(2) est… OPTIONS : ['un maximum', 'un minimum', "ni l'un ni l'autre"]
- après diapo 36 `df_n3_b3` RETROUVER : Cahier fermé : quelles sont les trois lignes d'un tableau de variations ?
- après diapo 36 `df_n3_b3` EXERCICE : f(x) = x² − 6x + 1 : le signe de f'(x) ? OPTIONS : ['Celui de x − 3 : négatif avant 3, positif après', 'Toujours positif : f est croissante sur tout ℝ', 'Celui de x + 3 : négatif avant −3, positif après']
- après diapo 38 `df_n3_b4` RETROUVER : Cahier fermé : à quelle condition f(x₀) est-il un extremum de f ?
- après diapo 38 `df_n3_b4` EXERCICE : f(x) = x + 9/x sur ]0 ; +∞[. Calcule f'(x), étudie son signe, puis déduis que x + 9/x ≥ 6 pour tout x > 0. OPTIONS : None
- après diapo 42 `df_n3_b5` RETROUVER : Cahier fermé : si f′(x) = g(x)/x² sur ]0 ; +∞[, d'où vient le signe de f′(x), et pourquoi ?
- après diapo 42 `df_n3_b5` EXERCICE : g(x) = x² − 2x + 3. Avec le tableau de variations de g, montre que g(x) > 0 pour tout réel x. OPTIONS : None
- après diapo 46 `df_s4_b1` RETROUVER : Cahier fermé : écris ce que le signe de f'' dit de la courbe, et quand on a un point d'inflexion.
- après diapo 46 `df_s4_b1` EXERCICE : f(x) = x³ − 6x² : le point d'inflexion ? OPTIONS : ['I(2 ; −16)', 'I(2 ; 0)', 'I(0 ; 0)']
- après diapo 50 `df_s4_b2` RETROUVER : Cahier fermé : écris les trois limites qui donnent une asymptote verticale, horizontale, oblique.
- après diapo 50 `df_s4_b2` EXERCICE : f(x) = (2x + 1)/(x − 1). Calcule lim f(x) quand x → 1⁺ et quand x → +∞, puis interprète chaque résultat. OPTIONS : None
- après diapo 54 `df_s4_b3` RETROUVER : Cahier fermé : quand lim f(x) = ±∞, écris l'arbre des branches infinies (limite de f(x)/x, puis de f(x) − ax).
- après diapo 54 `df_s4_b3` EXERCICE : f(x) = x − 3 + 2/x. Montre que la droite (Δ) : y = x − 3 est une asymptote oblique à (Cf) au voisinage de +∞. OPTIONS : None
- après diapo 57 `df_s5_b1` RETROUVER : Cahier fermé : comment trouve-t-on la position relative de (Cf) et de la droite (Δ) : y = ax + b ?
- après diapo 57 `df_s5_b1` EXERCICE : f(x) = x + 4/x et (Δ) : y = x. Sur ]0 ; +∞[, la courbe est… OPTIONS : ['confondue avec (Δ)', 'en dessous de (Δ)', 'au-dessus de (Δ)']
- après diapo 61 `df_s5_b2` RETROUVER : Cahier fermé : écris les conditions d'un axe de symétrie x = a, puis d'un centre de symétrie Ω(a ; b).
- après diapo 61 `df_s5_b2` EXERCICE : f(x) = x² − 4x + 5 : que vaut f(4 − x) ? OPTIONS : ['x² − 4x + 5', 'x² + 4x + 5', '−x² + 4x − 5']
- après diapo 64 `df_s5_b3` RETROUVER : Cahier fermé : dans quel ordre trace-t-on la courbe d'une fonction étudiée ?
- après diapo 64 `df_s5_b3` EXERCICE : Pour tracer la tangente (T) : y = 2x − 1, quels deux points places-tu ? OPTIONS : ['(0 ; 1) et (1 ; 3)', '(0 ; −1) et (1 ; 1)', '(0 ; −1) et (1 ; 2)']
- après diapo 67 `df_s6_b1` RETROUVER : Cahier fermé : comment lit-on sur la courbe le nombre de solutions de l'équation f(x) = m ?
- après diapo 67 `df_s6_b1` EXERCICE : Pour quelles valeurs de m l'équation f(x) = m n'a-t-elle aucune solution ? OPTIONS : ['m ∈ ]−∞ ; −2[', 'm ∈ ]2 ; +∞[', 'm ∈ ]−2 ; 2[']
- après diapo 70 `df_s6_b2` RETROUVER : Cahier fermé : par quelle symétrie obtient-on la courbe de f⁻¹, et quel lien y a-t-il entre f(x₀) = y₀ et f⁻¹ ?
- après diapo 70 `df_s6_b2` EXERCICE : f(x) = x³ + 2x est continue et strictement croissante sur ℝ. Calcule f(1), puis (f⁻¹)'(3). OPTIONS : None
- après diapo 73 `df_s6_b3` RETROUVER : Cahier fermé : écris la formule de la dérivée de f⁻¹ en y₀, avec ses conditions.
- après diapo 73 `df_s6_b3` EXERCICE : g(x) = x³ + x, g(1) = 2 : que vaut (g⁻¹)'(2) ? OPTIONS : ['1/2', '4', '1/4']
- après diapo 76 `df_n7_b1` RETROUVER : Cahier fermé : écris l'ordre des questions d'un problème d'analyse.
- après diapo 76 `df_n7_b1` EXERCICE : Pourquoi f admet-elle un minimum en −2/3 ? OPTIONS : ["f' s'annule en −2/3 en changeant de signe (− puis +)", "f s'annule en −2/3 : la courbe y touche l'axe des abscisses", "f est continue en −2/3 et définie de part et d'autre de −2/3"]
- après diapo 79 `df_n7_b2` RETROUVER : Cahier fermé : le taux en a à droite tend vers −∞. Que conclure, et quelle phrase d'interprétation écrit-on ?
- après diapo 79 `df_n7_b2` EXERCICE : f(x) = x√(x + 2) sur [−2 ; +∞[. Étudie la dérivabilité de f à droite en −2 et interprète le résultat. OPTIONS : None
- après diapo 82 `df_n7_b2c` RETROUVER : Cahier fermé : énonce les conditions pour que l'équation f(x) = 0 ait une solution unique dans ]a ; b[.
- après diapo 82 `df_n7_b2c` EXERCICE : f(x) = x³ + x − 1. Montre que l'équation f(x) = 0 admet une solution unique α dans ]0 ; 1[. OPTIONS : None
- après diapo 84 `df_s7_b3` RETROUVER : Cahier fermé : écris l'équation de la tangente à (Cf) au point d'abscisse x₀.
- après diapo 84 `df_s7_b3` EXERCICE : f′ > 0 sur un intervalle I : f est… OPTIONS : ['constante sur I', 'strictement décroissante sur I', 'strictement croissante sur I']
