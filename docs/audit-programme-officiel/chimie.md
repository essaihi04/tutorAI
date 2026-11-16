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

## Étape 2 — Les cours de chimie (ch9 à ch13)

Chaque cours a été relu en entier : écran, voix (fr et mixed), questions, réactions préparées, cahier, rappels, exercices, et les textes des simulations. Tous les calculs ont été refaits. Une ligne d'un tableau peut regrouper plusieurs champs.

| Cours | Corrections | Commit | Voix à refaire |
|---|---|---|---|
| ch9 Transformations lentes et rapides | 21 lignes (≈ 60 champs) + `equation.html` | `1751b7e8` | 1 diapositive (`tl_f1_facteur`) + 24 réactions + 1 énoncé |
| ch10 Suivi temporel, vitesse de réaction | 27 lignes (92 lignes du JSON) + `figures.html` | `87aa556d` | 31 réactions |
| ch11 Transformations dans les deux sens | 45 corrections (41 champs) | `c8d2dba7` | ≈ 30 réactions + 1 énoncé + 1 `dit` de compétence |
| ch12 État d'équilibre | 49 corrections | `b52ae666` | ≈ 45 réactions + 1 énoncé et 1 démonstration (n5) |
| ch13 Réactions acido-basiques | 19 corrections (34 champs) | `1d497c54` | 21 réactions |

Ce qui revenait le plus souvent :
- les erreurs sont surtout dans les **réactions préparées** (texte `ecrit` et voix `parole`), presque jamais à l'écran : réactions qui disent « faux » quand la bonne réponse est Vrai, valeurs fausses dans la voix, explication du mauvais distracteur ;
- les mots des **chapitres suivants** dans un chapitre (« équilibre », « constante d'équilibre », « rendement », « saponification », « Ka », « critère d'évolution ») ;
- le **vocabulaire hors cadre** : « chocs efficaces », « collisions », « Henderson », « Kb », « pKb », « pOH », « activité », « dissociation », « déplacement d'équilibre », « spectrophotomètre » ;
- la **définition de t₁/₂** donnée par x_max/2 comme règle générale ;
- des **flèches** : → au lieu de ⇌ pour les demi-équations et les réactions limitées ;
- les **charges** des équations mal comptées dans les réactions (S₂O₈²⁻ + 2I⁻ : −4 de chaque côté) ;
- « les unités mol/L se simplifient » dans Qr : faux en général ; on met les concentrations en mol/L et Qr s'écrit sans unité.

Aucun `speech_text` n'a changé sauf celui de `tl_f1_facteur` (ch9). Les mots du pointage sont intacts. Les réactions modifiées gardent leur ancien champ `audio` jusqu'à ce que leur voix soit refaite en local.

### À trancher par l'utilisateur (tous cours)

- ch9 : l'avancement (x, x_f, x_max) est utilisé sans rappel (prérequis de 1re année, vu en détail en ch10) : ajouter une puce de rappel ?
- ch9 : « chocs » seul (sans « efficaces ») a aussi été remplacé par « rencontres » ; si tu veux garder « chocs » à l'oral, ne régénère pas ces réactions.
- ch10 (p6, 2024 N) : x(48 h) ≈ 0,38 mmol dans le cours, mais la tangente donnée limite à 0,37 mmol (la figure donne 0,365). Corriger changerait la voix de p6.
- ch11 : « acide fort / acide faible », « amphotère », « ampholyte » apparaissent dans des réactions ; ils ne sont pas dans le JSON officiel, laissés. « [H₃O⁺]_éq » est utilisé avant que l'état d'équilibre soit défini (notation du national).
- ch12 : la carte annonce « au semestre 2, les piles : Qr,i comparé à K » (annonce, pas la règle) ; l'exercice n5 sur l'hydrolyse (sous-domaine 4) a été remplacé par K' = 1/K sur la même estérification.
- ch13 : la concentration massique C_m = C·M est dans la compétence C7 et le bilan, mais aucune diapositive ne l'enseigne (à ajouter, ou à retirer du bilan) ; « 17 sessions sur 20 » non vérifiable ; « le sens direct est favorisé » (K > 1) frôle le critère d'évolution.

### Cours ch9 — Transformations lentes et rapides

