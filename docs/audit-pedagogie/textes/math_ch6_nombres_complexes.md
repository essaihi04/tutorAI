# math_ch6_nombres_complexes — Nombres complexes (première partie)

## Ouverture — le nombre qui fait tourner

### Diapo 1 `nc_ouverture_cours` — Nombres complexes (première partie)
VOIX (fr) : Bienvenue dans un nouveau cours : Nombres complexes, la première partie. Dans ce cours, nous allons apprendre le nombre i, la forme algébrique, le module, l'argument, la forme trigonométrique, et leur usage en géométrie. Au national, les nombres complexes avec les probabilités comptent pour trente pour cent de la note. Comment allons-nous travailler ? Tu écoutes bien, tu réponds aux questions au tableau, et quand le cours s'arrête, tu écris dans ton cahier. Allons-y !
ÉCRAN : On apprend : i, forme algébrique, module, argument, géométrie | Au bac : complexes et probabilités = 30 % de la note | Écouter · répondre au tableau · écrire dans le cahier

### Diapo 2 `nc_o1` — La carte du chapitre : le nombre qui fait tourner
VOIX (fr) : Regarde le centre : un petit plan complexe, avec un point M. À côté, son écriture : z égale a plus i b. Chaque nombre complexe est un point du plan. Autour, les questions du chapitre, dans l'ordre du national. D'abord la forme algébrique, puis le quotient. Ensuite le conjugué, et le module. Puis la forme trigonométrique, le produit et la puissance. Enfin la géométrie : le milieu, la distance, l'alignement. En bas, en jaune : un exercice de complexes, dans vingt sujets sur vingt. La forme trigonométrique, dans dix-sept sujets. À droite, en pointillé, la partie deux : on la verra plus tard.
ÉCRAN : Au centre : le plan complexe, un point M et son écriture z = a + ib. | Autour, les questions du national : forme algébrique, quotient, conjugué, module, forme trigonométrique, produit et puissance, milieu, distance, alignement. | Un exercice de complexes dans les 20 sujets nationaux (2016-2025) ; la forme trigonométrique dans 17. | Partie 2 (plus tard) : équation, écriture exponentielle, rotation.
## I. Le nombre i et la forme algébrique

### Diapo 3 `nc_a1` — Une équation sans solution réelle
VOIX (fr) : Regarde la droite graduée, de moins trois à trois. Au-dessus de moins trois, de moins un, de zéro et de deux, on écrit leurs carrés. Neuf, un, zéro, quatre. Tous sont en vert : positifs ou nuls. Le carré d'un réel n'est jamais négatif. Maintenant, en bas : x carré égale moins un. Aucun réel ne marche, la ligne est barrée en rouge. Pour la résoudre, il faudra sortir de cette droite.
ÉCRAN : Sur la droite des réels : (−3)² = 9, (−1)² = 1, 0² = 0, 2² = 4. | Un carré de réel est toujours positif ou nul : x² ≥ 0. | Donc x² = −1 n'a aucune solution réelle. | Pour la résoudre, il faudra sortir de la droite.

