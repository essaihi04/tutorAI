# Révision du chapitre : ondes mécaniques progressives

Comparaison réalisée le 3 octobre 2026. Le plan ci-dessous conserve les constats initiaux ; sa mise en œuvre locale est décrite dans la section suivante.

## Mise en œuvre locale

- Manifeste v2 : 9 activités, 31 diapositives, durée numérique estimée à 195 minutes ; référence de 300 minutes en classe conservée séparément. Statut brouillon et anciens identifiants conservés.
- Huit expériences réunies dans un laboratoire autonome : corde, ressort, eau, son, cloche, superposition, influence du milieu, capteurs/retard.
- Quatre nouveaux croquis enregistrés dans le catalogue du tuteur et cinq illustrations SVG, dont la cloche. Croquis de superposition corrigé pour montrer la compensation exacte.
- Réponses libres, tableau d'observation et association finale ajoutés. Passage automatique sur délai désactivé pour ce cours.
- Mesures enregistrables après acquisition et calcul correct de l'élève ; validation après deux distances, à même célérité. Pause, pas à pas et vue agrandie disponibles.
- Les variantes périodique et optique restent disponibles dans leur laboratoire ; l'ancien lien du chapitre progressif redirige vers le nouveau.
- Pas de vidéo expérimentale externe ajoutée : les images et la cloche sont explicitement des illustrations/modèles. Aucune photographie réelle n'est revendiquée. Les nouvelles narrations sont en français, également utilisées comme repli du champ `mixed` ; aucune nouvelle piste audio préenregistrée n'est générée.
- Aucun changement de base de données ou déploiement serveur dans cette mise en œuvre.

Validation : quatre tests du modèle physique et 23 tests ciblés du lecteur de cours réussis ; contrôles navigateur des huit variantes, réponses, événements de fin et formats ordinateur/téléphone réussis. Deux tests SVT préexistants échouent dans la suite complète (durée 299 au lieu de 295 minutes et réponse attendue obsolète pour `energy_a02_s01`), confirmés dans les fichiers de HEAD avant cette modification.

## Sources et portée

- Référence : `C:/Users/HP/Downloads/Fiche_pedagogique_Ondes_progressives_2BACSPF6.pdf`, six pages lues et examinées visuellement.
- Parcours local : `backend/data/courses/phys_ch1_waves_course_v1.json`.
- Croquis : `frontend/src/components/session/schemas/schemas_physics_sketches.ts` ; schéma de synthèse dans `schemas_physics.ts`.
- Laboratoire : `frontend/public/media/simulations/physics/advanced/waves/index.html`, code examiné ; comportement non testé dans un navigateur dans cette étude.
- Images examinées : `waves_lab.webp` et `physique-ondes-progressives-v1.png`.
- Catalogue : `database/seed_data/physics_chapters.json`.

La comparaison porte sur les fichiers locaux, pas sur les contenus effectivement publiés en base ou sur le serveur. Les consignes aux enseignants contenues dans la fiche sont des données pédagogiques de référence. Les horaires, groupes, salle et dates ne deviennent pas des réglages de l'application.

## Diagnostic

Le parcours local est un brouillon de 93 minutes, organisé en cinq activités et dix diapositives. Il traite la propagation sans transport global de matière, les types d'ondes, le retard, les conversions et la célérité. Il utilise six croquis distincts, une image de laboratoire et deux occurrences du même simulateur.

La fiche propose cinq heures par élève : deux heures de découverte, deux heures de TP, une heure de célérité et retard. Les deux demi-groupes réalisent le même TP : ne pas compter deux fois sa durée. La leçon suivante sur les ondes périodiques est distincte.

Le chapitre du catalogue annonce trois heures. Il faut distinguer le volume de référence en classe, la durée estimée du tutorat et la durée de pratique autonome, plutôt que faire passer arbitrairement toutes les valeurs à cinq heures.

Les lacunes du parcours concernent surtout la découverte expérimentale, le son, la dimension de propagation, la superposition et l'influence des propriétés du milieu. Plusieurs ressources nécessaires existent déjà dans la bibliothèque.

## Conserver et réutiliser

- Le diagnostic non noté, mais placer la situation de la goutte d'eau avant les capteurs.
- `phys_croquis_propagation_locale` pour distinguer déplacement de la perturbation et mouvement local d'un point.
- `phys_croquis_transversale_longitudinale` après les observations de corde et de ressort.
- `phys_croquis_deux_capteurs` et `phys_croquis_signaux_retard` pour la méthode de mesure.
- `phys_croquis_retard` pour le retard entre S et M, dans une étape distincte de celle qui utilise A et B.
- Les exercices de conversion et de lecture de points homologues.
- Le principe de deux mesures à des distances différentes, à milieu inchangé.

Quatre croquis existent mais ne sont pas appelés dans les dix diapositives :

