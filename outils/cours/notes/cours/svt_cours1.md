# Cours SVT 1 — reactions_responsables_liberation_energie (agent du cours 1)

id : svt_ch1_reactions_responsables_liberation_energie
fichier : backend/data/courses/svt_ch1_reactions_responsables_liberation_energie.json
simulations : frontend/public/media/simulations/svt/reactions_responsables_liberation_energie-tableau/

## Étapes
- [x] Brief, BRIEF commun et skills lus (10 nov. 2026)
- [x] Exploration relue, témoin et kit craie étudiés
- [x] Générateur du cours : scratchpad/svt_cours1/ gen_base.py + p1..p4.py + gen_cours.py (`python gen_cours.py --ecrire` ; garde les réactions et pistes déjà posées). 43 diapositives, 11 activités, C1–C10 (cadre LE1–LE10).
- [x] Simulations (sous-agents opus, vérifiées headless) : commun.js, peinture.js, svt.css, glycolyse, exao (?vue=levures|mitochondries|pulse_o2), vesicules, chaine (?o2=0, ?entree=fadh2, ?poison=cyanure, ?etiquettes=examen), mitochondrie (?legendes=numeros), taxi (?transporteur=fad), pyruvate, krebs, atp, fermentations (?vue=lactique|alcoolique), compteur, rendement, carrefour (?vue=plan|complet)
- [x] bilan.html, carte.html (adaptés du témoin, vérifiés headless : hors cadre vide, aucun débordement)
- [x] Cadre : clé chapitres.reactions_responsables_liberation_energie posée par scratchpad/svt_cours1/poser_cadre.py ; controler_cadre → « cadre : OK » (1 point à relire : la question de calcul « … = ? »)
- [x] verifier_texte_corpus : darija rare = 0 ; 112 occurrences de mots français rares gardés exprès (termes du programme, d'examen ou de labo : organite, pédonculées, transporteur, oxydé, réduit, cyanure, résidu, vésicules, graphique, montage, seringue, kilojoules…)
- [ ] Réactions préparées — BLOQUÉ par la permission : `preparer_reponses.py items` fait (252 réactions, scratchpad/svt_cours1/items.json) ; dossier prêt sur le VPS : /tmp/gen_rep_svt1 (gen_reponses_vps.py avec « professeur de SVT », reponse_eleve.py, simulation_reaction.py, items.json). L'exécution sur le VPS (qui charge /etc/moalim/backend.env) a été refusée par le classifieur de permissions. À lancer par la session principale :
  ssh moalim-vps "cd /opt/moalim/backend && set -a && . /etc/moalim/backend.env && set +a && .venv/bin/python /tmp/gen_rep_svt1/gen_reponses_vps.py /tmp/gen_rep_svt1/items.json /tmp/gen_rep_svt1/sortie.json"
  puis scp de sortie.json et : python preparer_reponses.py poser <cours.json> sortie.json pistes_reponses.json ; puis régénérer avec gen_cours.py (il garde les réponses).
- [x] Vérifications finales : node --check OK sur les 15 pages + commun.js + peinture.js ; controler_cadre « cadre : OK » ; preparer_reponses verifier : 43 « pas de piste audio » + 252 « réaction manquante » (rien d'autre : tous les mots trouvés, toutes les clés) ; moments, repères et paramètres de chaque pointage retrouvés dans le code des simulations ; captures headless de chaque moment (scratchpad/svt_cours1/chk, chk3, s5).
- programme_semestre1.json : statut « construit ».

## Prêt pour la voix
OUI pour les 43 pistes des diapositives et les démonstrations (texte vérifié corpus) ; les réactions préparées doivent d'abord être écrites (ci-dessus).

## Fonctions manquantes du lecteur
- Aucun lien du lecteur vers la manip 3D svt-exao-levures.html (diapo 5 du plan) : remplacée par exao.html.
- Les simulations du cours ne sont pas encore enregistrées comme ressources de leçon (après validation).

## Décisions à faire valider
- (a) Complexes I–IV : NON appris (transporteurs anonymes T1–T4) ; le cours apprend à LIRE un document qui les nomme (CI…CIV, CV = ATP synthase, RH2/R) : diapo le_c8_national + chaine.html?etiquettes=examen. Raison : hors programme comme connaissance, mais présents dans 5 nationaux 2016-2025. Noté dans cadre.decisions.
- (b) Énergie du glucose : toujours celle de l'énoncé ; exemple du cours 2860 kJ et 30,5 kJ/mol (40,5 % ; 2,13 %) ; rendement.html accepte 2870 (40,4 %) et 36 ATP (38,4 %).
- (c) 38 ATP (2 + 2 + 30 + 4), en disant que certains documents écrivent 36 : on suit l'énoncé.
- (d) Plan de l'exploration suivi (42 diapos) ; « Ce qu'il faut retenir » séparé en deux diapos (fiche + carte) → 43. La manip 3D ExAO (diapo 5 du plan) n'est pas branchée : remplacée par exao.html?vue=levures (prédiction avant l'injection).
- (e) Le vrai/faux de le_x1 garde exprès l'affirmation fausse « Le glucose entre dans la mitochondrie » (piège classique).

## Problèmes
(aucun)
