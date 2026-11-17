## Oscillations libres d’un circuit RLC série

Fichier modifié : `backend/data/courses/en_attente/phys_ch8_circuit_RLC.json`. Je suis parti de la copie en attente de ce matin et rien n’a été perdu. Le cours en ligne n’a pas été touché.
- Scripts : `scratchpad/ch8/corriger.py`, puis `scratchpad/ch8/fix2024.py`.
- Copie d’avant : `scratchpad/ch8/avant.json`.

### Manques corrigés
| Constat (audit) | Ce qui a été fait | Diapo(s) |
|---|---|---|
| Haute : q(t) et Q_m absents | Nouvelle diapo. On écrit q(t) = C·u_C = C·E·cos(2πt/T₀) = Q_m·cos(2πt/T₀), avec Q_m = C·E (en coulomb ; en général Q_m = C·U_m). C’est aussi ajouté au cahier du bloc et à la fiche. | lc_c5_courant (nouvelle, vue `solution.html?vue=cos` déjà existante), lc_bl_fiche |
| Haute : i(t) jamais établi, pas de formule pour I_m | Même diapo, 8 lignes au centre, une par mot : i = dq/dt = −(2π/T₀)·Q_m·sin(…) ; rappel −sin α = cos(α + π/2) ; i = I_m·cos(2πt/T₀ + π/2) ; I_m = (2π/T₀)·Q_m = E·√(C/L) ; « q maximale ⇔ i = 0 ». Un exercice de fin de cours a été ajouté (I_m ≈ 38 mA), avec sa démonstration, son énoncé dit et 5 réactions préparées. | lc_c5_courant |
| Moyenne : la période de l’échange d’énergie (T₀/2) n’était pas écrite | Écrit à l’écran, au centre, au cahier et dans la voix : u_C(t + T₀/2) = −u_C(t), donc la période de l’échange est T₀/2 = 2 ms | lc_en3_echange |
| Moyenne : vocabulaire « amorties » / « non amorties » | « oscillations libres amorties », « oscillateur électrique libre et amorti » ; « oscillations non amorties » pour le LC idéal ; phrase du bac « pseudo-périodique car l’amplitude diminue » | lc_d4_libres, lc_r1_pseudo, lc_e5_lc_ideal |
| Basse : unités de la solution | U_m en V, T₀ en s, φ en rad (écran et cahier) ; rad aussi en lc_c3 | lc_e6_sinusoide, lc_c3_angles |
| Dit seulement à l’oral : la seule énergie est celle du condensateur | Écrit à l’écran et au cahier | lc_d4_libres |
| Dit seulement à l’oral : « le terme du milieu vide l’énergie » | Écrit : « terme d’amortissement » | lc_k2_k, lc_e5_lc_ideal |
| Dit seulement à l’oral : I_m tiré de l’énergie | Écrit ligne par ligne : I_m = √(2E/L) = √(2 × 7,2·10⁻⁵/0,1) = √(1,44·10⁻³) ≈ 3,8·10⁻² A ; vérifié par I_m = E·√(C/L) (voix réécrite) | lc_en3_echange |
| Démonstration : φ = 0 tiré de « la plus grande valeur possible » | Système des deux conditions initiales : (1) U_m·cos φ = E ; (2) i(0) = −C·(2π/T₀)·U_m·sin φ = 0, donc φ = 0 ou π ; U_m > 0 et E > 0, donc cos φ > 0 et φ = 0 ; U_m = E. 8 lignes au centre, voix réécrite | lc_c1_depart |
| Démonstration : la ligne « on remplace » manquait | q/C + (R + r)·dq/dt + L·d²q/dt² = k·dq/dt, puis on passe k·dq/dt à gauche. La question du début (R = 90 Ω, r = 10 Ω) reçoit maintenant sa réponse k = 100 Ω | lc_k2_k |
| Démonstration : conservation de E vue seulement sur la courbe | Preuve avec cos² + sin² = 1 : E_e = ½·C·E²·cos², E_m = ½·L·I_m²·sin², ½·L·I_m² = ½·C·E², donc E = ½·C·E² = 72 µJ. Elle utilise I_m de lc_c5, déjà vu (règle 27). Voix réécrite | lc_en4_somme |
| Notation R_T | « R + r : résistance totale (notée aussi R_T) » | lc_e2_remplacer |
| Fiche : conditions et formules | Ajoutés : « sans générateur », « convention récepteur », « R + r = 0 », unités de T₀, « T ≈ T₀ si l’amortissement est faible », q(t), Q_m, i(0), I_m, échange en T₀/2, |ΔE| « entre deux sommets (i = 0) » | lc_bl_fiche |

