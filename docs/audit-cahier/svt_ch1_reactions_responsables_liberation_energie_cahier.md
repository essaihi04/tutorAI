# Cahier de l'élève — SVT ch1 « Réactions responsables de la libération de l'énergie »

18 novembre 2026. Skill `cahier-de-l-eleve`. Fichiers : `backend/data/courses/svt_ch1_reactions_responsables_liberation_energie.json`
(en ligne) et `backend/data/courses/en_attente/…` (copie en attente). Script : scratchpad `svt_ch1_…/donnees.py` +
`appliquer.py` (relançable, ne pose que les 4 champs du cahier).

**Affichage.** L'application écrit déjà le titre de partie (« I. … ») au-dessus des lignes. Quand un bloc chevauche deux
parties, elle affiche tous les titres de partie en haut : la ligne qui finit la partie précédente commence donc par
« Suite du V — 4. … » (ou « VIII — 1. … » quand la 2e partie commence au milieu du bloc).

## Différences de plan de la copie en attente

En ligne : Ouverture · I ATP · II Respiration et fermentation · III Transporteurs et glycolyse · IV Mitochondrie (structure,
puis expériences ¹⁴C et mitochondries isolées) · V Matrice · VI Chaîne respiratoire (c1…c10b) · VII Fermentations · VIII Bilans ·
IX Cas types · X Bilan.
En attente : Ouverture · I ATP (rappel, une diapo, sans 30,5 kJ) · II Mise en évidence (+ levures au microscope, **définitions**
le_e5, carte) · **III Où se passe chaque étape ?** (¹⁴C, mitochondries isolées, avant la glycolyse) · IV Transporteurs et
glycolyse · V Mitochondrie (structure, composition) · VI Matrice · VII Chaîne (vésicules et cyanure AVANT le schéma du
national) · VIII Fermentations · IX Bilans · X Cas types (restitution, relier réaction et phénomène 2020 R, 2016 N, chaîne en
panne en 3 temps) et synthèse · XI Bilan. Le cahier de chaque fichier suit sa propre numérotation.

## Le cahier idéal (cours en ligne)

**Ouverture.** 1. Toute cellule consomme de l'énergie en permanence, tirée de la matière organique (glucose). 2. La cellule :
membrane plasmique, hyaloplasme, noyau, mitochondries *(dessin : cellule légendée)*. 3. Le glucose C₆H₁₂O₆ (6 C) : énergie
chimique dans ses liaisons, libérée pas à pas *(dessin : chaîne droite de 6 billes jaunes)*. 4. La matière organique vient
de la photosynthèse.

**I. L'ATP.** 1. ATP = adénosine (adénine + ribose) + 3 phosphates. 2. Hydrolyse : ATP + H₂O → ADP + Pi + énergie
(30,5 kJ/mol), énergie utilisable. 3. Phosphorylation : ADP + Pi + énergie → ATP (énergie du glucose). Remarque : l'ATP est
régénéré en permanence *(dessin : cycle ATP ⇄ ADP + Pi)*.

**II. Respiration et fermentation.** 1. ExAO : [O₂] 7,5 → 0 mg/L après le glucose, CO₂ ↑ → donc respiration ;
C₆H₁₂O₆ + 6 O₂ → 6 CO₂ + 6 H₂O + énergie *(courbe [O₂]–t)*. 2. Sans O₂ : CO₂ + éthanol : fermentation. 3. 2,3 fois plus de
levures avec O₂. Méthode : décrire puis « donc ». 4. Carte : glucose → glycolyse → respiration / fermentation.

**III. Transporteurs et glycolyse.** 1. 2 H = 2 H⁺ + 2 e⁻ ; NAD⁺ + 2 H⁺ + 2 e⁻ → NADH,H⁺ ; FAD → FADH₂. 2. Gagner des e⁻ =
réduit, perdre = oxydé (Attention : NAD⁺ → NADH,H⁺ est une réduction). 3. Glycolyse : équation-bilan avec 2 NAD⁺, 2 ADP +
2 Pi ; gain net 2 ATP ; définition *(dessin : 6 billes → 2 × 3 billes, 2 NADH,H⁺, 2 ATP nets)*.

**IV. La mitochondrie.** 1. Levures avec / sans O₂. 2. Définition + 6 légendes *(dessin : coupe légendée comme au bac)*.
3. Composition. 4. Glucose ¹⁴C → donc. 5. Mitochondries isolées → acide pyruvique. 6. ADP + Pi : O₂ et ATP couplés ; conditions
*(courbe : [O₂] et ATP, ajouts à 1 ; 2,5 ; 4,5 ; 8 min, valeurs 100 → 96 → 40 % et 10 → 90 UA)*.

