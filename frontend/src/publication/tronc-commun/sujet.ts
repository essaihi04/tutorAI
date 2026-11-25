/**
 * L'évaluation formative de Tronc Commun Sciences BIOF (SVT), 22 novembre 2026 : https://moalim.online/tronc-commun/?examen
 *
 * Préparation à la vraie évaluation, pas un contrôle chronométré (demande de l'utilisateur) : 20 points prévus pour
 * 50 minutes au plus, sans compte à rebours. Programme couvert : « La sortie écologique » (cours entier) et « Les facteurs
 * édaphiques » jusqu'à l'activité 3 (texture et structure, propriétés chimiques, propriétés hydriques) — rien au-delà.
 *
 * Chaque réponse est corrigée dès qu'elle est donnée : QCM, vrai/faux et calculs dans le navigateur (la clé est connue) ;
 * rédactions par le tuteur, élément par élément du barème (`answer-reaction`, comme la partie Exercices).
 */

export interface ItemQcm { texte: string; choix: string[]; bonne: number; explication: string }
export interface ItemVf { texte: string; vrai: boolean; explication: string }

interface Base { id: string; texte: string; points: number }
export type QuestionExamen =
  | (Base & { genre: 'qcm'; items: ItemQcm[] })
  | (Base & { genre: 'vf'; items: ItemVf[] })
  /** un nombre, jugé dans le navigateur (tolérance relative) ; −0,25 si l'unité manque */
  | (Base & { genre: 'valeur'; grandeur: string; valeur: number; unites: string[]; tolerance?: number; correction: string[] })
  /** une rédaction, notée par le tuteur sur les éléments du barème */
  | (Base & { genre: 'redaction'; attendu: string; elements: string[]; correction: string[] })
  /** tracer les trois lignes dans le triangle des textures (chacune parallèle au bon côté), puis nommer la texture */
  | (Base & { genre: 'triangle'; sol: { argile: number; limon: number; sable: number }; zone: string; choix: string[]; correction: string[] })
  /** ranger les comptes dans le tableau (IF / nombre d'espèces), monter les barres collées, placer les points de la courbe */
  | (Base & { genre: 'histogramme'; especes: [string, string][]; comptes: number[]; correction: string[] });

export interface PartieExamen {
  id: string;
  titre: string;
  /** temps conseillé, pour se repérer (aucun compte à rebours) */
  minutes: number;
  intro?: string;
  tableau?: { entetes: string[]; lignes: string[][] };
  donnees?: string[];
  questions: QuestionExamen[];
  /** nom court de l'onglet (ex. « Ex. 1 ») */
  court?: string;
  /** figures de l'énoncé (format des exercices : FiguresCahier) */
  figures?: unknown[];
}

