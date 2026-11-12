# Brief — écrire une partie du cours phys_ch6_dipole_RC (« Dipôle RC »)

Tu écris UN fichier de contenu `outils/cours/notes/cours/dipole_RC_build/pN.py` (N donné dans ta mission) et UN fichier
`outils/cours/notes/cours/dipole_RC_build/blocs_sN.json` (les 3 blocs de ta séance). Rien d'autre. Messages en français simple.
Travaille depuis la racine du dépôt /home/user/tutorAI. Pas de commit, pas de push, pas de git checkout/stash/reset, pas de sous-agent.

## À lire d'abord
1. `.agents/skills/cours-concentration/SKILL.md` (en entier), `.agents/skills/voix-du-cours/SKILL.md` section 1 (texte parlé),
   `.agents/skills/professeur/SKILL.md` (règles), `outils/cours/notes/cours/methode_blocs/BRIEF_AGENTS.md` (blocs : cahier, retrouver, exercice).
2. L'exploration : `backend/data/curriculum/exploration/dipole_RC.json` — surtout `plan.diapositives` (TES diapositives : id, title, lead,
   marche, visuel, question, prediction, competences, demonstration), `notions_complexes`, `pieges`, `erreurs_examen`, `analogies_validees`,
   `a_ne_pas_dire`, `redaction_nationale`, `cas_types`, `valeurs_reperes`, `questions_eleves`.
3. Le cadre : `backend/data/curriculum/cadre_reference_2bac_pc.json` → `chapitres.dipole_RC` (formules `ecriture`, `hors_cadre.mots` INTERDITS).
4. Le contrat des simulations : `outils/cours/notes/cours/dipole_RC_contrat_simulations.md` (pages, vues, moments, repères EXACTS).
   Les tables MOMENTS / REPERES de `outils/cours/notes/cours/dipole_RC_build/outils.py` en sont la copie : n'utilise que ceux-là.
5. Le MODÈLE (forme, ton, densité) : `outils/cours/notes/cours/radioactivite_build/p1.py` (lis 3-4 diapositives) et ses outils
   (S, vis, Q, DEMO, EX, VF, PU, R, C, SP dans `outils/cours/notes/cours/dipole_RC_build/outils.py`, même API).

## Règles
- Une diapositive par entrée de `plan.diapositives` qui t'est confiée, DANS L'ORDRE, id = `rc_<id du plan>_<un mot>` (ex. `rc_c4_charge`).
  Une seule idée nouvelle par diapositive. Compétence = la PREMIÈRE de la liste `competences` du plan (S(..., comp, ...)).
  `slide_type` parmi situation | concept | explanation | application | evaluation.
- Chaque diapositive : title, lead, 3-4 bullets, student_trace (= cahier, écrit comme le barème, formule du cadre), visuel `vis("page.html?vue=…")`
  (ou `figures.html?fig=…`), `fr` (français parlé) et `mixed` (darija simple + termes du programme en français, règles voix-du-cours :
  AUCUN chiffre, aucun symbole = / + × → ( ) % ², nombres et unités EN LETTRES, « u C », « dé u C sur dé t », « tau », « R C »,
  phrase entièrement française > 10 mots coupée par des virgules ; pas de tachkil), une question `Q(...)` (3 options, bonne réponse PAS
  toujours au même rang, `prediction=True` si le plan dit prediction), `pointage=[PU("extrait exact de mixed", "moment"), R("extrait", "repère")]`
  dans l'ordre de la voix, et `centre=[("formule", "extrait de mixed")]` quand une formule naît.
- Toute question ou exercice de calcul / « établis / montre / vérifie / trouve / détermine / déduis / combien / que vaut » porte
  `DEMO(parole, [(ligne écrite, extrait exact de parole), ...])` (style « la relation: … l'application numérique: … le résultat: … »).
  Vérifie CHAQUE calcul avec python.
- Les diapositives d'application et de national portent 1 à 3 exercices `EX(...)` / `VF(...)` niveau national (avec DEMO si calcul).
- Écrit : formules exactement comme le cadre (`q = C·u_C`, `i = C·du_C/dt`, `RC·du_C/dt + u_C = E`, `u_C(t) = E(1 − e^(−t/τ))`, `τ = R·C`,
  `E_e = ½·C·u_C²`…), exponentielle écrite `e^(−t/τ)`, virgule décimale, unités (µF, kΩ, ms). Jamais « I₀ = q/C ».
  Orientation : en décharge on garde le sens de i de la charge, i = C·du_C/dt < 0.
- Mots INTERDITS partout : ceux de `hors_cadre.mots` (filtre, déphasage, impédance, permittivité, séparation des variables, intégration…).
- Valeurs des simulations (à citer telles quelles) : courbe par défaut E = 12 V, R = 1 kΩ, C = 220 µF, τ = 0,22 s ; nationaux du contrat.
- Contrôle : `python3 outils/cours/notes/cours/dipole_RC_build/check_part.py pN` doit finir par « AUCUNE ERREUR » (il vérifie mots
  exacts, ordre, moments, repères, voix sans chiffre/symbole, mots interdits, démonstrations). Corrige jusqu'à zéro.

## blocs_sN.json (ta séance = 3 blocs de 4 diapositives, découpage `plan.seances` de l'exploration)
Forme exacte (JSON valide, écrit avec l'outil Write) :
{"seance": {"id": "rc_sN", "titre": "Séance N — …", "blocs": [
   {"id": "rc_sN_b1", "titre": "…", "slide_ids": [4 ids de tes diapositives, dans l'ordre],
    "cahier": [{"texte": "…"}, …2 à 4 lignes reprises des student_trace…],
    "retrouver": {"prompt": "Cahier fermé : …", "attendu": "<formule ou définition EXACTE du cadre>", "competence_id": "C?"},
    "exercice": {…}}, … ]},
 "predictions": [ids de tes diapositives dont la question a prediction=True]}
`exercice` : reprend un exercice d'une diapositive du bloc s'il y en a un (`{"type", "reprend": "<slide_id>/e<i>", "prompt", "options"
(= choices), "correct", "explanation"}`, un vrai/faux garde `statements`), sinon un QCM court niveau national (`options` 3, `correct`, `explanation`),
avec `demonstration: {"parole", "lignes": [{"texte", "mot"}]}` s'il demande un calcul (parole aux règles de la voix, chaque `mot` extrait exact).
Au moins une prédiction par bloc.

## Rapport final (court)
ids écrits, nombre de questions / prédictions / exercices / démonstrations, sortie finale de check_part, choix à faire valider.
