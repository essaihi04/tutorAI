# Brief — exploration de etat_equilibre (cours phys_ch12_etat_equilibre)

Chapitre 12 de physique-chimie (chimie) : « État d'équilibre d'un système chimique » (2BAC PC BIOF, Maroc).
Travaille depuis /home/user/tutorAI. Messages en français simple. Pas de commit, pas de push, pas de git checkout/stash/reset, pas de sous-agent.
Ton dossier : `outils/cours/notes/cours/etat_equilibre_build/` (préfixe des diapositives : `ee_`).
Le chapitre précédent est DÉJÀ construit : `backend/data/courses/phys_ch11_transformations_deux_sens.json` (Brønsted, pH, τ, deux sens, état
d'équilibre dynamique, conductimétrie, dilution). Ici on ne refait pas ces notions : on les rappelle en 1-2 diapositives et on construit dessus.

## Contenu attendu du chapitre (à confirmer par les nationaux et perimetre.json)
Quotient de réaction Qr d'une réaction en solution aqueuse (aA + bB ⇌ cC + dD : Qr = [C]^c·[D]^d / ([A]^a·[B]^b) ; l'eau solvant et les solides
n'y figurent pas ; concentrations en mol/L, Qr sans unité) ; Qr,i dans l'état initial ; Qr,éq à l'équilibre ; constante d'équilibre K = Qr,éq,
qui ne dépend que de la température (pas de l'état initial) ; K de la réaction inverse = 1/K ; détermination de K par conductimétrie et par le pH ;
relation entre K, C et τ pour un acide dans l'eau (K = C·τ²/(1 − τ)) ; facteurs dont dépend τ : K (nature de la réaction) et état initial
(concentration). Ka, pKa, Ke, produit ionique, autoprotolyse, prédominance, Henderson : chapitre SUIVANT (acides_bases), à renvoyer.
Critère d'évolution spontanée (comparer Qr,i à K pour prévoir le sens) : vérifie avec perimetre.json et les nationaux s'il appartient à ce chapitre
ou au chapitre « évolution spontanée » (piles, semestre 2) ; tranche et écris la décision.

## Ce que tu produis (tout, dans cet ordre)
1. `etat_equilibre_build/nationaux.md` : ce que demandent les nationaux PC 2016-2025 sur CE chapitre. Source :
   `backend/data/exams/physique/<année>-<session>/` (exam.json = énoncé + corrigé ; extraction.json = texte officiel + barème ; assets/*.png).
   Cherche : quotient de réaction, Qr,éq, constante d'équilibre K, expression de K en fonction de C et τ (ou de pH et C, ou de σ), K par conductimétrie,
   influence de l'état initial / de la dilution sur τ et pas sur K. Par session : questions, barème, valeurs, corrigé recalculé avec python ;
   erreurs du dépôt relevées. Note ce qui appartient au chapitre SUIVANT (Ka, pKa, Ke…) : on le renvoie. Regarde aussi
   `outils/cours/notes/cours/transformations_deux_sens_build/nationaux.md` (déjà fait pour le chapitre 11 : beaucoup de sessions enchaînent τ puis K).
2. `outils/cours/notes/cours/etat_equilibre_contrat_simulations.md` : contrat des simulations à la craie, dossier
   `frontend/public/media/simulations/chimie/etat-equilibre-tableau/` (kit commun.js, exposants.js, et une feuille `ee.css`
   copiés de `chimie/transformations-deux-sens-tableau/` (renomme tds.css en ee.css) — copie-les toi-même). Pages (4 à 6 html + bilan.html + carte.html
   + figures.html si des nationaux ont une figure), vues `?vue=`, moments et repères EXACTS, données numériques communes (exemples chiffrés vérifiés
   avec python : par ex. acide éthanoïque C = 1,0·10⁻² mol/L, pH = 3,4 → τ ≈ 4 %, K ≈ 1,6·10⁻⁵ ; même acide à 1,0·10⁻³ mol/L → τ plus grand,
   même K ; une mesure conductimétrique → K ; un Qr calculé à l'état initial et à l'équilibre), section finale « ## Diapositives servies »
   (une ligne par diapositive : `<id> <page>?vue=<vue>`).
   MODÈLE à suivre exactement pour la forme : `outils/cours/notes/cours/transformations_deux_sens_contrat_simulations.md`.
   IMPORTANT (défaut corrigé dans le moteur) : le moteur de commun.js / des pages garde, pour une étape M.etape dessinée en plusieurs morceaux,
   la durée la plus longue (Math.max) ; prends le moteur des pages de transformations-deux-sens-tableau (déjà corrigé).
3. `explo_a.py`, `explo_b.py`, `explo.py` → écrit `backend/data/curriculum/exploration/etat_equilibre.json`.
   MODÈLE : `outils/cours/notes/cours/transformations_deux_sens_build/explo.py`, `explo_a.py`, `explo_b.py` (mêmes clés, mêmes vérifications adaptées :
   ordre des ids, séances, champs, prédictions ≥ 1 sur 3 et ≥ 1 par bloc, visuels = « Diapositives servies », rappels 3–4 par compétence de types
   variés, toutes les capacités du cadre couvertes, mots hors cadre absents, nombres recalculés). Lis aussi
   `.agents/skills/exploration-de-cours/SKILL.md` (structure attendue) et `backend/data/curriculum/exploration/transformations_deux_sens.json`.
   Plan : 36 diapositives = 3 séances × 3 blocs × 4 diapositives (ouverture + carte au début, bilan `bl` + carte `cr` à la fin de la séance 3),
   compétences C1…C6 environ, chacune avec `cadre_ids`, `dit`, `rappels`. Une seule idée nouvelle par diapositive ; au moins 13 prédictions.
   Ids du plan courts (2 caractères comme o1, q1, k1…, bl, cr) et parties nommées : les parties seront écrites par 3 agents (une séance chacun) :
   donne dans l'exploration, pour chaque séance, la liste des parties (titre « I. … ») et leurs ids.
   Cadre (`CADRE`) : capacités EE1… (provisoires), formules (`ecriture` exacte + `dit` en lettres pour la voix), mots-clés, `hors_cadre.mots`
   (au moins : Ka, pKa, Ke, produit ionique, autoprotolyse, Henderson, diagramme de prédominance, indicateur coloré, activité, Le Chatelier, loi de
   modération, Guldberg, enthalpie, et « critère d'évolution spontanée » si tu le renvoies au semestre 2 — vérifie avec perimetre.json ; attention :
   le contrôle cherche ces mots dans le texte, choisis des mots qui ne cassent pas les mots permis), valeurs_reference.
   Ancien cours : vérifie `backend/data/courses/` (il ne semble pas y en avoir), dis-le dans `cours_existant`.
   VIDÉOS NON AUDITÉES : YouTube est bloqué depuis le cloud, ne tente pas yt-dlp ; appuie-toi sur les nationaux et perimetre.json, et écris-le
   dans `_note`, `sources`, `limites_de_l_exploration`, `verification.dix_professeurs`.
4. `cadre_ee.py` : copie de `transformations_deux_sens_build/cadre_tds.py` qui ajoute la SEULE clé `chapitres.etat_equilibre` à
   `backend/data/curriculum/cadre_reference_2bac_pc.json` (relit, ajoute, réécrit aussitôt). Lance-le.

## Contrôles
`python3 outils/cours/notes/cours/etat_equilibre_build/explo.py` doit réussir (toutes les assertions). Nombres vérifiés avec python.

## Rapport final (court, ≤ 25 lignes)
Sessions où le chapitre tombe (questions, points), pages/vues du contrat, ids du plan avec les séances et les titres des parties, compétences,
décisions à faire valider, erreurs du dépôt relevées.
