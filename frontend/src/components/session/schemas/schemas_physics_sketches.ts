import type { ScientificSchema } from './types';
import { BAC_PENCIL as P, BAC_PENCIL_FONT as FONT, BAC_PENCIL_PALETTE_ID, pencilDefs } from './pencilPalette';

const COURSE = 'phys_ch1_waves';
const CHAPTER = 'Ondes mécaniques progressives';
const LESSON = 'Propagation, retard et célérité';
const SOURCE_URL = 'https://www.youtube.com/watch?v=E79tE5gmdrk';
const SOURCE_TEACHER = 'Jihad El Goufifa';
const SOURCE_TITLE = 'Physique-Chimie 2Bac - 1: Les ondes mécaniques progressives (Cours)';
const REQUEST_WORDS = ['croquis', 'dessine', 'dessin au tableau', 'schématise', 'rsem lia', 'rassam lia', 'رسم ليا'];

export const PHYS_CROQUIS_PROPAGATION_LOCALE: ScientificSchema = {
  id: 'phys_croquis_propagation_locale',
  title: 'Croquis au crayon — Propagation et mouvement local',
  subject: 'physics',
  keywords: ['onde mécanique progressive', 'perturbation corde', 'propagation sans transport de matière', 'mouvement local', 'impulsion', ...REQUEST_WORDS],
  metadata: {
    courseId: 'phys_ch1_waves', chapter: 'Ondes mécaniques progressives', lesson: 'Propagation, retard et célérité',
    visualStyle: 'pencil', resourceRole: 'teacher_sketch', paletteId: 'bac-pencil-v1',
    sourceUrl: 'https://www.youtube.com/watch?v=E79tE5gmdrk', sourceTeacher: 'Jihad El Goufifa',
    sourceVideoTitle: 'Physique-Chimie 2Bac - 1: Les ondes mécaniques progressives (Cours)', auditStatus: 'video_reviewed',
    sourceTimecodes: ['09:30–12:00 · impulsion sur une corde et directions du mouvement'],
    learningObjectives: ['Distinguer propagation de la perturbation et mouvement local du milieu', 'Montrer l’absence de transport global de matière'],
    llmIntents: ['dessiner une impulsion qui se propage', 'expliquer ce qui bouge dans une onde mécanique'],
    drawingSteps: ['Tracer la position d’équilibre', 'Dessiner l’impulsion à deux dates', 'Ajouter la flèche de propagation', 'Montrer l’oscillation verticale d’un point P'],
  },
  category: 'process', viewBox: '0 0 900 520',
  layers: [
    { id: 'milieu', label: 'Milieu matériel', delay: 0, svgContent: `${pencilDefs('phys-prop')}
      <path d="M70 300 C180 300 215 190 300 300 S420 300 520 300 S700 300 830 300" fill="none" stroke="${P.ink}" stroke-width="4"/>
      <line x1="65" y1="300" x2="835" y2="300" stroke="${P.muted}" stroke-width="2" stroke-dasharray="9 8"/>
      <circle cx="260" cy="240" r="8" fill="${P.control}"/><text x="260" y="220" text-anchor="middle" font-size="20" fill="${P.control}" font-family="${FONT}">P</text>
      <text x="450" y="355" text-anchor="middle" font-size="21" fill="${P.muted}" font-family="${FONT}">la corde reste sur place globalement</text>` },
    { id: 'directions', label: 'Deux mouvements', delay: 550, svgContent: `
      <path d="M330 135 C455 105 590 105 720 135" fill="none" stroke="${P.positive}" stroke-width="4" marker-end="url(#phys-prop-green-arrow)"/>
      <text x="525" y="95" text-anchor="middle" font-size="24" fill="${P.positive}" font-family="${FONT}">la perturbation se propage →</text>
      <path d="M260 270 L260 180 M260 260 L260 345" fill="none" stroke="${P.control}" stroke-width="3" marker-end="url(#phys-prop-arrow)"/>
      <text x="125" y="210" font-size="21" fill="${P.control}" font-family="${FONT}">P oscille localement</text>
      <text x="450" y="445" text-anchor="middle" font-size="26" fill="${P.ink}" font-family="${FONT}">énergie + information  ≠  transport de matière</text>` },
  ],
  annotations: [
    { id: 'pulse', x: 145, y: 165, width: 190, height: 155, label: 'Perturbation', description: 'La forme progresse de proche en proche dans le milieu matériel.', color: P.positive },
    { id: 'point', x: 230, y: 175, width: 70, height: 180, label: 'Point P', description: 'P s’écarte de sa position d’équilibre puis y revient.', color: P.control },
  ],
  highlights: [{ id: 'two_motions', cx: 450, cy: 240, radius: 205, label: 'Propagation ≠ mouvement local' }],
};

