# Cahier de l'élève — Limites et continuité (`math_ch1_limites_continuite`)

Skill `cahier-de-l-eleve`, 18 novembre 2026. Le cahier idéal du chapitre, d'un seul tenant, dans l'ordre de la copie en attente (l'ordre de l'architecture). Les titres en chiffres romains sont ceux des parties du cours (`activities[].title`) : l'application les écrit d'elle-même en tête du bloc qui ouvre la partie ; les lignes du cahier portent la suite du plan (1., 2., a), b)…). Notation : `lim_{x→a}` s'écrit « lim » avec « x → a » dessous.

Programme : 2e Bac PC BIOF ; rien hors du cours. Les compléments propres au cours en ligne (rappels en séance 0, comparer deux racines, équation avec ∛, a³ − b³) sont en fin de fichier.

## Le cahier

**Limites et continuité**


### Ouverture — six questions sur une courbe


### I. Calculer une limite (rappel de 1re bac)

- Plan : limites, continuité, image d'un intervalle, valeurs intermédiaires, réciproque, ⁿ√.
- 1. Limite : lim_{x→1} (x² − 1)/(x − 1) = 2, même si f(1) n'existe pas.
- La limite est la valeur dont f(x) s'approche quand x s'approche de a.
- 2. Méthode : je remplace x par a. Un nombre → c'est le résultat ; « 0/0 » → je transforme.
- Exemple : lim_{x→1} (x² + 3x + 1) = 1 + 3 + 1 = 5.
- *[Figure — La limite en 1 : où mène le chemin] Les deux chemins mènent à la hauteur 2, mais le point (1 ; 2) manque : lim f(x) = 2 quand x → 1, même si f(1) n'existe pas.*
- 3. Formes indéterminées : 0/0 ; ∞/∞ ; +∞ − ∞ ; 0 × ∞.
- Indéterminée : résultat inconnu d'avance (trois « 0/0 » ont donné 2, 4 et 1/4).
- Devant une forme indéterminée, on transforme l'écriture, puis on remplace.
- Pas indéterminées : +∞ + ∞ = +∞ ; (−∞) × (−∞) = +∞ (règle des signes) ; k/∞ → 0.
- Attention : k/0 (k ≠ 0) donne un infini, son signe s'étudie à droite et à gauche.
- 4. Limites usuelles (n ∈ ℕ*) : lim_{x→+∞} xⁿ = +∞ ; lim_{x→+∞} √x = +∞.
- lim_{x→−∞} xⁿ = +∞ si n est pair, −∞ si n est impair ; lim_{x→±∞} 1/xⁿ = 0.
- ℓ ≠ 0 : ℓ × (±∞) = ±∞ (règle des signes). Exemple : lim_{x→−∞} (−2x³) = +∞.
- Rappel : a² − b² = (a − b)(a + b) ; exemple : x² − 9 = (x − 3)(x + 3).
- Rappel : si P(a) = 0, alors (x − a) est un facteur de P(x) : x² − 4x + 3 = (x − 3)(x − 1).
- *[Figure — Une racine a donne le facteur (x − a)] La parabole coupe l'axe en 1 et en 3 : P(1) = P(3) = 0, donc x² − 4x + 3 = (x − 1)(x − 3).*
- 5. Lever une forme indéterminée
- a) 0/0, polynômes : (x − a) en facteur. (x² − 9)/(x² − 4x + 3) = (x + 3)/(x − 1) → 3 en 3.
- b) 0/0 avec √ : multiplier haut et bas par le conjugué. (√(x + 3) − 2)/(x − 1) → 1/4 en 1.
- c) En ±∞ : quotient des termes de plus haut degré. lim_{x→+∞} (3x² + 1)/(x² − x) = 3.
- Attention : la règle du plus haut degré ne vaut qu'en +∞ ou en −∞, jamais en un réel a.
- Rappel : |x| est la distance de x à 0 ; √(x²) = |x| (x si x ≥ 0, −x si x ≤ 0).
- d) Racine en ±∞, même poids : le conjugué. lim_{x→+∞} (√(x² + x) − x) = 1/2.
- e) Racine en ±∞, poids différents : le plus lourd en facteur, avec √(x²) = |x|.
- Exemple en +∞ : √(x² + 1) − 3x = x(√(1 + 1/x²) − 3) ; la parenthèse → −2, donc → −∞.
- Attention : en −∞, √(x²) = |x| = −x.
- 6. Limite à droite (x → a⁺, x > a), à gauche (x → a⁻, x < a).
- lim_{x→1⁺} 1/(x − 1) = +∞ car x − 1 → 0⁺ ; lim_{x→1⁻} 1/(x − 1) = −∞ car x − 1 → 0⁻.
- Usuelles : lim_{x→0⁺} 1/x = +∞ ; lim_{x→0⁻} 1/x = −∞. Attention : jamais « k/0 » sans signe.
- 7. Interprétation géométrique ((C_f) : la courbe de f) :
- lim_{x→a} f(x) = ±∞ : la droite d'équation x = a est une asymptote verticale à (C_f).
- lim_{x→+∞} f(x) = ℓ : la droite y = ℓ est une asymptote horizontale à (C_f) au voisinage de +∞.
- *[Figure — Deux asymptotes] Limite infinie en 1 → asymptote verticale x = 1 ; limite 2 en ±∞ → asymptote horizontale y = 2.*
- 8. Limites de référence : lim_{x→0} sin(x)/x = 1 ; lim_{x→0} tan(x)/x = 1.
- lim_{x→0} (1 − cos x)/x² = 1/2.
- Avec sin(ax) : on fait apparaître sin(ax)/(ax) et on pose t = ax (t → 0).
- Exemple : sin(3x)/(2x) = (3/2) × sin(3x)/(3x), donc lim_{x→0} sin(3x)/(2x) = 3/2.
- Méthode : 1) je remplace ; 2) je nomme la forme ; 3) je choisis l'outil ; 4) j'interprète.
- Exemple : 1/(x − 1) − 2/(x² − 1) en 1 : « +∞ − ∞ », même dénominateur → 1/(x + 1) → 1/2.

