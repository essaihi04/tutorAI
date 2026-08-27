import type { ScientificSchema } from './types';
import { BAC_PENCIL as P, BAC_PENCIL_FONT as FONT, BAC_PENCIL_PALETTE_ID, pencilDefs } from './pencilPalette';

const REQUEST_WORDS = ['croquis', 'dessine', 'dessin au tableau', 'schématise', 'rsem lia', 'rassam lia', 'رسم ليا'];

export const CHEM_CROQUIS_CARTE_CINETIQUE: ScientificSchema = {
  id: 'chem_croquis_carte_cinetique',
  title: 'Croquis au crayon — Carte des transformations rapides et lentes',
  subject: 'chemistry',
  keywords: ['transformation rapide lente', 'cinétique chimique', 'durée transformation', 'facteurs cinétiques', 'concentration température', ...REQUEST_WORDS],
  metadata: {
    courseId: 'chem_ch1_kinetics', chapter: 'Transformations lentes et transformations rapides', lesson: 'Durée et facteurs cinétiques',
    visualStyle: 'pencil', resourceRole: 'teacher_sketch', paletteId: 'bac-pencil-v1',
    sourceUrl: 'https://www.youtube.com/watch?v=WAHItI0S14A', sourceTeacher: 'Zakaria TAOUSSE',
    sourceVideoTitle: 'leçon 01 chimie BIOF - Les transformation rapides et lentes', auditStatus: 'video_reviewed',
    sourceTimecodes: ['00:35–02:10 · carte du cours : rapide, lente, concentration et température'],
    learningObjectives: ['Organiser les notions du premier cours de cinétique', 'Distinguer classement temporel et facteurs expérimentaux'],
    llmIntents: ['dessiner la carte rapide lente', 'résumer les facteurs cinétiques du cours'],
    drawingSteps: ['Écrire transformation chimique au centre', 'Créer les branches rapide et lente', 'Ajouter la durée d’observation', 'Ajouter concentration et température comme facteurs'],
  },
  category: 'diagram', viewBox: '0 0 900 520',
  layers: [
    { id: 'centre', label: 'Notion centrale', delay: 0, svgContent: `${pencilDefs('chem-map')}
      <ellipse cx="450" cy="245" rx="175" ry="72" fill="none" stroke="${P.ink}" stroke-width="4"/>
      <text x="450" y="237" text-anchor="middle" font-size="25" fill="${P.ink}" font-family="${FONT}">TRANSFORMATION</text><text x="450" y="272" text-anchor="middle" font-size="25" fill="${P.ink}" font-family="${FONT}">CHIMIQUE</text>` },
    { id: 'classement', label: 'Rapide ou lente', delay: 450, svgContent: `
      <path d="M300 215 C225 185 180 150 155 105" fill="none" stroke="${P.positive}" stroke-width="4" marker-end="url(#chem-map-green-arrow)"/>
      <ellipse cx="125" cy="72" rx="90" ry="45" fill="none" stroke="${P.positive}" stroke-width="3"/><text x="125" y="80" text-anchor="middle" font-size="24" fill="${P.positive}" font-family="${FONT}">RAPIDE</text>
      <path d="M300 280 C225 315 185 350 155 405" fill="none" stroke="${P.alert}" stroke-width="4" marker-end="url(#chem-map-alert-arrow)"/>
      <ellipse cx="125" cy="440" rx="90" ry="45" fill="none" stroke="${P.alert}" stroke-width="3"/><text x="125" y="448" text-anchor="middle" font-size="24" fill="${P.alert}" font-family="${FONT}">LENTE</text>
      <text x="255" y="455" font-size="18" fill="${P.muted}" font-family="${FONT}">critère : durée</text>` },
    { id: 'facteurs', label: 'Facteurs', delay: 900, svgContent: `
      <path d="M610 215 C680 175 720 135 748 95" fill="none" stroke="${P.control}" stroke-width="4" marker-end="url(#chem-map-arrow)"/>
      <rect x="700" y="40" width="165" height="70" rx="22" fill="none" stroke="${P.control}" stroke-width="3"/><text x="782" y="82" text-anchor="middle" font-size="22" fill="${P.control}" font-family="${FONT}">concentration</text>
      <path d="M610 280 C680 320 720 360 748 410" fill="none" stroke="${P.observed}" stroke-width="4" marker-end="url(#chem-map-arrow)"/>
      <rect x="700" y="405" width="165" height="70" rx="22" fill="none" stroke="${P.observed}" stroke-width="3"/><text x="782" y="447" text-anchor="middle" font-size="22" fill="${P.observed}" font-family="${FONT}">température</text>
      <text x="650" y="255" text-anchor="middle" font-size="18" fill="${P.muted}" font-family="${FONT}">facteurs</text>` },
  ],
  annotations: [
    { id: 'classification', x: 25, y: 25, width: 285, height: 465, label: 'Classement', description: 'Rapide et lente qualifient la durée observable de la transformation.', color: P.positive },
    { id: 'factors', x: 600, y: 25, width: 280, height: 465, label: 'Facteurs cinétiques', description: 'Concentration et température modifient la fréquence des chocs efficaces.', color: P.control },
  ],
  highlights: [{ id: 'map', cx: 450, cy: 245, radius: 185, label: 'Carte du cours' }],
};

