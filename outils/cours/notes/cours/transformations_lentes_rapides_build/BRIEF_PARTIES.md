# Brief — écrire une partie du cours phys_ch9_transformations_lentes_rapides (« Transformations lentes et transformations rapides »)

Tu écris UN fichier de contenu `outils/cours/notes/cours/transformations_lentes_rapides_build/pN.py` (N donné dans ta mission) et UN fichier
`outils/cours/notes/cours/transformations_lentes_rapides_build/blocs_sN.json` (les 3 blocs de ta séance). Rien d'autre. Messages en français simple.
Travaille depuis la racine du dépôt /home/user/tutorAI. Pas de commit, pas de push, pas de git checkout/stash/reset, pas de sous-agent.
Les simulations sont écrites EN MÊME TEMPS par d'autres agents : tu ne les ouvres pas ; tu n'utilises que les vues, moments et repères
du contrat (copiés dans les tables MOMENTS / REPERES de `transformations_lentes_rapides_build/outils.py`).

## Répartition (fixe : build.py importe exactement ces noms)
| Fichier | Séance | Diapositives du plan (dans l'ordre) | Variables exportées |
|---|---|---|---|
| p1.py + blocs_s1.json | 1 | o1 o2 · x1 x2 x3 · x4 x5 x6 · x7 x8 x9 x10 (12) | `PARTIE1` = o1 o2 ; `PARTIE2` = x1…x3 ; `PARTIE3` = x4…x6 ; `PARTIE4` = x7…x10 |
| p2.py + blocs_s2.json | 2 | r1 r2 r3 r4 · r5 r6 r7 · r8 f1 f2 f3 f4 (12) | `PARTIE5` = r1…r4 ; `PARTIE6` = r5 r6 r7 ; `PARTIE7` = r8 f1 f2 f3 f4 |
| p3.py + blocs_s3.json | 3 | f5 f6 f7 f8 · t1 t2 t3 t4 · n1 n2 · bl cr (12) | `PARTIE8` = f5…f8 ; `PARTIE9` = t1…t4 ; `PARTIE10` = n1 n2 ; `BILAN` = bl cr |
Titres des parties (build.py) : Ouverture · I. Oxydants et réducteurs · II. Les demi-équations électroniques · III. L'équation d'oxydoréduction ·
IV. Transformations rapides et lentes · V. Voir, classer, titrer · VI. La température, facteur cinétique · VII. La concentration des réactifs ·
VIII. Trempe, vie quotidienne et catalyseur · IX. Deux sujets du national · X. Bilan du chapitre.
Chaque pN.py commence par `from outils import *` et ne définit que ses listes (une liste Python de S(...)).

## À lire d'abord
1. `.agents/skills/cours-concentration/SKILL.md` (en entier), `.agents/skills/voix-du-cours/SKILL.md` section 1 (texte parlé),
   `.agents/skills/professeur/SKILL.md` (règles), `outils/cours/notes/cours/methode_blocs/BRIEF_AGENTS.md` (blocs : cahier, retrouver, exercice).
2. L'exploration : `backend/data/curriculum/exploration/transformations_lentes_rapides.json` — surtout `plan.diapositives` (TES diapositives :
   id, title, lead, marche, visuel, question, prediction, competences, demonstration), `plan.seances`, `notions_complexes` (marches),
   `pieges`, `erreurs_examen`, `analogies_validees`, `a_ne_pas_dire`, `redaction_nationale`, `cas_types`, `questions_eleves`, `decisions_utilisateur`.
   Et l'analyse des nationaux : `outils/cours/notes/cours/transformations_lentes_rapides_build/nationaux.md`.
3. Le cadre : `backend/data/curriculum/cadre_reference_2bac_pc.json` → `chapitres.transformations_lentes_rapides` (formules `ecriture`, `dit`,
   `hors_cadre.mots` INTERDITS).
4. Le contrat des simulations : `outils/cours/notes/cours/transformations_lentes_rapides_contrat_simulations.md` (vues, moments, repères EXACTS,
   valeurs ; « Diapositives servies » dit quelle vue va avec quelle diapositive).
5. Le MODÈLE (forme, ton, densité) : `outils/cours/notes/cours/circuit_RLC_build/p1.py` (lis 3-4 diapositives) et les outils
   (S, vis, Q, DEMO, EX, VF, PU, R, C, SP dans `transformations_lentes_rapides_build/outils.py`, même API).