**V. La matrice.** 1. Décarboxylation + déshydrogénation : équation de l'acétyl-CoA *(dessin : 3 billes → CO₂ + acétyl 2 C–CoA)*.
2. Cycle de Krebs (2 C + 4 C → 6 C, 4 C régénéré). 3. Un tour : 2 CO₂, 3 NADH,H⁺, 1 FADH₂, 1 ATP + équation *(roue de Krebs)*.
Attention : ce CO₂ ne vient pas du dioxygène. 4. × 2 par glucose : 6 CO₂, 8 NADH,H⁺ ; avec la glycolyse 10 NADH,H⁺, 2 FADH₂.

**VI. Chaîne respiratoire et phosphorylation oxydative.** 1. Pulse d'O₂ : [H⁺] 20 → 44 × 10⁻⁹ mol/L puis retour *(courbe)*.
2. Membrane interne. 3. NADH,H⁺ → NAD⁺ + 2 H⁺ + 2 e⁻. 4. Définition de la chaîne. 5. ½ O₂ + 2 H⁺ + 2 e⁻ → H₂O, accepteur final.
6. Pompage des H⁺, gradient *(dessin : T1–T4 violets, e⁻ bleus, H⁺ roses)*. 7. Retour par les sphères, définition de la
phosphorylation oxydative *(dessin : sphère pédonculée)*. 8. Légender le schéma du national : 1–4, A, B, C *(schéma légendé
comme au bac)*. 9. Cyanure en flèches. 10. Vésicules : gradient + sphères nécessaires *(dessin : vésicule pH 4 / pH 8)*.

**VII. Fermentations.** Lactique et alcoolique (équations), accepteur final, définition *(dessin : acide pyruvique → acide
lactique ou éthanol + CO₂)*. **VIII. Bilans.** 38 ATP (4 directs + 10 × 3 + 2 × 2), r ≈ 40,5 % ; fermentation 2,13 %
*(barres de rendement)*. **IX. Cas types.** Méthodes : définir, sens des H⁺, comparer, décrire → déduire → expliquer →
hypothèse → vérifier. **X. Bilan** : définition de la respiration cellulaire, les deux voies avec leurs nombres.

Couleurs des dessins (lexique → palette du cahier) : carbone jaune, NAD cyan, FAD vert, H⁺ rose, e⁻ bleu, transporteurs
violets, ATP (doré) orange, membrane externe orange, membrane interne et sphères jaunes (dorées), matrice bleu, hyaloplasme vert,
noyau violet.

## Découpage

Bulles des diapositives : une phrase ou deux (≤ 180 caractères) par diapositive, dans `donnees.py` (BULLES, BULLES_EN_LIGNE,
BULLES_ATTENTE). Chaque dessin est posé sur la diapo qui l'enseigne et dans son bloc.

### Cours en ligne (`backend/data/courses/svt_ch1_reactions_responsables_liberation_energie.json`)

**le_s1_b1** — diapos : le_o1_trois_vivants, le_p1_cellule, le_p2_glucose  
- 1. Toute cellule vivante consomme de l'énergie en permanence.
- Elle tire cette énergie de la matière organique, surtout du glucose.
- 2. La cellule : membrane plasmique, hyaloplasme (liquide intérieur), noyau, mitochondries.
- 3. Le glucose C₆H₁₂O₆ (6 C) : énergie chimique rangée dans les liaisons de ses atomes.
- Elle est libérée quand ces liaisons sont cassées, pas à pas.
- *Figures :* La cellule ; Le glucose : 6 carbones

**le_s1_b2** — diapos : le_o2_acquis, le_a1_monnaie, le_a2_recharge  
- Suite de l'ouverture — 4. La matière organique est fabriquée par la photosynthèse.
- 1. ATP = adénosine (adénine + ribose) + 3 phosphates.
- 2. Hydrolyse (enzyme : ATPase) : ATP + H₂O → ADP + Pi + énergie (30,5 kJ par mole).
- C'est l'énergie utilisable par la cellule (contraction, synthèses…).
- 3. Phosphorylation : ADP + Pi + énergie → ATP ; l'énergie vient de la dégradation du glucose.
- Remarque : l'ATP ne se stocke presque pas, il est régénéré en permanence.
- *Figures :* L'ATP, utilisé puis rechargé

