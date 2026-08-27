import type { ScientificSchema } from './types';
import { BAC_PENCIL, BAC_PENCIL_FONT } from './pencilPalette';

// Croquis sobres conçus pour le Live Board : fond transparent, traits clairs
// et peu de couleurs. Le viewer ajoute la légère irrégularité du crayon et
// révèle les couches dans l'ordre où un professeur les tracerait.
const INK = BAC_PENCIL.ink;
const MUTED = BAC_PENCIL.muted;
const ATP = BAC_PENCIL.control;
const OXYGEN = BAC_PENCIL.observed;
const PRODUCT = BAC_PENCIL.positive;
const ALERT = BAC_PENCIL.alert;
const FONT = BAC_PENCIL_FONT;
const PENCIL_DEFS = `
  <defs>
    <marker id="pencilArrow" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto">
      <path d="M0,0 L9,3.5 L0,7" fill="none" stroke="${INK}" stroke-width="1.4"/>
    </marker>
    <marker id="oxygenArrow" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto">
      <path d="M0,0 L9,3.5 L0,7" fill="none" stroke="${OXYGEN}" stroke-width="1.4"/>
    </marker>
  </defs>`;

export const SVT_CROQUIS_CELLULE_MITOCHONDRIE: ScientificSchema = {
  id: 'svt_croquis_cellule_mitochondrie',
  title: 'Croquis au crayon — De la cellule à la mitochondrie',
  subject: 'svt',
  keywords: ['cellule', 'mitochondrie', 'cellule mitochondrie', 'localisation mitochondrie', 'zoom mitochondrie', 'consommation matière organique', 'خلية', 'ميتوكندريا'],
  metadata: {
    courseId: 'svt_ch1_energy',
    chapter: 'Consommation de la matière organique et libération de l\'énergie',
    lesson: 'Libération de l\'énergie emmagasinée dans la matière organique',
    visualStyle: 'pencil',
    resourceRole: 'teacher_sketch',
    learningObjectives: ['Localiser la mitochondrie dans une cellule eucaryote', 'Relier respiration cellulaire et mitochondrie'],
    llmIntents: ['dessiner une cellule avec ses mitochondries', 'faire un zoom cellule-mitochondrie', 'introduire le lieu de la respiration', 'montrer une membrane interne continue formant les crêtes'],
    drawingSteps: ['Tracer la cellule et le noyau', 'Ajouter quelques mitochondries', 'Agrandir une mitochondrie et la relier par une flèche', 'Tracer la membrane interne en un seul trait continu puis former ses replis'],
  },
  category: 'structure',
  viewBox: '0 0 900 520',
  layers: [
    { id: 'cellule', label: 'Cellule', delay: 0, svgContent: `
      ${PENCIL_DEFS}
      <path d="M80 260 C75 120 210 65 350 105 C455 135 470 305 385 385 C275 485 95 420 80 260Z" fill="none" stroke="${INK}" stroke-width="4"/>
      <ellipse cx="245" cy="255" rx="74" ry="62" fill="none" stroke="${MUTED}" stroke-width="3"/>
      <text x="245" y="260" text-anchor="middle" font-size="20" fill="${MUTED}" font-family="${FONT}">Noyau</text>
      <g fill="none" stroke="${ATP}" stroke-width="3">
        <ellipse cx="150" cy="185" rx="34" ry="17" transform="rotate(-18 150 185)"/>
        <path d="M122 186 Q138 169 151 185 T179 184"/>
        <ellipse cx="338" cy="190" rx="34" ry="17" transform="rotate(18 338 190)"/>
        <path d="M310 190 Q325 174 340 190 T366 190"/>
        <ellipse cx="330" cy="330" rx="34" ry="17" transform="rotate(-12 330 330)"/>
        <path d="M302 330 Q317 314 332 330 T358 330"/>
      </g>
      <text x="225" y="455" text-anchor="middle" font-size="22" fill="${INK}" font-family="${FONT}">Cellule eucaryote</text>` },
    { id: 'zoom', label: 'Zoom', delay: 650, svgContent: `
      <path d="M374 190 C470 150 505 135 550 145" fill="none" stroke="${INK}" stroke-width="3" marker-end="url(#pencilArrow)"/>
      <g transform="rotate(-7 705 250)">
        <ellipse cx="705" cy="250" rx="145" ry="92" fill="none" stroke="${INK}" stroke-width="4"/>
        <path d="M584 253 C588 208 620 180 663 166 C677 162 691 159 705 160 C715 161 720 168 716 177 C710 191 692 198 685 211 C679 222 688 233 700 228 C716 222 724 201 738 189 C750 178 767 180 777 191 C790 204 783 218 770 229 C757 241 742 250 742 264 C742 277 754 284 766 277 C783 268 792 246 807 240 C823 233 839 245 842 262 C848 293 813 316 771 325 C759 328 749 322 749 311 C750 296 763 284 761 270 C760 258 749 253 739 259 C724 268 720 291 709 305 C699 318 683 324 670 319 C656 314 652 303 657 291 C663 277 674 267 674 255 C673 243 663 238 653 244 C638 253 633 274 622 286 C611 298 596 295 588 284 C584 276 582 265 584 253Z" transform="translate(70.5 25) scale(.9)" fill="none" stroke="${MUTED}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
      </g>
      <text x="705" y="392" text-anchor="middle" font-size="24" fill="${ATP}" font-family="${FONT}">Mitochondrie</text>
      <text x="705" y="425" text-anchor="middle" font-size="17" fill="${INK}" font-family="${FONT}">siège de la respiration</text>` },
  ],
  annotations: [
    { id: 'cell', x: 65, y: 80, width: 400, height: 380, label: 'Cellule eucaryote', description: 'La respiration concerne les cellules animales, végétales et de nombreux micro-organismes.', color: MUTED },
    { id: 'mito', x: 555, y: 145, width: 300, height: 285, label: 'Mitochondrie', description: 'Organite compartimenté où se déroulent l’oxydation du pyruvate, le cycle de Krebs et la phosphorylation oxydative.', color: ATP },
  ],
  highlights: [
    { id: 'mitochondrie', cx: 705, cy: 250, radius: 155, label: 'Mitochondrie' },
  ],
};

