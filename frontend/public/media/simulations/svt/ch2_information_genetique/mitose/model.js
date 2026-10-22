// TP « Mitose dans la racine d'oignon » : protocole, champ microscopique, phases,
// indice mitotique et durées relatives. Champ reproductible : même graine, même lame.

export const PHASES = ['interphase', 'prophase', 'metaphase', 'anaphase', 'telophase'];
export const PHASE_LABELS = {
  interphase: 'Interphase', prophase: 'Prophase', metaphase: 'Métaphase', anaphase: 'Anaphase', telophase: 'Télophase',
};

export const PROTOCOL = [
  { id: 'prelever', label: 'Couper l’extrémité (1 cm) d’une racine d’oignon', why: 'La division a lieu dans le méristème, juste derrière la coiffe.' },
  { id: 'fixer', label: 'Fixer dans le liquide de Carnoy', why: 'La fixation tue les cellules et arrête les divisions dans l’état où elles étaient.' },
  { id: 'hydrolyser', label: 'Hydrolyser dans HCl à 60 °C', why: 'L’acide ramollit les parois et dissocie les cellules, ce qui permet de les étaler.' },
  { id: 'rincer', label: 'Rincer à l’eau', why: 'Le rinçage élimine l’acide, qui gênerait la coloration.' },
  { id: 'colorer', label: 'Colorer à l’orcéine acétique', why: 'Le colorant se fixe sur l’ADN : chromatine et chromosomes deviennent visibles.' },
  { id: 'ecraser', label: 'Écraser entre lame et lamelle', why: 'L’écrasement étale les cellules en une seule couche, observable au microscope.' },
];

/** Messages ciblés quand une étape arrive trop tôt. Clé : « étape placée — étape oubliée avant ». */
const ORDER_MESSAGES = {
  'colorer-hydrolyser': 'Sans hydrolyse, les parois sont rigides et les cellules restent collées : on ne pourra pas les étaler.',
  'colorer-rincer': 'Il reste de l’acide : rince avant de colorer.',
  'ecraser-colorer': 'Si tu écrases avant de colorer, les noyaux ne seront pas visibles.',
  'hydrolyser-fixer': 'Fixe d’abord : sinon les cellules continuent de vivre et de se diviser pendant la préparation.',
};

export function assessOrder(sequence) {
  for (let i = 0; i < sequence.length; i++) {
    if (sequence[i] === PROTOCOL[i].id) continue;
    const placed = sequence[i], missing = PROTOCOL[i].id;
    return {
      correct: false, position: i,
      reason: ORDER_MESSAGES[`${placed}-${missing}`] ?? `Étape ${i + 1} : ce n’est pas encore le moment de « ${PROTOCOL.find(s => s.id === placed)?.label ?? placed} ». Que faut-il faire avant ?`,
    };
  }
  return sequence.length === PROTOCOL.length
    ? { correct: true, reason: 'Protocole correct : la lame est prête à être observée.' }
    : { correct: false, position: sequence.length, reason: 'Continue : il manque des étapes.' };
}

/** Générateur pseudo-aléatoire reproductible (mulberry32). */
export function rng(seed) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/** Composition du champ : 48 cellules, proportions réalistes d'un méristème de racine. */
export const COMPOSITION = { interphase: 34, prophase: 6, metaphase: 3, anaphase: 2, telophase: 3 };
export const COLS = 8, ROWS = 6;

export function generateField(seed = 7) {
  const random = rng(seed);
  const phases = Object.entries(COMPOSITION).flatMap(([phase, n]) => Array(n).fill(phase));
  for (let i = phases.length - 1; i > 0; i--) { const j = Math.floor(random() * (i + 1)); [phases[i], phases[j]] = [phases[j], phases[i]]; }
  const cells = phases.map((phase, index) => ({
    index, phase, col: index % COLS, row: Math.floor(index / COLS),
    tilt: (random() - 0.5) * 0.25, shade: random(), stretch: 0.9 + random() * 0.2, angle: (random() - 0.5) * 0.5,
  }));
  // Cinq cellules repérées pour l'identification : une par phase, dans un ordre mélangé.
  const marked = [];
  for (const phase of PHASES) marked.push(cells.find(c => c.phase === phase && !marked.includes(c.index)).index);
  for (let i = marked.length - 1; i > 0; i--) { const j = Math.floor(random() * (i + 1)); [marked[i], marked[j]] = [marked[j], marked[i]]; }
  return { seed, cells, marked, focus: 0.35 + random() * 0.3 };
}

export function counts(field) {
  const result = Object.fromEntries(PHASES.map(p => [p, 0]));
  for (const cell of field.cells) result[cell.phase]++;
  return result;
}

