# Audit physique : notre programme et nos cours face au cadre officiel

Date : 15 novembre 2026.
Référence : cadre de référence officiel de l'examen national, physique-chimie, filière Sciences physiques, options internationales (CNEEO, 2015), transcrit dans `backend/cours 2bac pc/cadres de references 2BAC PC/cadre-de-reference-de-l-examen-national-physique-chimie-spc-2.json` (partie `content_structure_physics`, poids, annexe 2 des TP).

Le PDF officiel n'a pas pu être ouvert depuis la session cloud (`www.tawjihnet.net` est bloqué par le réseau). Le JSON officiel est un résumé : il donne les notions de chaque chapitre, pas le détail de l'annexe 1. Les points ambigus ont été tranchés dans le sens le plus strict : ce que le JSON officiel ne cite pas est retiré. Les points qui mériteraient une relecture sur le PDF sont listés à la fin de l'étape 1.

## Le cadre officiel, partie physique (67 % de la note)

| Sous-domaine officiel | Poids | Notions officielles | Notre cours |
|---|---|---|---|
| 1. Ondes | 11 % | Ondes mécaniques progressives (définitions, célérité, retard temporel) ; ondes mécaniques progressives périodiques (période, fréquence, longueur d'onde, diffraction) ; propagation d'une onde lumineuse (diffraction, aspect ondulatoire, milieux dispersifs, indice de réfraction, θ = λ/a) | ch1, ch2, ch3 |
| 2. Transformations nucléaires | 8 % | Décroissance radioactive (composition du noyau, isotope, diagramme N/Z, α, β⁺, β⁻, γ, loi de décroissance, demi-vie) ; noyaux, masse et énergie (défaut de masse, énergie de liaison, fission, fusion, bilan énergétique) | ch4, ch5 |
| 3. Électricité | 21 % | Dipôle RC ; dipôle RL ; circuit RLC série (amortissement, régimes périodique / pseudo-périodique / apériodique, oscillations libres, entretien) ; applications (transmission d'informations, modulation d'amplitude, démodulation) | ch6, ch7, ch8 ; **modulation : aucun cours** |
| 4. Mécanique | 27 % | Lois de Newton ; applications (chute verticale avec frottement, chute libre, projectile, particules chargées dans un champ magnétique, lois de Kepler, satellites et planètes) ; rotation d'un solide autour d'un axe fixe ; systèmes oscillants (solide-ressort, torsion, pendule pesant, pendule simple, amortissement, résonance) ; aspects énergétiques ; atome et mécanique de Newton (quantification de l'énergie, spectre de raies) | **aucun cours** |

TP officiels de physique : célérité d'une onde mécanique ; diffraction d'une onde sonore ou ultrasonore ; diffraction de la lumière ; dispersion de la lumière blanche ; charge d'un condensateur ; tension aux bornes d'une bobine ; oscillations libres RLC ; modulation et démodulation ; lois de Newton ; chute verticale avec frottement ; projectile ; pendules et résonance.

## Étape 1 — Notre programme face au cadre officiel

Fichiers comparés : `perimetre.json` (clés de physique), `physique.json` (domaines ondes, nucléaire, électricité, mécanique), `physique_blueprint.json`, `programme_semestre1.json` (ordres 1 à 8), `cadre_reference_2bac_pc.json` (fiches `ondes_mecaniques`, `ondes_mecaniques_periodiques`, `ondes_lumineuses`, `radioactivite`, `energie_nucleaire`, `dipole_RC`, `dipole_RL`, `circuit_RLC`). Les parties chimie de ces fichiers n'ont pas été touchées (session chimie).

### (a) Ce que nous avions en trop (hors cadre officiel)

| Fichier | Avant | Après | Raison |
|---|---|---|---|
| `perimetre.json`, `ondes_lumineuses` (notions, méthodes, démonstrations, source) | « lois de Snell-Descartes n₁·sin i₁ = n₂·sin i₂ », « appliquer Snell-Descartes aux deux faces d'un prisme », « calcul des angles de réfraction dans un prisme » | dispersion par le prisme **interprétée qualitativement** (l'indice dépend de la fréquence, le violet est le plus dévié) | Les relations du prisme sont hors cadre (retirées du cours et de la fiche OL11 le 15/11, commit `01d8a70c`) ; le périmètre les gardait encore. |
| `perimetre.json`, `ondes_lumineuses`, terme hors programme « minimum de déviation » | « on applique les lois de Snell-Descartes sur chaque face du prisme » | « relations du prisme, minimum de déviation, Snell-Descartes en calcul » : le motif attrape aussi `A = r + r'`, `D = i + i' − A`, `sin i = n·sin r`, « Snell » | La phrase « à dire à la place » enseignait justement la notion retirée. |
| `physique.json`, `ondes_lumineuses` | « Lois de Snell-Descartes » | retiré ; remplacé par λ₀ = c/ν, fréquence invariante, λ = λ₀/n | Même raison. |
| `cadre_reference_2bac_pc.json`, `ondes_lumineuses` | 4 formules du prisme (capacité OL11 retirée) encore dans `formules`, mot-clé « angle de déviation », décision « partie finale C9 pour le devoir » | formules et mot-clé retirés, décision réécrite | Une fiche ne garde que les formules de capacités officielles. |
| `physique.json`, `ondes_sonores` | « Niveau d'intensité sonore L = 10 log(I/I₀) », « Effet Doppler (qualitative) » | retirés (écho, mesure de λ et v aux ultrasons, diffraction des ultrasons) | Ni le niveau sonore ni l'effet Doppler ne sont dans le cadre ; `perimetre.json` les avait déjà en hors programme : les deux fichiers se contredisaient. |
| `perimetre.json`, `ondes_sonores` | « hauteur d'un son liée à sa fréquence, intensité liée à l'amplitude », terme « hauteur d'un son » | retirés ; hauteur et timbre ajoutés aux termes hors programme | Pas dans le cadre. |
| `perimetre.json`, `mouvement_projectile` | « particule chargée dans un champ électrique uniforme, déflexion électrique » (notion, méthode, terme, source, niveau) | retiré ; ajouté aux termes hors programme | Le cadre PC ne cite que « particules chargées dans un champ magnétique ». |
| `physique.json` et `perimetre.json`, `circuit_RLC` | « régime critique » (régimes, termes du programme, méthodes) | trois régimes officiels : périodique, pseudo-périodique, apériodique ; « régime critique » ajouté au terme hors programme de la résistance critique | Le cadre cite exactement trois régimes. |
| `cadre_reference_2bac_pc.json`, `circuit_RLC` | RLC2 « le régime critique étant la frontière, sans calcul », mot-clé « régime critique » | phrase et mot-clé retirés ; « régime critique » dans `hors_cadre` (mot et motif) | Même raison. |
| `perimetre.json`, `oscillateur_mecanique` | amortissement « pseudo-périodique, apériodique, critique » | sans « critique » ; terme hors programme ajouté | Le cadre dit « amortissement ». |
| `perimetre.json` et `physique.json`, `champ_magnetique` | « cyclotron : accélération entre les dees… », « spectromètre de masse, cyclotron » comme applications | contextes d'énoncé dont le fonctionnement est décrit par l'énoncé ; on garde la séparation de deux isotopes par R = m·v/(|q|·B) | Le cadre cite le mouvement de la particule, pas les appareils. |
| `perimetre.json`, `modulation_AM` | termes « filtre passe-bas », « filtre passe-haut » | « élimination de la composante continue » | Les notions du cadre parlent de démodulation ; les noms de filtres sont hors programme dans le RC et n'étaient pas dans nos propres notions. |

### (b) Ce qui manquait

| Fichier | Ajout | Raison |
|---|---|---|
| `perimetre.json`, `physique.json` | Chapitre **`ondes_mecaniques_periodiques`** (fiche complète : double périodicité, λ = v·T, points en phase, stroboscope, diffraction, milieu dispersif) ; `ondes_mecaniques` ne garde que les ondes progressives (définitions, célérité, retard, L = v·θ) | Deux chapitres officiels distincts ; `programme_semestre1.json` citait déjà la clé `ondes_mecaniques_periodiques`, qui n'existait pas dans le périmètre. |
| `perimetre.json`, `physique.json` | Chapitre **`rotation_solide`** (grandeurs angulaires, moment, J_Δ donné, Σ M_Δ = J_Δ·θ̈) | Chapitre officiel ; il n'existait que comme une ligne dans les oscillateurs. |
| `perimetre.json`, `physique.json` | Chapitre **`aspects_energetiques`** (travail, théorème de l'énergie cinétique, énergies potentielles, énergie mécanique) | Chapitre officiel absent de `physique.json`. |
| `perimetre.json`, `physique.json` | Chapitre **`atome_mecanique_newton`** (niveaux d'énergie, photon ΔE = h·ν, spectres de raies) | Chapitre officiel totalement absent. |
| `perimetre.json`, `dipole_RC` | associations de condensateurs et charge à courant constant | Capacité RC3 de la fiche, demandée au national (2018 N), absente du périmètre. |
| `physique.json` | RC : q = C·u_C, i = dq/dt, associations ; RL : u = L·di/dt + r·i, I₀ = E/(R+r), τ = L/(R+r) ; RLC : énergie totale, effet Joule, u_G = k·i ; modulation : circuit d'accord ; oscillateurs : amortissement et résonance (qualitatif) ; ondes lumineuses : lumière monochromatique, λ₀ = c/ν, spectre visible, λ = λ₀/n | Notions officielles qui manquaient à la liste du programme. |
| `physique_blueprint.json` | poids officiels de la physique et liste des sujets à ne jamais poser | Le blueprint ne citait pas le cadre. |
| `programme_semestre1.json` | ch1 → cours `phys_ch1_waves_exemple` ; ch2 → statut `en_ligne`, cours `phys_ch2_ondes_periodiques` ; note des chapitres de physique sans cours (semestre 2) | Le ch2 est publié mais était marqué « à explorer ». |

**Chapitres officiels sans cours** : modulation et démodulation d'amplitude ; toute la mécanique (lois de Newton et chute verticale, projectile, particule dans un champ magnétique, satellites et Kepler, rotation, systèmes oscillants, aspects énergétiques, atome et mécanique de Newton). Ils n'ont pas non plus de fiche dans `cadre_reference_2bac_pc.json` ; une fiche est à créer avant chaque cours (skill `cours-concentration`, étape 8). La mécanique pèse 27 % de la note et l'électricité 21 % (la modulation tombe dans 10 sessions sur 20 du national) : ce sont les prochains cours à faire.

### (c) Ce qui était mal formulé ou mal classé

| Fichier | Avant | Après | Raison |
|---|---|---|---|
| `physique.json`, `ondes_lumineuses` | « Relation sin(θ) = λ/a » (topic et question type) | « θ = λ/a (θ en rad) » | Le cadre écrit θ = λ/a. |
| `physique.json`, `ondes_mecaniques` | « diffraction : condition a ≈ λ » | « nette quand a est de l'ordre de λ ou plus petite » (au chapitre périodique) | Le barème attend la comparaison a ≤ λ ; « a ≈ λ » laissait croire qu'une fente plus fine ne diffracte pas. |
| `physique.json`, `modulation_AM` | « Taux de modulation : m = U_m/U_p (condition m ≤ 1) » | « m = U_m/U₀ ; bonne modulation si m < 1 et f_p ≫ f_m » | **Erreur scientifique** : le taux se rapporte à la tension de décalage U₀, pas à l'amplitude de la porteuse ; m = 1 est déjà la limite. |
| `physique.json`, `modulation_AM` | « Démodulation : détection d'enveloppe + filtre passe-bas » | « détection d'enveloppe (diode + RC parallèle, T_p ≪ RC < T_m) puis élimination de la composante continue » | **Erreur** : la seconde étape enlève la composante continue (dipôle RC série), ce n'est pas un passe-bas. |
| `physique.json`, `nucleaire` | « ΔE = \|Δm_produits − Δm_réactifs\| × c² » | « E_lib = \|Σm(produits) − Σm(réactifs)\|·c² » | Notation fausse : on soustrait des masses, pas des défauts de masse. |
| `physique.json`, `dipole_RL` | « i(t) = (E/R)(1 − e^(−t/τ)), τ = L/R » | « I₀ = E/(R + r), τ = L/(R + r) » | La bobine a une résistance r dans tous les nationaux. |
| `perimetre.json`, `ondes_lumineuses` | « demi-largeur angulaire θ = λ/a (petits angles) » | « écart angulaire θ = λ/a (θ en rad) » | Mot du cadre. |
| `perimetre.json`, `radioactivite` | « le noyau fils émet un photon γ » | « émet un rayonnement γ (onde électromagnétique) » | Le photon et E = h·ν appartiennent au chapitre « Atome et mécanique de Newton » ; la fiche du chapitre dit déjà « rayonnement γ ». |
| `perimetre.json`, `circuit_RLC` | entretien par « montage à amplificateur opérationnel, résistance négative, u = R·i » | « générateur u_G = k·i, k = R + r » | Écriture des sujets nationaux et de la fiche ; l'amplificateur opérationnel n'est pas au cadre. |
| `perimetre.json`, `ondes_sonores` | f pour la fréquence | N | Notation de la fiche et des nationaux. |
| `perimetre.json`, `oscillateur_mecanique` | rotation et énergies mêlées aux oscillateurs | rotation et énergies dans leurs propres chapitres | Trois notions officielles distinctes. |
| `cadre_reference_2bac_pc.json`, fiches de physique | « Le texte officiel du cadre n'a pas été relu : capacités à confirmer » | note de collationnement avec la notion officielle de chaque fiche | Collationnement fait ; chaque capacité relève d'une notion officielle. |
| `cadre_reference_2bac_pc.json`, `radioactivite`, `energie_nucleaire`, `ondes_lumineuses` | « E = hν », « photon » listés hors cadre sans précision | précisé : au programme dans « Atome et mécanique de Newton », hors de ces chapitres | Mal classé : ce n'est pas hors programme, c'est un autre chapitre. |

### Points à relire sur le PDF officiel (non tranchés par le JSON résumé)

- Méthode d'Euler (chute verticale) et repère de Frenet : gardés, ils figurent dans les orientations pédagogiques et les nationaux ; le JSON résumé ne les nomme pas.
- Spectre à trois raies du signal modulé et méthode du trapèze : gardés au périmètre de la modulation, à confirmer.
- Plan incliné avec frottement (coefficient de frottement) : gardé comme application des lois de Newton.
