## Physique ch1 à ch5 — démonstrations

Copies en attente écrites dans `backend/data/courses/en_attente/` (cours en ligne non touchés). Seuls les objets `demonstration` ont changé (vérifié par comparaison). Les cours en ligne servent de base pour ch2 à ch5. Pour ch1, la base est la copie en attente qui existait déjà, qui contient 22 diapos.

Règle appliquée : la relation avec ses conditions, une conversion par ligne, la substitution, chaque calcul intermédiaire, puis le résultat avec son unité et une conclusion qui répond à la question. Une démonstration déjà complète est restée telle quelle.

Les exemples sur les diapos (bullets, centre, student_trace) et au cahier ont été relus. Ce sont des récapitulatifs en une ligne (relation = substitution = résultat), dont l'exercice a sa propre démonstration complète. Ils n'ont **pas** été modifiés, pour ne pas toucher aux voix enregistrées ni au pointage.

### phys_ch1_waves_exemple — 4 relues, 1 réécrite
- wx_s2_b1b : `d = v·τ/2 → 1500 × 0,04/2 → 30 m` → `2d = v·τ (aller et retour) → d = v·τ/2 → (1500 × 0,04)/2 → 60/2 → 30 m`.
- Démonstrations gardées : wx_p2_milli, wx_s1_b3, wx_s2_b1.

### phys_ch2_ondes_periodiques — 26 relues, 16 réécrites
- op_c4_photo_datee : `t = 2,5 T → T = 50/2,5` → ajout de `T = t/2,5` avant la substitution.
- op_x2_national_2020 (q) : `2λ = 1 cm, donc λ = 0,5 cm = 0,5 × 10⁻² m` en une ligne → 2λ = 1 cm ; λ = 1/2 = 0,5 cm ; conversion ; N = v/λ ; substitution ; 50 Hz ; puis « λ = 0,5 cm et N = 50 Hz ».
- Autres : op_p3 (règle entier / entier et demi), op_p4 (k ∈ ℕ, puis 5 × 2/2), op_m6b (d = n·λ), op_d3 (condition a ≤ λ), op_r3_trois_lectures, op_r3b (q, e0), op_x1, op_x2 e0, op_x3 (q, e0, f0), blocs op_s2_b2 et op_s4_b3 : les conversions sont sur leur propre ligne et la substitution est séparée du résultat.

### phys_ch3_ondes_lumineuses — 17 relues, 14 réécrites
- ol_s2_b2 : `L = 2 × 6,5·10⁻⁷ × 2 / 10⁻⁴ → 2,6·10⁻² m = 2,6 cm` → conversions de λ et de a sur leurs lignes, puis (2 × 6,5·10⁻⁷ × 2)/10⁻⁴ ; 2,6·10⁻² m ; 2,6 cm.
- ol_s3_b1 : `λ₂ = L₂·λ₁/L₁` sans justification → « même a, même D : L proportionnelle à λ » ; L₂/L₁ = λ₂/λ₁ ; puis le calcul.
- Autres : ol_l1 (650 = 6,5 × 10², exposants), ol_l8 (1 m = 10⁹ nm, domaine du visible), ol_g5 et ol_s3_b2 (identification), ol_x2 f2 et ol_s4_b2 (« ν ne change pas »), ol_x3 et ol_s1_b3 (conversions).
- **Lignes seules, voix inchangée et audio gardé** : ol_p1_radian, ol_t4_relation, ol_p2_tangente, ol_c2b_en_bas. La voix disait déjà chaque étape.

