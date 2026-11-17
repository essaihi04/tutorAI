## Réactions responsables de la libération de l’énergie emmagasinée dans la matière organique

Fichier : `backend/data/courses/en_attente/svt_ch1_reactions_responsables_liberation_energie.json` (repris de la copie en attente, rien de perdu). 48 → 51 diapos, 13 diapos sans audio (voix changée ou nouvelle). Scripts : `scratchpad/svtc1/appliquer.py`, `barres.py`, `m3.py` ; copie d’avant : `scratchpad/svtc1/avant.json`.

### Manques corrigés

| Constat (audit) | Ce qui a été fait | Diapo(s) |
|---|---|---|
| Haute : définition de la respiration cellulaire absente | « Définition : … dégradation complète du glucose en CO₂ et H₂O, en présence de O₂, hyaloplasme puis mitochondrie ; 36 ou 38 ATP » : écran, centre, cahier, voix (« نعاود نقرا ») ; rappel C10_r4 | le_x4_synthese, bloc le_s5_b2 |
| Haute : équation du cycle de Krebs | CH3-CO-CoA + 3 NAD+ + FAD + ADP + Pi + 3 H2O → 2 CO2 + 3 NADH,H+ + FADH2 + ATP + CoA-H : écran, centre, cahier, voix ; rappel C5_r4 | le_k4_sorties, bloc le_s3_b1, le_b1 |
| Haute : équation d’un acide pyruvique dans la matrice | CH3-CO-COOH + 4 NAD+ + FAD + ADP + Pi + 3 H2O → 3 CO2 + 4 NADH,H+ + FADH2 + ATP ; × 2 par glucose (6 CO₂, 8 NADH,H+, 2 FADH₂, 2 ATP) ; atomes vérifiés | le_k5_fois_deux, bloc le_s3_b2, le_b1 |
| Haute : composition chimique de la mitochondrie (cadre « décrire les constituants ») | Nouvelle diapo : membrane externe 40-50 % lipides / 50-60 % protéines, interne 20 / 80 % (transporteurs, sphères), matrice (enzymes, NAD+, FAD, ADP, Pi, ATP, acide pyruvique, pas de glucose) ; vue `mitochondrie.html` réutilisée (moments et repères existants) | **le_m2c_composition** (nouvelle), bloc le_s2_b3 |
| Haute : glucose marqué au ¹⁴C | Nouvelle diapo : tableau T0-T4 du professeur 2 (+), analyse ligne par ligne (constat → donc → conclusion) ; **sans visuel** (tableau de document) | **le_m3a_glucose_marque** (nouvelle), bloc le_s3_b0 |
| Haute : définition de la phosphorylation oxydative | Définition (couplage oxydation des transporteurs réduits / phosphorylation de l’ADP, grâce au gradient) : écran, centre, cahier, voix ; retrouver du bloc mis à jour | le_c7_sphere, bloc le_s4_b1 |
| Moyenne : respiration avec 38 ATP | C6H12O6 + 6 O2 + 38 ADP + 38 Pi → 6 CO2 + 6 H2O + 38 ATP (36 si l’énoncé le dit), localisation écrite | le_r1_compteur, bloc le_s4_b3, le_b1 |
| Moyenne : chaleur et résidu non calculés | 2860 − 1159 = 1701 kJ ≈ 59,5 % (chaleur) ; 2860 − 61 = 2799 kJ surtout dans le résidu | le_r2_rendement, le_r3_comparer, blocs |
| Moyenne : étapes de la fermentation | Lactique : CH3-CO-COOH + NADH,H+ → CH3-CHOH-COOH + NAD+ ; alcoolique : → CH3-CHO + CO2 puis CH3-CHO + NADH,H+ → CH3-CH2-OH + NAD+ ; accepteur final des H nommé | le_f1_lactique, le_f2_alcoolique, bloc le_s4_b3 |
| Moyenne : masse des levures (aérobiose / anaérobiose) | Nouvelle diapo : tableau 150 g → 1,970 g ; 45 g → 0,255 g + éthanol ; calcul par gramme de glucose (≈ 0,013 contre ≈ 0,0057 g, ≈ 2,3 fois) ; **sans visuel** | **le_e3b_masse_levures** (nouvelle), bloc le_s1_b3 |
| Moyenne : protocole d’isolement des mitochondries | Broyage puis centrifugations (noyaux, puis mitochondries) : écran + cahier | le_m3_isolees, bloc le_s3_b0 |
| Basse : fermentation lactique du lait | Lait → yaourt, pH 6,8 → 4,8 (acide lactique) | le_f1_lactique |
| Basse : ADP + Pi dans le milieu des vésicules | Écrit sur l’écran, le cahier et la démonstration | le_c10_vesicules, le_c10b, bloc le_s4_b2 |
| Basse : preuves sans ExAO (eau de chaux, test éthanol, température) | Regroupées sur la nouvelle diapo des levures | le_e3b_masse_levures |
| Basse : adénine + ribose, ATPase | Écran + cahier | le_a1_monnaie |
| Basse : 2860 kJ = bombe calorimétrique | Écran + voix | le_r2_rendement |
| Basse : la chaîne réoxyde NADH,H+ et FADH₂ | Écran + cahier (et conséquence sans O₂ : cycle de Krebs arrêté) | le_c3_decharge, le_c5_o2, bloc le_s3_b2 |
| Oral seulement : membrane interne imperméable aux H⁺ | Écran, centre, cahier | le_c7_sphere |
| Oral seulement : origine des 10 NADH,H+ | 2 + 2 + 6 = 10 ; FADH₂ 2 × 1 = 2 écrits (centre, écran, cahier) | le_k5, le_r1 |
| Oral seulement : déchets minéraux | Écrit (écran, centre, cahier) | le_r3_comparer |
| Oral seulement : coenzyme A n’est pas une enzyme | Écrit | le_k2_acetyl |
| Oral seulement : exemple traité de le_x3 | Correction complète en 8 lignes au centre + cahier (voir démonstrations) | le_x3_chaine_en_panne |
| Notations recommandées | « O2 + 4 H+ + 4 e− → 2 H2O » en variante (le_c5) ; « r = E_ATP/E_glucose × 100 » en variante (le_r2) ; « on dit aussi oxydation complète / incomplète » (le_r3) ; localisation écrite à côté de chaque équation du cahier ; 7 barres à plat corrigées (question le_r2, réactions écrites, rappel C8_r3, attendus) | voir colonne |

