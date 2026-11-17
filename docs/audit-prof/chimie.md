# Audit des cours de chimie face aux cours de professeurs

17 novembre 2026. Nos 5 cours de chimie sont comparés au cours complet du Pr Nidal Naceiri Mrabti (2 PC, p. 113-174). Ils sont aussi comparés aux cours et résumés de 2 bac BIOF publiés sur moutamadris (même programme de chimie) et au cadre de référence officiel. Les copies auditées sont les copies en attente, dont les démonstrations ont été reprises le matin.

Un manque est **confirmé** quand au moins deux professeurs l'écrivent, ou un seul et le cadre officiel l'exige.

## Bilan

| Chapitre | Manques confirmés | haute | moyenne | basse | Démonstrations qui sautent des étapes |
|---|---|---|---|---|---|
| 9. Transformations rapides et lentes | 13 | 4 | 5 | 4 | 4 |
| 10. Suivi temporel, vitesse de réaction | 16 | 4 | 7 | 5 | 9 |
| 11. Transformations dans les deux sens | 15 | 3 | 6 | 6 | 5 |
| 12. État d'équilibre | 10 | 3 | 5 | 2 | 9 |
| 13. Réactions acido-basiques | 8 | 3 | 2 | 3 | 12 |
| **Total** | **62** | **17** | **25** | **20** | **39** |

## Ce qui revient dans plusieurs chapitres

1. **États physiques encore oubliés** dans des champs écrits : cahiers (« Zn + Cu²⁺(aq) », couples écrits « CH₃COOH ⇌ CH₃COO⁻ + H⁺ »), réponses attendues, réactions, et surtout les équations dessinées par les simulations du ch13 (eau, base, dosage, exploiter, acidité, comparer).
2. **Couples et demi-équations** : aucun exercice ne fait identifier les deux couples à partir d'une équation (ch9, ch10), alors que le cadre l'exige.
3. **Relations posées sans démonstration** : σ(x) donné sans tableau d'avancement ni n₀ ; x_max sans calcul ; σ jamais écrite en fonction de x_f et V ; G = k·σ et σ = Σλᵢ[Xᵢ] absentes.
4. **Définitions incomplètes** : transformation totale (x_f = x_max) et limitée (x_f < x_max) ; transformation rapide « ni avec les appareils de mesure courants » ; équivalence par les proportions stœchiométriques ; Ke « constante d'équilibre de l'autoprotolyse ».
5. **Notations du bac** : « sens direct / sens inverse » (nous disons « sens 1 / sens 2 ») ; vitesse v = (1/V)·dn/dt et v = d[X]/dt depuis une courbe n(t) ou [X](t).
6. **Tableaux d'avancement incomplets** (deux lignes seulement, sans l'état intermédiaire).

## Détail par chapitre

### Transformations rapides et transformations lentes

Sources lues :
- Notre cours : copie en attente `backend/data/courses/en_attente/phys_ch9_transformations_lentes_rapides.json` (écran, cahier, centre, voix, questions, exercices, séances, compétences ; recherche de toutes les équations écrites par script) + texte `nos-cours/phys_ch9_transformations_lentes_rapides.txt`.
- Pr Nidal Naceiri Mrabti, cours 2 PC, p. 113-123 (pas de décalage : page du sommaire = page du PDF) ; lues en image p. 114-123 (p. 121-123 : pages quadrillées vides).
- m_lentes_1 (Ahmed Hakim, 2 Bac international, scan) : p. 1-6 en image.
- m_lentes_2 (Pr Hicham Mahajar / Pr Youssef Tabit) : p. 1-5 en image.
- m_lentes_3 (Naoual Bendaoud) : p. 1-5 en image.
- m_lentes_4 (manuel de Terminale S français, « Chimie 2 », scan) : p. 1-8 en image (notation « = » française).
- Cadre officiel PDF : p. 14 sur 29 (savoir-faire, sous-domaine 1) et p. 23 sur 29 (programme, sous-domaine 1) en image ; fiche `cadre_reference_2bac_pc.json` (TLR1-7) ; `docs/audit-programme-officiel/chimie.md` (ch9). `experience_profs.json` : pas de clé `transformations_lentes_rapides`.

#### Plan comparé