export const EXAMEN = {
  titre: 'Évaluation formative — Sortie écologique et facteurs édaphiques',
  niveau: 'Tronc Commun Sciences BIOF',
  matiere: 'SVT',
  minutes: 50,
  consigne: "Prépare-toi à la vraie évaluation : réponds à chaque question comme sur ta copie. Dès que tu réponds, le tuteur corrige, " +
    "te donne ta note sur le barème et t'explique la bonne réponse. Prévois 50 minutes au plus ; tu avances à ton rythme.",
  parties: [
    {
      id: 'P1', titre: 'Partie I — Restitution des connaissances', minutes: 12,
      questions: [
        {
          id: '1', genre: 'qcm', points: 2, texte: 'Pour chaque proposition, choisis la seule réponse juste.',
          items: [
            { texte: 'La texture d’un sol correspond :', choix: ['à l’agencement des particules minérales et organiques', 'aux pourcentages de sables, de limons et d’argiles', 'à la quantité d’eau retenue par le sol', 'au pH de la solution du sol'], bonne: 1,
              explication: 'La texture, c’est la composition granulométrique : les pourcentages de sables, de limons et d’argiles. L’agencement des particules, c’est la structure.' },
            { texte: 'Le chêne-liège pousse sur les sols siliceux (acides) mais pas sur les sols calcaires : c’est une plante', choix: ['calcicole', 'calcifuge et silicicole', 'calcicole et silicifuge', 'indifférente au calcium'], bonne: 1,
              explication: 'Il fuit le calcaire (calcifuge) et préfère les sols siliceux (silicicole) : sur sol calcaire, le calcium gêne l’absorption des autres ions minéraux.' },
            { texte: 'L’eau du sol utilisable par les plantes est', choix: ['l’eau de gravité', 'l’eau hygroscopique', 'l’eau capillaire', 'toute l’eau du sol'], bonne: 2,
              explication: 'L’eau capillaire reste dans les fins pores après le drainage : la succion des racines est plus forte que l’attraction des particules, la plante l’absorbe. L’eau de gravité s’écoule ; l’eau hygroscopique est trop retenue.' },
            { texte: 'Lors d’une sortie écologique, la croix du bûcheron sert à', choix: ['capturer les insectes des branches', 'mesurer la hauteur d’un arbre', 'délimiter l’aire minimale', 'conserver les animaux récoltés'], bonne: 1,
              explication: 'Avec deux baguettes égales en T couché, on recule jusqu’à viser la base et le sommet de l’arbre : la distance D à l’arbre est égale à sa hauteur H.' },
          ],
        },
        {
          id: '2', genre: 'vf', points: 1, texte: 'Réponds par vrai ou faux.',
          items: [
            { texte: 'Le complexe argilo-humique est chargé négativement : il retient les cations (K⁺, Ca²⁺, Mg²⁺…).', vrai: true,
              explication: 'Vrai : l’expérience du bleu de méthylène (cations retenus, filtrat incolore) le montre.' },
            { texte: 'Un sol sableux a une faible perméabilité et une forte capacité de rétention en eau.', vrai: false,
              explication: 'Faux : c’est l’inverse. Le sol sableux, à gros grains et grands pores, laisse passer l’eau vite (forte perméabilité) et en retient peu.' },
            { texte: 'Une espèce d’indice de fréquence V est présente dans 80 % à 100 % des relevés.', vrai: true,
              explication: 'Vrai : 80 % ≤ F ≤ 100 % donne l’indice V, espèce très fréquente.' },
            { texte: 'Un écosystème est formé seulement de la biocénose.', vrai: false,
              explication: 'Faux : écosystème = biotope (le milieu et ses facteurs abiotiques) + biocénose (les êtres vivants), en interaction.' },
          ],
        },
        {
          id: '3-a', genre: 'redaction', points: 1, texte: 'Définis le point de flétrissement.',
          attendu: 'Le point de flétrissement est le pourcentage d’eau du sol au moment où la plante ne peut plus s’y approvisionner en eau et commence à souffrir de la sécheresse (elle flétrit).',
          elements: ['C’est un pourcentage (une teneur) d’eau du sol', 'À ce moment, la plante ne peut plus absorber l’eau du sol et flétrit'],
          correction: ['Le point de flétrissement : le % d’eau du sol au moment où la plante ne peut plus s’y approvisionner en eau', 'et commence à souffrir de la sécheresse (elle flétrit). Il ne reste alors que l’eau hygroscopique, inutilisable.'],
        },
        {
          id: '3-b', genre: 'redaction', points: 1, texte: 'Définis l’aire minimale d’un relevé.',
          attendu: 'L’aire minimale est la plus petite surface où sont représentées toutes les espèces végétales du milieu ; sur la courbe nombre d’espèces en fonction de la surface, elle correspond au début du palier.',
          elements: ['La plus petite surface du relevé', 'où toutes les espèces végétales du milieu sont représentées'],
          correction: ['L’aire minimale : la plus petite surface où sont représentées toutes les espèces végétales du milieu.', 'Sur la courbe « nombre d’espèces = f(surface) », c’est la surface où commence le palier.'],
        },
      ],
    },
    {
      id: 'P2', titre: 'Partie II — Exercice 1 : la texture et l’eau du sol', minutes: 17,
      intro: 'Pour comparer deux sols A et B, on place 100 g de chaque sol sec dans une bouteille dont le goulot est fermé par du coton. '
        + 'On verse sur chacun V₁ = 100 ml d’eau, puis on mesure le volume d’eau récupéré V₂ et la durée de l’écoulement (t₂ − t₁).',
      tableau: { entetes: ['', 'Sol A', 'Sol B'], lignes: [['Volume récupéré V₂', '70 ml', '20 ml'], ['Durée de l’écoulement t₂ − t₁', '10 min', '20 min']] },
      donnees: ['Perméabilité : P = V₂ / (t₂ − t₁)', 'Capacité de rétention en eau : Vr = V₁ − V₂', 'Le triangle des textures est donné dans la question 1-7.'],
      questions: [
        { id: '1-1', genre: 'valeur', points: 1, texte: 'Calcule la perméabilité P du sol A.', grandeur: 'P(A)', valeur: 7, unites: ['ml/min', 'ml.min', 'mL/min', 'ml min'],
          correction: ['P(A) = V₂ / (t₂ − t₁) = 70 / 10', 'P(A) = 7 ml/min'] },
        { id: '1-2', genre: 'valeur', points: 1, texte: 'Calcule la perméabilité P du sol B.', grandeur: 'P(B)', valeur: 1, unites: ['ml/min', 'ml.min', 'mL/min', 'ml min'],
          correction: ['P(B) = V₂ / (t₂ − t₁) = 20 / 20', 'P(B) = 1 ml/min'] },
        { id: '1-3', genre: 'valeur', points: 0.5, texte: 'Calcule la capacité de rétention en eau Vr du sol A.', grandeur: 'Vr(A)', valeur: 30, unites: ['ml', 'mL'],
          correction: ['Vr(A) = V₁ − V₂ = 100 − 70', 'Vr(A) = 30 ml'] },
        { id: '1-4', genre: 'valeur', points: 0.5, texte: 'Calcule la capacité de rétention en eau Vr du sol B.', grandeur: 'Vr(B)', valeur: 80, unites: ['ml', 'mL'],
          correction: ['Vr(B) = V₁ − V₂ = 100 − 20', 'Vr(B) = 80 ml'] },
        { id: '1-5', genre: 'redaction', points: 1, texte: 'Compare les résultats des deux sols, puis déduis lequel est le sol sableux et lequel est le sol argileux. Justifie.',
          attendu: 'Le sol A est plus perméable que le sol B (7 ml/min contre 1 ml/min) et il retient moins d’eau (30 ml contre 80 ml). Le sol A est donc le sol sableux (gros grains, grands pores où l’eau passe vite) et le sol B le sol argileux (particules fines, petits pores qui retiennent l’eau).',
          elements: ['Perméabilité : A plus perméable que B (7 contre 1 ml/min)', 'Rétention : B retient plus d’eau que A (80 contre 30 ml)', 'Déduction justifiée : A sableux (gros grains, grands pores), B argileux (particules fines, petits pores)'],
          correction: ['Le sol A est plus perméable (7 ml/min > 1 ml/min) et retient moins d’eau (30 ml < 80 ml) que le sol B.', 'A est le sol sableux : gros grains, grands pores, l’eau passe vite.', 'B est le sol argileux : particules fines, petits pores qui retiennent l’eau.'] },
        { id: '1-6', genre: 'redaction', points: 1, texte: 'Après plusieurs jours sans pluie, une plante flétrit plus tôt sur le sol A que sur le sol B. Explique ce résultat en t’appuyant sur les formes de l’eau dans le sol.',
          attendu: 'Dans le sol A (sableux), l’eau de gravité s’écoule vite et il reste peu d’eau capillaire, la seule eau utilisable par la plante. La teneur en eau atteint donc vite le point de flétrissement : il ne reste que l’eau hygroscopique, retenue par les particules et inutilisable. Le sol B (argileux) retient beaucoup plus d’eau capillaire : la plante y trouve de l’eau plus longtemps et flétrit plus tard.',
          elements: ['Sol A : l’eau (de gravité) s’écoule vite, il reste peu d’eau capillaire', 'Seule l’eau capillaire est utilisable ; au point de flétrissement il ne reste que l’eau hygroscopique, inutilisable', 'Sol B : il retient plus d’eau capillaire, la plante flétrit plus tard'],
          correction: ['Sol A : l’eau de gravité s’écoule vite ; il reste peu d’eau capillaire, la seule utilisable par la plante.', 'Le point de flétrissement est vite atteint : il ne reste que l’eau hygroscopique, trop retenue, inutilisable.', 'Sol B : il retient beaucoup d’eau capillaire, la plante y puise plus longtemps et flétrit plus tard.'] },
        { id: '1-7', genre: 'triangle', points: 2,
          texte: 'Un troisième sol C contient 30 % d’argile, 60 % de sable et 10 % de limon. Dans le triangle des textures, trace les trois lignes (chacune part de sa graduation et est parallèle au bon côté), puis donne la texture du sol C.',
          sol: { argile: 30, limon: 10, sable: 60 }, zone: 'Limon argilo-sableux',
          choix: ['Argile sableuse', 'Limon argilo-sableux', 'Limon sableux', 'Sable limoneux', 'Limon argileux'],
          correction: ['Argile 30 % : la ligne part de 30 sur l’axe de l’argile (côté gauche), parallèle au côté du sable, c’est-à-dire à la base du triangle (ligne horizontale).', 'Limon 10 % : la ligne part de 10 sur l’axe du limon (côté droit), parallèle au côté de l’argile, c’est-à-dire au côté gauche du triangle.',
            'Sable 60 % : la ligne part de 60 sur l’axe du sable (la base), parallèle au côté du limon, c’est-à-dire au côté droit du triangle.', 'Les trois lignes se coupent dans le domaine « Limon argilo-sableux » : c’est la texture du sol C.'] },
      ],
    },
    {
      id: 'P3', titre: 'Partie II — Exercice 2 : le complexe argilo-humique', minutes: 8,
      intro: 'On place 100 g d’un sol de jardin riche en humus dans deux entonnoirs munis d’un filtre. Sur le premier, on verse 20 ml d’éosine '
        + '(colorant rouge porté par des ions négatifs) ; sur le second, 20 ml de bleu de méthylène (colorant bleu porté par des ions positifs).',
      tableau: { entetes: ['', 'Entonnoir 1 : éosine', 'Entonnoir 2 : bleu de méthylène'], lignes: [['Filtrat obtenu', 'rouge', 'incolore et limpide']] },
      questions: [
        { id: '2-1', genre: 'redaction', points: 1, texte: 'Interprète le résultat obtenu avec le bleu de méthylène, puis celui obtenu avec l’éosine.',
          attendu: 'Le filtrat du bleu de méthylène est incolore : ses ions positifs (cations) ont été retenus par le sol. Le filtrat de l’éosine reste rouge : ses ions négatifs (anions) n’ont pas été retenus, ils ont été repoussés par le sol.',
          elements: ['Bleu de méthylène : ses cations sont retenus par le sol, d’où le filtrat incolore', 'Éosine : ses anions ne sont pas retenus (repoussés), d’où le filtrat rouge'],
          correction: ['Bleu de méthylène : filtrat incolore → ses ions positifs ont été retenus par le sol.', 'Éosine : filtrat rouge → ses ions négatifs n’ont pas été retenus, ils ont été repoussés.'] },
        { id: '2-2', genre: 'redaction', points: 1, texte: 'Déduis la charge électrique du complexe argilo-humique (CAH) et cite ses deux constituants.',
          attendu: 'Le CAH est chargé négativement : il attire et retient les cations, et repousse les anions. Il est formé d’argile (constituant minéral) et d’humus (matière organique décomposée).',
          elements: ['Le CAH est chargé négativement (il retient les cations, repousse les anions)', 'Constituants : l’argile et l’humus'],
          correction: ['Le CAH est chargé négativement : il retient les cations et repousse les anions.', 'Il est formé d’argile (minérale) et d’humus (matière organique décomposée).'] },
        { id: '2-3', genre: 'redaction', points: 1, texte: 'Explique l’importance du complexe argilo-humique pour la nutrition minérale des plantes.',
          attendu: 'Le CAH retient à sa surface les cations minéraux (K⁺, Ca²⁺, Mg²⁺, NH₄⁺…), ce qui limite leur perte dans les eaux de drainage (lessivage) ; il les libère peu à peu dans la solution du sol (échange de cations), où les racines les absorbent : la plante a un accès continu aux éléments nutritifs.',
          elements: ['Il retient les cations minéraux et limite leur perte dans les eaux de drainage', 'Il les libère progressivement dans la solution du sol, où les racines les absorbent'],
          correction: ['Le CAH retient les cations minéraux (K⁺, Ca²⁺, Mg²⁺, NH₄⁺…) : ils ne sont pas perdus dans les eaux de drainage.', 'Il les libère peu à peu dans la solution du sol : les racines les absorbent de façon continue.'] },
      ],
    },
    {
      id: 'P4', titre: 'Partie II — Exercice 3 : exploiter les relevés d’une sortie', minutes: 13,
      intro: 'Dans une prairie, on recense les espèces végétales sur des surfaces de plus en plus grandes (technique du quadrillage) :',
      tableau: { entetes: ['Surface du relevé (m²)', '1', '2', '4', '8', '16', '32', '64'], lignes: [['Nombre d’espèces', '4', '7', '10', '13', '15', '15', '15']] },
      donnees: ['Fréquence : F = (n / N) × 100 (n : relevés où l’espèce est présente ; N : nombre total de relevés)',
        'Indices de fréquence : F < 20 % → I (accidentelle) ; 20 % ≤ F < 40 % → II (accessoire) ; 40 % ≤ F < 60 % → III (assez fréquente) ; 60 % ≤ F < 80 % → IV (fréquente) ; 80 % ≤ F ≤ 100 % → V (très fréquente)'],
      questions: [
        { id: '3-1', genre: 'valeur', points: 1, texte: 'Détermine l’aire minimale de cette prairie.', grandeur: 'Aire minimale', valeur: 16, unites: ['m²', 'm2', 'm 2', 'mètres carrés', 'metres carres'],
          correction: ['Le nombre d’espèces cesse d’augmenter à partir de 16 m² (15 espèces à 16, 32 et 64 m²) : c’est le début du palier.', 'Aire minimale = 16 m²'] },
        { id: '3-2', genre: 'valeur', points: 0.5, texte: 'Dans cette prairie, on réalise N = 10 relevés ; le trèfle est présent dans n = 7 relevés. Calcule sa fréquence F.', grandeur: 'F', valeur: 70, unites: ['%'],
          correction: ['F = (n / N) × 100 = (7 / 10) × 100', 'F = 70 %'] },
        { id: '3-3', genre: 'qcm', points: 0.5, texte: 'D’après sa fréquence, le trèfle a :',
          items: [{ texte: 'l’indice de fréquence et la catégorie', choix: ['II — espèce accessoire', 'III — espèce assez fréquente', 'IV — espèce fréquente', 'V — espèce très fréquente'], bonne: 2,
            explication: '60 % ≤ F = 70 % < 80 % : indice IV, espèce fréquente.' }] },
        { id: '3-4', genre: 'valeur', points: 0.5, texte: 'Dans une autre station, on compte 60 vers de terre au total dans 6 relevés de 2 m² chacun. Calcule leur densité D (nombre d’individus par m²).', grandeur: 'D', valeur: 5, unites: ['/m²', '/m2', 'm-2', 'm⁻²', 'par m', 'individus'],
          correction: ['Surface totale = 6 × 2 = 12 m²', 'D = 60 / 12 = 5 individus/m²'] },
        { id: '3-5', genre: 'histogramme', points: 1.5,
          texte: 'Dans une troisième station, on a trouvé l’indice de fréquence de chaque espèce (liste ci-dessous). Range d’abord les comptes dans le tableau (IF / nombre d’espèces), puis trace l’histogramme de fréquence (rectangles collés) et la courbe de fréquence.',
          especes: [['Quercus suber', 'V'], ['Cistus salvifolius', 'V'], ['Lavandula stoechas', 'V'], ['Chamaerops humilis', 'IV'], ['Carex distachya', 'IV'],
            ['Rubia peregrina', 'III'], ['Daphne gnidium', 'II'], ['Urginea maritima', 'II'], ['Thymelaea lythroides', 'I'], ['Carlina corymbosa', 'I'],
            ['Ranunculus paludosus', 'I'], ['Holcus lanatus', 'I'], ['Anagallis arvensis', 'I']],
          comptes: [5, 2, 1, 2, 3],
          correction: ['Tableau : I → 5 · II → 2 · III → 1 · IV → 2 · V → 3 espèces.', 'Histogramme : en abscisse les indices I à V, en ordonnée le nombre d’espèces ; un rectangle par indice, collés les uns aux autres.',
            'Courbe : on relie les milieux des sommets des rectangles (on ne demande pas ici de la qualifier : c’est la question 3-6).'] },
        { id: '3-6', genre: 'redaction', points: 1, texte: 'La courbe de fréquence que tu viens de tracer est bimodale. Que peux-tu en déduire sur le peuplement végétal et sur le milieu de cette station ?',
          attendu: 'Une courbe de fréquence bimodale (ou multimodale) indique que le peuplement est hétérogène ; le milieu n’est pas stable : ses conditions écologiques sont en évolution (positive ou négative).',
          elements: ['Le peuplement (groupement) est hétérogène', 'Le milieu n’est pas stable : ses conditions écologiques évoluent'],
          correction: ['Courbe bimodale → peuplement hétérogène.', 'Le milieu n’est pas stable : ses conditions écologiques sont en évolution (une courbe unimodale montrerait au contraire un milieu homogène et stable).'] },
      ],
    },
  ] as PartieExamen[],
};

export const pointsQuestion = (q: QuestionExamen) => q.points;
export const totalPoints = () => EXAMEN.parties.reduce((n, p) => n + p.questions.reduce((m, q) => m + q.points, 0), 0);
