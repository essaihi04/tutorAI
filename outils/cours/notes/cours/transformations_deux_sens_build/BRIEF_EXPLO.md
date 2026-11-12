# Brief — exploration de transformations_deux_sens (cours phys_ch11_transformations_deux_sens)

Chapitre 11 de physique-chimie (chimie) : « Transformations chimiques s'effectuant dans les deux sens » (2BAC PC BIOF, Maroc).
Travaille depuis /home/user/tutorAI. Messages en français simple. Pas de commit, pas de push, pas de git checkout/stash/reset.
Ton dossier : `outils/cours/notes/cours/transformations_deux_sens_build/` (préfixe des diapositives : `td_`).

## Ce que tu produis (tout, dans cet ordre)
1. `transformations_deux_sens_build/nationaux.md` : ce que demandent les nationaux PC 2016-2025 sur CE chapitre. Source :
   `backend/data/exams/physique/<année>-<session>/` (exam.json = énoncé + corrigé ; extraction.json = texte officiel + barème ; assets/*.png).
   Cherche : couple acide/base, Brønsted, pH, pH-mètre, [H₃O⁺] = 10^(−pH), réaction d'un acide (ou d'une base) avec l'eau, tableau d'avancement,
   x_f, x_max, taux d'avancement final τ, réaction totale / limitée, conductimétrie pour trouver [H₃O⁺] ou τ (σ = Σλᵢ[Xᵢ]), influence de la
   dilution sur τ, état d'équilibre dynamique, estérification/hydrolyse comme exemple de réaction limitée. Par session : questions, barème, valeurs,
   corrigé recalculé avec python ; erreurs du dépôt relevées. Note bien ce qui appartient aux chapitres SUIVANTS (Qr, K → etat_equilibre ;
   Ke, Ka, pKa, prédominance → acides_bases) : on le renvoie, on ne l'enseigne pas ici.
2. `outils/cours/notes/cours/transformations_deux_sens_contrat_simulations.md` : contrat des simulations à la craie, dossier
   `frontend/public/media/simulations/chimie/transformations-deux-sens-tableau/` (kit commun.js, exposants.js, et une feuille `tds.css`
   copiés de `chimie/cinetique-tableau/` — copie-les toi-même). Pages (4 à 6 html + bilan.html + carte.html), vues `?vue=`, moments et repères EXACTS,
   données numériques communes (exemples chiffrés vérifiés avec python : par ex. acide éthanoïque C = 1,0·10⁻² mol/L, pH ≈ 3,4, τ ≈ 4 % ;
   acide chlorhydrique même C, pH = 2,0, τ = 1 ; une mesure conductimétrique ; un effet de la dilution), section finale « ## Diapositives servies »
   (une ligne par diapositive : `<id> <page>?vue=<vue>`), et une figure pour chaque national repris s'il y en a (page figures.html?fig=…, ou pas).
   MODÈLE à suivre exactement pour la forme : `outils/cours/notes/cours/cinetique_contrat_simulations.md`.
3. `explo_a.py`, `explo_b.py`, `explo.py` → écrit `backend/data/curriculum/exploration/transformations_deux_sens.json`.
   MODÈLE : `outils/cours/notes/cours/cinetique_build/explo.py`, `explo_a.py`, `explo_b.py` (mêmes clés, mêmes vérifications adaptées :
   ordre des ids, séances, champs, prédictions ≥ 1 sur 3 et ≥ 1 par bloc, visuels = « Diapositives servies », rappels 3–4 par compétence de types
   variés, toutes les capacités du cadre couvertes, mots hors cadre absents, nombres recalculés). Lis aussi
   `.agents/skills/exploration-de-cours/SKILL.md` (structure attendue) et `backend/data/curriculum/exploration/cinetique.json`.
   Plan : 36 diapositives = 3 séances × 3 blocs × 4 diapositives (ouverture + carte au début, bilan `bl` + carte `cr` à la fin de la séance 3),
   compétences C1…C6 environ, chacune avec `cadre_ids`, `dit`, `rappels`. Une seule idée nouvelle par diapositive ; au moins 13 prédictions.
   Cadre (`CADRE`) : capacités TD1… (provisoires), formules (`ecriture` exacte + `dit` en lettres pour la voix), mots-clés, `hors_cadre.mots`
   (au moins : Qr, quotient de réaction, constante d'équilibre, Ka, pKa, Ke, produit ionique, activité, Lewis, Arrhenius, degré d'ionisation,
   Ostwald, diagramme de prédominance… — vérifie ce qui est vraiment hors de CE chapitre avec perimetre.json clé acides_bases), valeurs_reference.
   Ancien cours : il n'y a pas d'ancien cours de ce chapitre (vérifie `backend/data/courses/`), dis-le dans `cours_existant`.
   VIDÉOS NON AUDITÉES : YouTube est bloqué depuis le cloud, ne tente pas yt-dlp ; appuie-toi sur les nationaux et perimetre.json, et écris-le
   dans `_note`, `sources`, `limites_de_l_exploration`, `verification.dix_professeurs`.
4. `cadre_tds.py` : copie de `cinetique_build/cadre_cin.py` qui ajoute la SEULE clé `chapitres.transformations_deux_sens` à
   `backend/data/curriculum/cadre_reference_2bac_pc.json` (relit, ajoute, réécrit aussitôt). Lance-le.

## Contrôles
`python3 outils/cours/notes/cours/transformations_deux_sens_build/explo.py` doit réussir (toutes les assertions). Nombres vérifiés avec python.

## Rapport final (court, ≤ 25 lignes)
Sessions où le chapitre tombe (questions, points), pages/vues du contrat, ids du plan avec les séances, compétences, décisions à faire valider,
erreurs du dépôt relevées.
