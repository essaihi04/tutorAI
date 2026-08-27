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
  phys_ch1_propagation_onde: {
    id: 'phys_ch1_propagation_onde',
    title: 'Propagation, retard et superposition d’une onde',
    defaultVariant: 'propagation',
    variants: [
      { id: 'propagation', label: 'Propagation' },
      { id: 'retard', label: 'Retard entre deux points' },
      { id: 'superposition', label: 'Superposition' },
    ],
    maxStep: 40,
    frameMs: 140,
  },
  phys_ch1_types_ondes: {
    id: 'phys_ch1_types_ondes',
    title: 'Ondes transversales et longitudinales',
    defaultVariant: 'comparaison',
    variants: [
      { id: 'comparaison', label: 'Comparer' },
      { id: 'transversale', label: 'Onde transversale' },
      { id: 'longitudinale', label: 'Onde longitudinale' },
    ],
    maxStep: 40,
    frameMs: 140,
  },
  phys_ch1_celerite_corde: {
    id: 'phys_ch1_celerite_corde',
    title: 'Célérité d’une onde sur une corde',
    defaultVariant: 'forte_tension',
    variants: [
      { id: 'forte_tension', label: 'Tension plus forte' },
      { id: 'faible_tension', label: 'Tension plus faible' },
      { id: 'forte_masse_lineique', label: 'Masse linéique plus forte' },
    ],
    maxStep: 40,
    frameMs: 140,
  },
  chem_ch1_facteurs_cinetiques: {
    id: 'chem_ch1_facteurs_cinetiques',
    title: 'Facteurs cinétiques',
    defaultVariant: 'temperature',
    variants: [
      { id: 'temperature', label: 'Température' },
      { id: 'concentration', label: 'Concentration' },
      { id: 'catalyseur', label: 'Catalyseur' },
      { id: 'surface_contact', label: 'Surface de contact' },
    ],
    maxStep: 36,
    frameMs: 160,
  },
  chem_ch1_energie_activation: {
    id: 'chem_ch1_energie_activation',
    title: 'Énergie d’activation et catalyse',
    defaultVariant: 'comparaison',
    variants: [
      { id: 'comparaison', label: 'Comparer les deux voies' },
      { id: 'sans_catalyseur', label: 'Sans catalyseur' },
      { id: 'avec_catalyseur', label: 'Avec catalyseur' },
    ],
    maxStep: 36,
    frameMs: 160,
  },
  chem_ch1_oxydoreduction: {
    id: 'chem_ch1_oxydoreduction',
    title: 'Transfert d’électrons en oxydoréduction',
    defaultVariant: 'transfert_direct',
    variants: [
      { id: 'transfert_direct', label: 'Transfert direct' },
      { id: 'pile', label: 'Pile' },
      { id: 'electrolyse', label: 'Électrolyse' },
    ],
    maxStep: 7,
    frameMs: 720,
  },
  svt_ch1_respiration_mitochondriale: {
    id: 'svt_ch1_respiration_mitochondriale',
    title: 'Bilan de la respiration mitochondriale',
    defaultVariant: 'bilan',
    variants: [
      { id: 'bilan', label: 'Bilan complet' },
      { id: 'krebs', label: 'Cycle de Krebs' },
      { id: 'chaine_respiratoire', label: 'Chaîne respiratoire' },
    ],
    maxStep: 9,
    frameMs: 700,
  },
  svt_ch1_glissement_sarcomere: {
    id: 'svt_ch1_glissement_sarcomere',
    title: 'Glissement des filaments et raccourcissement du sarcomère',
    defaultVariant: 'contraction',
    variants: [
      { id: 'repos', label: 'Au repos' },
      { id: 'contraction', label: 'Pendant la contraction' },
      { id: 'comparaison', label: 'Comparer repos et contraction' },
    ],
    maxStep: 30,
    frameMs: 170,
  },
  svt_ch1_couplage_excitation_contraction: {
    id: 'svt_ch1_couplage_excitation_contraction',
    title: 'Couplage excitation–contraction–relaxation',
    defaultVariant: 'cycle_complet',
    variants: [
      { id: 'cycle_complet', label: 'Cycle complet' },
      { id: 'liberation_calcium', label: 'Libération du Ca²⁺' },
      { id: 'contraction', label: 'Contraction' },
      { id: 'relaxation', label: 'Relaxation' },
    ],
    maxStep: 8,
    frameMs: 720,
  },
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

