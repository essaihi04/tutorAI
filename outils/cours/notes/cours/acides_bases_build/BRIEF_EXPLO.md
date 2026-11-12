# Brief — exploration de acides_bases (cours phys_ch13_acides_bases)

Chapitre 13 de physique-chimie (chimie) : « Transformations liées aux réactions acide-base » (2BAC PC BIOF, Maroc).
Travaille depuis /home/user/tutorAI. Messages en français simple. Pas de commit, pas de push, pas de git checkout/stash/reset, pas de sous-agent.
Ton dossier : `outils/cours/notes/cours/acides_bases_build/` (préfixe des diapositives : `ab_` ; outils.py, check_part.py, verif_sims.js y sont déjà copiés
et adaptés : ne les change pas sauf erreur évidente).
Les deux chapitres précédents sont DÉJÀ construits : `backend/data/courses/phys_ch11_transformations_deux_sens.json` (Brønsted, pH, τ, deux sens,
conductimétrie, dilution) et `backend/data/courses/phys_ch12_etat_equilibre.json` (Qr, Qr,éq, K, K = C·τ²/(1 − τ), τ dépend de K et de C).
Ici on ne refait pas ces notions : on les rappelle en 1-2 diapositives et on construit dessus. Ces deux cours RENVOYAIENT à ce chapitre :
Ke, autoprotolyse, Ka, pKa, τ d'une base (il faut Ke), K d'une réaction acide-base avec les Ka, prédominance, indicateur coloré.

