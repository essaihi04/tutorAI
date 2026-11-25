/**
 * L'évaluation formative du Tronc Commun physique-chimie (lien /TCF, 25 novembre 2026) : https://moalim.online/TCF/?examen
 *
 * Demande de l'utilisateur : « créer une évaluation englobant tous ces chapitres », « comme chez SVT pour le tronc commun ».
 * Même forme que l'évaluation de SVT (`../tronc-commun/sujet.ts`) : 20 points, environ 55 minutes, sans chronomètre, un temps
 * conseillé par partie, chaque réponse corrigée dès qu'elle est rendue (QCM, vrai/faux, calculs dans le navigateur ;
 * rédactions par le tuteur, élément par élément du barème). La page est `../tronc-commun/Examen.tsx` (`utiliserSujet`).
 *
 * Programme couvert, rien au-delà (livre du professeur) :
 *  - Chimie : « Synthèse d'espèces chimiques » (p. 118-121) et la CCM (p. 114-117) ; « Modèle de l'atome » (p. 122-128) ;
 *  - Physique : « Le mouvement » (p. 26-35) et « Principe d'inertie » (p. 36-42).
 * Nombres simples (règle 1 du skill tronc-commun), données différentes des exemples du livre et des cours ; figures
 * dessinées (format des figures du cahier), jamais une image du livre.
 *
 * Voix : `cours/tc_tcf_examen_voix.json` (clés `partie/<id>`, `question/<id>`, `correction/<id>`) ; `VOIX_TCF` liste
 * les pistes réellement posées dans `/media/audio/courses/tc_tcf_examen/` (vide tant qu'elles ne sont pas générées).
 */
import type { PartieExamen } from '../tronc-commun/sujet';

/** les figures de l'énoncé : format `FigureCahierData` (rendu `FiguresCahier`, craie inversée en noir sur la feuille) */
const MONTAGE_REFLUX = {
  type: 'schema', titre: 'Le montage de la synthèse',
  cadre: { l: 11, h: 12 },
  legende: 'Les éléments ①, ② et ③ et la flèche ④ sont à nommer (question 1-1).',
  elements: [
    // la potence et sa pince
    { f: 'ligne', pts: [[0.8, 0.3], [0.8, 11.2]], epais: true, couleur: 'faible' },
    { f: 'rect', de: [0.2, 0.1], a: [2.2, 0.4], couleur: 'faible' },
    { f: 'ligne', pts: [[0.8, 8.3], [3.5, 8.3]], couleur: 'faible' },
    // le chauffe-ballon
    { f: 'rect', de: [2.5, 0.3], a: [6.5, 2.1], arrondi: true, remplir: 'orange', couleur: 'orange' },
    // le ballon et le mélange
    { f: 'cercle', c: [4.5, 3.4], r: 1.3, couleur: 'blanc' },
    { f: 'ligne', pts: [[3.35, 2.9], [5.65, 2.9]], couleur: 'jaune' },
    { f: 'ligne', pts: [[3.5, 2.6], [4.5, 2.12], [5.5, 2.6]], lisse: true, remplir: 'jaune', couleur: 'jaune' },
    { f: 'point', at: [4.1, 2.6], couleur: 'faible' },
    { f: 'point', at: [4.9, 2.5], couleur: 'faible' },
    { f: 'ligne', pts: [[4.15, 4.62], [4.15, 5.4]] },
    { f: 'ligne', pts: [[4.85, 4.62], [4.85, 5.4]] },
    // le réfrigérant à boules (tube intérieur à boules dans sa gaine d'eau)
    { f: 'rect', de: [3.4, 5.4], a: [5.6, 10.2], arrondi: true, couleur: 'cyan', remplir: 'cyan' },
    { f: 'ellipse', c: [4.5, 6.4], rx: 0.6, ry: 0.55 },
    { f: 'ellipse', c: [4.5, 7.8], rx: 0.6, ry: 0.55 },
    { f: 'ellipse', c: [4.5, 9.2], rx: 0.6, ry: 0.55 },
    { f: 'ligne', pts: [[4.5, 10.2], [4.5, 11.3]], epais: true },
    // l'eau : la flèche ④ (en bas) et la sortie (en haut)
    { f: 'fleche', de: [7.6, 5.9], a: [5.6, 5.9], couleur: 'bleu' },
    { f: 'fleche', de: [5.6, 9.8], a: [7.6, 9.8], couleur: 'bleu' },
    // les numéros
    { f: 'ligne', pts: [[5.6, 7.8], [8.6, 7.8]], couleur: 'faible' },
    { f: 'texte', at: [9.3, 7.8], t: '①', taille: 'grand' },
    { f: 'ligne', pts: [[5.8, 3.4], [8.6, 3.4]], couleur: 'faible' },
    { f: 'texte', at: [9.3, 3.4], t: '②', taille: 'grand' },
    { f: 'ligne', pts: [[6.5, 1.2], [8.6, 1.2]], couleur: 'faible' },
    { f: 'texte', at: [9.3, 1.2], t: '③', taille: 'grand' },
    { f: 'texte', at: [8.3, 5.9], t: '④', taille: 'grand' },
  ],
};

