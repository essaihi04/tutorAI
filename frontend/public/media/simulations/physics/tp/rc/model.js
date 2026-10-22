// Dipôle RC idéal : générateur de tension E, conducteur ohmique R, condensateur C.
// Solutions exactes de RC·du/dt + u = E (charge) et RC·du/dt + u = 0 (décharge) :
// on n'intègre pas pas à pas, la courbe affichée est juste à tout instant.

export const LIMITS = {
  emf: [2, 12],            // V
  resistance: [100, 10000], // Ω
  capacitance: [10, 1000],  // µF
};

export function bounded(value, [min, max]) {
  return Number.isFinite(value) ? Math.min(max, Math.max(min, value)) : min;
}

/** τ = R·C, en secondes (R en Ω, C en µF). */
export function tau(resistance, capacitanceUf) {
  if (!(resistance > 0 && capacitanceUf > 0)) throw new RangeError('R et C doivent être positifs');
  return resistance * capacitanceUf / 1e6;
}

/** u_C(t) pendant la charge, condensateur initialement déchargé. */
export function chargeVoltage(emf, tauS, t) {
  return t <= 0 ? 0 : emf * (1 - Math.exp(-t / tauS));
}

/** u_C(t) pendant la décharge, depuis u0. */
export function dischargeVoltage(u0, tauS, t) {
  return t <= 0 ? u0 : u0 * Math.exp(-t / tauS);
}

/** i(t) en mA : charge positive, décharge négative (convention récepteur pour C). */
export function current(mode, emf, resistance, tauS, t) {
  const sign = mode === 'charge' ? 1 : -1;
  return sign * (emf / resistance) * Math.exp(-Math.max(0, t) / tauS) * 1000;
}

/** Énergie stockée ½·C·u², en mJ. */
export function energy(capacitanceUf, voltage) {
  return 0.5 * capacitanceUf * 1e-6 * voltage ** 2 * 1000;
}

/** La tangente à l'origine de la charge coupe l'asymptote u = E en t = τ. */
export function tangentAtOrigin(emf, tauS, t) {
  return (emf / tauS) * t;
}

/**
 * Une lecture de voltmètre : valeur exacte arrondie à la résolution de l'appareil
 * (0,01 V), plus un léger bruit reproductible pour que le tableau ressemble à une vraie
 * série de mesures. Le même essai donne toujours les mêmes valeurs.
 */
export function reading(exact, seed) {
  if (exact === 0) return 0; // condensateur vide : le voltmètre lit 0
  const noise = Math.sin(seed * 12.9898) * 43758.5453;
  const jitter = (noise - Math.floor(noise) - 0.5) * 0.02;
  return Math.round((exact + jitter) * 100) / 100;
}

/** Écart relatif en %, toujours positif. */
export function percentError(measured, reference) {
  if (!(reference > 0)) throw new RangeError('Référence invalide');
  return Math.abs(measured - reference) / reference * 100;
}

function parse(value) {
  return typeof value === 'number' ? value : Number(String(value ?? '').trim().replace(',', '.'));
}

/** La prédiction n'est pas notée : on la garde pour la confronter à la mesure. */
export function assessPrediction(choice) {
  const correct = choice === 'double';
  return {
    correct,
    reason: correct
      ? 'C’est ce que la mesure devra confirmer : τ = R·C est proportionnel à R.'
      : 'Garde ta prédiction en tête : la mesure va trancher.',
  };
}

/**
 * Vérifie la valeur de τ lue par l'élève. Tolérance 5 % : c'est l'ordre de la
 * précision d'une lecture graphique au bac.
 */
export function assessTau(answer, tauS, method) {
  const value = parse(answer);
  if (!Number.isFinite(value) || value <= 0) {
    return { correct: false, reason: 'Saisis une durée positive, en secondes.' };
  }
  if (Math.abs(value - tauS * 1000) <= 0.05 * tauS * 1000) {
    return { correct: false, reason: 'Ta valeur est en millisecondes : convertis en secondes.' };
  }
  if (percentError(value, tauS) <= 5) {
    return { correct: true, reason: method === 'tangent'
      ? 'Juste : la tangente à l’origine coupe l’asymptote u = E à t = τ.'
      : method === 'discharge'
        ? 'Juste : à t = τ, u_C ne vaut plus que 37 % de U₀.'
        : 'Juste : à t = τ, u_C atteint 63 % de E.' };
  }
  const hint = method === 'tangent'
    ? 'Trace la tangente à l’origine et lis l’abscisse de son intersection avec u = E.'
    : method === 'discharge'
      ? 'Cherche l’instant où u_C = 0,37 × U₀, pas 0,63 × U₀.'
      : 'Calcule d’abord 0,63 × E, puis lis l’instant où la courbe atteint cette tension.';
  return { correct: false, reason: hint };
}

/** Vérifie C déduite de τ et R, en µF. */
export function assessCapacitance(answer, tauMeasured, resistance, capacitanceUf) {
  const value = parse(answer);
  if (!Number.isFinite(value) || value <= 0) {
    return { correct: false, reason: 'Saisis une capacité positive, en µF.' };
  }
  const expected = tauMeasured / resistance * 1e6;
  if (percentError(value, expected * 1e-6) <= 5) {
    return { correct: false, reason: 'Ta valeur est en farads : exprime C en µF (1 F = 10⁶ µF).' };
  }
  if (percentError(value, expected) <= 5) {
    return { correct: true, reason: `Juste : C = τ / R. Écart avec la valeur nominale : ${percentError(value, capacitanceUf).toFixed(1).replace('.', ',')} %.` };
  }
  return { correct: false, reason: 'Utilise C = τ / R, avec τ en s et R en Ω : le résultat est en F, à convertir en µF.' };
}

/**
 * Un pas « rond » (1, 2 ou 5 × 10ⁿ) proche de span / count. Sert aux graduations et à
 * l'intervalle d'acquisition : un pas en fraction de τ donnerait la réponse à l'élève.
 */
export function niceStep(span, count) {
  const raw = span / count, mag = 10 ** Math.floor(Math.log10(raw));
  return [1, 2, 5, 10].map(k => k * mag).find(s => s >= raw * 0.999);
}

/** Durée d'observation : 5τ suffit, u_C dépasse alors 99 % de E. */
export function duration(tauS) {
  return 5 * tauS;
}
