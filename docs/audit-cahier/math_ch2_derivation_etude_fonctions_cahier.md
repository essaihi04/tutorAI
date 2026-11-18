# Cahier de l'élève — Dérivation et étude des fonctions (`math_ch2_derivation_etude_fonctions`)

18 novembre 2026, skill `cahier-de-l-eleve`. Le cahier idéal du chapitre, d'un seul tenant, dans l'ordre du cours en ligne. Les parties I. à XIII. sont celles du cours (`activities[].title`) : le lecteur les écrit lui-même en rose en tête du bloc (`CycleBloc.tsx`), les lignes du bloc portent donc la numérotation interne (1., 2., a), méthodes 1) 2) 3)). Chaque bloc a un nombre de lignes différent de son nombre de diapositives, pour que le lecteur garde ces lignes numérotées dans l'ordre (sinon il range une ligne sous chaque titre de diapositive). Application : script `/tmp/claude-0/-home-user-tutorAI/02f8f400-8fae-5359-a79d-1358639cc2d0/scratchpad/math_ch2_derivation_etude_fonctions/appliquer.py` (relançable).

Sources : `screen_content` / `speech_text` du cours, architecture `backend/data/curriculum/architecture/math_ch2_derivation_etude_fonctions.md`, exploration `backend/data/curriculum/exploration/derivation_etude_fonctions.json` (20 cas types, erreurs d'examen : phrase d'interprétation avec équation et voisinage, « demi-tangente » et son sens, signe de f′ justifié, « en changeant de signe », f(x) − y étudié par un signe, réciproque en trois lignes). Rien hors cadre : pas d'approximation affine, pas de fonctions ln/exp (chapitres suivants).


## I. Pourquoi dériver ; le nombre dérivé

- But : chaque calcul répond à une question sur la courbe (C_f) de f.
- Tangente → f′(a) ; variations → signe de f′ ; concavité → signe de f″ ; branches → limites.
- 1. Rappels. a) Pente de (AB) : (y_B − y_A)/(x_B − x_A) ; > 0 : monte ; < 0 : descend.
- b) Droite (D) : y = ax + b ; a est la pente, b l'ordonnée à l'origine.
- Un point M(x₀ ; y₀) est sur (D) si et seulement si y₀ = ax₀ + b.
- *Dessin — La pente de y = 2x − 1 : De (0 ; −1), un pas de 1 vers la droite fait monter de 2 : la pente est a = 2, et b = −1.*
- c) (xⁿ)′ = n·xⁿ⁻¹ ; (k)′ = 0 ; (k·u)′ = k·u′ ; (u + v)′ = u′ + v′.
- Exemple : (3x² − 5x + 4)′ = 6x − 5.
- d) Signe d'un produit : un tableau, une ligne par facteur, puis la règle des signes.
- Exemple : (x − 1)(x + 1) est + sur ]−∞ ; −1[, − sur ]−1 ; 1[, + sur ]1 ; +∞[.
- e) lim_{x→0⁺} 1/x = +∞ ; lim_{x→0⁻} 1/x = −∞ ; lim_{x→±∞} 1/x = 0.
- *Dessin — 1/x près de 0 : À droite de 0, 1/x monte vers +∞ ; à gauche, il plonge vers −∞ ; en ±∞, il tend vers 0.*
- 2. Taux d'accroissement de f entre x₀ et x (x ≠ x₀) : (f(x) − f(x₀))/(x − x₀).
- C'est la pente de la sécante (AM), avec A(x₀ ; f(x₀)) et M(x ; f(x)).
- 3. Définition : f, définie sur un intervalle ouvert I contenant x₀, est dérivable en x₀
- si lim_{x→x₀} (f(x) − f(x₀))/(x − x₀) = l avec l ∈ ℝ ; l = f′(x₀) est le nombre dérivé.
- Autre écriture (x = x₀ + h) : f′(x₀) = lim_{h→0} (f(x₀ + h) − f(x₀))/h.
- Quand M → A, la sécante (AM) devient la tangente en A : f′(x₀) est sa pente.
- *Dessin — La sécante (AM) : La pente de (AM) est le taux d'accroissement (f(x) − f(1))/(x − 1) ; pour M(2 ; 4), elle vaut 3/1 = 3.*
- *Dessin — De la sécante à la tangente : Quand M arrive sur A, la sécante (pointillés) devient la tangente (T) en A ; sa pente est le nombre dérivé f′(1) = 2.*
- 4. Méthode (dérivabilité en x₀) : 1) f(x₀) à part ; 2) le taux donne « 0/0 » ;
- 3) factoriser par (x − x₀) (polynôme) ou multiplier par le conjugué (racine) ;
- 4) on trouve l ∈ ℝ : « donc f est dérivable en x₀ et f′(x₀) = l ».
- Exemple : g(x) = √(x + 1) en 3 : taux = 1/(√(x + 1) + 2) → 1/4 = g′(3).

