# Cours SVT 4 : relation_gene_proteine (agent du cours 4)

id : svt_ch4_relation_gene_proteine
Fichier : backend/data/courses/svt_ch4_relation_gene_proteine.json (draft, mode concentration, 47 diapositives, 10 activités, 350 min)
Simulations : frontend/public/media/simulations/svt/relation_gene_proteine-tableau/
Générateur : scratchpad .../scratchpad/svt_cours4/ (gen_cours.py, gen_lib.py, gen_part1.py, gen_part2.py, remplacer4.py,
  faire_bilan_carte.py, poser_cadre.py, statut.py, contrat_simulations.md, tester_sim.py, balayer.py, verif_pointages.py, check_js.py)

## Étapes
- [x] Brief, BRIEF commun, skills lus ; exploration lue (RGP1–RGP10, plan 47, NC1–NC8) ; anciennes images regardées
- [x] Contrat des simulations (scratchpad/svt_cours4/contrat_simulations.md) + kit commun molecules.js (peinture du vivant, code génétique complet)
- [x] Simulations (5 sous-agents opus, chacun vérifié : check_js, tester_sim, captures regardées puis supprimées) :
  paire_homologues (paire, mutation), marquage (uracile, acides_amines), drepanocytose (sang, molecule, echelles),
  transcription (transcription, brins, noyau), code_genetique (codons, tableau, proprietes), traduction (traduction, polysome, trois_schemas),
  mutation (mutation ; type / sequence jugée), schema_bilan (schema, construire), examen (document_ldl, reperages, lignes, phrase, restitution, amelogenine)
- [x] bilan.html, carte.html (adaptés du cours 3 par faire_bilan_carte.py ; captures regardées)
- [x] Cours JSON (générateur) : 47 diapositives, 8 compétences, aucune erreur de mot
- [x] Fiche cadre posée dans cadre_reference_2bac_pc.json (chapitres.relation_gene_proteine, poser_cadre.py) ; controler_cadre → « cadre : OK ; 0 point à relire »
- [x] verifier_texte_corpus : darija rares remplacées (remplacer4.py + 2e passe) ; restent des termes du programme (locus, allèle, faucille, ribosome, codon, anticodon, noms d'acides aminés, LDL…), définitions relues en français, quelques darija à 1-2 occurrences gardés
- [x] Vérifications : node --check TOUT OK (14 fichiers) ; verif_pointages : 367 pointages, tout existe (seule console : favicon 404) ; balayage temporel de toutes les vues : aucun texte hors cadre
- [ ] Réactions préparées — items.json fait (235 réactions) ; kit copié sur le VPS (/tmp/gen_rep_svt4 : gen_reponses_vps.py, reponse_eleve.py, simulation_reaction.py, items.json) ; LANCEMENT REFUSÉ par le classifieur (Remote Shell Writes), non contourné.
  À lancer par la session principale :
    ssh moalim-vps "cd /opt/moalim/backend && set -a && . /etc/moalim/backend.env && set +a && .venv/bin/python /tmp/gen_rep_svt4/gen_reponses_vps.py /tmp/gen_rep_svt4/items.json /tmp/gen_rep_svt4/sortie.json"
    scp moalim-vps:/tmp/gen_rep_svt4/sortie.json C:/Users/HP/AppData/Local/Temp/claude/9269525a2680ed40/a857ffbb-cf28-4072-880f-f5ac5134ee69/scratchpad/svt_cours4/
    python outils/cours/voxtts/preparer_reponses.py poser backend/data/courses/svt_ch4_relation_gene_proteine.json <scratchpad>/svt_cours4/sortie.json <scratchpad>/svt_cours4/pistes_reponses.json
    ssh moalim-vps "rm -rf /tmp/gen_rep_svt4"
  (gen_cours.py garde ensuite les réponses posées si la question n'a pas changé)
- [x] preparer_reponses verifier : ne manquent que les 47 pistes audio et les 235 réactions
- [x] programme_semestre1.json : statut « construit » (statut.py), champ « reste »

## PRÊT POUR LA VOIX (Bodi) : OUI pour les 47 pistes mixed + 11 démonstrations ; les 235 réactions d'abord écrites sur le VPS (ci-dessus)

## Décisions à faire valider
- Brin non transcrit : la diapositive rg_t5 montre les DEUX chemins (complémentaire du brin transcrit, ou recopie T → U) et dit la raison
  (les deux sont complémentaires du brin transcrit) ; les deux sont acceptés (corrigés 2024 N, 2025 N : « accepter … brin transcrit »).
- Pas de manip S8 du labo 3D (transcription / traduction n'ont pas de geste de laboratoire ; les simulations à la craie la remplacent) ;
  électrophorèse de l'hémoglobine non construite (document seulement).
- perimetre.json NON modifié (partage ADN / réplication en attente) ; ADN et réplication seulement rappelés (rg_o1, rg_t1).
- Exemple du gène et des allèles : le groupe sanguin ABO (chromosome 9, allèles A, B, O), au lieu de la couleur des yeux (polygénique) ; diapositives 2-3 du plan
  redistribuées : rg_g1 (image chromosome_adn_gene.png), rg_g2 (locus + allèles, simulation).
- Mutation illustrée par la résistance de bactéries à la streptomycine (boîtes de Pétri reconstituées), comme Lamsaf ; définition du barème 2018 R.
- Marquages (uracile, leucine radioactifs) : document RECONSTITUÉ (aucun professeur ne le montre ; temps 5 / 15 / 30 min choisis), écrit sur la simulation.
- Documents d'examen redessinés à partir des corrigés officiels : 2023 N (LDL, triplets 29-35), 2024 N (amélogénine, AMELX), 2025 N (ALDP, triplets 147-152) ; 2017 N cité pour la délétion de 3.
- Images gardées : adn_arnm_proteine.png (ouverture, et couverture provisoire du cours), chromosome_adn_gene.png, transcription_arnm.png ;
  non reprises : traduction_ribosome.png (trois ARNt = sites hors cadre), mutation_gene_proteine_caractere.png (cellules identiques). Ancienne simulation expression/ jamais réutilisée.
- Capacités RGP1–RGP10 reconstruites d'après le cadre CNEE 2015 cité : à confirmer.
- Durée 350 min (10 activités) au lieu des ~4 h visées par le plan.

## Problèmes
- tester_sim.py --images : captures sur fond blanc, craie à moitié écrite (signalé par les sous-agents) ; ils ont regardé leurs propres captures sur fond sombre.

## Ce qui reste
- réactions préparées (VPS, commande ci-dessus) ; voix Bodi (session principale) ; couverture propre au chapitre ; validation utilisateur.
- fonctions manquantes du lecteur : aucune (moteur etapes.js : play_until / set_time / set_parameters / highlight). verif_pointages ne savait pas set_time (ajouté au script).