## Règles
- Une diapositive par entrée de `plan.diapositives` qui t'est confiée, DANS L'ORDRE, id = `tl_<id du plan>_<un mot>` (ex. `tl_x4_oxygene`,
  `tl_f2_bains`). Une seule idée nouvelle par diapositive. Compétence = la PREMIÈRE de la liste `competences` du plan.
  `slide_type` parmi situation | concept | explanation | application | evaluation.
- Chaque diapositive : title, lead, 3-4 bullets, student_trace (= cahier, écrit comme le barème), visuel `vis("page.html?vue=…", caption, alt)`
  (toujours la vue dans l'URL ; bilan.html et carte.html sans vue), `fr` (français parlé) et `mixed` (darija simple + termes du programme en
  français, règles voix-du-cours : AUCUN chiffre, aucun symbole (= + → ⇌ ⁺ ⁻ ° % ₂…), nombres et unités EN LETTRES, phrase entièrement française
  > 10 mots coupée par des virgules ; pas de tachkil), une question `Q(...)` (3 options, bonne réponse PAS toujours au même rang,
  `prediction=True` si le plan dit prediction), `pointage=[PU("extrait exact de mixed", "moment"), R("extrait", "repère")]` dans l'ordre de la
  voix (ce que la voix décrit, la simulation le montre à ce moment), et `centre=[("formule", "extrait de mixed")]` quand une équation naît.
- Toute question ou exercice de calcul / « équilibre / écris l'équation / combien / détermine / justifie un nombre » porte
  `DEMO(parole, [(ligne écrite, extrait exact de parole), ...])` (style « la relation: … le résultat: … » ; pour une demi-équation : « le couple: …
  les oxygènes: … les hydrogènes: … les charges: … le résultat: … »). Vérifie CHAQUE équilibrage (éléments ET charges) avec python.
- Les diapositives d'application et de national portent 1 à 3 exercices `EX(...)` / `VF(...)` niveau national (avec DEMO si calcul).
- Écrit : équations EXACTEMENT comme le cadre (formules `ecriture`) : demi-équation `Ox + n e⁻ ⇌ Red` (double flèche ⇌), réaction avec `→` ;
  charges en exposant Unicode (Cu²⁺, MnO₄⁻, S₂O₈²⁻, e⁻, H⁺), indices Unicode (H₂O₂) ; couple écrit `Cu²⁺/Cu` (l'oxydant d'abord) ; virgule décimale ;
  unités mol/L, mmol, min, °C. On écrit H⁺ (on dit une fois en x4 que H₃O⁺ est le même ion). Jamais « x = texte » pour une définition (utilise « : »).
- Voix : on dit les NOMS : « ion permanganate », « ions manganèse deux », « ions fer deux / fer trois », « ions iodure », « diiode »,
  « eau oxygénée », « acide oxalique », « dioxyde de carbone », « ions thiosulfate », « ions tétrathionate », « ions peroxodisulfate »,
  « ions sulfate », « ions cuivre deux », « ions zinc deux », « H plus », « électrons », « molécules d'eau », « vingt degrés Celsius »,
  « zéro virgule un mole par litre », « millimole », « minutes ». Une demi-équation se dit comme le `dit` du cadre (« … plus cinq électrons donne … »).
  Couleurs : « بنفسجي » (violet), « قهوي / brun », « أزرق », « صفر / jaune » — préfère les mots du corpus (les agents précédents ont
  remplacé les darija rares : « بلون jaune », « بلون orange »).