| Partie chez les professeurs | Où chez nous | Remarque |
|---|---|---|
| Oxydant, réducteur, couple (« espèces conjuguées »), demi-équation (Nidal p. 115 ; m_lentes_1 p. 1-2 ; m_lentes_2 p. 1-2 ; m_lentes_3 p. 1 ; m_lentes_4 p. 1-2) | tl_x1_zinc → tl_x3b_couple | Complet, sauf le mot « conjugué » et l'équation générale n₂Ox₁ + n₁Red₂ (voir manques) |
| Demi-équation en milieu acide, 4 étapes (Nidal p. 116 ; m_lentes_4 p. 2-3) | tl_x4_oxygene → tl_x6b_diiode | Complet, avec la vérification des charges |
| Équation d'oxydoréduction, multiplier, additionner (tous) | tl_x7_equation → tl_x10_verifier | Complet ; aucun exercice « identifier les deux couples à partir de l'équation » |
| Transformation rapide : précipité Cu(OH)₂ ou AgCl, acide-base, définition avec « états intermédiaires » (Nidal p. 117 ; m_lentes_2 p. 2 ; m_lentes_3 p. 2 ; m_lentes_4 p. 3) | tl_r1_bechers, tl_r2_rapide | Définition incomplète ; précipitation sans équation ; pas d'exemple acide-base |
| Transformation lente : H₂O₂ + I⁻, dismutation du thiosulfate, zinc + acide (Nidal p. 117-118 ; m_lentes_1 p. 2-3 ; m_lentes_2 p. 3 ; m_lentes_3 p. 2-3 ; m_lentes_4 p. 4) | tl_r3_lente, tl_r4_indices | Thiosulfate sans équation ni couples |
| Trois catégories rapide / lente / très lente (m_lentes_1 p. 2 ; m_lentes_4 p. 3-4) | tl_r5_echelle, tl_r6_classer | Présent |
| Techniques de suivi : manomètre, conductimétrie, pH-mètre (m_lentes_2 p. 3) | tl_r4_indices | pH-mètre absent (un seul prof) |
| Titrage, équivalence (m_lentes_4 p. 5-6) | tl_r7_titrage ; ch10 ci_m3_titrage, ci_m3b_calcul | Équivalence traitée en ch10 |
| Facteur cinétique : définition par la vitesse (Nidal p. 118 ; m_lentes_2 p. 4 ; m_lentes_3 p. 3 ; m_lentes_4 p. 6) | tl_f1_facteur | Chez nous « durée » seulement |
| Température : MnO₄⁻ + acide oxalique à 20 °C / 40 °C (Nidal p. 118-119 ; m_lentes_2 p. 4 ; m_lentes_4 p. 7) ; S₂O₈²⁻ + I⁻ (m_lentes_1 p. 5) | tl_r8_duree → tl_f4_courbes (H₂O₂ + I⁻) | Autre exemple, pas un manque |
| Concentration : I⁻ (Nidal p. 119 ; m_lentes_1 p. 4), thiosulfate et croix (m_lentes_2 p. 4-5), acide oxalique t_d (m_lentes_4 p. 6-7) | tl_f5_concentre → tl_f8_variable | Présent |
| Applications : autocuiseur, froid, chauffage, trempe, trempe + dilution, synthèses industrielles (m_lentes_1 p. 6 ; m_lentes_2 p. 5 ; m_lentes_3 p. 3-4 ; m_lentes_4 p. 8) | tl_t1_trempe, tl_t2_vie, tl_n2_glacee | Synthèses industrielles absentes |
| Catalyseur (cité : m_lentes_3 p. 3 ; m_lentes_4 p. 8) | tl_t3_catalyseur, tl_t4_courbes | Plus développé chez nous (choix déjà discuté dans l'audit du cadre) |
| Exercice type : couples, demi-équations, équation, tableau d'avancement, x_max, réactif limitant, n(I₂) final, C₂ plus grande, eau glacée (Nidal p. 120 ex. 1 ; m_lentes_3 p. 4-5, corrigé) ; Fe ou Zn + HCl, volume de H₂ (Nidal p. 120 ex. 2-3) | séances, compétences C1-C7, exercices de fin de diapo | Pas de tableau d'avancement ni de x_max calculé en ch9 |

#### Manques confirmés

| Priorité | Catégorie | Ce que disent les professeurs | Chez nous | Où l'ajouter |
|---|---|---|---|---|
| haute | Rédaction type / exercice | Identifier les deux couples Ox/Red à partir de l'équation ou des réactifs. Cadre p. 14 sur 29 : « Écrire l'équation … et identifier les deux couples intervenants » ; Nidal p. 120 ex. 1 Q1 ; m_lentes_1 p. 1 ; m_lentes_3 p. 4 Q1 ; m_lentes_4 p. 1 Q2 | Les couples sont toujours donnés dans l'énoncé ; aucune question ne les fait trouver | tl_x10_verifier (exercice : « S₂O₈²⁻(aq) + 2I⁻(aq) → 2SO₄²⁻(aq) + I₂(aq) : quels couples ? ») ; compétence C3 |
| haute | Définition | Rapide : « on ne peut pas suivre son évolution à l'œil nu **ni avec les appareils de mesure courants** du laboratoire ; on ne peut pas distinguer les **états intermédiaires** entre l'état initial et l'état final ». Lente : « on peut distinguer les états intermédiaires ». Nidal p. 117-118 ; m_lentes_2 p. 2-3 ; m_lentes_3 p. 2 (« à l'œil ou avec des instruments de mesure ») | tl_r2_rapide : « durée trop courte pour suivre son évolution à l'œil » (sans appareils, sans états intermédiaires) | tl_r2_rapide, tl_r3_lente (puce + cahier), tl_bl_fiche |
| haute | Définition / convention du cadre | Facteur cinétique : « paramètre capable de modifier la **vitesse** d'évolution d'une transformation » (Nidal p. 118 ; m_lentes_2 p. 4 ; m_lentes_4 p. 6) ; cadre p. 14 sur 29 : « influence des facteurs cinétiques sur la **vitesse** de réaction » | Écran et cahier : « paramètre qui modifie la durée » ; « vitesse d'évolution (la durée) » seulement dans l'attendu C5_r3 | tl_f1_facteur (« modifie la vitesse d'évolution, donc la durée »), tl_bl_fiche |
| haute | État physique dans les équations | Tous les profs écrivent (aq), (l), (s), (g) dans chaque équation et demi-équation (Nidal p. 115-119 ; m_lentes_2 p. 1-5 ; m_lentes_3 p. 1-4) ; règle 38 | Équations écrites sans état : tl_cr_carte cahier + student_trace « Zn + Cu²⁺(aq) → … » (Zn sans (s)) ; C3_r1 attendu « S₂O₈²⁻ + 2I⁻ → 2SO₄²⁻ + I₂ » ; C3_r4 attendu « Zn + Cu²⁺ → Zn²⁺ + Cu » ; C1_r3 attendu « Fe²⁺ ⇌ Fe³⁺ + e⁻ » ; tl_s1_b3 retrouver.attendu « MnO₄⁻ + 5Fe²⁺ + 8H⁺ → … + 4H₂O » ; C1_r2 et C1_r4 réponses « Zn ⇌ Zn²⁺ + 2e⁻ » ; tl_x9_oxalique réponses e0.0.1, e0.2.juste (« S₂O₈²⁻ + 2e⁻ ⇌ 2SO₄²⁻(aq) », états mélangés ; « 2I⁻ ⇌ I₂ + 2e⁻ »), e1.1.1, e1.2.2 ; textes alt des visuels tl_rp2, tl_x4, tl_x6_eau, tl_x7, tl_x8, tl_x10 | ids cités (ajouter les états partout) |
| moyenne | Tableau d'avancement / calcul | Exercice type du chapitre : n₀ = C·V de chaque réactif, tableau (état initial, intermédiaire, final), x_max pour chaque réactif (C₁V₁ − x_max = 0 ; C₂V₂ − 2x_max = 0), le plus petit → réactif limitant, n(I₂)_f = x_max ; puis C₂ plus grande : même n(I₂), donc même couleur. Nidal p. 120 ex. 1 Q4-6 et ex. 3 Q2 ; m_lentes_3 p. 4-5 ; cadre p. 14 sur 29 (« dresser le tableau d'avancement », sous-domaine 1.2) | tl_f7_palier affirme « I⁻ en excès, H₂O₂ limitant » sans calcul ; x_f, palier, réactif limitant utilisés sans tableau (déjà signalé « à trancher » dans l'audit du cadre). Le tableau est enseigné en ch10 | tl_f7_palier (exercice de fin de diapo avec volumes, n₀, x_max) ou rappel court avant tl_f7 |
| moyenne | Relation / méthode | Équation générale : (Ox₁ + n₁e⁻ ⇌ Red₁) × n₂ ; (Red₂ ⇌ Ox₂ + n₂e⁻) × n₁ ; n₂Ox₁ + n₁Red₂ → n₂Red₁ + n₁Ox₂. Nidal p. 115 ; m_lentes_2 p. 2 ; m_lentes_3 p. 1 ; m_lentes_4 p. 2 (a Red₁ + b Ox₂ = c Ox₁ + d Red₂) | Seulement des exemples (× 5, × 2 et × 5) | tl_x8_fer (puce « règle générale ») et tl_bl_fiche |
| moyenne | Exemples / état (s) | Équation d'une précipitation rapide : Cu²⁺(aq) + 2HO⁻(aq) → Cu(OH)₂(s) (Nidal p. 117 ; m_lentes_2 p. 2) ; Ag⁺(aq) + Cl⁻(aq) → AgCl(s) (m_lentes_2 p. 2 ; m_lentes_3 p. 2) | tl_r2_rapide, tl_r6_classer : « le chlorure d'argent AgCl » nommé, sans équation | tl_r2_rapide (puce + cahier) |
| moyenne | Exemple lent / équation | Dismutation du thiosulfate : couples S₂O₃²⁻(aq)/S(s) et SO₂(aq)/S₂O₃²⁻(aq), S₂O₃²⁻(aq) + 2H⁺(aq) → S(s) + SO₂(aq) + H₂O(l) ; mot « dismutation ». m_lentes_1 p. 3 ; m_lentes_2 p. 5 ; m_lentes_3 p. 2 | tl_r4_indices : « Ions thiosulfate S₂O₃²⁻ + acide : du soufre solide se forme » (pas d'équation, pas de couples) | tl_r4_indices |
| moyenne | État (g) / couple | Couple H⁺(aq)/H₂(g) : 2H⁺(aq) + 2e⁻ ⇌ H₂(g) ; métal + acide → H₂(g) (Nidal p. 115 Al, p. 120 ex. 2 Fe et ex. 3 Zn ; m_lentes_2 p. 3 « acide chlorhydrique avec le zinc » transformation lente) ; CO₂(g) (m_lentes_2 p. 4) | Aucune espèce (g) dans tout le cours (0 occurrence) | tl_x3b_couple (couple H⁺/H₂) ou tl_r3_lente (Zn(s) + 2H⁺(aq) → Zn²⁺(aq) + H₂(g)) |
| basse | Exemple | Réaction acide-base rapide : H₃O⁺(aq) + HO⁻(aq) → 2H₂O(l). m_lentes_2 p. 2 ; m_lentes_3 p. 2 ; m_lentes_4 p. 3 | Absent | tl_r2_rapide |
| basse | Vocabulaire | « réducteur conjugué », « espèces conjuguées ». Nidal p. 115 ; m_lentes_1 p. 2 ; m_lentes_2 p. 1-2 ; m_lentes_3 p. 1 ; m_lentes_4 p. 1-2 | Écran : « le réducteur qu'il devient » ; « conjugué » seulement dans une réponse de séance | tl_x3b_couple |
| basse | Applications | Accélérer en chauffant dans l'industrie : synthèse de l'ammoniac, synthèses organiques, esters. m_lentes_2 p. 5 ; m_lentes_3 p. 3 ; m_lentes_4 p. 8 | Seulement autocuiseur et réfrigérateur | tl_t2_vie |
| basse | Vocabulaire | Trempe : rendre le système « cinétiquement inerte ». m_lentes_3 p. 4 ; m_lentes_4 p. 4 et 8 | « bloquer la transformation » | tl_t1_trempe (facultatif) |

#### Manques chez un seul professeur

| Priorité | Catégorie | Ce que dit le professeur | Chez nous | Où l'ajouter |
|---|---|---|---|---|
| basse | Demi-équations | Cr₂O₇²⁻(aq) + 14H⁺(aq) + 6e⁻ ⇌ 2Cr³⁺(aq) + 7H₂O(l) ; O₂(aq) + 4H⁺(aq) + 4e⁻ ⇌ 2H₂O(l) (Nidal p. 116) | Le dichromate est dans la fiche `cadre_reference_2bac_pc.json` (formules TLR2) mais aucune diapo ne l'enseigne | tl_x6_eau (exercice) ou retirer de la fiche |
| basse | Suivi | pH-mètre pour suivre une transformation qui fait intervenir H₃O⁺ ou HO⁻ (m_lentes_2 p. 3) | conductimètre, manomètre seulement | tl_r4_indices |
| basse | Ordres de grandeur | Réfrigérateur ≈ 4 °C, congélateur ≈ −18 °C, autocuiseur ≈ 110 °C (m_lentes_3 p. 3) | « au-dessus de 100 °C » | tl_t2_vie |
| basse | Titrage | Réaction de titrage « rapide, totale et **unique** » (m_lentes_4 p. 5) | « rapide (et totale) » | tl_r7_titrage |
| — | Équivalence | Définition, changement de réactif limitant, n(I₂) = C₂V_E/2 (m_lentes_4 p. 5-6 ; cadre p. 14 sous-domaine 1.2) | Traité en ch10 (ci_m3_titrage, ci_m3b_calcul) | Rien à ajouter en ch9 |

#### Présent seulement à l'oral (à écrire)

- tl_f7_palier : « Une mole d'eau oxygénée donne une mole de diiode » (la raison de n(I₂) = n(H₂O₂)₀ : coefficients 1 et 1) n'est que dans la voix ; le cahier pose l'égalité sans « car ».
- tl_t1_trempe : « la trempe ralentit très fort, elle n'arrête pas tout : on dose vite ».
- tl_n2_glacee : « pas agiter : ce n'est pas un facteur du cours » (utile : Nidal p. 118 cite l'agitation).
- tl_x8_fer : le compte des charges « −1 + 10 + 8 = +17 ; +2 + 15 = +17 » est dit ; l'écran ne montre que « (charges +17 et +17) ».
- tl_f4_courbes : axes (n(I₂) en mmol, t en min) et paliers vers 30 min (20 °C) et 10 min (40 °C) dits ; l'écran n'a qu'une puce.
- tl_x10_verifier : la construction de H₂O₂ + 2I⁻ + 2H⁺ (deux demi-équations à 2 e⁻, addition) n'est que dans la voix ; l'écran montre seulement l'équation finale et les comptes.

#### Démonstrations qui sautent des étapes

- tl_f7_palier (exercice e0) et tl_s3_b1 : « I⁻ est en excès : H₂O₂ est le réactif limitant » est affirmé ; l'énoncé ne donne pas de volume, donc n(I⁻)₀ est inconnu. Manquent : n₀ de chaque réactif, x_max pour chacun (n(H₂O₂)₀ − x_max = 0 ; n(I⁻)₀ − 2x_max = 0), comparaison, puis « n(I₂)_f = x_max car coefficient 1 ».
- tl_x7_equation (question), tl_x9_oxalique exercices e0 et e1, tl_s1_b3 : on passe de « 2 électrons captés, 2 cédés » à l'équation finale sans la ligne d'addition (électrons qui s'annulent) ni la ligne de vérification des charges (−4 et −4 ; +2 et +2), alors que tl_x10_verifier dit « toujours vérifier ».
- tl_x6_eau exercices e0 (S₂O₈²⁻/SO₄²⁻) et e1 (CO₂/H₂C₂O₄), tl_s1_b2 : « charges : −2 et −4 : 2e⁻ à gauche » sans le « car » (pour passer de −2 à −4, du côté de l'oxydant) ni la ligne finale de vérification (−2 − 2 = −4 ; +2 − 2 = 0).
- tl_rp4_concentration et tl_s1_b4 : la substitution est écrite sans unités (« 0,02 / 0,5 », « 0,1 × 0,2 ») ; écrire « 0,02 mol / 0,5 L ».

#### Différences de notation ou de convention

| Point | Nous | Eux | Laquelle garder |
|---|---|---|---|
| Demi-équation | ⇌ | ⇌ (Nidal, m_lentes_2, m_lentes_3) ; → (m_lentes_1 p. 1) ; = (m_lentes_4) | ⇌ (cadre p. 23 sur 29) |
| Équation de réaction | → | → (Nidal p. 117-119, m_lentes_2, m_lentes_3) ; ⇌ (Nidal p. 115, Al) ; = (m_lentes_4, manuel français) | → |
| tl_rp1_ion, centre | « Cu(s) → Cu²⁺(aq) + 2e⁻ ; I(aq) + e⁻ → I⁻(aq) » | demi-équations avec ⇌ ; I₂(aq) + 2e⁻ ⇌ 2I⁻(aq) | Un atome I isolé n'est pas (aq) : écrire « I + e⁻ → I⁻ » sans état (échelle de l'atome) ou passer au couple I₂/I⁻ |
| CO₂ | CO₂(aq) | CO₂(aq) (Nidal équation p. 119, m_lentes_4) ; CO₂(g) (m_lentes_2 p. 4, Nidal couple p. 118) | (aq), mais rester cohérent dans tout le cours |
| Durée d'une transformation lente | tl_r3_lente : « quelques secondes à plusieurs minutes (ou plus) » ; tl_r5_echelle et tl_bl_fiche : « secondes à heures » | « quelques secondes à plusieurs heures » (Nidal p. 118 ; m_lentes_2 p. 3) ; « plusieurs minutes » (m_lentes_1 p. 2) | « quelques secondes à plusieurs heures » partout |
| Facteur cinétique | « modifie la durée » | « modifie la vitesse d'évolution » (3 profs + cadre) ; « durée » (m_lentes_3) | « vitesse d'évolution, donc durée » |
| Agitation | « pas un facteur du cours » (voix tl_n2_glacee) | facteur cinétique (Nidal p. 118) | Nous (absente du cadre) |
| Ion hydrogène | H⁺(aq) (« même ion que H₃O⁺ ») | H⁺(aq) en oxydoréduction ; H₃O⁺(aq) en acide-base | Nous |

#### Hors cadre chez les professeurs (ne pas ajouter)

- Autres facteurs cinétiques : lumière / éclairement, nature du solvant (m_lentes_3 p. 3 ; m_lentes_4 p. 8), agitation (Nidal p. 118) : le cadre p. 23 sur 29 ne cite que « température et concentration des réactifs ».
- Titrage conductimétrique repéré par G = f(V_versé) (m_lentes_4 p. 5) : le cadre PC demande le dosage par pH-mètre.
- Systèmes « stables » sans réaction spontanée, ocres (m_lentes_4 p. 5) ; réactions de Maillard (m_lentes_4 p. 8).
- Notation « = » dans les équations (m_lentes_4, programme français).
- Demi-équation « ⇌ » dans une équation-bilan (Nidal p. 115) : contraire à la convention → du cours.

### Suivi temporel d’une transformation chimique – vitesse de réaction

Version auditée : `backend/data/courses/en_attente/phys_ch10_cinetique.json` (écran, cahier des diapos et des séances, voix, questions, démonstrations `lignes`, exercices, rappels, réactions ; texte de `nos-cours/phys_ch10_cinetique.txt`).

Sources lues (toutes lues en image) :
- **Nidal** (Pr Nidal Naceiri Mrabti, cours 2 PC BIOF, `web/phys/nidal_p1.pdf`) : p. 124-135. Pas de décalage : la page « Page 124 » est la page 124 du PDF. Les p. 134-135 sont des feuilles quadrillées vides.
- **M1** (`m_suivi_1.pdf`, Pr Mahajar et Pr Tabit, 2 Bac Sciences) : p. 1-7.
- **M2** (`m_suivi_2.pdf`, scan d’un manuel « TS ») : p. 1-16. Les p. 1-8 sont « Chimie 3 : Suivi temporel », les p. 9-16 « Chimie 4 : Vitesse ». Les pages citées sont celles du PDF.
- **M3** (`m_suivi_3.pdf`, Pr Sbiro) : p. 1-5.
- **Cadre** (PDF officiel 2015, scan) : p. 16 (savoir-faire, « 14 sur 29 ») et p. 25 (programme, « 23 sur 29 »). J’ai aussi lu `cadre_reference_2bac_pc.json` (clé `chapitres.cinetique`, CIN1-CIN9) et `docs/audit-programme-officiel/chimie.md`. `experience_profs.json` n’a pas de clé `cinetique`.

#### Plan comparé
| Partie chez les professeurs | Où chez nous | Remarque |
|---|---|---|
| Méthodes physiques / chimiques ; liste des méthodes (Nidal p. 126 ; M1 p. 1 ; M3 p. 1 ; M2 p. 6) | ci_o2_methodes, ci_p5_choisir, ci_h4_comparer | Trois méthodes, mais pas le classement « physiques / chimiques » ni leurs avantages. |
| Dosage : montage, empois, trempe (« plongée »), couples, tableau, n(I₂) = x (Nidal p. 127-128 ; M1 p. 1-3 ; M3 p. 1-2 ; M2 p. 1-4) | ci_m1 → ci_a7 | Pas de couples ni de demi-équations ; la trempe ne cite que le froid ; l’équivalence n’est pas définie par les proportions. |
| Conductimétrie : RCl + eau, étalonnage, σ = Σλ[X], **on établit σ(x)** (Nidal p. 128-129 ; M1 p. 5-6 ; M3 p. 3-4 ; M2 p. 5-6) | ci_g1 → ci_g6, ci_r2 | σ(x) est donné sans démonstration ; l’exemple B n’a ni tableau, ni V, ni n₀. |
| Pression : P = P_atm + P(H₂), x = x_max·ΔP/ΔP_max (Nidal p. 130-131 ; M1 p. 4-5 ; M3 p. 2-3) | ci_p1, ci_z6, ci_p2, ci_p3 | Nous avons x = (P − P₀)·V/(RT) ; il manque la justification et la forme avec le rapport. |
| Vitesse volumique : définition en mots, unité SI, tangente, angle α (Nidal p. 125 ; M1 p. 6-7 ; M3 p. 5 ; M2 p. 11-12) | ci_v1 → ci_v4, ci_r1 | La définition en mots et l’unité SI manquent. |
| Vitesse lue sur une courbe n(X)(t) ou [X](t) (Nidal p. 128, p. 133 ; M2 p. 12) | — | **Absent.** |
| Évolution de v ; facteurs température **et concentration initiale** ; chocs efficaces (Nidal p. 132 ; M3 p. 5 ; M2 p. 12-16) | ci_v5 → ci_v8, cahier séance 4 | Il manque l’influence de la concentration initiale (C₁ > C₂ ⇒ v₀,₁ > v₀,₂). |
| t₁/₂ : définition, lecture, remarques (durée de la transformation, intervalle entre deux mesures ≪ t₁/₂) (Nidal p. 125-126 ; M1 p. 7 ; M3 p. 5 ; M2 p. 13-14) | ci_h1 → ci_h4 | Les deux remarques manquent. |
| Exercices types (Nidal p. 133 ; M2 p. 4, p. 8) | ci_n1 → ci_n8 (10 sujets du national), ci_r1, ci_r2 | Nous en avons plus qu’eux. Il manque le cas σ croissante à partir de 0 et la vitesse à partir de [X](t). |

#### Manques confirmés
| Priorité | Catégorie | Ce que disent les professeurs | Chez nous | Où l’ajouter |
|---|---|---|---|---|
| haute | démonstration σ(x) | Établir σ en fonction de x : σ = Σλᵢ[Xᵢ], puis [X] = n/V tiré du tableau d’avancement, puis σ_f, puis le rapport (Nidal p. 128 Q4 et p. 129 ; M1 p. 6 ; M3 p. 4 ; M2 p. 5-6). C’est exigé par le cadre p. 16 (exploiter la conductivité) et par CIN3, et le national 2021 N demande « montrer que σ = … ». | ci_g5_droite donne σ = σ₀ − (λ(HO⁻) − λ(CH₃COO⁻))·x/V sans l’établir. L’exemple B n’a pas de tableau d’avancement. V, n₀(HO⁻) et « ester en excès » ne sont écrits nulle part, et x_max = 1,0 mmol apparaît sans calcul. | ci_g4_descend (tableau et données de B) ; ci_g5_droite (démonstration complète) |
| haute | méthode / relation | Calculer la vitesse à partir de la courbe d’une espèce : v = (1/V)·dn(I₂)/dt (Nidal p. 128) ; v = d[I₂]/dt, car x = [I₂]·V et V est constant (M2 p. 12) ; [Zn²⁺](t) → v à 400 s (Nidal p. 133 Ex. 2). Pour un réactif, il faut mettre un signe −. C’est exigé par le cadre p. 16 (exploiter les courbes de quantité de matière et de concentration). | Nous calculons v seulement à partir de x(t) et de σ(t) (2021 N). Aucune relation v = d[X]/dt ou v = −(1/V)·dn(R)/dt. | nouvelle diapo après ci_v4_bareme (puis un exercice dans ci_n4_reactif) |
| haute | couples et demi-équations | Les deux couples Ox/Red et leurs demi-équations avec ⇌, avant l’équation-bilan : H₂O₂(aq)/H₂O(l) et I₂(aq)/I⁻(aq) ; S₂O₈²⁻(aq)/SO₄²⁻(aq) ; S₄O₆²⁻(aq)/S₂O₃²⁻(aq) ; Mg²⁺(aq)/Mg(s) et H⁺(aq)/H₂(g) (Nidal p. 127, p. 130 ; M1 p. 1-4 ; M3 p. 1, p. 3 ; M2 p. 9). C’est au cadre p. 16 et p. 25 : écrire l’équation et identifier les couples, avec ⇌ dans la demi-équation. | Aucun « couple » ni demi-équation dans le chapitre (0 occurrence de ⇌). Les équations sont données toutes faites. | ci_z4_equation (exemple A) ; ci_m3b_calcul (titrage) ; ci_p1_ballon (exemple C) |
| haute | définition et démonstration de l’équivalence | À l’équivalence, les réactifs sont dans les proportions stœchiométriques : n(I₂)/1 = n_E(S₂O₃²⁻)/2 avec n_E = C·V_E (M3 p. 1 ; M2 p. 1 ; M1 p. 3, tableau du dosage avec x_E). C’est au cadre p. 16 : « repérer l’équivalence et l’exploiter ». | ci_m3_titrage dit seulement « tout le diiode a réagi ». ci_m3b_calcul écrit directement n(I₂) = C·V_E/2, et l’écran saute l’application numérique (0,020 × 12,6·10⁻³/2 = 1,26·10⁻⁴ mol, puis × 10). | ci_m3_titrage, ci_m3b_calcul |
| moyenne | définition et unité | En mots : « quantité de matière formée ou consommée par unité de temps et de volume ». Unité SI : mol·m⁻³·s⁻¹, avec V en m³ et dx/dt en mol·s⁻¹ (Nidal p. 125 ; M1 p. 6 ; M3 p. 5). | ci_v2_definition : seulement la formule et mol·L⁻¹·min⁻¹. L’unité SI n’est jamais donnée. | ci_v2_definition |
| moyenne | facteur cinétique | Concentration initiale des réactifs : C₁ > C₂ ⇒ v₀,₁ > v₀,₂, avec les deux courbes x(t) et les tangentes à l’origine (Nidal p. 132 ; M3 p. 5 ; M2 p. 13, p. 15). Allure de la courbe quand C_A diminue (Nidal p. 133 Q6). C’est au cadre p. 16 (concentration et température) et CIN6. | Seule la température a sa diapo (ci_v8). La concentration initiale n’apparaît que dans un vrai/faux de fin (ci_v8 e1) ; ci_v6 parle de la concentration qui baisse pendant la réaction. | ci_v8_temperature (ajouter la 2e courbe) ou nouvelle diapo |
| moyenne | justification de la trempe | La trempe arrête la réaction par **dilution et refroidissement** : deux facteurs cinétiques, la concentration et la température (Nidal p. 127 ; M1 p. 2 ; M2 p. 2). Le cadre p. 16 demande de « justifier les opérations du suivi ». | ci_m2_trempe et ci_n8_trempe : « le refroidissement brusque bloque la réaction », sans la dilution. | ci_m2_trempe, ci_bl_fiche |
| moyenne | démonstration (pression) | P = P_atm + P(H₂), car l’air ne change pas (V et T constants) ; P(H₂)·V = x·R·T ; à la fin ΔP_max = x_max·RT/V ; d’où x = x_max·(P − P_atm)/(P_max − P_atm) (Nidal p. 131 ; M1 p. 4 ; M3 p. 3). | ci_p2_relation écrit (P − P₀)·V = n(H₂)·R·T sans dire pourquoi P − P₀ est la pression du seul H₂. La forme x = x_max·ΔP/ΔP_max manque. | ci_p2_relation |
| moyenne | exercice type | σ croissante à partir de σ₀ ≈ 0 (réaction de RCl avec l’eau, qui forme H⁺ et Cl⁻) : x = x_max·σ/σ_f (σ_max chez eux) (Nidal p. 128-129 ; M1 p. 5-6 ; M3 p. 3-4 ; M2 p. 5-6). | Un seul cas, σ qui décroît (exemple B). La formule générale le couvre, mais aucun exemple ni exercice ne le montre. | ci_g6_calcul (exercice) |
| moyenne | condition de la méthode | L’intervalle entre deux mesures (ou le temps de réponse) doit être très inférieur à t₁/₂ (Nidal p. 126 ; M1 p. 7 ; M2 p. 14). C’est au cadre p. 25 : « choix d’une méthode de suivi selon t₁/₂ ». | ci_h4_comparer : « t₁/₂ court → mesure en continu », sans ce critère. | ci_h4_comparer |
| moyenne | relation | Quantité de matière d’un liquide : n = ρ·V/M (Nidal p. 129 ; M3 p. 4). | Seulement n = m/M (ci_z1_mole). Aucun ρ dans le cours. | ci_z1_mole |
| basse | méthodes | Méthodes physiques (continues, rapides, peu de réactif, non destructives) et méthode chimique, le dosage, qui demande des prélèvements (Nidal p. 126 et p. 133 Ex. 1 ; M1 p. 1 ; M2 p. 6). | Les trois méthodes y sont, mais pas ce classement. | ci_o2_methodes ou ci_p5_choisir |
| basse | ordre de grandeur | La transformation est pratiquement finie après quelques t₁/₂ : environ 10 t₁/₂ chez Nidal p. 126 et M1 p. 7, environ 7 t₁/₂ chez M2 p. 14. On le dit comme un ordre de grandeur, pas comme une loi. | ci_h3_pieges dit seulement qu’à 2·t₁/₂ ce n’est pas fini. | ci_h3_pieges |
| basse | montage | Montage du titrage (burette, erlenmeyer, agitateur magnétique) et empois d’amidon : l’équivalence est repérée quand la couleur bleue disparaît (Nidal p. 127 ; M1 p. 2 ; M2 p. 1). | Ces mots sont seulement dans la voix et dans l’`alt` ; l’équivalence est repérée par « brun → incolore ». | ci_m3_titrage |
| basse | montage | Étalonnage du conductimètre avant les mesures (Nidal p. 128 ; M1 p. 5 ; M2 p. 5). | Absent. | ci_g1_cellule |
| basse | rédaction type | « La conductimétrie convient quand la conductivité des produits et celle des réactifs sont très différentes » ; « le suivi est continu » (Nidal p. 129 ; M1 p. 6). | ci_g2_ions : « si les ions changent, σ change ». | ci_p5_choisir |

#### Manques chez un seul professeur
| Priorité | Catégorie | Ce que dit le professeur | Chez nous | Où l’ajouter |
|---|---|---|---|---|
| basse | tableau | Tableau d’avancement de la réaction de dosage (M1 p. 3). | Seulement la relation n(I₂) = C·V_E/2. | ci_m3b_calcul |
| basse | notation | V dans PV = nRT est le volume occupé par le gaz V_g, différent du volume de solution V_A (Nidal p. 130-131). | ci_p2_relation : « V = 1,0 L » sans dire de quel volume il s’agit. | ci_p2_relation |
| basse | méthode | x_f se lit sur l’asymptote horizontale de la courbe (M1 p. 7). | Nous disons « palier » (ci_a7), ce qui suffit. | — |
| basse | exercice | Vrai/faux de cours, par exemple « le titrage est une méthode non destructive » (Nidal p. 133 Ex. 1). | — | ci_p5_choisir (exercice) |

#### Présent seulement à l’oral (à écrire)
- ci_a1b_en_cours : la définition de l’avancement (« le nombre de fois que la recette de l’équation a été faite, en mmol ») n’est que dans la voix.
- ci_g5_droite : la raison pour laquelle σ(x) est une droite (« chaque mmol de HO⁻ consommée fait baisser σ de la même quantité ») n’est que dans la voix.
- ci_a2_limitant : la rédaction par hypothèses (« Hypothèse 1 : si H₂O₂ est limitant… ») est dite. L’écrit donne seulement les égalités, sans « Si … est le réactif limitant ». Nidal l’écrit p. 131.
- ci_n8_trempe : la consigne « écris bloquer la réaction, pas seulement refroidir » n’est que dans la voix.
- ci_m3_titrage : burette et prélèvement : seulement dans la voix et dans l’`alt` (voir le manque « montage »).

#### Démonstrations qui sautent des étapes
- **ci_g5_droite** (et ci_g4_descend) : il manque tout le chemin. Tableau de B (ester en excès ; n₀(HO⁻) = [HO⁻]₀·V = 10 mol/m³ × V, avec V jamais donné). Puis σ = λ(Na⁺)[Na⁺] + λ(HO⁻)[HO⁻] + λ(CH₃COO⁻)[CH₃COO⁻], avec [HO⁻] = (n₀ − x)/V, [CH₃COO⁻] = x/V et [Na⁺] = n₀/V. Puis le regroupement en σ₀ − (λ(HO⁻) − λ(CH₃COO⁻))·x/V. Puis σ_f pour x = x_max (0,0501 + 0,0409 = 0,091 S/m). Enfin le rapport (σ₀ − σ)/(σ₀ − σ_f) = x/x_max.
- **ci_m3b_calcul** : il manque la ligne n_E(S₂O₃²⁻) = C·V_E, puis n(I₂)/1 = n_E(S₂O₃²⁻)/2. L’écran passe de 10 × C·V_E/2 à 1,26 mmol sans l’application numérique. La démonstration de l’exercice, elle, la donne.
- **ci_p2_relation** : il manque P = P_air + P(H₂), avec P_air = P₀ constante. La relation (P − P₀)·V = n(H₂)·R·T est posée sans justification.
- **ci_n6_sigma** (2021 N) : il manque la ligne dx/dt = −(1/160)·dσ/dt avant la substitution. Le calcul de v₁ n’a pas de démonstration : il faut écrire −(1/(160 × 10⁻⁴)) × (−0,0125), puis 160 × 10⁻⁴ = 1,6·10⁻², puis 0,0125/1,6·10⁻² = 0,78 mol·m⁻³·min⁻¹. La démonstration de σ₁/₂ écrit x_f = 10⁻³ mol sans dire « HO⁻ limitant (ester en excès), transformation totale : x_f = x_max = n₀(HO⁻) ».
- **ci_p4_2016R** : on « isole σ » sans l’écrire. Il faut σ = (1,57·10⁻³ − x)/6,3·10⁻³, puis 1,07·10⁻³/6,3·10⁻³ = 0,170 S·m⁻¹. Aucune démonstration (ci_n7 le fait pour G).
- **ci_r1_litres** (exercice de fin, 2016 R) : il manque 100 mL = 10⁻⁴ m³ et la ligne 5,25·10⁻⁵/10⁻⁴ = 5,25·10⁻¹ avant le résultat 0,525.
- **ci_v6_epuisement** : [H₂O₂]₀ = 20 mmol/L est donné sans le calcul 2,0 mmol / 0,100 L. C’est mineur.
- Vérifiées et justes : ci_a1b, ci_a2, ci_a6, ci_g3, ci_g6, ci_v3, ci_v4, ci_n1, ci_n2, ci_n4, ci_n7, ci_n8. Les valeurs recalculées sont exactes : 1,26·10⁻³ mol, σ_f = 0,091 S/m, 0,170 S·m⁻¹, 0,78 mol·m⁻³·min⁻¹.
- États physiques : toutes les équations écrites ont leurs états, (aq), (l), (s), (g), dans l’écran, le cahier, les questions et les démonstrations. Aucun oubli trouvé.

#### Différences de notation ou de convention
| Nous | Eux | À garder |
|---|---|---|
| Dernière ligne du tableau « État final : x_max » (ci_a1b) | x_f (M1 p. 2, M2 p. 5), x_m (Nidal) | « État final : x_f », avec x_f = x_max si la transformation est totale. Ainsi ch11 (x_f < x_max) ne contredit pas ch10. |
| σ_f | σ_max (M1 p. 6, M3 p. 4), σ_f (Nidal) | σ_f, en citant σ_max dans un exercice. |
| P₀ | P_atm, ΔP, ΔP_max (M1, M3) ; P_maxH₂ (Nidal) | P₀, en écrivant une fois « P₀ = P_atm » et ΔP_max. |
| « trempe » | « plongée » (Nidal p. 127, M1 p. 2) ; « trempe » (M2) | Trempe (mot du national 2017 R), en citant « plongée ». |
| v en mol·L⁻¹·min⁻¹, V en L | V en m³, unité SI mol·m⁻³·s⁻¹ (Nidal, M1, M3) | Garder les deux : SI dans la définition, mol·L⁻¹ dans les applications (déjà dans ci_r1). |
| L’évolution de v montrée par des triangles Δx/Δt (ci_v1) | l’angle α de la tangente diminue, tan α = dx/dt (Nidal p. 125, M1 p. 7) | Les nôtres, plus une phrase sur l’angle de la tangente. |
| H⁺(aq) | H₃O⁺(aq) (Nidal p. 130, M1 p. 4) | H⁺(aq) en ch10 ; H₃O⁺ arrive en ch11. |
| Équivalence brun → incolore | bleu → incolore avec l’empois | Garder la nôtre et ajouter l’empois. |

#### Hors cadre chez les professeurs (ne pas ajouter)
- Spectrophotométrie, absorbance, loi de Beer-Lambert, courbe d’étalonnage A = f(C) (M2 p. 6-9 ; cités dans les listes de Nidal p. 126 et M1 p. 1). C’est retiré exprès (chimie.md, `hors_cadre.mots`).
- pH-métrie comme méthode de suivi (Nidal p. 126, p. 130 Q2 ; M1 p. 1 ; M3 p. 1) : le pH appartient au chapitre suivant (ch11).
- Surface de contact d’un réactif solide, agitation (M2 p. 15-16) : le cadre ne retient que la température et la concentration.
- Détail de l’efficacité des chocs (orientation, énergie, rupture de liaisons) et leur caractère aléatoire, qui mène à la réaction inverse et à l’équilibre (M2 p. 16) : c’est pour ch11. Il faut aussi éviter le vocabulaire « collisions / risques de collisions » (M3 p. 5).
- Utilisation d’un tableur (M1 p. 7) ; comparaison avec la demi-vie radioactive (M2 p. 13).
- Toute loi « à 2·t₁/₂, x = 3/4·x_f » : aucun professeur ne l’écrit, et elle reste interdite.

### Transformations chimiques s’effectuant dans les deux sens

Sources lues :
- Notre cours : `backend/data/courses/en_attente/phys_ch11_transformations_deux_sens.json` (version en attente), tous les champs écrits (écran, cahier, centre, questions, réactions, démonstrations), en plus du texte `nos-cours/phys_ch11_transformations_deux_sens.txt`.
- Pr Nidal Naceiri Mrabti, cours 2 PC BIOF, `web/phys/nidal_p1.pdf`, **pp. 137-148** (pas de décalage : la page imprimée = la page du PDF), toutes lues en image. Les pp. 146-148 sont des pages quadrillées vides. Abrégé **N**.
- Pr Hicham Mahajar et Pr Youssef Tabit (moutamadris), `web/chim/m_deuxsens_1.pdf`, **pp. 1-5**, lues en image. Abrégé **M1**.
- Professeur non nommé (moutamadris), `web/chim/m_deuxsens_2.pdf`, **pp. 1-4**, lues en image (dans le .txt, les formules sont des images et ont disparu). Abrégé **M2**.
- Pr Zakaryae Chriki, résumé, `web/chim/m_deuxsens_r.pdf`, **p. 1** lue en image. La p. 2 (quotient de réaction, K) appartient au chapitre suivant ; lue dans le texte seulement. Abrégé **R**.
- Cadre officiel : PDF CNEEO 2015, **p. 14/29** (sous-domaine 2.1) et **p. 15/29** (2.2 et 2.3, pour savoir ce qui est hors chapitre), lues en image ; fiche `cadre_reference_2bac_pc.json` (clé `transformations_deux_sens`, TD1-TD8, `hors_cadre`) ; `docs/audit-programme-officiel/chimie.md` § ch11 ; SKILL cours-concentration § Chimie. `experience_profs.json` n’a pas de clé `transformations_deux_sens` (il n’y a que `ondes_mecaniques`).

#### Plan comparé

| Partie chez les professeurs | Où chez nous | Remarque |
|---|---|---|
| Acide et base selon Brønsted, couple, demi-équation (N p138, M1 p1, M2 p1, R p1) | td_b1_acide, td_b2_base, td_b3_couple | Présent. Le mot « ampholyte » n’est pas défini (voir manques). |
| L’eau ampholyte, HCO₃⁻ (N p138, M1 p1, M2 p1) | td_b3b_eau | L’idée y est, le mot non. |
| Réaction acido-basique HA₁ + A₂⁻ → A₁⁻ + HA₂ (N p138, M1 p1, M2 p1, R p1) | td_b4_reaction | Présent, avec les états. |
| Solution aqueuse (soluté, solvant), équations de dissolution (N p139, M1 p1) | td_z2_concentration (rappel C = n/V seulement) | Pas de définition (voir manques). |
| pH = −log[H₃O⁺], validité [H₃O⁺] ≤ 5·10⁻² mol/L, [H₃O⁺] = 10^(−pH) (N p139, M1 p2, R p1) | td_p1_ph, td_p2_calcul | La limite chiffrée manque, on dit seulement « diluée ». |
| Échelle de pH de 0 à 14, axe [H₃O⁺] (N p139, M1 p2) | — | Absente. |
| Propriétés du log (M1 p2, M2 p1) | td_z3_puissance (log(10ⁿ) = n seulement) | Partiel. |
| Mesure du pH : papier pH, pH-mètre (sonde/électrode + voltmètre), étalonnage (N p140, M1 p2, M2 p1-2) | td_p3_phmetre | Étalonnage présent ; ni papier pH ni constitution du pH-mètre. |
| Transformation totale : activité HCl, tableau, x_max = x_f, définition (N p140-141, M1 p2-3) | td_a5_totale | Présent comme exemple B ; la définition écrite manque. |
| Transformation limitée : 1 mL d’acide éthanoïque pur dans 500 mL, n₀ par la densité, x_f < x_max, définition (N p141-142, M1 p3-4, M2 p2-3) | td_p6_totale, td_a1 à td_a4 | Notre acide est donné par C (pas de calcul de n₀ par la densité) ; la définition par x_f < x_max manque à l’écran. |
| τ = x_f/x_max, 0 ≤ τ ≤ 1, en % ; τ = 1 totale, τ < 1 limitée (N p142, M1 p4, M2 p2, R p1) | td_a4_taux, td_a6_relation | Présent ; en plus chez nous : τ = 10^(−pH)/C. |
| Deux sens : bécher A (+ acide pur, pH baisse : sens direct), bécher B (+ éthanoate de sodium, pH monte : sens indirect) (N p143, M1 p4-5) | td_e1_inverse, td_e2_fleche | Seul le sens inverse est montré par l’expérience ; « sens 1 / sens 2 » au lieu de « sens direct / indirect ». |
| Écriture générale aA + bB ⇌ cC + dD (N p143, M1 p5) | — | Absente (on a seulement AH + H₂O ⇌ A⁻ + H₃O⁺). |
| État d’équilibre (définition), équilibre dynamique (N p144, M1 p5, M2 p3, R p1) | td_e3_etat, td_e4_dynamique | Présent. |
| Interprétation microscopique : v₁ baisse, v₂ monte, jusqu’à v₁ = v₂ (N p144, M2 p3) ; chocs efficaces (M1 p5, R p1) | td_e4_dynamique | Les chocs efficaces y sont (écran, pas le cahier) ; l’évolution de v₁ et v₂ manque. |
| Conductimétrie : σ en fonction de x_f et V, x_f, concentrations, pH, τ (N p145 ex. 1-2, M2 p3-4) | td_c1 à td_c3, td_n2_conductivite | On passe par [H₃O⁺], jamais par σ = (λ₁ + λ₂)·x_f/V ; le pH n’est jamais calculé à partir de σ. |
| Influence de la concentration sur τ (N p145 ex. 2 q7) | td_d1 à td_d3 | Présent (et en plus : nature de l’acide). |
| — | td_e5, td_e6, td_n1 à td_n4 | Chez nous seulement : sujets du national (estérification, 2017 N, 2021 R, 2019 N, 2023 N, 2024 R). |

#### Manques confirmés

| Priorité | Catégorie | Ce que disent les professeurs | Chez nous | Où l’ajouter |
|---|---|---|---|---|
| haute | Définition + critère | Totale : « l’évolution s’arrête par la disparition totale d’au moins un réactif ; x_f = x_max ». Limitée : « s’arrête sans disparition totale de tout réactif ; x_f < x_max » (N p141-142, M1 p3-4, M2 p2-3). Cadre p14 : « calculer x_f … et le comparer à x_max ». | Seul « τ = 1 : totale ; τ < 1 : limitée » est écrit (td_a4_taux). « x_f < x_max » n’apparaît que dans des réactions de td_a3_xf. | td_a3_xf (critère x_f < x_max) et td_a4_taux (les deux définitions) |
| haute | Notation du bac | « Sens direct » et « sens indirect » (ou « sens inverse ») de l’équation (N p143, M1 p4-5, R p1). | « sens 1 / sens 2 » partout ; « sens direct » : 0 occurrence. | td_e1_inverse, td_e2_fleche, td_e4_dynamique (écrire « sens direct (1) / sens inverse (2) ») |
| haute | Relation + démonstration | Exprimer σ en fonction de x_f (ou x_éq) et V : σ = (λ(H₃O⁺) + λ(A⁻))·x_f/V, d’où x_f = σ·V/(λ₁ + λ₂) (N p145 ex. 1 q2 et ex. 2 q5a, M2 p4 q2-3). | On écrit seulement σ = (λ₁ + λ₂)·[H₃O⁺] et τ = σ/(C·(λ₁ + λ₂)) ; « x_f/V » n’apparaît qu’en td_n3, pour [CH₃COO⁻]. | td_c2_relation (une ligne de plus : [H₃O⁺] = [A⁻] = x_f/V) |
| moyenne | Expérience / méthode | Bécher A : on ajoute de l’acide éthanoïque pur, le pH baisse, [H₃O⁺] augmente : le système évolue dans le sens direct (N p143, M1 p4). | Seul le sens inverse est montré (exemple E, td_e1_inverse). | td_e1_inverse (2ᵉ bécher) ou nouvelle diapo avant td_e2_fleche |
| moyenne | Interprétation microscopique | Au départ, seule la réaction 1 a lieu (vitesse v₁) ; A et B diminuent, donc v₁ diminue ; C et D apparaissent, donc v₂ augmente ; quand v₁ = v₂, le système n’évolue plus (N p144, M2 p3). Cadre p14 : « interpréter à l’échelle microscopique l’état d’équilibre ». | Seulement « les deux réactions continuent, à la même vitesse » et les chocs efficaces ; aucune évolution de v₁ et v₂. | td_e4_dynamique |
| moyenne | Condition d’une définition | pH = −log[H₃O⁺] valable pour des solutions diluées : [H₃O⁺] ≤ 5·10⁻² mol·L⁻¹ ; [H₃O⁺] est la valeur numérique en mol·L⁻¹ (N p139, M1 p2, R p1). | « solution aqueuse diluée », sans la limite chiffrée. | td_p1_ph (écran + cahier) |
| moyenne | Vocabulaire | Ampholyte : espèce qui est l’acide d’un couple et la base d’un autre ; l’eau est un ampholyte (N p138, M1 p1, M2 p1). | td_b3b_eau décrit les deux rôles de l’eau sans le mot. Le mot n’apparaît que dans les réactions de td_b3_couple et td_p5_ammoniac. | td_b3b_eau |
| moyenne | Calcul type (exercice) | n₀ = m/M = ρ·V/M = d·ρ_eau·V/M (1 mL d’acide éthanoïque pur, d = 1,05, M = 60 g/mol : n₀ = 1,75·10⁻² mol) (N p141, M1 p3, M2 p2). | Aucune densité ni masse volumique (0 occurrence) : n₀ vient toujours de C·V. | rappel près de td_a1_tableau, ou exercice de fin de td_a2_xmax |
| moyenne | Matériel / montage | pH-mètre : une sonde (électrode de verre + électrode de référence, ou électrode combinée) reliée à un voltmètre électronique gradué en pH (N p140, M1 p2, M2 p1). | Sonde, étalonnage et lecture seulement ; « électrode » et « voltmètre » : 0 occurrence. | td_p3_phmetre |
| basse | Matériel | Papier pH : une indication rapide du pH par sa couleur, moins précise que le pH-mètre (N p140, M1 p2). | Absent. | td_p3_phmetre |
| basse | Ordre de grandeur | Le pH va en pratique de 0 à 14 ; axe pH / [H₃O⁺] de 1 à 10⁻¹⁴ mol/L (N p139, M1 p2). | Absent (td_n1 dit seulement « pH de 0 à 7 » pour la figure). | td_p1_ph |
| basse | Calcul type | Calculer le pH à partir de σ : x_f, puis [H₃O⁺]_f = x_f/V, puis pH = −log[H₃O⁺] (N p145 ex. 2 q5b, M2 p4 q5). | De σ, on va seulement à [H₃O⁺] puis à τ (td_c3_calcul). | exercice de fin de td_c3_calcul |
| basse | Écriture générale | Une transformation limitée s’écrit aA + bB ⇌ cC + dD (N p143-144, M1 p5). | Seulement AH(aq) + H₂O(l) ⇌ A⁻(aq) + H₃O⁺(aq). | td_e2_fleche (cahier) |
| basse | Définition | Solution aqueuse = mélange homogène obtenu en dissolvant un soluté dans l’eau (solvant) (N p139, M1 p1, avec NaCl(s) → Na⁺(aq) + Cl⁻(aq) et HCl(g) → H⁺(aq) + Cl⁻(aq)). | Absente (td_z2 utilise « soluté » sans définir la solution aqueuse). | td_z2_concentration |
| basse | Outil | log(ab) = log a + log b ; log(a/b) = log a − log b ; log 1 = 0 ; log 10 = 1 ; log y = x ⇔ y = 10ˣ (M1 p2, M2 p1). | Seulement log(10ⁿ) = n. | td_z3_puissance |

**États physiques dans les équations écrites** (règle du SKILL : chaque espèce porte (aq), (l), (s), (g) dans tout champ écrit). Les professeurs les écrivent (M1 partout, N partout, M2 dans ses tableaux). Chez nous, l’écran et les centres sont bons, mais il reste ces champs écrits sans les états :

| Diapo | Champ | Texte |
|---|---|---|
| td_b3_couple | cahier | « (CH₃COOH ⇌ CH₃COO⁻ + H⁺) ; … (NH₄⁺ ⇌ NH₃ + H⁺) » |
| td_s1_b1 | cahier[1].texte | même texte |
| td_b4_reaction | exercices_fin_de_cours[0].explanation | « (HCOOH ⇌ HCOO⁻ + H⁺) » et « (NH₃ + H⁺(aq) ⇌ NH₄⁺(aq)) » : il manque les états de HCOOH, HCOO⁻, H⁺ et NH₃ |
| C1_r4 | réaction juste, ecrit | « (H₂O ⇌ HO⁻ + H⁺) » |
| td_p5_ammoniac | réaction 2.2 ecrit et statements[1].explanation | « B + H₂O(l) ⇌ … » : B sans (aq) |
| td_b1_acide | réaction 1.1 ecrit | « acide éthanoïque → … + H⁺ » : H⁺ sans (aq) |
| td_p5_ammoniac | réactions 0.juste et 1.2, ecrit | couples écrits « H2O / HO- », « NH4+ / NH3 » en ASCII, sans indices ni exposants |

Priorité haute (règle du 16 novembre). Correction : passer `annote()` sur ces champs.

#### Manques chez un seul professeur

| Priorité | Catégorie | Ce que dit le professeur | Chez nous | Où l’ajouter |
|---|---|---|---|---|
| basse | Exercice type | Mélange acide + base qui ne sont pas l’eau (HCOOH + éthanoate de sodium), σ avec Na⁺, concentrations effectives à l’équilibre de toutes les espèces (N p145 ex. 1). | Réaction CH₃COOH + NH₃ (td_b4) sans suivi par σ. | exercice de td_n2_conductivite (facultatif) |
| basse | Exemple | HCO₃⁻ est un ampholyte (HCO₃⁻/CO₃²⁻ et CO₂,H₂O/HCO₃⁻) (M1 p1). | Absent. | td_b3b_eau (facultatif) |
| basse | Convention | En solution aqueuse, on remplace H⁺(aq) par H₃O⁺(aq) (M1 p2). | Dit de façon indirecte en td_p4_eau. | — |
| basse | Définition | État d’équilibre : les grandeurs observables (T, pH, couleur, conductance) restent constantes (M1 p5) ; R p1 : T, pression et concentrations constantes. | « Les quantités de matière ne changent plus » ; le pH constant est montré. | td_e3_etat (facultatif) |
| basse | Justification | « La conductivité se mesure quand l’état final est atteint », donc [X] = [X]_f (M2 p4). | Pas dit. | td_c2_relation |

#### Présent seulement à l’oral (à écrire)

- **td_c2_relation** : la voix dit « les ions HO⁻ sont très peu nombreux, on les néglige » ; l’écran et le cahier disent « ions HO⁻ négligés » sans le « car » (solution acide : [HO⁻] très petite devant [H₃O⁺]).
- **td_b3_couple** : la voix dit « pourquoi la double flèche ? parce que A⁻ peut reprendre H⁺ » ; ce n’est écrit nulle part.
- **td_a2_xmax** : la voix dit « l’eau ne s’épuise pas, elle est en excès, **donc** l’acide est le réactif limitant ». Le cahier met « (réactif limitant) » entre parenthèses, sans le « donc ».
- **td_n4_dosage** : la voix explique « combien en reste-t-il ? 10^(−10,2) fois le volume total, une quantité très petite » et « une réaction de dosage doit être totale » ; l’écran donne directement x_f = C_A·V_A − 10^(−pH)·(V_A + V_B).
- **td_p3_phmetre** : le « pourquoi » du rinçage (« pour ne pas mélanger les solutions et fausser la mesure ») n’est qu’à l’oral.
- **td_e4_dynamique** (écrit à l’écran, mais **pas au cahier**) : l’interprétation par les chocs efficaces (« autant de chocs efficaces dans chaque sens par unité de temps ») est dans `bullets` et `student_trace`, pas dans `cahier`. Or c’est la phrase que demande le cadre (TD5).

#### Démonstrations qui sautent des étapes

- **td_n4_dosage** (écran, cahier, centre) : x_f = C_A·V_A − 10^(−pH)·(V_A + V_B) arrive tout fait. Il manque : (1) la ligne finale du tableau n(H₃O⁺)_f = C_A·V_A − x_f ; (2) n(H₃O⁺)_f = [H₃O⁺]_f·(V_A + V_B) avec [H₃O⁺]_f = 10^(−pH) ; (3) l’application numérique 10^(−10,2) × 26,0·10⁻³ = 1,6·10⁻¹² mol, négligeable devant 7,2·10⁻⁴ mol ; (4) pourquoi H₃O⁺ est le réactif limitant.
- **td_n3_proportion** (écran, cahier) : « [CH₃COO⁻] = x_f/V = C_A·τ » saute x_f = τ·x_max = τ·C_A·V ; « [CH₃COOH] = C_A − C_A·τ » saute n(CH₃COOH)_f = C_A·V − x_f, puis la division par V.
- **td_n2_conductivite** (démo de la question) : la ligne 2 « [H₃O⁺] = σ/(λ₁ + λ₂) » ne repart pas de σ = λ₁·[H₃O⁺] + λ₂·[C₆H₅COO⁻] et de [C₆H₅COO⁻] = [H₃O⁺] (tableau), alors que c’est la question notée (1,5 pt).
- **td_a6_relation, exercice de fin de cours (et td_s2_b2)** : la 1ʳᵉ ligne « τ = x_f/x_max = [H₃O⁺]_éq·V/(C·V) = 10^(−pH)/C » fait trois pas d’un coup (remplacer, simplifier V, [H₃O⁺] = 10^(−pH)). La diapo elle-même les détaille ; le corrigé non.
- **td_c3_calcul** (écran) : 1,56·10⁻²/(39,09·10⁻³) utilise λ en S·m²·mol⁻¹ sans écrire la conversion 35,0 + 4,09 = 39,09 mS·m²·mol⁻¹ = 39,09·10⁻³ S·m²·mol⁻¹. Cette conversion est écrite dans l’exercice, pas sur la diapo.

#### Différences de notation ou de convention

| Nous | Eux | Laquelle garder |
|---|---|---|
| sens 1 / sens 2 | sens direct / sens indirect (N, M1) ; sens direct / sens inverse (R) | Écrire « sens direct (1) » et « sens inverse (2) » : c’est le mot du national. |
| H₂O(l) ; NH₃(aq) dissous | N p140-143 : H₂O(aq) (faux) ; N p138 : NH₃(g), CH₃NH₂(g) dans l’eau | Garder les nôtres (M1 écrit aussi H₂O(l)). |
| Réaction acide + base (td_b4) avec → | N p138 : ⇌ ; M1, M2, R : → | Garder →, comme la majorité. |
| [H₃O⁺]_éq dès la partie IV | M1, M2 : [H₃O⁺]_f, n_f(H₃O⁺) ; N : [H₃O]_f, puis x_éq et [H₃O⁺]_éq dans ses exercices | Garder _éq (national), en disant une fois que « final = équilibre » pour une réaction limitée (question déjà ouverte dans `chimie.md`). |
| Étalonnage avec pH 4,0 puis pH 7,0 | N p140 : d’abord pH 7, puis pH 4 (solution acide) ou pH 9 (solution basique) | Garder le nôtre, mais écrire « une solution de pH 7 et une autre proche des mesures (4 ou 9) ». |
| Tableau : « état initial / en cours / état final » | « Etat initial / En cours » (M1), « Intermédiaire » (N), « état de transformation » (M2) | Garder le nôtre. |
| Couple AH/A⁻ | R : AH/B | Garder le nôtre (N et M1 écrivent aussi HA/A⁻). |
| Estérification (td_e5) écrite en mots (« acide + alcool ⇌ ester + eau ») | — | Mots acceptés ; si on l’écrit en formules, tout en (l) (SKILL). |

#### Hors cadre chez les professeurs (ne pas ajouter)

- Quotient de réaction Qr, Qr,éq, constante d’équilibre K et l’effet de la température sur K (R p2) : cadre 2.2, au chapitre suivant. « Le taux dépend de K » : idem.
- Conductance G et sa relation avec [Xᵢ] : cadre 2.2 (p15), pas ce chapitre.
- Domaine de définition de log et f⁻¹(f(x)) = x (M2 p1) : mathématiques, inutiles ici.
- « Solutions amphotères » (N p138, M1 p1) : on peut se limiter au mot « ampholyte ».
- R est un résumé « SM PC SVT » : rien de propre à la série SM dans la p. 1.

### État d’équilibre d’un système chimique

Version auditée : `backend/data/courses/en_attente/phys_ch12_etat_equilibre.json` (écran, cahier des diapos et des séances, voix fr, questions, `demonstration.lignes`, exercices, réactions ; texte de `nos-cours/phys_ch12_etat_equilibre.txt`). Équations vérifiées par script dans tous les champs écrits (états (aq), (l), (s), (g)).

Sources lues :
- **Nidal** (Pr Nidal Naceiri Mrabti, cours 2 BIOF, `web/phys/nidal_p1.pdf`) : p. 149-158, lues en image. Pas de décalage (le pied « Page 149 » est la page 149 du PDF). p. 149-154 cours, p. 155 série d’exercices, p. 156-158 feuilles quadrillées vides.
- **M1** (`m_equilibre_1.pdf`, cours moutamadris) : p. 1-3, lues en image.
- **M2** (`m_equilibre_2.pdf`, scan d’un manuel « TS ») : p. 1-16, lues en image. p. 1-8 = « Chimie 5 : L’équilibre chimique » (contenu de notre ch11) ; p. 9-16 = « Chimie 6 : Quotient de réaction ; constante d’équilibre ». Pages citées = pages du PDF.
- **MR** (`m_equilibre_r.pdf`, carte mentale, Pr Ali Amziane) : p. 1, lue en image.
- **Cadre** (PDF officiel 2015) : p. 16-17 du PDF (« 14 » et « 15 sur 29 »), lues en image ; fiche `cadre_reference_2bac_pc.json` (`chapitres.etat_equilibre`, EE1-EE7) ; `docs/audit-programme-officiel/chimie.md` (ch12) ; `experience_profs.json` n’a pas de clé `etat_equilibre`.

#### Plan comparé
| Partie chez les professeurs | Où chez nous | Remarque |
|---|---|---|
| Situation-problème, objectifs (Nidal p. 149 ; MR) | ee_o1_carte, ee_o2_flacons | Équivalent. |
| Rappel : tableau d’avancement, x_max, τ, état d’équilibre dynamique (M1 p. 3 ; M2 p. 4-8 ; Nidal p. 152-153) | ee_r1_taux, ee_r2_equilibre | Tableau à deux lignes seulement (initial, équilibre) ; x_max = C·V sans « réactif limitant ». |
| Qr : définition, expression générale, eau solvant, solides (Nidal p. 150 ; M1 p. 1 ; M2 p. 9-10 ; MR) | ee_q1_quotient → ee_q4_solides | Pas de phrase de définition « dans un état donné » ; pas de précipitation. |
| Qr dépend du sens d’écriture : Qr’ = 1/Qr (M1 p. 1 ; M2 p. 11 ; MR) | ee_k4_inverse | Dit au niveau de K (« le quotient se retourne ») : suffisant. |
| Qr dépend de l’avancement : Qr(x) par le tableau (Nidal p. 150-151 ; M2 p. 11-12) | ee_q5_sans_unite, ee_i3_au_cours | Valeurs numériques seulement, pas d’expression Qr(x). |
| Qr,i d’un mélange | ee_i1_initial, ee_i2_melange, ee_i2b_calcul, ee_n3_melange | En plus chez nous (national 2020 R) : à garder. |
| Qr,éq : définition ; détermination par conductimétrie, σ = Σλᵢ[Xᵢ], G (Nidal p. 152-153 ; M1 p. 1-2 ; M2 p. 12-14) | ee_e1 → ee_e3 (par le pH), ee_m2_conductimetrie, ee_m3_calcul | Nous passons par le pH d’abord (bien) ; la conductimétrie n’a ni G ni forme générale de σ ni unités de λ. |
| K : Qr,éq indépendant de l’état initial, K = Qr,éq, ne dépend que de T (Nidal p. 152-153 ; M1 p. 2 ; M2 p. 14-15 ; MR) | ee_k1_trois, ee_k2_produits, ee_k3_constante | Mise en évidence par le pH (eux : par σ, trois concentrations) : équivalent. Pas d’expression générale de K avec [ ]éq. |
| K’ = 1/K (Nidal p. 153 ; M1 p. 2-3 ; MR) | ee_k4_inverse | Présent. |
| K > 10⁴ : réaction considérée totale (Nidal p. 153 ; M1 p. 3) | — | Absent de ch12 (présent en ch13, ab_d2_reaction). |
| τ dépend de l’état initial (Nidal p. 154 ; M1 p. 3 ; M2 p. 16 ; MR) | ee_z3_dilution, ee_f1_dilution, ee_f4_bilan | Présent. |
| τ dépend de K (Nidal p. 154 ; M1 p. 3 ; M2 p. 15-16 ; MR) | ee_f2_nature, ee_f3_courbe | Présent. |
| Exercices : C par la masse, tableau en C, V, x_éq, τ(pH), τ(σ), Qr,éq = Cτ²/(1 − τ) (Nidal p. 155) | ee_k5_tau, ee_m4_national, ee_n1 → ee_n6, exercices des séances | Présent sauf C = m/(M·V). |

#### Manques confirmés
| Priorité | Catégorie | Ce que disent les professeurs | Chez nous | Où l’ajouter |
|---|---|---|---|---|
| haute | Relation (cadre) | **G et σ = Σλᵢ[Xᵢ]** : cadre p. 17 (« 15 sur 29 ») : « Utiliser la relation liant la conductance G d’une partie de solution aux concentrations molaires effectives [Xᵢ] » ; M1 p. 1-2 : G = 1/R, G = σ·S/L, σ = λ(M⁺)[M⁺] + λ(X⁻)[X⁻] ; M2 p. 12 : σ = Σλ_Xᵢ·[Xᵢ] avec S·m⁻¹, S·m²·mol⁻¹, mol·m⁻³ ; fiche EE5 (« G = k·σ ») | Aucune conductance G dans le cours ; σ seulement pour l’acide éthanoïque, sans forme générale | ee_m2_conductimetrie (écran + cahier : G = k·σ, σ = Σλᵢ[Xᵢ] avec unités), ee_bl_fiche |
| haute | Tableau d’avancement | **Tableau complet à trois lignes** (initial / en cours : x, CV − x, excès, x, x / équilibre : x_éq) et **x_max justifié** : « l’eau est en excès, l’acide est le réactif limitant : CV − x_max = 0 ⇒ x_max = C·V » : Nidal p. 152-153 ; M1 p. 2-3 ; M2 p. 4, p. 12 | ee_r1_taux : lignes « état initial » et « équilibre » seules ; « x_max = C·V » sans raison (la ligne « x » et « si la réaction était totale » sont seulement à l’oral) | ee_r1_taux (écran, cahier, figure du tableau) ; rappel dans ee_k5_tau |
| haute | Unités / application numérique | **λ et σ avec leurs unités dans le calcul**, valeurs séparées de λ(H₃O⁺) et λ(A⁻) : Nidal p. 152-153 (λ₁ = 4,09·10⁻³ S·m²·mol⁻¹, λ₂ = 35·10⁻³ S·m²·mol⁻¹, A.N. complète) ; M1 p. 2 (A.N. avec S·m⁻¹ et S·m²·mol⁻¹) ; M2 p. 13-14 | ee_m3_calcul : « 4,6·10⁻³/(39,09·10⁻³) » sans unité, la somme des λ n’est pas détaillée ; l’unité S·m²·mol⁻¹ n’apparaît que dans un énoncé d’exercice et une réaction | ee_m2_conductimetrie (données λ), ee_m3_calcul (ligne par ligne) |
| moyenne | Démonstration / méthode | **Qr en fonction de l’avancement x** par le tableau ([X] = n(X)/V, puis Qr(x)), valeurs pour deux x ; conclusion « Qr dépend de l’avancement » : Nidal p. 150-151 (Qr = 4x³/((4·10⁻⁴ − 2x)²(10⁻⁴ − x)), Qr à t = 0 et t½) ; M2 p. 11-12 (Qr = x²/((10 − x)(20 − x)), x = 2,0 et 4,0 mmol) | ee_i3_au_cours : quatre valeurs de Qr à partir de [H₃O⁺], sans expression en x ni tableau | ee_i3_au_cours (ou une diapo après ee_q5_sans_unite) |
| moyenne | Définition | **Définition écrite de Qr** : « grandeur qui caractérise un système chimique dans un état donné » : Nidal p. 150 ; M1 p. 1 ; M2 p. 9 (cadre EE2 : « dans un état donné ») | ee_q1_quotient : lead « Un seul nombre pour décrire le mélange » ; la définition n’est ni à l’écran ni au cahier | ee_q1_quotient (bullet + cahier) |
| moyenne | Formule générale | **K = Qr,éq = [C]ᶜ_éq·[D]ᵈ_éq/([A]ᵃ_éq·[B]ᵇ_éq)** : Nidal p. 152-153 ; M1 p. 2 ; M2 p. 15 ; MR | Seulement « K = Qr,éq » et l’expression de l’acide éthanoïque | ee_e2_quotient ou ee_k3_constante ; ee_bl_fiche |
| moyenne | Conversion | **µS·cm⁻¹ / mS·cm⁻¹ → S·m⁻¹** (× 10⁻⁶ × 10², × 10⁻³ × 10²) : M1 p. 2 (σ = 343 µS/cm → 343·10⁻⁶·10² S·m⁻¹) ; M2 p. 13 (encadré de conversion), p. 14 | Seulement mS/m → S/m (implicite) et mol/m³ → mol/L | ee_m3_calcul (ligne de conversion) ou un exercice |
| moyenne | Condition | **Mesure faite à l’équilibre** : « la réaction acido-basique est rapide (instantanée) : l’état d’équilibre est déjà atteint quand on mesure σ ou le pH » : M1 p. 2 ; M2 p. 13 (et p. 5) | Absent (on écrit [ ]éq sans dire pourquoi la mesure donne l’équilibre) | ee_e1_concentrations, ee_m2_conductimetrie |
| basse | Exemple | **Qr d’une précipitation** (solide seul au produit) : Fe³⁺(aq) + 3HO⁻(aq) ⇌ Fe(OH)₃(s), Qr = 1/([Fe³⁺]·[HO⁻]³) : M1 p. 1 ; M2 p. 10 | Solides seulement dans métal/ion (Zn, Cu, Al) | ee_q4_solides (une ligne) ou exercice |
| basse | Ordre de grandeur | **K > 10⁴ : réaction considérée comme totale** : Nidal p. 153 ; M1 p. 3 | Absent de ch12 (enseigné en ch13, ab_d2_reaction) | ee_k3_constante (une ligne) ou laisser en ch13 |

#### Manques chez un seul professeur
| Priorité | Catégorie | Ce que dit le professeur | Chez nous | Où l’ajouter |
|---|---|---|---|---|
| basse | Exercice type | C = m/(M·V) à partir d’une masse dissoute (Nidal p. 155, ex. 1 et 2 ; M2 p. 4 seulement dans la partie ch11) | ee_z1_concentration : C = n/V, pas n = m/M | Exercice de séance (ee_s1) |
| basse | Démonstration | Cas A(aq) + B(aq) ⇌ C(aq) + D(aq) à même C : K = τ²/(1 − τ)², donc τ dépend de K (M1 p. 3) | ee_f2_nature : comparaison numérique seulement | Facultatif |
| basse | Ordre de grandeur | K très différents selon la réaction : 1,6·10⁻⁴ ; 4,0 ; 2,5·10⁴ (M2 p. 15) | Deux K (1,6·10⁻⁵, 1,8·10⁻⁴) | ee_k3_constante (facultatif) |
| basse | Exemple | Qr d’une réaction avec H⁺(aq) : H₂O₂(aq) + 2I⁻(aq) + 2H⁺(aq) ⇌ I₂(aq) + 2H₂O(l) (Nidal p. 150-151) | Absent | Facultatif |

#### Présent seulement à l’oral (à écrire)
- ee_r1_taux : « l’acide diminue de x, et il se forme… » (ligne « en cours » du tableau) et « si la réaction était totale : x_max = C·V » : seulement dans la voix.
- ee_m2_conductimetrie : « la cellule du conductimètre » (l’appareil, la mesure) : seulement dans la voix.
- ee_q3_eau : l’eau « il y en a énormément » (solvant en large excès) : voix et réactions, pas à l’écran ni au cahier.
- ee_k2_produits : « le volume est 100 mL, donc chaque concentration est divisée par deux » : l’écran donne seulement « C = 5,0·10⁻³ mol/L après mélange ».
- ee_n5_courbe : « la courbe devient plate : c’est l’état d’équilibre » : l’écran dit seulement « Palier ».

#### Démonstrations qui sautent des étapes
- ee_r1_taux → manquent : « l’eau est en excès, CH₃COOH est le réactif limitant : C·V − x_max = 0 » ; « n_éq(H₃O⁺) = x_éq (tableau) » avant x_éq = [H₃O⁺]éq·V ; la ligne τ = x_éq/x_max = [H₃O⁺]éq·V/(C·V) (elle existe seulement dans la démo de la séance ee_s1_b1).
- ee_e3_expression (DÉMO) → seul le numérateur est démontré ; manquent : « [H₃O⁺]éq = 10^(−pH) (définition du pH) », « [CH₃COO⁻]éq = [H₃O⁺]éq car n = x_éq pour les deux, même V », « [CH₃COOH]éq = C − x_éq/V = C − 10^(−pH) », puis la ligne de substitution.
- ee_k2_produits → départ par les produits (sens 2) sans tableau : ni « [H₃O⁺]éq = 10^(−3,56) = 2,75·10⁻⁴ mol/L », ni pourquoi [CH₃COO⁻]éq = [H₃O⁺]éq (mêmes quantités initiales, consommées ensemble) ni [CH₃COOH]éq = C − [H₃O⁺]éq (formé = consommé) ; on réutilise directement 10^(−2pH)/(C − 10^(−pH)) établie pour l’acide.
- ee_m3_calcul → manquent : « σ = 4,6 mS/m = 4,6·10⁻³ S·m⁻¹ », « λ(H₃O⁺) + λ(CH₃COO⁻) = 35,0·10⁻³ + 4,09·10⁻³ = 39,09·10⁻³ S·m²·mol⁻¹ », la substitution avec unités.
- ee_m4_national → « τ = σ/(C·(λ₁ + λ₂)) = 0,22 » sans valeurs de λ, sans conversion C = 1,0·10⁻³ mol/L = 1,0 mol/m³ sur sa ligne, sans A.N.
- ee_i3_au_cours → chaque Qr est donné sans [CH₃COOH] = C − [H₃O⁺] ni calcul (ex. (1,0·10⁻⁴)²/(9,9·10⁻³) = 1,01·10⁻⁶).
- ee_n5_courbe → manquent les lignes du tableau : n_éq(ester) = n_éq(eau) = x_éq = 0,4 mol ; n_éq(alcool) = 0,6 − x_éq = 0,2 mol ; [X] = n/V et V qui se simplifie (écrit « le volume se simplifie » sans la ligne).
- ee_n4_pile → (6,5·10⁻¹)²/(6,5·10⁻¹)³ = 1/(6,5·10⁻¹) = 1,54 ≈ 1,5 : l’étape intermédiaire manque.
- Bien faites : démo des séances ee_s2_b3 (K = C·τ²/(1 − τ) jusqu’au bout), ee_s1_b3 (Qr,i), ee_s2_b1, ee_i2_melange, ee_n3_melange, ee_k5_tau.

#### Différences de notation ou de convention
| Nous | Eux | Laquelle garder |
|---|---|---|
| Eau solvant et solides « n’apparaissent pas dans Qr » | « [H₂O] = 1 », « [X] = 1 si solide » (Nidal p. 150), « concentration d’un solide remplacée par 1 » (M2 p. 10, MR) | Nous (cadre EE1 ; « activité = 1 » hors cadre). |
| « concentrations (en mol/L) » | « concentrations molaires effectives » (Nidal p. 150, 152 ; M2 p. 9 ; cadre p. 17) | Nous, en ajoutant une fois le mot « effectives » (vocabulaire du cadre). |
| mol/L, S/m, mol/m³ | mol·L⁻¹, S·m⁻¹, S·m²·mol⁻¹ (tous) | Les deux sont acceptés ; écrire au moins une fois l’écriture du bac. |
| x_éq sur les diapos, x_f dans la démo ee_s1_b1 et des réactions | « état final = état d’équilibre : x_f = x_éq » écrit (M1 p. 3 ; M2 p. 13 encadré) | Écrire « x_f = x_éq » une fois (ee_r1_taux). |
| Réactions de ee_i2b_calcul (e1s2) et ee_n3_melange (e1s2) : « Qr sans unité car les unités se simplifient » | Tous : Qr « grandeur sans unité » (convention, concentrations en mol·L⁻¹) | Convention (règle de cours-concentration) : corriger ces réactions. |
| **ee_n5_courbe** (écran) « Acide éthanoïque + éthanol ⇌ ester + eau » ; exercice, démo et réaction « acide + alcool ⇌ ester + eau » : sans état physique | — | Règle des états : estérification tout en (l). Seules équations écrites sans état du cours ; toutes les autres ont leurs états (vérifié par script). |
| ⇌ | « = » (M2), « → » à tort pour l’acide avec l’eau (Nidal p. 152) | Nous (⇌). |
| [H₃O⁺]éq à 3 chiffres (3,89·10⁻⁴) | « concentration déduite d’un pH : au plus deux chiffres significatifs » (M2 p. 3, partie ch11) | Garder nos valeurs (pH lu au centième), mais le dire une fois. |
| Lead ee_q1 « Un seul nombre pour décrire le mélange » | « grandeur qui caractérise un système dans un état donné » | Ajouter la phrase des professeurs (voir manques). |

#### Hors cadre chez les professeurs (ne pas ajouter)
- « Sa valeur renseigne sur l’évolution du système » (M1 p. 1 ; M2 p. 9) : critère d’évolution, sous-domaine 3 (piles).
- Concentration du solide ou de l’eau « égale à 1 » (Nidal p. 150 ; M2 p. 10 ; MR) : notion d’activité.
- Espèces gazeuses dans Qr (M2 p. 10, signalé hors programme par le manuel lui-même).
- M2 p. 1-8 (couples de Brønsted, définition du pH, pH-mètre U = a − b·pH, étalonnage, sens direct/inverse par ajout d’un réactif, chocs efficaces à l’échelle microscopique) : contenu de ch11, pas de ch12.
- Ka, pKa, Ke (aucun professeur ne les met ici ; chapitre suivant).

### Transformations liées aux réactions acido-basiques

Sources lues :
- Notre cours : `backend/data/courses/en_attente/phys_ch13_acides_bases.json` (version en attente), tous les champs écrits (écran, cahier, centre, questions, réactions, `exercices_fin_de_cours`, démonstrations, `seances`), plus `nos-cours/phys_ch13_acides_bases.txt`. Les équations dessinées au tableau par les simulations ont été lues dans `frontend/public/media/simulations/chimie/acides-bases-tableau/*.html`.
- Pr Nidal Naceiri Mrabti, cours 2 BIOF, `web/phys/nidal_p1.pdf`, **pp. 159-174**, lues en image. Pas de décalage (page du sommaire = page du PDF) ; seule la page 171 (série d’exercices) porte par erreur « Page 170 » en pied. Les pp. 172-174 sont quadrillées et vides. Abrégé **N**.
- Pr Sbiro Abdelkrim (moutamadris), `web/chim/m_acidebase_1.pdf`, **pp. 1-4**, lues en image. Abrégé **M1**.
- Manuel « TS, Chimie 7 : constante d’acidité » (moutamadris, scan, sans nom d’auteur), `web/chim/m_acidebase_2.pdf`, **pp. 1-8**, lues en image. Il s’arrête aux indicateurs colorés : il ne traite pas le dosage. Abrégé **M2**.
- Pr Zakaryae Chriki, résumé n° 5, `web/chim/m_acidebase_r.pdf`, **pp. 1-2**, lues en image. Abrégé **R**.
- Cadre officiel : PDF CNEEO 2015, **p. 15/29** (PDF p. 17, savoir-faire du sous-domaine 2.3) et **p. 24/29** (PDF p. 26, annexe 1, contenus 2.3), lues en image. Le JSON ne donne qu’une ligne : « produit ionique de l’eau, Ka, pKa, dosage acido-basique ». J’ai aussi lu la fiche `cadre_reference_2bac_pc.json` (clé `acides_bases`, AB1-AB10, `hors_cadre`, `decisions`), `docs/audit-programme-officiel/chimie.md` (§ ch13 et § PDF) et le SKILL cours-concentration (§ Chimie). `experience_profs.json` n’a pas de clé `acides_bases` : il n’y a que `ondes_mecaniques`.

#### Plan comparé

| Partie chez les professeurs | Où chez nous | Remarque |
|---|---|---|
| Conductivité de l’eau pure faible mais non nulle, donc l’eau contient des ions (N p161 : σ = 5,5 µS·m⁻¹ ; M1 p1) | ab_o2_trois_ph (on pose la question « quels ions ? ») | La preuve par la conductivité manque. |
| Autoprotolyse : équation avec les états (N p160-161, M1 p1, M2 p1, R p1) | ab_w1_autoprotolyse | Présente, avec les états à l’écran. |
| Tableau d’avancement de l’autoprotolyse pour 1 L : n₀ = ρ·V/M, x_max = n₀/2 ≈ 27,8 mol, x_éq = 10⁻⁷ mol, τ ≈ 3,6·10⁻⁹ (N p160, M1 p1, M2 p1) | — | Absent. On écrit seulement « réaction très limitée ». |
| Ke est la constante d’équilibre de l’autoprotolyse ; pKe = −log Ke, Ke = 10^(−pKe) ; Ke ne dépend que de la température (N p161-162, M1 p1, M2 p2, R p1) | ab_w2_ke | Ke y est seulement « produit ionique ». Ni « constante d’équilibre », ni Ke(T), ni Ke = 10^(−pKe). |
| Solution neutre, acide, basique : [H₃O⁺]² = Ke donne pH = pKe/2, et les inégalités ; à 0 °C, pKe = 15 et la neutralité est à pH = 7,5 (N p161-162, M2 p3) ; échelle de pH (N p162, M1 p1, M2 p3) | ab_w3_solutions | Seulement la règle « 7 à 25 °C », sans démonstration ni pKe/2. |
| pH à partir de [HO⁻] : pH = pKe + log[HO⁻], [HO⁻] = 10^(pH − pKe) (M2 p2, N p165) | ab_w4_ho, ab_w5_soude | Présent, avec 14 à la place de pKe. |
| Ka : définition avec AH(aq) + H₂O(l) ⇌ A⁻(aq) + H₃O⁺(aq), pKa, Ka = 10^(−pKa) (N p162, M1 p1-2, M2 p3, R p1) | ab_a1_ka, ab_a2_pka | Présent. |
| pH = pKa + log([A⁻]/[AH]), démontré (N p162, M1 p2, M2 p4, R p1) | ab_p1_relation | Présent ; il manque une étape (voir démonstrations). |
| Couples de l’eau : Ka = 1 et Ka = Ke, chacun tiré de son équation (M2 p4) | ab_a5_eau | Les valeurs sont données, les équations manquent. |
| K = Ka₁/Ka₂ = 10^(pKa₂ − pKa₁), démontré (N p163, M1 p2, M2 p4-5, R p1) | ab_k1_reaction, ab_k2_puissance | Présent ; la ligne du produit des deux fractions manque. |
| Comparer les acides : tableau d’avancement, τ = 10^(−pH)/C, influence de pKa (N p163-164, M1 p2, M2 p5) | ab_r2_constante, ab_c1_acides | Les valeurs de τ sont données sans calcul (voir démonstrations). |
| Comparer les bases : tableau, τ = 10^(pH − pKe)/C (N p164-165, M2 p6) ; Ka = (1 − τ)·Ke/(C·τ²) (M1 p3) | ab_b1, ab_b2_taux, ab_c2_bases, ab_a4_ammonium | Présent : τ = [HO⁻]_éq/C et Ka = Ke/Qr,éq, qui reviennent au même. |
| Axe des pKa, force croissante (N p165, M2 p3) | ab_c3_classement | Présent, de 0 à 14 seulement (c’est voulu, voir hors cadre). |
| Domaines de prédominance (N p166, M1 p3, M2 p7, R p1) | ab_p2_domaines | Présent. |
| Diagramme de distribution, α(HA) = [HA]/([HA] + [A⁻]) × 100 ; application : pourcentage à partir du pH (N p166-167, M1 p4, M2 p7, R p2) | ab_p3_distribution, ab_p4_national, ab_n3_2022n | Présent sous la notation « % AH ». |
| Indicateur coloré : HInd(aq) + H₂O(l) ⇌ Ind⁻(aq) + H₃O⁺(aq) ; teinte acide si pH < pKa − 1, teinte basique si pH > pKa + 1 ; teinte sensible ; zone de virage (N p167, M1 p4, M2 p8) | ab_i1_indicateur, ab_i2_virage | La couleur et la zone sont là. L’équation et la règle pKa ± 1 manquent. |
| Dosage : définition ; réaction totale, rapide, sélective ; méthodes colorimétrique, conductimétrique, pH-métrique (N p168, R p2) | ab_d1_montage, ab_d2_reaction | Présent avec « unique » ; le sens des trois mots n’est donné qu’à l’oral. |
| Relation d’équivalence générale par le tableau d’avancement : C_A·V_A/a = C_B·V_BE/b (N p168) ; C_A·V_A = C_B·V_BE (R p2) | ab_d3_equivalence | Seulement le cas des coefficients 1 ; le tableau n’apparaît qu’à l’oral et dans l’image. |
| Montage du dosage pH-métrique, étalonnage, pro-pipette (N p169, R p2) | ab_d1_montage | Présent, sans étalonnage ni prélèvement. |
| Tangentes parallèles ; courbe dérivée (extrémum) (N p169, R p2) | ab_d5_tangentes, ab_d6_derivee | Présent (on dit toujours « maximum »). |
| Exploiter pH = f(V_B) : pH_A à V_B = 0 (nature de l’acide), [H₃O⁺] et [HO⁻] en tout point, pH_E, choix de l’indicateur (R p2 ; N p170) | ab_e1_phe, ab_e3_indicateur, ab_w4_ho | Présent, sauf la lecture à V_B = 0. |
| Titrage colorimétrique : on arrête au changement de teinte et on lit V_E (N p169) | ab_e3_indicateur (une phrase) | Partiel. |
| Taux d’avancement de la réaction de dosage τ ≈ 1 (N p170 ; cadre p24/29) | ab_d2_reaction | Présent à l’écran, absent du cahier. |
| Exercice type « vinaigre » : dilution 1/100, masse d’acide, degré d’acidité, C_m (N p171) | ab_bl_fiche (C₀ = F·C ; C_m = C·M), ab_e4_base, ab_n5_2023r | La dilution est faite. C_m = C·M n’est enseigné sur aucune diapo. |
| — | ab_e2_demi, ab_e4_base, ab_e5_conductimetrie, ab_e5b_pourquoi, ab_n1 à ab_n5 | Chez nous seulement : demi-équivalence (pH = pKa), dosage d’une base, dosage conductimétrique, sujets du national. Aucun des quatre professeurs ne traite la demi-équivalence. |

#### Manques confirmés

| Priorité | Catégorie | Ce que disent les professeurs | Chez nous | Où l’ajouter |
|---|---|---|---|---|
| haute | État physique | Toutes les équations portent (aq)/(l) : N p160, 162, 163, 166 ; M1 p1-3 ; M2 p1-6 ; R p1. | L’écran et le cahier les ont. **Elles manquent dans les équations dessinées au tableau par les simulations** : `eau.html` l. 639 (AH ⇌ A⁻ + H⁺) et l. 717 (2H₂O ⇌ H₃O⁺ + HO⁻) ; `base.html` l. 574 et 678 (tableaux), l. 624 (NH₃ + H₂O ⇌ …), l. 721 (CH₃NH₂ + H₂O ⇌ …) ; `dosage.html` l. 690 (CH₃COOH + HO⁻ → …) ; `exploiter.html` l. 905 (NH₃ + H₃O⁺ → …) et l. 1030 ((CH₃)₃N + H₃O⁺ → …) ; `acidite.html` et `comparer.html` (équations écrites en texte). Elles manquent aussi dans des réactions et des réponses attendues : ab_a1_ka `reponses_fin_de_cours.e0s0.1.1.ecrit` (« AH + H2O ⇌ A⁻ + H3O⁺ », sans indices ni états) ; ab_n1_2016n `e0.0.2.ecrit` et `e0.2.2.ecrit` (« C2H5COOH + HO⁻ → … ») ; C1 `rappels[1].attendu` ; C7 `rappels[0].attendu` ; `seances[2].blocs[2].retrouver.attendu`. Sur ab_w5_soude, on écrit « Na⁺ + HO⁻ » sans (aq) et sans l’équation de dissolution, qui n’apparaît que dans l’exercice. | Les simulations citées ; les réactions et les attendus cités ; ab_w5_soude (bullet 0 : NaOH(s) → Na⁺(aq) + HO⁻(aq)) |
| haute | Définition (cadre) | « Savoir que le produit ionique de l’eau, Ke, est la constante d’équilibre associée à l’équation de la réaction d’autoprotolyse » (cadre p15/29) ; N p161 (même phrase) ; M1 p1 ; M2 p4 (Ka₂ = Ke). | ab_w2_ke dit seulement « produit ionique de l’eau ». Le mot « constante d’équilibre » n’y est jamais. | ab_w2_ke (bullet 0, cahier, centre) |
| haute | Condition + démonstration | Ke ne dépend que de la température (M1 p1, M2 p2 Doc 4 avec un tableau Ke(T), R p1) ; neutre : pH = pKe/2, acide : pH < pKe/2, basique : pH > pKe/2, démontré à partir de [H₃O⁺]² = Ke (N p161, M2 p3) ; à 0 °C, pKe = 15 et neutre à 7,5 (N p162). | ab_w3_solutions dit seulement « ces repères (7) sont valables à 25 °C ». Ni Ke(T), ni pKe/2, ni démonstration. Un sujet à 60 °C ne peut pas être traité. | ab_w2_ke (Ke ne dépend que de T) ; ab_w3_solutions (pH = pKe/2 et sa démonstration) |
| moyenne | Définition + relation | Indicateur : HInd(aq) + H₂O(l) ⇌ Ind⁻(aq) + H₃O⁺(aq) et pH = pKa + log([Ind⁻]/[HInd]) (M1 p4, M2 p8) ; teinte acide si [HInd] > 10·[Ind⁻], soit pH < pKa − 1 ; teinte basique si pH > pKa + 1 ; zone de virage [pKa − 1 ; pKa + 1], démontrée (N p167, M2 p8) ; M1 p4 en donne l’idée (« k fois supérieure »). Cadre p24/29 : « zone de virage ». | ab_i1_indicateur : le couple HInd/Ind⁻ sans équation ; ab_i2_virage : « encadre le pKa ». Nulle part pKa ± 1, ni la démonstration. | ab_i1_indicateur (équation) ; ab_i2_virage (pKa − 1 < pH < pKa + 1, avec ses lignes) |
| moyenne | Tableau d’avancement + ordre de grandeur | Autoprotolyse pour V = 1 L : n₀ = ρ·V/M = 55,5 mol, x_max = n₀/2 ≈ 27,8 mol, x_éq = [H₃O⁺]·V = 10⁻⁷ mol, τ = 3,6·10⁻⁹ ≪ 1, donc très limitée (N p160, M1 p1, M2 p1). | ab_w1_autoprotolyse affirme « réaction très limitée » sans le tableau ni le τ. | ab_w1_autoprotolyse, ou une diapo juste après |
| basse | Vocabulaire du bac | « Titrage », « titrer » (N p168-170, R p2 « doser (ou titrer) ») ; cadre p24/29 : « titrage pH-métrique ». | Les mots « titrage » et « pH-métrique » n’apparaissent nulle part (on dit seulement « dosage », « titrante », « titrée »). | ab_d1_montage |
| basse | Expérience | L’eau pure conduit très peu le courant, mais un peu, donc elle contient des ions (N p161, M1 p1). | Absent. | ab_o2_trois_ph ou ab_w1_autoprotolyse |
| basse | Relation inverse | Ke = 10^(−pKe) (M1 p1, M2 p2, R p1). | Seulement pKe = −log Ke. | ab_w2_ke |

#### Manques chez un seul professeur

| Priorité | Catégorie | Ce que dit le professeur | Chez nous | Où l’ajouter |
|---|---|---|---|---|
| moyenne | Tableau + relation générale | Tableau d’avancement de aA + bB → cC + dD (initial, intermédiaire, équivalence) ; à l’équivalence C_A·V_A − a·x_E = 0 et C_B·V_BE − b·x_E = 0, donc C_A·V_A/a = C_B·V_BE/b (N p168). | Le tableau n’est qu’à l’oral et dans l’image (voir « présent seulement à l’oral ») ; on ne traite que des coefficients 1. | ab_d3_equivalence |
| moyenne | Calcul (notre propre fiche) | Exercice vinaigre : dilution 1/100, masse d’acide m = C·V·M, degré d’acidité (N p171). | C_m = C·M figure dans la compétence C7 (« masse, concentration massique ») et dans ab_bl_fiche, mais aucune diapo ne l’enseigne (déjà relevé dans `chimie.md`). | ab_n5_2023r ou ab_e4_base |
| basse | Méthode | Courbe dérivée : V_E à l’extrémum de dpH/dV, maximum **ou minimum** (N p169). | « Maximum » partout, même pour les courbes qui descendent (ab_e4_base, ab_n2_2022r, ab_n5_2023r). | ab_d6_derivee |
| basse | Méthode | Titrage colorimétrique : quelques gouttes d’indicateur dans la solution titrée, arrêt au changement de teinte, lecture de V_E sur la burette (N p169). | Une seule phrase dans ab_e3_indicateur. | ab_e3_indicateur |
| basse | Montage | Prélever l’échantillon à la pipette (pro-pipette), étalonner le pH-mètre (N p169). | Absent ici (l’étalonnage est vu en ch11). | ab_d1_montage |
| basse | Lecture de courbe | pH_A à V_B = 0 : nature de la solution, et dissolution totale ou limitée ; le sens de la courbe donne le type de dosage (R p2). | Pas de lecture à V_B = 0. | ab_d4_courbe |
| basse | Vocabulaire | L’eau est un « ampholyte » / une « espèce amphotère » (M2 p1, p4). | Seulement dans une réaction de ab_r1_rappel ; l’écran de ab_a5_eau dit « un acide et une base ». | ab_a5_eau |
| basse | Outil maths | Propriétés du log : log(a·b) = log a + log b, log(a/b), log 1 = 0 (M2 p2 Doc 5). | ab_z1_puissance donne seulement log(10ⁿ) = n, alors que ab_p1, ab_k2 et ab_n4 se servent des autres propriétés. | ab_z1_puissance |

#### Présent seulement à l’oral (à écrire)

- ab_d2_reaction : le sens de « rapide » (dès chaque goutte), « totale » (jusqu’à l’épuisement d’un réactif) et « unique » (aucune autre réaction) n’est donné qu’à la voix ; N p168 l’écrit. Le contrôle τ ≈ 1 est à l’écran et dans le student_trace, mais pas dans le **cahier**.
- ab_d3_equivalence : le tableau d’avancement de la réaction de dosage (avant, à, après l’équivalence) est à la voix (« Regarde le tableau d’avancement ») et dans l’image, pas à l’écran ni au cahier.
- ab_r2_constante : le tableau d’avancement de l’acide dans l’eau (« le tableau d’avancement donne… ») n’est qu’à la voix et dans l’image ; l’écran donne seulement les résultats.
- ab_w1_autoprotolyse : la raison de [H₃O⁺] = [HO⁻] dans l’eau pure (« chaque réaction forme un H₃O⁺ et un HO⁻ ») n’est qu’à la voix (M2 p1 l’écrit).
- ab_i2_virage : « les deux formes y sont presque à égalité » (la raison de la teinte sensible) n’est qu’à la voix ; la liste des quatre zones de virage est dite ici et n’est écrite qu’en ab_e3.
- ab_d5_tangentes : la consigne de rédaction « à l’examen, la méthode doit se voir sur le dessin » n’est qu’à la voix.

#### Démonstrations qui sautent des étapes

- ab_k1_reaction (écran, cahier) et toutes les démonstrations de K (ab_k2_puissance e0 et e1, ab_k4_national question, `seances[2].blocs[0]`) : on écrit « On multiplie en haut et en bas par [H₃O⁺]_éq : K = Ka₁/Ka₂ » sans la ligne K = ([A₁⁻]_éq·[H₃O⁺]_éq/[AH₁]_éq) × ([AH₂]_éq/([A₂⁻]_éq·[H₃O⁺]_éq)). Les quatre professeurs l’écrivent (N p163, M1 p2, M2 p4-5, R p1).
- ab_a4_ammonium (écran, cahier) : « On multiplie en haut et en bas par [H₃O⁺]_éq : Qr,éq = Ke/Ka » sans la fraction [NH₄⁺]·[HO⁻]·[H₃O⁺]/([NH₃]·[H₃O⁺]) ni le regroupement (M1 p3 l’écrit). Même saut dans la démonstration e0 : « Ka·Qr,éq = [H₃O⁺]·[HO⁻] » arrive sans le produit des deux fractions ni les simplifications (×2 avec `seances[1].blocs[1]`).
- ab_p1_relation : on passe de Ka = … à « −log Ka = −log[H₃O⁺]_éq − log([A⁻]_éq/[AH]_éq) » sans la ligne −log Ka = −log([A⁻]_éq·[H₃O⁺]_éq/[AH]_éq) (N p162) et sans nommer la propriété log(a·b) = log a + log b.
- ab_a3_mesure (bullet 2 de l’écran, cahier, question, exercises[0]) : Ka = 10^(−2pH)/(C − 10^(−pH)) est posé sans sa ligne d’origine. Il faut le tableau : n(A⁻) = n(H₃O⁺) = x_éq, donc [A⁻]_éq = [H₃O⁺]_éq = x_éq/V = 10^(−pH), et [AH]_éq = (C·V − x_éq)/V = C − 10^(−pH) (M1 p2, N p166-167). Dans exercises[0], la formule finale arrive dès la ligne 1. Dans `exercices_fin_de_cours[0]`, « Ka = Qr,éq » est écrit sans le « car » (Ka est le K de la réaction de l’acide avec l’eau).
- ab_a5_eau : Ka(H₃O⁺/H₂O) = 1 et Ka(H₂O/HO⁻) = Ke sont donnés sans les équations H₃O⁺(aq) + H₂O(l) ⇌ H₂O(l) + H₃O⁺(aq), qui donne Ka = [H₃O⁺]/[H₃O⁺] = 1, et H₂O(l) + H₂O(l) ⇌ HO⁻(aq) + H₃O⁺(aq) (M2 p4).
- ab_w3_solutions : la règle pH < 7, = 7, > 7 n’est pas démontrée. Il manque [H₃O⁺] = [HO⁻] ⇒ [H₃O⁺]² = Ke ⇒ pH = pKe/2 = 7, puis les inégalités (N p161, M2 p3).
- ab_c1_acides : τ = 0,039 et τ = 0,126 sont donnés sans calcul. Il manque τ = x_éq/x_max = [H₃O⁺]_éq/C = 10^(−pH)/C = 10^(−3,41)/1,0·10⁻² = 0,039 (N p164, M2 p5).
- ab_d2_reaction (vérifier τ ≈ 1) : il manque V_total = V_A + V_B = 30 mL dans n(HO⁻)restant = [HO⁻]·V_total ; la raison de x_max = C_B·V_B (HO⁻ est le réactif limitant avant l’équivalence) ; puis x_f = x_max − n(HO⁻)restant et τ = x_f/x_max calculé en nombres.
- ab_d3_equivalence (écran, cahier) et les sept démonstrations « À l’équivalence… n(acide) = n(base) versée, donc C_A·V_A = C_B·V_BE » (ab_d3, ab_d6, ab_e4, ab_e5, ab_n2, ab_n3, ab_n5) : la ligne n(acide)initial = C_A·V_A et n(HO⁻)versé = C_B·V_BE manque, ainsi que le tableau à l’équivalence (C_A·V_A − x_E = 0 et C_B·V_BE − x_E = 0, N p168).
- ab_e2_demi : n(CH₃COOH)initial = C_A·V_A = 1,0·10⁻² × 20,0·10⁻³ = 2,0·10⁻⁴ mol n’est pas écrit (le 2,0·10⁻⁴ arrive sans origine) ; « même volume, donc [AH] = [A⁻] » n’est pas dit ; il n’y a pas de preuve littérale (n(AH)restant = C_A·V_A − C_B·V_BE/2 = C_A·V_A/2), seulement l’exemple chiffré.
- ab_e5b_pourquoi : la réaction de dosage H₃O⁺(aq) + HO⁻(aq) → 2H₂O(l) n’est écrite ni en e5 ni en e5b ; « Na⁺ (λ = 5,01) » n’a pas d’unité (mS·m²·mol⁻¹) ; la baisse de σ n’est pas justifiée par σ = Σλᵢ[Xᵢ] ; on ne dit pas pourquoi on ajoute 200 mL d’eau (pour rendre la dilution négligeable et garder des droites). Aucun des quatre professeurs ne traite ce dosage : constat interne seulement.
- ab_p4_national exercises[0] (et `seances[2].blocs[1]`) : « Donc le pourcentage de CH₃COO⁻ est [CH₃COO⁻]_éq/C » arrive sans la définition % CH₃COO⁻ = [CH₃COO⁻]/([CH₃COOH] + [CH₃COO⁻]).

#### Différences de notation ou de convention (nous / eux, laquelle garder)

| Nous | Eux | Garder |
|---|---|---|
| Ke = [H₃O⁺]·[HO⁻] (sans _éq) | Ke = [H₃O⁺]_éq·[HO⁻]_éq (N p161, M1 p1, M2 p2, R p1) | Écrire _éq dans la définition (cohérent avec Ka, écrit avec _éq) ; on peut ensuite l’omettre, comme le dit M2 p2 (note 1). |
| [HO⁻] = 10^(pH − 14) | [HO⁻] = 10^(pH − pKe) (N p165, M2 p2) ; pH = pKe + log[HO⁻] (M2 p2) | Forme générale avec pKe, puis « = 14 à 25 °C » (lié au manque Ke(T)). |
| Ka, pKa | K_A, pK_A (N, M1, M2, R ; c’est aussi la notation des sujets) | Garder Ka et ajouter une fois « noté aussi K_A ». |
| « % AH » (cahier de ab_p3 : seulement % AH) | α(HA) = [HA]/([HA] + [A⁻]) × 100 et α(A⁻) (N p166, M1 p4, R p2) | Ajouter α et écrire les deux formules. |
| Réaction de dosage « rapide, totale, unique » | « totale, rapide, sélective » (N p168, R p2) | Garder « unique » et ajouter « (sélective) ». |
| pKa(BBT) ≈ 7,0 | 7,2 (M1 p4, tableau) ; zone 6,0 – 7,6 pareille | Écart de lecture sans effet. Garder ≈ 7, puisque c’est « environ ». |
| 2H₂O(l) ⇌ … | H₂O(l) + H₂O(l) ⇌ … (M1 p1, R p1) ; « = » à la place de ⇌ (M2) | Garder 2H₂O(l) et ⇌ (le cadre demande ⇌ pour une réaction limitée). |
| « dosage » seul | « titrage » (N, R, cadre) | Garder « dosage » et ajouter « (titrage) » (voir manques). |

#### Hors cadre chez les professeurs (ne pas ajouter)

- Couples hors de 0-14 et acides ou bases « dont la réaction avec l’eau est quasi totale » : HI (−10), HCl (−6,3), HNO₃ (−1,8), NH₃/NH₂⁻ (33), C₂H₅OH/C₂H₅O⁻ (15,9) (N p165 ; M2 p3 Doc 8 et p6 remarques). Ils ont été retirés exprès (`chimie.md`, ab_c3_classement).
- Vocabulaire de la dissociation : « l’acide le plus fort (qui dissocie fortement dans l’eau) » (N p164-165). Hors cadre selon `chimie.md` (C6_r1).
- Renvois au manuel français TS (« activité préparatoire p. 143 », « rabats », « travaux pratiques p. 153 », notation pK_Ai) (M2) : propres à ce manuel.
- Le facteur « k = 9 » du BBT et le jaune de nitrazine (M1 p4) : détails sans intérêt pour le bac. La règle pKa ± 1 (facteur 10) suffit.
