// Modèles idéalisés : petites perturbations, milieu homogène, sans réflexion.
export function pulse(x, centre, amplitude = 1) {
  const u = (x - centre) / .65;
  return Math.abs(u) >= 1 ? 0 : amplitude * Math.cos(Math.PI * u / 2) ** 2;
}
export function speed(tension, density) {
  if (!(tension > 0 && density > 0)) throw new RangeError('Milieu invalide');
  return Math.sqrt(tension / density);
}
export function springPosition(x, centre, amplitude = 1) {
  // Small enough to keep neighbouring spires ordered at maximum amplitude.
  return x + .15 * pulse(x, centre, amplitude);
}
export function arrivals(p) {
  if (!(p.sensor1 > 0 && p.sensor2 > p.sensor1 && p.speed > 0)) throw new RangeError('Capteurs invalides');
  return { a: p.sensor1 / p.speed, b: p.sensor2 / p.speed, distance: p.sensor2 - p.sensor1 };
}
export function assess(p, elapsed, answer) {
  const d = arrivals(p);
  if (elapsed < (p.sensor2 + .65) / p.speed) return { correct: false, reason: 'Attends la fin du passage aux deux capteurs.' };
  const tau = d.b - d.a;
  if (!Number.isFinite(answer.delay) || !Number.isFinite(answer.speed) || answer.delay <= 0 || answer.speed <= 0) return { correct: false, reason: 'Saisis un retard positif en secondes et une célérité en m/s.' };
  if (Math.abs(answer.delay - tau) > .02 * tau + .002) return { correct: false, reason: 'Relis les deux maxima : τ = tB − tA. Les dates sont en secondes.' };
  if (Math.abs(answer.speed - p.speed) > .05 * p.speed) return { correct: false, reason: 'Utilise AB, puis v = AB / τ. Vérifie les unités.' };
  return { correct: true, reason: 'Calcul correct : enregistre cet essai puis change la distance AB.' };
}