export const SVT_CROQUIS_ATP_ADP: ScientificSchema = {
  id: 'svt_croquis_atp_adp',
  title: 'Croquis au crayon — Cycle ATP–ADP',
  subject: 'svt',
  keywords: ['ATP', 'ADP', 'cycle ATP ADP', 'hydrolyse ATP', 'phosphorylation ADP', 'couplage énergétique', 'monnaie énergétique', 'طاقة', 'أدينوزين ثلاثي الفوسفات'],
  metadata: {
    courseId: 'svt_ch1_energy',
    chapter: 'Consommation de la matière organique et libération de l\'énergie',
    lesson: 'Libération de l\'énergie emmagasinée dans la matière organique',
    visualStyle: 'pencil',
    resourceRole: 'teacher_sketch',
    learningObjectives: ['Expliquer l’hydrolyse et la régénération de l’ATP', 'Relier voies cataboliques et activités cellulaires'],
    llmIntents: ['dessiner le cycle ATP-ADP', 'expliquer le couplage énergétique', 'montrer comment ATP est consommé puis régénéré'],
    drawingSteps: ['Écrire ATP et ses trois phosphates', 'Tracer l’hydrolyse vers ADP + Pi', 'Tracer la phosphorylation en sens inverse', 'Relier libération et consommation d’énergie'],
  },
  category: 'cycle',
  viewBox: '0 0 900 520',
  layers: [
    { id: 'molecules', label: 'Molécules', delay: 0, svgContent: `
      ${PENCIL_DEFS}
      <text x="220" y="155" text-anchor="middle" font-size="36" font-weight="700" fill="${ATP}" font-family="${FONT}">ATP</text>
      <g fill="none" stroke="${ATP}" stroke-width="3">
        <circle cx="165" cy="220" r="25"/><circle cx="220" cy="220" r="25"/><circle cx="275" cy="220" r="25"/>
        <line x1="190" y1="220" x2="195" y2="220"/><line x1="245" y1="220" x2="250" y2="220"/>
      </g>
      <text x="165" y="228" text-anchor="middle" font-size="19" fill="${ATP}" font-family="${FONT}">P</text>
      <text x="220" y="228" text-anchor="middle" font-size="19" fill="${ATP}" font-family="${FONT}">P</text>
      <text x="275" y="228" text-anchor="middle" font-size="19" fill="${ATP}" font-family="${FONT}">P</text>
      <text x="680" y="155" text-anchor="middle" font-size="34" font-weight="700" fill="${INK}" font-family="${FONT}">ADP + Pi</text>
      <g fill="none" stroke="${INK}" stroke-width="3">
        <circle cx="620" cy="220" r="25"/><circle cx="675" cy="220" r="25"/><circle cx="760" cy="220" r="25" stroke-dasharray="5 4"/>
        <line x1="645" y1="220" x2="650" y2="220"/>
      </g>
      <text x="620" y="228" text-anchor="middle" font-size="19" fill="${INK}" font-family="${FONT}">P</text>
      <text x="675" y="228" text-anchor="middle" font-size="19" fill="${INK}" font-family="${FONT}">P</text>
      <text x="760" y="228" text-anchor="middle" font-size="19" fill="${INK}" font-family="${FONT}">Pi</text>` },
    { id: 'couplage', label: 'Couplage', delay: 600, svgContent: `
      <path d="M315 188 C400 115 505 115 585 188" fill="none" stroke="${INK}" stroke-width="3" marker-end="url(#pencilArrow)"/>
      <text x="450" y="105" text-anchor="middle" font-size="20" fill="${PRODUCT}" font-family="${FONT}">hydrolyse : énergie libérée</text>
      <path d="M585 270 C505 350 395 350 315 270" fill="none" stroke="${INK}" stroke-width="3" marker-end="url(#pencilArrow)"/>
      <text x="450" y="385" text-anchor="middle" font-size="20" fill="${ATP}" font-family="${FONT}">phosphorylation : énergie fournie</text>
      <text x="185" y="450" text-anchor="middle" font-size="18" fill="${MUTED}" font-family="${FONT}">mouvement · synthèse · transport</text>
      <text x="710" y="450" text-anchor="middle" font-size="18" fill="${MUTED}" font-family="${FONT}">respiration ou fermentation</text>` },
  ],
  annotations: [
    { id: 'hydrolysis', x: 300, y: 70, width: 300, height: 150, label: 'Hydrolyse', description: 'ATP + H₂O → ADP + Pi + énergie utilisable.', color: PRODUCT },
    { id: 'phosphorylation', x: 300, y: 255, width: 300, height: 150, label: 'Phosphorylation', description: 'ADP + Pi + énergie → ATP. L’ATP doit être régénéré continuellement.', color: ATP },
  ],
  highlights: [
    { id: 'atp', cx: 220, cy: 205, radius: 95, label: 'ATP' },
    { id: 'cycle', cx: 450, cy: 240, radius: 165, label: 'Couplage' },
  ],
};

