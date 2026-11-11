# Audit — hstTUKPqT5s — Prof Atif, « dipole RC 2bac, cours complet جميع الحالات »

## Fiche
- id : hstTUKPqT5s ; professeur : Prof Atif ; durée 1780 s (29 min 40) ; 7 531 vues ; publiée le 24/12/2024.
- Support : **feuilles A3/A4 manuscrites préparées d'avance** (stylo noir, titres en rouge, résultats encadrés), filmées du dessus ; il pointe au stylo rouge et ajoute quelques lignes en rouge en direct ; **feuille de brouillon** posée par-dessus pour les rappels de maths. Pas de tableau, pas de classe, pas de simulation.
- Transcription : 379 lignes, mais de très mauvaise qualité (voix basse, beaucoup de segments vides ou incompréhensibles, surtout 0:00–4:00, 6:00–8:00, 12:57–14:11, 23:02–26:00) : **le contenu a été reconstitué surtout par les 44 images lues**.
- Pourquoi elle compte : la plus « calculatoire » du lot. Elle établit **toutes** les équations différentielles de charge (en u_C, en q, en u_R, en i) puis la décharge, et montre **la méthode d'identification** pour trouver A et τ, avec des rappels de maths sur brouillon. Courte, dense, fidèle au format « fiche ».

## Plan horodaté
| Temps | Notion | Durée |
|---|---|---|
| 0:00–1:25 | Rappel conducteur ohmique : convention récepteur, loi d'Ohm, associations série/parallèle de résistances | ~1 min 30 |
| 1:25–4:05 | Condensateur : symbole, armatures A et B, q_A = q, q_B = −q, u_C = q/C, unités ; associations de condensateurs (série/parallèle), « augmente / diminue la capacité » | ~2 min 40 |
| 4:05–6:00 | Générateur idéal de tension / de courant ; I₀ = q/t ; i = dq/dt avec q = C·u_C ⇒ i = C·du_C/dt (dérivée « prime » des maths = d/dt) | ~2 min |
| 6:00–7:55 | Circuit avec interrupteur K (positions 1 et 2), fléchage u_C, u_R, i ; position 1 = charge, 2 = décharge | ~2 min |
| 7:55–13:00 | **Équations différentielles de charge** en u_C, q, u_R, i (additivité des tensions) | ~5 min (le plus long bloc) |
| 13:00–14:11 | Circuit de décharge : u_R + u_C = 0, mêmes équations « avec 0 à droite » | ~1 min |
| 14:11–15:30 | Oscilloscope : une entrée (voie) + masse, branchement pour visualiser u_C | ~1 min 20 |
| 15:30–17:00 | Les trois formes de solution : A(1 − e^(−αt)), A + B·e^(−t/τ), A + B·e^(−αt) ; « refais les exercices » | ~1 min 30 |
| 17:00–19:00 | Rappels de maths sur brouillon : (e^(u))' = u'·e^(u), (a·f)' = a·f', dérivée de 3(5 − 7x) | ~2 min |
| 19:00–22:55 | **Report dans l'équation, factorisation, identification** (5x + b = ax + 7 ⇒ a = 5, b = 7) ⇒ A = E et RC/τ − 1 = 0 ⇒ τ = RC ; e^x ≠ 0 | ~4 min |
| 23:00–24:50 | Analyse dimensionnelle de τ | ~2 min |
| 24:50–26:00 | Courbe de charge : régime transitoire / permanent, 5τ | ~1 min |
| 26:00–28:57 | Décharge : solution u_C = A·e^(−αt), α = 1/RC, condition initiale u_C(0) = E ⇒ A = E ; « produit nul » | ~3 min |
| 28:57–29:40 | Détermination graphique de τ : tangente à l'origine, 0,63·E ; annonce des exercices dans la vidéo suivante | ~40 s |

Les longs séjours : établissement des équations différentielles (≈ 5 min) et identification A/τ (≈ 4 min + 3 min pour la décharge) — c'est là que la difficulté est.

