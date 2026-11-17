## Dipôle RC

Copie en attente : `backend/data/courses/en_attente/phys_ch6_dipole_RC.json`. Je suis parti de cette copie, qui contenait déjà les démonstrations reprises ce matin. Script : `scratchpad/corr/phys6/apply.py` ; journal : `scratchpad/corr/phys6/log.json`. Le cours passe de 56 à 57 diapos (1 nouvelle). Les séances et les blocs ne changent pas, sauf le bloc `rc_s3_b3`, qui passe de 2 à 3 diapos.

### Manques corrigés

| Constat (audit) | Ce qui a été fait | Diapo(s) |
|---|---|---|
| Haute : i(t) en charge donné sans calcul | Calcul de i(t) écrit ligne par ligne (une entrée centre par ligne), avec la voix réécrite : i = C·du_C/dt, du_C/dt = (E/τ)·e^(−t/τ), i = (C·E/τ)·e^(−t/τ), C/τ = 1/R car τ = RC, i(t) = (E/R)·e^(−t/τ), i(0) = E/R = 12/10³ = 12 mA. Mis aussi à l'écran, au cahier et dans le cahier du bloc | rc_s7_q_i |
| Haute : i(t) de la décharge donné sans dériver ; u_R(t) jamais écrit. Moyenne : q(t) en décharge, q(0) = C·E, i(0) = −E/R | **Nouvelle diapo** : q(t) = C·E·e^(−t/τ), dérivée de u_C, i(t) = −(E/R)·e^(−t/τ), u_R = R·i = −E·e^(−t/τ), vérification u_R + u_C = 0. Elle réutilise la vue `continuite.html?vue=decharge`, qui n'était pas encore utilisée par le cours. Elle n'a pas de question (celle du bloc est sur rc_d2). Bloc rc_s3_b3, compétence C5 | rc_d3_decharge_qi (nouvelle) |
| Haute : forme A + B·e^(−αt) sans ses lignes | Dérivée −α·B·e^(−αt), remplacement, regroupement B·e^(−αt)(1 − RCα) + A = E pour tout t, puis « e^(−αt) ≠ 0 et B ≠ 0 » ⇒ α = 1/(RC), A = E, et enfin la condition initiale. Écrit à l'écran, au cahier, en 7 entrées centre ; voix réécrite. La question de la diapo (que vaut B) est gardée | rc_s4_condition |
| Haute : rc_d1 part de A·e^(−t/τ) sans la ligne de remplacement ni « A ≠ 0 », et la voix s'arrêtait avant A | Lignes complètes : la dérivée, −RC·(A/τ)·e^(−t/τ) + A·e^(−t/τ) = 0, la factorisation, « e^(−t/τ) ≠ 0 et A ≠ 0 » ⇒ τ = RC, u_C(0) = A·e⁰ = A = E (u_C est continue), puis u_C(t) = E·e^(−t/τ). La variante A·e^(−t/τ) + B ⇒ B = 0 est écrite à l'écran et au cahier. Voix réécrite jusqu'au bout | rc_d1_decharge |
| Haute (cadre RC4) : visualiser u_R | Ajouté à l'écran, au cahier et à la voix : entrée Y à la tête de la flèche de u_R, masse à l'autre borne de R ; u_R = R·i montre la forme de i. Un pointage `fleche_uR` est ajouté | rc_m2_acquisition |
| Moyenne : oscilloscope à mémoire, et pourquoi | « Système d'acquisition ou oscilloscope à mémoire, car la tension n'est pas périodique », à l'écran, au cahier et dans la voix | rc_m2_acquisition |
| Moyenne : tableau des solutions de la charge et de la décharge | Puce « Solutions » et cahier du bilan : u_C, q, i, u_R pour la charge et pour la décharge, avec leurs conditions initiales | rc_b1_bilan |
| Moyenne : q = I₀·t seulement si q(0) = 0 | Condition écrite à l'écran, au centre, au cahier et au bloc. Elle est ajoutée aussi à la 1re ligne des démonstrations g2/f0 et s1_b3 | rc_g1_generateur, rc_g2_pente |
| Basse : n condensateurs | C_eq = C₁ + … + Cₙ et 1/C_eq = 1/C₁ + … + 1/Cₙ, à l'écran, au cahier et au bloc | rc_a1_parallele, rc_a2_serie |
| Basse : intérêt du parallèle et de la série | Parallèle : « grande charge sous une petite tension ». Série : « C_eq plus petite que la plus petite » | rc_a1, rc_a2 |
| Basse : C positive, propre au condensateur | Écrit à l'écran, au cahier et dans une phrase de la voix | rc_c4_capacite |
| Basse : influence de τ sur la décharge | Une ligne à l'écran et au cahier | rc_t3_C |
| Basse : flash d'appareil photo (admis par le cadre) | Une ligne à l'écran et au cahier | rc_l7_energie |
| Notation : variante τ·du_C/dt + u_C = E | Une ligne au cahier et à l'écran, annoncée « plus tard » | rc_e3_formes |
| Notation : q = q_A, u_C = u_AB | Écrit à l'écran et au cahier | rc_c4_capacite |
| Seulement à l'oral : « A n'est pas nulle » | Écrit (centre, écran, cahier) | rc_d1_decharge |
| Seulement à l'oral : « montrer que RC est homogène à un temps » | Phrase du bac écrite à l'écran, au cahier et au bloc | rc_t1_dimension |
| Seulement à l'oral : R = 2 kΩ ⇒ τ = 0,44 s | Calcul écrit à l'écran et au cahier, avec des entrées centre sur la voix existante | rc_t2_influence |
| Seulement à l'oral : ordonnée à l'origine E/(RC) = 1000 V/s | Écrit à l'écran, au cahier et au centre, avec le contrôle 12/(10³ × 1,2·10⁻⁵) = 1000 V/s et « coupe l'axe en u_C = E » | rc_l5_pente |
| Seulement à l'oral : nouvelle origine des temps | Écrite au cahier de la diapo et du bloc | rc_d2_continuite |
| Seulement à l'oral : « interrupteur ouvert » | Écrit au cahier de la diapo et du bloc | rc_m4_regimes |
| Démonstration qui saute des étapes : rc_e5 « de même avec i » | u_R = R·i ⇒ RC·R·di/dt + R·i = 0, puis division par R (R ≠ 0). Voix réécrite, 5 entrées centre | rc_e5_uR_i |
| Démonstration qui saute des étapes : la tangente coupe l'asymptote à τ (TS seulement, mais exigé par la règle 37) | Pente (du_C/dt)(0) = (E/τ)·e⁰ = E/τ, tangente u = (E/τ)·t, (E/τ)·t = E ⇔ t = τ. Voix réécrite et 3 entrées centre | rc_l1_tangente |