function fullSegments(
  id: string,
  points: ScientificPoint[],
  color: string,
  label?: string,
): JSXGraphElementSpec[] {
  const segments: JSXGraphElementSpec[] = points.slice(1).map((point, index) => ({
    id: `${id}-${index}`,
    type: 'segment',
    points: [points[index], point],
    color,
  }));
  if (label && points.length) {
    segments.push({
      id: `${id}-label`,
      type: 'text',
      points: [points[Math.max(0, points.length - 6)]],
      label,
      color,
    });
  }
  return segments;
}

function pulse(x: number, center: number, amplitude = 2.7): number {
  return amplitude * Math.exp(-Math.pow((x - center) / 0.62, 2));
}

function propagationOndeSpec(variant: string, step: number, maxStep: number): JSXGraphVisualSpec {
  const progress = Math.max(0, Math.min(1, step / maxStep));
  if (variant === 'superposition') {
    const left = 1 + 10 * progress;
    const right = 11 - 10 * progress;
    const first = samples(x => pulse(x, left, 1.55), 0, 12, 73);
    const second = samples(x => pulse(x, right, 1.55), 0, 12, 73);
    const resultant = samples(x => pulse(x, left, 1.55) + pulse(x, right, 1.55), 0, 12, 73);
    return {
      engine: 'jsxgraph',
      title: 'Les perturbations se superposent puis poursuivent leur propagation',
      boundingBox: [-0.7, 4.2, 13.6, -1.3],
      axis: true,
      xLabel: 'x (m)',
      yLabel: 'élongation (m)',
      elements: [
        ...fullSegments('pulse-gauche', first, '#64748b'),
        ...fullSegments('pulse-droite', second, '#64748b'),
        ...fullSegments('resultante', resultant, 'cyan'),
        { id: 'resultante-label', type: 'text', points: [{ x: 6, y: 3.55 }], color: 'cyan', label: 'résultante' },
      ],
    };
  }

  const center = 1 + 10 * progress;
  const profile = samples(x => pulse(x, center), 0, 12, 73);
  const elements: JSXGraphElementSpec[] = [
    ...fullSegments('onde', profile, 'cyan'),
    { id: 'perturbation-label', type: 'text', points: [{ x: center, y: 3.0 }], color: 'cyan', label: 'perturbation' },
    { id: 'sens', type: 'arrow', points: [{ x: 1, y: 3.45 }, { x: 11.4, y: 3.45 }], color: 'green', label: 'sens de propagation' },
  ];
  if (variant === 'retard') {
    const reachedA = center >= 2;
    const reachedB = center >= 9;
    elements.push(
      { id: 'a', type: 'point', points: [{ x: 2, y: 0 }], color: reachedA ? 'orange' : 'white', label: 'A' },
      { id: 'b', type: 'point', points: [{ x: 9, y: 0 }], color: reachedB ? 'orange' : 'white', label: 'B' },
      { id: 'ab', type: 'segment', points: [{ x: 2, y: -0.55 }, { x: 9, y: -0.55 }], color: 'orange', label: 'd = AB' },
      { id: 'tau', type: 'text', points: [{ x: 5.5, y: -1.0 }], color: 'yellow', label: 'τ = d / v' },
    );
  }
  return {
    engine: 'jsxgraph',
    title: variant === 'retard' ? 'Le même signal atteint B après A' : 'Une perturbation se propage sans transport de matière',
    boundingBox: [-0.7, 4.2, 13.6, -1.3],
    axis: true,
    xLabel: 'x (m)',
    yLabel: 'élongation (m)',
    elements,
  };
}

