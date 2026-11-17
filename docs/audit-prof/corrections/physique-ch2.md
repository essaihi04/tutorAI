## Ondes mécaniques progressives périodiques

Fichier : `backend/data/courses/en_attente/phys_ch2_ondes_periodiques.json`. Je suis parti de la copie en attente, avec les démonstrations reprises ce matin. Le cours en ligne n'a pas été touché. Script des changements : `scratchpad/corr/ch2_build.py`. Copie d'avant : `scratchpad/corr/ch2_avant.json`. Le cours passe de 52 à 54 diapos.

### Manques corrigés
| Constat (audit) | Ce qui a été fait | Diapo(s) |
|---|---|---|
| Haute : T doit être la **plus petite** durée | Ajouté dans la puce, la trace, le cahier et la voix (« أصغر وقت… أول مرة »). Démo de la question : « pour la première fois », puis « T est la plus petite durée », puis T = 0,5 s. Mis à jour aussi dans le cahier du bloc, `retrouver`, l'option de l'exercice du bloc et le bilan. | op_t1_periode, op_s1_b2, op_b1_bilan |
| Haute : onde sinusoïdale = élongation **sinusoïdale du temps** | Sous-titre, puce, trace, cahier et voix réécrits ; la forme de la corde est donnée comme conséquence. Rappel C1_r2 : option juste et son `ecrit` réécrits (la `parole` reste juste). | op_o5_sinusoidale, op_s1_b2, op_b1_bilan, C1_r2 |
| Haute : onde périodique **non sinusoïdale** (instrument / diapason), lire T | **Nouvelle diapo** sans visuel. Elle a un tableau (diapason / instrument), 2 figures au cahier (sinusoïde, motif non sinusoïdal, avec T marquée) et le calcul ligne par ligne (T = 4 × 0,5 ms = 2 ms ; N = 500 Hz). Elle est en tête du bloc op_s2_b2, avec les compétences C1 et C2. Elle n'a pas de question : la question du bloc reste op_l3. | op_t8_non_sinusoidale |
| Haute : la fréquence ne change pas quand on change de milieu ; λ change | Écrit en puce, au centre, au cahier et dit dans la voix. Repris au cahier du bloc et au bilan (puce, voix, cahier). | op_c2_relation, op_s3_b1, op_b1_bilan |
| Haute : l'onde diffractée garde N, v, λ **si le milieu ne change pas** | Condition écrite partout (centre, puces, cahier, cahier du bloc, `retrouver`, bilan, explication du vrai/faux de op_x2). | op_d2_invariants, op_s4_b2, op_x2, op_b1_bilan, op_b2_carte |
| Haute : diffraction d'une onde **sonore / ultrasonore**, schéma du montage (cadre + TP) | **Nouvelle diapo** sans visuel. Contenu : montage E → fente → R sur un arc, relié à l'oscilloscope (figure au cahier) ; λ = v/N = 8,5 mm ; a = 5 mm ≤ λ, donc diffraction ; λ des sons audibles. Exercice de fin de cours (porte entrouverte, 680 Hz) avec sa démonstration et ses réactions préparées (juste, faux 1 et faux 2 pour chaque option fausse, sans audio). Placée en tête du bloc op_s4_b3, avec la compétence C7. | op_d4_ultrasons |
| Moyenne : stroboscope, N = k·N_e ; la plus grande N_e est N | Le centre a 3 lignes ; la voix fait le raisonnement (éclairs 2 fois plus lents → 2λ → encore immobile). Repris dans les puces, le cahier, le cahier du bloc, `retrouver`, l'attendu de C6_r1 et le bilan. | op_m2_immobile, op_s3_b3, C6_r1, op_b1_bilan |
| Moyenne : « onde diaphragmée » | Mot ajouté à la puce, au cahier, au cahier du bloc et à la voix. | op_d1_ouverture, op_s4_b2 |
| Moyenne : diffraction plus marquée quand a est plus petite | Écrit (puce, trace, cahier, cahier du bloc). La voix n'est pas changée. | op_d3_justifier |
| Moyenne : lire en phase / opposition sur deux courbes | Ajouté à la puce, au cahier, au cahier du bloc et à la voix (une phrase). | op_m5_premier_retour, op_s4_b1 |
| Moyenne : échelle d'une figure | Puce et cahier, avec un exemple (2,25 cm mesurés × 2 = 4,5 cm). | op_l5_intervalles, op_s2_b3 |
| Moyenne : sens du premier mouvement = celui de la source | Ajouté au centre et à la voix de op_r1, et écrit dans op_r4 (puce, cahier) et au cahier du bloc. | op_r1_retard, op_r4_source, op_s5_b1, op_s5_b2 |
| Basse : λ des sons audibles (1,7 cm à 17 m) | Calcul écrit au cahier : 340/20 000 et 340/20. | op_s2_air, op_s4_b3, op_d4 |
| Basse : obstacle, plus de zone calme ; diffraction propre aux ondes | Écrit au cahier. | op_d1_ouverture |
| Basse : aspects à T/4, T/2… | Non fait (voir plus bas). | — |
| Seulement à l'oral : op_p3 | Ajout de 6 puces (même unité, entier, entier et demi, « ni l'un ni l'autre (2,25) », conclusion), du cahier et du cahier du bloc. | op_p3_methode, op_s3_b2 |
| Seulement à l'oral : op_c2, « distance sur durée » | Mis au centre (ligne 1) et au cahier. | op_c2_relation |
| Seulement à l'oral : op_t7, « T = 5 sans unité est faux » | Mis au centre, en puce et au cahier. | op_t7_oscillo, op_s2_b1 |
| Seulement à l'oral : op_l4, sens de l'hypothèse | Puce et cahier. | op_l4_rides |
| Seulement à l'oral : op_b2, lien vers la lumière | Puce et cahier (annoncé, « au chapitre suivant »). | op_b2_carte |
| Notations | N, « aussi notée f ou ν » (cahier de op_t3) ; m/s = m·s⁻¹ (op_c2) ; k ∈ ℕ* et k ∈ ℕ (op_p1, op_p2, bloc, bilan) ; N_e (op_m2) ; « N = 1/T car en 1 s le point fait 1/T périodes » (op_t4). | op_t3, op_t4, op_c2, op_p1, op_p2 |
| **Erreur trouvée** dans op_x1 (national 2017) | La diapo concluait « SM = k·λ → en phase ». Sur la figure, SM = 6 cm et λ = 4 cm, donc SM/λ = 1,5 : M et S sont **en opposition de phase**. Le calcul est maintenant écrit et la conclusion corrigée (centre, voix, puces, cahier, cahier du bloc). | op_x1_national_2017, op_s5_b2 |

