# Analyse en profondeur des plateformes, avec REA

Octobre 2026. Suite de [lecons-des-tuteurs.md](lecons-des-tuteurs.md). Cette fois, on a analysé le code et les pages elles-mêmes, avec l'outil REA (rea-agents 6.7) et la lecture des dépôts ouverts. Les règles ont été les mêmes partout : uniquement ce qui est public, aucun compte créé, aucune connexion contournée, et on n'en retient que des idées de conception, jamais de code.

## 1. Ce qui a été analysé, et jusqu'où

| Plateforme | Ce que REA ou le code a montré | Ce qui est resté fermé |
|---|---|---|
| **PraxiLabs** | Catalogue complet : 203 expériences. Une page d'expérience passée dans REA ne charge aucune simulation : ni iframe, ni WebGL, seulement 9 petits scripts de site. Structure de 15 labos lue sur leurs pages publiques. | Les simulations elles-mêmes, réservées aux comptes. |
| **Khan Academy** | Code de Perseus, leur moteur d'exercices (licence MIT). Une page d'exercice publique passée dans REA. | La correction côté serveur, et le texte des indices. |
| **MATHia** (Carnegie Learning) | Démo élève publique passée dans REA. Le code de l'application contient les paramètres du modèle de maîtrise et les types d'indice. | Le code du serveur. |
| **CTAT** (Carnegie Mellon) | Un tuteur d'exemple lu en entier : graphe d'étapes, indices, erreurs prévues. | Rien, mais la licence est réservée à la recherche non commerciale. |
| **PhET** | Code des simulations pendule, condensateur et circuits. La simulation pendule en ligne, passée dans REA. | Le nouveau dépôt unique, pas encore public. |
| **Duolingo** | Tuteur de maths : machine à états, transitions, schéma des étapes (voir [lecons-des-tuteurs.md](lecons-des-tuteurs.md)). | La décision serveur. |
| **ASSISTments, Synthesis, Brilliant** | Documentation et jeux de données publics seulement. | Toutes les leçons et les aperçus : rien d'interactif sans compte. |

## 2. Le modèle commun : une question est un graphe d'étapes notées

Quatre systèmes analysés indépendamment font la même chose : CTAT, MATHia, Perseus et le tuteur de Duolingo.

1. **Une question est découpée en étapes**, chacune liée à une compétence. Dans le tuteur CTAT de l'addition de fractions : trouver le dénominateur commun, convertir, additionner. L'ordre peut rester libre.
2. **Les indices vont du général à la réponse.** MATHia a trois niveaux : rappeler le but de l'étape, expliquer la méthode, puis donner la réponse. CTAT fait de même : « que faire pour avoir le même dénominateur ? », puis « choisis un dénominateur commun », puis « entre 12 ».
3. **Les erreurs prévues ont leur message, rédigé à l'avance.** Chez CTAT : « au lieu d'additionner les dénominateurs… ». Chez Perseus, chaque réponse fausse anticipée porte son message, et chaque mauvais choix de QCM son explication. C'est un message rédigé par un enseignant, pas une explication improvisée.
4. **Incomplet n'est pas faux.** Chez Perseus, une réponse incomplète est « invalide » : l'élève reçoit un message et corrige sans perdre de points. MATHia autorise l'ambiguïté. C'est ce que fait déjà notre `<eval>incertain</eval>`.
5. **Une aide après une erreur ne pénalise pas.** Le texte de l'interface MATHia le dit à l'élève : demander un indice après une erreur n'affecte pas sa maîtrise.
6. **La clé de correction ne quitte pas le serveur.** Khan envoie l'item au navigateur sans les réponses.
7. **On suit l'élève par compétence.** Khan enregistre la série de réussites, les indices utilisés, le total juste et fait, et le niveau de maîtrise. MATHia utilise le modèle bayésien, avec un seuil de maîtrise et un nombre minimal d'exercices.

## 3. Les labos

