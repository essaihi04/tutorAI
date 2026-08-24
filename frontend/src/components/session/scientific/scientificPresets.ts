import type {
  CytoscapeEdgeSpec,
  CytoscapeNodeSpec,
  CytoscapeVisualSpec,
  JSXGraphElementSpec,
  JSXGraphVisualSpec,
  ScientificPoint,
  ScientificPresetId,
  ScientificVisualSpec,
} from './types';

export interface ScientificPresetVariant {
  id: string;
  label: string;
}

export interface ScientificPresetMeta {
  id: ScientificPresetId;
  title: string;
  variants: ScientificPresetVariant[];
  defaultVariant: string;
  maxStep: number;
  frameMs: number;
}

export const SCIENTIFIC_PRESETS: Record<ScientificPresetId, ScientificPresetMeta> = {
  svt_ch1_cycle_atp: {
    id: 'svt_ch1_cycle_atp',
    title: 'Cycle ATP–ADP',
    defaultVariant: 'cycle_complet',
    variants: [
      { id: 'cycle_complet', label: 'Cycle complet' },
      { id: 'hydrolyse', label: 'Hydrolyse' },
      { id: 'phosphorylation', label: 'Phosphorylation' },
      { id: 'couplage', label: 'Couplage énergétique' },
    ],
    maxStep: 5,
    frameMs: 850,
  },
  svt_ch1_levures_exao: {
    id: 'svt_ch1_levures_exao',
    title: 'Levures : respiration ou fermentation',
    defaultVariant: 'comparaison',
    variants: [
      { id: 'comparaison', label: 'Comparer' },
      { id: 'avec_oxygene', label: 'Avec O₂' },
      { id: 'sans_oxygene', label: 'Sans O₂' },
    ],
    maxStep: 24,
    frameMs: 180,
  },
  svt_ch1_chimiosmose: {
    id: 'svt_ch1_chimiosmose',
    title: 'Chaîne respiratoire et chimiosmose',
    defaultVariant: 'cycle_complet',
    variants: [
      { id: 'cycle_complet', label: 'Vue complète' },
      { id: 'transfert_electrons', label: 'Électrons' },
      { id: 'pompage_protons', label: 'Pompage H⁺' },
      { id: 'synthese_atp', label: 'Synthèse d’ATP' },
    ],
    maxStep: 7,
    frameMs: 800,
  },
  svt_ch1_carte_metabolique: {
    id: 'svt_ch1_carte_metabolique',
    title: 'De la matière organique à l’ATP',
    defaultVariant: 'vue_ensemble',
    variants: [
      { id: 'vue_ensemble', label: 'Vue d’ensemble' },
      { id: 'respiration', label: 'Respiration' },
      { id: 'fermentation_lactique', label: 'Fermentation lactique' },
      { id: 'fermentation_alcoolique', label: 'Fermentation alcoolique' },
    ],
    maxStep: 8,
    frameMs: 720,
  },
  svt_ch1_myogrammes: {
    id: 'svt_ch1_myogrammes',
    title: 'Réponses mécaniques du muscle',
    defaultVariant: 'secousse',
    variants: [
      { id: 'secousse', label: 'Secousse' },
      { id: 'sommation', label: 'Sommation' },
      { id: 'tetanus_incomplet', label: 'Tétanos incomplet' },
      { id: 'tetanus_complet', label: 'Tétanos complet' },
    ],
    maxStep: 32,
    frameMs: 110,
  },
  svt_ch1_cycle_actomyosine: {
    id: 'svt_ch1_cycle_actomyosine',
    title: 'Cycle des ponts actine–myosine',
    defaultVariant: 'cycle_complet',
    variants: [
      { id: 'cycle_complet', label: 'Cycle complet' },
      { id: 'fixation', label: '1. Fixation' },
      { id: 'pivotement', label: '2. Pivotement' },
      { id: 'detachement', label: '3. Détachement' },
      { id: 'reactivation', label: '4. Réactivation' },
    ],
    maxStep: 5,
    frameMs: 900,
  },
  svt_ch1_filieres_effort: {
    id: 'svt_ch1_filieres_effort',
    title: 'Régénération de l’ATP pendant l’effort',
    defaultVariant: 'vue_ensemble',
    variants: [
      { id: 'vue_ensemble', label: 'Vue d’ensemble' },
      { id: 'effort_bref', label: 'Effort bref' },
      { id: 'effort_intense', label: 'Effort intense' },
      { id: 'effort_prolonge', label: 'Effort prolongé' },
      { id: 'recuperation', label: 'Récupération' },
    ],
    maxStep: 7,
    frameMs: 760,
  },
};

