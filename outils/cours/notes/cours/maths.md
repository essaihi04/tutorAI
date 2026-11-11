# Avancement — agent MATHÉMATIQUES (10 novembre 2026)

Cours (ordre programme_semestre1.json) : limites_continuite, derivation_etude_fonctions, suites_definition, primitives, fonctions_ln, operations_formes.

## État
- [construit, réactions à générer] limites_continuite → math_ch1_limites_continuite (détail : section ## limites_continuite).

## Décisions à faire valider (agent maths, tranchées selon le cadre 2BAC PC BIOF et les nationaux 2016-2025)
- limites_continuite — dichotomie : GARDÉE, bloc court d1–d4 « pour les devoirs, pas demandé au national » (encadrement à une amplitude donnée, sans algorithme ni majoration d'erreur) ; capacité LC7 marquée « programme, hors examen national ». perimetre.json (motif « méthode de dichotomie » hors programme) NON modifié : à changer par l'utilisateur s'il valide.
- limites_continuite — « prolongement par continuité » : ni écrit ni dit (hors cadre) ; seulement « quelle valeur donner à f(a) pour que f soit continue en a ? ».
- limites_continuite — puissances rationnelles x^(p/q) : gardées, 3 diapositives courtes, x > 0 toujours écrit.
- limites_continuite — clé du chapitre : limites_continuite (cadre_reference + programme_semestre1) ; perimetre.json non modifié (clé à créer si validé).
- limites_continuite — rappel des limites l1–l13 gardé en tête ; ancien cours math_ch1_limits_course_v1 remplacé par math_ch1_limites_continuite (ancien fichier gardé).
- miroir y = x : une page par cours (limites et dérivation construits en parallèle), pas un fichier partagé.
- suites_definition : voir sa section (adjacentes non traitées, escalier comme image, pas de ln/exp, kⁿ par récurrence).

## Problèmes / manques du lecteur
- SSH moalim-vps refusé aux sous-agents par le classifieur de permissions : les réactions préparées (DeepSeek) doivent être générées par la session principale (items.json dans chaque dossier maths_build/<clé>/).
- Limite de 20 agents simultanés : les agents de cours n'ont pas toujours pu lancer de sous-agents.
- Kit maths commun écrit par l'agent maths : frontend/public/media/simulations/maths/commun/ (maths-tableau.js, maths.css, exposants.js) ; brief des agents : maths_build/BRIEF_COURS_MATHS.md ; outils check_js.py, test_page.py.

## Ce qui reste

## limites_continuite
(agent du cours math_ch1_limites_continuite ; build : maths_build/limites_continuite/ — p1…p6.py, build.py, cadre.py, prog.py, verif_sims.py, items.json)
- Cours : backend/data/courses/math_ch1_limites_continuite.json (draft, concentration) : 68 diapositives, 66 questions, 17 exercices, 50 démonstrations ; 11 activités ; compétences K1–K10 (cadre LC1–LC12).
- Simulations (maths/limites-continuite-tableau/) : ouverture, approche (trou, trois_trous, deux_cotes), infini (ecart, horizontale), raccord (trois_cas, limite_image, deux_branches), usuelles (usuelles, quotient), composee (machines, limite, racine_n), projections (croissante, decroissante, borne_ouverte, tout_R, non_monotone), traversee (+ vue signe), dichotomie (etapes, probleme), miroir (aller_retour, parabole, I_et_J, tableaux, reflet, asymptotes), racine (defaire, reflet_racine, equation), calculs (24 vues, données calculs-donnees.js écrites par build.py), bilan, carte ; outils lc-outils.js. Sous-agents impossibles (limite de 20 agents) : tout écrit par l'agent.
- Cadre : chapitres.limites_continuite ajoutée (cadre.py) ; controler_cadre « cadre : OK » (191 à relire : applications numériques et exemples). programme_semestre1 : statut construit.
- verifier_texte_corpus : 219 mots signalés, surtout termes du programme (théorème, intermédiaires, dichotomie, antécédent, restriction…) et quelques mots darija d'images (ثقب remplacé, المراية, الطباشير…).
- Réactions préparées : items.json (422 réactions) laissé dans le build ; à générer par la session principale (pas de ssh pour l'agent), puis `build.py --garder-reponses` n'est pas nécessaire : poser directement avec preparer_reponses.py poser.
- Décisions en plus : dichotomie annoncée « pour les devoirs » dans la voix ; e2/e3 sans question (comme le témoin) ; f′ écrit f’ à la craie (la police n'a pas ′).
- Manques du lecteur : aucun nouveau. Disque C: plein une fois pendant le travail (ENOSPC).
- PRÊT POUR LA VOIX : oui (texte figé ; réactions préparées à générer).

## derivation_etude_fonctions
(agent du cours math_ch2_derivation_etude_fonctions ; build : maths_build/derivation_etude_fonctions/ — p1…p5.py, build.py, cadre.py, prog.py, fiches.py,
corpus_fix.py, virgules.py, verif_sims.py, items.json, gen_reponses_vps.py (copie « professeur de mathématiques », chemin /tmp/gen_rep_derivation_etude_fonctions), CONTRAT_SIMULATIONS.md)
- Cours : backend/data/courses/math_ch2_derivation_etude_fonctions.json (draft, concentration) — 64 diapositives (plan de l'exploration, une idée chacune),
  62 questions (QCM à clé, options mélangées), 18 exercices, 31 démonstrations manuscrites (barème) ; 13 activités ; compétences K1–K10 (cadre DEF1–DEF10).
  Régénérer : `python build.py [--garder-reponses]` (écrit aussi derivation-tableau/calculs-vues.js). Bilan df_fin1_bilan (acquis, 9 blocs) et carte df_fin2_carte.
- Simulations (frontend/public/media/simulations/maths/derivation-tableau/) : secante (secante, equation[a]) ; demi-tangentes (coin, verticale, sens) ;
  variations (glisse[x_p]) ; concavite (roule[x_t], x4) ; branches (verticale, horizontale, oblique, oy, ox, direction, arbre) ; position (ecart[x]) ;
  symetrie (axe[x], centre[x]) ; trace (etapes, lecture[m], etude) ; miroir (reflet[x_a], pentes[x_a], verticale, restriction) ; calculs.html (21 vues, tableaux
  de signe/variations à la craie, calculs-vues.js écrit par le build) ; bilan.html, carte.html (adaptés de suites-tableau, fiches.py). Pages des sous-agents
  vérifiées par moi : check_js ok (12 pages), test_page sur les 46 vues : moments et repères conformes, aucun hors cadre (un texte de symetrie centre corrigé).
- Vérifs : controler_cadre « cadre : OK » (145 à relire : exemples numériques et équations de droites lues « y égale … ») ; verifier_texte_corpus : plus
  aucun mot darija rare, 187 mots français rares = termes du programme et nombres (sécante, anguleux, inflexion, voisinage, quarts, demis…) gardés exprès ;
  phrases françaises > 10 mots coupées par des virgules (voix et démonstrations) ; preparer_reponses verifier : SEULEMENT « pas de piste audio » (64) et
  « réaction manquante » (401) ; verif_sims : 64/64 diapositives ok (moments, repères, encre, hors cadre) — seul « peu d'encre » sur df_fin1_bilan, normal (page 2 de l'élève vide sans bilan).
- Cadre : chapitres.derivation_etude_fonctions (cadre.py, depuis l'exploration + formules du cours, hors_cadre.mots : bijection, L'Hôpital, Rolle,
  approximation affine, division euclidienne, convexité…). programme_semestre1.json : derivation_etude_fonctions → construit, math_ch2_derivation_etude_fonctions.
- Décisions à faire valider : pas d'approximation affine chiffrée (seulement « la courbe se confond avec sa tangente ») ; asymptote oblique à partir de la droite
  donnée (une limite, pas de division euclidienne) ; dérivée de ⁿ√u gardée (une diapositive df_dv5) ; jamais « bijection/bijective » ; exemples polynômes,
  rationnelles, racines (pas ln/exp) ; fil rouge x + 1/x (tangente, double barre, tracé) et x³ − 3x (variations, concavité) ; notation f_d′(x₀), f_g′(x₀)
  (indice puis prime, pour que le lecteur et la craie rendent l'indice) ; le rappel du TVI en une diapositive (df_ec4) ; symétrie gardée (contrôle continu)
  malgré son absence au national.
- Problèmes : SSH vers le VPS refusé aux sous-agents → réactions préparées NON générées ; items.json (401 réactions) prêt dans le dossier de build. À faire par la
  session principale : copier gen_reponses_vps.py (déjà adapté) + simulation_reaction.py + reponse_eleve.py (import modifié) + items.json dans
  /tmp/gen_rep_derivation_etude_fonctions, lancer, puis `preparer_reponses.py poser …`, puis `build.py --garder-reponses`.
  Le prime ′ (U+2032) est invisible dans la police de la craie : les pages écrivent f' (constaté par deux sous-agents).
- Manques du lecteur : Formule (CourseFocusStage) ne met un indice qu'après une lettre : « f'_d » afficherait « _d » → le cours écrit f_d′ ;
  pas de commande set_parameters dans un pointage (la tangente horizontale de df_tg3 et le cas √x de df_bi4 ne sont montrés que par la variante ou par la voix).
- PRÊT POUR LA VOIX : oui pour le texte du cours et des démonstrations ; réactions préparées à générer (VPS) avant `verifier` complet.

## suites_definition
(agent du cours math_ch3_suites_numeriques ; build : maths_build/suites_definition/ — p1…p5.py, build.py, cadre.py, prog.py, verif_sims.py, vite.py, adapter_fiches.py, items.json)
- Cours : backend/data/courses/math_ch3_suites_numeriques.json (draft, concentration) — 59 diapositives (58 du plan + l4b « glisse q »),
  57 questions, 5 exercices, 39 démonstrations manuscrites (barème) ; 9 activités ; compétences K1–K8 (cadre SU1–SU11). Régénérer : `python build.py [--garder-reponses]`.
- Simulations (frontend/public/media/simulations/maths/suites-tableau/) : su-outils.js ; axe.html (questions, cases, indices, machine, arith, geom,
  serrement[u0], colonnes, image_f) ; dominos.html (principe, trou) ; arbres.html (arbres, colonne) ; nuage.html (plancher, bornee, monotonie,
  reference, fraction) ; qn.html (positif, negatif, libre[q]) ; plafond.html (monte, couple, sous_plafond[M]) ; gendarmes.html (membre, encadre[k], bande) ;
  escalier.html (escalier[u0], boite, zone, point, national) ; calculs.html (24 vues, calculs-vues.js écrit par le build) ; bilan.html (9 blocs) ; carte.html (8 branches).
- Vérifs (11 novembre, 2ᵉ agent) : check_js ok sur les 11 pages ; verif_sims : 59/59 diapositives ok, AUCUN PROBLÈME (moments, repères, encre, hors cadre) ;
  paramètres extrêmes (u0 = 0,2 / 4, q = ±2, u0 = 0 / 30, k = 0,9, M = 4) et bilan/carte (fiche, lacunes, carte complète) vus en capture : rien hors cadre ;
  controler_cadre « cadre : OK » (84 à relire : applications numériques lues « u indice n égale … ») ; preparer_reponses verifier : SEULEMENT
  « réaction manquante » (314) et « pas de piste audio » ; verifier_texte_corpus : 350 mots à revoir, presque tous des termes du programme gardés exprès
  (indice, hérédité, initialisation, auxiliaire, critère, converge, cinquièmes…) et des couleurs/verbes darija courants.
- Cadre : chapitres.suites_definition (cadre.py). programme_semestre1.json : suites_definition → construit, cours math_ch3_suites_numeriques.
- Décisions (agent maths, appliquées) : pas de suites adjacentes (aucune diapositive) ; escalier uₙ₊₁ = f(uₙ) comme construction (f1, f2 : questions
  de lecture/conjecture seulement, aucune demande de tracer, jamais « toile d’araignée ») ; pas de ln ni exp (2ᵉ agent : retiré aussi la phrase
  « avec ln et exp plus tard » de l7) ; exemple f(x) = 2x/(x + 1), national f7 = g(x) = (4x + 3)/(x + 2) ; « en déduire uₙ ≤ (2/5)ⁿu₀ » rédigé par
  récurrence (c6), le recollement seulement comme image (gendarmes membre) ; une seule fiche cadre.
- Décisions en plus : l7 = √(uₙ + 7) ; p3 = raison 1/3 ; bilan et carte sans question ; « plafond / plancher » plutôt que « gendarmes » dans les textes.
- Problèmes : SSH moalim-vps refusé par le classifieur de permissions (deux agents) → réactions préparées NON générées ; items.json régénéré
  (314 réactions) dans maths_build/suites_definition/. À faire par la session principale : gen_reponses_vps.py (copie « professeur de mathématiques »),
  puis `preparer_reponses.py poser`, puis `build.py --garder-reponses`. Serveur 8898 lent (verif_sims ≈ 30 min).
- Manques du lecteur : aucun nouveau.
- PRÊT POUR LA VOIX : non (réactions préparées à générer sur le VPS, puis poser) — le texte du cours et des démonstrations, lui, est prêt.
- 11 nov. (coordinateur) : les 314 réactions ont été écrites sur le VPS et posées dans le JSON ; voix Bodi en file. NE PLUS régénérer sans `--garder-reponses`, ne plus changer les textes dits sans le signaler au coordinateur (la voix est calculée dessus).

## fonctions_ln (exploration)
- 11 nov. : EXPLORATION FAITE (étape 1 seulement, cours non construit) → backend/data/curriculum/exploration/fonctions_ln.json. Dix profs : Driss DOTCOM, Prof fati, maths variés, Aderdour, Math_houara, Ghazouani, MedBrahmi, Moussaoui, biadmostafa, LowDiscovery (Amine Hidane écarté : bac Lettres). Cadre LN1–LN10 (1.2.14–1.2.19, 1.2.22), plan K1–K9 (rappels 3–4 chacune), 53 diapositives (28 prédictions), 5 séances (dernière à 2 blocs). Décisions à valider : eʳ comme nombre seulement (exp au chapitre suivant) ; logarithme de base a exclu ; log décimal (2 diapos) et systèmes (1 diapo) gardés malgré 0 sujet ; lim ln(1+x)/x et ln x/(x−1) montrées comme nombre dérivé ; ln|u| et u'/u gardés ; intégrales/suites des nationaux renvoyées ; ln(ab) montrée (a2) sans être notée. Problème : disque C: à 0 octet pendant ~45 min → images de biadmostafa et des limites de Math_houara non prises ; dossier de travail effacé. Rien d'autre du dépôt modifié.

## primitives
(agent du cours math_ch4_primitives ; build : maths_build/primitives/ — p1…p4.py, build.py, outils.py (+ CALC, D), ajouts.py, cadre.py, prog.py, verif_sims.py, items.json, items_blocs.json, demos_blocs.json, CONTRAT_SIMULATIONS.md)
- Cours : backend/data/courses/math_ch4_primitives.json (draft, concentration) — 44 diapositives (préfixe pr_), 44 questions, 66 exercices, 72 démonstrations
  manuscrites (barème) ; 10 activités ; compétences K1–K8 (cadre PR1–PR8). Régénérer : `python build.py --garder-reponses` (garde réponses, séances, rappels,
  prédictions ; vérifié identique) ; écrit aussi primitives-tableau/calculs-vues.js (18 vues de calculs).
- Méthode des blocs : 5 séances / 14 blocs (S5 à 2 blocs : x1–x3 ; x4 + bilan + carte), 28 rappels (3–4 par compétence), 16 prédictions / 44
  (ajouts.py → methode_blocs/ajouts/math_ch4_primitives.json, `blocs.py base` puis `appliquer`).
- Simulations (frontend/public/media/simulations/maths/primitives-tableau/) : ouverture (carte, plus_tard) ; marche (marche) ; famille (famille[k], point[k]) ;
  intervalle (trou) ; pente (pente[x]) ; tableau (derivees, envers, puissance, inverse, racine, trigo) ; cercle (cercle, ax_plus_b) ; bulle (bulle, facteur, trois) ;
  organigramme (organigramme) ; calculs.html (18 vues) ; bilan.html (8 blocs, page 2 de l'élève) ; carte.html (centre + 9 branches). Retouche famille/point :
  l'essai pâlit avec la famille. bilan/carte refaits pour tout garder au-dessus de y = 360.
- Vérifs (11 nov.) : check_js ok (12 pages + calculs-vues.js) ; verif_sims 44/44 « AUCUN PROBLÈME » (moments, repères, encre, hors cadre) ; test_page sur
  les 18 vues de calculs (rien sous y = 322) ; controler_cadre « cadre : OK » (219 à relire : u = …, exemples, lectures de formules) ; blocs.py verifier
  « blocs : OK » (avis : S5 à 2 blocs) ; preparer_reponses verifier : SEULEMENT « réaction manquante » et « pas de piste audio » ; verifier_texte_corpus :
  238 mots à revoir = termes du programme (primitiver, bulle, organigramme, tiers, quarts…) et darija courante, gardés.
- Cadre : chapitres.primitives ajoutée (cadre.py). programme_semestre1.json : primitives → construit, math_ch4_primitives. perimetre.json non modifié.
- Décisions à valider : constante k ; 1 + tan²x « pour mémoire » (une diapositive) ; ln, exp, intégrale seulement annoncés « plus tard » ; lien graphique f/F
  en 2 diapositives (K8 sans exercice national) ; (u′v − uv′)/v² en une diapositive ; pas de fonctions par morceaux ni de linéarisation ; « la bulle » pour
  faire voir u′ ; ℝ* seulement écrit pour être barré (e2).
- Réactions préparées : NON générées (pas de ssh) : items.json (582 réactions) et items_blocs.json (91) dans le build, 0 démonstration nouvelle de bloc.
  À faire par la session principale : VPS puis `preparer_reponses.py poser`, puis `build.py --garder-reponses`.
- Manques du lecteur : aucun nouveau. Disque : pas de reste ; captures effacées ; serveur 8898 arrêté.
- PRÊT POUR LA VOIX : oui pour le texte (cours, démonstrations, blocs) ; réactions préparées à générer.

## operations_formes (exploration)
- 11 nov. : EXPLORATION FAITE (étape 1 seulement, cours non construit) → backend/data/curriculum/exploration/operations_formes.json (mêmes clés que fonctions_ln.json). Dix profs : Driss DOTCOM (m9W5z2SGo1I), Mouad Tahiri (fQ9DAZJpXdA, en classe), Prof fati (jMQp1IirBAU), mostapha maths (M6cl9HYFlIA), bacfacile/Benfath (4bp69jLvsw4), Aderdour (Q2ZMGqayHD0), Math & Phys (dIns8ihVX8M), Ghazouani (xTNiTr3vFXA), MedBrahmi (Tfe7Wn6lq9I), maths variés (x9KP-xDiziY, correction 2023 N). 31 images en flux (aucun téléchargement), 1 232 commentaires, 20 nationaux relus (complexes dans 20/20, forme trigonométrique 17/20).
- Cadre NC1–NC10 (2.4.1, 2.4.2, 2.4.4, 2.4.7) ; plan K1–K8 (rappels 3–4) ; 48 diapositives (23 prédictions, au moins une par bloc), 4 séances × 3 blocs × 4 ; 7 notions complexes, 15 visuels (v_i quart de tour, v_plan, v_vecteur, v_conjugue, v_module, v_argument, v_tableau_angles, v_trig, v_produit, v_moivre, v_alignement…) ; dossier proposé maths/operations-formes-tableau/.
- Décisions à valider : partie 1 = algébrique, quotient, affixe (point, vecteur, milieu), conjugué, module/distance, argument, forme trigonométrique, produit/quotient, Moivre, alignement (quotient réel) ; exponentielle, Euler, équation à Δ < 0 (14 sujets/20), rotation/translation/homothétie, angle (AB, AC), triangles, ensembles de points → partie 2 ; jamais [r ; θ] ; pas d'inégalité triangulaire ni d'arctan (corrigé 2017 N du dépôt l'utilise) ; calculatrice seulement pour vérifier. perimetre.json NON modifié (operations_formes y contient Euler, linéarisation, équations : à déplacer si validé) ; prérequis identites_remarquables proposé, non ajouté.
- Limites : 5 vidéos sans transcription (lues par le tableau) ; Prof fati par tranches ; découpage officiel partie 1/2 non lu dans un texte du ministère. Rien d'autre du dépôt modifié ; dossier de travail effacé.

## fonctions_ln (cours)
- 11 nov. (agent maths) : cours math_ch5_fonctions_ln lancé (un sous-agent opus), d'après exploration/fonctions_ln.json ; build maths_build/fonctions_ln/.