export const CHEM_CROQUIS_TRANSFERT_ELECTRONS: ScientificSchema = {
  id: 'chem_croquis_transfert_electrons',
  title: 'Croquis au crayon — Transfert d’électrons en oxydoréduction',
  subject: 'chemistry',
  keywords: ['oxydoréduction', 'oxydant réducteur', 'transfert électrons', 'demi équation électronique', 'couple ox red', ...REQUEST_WORDS],
  metadata: {
    courseId: 'chem_ch1_kinetics', chapter: 'Transformations lentes et transformations rapides', lesson: 'Rappel : réactions d’oxydoréduction',
    visualStyle: 'pencil', resourceRole: 'teacher_sketch', paletteId: 'bac-pencil-v1',
    sourceUrl: 'https://www.youtube.com/watch?v=WAHItI0S14A', sourceTeacher: 'Zakaria TAOUSSE',
    sourceVideoTitle: 'leçon 01 chimie BIOF - Les transformation rapides et lentes', auditStatus: 'video_reviewed',
    sourceTimecodes: ['02:30–09:30 · oxydant, réducteur, couples et transfert des électrons'],
    learningObjectives: ['Identifier donneur et accepteur d’électrons', 'Assembler deux demi-équations sans laisser d’électrons dans le bilan'],
    llmIntents: ['dessiner le transfert d’électrons', 'rappeler oxydant et réducteur avant la cinétique'],
    drawingSteps: ['Placer le réducteur à gauche', 'Tracer les électrons vers l’oxydant', 'Écrire les deux demi-équations', 'Barrer les électrons dans le bilan final'],
  },
  category: 'process', viewBox: '0 0 900 520',
  layers: [
    { id: 'acteurs', label: 'Donneur et accepteur', delay: 0, svgContent: `${pencilDefs('chem-redox')}
      <rect x="65" y="135" width="270" height="155" rx="28" fill="none" stroke="${P.input}" stroke-width="4"/>
      <text x="200" y="190" text-anchor="middle" font-size="28" fill="${P.input}" font-family="${FONT}">RÉDUCTEUR</text><text x="200" y="235" text-anchor="middle" font-size="21" fill="${P.ink}" font-family="${FONT}">donne des e⁻</text>
      <rect x="565" y="135" width="270" height="155" rx="28" fill="none" stroke="${P.control}" stroke-width="4"/>
      <text x="700" y="190" text-anchor="middle" font-size="28" fill="${P.control}" font-family="${FONT}">OXYDANT</text><text x="700" y="235" text-anchor="middle" font-size="21" fill="${P.ink}" font-family="${FONT}">capte des e⁻</text>` },
    { id: 'electrons', label: 'Électrons', delay: 500, svgContent: `
      <path d="M335 185 C405 135 495 135 565 185" fill="none" stroke="${P.positive}" stroke-width="5" marker-end="url(#chem-redox-green-arrow)"/>
      <circle cx="405" cy="135" r="22" fill="none" stroke="${P.positive}" stroke-width="3"/><circle cx="470" cy="125" r="22" fill="none" stroke="${P.positive}" stroke-width="3"/><text x="405" y="143" text-anchor="middle" font-size="18" fill="${P.positive}" font-family="${FONT}">e⁻</text><text x="470" y="133" text-anchor="middle" font-size="18" fill="${P.positive}" font-family="${FONT}">e⁻</text>
      <text x="450" y="90" text-anchor="middle" font-size="21" fill="${P.positive}" font-family="${FONT}">transfert d’électrons</text>` },
    { id: 'equations', label: 'Demi-équations', delay: 950, svgContent: `
      <text x="200" y="355" text-anchor="middle" font-size="24" fill="${P.input}" font-family="${FONT}">Red → Ox + n e⁻</text>
      <text x="700" y="355" text-anchor="middle" font-size="24" fill="${P.control}" font-family="${FONT}">Ox + n e⁻ → Red</text>
      <path d="M235 410 L665 410" stroke="${P.muted}" stroke-width="3"/><text x="450" y="455" text-anchor="middle" font-size="25" fill="${P.alert}" font-family="${FONT}">bilan : mêmes n e⁻, puis simplifier</text>` },
  ],
  annotations: [
    { id: 'donor', x: 50, y: 110, width: 300, height: 280, label: 'Réducteur', description: 'Le réducteur cède un ou plusieurs électrons : il est oxydé.', color: P.input },
    { id: 'acceptor', x: 550, y: 110, width: 300, height: 280, label: 'Oxydant', description: 'L’oxydant capte les électrons : il est réduit.', color: P.control },
  ],
  highlights: [{ id: 'transfer', cx: 450, cy: 155, radius: 145, label: 'e⁻ transférés' }],
};

