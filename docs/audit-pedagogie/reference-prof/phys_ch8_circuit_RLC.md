# phys_ch8_circuit_RLC — comparaison avec le cours de référence d'un professeur

Source : cours polycopié d'un professeur marocain (2ᵉ Bac SP, 2022/2023), leçon 8 « Oscillations libres dans un circuit RLC série », pages 54 à 61. Résumé et comparaison avec nos mots ; le texte du professeur n'est pas reproduit.

## Plan du professeur (ordre des notions, en une liste courte)
1. Porte d'entrée : les circuits RLC sont dans les récepteurs de radio et de télévision ; deux questions (quels phénomènes, quels paramètres).
2. Montage : rhéostat, condensateur, bobine ; résistance totale ; le condensateur chargé bascule dans la bobine, u_C à l'oscilloscope.
3. Observation et vocabulaire dans un même paragraphe : la charge oscille, les oscillations sont **amorties** (à cause de la résistance) et **libres** (pas de générateur) ; l'amortissement est expliqué aussitôt par l'effet Joule.
4. Trois régimes selon la résistance : pseudo-périodique (pseudo-période T), apériodique, **régime critique** en remarque, périodique (période propre T₀) ; lecture de T sur l'oscilloscope : nombre de divisions × sensibilité horizontale.
5. Équation différentielle du RLC en u_C, puis en q ; le terme en dérivée première est « responsable de l'amortissement ».
6. Circuit LC idéal : équation, solution en cosinus (amplitude, période propre, phase), T₀ = 2π√(LC) par identification, dimension de T₀ ; remarque T ≈ T₀ en pseudo-périodique.
7. Conditions initiales (u_C(0) = E, i(0) = 0) → U_m = E et φ = 0 ; q(t), i(t), I_m.
8. Énergie : dans le LC, énergie totale constante (démontrée en dérivant et en utilisant l'équation différentielle) et échange condensateur ↔ bobine ; dans le RLC, dE/dt = −R·i² < 0 (effet Joule).
9. Entretien : générateur u_G = k·i ; k = résistance totale annule le terme d'amortissement ; on retrouve l'équation du LC.

## Porte d'entrée et rappels : où le prof les place, et nous
- **Porte d'entrée.** Prof : la radio et la télévision (le RLC sert à choisir une station), puis l'expérience. Nous : la carte (diapo 2, qui annonce la modulation), puis le rappel de la décharge dans une résistance (diapo 5) et le remplacement par une bobine (diapo 6). Notre entrée par le contraste RC / RLC est meilleure pour comprendre ; la radio, qui donne le « pourquoi », n'est citée qu'au détour de la carte. Une phrase « c'est ce circuit qui choisit la station dans une radio » à la diapo 2 ou 8 relie le chapitre à la modulation.
- **Rappels.** Le prof n'en fait aucun : il s'appuie sur le RC et le RL. Nous rappelons q = C·u_C et i = dq/dt (diapo 3), u_b (diapo 4), la décharge RC (diapo 5), puis le cosinus (diapo 26) et sa dérivée (diapo 28). Notre audit veut avancer le rappel de la sinusoïde (défaut 1), ajouter la dérivée seconde (défaut 6), le radian et le cercle trigonométrique (défauts 8, 12). Le prof ne les fait pas, mais il n'emploie pas « période » avant d'avoir montré la courbe : il ne contredit pas l'audit.
- **Sensibilité de l'oscilloscope.** Le prof donne la règle de lecture T = (nombre de divisions) × (sensibilité horizontale) **au moment où il définit la période**. Nous parlons de « 2 ms par division » à la diapo 12 sans l'expliquer, et la règle n'est appliquée qu'à la diapo 44. **Le prof confirme le défaut 3 de l'audit** et donne la place : diapo 12, avec un exemple chiffré.

## Différences d'ordre qui comptent
| Notion | Place chez le prof | Place chez nous (diapo) | Ce qu'il faut changer chez nous |
|---|---|---|---|
| « Libres », « amorties », cause de l'amortissement | Ensemble, dès la première observation, avec l'effet Joule comme cause | Diapo 8 : libres, amorties, oscillateur, échange d'énergie ensemble, sans la cause | L'audit (défaut 2) propose d'étaler : « libres » diapo 8, « amorties » diapo 12, échange d'énergie diapo 51. **Le prof regroupe « libres » et « amorties », mais il donne la cause tout de suite.** Ce qui gêne chez nous n'est pas le nombre de mots, c'est « amorties » sans cause et « échange d'énergie » sans énergie de la bobine. Correction : garder « libres » diapo 8 ; à la diapo 12, « amorties » avec la cause en une phrase (« l'énergie part en chaleur dans les résistances : effet Joule ») ; l'échange d'énergie diapo 51 (audit). |
| Période / lecture à l'oscilloscope | Règle T = n × sensibilité donnée avec la pseudo-période | Diapo 12 (sensibilités nommées), règle diapo 44 | Mettre la règle et un exemple dans la diapo 12. |
| Régime critique | Remarque d'une ligne entre pseudo-périodique et apériodique | Absent | Voir « définitions » : **ne pas l'ajouter** comme notion ; notre cadre (audit-programme-officiel) l'a classé hors programme. |
| T ≈ T₀ en pseudo-périodique | Juste après le calcul de T₀ | Diapo 46 | Annoncer à la diapo 30 ou 33 « en pseudo-périodique faiblement amorti, T est très proche de T₀, on le vérifiera » ; garder la diapo 46. |
| Énergie : conservation dans le LC | Démontrée par dérivation et l'équation différentielle (même méthode que pour le RLC) | Diapo 54, par cos² + sin² = 1 | Les deux sont justes. La méthode du prof prépare directement dE/dt = −(R + r)·i² (diapo 58) : on peut l'ajouter en une ligne à la diapo 58 (« avec R + r = 0, dE/dt = 0 : on retrouve la conservation »). |
| Entretien | Dernière partie | Diapos 62-64 | Même place : garder. |

