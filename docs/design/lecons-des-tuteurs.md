# Ce que les grands tuteurs enseignent à Moalim, adapté au bac marocain

Octobre 2026. Six plateformes étudiées : Duolingo, Carnegie Learning (MATHia), Khanmigo, ASSISTments, Brilliant et Synthesis Tutor. Pour les cinq dernières, uniquement ce qu'elles publient (articles, blogs, documentation). Pour Duolingo, en plus de [lecons-de-duolingo.md](lecons-de-duolingo.md), une lecture du JavaScript public de son tuteur de maths à des fins éducatives : on en retient des idées de conception, aucun code. Les chiffres marqués « vérifié » ont été relus à la source ; les autres viennent de résumés.

## 1. Ce qu'elles ont en commun

1. **Le contenu est écrit par des humains, l'IA choisit le chemin.** Le tuteur de Duolingo est un graphe d'étapes rédigées (objectif, piège prévu, réplique parlée). Le serveur ne fait que classer la réponse de l'élève parmi des transitions prévues : juste, faux, passer, continuer, incertain. Synthesis suit un script avec des branches. Khan a mesuré que son tuteur juge mieux quand il lit d'abord les étapes et solutions rédigées. Brilliant fait concevoir les leçons par des humains.
2. **Faire avant d'expliquer.** Brilliant pose le problème avant la procédure. Synthesis fait manipuler avant d'écrire un symbole. Khan demande « comment tu as trouvé ça ? » avant de corriger.
3. **Terminer n'est pas maîtriser.** MATHia ne fait avancer que quand chaque compétence fine dépasse une probabilité de maîtrise, 0,95 classiquement. ASSISTments exige 3 bonnes réponses d'affilée sans indice, l'indice remettant la série à zéro (vérifié). Duolingo n'efface une erreur que si l'élève réussit un exercice du même générateur. Khan juge son tuteur sur la réussite sans aide à l'exercice suivant de la même compétence.
4. **Revenir plus tard.** ASSISTments réévalue à J+7, J+14, J+28 et J+56 après la maîtrise ; un échec renvoie à la pratique (vérifié). Brilliant mélange les types de problèmes en pratique.
5. **L'aide a des niveaux.** MATHia donne trois niveaux d'indice : rappel du but, méthode, puis réponse de l'étape. Une erreur connue y déclenche un message ciblé immédiat, et une erreur bénigne ne fait pas baisser la maîtrise.

## 2. Ce que les essais mesurés disent vraiment