export const CHEM_CROQUIS_DUREE_TRANSFORMATION: ScientificSchema = {
  id: 'chem_croquis_duree_transformation',
  title: 'Croquis au crayon — Durée d’une transformation chimique',
  subject: 'chemistry',
  keywords: ['durée transformation', 'transformation rapide lente', 'avancement temps plateau', 'courbe cinétique', 'instantanée', ...REQUEST_WORDS],
  metadata: {
    courseId: 'chem_ch1_kinetics', chapter: 'Transformations lentes et transformations rapides', lesson: 'Durée et facteurs cinétiques',
    visualStyle: 'pencil', resourceRole: 'teacher_sketch', paletteId: 'bac-pencil-v1',
    sourceUrl: 'https://www.youtube.com/watch?v=WAHItI0S14A', sourceTeacher: 'Zakaria TAOUSSE',
    sourceVideoTitle: 'leçon 01 chimie BIOF - Les transformation rapides et lentes', auditStatus: 'video_reviewed',
    sourceTimecodes: ['23:50–26:40 · courbe d’évolution, plateau et durée Δt'],
    learningObjectives: ['Lire la durée d’une transformation sur une courbe', 'Classer rapide et lente relativement au moyen d’observation'],
    llmIntents: ['dessiner une courbe cinétique vers un plateau', 'expliquer la durée delta t'],
    drawingSteps: ['Tracer les axes t et x', 'Dessiner une croissance vers un plateau', 'Projeter la fin sur l’axe du temps', 'Comparer à la durée d’observation'],
  },
  category: 'graph', viewBox: '0 0 900 520',
  layers: [
    { id: 'axes', label: 'Axes', delay: 0, svgContent: `${pencilDefs('chem-time')}
      <path d="M120 420 L810 420" stroke="${P.ink}" stroke-width="4" marker-end="url(#chem-time-arrow)"/><path d="M120 420 L120 70" stroke="${P.ink}" stroke-width="4" marker-end="url(#chem-time-arrow)"/>
      <text x="825" y="430" font-size="25" fill="${P.ink}" font-family="${FONT}">t</text><text x="90" y="75" font-size="25" fill="${P.ink}" font-family="${FONT}">x</text>
      <line x1="120" y1="125" x2="790" y2="125" stroke="${P.muted}" stroke-width="2" stroke-dasharray="8 7"/><text x="75" y="133" font-size="19" fill="${P.muted}" font-family="${FONT}">xf</text>` },
    { id: 'courbe', label: 'Évolution', delay: 500, svgContent: `
      <path d="M120 420 C190 255 300 160 455 135 C560 118 665 125 780 125" fill="none" stroke="${P.positive}" stroke-width="5"/>
      <circle cx="570" cy="126" r="9" fill="${P.control}"/><line x1="570" y1="126" x2="570" y2="420" stroke="${P.control}" stroke-width="3" stroke-dasharray="8 7"/>
      <text x="570" y="455" text-anchor="middle" font-size="23" fill="${P.control}" font-family="${FONT}">Δt</text><text x="655" y="105" font-size="21" fill="${P.positive}" font-family="${FONT}">état final</text>` },
    { id: 'lecture', label: 'Lecture', delay: 950, svgContent: `
      <rect x="155" y="65" width="250" height="90" rx="18" fill="none" stroke="${P.observed}" stroke-width="3"/><text x="280" y="102" text-anchor="middle" font-size="20" fill="${P.observed}" font-family="${FONT}">Δt très court → rapide</text><text x="280" y="135" text-anchor="middle" font-size="20" fill="${P.alert}" font-family="${FONT}">Δt long → lente</text>
      <text x="690" y="490" text-anchor="middle" font-size="19" fill="${P.muted}" font-family="${FONT}">dépend du moyen d’observation</text>` },
  ],
  annotations: [{ id: 'duration', x: 110, y: 90, width: 690, height: 375, label: 'Durée de transformation', description: 'La durée correspond au temps nécessaire pour atteindre pratiquement l’état final.', color: P.control }],
  highlights: [{ id: 'delta', cx: 570, cy: 285, radius: 145, label: 'Δt' }],
};

export const CHEM_CROQUIS_FACTEURS_CONTROLES: ScientificSchema = {
  id: 'chem_croquis_facteurs_controles',
  title: 'Croquis au crayon — Comparer concentration et température',
  subject: 'chemistry',
  keywords: ['facteurs cinétiques expérience', 'concentration température', 'deux béchers comparaison', 'essai témoin', 'variables contrôlées', ...REQUEST_WORDS],
  metadata: {
    courseId: 'chem_ch1_kinetics', chapter: 'Transformations lentes et transformations rapides', lesson: 'Durée et facteurs cinétiques',
    visualStyle: 'pencil', resourceRole: 'teacher_sketch', paletteId: 'bac-pencil-v1',
    sourceUrl: 'https://www.youtube.com/watch?v=WAHItI0S14A', sourceTeacher: 'Zakaria TAOUSSE',
    sourceVideoTitle: 'leçon 01 chimie BIOF - Les transformation rapides et lentes', auditStatus: 'video_reviewed',
    sourceTimecodes: ['27:00–31:20 · comparaison de béchers à concentration ou température différente'],
    learningObjectives: ['Construire une comparaison où une seule variable change', 'Prévoir l’effet d’une concentration ou température plus élevée'],
    llmIntents: ['dessiner deux béchers pour comparer la température', 'dessiner une expérience sur la concentration'],
    drawingSteps: ['Tracer deux béchers identiques', 'Écrire ce qui reste identique', 'Colorer la seule variable manipulée', 'Indiquer la transformation la plus rapide'],
  },
  category: 'comparison', viewBox: '0 0 900 520',
  layers: [
    { id: 'bechers', label: 'Deux essais', delay: 0, svgContent: `${pencilDefs('chem-factors')}
      <text x="235" y="65" text-anchor="middle" font-size="25" fill="${P.input}" font-family="${FONT}">Essai A</text><text x="665" y="65" text-anchor="middle" font-size="25" fill="${P.control}" font-family="${FONT}">Essai B</text>
      <path d="M120 110 L350 110 L325 405 Q235 450 145 405Z" fill="none" stroke="${P.ink}" stroke-width="4"/><path d="M550 110 L780 110 L755 405 Q665 450 575 405Z" fill="none" stroke="${P.ink}" stroke-width="4"/>
      <path d="M145 300 Q235 280 325 300" fill="none" stroke="${P.observed}" stroke-width="4"/><path d="M575 300 Q665 280 755 300" fill="none" stroke="${P.observed}" stroke-width="4"/>
      <g fill="none" stroke="${P.muted}" stroke-width="2"><circle cx="190" cy="340" r="9"/><circle cx="245" cy="365" r="9"/><circle cx="290" cy="335" r="9"/><circle cx="620" cy="340" r="9"/><circle cx="675" cy="365" r="9"/><circle cx="720" cy="335" r="9"/></g>` },
    { id: 'conditions', label: 'Conditions contrôlées', delay: 550, svgContent: `
      <text x="235" y="155" text-anchor="middle" font-size="22" fill="${P.input}" font-family="${FONT}">c = 1,0 mol·L⁻¹</text><text x="235" y="190" text-anchor="middle" font-size="22" fill="${P.ink}" font-family="${FONT}">T = 25 °C</text>
      <text x="665" y="155" text-anchor="middle" font-size="22" fill="${P.control}" font-family="${FONT}">c = 2,0 mol·L⁻¹</text><text x="665" y="190" text-anchor="middle" font-size="22" fill="${P.ink}" font-family="${FONT}">T = 25 °C</text>
      <path d="M385 255 L515 255" stroke="${P.muted}" stroke-width="3"/><text x="450" y="235" text-anchor="middle" font-size="19" fill="${P.muted}" font-family="${FONT}">une seule variable change</text>` },
    { id: 'conclusion', label: 'Conclusion', delay: 1000, svgContent: `
      <path d="M665 420 C700 455 740 465 800 450" fill="none" stroke="${P.positive}" stroke-width="4" marker-end="url(#chem-factors-green-arrow)"/>
      <text x="620" y="485" text-anchor="middle" font-size="22" fill="${P.positive}" font-family="${FONT}">c ↑ ou T ↑  →  durée ↓</text>
      <text x="235" y="485" text-anchor="middle" font-size="18" fill="${P.muted}" font-family="${FONT}">mêmes volumes · mêmes réactifs</text>` },
  ],
  annotations: [
    { id: 'control', x: 95, y: 85, width: 710, height: 405, label: 'Comparaison contrôlée', description: 'Pour attribuer l’effet à un facteur, tous les autres paramètres doivent rester identiques.', color: P.control },
  ],
  highlights: [{ id: 'one_variable', cx: 450, cy: 255, radius: 155, label: 'Une variable à la fois' }],
};