Blocs : le_s2_b3 avait 5 diapos ; il garde la structure (le_m1, le_m2, le_m2b, le_m2c) avec un nouvel exercice écrit (QCM composition, réactions juste / 1 / 2, sans audio). Nouveau bloc **le_s3_b0** (le_m3a, le_m3, le_m4 ; retrouver nouveau ; exercice des mitochondries isolées déplacé). Pour garder 3 blocs par séance, les blocs le_s3_b3 et le_s4_b3 descendent d’une séance (ids inchangés) : séance 4 = chaîne respiratoire, séance 5 = fermentations, bilans, cas du bac. Compétences : le_e3b dans C2 et C9, le_m2c dans C4, le_m3a dans C4 et C9.

### Non corrigés et pourquoi

- Manques chez un seul professeur (pHi / pHe des vésicules, CO et tabac, catabolisme / anabolisme, ATP intermédiaire, dessin d’observation) : non exigés par le cadre.
- Lactose → glucose + galactose : non ajouté (détail d’un document, pas une capacité).
- Les tableaux de le_e3b et le_m3a ne sont pas animés (règle 35 : il faudrait une animation, interdite ici) : à créer plus tard.
- « 36 ou 38 ATP » (règle SVT du 17 novembre) : appliqué au texte nouveau (définition de la respiration) ; le reste du cours garde « 38 ATP (36 si l’énoncé le dit) », comme la fiche du cadre : harmonisation à décider.
- le_e2 dit « jusqu’à 0 mg/L vers 8 min » alors que la simulation s’arrête au moment `respiration` (≈ 1 mg/L) ; l’épuisement est montré à la diapo suivante.
- le_s2_b3 n’a pas de question « À toi » (la diapo le_m2b, légende à poser, en tient lieu) ; le_m3a et le_e3b n’ont pas de question (une par bloc déjà).
- speech_text.fr de le_r2 et le_r3 gardent des barres à plat dans leurs anciennes phrases (texte dit, non écrit au tableau).