**PraxiLabs** suit le même gabarit partout : buts, méthode, objectifs, théorie, principe (ce qu'on manipule, ce qu'on mesure, le graphe linéarisé), puis la grandeur calculée et l'écart en %. Sur 15 labos étudiés, 14 recoupent le programme de 2e bac. Ils visent l'université et ne couvrent pas ce que le national exige. Les principaux écarts :

| Labo PraxiLabs | Ce que le bac attend en plus |
|---|---|
| Charge et décharge RC | Tangente à l'origine, méthode des 63 % et 37 %, ln(u) = f(t), énergie |
| Pendule simple, ressort | Équation différentielle, amortissement, énergie, régime pseudo-périodique |
| Chute libre, plan incliné | Frottements fluides, vitesse limite, méthode d'Euler |
| Tir horizontal | Tir oblique : angle, flèche, portée, équation de la trajectoire |
| Vitesse du son par résonance | Retard entre deux micros, d = v·τ, diffraction |
| Dosages | Tangentes parallèles, pKa à la demi-équivalence, taux d'avancement |
| Estérification, saponification | Rendement, constante K ≈ 4, effet d'un excès de réactif |
| Absents | Dipôles RL et RLC, nucléaire, piles, électrolyse, cinétique |

Note : leur page « Forced Oscillations » ne traite pas d'oscillations forcées, c'est un ressort-masse.

**PhET** montre comment faire des labos justes, avec des méthodes que Moalim peut réécrire lui-même :
- le pendule calculé par Runge-Kutta d'ordre 4, en petits pas, avec un pas de temps plafonné à 0,05 s, un ralenti à 1/8 et un pas-à-pas de 10 ms ;
- la décharge du condensateur calculée par la solution exacte u·e^(−dt/RC), pas par approximation ;
- la période mesurée automatiquement au passage par la verticale ;
- un voltmètre qui affiche « ? » tant que ses sondes ne touchent rien ;
- deux boutons : « Relancer » qui garde les réglages, « Tout réinitialiser » ;
- des phrases générées à partir du modèle (« Voltmètre : 3,2 volts »), que la voix du professeur pourrait lire.

## 4. Ce qu'on a le droit de réutiliser

| Source | Licence | Pour Moalim, produit payant |
|---|---|---|
| Perseus (Khan) | MIT | Code réutilisable en citant la licence. Pour l'instant, on n'en prend que les idées. |
| PhET : code | GPL-3.0 | À ne pas copier : il faudrait publier le code de Moalim. |
| PhET : simulations récentes | CC BY-NC 4.0 | Pas d'usage commercial sans accord avec PhET. |
| CTAT | Recherche non commerciale | Idées seulement. |
| PraxiLabs, MATHia, Duolingo | Propriétaires | Idées seulement. |

Les idées et les équations ne sont pas protégées. Tout ce qui est proposé ci-dessous est réécrit par nous.

## 5. Adapté au bac marocain, et simple

La question ouverte du national est déjà découpée en étapes notées : c'est son barème. Chacun des 60 examens de la banque a sa correction question par question. Le modèle commun s'applique donc tel quel :

- **étapes** = lignes du barème officiel, avec leurs points ;
- **compétence** = domaine du cadre de référence (déjà enregistré depuis l'étape 1) ;
- **erreurs prévues** = celles qui coûtent des points au national : unité, signe, mauvaise loi, application numérique sans expression littérale ;
- **indices** = but de l'étape, puis méthode, puis réponse, en darija à l'oral si l'élève le veut, avec les termes d'examen en français.

**Pilote proposé, une seule question.** On prend une question RC d'un national récent et on la décrit à la main en étapes, avec indices et erreurs prévues. Le skill prof s'en sert pour une seule question. Contrôle : sur cette question, comparer la note par étapes du tuteur au barème officiel. Rien d'autre ne change tant que ce pilote ne tient pas.

Les labos viennent ensuite : un labo RC à nous, avec prédiction d'abord, mesures, graphe, puis lecture de τ par la méthode des 63 % et par la tangente, comme au bac.