export const PHYS_CROQUIS_TRANSVERSALE_LONGITUDINALE: ScientificSchema = {
  id: 'phys_croquis_transversale_longitudinale',
  title: 'Croquis au crayon — Onde transversale ou longitudinale',
  subject: 'physics',
  keywords: ['onde transversale', 'onde longitudinale', 'corde ressort', 'compression dilatation', 'directions propagation perturbation', ...REQUEST_WORDS],
  metadata: {
    courseId: 'phys_ch1_waves', chapter: 'Ondes mécaniques progressives', lesson: 'Propagation, retard et célérité',
    visualStyle: 'pencil', resourceRole: 'teacher_sketch', paletteId: 'bac-pencil-v1',
    sourceUrl: 'https://www.youtube.com/watch?v=E79tE5gmdrk', sourceTeacher: 'Jihad El Goufifa',
    sourceVideoTitle: 'Physique-Chimie 2Bac - 1: Les ondes mécaniques progressives (Cours)', auditStatus: 'video_reviewed',
    sourceTimecodes: ['09:30–12:00 · corde transversale', '29:00–32:00 · ressort et compression longitudinale'],
    learningObjectives: ['Comparer direction de propagation et direction du mouvement local', 'Classer une onde mécanique'],
    llmIntents: ['comparer onde transversale et longitudinale', 'dessiner corde et ressort avec les directions'],
    drawingSteps: ['Séparer le tableau en deux', 'Tracer la corde et l’impulsion', 'Tracer le ressort et une compression', 'Ajouter les deux paires de flèches'],
  },
  category: 'comparison', viewBox: '0 0 900 520',
  layers: [
    { id: 'supports', label: 'Corde et ressort', delay: 0, svgContent: `${pencilDefs('phys-tl')}
      <line x1="450" y1="55" x2="450" y2="470" stroke="${P.muted}" stroke-width="2" stroke-dasharray="8 8"/>
      <text x="225" y="70" text-anchor="middle" font-size="27" fill="${P.observed}" font-family="${FONT}">TRANSVERSALE</text>
      <path d="M60 285 C125 285 150 150 225 285 S330 285 405 285" fill="none" stroke="${P.ink}" stroke-width="4"/>
      <text x="675" y="70" text-anchor="middle" font-size="27" fill="${P.input}" font-family="${FONT}">LONGITUDINALE</text>
      <path d="M500 285 q12 -55 24 0 q12 55 24 0 q7 -55 14 0 q7 55 14 0 q7 -55 14 0 q7 55 14 0 q20 -55 40 0 q20 55 40 0 q20 -55 40 0 q20 55 40 0 q20 -55 40 0" fill="none" stroke="${P.ink}" stroke-width="4"/>
      <text x="560" y="335" font-size="18" fill="${P.control}" font-family="${FONT}">compression</text>` },
    { id: 'fleches', label: 'Directions', delay: 550, svgContent: `
      <path d="M90 120 L360 120" stroke="${P.positive}" stroke-width="4" marker-end="url(#phys-tl-green-arrow)"/><text x="225" y="105" text-anchor="middle" font-size="19" fill="${P.positive}" font-family="${FONT}">propagation</text>
      <path d="M225 245 L225 150" stroke="${P.control}" stroke-width="4" marker-end="url(#phys-tl-arrow)"/><text x="225" y="380" text-anchor="middle" font-size="20" fill="${P.control}" font-family="${FONT}">déplacement ⟂ propagation</text>
      <path d="M520 120 L800 120" stroke="${P.positive}" stroke-width="4" marker-end="url(#phys-tl-green-arrow)"/><text x="660" y="105" text-anchor="middle" font-size="19" fill="${P.positive}" font-family="${FONT}">propagation</text>
      <path d="M555 220 L710 220" stroke="${P.control}" stroke-width="4" marker-end="url(#phys-tl-arrow)"/><text x="675" y="380" text-anchor="middle" font-size="20" fill="${P.control}" font-family="${FONT}">déplacement ∥ propagation</text>` },
  ],
  annotations: [
    { id: 'transverse', x: 45, y: 45, width: 375, height: 370, label: 'Transversale', description: 'Le mouvement local est perpendiculaire à la direction de propagation.', color: P.observed },
    { id: 'longitudinal', x: 480, y: 45, width: 370, height: 370, label: 'Longitudinale', description: 'Le mouvement local est parallèle à la direction de propagation.', color: P.input },
  ],
  highlights: [{ id: 'directions', cx: 450, cy: 255, radius: 235, label: 'Comparer les directions' }],
};

