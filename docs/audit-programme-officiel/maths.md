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
