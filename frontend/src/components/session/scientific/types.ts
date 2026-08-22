export interface ScientificPoint {
  x: number;
  y: number;
}

export interface JSXGraphElementSpec {
  id?: string;
  type: 'point' | 'segment' | 'line' | 'arrow' | 'circle' | 'function';
  points?: ScientificPoint[];
  center?: ScientificPoint;
  radius?: number;
  expression?: string;
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

export type ScientificVisualSpec =
  | JSXGraphVisualSpec
  | CytoscapeVisualSpec
  | MatterVisualSpec;

