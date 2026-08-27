import type { ScientificSchema } from './types';
import { BAC_PENCIL as P, BAC_PENCIL_FONT as FONT, BAC_PENCIL_PALETTE_ID, pencilDefs } from './pencilPalette';

export const MATH_CROQUIS_FORMES_INDETERMINEES: ScientificSchema = {
  id: 'math_croquis_formes_indeterminees',
  title: 'Croquis au crayon — Les quatre formes indéterminées',
  subject: 'math',
  keywords: ['formes indéterminées', 'FI limites', 'zéro sur zéro', 'infini sur infini', 'zéro fois infini', 'infini moins infini'],
  metadata: {
    courseId: 'math_ch1_limits', chapter: 'Limites et continuité', lesson: 'Lever une forme indéterminée',
    visualStyle: 'pencil', resourceRole: 'teacher_sketch', paletteId: 'bac-pencil-v1',
    sourceUrl: 'https://www.youtube.com/watch?v=rhN5zNtTiuE', sourceTeacher: 'Mouad Tahiri',
    sourceVideoTitle: 'Séance N°1 : Les limites - 2bac astuces et méthode', auditStatus: 'video_reviewed',
    sourceTimecodes: ['04:20–06:00 · rappel au tableau des quatre formes indéterminées'],
    learningObjectives: ['Reconnaître une forme indéterminée sans lui attribuer une valeur', 'Choisir ensuite une transformation algébrique adaptée'],
    llmIntents: ['dessiner la carte des formes indéterminées', 'rappeler les quatre FI en limites'],
    drawingSteps: ['Écrire FI au centre', 'Dessiner quatre bulles', 'Placer 0/0, ∞/∞, 0×∞ et ∞−∞', 'Ajouter l’avertissement : ce n’est pas un résultat'],
  },
  category: 'diagram', viewBox: '0 0 900 520',
  layers: [
    { id: 'centre', label: 'Forme indéterminée', delay: 0, svgContent: `${pencilDefs('math-fi')}
      <ellipse cx="450" cy="255" rx="105" ry="65" fill="none" stroke="${P.alert}" stroke-width="4"/><text x="450" y="245" text-anchor="middle" font-size="31" fill="${P.alert}" font-family="${FONT}">F. I.</text><text x="450" y="278" text-anchor="middle" font-size="17" fill="${P.ink}" font-family="${FONT}">à transformer</text>` },
    { id: 'bulles', label: 'Quatre formes', delay: 450, svgContent: `
      <path d="M385 210 L260 125 M515 210 L640 125 M385 300 L260 395 M515 300 L640 395" fill="none" stroke="${P.muted}" stroke-width="3"/>
      <ellipse cx="210" cy="105" rx="112" ry="65" fill="none" stroke="${P.input}" stroke-width="4"/><text x="210" y="118" text-anchor="middle" font-size="36" fill="${P.input}" font-family="${FONT}">0 / 0</text>
      <ellipse cx="690" cy="105" rx="112" ry="65" fill="none" stroke="${P.observed}" stroke-width="4"/><text x="690" y="118" text-anchor="middle" font-size="36" fill="${P.observed}" font-family="${FONT}">∞ / ∞</text>
      <ellipse cx="210" cy="415" rx="112" ry="65" fill="none" stroke="${P.control}" stroke-width="4"/><text x="210" y="428" text-anchor="middle" font-size="36" fill="${P.control}" font-family="${FONT}">0 × ∞</text>
      <ellipse cx="690" cy="415" rx="112" ry="65" fill="none" stroke="${P.reference}" stroke-width="4"/><text x="690" y="428" text-anchor="middle" font-size="36" fill="${P.reference}" font-family="${FONT}">∞ − ∞</text>` },
    { id: 'alerte', label: 'Avertissement', delay: 900, svgContent: `
      <path d="M335 345 Q450 385 565 345" fill="none" stroke="${P.alert}" stroke-width="3"/>
      <text x="450" y="500" text-anchor="middle" font-size="23" fill="${P.alert}" font-family="${FONT}">une F.I. n’est jamais la réponse finale</text>` },
  ],
  annotations: [{ id: 'fi', x: 80, y: 35, width: 740, height: 460, label: 'Formes indéterminées', description: 'Ces écritures signalent que les règles opératoires usuelles ne suffisent pas ; il faut transformer l’expression.', color: P.alert }],
  highlights: [{ id: 'center', cx: 450, cy: 255, radius: 120, label: 'Transformer avant de conclure' }],
};

