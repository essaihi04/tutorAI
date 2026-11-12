# Brief — écrire une partie du cours phys_ch11_transformations_deux_sens (« Transformations chimiques s'effectuant dans les deux sens »)

Tu écris UN fichier de contenu `outils/cours/notes/cours/transformations_deux_sens_build/pN.py` (N donné dans ta mission) et UN fichier
`outils/cours/notes/cours/transformations_deux_sens_build/blocs_sN.json` (les 3 blocs de ta séance). Rien d'autre. Messages en français simple.
Travaille depuis la racine du dépôt /home/user/tutorAI. Pas de commit, pas de push, pas de git checkout/stash/reset, pas de sous-agent.
Les simulations sont écrites EN MÊME TEMPS par d'autres agents : n'utilise que les vues, moments et repères du contrat
(lus automatiquement par `transformations_deux_sens_build/outils.py` : `python3 -c "import sys; sys.path.insert(0,'outils/cours/notes/cours/transformations_deux_sens_build'); import outils; print(outils.MOMENTS, outils.REPERES)"`).

## Répartition (fixe : build.py importe exactement ces noms)
| Fichier | Séance | Diapositives du plan (dans l'ordre) | Variables exportées |
|---|---|---|---|
| p1.py + blocs_s1.json | 1 | o1 o2 · b1 … b4 · p1 p2 p3 · p4 p5 p6 (12) | `PARTIE1` = o1 o2 ; `PARTIE2` = b1…b4 ; `PARTIE3` = p1 p2 p3 ; `PARTIE4` = p4 p5 p6 |
| p2.py + blocs_s2.json | 2 | a1 … a6 · e1 … e6 (12) | `PARTIE5` = a1…a6 ; `PARTIE6` = e1…e6 |
| p3.py + blocs_s3.json | 3 | c1 c2 c3 · d1 d2 d3 · n1 … n4 · bl cr (12) | `PARTIE7` = c1 c2 c3 ; `PARTIE8` = d1 d2 d3 ; `PARTIE9` = n1…n4 ; `BILAN` = bl cr |
Titres des parties (build.py) : Ouverture · I. Acides et bases selon Brønsted · II. pH d'une solution aqueuse · III. Réaction d'un acide avec l'eau ·
IV. Taux d'avancement final · V. Transformations dans les deux sens, état d'équilibre · VI. Conductimétrie : trouver τ ·
VII. Dilution et nature de l'acide · VIII. Sujets du national · IX. Bilan du chapitre.
Chaque pN.py commence par `from outils import *` et ne définit que ses listes (une liste Python de S(...)).

## À lire d'abord
1. `.agents/skills/cours-concentration/SKILL.md` (en entier), `.agents/skills/voix-du-cours/SKILL.md` section 1 (texte parlé),
   `.agents/skills/professeur/SKILL.md` (règles), `outils/cours/notes/cours/methode_blocs/BRIEF_AGENTS.md` (blocs : cahier, retrouver, exercice).
2. L'exploration : `backend/data/curriculum/exploration/transformations_deux_sens.json` — surtout `plan.diapositives` (TES diapositives : id, title,
   lead, marche, visuel, question, prediction, competences, demonstration), `plan.seances`, `notions_complexes`, `pieges`, `erreurs_examen`,
   `analogies_validees`, `a_ne_pas_dire`, `redaction_nationale`, `cas_types`, `questions_eleves`, `decisions_utilisateur`.
   Et l'analyse des nationaux : `outils/cours/notes/cours/transformations_deux_sens_build/nationaux.md` (valeurs exactes pour e6, n1…n4).
3. Le cadre : `backend/data/curriculum/cadre_reference_2bac_pc.json` → `chapitres.transformations_deux_sens` (formules `ecriture`, `dit`,
   `hors_cadre.mots` INTERDITS).
4. Le contrat des simulations : `outils/cours/notes/cours/transformations_deux_sens_contrat_simulations.md` (vues, moments, repères EXACTS, valeurs
   des exemples A à F ; « Diapositives servies » dit quelle vue va avec quelle diapositive). figures.html : `vis("figures.html?fig=fig_<session>", …)`.
5. Le MODÈLE (forme, ton, densité) : `outils/cours/notes/cours/cinetique_build/p2.py` (lis 3-4 diapositives) et pour bl/cr
   `outils/cours/notes/cours/cinetique_build/p4.py` (fin du fichier) ; les outils (S, vis, Q, DEMO, EX, VF, PU, R, C, SP) dans
   `transformations_deux_sens_build/outils.py`.

## Règles
- Une diapositive par entrée de `plan.diapositives` qui t'est confiée, DANS L'ORDRE, id = `td_<id du plan>_<un mot>` (ex. `td_b1_acide`,
  `td_a4_taux`). Une seule idée nouvelle par diapositive. Compétence = la PREMIÈRE de la liste `competences` du plan.
  `slide_type` parmi situation | concept | explanation | application | evaluation.
- Chaque diapositive : title, lead, 3-4 bullets, student_trace (= cahier, écrit comme le barème), visuel `vis("page.html?vue=…", caption, alt)`
  (toujours la vue dans l'URL ; bilan.html et carte.html sans vue), `fr` (français parlé) et `mixed` (darija simple en lettres arabes + termes du
  programme en français, règles voix-du-cours : AUCUN chiffre, aucun symbole (= + → ⇌ / ⁺ ⁻ ° % ₂ · [ ] …), nombres et unités EN LETTRES,
  phrase entièrement française > 10 mots coupée par des virgules ; pas de tachkil), une question `Q(...)` (3 options, bonne réponse PAS toujours
  au même rang, `prediction=True` si le plan dit prediction), `pointage=[PU("extrait exact de mixed", "moment"), R("extrait", "repère"), …]`
  dans l'ordre de la voix (ce que la voix décrit, la simulation le montre à ce moment), et `centre=[("formule", "extrait de mixed")]` quand une
  relation naît.