const INACTIVE_NODE = '#334155';
const ACTIVE_NODE = '#0891b2';
const ACTIVE_END = '#f97316';
const INACTIVE_EDGE = '#64748b';
const ACTIVE_EDGE = '#22d3ee';

function revealedCount(length: number, step: number, maxStep: number): number {
  if (length <= 0) return 0;
  const safeStep = Math.max(0, Math.min(maxStep, Math.round(step)));
  return Math.max(1, Math.ceil((safeStep / maxStep) * length));
}

function processSpec(
  title: string,
  layout: CytoscapeVisualSpec['layout'],
  rawNodes: Array<[string, string]>,
  rawEdges: Array<[string, string, string?]>,
  activePath: string[],
  step: number,
  maxStep: number,
): CytoscapeVisualSpec {
  const count = revealedCount(activePath.length, step, maxStep);
  const activeNodes = new Set(activePath.slice(0, count));
  const activePairs = new Set(
    activePath.slice(0, Math.max(0, count - 1)).map((id, index) => `${id}>${activePath[index + 1]}`),
  );
  const nodes: CytoscapeNodeSpec[] = rawNodes.map(([id, label]) => ({
    id,
    label,
    active: activeNodes.has(id),
    color: activeNodes.has(id)
      ? (id === activePath[Math.min(count - 1, activePath.length - 1)] ? ACTIVE_END : ACTIVE_NODE)
      : INACTIVE_NODE,
  }));
  const edges: CytoscapeEdgeSpec[] = rawEdges.map(([from, to, label]) => {
    const active = activePairs.has(`${from}>${to}`);
    return { from, to, label, active, color: active ? ACTIVE_EDGE : INACTIVE_EDGE };
  });
  return { engine: 'cytoscape', title, layout, nodes, edges };
}

function pointsToSegments(
  id: string,
  points: ScientificPoint[],
  color: string,
  label: string,
  step: number,
  maxStep: number,
  labelPoint?: ScientificPoint,
): JSXGraphElementSpec[] {
  const visible = Math.min(points.length, revealedCount(points.length, step, maxStep));
  const shown = points.slice(0, visible);
  const segments: JSXGraphElementSpec[] = shown.slice(1).map((point, index) => ({
    id: `${id}-${index}`,
    type: 'segment',
    points: [shown[index], point],
    color,
  }));
  const last = shown[shown.length - 1];
  if (last && visible === points.length) {
    segments.push({ id: `${id}-label`, type: 'text', points: [labelPoint || last], label, color });
  }
  return segments;
}

function samples(fn: (x: number) => number, from = 0, to = 12, count = 49): ScientificPoint[] {
  return Array.from({ length: count }, (_, index) => {
    const x = from + ((to - from) * index) / (count - 1);
    return { x, y: fn(x) };
  });
}

