## Limites et continuité

Copie en attente : `backend/data/courses/en_attente/math_ch1_limites_continuite.json` (partie du cours en ligne, aucune copie en attente n'existait). Le cours en ligne n'a pas été touché. 75 → 77 diapos.

### Manques corrigés

| Constat | Ce qui a été fait | Diapo(s) |
|---|---|---|
| Continuité à droite / à gauche + propriété « continue ⇔ à droite et à gauche » (haute) | Nouvelle diapo : les 2 définitions (avec [a ; a + r[ et ]a − r ; a]), la propriété, l'exemple m = 3 (continue à droite, pas à gauche), « de a » = « en a ». Rédaction : ① « donc f est continue à droite en 1 », ② « … à gauche en 1 » | **lc_c4b_droite_gauche** (nouvelle, K2, bloc lc_s3_b1), lc_c5_redaction, lc_e2_bilan, lc_e3_carte |
| Tableau des limites usuelles (haute, en partie) | Nouvelle diapo-tableau : xⁿ en +∞, en −∞ selon la parité de n, 1/xⁿ en ±∞, √x en +∞. 1/x en 0⁺ / 0⁻ ajouté là où 0⁺ est enseigné | **lc_l4c_usuelles** (nouvelle, K1, bloc lc_s1_b2), lc_l10_signe, lc_e2_bilan |
| Opérations ℓ × ∞, ∞ / ℓ (haute) | Règle des signes écrite et dite, exemple lim (−2x³) en −∞ | lc_l4c_usuelles, bloc lc_s1_b2 |
| « Dans un repère orthonormé » + « première bissectrice » | Écrit sur l'écran et au cahier (verdict « à revoir » chez les autres profs, gardé car la règle 38 l'exige) | lc_r6_miroir, lc_r7_construire, lc_e1_probleme_c, lc_e2_bilan, lc_e3_carte, bloc lc_s5_b3 |
| Unicité de f(x) = k, k ∈ f(I) (haute, cadre 1.2.4 « λ ») | Cas général écrit, exemple x³ + x − 1 = 1 | lc_t8_intervalle_ouvert, lc_e2_bilan, bloc lc_s4_b3 |
| « I ouvert contenant a » (moyenne) | Ajouté à la définition | lc_c2_limite_image, bloc lc_s2_b3 |
| Continue sur ]a ; b[ / [a ; b] (moyenne) | Puce + cahier | lc_i1_usuelles, bloc lc_s3_b1 |
| Exercice « D_f puis ensemble de continuité » (moyenne) | Exercice de fin g(x) = (2x + 1)/(x − 1) + cos x, démonstration et réactions | lc_i2_operations (fin de cours e0) |
| Image d'un segment = segment, d'un intervalle = intervalle (moyenne, cadre 1.2.2) | Propriété (admise) écrite | lc_j5_non_monotone, lc_e2_bilan, bloc lc_s4_b1 |
| Tableau des images (moyenne) | Cas [a ; b[, ]a ; b], [a ; +∞[ croissante et décroissante au cahier | lc_j4_borne_ouverte, bloc lc_s4_b1 |
| lim tan x / x = 1, lim (1 − cos x)/x² = 1/2 (moyenne) | Puce + cahier | lc_l12_sinus, bloc lc_s2_b2 |
| f⁻¹(f(x)) = x sur I, f(f⁻¹(x)) = x sur J (moyenne) | Puce + cahier (sous la forme aller / retour) | lc_r3_J, lc_e2_bilan, bloc lc_s5_b2 |
| a³ + b³ (moyenne) | Puce + cahier, exemple x³ + 8 (pas ∛ d'un négatif) | lc_lr2_cle_de_trois, lc_e2_bilan, bloc lc_s7_b2 |
| Limite avec valeur absolue à droite / à gauche (basse → moyenne) | Exercice de fin (x² − 1)/\|x − 1\| en 1, démonstration et réactions | lc_c3_deux_branches (fin de cours e0) |
| Continuité de \|x\|, tan, αf (basse) | Puces + cahier | lc_i1_usuelles, lc_i2_operations |
| ⁿ√x = ⁿ√y ⇔ x = y ; ¹√x = x ; n ∈ ℕ* (basse) | Puces + cahier | lc_n2_reciproque_xn, lc_n3_regles, bloc lc_s6_b2 |
| x^(p/q) avec p ∈ ℤ, q ∈ ℕ* ; 1/x^r = x^(−r) (basse) | Puces + cahier | lc_p2_pq, lc_p3_regles_puissances, bloc lc_s7_b1 |
| Oral seulement : « jamais un nombre sur 0 sans le signe » | Écrit à l'écran et au cahier | lc_l10_signe, bloc lc_s2_b1 |
| Notation x → a sous lim | `lim_{x→a}` dans les cahiers, traces, puces et formules du centre (≈ 30 champs) | lc_l1, l2, l5, l6, l7, l10, l11, l12, l12_b, c2, c5, i4, j4, lr1, lr3, e1_b, e2, e3 + blocs |
| Quantificateur ∀ dans les conditions | (∀x ∈ I) v(x) ≠ 0, (∀x ∈ I) u(x) ≥ 0 | lc_i2, lc_i3, lc_r3, lc_e2_bilan, blocs lc_s3_b2, lc_s7_b2 |
| « car… » (règle 38, « par où commencer ») | « continue car polynôme », « strictement croissante car f′ > 0 », exemples du cahier sans étape sautée (l5, l6, i3) | lc_t6_rediger, lc_r4_deux_lignes, lc_e1_probleme_b, lc_l5, lc_l6, lc_i3, blocs |

### Non corrigés et pourquoi

- Propres au Prof Fayssal, pas exigés par le cadre (1.2.1–1.2.4, 1.2.11, 1.2.22) : comparaison et encadrement, signe du trinôme, f′ ≥ 0 nulle en des points isolés, indice commun pour ∞/∞, équations avec ⁿ√ (puissance 6), nombre de solutions lu sur un tableau, TVI trigonométrique, X = x − 1, monotonie sans dériver.
- lc_r8 (« c'est f de y, pas f de x ») : verdict « à revoir », pas « confirmé » ; corriger demande de changer la voix. L'écran dit déjà « x ∈ J, y ∈ I ».
- Sens de l'asymptote (oral lc_l11) : pas chez les autres profs.
- Nouvelles pistes : aucune haute pour ce chapitre ; les 4 moyennes (composée g∘f, limite d'une composée, outil pour 0 × ∞, « il existe un unique α ») et les 6 basses ne sont pas faites.
- À signaler : la simulation de lc_r4 écrit « g′(x) = 2x − 2 ≥ 0 : strictement croissante » sans la règle des zéros isolés. Les simulations `bilan.html` (fiche) et `calculs.html?vue=c5_redaction` n'ont pas les ajouts : ce sont des fichiers du frontend, non modifiés.
- Puces ajoutées sans changer la voix (consigne) : lc_l12 (tan, cos), lc_t8 (k), lc_r3 (f⁻¹(f(x))), lc_lr2 (a³ + b³), lc_i1, lc_j4, lc_j5. La voix ne les dit pas : **à décider** s'il faut revoicer ces diapos.
- La nouvelle diapo lc_l4c_usuelles n'a pas de simulation (aucune vue existante ne convient) : c'est un tableau, `visual.kind = none`.
- L'exercice du bloc lc_s7_b4 (QCM sur le TVI) n'a pas de démonstration, comme avant.

### Démonstrations

- **27 relues**, dont 18 sur les diapos et 9 dans les blocs. **23 réécrites**, 4 gardées car déjà complètes : lc_i4 (question), lc_j3 (question), lc_p3 (question), bloc lc_s2_b3. Les lignes et la parole ont été réécrites, et l'audio retiré.
- 4 copies dans les blocs n'avaient pas de démonstration ; elles reçoivent maintenant la nouvelle : lc_s1_b3, lc_s2_b2, lc_s7_b2, lc_s7_b3. Les 2 nouveaux exercices ont aussi leur démonstration. Tous les calculs ont été vérifiés avec sympy.
- Exemples :
  - lc_n7 : « 2x³ + 11 = 27 ; x³ = 8, x = 2 ; vérif. » → condition, ⇔ 2x³ + 11 = 27, ⇔ 2x³ = 16, ⇔ x³ = 8, ⇔ x = ∛8 = 2 (3 impair, 8 > 0), vérification, « Donc la solution est x = 2 ».
  - bloc lc_s3_b2 : « 4 − 2x ≥ 0 ⇔ x ≤ 2 » → ⇔ −2x ≥ −4, ⇔ x ≤ 2 (on divise par −2 < 0 : le sens change), puis la conclusion sur la continuité.
  - lc_lr4 : « = x(∛(1/x − 1/x²) − 1) ; → −1 ; −∞ » → x² − x = x³(1/x − 1/x²), ∛(x³) = x, la limite de chaque facteur, (+∞) × (−1) = −∞, puis la phrase de conclusion.

### Voix à enregistrer

- **Diapos nouvelles** (`speech_text.mixed`) : lc_l4c_usuelles, lc_c4b_droite_gauche. Aucune voix de diapo existante n'a changé.
- **Démonstrations** (parole) :
  - questions : lc_z5_racine_facteur, lc_l7_plus_lourd, lc_l10_signe, lc_l13_devoir, lc_t9_f_alpha, lc_n1_defaire, lc_n4_simplifier, lc_n7_equation_racine, lc_lr4_infini, lc_e1_probleme ;
  - exercices de diapo : lc_l13_devoir ex 0, lc_e1_probleme ex 0 ;
  - exercices de fin de cours : lc_l5_facteur e0, lc_l13_devoir e0, lc_lr3_zero_sur_zero e0 ;
  - exercices de bloc : lc_s0_b2, lc_s1_b3, lc_s2_b2, lc_s3_b2, lc_s3_b3, lc_s4_b3, lc_s6_b1, lc_s6_b2, lc_s6_b3, lc_s7_b1, lc_s7_b2, lc_s7_b3.
- **Nouveaux exercices de fin de cours** (enonce_dit, démonstration, réactions juste / 0.1 / 0.2 / 2.1 / 2.2) : lc_i2_operations e0, lc_c3_deux_branches e0.

### Vérifications faites

- `json.load` : OK. Fins de ligne LF (0 CR).
- Chaque `mot` des démonstrations est trouvé dans sa parole, dans l'ordre. Chaque `mot` de pointage et de centre est trouvé dans `speech_text.mixed`. Aucun chiffre dans les voix nouvelles, les paroles ni les réactions : 0 erreur.
- Chaque diapo est dans exactement un bloc, et l'ordre des blocs est celui du cours. Chaque competence_id existe (K1 et K2 complétées). Chaque exercice ajouté a ses réactions pour toutes les options.
- `verifier_figures_cahier.py` : 11 figures, 0 erreur, 0 avertissement.
- sympy : (x − 2)(x − 3), limites 3, 3, −∞, 1/2, 4, 2, 1/4, 1/3, −∞, tan x/x → 1, (1 − cos x)/x² → 1/2, ±2 avec |x − 1|, x = 2, 27^(2/3) = 9, ⁸√81 = √3, f(1/2) = −3/8 : tout est juste.