const CHROMATOGRAMME = {
  type: 'schema', titre: 'Le chromatogramme (révélé)',
  cadre: { l: 10, h: 13.6 },
  legende: 'A : alcool isoamylique pur ; B : acétate d’isoamyle pur ; C : produit obtenu en fin de synthèse.',
  elements: [
    { f: 'rect', de: [0.5, 1.2], a: [7.5, 12.8], couleur: 'blanc' },
    { f: 'ligne', pts: [[0.5, 2], [7.5, 2]], trait: 'pointille', couleur: 'faible' },
    { f: 'texte', at: [4, 1.55], t: 'ligne de dépôt', taille: 'petit' },
    { f: 'ligne', pts: [[0.5, 12], [7.5, 12]], couleur: 'cyan' },
    { f: 'texte', at: [4, 12.4], t: 'front de l’éluant', taille: 'petit', couleur: 'cyan' },
    // les dépôts
    { f: 'texte', at: [2, 0.6], t: 'A' }, { f: 'texte', at: [4, 0.6], t: 'B' }, { f: 'texte', at: [6, 0.6], t: 'C' },
    { f: 'point', at: [2, 2], creux: true, couleur: 'faible' }, { f: 'point', at: [4, 2], creux: true, couleur: 'faible' }, { f: 'point', at: [6, 2], creux: true, couleur: 'faible' },
    // les taches
    { f: 'ellipse', c: [2, 5], rx: 0.4, ry: 0.28, remplir: 'orange', couleur: 'orange' },
    { f: 'ellipse', c: [4, 9], rx: 0.4, ry: 0.28, remplir: 'orange', couleur: 'orange' },
    { f: 'ellipse', c: [6, 5], rx: 0.4, ry: 0.28, remplir: 'orange', couleur: 'orange' },
    { f: 'ellipse', c: [6, 9], rx: 0.4, ry: 0.28, remplir: 'orange', couleur: 'orange' },
    // la règle graduée en cm, zéro sur la ligne de dépôt
    { f: 'ligne', pts: [[8.3, 2], [8.3, 12]] },
    ...[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(k => ({ f: 'ligne', pts: [[8.3, 2 + k], [k % 5 === 0 ? 8.85 : 8.6, 2 + k]] })),
    { f: 'texte', at: [9.2, 2], t: '0', taille: 'petit', ancre: 'gauche' },
    { f: 'texte', at: [9.2, 7], t: '5', taille: 'petit', ancre: 'gauche' },
    { f: 'texte', at: [9.05, 12.5], t: 'cm', taille: 'petit', ancre: 'gauche' },
    { f: 'texte', at: [9.2, 12], t: '10', taille: 'petit', ancre: 'gauche' },
  ],
};

const ENREGISTREMENT = {
  type: 'schema', titre: 'Figure 1 — L’enregistrement (τ = 20 ms)',
  cadre: { l: 28, h: 7 },
  legende: 'Les positions sont alignées ; deux positions successives sont à 4 cm l’une de l’autre.',
  elements: [
    { f: 'ligne', pts: [[0.3, 3.5], [27.7, 3.5]], trait: 'pointille', couleur: 'faible' },
    ...[0, 1, 2, 3, 4, 5, 6].map(i => ({ f: 'point', at: [1.5 + 4 * i, 3.5], t: `M${'₀₁₂₃₄₅₆'[i]}`, pos: 'n' })),
    { f: 'cote', de: [1.5, 1.6], a: [5.5, 1.6], t: '4 cm', pos: 's' },
    { f: 'fleche', de: [19.5, 6.3], a: [25.5, 6.3], texte: 'sens du mouvement', pos: 'n', couleur: 'jaune' },
  ],
};

const CERCLE = {
  type: 'schema', titre: 'Figure 2 — Le point M du bord du disque',
  cadre: { l: 10, h: 10 },
  legende: 'M tourne sur un cercle de centre O et de rayon R = 0,5 m, à vitesse constante v = 1 m/s.',
  elements: [
    { f: 'cercle', c: [5, 5], r: 3.5, remplir: 'faible', couleur: 'blanc' },
    { f: 'point', at: [5, 5], t: 'O', pos: 'so' },
    { f: 'ligne', pts: [[5, 5], [6.75, 8.03]], couleur: 'faible' },
    { f: 'texte', at: [5.4, 6.9], t: 'R', ancre: 'droite' },
    { f: 'point', at: [6.75, 8.03], t: 'M', pos: 'ne', couleur: 'jaune' },
    { f: 'fleche', de: [6.75, 8.03], a: [4.85, 9.13], texte: 'v', pos: 'n', couleur: 'jaune' },
    { f: 'arc', c: [5, 5], r: 4.2, de: -20, a: 30, fleche: true, couleur: 'cyan' },
  ],
};

const MARTEAU = {
  type: 'schema', titre: 'Le marteau (schéma sans échelle)',
  cadre: { l: 12, h: 6 },
  legende: 'G₁ : centre d’inertie du manche ; G₂ : centre d’inertie de la tête ; G₁G₂ = 20 cm.',
  elements: [
    { f: 'rect', de: [0.6, 2.6], a: [9, 3.4], arrondi: true, remplir: 'orange', couleur: 'orange' },
    { f: 'rect', de: [9, 1], a: [11.2, 5], remplir: 'faible', couleur: 'blanc' },
    { f: 'point', at: [4.8, 3] },
    { f: 'texte', at: [4.8, 4.1], t: 'G₁' },
    { f: 'point', at: [10.1, 3], t: 'G₂', pos: 'n' },
    { f: 'cote', de: [4.8, 0.4], a: [10.1, 0.4], t: '20 cm', pos: 'n' },
    { f: 'texte', at: [2.2, 4.1], t: 'manche', taille: 'petit' },
    { f: 'texte', at: [10.1, 5.5], t: 'tête', taille: 'petit' },
  ],
};

export const SUJET_TCF = {
  titre: 'Évaluation formative — Synthèse, atome, mouvement et principe d’inertie',
  niveau: 'Tronc Commun Sciences BIOF',
  matiere: 'Physique-Chimie',
  minutes: 55,
  programme: 'la synthèse d’une espèce chimique et la CCM ; le modèle de l’atome ; le mouvement (vitesse, mouvement rectiligne uniforme, mouvement circulaire uniforme) ; le principe d’inertie et le centre d’inertie',
  consigne: 'Prépare-toi à la vraie évaluation : réponds à chaque question comme sur ta copie, avec la relation, l’application numérique et le résultat avec son unité. '
    + 'Dès que tu réponds, le tuteur corrige, te donne ta note sur le barème et t’explique la bonne réponse. Prévois environ 55 minutes ; tu avances à ton rythme.',
  parties: [
    {
      id: 'P1', court: 'Chimie 1', titre: 'Chimie 1 — Synthèse d’une espèce chimique et CCM', minutes: 14,
      intro: 'L’acétate d’isoamyle est une espèce chimique à l’odeur de banane. Pour la synthétiser, on place dans un ballon de l’alcool isoamylique, '
        + 'de l’acide acétique et quelques grains de pierre ponce, puis on chauffe à reflux pendant 30 min avec le montage ci-dessous. '
        + 'On vérifie ensuite le produit obtenu par chromatographie sur couche mince (CCM) : on dépose A (alcool isoamylique pur), '
        + 'B (acétate d’isoamyle pur) et C (produit obtenu en fin de synthèse), on élue, puis on révèle les taches.',
      figures: [MONTAGE_REFLUX, CHROMATOGRAMME],
      donnees: ['Sur le chromatogramme : H = 10 cm (de la ligne de dépôt au front de l’éluant).',
        'Tache de A : h = 3 cm ; tache de B : h = 7 cm (hauteurs comptées depuis la ligne de dépôt).',
        'Rapport frontal : Rf = h/H'],
      questions: [
        {
          id: '1-1', genre: 'qcm', points: 1, texte: 'Nomme les éléments du montage : pour chaque numéro, choisis le bon nom.',
          items: [
            { texte: 'L’élément ① est :', choix: ['le ballon', 'le réfrigérant à boules', 'l’ampoule à décanter', 'l’éprouvette graduée'], bonne: 1,
              explication: '① est le réfrigérant à boules : l’eau froide qui circule autour des boules refroidit les vapeurs et les transforme en liquide.' },
            { texte: 'L’élément ② est :', choix: ['le chauffe-ballon', 'le bécher', 'le ballon', 'le réfrigérant'], bonne: 2,
              explication: '② est le ballon : il contient le mélange réactionnel (les réactifs et la pierre ponce).' },
            { texte: 'L’élément ③ est :', choix: ['le chauffe-ballon', 'le support élévateur', 'la potence', 'le bécher'], bonne: 0,
              explication: '③ est le chauffe-ballon : il chauffe le mélange.' },
            { texte: 'La flèche ④ indique :', choix: ['la sortie de l’eau', 'l’entrée de l’eau froide', 'la sortie des vapeurs', 'l’entrée des réactifs'], bonne: 1,
              explication: 'L’eau froide entre par le bas du réfrigérant (④) et sort par le haut : le réfrigérant reste plein d’eau froide.' },
          ],
        },
        {
          id: '1-2', genre: 'redaction', points: 1, texte: 'Donne le rôle du chauffage à reflux.',
          attendu: 'Le chauffage augmente la vitesse de la réaction ; le reflux (le réfrigérant à boules) condense les vapeurs qui se forment et les fait retomber dans le ballon : il évite la perte des réactifs et des produits.',
          elements: ['Le chauffage augmente la vitesse de la réaction', 'Le reflux (réfrigérant) condense les vapeurs et évite la perte des réactifs et des produits'],
          correction: ['Le chauffage : il augmente la vitesse de la réaction.',
            'Le reflux : le réfrigérant à boules condense les vapeurs, qui retombent dans le ballon ; on évite la perte des réactifs et des produits.'],
        },
        {
          id: '1-3', genre: 'vf', points: 1, texte: 'Réponds par vrai ou faux.',
          items: [
            { texte: 'La synthèse d’une espèce chimique est sa préparation à partir d’autres espèces chimiques, grâce à une transformation chimique.', vrai: true,
              explication: 'Vrai : c’est la définition de la synthèse.' },
            { texte: 'Les espèces chimiques obtenues à la fin d’une synthèse s’appellent les réactifs.', vrai: false,
              explication: 'Faux : les espèces de départ sont les réactifs ; les espèces obtenues sont les produits.' },
            { texte: 'En CCM, l’éluant est la phase fixe.', vrai: false,
              explication: 'Faux : l’éluant est la phase mobile, il monte le long de la plaque ; la phase fixe est la couche de gel de silice.' },
            { texte: 'Quand les taches sont incolores, on les fait apparaître avec une lampe UV ou avec le diiode : c’est la révélation.', vrai: true,
              explication: 'Vrai : on révèle les taches incolores aux UV ou au diiode I₂.' },
          ],
        },
        { id: '1-4', genre: 'valeur', points: 0.5, texte: 'Calcule le rapport frontal Rf(A) de l’alcool isoamylique.', grandeur: 'Rf(A)', valeur: 0.3, unites: [''],
          correction: ['Rf(A) = h(A)/H = 3/10', 'Rf(A) = 0,3 (sans unité)'] },
        { id: '1-5', genre: 'valeur', points: 0.5, texte: 'Calcule le rapport frontal Rf(B) de l’acétate d’isoamyle.', grandeur: 'Rf(B)', valeur: 0.7, unites: [''],
          correction: ['Rf(B) = h(B)/H = 7/10', 'Rf(B) = 0,7 (sans unité)'] },
        {
          id: '1-6', genre: 'redaction', points: 1, texte: 'Le produit C contient-il l’acétate d’isoamyle ? Est-il pur ? Justifie à l’aide du chromatogramme.',
          attendu: 'Oui : une tache de C est à la même hauteur que la tache de B (même rapport frontal 0,7), donc C contient l’acétate d’isoamyle. C n’est pas pur : il donne deux taches ; l’autre tache est à la même hauteur que celle de A (Rf = 0,3) : il reste de l’alcool isoamylique, un réactif qui n’a pas été consommé.',
          elements: ['C contient l’acétate d’isoamyle : une de ses taches a le même Rf (0,7) que la tache de B', 'C n’est pas pur : deux taches', 'L’autre tache a le même Rf (0,3) que A : il reste de l’alcool isoamylique (réactif)'],
          correction: ['Une tache de C est à la même hauteur que la tache de B (Rf = 0,7) : C contient l’acétate d’isoamyle.',
            'C donne deux taches : il n’est pas pur.', 'Sa deuxième tache a le même Rf que A (0,3) : il reste de l’alcool isoamylique, un réactif.'],
        },
      ],
    },
    {
      id: 'P2', court: 'Chimie 2', titre: 'Chimie 2 — Le modèle de l’atome', minutes: 13,
      intro: 'L’atome de magnésium a pour symbole ²⁴₁₂Mg.',
      donnees: ['Charge élémentaire : e = 1,6 × 10⁻¹⁹ C', 'Masse d’un nucléon : mp ≈ mn ≈ 1,67 × 10⁻²⁷ kg',
        'Les couches K, L et M contiennent au plus 2, 8 et 8 électrons.'],
      questions: [
        {
          id: '2-1', genre: 'qcm', points: 1, texte: 'Pour chaque proposition, choisis la seule réponse juste.',
          items: [
            { texte: 'Le noyau d’un atome est formé :', choix: ['de protons et d’électrons', 'de protons et de neutrons', 'seulement de neutrons', 'd’électrons et de neutrons'], bonne: 1,
              explication: 'Le noyau contient les nucléons : les protons (charge +e) et les neutrons (neutres). Les électrons sont autour du noyau.' },
            { texte: 'La charge du noyau ²⁴₁₂Mg est :', choix: ['+12e', '+24e', '−12e', '0'], bonne: 0,
              explication: 'Le noyau contient Z = 12 protons de charge +e chacun : Q(noyau) = +Z·e = +12e. Les neutrons ne portent pas de charge.' },
            { texte: 'L’ordre de grandeur du rayon d’un atome est :', choix: ['10⁻¹⁵ m', '10⁻¹⁰ m', '10⁻⁵ m', '10⁻²⁰ m'], bonne: 1,
              explication: 'Le rayon d’un atome est de l’ordre de 10⁻¹⁰ m ; celui du noyau, de l’ordre de 10⁻¹⁵ m : environ 10⁵ fois plus petit. L’atome est surtout du vide.' },
            { texte: 'Un isotope de ²⁴₁₂Mg est :', choix: ['²⁴₁₁Na', '²⁶₁₂Mg', '¹²₆C', 'l’ion Mg²⁺'], bonne: 1,
              explication: 'Des isotopes ont le même Z et des A différents : ²⁶₁₂Mg (Z = 12, A = 26) est un isotope de ²⁴₁₂Mg. L’ion Mg²⁺ n’est pas un isotope : il a perdu des électrons, son noyau ne change pas.' },
          ],
        },
        { id: '2-2', genre: 'valeur', points: 0.5, texte: 'Calcule le nombre de neutrons N du noyau de magnésium.', grandeur: 'N', valeur: 12, unites: [''],
          correction: ['N = A − Z = 24 − 12', 'N = 12 neutrons'] },
        { id: '2-3', genre: 'valeur', points: 1, texte: 'Calcule la masse approchée m de l’atome de magnésium.', grandeur: 'm', valeur: 4.0e-26, tolerance: 0.03, unites: ['kg'],
          correction: ['La masse des électrons est négligeable et mp ≈ mn : m ≈ A × mp', 'm ≈ 24 × 1,67 × 10⁻²⁷', 'm ≈ 4,0 × 10⁻²⁶ kg'] },
        {
          id: '2-4', genre: 'redaction', points: 1, texte: 'Donne la structure électronique de l’atome de magnésium, puis nomme sa couche externe et le nombre d’électrons qu’elle porte.',
          attendu: 'L’atome est neutre : il a autant d’électrons que de protons, 12. On remplit K (2), puis L (8), puis M : (K)²(L)⁸(M)². La couche externe est la couche M ; elle porte 2 électrons.',
          elements: ['Nombre d’électrons = Z = 12 (atome neutre)', 'Structure : (K)²(L)⁸(M)²', 'Couche externe : M, avec 2 électrons'],
          correction: ['L’atome est neutre : nombre d’électrons = Z = 12.', 'On remplit K, puis L, puis M : (K)²(L)⁸(M)².', 'La couche externe est M : elle porte 2 électrons.'],
        },
        {
          id: '2-5', genre: 'vf', points: 1, texte: 'L’atome de magnésium donne l’ion Mg²⁺. Réponds par vrai ou faux.',
          items: [
            { texte: 'L’ion Mg²⁺ se forme quand l’atome Mg gagne deux électrons.', vrai: false,
              explication: 'Faux : il perd deux électrons ; il a alors deux charges positives de plus que de charges négatives.' },
            { texte: 'L’ion Mg²⁺ est un cation.', vrai: true,
              explication: 'Vrai : un ion chargé positivement s’appelle un cation.' },
            { texte: 'L’ion Mg²⁺ possède 10 électrons.', vrai: true,
              explication: 'Vrai : 12 − 2 = 10 électrons ; sa structure est (K)²(L)⁸.' },
            { texte: '²⁴₁₂Mg, ²⁶₁₂Mg et l’ion Mg²⁺ appartiennent au même élément chimique, le magnésium.', vrai: true,
              explication: 'Vrai : ils ont tous le même numéro atomique Z = 12, qui caractérise l’élément chimique.' },
          ],
        },
        { id: '2-6', genre: 'valeur', points: 0.5, texte: 'Calcule la charge électrique q de l’ion Mg²⁺, en coulombs.', grandeur: 'q', valeur: 3.2e-19, unites: ['c'],
          correction: ['L’ion a perdu deux électrons : q = +2e', 'q = 2 × 1,6 × 10⁻¹⁹', 'q = 3,2 × 10⁻¹⁹ C'] },
      ],
    },
    {
      id: 'P3', court: 'Physique 1', titre: 'Physique 1 — Le mouvement', minutes: 16,
      intro: 'Un autoporteur glisse sur une table horizontale. On enregistre les positions successives M₀, M₁, M₂… de son point central M, '
        + 'à intervalles de temps égaux τ = 20 ms (figure 1). Pour les questions 3-6 et 3-7, on étudie un autre mouvement : '
        + 'celui d’un point M du bord d’un disque qui tourne (figure 2).',
      figures: [ENREGISTREMENT, CERCLE],
      donnees: ['τ = 20 ms ; deux positions successives sont distantes de 4 cm.', 'Vitesse moyenne : vm = d/Δt ; vitesse instantanée : vᵢ = Mᵢ₋₁Mᵢ₊₁/(2τ)',
        'Disque : R = 0,5 m ; v = 1 m/s ; ω = v/R ; T = 2π/ω'],
      questions: [
        {
          id: '3-1', genre: 'qcm', points: 1, texte: 'Pour chaque proposition, choisis la seule réponse juste.',
          items: [
            { texte: 'Un voyageur est assis dans un train qui roule. Il est :', choix: ['au repos par rapport au sol', 'en mouvement par rapport au train', 'au repos par rapport au train', 'en mouvement par rapport à tous les référentiels'], bonne: 2,
              explication: 'Le mouvement est relatif : le voyageur est au repos par rapport au train, et en mouvement par rapport au sol. Il faut toujours préciser le référentiel.' },
            { texte: 'La trajectoire d’un point est :', choix: ['la distance qu’il parcourt', 'l’ensemble des positions successives qu’il occupe au cours du mouvement', 'sa vitesse', 'la durée de son mouvement'], bonne: 1,
              explication: 'La trajectoire est l’ensemble des positions successives occupées par le point ; elle peut être rectiligne, circulaire ou curviligne.' },
            { texte: 'Une vitesse de 72 km/h est égale à :', choix: ['20 m/s', '72 m/s', '7,2 m/s', '259,2 m/s'], bonne: 0,
              explication: '1 m/s = 3,6 km/h, donc 72 km/h = 72/3,6 = 20 m/s.' },
            { texte: 'Le vecteur vitesse instantanée d’un point a pour direction :', choix: ['la perpendiculaire à la trajectoire', 'la tangente à la trajectoire en ce point', 'toujours la verticale', 'la droite qui va vers le centre'], bonne: 1,
              explication: 'Le vecteur vitesse a pour origine la position du point, pour direction la tangente à la trajectoire, pour sens celui du mouvement.' },
          ],
        },
        { id: '3-2', genre: 'valeur', points: 1, texte: 'Calcule la vitesse moyenne vm du point M entre les positions M₁ et M₅ (en m/s).', grandeur: 'vm', valeur: 2, unites: ['m/s', 'm.s', 'm·s', 'm s'],
          correction: ['vm = M₁M₅/(t₅ − t₁) = M₁M₅/(4τ)', 'M₁M₅ = 4 × 4 cm = 16 cm = 0,16 m ; 4τ = 4 × 20 ms = 80 ms = 0,08 s', 'vm = 0,16/0,08 = 2 m/s'] },
        { id: '3-3', genre: 'valeur', points: 1, texte: 'Calcule la vitesse instantanée v₃ du point M à la position M₃ (en m/s).', grandeur: 'v₃', valeur: 2, unites: ['m/s', 'm.s', 'm·s', 'm s'],
          correction: ['v₃ = M₂M₄/(2τ)', 'M₂M₄ = 2 × 4 cm = 8 cm = 0,08 m ; 2τ = 40 ms = 0,04 s', 'v₃ = 0,08/0,04 = 2 m/s'] },
        {
          id: '3-4', genre: 'redaction', points: 1, texte: 'Quelle est la nature du mouvement du point M ? Justifie.',
          attendu: 'Le mouvement est rectiligne uniforme : la trajectoire est une droite (les positions sont alignées) et la vitesse est constante (les distances parcourues pendant des durées égales τ sont égales, 4 cm ; v₃ = vm = 2 m/s).',
          elements: ['Trajectoire rectiligne : les positions sont alignées', 'Vitesse constante : distances égales pendant des durées égales (v₃ = vm = 2 m/s)', 'Conclusion : mouvement rectiligne uniforme'],
          correction: ['Les positions sont alignées : la trajectoire est rectiligne.', 'Pendant chaque durée τ, M parcourt 4 cm : la vitesse est constante (v₃ = vm = 2 m/s).',
            'Le mouvement de M est rectiligne uniforme.'],
        },
        {
          id: '3-5', genre: 'redaction', points: 1,
          texte: 'On prend M₀ comme origine de l’axe (Ox), orienté dans le sens du mouvement, et l’instant où M passe en M₁ comme origine des temps (t = 0). Écris l’équation horaire x(t) du mouvement de M.',
          attendu: 'x(t) = v·t + x₀ avec v = 2 m/s et x₀ = M₀M₁ = 4 cm = 0,04 m (abscisse de M à t = 0) : x(t) = 2t + 0,04 (x en m, t en s).',
          elements: ['La forme x(t) = v·t + x₀', 'v = 2 m/s et x₀ = M₀M₁ = 0,04 m', 'x(t) = 2t + 0,04 (en m, t en s)'],
          correction: ['Mouvement rectiligne uniforme : x(t) = v·t + x₀', 'v = 2 m/s ; à t = 0, M est en M₁ : x₀ = M₀M₁ = 4 cm = 0,04 m', 'x(t) = 2t + 0,04 (x en m, t en s)'],
        },
        { id: '3-6', genre: 'valeur', points: 0.5, texte: 'Figure 2 : calcule la vitesse angulaire ω du point M du disque.', grandeur: 'ω', valeur: 2, unites: ['rad/s', 'rad.s', 'rad·s', 'rad s'],
          correction: ['ω = v/R = 1/0,5', 'ω = 2 rad/s'] },
        { id: '3-7', genre: 'valeur', points: 0.5, texte: 'Figure 2 : calcule la période T du mouvement du point M.', grandeur: 'T', valeur: 3.14, unites: ['s'],
          correction: ['T = 2π/ω = 2π/2', 'T = π ≈ 3,14 s'] },
      ],
    },
    {
      id: 'P4', court: 'Physique 2', titre: 'Physique 2 — Principe d’inertie et centre d’inertie', minutes: 12,
      intro: 'Un palet de masse m = 0,5 kg glisse sans frottement sur une glace horizontale ; son centre d’inertie G a un mouvement rectiligne uniforme. '
        + 'Pour les questions 4-4 et 4-5, on étudie un marteau formé d’un manche de masse m₁ = 200 g et d’une tête de masse m₂ = 600 g (figure).',
      figures: [MARTEAU],
      donnees: ['g = 10 N/kg ; poids : P = m·g', 'Centre d’inertie d’un système de deux corps : G₁G = m₂/(m₁ + m₂) × G₁G₂'],
      questions: [
        {
          id: '4-1', genre: 'vf', points: 1, texte: 'Réponds par vrai ou faux.',
          items: [
            { texte: 'Un solide est pseudo-isolé quand la somme vectorielle des forces qui s’exercent sur lui est nulle.', vrai: true,
              explication: 'Vrai : ΣF⃗ = 0⃗, les forces se compensent.' },
            { texte: 'Le palet qui glisse sur la glace n’est soumis qu’à son poids.', vrai: false,
              explication: 'Faux : il est soumis à son poids P⃗ et à la réaction R⃗ de la glace, qui se compensent.' },
            { texte: 'D’après le principe d’inertie, le centre d’inertie d’un solide pseudo-isolé est forcément au repos.', vrai: false,
              explication: 'Faux : il est au repos OU en mouvement rectiligne uniforme (vecteur vitesse constant).' },
            { texte: 'Pour un solide homogène, le centre d’inertie est le point d’intersection de ses axes de symétrie.', vrai: true,
              explication: 'Vrai : par exemple, le centre d’une boule ou d’un disque homogène.' },
          ],
        },
        {
          id: '4-2', genre: 'redaction', points: 1, texte: 'Fais l’inventaire des forces qui s’exercent sur le palet, puis montre, à l’aide du principe d’inertie, que ces forces se compensent.',
          attendu: 'Système : le palet. Forces : son poids P⃗ (vertical, vers le bas) et la réaction R⃗ de la glace (perpendiculaire à la glace, vers le haut, car il n’y a pas de frottement). G a un mouvement rectiligne uniforme : d’après le principe d’inertie, le palet est pseudo-isolé, donc P⃗ + R⃗ = 0⃗ : les deux forces se compensent.',
          elements: ['Forces : le poids P⃗ et la réaction R⃗ de la glace', 'G en mouvement rectiligne uniforme → d’après le principe d’inertie, le palet est pseudo-isolé', 'P⃗ + R⃗ = 0⃗ : les forces se compensent'],
          correction: ['Système : le palet. Forces : le poids P⃗ et la réaction R⃗ de la glace (perpendiculaire à la glace, sans frottement).',
            'G a un mouvement rectiligne uniforme : d’après le principe d’inertie, le palet est pseudo-isolé.', 'Donc P⃗ + R⃗ = 0⃗ : le poids et la réaction se compensent.'],
        },
        { id: '4-3', genre: 'valeur', points: 0.5, texte: 'Calcule l’intensité R de la réaction de la glace sur le palet.', grandeur: 'R', valeur: 5, unites: ['n'],
          correction: ['P⃗ + R⃗ = 0⃗, donc R = P = m·g', 'R = 0,5 × 10', 'R = 5 N'] },
        { id: '4-4', genre: 'valeur', points: 1, texte: 'Calcule la distance G₁G entre le centre d’inertie du manche et le centre d’inertie G du marteau (en cm).', grandeur: 'G₁G', valeur: 15, unites: ['cm'],
          correction: ['G₁G = m₂/(m₁ + m₂) × G₁G₂', 'G₁G = 600/(200 + 600) × 20', 'G₁G = 15 cm'] },
        {
          id: '4-5', genre: 'qcm', points: 0.5, texte: 'Le centre d’inertie G du marteau se trouve :',
          items: [{ texte: 'sur le segment G₁G₂,', choix: ['au milieu de G₁G₂', 'plus près de G₂ (la tête)', 'plus près de G₁ (le manche)', 'en dehors du segment G₁G₂'], bonne: 1,
            explication: 'G₁G = 15 cm et GG₂ = 5 cm : G est plus près de la tête, la partie la plus lourde (600 g contre 200 g).' }],
        },
      ],
    },
  ] as PartieExamen[],
};

/**
 * Les voix de l'évaluation (voix Bodi, générées par lot : cours/tc_tcf_examen_voix.json), servies à
 * `/media/audio/courses/tc_tcf_examen/<clé>.mp3`. Rempli après la génération avec les pistes qui existent vraiment
 * (même script que `scripts/brancher_voix_examen.py`) ; une piste absente = pas de bouton.
 */
export const VOIX_TCF: string[] = [];