Blocs et compétences :
- lc_c5_courant entre dans le bloc lc_s3_b1, qui a maintenant 5 diapos et s’appelle « Trouver U_m et φ ; q(t) et i(t) ». Une ligne a été ajoutée à son cahier.
- La compétence C4 reçoit lc_c5_courant.

### Non corrigés et pourquoi
- Les manques signalés chez un seul professeur n’ont pas été ajoutés :
  - le tableau q et i à 0, T₀/4… : seule l’idée « quand l’une est maximale, l’autre s’annule » est écrite en lc_c5 ;
  - l’équation différentielle du LC établie par l’énergie ;
  - « le LC idéal est difficile à réaliser » ;
  - l’exercice E_m = (CU²/4)(1 − cos 4πt/T₀).
- Hors cadre : « quadrature » et « déphasage » ne sont jamais écrits.
- Pas de nouvelle simulation. lc_c5 réutilise la vue `cos` de solution.html, qui trace déjà u_C et i. La courbe q(t) n’est pas dessinée : q = C·u_C a la même forme.
- **À décider** :
  - lc_p4_national montre maintenant le calcul complet de L, et son exercice (2022 N 2.1.3, aussi exercice de bloc) demande ce même calcul. C’était déjà le cas, mais seul le résultat était donné.
  - Même situation pour lc_e8_T0 et l’exercice de bloc lc_s2_b2 (T₀ = 4 ms).
- Trois diapos qui reprennent un sujet entier ont 9 entrées au centre (lc_e8, lc_n1, lc_n2). C’est un peu plus que 8. Je ne les ai pas coupées en deux diapos, pour ne pas alourdir le cours.
- Les réactions préparées existantes n’ont pas été réécrites : l’audit n’y signale pas d’erreur.

### Démonstrations
**Relues :**
- les 47 démonstrations : questions, exercices, exercices de fin de cours, exercices de bloc ;
- toutes les preuves écrites sur une diapo (centre, puces, cahier) et la fiche.

**Réécrites ou complétées : 28.**

*Preuves sur diapo, une entrée du centre par ligne (27) :*
- avec la voix inchangée (16) :
  - lc_d6, lc_r4 ;
  - lc_e2, lc_e3, lc_e4, lc_e7 ;
  - lc_p1, lc_p3 ;
  - lc_c3, lc_c4 ;
  - lc_l1, lc_l3, lc_l4 ;
  - lc_en2, lc_a2, lc_a3 ;
- avec la voix réécrite (10) : lc_c1, lc_e8, lc_l2, lc_p4, lc_en3, lc_en4, lc_a4, lc_k2, lc_n1, lc_n2 ;
- nouvelle (1) : lc_c5.

En plus, lc_a5 reçoit une ligne de calcul au centre (1,80 − 1,26 = 0,54 mJ).

*Démonstrations des questions et exercices :*
- 2016 N (question de lc_a4) : la valeur de chaque énergie est maintenant sur sa propre ligne.
- 2023 N (fin de cours lc_en4 et exercice du bloc lc_s3_b3) : E_e calculé sur deux lignes.
- 2020 N III.4 : E_m sur deux lignes.
- 2021 R et 2020 R : « effet Joule : E diminue » est nommé.
- 2024 N (exercice de lc_a4 et sa copie dans le bloc) : un mot qui faisait sortir une ligne trop tôt a été corrigé.

*Nouvelle démonstration :* l’exercice I_m de lc_c5.

