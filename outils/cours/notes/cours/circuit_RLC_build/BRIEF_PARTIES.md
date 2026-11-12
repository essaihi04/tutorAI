# Brief — écrire une partie du cours phys_ch8_circuit_RLC (« Oscillations libres d'un circuit RLC série »)

Tu écris UN fichier de contenu `outils/cours/notes/cours/circuit_RLC_build/pN.py` (N donné dans ta mission) et UN fichier
`outils/cours/notes/cours/circuit_RLC_build/blocs_sN.json` (les 3 blocs de ta séance). Rien d'autre. Messages en français simple.
Travaille depuis la racine du dépôt /home/user/tutorAI. Pas de commit, pas de push, pas de git checkout/stash/reset, pas de sous-agent.

## Répartition (fixe : build.py importe exactement ces noms)
| Fichier | Séance | Diapositives du plan (dans l'ordre) | Variables exportées |
|---|---|---|---|
| p1.py + blocs_s1.json | 1 | o1 o2 d1 d2 d3 d4 d5 d6 · r1 r2 r3 r4 (12) | `PARTIE1` = o1…d6 (8) ; `PARTIE2` = r1…r4 (4) |
| p2.py + blocs_s2.json | 2 | e1 e2 e3 e4 e5 · e6 e7 e8 p1 p2 p3 p4 (12) | `PARTIE3` = e1…e5 (5) ; `PARTIE4` = e6…p4 (7) |
| p3.py + blocs_s3.json | 3 | c1 c2 c3 c4 · l1 l2 l3 l4 · en1 en2 en3 en4 (12) | `PARTIE5` = c1…c4 ; `PARTIE6` = l1…l4 ; `PARTIE7` = en1…en4 |
| p4.py + blocs_s4.json | 4 | a1 a2 a3 a4 a5 · k1 k2 k3 · n1 n2 · bl cr (12) | `PARTIE8` = a1…a5 ; `PARTIE9` = k1…k3 ; `PARTIE10` = n1 n2 ; `BILAN` = bl cr |
Titres des parties (build.py) : I. Un condensateur qui se vide dans une bobine · II. Les trois régimes · III. L'équation différentielle ·
IV. La solution du circuit LC et la période propre · V. Les conditions initiales : U_m et φ · VI. Lire un oscillogramme · VII. L'échange d'énergie ·
VIII. L'amortissement · IX. L'entretien des oscillations · X. Deux sujets du national · XI. Bilan du chapitre.
Chaque pN.py commence par `from outils import *` et ne définit que ses listes (une liste Python de S(...)).

## À lire d'abord
1. `.agents/skills/cours-concentration/SKILL.md` (en entier), `.agents/skills/voix-du-cours/SKILL.md` section 1 (texte parlé),
   `.agents/skills/professeur/SKILL.md` (règles), `outils/cours/notes/cours/methode_blocs/BRIEF_AGENTS.md` (blocs : cahier, retrouver, exercice).
2. L'exploration : `backend/data/curriculum/exploration/circuit_RLC.json` — surtout `plan.diapositives` (TES diapositives : id, title, lead,
   marche, visuel, question, prediction, competences, demonstration), `plan.seances`, `notions_complexes`, `pieges`, `erreurs_examen`,
   `analogies_validees`, `a_ne_pas_dire`, `redaction_nationale`, `cas_types`, `valeurs_reperes`, `questions_eleves`.
   Et l'analyse des nationaux : `outils/cours/notes/cours/circuit_RLC_build/nationaux.md` (valeurs vérifiées, erreurs du dépôt à ne pas reprendre).
3. Le cadre : `backend/data/curriculum/cadre_reference_2bac_pc.json` → `chapitres.circuit_RLC` (formules `ecriture`, `dit`, `hors_cadre.mots` INTERDITS).
4. Le contrat des simulations : `outils/cours/notes/cours/circuit_RLC_contrat_simulations.md` (pages, vues, moments, repères EXACTS ; la liste
   « Diapositives servies » dit quelle vue va avec quelle diapositive). Les tables MOMENTS / REPERES de
   `outils/cours/notes/cours/circuit_RLC_build/outils.py` en sont la copie : n'utilise que ceux-là.