- Mots INTERDITS partout (écrit et voix) : `hors_cadre.mots` (chocs efficaces, théorie des collisions, énergie d'activation, ordre de réaction,
  loi de vitesse, mécanisme réactionnel, nombre d'oxydation, potentiel standard…) et `a_ne_pas_dire` (motifs : « l'oxydant cède », « le réducteur
  capte », « la température augmente la quantité », « le catalyseur change l'état final »). Pour la température : « les entités s'agitent plus
  et se rencontrent plus souvent ». Catalyseur (t3, t4, n1) : définition seulement (accélère, ne figure pas dans l'équation, même état final).
- Valeurs (à citer telles quelles, voir le contrat) : température 20 °C et 40 °C (palier atteint environ trois fois plus tôt à 40 °C ;
  courbes : vers 30 min à 20 °C, vers 10 min à 40 °C), [I⁻]₀ = 0,1 puis 0,2 mol/L avec H₂O₂ limitant (même palier 2 mmol de diiode) ;
  si on double H₂O₂ (limitant) : palier 4 mmol (piège) ; tableau une_variable : exp. 1 (20 °C ; 0,1 mol/L), 2 (40 °C ; 0,1), 3 (40 °C ; 0,2) ;
  catalyseur : peroxodisulfate + iodure, quelques gouttes d'ions fer II ; courbes catalyseur : palier x_f = 0,3 mol, C₁ avec (plus tôt), C₂ sans.
  Nationaux : n1 = 2025 N (estérification acide éthanoïque + propan-1-ol ; exp. 1 θ₁, exp. 2 θ₂ > θ₁, exp. 3 θ₂ + H₂SO₄ ; courbes (a) (b) (c) ;
  (a) ↔ 3, (b) ↔ 2, (c) ↔ 1 ; vrai/faux justifié « x_f est le même » : vrai) ; n2 = 2017 R (estérification acide éthanoïque + éthanol, tubes
  au bain-marie à 100 °C, prélèvement dans l'eau glacée avant le dosage de l'acide restant : bloquer la réaction ; proposer deux facteurs pour
  accélérer : élever la température, ajouter un catalyseur — ou augmenter la concentration d'un réactif). Dire « une réaction entre un acide
  et un alcool, l'estérification, qu'on étudiera plus tard ».
- La carte (o1 et cr) : moments centre couple demi_equation equation rapide lente temperature concentration catalyseur trempe national suite
  (+ complete en cr). Le bilan (bl) : fiche oxydoreduction demi_equation equation rapide_lente facteur temperature concentration catalyseur trempe
  lacunes ; bl et cr portent `acquis=True` (modèle circuit_RLC_build/p4.py, regarde bl et cr). bl et cr portent une question courte (sans prédiction).
- Contrôle : `python3 outils/cours/notes/cours/transformations_lentes_rapides_build/check_part.py pN` doit finir par « AUCUNE ERREUR » (mots
  exacts, ordre, moments, repères, voix sans chiffre/symbole, mots interdits, démonstrations). Corrige jusqu'à zéro.

## blocs_sN.json (ta séance = 3 blocs de 4 diapositives, découpage `plan.seances`)
Forme exacte (JSON valide, écrit avec l'outil Write) — modèle : `outils/cours/notes/cours/circuit_RLC_build/blocs_s1.json` :
{"seance": {"id": "tl_sN", "titre": "Séance N — …", "blocs": [
   {"id": "tl_sN_b1", "titre": "…", "slide_ids": [4 ids de tes diapositives, dans l'ordre],
    "cahier": [{"texte": "…"}, …2 à 4 lignes reprises des student_trace…],
    "retrouver": {"prompt": "Cahier fermé : …", "attendu": "<formule ou définition EXACTE du cadre / du cahier>", "competence_id": "C?"},
    "exercice": {…}}, … ]},
 "predictions": [ids de tes diapositives dont la question a prediction=True]}
Titres des séances : 1 « Oxydants, réducteurs et équations d'oxydoréduction » ; 2 « Transformations rapides et lentes ; la température » ;
3 « La concentration, la trempe, le catalyseur, deux nationaux et le bilan ».
Blocs : s1 = [o1 o2 x1 x2] [x3 x4 x5 x6] [x7 x8 x9 x10] ; s2 = [r1 r2 r3 r4] [r5 r6 r7 r8] [f1 f2 f3 f4] ; s3 = [f5 f6 f7 f8] [t1 t2 t3 t4] [n1 n2 bl cr].
`exercice` : reprend un exercice d'une diapositive du bloc s'il y en a un (`{"type", "reprend": "<slide_id>/e<i>", "prompt", "options"
(= choices), "correct", "explanation"}`, un vrai/faux garde `statements`), sinon un QCM court niveau national (`options` 3, `correct`, `explanation`),
avec `demonstration: {"parole", "lignes": [{"texte", "mot"}]}` s'il demande un calcul ou un équilibrage (parole aux règles de la voix, chaque `mot`
extrait exact). Au moins une prédiction par bloc (le plan en donne déjà une par bloc).

## Rapport final (court)
ids écrits, nombre de questions / prédictions / exercices / démonstrations, sortie finale de check_part, choix à faire valider.