export const SVT_CROQUIS_EXPERIENCE_LEVURES: ScientificSchema = {
  id: 'svt_croquis_experience_levures',
  title: 'Croquis au crayon — Levures avec ou sans dioxygène',
  subject: 'svt',
  keywords: ['levures', 'expérience levures', 'levures avec sans O2', 'EXAO O2 CO2', 'respiration fermentation expérience', 'protocole expérimental', 'خميرة', 'تنفس', 'تخمر'],
  metadata: {
    courseId: 'svt_ch1_energy',
    chapter: 'Consommation de la matière organique et libération de l\'énergie',
    lesson: 'Libération de l\'énergie emmagasinée dans la matière organique',
    visualStyle: 'pencil',
    resourceRole: 'teacher_sketch',
    learningObjectives: ['Comparer respiration et fermentation à partir de mesures', 'Identifier variable, témoins et résultats attendus'],
    llmIntents: ['dessiner le protocole avec des levures', 'comparer une culture avec et sans dioxygène', 'préparer une lecture de courbes EXAO'],
    drawingSteps: ['Tracer deux enceintes identiques avec levures et glucose', 'Indiquer +O₂ et −O₂', 'Ajouter les capteurs et les résultats mesurés'],
  },
  category: 'comparison',
  viewBox: '0 0 900 520',
  layers: [
    { id: 'montage', label: 'Montage', delay: 0, svgContent: `
      ${PENCIL_DEFS}
      <text x="235" y="70" text-anchor="middle" font-size="25" fill="${OXYGEN}" font-family="${FONT}">Condition A : + O₂</text>
      <text x="665" y="70" text-anchor="middle" font-size="25" fill="${ALERT}" font-family="${FONT}">Condition B : − O₂</text>
      <path d="M135 125 L335 125 L315 390 Q235 440 155 390Z" fill="none" stroke="${INK}" stroke-width="4"/>
      <path d="M565 125 L765 125 L745 390 Q665 440 585 390Z" fill="none" stroke="${INK}" stroke-width="4"/>
      <path d="M155 310 Q235 285 315 310" fill="none" stroke="${MUTED}" stroke-width="3"/>
      <path d="M585 310 Q665 285 745 310" fill="none" stroke="${MUTED}" stroke-width="3"/>
      <g fill="none" stroke="${MUTED}" stroke-width="2">
        <circle cx="195" cy="345" r="8"/><circle cx="230" cy="365" r="7"/><circle cx="270" cy="340" r="9"/><circle cx="295" cy="372" r="7"/>
        <circle cx="625" cy="345" r="8"/><circle cx="660" cy="365" r="7"/><circle cx="700" cy="340" r="9"/><circle cx="725" cy="372" r="7"/>
      </g>
      <text x="235" y="475" text-anchor="middle" font-size="18" fill="${INK}" font-family="${FONT}">levures + glucose</text>
      <text x="665" y="475" text-anchor="middle" font-size="18" fill="${INK}" font-family="${FONT}">levures + glucose</text>` },
    { id: 'mesures', label: 'Mesures', delay: 650, svgContent: `
      <line x1="200" y1="115" x2="200" y2="255" stroke="${OXYGEN}" stroke-width="3"/>
      <circle cx="200" cy="270" r="12" fill="none" stroke="${OXYGEN}" stroke-width="3"/>
      <text x="145" y="190" text-anchor="middle" font-size="17" fill="${OXYGEN}" font-family="${FONT}">capteur O₂</text>
      <line x1="270" y1="115" x2="270" y2="255" stroke="${PRODUCT}" stroke-width="3"/>
      <circle cx="270" cy="270" r="12" fill="none" stroke="${PRODUCT}" stroke-width="3"/>
      <text x="325" y="190" text-anchor="middle" font-size="17" fill="${PRODUCT}" font-family="${FONT}">capteur CO₂</text>
      <text x="235" y="265" text-anchor="middle" font-size="19" fill="${OXYGEN}" font-family="${FONT}">O₂ ↓</text>
      <text x="235" y="292" text-anchor="middle" font-size="19" fill="${PRODUCT}" font-family="${FONT}">CO₂ ↑</text>
      <path d="M630 160 Q665 120 700 160" fill="none" stroke="${PRODUCT}" stroke-width="3"/>
      <circle cx="635" cy="150" r="6" fill="none" stroke="${PRODUCT}" stroke-width="2"/>
      <circle cx="665" cy="125" r="8" fill="none" stroke="${PRODUCT}" stroke-width="2"/>
      <circle cx="698" cy="150" r="6" fill="none" stroke="${PRODUCT}" stroke-width="2"/>
      <text x="665" y="220" text-anchor="middle" font-size="19" fill="${PRODUCT}" font-family="${FONT}">CO₂ ↑ + éthanol</text>
      <text x="235" y="430" text-anchor="middle" font-size="20" fill="${ATP}" font-family="${FONT}">beaucoup d’ATP</text>
      <text x="665" y="430" text-anchor="middle" font-size="20" fill="${ATP}" font-family="${FONT}">2 ATP nets</text>` },
  ],
  annotations: [
    { id: 'aerobic', x: 120, y: 90, width: 235, height: 365, label: 'Avec dioxygène', description: 'Les levures respirent : elles consomment O₂, rejettent CO₂ et récupèrent davantage d’énergie.', color: OXYGEN },
    { id: 'anaerobic', x: 545, y: 90, width: 240, height: 365, label: 'Sans dioxygène', description: 'Les levures réalisent une fermentation alcoolique : production d’éthanol, de CO₂ et seulement 2 ATP nets.', color: ALERT },
  ],
  highlights: [
    { id: 'avec_o2', cx: 235, cy: 270, radius: 150, label: 'Avec O₂' },
    { id: 'sans_o2', cx: 665, cy: 270, radius: 150, label: 'Sans O₂' },
  ],
};

