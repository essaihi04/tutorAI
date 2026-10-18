# Ondes mécaniques progressives

Laboratoire local sans dépendance externe, adapté à la fiche pédagogique 2BACSPF-6.

## Accès

`index.html?variant=cord` ouvre le parcours libre. Variantes : `cord`, `spring`, `water`, `sound`, `vacuum`, `superposition`, `medium`, `progressive`.

Ajouter `scope=single` limite la progression à l'expérience choisie, pour l'intégration dans une diapositive. Le menu reste disponible pour comparer les expériences. L'ancien accès `advanced/waves/index.html?variant=progressive` redirige ici. Les expériences de périodicité et d'optique restent dans l'ancien laboratoire.

## Modèles

- Impulsion à support compact, milieu homogène, aucune réflexion.
- Corde : mouvement transversal ; ressort : déplacement longitudinal limité pour éviter le croisement des spires.
- Son dans l'air : modèle longitudinal de petites oscillations, sans émission audio.
- Eau : vue du dessus des fronts ; ce n'est pas une représentation des trajectoires moléculaires.
- Cloche : comparaison qualitative ; jauge sans unité, aucune prétention de mesure acoustique ou de preuve expérimentale.
- Superposition linéaire : somme des déplacements, compensation exacte pour deux impulsions opposées identiques au même centre.
- Milieu : corde idéale, `v = sqrt(T / μ)` ; amplitude sans effet sur la célérité.
- Capteurs : dates des maxima. L'élève saisit τ en secondes et v en m/s. Deux essais corrects à distances différentes et même célérité sont nécessaires. Tolérance de lecture du retard : 2 % + 2 ms ; tolérance du calcul de v : 5 %.

L'état final est conservé. Les paramètres sont bornés ; leur modification annule la validation de l'essai courant. La réponse peut utiliser une virgule décimale. Les mesures validées restent visibles pour la comparaison.

## Intégration tuteur

Identifiant conservé : `physics_waves_advanced_lab`.

Contrat du template de plateforme : émission de `simulation_manifest` et `simulation_state` ; réception de `simulation_control` uniquement depuis la fenêtre parente. Statuts : `idle`, `running`, `paused`, `finished`.

Commandes : `start`, `set_variant`, `set_parameters`, `fire_pulse`, `pause`, `step`, `run_until` (`time_s` : lance si besoin puis s'arrête à cet instant), `set_time` (`time_s` : saute à cet instant, en pause), `record_measurement`, `check`, `reset`, `reveal_hint`. Le manifeste fournit les limites des paramètres ; le snapshot donne `duration_s`.

Le professeur animé de la page localise le bouton d'une commande avant de l'appuyer : la page parente envoie `simulation_locate` (`command`, `parameters`, `sequence`) et le script partagé `media/simulations/professor-locate.js`, chargé par chaque laboratoire, répond `simulation_control_rect` avec le rectangle de l'élément portant `data-professor-control` (sinon identifiants et libellés habituels), ou `null`. Aucun code ou URL fourni par le tuteur n'est exécuté.

Le snapshot rapporte les paramètres, le temps, les actions, la réponse saisie, les tentatives, les mesures validées et les variantes terminées. Les réponses libres du cours restent à examiner par le tuteur ; le laboratoire ne simule pas une correction automatique de rédaction.

## Vérification

- `node --test frontend/tests/waves-model.test.mjs` depuis la racine.
- `python tools/check_waves_browser.py` : Edge installé et Playwright Python nécessaires ; lance un serveur temporaire limité à `frontend/public`, teste les contrôles, les validations, les événements et les formats d'écran, puis ferme le serveur. Captures dans `tmp/waves-check/`.
- `python -m pytest app/tests/test_waves_reference.py app/tests/test_course_player.py` depuis `backend`.

Les contenus ajoutés sont en français. La version du manifeste passe à 2, tout en conservant les anciens identifiants et le statut brouillon. La publication en base et l'éventuelle génération de nouvelles pistes audio sont des opérations séparées.