export const MATH_CROQUIS_BOITE_FACTORISATION: ScientificSchema = {
  id: 'math_croquis_boite_factorisation',
  title: 'Croquis au crayon — Boîte à outils de factorisation',
  subject: 'math',
  keywords: ['factorisation limite', 'identités remarquables', 'a carré moins b carré', 'a cube moins b cube', 'racine polynôme', 'lever 0 sur 0'],
  metadata: {
    courseId: 'math_ch1_limits', chapter: 'Limites et continuité', lesson: 'Lever une forme indéterminée',
    visualStyle: 'pencil', resourceRole: 'teacher_sketch', paletteId: 'bac-pencil-v1',
    sourceUrl: 'https://www.youtube.com/watch?v=rhN5zNtTiuE', sourceTeacher: 'Mouad Tahiri',
    sourceVideoTitle: 'Séance N°1 : Les limites - 2bac astuces et méthode', auditStatus: 'video_reviewed',
    sourceTimecodes: ['04:30–11:00 · identités remarquables et factorisation', '14:30–22:30 · factoriser par x−a lorsque P(a)=0'],
    learningObjectives: ['Choisir une identité remarquable pour factoriser', 'Extraire le facteur x−a d’un polynôme qui s’annule en a'],
    llmIntents: ['dessiner la boîte des identités remarquables', 'montrer les factorisations utiles pour une limite'],
    drawingSteps: ['Tracer une boîte d’outils', 'Écrire le facteur commun', 'Ajouter les identités de degré deux et trois', 'Relier P(a)=0 à la présence du facteur x−a'],
  },
  category: 'diagram', viewBox: '0 0 900 520',
  layers: [
    { id: 'boite', label: 'Boîte', delay: 0, svgContent: `${pencilDefs('math-fact')}
      <path d="M70 90 Q70 55 110 55 L790 55 Q830 55 830 90 L830 455 Q830 480 800 480 L100 480 Q70 480 70 455Z" fill="none" stroke="${P.ink}" stroke-width="4"/>
      <path d="M320 55 L350 20 L550 20 L580 55" fill="none" stroke="${P.control}" stroke-width="4"/><text x="450" y="47" text-anchor="middle" font-size="22" fill="${P.control}" font-family="${FONT}">FACTORISER</text>` },
    { id: 'identites', label: 'Identités', delay: 450, svgContent: `
      <text x="115" y="135" font-size="24" fill="${P.observed}" font-family="${FONT}">ab − ac = a(b − c)</text>
      <text x="115" y="195" font-size="24" fill="${P.input}" font-family="${FONT}">a² − b² = (a − b)(a + b)</text>
      <text x="115" y="255" font-size="24" fill="${P.positive}" font-family="${FONT}">a³ − b³ = (a − b)(a² + ab + b²)</text>
      <text x="115" y="315" font-size="24" fill="${P.reference}" font-family="${FONT}">a³ + b³ = (a + b)(a² − ab + b²)</text>
      <path d="M105 340 L795 340" stroke="${P.muted}" stroke-width="2" stroke-dasharray="8 7"/>` },
    { id: 'racine', label: 'Facteur x−a', delay: 900, svgContent: `
      <text x="120" y="395" font-size="25" fill="${P.control}" font-family="${FONT}">si P(a) = 0</text><path d="M310 385 L430 385" stroke="${P.positive}" stroke-width="4" marker-end="url(#math-fact-green-arrow)"/>
      <text x="470" y="395" font-size="25" fill="${P.positive}" font-family="${FONT}">P(x) = (x − a)Q(x)</text>
      <text x="450" y="455" text-anchor="middle" font-size="18" fill="${P.alert}" font-family="${FONT}">simplifier seulement pour x ≠ a, puis calculer la limite</text>` },
  ],
  annotations: [{ id: 'toolbox', x: 65, y: 15, width: 770, height: 470, label: 'Boîte à outils', description: 'La factorisation fait apparaître un facteur commun qui peut être simplifié avant le passage à la limite.', color: P.control }],
  highlights: [{ id: 'root', cx: 520, cy: 395, radius: 150, label: 'Facteur x−a' }],
};

