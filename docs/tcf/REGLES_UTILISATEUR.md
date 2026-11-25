# Règles de l'utilisateur (copiées de la mémoire du projet, 25/11/2026)

Chaque section ci-dessous est une règle donnée par l'utilisateur ; elles s'appliquent toutes aux cours de /TCF.

## rythme-et-depart-de-zero

**Rythme.** Une expérience se fait dans cet ordre :
1. le principe d'abord, puis une question de vérification ;
2. chaque cas joué seul, arrêté, avec son résultat et un temps pour regarder ;
3. le cas décisif (la 4ᵉ souris de Griffith) n'est pas donné : question d'observation (micro, puis cartes après un délai) ; résultat et conclusion seulement ensuite.
4. après la dernière expérience seulement, un écran de bilan montre toutes les expériences ensemble, avec leurs résultats et la conclusion (Griffith : `ig_t1f_bilan`).

**Départ de zéro.** On considère que l'élève ne sait rien. Les notions des années d'avant (mitose, chromosome, vecteur, mole…) sont enseignées depuis zéro au début du cours, jamais supposées connues. Chaque notion est expliquée deux fois, de deux façons différentes.

**Why:** le 14 novembre 2026, sur Griffith (SVT ch3) : « il donne tout d'une manière rapide, l'élève ne peut pas le suivre ». Et : « le cours commence par la mitose et les chromosomes alors que la plupart des élèves ne connaissent pas encore ces notions ».
**How to apply:** règles 33 et 34 du skill professeur. Les scripts réécrits attendent dans `backend/data/courses/en_attente/<deck>.json`, avec l'`audio` retiré, jusqu'à leur voix Bodi. Audit dans `docs/audit-rythme/`. Voir [[question-eleve-au-tableau]], [[philosophie-resultats-memoire]], [[animations-plutot-que-tableaux]].

## simulation-d-abord

Demande de l'utilisateur (18 novembre 2026, 4 captures du cours des ondes sur un écran de bureau peu haut ~1360×560) : « le texte est plus grand que la simulation, et aussi dans la question ; donner davantage de taille aux simulations et gagner de l'espace ; l'ajouter comme skill et l'appliquer à tous les cours ».

**Why:** les cartes `screen_content` (20 px sous une simulation, 30 px sans) prenaient la moitié de la hauteur ou débordaient sur le titre ; les simulations se dessinaient petites (étiquettes ~8 px) ; le cadre « Observe » était plus grand que la simulation.

**How to apply:** la simulation remplit son cadre et garde ~70 % de la scène ; 1 à 3 cartes courtes, en colonne étroite à droite (15-18 px), qui ne répètent pas la simulation ; sans simulation, la liste s'ajuste à la hauteur ; question d'observation en bande fine. Vérifier à 1366×560, 1920×1080 et 724×350. Ne jamais changer un texte dit par la voix pour gagner de la place. Règle dans la skill simulations-au-tableau (session cloud « lecteur-sim-d-abord »). Voir [[telephone-en-paysage]], [[simulations-sur-toute-la-largeur]], [[tableaux-ecran-et-formules]].

## croquis-realistes

Dans les animations et les dessins du cahier, un muscle, un os, une cellule, un bécher, un marteau… est **peint en couleur et réaliste** sur le canvas, avant la craie : dégradés, ombre, texture, vraies proportions. La craie garde les légendes, les flèches, les courbes et les valeurs. Simple, mais reconnaissable au premier coup d'œil. Modèle : `peindreMuscle` de `svt/role_muscle_strie_squelettique-tableau/chaleur.html`, repris dans `consommation.html`.

**Why:** le 14 novembre 2026, sur le muscle de `consommation.html` dessiné en deux traits de craie : « au lieu de mettre un croquis de mauvaise qualité, veuillez mettre un dessin avec des couleurs… toujours chercher le réalisme dans les croquis ».
**How to apply:** règle 32 du skill professeur. Voir [[animations-plutot-que-tableaux]], [[cahier-avec-dessins]], [[labos-dessines-au-tableau]].

