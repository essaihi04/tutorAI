# Le cahier de l'élève — `phys_ch4_radioactivite` (Décroissance radioactive)

18 novembre 2026, skill `cahier-de-l-eleve`. Ce fichier est le **cahier idéal du chapitre**, écrit d'un seul tenant, puis
découpé dans `blocs[].cahier`, `blocs[].cahier_figures`, `concentration.cahier`, `concentration.cahier_figures` du cours
en ligne (`backend/data/courses/phys_ch4_radioactivite.json`) et de sa copie en attente
(`backend/data/courses/en_attente/phys_ch4_radioactivite.json`). Aucun autre champ n'a été touché.

## Règles de mise en page suivies

- Les **parties I, II, III…** sont les titres des `activities` (le lecteur les écrit en rose en tête du bloc où elles
  commencent) ; le cahier numérote dedans **1., 2., 3.…**, en continu d'un bloc à l'autre, et repart à 1 à chaque partie.
- Chaque bloc a **3 à 6 lignes** (une idée par ligne) et **0 à 2 figures** ; son nombre de lignes est toujours
  **différent** de son nombre de diapositives : sinon `TableauCahier` range chaque ligne sous le titre numéroté d'une
  diapositive, ce qui doublerait la numérotation et casserait le plan.
- Étiquettes : « Définition : » (mot pour mot comme la diapositive), « Méthode « … » : 1) 2) 3) » (cas types du
  national, `exploration/radioactivite.json`), « Attention : » (erreurs des copies, `erreurs_examen`), « Remarque : »,
  « Exemple : », « Rappel : » (outil de maths juste avant son usage).
- La bulle de chaque diapositive (`concentration.cahier`) : la trace de cette diapositive en une ou deux lignes.

## Le plan du cahier (copie en attente, ordre de la nouvelle logique)

- **I. Le noyau et sa stabilité** : 1. Le noyau (nucléons) · 2. Notation ᴬ_Z X, N = A − Z · méthode « composition » ·
  3. Isotopes, nucléide · 4. Diagramme (N, Z) · 5. Vallée de stabilité, isotopes sur une verticale.
- **II. La radioactivité et les désintégrations** : 1. Définition · 2. Aléatoire, spontanée, inéluctable · 3. Lois de
  Soddy · 4. α, β⁻, β⁺, γ, pénétration · 5. Méthodes « équation » et « type ».
- **III. Les désintégrations sur le diagramme, la famille** : 1. Déplacements β⁻, β⁺, α · 2. Prévoir le type (zones) ·
  3. Famille radioactive, lire une flèche, méthode « famille » (x, y).
- **IV. Compter les noyaux, puis la loi de décroissance** : 1. La moitié tous les 8 jours, définition de t½, méthode
  « lire t½ » · 2. Même proportion, −dN = λ·N·dt, dN/dt + λ·N = 0 · 3. Loi N(t) = N₀·e^(−λt), λ et ses unités ·
  4. Désintégrés N_d · 5. τ = 1/λ, méthode « lire τ » (tangente, 37 %) · 6. t½ = ln2/λ (établir), N₀/2ⁿ, pourcentages.
- **V. L'activité et la datation** : 1. Activité, Bq, a = λ·N, a(t) · 2. λ en s⁻¹ · 3. N = (m/M)·N_A, masse ·
  4. Méthode « courbe a(t) » · 5. Méthode « droite ln N » · 6. Datation au carbone 14, méthode « âge » · 7. Roche, r.
- **VI. Exercices du national** : 1. Le mot de la question donne la méthode ; 2022 R, 2021 N, 2022 N, 2025 N.
- **VII. Bilan** : les formules du chapitre, la phrase de la carte.

## Le cahier idéal (copie en attente)

### I. Le noyau et sa stabilité

*Bloc `ra_s1_b1` — L'atome, le noyau et sa notation*

- 1. Le noyau : des protons (charge +e) et des neutrons (charge nulle), appelés nucléons.
- Autour du noyau, très petit, se trouvent les électrons (charge −e) ; presque toute la masse est dans le noyau.
- 2. Notation ᴬ_Z X : X symbole de l'élément ; Z nombre de charge (protons) ; A nombre de nucléons.
- N = A − Z : nombre de neutrons. Exemple : ¹⁴₆C a Z = 6 protons, N = 8 neutrons, A = 14 nucléons.
- Attention : A en haut, Z en bas ; ne pas confondre A (nucléons) et N (neutrons).

*Bloc `ra_s1_b2` — Composition, isotopes, le diagramme (N, Z)*

- Méthode « composition » : Z protons ; N = A − Z neutrons (²³⁸₉₂U : 92 et 146).
- 3. Définition : des isotopes sont des noyaux de même nombre de charge Z et de nombres de nucléons A différents.
- Exemples : ¹²₆C et ¹⁴₆C ; ¹H, ²H, ³H. Nucléide : noyaux de même A et de même Z.
- 4. Diagramme (N, Z) : Z en abscisse, N en ordonnée ; un nucléide = un point (Z ; N).

*Bloc `ra_s1_b3` — La vallée de stabilité, les isotopes sur le diagramme*