### Diapo 4 `nc_a2` — Le nombre i : un quart de tour
VOIX (fr) : Regarde le point deux, sur la droite. On le multiplie par moins un : il fait un demi-tour autour de O, et arrive en moins deux. Multiplier par moins un, c'est un demi-tour. Maintenant le point un fait seulement un quart de tour. Il sort de la droite, et monte sur un axe vertical. Ce quart de tour, on l'appelle i. Un deuxième quart de tour : le point arrive sur moins un. Deux quarts de tour, c'est un demi-tour. Donc i fois i égale moins un : i au carré égale moins un. Retiens : i est un nombre complexe non réel, dont le carré vaut moins un. En bas, les deux solutions : x égale i, ou x égale moins i. Question : vérifie que, racine de deux fois i, au carré, égale moins deux.
ÉCRAN : Multiplier par −1, c'est faire un demi-tour autour de O : 2 devient −2. | Un quart de tour, fait deux fois, donne un demi-tour : ce quart de tour s'appelle i. | i × i = −1 : i² = −1 (i n'est pas un réel). | x² = −1 a deux solutions : i et −i.
QUESTION : (√2 i)² = ? OPTIONS : ['2', '−√2', '−2']
EXERCICE : (3i)² = ? OPTIONS : ['9', '−9', '6i']

### Diapo 5 `nc_z1_repere` — Rappel : un point, deux coordonnées
VOIX (fr) : Pour placer un nombre complexe dans un plan, revoyons le repère. Deux axes : l'axe des abscisses, horizontal, et l'axe des ordonnées, vertical. Ils se croisent en l'origine O. Plaçons un point : on avance de trois sur l'axe des abscisses, puis on monte de deux. C'est le point M de coordonnées trois, deux : trois est l'abscisse, deux l'ordonnée. Autrement dit : comme en classe, le numéro de la rangée et le numéro de la table. Deux nombres, et l'ordre compte : le point P de coordonnées deux, trois n'est pas M. Je relis : un point du plan a deux coordonnées, l'abscisse puis l'ordonnée.
ÉCRAN : Un repère : l'axe des abscisses (horizontal), l'axe des ordonnées (vertical), l'origine O. | M(3 ; 2) : on avance de 3, puis on monte de 2. | L'ordre compte : (3 ; 2) n'est pas (2 ; 3).

### Diapo 6 `nc_a3` — La forme algébrique z = a + ib
VOIX (fr) : Voici le plan : l'axe réel horizontal, l'axe imaginaire vertical, et l'origine O. On place trois plus deux i. On avance de trois sur l'axe réel, puis on monte de deux. Le point M se pose : M trois, deux. À côté, z égale trois plus deux i. Trois est en vert : c'est la partie réelle. Deux est en orange : c'est la partie imaginaire. Attention : la partie imaginaire, c'est deux, sans le i. Tout complexe s'écrit d'une seule façon : z égale a plus i b, avec a et b réels. C'est la forme algébrique. Quand on change a et b, le point M bouge, et l'écriture suit.
ÉCRAN : Tout complexe s'écrit de façon unique z = a + ib, avec a et b réels. | a = Re(z) : la partie réelle ; b = Im(z) : la partie imaginaire. | Im(z) est un réel, sans i : Im(3 − 5i) = −5. | 3 = 3 + 0i et 4i = 0 + 4i sont aussi des complexes : ℝ ⊂ ℂ.

### Diapo 7 `nc_a4` — Réels et imaginaires purs
VOIX (fr) : Toujours le plan, avec ses deux axes. Un point descend sur l'axe réel : là, b égale zéro. Le complexe est un réel, écrit en vert le long de l'axe réel. Un autre point glisse sur l'axe imaginaire : là, a égale zéro. Ce complexe s'appelle un imaginaire pur, en orange. Et O est entouré : zéro est sur les deux axes. Zéro est à la fois réel et imaginaire pur.
ÉCRAN : b = 0 : z = a est un réel ; son point est sur l'axe réel. | a = 0 : z = ib est un imaginaire pur (z ∈ iℝ) ; son point est sur l'axe imaginaire. | 0 = 0 + 0i est les deux à la fois. | −3 est réel ; 4i est imaginaire pur ; 2 + i n'est ni l'un ni l'autre.

### Diapo 8 `nc_a5` — Égalité de deux complexes : deux équations
VOIX (fr) : En haut, encadrée, la règle. Deux complexes sont égaux, si et seulement si, leurs parties réelles sont égales, et leurs parties imaginaires sont égales. Voici l'exemple : x moins deux, plus y plus un fois i, égale cinq moins trois i. En vert, les parties réelles : x moins deux égale cinq. En orange, les parties imaginaires : y plus un égale moins trois. Donc x égale sept, et y égale moins quatre. Dernière ligne : on vérifie dans les deux équations. Sept moins deux, ça fait cinq. Moins quatre plus un, ça fait moins trois. On retrouve cinq moins trois i : c'est juste.
ÉCRAN : z = z′ ⇔ Re(z) = Re(z′) et Im(z) = Im(z′). | Une égalité de complexes donne deux équations réelles. | (x − 2) + (y + 1)i = 5 − 3i ⇔ x − 2 = 5 et y + 1 = −3 ⇔ x = 7 et y = −4. | On vérifie la solution dans les deux équations.

### Diapo 9 `nc_a6` — Les puissances de i reviennent tous les quatre
VOIX (fr) : Sur l'axe réel, le point un : i puissance zéro égale un. On multiplie par i : un quart de tour, le point monte sur i. Encore un quart de tour : i au carré égale moins un. Encore un : i cube égale moins i. Encore un : i puissance quatre égale un. On est revenu au départ. Tous les quatre, on revient : i puissance quatre égale un. Pour une grande puissance, on regroupe par i au carré. Par exemple, i puissance six, égale i au carré, puissance trois. C'est moins un puissance trois, donc moins un. Le compteur pose le point sur i puissance n. Question : calcule i puissance deux mille vingt-six.
ÉCRAN : i⁰ = 1, i¹ = i, i² = −1, i³ = −i, i⁴ = 1. | Chaque multiplication par i : un quart de tour de plus. | Tous les quatre, on revient : i⁴ = 1. | Grande puissance : on regroupe par i², i²ᵏ = (−1)ᵏ.
QUESTION : i²⁰²⁶ = ? OPTIONS : ['−1', '1', '−i']
EXERCICE : i¹⁵ = ? OPTIONS : ['i', '−i', '−1']
OBSERVATION : Après le quatrième quart de tour, sur quel nombre le point se pose-t-il ?
## II. Calculer sous forme algébrique

### Diapo 10 `nc_z5_identites` — Rappel : développer, les identités remarquables
VOIX (fr) : Avant de calculer avec i, revoyons comment développer. Pour développer deux parenthèses, chaque terme de la première multiplie chaque terme de la seconde : a plus b fois c plus d égale ac plus ad plus bc plus bd. D'où l'identité remarquable : a plus b au carré égale a carré plus deux ab plus b carré. Et a moins b fois a plus b : ab et moins ab s'annulent, il reste a carré moins b carré. Par exemple x moins trois fois x plus trois égale x carré moins neuf. Autrement dit : un carré de côté a plus b, coupé en quatre morceaux : un carré a carré, deux rectangles ab, un petit carré b carré. Je relis : a plus b au carré égale a carré plus deux ab plus b carré.
ÉCRAN : (a + b)(c + d) = ac + ad + bc + bd : chaque terme fois chaque terme. | (a + b)² = a² + 2ab + b². | (a − b)(a + b) = a² − b² : par exemple (x − 3)(x + 3) = x² − 9.

### Diapo 11 `nc_c1` — Somme et produit : on développe, i² = −1
VOIX (fr) : Première ligne, la somme : trois plus i, plus deux moins i. On ajoute les parties réelles : trois plus deux, cinq. Puis les parties imaginaires : un moins un, zéro. La somme vaut cinq. Deuxième ligne, le produit : trois plus i, fois deux moins i. On développe comme d'habitude. Six, moins trois i, plus deux i, moins i au carré. En orange : i au carré, on le remplace par moins un. Six moins i, plus un. Le résultat, encadré : sept moins i. La partie réelle est sept, la partie imaginaire moins un.
ÉCRAN : Somme : on ajoute les parties réelles, puis les parties imaginaires. | Produit : on développe (distributivité), comme avec des réels. | Chaque i² est remplacé par −1. | On regroupe : partie réelle, puis partie imaginaire.

### Diapo 12 `nc_c2` — Carré et puissance : (1 + i)² = 2i
VOIX (fr) : Première ligne : un plus i, au carré. C'est une identité remarquable. Un au carré, plus deux fois un fois i, plus i au carré. On remplace i au carré par moins un : un plus deux i, moins un. Le un et le moins un s'annulent. Encadré en jaune : un plus i, au carré, égale deux i. Même geste avec un moins i : on trouve moins deux i. Pour une grande puissance, on passe par le carré. Un plus i, puissance quatre, c'est deux i au carré. Ça fait quatre i au carré, donc moins quatre.
ÉCRAN : Identité remarquable (a + b)² = a² + 2ab + b², avec i² = −1. | (1 + i)² = 1 + 2i + i² = 1 + 2i − 1 = 2i. | (1 − i)² = 1 − 2i + i² = −2i. | Grande puissance : on passe par le carré, (1 + i)⁴ = (2i)² = −4.

### Diapo 13 `nc_c3` — Un complexe fois son conjugué : un réel
VOIX (fr) : Première ligne : deux plus i, fois deux moins i. On développe : quatre, moins deux i, plus deux i, moins i au carré. En orange : les termes en i s'annulent. Moins deux i plus deux i, ça fait zéro. Reste quatre moins i au carré, donc quatre plus un, cinq. C'est un réel ! La formule, encadrée : a plus i b, fois a moins i b, égale a carré plus b carré. a moins i b, c'est le conjugué de a plus i b. Un complexe fois son conjugué donne un réel positif. Et en rouge, barré : a carré moins b carré, c'est faux.
ÉCRAN : a − ib est le conjugué de z = a + ib ; on le note z̄. | En développant, les termes en i s'annulent. | (a + ib)(a − ib) = a² + b² : un réel positif. | Piège : ce n'est pas a² − b².

### Diapo 14 `nc_c4` — Le quotient : multiplier par le conjugué du dénominateur
VOIX (fr) : Voici le quotient : trois plus i, sur un plus deux i. Le i en bas nous gêne. On multiplie le haut et le bas, par un moins deux i : c'est le conjugué du bas. En haut et en bas, le même facteur : la fraction ne change pas. On développe. En haut : trois, moins six i, plus i, moins deux i au carré. En bas : un plus quatre, cinq. Le bas est devenu réel. En haut, i au carré égale moins un : cinq moins cinq i. On sépare : cinq sur cinq, moins cinq sur cinq fois i. Le résultat, encadré : un moins i. Dernière ligne, en vert : on vérifie. Un moins i, fois un plus deux i, redonne trois plus i. Au national, ce calcul tombe dans dix sujets sur vingt. Question : écris un plus trois i, sur un moins i, sous forme algébrique.
ÉCRAN : On multiplie le haut ET le bas par le conjugué du dénominateur (c + id ≠ 0). | En bas : (c + id)(c − id) = c² + d², un réel. | On développe le haut, puis on sépare partie réelle et partie imaginaire. | On vérifie en remultipliant. Au national : 10 sujets sur 20.
QUESTION : (1 + 3i)/(1 − i) = ? OPTIONS : ['−2 + 4i', '−1 + 2i', '1 + 2i']
EXERCICE : 1/(1 + i) = ? OPTIONS : ['1/2 − (1/2)i', '1 − i', '1/2 + (1/2)i']
## III. Le plan complexe : affixes, parallélogramme

### Diapo 15 `nc_p1` — Le plan complexe : un complexe, un point
VOIX (fr) : Regarde le tableau. On trace deux axes. L'axe horizontal, c'est l'axe réel. L'axe vertical, c'est l'axe imaginaire. Au croisement, le point O, avec les vecteurs u et v. C'est le plan complexe, dans un repère orthonormé direct. Maintenant, on place trois plus deux i. On avance de trois sur l'axe réel, en vert. Puis on monte de deux, en orange. Le point M se pose : M de coordonnées trois, deux. Attention : les coordonnées sont des réels. On écrit deux, pas deux i. Tu peux glisser le point M : son écriture a plus i b change avec lui.
ÉCRAN : Le plan muni d'un repère orthonormé direct (O, u⃗, v⃗) s'appelle le plan complexe. | L'axe horizontal est l'axe réel ; l'axe vertical est l'axe imaginaire (ou axe des imaginaires purs). | 3 + 2i : on avance de 3, puis on monte de 2 : le point M(3 ; 2). | Les coordonnées de M sont réelles : M(3 ; 2), jamais (3 ; 2i).

### Diapo 16 `nc_p2` — L'affixe d'un point
VOIX (fr) : Sur le tableau, le même plan, avec ses axes. On place le point A, de coordonnées moins deux, un. En jaune, on écrit son complexe : z A égale moins deux plus i. Ce complexe s'appelle l'affixe du point A. Puis le point O : z O égale zéro. Dans le cadre : l'affixe, c'est le numéro du point. Le point a des coordonnées, et le complexe est son affixe. On écrit M de z, ou A de a.
ÉCRAN : Au point M(a ; b) correspond le complexe z_M = a + ib : c'est l'affixe de M. | On note M(z_M), ou A(a) : le point et son affixe. | A(−2 ; 1) a pour affixe z_A = −2 + i. | O a pour affixe z_O = 0 : l'affixe est le « numéro » du point.

### Diapo 17 `nc_z2_vecteur` — Rappel : un vecteur, un déplacement
VOIX (fr) : Avant l'affixe d'un vecteur, revoyons le vecteur. Deux points, A de coordonnées un, deux, et B de coordonnées quatre, moins un. La flèche de A vers B, c'est le vecteur AB. De combien a-t-on bougé ? Trois vers la droite, trois vers le bas. Les coordonnées du vecteur AB : x de B moins x de A, y de B moins y de A : trois et moins trois. Arrivée moins départ. Autrement dit : un vecteur est un déplacement, un chemin : trois pas à droite, trois en bas. Parti de O, le même déplacement mène au point trois, moins trois. Je relis : les coordonnées du vecteur AB, c'est arrivée moins départ.
ÉCRAN : Le vecteur AB⃗ : la flèche qui va de A vers B. | AB⃗(x_B − x_A ; y_B − y_A) : arrivée moins départ. | A(1 ; 2), B(4 ; −1) : AB⃗(3 ; −3).

### Diapo 18 `nc_p3` — L'affixe d'un vecteur : arrivée moins départ
VOIX (fr) : Regarde les deux points : A, d'affixe un plus deux i, et B, d'affixe quatre moins i. On trace la flèche de A vers B. Son affixe s'écrit : z A B égale z B moins z A. L'arrivée moins le départ. Maintenant, la flèche glisse jusqu'à O, sans tourner. Son extrémité tombe sur le point trois moins trois i. C'est l'affixe du vecteur A B. Enfin, la somme : deux vecteurs O M et O M prime. Leur somme est la diagonale du parallélogramme : son affixe est z plus z prime.
ÉCRAN : L'affixe du vecteur AB⃗ : z_{AB⃗} = z_B − z_A (arrivée moins départ). | La flèche AB⃗ glisse jusqu'à O : son extrémité est le point d'affixe z_B − z_A. | A(1 + 2i), B(4 − i) : z_{AB⃗} = (4 − i) − (1 + 2i) = 3 − 3i. | La somme z + z′ : la diagonale du parallélogramme construit sur OM⃗ et OM′⃗.

### Diapo 19 `nc_p4` — L'affixe du milieu
VOIX (fr) : Sur le tableau, deux points : A d'affixe un plus deux i, et B d'affixe un moins deux i. On trace le segment A B. Le milieu P est au centre du segment. Son affixe, c'est la moyenne des deux affixes : z I égale z A plus z B, sur deux. On calcule : a plus b égale deux. Les termes en i s'en vont. Donc p égale deux sur deux, égale un. En jaune : p égale un. Le point P est sur l'axe réel. C'est le sujet national de deux mille vingt-cinq. Question : quelle est l'affixe p du milieu P de A B ?
ÉCRAN : Le milieu I de [AB] a pour affixe z_I = (z_A + z_B)/2. | C'est la moyenne des deux affixes, comme pour les coordonnées du milieu. | 2025 N : a = 1 + 2i, b = 1 − 2i : à toi de calculer p.
QUESTION : a = 1 + 2i et b = 1 − 2i : quelle est l'affixe p du milieu P de [AB] ? (2025 N) OPTIONS : ['p = 1', 'p = 2', 'p = 2i']
EXERCICE : A(2 + 3i), B(4 − i) : l'affixe du milieu I de [AB] est : OPTIONS : ['6 + 2i', '1 − 2i', '3 + i']

### Diapo 20 `nc_p5` — Le parallélogramme : deux vecteurs égaux
VOIX (fr) : Regarde le tableau : M d'affixe un plus deux i, M prime d'affixe trois moins trois i, et B, quatre moins i, qui vaut z plus z prime. C'est la diagonale du parallélogramme O M B M prime. Pourquoi est-ce un parallélogramme ? Parce que le vecteur O M est égal au vecteur M prime B. Deux vecteurs égaux ont la même affixe : un plus deux i des deux côtés. La règle : A B C D est un parallélogramme si et seulement si b moins a égale c moins d. Autre façon de le voir : les diagonales ont le même milieu, a plus c égale b plus d.
ÉCRAN : Deux vecteurs égaux ont la même affixe : AB⃗ = DC⃗ ⇔ z_B − z_A = z_C − z_D. | ABCD est un parallélogramme ⇔ AB⃗ = DC⃗ ⇔ b − a = c − d. | Au tableau : z_M − z_O = 1 + 2i et z_B − z_{M′} = (4 − i) − (3 − 3i) = 1 + 2i : OMBM′ est un parallélogramme. | Autre façon : les diagonales [AC] et [BD] ont le même milieu ⇔ a + c = b + d.
## IV. Le conjugué

### Diapo 21 `nc_j1` — Le conjugué : le reflet dans l'axe réel
VOIX (fr) : Regarde le point M, d'affixe trois plus deux i. L'axe réel devient épais : c'est un miroir. Sous l'axe, le reflet de M apparaît : le point M prime. Même abscisse, trois. Ordonnée opposée, moins deux. Son affixe est trois moins deux i. On l'appelle le conjugué de z, et on dit z barre. Le conjugué de a plus i b, c'est a moins i b. Tu peux tirer le point M : son reflet le suit. C'est comme un minaret, qui se voit à l'envers dans l'eau.
ÉCRAN : Le conjugué de z = a + ib est z̄ = a − ib (on dit « z barre »). | On garde la partie réelle, on change le signe de la partie imaginaire. | Le point M′(z̄) est le symétrique de M(z) par rapport à l'axe réel. | Exemples : le conjugué de 3 + 2i est 3 − 2i ; celui de −2 + 5i est −2 − 5i.

### Diapo 22 `nc_j2` — Le conjugué passe à travers les opérations
VOIX (fr) : On vérifie la règle sur un exemple. En haut, deux complexes : z égale deux plus i, et z prime égale un moins trois i. Premier calcul : on fait le produit z z prime. On développe, et i carré égale moins un. On trouve cinq moins cinq i. Son conjugué est cinq plus cinq i. Deuxième calcul : on prend d'abord les conjugués, deux moins i, et un plus trois i. Leur produit donne aussi cinq plus cinq i. Les deux calculs donnent le même résultat, encadré en vert. Voilà la règle : le conjugué d'un produit, est le produit des conjugués. De même pour la somme, le quotient et la puissance.
ÉCRAN : Le conjugué d'une somme est la somme des conjugués : z̅+̅z̅′̅ = z̄ + z̄′. | Même règle pour le produit et la puissance : z̅z̅′̅ = z̄·z̄′ ; z̅ⁿ̅ = (z̄)ⁿ (n ∈ ℕ) ; pour z′ ≠ 0, le conjugué de z/z′ est z̄/z̄′. | Vérification : z = 2 + i, z′ = 1 − 3i : zz′ = 5 − 5i, son conjugué est 5 + 5i. | z̄·z̄′ = (2 − i)(1 + 3i) = 5 + 5i : c'est bien le même résultat.

### Diapo 23 `nc_j3` — z̄ = z : reconnaître un réel
VOIX (fr) : Regarde le point M et son reflet M prime, comme tout à l'heure. Maintenant, on pose M sur l'axe réel. Son reflet tombe sur lui-même : M prime égale M. Donc z barre égale z, et z est un réel. Dans l'autre sens, si z barre égale z, alors moins b égale b, donc b égale zéro. Ensuite, on regarde M et M prime ensemble. On ajoute : z plus z barre égale deux a, c'est deux fois la partie réelle. On soustrait, en orange : z moins z barre égale deux i b, c'est deux i fois la partie imaginaire. Et si z barre égale moins z, z est un imaginaire pur.
ÉCRAN : M sur l'axe réel : son reflet M′ est M lui-même, donc z̄ = z. | Si z̄ = z, alors −b = b, donc b = 0. | z réel ⇔ z̄ = z.

### Diapo 24 `nc_j3_b` — z + z̄ et z − z̄
VOIX (fr) : Regardons M et M′ ensemble : z égale trois plus deux i, z barre égale trois moins deux i. On additionne : plus deux i et moins deux i s'annulent ; z plus z barre égale deux a, deux fois la partie réelle : six. On soustrait : les trois s'annulent ; z moins z barre égale deux i b : quatre i. Et si z barre égale moins z, alors a égale zéro : z est imaginaire pur. Je relis : z plus z barre égale deux a, et z moins z barre égale deux i b.
ÉCRAN : z + z̄ = 2Re(z) : les parties imaginaires s'annulent. | z − z̄ = 2i Im(z) : les parties réelles s'annulent. | z imaginaire pur ⇔ z̄ = −z.

### Diapo 25 `nc_j4` — z·z̄ = a² + b²
VOIX (fr) : Au tableau, un exemple d'abord : cinq moins trois i, fois cinq plus trois i. On développe. Les termes en i s'annulent, et moins neuf i carré donne plus neuf. Le résultat est trente-quatre : plus de i ! En vert, la règle : a plus i b, fois a moins i b, égale a carré plus b carré. Donc z fois z barre est un réel positif. En rouge, le piège : a carré moins b carré est faux, car i carré égale moins un. Maintenant, le national deux mille vingt : c égale racine de deux, plus i racine de deux. Son conjugué est racine de deux, moins i racine de deux. Le produit donne deux plus deux, égale quatre. Question : calcule c fois c barre.
ÉCRAN : (a + ib)(a − ib) = a² + b² : les termes en i s'annulent et i² = −1. | z·z̄ est un réel positif : il n'y a plus de i. | Piège : a² − b² est faux, le signe devient + car i² = −1. | 2020 N : c = √2 + i√2 : à toi de calculer c·c̄.
QUESTION : c = √2 + i√2 : combien vaut c·c̄ ? (2020 N) OPTIONS : ['4', '0', '4i']
EXERCICE : (3 + 4i)(3 − 4i) = ? OPTIONS : ['−7', '25', '9 − 16i']

### Diapo 26 `nc_j5` — Résoudre une équation avec z̄
VOIX (fr) : Maintenant une équation avec z et z barre. Résoudre, c'est trouver tous les complexes z qui la vérifient. Exemple : z plus deux z barre égale neuf plus i. D'abord on pose z égale x plus i y, avec x et y réels, donc z barre égale x moins i y. On remplace et on regroupe : trois x moins i y égale neuf plus i. Deux complexes égaux : les parties réelles sont égales, les parties imaginaires aussi. Trois x égale neuf, donc x égale trois ; moins y égale un, donc y égale moins un. Conclusion : S égale l'ensemble formé de trois moins i. On vérifie. Autrement dit : en écrivant z avec x et y, l'équation devient deux équations réelles.
ÉCRAN : On pose z = x + iy, avec x et y réels ; alors z̄ = x − iy. | z + 2z̄ = 9 + i ⇔ x + iy + 2(x − iy) = 9 + i ⇔ 3x − iy = 9 + i. | Deux complexes égaux : 3x = 9 et −y = 1, donc x = 3 et y = −1. | On conclut : S = {3 − i}. Vérification : (3 − i) + 2(3 + i) = 9 + i.
## V. Le module, la distance et les ensembles de points

### Diapo 27 `nc_z3_pythagore` — Rappel : Pythagore et la distance OM
VOIX (fr) : Avant le module, revoyons Pythagore. Le point M de coordonnées trois, quatre. On descend vers l'axe : le point H. Le triangle OHM est rectangle en H : un côté trois, l'autre quatre, et OM le côté penché. Pythagore : OM au carré égale OH au carré plus HM au carré : neuf plus seize, vingt-cinq. Donc OM égale cinq. Autrement dit : une échelle contre un mur, le pied à trois mètres du mur, le haut à quatre mètres : l'échelle mesure cinq mètres. Je relis : dans un triangle rectangle, le carré de l'hypoténuse est la somme des carrés des deux autres côtés.
ÉCRAN : Triangle rectangle : le carré du grand côté est la somme des carrés des deux autres. | M(3 ; 4) : OM² = 3² + 4² = 25, donc OM = 5. | Une échelle : pied à 3 m du mur, haut à 4 m : elle mesure 5 m.

### Diapo 28 `nc_m1` — Le module : une distance
VOIX (fr) : Regarde le point M, de coordonnées trois, quatre. On le projette sur l'axe réel : c'est le point H. Le triangle O H M est rectangle en H. Ses côtés mesurent trois et quatre. On cherche l'hypoténuse O M. Pythagore : O M au carré, égale trois au carré plus quatre au carré, égale vingt-cinq. Donc O M égale cinq. Cette distance porte un nom : le module de z. On l'écrit z entre deux barres, sur l'hypoténuse. Le module de z, égale la racine de a carré plus b carré. C'est la distance O M. En jaune : le module de trois plus quatre i égale cinq.
ÉCRAN : M(3 ; 4) : H est sa projection sur l'axe réel ; le triangle OHM est rectangle en H. | Pythagore : OM² = 3² + 4² = 25, donc OM = 5. | Cette distance s'appelle le module de z : |z| = √(a² + b²) = OM. | |3 + 4i| = 5.

### Diapo 29 `nc_m2` — Calculer un module sans le i
VOIX (fr) : Sur le tableau, un cercle de centre O, de rayon cinq. Le point M glisse sur le cercle. Il passe par moins trois plus quatre i, puis par moins cinq. Le module reste cinq : tous les points du cercle, sont à la même distance de O. Dans le cadre, la règle : le module de a plus i b, égale la racine de a carré plus b carré. a et b sont des réels. Le i n'entre pas dans la racine. En rouge, une fausse écriture avec i carré : elle est barrée. Attention aussi : moins racine de trois, au carré, égale trois. Un carré n'est jamais négatif. Et z fois z barre, égale le module de z au carré.
ÉCRAN : |a + ib| = √(a² + b²), avec a et b réels : le i n'entre pas dans la racine. | Un carré n'est jamais négatif : (−√3)² = 3. | Les points d'un cercle de centre O ont tous le même module : son rayon. | z·z̄ = |z|² : le produit par le conjugué donne le carré du module.

### Diapo 30 `nc_enonce_2017n` — National 2017 N : l’énoncé, tel qu’à l’examen
VOIX (fr) : Maintenant, nous allons lire l'énoncé de l'examen national deux mille dix-sept, la session normale, tel qu'il est à l'examen. Exercice trois, trois points. On considère les nombres complexes a et b, tels que a égale racine de trois plus i, et b égale racine de trois moins un, plus, racine de trois plus un, i. Un a : vérifier que b égale, un plus i, fois a. b : en déduire que le module de b, égale deux racine de deux, et un argument de b, cinq pi sur douze. Maintenant, comprenons l'exercice, question par question.

### Diapo 31 `nc_m3` — Le module d'un produit (national 2017 N, question 1-b)
VOIX (fr) : En haut, en vert, la règle : le module d'un produit est le produit des modules. De même, le module d'un quotient est le quotient des modules. Et le module d'une puissance est la puissance du module. Maintenant, la question un b du national deux mille dix-sept : a égale racine de trois plus i. Le module de a, égale la racine de trois plus un, égale deux. Le module de un plus i, égale racine de deux. En jaune, on multiplie : racine de deux fois deux, égale deux racine de deux. On n'a rien développé. En bas, le piège, en orange : un plus moins un égale zéro, et son module est zéro. Mais le module de un, plus le module de moins un, égale deux. Le module d'une somme n'est pas la somme des modules : la ligne est barrée.
ÉCRAN : |zz′| = |z| × |z′| : on multiplie les modules. | 1-b (2017 N) : |a| = |√3 + i| = 2 ; |1 + i| = √2. | |b| = |(1 + i)a| = √2 × 2 = 2√2, sans développer.

### Diapo 32 `nc_m3_b` — Quotient, puissance… et le piège de la somme
VOIX (fr) : Même idée pour le quotient : le module d'un quotient est le quotient des modules. Et le module d'une puissance est la puissance du module : le module de un plus i, puissance quatre, égale racine de deux puissance quatre, donc quatre. Mais attention, la somme n'obéit pas : un plus moins un égale zéro, de module zéro, alors que le module de un plus le module de moins un égale deux. Le module d'une somme n'est pas la somme des modules.
ÉCRAN : |z/z′| = |z|/|z′| (z′ ≠ 0) et |zⁿ| = |z|ⁿ (n ∈ ℕ). | Piège : |1 + (−1)| = 0 mais |1| + |−1| = 2. | |z + z′| ≠ |z| + |z′| en général.

### Diapo 33 `nc_m4` — La distance AB = |z_B − z_A|
VOIX (fr) : Sur le tableau, deux points : A d'affixe trois moins deux i, et B d'affixe un plus quatre i. On trace la flèche de A vers B. Son affixe : b moins a égale moins deux plus six i. Maintenant, la flèche glisse jusqu'à O, sans tourner. Sa longueur ne change pas. Elle va de O, au point moins deux plus six i. Donc la distance A B, est le module de b moins a. En jaune : A B égale la racine de quarante, égale deux racine de dix. Chaque affixe garde sa couleur, pour ne pas se tromper de signe. Question : calcule la distance A B.
ÉCRAN : Le vecteur AB⃗ a pour affixe z_B − z_A. | Ramené en O, il arrive au point d'affixe z_B − z_A : sa longueur est un module. | AB = |z_B − z_A|. | a = 3 − 2i, b = 1 + 4i : à toi de calculer AB.
QUESTION : a = 3 − 2i et b = 1 + 4i : calcule AB. OPTIONS : ['2√10', '√20', '40']
EXERCICE : A(1 + i), B(4 + 5i) : AB = ? OPTIONS : ['√41', '5', '7']

### Diapo 34 `nc_m5` — Ensembles de points : le cercle et la médiatrice
VOIX (fr) : Regarde le cercle de centre O et de rayon cinq : M se déplace dessus et le module de z reste cinq, c'est-à-dire O M égale cinq. Remplaçons O par un point A : le module de z moins z A est la distance A M. Donc le module de z moins z A égale r signifie A M égale r : c'est le cercle de centre A et de rayon r. Autre cas : le module de z moins z A égale le module de z moins z B, c'est-à-dire A M égale B M : c'est la médiatrice du segment A B. Attention : il faut d'abord écrire z moins quelque chose. Par exemple, le module de deux z moins quatre i égale six donne le module de z moins deux i égale trois : le cercle de centre A d'affixe deux i et de rayon trois.
ÉCRAN : |z − z_A| = AM : le module d'une différence est une distance. | |z − z_A| = r (r > 0) ⇔ AM = r : l'ensemble des points M est le cercle de centre A et de rayon r. | |z − z_A| = |z − z_B| ⇔ AM = BM : l'ensemble des points M est la médiatrice de [AB]. | On transforme d'abord : |2z − 4i| = 6 ⇔ 2|z − 2i| = 6 ⇔ |z − 2i| = 3.

### Diapo 35 `nc_m6` — Ensemble des points M tels que Z soit réel
VOIX (fr) : Regarde le plan : les réels sont sur l'axe réel, les imaginaires purs sur l'axe imaginaire. Z réel signifie que sa partie imaginaire est nulle. Question du national : où sont les points M d'affixe z pour lesquels Z est réel ? Exemple : Z égale un plus i, fois z, moins deux i. On pose z égale x plus i y, avec x et y réels. On développe et on remplace i carré par moins un : Z égale x moins y, plus i fois x plus y moins deux. Z est réel si et seulement si x plus y moins deux égale zéro, c'est-à-dire y égale moins x plus deux : l'ensemble des points M est la droite D. Si Z est un quotient, on enlève le point où le dénominateur est nul. Question : pour le même Z, où sont les points M qui le rendent imaginaire pur ?
ÉCRAN : On pose z = x + iy, avec x et y réels, et on écrit Z sous forme algébrique. | Z = (1 + i)z − 2i = (x − y) + i(x + y − 2). | Z réel ⇔ Im(Z) = 0 ⇔ x + y − 2 = 0 ⇔ y = −x + 2 : la droite (D) d'équation y = −x + 2. | Si Z est un quotient, on enlève le point où le dénominateur est nul : « … privé du point A ».
QUESTION : Même Z = (1 + i)z − 2i, avec z = x + iy : Z est imaginaire pur ⇔ OPTIONS : ["x + y − 2 = 0 : la droite d'équation y = −x + 2", "x − y = 0 : la droite d'équation y = x", 'x² + y² = 4 : le cercle de centre O et de rayon 2']
## VI. L'argument

### Diapo 36 `nc_z4_cercle` — Rappel : le cercle trigonométrique
VOIX (fr) : Avant l'argument, revoyons le cercle trigonométrique, de centre O et de rayon un. Les angles se mesurent avec pi : un tour, deux pi ; un demi-tour, pi ; un quart de tour, pi sur deux. Le point M sur le cercle, à l'angle téta égale pi sur trois. On le projette sur les deux axes : son abscisse s'appelle cos téta, son ordonnée sin téta. Ici cos pi sur trois égale un demi, sin pi sur trois égale racine de trois sur deux. Autrement dit : la lumière vient d'en haut ; l'ombre de M sur l'axe horizontal, c'est cos téta. Je relis : sur le cercle trigonométrique, M a pour coordonnées cos téta et sin téta.
ÉCRAN : Cercle de centre O et de rayon 1 : un tour = 2π, un demi-tour = π, un quart de tour = π/2. | M à l'angle θ : M(cos θ ; sin θ). | cos π/3 = 1/2 et sin π/3 = √3/2.

### Diapo 37 `nc_g1` — L'argument : l'angle de u vers OM
VOIX (fr) : Regarde le plan complexe. Le point M est sur un cercle, de rayon deux. Son affixe est z. Maintenant, regarde l'arc qui part de u. Il tourne de u vers OM, dans le sens inverse des aiguilles. Cet angle s'appelle l'argument de z. On écrit : arg z, congru à teta, modulo deux pi. Le module, c'est une distance. L'argument, c'est un angle. Regarde M glisser sur le cercle. Le module reste deux, mais l'angle change. Même module, autre argument.
ÉCRAN : M est l'image de z ≠ 0 ; on regarde la demi-droite [OM). | Un argument de z est une mesure, en radians, de l'angle orienté (u⃗, OM⃗) : de u⃗ vers OM⃗. | Sens positif : le sens inverse des aiguilles d'une montre. | M glisse sur le cercle : même module, autre argument.

### Diapo 38 `nc_g2` — Un tour de plus, le même point : [2π]
VOIX (fr) : Regarde le point M sur le cercle. L'arc dessine l'angle pi sur trois. Maintenant, M fait un tour complet. Il revient exactement au même point. Un tour complet, c'est deux pi. Donc pi sur trois plus deux pi, égale sept pi sur trois. C'est le même point. Voilà pourquoi on écrit modulo deux pi. arg z, congru à pi sur trois, modulo deux pi. Regarde le point O, entouré. O n'a pas de direction. Donc zéro n'a pas d'argument.
ÉCRAN : Un tour complet mesure 2π : M revient au même point. | π/3 et π/3 + 2π = 7π/3 donnent le même point. | Un argument est défini à 2π près : arg z ≡ π/3 [2π]. | 0 n'a pas d'argument : le point O n'a pas de direction.

### Diapo 39 `nc_g3` — Arguments des réels et des imaginaires purs
VOIX (fr) : Regarde le point deux, sur l'axe réel, à droite. Il est déjà dans la direction de u. L'angle est zéro. Maintenant, le point moins trois, à gauche. De u vers lui, c'est un demi-tour : pi. Ensuite, le point deux i, en haut de l'axe imaginaire. Un quart de tour : pi sur deux. Enfin, le point moins deux i, en bas. Un quart de tour dans l'autre sens : moins pi sur deux. Seul le côté compte, pas la distance.
ÉCRAN : 2 est sur l'axe réel, à droite : arg 2 ≡ 0 [2π]. | −3 est sur l'axe réel, à gauche (demi-tour) : arg(−3) ≡ π [2π]. | 2i est sur l'axe imaginaire, en haut : arg(2i) ≡ π/2 [2π]. | −2i est sur l'axe imaginaire, en bas : arg(−2i) ≡ −π/2 [2π].

### Diapo 40 `nc_g4` — a = r cos θ, b = r sin θ
VOIX (fr) : Pour trouver l'angle, on part de a et b. Le point M d'affixe a plus i b est à la distance r de O, le module, et à l'angle téta. On le projette : a sur l'axe réel, b sur l'axe imaginaire. Sur le cercle de rayon un on lisait cos téta et sin téta ; ici le rayon est r, tout est multiplié par r : a égale r cos téta, b égale r sin téta. On divise par r : cos téta égale a sur r, sin téta égale b sur r. Autrement dit : cos téta, c'est la part de r qu'on avance, sin téta la part qu'on monte. Je relis : cos téta égale a sur r, et sin téta égale b sur r.
ÉCRAN : z = a + ib ≠ 0, r = |z| et θ ≡ arg z [2π] : a = r cos θ et b = r sin θ. | Donc cos θ = a/r et sin θ = b/r.

### Diapo 41 `nc_g4_b` — Le tableau des angles remarquables
VOIX (fr) : Il reste à reconnaître l'angle. Le premier quart du cercle : zéro, pi sur six, pi sur quatre, pi sur trois, pi sur deux, avec sous chaque angle son cosinus et son sinus. L'astuce : racine de zéro sur deux, racine de un sur deux, racine de deux sur deux, racine de trois sur deux, racine de quatre sur deux ; elle monte pour le sinus, elle descend pour le cosinus. Question : quel angle a pour cosinus et pour sinus racine de deux sur deux ?
ÉCRAN : Astuce du sinus : √0/2, √1/2, √2/2, √3/2, √4/2 pour 0, π/6, π/4, π/3, π/2. | Le cosinus lit la même liste à l'envers : cos π/4 = sin π/4 = √2/2.
QUESTION : Quel angle θ a pour cosinus √2/2 et pour sinus √2/2 ? OPTIONS : ['π/6', 'π/3', 'π/4']
EXERCICE : r = 2 et a = 1 : combien vaut cos θ ? OPTIONS : ['1/2', '2', '√3/2']
## VII. La forme trigonométrique

### Diapo 42 `nc_t1` — La forme trigonométrique z = r(cos θ + i sin θ)
VOIX (fr) : Regarde le point racine de trois plus i. D'abord le module. OM égale racine de, trois plus un, donc deux. Ensuite, on met deux en facteur. Racine de trois plus i, égale deux fois, racine de trois sur deux, plus un demi i. Maintenant, le tableau. Racine de trois sur deux, c'est cos pi sur six. Un demi, c'est sin pi sur six. L'arc pi sur six se dessine. Voici la forme trigonométrique : deux fois, cos pi sur six, plus i sin pi sur six. En général, z égale r fois, cos teta plus i sin teta. r est le module, strictement positif. Teta est un argument.
ÉCRAN : 1. Le module : r = |√3 + i| = √(3 + 1) = 2. | 2. r en facteur : √3 + i = 2(√3/2 + (1/2)i). | 3. Le tableau : √3/2 = cos π/6 et 1/2 = sin π/6. | √3 + i = 2(cos π/6 + i sin π/6) : r = 2 > 0 et arg(√3 + i) ≡ π/6 [2π].

### Diapo 43 `nc_t2` — National 2023 N, exercice 2 : question 1, a = √2 + i√2 sous forme trigonométrique
VOIX (fr) : Voici la question un du national deux mille vingt-trois. a égale racine de deux, plus i racine de deux. Première ligne, le module. Racine de, racine de deux au carré, plus racine de deux au carré. Ça fait racine de quatre, donc deux. À toi : mets deux en facteur, et cherche l'angle dans le tableau. Question : quelle est la forme trigonométrique de a ?
ÉCRAN : Ligne 1 : |a| = √((√2)² + (√2)²) = √4 = 2. | Ligne 2, à toi : a = 2(… + …i). | Ligne 3, à toi : l'angle lu dans le tableau. | Ligne 4 : arg a ≡ … [2π]. Toujours la forme complète (0,5 point).
QUESTION : 2023 N : a = √2 + i√2 et |a| = 2. La forme trigonométrique de a est : OPTIONS : ['a = 2(cos π/4 + i sin π/4)', 'a = 2(cos π/3 + i sin π/3)', 'a = √2(cos π/4 + i sin π/4)']

### Diapo 44 `nc_t3` — Les signes choisissent le quart : π − θ, π + θ, −θ
VOIX (fr) : Regarde le point moins racine de trois plus i. Il est à gauche, et en haut. a est négatif, b est positif. Le module est encore deux. On met deux en facteur : deux fois, moins racine de trois sur deux, plus un demi i. Attention, ce n'est pas pi sur six. Le cosinus est négatif. Regarde l'arc : il va jusqu'au deuxième quart. L'angle est pi moins pi sur six, donc cinq pi sur six. La forme trigonométrique : deux fois, cos cinq pi sur six, plus i sin cinq pi sur six. Retiens : à gauche en haut, pi moins teta. À gauche en bas, pi plus teta. À droite en bas, moins teta. La calculatrice sert seulement à vérifier.
ÉCRAN : −√3 + i : a < 0 et b > 0, le point est à gauche, en haut. | r = 2 et −√3 + i = 2(−√3/2 + (1/2)i). | Le tableau donne π/6 ; à gauche en haut : θ = π − π/6 = 5π/6.

### Diapo 45 `nc_t3_b` — Les trois autres quarts : π − θ, π + θ, −θ
VOIX (fr) : Maintenant tous les cas, un par un. Le point racine de trois plus i, à droite en haut : le tableau donne pi sur six, l'angle de référence. Premier cas : moins racine de trois plus i, à gauche en haut : pi moins pi sur six, cinq pi sur six. Deuxième cas : moins racine de trois moins i, à gauche en bas : un demi-tour plus pi sur six, sept pi sur six. Troisième cas : racine de trois moins i, à droite en bas : moins pi sur six. Le module reste deux, seul le quart change l'angle. Je relis : à gauche en haut, pi moins téta ; à gauche en bas, pi plus téta ; à droite en bas, moins téta.
ÉCRAN : Le tableau donne l'angle de référence : π/6 pour √3 + i. | À gauche en haut (a < 0, b > 0) : π − π/6 ; à gauche en bas (a < 0, b < 0) : π + π/6. | À droite en bas (a > 0, b < 0) : −π/6. Le module reste 2.

### Diapo 46 `nc_t4` — Deux fausses formes trigonométriques
VOIX (fr) : Regarde cette écriture : moins deux fois, cos pi sur trois, plus i sin pi sur trois. Le moins deux est entouré en rouge. Un module est une distance, donc r est toujours strictement positif. Ce n'est pas une forme trigonométrique. Pour corriger, le moins rentre dans l'angle. Moins cos teta, égale cos de pi plus teta. Moins sin teta, égale sin de pi plus teta. On obtient deux fois, cos quatre pi sur trois, plus i sin quatre pi sur trois. Deuxième fausse forme : deux fois, moins cos teta, plus i sin teta. Le moins devant le cosinus est barré. On écrit deux fois, cos de pi moins teta, plus i sin de pi moins teta. Question : moins deux fois, cos pi sur trois, plus i sin pi sur trois, est-ce une forme trigonométrique ?
ÉCRAN : Dans r(cos θ + i sin θ), r est le module : r > 0 toujours. | Le moins rentre dans l'angle : −cos θ = cos(π + θ) et −sin θ = sin(π + θ).
QUESTION : −2(cos π/3 + i sin π/3) est-elle une forme trigonométrique ? Corrige-la. OPTIONS : ['Oui, telle quelle', 'Non : elle vaut 2(cos 4π/3 + i sin 4π/3)', 'Non : elle vaut 2(cos(−π/3) + i sin(−π/3))']
EXERCICE : Corrige 2(−cos π/6 + i sin π/6). OPTIONS : ['2(cos 5π/6 + i sin 5π/6)', '2(cos 7π/6 + i sin 7π/6)', '2(cos(−π/6) + i sin(−π/6))']

### Diapo 47 `nc_t4_b` — Le moins devant le cosinus seul
VOIX (fr) : Revenons à la première écriture : moins deux fois cos pi sur trois plus i sin pi sur trois devient deux fois cos quatre pi sur trois plus i sin quatre pi sur trois. Deuxième erreur : deux fois moins cos téta plus i sin téta. Le moins est seulement devant le cosinus : on utilise pi moins téta. Moins cos téta égale cos de pi moins téta, et sin téta égale sin de pi moins téta. On écrit deux fois cos de pi moins téta plus i sin de pi moins téta. Je relis : dans la forme trigonométrique, le module est positif, et il n'y a pas de moins devant cos et sin.
ÉCRAN : −2(cos π/3 + i sin π/3) = 2(cos 4π/3 + i sin 4π/3). | 2(−cos θ + i sin θ) : −cos θ = cos(π − θ) et sin θ = sin(π − θ). | Donc 2(−cos θ + i sin θ) = 2(cos(π − θ) + i sin(π − θ)).

### Diapo 48 `nc_t5` — Retour : de la forme trigonométrique à la forme algébrique
VOIX (fr) : Maintenant, le chemin inverse. Regarde la forme : deux fois, cos deux pi sur trois, plus i sin deux pi sur trois. On remplace cos et sin par leurs valeurs. Deux pi sur trois, c'est pi moins pi sur trois. Donc cos deux pi sur trois égale moins un demi. Et sin deux pi sur trois, égale racine de trois sur deux. On développe : deux fois moins un demi, égale moins un. Deux fois racine de trois sur deux, égale racine de trois. Le résultat : moins un, plus i racine de trois. Regarde le point se placer. Il est à gauche, en haut, avec l'arc deux pi sur trois.
ÉCRAN : On remplace cos θ et sin θ par leurs valeurs, puis on développe. | 2π/3 = π − π/3 : cos 2π/3 = −1/2 et sin 2π/3 = √3/2. | 2(cos 2π/3 + i sin 2π/3) = 2(−1/2 + (√3/2)i) = −1 + i√3. | Contrôle : le point est à gauche, en haut, à la distance 2 de O.

### Diapo 49 `nc_enonce_2024n` — National 2024 N : l’énoncé, tel qu’à l’examen
VOIX (fr) : Maintenant, nous allons lire l'énoncé de l'examen national deux mille vingt-quatre, la session normale, tel qu'il est à l'examen. Exercice trois, quatre points. Dans le plan complexe, on considère les points A et B, d’affixes a égale racine de trois, fois un moins i, et b égale deux plus racine de trois, plus i. Un : vérifier que le module de a, égale racine de six, et un argument de a, moins pi sur quatre. Maintenant, comprenons cette question.

### Diapo 50 `nc_t6` — National 2024 N, exercice 3 : question 1, vérifier |a| et arg a
VOIX (fr) : Voici la question un du sujet national, deux mille vingt-quatre. a égale racine de trois, fois un moins i. On demande de vérifier, le module et l'argument. Regarde la règle en orange. Le module d'un produit, c'est le produit des modules. Racine de trois est un réel positif. Donc le module de a égale racine de trois, fois le module de un moins i. Racine de trois fois racine de deux, égale racine de six. Ensuite, on met racine de six en facteur. On trouve racine de deux sur deux, moins racine de deux sur deux i. Le cosinus est positif, le sinus est négatif. C'est le quatrième quart : moins pi sur quatre. Donc arg a, congru à moins pi sur quatre, modulo deux pi.
ÉCRAN : |λz| = |λ| × |z| : √3 est un réel positif, il sort du module. | |a| = √3 × |1 − i| = √3 × √2 = √6. | a = √6(√2/2 − (√2/2)i) : cos positif, sin négatif, quatrième quart. | = √6(cos(−π/4) + i sin(−π/4)), donc arg a ≡ −π/4 [2π].
## VIII. Produit, quotient et Moivre

### Diapo 51 `nc_r1` — Le produit : modules multipliés, arguments additionnés
VOIX (fr) : Regarde le point un plus i. Son module est racine de deux. Son argument est pi sur quatre. Maintenant, on le multiplie par lui-même. Regarde l'angle pi sur quatre, posé deux fois : pi sur deux. Et la longueur : racine de deux fois racine de deux, égale deux. Le point deux i se pose. Vérifie : un plus i au carré, égale deux i. Voilà la règle du produit. Le module d'un produit est le produit des modules. L'argument d'un produit, c'est la somme des arguments, à deux pi près. Comme une photo sur un téléphone : on l'agrandit, et on la tourne.
ÉCRAN : 1 + i : module √2, argument π/4. | (1 + i)² : longueur √2 × √2 = 2, angle π/4 + π/4 = π/2 : c'est 2i. | |zz′| = |z| × |z′| et arg(zz′) ≡ arg z + arg z′ [2π] (z et z′ non nuls). | Les modules se multiplient, ils ne s'additionnent pas.
OBSERVATION : Regarde les deux arcs : quel est l'angle de (1 + i)² ?

### Diapo 52 `nc_r2` — Multiplier par i : un quart de tour
VOIX (fr) : Regarde le point trois plus i. Maintenant, on le multiplie par i. Le module de i est un. Son argument est pi sur deux. Donc la longueur ne change pas, et on ajoute pi sur deux. Regarde : le point tourne d'un quart de tour, autour de O. Il arrive en moins un plus trois i. Le calcul le confirme. i fois trois plus i, égale trois i plus i au carré. Comme i au carré égale moins un, on trouve moins un, plus trois i. C'est le quart de tour du début du chapitre. Dans la partie deux, il aura un nom : la rotation. Question : où arrive le point trois plus i, quand on multiplie par i ?
ÉCRAN : |i| = 1 et arg i ≡ π/2 [2π]. | Multiplier par i : la longueur ne change pas, l'angle augmente de π/2. | Un quart de tour autour de O ; en partie 2, il aura un nom : la rotation.
QUESTION : Où arrive le point d'affixe 3 + i quand on multiplie par i ? OPTIONS : ['3 − i', '−1 + 3i', '−3 − i']
EXERCICE : Où arrive le point d'affixe 2 quand on multiplie par i ? OPTIONS : ['2i', '−2', '2 + i']

### Diapo 53 `nc_r3` — Le conjugué et l'inverse : l'angle change de signe
VOIX (fr) : Regarde le point z. Son module est deux, son argument pi sur trois. D'abord, le conjugué z barre. C'est le symétrique de z, par rapport à l'axe réel. Même longueur, deux. Et l'angle devient moins pi sur trois. Ensuite, l'inverse un sur z. Son angle est aussi moins pi sur trois. Mais la longueur devient un sur deux. Enfin, le quotient z sur z prime. On divise les modules. Et on recule de l'angle de z prime : arg z moins arg z prime. Pour moins z, c'est un demi-tour : pi plus arg z.
ÉCRAN : Conjugué (z ≠ 0) : |z̄| = |z| et arg z̄ ≡ −arg z [2π]. | Inverse (z ≠ 0) : |1/z| = 1/|z| et arg(1/z) ≡ −arg z [2π]. | z = 2(cos π/3 + i sin π/3) : 1/z = (1/2)(cos(−π/3) + i sin(−π/3)).

### Diapo 54 `nc_r3_b` — Le quotient et l'opposé
VOIX (fr) : Maintenant le quotient z sur z′ : on divise les modules, et on recule de l'angle de z′ : arg z moins arg z′. Le quotient fait l'inverse du produit : le produit ajoute les angles, le quotient les retranche. Et moins z, c'est un demi-tour : son argument est pi plus arg z. Je relis : l'argument de z sur z′ égale arg z moins arg z′, modulo deux pi.
ÉCRAN : Quotient (z et z′ non nuls) : |z/z′| = |z|/|z′| et arg(z/z′) ≡ arg z − arg z′ [2π]. | Le produit ajoute les angles, le quotient les retranche. | Opposé (z ≠ 0) : arg(−z) ≡ π + arg z [2π] (un demi-tour).

### Diapo 55 `nc_enonce_2017n_p2` — National 2017 N : la suite de l’énoncé
VOIX (fr) : Même exercice du national deux mille dix-sept : a égale racine de trois plus i, et b égale, un plus i, fois a. Voici la suite de l'énoncé. Un b : en déduire que le module de b, égale deux racine de deux, et un argument de b, cinq pi sur douze. c : déduire le cosinus, de cinq pi sur douze. Maintenant, comprenons l'exercice, question par question.

### Diapo 56 `nc_r4` — National 2017 N, exercice 3 : question 1-b, |b| et arg b par b = (1 + i)a
VOIX (fr) : Sur la figure, deux points : z et z prime, avec leurs angles teta et teta prime. Regarde le produit. Les deux arcs se mettent bout à bout : teta plus teta prime. Et la longueur devient r fois r prime. La règle s'écrit dans le cadre. Le module d'un produit, est le produit des modules. L'argument d'un produit, est la somme des arguments. Question un b du national deux mille dix-sept : b égale un plus i, fois a. Avec a égale racine de trois plus i. Le module de a est deux, son argument pi sur six. Le module de un plus i est racine de deux, son argument pi sur quatre. Donc le module de b égale deux racine de deux, et l'argument de b, pi sur quatre plus pi sur six, égale cinq pi sur douze.
ÉCRAN : a = √3 + i : |a| = 2 et arg a ≡ π/6 [2π]. | 1 + i : |1 + i| = √2 et arg(1 + i) ≡ π/4 [2π]. | 1-b : |b| = |1 + i| × |a| = 2√2 : les modules se multiplient. | 1-b : arg b ≡ π/4 + π/6 ≡ 5π/12 [2π] : les arguments s'additionnent.

### Diapo 57 `nc_r5` — National 2017 N, exercice 3 : question 1-c, cos 5π/12 par identification
VOIX (fr) : Question un c du national deux mille dix-sept : le même nombre b, écrit de deux façons. En blanc, on développe : un plus i, fois racine de trois plus i. i carré devient moins un. En jaune, la forme algébrique : racine de trois moins un, plus racine de trois plus un, fois i. En cyan, la forme trigonométrique trouvée avant : deux racine de deux, facteur de cos cinq pi sur douze, plus i sin cinq pi sur douze. Deux écritures du même nombre : les parties réelles sont égales. En vert : deux racine de deux, fois cos cinq pi sur douze, égale racine de trois moins un. On isole le cosinus, et on multiplie en haut et en bas, par racine de deux. Le résultat encadré : racine de six moins racine de deux, sur quatre.
ÉCRAN : 1-c : on développe : b = (1 + i)(√3 + i) = (√3 − 1) + (√3 + 1)i. | Avec la diapositive précédente : b = 2√2(cos 5π/12 + i sin 5π/12). | Même nombre, deux écritures : on égale les parties réelles. | cos 5π/12 = (√3 − 1)/(2√2) = (√6 − √2)/4.

### Diapo 58 `nc_r6` — Moivre : la puissance multiplie l'angle
VOIX (fr) : D'abord, sur le cercle de rayon un. Le point z a l'angle pi sur quatre. z carré, z cube, jusqu'à z puissance huit. À chaque fois, l'angle avance de pi sur quatre. Une puissance, c'est un produit répété. Donc les angles s'additionnent. Maintenant z égale un plus i. Sa longueur est racine de deux. Les points s'écartent : une spirale. Les longueurs se multiplient aussi. Après huit pas, on tombe sur l'axe réel, en seize. La formule de Moivre est dans le cadre. r puissance n, facteur de cos n teta plus i sin n teta. Question : un plus i, puissance huit, égale combien ?
ÉCRAN : zⁿ = z × z × … × z : les modules se multiplient, les arguments s'additionnent. | Formule de Moivre : (cos θ + i sin θ)ⁿ = cos nθ + i sin nθ. | [r(cos θ + i sin θ)]ⁿ = rⁿ(cos nθ + i sin nθ) (n ∈ ℕ) : le module aussi est élevé à la puissance. | (1 + i)⁸ = (√2)⁸(cos 2π + i sin 2π) = 16.
QUESTION : D'après la formule de Moivre, (√3 + i)⁶ = ? OPTIONS : ['64', '−64', '64i']
EXERCICE : 1 + i√3 = 2(cos π/3 + i sin π/3). Alors (1 + i√3)⁶ = OPTIONS : ['−64', '64', '2']

### Diapo 59 `nc_enonce_2020r` — National 2020 R : l’énoncé, tel qu’à l’examen
VOIX (fr) : Maintenant, nous allons lire l'énoncé de l'examen national deux mille vingt, la session de rattrapage, tel qu'il est à l'examen. Exercice deux, cinq points. Deux : on pose a, égale racine de deux sur deux, plus racine de deux sur deux, i. a : écrire a sous forme trigonométrique, et en déduire que a puissance deux mille vingt, est un nombre réel. Maintenant, comprenons cette question.

### Diapo 60 `nc_r7` — National 2020 R, exercice 2 : question 2-a, une puissance réelle
VOIX (fr) : Sur le cercle, les puissances de a. a égale cos pi sur quatre, plus i sin pi sur quatre. Chaque puissance avance de pi sur quatre. Regarde : certaines puissances tombent sur l'axe réel. Elles s'allument. C'est quand n teta est un multiple de pi. Alors le sinus est nul, et la puissance est un réel. D'autres tombent sur l'axe imaginaire. Là, le cosinus est nul : imaginaire pur. Question deux a du national deux mille vingt, rattrapage : a puissance deux mille vingt. Deux mille vingt fois pi sur quatre, égale cinq cent cinq pi.
ÉCRAN : 2-a (2020 R) : a = √2/2 + (√2/2)i = cos π/4 + i sin π/4 (module 1). | 2-a : Moivre : a²⁰²⁰ = cos(2020π/4) + i sin(2020π/4) = cos 505π + i sin 505π. | sin 505π = 0 : la partie imaginaire est nulle ; a²⁰²⁰ = −1, un réel. | zⁿ est réel quand nθ est un multiple de π ; imaginaire pur quand nθ = π/2 + kπ (k entier).

### Diapo 61 `nc_enonce_2023r` — National 2023 R : l’énoncé, tel qu’à l’examen
VOIX (fr) : Maintenant, nous allons lire l'énoncé de l'examen national deux mille vingt-trois, la session de rattrapage, tel qu'il est à l'examen. Exercice trois, trois points. Un : on considère le nombre complexe a, égale racine de trois sur deux, plus trois demis i. a : montrer que a égale racine de trois, fois, cos pi sur trois, plus i sin pi sur trois. b : déduire que a puissance deux mille vingt-deux, est un nombre réel. Maintenant, comprenons l'exercice, question par question.

### Diapo 62 `nc_r8` — National 2023 R, exercice 3 : questions 1-a et 1-b, Moivre plutôt que développer
VOIX (fr) : Questions un a et un b du national deux mille vingt-trois, rattrapage. a égale racine de trois sur deux, plus trois sur deux i. Développer a puissance deux mille vingt-deux ? Impossible. Alors, question un a : d'abord la forme trigonométrique. En cyan, le module : racine de trois quarts plus neuf quarts. C'est racine de trois. On met racine de trois en facteur : un demi, plus racine de trois sur deux i. C'est cos pi sur trois, plus i sin pi sur trois. Question un b : Moivre, en blanc. Attention, en rouge : le module aussi est élevé à la puissance. Racine de trois puissance deux mille vingt-deux, égale trois puissance mille onze. Et deux mille vingt-deux pi sur trois, égale six cent soixante-quatorze pi. Un nombre pair de pi : le cosinus vaut un. Le résultat encadré : trois puissance mille onze, un réel.
ÉCRAN : Développer (√3/2 + (3/2)i)²⁰²² à la main : impossible. | 1-a : |a| = √3 et a = √3(cos π/3 + i sin π/3). | 1-b : Moivre : a²⁰²² = (√3)²⁰²²(cos 2022π/3 + i sin 2022π/3). | (√3)²⁰²² = 3¹⁰¹¹ et 2022π/3 = 674π : a²⁰²² = 3¹⁰¹¹, un réel.
## IX. Géométrie : alignement, distances, angles, nature d'un triangle

### Diapo 63 `nc_i1` — Trois points alignés : un quotient réel
VOIX (fr) : Regarde A, B et deux vecteurs qui partent de A : AB et AC. Les deux vecteurs ont la même origine, A. Quand C est sur la droite AB, AC égale k fois AB. Avec les affixes : c moins a, égale k fois, b moins a. Donc le quotient, c moins a sur b moins a, égale k. Un réel : la valeur s'affiche sur l'axe réel. Maintenant on tire C hors de la droite. Le quotient quitte l'axe réel. Pas réel : pas alignés. Au national deux mille vingt et un, rattrapage : a égale trois plus deux i. c égale moins un moins deux i, d égale moins trois moins quatre i.
ÉCRAN : A, B, C alignés ⇔ AC⃗ = k·AB⃗ avec k réel : deux vecteurs colinéaires de même origine A. | En affixes : c − a = k(b − a), donc (c − a)/(b − a) = k, un réel. | On garde la même origine A en haut et en bas : (c − a)/(b − a). | Quotient avec une partie imaginaire non nulle : les points ne sont pas alignés.
QUESTION : 2021 R : a = 3 + 2i, c = −1 − 2i, d = −3 − 4i. Que vaut (d − a)/(c − a), et que conclure ? OPTIONS : ['3/2 : A, C et D sont alignés', '(3/2)i : A, C et D ne sont pas alignés', '−3/2 : A, C et D ne sont pas alignés']
EXERCICE : A(1), B(2 + i), C(4 + 3i) : que vaut (c − a)/(b − a) ? OPTIONS : ['1 + i : alignés', '3 : alignés', '3i : pas alignés']

### Diapo 64 `nc_enonce_2025n` — National 2025 N : l’énoncé, tel qu’à l’examen
VOIX (fr) : Maintenant, nous allons lire l'énoncé de l'examen national deux mille vingt-cinq, la session normale, tel qu'il est à l'examen. Exercice deux, trois points et demi. Dans le plan complexe, on considère les points A, B, C, D et oméga, d’affixes a égale un plus deux i, b égale a barre, c égale trois fois, trois plus i, sur deux, d égale trois fois, un plus i, sur deux, et oméga égale cinq demis. Deux a : vérifier que oméga moins a, oméga moins b, et oméga moins c, ont le même module. Maintenant, comprenons cette question.

### Diapo 65 `nc_i2` — National 2025 N, exercice 2 : question 2-a, égalité de distances
VOIX (fr) : Question deux a du national deux mille vingt-cinq. Regarde A et B. a égale un plus deux i, b égale un moins deux i. B est le symétrique de A, par rapport à l'axe réel : b égale a barre. Ensuite, Omega, d'affixe cinq sur deux, sur l'axe réel. Le symétrique de Omega, c'est Omega lui-même. Donc les deux segments, Omega A et Omega B, ont la même longueur. On le vérifie par le calcul. Omega A, c'est le module de omega moins a. Trois sur deux moins deux i : racine de neuf quarts plus quatre, égale cinq sur deux. De même, Omega C : le module de moins deux moins trois sur deux i, égale cinq sur deux. Question : sans calculer, pourquoi Omega A égale Omega B ?
ÉCRAN : 2-a : ΩA = |ω − a| : une distance est le module d'une différence. | b = ā : B est le reflet de A dans l'axe réel ; ω = 5/2 est sur cet axe. | ΩC = |ω − c| = |−2 − (3/2)i| = √(4 + 9/4) = 5/2. | À toi : pourquoi ΩA = ΩB, sans calcul ?
QUESTION : ω = 5/2, a = 1 + 2i, b = 1 − 2i : sans calculer, pourquoi ΩA = ΩB ? OPTIONS : ["B est le symétrique de A par rapport à l'axe réel, qui contient Ω", "a et b ont la même partie imaginaire, et Ω est sur l'axe réel", "Ω est sur l'axe imaginaire, car ω = 5/2 est un nombre imaginaire pur"]
EXERCICE : 2025 N : P est le milieu de [AB], avec a = 1 + 2i et b = 1 − 2i. Alors p = OPTIONS : ['1 + 2i', '2', '1']

### Diapo 66 `nc_i3` — L'angle de deux vecteurs : l'argument du quotient
VOIX (fr) : Regarde les deux vecteurs qui partent de A : A B et A C. D'abord C est sur la droite A B et le quotient tombe sur l'axe réel. On tire C hors de la droite : le quotient sort de l'axe réel et son angle apparaît. Cet angle est l'angle entre le vecteur A B et le vecteur A C. Pourquoi ? L'affixe du vecteur A B est b moins a, donc son angle avec u est l'argument de b moins a ; de même pour A C. L'angle de A B vers A C est la différence des arguments, c'est-à-dire l'argument du quotient. Deux cas importants : quotient réel, angle zéro ou pi, les points sont alignés ; quotient imaginaire pur, angle pi sur deux ou moins pi sur deux, les droites A B et A C sont perpendiculaires. Exemple : a égale un plus i, b égale trois plus deux i, c égale trois i : le quotient vaut i, donc A B et A C sont perpendiculaires.
ÉCRAN : Pour A ≠ B : AB⃗ a pour affixe b − a, donc (u⃗, AB⃗) ≡ arg(b − a) [2π]. | Pour A ≠ B et A ≠ C : (AB⃗, AC⃗) ≡ arg(c − a) − arg(b − a) ≡ arg((c − a)/(b − a)) [2π]. | Quotient réel : angle 0 ou π, A, B, C alignés. Quotient imaginaire pur : angle π/2 ou −π/2, (AB) ⊥ (AC). | Exemple : a = 1 + i, b = 3 + 2i, c = 3i : (c − a)/(b − a) = i, donc (AB⃗, AC⃗) ≡ π/2 [2π] et (AB) ⊥ (AC).

### Diapo 67 `nc_i4` — La nature d'un triangle
VOIX (fr) : Regarde le tableau : la distance A B est le module de b moins a. Chaque côté d'un triangle est une distance. Pour trouver la nature d'un triangle, on compare les côtés et on cherche l'angle. Premier exemple : a égale deux, b égale un plus i racine de trois, c égale trois plus i racine de trois. A B, A C et B C valent tous deux : le triangle est équilatéral. Deuxième exemple : le quotient c moins a sur b moins a égale i. Le module de i vaut un, donc A C égale A B : isocèle. L'argument de i vaut pi sur deux : l'angle en A est droit. Conclusion : le triangle A B C est isocèle et rectangle en A. Question : si le quotient vaut deux i, quelle est la nature du triangle A B C ?
ÉCRAN : Les côtés sont des distances : AB = |b − a|, AC = |c − a|, BC = |c − b|. | a = 2, b = 1 + i√3, c = 3 + i√3 : AB = AC = BC = 2, donc ABC est équilatéral. | (c − a)/(b − a) = i : |i| = 1 donne AC = AB ; arg i ≡ π/2 [2π] donne (AB) ⊥ (AC). | Donc ABC est isocèle et rectangle en A.
QUESTION : (c − a)/(b − a) = 2i : quelle est la nature du triangle ABC ? OPTIONS : ['isocèle et rectangle en A', 'rectangle en A, mais pas isocèle', 'équilatéral']
## X. Deux sujets nationaux, une question à la fois

### Diapo 68 `nc_enonce_2023n` — National 2023 N : l’énoncé, tel qu’à l’examen
VOIX (fr) : Maintenant, nous allons lire l'énoncé de l'examen national deux mille vingt-trois, la session normale, tel qu'il est à l'examen. Exercice deux, trois points. Dans le plan complexe, on considère les points A, B, C et D, d’affixes a égale racine de deux, plus i racine de deux, b égale un plus racine de deux, plus i, c égale b barre, et d égale deux i. Un : écrire a, sous forme trigonométrique. Deux a : vérifier que b moins d, égale c. b : montrer que, racine de deux plus un, fois b moins a, égale b moins d, et déduire que A, B et D sont alignés. Maintenant, comprenons l'exercice, question par question.

### Diapo 69 `nc_n1` — National 2023 N, exercice 2 : questions 1 et 2-a
VOIX (fr) : Voici un sujet entier : national deux mille vingt-trois. En blanc, l'énoncé : a, b, c égale b barre, et d égale deux i. Regarde les points A, B et D dans le plan. Question un, en bleu : la forme trigonométrique de a. On l'a déjà faite : deux, facteur de cos pi sur quatre, plus i sin pi sur quatre. Sur la figure : O A égale deux, et l'angle est pi sur quatre. Question deux a, à toi : calcule b moins d, et compare avec c. Question : combien vaut b moins d ?
ÉCRAN : a = √2 + i√2, b = 1 + √2 + i, c = b̄, d = 2i. | Question 1 : a = 2(cos π/4 + i sin π/4). | 2-a, à toi : calcule b − d, puis compare avec c.
QUESTION : 2023 N : b = 1 + √2 + i et d = 2i. Que vaut b − d ? OPTIONS : ['1 + √2 − i = b̄ = c', '1 + √2 + 3i = b̄ + 4i', '−1 − √2 + i = −b̄ = −c']

### Diapo 70 `nc_n1_b` — National 2023 N, exercice 2 : question 2-a corrigée, puis 2-b
VOIX (fr) : Continuons le sujet de deux mille vingt-trois. Question deux a : b moins d égale un plus racine de deux plus i, moins deux i. Donc un plus racine de deux moins i, c'est c. Regarde la figure : enlever deux i, c'est descendre de deux. Le point B descend, et arrive sur C, le symétrique de B. Question deux b : d'abord, montrer que racine de deux plus un, fois b moins a, égale b moins d. b moins a égale un, plus un moins racine de deux, fois i. Multiplié par racine de deux plus un, on trouve racine de deux plus un, moins i : c'est c, donc b moins d. Que peut-on dire des points A, B et D ? Question : quelle est la conclusion ?
ÉCRAN : 2-a : b − d = 1 + √2 + i − 2i = 1 + √2 − i = c : B descend de 2 et tombe sur C. | 2-b : (√2 + 1)(b − a) = (√2 + 1)(1 + (1 − √2)i) = √2 + 1 − i = b − d : à toi de conclure.
QUESTION : 2023 N : (√2 + 1)(b − a) = b − d. Que peut-on conclure ? OPTIONS : ['A, B et D sont alignés', 'A, B et D ne sont pas alignés', 'B est le milieu de [AD]']

### Diapo 71 `nc_n1_alignes` — National 2023 N, exercice 2 : question 2-b corrigée, la droite
VOIX (fr) : Correction de la question deux b. On divise par b moins a, qui n'est pas nul : b moins d, sur b moins a, égale racine de deux plus un. Racine de deux plus un est un réel. Donc les vecteurs A B et D B sont colinéaires. Regarde la droite A B : elle passe par A, par B, et elle arrive jusqu'à D. Donc A, B et D sont alignés. C'est la phrase qu'on écrit à l'examen.
ÉCRAN : On divise par b − a ≠ 0 : (b − d)/(b − a) = √2 + 1 ∈ ℝ. | Donc AB⃗ et DB⃗ sont colinéaires : la droite (AB) passe par D. | A, B et D sont alignés.

### Diapo 72 `nc_enonce_2023n_p2` — National 2023 N : la suite de l’énoncé
VOIX (fr) : Même exercice du national deux mille vingt-trois : a égale racine de deux, plus i racine de deux, et c égale b barre. Voici la suite de l'énoncé. Trois a : vérifier que a fois c, égale deux b. b : en déduire que deux arguments de b, égale pi sur quatre. Maintenant, comprenons l'exercice, question par question.

### Diapo 73 `nc_n1_c` — National 2023 N, exercice 2 : questions 3-a et 3-b, les arguments
VOIX (fr) : Question trois a : vérifier que a fois c égale deux b. On développe a fois c : deux plus deux racine de deux, plus deux i, c'est deux b. Question trois b : en déduire deux arg b. Regarde la figure : A, B et C, chaque point avec son angle. L'argument de a vaut pi sur quatre. Et C est le symétrique de B : l'argument de c est moins l'argument de b. On passe aux arguments. Rappelle-toi : l'argument d'un produit est la somme des arguments. La suite, avec la rotation, c'est la question quatre du sujet. Question : combien vaut deux arg b ?
ÉCRAN : 3-a : ac = (√2 + i√2)(1 + √2 − i) = 2 + 2√2 + 2i = 2b ; c = b̄ et arg a ≡ π/4 [2π]. | arg(zz′) ≡ arg z + arg z′ [2π] ; arg z̄ ≡ −arg z [2π]. | 3-b, à toi : 2 arg b ≡ … [2π].
QUESTION : 2023 N : ac = 2b, c = b̄ et arg a ≡ π/4 [2π]. Alors 2 arg b ≡ OPTIONS : ['π/2 [2π]', 'π/4 [2π]', '0 [2π]']

### Diapo 74 `nc_enonce_2024n_p2` — National 2024 N : la suite de l’énoncé
VOIX (fr) : Même exercice du national deux mille vingt-quatre : b égale deux plus racine de trois, plus i. Voici la suite de l'énoncé. Deux b : en déduire une forme trigonométrique de b, puis vérifier que b puissance vingt-quatre, est un nombre réel. Maintenant, comprenons cette question.

### Diapo 75 `nc_n2` — National 2024 N, exercice 3 : question 2-b, la forme trigonométrique de b et b²⁴
VOIX (fr) : Question deux b du national deux mille vingt-quatre. D'abord, en déduire la forme trigonométrique de b : b égale b sur a, fois a. Les modules se multiplient : trois plus racine de trois, sur trois, fois racine de six, égale racine de six plus racine de deux. Les arguments s'additionnent : pi sur trois moins pi sur quatre, égale pi sur douze. Donc b égale racine de six plus racine de deux, facteur de cos pi sur douze, plus i sin pi sur douze. Regarde l'angle : pi sur douze, tout petit. Vingt-quatre fois pi sur douze, égale deux pi. Un tour complet : l'arc revient sur l'axe réel. Donc b puissance vingt-quatre, c'est le module puissance vingt-quatre. Un réel, encadré en jaune. Pas besoin de calculer ce grand nombre.
ÉCRAN : 2-b : b = (b/a) × a = ((3 + √3)/3)e^{iπ/3} × √6e^{−iπ/4} = (√6 + √2)(cos π/12 + i sin π/12). | 24 × π/12 = 2π : un tour complet. | b²⁴ = (√6 + √2)²⁴(cos 2π + i sin 2π) = (√6 + √2)²⁴, un réel. | Inutile de calculer (√6 + √2)²⁴ : c'est un réel.
## XI. Bilan et carte du chapitre

### Diapo 76 `nc_b1_bilan` — Ce qu'il faut retenir
VOIX (fr) : Faisons le bilan sur une seule fiche, bloc par bloc, et écris avec moi. Un : i carré égale moins un, et z égale a plus i b. Deux : le quotient. On multiplie en haut et en bas, par le conjugué du dénominateur. Trois : les affixes. L'affixe du vecteur AB, c'est z B moins z A. Le milieu, c'est z A plus z B, sur deux. Quatre : le conjugué, le symétrique par rapport à l'axe réel. z fois z barre égale a carré plus b carré. Cinq : le module, une distance. Racine de a carré plus b carré, sans le i. Six : l'argument et la forme trigonométrique. r facteur de cos teta plus i sin teta, avec r strictement positif. Sept : produit, quotient, Moivre. Les modules se multiplient, les arguments s'additionnent. Et à la puissance n, le module aussi. Huit : l'alignement. Le quotient c moins a, sur b moins a, est un réel. Voilà la fiche entière. La deuxième page est la tienne : ce qu'il te reste à retravailler.
ÉCRAN : 1. i² = −1 ; z = a + ib, avec a = Re(z) et b = Im(z) réels ; réel : b = 0 ; imaginaire pur : a = 0. ⚠ Jamais i = √(−1). | 2. Quotient (c + id ≠ 0) : on multiplie en haut et en bas par le conjugué du dénominateur ; (c + id)(c − id) = c² + d². ⚠ c² + d², pas c² − d². | 3. Affixes : z_{AB⃗} = z_B − z_A (arrivée moins départ) ; milieu de [AB] : z_I = (z_A + z_B)/2 ; ABCD parallélogramme ⇔ z_B − z_A = z_C − z_D. | 4. Conjugué : z̄ = a − ib, le symétrique de M par rapport à l'axe réel ; z·z̄ = a² + b² ; z réel ⇔ z̄ = z ; z ∈ iℝ ⇔ z̄ = −z. | 5. Module : |z| = √(a² + b²) = OM ; AB = |z_B − z_A| ; |zz′| = |z|·|z′|. ⚠ Pas de i dans la racine ; |z + z′| ≠ |z| + |z′|. | 6. Argument et forme trigonométrique : arg z ≡ θ [2π] ; z = r(cos θ + i sin θ), r = |z| > 0, cos θ = a/r, sin θ = b/r ; les signes donnent π − θ, π + θ, −θ. ⚠ 0 n'a pas d'argument. | 7. Produit, quotient, Moivre (z, z′ ≠ 0) : arg(zz′) ≡ arg z + arg z′ ; arg(z/z′) ≡ arg z − arg z′ ; arg z̄ ≡ −arg z [2π] ; [r(cos θ + i sin θ)]ⁿ = rⁿ(cos nθ + i sin nθ). ⚠ rⁿ, pas r. | 8. Géométrie : pour A ≠ B, A, B, C alignés ⇔ (c − a)/(b − a) ∈ ℝ ; (AB⃗, AC⃗) ≡ arg((c − a)/(b − a)) [2π] ; quotient imaginaire pur ⇔ (AB) ⊥ (AC) ; |z − z_A| = r : cercle de centre A et de rayon r ; |z − z_A| = |z − z_B| : médiatrice de [AB]. | Page 2, ta page : ce qu'il te reste à retravailler, d'après tes réponses du cours.

### Diapo 77 `nc_b2_carte` — La carte du chapitre et la suite
VOIX (fr) : Dessinons la carte du chapitre, en une seule image. Au centre : un point M, et ses deux écritures. a plus i b, et r facteur de cos teta plus i sin teta. Pour aller de la première à la deuxième : le module et l'argument. Pour revenir : cos et sin. Autour, les branches. Le calcul algébrique, avec i carré égale moins un. Le conjugué, le symétrique. Le module, la distance. L'argument, l'angle. Le produit et Moivre : les angles s'additionnent. Et la géométrie : milieu, distance, alignement. En pointillé, la partie deux. Une troisième écriture, plus courte : l'écriture exponentielle. L'équation du second degré, et la rotation. On les verra bientôt. Les branches entourées en rouge, on les reprendra ensemble. Question : pour multiplier deux complexes, quelle écriture est la plus rapide ?
ÉCRAN : Au centre : un point M et ses deux écritures, a + ib et r(cos θ + i sin θ). | De a + ib vers r(cos θ + i sin θ) : module et argument ; retour : cos et sin. | Les branches : calcul algébrique, conjugué, module, argument, produit et Moivre, géométrie. | Partie 2 (annoncée) : écriture exponentielle, équation du second degré, rotation.
QUESTION : Pour multiplier deux complexes, quelle écriture est la plus rapide ? OPTIONS : ['La forme algébrique : on développe toujours, en remplaçant i² par −1', 'La forme trigonométrique : modules multipliés, arguments additionnés', 'Aucune écriture : on place les points, puis on lit le produit sur la figure']
EXERCICE : Vrai ou faux ? OPTIONS : None

### Diapo 78 `nc_fermeture_cours` — Ce qu'il faut retenir, et comment réviser
VOIX (fr) : Nous arrivons à la fin du cours : Nombres complexes, la première partie. Que faut-il retenir ? Trois idées. Première : i au carré égale moins un, et z égale a plus i b. Deuxième : le module est racine de a carré plus b carré, et la distance AB est le module de z B moins z A. Troisième : la forme trigonométrique : z égale r fois cos teta plus i sin teta. Maintenant quelques conseils pour réviser. Relis ton cahier, et refais seul les exercices du national. Quand tu réponds, écris chaque étape, et chaque résultat avec sa justification, car chaque étape a ses points. Le jour de l'examen, partage ton temps, et commence par la question qui te paraît facile. La veille, dors bien. Écris ces conseils dans ton cahier. Tu as bien travaillé, bon courage !
ÉCRAN : Retenir : i² = −1 · |z| = √(a² + b²) · z = r(cos θ + i sin θ) | Réviser : relire le cahier, refaire les exercices du national | Rédiger : chaque étape, et sa justification (car…) | Jour J : gérer son temps · bien dormir la veille

## Questions de bloc (posées après la dernière diapo du bloc)
- après diapo 4 `nc_s1_b0` RETROUVER : Cahier fermé : quel est le carré de i ?
- après diapo 4 `nc_s1_b0` EXERCICE : (2i)² = ? OPTIONS : ['−4', '4', '2i']
- après diapo 7 `nc_s1_b1` RETROUVER : Cahier fermé : écris la forme algébrique d'un complexe z et nomme ses parties.
- après diapo 7 `nc_s1_b1` EXERCICE : Re(−2 + 7i) et Im(−2 + 7i) valent : OPTIONS : ['7 et −2', '−2 et 7', '−2 et 7i']
- après diapo 11 `nc_s1_b2` RETROUVER : Cahier fermé : que vaut i⁴, et comment calcule-t-on i²⁰²⁶ ?
- après diapo 11 `nc_s1_b2` EXERCICE : (1 + 2i)(3 − i) = ? OPTIONS : ['5 + 5i', '1 + 5i', '3 − 2i']
- après diapo 14 `nc_s1_b3` RETROUVER : Cahier fermé : que vaut (a + ib)(a − ib) ?
- après diapo 14 `nc_s1_b3` EXERCICE : (2 + i)/(1 − i) = ? OPTIONS : ['1/2 + (3/2)i', '2 + i', '3/2 + (1/2)i']
- après diapo 18 `nc_s2_b1` RETROUVER : Cahier fermé : écris l'affixe du vecteur AB⃗.
- après diapo 18 `nc_s2_b1` EXERCICE : Le point B(0 ; −3) a pour affixe : OPTIONS : ['−3', '−3i', '3i']
- après diapo 20 `nc_s2_b1b` RETROUVER : Cahier fermé : quand ABCD est-il un parallélogramme ? Écris-le avec les affixes.
- après diapo 20 `nc_s2_b1b` EXERCICE : Vrai ou faux ? OPTIONS : None
- après diapo 23 `nc_s2_b2` RETROUVER : Cahier fermé : écris le conjugué de z = a + ib, et quand z est réel.
- après diapo 23 `nc_s2_b2` EXERCICE : z = 1 + i : quel est le conjugué de z² ? OPTIONS : ['2i', '−2i', '2']
- après diapo 25 `nc_s2_b2b` RETROUVER : Cahier fermé : écris z + z̄ et z − z̄.
- après diapo 25 `nc_s2_b2b` EXERCICE : z = 3 − 4i : combien vaut z + z̄ ? OPTIONS : ['−8i', '6', '6 − 8i']
- après diapo 28 `nc_s2_b3` RETROUVER : Cahier fermé : écris le module de z = a + ib.
- après diapo 28 `nc_s2_b3` EXERCICE : |−3 + 4i| = ? OPTIONS : ['5', '1', '7']
- après diapo 33 `nc_s2_b3b` RETROUVER : Cahier fermé : écris la distance AB avec les affixes.
- après diapo 33 `nc_s2_b3b` EXERCICE : Vrai ou faux ? OPTIONS : None
- après diapo 35 `nc_s2_b3c` RETROUVER : Cahier fermé : quel est l'ensemble des points M(z) tels que |z − z_A| = r (r > 0) ?
- après diapo 35 `nc_s2_b3c` EXERCICE : L'ensemble des points M(z) tels que |z − 1 + i| = 2 est : OPTIONS : ['le cercle de centre A(−1 + i) et de rayon 2', 'le cercle de centre A(1 − i) et de rayon 2', 'la médiatrice de [OA], avec A(1 − i)']
- après diapo 39 `nc_s3_b1` RETROUVER : Cahier fermé : pourquoi écrit-on [2π] après un argument ?
- après diapo 39 `nc_s3_b1` EXERCICE : arg z ≡ π/4 [2π]. Lequel est aussi un argument de z ? OPTIONS : ['9π/4', '5π/4', 'π/2']
- après diapo 41 `nc_s3_b1b` RETROUVER : Cahier fermé : écris cos θ et sin θ avec a, b et |z|.
- après diapo 41 `nc_s3_b1b` EXERCICE : Quel angle a pour cosinus 1/2 et pour sinus √3/2 ? OPTIONS : ['π/6', 'π/3', 'π/4']
- après diapo 44 `nc_s3_b2` RETROUVER : Cahier fermé : écris la forme trigonométrique de z.
- après diapo 44 `nc_s3_b2` EXERCICE : Écris 1 + i sous forme trigonométrique. OPTIONS : ['√2(cos π/4 + i sin π/4)', '2(cos π/4 + i sin π/4)', '√2(cos π/2 + i sin π/2)']
- après diapo 46 `nc_s3_b2b` RETROUVER : Cahier fermé : a < 0 et b < 0, l'angle du tableau est α : quel argument ?
- après diapo 46 `nc_s3_b2b` EXERCICE : Vrai ou faux ? OPTIONS : None
- après diapo 50 `nc_s3_b3` RETROUVER : Cahier fermé : comment revient-on de r(cos θ + i sin θ) à a + ib ?
- après diapo 50 `nc_s3_b3` EXERCICE : Écris √2(cos 3π/4 + i sin 3π/4) sous forme algébrique. OPTIONS : ['1 + i', '−1 + i', '−1 − i']
- après diapo 52 `nc_s3_b3b` RETROUVER : Cahier fermé : écris l'argument d'un produit.
- après diapo 52 `nc_s3_b3b` EXERCICE : i(1 + 2i) = ? OPTIONS : ['2 − i', '−2 + i', '−1 + 2i']
- après diapo 56 `nc_s4_b1` RETROUVER : Cahier fermé : écris l'argument d'un quotient.
- après diapo 56 `nc_s4_b1` EXERCICE : z = 4(cos π/2 + i sin π/2) et z′ = 2(cos π/6 + i sin π/6). Alors z/z′ = OPTIONS : ['2(cos π/3 + i sin π/3)', '2(cos 2π/3 + i sin 2π/3)', '8(cos π/3 + i sin π/3)']
- après diapo 58 `nc_s4_b1b` RETROUVER : Cahier fermé : écris la formule de Moivre.
- après diapo 58 `nc_s4_b1b` EXERCICE : Vrai ou faux ? OPTIONS : None
- après diapo 65 `nc_s4_b2` RETROUVER : Cahier fermé : quand trois points A, B, C sont-ils alignés ?
- après diapo 65 `nc_s4_b2` EXERCICE : (cos π/6 + i sin π/6)⁶ = ? OPTIONS : ['1', '−1', 'i']
- après diapo 67 `nc_s4_b2b` RETROUVER : Cahier fermé : écris une mesure de l'angle (AB⃗, AC⃗) avec les affixes a, b, c.
- après diapo 67 `nc_s4_b2b` EXERCICE : A(1), B(2 + i), C(i) : que vaut (c − a)/(b − a), et que peut-on dire ? OPTIONS : ['−1 : A, B et C sont alignés', '1 + i : (AB) et (AC) sont perpendiculaires', 'i : (AB) et (AC) sont perpendiculaires']
- après diapo 73 `nc_s4_b3` RETROUVER : Cahier fermé : (b − d)/(b − a) est un réel : que peut-on dire de A, B et D ?
- après diapo 73 `nc_s4_b3` EXERCICE : (c − a)/(b − a) = −3 : les points A, B, C sont : OPTIONS : ['alignés', 'non alignés', 'on ne peut pas savoir']
- après diapo 77 `nc_s4_b4` RETROUVER : Cahier fermé : comment écrit-on un quotient sous forme algébrique ?
- après diapo 77 `nc_s4_b4` EXERCICE : Même b : b¹² = ? OPTIONS : ['(√6 + √2)¹²', '−(√6 + √2)¹²', '(√6 + √2)¹² i']