### II. Continuité en un point

- 1. Définition : f est définie sur un intervalle ouvert I contenant a ;
- f est continue en a si lim_{x→a} f(x) = f(a) : la courbe arrive sur le point (a ; f(a)).
- Exemple : lim_{x→1} f(x) = 2 et f(1) = 3 : f n'est pas continue en 1 (la courbe saute).
- 2. Deux expressions : limite à droite avec la branche x > a, à gauche avec x < a.
- f(a) se calcule avec la branche qui porte l'égalité (x ≥ a ou x ≤ a).
- *[Figure — Pas continue en a : la courbe saute] La courbe arrive en ℓ par la gauche, mais le point (a ; f(a)) est ailleurs : lim f(x) ≠ f(a), f n'est pas continue en a.*
- 3. f est continue à droite en a si lim_{x→a⁺} f(x) = f(a) ;
- f est continue à gauche en a si lim_{x→a⁻} f(x) = f(a).
- Propriété : f est continue en a ⇔ f est continue à droite et à gauche en a.
- Exemple : 3x − 1 (x < 1), x² + m (x ≥ 1) : continue en 1 ⇔ 1 + m = 2 ⇔ m = 1.
- Méthode (bac) : 1) f(a) = … ; 2) ① lim_{x→a⁺} f(x) = f(a), donc f est continue à droite en a ;
- 3) ② lim_{x→a⁻} f(x) = f(a), continue à gauche ; 4) « d'après ① et ②, f est continue en a ».
- *[Figure — m = 1 soude la courbe en 1] Avec m = 1, la branche x² + m part de (1 ; 2), là où arrive 3x − 1 : la courbe est soudée, f est continue en 1.*

### III. Continuité sur un intervalle

