# Chaîne respiratoire et phosphorylation oxydative

La diapositive `energy_a07_s02` utilise le preset existant
`svt_ch1_chimiosmose`, maintenant rendu par `RespiratoryChainVisual` en SVG
transparent. Deux boutons sélectionnent `nadh` ou `fadh2` ; `scene` reste
compatible avec les anciens decks et correspond au trajet NADH.

Le contrôle partagé du tuteur conserve démarrage, pause, remise au début,
pas suivant/précédent, choix de variante et état final `finished`. Le rendu
respecte la préférence de réduction des mouvements. Aucun script ni asset
externe n'est chargé. La tête F₁ est fixe côté matrice ; le rotor central
tourne. Les particules illustrent le mouvement, pas une vitesse moléculaire
ou un comptage stœchiométrique en temps réel.

Les bilans sont exprimés par paire d'électrons : CI = 4 H⁺, CII = 0,
CIII = 4, CIV = 2. NADH entraîne donc le déplacement de 10 H⁺, FADH₂ de 6.
Les 2 H⁺ consommés avec ½ O₂ pour produire H₂O ne sont pas les 2 H⁺ pompés
par CIV. Les électrons ne traversent jamais l'ATP synthase.

L'affichage suit la convention scolaire demandée : **3 ATP/NADH,H⁺ et
2 ATP/FADH₂**. Ce bilan théorique par coenzyme n'est ni un compteur en
temps réel ni une affirmation d'un rendement biochimique universel.

La scène comporte 18 pas et trois raccourcis : accumulation (4), retour
avec pompage encore actif (9), puis arrêt du pompage et relaxation (13–18).
Les H⁺ sont visibles dans les deux compartiments, avec leur pH et
ΔpH = pH matrice − pH espace. Les concentrations et leur rapport restent
disponibles dans le modèle sans surcharger le dessin.

Le modèle est illustratif, à volumes-échantillons égaux, sans tampon :
55 ± 45 × intensité nmol/L. Il conserve 22 marqueurs, chacun représentant
5 nmol/L dans son échantillon. Au maximum : 20 marqueurs contre 2,
pH 7 contre 8 (100 contre 10 nmol/L). À l'équilibre : 11 contre 11 et
pH ≈ 7,26 de chaque côté. Cela n'imite pas les volumes ni le pouvoir tampon
des compartiments mitochondriaux réels. Le champ électrique est supposé
se dissiper aussi pendant cette démonstration : **l'égalité des seuls pH
ne suffit pas à conclure à l'absence de force proton-motrice réelle**.
Le pompage et les électrons s'arrêtent au pas 13 ; les derniers H⁺ passent
par l'ATP synthase jusqu'au pas 18. Le rotor et les particules d'ATP cessent
alors de s'animer. L'état communiqué au tuteur est recalculé côté serveur.

Vérification du modèle : `node frontend/scripts/test-respiratory-chain.mjs`.

L'affichage réduit ne montre plus les équations de réaction ni les longs
paragraphes : seuls restent les noms des compartiments, pH, ΔpH, bilan
scolaire et une courte légende. Les concentrations détaillées sont conservées
dans le modèle. Les explications restent accessibles via descriptions et
info-bulles. Trois zones cliquables et accessibles au clavier rejouent les
événements moléculaires : coenzyme réduit → départ des deux électrons ;
O₂ qui attend puis reçoit quatre e⁻ et quatre H⁺ → deux molécules d'eau ;
ADP à deux phosphates qui reçoit Pi → ATP à trois phosphates, après retour
des H⁺. Les transformations CSS respectent pause et réduction du mouvement.
Ces vues locales illustrent des événements, pas un compteur stœchiométrique
de toute la mitochondrie.

Références : [Mitochondrial electron transport chain, Figure 1 (2020)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7767752/)
et [ATP synthase: From sequence to ring size to the P/O ratio (2010)](https://pmc.ncbi.nlm.nih.gov/articles/PMC2947903/).

Aperçu dans le vrai lecteur : `/dev/course-player?scene=respiratory-chain`.
Le manifeste local est modifié ; la synchronisation/publication d'un deck
hébergé et la régénération de sa narration audio sont des opérations séparées.
Ne pas synchroniser l'ensemble du cours pour cette seule scène sans vérifier
les autres modifications en attente.
