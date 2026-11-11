# Audit — gm5vLzAjBms — Prof B. Mouslim (Cours du Soir PC)

## Fiche
- **id** : gm5vLzAjBms — **professeur** : Badr Mouslim, chaîne « Cours du Soir PC »
- **titre** : « Cours + Astuces – Dipôle RC (de A à Z) – Électricité – 2 Bac Biof » — **durée** 5027 s (1 h 24) — **vues** ≈ 13 000 — publié le 9/12/2024
- **support** : tablette (diapos à deux colonnes, en-tête « ELECTRICITÉ / Dipôle RC / 2 BAC BIOF »). Schémas et courbes **imprimés** (circuit avec K, courbes sur papier millimétré), annotés à la main au stylet de couleur. Il surligne beaucoup (jaune, vert). Voix couverte par une musique de fond : **sous-titres automatiques presque vides** (640 lignes, surtout des fragments et « [موسيقى] »). L'audit repose donc à 90 % sur les images du tableau (70 lues).
- **pourquoi elle compte** : c'est le cours **le plus complet en dérivations écrites** : les **quatre équations différentielles** (u_C, q, i, u_R) en charge **et** en décharge, i(t) de charge et de décharge avec les courbes, la **discontinuité de i** expliquée avec un dessin, τ par **deux méthodes** en charge et en décharge, l'**énergie démontrée** par la puissance, et l'**association des condensateurs** démontrée. Pas d'exemple chiffré, pas d'exercice.

## Plan horodaté (durée = difficulté perçue)
| temps | notion | durée |
|---|---|---|
| 0:00–7:40 | dipôle RC, condensateur (définition, symbole, armatures, diélectrique, q = q_A = −q_B), capacité et sous-multiples, condensateur réel (résistance de fuite) | 7 min |
| 8:40–13:00 | relation q–i (i = dq/dt ; I = Q/Δt), q = C·u_C, i = C·du_C/dt | 4 min |
| 13:00–23:40 | **association série et parallèle** (démonstrations, cas général, intérêt) | **10 min** |
| 23:50–30:40 | échelon montant / descendant, montage K (1)/(2), oscilloscope, régimes transitoire / permanent, continuité de u_C | 7 min |
| 30:50–39:00 | **charge : équations différentielles en u_C, q, i, u_R** | **8 min** |
| 39:00–47:00 | **solution A + B·e^(−αt), détermination de A, α, B** | **8 min** |
| 47:00–53:00 | q(t) et **i(t) de charge** (dérivation, courbe, i(∞) = 0, condensateur = interrupteur ouvert) | 6 min |
| 53:00–1:06:00 | **décharge** : 4 équations, solution A·e^(−βt), u_C(t), q(t), **i(t) négatif** | **13 min** |
| 1:06:00–1:07:10 | remarque : u_C continue, i discontinu (dessin charge→décharge) | 1 min |
| 1:07:10–1:12:30 | τ = RC, analyse dimensionnelle | 5 min |
| 1:12:50–1:19:20 | **lecture de τ** : 0,63E / tangente–asymptote (charge) ; 0,37E / tangente–axe des temps (décharge) | 6,5 min |
| 1:19:20–1:24:00 | **énergie emmagasinée** : P = u·i → E_e = ½·C·u_C² → E_e = q²/(2C) | 5 min |

Les longs séjours : association (10 min, inhabituel), les équations différentielles et leur solution (16 min en charge, 13 en décharge).

## Rappels du tronc commun / 1re
- **Convention récepteur** : sur le symbole agrandi, flèche i (verte) entrant par l'armature A, flèche u_C (jaune) en sens opposé sous le condensateur ; électrons e⁻ sortant de B. Sur le circuit imprimé : u_R et u_C fléchés vers le haut, i vers le bas dans la branche R–C.
- **Loi d'additivité des tensions** : écrite à chaque fois en toutes lettres : « On applique la loi d'additivité des tensions : U_R + U_C = E » (et U_AB = U_AD + U_DB pour la série).
- **Loi d'Ohm** : « D'après la loi d'Ohm U_R = R × i ». Réutilisée sous la forme i = U_R/R (encart) pour l'équation en u_R.
- **i = dq/dt** : « intensité variable → i(t) = dq/dt » à côté de « intensité continue (I_dc) → I = Q/Δt », unités fléchées (A), (C), (s).
- **Loi des nœuds** (parallèle) : i = i₁ + i₂.
- **Maths** : e⁰ = 1, lim e^x (x→−∞) = 0, e^(−∞) = 0, dérivée de e^(−αt) = −α·e^(−αt), constante sortie de la dérivée.