Exemples travaillés sur les diapos : j'ai ajouté une entrée centre par ligne, sur des mots de la voix existante, sans changer la voix. Ces entrées donnent la loi utilisée, les conversions et la substitution. Diapos concernées : rc_c6, rc_a1, rc_a2, rc_g2, rc_m4, rc_e2, rc_e3, rc_e4, rc_e6, rc_rp7, rc_s2, rc_s3, rc_s5, rc_s6, rc_t2, rc_t3, rc_l2, rc_l3, rc_l4, rc_l5, rc_l8, rc_n2.

Valeurs particulières : elles sont maintenant calculées et non plus annoncées. 1 − e⁻¹ ≈ 1 − 0,37 = 0,63 (rc_rp7, rc_s6, rc_l2) ; e⁻⁵ ≈ 0,007 donc 0,99·E (rc_s6) ; e⁻¹ ≈ 0,37 (rc_l3) ; 0,63² ≈ 0,40 (rc_l8). L'exemple de rc_c4 restait sans résultat (« 10 µF sous 2 V ») : il va maintenant jusqu'à q = 20 µC, à l'écran et dans la voix. Les cahiers de rc_n1 et rc_n2 ont reçu leur application numérique.

**Doute Q_max** (rc_e8_national e0, bloc rc_s2_b3) : l'énoncé est cohérent en lui-même (Q_max = C·E ⇒ E = 12·10⁻⁶/10⁻⁵ = 1,2 V). Il n'est pas daté « 2023 R ». Je n'ai donc changé ni l'énoncé ni « correct ». J'ai vérifié le sujet 2023 R dans `backend/data/exams/physique/2023-rattrapage` : C₀ = 10 µF et, dans le corrigé, E_e = 0,72 mJ, d'où q_max = 120 µC et E = 12 V. Notre 12 µC n'est donc pas la donnée du national. J'ai seulement corrigé la réaction du choix « 120 V » : ce chiffre vient de 12 × 10 (une multiplication au lieu d'une division), et non d'une erreur d'unités.

### Non corrigés et pourquoi

- **Exercice de capacité équivalente d'un montage mixte** (priorité basse) : ce n'est pas un simple ajout écrit. Il faut un exercice, sa démonstration et 5 réactions.
- **Manques chez un seul professeur** : je ne les ai pas ajoutés (convention générateur, générateur de résistance interne r, continuité de u_C par l'énergie, énergie en décharge, intérêt de la série pour la tension, condensateur débranché, comparaison avec la valeur du fabricant). Exceptions : la justification de la tangente, exigée par la règle 37, et i(t) de la charge par la dérivée, exigé par le cadre RC6.
- **Hors cadre**, non ajoutés : t½ = τ·ln 2, l'intégration pour l'énergie, C = ε·S/e. J'ai aussi retiré « temps de demi-vie » d'une réaction (rc_l3_descente q/2/2).
- **Simulations non modifiées** : `bilan.html` n'affiche pas le tableau des solutions ajouté au bilan, `figures.html?fig=fig_condition_initiale` et `fig_decharge_solution` n'affichent pas les nouvelles lignes, et la nouvelle diapo rc_d3 n'a pas de vue dédiée à q(t) et u_R(t) (elle utilise la vue décharge u_C / i).
- **15 réactions déjà présentes avec des chiffres dans leur parole** (rc_a2, rc_g2, rc_e3, rc_l2, rc_l3, rc_l5, rc_l6) : elles étaient déjà là avant, je ne les ai pas réécrites. Elles sont à reprendre avant l'enregistrement de la voix Bodi.
- Les réactions de rc_a1 disent « comme si la surface des armatures augmentait » : c'est une analogie, déjà dans la voix de la diapo. Je l'ai gardée.

### Démonstrations

- 46 relues, plus les preuves écrites sur les diapos et les 253 réactions écrites. **12 réécrites** :
  - rc_s4/e0 et ses 3 copies (n1/f0, s3_b1, s4_b3) ;
  - rc_l3/e0 et rc_l3/f0 ;
  - rc_l4/f0 et la copie s4_b1 ;
  - rc_l5/f0 et la copie s4_b2 ;
  - rc_g2/f0 et la copie s1_b3.
- **7 preuves sur diapo réécrites**, avec leur voix : rc_s7, rc_d1, rc_s4, rc_e5, rc_l1, rc_c4, et la nouvelle rc_d3. Les autres démonstrations étaient complètes et sont restées telles quelles.
- **9 réactions corrigées** : l'erreur nommée correspond maintenant au vrai calcul qui donne le chiffre de l'élève. Ce sont 0,5 µF (I₀/Δu sans Δt), 120 V, 1,2·10⁻⁵ J (c'est q elle-même), 300 Ω (6 × 50), 1,44 F (τ × R₁), et « demi-vie » retiré.
- Avant → après :
  - rc_s4 : « l'équation donne A = E et α = 1/RC » → dérivée −α·B·e^(−αt), remplacement, B·e^(−αt)(1 − RCα) + A = E pour tout t, e^(−αt) ≠ 0 et B ≠ 0 ⇒ α = 1/(RC), il reste A = E.
  - rc_s7 : « i(t) = (E/R)·e^(−t/τ) » → i = C·du_C/dt = (C·E/τ)·e^(−t/τ), C/τ = 1/R car τ = RC, i(t) = (E/R)·e^(−t/τ), i(0) = 12/10³ = 12 mA.
  - Copies q(t) = A(1 − e^(−αt)) : « Vrai pour tout t, donc RCα − 1 = 0 » → « Vrai pour tout t ; e^(−αt) varie avec t et ne s'annule jamais : RCα − 1 = 0, il reste A = C·E », et la dérivée porte son « car (e^(−αt))′ = −α·e^(−αt) ».
- Tous les calculs ont été vérifiés en Python : 2·10⁻⁵ C, 0,22 s, 0,44 s, 0,632, 0,368, e⁻⁵ = 0,0067, 12 mA, 7,56 V, 4,44 mA, 120 Ω, 100 µF, −83,3 s⁻¹, 1,2·10⁻⁵ F, 1000 V/s, 1,58·10⁻² J, 0,397, 7,2·10⁻⁶ J, 1,2 V.

### Voix à enregistrer

- **Diapos** (speech_text.mixed, audio retiré) : rc_c4_capacite, rc_m2_acquisition, rc_e5_uR_i, rc_s4_condition, rc_s7_q_i, rc_d1_decharge, rc_l1_tangente, et la nouvelle rc_d3_decharge_qi.
- **Démonstrations** (parole changée ; aucune n'avait de piste audio) : rc_g2_pente/f0, rc_s1_b3/exercice, rc_s4_condition/e0, rc_n1_2019/f0, rc_s3_b1/exercice, rc_s4_b3/exercice, rc_l3_descente/e0, rc_l3_descente/f0, rc_l4_deduire/f0, rc_s4_b1/exercice, rc_l5_pente/f0, rc_s4_b2/exercice.
- **Réactions** (audio retiré) : rc_e8_national e0/0/1, e0/0/2 ; rc_l3_descente q/2/2 ; fin de cours : rc_g2_pente e0/0/2, rc_l8_calcul e1/2/2, rc_n2_2021R e0/1/1, e0/1/2, e2/2/1, e2/2/2.

### Vérifications faites

- `json.load` : OK. Le fichier a été écrit avec `json.dumps(ensure_ascii=False, indent=2)` et des fins de ligne LF (0 CR). Il a été relu juste avant l'écriture et était identique à la copie de départ.
- `verif_attente.py` : 57 diapos, 0 mot absent, 0 hors bloc, 0 doublon, 0 compétence inconnue, 8 diapos sans voix (les 8 listées plus haut).
- Script maison :
  - chaque `mot` de `demonstration.lignes` est dans sa parole ;
  - chaque `mot` de pointage et de centre est dans `speech_text.mixed` ;
  - `apres_mot` de l'observation de rc_t2 est présent ;
  - aucun chiffre ni symbole dans les voix ;
  - l'ordre des blocs suit l'ordre des diapos ;
  - au plus un « À toi » par bloc ;
  - aucun mot hors cadre (demi-vie, intégration, permittivité, Laplace, impédance).
- `backend/scripts/verifier_figures_cahier.py` : 9 figures, 0 erreur, 0 avertissement.
- Rien d'autre n'est modifié dans le dépôt ; aucun commit.