export const SVT_CROQUIS_GLYCOLYSE: ScientificSchema = {
  id: 'svt_croquis_glycolyse',
  title: 'Croquis au crayon — Bilan de la glycolyse',
  subject: 'svt',
  keywords: ['glycolyse', 'bilan glycolyse', 'glucose pyruvate', '2 ATP nets', '2 NADH H+', 'cytoplasme', 'تحلل سكري'],
  metadata: {
    courseId: 'svt_ch1_energy',
    chapter: 'Consommation de la matière organique et libération de l\'énergie',
    lesson: 'Libération de l\'énergie emmagasinée dans la matière organique',
    visualStyle: 'pencil',
    resourceRole: 'teacher_sketch',
    learningObjectives: ['Établir le bilan carboné et énergétique de la glycolyse', 'Localiser la glycolyse dans le cytoplasme'],
    llmIntents: ['dessiner le bilan de la glycolyse', 'montrer le passage glucose-pyruvate', 'expliquer les 2 ATP nets'],
    drawingSteps: ['Écrire glucose C₆', 'Tracer la phase d’activation et la coupure', 'Dessiner deux pyruvates C₃', 'Ajouter le bilan net ATP et NADH,H⁺'],
  },
  category: 'process',
  viewBox: '0 0 900 520',
  layers: [
    { id: 'carbone', label: 'Carbone', delay: 0, svgContent: `
      ${PENCIL_DEFS}
      <rect x="55" y="45" width="790" height="425" rx="28" fill="none" stroke="${MUTED}" stroke-width="2" stroke-dasharray="10 8"/>
      <text x="90" y="85" font-size="18" fill="${MUTED}" font-family="${FONT}">cytoplasme</text>
      <text x="150" y="235" text-anchor="middle" font-size="28" fill="${INK}" font-family="${FONT}">Glucose</text>
      <text x="150" y="275" text-anchor="middle" font-size="23" fill="${MUTED}" font-family="${FONT}">C₆</text>
      <g fill="none" stroke="${INK}" stroke-width="3">
        <circle cx="105" cy="320" r="15"/><circle cx="123" cy="320" r="15"/><circle cx="141" cy="320" r="15"/>
        <circle cx="159" cy="320" r="15"/><circle cx="177" cy="320" r="15"/><circle cx="195" cy="320" r="15"/>
      </g>
      <path d="M230 275 C325 275 350 275 420 275" fill="none" stroke="${INK}" stroke-width="4" marker-end="url(#pencilArrow)"/>
      <path d="M470 270 C545 220 585 195 650 185" fill="none" stroke="${INK}" stroke-width="3" marker-end="url(#pencilArrow)"/>
      <path d="M470 280 C545 330 585 355 650 365" fill="none" stroke="${INK}" stroke-width="3" marker-end="url(#pencilArrow)"/>
      <text x="735" y="175" text-anchor="middle" font-size="24" fill="${INK}" font-family="${FONT}">Pyruvate C₃</text>
      <text x="735" y="355" text-anchor="middle" font-size="24" fill="${INK}" font-family="${FONT}">Pyruvate C₃</text>` },
    { id: 'energie', label: 'Bilan', delay: 650, svgContent: `
      <text x="350" y="220" text-anchor="middle" font-size="18" fill="${ALERT}" font-family="${FONT}">− 2 ATP investis</text>
      <text x="525" y="410" text-anchor="middle" font-size="18" fill="${PRODUCT}" font-family="${FONT}">+ 4 ATP formés</text>
      <path d="M300 130 Q450 95 600 130" fill="none" stroke="${ATP}" stroke-width="3"/>
      <text x="450" y="105" text-anchor="middle" font-size="24" font-weight="700" fill="${ATP}" font-family="${FONT}">gain net : 2 ATP</text>
      <text x="450" y="455" text-anchor="middle" font-size="21" fill="${OXYGEN}" font-family="${FONT}">+ 2 NADH,H⁺ · aucun O₂ consommé directement</text>` },
  ],
  annotations: [
    { id: 'carbon', x: 80, y: 150, width: 730, height: 240, label: 'Bilan carboné', description: 'Les 6 carbones du glucose se retrouvent dans deux pyruvates à 3 carbones.', color: INK },
    { id: 'energy', x: 255, y: 70, width: 390, height: 100, label: 'Bilan énergétique', description: '4 ATP sont formés mais 2 ont été investis : le gain net vaut 2 ATP.', color: ATP },
  ],
  highlights: [
    { id: 'bilan_net', cx: 450, cy: 120, radius: 150, label: '2 ATP nets' },
    { id: 'pyruvates', cx: 730, cy: 270, radius: 135, label: '2 pyruvates' },
  ],
};

export const SVT_CROQUIS_MITOCHONDRIE: ScientificSchema = {
  id: 'svt_croquis_mitochondrie',
  title: 'Croquis au crayon — Ultrastructure de la mitochondrie',
  subject: 'svt',
  keywords: ['mitochondrie', 'croquis mitochondrie', 'ultrastructure mitochondrie', 'crêtes mitochondriales', 'membrane interne externe', 'matrice mitochondriale', 'espace intermembranaire', 'ميتوكندريا', 'بنية الميتوكندريا'],
  metadata: {
    courseId: 'svt_ch1_energy',
    chapter: 'Consommation de la matière organique et libération de l\'énergie',
    lesson: 'Libération de l\'énergie emmagasinée dans la matière organique',
    visualStyle: 'pencil',
    resourceRole: 'teacher_sketch',
    learningObjectives: ['Identifier les compartiments mitochondriaux', 'Relier structure et étapes de la respiration'],
    llmIntents: ['dessiner une mitochondrie annotée', 'expliquer que les crêtes sont des replis de la membrane interne', 'localiser Krebs et chaîne respiratoire'],
    drawingSteps: ['Tracer la membrane externe', 'Tracer la membrane interne en un seul trait continu autour de la matrice', 'Former plusieurs replis de cette même membrane sur toute la longueur', 'Nommer espace intermembranaire, crêtes et matrice', 'Localiser Krebs et chaîne respiratoire'],
  },
  category: 'structure',
  viewBox: '0 0 900 520',
  layers: [
    { id: 'enveloppe', label: 'Enveloppe', delay: 0, svgContent: `
      ${PENCIL_DEFS}
      <path d="M96 290 C85 205 146 114 252 76 C371 32 514 70 590 155 C666 241 641 357 549 423 C458 488 315 492 198 440 C133 411 102 359 96 290Z" fill="none" stroke="${INK}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M129 288 C119 219 170 142 262 108 C291 98 319 91 347 88 C366 86 379 96 376 112 C373 134 348 151 328 163 C310 174 309 190 324 202 C342 217 365 208 382 190 C405 166 416 128 442 111 C460 99 484 102 499 117 C518 136 510 156 494 173 C476 193 455 207 454 229 C453 248 471 261 489 253 C513 243 526 211 548 195 C570 179 596 187 610 210 C630 242 627 286 611 321 C597 350 575 373 546 390 C528 401 509 407 490 410 C472 413 460 403 460 386 C460 361 481 340 480 317 C479 298 463 288 447 297 C424 311 417 347 400 372 C387 392 366 403 346 401 C326 399 316 383 321 365 C327 340 345 322 344 300 C343 282 327 273 311 283 C288 298 281 333 263 354 C247 373 224 376 204 365 C166 344 135 320 129 288Z" fill="none" stroke="${MUTED}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
      <text x="390" y="268" text-anchor="middle" font-size="18" fill="${PRODUCT}" font-family="${FONT}">cycle de Krebs</text>` },
    { id: 'legendes', label: 'Légendes', delay: 650, svgContent: `
      <path d="M520 92 L670 52" fill="none" stroke="${ATP}" stroke-width="2.5"/>
      <text x="690" y="46" font-size="18" fill="${ATP}" font-family="${FONT}">Espace</text>
      <text x="690" y="68" font-size="18" fill="${ATP}" font-family="${FONT}">intermembranaire</text>
      <path d="M616 181 L670 143" fill="none" stroke="${INK}" stroke-width="2.5"/>
      <text x="690" y="149" font-size="19" fill="${INK}" font-family="${FONT}">Membrane externe</text>
      <path d="M611 321 L670 229" fill="none" stroke="${MUTED}" stroke-width="2.5"/>
      <text x="690" y="235" font-size="19" fill="${MUTED}" font-family="${FONT}">Membrane interne</text>
      <path d="M505 292 L670 302" fill="none" stroke="${PRODUCT}" stroke-width="2.5"/>
      <text x="690" y="308" font-size="21" fill="${PRODUCT}" font-family="${FONT}">Matrice</text>
      <path d="M480 317 L590 417 L670 417" fill="none" stroke="${OXYGEN}" stroke-width="2.5"/>
      <text x="690" y="412" font-size="20" fill="${OXYGEN}" font-family="${FONT}">Crête</text>
      <text x="690" y="434" font-size="15" fill="${OXYGEN}" font-family="${FONT}">repli membranaire</text>` },
  ],
  annotations: [
    { id: 'matrix', x: 250, y: 185, width: 290, height: 170, label: 'Matrice', description: 'Compartiment où se déroulent l’oxydation du pyruvate et le cycle de Krebs.', color: PRODUCT },
    { id: 'inner', x: 120, y: 85, width: 515, height: 330, label: 'Membrane interne', description: 'Membrane continue dont les replis forment les crêtes et portent la chaîne respiratoire et l’ATP synthase.', color: OXYGEN },
  ],
  highlights: [
    { id: 'cretes', cx: 420, cy: 255, radius: 185, label: 'Crêtes mitochondriales' },
    { id: 'matrice', cx: 390, cy: 280, radius: 105, label: 'Matrice' },
  ],
};

