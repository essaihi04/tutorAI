export interface ScientificPoint {
  x: number;
  y: number;
}

export interface JSXGraphElementSpec {
  id?: string;
  type:
    | 'point' | 'segment' | 'line' | 'arrow' | 'circle' | 'function'
    | 'text' | 'polygon' | 'angle' | 'area';
  points?: ScientificPoint[];
  center?: ScientificPoint;
  radius?: number;
  expression?: string;
  /** Bornes d'une courbe ou d'une aire : une trajectoire s'arrête au sol. */
  domain?: [number, number];
  /** Polygone plein (défaut) ou contour seul. */
  filled?: boolean;
  label?: string;
  color?: string;
  draggable?: boolean;
  dashed?: boolean;
}

export interface JSXGraphVisualSpec {
  engine: 'jsxgraph';
  title?: string;
  boundingBox?: [number, number, number, number];
  axis?: boolean;
  grid?: boolean;
  /** Nom et unité de l'axe — « t (s) ». Un axe anonyme est faux au BAC. */
  xLabel?: string;
  yLabel?: string;
  elements: JSXGraphElementSpec[];
}

export interface CytoscapeNodeSpec {
  id: string;
  label: string;
  color?: string;
  /** Un état actif reçoit un contour lumineux dans les scènes pilotées. */
  active?: boolean;
}

export interface CytoscapeEdgeSpec {
  from: string;
  to: string;
  label?: string;
  color?: string;
  active?: boolean;
}

export interface CytoscapeVisualSpec {
  engine: 'cytoscape';
  title?: string;
  layout?: 'breadthfirst' | 'circle' | 'grid' | 'cose';
  nodes: CytoscapeNodeSpec[];
  edges: CytoscapeEdgeSpec[];
}

export interface MatterBodySpec {
  id: string;
  shape: 'rectangle' | 'circle';
  x: number;
  y: number;
  width?: number;
  height?: number;
  radius?: number;
  label?: string;
  color?: string;
  /** Inclinaison en radians — indispensable au plan incliné. */
  angle?: number;
  isStatic?: boolean;
  restitution?: number;
  friction?: number;
  /** 0 par défaut : sans quoi une chute libre tend vers une vitesse limite. */
  frictionAir?: number;
  velocity?: ScientificPoint;
}

export interface MatterConstraintSpec {
  fromBody?: string;
  toBody?: string;
  pointA?: ScientificPoint;
  pointB?: ScientificPoint;
  length?: number;
  stiffness?: number;
}

export type MatterQuantity =
  | 'x' | 'y' | 'height' | 'vx' | 'vy' | 'speed' | 'angle' | 'time';

/** Une grandeur lue en direct : c'est ce qui fait d'une animation une mesure. */
export interface MatterMeasureSpec {
  quantity: MatterQuantity;
  /** Absent pour `time`, qui n'appartient à aucun corps. */
  body?: string;
  label: string;
  /** Retirée en amont si la scène n'a pas d'échelle : pas d'unité inventée. */
  unit?: string;
  decimals: number;
  /** `height` seulement : ordonnée du sol, l'axe y de Matter descendant. */
  origin?: number;
}

/** Un réglage que l'élève déplace ; la scène rejoue alors depuis le début. */
export interface MatterParameterSpec {
  target: string;
  label: string;
  min: number;
  max: number;
  step: number;
  value: number;
  unit?: string;
}

export interface MatterVisualSpec {
  engine: 'matter';
  title?: string;
  width?: number;
  height?: number;
  gravity?: ScientificPoint;
  autoplay?: boolean;
  bodies: MatterBodySpec[];
  constraints?: MatterConstraintSpec[];
  /** Pixels par mètre. Sans elle, aucune mesure ne porte d'unité. */
  scale?: number;
  measures?: MatterMeasureSpec[];
  parameters?: MatterParameterSpec[];
}

export type RoughSVGElementType =
  | 'line'
  | 'arrow'
  | 'rect'
  | 'circle'
  | 'ellipse'
  | 'polygon'
  | 'polyline'
  | 'text';

export interface RoughSVGElementSpec {
  id?: string;
  type: RoughSVGElementType;
  x?: number;
  y?: number;
  width?: number;
  height?: number;
  radius?: number;
  radiusX?: number;
  radiusY?: number;
  points?: ScientificPoint[];
  text?: string;
  color?: string;
  fill?: string;
  strokeWidth?: number;
  fontSize?: number;
  align?: 'start' | 'middle' | 'end';
  dashed?: boolean;
}

export interface RoughSVGLegendItem {
  color: string;
  label: string;
}

/**
 * SVG scientifique déclaratif et sécurisé. Il couvre les structures
 * spatiales (cellules, appareils, chromosomes, circuits, coupes) qui ne
 * relèvent ni d'un repère JSXGraph, ni d'un réseau Cytoscape, ni d'une
 * simulation mécanique Matter.js.
 */
