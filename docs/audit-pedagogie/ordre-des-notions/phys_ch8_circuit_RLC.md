# phys_ch8_circuit_RLC

## Ordre proposé des premières notions
1. Rappel : q = C·u_C et i = dq/dt (diapo 3)
2. Rappel : u_b = L·di/dt + r·i, continuité de i dans la bobine (diapo 4 ; la continuité n'est rappelée qu'à la diapo 11, à mettre ici)
3. Rappel : la décharge dans une résistance seule (diapo 5)
4. Rappel : sinusoïde, amplitude, période (diapo 26, à placer avant la diapo 6)
5. La décharge dans une bobine : u_C change de signe (diapo 6)
6. Condensateur vide, courant maximal (diapo 7)
7. Les oscillations libres, la pseudo-période (diapos 8 et 12)
8. Les trois régimes et le rôle de R + r (diapos 13-14)

## Défauts
| # | Diapo | Type | Ce qui est dit (citation courte) | Pourquoi ça perturbe | Correction proposée | Gravité |
|---|---|---|---|---|---|---|
| 1 | 8, 12, 14 | 1 notion avant | 8 : « entre eux, environ quatre millisecondes » (T) ; 12 : « T, la pseudo-période » ; 14 : « régime périodique » | Période, amplitude et « périodique » sont employées dès la diapo 8. Le rappel sur la sinusoïde, l'amplitude et la période n'arrive qu'à la diapo 26. | Placer le rappel de la diapo 26 (sans la formule en cos) avant la diapo 6, puis dire « pseudo-période » en s'y appuyant. | moyenne |
| 2 | 8 | 2 trop vite | écran « oscillations amorties … oscillateur électrique libre et amorti … le condensateur et la bobine se l'échangent » | Libres, amorties, oscillateur et échange d'énergie arrivent dans la même diapo. L'énergie de la bobine n'est rappelée qu'à la diapo 51. | Garder « oscillations libres » à la diapo 8. Dire « amorties » à la diapo 12 (sommets qui baissent) et « échange d'énergie » à la diapo 51. | moyenne |
| 3 | 12 | 1 notion avant | « l'écran de l'oscilloscope, avec ses sensibilités : deux volts par division, et deux millisecondes par division » | La sensibilité (balayage, V/div) n'est jamais expliquée. On s'en sert pour lire T aux diapos 44, 50 et 90. | Ajouter une phrase-rappel avec exemple : « 1 carreau = 2 ms ; 3 carreaux = 6 ms ». | moyenne |
| 4 | 17 | 4 question tôt | QUESTION « On divise C par 4 … plus rapides : T ≈ 2 ms » | La relation T₀ ∝ √C (×4 donne ×2) n'est enseignée qu'à la diapo 33. Ici l'élève n'a vu qu'un seul cas (×4 → 8 ms). | Demander seulement « plus lentes ou plus rapides ? », sans valeur de T, ou déplacer la question après la diapo 33. | moyenne |
| 5 | bloc après 19 | 4 question tôt | RETROUVER « écris l'équation différentielle vérifiée par la charge q » + EXERCICE « coefficient 1/(LC) de d²u_C/dt² + … » | Les équations en q et en u_C ne sont établies qu'aux diapos 23 et 24. Après la diapo 19, l'élève n'a que l'additivité. | Déplacer ce bloc après la diapo 24. | forte |
| 6 | 22 | 1 notion avant | « dé i sur dé t est la dérivée seconde de q. Écris l'équation … d'abord la dérivée seconde » | La dérivée seconde est nommée pour la première fois dans une question « à toi ». On ne l'explique qu'à la diapo suivante. | Ajouter avant la diapo 22 un rappel de maths : dériver deux fois, exemple avec la position, la vitesse et l'accélération. Ou placer la diapo 23 avant la diapo 22. | forte |
| 7 | bloc après 25 | 4 question tôt | RETROUVER « dans u = U_m·cos(2πt/T), que représentent U_m et T ? » | Le cosinus, U_m et T ne sont enseignés qu'à la diapo 26. On demande de « retrouver » ce qui n'a pas été dit. | Déplacer ce bloc après la diapo 27 (ou placer la diapo 26 plus tôt, voir défaut 1). | forte |
| 8 | 27 | 1 notion avant | « Et phi, c'est la phase à l'origine » ; écran « φ … en rad » | φ et le radian sont nommés sans explication. Leur sens n'arrive qu'aux diapos 37-41, et le radian n'est jamais rappelé. | Ajouter au rappel de la diapo 26 : « un tour = 2π radians ; φ dit où en est la courbe à t = 0 ». | moyenne |
| 9 | 29 | 1 notion avant | « La dérivée de sinus, c'est cosinus » | Le rappel de la diapo 28 ne traite que la dérivée du cosinus. Celle du sinus arrive sans rappel, au milieu d'un calcul double. | Ajouter cette règle, avec une courbe, à la diapo 28. | moyenne |
| 10 | bloc après 32 | 4 question tôt | « à partir de T₀ = 2π√(LC), écris L en fonction de T₀ et de C » + EXERCICE 2022 N L | La méthode « élever au carré, puis isoler » n'est enseignée qu'à la diapo 48. | Déplacer le bloc après la diapo 48, ou placer la diapo 48 juste après la diapo 30. | moyenne |
| 11 | 36 | 2 trop vite | « L égale T zéro au carré sur quatre pi carré C » | L est isolée d'un coup, douze diapos avant la diapo 48 qui enseigne comment le faire. | Placer la diapo 48 avant la diapo 36. | moyenne |
| 12 | 37, 39 | 1 notion avant | « sinus phi égale zéro : phi égale zéro, ou phi égale pi » ; « cosinus de zéro virgule cinq … plus pi sur trois, et moins pi sur trois » | Les angles qui ont un sinus nul ou un cosinus de 0,5 supposent le cercle trigonométrique, jamais rappelé. | Ajouter un rappel du cercle trigonométrique (valeurs 0, π/3, π/2, π et signe de sin et cos) avant la diapo 37. | moyenne |
| 13 | bloc après 39 | 4 question tôt | EXERCICE « La courbe i(t) part de 0 en descendant. Détermine φ » | La règle « le sens de départ donne le signe de sin φ » n'est enseignée qu'à la diapo 41. | Déplacer l'exercice après la diapo 41. | forte |
| 14 | 40 | 1 notion avant | énoncé 2020 N « un générateur G délivrant une tension proportionnelle à l'intensité … u G égale k fois i » | L'entretien n'est enseigné qu'à la diapo 62. L'élève lit un montage inconnu pour une question sur I_m et φ. | Ne lire que la phrase « i(t) = I_m·cos(…) ; déterminer I_m, T₀ et φ », ou dire « le générateur G sera vu à la diapo 62 ». | moyenne |
| 15 | 42 | 1 notion avant | « on utilise une relation de mathématiques : moins sinus alpha égale cosinus de alpha plus pi sur deux » | Cette identité n'a jamais été vue. Elle sert à trouver φ = +π/2, une question du bac. | Montrer cette relation sur le graphe (la courbe −sin est la courbe cos décalée d'un quart de période), comme à la diapo 28. | moyenne |
| 16 | 9, 15, 34-35, 43, 45, 47, 57, 60, 82-86, 88-89 | 2 trop vite | énoncés lus par morceaux : 2025 N 2.2.2 (diapo 9) avant 2.2.1 (diapo 43) et 2.1 (diapo 88) ; 2020 N III.2 (diapo 40) avant II.1 (diapo 82) | Les questions d'un même sujet sont lues dans le désordre, parfois 40 à 80 diapos avant leur correction. La diapo 9 cite aussi diodes et démodulation AM. | Lire chaque partie juste avant sa démonstration, dans l'ordre du sujet. Dire en une phrase que diode et AM viennent plus tard. | moyenne |

## Notions importantes dites une seule fois
- Équation en u_C forme LC·d²u_C/dt² + (R + r)·C·du_C/dt + u_C = 0 — diapo 24 (reprise seulement dans les sujets complets, diapos 87 et 90)
- Dimension : √(LC) est un temps — diapo 31
- T₀ ne dépend pas de la charge de départ (E change U_m, pas T₀) — diapo 32
- q(t), i(t) = I_m·cos(2πt/T₀ + π/2) et I_m = E·√(C/L) — diapo 42
- L'énergie s'échange avec la période T₀/2 — diapo 53
- Preuve de la conservation (cos² + sin² = 1) et usage E_m = E − ½·C·u_C² — diapo 54 (une seule application, diapo 87)
- Dérivée d'un carré d(x²)/dt = 2x·dx/dt — diapo 56
- Reconnaître E_e et E_m sur un graphe d'énergie — diapo 61
- Mesurer T sur plusieurs périodes (compter les intervalles) — diapo 44
