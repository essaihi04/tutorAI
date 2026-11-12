# Brief — écrire une partie du cours phys_ch12_etat_equilibre (« État d'équilibre d'un système chimique »)

Tu écris UN fichier de contenu `outils/cours/notes/cours/etat_equilibre_build/pN.py` (N donné dans ta mission) et UN fichier
`outils/cours/notes/cours/etat_equilibre_build/blocs_sN.json` (les 3 blocs de ta séance). Rien d'autre. Messages en français simple.
Travaille depuis la racine du dépôt /home/user/tutorAI. Pas de commit, pas de push, pas de git checkout/stash/reset, pas de sous-agent.
Les simulations sont écrites EN MÊME TEMPS par d'autres agents : n'utilise que les vues, moments et repères du contrat
(lus automatiquement par `etat_equilibre_build/outils.py` : `python3 -c "import sys; sys.path.insert(0,'outils/cours/notes/cours/etat_equilibre_build'); import outils; print(outils.MOMENTS, outils.REPERES)"`).

## Répartition (fixe : build.py importe exactement ces noms)
| Fichier | Séance | Diapositives du plan (dans l'ordre) | Variables exportées |
|---|---|---|---|
| p1.py + blocs_s1.json | 1 | o1 o2 · r1 r2 · q1 … q5 · i1 i2 i3 (12) | `PARTIE1` = o1 o2 ; `PARTIE2` = r1 r2 ; `PARTIE3` = q1…q5 ; `PARTIE4` = i1 i2 i3 |
| p2.py + blocs_s2.json | 2 | e1 e2 e3 · k1 … k5 · m1 … m4 (12) | `PARTIE5` = e1 e2 e3 ; `PARTIE6` = k1…k5 ; `PARTIE7` = m1…m4 |
| p3.py + blocs_s3.json | 3 | f1 … f4 · n1 … n6 · bl cr (12) | `PARTIE8` = f1…f4 ; `PARTIE9` = n1…n6 ; `BILAN` = bl cr |
Titres des parties : ceux de `plan.seances[n].parties` de l'exploration.
Chaque pN.py commence par `from outils import *` et ne définit que ses listes (une liste Python de S(...)).

## À lire d'abord
1. `.agents/skills/cours-concentration/SKILL.md` (en entier), `.agents/skills/voix-du-cours/SKILL.md` section 1 (texte parlé),
   `.agents/skills/professeur/SKILL.md` (règles), `outils/cours/notes/cours/methode_blocs/BRIEF_AGENTS.md` (blocs : cahier, retrouver, exercice).
2. L'exploration : `backend/data/curriculum/exploration/etat_equilibre.json` — surtout `plan.diapositives` (TES diapositives : id, title,
   lead, marche, visuel, question, prediction, competences, demonstration), `plan.seances`, `notions_complexes`, `pieges`, `erreurs_examen`,
   `analogies_validees`, `a_ne_pas_dire`, `redaction_nationale`, `cas_types`, `questions_eleves`, `decisions_utilisateur`.
   Et l'analyse des nationaux : `outils/cours/notes/cours/etat_equilibre_build/nationaux.md` (valeurs exactes pour les diapositives de national).
3. Le cadre : `backend/data/curriculum/cadre_reference_2bac_pc.json` → `chapitres.etat_equilibre` (formules `ecriture`, `dit`,
   `hors_cadre.mots` INTERDITS).
4. Le contrat des simulations : `outils/cours/notes/cours/etat_equilibre_contrat_simulations.md` (vues, moments, repères EXACTS, valeurs
   des exemples A à F ; « Diapositives servies » dit quelle vue va avec quelle diapositive). figures.html : `vis("figures.html?fig=fig_<session>", …)`.
5. Le MODÈLE (forme, ton, densité) : `outils/cours/notes/cours/transformations_deux_sens_build/p2.py` (lis 3-4 diapositives) et pour bl/cr
   `outils/cours/notes/cours/transformations_deux_sens_build/p3.py` (fin du fichier) ; les outils (S, vis, Q, DEMO, EX, VF, PU, R, C, SP) dans
   `etat_equilibre_build/outils.py`.

