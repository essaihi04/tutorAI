/** Convention scolaire du chapitre, et non rendement universel des mitochondries. */
export type EnergyBalanceVariant = 'scene' | 'navette_36';
export const ENERGY_PHASES = [
  { label: 'Glycolyse', step: 0 },
  { label: 'Matrice', step: 3 },
  { label: 'Chaîne', step: 6 },
  { label: 'Bilan', step: 8 },
  { label: 'Rendement', step: 9 },
] as const;

export function energyPhase(step: number) {
  const safe = Number.isFinite(step) ? Math.max(0, Math.min(10, step)) : 0;
  return safe < 3 ? 0 : safe < 6 ? 1 : safe < 8 ? 2 : safe < 9 ? 3 : 4;
}

export function energyBalance(variant: string = 'scene') {
  const cytosolicNadhYield = variant === 'navette_36' ? 2 : 3;
  const glycolysisATP = 2;
  const matrixATP = 2;
  const nadhATP = 8 * 3 + 2 * cytosolicNadhYield;
  const fadh2ATP = 2 * 2;
  const chainATP = nadhATP + fadh2ATP;
  const totalATP = glycolysisATP + matrixATP + chainATP;
  const glucoseEnergy = 2860; // kJ par mole de glucose
  const atpEnergy = 30.5; // kJ par mole d'ATP, convention de calcul du cours
  const respirationEnergy = totalATP * atpEnergy;
  const fermentationEnergy = glycolysisATP * atpEnergy;
  return {
    glycolysisATP, matrixATP, nadhATP, fadh2ATP, chainATP, totalATP,
    cytosolicNadhYield, glucoseEnergy, atpEnergy, respirationEnergy, fermentationEnergy,
    respirationPercent: 100 * respirationEnergy / glucoseEnergy,
    fermentationPercent: 100 * fermentationEnergy / glucoseEnergy,
  };
}

export const energyNumber = (value: number, decimals = 0) => value.toLocaleString('fr-FR', {
  minimumFractionDigits: decimals, maximumFractionDigits: decimals,
});

export function energyExplanation(phase: number, variant: string) {
  const b = energyBalance(variant);
  return [
    'Dans le cytoplasme, un glucose donne deux pyruvates : 2 ATP nets et 2 NADH,H⁺. Les NADH transporteront leurs électrons vers la chaîne.',
    'Dans la matrice : oxydation des deux pyruvates puis deux tours de Krebs. Ensemble : 2 ATP, 8 NADH,H⁺ et 2 FADH₂. Les 2 ATP directs viennent du cycle de Krebs.',
    variant === 'navette_36'
      ? 'Convention 36 ATP : les 2 NADH cytoplasmiques rapportent 2 ATP chacun via la navette choisie. La chaîne fournit (8 × 3) + (2 × 2) + (2 × 2) = 32 ATP.'
      : 'Convention du cours : 1 NADH,H⁺ → 3 ATP ; 1 FADH₂ → 2 ATP. Les 10 NADH (2 + 8) et les 2 FADH₂ alimentent la chaîne : 30 + 4 = 34 ATP.',
    `Les 4 ATP directs (2 + 2) s’ajoutent aux ${b.chainATP} ATP de la chaîne : ${b.totalATP} ATP par glucose. Ne pas ajouter les NADH et FADH₂ au total : leur énergie est déjà comptée dans l’ATP de la chaîne. Les navettes expliquent la variante 36/38 du cours.`,
    `R = (énergie conservée dans l’ATP ÷ 2 860) × 100. Avec 30,5 kJ/mol d’ATP : respiration ${energyNumber(b.respirationEnergy)} kJ → ${energyNumber(b.respirationPercent, 1)} % ; fermentation 61 kJ → 2,13 %. Le reste est dissipé en chaleur ou reste dans les produits organiques de fermentation.`,
  ][phase] ?? '';
}
