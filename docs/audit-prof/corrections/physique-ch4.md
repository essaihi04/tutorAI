## Décroissance radioactive

Fichier modifié : `backend/data/courses/en_attente/phys_ch4_radioactivite.json` (partie de la copie de ce matin ; rien de perdu, seuls les `audio` des voix changées sont retirés). 59 → 61 diapos. Script de correction : `scratchpad/ch4/patch1.py` ; copie d'avant : `scratchpad/ch4/backup_avant.json`.

### Manques corrigés
| Constat (audit) | Ce qui a été fait | Diapo(s) |
|---|---|---|
| Haute : m(t) = m₀·e^(−λt), n(t) absents | Nouvelle diapo après la mole (règle 27 : N = (m/M)·N_A n'est enseigné qu'à ra_p4_mole) : m = (M/N_A)·N, M/N_A constant ⇒ m(t) = m₀·e^(−λt), n(t) = n₀·e^(−λt) ; ajouté au bilan | ra_a5b_masse_inverse (nouvelle), ra_z1_bilan |
| Haute : unité de τ absente | Puce, centre et cahier « τ en s (ou unité de t), car λ en s⁻¹ » ; bilan « τ = 1/λ (en s) » | ra_l7_tau, ra_z1_bilan |
| Haute : jamais N → m ni a → m | Même nouvelle diapo : n = N/N_A puis m = n·M (chaque relation avec son « car »), N = a/λ ; question QCM a₀ → N₀ → n₀ → m₀ (iode 131, 8,7·10⁻¹⁰ g) avec démonstration 7 lignes et 5 réactions préparées | ra_a5b_masse_inverse |
| Moyenne : lecture de τ à 0,37·N₀ | Nouvelle diapo : N(τ) = N₀·e^(−λτ), λτ = 1, e⁻¹ ≈ 0,37 calculé, méthode de lecture, exemple 0,37 × 8,0·10²⁰ ≈ 3,0·10²⁰ → τ ≈ 11,5 j (vue existante courbe.html?courbe=N) | ra_l7b_037 (nouvelle) |
| Moyenne : τ sur a(t) | Puce, voix, cahier : tangente à l'origine ou a(τ) ≈ 0,37·a₀ (car a = λ·N) | ra_a6_courbe_a |
| Moyenne : pénétration α et β | « α arrêtée par une feuille de papier », « β⁻ arrêtée par quelques mm d'aluminium » (puces + cahier) | ra_d1_alpha, ra_d2_beta_moins |
| Moyenne : origine du C14 | Puce + cahier : produit sans arrêt dans la haute atmosphère (neutrons cosmiques, azote), teneur constante ; a₀ défini avec cette hypothèse | ra_c1_principe |
| Moyenne : choix du nucléide, ≈ 40 000 ans | Puces + cahier : 7 × 5730 ≈ 40 000 ans, N₀/2⁷ = N₀/128 < 1 % (calculé) ; plus vieux ⇒ t½ plus grande : uranium 238 / plomb 206 | ra_c4_fils_pere |
| Moyenne : seuil Z < 20 | Lead, puce, cahier « légers (Z < 20) : N ≈ Z » | ra_s2_vallee |
| Basse : élément chimique, abondance | Définition (atomes et ions de même Z) au cahier ; uranium naturel 99,3 % / 0,7 % | ra_n6_isotopes |
| Basse : masses et charges p, n | Puce d'ordres de grandeur (1,67·10⁻²⁷ kg ; ±1,6·10⁻¹⁹ C) | ra_n2_atome |
| Basse : γ, excédent d'énergie, état fondamental | Puce + cahier (Y* excité, Y état fondamental) | ra_d4_gamma |
| Basse : β⁺ surtout artificiels ; He²⁺ | Puces | ra_d3_beta_plus, ra_d1_alpha |
| Basse : liaisons chimiques ; λ indépendante de N₀ | Puce + cahier ; ra_l6 avait 0 puce : 5 puces | ra_r2b_spontanee, ra_l6_lambda |
| Basse : 4 familles | Puce (²³⁸U, ²³⁵U, ²³²Th, ²³⁷Np) | ra_f1_famille |
| Basse : t½ caractéristique du nucléide, ordres de grandeur | Puce + cahier (3,8 j → 4,5·10⁹ ans) | ra_t1_definition |
| Basse : « nombre moyen », curie, Becquerel 1896 | Puces + cahier | ra_a2_definition |
| Basse : a(n·t½) = a₀/2ⁿ ; a = (ln2/t½)·N | Ligne de centre + puce ; puce | ra_a3b_loi_activite, ra_a3_demo |
| Oral seulement (7 cas) | Écrits : λ·t sans unité (ra_l6), ln(a/a₀) = −λt (ra_c2), 1 + r = e^(λt) (ra_c4b), excédent d'énergie (ra_d4), électron créé (ra_d2), « la droite N = Z ne suffit pas » (ra_s2), « N jamais nul » (ra_t3) | 7 diapos |
| Notations | Isotopes sur une horizontale si N en abscisse (ra_s5) ; ⁰₊₁e, « positron » (ra_d3) ; a et non A (ra_a2) ; t₁/₂ (ra_t1) ; t = −(1/λ)·ln(a/a₀) = même relation (ra_c2) ; « constante de désintégration » (ra_l6) ; ln a = ln a₀ − λt (fiche RA9, exigé par le cadre) (ra_a7) | 7 diapos |
| Erreur trouvée | ra_f2_systeme : la voix calculait thorium 232 → plomb 208 alors que la figure écrit uranium 238 → plomb 206 (national 2012 N) : voix refaite sur l'exemple de la figure, pas à pas | ra_f2_systeme |