export const SVT_CROQUIS_KREBS: ScientificSchema = {
  id: 'svt_croquis_krebs',
  title: 'Croquis au crayon — Bilan du cycle de Krebs',
  subject: 'svt',
  keywords: ['krebs', 'cycle de Krebs', 'bilan cycle Krebs', 'acétyl CoA oxaloacétate', 'matrice mitochondriale', 'NADH FADH2 CO2', 'دورة كريبس'],
  metadata: {
    courseId: 'svt_ch1_energy',
    chapter: 'Consommation de la matière organique et libération de l\'énergie',
    lesson: 'Libération de l\'énergie emmagasinée dans la matière organique',
    visualStyle: 'pencil',
    resourceRole: 'teacher_sketch',
    learningObjectives: ['Établir le bilan du cycle de Krebs pour un glucose', 'Montrer le rôle majeur des transporteurs réduits'],
    llmIntents: ['dessiner le cycle de Krebs', 'résumer les entrées et sorties de Krebs', 'expliquer NADH et FADH2 avant la chaîne'],
    drawingSteps: ['Tracer un cycle simple dans la matrice', 'Faire entrer deux acétyl-CoA', 'Faire sortir CO₂, NADH,H⁺, FADH₂ et ATP', 'Préciser deux tours par glucose'],
  },
  category: 'cycle',
  viewBox: '0 0 900 520',
  layers: [
    { id: 'cycle', label: 'Cycle', delay: 0, svgContent: `
      ${PENCIL_DEFS}
      <rect x="45" y="45" width="810" height="430" rx="28" fill="none" stroke="${MUTED}" stroke-width="2" stroke-dasharray="10 8"/>
      <text x="80" y="82" font-size="18" fill="${MUTED}" font-family="${FONT}">matrice mitochondriale</text>
      <path d="M360 150 C555 105 650 250 585 365 C515 485 300 420 290 275 C285 215 310 175 360 150" fill="none" stroke="${INK}" stroke-width="4" marker-end="url(#pencilArrow)"/>
      <text x="455" y="250" text-anchor="middle" font-size="31" fill="${INK}" font-family="${FONT}">Cycle de Krebs</text>
      <text x="455" y="290" text-anchor="middle" font-size="20" fill="${MUTED}" font-family="${FONT}">2 tours par glucose</text>
      <path d="M105 190 L300 205" fill="none" stroke="${INK}" stroke-width="3" marker-end="url(#pencilArrow)"/>
      <text x="100" y="155" font-size="22" fill="${INK}" font-family="${FONT}">2 acétyl-CoA</text>` },
    { id: 'bilan', label: 'Bilan', delay: 650, svgContent: `
      <path d="M590 180 L790 130" fill="none" stroke="${INK}" stroke-width="3" marker-end="url(#pencilArrow)"/>
      <text x="795" y="120" font-size="20" fill="${PRODUCT}" font-family="${FONT}">4 CO₂</text>
      <path d="M640 250 L815 250" fill="none" stroke="${INK}" stroke-width="3" marker-end="url(#pencilArrow)"/>
      <text x="815" y="238" text-anchor="end" font-size="20" fill="${OXYGEN}" font-family="${FONT}">6 NADH,H⁺</text>
      <path d="M600 330 L790 390" fill="none" stroke="${INK}" stroke-width="3" marker-end="url(#pencilArrow)"/>
      <text x="800" y="402" font-size="20" fill="${OXYGEN}" font-family="${FONT}">2 FADH₂</text>
      <path d="M355 410 L205 440" fill="none" stroke="${INK}" stroke-width="3" marker-end="url(#pencilArrow)"/>
      <text x="90" y="455" font-size="22" fill="${ATP}" font-family="${FONT}">2 ATP</text>
      <text x="450" y="505" text-anchor="middle" font-size="17" fill="${MUTED}" font-family="${FONT}">Les transporteurs réduits gardent l’essentiel de l’énergie.</text>` },
  ],
  annotations: [
    { id: 'cycle', x: 275, y: 105, width: 390, height: 330, label: 'Cycle de Krebs', description: 'Pour un glucose, le cycle tourne deux fois et régénère l’oxaloacétate.', color: INK },
    { id: 'carriers', x: 600, y: 195, width: 245, height: 230, label: 'Transporteurs réduits', description: 'NADH,H⁺ et FADH₂ livrent ensuite leurs électrons à la chaîne respiratoire.', color: OXYGEN },
  ],
  highlights: [
    { id: 'cycle_krebs', cx: 455, cy: 275, radius: 175, label: 'Cycle' },
    { id: 'transporteurs', cx: 735, cy: 300, radius: 125, label: 'Transporteurs réduits' },
  ],
};

