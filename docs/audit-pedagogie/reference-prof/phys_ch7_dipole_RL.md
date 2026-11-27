# phys_ch7_dipole_RL — comparaison avec le cours de référence d'un professeur

Source : cours polycopié d'un professeur marocain (2ᵉ Bac SP, 2022/2023), leçon 7 « Dipôle RL », pages 45 à 53. Résumé et comparaison avec nos mots ; le texte du professeur n'est pas reproduit.

## Plan du professeur (ordre des notions, en une liste courte)
1. Porte d'entrée : la bobine est partout (sonnette, transformateur, détecteur de métaux, antenne, allumage d'un moteur) ; trois questions (qu'est-ce, quel rôle, quel comportement).
2. La bobine : définition (fil enroulé), symbole, inductance L (henry) et résistance r.
3. Tension aux bornes : u_b = L·di/dt + r·i, **donnée d'emblée** ; cas r = 0 ; courant constant → la bobine se comporte comme une résistance r.
4. Remarque immédiate : variation très rapide de i (ouverture du circuit) → surtension ; usage : l'étincelle de la bougie.
5. Expérience des deux lampes : retard à l'allumage et à l'extinction ; conclusion « la bobine retarde l'établissement et l'annulation du courant ».
6. Dipôle RL, résistance totale R + r ; étude expérimentale de l'établissement puis de la rupture, avec **une diode qui évite l'étincelle**, expliquée dès le montage ; deux régimes ; 5τ.
7. Établissement : équation en i, puis en u_R ; solution, constantes par l'équation et par i(0) = 0 ; u_R(t), u_b(t) ; cas r négligeable.
8. Rupture (diode idéale) : même démarche, i(0) = I₀.
9. Constante de temps τ = L/(R + r) : dimension, deux méthodes de lecture pour chaque cas.
10. Énergie : mise en évidence par un petit moteur qui tourne à l'ouverture (la diode bloque le courant pendant l'établissement), puis démonstration par la puissance reçue, E_m = ½·L·i².

