# Audit chimie : notre programme et nos cours face au cadre officiel

Date : 15 novembre 2026.
Référence : cadre de référence officiel de l'examen national, physique-chimie, filière Sciences physiques, options internationales (CNEEO, 2015), transcrit dans `backend/cours 2bac pc/cadres de references 2BAC PC/cadre-de-reference-de-l-examen-national-physique-chimie-spc-2.json`.

Le PDF officiel en ligne n'a pas pu être ouvert depuis la session cloud : les sites du ministère et ses miroirs sont bloqués par le réseau. Les points ambigus ont été tranchés avec le JSON officiel seul, dans le sens le plus strict (si ce n'est pas dans le cadre, on le retire).

## Le cadre officiel, partie chimie (33 % de la note)

| Sous-domaine officiel | Poids | Notions officielles | Notre cours |
|---|---|---|---|
| 1. Transformations rapides et lentes | 6 % | Transformations lentes et rapides (oxydoréduction, facteurs cinétiques) ; suivi temporel, vitesse de réaction (tableau d'avancement, vitesse volumique, temps de demi-réaction) | ch9, ch10 |
| 2. Transformations non totales | 10 % | Transformations dans les deux sens (acide-base de Brønsted, pH, taux d'avancement final, état d'équilibre) ; état d'équilibre (quotient de réaction, constante d'équilibre) ; réactions acido-basiques (produit ionique de l'eau, Ka, pKa, dosage acido-basique) | ch11, ch12, ch13 |
| 3. Sens d'évolution d'un système chimique | 10 % | Évolution spontanée (critère Qr et K) ; piles (constitution, f.é.m., polarité) ; transformations forcées (électrolyse, réactions aux électrodes) | **aucun cours** |
| 4. Contrôle de l'évolution des systèmes chimiques | 7 % | Estérification et hydrolyse (caractéristiques, rendement, catalyseur) ; contrôle par changement de réactif ou catalyse (anhydride d'acide, saponification) | **aucun cours** |

Travaux pratiques officiels de chimie : facteurs cinétiques ; suivi temporel par mesure de conductance ; avancement final d'une réaction acide-base ; constante d'équilibre ; dosage par mesure de pH ; pile ; électrolyse ; estérification et hydrolyse ; savons ; dosage direct de l'aspirine.

## Étape 1 — Notre programme face au cadre officiel

Fichiers comparés : `perimetre.json` (clés `cinetique`, `acides_bases`, `dosage`, `esterification_hydrolyse`, `piles_electrolyse`), `physique.json` (domaine `chimie`), `physique_blueprint.json` (règles `chimie`), `programme_semestre1.json` (ordres 9 à 13), `cadre_reference_2bac_pc.json` (fiches `transformations_lentes_rapides`, `cinetique`, `transformations_deux_sens`, `etat_equilibre`, `acides_bases`).

### (a) Ce que nous avions en trop (hors cadre officiel)

| Fichier | Avant | Après | Raison |
|---|---|---|---|
| `physique.json`, chapitre `acides_bases` | « Solution tampon » | retiré | La solution tampon n'est pas dans le cadre officiel. |
| `perimetre.json`, `acides_bases`, `termes_hors_programme` | « pouvoir tampon quantifié », avec « la solution tampon est décrite qualitativement » | « solution tampon, pouvoir tampon » : le motif attrape aussi « solution tampon » et « effet tampon », et la phrase dit qu'on n'en parle pas | Le texte laissait entendre que la solution tampon était au programme. |
| `physique.json`, chapitre `cinetique` | « Suivi temporel : conductimétrie, spectrophotométrie » | « titrage après trempe, conductimétrie (mesure de conductance), mesure de pression ou de volume de gaz » | La spectrophotométrie n'est pas dans le cadre (TP officiel : mesure de conductance), et la loi de Beer-Lambert était déjà dans nos termes hors programme. |
| `perimetre.json`, `cinetique`, notions | « catalyseur (homogène, hétérogène, enzymatique) » | « catalyseur (sans les types de catalyse, hors cadre) » | Le cadre cite le catalyseur sans classer les types de catalyse. |
| Fiches `transformations_lentes_rapides` et `cinetique`, `hors_cadre.mots` | — | ajout de « catalyse homogène », « catalyse hétérogène », « catalyse enzymatique », « spectrophotométrie », « absorbance » | Mêmes raisons ; ces mots sont maintenant contrôlés dans les cours. |
| Fiches `transformations_deux_sens`, `etat_equilibre`, `acides_bases`, `hors_cadre.mots` | — | ajout de « solution tampon » (et « effet tampon » pour ch13) | Même raison. |

### (b) Ce qui manque