## II. L'équation de la tangente

- 1. Si f est dérivable en x₀, (C_f) admet au point A(x₀ ; f(x₀)) la tangente
- (T) : y = f′(x₀)(x − x₀) + f(x₀).
- Méthode : 1) « f dérivable en x₀ car … » ; 2) f(x₀), f′(x), f′(x₀) ; 3) remplacer, développer.
- Exemple : f(x) = x + 1/x, x₀ = 2 : f(2) = 5/2, f′(2) = 3/4, (T) : y = (3/4)x + 1.
- Vérifier : A est sur (T) : (3/4) × 2 + 1 = 5/2 ✓.
- 2. Si f′(x₀) = 0 : tangente horizontale d'équation y = f(x₀) (x + 1/x en 1 : y = 2).
- *Dessin — Tangente à x + 1/x en 2 : En A(2 ; 5/2), la tangente a pour pente f′(2) = 3/4 : (T) : y = (3/4)x + 1.*

## III. À droite, à gauche : demi-tangentes et point anguleux

- 1. f dérivable à droite en x₀ : lim_{x→x₀⁺} (f(x) − f(x₀))/(x − x₀) = l ∈ ℝ ; l = f_d′(x₀).
- (C_f) admet en A une demi-tangente à droite : y = f_d′(x₀)(x − x₀) + f(x₀), x ≥ x₀.
- De même à gauche (x → x₀⁻) : f_g′(x₀) et demi-tangente à gauche, avec x ≤ x₀.
- 2. Théorème : f dérivable en x₀ ⟺ dérivable à droite et à gauche en x₀ et f_d′(x₀) = f_g′(x₀).
- Si f_d′(x₀) ≠ f_g′(x₀) : A est un point anguleux (|x² − 1| en 1 : 2 et −2).
- Remarque : f dérivable en x₀ ⟹ f continue en x₀ ; la réciproque est fausse.
- *Dessin — Un point anguleux : En A(1 ; 0), deux demi-tangentes de pentes 2 (à droite) et −2 (à gauche) : f_d′(1) ≠ f_g′(1), A est un point anguleux.*
- 3. Si le taux tend vers ±∞ quand x → x₀⁺ (ou x₀⁻), f n'est pas dérivable à droite (ou à gauche)
- et (C_f) admet au point d'abscisse x₀ une demi-tangente verticale.
- Sens (elle part du côté de la courbe) : à droite, +∞ ↑, −∞ ↓ ; à gauche, +∞ ↓, −∞ ↑.
- Exemple : √x en 0 : taux 1/√x → +∞ : demi-tangente verticale dirigée vers le haut en O.
- 4. Par morceaux : formule de x > x₀ à droite, de x < x₀ à gauche ; comparer f_d′ et f_g′.
- Attention : écrire « demi-tangente » (pas « tangente ») et, si elle est verticale, son sens.
- *Dessin — Demi-tangente verticale en 0 : Pour √x en 0, le taux 1/√x → +∞ : pas dérivable à droite, mais demi-tangente verticale dirigée vers le haut.*

## IV. Calculer une dérivée

- 1. (xⁿ)′ = n·xⁿ⁻¹ (n ∈ ℤ*, x ≠ 0 si n < 0) ; (1/x)′ = −1/x² (x ≠ 0) ; (√x)′ = 1/(2√x) (x > 0).
- (sin x)′ = cos x ; (cos x)′ = −sin x ; (tan x)′ = 1 + tan²x (cos x ≠ 0).
- (sin(ax + b))′ = a·cos(ax + b) ; (cos(ax + b))′ = −a·sin(ax + b).
- 2. (u·v)′ = u′v + uv′ ; (u/v)′ = (u′v − uv′)/v² et (1/v)′ = −v′/v², v ≠ 0 sur I.
- Attention : (u·v)′ ≠ u′·v′ ; dans (u/v)′, un moins au numérateur et v² en bas.
- 3. (uⁿ)′ = n·u′·uⁿ⁻¹ ; ex. : ((x² − 2x + 3)³)′ = 3(2x − 2)(x² − 2x + 3)² (ne pas oublier u′).
- 4. (√u)′ = u′/(2√u) là où u > 0 ; ex. : (√(x² + 1))′ = x/√(x² + 1), du signe de x.
- (ⁿ√u)′ = u′/(n·(ⁿ√u)ⁿ⁻¹) là où u > 0 ; ex. : (³√x)′ = 1/(3(³√x)²) sur ]0 ; +∞[.
- Composée : g dérivable en x₀, f dérivable en g(x₀) ⟹ (f∘g)′(x₀) = g′(x₀)·f′(g(x₀)).
- 5. f dérivable sur [a ; b] : sur ]a ; b[, à droite en a, à gauche en b ; f′ : x ↦ f′(x).
- Polynôme : dérivable sur ℝ ; rationnelle : sur chaque intervalle de Df ; √x : sur ]0 ; +∞[.
- 6. Méthode « f′(x) = … » : 1) « f est dérivable sur I car … » ; 2) dériver ; 3) factoriser.

