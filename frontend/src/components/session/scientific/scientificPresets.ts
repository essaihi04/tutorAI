import type {
  CytoscapeEdgeSpec,
  CytoscapeNodeSpec,
  CytoscapeVisualSpec,
  JSXGraphElementSpec,
  JSXGraphVisualSpec,
  RoughSVGElementSpec,
  RoughSVGVisualSpec,
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
  svt_ch1_glycolyse_etapes: {
    id: 'svt_ch1_glycolyse_etapes', title: 'Les étapes de la glycolyse',
    defaultVariant: 'scene', variants: [{ id: 'scene', label: 'Glycolyse' }], maxStep: 9, frameMs: 900,
  },
  svt_ch1_krebs_detaille: {
    id: 'svt_ch1_krebs_detaille', title: 'Oxydation du pyruvate et cycle de Krebs',
    defaultVariant: 'scene', variants: [{ id: 'scene', label: 'Krebs' }], maxStep: 10, frameMs: 850,
  },
  svt_ch1_echelle_redox: {
    id: 'svt_ch1_echelle_redox', title: 'Potentiels d’oxydoréduction',
    defaultVariant: 'scene', variants: [{ id: 'scene', label: 'Échelle redox' }], maxStep: 8, frameMs: 850,
  },
  svt_ch1_ultrastructure_mitochondrie: {
    id: 'svt_ch1_ultrastructure_mitochondrie', title: 'Ultrastructure et composition de la mitochondrie',
    defaultVariant: 'scene', variants: [{ id: 'scene', label: 'Ultrastructure' }], maxStep: 12, frameMs: 850,
  },
  svt_ch1_flux_protons: {
    id: 'svt_ch1_flux_protons', title: 'Réduction du dioxygène et flux de protons',
    defaultVariant: 'scene', variants: [{ id: 'scene', label: 'Flux de protons' }], maxStep: 8, frameMs: 850,
  },
  svt_ch1_molecules_glucose_atp: {
    id: 'svt_ch1_molecules_glucose_atp', title: 'Structure du glucose et de l’ATP',
    defaultVariant: 'scene', variants: [{ id: 'scene', label: 'Glucose et ATP' }], maxStep: 5, frameMs: 850,
  },
  svt_ch1_rendement_energetique: {
    id: 'svt_ch1_rendement_energetique', title: 'Bilan en ATP et rendement énergétique',
    defaultVariant: 'scene', variants: [{ id: 'scene', label: 'Rendement énergétique' }], maxStep: 10, frameMs: 900,
  },
  svt_ch1_schema_bilan_annote: {
    id: 'svt_ch1_schema_bilan_annote', title: 'Schéma-bilan de la respiration',
    defaultVariant: 'scene', variants: [{ id: 'scene', label: 'Schéma-bilan' }], maxStep: 21, frameMs: 900,
  },
  svt_ch1_vesicules_atp_synthase: {
    id: 'svt_ch1_vesicules_atp_synthase', title: 'Rôle des sphères pédonculées',
    defaultVariant: 'scene', variants: [{ id: 'scene', label: 'Vésicules retournées' }], maxStep: 8, frameMs: 850,
  },
  svt_ch1_chimiosmose: {
    id: 'svt_ch1_chimiosmose',
    title: 'Chaîne respiratoire et chimiosmose',
    defaultVariant: 'scene',
    variants: [{ id: 'scene', label: 'Chaîne respiratoire' }],
    maxStep: 12,
    frameMs: 800,
  },
  svt_ch1_carte_metabolique: {
    id: 'svt_ch1_carte_metabolique',
    title: 'De la matière organique à l’ATP',
    defaultVariant: 'scene',
    variants: [{ id: 'scene', label: 'Devenir du pyruvate' }],
    maxStep: 10,
    frameMs: 850,
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
  svt_ch1_chaleurs_muscle: {
    id: 'svt_ch1_chaleurs_muscle',
    title: 'Secousse musculaire et dégagements de chaleur',
    defaultVariant: 'comparaison',
    variants: [
      { id: 'comparaison', label: 'Comparer avec et sans O₂' },
      { id: 'avec_oxygene', label: 'Récupération avec O₂' },
      { id: 'sans_oxygene', label: 'Récupération sans O₂' },
    ],
    maxStep: 36,
    frameMs: 130,
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

function muscleHeatSpec(variant: string, step: number, maxStep: number): JSXGraphVisualSpec {
  const twitchCurve = samples(t => 5.5 * Math.exp(-Math.pow((t - 2.1) / 0.68, 2)), 0, 8, 81);
  const initialHeat = samples(t => 2.7 * Math.exp(-Math.pow((t - 2.6) / 1.0, 2)), 0, 8, 81);
  const delayedWithOxygen = samples(t => 1.7 * Math.exp(-Math.pow((t - 5.8) / 1.25, 2)), 0, 8, 81);
  const delayedWithoutOxygen = samples(t => 0.25 * Math.exp(-Math.pow((t - 5.8) / 1.25, 2)), 0, 8, 81);
  const elements = [
    ...pointsToSegments('secousse', twitchCurve, 'orange', 'Tension musculaire', step, maxStep),
    ...pointsToSegments('initiale', initialHeat, 'red', 'Chaleur initiale', step, maxStep),
  ];
  if (variant !== 'sans_oxygene') {
    elements.push(...pointsToSegments('retardee-o2', delayedWithOxygen, 'cyan', 'Chaleur retardée avec O₂', step, maxStep));
  }
  if (variant !== 'avec_oxygene') {
    elements.push(...pointsToSegments('retardee-sans-o2', delayedWithoutOxygen, 'purple', 'Chaleur retardée sans O₂', step, maxStep));
  }
  return {
    engine: 'jsxgraph',
    title: 'La chaleur retardée dépend des réactions oxydatives de récupération',
    boundingBox: [-0.5, 6.5, 8.7, -0.8],
    axis: true,
    grid: true,
    xLabel: 'Temps (u.a.)',
    yLabel: 'Valeur relative (u.a.)',
    elements,
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

function glycolyseEtapesSpec(_variant: string, step: number, maxStep: number): CytoscapeVisualSpec {
  const nodes: Array<[string, string]> = [
    ['glucose', 'Glucose 6C'], ['g6p', 'Glucose-6-phosphate 6C'],
    ['f6p', 'Fructose-6-phosphate 6C'], ['f16bp', 'Fructose-1,6-bisphosphate 6C'],
    ['trioses', '2 trioses phosphate 3C'], ['bpg', '2 × 1,3-bisphosphoglycérate 3C'],
    ['pg3', '2 × 3-phosphoglycérate 3C'], ['pg2', '2 × 2-phosphoglycérate 3C'],
    ['pep', '2 × phosphoénolpyruvate 3C'], ['pyruvate', '2 pyruvates 3C'],
  ];
  const edges: Array<[string, string, string?]> = [
    ['glucose', 'g6p', '1 hexokinase · ATP → ADP'], ['g6p', 'f6p', '2 isomérisation'],
    ['f6p', 'f16bp', '3 PFK · ATP → ADP'], ['f16bp', 'trioses', '4–5 scission + isomérisation'],
    ['trioses', 'bpg', '6 : 2 NAD⁺ + 2 Pi → 2 NADH,H⁺'], ['bpg', 'pg3', '7 : 2 ADP → 2 ATP'],
    ['pg3', 'pg2', '8 mutase'], ['pg2', 'pep', '9 : −2 H₂O'], ['pep', 'pyruvate', '10 : 2 ADP → 2 ATP'],
  ];
  return processSpec('Glycolyse : 2 ATP nets et 2 NADH,H⁺ par glucose', 'breadthfirst', nodes, edges,
    nodes.map(([id]) => id), step, maxStep);
}

function krebsDetailleSpec(_variant: string, step: number, maxStep: number): CytoscapeVisualSpec {
  const nodes: Array<[string, string]> = [
    ['pyruvate', 'Pyruvate 3C'], ['acetyl', 'Acétyl-CoA 2C'], ['citrate', 'Citrate 6C'],
    ['c5', 'Composé 5C'], ['c4a', 'Composé 4C'], ['succinate', 'Succinate 4C'],
    ['fumarate', 'Fumarate 4C'], ['malate', 'Malate 4C'], ['oxaloacetate', 'Oxaloacétate 4C'],
    ['bilan', 'Par glucose : 6 CO₂ · 8 NADH,H⁺ · 2 FADH₂ · 2 ATP'],
  ];
  const edges: Array<[string, string, string?]> = [
    ['pyruvate', 'acetyl', 'CO₂ + NADH,H⁺'], ['acetyl', 'citrate', '+ oxaloacétate'],
    ['citrate', 'c5', 'CO₂ + NADH,H⁺'], ['c5', 'c4a', 'CO₂ + NADH,H⁺'],
    ['c4a', 'succinate', 'ADP + Pi → ATP'], ['succinate', 'fumarate', 'FAD → FADH₂'],
    ['fumarate', 'malate', '+ H₂O'], ['malate', 'oxaloacetate', 'NAD⁺ → NADH,H⁺'],
    ['oxaloacetate', 'citrate', 'nouveau tour'], ['oxaloacetate', 'bilan', '2 tours par glucose'],
  ];
  return processSpec('Oxydation du pyruvate puis deux tours de Krebs', 'circle', nodes, edges,
    ['pyruvate', 'acetyl', 'citrate', 'c5', 'c4a', 'succinate', 'fumarate', 'malate', 'oxaloacetate', 'bilan'], step, maxStep);
}

function echelleRedoxSpec(_variant: string, step: number, maxStep: number): JSXGraphVisualSpec {
  const couples = [
    { y: -320, label: 'NADH,H⁺ / NAD⁺', color: 'cyan' },
    { y: -100, label: 'FMNH₂ / FMN', color: 'blue' },
    { y: 40, label: 'QH₂ / Q', color: 'orange' },
    { y: 250, label: 'cyt c Fe²⁺ / Fe³⁺', color: 'purple' },
    { y: 820, label: 'H₂O / O₂', color: 'green' },
  ];
  const shown = Math.min(couples.length, revealedCount(couples.length, step, maxStep));
  const elements: JSXGraphElementSpec[] = couples.slice(0, shown).flatMap((c, i) => [
    { id: `redox-p-${i}`, type: 'point', points: [{ x: 2.2, y: c.y }], color: c.color },
    { id: `redox-t-${i}`, type: 'text', points: [{ x: 2.7, y: c.y }], label: c.label, color: c.color },
  ]);
  if (step >= 6) elements.push({ id: 'flux-e', type: 'arrow', points: [{ x: 6.2, y: -320 }, { x: 6.2, y: 820 }], color: 'yellow', label: 'flux spontané des e⁻' });
  if (step >= 7) elements.push({ id: 'delta-e', type: 'text', points: [{ x: 4.5, y: 650 }], color: 'orange', label: 'ΔE°′ > 0 : énergie libérée' });
  if (step >= 8) elements.push({ id: 'o2-final', type: 'text', points: [{ x: 4.5, y: 800 }], color: 'green', label: 'O₂ = accepteur final → H₂O' });
  return { engine: 'jsxgraph', title: 'Échelle des potentiels redox mitochondriaux',
    boundingBox: [-0.6, 950, 8.3, -430], axis: true, grid: true, xLabel: 'couples redox', yLabel: 'E°′ (mV)', elements };
}

function ultrastructureMitochondrieSpec(_variant: string, step: number, _maxStep: number): RoughSVGVisualSpec {
  const INK = '#e0f2fe', CYAN = '#22d3ee', MATRIX = '#0c4a6e', GOLD = '#fde047';
  // Les huit reperes du document sont numerotes sur la coupe et repris dans
  // une legende : c'est la forme exacte de la question d'examen, « annotez le
  // document en donnant le nom correspondant a chaque numero ».
  const reperes: Array<[number, number, string]> = [
    [286, 52, 'Membrane externe'],
    [352, 86, 'Membrane interne'],
    [300, 200, 'Matrice'],
    [168, 200, 'Crêtes mitochondriales'],
    [470, 104, 'Espace intermembranaire'],
    [392, 252, 'ADN mitochondrial'],
    [112, 132, 'Phospholipides'],
    [452, 286, 'Protéines intégrées'],
  ];
  const shown = Math.max(0, Math.min(reperes.length, Math.round(step)));

  const el: RoughSVGElementSpec[] = [
    { type: 'ellipse', x: 300, y: 200, radiusX: 262, radiusY: 148, color: CYAN, fill: '#082f49' },
    { type: 'ellipse', x: 300, y: 200, radiusX: 232, radiusY: 118, color: CYAN, fill: MATRIX },
  ];
  for (let i = 0; i < 5; i += 1) {
    const x = 130 + i * 85;
    el.push({ type: 'polyline', color: CYAN, strokeWidth: 3, points: [
      { x, y: 200 - 112 }, { x: x + 34, y: 200 - 46 }, { x, y: 200 }, { x: x + 34, y: 200 + 46 }, { x, y: 200 + 112 },
    ] });
  }
  el.push({ type: 'circle', x: 392, y: 252, radius: 17, color: GOLD, fill: '#713f12' });

  reperes.slice(0, shown).forEach(([x, y], i) => {
    el.push({ type: 'circle', x, y, radius: 15, color: GOLD, fill: '#0f172a' });
    el.push({ type: 'text', x, y: y + 7, text: String(i + 1), color: GOLD, fontSize: 19, align: 'middle' });
  });
  reperes.slice(0, shown).forEach(([, , label], i) => {
    el.push({ type: 'text', x: 600, y: 70 + i * 34, text: `${i + 1}  ${label}`, color: INK, fontSize: 19, align: 'start' });
  });

  if (step >= 9) {
    el.push({ type: 'circle', x: 186, y: 68, radius: 9, color: '#4ade80', fill: '#14532d' });
    el.push({ type: 'text', x: 600, y: 358, text: 'Porine : ions et métabolites hydrosolubles', color: '#4ade80', fontSize: 17, align: 'start' });
  }
  if (step >= 10) {
    for (let i = 0; i < 4; i += 1) {
      const x = 172 + i * 86;
      el.push({ type: 'line', x, y: 318, width: 0, height: -16, color: '#c4b5fd', strokeWidth: 3 });
      el.push({ type: 'circle', x, y: 296, radius: 11, color: '#c4b5fd', fill: '#4c1d95' });
    }
    el.push({ type: 'text', x: 600, y: 388, text: 'Sphères pédonculées = ATP synthase', color: '#c4b5fd', fontSize: 17, align: 'start' });
  }
  if (step >= 11) {
    const rows: Array<[string, string, string]> = [
      ['Membrane externe', '38 % lipides · 62 % protéines', 'comparable à la membrane cytoplasmique'],
      ['Membrane interne', '20 % lipides · 80 % protéines', 'nombreuses enzymes, dont l’ATP synthase'],
      ['Matrice', 'pas de glucose · pyruvate et ATP', 'déshydrogénases et carboxylases'],
    ];
    el.push({ type: 'rect', x: 40, y: 396, width: 880, height: 138, color: CYAN, fill: '#06202e' });
    rows.forEach(([a, b, c], i) => {
      const y = 428 + i * 34;
      el.push({ type: 'text', x: 62, y, text: a, color: GOLD, fontSize: 17, align: 'start' });
      el.push({ type: 'text', x: 268, y, text: b, color: INK, fontSize: 17, align: 'start' });
      el.push({ type: 'text', x: 570, y, text: c, color: '#93c5fd', fontSize: 16, align: 'start' });
    });
  }
  if (step >= 12) {
    el.push({ type: 'text', x: 480, y: 556, align: 'middle', fontSize: 18, color: '#4ade80',
      text: 'Une membrane interne riche en protéines : c’est là que se déroulent les oxydations respiratoires.' });
  }

  return { engine: 'roughsvg', title: 'Ultrastructure de la mitochondrie', width: 960, height: 576,
    description: 'Coupe annotée de la mitochondrie et composition chimique de ses compartiments.', elements: el };
}

function fluxProtonsSpec(_variant: string, step: number, _maxStep: number): RoughSVGVisualSpec {
  // Repere dessine a la main plutot que confie a JSXGraph : une cinetique de
  // 330 s contre 60 unites ne tient pas dans le rapport du conteneur, et le
  // moteur etirait alors l'axe des abscisses jusqu'a faire cogner son nom
  // contre ses propres graduations.
  const AXE = '#94a3b8', INK = '#e0f2fe', ORANGE = '#fb923c', GOLD = '#fde047';
  const px = (t: number) => 150 + t * (750 / 330);
  const py = (h: number) => 430 - h * (340 / 62);
  const courbe: Array<[number, number]> = [
    [0, 10], [20, 10], [40, 10], [55, 32], [66, 58],
    [90, 50], [130, 40], [180, 32], [240, 25], [330, 18],
  ];
  const total = courbe.length - 1;
  const shown = step >= 5 ? total : Math.max(1, Math.ceil((step / 5) * total));

  const el: RoughSVGElementSpec[] = [
    { type: 'arrow', points: [{ x: 150, y: 430 }, { x: 920, y: 430 }], color: AXE, strokeWidth: 2 },
    { type: 'arrow', points: [{ x: 150, y: 430 }, { x: 150, y: 76 }], color: AXE, strokeWidth: 2 },
    // Nom ET unite sur chaque axe : un axe anonyme est faux au bac.
    { type: 'text', x: 535, y: 470, text: 'temps (s)', color: INK, fontSize: 19, align: 'middle' },
    { type: 'text', x: 150, y: 62, text: '[H⁺] (10⁻⁹ mol/L)', color: INK, fontSize: 19, align: 'start' },
  ];
  [0, 100, 200, 300].forEach(t => {
    el.push({ type: 'line', points: [{ x: px(t), y: 430 }, { x: px(t), y: 438 }], color: AXE, strokeWidth: 2 });
    el.push({ type: 'text', x: px(t), y: 458, text: String(t), color: '#cbd5e1', fontSize: 16, align: 'middle' });
  });
  [10, 20, 30, 40, 50, 60].forEach(h => {
    el.push({ type: 'line', points: [{ x: 142, y: py(h) }, { x: 150, y: py(h) }], color: AXE, strokeWidth: 2 });
    el.push({ type: 'text', x: 132, y: py(h) + 6, text: String(h), color: '#cbd5e1', fontSize: 16, align: 'end' });
  });

  el.push({ type: 'line', dashed: true, color: GOLD, strokeWidth: 2,
    points: [{ x: px(40), y: 430 }, { x: px(40), y: 104 }] });
  el.push({ type: 'text', x: px(40) + 10, y: 96, text: 'pulse de O₂', color: GOLD, fontSize: 18, align: 'start' });

  el.push({ type: 'polyline', color: ORANGE, strokeWidth: 4,
    points: courbe.slice(0, shown + 1).map(([t, h]) => ({ x: px(t), y: py(h) })) });

  if (step >= 6) el.push({ type: 'text', x: px(95), y: 94, align: 'start',
    text: 'montée rapide : les H⁺ sortent de la matrice', color: ORANGE, fontSize: 18 });
  if (step >= 7) el.push({ type: 'text', x: px(150), y: py(44), align: 'start',
    text: 'décroissance lente : ils regagnent la matrice', color: '#67e8f9', fontSize: 18 });
  if (step >= 8) el.push({ type: 'text', x: px(60), y: py(6), align: 'start',
    text: 'sans O₂, aucun flux : la chaîne est à l’arrêt', color: '#4ade80', fontSize: 18 });

  return { engine: 'roughsvg', title: 'Flux de protons après un pulse de dioxygène', width: 960, height: 500,
    description: 'Concentration en protons du milieu avant et après une injection de dioxygène.', elements: el };
}

function moleculesGlucoseAtpSpec(_variant: string, step: number, _maxStep: number): RoughSVGVisualSpec {
  const phosphate = (x: number, text: string): RoughSVGElementSpec[] => [
    { type: 'circle', x, y: 210, radius: 34, color: '#22d3ee', fill: '#0c4a6e' },
    { type: 'text', x, y: 218, text, color: '#e0f2fe', fontSize: 22, align: 'middle' },
  ];
  const all: RoughSVGElementSpec[] = [
    { type: 'polygon', points: [{ x: 80, y: 120 }, { x: 155, y: 80 }, { x: 230, y: 120 }, { x: 230, y: 210 }, { x: 155, y: 250 }, { x: 80, y: 210 }], color: '#22c55e', fill: '#14532d' },
    { type: 'text', x: 155, y: 170, text: 'Glucose', color: 'white', fontSize: 26, align: 'middle' },
    { type: 'text', x: 155, y: 285, text: 'C₆H₁₂O₆ · hexose cyclique', color: '#bbf7d0', fontSize: 18, align: 'middle' },
    { type: 'rect', x: 330, y: 145, width: 105, height: 120, color: '#c084fc', fill: '#581c87' },
    { type: 'text', x: 382, y: 210, text: 'Adénine', color: 'white', fontSize: 19, align: 'middle' },
    { type: 'polygon', points: [{ x: 465, y: 150 }, { x: 535, y: 175 }, { x: 520, y: 250 }, { x: 450, y: 250 }, { x: 430, y: 185 }], color: '#fbbf24', fill: '#78350f' },
    { type: 'text', x: 485, y: 215, text: 'Ribose', color: 'white', fontSize: 18, align: 'middle' },
    ...phosphate(600, 'P'), ...phosphate(690, 'P'), ...phosphate(780, 'P'),
    { type: 'arrow', points: [{ x: 748, y: 150 }, { x: 748, y: 95 }], color: '#fb7185', strokeWidth: 4 },
    { type: 'text', x: 748, y: 72, text: 'liaison riche en énergie', color: '#fb7185', fontSize: 17, align: 'middle' },
    { type: 'text', x: 595, y: 330, text: 'ATP + H₂O ⇄ ADP + Pi + énergie', color: '#fef08a', fontSize: 25, align: 'middle' },
    { type: 'text', x: 595, y: 370, text: 'hydrolyse exoénergétique · phosphorylation endoénergétique', color: '#bae6fd', fontSize: 16, align: 'middle' },
  ];
  const countByStep = [3, 5, 9, 13, 15, all.length][Math.max(0, Math.min(5, Math.round(step)))] || all.length;
  return { engine: 'roughsvg', title: 'Le glucose stocke l’énergie ; l’ATP la transfère', width: 900, height: 430, elements: all.slice(0, countByStep) };
}

function rendementEnergetiqueSpec(_variant: string, step: number, _maxStep: number): RoughSVGVisualSpec {
  const lines = [
    'Glycolyse : 2 ATP + 2 NADH,H⁺',
    'Matrice : 2 ATP + 8 NADH,H⁺ + 2 FADH₂',
    'Total avant chaîne : 4 ATP + 10 NADH,H⁺ + 2 FADH₂',
    '1 NADH,H⁺ → 3 ATP ; 1 FADH₂ → 2 ATP',
    '4 + (10 × 3) + (2 × 2) = 38 ATP',
    'Navettes : 38 ATP (cœur, foie) ou 36 ATP (muscle, cerveau)',
    'Fermentation : 2 ATP', 'R = (E′ / 2860) × 100',
    'Même échelle : 2860 kJ par mole de glucose',
    'Respiration : 1159 kJ en ATP → 40,5 %',
    'Fermentation : 61 kJ en ATP → 2,13 %',
  ];
  const n = Math.max(1, Math.min(lines.length, Math.round(step) + 1));
  const elements: RoughSVGElementSpec[] = lines.slice(0, n).map((text, i) => ({
    type: 'text', x: 40, y: 45 + i * 28, text, color: i === n - 1 ? '#fef08a' : '#e2e8f0', fontSize: 17,
  }));
  if (step >= 8) elements.push(
    { type: 'rect', x: 500, y: 85, width: 330, height: 70, color: '#64748b' },
    { type: 'rect', x: 500, y: 85, width: 134, height: 70, color: '#22c55e', fill: '#166534' },
    { type: 'text', x: 665, y: 180, text: 'Respiration : 2860 kJ', color: 'white', fontSize: 16, align: 'middle' },
    { type: 'rect', x: 500, y: 250, width: 330, height: 70, color: '#64748b' },
    { type: 'rect', x: 500, y: 250, width: 7, height: 70, color: '#22c55e', fill: '#166534' },
    { type: 'text', x: 665, y: 345, text: 'Fermentation : 2860 kJ', color: 'white', fontSize: 16, align: 'middle' },
  );
  return { engine: 'roughsvg', title: 'Respiration et fermentation à la même échelle énergétique', width: 900, height: 410, elements,
    legend: [{ color: '#22c55e', label: 'Énergie conservée dans l’ATP' }, { color: '#64748b', label: 'Chaleur ou énergie résiduelle' }] };
}

function schemaBilanAnnoteSpec(_variant: string, step: number, _maxStep: number): RoughSVGVisualSpec {
  const labels = [
    '1 Glucose C₆H₁₂O₆', '2 Deux pyruvates', '3 2 ADP + 2 Pi → 2 ATP', '4 Glycolyse',
    '5–7 2 R′ → 2 R′H₂ · déshydrogénation', '8 Hyaloplasme', '9 Espace intermembranaire',
    '10 Matrice', '11 Pyruvates dans la matrice', '12 Décarboxylation · 6 CO₂',
    '13–15 10 R′ → 10 R′H₂', '16 2 ADP + 2 Pi → 2 ATP', '17 Membrane interne',
    '18 12 R′H₂ + 6 O₂', '19 12 R′ + 6 H₂O', '20 Sphère pédonculée',
    '21 Mitochondrie · 34 ATP',
  ];
  const shown = step >= 21 ? labels.length : Math.max(0, Math.min(labels.length, Math.round(step)));
  const elements: RoughSVGElementSpec[] = [
    { type: 'rect', x: 40, y: 35, width: 820, height: 100, color: '#38bdf8' },
    { type: 'text', x: 55, y: 60, text: 'HYALOPLASME', color: '#7dd3fc', fontSize: 18 },
    { type: 'ellipse', x: 60, y: 155, radiusX: 390, radiusY: 115, color: '#f59e0b' },
    { type: 'ellipse', x: 90, y: 175, radiusX: 350, radiusY: 90, color: '#fb7185' },
    { type: 'text', x: 450, y: 190, text: 'MITOCHONDRIE', color: '#fdba74', fontSize: 18, align: 'middle' },
    { type: 'arrow', points: [{ x: 200, y: 95 }, { x: 200, y: 225 }], color: '#22d3ee' },
    { type: 'arrow', points: [{ x: 400, y: 230 }, { x: 650, y: 230 }], color: '#22c55e' },
  ];
  labels.slice(0, shown).forEach((text, i) => elements.push({
    type: 'text', x: 55 + (i % 3) * 275, y: 310 + Math.floor(i / 3) * 30,
    text, color: i === shown - 1 ? '#fef08a' : '#e2e8f0', fontSize: 14,
  }));
  if (shown === 0) labels.forEach((_, i) => elements.push({ type: 'text', x: 85 + (i % 7) * 110, y: 335 + Math.floor(i / 7) * 35, text: String(i + 1), color: '#fef08a', fontSize: 18 }));
  return { engine: 'roughsvg', title: step === 0 ? 'Repères à identifier' : 'Correction progressive du schéma-bilan', width: 900, height: 520, elements };
}

function vesiculesAtpSynthaseSpec(_variant: string, step: number, _maxStep: number): RoughSVGVisualSpec {
  const elements: RoughSVGElementSpec[] = [
    { type: 'text', x: 70, y: 45, text: 'Mitochondrie', color: 'white', fontSize: 18 },
    { type: 'arrow', points: [{ x: 155, y: 42 }, { x: 250, y: 42 }], color: '#22d3ee' },
    { type: 'text', x: 280, y: 45, text: 'Ultrasons → fragments → vésicules retournées', color: '#bae6fd', fontSize: 18 },
  ];
  const experiments = [
    ['pHi 6 · pHe 4', 'Pas d’ATP', '#ef4444'], ['pHi 7 · pHe 7', 'Pas d’ATP', '#ef4444'], ['pHi 6 · pHe 9', 'ATP synthétisé', '#22c55e'],
  ];
  experiments.forEach((exp, i) => {
    if (step < 4 + i) return;
    const x = 185 + i * 270;
    elements.push(
      { type: 'circle', x, y: 220, radius: 82, color: '#c084fc' },
      { type: 'circle', x, y: 220, radius: 55, color: '#64748b' },
      { type: 'text', x, y: 215, text: exp[0], color: 'white', fontSize: 17, align: 'middle' },
      { type: 'text', x, y: 330, text: exp[1], color: exp[2], fontSize: 18, align: 'middle' },
    );
    for (let k = 0; k < 7; k += 1) elements.push({ type: 'circle', x: x - 60 + k * 20, y: 125, radius: 6, color: '#fb7185', fill: '#fb7185' });
    if (i === 2) elements.push({ type: 'arrow', points: [{ x, y: 195 }, { x, y: 120 }], color: '#fb7185', strokeWidth: 4 });
  });
  if (step >= 7) elements.push({ type: 'text', x: 450, y: 390, text: 'ATP seulement si pHi < pHe : [H⁺]i > [H⁺]e', color: '#fef08a', fontSize: 22, align: 'middle' });
  if (step >= 8) elements.push({ type: 'text', x: 450, y: 435, text: 'ADP + Pi · gradient de H⁺ sortant · ATP synthase', color: '#bbf7d0', fontSize: 19, align: 'middle' });
  return { engine: 'roughsvg', title: 'Les sphères pédonculées utilisent le gradient de protons', width: 900, height: 480, elements };
}

function chimiosmoseSpec(_variant: string, step: number, maxStep: number): CytoscapeVisualSpec {
  return processSpec(
    'Chaîne respiratoire de la membrane interne mitochondriale', 'breadthfirst',
    [
      ['nadh', 'NADH,H⁺'], ['ci', 'CI · 4 H⁺'], ['fadh2', 'FADH₂'], ['cii', 'CII · 0 H⁺'],
      ['q', 'Coenzyme Q'], ['ciii', 'CIII · 4 H⁺'], ['cytc', 'Cytochrome c'], ['civ', 'CIV · 2 H⁺'],
      ['o2', '½ O₂ + 2 H⁺'], ['h2o', 'H₂O'], ['gradient', 'Gradient de H⁺'],
      ['atpsynthase', 'ATP synthase · 3 H⁺/ATP'], ['atp', 'NADH → 3 ATP · FADH₂ → 2 ATP'],
    ],
    [
      ['nadh', 'ci', '2 e⁻'], ['ci', 'q'], ['fadh2', 'cii', '2 e⁻'], ['cii', 'q'],
      ['q', 'ciii'], ['ciii', 'cytc'], ['cytc', 'civ'], ['civ', 'o2'], ['o2', 'h2o'],
      ['ci', 'gradient', '4 H⁺'], ['ciii', 'gradient', '4 H⁺'], ['civ', 'gradient', '2 H⁺'],
      ['gradient', 'atpsynthase', 'retour des H⁺'], ['atpsynthase', 'atp', 'ADP + Pi'],
    ],
    ['nadh', 'ci', 'q', 'ciii', 'cytc', 'civ', 'o2', 'h2o', 'gradient', 'atpsynthase', 'atp'], step, maxStep,
  );
}

function metabolicSpec(_variant: string, step: number, maxStep: number): CytoscapeVisualSpec {
  const nodes: Array<[string, string]> = [
    ['glucose', 'Glucose'], ['glycolyse', 'Glycolyse : 2 ATP + 2 NADH,H⁺'], ['pyruvate', '2 pyruvates'],
    ['respiration', 'Respiration mitochondriale'], ['lactate', '2 acides lactiques'],
    ['acetaldehyde', '2 acétaldéhydes + 2 CO₂'], ['ethanol', '2 éthanols'],
    ['nad_resp', 'NAD⁺ régénéré'], ['nad_lac', 'NAD⁺ régénéré'], ['nad_eth', 'NAD⁺ régénéré'],
    ['conclusion', 'Sans régénération du NAD⁺, la glycolyse s’arrête'],
  ];
  const edges: Array<[string, string, string?]> = [
    ['glucose', 'glycolyse'], ['glycolyse', 'pyruvate'], ['pyruvate', 'respiration', 'avec O₂'],
    ['pyruvate', 'lactate', 'fermentation lactique'], ['pyruvate', 'acetaldehyde', 'décarboxylation'],
    ['acetaldehyde', 'ethanol', 'NADH,H⁺ → NAD⁺'], ['respiration', 'nad_resp'],
    ['lactate', 'nad_lac'], ['ethanol', 'nad_eth'], ['nad_resp', 'conclusion'], ['nad_lac', 'conclusion'], ['nad_eth', 'conclusion'],
  ];
  return processSpec('Trois devenirs du pyruvate, une même nécessité : régénérer le NAD⁺', 'breadthfirst', nodes, edges,
    nodes.map(([id]) => id), step, maxStep);
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
    case 'svt_ch1_glycolyse_etapes': return glycolyseEtapesSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_krebs_detaille': return krebsDetailleSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_echelle_redox': return echelleRedoxSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_ultrastructure_mitochondrie': return ultrastructureMitochondrieSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_flux_protons': return fluxProtonsSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_molecules_glucose_atp': return moleculesGlucoseAtpSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_rendement_energetique': return rendementEnergetiqueSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_schema_bilan_annote': return schemaBilanAnnoteSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_vesicules_atp_synthase': return vesiculesAtpSynthaseSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_chimiosmose': return chimiosmoseSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_carte_metabolique': return metabolicSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_myogrammes': return myogramSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_chaleurs_muscle': return muscleHeatSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_cycle_actomyosine': return actomyosineSpec(safeVariant, step, meta.maxStep);
    case 'svt_ch1_filieres_effort': return filieresSpec(safeVariant, step, meta.maxStep);
  }
}