- 5. Vallée de stabilité : bande des noyaux stables ; légers (Z < 20) : N ≈ Z ; lourds : N > Z.
- Hors de la vallée : noyau instable. Attention : être sur la droite N = Z ne suffit pas.
- Les isotopes d'un élément sont sur une même droite perpendiculaire à l'axe des Z.
- ¹²C est dans la vallée (stable) ; ¹⁴C est au-dessus (trop de neutrons) : instable.
- 🖉 **La vallée de stabilité** — Les noyaux stables forment la vallée (N ≈ Z pour les légers, N > Z pour les lourds) ; les isotopes sont sur une même verticale.


### II. La radioactivité et les désintégrations

*Bloc `ra_s2_b1` — La radioactivité et ses caractères*

- 1. Définition : la radioactivité est la transformation spontanée d'un noyau instable (père) en un noyau plus stable (fils), avec émission d'une particule.
- Noyau père → noyau fils + particule ; le fils est plus stable, pas forcément stable.
- 2. Elle est aléatoire : on ne peut prévoir ni quel noyau se désintègre, ni à quel instant.
- Elle est spontanée et inéluctable : température, pression, liaisons chimiques n'y changent rien.

*Bloc `ra_s2_b2` — Les lois de Soddy, α et β⁻*

- 3. Lois de Soddy, pour ᴬ_Z X → ᴬ¹_Z₁ Y + ᴬ²_Z₂ P : A = A₁ + A₂ et Z = Z₁ + Z₂.
- Remarque : on conserve la charge Z, pas le nombre de protons (un neutron peut devenir proton).
- 4. α (noyaux lourds) : ᴬ_Z X → ᴬ⁻⁴_Z₋₂ Y + ⁴₂He ; ex. ²¹⁰₈₄Po → ²⁰⁶₈₂Pb + ⁴₂He.
- β⁻ : ¹₀n → ¹₁p + ⁰₋₁e ; ᴬ_Z X → ᴬ_Z₊₁ Y + ⁰₋₁e ; ex. ¹⁴₆C → ¹⁴₇N + ⁰₋₁e.
- Attention : l'électron β⁻ est créé dans le noyau, qui ne contient pas d'électron.

*Bloc `ra_s2_b3` — β⁺, γ, le noyau fils et le type*

- β⁺ : ¹₁p → ¹₀n + ⁰₁e (positon) ; ᴬ_Z X → ᴬ_Z₋₁ Y + ⁰₁e ; ex. ³⁰₁₅P → ³⁰₁₄Si + ⁰₁e.
- γ : désexcitation du fils excité, ᴬ_Z Y* → ᴬ_Z Y + γ ; A et Z ne changent pas.
- Pénétration : α arrêtée par du papier, β par quelques mm d'aluminium, γ par du plomb.
- 5. Méthode « équation » : 1) écrire ᴬ_Z Y inconnu ; 2) « d'après les lois de Soddy » : A puis Z ; 3) Z donne l'élément (tableau).
- Méthode « type » : Soddy donne A et Z de la particule : ⁴₂He → α ; ⁰₋₁e → β⁻ ; ⁰₁e → β⁺.
- Exemple (2021 R) : ³²₁₅P → ³²₁₆S + ⁰₋₁e : β⁻.


### III. Les désintégrations sur le diagramme, la famille

*Bloc `ra_s3_b1` — Chaque désintégration sur le diagramme*

- 1. Sur le diagramme (N, Z), chaque désintégration rapproche le noyau de la vallée.
- β⁻ : Z + 1 et N − 1 ; β⁺ : Z − 1 et N + 1 (A ne change pas) ; α : Z − 2 et N − 2 (A − 4).
- 2. Prévoir le type : au-dessus de la vallée (trop de neutrons) → β⁻ ;
- au-dessous (trop de protons) → β⁺ ; noyaux lourds (en haut à droite) → α.
- 🖉 **Le noyau redescend vers la vallée** — β⁻ : Z + 1 et N − 1 ; β⁺ : Z − 1 et N + 1 ; α : Z − 2 et N − 2.
- 🖉 **Le diagramme (N, Z) et ses zones** — Au-dessus de la vallée (trop de neutrons) : β⁻ ; au-dessous (trop de protons) : β⁺ ; noyaux lourds : α.

*Bloc `ra_s3_b2` — La famille radioactive*

- 3. Définition : une famille radioactive est une suite de désintégrations d'un noyau père jusqu'à un noyau stable.
- Exemple : ²³⁸₉₂U → … → ²⁰⁶₈₂Pb (stable) : 8 désintégrations α et 6 désintégrations β⁻.
- Lire une flèche : A − 4 et Z − 2 → α ; A constant, Z + 1 → β⁻ ; A constant, Z − 1 → β⁺.
- Méthode « famille » : ᴬ_Z X → ᴬ'_Z' Y + y ⁴₂He + x ⁰₋₁e ; 1) A = A' + 4y donne y ; 2) Z = Z' + 2y − x donne x.
- Vérifier : 238 = 206 + 4 × 8 et 92 = 82 + 2 × 8 − 6.