## V. Signe de f' et variations

- 1. Théorème (f dérivable sur un intervalle I) : f′ > 0 sur I ⟹ f strictement croissante sur I ;
- f′ < 0 sur I ⟹ f strictement décroissante sur I ; f′ = 0 sur I ⟹ f constante sur I.
- Remarque : f′ peut s'annuler en des points isolés (x³ est strictement croissante sur ℝ).
- 2. Si f′ s'annule en x₀ en changeant de signe, f(x₀) est un extremum de f :
- + puis − : maximum ; − puis + : minimum (x³ − 3x : max f(−1) = 2, min f(1) = −2).
- Extremum en a (I ouvert) ⟹ f′(a) = 0 ; réciproque fausse : x³ en 0 (+ 0 +).
- *Dessin — Sommet et creux de x³ − 3x : Tangente horizontale au sommet et au creux : f′ s'annule en changeant de signe, maximum f(−1) = 2, minimum f(1) = −2.*
- 3. Méthode (tableau de variations) : 1) « f est dérivable sur I car … », calculer f′(x) ;
- 2) factoriser f′(x) et écarter les facteurs positifs en le disant (3 > 0, x² > 0, √… > 0) ;
- 3) tableau de signe ; 4) tableau x | f′(x) | f(x), limites et extremums au bout des flèches.
- Exemple : x³ − 3x : f′(x) = 3(x − 1)(x + 1), du signe de (x − 1)(x + 1).
- *Dessin — Variations de f(x) = x³ − 3x : f′(x) = 3(x − 1)(x + 1) : maximum f(−1) = 2, minimum f(1) = −2 ; les limites aux bornes au bout des flèches.*
- Attention : valeur exclue de Df = double barre (pas un 0) ; flèche vers la limite calculée.
- Exemple : x + 1/x : f′(x) = (x − 1)(x + 1)/x², double barre en 0.
- 4. Minimum m sur I ⟹ f(x) ≥ m pour tout x de I (x + 1/x ≥ 2 pour tout x > 0).
- 5. Fonction auxiliaire : f′(x) = g(x)/x² et x² > 0 ⟹ f′(x) a le signe de g(x).
- Le signe de g se lit dans son tableau (partie I) : minimum positif ⟹ g(x) > 0.
- *Dessin — x + 1/x sur ]0 ; +∞[ : la double barre : 0 est exclu : une double barre, pas un 0 ; la flèche part de la limite +∞ en 0⁺ et descend au minimum 2.*

## VI. Concavité et point d'inflexion

- 1. (C_f) au-dessus de ses tangentes sur I : convexe (∪) ; en dessous : concave (∩).
- 2. f deux fois dérivable sur I, f″ = (f′)′ : f″ ≥ 0 sur I ⟹ convexe ; f″ ≤ 0 ⟹ concave.
- 3. f″ s'annule en x₀ en changeant de signe ⟹ I(x₀ ; f(x₀)) est un point d'inflexion de (C_f).
- En I, (C_f) traverse sa tangente ; x³ − 3x : f″(x) = 6x, I(0 ; 0), tangente y = −3x.
- Exemple : x³ − 3x² + 2x + 2 : f″(x) = 6(x − 1) change de signe en 1 : I(1 ; 2).
- Attention : f″(x₀) = 0 seul ne suffit pas (x⁴ : f″(x) = 12x² ≥ 0, pas d'inflexion).
- *Dessin — Le point d'inflexion I : En I(0 ; 0), la tangente y = −3x traverse la courbe : concave avant, convexe après, I est un point d'inflexion.*
- *Dessin — Tableau de concavité de x³ − 3x : f″(x) = 6x change de signe en 0 : (C_f) est concave (∩) puis convexe (∪), et I(0 ; 0) est un point d'inflexion.*

## VII. Branches infinies

- 1. lim_{x→a⁺} f(x) = ±∞ (ou x → a⁻) : la droite x = a est une asymptote verticale à (C_f).
- 2. lim_{x→+∞} f(x) = b : la droite y = b est asymptote horizontale à (C_f) au voisinage de +∞.
- 3. lim_{x→+∞} [f(x) − (ax + b)] = 0, a ∈ ℝ* : y = ax + b asymptote oblique au voisinage de +∞.
- Remarque : de même en −∞ ; toujours écrire « au voisinage de +∞ » (ou « de −∞ »).
- 4. En ±∞ : f(x) → ±∞ et f(x)/x → ±∞ : branche parabolique de direction l'axe des ordonnées.
- f(x) → ±∞ et f(x)/x → 0 : branche parabolique de direction l'axe des abscisses.
- *Dessin — Asymptote oblique : L'écart f(x) − (2x + 1) = 1/x tend vers 0 en +∞ : la droite (Δ) : y = 2x + 1 est asymptote oblique au voisinage de +∞.*
- *Dessin — Deux branches paraboliques : x² : f(x)/x = x → +∞, direction l'axe des ordonnées ; √x : f(x)/x = 1/√x → 0, direction l'axe des abscisses.*
- 5. Si f(x)/x → a ≠ 0, on calcule lim [f(x) − ax] :
- → b ∈ ℝ : la droite y = ax + b est une asymptote oblique à (C_f) ;
- → ±∞ : branche parabolique de direction la droite y = ax (x + √x : direction y = x).
- Phrase type : « (C_f) admet une … d'équation … au voisinage de +∞ » (équation et voisinage).
- 6. Droite (D) : y = ax + b donnée : montrer que lim [f(x) − (ax + b)] = 0, puis la phrase.
- *Dessin — Branche parabolique de direction y = x : f(x)/x → 1 mais f(x) − x = √x → +∞ : l'écart grandit, branche parabolique de direction y = x, sans asymptote.*

## VIII. Position relative d'une courbe et d'une droite

- 1. Position de (C_f) et de (Δ) : y = ax + b : on étudie le signe de f(x) − (ax + b).
- > 0 sur I : (C_f) au-dessus de (Δ) sur I ; < 0 : (C_f) en dessous de (Δ).
- = 0 en x₀ : (C_f) et (Δ) se coupent au point d'abscisse x₀.
- Méthode : f(x) − y, factoriser, tableau de signe (ligne du facteur), conclure par intervalle.
- Attention : asymptote → une limite ; position → un signe (x + 1/x − x = 1/x).
- *Dessin — Position de la courbe et de (Δ) : f(x) = x + 1/x et (Δ) : y = x : f(x) − x = 1/x, positif pour x > 0 (au-dessus), négatif pour x < 0 (en dessous).*

## IX. Axe et centre de symétrie

- 1. Le symétrique du réel x par rapport au réel a est 2a − x.
- 2. Axe x = a de (C_f) : pour tout x ∈ Df, (2a − x) ∈ Df et f(2a − x) = f(x).
- 3. Centre Ω(a ; b) de (C_f) : pour tout x ∈ Df, (2a − x) ∈ Df et f(2a − x) + f(x) = 2b.
- Exemple : (x + 1)/(x − 2) : f(4 − x) + f(x) = 2 = 2 × 1 : Ω(2 ; 1) est centre de symétrie.
- Remarque : a = 0 : f paire (f(−x) = f(x)) : axe (Oy) ; f impaire (f(−x) = −f(x)) : centre O.
- *Dessin — Centre de symétrie Ω(2 ; 1) : M(3 ; 4) et M′(1 ; −2) ont pour milieu Ω(2 ; 1) : f(4 − x) + f(x) = 2, Ω est centre de symétrie de la courbe.*

## X. Construire et lire la courbe

- 1. Méthode (tracer (C_f)) dans un repère orthonormé (O ; i⃗ ; j⃗) :
- 1) lister ce que l'étude annonce : asymptotes, branches, extremums, points, tangentes ;
- 2) tracer d'abord les asymptotes et les tangentes (deux points par droite) ;
- 3) placer les points : extremums avec leur petite tangente horizontale, points de l'énoncé ;
- 4) tracer la courbe d'un seul trait en suivant les flèches du tableau et la concavité ;
- elle longe chaque asymptote du côté donné par la position relative.
- 2. f paire ou impaire : on l'étudie sur Df ∩ [0 ; +∞[, puis on complète par symétrie.
- 3. Lecture : nombre de solutions de f(x) = m = nombre de points communs de (C_f) et de y = m.
- f(x) ≥ 0 : (C_f) au-dessus de l'axe des abscisses ; f(x) = x : (C_f) coupe y = x.
- *Dessin — Résoudre f(x) = 3 sur la courbe : La droite y = 3 coupe la courbe de f(x) = x + 1/x en deux points : l'équation f(x) = 3 a deux solutions.*