export const PHYS_CROQUIS_SON_MILIEU: ScientificSchema = {
  id: 'phys_croquis_son_milieu',
  title: 'Croquis au crayon — Le son a besoin d’un milieu',
  subject: 'physics',
  keywords: ['son milieu matériel', 'cloche à vide', 'son dans le vide', 'diapason bille', 'onde sonore', ...REQUEST_WORDS],
  metadata: {
    courseId: 'phys_ch1_waves', chapter: 'Ondes mécaniques progressives', lesson: 'Propagation, retard et célérité',
    visualStyle: 'pencil', resourceRole: 'teacher_sketch', paletteId: 'bac-pencil-v1',
    sourceUrl: 'https://www.youtube.com/watch?v=E79tE5gmdrk', sourceTeacher: 'Jihad El Goufifa',
    sourceVideoTitle: 'Physique-Chimie 2Bac - 1: Les ondes mécaniques progressives (Cours)', auditStatus: 'video_reviewed',
    sourceTimecodes: ['18:00–22:00 · sonnette sous cloche et diapason avec bille'],
    learningObjectives: ['Établir que le son est une onde mécanique', 'Relier vibration de la source et mise en mouvement du milieu'],
    llmIntents: ['dessiner l’expérience de la cloche à vide', 'dessiner le diapason et la bille'],
    drawingSteps: ['Tracer la cloche et la sonnette', 'Représenter l’air puis son retrait', 'Tracer le diapason et la bille', 'Conclure que le son exige un milieu matériel'],
  },
  category: 'comparison', viewBox: '0 0 900 520',
  layers: [
    { id: 'cloche', label: 'Cloche à vide', delay: 0, svgContent: `${pencilDefs('phys-son')}
      <text x="235" y="65" text-anchor="middle" font-size="25" fill="${P.observed}" font-family="${FONT}">Sonnette sous cloche</text>
      <path d="M95 390 L375 390 M125 390 C120 260 135 120 235 110 C335 120 350 260 345 390" fill="none" stroke="${P.ink}" stroke-width="4"/>
      <path d="M195 280 Q235 230 275 280 L275 335 L195 335Z" fill="none" stroke="${P.control}" stroke-width="4"/>
      <circle cx="235" cy="345" r="9" fill="${P.control}"/>
      <g fill="${P.observed}"><circle cx="165" cy="190" r="4"/><circle cx="285" cy="185" r="4"/><circle cx="180" cy="240" r="4"/><circle cx="310" cy="260" r="4"/></g>
      <path d="M110 420 L360 420" stroke="${P.muted}" stroke-width="3"/><text x="235" y="465" text-anchor="middle" font-size="20" fill="${P.alert}" font-family="${FONT}">air retiré → son s’atténue</text>` },
    { id: 'diapason', label: 'Diapason', delay: 600, svgContent: `
      <text x="665" y="65" text-anchor="middle" font-size="25" fill="${P.input}" font-family="${FONT}">Diapason + bille</text>
      <path d="M590 130 L590 315 Q590 360 640 360 Q690 360 690 315 L690 130 M640 360 L640 445" fill="none" stroke="${P.ink}" stroke-width="5"/>
      <path d="M570 160 Q550 195 570 230 M710 160 Q730 195 710 230" fill="none" stroke="${P.positive}" stroke-width="3"/>
      <line x1="760" y1="120" x2="760" y2="260" stroke="${P.muted}" stroke-width="2"/><circle cx="760" cy="285" r="20" fill="none" stroke="${P.control}" stroke-width="4"/>
      <path d="M710 280 L738 285" stroke="${P.alert}" stroke-width="4" marker-end="url(#phys-son-alert-arrow)"/>
      <text x="665" y="475" text-anchor="middle" font-size="20" fill="${P.positive}" font-family="${FONT}">la source vibre et met le milieu en mouvement</text>` },
  ],
  annotations: [
    { id: 'vacuum', x: 90, y: 85, width: 295, height: 390, label: 'Cloche à vide', description: 'La sonnette continue de vibrer mais le son reçu diminue lorsque l’air est retiré.', color: P.alert },
    { id: 'fork', x: 520, y: 85, width: 330, height: 390, label: 'Diapason', description: 'Le déplacement de la bille rend visible la vibration de la source sonore.', color: P.input },
  ],
  highlights: [{ id: 'matter', cx: 450, cy: 275, radius: 235, label: 'Le son exige de la matière' }],
};

export const PHYS_CROQUIS_SUPERPOSITION: ScientificSchema = {
  id: 'phys_croquis_superposition',
  title: 'Croquis au crayon — Superposition de deux perturbations',
  subject: 'physics',
  keywords: ['superposition ondes', 'deux perturbations se croisent', 'interférence impulsions', 'ondes après croisement', ...REQUEST_WORDS],
  metadata: {
    courseId: 'phys_ch1_waves', chapter: 'Ondes mécaniques progressives', lesson: 'Propagation, retard et célérité',
    visualStyle: 'pencil', resourceRole: 'teacher_sketch', paletteId: 'bac-pencil-v1',
    sourceUrl: 'https://www.youtube.com/watch?v=E79tE5gmdrk', sourceTeacher: 'Jihad El Goufifa',
    sourceVideoTitle: 'Physique-Chimie 2Bac - 1: Les ondes mécaniques progressives (Cours)', auditStatus: 'video_reviewed',
    sourceTimecodes: ['23:30–27:00 · approche, superposition puis séparation de deux impulsions'],
    learningObjectives: ['Appliquer le principe de superposition', 'Montrer que les perturbations poursuivent leur propagation après le croisement'],
    llmIntents: ['dessiner deux impulsions qui se croisent', 'expliquer la superposition algébrique'],
    drawingSteps: ['Tracer trois lignes temporelles', 'Dessiner les impulsions avant le croisement', 'Additionner les déformations au croisement', 'Replacer les impulsions après le croisement'],
  },
  category: 'process', viewBox: '0 0 900 520',
  layers: [
    { id: 'avant', label: 'Avant', delay: 0, svgContent: `${pencilDefs('phys-sup')}
      <text x="75" y="105" font-size="21" fill="${P.muted}" font-family="${FONT}">avant</text><line x1="160" y1="100" x2="840" y2="100" stroke="${P.muted}" stroke-width="2"/>
      <path d="M180 100 L245 100 Q275 35 305 100 L430 100" fill="none" stroke="${P.input}" stroke-width="4"/>
      <path d="M500 100 L620 100 Q650 165 680 100 L820 100" fill="none" stroke="${P.alert}" stroke-width="4"/>
      <path d="M315 55 L430 55" stroke="${P.positive}" stroke-width="3" marker-end="url(#phys-sup-green-arrow)"/><path d="M685 175 L570 175" stroke="${P.positive}" stroke-width="3" marker-end="url(#phys-sup-green-arrow)"/>` },
    { id: 'pendant', label: 'Pendant', delay: 500, svgContent: `
      <text x="65" y="275" font-size="21" fill="${P.muted}" font-family="${FONT}">pendant</text><line x1="160" y1="270" x2="840" y2="270" stroke="${P.muted}" stroke-width="2"/>
      <path d="M250 270 L390 270 Q430 235 450 270 Q470 305 510 270 L650 270" fill="none" stroke="${P.control}" stroke-width="5"/>
      <text x="700" y="240" font-size="19" fill="${P.control}" font-family="${FONT}">somme algébrique</text>` },
    { id: 'apres', label: 'Après', delay: 1000, svgContent: `
      <text x="75" y="445" font-size="21" fill="${P.muted}" font-family="${FONT}">après</text><line x1="160" y1="440" x2="840" y2="440" stroke="${P.muted}" stroke-width="2"/>
      <path d="M180 440 L300 440 Q330 505 360 440 L480 440" fill="none" stroke="${P.alert}" stroke-width="4"/>
      <path d="M520 440 L640 440 Q670 375 700 440 L820 440" fill="none" stroke="${P.input}" stroke-width="4"/>
      <text x="450" y="505" text-anchor="middle" font-size="20" fill="${P.positive}" font-family="${FONT}">formes retrouvées · propagation poursuivie</text>` },
  ],
  annotations: [{ id: 'sum', x: 235, y: 205, width: 465, height: 120, label: 'Superposition', description: 'Au croisement, l’élongation résultante est la somme algébrique des deux élongations.', color: P.control }],
  highlights: [{ id: 'crossing', cx: 450, cy: 270, radius: 150, label: 'Croisement temporaire' }],
};

