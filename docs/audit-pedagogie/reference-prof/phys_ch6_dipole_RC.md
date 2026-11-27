# phys_ch6_dipole_RC — comparaison avec le cours de référence d'un professeur

Source : cours polycopié d'un professeur marocain (2ᵉ Bac SP, 2022/2023), leçon 6 « Dipôle RC », pages 34 à 44. Résumé et comparaison avec nos mots ; le texte du professeur n'est pas reproduit.

## Plan du professeur (ordre des notions, en une liste courte)
1. Porte d'entrée : le flash d'un appareil photo contient un condensateur ; deux questions (qu'est-ce qu'un condensateur, quel rôle).
2. Rappels groupés : dipôle, sens conventionnel du courant, nature du courant (électrons en sens inverse), conventions récepteur et générateur, loi d'Ohm, **branchement de l'oscilloscope** (entrée Y à la borne d'entrée du courant, masse à l'autre).
3. Condensateur : définition (deux armatures, un isolant), symbole.
4. Expérience de charge puis décharge dans une diode électroluminescente (la DEL s'allume un instant) ; interprétation par les électrons (q_A = q = −q_B) ; le courant ne traverse pas l'isolant ; la décharge est montrée qualitativement dès ici.
5. i = dq/dt (débit de charges), avec le signe : i > 0 en charge, i < 0 en décharge.
6. q = C·u_C, le farad et ses sous-multiples ; i = C·du_C/dt.
7. Associations : série d'abord (même courant, tensions qui s'ajoutent), puis parallèle (loi des nœuds) ; intérêt de chacune.
8. Dipôle RC et échelon de tension (montant / descendant, définis par leurs valeurs avant et après t = 0).
9. Étude expérimentale de la charge et de la décharge : deux régimes, régime permanent atteint vers 5τ.
10. Étude théorique de la charge : équation en u_C, puis en q ; solution de la forme « constante + constante × exponentielle » ; deux constantes par l'équation, la troisième par la condition initiale ; q(t), i(t).
11. Même étude pour la décharge.
12. Constante de temps : définition, analyse dimensionnelle, deux méthodes de lecture en charge (63 %, tangente/asymptote) et en décharge (37 %, tangente/axe des temps).
13. Énergie : mise en évidence (la DEL), puis démonstration par la puissance reçue p = u_C·i, d'où E_e = ½·C·u_C² = q²/(2C).

## Porte d'entrée et rappels : où le prof les place, et nous
- **Porte d'entrée.** Prof : le flash d'appareil photo, puis l'expérience de la DEL qui s'allume à la décharge. Nous : diapo 2, la carte du chapitre (un réservoir de charges), puis l'expérience des aiguilles (diapo 10). Notre expérience montre mieux u_C et i ; la sienne montre d'emblée **à quoi sert** un condensateur (il rend une énergie). Nous ne parlons du flash qu'à la diapo 63. Proposition : une phrase et une image de flash à la diapo 2 ou 8, sans rien retirer.
- **Rappels groupés.** Le prof met tous les rappels d'électricité au début, **y compris le branchement de l'oscilloscope**. Nous rappelons courant, tension, loi d'Ohm, additivité, puissances de dix (diapos 3-7), mais le branchement de l'acquisition arrive d'un bloc à la diapo 21. **Le prof confirme le défaut 7 de notre audit** : le branchement (entrée Y, masse) doit être enseigné à part, avant d'être utilisé ; on peut le placer avec les rappels ou sur une diapo dédiée avant la diapo 21.
- **Conventions récepteur / générateur.** Le prof les rappelle ensemble ; nous n'avons que la convention récepteur (diapo 5). Suffisant pour ce chapitre.
- **La charge électrique et le coulomb.** Le prof définit q comme « quantité d'électricité », en coulomb, au moment de l'interprétation de l'expérience, puis i comme débit de charges. **Confirme le défaut 3 de l'audit** : dire le coulomb et i = q/t dès la diapo 3.
- **La puissance électrique.** Le prof s'en sert pour démontrer l'énergie (p = u·i). Nous la citons à la diapo 63 sans l'avoir rappelée. **Confirme le défaut 21 de l'audit.**

