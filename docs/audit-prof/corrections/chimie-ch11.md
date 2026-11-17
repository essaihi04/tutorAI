## Transformations chimiques s’effectuant dans les deux sens

Fichier modifié : `backend/data/courses/en_attente/phys_ch11_transformations_deux_sens.json` (copie en attente, partie de la version du matin ; le cours en ligne n’est pas touché). 42 → 44 diapos.

### Manques corrigés

| Constat (audit) | Ce qui a été fait | Diapo(s) |
|---|---|---|
| H1 Définitions totale (x_f = x_max) / limitée (x_f < x_max) absentes | Écran : deux puces (disparition d’un réactif ou non, x_f/x_max, τ) ; cahier ; bloc ; voix complétée et relue ; 2 entrées centre. a3 : « x_f < x_max » écrit | td_a4_taux, td_a3_xf, td_s2_b1 |
| H2 « sens direct / sens inverse » jamais écrit | Écrit partout « sens direct (1) / sens inverse (2) » (écran, cahier, légendes, blocs, retrouver, rappel C4_r1, réactions) ; nouvelle diapo qui les nomme | td_e1_inverse, td_e1b_direct (nouvelle), td_e2_fleche, td_e4_dynamique, td_s2_b2, td_s2_b3, C4 |
| H3 σ jamais écrite en fonction de x_f et V | Preuve en 6 lignes (une entrée centre par ligne) : σ = Σλᵢ[Xᵢ] → … → σ = (λ₁ + λ₂)·x_f/V → x_f = σ·V/(λ₁ + λ₂) ; voix réécrite ; cahier, bloc, retrouver | td_c2_relation, td_s3_b1 |
| H États physiques manquants (7 champs) | (aq)/(l) ajoutés : cahier couple et bloc, explication b4, réaction C1_r4, p5 « B(aq) », b1 « H⁺(aq) », e1 « Na⁺(aq) + CH₃COO⁻(aq) », n4 « R–NH₂(aq) » ; formules ASCII (H3O+, H2O / HO-, NH4+ / NH3, C6H5COOH, 10^-x, tau2, x max…) remises en notation du bac dans 73 champs écrits | td_b3_couple, td_s1_b1, td_b4_reaction, C1, td_p5_ammoniac, td_b1_acide, td_e1_inverse, td_n4b_calcul, réactions de 15 diapos |
| M Bécher A : ajout d’acide pur, pH baisse → sens direct | Nouvelle diapo (sans question) : expérience, équation dans le sens direct, rappel de l’exemple E (sens inverse), relecture | td_e1b_direct (bloc td_s2_b2, C4) |
| M v₁ diminue, v₂ augmente jusqu’à v₁ = v₂ | Puce + cahier + voix + entrée centre « v₁ = v₂ » | td_e4_dynamique, td_s2_b3 |
| M Condition du pH ([H₃O⁺] ≤ 5·10⁻² mol/L, valeur en mol/L) | Écran, cahier, bloc, fiche bilan | td_p1_ph, td_s1_b2, td_bl_fiche |
| M Ampholyte | Puce, cahier, bloc, voix (« ampholyte » + relecture), centre ; « amphotère » remplacé dans les réactions écrites | td_b3b_eau, td_s1_b1, td_p5_ammoniac |
| M n₀ par la densité (1 mL d’acide pur) | Exercice de fin de cours avec démonstration (6 lignes) et réactions préparées (juste / faux 1 / faux 2) | td_a2_xmax |
| M pH-mètre : électrode + voltmètre | Puce, cahier, bloc, une phrase de voix | td_p3_phmetre, td_s1_b3 |
| B Papier pH ; échelle 0–14 ; aA + bB ⇌ cC + dD ; solution aqueuse ; règles du log | Ajouts écrits (écran/cahier/bloc) | td_p3_phmetre, td_p1_ph, td_e2_fleche, td_z2_concentration, td_z3_puissance, td_r_b2 |
| B pH à partir de σ | Exercice de fin de cours (x_f = σV/(λ₁+λ₂), [H₃O⁺], pH) avec démonstration 8 lignes et réactions | td_c3_calcul |
| Oral seulement | Écrit : HO⁻ négligés « car la solution est acide » (c2) ; double flèche « car A⁻ peut reprendre H⁺ » (b3) ; « l’eau est en excès, donc l’acide est le réactif limitant » (a2) ; but du rinçage (p3) ; chocs efficaces au cahier de la diapo (e4) ; n4 détaillé | td_c2, td_b3_couple, td_a2_xmax, td_p3, td_e4, td_n4 |
| Notations recommandées | « final = équilibre » écrit (x_f = x_éq, [X]_f = [X]_éq) ; étalonnage « 4,0 puis 7,0 ; basique 7,0 et 9,0 » ; substitutions ajoutées (n₀ = C·V, x_max, x_f de l’exemple B, n(CH₃COOH)_éq) | td_e3_etat, td_s2_b3, td_p3, td_a1, td_a5, td_e3 |
| Erreur trouvée en relisant | Fiche bilan : la formule « τ = 10^(−pH)/C » s’écrivait au mot du pH (avant le bloc τ) ; remplacée par « τ = 1 : totale ; τ < 1 : limitée », sur son mot | td_bl_fiche |