export const PHYS_CROQUIS_RESSORT_CELERITE: ScientificSchema = {
  id: 'phys_croquis_ressort_celerite',
  title: 'Croquis au crayon — Mesurer la célérité sur un ressort',
  subject: 'physics',
  keywords: ['ressort célérité', 'onde sur ressort', 'capteurs retard distance', 'mesure vitesse propagation', 'compression ressort', ...REQUEST_WORDS],
  metadata: {
    courseId: 'phys_ch1_waves', chapter: 'Ondes mécaniques progressives', lesson: 'Propagation, retard et célérité',
    visualStyle: 'pencil', resourceRole: 'teacher_sketch', paletteId: 'bac-pencil-v1',
    sourceUrl: 'https://www.youtube.com/watch?v=E79tE5gmdrk', sourceTeacher: 'Jihad El Goufifa',
    sourceVideoTitle: 'Physique-Chimie 2Bac - 1: Les ondes mécaniques progressives (Cours)', auditStatus: 'video_reviewed',
    sourceTimecodes: ['29:00–33:00 · ressort, règle et chronométrage de la propagation'],
    learningObjectives: ['Relier distance, retard et célérité', 'Identifier les grandeurs à mesurer expérimentalement'],
    llmIntents: ['dessiner le montage de mesure sur ressort', 'expliquer v égale d sur tau'],
    drawingSteps: ['Tracer le ressort horizontal', 'Placer A et B', 'Coter la distance d', 'Ajouter les dates et calculer le retard'],
  },
  category: 'diagram', viewBox: '0 0 900 520',
  layers: [
    { id: 'montage', label: 'Montage', delay: 0, svgContent: `${pencilDefs('phys-res')}
      <path d="M85 250 q15 -70 30 0 q15 70 30 0 q15 -70 30 0 q15 70 30 0 q15 -70 30 0 q15 70 30 0 q15 -70 30 0 q15 70 30 0 q15 -70 30 0 q15 70 30 0 q15 -70 30 0 q15 70 30 0 q15 -70 30 0 q15 70 30 0 q15 -70 30 0 q15 70 30 0 q15 -70 30 0 q15 70 30 0 q15 -70 30 0 q15 70 30 0 q15 -70 30 0 q15 70 30 0 q15 -70 30 0 q15 70 30 0" fill="none" stroke="${P.ink}" stroke-width="4"/>
      <path d="M105 135 L790 135" stroke="${P.positive}" stroke-width="4" marker-end="url(#phys-res-green-arrow)"/><text x="450" y="105" text-anchor="middle" font-size="22" fill="${P.positive}" font-family="${FONT}">compression qui se propage</text>
      <line x1="260" y1="185" x2="260" y2="360" stroke="${P.observed}" stroke-width="4"/><line x1="680" y1="185" x2="680" y2="360" stroke="${P.control}" stroke-width="4"/>
      <text x="260" y="390" text-anchor="middle" font-size="24" fill="${P.observed}" font-family="${FONT}">A · tA</text><text x="680" y="390" text-anchor="middle" font-size="24" fill="${P.control}" font-family="${FONT}">B · tB</text>` },
    { id: 'mesure', label: 'Mesure', delay: 650, svgContent: `
      <path d="M270 435 L670 435" stroke="${P.ink}" stroke-width="3" marker-end="url(#phys-res-arrow)"/><path d="M670 450 L270 450" stroke="${P.ink}" stroke-width="3" marker-end="url(#phys-res-arrow)"/>
      <text x="470" y="425" text-anchor="middle" font-size="23" fill="${P.ink}" font-family="${FONT}">d = AB</text>
      <rect x="335" y="310" width="270" height="82" rx="18" fill="none" stroke="${P.reference}" stroke-width="3"/>
      <text x="470" y="345" text-anchor="middle" font-size="23" fill="${P.reference}" font-family="${FONT}">τ = tB − tA</text><text x="470" y="377" text-anchor="middle" font-size="26" fill="${P.positive}" font-family="${FONT}">v = d / τ</text>` },
  ],
  annotations: [{ id: 'measure', x: 225, y: 170, width: 500, height: 295, label: 'Mesure de propagation', description: 'La distance AB est connue ; le retard vaut tB − tA. Les unités doivent être converties en m et s.', color: P.observed }],
  highlights: [{ id: 'formula', cx: 470, cy: 350, radius: 145, label: 'v = d/τ' }],
};