function levuresSpec(variant: string, step: number, maxStep: number): JSXGraphVisualSpec {
  const avecOxygene = [
    { id: 'o2-aero', label: 'O₂ avec O₂', color: 'cyan', points: samples(x => 18 - 0.8 * x), labelPoint: { x: 6.5, y: 13.6 } },
    { id: 'co2-aero', label: 'CO₂ avec O₂', color: 'green', points: samples(x => 2 + 0.75 * x), labelPoint: { x: 8.2, y: 9.2 } },
    { id: 'eth-aero', label: 'Éthanol avec O₂', color: 'purple', points: samples(() => 0.8), labelPoint: { x: 4.3, y: 1.55 } },
  ];
  const sansOxygene = [
    { id: 'o2-ana', label: 'O₂ sans O₂', color: 'blue', points: samples(() => 0.5), labelPoint: { x: 11.2, y: 1.5 } },
    { id: 'co2-ana', label: 'CO₂ sans O₂', color: 'orange', points: samples(x => 2 + 0.45 * x), labelPoint: { x: 5.6, y: 5.3 } },
    { id: 'eth-ana', label: 'Éthanol sans O₂', color: 'red', points: samples(x => 0.8 + 0.62 * x), labelPoint: { x: 11.2, y: 8.5 } },
  ];
  const selected = variant === 'avec_oxygene'
    ? avecOxygene
    : variant === 'sans_oxygene'
      ? sansOxygene
      : [...avecOxygene, ...sansOxygene];
  return {
    engine: 'jsxgraph',
    title: 'Évolution relative des substances chez les levures',
    boundingBox: [-0.7, 21, 15.8, -1.8],
    axis: true,
    grid: true,
    xLabel: 'Temps (min)',
    yLabel: 'Valeur relative (u.a.)',
    elements: selected.flatMap(series => pointsToSegments(
      series.id, series.points, series.color, series.label, step, maxStep, series.labelPoint,
    )),
  };
}

function twitch(t: number, onset: number): number {
  const z = t - onset;
  return z <= 0 ? 0 : 8.2 * z * Math.exp(-1.75 * z);
}

function myogramPoints(variant: string): ScientificPoint[] {
  const onsets = variant === 'secousse' ? [1]
    : variant === 'sommation' ? [1, 2.1]
      : variant === 'tetanus_incomplet' ? [1, 1.85, 2.7, 3.55, 4.4, 5.25, 6.1]
        : Array.from({ length: 25 }, (_, index) => 1 + index * 0.24);
  return samples(
    time => Math.min(7.3, onsets.reduce((force, onset) => force + twitch(time, onset), 0)),
    0, 8, 97,
  );
}

function myogramSpec(variant: string, step: number, maxStep: number): JSXGraphVisualSpec {
  const label = SCIENTIFIC_PRESETS.svt_ch1_myogrammes.variants.find(v => v.id === variant)?.label || 'Myogramme';
  return {
    engine: 'jsxgraph',
    title: label,
    boundingBox: [-0.5, 8.5, 9, -0.8],
    axis: true,
    grid: true,
    xLabel: 'Temps (u.a.)',
    yLabel: 'Tension musculaire (u.a.)',
    elements: pointsToSegments('myogramme', myogramPoints(variant), 'orange', label, step, maxStep),
  };
}

function atpSpec(variant: string, step: number, maxStep: number): CytoscapeVisualSpec {
  const paths: Record<string, string[]> = {
    hydrolyse: ['atp', 'adp', 'travail'],
    phosphorylation: ['nutriments', 'adp', 'atp'],
    couplage: ['nutriments', 'atp', 'travail', 'adp'],
    cycle_complet: ['nutriments', 'adp', 'atp', 'travail'],
  };
  return processSpec(
    'L’ATP transfère l’énergie aux activités cellulaires', 'circle',
    [
      ['nutriments', 'Énergie de la respiration / fermentation'],
      ['adp', 'ADP + Pi'],
      ['atp', 'ATP'],
      ['travail', 'Travail cellulaire'],
    ],
    [
      ['nutriments', 'adp', 'Phosphorylation'],
      ['adp', 'atp', '+ énergie'],
      ['atp', 'travail', 'Hydrolyse : énergie libérée'],
      ['atp', 'adp', 'ATP → ADP + Pi'],
      ['travail', 'adp', 'Après transfert'],
    ],
    paths[variant] || paths.cycle_complet, step, maxStep,
  );
}

