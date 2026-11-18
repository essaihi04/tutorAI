# Architecture — Transformations chimiques s'effectuant dans les deux sens (phys_ch11)

Revue de la logique du 18 novembre 2026 (skill `logique-de-cours`). Le travail part de la copie en attente, plus
récente que le cours en ligne. La nouvelle version est dans
`backend/data/courses/en_attente/phys_ch11_transformations_deux_sens.json`. Les pistes à mettre en voix sont dans
`phys_ch11_transformations_deux_sens_voix.json` : 14 pistes, toutes celles des deux questions d'observation ajoutées.

## 1. Sources et constats

**Profs (4 cours lus).** Le relevé est dans `sources_chimie_ch9_ch11.md`, chapitre C. Les cours lus :
- Mahajar et Tabit (AlloSchool, Cours 1) ;
- El Founani (AlloSchool, version LaTeX) ;
- Sbiro (pc1.ma, repris par El Goufifa) ;
- Hadjyne (pc1.ma).

L'ordre commun :
1. Brønsted : couple, demi-équation, l'eau ampholyte ; puis la réaction acide-base ;
2. le pH : rappel du log, pH-mètre étalonné ;
3. la réaction d'un acide avec l'eau et son tableau d'avancement ;
4. τ = x_f/x_max ;
5. l'expérience des deux sens : on ajoute de l'acide pur (le pH baisse) ou de l'éthanoate de sodium (le pH monte), d'où ⇌ ;
6. l'équilibre dynamique.