### Non corrigés et pourquoi

- Les 5 manques chez un seul professeur (mélange HCOOH + éthanoate avec Na⁺, HCO₃⁻, convention H⁺ → H₃O⁺, grandeurs observables constantes, « σ se mesure à l’état final ») : non exigés par le cadre.
- Les simulations écrivent encore « sens 1 / sens 2 » (equilibre.html, bilan, carte) : pas de modification de simulation autorisée. L’écran du cours dit « sens direct (1) ».
- td_e1b_direct réutilise la vue `equilibre.html?vue=double_fleche` (sens_1 puis sens_2) : aucune vue ne montre l’ajout d’acide pur (bécher A). Il faudrait une nouvelle vue si on veut l’animation.
- Les voix de td_e1_inverse et td_e2_fleche disent toujours « le sens un / le sens deux » (gardées pour ne pas refaire leurs pistes) ; td_e1b_direct et td_e4 disent « le sens direct, le sens un ».
- Blocs td_s2_b2 et td_s3_b3 : 5 diapos (une nouvelle diapo chacun), toujours un seul tableau « À toi ».
- Réactions préparées (≈ 150) : notations et états corrigés dans `ecrit`, pas réécrites en démonstrations complètes ; deux `parole` disent encore « amphotère ».
- td_n1_figure : C₁ = 1,58·10⁻² mol/L garde 3 chiffres alors que τ ≈ 0,10 est lu à 2 chiffres (repris du corrigé du national) — à décider.

### Démonstrations

Relues : toutes (25 démonstrations de questions/exercices/blocs, preuves et calculs écrits des diapos, cahiers, bilan). Réécrites ou nouvelles : 10 démonstrations (td_a6 e0 + bloc td_s2_b2, td_n3 e1 + bloc td_s3_b3, td_c3 question, td_n2 question, td_n2 exercice, td_a2 e0 nouveau, td_c3 e0 nouveau) ; 5 preuves de diapo passées en une entrée centre par ligne (td_c2 6 lignes, td_c3 8, td_n3 8, td_n4 6 + td_n4b 8) ; lignes 0 de td_a3 (3 copies) et ligne 6 de td_c3 e0 (2 copies) avec leur « car ». Déjà complètes, gardées : td_p2, td_p6, td_a3, td_a5, td_e5, td_e6, td_d1b, td_n1, td_c3 e0.