function chimiosmoseSpec(variant: string, step: number, maxStep: number): CytoscapeVisualSpec {
  const paths: Record<string, string[]> = {
    transfert_electrons: ['nadh', 'electrons', 'complexes', 'o2', 'h2o'],
    pompage_protons: ['electrons', 'complexes', 'pompage', 'gradient'],
    synthese_atp: ['gradient', 'atpsynthase', 'adp', 'atp'],
    cycle_complet: ['nadh', 'electrons', 'complexes', 'pompage', 'gradient', 'atpsynthase', 'atp'],
  };
  return processSpec(
    'Membrane interne mitochondriale', 'breadthfirst',
    [
      ['nadh', 'NADH,H⁺ / FADH₂'], ['electrons', 'Électrons'],
      ['complexes', 'Complexes respiratoires'], ['pompage', 'Pompage des H⁺'],
      ['gradient', 'Gradient de H⁺'], ['atpsynthase', 'ATP synthase : ADP + Pi'],
      ['atp', 'ATP'], ['o2', 'O₂ accepteur final'], ['h2o', 'H₂O'],
    ],
    [
      ['nadh', 'electrons', 'Oxydation'], ['electrons', 'complexes', 'Transfert'],
      ['complexes', 'pompage', 'Énergie'], ['pompage', 'gradient', 'H⁺ accumulés'],
      ['gradient', 'atpsynthase', 'Retour des H⁺'],
      ['atpsynthase', 'atp', 'Phosphorylation'], ['complexes', 'o2', 'e⁻'],
      ['o2', 'h2o', '+ H⁺'],
    ],
    paths[variant] || paths.cycle_complet, step, maxStep,
  );
}

const METABOLIC_NODES: Array<[string, string]> = [
  ['glucose', 'Glucose'], ['glycolyse', 'Glycolyse (cytosol)'], ['pyruvate', 'Pyruvate'],
  ['acetyl', 'Acétyl-CoA'], ['krebs', 'Cycle de Krebs'], ['chaine', 'Chaîne respiratoire'],
  ['atp', 'ATP'], ['lactate', 'Lactate'], ['ethanol', 'Éthanol + CO₂'], ['travail', 'Activités cellulaires'],
];
const METABOLIC_EDGES: Array<[string, string, string?]> = [
  ['glucose', 'glycolyse', 'Oxydation partielle'], ['glycolyse', 'pyruvate', '2 ATP + coenzymes réduits'],
  ['pyruvate', 'acetyl', 'Avec O₂'], ['acetyl', 'krebs', 'CO₂'],
  ['krebs', 'chaine', 'NADH / FADH₂'], ['chaine', 'atp', 'ATP'],
  ['pyruvate', 'lactate', 'Sans O₂'], ['pyruvate', 'ethanol', 'Sans O₂'],
  ['glycolyse', 'atp'], ['atp', 'travail', 'Hydrolyse'],
];

function metabolicSpec(variant: string, step: number, maxStep: number): CytoscapeVisualSpec {
  const paths: Record<string, string[]> = {
    respiration: ['glucose', 'glycolyse', 'pyruvate', 'acetyl', 'krebs', 'chaine', 'atp', 'travail'],
    fermentation_lactique: ['glucose', 'glycolyse', 'pyruvate', 'lactate'],
    fermentation_alcoolique: ['glucose', 'glycolyse', 'pyruvate', 'ethanol'],
    vue_ensemble: ['glucose', 'glycolyse', 'pyruvate', 'acetyl', 'krebs', 'chaine', 'atp', 'travail'],
  };
  return processSpec(
    'Respiration et fermentations : voies comparées', 'breadthfirst',
    METABOLIC_NODES, METABOLIC_EDGES, paths[variant] || paths.vue_ensemble, step, maxStep,
  );
}