Ce que les profs font peu :
- la conductimétrie n'apparaît qu'en exercice ;
- aucun cours ne traite la dilution dans ce chapitre (Sbiro la place au chapitre « État d'équilibre »).

**Cadre.** Fiche `transformations_deux_sens`, capacités TD1 à TD8. TD7 (influence de la dilution et de la nature de
l'acide sur τ) est bien dans ce chapitre. Qr, K, Ka et pKa sont exclus (hors cadre de ce cours).

**National.** Ce qui revient le plus :
- τ calculé : 11 sessions sur 20 (par le pH, ou par σ en 2019 N) ;
- « montrer que τ = 10^(−pH)/C » : 2021 R ;
- la dilution augmente τ : 2021 R et 2025 R ;
- un dosage est total, τ ≈ 1 : 2024 R ;
- Brønsted et l'équation avec l'eau : presque chaque sujet d'acide.

**Logique de la copie en attente.** Elle suit déjà l'ordre commun des profs : Brønsted, pH, acide + eau, τ, deux
sens, équilibre dynamique. Les rappels de zéro sont en place (ion, concentration, puissances de dix et log, dilution
juste avant les dilutions). Deux manques au regard des règles du 18 novembre :
1. le tableau d'avancement est dit entièrement par la voix : l'élève ne construit aucune ligne lui-même ;
2. l'élève n'est jamais invité à **prévoir** ce que fait le pH quand on dilue : la voix donne 3,9 aussitôt.

Les deux questions d'observation existantes (`td_e1_inverse` : le pH monte ; `td_d2_taux` : les barres de τ) sont bien placées.

## 2. Architecture (ordre gardé), diapositive par diapositive

**=** : inchangée (voix gardée). **Obs** : question d'observation ajoutée.

### Séance 1 — Les bases depuis zéro ; acide, base, couple

| Diapo | Voix | Pourquoi ici |
|---|---|---|
| `td_o1_carte` | = | La carte du chapitre. |
| `td_o2_flacons` | = | L'énigme de départ : même concentration, pas le même pH. Elle donne envie de comprendre ; la réponse viendra avec τ. |
| `z1`, `z2`, `z3` | = | L'ion et le proton, la concentration, les puissances de dix et le log, enseignés de zéro juste avant le pH et Brønsted (règle 6). |
| `b1` → `b3b` | = | L'acide cède un proton, la base le capte, le couple, l'eau dans deux couples. Chaque fois l'animation d'abord, la définition lue ensuite. Ordre des profs. |

### Séance 2 — Réaction acido-basique, pH, réaction d'un acide avec l'eau

| Diapo | Voix | Pourquoi ici |
|---|---|---|
| `b4`, `p1`, `p2`, `p3` | = | La réaction acide-base, puis le pH (relation et sens), le calcul de [H₃O⁺] et le pH-mètre étalonné. |
| `p4`, `p5`, `p6` | = | L'acide puis la base avec l'eau. « Si la réaction était totale, le pH serait 2,0 ; on mesure 3,4 » : la conclusion « pas totale » est tirée d'une mesure, pas affirmée. |
| `td_a1_tableau` | = + **Obs** | Le tableau construit par l'élève. La voix s'arrête après l'état initial (« zéro et zéro ») et demande : « en cours, combien d'ions H₃O⁺ se sont formés ? » (C·V − x / x / 0). La voix reprend avec « السطر الثاني، en cours » (« la deuxième ligne, en cours »), qui confirme x. |
| `a2`, `a3`, `a4` | = | x_max calculé, x_f mesuré par le pH, τ = x_f/x_max. |

### Séance 3 — Taux d'avancement final, deux sens, état d'équilibre

| Diapo | Voix | Pourquoi ici |
|---|---|---|
| `a5`, `a6` | = | HCl (τ = 1), puis « montrer que τ = 10^(−pH)/C » (2021 R), démontré ligne par ligne et vérifié sur l'exemple A. |
| `e1`, `e1b`, `e2` | = | Les deux sens au labo animé, puis la double flèche. |
| `e3`, `e4` | = | L'état d'équilibre (le pH ne bouge plus), puis l'équilibre dynamique au niveau des entités (chocs dans les deux sens, TD5). |
| `e5`, `e6` | = | L'estérification (2016 N, annoncée « étudiée plus tard ») et 2017 N : τ décide entre totale et limitée. |
| `c1`, `c2`, `c3` | = | La conductimétrie donne τ. L'expérience des deux acides de même concentration vient d'abord, puis la relation, puis le calcul. |

### Séance 4 — Conductimétrie, dilution, questions du national, bilan

| Diapo | Voix | Pourquoi ici |
|---|---|---|
| `td_z4_dilution` | = | Le geste de dilution, enseigné juste avant de s'en servir. |
| `td_d1_dilution` | = + **Obs** | La voix s'arrête après « المحلول ولا dilué dix fois » (« la solution est diluée dix fois ») et la scène montre le deuxième bécher. Question : « que montre le pH-mètre ? » (diminue / augmente / ne change pas). La voix reprend avec « le pH égale trois virgule neuf ». C'est la prédiction du cas décisif du national 2021 R et 2025 R. |
| `d1b`, `d2`, `d3` | = | La 3ᵉ dilution, le tableau des τ (l'observation des barres existe déjà), puis la nature de l'acide. |
| `n1` → `n4b` | = | Nationaux 2021 R, 2019 N, 2023 N et 2024 R (méthode, puis calcul ligne par ligne). |
| `td_bl_fiche`, `td_cr_carte` | = | Bilan. |

## 3. Ce qui reste, et pourquoi

- **L'ordre n'est pas changé.** Il est déjà celui des profs, et chaque prérequis est enseigné juste avant son usage.
  Déplacer des diapositives coûterait des voix sans gain pour l'élève.
- **Le sens inverse (`e1`) est joué avant le sens direct (`e1b`)**, alors que les profs font l'inverse. Le texte de
  `e1b` renvoie à l'expérience de `e1` (« dans l'expérience d'avant, le pH a monté »). Les inverser obligerait à
  réécrire deux voix. Pédagogiquement, la surprise (le pH qui monte) ouvre bien la question des deux sens.
- **`a5` écrit déjà ⇌ pour l'acide éthanoïque**, avant l'expérience des deux sens. La double flèche est annoncée dès
  `b3` (pour le couple) et `p4`, avec « on la comprendra plus tard ». C'est une annonce, pas une preuve affirmée ; on la garde.
- **La dilution reste dans ce chapitre** (TD7 du cadre, deux nationaux), même si les profs la mettent ailleurs.
- **Brønsted, la base avec l'eau** (`p5`) : son τ est renvoyé au ch13 (Ka) ; ce cours n'en dit rien.

## 4. Besoins hors de ce cours (fichiers partagés, non modifiés)

- `td_b3b_eau`, `td_d1b_mesures`, `td_e2_fleche` et `td_n4b_calcul` continuent la scène de la diapositive d'avant
  (même URL). Il faudrait `?depart=<moment>` dans le kit partagé.
- `td_cr_carte` : un geste part 0,7 s après son mot (gestes trop serrés). À corriger à la prochaine voix de la carte.

## 5. 2ᵉ passe du 18 novembre : le national joué pas à pas, rien de décisif avant la réponse

Demande de l'utilisateur : « simple, animé, expliqué ; ne pas tout donner au départ ; laisser à l'élève le temps de
trouver seul ; une raison derrière chaque choix ». Le constat : `td_n1_figure` (2021 R) lisait la courbe et donnait
C₁, C₂ et la conclusion d'une traite ; l'élève ne faisait aucune étape. Les autres nationaux du cours (`td_n2` à
`td_n4b`) suivaient déjà leur calcul ligne par ligne, mais `td_n2` donnait la conversion d'unité, le piège du sujet,
avant que l'élève la cherche.

### Le sujet choisi : national 2021 R, exercice 1 (acide méthanoïque)

Pourquoi lui : c'est le seul sujet qui réunit les trois cas types du chapitre (l'équation avec l'eau et sa flèche,
« montrer que τ = 10^(−pH)/C », la dilution augmente τ), et ses questions se suivent comme notre cours. Ses valeurs sont
celles de la simulation : C_a = 1,0·10⁻¹ mol/L, pH = 2,38 ; S₁ pH 2,8 → τ₁ ≈ 0,10 ; S₂ pH 3,6 → τ₂ ≈ 0,45 ;
C₁ = 1,58·10⁻² et C₂ = 5,58·10⁻⁴ mol/L (corrigé du sujet). Les questions 1 à 4 (dosage) et 6 à 8 (rapport [A⁻]/[AH],
pKa) sont hors de ce chapitre (ch13) : elles ne sont pas jouées.

### Les quatre diapositives, une par question (`td_n1_figure` est remplacée)

Simulation nouvelle : `transformations-deux-sens-tableau/national.html?ex=2021R&vue=q1…q4` (une URL par diapositive :
la scène se recharge à chaque question). Chaque vue s'ouvre figée (`demarrer: reset`), la voix la conduit par
`play_until`, et une question d'observation arrête la voix avant l'étape décisive. Pendant la question,
`sim_avant: {conclusions: false}` tait tout ce qui suit l'étape de la question ; `sim_apres` l'écrit pendant que la
voix confirme.

| Diapo | Question du sujet | L'animation (les valeurs naissent de l'appareil) | L'élève répond avant la voix |
|---|---|---|---|
| `td_n1a_equation` | Q5 : l'équation avec l'eau | Bécher S_a peint, la sonde du pH-mètre descend, la valeur hésite puis se fixe à 2,38 ; l'équation s'écrit avec la flèche en blanc « ? ». Après la réponse : pH si totale = 1,0, 2,38 > 1,0, l'équation avec ⇌ encadrée (0,5 pt). | Quelle flèche ? (→ / ⇌ / ←). Raison : la flèche se justifie par une mesure (règle 4), pas par une habitude. |
| `td_n1b_montrer` | Q9 : montrer que τ = 10^(−pH)/C | Le tableau d'avancement, puis x_max = C·V (l'eau en excès). Après la réponse : la case x_f de H₃O⁺ encadrée, x_f = 10^(−pH)·V, τ en fractions encadré, S_a : τ = 0,042. | x_f = ? (10^(−pH)·V / C·V / 10^(−pH)). C'est la marche décisive de la démonstration ; les deux erreurs proposées sont celles des copies (x_max à la place de x_f, la concentration à la place de la quantité). |
| `td_n1c_courbe` | Q10 : lire τ sur la courbe | Deux béchers S₁, S₂ et leurs pH-mètres (2,8 puis 3,6) ; la courbe τ(pH) se trace ; la lecture de S₁ faite en pointillés (τ₁ ≈ 0,10) ; celle de S₂ tracée, sa valeur tue (« τ₂ = ? ») ; le tableau du sujet se remplit. | Lis τ₂ (0,10 / 0,45 / 3,6). La première lecture est montrée, la deuxième faite par l'élève (règle 3). |
| `td_n1d_dilution` | Q10-11 : C, puis l'effet de la dilution | Le tableau (pH, τ), C = 10^(−pH)/τ, C₁ puis C₂ dans le tableau ; deux béchers peints, S₂ avec moins de molécules d'acide. Après la réponse : « C₂ < C₁ et τ₂ > τ₁ : la dilution augmente τ » encadré, comme le barème. | Que fait τ quand on dilue ? |