export const SVT_CROQUIS_CHAINE_RESPIRATOIRE: ScientificSchema = {
  id: 'svt_croquis_chaine_respiratoire',
  title: 'Croquis au crayon — Chaîne respiratoire et ATP synthase',
  subject: 'svt',
  keywords: ['chaîne respiratoire', 'croquis chaîne respiratoire', 'phosphorylation oxydative', 'gradient H+', 'ATP synthase', 'dioxygène accepteur final', 'NADH électrons', 'السلسلة التنفسية', 'أكسجين'],
  metadata: {
    courseId: 'svt_ch1_energy',
    chapter: 'Consommation de la matière organique et libération de l\'énergie',
    lesson: 'Libération de l\'énergie emmagasinée dans la matière organique',
    visualStyle: 'pencil',
    resourceRole: 'teacher_sketch',
    learningObjectives: ['Distinguer flux d’électrons, pompage de H⁺ et synthèse d’ATP', 'Expliquer le rôle final de O₂'],
    llmIntents: ['dessiner la chaîne respiratoire', 'expliquer le gradient protonique', 'montrer le rôle de ATP synthase et O2'],
    drawingSteps: ['Tracer la membrane interne', 'Placer les complexes et le trajet des électrons', 'Dessiner le pompage des H⁺', 'Ajouter l’ATP synthase et le retour des H⁺'],
  },
  category: 'process',
  viewBox: '0 0 900 520',
  layers: [
    { id: 'chaine', label: 'Chaîne', delay: 0, svgContent: `
      ${PENCIL_DEFS}
      <text x="70" y="75" font-size="19" fill="${MUTED}" font-family="${FONT}">espace intermembranaire</text>
      <path d="M55 205 Q120 180 185 205 T315 205 T445 205 T575 205 T705 205 T845 205" fill="none" stroke="${INK}" stroke-width="4"/>
      <path d="M55 245 Q120 220 185 245 T315 245 T445 245 T575 245 T705 245 T845 245" fill="none" stroke="${MUTED}" stroke-width="4"/>
      <text x="70" y="470" font-size="19" fill="${MUTED}" font-family="${FONT}">matrice</text>
      <g fill="none" stroke="${INK}" stroke-width="3">
        <rect x="190" y="170" width="70" height="115" rx="18"/>
        <rect x="370" y="170" width="70" height="115" rx="18"/>
        <rect x="550" y="170" width="70" height="115" rx="18"/>
      </g>
      <text x="225" y="235" text-anchor="middle" font-size="22" fill="${INK}" font-family="${FONT}">I</text>
      <text x="405" y="235" text-anchor="middle" font-size="22" fill="${INK}" font-family="${FONT}">III</text>
      <text x="585" y="235" text-anchor="middle" font-size="22" fill="${INK}" font-family="${FONT}">IV</text>
      <path d="M105 335 C180 330 180 275 210 260 L370 260 L550 260 L690 330" fill="none" stroke="${OXYGEN}" stroke-width="3" marker-end="url(#oxygenArrow)"/>
      <text x="85" y="355" font-size="18" fill="${OXYGEN}" font-family="${FONT}">NADH,H⁺ → e⁻</text>
      <text x="700" y="350" font-size="18" fill="${OXYGEN}" font-family="${FONT}">O₂ → H₂O</text>` },
    { id: 'gradient', label: 'Gradient et ATP', delay: 650, svgContent: `
      <g fill="none" stroke="${ATP}" stroke-width="3" marker-end="url(#pencilArrow)">
        <path d="M225 180 L225 105"/><path d="M405 180 L405 105"/><path d="M585 180 L585 105"/>
      </g>
      <g fill="none" stroke="${ATP}" stroke-width="2">
        <circle cx="190" cy="110" r="12"/><circle cx="265" cy="105" r="12"/><circle cx="365" cy="110" r="12"/>
        <circle cx="445" cy="105" r="12"/><circle cx="545" cy="110" r="12"/><circle cx="625" cy="105" r="12"/>
      </g>
      <text x="410" y="65" text-anchor="middle" font-size="20" fill="${ATP}" font-family="${FONT}">accumulation de H⁺</text>
      <path d="M735 165 L790 165 L790 285 L735 285Z" fill="none" stroke="${PRODUCT}" stroke-width="4"/>
      <circle cx="762" cy="305" r="34" fill="none" stroke="${PRODUCT}" stroke-width="4"/>
      <path d="M760 105 L760 270" fill="none" stroke="${PRODUCT}" stroke-width="3" marker-end="url(#pencilArrow)"/>
      <text x="760" y="390" text-anchor="middle" font-size="18" fill="${PRODUCT}" font-family="${FONT}">ATP synthase</text>
      <text x="760" y="430" text-anchor="middle" font-size="22" fill="${ATP}" font-family="${FONT}">ADP + Pi → ATP</text>` },
  ],
  annotations: [
    { id: 'electrons', x: 80, y: 250, width: 660, height: 135, label: 'Flux d’électrons', description: 'Les électrons des transporteurs réduits passent entre les complexes jusqu’au dioxygène, accepteur final.', color: OXYGEN },
    { id: 'gradient', x: 160, y: 45, width: 500, height: 150, label: 'Gradient de protons', description: 'L’énergie des transferts pompe des H⁺ vers l’espace intermembranaire.', color: ATP },
    { id: 'synthase', x: 700, y: 120, width: 150, height: 330, label: 'ATP synthase', description: 'Le retour des H⁺ vers la matrice fournit l’énergie de phosphorylation de l’ADP.', color: PRODUCT },
  ],
  highlights: [
    { id: 'flux_electrons', cx: 405, cy: 300, radius: 190, label: 'Électrons' },
    { id: 'gradient_h', cx: 405, cy: 105, radius: 160, label: 'Gradient H⁺' },
    { id: 'atp_synthase', cx: 760, cy: 265, radius: 95, label: 'ATP synthase' },
  ],
};

