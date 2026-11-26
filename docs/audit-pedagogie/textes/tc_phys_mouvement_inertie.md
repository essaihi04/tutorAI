# tc_phys_mouvement_inertie — Le mouvement et le principe d’inertie

## Ouverture et prérequis — forces, vecteurs, graphiques

### Diapo 1 `mi_ouverture_cours` — Le mouvement et le principe d’inertie
VOIX (fr) : Bienvenue dans un nouveau cours : le mouvement et le principe d’inertie. Nous allons apprendre à décrire le mouvement d’un corps : le référentiel, le repère, la trajectoire et la vitesse. Puis nous verrons le principe d’inertie : pourquoi un corps continue seul en ligne droite. C’est la base de la mécanique, que tu retrouveras jusqu’au bac. Comment allons-nous travailler ? Tu écoutes bien, tu réponds aux questions au tableau, et quand le cours s’arrête, tu écris dans ton cahier. Allons-y !
ÉCRAN : On apprend : référentiel, trajectoire, vitesse, inertie | Pourquoi : la base de la mécanique, jusqu’au bac | Écouter · répondre au tableau · écrire dans le cahier

### Diapo 2 `mi_r1_force` — Rappel : une force
VOIX (fr) : Avant de commencer, il faut savoir ce qu’est une force. Cette personne pousse une caisse : c’est une action mécanique, on l’appelle une force. On la représente par un vecteur, qui a quatre caractéristiques. Le point d’application : le point A, où la main touche la caisse. La droite d’action : ici horizontale. Le sens : vers la droite. L’intensité, en newtons : F égale deux cents newtons. Pour dessiner le vecteur, on choisit une échelle : un carreau pour cent newtons. Deux cents newtons, ce sont deux carreaux.
ÉCRAN : Point · droite · sens · intensité (N) | 1 carreau ↔ 100 N

### Diapo 3 `mi_r2_poids` — Rappel : le poids P = m·g
VOIX (fr) : Une force très importante : le poids. Cette boule a une masse m égale deux kilogrammes. La Terre l’attire sans la toucher : c’est une force à distance ; la main qui pousse, c’était une force de contact. Le point d’application du poids est G, le centre de la boule. Sa direction : la verticale. Son sens : toujours vers le bas. Son intensité : P égale m fois g, avec g égale dix newtons par kilogramme. Donc P égale deux fois dix, vingt newtons. Avec l’échelle un carreau pour dix newtons : deux carreaux.
ÉCRAN : P = m·g   (g = 10 N/kg) | P = 2 × 10 = 20 N
QUESTION : Une valise a une masse m = 5 kg (g = 10 N/kg). Son poids vaut… OPTIONS : ['5 N', '50 N', '0,5 N']

### Diapo 4 `mi_r3_reaction` — Rappel : poids et réaction
VOIX (fr) : Posons un livre de un kilogramme sur une table. Sur lui, le poids P, vers le bas. Pourquoi ne tombe-t-il pas ? Parce que la table le pousse vers le haut : c’est la réaction R. Sans frottement, R est perpendiculaire à la table. P et R ont la même droite d’action et des sens contraires. On dit que P et R se compensent : vecteur P plus vecteur R égale vecteur nul. Ils ont donc la même intensité : P égale R égale dix newtons.
ÉCRAN : P⃗ + R⃗ = 0⃗ | P = R = 10 N

### Diapo 5 `mi_r3b_compense` — Deux forces qui se compensent
VOIX (fr) : Voyons la même idée autrement. Cet anneau est tiré par deux dynamomètres. L’un tire vers la gauche : la force F un. L’autre tire vers la droite : la force F deux. Et l’anneau ne bouge pas. Pourquoi ? F un et F deux ont la même droite d’action et des sens contraires. Chaque dynamomètre indique cinq newtons : même intensité. Ces deux forces se compensent : vecteur F un plus vecteur F deux égale vecteur nul. Je répète : deux forces se compensent quand elles ont la même droite d’action, des sens contraires et la même intensité.
ÉCRAN : F⃗₁ + F⃗₂ = 0⃗
QUESTION : Deux forces de même intensité et de sens contraires, mais sur deux droites parallèles différentes, se compensent. OPTIONS : ['Vrai', 'Faux']

### Diapo 6 `mi_r4_vecteur` — Rappel : les coordonnées d’un vecteur
VOIX (fr) : Un rappel de mathématiques : le vecteur et ses coordonnées. Voici un repère : un point O, et deux vecteurs unitaires, i sur l’axe horizontal et j sur l’axe vertical. Chaque carreau vaut un mètre. Voici le point H. Pour trouver ses coordonnées, on part de O et on compte les carreaux sur x : un, deux, trois ; puis sur y : un, deux. H a pour coordonnées trois et deux. Le vecteur OH s’écrit : OH égale trois i plus deux j. Pour aller de O à H, on fait trois carreaux vers la droite et deux vers le haut.
ÉCRAN : H(3 ; 2) | OH⃗ = 3·i⃗ + 2·j⃗

### Diapo 7 `mi_r5_graphique` — Rappel : lire un graphique
VOIX (fr) : Comment lire un graphique ? D’abord, on lit les axes : l’axe horizontal porte t en secondes, l’axe vertical porte x en mètres. Voici la courbe de x en fonction de t. Que vaut x quand t égale deux secondes ? On monte verticalement depuis t égale deux jusqu’à la courbe, puis on va horizontalement jusqu’à l’axe vertical. On lit : x égale cinq mètres.
ÉCRAN : à t = 2 s : x = 5 m