## XI. Dérivée et courbe de la fonction réciproque

- 1. Rappel : f continue et strictement monotone sur I admet une réciproque f⁻¹ sur J = f(I).
- (C_f⁻¹) est la symétrique de (C_f) par rapport à la droite y = x ; f(x₀) = y₀ ⟺ f⁻¹(y₀) = x₀.
- 2. Théorème : si f est continue et strictement monotone sur I, dérivable en x₀ et f′(x₀) ≠ 0,
- alors f⁻¹ est dérivable en y₀ = f(x₀) et (f⁻¹)′(y₀) = 1/f′(x₀).
- Si f est dérivable sur I et f′ ne s'annule pas sur I : (f⁻¹)′(x) = 1/f′(f⁻¹(x)) sur J.
- Dans le miroir, la pente m devient 1/m : x² + 1 : f′(2) = 4, (f⁻¹)′(5) = 1/4.
- *Dessin — La pente dans le miroir : Dans le miroir y = x, la tangente de pente f′(2) = 4 en A devient la tangente de pente 1/4 en A′ : (f⁻¹)′(5) = 1/4.*
- Attention : f′(x₀) = 0 ⟹ tangente verticale à (C_f⁻¹) en (y₀ ; x₀) : f⁻¹ non dérivable en y₀.
- 3. Méthode ((f⁻¹)′(y₀)) : 1) trouver x₀ tel que f(x₀) = y₀ ; 2) vérifier les conditions ;
- 3) (f⁻¹)′(y₀) = 1/f′(x₀). Exemple : x³ + x : f(1) = 2, f′(1) = 4, donc (f⁻¹)′(2) = 1/4.
- 4. (C_f⁻¹) : symétrique par rapport à y = x de la partie de (C_f) sur I ; (a ; b) → (b ; a).
- Une tangente horizontale devient verticale ; une asymptote se symétrise aussi.