### Non corrigés et pourquoi
- Chez un seul professeur : 5τ (99 %), « 63 % désintégrés », N₀·2^(−t/t½), « période radioactive » : non ajoutés. L'hypothèse « teneur constante en C14 » (Chouvin) est seulement dite dans la définition de a₀, car la datation en dépend.
- Hors cadre (u, défaut de masse, fission, interaction forte, r = r₀A^(1/3), déviation dans un champ, équation de formation du C14) : non ajoutés.
- La vue courbe.html?courbe=N écrit déjà t½ et « τ = t½/ln2 = 11,5 jours » sur ra_l7_tau / ra_l7b_037, avant la diapo de la demi-vie (simulation non modifiée : à décider).
- L'exercice du bloc ra_s3_b1 (²³⁸U → ²⁰⁶Pb) est maintenant le même calcul que l'exemple de ra_f2 (et le bilan de ra_f1) : proposer ²³²Th → ²⁰⁸Pb (6 α, 4 β⁻) ?
- La question de ra_a5b est sur la 1ʳᵉ diapo de son bloc ra_s5_b2 (pas la dernière) : seul endroit après la mole sans dépasser 4 diapos par bloc.

### Démonstrations
Relues : toutes (14 diapos-preuves, 12 questions/exercices, 9 exercices de blocs, réactions de calcul). Réécrites ou complétées : 21.
- Diapos (une ligne de centre par étape, sur son mot) : ra_l3_equation, ra_l5_loi, ra_l7_tau, ra_l7b_037 (nouv.), ra_t2_demo, ra_t3_paliers, ra_t4_pourcentages (formule parachutée retirée), ra_a3b_loi_activite, ra_a4_unites, ra_a6_courbe_a, ra_a7_droite_ln, ra_c2_demo, ra_c3_calcul, ra_c4b_rapport, ra_f2_systeme.
- Questions / blocs : ra_s1_diagramme/q (partait de 14 − 6 alors que l'énoncé donne N = 8), ra_a2_definition/q (créée), ra_a5b/q (créée), ra_s4_b1 (unité de τ), ra_s4_b3 (unité de a), ra_s5_b1 (m déjà en g, « noyaux »), ra_s6_b1 (n'avait pas de démonstration : reprise de ra_x2/f0) ; ra_l8/q : « 300 noyaux désintégrés » ; réactions écrites de ra_x3/q avec ln(N₀/N) = λt.
- Gardées telles quelles (complètes) : ra_l4/q, ra_t3/q, ra_a5/q, ra_c4b/q, ra_x2/f0, ra_x3/q et e0, ra_x4/q, blocs s1_b1, s2_b2, s2_b3, s3_b1, s4_b2, s5_b3.
Exemples :
1. ra_l3 : « dN = −λ·N·dt » posé → dN = N(t+dt) − N(t) ; désintégrés = N(t) − N(t+dt) = −dN ; −dN = λ·N·dt ; dN = −λ·N·dt ; dN/dt = −λN ; dN/dt + λN = 0.
2. ra_l5 : « dN/dt = −λN₀e^(−λt) = −λN » → N = K·e^(−λt) ; dérivée ; −λKe^(−λt) + λKe^(−λt) = 0 ; N(0) = K·e⁰ = K = N₀ ; N = N₀·e^(−λt).
3. ra_t3 : « on divise par 2 à chaque palier » → N(n·t½) = N₀·e^(−λ·n·t½) = N₀·e^(−n·ln2) ; e^(n·ln2) = 2ⁿ ; N = N₀/2ⁿ.

