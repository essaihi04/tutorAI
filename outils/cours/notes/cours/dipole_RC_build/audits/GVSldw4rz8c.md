# Audit — GVSldw4rz8c — Prof Ridouan, « Dipôle RC cours 1 électricité semestre 1 partie 1 »

## Fiche
- id : GVSldw4rz8c — Prof Ridouan (chaîne « Prof Ridouan physique-chimie »), publiée le 26/12/2023.
- Durée : 2280 s (38 min) — ≈ 85 000 vues — 62 commentaires récupérés.
- Support : **diaporama PowerPoint animé** (fond blanc, titres rouges, lignes qui apparaissent une à une, pointeur rouge), voix off en darija + termes français. Pas de tableau, pas de classe, pas de manip.
- Pourquoi elle compte : très vue ; c'est la version « équations » du chapitre, avec la **méthode A·e^(−αt) + B pas à pas** (la plus détaillée vue jusqu'ici), puis les 4 équations différentielles de la charge (u_C, q, u_R, i) avec leur courbe. **Partie 1 seulement : ni décharge, ni énergie** (renvoyées à la partie 2).
- Transcription : 493 lignes, mais très trouée (nombreuses lignes d'un mot) ; les images ont porté l'essentiel.

## Plan horodaté
| Temps | Notion | Durée |
|---|---|---|
| 0:00–1:00 | Titre « dipôle » ; R déjà connu, C nouveau ; la capacité = aptitude à stocker l'énergie électrique | 1 min |
| 1:00–1:35 | Rappel « Intensité du courant » (courant qui varie avec le temps) | 0,5 min |
| 1:35–2:35 | Générateurs idéaux : de courant (symbole cercle traversé, I = I₀ = cte) et de tension | 1 min |
| 2:35–3:28 | Conducteur ohmique (Récepteur), convention récepteur | 1 min |
| 3:28–4:25 | Association des conducteurs ohmiques (dérivation, série) | 1 min |
| 4:25–6:50 | Condensateur (Récepteur) : symbole, armatures, signe des armatures, C, Farad, sous-multiples | 2,5 min |
| 6:50–9:00 | « Préciser la charge de chaque armature » (sens des électrons) | 2 min |
| 9:00–10:00 | q = C·u_C, unités, u_C = q/C | 1 min |
| 10:00–10:30 | Association des condensateurs (dessinée, formules dites seulement) | 0,5 min |
| 10:30–11:50 | Loi d'additivité des tensions sur le circuit RC | 1,3 min |
| 11:50–12:55 | Relation intensité–charge → i = C·du_C/dt (relation ③) | 1 min |
| 13:00–14:30 | Rappel mathématique : forme d'une équation différentielle, dérivée de l'exponentielle | 1,5 min |
| 14:30–17:00 | Charge : établir l'ED en u_C | 2,5 min |
| 17:00–24:00 | **Résolution u_C = A·e^(−αt) + B : dérivée, remplacement, factorisation, B, α, A** | **7 min (le plus long)** |
| 24:00–24:20 | τ = R×C, constante de temps, unité seconde | 0,3 min |
| 24:20–27:35 | Courbe u_C(t), oscilloscope, limites, régime transitoire/permanent, 5τ | 3 min |
| 27:35–29:55 | Exemple : lire E et τ « par 2 méthodes » (tangente, 0,63E) | 2,5 min |
| 30:00–32:50 | ED de q, solution q = CE(1−e^(−t/τ)), q_m = CE | 3 min |
| 33:00–35:10 | ED de u_R, solution, courbe | 2 min |
| 35:10–37:57 | ED de i, solution, courbe, 0,37·E/R | 2,5 min |

Séjour long = la résolution de l'ED (7 min) et les courbes/lectures de τ.

## Rappels du tronc commun / 1re
- **Générateur de courant idéal** dessiné (cercle avec trait horizontal, I = I₀ = cte) en plus du générateur de tension — mais il ne s'en sert pas ensuite (pas de charge à courant constant).
- **Convention récepteur** : conducteur ohmique avec flèche i rose vers la droite et flèche u_R en sens opposé, titre « Conducteur ohmique (Récepteur) » ; même titre « condensateur (Récepteur) ».
- **Association des résistances** : dérivation R_éq = R₁×R₂/(R₁+R₂) (« produit sur somme », « si elles ne sont que deux »), série = somme.
- **Loi d'additivité** : circuit E, R, C avec i qui monte dans le générateur, i qui descend vers le condensateur, u_R flèche vers la gauche au-dessus de R, u_C flèche vers le haut à droite.
- **Loi d'Ohm** u_R = R × i écrite à chaque ED. **i = dq/dt** introduite comme « relation intensité–charge » ; plus « si le courant est continu : I = q/t ».

## Définitions telles qu'écrites
- Symbole du condensateur : deux traits parallèles ; les deux traits annotés « armature » (flèches courbes vertes/roses), lettre C au-dessus.
- « C : capacité du condensateur » ; « Son unité est le Farad (F) » ; « Elle emmagasine (petit chwia) d'énergie » [sic]. Sous-multiples : 1 nF = 10⁻⁹ F, 1 µF = 10⁻⁶ F, 1 pF = 10⁻¹² F, 1 mF = 10⁻³ F.
- Charge : « La charge d'un condensateur noté q », « S'exprime en coulomb C » ; q_A = +q, q_B = −q.
- « τ = R × C : Appelé la constante de temps du dipôle RC ». Unité : la seconde (dit, « c'est une durée ») ; **pas d'analyse dimensionnelle**.
- Régime transitoire (u_C augmente) / régime permanent (u_C constante, après ≈ 5τ) : dits sur la courbe, pas écrits.
- Échelon de tension, énergie emmagasinée : **absents** de cette partie.

## Formules telles qu'écrites / dites
- q = C × u_C (« Avec q = C × u_C ») ; dit aussi u_C = q/C (unités C = F·V).
- i = dq/dt → i = d(C × u_C)/dt = C·du_C/dt, encadrée en vert avec un numéro ③ ; encadré vert-jaune réutilisé sur chaque diapo d'ED.
- **ED de u_C** (titre « Déterminer Équation différentielle vérifiée par u_C », encadré « À t=0 u_C =0 ») : E = u_R + u_C ; u_R = R × i ; **E = R × C·du_C/dt + u_C** (E à gauche).
- Rappel math : « a × d(grandeur)/dt + grandeur = constante » (écrit « garndeur » sur la diapo) ; d/dt(e^(ax)) = a·e^(ax).
- **Résolution** (ordre des lignes) : u_C = A·e^(−αt) + B → du_C/dt = A(−α·e^(−αt)) = −αA·e^(−αt) → E = R × C(−αA·e^(−αt)) + A·e^(−αt) + B → E = −αRCA·e^(−αt) + A·e^(−αt) + B → E = A·e^(−αt)(−αRC + 1) + B → A·e^(−αt)(−αRC + 1) + B − E = 0 → accolade { B − E = 0 ; −αRC + 1 = 0 } → **B = E**, **α = 1/RC** (encadrés). Puis « Pour trouver B: on travail par les conditions initial » [sic, c'est A qu'on cherche] : à t=0 u_C=0 → 0 = A·e^(−α×0) + B → 0 = A + B → A = −B = −E → u_C = −E·e^(−t/RC) + E → **u_C = E(1−e^(−t/RC))**, puis E(1−e^(−t/τ)).
- Justification dite : le facteur (−αRC+1) doit être nul car « A = 0 n'a pas de sens » (u_C serait constante = B, pas logique).
- Astuce dite : dans la dérivée, on « sort » −α devant et on laisse l'exponentielle telle quelle ; « la constante collée à l'exponentielle se trouve par les conditions initiales ».
- **ED de q** : u_R + u_C = E ; R × i + u_C = E ; « Or i = dq/dt Et u_C = q/C » → **E = R·dq/dt + q/C ou EC = RC·dq/dt + q**. Solution : q = CE(1−e^(−t/τ)) ; q_m = CE.
- **ED de u_R** : dérivation de l'additivité du_R/dt + du_C/dt = dE/dt = 0 ; du_C/dt = u_R/(R×C) → **du_R/dt + u_R/(R×C) = 0** ; solution u_R = E·e^(−t/τ).
- **ED de i** : même départ, u_R = R × i → **R·di/dt + i/C = 0** ; solution i(t) = (E/R)·e^(−t/τ) ; I₀ = E/R.
- Associations de condensateurs : schémas C₁//C₂ et C₁–C₂ en série ; formules **seulement dites** : « exactement l'inverse des résistances » (dérivation : somme ; série : produit sur somme) ; « pas très important ».

## Méthodes graphiques
- Courbe u_C(t) : quadrillage vide « u_C (V) / t(ms) » qui se remplit ; t = 0 ⇒ u_C = 0 ; « t => ∞ ⇒ u_C = E » ; pointillé horizontal en E (asymptote).
- Exemple (graphe type examen, courbe (C₁), tangente (T), 12 V, 50 ms) : E = 12 V lu sur l'asymptote (trait rouge, point vert sur l'axe).
  - Méthode 1 : tangente à l'origine ∩ asymptote horizontale → projection sur l'axe des temps → τ = 50 ms.
  - Méthode 2 (écrite) : u_C(τ) = E(1−e^(−τ/τ)) = E(1−e^(−1)) = E(1−0,37) = **0,63E** ; 12 × 0,63 = 7,56 V → projeter **sur la courbe** puis sur l'axe des temps → 50 ms.
- 5τ : avant 5τ u_C augmente (transitoire), après c'est constant (permanent).
- q(t), u_R(t), i(t) : graphes quadrillés bleus avec tangente rouge à l'origine qui coupe l'asymptote (q_m) ou l'axe des temps (u_R, i) à τ ; pour i : ordonnée 0,37·E/R pointillée → τ.
- Courbes non temporelles (ln, du/dt = f(u)) : **absentes**.

## Montages
- Circuit de charge : générateur de tension E (cercle, flèche E vers le haut), interrupteur K simple (deux points, ouvert puis fermé), R, C — **pas d'interrupteur à 2 positions** (la décharge est pour la partie 2).
- Oscilloscope : fils roses « Y » (voie) en haut du condensateur et symbole masse en bas → visualise u_C. Pas d'inversion ni de −u_R.
- Générateur de courant : symbole et I = I₀ = cte seulement ; pas de q = I·t ni u_C = I·t/C (seulement « I = q/t si courant continu »).

## Exemples chiffrés et analogies
- E = 12 V, τ = 50 ms, 0,37 / 0,63, 12 × 0,63 = 7,56 V.
- Analogie : le condensateur stocke de l'énergie « comme un petit réservoir », peut se comporter comme générateur et « allumer une lampe un moment ». « Petit chwia d'énergie » (formule devenue mème dans les commentaires).

## Ce sur quoi il insiste
- Savoir **pourquoi** l'armature où entre le courant est positive : les électrons vont en sens inverse du courant, quittent cette armature et s'accumulent sur l'autre — « je vous l'explique pour que vous ne l'appreniez pas par cœur ».
- « Prenez une feuille et un stylo et suivez avec moi » pendant la résolution.
- i = dq/dt et u_C = q/C (q = C·u_C) : « obligatoire de les mémoriser ».
- **ردو البال** : pour la méthode 0,63E, projeter sur la **courbe**, pas sur la tangente.
- Parfois l'énoncé inverse les lettres (B devant l'exponentielle, A seule) : peu importe, la constante collée à l'exponentielle se trouve par les conditions initiales, celle qui multiplie t dans l'exposant se trouve par l'ED.
- Questions d'examen citées : l'énoncé donne l'expression avec un nombre (ex. q_m chiffré, ou E/R chiffré) et demande d'en déduire C, E ou R. Aucun national cité précisément.