| Diapositive (id) | Avant → après | Raison |
|---|---|---|
| tl_o1_carte (QCM, option A) | « Mesurer la couleur … au spectrophotomètre » → « Citer un exemple de transformation très lente » | spectrophotométrie hors cadre ; distracteur pris dans le programme |
| tl_o1_carte (réactions 0.1 et 0.2, ecrit + parole) | « le spectrophotomètre mesure la couleur… » → « un exemple de transformation très lente (la rouille) fait partie du chapitre, mais ne revient pas à chaque session » | suit le nouveau distracteur |
| tl_x6_eau (lead) | « Les mêmes gestes pour deux couples du national » → « … pour un couple du national : l'eau oxygénée » | la diapo ne traite qu'un couple |
| tl_x6_eau (exercice e1, réactions 2.1 et 2.2, ecrit + parole) | « équilibrée en matière et en charge » / « sens de l'oxydation » → « atomes équilibrés, mais charges −2 et +2 ; électrons du côté du réducteur H₂C₂O₄ » | erreur : le distracteur H₂C₂O₄ + 2e⁻ ⇌ 2CO₂ + 2H⁺ n'est pas équilibré en charge |
| tl_x6_eau (exercice e0, réaction 2.2, ecrit) | « tu as écrit l'oxydation » → « électrons à droite : charges −2 et −6 » | le distracteur n'est pas une oxydation valable |
| tl_x6_eau (exercice e2, 4 ecrits) | « Ox + n e⁻ = Red », « I2 + 2 e- », « H2O2 » → ⇌ et indices | notation du cours (⇌ pour les demi-équations) |
| tl_x9_oxalique (exercice e0, réaction 1.1, ecrit + parole) | « repère l'oxydant le plus fort » → « l'énoncé donne les réactifs, ils s'écrivent à gauche » | « oxydant le plus fort » renvoie à l'échelle des potentiels (hors cadre) |
| tl_x10_verifier (exercice e1, affirmation 1, réaction juste, ecrit + parole) | « charge nulle à gauche et à droite » → « −4 à gauche et −4 à droite » | erreur : S₂O₈²⁻ + 2I⁻ → 2SO₄²⁻ + I₂ a une charge −4 |
| tl_x10_verifier (exercice e1, affirmation 3, réactions juste et 1.2, ecrit + parole) | « H₂O₂ est l'oxydant » → « S₂O₈²⁻ est l'oxydant » | erreur : pas d'eau oxygénée dans cette réaction |
| tl_f1_facteur (puce, trace, cahier, cahier de séance 3, voix fr + mixed) | « Les deux facteurs de ce chapitre » → « On commence par deux facteurs … (le catalyseur vient plus loin) » | contradiction avec tl_t3 (le catalyseur est le 3e facteur du chapitre) |
| tl_r8_duree (réactions 0.2 et 1 juste, ecrit + parole) | « les chocs entre elles », « se heurtent / كيتصادمو » → « s'agitent plus et se rencontrent plus souvent » | théorie des chocs hors cadre (décision de la fiche) |
| tl_f5_concentre (réaction 0.2, ecrit + parole) | « plus les chocs entre réactifs sont nombreux » → « plus les entités se rencontrent souvent » | idem |
| tl_n2_glacee (exercice e0, réactions 0.1, 0.2, 1 juste) | « énergie des chocs », « chocs efficaces », « الصدمات », « réduit le rendement » → « agitation des entités », « favorise les rencontres », « l'eau dilue le mélange » | chocs efficaces / rendement hors de ce chapitre |
| tl_n2_glacee (exercice fin e1, 4 réactions, ecrit + parole) | « chocs (efficaces) », « collisions » → « les entités se rencontrent plus / moins souvent » | théorie des collisions hors cadre |
| Compétences C5_r4 (réaction 1.2) et C6_r4 (réaction 0.2) | « plus de chocs », « les chocs كيقلو » → « se rencontrent plus / moins souvent » | idem |
| tl_n1_lecture (exercice e1, 4 réactions, ecrit + parole) | « état d'équilibre », « constante d'équilibre », « accélère dans les deux sens », « estérification limitée » → « état final », « mêmes quantités initiales », « le catalyseur n'est pas dans l'équation » | équilibre et constante d'équilibre hors de ce chapitre |
| tl_f7_palier (nouvelle 1re puce) | — → « Rappel : le réactif limitant est celui qui est entièrement consommé le premier ; il fixe la quantité finale de produit. » | prérequis utilisé sans être rappelé |
| Compétence C7 (cadre_ids) | TLR6, TLR7 → TLR5, TLR6, TLR7 | le catalyseur appartient à TLR5 |
| Compétence C1, rappel C1_r3 | Fe²⁺ + Ce⁴⁺ → Fe³⁺ + Ce³⁺ → MnO₄⁻ + 5Fe²⁺ + 8H⁺ → Mn²⁺ + 5Fe³⁺ + 4H₂O (énoncé, attendu, enonce_dit) | le couple du cérium n'est pas au programme ; on reprend une réaction du cours |
| 17 réactions écrites (tl_x3b_couple, tl_x9_oxalique, tl_x10_verifier, rappels C1, séance 1) | demi-équations écrites avec → (ex. S₂O₈²⁻ + 2e⁻ → 2SO₄²⁻) → ⇌ | règle de la fiche : ⇌ pour les demi-équations |
| Simulation equation.html (D.d1 / D.d2 des 4 vues) | demi-équations avec → → ⇌ | même notation que les diapos tl_x7 à tl_x9 (contenu seulement) |

Voix à refaire :
- tl_f1_facteur : speech_text fr et mixed (les mots du pointage sont gardés tels quels)
- tl_o1_carte : réactions q 0.1 et q 0.2 (parole)
- tl_x6_eau : exercice e1, réactions 2.1 et 2.2 (parole)
- tl_x9_oxalique : exercice e0, réaction 1.1 (parole)
- tl_x10_verifier : exercice e1s0 réaction 1/juste ; exercice e1s2 réactions 0/juste et 1/2 (parole)
- tl_r8_duree : réactions q 0.2 et q 1/juste (parole)
- tl_f5_concentre : réaction q 0.2 (parole)
- tl_n2_glacee : concentration.reponses e0 0.2 et 1/juste ; reponses_fin_de_cours e1s0 1/juste, e1s1 0/juste, e1s1 1/1, e1s1 1/2 (parole)
- tl_n1_lecture : reponses_fin_de_cours e1s0 0/juste, e1s0 1/1, e1s2 0/2, e1s2 1/juste (parole)
- Compétence C5, rappel C5_r4 réaction 1.2 ; compétence C6, rappel C6_r4 réaction 0.2 (parole)
- Compétence C1, rappel C1_r3 : enonce_dit (audio enonce_rappel_C1_r3)

Points vérifiés sans erreur
- Les 7 compétences pointent sur des capacités qui existent (TLR1 à TLR7) ; chaque partie et chaque diapo correspond au sous-domaine 1 du cadre (oxydoréduction, rapide/lente, facteurs cinétiques) ou au catalyseur (sous-domaine 4), sans types de catalyse.
- Toutes les équations finales et demi-équations justes du cours, des exercices et des simulations ont été recomptées avec python (éléments et charges) : Zn/Cu²⁺, H₂O₂/I⁻, MnO₄⁻/Fe²⁺ (+17/+17), MnO₄⁻/H₂C₂O₄ (+4/+4, 16 − 10 = 6 H⁺), S₂O₈²⁻/I⁻ (−4/−4), I₂/S₂O₃²⁻ (−4/−4), les 8 demi-équations de la fiche.
- Calculs : C = 0,02/0,5 = 0,04 mol/L ; n = 0,1 × 0,2 = 0,02 mol ; 30/10 = 3 ; palier n(I₂) = n(H₂O₂)₀ (2 puis 4 mmol) ; toutes les bonnes réponses (champ correct) des QCM et vrai/faux sont cohérentes avec leurs réactions.
- Couleurs conformes aux valeurs de référence (MnO₄⁻ violet, Cu²⁺ bleu, I₂ jaune à brun, soufre trouble blanc-jaune) ; durées des simulations cohérentes avec les diapos (20 °C : 30 min ; 40 °C : 10 min ; 0,2 mol/L : 15 min).
- Ordre logique : rappels (ion, conservation, mole, concentration) avant usage ; chaque compétence est travaillée puis évaluée (4 rappels par compétence + exercices) ; la fiche « Ce qu'il faut retenir » et la carte reprennent les 7 compétences.
- Aucun terme hors cadre restant (recherche des listes hors_cadre.mots et termes_hors_programme dans écran, voix, questions, réactions, cahier, retrouver, exercices et textes des simulations) ; verifier_figures_cahier.py : 0 erreur avant et après.