1. **Sous-domaines 3 et 4 sans cours (17 % de la note, et la partie I de chaque exercice de chimie du national porte sur une pile ou une électrolyse)** :
   - « Évolution spontanée d'un système chimique » (critère Qr,i et K) ;
   - « Transformations spontanées dans les piles » (constitution, f.é.m., polarité, quantité d'électricité) ;
   - « Exemples de transformations forcées » (électrolyse) ;
   - « Réactions d'estérification et d'hydrolyse » ;
   - « Contrôle de l'évolution des systèmes chimiques » (anhydride d'acide, saponification, catalyse).
   Ces chapitres ont déjà un périmètre (`perimetre.json` : `piles_electrolyse`, `esterification_hydrolyse`) mais ni fiche dans `cadre_reference_2bac_pc.json`, ni ligne dans `programme_semestre1.json` (ils sont au 2ᵉ semestre), ni cours. **À construire** (exploration-de-cours puis cours-concentration). Aucune fiche n'a été inventée ici : elle doit naître de l'exploration.
2. `physique.json` ne citait pas l'oxydoréduction ni les transformations lentes et rapides (sous-domaine 1), ni Ke, τ, Qr et K (sous-domaine 2), ni le critère d'évolution spontanée, la constitution et la polarité d'une pile (sous-domaine 3), ni l'anhydride d'acide et la saponification (sous-domaine 4) : ajoutés.
3. `physique.json`, estérification : le rôle du catalyseur et de la température (vitesse, pas état final) manquait : ajouté.

### (c) Ce qui était mal formulé ou mal classé

| Fichier | Avant | Après | Raison |
|---|---|---|---|
| `perimetre.json`, `cinetique` (notion et méthode) | t₁/₂ : « date à laquelle x = x_max/2 » | « durée au bout de laquelle x = x_f/2 (x_f = x_max pour une transformation totale) » | Définition du cours et des corrigés : moitié de l'avancement **final**. L'ancienne écriture est fausse pour une transformation limitée. Nos fiches et nos cours disaient déjà x_f/2. |
| `physique.json`, `piles_electrolyse` | « Lois de Faraday : m = (M × I × t)/(n × F) » | « Bilan de matière : Q = I·Δt = n(e⁻)·F, d'où m = M·I·Δt/(n·F) » | Le cadre ne parle pas de « lois de Faraday » (et la « loi de Faraday » est hors programme en induction) ; la relation se démontre à partir de Q = n(e⁻)·F. |
| `physique.json`, `esterification_hydrolyse` | « Déplacement d'équilibre : excès d'un réactif, distillation » | « Contrôle de l'état final : excès d'un réactif, élimination d'un produit (distillation) » | « Déplacement d'équilibre » renvoie au principe de Le Chatelier, hors programme (règle de `perimetre.json`). |
| `programme_semestre1.json` et fiche `acides_bases` | « Transformations liées aux réactions acide-base » | « Transformations associées aux réactions acido-basiques » | Titre officiel du cadre. |
| Les cinq fiches de chimie, `_note` | « capacités provisoires, à collationner avec le texte officiel » | « collationnées le 15 novembre 2026 avec le cadre officiel » | Fait par cet audit. |
| Fiche `transformations_lentes_rapides`, `source` | catalyseur sans source officielle | « CDR-PC-2015 sous-domaine 4 pour le catalyseur » | Le catalyseur est au cadre (sous-domaine 4, et facteur cinétique) : il reste au cours ch9, sans types de catalyse. |

### Points vérifiés et gardés

- Les capacités TLR1-7, CIN1-8, TD1-8, EE1-7, AB1-10 visent toutes une notion officielle (tableau ci-dessus). Les formules des fiches ont été recalculées : demi-équations et équations équilibrées (éléments et charges), x_max des exemples, conductivités (σ₀ = 0,249 S/m, σ_f = 0,091 S/m), pression (2 490 Pa), Qr,éq (1,57·10⁻⁵), K(méthanoïque) (1,8·10⁻⁴), pKa de NH₄⁺/NH₃ par Ke (9,22), K = 10^(pKa₂ − pKa₁), points de la courbe de dosage (pH_E = 8,25 ; 5,75), zones de virage. Aucune erreur trouvée dans les fiches.
- « Chocs efficaces » reste hors cadre (déjà dans nos termes hors programme) : le JSON officiel ne cite pas d'interprétation microscopique en cinétique. Si l'utilisateur dispose du PDF détaillé (annexe 1) et qu'elle y figure, la règle est à revoir.
- Dosage conductimétrique : gardé (le cadre dit « dosage acido-basique » sans limiter la méthode), une diapositive seulement.
- Le critère d'évolution spontanée reste hors des cours ch11-ch13 (il appartient au sous-domaine 3).
- `physique_blueprint.json` : rien hors cadre dans la partie chimie (structure des exercices observée sur 20 nationaux).
- Le découpage de `perimetre.json` (clé `cinetique` pour ch9-ch10, clé `acides_bases` pour ch11-ch13) ne correspond pas aux clés de `programme_semestre1.json`, mais les fiches du cadre font le lien : laissé tel quel.