### Diapo 8 `mi_r6_droite` — Rappel : la droite x = a·t + b
VOIX (fr) : Cette courbe est une droite. Toute droite s’écrit : x égale a t plus b. b est la valeur de x quand t égale zéro : ici b égale un mètre. a est la pente. Pour la calculer, on prend deux points de la droite : le point t égale un, x égale trois, et le point t égale trois, x égale sept. Delta x égale sept moins trois, soit quatre mètres. Delta t égale trois moins un, soit deux secondes. a égale delta x sur delta t, quatre sur deux, a égale deux mètres par seconde. La droite : x égale deux t plus un.
ÉCRAN : x = a·t + b | a = Δx/Δt = 4/2 = 2 m/s
QUESTION : Une droite passe par les points (0 ; 2) et (2 ; 8) (t en s, x en m). Son équation est… OPTIONS : ['x = 2·t + 3', 'x = 3·t + 2', 'x = 8·t + 2']
## Partie 1 — Décrire un mouvement : relativité, repères, trajectoire

### Diapo 9 `mi_m1_bus` — Au repos ou en mouvement ?
VOIX (fr) : Commençons la première partie : le mouvement. Regarde ce bus. A est assis à l’avant. B marche vers l’arrière pour chercher une place. C est debout au bord de la route. Le bus roule lentement, et B se déplace dans le bus. Question : A est-il en mouvement ou au repos ? Par rapport au bus, A reste toujours à la même place. Mais par rapport à C, A s’éloigne avec le bus. B change de place par rapport au bus et par rapport à C. Et C, par rapport à la route, reste toujours au même endroit.
ÉCRAN : A, B, C : au repos ou en mouvement ?

### Diapo 10 `mi_m2_tableau` — Le mouvement est relatif
VOIX (fr) : Rassemblons cela dans un tableau. Première ligne, par rapport à A : B en mouvement, C en mouvement. Deuxième ligne, par rapport à B : A en mouvement, C en mouvement. Troisième ligne, par rapport au bus : A au repos, B en mouvement, C en mouvement. Quatrième ligne, par rapport à la route : A en mouvement, B en mouvement, C au repos. Tu vois ? La même personne A est tantôt au repos, tantôt en mouvement. Donc le mouvement est relatif : il dépend du corps auquel on compare.
ÉCRAN : Le mouvement est relatif

### Diapo 11 `mi_m3_referentiel` — Le référentiel
VOIX (fr) : Le corps auquel on compare s’appelle le référentiel. Le référentiel est un solide indéformable, par rapport auquel on étudie le mouvement. Par exemple le référentiel terrestre : la Terre, et tout ce qui y est fixé, comme la maison et l’arbre. Il y a aussi le référentiel lié au bus. Regarde le conducteur : au repos par rapport au bus, en mouvement par rapport au référentiel terrestre. Donc, avant d’étudier un mouvement, il faut choisir le référentiel.
ÉCRAN : Référentiel : solide de référence | Ex. : référentiel terrestre
QUESTION : Dans un train qui roule, un voyageur est assis. Par rapport au train, il est… OPTIONS : ['en mouvement', 'au repos', 'en mouvement, puis au repos']

### Diapo 12 `mi_m4_axe` — Le repère d’espace : un axe
VOIX (fr) : Après avoir choisi le référentiel, on lui lie un repère d’espace. Si le mouvement est rectiligne, comme cette voiture sur une route droite, un axe suffit. On choisit un point O et un vecteur unitaire i. La position de la voiture est le point H. Le vecteur position : OH égale x fois i. x est l’abscisse de H : ici x égale trois mètres. Si le point est à gauche de O, l’abscisse est négative : ici x égale moins deux mètres.
ÉCRAN : OH⃗ = x·i⃗  (x : abscisse)

### Diapo 13 `mi_m5_plan` — Le repère du plan
VOIX (fr) : Si le mouvement se fait dans un plan, comme le ballon sur le terrain, il faut deux axes : le repère O, i, j. La position H du ballon a deux coordonnées : x égale quatre mètres et y égale deux mètres. Le vecteur position : OH égale x i plus y j, soit quatre i plus deux j. C’est la même idée que le vecteur du rappel de mathématiques.
ÉCRAN : OH⃗ = x·i⃗ + y·j⃗ = 4·i⃗ + 2·j⃗

### Diapo 14 `mi_m6_espace` — Le repère de l’espace
VOIX (fr) : Si le mouvement se fait dans l’espace, comme le ballon en l’air, il faut trois axes : le repère O, i, j, k. Le point H a trois coordonnées, x, y et z : ici trois, deux et deux. Le vecteur position : OH égale x i plus y j plus z k. Donc : mouvement rectiligne, un axe ; mouvement plan, deux axes ; mouvement dans l’espace, trois axes.
ÉCRAN : OH⃗ = x·i⃗ + y·j⃗ + z·k⃗ | 1 axe · 2 axes · 3 axes
QUESTION : Un oiseau vole dans l’air. Pour repérer sa position, il faut… OPTIONS : ['un axe (O, i⃗)', 'deux axes (O, i⃗, j⃗)', 'trois axes (O, i⃗, j⃗, k⃗)']

### Diapo 15 `mi_m7_temps` — Le repère de temps
VOIX (fr) : Pour décrire un mouvement, il faut dire où, mais aussi quand. Il faut un repère de temps : un chronomètre et une origine des dates. C’est moi qui choisis t égale zéro : ici, quand la voiture passe en O. Après une seconde, la voiture est à x égale deux mètres. Après deux secondes, à x égale quatre mètres. Après trois secondes, à x égale six mètres. Chaque position a sa date.
ÉCRAN : Origine des dates : t = 0 (choisie)

### Diapo 16 `mi_m8_trajectoire` — La trajectoire
VOIX (fr) : Maintenant la trajectoire. Regarde ce ballon frappé. Régulièrement, on marque sa position par un point. Voici les positions successives du ballon. Si on les relie, on obtient une ligne : c’est la trajectoire. La trajectoire est l’ensemble des positions successives occupées par un point du corps.
ÉCRAN : Trajectoire : positions successives

### Diapo 17 `mi_m9_formes` — Trois formes de trajectoire
VOIX (fr) : La trajectoire a plusieurs formes. Si c’est une droite, comme la voiture sur une route droite, on dit trajectoire rectiligne. Si c’est un cercle, comme la valve d’une roue qui tourne, on dit trajectoire circulaire. Et si c’est une ligne courbe, comme le ballon, on dit trajectoire curviligne.
ÉCRAN : rectiligne · circulaire · curviligne

