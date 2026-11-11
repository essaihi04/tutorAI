# Exploration SVT génétique (agent d'exploration, 10 novembre 2026)

Mission : trois explorations, dans l'ordre : notion_information_genetique → relation_gene_proteine → genie_genetique.
Dossier de travail : C:\Users\HP\AppData\Local\Temp\claude\9269525a2680ed40\a857ffbb-cf28-4072-880f-f5ac5134ee69\scratchpad\explo_genetique\
(examens : digest_examens.txt ; audits : audit_<id>.md)

## Constats de départ
- perimetre.json (SVT) : clés existantes relation_gene_proteine (contient aussi ADN/réplication) et mutations_maladies ; MANQUENT notion_information_genetique et genie_genetique.
- Examens PC 2016-2025 (coef 5) : génétique d'expression quasi à chaque session (séquences → ARNm → acides aminés → origine génétique) ; réplication/mitose : 2017 R (thymidine radioactive, fève), 2018 R (QCM métaphase, réplication ; anaphase), 2024 N (V/F phase S), 2024 R (QCM G1, fin de S, yeux de réplication) ; génie génétique : AUCUNE question en 20 sessions.
- perimetre.json met PCR, séquençage, électrophorèse détaillée en termes hors programme (SVT global).
- Anciennes ressources : seed database/seed_data/lessons/svt_ch2_l1.json (nature de l'info génétique, sans médias) et svt_ch2_l2.json (expression, 5 images + simulation 3D) ; simulations media/simulations/svt/ch2_information_genetique/mitose (TP racine d'oignon) et /expression (WebGL three.js) ; images media/images/svt/ch2_information_genetique/lesson_2_expression (5 png). Labo 3D : inventaire S6 extraction ADN, S7 mitose, S8 synthèse protéines, S9 génie génétique (non codées).