export const CHEM_CROQUIS_TROIS_BECHERS: ScientificSchema = {
  id: 'chem_croquis_trois_bechers',
  title: 'Croquis au crayon — Trois béchers à températures différentes',
  subject: 'chemistry',
  keywords: ['trois béchers température', 'dégagement gazeux température', 'bulles réaction froide chaude', 'diagnostic cinétique', ...REQUEST_WORDS],
  metadata: {
    courseId: 'chem_ch1_kinetics', chapter: 'Transformations lentes et transformations rapides', lesson: 'Diagnostic — mêmes réactifs, durées différentes',
    visualStyle: 'pencil', resourceRole: 'teacher_sketch', paletteId: 'bac-pencil-v1', auditStatus: 'curriculum_reviewed',
    learningObjectives: ['Comparer qualitativement la rapidité dans trois conditions', 'Formuler l’hypothèse que la température est un facteur cinétique'],
    llmIntents: ['dessiner trois béchers froid tempéré chaud', 'faire prédire l’intensité du dégagement gazeux'],
    drawingSteps: ['Tracer trois béchers identiques', 'Ajouter les mêmes réactifs', 'Noter les trois températures', 'Dessiner peu, moyen puis beaucoup de bulles', 'Formuler l’hypothèse'],
  },
  category: 'comparison', viewBox: '0 0 900 520',
  layers: [
    { id: 'bechers', label: 'Montages identiques', delay: 0, svgContent: `${pencilDefs('chem-three')}
      <path d="M55 150 L265 150 L245 405 Q160 450 75 405Z M345 150 L555 150 L535 405 Q450 450 365 405Z M635 150 L845 150 L825 405 Q740 450 655 405Z" fill="none" stroke="${P.ink}" stroke-width="4"/>
      <path d="M75 330 Q160 310 245 330 M365 330 Q450 310 535 330 M655 330 Q740 310 825 330" fill="none" stroke="${P.observed}" stroke-width="4"/>
      <text x="160" y="475" text-anchor="middle" font-size="22" fill="${P.observed}" font-family="${FONT}">10 °C · froid</text><text x="450" y="475" text-anchor="middle" font-size="22" fill="${P.input}" font-family="${FONT}">25 °C · témoin</text><text x="740" y="475" text-anchor="middle" font-size="22" fill="${P.control}" font-family="${FONT}">40 °C · chaud</text>` },
    { id: 'bulles', label: 'Indices observés', delay: 550, svgContent: `
      <g fill="none" stroke="${P.positive}" stroke-width="3"><circle cx="150" cy="285" r="8"/><circle cx="440" cy="285" r="8"/><circle cx="470" cy="250" r="10"/><circle cx="425" cy="220" r="7"/><circle cx="720" cy="285" r="8"/><circle cx="755" cy="275" r="10"/><circle cx="700" cy="245" r="7"/><circle cx="770" cy="220" r="12"/><circle cx="725" cy="195" r="9"/><circle cx="790" cy="175" r="7"/></g>
      <text x="160" y="115" text-anchor="middle" font-size="20" fill="${P.muted}" font-family="${FONT}">peu de bulles</text><text x="450" y="115" text-anchor="middle" font-size="20" fill="${P.positive}" font-family="${FONT}">dégagement visible</text><text x="740" y="115" text-anchor="middle" font-size="20" fill="${P.control}" font-family="${FONT}">dégagement intense</text>` },
    { id: 'hypothese', label: 'Hypothèse', delay: 1000, svgContent: `
      <path d="M160 75 C340 25 560 25 740 75" fill="none" stroke="${P.alert}" stroke-width="3"/>
      <text x="450" y="45" text-anchor="middle" font-size="22" fill="${P.alert}" font-family="${FONT}">mêmes réactifs · même volume · seule T change</text>` },
  ],
  annotations: [{ id: 'temperature', x: 40, y: 35, width: 820, height: 450, label: 'Effet de la température', description: 'À composition identique, un dégagement plus intense ou une durée plus courte indique une transformation plus rapide.', color: P.control }],
  highlights: [{ id: 'comparison', cx: 450, cy: 285, radius: 235, label: 'Comparer à conditions contrôlées' }],
};