## Faux, imprécis ou à ne pas répéter
- « C : capacité … **Elle** emmagasine d'énergie » : c'est le condensateur qui emmagasine l'énergie, pas sa capacité ; et « la capacité est la capacité de stocker l'énergie » (0:46) — imprécis : C relie q et u_C.
- Diapo : « Pour trouver B » alors qu'on trouve A ; fautes « garndeur », « on travail par les conditions initial ».
- « Si le courant est continu : I = q/t » — à dire « courant constant : q = I·t ».
- « t => ∞ » écrit avec une flèche de type implication.
- Pas d'erreur hors programme (ni Laplace, ni séparation des variables, ni sinusoïdal). Formules d'association des condensateurs seulement dites (« pas très important ») : le cadre PC les demande, il faut les écrire.

## Commentaires d'élèves (62)
- Mème « petit chwiya » (6:32) : 3 commentaires, 26 + 5 likes — l'humour retient l'attention.
- Demandes de la **partie 2** (décharge) : ≈ 7 (« partie 2 imta ? », « Pt2 3afak »… réponse : dans la playlist).
- Questions :
  - « Si je remplace RC par τ, la relation reste juste ? » → oui, τ = RC, u_C = E(1−e^(−t/τ)) est la même expression.
  - « Peut-on nous demander l'ED en u_R ? » → oui (réponse d'élève) ; elle est traitée à 33:00.
  - « Quand faut-il faire la démonstration ? » → quand l'énoncé dit « établir / montrer » l'ED ; sinon on l'utilise.
  - Prérequis : « que faut-il savoir de la 1re en électricité / mécanique ? » (2 fois) ; « travail et énergie, on en a besoin ? ».