function typesOndesSpec(variant: string, step: number, maxStep: number): JSXGraphVisualSpec {
  const progress = Math.max(0, Math.min(1, step / maxStep));
  const center = 1 + 10 * progress;
  const elements: JSXGraphElementSpec[] = [];
  if (variant !== 'longitudinale') {
    const transverse = samples(x => 2.25 + pulse(x, center, 1.15), 0, 12, 49);
    elements.push(
      ...fullSegments('transverse', transverse, 'cyan'),
      ...transverse.filter((_, index) => index % 4 === 0).map((point, index) => ({
        id: `grain-t-${index}`, type: 'point' as const, points: [point], color: 'cyan',
      })),
      { id: 'label-t', type: 'text', points: [{ x: 6, y: 3.85 }], color: 'cyan', label: 'transversale : déplacement ⟂ propagation' },
      { id: 'arrow-t', type: 'arrow', points: [{ x: 1, y: 1.55 }, { x: 11, y: 1.55 }], color: 'green' },
    );
  }
  if (variant !== 'transversale') {
    const particles = Array.from({ length: 25 }, (_, index) => {
      const restX = index * 0.5;
      const displacement = 0.38 * Math.exp(-Math.pow((restX - center) / 0.9, 2));
      return { x: restX + displacement, y: -1.65 };
    });
    elements.push(
      ...particles.map((point, index) => ({
        id: `grain-l-${index}`, type: 'point' as const, points: [point], color: 'orange',
      })),
      { id: 'label-l', type: 'text', points: [{ x: 6, y: -0.75 }], color: 'orange', label: 'longitudinale : déplacement ∥ propagation' },
      { id: 'arrow-l', type: 'arrow', points: [{ x: 1, y: -2.45 }, { x: 11, y: -2.45 }], color: 'green' },
    );
  }
  return {
    engine: 'jsxgraph',
    title: 'La matière oscille localement ; seule la perturbation se propage',
    boundingBox: [-0.8, 4.5, 13.8, -3.1],
    axis: false,
    elements,
  };
}

function celeriteCordeSpec(variant: string, step: number, maxStep: number): JSXGraphVisualSpec {
  const progress = Math.max(0, Math.min(1, step / maxStep));
  const speedFactors: Record<string, number> = {
    forte_tension: 1.35,
    faible_tension: 0.72,
    forte_masse_lineique: 0.62,
  };
  const descriptions: Record<string, string> = {
    forte_tension: 'T plus grande → v plus grande',
    faible_tension: 'T plus faible → v plus faible',
    forte_masse_lineique: 'μ plus grande → v plus faible',
  };
  const referenceCenter = 1 + 8 * progress;
  const changedCenter = Math.min(11.2, 1 + 8 * (speedFactors[variant] || 1) * progress);
  const reference = samples(x => 2.15 + pulse(x, referenceCenter, 0.9), 0, 12, 61);
  const changed = samples(x => -1.35 + pulse(x, changedCenter, 0.9), 0, 12, 61);
  return {
    engine: 'jsxgraph',
    title: 'Même durée : la distance parcourue révèle la célérité',
    boundingBox: [-0.8, 4.1, 14.8, -3.0],
    axis: false,
    elements: [
      ...fullSegments('corde-reference', reference, 'blue'),
      ...fullSegments('corde-modifiee', changed, 'orange'),
      { id: 'ref-label', type: 'text', points: [{ x: 12.6, y: 2.15 }], color: 'blue', label: 'référence' },
      { id: 'changed-label', type: 'text', points: [{ x: 12.6, y: -1.35 }], color: 'orange', label: descriptions[variant] || 'condition modifiée' },
      { id: 'law', type: 'text', points: [{ x: 6, y: -2.45 }], color: 'yellow', label: 'v = √(T / μ)' },
    ],
  };
}