export const PHYS_CROQUIS_CORDE_POULIE: ScientificSchema = {
  id: 'phys_croquis_corde_poulie',
  title: 'Croquis au crayon — Corde tendue par une masse',
  subject: 'physics',
  keywords: ['corde poulie masse', 'tension corde', 'célérité tension masse linéique', 'v racine T sur mu', 'poids Mg', ...REQUEST_WORDS],
  metadata: {
    courseId: 'phys_ch1_waves', chapter: 'Ondes mécaniques progressives', lesson: 'Propagation, retard et célérité',
    visualStyle: 'pencil', resourceRole: 'teacher_sketch', paletteId: 'bac-pencil-v1',
    sourceUrl: 'https://www.youtube.com/watch?v=E79tE5gmdrk', sourceTeacher: 'Jihad El Goufifa',
    sourceVideoTitle: 'Physique-Chimie 2Bac - 1: Les ondes mécaniques progressives (Cours)', auditStatus: 'video_reviewed',
    sourceTimecodes: ['44:00–51:00 · corde de longueur L, poulie, masse et bilan des forces'],
    learningObjectives: ['Relier la célérité à la tension et à la masse linéique', 'Déduire la tension du poids de la masse suspendue'],
    llmIntents: ['dessiner corde poulie masse suspendue', 'expliquer l’effet de la tension sur la célérité'],
    drawingSteps: ['Tracer la corde et la poulie', 'Suspendre la masse M', 'Ajouter T et P', 'Écrire T voisin de Mg puis v égale racine de T sur mu'],
  },
  category: 'diagram', viewBox: '0 0 900 520',
  layers: [
    { id: 'montage', label: 'Corde et poulie', delay: 0, svgContent: `${pencilDefs('phys-poulie')}
      <line x1="80" y1="210" x2="690" y2="210" stroke="${P.ink}" stroke-width="5"/><circle cx="720" cy="210" r="34" fill="none" stroke="${P.muted}" stroke-width="4"/>
      <path d="M690 210 Q720 176 754 210 L754 370" fill="none" stroke="${P.ink}" stroke-width="5"/>
      <rect x="700" y="370" width="108" height="90" rx="8" fill="none" stroke="${P.control}" stroke-width="4"/><text x="754" y="425" text-anchor="middle" font-size="28" fill="${P.control}" font-family="${FONT}">M</text>
      <path d="M100 165 L670 165" stroke="${P.positive}" stroke-width="4" marker-end="url(#phys-poulie-green-arrow)"/><text x="385" y="135" text-anchor="middle" font-size="21" fill="${P.positive}" font-family="${FONT}">onde sur la corde</text>
      <path d="M100 260 L670 260" stroke="${P.muted}" stroke-width="3" marker-end="url(#phys-poulie-arrow)"/><text x="385" y="295" text-anchor="middle" font-size="21" fill="${P.muted}" font-family="${FONT}">L</text>` },
    { id: 'forces', label: 'Forces et relation', delay: 650, svgContent: `
      <path d="M754 375 L754 305" stroke="${P.input}" stroke-width="4" marker-end="url(#phys-poulie-arrow)"/><text x="775" y="325" font-size="22" fill="${P.input}" font-family="${FONT}">T</text>
      <path d="M754 455 L754 505" stroke="${P.alert}" stroke-width="4" marker-end="url(#phys-poulie-alert-arrow)"/><text x="780" y="500" font-size="22" fill="${P.alert}" font-family="${FONT}">P = Mg</text>
      <rect x="125" y="340" width="455" height="115" rx="20" fill="none" stroke="${P.reference}" stroke-width="3"/>
      <text x="352" y="382" text-anchor="middle" font-size="25" fill="${P.ink}" font-family="${FONT}">à l’équilibre : T ≈ Mg</text>
      <text x="352" y="430" text-anchor="middle" font-size="30" fill="${P.positive}" font-family="${FONT}">v = √(T / μ)</text>` },
  ],
  annotations: [{ id: 'tension', x: 660, y: 160, width: 170, height: 345, label: 'Masse suspendue', description: 'À l’équilibre et avec une poulie idéale, la tension de la corde est égale au poids Mg.', color: P.control }],
  highlights: [{ id: 'law', cx: 350, cy: 400, radius: 175, label: 'Tension et inertie linéique' }],
};

