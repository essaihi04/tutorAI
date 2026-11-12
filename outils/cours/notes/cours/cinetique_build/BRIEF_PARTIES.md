# Brief — écrire une partie du cours phys_ch10_cinetique (« Suivi temporel d'une transformation chimique, vitesse de réaction »)

Tu écris UN fichier de contenu `outils/cours/notes/cours/cinetique_build/pN.py` (N donné dans ta mission) et UN fichier
`outils/cours/notes/cours/cinetique_build/blocs_sN.json` (les 3 blocs de ta séance). Rien d'autre. Messages en français simple.
Travaille depuis la racine du dépôt /home/user/tutorAI. Pas de commit, pas de push, pas de git checkout/stash/reset, pas de sous-agent.
Les simulations sont écrites EN MÊME TEMPS par d'autres agents : n'utilise que les vues, moments et repères du contrat
(copiés dans les tables MOMENTS / REPERES de `cinetique_build/outils.py`).

## Répartition (fixe : build.py importe exactement ces noms)
| Fichier | Séance | Diapositives du plan (dans l'ordre) | Variables exportées |
|---|---|---|---|
| p1.py + blocs_s1.json | 1 | o1 o2 · m1 m2 m3 · a1 … a7 (12) | `PARTIE1` = o1 o2 ; `PARTIE2` = m1 m2 m3 ; `PARTIE3` = a1…a7 |
| p2.py + blocs_s2.json | 2 | g1 … g6 · p1 … p6 (12) | `PARTIE4` = g1…g6 ; `PARTIE5` = p1…p6 |
| p3.py + blocs_s3.json | 3 | v1 … v4 · v5 … v8 · h1 … h4 (12) | `PARTIE6` = v1…v4 ; `PARTIE7` = v5…v8 ; `PARTIE8` = h1…h4 |
| p4.py + blocs_s4.json | 4 | n1 … n8 · r1 r2 · bl cr (12) | `PARTIE9` = n1…n8 ; `PARTIE10` = r1 r2 ; `BILAN` = bl cr |
Titres des parties (build.py) : Ouverture · I. Suivre une transformation au cours du temps · II. Tableau d'avancement et courbe x(t) ·
III. Suivi par conductimétrie · IV. Suivi par la pression d'un gaz ; choisir sa méthode · V. Vitesse volumique de réaction ·
VI. Évolution de la vitesse · VII. Temps de demi-réaction · VIII. Sujets du national · IX. Pièges de rédaction · X. Bilan du chapitre.
Chaque pN.py commence par `from outils import *` et ne définit que ses listes (une liste Python de S(...)).

## À lire d'abord
1. `.agents/skills/cours-concentration/SKILL.md` (en entier), `.agents/skills/voix-du-cours/SKILL.md` section 1 (texte parlé),
   `.agents/skills/professeur/SKILL.md` (règles), `outils/cours/notes/cours/methode_blocs/BRIEF_AGENTS.md` (blocs : cahier, retrouver, exercice).
2. L'exploration : `backend/data/curriculum/exploration/cinetique.json` — surtout `plan.diapositives` (TES diapositives : id, title, lead, marche,
   visuel, question, prediction, competences, demonstration), `plan.seances`, `notions_complexes`, `pieges`, `erreurs_examen`, `analogies_validees`,
   `a_ne_pas_dire`, `redaction_nationale`, `cas_types`, `questions_eleves`, `decisions_utilisateur`.
   Et l'analyse des nationaux : `outils/cours/notes/cours/cinetique_build/nationaux.md` (section « Figures pour figures.html » pour p4, p6, n1…n8).