function facteursCinetiquesSpec(variant: string, step: number, maxStep: number): JSXGraphVisualSpec {
  const factorLabels: Record<string, string> = {
    temperature: 'température plus élevée',
    concentration: 'concentration plus élevée',
    catalyseur: 'avec catalyseur',
    surface_contact: 'surface de contact plus grande',
  };
  const fastRates: Record<string, number> = {
    temperature: 0.52,
    concentration: 0.43,
    catalyseur: 0.68,
    surface_contact: 0.47,
  };
  const reference = samples(t => 10 * (1 - Math.exp(-0.23 * t)), 0, 12, 73);
  const accelerated = samples(t => 10 * (1 - Math.exp(-(fastRates[variant] || 0.5) * t)), 0, 12, 73);
  const time = 12 * Math.max(0, Math.min(1, step / maxStep));
  const refY = 10 * (1 - Math.exp(-0.23 * time));
  const fastY = 10 * (1 - Math.exp(-(fastRates[variant] || 0.5) * time));
  return {
    engine: 'jsxgraph',
    title: 'Le facteur modifie la vitesse, pas l’état final',
    boundingBox: [-0.8, 11.8, 14.5, -1.5],
    axis: true,
    grid: true,
    xLabel: 'temps (min)',
    yLabel: 'avancement (mmol)',
    elements: [
      ...pointsToSegments('reference', reference, 'blue', 'référence', step, maxStep, { x: 10.8, y: 8.8 }),
      ...pointsToSegments('acceleree', accelerated, 'orange', factorLabels[variant] || 'facteur augmenté', step, maxStep, { x: 8.6, y: 10.7 }),
      { id: 'plateau', type: 'segment', points: [{ x: 0, y: 10 }, { x: 12, y: 10 }], color: 'green', dashed: true, label: 'même état final' },
      // Les deux points avancent sur les courbes : leurs noms sont déjà
      // écrits à des positions fixes au bout des courbes. Ne pas rattacher de
      // texte aux marqueurs mobiles évite doublons, déplacement et clignotement.
      { id: 'ref-now', type: 'point', points: [{ x: time, y: refY }], color: 'blue' },
      { id: 'fast-now', type: 'point', points: [{ x: time, y: fastY }], color: 'orange' },
    ],
  };
}

function energieActivationSpec(variant: string, step: number, maxStep: number): JSXGraphVisualSpec {
  const progress = Math.max(0, Math.min(1, step / maxStep));
  const sansCatalyseur = (x: number) => 2 - 0.1 * x + 5.2 * Math.pow(Math.sin(Math.PI * x / 10), 2);
  const avecCatalyseur = (x: number) => 2 - 0.1 * x + 2.7 * Math.pow(Math.sin(Math.PI * x / 10), 2);
  const showWithout = variant !== 'avec_catalyseur';
  const showWith = variant !== 'sans_catalyseur';
  const movingFn = variant === 'sans_catalyseur' ? sansCatalyseur : avecCatalyseur;
  const x = 10 * progress;
  const elements: JSXGraphElementSpec[] = [
    { id: 'reactifs', type: 'text', points: [{ x: 0.7, y: 1.55 }], color: 'white', label: 'Réactifs' },
    { id: 'produits', type: 'text', points: [{ x: 9.3, y: 0.55 }], color: 'white', label: 'Produits' },
    { id: 'delta-r', type: 'segment', points: [{ x: 0, y: 2 }, { x: 1.2, y: 2 }], color: 'white' },
    { id: 'delta-p', type: 'segment', points: [{ x: 8.8, y: 1 }, { x: 10, y: 1 }], color: 'white' },
  ];
  if (showWithout) {
    elements.push(...fullSegments('sans-cat', samples(sansCatalyseur, 0, 10, 73), 'red'));
  }
  if (showWith) {
    elements.push(...fullSegments('avec-cat', samples(avecCatalyseur, 0, 10, 73), 'green'));
  }
  elements.push(
    { id: 'ea', type: 'segment', points: [{ x: 5, y: 2 }, { x: 5, y: variant === 'avec_catalyseur' ? avecCatalyseur(5) : sansCatalyseur(5) }], color: 'yellow', label: 'Ea' },
    { id: 'progress', type: 'point', points: [{ x, y: movingFn(x) }], color: 'orange', label: 'système' },
    { id: 'message', type: 'text', points: [{ x: 5, y: -0.35 }], color: 'cyan', label: 'Le catalyseur abaisse Ea sans changer ΔrH ni l’état final' },
  );
  return {
    engine: 'jsxgraph',
    title: 'Deux chemins réactionnels, mêmes réactifs et produits',
    boundingBox: [-0.8, 8.3, 11.8, -1.0],
    axis: true,
    xLabel: 'coordonnée réactionnelle',
    yLabel: 'énergie relative',
    elements,
  };
}

