export const VISEMES: string[];
export class LipSyncAnalyser {
  connect(source: AnalyserNode): void;
  disconnect(): void;
  sample(): Record<string, number> | null;
  getAmplitude(): number;
}