### Diapo 18 `mi_m10_valve` — La valve vue par le cycliste et par le piéton
VOIX (fr) : Regardons la valve d’une roue de vélo, depuis deux endroits. D’abord le cycliste, sur le vélo. Pour lui, la valve tourne en cercle : trajectoire circulaire. Ensuite le piéton, debout au bord de la route. Pour lui, la valve dessine autre chose. Regarde bien. Pour le piéton, la trajectoire n’est pas un cercle : elle monte et descend, comme des arches. Donc la trajectoire dépend, elle aussi, du référentiel.
ÉCRAN : La trajectoire dépend du référentiel
QUESTION : La trajectoire de la valve d’une roue de vélo qui roule est un cercle… OPTIONS : ['pour tout observateur', 'pour le cycliste seulement', 'pour le piéton seulement']
OBSERVATION : Pour le piéton, la trajectoire de la valve est-elle encore un cercle ?
## Partie 1 — La vitesse : moyenne, enregistrement, instantanée

### Diapo 19 `mi_v1_moyenne` — La vitesse moyenne
VOIX (fr) : Maintenant la vitesse. Cette voiture roule sur une route droite. Regarde : elle parcourt une distance d égale trois cents mètres, en une durée delta t égale soixante secondes. La vitesse moyenne est la distance divisée par la durée : v m égale d sur delta t. Soit trois cents sur soixante : v m égale cinq mètres par seconde. En moyenne, chaque seconde, la voiture parcourt cinq mètres. Si la trajectoire est curviligne, d est la longueur de l’arc parcouru.
ÉCRAN : v_m = d/Δt   (m/s) | v_m = 300/60 = 5 m/s

### Diapo 20 `mi_v2_unites` — Convertir m/s et km/h
VOIX (fr) : Une question : un mètre par seconde, combien de kilomètres par heure ? En une seconde, on parcourt un mètre. Dans une heure, il y a trois mille six cents secondes : on parcourt trois mille six cents mètres, soit trois virgule six kilomètres. Donc un mètre par seconde égale trois virgule six kilomètres par heure. La méthode : des mètres par seconde aux kilomètres par heure, on multiplie par trois virgule six ; des kilomètres par heure aux mètres par seconde, on divise par trois virgule six. Par exemple, cinq mètres par seconde, c’est cinq fois trois virgule six, dix-huit kilomètres par heure.
ÉCRAN : 1 m/s = 3,6 km/h | m/s → km/h : × 3,6 · km/h → m/s : ÷ 3,6

### Diapo 21 `mi_v3_eleve` — À toi : la vitesse moyenne
VOIX (fr) : À toi maintenant. Une voiture parcourt mille deux cents mètres en soixante secondes. Calcule sa vitesse moyenne en mètres par seconde, puis en kilomètres par heure. Utilise la méthode : la relation, l’application numérique, et le résultat avec son unité.
ÉCRAN : d = 1 200 m ; Δt = 60 s
QUESTION : Une voiture parcourt 1 200 m en 60 s. Sa vitesse moyenne est… OPTIONS : ['20 m/s, soit 72 km/h', '20 m/s, soit 5,6 km/h', '72 m/s, soit 20 km/h']

### Diapo 22 `mi_e1_materiel` — La table à coussin d’air
VOIX (fr) : Pour étudier un mouvement avec précision, on utilise la table à coussin d’air : une table horizontale. Dessus, l’autoporteur : un disque qui glisse. La soufflerie envoie de l’air sous l’autoporteur : c’est le coussin d’air, et grâce à lui il n’y a pas de frottement. Au centre de l’autoporteur, il y a l’éclateur. Le générateur d’impulsions donne une étincelle toutes les tau, ici tau égale vingt millisecondes. Chaque étincelle marque un point sur la feuille d’enregistrement.
ÉCRAN : Coussin d’air : pas de frottement | Une étincelle toutes les τ = 20 ms

### Diapo 23 `mi_e2_enregistrement` — L’enregistrement
VOIX (fr) : Lançons l’autoporteur sur la table. Regarde : toutes les vingt millisecondes, une étincelle jaillit et marque un point sur la feuille. Voici les points : M zéro, M un, M deux, jusqu’à M sept. Entre deux points voisins, toujours la même durée : tau égale vingt millisecondes.
ÉCRAN : τ = 20 ms entre deux points voisins

### Diapo 24 `mi_e3_lire` — Lire un enregistrement
VOIX (fr) : Comment lire cet enregistrement ? On pose la règle. On mesure la distance entre deux points voisins : un, deux, trois, quatre, cinq, six, sept. Chaque intervalle vaut deux centimètres : les distances sont égales. Et la durée entre M un et M six ? On compte les intervalles : un, deux, trois, quatre, cinq. Cinq intervalles, donc delta t égale cinq tau, soit cinq fois vingt, cent millisecondes.
ÉCRAN : Δt = n·τ (n : nombre d’intervalles)
QUESTION : Sur le même enregistrement (τ = 20 ms), la durée entre M₂ et M₇ est… OPTIONS : ['100 ms', '140 ms', '120 ms']

### Diapo 25 `mi_e4_instant` — La vitesse instantanée
VOIX (fr) : Maintenant la vitesse instantanée : la vitesse à un instant. Par exemple en M trois. On prend les deux points voisins : M deux et M quatre. On mesure M deux M quatre : quatre centimètres, soit zéro virgule zéro quatre mètre. La durée entre eux : deux intervalles, deux tau, quarante millisecondes. La relation : v i égale M i moins un M i plus un, sur deux tau. Donc v trois égale zéro virgule zéro quatre sur zéro virgule zéro quatre : un mètre par seconde.
ÉCRAN : v_i = Mᵢ₋₁Mᵢ₊₁/(2τ) | v₃ = 0,04/0,04 = 1 m/s