## Ce que le prof explique et que nous n'expliquons pas (ou mal) — avec la diapo où l'ajouter
- **La cause de l'amortissement dès qu'on le nomme** (effet Joule) : nous ne l'expliquons qu'à la diapo 55. Une phrase à la diapo 12.
- **« Le terme en dérivée première est responsable de l'amortissement »** : le prof le dit dès l'équation du RLC. Nous le disons à la diapo 25 (LC idéal), puis à la diapo 63 (entretien). Le redire à la diapo 23 ou 24, quand l'équation apparaît : cela prépare la diapo 25 et la diapo 63.
- **La lecture de T sur l'écran** : voir plus haut (diapo 12).
- **Le lien avec la radio** : voir porte d'entrée (diapo 2 ou 8), utile pour le futur cours de modulation (circuit d'accord).

## Définitions et méthodes : formulation du prof vs la nôtre (seulement quand la nôtre est moins exacte ou moins conforme au programme)
- **Régime critique** : le prof le cite en remarque. Notre cadre de référence (`docs/audit-programme-officiel/physique.md`, étape 1) l'a retiré du périmètre (« hors cadre »). Ne pas l'ajouter ; si un élève le lit dans un livre, une phrase en réponse suffit.
- **Pseudo-période** : le prof la définit comme la durée entre deux passages successifs par la valeur maximale. La nôtre (« durée entre deux sommets successifs », diapo 12) est équivalente et conforme.
- **Résistance totale** : le prof note R la résistance totale (rhéostat + bobine) ; nous écrivons R + r. La nôtre évite l'erreur fréquente (k = R au lieu de k = R + r) : garder.
- **Énergie du LC** : le prof conclut que l'énergie totale égale l'énergie initiale du condensateur ; nous aussi (diapo 52). Conforme.

## Ce que nous faisons mieux (court ; à garder)
- Le contraste décharge dans R / décharge dans une bobine (diapos 5-6), puis l'arrêt sur image « condensateur vide, courant maximal » (diapo 7) : on comprend pourquoi u_C devient négative ; le prof le constate seulement.
- Le choix de φ par le sens de départ de la courbe (diapos 39-41) et le passage de i en cosinus (diapo 42), demandés au national.
- La lecture de T sur plusieurs périodes, « compter les intervalles, pas les sommets » (diapo 44).
- L'énergie perdue entre deux sommets (diapo 59) et la reconnaissance des courbes E_e / E_m (diapo 61).
- T₀ indépendante de la charge de départ (diapo 32) et l'effet de la racine (diapo 33).

## Corrections recommandées pour notre cours (liste numérotée, concrète : diapo, quoi, pourquoi), sans raccourcir le cours
1. **Diapo 12** : expliquer la sensibilité horizontale avec la règle T = (nombre de divisions) × (ms par division) et un exemple chiffré ; dire « amorties » ici avec sa cause (effet Joule). (Prof ; audit défauts 2 et 3, confirmés.)
2. **Diapo 8** : garder seulement « oscillations libres » (pas de générateur) ; retirer de l'écran « amorties » et « se l'échangent », dits diapos 12 et 51. (Audit défaut 2 ; le prof regroupe les mots mais donne la cause.)
3. **Avant la diapo 6** : placer le rappel sinusoïde / amplitude / période (diapo 26, sans la formule). (Audit défaut 1 ; le prof n'emploie « période » qu'après avoir montré la courbe.)
4. **Avant la diapo 22** : rappel de la dérivée seconde (position → vitesse → accélération), ou placer la diapo 23 avant la diapo 22. (Audit défaut 6.)
5. **Diapo 23 ou 24** : dire que le terme en dq/dt (ou du_C/dt) est celui de l'amortissement, comme le prof, avant la diapo 25 qui le barre.
6. **Diapo 30 ou 33** : annoncer « T ≈ T₀ si l'amortissement est faible », vérifié diapo 46.
7. **Diapo 58** : ajouter la ligne « si R + r = 0, dE/dt = 0 : l'énergie se conserve », qui relie la preuve du prof à la nôtre (diapo 54).
8. **Diapo 2 ou 8** : citer la radio (le RLC choisit la station) comme porte d'entrée concrète ; elle prépare le cours de modulation.
9. **Ne pas ajouter** le régime critique (hors du cadre officiel retenu), malgré la remarque du prof.
10. **Garder** les autres corrections de l'audit (radian et cercle trigonométrique, défauts 8 et 12 ; dérivée du sinus, défaut 9 ; −sin α = cos(α + π/2), défaut 15 ; diapo 48 avant la diapo 36, défauts 10-11 ; énoncés dans l'ordre, défaut 16 ; questions de bloc, défauts 4, 5, 7, 13) : le prof ne les contredit pas.
