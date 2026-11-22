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
  | (Base & { genre: 'redaction'; attendu: string; elements: string[]; correction: string[] });

export interface PartieExamen {
  id: string;
  titre: string;
  /** temps conseillé, pour se repérer (aucun compte à rebours) */
  minutes: number;
  intro?: string;
  tableau?: { entetes: string[]; lignes: string[][] };
  donnees?: string[];
  questions: QuestionExamen[];
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
      id: 'P1', titre: 'Partie I — Restitution des connaissances', minutes: 15,
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
          id: '2', genre: 'vf', points: 2, texte: 'Réponds par vrai ou faux.',
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
        {
          id: '3-c', genre: 'redaction', points: 1, texte: 'Définis un écosystème.',
          attendu: 'Un écosystème est un ensemble dynamique formé d’un milieu naturel, le biotope (eau, sol, climat, lumière…), et des êtres vivants qui l’occupent, la biocénose, qui interagissent entre eux et avec le milieu. Écosystème = biotope + biocénose.',
          elements: ['Le biotope : le milieu et ses facteurs abiotiques (sol, eau, climat, lumière…)', 'La biocénose : les êtres vivants qui l’occupent', 'Des interactions entre les êtres vivants et avec le milieu'],
          correction: ['Écosystème = biotope + biocénose :', 'biotope = le milieu (sol, eau, climat, lumière…) ; biocénose = les êtres vivants qui l’occupent,', 'en interaction entre eux et avec leur milieu.'],
        },
      ],
    },
    {
      id: 'P2', titre: 'Partie II — Exercice 1 : l’eau dans deux sols', minutes: 15,
      intro: 'Pour comparer deux sols A et B, on place 100 g de chaque sol sec dans une bouteille dont le goulot est fermé par du coton. '
        + 'On verse sur chacun V₁ = 100 ml d’eau, puis on mesure le volume d’eau récupéré V₂ et la durée de l’écoulement (t₂ − t₁).',
      tableau: { entetes: ['', 'Sol A', 'Sol B'], lignes: [['Volume récupéré V₂', '70 ml', '20 ml'], ['Durée de l’écoulement t₂ − t₁', '10 min', '20 min']] },
      donnees: ['Perméabilité : P = V₂ / (t₂ − t₁)', 'Capacité de rétention en eau : Vr = V₁ − V₂'],
      questions: [
        { id: '1-1', genre: 'valeur', points: 1, texte: 'Calcule la perméabilité P du sol A.', grandeur: 'P(A)', valeur: 7, unites: ['ml/min', 'ml.min', 'mL/min', 'ml min'],
          correction: ['P(A) = V₂ / (t₂ − t₁) = 70 / 10', 'P(A) = 7 ml/min'] },
        { id: '1-2', genre: 'valeur', points: 1, texte: 'Calcule la perméabilité P du sol B.', grandeur: 'P(B)', valeur: 1, unites: ['ml/min', 'ml.min', 'mL/min', 'ml min'],
          correction: ['P(B) = V₂ / (t₂ − t₁) = 20 / 20', 'P(B) = 1 ml/min'] },
        { id: '1-3', genre: 'valeur', points: 0.5, texte: 'Calcule la capacité de rétention en eau Vr du sol A.', grandeur: 'Vr(A)', valeur: 30, unites: ['ml', 'mL'],
          correction: ['Vr(A) = V₁ − V₂ = 100 − 70', 'Vr(A) = 30 ml'] },
        { id: '1-4', genre: 'valeur', points: 0.5, texte: 'Calcule la capacité de rétention en eau Vr du sol B.', grandeur: 'Vr(B)', valeur: 80, unites: ['ml', 'mL'],
          correction: ['Vr(B) = V₁ − V₂ = 100 − 20', 'Vr(B) = 80 ml'] },
        { id: '1-5', genre: 'redaction', points: 1.5, texte: 'Compare les résultats des deux sols, puis déduis lequel est le sol sableux et lequel est le sol argileux. Justifie.',
          attendu: 'Le sol A est plus perméable que le sol B (7 ml/min contre 1 ml/min) et il retient moins d’eau (30 ml contre 80 ml). Le sol A est donc le sol sableux (gros grains, grands pores où l’eau passe vite) et le sol B le sol argileux (particules fines, petits pores qui retiennent l’eau).',
          elements: ['Perméabilité : A plus perméable que B (7 contre 1 ml/min)', 'Rétention : B retient plus d’eau que A (80 contre 30 ml)', 'Déduction justifiée : A sableux (gros grains, grands pores), B argileux (particules fines, petits pores)'],
          correction: ['Le sol A est plus perméable (7 ml/min > 1 ml/min) et retient moins d’eau (30 ml < 80 ml) que le sol B.', 'A est le sol sableux : gros grains, grands pores, l’eau passe vite.', 'B est le sol argileux : particules fines, petits pores qui retiennent l’eau.'] },
        { id: '1-6', genre: 'redaction', points: 1.5, texte: 'Après plusieurs jours sans pluie, une plante flétrit plus tôt sur le sol A que sur le sol B. Explique ce résultat en t’appuyant sur les formes de l’eau dans le sol.',
          attendu: 'Dans le sol A (sableux), l’eau de gravité s’écoule vite et il reste peu d’eau capillaire, la seule eau utilisable par la plante. La teneur en eau atteint donc vite le point de flétrissement : il ne reste que l’eau hygroscopique, retenue par les particules et inutilisable. Le sol B (argileux) retient beaucoup plus d’eau capillaire : la plante y trouve de l’eau plus longtemps et flétrit plus tard.',
          elements: ['Sol A : l’eau (de gravité) s’écoule vite, il reste peu d’eau capillaire', 'Seule l’eau capillaire est utilisable ; au point de flétrissement il ne reste que l’eau hygroscopique, inutilisable', 'Sol B : il retient plus d’eau capillaire, la plante flétrit plus tard'],
          correction: ['Sol A : l’eau de gravité s’écoule vite ; il reste peu d’eau capillaire, la seule utilisable par la plante.', 'Le point de flétrissement est vite atteint : il ne reste que l’eau hygroscopique, trop retenue, inutilisable.', 'Sol B : il retient beaucoup d’eau capillaire, la plante y puise plus longtemps et flétrit plus tard.'] },
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
      id: 'P4', titre: 'Partie II — Exercice 3 : exploiter les relevés d’une sortie', minutes: 12,
      intro: 'Dans une prairie, on recense les espèces végétales sur des surfaces de plus en plus grandes (technique du quadrillage) :',
      tableau: { entetes: ['Surface du relevé (m²)', '1', '2', '4', '8', '16', '32', '64'], lignes: [['Nombre d’espèces', '4', '7', '10', '13', '15', '15', '15']] },
      questions: [
        { id: '3-1', genre: 'valeur', points: 1, texte: 'Détermine l’aire minimale de cette prairie.', grandeur: 'Aire minimale', valeur: 16, unites: ['m²', 'm2', 'm 2', 'mètres carrés', 'metres carres'],
          correction: ['Le nombre d’espèces cesse d’augmenter à partir de 16 m² (15 espèces à 16, 32 et 64 m²) : c’est le début du palier.', 'Aire minimale = 16 m²'] },
        { id: '3-2', genre: 'valeur', points: 0.5, texte: 'Dans cette prairie, on réalise N = 10 relevés ; le trèfle est présent dans n = 7 relevés. Calcule sa fréquence F.', grandeur: 'F', valeur: 70, unites: ['%'],
          correction: ['F = (n / N) × 100 = (7 / 10) × 100', 'F = 70 %'] },
        { id: '3-3', genre: 'qcm', points: 0.5, texte: 'D’après sa fréquence, le trèfle a :',
          items: [{ texte: 'l’indice de fréquence et la catégorie', choix: ['II — espèce accessoire', 'III — espèce assez fréquente', 'IV — espèce fréquente', 'V — espèce très fréquente'], bonne: 2,
            explication: '60 % ≤ F = 70 % < 80 % : indice IV, espèce fréquente.' }] },
        { id: '3-4', genre: 'valeur', points: 1, texte: 'Dans une autre station, on compte 60 vers de terre au total dans 6 relevés de 2 m² chacun. Calcule leur densité D (nombre d’individus par m²).', grandeur: 'D', valeur: 5, unites: ['/m²', '/m2', 'm-2', 'm⁻²', 'par m', 'individus'],
          correction: ['Surface totale = 6 × 2 = 12 m²', 'D = 60 / 12 = 5 individus/m²'] },
        { id: '3-5', genre: 'redaction', points: 1, texte: 'Les relevés d’une autre station donnent une courbe de fréquence bimodale. Que peux-tu en déduire sur le peuplement végétal et sur le milieu ?',
          attendu: 'Une courbe de fréquence bimodale (ou multimodale) indique que le peuplement est hétérogène ; le milieu n’est pas stable : ses conditions écologiques sont en évolution (positive ou négative).',
          elements: ['Le peuplement (groupement) est hétérogène', 'Le milieu n’est pas stable : ses conditions écologiques évoluent'],
          correction: ['Courbe bimodale → peuplement hétérogène.', 'Le milieu n’est pas stable : ses conditions écologiques sont en évolution (une courbe unimodale montrerait au contraire un milieu homogène et stable).'] },
      ],
    },
  ] as PartieExamen[],
};

export const pointsQuestion = (q: QuestionExamen) => q.points;
export const totalPoints = () => EXAMEN.parties.reduce((n, p) => n + p.questions.reduce((m, q) => m + q.points, 0), 0);