export const MATH_CROQUIS_STRATEGIE_FI: ScientificSchema = {
  id: 'math_croquis_strategie_fi',
  title: 'Croquis au crayon — Stratégie pour lever 0/0',
  subject: 'math',
  keywords: ['méthode limite 0 sur 0', '0/0', 'lever une indétermination', 'stratégie forme indéterminée', 'substitution factorisation simplification', 'limite quotient polynômes', 'x carré moins 4'],
  metadata: {
    courseId: 'math_ch1_limits', chapter: 'Limites et continuité', lesson: 'Lever une forme indéterminée',
    visualStyle: 'pencil', resourceRole: 'teacher_sketch', paletteId: 'bac-pencil-v1',
    sourceUrl: 'https://www.youtube.com/watch?v=rhN5zNtTiuE', sourceTeacher: 'Mouad Tahiri',
    sourceVideoTitle: 'Séance N°1 : Les limites - 2bac astuces et méthode', auditStatus: 'video_reviewed',
    sourceTimecodes: ['05:00–08:30 · exemple (x²−4)/(3x−6)', '12:00–22:30 · méthode répétée sur des polynômes de degré supérieur'],
    learningObjectives: ['Structurer la résolution d’une limite donnant 0/0', 'Justifier la factorisation puis la simplification au voisinage du point'],
    llmIntents: ['dessiner l’algorithme pour lever zéro sur zéro', 'résoudre graphiquement la méthode factoriser simplifier remplacer'],
    drawingSteps: ['Remplacer x par a', 'Identifier 0/0', 'Factoriser numérateur et dénominateur', 'Simplifier le facteur x−a', 'Remplacer de nouveau et conclure'],
  },
  category: 'process', viewBox: '0 0 900 520',
  layers: [
    { id: 'depart', label: 'Substitution', delay: 0, svgContent: `${pencilDefs('math-flow')}
      <rect x="45" y="175" width="170" height="105" rx="22" fill="none" stroke="${P.input}" stroke-width="4"/><text x="130" y="215" text-anchor="middle" font-size="21" fill="${P.input}" font-family="${FONT}">1. remplacer</text><text x="130" y="252" text-anchor="middle" font-size="25" fill="${P.ink}" font-family="${FONT}">x par a</text>
      <path d="M215 228 L300 228" stroke="${P.positive}" stroke-width="4" marker-end="url(#math-flow-green-arrow)"/>
      <ellipse cx="370" cy="228" rx="70" ry="60" fill="none" stroke="${P.alert}" stroke-width="4"/><text x="370" y="239" text-anchor="middle" font-size="30" fill="${P.alert}" font-family="${FONT}">0 / 0 ?</text>` },
    { id: 'transformer', label: 'Transformer', delay: 500, svgContent: `
      <path d="M440 228 L520 228" stroke="${P.positive}" stroke-width="4" marker-end="url(#math-flow-green-arrow)"/>
      <rect x="520" y="125" width="325" height="205" rx="25" fill="none" stroke="${P.control}" stroke-width="4"/>
      <text x="682" y="165" text-anchor="middle" font-size="23" fill="${P.control}" font-family="${FONT}">2. factoriser</text>
      <text x="682" y="207" text-anchor="middle" font-size="22" fill="${P.ink}" font-family="${FONT}">x² − 4 = (x−2)(x+2)</text>
      <text x="682" y="245" text-anchor="middle" font-size="22" fill="${P.ink}" font-family="${FONT}">3x − 6 = 3(x−2)</text>
      <path d="M570 265 L790 265" stroke="${P.alert}" stroke-width="3"/><text x="682" y="305" text-anchor="middle" font-size="22" fill="${P.positive}" font-family="${FONT}">simplifier (x−2)</text>` },
    { id: 'conclure', label: 'Conclure', delay: 1000, svgContent: `
      <path d="M682 330 L682 395" stroke="${P.positive}" stroke-width="4" marker-end="url(#math-flow-green-arrow)"/>
      <rect x="500" y="395" width="365" height="90" rx="22" fill="none" stroke="${P.positive}" stroke-width="4"/><text x="682" y="430" text-anchor="middle" font-size="22" fill="${P.positive}" font-family="${FONT}">3. remplacer à nouveau</text><text x="682" y="465" text-anchor="middle" font-size="25" fill="${P.ink}" font-family="${FONT}">lim = (2+2)/3 = 4/3</text>
      <text x="225" y="420" text-anchor="middle" font-size="19" fill="${P.muted}" font-family="${FONT}">la limite étudie le voisinage :</text><text x="225" y="452" text-anchor="middle" font-size="21" fill="${P.reference}" font-family="${FONT}">x peut être ≠ a</text>` },
  ],
  annotations: [
    { id: 'detect', x: 35, y: 155, width: 415, height: 150, label: 'Détecter', description: 'La substitution donne une information : une valeur directe ou une forme indéterminée à transformer.', color: P.alert },
    { id: 'solve', x: 490, y: 110, width: 380, height: 380, label: 'Lever 0/0', description: 'Factoriser, simplifier pour x voisin de a, puis seulement effectuer la nouvelle substitution.', color: P.positive },
  ],
  highlights: [{ id: 'workflow', cx: 450, cy: 260, radius: 235, label: 'Remplacer → transformer → conclure' }],
};