## compter-en-allumant

Demande de l'utilisateur (18 novembre 2026, capture des ondes « VII.1 b Correction jouée : Δt, puis v » où les 5 divisions étaient comptées avec des chiffres rouges griffonnés) : « allumer les divisions quand on compte, ou pour expliquer ces types, divisions ou autres, dans tous les cours ; on veut le maximum de concentration ».

**Why:** l'allumage tour à tour garde l'œil de l'élève sur l'élément compté ; des chiffres griffonnés ou tout marqué d'un coup dispersent l'attention.

**How to apply:** skill simulations-au-tableau règle 16, professeur règle 44 (e3bf62d4). Chaque élément compté s'allume (halo doux) avec son numéro propre à la craie, reste allumé, total écrit à la fin puis utilisé dans la formule ; un repère par élément pour que le tuteur s'y arrête. Voir [[simulation-d-abord]], [[animations-plutot-que-tableaux]].

## un-objet-un-seul-dessin

Règle de l'utilisateur (18 novembre 2026, deux captures de SVT ch1) : « une fois qu'un élément du cours est modélisé ou représenté sous une forme, il doit rester sous la même forme dans tout le cours pour ne pas perturber les élèves ». Le glucose était une chaîne de 6 billes jaunes dans « La glycolyse : où ? » (`glycolyse.html`), mais deux rangées de 3 dans la carte (`carrefour.html`), un anneau dans `depart.html` et des billes blanches dans `comparer.html`.

**Why:** un dessin différent fait croire à l'élève que c'est une autre chose (deux rangées de 3 = déjà deux acides pyruviques).

**Généralisé le même jour** : « pour tous les cours de toutes les matières ; dans les prochains cours, le glucose garde la même forme et les mêmes couleurs dans toutes les matières ». Donc un seul lexique pour tout le site : `docs/lexique-visuel.md` + module de dessin partagé dans `frontend/public/media/simulations/shared/`.

**Puis, toujours le 18/11** : « une lexique commune à chaque élément ; chaque nouveau cours va vers ce lexique ; une molécule de glucose a plusieurs formes, développée, semi-développée… ; chaque élément a son propre lexique ». Format : `docs/lexique-visuel/README.md` + `docs/lexique-visuel/<element>.md` (toutes les formes : brute, développée, semi-développée, cyclique, simplifiée des animations ; quand utiliser chacune) ; module `simulations/shared/lexique/` avec `{ forme: … }`.

**How to apply:** règle 15 du skill simulations-au-tableau, règle 43 du skill professeur, règle 10 de logique-de-cours. Une fonction de dessin par objet dans le script commun du dossier du cours (`peinture.js` / `commun.js`), utilisée par toutes ses simulations ; un « Lexique visuel » (objet → forme, couleur, étiquette, fonction) dans `backend/data/curriculum/architecture/<deck>.md` ; ce que l'objet devient se dessine à partir de lui ; une couleur garde son sens dans tout le cours. Voir [[animations-plutot-que-tableaux]], [[croquis-realistes]].

## cahier-general-et-organise

Demande de l'utilisateur du 24/11/2026 pour le cahier :
- Le cahier ne contient que le cours en général, jamais les données d'un exercice ou d'un document (S1/S2, Maâmora, zones A/B/C…). En révisant, l'élève n'a pas les énoncés.
- Il doit être organisé : titre au milieu, paragraphe qui commence à gauche, définitions encadrées à part, tableaux dès qu'on compare des cas, graphes, formules encadrées.
- Les couleurs suivent une charte fixe.
- Il est écrit au niveau de la classe : le Tronc Commun n'est pas le 2ᵉ Bac.

**Why:** avant, le cahier était du texte en vrac, plein de chiffres d'exercices, inutilisable pour réviser seul.