- Remerciements nombreux (≈ 25), « Hadchi bzaf » (1 : trop dense).
- Horodatage pointé : 6:32 (mème), 20:07 (blague « RCA »).

## Ce que notre cours doit lui prendre
1. **La résolution A·e^(−αt) + B ligne par ligne**, chaque ligne apparaissant à son tour, couleurs fixes (A rouge, α rouge, la partie A·e^(−αt)+B remplacée en bleu), la forme cible u_C = A·e^(−αt)+B gardée en bas à droite comme repère, l'accolade { B−E=0 ; −αRC+1=0 } avec résultats encadrés, puis t = 0 → A = −E. Ajouter la phrase « le facteur doit être nul parce que A ne peut pas être 0 ».
2. Le **rappel math** juste avant (forme a·dX/dt + X = constante, dérivée de e^(ax)) : petit prérequis à vérifier par une question.
3. L'explication du **signe des armatures par le trajet des électrons** (flèche e⁻ verte opposée à i, +++ puis −−−), à animer en simulation.
4. La **méthode 2 écrite** u_C(τ) = E(1−e⁻¹) = 0,63E avec l'avertissement « projeter sur la courbe, pas sur la tangente ».
5. La série des 4 ED (u_C, q, u_R, i) sur le même circuit fixe à droite avec l'encadré « À t=0 u_C=0 » et i = C·du_C/dt toujours visible ; les graphes q, u_R, i avec leur tangente rouge et τ.
6. À corriger chez nous : écrire les formules d'association des condensateurs, dire que c'est le condensateur (pas C) qui stocke l'énergie, q = I·t à courant constant.