export const MATH_CROQUIS_TROU_LIMITE: ScientificSchema = {
  id: 'math_croquis_trou_limite',
  title: 'Croquis au crayon — Un trou, mais une limite finie',
  subject: 'math',
  keywords: ['trou dans la courbe', 'limite finie fonction non définie', 'x carré moins 1 sur x moins 1', 'limite en 1 égale 2', 'prolongement par continuité'],
  metadata: {
    courseId: 'math_ch1_limits', chapter: 'Limites et continuité', lesson: 'Calculer — reconnaître puis lever une indétermination',
    visualStyle: 'pencil', resourceRole: 'teacher_sketch', paletteId: 'bac-pencil-v1', auditStatus: 'curriculum_reviewed',
    learningObjectives: ['Distinguer valeur f(a) et limite quand x tend vers a', 'Interpréter une simplification valable au voisinage de a'],
    llmIntents: ['dessiner une droite avec un trou', 'expliquer pourquoi la limite existe même si f de a n’existe pas'],
    drawingSteps: ['Tracer les axes et la droite y=x+1', 'Effacer le point de la courbe en (1,2)', 'Faire approcher deux flèches de gauche et de droite', 'Écrire f non définie en 1 mais limite égale 2'],
  },
  category: 'graph', viewBox: '0 0 900 520',
  layers: [
    { id: 'repere', label: 'Repère', delay: 0, svgContent: `${pencilDefs('math-hole')}
      <path d="M95 420 L820 420" stroke="${P.ink}" stroke-width="4" marker-end="url(#math-hole-arrow)"/><path d="M250 485 L250 55" stroke="${P.ink}" stroke-width="4" marker-end="url(#math-hole-arrow)"/><text x="830" y="430" font-size="23" fill="${P.ink}" font-family="${FONT}">x</text><text x="225" y="65" font-size="23" fill="${P.ink}" font-family="${FONT}">y</text>
      <line x1="410" y1="70" x2="410" y2="445" stroke="${P.muted}" stroke-width="2" stroke-dasharray="8 7"/><line x1="225" y1="260" x2="780" y2="260" stroke="${P.muted}" stroke-width="2" stroke-dasharray="8 7"/><text x="410" y="455" text-anchor="middle" font-size="20" fill="${P.muted}" font-family="${FONT}">1</text><text x="225" y="267" text-anchor="end" font-size="20" fill="${P.muted}" font-family="${FONT}">2</text>` },
    { id: 'courbe', label: 'Courbe trouée', delay: 450, svgContent: `
      <path d="M100 445 L390 275 M430 245 L780 40" fill="none" stroke="${P.input}" stroke-width="5"/>
      <circle cx="410" cy="260" r="13" fill="#0f172a" stroke="${P.control}" stroke-width="5"/>
      <text x="590" y="120" font-size="22" fill="${P.input}" font-family="${FONT}">y = x + 1, sauf en x = 1</text>
      <text x="455" y="300" font-size="20" fill="${P.control}" font-family="${FONT}">trou : f(1) n’existe pas</text>` },
    { id: 'approche', label: 'Approche bilatérale', delay: 900, svgContent: `
      <path d="M325 315 L385 278" stroke="${P.positive}" stroke-width="4" marker-end="url(#math-hole-green-arrow)"/><path d="M500 207 L435 245" stroke="${P.positive}" stroke-width="4" marker-end="url(#math-hole-green-arrow)"/>
      <rect x="500" y="330" width="330" height="110" rx="22" fill="none" stroke="${P.reference}" stroke-width="3"/><text x="665" y="372" text-anchor="middle" font-size="22" fill="${P.reference}" font-family="${FONT}">x → 1⁻ et x → 1⁺</text><text x="665" y="413" text-anchor="middle" font-size="27" fill="${P.positive}" font-family="${FONT}">f(x) → 2</text>` },
  ],
  annotations: [
    { id: 'hole', x: 365, y: 210, width: 210, height: 115, label: 'Valeur absente', description: 'Le point (1,2) ne fait pas partie de la courbe de la fonction initiale.', color: P.control },
    { id: 'limit', x: 480, y: 320, width: 360, height: 130, label: 'Limite présente', description: 'Les valeurs de f(x) s’approchent de 2 aussi bien à gauche qu’à droite de 1.', color: P.positive },
  ],
  highlights: [{ id: 'distinction', cx: 410, cy: 260, radius: 125, label: 'f(1) ≠ limite en 1' }],
};

