# Brief — écrire une partie du cours phys_ch13_acides_bases (« Transformations liées aux réactions acide-base »)

Tu écris UN fichier de contenu `outils/cours/notes/cours/acides_bases_build/pN.py` (N donné dans ta mission) et UN fichier
`outils/cours/notes/cours/acides_bases_build/blocs_sN.json` (les 3 blocs de ta séance). Rien d'autre. Messages en français simple.
Travaille depuis la racine du dépôt /home/user/tutorAI. Pas de commit, pas de push, pas de git checkout/stash/reset, pas de sous-agent.
Les simulations sont écrites EN MÊME TEMPS par d'autres agents : n'utilise que les vues, moments et repères du contrat
(lus automatiquement par `acides_bases_build/outils.py` : `python3 -c "import sys; sys.path.insert(0,'outils/cours/notes/cours/acides_bases_build'); import outils; print(outils.MOMENTS, outils.REPERES)"`).

## Répartition (fixe : build.py importe exactement ces noms)
| Fichier | Séance | Diapositives du plan (dans l'ordre) | Variables exportées |
|---|---|---|---|
| p1.py + blocs_s1.json | 1 | o1 o2 · r1 r2 · w1 … w5 · b1 b2 b3 (12) | `PARTIE1` = o1 o2 ; `PARTIE2` = r1 r2 ; `PARTIE3` = w1…w5 ; `PARTIE4` = b1 b2 b3 |
| p2.py + blocs_s2.json | 2 | a1 … a5 · c1 c2 c3 · k1 … k4 (12) | `PARTIE5` = a1…a5 ; `PARTIE6` = c1 c2 c3 ; `PARTIE7` = k1…k4 |
| p3.py + blocs_s3.json | 3 | p1 … p4 · i1 i2 · d1 … d6 (12) | `PARTIE8` = p1…p4 ; `PARTIE9` = i1 i2 ; `PARTIE10` = d1…d6 |
| p4.py + blocs_s4.json | 4 | e1 … e5 · n1 … n5 · bl cr (12) | `PARTIE11` = e1…e5 ; `PARTIE12` = n1…n5 ; `BILAN` = bl cr |

Titres des parties (ceux de `plan.seances[n].parties` de l'exploration) :
- séance 1 : « Ouverture » (o1 o2) ; « I. Rappels : couples acide/base, pH, constante d'équilibre » (r1 r2) ;
  « II. L'autoprotolyse de l'eau et le produit ionique Ke » (w1…w5) ; « III. Une base dans l'eau : pH et taux d'avancement final » (b1 b2 b3) ;
- séance 2 : « IV. La constante d'acidité Ka et le pKa » (a1…a5) ; « V. Comparer des acides et des bases » (c1 c2 c3) ;
  « VI. La constante d'équilibre d'une réaction acide-base » (k1…k4) ;
- séance 3 : « VII. Domaines de prédominance et diagramme de distribution » (p1…p4) ; « VIII. Les indicateurs colorés » (i1 i2) ;
  « IX. Le dosage acido-basique : réaction, équivalence, courbe » (d1…d6) ;
- séance 4 : « X. Exploiter une courbe de dosage » (e1…e5) ; « XI. Sujets du national » (n1…n5) ; « XII. Bilan du chapitre » (bl cr).
Chaque pN.py commence par `from outils import *` et ne définit que ses listes (une liste Python de S(...)).

## À lire d'abord
1. `.agents/skills/cours-concentration/SKILL.md` (en entier), `.agents/skills/voix-du-cours/SKILL.md` section 1 (texte parlé),
   `.agents/skills/professeur/SKILL.md` (règles), `outils/cours/notes/cours/methode_blocs/BRIEF_AGENTS.md` (blocs : cahier, retrouver, exercice).
2. L'exploration : `backend/data/curriculum/exploration/acides_bases.json` — surtout `plan.diapositives` (TES diapositives : id, title,
   lead, marche, visuel, question, prediction, competences, demonstration), `plan.seances`, `notions_complexes`, `pieges`, `erreurs_examen`,
   `analogies_validees`, `a_ne_pas_dire`, `redaction_nationale`, `cas_types`, `questions_eleves`, `decisions_utilisateur`.
   Et l'analyse des nationaux : `outils/cours/notes/cours/acides_bases_build/nationaux.md` (valeurs exactes pour les diapositives de national).
3. Le cadre : `backend/data/curriculum/cadre_reference_2bac_pc.json` → `chapitres.acides_bases` (formules `ecriture`, `dit`,
   `hors_cadre.mots` INTERDITS).
4. Le contrat des simulations : `outils/cours/notes/cours/acides_bases_contrat_simulations.md` (vues, moments, repères EXACTS, valeurs
   des exemples A à N ; « Diapositives servies » dit quelle vue va avec quelle diapositive). figures.html : `vis("figures.html?fig=fig_<session>", …)`.
5. Le MODÈLE (forme, ton, densité) : `outils/cours/notes/cours/etat_equilibre_build/p2.py` (lis 3-4 diapositives) et pour bl/cr
   `outils/cours/notes/cours/etat_equilibre_build/p3.py` (fin du fichier) ; les outils (S, vis, Q, DEMO, EX, VF, PU, R, C, SP, BQ) dans
   `acides_bases_build/outils.py`.

## Règles
- Une diapositive par entrée de `plan.diapositives` qui t'est confiée, DANS L'ORDRE, id = `ab_<id du plan>_<un mot>` (ex. `ab_w2_ke`,
  `ab_d3_equivalence`). Une seule idée nouvelle par diapositive. Compétence = la PREMIÈRE de la liste `competences` du plan.
  `slide_type` parmi situation | concept | explanation | application | evaluation.
- Chaque diapositive : title, lead, 3-4 bullets, student_trace (= cahier, écrit comme le barème), visuel `vis("page.html?vue=…", caption, alt)`
  (toujours la vue dans l'URL ; bilan.html et carte.html sans vue), `fr` (français parlé) et `mixed` (darija simple en lettres arabes + termes du
  programme en français, règles voix-du-cours : AUCUN chiffre, aucun symbole (= + → ⇌ / ⁺ ⁻ ° % ₂ · [ ] …), nombres et unités EN LETTRES,
  phrase entièrement française > 10 mots coupée par des virgules ; pas de tachkil), une question `Q(...)` (3 options, bonne réponse PAS toujours
  au même rang, `prediction=True` si le plan dit prediction), `pointage=[PU("extrait exact de mixed", "moment"), R("extrait", "repère"), …]`
  dans l'ordre de la voix (ce que la voix décrit, la simulation le montre à ce moment), `SP("extrait", pH=…)` ou `SP("extrait", V_B=…)` sur les
  vues à poignée (eau?vue=solutions, predominance?vue=domaines|distribution, dosage?vue=courbe), et `centre=[("formule", "extrait de mixed")]`
  quand une relation naît.
- Toute question ou exercice de calcul (« calcule / combien / détermine / déduis / montre / vérifie / établis / trouve ») porte `DEMO(parole,
  [(ligne écrite, extrait exact de parole), ...])` (style « la relation: … l'application numérique: … le résultat: … »). Vérifie CHAQUE nombre
  avec python (les courbes J, K, L du contrat sont déjà calculées : reprends-les telles quelles).
- Les diapositives d'application et de national portent 1 à 3 exercices `EX(...)` / `VF(...)` niveau national (avec DEMO si calcul).
- Écrit : relations EXACTEMENT comme le cadre (`formules[].ecriture` de `chapitres.acides_bases`) : 2H₂O ⇌ H₃O⁺ + HO⁻ ; Ke = [H₃O⁺]·[HO⁻] ;
  Ke = 1,0·10⁻¹⁴ ; pKe = −log Ke = 14 ; pH = −log[H₃O⁺] ; [HO⁻] = Ke/[H₃O⁺] ; [HO⁻] = 10^(pH − 14) ; τ = [HO⁻]_éq/C ; K = C·τ²/(1 − τ) ;
  Ka = [A⁻]_éq·[H₃O⁺]_éq/[AH]_éq ; pKa = −log Ka ; Ka = 10^(−pKa) ; Ka = Ke/Qr,éq ; pKa(H₃O⁺/H₂O) = 0 ; pKa(H₂O/HO⁻) = 14 ; K = Ka₁/Ka₂ ;
  K = 10^(pKa₂ − pKa₁) ; K = Ka/Ke ; pH = pKa + log([A⁻]_éq/[AH]_éq) ; C_A·V_A = C_B·V_BE ; C_B·V_B = C_A·V_AE ; pH = pKa à V_B = V_BE/2 ;
  C_m = C·M ; indices et charges Unicode (H₃O⁺, HO⁻, CH₃COOH, CH₃COO⁻, NH₄⁺, NH₃, CH₃NH₂, CH₃NH₃⁺) ; ⇌ pour une réaction limitée, → pour la
  réaction de DOSAGE ; Ke, Ka, pKa, K, pH sans unité ; virgule décimale ; unités mol, mol/L, mL, L, g/L, S/m, mS/m. Jamais « x = texte » pour une
  définition (« : »). pH au centième pour une solution mesurée (3,41 ; 10,60), au dixième pour une lecture de courbe (8,3 ; 5,7 ; 4,8).
- Voix : les `dit` du cadre (« K e », « p K e », « K a », « p K a », « K a un sur K a deux », « dix puissance p K a deux moins p K a un »,
  « C A fois V A égale C B fois V B E »), « p H », « ions H trois O plus », « ions hydroxyde H O moins », « double flèche », « simple flèche »,
  « produit ionique de l'eau », « constante d'acidité », « zone de virage », « équivalence », « demi-équivalence », « méthode des tangentes »,
  « mole par litre », « millilitre ».
- Mots INTERDITS partout (écrit et voix) : `hors_cadre.mots` du cadre (Henderson, Hasselbalch, Flood, Lewis, Arrhenius, Ostwald, loi de dilution,
  degré d'ionisation, activité chimique, pouvoir tampon, Le Chatelier, dosage potentiométrique, méthode de Gran, dérivée seconde, polyacide,
  Kb, pKb, pOH, critère d'évolution spontanée, évolution spontanée…) et `a_ne_pas_dire` (dont : [HO⁻] = 10^(−pH) ; dosage avec ⇌ ; pH = pKa
  « à l'équivalence » ; C_A·V_A = C_B·V_B sans le E). On dit « pH = pKa + log([A⁻]/[AH]) » sans lui donner de nom. La comparaison de Qr,i à K
  (sens) vient au semestre 2 : dire seulement « on le verra au semestre deux » sans la nommer.
- Valeurs : celles du contrat (« Données communes », exemples A à N), telles quelles. Nationaux : les valeurs de nationaux.md.
- La carte (o1 et cr) : moments du contrat pour carte.html (+ `complete` en cr). Le bilan (bl) : moments du contrat pour bilan.html.
  bl et cr portent `acquis=True` et une question courte (sans prédiction) ; modèle etat_equilibre_build/p3.py.
- Contrôle : `python3 outils/cours/notes/cours/acides_bases_build/check_part.py pN` doit finir par « AUCUNE ERREUR ». Corrige jusqu'à zéro.

## blocs_sN.json (ta séance = 3 blocs de 4 diapositives, découpage `plan.seances`)
Forme exacte (JSON valide, écrit avec l'outil Write) — modèle : `outils/cours/notes/cours/etat_equilibre_build/blocs_s2.json` :
{"seance": {"id": "ab_sN", "titre": "Séance N — …", "blocs": [
   {"id": "ab_sN_b1", "titre": "…", "slide_ids": [4 ids de tes diapositives, dans l'ordre],
    "cahier": [{"texte": "…"}, …2 à 4 lignes reprises des student_trace…],
    "retrouver": {"prompt": "Cahier fermé : …", "attendu": "<formule ou définition EXACTE du cadre / du cahier>", "competence_id": "C?"},
    "exercice": {…}}, … ]},
 "predictions": [ids de tes diapositives dont la question a prediction=True]}
Titres des séances : 1 « L'eau, le produit ionique Ke et le pH d'une base » ; 2 « Constante d'acidité Ka, pKa et constante d'une réaction
acide-base » ; 3 « Prédominance, indicateurs colorés et dosage acido-basique » ; 4 « Exploiter un dosage, sujets du national, bilan ».
Blocs : s1 = [o1 o2 r1 r2] [w1 w2 w3 w4] [w5 b1 b2 b3] ; s2 = [a1 a2 a3 a4] [a5 c1 c2 c3] [k1 k2 k3 k4] ;
s3 = [p1 p2 p3 p4] [i1 i2 d1 d2] [d3 d4 d5 d6] ; s4 = [e1 e2 e3 e4] [e5 n1 n2 n3] [n4 n5 bl cr].
`exercice` : reprend un exercice d'une diapositive du bloc s'il y en a un (`{"type", "reprend": "<slide_id>/e<i>", "prompt", "options"
(= choices), "correct", "explanation"}`, un vrai/faux garde `statements`, et la `demonstration` s'il en a une), sinon un QCM court niveau national
(`options` 3, `correct`, `explanation`), avec `demonstration: {"parole", "lignes": [{"texte", "mot"}]}` s'il demande un calcul (parole aux règles de
la voix, chaque `mot` extrait exact). Au moins une prédiction par bloc.

## Rapport final (court)
ids écrits, nombre de questions / prédictions / exercices / démonstrations, sortie finale de check_part, choix à faire valider.
