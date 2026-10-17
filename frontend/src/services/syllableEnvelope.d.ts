export class SyllableEnvelope {
  constructor(options?: { floor?: number; slowTau?: number; low?: number; high?: number; attack?: number; release?: number; window?: number });
  readonly open: number;
  push(rms: number, dt: number, now: number, latency?: number): number;
  reset(): void;
}