export const SVT_CROQUIS_RESPIRATION_FERMENTATION: ScientificSchema = {
  id: 'svt_croquis_respiration_fermentation',
  title: 'Croquis au crayon — Respiration ou fermentation',
  subject: 'svt',
  keywords: ['respiration', 'fermentation', 'respiration versus fermentation', 'avec sans dioxygène', 'pyruvate bifurcation', 'rendement ATP comparé', 'fermentation lactique alcoolique', 'تنفس', 'تخمر'],
  metadata: {
    courseId: 'svt_ch1_energy',
    chapter: 'Consommation de la matière organique et libération de l\'énergie',
    lesson: 'Libération de l\'énergie emmagasinée dans la matière organique',
    visualStyle: 'pencil',
    resourceRole: 'teacher_sketch',
    learningObjectives: ['Comparer respiration et fermentation', 'Expliquer l’effet de O₂ sur l’oxydation et le rendement'],
    llmIntents: ['dessiner la bifurcation respiration-fermentation', 'comparer les voies avec et sans O2', 'expliquer pourquoi la respiration produit plus ATP'],
    drawingSteps: ['Tracer la glycolyse commune', 'Faire bifurquer les pyruvates selon la présence de O₂', 'Écrire les produits finaux', 'Comparer les rendements ATP'],
  },
  category: 'comparison',
  viewBox: '0 0 900 520',
  layers: [
    { id: 'commun', label: 'Voie commune', delay: 0, svgContent: `
      ${PENCIL_DEFS}
      <text x="450" y="65" text-anchor="middle" font-size="27" fill="${INK}" font-family="${FONT}">Glucose C₆</text>
      <path d="M450 85 L450 155" fill="none" stroke="${INK}" stroke-width="3" marker-end="url(#pencilArrow)"/>
      <rect x="335" y="160" width="230" height="62" rx="18" fill="none" stroke="${MUTED}" stroke-width="3"/>
      <text x="450" y="199" text-anchor="middle" font-size="24" fill="${INK}" font-family="${FONT}">Glycolyse : +2 ATP</text>
      <path d="M450 225 L450 275" fill="none" stroke="${INK}" stroke-width="3" marker-end="url(#pencilArrow)"/>
      <text x="450" y="305" text-anchor="middle" font-size="24" fill="${INK}" font-family="${FONT}">2 pyruvates C₃</text>` },
    { id: 'branches', label: 'Deux voies', delay: 650, svgContent: `
      <path d="M400 315 C330 350 250 365 180 385" fill="none" stroke="${OXYGEN}" stroke-width="3" marker-end="url(#oxygenArrow)"/>
      <path d="M500 315 C570 350 650 365 720 385" fill="none" stroke="${INK}" stroke-width="3" marker-end="url(#pencilArrow)"/>
      <text x="250" y="340" text-anchor="middle" font-size="20" fill="${OXYGEN}" font-family="${FONT}">avec O₂</text>
      <text x="650" y="340" text-anchor="middle" font-size="20" fill="${ALERT}" font-family="${FONT}">sans O₂</text>
      <rect x="55" y="385" width="310" height="105" rx="20" fill="none" stroke="${OXYGEN}" stroke-width="3"/>
      <text x="210" y="420" text-anchor="middle" font-size="23" fill="${OXYGEN}" font-family="${FONT}">Respiration</text>
      <text x="210" y="452" text-anchor="middle" font-size="18" fill="${PRODUCT}" font-family="${FONT}">CO₂ + H₂O</text>
      <text x="210" y="478" text-anchor="middle" font-size="18" fill="${ATP}" font-family="${FONT}">plusieurs dizaines d’ATP</text>
      <rect x="535" y="385" width="310" height="105" rx="20" fill="none" stroke="${ALERT}" stroke-width="3"/>
      <text x="690" y="420" text-anchor="middle" font-size="23" fill="${ALERT}" font-family="${FONT}">Fermentation</text>
      <text x="690" y="452" text-anchor="middle" font-size="17" fill="${PRODUCT}" font-family="${FONT}">lactate ou éthanol + CO₂</text>
      <text x="690" y="478" text-anchor="middle" font-size="18" fill="${ATP}" font-family="${FONT}">2 ATP nets</text>` },
  ],
  annotations: [
    { id: 'common', x: 315, y: 35, width: 270, height: 285, label: 'Étape commune', description: 'La glycolyse précède aussi bien la respiration que les fermentations.', color: MUTED },
    { id: 'respiration', x: 45, y: 330, width: 330, height: 170, label: 'Respiration', description: 'En présence de dioxygène, le glucose est oxydé plus complètement et le rendement est élevé.', color: OXYGEN },
    { id: 'fermentation', x: 525, y: 330, width: 330, height: 170, label: 'Fermentation', description: 'Sans dioxygène, les produits restent organiques et le gain se limite aux 2 ATP nets de la glycolyse.', color: ALERT },
  ],
  highlights: [
    { id: 'voie_commune', cx: 450, cy: 185, radius: 145, label: 'Glycolyse' },
    { id: 'comparaison', cx: 450, cy: 420, radius: 390, label: 'Deux voies' },
  ],
};