export const MATH_CROQUIS_ASYMPTOTES: ScientificSchema = {
  id: 'math_croquis_asymptotes',
  title: 'Croquis au crayon — Asymptotes verticale et horizontale',
  subject: 'math',
  keywords: ['asymptote verticale horizontale', 'limite infinie en a', 'limite finie à infini', 'x égale a y égale L', 'fonction 1 sur x'],
  metadata: {
    courseId: 'math_ch1_limits', chapter: 'Limites et continuité', lesson: 'Asymptotes — traduire une limite en géométrie',
    visualStyle: 'pencil', resourceRole: 'teacher_sketch', paletteId: 'bac-pencil-v1', auditStatus: 'curriculum_reviewed',
    learningObjectives: ['Associer chaque type de limite à l’équation correcte de l’asymptote', 'Lire les comportements unilatéraux près d’une asymptote verticale'],
    llmIntents: ['dessiner asymptote verticale et horizontale', 'expliquer x égale a contre y égale L'],
    drawingSteps: ['Tracer le repère', 'Dessiner x=a en pointillés', 'Dessiner y=L en pointillés', 'Tracer deux branches qui s’en approchent', 'Écrire les limites justificatives'],
  },
  category: 'graph', viewBox: '0 0 900 520',
  layers: [
    { id: 'repere', label: 'Repère et asymptotes', delay: 0, svgContent: `${pencilDefs('math-asym')}
      <path d="M80 285 L825 285" stroke="${P.ink}" stroke-width="4" marker-end="url(#math-asym-arrow)"/><path d="M360 475 L360 45" stroke="${P.ink}" stroke-width="4" marker-end="url(#math-asym-arrow)"/>
      <line x1="510" y1="55" x2="510" y2="475" stroke="${P.alert}" stroke-width="4" stroke-dasharray="10 8"/><text x="525" y="85" font-size="23" fill="${P.alert}" font-family="${FONT}">x = a</text>
      <line x1="80" y1="170" x2="825" y2="170" stroke="${P.reference}" stroke-width="4" stroke-dasharray="10 8"/><text x="740" y="155" font-size="23" fill="${P.reference}" font-family="${FONT}">y = L</text>` },
    { id: 'branches', label: 'Branches', delay: 500, svgContent: `
      <path d="M90 420 C250 385 405 330 465 200 C492 140 503 85 507 55" fill="none" stroke="${P.input}" stroke-width="5"/>
      <path d="M514 475 C525 385 550 300 610 235 C670 180 735 172 820 170" fill="none" stroke="${P.positive}" stroke-width="5"/>
      <path d="M455 110 L500 65" stroke="${P.alert}" stroke-width="4" marker-end="url(#math-asym-alert-arrow)"/><path d="M700 210 L800 180" stroke="${P.positive}" stroke-width="4" marker-end="url(#math-asym-green-arrow)"/>` },
    { id: 'justifications', label: 'Limites justificatives', delay: 950, svgContent: `
      <rect x="55" y="40" width="330" height="105" rx="20" fill="none" stroke="${P.alert}" stroke-width="3"/><text x="220" y="80" text-anchor="middle" font-size="20" fill="${P.alert}" font-family="${FONT}">x → a : f(x) → ±∞</text><text x="220" y="117" text-anchor="middle" font-size="20" fill="${P.ink}" font-family="${FONT}">⇒ verticale x = a</text>
      <rect x="560" y="350" width="315" height="105" rx="20" fill="none" stroke="${P.reference}" stroke-width="3"/><text x="717" y="390" text-anchor="middle" font-size="20" fill="${P.reference}" font-family="${FONT}">x → ±∞ : f(x) → L</text><text x="717" y="427" text-anchor="middle" font-size="20" fill="${P.ink}" font-family="${FONT}">⇒ horizontale y = L</text>` },
  ],
  annotations: [
    { id: 'vertical', x: 430, y: 40, width: 105, height: 440, label: 'Asymptote verticale', description: 'La variable x approche une valeur finie a tandis que f(x) devient infinie.', color: P.alert },
    { id: 'horizontal', x: 550, y: 130, width: 330, height: 80, label: 'Asymptote horizontale', description: 'À l’infini sur l’axe des x, la courbe se rapproche d’une hauteur finie L.', color: P.reference },
  ],
  highlights: [{ id: 'equations', cx: 510, cy: 170, radius: 170, label: 'x=a ou y=L' }],
};