### IV. Compter les noyaux, puis la loi de décroissance

*Bloc `ra_s3_b3` — Beaucoup de noyaux : on compte, la demi-vie*

- Rappel : 10ⁿ = 1 suivi de n zéros (1,19·10⁷ = 11 900 000) ; 10⁻³ = 0,001 ; 2·10⁻⁶ g = 0,000 002 g.
- 1. Iode 131 : N₀ = 400 noyaux ; à 8, 16, 24 jours il en reste 200, 100, 50 : N est divisé par 2 tous les 8 jours.
- Définition : la demi-vie t½ est la durée au bout de laquelle la moitié des noyaux initialement présents s'est désintégrée.
- N(t½) = N₀/2 ; t½ est propre au nucléide, sans dépendre de N₀ (iode 131 : 8 jours ; carbone 14 : 5730 ans).
- Méthode « lire t½ » : 1) lire N₀ ; 2) placer N₀/2 sur l'axe des N ; 3) aller à la courbe ; 4) descendre sur l'axe des t.
- 🖉 **Iode 131 : la moitié tous les 8 jours** — 400, 200, 100, 50 noyaux à 0, 8, 16, 24 jours : la demi-vie de l'iode 131 est t½ = 8 jours.

*Bloc `ra_s4_b1` — La même proportion, l'équation, l'exponentielle*

