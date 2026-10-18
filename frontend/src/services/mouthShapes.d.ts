export type MouthViseme = 'viseme_aa' | 'viseme_E' | 'viseme_I' | 'viseme_O' | 'viseme_U' | 'viseme_SS';
export interface BandLevels { L1: number; L2: number; H: number; F: number; }
export const MOUTH_BANDS: Record<keyof BandLevels, [number, number]>;
export const MOUTH_VISEMES: MouthViseme[];
export function bandLevels(db: Float32Array | number[], binHz: number): BandLevels;
export function mouthShapeWeights(levels: BandLevels | null): Record<MouthViseme, number>;
export class MouthShaper {
  constructor(rate?: number);
  rate: number;
  weights: Record<MouthViseme, number>;
  trail: Array<[number, BandLevels | null]>;
  push(levels: BandLevels | null, open: number, dt: number, now?: number, latency?: number): Record<MouthViseme, number>;
  dominant(): MouthViseme | null;
}