- Toute question ou exercice de calcul (« calcule / combien / détermine / déduis / montre / vérifie ») porte `DEMO(parole, [(ligne écrite,
  extrait exact de parole), ...])` (style « la relation: … l'application numérique: … le résultat: … »). Vérifie CHAQUE nombre avec python.
- Les diapositives d'application et de national portent 1 à 3 exercices `EX(...)` / `VF(...)` niveau national (avec DEMO si calcul).
- Écrit : relations EXACTEMENT comme le cadre (`ecriture`) : pH = −log[H₃O⁺] ; [H₃O⁺] = 10^(−pH) ; τ = x_f/x_max ; x_max = C·V ;
  x_f = [H₃O⁺]_éq·V ; τ = 10^(−pH)/C ; AH + H₂O ⇌ A⁻ + H₃O⁺ ; σ = (λ(H₃O⁺) + λ(A⁻))·[H₃O⁺] … ; indices et charges Unicode (H₃O⁺, HO⁻,
  CH₃COOH, CH₃COO⁻, NH₄⁺) ; ⇌ pour les deux sens, → pour une réaction totale ; virgule décimale ; unités mol, mol/L, mol/m³, S/m,
  mS·m²·mol⁻¹. Jamais « x = texte » pour une définition (« : »).
- Voix : « p H », « p H égale moins log de la concentration des ions H trois O plus », « dix puissance moins p H », « tau », « x f », « x max »,
  « acide éthanoïque », « ions éthanoate », « ions oxonium » ou « ions H trois O plus » (choisis comme l'exploration), « acide chlorhydrique »,
  « ammoniac », « ions ammonium », « double flèche », « sigma », « lambda », « mole par litre », « mole par mètre cube », « siemens par mètre »,
  « quatre pour cent ».
- Mots INTERDITS partout (écrit et voix) : `hors_cadre.mots` (Qr, quotient de réaction, constante d'équilibre, Ka, pKa, Ke, produit ionique,
  autoprotolyse, Henderson, diagramme de prédominance, indicateur coloré…) et `a_ne_pas_dire`. Ces notions viennent aux chapitres suivants :
  dire seulement « on le verra au chapitre suivant » sans les nommer.
- Valeurs : celles du contrat, telles quelles (exemples A à F). Nationaux : les valeurs de nationaux.md.
- La carte (o1 et cr) : moments du contrat pour carte.html (+ `complete` en cr). Le bilan (bl) : moments du contrat pour bilan.html.
  bl et cr portent `acquis=True` et une question courte (sans prédiction) ; modèle cinetique_build/p4.py.
- Contrôle : `python3 outils/cours/notes/cours/transformations_deux_sens_build/check_part.py pN` doit finir par « AUCUNE ERREUR ». Corrige jusqu'à zéro.

## blocs_sN.json (ta séance = 3 blocs de 4 diapositives, découpage `plan.seances`)
Forme exacte (JSON valide, écrit avec l'outil Write) — modèle : `outils/cours/notes/cours/cinetique_build/blocs_s2.json` s'il existe, sinon
`outils/cours/notes/cours/transformations_lentes_rapides_build/blocs_s2.json` :
{"seance": {"id": "td_sN", "titre": "Séance N — …", "blocs": [
   {"id": "td_sN_b1", "titre": "…", "slide_ids": [4 ids de tes diapositives, dans l'ordre],
    "cahier": [{"texte": "…"}, …2 à 4 lignes reprises des student_trace…],
    "retrouver": {"prompt": "Cahier fermé : …", "attendu": "<formule ou définition EXACTE du cadre / du cahier>", "competence_id": "C?"},
    "exercice": {…}}, … ]},
 "predictions": [ids de tes diapositives dont la question a prediction=True]}
Titres des séances : 1 « Acides et bases selon Brønsted, pH, réaction d'un acide avec l'eau » ; 2 « Taux d'avancement final, réaction dans les deux
sens, état d'équilibre » ; 3 « Conductimétrie, dilution, questions du national, bilan ».
Blocs : s1 = [o1 o2 b1 b2] [b3 b4 p1 p2] [p3 p4 p5 p6] ; s2 = [a1 a2 a3 a4] [a5 a6 e1 e2] [e3 e4 e5 e6] ; s3 = [c1 c2 c3 d1] [d2 d3 n1 n2] [n3 n4 bl cr].
`exercice` : reprend un exercice d'une diapositive du bloc s'il y en a un (`{"type", "reprend": "<slide_id>/e<i>", "prompt", "options"
(= choices), "correct", "explanation"}`, un vrai/faux garde `statements`, et la `demonstration` s'il en a une), sinon un QCM court niveau national
(`options` 3, `correct`, `explanation`), avec `demonstration: {"parole", "lignes": [{"texte", "mot"}]}` s'il demande un calcul (parole aux règles de
la voix, chaque `mot` extrait exact). Au moins une prédiction par bloc.

## Rapport final (court)
ids écrits, nombre de questions / prédictions / exercices / démonstrations, sortie finale de check_part, choix à faire valider.