**How to apply:** suivre le skill cahier-de-l-eleve (§ 2 bis, § 6 et § 7). Chaque ligne commence par le bon préfixe (I., 1., Définition :, Formule :, Méthode :, Attention :, Donc, lignes « | a | b | »), car `memoire/LignesCahier.tsx` les met en forme. Voir [[cahier-avec-dessins]].

## cahier-avec-dessins

Le contenu « À écrire dans le cahier » ne doit pas être que du texte : quand la notion se dessine, une courbe, un schéma
ou un croquis simple et légendé l'accompagne (axes avec unités, valeurs du cours, une légende qui dit quoi voir). Pas un
dessin partout : environ un par bloc au plus, rien pour une définition verbale, une carte ou un bilan.

**Why:** demande de l'utilisateur (14 novembre 2026) — « il n'y a que du texte, aucune courbe, aucun graphe, aucun
croquis » ; l'élève recopie pour la mémoire longue, et un dessin aide à comprendre et à retenir.

**How to apply:** données `cahier_figures` sur la diapo (`concentration`) et sur le bloc (2 au plus) ; format
`docs/audit-cahier/FORMAT.md`, rendu `FigureCahier.tsx`, vérificateur `backend/scripts/verifier_figures_cahier.py`.
À l'étape cahier, le tuteur invite en darija à écrire (avantages : ancrer, mémoire longue, bien écrire, relire de temps en temps), une phrase différente à chaque fois (`memoire/invitationsCahier.ts`, 12 phrases ; pistes Bodi `reactions/cahier-N.mp3` via le lot `/srv/corpus_v4/voix_lot/_cahier_invitations`, puis remplir `AVEC_PISTE`). Le texte et les dessins doivent être grands : `SansDefilement` cherche le plus grand zoom qui tient (dichotomie). Règle 31 du skill professeur, étape 5 du skill cours-concentration. Même esprit que [[animations-plutot-que-tableaux]] ;
voir aussi [[cours-en-mode-concentration]] et [[tableaux-ecran-et-formules]].

## une-seule-voix

Une seule voix à la fois, celle de l'écran visible. Ouvrir une question pendant l'explication met l'explication en pause ; fermer l'écran coupe sa voix, et l'explication reprend là où elle s'était arrêtée. Tous les lecteurs (piste de la diapo, voix du tuteur, voix du cycle de mémoire) sont inscrits dans `frontend/src/components/course/voixUnique.ts`.

**Why:** le 14 novembre 2026, l'utilisateur a entendu l'explication et l'énoncé de la question en même temps : « normalement il doit arrêter l'explication… si l'écran est fermé, l'audio doit aussi stopper ».
**How to apply:** tout nouveau `new Audio` ou `<audio>` appelle `inscrireVoix`. Règle 29 du skill professeur. Voir [[cours-en-mode-concentration]], [[question-eleve-au-tableau]].

## telephone-en-paysage

Le lecteur de cours sera utilisé sur téléphone en **paysage** (~724 × 350 px CSS). Tout doit tenir sur un seul écran, bien
rangé : simulation, titre, questions, écriture, bulles, tuteur, sans défilement ni texte qui chevauche (demande du 16/11/2026,
capture du ch11 chimie où « atome de sodium Na » chevauchait « atome de chlore Cl » et le tuteur couvrait la barre du haut).

**Why:** un plancher de texte fixe (`craie.tailleMin = 18`) gardait le texte grand pendant que le dessin rétrécissait →
chevauchements ; le tuteur 180 × 320 px prenait toute la hauteur.

**How to apply:**
- Le kit `shared/tableau/tableau.js` réduit le plancher sous 900 × 400 px (jamais sous 60 %) : une simu ne doit pas
  contourner ça avec ses propres tailles en px écran fixes.
- Le tuteur rétrécit quand `innerHeight < 520` en paysage (`echelleTuteur`, `useColonneTuteur` dans `AIAvatar.tsx`) ;
  toute nouvelle zone qui réserve sa colonne doit utiliser `useColonneTuteur()`, pas `COLONNE_TUTEUR`.
