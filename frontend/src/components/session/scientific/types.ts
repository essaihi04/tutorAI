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
}

export interface CytoscapeEdgeSpec {
  from: string;
  to: string;
  label?: string;
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

export interface MatterVisualSpec {
  engine: 'matter';
  title?: string;
  width?: number;
  height?: number;
  gravity?: ScientificPoint;
  autoplay?: boolean;
  bodies: MatterBodySpec[];
  constraints?: MatterConstraintSpec[];
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

export type ScientificVisualSpec =
  | JSXGraphVisualSpec
  | CytoscapeVisualSpec
  | MatterVisualSpec
  | RoughSVGVisualSpec;
