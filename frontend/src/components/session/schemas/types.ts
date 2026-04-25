/**
 * Types pour la bibliothèque de schémas SVG scientifiques
 */

export interface SchemaAnnotation {
  id: string;
  x: number;
  y: number;
  width: number;
  height: number;
  label: string;
  description: string;
  color?: string;
}

export interface SchemaLayer {
  id: string;
  label: string;
  svgContent: string;
  delay?: number;
}

export interface SchemaHighlight {
  id: string;
  targetLayerId?: string;
  cx: number;
  cy: number;
  radius: number;
  label: string;
}

export interface ScientificSchema {
  id: string;
  title: string;
  subject: 'svt' | 'physics' | 'chemistry' | 'math';
  keywords: string[];
  category: 'process' | 'structure' | 'cycle' | 'diagram' | 'graph' | 'comparison';
  viewBox: string;
  backgroundColor?: string;
  layers: SchemaLayer[];
  annotations: SchemaAnnotation[];
  highlights: SchemaHighlight[];
}
