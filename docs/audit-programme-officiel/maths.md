# Audit du programme de mathématiques face au cadre officiel (15 novembre 2026)

**Référence** : cadre de référence de l'examen national, mathématiques, série sciences expérimentales (filières Sciences physiques et SVT), MEN / CNEEO, options internationales, octobre 2015 (note 117 X 15). Transcription : `backend/cours 2bac pc/cadres de references 2BAC PC/cadre-de-reference-de-l-examen-national-maths-sciences-experimentales.json`.

Objectifs officiels : 1.1.1–1.1.5 (suites), 1.2.1–1.2.24 (continuité, dérivation, étude de fonctions, primitives, ln, log décimal, exp, équations différentielles), 1.3.1–1.3.4 (calcul intégral), 2.1.1–2.1.3 (produit scalaire dans V3), 2.2.1–2.2.6 (applications dans l'espace), 2.3.1–2.3.4 (produit vectoriel), 2.4.1–2.4.9 (nombres complexes), 2.5.1–2.5.6 (probabilités). Poids : analyse 55 %, géométrie de l'espace 15 %, complexes et probabilités 30 %.

Fichiers comparés : `perimetre.json` (partie Mathématiques), `mathematiques.json`, `mathematiques_blueprint.json`, `programme_semestre1.json`, fiches maths de `cadre_reference_2bac_pc.json` (limites_continuite, derivation_etude_fonctions, suites_definition, primitives, fonctions_ln, operations_formes), et `prerequis.json` (liste des chapitres).

## Étape 1 — Notre programme face au cadre officiel

### (a) Ce que nous avions en trop (hors cadre officiel) — retiré

| Où | Contenu | Pourquoi c'est hors cadre | Correction |
|---|---|---|---|
| `mathematiques.json`, `perimetre.json`, `prerequis.json` | Chapitre « Arithmétique dans Z » (PGCD, Bézout, congruences, nombres premiers), noté « rattrapage principalement » | Aucun sous-domaine d'arithmétique dans le cadre de la série sciences expérimentales (programme de la filière Sciences mathématiques) | Chapitre retiré des trois fichiers ; terme générique hors programme ajouté dans `perimetre.json` (PGCD, PPCM, Bézout, congruences, Fermat, restes chinois) |
| `mathematiques.json` (convergence), `perimetre.json` (convergence : notion, terme, méthode, démonstration admise) | Suites adjacentes | Absentes des objectifs 1.1.1 à 1.1.5 et des nationaux PC 2016-2025 (seulement citées par les orientations pédagogiques) | Retirées ; terme hors programme ajouté au chapitre convergence ; dans la fiche `suites_definition`, passées de « toléré si annoncé » à `hors_cadre.mots` |
| `mathematiques.json` (transformations) | « Similitude directe : z' = az + b » | Le cadre ne cite que translation, homothétie, rotation (2.4.5, 2.4.6) ; `perimetre.json` la classait déjà hors programme | Retirée |
| `mathematiques.json` (géométrie complexe) | « Affixe du barycentre » | Pas dans 2.4.4 ; `perimetre.json` classait déjà « barycentre » hors programme | Retiré (on garde le milieu) |
| `mathematiques.json` (géométrie complexe) | Ensemble de points `|z−a|/|z−b| = k` | Pour k ≠ 1 c'est un cercle d'Apollonius, absent du cadre ; seules les traductions de distance, angle, alignement, orthogonalité sont exigées (2.4.4) | Remplacé par cercle `|z−a| = r` et médiatrice `|z−a| = |z−b|` |
| `perimetre.json` (geometrie_complexe) | « Points cocycliques » | Absent de 2.4.4 / 2.4.7 | Remplacé par le parallélogramme (z_A + z_C = z_B + z_D), déjà au programme |
| `perimetre.json` (fonctions_exp) | « Exponentielle de base a : a^x = e^(x ln a), dérivée ln a·a^x » (et le terme « exponentielle de base a ») | Le cadre ne cite que l'exponentielle népérienne (1.2.20, 1.2.21) et 10^x avec le logarithme décimal (1.2.18) ; le cours ln exclut déjà le logarithme de base a | Remplacé par « 10^x = e^(x ln 10), 10^x = a ⇔ x = log a » ; terme hors programme « exponentielle / logarithme de base a, changement de base » ajouté (fonctions_exp et fonctions_ln) |
| `cadre_reference_2bac_pc.json` (limites_continuite) | Restes de la dichotomie (LC7) retirée le 15/11 : deux formules `capacite: LC7` ((a+b)/2, f((a+b)/2)), mots-clés « dichotomie » et « amplitude », décision « gardée en bloc court pour les devoirs » | Hors cadre officiel (1.2.3–1.2.4 demandent existence, unicité, localisation, pas la méthode de dichotomie) ; contradiction avec `hors_cadre.mots` qui contenait déjà « dichotomie » | Formules et mots-clés retirés ; décision réécrite (« retirée, pas de partie pour les devoirs ») |

### (b) Ce qui manquait — ajouté

| Où | Manque | Objectif officiel | Correction |
|---|---|---|---|
| `mathematiques.json` (analyse) | Continuité, image d'un intervalle, théorème des valeurs intermédiaires, dérivabilité, résolution graphique, problèmes de minimum / maximum | 1.2.1 à 1.2.10, 1.2.12 | Ajoutés au chapitre « Limites, continuité, dérivation et étude complète d'une fonction » |
| `mathematiques.json` (analyse) | Équations différentielles y' = ay + b et y'' + ay' + by = 0 | 1.2.23, 1.2.24 | Ajoutées (chapitre exponentielle) |
| `mathematiques.json` (intégration) | Volume d'un solide de révolution ; propriétés de l'intégrale | 1.3.2, 1.3.4 | Ajoutés |
| `mathematiques.json` (ln) | Logarithme décimal, systèmes logarithmiques, lim ln(1+x)/x | 1.2.17, 1.2.18, 1.2.19 | Ajoutés |
| `mathematiques.json` (exp) | Systèmes exponentiels, lim (e^x − 1)/x | 1.2.20, 1.2.21 | Ajoutés |
| `mathematiques.json` (suites) | Suites homographiques u_{n+1} = (au_n+b)/(cu_n+d), suites de référence, limite de f(u_n), problèmes (seuil, somme) | 1.1.1, 1.1.2, 1.1.3, 1.1.5 | Ajoutés |
| `mathematiques.json` (complexes) | Formules d'Euler et linéarisation ; équations se ramenant au second degré ; mesure d'un angle, orthogonalité | 2.4.3, 2.4.9, 2.4.4 | Ajoutés |
| `mathematiques.json` (géométrie) | Sphère de diamètre [AB] (MA·MB = 0), plan défini par trois points (produit vectoriel), distance d'un point à une droite, position droite-sphère, produit scalaire dans V3 | 2.2.5, 2.3.2, 2.3.3, 2.2.6, 2.1.1–2.1.3 | Ajoutés |
| `mathematiques.json` (probabilités) | « Modèle de dénombrement convenable » formulé comme dans le cadre | 2.5.1 | Ajouté |
| `perimetre.json` (etude_fonction) | Résolution graphique de f(x) = g(x), f(x) ≤ g(x) ; problèmes de valeur minimale / maximale (présents dans le cadre, absents des notions) | 1.2.10, 1.2.12 | Deux notions ajoutées |
| `mathematiques.json`, `mathematiques_blueprint.json` | Poids officiels (55 % / 15 % / 30 %) et chemin du cadre officiel | tableau a | Ajoutés (`poids_officiels`, `cadre_reference`) |

Le reste de `perimetre.json` couvrait déjà tous les objectifs officiels (vérifié objectif par objectif : 1.1.1–1.1.5, 1.2.1–1.2.24, 1.3.1–1.3.4, 2.1.1–2.5.6).

### (c) Ce qui était mal formulé ou mal classé — corrigé

| Où | Avant | Après | Raison |
|---|---|---|---|
| `mathematiques.json` `level` | « Sciences Physiques / Sciences Mathématiques » | « Sciences Expérimentales, filière Sciences Physiques (PC) BIOF » | Le cadre est celui des sciences expérimentales ; la filière SM a un autre programme (c'est ce mélange qui avait fait entrer l'arithmétique et les suites adjacentes) |
| `mathematiques.json` `cadre_reference` | « Cadre de Référence MEN » sans source | Chemin du JSON officiel | Traçabilité |
| `mathematiques.json` (complexes) | « Résolution d'équations du second degré dans C (z²+bz+c=0) » | « az² + bz + c = 0 avec a, b, c réels (2.4.8) » | Le cadre précise « coefficients réels » |
| `mathematiques.json` (géométrie) | « Intersection de plans » comme thème | Retiré des thèmes ; dans `perimetre.json` marqué « rappel de 1re bac, pas un objectif du cadre 2e bac » | Pas d'objectif 2e bac |
| `mathematiques.json` / `perimetre.json` (probabilités) | « Formule des probabilités totales » sans rattachement | « lue sur l'arbre, outil de 2.5.3 » | Le cadre parle de probabilité conditionnelle appliquée au calcul de l'intersection ; on garde l'outil, sans en faire un objectif à part (« Bayes » reste hors programme) |
| Chaque thème de `mathematiques.json` | Pas de numéro officiel | Numéro officiel entre parenthèses (1.2.3, 2.4.8…) | Chaque notion cite sa notion officielle |
| `cadre_reference_2bac_pc.json` (6 fiches maths) | Capacités « provisoires, à collationner », « texte officiel non relu » | Champ `officiel` sur chaque capacité (ex. LC5 → 1.2.3, NC7 → 2.4.2) et champ `collation_officielle` | Collation faite avec le JSON officiel |
| `cadre_reference_2bac_pc.json` (primitives) | « linéarisation » dans `hors_cadre.mots` | Déplacée dans `tolere_si_annonce` (« 2.4.3, chapitre des complexes, plus tard ») | La linéarisation EST au cadre (2.4.3) ; elle est seulement prématurée dans le cours des primitives |
| `cadre_reference_2bac_pc.json` (operations_formes) | « racine n-ième » dans `hors_cadre.mots` | « racine n-ième d'un complexe » | La racine n-ième d'un réel positif est au programme (fiche limites_continuite, LC10) ; seule celle d'un complexe est hors cadre |
| `cadre_reference_2bac_pc.json` (limites_continuite) | Source : « la dichotomie et les puissances rationnelles … à collationner » | Racine n-ième et puissances rationnelles rattachées à 1.2.22 (« fonctions figurant au programme ») ; dichotomie retirée | Décision explicite |
| `programme_semestre1.json` (maths) | `cle` présentée comme une clé de `perimetre.json`, alors que limites_continuite, derivation_etude_fonctions et primitives n'y existent pas | Champs `perimetre` (clés de `perimetre.json` qui couvrent le chapitre) et `objectifs_officiels` ajoutés ; `_note_maths` explique que `cle` est la clé de la fiche du cadre | Le lien chapitre → périmètre était cassé pour trois chapitres sur six |

Points laissés tels quels, après vérification :
- **Racine n-ième et puissances rationnelles** (cours ch1, ch4) : pas d'objectif propre dans le cadre, mais fonctions du programme (1.2.22 « fonctions figurant au programme ») et nécessaires aux primitives de xʳ. Gardées. À trancher par l'utilisateur s'il veut les retirer.
- **« convexité »** reste un terme hors programme (sens de l'inégalité de convexité) ; « courbe convexe / concave » par le signe de f'' reste permis (le cadre dit « concavité »).
- **Fonction définie par une intégrale, valeur moyenne, suites d'intégrales** (perimetre, integration) : gardées comme applications des propriétés de l'intégrale (1.3.2) et des primitives.
- Un test existant échoue pour la SVT (`notion_information_genetique` sans chapitre dans `svt.json`) : hors de ma matière, non touché.

## Étape 2 — Les cours de maths (6 cours + l'ancien cours v1)

Chaque cours a été relu en entier contre le cadre officiel : écran, voix (fr et mixed), questions, réactions préparées, cahier, figures, séances, simulations du chapitre. Tous les calculs, résultats d'exercices et bonnes réponses de QCM ont été refaits (python, sympy, cmath). Aucune partie de cours n'est hors cadre officiel ; les erreurs étaient surtout dans les **réactions préparées**.

| Cours | Corrections | Voix à refaire |
|---|---|---|
| ch1 limites et continuité | 17 + 4 (voix « devoir » et asymptote, ajoutées après relecture) ; 53 audios orphelins de la dichotomie supprimés | 6 pistes (3 diapositives) |
| ch1 ancien cours v1 (fixture de tests) | 1 (prolongement par continuité) | sans audio |
| ch2 dérivation et étude de fonctions | 22 | 4 réactions |
| ch3 suites numériques | 17 | 3 |
| ch4 primitives | 5 | 3 |
| ch5 fonction ln | 29 | 12 réactions |
| ch6 nombres complexes (partie 1) | 22 | 13 |

Corrections ajoutées après la relecture du ch1 (en plus du tableau de l'agent ci-dessous) :

| Diapositive | Avant → après | Raison |
|---|---|---|
| `lc_l13_devoir` (voix fr, mixed) | « À toi, comme en devoir. » / « دابا نتا، بحال فالفرض. » → « À toi. » / « دابا نتا. » | Pas d'étiquette « devoir » |
| `lc_r9_valeur_absolue` (voix fr, mixed) | « Un exemple complet de devoir. » → « Un exemple complet. » (et mixed) | Idem |
| `lc_l11_interpreter` (voix fr, mixed) | « l'écart … se rapproche de zéro, sans jamais l'atteindre » → « l'écart … tend vers zéro » | Une courbe peut couper son asymptote : la phrase était donnée comme règle générale |
| `media/audio/courses/math_ch1_limites_continuite/` | 53 pistes `lc_d1…lc_d4` (dichotomie) | Supprimées : plus aucune diapositive ne les utilise |

### math_ch1_limites_continuite

**Conformité.** Ouverture et I (rappels de limites, nécessaires pour 1.2.1 et 1.2.22) ; II continuité en un point → 1.2.1 ; III continuité sur un intervalle (√u, composée) → 1.2.1 et 1.2.2 ; IV image d'un intervalle → 1.2.2 ; V théorème des valeurs intermédiaires, solution unique, f(α) = 0 → 1.2.3 et 1.2.4 ; VI (ex-VII) fonction réciproque, J = f(I), sens de variation, courbe symétrique → 1.2.11 ; VII (ex-VIII) racine n-ième, réciproque de xⁿ, puissances rationnelles (toujours x > 0) → 1.2.11, gardées sur décision ; VIII (ex-IX) limites avec ⁿ√ → 1.2.1 et 1.2.22 ; IX (ex-X) problème national et bilan → 1.2.3, 1.2.4, 1.2.11, 1.2.22. Compétences K1 à K10 (K6 = dichotomie, déjà retirée) : toutes rattachées à une notion officielle. Aucune partie hors programme.

Vérifié sans erreur : les résultats de tous les QCM, rappels, exercices de séance et figures du cahier, refaits à la main (f(1/2) = −3/8, √110 − 10 ≈ 0,488, √10100 − 100 ≈ 0,499, 3⁵ = 243 > 2⁷ = 128, 2^(2/3 + 1/3 + 1/2) = 2√2, ⁸√81 = √3, (∛(x+8) − 2)/x → 1/12, etc.). Les conditions sont justes partout : x > 0 pour x^(p/q), x ≥ 0 pour ⁿ√, u ≥ 0 pour √u, « strictement » monotone pour l'unicité et pour la réciproque. « Prolongement par continuité » n'est ni écrit ni dit (on demande seulement « quelle valeur donner à f(1) »). Aucun terme bijection, Rolle, L'Hôpital ou epsilon. La voix ne cite jamais de numéro de partie.

| diapositive (id) | avant → après | raison |
|---|---|---|
| lc_partie7 / 8 / 9 / lc_bilan (titres de partie) | VII, VIII, IX, X → VI, VII, VIII, IX | Il manquait la partie VI depuis le retrait de la dichotomie. Seul l'écran change : la voix ne cite aucun numéro. |
| simulation calculs.html?vue=e1_probleme (lc_e1_probleme_b/c), `calculs-donnees.js` | lignes « 4) f(3/4) = 11/64 > 0 » et « donc 1/2 < α < 3/4 » retirées ; « 5) continue et strictement croissante » → « 4) … » | C'était une étape de dichotomie (milieu de [1/2 ; 1]) restée à l'écran. Le problème a 4 questions, comme la voix. |
| `limites-continuite-tableau/dichotomie.html` | fichier supprimé | Simulation de la dichotomie, plus utilisée par aucune diapositive. |
| lc_e1_probleme (concentration.pointage[1].mot) | « فيها خمسة ديال الأسئلة: » → « فيها ربعة ديال الأسئلة: » | Repère hérité du problème à 5 questions (avec la dichotomie). Il n'existait plus dans la voix, donc le moment « plan » ne se déclenchait pas. |
| lc_l13_devoir (title) | « À toi : quatre limites de devoir » → « À toi : calculer des limites » | Étiquette « devoir » retirée. La notion est dans le cadre. De plus, le titre annonçait « quatre » alors que la diapositive en contient deux, plus une en fin de cours. |
| séance lc_s2_b2 (titre) | « … ; quatre limites de devoir » → « … ; à toi : des limites » | Même raison. |
| lc_l12_sinus_b (title) + `calculs-donnees.js` vue l12_sinus (titre) | « le changement de variable » → « on pose t = 3x » | Le terme figure dans la liste des pièges hors cadre. La voix dit déjà « on pose t ». |
| lc_lr4_infini (réaction q.2.juste, ecrit) | « ∛(x²−x) ~ x^(2/3) » → « se comporte comme x^(2/3) » | La notation ~ (équivalents) est hors programme. |
| lc_lr4_infini (réaction q.0.1, ecrit) | vide → indice écrit d'après la parole | L'écrit manquait. |
| lc_lr3_zero_sur_zero (réponse fin de cours e0.2.2, ecrit) | vide → correction (1/3) d'après la parole | L'écrit manquait. |
| lc_l6_conjugue (réponse fin de cours e0.2.1, ecrit) | vide → indice sur le signe du conjugué | L'écrit manquait. |
| lc_l7_plus_lourd (réaction q.0.1, ecrit) | « Tu as raison : … donc la limite vaut 3 » → indice « +∞ est un piège fréquent… compare les termes de plus haut degré » | Pour une réponse fausse (+∞), l'écrit disait « Tu as raison » et donnait la réponse dès le premier essai. Il est maintenant aligné sur la parole. |
| lc_e1_probleme (réponse fin de cours e1.2.1, ecrit) | parlait de « [0 ; +∞[ » pour l'option « ]0 ; 1[ » → explique que α est dans ]0 ; 1[ mais que la réciproque est définie sur J = f(ℝ) | Réaction qui ne correspondait pas à l'option choisie. |
| lc_t4_au_moins_une (e0s2.0.2, ecrit) | « revient à la même signe » → « revient au même signe » | Coquille. |
| K9_r4 (réaction 0.1, ecrit) | « ᵠ√(xᵖ) » → « ᑫ√(xᵖ) » | Mauvais caractère : un phi au lieu de q. |
| note (métadonnée du cours) | phrase « Dichotomie en bloc court « pour les devoirs » » et mot « dichotomie » dans la liste des diapos découpées retirés | Affirmation périmée. La phrase « Dichotomie retirée le 15 novembre 2026 » est gardée comme historique. |

**Voix à refaire :** aucune pour ce cours (seuls l'écrit, les titres, un repère de pointage et les simulations ont changé).

**Points douteux non corrigés (à décider) :**
1. lc_l13_devoir, speech_text fr « À toi, comme en devoir » et mixed « بحال فالفرض ». lc_r9_valeur_absolue, speech_text fr « Un exemple complet de devoir » et mixed « مثال كامل ديال الفرض ». Le mot « devoir » est lu, mais il ne présente pas le contenu comme hors national (la notion est dans le cadre). À refaire si l'utilisateur veut zéro « devoir », par exemple « À toi, comme au national ». Les ids internes `lc_l13_devoir` et `?vue=l13_devoir` restent : ils ne s'affichent pas, et les renommer casserait les chemins audio.
2. lc_l11_interpreter, voix fr et mixed : « l'écart … se rapproche de zéro, sans jamais l'atteindre » (mixed : « la courbe عمرها ما كتوصل لـ la droite »). C'est vrai pour la courbe de l'exemple, (2x + 1)/(x + 1), mais c'est faux en général : une courbe peut couper son asymptote. Si l'on veut éviter cette idée fausse, il faut retirer « sans jamais l'atteindre » (voix à refaire).
3. lc_t7_valeur_k, voix : « Si k est en dehors, la droite ne coupe pas la courbe ». C'est vrai ici (x³ + x − 1 est strictement croissante) ; l'écran dit correctement « peut ne pas couper ».
4. lc_e1_probleme, parole de la réponse e1.2.1 : elle parle de [0 ; +∞[ alors que l'option choisie est ]0 ; 1[. Ce n'est pas faux scientifiquement, mais c'est hors sujet. L'écrit est corrigé ; la parole est à refaire si l'on veut qu'elle colle à l'option.
5. Hors de mon périmètre, signalé seulement :
   - 53 fichiers audio de la dichotomie (`lc_d1…lc_d4*.mp3`) restent suivis dans `frontend/public/media/audio/courses/math_ch1_limites_continuite/`, sans aucune référence dans le cours.
   - Dans `cadre_reference_2bac_pc.json` (fiche limites_continuite), il reste des traces de la dichotomie : « dichotomie » et « amplitude » dans `mots_cles`, deux formules LC7 (f((a + b)/2) et m = (a + b)/2), et une ligne de `decisions` qui dit que la dichotomie est « gardée ».
   - L'en-tête de `calculs-donnees.js` dit « écrit par le build maths_build/limites_continuite/build.py, ne pas éditer à la main ». Ce script n'est pas dans le dépôt. S'il existe ailleurs, il faut y reporter les deux corrections, sinon une reconstruction remettrait l'étape de dichotomie.

### math_ch1_limits_course_v1 (ancien cours, fixture de tests)

| diapositive (id) | avant → après | raison |
|---|---|---|
| limits_a01_s02 (question.prompt) | « … pour rendre le prolongement continu ? » → « … pour que f soit continue en 1 ? » | « Prolongement par continuité » est hors cadre. |
| limits_a01_s02 (question.options[2]) | « La fonction ne peut jamais être prolongée » → « Aucune valeur ne convient » | Même raison. |
| limits_a01_s02 (question.feedback_incorrect) | « Le prolongement continu prend au point la valeur de la limite. » → « Pour que f soit continue en 1, f(1) doit être égale à la limite en 1. » | Même raison. |
| limits_a01_s02 (speech_text et speech_base, fr et mixed) | « On peut ensuite prolonger la fonction par continuité… » / « نديرو prolongement par continuité » → « Et si l'on veut une fonction continue en un, quelle valeur donner à f de un ? La valeur de la limite, deux. » (et l'équivalent en mixed) | Terme hors programme dans la voix. |

Pas d'autre erreur scientifique. Les 8 `answer_key` sont justes. Pas de L'Hôpital (le test `test_limit_course_does_not_teach_lhopital…` reste valable). `test_schema_catalog.py` passe (16 tests). `test_course_player.py` n'a pas pu tourner ici : le module `supabase` est absent.

**Voix à refaire (v1) :** limits_a01_s02, speech_text fr et mixed, et speech_base fr et mixed. Ce fichier n'a aucun champ audio, donc rien n'est à régénérer en pratique.

### math_ch2_derivation_etude_fonctions

**Conformité** : les 13 parties sont dans le cadre officiel. I nombre dérivé et II tangente → 1.2.5 ; III demi-tangentes et point anguleux → 1.2.5 ; IV calcul des dérivées → 1.2.6 ; V signe de f′, variations, extremum, inégalité, fonction auxiliaire → 1.2.7, 1.2.8, 1.2.12, 1.2.13 ; VI concavité et point d'inflexion → 1.2.13, 1.2.22 ; VII branches infinies, VIII position relative, IX symétrie → 1.2.22 ; X tracé et lecture graphique → 1.2.9, 1.2.10, 1.2.22 ; XI réciproque → 1.2.11 ; XII étude complète → 1.2.22, avec le rappel du TVI (1.2.3, 1.2.4, vu au ch1) ; XIII bilan et carte. Les rappels de 1re bac (pente, droite, polynôme, signe, 1/x) servent de prérequis. Compétences K1 à K10 : leurs cadre_ids DEF1 à DEF10 renvoient aux objectifs 1.2.5 à 1.2.13 et 1.2.22. Toutes les diapositives sont dans des séances et aucun id ne manque.

Rien trouvé hors programme (écran, voix fr et mixed, questions, réactions, cahier, figures, séances, simulations) : pas de bijection, L'Hôpital, Rolle, accroissements finis, développement limité, approximation affine chiffrée, convexité au sens de l'inégalité, arctan, dichotomie, ln ou exp. « Convexe/concave » vient toujours du signe de f″ ou de la position par rapport aux tangentes. Les conditions sont toutes justes : point d'inflexion (f″ s'annule en changeant de signe, contre-exemple x⁴), extremum (f′ s'annule en changeant de signe), réciproque (f′(x₀) ≠ 0), branches paraboliques (lim f(x)/x puis lim [f(x) − ax]), symétrie ((2a − x) ∈ Df en première ligne), sens des demi-tangentes verticales. Tous les calculs ont été refaits et sont justes, ainsi que l'option désignée par `correct` dans chaque QCM.

| diapositive (id) | avant → après | raison |
|---|---|---|
| df_tr6_lire (réaction e0, option 0, 2e essai) | écrit « Ici, la courbe reste entre −2 et 2 » → « la courbe ne prend aucune valeur strictement comprise entre −2 et 2 : en dessous de −2 (x < 0) ou au-dessus de 2 (x > 0) » ; même correction dans la parole | erreur scientifique : c'est l'inverse pour x + 1/x |
| df_tr6_lire (e0, option 1, 1er essai) | écrit et parole laissaient croire que, pour m > 2, la droite ne coupe pas la courbe → « pour m > 2, la droite passe au-dessus du minimum 2 et coupe la branche de droite en deux points » | erreur scientifique |
| df_tr6_lire (e0, option 1, 2e essai) | « m > 2 : la droite reste au-dessus de la courbe… la courbe reste entre −2 et 2 » ; « intervalle des valeurs prises par f » → « m > 2 : deux solutions ; f ne prend que des valeurs ≤ −2 ou ≥ 2 » (écrit et parole) | erreur scientifique |
| df_dv6_montrer (e0, option 0, 2e essai) | « 0 vient d'un oubli du second terme x/(2√(x + 1)) » → « oubli du premier terme u′v = √(x + 1), qui vaut 1 en 0 » (écrit et parole) | c'est le terme u′v qui manque pour trouver 0 |
| df_dt6_morceaux (q, option 1, 2e essai) | « x√x − 2x correspond à x ≥ 0 » → « x > 0 » | l'accolade donne x > 0 |
| df_dv2_produit_quotient_b (exercice e0, option 1, 1er essai) | « Le numérateur vaut trois, c'est bien… u prime v moins u v prime » → « Le nombre 3 est bon, mais pas son signe… u′v − uv′ » | le numérateur vaut −3 ; à l'écran la formule s'écrit en symboles |
| df_nd4_calcul_b (e0, option 0, 2e essai) | « (x²−3x+4−2)/(x−1) = (x−2) » → « … = (x − 1)(x − 2)/(x − 1) = x − 2 → −1 » | une étape manquait |
| df_pr2_signe et séance df_s5_b1 (cahier_figures, légende) | « f(x) − x = 1/x… » → « Ici f(x) = x + 1/x et (Δ) : y = x (même écart 1/x que dans l'exemple) : f(x) − x = 1/x… » | la figure ne trace pas la fonction de la diapositive (2x + 1 + 1/x) ; la légende le dit maintenant |
| séance df_s2_b1 (retrouver.prompt) | « f prime à droite et f prime à gauche » → « f_d′(x₀) et f_g′(x₀) » | à l'écran, en notation |
| df_nd4_calcul_b (q option 2 ; e0 options 0 et 1), df_dt3_anguleux (q option 2), df_dt5_sens et df_dt5_sens_b (exercice, options 1 et 2), df_dt6_morceaux (e0, options 0 et 1), df_sy4_rediger (e0, option 2), rappel K7_r2 (option 0) : 12 réactions à une mauvaise réponse | « Bonne réponse : X. » / « Réponse correcte : X. » en tête → « La bonne réponse est X. » | la réaction à une réponse fausse commençait comme un « bravo » |

Total : 22 corrections (12 débuts de réaction + 10 autres). `verifier_figures_cahier.py` : 0 erreur. Le JSON se recharge. Les simulations n'ont pas été modifiées : elles sont justes, et trace.html donne bien « m > 2 ou m < −2 : 2 solutions ».

**Voix à refaire**
- df_tr6_lire : `concentration.reponses.e0["0"]["2"].parole`
- df_tr6_lire : `concentration.reponses.e0["1"]["1"].parole`
- df_tr6_lire : `concentration.reponses.e0["1"]["2"].parole`
- df_dv6_montrer : `concentration.reponses.e0["0"]["2"].parole`

(Aucun speech_text, enonce_dit ni dit n'a été modifié.)

**Points douteux non corrigés**
- Objectif 1.2.22 : la périodicité n'est jamais traitée. Objectif 1.2.12 (problèmes de valeur minimale ou maximale) : seulement l'inégalité x + 1/x ≥ 2, pas de vrai problème d'optimisation. Objectif 1.2.10 : l'inéquation f(x) ≤ g(x) n'est qu'effleurée. Je n'ai rien ajouté (consigne : pas de nouveau contenu). À décider.
- Des statistiques dites dans la voix ne sont pas vérifiables : « neuf sujets sur vingt » (df_va7_auxiliaire), « sept sujets sur vingt » (df_ec4_unique), « 8 à 11 points sur 20 » (carte), « type national 2021 » (calculs-vues.js).
- df_va1_monte, student_trace et cahier : « f′ > 0 sur I (sauf peut-être en des points isolés) ». La formule habituelle est « f′ ≥ 0, ne s'annulant qu'en des points isolés ». Ce n'est pas faux, mais c'est maladroit.
- Rappel K8_r2 : il utilise x = −b/(2a), où a désigne le coefficient du trinôme, alors que la même lettre a désigne aussi l'axe x = a. Cela peut prêter à confusion.
- Les cadre_ids des compétences renvoient aux fiches de travail (DEF1 à DEF10), pas directement aux numéros officiels 1.2.x. La correspondance est juste.
- Les fichiers audio des 4 paroles modifiées sont maintenant périmés : leur champ `audio` est resté en place.

### math_ch3_suites_numeriques

**Conformité.** I (termes, arithmétique, géométrique, sommes : rappels utilisés par 1.1.1) · II (récurrence : l'outil de 1.1.1 et 1.1.4) · III (majorée, minorée, bornée, sens de variation : 1.1.2 et 1.1.4) · IV (suite auxiliaire pour uₙ₊₁ = auₙ + b et pour la suite homographique (auₙ + b)/(cuₙ + d), x3 et e1 : 1.1.1) · V (suites de référence nᵅ, qⁿ selon q, f(uₙ) : 1.1.2 et 1.1.3) · VI (croissante et majorée ⇒ convergente, critère de comparaison, kⁿ : 1.1.2) · VII (uₙ₊₁ = f(uₙ), f continue sur I, f(I) ⊂ I, ℓ = f(ℓ) dans I : 1.1.4) · VIII (rang, somme et sa limite : 1.1.5) · IX bilan et carte (les mêmes huit compétences). Les compétences K1 à K8 (cadre_ids SU1 à SU11) correspondent toutes à 1.1.1–1.1.5. Aucune partie ni diapositive hors programme.

Absents (contrôlé partout : écran, voix fr et mixed, questions, réactions, cahier, compétences, séances, simulations du dossier suites-tableau) : suites adjacentes, le mot « arithmético-géométrique », récurrence forte ou double, ordre 2, Fibonacci, série ou somme infinie, epsilon, dichotomie, ln et exp, L'Hôpital, bijection, « devoir », « contrôle », « manuel ». La seule trace des suites adjacentes était dans la `note` interne (« pas de suites adjacentes ») : je l'ai retirée.

Points vérifiés et justes : la limite de qⁿ (4 cas, q ≤ −1 : pas de limite), nᵅ, « croissante et majorée ⇒ convergente » (sans « vers le majorant », c3 et K6_r3), les conditions avant ℓ = f(ℓ) (f continue sur I, f(I) ⊂ I, u₀ ∈ I, suite convergente, puis la solution qui est dans I), les formules de somme (nombre de termes n − p + 1, la puissance est le nombre de termes). Tous les exemples et exercices ont été refaits en python : a1, a9b (2047), s2 (93), K1_r2/r4, r4, r6, r8 (2023 R), m2, m3, x3 (2016, facteur 1/2), x4b, c5/c6 (2020 N, uₙ ≤ (3/2)(2/5)ⁿ), f1 à f7 (g(x) − x = (3 − x)(x + 1)/(x + 2), u₁ = 7/3…), p1 (197), s7 (99), p3 (3/2), K8_r2 (4/3), e1 (2024 : uₙ = 1 + 1/(1 − (2/3)ⁿ⁺¹), limite 2), valeurs des cahier_figures. Tout est juste, sauf ce qui suit.

| diapositive (id) | avant → après | raison |
|---|---|---|
| su_r3_heredite_affine (lead) | « passer de uₙ > 16 à uₙ₊₁ > 16 » → « de uₙ > 1 à uₙ₊₁ > 1 » | l'exemple de la diapositive (uₙ₊₁ = (1/16)uₙ + 15/16, écran, voix, craie) est uₙ > 1 |
| su_m1_pour_tout_n (réaction q, option C, 2e essai, `ecrit`) | vide → texte (deux ou trois termes ne suffisent pas, il faut uₙ₊₁ ≥ uₙ pour tout n) | réaction écrite vide |
| su_l4c_quatre_cas (réaction q option B, `ecrit`) | « si \|q\| > 1, pas de limite » → « si q ≤ −1, pas de limite » | faux : pour q > 1, qⁿ → +∞ (la voix disait déjà q < −1) |
| su_l4c_quatre_cas (réaction juste, `ecrit`) | « termes alternés de module croissant » → « de signes alternés, de valeur absolue croissante » | « module » est un mot des complexes |
| su_c3_plafond_limite (bullet 2) | « Une suite majorée par M a une limite ℓ ≤ M » → « Si elle converge, une suite majorée… » | être majorée ne donne pas une limite (exemple : (−1)ⁿ) |
| su_c2_couple (réaction fin de cours, `ecrit`) | « au-dessus de sa borne inférieure » → « au-dessus de son plancher 1 » | « borne inférieure » est hors cadre (au sens de l'infimum) |
| su_c8_ecart (réaction option C, `ecrit`) | « 2/7 est la raison de la suite » → « la raison de la suite géométrique (2/7)ⁿ, pas la limite de uₙ » | (uₙ) n'est pas géométrique |
| su_f2_place_u0 (bullet 2, student_trace, cahier) | « u₀ < 1 : monte vers 1 » → « 0 < u₀ < 1 » | faux pour u₀ ≤ 0 avec f(x) = 2x/(x + 1) (0 est l'autre point fixe ; −1 est une valeur interdite). Le curseur de la simulation va de 0,2 à 4, donc la voix reste juste |
| su_f3_encadrement_f (réaction option C, `ecrit`) | « la vraie borne supérieure » → « le bon majorant 4/3 de uₙ₊₁ » | même mot hors cadre |
| su_e1_complet (réaction option A, 2e essai, `ecrit`) | « en calculant la limite dans la relation de récurrence » → limite par uₙ = 1 + 1/(1 − (2/3)ⁿ⁺¹) | passer à la limite dans la relation demande les conditions de 1.1.4, qui ne sont pas posées ici |
| su_e1_complet (réaction option B, 2e essai, `ecrit` et `parole`) | « décroissante et minorée par 2, donc sa limite est 2 / la limite est le minorant » → « elle converge, mais le théorème ne dit pas vers quoi ; vₙ → 0 donc uₙ → 2 » | erreur scientifique (la limite n'est pas forcément le minorant) |
| su_e1_complet (réaction juste, `ecrit` et `parole`) | « décroissante et minorée par 2, donc elle converge vers 2 » → « elle converge ; sa limite vient de la suite auxiliaire » | même erreur |
| compétence K3, rappel K3_r2 (`enonce_dit`) | « arithmétique, géométrique, ou ni l'une ni l'autre ? » → « croissante, constante, ou décroissante ? » | la voix ne lisait pas la même question que l'écran |
| compétence K8, rappel K8_r2 (réaction B, 2e essai, `ecrit`) | « +∞ n'arrive que si \|q\| ≥ 1 » → « avec w₀ = 1, Sₙ tend vers +∞ seulement si q ≥ 1 » | faux : pour q ≤ −1, Sₙ n'a pas de limite |
| séance su_s6, bloc su_s5_b2 (exercice, réaction C, `ecrit`) | « borne inférieure… borne supérieure » → « membre de gauche… membre de droite » | même mot hors cadre |
| séance su_s7, bloc su_s6_b1 (cahier[2]) | « lim Sₙ = w₀/(1 − q) » (Sₙ et w₀ pas définis) → « lim (w₀ + … + wₙ) = w₀/(1 − q) » | notation sans définition |
| note (métadonnée) | « Décisions : pas de suites adjacentes ; » → retiré | aucune trace des suites adjacentes |

En tout : 17 corrections, toutes dans le JSON. Les simulations n'ont pas été modifiées (relues : qn, plafond, gendarmes, somme, escalier, nuage, axe, calculs-vues.js, bilan, carte, arbres, sauts : justes). Aucune cahier_figures touchée. Le JSON se recharge et le diff ne contient que ces lignes.

**Voix à refaire**
- su_e1_complet : `parole` de la réaction q, option B (index 1), 2e essai (`reponses.q.1.2`).
- su_e1_complet : `parole` de la réaction q juste (`reponses.q.2.juste`).
- Rappel K3_r2 (compétence K3) : `enonce_dit`.

**Points douteux non corrigés (à décider)**
- su_m4_quotient : la démonstration dit « uₙ > 0 pour tout n (question 2) », à l'écran et dans la `parole` (« d'après la question deux »). Or la question donne uₙ > 0 directement et il n'y a pas de question 2. Ce n'est pas faux, mais c'est incohérent. Pour corriger, il faut changer l'écrit et la voix.
- su_e1_complet, réaction A au 2e essai : la `parole` dit « يلا حسبنا la limite من la relation ». Elle est ambiguë (la relation de récurrence, ou uₙ en fonction de vₙ ?), mais pas fausse. Laissée telle quelle.
- su_b2_bornee : la voix lit u₁ = 5/3 « un virgule six » (1,666…, arrondi à 1,67, ou 1,7 au dixième). C'est une troncature, laissée telle quelle.
- su_a3_termes (formule explicite uₙ = 3n + 2) utilise la vue « machine » de la récurrence. La légende parle de « × ¼ puis + 12 », ce qui est en décalage avec la diapositive. La vue montre bien aussi uₙ = 3n + 2 en haut.
- su_c8_ecart, réaction C au 2e essai : la `parole` dit « la raison ديال la suite » pour 2/7 (l'écrit est corrigé en « suite géométrique (2/7)ⁿ »). C'est une imprécision mineure dans la voix.
- K5_r4 (écrit) : « elle oscille entre +∞ et −∞ ». La formulation est approximative mais la conclusion (pas de limite) est juste.
- Les identifiants SU1 à SU11 sont provisoires (la fiche le dit elle-même). Ils ne sont pas les numéros officiels 1.1.x ; la correspondance est donnée plus haut.

### math_ch4_primitives

Conformité : toutes les parties correspondent au cadre officiel. Ouverture et rappels : prérequis de dérivation (1.2.x) au service de 1.2.14/1.2.15. Parties I, II et VII : 1.2.15 (primitive sur un intervalle, F′ = f, existence pour f continue, famille F + k, condition F(x₀) = y₀, lien entre signe de f et variations de F). Parties III et IV : 1.2.14 (primitives usuelles, linéarité, transformer l'écriture). Parties V et VI : 1.2.15 (u′uⁿ, u′uʳ avec u > 0, u′/u², u′/√u avec u > 0, u′cos u, u′sin u, u′v + uv′, (u′v − uv′)/v²). Partie VIII : 1.2.14/1.2.15 en exercices type national. Partie IX : bilan. ln, exp et l'intégrale ∫ₐᵇ (1.3.1) sont seulement annoncés « plus tard ». 1 + tan²x est donné « pour mémoire ».

Rien de hors cadre : pas de fonction par morceaux, pas de linéarisation de cos² ou sin², pas d'intégrale indéfinie, pas de changement de variable, pas d'éléments simples, pas d'arctan ni de 1/(1 + x²), pas de dichotomie. Vérifié dans l'écran, les voix fr et mixed, les questions, les réactions préparées, le cahier, les séances, les compétences et les 15 simulations.

Toutes les primitives du cours ont été vérifiées en les dérivant avec sympy (environ 50 cas : diapositives, exercices de fin de cours, rappels, séances), ainsi que les constantes k (11/6, −3, 2/3, −1/4, 1/2). Aucune erreur trouvée. Pour chaque QCM, l'index `correct` désigne bien l'option juste, et la réaction « juste » est placée sur cette option.

| diapositive (id) | avant → après | raison |
|---|---|---|
| pr_partie8 (titre de la partie) | « VIII. Types national et devoir » → « VIII. Exercices type national » | retrait de l'étiquette « devoir » (règle utilisateur) |
| pr_x2 (title) | « Type devoir : forme u′uⁿ et condition » → « Type national : forme u′uⁿ et condition » | la notion (forme u′uⁿ, puis condition F(x₀) = y₀) appartient à 1.2.15 ; on retire seulement l'étiquette « devoir » |
| pr_x2 (speech_text fr) | « Un exercice de devoir qui enchaîne… » → « Un exercice qui enchaîne… » | même raison |
| pr_x2 (speech_text mixed) | « تمرين ديال الفرض فيه… » → « تمرين فيه… » | même raison (« الفرض » veut dire « le devoir ») |
| séance pr_s4, bloc pr_s3_b2b (exercice) | QCM `reprend: pr_l3/e0`, copie exacte de l'exercice du bloc précédent pr_s3_b2 (développer (x + 1)²) → vrai/faux `reprend: pr_c1/e0` (« une primitive de u′uⁿ est uⁿ⁺¹/(n + 1) » ; « … même sans u′ » : faux) | le bloc « D'où vient u′uⁿ ; la bulle » n'évaluait pas sa propre notion (doublon) ; l'exercice repris existe déjà dans le cours |

Voix à refaire :
- pr_x2 : speech_text.fr
- pr_x2 : speech_text.mixed
- séance pr_s4, bloc pr_s3_b2b : exercice.enonce_dit. Le texte est repris mot pour mot de l'enonce_dit de pr_c1, exercices_fin_de_cours[0]. Il faut donc peut-être seulement réutiliser cet audio, s'il existe.

Points douteux non corrigés :
- pr_d4, question.enonce_dit : la voix dit « est-ce que h de x égale x sinus de x, est une primitive de petit h de x » ; il faudrait « grand H de x ». C'est compréhensible grâce au contraste avec « petit h » ; je n'ai pas modifié la voix. À refaire si on veut la notation exacte.
- pr_x4, speech_text : « la primitive de un sur x sera ln… » ; il faudrait plutôt « une primitive ». C'est mineur et seulement annoncé « plus tard ».
- Les exercices de fin de cours des diapositives qui ont déjà une question (pr_d4, pr_e3, pr_e7, pr_l1, pr_c1, pr_c7, pr_g2, pr_x3) n'ont pas de réactions préparées dans `reponses_fin_de_cours`. C'est peut-être voulu ; ce n'est pas une erreur scientifique.
- pr_e1 et rappel K2_r1 : la bonne réponse « admet des primitives sur [0 ; +∞[ » (√x + …) est juste (fonction continue sur un intervalle fermé à gauche). On pourrait préférer ]0 ; +∞[ par cohérence avec le reste du cours ; je n'ai pas modifié.
- Titre de la séance pr_s6 : « Types national, bilan et carte ». L'accord est maladroit, mais il n'y a pas d'étiquette « devoir » ; je n'ai pas modifié.
- Ce que j'ai observé dans `git diff --stat` : plusieurs fichiers de `backend/data/curriculum/` sont modifiés dans l'arbre de travail. Ce n'est pas moi qui les ai modifiés ; je ne les ai pas touchés.

### math_ch5_fonctions_ln

Conformité : Ouverture et rappels (prérequis : 1.2.14 primitives usuelles, signe, inégalités, second degré pour 1.2.17) ; I naissance de ln (1.2.14–1.2.15, définition OP) ; II courbe, e, tangente (1.2.22) ; III domaine (1.2.22 / 1.2.17) ; IV règles (1.2.16) ; V équations, inéquations, systèmes, plus petit n (1.2.17) ; VI limites (1.2.19, 1.2.5 pour la demi-tangente) ; VII (ln u)' (1.2.6, 1.2.22) ; VIII primitives u'/u (1.2.14–1.2.15) ; IX étude et inégalités (1.2.13, 1.2.22) ; X log décimal, 10ˣ = a (1.2.18) ; XI bilan et carte. Toutes les parties et les compétences K1–K9 correspondent à une notion officielle. Il n'y a ni dichotomie, ni log de base a (sauf une mention « changement de base », corrigée), ni exponentielle comme fonction (eʳ reste un nombre, annoncé « plus tard »). competence_ids, competences et seances sont cohérents : les 65 diapositives sont toutes couvertes.

| diapositive (id) | avant → après | raison |
|---|---|---|
| ln_o1 (réaction fin de cours e0s0, choix 1, niveau 2 : ecrit + parole) | « ln(1) = 0, car e^0 = 1 » → « car ln est la primitive de 1/x qui s'annule en 1 (sa définition) » | l'exponentielle n'est pas encore vue |
| ln_c2 (réaction e1s2, choix 1, niveau 2 : ecrit + parole) | « car e⁰ = 1 » / « exponentielle de zéro égale un » → « ln s'annule en 1 par définition » | même raison |
| ln_c3 (réaction e0, choix 0, niveau 2 : parole) | « حيت e puissance zéro كتساوي un » → « ln كتنعدم فـ un بالتعريف » | même raison |
| ln_a1 (réaction q, choix 1, niveau 1 : ecrit + parole ; niveau 2 : ecrit) | « tu as calculé 1,61 − 0,69 ≈ 0,92 » / « 1,11 viendrait d'une soustraction » → « tu as multiplié 0,69 × 1,61 ≈ 1,11 ; ln(ab) ≠ ln a × ln b » | calcul faux : 1,61 − 0,69 = 0,92 (c'est l'option C) ; 1,11 = 0,69 × 1,61 |
| ln_q6 (réaction e0, choix 1, niv. 1 : ecrit + parole ; niv. 2 : parole ; choix 2, niv. 2 : ecrit + parole) | X = 2, Y = 1, x = e², y = e (copiés de l'exemple) → X = 1, Y = 0, x = e, y = 1 | ces réactions expliquent l'exercice ln x + ln y = 1, ln x − ln y = 1 avec les valeurs de l'exemple de la diapositive ; elles se contredisaient avec la bonne réponse A (e ; 1) |
| ln_e3 (réaction e0, choix 1, niveau 1 : ecrit + parole) | f(x) = x − ln x + ½(ln x)² (trois termes) → f(x) = x + ½ − ln x + ½(ln x)² (quatre termes) | la fonction était recopiée sans le terme ½, alors que f(1) = 3/2 en dépend |
| ln_l5 (écran bullets[3]) | « En posant x = 1 + h : lim_{x→0} ln(1 + x)/x = 1 » → « … lim_{h→0} ln(1 + h)/h = 1, soit lim_{x→0} ln(1 + x)/x = 1 » | mauvaise variable après le changement x = 1 + h |
| ln_l7 (réaction e1s0, choix 1, niveau 1 : ecrit) | « Revois le changement de variable » → « Reprends t = √x » | le cadre dit « poser t = √x » ; « changement de variable » est dans la liste des pièges |
| ln_z1_primitive (réactions e0, choix 0 et 2, niveau 1 : ecrit) | « Regarde le premier geste : x³ donne x⁴ sur 4 » → « Rappelle la règle : xⁿ a pour primitive xⁿ⁺¹/(n + 1) (x³ donne x⁴/4) » | ces réactions renvoyaient aux « trois gestes », qui ne sont plus à l'écran |
| competences K5, rappel K5_r4 (réaction 0 juste : parole ; réaction 1, niveau 2 : parole) | « ln x qui tend vers plus l'infini » (en 0⁺) → « vers moins l'infini » ; « لموinus » → « لـ moins » | erreur scientifique ; mot abîmé dans le texte lu |
| competences K9, rappel K9_r3 (réaction 0 juste : ecrit + parole ; réaction 1, niveau 2 : ecrit + parole) | « formule de changement de base » ; « par définition 10^(log x) = x, en prenant ln… » → « c'est la définition du logarithme décimal ; vérification log 10 = 1 » | log de base a est hors programme (seul le log décimal, 1.2.18) ; la diapositive ln_g1 définit log x = ln x / ln 10 |
| ln_b1 (écran bullets[6]) | « u'/u → ln|u| » → « u'/u → ln|u| (u ne s'annule pas sur I) » | condition de validité manquante |
| ln_b2 (écran bullets[3]) | « u'/u → ln|u| » → « … (u ≠ 0 sur I) » | même raison |
| seance ln_s5, bloc ln_s4_b2 (retrouver.attendu) | « u'/u → ln|u| » → « … (sur un intervalle où u ne s'annule pas) » | même raison |
| simulation bilan.html (bloc 7 · Primitives) | 'u’/u → ln|u|' → 'u’/u → ln|u| (u ≠ 0 sur I)' | même raison |

Total : 28 modifications dans le JSON et 1 dans la simulation, soit 15 lignes du tableau. Le JSON se recharge et `git diff` ne touche que les lignes voulues. cahier_figures n'a pas été modifié.

Voix à refaire :
- ln_o1 : reponses_fin_de_cours e0s0 → choix 1 → niveau 2, parole
- ln_c2 : reponses_fin_de_cours e1s2 → choix 1 → niveau 2, parole
- ln_c3 : reponses_fin_de_cours e0 → choix 0 → niveau 2, parole
- ln_a1 : concentration.reponses q → choix 1 → niveau 1, parole
- ln_q6 : reponses_fin_de_cours e0 → choix 1 → niveau 1, parole
- ln_q6 : reponses_fin_de_cours e0 → choix 1 → niveau 2, parole
- ln_q6 : reponses_fin_de_cours e0 → choix 2 → niveau 2, parole
- ln_e3 : reponses_fin_de_cours e0 → choix 1 → niveau 1, parole
- rappel K5_r4 : réaction 0 juste, parole ; réaction 1 niveau 2, parole
- rappel K9_r3 : réaction 0 juste, parole ; réaction 1 niveau 2, parole

Points douteux NON corrigés (à décider) :
- ln_l5 : speech_text fr et mixed disent « on pose x égale un plus h, et on obtient … ln de un plus x sur x quand x tend vers zéro ». C'est le même glissement de variable que l'écran, mais à l'oral. Ce n'est pas faux sur le fond ; je ne l'ai pas changé, pour garder la voix.
- ln_l5 : deux paroles de réaction (e1, choix 1 et 2, niveau 1) disent « le changement de variable, u = 3x ». Dans une limite, c'est la méthode « poser X = … » du cadre (LN5), pas le changement de variable des intégrales. Je les ai laissées.
- ln_z1_primitive : les paroles des réactions e0 choix 0 et 2 (niveau 1) renvoient encore au « premier geste, x³ → x⁴/4 », qui n'est plus montré. C'est juste en maths, mais la référence ne correspond plus à ce qui est à l'écran ; il faudrait les refaire.
- ln_a3 : la légende et l'alt de la simulation (calculs.html?vue=a3) montrent ln(1/8) = −3 ln 2 avant que la règle de la puissance soit vue (ln_a4). La vue écrit −ln(2 × 2 × 2), donc le calcul passe par le produit : acceptable.
- ln_o1 : « ln est dans 18 sujets nationaux sur 20 ; un problème avec ln dans 12 ». Ces chiffres ne sont pas vérifiables ici.
- simulation calculs-vues.js : une vue ancienne « Trois gestes à avoir en main » existe encore, mais aucune diapositive ne l'appelle. Elle est sans erreur ; on peut la supprimer plus tard.

### math_ch6_nombres_complexes

**Conformité** : toutes les parties correspondent au cadre officiel. Ouverture (rappels de repère, vecteur, Pythagore, cercle trigonométrique et identités, prérequis de 2.4.1 et 2.4.4) ; I le nombre i et la forme algébrique → 2.4.1 ; II le calcul algébrique → 2.4.1 ; III les affixes → 2.4.4 ; IV le conjugué → 2.4.1 ; V le module et la distance → 2.4.1 et 2.4.4 ; VI l'argument → 2.4.2 ; VII la forme trigonométrique → 2.4.2 ; VIII produit, quotient et Moivre → 2.4.1 ; IX l'alignement et l'égalité de distances → 2.4.4 et 2.4.7 ; X les sujets nationaux 2023 N et 2024 N → 2.4.1, 2.4.2 et 2.4.7 ; XI le bilan et la carte. Les compétences K1 à K8 renvoient aux capacités NC1 à NC10 de la fiche, qui dépendent de 2.4.1, 2.4.2, 2.4.4 et 2.4.7. Aucune diapositive n'est hors programme. L'écriture exponentielle, l'équation du second degré et la rotation sont seulement annoncées. On ne trouve pas de similitude, de barycentre, d'arctan, de notation [r ; θ], de racines n-ièmes, de coefficients complexes ni de « corps ».

**Calculs refaits en python (cmath)** : tous les exemples, QCM, rappels et sujets nationaux sont justes. Exemples vérifiés : i²⁰²⁶ = −1 ; (1 + 3i)/(1 − i) = −1 + 2i ; (2 − i)/(2 + 4i) = −i/2 ; AB = 2√10 ; cos 5π/12 = (√6 − √2)/4 ; (√3 + i)⁶ = −64 ; a²⁰²⁰ = −1 ; a²⁰²² = 3¹⁰¹¹ ; (d − a)/(c − a) = 3/2 ; ΩA = ΩB = 5/2. Pour le sujet 2023 N : b − d = c, (b − d)/(b − a) = √2 + 1, ac = 2b et 2 arg b ≡ π/4. Pour le sujet 2024 N : b¹² < 0, b⁶ est imaginaire pur et b²⁴ est réel.

| diapositive (id) | avant → après | raison |
|---|---|---|
| nc_n1 (réactions e0 : juste, 1.2, 2.2 ; écrit et voix) | « B n'est pas le milieu car le quotient n'est pas égal à 1/2 » (ou « à 2 ») → « si B était le milieu de [AD], le quotient (b − d)/(b − a) vaudrait −1 » | Erreur scientifique : B milieu de [AD] ⇔ (b − d)/(b − a) = −1 |
| nc_b1_bilan (5 réactions de la réserve, écrit et voix) | Les réactions parlaient d'un z = 1 + i absent de l'énoncé (« le module de 1 + i est √2, pas 2 »…) → réactions réécrites sur la vraie question (place du signe moins, r > 0) | Les réactions ne correspondaient pas au QCM, et certaines phrases se contredisaient |
| nc_i2 (réserve, affirmation 1) | « OA = OB » (lu : « O A égale O B ») → « ΩA = ΩB », avec l'explication par la symétrie | Les six réactions préparées traitaient toutes de ΩA = ΩB |
| nc_r4 (réaction e0, option 2, écrit et voix) | « celui de 1 + i et celui de a » → « celui de i et celui de a » | Dans ce QCM, b = ia |
| nc_c3 (réaction e1s1 juste) | « −(ib)(−ib) donne −i²b² » → « (ib)(−ib) = −i²b² = +b² » | Erreur de signe |
| nc_g3 (2 réactions) | « −i est sous l'axe imaginaire » ; « 3i : au-dessus ou au-dessous de l'axe imaginaire » → « sur l'axe imaginaire, sous l'axe réel » ; « de l'axe réel » | Le mauvais axe était nommé |
| nc_g4 (puce, trace, cahier, et le cahier du bloc séance 4) | « z = a + ib, r = \|z\| : cos θ = a/r… » → « z = a + ib ≠ 0, r = \|z\|, θ ≡ arg z [2π] : … » | L'argument n'existe que pour z ≠ 0 ; θ n'était pas défini |
| nc_r1 (puce, trace, cahier, et le cahier du bloc séance 5) ; nc_b1_bilan puce 7 | arg(zz′) ≡ arg z + arg z′ [2π] → ajout de « (z, z′ ≠ 0) » | La condition manquait |
| nc_i1 (trace, cahier, centre, cahier du bloc séance 6) ; nc_b1_bilan puce 8 | « A, B, C alignés ⇔ (c − a)/(b − a) ∈ ℝ » → « Pour A ≠ B : … » | La condition b ≠ a manquait |
| nc_r7 (puce 4, alt) et moivre.html (4 textes visibles) | « nθ ≡ π/2 [π] » → « nθ = π/2 + kπ (k entier) » | La notation modulo π est hors programme (perimetre.json : on travaille modulo 2π) |
| Rappel K5_r3 (réactions 0.2 et 1.juste, écrit et voix) | « \|z + z′\| ≤ \|z\| + \|z′\| (inégalité triangulaire) » → seulement le contre-exemple z = 1, z′ = −1 | L'inégalité triangulaire est hors cadre |
| Rappel K8_r3 (enonce_dit) | « valeur absolue de oméga moins a » → « le module de oméga moins a » | Mauvais terme pour un complexe |
| nc_m2 (énoncé lu de l'exercice de réserve) | « le module de un moins i, c'est-à-dire la valeur absolue de un moins i » → « le module de un moins i » | Même faute de terme |
| nc_r3_b (réactions e0s0 juste et e0s1 juste) | « par une rotation d'un demi-tour » → « par un demi-tour autour de O » ; voix : « la valeur absolue de z barre » → « le module de z barre » | La rotation n'est qu'annoncée (partie 2) ; mauvais terme |
| nc_m3 / nc_m3_b, nc_t3 / nc_t3_b, nc_r3 / nc_r3_b (reponses_fin_de_cours) | Les réactions avaient été copiées en double lors de la scission des diapositives (clés e1s* en trop sur la diapositive mère ; e0 sans objet et e1s* mal numérotées sur la diapositive _b) → doublons supprimés, clés e1s* renommées en e0s* | Les clés ne correspondaient plus aux exercices ; la diapositive _b proposait les réactions d'un QCM \|z⁴\| pour un vrai/faux |
| nc_a6 (7 réactions), nc_j2, nc_g1 (3), nc_r1, nc_r2 (3), nc_r6 (2), nc_t4, nc_n2 (2), rappel K1_r2 | « i^2026 », « 1⁲⁵ », « \overline{zⁿ} », « pi/2 », « -2 », « 2^6 », « cos de pi moins teta »… → i²⁰²⁶, 1²⁵, conj(zⁿ), π/2, −2, 2⁶, cos(π − θ) | À l'écran, on écrit les formules en symboles (règle de l'utilisateur) ; « 1⁲⁵ » était une coquille |

En tout : 22 corrections (68 champs du JSON et 4 lignes de moivre.html). `verifier_figures_cahier.py` : 0 erreur (aucune figure modifiée).

**Voix à refaire** (13) :
- nc_n1 : reponses_fin_de_cours.e0 → `0.juste.parole` et `1.2.parole`
- nc_b1_bilan : reponses_fin_de_cours.e0 → `0.1.parole`, `0.2.parole`, `1.juste.parole`, `2.1.parole`, `2.2.parole`
- nc_r4 : reponses_fin_de_cours.e0 → `2.1.parole`
- nc_r3_b : reponses_fin_de_cours.e0s1 (anciennement e1s1) → `1.juste.parole`
- nc_i2 : `exercices_fin_de_cours[0].enonce_dit`
- nc_m2 : `exercices_fin_de_cours[0].enonce_dit`
- rappel K5_r3 : `reponses.0.2.parole` et `reponses.1.juste.parole`
- rappel K8_r3 : `enonce_dit`

Pour ces 13 voix, le champ `audio` pointe encore vers les anciens mp3. Ils diront l'ancienne version (par exemple « un sur deux ») tant qu'ils ne sont pas régénérés.

**Points douteux non corrigés**
1. Dans les séances, un exercice `reprend: "<diapo>/e<i>"` lit seulement `concentration.reponses` (code dans frontend/src/components/course/memoire/api.ts). Or la plupart des exercices repris ici viennent de la réserve (`exercices_fin_de_cours`), et leurs réactions sont rangées dans `reponses_fin_de_cours`. À la fin des blocs, ils n'ont donc pas de réactions préparées. Le problème vient de la plateforme et touche sans doute les autres cours.
2. Rappel K8_r1 (réactions) : « un quotient imaginaire pur donne des droites perpendiculaires ». L'orthogonalité fait partie du cadre (2.4.4), mais ce cours la renvoie à la partie 2. Je l'ai laissée.
3. nc_a6 (voix d'une réaction de la réserve) et nc_r2 (réaction q.0.2) : le mot « rotation » est employé, avant ou au moment de son annonce pour la partie 2. C'est toléré, je n'y ai pas touché.
4. Certaines réactions de la réserve utilisent l'argument d'un produit avant la diapositive nc_r1 : nc_t4 e1s1, nc_t6 e0 (« 2 est réel positif, donc arg b = arg(1 + i) »). De même, le QCM de réserve de nc_r3 porte sur le quotient, qui n'est enseigné qu'en nc_r3_b. Ce sont des exercices de réserve ; je les ai laissés.
5. Les fréquences annoncées au national (20 sujets sur 20, la forme trigonométrique dans 17, le quotient dans 10) n'ont pas pu être vérifiées.
6. calculs-vues.js est généré par `maths_build/operations_formes/build.py` (« ne pas modifier à la main »). Je n'y ai trouvé aucune erreur et je n'y ai pas touché.


## Voix à refaire (toutes les pistes, en local)

- **ch1** `math_ch1_limites_continuite` : `lc_l13_devoir` (speech_text fr, mixed) ; `lc_r9_valeur_absolue` (speech_text fr, mixed) ; `lc_l11_interpreter` (speech_text fr, mixed).
- **ch2** `math_ch2_derivation_etude_fonctions` : `df_tr6_lire` réactions e0 « 0 » niveau 2, « 1 » niveaux 1 et 2 ; `df_dv6_montrer` réaction e0 « 0 » niveau 2.
- **ch3** `math_ch3_suites_numeriques` : `su_e1_complet` réactions q option 1 niveau 2 et q option 2 « juste » ; rappel `K3_r2` (enonce_dit).
- **ch4** `math_ch4_primitives` : `pr_x2` (speech_text fr, mixed) ; exercice du bloc `pr_s3_b2b` (enonce_dit, texte identique à celui de `pr_c1` : son audio peut être réutilisé).
- **ch5** `math_ch5_fonctions_ln` : `ln_o1` (e0s0, choix 1, niveau 2) ; `ln_c2` (e1s2, choix 1, niveau 2) ; `ln_c3` (e0, choix 0, niveau 2) ; `ln_a1` (q, choix 1, niveau 1) ; `ln_q6` (e0, choix 1 niveaux 1 et 2 ; choix 2 niveau 2) ; `ln_e3` (e0, choix 1, niveau 1) ; rappel `K5_r4` (réaction 0 juste, réaction 1 niveau 2) ; rappel `K9_r3` (réaction 0 juste, réaction 1 niveau 2).
- **ch6** `math_ch6_nombres_complexes` : `nc_n1` (reponses_fin_de_cours e0 : 0 juste, 1 niveau 2) ; `nc_b1_bilan` (e0 : 0.1, 0.2, 1 juste, 2.1, 2.2) ; `nc_r4` (e0 : 2.1) ; `nc_r3_b` (e0s1 : 1 juste) ; `nc_i2` et `nc_m2` (exercices_fin_de_cours[0].enonce_dit) ; rappel `K5_r3` (0.2, 1 juste) ; rappel `K8_r3` (enonce_dit).

## Étape 3 — Les skills

Sous le titre commun « Conformité au cadre officiel du ministère (mandatory check) » de `.agents/skills/exploration-de-cours/SKILL.md` et `.agents/skills/cours-concentration/SKILL.md` (créé par la session SVT), sous-partie **« Maths »** : numérotation officielle et poids, cadre de la série sciences expérimentales (jamais un item de la filière SM), liste des pièges hors cadre et des erreurs de réactions trouvés dans cet audit.