export const MATH_CROQUIS_TVI: ScientificSchema = {
  id: 'math_croquis_tvi',
  title: 'Croquis au crayon — Théorème des valeurs intermédiaires',
  subject: 'math',
  keywords: ['théorème valeurs intermédiaires', 'TVI solution f x égale zéro', 'continuité intervalle', 'changement de signe', 'existence unicité racine'],
  metadata: {
    courseId: 'math_ch1_limits', chapter: 'Limites et continuité', lesson: 'Continuité et TVI — existence puis unicité',
    visualStyle: 'pencil', resourceRole: 'teacher_sketch', paletteId: 'bac-pencil-v1', auditStatus: 'curriculum_reviewed',
    learningObjectives: ['Vérifier les trois hypothèses du TVI', 'Distinguer existence et unicité d’une solution'],
    llmIntents: ['dessiner le TVI avec changement de signe', 'expliquer existence puis unicité d’une racine'],
    drawingSteps: ['Tracer l’intervalle fermé de a à b et une courbe continue', 'Placer f(a) sous 0 et f(b) au-dessus de 0', 'Colorer la bande des valeurs intermédiaires', 'Marquer une intersection α', 'Ajouter la monotonie seulement pour l’unicité'],
  },
  category: 'graph', viewBox: '0 0 900 520',
  layers: [
    { id: 'repere', label: 'Intervalle', delay: 0, svgContent: `${pencilDefs('math-tvi')}
      <path d="M80 280 L830 280" stroke="${P.ink}" stroke-width="4" marker-end="url(#math-tvi-arrow)"/><path d="M160 470 L160 55" stroke="${P.ink}" stroke-width="4" marker-end="url(#math-tvi-arrow)"/>
      <line x1="230" y1="80" x2="230" y2="440" stroke="${P.muted}" stroke-width="2" stroke-dasharray="8 7"/><line x1="740" y1="80" x2="740" y2="440" stroke="${P.muted}" stroke-width="2" stroke-dasharray="8 7"/><text x="230" y="465" text-anchor="middle" font-size="23" fill="${P.muted}" font-family="${FONT}">a</text><text x="740" y="465" text-anchor="middle" font-size="23" fill="${P.muted}" font-family="${FONT}">b</text>` },
    { id: 'courbe', label: 'Continuité et signe', delay: 450, svgContent: `
      <path d="M230 405 C335 390 365 335 430 300 C515 250 565 155 740 105" fill="none" stroke="${P.input}" stroke-width="5"/>
      <circle cx="230" cy="405" r="9" fill="${P.alert}"/><circle cx="740" cy="105" r="9" fill="${P.positive}"/>
      <text x="250" y="425" font-size="20" fill="${P.alert}" font-family="${FONT}">f(a) &lt; 0</text><text x="660" y="90" font-size="20" fill="${P.positive}" font-family="${FONT}">f(b) &gt; 0</text>
      <path d="M250 180 C365 145 565 145 720 180" fill="none" stroke="${P.observed}" stroke-width="3"/><text x="485" y="135" text-anchor="middle" font-size="20" fill="${P.observed}" font-family="${FONT}">f continue sur [a,b]</text>` },
    { id: 'racine', label: 'Existence', delay: 850, svgContent: `
      <circle cx="470" cy="280" r="11" fill="${P.control}"/><line x1="470" y1="280" x2="470" y2="440" stroke="${P.control}" stroke-width="3" stroke-dasharray="8 7"/><text x="470" y="465" text-anchor="middle" font-size="23" fill="${P.control}" font-family="${FONT}">α</text>
      <rect x="525" y="315" width="320" height="130" rx="22" fill="none" stroke="${P.reference}" stroke-width="3"/><text x="685" y="350" text-anchor="middle" font-size="19" fill="${P.reference}" font-family="${FONT}">0 entre f(a) et f(b)</text><text x="685" y="385" text-anchor="middle" font-size="22" fill="${P.positive}" font-family="${FONT}">∃ α ∈ ]a,b[ : f(α)=0</text><text x="685" y="420" text-anchor="middle" font-size="18" fill="${P.alert}" font-family="${FONT}">unicité : ajouter stricte monotonie</text>` },
  ],
  annotations: [
    { id: 'hypotheses', x: 205, y: 70, width: 560, height: 365, label: 'Hypothèses du TVI', description: 'Il faut un intervalle, la continuité sur cet intervalle et une valeur cible située entre f(a) et f(b).', color: P.observed },
    { id: 'uniqueness', x: 510, y: 300, width: 345, height: 155, label: 'Existence ≠ unicité', description: 'Le TVI garantit au moins une solution. Une monotonie stricte permet ensuite de conclure qu’elle est unique.', color: P.alert },
  ],
  highlights: [{ id: 'root', cx: 470, cy: 280, radius: 120, label: 'Passage par zéro' }],
};