## Définitions telles qu'écrites
- **Condensateur** : « dipôle constitué de deux conducteurs appelés armatures séparés par un diélectrique ».
- **Diélectrique** : « (isolant électrique) [verre, plastique, vide…] ».
- **Charge** : « q : la charge (C) : [quantité d'électricité] » ; |q_A| = |q_B| ; q = q_A = −q_B → Coulomb (C).
- **Capacité** : « C : capacité du condensateur → Farad (F) » ; mF, µF, nF, pF = ×10⁻³, 10⁻⁶, 10⁻⁹, 10⁻¹² F.
- **Échelon de tension** : « ascendant » {u = 0 pour t < 0 ; u = E pour t ≥ 0} et « descendant » (diapos imprimées).
- **Régime transitoire** : « la tension u_C(t) augmente ou diminue ». **Régime permanent** : « la tension u_C(t) reste constante » (u_C = E en charge, u_C = 0 en décharge, écrits à la main sur les courbes).
- **Constante de temps** : « τ = RC » ; « la constante τ a la dimension d'un temps ⇒ elle est exprimée en seconde (s) ».
- **Énergie** : titre « Énergie emmagasinée dans un condensateur », pas de phrase de définition, seulement la démonstration.

## Formules — telles qu'écrites (ordre des lignes)
- **q = C × U_C** (encadré, unités fléchées (C) (F) (V)). Majuscule U_C au début, u_C minuscule sur les diapos imprimées.
- **i = C·dU_C/dt** : « On a : i(t) = dq/dt et q = C × U_C » → i(t) = d(C·U_C)/dt → encadré i(t) = C·dU_C/dt (C entouré : constante sortie).
- **Charge, équation en u_C** : U_R + U_C = E ; U_R = R × i, i = dq/dt, q = C·U_C → i = C·dU_C/dt → U_R = R × C·dU_C/dt → **RC·dU_C/dt + U_C = E**, RC surligné et renommé τ : « On pose τ = RC » (encadré).
- **Charge, en q** : U_R + U_C = E → R × i + U_C = E → (encart q = C·U_C ⇒ U_C = q/C ; i = dq/dt) → R·dq/dt + q/C = E → ×C → RC·dq/dt + q = C·E (dit).
- **Charge, en i** (rare chez les profs) : on dérive toute l'équation : d/dt(R·i + U_C = E) → R·di/dt + dU_C/dt = dE/dt = 0 (E constante, barrée) ; dU_C/dt = i/C → C × (R·di/dt + i/C) = 0 → **RC·di/dt + i = 0** (encadré).
- **Charge, en u_R** : d/dt(U_R + U_C = E) → dU_R/dt + dU_C/dt = 0 → dU_R/dt + i/C = 0 → dU_R/dt + (1/C)·U_R/R = 0 → RC·dU_R/dt + U_R = 0.
- **Solution (charge)** : encadré **U_C(t) = A + B·e^(−αt)** (variante notée à côté : U_C(t) = A(1 − e^(−αt))). « Détermination de A, B et α : » dU_C/dt = dA/dt (= 0) + B·d(e^(−αt))/dt → encadré dU_C/dt = −Bα·e^(−αt). « On remplace dans l'éq. diff. » : RC × (−Bα)·e^(−αt) + A + B·e^(−αt) = E → B·e^(−αt)[−RCα + 1] = E − A, les deux crochets « = 0 » (le membre de gauche dépend du temps, celui de droite non) → système {−RCα + 1 = 0 ; E − A = 0} ⇒ **α = 1/RC ; A = E**. « Pour déterminer B (les conditions initiales) : initialement le condensateur déchargé (U_C(t=0) = 0) » → U_C(0) = E + B = 0 ⇒ **B = −E** (rappel e⁰ = 1).
- **Résultat** : « L'expression de la tension aux bornes du condensateur pendant la charge est : **U_C(t) = E(1 − e^(−t/τ))** » ; {t = 0 ⇒ U_C = 0 ; t → +∞ ⇒ U_C(∞) = E}.
- **q(t) charge** : q(t) = C × U_C(t) = C·E(1 − e^(−t/τ)), **Q_max = C·E** surligné ; q(0) = 0 ; q(∞) = C × E.
- **i(t) charge** : deux voies écrites (i = C·dU_C/dt / i = dq/dt), il prend dq/dt : q = CE − CE·e^(−t/τ) → dq/dt = d(CE)/dt (= 0) − CE·d(e^(−t/τ))/dt, avec (−1/τ)·e^(−t/τ) → dq/dt = +(CE/τ)·e^(−t/τ) = CE/(R×C)·e^(−t/τ) → **i(t) = (E/R)·e^(−t/τ)**, « I_max = I₀ = E/R » ; i(t=0) = E/R et i(t→∞) = 0.
- **Décharge** : « U_R + U_C = 0 (absence du générateur) » → R × i + U_C = 0 → **RC·dU_C/dt + U_C = 0** ; puis en encadrés rouges : RC·dq/dt + q = 0 ; RC·di/dt + i = 0 ; RC·dU_R/dt + U_R = 0 (dit en français : « on fait les mêmes étapes »).
- **Solution (décharge)** : U_C = A·e^(−βt), « A et β deux constantes » ; dU_C/dt = −βA·e^(−βt) ; RC × (−βA·e^(−βt)) + A·e^(−βt) = 0 → A·e^(−βt)[−RCβ + 1] = 0, avec « ≠ 0 » sous A·e^(−βt) → β = 1/RC ; « Détermination de A : [on utilise les C.I.] U_C(t=0) = E » → A = E → **U_C(t) = E·e^(−t/τ)** ; U_C(0) = E, U_C(∞) = 0 V.
- **q(t) décharge** : q = CE·e^(−t/τ), CE souligné « Q_m » ; q(0) = C × E, q(∞) = 0.
- **i(t) décharge** : i = C·dU_C/dt avec dU_C/dt = −(E/RC)·e^(−t/τ) → i(t) = −(E/RC) × C·e^(−t/τ) → encadré **i(t) = −(E/R)·e^(−t/τ)**, « I₀ = I_m » ; i(0) = −E/R (surligné), i(∞) = 0.
- **τ, dimensions** : [τ] = [R] × [C] ; loi d'Ohm U = R × i ⇒ [R] = [U]/[I] ; « pour un condensateur » i = C·dU_C/dt ⇒ [I] = [C] × [U]/[T] ⇒ [C] = [I]·[T]/[U] ; [τ] = [U]/[I] × [I]·[T]/[U] = [T].
- **Énergie** : encadré P = U × i « → puissance électrique » ; P = U_C × i et i = C·dU_C/dt → P = C × U_C × dU_C/dt = d/dt(½·C·U_C²) (flèche : on reconnaît la dérivée) ; « et on sait que : P = dE_e/dt » ⇒ « Donc : **E_e = ½·C·U_C²** » ; E_e(t) = ½·C·U_C²(t) → « la charge : ½·C·E²(1 − e^(−t/τ))² » ; « la décharge : ½·C·E²(e^(−t/τ))² » ; « ⇒ régime permanent : U_C = cte » (E_e max = ½·C·E²). Puis q = C × U_C ⇒ U_C² = (q/C)² → E_e = ½·C × (q/C)² = ½ × C/C² × q² → encadré **E_e = q²/(2C)** (écrit ½C au dénominateur). Symbole **E_e**, jamais W ni ξ ; aucune unité (J) écrite sur les images lues.
- **Associations** : série (« même intensité », q = q₁ = q₂) : U_AB = U_AD + U_DB ; U_AD = q₁/C₁, U_DB = q₂/C₂, U_AB = q/C → q/C = q₁/C₁ + q₂/C₂ → q barré → **1/C = 1/C₁ + 1/C₂** ⇒ C = C₁C₂/(C₁ + C₂) ; « en général » 1/C = Σ 1/Cᵢ ; « Intérêt : diminue la capacité ». Parallèle (« même tension ») : loi des nœuds i = i₁ + i₂, « i = q/t ; i₁ = q₁/t ; i₂ = q₂/t » → q = q₁ + q₂ ; C·U_AB = C₁·U_AB + C₂·U_AB → **C = C₁ + C₂** ; « en général C = Σ Cᵢ » ; « Intérêt : C > C₁ et C > C₂ ».

## Méthodes graphiques
- **Charge, méthode 1** : on remplace t par τ : U_C(τ) = E(1 − e^(−1)) → encadré **U_C(τ) = 0,63E** ; « τ est l'abscisse correspondant à l'ordonnée 0,63E ». Sur la courbe millimétrée : E entouré, trait pointillé horizontal jaune à 0,63·E jusqu'à la courbe, puis vertical jusqu'à τ.
- **Charge, méthode 2** : « τ est l'abscisse du point d'intersection de la tangente à t = 0 et l'asymptote (U_C = E) » ; tangente bleue depuis l'origine jusqu'à la droite pointillée E, verticale vers τ.
- **Décharge, méthode 1** : U_C(τ) = E·e^(−1) (flèche « 0,37 ») → **U_C(τ) = 0,37E** ; « τ est l'abscisse correspondant à l'ordonnée 0,37E ».
- **Décharge, méthode 2** : « τ est l'abscisse du point d'intersection de la tangente à t = 0 et l'axe des abscisses » (tangente violette depuis E, axe des temps surligné jaune, asymptote 0 en vert).
- **Absents** : lecture de τ sur i(t) ou u_R(t) (alors que la courbe i(t) est au tableau), 5τ / durée du régime transitoire, courbe ln, du/dt = f(u). C'est le manque principal de la vidéo pour les questions d'examen.
- **Continuité** (1:06) : charge puis décharge dessinées à la suite ; à l'instant de bascule, pointillé vertical : « U_C(t⁻) = U_C(t⁺) : U_C est continue » ; sur i(A) : +E/R qui décroît vers 0, puis **saut à −E/R** et retour vers 0 : i(t⁻) ≠ i(t⁺), **i discontinu**. Déjà annoncé à 28:30 (« i = dq/dt discontinue » griffonné), ce qui a laissé un élève sans réponse jusque-là.

## Montages, oscilloscope
- Circuit imprimé : générateur E (cercle, flèche E vers le haut), i, interrupteur **K à deux positions ① (gauche, charge) et ② (droite, décharge)**, A, R (u_R), B, C (u_C), M relié à la masse ; flèche rouge « Entrée Y » sur B. Sous les deux courbes : « Interrupteur K à la position ① / ② ».
- **Oscilloscope** : petit croquis (voies Y₁, Y₂, masse). Règle dite : on relie la voie à la borne du côté de la **pointe de la flèche** de la tension et la masse à l'autre ; visualiser u_C (« visualiser » écrit). Pas de « −u_R » ni du bouton « inverser ».
- **Générateur de courant** (q = I·t) : non traité. Un élève demande quand on sait que le générateur est idéal pour utiliser I = Q/t : sans réponse.
- **Condensateur réel** : C en parallèle avec R_f, « résistance de fuite (modélisation des pertes) », ordre de grandeur « × MΩ » — **hors programme PC**.
- Le condensateur en régime permanent dessiné comme **interrupteur ouvert** → i = 0 (belle image).

## Exemples chiffrés, analogies
- **Aucun exemple chiffré** dans tout le cours (ni E, ni R, ni C, ni τ en valeurs). Aucune analogie physique (réservoir, seau…). Une seule image concrète pour la série : « tu as besoin d'une petite capacité et tu n'as que des grandes : tu les mets en série ».

## Insistances, erreurs d'élèves, méthodes
- **Méthode type « établir l'équation différentielle »** toujours dans le même ordre écrit : loi d'additivité → loi d'Ohm → i = dq/dt → q = C·u_C → remplacer → multiplier par C si besoin. Pour i et u_R : **dériver l'équation entière** (dE/dt = 0).
- **Méthode type « trouver A, B, α »** : dériver la solution, remplacer, factoriser par e^(−αt), le terme qui dépend du temps et la constante sont nuls séparément, puis la condition initiale pour B. Il insiste : α et A viennent de l'équation, **B vient des conditions initiales**.
- **Signe de i en décharge** : il insiste que le moins veut dire que le courant **change de sens** (surlignage de −E/R) — erreur fréquente : écrire i positif en décharge.
- **Au carré** dans l'énergie : il prévient qu'on oublie le carré de U_C (et un élève demande d'où sort un carré : réponse = on élève U_C = q/C au carré).
- **Le ½** de l'énergie : vient de la dérivée de U_C² (2·U_C·dU_C/dt) ; un élève pointe 1:20:16 pour cela : point à montrer très lentement.
- Pas de session nationale citée, pas de conseil d'examen explicite lisible.

## Faux, approximatif, hors programme
- **Titre de diapo faux** à 1:01 : la solution de décharge est titrée « …pendant la **charge** est » (un élève le signale ; le prof le reconnaît). À ne pas reproduire.
- **i = q/t** dans la démonstration du parallèle (au lieu de dq/dt) : raccourci correct dans le résultat mais faux comme écriture ; dire plutôt « q = q₁ + q₂ car les deux condensateurs se chargent pendant le même temps », ou dériver.
- **Condensateur réel / résistance de fuite** : hors programme PC.
- **Associations série/parallèle** : au programme mais traitées longuement (10 min), sans exemple.
- Équation de charge en u_R écrite sans le RC final visible : vérifier l'écriture « RC·du_R/dt + u_R = 0 ».
- Notations mêlées : U_C / u_C, α (charge) puis β (décharge), I₀ = I_m = I_max, Q_m = Q_max.

## Commentaires d'élèves (51 lus)
- Remerciements très majoritaires (≈ 35) : « explication claire, directe, sans détour », « the best teacher ».
- **Qualité d'image** : 360p, écriture en jaune illisible (4 fois) → notre tableau doit garder le jaune pour le surlignage, jamais pour l'écrit.
- **28:15 « pourquoi l'intensité i est discontinue ? »** → réponse : u_C ne peut pas sauter (la charge ne s'accumule pas instantanément), mais i peut changer d'un coup : 0 juste avant la fermeture, E/R juste après ; puis +E/R → −E/R en basculant de la charge à la décharge (le courant change de sens).
- **1:20:16 « d'où vient le ½ dans la dérivée ? »** → d(½·C·u_C²)/dt = ½·C·2·u_C·du_C/dt = C·u_C·du_C/dt = P.
- **« d'où vient un carré ? »** (énergie en q) → u_C = q/C, donc u_C² = q²/C².
- **« Quand sait-on que le générateur est idéal pour utiliser I = Q/t ? »** → seulement quand l'énoncé parle d'un **générateur de courant** (intensité constante I₀) : q = I₀·t ; avec un générateur de tension, i varie et on n'utilise pas I = Q/t.
- **Erreur signalée** : décharge titrée « charge » (1 fois).
- Demandes : exercices difficiles RC et RL (2), vidéo à faire avant les contrôles (1).

## Ce que notre cours doit lui prendre
1. **Les quatre équations différentielles en tableau** (u_C, q, i, u_R) pour la charge **et** la décharge, avec la remarque : i et u_R ont la même équation à second membre nul dans les deux cas — et la méthode « dériver l'équation entière » pour i et u_R.
2. **La factorisation B·e^(−αt)[1 − RCα] = E − A** et la phrase « ce qui dépend du temps est nul, ce qui est constant est nul » : la meilleure présentation de la détermination de α et A ; puis B par la condition initiale (C déchargé).
3. **Le dessin de continuité** : charge puis décharge enchaînées, u_C continue, i qui saute de +E/R à −E/R ; et le **condensateur = interrupteur ouvert** en régime permanent (i = 0).
4. **L'énergie par la puissance** : P = u_C·i = C·u_C·du_C/dt = d(½·C·u_C²)/dt, puis E_e en charge, en décharge et au régime permanent (½·C·E²), puis E_e = q²/(2C) — en montrant lentement le ½ et le carré (deux questions d'élèves).
5. **Les deux méthodes de τ** écrites en phrase-réponse (« τ est l'abscisse correspondant à l'ordonnée 0,63E », « …de la tangente à t = 0 et de l'asymptote / de l'axe des temps ») — à compléter nous-mêmes par ce qui manque ici : τ sur i(t) (0,37·I₀), 5τ, exemples chiffrés, −u_R et l'oscilloscope.
