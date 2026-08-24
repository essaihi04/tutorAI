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

export type ScientificPresetId =
  | 'svt_ch1_cycle_atp'
  | 'svt_ch1_levures_exao'
  | 'svt_ch1_chimiosmose'
  | 'svt_ch1_carte_metabolique'
  | 'svt_ch1_myogrammes'
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

export type ScientificVisualSpec =
  | JSXGraphVisualSpec
  | CytoscapeVisualSpec
  | MatterVisualSpec
  | RoughSVGVisualSpec
  | ScientificPresetVisualSpec;