export const CHEM_CROQUIS_INDICES_MACROSCOPIQUES: ScientificSchema = {
  id: 'chem_croquis_indices_macroscopiques',
  title: 'Croquis au crayon — Indices macroscopiques d’une transformation',
  subject: 'chemistry',
  keywords: ['indice macroscopique transformation', 'couleur absorbance gaz pression pH conductivité', 'suivi cinétique grandeur mesurable', 'précipité', ...REQUEST_WORDS],
  metadata: {
    courseId: 'chem_ch1_kinetics', chapter: 'Transformations lentes et transformations rapides', lesson: 'Classer — rapide ou lente à l’échelle de l’observation',
    visualStyle: 'pencil', resourceRole: 'teacher_sketch', paletteId: 'bac-pencil-v1', auditStatus: 'curriculum_reviewed',
    learningObjectives: ['Choisir une grandeur mesurable liée à l’avancement', 'Distinguer observation qualitative et suivi quantitatif'],
    llmIntents: ['dessiner les indices d’une transformation chimique', 'choisir entre couleur gaz pH et conductivité'],
    drawingSteps: ['Tracer quatre vignettes', 'Dessiner changement de couleur', 'Dessiner gaz ou pression', 'Dessiner pH/conductivité', 'Relier chaque indice à une grandeur suivie'],
  },
  category: 'diagram', viewBox: '0 0 900 520',
  layers: [
    { id: 'qualitatif', label: 'Indices visibles', delay: 0, svgContent: `${pencilDefs('chem-index')}
      <rect x="45" y="70" width="385" height="175" rx="25" fill="none" stroke="${P.observed}" stroke-width="3"/><text x="237" y="105" text-anchor="middle" font-size="22" fill="${P.observed}" font-family="${FONT}">COULEUR / ABSORBANCE</text>
      <path d="M95 125 L175 125 L165 215 Q135 235 105 215Z" fill="none" stroke="${P.ink}" stroke-width="3"/><path d="M105 185 Q135 175 165 185" stroke="${P.input}" stroke-width="8"/>
      <path d="M285 125 L365 125 L355 215 Q325 235 295 215Z" fill="none" stroke="${P.ink}" stroke-width="3"/><path d="M295 185 Q325 175 355 185" stroke="${P.alert}" stroke-width="8"/><path d="M185 180 L275 180" stroke="${P.positive}" stroke-width="4" marker-end="url(#chem-index-green-arrow)"/>
      <rect x="470" y="70" width="385" height="175" rx="25" fill="none" stroke="${P.positive}" stroke-width="3"/><text x="662" y="105" text-anchor="middle" font-size="22" fill="${P.positive}" font-family="${FONT}">GAZ / PRESSION</text>
      <path d="M545 125 L655 125 L645 220 Q600 240 555 220Z" fill="none" stroke="${P.ink}" stroke-width="3"/><g fill="none" stroke="${P.positive}" stroke-width="2"><circle cx="585" cy="185" r="7"/><circle cx="615" cy="160" r="10"/><circle cx="590" cy="135" r="6"/></g><circle cx="760" cy="175" r="45" fill="none" stroke="${P.control}" stroke-width="3"/><path d="M760 175 L785 145" stroke="${P.alert}" stroke-width="3"/>` },
    { id: 'quantitatif', label: 'Grandeurs mesurées', delay: 600, svgContent: `
      <rect x="45" y="280" width="385" height="175" rx="25" fill="none" stroke="${P.control}" stroke-width="3"/><text x="237" y="315" text-anchor="middle" font-size="22" fill="${P.control}" font-family="${FONT}">pH / CONDUCTIVITÉ</text><path d="M130 345 L130 420 M115 420 L145 420" stroke="${P.ink}" stroke-width="4"/><rect x="180" y="342" width="120" height="75" rx="10" fill="none" stroke="${P.control}" stroke-width="3"/><text x="240" y="390" text-anchor="middle" font-size="25" fill="${P.control}" font-family="${FONT}">pH(t)</text>
      <rect x="470" y="280" width="385" height="175" rx="25" fill="none" stroke="${P.reference}" stroke-width="3"/><text x="662" y="315" text-anchor="middle" font-size="22" fill="${P.reference}" font-family="${FONT}">CONCENTRATION</text><path d="M535 420 L535 345 L800 345" stroke="${P.ink}" stroke-width="3"/><path d="M550 360 C620 380 690 405 785 420" fill="none" stroke="${P.reference}" stroke-width="4"/><text x="670" y="395" text-anchor="middle" font-size="21" fill="${P.reference}" font-family="${FONT}">[réactif](t)</text>` },
  ],
  annotations: [{ id: 'indicator', x: 35, y: 55, width: 830, height: 415, label: 'Indicateur temporel', description: 'Une grandeur pertinente varie de façon reproductible avec l’avancement et peut être relevée à différents instants.', color: P.observed }],
  highlights: [{ id: 'choice', cx: 450, cy: 260, radius: 235, label: 'Choisir une grandeur qui évolue' }],
};