## Règles
- Une diapositive par entrée de `plan.diapositives` qui t'est confiée, DANS L'ORDRE, id = `ee_<id du plan>_<un mot>` (ex. `ee_q1_quotient`,
  `ee_k2_constante`). Une seule idée nouvelle par diapositive. Compétence = la PREMIÈRE de la liste `competences` du plan.
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
- Écrit : relations EXACTEMENT comme le cadre (`formules[].ecriture` de `chapitres.etat_equilibre`) : Qr = [C]^c·[D]^d/([A]^a·[B]^b) ;
  K = Qr,éq ; K' = 1/K ; τ = 10^(−pH)/C ; Qr,éq = 10^(−2pH)/(C − 10^(−pH)) ; [A⁻]_éq = [H₃O⁺]_éq = C·τ ; [AH]_éq = C·(1 − τ) ; K = C·τ²/(1 − τ) ;
  σ = (λ(H₃O⁺) + λ(A⁻))·[H₃O⁺] ; [H₃O⁺]_éq = σ/(λ(H₃O⁺) + λ(A⁻)) ; indices et charges Unicode (H₃O⁺, HO⁻, CH₃COOH, CH₃COO⁻, Cu²⁺, Zn²⁺) ;
  ⇌ pour les deux sens ; Qr et K sans unité ; virgule décimale ; unités mol, mol/L, mol/m³, S/m, mS·m²·mol⁻¹. Jamais « x = texte » pour une
  définition (« : »). « activité » est un mot interdit : n'écris pas « activité » même au sens courant.
- Voix : les `dit` du cadre (« Q r », « Q r à l'équilibre », « K », « K prime égale un sur K », « tau », « C fois tau au carré sur un moins tau »),
  « p H », « dix puissance moins p H », « quotient de réaction », « constante d'équilibre », « acide éthanoïque », « ions éthanoate »,
  « ions H trois O plus », « double flèche », « sigma », « lambda », « mole par litre », « mole par mètre cube », « siemens par mètre ».
- Mots INTERDITS partout (écrit et voix) : `hors_cadre.mots` du cadre (Ka, pKa, Ke, produit ionique, autoprotolyse, Henderson, prédominance,
  indicateur coloré, critère d'évolution spontanée, évolution spontanée, Le Chatelier, activité…) et `a_ne_pas_dire`. Ces notions viennent plus
  tard (chapitre suivant ou semestre 2) : dire seulement « on le verra plus tard » sans les nommer. Qr,i se calcule ici, mais on ne s'en sert
  PAS pour prévoir le sens d'évolution (semestre 2).
- Valeurs : celles du contrat (« Données communes », exemples A à K), telles quelles (pH au centième). Nationaux : les valeurs de nationaux.md.
- La carte (o1 et cr) : moments du contrat pour carte.html (+ `complete` en cr). Le bilan (bl) : moments du contrat pour bilan.html.
  bl et cr portent `acquis=True` et une question courte (sans prédiction) ; modèle transformations_deux_sens_build/p3.py.
- Contrôle : `python3 outils/cours/notes/cours/etat_equilibre_build/check_part.py pN` doit finir par « AUCUNE ERREUR ». Corrige jusqu'à zéro.

## blocs_sN.json (ta séance = 3 blocs de 4 diapositives, découpage `plan.seances`)
Forme exacte (JSON valide, écrit avec l'outil Write) — modèle : `outils/cours/notes/cours/transformations_deux_sens_build/blocs_s2.json` :
{"seance": {"id": "ee_sN", "titre": "Séance N — …", "blocs": [
   {"id": "ee_sN_b1", "titre": "…", "slide_ids": [4 ids de tes diapositives, dans l'ordre],
    "cahier": [{"texte": "…"}, …2 à 4 lignes reprises des student_trace…],
    "retrouver": {"prompt": "Cahier fermé : …", "attendu": "<formule ou définition EXACTE du cadre / du cahier>", "competence_id": "C?"},
    "exercice": {…}}, … ]},
 "predictions": [ids de tes diapositives dont la question a prediction=True]}
Titres des séances : 1 « Le quotient de réaction Qr » ; 2 « Qr à l'équilibre, constante d'équilibre K, mesures » ;
3 « De quoi dépend τ, questions du national, bilan ».
Blocs : s1 = [o1 o2 r1 r2] [q1 q2 q3 q4] [q5 i1 i2 i3] ; s2 = [e1 e2 e3 k1] [k2 k3 k4 k5] [m1 m2 m3 m4] ; s3 = [f1 f2 f3 f4] [n1 n2 n3 n4] [n5 n6 bl cr].
`exercice` : reprend un exercice d'une diapositive du bloc s'il y en a un (`{"type", "reprend": "<slide_id>/e<i>", "prompt", "options"
(= choices), "correct", "explanation"}`, un vrai/faux garde `statements`, et la `demonstration` s'il en a une), sinon un QCM court niveau national
(`options` 3, `correct`, `explanation`), avec `demonstration: {"parole", "lignes": [{"texte", "mot"}]}` s'il demande un calcul (parole aux règles de
la voix, chaque `mot` extrait exact). Au moins une prédiction par bloc.

## Rapport final (court)
ids écrits, nombre de questions / prédictions / exercices / démonstrations, sortie finale de check_part, choix à faire valider.