- td_n4_dosage : « x_f = C_A·V_A − 10^(−pH)·(V_A + V_B) = 7,2·10⁻⁴ mol » d’un coup → méthode en 6 lignes (équation, état initial, n(H₃O⁺)_f = C_A·V_A − x_f, n(H₃O⁺)_f = 10^(−pH)·(V_A + V_B), x_f, limitant car C_A·V_A < C_B·V_B) puis td_n4b_calcul en 8 lignes (conversions, 1,6·10⁻¹² mol négligeable, x_max, τ = 1).
- td_a6 e0 : « τ = x_f/x_max = [H₃O⁺]_éq·V/(C·V) = 10^(−pH)/C » en une ligne → définition avec x_f et x_max, puis « V se simplifie », puis [H₃O⁺]_éq = 10^(−pH), puis l’application numérique.
- td_n2 question : « [H₃O⁺] = σ/(λ₁ + λ₂) » parachuté → σ = λ₁[H₃O⁺] + λ₂[C₆H₅COO⁻], [C₆H₅COO⁻] = [H₃O⁺] = x_f/V, x_f = σV/(λ₁ + λ₂), τ = σ/(C(λ₁ + λ₂)), conversion de C, somme des λ, τ ≈ 0,22 < 1.

### Voix à enregistrer (id)

- Diapos (audio retiré ou nouvelles) : td_b3b_eau, td_p3_phmetre, td_a4_taux, td_e1b_direct (nouvelle), td_e4_dynamique, td_c2_relation, td_c3_calcul, td_n3_proportion, td_n4_dosage, td_n4b_calcul (nouvelle).
- Démonstrations (parole nouvelle, sans audio) : td_a6_relation e0 (+ bloc td_s2_b2), td_n3_proportion e1 (+ bloc td_s3_b3), td_c3_calcul question, td_n2_conductivite question et exercises[0], td_a2_xmax e0, td_c3_calcul e0.
- Énoncés (`enonce_dit`, pas d’`enonce_audio`) : td_a2_xmax e0, td_c3_calcul e0.
- Réactions préparées nouvelles : td_a2_xmax `reponses_fin_de_cours.e0` (0.1, 0.2, 1.juste, 2.1, 2.2) et td_c3_calcul `reponses_fin_de_cours.e0` (mêmes clés).

### Vérifications faites

- JSON valide, écrit avec `json.dumps(ensure_ascii=False, indent=2)` + LF ; fichier relu (empreinte comparée) juste avant chaque écriture.
- `verif_attente.py` : 44 diapos, 0 mot absent, 0 hors bloc, 0 doublon, 0 compétence inconnue, 10 diapos sans voix (celles listées).
- Script maison : chaque `mot` de démonstration dans sa parole et dans l’ordre des lignes ; chaque `mot` de centre dans la voix et dans l’ordre ; aucune voix ni parole nouvelle avec chiffre ou symbole ; un seul tableau « À toi » par bloc ; nouvelles diapos avec compétence (C4, C3) et bloc ; moments `sens_1`, `sens_2`, `tableau`, `x_f`, `x_max`, `taux` présents dans les simulations.
- Scan des équations écrites : plus aucune espèce sans état (restent seulement les lettres générales aA + bB ⇌ cC + dD, sans état par règle) ; plus aucune formule ASCII dans les champs écrits.
- `verifier_figures_cahier.py` : 3 figures, 0 erreur.
- Calculs refaits en Python : 10^(−3,41) = 3,89·10⁻⁴, τ = 0,039 ; 35,0 + 4,09 = 39,09 ; 1,56·10⁻²/39,09·10⁻³ = 0,399 ; x_f = 3,99·10⁻⁵ mol, pH = 3,40 (pièges 4,40 et 0,40) ; n₀ = 1,05/60 = 1,75·10⁻² (pièges 1,67·10⁻², 63) ; 8,6·10⁻³/38,23·10⁻³ = 0,225 et ≈ 225 ; 10^(−3,05) = 8,9·10⁻⁴, τ = 0,0178, α = 0,982 ; 10^(−3,1)/5,0·10⁻² = 0,016 ; 4,5·10⁻² × 1,60·10⁻² = 7,2·10⁻⁴, C_B·V_B = 9,0·10⁻⁴, 10^(−10,2) × 2,60·10⁻² = 1,6·10⁻¹².