export const CHEM_CROQUIS_QUATRE_FACTEURS: ScientificSchema = {
  id: 'chem_croquis_quatre_facteurs',
  title: 'Croquis au crayon — Les quatre facteurs cinétiques',
  subject: 'chemistry',
  keywords: ['quatre facteurs cinétiques', 'température concentration surface catalyseur', 'chocs efficaces', 'accélérer transformation', 'carte facteurs', ...REQUEST_WORDS],
  metadata: {
    courseId: 'chem_ch1_kinetics', chapter: 'Transformations lentes et transformations rapides', lesson: 'Facteurs cinétiques — accélérer sans changer le bilan',
    visualStyle: 'pencil', resourceRole: 'teacher_sketch', paletteId: 'bac-pencil-v1', auditStatus: 'curriculum_reviewed',
    learningObjectives: ['Relier chaque facteur à un mécanisme microscopique', 'Séparer rapidité et état final'],
    llmIntents: ['dessiner les quatre facteurs cinétiques', 'expliquer chocs fréquents surface et catalyse'],
    drawingSteps: ['Écrire rapidité au centre', 'Ajouter température et concentration', 'Ajouter surface de contact et catalyseur', 'Relier aux chocs efficaces ou à une voie facilitée', 'Préciser que le bilan final ne change pas'],
  },
  category: 'diagram', viewBox: '0 0 900 520',
  layers: [
    { id: 'centre', label: 'Rapidité', delay: 0, svgContent: `${pencilDefs('chem-four')}
      <ellipse cx="450" cy="255" rx="135" ry="65" fill="none" stroke="${P.positive}" stroke-width="4"/><text x="450" y="245" text-anchor="middle" font-size="26" fill="${P.positive}" font-family="${FONT}">RAPIDITÉ ↑</text><text x="450" y="282" text-anchor="middle" font-size="17" fill="${P.muted}" font-family="${FONT}">durée ↓</text>` },
    { id: 'rencontres', label: 'Rencontres efficaces', delay: 450, svgContent: `
      <path d="M350 215 L220 115" stroke="${P.control}" stroke-width="4" marker-end="url(#chem-four-arrow)"/><rect x="55" y="45" width="205" height="105" rx="22" fill="none" stroke="${P.control}" stroke-width="3"/><text x="157" y="85" text-anchor="middle" font-size="22" fill="${P.control}" font-family="${FONT}">TEMPÉRATURE ↑</text><text x="157" y="122" text-anchor="middle" font-size="17" fill="${P.ink}" font-family="${FONT}">chocs plus énergétiques</text>
      <path d="M350 295 L220 405" stroke="${P.input}" stroke-width="4" marker-end="url(#chem-four-arrow)"/><rect x="55" y="375" width="205" height="105" rx="22" fill="none" stroke="${P.input}" stroke-width="3"/><text x="157" y="415" text-anchor="middle" font-size="22" fill="${P.input}" font-family="${FONT}">CONCENTRATION ↑</text><text x="157" y="452" text-anchor="middle" font-size="17" fill="${P.ink}" font-family="${FONT}">chocs plus fréquents</text>` },
    { id: 'facilitation', label: 'Contact et voie', delay: 900, svgContent: `
      <path d="M550 215 L680 115" stroke="${P.observed}" stroke-width="4" marker-end="url(#chem-four-arrow)"/><rect x="640" y="45" width="205" height="105" rx="22" fill="none" stroke="${P.observed}" stroke-width="3"/><text x="742" y="85" text-anchor="middle" font-size="22" fill="${P.observed}" font-family="${FONT}">SURFACE ↑</text><text x="742" y="122" text-anchor="middle" font-size="17" fill="${P.ink}" font-family="${FONT}">plus de sites exposés</text>
      <path d="M550 295 L680 405" stroke="${P.reference}" stroke-width="4" marker-end="url(#chem-four-arrow)"/><rect x="640" y="375" width="205" height="105" rx="22" fill="none" stroke="${P.reference}" stroke-width="3"/><text x="742" y="415" text-anchor="middle" font-size="22" fill="${P.reference}" font-family="${FONT}">CATALYSEUR</text><text x="742" y="452" text-anchor="middle" font-size="17" fill="${P.ink}" font-family="${FONT}">autre voie, Ea plus faible</text>
      <text x="450" y="500" text-anchor="middle" font-size="19" fill="${P.alert}" font-family="${FONT}">accélérer ≠ augmenter la quantité finale</text>` },
  ],
  annotations: [
    { id: 'collisions', x: 40, y: 35, width: 275, height: 455, label: 'Rencontres efficaces', description: 'Température et concentration augmentent le nombre de collisions efficaces par unité de temps.', color: P.control },
    { id: 'pathway', x: 600, y: 35, width: 275, height: 455, label: 'Contact ou voie facilitée', description: 'La surface expose davantage de sites ; le catalyseur propose un mécanisme d’activation plus facile.', color: P.reference },
  ],
  highlights: [{ id: 'speed', cx: 450, cy: 255, radius: 150, label: 'Même état final, durée différente' }],
};

