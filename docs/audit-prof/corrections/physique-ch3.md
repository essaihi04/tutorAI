## Propagation d’une onde lumineuse

Fichier : `backend/data/courses/en_attente/phys_ch3_ondes_lumineuses.json`. Je suis parti de la copie en attente, qui contenait déjà les démonstrations reprises ce matin. Le cours en ligne n'a pas été touché.
- Script : `scratchpad/corr/ch3p/build.py`.
- Copie d'avant : `scratchpad/corr/ch3p/avant.json`.
- Le cours passe de 53 à 55 diapos.

### Manques corrigés
| Constat (audit) | Ce qui a été fait | Diapo(s) |
|---|---|---|
| Haute : définition de « polychromatique » | Ajoutée à l'écran : puce, trace, centre, cahier. Ajoutée aussi à la voix, avec « نعاود نقرا ». Reprise dans ol_p1 (« infinité de radiations monochromatiques »), dans le cahier du bloc et au bilan (bloc 6). | ol_r1_monochromatique, ol_p1_blanche, ol_s3_b3r, ol_b1_bilan |
| Haute : la dispersion doit être **déduite**, pas affirmée | ol_p2 : l'ordre de la voix est corrigé. On part de l'observation (déviations différentes), puis on conclut que n dépend de ν, puis n(rouge) < n(violet). Le centre a 3 lignes. ol_p4 : la chaîne du bac en 3 étapes : n dépend de ν ; n = c/v avec c constante, donc v = c/n dépend de ν ; donc le milieu est dispersif. Elle est écrite au centre, en puce, au cahier, au bilan et dans une nouvelle démonstration (ol_x3 f1). | ol_p2_violet, ol_p4_dispersif, ol_s4_b2, ol_s4_b3, ol_b1_bilan, ol_x3 f1 |
| Haute : schéma du montage | Figure au cahier (`cahier_figures`) : laser, fente de largeur a, écran, cotes D et L. Elle est reprise dans le cahier du bloc. θ n'est **pas** dessiné ici, car il n'est enseigné qu'en ol_t1 (règle 27). | ol_d5_montage, ol_s1_b2 |
| Moyenne : « onde électromagnétique » | Ajouté en puce, au centre, au cahier, dans la voix, au cahier du bloc et au bilan. | ol_r2_vide, ol_s3_b3r, ol_b1_bilan |
| Moyenne : double périodicité, T, ν = 1/T, λ₀ = c·T | ol_r3 est réécrit : λ₀ = c·T, car pendant une période T la lumière parcourt λ₀ ; puis ν = 1/T, donc λ₀ = c/ν. C'est écrit au centre (4 lignes), en puce, au cahier, dans la voix et au cahier du bloc. | ol_r3_lambda0, ol_s3_b3 |
| Moyenne : condition de diffraction ; fente large = presque tout droit (dit seulement à l'oral) | ol_d2 : deux puces (fente large de 0,4 mm ; condition), plus la trace et le cahier. ol_t4 : ordre de grandeur « a de l'ordre de λ, au plus quelques centaines de λ (0,10 mm ≈ 150 λ) ». | ol_d2_fente_fine, ol_t4_relation, ol_s1_b1 |
| Moyenne : milieux plus ou moins dispersifs, air très peu | Écrit en puce, au centre, au cahier et dans la voix. | ol_p4_dispersif, ol_s4_b3 |
| Moyenne : vérifier θ = λ/a par des mesures | **Nouvelle diapo** ol_g6_theta. Elle reprend la vue existante `courbe.html?courbe=theta_inverse_a`. Contenu : θ = L/(2D) pour chaque fente, avec le calcul fait sur une fente ; le tableau a, 1/a, L, θ ; la droite ; la pente k = 6,5·10⁻⁷ m ; l'identification k = λ. Elle a 8 lignes au centre, une voix, un cahier, une figure au cahier, la compétence C5 et le bloc ol_s3_b2. | ol_g6_theta, ol_g5_autres, ol_s3_b2 |
| Moyenne : fréquences limites du visible | ν = c/λ₀ calculé pour le rouge (3,75·10¹⁴ Hz) et pour le violet (7,50·10¹⁴ Hz). C'est écrit au centre, dans la voix, en puce, au cahier, sur la figure et au cahier du bloc. | ol_r4_spectre, ol_s3_b3 |
| Basse : fil, θ = λ/d | Puce, centre (4 lignes) et voix : θ = λ/d ; θ = L/(2D) ; d'où d = 2λD/L. | ol_c4_cheveu, ol_s3_b1, ol_b1_bilan |
| Basse : l'onde diffractée garde λ, ν et v | Une puce. | ol_d4_onde |
| Basse : la lumière transporte de l'énergie | Une puce, le cahier et une phrase dans la voix. | ol_r2_vide |
| Basse : c = 299 792 458 m/s | Une puce. | ol_r2b_celerite |
| Basse : arc-en-ciel | Une puce et le cahier. | ol_p1_blanche |
| Basse : UV jusqu'à ~10 nm, IR jusqu'à ~1 mm | Une puce. | ol_r4_spectre |
| Seulement à l'oral : valeurs des indices | Écrites en puce, à la trace, au cahier et au cahier du bloc. | ol_n4_indice, ol_s4_b1 |
| Seulement à l'oral : L se mesure d'une extinction à l'autre | Écrit en puce, à la trace et au cahier. | ol_d5_montage, ol_s1_b2 |
| Seulement à l'oral : « la source impose la fréquence » | Écrit en puce, à la trace et au cahier. | ol_n2_frequence, ol_s4_b1 |
| Seulement à l'oral : la sonnette sous la cloche à vide | Écrite en puce. | ol_r2_vide |
| Démo qui saute une étape : λ = λ₀/n | ol_n5 est réécrite en 8 lignes : ν = c/λ₀ ; ν = v/λ ; même ν ; λ = λ₀·v/c ; v/c = 1/n car n = c/v ; λ = λ₀/n ; n = λ₀/λ ; dans l'air λ ≈ λ₀. C'est fait au centre, en puce, au cahier et dans la voix. | ol_n5_lambda_n |
| Démo qui saute une étape : n = L/L' | **Nouvelle diapo** ol_n6_cuve. Elle reprend la vue `diffraction.html?vue=cuve`. Contenu : L = 2λ₀D/a ; L' = 2λD/a ; L/L' = λ₀/λ ; λ₀/λ = n ; n = 2,4/1,8 ≈ 1,33. Elle a 7 lignes, une voix, un cahier, les compétences C7 et C4, et le bloc ol_s4_b2. | ol_n6_cuve, ol_c5_cuve, ol_x4, ol_b1_bilan |
| Démo qui saute une étape : θ = f(1/a) | Voir ol_g6_theta. | ol_g6_theta |
| Notations | Autres noms de θ (demi-écart angulaire, angle de diffraction) en ol_t1. Mise en garde « d = L/2 dans certains énoncés » en ol_c4. « Dans l'air λ ≈ λ₀ (θ = λ₀/a) » en ol_n5. « m/s = m·s⁻¹ » en ol_r2. | ol_t1_theta, ol_c4_cheveu, ol_n5_lambda_n, ol_r2_vide |
| Hors bloc (déjà dans le cours en ligne) | Les deux diapos de bilan sont mises dans un **nouveau bloc** ol_s5_b2. Il a un cahier de 3 lignes et un `retrouver` (les deux égalités). Son exercice est un QCM (λ dans le verre), avec démonstration et réactions préparées : juste, faux 1 et faux 2, sans audio. | ol_b1_bilan, ol_b2_carte |

### Non corrigés et pourquoi
- Manques chez un seul professeur : non faits. Le cadre ne les exige pas (θ ≤ 15°, L' = f(1/d), tableau des indices du verre, montage de dispersion complet). La mesure de L d'une extinction à l'autre est faite, mais parce que l'audit la classe aussi « seulement à l'oral ».
- « La fente se comporte comme une source secondaire » (basse, côté voix) : non fait. Ce n'est pas un simple ajout écrit, et le mot est proche de « Huygens », qui est hors cadre.
- Condition « jusqu'à 100 λ » : je ne l'ai pas écrite telle quelle, car **nos propres mesures la contredisent**. Avec a = 0,40 mm (≈ 600 λ), on mesure encore L = 6,5 mm. J'ai écrit à la place « de l'ordre de λ, au plus quelques centaines de λ ». **À décider.**
- **À décider** : le bloc ol_s3_b2 a maintenant **5 diapos** (g2, g3, g4, g6, g5), au-dessus de la règle des 3–4. Le couper en deux ferait une séance de 4 blocs.
- Les 2 nouvelles diapos ne demandent aucune nouvelle simulation : elles reprennent des vues existantes. Les simulations n'ont pas été modifiées. Les pages `bilan.html` et `carte.html` n'écrivent donc pas les ajouts (polychromatique, électromagnétique, chaîne de la dispersion) : ils sont seulement dans les puces du bilan.
- `speech_text.fr` a été mis à jour sur les diapos dont la voix change. La voix du bilan ol_b1 n'est pas modifiée : elle résume, et les puces sont plus complètes.
- Les rappels (`competences[].rappels`) de calcul n'ont pas de démonstration. Le format des rappels ne la prévoit pas (`memoire/api`).
- Les réactions préparées existantes ne sont pas réécrites. Leurs valeurs ont été relues et sont justes. Elles restent courtes, parce que la démonstration s'ouvre juste après.
- `controler_cadre.py` (chemin Windows) n'a pas pu être lancé. Deux écritures ne sont pas dans la liste des formules de la fiche : « ν = 1/T » (rappel du chapitre 2) et « L/L' = λ₀/λ » (étape de calcul).

### Démonstrations
Toutes ont été relues : 17 démonstrations de questions, d'exercices et de blocs, plus les preuves et exemples au centre des diapos et dans les cahiers.

Réécrites ou ajoutées :
- **9 tableaux de démonstration** :
  - nouveaux : ol_g1_points/q, ol_r4_spectre/q, ol_x3/f1, bloc ol_s5_b2 ;
  - repris : ol_x2/f1, ol_x2/f2, ol_x3/f0, ol_x4/f0, bloc ol_s4_b2.
- **19 preuves au centre**, une entrée par ligne, chacune sur son mot :
  - avec une nouvelle voix : ol_l7, ol_g4, ol_c4, ol_r3, ol_r4, ol_n5, ol_p2, ol_p4, ol_x2, et les nouvelles diapos ol_g6 et ol_n6 ;
  - sur la voix existante (audio gardé) : ol_p1_radian, ol_p2_tangente, ol_l6, ol_l8, ol_l9, ol_c3, ol_g3, ol_g5, ol_x3.
- **Cahiers avec le calcul en étapes** : ol_l7, ol_x2, ol_x3, ol_x4, ol_r4, ol_n5.

Exemples avant → après :
- **ol_l7** : avant, « relation, AN, résultat, unité », sans calcul. Après : λ = aL/(2D) ; a = 1,0·10⁻⁴ m ; L = 2,6·10⁻² m ; (1,0·10⁻⁴ × 2,6·10⁻²)/(2 × 2,0) ; 6,5·10⁻⁷ m ; 650 nm.
- **ol_x2/f2** : avant, « λ = v/ν et v = c/n, donc λ = λ₀/n ; 580/1,5 ». Après : ν invariant ; λ₀ = c/ν et λ = v/ν ; λ/λ₀ = v/c ; v/c = 1/n car n = c/v ; 580/1,5 ; ≈ 387 nm.
- **ol_x2** (diapo) : avant, « a = 2λ₀D/L » seul. Après : λ₀/a = L/(2D) ; a = 2λ₀D/L ; λ₀ = 5,8·10⁻⁷ m ; L = 2,7·10⁻² m ; AN ; a ≈ 6,0·10⁻⁵ m = 60 µm.

Compromis : en ol_r4, la substitution et le résultat de ν restent sur la même ligne (2 calculs sur une diapo, 8 lignes au plus).

### Voix à enregistrer (id)
- **Diapos (`audio.mixed` retiré, 13)** : ol_l7_calcul_lambda, ol_c4_cheveu, ol_g4_identifier, **ol_g6_theta** (nouvelle), ol_r1_monochromatique, ol_r2_vide, ol_r3_lambda0, ol_r4_spectre, ol_n5_lambda_n, **ol_n6_cuve** (nouvelle), ol_p2_violet, ol_p4_dispersif, ol_x2_national_2023.
- **Démonstrations** : ol_g1_points/q, ol_r4_spectre/q, ol_x2_national_2023/f1, ol_x2_national_2023/f2, ol_x3_national_2021/f0, ol_x3_national_2021/f1, ol_x4_national_2025/f0, bloc ol_s4_b2, bloc ol_s5_b2. Il faut aussi enregistrer celles de ce matin (ol_l1/f0, ol_l8/q, ol_g5/q, blocs ol_s1_b3, ol_s2_b2, ol_s3_b1, ol_s3_b2).
- **Réactions et énoncés** : bloc ol_s5_b2. Pour l'exercice : `enonce_dit` et les réactions 0/1, 0/2, 1/juste, 2/1, 2/2. Pour le `retrouver` : `enonce_dit`.

### Vérifications faites (résultats)
- JSON valide, fins de ligne LF, `ensure_ascii=False`, `indent=2`, retour à la ligne final. Le fichier a été relu et comparé à la copie de départ juste avant l'écriture.
- `verif_attente.py` : 55 diapos, **0 mot absent, 0 hors bloc**, 0 doublon, 0 compétence inconnue, 13 diapos sans voix (celles de la liste).
- `scratchpad/corr/ch3p/verif.py` : 0 erreur. Il vérifie :
  - chaque `mot` de démonstration est dans sa parole, dans l'ordre ;
  - chaque `mot` du centre et du pointage est dans `speech_text.mixed`, et chaque `centre:N` existe ;
  - aucun chiffre, symbole ni tachkil dans les voix ni dans les paroles ;
  - chaque diapo est dans un seul bloc, les blocs suivent l'ordre du cours, avec une seule question par bloc ;
  - compétences et `slide_ids` sont cohérents.
- `verifier_figures_cahier.py` : 11 figures, 0 erreur, 0 avertissement.
- Calculs refaits en Python, tous justes :
  - λ = 6,5·10⁻⁷ m (×2) ; θ = 1,625 / 3,25 / 6,5 / 13 ·10⁻³ rad ; k = 6,5·10⁻⁷ m ;
  - ν = 3,75·10¹⁴ et 7,50·10¹⁴ Hz ; n = 1,33 ;
  - a = 6,01·10⁻⁵ m ; λ₀R = 730 nm ; v = 2·10⁸ m/s ; λ = 387 nm ; 532/1,33 = 400 nm ; v = 2,26·10⁸ m/s ;
  - k = 2·10⁻² ; λ = 600 nm ; d = 8·10⁻⁵ m ; L₂ = 52 mm ; 65 000 nm ; 0,75 ; 0,10 mm ≈ 154 λ ;
  - λ₀ = 600 nm et λ = 400 nm (exercice du bilan, distracteur 900 = 600 × 1,5).