## XII. Le problème d'analyse : une étude complète

- 1. Plan d'étude : 1) Df ; 2) limites aux bornes, branches infinies ; 3) dérivabilité au bord ;
- 4) f′(x), son signe, variations ; 5) f″, concavité ; 6) position relative ; 7) tracé ; 8) f⁻¹.
- Remarque : un résultat donné (« montrer que … ») sert à la suite, même non démontré.
- 2. Exemple : f(x) = x√(x + 1) : il faut x + 1 ≥ 0, donc Df = [−1 ; +∞[.
- Taux en −1⁺ : x/√(x + 1) → −∞ : demi-tangente verticale dirigée vers le bas en A(−1 ; 0).
- f′(x) = (3x + 2)/(2√(x + 1)) sur ]−1 ; +∞[, du signe de 3x + 2 car 2√(x + 1) > 0.
- *Dessin — Variations de f(x) = x√(x + 1) : f′(x) a le signe de 3x + 2 : f décroît de 0 au minimum −2√3/9 en −2/3, puis croît vers +∞.*
- Minimum f(−2/3) = −2√3/9 ; f(0) = 0 : (C_f) passe par O.
- f(x)/x = √(x + 1) → +∞ en +∞ : branche parabolique de direction l'axe des ordonnées.
- 3. Rappel : f continue et strictement monotone sur [a ; b] et f(a)·f(b) < 0
- ⟹ l'équation f(x) = 0 admet une solution unique α dans ]a ; b[.
- Interprétation : (C_f) coupe l'axe des abscisses en un seul point, d'abscisse α.
- *Dessin — La courbe de f(x) = x√(x + 1) : Demi-tangente verticale vers le bas en A(−1 ; 0), minimum en −2/3 (tangente horizontale), puis O et B(1 ; √2), de plus en plus raide.*

## XIII. Bilan du chapitre

- Fiche : tangente y = f′(a)(x − a) + f(a) ; taux infini : demi-tangente verticale.
- Signe de f′ : variations ; f′ ou f″ s'annule en changeant de signe : extremum ou inflexion.
- Branches : x = a ; y = b ; y = ax + b ; directions (Oy), (Ox), y = ax ; toujours le voisinage.
- Position : signe de f(x) − y ; symétrie : (2a − x) ∈ Df ; (f⁻¹)′(y₀) = 1/f′(x₀), f′(x₀) ≠ 0.
- Carte : recopier la carte du chapitre et entourer en rouge les branches à retravailler.

**Seulement dans la copie en attente** (exercice de la fonction auxiliaire, `df_n3_b5`, partie V) :

- Exemple : g(x) = 2x³ − 3x² + 2 sur ]0 ; +∞[ : g′(x) = 6x(x − 1), du signe de x − 1.
- g décroît puis croît : minimum g(1) = 1, donc g(x) ≥ 1 > 0.
- f(x) = x² − 3x − 2/x : f′(x) = 2x − 3 + 2/x² = (2x³ − 3x² + 2)/x² = g(x)/x².
- g(x) > 0 et x² > 0 : f′(x) > 0, f est strictement croissante sur ]0 ; +∞[.
- lim_{x→0⁺} f(x) = −∞ et lim_{x→+∞} f(x) = +∞ : au bout des flèches.
- Tracé : A(−1 ; 0), minimum (−2/3 ; −2√3/9) ≈ (−0,67 ; −0,38), O et B(1 ; √2) ≈ (1 ; 1,41).
- Puis d'un trait : de A vers le bas, plate au minimum, par O et B, de plus en plus raide.
- *Dessins — tableaux de variations de g (minimum g(1) = 1 > 0) et de f (croissante de −∞ à +∞).*

## Découpage

### Cours en ligne (`backend/data/courses/math_ch2_derivation_etude_fonctions.json`)

| Bloc | Diapos | Lignes (clés du script) | Figures du bloc |
|---|---|---|---|
| `df_s0_b1` | c1_carte, z1_pente, z2_equation_droite | 5 : but, but2, pente_l, droite_l, droite_l2 | La pente de y = 2x − 1 |
| `df_s0_b2` | z3_deriver_polynome, z4_signe_produit, z5_un_sur_x | 5 : poly_l, poly_l2, signe_l, signe_ex, unsurx_l | 1/x près de 0 |
| `df_s1_b1` | nd1_secante, nd2_rapprocher, nd3_nombre_derive | 6 : taux, taux2, def1, def2, def3, def4 | La sécante (AM); De la sécante à la tangente |
| `df_s1_b2` | nd4_calcul, nd4_calcul_b | 4 : meth1, meth2, meth3, meth_ex | — |
| `df_s1_b3` | tg1_equation, tg2_ecrire, tg3_verifier | 6 : tg1, tg2, tg_meth, tg_ex, tg_verif, tg_horiz | Tangente à x + 1/x en 2 |
| `df_s2_b1` | dt1_droite, dt2_gauche, dt3_anguleux | 6 : dd1, dd2, dg, thm_dg, anguleux, continue | Un point anguleux |
| `df_s2_b2` | dt4_infini, dt5_sens, dt5_sens_b, dt6_morceaux | 6 : vert1, vert2, sens, vert_ex, morceaux, att_demi | Demi-tangente verticale en 0 |
| `df_s2_b3` | dv1_tableau, dv2_produit_quotient, dv2_produit_quotient_b, dv3_puissance | 6 : us1, us2, us3, uv, uv_att, un | — |
| `df_s3_b1` | dv4_racine, dv5_racine_n, dv5b_intervalle, dv6_montrer | 6 : racu, racn, comp, interv, interv2, montrer | — |
| `df_s3_b2` | va1_monte, va2_sommet, va2_sommet_b | 6 : var1, var2, var_rq, ext1, ext2, ext3 | Sommet et creux de x³ − 3x |
| `df_s3_b2b` | va3_factoriser, va4_tableau | 4 : tab1, tab2, tab3, tab_ex | Variations de f(x) = x³ − 3x |
| `df_s3_b3` | va5_double_barre, va6_extremum, va7_auxiliaire | 5 : barre, barre_ex, min, aux1, aux2 | x + 1/x sur ]0 ; +∞[ : la double barre |
| `df_s4_b1` | co1_sous, co2_traverse, co3_f_seconde, co4_changeant | 6 : conc1, conc2, infl1, infl2, infl_ex, infl_att | Le point d'inflexion I; Tableau de concavité de x³ − 3x |
| `df_s4_b2` | bi1_verticale, bi2_horizontale, bi3_oblique, bi4_pente_om | 6 : av, ah, ao, voisinage, bp_oy, bp_ox | Asymptote oblique; Deux branches paraboliques |
| `df_s4_b3` | bi5_direction, bi6_arbre, bi6_arbre_b, bi7_droite_donnee | 5 : arbre1, arbre2, arbre3, phrase, donnee | Branche parabolique de direction y = x |
| `df_s5_b1` | pr1_dessus, pr2_signe, pr3_tableau | 5 : pos1, pos2, pos3, pos_meth, pos_att | Position de la courbe et de (Δ) |
| `df_s5_b2` | sy1_symetrique, sy2_axe, sy3_centre, sy4_rediger | 5 : sym1, sym_axe, sym_ctr, sym_ex, parite | Centre de symétrie Ω(2 ; 1) |
| `df_s5_b3` | tr1_tableau_lu, tr2_droites, tr3_points | 4 : tr0, tr1, tr2, tr3 | — |
| `df_s6_b1` | tr4_branche, tr5_symetrie, tr6_lire | 5 : tr4, tr4b, tr_par, lire, lire2 | Résoudre f(x) = 3 sur la courbe |
| `df_s6_b2` | rec1_miroir, rec2_pente, rec3_formule | 6 : rec_rap, rec_mir, rec_thm1, rec_thm2, rec_thm3, rec_pente | La pente dans le miroir |
| `df_s6_b3` | rec4_condition, rec5_national, rec6_courbe | 5 : rec_att, rec_m1, rec_m2, rec_c1, rec_c2 | — |
| `df_s7_b1` | ec1_ordre, ec2_forme, ec3_etude, ec3_etude_b | 6 : plan1, plan2, plan_rq, et_df, et_bord, et_fp | Variations de f(x) = x√(x + 1) |
| `df_s7_b2` | ec3_etude_c, ec4_unique | 5 : et_min, et_bp, tvi1, tvi2, tvi3 | La courbe de f(x) = x√(x + 1) |
| `df_s7_b3` | fin1_bilan, fin2_carte | 5 : bil1, bil2, bil3, bil4, bil5 | — |

### Copie en attente (`backend/data/courses/en_attente/math_ch2_derivation_etude_fonctions.json`)

| Bloc | Diapos | Lignes (clés du script) | Figures du bloc |
|---|---|---|---|
| `df_n1_b1` | c1_carte, z1_pente, nd1_secante | 5 : but, but2, pente_a, taux, taux2 | La sécante (AM) |
| `df_n1_b2` | nd2_rapprocher, nd3_nombre_derive, nd4_calcul, nd4_calcul_b | 6 : def1, def2_a, def3, meth1, meth2, meth3 | De la sécante à la tangente |
| `df_n1_b3` | z2_equation_droite, tg1_equation, tg2_ecrire | 5 : droite_a, tg1, tg2, tg_meth, tg_ex | Tangente à x + 1/x en 2 |
| `df_n1_b4` | tg3_verifier, dt1_droite, dt2_gauche | 5 : tg_verif, tg_horiz, dd1, dd2, dg | — |
| `df_n2_b1` | dt3_anguleux, z5_un_sur_x, dt4_infini | 6 : thm_dg, anguleux, continue, unsurx_a, vert1, vert2 | Un point anguleux; Demi-tangente verticale en 0 |
| `df_n2_b2` | dt5_sens, dt5_sens_b, dt6_morceaux | 4 : sens, vert_ex, morceaux, att_demi | — |
| `df_n2_b3` | z3_deriver_polynome, dv1_tableau, dv2_produit_quotient, dv2_produit_quotient_b | 6 : poly_a, us1, us2, us3, uv, uv_att | — |
| `df_n2_b4` | dv3_puissance, dv4_racine, dv5_racine_n | 4 : un, racu, racn, comp | — |
| `df_n3_b1` | dv5b_intervalle, dv6_montrer, va1_monte | 6 : interv, interv2, montrer, var1, var2, var_rq | — |
| `df_n3_b2` | va2_sommet, va2_sommet_b, z4_signe_produit | 5 : ext1, ext2, ext3, signe_a, signe_ex | Sommet et creux de x³ − 3x |
| `df_n3_b3` | va3_factoriser, va4_tableau, va5_double_barre | 6 : tab1, tab2, tab3, tab_ex, barre, barre_ex | Variations de f(x) = x³ − 3x; x + 1/x sur ]0 ; +∞[ : la double barre |
| `df_n3_b4` | va6_extremum, va7_auxiliaire | 3 : min, aux1, aux2 | — |
| `df_n3_b5` | va8_aux_a, va8_aux_b, va8_aux_c, va8_aux_d | 5 : ex_g1, ex_g2, ex_f1, ex_f2, ex_f3 | Variations de g(x) = 2x³ − 3x² + 2; Variations de f(x) = x² − 3x − 2/x |
| `df_s4_b1` | co1_sous, co2_traverse, co3_f_seconde, co4_changeant | 6 : conc1, conc2, infl1, infl2, infl_ex, infl_att | Le point d'inflexion I; Tableau de concavité de x³ − 3x |
| `df_s4_b2` | bi1_verticale, bi2_horizontale, bi3_oblique, bi4_pente_om | 6 : av, ah, ao, voisinage, bp_oy, bp_ox | Asymptote oblique; Deux branches paraboliques |
| `df_s4_b3` | bi5_direction, bi6_arbre, bi6_arbre_b, bi7_droite_donnee | 5 : arbre1, arbre2, arbre3, phrase, donnee | Branche parabolique de direction y = x |
| `df_s5_b1` | pr1_dessus, pr2_signe, pr3_tableau | 5 : pos1, pos2, pos3, pos_meth, pos_att | Position de la courbe et de (Δ) |
| `df_s5_b2` | sy1_symetrique, sy2_axe, sy3_centre, sy4_rediger | 5 : sym1, sym_axe, sym_ctr, sym_ex, parite | Centre de symétrie Ω(2 ; 1) |
| `df_s5_b3` | tr1_tableau_lu, tr2_droites, tr3_points | 4 : tr0, tr1, tr2, tr3 | — |
| `df_s6_b1` | tr4_branche, tr5_symetrie, tr6_lire | 5 : tr4, tr4b, tr_par, lire, lire2 | Résoudre f(x) = 3 sur la courbe |
| `df_s6_b2` | rec1_miroir, rec2_pente, rec3_formule | 6 : rec_rap, rec_mir, rec_thm1, rec_thm2, rec_thm3, rec_pente | La pente dans le miroir |
| `df_s6_b3` | rec4_condition, rec5_national, rec6_courbe | 5 : rec_att, rec_m1, rec_m2, rec_c1, rec_c2 | — |
| `df_n7_b1` | ec1_ordre, ec2_forme, ec3_etude | 4 : plan1, plan2, plan_rq, et_df | — |
| `df_n7_b2` | ec3_etude_a2, ec3_etude_b, ec3_etude_c | 4 : et_bord, et_fp, et_min, et_bp | Variations de f(x) = x√(x + 1) |
| `df_n7_b2c` | ec3_etude_d, ec3_etude_e, ec4_unique | 5 : et_pts, et_trait, tvi1, tvi2, tvi3 | La courbe de f(x) = x√(x + 1) |
| `df_s7_b3` | fin1_bilan, fin2_carte | 5 : bil1, bil2, bil3, bil4, bil5 | — |

Bulles (`concentration.cahier`) : une phrase ou deux par diapositive, la trace de cette diapositive (dictionnaire `BULLES` du script ; `df_ec3_etude` a une bulle propre à la copie en attente, où la diapositive ne traite que Df).

Figures des bulles : `df_z2_equation_droite` → La pente de y = 2x − 1 ; `df_z5_un_sur_x` → 1/x près de 0 ; `df_nd1_secante` → La sécante (AM) ; `df_nd3_nombre_derive` → De la sécante à la tangente ; `df_tg2_ecrire` → Tangente à x + 1/x en 2 ; `df_dt3_anguleux` → Un point anguleux ; `df_dt4_infini` → Demi-tangente verticale en 0 ; `df_va2_sommet_b` → Sommet et creux de x³ − 3x ; `df_va4_tableau` → Variations de f(x) = x³ − 3x ; `df_va5_double_barre` → x + 1/x sur ]0 ; +∞[ : la double barre ; `df_co2_traverse` → Le point d'inflexion I ; `df_co3_f_seconde` → Tableau de concavité de x³ − 3x ; `df_bi3_oblique` → Asymptote oblique ; `df_bi4_pente_om` → Deux branches paraboliques ; `df_bi5_direction` → Branche parabolique de direction y = x ; `df_pr2_signe` → Position de la courbe et de (Δ) ; `df_sy3_centre` → Centre de symétrie Ω(2 ; 1) ; `df_tr6_lire` → Résoudre f(x) = 3 sur la courbe ; `df_rec2_pente` → La pente dans le miroir ; `df_ec3_etude_b` → Variations de f(x) = x√(x + 1) ; `df_ec3_etude_c` → La courbe de f(x) = x√(x + 1). En attente : mêmes figures, plus `df_va8_aux_b` → tableau de g, `df_va8_aux_d` → tableau de f ; le tableau de x√(x + 1) va sur `df_ec3_etude_c` et la courbe sur `df_ec3_etude_e` (diapositives qui les construisent dans cette version).
