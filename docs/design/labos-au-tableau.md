# Laboratoires dessinés au tableau

Depuis le 24 octobre 2026, tous les laboratoires de `frontend/public/media/simulations` sont dessinés comme le tableau du cours : fond vert sombre quadrillé, écriture à la craie (Patrick Hand, palette de `LiveBoard`), schémas tracés à main levée, et surtout **écrits en direct** — chaque trait se trace, chaque texte s'écrit lettre par lettre, comme un professeur qui fait un live. Référence visuelle : l'onde progressive avec les capteurs A et B, le retard τ, la distance AB et la célérité v (`physics/progressive`).

## Le kit `shared/tableau`

- `tableau.css` : fond, police, boutons à la craie (`.craie-btn`, cadre tracé à main levée), onglets soulignés (`.onglet`), saisies pointillées (`.craie-champ`), choix (`.choix`), curseurs (`.curseur`), panneaux posés sur la scène (`.panneau.haut-droite` …), bulle de retour (`.bulle`), caret d'écriture (`.en-cours`).
- `tableau.js` (`window.Tableau`) :
  - `Craie` : `debut(graine, temps)`, `trait`, `ligne`, `fleche`, `cote`, `rect`, `cercle`, `courbe`, `point`, `texte`, `axe`, `direct(fn)`, `depuis(t)`, `pause(s)`, `fin()`. Le tremblement est déterministe (graine) ; le temps fait avancer l'écriture, `direct` dessine d'un coup les parties animées, `depuis` fait écrire plus tard ce qui apparaît plus tard, `fin()` dessine le bout de craie et dit si tout est écrit.
  - `ecrire(el, texte)` / `bulle(el, texte, kind)` : texte HTML écrit lettre par lettre.
  - `protocole({id, commandes, config, texte, etat, progression, executer})` : manifeste, état, `executeAICommand`, écoute de `simulation_control` ; le bouton `data-professor-control` de la commande clignote (`appuyer`) quand elle arrive — le professeur animé vient d'appuyer dessus.
  - `boutons`, `onglets` (data-variant), `curseur`, `glisser` (poignées déplaçables sur le dessin), `fr`, `nombre`.

## Règles

1. Peu de boutons : un principal, Recommencer, Vérifier dans le panneau de réponse, Un indice. Les réglages se font d'abord sur le dessin (capteur que l'on glisse, interrupteur que l'on bascule), sinon par un curseur à la craie.
2. Chaque contrôle garde `data-professor-control="cmd1 cmd2"` et la page charge `/media/simulations/professor-locate.js` : le professeur localise le bouton, vole jusqu'à lui et appuie.
3. Le pont tuteur ne change pas : mêmes `simulation_id`, commandes, paramètres, état (`backend/app/tests/test_course_player.py` vérifie les chaînes du protocole).
4. Tout tient dans l'iframe sans défilement ; `MediaViewer` affiche chaque laboratoire du site à sa taille réelle, sur fond transparent.
5. Les modèles (`model.js`) restent séparés et testés (`frontend/tests/*.test.mjs`).

## Écrire un nouveau laboratoire

Partir de `TEMPLATE_TABLEAU.html` (et non du gabarit blanc `TEMPLATE_SIMULATION.html`) : la boucle de rendu appelle `craie.debut(7, (performance.now() - ouvert) / 1000)`, dessine les parties fixes, puis `craie.direct(() => …)` pour l'animation, et redemande une image tant que `craie.fin()` renvoie faux ou que la scène bouge.

## Le professeur montre la simulation du doigt (25 octobre 2026)

- **Repères pointables** : pendant le dessin, `craie.repere(id, x, y, w, h, libellé)` enregistre un rectangle (en px de la page) ; un panneau HTML se déclare avec `data-professor-point="id"` et `data-professor-label`. `Tableau.rectRepere(id)` les retrouve, `Tableau.listeReperes()` les énumère.
- **Pointage** : la commande `highlight {target: id}` (aussi `point`, `montrer`) ne presse rien. `professor-locate.js` répond `mode: 'point'` avec le rectangle du repère ; le professeur entre dans la simulation, montre le repère du doigt pendant `PROFESSOR_POINT_HOLD_MS` et la commande part aussitôt : le kit entoure le repère à la craie (`Tableau.surligner`, `.repere-anneau`). Un appui (`start`, `fire_pulse`…) garde le comportement précédent (vol, appui, puis commande).
- **Script d'explication** : `Tableau.explication({ variante: [{ repere, texte }, …] })` part dans le manifeste (`capabilities.explication`, avec `capabilities.reperes`). Le serveur (`backend/app/services/simulation_explication.py`) l'injecte dans le prompt : le tuteur dit chaque phrase et envoie le pointage du repère ; il peut relancer la simulation lui-même (`fire_pulse` ou `start`) quand l'élève ne comprend pas.
- **Réactions aux réponses** : une vérification dans le labo (`check` → `correct`) fait lever les bras du professeur ou dire non de la tête (`MediaViewer` → `signalerReponseEleve`) ; le jugement `<eval>` du tuteur arrive au personnage par `professor_reaction` ; côté serveur, une vérification fausse donne un indice en pointant le repère manquant, puis, à la deuxième, une relance de la simulation et une ré-explication autrement (`decider_reaction`, `prompt_reexplication`).
