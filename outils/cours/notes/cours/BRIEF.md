# Brief commun aux trois agents de cours (10 novembre 2026)

Dépôt : C:\Users\HP\Desktop\ai-tutor-bac (partagé : d'autres sessions y travaillent).

## But
Construire TOUS les cours restants du 1er semestre de ta matière (liste et ordre : backend/data/curriculum/programme_semestre1.json),
en mode concentration, au même niveau que le cours témoin déjà fini :
- backend/data/courses/phys_ch2_ondes_periodiques.json (47 diapositives, compétences, demonstrations, concentration…)
- frontend/public/media/simulations/physics/ondes-periodiques-tableau/ (simulations à la craie, bilan.html, carte.html)
- backend/data/curriculum/exploration/ondes_mecaniques_periodiques.json (exploration)

## Méthode (lire les skills AVANT de commencer, et les suivre à la lettre)
.agents/skills/exploration-de-cours/SKILL.md, cours-concentration/SKILL.md, simulations-au-tableau/SKILL.md,
professeur/SKILL.md, voix-du-cours/SKILL.md (sections texte parlé ; PAS la génération), suivi-des-acquis/SKILL.md,
scientific-course-visuals/SKILL.md. Labo 3D (labo-virtuel-2bac) : seulement PLANIFIER les manips dans l'exploration, ne pas les construire.

Pour chaque cours, dans l'ordre :
1. Exploration (skill exploration-de-cours) : 10 vidéos YouTube de 10 profs marocains, transcriptions + images du tableau
   (backend/scripts/explorer_cours.py), audit, comparaison, cadre de référence, erreurs d'examen, commentaires d'élèves,
   notions complexes découpées. Fichier : backend/data/curriculum/exploration/<clé>.json.
   Si l'exploration existe déjà (ondes_lumineuses, reactions_responsables_liberation_energie, role_muscle_strie_squelettique,
   limites_continuite, derivation_etude_fonctions), ne la refais pas : pars d'elle.
   YouTube limite les requêtes (429) : espace tes téléchargements, une vidéo à la fois. Images lourdes : supprime-les après
   lecture ; besoin d'espace → VPS (ssh moalim-vps, dossier /srv/corpus_v4/explo_<matière>/, à nettoyer à la fin).
2. Cours existant : s'il y a un ancien cours de ce chapitre dans backend/data/courses/ (ex. *_course_v1.json), regarde-le et
   ses images (section 6 bis du skill exploration) : on garde les images utiles, on ne reprend JAMAIS ses anciennes
   simulations, on les refait selon les nouvelles règles.
3. Cours : backend/data/courses/<id>.json (id du style phys_chN_<clé>, svt_chN_<clé>, math_chN_<clé>), "status": "draft",
   "mode": "concentration", compétences, demonstration sur toute question de calcul/démonstration, concentration complète,
   bilan + carte du chapitre à la fin, speech_text.mixed en darija simple (règles voix-du-cours).
4. Simulations à la craie : frontend/public/media/simulations/<physics|chemistry|svt|maths>/<clé>-tableau/ (nouvelles).
5. Cadre : fiche du chapitre dans backend/data/curriculum/cadre_reference_2bac_pc.json (clé chapitres.<clé>), puis
   python outils/cours/voxtts/controler_cadre.py <cours.json> <clé> → « cadre : OK ».
   Ce fichier et programme_semestre1.json sont partagés avec les deux autres agents : modifie-les UNIQUEMENT par un petit
   script python qui relit le fichier, ajoute ta clé, et réécrit aussitôt (indent 2, ensure_ascii=False), jamais par une
   réécriture complète gardée en mémoire. Ne touche à aucune clé d'un autre chapitre.
6. Réactions préparées : preparer_reponses.py items/poser (DeepSeek via VPS gen_reponses_vps.py) — texte seulement.
7. Vérifications : node --check des scripts de chaque simulation ; controler_cadre OK ; preparer_reponses.py verifier
   doit tout passer SAUF les pistes audio manquantes.

## Interdits
- NE GÉNÈRE AUCUNE VOIX (pas de Kaggle) : le compte n'a que 2 sessions GPU et trois agents se battraient. La session
  principale fera toutes les voix Bodi. Quand un cours est prêt pour la voix, écris-le dans ton fichier d'avancement.
- Aucun commit, aucun push, aucun déploiement, pas de stash/reset/checkout. Ne modifie pas les fichiers de l'application
  (frontend/src, backend/app) : si le lecteur manque d'une fonction, note-le dans ton avancement.
- Ne touche pas aux cours / simulations des autres matières ni au cours témoin.
- Ne lis pas les fichiers d'identifiants ; ne te connecte à aucun site.

## Décisions en attente de l'utilisateur
Quand une exploration laisse une décision ouverte (ordre des chapitres, notion à inclure ou non…), tranche selon le cadre de
référence officiel et les examens nationaux, construis, et écris la décision dans ton fichier d'avancement (section
« Décisions à faire valider »).

## Avancement (pour reprendre si ton contexte s'épuise)
Tiens à jour le fichier <matière>.md de ce dossier : cours par cours, étape faite, fichiers créés, décisions, problèmes.
Relis-le au début. Travaille cours par cours (un cours fini et vérifié avant le suivant).
