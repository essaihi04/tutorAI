# Brief des agents « cours de maths » (10 novembre 2026)

Tu construis UN cours de mathématiques complet (2ᵉ Bac Sciences Physiques BIOF, Maroc) en mode concentration, au niveau du
cours témoin de physique. Tout est déjà décidé dans l'exploration de ton chapitre ; tu la suis.

## À lire d'abord (dans cet ordre)
1. `outils\cours\notes\cours\BRIEF.md`
   (brief commun : méthode, interdits — AUCUNE voix, aucun commit/push/stash/reset/checkout, ne pas toucher frontend/src ni
   backend/app, ni les cours/simulations des autres matières, ni le cours témoin ; pas de fichiers d'identifiants).
2. Les skills du dépôt `.agents\skills\` : cours-concentration, simulations-au-tableau,
   voix-du-cours (sections 1, 2 et 6 seulement : PAS de génération), professeur (règles 10, 14, 17, 18, 20–23), suivi-des-acquis.
3. Le cours témoin `backend/data/courses/phys_ch2_ondes_periodiques.json` (regarde 3–4 diapositives entières : screen_content,
   speech_text.fr/mixed, question + correct + demonstration, exercises, concentration {demarrer, centre, pointage, cahier, variante},
   bilan op_b1_bilan et carte op_b2_carte) et `frontend/public/media/simulations/physics/ondes-periodiques-tableau/bilan.html`, `carte.html`.
4. TON exploration `backend/data/curriculum/exploration/<clé>.json` : plan (compétences + diapositives dans l'ordre), cadre,
   notions_complexes (marches), visuels, redaction_nationale, cas_types, pieges, erreurs_examen, a_ne_pas_dire,
   exclus_hors_programme, questions_eleves, commentaires_eleves, cours_existant, decisions_utilisateur.

## Le kit maths (déjà écrit, à utiliser tel quel — ne le modifie pas ; s'il te manque une fonction, ajoute-la dans ta page)
- `frontend/public/media/simulations/maths/commun/maths-tableau.js` : lis son en-tête. `MathsTableau.page({id, titre, texte, vues})` ;
  chaque vue : `titre`, `dessiner(c, K)` (écriture pas à pas, `K.marque('moment')`, `K.anime(durée, p => …)`, `K.axes`, `K.courbe`,
  `K.courbePart`, `K.proj`, `K.rond`, `K.lignes`, `K.titre`, `K.grille`), `decrire` (moment → phrase de ce qui se voit),
  `params` + `poignees` (l'élève glisse un point), `lecture`, `explication`. Le kit gère le bouton unique, play_until, set_time,
  set_parameters, highlight, ce_qui_se_voit, moments, derniere_main.
- `maths/commun/maths.css`, `maths/commun/exposants.js` (exposants « x² », « 10⁻³ » bien écrits à la craie).
- MODÈLE de page : `frontend/public/media/simulations/maths/limites-continuite-tableau/traversee.html` (TVI, six vues). Copie sa forme.
- Le bilan et la carte : copie `physics/ondes-periodiques-tableau/bilan.html` et `carte.html` dans ton dossier, change les blocs/
  branches, les titres, les textes, et remplace `<script src="commun.js">` par `/media/simulations/maths/commun/maths-tableau.js`
  (il fournit `window.OndesTableau.Scene`) et `ondes.css` par `/media/simulations/maths/commun/maths.css`.
- Tes pages vont dans `frontend/public/media/simulations/maths/<dossier>-tableau/` (dossier donné plus bas). Une page par grande
  construction (approche d'une limite, raccord de deux branches, projections, miroir y = x, tangente, tableau de variations,
  escalier d'une suite…) avec plusieurs vues ; et une page `calculs.html?vue=<id>` pour les calculs écrits à la main au tableau
  (lignes qui s'écrivent l'une après l'autre avec des moments, des mots entourés, des flèches) — c'est le « v_tableaux » des explorations.
- Règles : fond transparent, tout dans 760 × 420, rien sous la barre du lecteur en bas (garde ~60 px libres en bas), apostrophe
  typographique ’ dans les chaînes JS, texte au tableau en français, indices jamais avec « _ » visible (le kit rend `u_n`, `x_0`),
  seulement le programme (cadre). Chaque moment que la voix décrit est un moment nommé de la vue.

## Outils (dossier `cours\maths_build\`, à côté de ce brief)
- `outils.py` : fonctions S (diapositive), Q (question + correct + demonstration), DEMO(parole, [(texte, mot)]), EX, VF, PU (pointage
  play_until), R (repère), C (cible centre:N / visuel), vis(page, caption, alt) — `vis("limites-continuite-tableau/traversee.html?vue=une", …)`.
  S vérifie que chaque `mot` est un extrait exact du texte dit. `build_modele.py` (exemple de build complet du cours de physique :
  activités, compétences avec slide_ids/cadre_ids/dit, deck, option --garder-reponses), `cadre_modele.py` (ajout d'UNE clé
  dans cadre_reference_2bac_pc.json : relit, ajoute, réécrit aussitôt), `prog_modele.py` (statut dans programme_semestre1.json),
  `verif_sims_modele.py` (vérifie en headless que chaque moment/repère cité par le cours existe dans la simulation).
- Fais TON dossier `cours\maths_build\<clé>\` : copie outils.py, écris tes p1.py…pN.py (contenu), build.py, cadre.py, prog.py, verif_sims.py.
  Ne modifie jamais le JSON du cours à la main : on le régénère depuis les p*.py.
- `check_js.py <pages…>` : node --check de chaque script inline. `test_page.py [--shot dossier] <url…>` : headless (Chrome +
  Playwright) — joue chaque moment, donne encre, repères, ce_qui_se_voit, erreurs, textes hors cadre, capture. Il faut un serveur
  statique : `python -m http.server 8898 -d frontend/public --bind 127.0.0.1` (s'il ne répond pas
  sur 8898, lance-le en arrière-plan). Regarde les captures avec Read (fond blanc à la capture = transparent dans le lecteur).

## Le cours
- Fichier `backend/data/courses/<id>.json`, `"status": "draft"`, `"mode": "concentration"`, `stable_id` = id, `lesson_match`,
  `catalog`, `note`, `activities` (une par bloc du plan), `competences` [{id, label, slide_ids, cadre_ids, dit}] (6–10).
- Chaque diapositive : title + lead clairs (le classifieur de questions les lit), bullets, student_trace, visual (simulation à la
  craie : tout ce qui se construit ou bouge ; une seule idée par diapositive), speech_text.fr ET speech_text.mixed (darija simple,
  règles voix-du-cours : termes du programme en français, nombres et formules dits en français en toutes lettres, aucun chiffre ni
  symbole, pas de tachkil, phrases françaises de plus de dix mots coupées par des virgules ; la voix dit d'abord ce que montre la
  construction et où regarder), question (QCM, options mélangées, `correct`), exercices, concentration complète.
- **Démonstrations manuscrites (centrales en maths)** : toute question ou exercice qui demande de calculer, montrer, justifier,
  résoudre, déterminer porte `demonstration {parole, lignes:[{texte, mot}]}` : les lignes écrites comme le barème (redaction_nationale
  de l'exploration : « Posons… », « f est continue sur… », « d'après le TVI… », « donc… »), chaque `mot` extrait exact de `parole`.
- Les formules au centre (`concentration.centre`) apparaissent quand la voix les dit ; `pointage` : chaque phase décrite →
  play_until sur le moment nommé ; repères montrés ; `variante` quand un paramètre se glisse (set_parameters + play_until + highlight).
- Lis les formules dans la voix comme le cadre les dit (`dit`) : « la limite de f de x, quand x tend vers a, égale f de a ».
- Fin du cours : « Ce qu'il faut retenir » (bilan.html, concentration.acquis: true, un bloc par partie, play_until par bloc) et
  « La carte du chapitre » (carte.html), comme le témoin.
- Nomme les fichiers audio ? NON : pas de champ audio (la session principale fera les voix).

## Cadre, réactions, vérifications
- Cadre : la fiche de ton exploration (`cadre`) → `cadre_reference_2bac_pc.json` clé `chapitres.<clé>` par un petit script qui relit,
  ajoute ta seule clé, réécrit aussitôt (indent 2, ensure_ascii=False). Puis
  `python outils/cours/voxtts/controler_cadre.py <cours.json> <clé>` → « cadre : OK » (les « à relire » ne bloquent
  pas, mais relis-les). Un mot de `hors_cadre.mots` ne doit apparaître NI à l'écrit NI dans la voix.
- `python outils/cours/voxtts/verifier_texte_corpus.py <cours.json>` : remplace les mots rares non programme.
- Réactions préparées (texte seulement) : `python outils/cours/voxtts/preparer_reponses.py items <cours.json> <items.json>`,
  puis sur le VPS (`ssh moalim-vps`) : `mkdir -p /tmp/gen_rep_<clé>` ; copie-y `backend/app/services/simulation_reaction.py`,
  `backend/app/services/reponse_eleve.py` (dans reponse_eleve.py remplace « from app.services.simulation_reaction import » par
  « from simulation_reaction import »), `outils/cours/voxtts/gen_reponses_vps.py` (remplace « professeur de physique »
  par « professeur de mathématiques » dans TA copie) et items.json ; puis
  `cd /opt/moalim/backend && set -a && . /etc/moalim/backend.env && set +a && .venv/bin/python /tmp/gen_rep_<clé>/gen_reponses_vps.py /tmp/gen_rep_<clé>/items.json /tmp/gen_rep_<clé>/sortie.json`
  (ne jamais afficher l'environnement), rapatrie sortie.json, `preparer_reponses.py poser <cours.json> <sortie.json> <pistes.json>`,
  relis quelques paroles (pas de chiffres, pas de symboles), nettoie /tmp/gen_rep_<clé> sur le VPS. Ensuite tes rebuilds se font
  avec `--garder-reponses`.
- Vérifs finales : check_js.py sur toutes tes pages ; test_page.py sur chaque vue utilisée ; verif_sims (moments/repères du cours
  présents) ; controler_cadre OK ; `preparer_reponses.py verifier <cours.json>` ne doit signaler QUE « pas de piste audio » /
  « voix manquante ».
- programme_semestre1.json : ta clé → `"statut": "construit"`, `"cours": "<id>"` (petit script, ta seule entrée).

## Compte rendu
Tiens ta section dans `cours\maths.md` (seulement TA section `## <clé>`, en relisant le fichier juste avant d'écrire : d'autres
agents y écrivent) : étapes faites, fichiers, nombre de diapositives, compétences, simulations (pages et vues), décisions prises,
problèmes, manques du lecteur, « PRÊT POUR LA VOIX : oui/non ». Ton rapport final (SubagentHandback) reprend ces points.
Disque C: presque plein (~1,5 Go) : pas de gros fichiers ; nettoie tes temporaires.