### Diapo 26 `mi_e5_comparer` — Comparer les vitesses
VOIX (fr) : Recommençons en M cinq : M quatre M six vaut aussi quatre centimètres, donc v cinq égale un mètre par seconde. Et la vitesse moyenne de M un à M six : dix centimètres en cinq tau, soit zéro virgule dix sur zéro virgule dix : un mètre par seconde. v trois, v cinq et v m sont égales : la vitesse est constante.
ÉCRAN : v₃ = v₅ = v_m = 1 m/s

### Diapo 27 `mi_e6_eleve` — À toi : une vitesse instantanée
VOIX (fr) : À toi. Un autre enregistrement : tau égale vingt millisecondes, et deux points voisins sont à trois centimètres. Calcule la vitesse instantanée en M quatre.
ÉCRAN : τ = 20 ms ; MᵢMᵢ₊₁ = 3 cm
QUESTION : Points espacés de 3 cm, τ = 20 ms. La vitesse instantanée v₄ vaut… OPTIONS : ['0,75 m/s', '1,5 m/s', '3 m/s']
## Partie 1 — Le vecteur vitesse et le mouvement rectiligne uniforme

### Diapo 28 `mi_e7_vecteur` — Le vecteur vitesse
VOIX (fr) : La vitesse a, elle aussi, un vecteur : le vecteur vitesse. Regarde cette trajectoire courbe, et le point M trois. Le vecteur vitesse v trois a quatre caractéristiques. Son origine : le point M trois. Sa direction : la tangente à la trajectoire en M trois. Son sens : le sens du mouvement. Et sa valeur : v trois. Voilà comment on dessine le vecteur v trois, en vert.
ÉCRAN : Origine M₃ · tangente · sens du mouvement · v₃

### Diapo 29 `mi_e8_echelle` — Méthode : représenter v⃗ à l’échelle
VOIX (fr) : Comment dessiner le vecteur vitesse à l’échelle ? Voici la méthode. Revenons à l’enregistrement : v trois égale un mètre par seconde. D’abord, on choisit l’échelle : un centimètre pour zéro virgule cinq mètre par seconde. Ensuite, on calcule la longueur : un sur zéro virgule cinq, deux centimètres. On compte : un, deux. Enfin, on trace la flèche depuis M trois, le long de la trajectoire, dans le sens du mouvement, longue de deux centimètres.
ÉCRAN : 1 cm ↔ 0,5 m/s | ℓ = 1/0,5 = 2 cm

### Diapo 30 `mi_e9_eleve` — À toi : le vecteur v⃗₄
VOIX (fr) : À toi : v quatre égale un virgule cinq mètre par seconde, avec la même échelle, un centimètre pour zéro virgule cinq mètre par seconde. Quelle doit être la longueur de la flèche ?
ÉCRAN : v₄ = 1,5 m/s ; 1 cm ↔ 0,5 m/s
QUESTION : Échelle 1 cm ↔ 0,5 m/s. Le vecteur v⃗₄ (v₄ = 1,5 m/s) mesure… OPTIONS : ['1,5 cm', '3 cm', '0,75 cm']

### Diapo 31 `mi_u1_tableau` — Le mouvement rectiligne uniforme : le tableau
VOIX (fr) : Maintenant le mouvement rectiligne uniforme : une trajectoire rectiligne et une vitesse constante, comme notre enregistrement, avec tau égale vingt millisecondes et deux centimètres entre deux points. On choisit M zéro comme origine des abscisses : x égale zéro. Et M deux comme origine des dates : t égale zéro. Chaque point nous donne sa date et son abscisse. M zéro : t égale moins quarante millisecondes, x égale zéro. M un : moins vingt, et deux centimètres. M deux : zéro, et quatre centimètres. M trois : vingt, et six centimètres. Et ainsi de suite jusqu’à M sept : cent millisecondes et quatorze centimètres. Voilà le tableau de x et de t, produit par l’animation.
ÉCRAN : MRU : trajectoire rectiligne, vitesse constante | M₀ : x = 0 · M₂ : t = 0

### Diapo 32 `mi_u2_courbe` — La courbe x en fonction de t
VOIX (fr) : Traçons la courbe de x en fonction de t. L’axe horizontal : t en millisecondes. L’axe vertical : x en centimètres. Chaque colonne du tableau devient un point : le premier, le deuxième, le troisième, et ainsi de suite jusqu’au dernier. Regarde : tous les points sont sur la même droite. La courbe x en fonction de t de ce mouvement est une droite.
ÉCRAN : MRU : x = f(t) est une droite

### Diapo 33 `mi_u3_pente` — La pente est la vitesse
VOIX (fr) : Quelle est l’équation de cette droite ? x égale a t plus b. b, c’est x quand t égale zéro : quatre centimètres. a, c’est la pente. On prend deux points : t égale zéro, x égale quatre, et t égale cent, x égale quatorze. Delta x égale quatorze moins quatre, dix centimètres, soit zéro virgule dix mètre. Delta t égale cent millisecondes, soit zéro virgule dix seconde. a égale zéro virgule dix sur zéro virgule dix : un mètre par seconde. Tu vois ? a est exactement la vitesse v que nous avons calculée. La pente est égale à la vitesse.
ÉCRAN : b = x₀ = 4 cm | a = Δx/Δt = 0,10/0,10 = 1 m/s = v
QUESTION : Pour un mouvement rectiligne uniforme, la pente de la droite x = f(t) est égale… OPTIONS : ['à la vitesse v', 'à l’abscisse x₀', 'à la durée τ']

### Diapo 34 `mi_u4_equation` — L’équation horaire
VOIX (fr) : Pour un mouvement rectiligne uniforme, on écrit donc l’équation horaire : x de t égale v fois t plus x zéro. x zéro est l’abscisse à t égale zéro : ici zéro virgule zéro quatre mètre. v est la vitesse : un mètre par seconde. Donc x de t égale un fois t, plus zéro virgule zéro quatre, avec x en mètres et t en secondes.
ÉCRAN : x(t) = v·t + x₀ | x(t) = 1·t + 0,04 (m, s)