export const PHYS_CROQUIS_RETARD: ScientificSchema = {
  id: 'phys_croquis_retard',
  title: 'Croquis au crayon — Retard entre la source S et le point M',
  subject: 'physics',
  keywords: ['retard onde source point M', 'tau SM sur v', 'élongation yM yS', 'onde progressive relation temporelle', ...REQUEST_WORDS],
  metadata: {
    courseId: 'phys_ch1_waves', chapter: 'Ondes mécaniques progressives', lesson: 'Propagation, retard et célérité',
    visualStyle: 'pencil', resourceRole: 'teacher_sketch', paletteId: 'bac-pencil-v1',
    sourceUrl: 'https://www.youtube.com/watch?v=E79tE5gmdrk', sourceTeacher: 'Jihad El Goufifa',
    sourceVideoTitle: 'Physique-Chimie 2Bac - 1: Les ondes mécaniques progressives (Cours)', auditStatus: 'video_reviewed',
    sourceTimecodes: ['56:00–58:20 · source S, point M, distance et retard temporel'],
    learningObjectives: ['Interpréter le retard comme une translation temporelle', 'Écrire τ égale SM sur v et yM de t égale yS de t moins τ'],
    llmIntents: ['dessiner le retard entre S et M', 'expliquer la relation yM(t)=yS(t−tau)'],
    drawingSteps: ['Tracer le milieu avec S et M', 'Coter SM', 'Dessiner le profil à la source puis au point M', 'Écrire les deux relations de retard'],
  },
  category: 'graph', viewBox: '0 0 900 520',
  layers: [
    { id: 'positions', label: 'S et M', delay: 0, svgContent: `${pencilDefs('phys-ret')}
      <line x1="90" y1="280" x2="825" y2="280" stroke="${P.muted}" stroke-width="3"/>
      <circle cx="170" cy="280" r="10" fill="${P.input}"/><circle cx="680" cy="280" r="10" fill="${P.control}"/>
      <text x="170" y="325" text-anchor="middle" font-size="26" fill="${P.input}" font-family="${FONT}">S</text><text x="680" y="325" text-anchor="middle" font-size="26" fill="${P.control}" font-family="${FONT}">M</text>
      <path d="M185 360 L665 360" stroke="${P.ink}" stroke-width="3" marker-end="url(#phys-ret-arrow)"/><path d="M665 375 L185 375" stroke="${P.ink}" stroke-width="3" marker-end="url(#phys-ret-arrow)"/><text x="425" y="350" text-anchor="middle" font-size="22" fill="${P.ink}" font-family="${FONT}">SM = d</text>` },
    { id: 'profils', label: 'Profils décalés', delay: 550, svgContent: `
      <path d="M90 220 L120 220 Q170 80 220 220 L300 220" fill="none" stroke="${P.input}" stroke-width="4"/><text x="170" y="75" text-anchor="middle" font-size="20" fill="${P.input}" font-family="${FONT}">signal en S à t</text>
      <path d="M550 220 L610 220 Q660 80 710 220 L790 220" fill="none" stroke="${P.control}" stroke-width="4"/><text x="660" y="75" text-anchor="middle" font-size="20" fill="${P.control}" font-family="${FONT}">même signal en M à t + τ</text>
      <path d="M260 150 L555 150" stroke="${P.positive}" stroke-width="4" marker-end="url(#phys-ret-green-arrow)"/>` },
    { id: 'relations', label: 'Relations', delay: 1000, svgContent: `
      <rect x="180" y="415" width="540" height="80" rx="18" fill="none" stroke="${P.reference}" stroke-width="3"/>
      <text x="450" y="448" text-anchor="middle" font-size="25" fill="${P.positive}" font-family="${FONT}">τ = SM / v</text>
      <text x="450" y="480" text-anchor="middle" font-size="24" fill="${P.reference}" font-family="${FONT}">yM(t) = yS(t − τ)</text>` },
  ],
  annotations: [{ id: 'delay', x: 145, y: 45, width: 600, height: 450, label: 'Retard', description: 'M reproduit le mouvement de S avec un retard τ = SM/v, sans changement de forme dans le modèle idéal.', color: P.reference }],
  highlights: [{ id: 'relation', cx: 450, cy: 455, radius: 180, label: 'Translation temporelle' }],
};