export const MATH_CROQUIS_CARTE_METHODES: ScientificSchema = {
  id: 'math_croquis_carte_methodes',
  title: 'Croquis au crayon — Carte des méthodes de limites',
  subject: 'math',
  keywords: ['carte méthodes limites', 'calcul direct factoriser conjugué terme dominant', 'asymptote continuité TVI', 'synthèse limites', 'méthode BAC limites'],
  metadata: {
    courseId: 'math_ch1_limits', chapter: 'Limites et continuité', lesson: 'Bilan de compétence',
    visualStyle: 'pencil', resourceRole: 'teacher_sketch', paletteId: 'bac-pencil-v1', auditStatus: 'curriculum_reviewed',
    learningObjectives: ['Choisir une méthode à partir du diagnostic initial', 'Relier calcul de limite, géométrie et preuve d’existence'],
    llmIntents: ['dessiner la carte complète du chapitre limites', 'choisir entre factoriser conjugué dominant asymptote et TVI'],
    drawingSteps: ['Écrire limite au centre', 'Créer la branche calcul direct', 'Créer la branche FI et ses quatre outils', 'Créer la branche interprétation asymptotique', 'Créer la branche continuité et TVI'],
  },
  category: 'diagram', viewBox: '0 0 900 520',
  layers: [
    { id: 'centre', label: 'Diagnostic', delay: 0, svgContent: `${pencilDefs('math-map')}
      <ellipse cx="450" cy="255" rx="120" ry="62" fill="none" stroke="${P.ink}" stroke-width="4"/><text x="450" y="247" text-anchor="middle" font-size="27" fill="${P.ink}" font-family="${FONT}">CALCULER</text><text x="450" y="282" text-anchor="middle" font-size="24" fill="${P.ink}" font-family="${FONT}">UNE LIMITE</text>` },
    { id: 'calcul', label: 'Calcul', delay: 400, svgContent: `
      <path d="M340 225 L220 120" stroke="${P.positive}" stroke-width="4" marker-end="url(#math-map-green-arrow)"/><rect x="45" y="45" width="230" height="120" rx="22" fill="none" stroke="${P.positive}" stroke-width="3"/><text x="160" y="83" text-anchor="middle" font-size="21" fill="${P.positive}" font-family="${FONT}">SUBSTITUTION</text><text x="160" y="118" text-anchor="middle" font-size="18" fill="${P.ink}" font-family="${FONT}">valeur déterminée ?</text><text x="160" y="147" text-anchor="middle" font-size="18" fill="${P.positive}" font-family="${FONT}">conclure</text>
      <path d="M340 290 L220 405" stroke="${P.alert}" stroke-width="4" marker-end="url(#math-map-alert-arrow)"/><rect x="35" y="345" width="275" height="140" rx="22" fill="none" stroke="${P.alert}" stroke-width="3"/><text x="172" y="378" text-anchor="middle" font-size="21" fill="${P.alert}" font-family="${FONT}">FORME INDÉTERMINÉE</text><text x="172" y="414" text-anchor="middle" font-size="17" fill="${P.ink}" font-family="${FONT}">factoriser · même dénominateur</text><text x="172" y="447" text-anchor="middle" font-size="17" fill="${P.ink}" font-family="${FONT}">conjugué · terme dominant</text>` },
    { id: 'interpreter', label: 'Interpréter et démontrer', delay: 850, svgContent: `
      <path d="M560 225 L680 120" stroke="${P.reference}" stroke-width="4" marker-end="url(#math-map-arrow)"/><rect x="625" y="45" width="240" height="120" rx="22" fill="none" stroke="${P.reference}" stroke-width="3"/><text x="745" y="83" text-anchor="middle" font-size="21" fill="${P.reference}" font-family="${FONT}">INTERPRÉTER</text><text x="745" y="118" text-anchor="middle" font-size="18" fill="${P.ink}" font-family="${FONT}">asymptote verticale</text><text x="745" y="147" text-anchor="middle" font-size="18" fill="${P.ink}" font-family="${FONT}">ou horizontale</text>
      <path d="M560 290 L680 405" stroke="${P.observed}" stroke-width="4" marker-end="url(#math-map-arrow)"/><rect x="610" y="345" width="265" height="140" rx="22" fill="none" stroke="${P.observed}" stroke-width="3"/><text x="742" y="378" text-anchor="middle" font-size="21" fill="${P.observed}" font-family="${FONT}">DÉMONTRER</text><text x="742" y="414" text-anchor="middle" font-size="18" fill="${P.ink}" font-family="${FONT}">continuité + TVI</text><text x="742" y="447" text-anchor="middle" font-size="18" fill="${P.alert}" font-family="${FONT}">monotonie ⇒ unicité</text>` },
  ],
  annotations: [
    { id: 'diagnostic', x: 320, y: 185, width: 260, height: 145, label: 'Diagnostiquer avant d’agir', description: 'La première substitution choisit la branche : calcul terminé ou transformation nécessaire.', color: P.ink },
    { id: 'proof', x: 600, y: 330, width: 285, height: 165, label: 'Preuve d’existence', description: 'Le TVI n’est pas une méthode de calcul de limite : il réutilise la continuité pour établir l’existence d’une solution.', color: P.observed },
  ],
  highlights: [{ id: 'map', cx: 450, cy: 255, radius: 145, label: 'Choisir la bonne branche' }],
};

void BAC_PENCIL_PALETTE_ID;