### Diapo 35 `mi_u5_signe` — Le signe de la vitesse
VOIX (fr) : Attention au signe. Si l’axe est dans le sens du mouvement, v x égale plus v : plus un mètre par seconde. Mais si on retourne l’axe, contre le sens du mouvement, x diminue avec le temps, et v x égale moins v : moins un mètre par seconde. Donc l’équation horaire : x de t égale v x fois t plus x zéro, et v x est positive ou négative selon l’axe.
ÉCRAN : x(t) = v_x·t + x₀ ; v_x = ± v

### Diapo 36 `mi_u6_eleve` — À toi : l’équation horaire
VOIX (fr) : À toi, avec l’application du livre. Tau égale cinquante millisecondes, et deux centimètres entre deux points. M zéro est l’origine des abscisses, et M deux l’origine des dates. Écris l’équation horaire x de t.
ÉCRAN : τ = 50 ms ; 2 cm ; M₀ : x = 0 ; M₂ : t = 0
QUESTION : τ = 50 ms, points espacés de 2 cm, M₀ origine des abscisses, M₂ origine des dates. L’équation horaire est… OPTIONS : ['x(t) = 0,4·t + 0,04', 'x(t) = 0,04·t + 0,4', 'x(t) = 2,5·t + 0,04']
## Partie 1 — Le mouvement circulaire uniforme

### Diapo 37 `mi_c1_circulaire` — Le mouvement circulaire uniforme
VOIX (fr) : Maintenant, on attache l’autoporteur par un fil à un point O, et on le lance. Regarde : il tourne. Ses points sont sur un cercle : trajectoire circulaire, et le rayon R égale dix centimètres. On mesure les arcs entre deux points voisins. On compte : un, deux, trois, et ainsi de suite. Ils valent tous deux centimètres, pendant la même durée tau. Donc la vitesse est constante. C’est le mouvement circulaire uniforme : trajectoire circulaire et vitesse constante.
ÉCRAN : MCU : trajectoire circulaire, vitesse constante

### Diapo 38 `mi_c2_omega` — La vitesse angulaire ω
VOIX (fr) : Dans le mouvement circulaire, on utilise aussi la vitesse angulaire. Quand M tourne, le rayon OM tourne d’un angle, delta teta, en radians. La vitesse angulaire oméga, c’est l’angle divisé par la durée. On peut la calculer : oméga égale v sur R. Ici v égale un mètre par seconde, et R égale zéro virgule dix mètre : oméga égale dix radians par seconde.
ÉCRAN : ω = v/R   (rad/s) | ω = 1/0,10 = 10 rad/s

### Diapo 39 `mi_c3_periode` — La période et la fréquence
VOIX (fr) : Combien de temps dure un tour complet ? C’est la période T. Suivons l’autoporteur jusqu’à ce qu’il fasse un tour. La relation : T égale deux pi sur oméga. Et la fréquence f : le nombre de tours en une seconde. f égale un sur T, et son unité est le hertz.
ÉCRAN : T = 2π/ω   (s) | f = 1/T   (Hz)
QUESTION : Dans un mouvement circulaire uniforme, la période T est… OPTIONS : ['le nombre de tours par seconde', 'la durée d’un tour', 'la vitesse angulaire']

### Diapo 40 `mi_c4_methode` — Méthode : v, ω, T et f
VOIX (fr) : Voici la méthode complète, avec l’application du livre : tau égale vingt millisecondes, arcs de deux centimètres, R égale dix centimètres. Premièrement, v : deux centimètres sur vingt millisecondes, zéro virgule zéro deux sur zéro virgule zéro deux, un mètre par seconde. Deuxièmement, oméga égale v sur R : un sur zéro virgule dix, dix radians par seconde. Troisièmement, T égale deux pi sur oméga : deux pi sur dix, environ zéro virgule soixante-trois seconde. Quatrièmement, f égale un sur T : environ un virgule six hertz.
ÉCRAN : v → ω = v/R → T = 2π/ω → f = 1/T

### Diapo 41 `mi_c5_eleve` — À toi : ω et T
VOIX (fr) : À toi : arcs de trois centimètres, tau égale vingt millisecondes, et R égale trente centimètres. Calcule v, oméga, T et f.
ÉCRAN : arc = 3 cm ; τ = 20 ms ; R = 30 cm
QUESTION : Arcs de 3 cm, τ = 20 ms, R = 30 cm. ω et T valent… OPTIONS : ['ω = 5 rad/s ; T ≈ 1,26 s', 'ω = 0,05 rad/s ; T ≈ 126 s', 'ω = 5 rad/s ; T ≈ 0,8 s']
## Partie 2 — Le centre d’inertie

### Diapo 42 `mi_i1_curling` — Le palet de curling
VOIX (fr) : Deuxième partie : le principe d’inertie. Regarde ce palet de curling. Le joueur le lance sur la glace, et il glisse tout seul. Regarde ses positions toutes les demi-secondes : toujours la même distance, et en ligne droite. Sur lui, deux forces : le poids P et la réaction R de la glace, qui se compensent. Alors pourquoi continue-t-il d’avancer, alors que rien ne le pousse ? C’est la question de cette partie.
ÉCRAN : P⃗ + R⃗ = 0⃗, et pourtant il avance

### Diapo 43 `mi_i2_rotation` — L’autoporteur lancé en tournant
VOIX (fr) : Revenons à la table à coussin d’air. Cette fois, l’autoporteur a deux éclateurs : A au centre, et B au bord. On le lance en le faisant tourner sur lui-même. Regarde les traces de A et de B. Regarde bien. A donne des points alignés, régulièrement espacés : un mouvement rectiligne uniforme. B donne des boucles : ce n’est pas un mouvement rectiligne uniforme.
ÉCRAN : A : droite à pas égaux · B : boucles
OBSERVATION : Quelle trace donne une droite à pas égaux ?

### Diapo 44 `mi_i3_axes` — Le centre d’inertie G
VOIX (fr) : Pourquoi A est-il spécial ? Refaisons l’expérience sur deux faces de l’autoporteur : il a des axes de symétrie. L’axe delta un, puis l’axe delta deux. Ils se coupent en un seul point : G. C’est le seul point qui a toujours un mouvement rectiligne uniforme, quelle que soit la façon de lancer l’autoporteur. Ce point s’appelle le centre d’inertie G.
ÉCRAN : G : le seul point toujours en MRU

