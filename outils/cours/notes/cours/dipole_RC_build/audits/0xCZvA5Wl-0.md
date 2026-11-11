# Audit — 0xCZvA5Wl-0 (Prof Laksabi, charge du condensateur)

## Fiche
- **id** : 0xCZvA5Wl-0 — **professeur** : Prof Laksabi — **titre** : « ÉLECTRICITÉ 02 : dipôle RC la phase de chargement du condensateur » — **durée** : 3735 s (1 h 02) — **vues** : ≈ 88 600 — publiée (métadonnée) 20/12/2025 ; à l'écran le prof montre son téléphone daté du 19 décembre et dit « 2020 » (enregistrement à 5 h 30 du matin) : date d'enregistrement incertaine.
- **Support** : grand tableau blanc en 4 panneaux, feutres rouge/bleu/vert/noir, filmé face caméra, seul (pas de classe). Darija + termes français ; sous-titres auto arabes (1613 lignes) lus au son.
- **Pourquoi elle compte** : 2ᵉ vidéo d'une série (V1 = les relations du conducteur ohmique et du condensateur ; V3/V4 = décharge + nationaux annoncés). Elle est **toute entière sur la charge**, menée par une méthode unique : « garde 4 relations au coin du tableau et dérive tout d'elles, n'apprends rien par cœur ». Commentaires très positifs (« premier prof avec qui je comprends l'électricité / le RC »).

## Plan horodaté
| Temps | Notion | Durée |
|---|---|---|
| 00:00–02:50 | Rappel V1, générateur de **tension** (pas de courant), convention récepteur, conditions initiales u_C(0)=0, q(0)=0, E_e(0)=0 ; analogie téléphone 0 %→100 % | 3 min |
| 02:50–14:20 | **Équations différentielles** : définition (« la fonction et sa dérivée dans la même équation », exemple f + 4f′ = 2) ; ED en u_C, q, i, u_R | **11,5 min** |
| 14:20–25:10 | **Solution u_C = A + B·e^(−αt)** : méthode en 4 étapes Dév / Dér / Remp / Fact, A = E, α = 1/RC, B = −E par les C.I. | **11 min** |
| 25:10–33:00 | **2ᵉ forme u_C = A(1 − e^(−t/τ))** : astuce « f + τ·f′ = A » (coefficient de la dérivée = τ, second membre = A), A = E, τ = RC ; même chose pour q (A = EC) | 8 min |
| 33:00–39:30 | **Courbe u_C(t)** : tableau t = 0 / τ / +∞ → 0 / 0,63E / E ; asymptote, tangente à l'origine, τ = intersection tangente–asymptote, méthode 0,63E ; τ = RC ⇒ R = τ/C, C = τ/R ; dimension de τ (mentionnée, renvoyée aux exercices) | 6,5 min |
| 39:30–45:00 | Passer d'une grandeur à l'autre : q = C·u_C ⇒ q(t) ; i = C·du_C/dt ⇒ i = (E/R)e^(−t/τ) ; u_R = R·i ⇒ u_R = E·e^(−t/τ) ; courbes q(t) (Q_m, 0,63Q_m) et i(t) (E/R, 0,37·E/R) | 5,5 min |
| 45:00–62:00 | **Résumé en 4 colonnes + 4 cas types chiffrés** (calcul de C, de E_e en régime permanent, de R, de C, de E_e(τ)) ; régime transitoire / permanent (5τ) | **17 min** |

