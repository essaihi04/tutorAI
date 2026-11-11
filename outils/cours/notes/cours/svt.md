# Avancement SVT (agent SVT, 10 novembre 2026)

Brief : BRIEF.md (même dossier). Skills lus : exploration-de-cours, cours-concentration, simulations-au-tableau,
professeur, voix-du-cours, suivi-des-acquis, scientific-course-visuals.

## Organisation
Un sous-agent (opus) par cours, chacun suit le brief à la lettre et tient sa section ci-dessous à jour.
- Cours 1 et 2 (explorations faites) : construits en parallèle.
- Cours 3, 4, 5 : explorations à faire, une vidéo YouTube à la fois (429), puis construction.

| # | clé | id du cours | simulations | statut |
|---|-----|-------------|-------------|--------|
| 1 | reactions_responsables_liberation_energie | svt_ch1_reactions_responsables_liberation_energie | svt/reactions_responsables_liberation_energie-tableau/ | construit (43 diapos, 10 comp., 15 simus) ; 252 réactions posées par la session principale ; voix en file |
| 2 | role_muscle_strie_squelettique | svt_ch2_role_muscle_strie_squelettique | svt/role_muscle_strie_squelettique-tableau/ | construit et vérifié (53 diapos, 9 comp., 12 simus, 279 réactions) |
| 3 | notion_information_genetique | svt_ch3_notion_information_genetique | svt/notion_information_genetique-tableau/ | construit (47 diapos, 8 comp., 11 simus) ; 247 réactions posées par la session principale ; voix en file |
| 4 | relation_gene_proteine | svt_ch4_relation_gene_proteine | svt/relation_gene_proteine-tableau/ | construit (47 diapos, 8 comp., 10 simus) ; 235 réactions À ÉCRIRE (VPS refusé) |
| 5 | genie_genetique | svt_ch5_genie_genetique | — | HORS PROGRAMME PC (exploration courte) : aucun cours, à valider |

## Prêts pour la voix
- Cours 2 muscle : 53 pistes, 279 réactions, 7 démonstrations.
- Cours 1 énergie : 43 pistes + démonstrations + 252 réactions (posées).
- Cours 3 information génétique : 47 pistes + 9 démonstrations + 247 réactions (posées).
- Cours 4 expression : 47 pistes + 10 démonstrations ; 235 réactions à écrire d'abord (voir blocage).
- NE PLUS CHANGER les textes dits des cours 1, 2, 3 (voix en calcul) ; régénérer seulement avec --garder-reponses.

## Décisions à faire valider
- (énergie) complexes I–IV : non appris, transporteurs anonymes T1–T4 ; lecture d'un document qui les nomme (le_c8_national, chaine.html?etiquettes=examen).
- (énergie) glucose : valeur de l'énoncé ; exemple 2860 kJ et 30,5 kJ/ATP (40,5 % / 2,13 %) ; 38 ATP, suivre l'énoncé s'il dit 36.
- (énergie) statut « construit » posé alors que les réactions manquent.
- (muscle) 53 diapos au lieu de 62, 5 séances, ordre du manuel ; diapo labo 3D retirée.
- (muscle) fibres glycérinées : aucun document réel trouvé → document reconstitué, présenté comme tel (ms_c1_exigences).
- (muscle) valeurs rondes (secousse 0,01/0,04/0,05 s ; sarcomère 2,5→2,0 µm), tableaux d'examen reconstitués.
- (génie génétique) HORS programme PC (cadre SVT PC 2015 : sous-domaines 2.1–2.4 seulement, 0 question en 20 sessions) : aucun cours ; statut hors_programme_pc.
- (info génétique) mitose végétale gardée (1 diapo) ; extraction ADN = labo 3D seulement ; Taylor gardé (2017 R) ; réplication sans hélicase/Okazaki ; capacités NIG1–NIG11 reconstruites ; couverture provisoire à refaire.
- (expression) perimetre.json : retirer ADN/réplication de relation_gene_proteine (propositions dans l'exploration, a_ajouter.perimetre_json) — non appliqué ; brin non transcrit : raison puis raccourci T→U, deux chemins acceptés ; pas de manip S8.

## Blocage (cours 1 et 3 : résolus par la session principale)
- Cours 1 : l'exécution de gen_reponses_vps.py sur le VPS (charge /etc/moalim/backend.env) a été refusée par le classifieur
  de permissions. Non contourné. Commande dans svt_cours1.md ; puis poser + gen_cours.py --ecrire.
- Cours 3 : ssh/scp vers moalim-vps refusé. Dossier prêt scratchpad/svt_cours3/gen_rep/ ; commandes dans svt_cours3.md.

## Fonctions manquantes du lecteur
- Aucun lien du cours vers une manip du labo 3D (énergie : svt-exao-levures.html).
- preparer_reponses.py ne gère pas les exercices d'association.

## Journal par cours
Chaque sous-agent tient son propre fichier dans ce dossier (pas d'écriture concurrente) :
svt_cours1.md, svt_cours2.md, svt_genetique_exploration.md, svt_cours3.md, svt_cours4.md, svt_cours5.md.
Ce fichier-ci est la synthèse, mise à jour par l'agent SVT principal.
- Cours 4 : lancement sur le VPS refusé (« Remote Shell Writes »). Kit déjà sur le VPS dans /tmp/gen_rep_svt4 ; commandes dans svt_cours4.md
  (gen_reponses_vps.py → scp sortie.json → preparer_reponses.py poser → rm /tmp/gen_rep_svt4).
- (expression) ABO pour gène/allèles ; mutation par bactéries résistantes (boîtes reconstituées) ; marquages reconstitués (5/15/30 min) ;
  documents 2023 N/2024 N/2025 N redessinés ; RGP1–RGP10 reconstruites ; 350 min ; couverture provisoire.

## Reste
- Réactions du cours 4 (VPS), voix Bodi des cours 1–4, couvertures génétiques (cours 3 et 4), passage dans /dev/course-player,
  validation par l'utilisateur, décision génie génétique, mise à jour de perimetre.json (partage ADN/réplication).