### Diapo 45 `mi_i4_symetrie` — Où est G ?
VOIX (fr) : Et où est G pour d’autres corps ? Si le corps est homogène, G est à l’intersection de ses éléments de symétrie. La sphère : G au centre. Le cylindre : G au milieu de son axe. Le disque : G au centre. Et la barre : G au milieu.
ÉCRAN : Homogène : G à l’intersection des éléments de symétrie
QUESTION : Un autoporteur est lancé en tournant sur la table horizontale. Le point toujours en mouvement rectiligne uniforme est… OPTIONS : ['l’éclateur B, au bord', 'le centre d’inertie G', 'aucun point']
## Partie 2 — Le principe d’inertie

### Diapo 46 `mi_i5_translation` — L’autoporteur lancé sans tourner
VOIX (fr) : Maintenant, on lance l’autoporteur sans le faire tourner. Regarde : A au centre, qui est à la place de G, et B au bord. Tous ont un mouvement rectiligne uniforme : des points sur des droites, régulièrement espacés.
ÉCRAN : Sans rotation : A, B et G en MRU

### Diapo 47 `mi_i6_forces` — Les forces sur l’autoporteur
VOIX (fr) : Pourquoi G garde-t-il un mouvement rectiligne uniforme ? Étudions les forces. Le système : l’autoporteur. Sur lui, le poids P, en G, vers le bas. Et la réaction R de la table, vers le haut, perpendiculaire car il n’y a pas de frottement. P et R ont la même droite, des sens contraires et la même intensité : elles se compensent. Vecteur P plus vecteur R égale vecteur nul. On dit que l’autoporteur est pseudo-isolé.
ÉCRAN : P⃗ + R⃗ = 0⃗ | Système pseudo-isolé

### Diapo 48 `mi_i7_isole` — Isolé ou pseudo-isolé
VOIX (fr) : Il y a deux cas. Un système isolé : il n’est soumis à aucune force, comme une sonde très loin de tout. Cela n’existe pas en pratique. Un système pseudo-isolé : il est soumis à des forces, mais elles se compensent : la somme des forces égale vecteur nul, comme l’autoporteur.
ÉCRAN : Isolé : aucune force | Pseudo-isolé : ΣF⃗ = 0⃗

### Diapo 49 `mi_i8_enonce` — Le principe d’inertie
VOIX (fr) : Nous pouvons maintenant écrire le principe d’inertie. Si G est au repos, il reste au repos : le vecteur vitesse est nul. S’il est en mouvement, il reste en mouvement rectiligne uniforme : le vecteur vitesse est constant. Je relis : dans un référentiel galiléen, si un solide est isolé ou pseudo-isolé, le vecteur vitesse de son centre d’inertie est constant.
ÉCRAN : v⃗_G = 0⃗ : repos · v⃗_G constant : MRU
QUESTION : Un solide pseudo-isolé, immobile au départ dans un référentiel galiléen, peut se mettre en mouvement tout seul. OPTIONS : ['Vrai', 'Faux']
## Partie 2 — Référentiel galiléen et méthode

### Diapo 50 `mi_i9_galileen` — Le référentiel galiléen
VOIX (fr) : Un référentiel galiléen est un référentiel où le principe d’inertie est vérifié. Le référentiel terrestre est galiléen. Regarde cette boule suspendue dans le bus. Quand le bus roule en mouvement rectiligne uniforme, le fil reste vertical : la boule est au repos dans le bus. Donc le bus, lui aussi, est galiléen. Mais quand le bus freine brusquement, la boule part vers l’avant sans que rien ne la pousse. Le bus qui freine n’est pas galiléen.
ÉCRAN : Galiléen : terrestre, et tout référentiel en MRU par rapport à lui

### Diapo 51 `mi_i10_grue` — Méthode : appliquer le principe d’inertie
VOIX (fr) : Voici la méthode pour appliquer le principe d’inertie. Une grue monte un bloc de béton de mille cinq cents kilogrammes, à vitesse constante. Première étape : le système, c’est le bloc. Deuxième étape : les forces : le poids P vers le bas, et la tension T du câble vers le haut. Troisième étape : G monte en mouvement rectiligne uniforme, dans le référentiel terrestre, qui est galiléen. Donc, d’après le principe d’inertie : vecteur P plus vecteur T égale vecteur nul. Quatrième étape : T égale P égale m fois g, mille cinq cents fois dix, soit un virgule cinq fois dix puissance quatre newtons.
ÉCRAN : Système · forces · mouvement de G · ΣF⃗ = 0⃗ | T = P = m·g = 1,5 × 10⁴ N

### Diapo 52 `mi_i11_eleve` — À toi : le seau du puits
VOIX (fr) : À toi. Un seau d’eau de huit kilogrammes monte du puits à vitesse constante. g égale dix newtons par kilogramme. Quelle est la tension T de la corde ? Applique la méthode.
ÉCRAN : m = 8 kg ; vitesse constante ; g = 10 N/kg
QUESTION : Un seau de 8 kg monte à vitesse constante (g = 10 N/kg). La tension de la corde vaut… OPTIONS : ['8 N', '80 N', 'plus de 80 N, car il monte']
## Partie 2 — Le centre de masse

### Diapo 53 `mi_g1_haltere` — Le centre de masse d’un haltère
VOIX (fr) : Maintenant le centre de masse. Voici un haltère : deux masses égales en A un et A deux. Le centre de masse C est le point tel que : m un fois vecteur CA un, plus m deux fois vecteur CA deux, égale vecteur nul. Comme les masses sont égales : vecteur CA un plus vecteur CA deux égale vecteur nul, donc C est au milieu de A un A deux. Si tu poses l’haltère sur ton doigt en C, il reste en équilibre. Pour un solide homogène, le centre de masse et le centre d’inertie G sont le même point.
ÉCRAN : m₁·CA⃗₁ + m₂·CA⃗₂ = 0⃗ | m₁ = m₂ : C au milieu