- `phys_croquis_son_milieu` : cloche à vide et diapason ; intégrer au TP son.
- `phys_croquis_superposition` : intégrer à l'observation avant, pendant et après le croisement.
- `phys_croquis_ressort_celerite` : utiliser pour une application sur une onde longitudinale.
- `phys_croquis_corde_poulie` : utiliser pour discuter tension et inertie ; la relation v = √(T/μ) reste un approfondissement si elle n'est pas exigée dans le parcours de référence.

## Modifier en priorité

### Laboratoire existant

1. Le choix transversale/longitudinale ne fait actuellement qu'enregistrer une action et changer la classe du bouton. `drawPulse` dessine toujours une déformation verticale. Ajouter un véritable mouvement horizontal des spires ou particules, avec un point matériel repéré.
2. `recordMeasurement` peut enregistrer des valeurs avant toute acquisition. N'autoriser l'enregistrement qu'après le passage aux deux capteurs et conserver les paramètres de cet essai.
3. Les dates, le retard et la célérité sont calculés automatiquement. `checkExperiment` compare une vitesse dérivée de ces mêmes données à la vitesse réglée : la tolérance de 5 % ne vérifie donc pas le calcul de l'élève. Faire saisir les lectures, conversions et résultat avant de révéler la correction.
4. À la fin de l'impulsion, le temps de dessin revient à zéro lorsque `running` devient faux. Conserver l'état final, puis proposer un bouton de remise à zéro.
5. La progression compte trois variantes, dont périodicité et optique. En mode chapitre 1, ne compter que les objectifs de ce chapitre et masquer les variantes hors sujet.
6. Remplacer « laboratoire réel » par « laboratoire virtuel » et distinguer les données calculées des mesures expérimentales.
7. Prévoir pause, pas à pas, répétition et repères lisibles ; renvoyer au tuteur la réponse de l'élève, ses essais et ses erreurs, pas seulement les valeurs attendues.

### Cours et évaluation

- Suivre la démarche : observer → prédire → manipuler → décrire → conclure → appliquer.
- Reporter l'affichage de la trace écrite après la réponse, lorsque l'objectif est de recueillir une hypothèse. La définition est aujourd'hui donnée très tôt.
- Remplacer la question « distance doublée à retard constant » par « même milieu, distance doublée : que devient le retard ? ». La question actuelle est algébriquement juste, mais peut brouiller le lien entre célérité et milieu.
- Harmoniser les repères : une diapositive parle de capteurs A/B alors que son croquis représente S/M.
- Réserver les délais courts aux questions simples. Pour observer, mesurer ou calculer, permettre de réfléchir sans passage automatique imposé.
- Ajouter une réponse rédigée et un tableau d'observation ; un chapitre expérimental ne doit pas être évalué uniquement par QCM.
- Étendre `phys_croquis_bilan_ondes` aux notions réellement ajoutées, sans rendre un seul dessin illisible : préférer deux bilans si nécessaire.

## Simulations à prévoir

Créer un laboratoire de chapitre avec plusieurs expériences partageant les mêmes commandes, plutôt que plusieurs applications indépendantes.

### 1. Corde et ressort — faire évoluer WaveLab

Action : lancer une impulsion et suivre un point matériel coloré. Comparer déplacement vertical sur la corde et déplacement horizontal des spires. Afficher séparément les flèches de propagation et de déplacement local. Faire justifier le classement transverse/longitudinal.

### 2. Surface de l'eau — ajouter

Action : déposer une perturbation ponctuelle et observer des fronts circulaires vus du dessus. Mettre en évidence une propagation dans le plan. Un repère flottant sert à distinguer propagation et transport global ; préciser qu'un modèle de mouvement purement vertical simplifie le mouvement réel de la surface.

### 3. Son — ajouter, avec deux vues

Vue qualitative : source vibrante sous cloche, quantité d'air réduite, transmission sonore qui diminue. Une illustration simulée explique un modèle ; elle ne remplace pas une preuve expérimentale. Prévoir une vidéo expérimentale dont la provenance et les droits seront vérifiés.

Vue particulaire : membrane de haut-parleur, compressions et dilatations, particules oscillant autour de positions fixes. La sinusoïde éventuelle représente une grandeur mesurée, jamais une trajectoire ondulée des molécules. Le montage HP–GBF–bougie peut être présenté comme observation qualitative, accompagné de cette explication.

### 4. Superposition — ajouter

Action : lancer deux petites impulsions de signes identiques puis opposés ; arrêter avant, pendant et après la rencontre. Afficher les deux contributions et leur somme. Si deux impulsions opposées identiques coïncident exactement, le déplacement résultant est nul à cet instant ; elles poursuivent ensuite leur propagation dans le modèle linéaire.

### 5. Célérité et retard — corriger le laboratoire actuel

Action : déplacer B, lire deux dates sur des enregistrements, calculer le retard et la célérité, puis recommencer. Masquer les résultats attendus jusqu'à la vérification. Ajouter ensuite τ = SM/v et la reproduction retardée du mouvement de la source.