## Différences d'ordre qui comptent
| Notion | Place chez le prof | Place chez nous (diapo) | Ce qu'il faut changer chez nous |
|---|---|---|---|
| Décharge (vue qualitative) | Dès la première expérience (DEL), avant i = dq/dt | Diapo 14 en parle (« i négatif ») ; la décharge n'est montrée que diapo 20, étudiée diapos 57-60 | L'audit (défaut 5) propose de retirer la décharge de la diapo 14. **Le prof montre une autre solution** : faire voir la décharge (K basculé, une lampe ou une DEL s'allume un instant) dans l'expérience du début (diapo 10 ou 11). Alors « i < 0 en décharge » à la diapo 14 n'arrive plus trop tôt. Choisir l'une des deux ; celle du prof garde le contenu. |
| Additivité des tensions avec un condensateur | Pas dans les rappels ; écrite seulement dans l'étude du RC | Diapo 6, avant la diapo 8 qui présente le condensateur | Déplacer la diapo 6 après la diapo 8, ou faire l'exemple avec une lampe. (Audit défaut 1 ; le prof ne fait pas ce rappel trop tôt.) |
| Associations de condensateurs | Avant le dipôle RC, juste après q = C·u_C | Diapos 16-17, même place | Même place : garder. L'ordre série/parallèle est inversé, sans importance. |
| Échelon de tension | Défini avant l'étude expérimentale | Diapo 20, même place | Garder. |
| Étude expérimentale avant les équations (régimes, 5τ) | Oui | Oui (diapos 22-24) | Garder ; le prof donne « 5τ » dès l'expérience, nous à la diapo 42 : on peut l'annoncer dès la diapo 23 (« on verra que c'est environ 5τ »). |
| Solution « A + B·e^(−αt) » et condition initiale | Méthode unique dès la charge : deux constantes par l'équation, la troisième par t = 0 | Diapo 37-38 (A et τ), diapo 40 (A + B·e^(−αt) et condition initiale), diapo 41 (vérifier) | Rien à changer sur le fond ; l'audit (défaut 14) propose de mettre « vérifier » (diapo 41) avant « trouver » (diapo 37). Le prof ne fait pas de « vérifier » ; il ne tranche pas. |
| Dimension de τ | Après la charge et la décharge | Diapo 45, après la charge | Même idée ; garder. |
| Énergie | Mise en évidence par la DEL du début, puis démonstration par p = u·i | Diapo 63 (lampe), formule « admise » avec une phrase sur la dérivée | Ajouter le rappel p = u·i (en watt) avant la diapo 63 ; la démonstration courte du prof (p = C·u_C·du_C/dt = d(½·C·u_C²)/dt) peut remplacer la phrase actuelle. |

## Ce que le prof explique et que nous n'expliquons pas (ou mal) — avec la diapo où l'ajouter
- **Le rôle de l'isolant dans l'arrêt du courant** : le courant ne peut pas durer parce que l'isolant coupe le circuit. Notre diapo 8 dit « aucune charge ne passe », mais la diapo 10 ne relie pas « le courant ne dure pas » à l'isolant. Ajouter à la voix de la diapo 10 ou 11 : « le courant s'arrête parce que l'isolant coupe le circuit ».
- **L'intérêt des associations** : le prof dit que la série supporte une tension plus grande, et le parallèle stocke plus de charge sous une petite tension. Notre diapo 16 a l'intérêt du parallèle ; la diapo 17 n'a pas celui de la série (« supporter une tension plus grande »). L'ajouter à la diapo 17.
- **Décharge : les deux méthodes de lecture de τ** (37 % et tangente qui coupe l'axe des temps) : nous les avons (diapo 61), mais seulement sur i(t) de la charge ; ajouter l'exemple de u_C en décharge sur la même diapo (l'exercice y est déjà).
- **Les sous-multiples du farad avec le pico** : le prof les donne à q = C·u_C ; nous aussi (diapo 12), mais pas dans le rappel des puissances (diapo 7). (Audit défaut 2.)
- **Le flash** comme usage, dès l'introduction (voir plus haut).

## Définitions et méthodes : formulation du prof vs la nôtre (seulement quand la nôtre est moins exacte ou moins conforme au programme)
- **Énergie emmagasinée** : nous écrivons « expression admise » et justifions le ½ par une dérivée (diapo 63). Le prof la démontre par la puissance reçue. Notre phrase « la dérivée de ½·C·u_C² est u_C·i, la puissance reçue » est juste, mais elle suppose deux notions jamais vues (puissance, dérivée d'un carré). Soit dire seulement « expression admise » (conforme au programme), soit ajouter les deux rappels.
- **Constante de temps, méthode de la tangente** : prof et nous disons « abscisse de l'intersection de la tangente à l'origine avec l'asymptote (charge) / avec l'axe des temps (décharge) ». Conforme.
- **Échelon de tension** : le prof le définit par les valeurs de la tension avant et après t = 0 (0 puis E ; E puis 0). Notre diapo 20 dit la même chose avec K ; conforme.

## Ce que nous faisons mieux (court ; à garder)
- Les aiguilles de l'ampèremètre et du voltmètre (diapo 10) : on voit i sauter et u_C monter, ce que la DEL ne montre pas.
- La dérivée comme pente (diapo 13) avant i = dq/dt ; le prof l'utilise sans rappel.
- L'équation construite par l'élève en trois étapes (diapos 26-28), puis la rédaction du corrigé (diapo 29).
- Le générateur de courant (diapos 18-19) et les courbes sans le temps (diapos 55-56), demandés au national et absents chez le prof.
- Le tableau des huit équations (diapo 62).

## Corrections recommandées pour notre cours (liste numérotée, concrète : diapo, quoi, pourquoi), sans raccourcir le cours
1. **Avant la diapo 21** : une diapo (ou un rappel ajouté aux diapos 3-7) sur l'oscilloscope / l'acquisition : entrée Y, masse, « tête de flèche → entrée Y », sur un dessin ; puis la diapo 21 applique la règle. (Prof : rappel groupé au début ; audit défaut 7, confirmé.)
2. **Diapo 3** : ajouter « la charge q se mesure en coulomb (C) ; i = la charge qui passe en une seconde ». (Prof : q défini avec son unité ; audit défaut 3, confirmé.)
3. **Diapos 10-11** : ajouter la décharge vue qualitativement (on bascule K, une lampe s'allume un instant : le condensateur rend ses charges), et dire que le courant s'arrête parce que l'isolant coupe le circuit. Cela rend la phrase « i < 0 en décharge » de la diapo 14 légitime. (Alternative au défaut 5 de l'audit, tirée du prof.)
4. **Diapo 6** : la placer après la diapo 8, ou refaire l'exemple avec une lampe. (Audit défaut 1.)
5. **Diapo 17** : ajouter l'intérêt de la série (supporter une tension plus grande que chaque condensateur seul) et le rappel « R_eq = R₁ + R₂ » demandé par l'audit (défaut 6).
6. **Diapo 23** : annoncer « le régime permanent est atteint au bout d'environ 5τ, on le montrera » ; le prof le dit dès l'expérience, nous seulement à la diapo 42.
7. **Avant la diapo 63** : rappel d'une phrase sur la puissance p = u·i (watt) ; puis, au choix, la démonstration du prof ou « expression admise ». (Audit défaut 21, confirmé.)
8. **Diapo 2 ou 8** : citer le flash d'appareil photo comme usage dès l'entrée (le prof en fait sa porte d'entrée).
9. **Diapo 61** : ajouter la lecture de τ sur u_C en décharge (37 % de E, tangente qui coupe l'axe des temps), pas seulement sur i(t) de la charge.
10. **Garder** les corrections de l'audit sur les questions posées trop tôt (défauts 9, 10, 12, 15-20) et sur les énoncés lus dans le désordre (défaut 22) : le prof n'a pas de questions intercalées, il ne les contredit pas.