### Diapo 54 `mi_g2_relation` — La relation barycentrique
VOIX (fr) : Pour trouver G de deux corps, il y a la relation barycentrique. On prend n’importe quel point O. Vecteur OG égale m un fois vecteur OG un, plus m deux fois vecteur OG deux, le tout sur m un plus m deux. Et G est toujours entre G un et G deux, plus près de la masse la plus grande.
ÉCRAN : OG⃗ = (m₁·OG⃗₁ + m₂·OG⃗₂)/(m₁ + m₂)

### Diapo 55 `mi_g3_marteau` — Méthode : le centre de masse du marteau
VOIX (fr) : Voici la méthode, avec un marteau. Le manche : m un égale cent grammes, son centre est G un. La tête : m deux égale quatre cents grammes, son centre est G deux. G un G deux égale vingt-cinq centimètres. La méthode : on prend O en G un. Vecteur G un G un est nul, donc : vecteur G un G égale m deux fois vecteur G un G deux, sur m un plus m deux. L’application numérique : G un G égale quatre cents sur cinq cents, fois vingt-cinq, soit vingt centimètres. G est près de la tête, car elle est la plus lourde.
ÉCRAN : O en G₁ : G₁G⃗ = m₂·G₁G⃗₂/(m₁ + m₂) | G₁G = 400/500 × 25 = 20 cm

### Diapo 56 `mi_g4_eleve` — À toi : une tige à deux masses
VOIX (fr) : À toi : une tige légère. m un égale deux cents grammes en A, et m deux égale six cents grammes en B. AB égale quarante centimètres. Où est G ? Prends O en A.
ÉCRAN : m₁ = 200 g ; m₂ = 600 g ; AB = 40 cm
QUESTION : m₁ = 200 g en A, m₂ = 600 g en B, AB = 40 cm. AG vaut… OPTIONS : ['30 cm', '10 cm', '20 cm']
## Bilan du cours

### Diapo 57 `mi_b1_bilan` — Ce qu’il faut retenir
VOIX (fr) : Voici ce qu’il faut retenir. Un : les forces : P égale m fois g, et deux forces qui se compensent. Deux : le mouvement est relatif, on choisit le référentiel. Trois : les repères : le vecteur OM, et t égale zéro. Quatre : la trajectoire. Cinq : la vitesse : v m égale d sur delta t, et v i égale M i moins un M i plus un sur deux tau. Six : le mouvement rectiligne uniforme : x de t égale v x fois t plus x zéro. Sept : le mouvement circulaire uniforme : oméga égale v sur R, T égale deux pi sur oméga, f égale un sur T. Huit : le principe d’inertie : isolé ou pseudo-isolé, G au repos ou en mouvement rectiligne uniforme. Neuf : le centre de masse, avec la relation barycentrique.
ÉCRAN : 1 · Forces : P = m·g ; deux forces se compensent : même droite, sens contraires, même intensité. | 2 · Relativité : le mouvement dépend du référentiel. | 3 · Repères : OM⃗ = x·i⃗ + y·j⃗ + z·k⃗ ; origine des dates t = 0. | 4 · Trajectoire : ensemble des positions successives. | 5 · Vitesse : v_m = d/Δt ; v_i = Mᵢ₋₁Mᵢ₊₁/(2τ) ; 1 m/s = 3,6 km/h. | 6 · MRU : x(t) = v_x·t + x₀. | 7 · MCU : ω = v/R ; T = 2π/ω ; f = 1/T. | 8 · Principe d’inertie : isolé ou pseudo-isolé ⇒ v⃗_G constant (référentiel galiléen). | 9 · Centre de masse : OG⃗ = (m₁·OG⃗₁ + m₂·OG⃗₂)/(m₁ + m₂).

### Diapo 58 `mi_b2_carte` — La carte du chapitre
VOIX (fr) : Et voici la carte du chapitre. Au centre, le mouvement et l’inertie. Première branche : les forces. Puis le référentiel. Puis les repères. Puis la trajectoire. Puis la vitesse. Puis le mouvement rectiligne uniforme. Puis le mouvement circulaire uniforme. Puis le principe d’inertie. Et enfin, le centre de masse. Touche une branche pour relire sa phrase.
ÉCRAN : Forces · Référentiel · Repères · Trajectoire · Vitesse · MRU · MCU · Principe d’inertie · Centre de masse.

### Diapo 59 `mi_fermeture_cours` — Ce qu’il faut retenir, et comment réviser
VOIX (fr) : Nous arrivons à la fin du cours : le mouvement et le principe d’inertie. Que faut-il retenir ? Trois idées. Première : le mouvement est relatif, on choisit d’abord le référentiel. Deuxième : pour un mouvement rectiligne uniforme, x de t égale v x fois t plus x zéro. Troisième : le principe d’inertie : un solide pseudo-isolé a son centre d’inertie au repos ou en mouvement rectiligne uniforme. Maintenant quelques conseils pour réviser. Relis ton cahier, et refais seul les calculs. Dans un calcul, écris la relation, puis l’application numérique, puis le résultat avec son unité, car chaque étape a ses points. Le jour du contrôle, partage ton temps, et commence par la question qui te paraît facile. La veille, dors bien. Écris ces conseils dans ton cahier. Tu as bien travaillé, bon courage !
ÉCRAN : Retenir : référentiel · x(t) = v_x·t + x₀ · principe d’inertie | Réviser : relire le cahier, refaire les calculs seul | Rédiger : relation → A.N. → résultat avec l’unité | Jour J : gérer son temps · bien dormir la veille