## Rappels du tronc commun / 1re
- Feuille « **Rappel conducteur ohmique** » : schéma en **convention récepteur** (flèche de i dans un sens, flèche u_R en sens opposé sous la résistance), mot « Récepteur » écrit. Loi d'Ohm écrite **u_R = R·i** (« Ri ») avec u_R : tension (V), R : résistance (Ω), i : intensité (A).
- Associations de conducteurs : série R_éq = R₁ + R₂ ; parallèle 1/R_éq = 1/R₁ + 1/R₂ puis réduit au même dénominateur R_éq = R₁R₂/(R₁ + R₂) (il le présente comme « la règle à retenir quand il n'y en a que deux »).
- i = dq/dt rappelé encadré ; il insiste que « prime » des maths s'écrit d/dt en physique.
- Additivité des tensions : chaque équation commence par la phrase écrite « d'après la loi d'additivité des tensions ».
- Rappels de maths (brouillon) : dérivée de l'exponentielle composée, constante sortie de la dérivée, identification des coefficients, e^x ≠ 0, « xy = 0 ⇒ x = 0 ou y = 0 ».

## Définitions telles qu'écrites
- Condensateur : dessin de deux plaques face à face (armatures A et B, mot « armature » avec flèche), courant i arrivant sur A, flèche u_C. Pas de phrase de définition écrite.
- « C : capacité de condensateur (F) farad » ; « q : charge de condensateur (C) coulomb » ; q_B = −q ; q_A = q (dit : A reçoit les charges positives, B les négatives).
- Régime transitoire / régime permanent : seulement écrits sur la courbe (au-dessus de la montée et du palier), pas définis en phrase.
- « τ = RC », annoté en rouge **« constante de temps (s) »**.
- Échelon de tension, énergie emmagasinée : **non traités**.

## Formules telles qu'écrites (et dites)
- Encadré **u_C = q/C** (dit « u_C égale q sur C », écrit avec q au numérateur et non q = C·u_C) ; plus loin « avec q = C·u_C ».
- Générateur idéal de tension : symbole (cercle traversé, flèche E, « tension cst ») ; à côté, encadré i = dq/dt (placement trompeur : c'est la relation générale, pas propre au générateur de tension).
- Générateur idéal de courant : symbole (cercle + flèche I₀, « courant cst »), encadré **I₀ = q/t** (dit : q = I·t, t la durée de fonctionnement). u_C = I₀·t/C **non écrit**.
- Ligne : « i = dq/dt, avec q = C·u_C donc **i = C·du_C/dt** » (encadré) — C sort de la dérivée « car c'est une constante ».
- Charge, en u_C (titre « Eq. diff vérifiée par u_C ») : u_R + u_C = E → R·i + u_C = E → encadré **RC·du_C/dt + u_C = E** (écrit « Rc »).
- Charge, en q : u_R + u_C = E → R·i + q/C = E → R·dq/dt + q/C = E → encadré **RC·dq/dt + q = EC** (il multiplie tout par C).
- Charge, en u_R : u_R + u_C = E → du_R/dt + du_C/dt = dE/dt → du_R/dt + i/C = 0 → **du_R/dt + u_R/(RC) = 0** (il remplace i par u_R/R ; il rappelle que la dérivée d'une constante est nulle).
- Charge, en i : R·i + u_C = E → d(Ri)/dt + du_C/dt = dE/dt → R·di/dt + i/C = 0 → encadré **RC·di/dt + i = 0**. Il écrit en rouge la forme générale **y' + a·y = c** pour dire « l'inconnue + sa dérivée × un nombre = un nombre ».
- Décharge : u_R + u_C = 0 → u_C + RC·du_C/dt = 0 (« les mêmes équations, il suffit de mettre 0 »).
- Solution de charge : (1) RC·du_C/dt + u_C = E, solution **u_C = A(1 − e^(−t/τ))** ; du_C/dt = A·(1/τ)·e^(−t/τ) ; on remplace dans (1) : A − A·e^(−t/τ) + RC·(A/τ)·e^(−t/τ) = E → A·e^(−t/τ)(RC/τ − 1) + A = E → **A = E et RC/τ − 1 = 0 ⇒ τ = RC**. Ordre des lignes très propre, recopiable.
- Trois formes annoncées sur brouillon : u_C = A(1 − e^(−αt)), u_C = A + B·e^(−t/τ), u_C = A + B·e^(−αt) ; « les inconnues sont A et α, ou A, B et τ ».
- Décharge : u_C = A·e^(−αt) ; du_C/dt = −Aα·e^(−αt) ; A·e^(−αt) + RC(−Aα·e^(−αt)) = 0 → A·e^(−αt)(1 − RCα) = 0 → 1 − RCα = 0 ⇒ **α = 1/RC** ; « à t = 0 : u_C(t=0) = E, u_C(t=0) = A·e^(−α·0) (e⁰ = 1) ⇒ E = A ». Ici A est trouvé par la **condition initiale** (à la charge, par identification).
- Analyse dimensionnelle : « L'équation dimensionnelle » [τ] = [R]·[C] ; [τ] = [U]/[I] · [I]·[t]/[U] = [t] = s. Il exige d'écrire d'où viennent [R] (u = R·i) et [C] (i = C·du_C/dt).
- i(t), u_R(t), q(t) explicites, E_e = ½·C·u_C² : **non traités**.
- Associations de condensateurs : parallèle **C_éq = C₁ + C₂** (« augmente la capacité ») ; série **1/C_éq = 1/C₁ + 1/C₂** (« diminue la capacité » ; exemple oral 6/5, plus petit que chacune). Il souligne que c'est « l'inverse » des résistances.

## Méthodes graphiques
- Courbe u_C(t) de charge : axes u_C(t) et t, asymptote E, **tangente à l'origine** en trait fin coupant l'asymptote, projection donnant τ ; ajout en rouge de **0,63E** sur l'axe, de **5τ**, et des mots « régime transitoire » (sur la montée) et « régime permanent » (sur le palier). Dit : deux méthodes, intersection tangente/asymptote, ou 0,63 × E projeté sur la courbe.
- Courbe de décharge : décroissance depuis E (marqué en rouge), tangente à l'origine jusqu'à l'axe des t, τ au point d'intersection. **0,37E non dit.**
- Pas de droite ln, pas de du/dt = f(u), pas de lecture sur i(t)/u_R(t).

## Montages
- Circuit unique : générateur E (flèche vers le haut), interrupteur K à deux positions (1) et (2), C puis R en série ; flèches rouges u_C (sur C) et u_R (sur R) opposées à i ; « Si l'interrupteur à la position (1) : le condensateur est en charge ; position (2) : en décharge ». Petits schémas séparés « circuit en charge » et « circuit de décharge » (décharge : C et R seuls, u_C et u_R fléchés).
- Générateur idéal de courant : seulement symbole + I₀ = q/t, pas de montage dédié ni de u_C linéaire.
- Oscilloscope : dit que l'appareil « montre les courbes de n'importe quelle grandeur », a une entrée (voie) et une masse ; dessine en rouge **Y au-dessus de C et la masse entre C et R** pour visualiser u_C. Pas de −u_R, pas d'inversion, pas d'ExAO.

## Exemples chiffrés et analogies
- Aucun exemple chiffré E/R/C/τ. Exemples de maths seulement : 3(5 − 7x), e^(3x), identification 5x + b = ax + 7.
- Aucune analogie physique.

## Ce sur quoi il insiste
- Toujours écrire « d'après la loi d'additivité des tensions » avant l'équation.
- Pour l'équation différentielle : « isole UNE variable (u_C, q ou i) et garde la forme y' + a·y = c ».
- La méthode A/τ : dériver, remplacer, factoriser, identifier ; « ce n'est pas facile, refais les exercices et retiens la méthode par la pratique ».
- Dans l'analyse dimensionnelle, écrire les relations utilisées (u = R·i, i = C·du/dt).
- Pas de national cité, pas d'erreurs d'élèves citées explicitement.

## Faux, imprécis ou hors programme
- Encadré i = dq/dt rangé sous « générateur idéal de tension » : confusion de mise en page, à ne pas reproduire.
- Notation **I₀ = q/t** : vraie seulement si q(0) = 0 ; préférer q = I₀·t.
- Lettres « Rc », « (Ri) », A et B des armatures pas toujours cohérentes ; τ et α mélangés au fil des formes.
- Rien d'hors programme PC (pas de Laplace, ni de sinusoïdal, ni de séparation des variables). Énergie et i(t) manquent (lacunes, pas fautes).

## Commentaires d'élèves (10 seulement)
- 7 remerciements (« très bonne explication », « merci », cœurs) ; 1 « explication au niveau, on veut un exercice » ; 1 « faites-nous RL » (3 likes) ; aucun horodatage, aucune question de fond. Demande récurrente implicite : **des exercices** après le cours.

## Ce que notre cours doit lui prendre
1. **Les quatre équations différentielles de charge (u_C, q, u_R, i) dans le même gabarit** : titre « Éq. diff vérifiée par … », phrase « d'après la loi d'additivité », 3–4 lignes, résultat encadré ; puis décharge = « même chose avec 0 ».
2. La forme rouge **y' + a·y = c** comme repère visuel de « l'équation est finie ».
3. **L'ordre des lignes de l'identification** (dériver → remplacer → factoriser e^(−t/τ) → A = E et RC/τ − 1 = 0), précédé d'un mini-rappel de maths (dérivée de e^(u), identification sur 5x + b = ax + 7) — c'est le vrai prérequis caché.
4. Le contraste charge / décharge : A trouvé par identification d'un côté, par la condition initiale u_C(0) = E de l'autre (e⁰ = 1).
5. L'analyse dimensionnelle de τ en deux lignes [U]/[I] · [I][t]/[U].
6. La courbe annotée (tangente, 0,63E, 5τ, régime transitoire/permanent) — à compléter par 0,37E pour la décharge, l'énergie, i(t) et des exemples chiffrés, absents ici.