### Voix à enregistrer (id)
- Pistes de diapo (15, `audio` retiré ou absent) : ra_f2_systeme, ra_l3_equation, ra_l5_loi, ra_l7_tau, ra_l7b_037, ra_t2_demo, ra_t3_paliers, ra_a3b_loi_activite, ra_a4_unites, ra_a5b_masse_inverse, ra_a6_courbe_a, ra_a7_droite_ln, ra_c2_demo, ra_c3_calcul, ra_c4b_rapport.
- Démonstrations : ra_s1_diagramme/q, ra_a2_definition/q, ra_a5b_masse_inverse/q.
- Énoncé et réactions : ra_a5b_masse_inverse/q (enonce_dit ; q/0/1, q/0/2, q/1/1, q/1/2, q/2/juste).
- Blocs (non joués aujourd'hui) : démonstrations ra_s4_b1, ra_s4_b3, ra_s5_b1, ra_s6_b1.

### Vérifications faites (résultats)
- JSON valide, écrit json.dumps(ensure_ascii=False, indent=2), LF, relu juste avant l'écriture ; seules suppressions par rapport à la copie de ce matin : les 14 `audio` des voix/démonstration changées.
- `verif_attente.py` : 61 diapos, 0 mot absent, 0 hors bloc, 0 doublon, 0 compétence inconnue (15 diapos sans voix = celles à enregistrer).
- Script maison : chaque `mot` (centre, pointage, lignes) présent ET dans l'ordre de sa voix ; nouvelles voix sans chiffre, symbole ni tachkil ; chaque diapo dans un seul bloc ; cahiers de blocs = cahiers des diapos ; moments des pointages existants dans les simulations (courbe, tau, nombre, fin, equation, pente, application, resultat, systeme, y, x, conclusion).
- `verifier_figures_cahier.py` : 7 figures, 0 erreur.
- Calculs refaits en Python : λ(Po) = 5,8·10⁻⁸ s⁻¹ ; t½(I) = 6,91·10⁵ s, λ = 1,0·10⁻⁶ s⁻¹, N₀ = 4,0·10¹² ; m₀ = 8,70·10⁻¹⁰ g (pièges 6,64·10⁻¹² et 8,7·10⁻²²) ; pente −0,0485, t½ = 14,3 j ; bois 8268 × 0,2734 = 2,26·10³ ans ; 7 × 5730 = 40 110, 1/128 = 0,78 % ; Pu : 2,78·10⁹ s, 2,49·10⁻¹⁰ s⁻¹, 4,0·10²⁰, 45 ans ; Cd : 2,49·10⁴ s, 4,5·10¹⁶, 5,6·10¹⁵ ; e⁻¹ = 0,368, 0,37 × 8 = 2,96 ; famille U : y = 8, x = 6.