export interface RoughSVGVisualSpec {
  engine: 'roughsvg';
  title?: string;
  description?: string;
  width?: number;
  height?: number;
  background?: string;
  elements: RoughSVGElementSpec[];
  legend?: RoughSVGLegendItem[];
}

export type Mitochondrion3DPart =
  | 'all'
  | 'outer_membrane'
  | 'intermembrane_space'
  | 'inner_membrane'
  | 'cristae'
  | 'matrix'
  | 'mitochondrial_dna';

/**
 * Scène Three.js strictement bornée au modèle scientifique versionné.
 *
 * Le LLM choisit seulement l'état de la scène. Il ne peut fournir ni
 * géométrie, ni matériau, ni texture, ni URL, ni code exécutable.
 */
export interface Mitochondrion3DVisualSpec {
  engine: 'three';
  model: 'mitochondrion';
  title?: string;
  description?: string;
  autoplay?: boolean;
  labels?: boolean;
  focus?: Mitochondrion3DPart;
}

export type MuscleExcitation3DPart =
  | 'all'
  | 'muscle'
  | 'fascicle'
  | 'muscle_fiber'
  | 'myofibril'
  | 'neuromuscular_junction'
  | 'sarcolemma'
  | 't_tubule'
  | 'sarcoplasmic_reticulum'
  | 'calcium'
  | 'troponin'
  | 'tropomyosin'
  | 'actin'
  | 'myosin'
  | 'atp'
  | 'sarcomere';

/**
 * Modèle 3D procédural et versionné du couplage excitation–contraction.
 * Le LLM choisit uniquement l'étape et le repère ; la géométrie reste dans
 * le composant pédagogique audité.
 */
export interface MuscleExcitation3DVisualSpec {
  engine: 'three';
  model: 'muscle_excitation_contraction';
  title?: string;
  description?: string;
  autoplay?: boolean;
  labels?: boolean;
  focus?: MuscleExcitation3DPart;
  step?: number;
}

export type ScientificPresetId =
  | 'phys_ch1_propagation_onde'
  | 'phys_ch1_types_ondes'
  | 'phys_ch1_celerite_corde'
  | 'chem_ch1_facteurs_cinetiques'
  | 'chem_ch1_energie_activation'
  | 'chem_ch1_oxydoreduction'
  | 'svt_ch1_respiration_mitochondriale'
  | 'svt_ch1_glissement_sarcomere'
  | 'svt_ch1_couplage_excitation_contraction'
  | 'svt_ch1_cycle_atp'
  | 'svt_ch1_levures_exao'
  | 'svt_ch1_glycolyse_etapes'
  | 'svt_ch1_krebs_detaille'
  | 'svt_ch1_echelle_redox'
  | 'svt_ch1_molecules_glucose_atp'
  | 'svt_ch1_rendement_energetique'
  | 'svt_ch1_schema_bilan_annote'
  | 'svt_ch1_vesicules_atp_synthase'
  | 'svt_ch1_ultrastructure_mitochondrie'
  | 'svt_ch1_flux_protons'
  | 'svt_ch1_chimiosmose'
  | 'svt_ch1_carte_metabolique'
  | 'svt_ch1_myogrammes'
  | 'svt_ch1_chaleurs_muscle'
  | 'svt_ch1_cycle_actomyosine'
  | 'svt_ch1_filieres_effort';

/**
 * Référence sûre vers une scène versionnée. Le LLM choisit un identifiant et
 * un état ; le navigateur résout ensuite la scène vers JSXGraph/Cytoscape.
 * Aucun code, HTML ou URL n'est accepté dans ce contrat.
 */
export interface ScientificPresetVisualSpec {
  engine: 'preset';
  /** Facultatif pour les consommateurs génériques ; le catalogue reste source de vérité. */
  title?: string;
  presetId: ScientificPresetId;
  variant?: string;
  autoplay?: boolean;
  step?: number;
}

export type ScientificControlName =
  | 'start' | 'pause' | 'reset' | 'next' | 'previous' | 'set_variant' | 'highlight';

export interface ScientificControlCommand {
  /** Permet de rejouer deux commandes identiques reçues à la suite. */
  sequence: number;
  presetId: ScientificPresetId;
  command: ScientificControlName;
  parameters?: { variant?: string; step?: number };
}

/** État compact renvoyé au tuteur pour qu'il puisse suivre la scène. */
export interface ScientificSimulationUpdate {
  type: 'simulation_state';
  simulation_id: ScientificPresetId;
  current_state: {
    simulation_status: 'idle' | 'running' | 'paused' | 'finished';
    preset_id: ScientificPresetId;
    variant: string;
    step: number;
    max_step: number;
  };
  student_actions: Array<{
    action: string;
    variant: string;
    step: number;
  }>;
  objective_progress: number;
  timestamp: string;
}

export type ScientificVisualSpec =
  | JSXGraphVisualSpec
  | CytoscapeVisualSpec
  | MatterVisualSpec
  | RoughSVGVisualSpec
  | Mitochondrion3DVisualSpec
  | MuscleExcitation3DVisualSpec
  | ScientificPresetVisualSpec;