3. Le cadre : `backend/data/curriculum/cadre_reference_2bac_pc.json` → `chapitres.cinetique` (formules `ecriture`, `dit`, `hors_cadre.mots` INTERDITS).
4. Le contrat des simulations : `outils/cours/notes/cours/cinetique_contrat_simulations.md` (vues, moments, repères EXACTS, valeurs des exemples
   A, B, C ; « Diapositives servies » dit quelle vue va avec quelle diapositive). figures.html : `vis("figures.html?fig=fig_<session>", …)`,
   moments axes courbe tangente (seulement si le sujet donne une tangente) lecture fin ; repères axe_t axe_y courbe tangente point valeur.
5. Le MODÈLE (forme, ton, densité) : `outils/cours/notes/cours/transformations_lentes_rapides_build/p2.py` (lis 3-4 diapositives) et les outils
   (S, vis, Q, DEMO, EX, VF, PU, R, C, SP dans `cinetique_build/outils.py`).

## Règles
- Une diapositive par entrée de `plan.diapositives` qui t'est confiée, DANS L'ORDRE, id = `ci_<id du plan>_<un mot>` (ex. `ci_m2_trempe`,
  `ci_v3_tangente`). Une seule idée nouvelle par diapositive. Compétence = la PREMIÈRE de la liste `competences` du plan.
  `slide_type` parmi situation | concept | explanation | application | evaluation.
- Chaque diapositive : title, lead, 3-4 bullets, student_trace (= cahier, écrit comme le barème), visuel `vis("page.html?vue=…", caption, alt)`
  (toujours la vue dans l'URL ; bilan.html et carte.html sans vue), `fr` (français parlé) et `mixed` (darija simple + termes du programme en
  français, règles voix-du-cours : AUCUN chiffre, aucun symbole (= + → / ⁺ ⁻ ° % ₂ · …), nombres et unités EN LETTRES, phrase entièrement
  française > 10 mots coupée par des virgules ; pas de tachkil), une question `Q(...)` (3 options, bonne réponse PAS toujours au même rang,
  `prediction=True` si le plan dit prediction), `pointage=[PU("extrait exact de mixed", "moment"), R("extrait", "repère"), SP("extrait", t=8)]`
  dans l'ordre de la voix (ce que la voix décrit, la simulation le montre à ce moment), et `centre=[("formule", "extrait de mixed")]` quand une
  relation naît.