export const PHYS_CROQUIS_DEUX_CAPTEURS: ScientificSchema = {
  id: 'phys_croquis_deux_capteurs',
  title: 'Croquis au crayon — Deux capteurs sur une corde',
  subject: 'physics',
  keywords: ['deux capteurs onde', 'capteurs A B corde', 'distance retard célérité', 'AB 80 cm 20 ms', 'protocole onde', ...REQUEST_WORDS],
  metadata: {
    courseId: 'phys_ch1_waves', chapter: 'Ondes mécaniques progressives', lesson: 'Retard et célérité — mesurer sans confondre',
    visualStyle: 'pencil', resourceRole: 'teacher_sketch', paletteId: 'bac-pencil-v1', auditStatus: 'curriculum_reviewed',
    learningObjectives: ['Identifier d, tA et tB dans un montage', 'Convertir les unités avant le calcul de v'],
    llmIntents: ['dessiner deux capteurs sur une corde', 'poser un calcul de célérité à partir de AB et du retard'],
    drawingSteps: ['Tracer la corde et la source', 'Placer A et B', 'Coter AB', 'Noter tA et tB', 'Écrire τ puis v avec conversions'],
  },
  category: 'diagram', viewBox: '0 0 900 520',
  layers: [
    { id: 'montage', label: 'Montage', delay: 0, svgContent: `${pencilDefs('phys-ab')}
      <path d="M70 250 C120 250 145 150 200 250 S290 250 355 250 S510 250 830 250" fill="none" stroke="${P.ink}" stroke-width="4"/>
      <rect x="330" y="190" width="45" height="125" rx="8" fill="none" stroke="${P.observed}" stroke-width="4"/><rect x="690" y="190" width="45" height="125" rx="8" fill="none" stroke="${P.control}" stroke-width="4"/>
      <text x="352" y="350" text-anchor="middle" font-size="25" fill="${P.observed}" font-family="${FONT}">A : 12 ms</text><text x="712" y="350" text-anchor="middle" font-size="25" fill="${P.control}" font-family="${FONT}">B : 32 ms</text>
      <path d="M205 125 L760 125" stroke="${P.positive}" stroke-width="4" marker-end="url(#phys-ab-green-arrow)"/><text x="480" y="95" text-anchor="middle" font-size="22" fill="${P.positive}" font-family="${FONT}">sens de propagation</text>` },
    { id: 'mesures', label: 'Mesures et unités', delay: 600, svgContent: `
      <path d="M365 410 L700 410" stroke="${P.ink}" stroke-width="3" marker-end="url(#phys-ab-arrow)"/><path d="M700 425 L365 425" stroke="${P.ink}" stroke-width="3" marker-end="url(#phys-ab-arrow)"/><text x="532" y="400" text-anchor="middle" font-size="22" fill="${P.ink}" font-family="${FONT}">AB = 80 cm = 0,80 m</text>
      <text x="175" y="415" text-anchor="middle" font-size="22" fill="${P.reference}" font-family="${FONT}">τ = 20 ms</text><text x="175" y="455" text-anchor="middle" font-size="22" fill="${P.reference}" font-family="${FONT}">= 0,020 s</text>
      <text x="700" y="480" text-anchor="middle" font-size="27" fill="${P.positive}" font-family="${FONT}">v = 40 m·s⁻¹</text>` },
  ],
  annotations: [{ id: 'ab', x: 315, y: 175, width: 445, height: 285, label: 'Deux détections', description: 'Le même signal est détecté en A puis en B ; le retard est la différence des deux dates.', color: P.observed }],
  highlights: [{ id: 'units', cx: 470, cy: 420, radius: 190, label: 'Convertir avant de calculer' }],
};

export const PHYS_CROQUIS_SIGNAUX_RETARD: ScientificSchema = {
  id: 'phys_croquis_signaux_retard',
  title: 'Croquis au crayon — Décalage de deux signaux',
  subject: 'physics',
  keywords: ['signaux capteurs A B', 'signaux homologues', 'pics décalés retard', 'retard graphique', 'lecture graphique retard', 'points homologues', 'tA 1,5 tB 3,5', ...REQUEST_WORDS],
  metadata: {
    courseId: 'phys_ch1_waves', chapter: 'Ondes mécaniques progressives', lesson: 'Méthode BAC — exploiter deux signaux',
    visualStyle: 'pencil', resourceRole: 'teacher_sketch', paletteId: 'bac-pencil-v1', auditStatus: 'curriculum_reviewed',
    learningObjectives: ['Repérer deux points homologues sur des signaux', 'Lire τ puis calculer la célérité'],
    llmIntents: ['dessiner deux pics décalés', 'montrer comment lire un retard sur un graphe'],
    drawingSteps: ['Tracer les axes', 'Dessiner le signal A', 'Reproduire la même forme décalée pour B', 'Projeter les pics sur t', 'Coter τ'],
  },
  category: 'graph', viewBox: '0 0 900 520',
  layers: [
    { id: 'axes', label: 'Axes', delay: 0, svgContent: `${pencilDefs('phys-signals')}
      <path d="M100 420 L830 420" stroke="${P.ink}" stroke-width="4" marker-end="url(#phys-signals-arrow)"/><path d="M100 420 L100 70" stroke="${P.ink}" stroke-width="4" marker-end="url(#phys-signals-arrow)"/><text x="840" y="430" font-size="23" fill="${P.ink}" font-family="${FONT}">t (s)</text><text x="55" y="75" font-size="21" fill="${P.ink}" font-family="${FONT}">signal</text>` },
    { id: 'courbes', label: 'Deux signaux', delay: 450, svgContent: `
      <path d="M110 420 C210 420 225 395 260 210 C290 100 325 385 365 420" fill="none" stroke="${P.observed}" stroke-width="5"/><text x="250" y="125" font-size="25" fill="${P.observed}" font-family="${FONT}">A</text>
      <path d="M410 420 C505 420 530 395 565 210 C595 100 630 385 675 420" fill="none" stroke="${P.control}" stroke-width="5"/><text x="555" y="125" font-size="25" fill="${P.control}" font-family="${FONT}">B</text>
      <line x1="280" y1="160" x2="280" y2="420" stroke="${P.observed}" stroke-width="3" stroke-dasharray="8 7"/><line x1="585" y1="160" x2="585" y2="420" stroke="${P.control}" stroke-width="3" stroke-dasharray="8 7"/>
      <text x="280" y="455" text-anchor="middle" font-size="20" fill="${P.observed}" font-family="${FONT}">tA = 1,5 s</text><text x="585" y="455" text-anchor="middle" font-size="20" fill="${P.control}" font-family="${FONT}">tB = 3,5 s</text>` },
    { id: 'retard', label: 'Retard', delay: 900, svgContent: `
      <path d="M295 330 L570 330" stroke="${P.positive}" stroke-width="4" marker-end="url(#phys-signals-green-arrow)"/><text x="432" y="310" text-anchor="middle" font-size="24" fill="${P.positive}" font-family="${FONT}">τ = 2,0 s</text>
      <text x="715" y="250" text-anchor="middle" font-size="21" fill="${P.reference}" font-family="${FONT}">même pic</text><text x="715" y="282" text-anchor="middle" font-size="21" fill="${P.reference}" font-family="${FONT}">= points homologues</text>` },
  ],
  annotations: [{ id: 'peaks', x: 210, y: 90, width: 430, height: 380, label: 'Pics homologues', description: 'On mesure le décalage horizontal entre deux points de même forme, ici les maxima.', color: P.positive }],
  highlights: [{ id: 'tau', cx: 430, cy: 330, radius: 150, label: 'Décalage horizontal' }],
};

