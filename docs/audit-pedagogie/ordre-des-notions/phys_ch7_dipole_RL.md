# phys_ch7_dipole_RL

## Ordre proposé des premières notions
1. Rappel : courant, tension, ampèremètre/voltmètre, en série / en dérivation (absent ; à ajouter avant la diapo 3, en reprenant les diapos 3-4 du RC)
2. La loi d'Ohm, convention récepteur (diapo 3)
3. La bobine : fil enroulé, spires, résistance r du fil (diapo 6, sans parler encore de L)
4. L'additivité des tensions avec R et une bobine (diapo 4, à placer après la diapo 6)
5. La dérivée comme une pente, di/dt (diapo 5)
6. L'expérience des deux lampes : retard à l'allumage, puis même éclat (diapos 7-9)
7. Le retard à l'ouverture (diapo 10), puis l'auto-induction (diapo 11)
8. La continuité de i, sur une diapo à part (aujourd'hui dans la diapo 11)

## Défauts
| # | Diapo | Type | Ce qui est dit (citation courte) | Pourquoi ça perturbe | Correction proposée | Gravité |
|---|---|---|---|---|---|---|
| 1 | 4 | 1 notion avant | « une résistance R, et une bobine … la tension de la bobine, u b » + QUESTION sur u_b | La bobine n'est présentée qu'à la diapo 6. L'élève calcule la tension d'un objet qu'il ne connaît pas. | Placer la diapo 4 après la diapo 6. | moyenne |
| 2 | 6 | 1 notion avant | « on enfonce un noyau de fer : l'inductance L augmente » ; « l'inductance L, en henry » | L est nommée sans aucun sens. Ce qu'elle mesure (u_b = L·di/dt) n'apparaît qu'à la diapo 13. | Dire « L, un nombre qui dit combien la bobine freine les variations de i ; on le mesure à la diapo 13 », et déplacer le noyau de fer après la diapo 13. | moyenne |
| 3 | 7-8 | 1 notion avant | « la lampe L un … la lampe L deux » | Juste après « L = inductance », les lampes s'appellent L₁ et L₂ : l'élève faible confond les deux. | Nommer les lampes « lampe 1 » et « lampe 2 », ou « A » et « B ». | moyenne |
| 4 | 9 | 2 trop vite | « on parle du régime permanent … la bobine se comporte comme une résistance r. Donc u b égale r fois I zéro … I p » + QUESTION | Quatre notions dans une seule diapo (régime permanent, bobine = résistance, I₀/I_p, u_b = r·I₀), puis un calcul, alors que l'élève vient de voir la bobine. | Garder ici seulement « même éclat → même courant final ». Déplacer u_b = r·I₀ et la question après la diapo 14 (ou la diapo 21). | moyenne |
| 5 | 11 | 2 trop vite | « l'auto-induction … Et un résultat important : l'intensité dans une bobine est continue » | Deux notions nouvelles dans la même diapo. La continuité de i est la clé des diapos 32, 45, 59 et 64. | Faire une diapo à part pour la continuité de i, avec les lampes à la fermeture et à l'ouverture. | moyenne |
| 6 | 12-13 | 1 notion avant | « un GBF » ; écran « voie Y₁ … voie Y₂ … masse au point commun » ; « u_Y2 = −u_R » | L'oscilloscope, ses voies, la masse et l'inversion d'une voie ne sont jamais expliqués dans ce cours. La diapo 13 lit i à partir de −u_Y2/R. | Ajouter avant la diapo 12 un rappel sur l'oscilloscope (deux voies, masse commune, une voie inversée), ou ôter des écrans la ligne u_Y2. | moyenne |
| 7 | 16-17 | 1 notion avant | 2025 R : « une diode supposée idéale de tension seuil », « E m l'énergie qui y est emmagasinée », « modulation d'amplitude » | Diode, énergie magnétique et modulation sont lues à la diapo 17. La diode est expliquée à la diapo 60 et l'énergie à la diapo 65. La diapo 18 ne répond pas à la partie énergie. | Lire l'énoncé 2025 R seulement avant la diapo 64. Pour la diapo 18, ne lire que la question 1.4 « u_b ». | moyenne |
| 8 | 30 | 1 notion avant | « L sur R plus r, c'est tau, la constante de temps. Et E sur R plus r, c'est I zéro » | La constante de temps n'est ni rappelée (RC) ni définie dans ce cours avant les diapos 42 et 47-48. L'élève reçoit un nom sans sens. | Ajouter une phrase-rappel du RC (« τ dit combien de temps dure la montée ; au RC τ = RC »), ou dire « on montrera à la diapo 42 que c'est τ ». | moyenne |
| 9 | bloc après 27 | 4 question tôt | « Calcule le coefficient (R + r)/L de l'équation di/dt + ((R + r)/L)·i = E/L » | Cette forme rangée et divisée par L n'est enseignée qu'aux diapos 29-30. | Déplacer la question après la diapo 30. | moyenne |
| 10 | 38 | 4 question tôt | « Avant de calculer, réfléchis : si U R égale huit volts, combien vaut r ? » ; écran « r = R·(E/U_R − 1) » | On demande r avant toute méthode. La formule r = R·(E/U_R − 1) tombe d'un coup sans être tirée de I₀ = E/(R + r). | Commencer par la question « quelle courbe est u_R ? », puis calculer I₀ = U_R/R, puis R + r = E/I₀ (méthode de la diapo 52, à placer avant). | moyenne |
| 11 | bloc après 49 | 4 question tôt | « On prend L₁ = 2L₀ = 1 H. Quelle courbe obtient-on ? » | L'effet de L sur τ et sur le palier n'est enseigné qu'à la diapo 50. | Déplacer l'exercice après la diapo 50. | moyenne |
| 12 | bloc après 54 | 4 question tôt | RETROUVER « quelle valeur prend i à t = τ, à l'établissement puis à la rupture ? » | La rupture n'est enseignée qu'aux diapos 57-59. | Ne garder que l'établissement, et poser la rupture après la diapo 59. | forte |
| 13 | bloc après 56 | 4 question tôt | RETROUVER « écris l'expression de l'énergie magnétique » + EXERCICE « 2016 R … Calcule l'énergie » | L'énergie de la bobine n'est enseignée qu'à la diapo 65. | Déplacer ce bloc après la diapo 66 (l'exercice y est déjà en double). | forte |
| 14 | 60 | 1 notion avant | « on ajoute une diode avec une résistance R un » ; écran « la diode est bloquée » | On ne dit jamais ce qu'est une diode (sens passant, sens bloqué, symbole). Toute la question 2025 R (diapo 64) repose dessus. | Ajouter avant la diapo 60 une diapo-rappel sur la diode : symbole, le courant passe dans un seul sens, diode idéale. | forte |
| 15 | 60 | 2 trop vite | « une surtension apparaît et une étincelle jaillit » ; « lampe au néon » | Surtension, étincelle et usages arrivent ensemble, sans chiffre, avant le calcul de la diapo 64. | Donner le chiffre de la diapo 64 (u_b = −100 V = 10·E) dès cette diapo, et garder les usages pour après. | moyenne |
| 16 | 65 | 1 notion avant | « la résistance chauffe. C'est l'effet Joule » | L'effet Joule est nommé sans explication. | Ajouter : « l'énergie électrique devient de la chaleur dans la résistance : c'est l'effet Joule ». | moyenne |

## Notions importantes dites une seule fois
- Mesure de L avec un courant en triangle (palier ÷ pente) — diapos 12-13
- Schéma équivalent de la bobine réelle (L idéale + r en série) — diapo 14
- Continuité de i, énoncée comme règle — diapo 11 (ensuite seulement appliquée)
- Dimension de τ = L/(R + r) — diapo 46
- Influence de R : I₀ et τ baissent ensemble (le contraire du RC) — diapo 51 (seulement observée à la diapo 23)
- Tangente à l'origine d'une courbe qui descend (rupture) — diapo 59
- Diode en parallèle, surtension u_b = −R₁·I₀ — diapos 60 et 64 (un seul exemple)
- Effet Joule à la rupture — diapo 65
