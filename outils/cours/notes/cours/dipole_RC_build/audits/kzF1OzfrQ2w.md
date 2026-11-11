# Audit — kzF1OzfrQ2w — Prof Noureddine, « Electricité - RC : Cours + Résumé »

## Fiche
- **id** : kzF1OzfrQ2w — **professeur** : Noureddine (chaîne Noureddine Physique) — **publiée** : 2 mai 2021.
- **titre** : « Electricité - RC: Cours + Résumé - Prof Noureddine | 2 BAC Biof » — **durée** : 3146 s (52 min 26) — **vues** : ≈ 753 000.
- **support** : vrai tableau noir (trois panneaux verts), craies de couleur (jaune pour les titres, orange pour les cadres et questions, bleu pour les courbes et les flèches), prof seul face caméra, pas d'élèves. Il efface et réécrit plusieurs fois.
- **source utilisée** : **aucune transcription** (pas de sous-titres arabes, deux essais) → audit fait **uniquement sur les images du tableau** (64 images lues) et les **150 commentaires**. Ce qui est « dit » n'est donc pas connu ; seul l'écrit est fiable.
- **pourquoi elle compte** : la plus vue du lot probable ; format « résumé + exercice type » : il ne refait pas le cours de A à Z, il pose les **formules utiles**, puis traite **un seul exercice complet** (charge par **générateur de courant**, décharge dans R, droite ln u_C, énergie). C'est le modèle d'une « fiche de révision qui se lit au tableau ». Aucune expérience, aucune définition longue.

## Plan horodaté (d'après les images)
| Temps | Notion | Durée |
|---|---|---|
| 0:00–1:00 | Générique noir | 1 min |
| 1:00–3:00 | Titre « Dipôle RC », annonce orale (R → Ω, C → F, flèches sous le titre) | 2 min |
| 3:00–8:00 | **Association des condensateurs** : parallèle (loi des nœuds → q_eq = q1 + q2 → C_eq = C1 + C2, « Intérêt : augmenter la capacité »), puis série (même i → q_eq = q1 = q2 → 1/C_eq = 1/C1 + 1/C2) | ≈ 5 min |
| 8:00–12:30 | **Générateurs** : « G. idéal de tension (95 %) » délivre une tension constante E ; « G. idéale de courant (5 %) » délivre I = cte, I₀ = q/t | ≈ 4 min |
| 13:00–16:30 | **Formules** (encadrés) : u_R = R·i, i = u_R/R, u_C = q/C, q = C·u_C, i = dq/dt, i = C·du_C/dt, I₀ = q/C (**erreur**, voir plus bas), E_e = ½·C·u_C², E_e = q²/(2C), « c'est une énergie électrique », unités sous les lettres (V, Ω, A, C, F, J) | ≈ 3,5 min |
| 17:00–24:00 | **Exercice, cas ①** : circuit générateur de courant I₀ = 1 µA, interrupteur K positions (1)/(2), C, R. « I/ K en position ① » : courbe u_C(t) droite de 0 à 5 V en 10 s. « 1/ Mq : u_C = (I₀/C)·t » ; « 2/ Calculer C » par analogie avec y = a·x → C = 2·10⁻⁶ F. Armatures A (+q) et B (−q), flèches de i et de u_C | ≈ 7 min (long séjour) |
| 28:00–37:00 | **Décharge** : « II/ À t = 10 s, on bascule K vers la position ② ». « 1/ Trouver l'éq. diff (u_C) » par la loi d'additivité des tensions ; « 2/ la solution s'écrit sous la forme u_C = A·e^(−αt) + B » ; dérivée, remplacement, identification α = 1/RC = 1/τ, B = 0 ; conditions initiales, continuité de u_C → A = U₀ | ≈ 9 min (**le plus long séjour**) |
| 41:00–43:00 | Graphe d'ensemble charge (rampe) + décharge (exponentielle) avec **changement d'origine des temps**, « u_C est une fonction continue » | ≈ 2–3 min |
| 43:00–49:00 | « 3/ » courbe **ln u_C = f(t)** droite décroissante → « Calculer R ? » | ≈ 5 min |
| 49:00–52:00 | « 4/ Déterminer t pour que l'E_e diminue de 30 % de sa valeur initiale » → t = −(RC/2)·ln(0,7) | ≈ 3 min |
| 52:20 | Carton final « EN COURANT » (lien vers la vidéo suivante) | — |