- 2. Pendant une même durée, la même proportion de noyaux se désintègre (≈ 8 % par jour pour l'iode 131).
- Noyaux désintégrés pendant dt : −dN = λ·N·dt (λ : constante radioactive, en s⁻¹).
- Équation différentielle : dN/dt + λ·N = 0.
- Rappel : e⁰ = 1 ; e^(−x) diminue quand x augmente et tend vers 0 sans jamais l'atteindre.
- 🖉 **L'exponentielle qui décroît** — e⁰ = 1 ; quand x augmente, e^(−x) diminue et s'approche de 0 sans jamais l'atteindre.

*Bloc `ra_s4_b2` — ln, la loi, λ*

- Rappel : ln(eˣ) = x ; ln(1/2) = −ln2 ≈ −0,693.
- 3. Loi de décroissance : N(t) = N₀·e^(−λt), solution de dN/dt + λ·N = 0 avec N(0) = N₀.
- N₀ : noyaux présents à t = 0 ; N(t) : noyaux restants à l'instant t.
- λ : propre au nucléide, en s⁻¹ (ou j⁻¹, an⁻¹) ; ne dépend ni de N₀, ni de la température, ni de la pression.
- Attention : λ·t est sans unité : λ et t dans la même unité de temps. Plus λ est grande, plus la décroissance est rapide.

*Bloc `ra_s4_b3` — Restants et désintégrés, τ*

- 4. Noyaux désintégrés : N_d = N₀ − N(t) = N₀·(1 − e^(−λt)). Attention : lire « restants » ou « désintégrés ».
- 5. Constante de temps : τ = 1/λ (en s, ou dans l'unité de t).
- Méthode « lire τ » : la tangente à l'origine (y = N₀ − λ·N₀·t) coupe l'axe des temps en t = τ ;
- ou bien N(τ) = N₀·e⁻¹ ≈ 0,37·N₀ : placer 0,37·N₀, aller à la courbe, descendre : t = τ.
- 🖉 **Restants et désintégrés** — N(t) diminue, N_d = N₀ − N(t) augmente ; les deux courbes se croisent à t½, où N = N_d = N₀/2.
- 🖉 **La tangente à l'origine donne τ** — La tangente à l'origine coupe l'axe des temps en τ = 1/λ (ici 11,5 jours) ; N(τ) ≈ 0,37·N₀.

*Bloc `ra_s5_b1` — t½ = ln2/λ, les paliers, les pourcentages*

- 6. t½ = ln2/λ = τ·ln2 : N₀·e^(−λ·t½) = N₀/2 ⇒ e^(−λ·t½) = 1/2 ⇒ λ·t½ = ln2.
- Méthode « établir t½ » : la loi et N(t½) = N₀/2 ; simplifier par N₀ ; prendre ln ; isoler t½.
- Après n demi-vies : N(n·t½) = N₀/2ⁿ (N₀/2, N₀/4, N₀/8…) ; N ne devient jamais nul.
- Méthode « x % désintégrés » : il reste (100 − x) % : N = (1 − x/100)·N₀ ; puis la loi donne t.
- Exemple : à 2t½ il reste 25 %, donc 75 % sont désintégrés.
- 🖉 **N₀/2, N₀/4, N₀/8** — Après n demi-vies il reste N₀/2ⁿ : N₀/2 à t½ = 8 jours, N₀/4 à 2t½, N₀/8 à 3t½.


### V. L'activité et la datation

*Bloc `ra_s5_b2` — L'activité : a = λ·N, puis a(t)*

- 1. Définition : l'activité a est le nombre moyen de désintégrations par seconde dans l'échantillon.
- Unité : le becquerel, 1 Bq = 1 désintégration par seconde (mesurée au compteur Geiger).
- a = −dN/dt = λ·N (λ en s⁻¹ pour a en Bq).
- a₀ = λ·N₀ ; a(t) = a₀·e^(−λt) : même loi que N ; a(n·t½) = a₀/2ⁿ.
- Remarque : des sujets notent l'activité A ; ici A est le nombre de nucléons.

*Bloc `ra_s5_b3` — Les secondes, la mole, le nombre de noyaux*

- 2. Attention : pour a en Bq, λ en s⁻¹ : t½ en secondes (1 j = 86 400 s ; 1 an ≈ 3,16·10⁷ s).
- Exemple (2020 N) : polonium 210, t½ = 138 j = 1,19·10⁷ s ; λ = ln2/t½ ≈ 5,8·10⁻⁸ s⁻¹.
- Rappel : 1 mol = 6,02·10²³ entités (N_A, nombre d'Avogadro) ; n = m/M.
- 3. Nombre de noyaux : N = (m/M)·N_A (m en g, M en g/mol, N_A = 6,02·10²³ mol⁻¹).
- Attention : m en grammes (2 µg = 2·10⁻⁶ g) ; tritium (M = 3 g/mol) : N ≈ 4,0·10¹⁷ (2023 N).

*Bloc `ra_s6_b1` — La masse, la courbe a(t), la droite ln N*

- Sens inverse : m = (N/N_A)·M ; si a est connue, N = a/λ (λ en s⁻¹) ; m(t) = m₀·e^(−λt).
- 4. Méthode « courbe a(t) » : lire a₀ ; a₀/2 donne t½ ; τ par la tangente ou à 0,37·a₀ ; N₀ = a₀/λ.
- Exemple (2022 N) : iode 131, a₀ = 4·10⁶ Bq, t½ = 8 j = 6,91·10⁵ s, λ ≈ 1,0·10⁻⁶ s⁻¹, N₀ ≈ 4,0·10¹².
- 5. Méthode « droite ln N » : ln N = ln N₀ − λ·t : pente = −λ ; ordonnée à l'origine = ln N₀.
- 🖉 **Lire la courbe a(t)** — Iode 131 : a₀ = 4·10⁶ Bq ; a = a₀/2 à t½ = 8 jours ; puis λ en s⁻¹ et N₀ = a₀/λ.
- 🖉 **La droite ln N = f(t)** — ln N = ln N₀ − λ·t : une droite d'ordonnée à l'origine ln N₀ et de pente −λ (phosphore 32 : λ = 0,0485 j⁻¹).

*Bloc `ra_s6_b2` — Le principe de la datation*

- 6. Datation : la teneur en carbone 14 de l'air est constante (il est produit sans arrêt dans la haute atmosphère).
- Vivant : activité constante a₀ (échanges avec l'air) ; après la mort : a(t) = a₀·e^(−λt).
- a₀ : activité d'un échantillon vivant (récent) de même masse.
- Méthode « âge » : a/a₀ = e^(−λt) ⇒ ln(a₀/a) = λ·t ⇒ t = (1/λ)·ln(a₀/a) = (t½/ln2)·ln(a₀/a).
- De même t = (1/λ)·ln(N₀/N). Contrôle : t > 0, avec l'unité de t½.
- 🖉 **Le carbone 14 : vivant, puis mort** — Vivant : activité constante a₀ ; après la mort, a(t) = a₀·exp(−λt) diminue : a₀/2 au bout de t½ = 5730 ans.

*Bloc `ra_s6_b3` — Dater une roche*

- 7. Roche (sans fils au départ, fils stable) : N(père) = N₀·e^(−λt) ; N(fils) = N₀ − N(père).
- r = N(fils)/N(père) = e^(λt) − 1 ⇒ t = (1/λ)·ln(1 + r).
- Remarque : plus l'échantillon est ancien, plus t½ doit être grande (¹⁴C : jusqu'à ≈ 40 000 ans ; roche : ²³⁸U).


### VI. Exercices du national, joués étape par étape

*Bloc `ra_s7_b1` — Cas types, datation 2022 R, national 2021 N*

- 1. Le mot de la question donne la méthode : composition, équation, type, famille, t½ et λ, nombre de noyaux, âge, pourcentage.
- Datation (2022 R) : a = 318 Bq, a₀ = 418 Bq : t = (5730/0,693)·ln(418/318) ≈ 2,26·10³ ans.
- 2021 N (²³⁸Pu, α) : t½ = 88 ans = 2,78·10⁹ s ; λ ≈ 2,49·10⁻¹⁰ s⁻¹ ; N₀ = a₀/λ ≈ 4,0·10²⁰.
- 30 % désintégrés : N = 0,70·N₀ ⇒ t = (t½/ln2)·ln(1/0,70) ≈ 45 ans.

*Bloc `ra_s7_b2` — Nationaux 2022 N et 2025 N*

- 2022 N (¹³¹I, β⁻) : 95 % désintégrés ⇒ N = 0,05·N₀ ⇒ t = (8/0,693)·ln 20 ≈ 34,6 jours.
- 2025 N (¹⁰⁷Cd, β⁺) : N₀ = a₀·t½/ln2 ≈ 4,5·10¹⁶ ; entre 2t½ et 3t½ : N₀/8 ≈ 5,6·10¹⁵ désintégrés.
- Attention : λ en s⁻¹ dès qu'une activité en Bq intervient ; « désintégrés » n'est pas « restants ».


### VII. Bilan du chapitre

*Bloc `ra_s7_b3` — Bilan et carte*

- Bilan : N = A − Z ; Soddy : A et Z conservés ; N(t) = N₀·e^(−λt) ; τ = 1/λ ; t½ = ln2/λ = τ·ln2.
- a = λ·N et a(t) = a₀·e^(−λt) (λ en s⁻¹) ; N = (m/M)·N_A ; t = (1/λ)·ln(a₀/a).
- Un noyau seul : le hasard ; beaucoup de noyaux : la loi N(t) = N₀·e^(−λt).


## Le cahier du cours en ligne (son ordre)

Le cours en ligne garde son ordre : le diagramme avec ses zones et ses flèches vient en partie I, avant la définition
de la radioactivité. Le cahier y explique donc chaque type en une ligne (« un neutron devient proton : Z + 1, N − 1 »)
et renvoie à la partie II ; la famille est en partie II, la demi-vie après la loi, la datation dans la partie IV.
Les lignes sont les mêmes que dans la copie en attente, renumérotées dans l'ordre du cours en ligne.

### I. Le noyau et sa stabilité

*Bloc `ra_s1_b1` — L'atome, le noyau et sa notation*

- 1. Le noyau : des protons (charge +e) et des neutrons (charge nulle), appelés nucléons.
- Autour du noyau, très petit, se trouvent les électrons (charge −e) ; presque toute la masse est dans le noyau.
- 2. Notation ᴬ_Z X : X symbole de l'élément ; Z nombre de charge (protons) ; A nombre de nucléons.
- N = A − Z : nombre de neutrons. Exemple : ¹⁴₆C a Z = 6 protons, N = 8 neutrons, A = 14 nucléons.
- Attention : A en haut, Z en bas ; ne pas confondre A (nucléons) et N (neutrons).

*Bloc `ra_s1_b2` — Composition, isotopes et diagramme (N, Z)*

- Méthode « composition » : Z protons ; N = A − Z neutrons (²³⁸₉₂U : 92 et 146).
- 3. Définition : des isotopes sont des noyaux de même nombre de charge Z et de nombres de nucléons A différents.
- Exemples : ¹²₆C et ¹⁴₆C ; ¹H, ²H, ³H. Nucléide : noyaux de même A et de même Z.
- 4. Diagramme (N, Z) : Z en abscisse, N en ordonnée ; un nucléide = un point (Z ; N).

*Bloc `ra_s1_b3` — La vallée, les zones, les flèches une à une*

- 5. Vallée de stabilité : bande des noyaux stables ; légers (Z < 20) : N ≈ Z ; lourds : N > Z.
- Hors de la vallée, le noyau est instable : il se transforme (radioactivité, partie II) pour s'en rapprocher.
- 6. Trop de neutrons (au-dessus) → β⁻ : un neutron devient proton : Z + 1, N − 1.
- Trop de protons (au-dessous) → β⁺ : un proton devient neutron : Z − 1, N + 1 (A ne change pas).
- Noyau lourd → α : il perd 2 protons et 2 neutrons : Z − 2, N − 2, A − 4.
- 🖉 **Le diagramme (N, Z) et ses zones** — Au-dessus de la vallée (trop de neutrons) : β⁻ ; au-dessous (trop de protons) : β⁺ ; noyaux lourds : α.
- 🖉 **Le noyau redescend vers la vallée** — β⁻ : Z + 1 et N − 1 ; β⁺ : Z − 1 et N + 1 ; α : Z − 2 et N − 2.


### II. Les désintégrations

*Bloc `ra_s2_b1` — Les isotopes, la radioactivité et ses trois caractères*

- 7. Les isotopes d'un élément sont sur une même droite perpendiculaire à l'axe des Z.
- 1. Définition : la radioactivité est la transformation spontanée d'un noyau instable (père) en un noyau plus stable (fils), avec émission d'une particule.
- Noyau père → noyau fils + particule ; le fils est plus stable, pas forcément stable.
- 2. Elle est aléatoire : on ne peut prévoir ni quel noyau se désintègre, ni à quel instant.
- Elle est spontanée et inéluctable : température, pression, liaisons chimiques n'y changent rien.

*Bloc `ra_s2_b2` — Les lois de Soddy, α et β⁻*

- 3. Lois de Soddy, pour ᴬ_Z X → ᴬ¹_Z₁ Y + ᴬ²_Z₂ P : A = A₁ + A₂ et Z = Z₁ + Z₂.
- Remarque : on conserve la charge Z, pas le nombre de protons (un neutron peut devenir proton).
- 4. α (noyaux lourds) : ᴬ_Z X → ᴬ⁻⁴_Z₋₂ Y + ⁴₂He ; ex. ²¹⁰₈₄Po → ²⁰⁶₈₂Pb + ⁴₂He.
- β⁻ : ¹₀n → ¹₁p + ⁰₋₁e ; ᴬ_Z X → ᴬ_Z₊₁ Y + ⁰₋₁e ; ex. ¹⁴₆C → ¹⁴₇N + ⁰₋₁e.
- Attention : l'électron β⁻ est créé dans le noyau, qui ne contient pas d'électron.
- β⁺ : ¹₁p → ¹₀n + ⁰₁e (positon) ; ᴬ_Z X → ᴬ_Z₋₁ Y + ⁰₁e ; ex. ³⁰₁₅P → ³⁰₁₄Si + ⁰₁e.

*Bloc `ra_s2_b3` — γ, le noyau fils inconnu, le type par la particule*

- γ : désexcitation du fils excité, ᴬ_Z Y* → ᴬ_Z Y + γ ; A et Z ne changent pas.
- Pénétration : α arrêtée par du papier, β par quelques mm d'aluminium, γ par du plomb.
- 5. Méthode « équation » : 1) écrire ᴬ_Z Y inconnu ; 2) « d'après les lois de Soddy » : A puis Z ; 3) Z donne l'élément (tableau).
- Méthode « type » : Soddy donne A et Z de la particule : ⁴₂He → α ; ⁰₋₁e → β⁻ ; ⁰₁e → β⁺.
- Exemple (2021 R) : ³²₁₅P → ³²₁₆S + ⁰₋₁e : β⁻.

*Bloc `ra_s3_b1` — La famille radioactive*

- 6. Définition : une famille radioactive est une suite de désintégrations d'un noyau père jusqu'à un noyau stable.
- Exemple : ²³⁸₉₂U → … → ²⁰⁶₈₂Pb (stable) : 8 désintégrations α et 6 désintégrations β⁻.
- Méthode « famille » : ᴬ_Z X → ᴬ'_Z' Y + y ⁴₂He + x ⁰₋₁e ; 1) A = A' + 4y donne y ; 2) Z = Z' + 2y − x donne x.
- Vérifier : 238 = 206 + 4 × 8 et 92 = 82 + 2 × 8 − 6.
- Lire une flèche : A − 4 et Z − 2 → α ; A constant, Z + 1 → β⁻ ; A constant, Z − 1 → β⁺.