- 1. f continue sur [a ; b] : continue sur ]a ; b[, à droite en a et à gauche en b.
- 2. Polynômes, |x|, sin, cos : continues sur ℝ ; √x : continue sur [0 ; +∞[.
- Rationnelles, tan : continues sur chaque intervalle de leur domaine de définition.
- 3. Somme, produit, αf de fonctions continues sur I : continues ; u/v si v(x) ≠ 0 sur I.
- 4. √u est continue sur I si u est continue sur I et (∀x ∈ I) u(x) ≥ 0.
- Attention : la positivité se prouve : x ≥ 2 ⇒ 3x − 6 ≥ 0 ; √(3x − 6) continue sur [2 ; +∞[.

### IV. Image d'un intervalle

- Fin du III — 5. Si lim_{x→a} u(x) = ℓ ≥ 0, alors lim_{x→a} √(u(x)) = √ℓ (a réel ou ±∞).
- Exemple : lim_{x→+∞} √(4 + 1/x) = √4 = 2.
- Rappel : f′ > 0 sur I ⇒ f strictement croissante ; f′ < 0 ⇒ f strictement décroissante.
- 1. Définition : l'image de I par f, notée f(I), est l'ensemble des f(x) pour x dans I.
- Exemple : f(x) = x² − 4x + 1 croît sur [2 ; 5] : f([2 ; 5]) = [f(2) ; f(5)] = [−3 ; 6].
- 2. f continue et strictement croissante sur [a ; b] : f([a ; b]) = [f(a) ; f(b)].
- f continue et strictement décroissante sur [a ; b] : f([a ; b]) = [f(b) ; f(a)].
- 3. Borne ouverte ou infinie → limite, crochet ouvert : f ↗, f([a ; +∞[) = [f(a) ; lim_{x→+∞} f(x)[.
- Exemple : g(x) = 4/x décroît sur ]0 ; 4] : g(]0 ; 4]) = [g(4) ; lim_{x→0⁺} g(x)[ = [1 ; +∞[.
- 4. f continue : l'image d'un intervalle est un intervalle (d'un segment, un segment).
- Non monotone sur [a ; b] : f([a ; b]) = [m ; M], m et M lus dans le tableau de variations.
- *[Figure — Image de [1 ; 3] par f croissante] Quand x parcourt [1 ; 3], f(x) monte de f(1) = 2 à f(3) = 7 : f([1 ; 3]) = [2 ; 7] (en jaune sur les axes).*
- *[Figure — h(x) = x³ − 3x sur [−2 ; 2]] h n'est pas monotone : m = −2 et M = 2 se lisent dans le tableau, donc h([−2 ; 2]) = [−2 ; 2].*

### V. Le théorème des valeurs intermédiaires

- 1. Résoudre f(x) = 0, c'est trouver où (C_f) coupe l'axe des abscisses.
- f continue sur [a ; b], f(a) < 0 et f(b) > 0 : la courbe coupe l'axe en un point α.
- Condition 1 : f continue sur [a ; b] (sinon la courbe peut sauter par-dessus l'axe).
- Condition 2 : f(a) et f(b) de signes contraires, c'est-à-dire f(a) × f(b) < 0.
- *[Figure — La courbe coupe l'axe en α] f continue sur [a ; b] passe de f(a) < 0 à f(b) > 0 : la courbe coupe l'axe des abscisses en α, solution de f(x) = 0.*
- 2. Théorème des valeurs intermédiaires (TVI) : f continue sur [a ; b] et f(a) × f(b) < 0
- ⇒ l'équation f(x) = 0 admet au moins une solution dans ]a ; b[.
- 3. Si de plus f est strictement monotone sur [a ; b] : solution unique α dans ]a ; b[.
- Méthode : 1) Posons f(x) = … ; 2) f continue sur [a ; b] car … ; 3) f strictement monotone car …
- 4) f(a) × f(b) < 0 ; 5) d'après le TVI, f(x) = 0 a une solution unique α dans ]a ; b[.
- Attention : « au moins une » ≠ « unique » ; α ∈ ]a ; b[ (ouvert) ; le TVI ne donne pas α.
- *[Figure — « Au moins une » solution] f(a) × f(b) < 0 garantit au moins une solution dans ]a ; b[ ; ici la courbe coupe l'axe trois fois.*
- 4. f continue sur [a ; b], k entre f(a) et f(b) : f(x) = k a au moins une solution.
- Méthode : poser h(x) = f(x) − k et appliquer le TVI à h(x) = 0.
- 5. f continue, strictement monotone sur I, k ∈ f(I) : f(x) = k a une solution unique dans I.
- Exemple : x³ + x − 1 : f(ℝ) = ℝ (limites), 0 ∈ f(ℝ) ; f(0) < 0 < f(1), donc 0 < α < 1.
- 6. α solution de f(x) = 0 : f(α) = 0, puis on isole (α³ + α − 1 = 0, donc α³ = 1 − α).
- Signe : f croissante ⇒ f(x) < 0 pour x < α et f(x) > 0 pour x > α.
- *[Figure — f(x) = k : la droite y = k coupe la courbe] k est entre f(a) et f(b) : la droite y = k coupe la courbe, f(x) = k a au moins une solution c dans [a ; b].*

### VI. La fonction réciproque

- 1. f⁻¹ défait ce que f a fait : f(2) = 5 ⇔ f⁻¹(5) = 2 (f(x) = x² + 1 sur [0 ; +∞[).
- Attention : f⁻¹ n'est pas 1/f.
- 2. Théorème : si f est continue et strictement monotone sur un intervalle I,
- alors f admet une fonction réciproque f⁻¹ définie sur l'intervalle J = f(I).
- Exemple : x² sur ℝ : 4 a deux antécédents ; on restreint à [0 ; +∞[ (un seul).
- 3. (∀x ∈ I) f⁻¹(f(x)) = x ; (∀x ∈ J) f(f⁻¹(x)) = x.
- *[Figure — x² sur ℝ : deux antécédents de 4] Sur ℝ, 4 a deux antécédents, −2 et 2 : pas de réciproque. Sur [0 ; +∞[ (en jaune), x² est strictement croissante : un seul.*
- Méthode (bac) : g continue sur I car … ; g strictement monotone sur I car (signe de g′) ;
- donc g admet une fonction réciproque g⁻¹ définie sur un intervalle J = g(I) = …
- Exemple : g(x) = x² − 2x − 1 sur [1 ; +∞[ : J = [g(1) ; lim_{x→+∞} g(x)[ = [−2 ; +∞[.
- 4. f⁻¹ est continue sur J et a le même sens de variation que f.
- 5. Repère orthonormé : (C_f⁻¹) et (C_f) symétriques par rapport à la droite d'équation y = x.
- M(a ; b) ∈ (C_f) ⇔ M′(b ; a) ∈ (C_f⁻¹).
- *[Figure — Le miroir y = x] M(2 ; 5) sur (C_f) donne M′(5 ; 2) sur la courbe de f⁻¹ : les deux courbes sont symétriques par rapport à y = x.*
- Méthode (tracer (C_f⁻¹)) : 1) la droite y = x ; 2) les points, coordonnées échangées ;
- 3) une asymptote verticale x = a devient l'asymptote horizontale y = a ; 4) relier.
- 6. Expression : pour x ∈ J et y ∈ I, f⁻¹(x) = y ⇔ f(y) = x ; on isole y.
- Exemple : f(x) = √(x − 1), J = [0 ; +∞[ : √(y − 1) = x ⇔ y = x² + 1 ; f⁻¹(x) = x² + 1.
- Exemple : x² + 2x − 3 sur ]−1 ; +∞[, J = ]−4 ; +∞[ : (y + 1)² = x + 4 (forme canonique) ;
- |y + 1| = √(x + 4) et y + 1 > 0, donc f⁻¹(x) = √(x + 4) − 1. Attention : √(A²) = |A|.

### VII. Racine n-ième et puissances rationnelles

- 1. Racine n-ième (n ∈ ℕ*) : ⁿ√ est la réciproque de x ↦ xⁿ sur [0 ; +∞[.
- Définition : ⁿ√x = y ⇔ x = yⁿ (x ≥ 0, y ≥ 0). Exemple : ∛8 = 2 car 2³ = 8 ; √x = ²√x.
- 2. Règles (x ≥ 0, y ≥ 0) : ⁿ√x × ⁿ√y = ⁿ√(xy) ; ⁿ√x/ⁿ√y = ⁿ√(x/y) (y > 0).
- (ⁿ√x)ⁿ = ⁿ√(xⁿ) = x ; ⁿ√(ᵐ√x) = ⁿᵐ√x ; ⁿᵐ√(xᵐ) = ⁿ√x ; ⁿ√x = ⁿ√y ⇔ x = y.
- Remarque : au programme, rien de négatif sous ⁿ√, même si n est impair.
- *[Figure — x³ et ∛x : le miroir y = x] Sur [0 ; +∞[, la courbe de ∛x est la symétrique de celle de x³ par rapport à y = x : (2 ; 8) ↔ (8 ; 2), car ∛8 = 2.*
- Méthode (simplifier) : tout en puissances d'un même nombre, réduire l'indice, regrouper.
- Exemple : 9 = 3², 81 = 3⁴ : (⁴√9 × √9)/⁸√81 = (√3 × 3)/√3 = 3.
- 3. Équation xⁿ = a, n pair : a > 0 → x = ⁿ√a ou x = −ⁿ√a ; a < 0 → pas de solution.
- n impair : a > 0 → x = ⁿ√a ; a < 0 → x = −ⁿ√(−a). x⁴ = 16 ⇔ x = ±2 ; x³ = −27 ⇔ x = −3.
- Attention : d'abord la parité de n, ensuite le signe de a.
- 4. Puissances rationnelles (x > 0) : x^(1/n) = ⁿ√x. Exemple : 8^(1/3) = ∛8 = 2.
- x^(p/q) = ᑫ√(xᵖ) (p ∈ ℤ, q ∈ ℕ*) : le dénominateur est l'indice. Ex. : 8^(2/3) = ∛64 = 4.
- Règles (x > 0, y > 0 ; r, s ∈ ℚ) : x^r × x^s = x^(r+s) ; (x^r)^s = x^(rs) ; x^r/x^s = x^(r−s).
- (xy)^r = x^r × y^r ; 1/x^r = x^(−r). Exemple : ∛4 × 2^(1/3) × √2 = 2^(3/2) = 2√2.
- Attention : x^(1/n) n'est pas 1/xⁿ.

### VIII. Limites et continuité avec ⁿ√u

- 1. ⁿ√u est continue sur I si u est continue sur I et (∀x ∈ I) u(x) ≥ 0.
- 2. lim u = ℓ ≥ 0 ⇒ lim ⁿ√u = ⁿ√ℓ ; lim u = +∞ ⇒ lim ⁿ√u = +∞ (même règle que √u).
- Exemple : lim_{x→+∞} (∛(x + 1) + √x) = +∞ (« +∞ + ∞ », pas d'indétermination).
- 3. « +∞ − ∞ » avec des racines : comparer les poids, mettre le plus lourd en facteur.
- Exemple : ∛(x² − x) − x = x(∛(1/x − 1/x²) − 1) en +∞ ; la parenthèse → −1, donc → −∞.

### IX. Un problème national, question par question, et le bilan

- Problème : f(x) = x³ + x − 1. 1) lim_{x→−∞} f(x) = −∞ ; lim_{x→+∞} f(x) = +∞ (terme x³).
- 2) f′(x) = 3x² + 1 > 0 car x² ≥ 0 : f strictement croissante sur ℝ ; tableau : −∞ ↗ +∞.
- 3) f continue, strictement croissante sur ℝ, 0 ∈ f(ℝ) = ℝ : solution unique α dans ℝ.
- f(1/2) = −3/8 < 0 et f(1) = 1 > 0, donc 1/2 < α < 1.
- 4) f admet une fonction réciproque f⁻¹ définie sur J = f(ℝ) = ℝ.
- (C_f⁻¹) : symétrique de (C_f) par rapport à y = x ; A(0 ; −1) ∈ (C_f) donne A′(−1 ; 0).
- *[Figure — x³ + x − 1 coupe l'axe une seule fois] f est continue et strictement croissante ; f(1/2) < 0 < f(1) : une seule traversée, en α, avec 1/2 < α < 1.*
- Bilan — une question du bac, sa liste de conditions :
- Limite : remplacer, nommer la forme, choisir l'outil, interpréter (asymptote).
- Continue en a : lim_{x→a} f(x) = f(a) (deux expressions : à droite et à gauche).
- Solution unique : continue + strictement monotone + f(a) × f(b) < 0 (ou 0 ∈ f(I)).
- Réciproque : continue + strictement monotone sur I ⇒ f⁻¹ définie sur J = f(I), même sens.
- Courbe de f⁻¹ : symétrique de (C_f) par rapport à la droite d'équation y = x.

## Méthodes des cas types du national (où elles sont écrites)

- Calculer une limite : remplacer → nommer la forme → choisir l'outil → interpréter (I.2, I.5, I.8, phrase I.7).
- Continuité d'une fonction à deux expressions, valeur du paramètre m : f(a), ①, ②, « d'après ① et ② » (II.3).
- Continuité sur I : fonctions usuelles, opérations, √u avec la positivité prouvée (III.2-4).
- Image d'un intervalle : sens de variation, borne fermée → image, ouverte → limite (IV.2-4).
- Solution unique α : Posons f(x) ; continue ; strictement monotone ; f(a) × f(b) < 0 ; d'après le TVI (V.3).
- Solution unique sur ℝ ou ]0 ; +∞[ : f(I) par les limites, 0 ∈ f(I), puis encadrement (V.5).
- Utiliser α : f(α) = 0 puis isoler ; signe de f avant et après α (V.6).
- Réciproque définie sur J : continue + strictement monotone, J = f(I) (VI.2, méthode bac).
- Construire (C_f⁻¹) : y = x, points échangés, asymptotes échangées (VI.5).
- Expression de f⁻¹(x) : ligne pivot, forme canonique, racine justifiée, |A| levée (VI.6).
- Racines n-ièmes : simplifier, xⁿ = a (VII.2-3) ; puissances rationnelles (VII.4) ; limites avec ⁿ√u (VIII).

## Compléments propres au cours en ligne

- Rappels de 1re bac (séance 0) : a) a² − b² ; b) signe de x − a ; c) signe de f′ ; d) √(x²) = |x| ; e) racine → facteur (x − a).
- VII.2 : x < y ⇔ ⁿ√x < ⁿ√y ; comparer deux racines : même indice d'abord (diapositive n5).
- VII.3 : équation avec une racine : condition, puissance n, résoudre, vérifier (diapositive n7).
- VIII : complément de devoir a³ − b³ = (a − b)(a² + ab + b²), lim_{x→0} (∛(x + 8) − 2)/x = 1/12 (diapositives lr2, lr3).

## Découpage

Chaque bloc : 3 à 6 lignes (jamais autant de lignes que de diapositives, sinon le tableau du cahier range une ligne sous chaque titre de diapositive), 0 à 2 figures. Les bulles de diapositive (`concentration.cahier`) gardent la trace de leur diapositive en une ou deux phrases.

### Copie en attente

| Bloc | Diapositives | Lignes | Figures du bloc |
|---|---|---|---|
| `lc_s1_b1` | o1_carte, l1_chemin, l2_remplacer | 5 (« Plan : limites, continuité, image d'un intervall… ») | La limite en 1 : où mène le chemin |
| `lc_s1_b2` | l3_zero_sur_zero, l4_formes, l4_formes_b | 5 (« 3. Formes indéterminées : 0/0 ; ∞/∞ ; +∞ − ∞ ; 0… ») | — |
| `lc_s1_b3` | l4c_usuelles, z1_factoriser, z5_racine_facteur | 5 (« 4. Limites usuelles (n ∈ ℕ*) : lim_{x→+∞} xⁿ = +… ») | Une racine a donne le facteur (x − a) |
| `lc_s1_b4` | l5_facteur, l6_conjugue, l7_plus_lourd | 5 (« 5. Lever une forme indéterminée… ») | — |
| `lc_s2_b1` | z4_valeur_absolue, l8_racine_infini, l8_racine_infini_b | 5 (« Rappel : \|x\| est la distance de x à 0 ; √(x²) = … ») | — |
| `lc_s2_b2` | l9_deux_cotes, l10_signe, l11_interpreter | 6 (« 6. Limite à droite (x → a⁺, x > a), à gauche (x … ») | Deux asymptotes |
| `lc_s2_b3` | l12_sinus, l12_sinus_b, l13_devoir | 6 (« 8. Limites de référence : lim_{x→0} sin(x)/x = 1… ») | — |
| `lc_s2_b4` | c1_soudee, c2_limite_image, c3_deux_branches | 5 (« 1. Définition : f est définie sur un intervalle … ») | Pas continue en a : la courbe saute |
| `lc_s3_b0` | c4_parametre, c4b_droite_gauche, c5_redaction, c5b_parametre | 6 (« 3. f est continue à droite en a si lim_{x→a⁺} f(… ») | m = 1 soude la courbe en 1 |
| `lc_s3_b1` | i1_usuelles, i2_operations, i3_racine_u | 6 (« 1. f continue sur [a ; b] : continue sur ]a ; b[… ») | — |
| `lc_s3_b2` | i4_composee, z3_derivee, j1_hauteurs | 5 (« Fin du III — 5. Si lim_{x→a} u(x) = ℓ ≥ 0, alors… ») | — |
| `lc_s3_b3` | j2_croissante, j3_decroissante, j4_borne_ouverte, j5_non_monotone | 6 (« 2. f continue et strictement croissante sur [a ;… ») | Image de [1 ; 3] par f croissante ; h(x) = x³ − 3x sur [−2 ; 2] |
| `lc_s4_b1` | t1_couper_axe, t2_continue, t3_produit | 4 (« 1. Résoudre f(x) = 0, c'est trouver où (C_f) cou… ») | La courbe coupe l'axe en α |
| `lc_s4_b2` | t4_au_moins_une, t5_unique, t6_rediger | 6 (« 2. Théorème des valeurs intermédiaires (TVI) : f… ») | « Au moins une » solution |
| `lc_s4_b3` | t7_valeur_k, t8_intervalle_ouvert, t9_f_alpha | 6 (« 4. f continue sur [a ; b], k entre f(a) et f(b) … ») | f(x) = k : la droite y = k coupe la courbe |
| `lc_s5_b1` | r1_aller_retour, r2_strictement_monotone, r3_J | 6 (« 1. f⁻¹ défait ce que f a fait : f(2) = 5 ⇔ f⁻¹(5… ») | x² sur ℝ : deux antécédents de 4 |
| `lc_s5_b2` | r4_deux_lignes, r5_sens, r6_miroir | 6 (« Méthode (bac) : g continue sur I car … ; g stric… ») | Le miroir y = x |
| `lc_s5_b3` | r7_construire, r8_expression, r9_valeur_absolue, r9_valeur_absolue_b | 6 (« Méthode (tracer (C_f⁻¹)) : 1) la droite y = x ; … ») | — |
| `lc_s6_b1` | n1_defaire, n2_reciproque_xn, n3_regles | 5 (« 1. Racine n-ième (n ∈ ℕ*) : ⁿ√ est la réciproque… ») | x³ et ∛x : le miroir y = x |
| `lc_s6_b2` | n4_simplifier, n6_equation, n6_equation_b | 5 (« Méthode (simplifier) : tout en puissances d'un m… ») | — |
| `lc_s6_b3` | p1_exposant, p2_pq, p3_regles_puissances | 5 (« 4. Puissances rationnelles (x > 0) : x^(1/n) = ⁿ… ») | — |
| `lc_s6_b4` | lr1_continuite, lr4_infini | 5 (« 1. ⁿ√u est continue sur I si u est continue sur … ») | — |
| `lc_s7_b1` | e1_probleme, e1_probleme_b, e1_probleme_b2, e1_probleme_unique, e1_probleme_tvi, e1_probleme_c, e1_probleme_d | 6 (« Problème : f(x) = x³ + x − 1. 1) lim_{x→−∞} f(x)… ») | x³ + x − 1 coupe l'axe une seule fois |
| `lc_s7_b4` | e2_bilan, e3_carte | 6 (« Bilan — une question du bac, sa liste de conditi… ») | — |

Figures de diapositive : `lc_z5_racine_facteur` (Une racine a donne le facteur (x − a)) ; `lc_l1_chemin` (La limite en 1 : où mène le chemin) ; `lc_l10_signe` (1/(x − 1) à droite et à gauche de 1) ; `lc_l11_interpreter` (Deux asymptotes) ; `lc_c1_soudee` (Pas continue en a : la courbe saute) ; `lc_c4_parametre` (m = 1 soude la courbe en 1) ; `lc_j2_croissante` (Image de [1 ; 3] par f croissante) ; `lc_j5_non_monotone` (h(x) = x³ − 3x sur [−2 ; 2]) ; `lc_t1_couper_axe` (La courbe coupe l'axe en α) ; `lc_t4_au_moins_une` (« Au moins une » solution) ; `lc_t7_valeur_k` (f(x) = k : la droite y = k coupe la courbe) ; `lc_r2_strictement_monotone` (x² sur ℝ : deux antécédents de 4) ; `lc_r6_miroir` (Le miroir y = x) ; `lc_n2_reciproque_xn` (x³ et ∛x : le miroir y = x) ; `lc_e1_probleme_tvi` (x³ + x − 1 coupe l'axe une seule fois).

### Cours en ligne

| Bloc | Diapositives | Lignes | Figures du bloc |
|---|---|---|---|
| `lc_s0_b1` | o1_carte, z1_factoriser, z2_signe | 4 (« Plan : limites, continuité, image d'un intervall… ») | — |
| `lc_s0_b2` | z3_derivee, z4_valeur_absolue, z5_racine_facteur | 4 (« c) f′ > 0 sur I ⇒ f strictement croissante ; f′ … ») | Une racine a donne le facteur (x − a) |
| `lc_s1_b1` | l1_chemin, l2_remplacer, l3_zero_sur_zero | 5 (« 1. Limite : lim_{x→1} (x² − 1)/(x − 1) = 2, même… ») | La limite en 1 : où mène le chemin |
| `lc_s1_b2` | l4_formes, l4_formes_b, l4c_usuelles, l5_facteur | 6 (« 3. Formes indéterminées : 0/0 ; ∞/∞ ; +∞ − ∞ ; 0… ») | — |
| `lc_s1_b3` | l6_conjugue, l7_plus_lourd, l8_racine_infini | 4 (« b) 0/0 avec √ : multiplier haut et bas par le co… ») | — |
| `lc_s2_b1` | l8_racine_infini_b, l9_deux_cotes, l10_signe | 5 (« e) Poids différents : le plus lourd en facteur ;… ») | 1/(x − 1) à droite et à gauche de 1 |
| `lc_s2_b2` | l11_interpreter, l12_sinus, l12_sinus_b, l13_devoir | 6 (« 7. Interprétation ((C_f) : courbe de f) : lim_{x… ») | Deux asymptotes |
| `lc_s2_b3` | c1_soudee, c2_limite_image, c3_deux_branches | 5 (« 1. Définition : f est définie sur un intervalle … ») | Pas continue en a : la courbe saute |
| `lc_s3_b1` | c4_parametre, c4b_droite_gauche, c5_redaction, i1_usuelles | 6 (« Fin du II — 3. Continue à droite en a : lim_{x→a… ») | m = 1 soude la courbe en 1 |
| `lc_s3_b2` | i2_operations, i3_racine_u, i4_composee | 4 (« 3. Somme, produit, αf de fonctions continues sur… ») | — |
| `lc_s3_b3` | j1_hauteurs, j2_croissante, j3_decroissante | 4 (« 1. Définition : l'image de I par f, notée f(I), … ») | Image de [1 ; 3] par f croissante |
| `lc_s4_b1` | j4_borne_ouverte, j5_non_monotone, t1_couper_axe, t2_continue | 5 (« Fin du IV — 3. Borne ouverte ou infinie → limite… ») | h(x) = x³ − 3x sur [−2 ; 2] ; La courbe coupe l'axe en α |
| `lc_s4_b2` | t3_produit, t4_au_moins_une, t5_unique | 5 (« Condition 2 : f(a) et f(b) de signes contraires,… ») | « Au moins une » solution |
| `lc_s4_b3` | t6_rediger, t7_valeur_k, t8_intervalle_ouvert, t9_f_alpha | 6 (« Méthode : 1) Posons f(x) = … ; 2) f continue sur… ») | f(x) = k : la droite y = k coupe la courbe |
| `lc_s5_b2` | r1_aller_retour, r2_strictement_monotone, r3_J, r4_deux_lignes | 6 (« 1. f⁻¹ défait ce que f a fait : f(2) = 5 ⇔ f⁻¹(5… ») | x² sur ℝ : deux antécédents de 4 |
| `lc_s5_b3` | r5_sens, r6_miroir, r7_construire | 5 (« 4. f⁻¹ est continue sur J et a le même sens de v… ») | Le miroir y = x |
| `lc_s6_b1` | r8_expression, r9_valeur_absolue, r9_valeur_absolue_b, n1_defaire | 5 (« Fin du VI — 6. f⁻¹(x) = y ⇔ f(y) = x (x ∈ J, y ∈… ») | — |
| `lc_s6_b2` | n2_reciproque_xn, n3_regles, n4_simplifier | 4 (« Définition : ⁿ√, réciproque de x ↦ xⁿ sur [0 ; +… ») | x³ et ∛x : le miroir y = x |
| `lc_s6_b3` | n5_comparer, n6_equation, n6_equation_b, n7_equation_racine | 5 (« x < y ⇔ ⁿ√x < ⁿ√y (x ≥ 0, y ≥ 0). Comparer deux … ») | — |
| `lc_s7_b1` | p1_exposant, p2_pq, p3_regles_puissances | 5 (« 4. Puissances rationnelles (x > 0) : x^(1/n) = ⁿ… ») | — |
| `lc_s7_b2` | lr1_continuite, lr2_cle_de_trois, lr3_zero_sur_zero, lr4_infini | 5 (« 1. ⁿ√u est continue sur I si u est continue sur … ») | — |
| `lc_s7_b3` | e1_probleme, e1_probleme_b, e1_probleme_c | 6 (« Problème type : f(x) = x³ + x − 1 sur ℝ.… ») | x³ + x − 1 coupe l'axe une seule fois |
| `lc_s7_b4` | e2_bilan, e3_carte | 6 (« Bilan — une question du bac, sa liste de conditi… ») | — |

Figures de diapositive : `lc_z5_racine_facteur` (Une racine a donne le facteur (x − a)) ; `lc_l1_chemin` (La limite en 1 : où mène le chemin) ; `lc_l10_signe` (1/(x − 1) à droite et à gauche de 1) ; `lc_l11_interpreter` (Deux asymptotes) ; `lc_c1_soudee` (Pas continue en a : la courbe saute) ; `lc_c4_parametre` (m = 1 soude la courbe en 1) ; `lc_j2_croissante` (Image de [1 ; 3] par f croissante) ; `lc_j5_non_monotone` (h(x) = x³ − 3x sur [−2 ; 2]) ; `lc_t1_couper_axe` (La courbe coupe l'axe en α) ; `lc_t4_au_moins_une` (« Au moins une » solution) ; `lc_t7_valeur_k` (f(x) = k : la droite y = k coupe la courbe) ; `lc_r2_strictement_monotone` (x² sur ℝ : deux antécédents de 4) ; `lc_r6_miroir` (Le miroir y = x) ; `lc_n2_reciproque_xn` (x³ et ∛x : le miroir y = x) ; `lc_e1_probleme_b` (x³ + x − 1 coupe l'axe une seule fois).