export const CHEM_CROQUIS_CATALYSEUR: ScientificSchema = {
  id: 'chem_croquis_catalyseur',
  title: 'Croquis au crayon — Ce que change un catalyseur',
  subject: 'chemistry',
  keywords: ['catalyseur énergie activation', 'profil énergie activation', 'profil énergétique catalysé', 'catalyseur régénéré', 'même état final', 'voie réactionnelle', ...REQUEST_WORDS],
  metadata: {
    courseId: 'chem_ch1_kinetics', chapter: 'Transformations lentes et transformations rapides', lesson: 'Le catalyseur : trois idées à ne pas confondre',
    visualStyle: 'pencil', resourceRole: 'teacher_sketch', paletteId: 'bac-pencil-v1', auditStatus: 'curriculum_reviewed',
    learningObjectives: ['Expliquer l’accélération par une voie d’activation plus basse', 'Montrer que le catalyseur est régénéré et ne change pas l’état final'],
    llmIntents: ['dessiner le profil énergétique avec et sans catalyseur', 'expliquer catalyseur régénéré et même quantité finale'],
    drawingSteps: ['Tracer énergie en fonction de l’avancement', 'Placer mêmes niveaux initial et final', 'Dessiner la barrière haute sans catalyseur', 'Dessiner la barrière basse catalysée', 'Ajouter Cat au départ et régénéré à la fin'],
  },
  category: 'graph', viewBox: '0 0 900 520',
  layers: [
    { id: 'axes', label: 'Profil énergétique', delay: 0, svgContent: `${pencilDefs('chem-cat')}
      <path d="M90 420 L810 420" stroke="${P.ink}" stroke-width="4" marker-end="url(#chem-cat-arrow)"/><path d="M90 420 L90 60" stroke="${P.ink}" stroke-width="4" marker-end="url(#chem-cat-arrow)"/><text x="820" y="430" font-size="20" fill="${P.ink}" font-family="${FONT}">avancement</text><text x="45" y="75" font-size="20" fill="${P.ink}" font-family="${FONT}">énergie</text>
      <line x1="110" y1="330" x2="250" y2="330" stroke="${P.input}" stroke-width="4"/><line x1="660" y1="360" x2="800" y2="360" stroke="${P.positive}" stroke-width="4"/><text x="180" y="315" text-anchor="middle" font-size="19" fill="${P.input}" font-family="${FONT}">réactifs</text><text x="730" y="345" text-anchor="middle" font-size="19" fill="${P.positive}" font-family="${FONT}">produits</text>` },
    { id: 'profils', label: 'Deux voies', delay: 500, svgContent: `
      <path d="M250 330 C350 320 350 85 450 85 C550 85 555 350 660 360" fill="none" stroke="${P.alert}" stroke-width="5"/><text x="450" y="65" text-anchor="middle" font-size="20" fill="${P.alert}" font-family="${FONT}">sans catalyseur · Ea grande</text>
      <path d="M250 330 C330 325 345 205 415 205 C465 205 480 285 525 285 C570 285 595 350 660 360" fill="none" stroke="${P.reference}" stroke-width="5"/><text x="470" y="190" text-anchor="middle" font-size="20" fill="${P.reference}" font-family="${FONT}">avec catalyseur · autre voie</text>
      <path d="M295 330 L295 205" stroke="${P.control}" stroke-width="3" marker-end="url(#chem-cat-arrow)"/><text x="275" y="270" text-anchor="end" font-size="18" fill="${P.control}" font-family="${FONT}">Ea ↓</text>` },
    { id: 'bilan', label: 'Bilan du catalyseur', delay: 1000, svgContent: `
      <rect x="180" y="445" width="545" height="60" rx="18" fill="none" stroke="${P.observed}" stroke-width="3"/><text x="452" y="482" text-anchor="middle" font-size="21" fill="${P.observed}" font-family="${FONT}">Cat au départ → étapes intermédiaires → Cat régénéré</text>
      <text x="700" y="115" text-anchor="middle" font-size="18" fill="${P.positive}" font-family="${FONT}">mêmes niveaux initial/final</text>` },
  ],
  annotations: [
    { id: 'barrier', x: 245, y: 50, width: 425, height: 330, label: 'Énergie d’activation', description: 'Le catalyseur accélère la réaction en proposant un chemin dont l’énergie d’activation est plus faible.', color: P.reference },
    { id: 'final', x: 640, y: 300, width: 180, height: 95, label: 'Même état final', description: 'Le catalyseur n’abaisse pas l’énergie des produits et ne modifie pas la composition finale d’un même équilibre.', color: P.positive },
  ],
  highlights: [{ id: 'two_paths', cx: 450, cy: 235, radius: 190, label: 'Deux chemins, mêmes extrémités' }],
};

export const CHEM_CROQUIS_SURFACE_CONTACT: ScientificSchema = {
  id: 'chem_croquis_surface_contact',
  title: 'Croquis au crayon — Comprimé entier ou réduit en poudre',
  subject: 'chemistry',
  keywords: ['surface de contact', 'comprimé entier poudre', 'même masse solide', 'facteur cinétique solide', 'protocole surface', ...REQUEST_WORDS],
  metadata: {
    courseId: 'chem_ch1_kinetics', chapter: 'Transformations lentes et transformations rapides', lesson: 'Méthode BAC — proposer et critiquer un protocole',
    visualStyle: 'pencil', resourceRole: 'teacher_sketch', paletteId: 'bac-pencil-v1', auditStatus: 'curriculum_reviewed',
    learningObjectives: ['Proposer un protocole contrôlé sur la surface de contact', 'Relier poudre et nombre de sites accessibles'],
    llmIntents: ['dessiner comprimé entier contre poudre', 'expliquer l’effet de la surface de contact'],
    drawingSteps: ['Tracer deux béchers identiques', 'Placer la même masse sous deux formes', 'Indiquer les paramètres constants', 'Montrer davantage de bulles avec la poudre', 'Conclure surface plus grande donc plus rapide'],
  },
  category: 'comparison', viewBox: '0 0 900 520',
  layers: [
    { id: 'montages', label: 'Deux formes du solide', delay: 0, svgContent: `${pencilDefs('chem-surface')}
      <path d="M100 105 L380 105 L355 405 Q240 460 125 405Z M520 105 L800 105 L775 405 Q660 460 545 405Z" fill="none" stroke="${P.ink}" stroke-width="4"/>
      <path d="M125 300 Q240 275 355 300 M545 300 Q660 275 775 300" fill="none" stroke="${P.observed}" stroke-width="4"/>
      <rect x="190" y="320" width="100" height="55" rx="25" fill="none" stroke="${P.input}" stroke-width="4"/><text x="240" y="475" text-anchor="middle" font-size="22" fill="${P.input}" font-family="${FONT}">comprimé entier</text>
      <g fill="${P.control}"><circle cx="615" cy="345" r="7"/><circle cx="640" cy="330" r="6"/><circle cx="665" cy="355" r="8"/><circle cx="690" cy="325" r="7"/><circle cx="715" cy="350" r="6"/></g><text x="660" y="475" text-anchor="middle" font-size="22" fill="${P.control}" font-family="${FONT}">même masse en poudre</text>` },
    { id: 'reaction', label: 'Zone de contact', delay: 550, svgContent: `
      <g fill="none" stroke="${P.positive}" stroke-width="2"><circle cx="230" cy="275" r="8"/><circle cx="250" cy="250" r="6"/><circle cx="610" cy="285" r="6"/><circle cx="635" cy="265" r="8"/><circle cx="660" cy="240" r="6"/><circle cx="685" cy="275" r="9"/><circle cx="710" cy="245" r="7"/><circle cx="735" cy="215" r="6"/></g>
      <text x="450" y="65" text-anchor="middle" font-size="20" fill="${P.alert}" font-family="${FONT}">même masse · même solution · même T · même agitation</text>
      <path d="M395 240 L505 240" stroke="${P.positive}" stroke-width="4" marker-end="url(#chem-surface-green-arrow)"/><text x="450" y="220" text-anchor="middle" font-size="18" fill="${P.positive}" font-family="${FONT}">surface ↑</text>` },
  ],
  annotations: [{ id: 'surface', x: 80, y: 50, width: 740, height: 430, label: 'Surface exposée', description: 'À masse égale, la poudre présente une surface totale plus grande, donc davantage de contacts simultanés avec la solution.', color: P.control }],
  highlights: [{ id: 'powder', cx: 660, cy: 315, radius: 150, label: 'Davantage de sites accessibles' }],
};