## Contenu attendu (à confirmer par les nationaux et perimetre.json, clés `acides_bases` ET `dosage`)
Autoprotolyse de l'eau, produit ionique Ke = [H₃O⁺]·[HO⁻] = 10⁻¹⁴ à 25 °C, pKe = 14 ; solutions acide / neutre / basique ; pH d'une solution de
base (HO⁻) par Ke ; τ d'une base dans l'eau ; constante d'acidité Ka = [A⁻]_éq·[H₃O⁺]_éq/[AH]_éq, pKa = −log Ka ; Ka de NH₄⁺/NH₃, H₂O/HO⁻, H₃O⁺/H₂O ;
comparer des acides (même C : plus Ka grand, plus τ grand, plus pH petit) et des bases ; K d'une réaction acide-base K = Ka₁/Ka₂ (= 10^(pKa₂ − pKa₁)) ;
pH = pKa + log([A⁻]_éq/[AH]_éq) (sans nommer Henderson) ; domaines de prédominance ; diagramme de distribution ; indicateur coloré (zone de virage) ;
DOSAGE acido-basique (clé `dosage` de perimetre.json) : réaction de dosage (rapide, totale, unique), équivalence C_A·V_A = C_B·V_BE, courbe pH = f(V_B),
méthode des tangentes parallèles, pH à l'équivalence (acide fort/base forte = 7 ; acide faible/base forte > 7…), demi-équivalence pH = pKa,
choix de l'indicateur coloré, dosage conductimétrique (rupture de pente) si les nationaux le demandent.
Le DOSAGE tombe presque à chaque national : il doit être bien couvert. Si les nationaux et le programme montrent que le dosage est un chapitre
à part dans programme_semestre1.json, dis-le et tranche (proposition : il reste DANS ce cours, partie finale, car programme_semestre1 n'a pas de clé dosage).
Critère d'évolution spontanée (Qr,i comparé à K) : semestre 2 (piles), toujours renvoyé.

## Ce que tu produis (tout, dans cet ordre)
1. `acides_bases_build/nationaux.md` : ce que demandent les nationaux PC 2016-2025 sur CE chapitre (Ke, pH d'une base, Ka, pKa, K = Ka₁/Ka₂,
   prédominance, indicateur, dosage, équivalence, demi-équivalence, courbe, tangentes). Source : `backend/data/exams/physique/<année>-<session>/`
   (exam.json = énoncé + corrigé ; extraction.json = texte officiel + barème ; assets/*.png). Par session : questions, barème, valeurs, corrigé
   recalculé avec python ; erreurs du dépôt relevées ; figures utiles (courbes de dosage : chemin du png) pour figures.html.
   Regarde aussi `outils/cours/notes/cours/transformations_deux_sens_build/nationaux.md` et `etat_equilibre_build/nationaux.md` (questions renvoyées ici).
2. `outils/cours/notes/cours/acides_bases_contrat_simulations.md` : contrat des simulations à la craie, dossier
   `frontend/public/media/simulations/chimie/acides-bases-tableau/` (copie toi-même commun.js, exposants.js et la feuille de style de
   `chimie/etat-equilibre-tableau/` ; renomme ee.css en ab.css). Pages (5 à 7 html + figures.html si des nationaux ont une figure + bilan.html + carte.html),
   vues `?vue=`, moments et repères EXACTS (noms en minuscules, chiffres et _ ), poignées (si utiles : pH, V_B…), données numériques communes (exemples
   chiffrés vérifiés avec python : ex. acide éthanoïque pKa = 4,8 ; NH₄⁺/NH₃ pKa = 9,2 ; un dosage acide éthanoïque C_A = 1,0·10⁻² mol/L, V_A = 20 mL
   par la soude C_B = 1,0·10⁻² mol/L → V_BE = 20 mL, pH_E ≈ 8,4, demi-équivalence pH = 4,8 ; une courbe calculée réellement), section finale
   « ## Diapositives servies » (une ligne par diapositive : `<id> <page>?vue=<vue>`).
   MODÈLE à suivre exactement pour la forme : `outils/cours/notes/cours/etat_equilibre_contrat_simulations.md`.
   IMPORTANT : le moteur des pages doit garder, pour une étape M.etape dessinée en plusieurs morceaux, la durée la plus longue (Math.max) ;
   le contrat l'impose (prends le moteur des pages de etat-equilibre-tableau).
   Vérifie que outils.py lit bien tes moments et repères : `python3 -c "import sys; sys.path.insert(0,'outils/cours/notes/cours/acides_bases_build'); import outils; print(outils.MOMENTS, outils.REPERES)"`
   (après avoir écrit l'exploration et le cadre, car outils.py lit les deux).
3. `explo_a.py`, `explo_b.py`, `explo.py` → écrit `backend/data/curriculum/exploration/acides_bases.json`.
   MODÈLE : `outils/cours/notes/cours/etat_equilibre_build/explo.py`, `explo_a.py`, `explo_b.py` (mêmes clés, mêmes vérifications adaptées :
   ordre des ids, séances, champs, prédictions ≥ 1 sur 3 et ≥ 1 par bloc, visuels = « Diapositives servies », rappels 3–4 par compétence de types
   variés, toutes les capacités du cadre couvertes, mots hors cadre absents, nombres recalculés). Lis aussi
   `.agents/skills/exploration-de-cours/SKILL.md` et `backend/data/curriculum/exploration/etat_equilibre.json`.
   Plan : 48 diapositives = 4 séances × 3 blocs × 4 diapositives (ouverture + carte au début, bilan `bl` + carte `cr` à la fin de la séance 4) ;
   compétences C1…C8 environ, chacune avec `cadre_ids`, `dit`, `rappels`. Une seule idée nouvelle par diapositive ; au moins 16 prédictions.
   Ids du plan courts (2 caractères, ex. o1, r1, w1, a1, p1, d1, n1, bl, cr) et parties nommées « I. … » ; les parties seront écrites par 4 agents
   (une séance chacun) : donne, pour chaque séance, la liste des parties (titre) et leurs ids, et le découpage en 3 blocs de 4.
   Cadre (`CADRE`) : capacités AB1… (provisoires), formules (`ecriture` exacte + `dit` en lettres pour la voix), mots-clés, `hors_cadre.mots`
   (au moins : Henderson, Hasselbalch, Flood, Lewis, Arrhenius, Ostwald, degré d'ionisation, coefficient de dissociation, activité chimique,
   pouvoir tampon, Le Chatelier, dosage potentiométrique, critère d'évolution spontanée, évolution spontanée, enthalpie ; attention : le contrôle
   cherche ces mots dans le texte, choisis des mots qui ne cassent pas les mots permis — ex. pas « activité » seul si cela gêne), valeurs_reference.
   Ancien cours : vérifie `backend/data/courses/` (ancien chem_* ?), dis-le dans `cours_existant`.
   VIDÉOS NON AUDITÉES : YouTube est bloqué depuis le cloud, ne tente pas yt-dlp ; appuie-toi sur les nationaux et perimetre.json, et écris-le
   dans `_note`, `sources`, `limites_de_l_exploration`, `verification.dix_professeurs`.
4. `cadre_ab.py` : copie de `etat_equilibre_build/cadre_ee.py` qui ajoute la SEULE clé `chapitres.acides_bases` à
   `backend/data/curriculum/cadre_reference_2bac_pc.json` (relit, ajoute, réécrit aussitôt). Lance-le.
5. `BRIEF_PARTIES.md` et `BRIEF_SIMS.md` pour les agents suivants : copies adaptées de `etat_equilibre_build/BRIEF_PARTIES.md` et `BRIEF_SIMS.md`
   (4 parties p1…p4 / blocs_s1…s4.json, une séance chacune, avec le tableau des variables PARTIEn exportées, les titres des séances et le
   découpage des blocs ; formules du cadre ; mots interdits ; dit de la voix). Et `build.py`, `ajouts.py`, `prog.py`, `refaire.sh` adaptés
   (copies de etat_equilibre_build, 4 séances, titres des parties, id phys_ch13_acides_bases, lesson_match, catalog) — sans les lancer
   (les p*.py n'existent pas encore).

## Contrôles
`python3 outils/cours/notes/cours/acides_bases_build/explo.py` doit réussir (toutes les assertions). Nombres vérifiés avec python.

## Rapport final (court, ≤ 30 lignes)
Sessions où le chapitre tombe (questions, points), pages/vues du contrat (et quelles pages confier à quels agents de simulation : 4 agents au plus,
une liste de pages par agent), ids du plan avec les séances et les titres des parties, compétences, décisions à faire valider, erreurs du dépôt relevées.