function oxydoreductionSpec(variant: string, step: number, maxStep: number): CytoscapeVisualSpec {
  const paths: Record<string, string[]> = {
    transfert_direct: ['reducteur', 'electrons', 'oxydant', 'produits'],
    pile: ['anode', 'electrons', 'circuit', 'cathode', 'reduction'],
    electrolyse: ['generateur', 'anode', 'oxydation', 'electrons', 'cathode', 'reduction'],
  };
  return processSpec(
    variant === 'pile' ? 'Pile : réaction spontanée et courant électrique'
      : variant === 'electrolyse' ? 'Électrolyse : transformation imposée par le générateur'
        : 'Oxydation et réduction sont simultanées',
    'breadthfirst',
    [
      ['reducteur', 'Réducteur : donne e⁻'], ['electrons', 'Électrons'],
      ['oxydant', 'Oxydant : capte e⁻'], ['produits', 'Produits redox'],
      ['anode', 'Anode : oxydation'], ['circuit', 'Circuit extérieur'],
      ['cathode', 'Cathode : réduction'], ['reduction', 'Espèce réduite'],
      ['generateur', 'Générateur'], ['oxydation', 'Espèce oxydée'],
    ],
    [
      ['reducteur', 'electrons', 'oxydation'], ['electrons', 'oxydant', 'transfert'],
      ['oxydant', 'produits', 'réduction'], ['anode', 'electrons', 'e⁻ libérés'],
      ['electrons', 'circuit', 'courant'], ['circuit', 'cathode', 'e⁻ reçus'],
      ['cathode', 'reduction'], ['generateur', 'anode', 'impose le sens'],
      ['anode', 'oxydation'], ['oxydation', 'electrons', 'e⁻ arrachés'],
    ],
    paths[variant] || paths.transfert_direct,
    step,
    maxStep,
  );
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

function respirationMitochondrialeSpec(variant: string, step: number, maxStep: number): CytoscapeVisualSpec {
  const paths: Record<string, string[]> = {
    krebs: ['pyruvate', 'acetyl', 'krebs', 'co2', 'coenzymes'],
    chaine_respiratoire: ['coenzymes', 'chaine', 'o2', 'h2o', 'gradient', 'atp'],
    bilan: ['glucose', 'glycolyse', 'pyruvate', 'acetyl', 'krebs', 'coenzymes', 'chaine', 'gradient', 'atp'],
  };
  return processSpec(
    'Matrice : Krebs · membrane interne et crêtes : chaîne respiratoire',
    'breadthfirst',
    [
      ['glucose', 'Glucose'], ['glycolyse', 'Glycolyse (cytosol)'],
      ['pyruvate', 'Pyruvate'], ['acetyl', 'Acétyl-CoA'],
      ['krebs', 'Krebs (matrice)'], ['co2', 'CO₂ rejeté'],
      ['coenzymes', 'NADH,H⁺ / FADH₂'], ['chaine', 'Chaîne respiratoire (crêtes)'],
      ['o2', 'O₂'], ['h2o', 'H₂O'], ['gradient', 'Gradient de H⁺'],
      ['atp', 'ATP + chaleur'],
    ],
    [
      ['glucose', 'glycolyse', 'oxydation partielle'], ['glycolyse', 'pyruvate'],
      ['pyruvate', 'acetyl'], ['acetyl', 'krebs'], ['krebs', 'co2'],
      ['krebs', 'coenzymes', 'électrons + H⁺'], ['coenzymes', 'chaine'],
      ['chaine', 'o2', 'accepteur final'], ['o2', 'h2o'],
      ['chaine', 'gradient', 'pompage des H⁺'], ['gradient', 'atp', 'ATP synthase'],
    ],
    paths[variant] || paths.bilan,
    step,
    maxStep,
  );
}

function sarcomereElements(prefix: string, contraction: number, y: number): JSXGraphElementSpec[] {
  const leftZ = 0.9 + 1.8 * contraction;
  const rightZ = 11.1 - 1.8 * contraction;
  const leftActinEnd = leftZ + 4.1;
  const rightActinEnd = rightZ - 4.1;
  return [
    { id: `${prefix}-z-left`, type: 'segment', points: [{ x: leftZ, y: y - 0.85 }, { x: leftZ, y: y + 0.85 }], color: 'white', label: 'Z' },
    { id: `${prefix}-z-right`, type: 'segment', points: [{ x: rightZ, y: y - 0.85 }, { x: rightZ, y: y + 0.85 }], color: 'white', label: 'Z' },
    { id: `${prefix}-actin-left-up`, type: 'segment', points: [{ x: leftZ, y: y + 0.42 }, { x: leftActinEnd, y: y + 0.42 }], color: 'cyan' },
    { id: `${prefix}-actin-left-down`, type: 'segment', points: [{ x: leftZ, y: y - 0.42 }, { x: leftActinEnd, y: y - 0.42 }], color: 'cyan' },
    { id: `${prefix}-actin-right-up`, type: 'segment', points: [{ x: rightActinEnd, y: y + 0.42 }, { x: rightZ, y: y + 0.42 }], color: 'cyan' },
    { id: `${prefix}-actin-right-down`, type: 'segment', points: [{ x: rightActinEnd, y: y - 0.42 }, { x: rightZ, y: y - 0.42 }], color: 'cyan' },
    { id: `${prefix}-myosin`, type: 'segment', points: [{ x: 4.1, y }, { x: 7.9, y }], color: 'orange', label: 'myosine : longueur constante' },
    { id: `${prefix}-left-slide`, type: 'arrow', points: [{ x: 3.4, y: y + 1.15 }, { x: 5.1, y: y + 1.15 }], color: 'green' },
    { id: `${prefix}-right-slide`, type: 'arrow', points: [{ x: 8.6, y: y + 1.15 }, { x: 6.9, y: y + 1.15 }], color: 'green' },
  ];
}

function glissementSarcomereSpec(variant: string, step: number, maxStep: number): JSXGraphVisualSpec {
  const progress = Math.max(0, Math.min(1, step / maxStep));
  const elements: JSXGraphElementSpec[] = variant === 'comparaison'
    ? [
        ...sarcomereElements('repos', 0, 2.2),
        { id: 'repos-label', type: 'text' as const, points: [{ x: 6, y: 3.75 }], color: 'white', label: 'repos' },
        ...sarcomereElements('contracte', progress, -2.0),
        { id: 'contracte-label', type: 'text' as const, points: [{ x: 6, y: -3.55 }], color: 'yellow', label: 'contraction' },
      ]
    : sarcomereElements('sarcomere', variant === 'repos' ? 0 : progress, 0);
  elements.push({
    id: 'conclusion', type: 'text', points: [{ x: 6, y: variant === 'comparaison' ? -4.1 : -1.8 }],
    color: 'cyan', label: 'Les filaments ne raccourcissent pas : leur chevauchement augmente',
  });
  return {
    engine: 'jsxgraph',
    title: 'Les stries Z se rapprochent tandis que la bande A reste constante',
    boundingBox: [-0.7, variant === 'comparaison' ? 4.7 : 2.8, 12.8, variant === 'comparaison' ? -4.8 : -2.4],
    axis: false,
    elements,
  };
}

function couplageExcitationContractionSpec(variant: string, step: number, maxStep: number): CytoscapeVisualSpec {
  const paths: Record<string, string[]> = {
    liberation_calcium: ['message', 'tubule', 'reticulum', 'calcium'],
    contraction: ['calcium', 'troponine', 'ponts', 'glissement', 'contraction'],
    relaxation: ['fin_message', 'pompe', 'reticulum', 'sites_masques', 'relaxation'],
    cycle_complet: ['message', 'tubule', 'reticulum', 'calcium', 'troponine', 'ponts', 'glissement', 'contraction', 'fin_message', 'pompe', 'reticulum', 'sites_masques', 'relaxation'],
  };
  return processSpec(
    'Le Ca²⁺ relie le message électrique au mouvement mécanique',
    'breadthfirst',
    [
      ['message', 'Potentiel d’action'], ['tubule', 'Tubule T'],
      ['reticulum', 'Réticulum sarcoplasmique'], ['calcium', 'Ca²⁺ cytosolique'],
      ['troponine', 'Troponine : sites exposés'], ['ponts', 'Ponts actine–myosine + ATP'],
      ['glissement', 'Glissement des filaments'], ['contraction', 'Contraction'],
      ['fin_message', 'Fin du message'], ['pompe', 'Pompes Ca²⁺ + ATP'],
      ['sites_masques', 'Sites de l’actine masqués'], ['relaxation', 'Relaxation'],
    ],
    [
      ['message', 'tubule'], ['tubule', 'reticulum', 'déclenche'],
      ['reticulum', 'calcium', 'libération'], ['calcium', 'troponine'],
      ['troponine', 'ponts'], ['ponts', 'glissement', 'cycles ATP'],
      ['glissement', 'contraction'], ['contraction', 'fin_message', 'fin de l’excitation'], ['fin_message', 'pompe'],
      ['pompe', 'reticulum', 'recapture du Ca²⁺'], ['reticulum', 'sites_masques'],
      ['sites_masques', 'relaxation'],
    ],
    paths[variant] || paths.cycle_complet,
    step,
    maxStep,
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
    case 'phys_ch1_propagation_onde': return propagationOndeSpec(safeVariant, step, meta.maxStep);
    case 'phys_ch1_types_ondes': return typesOndesSpec(safeVariant, step, meta.maxStep);
    case 'phys_ch1_celerite_corde': return celeriteCordeSpec(safeVariant, step, meta.maxStep);
    case 'chem_ch1_facteurs_cinetiques': return facteursCinetiquesSpec(safeVariant, step, meta.maxStep);
    case 'chem_ch1_energie_activation': return energieActivationSpec(safeVariant, step, meta.maxStep);
    case 'chem_ch1_oxydoreduction': return oxydoreductionSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_respiration_mitochondriale': return respirationMitochondrialeSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_glissement_sarcomere': return glissementSarcomereSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_couplage_excitation_contraction': return couplageExcitationContractionSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_cycle_atp': return atpSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_levures_exao': return levuresSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_chimiosmose': return chimiosmoseSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_carte_metabolique': return metabolicSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_myogrammes': return myogramSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_cycle_actomyosine': return actomyosineSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_filieres_effort': return filieresSpec(safeVariant, step, meta.maxStep);
  }
}