### Non corrigés et pourquoi
- y(t) = A·cos(2πt/T + φ) : la fiche du cadre classe « phase à l'origine » hors cadre et dit que ce n'est demandé dans aucun national.
- Δt/T = k (Chriki) et « durée entre deux perturbations » : un seul professeur les donne, et le cadre ne les exige pas.
- Aspects de la corde à T/4, T/2… (basse) : il faudrait un dessin à quatre courbes, donc plus qu'un simple ajout écrit. L'animation de op_c1 et la démo de op_c2 couvrent déjà l'idée.
- Les 2 nouvelles diapos n'ont **pas de visuel**, car aucune vue existante ne convient (pas d'oscillogramme d'instrument, pas de fente à ultrasons). Elles ont un tableau ou un centre écrit, plus des figures au cahier. **À décider** : une vue `figures.html?fig=…` (oscillogramme non sinusoïdal, montage E-fente-R).
- Dans op_x1, l'étape `fin` de la simulation écrit encore « y_M(t) = y_S(t − 0,03) » pendant que la voix conclut « opposition de phase ». Ce n'est pas faux, mais la simulation n'a pas été modifiée.
- Les nouvelles diapos ne sont pas à la dernière place du bloc. La question du bloc reste donc la dernière **question**, mais pas la dernière diapo. op_d4 est placée en tête de op_s4_b3, pour que la question de op_s3 reste la dernière.
- Les réactions préparées (les ~150 existantes) n'ont pas été réécrites, ni les QCM des rappels (sans démonstration).
- op_b1_bilan : le `speech_text.fr` n'a pas été refait, seul `mixed` est à jour.

### Démonstrations
Toutes ont été relues : question.demonstration, exercices, exercices de fin de cours, blocs, centres des diapos, cahiers. Les démos reprises ce matin étaient complètes et n'ont pas été changées.