## NOUVELLES RÈGLES (11 novembre 2026) — obligatoires pour primitives, fonctions_ln, operations_formes
Lis `.agents/skills/cours-concentration/SKILL.md` section « Memory and rhythm » (+ « Data »), `suivi-des-acquis` sections 6–8,
`professeur` règle 26, et le brief `cours\methode_blocs\BRIEF_AGENTS.md` (outil `methode_blocs\blocs.py`, modèles finis
`methode_blocs\ajouts\math_ch1_limites_continuite.json`, `math_ch2_…`, `math_ch3_…` et le cours `backend/data/courses/math_ch1_limites_continuite.json`).
- `seances` à la racine du cours : séances de 3 blocs de 3–4 diapositives qui se suivent ; chaque bloc : `titre`, `cahier` (2–4 lignes
  barème), `retrouver` {prompt « Cahier fermé : … », attendu = formule/définition EXACTE du cadre, competence_id}, `exercice`
  (repris d'un exercice de diapo, ou nouveau QCM/libre avec demonstration s'il y a un calcul) ; bilan + carte dans la dernière séance.
- `competences[].rappels` : 3–4 questions de rappel par compétence, au moins deux formes (libre/qcm/vrai_faux).
- `question.prediction: true` sur au moins une diapositive sur trois (⌈n/3⌉) et au moins une par partie : question posée AVANT l'explication.
- UNE seule idée nouvelle par diapositive ; pas de passage automatique (rien à faire côté données).
- Comme ton cours est NOUVEAU, tu peux écrire seances/rappels/prediction directement dans tes p*.py/build.py ; OU construire le cours,
  faire `blocs.py base <cours>` une fois, puis écrire `methode_blocs/ajouts/<deck>.json` et `blocs.py appliquer`. Dans les deux cas
  le contrôle final est `python methode_blocs/blocs.py verifier <cours.json> <clé>` → « blocs : OK » et « cadre : OK ».
- Réactions préparées : produis SEULEMENT les items dans ton dossier de build : `preparer_reponses.py items <cours> <build>/items.json`
  et `blocs.py items <cours> <build>/items_blocs.json <build>/demos_blocs.json` (si tu passes par base/appliquer). Le coordinateur
  les fait écrire sur le VPS. Pas de SSH.
- Disque C: < 1 Go : aucun téléchargement de vidéo, aucune grosse capture gardée ; efface tes temporaires aussitôt.
