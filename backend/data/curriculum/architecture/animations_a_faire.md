# Animations à faire : les activités encore écrites en tableau et en encadrés

Règle de l'utilisateur, 18 novembre 2026 (skill `professeur`, règle 42 ; `logique-de-cours`, règle 5) : une **activité dont
le résultat change** (dans le temps, d'un compartiment à l'autre, avant / après un ajout, avec / sans un facteur, cas
après cas) se joue au tableau en **animation réaliste**. Elle ne s'écrit pas en tableau de résultats suivi d'encadrés de
conclusion. Ce qui bouge se voit bouger. Chaque temps ou cas est un moment (`play_until`) arrêté. Le cas décisif est posé
en question avant sa conclusion. Le tableau, si le bac en a besoin, vient en dernier, rempli par l'animation (règle 35).
La vérification se fait au téléphone en paysage (~724 × 350 px CSS ; l'iframe y fait ~577 × 255).

Modèle fait le 18/11 : `svt/reactions_responsables_liberation_energie-tableau/glucose-marque.html` sur
`le_m3a_glucose_marque` (SVT ch1). On y trouve : une cellule peinte, les molécules ¹⁴C qui brillent dans leur forme du cours,
une horloge T0 → T4 et un compteur par compartiment. La conclusion attend la question d'observation (`sim_avant` /
`sim_apres` `{conclusions}`). Le tableau final est rempli par l'animation. Une vue compacte prend le relais quand la bande
de la question écrase la figure.

Inventaire du 18/11/2026 sur les 23 cours (`backend/data/courses/*.json` qui ont une copie dans `en_attente/`, en ligne et
en attente). Critères : un `screen_content.table` de résultats, ou au moins trois encadrés `concentration.centre` de
résultats et de conclusions, sur une diapositive sans simulation au tableau.

Pour chaque diapositive, quand on la fera : garder `speech_text` (et sa voix) si possible. Recaler seulement le `pointage`
sur les mots déjà dits. Retirer de `screen_content` et de `centre` ce que l'animation montre. Respecter la règle 15 des
simulations (un objet, un seul dessin : les formes du lexique visuel). Faire les deux fichiers (en ligne et en attente).

## À faire (par ordre de priorité)