/** Ce qui distingue chaque phase de ses voisines, pour guider sans donner la réponse. */
const CONFUSIONS = {
  'interphase-prophase': 'Les chromosomes sont-ils visibles sous forme de filaments ? En interphase, la chromatine est diffuse et le nucléole visible.',
  'prophase-interphase': 'Regarde l’intérieur du noyau : des filaments distincts, ou une chromatine diffuse avec un nucléole ?',
  'prophase-metaphase': 'L’enveloppe du noyau est-elle encore là ? Les chromosomes sont-ils alignés au centre ?',
  'metaphase-prophase': 'Les chromosomes sont-ils groupés dans un noyau, ou alignés sur une ligne au milieu de la cellule ?',
  'metaphase-anaphase': 'Les chromosomes forment-ils encore une seule ligne au centre, ou deux groupes qui s’éloignent ?',
  'anaphase-metaphase': 'Vois-tu une seule plaque au centre, ou deux lots de chromosomes en route vers les pôles ?',
  'anaphase-telophase': 'Les deux lots sont-ils encore en mouvement, ou déjà regroupés en deux noyaux avec une paroi au milieu ?',
  'telophase-anaphase': 'Vois-tu deux noyaux qui se reforment et une nouvelle paroi entre eux ?',
  'interphase-telophase': 'Une seule cellule, mais deux noyaux et une paroi qui se forme au milieu : est-ce vraiment une interphase ?',
  'telophase-interphase': 'Combien de noyaux contient la cellule ?',
};
// Clé : « réponse donnée — phase réelle ». Le message aide à voir ce que l'élève a manqué.

export function assessIdentification(phase, answer) {
  if (answer === phase) return { correct: true, reason: `Oui : ${PHASE_LABELS[phase].toLowerCase()}.` };
  return { correct: false, reason: CONFUSIONS[`${answer}-${phase}`] ?? 'Observe l’état des chromosomes : diffus, condensés, alignés, séparés ou regroupés aux pôles ?' };
}

function parse(value) {
  return typeof value === 'number' ? value : Number(String(value ?? '').trim().replace(',', '.').replace('%', ''));
}

/** Indice mitotique = cellules en division / nombre total de cellules × 100. */
export function mitoticIndex(c) {
  const total = Object.values(c).reduce((a, b) => a + b, 0);
  return (total - c.interphase) / total * 100;
}

export function assessIndex(answer, c) {
  const value = parse(answer), expected = mitoticIndex(c);
  const total = Object.values(c).reduce((a, b) => a + b, 0), dividing = total - c.interphase;
  if (!Number.isFinite(value) || value <= 0) return { correct: false, reason: 'Saisis un pourcentage positif.' };
  if (Math.abs(value * 100 - expected) <= 1) return { correct: false, reason: 'C’est une fraction : multiplie par 100 pour l’exprimer en %.' };
  if (Math.abs(value - dividing / c.interphase * 100) <= 1) return { correct: false, reason: 'Divise par le nombre TOTAL de cellules, pas par celles en interphase.' };
  if (Math.abs(value - expected) <= 1) return { correct: true, reason: `Juste : IM = ${dividing} / ${total} × 100.` };
  return { correct: false, reason: 'IM = (nombre de cellules en division) / (nombre total de cellules) × 100. Les cellules en division sont en prophase, métaphase, anaphase ou télophase.' };
}

/** Durée d'une phase = (cellules dans la phase / total) × durée du cycle, en minutes. */
export function phaseDuration(c, phase, cycleHours) {
  const total = Object.values(c).reduce((a, b) => a + b, 0);
  return c[phase] / total * cycleHours * 60;
}

export function assessDuration(answer, c, phase, cycleHours) {
  const value = parse(answer), expected = phaseDuration(c, phase, cycleHours);
  const total = Object.values(c).reduce((a, b) => a + b, 0), dividing = total - c.interphase;
  if (!Number.isFinite(value) || value <= 0) return { correct: false, reason: 'Saisis une durée positive, en minutes.' };
  if (Math.abs(value * 60 - expected) <= 0.05 * expected) return { correct: false, reason: 'Ta valeur est en heures : convertis en minutes.' };
  if (Math.abs(value - c[phase] / dividing * cycleHours * 60) <= 0.05 * expected) return { correct: false, reason: 'Le dénominateur est le nombre total de cellules : toutes passent par le cycle, interphase comprise.' };
  if (Math.abs(value - expected) <= 0.05 * expected) return { correct: true, reason: `Juste : ${c[phase]} / ${total} × ${cycleHours} h = ${(expected).toFixed(0)} min. Plus une phase est courte, moins on y trouve de cellules.` };
  return { correct: false, reason: 'La proportion de cellules dans une phase est proportionnelle à la durée de cette phase : durée = (n / N) × durée du cycle.' };
}

/** Quantité d'ADN par cellule (en unités q) à un instant du cycle normalisé 0..1. */
export function dnaQuantity(x) {
  // G1 (0–0,4) : q ; S (0,4–0,7) : doublement ; G2 et mitose jusqu'à la séparation (0,7–0,95) : 2q ; cellules filles : q.
  if (x < 0.4) return 1;
  if (x < 0.7) return 1 + (x - 0.4) / 0.3;
  if (x < 0.95) return 2;
  return 1;
}

export const DNA_CHOICES = [
  { id: 'constant', label: 'Constante pendant tout le cycle' },
  { id: 'cycle', label: 'Doublée pendant l’interphase (phase S), puis divisée par deux à la fin de la mitose' },
  { id: 'halved', label: 'Divisée par deux pendant la prophase' },
];

export function assessDna(choice) {
  return choice === 'cycle'
    ? { correct: true, reason: 'Juste : l’ADN est répliqué en phase S, puis réparti également entre les deux cellules filles à l’anaphase-télophase.' }
    : choice === 'halved'
      ? { correct: false, reason: 'En prophase, les chromosomes se condensent seulement : chacun a déjà deux chromatides, la quantité d’ADN ne change pas.' }
      : { correct: false, reason: 'Si l’ADN ne doublait jamais, chaque division le diviserait par deux : que se passerait-il après quelques générations ?' };
}