### Démonstrations (relues, réécrites, 3 exemples avant → après en une ligne chacun)

Relues : 9 démonstrations (questions le_t2, le_g3, le_c10b, le_r2 ; exercice le_x2 ; blocs le_s3_b1, le_s3_b3, le_s5_b1, le_s5_b2) et 12 exemples écrits au centre / cahier. Réécrites : 4 démonstrations (le_t2, le_c10b, le_x2 + sa copie du bloc le_s5_b1) et les exemples de 8 diapos (le_e2, le_k5, le_r1, le_r2, le_r3, le_x3) + 2 nouvelles analyses (le_e3b, le_m3a). Gardées complètes : le_g3, le_r2 (question), le_s3_b1 (8 NADH,H+), le_s3_b3, le_s5_b2 (2,13 %). Calculs vérifiés en python (1159, 40,5 %, 1701, 59,5 %, 61, 2,13 %, 2799, 0,013, 0,0057, 2,3, 6,9 UA, 8,25 min, 10, 8, 38) ; équations de la matrice équilibrées (C, H, O).
- le_x3 : « méthode seule à l’écran » → 8 lignes : 4 périodes avec valeurs (100 %, 96 %, 96 → 40 %, ATP 10 → 90 UA, paliers 40 % / 90 UA), « donc » (couplage), hypothèse au conditionnel, flèches, « vérifiée, car [O₂] reste à 40 % ».
- le_r2 / le_r3 (centre) : « r = (38 × 30,5)/2860 × 100 → 40,5 % » → AN / r = 1159/2860 × 100 / ≈ 0,405 / 0,405 × 100 = 40,5 % / chaleur 2860 − 1159 = 1701 kJ ≈ 59,5 % (idem 61/2860 ≈ 0,0213 → 2,13 %, puis 2799 kJ).
- le_t2 (question) : « il gagne des électrons → réduit » → 2 H = 2 H+ + 2 e− / FAD + 2 H+ + 2 e− → FADH2 / gagne 2 électrons / règle « gagner des électrons, c’est être réduit » / donc réduit. (Aussi le_c10b : les trois conditions vérifiées une par une, puis « Réponse : non, car pas de gradient » ; le_x2 : conclusion avec les rendements 40,5 % et 2,13 %.)

### Voix à enregistrer (id)

- Diapos (speech_text.mixed, audio retiré) : le_e2_decrire, **le_e3b_masse_levures**, **le_m2c_composition**, **le_m3a_glucose_marque**, le_k4_sorties, le_k5_fois_deux, le_c7_sphere, le_f2_alcoolique, le_r1_compteur, le_r2_rendement, le_r3_comparer, le_x3_chaine_en_panne, le_x4_synthese.
- Démonstrations (parole) : le_t2_reduit/question, le_c10b_vesicules_cas/question, le_x2_qui_respire/exercises[0], bloc le_s5_b1/exercice.
- Blocs : le_s2_b3/exercice (énoncé + 5 réactions), le_s3_b0/retrouver (énoncé) — non joués aujourd’hui (fin de cours).

### Vérifications faites (résultats)

- JSON valide, `ensure_ascii=False`, `indent=2`, LF (0 CR) ; fichier relu juste avant chaque écriture (identique à la lecture).
- `verif_attente.py` : 51 diapos, 0 mot absent, 0 hors bloc, 0 doublon, 0 compétence inconnue, 13 diapos sans voix (celles listées).
- Script maison : mots des démonstrations présents et dans l’ordre, centres dans l’ordre de la voix, apres_mot de l’observation présent, chaque diapo dans sa compétence, ordre des blocs = ordre du cours ; voix et paroles nouvelles sans chiffre ni symbole ; 1 alerte fausse (« complète / incomplète », des mots).
- Moments et repères cités existent (mitochondrie.html : membrane_externe… spheres_pedonculees, medaillon ; exao.html : respiration, ajout_glucose_rien, ajout_pyruvate, o2_baisse_atp_monte, palier_final, hypothese).
- `scripts/verifier_formules.py` : 13 → 0 relation à remettre. `verifier_figures_cahier.py` : 8 figures, 0 erreur.