### III. La loi de décroissance et la demi-vie

*Bloc `ra_s3_b2` — Beaucoup de noyaux : la même proportion, l'équation*

- 1. Un échantillon : le nombre N de noyaux restants diminue de façon régulière.
- Pendant une même durée, la même proportion de noyaux se désintègre (≈ 8 % par jour pour l'iode 131).
- Noyaux désintégrés pendant dt : −dN = λ·N·dt (λ : constante radioactive, en s⁻¹).
- Équation différentielle : dN/dt + λ·N = 0.

*Bloc `ra_s3_b3` — L'exponentielle, ln, et la loi de décroissance*

- Rappel : e⁰ = 1 ; e^(−x) diminue quand x augmente et tend vers 0 sans jamais l'atteindre.
- Rappel : ln(eˣ) = x ; ln(1/2) = −ln2 ≈ −0,693.
- 2. Loi de décroissance : N(t) = N₀·e^(−λt), solution de dN/dt + λ·N = 0 avec N(0) = N₀.
- N₀ : noyaux présents à t = 0 ; N(t) : noyaux restants à l'instant t.
- 🖉 **L'exponentielle qui décroît** — e⁰ = 1 ; quand x augmente, e^(−x) diminue et s'approche de 0 sans jamais l'atteindre.

*Bloc `ra_s4_b1` — λ, τ, restants et désintégrés*

- λ : propre au nucléide, en s⁻¹ (ou j⁻¹, an⁻¹) ; ne dépend ni de N₀, ni de la température, ni de la pression.
- Attention : λ·t est sans unité : λ et t dans la même unité de temps. Plus λ est grande, plus la décroissance est rapide.
- 3. Constante de temps : τ = 1/λ (en s, ou dans l'unité de t).
- Méthode « lire τ » : la tangente à l'origine (y = N₀ − λ·N₀·t) coupe l'axe des temps en t = τ ;
- ou bien N(τ) = N₀·e⁻¹ ≈ 0,37·N₀ : placer 0,37·N₀, aller à la courbe, descendre : t = τ.
- 4. Noyaux désintégrés : N_d = N₀ − N(t) = N₀·(1 − e^(−λt)). Attention : lire « restants » ou « désintégrés ».
- 🖉 **Restants et désintégrés** — N(t) diminue, N_d = N₀ − N(t) augmente ; les deux courbes se croisent à t½, où N = N_d = N₀/2.
- 🖉 **La tangente à l'origine donne τ** — La tangente à l'origine coupe l'axe des temps en τ = 1/λ (ici 11,5 jours) ; N(τ) ≈ 0,37·N₀.

*Bloc `ra_s4_b2` — La demi-vie*

- 5. Définition : la demi-vie t½ est la durée au bout de laquelle la moitié des noyaux initialement présents s'est désintégrée.
- N(t½) = N₀/2 ; t½ est propre au nucléide, sans dépendre de N₀ (iode 131 : 8 jours ; carbone 14 : 5730 ans).
- t½ = ln2/λ = τ·ln2 : N₀·e^(−λ·t½) = N₀/2 ⇒ e^(−λ·t½) = 1/2 ⇒ λ·t½ = ln2.
- Méthode « lire t½ » : 1) lire N₀ ; 2) placer N₀/2 sur l'axe des N ; 3) aller à la courbe ; 4) descendre sur l'axe des t.
- Après n demi-vies : N(n·t½) = N₀/2ⁿ (N₀/2, N₀/4, N₀/8…) ; N ne devient jamais nul.
- Méthode « x % désintégrés » : il reste (100 − x) % : N = (1 − x/100)·N₀ ; puis la loi donne t.
- 🖉 **N₀/2, N₀/4, N₀/8** — Après n demi-vies il reste N₀/2ⁿ : N₀/2 à t½ = 8 jours, N₀/4 à 2t½, N₀/8 à 3t½.