export const CHEM_CROQUIS_COURBES_FACTEUR: ScientificSchema = {
  id: 'chem_croquis_courbes_facteur',
  title: 'Croquis au crayon — Deux cinétiques, même état final',
  subject: 'chemistry',
  keywords: ['deux courbes cinétiques', 'pente initiale durée demi réaction', 'même plateau facteur cinétique', 'plus rapide courbe', 'avancement temps comparaison', ...REQUEST_WORDS],
  metadata: {
    courseId: 'chem_ch1_kinetics', chapter: 'Transformations lentes et transformations rapides', lesson: 'Laboratoire — isoler l’effet d’un facteur',
    visualStyle: 'pencil', resourceRole: 'teacher_sketch', paletteId: 'bac-pencil-v1', auditStatus: 'curriculum_reviewed',
    learningObjectives: ['Comparer pentes initiales et durées caractéristiques', 'Conclure qu’un facteur cinétique accélère sans modifier le plateau'],
    llmIntents: ['dessiner deux courbes rapide et lente', 'expliquer même état final mais durées différentes'],
    drawingSteps: ['Tracer x en fonction de t', 'Placer le plateau commun xf', 'Dessiner la courbe témoin', 'Dessiner la courbe accélérée plus raide', 'Comparer t1/2 et l’état final'],
  },
  category: 'graph', viewBox: '0 0 900 520',
  layers: [
    { id: 'repere', label: 'Repère et état final', delay: 0, svgContent: `${pencilDefs('chem-curves')}
      <path d="M110 420 L825 420" stroke="${P.ink}" stroke-width="4" marker-end="url(#chem-curves-arrow)"/><path d="M110 420 L110 65" stroke="${P.ink}" stroke-width="4" marker-end="url(#chem-curves-arrow)"/><text x="835" y="430" font-size="22" fill="${P.ink}" font-family="${FONT}">t</text><text x="75" y="70" font-size="22" fill="${P.ink}" font-family="${FONT}">x</text>
      <line x1="110" y1="115" x2="800" y2="115" stroke="${P.muted}" stroke-width="3" stroke-dasharray="8 7"/><text x="70" y="123" font-size="20" fill="${P.muted}" font-family="${FONT}">xf</text>` },
    { id: 'courbes', label: 'Rapide et lente', delay: 500, svgContent: `
      <path d="M110 420 C180 210 285 120 515 115 C625 113 700 115 800 115" fill="none" stroke="${P.control}" stroke-width="5"/><text x="300" y="165" font-size="22" fill="${P.control}" font-family="${FONT}">condition accélérée</text>
      <path d="M110 420 C255 330 365 205 580 145 C665 120 735 115 800 115" fill="none" stroke="${P.observed}" stroke-width="5"/><text x="525" y="245" font-size="22" fill="${P.observed}" font-family="${FONT}">témoin</text>
      <line x1="110" y1="267" x2="800" y2="267" stroke="${P.reference}" stroke-width="2" stroke-dasharray="7 7"/><text x="65" y="275" font-size="18" fill="${P.reference}" font-family="${FONT}">xf/2</text>` },
    { id: 'comparaison', label: 'Durées caractéristiques', delay: 950, svgContent: `
      <line x1="225" y1="267" x2="225" y2="420" stroke="${P.control}" stroke-width="3" stroke-dasharray="7 7"/><line x1="415" y1="267" x2="415" y2="420" stroke="${P.observed}" stroke-width="3" stroke-dasharray="7 7"/>
      <text x="225" y="455" text-anchor="middle" font-size="19" fill="${P.control}" font-family="${FONT}">t½ accéléré</text><text x="415" y="455" text-anchor="middle" font-size="19" fill="${P.observed}" font-family="${FONT}">t½ témoin</text>
      <text x="650" y="490" text-anchor="middle" font-size="21" fill="${P.positive}" font-family="${FONT}">pente ↑ · t½ ↓ · même xf</text>` },
  ],
  annotations: [
    { id: 'initial', x: 100, y: 185, width: 360, height: 245, label: 'Évolution initiale', description: 'La transformation la plus rapide présente une pente initiale plus forte et atteint plus tôt une fraction donnée de xf.', color: P.control },
    { id: 'plateau', x: 500, y: 80, width: 310, height: 95, label: 'État final identique', description: 'Si seul un facteur cinétique est modifié, les deux courbes atteignent le même plateau dans ce modèle.', color: P.positive },
  ],
  highlights: [{ id: 'half_time', cx: 320, cy: 330, radius: 160, label: 'Comparer t½' }],
};

void BAC_PENCIL_PALETTE_ID;