La courbe du sujet est redessinée pour passer par les deux lectures du corrigé (τ = 1/(1 + 10^(1,084·(3,68 − pH))),
jamais écrite : Ka est au ch13). Les exercices de fin de cours et la figure du cahier de `td_n1_figure` passent sur
`td_n1d_dilution` et `td_n1c_courbe` (mêmes textes, mêmes voix). Le cahier écrit chaque question comme le barème.

**Séances.** Le bloc `td_s3_b2` garde dilution, nature de l'acide et 2019 N (son ardoise devient le vrai/faux déjà
voicé de `td_n2`, `reprend: td_n2_conductivite/e0`). Le nouveau bloc `td_n_b1` (les quatre diapositives, cahier Q5,
Q9, Q10-11, `retrouver` « montre que τ = 10^(−pH)/C », ardoise C₂ reprise de l'ancien bloc) ouvre une **séance 5**
avec le bloc de rédaction et le bilan : la séance 4 aurait eu 15 diapositives. Compétences : `td_n1a` → C7 (rédiger),
`td_n1b` → C3, `td_n1c` et `td_n1d` → C6.

### Rien de décisif avant la réponse

- `td_n2_conductivite` (2019 N) : nouvelle question d'observation sur la conversion (« C en mol/m³ ? » : 1,0·10⁻³ /
  1,0 / 1,0·10⁻⁶), le piège du sujet. `conductimetrie.html?vue=national` accepte `conclusions` : à `false`, la ligne de
  conversion s'écrit « = ? mol/m³ » et l'application numérique et le résultat se taisent. Voix de la diapositive gardée.