Les autres étaient déjà complètes et n’ont pas changé.

**Trois exemples avant → après :**
- lc_c1_depart : « U_m·cos φ = E est la plus grande valeur, donc φ = 0 » → système (1) cos φ, (2) i(0) = 0 ⇒ sin φ = 0 ⇒ φ ∈ {0 ; π} ; U_m > 0 et E > 0 ⇒ φ = 0 ⇒ U_m = E.
- lc_en3_echange : « E = ½·L·I_m² = 72 µJ, donc I_m ≈ 38 mA » → I_m = √(2E/L) ; substitution ; √(1,44·10⁻³) ; 3,8·10⁻² A = 38 mA ; vérification par E·√(C/L).
- lc_e8_T0 : « T₀² = 40 × 0,1 × 4·10⁻⁶ = 1,6·10⁻⁵ ; T₀ = 4 ms » → T₀² = 4π²·L·C ; C = 4 µF = 4·10⁻⁶ F ; substitution ; 1,6·10⁻⁵ s² ; T₀ = √(…) = 4·10⁻³ s = 4 ms.

### Voix à enregistrer (id)
- **Diapos (audio retiré)** : lc_c1_depart, lc_e8_T0, lc_l2_voisine, lc_p4_national, lc_en3_echange, lc_en4_somme, lc_a4_perdue, lc_k2_k, lc_n1_2020N, lc_n2_2025N, et lc_c5_courant (nouvelle). Leur `speech_text.fr` a été mis à jour aussi.
- **Nouvelle diapo lc_c5_courant** :
  - l’énoncé dit de l’exercice e0 ;
  - sa démonstration ;
  - 5 réactions : 1/juste, 0/1, 0/2, 2/1, 2/2.
- Aucune démonstration existante n’a vu sa `parole` changer : seules des lignes et des mots ont bougé.

### Vérifications faites (résultats)
- JSON valide, LF, `ensure_ascii=False`, indent 2. Le fichier a été relu juste avant chaque écriture.
- `verif_attente.py` :
  - 52 diapos ;
  - 0 mot absent, 0 hors bloc, 0 doublon ;
  - 0 compétence inconnue ;
  - 11 diapos sans voix (celles de la liste).
- Chaque diapo est dans exactement un bloc, dans l’ordre du cours, et appartient à une compétence.
- Les entrées du centre et les lignes de démonstration sortent dans l’ordre de la voix.
- Aucun chiffre, symbole ni tachkil dans les voix et les paroles nouvelles.
- Pas de nouveau mot hors cadre (motifs de la fiche `circuit_RLC`).
- `verifier_figures_cahier.py` : 9 figures, 0 erreur.
- **Calculs refaits en Python :**
  - T₀ : √(LC) = 6,32·10⁻⁴ s ; 2π√(LC) = 3,97·10⁻³ s (avec π² = 10 : 4·10⁻³ s exactement).
  - I_m : E·√(C/L) = √(2E/L) = 3,79·10⁻² A ; avec T₀ = 4 ms, (2π/T₀)·Q_m = 3,77·10⁻² A.
  - Énergie : ½·L·I_m² = ½·C·E² = 7,2·10⁻⁵ J.
  - Énergie perdue entre deux sommets : ½ × 4·10⁻⁶ × 20 = 4·10⁻⁵ J.
  - 2021 R : 2π√(5,1·10⁻⁵) = 44,9 ms.
  - 2022 N : L = 0,05 H.
  - 2020 N : C = 2,5·10⁻⁶ F ; E_t = 3,2·10⁻⁵ J ; ½·L·i² = 1,152·10⁻⁵ J ; E_e = 2,05·10⁻⁵ J.
  - 2025 N : T = 2,8·10⁻⁴ s ; énergie dissipée 2,55·10⁻⁵ J.
  - 2023 N : C = 10⁻⁷ F ; E = 5·10⁻⁶ J ; E_e = 3,2·10⁻⁶ J ; E_m = 1,8·10⁻⁶ J.
  - 2016 N : 7,2·10⁻⁴ J et 8·10⁻⁵ J.