5. Le MODÈLE (forme, ton, densité) : `outils/cours/notes/cours/dipole_RL_build/p1.py` (lis 3-4 diapositives) et ses outils
   (S, vis, Q, DEMO, EX, VF, PU, R, C, SP dans `outils/cours/notes/cours/circuit_RLC_build/outils.py`, même API).

## Règles
- Une diapositive par entrée de `plan.diapositives` qui t'est confiée, DANS L'ORDRE, id = `lc_<id du plan>_<un mot>` (ex. `lc_d3_courant`,
  `lc_en2_depart`). Une seule idée nouvelle par diapositive. Compétence = la PREMIÈRE de la liste `competences` du plan (S(..., comp, ...)).
  `slide_type` parmi situation | concept | explanation | application | evaluation.
- Chaque diapositive : title, lead, 3-4 bullets, student_trace (= cahier, écrit comme le barème, formule du cadre), visuel
  `vis("page.html?vue=…", caption, alt)` (ou `vis("figures.html?fig=…", …)`, `vis("equation.html", …)`, `vis("entretien.html", …)`),
  `fr` (français parlé) et `mixed` (darija simple + termes du programme en français, règles voix-du-cours : AUCUN chiffre, aucun symbole
  = / + × → ( ) % ² π φ √ −, nombres et unités EN LETTRES, phrase entièrement française > 10 mots coupée par des virgules ; pas de tachkil),
  une question `Q(...)` (3 options, bonne réponse PAS toujours au même rang, `prediction=True` si le plan dit prediction),
  `pointage=[PU("extrait exact de mixed", "moment"), R("extrait", "repère")]` dans l'ordre de la voix, et `centre=[("formule", "extrait de mixed")]`
  quand une formule naît. Une vue sans `?vue=` prend la vue par défaut (circuit-lc → montage, oscillogramme → periodique, solution → cos,
  periode → T0, energie → echange) : écris toujours la vue dans l'URL.