## Rappels (tronc commun / 1re)
- Convention récepteur : u_C dessinée **opposée** au courant, u_R aussi ; E dans le même sens que i au générateur (« générateur »). Il renvoie à la V1 pour ces sens.
- Loi d'additivité : « u_C + u_R = E », dite « d'après la loi d'additivité des tensions », et il insiste : **ce n'est pas une relation à apprendre, elle se lit sur le circuit** (décharge : u_C + u_R = 0).
- Boîte permanente en bas à droite du tableau (jamais effacée, « j'efface le circuit mais pas ça ») : symbole R → **u_R = R i** ; symbole condensateur → **q = C u_C** ; **i = dq/dt | i = C du_C/dt**.
- Rappel maths : (e^u)′ = u′e^u, (e^(−4x))′ = −4e^(−4x), (e^(−αt))′ = −α e^(−αt), (−t/τ)′ = −1/τ ; e⁰ = 1 ; e^(−∞) → 0 (« positif, s'approche de 0 sans l'atteindre ») ; renvoi au nucléaire (N = N₀e^(−λt)).

## Définitions (telles qu'écrites / dites)
- Titre : « # La charge ». Pas de définition écrite du condensateur, des armatures, de la capacité ni de l'échelon (supposés vus en V1).
- **Équation différentielle** (dite) : une équation où figurent la fonction et sa dérivée en même temps ; exemple au tableau « f + 4f′ = 2 ».
- **Conditions initiales** (écrit « Les condition initiale ») : u_C(t=0)=0 ; q(t=0)=0 ; E_e(0)=0.
- **Régime transitoire / permanent** (dit puis écrit « R.T » / « R.P » sur la courbe) : permanent = quand la courbe se stabilise, « après 5τ ».
- **τ** (dit) : « l'intersection entre la tangente et l'asymptote » ; pas de nom « constante de temps » écrit.
- Énergie : écrite « l'énergie E_e » puis **E_e = ½ C u_C²** (cadre en haut du tableau).

## Formules — écrites et dites
- ED u_C (lignes) : u_C + u_R = E ↓ u_C + Ri = E ↓ u_C + RC·du_C/dt = E (encadrée dans une bulle, flèches « f » sous u_C et « f′ » sous du_C/dt).
- ED q : u_C + u_R = E ; q/C + Ri = E ; q/C + R·dq/dt = E ; « ×C( … ) » ; **q + RC·dq/dt = EC**.
- ED i : u_C + u_R = E ; « Dér : » du_C/dt + du_R/dt = 0 ; i/C + d(Ri)/dt = 0 ; ×C ⇒ **i + RC·di/dt = 0**.
- ED u_R : du_C/dt + du_R/dt = 0 ; (u_R/R)/C + du_R/dt = 0 ; u_R/RC + du_R/dt = 0 | **u_R + RC·du_R/dt = 0**.
- Choix assumé : **toujours laisser le coefficient 1 devant la fonction** (pas la forme du/dt + u/RC = E/RC, qu'il dit « juste aussi » mais déconseille) — parce que cela donne τ et A par simple lecture.
- Solution forme 1 : « 2°/ La Solution s'écrit sous forme : u_C = A + B e^(−αt) (1). Déterminer A, B et α ». Ligne par ligne : du_C/dt = dA/dt + B·d(e^(−αt))/dt = 0 + B[−α e^(−αt)] ⇒ du_C/dt = −αB e^(−αt) (2) ; « On remplace (1) et (2) ds É.D » : A + Be^(−αt) − RCαBe^(−αt) = E ; Be^(−αt) − RCαBe^(−αt) = E − A ; **Be^(−αt)[1 − RCα] = E − A** ; { E − A = 0 ⇒ **A = E** ; 1 − RCα = 0 ⇒ **α = 1/RC** } (« le produit est nul : l'exponentielle n'est jamais nulle ») ; « D'après C.I : u_C(t=0) = A + Be⁰ = A + B = 0 ⇒ **B = −A = −E** ».
- Solution forme 2 : « La solution de l'équation diff s'écrit sous forme : u_C = A(1 − e^(−t/τ)). Déterminer A et τ » : développer u_C = A − Ae^(−t/τ) (1) ; du_C/dt = (A/τ)e^(−t/τ) (2) ; remplacer ; Ae^(−t/τ)[−1 + RC/τ] = E − A ⇒ **A = E**, **τ = RC**. Puis le raccourci « f + τf′ = A » : on lit τ = RC et A = E directement sur u_C + RC du_C/dt = E ; de même q = A(1 − e^(−t/τ)) ⇒ A = EC, τ = RC. Il dit qu'on peut s'en servir pour **anticiper** le résultat, mais que la rédaction complète reste obligatoire.
- Dérivées : u_C = E(1 − e^(−t/τ)) ; q = EC(1 − e^(−t/τ)) ; « On a : i = C du_C/dt ; i = C(A/τ e^(−t/τ)) ; i = C(E/RC e^(−t/τ)) ; **i = (E/R) e^(−t/τ)** » (encadré) ; i·R = u_R ⇒ **u_R = E e^(−t/τ)**. Schéma : u_C → q, → i, → u_R (flèches).
- Valeurs : u_C(0)=E(1−e⁰)=0 ; u_C(τ)=E(1−e^(−1)) = **0,63E** ; u_C(∞)=E(1−e^(−∞)) = E (il précise que « t = ∞ » est une écriture fausse en maths : c'est une limite).
- Énergie : **E_e = ½ C u_C²** ; en R.P. : E_em = ½ C u_Cmax² = ½ C E² ; aussi **E_e = Q_m²/2C** (u_C remplacé par q/C) ; à t = τ : E_e(τ) = ½ C (0,63E)².
- τ = RC ⇒ R = τ/C ; C = τ/R. Q_m = C·E ⇒ C = Q_m/E. u_Rm = R·I₀ et u_Rm = E ⇒ R = E/I₀.
- Analyse dimensionnelle de τ : seulement **mentionnée** (« elle ne tombe plus depuis 2020 », renvoyée aux exercices).
- Pas d'associations de condensateurs ; il glisse seulement « si les condensateurs sont doublés, c'est un autre problème ».

## Méthodes graphiques
- u_C(t) (axes « u(V) » / « t(s) ») : asymptote horizontale pointillée « U_Cmax = E », tangente à l'origine, son intersection avec l'asymptote projetée sur l'axe = τ ; ligne pointillée 0,63E ⇒ projection τ (« si tu n'as pas la tangente »).
- q(t) : Q_m (= CE), 0,63Q_m, τ.
- i(t) (« i(A) ») : départ E/R (= I₀), décroissante, tangente à l'origine coupant l'axe des temps en τ, 0,37·E/R ⇒ τ. Il prévient : **i décroît pendant la charge** (ce n'est pas la courbe du condensateur) ; en décharge, i « monte depuis −I_max ».
- u_R(t) : départ E, décroissante.
- « R.T » puis « R.P » écrits sous la courbe ; R.P après 5τ.
- Aucune droite ln, aucune courbe du/dt = f(u).

## Montages
- **Générateur de tension idéal** seulement (« pas de courant cette fois », annonce un générateur de courant traité en V1). Circuit : C en haut, R à gauche, E (cercle) à droite, **pas d'interrupteur K dessiné**, flèches i, flèches bleues u_C (au-dessus de C), u_R (à gauche de R), E.
- Pas d'oscilloscope ni d'ExAO dans cette vidéo.

## Exemples chiffrés et analogies
- Analogie **téléphone qui charge** (0 % → 100 %, il ne passe pas à 101 %) : u_C croissante bornée ; « on ne charge pas un téléphone déjà à 100 % » ⇒ C.I. nulles.
- Cas 1 (u_C) : graphe E = 10 V, τ = 0,01 s, R = 1 kΩ ⇒ C = τ/R = 0,01/(1×10³) = 10⁻⁵ F ; E_em en R.P = ½·10⁻⁵·10² = 5×10⁻⁴ J.
- Cas 2 (q) : Q₀ = 10⁻⁵ C, τ = 10⁻³ s, E = 10 V ⇒ **sans R, τ = RC inutilisable** ⇒ Q_m = CE ⇒ C = 10⁻⁶ F ; E_e = ½ C E² ou Q_m²/2C.
- Cas 3 (i) : E = 6 V, I₀ = 10 mA, τ = 0,1 s ⇒ R = E/I₀ = 600 Ω, puis C = τ/R.
- Cas 4 (u_R) : E = 6 V, τ = 1 ms, C = 5 µF ⇒ R = τ/C = 2×10² Ω ; E_e(τ) = ½ C (0,63E)².

## Insistances, erreurs, conseils
- « Ne mémorise pas » répété ~10 fois : 4 relations (u_R = Ri, q = Cu_C, i = dq/dt = C du_C/dt) + l'additivité suffisent à tout produire.
- **Garder 1 devant la fonction** dans l'ED (« astuce redoutable ») : répété 6–7 fois, lien direct avec τ et A.
- Les **C.I. de la décharge** diffèrent : écrire u_C(0) = 0 en décharge est faux.
- Méthode 4 étapes **Dév → Dér → Remp → Fact** encadrée, cochée au fur et à mesure.
- « C'est ton cerveau qui guide ta main » : avant d'écrire τ = RC, vérifier qu'on a R ; sinon passer par Q_m = CE ou E = RI₀ (« physique royale »). Erreur type : appliquer τ = RC avec deux inconnues.
- i(t) décroissante en charge : piège signalé.
- Ne pas confondre u_Cmax « = E » valable pour un seul R et un seul C.
- Exam : V suivante = nationaux 2019 SVT, 2019 PC et un autre PC ; conseil d'éviter les « notes catastrophiques ».
- Unités : convertir ms, mA, µF en unités SI avant le calcul (fait au tableau à chaque cas).

## Faux, approximatif ou hors programme
- Rien de hors programme (pas de séparation des variables, ni Laplace, ni régime sinusoïdal).
- Approximations à ne pas répéter : « 1 − e^(−1) ≈ 0,63 » correct, mais u_C(∞) écrit « E(1 − e^(−∞)) » (il corrige oralement : limite). La convention « α » + « B = −A » est bonne mais il écrit « D'après C.I » sans recopier u_C(0)=0 sur la même ligne en forme 2.
- Il appelle τ « l'intersection » (c'est sa lecture graphique, pas sa définition) — à ne pas donner comme définition.
- Orthographe au tableau : « Les condition initiale », « s'écrit se forme ».
- « l'énergie E_e » en R.P qualifiée de « maximale » : juste pour la charge, à préciser.

## Commentaires d'élèves (150 lus)
- Remerciements / « premier prof avec qui je comprends le RC / l'électricité » : ~60 (dont 85 likes en tête) ; dizaines de prières pour sa mère (il en parle à 52:30).
- « Je ne comprends rien en PC » (25 likes) ; un élève dit n'avoir pas compris son prof de classe, compris ici ; un autre a un devoir le lendemain et dit tout comprendre.
- Horodatages : 14:29 (« vitesse ×2 », il dit pouvoir regarder en ×2), 55:43 « physique royale » (mème), 33:18, 52:30.
- Demandes : partie 3 / décharge, mécanique, chimie organique. Aucune question de fond (pas de doute sur une formule).

## Ce que notre cours doit lui prendre
1. La **boîte des 4 relations** fixe dans un coin du tableau, réutilisée pour chaque ED (q, i, u_R) — et la règle « l'additivité se lit sur le circuit ».
2. La rédaction ligne par ligne des ED avec le **coefficient 1 devant la fonction**, puis la lecture « f + τ·f′ = A » pour anticiper τ = RC et A = E (puis rédaction complète).
3. La méthode **Dév / Dér / Remp / Fact** encadrée, avec le passage « produit nul, exponentielle jamais nulle » et les C.I. pour B.
4. Le **tableau t = 0 / τ / ∞** → 0 / 0,63E / E avant de tracer la courbe (le chiffre précède le dessin).
5. Les **cas types « je n'ai pas R »** : choisir la relation selon les données (τ = RC, Q_m = CE, E = RI₀, E_e = ½CE² ou Q_m²/2C, E_e(τ) avec 0,63E).
6. Le **piège i(t) décroissante pendant la charge** et l'analogie téléphone (avec sa limite : la charge d'un condensateur n'est pas linéaire).