## Chapitre 1 : notion_information_genetique
Statut : 10 audits faits (20:40), 2 sources complémentaires en téléchargement, puis synthèse.
Vidéos (audit_<id>.md dans le dossier de travail) :
1. wrFXLGtj23w Prof Faress, cours complet 142 min — fait (zoom noyau→ADN, cycle q/2q, mitose ; 25 min d'enzymologie hors programme)
2. D8bO8v-csYQ Maison Des Sciences, cours complet 123 min — fait (le plus riche en documents : amibe, acétabulaire, Gurdon, Griffith, Avery, Chargaff, exercice courbe)
3. 3ous51ywCAQ SVT Mousstaid, résumé 36 min — fait (réplication en 3 colonnes G1/S/G2, maçon ADN polymérase)
4. pwhXDn3WP-Q Pr Ayyoub Lamsaf, partie 1, 33 min — fait (amibe, acétabulaire, méthode on observe / on déduit)
5. sSxAqe_in34 Prof Sarah, partie 1, 10 min — fait (intro scène de crime, noyau ; mince)
6. l2bkjgwtdRg Driss DOTCOM, résumé 44 min — fait (photos de mitose, phrases-justification ; erreurs chromatide/chromosome)
7. GG_G8CCM0L8 Dr Ikram, partie 1 cycle et mitose, 44 min — fait (mots imposés par phase, bonbons doublés)
8. Ud-dxvPcfpA Ouissamsvt, exercices 53 min — fait (QCM, V/F, photos, courbe 0-36 h décrite phase par phase)
9. w_JmVcGoVmg Prof Wessal, live 72 min — fait (courbe q→2q, 3 mots ; réplication reportée)
10. -71A2w7fNEc M. Aouragh, résumé 17 min — fait (fiche, PMAT, courbe Q→2Q colorée)
Complémentaires (mêmes profs, non comptés) : Kt-Sr2em7UM Lamsaf « mécanisme de la réplication » (Meselson-Stahl ?), QsPZTaFg79E Faress « national 2015 R, durée du cycle » (calculs).
Trous constatés : Meselson-Stahl, Taylor, indice mitotique / durées : presque personne ; Griffith/Avery/Chargaff : seulement Maison Des Sciences.

FAIT (21:30) : backend/data/curriculum/exploration/notion_information_genetique.json écrit (générateur scratchpad/scripts/gen_nig.py), 11 capacités NIG1-NIG11, 8 compétences, 47 diapositives, 9 notions complexes, 10 simulations à la craie prévues, 2 manips labo 3D planifiées (S7 mitose, S6 extraction ADN). Checklist OK. Clé ajoutée dans perimetre.json (script perimetre_nig.py). Statut « explore » posé dans programme_semestre1.json.

## Chapitre 2 : relation_gene_proteine
Statut : téléchargements lancés (liste_ch2.txt) : 6xn9O_YPUH0 Lamsaf (version PC), UstraDXOHsI Faress, eZ67oGGh_j8 Sarah, 1lF9NJ_xAU0 Mousstaid, dwX1nxslF4U Elbrahimi, xF6bmRtAzTk Ikram (transcription), 9DeCtVL396E Ouissam (exercice national), RApWn5qtoFQ Wessal (exercice), R1rPnnabpWM AJIN9RAW, e4GMkobtA10 SVTfabour. Driss l2bkjgwtdRg (déjà audité, 19 min d'expression + national 2025) en source complémentaire.

### Reprise (11 novembre, 00:10, agent de reprise)
- YouTube refuse TOUS les sous-titres (429 depuis le 10 nov. 21:06) ; commentaires et vidéo passent. Décision : audits sur images + commentaires ; un fichier <id>.txt d'une ligne « SOUS-TITRES INDISPONIBLES » marque l'absence (à retenter à la fin).
- Disque C: plein (52 Mo libres à 00:37) : les images sont prises SANS télécharger la vidéo (scratchpad/scripts/images_flux.py : ffmpeg lit le flux à chaque instant) ; lecture en planches 2×2 (scripts/planches.sh).
- L'ancien script telecharger.sh (PID 9848, liste_ch2.txt) tourne encore : pas pu l'arrêter (refusé) ; neutralisé par les marqueurs (.txt, commentaires, IMAGES_LUES présents → il saute tout).
- Audits faits : eZ67oGGh_j8 Sarah (partie 1 seulement : gène, allèle, mutation ; pas de transcription), 1lF9NJ_xAU0 Mousstaid (résumé + 2 exemples brin transcrit / non transcrit).

- Audits faits aussi : dwX1nxslF4U Elbrahimi (schéma bilan préparé, 3 phases de traduction), xF6bmRtAzTk Ikram (transcription, astuce brin non transcrit), 9DeCtVL396E Ouissam (national 2017 R XPB + 2018 N Mody-2), RApWn5qtoFQ Wessal (4 repérages, phrases à trous).
- Générateur écrit : scratchpad/scripts/gen_rgp.py + gen_rgp_suite.py (47 diapositives, 8 compétences, 10 capacités RGP1-RGP10, 8 notions complexes, 10 simulations). Reste : audits AJIN9RAW (R1rPnnabpWM) et SVTfabour (e4GMkobtA10), remplir leurs champs (placeholders AJIN9RAW_* / FABOUR_*), lancer, statut explore.

## Chapitre 3 : genie_genetique
FAIT (11 nov., 01:15) : HORS PROGRAMME PC. Preuves : cadre de référence SVT filière Sciences Physiques 2015 (CNEE, option français, lu en entier : domaine 2 = 2.1 à 2.4, aucun mot génie génétique / restriction / OGM / plasmide) ; 0 question en 20 sessions PC ; absent de svt.json et perimetre.json ; toutes les vidéos marocaines de génie génétique étiquetées « option SVT / médecine » (Faress, Sarah, Lamsaf, Wessal, AJIN9RAW). Exploration courte : backend/data/curriculum/exploration/genie_genetique.json (générateur scratchpad/scripts/gen_gg.py). programme_semestre1.json : statut « hors_programme_pc » + decision_a_valider (script statut_gg.py).

## Décisions à faire valider
- genie_genetique : pas de cours pour les PC (hors cadre). Si l'utilisateur veut un module facultatif « médecine », exploration complète à faire (vidéos déjà repérées dans le fichier).

### Reprise 2 (11 novembre, 10:20, troisième agent)
- Constat : les 10 audits du chapitre 2 sont faits, relation_gene_proteine.json écrit et reproductible (gen_rgp.py régénère un fichier identique), statut « explore » posé, genie_genetique tranché (hors programme PC). Vidéos et images déjà supprimées (explo_genetique ne garde que .txt / commentaires / audits).
- Les sous-titres YouTube passent de nouveau (10:24, R1rPnnabpWM : 1897 lignes). Téléchargement séquentiel des 6 autres transcriptions manquantes (1lF9NJ_xAU0, 9DeCtVL396E, dwX1nxslF4U, e4GMkobtA10, eZ67oGGh_j8, xF6bmRtAzTk), puis compléments « transcription » dans les audits et intégration dans gen_rgp_suite.py.
- FAIT (12:20) : 6 transcriptions récupérées une à une (R1rPnnabpWM, 1lF9NJ_xAU0, 9DeCtVL396E, dwX1nxslF4U, xF6bmRtAzTk, + RApWn5qtoFQ déjà là) ; eZ67oGGh_j8 et e4GMkobtA10 n'ont AUCUN sous-titre arabe (pas un 429). Audits complétés par 3 sous-agents opus (section 15 « Complément d'après la transcription », limites corrigées). Intégration : scratchpad/scripts/gen_rgp_complements.py (exécuté par gen_rgp.py) : +4 insistances, +4 pièges (comptage des nucléotides, synonymes des brins, lecture du tableau, mutation silencieuse), +4 analogies (file d'attente, téléphone, salle/porte, train/rail), +3 conseils (ordre de la phrase d'origine génétique), +2 à ne pas dire, variante « brin non transcrit » précisée, limites réécrites. relation_gene_proteine.json régénéré (140 266 o, JSON valide).
- Nettoyage : aucune vidéo ni image dans explo_genetique (seuls .txt, commentaires, audits, scripts).
- Chapitre 2 TERMINÉ. Chapitre 3 déjà tranché (hors programme PC).