- Toute question ou exercice de calcul / « établis / montre / vérifie / trouve / détermine / déduis / combien / que vaut » porte
  `DEMO(parole, [(ligne écrite, extrait exact de parole), ...])` (style « la relation: … l'application numérique: … le résultat: … »).
  Vérifie CHAQUE calcul avec python.
- Les diapositives d'application et de national portent 1 à 3 exercices `EX(...)` / `VF(...)` niveau national (avec DEMO si calcul).
- Écrit : formules EXACTEMENT comme le cadre :
  `i = dq/dt = C·du_C/dt` ; `q = C·u_C` ; `u_b(0⁺) = −u_C(0)` ; `u_C + u_R + u_b = 0` ; `u_b = L·di/dt + r·i` ; `u_R = R·i` ;
  `L·d²q/dt² + (R + r)·dq/dt + q/C = 0` ; `LC·d²u_C/dt² + (R + r)·C·du_C/dt + u_C = 0` ; `d²u_C/dt² + ((R + r)/L)·du_C/dt + u_C/(LC) = 0` ;
  `d²u_C/dt² + u_C/(LC) = 0` (et `d²q/dt² + q/(LC) = 0`) ; `u_C(t) = U_m·cos(2πt/T₀ + φ)` ; `T₀ = 2π√(LC)` ; `ω₀ = 2π/T₀ = 1/√(LC)` (une ligne, e8) ;
  `[L]·[C] = [T]²` ; `u_C(0) = U_m·cos φ` ; `T ≈ T₀` ; `L = T₀²/(4π²·C)` et `C = T₀²/(4π²·L)` ; `π² = 10` ; `E = ½·C·u_C² + ½·L·i²` ;
  `E = ½·C·E² = ½·L·I_m²` ; `dE/dt = −(R + r)·i²` (bobine seule : `dE_T/dt = −r·i²`) ; `|ΔE| = ½·C·(U₁² − U₂²)` ; `u_G = k·i` ;
  `L·d²q/dt² + (R + r − k)·dq/dt + q/C = 0` ; `k = R + r`.
  Toujours « R + r » (résistance totale). On écrit u_b et on dit une fois que les sujets écrivent aussi u_L ; E_m = énergie MAGNÉTIQUE (jamais
  « mécanique ») ; « T₀ » période propre, « T » pseudo-période ; virgule décimale ; unités (µF, mH, Ω, ms, mA, µJ) ; puissances 10⁻⁶.
- Voix (mixed et fr) : « u C », « u R », « u b », « u G », « q », « dé q sur dé t », « dé u C sur dé t », « dé i sur dé t »,
  « dé deux q sur dé t deux », « dé deux u C sur dé t deux », « T zéro », « deux pi racine de L C », « T zéro au carré », « quatre pi carré »,
  « pi deux égale dix » (π² = 10), « U m », « I m », « phi », « oméga zéro », « E e », « E m », « R plus r », « k égale R plus r »,
  « u G égale k i », « un demi C u C au carré », « un demi L i au carré », « dé E sur dé t égale moins R plus r fois i au carré »,
  « dix puissance moins six », « microfarad », « millihenry », « milliseconde », « microjoule ». Jamais de chiffre ni de symbole.
- Mots INTERDITS partout (écrit et voix) : `hors_cadre.mots` (facteur de qualité, résonance, oscillations forcées, impédance, réactance,
  équation caractéristique, discriminant, décrément logarithmique, coefficient d'amortissement, enveloppe exponentielle, résistance critique,
  oscillateur harmonique, déphasage, analogie électromécanique…) et `a_ne_pas_dire` (motifs : « 2π√(L/C) », « la pseudo-période est la période
  propre », « la résistance crée les oscillations », « avec une résistance l'énergie se conserve »). Le régime critique : une phrase (r2),
  « la frontière », aucune valeur calculée. Entretien : `u_G = k·i` (jamais « résistance négative »).
- Valeurs des simulations (à citer telles quelles, voir le contrat) : E = 6 V, C = 4 µF, L = 0,1 H, r = 10 Ω, R = 10 Ω (R + r = 20 Ω) ;
  T₀ = 2π√(LC) ≈ 4 ms (π² = 10 : T₀² = 40 × 0,1 × 4·10⁻⁶ = 1,6·10⁻⁵, T₀ = 4·10⁻³ s) ; pseudo-période T ≈ 4 ms ; sommets 6 ; 4,0 ; 2,7 ; 1,8 V ;
  du 1er au 4e sommet 3T ≈ 12 ms ; u_b(0⁺) = −6 V ; E(0) = ½·C·E² = 7,2·10⁻⁵ J ; I_m ≈ 38 mA ; énergie perdue entre les sommets 0 et T :
  ½ × 4·10⁻⁶ × (6² − 4²) = 4·10⁻⁵ J ; apériodique R = 1 kΩ ; frontière R = 300 Ω (pas de formule) ; E = 12 V → U_m = 12 V, même T₀ ;
  C × 4 ou L × 4 → T₀ ≈ 8 ms ; entretien k = R + r = 20 Ω ; phase : U_m = 6 V, u_C(0) = 3 V, φ = ±π/3, courbe qui monte → φ = −π/3.
  Le plan donne parfois d'autres nombres (e8 : L = 0,1 H, C = 10 µF → T₀ ≈ 6,3 ms) : une QUESTION peut garder ses nombres, mais ce que
  la voix dit de l'écran doit être ce que la simulation montre (C = 4 µF, T₀ ≈ 4 ms).
  Nationaux (figures.html, valeurs vérifiées) : 2021 R (fig_2021R : L = 0,51 H, r = 5 Ω, C = 100 µF, R₃ = 10 Ω → (a), R₄ = 100 Ω → (b),
  T = 45 ms, T₀ ≈ 44,9 ms, 1,80 → 1,26 mJ : 0,54 mJ) ; 2022 N (fig_2022N : E = 12 V, C = 50 µF, C₁, T₀ = 10 ms, L = 0,05 H) ;
  2020 N (fig_2020N : L = 1 H, r = 10 Ω, R = 90 Ω, T = 10 ms, C = 2,5 µF, k₀ = 100 Ω, I_m = 8 mA, φ = +π/2, E_t = 3,2·10⁻⁵ J,
  E_e(16 ms) ≈ 2,05·10⁻⁵ J avec i = 4,8 mA) ; 2023 N (fig_2023N : L = 1 H, T₀ = 4 × 0,5 = 2 ms, C = 0,1 µF, E_m(1,8 ms) = 1,8·10⁻⁶ J) ;
  2025 N (fig_2025N : C₀ = 1 µF, U₀ = 10 V, T = 4 × 7·10⁻⁵ = 2,8·10⁻⁴ s, i < 0 entre t_A et t_B, dE_T/dt = −r·i², |E_th| = 2,55·10⁻⁵ J) ;
  sans figure : 2016 N (C = 10 µF, q = 120 → 40 µC : 6,4·10⁻⁴ J), 2019 N (E = 10 V, C = 10 µF : 5·10⁻⁴ J ; u_C = −8 V : E_m = 1,8·10⁻⁴ J),
  2018 N (k = 5 → r = 5 Ω ; T₀ = 2,5 ms, C = 2,5 µF → L ≈ 63 mH), 2024 R (E = 5 V → u_b(0⁺) = −5 V).
- Les diapositives à visuel « cahier » du plan (l3) prennent `figures.html?fig=fig_carre` ; o2 prend `circuit-lc.html?vue=montage` (montage,
  charge, fleches) OU `figures.html?fig=fig_prerequis` (charge, bobine, derivee, recette — conseillé pour les trois gestes) ; jamais une vue hors contrat.
- La carte (o1 et cr) : moments centre depuis decharge regimes equation solution periode conditions lecture energie amortissement entretien
  national suite (+ complete en cr). Le bilan (bl) : fiche oscillations regimes equation lc solution periode conditions lecture energie
  amortissement entretien lacunes ; bl et cr portent `acquis=True` (comme dipole_RL_build/p4.py).
- Contrôle : `python3 outils/cours/notes/cours/circuit_RLC_build/check_part.py pN` doit finir par « AUCUNE ERREUR » (il vérifie mots
  exacts, ordre, moments, repères, voix sans chiffre/symbole, mots interdits, démonstrations). Corrige jusqu'à zéro.

## blocs_sN.json (ta séance = 3 blocs de 4 diapositives, découpage `plan.seances` de l'exploration)
Forme exacte (JSON valide, écrit avec l'outil Write) :
{"seance": {"id": "lc_sN", "titre": "Séance N — …", "blocs": [
   {"id": "lc_sN_b1", "titre": "…", "slide_ids": [4 ids de tes diapositives, dans l'ordre],
    "cahier": [{"texte": "…"}, …2 à 4 lignes reprises des student_trace…],
    "retrouver": {"prompt": "Cahier fermé : …", "attendu": "<formule ou définition EXACTE du cadre>", "competence_id": "C?"},
    "exercice": {…}}, … ]},
 "predictions": [ids de tes diapositives dont la question a prediction=True]}
Titres des séances (plan.seances) : 1 « Un condensateur qui se vide dans une bobine : oscillations et régimes » ; 2 « L'équation différentielle
et la période propre » ; 3 « Conditions initiales, oscillogrammes et échange d'énergie » ; 4 « Amortissement, entretien, deux nationaux ».
Blocs : s1 = [o1 o2 d1 d2] [d3 d4 d5 d6] [r1 r2 r3 r4] ; s2 = [e1 e2 e3 e4] [e5 e6 e7 e8] [p1 p2 p3 p4] ;
s3 = [c1 c2 c3 c4] [l1 l2 l3 l4] [en1 en2 en3 en4] ; s4 = [a1 a2 a3 a4] [a5 k1 k2 k3] [n1 n2 bl cr].
(Attention : les blocs de la séance 2 ne suivent pas les parties : le bloc 2 = e5 e6 e7 e8.)
`exercice` : reprend un exercice d'une diapositive du bloc s'il y en a un (`{"type", "reprend": "<slide_id>/e<i>", "prompt", "options"
(= choices), "correct", "explanation"}`, un vrai/faux garde `statements`), sinon un QCM court niveau national (`options` 3, `correct`, `explanation`),
avec `demonstration: {"parole", "lignes": [{"texte", "mot"}]}` s'il demande un calcul (parole aux règles de la voix, chaque `mot` extrait exact).
Au moins une prédiction par bloc. (Modèle : outils/cours/notes/cours/dipole_RL_build/blocs_s1.json.)

## Rapport final (court)
ids écrits, nombre de questions / prédictions / exercices / démonstrations, sortie finale de check_part, choix à faire valider.
