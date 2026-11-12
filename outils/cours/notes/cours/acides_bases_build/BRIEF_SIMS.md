# Brief — simulations du cours phys_ch13_acides_bases (« Transformations liées aux réactions acide-base »)

Travaille depuis /home/user/tutorAI. Messages en français simple. Pas de commit, pas de push, pas de git checkout/stash/reset, pas de sous-agent.
Tu écris UNIQUEMENT les pages qui te sont confiées dans `frontend/public/media/simulations/chimie/acides-bases-tableau/` (kit déjà copié :
commun.js, exposants.js, ab.css — ne les modifie pas ; si tu as besoin d'une aide commune, mets-la dans ta page).

Répartition (4 agents, une liste de pages chacun ; port du serveur de test entre parenthèses) :
- agent 1 (port 8951) : `eau.html` (7 vues), `base.html` (4 vues), `carte.html` ;
- agent 2 (port 8952) : `acidite.html` (5 vues), `comparer.html` (7 vues) ;
- agent 3 (port 8953) : `predominance.html` (5 vues), `dosage.html` (6 vues) ;
- agent 4 (port 8954) : `exploiter.html` (6 vues), `figures.html` (5 figures : fig_2025R, fig_2016N, fig_2022R, fig_2022N, fig_2024R), `bilan.html`.

À lire d'abord :
1. `.agents/skills/simulations-au-tableau/SKILL.md` (en entier).
2. Le CONTRAT : `outils/cours/notes/cours/acides_bases_contrat_simulations.md` (vues, moments, repères EXACTS, données numériques communes,
   courbes de dosage déjà calculées). Les noms de moments et de repères sont lus par le cours écrit en même temps par d'autres agents :
   respecte-les à la lettre. Pour figures.html : `outils/cours/notes/cours/acides_bases_build/nationaux.md` § 5 (points relevés) et les figures
   du dépôt (`backend/data/exams/physique/<session>/assets/…png`, à regarder avec Read).
3. Les modèles (lis-les pour l'API, le style, la peinture des béchers et des axes) :
   les pages de `frontend/public/media/simulations/chimie/etat-equilibre-tableau/` (rappel.html, constante.html, conductimetrie.html,
   facteurs.html, figures.html, bilan.html, carte.html : leur moteur est le bon, il garde la durée la plus longue d'une étape — Math.max),
   `chimie/transformations-deux-sens-tableau/avancement.html` (tableau d'avancement), et `commun.js` (Tableau, Craie, protocole, repere,
   play_until, __horsCadre).

Règles : fond transparent, un seul bouton, poignées glissables seulement où le contrat en met (`pH` sur eau?vue=solutions,
predominance?vue=domaines et ?vue=distribution ; `V_B` sur dosage?vue=courbe), tout dans 760 × 420, rien hors cadre (`__horsCadre` vide),
aucun texte superposé, indices et charges rendus, virgule décimale, ⇌ pour une réaction limitée et → pour le dosage, couleurs vraies des
indicateurs (BBT jaune / vert / bleu…), aucun mot interdit du contrat (ligne « Jamais »). Chaque moment `play_until` doit pouvoir être atteint
et figer la scène ; chaque repère déclaré au plus tard à son moment. `ce_qui_se_voit` en français simple avec les valeurs.
Les courbes de dosage et de distribution sont tracées avec les points du contrat (exemples H, J, K, L, M) : le modèle de calcul n'est jamais
écrit à l'écran. Vérifie les nombres affichés avec python (ils doivent égaler ceux du contrat).

Contrôles obligatoires avant de rendre :
- `node --check` sur le script extrait de chaque page (python3 extrait le contenu des <script> sans src dans un fichier .js de TON dossier
  scratchpad (celui que ton système te donne ; crée un sous-dossier `sims/`), puis node --check).
- Test headless (Playwright pour node, déjà installé : `require('playwright')`, `chromium.launch()` sans option) : serveur
  `python3 -m http.server <ton port> -d frontend/public` (arrête-le à la fin), pour CHAQUE vue : chargement sans erreur JS,
  état `simulation_state` reçu (postMessage), chaque moment du contrat joué par `play_until` (commande postMessage
  `{type:'simulation_control', command:'play_until', parameters:{moment}}`), chaque repère du contrat présent (`Tableau.listeReperes()`), `__horsCadre` vide,
  les poignées testées aux deux bouts (`set_parameters`), et une capture PNG (deviceScaleFactor 1) dans ton scratchpad que tu REGARDES avec
  l'outil Read (lisibilité, rien de coupé, rien de superposé).
  Modèle de script : `outils/cours/notes/cours/acides_bases_build/verif_sims.js` (même protocole ; il lit le cours, qui n'existe pas encore :
  écris ton propre petit script à partir de la liste des vues du contrat).
- Efface tes captures à la fin.

Rapport final (court) : pages et vues écrites, moments/repères (conformes ou écarts), poignées, résultats des tests, choix à faire valider.