- Styles compacts dans `ANIMATIONS` de `CourseFocusStage.tsx` sous `@media (max-height: 520px) and (orientation: landscape)`.
- Tester à 724 × 350 et 640 × 320 (dev server « cours-ondes », `?cours=…&diapo=…`) avant de livrer un écran.
Voir aussi [[simulations-sur-toute-la-largeur]], [[tableaux-ecran-et-formules]].

## nombres-jamais-colles-darija-francais

Dans tout texte dit par la voix (cours, réactions, démonstrations, énoncés, cahier), un nombre ou une formule ne mélange
jamais darija et français dans deux mots successifs : « جوج noyaux » → « deux noyaux », « x زائد واحد » → « x plus un »,
« dix أس ناقص خمسة » → « dix puissance moins cinq », « تسعمية nanomètre » → « neuf cents nanomètre ». Un comptage
entièrement en darija (« جوج طرق ») reste tel quel : l'utilisateur veut « simplement éviter ce mélange », rien de plus.

**Why:** l'utilisateur l'a redemandé le 22/11/2026 en entendant 400–800 mal dits en physique ch3 ; la règle du 21/11
n'avait été appliquée qu'aux nombres (pas aux opérateurs زائد/ناقص/يساوي/أس ni aux centaines en un mot), et le
modèle Bodi déforme aussi des nombres bien écrits (« huit cents » entendu « deux cent vingt »).

**How to apply:** la règle est forcée dans le code depuis 6027fc83 : `texte_parle.parle` applique `nombres_darija_fr`
en premier (cours, lots, cache, réponses libres du tuteur après repush du kernel en direct), et le prompt du tuteur
(`llm_service.py`) la donne ; skills voix-du-cours § 1/§ 5 et prononciation § 8. Pour un cours : passer `scripts/voix/nombres_fr.py` (et ses tests `test_nombres_fr.py`) sur tout texte avant de
générer une voix ; contrôler ensuite par transcription (STT) que les nombres entendus sont ceux du texte. Vérifier
aussi « que toutes les phrases sont bien écrites d'abord » : mots cassés à moitié arabes/latins (« فالنoyau »,
« زéro », « Mزيان ») et mots d'arabe classique mal lus (« نقل » dans le cahier). Voir [[voix-bodi-pour-tout]],
[[academy-tts-ignore-le-tachkil]].

## animations-plutot-que-tableaux

Une diapo qui compare des valeurs, montre l'effet d'un paramètre ou décrit des étapes se fait en **petite animation au tableau que l'élève manipule** : les valeurs sont le résultat de ce qu'on voit, un ou deux curseurs (température, tension, R, C, concentration…) changent le paramètre et l'effet se voit tout de suite. Simple, utile, agréable : un bouton, ≤ 2 curseurs. Le tableau ne reste que pour la fiche bilan, la carte, ou les données que l'examen donne en tableau. Modèle : `ondes-tableau/milieux.html` sur `wx_c2_facteurs` (course du son acier/eau/air, curseur de température de l'air).

**Why:** l'utilisateur, le 14 novembre 2026, sur le tableau des célérités : « il fallait penser à les créer avec des petites animations pour ancrer la notion au lieu de le faire sous forme écrite ou tableau » ; puis « faire des manips dans l'air… changer la température et voir les changements, généraliser pour les autres cours ».
**Étendu le 18/11/2026** (capture téléphone de `le_m3a_glucose_marque`, glucose marqué ¹⁴C : tableau T0-T4 + quatre encadrés de conclusion qui débordaient sous la barre) : « ce type d'activité, c'est mieux de le faire sous forme d'animation au lieu de texte ; toujours le privilégier ». Toute activité dont le résultat change (temps, compartiments, avant/après, avec/sans) s'explique par l'animation **autant que possible** (ce qui bouge se voit, un moment par temps, conclusion après la réponse de l'élève) ; vérifiée au téléphone en paysage. **Nuance immédiate de l'utilisateur : « le maximum possible, pas jamais »** — au bac il y a des tableaux, l'élève doit s'y habituer : l'animation se change ensuite en tableau à la manière de l'examen, que l'élève lit lui-même ; combiner texte / tableau / animation selon le besoin, chaque choix avec sa raison. Règle 42 du skill professeur et skill logique-de-cours ; diapos restantes listées dans `backend/data/curriculum/architecture/animations_a_faire.md`.

