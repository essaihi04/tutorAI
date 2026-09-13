/** Carbon counts are per glucose; ATP uses the authored BAC convention (38). */
export const GLUCOSE_STOPS = [
  { title: 'Le glucose se partage', short: 'Glycolyse', place: 'Hyaloplasme', note: '6 carbones → deux molécules de 3 carbones.', atp: 2, carbon: 6, co2: 0,
    detail: '2 ATP sont investis, 4 sont formés : gain net de 2 ATP. Deux NAD⁺ deviennent 2 NADH,H⁺. Aucun O₂ consommé ici.' },
  { title: 'Les pyruvates entrent', short: 'Entrée', place: 'Matrice mitochondriale', note: 'Ce sont les pyruvates, pas le glucose, qui entrent.', atp: 2, carbon: 4, co2: 2,
    detail: 'Après le passage des deux membranes, chaque pyruvate perd un CO₂ et devient un acétyl-CoA à 2 carbones. Gain : 2 NADH,H⁺, aucun ATP direct.' },
  { title: 'Le cycle libère les carbones', short: 'Krebs', place: 'Matrice mitochondriale', note: 'Deux tours de cycle pour un glucose.', atp: 4, carbon: 0, co2: 6,
    detail: 'Bilan des deux tours : 4 CO₂, 2 ATP, 6 NADH,H⁺ et 2 FADH₂. Les carbones apportés par l’acétyl-CoA ne ressortent pas nécessairement dès le premier tour.' },
  { title: 'L’énergie devient ATP', short: 'Chaîne', place: 'Membrane interne', note: 'Les électrons voyagent ; les H⁺ font tourner l’ATP synthase.', atp: 38, carbon: 0, co2: 6,
    detail: 'Les transporteurs réduits cèdent leurs électrons. La chaîne pompe les H⁺ vers l’espace intermembranaire. Leur retour dans la matrice permet de former l’ATP. O₂ reçoit les électrons et forme H₂O. Bilan scolaire : 34 ATP.' },
  { title: 'Un glucose, deux bilans', short: 'Bilan', place: 'À l’échelle de la cellule', note: 'Compare l’énergie conservée dans l’ATP.', atp: 38, carbon: 0, co2: 6,
    detail: 'Convention du cours : 38 ATP × 30,5 / 2860 × 100 = 40,5 %. Fermentation : 2 ATP × 30,5 / 2860 × 100 = 2,13 %. Ces rendements scolaires ne sont pas des valeurs universelles.' },
] as const;

export function glucoseStop(step: number, maxStep: number) {
  const safe = Number.isFinite(step) ? Math.max(0, Math.min(maxStep, step)) : 0;
  return Math.min(4, Math.floor(safe / maxStep * 5));
}

export function glucoseStopStep(stop: number, maxStep: number) {
  return Math.ceil(Math.max(0, Math.min(4, stop)) * maxStep / 5);
}