- `td_d2_taux` : sa question (« que font les barres ? ») se posait après la flèche jaune qui monte d'une barre à
  l'autre. `diluer.html` accepte `conclusions` : à `false`, la flèche et la conclusion se taisent
  (`sim_avant` / `sim_apres` ajoutés). Voix gardée.
- `td_a1_tableau`, `td_d1_dilution`, `td_e1_inverse` relus : rien ne s'écrit avant la réponse (le `play_until`
  d'`avancement.html` et de `dilution.html` rejoue depuis zéro et s'arrête avant la ligne « en cours » / le pH de S₂ ;
  `td_e1_inverse` avait déjà `sim_avant`).
- Les deux erreurs « introuvable » (`td_d2_taux`, repères `ligne_1`, `ligne_2`) venaient d'un nom calculé
  (`'ligne_' + (i + 1)`) : `diluer.html` les nomme maintenant en clair. Elles disparaissent aussi pour le cours en ligne.

Compatibilité : `conclusions` vaut `true` par défaut dans les trois pages ; le cours en ligne, qui ne l'envoie pas,
voit exactement la même chose qu'avant.

### Mots

Les 4 diapositives et les 35 champs d'observation passent `verifier_mots` (sur la copie en attente :
`verifier_mots.py en_attente/phys_ch11_transformations_deux_sens …`, et pour les observations le même calcul de
fréquence). Remplacés : « oxonium » → « H trois O plus », « méthanoate » → « H C O O moins », « barème » → « la réponse
qu'il faut écrire à l'examen », « السؤال الخامس / التاسع / العاشر / الحادي عشر » → « la question cinq / neuf / dix /
onze », « محاليل » → « solutions », « dilué كثر » → « فيها الما كثر », « trait » → « la ligne », « قسنا » → « لقينا »,
« نحلوه » → « نجاوبو », « ونتسناو حتى يوقف » → « كيتبدل شوية، ومن بعد كيبقى هو هو », « كيكبر » → « كيطلع ».
Gardés (termes du programme, à écouter) : « méthanoïque » (nom de l'acide du sujet) ; « siemens » (dit « si mènsse »).

**À changer à la prochaine voix des diapositives déjà voicées** (non réécrites ici pour garder leurs voix) :
« l'afficheur » (`td_o2_flacons`, `td_p3_phmetre`, `td_p6_totale`, `td_e1_inverse`, `td_e3_etat`, `td_c1_ions`,
`td_d1_dilution`) → « le p H mètre » / « الرقم » ; « chronomètre » (`td_e3_etat`) → « الوقت » ; « béchers »
(`td_c1_ions`, `td_d1b_mesures`, `td_d3_nature`) → « les deux / trois bécher » ou « الكيسان » ; « oxonium » et
« éthanoate » (`td_e1_inverse`, `td_e3_etat`) → « H trois O plus », « C H trois C O O moins » ; « diluée »
(retour r1 de l'observation de `td_d2_taux`).

### Voix et vérifications

- 39 pistes ajoutées à `phys_ch11_transformations_deux_sens_voix.json` (4 diapositives, 35 champs d'observation ;
  champ `passe: 2e_passe_18_11`), 53 en tout.
- `verifier_pointage_simulations.py --ecarts` : 0 « introuvable » (copie en attente et cours en ligne, contre 2 et 2).
  Les écarts GESTE des 4 nouvelles diapositives viennent de leur voix absente (le script compte 1 s par geste sans
  durée de piste) ; à revoir une fois la voix faite. `td_n2_conductivite` garde son écart DEPART (`start`, la page
  `conductimetrie.html` rejoue depuis zéro à chaque `play_until`).
- `national.html` vérifiée dans Chromium (aucune erreur, `play_until` sur chaque moment, `conclusions` false/true,
  captures 1024 × 560 et 724 × 350) ; `node --check` sur les scripts des trois pages ; `verifier_formules.py` : rien
  pour ce dossier.

### Ce qui n'a pas pu être fait

- Les voix (39 pistes) : à faire sur le VPS.
- Téléphone paysage : `national.html` tient tout son dessin dans un rectangle de 700 × 270 (deux points invisibles fixent la
  boîte d'encre, `scene: {ajuster: true}`), écrit de 17 à 22 et tient le plancher du kit à 15 px dans cette page seule.
  Mesuré en 724 × 350 : texte de base ≥ 15,6 px à l'écran (étages des fractions compris), rien hors du canvas, aucun
  chevauchement (captures q1-q4, aussi en 1024 × 560). Les indices et exposants restent à 62 % de leur ligne (≈ 10 px),
  comme partout dans le kit.
- `?depart=<moment>` du kit partagé (déjà noté au § 4) reste un besoin.
