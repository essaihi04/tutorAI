/**
 * Formes de bouche (visèmes) du professeur, lues dans le spectre de la voix entendue.
 *
 * Indépendant de la langue : français, darija ou arabe, seul le son compte. Trois axes continus,
 * mesurés en décibels sur quatre bandes de fréquence :
 * - ouverture : 550–1100 Hz contre 250–500 Hz (premier formant haut pour « a », bas pour « i », « ou ») ;
 * - arrondi : 1500–3000 Hz très en dessous de 550–1100 Hz (« o », « ou ») ;
 * - avant : 1500–3000 Hz proche de 550–1100 Hz (« i », « é ») ;
 * - friction : 3500–8000 Hz qui domine (« s », « ch », « f »).
 * Réglé sur la voix française Hortense de Windows : les mots « papa », « beau », « ici », « sss »
 * donnent bien « a », « o », « i » et « s ». Pour une bouche de quelques dizaines de pixels, le
 * mouvement juste compte plus que le phonème exact.
 */
export const MOUTH_BANDS = { L1: [250, 500], L2: [550, 1100], H: [1500, 3000], F: [3500, 8000] };
export const MOUTH_VISEMES = ['viseme_aa', 'viseme_E', 'viseme_I', 'viseme_O', 'viseme_U', 'viseme_SS'];

const clamp = value => Math.max(0, Math.min(1, value));

/**
 * Niveau moyen (dB) de chaque bande, à partir de `AnalyserNode.getFloatFrequencyData`.
 * @param {Float32Array | number[]} db
 * @param {number} binHz largeur d'une case de fréquence (sampleRate / fftSize)
 */
export function bandLevels(db, binHz) {
  const levels = {};
  for (const [name, [lo, hi]] of Object.entries(MOUTH_BANDS)) {
    let sum = 0, count = 0;
    for (let i = Math.ceil(lo / binHz); i < Math.min(db.length, Math.floor(hi / binHz)); i++) {
      if (Number.isFinite(db[i])) { sum += db[i]; count++; }
    }
    levels[name] = count ? sum / count : -160;
  }
  return levels;
}

/**
 * Poids des visèmes (somme ≤ 1) pour un instant de voix. Sans mesure (rire, silence) : bouche « a ».
 * @param {{ L1: number, L2: number, H: number, F: number } | null} levels
 */
export function mouthShapeWeights(levels) {
  const weights = Object.fromEntries(MOUTH_VISEMES.map(name => [name, 0]));
  if (!levels) { weights.viseme_aa = 1; return weights; }
  const { L1, L2, H, F } = levels;
  const open = clamp((L2 - L1 + 22) / 18);
  const round = clamp((L2 - H - 16) / 10);
  const front = clamp((H - L2 + 12) / 8);
  const friction = clamp((F - Math.max(L1, L2) + 22) / 14);
  const voiced = 1 - friction;
  weights.viseme_aa = voiced * (1 - round) * (1 - front) * open;
  weights.viseme_E = voiced * (1 - round) * ((1 - front) * (1 - open) * 0.8 + front * open);
  weights.viseme_I = voiced * (1 - round) * front * (1 - open);
  weights.viseme_O = voiced * round * open;
  weights.viseme_U = voiced * round * (1 - open);
  weights.viseme_SS = friction;
  return weights;
}

/**
 * Lisse les formes d'une image à l'autre et les règle sur l'ouverture de la voix (0…1) :
 * en silence la bouche se referme sous la moustache, à chaque syllabe elle prend la forme du son.
 * Le spectre est retardé de la latence de sortie, comme l'ouverture (`SyllableEnvelope`) : la forme
 * tombe avec le son entendu.
 */
export class MouthShaper {
  /** @param {number} rate vitesse de passage d'une forme à l'autre (par seconde) */
  constructor(rate = 18) {
    this.rate = rate;
    this.weights = Object.fromEntries(MOUTH_VISEMES.map(name => [name, 0]));
    /** @type {Array<[number, any]>} */
    this.trail = [];
  }

  /**
   * @param {{ L1: number, L2: number, H: number, F: number } | null} levels
   * @param {number} open ouverture de la voix (0…1)
   * @param {number} dt secondes depuis l'image précédente
   * @param {number} [now] horloge en secondes
   * @param {number} [latency] latence de sortie audio en secondes
   */
  push(levels, open, dt, now = 0, latency = 0) {
    this.trail.push([now, levels]);
    while (this.trail.length > 2 && this.trail[0][0] < now - 0.6) this.trail.shift();
    const wanted = now - Math.min(0.48, Math.max(0, latency));
    let heard = this.trail[0][1];
    for (const [t, value] of this.trail) { if (t <= wanted) heard = value; else break; }
    const target = mouthShapeWeights(heard);
    const ease = 1 - Math.exp(-Math.max(0, dt) * this.rate);
    for (const name of MOUTH_VISEMES) this.weights[name] += (target[name] * clamp(open) - this.weights[name]) * ease;
    return this.weights;
  }

  /** La forme la plus marquée, ou `null` quand la bouche est fermée. */
  dominant() {
    let best = null, value = 0.05;
    for (const name of MOUTH_VISEMES) if (this.weights[name] > value) { best = name; value = this.weights[name]; }
    return best;
  }
}
