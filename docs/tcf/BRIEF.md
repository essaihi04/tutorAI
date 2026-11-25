# Brief commun — cours du Tronc Commun physique-chimie sur /TCF (25/11/2026, sessions cloud)

Projet Moalim (moalim.online) : tuteur IA, cours en JSON joués par un lecteur React en **mode concentration**
(diapos avec une simulation peinte au tableau ~70 % de l'écran, voix darija + français, cahier, questions).
Un nouveau lien libre **/TCF** reçoit trois cours de Tronc Commun Sciences option française (TCSF), physique-chimie.
Tu écris UN de ces cours (voir ta mission). Les deux autres sont écrits en même temps par d'autres agents, dans le même
dossier : ne touche QUE tes fichiers.

## Où (session cloud)

- Dépôt `essaihi04/tutorAI`, branche de travail **`tcf-cours`** (`git fetch origin tcf-cours && git checkout tcf-cours`).
  Ce brief appelle `W` la racine du dépôt. Ne touche QUE tes fichiers (les deux autres cours sont écrits en même temps
  par d'autres sessions cloud sur la même branche). Commite tes fichiers souvent (au moins à chaque grosse étape), puis
  `git fetch origin && git rebase origin/tcf-cours && git push origin HEAD:tcf-cours` ; jamais `--force`, jamais sur
  `main`, aucun déploiement.
  **Les `.json` sont ignorés par `.gitignore`** : ajoute ton cours et sa liste de voix avec `git add -f` (vérifie avec
  `git ls-files frontend/src/publication/tcf/cours` qu'ils sont bien suivis).
- Ton cours : `W/frontend/src/publication/tcf/cours/<id>.json` (CourseDeck, `mode: "concentration"`, `language: "mixed"`,
  `niveau: "tronc_commun_sciences_biof"`, `subject`), et la liste de ses voix `<id>_voix.json` (voir plus bas).
- Tes simulations : le dossier indiqué dans ta mission. **Une partie est déjà commencée** par un premier agent
  (interrompu) : relis-la, garde ce qui est bon, complète et corrige.
- La page /TCF existe (`W/frontend/src/publication/tcf.tsx`, `W/frontend/tcf.html`, `W/frontend/vite.tcf.config.ts`) : ne
  la modifie pas. En local : `cd W/frontend && npm ci` (si besoin) puis `npx vite --config vite.tcf.config.ts --port 5173`
  puis `http://localhost:5173/TCF/tcf.html?cours=<id>` (`&diapo=<slide id>`). En dev, pas de fiche à remplir.

## À lire d'abord (en entier)

1. Skills : `W/.agents/skills/tronc-commun/SKILL.md`, `cours-concentration`, `simulations-au-tableau`, `professeur`
   (toutes ses règles numérotées), `logique-de-cours`, `cahier-de-l-eleve`, `voix-du-cours` (§ 1 et 2), `prononciation`,
   `suivi-des-acquis`.
2. Les règles de l'utilisateur : `W/docs/tcf/REGLES_UTILISATEUR.md` (copie de la mémoire du projet).
3. Le modèle (même structure, même qualité) : `W/frontend/src/publication/tronc-commun/cours/tc_svt_sortie_ecologique.json`
   (+ `_voix.json`), ses simulations `W/frontend/public/media/simulations/svt/tc_sortie_ecologique-tableau/`, le kit
   `W/frontend/public/media/simulations/shared/tableau/` ; pour le style peint en physique-chimie, `physics/ondes-tableau/`
   et `chimie/*-tableau/`.
4. Le contenu du livre de référence, résumé : `W/docs/tcf/CONTENU_LIVRE.md` (le livre n'est pas dans le dépôt).
   **Aucune image du livre** : chaque figure, expérience, montage ou schéma est recréé en animation peinte (couleur,
   réaliste, verrerie avec reflets, liquide visible — jamais deux traits de craie).
5. **Consigne de l'utilisateur** : « même si vous ne trouvez pas de simulation, créez-les vous-mêmes et animez le cours
   avec des animations du mouvement » → chaque diapo a sa propre simulation créée par toi, avec du vrai mouvement
   synchronisé à la voix ; aucune image fixe, aucune simulation empruntée faute de mieux.

## Exigences de l'utilisateur (non négociables)

- **Toutes les méthodes du chapitre**, expliquées simplement **en partant de zéro** (prérequis enseignés dans des diapos
  de rappel, chaque notion nouvelle expliquée deux fois de deux façons, une idée par diapo) ; chaque méthode montrée
  lentement sur un exemple par le tuteur, puis refaite par l'élève sur un autre (question au tableau avec démonstration).
- **Animations réalistes** : chaque diapo a sa simulation peinte (iframe 760×420, fond transparent, kit `shared/tableau`
  + un `commun.js` du cours), avec des `moments` nommés, `play_until`, `set_parameters`, `highlight`, `repere` sur chaque
  élément que la voix nomme, `ce_qui_se_voit`. Données tabulées : d'abord produites par l'animation, puis les nombres
  volent dans le tableau. Compter = allumer un à un avec le numéro.
- **Voix, tableau et animation synchronisés** : ce qui est dit est montré ET écrit au même instant — `concentration.pointage`
  (`play_until` / `repere` sur les mots exacts du texte parlé), `concentration.centre` (formules écrites sur leur mot),
  la simulation qui écrit ses étiquettes et ses calculs à la craie au moment où la voix les dit. Chaque `mot` est un
  extrait exact de `speech_text.mixed`.
- **Nombres simples** (règle 1 du skill tronc-commun) : choisis des données qui donnent des résultats entiers ou une
  décimale simple ; garde la méthode du livre.
- **Téléphone en paysage** : chaque vue lisible dans un cadre de 429×250 (étape en cours seule, texte ≥ 15 px) et belle
  à 760×420 / 1100×560.
- Voix : darija simple + français pour les termes du programme, les nombres, les unités et les formules dites en mots
  (« vingt-deux », « v égale d sur delta t ») ; jamais un nombre en chiffres ni un symbole dans `speech_text` ; jamais un
  nombre français collé à un mot darija mal choisi (mémoire nombres-jamais-colles…) ; « الحرارة » et pas « السخانة » ;
  phrases françaises de plus de dix mots coupées par des virgules. Mots rares : vérifie-les avec
  `python -X utf8 W/scripts/voix/verifier_mots.py` (lis son en-tête pour l'usage ; s'il ne lit que `backend/data/courses`,
  adapte l'appel ou fais la même vérification avec `W/backend/data/voix/frequences_corpus_v4.json`) et préfère les
  mots fréquents du corpus. Liste les mots douteux dans ton rapport (l'utilisateur les écoutera).
- Structure (comme le modèle SVT) : diapo d'ouverture `<préfixe>_ouverture_cours` et de fermeture
  `<préfixe>_fermeture_cours` (cours-concentration 9d, adaptées au Tronc Commun : pas de pourcentage du national ;
  « l'évaluation / le contrôle » à la place), `competences` (6-10, 3-4 `rappels` chacune), `seances` → `blocs` de 3-4
  diapos avec leurs lignes de `cahier` (général et organisé, jamais les données d'un exercice, `cahier_figures` quand la
  notion se dessine), UNE question « À toi » par bloc (QCM / vrai-faux / libre, `correct`, démonstration pour tout calcul),
  réactions préparées pour chaque option (`concentration.reponses[cle][option]` = `juste` ou `1`/`2`, chacun
  `{parole, ecrit}`), 0-2 `observation` dans le cours, bilan « Ce qu'il faut retenir » (`bilan.html`) + carte du chapitre
  (`carte.html`) avec imprimer, fermeture.
- Pas d'`audio` dans le JSON (les voix seront générées ensuite à partir de `<id>_voix.json`).

## La liste des voix `<id>_voix.json`

Même format et mêmes conventions d'`id` que `tc_svt_sortie_ecologique_voix.json` :
`{"deck": "<id>", "voix": "academy-v6-bodi (par lot)", "pistes": [{"type", "id", "texte"}]}` avec les types que sait poser
`W/scripts/brancher_voix_edaph.py` (lis-le : diapo, enonce, demonstration, reaction, observation_*, rappel_enonce,
rappel_reaction, bloc_*). Chaque `texte` est EXACTEMENT le texte parlé du champ correspondant du cours (le script compare
les textes). Lance `python -X utf8 W/scripts/tcf/lister_voix_tcf.py <cours.json>` à la fin : il écrit `<id>_voix.json` (mets les textes parlés aux mêmes champs que le modèle SVT).

## Vérifier avant de rendre

- `python -I W/scripts/verifier_formules.py <cours.json>` (et sur ton dossier de simulations) : rien.
- `python -I W/backend/scripts/verifier_parcours.py <cours.json>` : rien.
- `python -I W/scripts/verifier_pointage.py …` et `python W/backend/scripts/verifier_figures_cahier.py <cours.json>` si
  applicables (lis leurs en-têtes) : 0 erreur ; chaque `mot` trouvé dans le texte.
- Chaque simulation : captures avec Playwright (Python ou Node ; installe-le si besoin) de chaque vue et de chaque moment, à 760×420 et à 429×250 ; regarde-les avec Read ; corrige ce qui
  déborde, se chevauche, est illisible ou pas réaliste. Aucune erreur dans la console.
- Le cours joué dans la page /TCF (Playwright sur ton serveur Vite) : il se charge, chaque diapo affiche sa simulation,
  pas d'erreur console. Captures de quelques diapos à 1280×720 et en téléphone paysage 724×350.

## Rapport final (court)

Fichiers créés ; nombre de diapos, blocs, compétences, questions, pistes de voix ; méthodes couvertes ; ce qui a été
vérifié (et comment) ; ce qui reste douteux (mots pour la voix, points de science, vues imparfaites), le SHA du dernier commit poussé sur `tcf-cours`. Écris aussi ce rapport dans `W/docs/tcf/RAPPORT_<id>.md` (commité).
