# Cours SVT 2 : role_muscle_strie_squelettique (agent du cours 2)

id : svt_ch2_role_muscle_strie_squelettique
Fichier : backend/data/courses/svt_ch2_role_muscle_strie_squelettique.json
Simulations : frontend/public/media/simulations/svt/role_muscle_strie_squelettique-tableau/
Générateur : scratchpad .../scratchpad/svt_cours2/

## Étapes
- [x] Brief lu
- [x] Skills lus
- [x] Exploration + ancien cours lus (images regardées : hierarchie_muscle_3d, micrographie, sarcomere_actine_myosine_3d, reconstitution_emg_effort gardées)
- [x] Simulations (4 sous-agents opus, contrat : scratchpad/svt_cours2/contrat_simulations.md) : myographe, intensite, sommation (+myogramme.js), chaleur, voies, structure, sarcomere (+filaments.js), calcium, cycle, exigences (+molecules.js) ; node --check OK, moments vérifiés en Chrome headless
- [x] bilan.html, carte.html (adaptés du témoin ; vérifiés en Chrome headless : rien hors cadre)
- [x] Cours JSON : 53 diapositives, 11 activités, 253 min, compétences C1–C9 ; générateur scratchpad/svt_cours2/gen_cours.py (+ gen_lib.py, gen_part1.py, gen_part2.py) ; tous les mots des repères vérifiés, tous les moments/repères/paramètres appelés existent dans les simulations
- [x] Fiche cadre role_muscle_strie_squelettique ajoutée (script) ; controler_cadre → « cadre : OK ; 0 point à relire »
- [x] verifier_texte_corpus : 330 → 272 mots ; restent ~99 termes SVT du programme (absents du corpus de physique, gardés) et ~107 formes darija courantes mais rares dans le corpus (négations, conjugaisons) — à relire avant la voix
- [x] Réactions préparées : 279/279 écrites (DeepSeek, VPS, dossier temporaire supprimé), posées ; aucune parole avec chiffre
- [x] Vérifications : node --check de tous les scripts OK ; controler_cadre « cadre : OK » ; preparer_reponses verifier : seules manquent les 53 pistes de diapositive et les 279 voix de réactions
- [x] programme_semestre1.json : statut « construit »

## PRÊT POUR LA VOIX (Bodi) : oui — 53 pistes mixed + 279 réactions + 7 démonstrations (question.demonstration.parole)

## Décisions à faire valider
- (a) Longueur : 53 diapositives (au lieu des 62 du plan d'exploration), 11 activités, environ 4 h en 5 séances ; ordre du manuel gardé (myogramme → chaleur/chimie → structure → glissement → mécanisme Ca²⁺/ATP → voies de l'ATP → méthode → bilan). Fusions : inefficace+seuil ; recrutement+amplitude max ; tableau repos/activité + ATP/PC ; bande claire/zone H/bande sombre en une comparaison ; accès fermé + Ca²⁺ ; striation dite dans « les bandes » et reprise en restitution ; méthode décrire/comparer/déduire/expliquer/hypothèse en 3 diapositives ; la diapositive « labo 3D » retirée (manip non branchée au lecteur).
- (b) Fibres glycérinées : aucun document réel trouvé (examens 2016–2025 du dépôt, ancien cours, images). Diapositive GARDÉE avec un document reconstitué, écrit « Document reconstitué (d'après les expériences classiques des manuels) » sur la simulation exigences.html et dit dans la voix ; raison : capacité MSS9 du cadre (montrer que ATP et Ca²⁺ sont nécessaires) et associations des nationaux 2022 N / 2024 R sur les rôles du Ca²⁺ et de l'ATP. À remplacer par un document du manuel si l'utilisateur en fournit un.
- Valeurs du sarcomère (2,5/1,5/1,0/0,5 → 2,0/1,5/0,5/0 µm) et de la secousse (0,01/0,04/0,05 s) choisies rondes, dites comme ordres de grandeur.

## Problèmes
- Le corpus de la voix (professeurs de physique) ne connaît pas la plupart des termes SVT (sarcomère, myosine, stries…) : gardés comme termes du programme ; à écouter avec attention après la génération (detecter_murmures).

## Fonctions manquantes du lecteur
- Aucune bloquante. Les exercices d'association ne sont pas préparés par preparer_reponses (non utilisés ici).

## Ce qui reste
- Voix Bodi (session principale), puis lecture dans le lecteur (/dev/course-player) et validation par l'utilisateur.
- Document réel des fibres glycérinées à fournir si possible (remplacerait le document reconstitué).