## Questions de bloc (posées après la dernière diapo du bloc)
- après diapo 3 `mi_b1` RETROUVER : Cahier fermé : écris la relation du poids avec ses unités.
- après diapo 3 `mi_b1` EXERCICE : Le poids d’un corps de 4 kg (g = 10 N/kg) vaut… OPTIONS : ['4 N', '40 N', '0,4 N']
- après diapo 5 `mi_b2` RETROUVER : Cahier fermé : quand deux forces se compensent-elles ?
- après diapo 5 `mi_b2` EXERCICE : Un livre de 2 kg posé sur une table : la réaction R vaut… OPTIONS : ['2 N', '20 N', '0 N']
- après diapo 8 `mi_b3` RETROUVER : Cahier fermé : comment calcule-t-on la pente a d’une droite ?
- après diapo 8 `mi_b3` EXERCICE : Une droite passe par (0 ; 1) et (1 ; 4). Sa pente vaut… OPTIONS : ['1', '3', '4']
- après diapo 11 `mi_b4` RETROUVER : Cahier fermé : définis le référentiel.
- après diapo 11 `mi_b4` EXERCICE : Une personne assise dans une voiture qui roule est au repos par rapport… OPTIONS : ['au sol', 'à la voiture', 'à un arbre']
- après diapo 14 `mi_b5` RETROUVER : Cahier fermé : écris le vecteur position dans le plan.
- après diapo 14 `mi_b5` EXERCICE : Une voiture sur une route droite : le repère d’espace a… OPTIONS : ['un axe', 'deux axes', 'trois axes']
- après diapo 18 `mi_b6` RETROUVER : Cahier fermé : définis la trajectoire.
- après diapo 18 `mi_b6` EXERCICE : La trajectoire d’une balle qu’on lance en l’air vers l’avant est… OPTIONS : ['rectiligne', 'circulaire', 'curviligne']
- après diapo 21 `mi_b7` RETROUVER : Cahier fermé : écris la relation de la vitesse moyenne et ses unités.
- après diapo 21 `mi_b7` EXERCICE : 36 km/h en m/s, c’est… OPTIONS : ['10 m/s', '129,6 m/s', '3,6 m/s']
- après diapo 24 `mi_b8` RETROUVER : Cahier fermé : que représente τ sur un enregistrement ?
- après diapo 24 `mi_b8` EXERCICE : τ = 40 ms : la durée entre M₀ et M₃ est… OPTIONS : ['80 ms', '120 ms', '160 ms']
- après diapo 27 `mi_b9` RETROUVER : Cahier fermé : écris la relation de la vitesse instantanée.
- après diapo 27 `mi_b9` EXERCICE : M₁M₃ = 4 cm et τ = 40 ms : v₂ vaut… OPTIONS : ['0,5 m/s', '1 m/s', '0,1 m/s']
- après diapo 30 `mi_b10` RETROUVER : Cahier fermé : donne les quatre caractéristiques du vecteur vitesse.
- après diapo 30 `mi_b10` EXERCICE : Échelle 1 cm ↔ 2 m/s : un vecteur de 6 m/s mesure… OPTIONS : ['3 cm', '12 cm', '6 cm']
- après diapo 33 `mi_b11` RETROUVER : Cahier fermé : définis le mouvement rectiligne uniforme.
- après diapo 33 `mi_b11` EXERCICE : Pour un MRU, la courbe x = f(t) est… OPTIONS : ['une droite', 'une parabole', 'un cercle']
- après diapo 36 `mi_b12` RETROUVER : Cahier fermé : écris l’équation horaire du MRU.
- après diapo 36 `mi_b12` EXERCICE : x(t) = 3·t + 2 (SI) : la vitesse vaut… OPTIONS : ['2 m/s', '3 m/s', '5 m/s']
- après diapo 39 `mi_b13` RETROUVER : Cahier fermé : écris les relations de ω, T et f.
- après diapo 39 `mi_b13` EXERCICE : La fréquence f d’un MCU s’exprime en… OPTIONS : ['rad/s', 'Hz', 's']
- après diapo 41 `mi_b14` RETROUVER : Cahier fermé : donne les étapes du calcul de T à partir d’un enregistrement circulaire.
- après diapo 41 `mi_b14` EXERCICE : ω = 2π rad/s : la période vaut… OPTIONS : ['1 s', '2π s', '0,5 s']
- après diapo 45 `mi_b15` RETROUVER : Cahier fermé : qu’a de particulier le centre d’inertie d’un autoporteur lancé ?
- après diapo 45 `mi_b15` EXERCICE : Le centre d’inertie d’une boule homogène est… OPTIONS : ['à sa surface', 'en son centre', 'en dessous d’elle']
- après diapo 49 `mi_b16` RETROUVER : Cahier fermé : énonce le principe d’inertie.
- après diapo 49 `mi_b16` EXERCICE : L’autoporteur glisse sur la table horizontale sans frottement : il est… OPTIONS : ['isolé', 'pseudo-isolé', 'ni l’un ni l’autre']
- après diapo 52 `mi_b17` RETROUVER : Cahier fermé : donne les quatre étapes pour appliquer le principe d’inertie.
- après diapo 52 `mi_b17` EXERCICE : Un ascenseur de 500 kg monte à vitesse constante (g = 10 N/kg). La tension du câble vaut… OPTIONS : ['500 N', '5 000 N', '0 N']
- après diapo 56 `mi_b18` RETROUVER : Cahier fermé : écris la relation barycentrique pour deux corps.
- après diapo 56 `mi_b18` EXERCICE : m₁ = m₂ : le centre de masse est… OPTIONS : ['au milieu de G₁G₂', 'en G₁', 'en G₂']
- après diapo 58 `mi_b19` RETROUVER : Cahier fermé : écris l’équation horaire du MRU et la relation ω = v/R.
- après diapo 58 `mi_b19` EXERCICE : Un solide pseudo-isolé, dans un référentiel galiléen, a son centre d’inertie… OPTIONS : ['accéléré', 'au repos ou en MRU', 'en MCU']
- après diapo 59 `mi_bloc_fin_cours` RETROUVER : Cahier fermé : cite trois idées à retenir du cours.
- après diapo 59 `mi_bloc_fin_cours` EXERCICE : Pour un calcul en physique, on écrit… OPTIONS : ['le résultat seul', 'la relation, l’application numérique, le résultat avec l’unité', 'l’unité seule']
