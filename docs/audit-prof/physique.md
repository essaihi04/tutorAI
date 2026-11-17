# Audit des cours de physique du semestre 1 face aux cours de professeurs

17 novembre 2026. Nos 8 cours (écran, cahier, voix, questions, démonstrations) sont comparés au cours complet du Pr Nidal Naceiri Mrabti (2 PC, partie 1). Ils sont aussi comparés aux cours et résumés publiés sur moutamadris (Pr Mahajar, Sbiro, Chriki, El Kaouahi, Asnaoui, Hajji, Bendaoud, Chouvin, manuel TS) et au cadre de référence officiel. Pour le circuit RLC, seuls Nidal et Sbiro sont disponibles.

Un manque est **confirmé** quand au moins deux professeurs l'écrivent, ou un seul et le cadre officiel l'exige. Ce qui est hors cadre (régime critique, effet Doppler…) est écarté.

## Bilan

| Chapitre | Manques confirmés | haute | moyenne | basse | Démonstrations qui sautent des étapes |
|---|---|---|---|---|---|
| 1. Ondes mécaniques progressives (version en attente, 22 diapos) | 17 | 5 | 9 | 3 | 4 |
| 2. Ondes mécaniques progressives périodiques | 17 | 6 | 6 | 5 | 4 |
| 3. Propagation d'une onde lumineuse | 16 | 3 | 6 | 7 | 5 |
| 4. Décroissance radioactive | 22 | 3 | 6 | 13 | 8 |
| 5. Noyaux, masse et énergie | 10 | 1 | 5 | 4 | 4 |
| 6. Dipôle RC | 12 | 3 | 3 | 6 | 6 |
| 7. Dipôle RL | 12 | 4 | 3 | 5 | 5 |
| 8. Oscillations libres RLC | 5 | 2 | 2 | 1 | 4 |
| **Total** | **111** | **27** | **40** | **44** | **40** |

## Ce qui revient dans tous les chapitres

1. **Des relations posées sans la ligne d'où elles viennent.** Exemples : τ = SM/v sans v = d/Δt ; λ = v·T tirée d'un exemple chiffré ; n = λ₀/λ sans « car n = c/v » ; dN = −λN·dt sans « noyaux désintégrés pendant dt = −dN » ; i(t) en RC sans i = C·du_C/dt. C'est le même oubli que l'état physique en chimie : les professeurs l'écrivent toujours.
2. **Les équations différentielles ne sont pas résolues jusqu'au bout** (RC, RL, radioactivité, RLC). La forme A·e^(−t/τ) + B n'apparaît jamais. B et τ ne sont pas identifiés par l'équation, ni A par la condition initiale (u_C(0) = 0, i(0) = 0, N(0) = N₀). La solution de rupture n'est pas vérifiée. Les grandeurs dérivées (i, u_R, u_b, q, m(t), n(t)) ne sont pas écrites.
3. **Les valeurs particulières sont annoncées, pas calculées** : N(τ) = N₀·e⁻¹, N(n·t½) = N₀/2ⁿ, 63 % et 37 %, période de l'échange d'énergie T₀/2.
4. **Les conditions et les unités des lois** : onde non amortie pour y_M(t) = y_S(t − τ) ; « la plus petite durée » dans la définition de T ; l'unité de τ ; m/s = m·s⁻¹ (notation des sujets).
5. **Les montages ne sont qu'en simulation** : il manque le schéma annoté au cahier (diffraction, acquisition RC avec u_R, oscilloscope à mémoire), alors que le cadre le demande.
6. **Des notions du cadre manquent** : la diffraction d'une onde sonore ou ultrasonore, la définition générale d'une lumière polychromatique, l'énergie de masse, les applications et dangers de la radioactivité, q(t) et i(t) en LC.

Ces points sont maintenant des règles du skill de création de cours : règle 37 de `professeur` (volet physique) et étape 9b de `cours-concentration`.

## À reprendre avant toute mise en ligne

La copie en attente de l'onde mécanique (`en_attente/phys_ch1_waves_exemple.json`) **n'a pas les 14 corrections de l'audit du 15 novembre** (`docs/audit-programme-officiel/physique.md`), qui sont déjà dans la copie en ligne. Elles sont à reporter avant de remplacer le cours en ligne.

## Détail par chapitre