### phys_ch4_radioactivite — 19 relues, 13 réécrites
- ra_c4b_rapport : `r = 1 ⇒ e^(λt) = 2` → N(père) = N₀·e^(−λt) ; N(fils) = N₀ − N(père) ; r = e^(λt) − 1 ; e^(λt) = 2 ; λt = ln 2 ; t = ln 2/λ = t½.
- ra_s3_b1 : `238 = 206 + 4y ⇒ y = 8` → l'équation avec x et y ; conservation de A ; 4y = 32 ; conservation de Z ; 92 = 82 + 16 − x ; x = 6 ; conclusion.
- Autres : ra_t3 (« il reste 1/8 »), ra_a5 (2 µg = 2·10⁻⁶ g), ra_x2 et ra_x3 (de la loi jusqu'à t = (t½/ln2)·ln(N₀/N), avec le calcul intermédiaire), ra_x3 e0, ra_s2_b2 et ra_s2_b3 (équation avec ᴬ_ZX, puis identification du noyau fils), ra_x4, ra_s1_b1, ra_s4_b2 (N/N₀ = 0,125), ra_s5_b3.

### phys_ch5_energie_nucleaire — 15 relues, 13 réécrites
- en_d4_carbone : `Δm = 6 × 1,00728 + 8 × 1,00866 − 13,99995 → 0,11301 u` → ajout de `6,04368 + 8,06928 − 13,99995` puis de `14,11296 − 13,99995`.
- en_e4_polonium e0 : `Δm = 1644,8/931,5 = 1,7658 u` → Δm = E_ℓ/c² ; Δm = 1644,8 MeV/c² ; conversion u ; conversion kg.
- Autres : en_m4_931, en_l3_calcul et en_s1_b3 (1 u·c² = 931,5 MeV écrit) ; en_l4_par_nucleon (9 lignes, une seule démonstration possible par question) ; en_s2_piege et en_a3_comparer (règle de stabilité, substitution puis résultat) ; en_b5_beta (q, e0) ; en_e4_polonium q ; en_c2_qcm2019 ; en_n3_2025 e0.

### Démonstrations douteuses
- **en_n3_2025 e0 (erreur)** : 4,7·10²³ × 1,6·10⁻¹³ = 7,52·10¹⁰ J, pas 7,6·10¹⁰ J. La démonstration dit maintenant 7,5·10¹⁰ J. Elle explique ensuite que la valeur non arrondie (2,56·10²¹ × 185 = 4,74·10²³ MeV) donne 7,6·10¹⁰ J. `correct` (0) n'a pas été changé. Il faudrait plutôt corriger le texte de l'option et la réaction juste (7,6 → 7,5), ou bien donner 4,74·10²³ MeV dans l'énoncé.
- Tous les autres calculs ont été vérifiés en Python et donnent la réponse de `correct`.
- Hors démonstrations, sans changement : ch3 `ol_b1_bilan` et `ol_b2_carte` ne sont dans aucun bloc (c'est déjà le cas dans le cours en ligne). Plusieurs démonstrations gardées écrivent encore `a / b` avec des espaces, donc la barre n'est pas empilée (ex. wx_s2_b1, op_t4).
- La copie en attente ch1 date du 16/11 00:59. Le cours en ligne a changé ensuite (21:07), par exemple `concentration` de wx_b2_national. Ce n'est pas fusionné ici.

### Voix à enregistrer (`demonstration.parole`, audio retiré)
- ch1 : wx_s2_b1b (bloc).
- ch2 : op_c4_photo_datee/q, op_p3_methode/f0, op_p4_troisieme/q, op_m6b_deja_ecartes/q, op_d3_justifier/q, op_r3_trois_lectures/f0, op_r3b_calculs/q, op_x1_national_2017/f0, op_x2_national_2020/q, op_x2_national_2020/e0, op_x3_devoir/q, op_x3_devoir/e0, op_x3_devoir/f0, op_s2_b2 (bloc), op_s4_b3 (bloc). op_r3b_calculs/e0 n'a changé que ses lignes et garde son audio.
- ch3 : ol_l1_metre/f0, ol_l8_ordre_grandeur/q, ol_g5_autres/q, ol_x2_national_2023/f2, ol_x3_national_2021/f0, ol_s1_b3, ol_s2_b2, ol_s3_b1, ol_s3_b2, ol_s4_b2 (blocs).
- ch4 : ra_t3_paliers/q, ra_a5_masse/q, ra_c4b_rapport/q, ra_x2_2021N/f0, ra_x3_2022N/q, ra_x3_2022N/e0, ra_x4_2025N/q, ra_s1_b1, ra_s2_b2, ra_s2_b3, ra_s3_b1, ra_s4_b2, ra_s5_b3 (blocs).
- ch5 : en_m4_931/q, en_d4_carbone/q, en_l3_calcul/q, en_l4_par_nucleon/f0, en_s2_piege/q, en_a3_comparer/q, en_b5_beta/q, en_b5_beta/e0, en_e4_polonium/q, en_e4_polonium/e0, en_n3_2025/e0, en_c2_qcm2019/q, en_s1_b3 (bloc).

### Vérifications faites
- `json.load` réussit sur les 5 copies (LF, indent 2, ensure_ascii=False, retour à la ligne final comme les originaux).
- Chaque `mot` de chaque `demonstration.lignes` se trouve dans sa parole, et dans l'ordre (première occurrence croissante) ; chaque `mot` de pointage et de centre se trouve dans `speech_text.mixed` : 0 erreur.
- Aucun chiffre ni symbole dans les nouvelles paroles (darija + termes, nombres et unités en mots français).
- Chaque diapo est dans exactement un bloc et chaque competence_id existe : 0 erreur, sauf les 2 diapos de bilan de ch3 déjà hors bloc en ligne.
- Comparaison avant / après : rien d'autre que les `demonstration` n'a changé. `verifier_figures_cahier.py` n'a pas été lancé (il est réservé aux maths).
- Scripts : `scratchpad/p15/apply.py` (modifications) et `scratchpad/p15/verif.py`.