**le_s1_b3** — diapos : le_e1_mesurer, le_e2_decrire, le_e3_sans_o2, le_e3b_masse_levures  
- 1. ExAO : levures en milieu aéré, glucose injecté à 2 min ; on mesure [O₂] et CO₂.
- Avant : [O₂] stable vers 7,5 mg/L ; après : [O₂] ↓ de 7,5 à 0 mg/L (vers 8 min), CO₂ ↑.
- Donc, avec O₂ (aérobiose), les levures respirent : C₆H₁₂O₆ + 6 O₂ → 6 CO₂ + 6 H₂O + énergie
- 2. Sans O₂ (anaérobiose) : CO₂ toujours produit et éthanol formé : fermentation alcoolique.
- 3. Avec O₂, 2,3 fois plus de levures par g de glucose : la respiration libère plus d'énergie.
- Méthode : décrire d'abord (avant / après, avec les valeurs), puis déduire avec « donc ».
- *Figures :* [O₂] autour des levures

**le_s2_b1** — diapos : le_e4_carte, le_t1_deux_h, le_t2_reduit  
- Suite du II — 4. Carte : glucose → glycolyse (hyaloplasme) → acide pyruvique ;
- avec O₂ : respiration (mitochondrie) ; sans O₂ : fermentation (hyaloplasme).
- 1. Dégrader une molécule organique, c'est lui arracher des hydrogènes (2 H = 2 H⁺ + 2 e⁻).
- NAD⁺ (transporteur d'hydrogène) : NAD⁺ + 2 H⁺ + 2 e⁻ → NADH,H⁺ ; de même FAD → FADH₂.
- 2. Gagner des électrons = être réduit ; perdre des électrons = être oxydé.
- Attention : NAD⁺ → NADH,H⁺ est une réduction (et non une oxydation).
- *Figures :* aucune

**le_s2_b2** — diapos : le_g1_ou, le_g2_six_carbones, le_g3_bilan  
- 3. La glycolyse (hyaloplasme, sans O₂) : glucose (6 C) → 2 acides pyruviques (3 C).
- 2 ATP dépensés, 4 ATP formés : gain net 4 − 2 = 2 ATP ; 2 NAD⁺ réduits en 2 NADH,H⁺.
- C₆H₁₂O₆ + 2 ADP + 2 Pi + 2 NAD⁺ → 2 CH₃-CO-COOH + 2 ATP + 2 NADH,H⁺
- Définition : la glycolyse est la dégradation du glucose en 2 acides pyruviques (hyaloplasme).
- Elle se fait sans O₂ et elle est commune à la respiration et à la fermentation.
- Attention : écrire 2 NAD⁺ et 2 ADP + 2 Pi à gauche ; gain net = 2 ATP (et non 4).
- *Figures :* La glycolyse : 6 C → 2 × 3 C

**le_s2_b3** — diapos : le_m1_deux_levures, le_m2_legender, le_m2b_construire, le_m2c_composition  
- 1. Avec O₂, mitochondries nombreuses et développées, alors que sans O₂ elles sont rares.
- 2. Définition : la mitochondrie est un organite à double membrane, siège de la respiration.
- Légende : membrane externe, membrane interne (crêtes), espace intermembranaire,
- matrice, sphères pédonculées (sur la membrane interne, tête vers la matrice).
- 3. Membrane interne : 80 % de protéines (transporteurs, sphères) ; externe : 50 à 60 %.
- Matrice : enzymes, NAD⁺, FAD, ADP, Pi, acide pyruvique ; pas de glucose.
- *Figures :* La mitochondrie en coupe

**le_s3_b0** — diapos : le_m3a_glucose_marque, le_m3_isolees, le_m4_o2_atp  
- 4. Glucose ¹⁴C : radioactivité → acide pyruvique (hyaloplasme) → mitochondrie → CO₂.
- Donc glycolyse dans le hyaloplasme ; l'acide pyruvique est dégradé dans la matrice.
- 5. Mitochondries isolées + glucose : [O₂] stable ; + acide pyruvique : [O₂] diminue.
- Donc la mitochondrie n'utilise pas le glucose mais l'acide pyruvique.
- 6. + ADP + Pi : [O₂] ↓ de 96 à 40 % et ATP ↑ de 10 à 90 UA : O₂ consommé et ATP produit couplés.
- Conditions de la synthèse d'ATP : acide pyruvique, ADP + Pi et O₂.
- *Figures :* Mitochondries isolées : O₂ et ATP

**le_s3_b1** — diapos : le_k1_pyruvate, le_k2_acetyl, le_k3_roue, le_k4_sorties  
- 1. Dans la matrice, l'acide pyruvique est décarboxylé (CO₂) et déshydrogéné (NADH,H⁺).
- CH₃-CO-COOH + CoA-H + NAD⁺ → CH₃-CO-CoA + CO₂ + NADH,H⁺ (acétyl-CoA)
- 2. Cycle de Krebs : l'acétyl (2 C) se fixe sur un composé à 4 C, régénéré à la fin du tour.
- 3. Un tour : 2 CO₂, 3 NADH,H⁺, 1 FADH₂, 1 ATP.
- CH₃-CO-CoA + 3 NAD⁺ + FAD + ADP + Pi + 3 H₂O → 2 CO₂ + 3 NADH,H⁺ + FADH₂ + ATP + CoA-H
- Attention : ce CO₂ vient des décarboxylations, pas du dioxygène.
- *Figures :* Acide pyruvique → acétyl-CoA ; Un tour du cycle de Krebs

**le_s3_b2** — diapos : le_k5_fois_deux, le_c1_pulse, le_c2_membrane, le_c3_decharge  
- Suite du V — 4. Par glucose (× 2) : 6 CO₂, 8 NADH,H⁺, 2 FADH₂, 2 ATP dans la matrice.
- Avec la glycolyse : 10 NADH,H⁺ et 2 FADH₂ ; l'énergie est surtout dans ces transporteurs.
- 1. Injection d'O₂ à des mitochondries riches en NADH,H⁺ : [H⁺] ↑ de 20 à 44 × 10⁻⁹ mol/L,
- puis revient à sa valeur initiale (vers 300 s).
- 2. Membrane interne : transporteurs (T1 à T4) et sphères pédonculées (tête côté matrice).
- 3. NADH,H⁺ → NAD⁺ + 2 H⁺ + 2 e⁻ : les transporteurs réduits sont oxydés ; NAD⁺ et FAD resservent.
- *Figures :* [H⁺] du milieu après un peu d'O₂

**le_s3_b3** — diapos : le_c4_relais, le_c5_o2, le_c6_protons  
- 4. Définition : la chaîne respiratoire est un ensemble de transporteurs de la membrane interne
- qui transfèrent les électrons (T1 → T4) par des réactions d'oxydoréduction.
- 5. ½ O₂ + 2 H⁺ + 2 e⁻ → H₂O : le dioxygène est l'accepteur final des électrons.
- Sans O₂ : chaîne arrêtée, NADH,H⁺ et FADH₂ non réoxydés, cycle de Krebs arrêté.
- 6. Le passage des électrons pompe les H⁺ de la matrice vers l'espace intermembranaire.
- Il se forme un gradient de protons (il explique le pic de [H⁺] de l'expérience).
- *Figures :* La chaîne respiratoire pompe les H⁺

**le_s4_b1** — diapos : le_c7_sphere, le_c8_national, le_c8b_construire, le_c9_poison  
- 7. Les H⁺ reviennent dans la matrice par les sphères pédonculées seulement : ADP + Pi → ATP.
- Définition : la phosphorylation oxydative est la phosphorylation de l'ADP en ATP couplée
- à l'oxydation des transporteurs réduits par la chaîne respiratoire (gradient de protons).
- 8. Légender : 1 membrane interne, 2 sphère pédonculée, 3 espace intermembranaire, 4 matrice ;
- A oxydation de NADH,H⁺, B réduction de O₂ en H₂O, C phosphorylation de l'ADP.
- 9. Cyanure → électrons arrêtés → O₂ non consommé → pas de pompage → pas de gradient → pas d'ATP.
- *Figures :* La sphère pédonculée fait l'ATP ; La chaîne respiratoire, légendée (bac)

**le_s4_b2** — diapos : le_c10_vesicules, le_c10b_vesicules_cas  
- 10. Vésicules de membrane interne (sphères vers l'extérieur) + ADP + Pi :
- pH égaux → pas d'ATP ; intérieur acide (pH 4, dehors pH 8) → ATP ; sans sphères → pas d'ATP.
- Donc la synthèse d'ATP nécessite un gradient de protons et les sphères pédonculées.
- *Figures :* Vésicule : intérieur acide → ATP

**le_s4_b3** — diapos : le_f1_lactique, le_f2_alcoolique, le_r1_compteur, le_r2_rendement  
- 1. Fermentation lactique : C₆H₁₂O₆ + 2 ADP + 2 Pi → 2 CH₃-CHOH-COOH + 2 ATP
- 2. Fermentation alcoolique : C₆H₁₂O₆ + 2 ADP + 2 Pi → 2 CH₃-CH₂-OH + 2 CO₂ + 2 ATP
- NADH,H⁺ rend ses H à l'acide pyruvique (lactique) ou à l'éthanal (alcoolique) : NAD⁺ régénéré.
- Définition : fermentation = dégradation incomplète du glucose, sans O₂, dans le hyaloplasme.
- VIII — 1. 4 ATP directs + 10 NADH,H⁺ × 3 + 2 FADH₂ × 2 = 38 ATP par glucose (ou 36).
- 2. Rendement : r = (38 × 30,5)/2860 × 100 ≈ 40,5 % ; le reste (1701 kJ) part en chaleur.
- *Figures :* Les deux fermentations

**le_s5_b1** — diapos : le_r3_comparer, le_x1_restitution, le_x2_qui_respire  
- Suite du VIII — 3. Fermentation : r = (2 × 30,5)/2860 × 100 ≈ 2,13 %.
- Respiration : dégradation complète (CO₂, H₂O) ; fermentation : incomplète (résidu organique).
- 1. Méthode (définir) : nature + lieu (et conditions) + produits.
- Sens des H⁺ : chaîne, matrice → espace intermembranaire ; sphère, espace → matrice.
- 2. Méthode (comparer) : critère par critère, « plus élevé chez… (valeur) que chez… (valeur) ».
- Puis conclure par la voie dominante : A respire surtout, B fermente davantage.
- *Figures :* Rendement : respiration et fermentation

**le_s5_b2** — diapos : le_x3_chaine_en_panne, le_x4_synthese, le_b1_bilan, le_b2_carte  
- Suite du IX — 3. Méthode : décrire (périodes, valeurs) → déduire (« donc ») → expliquer (flèches)
- → hypothèse au conditionnel → vérifiée ou rejetée, avec la donnée du document.
- Ex. : « le cyanure bloquerait la chaîne » : vérifiée, car [O₂] reste à 40 % et l'ATP à 90 UA.
- 4. Définition : la respiration cellulaire est une dégradation complète du glucose en CO₂ et H₂O,
- avec O₂, dans le hyaloplasme puis la mitochondrie : 36 ou 38 ATP par glucose.
- Bilan : avec O₂ → respiration (38 ATP, 40,5 %) ; sans O₂ → fermentation (2 ATP, 2,13 %).
- *Figures :* Mitochondries isolées : O₂ et ATP

### Copie en attente (`backend/data/courses/en_attente/svt_ch1_reactions_responsables_liberation_energie.json`)

**le_s1_b1** — diapos : le_o1_trois_vivants, le_o2_acquis, le_p1_cellule, le_p2_glucose  
- 1. Toute cellule vivante consomme de l'énergie en permanence.
- Elle la tire de la matière organique (glucose, amidon), fabriquée par la photosynthèse.
- 2. La cellule : membrane plasmique, hyaloplasme (liquide intérieur), noyau, mitochondries.
- 3. Le glucose C₆H₁₂O₆ (6 C) : énergie chimique rangée dans les liaisons de ses atomes.
- Elle est libérée quand ces liaisons sont cassées, pas à pas.
- *Figures :* La cellule ; Le glucose : 6 carbones

**le_s1_b2** — diapos : le_a1_monnaie, le_e1_mesurer, le_e2_decrire, le_e3_sans_o2  
- 1. Hydrolyse : ATP + H₂O → ADP + Pi + énergie, l'énergie utilisable par la cellule.
- 2. Phosphorylation : ADP + Pi + énergie → ATP, grâce à la dégradation du glucose.
- II — 1. ExAO : glucose injecté à 2 min ; [O₂] ↓ de 7,5 à 0 mg/L (vers 8 min) et CO₂ ↑.
- Donc, avec O₂ (aérobiose), les levures respirent : C₆H₁₂O₆ + 6 O₂ → 6 CO₂ + 6 H₂O + énergie
- 2. O₂ épuisé : CO₂ toujours produit et éthanol formé : fermentation (anaérobiose).
- Méthode : décrire d'abord (avant / après, avec les valeurs), puis déduire avec « donc ».
- *Figures :* L'ATP, utilisé puis rechargé ; [O₂] autour des levures

**le_s1_b3** — diapos : le_e3b_masse_levures, le_m1_deux_levures, le_e5_definitions, le_e4_carte  
- 3. Avec O₂, 2,3 fois plus de levures par g de glucose : la respiration libère plus d'énergie.
- 4. Avec O₂, mitochondries nombreuses et développées, alors que sans O₂ elles sont rares.
- 5. Définition : la respiration est une dégradation complète du glucose en CO₂ et H₂O, avec O₂.
- Définition : la fermentation est une dégradation incomplète du glucose, sans O₂ (résidu organique).
- La respiration libère beaucoup d'énergie, la fermentation peu.
- 6. Carte : glucose → glycolyse (hyaloplasme) → avec O₂ : respiration ; sans O₂ : fermentation.
- *Figures :* aucune

**le_s2_b1** — diapos : le_m3a_glucose_marque, le_m3_isolees, le_m4_o2_atp  
- 1. Glucose ¹⁴C : radioactivité → acide pyruvique (hyaloplasme) → mitochondrie → CO₂.
- Donc le glucose devient acide pyruvique dans le hyaloplasme, dégradé ensuite dans la mitochondrie.
- 2. Mitochondries isolées + glucose : [O₂] stable ; + acide pyruvique : [O₂] diminue.
- Donc la mitochondrie n'utilise pas le glucose mais l'acide pyruvique.
- 3. + ADP + Pi : [O₂] ↓ de 96 à 40 % et ATP ↑ de 10 à 90 UA : O₂ consommé et ATP produit couplés.
- Conditions de la synthèse d'ATP : acide pyruvique, ADP + Pi et O₂.
- *Figures :* Mitochondries isolées : O₂ et ATP

**le_s2_b2** — diapos : le_t1_deux_h, le_t2_reduit  
- 1. Dégrader une molécule organique, c'est lui arracher des hydrogènes (2 H = 2 H⁺ + 2 e⁻).
- NAD⁺ (transporteur d'hydrogène) : NAD⁺ + 2 H⁺ + 2 e⁻ → NADH,H⁺ ; de même FAD → FADH₂.
- 2. Gagner des électrons = être réduit ; perdre des électrons = être oxydé.
- Attention : NAD⁺ → NADH,H⁺ est une réduction (et non une oxydation).
- *Figures :* aucune

**le_s2_b3** — diapos : le_g1_ou, le_g2_six_carbones, le_g3_bilan  
- 3. La glycolyse (hyaloplasme, sans O₂, prouvé au III) : glucose (6 C) → 2 acides pyruviques.
- 2 ATP dépensés, 4 ATP formés : gain net 4 − 2 = 2 ATP ; 2 NAD⁺ réduits en 2 NADH,H⁺.
- C₆H₁₂O₆ + 2 ADP + 2 Pi + 2 NAD⁺ → 2 CH₃-CO-COOH + 2 ATP + 2 NADH,H⁺
- Définition : la glycolyse est la dégradation du glucose en 2 acides pyruviques (hyaloplasme).
- Elle se fait sans O₂ et elle est commune à la respiration et à la fermentation.
- Attention : écrire 2 NAD⁺ et 2 ADP + 2 Pi à gauche ; gain net = 2 ATP (et non 4).
- *Figures :* La glycolyse : 6 C → 2 × 3 C

**le_s3_b1** — diapos : le_m2_legender, le_m2b_construire, le_m2c_composition  
- 1. Définition : la mitochondrie est un organite à double membrane, siège de la respiration.
- Légende : membrane externe, membrane interne (crêtes), espace intermembranaire,
- matrice, sphères pédonculées (sur la membrane interne, tête vers la matrice).
- 2. Membrane interne : 80 % de protéines (transporteurs, sphères) ; externe : 50 à 60 %.
- Matrice : enzymes (décarboxylases, déshydrogénases), NAD⁺, FAD, ADP, Pi ; pas de glucose.
- *Figures :* La mitochondrie en coupe

**le_s3_b2** — diapos : le_k1_pyruvate, le_k2_acetyl, le_k3_roue  
- 1. Dans la matrice, l'acide pyruvique est décarboxylé (CO₂) et déshydrogéné (NADH,H⁺).
- CH₃-CO-COOH + CoA-H + NAD⁺ → CH₃-CO-CoA + CO₂ + NADH,H⁺ (acétyl-CoA)
- Attention : ce CO₂ vient de la décarboxylation, pas du dioxygène.
- 2. Cycle de Krebs : l'acétyl (2 C) se fixe sur un composé à 4 C, régénéré à la fin du tour.
- *Figures :* Acide pyruvique → acétyl-CoA

**le_s3_b3** — diapos : le_k4_sorties, le_k5_fois_deux  
- 3. Un tour : 2 CO₂, 3 NADH,H⁺, 1 FADH₂, 1 ATP.
- CH₃-CO-CoA + 3 NAD⁺ + FAD + ADP + Pi + 3 H₂O → 2 CO₂ + 3 NADH,H⁺ + FADH₂ + ATP + CoA-H
- 4. Par glucose (× 2) : 6 CO₂, 8 NADH,H⁺, 2 FADH₂, 2 ATP dans la matrice.
- Avec la glycolyse : 10 NADH,H⁺ et 2 FADH₂ ; l'énergie est surtout dans ces transporteurs.
- Attention : 1 glucose = 2 acides pyruviques = 2 tours : tout se compte × 2.
- *Figures :* Un tour du cycle de Krebs

**le_s4_b1** — diapos : le_c1_pulse, le_c2_membrane, le_c3_decharge  
- 1. Injection d'O₂ à des mitochondries riches en NADH,H⁺ : [H⁺] ↑ de 20 à 44 × 10⁻⁹ mol/L,
- puis revient à sa valeur initiale (vers 300 s).
- 2. Membrane interne : transporteurs (T1 à T4) et sphères pédonculées (tête côté matrice).
- 3. NADH,H⁺ → NAD⁺ + 2 H⁺ + 2 e⁻ : les transporteurs réduits sont oxydés à la membrane interne.
- NAD⁺ et FAD redeviennent disponibles pour la glycolyse et le cycle de Krebs.
- *Figures :* [H⁺] du milieu après un peu d'O₂

**le_s4_b2** — diapos : le_c4_relais, le_c5_o2, le_c6_protons, le_c7_sphere  
- 4. Chaîne respiratoire : transporteurs de la membrane interne, relais des e⁻ par oxydoréduction.
- 5. ½ O₂ + 2 H⁺ + 2 e⁻ → H₂O : le dioxygène est l'accepteur final des électrons.
- 6. Le passage des électrons pompe les H⁺ de la matrice vers l'espace : gradient de protons.
- 7. Les H⁺ reviennent dans la matrice par les sphères pédonculées seulement : ADP + Pi → ATP.
- Définition : la phosphorylation oxydative est la phosphorylation de l'ADP en ATP couplée
- à l'oxydation des transporteurs réduits par la chaîne respiratoire (gradient de protons).
- *Figures :* La chaîne respiratoire pompe les H⁺ ; La sphère pédonculée fait l'ATP

**le_s4_b3** — diapos : le_c10_vesicules, le_c10b_vesicules_cas, le_c9_poison, le_c8_national, le_c8b_construire  
- 8. Vésicules + ADP + Pi : pH égaux → pas d'ATP ; intérieur acide (pH 4, dehors 8) → ATP.
- Sans sphères, même gradient → pas d'ATP : il faut un gradient de H⁺ et les sphères.
- 9. Cyanure → électrons arrêtés → O₂ non consommé → pas de pompage → pas de gradient → pas d'ATP.
- 10. Légender : 1 membrane interne, 2 sphère pédonculée, 3 espace intermembranaire, 4 matrice ;
- A oxydation de NADH,H⁺, B réduction de O₂ en H₂O, C phosphorylation de l'ADP.
- Méthode : repérer d'abord la tête des sphères pédonculées : elle est côté matrice.
- *Figures :* Vésicule : intérieur acide → ATP ; La chaîne respiratoire, légendée (bac)

**le_s5_b1** — diapos : le_f1_lactique, le_f2_alcoolique  
- 1. Lactique : CH₃-CO-COOH + NADH,H⁺ → CH₃-CHOH-COOH + NAD⁺ (NAD⁺ régénéré).
- C₆H₁₂O₆ + 2 ADP + 2 Pi → 2 CH₃-CHOH-COOH + 2 ATP (muscle, bactéries du lait)
- 2. Alcoolique : CH₃-CO-COOH → CH₃-CHO + CO₂ ; CH₃-CHO + NADH,H⁺ → CH₃-CH₂-OH + NAD⁺
- C₆H₁₂O₆ + 2 ADP + 2 Pi → 2 CH₃-CH₂-OH + 2 CO₂ + 2 ATP (levure)
- Définition : la fermentation est une dégradation incomplète du glucose, sans O₂ (hyaloplasme).
- Elle laisse un résidu organique et ne donne que 2 ATP, ceux de la glycolyse.
- *Figures :* Les deux fermentations

**le_s5_b2** — diapos : le_r1_compteur, le_r2_rendement, le_r3_comparer  
- 1. NADH,H⁺ = 2 + 2 + 6 = 10 ; FADH₂ = 2 ; 1 NADH,H⁺ → 3 ATP ; 1 FADH₂ → 2 ATP.
- Bilan = 2 + 2 + (10 × 3) + (2 × 2) = 38 ATP par glucose (on retient 36 ou 38).
- C₆H₁₂O₆ + 6 O₂ + 38 ADP + 38 Pi → 6 CO₂ + 6 H₂O + 38 ATP
- 2. Rendement = part de l'énergie du glucose mise dans l'ATP : r = (38 × 30,5)/2860 × 100 ≈ 40,5 %.
- 3. Fermentation : r = (2 × 30,5)/2860 × 100 ≈ 2,13 % : l'énergie reste dans le résidu organique.
- Respiration : dégradation complète (CO₂, H₂O) ; fermentation : incomplète (résidu organique).
- *Figures :* Rendement : respiration et fermentation

**le_s6_b1** — diapos : le_x1_restitution, le_x1b_protons, le_x1c_qcm  
- 1. Méthode (définir) : nature + lieu et conditions + produits.
- Ex. (2024 R) : fermentation lactique = dégradation incomplète du glucose, hyaloplasme, sans O₂,
- avec production d'acide lactique et peu d'énergie (2 ATP).
- 2. Sens des H⁺ : chaîne, matrice → espace intermembranaire ; sphère, espace → matrice.
- 3. Méthode (QCM) : refaire le schéma, puis chercher le mot faux (lieu, sens, nombre, produit).
- *Figures :* La chaîne respiratoire, légendée (bac)

**le_s6_b1b** — diapos : le_x1d_reactions, le_x1e_reactions_c, le_x1f_reactions_krebs  
- 4. Méthode (relier phénomène et réaction) : regarder ce que donne la réaction, puis d'où elle part.
- Éthanol + CO₂ → fermentation alcoolique ; acide lactique → fermentation lactique.
- Glucose → 2 acides pyruviques + 2 NADH,H⁺ + 2 ATP → glycolyse.
- Acétyl-CoA → 2 CO₂ + 3 NADH,H⁺ + FADH₂ → cycle de Krebs (GTP : équivaut à un ATP).
- Attention : une réaction est de trop (l'intrus) ; 2020 R : (1 ; c) (2 ; e) (3 ; b) (4 ; a).
- *Figures :* aucune

**le_s6_b2** — diapos : le_x2_qui_respire, le_x2b_fatigue  
- 5. Méthode (comparer) : critère par critère, « plus faible chez… (valeur) que chez… (valeur) ».
- 2016 N : chez le non-entraîné, mitochondries 5 % contre 11 %, O₂ 2,5 contre 5,5 L/min,
- acide lactique 12 contre 6 mmol/L : il utilise davantage la fermentation lactique.
- 6. Expliquer en flèches : fermentation lactique → 2 ATP par glucose → peu d'ATP → fatigue rapide.
- *Figures :* aucune

**le_s6_b3** — diapos : le_x3_chaine_en_panne, le_x3b_deduire, le_x3c_hypothese  
- 7. Méthode : décrire (périodes bornées par les ajouts, valeurs) → déduire (« donc »)
- → hypothèse au conditionnel → vérifiée ou rejetée, avec la donnée du document.
- Ex. : après ADP + Pi, [O₂] ↓ de 96 à 40 % et ATP ↑ de 10 à 90 UA : O₂ et ATP couplés.
- Hypothèse : le cyanure bloquerait la chaîne respiratoire.
- Vérifiée : après le cyanure, [O₂] reste à 40 % et l'ATP à 90 UA.
- *Figures :* Mitochondries isolées : O₂ et ATP

**le_s6_b4** — diapos : le_x4_synthese, le_b1_bilan  
- Suite du X — 8. Définition : la respiration cellulaire est une dégradation complète du glucose
- en CO₂ et H₂O, avec O₂, dans le hyaloplasme puis la mitochondrie : 36 ou 38 ATP par glucose.
- Avec O₂ : glycolyse (hyaloplasme) → acétyl-CoA, Krebs (matrice) → chaîne (membrane interne).
- Sans O₂ : glycolyse → fermentation (hyaloplasme) : 2 ATP (r ≈ 2,13 %), résidu organique.
- Bilan : la cellule dégrade le glucose et met une partie de son énergie dans l'ATP.
- *Figures :* aucune


## Ce qui reste / doutes

- Les blocs qui chevauchent deux parties (en ligne s1_b2, s2_b1, s3_b2, s4_b3, s5_b1, s5_b2 ; en attente s1_b2, s6_b4) :
  l'application met les deux titres de partie en haut ; les lignes « Suite du … — n. » rattrapent la numérotation. Un
  découpage des blocs aligné sur les parties serait plus net (hors de mon champ : `slide_ids`).
- Une trentaine de lignes font 91 à 99 caractères (équations, définitions) : sous la limite de 100, à surveiller au
  téléphone en paysage, surtout dans les blocs à 2 figures (en ligne s1_b1, s3_b1, s4_b1 ; en attente s1_b1, s1_b2, s4_b2, s4_b3).
- Palette du cahier sans « doré » : ATP en orange (comme Pi), sphère et membrane interne en jaune (comme le carbone).
- Courbe [O₂] / ATP : deux grandeurs sur un même axe (% et UA, mêmes valeurs numériques 0–100) faute de double axe.
- Le document 2020 R écrit GTP au lieu d'ATP pour un tour de Krebs : noté « GTP : équivaut à un ATP ».
- Rendus non vérifiés à l'écran (pas de capture) : positions calculées pour 400 px de large, ≤ 14 éléments par figure.