- Toute question ou exercice de calcul (« calcule / combien / détermine / déduis / montre / vérifie ») porte `DEMO(parole, [(ligne écrite,
  extrait exact de parole), ...])` (style « la relation: … l'application numérique: … le résultat: … »). Vérifie CHAQUE nombre avec python.
- Les diapositives d'application et de national portent 1 à 3 exercices `EX(...)` / `VF(...)` niveau national (avec DEMO si calcul).
- Écrit : relations EXACTEMENT comme le cadre (`ecriture`) : v(t) = (1/V)·dx/dt ; x(t₁/₂) = x_f/2 ; G = k·σ ; σ = Σ λᵢ·[Xᵢ] ;
  x = x_max·(σ₀ − σ)/(σ₀ − σ_f) ; x = (P − P₀)·V/(R·T) ; n(I₂) = C·V_E/2 … ; indices et charges Unicode (H₂O₂, I⁻, S₂O₃²⁻, HO⁻, t₁/₂, σ₀) ;
  flèche → ; virgule décimale ; unités mmol, mol/L, min, S/m, mS·m²·mol⁻¹, Pa, K, mmol·L⁻¹·min⁻¹. Jamais « x = texte » pour une définition (« : »).
- Voix : « v de t égale un sur V fois d x sur d t », « t un demi », « x f sur deux », « sigma zéro », « lambda », « eau oxygénée », « ions iodure »,
  « diiode », « ions thiosulfate », « ions hydroxyde », « ions éthanoate » (ou acétate, choisis comme l'exploration), « ions sodium », « magnésium »,
  « dihydrogène », « millimole », « minutes », « siemens par mètre », « pascal », « kelvin », « deux virgule cinq millimoles par litre et par minute ».
- Mots INTERDITS partout (écrit et voix) : `hors_cadre.mots` (chocs efficaces, énergie d'activation, ordre de réaction, loi de vitesse, constante de
  vitesse, mécanisme, Arrhenius, Beer-Lambert, exponentielle…) et `a_ne_pas_dire`. Pour expliquer que v diminue : « les réactifs s'épuisent, leurs
  entités se rencontrent moins souvent ».
- Valeurs : celles du contrat, telles quelles (exemple A : x_max = 2,0 mmol, V = 100 mL, v(0) = 2,5 mmol·L⁻¹·min⁻¹, t₁/₂ ≈ 5,5 min, x(8) = 1,26 mmol,
  V_E = 12,6 mL ; exemple B : σ₀ = 0,249 S/m, σ_f = 0,091 S/m, à 10 min σ = 0,170 S/m → x = 0,50 mmol ; exemple C : P − P₀ = 2,49·10³ Pa → x = 1,0 mmol).
  Nationaux : les valeurs de nationaux.md.
- La carte (o1 et cr) : moments centre methodes trempe tableau mesure courbe vitesse diminue demi_reaction national suite (+ complete en cr).
  Le bilan (bl) : fiche suivi avancement mesure_x courbe vitesse evolution demi_reaction redaction lacunes ; bl et cr portent `acquis=True`
  (modèle transformations_lentes_rapides_build/p3.py, regarde bl et cr). bl et cr portent une question courte (sans prédiction).
- Contrôle : `python3 outils/cours/notes/cours/cinetique_build/check_part.py pN` doit finir par « AUCUNE ERREUR ». Corrige jusqu'à zéro.

## blocs_sN.json (ta séance = 3 blocs de 4 diapositives, découpage `plan.seances`)
Forme exacte (JSON valide, écrit avec l'outil Write) — modèle : `outils/cours/notes/cours/transformations_lentes_rapides_build/blocs_s2.json` :
{"seance": {"id": "ci_sN", "titre": "Séance N — …", "blocs": [
   {"id": "ci_sN_b1", "titre": "…", "slide_ids": [4 ids de tes diapositives, dans l'ordre],
    "cahier": [{"texte": "…"}, …2 à 4 lignes reprises des student_trace…],
    "retrouver": {"prompt": "Cahier fermé : …", "attendu": "<formule ou définition EXACTE du cadre / du cahier>", "competence_id": "C?"},
    "exercice": {…}}, … ]},
 "predictions": [ids de tes diapositives dont la question a prediction=True]}
Titres des séances : 1 « Suivre une transformation : trempe, titrage, avancement » ; 2 « Conductimétrie et pression : mesurer x autrement » ;
3 « Vitesse volumique et temps de demi-réaction » ; 4 « Sujets du national et bilan ».
Blocs : s1 = [o1 o2 m1 m2] [m3 a1 a2 a3] [a4 a5 a6 a7] ; s2 = [g1 g2 g3 g4] [g5 g6 p1 p2] [p3 p4 p5 p6] ; s3 = [v1 v2 v3 v4] [v5 v6 v7 v8] [h1 h2 h3 h4] ;
s4 = [n1 n2 n3 n4] [n5 n6 n7 n8] [r1 r2 bl cr].
`exercice` : reprend un exercice d'une diapositive du bloc s'il y en a un (`{"type", "reprend": "<slide_id>/e<i>", "prompt", "options"
(= choices), "correct", "explanation"}`, un vrai/faux garde `statements`, et la `demonstration` s'il en a une), sinon un QCM court niveau national
(`options` 3, `correct`, `explanation`), avec `demonstration: {"parole", "lignes": [{"texte", "mot"}]}` s'il demande un calcul (parole aux règles de
la voix, chaque `mot` extrait exact). Au moins une prédiction par bloc.

## Rapport final (court)
ids écrits, nombre de questions / prédictions / exercices / démonstrations, sortie finale de check_part, choix à faire valider.