### Ondes mécaniques progressives
Notre cours audité : `backend/data/courses/en_attente/phys_ch1_waves_exemple.json` (22 diapos : écran, cahier, voix `fr`, questions, rappels, exercices des blocs).
Sources lues : (professeur, document, pages lues en image)
- Pr Nidal Naceiri Mrabti, cours 2 BIOF (`nidal_p1.pdf`), p. 4-21 en image (unité 1 = p. 5-10 ; unité 2, p. 13-20 = chapitre suivant ; p. 11, 12 et 21 sont des pages quadrillées vides).
- Pr Hicham Mahajar et Pr Youssef Tabit (`m_Ondes-mecaniques-progressives_1`), p. 1-4 en image.
- Pr Bendaoud (`_2`, auteur « LB »), p. 1-7 du PDF en image (numérotées 3-9).
- Auteur non nommé (`_3`, fiche d'activités), p. 1-14 en image (p. 1-4 sur ce chapitre ; p. 5-14 sur les ondes périodiques et le son, donc le chapitre suivant).
- Manuel français TS mis en page par J. Chouvin (`_4`, scan), p. 1-6 en image.
- Pr El Kaouahi El Mokhtar (`_5`), p. 1-3 en image.
- Aussi lus : cadre `cadre_reference_2bac_pc.json` (OMP1-OMP8, formules, hors_cadre), `experience_profs.json` (ondes_mecaniques, profs YouTube et nationaux), `docs/audit-programme-officiel/physique.md`.

#### Plan comparé (tableau : partie chez les professeurs → où chez nous → remarque)
| Partie chez les professeurs | Chez nous | Remarque |
|---|---|---|
| Activité : caillou dans l'eau, corde, ressort ; définition de l'onde mécanique (tous) | wx_o1_bouee, wx_i1_corde, wx_i2_definition | La définition est conforme à OMP1. Le « milieu élastique » n'est expliqué qu'à la voix. |
| Transversale ou longitudinale, avec des schémas (tous) | wx_i3_types, wx_i3b_longitudinale | Bien fait. Il manque le cas du ressort qui porte une onde transversale (Chouvin p. 2). |
| Onde sonore : cloche à vide, haut-parleur et bougie, compression et dilatation (Nidal p. 7, Mahajar p. 2, El Kaouahi p. 2, Chouvin p. 3) | wx_i3b_longitudinale | La conclusion est écrite (longitudinal, pas dans le vide), mais aucune des deux expériences n'est montrée. |
| Propriétés : direction et dimension, superposition (tous) | wx_i3b_longitudinale (dimension) | La superposition est hors cadre et volontairement absente. |
| Célérité v = d/Δt, unités, milieu homogène (tous) | wx_p1_vitesse, wx_c1_celerite | Bien fait (mesure de front à front). |
| Facteurs : forme, élasticité, inertie, température, tension, μ (Mahajar p. 3-4, Bendaoud p. 5, Nidal p. 8, El Kaouahi p. 3, Chouvin p. 5) | wx_c2_facteurs, wx_c2b_temperature | Manquent la forme de la perturbation, ainsi que l'élasticité et l'inertie. |
| Retard τ = t_M − t_S = SM/v ; y_M(t) = y_S(t − τ) ; cas général M₁M₂ (tous) | wx_r1_retard | Seule la paire S et M est traitée, et sans la condition « non amortie ». |
| Durée de la perturbation et longueur (Bendaoud p. 6-7, Nidal p. 10) | wx_r2_duree_longueur | L = v·θ est présent ; manquent la date d'arrêt d'un point et l'état d'un point à une date t. |
| Exercices sur l'aspect : photos à deux dates, t₀ inconnu, tracer l'aspect (Bendaoud p. 7, Nidal p. 10, El Kaouahi p. 3) | wx_c1_celerite, wx_l1_aspect, wx_l2_sens | La lecture et le sens du mouvement y sont. Manquent t₀, l'échelle et le tracé de l'aspect. |
| Deux micros et oscilloscope ; ultrasons ; échographie ou télémètre (Nidal p. 10, Bendaoud p. 8-9, Chouvin p. 5) | wx_p2_milli, wx_m1_micros, wx_m1b_lecture, wx_m2_sonar, wx_m2b_formule | Bien fait. Manquent le µs et le micro déplacé de d'. |
| Même distance dans deux milieux (Chouvin p. 6, ex. 2 fonte/eau) | — | Absent (cas de national d'après experience_profs « deux_milieux »). |
| Comparaison entre le mouvement d'un corps et la propagation d'une onde (Mahajar p. 4) | — | Chez un seul professeur. |
| Méthode et bilan | wx_b1_redaction, wx_b2_national, wx_b3_bilan, wx_b4_carte | Plus riche que chez les professeurs. |

#### Manques confirmés (tableau trié)
| Priorité | Catégorie | Ce que disent les professeurs | Chez nous | Où l'ajouter |
|---|---|---|---|---|
| haute | Condition de validité | La relation y_M(t) = y_S(t − τ) (« tous les points subissent la même perturbation ») ne vaut que pour une onde **non amortie**, dont l'amplitude se conserve : Nidal p. 9, Bendaoud p. 6, Mahajar p. 4 (« sans amortissement »). En réalité les frottements font diminuer l'énergie et l'amplitude : Bendaoud p. 4 (remarque), fiche _3 p. 3 et p. 10. | Ni « amorti » ni « non amortie » n'apparaissent dans tout le JSON. La relation y_M = y_S(t − τ) est donnée sans condition. | wx_r1_retard (écran et cahier : « si l'onde n'est pas amortie ») ; à reprendre dans wx_b3_bilan, point 4 |
| haute | Loi, cas général | Retard entre deux points quelconques : τ = M₁M₂/v et y_M₂(t) = y_M₁(t − τ). Sources : Mahajar p. 4, Bendaoud p. 6 (« en général τ = M'M/v »), El Kaouahi p. 3 (τ = t_M' − t_M, Y_M'(t) = Y_M(t − τ)), Chouvin p. 6. Le cadre admet ces variantes (OMP4, OMP5). | Seule la paire S et M figure à l'écran, au cahier et au bilan. Le cas des deux micros donne v = d/τ, mais sans relation d'élongation entre deux points. | wx_r1_retard (puce « entre deux points M₁, M₂ : τ = M₁M₂ / v, y_M₂(t) = y_M₁(t − τ) ») ; wx_b3_bilan |
| haute | Méthode, exercice type | Date d'arrêt et état d'un point à une date t. Le point est atteint à t_M = SM/v et revient au repos à t_M + θ ; on en déduit s'il est au repos, en vibration ou pas encore atteint. Sources : Bendaoud p. 6-7 (exercice d'application 1), Nidal p. 10 (ex. 1, Q5 « à quel instant s'arrête M ? »), experience_profs (« date d'arrêt = date d'arrivée + θ »). | Aucune occurrence de « s'arrête » ou de « date d'arrivée ». wx_l2_sens dit seulement qu'un point est au repos devant le front ou derrière la queue. | wx_r2_duree_longueur (puce, plus un exercice dans le bloc wx_s1_b3) |
| haute | Méthode, exercice type | La source démarre à t₀ ; il faut dater une photo. On a Δt = t − t₀, t_N = t₀ + SN/v et t₀ = t₁ − d₁/v. Sources : Bendaoud p. 7 (ex. 2 : photos à t₁ et t₂, t₀ = t₁ − d₁/v, d₃ = v(t₃ − t₀)), Nidal p. 8 (Δt' = t_N − t₀, t_N = 22,5 ms), experience_profs « source_t0 ». | Aucune occurrence de t₀. Le cours suppose toujours que la source démarre à 0. | wx_c1_celerite (rappel Δt = t − t₀) ou wx_r1_retard ; exercice dans le bloc wx_s1_b2b |
| haute | Exercice type | Même distance dans deux milieux : deux signaux arrivent avec un écart τ. On écrit τ = d/v_lent − d/v_rapide, puis on isole d. Sources : Chouvin p. 6 (ex. 2, fonte et eau, d = 3,86 km), experience_profs « deux_milieux » (nationaux). | La simulation montre la course acier, eau, air, mais aucune relation n'est écrite. Ni « fonte » ni « deux milieux » n'apparaissent. | wx_c2_facteurs (écrire t = d/v pour chaque milieu) ; ligne « deux milieux » dans le tableau de wx_b2_national |
| moyenne | Facteur de la célérité | La célérité ne dépend pas de la **forme** (ni de la durée) de la perturbation. Sources : Mahajar p. 3 (expérience de deux formes, V₁ = V₂), Bendaoud p. 5, Nidal p. 8, Chouvin p. 5 (« forme et amplitude »), El Kaouahi p. 3 (« ni de l'amplitude ni de la durée »). | Seule l'amplitude est traitée (« frapper plus fort »). La forme n'est jamais citée. | wx_c2b_temperature (puce « ni la forme ni l'amplitude de la perturbation ») |
| moyenne | Définition, facteurs | La célérité dépend du milieu par son **élasticité**, son **inertie** et sa température. L'inertie d'une corde, c'est sa masse linéique. Sources : Mahajar p. 4, Bendaoud p. 5, Nidal p. 8, El Kaouahi p. 3. | Le cours dit « nature du milieu », « tension », « corde plus lourde ». Les mots élasticité et inertie sont absents. | wx_c2b_temperature (une ligne : tension = élasticité, masse linéique = inertie) |
| moyenne | Expérience attendue | Cloche à vide : on fait le vide et la sonnerie ne s'entend plus, donc le son a besoin d'un milieu matériel. Sources : Mahajar p. 2, Nidal p. 7, El Kaouahi p. 2, Chouvin p. 3, fiche _3 p. 1. | La conclusion est écrite (« pas dans le vide ») mais l'expérience n'est pas montrée. Aucune occurrence de « cloche ». | wx_i3b_longitudinale (une puce avec l'expérience) |
| moyenne | Expérience attendue | Haut-parleur et bougie : la flamme bouge dans la direction de propagation, donc le son est longitudinal. Sources : Nidal p. 7, El Kaouahi p. 2, Chouvin p. 3 (Mahajar p. 2 : diapason et pendule). | Absent : aucune occurrence de bougie, flamme ou haut-parleur. | wx_i3b_longitudinale |
| moyenne | Méthode (exploiter une photo) | Utiliser l'échelle (règle graduée, « 1 m », « 2 cm ») pour mesurer la distance du front sur une photo. Sources : Nidal p. 10 (ex. 1), Bendaoud p. 7 (ex. 2), experience_profs « photo ». | « Échelle » est absent. wx_c1_celerite mesure du front au front sans conversion d'échelle. | wx_c1_celerite (puce « distance réelle = mesure × échelle ») |
| moyenne | Méthode, schéma | Représenter l'aspect de la corde à une date t₃ : placer le front à v·(t₃ − t₀), puis mettre la longueur L derrière lui. Sources : Bendaoud p. 7 (ex. 2, Q4, avec figure), fiche _3 p. 1 (b1) et p. 6 (e), experience_profs « dessiner_aspect ». | Absent : on lit des aspects, on n'en trace jamais. | wx_l1_aspect (méthode en 2 étapes) ou un exercice dans le bloc wx_s1_b3 |
| moyenne | Unités | Sensibilité en µs/div et durées en µs, avec 1 µs = 10⁻⁶ s. Sources : Bendaoud p. 8-9 (100 µs/div, Δt₂ = 20 µs), experience_profs (insistance « µs → s (×10⁻⁶) »). | Seule la milliseconde est vue (wx_p2_milli). Aucune occurrence de « µs ». | wx_p2_milli (ligne µs) ; wx_m1b_lecture |
| moyenne | Piège classique | Un ressort peut porter une onde **transversale** (secousse perpendiculaire). On décide en comparant les deux directions, pas d'après l'exemple appris. Sources : Chouvin p. 2 (Doc. 4), experience_profs (insistance et piège « le ressort est toujours longitudinal »). | Le cours associe toujours le ressort à la longitudinale (wx_i3b, cahier, carte). | wx_i3_types ou wx_i3b_longitudinale (une puce « attention ») |
| moyenne | Exercice type | Micro R₂ déplacé de d' : le nouveau retard vaut τ' = (d + d')/v. Il faut écrire la distance réellement parcourue. Sources : Nidal p. 10 (ex. 2, Q4, d' = 51 cm), experience_profs « geometrie ». | La simulation déplace M₂, mais aucune relation ni exercice ne traite ce cas. | wx_m1b_lecture (exemple) ou un exercice dans le bloc wx_s2_b1 |
| basse | Propriété (phrase type) | « Une onde se propage, à partir de sa source, dans toutes les directions qui lui sont offertes. » Sources : Mahajar p. 2, Bendaoud p. 4, Nidal p. 8, El Kaouahi p. 2, Chouvin p. 1. Le vocabulaire « milieu uni-, bi-, tridimensionnel » vient de Nidal p. 8 et Mahajar p. 2. | La phrase n'existe que dans des réactions préparées (C2_r2, exercice wx_i3_types). L'écran dit seulement « Dimension : 1, 2, 3 ». | wx_i3b_longitudinale (puce dimension) |
| basse | Définition | Une perturbation est une modification temporaire (ou une variation) d'une propriété mécanique du milieu. Sources : Bendaoud p. 3, El Kaouahi p. 1. | wx_i1_corde dit « la déformation qui avance ». C'est suffisant mais plus étroit (le son n'est pas une déformation visible). | wx_i1_corde (facultatif) |
| basse | Exemple | Matériaux qui conduisent mal le son (isolants phoniques, corps mous ou poreux). Sources : Chouvin p. 3, fiche _3 p. 1. | Absent. | wx_c2_facteurs (facultatif) |

#### Manques chez un seul professeur (tableau court, même colonnes)
| Priorité | Catégorie | Ce que disent les professeurs | Chez nous | Où l'ajouter |
|---|---|---|---|---|
| basse | Tableau de comparaison | Comparaison entre le mouvement d'un corps et la propagation d'une onde (matière ou énergie, trajectoire ou toutes directions, vide ou pas, conditions initiales ou milieu) : Mahajar p. 4. La fiche _3 p. 3 parle d'une « célérité pour la distinguer de la vitesse d'un corps ». | Implicite (wx_p1_vitesse, puis wx_c1_celerite). | wx_c1_celerite (facultatif) |
| basse | Méthode | Chronophotographie : τ = nombre d'intervalles × durée entre deux images (fiche _3 p. 4, « TP chronophotographique » ; experience_profs). | Absent. | Exercice de réserve dans wx_b2_national |
| basse | Exemple | Échographie (cœur à 1,5 cm, Δt = 20 µs) : Bendaoud p. 8-9. Télémètre : Chouvin p. 5. | L'échographie est seulement citée (wx_m2_sonar). | Facultatif |

#### Présent seulement à l'oral (à écrire)
- wx_i2_definition : « milieu élastique = un milieu qui se déforme puis revient à son état » et « la perturbation passe de proche en proche ». Ces deux phrases ne sont ni à l'écran ni au cahier. Trois documents l'écrivent : El Kaouahi p. 1 (« reprend sa forme initiale »), Chouvin p. 1 (encadré), fiche _3 p. 2.
- wx_r2_duree_longueur : la justification de L = v·θ (« pendant θ, le front avance de v·θ ») n'existe qu'à la voix. L'écran et le cahier ne donnent que la formule.
- wx_r1_retard : « plus M est loin, plus τ est grand » n'existe qu'à la voix.
- wx_c2b_temperature : « 340 m/s n'est pas toujours vrai, c'est vers 20 °C » est bien écrit. En revanche « air chaud = plus vite » est écrit sans la valeur 0 °C → 331 m/s, qui ne se trouve que chez Chouvin p. 5. Ce point n'est pas un manque.

#### Démonstrations qui sautent des étapes (id → ce qui manque)
- wx_r1_retard → τ = SM/v est posé sans dériver de v = d/Δt (d = SM, Δt = t_M − t_S, avec t_S = 0). L'écran affiche « τ = t_M − t_S = SM / v » sans le « car v = SM / (t_M − t_S) ». Nidal p. 9 et El Kaouahi p. 3 écrivent la chaîne. De même, y_M(t) = y_S(t − τ) n'est pas justifiée par la phrase type « à la date t, M a l'élongation que S avait à la date t − τ ». La voix dit seulement « M fait ce que S a fait, plus tard ».
- wx_r2_duree_longueur → L = v·θ n'est démontrée qu'à l'oral (voir plus haut). Le passage « θ se lit sur y(t), L sur y(x), donc θ = L/v » (Bendaoud p. 7, θ = l/v) n'est fait dans aucun sens.
- wx_c2_facteurs → la course acier, eau, air affiche des durées, mais t = d/v n'est jamais écrit pour chaque milieu. C'est l'étape qui manque au cas « deux milieux ».
- Les autres calculs (wx_m2b_formule 2d = v·τ, wx_m1b_lecture τ = n × S_H, wx_b2_national pente = 1/v, wx_b1_redaction 0,68/(2×10⁻³) = 340) sont complets et justes.

#### Différences de notation ou de convention (nous / eux, laquelle garder)
| Nous | Eux | À garder |
|---|---|---|
| τ = retard, θ = durée de la perturbation, L = sa longueur | Bendaoud p. 6 : Δt = durée de la perturbation (p. 7 : θ et l) ; fiche _3 p. 3 et p. 8 : θ = retard ; El Kaouahi : τ = t_M' − t_M | Garder les nôtres (décision de la fiche cadre), mais dire en une phrase que l'énoncé peut appeler la durée Δt. |
| « sensibilité horizontale », écrit en toutes lettres | Nidal p. 10 : S_X ; p. 20 : S_h ; experience_profs : S_H | Ajouter le symbole S_H à côté des mots (wx_m1b_lecture). |
| v | V (Mahajar, Nidal, El Kaouahi) ; ϑ (Chouvin) | Garder v. |
| élongation y | « allongement » (Mahajar p. 3, Bendaoud p. 6, Nidal p. 9 « Elongation ») | Garder élongation. On peut citer « allongement » une fois. |
| Dimension 1, 2, 3 | milieu uni-, bi-, tridimensionnel (Mahajar p. 2, Nidal p. 8, Bendaoud p. 4) | Garder les deux écritures (voir la ligne basse des manques). |
| Définition unique « onde mécanique progressive » (OMP1) | Mahajar p. 1 et Bendaoud p. 3 séparent « onde mécanique » et « onde progressive = succession entretenue de signaux » | Garder la nôtre (texte du cadre). |
| La célérité dépend de la nature du milieu (sans parler de densité) | Bendaoud p. 5 et p. 9 (« plus dense »), El Kaouahi p. 3 (« densité ») | Garder la nôtre : « plus dense = plus rapide » est dans a_ne_pas_dire. |
| m/s et m·s⁻¹ | m.s⁻¹ (Bendaoud, Nidal, Chouvin) | Les deux sont déjà écrits. |

#### Hors cadre chez les professeurs (ne pas ajouter)
- Superposition ou croisement de deux ondes : Mahajar p. 2, Bendaoud p. 4-5, Nidal p. 8, El Kaouahi p. 2, Chouvin p. 4. Ce point est dans hors_cadre.
- Formules v = √(F/μ) et v = √(g·h), avec leurs applications : Mahajar p. 4, Bendaoud p. 5-6, Nidal p. 9, El Kaouahi p. 3. Elles sont hors cadre (la tension et μ restent admis seulement de façon qualitative). Une formule donnée par l'énoncé reste un cas d'exercice (experience_profs).
- Ondes S et P des séismes : El Kaouahi p. 1-2 ; ébranlement sismique dans la fiche _3 p. 4.
- Vitesse supersonique et nombre de Mach : fiche _3 p. 4.
- Tout ce qui est périodique (période, λ, stroboscope, phase, diffraction, milieu dispersif) : fiche _3 p. 5-14 et Nidal p. 13-20. C'est le chapitre suivant.

#### Remarque hors comparaison (à vérifier avant publication)
La copie en attente **n'a pas reçu les 14 corrections de l'audit du 15 novembre** (`docs/audit-programme-officiel/physique.md`), alors que la copie en ligne les a. Exemples :
- C1_r3, reponses.0.2.ecrit : la phrase « alors que la lumière… si » est toujours là.
- C8_r3 : le mot « fréquence » est toujours dans 3 réactions.
- C8_r2, reponses.2.2 : la réaction dit encore « 3400 m… tu as oublié de diviser par 2 ».
- C3_r2, reponses.0.1 : la réaction dit encore « 0,12 vient de la division inversée ».

Il faut reporter ces corrections avant de remplacer la copie en ligne.

### Ondes mécaniques progressives périodiques

Sources lues : Mahajar et Tabit (m_…periodiques_1, p. 1-4, lues en image) ; Bendaoud (m_…_2, p. 10-14, en image) ; Chriki (m_…_3, p. 3-8, en image) ; manuel scanné « TS » (m_…_4, p. 1-6, en image) ; Sbiro (m_…_5, p. 1-6, en image) ; Nidal Naceiri Mrabti (nidal_p1, p. 13 en texte, p. 14-20 en image, p. 21-22 vides) ; cadre officiel PC, PDF p. 5 « 2- Ondes mécaniques progressives périodiques » (en image) et annexe 2 (TP). Notre cours : texte des 50 diapos + JSON complet (écran, cahier, tableau `centre`, exercices, rappels, séances). experience_profs.json n'a pas de clé `ondes_mecaniques_periodiques`.

#### Plan comparé
| Partie chez les professeurs | Où chez nous | Remarque |
|---|---|---|
| Activité : son d'un instrument (périodique) / d'un diapason (sinusoïdal) à l'oscilloscope (Mahajar p1, Nidal p14, TS p1, Bendaoud p10) | op_o1 à op_o5 (vibreur, roue, sonnerie) | Aucun exemple d'onde périodique NON sinusoïdale |
| Définitions : onde périodique, sinusoïdale (évolution temporelle) | op_o4_definition, op_o5_sinusoidale | Sinusoïdale définie par la forme de la corde |
| Périodicité temporelle T, N = 1/T | op_t1 à op_t7 | Bien détaillé (oscillogramme, préfixes) ; « plus petite » manque |
| Périodicité spatiale λ, double périodicité | op_l1 à op_l6 | Bien ; pas d'échelle de figure |
| λ = v·T (aspects à T/4, ou deux micros) | op_c1, op_c2, op_c3, op_c4 | Relation trouvée par des nombres |
| En phase / opposition (d = kλ, (2k+1)λ/2) + courbes | op_p1 à op_p4 | Pas de critère écrit pour lire deux courbes |
| Stroboscope (immobilité, ralenti, Ne = N/k) | op_m1, op_m2 | Seulement Ne = N |
| Deux micros / récepteurs, λ et v | op_m3 à op_m6b | Bien (version ultrasons) |
| Diffraction : cuve, a ≤ λ, onde diaphragmée, propriétés | op_d1 à op_d3 | Pas le mot « diaphragmée », pas de son/ultrasons |
| Milieu dispersif (tableau, eau / air) | op_s1 à op_s3 | Bien |
| Retard y_M(t) = y_S(t − τ) | op_r1 à op_r4 | Bien ; sens du 1er mouvement absent |
| Exercices types (coupe de l'eau, QCM, micros, fente ultrasons) | op_x1 à op_x3 | Pas d'exercice de diffraction sonore |

#### Manques confirmés
| Priorité | Catégorie | Ce que disent les professeurs | Chez nous | Où l'ajouter |
|---|---|---|---|---|
| haute | définition | T = la **plus petite** durée pour retrouver le même état vibratoire : Nidal p15, TS p1, Bendaoud p10 (« durée minimale »), Mahajar p2 ; cadre « définir la période » | « la durée au bout de laquelle… » (sans « plus petite » : 2T vérifierait aussi), écran, cahier et bilan | op_t1_periode, op_b1_bilan |
| haute | définition | Onde sinusoïdale = l'élongation de chaque point (ou de la source) varie selon une fonction sinusoïdale **du temps** : Mahajar p2, Bendaoud p10, Nidal p14, Sbiro p1 ; cadre « définir une onde progressive sinusoïdale » | « Source qui vibre régulièrement → onde sinusoïdale » ; « a la forme d'une sinusoïde » (forme dans l'espace seulement) | op_o5_sinusoidale (cahier), op_b1_bilan |
| haute | exemple / méthode | Reconnaître sur un oscillogramme une onde périodique non sinusoïdale (instrument) et une sinusoïdale (diapason), lire T sur les deux : Mahajar p1, Nidal p14, TS p1, Bendaoud p10 ; cadre « reconnaître une onde progressive périodique et sa période » | Aucun exemple périodique non sinusoïdal (0 occurrence « instrument », « diapason ») | op_o5_sinusoidale ou une diapo après op_t7_oscillo |
| haute | loi / condition | La fréquence ne change pas quand l'onde change de milieu ; λ = v/N change avec le milieu : TS p3 (encadré), Nidal p20 (ex. 1, QCM « la fréquence varie avec le milieu »), Chriki p8 (ex. 7, 1.2 « λ varie-t-elle dans l'air ? ») | Seulement « la fréquence est imposée par le vibreur » (diffraction, op_d2) ; rien sur un changement de milieu | op_c2_relation (ligne + cahier), op_b1_bilan |
| haute | condition | Onde diffractée : même N, même v, même λ **si le milieu de propagation n'est pas changé** : Mahajar p4, Nidal p19 ; cadre « caractéristiques de l'onde diffractée » | Cahier op_d2 et bilan : « même fréquence, même λ, même célérité » sans la condition | op_d2_invariants (cahier), op_b1_bilan (point 7) |
| haute | montage / exemple | Diffraction d'une onde sonore ou ultrasonore (fente, porte entrouverte) : Bendaoud p13-14 (ex. 2 : ultrasons 24 kHz, a ≈ λ ; 2 MHz : pas de diffraction), TS p5 ; cadre p5 « proposer le schéma d'un montage… diffraction… ondes sonores et ultrasonores » + TP « diffraction d'une onde sonore ou ultrasonore » | Diffraction seulement dans la cuve à eau ; aucun schéma émetteur → fente → récepteur | nouvelle diapo après op_d3_justifier ; exercice dans op_x2 ou séance 4 bloc 2 |
| moyenne | méthode (stroboscope) | Immobilité apparente si N = k·Ne (Ne = N/k) ; la **plus grande** fréquence des éclairs donnant l'immobilité est N : Bendaoud p11-12, Sbiro p1 et p3 (application), TS p4 (première immobilité en diminuant Ne) | « Condition : fréquence des éclairs = fréquence du vibreur » seulement | op_m2_immobile |
| moyenne | vocabulaire | « Onde diaphragmée » quand a > λ (l'onde passe sans changer de forme) : Bendaoud p13, Chriki p4, Nidal p19 | « l'onde passe tout droit, limitée à la largeur » sans le mot | op_d1_ouverture |
| moyenne | loi | Diffraction d'autant plus marquée que a est petite (λ/a grand) : Bendaoud p13, Chriki p4, TS p5 (question 3) | « nette quand a est de l'ordre de λ ou plus petite » : pas l'évolution | op_d3_justifier |
| moyenne | méthode | Lire en phase / opposition sur deux courbes : en phase si elles s'annulent et atteignent max et min ensemble ; opposition : y₁ = − y₂ (l'une max quand l'autre min) : Sbiro p4, Chriki p3-4, Nidal p17 (deux oscillogrammes) | « même mouvement au même instant » (op_p1) et « courbes en phase » (op_m3) ; pas de critère écrit sur courbes | op_p2_opposition ou op_m5_premier_retour |
| moyenne | méthode | Lire λ avec l'échelle d'une figure (« 1 cm représente 8 cm », échelle 1/10) : Chriki p3, TS p4 (ex. d'entraînement 2), Mahajar p2 (« échelle réelle ») | Toujours une règle posée sur la figure ; « échelle » absent | op_l5_intervalles ou op_x1_national_2017 |
| moyenne | méthode | Sens du mouvement d'un point quand l'onde l'atteint = premier mouvement de la source ; forme du front selon que la lame part vers le haut ou le bas : Sbiro p2 (remarque), Chriki p5 (ex. 1, 3-2) | Absent (ni ch2 ni ch1) | op_r1_retard ou op_r4_source |
| basse | ordre de grandeur | Domaine des λ des sons audibles : 1,7 cm à 17 m (λ = v/N, 20 Hz–20 kHz) : Bendaoud p14, TS p3 | 20 Hz–20 kHz cité (op_m4), pas les λ | op_m4_microsecondes ou op_s2_air |
| basse | exemple | Diffraction par un obstacle ou le bord d'une règle ; plus de « zone d'ombre » derrière : Bendaoud p13 (fig. c), TS p5 (doc. 12) | « (ou un obstacle) » dans la définition seulement | op_d1_ouverture |
| basse | idée | La diffraction est caractéristique des ondes (révèle la nature ondulatoire) : Bendaoud p13, TS p6, Sbiro p5 | Seulement à l'oral de op_b2 (« la lumière aussi se diffracte ») | op_d1_ouverture ou op_b2_carte |
| basse | relation | y(t) = A·cos(2πt/T + φ) (A en m, T en s, φ phase à l'origine) : Nidal p14, Sbiro p1 — non exigé par le cadre pour ce chapitre | Absent | op_o5_sinusoidale (encadré facultatif) |
| basse | schéma | Aspects successifs de la corde à t = 0, T/4, T/2, 3T/4, T : le front avance de λ en T : Bendaoud p11, Sbiro p2 | Animation chrono (op_c1) sans figure écrite | op_c1_avance (cahier_figures) |

#### Manques chez un seul professeur
| Priorité | Catégorie | Ce que dit le professeur | Chez nous | Où l'ajouter |
|---|---|---|---|---|
| basse | méthode | Comparer deux points par les durées : Δt/T = Δt·N = k (entier → en phase ; « ,5 » → opposition) : Chriki p4 | Seulement SM = kλ → τ = kT (op_r2) | op_p3_methode |
| basse | définition | T = durée séparant l'arrivée de deux perturbations successives en un point ; λ = distance entre deux perturbations consécutives : Chriki p3 | Équivalent par « même état » | — |

#### Présent seulement à l'oral (à écrire)
- op_p3_methode : l'écran n'a aucune puce ; « ni entier ni entier et demi (2,25) → ni en phase ni en opposition » et « d et λ dans la même unité » sont dans la voix (et la correction d'un exercice), pas dans le cahier.
- op_c2_relation : « la célérité est une distance sur une durée » (pourquoi v = λ/T) : voix seulement.
- op_t7_oscillo : « T = 5 » sans unité est faux : voix seulement.
- op_l4_rides : sens de l'hypothèse « sans amortissement ni réflexion » (l'amplitude ne diminue pas, rien ne revient des bords) : voix seulement.
- op_b2_carte : lien diffraction → lumière (chapitre suivant) : voix seulement.

#### Démonstrations qui sautent des étapes
- op_c2_relation → λ = v·T est tirée de 0,5/0,5 = 1 ; il manque la ligne générale écrite : v = d/Δt avec d = λ parcourue pendant Δt = T, donc v = λ/T (Bendaoud p11, TS p3, Mahajar p2).
- op_r2_relation → « Si SM = k·λ, alors τ = k·T » : manque τ = SM/v = k·λ/v = k·T (car λ/v = T).
- op_x1_national_2017 → tableau « SM = k · λ → en phase » sans calcul SM/λ = valeur entière (Nidal p17 écrit SM = 3λ).
- op_d2_invariants → λ identique montrée par la mesure ; la déduction λ = v/N (même v car même milieu, même N car même source) n'est écrite que dans une réaction de rappel (C7), pas à l'écran ni au cahier (Bendaoud p13 « par conséquent »).

#### Différences de notation ou de convention
| Nous | Eux | Garder |
|---|---|---|
| N (fréquence) | ν (Mahajar, TS, Sbiro), N (Nidal, Bendaoud) | N (national PC) ; dire une fois que ν et f se voient |
| v en m/s | V ou ϑ ; m.s⁻¹ (Mahajar, Nidal, Bendaoud) | v ; écrire une fois m/s = m·s⁻¹ |
| d = (2k + 1)·λ/2, k ∈ ℕ | (k + ½)·λ, k ∈ ℕ (Nidal p16) ; K ∈ ℤ (Mahajar p3) | la nôtre (Bendaoud, Sbiro, Chriki, national) |
| d = k·λ, « k entier non nul » | k ∈ ℕ* (Nidal, Sbiro) ; k ∈ ℕ (Chriki) | la nôtre, avec le symbole ℕ* |
| retard τ | θ (Chriki p4) | τ |
| diffraction si a ≤ λ | a < λ (Nidal p18-19), a ≈ λ (Sbiro p5) | a ≤ λ (cadre) |
| fréquence des éclairs en mots | Ne (Bendaoud), νe (Sbiro), νE (TS) | ajouter N_e avec le manque stroboscope |

#### Hors cadre chez les professeurs (ne pas ajouter)
- θ = λ/a, sin θ ≈ θ (Chriki p4) et L = 2λD/a (Chriki p8) : chapitre ondes lumineuses (ch3).
- Ralenti apparent dans le même sens / sens contraire (Bendaoud p12, Sbiro p1-2, Mahajar p2) : écarté exprès (audit : montré seulement dans stroboscope.html, « on ne calcule rien »).
- v = √(F/μ) pour la corde (Sbiro p6), v = √(g·h) pour le tsunami (Chriki p5) : donnée d'énoncé seulement.
- Air dispersif pour le tonnerre (TS p6) ; vitesse d'écoulement v⃗ = v⃗₀ + v⃗ₑ (Chriki p8).
- Écho, épaisseur d'une couche (Chriki p5), transversale/longitudinale, c gaz < liquide < solide (Sbiro p3-4) : notions du ch1, pas des manques ici.

### Propagation d’une onde lumineuse
Notre cours audité : `backend/data/courses/phys_ch3_ondes_lumineuses.json` (écran, cahier, `cahier_figures`, voix `fr`, questions, rappels, séances, exercices des nationaux), relu aussi à plat (3 490 champs texte).
Sources lues : (professeur, document, pages lues en image)
- Pr Nidal Naceiri Mrabti, cours 2 BIOF (`nidal_p1.pdf`), p. 22-35 en image (cours p. 23-31, série d'exercices p. 32 ; p. 22, 33, 34 = pages quadrillées vides ; p. 35 = chapitre suivant).
- Pr Hicham Mahajar et Pr Youssef Tabit (`m_…_1`), p. 1-4 en image.
- Pr Ahmed Hakim, lycée Ibn Arabi Fès (`m_…_2`), p. 1-8 en image (p. 1 recopie la liste du cadre de référence 2015 ; p. 8 = TP).
- Pr Delahi Mohamed et Pr Ettaki Khalid (`m_…_3`), p. 1-7 en image.
- Manuel français TS « La lumière, modèle ondulatoire » (`m_…_4`, scan), p. 1-6 en image.
- Pr Sbiro Abdelkrim (`m_…_5`), p. 1-4 en image.
- Aussi lus : cadre officiel `cadre-de-reference-…-spc-2.json` (notion « propagation d'une onde lumineuse » ; TP « diffraction des ondes lumineuses », « dispersion de la lumière blanche »), fiche `cadre_reference_2bac_pc.json` → `ondes_lumineuses` (OL1-OL10, formules, hors_cadre, valeurs_reference), `docs/audit-programme-officiel/physique.md`, SKILL `cours-concentration` (Physique). `experience_profs.json` n'a pas de clé `ondes_lumineuses` (seulement `ondes_mecaniques`).

#### Plan comparé
| Partie chez les professeurs | Chez nous | Remarque |
|---|---|---|
| Laser seul → point ; fente fine → taches ; propagation rectiligne non vérifiée (tous) | ol_d1_tout_droit, ol_d2_fente_fine | Bien fait. « Fente large : pas de diffraction » n'est dit qu'à la voix (ol_d2). |
| Figure : tache centrale 2× plus large, extinctions, ⊥ à la fente ; trou circulaire → anneaux (tous) | ol_d3_figure, ol_d6_fil | Conforme. |
| Analogie avec les ondes mécaniques → aspect ondulatoire (tous) | ol_d4_onde | Conforme à OL1. |
| La lumière est une onde **électromagnétique**, transversale, double périodicité T et λ (Nidal p. 25, Mahajar p. 2, Hakim p. 2, Delahi p. 1, Manuel p. 4, Sbiro p. 2) | ol_r2_vide : « ce n'est pas une onde mécanique » | Le mot « électromagnétique », T et ν = 1/T manquent. |
| Monochromatique / polychromatique, définitions et exemples (tous) | ol_r1_monochromatique, ol_p1_blanche | Monochromatique défini ; polychromatique seulement pour la lumière blanche. |
| Spectre visible 400-800 nm, UV, IR, fréquences limites (tous ; Hz chez Hakim, Delahi, Manuel) | ol_r4_spectre, ol_r3_lambda0 | Bornes en Hz absentes (seulement « ordre de 10¹⁴ Hz »). |
| c, v < c, n = c/v, valeurs d'indices, n = λ₀/λ, λ = λ₀/n, ν invariant (tous) | ol_r2_vide, ol_r2b_celerite, ol_n1…ol_n5 | Complet ; valeurs d'indices seulement à la voix. |
| Influence de a et de λ ; θ = λ/a ; tan θ = L/2D ; L = 2λD/a (tous) | ol_t1…ol_t4, ol_l1…ol_l9 | Très complet (rappels radian/tangente, conversions, ordre de grandeur, rédaction en 4 lignes). |
| Vérifier θ = λ/a par mesures : tableau a, L, θ = L/2D, courbe θ = f(1/a), pente = λ (Nidal p. 26-27, Sbiro p. 2, Hakim p. 8 TP) | ol_g1…ol_g4 (courbe L = f(1/a)), ol_g5 (θ = f(1/a) en une ligne) | Méthode faite sur L = f(1/a) ; θ = f(1/a) n'est qu'une puce. |
| Fil : θ = λ/d (Nidal p. 27, Sbiro p. 2, Delahi p. 4, Mahajar p. 2) | ol_d6_fil, ol_c4_cheveu | d = 2λD/L écrit ; θ = λ/d jamais écrit. |
| Diffraction en lumière blanche : centre blanc, bords irisés (Delahi p. 4, Manuel p. 3, Nidal p. 32 ex. 1) | ol_p5_fente_blanche | Conforme. |
| Réfraction (définition), dispersion par le prisme, violet le plus dévié, interprétation n → v → dispersif (tous) | ol_p1…ol_p4 | La chaîne de déduction n = c/v ⇒ v dépend de ν n'est pas écrite. |
| Relations du prisme, Snell-Descartes en calcul (tous) | — | Hors cadre (retiré exprès, OL11). |
| Exercices types (laser → ν, v et λ dans un milieu ; λ par diffraction ; courbe) | ol_n5, ol_x2…ol_x4, ol_c3, ol_g5 | Couverts, avec les nationaux 2021 N, 2023 R, 2025 R. |

#### Manques confirmés
| Priorité | Catégorie | Ce que disent les professeurs | Chez nous | Où l'ajouter |
|---|---|---|---|---|
| haute | Définition | « Une lumière polychromatique est constituée de plusieurs radiations monochromatiques » : Nidal p. 25, Hakim p. 3 et p. 5 (« au moins deux radiations de fréquences différentes »), Sbiro p. 3, Mahajar p. 4 ; cadre OL6 « définir… une lumière polychromatique » | Seulement « la lumière blanche est polychromatique : infinité de radiations » (ol_p1). Aucune définition générale à l'écran ni au cahier. | ol_r1_monochromatique (définir les deux côte à côte), rappel dans ol_p1_blanche et au bilan ol_b1_bilan (bloc 6) |
| haute | Rédaction / interprétation | Chaîne écrite : les radiations ne sont pas déviées de la même façon (D_R ≠ D_V) ⇒ n dépend de la fréquence ; **or n = c/v avec c constante** ⇒ v dépend de ν ⇒ le verre est dispersif : Nidal p. 30-31, Hakim p. 7, Delahi p. 7, Manuel p. 6, Mahajar p. 4 ; cadre OL10 « interpréter la dispersion » | ol_p2 dit « pourquoi ? parce que chaque radiation a son indice » (cause affirmée, pas déduite) ; ol_p3 passe par v = λ·ν ; le lien n = c/v ⇒ v dépend de ν n'est écrit nulle part | ol_p2_violet ou ol_p4_dispersif : 3 lignes « observation → n dépend de ν → v = c/n dépend de ν → dispersif » |
| haute | Schéma / montage | Montage annoté laser – fente (a) – écran à D – tache L – θ dessiné par les 6 : Nidal p. 26, Mahajar p. 2, Hakim p. 4 et 8, Delahi p. 1, Manuel p. 3, Sbiro p. 1 ; cadre 2015 cité par Hakim p. 1 « proposer le schéma d'un montage expérimental… diffraction » | Le montage n'existe qu'en simulation (ol_d5). Au cahier : les trois définitions en mots ; le croquis de ol_t1 n'a que « fente » et θ (ni laser, ni écran, ni a, D, L) | ol_d5_montage : `cahier_figures` « schéma du montage » avec laser, fente a, écran, D, L, θ |
| moyenne | Définition / nature | « La lumière est une onde électromagnétique » (se propage dans le vide et les milieux transparents) : Nidal p. 25, Mahajar p. 1-2, Hakim p. 2, Delahi p. 1, Manuel p. 4, Sbiro p. 2 | « La lumière n'est pas une onde mécanique » seulement (ol_r2, rappel C6) ; le mot « électromagnétique » n'apparaît jamais | ol_r2_vide (une puce + cahier) |
| moyenne | Relation / grandeur | Double périodicité : T et ν = 1/T ; λ₀ = c·T = c/ν : Nidal p. 25, Mahajar p. 2, Hakim p. 2, Delahi p. 2, Manuel p. 5 ; cadre (variante admise λ₀ = c·T) | λ₀ = c/ν seulement ; T jamais défini ici, alors que des réactions écrites l'emploient (séance 5 bloc 1 : « lambda = v × T ») | ol_r3_lambda0 : ajouter « ν = 1/T ; λ₀ = c·T = c/ν » |
| moyenne | Condition | Diffraction visible seulement si l'ouverture ou l'obstacle est petit, de l'ordre de λ (jusqu'à ~100 λ) ; fente large : une seule tache, pas de diffraction : Mahajar p. 1-2 (10λ ≤ a ≤ 100λ), Hakim p. 8 (« de λ à 100 λ »), Delahi p. 3, Manuel p. 1-2 ; cadre OL2 | « Fente très fine » sans ordre de grandeur ; « fente de 0,4 mm : presque tout droit » seulement à la voix | ol_d2_fente_fine (puce « condition ») |
| moyenne | Définition | « Tous les milieux transparents sont plus ou moins dispersifs ; l'air l'est très peu (comme le vide) » : Hakim p. 7, Manuel p. 6 ; Delahi p. 7 (air et vide non dispersifs) ; cadre OL10 « plus ou moins dispersifs » | Seul « le vide n'est pas dispersif » (ol_p4) | ol_p4_dispersif |
| moyenne | Méthode | Vérifier θ = λ/a par mesures : pour chaque fente θ = L/(2D), tableau (a, 1/a, L, θ), courbe θ = f(1/a) droite par l'origine, pente k = λ ⇒ θ = λ/a : Nidal p. 26-27, Sbiro p. 2, Hakim p. 8 (TP) ; cadre 2015 cité par Hakim p. 1 « exploiter des mesures… vérifier θ = λ/a » | ol_g5 : une puce « θ = f(1/a) : k = λ », sans tableau ni calcul de θ | ol_g5_autres (ou une diapo ol_g6 courte : tableau + pente) |
| moyenne | Ordre de grandeur | Fréquences du visible : 3,75·10¹⁴ Hz (rouge, 800 nm) à 7,5·10¹⁴ Hz (violet, 400 nm), parfois en THz : Hakim p. 2-3 (exercice), Delahi p. 3, Manuel p. 5 ; fiche `valeurs_reference` | « De l'ordre de 10¹⁴ Hz » (ol_r3) | ol_r4_spectre (bornes en Hz sous la bande) |
| basse | Relation | Fil : θ = λ/d : Nidal p. 27, Sbiro p. 2 ; Delahi p. 4 et Mahajar p. 2 (« fil de diamètre a ») ; variante admise de la fiche | « d prend la place de a », d = 2λD/L ; θ = λ/d non écrit | ol_c4_cheveu |
| basse | Propriété | L'onde diffractée garde la même λ, la même fréquence et la même célérité : Mahajar p. 2, Delahi p. 1 | Non dit dans ce chapitre | ol_d4_onde |
| basse | Propriété | La lumière transporte de l'énergie (énergie lumineuse, rayonnante) : Hakim p. 2, Manuel p. 4 | Absent | ol_r2_vide |
| basse | Valeur | c = 299 792 458 m·s⁻¹ ≈ 3·10⁸ : Nidal p. 25, Mahajar p. 2, Manuel p. 4 | 3,00·10⁸ m/s seulement | ol_r2b_celerite (une parenthèse) |
| basse | Exemple | Arc-en-ciel = dispersion de la lumière du Soleil par les gouttes d'eau : Nidal p. 23, Manuel p. 6 (qualitatif admis par la fiche) | Absent | ol_p1_blanche |
| basse | Description | La fente se comporte comme une source lumineuse (secondaire) : Mahajar p. 1, Sbiro p. 1 | Absent | ol_d2_fente_fine (voix) |
| basse | Ordre de grandeur | UV et IR situés au-delà : UV jusqu'à ~10 nm, IR jusqu'à ~1 mm : Hakim p. 3, Delahi p. 3 (bande des ondes électromagnétiques) | UV < 400 nm, IR > 800 nm seulement | ol_r4_spectre (facultatif) |

#### Manques chez un seul professeur
| Priorité | Catégorie | Ce que dit le professeur | Chez nous | Où l'ajouter |
|---|---|---|---|---|
| basse | Méthode | L se mesure entre les milieux des deux premières extinctions ; la figure est symétrique (Hakim p. 4) | Dit seulement à la voix (« d'une extinction à l'autre ») | ol_d5_montage |
| basse | Condition | « Petit angle : θ ≤ 15° » pour tan θ ≈ θ (Sbiro p. 1) | « θ petit, en radian » | rien (garder notre formulation) |
| basse | Exercice | Courbe L' = f(1/d) avec des fils de diamètres différents (Nidal p. 32, ex. 1 B) | Courbes seulement avec des fentes | rappel C5 ou séance 4 (variante) |
| basse | Tableau | Indices du verre par couleur (rouge 1,618 … violet 1,652) (Mahajar p. 3) | n(rouge) < n(violet), qualitatif | rien |
| basse | Montage | Montage de dispersion : source, condenseur, fente, lentille, prisme, écran (Manuel p. 6) | Lampe + prisme + écran | rien |

#### Présent seulement à l'oral (à écrire)
- ol_n4_indice : valeurs « air ≈ 1 ; eau 1,33 ; verre ≈ 1,5 » (écrites chez Delahi p. 2, Manuel p. 4, Sbiro p. 3 et dans la fiche) ; l'écran et le cahier n'ont que n = c/v, n ≥ 1, v = c/n.
- ol_d5_montage : L mesurée « d'une extinction à l'autre » (de la 1ʳᵉ extinction à gauche à la 1ʳᵉ à droite).
- ol_d2_fente_fine : « fente de 0,4 mm : la lumière passe presque tout droit » (fente large → pas de diffraction).
- ol_n2_frequence : « la source impose la fréquence » (Hakim p. 2, Delahi p. 1 l'écrivent) ; chez nous, à la voix et dans des réactions, pas à l'écran ni au cahier.
- ol_r2_vide : expérience de la sonnette sous cloche à vide (on la voit, on ne l'entend plus) : seulement à la voix.

#### Démonstrations qui sautent des étapes
- ol_n5_lambda_n : « λ = λ₀·v/c = λ₀/n » : il manque « or v/c = 1/n, car n = c/v ». La forme n = λ₀/λ (Nidal p. 25, Mahajar p. 3, Sbiro p. 3) n'est écrite qu'au lead du bilan (ol_b1).
- ol_n5_lambda_n / ol_c5_cuve : « L proportionnelle à λ, donc L' = L/n et n = L/L' » : il manque les deux expressions L = 2λ₀D/a (air) et L' = 2λD/a (liquide, même a et D), puis le quotient L/L' = λ₀/λ = n. C'est la question « vérifier n = L/L' » du national 2025 R (ol_x4).
- ol_p2_violet : l'ordre est inversé (« pourquoi ? parce que chaque radiation a son indice »). Au bac, on déduit : déviations différentes ⇒ indices différents ⇒ v = c/n différentes ⇒ dispersif (voir manque haute).
- ol_g5_autres : « θ = f(1/a) : k = λ » sans l'étape où chaque θ est calculé par θ = L/(2D) à partir des mesures (Nidal p. 26, Sbiro p. 2).
- Rien à redire sur ol_l9_etablir (les 4 lignes), ol_c3_rapport (division membre à membre), ol_g3/ol_g4 (pente avec unités, identification), ol_l6_isoler.

#### Différences de notation ou de convention
- Nom de θ : nous « écart angulaire » (comme le cadre) ; eux aussi « demi-largeur angulaire » (Hakim p. 4), « demi-écart angulaire » (Manuel p. 3), « angle de diffraction » (Delahi p. 4), « angle sous lequel on voit la moitié de la tache centrale depuis la fente » (Nidal p. 26, Sbiro p. 1). Garder « écart angulaire » ; citer une fois les autres noms (ils apparaissent dans les énoncés).
- Demi-largeur notée d : Hakim p. 4 (tache = 2d, tan θ = d/D) et Delahi p. 4 (d = L/2). Garder L (largeur totale) ; prévenir que d est chez nous le diamètre du fil.
- Fil : diamètre « a » chez Nidal p. 27, Mahajar p. 2, Delahi p. 4 ; « d » chez Sbiro p. 2, Nidal (remarque). Garder d (fiche).
- λ ou λ₀ dans θ = λ/a : Nidal p. 28 écrit θ = λ₀/a ; nous λ. Garder λ, et écrire une fois « dans l'air, λ ≈ λ₀ ».
- Vitesse : nous v ; V (Nidal, Mahajar, Delahi), ϑ (Manuel), et Sbiro écrit la fréquence υ, très proche de v. Garder v et ν.
- Unités : nous « m/s » ; tous les professeurs « m·s⁻¹ » (notation des sujets nationaux). Garder m/s si c'est la règle des autres chapitres, mais montrer une fois « m/s = m·s⁻¹ ».
- Bornes du visible : 400 nm < λ < 800 nm (Nidal p. 25), 400-780 nm (Delahi p. 3, schéma) ; garder 400-800 nm (fiche).
- Erreurs chez les professeurs, à ne pas reprendre : Mahajar p. 2 « onde longitudinale électromagnétique » (la lumière est transversale, Nidal p. 25) ; Mahajar p. 4 « n_R = n_V » (au lieu de ≠) ; Nidal p. 25 « c = 29979245 » (chiffre manquant) ; Nidal p. 28 « λ₀ = 6×10⁻⁶ m » puis « 600 nm » (c'est 6×10⁻⁷ m).

#### Hors cadre chez les professeurs (ne pas ajouter)
- Lois de Snell-Descartes en calcul (n₁ sin i₁ = n₂ sin i₂) et applications chiffrées : Nidal p. 28-29, Mahajar p. 3, Hakim p. 6-7, Sbiro p. 3-4, Manuel p. 6.
- Relations du prisme sin i = n sin r, A = r + r', D = i + i' − A et leurs démonstrations : Nidal p. 29-30 et ex. 2 p. 32, Mahajar p. 3-4, Hakim p. 6, Delahi p. 5-6, Sbiro p. 4 (OL11 retiré le 15/11).
- Trou circulaire θ = 1,22 λ/d : Nidal p. 27-28, Sbiro p. 2 (« 1,22 λ/a » est dans les mots hors cadre).
- Loi de Cauchy n = a + b/λ² : Sbiro p. 4.
- Diffraction par un CD ou la trame d'un voilage (réseau) : Manuel p. 3.
- Spectre de raies de la lampe à mercure : Manuel p. 5, Hakim p. 3 (« spectre discontinu ») : chapitre « Atome et mécanique de Newton ».
- Description champ électrique + champ magnétique : Nidal p. 25, Mahajar p. 2 : dire seulement « onde électromagnétique ».
- Rayons γ, X, ondes hertziennes (bande des ondes électromagnétiques) : Delahi p. 3, Manuel p. 4 : au plus une image, sans contenu à apprendre.

### Décroissance radioactive
Notre cours audité : `backend/data/courses/phys_ch4_radioactivite.json` (diapos ra_*, écran, cahier, voix `fr`, questions, rappels, exercices des blocs).
Sources lues : (professeur, document, pages lues en image)
- Pr Nidal Naceiri Mrabti, cours 2 BIOF (`nidal_p1.pdf`), p. 36-47 en image (p. 36-43 cours, p. 44 série d'exercices, p. 45-47 pages quadrillées vides).
- Pr Hicham Mahajar et Pr Youssef Tabit (`m_Decroissance-radioactive_1`), p. 1-7 en image.
- Pr Zakaryae Chriki (`_2`, résumé n° 5, « SM PC SVT »), p. 1-4 en image.
- Auteur « hajji » (`_3`, « Radioactivité spontanée »), p. 1-5 en image (p. 1-2 sur ce chapitre ; p. 2-5 : u, défaut de masse, fission, fusion = chapitre suivant ; p. 5 datation).
- Manuel français TS mis en page par J. Chouvin (`_4`, scan), p. 1-8 en image.
- Pr Sbiro Abdelkrim (`_5`), p. 1-6 en image.
- Aussi lus : cadre officiel (`cadre-de-reference-…-spc-2.json`, « Décroissance radioactive (composition du noyau, isotope, diagramme N/Z, α, β⁺, β⁻, γ, loi de décroissance, demi-vie) »), fiche `cadre_reference_2bac_pc.json` → `radioactivite` (RA1-RA10, formules, hors_cadre, décisions), `docs/audit-programme-officiel/physique.md` (section ch4). `experience_profs.json` n'a pas de clé `radioactivite` (seulement `ondes_mecaniques`).

#### Plan comparé (tableau : partie chez les professeurs → où chez nous → remarque)
| Partie chez les professeurs | Chez nous | Remarque |
|---|---|---|
| Situation-problème, histoire (Becquerel 1896, Curie, Rutherford) : Nidal p. 36, Mahajar p. 2-3, Sbiro p. 1, Chouvin p. 1 | ra_n1_ouverture | Ouverture par la datation du bois ; aucune histoire. |
| Composition du noyau, ᴬ_Z X, masses et charges du proton et du neutron (Nidal p. 37, Mahajar p. 1, Chriki p. 1, hajji p. 1, Sbiro p. 1) | ra_n2_atome, ra_n3_compter, ra_n4_notation, ra_n5_composition | Bien fait. Pas de valeurs mₚ, mₙ, e. |
| Élément chimique, nucléide, isotopes, abondance naturelle (Nidal p. 37, Mahajar p. 1, Chriki p. 1, Sbiro p. 1) | ra_n6_isotopes | Manquent « élément chimique » et l'abondance. |
| Dimension et masse volumique du noyau r = r₀A^(1/3) (Mahajar p. 1, Sbiro p. 1) | — | Hors fiche (voir dernière section). |
| Diagramme (N, Z) : Z < 20 → N ≈ Z (A/Z ≈ 2), lourds N > Z, zones β⁻, β⁺, α, isotopes sur une même droite (Nidal p. 38-39, Mahajar p. 2, Chriki p. 1, Chouvin p. 2-3, Sbiro p. 2) | ra_s1_diagramme … ra_s5_isotopes_ligne | Bien fait, plus progressif. Le seuil Z < 20 manque. |
| Définition, propriétés : aléatoire, spontanée, inévitable, indépendante de T, P, liaisons chimiques (Nidal p. 39, Mahajar p. 4, Chriki p. 1, Chouvin p. 1) | ra_r1_definition, ra_r2_caracteres, ra_r2b_spontanee | Bien fait ; les liaisons chimiques ne sont pas citées. |
| Lois de Soddy (tous) | ra_r3_soddy, ra_d5_inconnu, ra_d6_type | Bien fait. |
| α, β⁻, β⁺, γ : équations, mécanisme n → p, p → n, flèches sur le diagramme, Y* (tous) | ra_s4_fleches, ra_s4b_alpha, ra_d1_alpha … ra_d4_gamma | Bien fait. Manquent : pénétration de α et β, β⁺ « artificiels », état fondamental. |
| Famille radioactive, 4 familles naturelles, diagramme (Nidal p. 40 et 44, Mahajar p. 5-6, Chriki p. 2, Sbiro p. 4) | ra_f1_famille, ra_f2_systeme, ra_f3_famille2024 | Plus riche que chez eux (système y, x). Les 4 familles naturelles manquent. |
| Loi : établir N(t), λ (s⁻¹), m(t) et n(t) (Nidal p. 41, Mahajar p. 6, Chriki p. 3, Sbiro p. 4 et 6, Chouvin p. 6) | ra_l1_echantillon … ra_l5_loi, ra_l6_lambda | Loi bien amenée. Manquent m(t) = m₀·e^(−λt) et n(t). ra_l6_lambda n'a aucune puce à l'écran. |
| τ = 1/λ (en s), N(τ) = 0,37·N₀, tangente à l'origine (Nidal p. 42, Mahajar p. 6, Chriki p. 3, Sbiro p. 5, Chouvin p. 7) | ra_l7_tau | Unité de τ absente ; lecture à 0,37·N₀ non décrite comme méthode. |
| Demi-vie : définition, démonstration, N₀/2ⁿ, tableau de valeurs (tous) | ra_t1_definition … ra_t4_pourcentages | Bien fait ; pas de tableau d'ordres de grandeur. |
| Activité : −dN/dt, Bq (Ci), a = λN, a(t), courbe a(t) avec τ (Nidal p. 42-43, Mahajar p. 7, Chriki p. 3-4, hajji p. 2, Sbiro p. 5, Chouvin p. 6-7) | ra_a1_compteur … ra_a7_droite_ln | Bien fait. Manquent τ sur a(t), « nombre moyen », Ci. |
| Masse ↔ nombre de noyaux (Nidal p. 41 et 44, Chriki p. 4, Sbiro p. 6, Chouvin p. 7) | ra_p4_mole, ra_a5_masse | Sens m → N seulement ; jamais N → m. |
| Datation : C14 produit dans la haute atmosphère, échantillon témoin, choix du nucléide, formule (Nidal p. 43, Mahajar p. 7, Chriki p. 3, hajji p. 5, Chouvin p. 8, Sbiro p. 5-6) | ra_c1_principe, ra_c2_demo, ra_c3_calcul | Bon ; manquent l'origine du C14 et la limite du C14 (choix du nucléide). |
| Roche : rapport fils/père | ra_c4_fils_pere, ra_c4b_rapport | Chez nous seulement (cadre RA10). |
| Rappels exp et ln (Sbiro p. 6) | ra_l4a_exp, ra_l4_rappel, ra_p3_puissances | Plus riche chez nous. |
| Exercices (Nidal p. 41, 43, 44 ; Chouvin p. 7-8) | ra_x1_cas_types … ra_x4_2025N | Plus riche chez nous (nationaux). |

#### Manques confirmés (tableau trié)
| Priorité | Catégorie | Ce que disent les professeurs | Chez nous | Où l'ajouter |
|---|---|---|---|---|
| haute | Loi (autre forme) | La loi vaut aussi pour la masse et la quantité de matière : m(t) = m₀·e^(−λt), n(t) = n₀·e^(−λt). Sources : Nidal p. 41 (n(t)), Chriki p. 3 (encadré m et n), Sbiro p. 6 (démontré à partir de N = (m/M)·N_A). La fiche admet m(t) = m₀·e^(−λt) (variante de RA6). | Aucune occurrence de m₀, m(t), n₀ dans tout le JSON. | ra_l5_loi (puce « même loi pour m et n, car N = (m/M)·N_A ») ; ra_z1_bilan |
| haute | Unité | τ = 1/λ a la dimension d'un temps, en seconde (s) dans le SI. Sources : Nidal p. 42, Mahajar p. 6, Chriki p. 3, hajji p. 1 ; fiche : « τ en s ». | ra_l7_tau ne donne aucune unité (écran, cahier, voix). « τ en jours » n'apparaît que dans les réactions de l'exercice du bloc seances[3].blocs[0]. | ra_l7_tau (puce « τ en s, ou dans l'unité de t : c'est une durée ») |
| haute | Méthode, exercice type | Calculer une masse à partir d'un nombre de noyaux ou d'une activité : m₀ = (N₀/N_A)·M (Nidal p. 41, application Q3 ; p. 44, ex. 2 Q4 et ex. 3 Q4 « masse injectée m₀ pour a₀ = 37 Bq ») ; arbre « a = λN, N ↔ n = N/N_A = m/M, m = N·m₁ » (Chriki p. 4). | Seul le sens m → N existe (ra_a5_masse, exercice seances[4].blocs[0]). Jamais N → m ni a → m. | ra_a5_masse (puce « inverse : m = (N/N_A)·M ») ; un exercice a → N → m dans le bloc seances[4] |
| moyenne | Méthode (exploiter une courbe) | Deuxième lecture de τ : placer 0,37·N₀ (ou N₀/e) sur l'axe, projeter sur la courbe puis sur l'axe des temps. Sources : Chriki p. 3 (« Comment déterminer graphiquement τ »), Nidal p. 42 (figure 0,37·N₀), Sbiro p. 5 (figure), Chouvin p. 7 (N₀/e sur la figure). | ra_l7_tau écrit « N(τ) ≈ 0,37·N₀ » mais la méthode de lecture n'est pas écrite ; « Ce point donne τ » renvoie à la tangente. | ra_l7_tau (puce « ou : on lit t pour N = 0,37·N₀ ») |
| moyenne | Méthode (exploiter une courbe) | τ se lit aussi sur la courbe a(t) : tangente à l'origine ou a = 0,37·a₀. Sources : Nidal p. 43 (figure a(t) avec 0,37·a₀ et τ), Chouvin p. 7 (doc. 16, A₀/e) ; fiche RA9 (« courbe N(t) ou a(t) … tangente à l'origine et τ »). | ra_a6_courbe_a ne lit que a₀/2 → t½. Aucune tangente sur a(t). | ra_a6_courbe_a (puce « tangente à l'origine ou 0,37·a₀ → τ ») |
| moyenne | Propriété (qualitatif admis) | Pouvoir de pénétration : α arrêtée par une feuille de papier, β par quelques mm d'aluminium, γ par du béton ou du plomb. Sources : Sbiro p. 2 (texte et figure), Chouvin p. 1 (activité 1), p. 3 (note 1, β) et p. 4 (α, γ) ; fiche : « qualitatif_admis : pouvoir de pénétration ». | Seul γ est traité (ra_d4_gamma, puce 4). Rien sur α ni β. | ra_d1_alpha (« arrêtée par une feuille de papier ») ; ra_d2_beta_moins (« quelques mm d'aluminium ») |
| moyenne | Datation (explication) | Le carbone 14 est produit en permanence dans la haute atmosphère par l'action des neutrons cosmiques sur l'azote ; le rapport C14/C12 y reste constant. Sources : Nidal p. 43, Mahajar p. 7, Chouvin p. 8 (doc. 17), hajji p. 5 (« régénéré dans l'atmosphère », 10⁻¹²). | ra_c1_principe explique les échanges avec l'air, mais jamais d'où vient le C14 de l'air (« cosmique » : 0 occurrence). | ra_c1_principe (une puce) |
| moyenne | Datation (choix du nucléide) | Plus l'échantillon est ancien, plus la demi-vie du nucléide utilisé doit être grande. Le C14 ne date pas au-delà d'environ 40 000 ans ; pour les roches on utilise U/Pb, K/Ar. Sources : Nidal p. 43, Mahajar p. 7, Chouvin p. 8 (doc. 19). | Absent (« 40 000 » : 0 occurrence). ra_c4_fils_pere parle de la roche sans dire pourquoi on n'utilise pas le C14. | ra_c1_principe ou ra_c4_fils_pere (une puce) |
| moyenne | Condition (diagramme) | Le seuil : pour Z < 20 (noyaux légers), les stables sont près de N = Z (A/Z ≈ 2) ; pour Z > 20, au-dessus. Sources : Nidal p. 38-39, Mahajar p. 2, Chriki p. 1, Chouvin p. 2. | ra_s2_vallee dit « légers : N ≈ Z », sans dire ce qu'est un noyau léger. | ra_s2_vallee (« légers (Z < 20) ») |
| basse | Définition | Élément chimique : ensemble des atomes et des ions qui ont le même nombre de protons Z. Sources : Nidal p. 37, Mahajar p. 1. | « élément chimique » n'apparaît que dans « X : le symbole de l'élément chimique » (ra_n4_notation). | ra_n6_isotopes |
| basse | Ordres de grandeur | Proton : m ≈ 1,67·10⁻²⁷ kg, charge e = 1,6·10⁻¹⁹ C ; neutron : m ≈ 1,67·10⁻²⁷ kg, charge 0. Sources : Nidal p. 37 (tableau), Sbiro p. 1, hajji p. 1 (e). | Charges + et 0 seulement (ra_n2_atome). | ra_n2_atome (facultatif) |
| basse | Exemple | Abondance naturelle des isotopes (U : 99,276 / 0,718 / 0,006 % ; O 16, 17, 18). Sources : Nidal p. 37, Mahajar p. 1 (remarque), Sbiro p. 1. | Absent. | ra_n6_isotopes (facultatif) |
| basse | Définition | γ : le noyau fils excité possède un excédent d'énergie par rapport à son état fondamental ; Y* = état excité, Y = état fondamental. Sources : Nidal p. 40, Mahajar p. 5, Chriki p. 2, Chouvin p. 4, Sbiro p. 4. | Écran : « noyau fils souvent excité : Y* ». « Trop d'énergie » n'est qu'à la voix ; « fondamental » n'est que dans une réaction du rappel C4_r3. | ra_d4_gamma |
| basse | Propriété | β⁺ concerne surtout des noyaux artificiels. Sources : Mahajar p. 5, Chouvin p. 3, Sbiro p. 3. | « artificiel » : 0 occurrence. | ra_d3_beta_plus |
| basse | Propriété | La particule α est un noyau d'hélium ionisé He²⁺ (charge +2e). Sources : Mahajar p. 3, Chouvin p. 3, Sbiro p. 2. | « noyau d'hélium ⁴₂He » sans la charge. | ra_d1_alpha (facultatif) |
| basse | Propriété | La radioactivité (et λ) ne dépend ni des conditions physiques ni des liaisons chimiques de l'atome ; λ ne dépend pas des conditions initiales. Sources : Mahajar p. 4 et 6, Chriki p. 3. | ra_r2b_spontanee : température et pression seulement. | ra_r2b_spontanee ; ra_l6_lambda |
| basse | Exemple | Quatre familles naturelles : ²³⁸U, ²³⁵U, ²³²Th, ²³⁷Np. Sources : Nidal p. 40, Mahajar p. 5. | Absent (ra_f1_famille ne cite que U 238). | ra_f1_famille (facultatif) |
| basse | Ordres de grandeur | Tableau de demi-vies très différentes (de 3·10⁻⁷ s à 10⁹ ans) ; t½ est caractéristique du nucléide et ne dépend pas de N₀. Sources : Nidal p. 42, Chouvin p. 6 (doc. 14), hajji p. 2, Chriki p. 3. | Valeurs dispersées dans les exemples ; aucune phrase « t½ caractéristique du nucléide » (seul λ est « propre au nucléide », cahier de ra_l6_lambda). | ra_t1_definition |
| basse | Définition | Activité = nombre **moyen** de désintégrations par seconde. Sources : Nidal p. 42, Chouvin p. 6. | « nombre de désintégrations par seconde » (ra_a2_definition). | ra_a2_definition (facultatif) |
| basse | Unité | Le curie : 1 Ci = 3,7·10¹⁰ Bq. Sources : Mahajar p. 7, Chouvin p. 6. | Absent. | ra_a2_definition (facultatif) |
| basse | Loi | a(n·t½) = a₀/2ⁿ (variante de la fiche). Sources : Nidal p. 44 (ex. 2 Q3), Chouvin p. 7 (doc. 16 : A₀/2, A₀/4, A₀/8). | Seulement « moitié des noyaux, moitié de l'activité » (ra_a3b_loi_activite) et a = a₀/4 dans un exercice. | ra_a3b_loi_activite |
| basse | Propriété | a = (ln2/t½)·N : à N égal, le nucléide de plus courte demi-vie a la plus grande activité. Sources : Chouvin p. 7, hajji p. 2. | Seul le QCM de ra_x4_2025N (« plus λ est petite, plus la décroissance est lente »). | ra_a3_demo (facultatif) |
| basse | Culture | Découverte (Becquerel 1896, Marie et Pierre Curie). Sources : Mahajar p. 2-3, Sbiro p. 1, Chouvin p. 1. | « Becquerel » n'existe que comme unité. | ra_n1_ouverture ou ra_a2_definition (une phrase) |

#### Manques chez un seul professeur (tableau court, même colonnes)
| Priorité | Catégorie | Ce que disent les professeurs | Chez nous | Où l'ajouter |
|---|---|---|---|---|
| moyenne | Méthode (5τ) | À t = 5τ, N = N₀·e⁻⁵ ≈ N₀/100 : 99 % des noyaux sont désintégrés : Chouvin p. 7. | Absent. | ra_l7_tau (facultatif) |
| moyenne | Méthode (63 %) | À t = τ, 63 % des noyaux sont désintégrés : Nidal p. 42 (Mahajar p. 6 écrit à tort « 37 % désintégrés »). | On écrit seulement 0,37·N₀ restants. | ra_l7_tau (« 37 % restent, 63 % désintégrés ») |
| basse | Loi (autre écriture) | N(t) = N₀·2^(−t/t½) : Mahajar p. 7. | Absent. | facultatif |
| basse | Méthode | Droite ln a = f(t) (fiche RA9 seule, aucun professeur). | Seulement ln N = f(t) (ra_a7_droite_ln). | ra_a7_droite_ln (une ligne « même chose avec ln a ») |
| basse | Datation (hypothèse) | Hypothèse : la teneur en C14 de l'atmosphère est restée constante : Chouvin p. 8. | Absent. | ra_c1_principe (facultatif) |
| basse | Vocabulaire | « Période radioactive » = demi-vie : Chriki p. 3. | Absent. | facultatif |

#### Présent seulement à l'oral (à écrire)
- ra_l6_lambda : « λ·t n'a pas d'unité, donc λ et t doivent utiliser la même unité de temps » n'est qu'à la voix. Cette diapo n'a d'ailleurs **aucune puce** à l'écran (seulement le lead et la trace).
- ra_c2_demo : l'étape « ln(a/a₀) = −λt, puis on inverse la fraction pour enlever le signe moins » n'est qu'à la voix ; l'écran passe de a/a₀ = e^(−λt) à ln(a₀/a) = λt.
- ra_c4b_rapport : « 1 + r = e^(λt), on prend ln » n'est qu'à la voix.
- ra_d4_gamma : « il a trop d'énergie » (excédent d'énergie) n'est qu'à la voix.
- ra_d2_beta_moins : « le noyau ne contenait pas d'électron : il est créé à cet instant » n'est qu'à la voix.
- ra_s2_vallee : « être sur la droite N = Z ne suffit pas, il faut être dans la vallée » n'est qu'à la voix.
- ra_t3_paliers : « le nombre ne devient jamais zéro, seulement très petit » n'est qu'à la voix (l'idée est écrite pour e^(−x) dans ra_l4a_exp).

#### Démonstrations qui sautent des étapes (id → ce qui manque)
- ra_l3_equation → la ligne « nombre de noyaux désintégrés pendant dt = N(t) − N(t + dt) = −dN » (Mahajar p. 6, Chouvin p. 5) manque : on passe directement à dN = −λ·N·dt.
- ra_l5_loi → la vérification ne contrôle que l'équation ; il manque la condition initiale N(0) = N₀·e⁰ = N₀ (Mahajar p. 6 l'utilise pour trouver la constante).
- ra_l7_tau → N(τ) = N₀·e^(−λ·(1/λ)) = N₀·e⁻¹ : l'étape λ·τ = 1 n'est pas écrite. Pourquoi la tangente coupe l'axe en τ n'est pas justifié (aucun professeur ne le fait non plus).
- ra_t3_paliers → N₀/2ⁿ est obtenu en divisant par 2 à chaque palier, sans le calcul N(n·t½) = N₀·e^(−λ·n·t½) = N₀·e^(−n·ln2) = N₀/2ⁿ (Sbiro p. 5).
- ra_t4_pourcentages → affiche t = (1/λ)·ln(N₀/N) avant toute démonstration ; elle n'est établie qu'à ra_c2_demo, et seulement pour a (déjà signalé dans `physique.md`).
- ra_a3b_loi_activite → la ligne a(t) = λ·N₀·e^(−λt) = a₀·e^(−λt) n'est pas écrite (« l'activité suit la même loi ») ; Mahajar p. 7, Sbiro p. 5 et Chouvin p. 7 l'écrivent.
- ra_c2_demo → l'étape ln(a/a₀) = −λt manque à l'écran (voir « oral »).
- ra_c4b_rapport → le calcul r = (N₀ − N₀·e^(−λt)) / (N₀·e^(−λt)) = e^(λt) − 1 n'est écrit nulle part (« N₀ se simplifie ») ; l'étape 1 + r = e^(λt) n'est qu'à la voix.

#### Différences de notation ou de convention (nous / eux, laquelle garder)
- Diagramme (N, Z) : nous Z en abscisse, N en ordonnée (Nidal, Mahajar, Chriki) ; Chouvin p. 2-5 met N en abscisse et Z en ordonnée, et Sbiro p. 2 l'écrit aussi dans son texte (alors que sa figure met Z en abscisse). Garder la nôtre (décision de la fiche) ; prévenir que les isotopes sont alors sur une verticale.
- Positon : nous ⁰₁e et « positon » ; Nidal p. 39-40 et Mahajar p. 5 disent « positron », hajji p. 1 et Sbiro p. 3 écrivent ⁰₊₁e, Mahajar ⁰₁e⁺ et ⁰₋₁e⁻. Garder ⁰₁e et « positon » ; accepter les autres écritures de l'élève.
- Activité : nous a (fiche) ; Chouvin p. 6, hajji p. 2 et Chriki p. 3 (« a(t) = A(t) ») écrivent A. Garder a (A = nombre de nucléons).
- Demi-vie : nous t½ ; les professeurs écrivent t₁/₂. Garder t½.
- Seuil des noyaux lourds : professeurs A > 200 et Z > 82 (Nidal p. 38, Mahajar p. 4, Sbiro p. 3), A > 208 (Chriki p. 1) ; nous « noyaux lourds » sans seuil (décision de la fiche). Garder la nôtre.
- Datation : nous t = (1/λ)·ln(a₀/a) (comme Mahajar p. 7, hajji p. 5) ; Nidal p. 43, Chouvin p. 8 et Sbiro p. 6 écrivent t = −(1/λ)·ln(a/a₀). Garder la nôtre ; montrer une fois l'égalité des deux.
- Demi-vie définie par l'activité divisée par deux (Chouvin p. 6) ; nous par les noyaux (tous les autres). Garder la nôtre.
- λ appelée « constante de désintégration » (Mahajar p. 6) ; nous « constante radioactive ». Garder la nôtre.
- Erreurs chez les professeurs, à ne pas reprendre : Mahajar p. 6, « τ : durée nécessaire pour la désintégration de 37 % » (c'est 63 % désintégrés, 37 % restants) ; Nidal p. 39, « tous les noyaux de Z > 20 sont instables » (il veut dire les lourds) ; Mahajar p. 2 mélange Z > 20 et Z > 70.

#### Hors cadre chez les professeurs (ne pas ajouter)
- hajji p. 2-5 : unité de masse atomique u, défaut de masse, énergie de liaison, MeV, fission, fusion, bilan énergétique : chapitre « Noyaux, masse et énergie » (ch5), hors de ce chapitre.
- Chouvin p. 2 « interaction forte », p. 3 « antiparticule » : mots hors cadre de la fiche.
- Chouvin p. 5 : histogramme des comptages et moyenne n̄ = Σpᵢnᵢ/Σpᵢ (fluctuation statistique, hors cadre).
- Chouvin p. 4 : longueur d'onde du γ (10⁻⁴ nm), spectre électromagnétique ; gammagraphie (usage seulement).
- Chriki p. 3 : λ « probabilité de désintégration par unité de temps » (à ne pas développer).
- Mahajar p. 1 et Sbiro p. 1 : rayon r = r₀·A^(1/3) et masse volumique du noyau (≈ 2·10¹⁷ kg/m³) ; Chriki p. 1 « noyau 100 000 fois plus petit ». Ni le cadre ni la fiche ne le demandent ; au plus un ordre de grandeur oral (notre image du stade dans ra_n2_atome suffit).
- Sbiro p. 2 : déviation des rayons α, β, γ dans un champ électrique (la figure seulement).
- Chouvin p. 8 : équation de formation ¹⁴N + ¹n → ¹⁴C + ¹H (réaction provoquée) ; au plus une phrase, sans l'équation.
- Aucun professeur ne parle de neutrino ou d'antineutrino.

### Noyaux, masse et énergie
Notre cours audité : `backend/data/courses/phys_ch5_energie_nucleaire.json` (écran, cahier, voix, questions, réactions, rappels), relu aussi à plat (`nos-cours/phys_ch5_energie_nucleaire.txt`). Tous nos calculs ont été refaits : ils sont justes.
Sources lues : (professeur, document, pages lues en image)
- Pr Nidal Naceiri Mrabti, cours 2 BIOF (`nidal_p1.pdf`) : p. 48-60 en image (cours p. 48-55, exercices p. 56 ; p. 57-59 = pages quadrillées vides ; p. 60 = chapitre suivant).
- Auteur non indiqué (`m_…_1`) : p. 1-9 et 14-17 en image ; p. 10-13 lues en texte (décroissance radioactive = notre ch4). Pages utiles au ch5 : p. 1-4 et 14-17.
- Manuel français TS « Physique 5 » (`m_…_2`, scan) : p. 1-6 en image.
- Pr Delahi Mohamed (`m_…_3`) : p. 1-6 en image.
- Pr Asnaoui Omar, lycée Elworoud, Tinghir (`m_…_4`) : p. 1-5 en image.
- Pr Sbiro Abdelkrim (`m_…_5`) : p. 1-4 en image.
- Cadre officiel : PDF p. 8 du fichier (« Page 6 sur 29 », « 2- Noyaux - Masse et énergie ») lu en image ; JSON (notion « défaut de masse, énergie de liaison, fission, fusion, bilan énergétique ») ; fiche `cadre_reference_2bac_pc.json` → `energie_nucleaire` (EN1-EN8, hors_cadre) ; `docs/audit-programme-officiel/physique.md` ; SKILL `cours-concentration` (Physique). `experience_profs.json` n'a pas de clé `energie_nucleaire`.
- Le PDF officiel demande, en plus de ce que résume le JSON : « Connaître la relation d'équivalence masse-énergie et **calculer l'énergie de masse** », « faire le bilan énergétique ΔE en utilisant : **les énergies de masse** ; les énergies de liaisons ; le diagramme d'énergie », « **Reconnaître quelques applications de la radioactivité** », « **Connaître quelques dangers de la radioactivité** ». L'audit du 15 novembre (qui suivait le JSON) disait la notion couverte « en entier » : ces deux derniers points manquent.

#### Plan comparé
| Partie chez les professeurs | Chez nous | Remarque |
|---|---|---|
| Relation d'Einstein E = m·c², « énergie de masse » d'une particule au repos (tous) | en_m1_soleil, en_m2_einstein, en_m2b_un_gramme | Relation et unités présentes ; le nom « énergie de masse » et « au repos » manquent (0 occurrence). |
| ΔE = Δm·c² ; ΔE < 0 : le système cède de l'énergie au milieu extérieur (Nidal p. 49, Sbiro p. 1-3) | en_m2b_un_gramme, en_b2b_energie | Conforme. |
| Unités : u (1/12 de ¹²C, calcul par M/(12·N_A)), eV, MeV, MeV/c², 1 u = 931,5 MeV/c² (tous) | en_m3_unites, en_m3b_electronvolt, en_m4_931 | Calcul de 931,5 bien fait ; le calcul de 1 u = 1,66·10⁻²⁷ kg manque. |
| Défaut de masse : activité de la balance, définition, formule, Δm > 0 (tous) | en_d1_composition, en_d2_balance, en_d3_formule, en_d4_carbone | Bien fait ; la phrase de définition n'est pas au cahier. |
| Énergie de liaison : définition, E_ℓ = Δm·c² = [Z·m_p + (A − Z)·m_n − m(X)]·c², diagramme (nucléons en haut), E_ℓ > 0, nucléon isolé E_ℓ = 0 (tous) | en_l1_separer, en_l2_former, en_l3_calcul, en_e2_formule | Définition conforme ; la forme développée n'est jamais écrite. |
| Énergie de liaison par nucléon ξ = E_ℓ/A, stabilité (tous) | en_l4_par_nucleon, en_s1_stabilite, en_s2_piege | Conforme (ξ cité, piège E_ℓ/E_ℓ/A en plus). |
| Courbe d'Aston −E_ℓ/A = f(A), zone stable, fusion à gauche, fission à droite (tous) | en_a1_courbe, en_a2_zones, en_a2b_fission, en_a3_comparer | Conforme ; bornes différentes selon les professeurs (voir notations). |
| Réaction provoquée ; fission (définition, exemples, réaction en chaîne, centrale, bombe A) (tous) | en_r1_spontanee, en_r2_fission, en_r3_chaine, en_r5_soddy | Il manque l'emballement (bombe) et pourquoi un neutron. |
| Fusion (définition, répulsion, température et pression, étoiles, bombe H) (tous) | en_p3_charges, en_r4_fusion | Pas de bombe H, pas de « pression ». |
| Bilan énergétique général X₁ + X₂ → X₃ + X₄ : ΔE = [Σm(produits) − Σm(réactifs)]·c², E_lib = \|ΔE\| (tous) | en_b1_masse_diminue, en_b2_methode, en_b2b_energie, en_b3_fusion_calcul, en_b4_fission_calcul | Conforme (notation Σ). |
| Bilan par les énergies de liaison + diagramme énergétique (E_i, E_f) (Nidal p. 53, Delahi p. 6, Asnaoui p. 4-5, Sbiro p. 3-4) | en_e1_diagramme, en_e2_formule, en_e3_2023, en_e4_polonium, en_c2_qcm2019 | Lecture bien faite ; l'élève ne trace jamais le diagramme. |
| Bilans α, β⁻, β⁺ (Nidal p. 54, Sbiro p. 3-4, Delahi p. 6) | en_b5_beta (β⁻), en_n3_2025 (β⁺), en_e4_polonium et en_c2_qcm2019 (α) | Conforme. |
| Énergie d'un gramme / d'une mole / d'un kg, comparaison avec le pétrole (Nidal p. 56, manuel p. 3 et 6, auteur 1 p. 17, Asnaoui p. 5) | en_n1_echantillon, en_n1b_energie_totale, en_n2_comparaison, en_n3_2025 | Conforme. |
| Applications et dangers de la radioactivité, pouvoir de pénétration α/β/γ (Nidal p. 55, Sbiro p. 4, auteur 1 p. 5, 8-9 ; cadre) | — (ni ch5 ni ch4) | **Absent.** |
| — | en_p1_energie, en_p2_puissances, en_c1_cas_types, en_z1_bilan, en_z2_carte | Rappels et méthode du barème en plus : bien. |

#### Manques confirmés
| Priorité | Catégorie | Ce que disent les professeurs | Chez nous | Où l'ajouter |
|---|---|---|---|---|
| haute | Définition + calcul (cadre) | « Toute particule de masse m, au repos, possède une énergie E appelée **énergie de masse** E = m·c² » : Nidal p. 49 (+ application : énergie de masse du neutron, 1,5·10⁻¹⁰ J), auteur 1 p. 2 (« énergie de masse ou énergie de repos E₀ ») et p. 3 (énergie de masse du noyau d'hélium en MeV), manuel p. 1, Delahi p. 1 (exercice : énergie de masse du proton en J puis en MeV), Asnaoui p. 1 (énergie de masse d'une mole de ¹²C), Sbiro p. 1. Cadre : « calculer l'énergie de masse » ; bilan « en utilisant les énergies de masse ». | en_m2_einstein dit « toute masse m correspond à une énergie » : le nom « énergie de masse » et « au repos » n'apparaissent nulle part ; aucun calcul d'énergie de masse d'une particule ou d'un noyau. | en_m2_einstein (définition), en_m2b_un_gramme ou en_m4_931 (exercice : énergie de masse du proton ou du noyau ⁴He, en J puis en MeV), en_z1_bilan bloc 1 |
| moyenne | Notion du cadre | Nidal p. 55 : pouvoir de pénétration (α arrêté par une feuille de papier, β par une plaque d'aluminium, γ par du béton ou du plomb), dangers (cellules, cancer), applications (agriculture, industrie, centrales, médecine, datation en géologie) ; Sbiro p. 4 : rayonnements ionisants, gravité selon le type et la dose, applications médicales ; auteur 1 p. 5 (radiographie, médicaments, datation ; dangers) et p. 8-9 (α arrêté par le papier, β par quelques mm d'aluminium, γ le plus pénétrant). Cadre : « Reconnaître quelques applications de la radioactivité », « Connaître quelques dangers de la radioactivité ». | Absent du ch5 et du ch4 (aucun « danger », « pénétr », « radiothérapie »). | Nouvelle diapo après en_r3_chaine (ou avant en_c1_cas_types), qualitative ; une ligne dans en_z1_bilan |
| moyenne | Formule (tableau de formules) | E_ℓ = [Z·m_p + (A − Z)·m_n − m(ᴬ_ZX)]·c² écrite en une ligne : Delahi p. 2, Asnaoui p. 2, Sbiro p. 1 (encadrée), manuel p. 3 (encadrée). | Seulement E_ℓ = Δm·c² ; la forme développée n'est écrite nulle part (ni écran, ni cahier, ni bilan). | en_l2_former (ligne de cahier), en_z1_bilan bloc 3 |
| moyenne | Définition (rédaction) | Défaut de masse défini par une phrase : « différence entre la masse des nucléons isolés et au repos et la masse du noyau au repos » (Delahi p. 2) ; Sbiro p. 1 (« la différence est appelée défaut de masse ») ; manuel p. 3 ; Nidal p. 50 (définition par la relation). Cadre : « **Définir** et calculer le défaut de masse ». | La phrase existe dans les bullets de en_d3_formule, mais le cahier et le student_trace de en_d3 n'ont que la formule ; en_z1_bilan bloc 2 donne la propriété (« la masse d'un noyau est inférieure… ») au lieu de la définition. Le mot « au repos » manque. | Cahier de en_d3_formule ; en_z1_bilan bloc 2 |
| moyenne | Démonstration (unités) | Calcul 1 u = m(¹²C)/12 = M(¹²C)/(12·N_A) = 12·10⁻³/(12 × 6,02·10²³) = 1,66·10⁻²⁷ kg : Nidal p. 49, Delahi p. 1, Asnaoui p. 1, Sbiro p. 1, auteur 1 p. 2 (« Montrer que 1 u = 1,66·10⁻²⁷ kg »). | en_m3_unites affirme la valeur (« un douzième de la masse d'un atome de carbone 12 ») sans le calcul ni la relation avec M et N_A. | en_m3_unites (une ligne de calcul) |
| moyenne | Exercice type / méthode | « Tracer le diagramme énergétique » de la réaction : Nidal p. 56 (Ex. 1 q.4, Ex. 2 q.4) ; « dresser le schéma énergétique » : Asnaoui p. 5 (applications 1 et 2). Cadre : bilan « en utilisant … le diagramme d'énergie ». | On lit des diagrammes (en_e1_diagramme, en_e4_polonium) mais aucune question ne fait construire le diagramme ; les étapes de construction (niveau des nucléons séparés, niveau des réactifs, niveau des produits, flèches E_ℓ et ΔE) ne sont pas écrites comme une méthode. | en_e1_diagramme (méthode en 4 lignes) ; exercice dans en_e3_2023 ou en_b3_fusion_calcul |
| basse | Exemple / culture (qualitatif admis) | Réaction en chaîne non contrôlée → explosion (bombe A) ; fusion incontrôlée → bombe H : Nidal p. 53, auteur 1 p. 15-16, manuel p. 5-6, Asnaoui p. 4 (« jusqu'à une explosion »), Delahi p. 5 (bombe H). | en_r3_chaine dit seulement « dans une centrale, elle est contrôlée » ; aucune mention de l'emballement. | en_r3_chaine, en_r4_fusion (une phrase) |
| basse | Condition | Pourquoi le neutron sert de projectile : particule neutre, pas de répulsion par le noyau : Sbiro p. 2, auteur 1 p. 14 (question c). | en_r2_fission ne le dit pas (« neutre » : 0 occurrence). | en_r2_fission |
| basse | Condition | Fusion : température **et pression** très élevées (cœur des étoiles) pour vaincre la répulsion électrique : Asnaoui p. 3, auteur 1 p. 16 ; Nidal p. 53 (« grande énergie cinétique »). | en_r4_fusion : seulement « température très élevée (≈ 10⁸ K) ». | en_r4_fusion |
| basse | Sens physique | Forme de l'énergie libérée : énergie cinétique des particules produites et rayonnement γ : manuel p. 2 et p. 5 ; Asnaoui p. 4 (équations de fission avec + γ) ; auteur 1 p. 16 (chaleur et lumière du Soleil). | « De l'énergie est libérée » sans dire sous quelle forme. | en_b1_masse_diminue (une phrase, « rayonnement γ » et non « photon ») |

#### Manques chez un seul professeur
| Priorité | Catégorie | Ce que disent les professeurs | Chez nous | Où l'ajouter |
|---|---|---|---|---|
| basse | Définition | Électronvolt : énergie acquise par un électron accéléré sous une tension de 1 V (Nidal p. 49). | en_m3b_electronvolt donne la valeur seulement. | en_m3b_electronvolt (facultatif) |
| basse | Équation | Dissociation écrite : ⁷₃Li → 3 ¹₁p + 4 ¹₀n (Delahi p. 2-3). | en_l1_separer : animation, pas d'équation. | en_l1_separer |
| basse | Méthode | N = m(échantillon)/m(noyau) (manuel p. 6). | N = m·N_A/M seulement. | — (garder la nôtre) |
| basse | Ordre de grandeur | Perte de masse relative (m_av − m_ap)/m_av ≈ 2·10⁻⁵ (manuel p. 1). | Absent. | — |

#### Présent seulement à l'oral (à écrire)
- en_m4_931 et en_l3_calcul : « on garde u dans la ligne, puis on le remplace par 931,5 MeV/c², et les c² se simplifient » n'est dit qu'à la voix ; l'écran de en_l3 écrit « 0,03038 u × 931,5 MeV/u ». Nidal p. 51 et Delahi p. 3 écrivent E_ℓ = 3,038·10⁻² × 931,5 MeV/c² × c² = 28,29 MeV. Écrire cette ligne sur en_l3_calcul.
- en_a1_courbe : la forme de la courbe (« elle descend vite, puis remonte doucement ») n'est qu'à la voix.

#### Démonstrations qui sautent des étapes
- en_l2_former : E_ℓ = Δm·c² est posé (« la masse perdue devient de l'énergie ») sans le bilan des énergies de masse : E_ℓ = E(nucléons séparés) − E(noyau) = [Z·m_p + (A − Z)·m_n]·c² − m(ᴬ_ZX)·c² = Δm·c² (auteur 1 p. 3, Activité 4 ; manuel p. 3, encadré ; Delahi p. 2). C'est aussi le « bilan par les énergies de masse » du cadre.
- en_e1_diagramme / en_e2_formule : ΔE = ΣE_ℓ(réactifs) − ΣE_ℓ(produits) n'est montré qu'avec des nombres (10,841 − 28,296) ; la ligne littérale ΔE = [E_ℓ(X₁) + E_ℓ(X₂)] + [−E_ℓ(X₃) − E_ℓ(X₄)] lue sur les flèches manque (Asnaoui p. 5, Nidal p. 53).
- en_e3_2023 : « deux routes, la même réponse » est constaté (17,455 contre 17,6 MeV) sans montrer que, en remplaçant E_ℓ = Δm·c², la formule des énergies de liaison redonne [Σm(produits) − Σm(réactifs)]·c² (Sbiro p. 3).
- en_n1_echantillon : on passe de n = m/M à N = m·N_A/M sans écrire N = n·N_A.

#### Différences de notation ou de convention
| Nous | Eux | Laquelle garder |
|---|---|---|
| Δm (réaction) = Σm(produits) − Σm(réactifs) < 0 ; E_lib = \|ΔE\| | Manuel p. 1-2 : D_m = m_av − m_ap > 0 et Q = D_m·c² | La nôtre (Nidal p. 53, Delahi p. 5-6, Asnaoui p. 5, Sbiro p. 3, cadre E_lib = \|ΔE\|). |
| Zone des noyaux les plus stables 20 < A < 190 ; fusion A < 20 ; fission A > 190 | Delahi p. 3 : 20 < A < 190 ; auteur 1 p. 4 : 20 à 195 ; Nidal p. 52 et Asnaoui p. 3 : 40 < A < 195 (fusion A < 40, fission A > 195) ; manuel p. 4 : 50 < A < 75 « très stables » | La nôtre, en gardant « environ » (aucune borne au cadre). |
| « Δm (u) × 931,5 → MeV », écran « 931,5 MeV/u » | « Δm × 931,5 MeV/c² × c² » (Nidal p. 51, Delahi p. 3) | La leur dans la ligne de calcul écrite (voir « à l'oral »). |
| Diagramme : paliers sans nom | Paliers E_i (réactifs) et E_f (produits), ΔE = E_f − E_i ; Nidal p. 53 ajoute E′ (nucléons) ; Sbiro p. 3 « E.T. » | Ajouter E_i et E_f sur en_e1_diagramme (déjà « ΔE = E_f − E_i » dans une réaction de en_e4_polonium). |
| Bilan général écrit avec Σ | X₁ + X₂ → X₃ + X₄ et ΔE = [m(X₃) + m(X₄) − m(X₁) − m(X₂)]·c² (tous) | Les deux sont justes ; garder Σ, éventuellement montrer la forme à 4 noyaux une fois. |
| E_ℓ, E_ℓ/A (ξ cité) | E_l, E_L, ξ, E_ℓ/A | La nôtre. |
| « libère de l'énergie » | Nidal p. 53 « exoénergétique / endoénergétique » ; Delahi p. 6 « exothermique / endothermique » | La nôtre (exo/endothermique est dans `hors_cadre` de la fiche). |
| E = m·c² « énergie de masse » (à ajouter) | Sbiro p. 1 « énergie massique » | « énergie de masse » (cadre). |

#### Hors cadre chez les professeurs (ne pas ajouter)
- Interaction forte, forces nucléaires de cohésion (auteur 1 p. 1).
- « Neutron thermique » (Nidal p. 52), barres de contrôle (auteur 1 p. 15).
- Énergie totale E = m·c² + E_c d'une particule en mouvement (auteur 1 p. 2, manuel p. 2).
- Exo/endothermique (Delahi p. 6) ; ITER, fusion contrôlée (Delahi p. 5, manuel p. 6).
- Cycle proton-proton et évolution du Soleil (auteur 1 p. 17) ; yoctogramme (Asnaoui p. 1) ; histoire Chadwick, Joliot-Curie, Fermi (auteur 1 p. 14).
- Radioactivité, lois de Soddy, décroissance, datation, désexcitation γ détaillée (auteur 1 p. 5-13) : chapitre précédent (ch4), pas un manque du ch5.
- « Photon » (auteur 1 p. 9) : seulement dans « Atome et mécanique de Newton » ; dire « rayonnement γ ».

### Dipôle RC
Sources lues : Pr Nidal Naceiri Mrabti, cours 2 BIOF, p. 61-72 lues en image (p. 73-75 : pages quadrillées vides) ; Chriki (m_Dipole-RC_1, résumé n° 6, p. 1-4 en image) ; Delahi Mohamed (m_Dipole-RC_2, p. 1-10 en image) ; manuel TS « Physique 6 » (m_Dipole-RC_3, scan, p. 1-6 en image) ; Sbiro Abdelkrim (m_Dipole-RC_4, p. 1-6 en image). Cadre : fiche `dipole_RC` de backend/data/curriculum/cadre_reference_2bac_pc.json (RC1-RC9), JSON officiel (le PDF officiel est un scan sans texte), audit docs/audit-programme-officiel/physique.md. experience_profs.json n'a pas de clé dipole_RC. Notre cours relu en entier (texte + JSON aplati : écran, cahier, voix, questions, démonstrations, réactions).

#### Plan comparé
| Partie chez les professeurs | Où chez nous | Remarque |
|---|---|---|
| Condensateur : armatures, diélectrique, symbole (tous) | rc_c1_plaques | OK |
| Charge des armatures q_A = −q_B = q (tous) | rc_c3_electrons | OK |
| i = dq/dt, I = Q/Δt, signe de i (tous) | rc_c5_intensite, rc_c6_relation | OK |
| q = C·u_C par charge à courant constant, tableau, q = f(u) (Nidal p. 62-63, Sbiro p. 2, TS p. 2, Delahi p. 3) | rc_c4, rc_g1, rc_g2, rc_l6 | manque la condition q(0) = 0 |
| Sous-multiples du farad (tous) | rc_rp5, rc_c4 | OK |
| Associations série / parallèle, cas de n condensateurs, intérêt, exercice mixte (Nidal p. 63-65, Chriki p. 1-2, Delahi p. 4-5, Sbiro p. 3) | rc_a1, rc_a2, rc_l6 | deux condensateurs seulement, pas d'exercice mixte |
| Énergie emmagasinée (tous) | rc_l7, rc_l8 | OK (lampe au lieu du moteur) |
| Échelon montant / descendant, graphe u(t) (Nidal p. 65, Delahi p. 5-6, Sbiro p. 3/5) | rc_m1 + simulation circuit-rc.html?vue=montage | OK (graphe dans la simulation) |
| Montage, oscilloscope à mémoire, voies Y (Nidal p. 66, Delahi p. 6, TS p. 3, Sbiro p. 4) | rc_m2_acquisition | u_C seulement ; « à mémoire » absent |
| Régimes transitoire / permanent, 5τ (tous) | rc_m4, rc_s6 | OK |
| ED de la charge (u_C, q) (tous) | rc_e2, rc_e3, rc_e4, rc_e8 | OK |
| Solution A·e^(−t/τ) + B : A, B, τ (Chriki p. 2, Sbiro p. 4, Nidal p. 68) | rc_s2, rc_s3 (forme A(1 − e^(−t/τ))), rc_s4 (résumé) | la forme des professeurs n'a pas ses lignes |
| q(t), i(t), u_R(t) en charge (tous) | rc_s7, rc_s8 | i(t) non dérivé |
| ED et solution de la décharge (tous) | rc_e6, rc_d1, rc_d2 | q(t) et u_R(t) de la décharge absents |
| τ : définition, analyse dimensionnelle, influence de R et C (tous) | rc_t1, rc_t2, rc_t3 | influence montrée en charge seulement |
| Lecture de τ : tangente, 63 %, 37 % (tous) | rc_l1, rc_l2, rc_l3 | OK |
| Tableau récapitulatif charge / décharge (Delahi p. 9, Chriki p. 4) | rc_e7 (équations seulement), rc_b1 | pas de tableau des solutions et des conditions initiales |
| Exercices types (Nidal p. 72, Delahi p. 10) | rc_l4, rc_l5, rc_n1, rc_n2 | OK |

#### Manques confirmés
| Priorité | Catégorie | Ce que disent les professeurs | Chez nous | Où l'ajouter |
|---|---|---|---|---|
| haute | démonstration | i(t) se **déduit** de u_C(t) : i = C·du_C/dt = C·(E/τ)·e^(−t/τ) = (E/R)·e^(−t/τ) car τ = RC (Nidal p. 68, Chriki p. 3, TS p. 5, Sbiro p. 5) ; en décharge i = C·(−E/τ)·e^(−t/τ) = −(E/R)·e^(−t/τ) (Nidal p. 70, Chriki p. 4, Sbiro p. 6) ; cadre RC6 « en déduire i(t) » | rc_s7 : i(t) = (E/R)·e^(−t/τ) donné sans calcul (pas de demonstration.lignes) ; rc_d2 : i(t) = −(E/R)·e^(−t/τ) donné, seul i(0) est démontré | rc_s7_q_i, rc_d2_continuite |
| haute | méthode / démonstration | Forme u_C = A·e^(−t/τ) + B (ou A·e^(−mt) + B, A·e^(−αt) + B) avec toutes les lignes : dérivée −(A/τ)·e^(−t/τ), on remplace, A·e^(−t/τ)(1 − RC/τ) + B = E pour tout t ⇒ B = E et τ = RC, puis u_C(0) = 0 ⇒ A = −E (Chriki p. 2, Sbiro p. 4, Nidal p. 68) ; en décharge même forme ⇒ B = 0, puis A = E (Chriki p. 4, Sbiro p. 6, Nidal p. 69) | rc_s4 : « l'équation donne A = E et α = 1/RC », sans les lignes ; rc_d1 part directement de A·e^(−t/τ) (pas de B) | rc_s4_condition (lignes à l'écran et au cahier), rc_d1_decharge (variante avec B = 0) |
| haute | montage | Visualiser u_R (donc la forme de i) : Y₁ − Y₂ donne u_R = R·i (TS p. 3-4, doc. 8) ; cadre RC4 « brancher un oscilloscope ou un système d'acquisition pour visualiser u_C **ou u_R** » | rc_m2 : seulement u_C ; u_R n'apparaît que dans une réaction (« brancher aux bornes du conducteur ohmique permet de visualiser u_R ») | rc_m2_acquisition |
| moyenne | lois / tableau | Décharge : q(t) = C·E·e^(−t/τ) (Nidal p. 70, Delahi p. 9) ; u_R(t) = −E·e^(−t/τ) (Chriki p. 4, Delahi p. 9, Sbiro p. 6) ; conditions initiales q(0) = C·E, i(0) = −E/R (Chriki p. 4) ; tableau des solutions u_C, q, i, u_R en charge et en décharge (Delahi p. 9, Chriki p. 4) | q(t) et u_R(t) de la décharge absents de l'écran et du cahier (u_R = −E n'est que dans une réaction de rc_d2) ; rc_e7 range les équations, pas les solutions | rc_d2_continuite (deux lignes) + tableau des solutions dans rc_b1_bilan |
| moyenne | condition | q = I₀·t seulement si le condensateur est initialement déchargé : q = I₀·t + q₀ avec q(0) = 0 (Nidal p. 63, TS p. 2 : « décharger le condensateur avant l'acquisition ») | rc_g1 : « q = I₀·t » sans condition (la condition n'est que dans un énoncé d'exercice et une réaction) | rc_g1_generateur |
| moyenne | montage | Oscilloscope **à mémoire** (ou système d'acquisition), car la tension n'est pas périodique, elle ne se répète pas (Delahi p. 6, TS p. 3, Sbiro p. 4) | rc_m2 : « système d'acquisition informatisé ou oscilloscope », sans « à mémoire » ni pourquoi | rc_m2_acquisition |
| basse | loi | Cas de n condensateurs : C = C₁ + C₂ + … + Cₙ ; 1/C = 1/C₁ + … + 1/Cₙ (Chriki p. 1-2, Delahi p. 4-5, Nidal p. 63-64, Sbiro p. 3) | deux condensateurs seulement | rc_a1_parallele, rc_a2_serie |
| basse | exercice type | Capacité équivalente d'un montage mixte (série + parallèle) (Nidal p. 65, deux montages ; Delahi p. 5, exercice n° 1) | aucun exercice mixte | exercice de fin de rc_a2_serie |
| basse | définition | Intérêt du parallèle : grande charge sous une petite tension (Nidal p. 64, Delahi p. 5) ; série : C_eq plus petite que la plus petite (Chriki p. 2, Nidal p. 64) | écran « le parallèle augmente la capacité », « la série diminue » ; « plus petite que C₁ et C₂ » seulement dans la légende du visuel et les réactions | rc_a1_parallele, rc_a2_serie (cahier) |
| basse | définition | C est une grandeur positive, caractéristique du condensateur, qui ne dépend ni de la tension ni de la durée de charge (Nidal p. 63 ; Delahi p. 3 « toujours positif ») | rc_c4 : « C est la capacité » ; « constante positive » seulement dans un rappel | rc_c4_capacite |
| basse | méthode | Influence de τ (R, C) sur la **décharge** aussi (Chriki p. 4, courbes τ₁ > τ₂ ; Nidal p. 67 « durée de charge ou de décharge ») | rc_t2, rc_t3 : charge seulement | rc_t3_C (une ligne) |
| basse | ordre de grandeur | Usages et valeurs : flash d'appareil photo, allumage de voiture, mémoire (Delahi p. 3, tableau ; TS p. 1 et 6 ; Nidal p. 61) ; le cadre admet le flash (qualitatif_admis) | « flash » : 0 occurrence | rc_c1_plaques ou rc_l7_energie |

#### Manques chez un seul professeur
| Priorité | Catégorie | Ce que dit le professeur | Chez nous | Où l'ajouter |
|---|---|---|---|---|
| moyenne | démonstration | Tangente à l'origine : pente E/τ, équation u = (E/τ)·t, elle coupe u = E à t = τ (TS p. 5, doc. 13) | rc_l1 : méthode sans justification | rc_l1_tangente |
| basse | convention | Convention générateur : flèche de E dans le sens de i (Sbiro p. 4-5) | convention récepteur seulement | rc_m2_acquisition |
| basse | loi | Générateur de résistance interne r : I₀ = E/(R + r) (Nidal p. 72, exercice 2) | absent | exercice de fin de rc_l4_deduire |
| basse | rédaction | i(t) en charge par l'additivité : R·i = E − u_C = E·e^(−t/τ) (Sbiro p. 5) | absent | rc_s8_quatre (déjà u_R = E·e^(−t/τ)) |
| basse | justification | u_C continue car l'énergie ½·C·u_C² ne peut pas sauter (puissance infinie) (TS p. 6) | rc_m4 : « u_C est continue » sans « car » | rc_m4_regimes |
| basse | énergie | En décharge, l'énergie devient travail utile + chaleur par effet Joule dans R (Nidal p. 71) | rc_l7 : « il la rend » | rc_l7_energie |
| basse | définition | Montées en série : supportent une tension plus grande (Nidal p. 64) | absent | rc_a2_serie |
| basse | définition | Un condensateur débranché garde sa charge et u = E (Sbiro p. 1) | absent | rc_c2_aiguilles |
| basse | méthode | Comparer C mesurée à la valeur du fabricant (Nidal p. 62) | absent | rc_g2_pente |

#### Présent seulement à l'oral (à écrire)
- rc_d1_decharge : « l'exponentielle ne s'annule jamais, **et A n'est pas nulle** » : l'écran écrit seulement « … = 0, donc τ = RC » (le « car » manque).
- rc_t1_dimension : « montrer que RC est homogène à un temps : tu écris ces trois lignes » (phrase du bac) : seulement dans la voix.
- rc_t2_influence : R doublé (2 kΩ) ⇒ τ = 0,44 s : seulement dans la voix (l'écran a deux lignes sans nombre).
- rc_l5_pente : ordonnée à l'origine E/(RC) = 1000 V/s (sert à retrouver E) : valeur seulement dans la voix ; le cahier n'a pas l'ordonnée à l'origine.
- rc_d2_continuite : « nouvelle origine des temps t = 0 à la bascule » : écran oui, cahier non.
- rc_m4_regimes : « le condensateur se comporte comme un interrupteur ouvert » : écran oui, cahier non.

#### Démonstrations qui sautent des étapes
- rc_s7_q_i → la dérivée : i = C·du_C/dt = C·(E/τ)·e^(−t/τ) = (E/RC)·C·e^(−t/τ) = (E/R)·e^(−t/τ) (ni écran, ni voix, ni lignes de démonstration ; déjà signalé par l'audit du 15/11 pour la voix).
- rc_d2_continuite → i(t) = −(E/R)·e^(−t/τ) donné sans dériver E·e^(−t/τ) ; u_R(t) = −E·e^(−t/τ) jamais écrit.
- rc_s4_condition → « l'équation donne A = E et α = 1/RC » : manquent dérivée −αB·e^(−αt), remplacement, regroupement B·e^(−αt)(1 − RCα) + A = E pour tout t.
- rc_d1_decharge → manque la ligne −RC·(A/τ)·e^(−t/τ) + A·e^(−t/τ) = 0 avant la factorisation, et « A ≠ 0 ».
- rc_e5_uR_i → « De même avec i » : manquent u_R = R·i, R·RC·di/dt + R·i = 0, puis division par R.
- rc_l1_tangente → pourquoi la tangente coupe l'asymptote à τ (pente à l'origine E/τ) : non justifié (un seul professeur, TS p. 5).

#### Différences de notation ou de convention
| Nous | Eux | Laquelle garder |
|---|---|---|
| RC·du_C/dt + u_C = E ; du_C/dt + (1/RC)·u_C = E/(RC) | τ·du_C/dt + u_C = E (Sbiro p. 4, TS p. 5) | garder les nôtres ; citer la forme avec τ comme variante (une ligne dans rc_e3_formes) |
| u_C, q | u_AB, q_A (Delahi, TS) | garder u_C et q ; dire une fois q = q_A, u_C = u_AB |
| A + B·e^(−αt), α | λ (Delahi), m (Nidal), α (Sbiro) ; A·e^(−t/τ) + B (Chriki) | garder α et τ ; préciser « quelles que soient les lettres » (déjà dans rc_s4) |
| E_e | ℰ_e (Chriki, TS), ξ_e (Sbiro), E_C (Delahi) | garder E_e |
| I₀ = E/R = i(0) | Nidal p. 68 : « I : intensité en régime permanent » (faux, c'est à t = 0) | garder I₀ = i(0) |
| Montage de lampe pour l'énergie | moteur qui soulève une masse (Nidal p. 71, TS p. 6, Sbiro p. 6) | les deux conviennent |
Erreurs vues chez les professeurs (à ne pas copier) : Delahi p. 9 u_R(t) = E(1 − e^(−λt)) en charge (faux : E·e^(−λt)) ; Sbiro p. 6 « la tangente coupe l'asymptote u_c = E » en décharge (c'est l'axe des temps) ; Nidal p. 69 décharge « initialement déchargé » et ED de q « = CE », p. 70 q(t) = −CE·e^(−t/τ) ; Chriki p. 2 intérêt de la série écrit « en parallèle » ; Delahi p. 7 « 5τ … U_C = E » dans la décharge.

#### Hors cadre chez les professeurs (ne pas ajouter)
- Durée t½ = τ·ln 2 (TS p. 5) : non exigée ; l'audit du 15/11 demande déjà d'éviter « demi-vie » dans le RC.
- Énergie établie par intégration E_e = ∫p·dt (Sbiro p. 6) : « intégration » est dans hors_cadre ; expression admise (décision de la fiche).
- La capacité dépend de la surface, de la distance, de la nature de l'isolant (Delahi p. 3) : mène à C = ε·S/e et à la permittivité (hors_cadre).
- Activités de laboratoire du manuel TS (poussoirs P₁, P₂, carte d'acquisition détaillée) : contexte d'énoncé, pas une notion.

### Dipôle RL
Sources lues : Pr Nidal Naceiri Mrabti, cours 2 BIOF, p. 76-85 lues en image (p. 86-88 : pages quadrillées vides) ; Chriki Zakaryae (m_Dipole-RL_1, résumé n° 7, p. 1-3 en image) ; Hajji Lahoucine (m_Dipole-RL_2, diaporama, p. 1-13 en image) ; manuel TS « Physique 7 : le dipôle (R, L) » (m_Dipole-RL_3, scan, p. 1-6 en image) ; Sbiro Abdelkrim (m_Dipole-RL_4, p. 1-5 en image). Cadre : fiche `dipole_RL` de backend/data/curriculum/cadre_reference_2bac_pc.json (RL1-RL8, formules, hors_cadre), JSON officiel (« Dipôle RL (inductance, équation différentielle, retard à l'établissement du courant, énergie magnétique) » ; TP « tension aux bornes d'une bobine »), audit docs/audit-programme-officiel/physique.md. experience_profs.json n'a pas de clé dipole_RL. Notre cours relu en entier (texte + JSON aplati : écran, cahier, voix, questions, démonstrations, réactions ; simulation triangle.html).

#### Plan comparé
| Partie chez les professeurs | Où chez nous | Remarque |
|---|---|---|
| Bobine : fil enroulé, vernis, noyau de fer, symbole, L (H), r (Ω) (tous) | rl_b1_bobine | OK |
| Schéma équivalent : bobine idéale L en série avec r (Chriki p. 1, Nidal p. 77/79, TS p. 2 doc. 7) | rl_b8_reelle | absent |
| Expérience des deux lampes : retard à l'établissement (tous) | rl_b2a, rl_b2, rl_b3, rl_b4 | OK |
| Courant triangulaire (GBF + R, oscilloscope Y₁/Y₂) → u = L·di/dt (Nidal p. 78-79, Sbiro p. 1-2, Hajji p. 2-3, TS p. 1-2) | rl_b6_triangle, rl_b7_inductance, simulation triangle.html | GBF + bobine seuls : ni R, ni voies, ni signe u_Y2 = −R·i |
| u_b = L·di/dt + r·i, convention récepteur, cas r = 0, régime permanent u_b = r·I (tous) | rl_b8, rl_b3, rl_b10 | OK |
| Surtension : di/dt grand → u_b grande ; étincelle, diode (tous) ; bougie, lampe au néon (Nidal p. 76/79, TS p. 2) | rl_t3_diode, rl_t4_national | applications absentes |
| Montage échelon, visualiser i par u_R = R·i, acquisition (tous) | rl_m1_montage | « acquisition » absent |
| Régimes transitoire / permanent, I₀ = E/(R + r), 5τ (tous) | rl_m2, rl_m3, rl_m4, rl_s6 | OK (5τ à l'établissement seulement) |
| ED en i à l'établissement, formes avec R_T et τ (tous) | rl_e1 à rl_e4, rl_e7 | OK |
| ED en u_R à l'établissement (Nidal p. 81, Chriki p. 2) | rl_e5_uR | OK |
| Solution A·e^(−αt) + B : B et α par l'ED, A par la condition initiale (Chriki p. 2, Hajji p. 6, Sbiro p. 3, Nidal p. 82) | rl_s1 à rl_s4 (forme A(1 − e^(−t/τ))) | la forme des professeurs n'apparaît pas ; pas de « condition initiale » |
| u_R(t) à l'établissement (Nidal p. 82, Chriki p. 3) | rien (seulement u_R = R·i) | absent |
| u_b(t) à l'établissement, r ≠ 0 (Nidal p. 82, Sbiro p. 4, Chriki p. 3, Hajji p. 7) | rl_l6_ub (bobine idéale seulement, sans calcul) | absent pour r ≠ 0 |
| τ : définition, analyse dimensionnelle, influence de L et R (tous) | rl_s5, rl_s7, rl_s8 | OK |
| Lecture de τ : tangente, 63 %, 37 % (tous) | rl_l1, rl_l2, rl_t2 | OK |
| Rupture : ED en i, solution vérifiée, A par i(0) = I₀ (Nidal p. 83, Hajji p. 7-8, Sbiro p. 4-5, Chriki p. 3) | rl_t1 (ED), rl_t2 (solution donnée) | solution non vérifiée |
| Rupture : ED en u_R, u_R(t) (Nidal p. 83-84) | rl_t2 (u_R(t) seulement) | ED en u_R absente |
| Énergie E_m = ½·L·i², unités (tous) ; mise en évidence par un moteur (TS p. 6, Sbiro p. 5) | rl_l7, rl_l8 | moteur absent |
| Exercices types (Nidal p. 85 ; Hajji p. 12-13) | rl_b9, rl_b10, rl_e7, rl_e8, rl_n1, rl_n2, rl_t4 | OK |

#### Manques confirmés
| Priorité | Catégorie | Ce que disent les professeurs | Chez nous | Où l'ajouter |
|---|---|---|---|---|
| haute | démonstration | Rupture : on vérifie la solution : i = A·e^(−αt) + B, di/dt = −αA·e^(−αt), on remplace dans τ·di/dt + i = 0 ⇒ B = 0 et α = 1/τ ; puis la condition initiale i(0) = E/R_T ⇒ A = E/R_T (Nidal p. 83, Hajji p. 8, Sbiro p. 5 ; Chriki p. 3 donne la condition i(0) = I₀) ; cadre RL5 « vérifier qu'une expression est solution… et déterminer ses constantes » | rl_t2 : « Solution : i(t) = I₀·e^(−t/τ) » donnée, sans dérivée ni remplacement (écran, cahier, voix) | rl_t2_descente (lignes de démonstration) |
| haute | méthode / démonstration | Forme i(t) = A·e^(−αt) + B (ou A + B·e^(kt), A·e^(−mt) + B) : B = E/R_T et α = 1/τ par l'ED « pour tout t », puis A = −E/R_T par la **condition initiale** i(0) = 0 (Chriki p. 2, Hajji p. 6, Sbiro p. 3, Nidal p. 82) ; cadre RL5 « déterminer A, B, τ avec l'équation et la condition initiale » ; variante admise « i(t) = A + B·e^(−t/τ) » | rl_s1 impose A(1 − e^(−t/τ)) : i(0) = 0 est une conséquence de la forme, jamais une condition initiale qu'on utilise ; la forme A + B·e^(−t/τ) n'apparaît nulle part | rl_s4_A (variante en lignes) ou nouvelle diapo après rl_s4 |
| haute | loi / démonstration | u_b(t) pour r ≠ 0 : u_b = E − R·i = E − (R·E/(R + r))(1 − e^(−t/τ)) = r·E/(R + r) + (R·E/(R + r))·e^(−t/τ) ; à t = 0 u_b = E, quand t → ∞ u_b = r·I₀ (Nidal p. 82, Sbiro p. 4, Chriki p. 3, Hajji p. 7) ; cadre RL5 « écrire i(t), u_R(t), u_b(t) » | rl_l6 : seulement « bobine idéale : u_b(t) = E·e^(−t/τ) », sans calcul ; rien pour r ≠ 0 | rl_l6_ub (ou rl_e6_ub) |
| haute | loi | u_R(t) à l'établissement : u_R = R·i = (R·E/(R + r))(1 − e^(−t/τ)) = U(1 − e^(−t/τ)) (Nidal p. 82 ; Chriki p. 3 tableau « U_R(t) = R·i(t) ») ; cadre RL5 « écrire u_R(t) » | jamais écrit (seulement u_R = R·i et U_R = R·E/(R + r) en régime permanent, rl_e8) ; la rupture a u_R(t) (rl_t2) | rl_s4_A (une ligne) ou rl_l2_pourcent |
| moyenne | montage / méthode | TP « tension aux bornes d'une bobine » : GBF, bobine **et conducteur ohmique R**, masse commune ; voie Y₂ = u_R donne i ; à cause de la masse u_Y2 = −u_R = −R·i, donc i = −u_Y2/R ; lire les sensibilités, i = a·t + b, L = u_L/(di/dt) (Nidal p. 78-79, Sbiro p. 1-2, Hajji p. 2-3, TS p. 1-2 doc. 4-5) ; cadre : TP officiel | rl_b6 : « un GBF impose dans une bobine… un courant en triangle » ; la simulation triangle.html ne dessine ni R ni oscilloscope | rl_b6_triangle (+ figure), rl_b7_inductance |
| moyenne | définition / schéma | Schéma équivalent : bobine (L, r) = bobine idéale L en série avec un conducteur ohmique r, d'où u_b = L·di/dt + r·i par additivité (Chriki p. 1, Nidal p. 77 et 79, TS p. 2 doc. 7) | « schéma équivalent » : 0 occurrence ; rl_b8 « on admet » sans ce schéma | rl_b8_reelle |
| moyenne | équation | Rupture : ED vérifiée par u_R : u_R + (L/R_T)·du_R/dt = 0 (Nidal p. 83) ; cadre RL4 « équation vérifiée par i ou u_R à l'établissement **et à la rupture** », variante admise (L/(R + r))·du_R/dt + u_R = 0 | rl_t1 : ED en i seulement | rl_t1_rupture (une ligne) |
| basse | ordre de grandeur / application | Surtension utilisée : étincelle de la bougie (allumage d'un moteur à essence), lampe au néon allumée par une pile de 6 V (Nidal p. 76 et 79, TS p. 2 doc. 8) | « néon », « bougie », « allumage » : 0 occurrence | rl_t3_diode |
| basse | méthode | Rupture : régime permanent (i = 0) pratiquement atteint à 5τ (Nidal p. 80-81, Hajji p. 5 et 9, courbes jusqu'à 5τ) | 5τ seulement à l'établissement (rl_s6) | rl_t2_descente |
| basse | montage | Visualiser i avec un oscilloscope numérique **ou un système d'acquisition** (Nidal p. 80 et 85, TS p. 3) ; cadre RL3 « oscilloscope ou acquisition informatisée » | « acquisition » : 0 occurrence ; rl_m1 « oscilloscope » | rl_m1_montage |
| basse | énergie | Mise en évidence : à l'ouverture, la bobine fait tourner un moteur qui soulève une masse (TS p. 6, Sbiro p. 5) | rl_l7 : énergie rendue en chaleur (effet Joule) seulement | rl_l7_energie |
| basse | loi | Rupture : u_b(t) = E·e^(−t/τ)·(r/R_T − 1), bobine idéale u_b = −E·e^(−t/τ) (Hajji p. 10) ; u_L final = 0 (Nidal p. 81) ; cadre RL5 « écrire u_b(t) » | rien sur u_b à la rupture (sauf la surtension −R₁·I₀ de rl_t4) | rl_t2_descente |

#### Manques chez un seul professeur
| Priorité | Catégorie | Ce que dit le professeur | Chez nous | Où l'ajouter |
|---|---|---|---|---|
| moyenne | démonstration | Tangente à l'origine : (di/dt)₀ = I_p/τ, donc elle coupe l'asymptote à t = τ (TS p. 5) | rl_l1 : méthode sans justification (rl_l5 donne E/L sans le lien I₀/τ) | rl_l1_tangente |
| moyenne | démonstration | Identification : « avec A ≠ 0 » (Sbiro p. 3 et 5) | rl_s3 : seulement « l'exponentielle ne s'annule jamais » | rl_s3_tau |
| basse | méthode | Influence de E : I_p change, τ ne change pas (TS p. 4, doc. 13) | absent (L et R seulement) | rl_s7_L ou rl_s8_R |
| basse | justification | i continue car E_m = ½·L·i² ne peut pas sauter (puissance infinie) (TS p. 6) | rl_b5 : « i est continue » sans « car » | rl_b5_continuite |
| basse | ordre de grandeur | Tableau des inductances : 10⁻⁶ H à 100 H ; noyau de fer ×1000 (TS p. 2 doc. 6) | absent (valeurs 2 mH à 0,5 H dans les exercices) | rl_b1_bobine |
| basse | méthode | r par la droite u_L = f(I) en régime permanent (pente r) (Nidal p. 78-79) | r à l'ohmmètre ou r = u_b/I₀ | rl_b10_national |
| basse | rédaction | Tableau t = 0 / régime permanent / r = 0 pour i, u_R, u_L, additivité, ED (Chriki p. 3) | rl_e6 (en lignes) | rl_bl_fiche |
| basse | énergie | E_m = L·u_R²/(2R²) (Nidal p. 84) ; instant où E_m = 60 % de sa valeur initiale (Nidal p. 85, ex. 2) | absent | exercice de fin de rl_l8_double |
| basse | méthode | t_1/2 = τ·ln 2 (i = 0,5·I_p) (TS p. 4) | absent | non nécessaire |

#### Présent seulement à l'oral (à écrire)
- rl_e6_ub : « u_b saute à E. **Pourquoi ? i est petite, mais sa pente est très grande** » : le « car » (di/dt grand) n'est que dans la voix.
- rl_b1_bobine : « r, la résistance du fil, en ohm, **car le fil est long** » : seulement dans la voix.
- rl_s1_forme : « **Après cinq tau, i a presque atteint A** » : voix ; l'écran de rl_s1 n'en parle pas (5τ est écrit plus loin, rl_s6).
- rl_s5_dimension : « elle est au programme : **sache écrire ces trois lignes** » (phrase de rédaction du bac) : seulement dans la voix.
- rl_t3_diode : « à cet instant, **u_b devient grande et négative** » : voix ; écrit seulement dans rl_t4.

#### Démonstrations qui sautent des étapes
- rl_t2_descente → toute la vérification : di/dt = −(I₀/τ)·e^(−t/τ) ; L·(−I₀/τ)·e^(−t/τ) + (R + r)·I₀·e^(−t/τ) = 0 ⇒ τ = L/(R + r) ; puis i(0) = I₀ (continuité) ⇒ A = I₀.
- rl_s1_forme / rl_s4_A → la constante liée à i(0) n'est jamais trouvée par la condition initiale (la forme A(1 − e^(−t/τ)) la contient déjà) ; manque la version A + B·e^(−t/τ) avec B = −A tiré de i(0) = 0.
- rl_s3_tau → « A ≠ 0 » manque avant « L/τ − (R + r) = 0 » (écran, cahier et voix).
- rl_l6_ub → u_b(t) = E·e^(−t/τ) donné sans les lignes u_b = E − R·i = E − R·I₀(1 − e^(−t/τ)) et R·I₀ = E (r = 0).
- rl_l1_tangente → pourquoi la tangente coupe l'asymptote à τ : pente à l'origine I₀/τ = E/L (un seul professeur, TS p. 5).

#### Différences de notation ou de convention
| Nous | Eux | Laquelle garder |
|---|---|---|
| R + r | R_T (Nidal, Sbiro), R_t (Chriki) ; R = R′ + r avec R′ le conducteur ohmique (Hajji, TS) | garder R + r ; dire une fois « R_T = R + r, résistance totale » (rl_e3) |
| u_b (u_L, u_B annoncés) | u_L (Chriki, Nidal, Sbiro), u_AB (Hajji, TS) | garder u_b ; ajouter u_AB aux variantes |
| L·di/dt + (R + r)·i = E ; di/dt + ((R + r)/L)·i = E/L | τ·di/dt + i = E/R_T (Chriki p. 2, Sbiro p. 3), I_p = τ·di/dt + i (TS p. 5), i + (L/R_T)·di/dt = E/R_T (Nidal p. 81) | garder les nôtres ; écrire en toutes lettres τ·di/dt + i = I₀ dans rl_e4 (aujourd'hui seulement « L/(R + r) = τ ») |
| i = A(1 − e^(−t/τ)) | A·e^(−αt) + B (Chriki, Sbiro), A + B·e^(kt) (Hajji), A·e^(−mt) + B (Nidal) | garder la nôtre et ajouter la forme générale (manque haute) |
| I₀ (I_p annoncé) | I_p (TS), I_m / I_max (Nidal p. 80, 84), E/R_T | garder I₀ |
| Rupture par K en position 2 | ouverture de K avec diode en parallèle (Chriki, Hajji, Sbiro, TS) ; Nidal : position 2 et diode | les deux conviennent (rl_t3/rl_t4 traitent la diode) |
| E_m | ℰ_m (Chriki), E_B (Hajji) | garder E_m |
Erreurs vues chez les professeurs (à ne pas copier) : Hajji p. 3 « L… appelé conductance » (inductance) ; Hajji p. 6 « k = τ = −R/L » (k = −1/τ) ; Hajji p. 7 u_L = E(1 − (1 + e^(−t/τ))) (signe) ; Nidal p. 77 « cette résistance augmente avec un noyau de fer » (c'est L) ; Nidal p. 81 « régime permanent… lorsque t < 5τ » (t > 5τ) ; Nidal p. 84 i = I_m(1 − e^(−τ·t)) (e^(−t/τ)) ; Chriki p. 2 asymptote « I₀ = E/R » (E/R_t) et p. 3 « on obtient R = r » ; Sbiro p. 4 asymptote « u_c = E/R_T » (i).

#### Hors cadre chez les professeurs (ne pas ajouter)
- Bobine plate, solénoïde, solénoïde infini selon ℓ et le rayon (Hajji p. 1) ; L dépend de la section, de la longueur, du nombre de spires et du milieu (Sbiro p. 1) : perméabilité hors cadre (le noyau de fer en qualitatif suffit).
- Démonstration de E_m = ½·L·i² par la puissance (Sbiro p. 5) ou par l'intégrale ∫L·i·di (TS p. 6, doc. 17) : le cadre dit « expression admise » (RL8).
- t_1/2 = τ·ln 2 (TS p. 4) : non exigé.
- Les documents Chriki (« SM PC SVT ») et TS (programme français) ne contiennent rien de propre à la série SM ; aucun ne cite la loi de Lenz ou de Faraday.

### Oscillations libres d’un circuit RLC série
Sources lues : Pr Nidal Naceiri Mrabti, cours 2 BIOF (nidal_p1.pdf), p. 89-95 lues en image (p. 96-98 : pages sans texte, 2 mots chacune) ; Pr Sbiro Abdelkrim, « Oscillations libres dans un dipole RLC en série » (pc1.ma, dépôt), p. 1-5 lues en image. Pas de document moutamadris pour ce chapitre. Cadre : fiche `circuit_RLC` de backend/data/curriculum/cadre_reference_2bac_pc.json (RLC1-RLC8, formules, hors_cadre), JSON officiel (notion « Circuit RLC série (amortissement, régimes…, oscillations libres, entretien) »), docs/audit-programme-officiel/physique.md. experience_profs.json n’a pas de clé circuit_RLC. Notre cours relu en entier (texte écran / cahier / voix) et JSON cherché (questions, réponses, rappels, séances).

#### Plan comparé
| Partie chez les professeurs | Où chez nous | Remarque |
|---|---|---|
| Montage à deux positions, oscilloscope (Nidal p. 90, Sbiro p. 1 voie Y₁) | lc_d1_rc, lc_d2_bobine (simulation ?vue=bascule) | OK |
| Oscillations libres amorties, « oscillateur libre et amorti » ; seule énergie = celle du condensateur (Nidal p. 90, Sbiro p. 1) | lc_d4_libres | mot « amorties » absent de l’écran ; l’idée d’énergie seulement à l’oral |
| Trois régimes, T₀ et T ≈ T₀ (Nidal p. 90, Sbiro p. 1) | lc_r1 → lc_r4, lc_l2_voisine | OK |
| ED en u_C puis en q, R_T = R + r (Nidal p. 91, Sbiro p. 2) | lc_e1 → lc_e4 | OK |
| ED du LC idéal (Nidal p. 91, Sbiro p. 2) | lc_e5_lc_ideal | OK |
| Solution u_C = U_m·cos(2πt/T₀ + φ), unités de U_m, φ, T₀ (Nidal p. 92, Sbiro p. 2) | lc_e6_sinusoide | unités absentes (φ en rad) |
| Vérification et T₀ = 2π√(LC) (Nidal p. 92, Sbiro p. 2) | lc_rp4, lc_e7, lc_e8 | OK |
| Dimension de T₀ (Nidal p. 92, Sbiro p. 3) | lc_p1_unites | OK |
| Conditions initiales U_m, φ (Nidal p. 92, Sbiro p. 3) | lc_c1 → lc_c4 | OK (raisonnement différent, voir démonstrations) |
| q(t) = Q_m·cos(2πt/T₀), Q_m = C·E (Nidal p. 93, Sbiro p. 3) | — | **absent** |
| i(t) = I_m·cos(2πt/T₀ + π/2), I_m = (2π/T₀)·Q_m = E·√(C/L) (Nidal p. 93, Sbiro p. 3) | lc_c4 (exercice), lc_n1 (i donnée), lc_en3 (I_m par l’énergie) | expression de i(t) jamais établie ; formule de I_m absente |
| Énergie du LC, courbes E_e, E_m, E_t, conservation démontrée (Nidal p. 93, Sbiro p. 3-4) | lc_en1 → lc_en4 | conservation vue sur la courbe ; démonstration seulement en lc_a3 (cas général) |
| Période de l’échange d’énergie = T₀/2 (Sbiro p. 4 ; Nidal p. 95 ex. 2) | lc_en3 « deux fois par période » | T₀/2 seulement dans une réponse de lc_en4 |
| Énergie du RLC, dE/dt = −R_T·i², courbes (Nidal p. 94, Sbiro p. 5) | lc_a1 → lc_a5 | OK |
| Entretien u_G = k·i, k = R_T, « se comporte comme un LC » (Nidal p. 94, Sbiro p. 5) | lc_k1 → lc_k3 | OK |
| Exercices (Nidal p. 95) | lc_r4, lc_p4, lc_l4, lc_n1, lc_n2 | OK |

#### Manques confirmés
| Priorité | Catégorie | Ce que disent les professeurs | Chez nous | Où l’ajouter |
|---|---|---|---|---|
| haute | relation / loi | q(t) = C·u_C(t) = Q_m·cos(2πt/T₀ + φ), avec Q_m = C·U_m (= C·E) : Nidal p. 93, Sbiro p. 3 ; cadre RLC4 (« ou q = Q_m·cos(2πt/T₀ + φ) ») | aucune expression de q(t), pas de Q_m (cherché : Q_m, q_m, q(t) =) | nouvelle diapo après lc_c1_depart (+ lc_bl_fiche) |
| haute | relation + démonstration | i(t) = dq/dt = −(2π/T₀)·Q_m·sin(2πt/T₀) = I_m·cos(2πt/T₀ + π/2), I_m = (2π/T₀)·Q_m = E·√(C/L) : Nidal p. 93, Sbiro p. 3 ; cadre RLC6 (variante I_m = U_m·√(C/L)) | i(t) = I_m·cos(…) seulement donné dans des exercices (lc_c4, lc_n1) ; I_m tiré de l’énergie en lc_en3 (≈ 38 mA), sans formule | même nouvelle diapo après lc_c1_depart ; renvoi dans lc_en3_echange |
| moyenne | relation | Période de l’échange d’énergie = T₀/2 : Sbiro p. 4 (« égale à la moitié de la période propre ») ; Nidal p. 95 ex. 2 (E_m = (CU²/4)(1 − cos(4πt/T₀))) | écran/cahier : « E_e est maximale deux fois par période » ; T₀/2 seulement dans reponses_fin_de_cours de lc_en4 et en graduation de figure | lc_en3_echange (écran + cahier) |
| moyenne | définition / vocabulaire | « oscillations libres amorties » (RLC), « non amorties » (LC idéal), « oscillateur électrique libre et amorti » : Nidal p. 90, Sbiro p. 1 ; mot-clé du cadre « amortissement » | lc_d4 : « oscillations électriques libres » ; « amorties » seulement en lc_k3 et dans des réponses | lc_d4_libres, lc_r1_pseudo, lc_e5_lc_ideal |
| basse | unités | U_m en V, φ en rad, T₀ en s, donnés avec la solution : Nidal p. 92, Sbiro p. 2 | lc_e6 : pas d’unité pour φ (rad apparaît en lc_c4) ; T₀ en s en lc_e8 | lc_e6_sinusoide (cahier) |

#### Manques chez un seul professeur
| Priorité | Catégorie | Ce que dit le professeur | Chez nous | Où l’ajouter |
|---|---|---|---|---|
| basse | tableau | Tableau q et i à t = 0, T₀/4, T₀/2, 3T₀/4, T₀ et graphe q(t), i(t) : « quand l’une est maximale, l’autre s’annule » (Sbiro p. 3) | idée présente (lc_d3, lc_d5, lc_en3), pas de tableau | avec la diapo q(t)/i(t) proposée |
| basse | démonstration | ED du LC établie par l’énergie : dE/dt = 0 ⇒ i·(u_C + L·di/dt) = 0 ⇒ ED (Sbiro p. 4) | absent | exercice de lc_en4_somme |
| basse | remarque | Le LC idéal est difficile à réaliser : toute bobine a une résistance (Sbiro p. 2) | lc_e5 : « imagine un circuit sans résistance » | lc_e5_lc_ideal |
| basse | exercice type | E_m(t) = (C·U²/4)·(1 − cos(4πt/T₀)) avec sin²x = (1 − cos 2x)/2, puis C et L par la courbe (Nidal p. 95 ex. 2) | absent | exercice de lc_en3_echange |

#### Présent seulement à l’oral (à écrire)
- lc_d4_libres : « le condensateur et la bobine échangent seuls l’énergie du départ » (la seule source d’énergie est l’énergie stockée dans le condensateur — Nidal p. 90) : écran/cahier disent seulement « sans générateur ».
- lc_k2_k : « le terme du milieu, c’est lui qui vide l’énergie » (terme en dq/dt = terme d’amortissement — Sbiro p. 2) : à écrire aussi en lc_e5_lc_ideal.
- lc_en3_echange : I_m tiré de E = ½·L·I_m² (I_m = √(2E/L)) : seul le résultat 38 mA est écrit.

#### Démonstrations qui sautent des étapes
- lc_c1_depart : φ = 0 tiré de « u_C(0) = U_m·cos φ = E est la plus grande valeur possible » ; i(0) = 0 est dit mais pas utilisé. Nidal p. 92 écrit le système U_m·cos φ = E et −(2π/T₀)·U_m·sin φ = 0 ⇒ sin φ = 0 ⇒ φ = 0 ou π ; cos φ > 0 (E > 0) ⇒ φ = 0, U_m = E. À ajouter (marche sans lire la courbe).
- lc_k2_k : « on remplace » saute la ligne q/C + (R + r)·i + L·di/dt = k·i ⇒ q/C + (R + r − k)·i + L·di/dt = 0 (écrite par Nidal p. 94 et Sbiro p. 5).
- lc_en4_somme : la conservation de E dans le LC est montrée seulement par la courbe ; Nidal p. 93 (dE/dt = 0) et Sbiro p. 4 (cos² + sin² = 1) la démontrent. Notre preuve n’existe qu’en lc_a3 (cas R + r = 0) : ajouter un renvoi ou la ligne dE/dt = i·(u_C + L·di/dt) = 0.
- lc_c1_depart → q(t), i(t) : la dérivation i = dq/dt = −(2π/T₀)·Q_m·sin(…) = I_m·cos(… + π/2) (avec −sin α = cos(α + π/2)) n’existe pas (voir manques).

#### Différences de notation ou de convention
| Nous | Eux | Garder |
|---|---|---|
| R + r | R_T = R + r (Nidal p. 91), R_t (Sbiro p. 2) | R + r ; dire une fois « on note aussi R_T » |
| u_b | u_L (Nidal, Sbiro) | u_b, avec la mention u_L déjà en lc_e2 |
| E, E_e, E_m (E_t cité en lc_en2) | E_t, E_e, E_m (Nidal) ; ξ_t, ξ_e, ξ_m (Sbiro) | les nôtres |
| u_G = k·i | u_g = K·i (Nidal p. 94) ; u_g = R₀·i (Sbiro p. 5) | u_G = k·i (nationaux, cadre) |
| T ≈ T₀ (admis) | T ≈ T₀ (Nidal) ; T = T₀ (Sbiro p. 1) | T ≈ T₀ |
| φ en rad | φ « en (s) » (Nidal p. 92, erreur) | rad |
| E_m = ½·L·i² ; E = ½·C·u_C² + ½·L·i² | Nidal p. 93-94 : « E_e = ½·L·i² » et « E_t = ½·C·u_C² + L·i² » (coquilles) | les nôtres |

#### Hors cadre chez les professeurs (ne pas ajouter)
- Sbiro p. 1 : régimes sous-critique, critique, surcritique (cadre : trois régimes seulement).
- Sbiro p. 5 : montage à amplificateur opérationnel, « résistance négative », u_g = R₀·i (écrire u_G = k·i).
- Sbiro p. 3 : « q et i sont en quadrature de phase » (« déphasage » est dans hors_cadre) : garder seulement « quand l’une est maximale, l’autre s’annule ».