- **Khanmigo n'a rien ajouté de mesurable.** Essai randomisé sur deux ans dans 18 collèges du Tennessee : +0,06 à 0,08 écart-type par an, un gain « semblable » à Khan Academy sans IA. Les élèves ne l'ont sollicité que dans 17 % des séances où ils s'étaient trompés. Source vérifiée : Oreopoulos et Low, [NBER w35620](https://www.nber.org/papers/w35620). Un tuteur qui attend qu'on vienne le chercher, et qui refuse la réponse, est contourné.
- **Ce qui a marché chez Khan** (A/B tests vérifiés, [blog Khan, mai 2026](https://blog.khanacademy.org/?p=21314)) :
  - un vérificateur de calcul qui ne regarde que les étapes déjà écrites par l'élève : moitié moins de réponses données trop tôt ;
  - un résumé en texte des derniers essais de l'élève dans le prompt : +3,4 % de réussite à l'exercice suivant ;
  - un rappel des prérequis : +2,7 % ;
  - l'historique brut en JSON : aucun effet.
- **MATHia** : effet nul la première année, puis environ +8 points de percentile au lycée la deuxième ([RAND 2014](https://eric.ed.gov/?id=EJ1024233)). Il faut une année pour qu'un tuteur s'installe.
- **ASSISTments** : +0,18 écart-type sur 2 850 élèves dans le Maine, surtout chez les élèves faibles ([SRI](https://www.sri.com/publication/education-learning-pubs/digital-learning-pubs/how-big-is-that-reporting-the-effect-size-and-cost-of-assistments-in-the-maine-homework-efficacy-study/)). C'est le meilleur résultat mesuré, obtenu avec le système le plus simple : retour immédiat et maîtrise stricte.

## 3. Où en est Moalim

Moalim fonctionne pour la 2e bac Sciences Physiques BIOF, en Maths, PC et SVT. Il dispose :
- des trois cadres de référence officiels, avec le poids de chaque domaine à l'examen ;
- de 60 examens nationaux de 2016 à 2025, notés sur 20, où les questions ouvertes dominent : 1 700 contre 22 QCM.

| Leçon | Dans Moalim |
|---|---|
| Contenu rédigé, IA qui choisit le chemin | En partie : cours rédigés, mais le modèle génère librement le tour. |
| Classer la réponse, y compris « incertain » | Fait : `<eval>` correct, partiel, faux, incertain. |
| Effacer une erreur par une nouvelle réussite | Préparé : `boite_erreurs.py`, pas encore branché. |
| Maîtrise par compétence fine, gardée d'une séance à l'autre | En partie : `knowledge_tracing.py` estime, mais oublie à chaque séance. |
| Notions normalisées | Absent : `topic` est du texte libre, sans lien avec le cadre de référence. |
| Révision espacée | Absente en pratique : la table existe, rien ne l'appelle. |
| Mesure de la réussite sans aide à l'exercice suivant | Absente. |

## 4. Adapter au bac marocain

1. **Les notions sont les domaines du cadre de référence.** Chaque réponse enregistrée doit porter la clé du domaine officiel (par exemple Mécanique, Électricité), pas un titre libre. C'est la condition pour que la boîte à erreurs, la maîtrise et le plan d'études parlent de la même chose. Les cadres donnent aussi les niveaux d'habileté (restitution, application, situation-problème). Une notion n'est maîtrisée que si l'élève réussit au niveau que le national exige pour elle.
2. **Choisir quoi revoir selon le poids au national.** À maîtrise égale, la Mécanique (27 % de l'épreuve de PC selon le cadre de référence) passe avant un domaine qui pèse moins. `study_plan_service.py` pondère déjà les matières par leur coefficient ; il faut descendre au domaine.
3. **Les erreurs typiques viennent des corrections du national.** Les 60 examens ont leur barème et leur correction question par question. On peut en tirer, pour chaque type de question, les erreurs qui coûtent des points : unité oubliée, signe, mauvaise loi, justification absente. Chacune reçoit un message ciblé, comme les erreurs connues de MATHia. Et « partiel » se lit comme au bac : des points pour la démarche, pas tout ou rien.
4. **Questions ouvertes : moins de part au hasard.** Le paramètre « réussir sans savoir » du modèle de maîtrise vaut 0,20, une valeur de QCM. Pour une question ouverte du bac, il doit être bien plus bas. Notre « chance d'apprendre » vaut 0,15, au-dessus de la borne de 0,1 souvent citée (non relu à la source) : à revoir.
5. **La langue.** L'élève peut expliquer son raisonnement en darija à l'oral, et c'est souhaitable : c'est la reformulation demandée par le skill prof. Mais la réponse ne compte que si les termes d'examen en français sont là, car c'est en français qu'il sera noté (BIOF).
6. **Le calendrier.** La date d'examen est figée au 4 juin 2026 dans `study_plan_service.py` et `BacCountdown.tsx`, donc déjà passée : elle doit devenir un réglage, avec la session de rattrapage. Le rythme J+7, 14, 28, 56 se cale sur cette date : rien de nouveau dans les dernières semaines, seulement de la révision mélangée, puisque le national mélange les chapitres.
7. **Ne pas faire fuir.** L'essai Khanmigo montre qu'un refus rigide fait partir les élèves. Le skill prof donne la réponse après deux essais, et c'est bien. Ce qu'il faut ajouter : avant de juger une réponse fausse, demander « comment tu as trouvé ça ? ». Et proposer au lieu d'attendre : un élève de bac qui se trompe ne demande pas d'aide.
8. **Les laboratoires d'abord.** En PC et SVT, chaque étape d'un cours peut s'ouvrir sur une prédiction dans le labo (« si on double la résistance, que devient l'intensité ? »). L'explication vient après la réponse, plus courte. On peut aussi attendre un état précis de la simulation avant d'avancer, comme Synthesis.

## 5. Comment avancer : simple, contrôlable, suivable

On ne met pas tout en place d'un coup. On adapte d'abord au contexte marocain, une étape à la fois. Chaque étape :
- change une seule chose ;
- se vérifie par un contrôle simple, lisible sans lire le code ;
- est observée au moins une semaine avant de passer à la suivante.

### Phase 1 : le contexte marocain, rien d'autre

| Étape | Ce qui change | Comment on contrôle |
|---|---|---|
| 1. Notions officielles | Chaque réponse enregistrée porte le domaine du cadre de référence (Mécanique, Électricité, Ondes…), choisi dans la liste officielle. Si aucun domaine ne correspond, on enregistre « non classé », sans rien deviner. | Pour un élève, le décompte des réponses par domaine officiel. La part de « non classé » doit baisser. |
| 2. Date d'examen réglable | La date du national et celle du rattrapage deviennent des réglages, au lieu du 4 juin 2026 écrit en dur. | Le compte à rebours et le plan d'études affichent la date réglée. |
| 3. Fiche de suivi par élève | Une vue simple par domaine : réponses justes, fausses, incertaines, poids du domaine au national. | Un enseignant lit la fiche et comprend où en est l'élève sans explication. |

Ce qui est déjà fait reste en place sans rien décider à la place de l'élève : `<eval>` « incertain » demande seulement de préciser, et `boite_erreurs.py` n'est pas branché.

### Plus tard, une étape à la fois, seulement si la phase 1 tient

1. Enregistrer les réponses depuis `<eval>` plutôt que par mots-clés.
2. Brancher la boîte à erreurs : une question sur le domaine le plus raté, en début de séance.
3. Garder la maîtrise d'une séance à l'autre et revoir les paramètres pour les questions ouvertes.
4. Révision espacée J+7, 14, 28, 56, calée sur la date réglée.
5. Erreurs typiques tirées des corrections du national ; cours en étapes avec prédiction dans le labo.

Chacune n'est gardée que si l'indicateur suivant s'améliore : la réussite sans aide à la question suivante sur le même domaine.

## 6. Ce qu'il ne faut pas reprendre

- **Le blocage jusqu'au lendemain** d'ASSISTments après 10 questions sans maîtrise. Il laisse le temps à l'enseignant d'intervenir ; Moalim n'a pas d'enseignant derrière. On signale le blocage et on change d'approche.
- **Le tuteur qui attend qu'on vienne le chercher.** C'est la principale leçon de l'essai Khanmigo.
- **Le refus absolu de donner la réponse.** Il fait fuir les élèves pressés par l'examen.