| # | Cours | Diapositive | Aujourd'hui | Animation à faire |
|---|-------|-------------|-------------|-------------------|
| 1 | SVT ch2 muscle | `ms_c2a_calcium_libere` — L'excitation libère le Ca²⁺ | tableau lot 1 / lot 2 × réticulum / sarcoplasme (« radioactivité forte / faible ») + 5 encadrés | Même genre que le glucose marqué. Une fibre peinte coupée (réticulum sarcoplasmique en sacs autour des myofibrilles, sarcoplasme). Des ions ⁴⁵Ca²⁺ qui brillent, et un compteur de radioactivité par compartiment. Moment `lot1_relache` : le Ca²⁺ est dans le réticulum (fort / faible). Moment `excitation` : un influx arrive. Moment `lot2_contracte` : le Ca²⁺ sort dans le sarcoplasme (faible / fort), arrêt avant la conclusion, question « où est passé le calcium ? ». Puis la conclusion. Puis l'équorine qui s'éclaire. Tableau à la fin. Une nouvelle vue `?vue=radioactif` de `role_muscle_strie_squelettique-tableau/calcium.html` garde le même dessin de la fibre. |
| 2 | SVT ch4 gène-protéine | `rg_a5_in_vitro` — Synthèse in vitro : sans ARNm, pas de protéine | tableau de 3 périodes (avant / après 1ʳᵉ / après 2ᵉ injection) | Un tube peint (extrait : ribosomes, ARNt, ATP) et des acides aminés radioactifs qui brillent. Deux courbes tracées dans le temps : l'ARNm dans le milieu, et les acides aminés incorporés. Moments : `avant_injection` (rien ne s'incorpore), `injection_1` (l'ARNm baisse, les protéines montent), `injection_2` (même chose). La question « que faut-il pour fabriquer une protéine ? » vient avant la conclusion. Nouvelle vue de `relation_gene_proteine-tableau/marquage.html` (mêmes acides aminés que `?vue=acides_amines`). |
| 3 | SVT ch4 gène-protéine | `rg_p5_beadle_tatum` — Beadle et Tatum : un gène, une enzyme | tableau souches × milieux (+ / −) + 3 encadrés | Quatre tubes (ou boîtes) peints par souche : sauvage, mutant 1, mutant 2, mutant 3. Pour chaque milieu (MM, + ornithine, + citrulline, + arginine), le champignon pousse ou non (un mycélium qui s'étend). Au-dessus, la chaîne précurseur → ornithine → citrulline → arginine, avec l'enzyme bloquée barrée. Un mutant par moment. Le mutant 2 est posé en question (« quelle enzyme manque ? ») avant sa réponse. Le tableau + / − se remplit à la fin. Nouveau `relation_gene_proteine-tableau/beadle_tatum.html`. |
| 4 | SVT ch2 muscle | `ms_c1c_myofibrille` — Myofibrille isolée : deux inhibiteurs | 7 encadrés (avant T₁, T₁, T₂ salyrgan, T₂ chélateur) | Une myofibrille peinte reliée à un capteur, et la courbe de tension tracée dans le temps. T₁ : ajout de Ca²⁺ + ATP, la myofibrille se raccourcit et la tension monte. T₂ : deux variantes, salyrgan (l'ATP n'est plus hydrolysé) ou chélateur (le Ca²⁺ est fixé), la tension retombe. Chaque ajout est une seringue et un moment. La question « pourquoi la tension retombe ? » vient avant la conclusion. À voir : une vue de `role_muscle_strie_squelettique-tableau/inhibiteurs.html` ou de `myographe.html`, avec le même dessin de la myofibrille que `sarcomere.html`. |
| 5 | SVT ch1 énergie | `le_e3b_masse_levures` — Avec ou sans dioxygène : combien de levures ? | tableau 3 critères × avec / sans O₂ + 8 encadrés | Deux fioles peintes côte à côte (aérobiose / anaérobiose), du même dessin que les levures de `fermentations.html`. Le glucose consommé descend (150 g / 45 g) et les levures bourgeonnent (1,970 g / 0,255 g), avec un compteur sous chaque fiole. Le test à l'éthanol est positif seulement sans O₂. Puis le calcul « levures par gramme de glucose » écrit à la craie (fraction, règle 12). La question « laquelle libère le plus d'énergie ? » vient avant la conclusion. Le tableau à la fin. |
| 6 | SVT ch2 muscle | `ms_t4a_sang` — Le sang qui entre et qui sort du muscle (Chauveau et Kaufmann) | tableau 6 lignes repos / activité + 6 encadrés | Un muscle peint (cheval) avec son artère et sa veine. Le débit de sang se voit (des globules qui défilent plus vite en activité). Des compteurs à l'entrée et à la sortie : O₂ consommé, CO₂ rejeté, glucose prélevé, lipides et protides à 0. Moments `repos` et `activite`. Les rapports (× 4,6, × 17, × 27) sont écrits sur leur moment. La question « quel métabolite le muscle consomme-t-il ? » vient avant la conclusion. Le tableau à la fin. Même dessin du muscle que `chaleur.html` / `consommation.html`. |
| 7 | SVT ch2 muscle | `ms_r6b_intensite` — Un effort de plus en plus intense | tableau 5 lignes (intensité, O₂, acide lactique) + 6 encadrés | Un coureur ou un cycliste, avec un curseur « intensité » (règle 28). Deux jauges ou deux courbes en fonction de l'intensité : l'O₂ monte puis plafonne à 3,04 L/min, et l'acide lactique, à l'état de traces, s'envole après 68 kJ/min. Moments : `faible`, `seuil`, `intense`. La question « que se passe-t-il quand l'O₂ ne monte plus ? » vient avant la conclusion (la fermentation s'ajoute). Les valeurs du tableau sont produites par l'animation. |
| 8 | SVT ch3 information génétique | `ig_n1b_feulgen` — Le chromosome contient de l'ADN : la preuve | 5 encadrés (Feulgen, puis histones retirées) | Deux expériences jouées l'une après l'autre. 1) Des cellules peintes (même dessin que `noyau.html` / `mitose.html`) ; le colorant de Feulgen versé, les noyaux et les chromosomes deviennent rouges. Question « que contiennent les chromosomes ? ». 2) Un chromosome dont on retire les histones : la charpente de protéines reste, et un très long fil d'ADN se déroule. La conclusion « chromosome = ADN + protéines » s'écrit à la fin. |
| 9 | SVT ch4 gène-protéine | `rg_c1b_nirenberg` — Nirenberg et Matthaei : déchiffrer les codons | tableau 3 ARNm → chaîne + 4 encadrés | Un tube in vitro avec un ribosome qui lit l'ARNm de synthèse, codon par codon, et la chaîne qui s'allonge. Poly-U donne Phe-Phe-Phe. UGUG… donne Cys-Val-Cys-Val, joué en question : « lecture par 2 ou par 3 ? ». Les deux lectures sont montrées, une seule donne le résultat. Poly-C donne Pro. Le tableau se remplit à la fin. Nouvelle vue `?vue=nirenberg` de `relation_gene_proteine-tableau/code_genetique.html` (mêmes codons et acides aminés). |
| 10 | SVT ch4 gène-protéine | `rg_t2b_arbre_noel` — L'« arbre de Noël » | tableau « ce qu'on voit / interprétation » (4 lignes) | L'électronographie redessinée qui devient une animation. Des ARN polymérases partent l'une après l'autre sur le gène (le tronc) et les ARN (les branches) s'allongent derrière elles. Les branches courtes sont au début du gène et les longues à la fin. Question « où est le début du gène ? ». Puis chaque ligne d'interprétation s'écrit sur sa ligne de l'image. Nouvelle vue `?vue=arbre_noel` de `relation_gene_proteine-tableau/transcription.html`. |
| 11 | SVT ch4 gène-protéine | `rg_p4b_albinisme` — L'albinisme : une enzyme et un pigment | tableau saine / albinos × tyrosinase, mélanine, phénotype + 3 encadrés | Deux mélanocytes peints côte à côte. Chez la personne saine, la tyrosinase (même forme d'enzyme que dans le cours) transforme la tyrosine en mélanine et la peau se colore. Chez la personne albinos, l'enzyme déformée ne fixe pas la tyrosine : pas de mélanine, la peau reste claire. Un cas puis l'autre, la comparaison à la fin. Avec / sans enzyme fonctionnelle, c'est un cas après cas. |
| 12 | Physique ch5 énergie nucléaire | `en_r3b_applications_dangers` — Applications et dangers | 5 encadrés (α, β, γ arrêtés par…, dangers, applications) | Partie « pouvoir de pénétration » seulement : trois sources tirent α, β et γ vers un papier, puis une plaque d'aluminium de quelques mm, puis du plomb ou du béton. On voit chaque rayonnement arrêté là où il l'est, un moment par écran. Les dangers et les applications restent du texte (ce n'est pas une activité). Dans `physics/energie-nucleaire-tableau/` ou `radioactivite-tableau/` (mêmes particules α, β, γ que le chapitre 4). Priorité basse. |

## Déjà fait dans la copie en attente (le cours en ligne a encore le tableau)

- Physique ch2 `op_t8_non_sinusoidale` (diapason / instrument) et `op_d4_ultrasons` (diffraction des ultrasons) : en
  attente, ce sont des simulations au tableau. Le cours en ligne garde le tableau et les encadrés jusqu'à la bascule de
  la copie en attente.
- SVT ch2 `ms_x3_hypothese` : en attente, `national.html?vue=nageurs` (la figure du national animée). Le cours en ligne
  n'a pas encore de visuel.

## Restent des tableaux (raison)

- Tableaux de raisonnement, de méthode ou de bilan (règle 35 : « sign, variation, avancement, unit and method tables, the
  bilan sheet ») : `phys_ch10_cinetique/ci_g4b_tableau` (tableau d'avancement), `phys_ch9…/tl_rp5_avancement`,
  `math_ch1…/lc_l4c_usuelles` (limites usuelles, une fiche de référence), `math_ch5…/ln_e6`, `ln_e6_b`, `ln_e6_c`
  (étude de fonction), `svt_ch2…/ms_r7_tableau` (bilan des trois voies), `phys_ch1_waves_exemple/wx_b2_national`
  (cas types).
- Méthode de rédaction du national : `wx_b1_redaction`, `op_c3_rediger`, `svt_ch2…/ms_x1_decrire_comparer`,
  `ms_x2_deduire_expliquer` (données données en tableau par l'énoncé : on apprend à le lire).
- `svt_ch1…/le_x2_qui_respire` : exercice type dont l'énoncé du bac donne les valeurs en tableau. À rendre vivant plus
  tard comme figure du national (règle 41), mais ce n'est pas une activité à animer en priorité.
- Calculs : `phys_ch5…/en_m4b_energie_masse`, `phys_ch10…/ci_z4b_couples`.
- `phys_ch1_waves_exemple/wx_l1_aspect` : déjà une simulation, le petit tableau sert à lire les axes.