Réécrites :
- 3 tableaux de démonstration : op_t1/q, op_s3_b1/exercice (λ = v/N justifiée), op_d4/e0 (nouvelle, 7 lignes).
- 19 preuves au centre des diapos, une entrée par ligne sur son mot : op_t7, op_t8, op_c2, op_c3, op_c4, op_l5, op_m2, op_m4, op_m6b, op_d2, op_d4, op_s1, op_s2, op_r1, op_r2, op_r3b, op_x1, op_x2, op_x3.

Exemples avant → après :
- op_c2 : « v = λ/T : 0,5/0,5 = 1 m/s » → v = d/Δt ; pendant Δt = T l'onde parcourt d = λ ; v = λ/T ; 0,5/0,5 = 1 m/s ; λ = v·T ; N = 1/T donc v = λ·N ; unités ; autre milieu.
- op_r2 : « SM = k·λ → τ = k·T → en phase » → SM = k·λ ; τ = SM/v = k·λ/v ; λ/v = T (car λ = v·T), donc τ = k·T ; M en phase avec S.
- op_m6b : « λ = (d₂ − d₁)/n = … = 0,85 cm » et « v = … = 340 m/s » → d = 11,7 − 10,0 ; d = 1,7 cm ; d = 2λ donc λ = d/2 ; λ = 1,7/2 ; λ = 0,85 cm = 8,5 × 10⁻³ m ; N = 40 kHz = 40 000 Hz ; v = 8,5 × 10⁻³ × 40 000 ; v = 340 m/s.

Compromis : dans op_r3b, op_x2 et op_x3 (trois calculs sur une diapo), une ligne garde « AN = résultat », pour rester à 8 lignes au plus. Chaque calcul est aussi détaillé sur son tableau de démonstration.

### Voix à enregistrer (id)
- **Diapos (`speech_text.mixed` changé, `audio.mixed` retiré, 22)** : op_t1_periode, op_o5_sinusoidale, op_t7_oscillo, **op_t8_non_sinusoidale** (nouvelle), op_c2_relation, op_c3_rediger, op_m2_immobile, op_m4_microsecondes, op_m5_premier_retour, op_m6b_deja_ecartes, op_d1_ouverture, op_d2_invariants, **op_d4_ultrasons** (nouvelle), op_s1_frequence, op_s2_air, op_r1_retard, op_r2_relation, op_r3b_calculs, op_x1_national_2017, op_x2_national_2020, op_x3_devoir, op_b1_bilan.
- **Démonstrations** : op_t1_periode/q (audio retiré), op_d4_ultrasons/e0 (nouvelle), seances op_s3_b1/exercice (aucune piste avant). Il faut aussi enregistrer les démos dont l'audio a été retiré ce matin.
- **Réactions et énoncé** : op_d4_ultrasons, `reponses_fin_de_cours` e0 (0/juste, 1/1, 1/2, 2/1, 2/2) et `enonce_dit` de e0.

### Vérifications faites (résultats)
- JSON valide, fins de ligne LF, `ensure_ascii=False`, `indent=2`. Fichier relu juste avant chaque écriture.
- `verif_attente.py` : 54 diapos, **0 mot absent, 0 hors bloc**, 0 doublon, 0 compétence inconnue, 22 diapos sans voix (celles listées ci-dessus).
- Mon script : chaque `mot` du centre et du pointage est dans `speech_text.mixed`, chaque `centre:i` a son pointage, chaque `mot` de démonstration est dans sa `parole` ; chaque diapo est dans exactement un bloc et les blocs sont contigus ; chaque `competence_id` existe ; pas de chiffre, de symbole ni de tachkil dans les voix ; une seule question par bloc.
- Calculs refaits en Python, tous justes : 0,5 ms ; 2000 Hz ; 2 ms ; 500 Hz ; 0,30 et 0,33 m/s ; 25 µs ; 40 000 Hz ; 1,7 cm, 0,85 cm et 340 m/s ; λ = 8,5 mm ; 0,5 m ; 17 m et 1,7 cm ; 340 m/s (×2) ; τ = 0,2 s ; 50 Hz ; 2,5 m/s ; 5 cm ; 2 m/s ; 30 ms ; SM/λ = 1,5 ; 4,5/1,5 = 3 ; 0,3/20 = 1,5 × 10⁻² m.
- Voix : les phrases « T égale le nombre de divisions, fois la sensibilité horizontale » ont été coupées par une virgule. Il reste des expressions numériques de 10 à 11 mots d'un seul tenant (ex. « v égale un virgule cinq fois dix puissance moins deux »), comme ailleurs dans le cours.
