# Cours SVT 3 : notion_information_genetique (agent du cours 3)

id : svt_ch3_notion_information_genetique
Fichier : backend/data/courses/svt_ch3_notion_information_genetique.json
Simulations : frontend/public/media/simulations/svt/notion_information_genetique-tableau/
Générateur : scratchpad .../scratchpad/svt_cours3/ (gen_cours.py, gen_lib.py, gen_part*.py)

## Étapes
- [x] Brief, BRIEF commun, skills lus ; exploration lue (cadre NIG1–NIG11, plan 47 diapos, NC1–NC9)
- [x] Dossier des simulations créé : commun.js (window.GenetiqueTableau.Scene), genetique.css
- [x] Contrat des simulations écrit (scratchpad/svt_cours3/contrat_simulations.md)
- [x] Simulations : sous-agents IMPOSSIBLES (« Concurrent subagent limit reached », consigne : ne pas réessayer) → je les écris moi-même avec un moteur commun etapes.js (vues, moments, play_until, protocole, poignées, peinture partagée)
  - faits et vérifiés (node --check, chaque moment piloté, __horsCadre vide, image regardée) : noyau.html, zoom.html, cycle.html, mitose.html, bacteries.html, adn.html
  - faits aussi : meselson.html, thymidine.html, replication.html, documents.html (11/11 reprise : node --check TOUT OK ; verif_pointages.py : 359 pointages, tout existe, seule erreur console = favicon 404)
- [x] Cours JSON (générateur) : 47 diapositives, 10 activités, 300 min, aucune erreur de mot
- [x] bilan.html, carte.html
- [x] Fiche cadre (scratchpad/svt_cours3/poser_cadre.py ; + formules « interphase = G1 + S + G2 » et « nucléosome = ADN + histones ») + controler_cadre → « cadre : OK » (2 à relire bénins)
- [x] verifier_texte_corpus : toutes les darija rares remplacées (remplacer.py) ; restent 281 mots français rares = termes du programme, définitions relues en français, nombres (heures) : gardés exprès
- [ ] Réactions préparées — BLOQUÉ par la permission (ssh/scp vers moalim-vps refusé par le classifieur ; non contourné).
  Fait : `preparer_reponses.py items` → 247 réactions, scratchpad/svt_cours3/items.json ; dossier prêt localement :
  scratchpad/svt_cours3/gen_rep/ (gen_reponses_vps.py « professeur de SVT », chemin /tmp/gen_rep_svt3 ; reponse_eleve.py avec import corrigé ; simulation_reaction.py ; items.json).
  À lancer par la session principale :
    ssh moalim-vps "mkdir -p /tmp/gen_rep_svt3" && scp C:/Users/HP/AppData/Local/Temp/claude/9269525a2680ed40/a857ffbb-cf28-4072-880f-f5ac5134ee69/scratchpad/svt_cours3/gen_rep/* moalim-vps:/tmp/gen_rep_svt3/
    ssh moalim-vps "cd /opt/moalim/backend && set -a && . /etc/moalim/backend.env && set +a && .venv/bin/python /tmp/gen_rep_svt3/gen_reponses_vps.py /tmp/gen_rep_svt3/items.json /tmp/gen_rep_svt3/sortie.json"
    scp moalim-vps:/tmp/gen_rep_svt3/sortie.json <scratchpad>/svt_cours3/ && python outils/cours/voxtts/preparer_reponses.py poser backend/data/courses/svt_ch3_notion_information_genetique.json <scratchpad>/svt_cours3/sortie.json <scratchpad>/svt_cours3/pistes_reponses.json
    (gen_cours.py garde ensuite les réponses posées si la question n'a pas changé) ; ssh moalim-vps "rm -rf /tmp/gen_rep_svt3"
- [x] Vérifications finales (11/11) : node --check TOUT OK (14 fichiers) ; controler_cadre « cadre : OK » ; preparer_reponses verifier : seules manquent les 47 pistes audio et les 247 réactions (VPS) ; verif_pointages (Chrome headless, toutes les simulations) : 359 pointages, aucune erreur console, rien hors cadre.
- [x] programme_semestre1.json : statut « construit », champ « reste » (réactions + voix)

## PRÊT POUR LA VOIX (Bodi) : OUI pour les 47 pistes mixed + 9 démonstrations ; les 247 réactions d'abord écrites sur le VPS (ci-dessus)

## Décisions à faire valider
- Mitose végétale : GARDÉE en une diapositive (ig_m5_vegetale, comparaison animale/végétale : calottes polaires, pas d'asters, nouvelle paroi) — le cadre (NIG4) demande de comparer, et les examens donnent des photos de racine (méristème) à reconnaître.
- Extraction de l'ADN (oignon, banane) : PAS de diapositive ; seulement planifiée comme manip du labo 3D (exploration) — jamais demandée aux nationaux PC, observation qualitative.
- Thymidine radioactive (Taylor) : GARDÉE (ig_r7, ig_r8) — tombée au national 2017 R ; correction reprise du corrigé national.
- Hors cadre tenus hors du cours : hélicase, primase, Okazaki, brin précoce/retardé, kinétochore, cyclines… (liste hors_cadre de la fiche) ; la réplication reste au niveau ADN polymérase + yeux/fourches + sens 5'→3'.
- Capacités NIG1–NIG11 reconstruites (texte officiel du cadre SVT PC absent du dépôt) : à confirmer. Fiche cadre posée avec deux formules ajoutées (interphase = G1 + S + G2 ; nucléosome = ADN + histones).
- Aucune image de l'ancien cours svt_ch2_l1 reprise : les 47 diapositives sont des simulations à la craie ; couverture provisoire : /media/images/course-covers/svt-energy-cellulaire.png (à remplacer par une couverture génétique).
- Mots français rares gardés exprès dans la voix : termes du programme (chromatide, centromère, semi-conservative, hybride…), noms propres (Griffith, Avery, Meselson, Stahl, Chargaff, Gurdon, Watson, Crick), définitions relues en français, « heures » dans les nombres.

## Problèmes

## Ce qui reste
- réactions préparées (VPS, commandes ci-dessus) ; voix Bodi (session principale) ; couverture du cours ; validation utilisateur.
- fonctions manquantes du lecteur : aucune relevée (moteur etapes.js : play_until/set_time/set_parameters/highlight, comme le témoin).