export const PHYS_CROQUIS_BILAN_ONDES: ScientificSchema = {
  id: 'phys_croquis_bilan_ondes',
  title: 'Croquis au crayon — Bilan des ondes mécaniques',
  subject: 'physics',
  keywords: ['bilan ondes mécaniques', 'carte onde propagation retard célérité', 'milieu énergie transversale longitudinale', 'synthèse chapitre ondes', ...REQUEST_WORDS],
  metadata: {
    courseId: 'phys_ch1_waves', chapter: 'Ondes mécaniques progressives', lesson: 'Bilan de compétence',
    visualStyle: 'pencil', resourceRole: 'teacher_sketch', paletteId: 'bac-pencil-v1', auditStatus: 'curriculum_reviewed',
    learningObjectives: ['Relier définition, types et mesure d’une onde mécanique', 'Mobiliser τ et v avec les unités SI'],
    llmIntents: ['dessiner le bilan du chapitre des ondes', 'faire une carte propagation types retard célérité'],
    drawingSteps: ['Écrire onde mécanique au centre', 'Ajouter milieu et transport d’énergie', 'Ajouter transversale et longitudinale', 'Ajouter τ puis v'],
  },
  category: 'diagram', viewBox: '0 0 900 520',
  layers: [
    { id: 'centre', label: 'Définition', delay: 0, svgContent: `${pencilDefs('phys-bilan')}
      <ellipse cx="450" cy="255" rx="170" ry="70" fill="none" stroke="${P.ink}" stroke-width="4"/><text x="450" y="245" text-anchor="middle" font-size="25" fill="${P.ink}" font-family="${FONT}">ONDE MÉCANIQUE</text><text x="450" y="282" text-anchor="middle" font-size="19" fill="${P.muted}" font-family="${FONT}">perturbation progressive</text>` },
    { id: 'sens', label: 'Nature et types', delay: 450, svgContent: `
      <path d="M330 220 L210 125" stroke="${P.positive}" stroke-width="4" marker-end="url(#phys-bilan-green-arrow)"/><text x="145" y="95" text-anchor="middle" font-size="21" fill="${P.positive}" font-family="${FONT}">milieu matériel</text><text x="145" y="125" text-anchor="middle" font-size="18" fill="${P.muted}" font-family="${FONT}">énergie, pas matière</text>
      <path d="M330 290 L205 395" stroke="${P.observed}" stroke-width="4" marker-end="url(#phys-bilan-arrow)"/><text x="145" y="420" text-anchor="middle" font-size="21" fill="${P.observed}" font-family="${FONT}">transversale ⟂</text><text x="145" y="452" text-anchor="middle" font-size="21" fill="${P.input}" font-family="${FONT}">longitudinale ∥</text>` },
    { id: 'mesure', label: 'Mesure', delay: 900, svgContent: `
      <path d="M570 220 L700 125" stroke="${P.control}" stroke-width="4" marker-end="url(#phys-bilan-arrow)"/><text x="750" y="90" text-anchor="middle" font-size="22" fill="${P.control}" font-family="${FONT}">retard</text><text x="750" y="125" text-anchor="middle" font-size="24" fill="${P.control}" font-family="${FONT}">τ = tB − tA</text>
      <path d="M570 290 L700 395" stroke="${P.reference}" stroke-width="4" marker-end="url(#phys-bilan-arrow)"/><text x="750" y="420" text-anchor="middle" font-size="22" fill="${P.reference}" font-family="${FONT}">célérité</text><text x="750" y="455" text-anchor="middle" font-size="25" fill="${P.positive}" font-family="${FONT}">v = d / τ</text>` },
  ],
  annotations: [{ id: 'summary', x: 70, y: 45, width: 760, height: 430, label: 'Carte de synthèse', description: 'Une onde mécanique exige un milieu, transfère de l’énergie et se caractérise expérimentalement par un retard et une célérité.', color: P.ink }],
  highlights: [{ id: 'core', cx: 450, cy: 255, radius: 185, label: 'Onde mécanique progressive' }],
};

// Les constantes de provenance sont volontairement conservées au niveau du
// module : elles rendent les divergences détectables lors d'une future révision.
void [COURSE, CHAPTER, LESSON, SOURCE_URL, SOURCE_TEACHER, SOURCE_TITLE, BAC_PENCIL_PALETTE_ID];
