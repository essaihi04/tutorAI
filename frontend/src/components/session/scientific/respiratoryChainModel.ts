/** Authored teaching model, not a prediction of mitochondrial pH.
 * Equal reference volumes, no buffering: 22 markers represent a conserved
 * pool of H⁺, each equivalent to 5 nmol/L in its reference volume.
 * At maximum separation: 100 vs 10 nmol/L (pH 7 vs 8).
 * The electrical component is assumed to dissipate during relaxation too;
 * equal pH alone does NOT imply zero proton-motive force in real mitochondria.
 */
export const RESPIRATORY_MAX_STEP = 18;

export const RESPIRATORY_YIELDS = {
  nadh: { donor: 'NADH,H⁺', oxidized: 'NAD⁺', pumped: 10, atp: 3 },
  fadh2: { donor: 'FADH₂', oxidized: 'FAD', pumped: 6, atp: 2 },
} as const;

export function respiratoryGradientFrame(rawStep: number) {
  const step = Math.max(0, Math.min(RESPIRATORY_MAX_STEP, Number.isFinite(rawStep) ? rawStep : 0));
  const relaxing = step >= 13;
  const strength = relaxing ? (RESPIRATORY_MAX_STEP - step) / 5 : Math.min(1, Math.max(0, (step - 3) / 4));
  const intermembraneConcentration = 55 + 45 * strength;
  const matrixConcentration = 55 - 45 * strength;
  const intermembranePH = 9 - Math.log10(intermembraneConcentration);
  const matrixPH = 9 - Math.log10(matrixConcentration);
  const intermembraneParticles = Math.round(intermembraneConcentration / 5);
  return {
    step, strength, relaxing,
    phase: relaxing ? 'equilibrium' : step >= 9 ? 'return' : 'accumulation',
    electrons: step >= 1 && !relaxing,
    pumping: step >= 4 && !relaxing,
    returning: step >= 9 && strength > 0,
    makingAtp: step >= 11 && strength > 0,
    intermembraneConcentration, matrixConcentration,
    intermembranePH, matrixPH,
    deltaPH: matrixPH - intermembranePH,
    concentrationRatio: intermembraneConcentration / matrixConcentration,
    intermembraneParticles, matrixParticles: 22 - intermembraneParticles,
  } as const;
}