**How to apply:** règle 28 du skill professeur et étape 3 de cours-concentration. On garde la voix existante en réécrivant seulement le `pointage` sur ses mots. Voir [[labos-dessines-au-tableau]], [[tuteur-pilote-les-simulations]], [[cours-en-mode-concentration]].

## donnees-tabulees-animation-puis-tableau

Un tableau de données que l'élève lit (Chargaff, comptages de cellules, pH mesurés…) n'apparaît jamais d'abord en tableau : l'animation peinte produit les valeurs (compteurs, appareil), fait VOIR la comparaison (A et T au même niveau), puis s'efface et les nombres volent dans le tableau ; colonnes calculées et conclusion en dernier. Restent des tableaux : signe, variations, avancement, méthodes, bilan, carte, données d'examen.

**Why:** demande de l'utilisateur du 14 novembre 2026 sur le tableau de Chargaff (« ensuite seulement l'animation se transforme en tableau »).

**How to apply:** règle 35 du skill professeur et étape 3 de cours-concentration ; modèle : vue `chargaff` d'`adn.html` (diapo ig_s2_chargaff). Voir [[animations-plutot-que-tableaux]], [[croquis-realistes]].

## tableaux-ecran-et-formules

Règles données par l'utilisateur le 12 novembre 2026 (ajoutées au skill cours-concentration, « The screen ») :
- Tout tableau montré à l'élève tient dans UN écran, sans défilement (composant `SansDefilement.tsx`, zoom pour remplir) ; un contenu trop long se coupe en deux, jamais de défilement.
- Le tableau du tuteur (question de l'élève, démonstration) s'ouvre en GRAND devant la diapositive, pas en petit cadre sous la figure.
- À l'écran, une formule s'écrit en notation (« g(x) = (2x² − 8)/(x − 2) », « 8 », « 3 ms ») ; les mots (« égale », « au carré », « huit ») ne vont que dans la voix. Règle ajoutée à REGLES_VOIX (simulation_reaction.py) pour toutes les questions/explications générées en direct.
- La fenêtre de bloc a un × ; après un « retrouver », la correction s'écrit sur le tableau de démonstration.

**Why:** l'élève doit tout voir d'un coup et lire comme au tableau du prof ; les questions de reprise s'affichaient « égal deux x au carré ».
**How to apply:** tout nouvel écran ou cours vérifie l'absence de défilement ; tout texte écrit généré par un LLM reçoit la règle d'écriture. Voir [[cours-en-mode-concentration]], [[voix-bodi-pour-tout]].

## tuteur-pilote-les-simulations

Demandé le 6–7 novembre 2026 : le tuteur comprend et explique ses simulations, va jusqu'à l'élément à montrer, peut les lancer, mettre en pause, reprendre et relancer autant de fois que l'explication ou l'élève le demande, peut afficher une autre simulation, et répond aux questions libres pendant le cours en s'appuyant sur la simulation affichée. Il doit « voir ce qui se passe » en temps réel (l'utilisateur a proposé l'OCR DeepSeek).

**Why:** être « sur la même longueur d'onde » que l'élève, comme un prof qui voit le tableau.

**How to apply:** chaque manip expose `pause`/`resume`/`set_time`/`set_parameters` et met dans son état une phrase `ce_qui_se_voit` renvoyée en direct (~2 fois/s) — plus exact, instantané et gratuit qu'un OCR d'écran ; l'OCR ne reste qu'un repli pour une simulation tierce qui ne se décrit pas. Règles du prompt : `simulation_explication.regles_du_pilotage`. Les manips pour qu'il « ramène une autre simulation » doivent être enregistrées comme ressources de la leçon. Voir [[labos-dessines-au-tableau]].

Ajout du 8 novembre 2026 : ce que le tuteur dit, la simulation le montre au même moment. Une phase décrite (« M monte, descend, revient ») se rejoue et se fige sur l'instant (`play_until {moment}`) ; jamais commentée sur une scène déjà finie. Les instants clés sont extraits de la simulation d'abord (`moments` nommés, calculés depuis la physique). Règle 18 du skill professeur.

Ajout du 8 novembre 2026 (2) : s'il y a une variante (M₂ plus loin…), le tuteur la fait lui-même pour comparer ; si l'élève la fait lui-même, son nouveau résultat est interprété sur-le-champ (DeepSeek), dit par la voix en direct, suivi d'une question (vrai/faux, QCM ou directe selon sa compréhension), sans quitter la diapositive. Règle 19 du skill professeur.

Ajout du 17 novembre 2026 (remplace « se rejoue » ci-dessus pour le cours) : ce qui est dessiné reste au tableau jusqu'à la
diapositive suivante — un `start`/`resume`/`play_until` reçu après coup ne rembobine plus (garde `sansRetourArriere` dans
`shared/tableau/tableau.js`) ; seuls Réécouter (`reset`) et Rejouer recommencent. Dans le cours, la baguette ne va **jamais**
vers les boutons de la simulation (Lancer, Pause, Observe…) : ces commandes partent seules ; elle ne montre que les repères
(`highlight`). Le professeur reste visible (l'utilisateur a refusé qu'il disparaisse au clic sur la simulation).

Ajout du 17 novembre 2026 (2) : signalé sur la chaîne respiratoire (cours SVT réactions libératrices d'énergie) — le prof
parlait de l'oxydation de NADH,H⁺ sans que la simulation la montre, et la baguette se posait sur un autre objet. Règle :
chaque processus nommé a un moment animé qui part avec la phrase ; la baguette se pose sur l'objet nommé, jamais un voisin.
Correction + règle au skill confiées à des sessions cloud (chaîne respiratoire, cours SVT ch1/ch2, ch3/ch4).
Même jour, en local (carrefour.html) : un réactif dégradé reste au tableau, pâli et marqué « (dégradé) » (règle 39 du skill
professeur, « faciliter le suivi »). Causes trouvées de la baguette mal posée : repère pas encore dessiné → l'avatar visait le
milieu de l'iframe ou un bouton (corrigé : attente ≤ 3 s) ; scène qui part seule (`demarrer: start`) et dépasse la voix →
geler au premier mot ; play_until lointain → rattrapage accéléré (commun.js). Contrôle : scripts/verifier_pointage.py et
scripts/verifier_baguette.py (serveur labo-site, port 8772, Chrome local).

## philosophie-resultats-memoire

Un cours ne se juge pas à sa beauté mais à ce que l'élève sait encore plus tard. Chaque cours doit respecter la limite de ce qu'un élève peut capter (temps et quantité d'informations) : une fois cette limite atteinte, on arrête d'expliquer, on lui fait écrire dans le cahier, puis un exercice pour fixer ; et il faut une stratégie pour faire passer les notions de la mémoire courte à la mémoire longue.

**Why:** demande de l'utilisateur du 11 novembre 2026 (« on veut des résultats, pas seulement une belle plateforme »), qui reprend ses messages du 3 août (« explique, attend, pose des questions, attend l'élève, puis la deuxième étape ») et du 17 août 2026 (temps d'apprentissage, alterner, rythme de l'élève). L'audit du même jour montrait des cours de 47 à 68 diapositives à la suite, 100 % de QCM, passage automatique.

**How to apply:** appuis de recherche retenus — mémoire de travail ≈ 4 éléments (Cowan 2001), charge cognitive (Sweller 1988), découpage au rythme de l'élève (Mayer, effet médian 0,79), questions intercalées (Szpunar 2013), se tester plutôt que relire et révisions espacées (Roediger & Karpicke 2006, Cepeda 2008, Dunlosky 2013). Ne pas s'appuyer sur les « styles d'apprentissage » (non confirmés) : adapter sur ce que l'élève a réussi. Mesurer par un rappel différé (J+1, J+7, J+30), pas par la réussite pendant le cours. Précisions du 11 novembre 2026 : les rappels ne mélangent JAMAIS les matières (seulement la matière du cours ouvert) ; tout est tracé (chaque rappel, cahier, saturation, séance, notification) ; notifications par élève selon ce qui est dû et sa durée, au plus une par jour ; l'expérience reste simple et agréable. Changements validés au lecteur : 1 prévoir d'abord, 2 temps de réflexion avant les choix, 3 l'élève décide quand avancer (« Suite → », plus de passage automatique). Écrit dans les skills cours-concentration (« Memory and rhythm »), suivi-des-acquis (6–8), professeur (règle 26). Voir [[cours-en-mode-concentration]], [[suivi-des-acquis-par-competence]].

## programme-hors-cadre

Un cours ne garde une notion vue par un ou deux profs que si le cadre de référence ou un **national de la filière PC/SVT** l'exige ; un devoir, un contrôle, un examen SM ou « les profs le font » ne suffit pas. Jamais de partie « pour les devoirs ».

**Why:** le 15/11/2026, une professeure de maths a jugé le cours de limites trop long et hors sujet ; la dichotomie (maths ch1) et les relations du prisme (physique ch3) y étaient entrées comme « pour les devoirs », l'agent les ayant même ajoutées comme capacités du cadre (LC7, OL11). L'utilisateur les a fait retirer.

**How to apply:** chaque partie d'un plan cite sa notion de `perimetre.json` ; ne jamais assouplir les `termes_hors_programme` ni ajouter une capacité au cadre pour faire passer un contenu — le signaler à l'utilisateur. Règle inscrite dans les skills exploration-de-cours et cours-concentration. Voir [[exploration-avant-chaque-cours]], [[cours-en-mode-concentration]].

## pas-de-photocopie-de-tableau

Un tableau de données d'un document (relevés, résultats d'expérience…) ne s'affiche pas en photocopie : on le recrée au tableau, puis on le remplit en animation (cases qui s'allument, nombres qui volent dans leur case, l'élève calcule une partie). Puis précisé : « la même chose pour les autres diapos » — aucune diapo ne montre une photocopie ou image du document du prof (profil de sol, coupe, outils, herbier…) : tout est recréé au tableau et animé (croquis peints réalistes).

**Why:** demande de l'utilisateur (22/11/2026) sur la diapo du tableau des invertébrés de l'Oued Bouregreg (cours TC sortie écologique) : « mieux de créer un tableau au lieu de mettre une photocopie, et de le remplir ».

**How to apply:** à chaque conversion d'un cours de prof (PowerPoint, scans). Voir [[donnees-tabulees-animation-puis-tableau]], [[compter-en-allumant]], [[tableaux-ecran-et-formules]].

## voix-bodi-pour-tout

Toutes les pistes d'un cours (texte des diapositives ET réactions préparées) se font avec la voix Bodi, le modèle le plus récent (`academy-v6-bodi` depuis le 24/11/2026, voir [[modeles-v6-voix-v5-moulsot]] ; avant `academy-v5-bodi`), réglé dans `kaggle_tts_modele` du backend du VPS). Méthode : script sur le VPS qui réveille le kernel d'essai (`scripts.kaggle_tts._reveiller_essai`, env `/etc/moalim/backend.env` chargé) et envoie chaque texte à `/tts` (`langue: ma`, `pas_flow: 10`), deux à la fois. Modèles : `/srv/corpus_v4/cours_bodi/voix_bodi.py` (cours des ondes) et `/srv/corpus_v4/cours_op_bodi/voix_bodi_op.py` (ondes périodiques).

**Why:** demande de l'utilisateur du 10 novembre 2026 (« je veux pas cette voix… la voix de Bodi… tout générer avec ce modèle, c'est le plus récent d'entraînement ») ; l'ancien générateur `gen_kaggle_cours_exemple.py` produit la voix Amine (référence `reference_amine.flac`).

**How to apply:** ne plus lancer `gen_kaggle_cours_exemple.py` pour un cours. Le compte Kaggle n'a que 2 sessions GPU : un kernel déjà lancé occupe une session jusqu'à sa fin, même si on pousse une nouvelle version par-dessus (le statut ne montre que la dernière version) ; « Maximum batch GPU session count of 2 reached » fait lire au réveil un vieux journal (tunnel mort). Voir [[voix-kaggle-a-la-demande]], [[cours-en-mode-concentration]].

## voix-toujours-sans-tunnel

Générer les voix uniquement en lot sans tunnel : `/srv/corpus_v4/voix_lot/lancer_lot.sh N pousser|statut|recuperer`
(kernel `<compte>/academy-tts-lot`, textes embarqués, TTS + vérification MoulSot dans le kernel, WAV en sortie ;
`KERNEL_LOT=academy-tts-lot2` pour un second lot sur le même compte), suivi par `suivre_compte.sh N ETIQ`.
Transcription seule des voix déjà publiées : `stt_seul.py` / `lancer_stt.sh` (sans tunnel aussi).

**Why:** l'utilisateur, 22/11/2026 : « pour la génération des audios ne doit pas faire avec tunnel, il est déjà annulé,
veuillez toujours les mettre sans tunnel » — Kaggle annule les kernels à tunnel cloudflared depuis le 20/11.

**How to apply:** ne jamais lancer `lancer_compte*.sh`, `voix_bodi_lot*.py` ni le kernel d'essai à tunnel pour
générer ; écrire dans tout skill de voix que le lot est sans tunnel. Compte 4 (zahraoui) : annulé par Kaggle en
cours de lot, ne pas compter dessus. Voir [[voix-kaggle-a-la-demande]], [[voix-bodi-pour-tout]].

## tc-voix-noms-fichiers

Voix du tronc commun (`frontend/src/publication/tronc-commun/cours/tc_svt_*_voix.json`) : le MP3 d'une piste est
`/media/audio/courses/<deck>/<type>/<id>.mp3`, où les « : » et « / » de l'id deviennent « __ »
(`rv_s3_histogramme:0` → `rv_s3_histogramme__0.mp3`, `fe_t1_solides/q/0/1` → `fe_t1_solides__q__0__1.mp3`).

**Why:** le 24/11/2026, sans cette conversion, j'ai compté 469 pistes manquantes au lieu de 171 et lancé 3 lots
Kaggle inutiles ; l'utilisateur a corrigé (« ses audios sont déjà générés… il reste seulement une partie de facteurs édaphiques »).

**How to apply:** avant de générer des voix du tronc commun, comparer avec `find /var/www/moalim/media/audio/courses/tc_svt_*`
sur le serveur en appliquant la conversion, et demander à l'utilisateur en cas de doute. Voir [[voix-bodi-pour-tout]].

## agents-avec-opus

Travailler seulement avec Opus : chaque sous-agent lancé avec l'outil Agent reçoit `model: "opus"` (demande du 10 novembre 2026, après le passage de la session à claude-opus-5-5).

**Why:** consigne explicite de l'utilisateur (« veuiller travailler seulement avec opus ») ; les explorations de cours faites avec un autre modèle ont été interrompues et relancées sous Opus.

**How to apply:** ne jamais laisser un agent hériter d'un autre modèle ; un agent déjà lancé avec un autre modèle ne peut pas changer de modèle en cours : l'arrêter et le relancer sous Opus à partir de ses fichiers de travail. Voir [[exploration-avant-chaque-cours]].