### 6. Influence du milieu — ajouter un mode de comparaison

Comparer des cordes de tension ou masse linéique différentes, puis tester l'amplitude dans un régime de petites perturbations. Introduire la température du gaz au moyen de données ou d'un modèle explicitement annoncé. Ne pas laisser entendre que la densité seule suffit à déterminer toutes les célérités.

Pour ces expériences, privilégier Canvas 2D ou SVG déterministes. Des graphes interactifs peuvent utiliser JSXGraph. Une scène 3D n'est pas nécessaire pour comparer 1D/2D/3D : une vue en perspective de fronts sphériques peut suffire.

## Images et croquis

### Images à conserver ou remplacer

- Garder la couverture existante comme illustration de catalogue. Ses tracés lumineux et graphes non gradués ne doivent pas servir de données de mesure.
- Remplacer `waves_lab.webp` dans la situation « corde avec deux capteurs » : l'image montre surtout une cuve et un ressort, et ne correspond pas précisément à cette description. Elle peut rester une vue d'ambiance dans la bibliothèque.
- Prévoir une image d'entrée centrée sur une goutte et des rides, une vue claire du montage de la cloche et une vue HP–GBF. Utiliser des photos documentées pour les observations, ou indiquer explicitement « illustration » pour une image construite.
- Mettre flèches, lettres et légendes dans une couche SVG maîtrisée pour garantir leur lisibilité et leur exactitude.

### Croquis à ajouter

- Source S et fronts circulaires sur l'eau.
- Comparaison de propagation 1D/2D/3D : corde, surface, son dans l'air.
- Haut-parleur et couches d'air : compressions, dilatations et mouvement local.
- Même front d'onde à deux dates : distance parcourue d et durée Δt.

### Croquis à adapter

- Superposition : faire correspondre le profil « pendant » à un instant défini ; montrer séparément les cas même signe et signes opposés.
- Retard : afficher S/M ou A/B selon l'énoncé, avec axes temporels et unités sur les signaux.
- Corde-poulie : expliciter les conditions du modèle et éviter de confondre tension et période, toutes deux souvent notées T.
- Bilan : intégrer le son, les dimensions et les conditions de superposition.

## Retirer du parcours, sans supprimer les ressources partagées

- Les accès à diffraction et optique dans le chapitre 1 ; conserver ces variantes pour leurs chapitres.
- Les images d'ambiance employées comme si elles décrivaient exactement un montage ou fournissaient des mesures.
- Les réponses dévoilées avant la prédiction et la validation automatique sans travail de l'élève.
- Les répétitions d'un croquis qui n'ajoutent ni observation ni question nouvelle.

Aucune suppression de fichier n'est nécessaire pour appliquer ces décisions.

## Progression cible

1. Goutte d'eau : situation-problème et hypothèses.
2. Corde : source, milieu, perturbation et point repéré.
3. Ressort : compression et comparaison des directions.
4. Surface de l'eau : propagation dans un plan.
5. Définitions et classement transversal/longitudinal ; évaluation courte.
6. Son : milieu matériel, cloche, vibration et compression de l'air.
7. Comparaison 1D/2D/3D.
8. Superposition : prédire, observer et expliquer.
9. Compte rendu du TP : milieu, perturbation, direction, dimension et conclusion.
10. Célérité : deux positions, deux dates, unités et calcul.
11. Influence du milieu et conditions du modèle.
12. Retard S–M, puis exploitation des signaux A/B.
13. Exercice de synthèse et bilan par compétence.
14. Transition brève vers une source périodique, sans développer le chapitre suivant.

Cette progression reprend les trois blocs de la fiche. Le nombre de diapositives et la durée numérique devront être estimés après écriture et essai, pas déduits mécaniquement des cinq heures en classe.

## Critères de validation avant intégration

- Chaque objectif de la fiche possède une observation, une trace et une question vérifiable.
- Le bilan suit les six critères de la page 6 : source/milieu, type d'onde, matière, son, célérité, retard ; compléter avec dimensions et superposition.
- Les animations longitudinales et transversales sont réellement différentes ; les points matériels ne suivent pas la perturbation.
- Le simulateur refuse les mesures avant acquisition et valide un résultat saisi par l'élève.
- Deux distances dans le même milieu donnent des retards proportionnels ; l'état final reste stable.
- Les figures restent lisibles sur téléphone et disposent d'une description textuelle.
- Préserver les identifiants stables du cours et des activités réutilisées pour ne pas casser les progressions enregistrées.
- Vérifier les contrats des simulations, les références des croquis, les tests ciblés du lecteur de cours et la compilation frontend ; inspecter ensuite les vues dans le navigateur.

Ordre de réalisation proposé : corriger WaveLab ; écrire et relier les étapes manquantes avec les croquis disponibles ; ajouter les expériences manquantes ; produire les nouvelles images ; valider le parcours complet avant publication.