## Rappels du tronc commun / 1re
- **Loi des nœuds** écrite en tête du panneau 2 (« loi des nœuds : i = i1 + i2 ») pour démontrer le parallèle ; en série « i = i1 = i2 ».
- **Loi d'Ohm** u_R = R·i et sa forme inverse i = u_R/R, en tête des « Formules ».
- **Loi d'additivité des tensions** nommée en toutes lettres avant l'équation (« la loi d'add. des tensions : u_C + u_R = 0 »).
- **Convention récepteur** : jamais nommée par écrit, mais appliquée dans les dessins : flèche de u_R opposée au sens de i dans R, flèche de u_C vers l'armature A qui reçoit le courant.
- **i = dq/dt** écrit puis enchaîné avec q = C·u_C pour donner i = C·du_C/dt (deux lignes dans un même encadré).

## Définitions telles qu'écrites
Très peu de définitions écrites (format résumé) :
- « Intérêt : c'est pour augmenter la capacité » (association en parallèle).
- « G. idéal de tension : délivre une tension = cte » ; « G. idéale de courant : délivre une I = cte ».
- E_e : « c'est une énergie électrique ».
- « u_C est une fonction continue » (justifie la condition initiale).
- Rien d'écrit sur : condensateur/armatures (seulement A : +q, B : −q sur le schéma), capacité, échelon de tension, régimes transitoire/permanent, constante de temps (τ = RC est posée sans définition ni analyse dimensionnelle).

## Formules telles qu'écrites
- Association : **Ceq = C₁ + C₂** ; **1/Ceq = 1/C₁ + 1/C₂** (Ceq avec « eq » en indice, encadrées) ; q_eq = q₁ + q₂ (parallèle) ; q_eq = q₁ = q₂ (série).
- Formules : **u_R = R.i** (point de multiplication), **u_C = q/C**, **q = C.u_C**, **i = dq/dt**, **i = C du_C/dt**, **E_e = ½ C u_C²**, **E_e = q²/(2C)** ; unités notées en petit au-dessus des symboles (V, Ω, A ; C, F ; J).
- Générateur de courant : **I₀ = q/t → q = I₀.t**, puis **u_C = (I₀/C).t** (encadré, « Mq » = montrer que) ; « la courbe est une fct linéaire : u_C = a.t » ; à côté « y = a.x », « a = Δ/Δ ».
- Calcul de C, ordre des lignes : I₀/C = a → C = I₀/a = 10⁻⁶ / ((5 − 0)/(10 − 0)) = 10⁻⁶/0,5 → **C = 2.10⁻⁶ F** (encadré).
- Décharge : u_C + u_R = 0 → u_C + Ri = 0 → **u_C + RC du_C/dt = 0** (encadré). Ordre : u_C d'abord, puis RC·du_C/dt.
- Solution « s'écrit sous la forme » **u_C = A.e^(−αt) + B** avec des « ? » sous A, α, B (inconnues à trouver). Puis du_C/dt = A(−α)e^(−αt) = −αA e^(−αt) ; « Je remplace dans l'éq. diff » : A e^(−αt) + B − RCαA e^(−αt) = 0 → A e^(−αt)(1 − RCα) + B = 0 avec accolades « = 0 » sous chaque terme ; « pour que cette éq. soit vérifiée il faut que » {1 − RCα = 0 ; B = 0} ⇒ α = 1/RC = 1/τ ; τ = RC ; u_C(t) = A.e^(−t/RC).
- Conditions initiales : « À t = 0 : u_C(t=0) = A.e⁰ » et « u_C(t=0) = U₀ = 5 V » ⇒ **A = U₀** → **u_C(t) = U₀.e^(−t/RC)** (encadré).
- Droite ln : u_C = U₀.e^(−t/RC) → ln u_C = ln U₀ + ln e^(−t/RC) → **ln u_C = −(1/RC).t + ln U₀** (encadré) ; « par analogie » avec ln u_C = a t + b : −1/RC = a → **R = −1/(C × a)**, en Ω.
- Énergie : E_e = 70 % E_e0 → ½ C u_C² = 0,7·½ C U₀² → ½ C U₀² e^(−2t/RC) = 0,7·½ C U₀² (barres pour simplifier) → e^(−2t/RC) = 0,7 → −2t/RC = ln(0,7) → **t = −(RC/2)·ln(0,7)**.
- Absents : charge sous tension E (u_R + u_C = E, E(1 − e^(−t/τ))), i(t), u_R(t), q(t), analyse dimensionnelle de τ.

## Méthodes graphiques
- **Courbe u_C(t) droite** (générateur de courant) : pente lue avec deux points ((5 − 0)/(10 − 0)) puis identification avec la formule → C.
- **Graphe composé** charge (rampe linéaire) puis décharge (exponentielle) : deux axes u_C, le deuxième placé au point de bascule (t₀ = 10 s), accolades « charge » / « décharge ». Message : la décharge a sa **propre origine des temps**, et U₀ = 5 V est la valeur atteinte à la fin de la charge.
- **Droite ln u_C = f(t)** : points (0 ; 0,2) et (5 s ; 0,1) lus, pente a, R = −1/(C·a). (Valeurs effacées ensuite, pas de résultat final lisible.)
- Pas de tangente à l'origine, pas de 0,63·E / 0,37·U₀, pas de 5τ, pas de courbe du/dt = f(u).

## Montages
- **Générateur de courant traité en priorité** : symbole (cercle traversé d'un trait, flèche I₀ vers le haut), I₀ = 1 µA, charge linéaire u_C = (I₀/C)·t. Il annonce « 95 % » des sujets avec un générateur de tension et « 5 % » avec un générateur de courant.
- Générateur de tension : seulement le symbole, la flèche E et i = dq/dt = C du_C/dt à côté — **jamais utilisé dans l'exercice**.
- Interrupteur K à deux positions (1) charge / (2) décharge, dessiné comme une lame entre deux plots en haut du circuit.
- Masse dessinée sous l'armature B ; pas d'oscilloscope, pas d'ExAO, pas de « −u_R ».

## Exemples chiffrés et analogies
- I₀ = 1 µA ; u_C passe de 0 à 5 V en 10 s ; C = 2·10⁻⁶ F ; U₀ = 5 V ; droite ln u_C de 0,2 à 0,1 sur 5 s ; énergie qui baisse de 30 % (reste 70 %).
- Aucune analogie concrète (réservoir, seau…) visible au tableau. Il utilise l'« analogie » au sens mathématique : identifier la formule à y = a·x ou à a·t + b — mot écrit deux fois (« par analogie »).

## Ce sur quoi il insiste
- La méthode « **Mq / On sait que / puisque… / encadré** » : partir d'une formule connue, injecter la propriété du générateur, encadrer.
- La méthode de résolution de l'équation différentielle en 4 temps (forme de la solution avec « ? », dériver, remplacer, identifier « pour que cette éq. soit vérifiée il faut que »), puis les conditions initiales. C'est le passage le plus long (≈ 9 min).
- **Continuité de u_C** pour trouver A, et la nouvelle origine des temps au moment de la bascule.
- Le linéaire (droite par l'origine, u_C = a·t) contre l'affine (ln u_C = a t + b) — il écrit les deux mots.
- Pourcentages : « 95 % / 5 % » des sujets (tension / courant).
- Énergie : traduire « diminue de 30 % » en « E_e = 70 % E_e0 » (piège classique, il l'écrit en premier).
- Aucun national cité par écrit (pas de transcription pour vérifier l'oral).

## Faux, approximatif ou hors programme
- **Erreur au tableau à ≈ 14:29** : dans l'encadré « Formules », il écrit **I₀ = q/C** au lieu de **I₀ = q/t** (signalé par un commentaire épinglé de 52 likes et un autre de 184 likes qui donne la bonne formule). Dans l'exercice il écrit correctement I₀ = q/t.
- Unité de la courbe u_C d'abord notée « (µV) » puis corrigée en « (V) ».
- « 95 % / 5 % » est une estimation orale, à ne pas répéter comme une statistique.
- ln u_C avec u_C en volts : usage toléré au bac mais à présenter comme « ln de la valeur numérique ».
- Rien de hors programme (pas de Laplace, pas de séparation des variables : il utilise bien la méthode « forme donnée + identification »).

## Commentaires d'élèves (150 lus)
- **Remerciements / « meilleur prof »** : ≈ 45 (beaucoup en darija, plusieurs étrangers : Sénégal, Tunisie).
- **« Bac 2024/2025/2026 bano hna », prières, « chhal jbti »** : ≈ 60 — pas de contenu pédagogique.
- **Correction de formule** : 2 commentaires très likés (184 et 52) : **I = q/t et non q/C**, horodatage 14:29. → réponse correcte : pour un générateur de courant, I₀ = q/t, donc q = I₀·t et u_C = I₀·t/C.
- **Demandes de suite** : RLC forcé (SM), RL, RLC (≈ 6) ; demandes d'exercices (≈ 2).
- **Horodatage pointé** : 23:55 (« merci pour les explications ») — moment de la décharge / équation différentielle.
- Un élève dit qu'il a mieux compris ici qu'en classe ; un autre se plaint de ne pas savoir quelle vidéo de la playlist contient quoi.
- Aucune question de fond ouverte (format résumé, public de révision).

## Ce que notre cours doit lui prendre
1. **Le dessin « charge-puis-décharge » sur un même graphe avec une deuxième origine des temps au point de bascule**, et la phrase « u_C est une fonction continue → la valeur de fin de charge est la condition initiale de la décharge ». À montrer en simulation (le zéro du chronomètre qui se déplace).
2. **La résolution de l'équation différentielle en 4 lignes fixes**, avec des « ? » sous A, α, B qui disparaissent un à un ; l'accolade « = 0 » sous (1 − RCα) et sous B. Excellent pour une animation pas à pas.
3. **Le cas du générateur de courant** : I₀ = q/t → q = I₀·t → u_C = (I₀/C)·t → droite → C = I₀/pente. Court, chiffré (1 µA, 5 V, 10 s → 2 µF). Notre cours doit le traiter et **mettre en garde contre I = q/C** (l'erreur même du prof, très commentée).
4. **La droite ln u_C = f(t)** : passage u_C = U₀e^(−t/RC) → ln u_C = −t/RC + ln U₀ → identification « par analogie » avec a t + b.
5. **Énergie « diminue de 30 % » → reste 70 %**, et la simplification ½ C U₀² des deux côtés jusqu'à t = −(RC/2)·ln 0,7.
6. Les associations série/parallèle par la loi des nœuds (même i en série, i = i1 + i2 en parallèle) avec « intérêt : augmenter la capacité ».
Ce qu'il **ne** donne pas et que nos autres sources doivent couvrir : charge sous échelon E, définitions, τ et son unité, tangente / 63 %, i(t), u_R(t), oscilloscope.
