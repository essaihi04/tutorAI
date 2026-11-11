# Audit — AOK4FfniVZA (Driss DOTCOM, Dipôle RC)

## Fiche
- id : AOK4FfniVZA — professeur : Driss DOTCOM (YouTube) — titre : « Dipôle RC 2 Bac : Electricité -- Cours Complet --- ملخص شامل »
- durée : 3283 s (54 min 43) — vues : ≈ 125 700 — publiée le 5 décembre 2025.
- support : grand tableau blanc tourné en studio, trois colonnes séparées par des traits roses ondulés, feutres de 4 couleurs (rose = titres, vert/turquoise = encadrés et rappels, noir = calculs, bleu = énoncé d'exercice). Prof debout, face caméra entre deux écritures. Pas de classe, pas d'expérience, pas d'oscilloscope réel.
- sources lues : transcription automatique 1633 lignes (lue en entier), 150 commentaires, 61 images du tableau (une par minute + passes à 20-30 s autour des courbes et de l'oscilloscope).
- pourquoi elle compte : format « résumé complet + un devoir corrigé », très suivi par les candidats (commentaires « Bac 2026 »). C'est la vidéo-type de la méthode « quatre équations différentielles × deux régimes ». Il traite charge et décharge, la méthode d'identification de A et τ et l'analyse dimensionnelle, mais **ne traite pas l'énergie** et contient une erreur de lecture de τ.

## Plan horodaté
| Temps | Notion | Durée |
|---|---|---|
| 00:00–01:20 | Annonce : l'unité électricité = RC, RL, RLC (+ modulation pour PC) ; RC identique PC/SVT | 1 min 20 |
| 01:45–04:10 | Rappels : générateur (3 symboles : pile, source avec E dans un cercle), courant sort du + ; générateur : tension et courant dans le même sens, récepteur : sens opposés ; nommer U_AB (flèche vers A) | 2 min 30 |
| 04:10–06:20 | Loi d'Ohm U_R = R·i (V, Ω, A) ; R en série et en parallèle (produit sur somme) | 2 min |
| 06:20–09:30 | Condensateur : deux plaques + isolant, image électrons qui s'accumulent ; analogie « القرعة » (bouteille) remplie d'eau / d'électricité ; lampe qui s'allume puis s'éteint ; q, u_C, C et unités | 3 min |
| 09:30–11:15 | i = dq/dt = C·du_C/dt ; associations de condensateurs (inverse des résistances) | 2 min |
| 11:15–13:50 | Montage-type à interrupteur K (1) charge, (2) décharge ; « quatre choses à savoir » : équation différentielle, solution, intensité, courbe | 2 min 30 |
| 13:50–21:00 | Charge : **quatre équations différentielles** (u_C, q, u_R, i) | 7 min (plus long séjour) |
| 21:00–28:10 | Solution : cas 1 « trouver A et τ », cas 2 « vérifier que c'est la solution » | 7 min |
| 28:15–29:40 | Intensité i(t) = (E/R)·e^(−t/RC), I₀ = E/R | 1 min 30 |
| 29:40–30:55 | Courbe u_C(t) : tangente à l'origine, 0,63·E, régime transitoire / permanent | 1 min 15 |
| 31:15–44:15 | Devoir corrigé (E = 12 V, courbe i(t)) : représenter u_C et u_R, oscilloscope, éq. diff., A et τ, i(t), dimension de τ, R, τ et C, condensateurs en parallèle | 13 min |
| 44:20–52:15 | Décharge : quatre équations différentielles, solution A·e^(−t/τ), conditions initiales, 0,37·E, i(t) négatif | 8 min |
| 52:15–54:40 | Exhortation (répétition), publicité pour ses groupes | 2 min 30 |

## Rappels du tronc commun / 1re
- Il passe 6 min sur les rappels, sur un panneau « Rappels » encadré en vert qui reste au tableau toute la vidéo : **Générateur** (trois symboles, flèche E dans le sens du courant), **Récepteur** (résistance A→B, i vers B, flèche U_AB = U_R en sens inverse : convention récepteur), **Loi d'Ohm** U_R = R·i avec les unités (V) (Ω) (A) sous chaque lettre, R_éq série = R₁ + R₂, R_éq parallèle = R₁·R₂/(R₁ + R₂) dérivée de 1/R_éq = 1/R₁ + 1/R₂ au milieu du tableau.
- Phrase-règle répétée plusieurs fois : « au générateur, la tension va avec le courant ; à tout récepteur, elle va contre ». Elle sert ensuite à flécher u_R et u_C dans l'exercice (question 1).
- Loi d'additivité écrite **Σ U(récepteurs) = Σ U(générateurs)** (abrégée « Σ U(r) = Σ U(g) »), en premier sur chaque équation, toujours.
- i = dq/dt écrit puis développé i = d(u_C·C)/dt = C·du_C/dt (« C est constante, elle sort de la dérivée »).
- Il ne rappelle pas que i est algébrique ; un élève le lui reproche (cf. commentaires).

## Définitions telles qu'écrites
- Condensateur : dit « un récepteur formé de deux plaques (صفائح) séparées par un isolant ». Au tableau : symbole avec un rectangle hachuré vert « Isolant » entre les deux armatures, A à gauche, B à droite, U_AB = U_C.
- q = U_c × C, avec sous chaque lettre « charge du condensateur », « tension (V) », « capacité (F) ». Charge en coulomb dit oralement.
- Capacité : « ce que contient le condensateur », comparée au volume de la bouteille (2 L), la charge étant l'eau qu'il y a dedans. Le mot « armature » n'est pas employé (il dit « plaques »).
- Régime transitoire / permanent : dits oralement en regardant la courbe (partie qui monte / partie plate où la tension ne change plus), pas écrits.
- Échelon de tension, constante de temps comme mot défini, énergie emmagasinée : **absents**.

## Formules telles qu'écrites et dites
- i = dq/dt = C·du_C/dt (le « dt » ressemble à « dr » au tableau).
- Associations : C_éq = C₁ + C₂ (parallèle, dessin de deux condensateurs l'un au-dessus de l'autre) | C_éq = C₁·C₂/(C₁ + C₂) (série). Dit : « l'inverse des résistances ».
- Charge, panneau à 4 cases « u_C(t) | q(t) / u_R(t) | i(t) » :
  - u_C : Σ U(r) = Σ U(g) → u_C + u_R = E → u_C + R·i = E → **u_C + RC·du_C/dt = E** (dans l'exercice, écrit RC·du_C/dt + u_C = E).
  - q : idem, encadré « q = u_C·C ⇒ u_C = q/C » → **q/C + R·dq/dt = E**.
  - u_R : on **dérive** toute la loi d'additivité : du_C/dt + du_R/dt = 0, puis on **multiplie par C** : C·du_C/dt + C·du_R/dt = 0, soit i + C·du_R/dt = 0 → **u_R/R + C·du_R/dt = 0** (encadré vert « u_R = R·i ⇒ i = u_R/R »).
  - i : même dérivation → C·du_C/dt + C·d(R·i)/dt = 0 → **i + RC·di/dt = 0**.
  - Dit : « SVT : seulement u_C et q ; PC : apprenez aussi u_R et i, c'est tombé récemment au national ».
- Solution (charge) : u_C(t) = A(1 − e^(−t/τ)). Méthode écrite ligne par ligne :
  1. développer : u_C = A − A·e^(−t/τ) ;
  2. dériver : du_C/dt = 0 − A × d(e^(−t/τ))/dt = −A × (−1/τ)·e^(−t/τ) = +(A/τ)·e^(−t/τ) ; à côté, un encadré bleu-mnémo avec des **petits visages souriants** : d(e^(☺t))/dt = ☺·e^(☺t) (« ce qui est collé à t descend devant »).
  3. remplacer : A − A·e^(−t/τ) + RC·(A/τ)·e^(−t/τ) = E ;
  4. factoriser : A·e^(−t/τ)·(RC/τ − 1) = E − A, puis accolade « RC/τ − 1 = 0 ⇔ τ = RC » et « E − A = 0 ⇔ E = A » ;
  5. **réécrire u_C = E(1 − e^(−t/RC))** — il insiste : sinon le point est perdu.
- Cas « vérifier que c'est la solution » : analogie 3x + 1 = 4, vérifier x = 1 ; on développe, on dérive, on remplace et on retrouve E — « E = E, donc u_C est solution de l'éq. diff. ».
- Intensité : i = C·du_C/dt = C × E/(RC)·e^(−t/RC) → encadré **i = (E/R)·e^(−t/RC)** et à part **I₀ = E/R**.
- Décharge (circuit C ∥ R seul) : u_C + RC·du_C/dt = 0 ; q/C + R·dq/dt = 0 ; u_R/R + C·du_R/dt = 0 ; i + RC·di/dt = 0. Dit : « même chose, E devient 0 ».
- Solution décharge : u_C(t) = A·e^(−t/τ), « A = ? τ = ? » ; dérivée −(A/τ)·e^(−t/τ) ; A·e^(−t/τ)(1 − RC/τ) = 0 ⇒ τ = RC ; puis **conditions initiales** : u_C(0) = E (lu sur la courbe) et u_C(0) = A·e⁰ = A ⇒ A = E ; encadré u_C(t) = E·e^(−t/RC) ; i = C·du_C/dt = −(E/R)·e^(−t/RC).
- Dimension de τ (exercice) : τ = RC ⇒ [τ] = [R]×[C] ; de U = R·I : [R] = [U]/[I] ; de i = C·du/dt : [I] = [C]·[U]/[t] ⇒ [C] = [I]·[t]/[U] ; produit : [τ] = [U]/[I] × [I]·[t]/[U] = [t] — « τ a la dimension d'un temps, en s ».
- Aucune solution générale A·e^(−αt) + B, aucune écriture du/dt + u/(RC) = E/(RC).

## Méthodes graphiques
- Courbe u_C(t) de charge dessinée : asymptote pointillée E, tangente verte à l'origine coupant l'asymptote à t = τ, ordonnée 0,63·E marquée. Dit : « si la tangente n'est pas donnée, prends le maximum × 0,63 et projette **sur la courbe**, pas sur la droite ». Exemple oral : 10 × 0,63 = 6,3.
- Décharge : courbe décroissante, 0,37·E, τ ; règle dite « charge → 0,63, décharge → 0,37 ».
- Dans l'exercice, τ lu sur i(t) : tangente à l'origine de i(t) qui coupe l'axe des temps.
- 5τ, ln, courbes non temporelles, du/dt = f(u) : absents.

## Montages
- Montage-type : générateur E (cercle) – R – interrupteur K avec positions (1) et (2), C, et R' sur la branche de décharge ; légende « (1) charge (2) décharge ». Analogie : remplacer R par une lampe qui s'allume encore après qu'on a retiré la pile.
- Fléchage (question 1) : on suit le courant depuis le + du générateur, flèches bleues de i ; u_R et u_C dessinés contre i.
- Oscilloscope (question 2) : règle « **la tête de la flèche de la tension va sur la voie (Y), l'autre bout à la masse** » (il dit « القمقوم » puis « la masse », pas « المشطة »), symbole masse à trois traits. Il le montre pour u_R puis pour u_C. Pas de « −u_R », pas d'« inverser », pas d'ExAO.
- Générateur de courant (q = I·t) : absent.

## Exemples chiffrés et analogies
- Devoir : E = 12 V ; courbe i(t) avec I₀ = 0,6 mA, intercepte de la tangente marquée « 3 » sur l'axe t (s). R = E/I₀ = 12/(0,6·10⁻³) = 20 kΩ (il dit « 200 mille » puis corrige en 20 kΩ). τ écrit **0,3 s** puis C = τ/R = 0,3/20 000 = **1,5·10⁻⁴ F** — faux deux fois (lecture : le graphique porte 3 s ; et 0,3/20 000 = 1,5·10⁻⁵). Avec τ = 3 s, C = 1,5·10⁻⁴ F est juste. Puis C équivalent à C₁ ∥ C₂ avec C₁ = 2C₂ : C = 3C₂ ⇒ C₂ = 5·10⁻⁵ F, C₁ = 10⁻⁴ F (l'énoncé disait d'abord « en série », il le corrige en « parallèle »).
- Analogies : bouteille / « قرعة » à remplir (charge = eau dedans, capacité = volume, débrancher le robinet = garder la charge) ; lampe qui reste allumée puis s'éteint peu à peu (décharge) ; équation 3x + 1 = 4 pour « vérifier une solution » ; le menuisier qui devient habile par répétition.

## Insistances, erreurs citées, méthodes, conseils
- « Quatre équations différentielles, pas une » (u_C, q, u_R, i), en charge et en décharge — répété ≥ 5 fois.
- Toujours commencer par la loi d'additivité, puis Ohm, puis i = C·du_C/dt (ou dq/dt selon la grandeur demandée).
- Pour u_R et i : « dérive tout, puis multiplie par C » ; il reconnaît que c'est le point où les élèves bloquent et refait la démonstration une deuxième fois exprès.
- Après avoir trouvé A et τ, **réinjecter** dans la solution : « beaucoup s'arrêtent là au national et perdent le point ».
- Deux formes de question sur la solution : « trouve A et τ » vs « vérifie que… est solution ».
- « L'électricité est facile : ce que tu vois dans le cours est exactement ce qui tombe au devoir et au national. »
- Oscilloscope : « très demandé au national, beaucoup l'ignorent ».
- Aucun national cité avec année ou session ; le « devoir » est un devoir de lycée (partie nucléaire + RC).

## Faux, approximatif ou hors programme
- **τ lu 0,3 s** alors que la courbe porte 3 s (relevé par les élèves, 3 commentaires), et C = 0,3/20 000 annoncé 1,5·10⁻⁴ F (incohérent).
- Dit « τ = RC est le titre du cours ». Il ne dit pas que i est algébrique ; à la décharge il trouve i négatif sans expliquer pourquoi (sens réel du courant inversé).
- « Le condensateur se remplit d'électrons » / « une plaque se charge en +, l'autre en − » : correct, mais l'image « remplir d'électricité » laisse croire que la charge totale augmente (il faut dire +q et −q).
- Le condensateur de décharge dit « en parallèle avec la résistance » : tolérable pour un circuit à deux dipôles, mais ambigu.
- Rien d'hors programme (pas de Laplace, impédance, sinusoïdal…). **L'énergie E_e = ½·C·u_C² est absente**, ce qu'un élève signale.

## Commentaires d'élèves (150 lus)
- ≈ 90 % sont des vœux de réussite « Bac 2026 » et des remerciements (« explication simple », « qualité »).
- Erreurs pointées : τ = 3 s et non 0,3 (1 commentaire avec 3 likes, « 42:15 0.03 » un autre) ; montage de l'oscilloscope oublié à la question 31:01-31:15 (2 commentaires, sur le ton de la blague) ; équation en q « il fallait multiplier par C » (1) ; « i est une valeur algébrique, elle peut être opposée à la tension » à 4:00 (1).
- Contenu manquant demandé : énergie emmagasinée (2), dipôle RL (4), exercices plus difficiles (1), plus de nationaux (1).
- Difficulté : « 10 minutes et je n'ai rien compris » (1), « l'électricité est difficile sans exercices » (1). Une critique en faveur d'autres chaînes.
- Questions à servir au tuteur : « Pourquoi i est négatif à la décharge ? » → le courant circule dans le sens opposé à celui choisi comme positif ; u_C diminue donc du_C/dt < 0 et i = C·du_C/dt < 0. « Faut-il multiplier par C l'équation en q ? » → non, q/C + R·dq/dt = E est déjà juste ; multiplier par C donne RC·dq/dt + q = C·E, forme équivalente.

## Ce que notre cours doit lui prendre
1. **Le tableau à quatre cases** u_C | q / u_R | i pour les équations différentielles, même départ (Σ U(r) = Σ U(g)) dans chaque case, et le geste « dérive tout, puis × C » pour u_R et i.
2. **La méthode d'identification en 5 lignes** (développer, dériver, remplacer, factoriser par A·e^(−t/τ), deux accolades τ = RC et A = E) puis la réécriture finale obligatoire ; l'encadré mnémo de dérivée de l'exponentielle (« ce qui est collé à t descend devant »).
3. La distinction **« trouve A et τ » / « vérifie que… est solution »**, avec l'analogie 3x + 1 = 4.
4. La règle d'oscilloscope « tête de flèche → voie Y, queue → masse », appliquée après avoir fléché i puis u contre i aux récepteurs.
5. L'analyse dimensionnelle de τ écrite sur trois lignes ([R] = [U]/[I], [C] = [I][t]/[U], produit).
6. Le panneau de rappels permanent (générateur / récepteur / Ohm avec unités sous les lettres).
À corriger chez nous : lire τ correctement sur l'axe (et vérifier par le calcul C = τ/R), dire i algébrique avant la décharge, ajouter l'énergie ½·C·u_C², le mot « armatures » et +q/−q.