## Porte d'entrée et rappels : où le prof les place, et nous
- **Porte d'entrée.** Prof : une liste d'objets du quotidien. Nous : la carte du chapitre (diapo 2), puis l'expérience des deux lampes (diapos 7-11). Notre entrée par l'expérience est plus parlante ; aucun objet du quotidien n'est cité avant la diapo 60 (bougie, néon). Une phrase d'usages à la diapo 2 ou 6 suffirait.
- **Rappels.** Le prof n'en fait aucun dans cette leçon (il s'appuie sur ceux du RC). Nous rappelons Ohm, l'additivité et la dérivée (diapos 3-5). Notre audit demande d'ajouter le rappel courant/tension/appareils ; le prof ne le contredit pas.
- **Rappel de τ.** Le prof ne nomme τ qu'au moment de la solution (« on pose τ = L/(R + r) »), puis le définit et l'étudie. Nous le nommons à la diapo 30 sans rappel. **Le prof confirme le défaut 8 de l'audit** : à la diapo 30, soit rappeler τ du RC, soit dire « on montrera que c'est τ ».
- **La diode.** Le prof l'introduit dans le montage de l'étude expérimentale, avec son rôle (éviter l'étincelle de la surtension), bien avant la rupture. Nous ne disons jamais ce qu'est une diode (diapo 60). **Le prof confirme le défaut 14 de l'audit** (forte) et indique la place : au montage (diapo 19) ou juste avant la diapo 60.

## Différences d'ordre qui comptent
| Notion | Place chez le prof | Place chez nous (diapo) | Ce qu'il faut changer chez nous |
|---|---|---|---|
| u_b = L·di/dt + r·i | Donnée d'emblée, avant toute expérience | Découverte par le courant en triangle (diapos 12-13), puis bobine réelle (diapo 14) | Notre ordre est meilleur (on découvre L par la mesure). Garder. Mais l'audit (défaut 2) a raison : à la diapo 6, L doit recevoir un sens provisoire (« un nombre qui dit combien la bobine freine les variations de i »), puisque la mesure n'arrive qu'à la diapo 13. |
| Expérience des deux lampes | Après u_b (illustration) | Diapos 7-11, avant u_b (découverte) | Garder notre ordre. Le prof nomme aussi les lampes L₁ et L₂ : il ne règle pas la confusion avec l'inductance L ; la correction de l'audit (défaut 3 : « lampe 1, lampe 2 ») reste nécessaire. |
| Surtension à l'ouverture | Juste après u_b, comme conséquence de di/dt très grand | Diapo 60, à la fin de la rupture | Ajouter dès la diapo 13 ou 14 une phrase-cause : « si i tombe d'un coup, di/dt est énorme, donc u_b aussi » ; la diapo 60 redit ensuite le phénomène avec la diode. Cela répond aussi au défaut 15 de l'audit (surtension sans explication ni chiffre). |
| Diode | Dans le montage expérimental, avec son rôle | Diapo 60 sans définition | Ajouter la diapo-rappel sur la diode (symbole, un seul sens, diode idéale) avant la diapo 60, et la citer au montage (diapo 19). |
| Régime permanent : « la bobine se comporte comme une résistance r » | Dans la partie u_b, avant l'expérience | Diapo 9 (avec I₀, u_b = r·I₀ et une question), puis diapo 21 | L'audit (défaut 4) propose de ne garder à la diapo 9 que « même éclat → même courant final ». Le prof dit la phrase « résistance r » tôt, mais **après** la formule de u_b, ce qui la justifie. Chez nous, la formule n'arrive qu'à la diapo 14 : la correction de l'audit est la bonne. |
| Équation en u_R | Remarque juste après l'équation en i | Diapo 31, même place | Garder. |
| Énergie | Démontrée par p = u·i (bobine idéale) | Diapo 65, « expression admise » | Conforme au programme. Ajouter seulement l'effet Joule expliqué (audit défaut 16). |

## Ce que le prof explique et que nous n'expliquons pas (ou mal) — avec la diapo où l'ajouter
- **Pourquoi une diode est dans le montage** (éviter l'étincelle) : voir plus haut. Diapo 19 (une phrase) et diapo-rappel avant la diapo 60.
- **La surtension comme conséquence de u_b = L·di/dt** : voir plus haut. Diapo 13 ou 14.
- **Énergie : l'expérience du moteur** : le prof montre que, la diode bloquant le courant pendant l'établissement, le moteur ne tourne qu'à l'ouverture, avec l'énergie de la bobine. Notre diapo 65 cite le moteur à l'écran, mais la voix parle seulement de la barre d'énergie. Ajouter une phrase à la voix (« à l'ouverture, un petit moteur tourne : c'est l'énergie stockée dans la bobine »).
- **Usages de la bobine** (transformateur, détecteur de métaux, antenne, allumage) : une phrase à la diapo 2 ou 6.

## Définitions et méthodes : formulation du prof vs la nôtre (seulement quand la nôtre est moins exacte ou moins conforme au programme)
- **Influence de la bobine** : le prof dit qu'elle retarde l'établissement **et l'annulation** du courant. Nous disons la même chose en deux diapos (8 et 10), puis « s'oppose aux variations » (diapo 11). Conforme et plus complet chez nous.
- **Rupture** : le prof étudie la rupture avec la diode idéale (la diode conduit à l'ouverture) ; nous avec un interrupteur à deux positions (diapo 57), puis la diode à part (diapos 60, 64). Les deux sont au national ; garder les deux, en signalant à la diapo 57 que « K en position 2 » et « diode qui prend le relais » donnent la même équation.
- **Énergie magnétique** : « expression admise » chez nous, démontrée chez le prof. Les deux sont conformes.

## Ce que nous faisons mieux (court ; à garder)
- La découverte de u_b = L·di/dt par le courant en triangle (diapos 12-13) : le prof la donne sans preuve.
- La continuité de i, énoncée comme règle (diapo 11) puis appliquée (diapos 32, 45, 59, 64) ; le prof s'en sert sans la nommer.
- L'influence de R : I₀ et τ baissent ensemble, « le contraire du RC » (diapo 51).
- Les méthodes du national : trouver r, trouver L, la droite di/dt = f(i), la courbe u_b(t), le calcul de la surtension (diapo 64).

## Corrections recommandées pour notre cours (liste numérotée, concrète : diapo, quoi, pourquoi), sans raccourcir le cours
1. **Avant la diapo 60** : diapo-rappel sur la diode (symbole, passe dans un seul sens, diode idéale = tension nulle quand elle conduit) ; **diapo 19** : une phrase « parfois on ajoute une diode pour éviter une étincelle, on verra pourquoi ». (Prof : diode au montage ; audit défaut 14, confirmé.)
2. **Diapo 13 ou 14** : ajouter la conséquence de u_b = L·di/dt : « si i s'annule d'un coup, di/dt est énorme, la tension aussi : c'est une surtension » ; puis, diapo 60, donner le chiffre (−100 V = 10·E) qui sera calculé diapo 64. (Prof ; audit défaut 15.)
3. **Diapo 30** : rappeler τ du RC ou annoncer « on montrera diapo 42 que c'est la constante de temps ». (Audit défaut 8, confirmé par le prof qui ne nomme τ qu'à la solution.)
4. **Diapo 6** : donner à L un sens provisoire (« combien la bobine freine les variations de i ; on le mesure diapo 13 ») ; déplacer le noyau de fer après la diapo 13. (Audit défaut 2.)
5. **Diapos 7-10** : nommer les lampes « lampe 1 » et « lampe 2 ». (Audit défaut 3 ; le prof garde L₁, L₂, ce qui ne règle rien.)
6. **Diapo 9** : garder seulement « même éclat, même courant final » ; u_b = r·I₀ et la question passent après la diapo 14. (Audit défaut 4.)
7. **Diapo 4** : la placer après la diapo 6. (Audit défaut 1.)
8. **Diapo 65** : dans la voix, l'expérience du moteur et l'effet Joule expliqué en une phrase (« l'énergie électrique devient chaleur dans la résistance »). (Prof ; audit défaut 16.)
9. **Diapo 57** : une phrase reliant les deux montages de rupture (K en position 2, ou diode qui prend le relais) : même équation, second membre nul.
10. **Diapo 2 ou 6** : citer quelques usages de la bobine (allumage d'un moteur, transformateur, détecteur de métaux) comme porte d'entrée concrète.
11. **Garder** les autres corrections de l'audit (oscilloscope avant la diapo 12, défaut 6 ; énoncé 2025 R lu trop tôt, défaut 7 ; questions de bloc, défauts 9-13) : le prof ne les contredit pas.
