## Chimie ch10 à ch13 — démonstrations

Les copies en attente sont dans `backend/data/courses/en_attente/` : phys_ch10_cinetique, phys_ch11_transformations_deux_sens, phys_ch12_etat_equilibre et phys_ch13_acides_bases. Aucune copie n'existait avant ; chaque copie part du cours en ligne, qui n'a pas été touché. Seuls les objets `demonstration` ont changé (vérifié par comparaison avec le cours en ligne).

Règles appliquées (10 et 37) :
- la relation, avec son origine (tableau d'avancement, loi des gaz parfaits, Ke, équivalence, demi-équivalence) ;
- chaque conversion d'unité sur sa ligne ;
- la substitution, puis chaque calcul intermédiaire (carré, différence, puissance de dix) ;
- le résultat avec son unité, puis la phrase qui répond à la question.

Les équations réécrites portent les états (aq), (l), (s), (g). Chaque démonstration d'un bloc (`seances[].blocs[].exercice`) qui était une copie d'une démonstration de diapo a reçu la même nouvelle version.

Les exemples travaillés des diapos et du cahier (`bullets`, `centre`, `student_trace`, `cahier`) ont été relus et leurs calculs recalculés en Python : tous sont justes. Ce sont des récapitulatifs, et chaque exercice a sa propre démonstration complète. Ils n'ont pas été modifiés, pour ne toucher ni aux voix ni au pointage.

### phys_ch10_cinetique — 41 relues, 34 réécrites (25 + 9 copies de bloc)
- **ci_m3_titrage f0 (et ci_s1_b2)**
  - Avant : `n(I₂) = 0,020 × 16,9·10⁻³/2 = 1,69·10⁻⁴ mol = 0,169 mmol`
  - Après, une ligne par étape : l'équivalence (I₂(aq) + 2S₂O₃²⁻(aq), donc C·V_E/2) ; V_E converti en L ; la substitution ; 1,69·10⁻⁴ mol ; × 10 prélèvements ; 1,69·10⁻³ mol = 1,69 mmol ; x = n(I₂).
- **ci_g3_formule q**
  - Avant : la démonstration calculait σ₀ mais ne disait jamais l'unité demandée.
  - Après : analyse des unités ; 1 mol/L = 10³ mol/m³ ; le calcul ; « la concentration se met en mol/m³ ».
- Autres réécritures :
  - « dx/dt = pente » et la pente sur leur ligne : v4_bareme, n1, n2 ;
  - conversions mS → S et mol/L → mol/m³ : r2, s2_b1, p4 ;
  - origine de la formule x = (P − P₀)·V/(R·T) : p2 ;
  - raison du réactif limitant : a2, n1 e0 ;
  - « x_f = x_max car totale » : n1 f0 ;
  - lecture de t₁/₂ non demandée retirée : n6 et n7.

### phys_ch11_transformations_deux_sens — 25 relues, 19 réécrites (12 + 7)
- **td_a6_relation f0**
  - Avant : `τ = 10^(−pH)/C`, sans dire d'où vient la formule.
  - Après : τ = x_f/x_max = [H₃O⁺]·V/(C·V) ; 10^(−3,41) = 3,89·10⁻⁴ ; la substitution ; 0,039 ; « limitée ».
- **td_c3_calcul q**
  - Avant : la démonstration se terminait sur τ, alors que la question demandait l'unité.
  - Après : (S·m⁻¹)/(S·m²·mol⁻¹) = mol·m⁻³ ; l'exemple ; la conversion ; « elle sort en mol/m³, on divise par 10³ ».
- Autres réécritures :
  - lignes « 10^(−pH) = … » ajoutées : a3, a5, n1, n3 ;
  - λ converti de mS en S : c3 e0, n2 ;
  - conservation de la matière ajoutée à la dilution : d1b ;
  - τ₁ et τ₂ calculés sur des lignes séparées : e6.

### phys_ch12_etat_equilibre — 28 relues, 26 réécrites (18 + 8)
- **ee_m4_national e0**
  - Avant : `[A⁻]_éq = [H₃O⁺]_éq = C·τ`, sans justification.
  - Après : AH(aq) + H₂O(l) ⇌ A⁻(aq) + H₃O⁺(aq) et K = Qr,éq ; x_éq = τ·C·V ; le tableau ; [AH] = C(1 − τ) ; la substitution ; C²τ²/(C(1 − τ)) ; « on simplifie par C ».
- **ee_i2_melange e0**
  - Avant : quatre quantités calculées sur une seule ligne.
  - Après : n = C·V sur deux lignes ; « V_T se simplifie » ; le rapport des n ; la substitution ; 5,0·10⁻⁵/2,0·10⁻⁴ ; 0,25.
- Autres réécritures :
  - carrés et différences calculés sur leur ligne : K = C·τ²/(1 − τ), n1, n2, n4 (0,10² et 0,20³) ;
  - « solides absents de Qr » : n4 ;
  - « Qr s'inverse, donc K' = 1/K » : n5 ;
  - origine de [AH] = C(1 − τ) : k5.

### phys_ch13_acides_bases — 42 relues, 39 réécrites (29 + 10)
- **ab_k2_puissance f0**
  - Avant : `K = Ka₁/Ka₂ = 10^(pKa₂ − pKa₁)`, posé directement.
  - Après : l'expression de K ; × [H₃O⁺]/[H₃O⁺], donc Ka₁/Ka₂ ; Ka = 10^(−pKa) ; la substitution ; 10^(−1,04) ; 9,1·10⁻².
- **ab_n3_2022n q**
  - Avant : `% AH = 1/(1 + 0,316)`, sans dire d'où vient la formule.
  - Après : % AH = [AH]/([AH] + [A⁻]) = 1/(1 + [A⁻]/[AH]) ; 1/1,316 ; 76 %.
- Autres réécritures :
  - [HO⁻] = Ke/[H₃O⁺] établi à partir de Ke : w4, w5 ;
  - τ d'une base avec son équation : b2, b3 ;
  - K = Ka/Ke expliqué, avec H₂O(l) absente de K : k3, k4, n1 ;
  - « à l'équivalence, n(acide) = n(base) » ajouté à tous les dosages ;
  - demi-équivalence justifiée par log 1 = 0 : e2 ;
  - log 0,1 = −1 et log 0,25 = −0,6 sur leur ligne : p1, n4 ;
  - dilution × 100 et × 10 : e4, n5.

### Démonstrations douteuses
- **ee_k2_produits f0 (et ee_s2_b2)** : avec les valeurs arrondies, (2,75·10⁻⁴)²/4,72·10⁻³ = 1,60·10⁻⁵, alors que l'option juste dit 1,61·10⁻⁵. On obtient 1,61 seulement avec 10^(−3,56) non arrondi. La démonstration écrit « ≈ 1,6·10⁻⁵ (1,61·10⁻⁵ avec [H₃O⁺]éq non arrondie) ». `correct` n'a pas été changé.
- **Démonstrations qui ne répondaient pas à la question** (corrigé) :
  - ci_g3_formule q et td_c3_calcul q : la question demandait une unité, la démonstration donnait un calcul ;
  - ci_n6_sigma f0 et ci_n7_conductance q : elles ajoutaient une lecture de t₁/₂ qui n'était pas demandée.
- **Toutes les autres valeurs** ont été recalculées en Python : chaque démonstration aboutit à l'option `correct`.

### Pistes voix à enregistrer (`demonstration.parole`, audio retiré)
- ch10 : ci_z4_equation/q, ci_m3_titrage/f0, ci_a1b_en_cours/q, ci_a2_limitant/f0, ci_a6_composition/f0, ci_a6_composition/f1, ci_g3_formule/q, ci_g6_calcul/f0, ci_p2_relation/q, ci_p2_relation/e0, ci_p4_2016R/f1, ci_v4_bareme/e0, ci_v4_bareme/f0, ci_h4_comparer/f0, ci_n1_aspirine/q, ci_n1_aspirine/e0, ci_n1_aspirine/f0, ci_n2_diminue/f0, ci_n3_deux/f0, ci_n4_reactif/f1, ci_n6_sigma/f0, ci_n7_conductance/q, ci_n8_trempe/f0, ci_r2_unites/f0. Blocs : ci_s1_b2, ci_s1_b3, ci_s2_b1, ci_s2_b2, ci_s2_b3, ci_s3_b1, ci_s3_b3, ci_s4_b1, ci_s4_b2, ci_s4_b3.
- ch11 : td_p6_totale/f0, td_a3_xf/q, td_a3_xf/e0, td_a5_totale/f0, td_a6_relation/f0, td_e6_national/f0, td_c3_calcul/q, td_c3_calcul/e0, td_d1b_mesures/q, td_n1_figure/f0, td_n2_conductivite/q, td_n3_proportion/f1. Blocs : td_s1_b3, td_s2_b1, td_s2_b2, td_s2_b3, td_s3_b1, td_s3_b2, td_s3_b3.
- ch12 : ee_r1_taux/f0, ee_q5_sans_unite/f0, ee_i2_melange/q, ee_i2_melange/e0, ee_e1_concentrations/f0, ee_k2_produits/f0, ee_k5_tau/q, ee_m1_methanoique/f0, ee_m4_national/q, ee_m4_national/e0, ee_f4_bilan/f0, ee_n1_national/f0, ee_n2_base/f0, ee_n3_melange/q, ee_n3_melange/e0, ee_n4_pile/f0, ee_n5_courbe/f0, ee_n6_taux/f0. Blocs : ee_s1_b1, ee_s1_b3, ee_s2_b1, ee_s2_b2, ee_s2_b3, ee_s3_b1, ee_s3_b2, ee_s3_b3.
- ch13 : ab_w4_ho/q, ab_w4_ho/e0, ab_w5_soude/f0, ab_b2_taux/f0, ab_b3_national/q, ab_b3_national/e0, ab_a3_mesure/q, ab_a3_mesure/e0, ab_a4_ammonium/f0, ab_c3_classement/e0, ab_k2_puissance/f0, ab_k2_puissance/f1, ab_k3_totale/f0, ab_k4_national/q, ab_k4_national/f0, ab_p1_relation/f0, ab_p4_national/e0, ab_d3_equivalence/f0, ab_d6_derivee/e0, ab_e2_demi/f0, ab_e4_base/f0, ab_e5_conductimetrie/f0, ab_n1_2016n/f0, ab_n2_2022r/f0, ab_n2_2022r/f1, ab_n3_2022n/q, ab_n3_2022n/e0, ab_n4_2024r/f0, ab_n5_2023r/f0. Blocs : ab_s1_b2, ab_s1_b3, ab_s2_b1, ab_s2_b2, ab_s2_b3, ab_s3_b1, ab_s3_b3, ab_s4_b1, ab_s4_b2, ab_s4_b3.
- 34 de ces démonstrations avaient un audio, qui a été retiré : 9 en ch10, 6 en ch11, 7 en ch12 et 12 en ch13. Les autres n'avaient pas encore de voix.

### Vérifications faites
- `json.load` réussit sur les 4 copies (indent 2, ensure_ascii=False, fins de ligne LF, retour à la ligne final comme les originaux). La copie a été relue juste avant chaque écriture.
- Aucune différence avec le cours en ligne en dehors des `demonstration`.
- Chaque `mot` de `demonstration.lignes` se trouve dans sa parole, dans l'ordre ; chaque `mot` de pointage et de centre se trouve dans `speech_text.mixed` : 0 erreur.
- Aucune démonstration ne dépasse 8 lignes.
- Les paroles sans audio ne contiennent ni chiffre, ni symbole, ni tachkil ; « يلا » est écrit à la place de « إلا ».
- Chaque diapo est dans exactement un bloc et tous les `competence_ids` existent : 0 erreur sur les 4 cours.
- Aucune notion d'un chapitre suivant : ni équilibre ni K en ch10, ni Qr ni K en ch11, ni Ka ni Ke en ch12. Le mot « dissociation », hors cadre, est remplacé par « dissolution ».
- Scripts : `scratchpad/corr/chim/` (ch10.py à ch13.py, engine.py, verif.py, journaux *.log.json).