function actomyosineSpec(variant: string, step: number, maxStep: number): CytoscapeVisualSpec {
  const cycle = ['ca', 'fixation', 'pivotement', 'detachement', 'reactivation'];
  const single: Record<string, string[]> = {
    fixation: ['ca', 'fixation'], pivotement: ['fixation', 'pivotement'],
    detachement: ['pivotement', 'detachement'], reactivation: ['detachement', 'reactivation'],
    cycle_complet: cycle,
  };
  return processSpec(
    'Le Ca²⁺ autorise le cycle ; l’ATP détache puis réactive la myosine', 'circle',
    [
      ['ca', 'Ca²⁺ : sites de l’actine exposés'],
      ['fixation', 'Tête de myosine–ADP–Pi fixée'],
      ['pivotement', 'Pivotement : filaments glissent'],
      ['detachement', 'ATP fixé : détachement'],
      ['reactivation', 'ATP hydrolysé : tête réarmée'],
    ],
    [
      ['ca', 'fixation', 'Formation du pont'], ['fixation', 'pivotement', 'Pi puis ADP libérés'],
      ['pivotement', 'detachement', 'Fixation d’ATP'], ['detachement', 'reactivation', 'Hydrolyse de l’ATP'],
      ['reactivation', 'fixation', 'Nouveau cycle si Ca²⁺'],
    ],
    single[variant] || cycle, step, maxStep,
  );
}

function filieresSpec(variant: string, step: number, maxStep: number): CytoscapeVisualSpec {
  const paths: Record<string, string[]> = {
    effort_bref: ['stock_atp', 'contraction'],
    effort_intense: ['glycogene', 'glycolyse', 'atp', 'contraction'],
    effort_prolonge: ['substrats', 'respiration', 'atp', 'contraction'],
    recuperation: ['o2', 'respiration', 'pc', 'atp'],
    vue_ensemble: ['substrats', 'respiration', 'atp', 'contraction'],
  };
  return processSpec(
    'Les filières régénèrent le même ATP à des vitesses et capacités différentes', 'breadthfirst',
    [
      ['stock_atp', 'Faible stock d’ATP'], ['pc', 'Phosphocréatine'],
      ['glycogene', 'Glycogène / glucose'], ['glycolyse', 'Glycolyse anaérobie'],
      ['substrats', 'Glucose + lipides + O₂'], ['o2', 'O₂ de récupération'],
      ['respiration', 'Respiration mitochondriale'], ['atp', 'ATP régénéré'],
      ['contraction', 'Contraction musculaire'], ['lactate', 'Lactate'],
    ],
    [
      ['stock_atp', 'contraction', 'Immédiat'], ['pc', 'atp'],
      ['glycogene', 'glycolyse', 'Sans O₂'], ['glycolyse', 'atp'],
      ['glycolyse', 'lactate'], ['substrats', 'respiration', 'Avec O₂'],
      ['o2', 'respiration', 'Récupération'], ['respiration', 'atp'],
      ['atp', 'contraction', 'Hydrolyse'], ['respiration', 'pc', 'Reconstitution'],
    ],
    paths[variant] || paths.vue_ensemble, step, maxStep,
  );
}

export function normalizePresetVariant(meta: ScientificPresetMeta, variant?: string): string {
  return meta.variants.some(item => item.id === variant) ? variant as string : meta.defaultVariant;
}

export function resolveScientificPreset(
  presetId: ScientificPresetId,
  variant: string,
  step: number,
): ScientificVisualSpec {
  const meta = SCIENTIFIC_PRESETS[presetId];
  const safeVariant = normalizePresetVariant(meta, variant);
  switch (presetId) {
    case 'svt_ch1_cycle_atp': return atpSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_levures_exao': return levuresSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_chimiosmose': return chimiosmoseSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_carte_metabolique': return metabolicSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_myogrammes': return myogramSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_cycle_actomyosine': return actomyosineSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_filieres_effort': return filieresSpec(safeVariant, step, meta.maxStep);
  }
}
