## Transformations rapides et transformations lentes

Fichier modifié : `backend/data/courses/en_attente/phys_ch9_transformations_lentes_rapides.json` (seule cette copie en attente). Le travail part de la copie de ce matin, et tout ce qu'elle contenait est conservé. Le script `scratchpad/corr/ch9c/build.py` est rejouable ; l'état d'avant est dans `ch9c/avant.json` et le journal dans `ch9c/log.json`.

### Manques corrigés

| Constat (audit) | Ce qui a été fait | Diapo(s) |
|---|---|---|
| Haute : états physiques absents dans des équations écrites | Ajout de (s), (aq), (l), (g) dans le cahier et la trace, dans les réactions « ecrit » (x9 e0 et e1, C1 r1, r2 et r4, s1_b1), dans le prompt C2_r2 et dans les nouvelles équations. L'atome I isolé s'écrit sans état. Les formules ASCII (H2O2, MnO4) sont réécrites. | tl_cr_carte, tl_x9_oxalique, tl_rp1_ion, tl_r6_classer, C1, C2, C4, tl_s1_b1 |
| Haute : aucun exercice ne fait identifier les deux couples | Une puce, le cahier, une ligne au centre et la voix donnent la méthode « même élément ; l'oxydant d'abord ». Le cahier du bloc a un exemple avec Fe³⁺/Fe²⁺. Un nouvel exercice a été ajouté (2Fe³⁺(aq) + 2I⁻(aq) → …), avec sa démonstration en 7 lignes et ses réactions. Le libellé de C3 est complété (exigé par le cadre, p. 14). | tl_x10_verifier, tl_s1_b3, C3 |
| Haute : définition « rapide / lente » incomplète | Rapide : « ni à l'œil nu ni avec les appareils de mesure courants ; on ne distingue pas les états intermédiaires ». Lente : « de quelques secondes à plusieurs heures ; on distingue les états intermédiaires ». La correction est faite dans la puce, le cahier, l'attendu de s2_b1, la voix (« Je relis »), le centre, la fiche et le catalogue. | tl_r2_rapide, tl_r3_lente, tl_r5_echelle, tl_bl_fiche, C4_r1 |
| Haute : facteur cinétique défini par la durée | Nouvelle définition : « paramètre capable de modifier la vitesse d'évolution d'une transformation, donc sa durée ». Elle est mise dans le lead, la puce, le cahier, le bloc, l'attendu, la voix, le centre et la fiche. | tl_f1_facteur, tl_s2_b3, tl_bl_fiche, tl_f7_palier |
| Moyenne : pas de tableau d'avancement ni de x_max | **Nouvelle diapo tl_rp5_avancement**, un rappel de 1re bac (règle 34) : n = n₀ − a·x, n(I⁻)₀ = [I⁻]₀·V avec V = 100 mL = 0,100 L (la même valeur que la simulation), x_max calculé pour chaque réactif, choix du réactif limitant, n(I₂)_f = x_max « car coefficient 1 », et l'image des tables et des chaises. Le calcul est écrit au centre, une ligne par mot. Les données de tl_f7 (puce, cahier) sont réécrites avec ce calcul. | tl_rp5_avancement (nouvelle), tl_f7_palier, tl_s3_b1 |
| Moyenne : pas d'équation générale | Règle (Ox₁ + n₁e⁻ ⇌ Red₁) × n₂ ; (Red₂ ⇌ Ox₂ + n₂e⁻) × n₁ ; n₂Ox₁ + n₁Red₂ → n₂Red₁ + n₁Ox₂. Elle est mise dans la puce, le cahier, le centre, la voix, le cahier du bloc et la fiche. | tl_x8_fer, tl_s1_b3, tl_bl_fiche |
| Moyenne : la précipitation n'a pas d'équation | Ag⁺(aq) + Cl⁻(aq) → AgCl(s) est écrite dans la puce, le cahier, le centre et la voix. | tl_r2_rapide, tl_r6_classer, tl_s2_b1 |
| Moyenne : thiosulfate sans équation ni couples | S₂O₃²⁻(aq) + 2H⁺(aq) → S(s) + SO₂(aq) + H₂O(l), avec les couples S₂O₃²⁻/S et SO₂/S₂O₃²⁻ (l'ion est oxydant et réducteur). Mis dans la puce, le cahier, le centre et la voix. | tl_r4_indices, tl_s2_b1 |
| Moyenne : aucune espèce (g) | Ajout du couple H⁺/H₂ : 2H⁺(aq) + 2e⁻ ⇌ H₂(g), et de Zn(s) + 2H⁺(aq) → Zn²⁺(aq) + H₂(g) comme exemple d'un gaz qui se dégage. | tl_x3b_couple, tl_r4_indices, tl_s1_b1 |
| Basse : pas d'exemple acide-base | H₃O⁺(aq) + HO⁻(aq) → 2H₂O(l) est ajoutée dans la puce, le cahier, le centre et la voix. | tl_r2_rapide |
| Basse : « conjugué » absent | « réducteur conjugué, espèces conjuguées » ajouté dans la puce, le cahier et la voix. | tl_x3b_couple |
| Basse : applications industrielles | Phrase « dans l'industrie, on chauffe pour accélérer les synthèses (ammoniac) », à l'écrit seulement. | tl_t2_vie, tl_s3_b2 |
| Basse : « cinétiquement inerte » | Ajouté dans une puce. | tl_t1_trempe |
| Dit seulement à l'oral, maintenant écrit | f7 : « car 1 mol de H₂O₂ donne 1 mol de I₂ » et le calcul de x_max. t1 : « elle n'arrête pas tout : on dose vite ». n2 : « agiter n'est pas un facteur du programme ». x8 : le compte des charges +17 et +17. f4 : les axes avec leurs unités et les paliers vers 30 min et 10 min. x10 : la construction avec les deux demi-équations. | tl_f7_palier, tl_t1_trempe, tl_n2_glacee, tl_x8_fer, tl_f4_courbes, tl_x10_verifier |
| Notation | Durée d'une transformation lente : « quelques secondes à plusieurs heures » partout. La puce sur la durée de la transformation rapide est complétée. CO₂ reste (aq) dans tout le cours. | tl_r3, tl_r5, tl_r2, fiche, C4_r1 |
| Hors audit : chiffres et formules lus par la voix | Trois paroles de réaction lisaient des chiffres ou des formules (« 8 millimoles », « MnO4 moins », « H2C2O4 »). Elles sont réécrites en mots et leur audio est retiré. | C4_r1 0.1, C4_r4 1.juste, tl_f7_palier e0.2.1 |

### Non corrigés et pourquoi

- **États physiques dans les `attendu` (C3_r1, C3_r4, C1_r3, tl_s1_b3) et dans les textes `alt` des visuels** : la règle du skill cours-concentration (Chimie) interdit les états dans `attendu` et `alt`. Ces champs sont laissés tels quels. **À décider** : l'attendu d'un « retrouver » est réécrit sur le tableau de correction, donc la règle est peut-être à revoir.
- **Le texte écrit par les simulations** (`bilan.html`, `carte.html`, `equation.html`) n'a pas été modifié : il est interdit de toucher à autre chose qu'au cours en attente. La fiche `bilan.html` dit déjà « vitesse d'évolution ». La carte dit encore « lente (secondes → heures) ».
- **Manques signalés chez un seul professeur** (dichromate, pH-mètre, ordres de grandeur 4 °C et −18 °C, titrage « unique ») : non ajoutés, car aucun n'est exigé par le cadre.
- **Hors cadre** (lumière, solvant, agitation comme facteur, titrage conductimétrique) : non ajouté. Le cours dit maintenant à l'écrit que l'agitation n'est pas un facteur du programme.
- **Les deux nouveaux exercices** (lire les couples, réactif limitant) sont dans la réserve `exercices_fin_de_cours`. Les blocs tl_s1_b3 et tl_s1_b4 ont déjà leur question « À toi », et la règle 27 n'en permet qu'une par bloc.
- **tl_rp5_avancement n'a pas de visuel** : aucune vue existante ne montre l'avancement. Le calcul s'écrit ligne par ligne au centre.

### Démonstrations (relues, réécrites, 3 exemples avant → après en une ligne chacun)

Relues : les 17 démonstrations du cours et les exemples travaillés écrits sur les diapos (x4, x5, x6, x6b, x7, x8, x9, x10, rp3, rp4, f7). Réécrites ou nouvelles : 14, dont 2 nouvelles. Elles ont toutes 7 lignes ou moins, partent des données, nomment la règle, et finissent par une vérification puis la réponse :
- tl_x7_equation q, x9 f0 et f1, s1_b3 : avant « 2 électrons captés, 2 cédés → équation finale » ; après, une ligne d'addition « … + 2e⁻ → … + 2e⁻ ; les 2e⁻ s'annulent », puis la ligne de vérification des charges (−4 et −4, +2 et +2).
- tl_f7_palier f0 et tl_s3_b1 : avant « I⁻ est en excès : H₂O₂ limitant » affirmé sans calcul ; après, les données (n(I⁻)₀ = 10 mmol), puis 4 − x_max = 0 donne 4 mmol, puis 10 − 2x_max = 0 donne 5 mmol, puis la comparaison, le réactif limitant, « n(I₂) = x_max car coefficient 1 », et enfin 4 mmol.
- tl_x6_eau f0 et f1, s1_b2 : avant « charges −2 et −4 : 2e⁻ à gauche » ; après, « pour passer de −2 à −4, on ajoute 2e⁻ du côté de l'oxydant », puis la vérification −2 − 2 = −4.

Les autres réécritures :
- rp4 q et s1_b4 : une ligne de données avec les unités, et la relation C = n/V écrite avant n = C·V.
- x4 q : la raison « en milieu acide, H₂O apporte O », puis la vérification 4 = 4.

Restées telles quelles, car déjà complètes : x10 f0, f4 f0 et s2_b3, n1 f0 et s3_b3.

### Voix à enregistrer (id)

- **Diapos (speech_text changé ou nouveau, audio retiré)** : tl_x3b_couple, tl_x8_fer, tl_x10_verifier, tl_rp5_avancement (nouvelle), tl_r2_rapide, tl_r3_lente, tl_r4_indices, tl_f1_facteur, tl_bl_fiche.
- **Démonstrations sans audio** :
  - questions : tl_x4_oxygene q, tl_x7_equation q, tl_rp4_concentration q ;
  - réserve : tl_x6_eau f0 et f1, tl_x9_oxalique f0 et f1, tl_x10_verifier f0 et f2, tl_rp5_avancement f0, tl_f4_courbes f0, tl_f7_palier f0, tl_n1_lecture f0 ;
  - blocs : tl_s1_b2, tl_s1_b3, tl_s1_b4, tl_s2_b3, tl_s3_b1, tl_s3_b3.
- **Énoncés dits** : tl_f7_palier f0 et tl_s3_b1 (enonce_dit changé, enonce_audio retiré), tl_x10_verifier f2, tl_rp5_avancement f0.
- **Réactions** : tl_x10_verifier e2 (5), tl_rp5_avancement e0 (5), C4_r1 0.1, C4_r4 1.juste, tl_f7_palier e0.2.1.

### Vérifications faites (résultats)

- JSON valide ; écrit avec ensure_ascii=False, indent=2, fins de ligne LF (0 CR). Le fichier a été relu juste avant l'écriture et n'avait pas changé depuis 07:02.
- `verif_attente.py` : 42 diapos, **0 mot absent**, **0 hors bloc**, 0 doublon, 0 compétence inconnue, 9 diapos sans voix (celles de la liste ci-dessus).
- Chaque « mot » des démonstrations, du pointage et du centre est un extrait exact, et unique, de sa parole ou de sa voix. L'`apres_mot` des 2 observations est présent.
- `verifier_figures_cahier.py` : 5 figures, 0 erreur.
- Recherche des équations écrites sans état : il reste 23 signalements, tous faux (des noms d'espèces dans des phrases ou dans une notation de couple). Aucune formule ASCII ne reste dans un champ écrit.
- Champs dits (parole, dit, enonce_dit, mixed) : 0 chiffre, 0 symbole, 0 tachkil. Aucune phrase en français de plus de 10 mots sans virgule dans les textes nouveaux.
- Calculs vérifiés en python :
  - quantités et concentrations : 0,1 × 0,100 = 0,01 mol ; 0,02/0,5 = 0,04 ; 0,1 × 0,2 = 0,02 ; 0,01/0,100 = 0,1 ;
  - charges : +17 et +17 ; +4 et +4 ; −4 et −4 (S₂O₈²⁻ et S₂O₃²⁻) ; Fe³⁺ +2 ; I₂ −2 ; CO₂ 0 ;
  - x_max : (2 ; 10) donne 2, H₂O₂ limitant ; (4 ; 10) donne 4, H₂O₂ ; (3 ; 4) donne 2, I⁻ ;
  - équilibre des équations du thiosulfate, de Zn + 2H⁺ et de H₃O⁺ + HO⁻.
- Aucun autre fichier du dépôt n'a été modifié ; rien n'a été commité.