À trancher par l'utilisateur
- L'avancement x, x_f et « avancement maximal » sont utilisés (tl_t4_courbes, tl_n1_lecture, tl_f8_variable, rappel C7_r4) sans rappel dans ce chapitre (prérequis de 1re année, vu en détail au chapitre suivant). Ajouter une courte diapo de rappel, ou une puce, si tu veux que le cours parte vraiment de zéro.
- Le mot « chocs » seul (sans « efficaces ») a été remplacé partout par « rencontres » pour suivre la décision de la fiche ; cela fait plusieurs voix à refaire. Si tu préfères garder « chocs » dans la voix, il suffit de ne pas régénérer ces réactions (l'écrit reste juste).
- Rappel C7_r3 (parole juste) : « le plus rapide a le facteur cinétique le plus fort » est flou mais pas faux ; laissé tel quel.

### Cours ch10 — Suivi temporel, vitesse de réaction

| Diapositive (id) | Avant → après | Raison |
|---|---|---|
| ci_o1_carte (réactions q.0.1, q.0.2, q.1.juste, q.2.2) | « t₁/₂ : x atteint la moitié de x max » → « x = x_f/2 » (écrit et voix) | Définition de t₁/₂ fausse en règle générale |
| ci_h4_comparer (e0.0.2, e0.1.juste) | La voix disait « t un demi = نص ديال x max، ماشي x f » → t₁/₂ à x_f/2 ; x_max/2 seulement si totale | Contredisait la bonne réponse et la définition |
| ci_n1_aspirine (e1.0.1, e1.0.2, e1.1.juste, e1.2.1, e1.2.2) | « t₁/₂ est la date où x = x_max/2 » → « x = x_f/2, ici x_f = x_max (totale) » ; « 35 s ≈ x_max/4 » → « à 35 s, x ≈ 0,8 mmol » | Règle de t₁/₂ |
| ci_n2_diminue e1s0.1.2 | « x_f n'est pas 0,8 mmol, x_f > 0,8 mmol » → x_f = x_max = 0,8 mmol donné par le texte, t₁/₂ = 4 min | Faux : x_f ne peut pas dépasser x_max ; contredisait la bonne réponse (Vrai) |
| ci_n2_diminue e1s2.1.2 | « la bonne réponse est faux » → « Vrai : à la fin, v = 0 » | Contredisait la bonne réponse |
| ci_n2_diminue e1s1.0.2, e1s1.1.juste, e1s1.0.1 | « à 2·t₁/₂, x = 3/4 de x_max » → lecture x(8 min) = 0,6 mmol < x_f | Propriété d'une loi d'ordre 1 (hors programme) |
| ci_h3_pieges (explication statement 0, e0s0.0.2) | « à 2·t₁/₂, x ≈ 3/4 de x_f » → lecture de l'exemple A (1,5 < 2,0 mmol) | Idem |
| ci_g6_calcul e1s1.1.2 | « Faux : x_f ≠ x_max, équilibre » → « Vrai : σ = σ_f donne x = x_max » | Contredisait la bonne réponse, notion d'équilibre hors chapitre |
| ci_n5_trois e1s2.0.2 | voix « 27 mmol » → « cent trente-trois millimoles » ; écrit « équilibre » → « état final » | Valeur fausse ; équilibre = chapitre suivant |
| ci_v8_temperature e1s1.1.juste | voix « توصل للتوازن » → « l'état final » | Équilibre hors chapitre |
| ci_v8_temperature e1s2 (0.juste, 1.1, 1.2) | « chocs / collisions entre entités » → « les entités se rencontrent plus souvent » | Vocabulaire de la théorie des collisions ; aligné sur v6 et le périmètre |
| ci_v8_temperature e0.2.1 | voix pente « 0,57 » → « 0,75 mmol/min » | Valeur fausse |
| ci_v4_bareme q.1.2 | voix « tu as divisé par V en mL » → « mauvaise conversion (0,01 L au lieu de 0,100 L) » | 25 vient de V = 0,01 L, pas de V en mL |
| ci_v4_bareme e1.0.juste ; e1.2.1 | voix bafouillée « سبعة و خمسين... لا » supprimée ; écrit v₀ → v(t₁) | Erreur de texte ; t₁ = 60 h |
| ci_a6_composition e1.0.1 | voix « 1,66... لا » → « un virgule soixante-neuf » | Valeur fausse / bafouillage |
| C5_r2 (rappel) | options 1,0·10⁻² et 0,01 (identiques) → option C = 1,0 mol·L⁻¹·s⁻¹ ; voix 0.juste « 0,75 sur 57 s » → « sur 75 s » ; réaction 2.2 adaptée | Deux options égales ; valeur fausse |
| ci_p4_2016R (puces 2-3, trace, cahier, cahier séance s3) | « x = x_max/2 » → « x_f/2 = x_max/2 (transformation totale) » ; « vue à la séance 3 » → « séance 4 » | Règle de t₁/₂ ; t₁/₂ est enseigné en séance 4 |
| ci_n2_diminue (lead, puce 0) | « Saponification » → « Un ester avec les ions hydroxyde » ; « (réaction étudiée plus tard) » | Décision de la fiche : ne pas nommer la saponification |
| ci_n3_deux (lead) | « Deux estérifications » → « Deux réactions avec l'éthanol » | Une des deux est un anhydride |
| ci_n7_conductance e0s1 (écrit) | G = σ·S/L → G = k·σ (k constante de cellule, en m) | Même notation que le cours (g1) |
| ci_n7_conductance e0s2.0.2 | « et non 12,5/2 » → « et non 12,5 mS (moitié de G₀ ≈ 25 mS) » | Erreur |
| ci_m3_titrage, n7, n4, p6, h1, h3, h4, a5, n2, g6, r1, C6_r2 (écrits) | « S2O3^2- », « n de I2 égale C fois V E sur deux », « x f », « x max », « zéro virgule trente-huit », « 10^-2 », « 0.5 »… → notation (S₂O₃²⁻, n(I₂) = C·V_E/2, x_f, 0,38 mmol, 10⁻², 0,5) ; « 2,5 mol·m⁻³ » → « ·min⁻¹ » ; « V = 0,050 L » retiré de C6_r2 | Formules en notation à l'écran ; unité incomplète ; valeur hors contexte |
| C4_r1 2.2, C4_r3 1.1/1.2 (voix) | « quaranteminutes », « xf », « xmax » → « quarante minutes », « x f », « x max » | Fautes de frappe lues par la synthèse vocale |
| figures.html (2016 R, 2018 R, 2019 R) | « à x_max/2 » → « x_f/2 = x_max/2 » ; palier 2019 R « x_max » → « x_f = x_max » | Règle de t₁/₂ |
| figures.html (2016 R, 2018 R, 2021 N, 2025 R) | « saponification » → « ester avec les ions hydroxyde » ; titre 2017 N « deux estérifications » → « deux réactions avec l'éthanol » | Décision de la fiche |
| figures.html (2025 N, courbe a) | t₁/₂(a) 40 min → 45 min | Les réactions disent « 45 min = t₁/₂ de la courbe (a) » |

Voix à refaire :
- ci_o1_carte : q.0.1, q.0.2, q.1.juste, q.2.2
- ci_a6_composition : e1.0.1
- ci_g6_calcul : e1s1.1.2
- ci_v4_bareme : q.1.2, e1.0.juste
- ci_v8_temperature : e0.2.1, e1s1.1.juste, e1s2.0.juste, e1s2.1.1, e1s2.1.2
- ci_h3_pieges : e0s0.0.2
- ci_h4_comparer : e0.0.2, e0.1.juste
- ci_n1_aspirine : e1.0.1, e1.0.2, e1.1.juste, e1.2.1, e1.2.2
- ci_n2_diminue : e1s0.1.2, e1s1.0.2, e1s1.1.juste, e1s2.1.2
- ci_n5_trois : e1s2.0.2
- Rappels : C4_r1 2.2, C4_r3 1.1, C4_r3 1.2, C5_r2 0.juste, C5_r2 2.2
(Aucun speech_text de diapositive modifié ; les énoncés lus ne changent pas. C5_r2 : l'option C affichée a changé, l'enonce_dit ne lit pas les options.)

Points vérifiés sans erreur
- Calculs refaits en Python : titrage (V_E 12,6 et 16,9 mL → 1,26 et 1,69 mmol), x_max/réactif limitant (exemple A, exercices, 2019 R), σ₀ = 0,249 et σ_f = 0,091 S/m, x(σ) = 0,50 et 0,80 mmol, loi des gaz (x = 1,0 et 0,50 mmol), vitesses (2,5 ; 7,5 ; 1,6 ; 1,25·10⁻² ; 1,0·10⁻³ ; 0,525 ; 0,78), relations 2016 R, 2018 R, 2021 N.
- Cohérence avec les modèles des simulations : exemple A (x = 2(1−e^(−t/8)) : mesures, t₁/₂ = 5,5 min, v(8) = 0,92, v(20) = 0,21, x(11 min) = 1,5), exemple B (t/(t+10) : σ(10) = 0,170, σ(40) = 0,123), 2019 R, 2025 R, 2023 N, 2021 N, 2018 R (G(34 min) ≈ 13,5 mS).
- Le champ correct de toutes les questions, exercices, rappels et blocs correspond à la réaction « juste ».
- Les cadre_ids C1-C8 → CIN1-CIN8 existent ; chaque compétence a ses diapositives et ses rappels ; ordre des prérequis respecté (tableau et réactif limitant avant x(t), conductivité avant l'exemple B, totale/x_f avant t₁/₂).
- Aucun terme interdit (ordre de réaction, loi de vitesse, Arrhenius, énergie d'activation, Beer-Lambert, absorbance, types de catalyse) dans le cours ni dans les simulations ; les exponentielles restent dans le code de calcul seulement.
- JSON rechargé, format identique ; verifier_figures_cahier : 0 erreur avant et après.

À trancher par l'utilisateur
- 2024 N (p6) : le cours lit x(48 h) ≈ 0,38 mmol, mais avec la tangente donnée ((0 ; 0,25) et (60 h ; 0,40)) x(48 h) ne peut pas dépasser 0,37 mmol ; la figure donne 0,365. Passer à « ≈ 0,37 mmol » changerait la voix de p6 (fr + mixed) et plusieurs réactions : non fait.
- conductimetrie.html garde le nom interne de vue « saponification » (identifiant d'URL, pas affiché).
- C1_r1 (voix 0.1) cite « l'expérience d'estérification » pour la trempe du diiode : maladroit mais pas faux, non modifié.
- « Chocs des molécules » reste dans le rappel sur la pression d'un gaz (z6_gaz), où il explique la pression et pas la vitesse : laissé tel quel.

### Cours ch11 — Transformations dans les deux sens

Fichier modifié : backend/data/courses/phys_ch11_transformations_deux_sens.json (45 corrections dans 41 champs). Simulations : aucune modification nécessaire.

| Diapositive (id) | Avant → après | Raison |
|---|---|---|
| td_b1_acide (q.0 juste, écrit) | `CH₃COOH = CH₃COO⁻ + H⁺` → `CH₃COOH → CH₃COO⁻ + H⁺` | même flèche que l'écran |
| td_b3_couple (fin e1s0, e1s2, écrit) | `H₃O⁺ = H₂O + H⁺`, `AH = A⁻ + H⁺` → avec ⇌ | demi-équation : ⇌, pas « = » |
| td_p4_eau (fin e1s0.1.1, écrit) | `AH + H₂O → A⁻ + H₃O⁺` → `⇌` | réaction limitée |
| td_a3_xf (fin e1s1.1.2, écrit) | `CH₃COOH + H₂O → …` → `⇌` | réaction limitée |
| td_a5_totale (fin e0, explication) | « 0,46 vient de pH/C mal posé » → « 0,46 : erreur de calcul » | pH/C = 460, explication fausse |
| td_n2_conductivite (fin e1s2.1.2, écrit) | `C₆H₅COOH + H₂O → …` → `⇌` | réaction limitée (τ = 0,22) |
| td_n2_conductivite (q.1.2, voix) | « la virgule a bougé de deux rangs » → « d'un rang » | 0,022 → 0,22 : un seul rang |
| td_n3_proportion (fin e0s1 juste, écrit + voix) | « s'est dissociée… la dissociation » → « a réagi avec l'eau… réaction très limitée » | « dissociation » : hors programme (coefficient de dissociation) |
| td_n3_proportion (fin e1 juste, écrit) | « forme non dissociée » → « n'a pas réagi avec l'eau » | même raison |
| td_n3_proportion (fin e1.1.2, écrit + voix) | 8,0·10⁻⁴ → 7,9·10⁻⁴ ; voix : « h trois », chiffres arabes → « la concentration des ions H trois O plus… sept virgule neuf » | 10^(−3,1) = 7,94·10⁻⁴ ; voix lisible |
| td_n4_dosage (fin e0s2.1.2, écrit) | « 1,6×10^-11 mol, environ 10^7 fois plus petit » → « 1,6×10⁻¹² mol, plus de 10⁸ fois plus petit » | 6,3·10⁻¹¹ × 0,026 = 1,6·10⁻¹² |
| td_n4_dosage (fin e0s2.0 juste, voix) | « un virgule seize fois dix puissance moins douze » → « un virgule six… » | valeur fausse |
| td_n4_dosage (fin e0s2.1.2, voix) | « … moins onze mole » → « … moins douze mole » | valeur fausse |
| td_c3_calcul (e0.2.1, voix) | « sigma doit être en mole par mètre cube » → « on divise sigma par la somme des λ : la concentration sort en mol/m³, puis ÷ 1000 » | σ est en S/m, erreur d'unité |
| td_c3_calcul (e0.1.1, e0.1.2, voix) | « [H₃O⁺] », « [H trois O plus] » → « la concentration des ions H trois O plus » | à l'oral : des mots, pas de notation |
| td_p2_calcul (fin e1.2.1, e1.2.2, voix) | « 3,4 » → « trois virgule quatre » | idem |
| td_p6_totale (fin e1.2.1, e1.2.2, voix) | « [H trois O plus] », « [H3O+] » → mots ; « moins log inverse » → « dix puissance moins deux » | notation lue à voix haute ; calcul mal dit |
| td_a3_xf (q.1.2, voix) | « 1,0·10⁻³ » → « un virgule zéro fois dix puissance moins trois » | notation lue à voix haute |
| td_n2_conductivite (q.1.2, e0.0.2, voix) | « τ », « σ » → « tau », « sigma » | idem |
| C5_r3 (2.2, écrit + voix) | « on divise par 10³… on ne multiplie pas » → « de mol/L à mol/m³, on multiplie une seule fois par 10³ » | sens de conversion inversé |
| C6_r1 (0 juste et 1.2, écrit ; 1.2 voix) | « plus l'acide est dissocié », « se dissocie davantage », « كيتفكك » → « la part de l'acide qui réagit avec l'eau est plus grande » | dissociation hors programme |
| C6_r3 (0.2, voix) | « كيتفكك كليا فالماء » → « كيتفاعل كليا مع الماء » | même raison |
| C3_r2 (2.2, voix) | « trois virgule nine » → « trois virgule neuf » | mot anglais dans la voix |
| C2_r2 (2.1), C3_r2 (0.1, 2.1, 2.2), C3_r3 (1.1), C6_r3 (1.2) (voix) | « [H trois O plus] », « [H₃O⁺] » → « la concentration des ions H trois O plus » | à l'oral : des mots |
| C7_r1 (2.2), C7_r3 (0 juste) (voix) | « le double sens ⇌ », « … ⇌ … » → « la double flèche » | symbole lu à voix haute |
| C7_r3 (enonce_dit) | « qu'est-ce que cela signifie, et pourquoi… ? » → « vrai ou faux ? » | la voix posait une question ouverte sur un vrai/faux |
| C6 (dit) | « la dilution augmente τ » → « … tau » | champ parlé |

Voix à refaire :
- td_p2_calcul : reponses_fin_de_cours e1 option 2 (1 et 2)
- td_p6_totale : reponses_fin_de_cours e1 option 2 (1 et 2)
- td_a3_xf : concentration.reponses q option 1 (2)
- td_c3_calcul : concentration.reponses e0 option 1 (1 et 2), option 2 (1)
- td_n2_conductivite : concentration.reponses q option 1 (2), e0 option 0 (2)
- td_n3_proportion : reponses_fin_de_cours e0s1 option 0 (juste), e1 option 1 (2)
- td_n4_dosage : reponses_fin_de_cours e0s2 option 0 (juste), option 1 (2)
- C2_r2 (2.1) ; C3_r2 (0.1, 2.1, 2.2) ; C3_r3 (1.1) ; C5_r3 (2.2) ; C6_r1 (1.2) ; C6_r3 (0.2, 1.2) ; C7_r1 (2.2) ; C7_r3 (0 juste, et enonce_dit → enonce_audio) ; compétence C6 (dit)
- Aucun speech_text (fr ou mixed) n'a été modifié : les mots du pointage restent valables.

Points vérifiés sans erreur
- Aucun terme des chapitres suivants ni hors programme (Qr, K, Ka, pKa, Ke, produit ionique, autoprotolyse, prédominance, indicateur, tampon, Lewis, Arrhenius, Ostwald, Henderson…) dans l'écran, la voix (fr et mixed), les questions, les réactions, le cahier, les exercices ou le texte des simulations. Ka n'apparaît que dans un commentaire de code (diluer.html), jamais affiché.
- Tous les calculs refaits en python : 10^(−3,4) = 4,0·10⁻⁴ ; τ = 0,040 / 0,13 / 0,32 ; HCOOH 0,13 ; x_max = 1,0·10⁻³ mol ; x_f = 4,0·10⁻⁵ mol ; σ : 0,399 mol/m³ et 10 mol/m³ ; 2019 N τ = 0,225 ; 2021 R C₁ = 1,58·10⁻², C₂ = 5,58·10⁻⁴ mol/L ; 2023 N τ = 0,0178, α = 0,982 ; 2022 N τ = 0,016 ; 2024 R 7,2·10⁻⁴ mol ; estérification 0,66 et 0,67.
- Exemple E (pH 3,6) et exemple D sont cohérents avec le modèle de la simulation (même acide, pH arrondis au dixième).
- Le champ `correct` de chaque QCM et vrai/faux (diapositives, fin de cours, rappels, séances) correspond à la réaction « juste ».
- Les cadre_ids C1-C7 renvoient tous à TD1-TD8, et chaque capacité est couverte. Ordre logique (Brønsted → pH → acide + eau → tableau, x_max, x_f, τ → deux sens, équilibre → conductimétrie → dilution → national → bilan) ; chaque compétence a ses rappels.
- Format JSON conservé (rechargement identique) ; verifier_figures_cahier.py : 0 erreur, 0 avertissement avant et après.

À trancher par l'utilisateur
- « acide fort / acide faible » (réactions de td_p2, td_p6, td_c3, td_n3, C3_r3, C4_r2, C6_r3) : ces mots ne sont ni dans mots_cles ni dans hors_cadre. Je les ai laissés. Faut-il les remplacer par « réaction totale / limitée » ?
- « [H₃O⁺]_éq » et « à l'équilibre » sont utilisés dès la partie IV (td_a3_xf, td_a6, fiche), avant que l'état d'équilibre soit défini (td_e3_etat, partie V). C'est la notation du national. Garder ou écrire « à l'état final » jusqu'à la partie V (la voix de td_a3_xf serait à refaire) ?
- « amphotère / ampholyte » apparaissent dans des réactions écrites (td_b3_couple, td_p5_ammoniac) : ces mots ne sont pas dans mots_cles. Je les ai laissés.
- td_cr_carte, voix : « tau par le pH, presque chaque année », alors que l'écran dit « τ par le pH (6 sessions) ». La différence est légère ; je n'ai rien changé.

### Cours ch12 — État d'équilibre

| Diapositive (id) | Avant → après | Raison |
|---|---|---|
| ee_r1_taux (V/F e1s0, 3 réactions) | « V n'est pas donné », « V = 1 L, x_max = 10⁻² mol », « Faux » → x_max = 1,0·10⁻² × 0,100 = 1,0·10⁻³ mol, réponse Vrai | Réactions fausses : V = 100 mL est donné, l'affirmation est vraie |
| ee_q5_sans_unite (QCM e0, 1er essai sur 3,09·10⁻²) | « vérifie la division par [CH₃COOH] » → « as-tu multiplié les deux concentrations ? » | Mauvais diagnostic (3,09·10⁻² = carré oublié) |
| ee_q5_sans_unite (QCM e0, 1er essai sur 9,0·10⁻⁸) | « carré oublié / puissance de dix » → « il manque la division par [CH₃COOH] » | Mauvais diagnostic |
| ee_q5_sans_unite (V/F e1s0 ×3, e1s1 ×2) | « les unités mol/L se simplifient » → « par convention, valeur en mol/L, Qr sans unité » | Faux pour Qr = [A⁻][H₃O⁺]/[AH] (mol²/L² ÷ mol/L) |
| ee_q5_sans_unite (V/F e1s2, 2e essai) | « son activité vaut un » → « l'eau, solvant, ne figure pas » | « activité » hors programme |
| ee_i2_melange (exercice e0, réaction juste) | quantités 5·10⁻³ et 10⁻² (exemple du cours) → 1,0·10⁻² ; 5,0·10⁻³ ; 1,0·10⁻² ; 2,0·10⁻² mol | Valeurs de l'exercice fausses dans la correction |
| ee_i2_melange (V/F e1s2) | « une concentration au numérateur, une au dénominateur » → deux et deux ; « comme K » retiré | Erreur ; K pas encore enseigné |
| ee_e1_concentrations (V/F e1s0, 2e essai) | « l'autoprotolyse de l'eau », « de votre part » → « ions H₃O⁺ de l'eau seule négligés » | Terme hors cadre (Ke, chapitre suivant) |
| ee_e3_expression (V/F e0s2, 2 réactions) | « concentration de référence 1 mol/L », « activité », « unités se simplifient » → convention : Qr,éq sans unité | Hors programme + faux |
| ee_k2_produits (QCM e0, 2e essai sur 5,5·10⁻²) | « ne tient pas compte du second terme du dénominateur » → « c'est τ, pas Qr,éq » | Mauvais diagnostic |
| ee_m4_national (QCM e0, parole) | « Ka égale le quotient… » → « K égale… » | Ka : chapitre suivant |
| ee_m4_national (V/F e1s1, 3 réactions) | « c0 = 1 mol/L », « C° » ; 2e essai « Faux est la bonne, constante d'acidité » → réponse Vrai, K sans unité | Hors programme + réaction contraire au champ correct |
| ee_f4_bilan (V/F e1s2, 2 réactions) | « l'équilibre se déplace dans le sens direct » → « C diminue, K = C·τ²/(1 − τ) constante, donc τ augmente » | Déplacement d'équilibre interdit |
| ee_f4_bilan (QCM e0) | « confusion avec le pH » → « erreur de calcul » | Explication sans sens |
| ee_n1_national (QCM e0) | « Qr,éq = KA » → « de l'ordre de 10⁻⁵ » | Ka hors chapitre |
| ee_n1_national (V/F e1s1 ×3) | « unités se simplifient » → convention sans unité | Faux pour ce quotient |
| ee_n1_national (V/F e1s2) | « activité égale à un », « on la compte comme un » → « le solvant ne s'écrit pas » | Hors programme |
| ee_n2_base (V/F e1s2) | « son activité vaut 1 » → « le solvant n'apparaît pas » | Hors programme |
| ee_n3_melange (exercice e0, juste) | « j'avais dit Qr,i = 1 à l'oral, c'était faux » → « ici ≠ 1 car concentrations différentes » | Phrase fausse (Qr,i = 1 est juste pour le national) |
| ee_n3_melange (V/F e1s2, juste) | « comme K à laquelle on le compare » → retiré | Critère d'évolution (sous-domaine 3) |
| ee_n4_pile (V/F e1s1, juste) | « leur activité vaut 1 » → « solides absents » | Hors programme |
| ee_n5_courbe (exercice e0 + 5 réactions + énoncé dit) | Hydrolyse d'un ester (2018 R), K = 0,25 → K' = 1/K de la même estérification : 1/4 = 0,25 | L'hydrolyse est une notion du sous-domaine 4 au-delà de l'exemple annoncé |
| ee_cr_carte (QCM, 2e essai) | « sert pour le sens d'évolution » → « sert quand on mélange plusieurs solutions » | Critère d'évolution hors cadre |
| Compétence C1 (rappel C1_r3, 3 réactions) | « unités se simplifient » → convention sans unité | Faux pour ce quotient |
| Compétence C4 (rappel C4_r2) | « Relis l'exemple C » → « la diapositive La réaction inverse » ; « K grand = réaction favorisée » retiré | Mauvais renvoi ; interprétation hors capacités |
| Compétence C5 (rappel C5_r2, 2e essai) | « tu as oublié (1 − τ) » → « 2,2·10⁻⁴ = C·τ : carré et (1 − τ) oubliés » | Mauvais diagnostic |
| Compétence C6 (rappel C6_r1, écrit) | « l'acide se dissocie davantage » → « la réaction avec l'eau est plus avancée » | Vocabulaire de la dissociation, hors cadre |

Voix à refaire :
- ee_r1_taux : reponses_fin_de_cours e1s0.0.juste, e1s0.1.1, e1s0.1.2
- ee_q5_sans_unite : reponses_fin_de_cours e0.1.1, e0.2.1, e1s0.0.1, e1s0.0.2, e1s0.1.juste, e1s1.0.juste, e1s1.1.2, e1s2.0.2
- ee_i2_melange : concentration.reponses e0.1.juste
- ee_e3_expression : concentration.reponses e0s2.0.2, e0s2.1.juste
- ee_k2_produits : reponses_fin_de_cours e0.1.2
- ee_m4_national : concentration.reponses e0.2.1 ; reponses_fin_de_cours e1s1.0.juste, e1s1.1.1, e1s1.1.2
- ee_f4_bilan : reponses_fin_de_cours e1s2.0.juste, e1s2.1.2
- ee_n1_national : reponses_fin_de_cours e0.2.2, e1s1.0.juste, e1s1.1.1, e1s1.1.2, e1s2.1.2
- ee_n2_base : reponses_fin_de_cours e1s2.0.2
- ee_n3_melange : concentration.reponses e0.0.juste ; reponses_fin_de_cours e1s2.0.juste
- ee_n4_pile : reponses_fin_de_cours e1s1.0.juste
- ee_n5_courbe : exercices_fin_de_cours[0].enonce_dit et demonstration.parole ; reponses_fin_de_cours e0 (0.1, 0.2, 1.juste, 2.1, 2.2)
- ee_cr_carte : concentration.reponses q.2.2
- compétences : C1_r3 (0.1, 0.2, 1.juste), C4_r2 (0.1, 1.2), C5_r2 (1.2)
- Aucun speech_text (fr ou mixed) n'a changé ; les pointages sont intacts.

Points vérifiés sans erreur
- Expressions de Qr : eau solvant et solides absents, coefficients en exposants (2I⁻ + S₂O₈²⁻, 3Cu²⁺ + 2Al, 2Ag⁺ + Cu), produits au numérateur ; équations équilibrées.
- Valeurs recalculées en Python : Qr,éq = 1,57·10⁻⁵ ; 1,61·10⁻⁵ ; 1,56·10⁻⁵ ; méthanoïque 1,81·10⁻⁴ ; K' = 6,25·10⁴ ; conductimétrie 0,118 → 1,58·10⁻⁵ ; 2019 N 6,2·10⁻⁵ ; 2021 N 1,77·10⁻⁵ ; 2022 R 5,0·10⁻⁴ ; Qr,i 0,25 / 1 / 4 / 1,5 / 1,25 ; courbes τ(C) (0,33/0,72 et 0,013/0,042).
- Champ `correct` de chaque QCM et vrai/faux cohérent avec les explications ; réactions corrigées là où elles le contredisaient (r1, m4).
- Simulations (textes, valeurs, équations) cohérentes avec le cours ; aucun terme hors cadre ; rien modifié.
- Ordre : log, concentration, τ, tableau et pH rappelés avant usage ; dilution rappelée (z3) avant f1 ; chaque compétence C1-C7 a une question ; cadre_ids EE1-EE7 existent ; bilan aligné sur les compétences ; vérificateur de figures 0 erreur avant et après.

À trancher par l'utilisateur
- ee_cr_carte (écran, voix) et carte.html annoncent « au semestre 2, les piles : Qr,i comparé à K ». La règle n'est ni énoncée ni appliquée, mais l'idée est annoncée. Faut-il garder cette annonce ou écrire seulement « les piles » ?
- ee_n5_courbe : l'estérification reste comme exemple de K lu sur une courbe, comme le prévoit la fiche. L'exercice de fin parle maintenant de K' = 1/K sur la même réaction, sans le mot « hydrolyse ». À supprimer si l'exemple gêne la règle « eau solvant ».
- Dans ee_i2_melange e1s2.0.juste, la voix dit encore « comme la constante d'équilibre K » avant que K soit enseigné. C'est un détail laissé tel quel ; l'écrit a été corrigé.
- C6_r1 : la voix dit encore « l'acide se dissocie plus » (en darija). C'est juste, mais ce n'est pas le vocabulaire du cadre. L'écrit a été corrigé.
- Les réactions dont la voix a changé gardent leur ancien champ `audio` (fichiers v12 désormais faux) jusqu'au réenregistrement.

### Cours ch13 — Réactions acido-basiques

Fichier corrigé : backend/data/courses/phys_ch13_acides_bases.json. Les simulations n'ont pas été modifiées : aucune erreur ni aucun terme hors programme trouvé dans leurs textes.

| Diapositive (id) | Avant → après | Raison |
|---|---|---|
| (cours) title | « Transformations liées aux réactions acide-base » → « Transformations associées aux réactions acido-basiques » ; ajout du nouveau titre en tête de lesson_match | Titre officiel (le catalog ne contient pas le titre) |
| ab_n1_2016n (e1s0, réponse juste) | « la relation de Henderson » → « la relation pH = pKa + log(base/acide) » ; « au point E, pH = 8,7 » → « à V_B = 7 mL, pH = 11,6 » | Terme hors cadre ; l'énoncé porte sur V_B = 7 mL |
| ab_n1_2016n (e1s1, 1er essai) | pKa « environ 4,8 » → 4,9 ; pH « 8,7 et au-delà » → 11,6 à V_B = 7 mL | Valeur fausse (acide propanoïque : 4,9) |
| ab_n4_2024r (e0, choix 11,4) | « Henderson Hasselbalch » → la relation ; « 11,4 est le pH de la solution » → « 11,4 vient du rapport à l'envers (log 4) » | Terme hors cadre ; la solution a pH = 11,88 |
| ab_cr_carte (question) | « la relation de Henderson » → « la relation pH = pKa + log(A⁻/AH) » | Terme hors cadre |
| ab_a4_ammonium (e0, choix 3,3) | « 3,3 correspond au pKb » → « 3,3 = −log Qr,éq : on a pris Ka = Qr,éq » | pKb hors cadre |
| ab_a4_ammonium (e1s1, ×2) | « constante (de basicité) Kb, Ka = Ke/Kb » → « Qr,éq de la réaction de la base avec l'eau, Ka = Ke/Qr,éq » | Kb hors cadre |
| ab_b3_national (e1s0, 1er essai) | voix : « différence entre pH et pOH » → « entre [H₃O⁺] et [HO⁻] » | pOH hors cadre |
| ab_b3_national (e1s2, ×3) | τ de l'ammoniac « environ 1 % / 0,01 » → 0,040 (4 %) ; voix déformée « بزوج فرانك فالمية » → « 20 % » | Valeur fausse (cours : τ = 0,040) |
| ab_w4_ho (e1s0) | « autoionisation de l'eau » → « autoprotolyse de l'eau » | Mot du programme |
| ab_b2_taux (e0, choix 8,5·10⁻⁸, ×2) | « 8,5·10⁻⁸ est [H₃O⁺] » → « 8,5·10⁻⁸ = 10^(−pH)/C, la formule d'un acide » | Faux : [H₃O⁺] = 8,5·10⁻¹¹ |
| ab_a1_ka (e0s1, ×2) | « les unités se simplifient » ; « concentration de référence » → « sans unité, comme toute constante d'équilibre » | Raison fausse (mol/L ne se simplifie pas) ; c° hors cadre |
| ab_a3_mesure (question, choix 3,41) | écrit : Ka = 10^(−pH)/(C − 10^(−pH)) → 10^(−2pH)/(C − 10^(−pH)) | Il manquait le carré (la voix était juste) |
| ab_a3_mesure (exercice, 2 réponses) | suppression de « ma formule orale était incomplète » et de « plutôt 4,77 que 4,8 » | Remarques internes fausses (4,79 est cohérent avec 4,8) |
| ab_c3_classement (e1s2) | suppression de « hors de 0–14, l'acide ou la base réagit avec l'eau elle-même » | Notion hors programme |
| ab_e3_indicateur (e1, ×2) | phénolphtaléine « après », hélianthine « avant » l'équivalence → l'inverse (le pH descend) | Erreur (base dosée par un acide) |
| ab_n3_2022n (vrai/faux) | suppression de « (Le corrigé du dépôt écrit ⇌ : c'est une erreur.) » | Note interne visible par l'élève |
| ab_e5_conductimetrie, ab_e5b_pourquoi | compétence C7 (AB8) → C8 (AB9) | AB9 et le libellé de C8 contiennent « courbe σ = f(V) » |
| séances ab_s3, ab_s4, ab_s5 | titres réécrits selon le vrai contenu (la séance 3 contient les indicateurs ; la séance 4 l'équivalence et la courbe ; la séance 5 la conductimétrie) | Les anciens titres ne correspondaient plus aux blocs |

Voix à refaire (parole de réaction ; aucun speech_text modifié) :
- ab_a1_ka : reponses_fin_de_cours e0s1/0/2, e0s1/1/juste
- ab_a3_mesure : concentration.reponses e0/0/2, e0/1/juste (audio v12 existant)
- ab_a4_ammonium : reponses_fin_de_cours e0/2/2, e1s1/0/2, e1s1/1/juste
- ab_b2_taux : reponses_fin_de_cours e0/0/1, e0/0/2
- ab_b3_national : reponses_fin_de_cours e1s0/0/1, e1s2/0/juste, e1s2/1/1, e1s2/1/2
- ab_c3_classement : reponses_fin_de_cours e1s2/0/juste
- ab_cr_carte : concentration.reponses q/0/1 (audio v13 existant)
- ab_e3_indicateur : reponses_fin_de_cours e1/0/2, e1/1/2
- ab_n1_2016n : reponses_fin_de_cours e1s0/0/juste, e1s1/0/1
- ab_n4_2024r : reponses_fin_de_cours e0/1/1
- ab_w4_ho : reponses_fin_de_cours e1s0/1/2

Points vérifiés sans erreur
- Recalculs en Python : pH 3,41 / 2,90, [HO⁻] = 2,57·10⁻¹¹ et 3,98·10⁻⁴ mol/L, τ = 0,040 / 0,20 / 0,117, Ka = 1,57·10⁻⁵ (pKa 4,8), 2023 N : 4,79, NH₄⁺ : 6,06·10⁻¹⁰ (9,2), méthylamine 10,7, K = 11 / 8,9·10⁻² / 2,5·10⁴ / 1,6·10⁹ / 9,1·10⁻² / 7,9·10⁵ / 1,26·10⁹ / 8,13·10⁹, distribution (90,9 % ; 20 % à pH 4,2), 2022 N (0,316 ; 76 %), 2024 R (10,2), 2022 R (1,26·10⁻⁸), conductimétrie (38,8 / 11,4 / 33,5 mS/m, C_A = 1,0·10⁻² mol/L).
- Toutes les QCM (question, exercises, exercices_fin_de_cours, rappels, séances) : le champ correct correspond à l'explication et aux réactions « juste ».
- Ke = 10⁻¹⁴ à 25 °C, pKa de l'eau 0 et 14, K = Ka₁/Ka₂ (Ka₁ = couple de l'acide qui réagit), K = Ka/Ke, zones de virage (3,1–4,4 ; 4,2–6,2 ; 6,0–7,6 ; 7,2–8,8 ; 8,2–10) : justes dans le cours et dans les simulations (indicateurs.html, exploiter.html, comparer.html, acidite.html, figures.html).
- Ordre : Ke avant [HO⁻], Ka avant la prédominance, tableau et réactif limitant avant l'équivalence, pente avant la dérivée ; chaque compétence a des diapositives puis des rappels ; les cadre_ids AB1–AB10 existent dans la fiche.
- Plus aucun terme de hors_cadre.mots ni des motifs termes_hors_programme (acides_bases, dosage) dans le cours ni dans les simulations ; aucune solution tampon ; le critère d'évolution est seulement renvoyé au semestre 2 (k4).
- Format json.dumps(indent=2) + '\n' conservé et rechargé ; verifier_figures_cahier.py : 0 erreur avant et après.

À trancher par l'utilisateur
- Concentration massique C_m = C·M (AB8, libellé de C7, bilan ab_bl_fiche) : aucune diapositive ne l'enseigne et aucun exercice ne l'utilise (l'exemple N de la fiche, 499,2 g/L, n'est pas utilisé). Faut-il ajouter un exercice (par exemple en e4) ou retirer C_m du bilan ?
- « 17 sessions sur 20, un dosage dans 13 » (ab_o1_carte, ab_cr_carte) : ces chiffres ne sont pas vérifiables depuis le cours.
- Les réactions de k4 disent « le sens direct est favorisé » quand K > 1. Ce n'est pas le critère Qr/K, mais on peut le neutraliser si on veut éviter toute allusion au sous-domaine 3.