export const SVT_CROQUIS_BILAN_RESPIRATION: ScientificSchema = {
  id: 'svt_croquis_bilan_respiration',
  title: 'Croquis au crayon — Bilan de la respiration cellulaire',
  subject: 'svt',
  keywords: ['respiration cellulaire', 'bilan respiration cellulaire', 'glucose O2 CO2 H2O ATP', 'glycolyse Krebs chaîne respiratoire', 'bilan énergétique global', 'libération énergie', 'تنفس خلوي'],
  metadata: {
    courseId: 'svt_ch1_energy',
    chapter: 'Consommation de la matière organique et libération de l\'énergie',
    lesson: 'Libération de l\'énergie emmagasinée dans la matière organique',
    visualStyle: 'pencil',
    resourceRole: 'teacher_sketch',
    learningObjectives: ['Organiser les étapes de la respiration et leurs lieux', 'Construire le bilan global de l’oxydation du glucose'],
    llmIntents: ['dessiner le schéma-bilan de la respiration', 'résumer tout le premier cours', 'relier glycolyse Krebs chaîne et ATP'],
    drawingSteps: ['Écrire le glucose à l’entrée', 'Aligner glycolyse, Krebs et chaîne respiratoire', 'Associer cytoplasme, matrice et membrane interne', 'Ajouter O₂, CO₂, H₂O, ATP et chaleur'],
  },
  category: 'diagram',
  viewBox: '0 0 900 520',
  layers: [
    { id: 'etapes', label: 'Étapes', delay: 0, svgContent: `
      ${PENCIL_DEFS}
      <text x="95" y="185" text-anchor="middle" font-size="24" fill="${INK}" font-family="${FONT}">Glucose</text>
      <path d="M150 180 L230 180" fill="none" stroke="${INK}" stroke-width="3" marker-end="url(#pencilArrow)"/>
      <rect x="235" y="125" width="170" height="110" rx="22" fill="none" stroke="${MUTED}" stroke-width="3"/>
      <text x="320" y="175" text-anchor="middle" font-size="23" fill="${INK}" font-family="${FONT}">Glycolyse</text>
      <text x="320" y="207" text-anchor="middle" font-size="17" fill="${MUTED}" font-family="${FONT}">cytoplasme</text>
      <path d="M410 180 L490 180" fill="none" stroke="${INK}" stroke-width="3" marker-end="url(#pencilArrow)"/>
      <ellipse cx="650" cy="250" rx="155" ry="150" fill="none" stroke="${INK}" stroke-width="4"/>
      <path d="M518 250 C518 170 575 116 641 112 C658 111 670 119 668 132 C665 150 646 166 638 181 C632 193 640 205 652 205 C670 205 681 184 693 168 C706 151 727 151 739 166 C751 181 747 196 737 210 C726 225 714 236 717 250 C720 264 734 270 745 262 C759 252 765 232 780 226 C792 222 801 232 803 245 C807 280 792 319 765 345 C751 359 735 368 717 375 C702 380 690 372 690 358 C691 339 707 323 706 306 C705 293 694 286 683 293 C668 303 663 327 651 340 C640 352 623 352 612 341 C601 330 604 316 614 304 C626 289 638 278 635 265 C632 252 619 247 608 256 C592 269 587 293 573 304 C558 315 540 307 530 292 C522 280 518 265 518 250Z" fill="none" stroke="${MUTED}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
      <text x="660" y="235" text-anchor="middle" font-size="22" fill="${PRODUCT}" font-family="${FONT}">Krebs</text>
      <text x="660" y="264" text-anchor="middle" font-size="17" fill="${MUTED}" font-family="${FONT}">matrice</text>
      <text x="650" y="355" text-anchor="middle" font-size="21" fill="${OXYGEN}" font-family="${FONT}">chaîne respiratoire</text>
      <text x="650" y="385" text-anchor="middle" font-size="16" fill="${MUTED}" font-family="${FONT}">membrane interne</text>` },
    { id: 'bilan', label: 'Bilan global', delay: 650, svgContent: `
      <path d="M320 100 C400 45 515 45 560 105" fill="none" stroke="${OXYGEN}" stroke-width="3" marker-end="url(#oxygenArrow)"/>
      <text x="455" y="42" text-anchor="middle" font-size="22" fill="${OXYGEN}" font-family="${FONT}">O₂ consommé en fin de chaîne</text>
      <path d="M730 120 L825 75" fill="none" stroke="${INK}" stroke-width="3" marker-end="url(#pencilArrow)"/>
      <text x="830" y="65" text-anchor="end" font-size="20" fill="${PRODUCT}" font-family="${FONT}">CO₂</text>
      <path d="M775 245 L850 245" fill="none" stroke="${INK}" stroke-width="3" marker-end="url(#pencilArrow)"/>
      <text x="850" y="235" text-anchor="end" font-size="20" fill="${PRODUCT}" font-family="${FONT}">H₂O</text>
      <path d="M650 405 L650 470" fill="none" stroke="${ATP}" stroke-width="3" marker-end="url(#pencilArrow)"/>
      <text x="650" y="505" text-anchor="middle" font-size="25" font-weight="700" fill="${ATP}" font-family="${FONT}">ATP + chaleur</text>
      <text x="240" y="430" font-size="22" fill="${INK}" font-family="${FONT}">Glucose + O₂</text>
      <text x="430" y="430" font-size="22" fill="${INK}" font-family="${FONT}">→</text>
      <text x="470" y="430" font-size="22" fill="${PRODUCT}" font-family="${FONT}">CO₂ + H₂O</text>` },
  ],
  annotations: [
    { id: 'glycolysis', x: 220, y: 105, width: 200, height: 150, label: 'Glycolyse', description: 'Dans le cytoplasme : glucose → 2 pyruvates, 2 ATP nets et 2 NADH,H⁺.', color: MUTED },
    { id: 'mitochondrial', x: 485, y: 80, width: 330, height: 350, label: 'Étapes mitochondriales', description: 'Le cycle de Krebs fournit les transporteurs réduits ; la chaîne respiratoire produit la majorité de l’ATP.', color: OXYGEN },
    { id: 'equation', x: 210, y: 395, width: 410, height: 70, label: 'Bilan global', description: 'L’oxydation complète du glucose consomme du dioxygène et produit CO₂, H₂O, ATP et chaleur.', color: PRODUCT },
  ],
  highlights: [
    { id: 'glycolyse', cx: 320, cy: 180, radius: 100, label: 'Glycolyse' },
    { id: 'mitochondrie', cx: 650, cy: 250, radius: 170, label: 'Mitochondrie' },
    { id: 'atp', cx: 650, cy: 465, radius: 120, label: 'ATP' },
  ],
};

export const SVT_ENERGY_PENCIL_SKETCHES = [
  SVT_CROQUIS_CELLULE_MITOCHONDRIE,
  SVT_CROQUIS_ATP_ADP,
  SVT_CROQUIS_EXPERIENCE_LEVURES,
  SVT_CROQUIS_GLYCOLYSE,
  SVT_CROQUIS_MITOCHONDRIE,
  SVT_CROQUIS_KREBS,
  SVT_CROQUIS_CHAINE_RESPIRATOIRE,
  SVT_CROQUIS_RESPIRATION_FERMENTATION,
  SVT_CROQUIS_BILAN_RESPIRATION,
] as const;
