# Brief — simulations du cours phys_ch12_etat_equilibre (« État d'équilibre d'un système chimique »)

Travaille depuis /home/user/tutorAI. Messages en français simple. Pas de commit, pas de push, pas de git checkout/stash/reset, pas de sous-agent.
Tu écris UNIQUEMENT les pages qui te sont confiées dans `frontend/public/media/simulations/chimie/etat-equilibre-tableau/` (kit déjà copié :
commun.js, exposants.js, ee.css — ne les modifie pas ; si tu as besoin d'une aide commune, mets-la dans ta page).

À lire d'abord :
1. `.agents/skills/simulations-au-tableau/SKILL.md` (en entier).
2. Le CONTRAT : `outils/cours/notes/cours/etat_equilibre_contrat_simulations.md` (vues, moments, repères EXACTS, données numériques communes).
   Les noms de moments et de repères sont lus par le cours écrit en même temps par d'autres agents : respecte-les à la lettre.
3. Les modèles (lis-les pour l'API, le style, la peinture des béchers et des axes) :
   les pages de `frontend/public/media/simulations/chimie/transformations-deux-sens-tableau/` (avancement.html, conductimetrie.html, dilution.html, equilibre.html, figures.html, bilan.html, carte.html : leur moteur est le bon, il garde la durée la plus longue d'une étape),
   `frontend/public/media/simulations/physics/circuit-rlc-tableau/circuit-lc.html`, et `commun.js` (Tableau, Craie, protocole, repere, play_until, __horsCadre).

Règles : fond transparent, un seul bouton, poignées glissables seulement où le contrat en met, tout dans 760 × 420, rien hors cadre (`__horsCadre` vide),
aucun texte superposé, indices et charges rendus, virgule décimale, aucun mot interdit du contrat. Chaque moment `play_until` doit pouvoir être atteint
et figer la scène ; chaque repère déclaré au plus tard à son moment. `ce_qui_se_voit` en français simple avec les valeurs.
Vérifie les nombres affichés avec python (ils doivent égaler ceux du contrat).

Contrôles obligatoires avant de rendre :
- `node --check` sur le script extrait de chaque page (ex. : python3 extrait le contenu des <script> sans src dans un fichier .js du scratchpad
  /tmp/claude-0/-home-user-tutorAI/97eb67fb-c4da-5d67-a778-c5e9c433802b/scratchpad/sims/ (crée-le), puis node --check).
- Test headless (Playwright pour node, déjà installé : `require('playwright')`, `chromium.launch()` sans option) : serveur
  `python3 -m http.server <port> -d frontend/public` (prends le port qui t'est donné ; arrête-le à la fin), pour CHAQUE vue : chargement sans erreur JS,
  état `simulation_state` reçu (postMessage), chaque moment du contrat joué par `play_until` (commande postMessage
  `{type:'simulation_control', command:'play_until', parameters:{moment}}`), chaque repère du contrat présent (`Tableau.listeReperes()`), `__horsCadre` vide,
  et une capture PNG (deviceScaleFactor 1) dans le scratchpad que tu REGARDES avec l'outil Read (lisibilité, rien de coupé, rien de superposé).
  Modèle de script : `outils/cours/notes/cours/transformations_deux_sens_build/verif_sims.js` (même protocole).
- Efface tes captures à la fin.

Rapport final (court) : pages et vues écrites, moments/repères (conformes ou écarts), poignées, résultats des tests, choix à faire valider.