### IV. L'activité et la datation

*Bloc `ra_s4_b3` — L'activité : a = λ·N, puis a(t)*

- 1. Définition : l'activité a est le nombre moyen de désintégrations par seconde dans l'échantillon.
- Unité : le becquerel, 1 Bq = 1 désintégration par seconde (mesurée au compteur Geiger).
- a = −dN/dt = λ·N (λ en s⁻¹ pour a en Bq).
- a₀ = λ·N₀ ; a(t) = a₀·e^(−λt) : même loi que N ; a(n·t½) = a₀/2ⁿ.
- Remarque : des sujets notent l'activité A ; ici A est le nombre de nucléons.

*Bloc `ra_s5_b1` — Puissances de dix, la mole, le nombre de noyaux*

- Rappel : 10ⁿ = 1 suivi de n zéros (1,19·10⁷ = 11 900 000) ; 10⁻³ = 0,001 ; 2·10⁻⁶ g = 0,000 002 g.
- 2. Attention : pour a en Bq, λ en s⁻¹ : t½ en secondes (1 j = 86 400 s ; 1 an ≈ 3,16·10⁷ s).
- Exemple (2020 N) : polonium 210, t½ = 138 j = 1,19·10⁷ s ; λ = ln2/t½ ≈ 5,8·10⁻⁸ s⁻¹.
- Rappel : 1 mol = 6,02·10²³ entités (N_A, nombre d'Avogadro) ; n = m/M.
- 3. Nombre de noyaux : N = (m/M)·N_A (m en g, M en g/mol, N_A = 6,02·10²³ mol⁻¹).
- Attention : m en grammes (2 µg = 2·10⁻⁶ g) ; tritium (M = 3 g/mol) : N ≈ 4,0·10¹⁷ (2023 N).

*Bloc `ra_s5_b2` — Lire les courbes, puis le principe de la datation*

- Sens inverse : m = (N/N_A)·M ; si a est connue, N = a/λ (λ en s⁻¹) ; m(t) = m₀·e^(−λt).
- 4. Méthode « courbe a(t) » : lire a₀ ; a₀/2 donne t½ ; τ par la tangente ou à 0,37·a₀ ; N₀ = a₀/λ.
- 5. Méthode « droite ln N » : ln N = ln N₀ − λ·t : pente = −λ ; ordonnée à l'origine = ln N₀.
- 6. Datation : la teneur en carbone 14 de l'air est constante (il est produit sans arrêt dans la haute atmosphère).
- Vivant : activité constante a₀ (échanges avec l'air) ; après la mort : a(t) = a₀·e^(−λt).
- 🖉 **La droite ln N = f(t)** — ln N = ln N₀ − λ·t : une droite d'ordonnée à l'origine ln N₀ et de pente −λ (phosphore 32 : λ = 0,0485 j⁻¹).
- 🖉 **Le carbone 14 : vivant, puis mort** — Vivant : activité constante a₀ ; après la mort, a(t) = a₀·exp(−λt) diminue : a₀/2 au bout de t½ = 5730 ans.

*Bloc `ra_s5_b3` — Dater un bois, dater une roche*

- a₀ : activité d'un échantillon vivant (récent) de même masse.
- Méthode « âge » : a/a₀ = e^(−λt) ⇒ ln(a₀/a) = λ·t ⇒ t = (1/λ)·ln(a₀/a) = (t½/ln2)·ln(a₀/a).
- Datation (2022 R) : a = 318 Bq, a₀ = 418 Bq : t = (5730/0,693)·ln(418/318) ≈ 2,26·10³ ans.
- 7. Roche (sans fils au départ, fils stable) : N(père) = N₀·e^(−λt) ; N(fils) = N₀ − N(père).
- r = N(fils)/N(père) = e^(λt) − 1 ⇒ t = (1/λ)·ln(1 + r).
- Remarque : plus l'échantillon est ancien, plus t½ doit être grande (¹⁴C : jusqu'à ≈ 40 000 ans ; roche : ²³⁸U).


### V. Cas types du national

*Bloc `ra_s6_b1` — Cas types et nationaux 2021 N, 2022 N*

- 1. Le mot de la question donne la méthode : composition, équation, type, famille, t½ et λ, nombre de noyaux, âge, pourcentage.
- 2021 N (²³⁸Pu, α) : t½ = 88 ans = 2,78·10⁹ s ; λ ≈ 2,49·10⁻¹⁰ s⁻¹ ; N₀ = a₀/λ ≈ 4,0·10²⁰.
- 30 % désintégrés : N = 0,70·N₀ ⇒ t = (t½/ln2)·ln(1/0,70) ≈ 45 ans.
- 2022 N (¹³¹I, β⁻) : 95 % désintégrés ⇒ N = 0,05·N₀ ⇒ t = (8/0,693)·ln 20 ≈ 34,6 jours.


### VI. Bilan du chapitre

*Bloc `ra_s6_b2` — National 2025 N, bilan et carte*

- 2025 N (¹⁰⁷Cd, β⁺) : N₀ = a₀·t½/ln2 ≈ 4,5·10¹⁶ ; entre 2t½ et 3t½ : N₀/8 ≈ 5,6·10¹⁵ désintégrés.
- Attention : λ en s⁻¹ dès qu'une activité en Bq intervient ; « désintégrés » n'est pas « restants ».
- Bilan : N = A − Z ; Soddy : A et Z conservés ; N(t) = N₀·e^(−λt) ; τ = 1/λ ; t½ = ln2/λ = τ·ln2.
- a = λ·N et a(t) = a₀·e^(−λt) (λ en s⁻¹) ; N = (m/M)·N_A ; t = (1/λ)·ln(a₀/a).
- Un noyau seul : le hasard ; beaucoup de noyaux : la loi N(t) = N₀·e^(−λt).


## Dessins

| Diapositive | Dessin | Nouveau ? |
|---|---|---|
| ra_s2_vallee | La vallée de stabilité (N = Z, la vallée, une verticale d'isotopes : stable / instable) | nouveau |
| ra_s4b_alpha | Le noyau redescend vers la vallée (flèches β⁻, β⁺, α) | gardé |
| ra_s3_zones | Le diagramme (N, Z) et ses zones | gardé |
| ra_l1b_moitie | Iode 131 : 400, 200, 100, 50 noyaux à 0, 8, 16, 24 jours (en attente seulement) | nouveau |
| ra_l4a_exp | L'exponentielle qui décroît | gardé |
| ra_l8_restants | Restants N(t) et désintégrés N_d, croisement à t½ (N₀/2) | nouveau |
| ra_l7_tau | La tangente à l'origine donne τ (τ = 8/ln2 ≈ 11,5 j ; 0,37·N₀ ≈ 2,94·10²⁰) | gardé |
| ra_t3_paliers | N₀/2, N₀/4, N₀/8 | gardé |
| ra_a6_courbe_a | Lire la courbe a(t) : a₀ = 4·10⁶ Bq, a₀/2 à t½ = 8 j | nouveau |
| ra_a7_droite_ln | La droite ln N = f(t) | gardé |
| ra_c1_principe | Le carbone 14 : vivant, puis mort | gardé |

Valeurs recalculées en Python : 400·2⁻² = 100 ; 8·e⁻¹ = 2,943 ; 8/ln2 = 11,54 ; (5730/0,693)·ln(418/318) = 2,26·10³ ans ;
(88/0,693)·ln(1/0,70) = 45,3 ans ; (8/0,693)·ln 20 = 34,6 j ; 2·10⁻⁶/3 × 6,02·10²³ = 4,0·10¹⁷ ; 0,693/(6,91·10⁵) = 1,0·10⁻⁶ s⁻¹.

## Ce qui a été corrigé par rapport au cahier d'avant

- Aucune numérotation, aucun « Définition / Méthode / Attention » : ajoutés ; les définitions reprises mot pour mot.
- Copie en attente : les blocs gardaient les lignes de l'ancien ordre ; ils suivent maintenant leurs propres diapositives.
- Méthodes du national écrites en étapes : composition, équation (Soddy cité), type, famille, lire t½, lire τ (tangente
  et 37 %), établir t½, x % désintégrés, courbe a(t), droite ln N, âge, roche.
- Cours en ligne : la figure « droite ln N » était dans le bloc des puissances de dix (ra_s5_b1) et celle du carbone 14
  était répétée dans ra_s5_b3 : retirées de là ; zones et flèches ne sont plus écrites avant d'être expliquées.
- Pénétration de α, β, γ ajoutée (dite dans les diapositives, absente du cahier).

## Ce qui reste

- Le cours en ligne nomme β⁻, β⁺, α en partie I avant la définition de la radioactivité (défaut de l'ordre des
  diapositives, corrigé dans la copie en attente) : le cahier ne peut que l'expliquer sur place.
- Pas de contrôle visuel des nouvelles figures dans le navigateur (pas de banc de rendu de `FigureCahier.tsx`) : elles
  suivent la forme des figures déjà relues ; `verifier_figures_cahier.py` : 0 erreur, 0 avertissement.
- Trois définitions dépassent 90 caractères (radioactivité, demi-vie, famille) : gardées entières, mot pour mot.

