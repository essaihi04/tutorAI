// Ondes mécaniques progressives — laboratoire dessiné au tableau.
// Le modèle physique est dans model.js ; le dessin à la craie et le pont tuteur dans shared/tableau/tableau.js.
import { pulse, speed, springPosition, arrivals, assess } from './model.js';

const { Craie, fr, nombre, bulle, ecrire, onglets, curseur, glisser, protocole } = window.Tableau;
const $ = id => document.getElementById(id);
const variants = {
  cord: ['Corde', 'Un point reste près de sa place', 'Suis le point orange pendant le passage de l’impulsion.', 'Le déplacement du point orange est…', ['Perpendiculaire à la propagation', 'Parallèle à la propagation', 'Un voyage jusqu’au bout de la corde'], 0, 'Compare la flèche horizontale et le mouvement du point.'],
  spring: ['Ressort', 'Une compression de proche en proche', 'Suis une spire repérée et compare les directions.', 'Le mouvement local des spires est…', ['Parallèle à la propagation', 'Perpendiculaire à la propagation', 'Un transport de tout le ressort'], 0, 'Observe la spire orange et sa position d’équilibre.'],
  water: ['Surface de l’eau', 'Une perturbation dans un plan', 'Lance une perturbation au centre et observe le front circulaire.', 'Dans ce modèle, les rides se propagent…', ['Dans le plan de la surface : 2D', 'Sur une seule droite : 1D', 'Dans tout le volume de l’eau : 3D'], 0, 'La vue montre le dessus de la surface.'],
  sound: ['Son dans l’air', 'L’air vibre localement', 'Observe la membrane, les compressions et un point matériel orange.', 'Dans l’air, le son est une onde…', ['Longitudinale', 'Transversale', 'Qui transporte les molécules jusqu’à l’oreille'], 0, 'Les points oscillent horizontalement autour de leurs positions de repos.'],
  vacuum: ['Cloche à vide', 'Quel rôle joue le milieu ?', 'Compare deux quantités d’air. La source continue à vibrer.', 'Quand on retire presque tout l’air, la transmission sonore par l’air…', ['Diminue alors que la source peut encore vibrer', 'Augmente', 'Ne dépend pas de l’air'], 0, 'Compare le mouvement de la source et la jauge de transmission.'],
  superposition: ['Superposition', 'Avant, pendant, après', 'Essaie les deux signes. À t = 2,5 s les centres coïncident.', 'Après leur rencontre, deux petites impulsions idéales…', ['Poursuivent leur propagation', 'Disparaissent définitivement', 'Restent bloquées au centre'], 0, 'Arrête à 2,5 s, puis observe à 4 s.'],
  medium: ['Influence du milieu', 'Qu’est-ce qui change la célérité ?', 'Compare tension et masse linéique, puis change seulement l’amplitude.', 'À tension et masse linéique fixées, augmenter une petite amplitude…', ['Ne change pas la célérité du modèle', 'Double toujours la célérité', 'Arrête la propagation'], 0, 'Dans ce modèle linéaire : v = √(T/μ).'],
  progressive: ['Capteurs et retard', 'Mesurer puis calculer', 'Glisse les capteurs A et B sur la corde, lance, lis tA et tB, calcule τ et v, puis compare deux distances.', 'Calcule à partir de tes lectures.', [], 0, 'τ = tB − tA ; v = AB/τ. Les axes sont en secondes et mètres.'],
};
const id = 'physics_waves_advanced_lab';
const query = new URLSearchParams(location.search);
const initial = variants[query.get('variant')] ? query.get('variant') : 'cord';
const focusOnly = query.get('scope') === 'single';
if (focusOnly) document.body.classList.add('scope-single');
const S = { variant: initial, time: 0, running: false, observed: false, status: 'idle', completed: new Set(), measurements: [], visits: {}, attempts: 0, hints: 0, validated: false, trial: null, stopAt: null,
  ouvert: performance.now(), marques: { a: null, b: null, resultat: null }, dirty: true,
  params: { speed: 4, sensor1: 2, sensor2: 7, amplitude: 1, tension: 4, density: .25, air: 100, sign: -1 } };
const numericLimits = { speed: [1, 10], sensor1: [1, 5], sensor2: [5.5, 9], amplitude: [.3, 1.5], tension: [1, 9], density: [.1, .5], air: [0, 100], sign: [-1, 1] };
const commandMap = { speed_m_s: 'speed', sensor_1_m: 'sensor1', sensor_2_m: 'sensor2', mass_density_kg_m: 'density', tension_n: 'tension' };
const commands = ['start', 'set_variant', 'set_parameters', 'fire_pulse', 'pause', 'step', 'run_until', 'set_time', 'record_measurement', 'check', 'reset', 'reveal_hint'];
const config = { id, version: '4.0', title: 'Ondes mécaniques progressives', variants: Object.entries(variants).map(([k, v]) => ({ id: k, label: v[0], objective: v[2] })), commands,
  command_schema: { set_variant: { variant_id: Object.keys(variants).join(' | ') }, run_until: { time_s: '0..duration_s (lance si besoin, puis s’arrête à cet instant)' }, set_time: { time_s: '0..duration_s (saute à cet instant, en pause)' }, set_parameters: { speed_m_s: '1..10', sensor_1_m: '1..5', sensor_2_m: '5.5..9', amplitude: '.3..1.5', tension_n: '1..9', mass_density_kg_m: '.1...5', air: '0..100', sign: '-1 | 1' } } };

const ratio = () => focusOnly ? Number(S.completed.has(S.variant)) : S.completed.size / Object.keys(variants).length;
const snapshot = () => ({ simulation_status: S.status, current_variant: S.variant, time_s: +S.time.toFixed(2), duration_s: +duration().toFixed(2), parameters: { ...S.params }, acquisition_complete: acquired(), student_observed: S.observed, attempts: S.attempts, hints_used: S.hints, completed_variants: [...S.completed], measurements: S.measurements, student_response: readAnswer(), objective_progress: ratio() });
const pont = protocole({ id, commandes: commands, config, etat: snapshot, progression: ratio, executer,
  texte: 'Huit expériences dessinées au tableau : corde, ressort, eau, son, cloche, superposition, milieu et retard. Dans « Capteurs et retard », l’élève glisse les capteurs A et B sur la corde, lit tA et tB, puis saisit τ et v ; deux calculs validés à distances différentes terminent la mesure.' });
const log = (a, d) => pont.noter(a, { ...d, variant: S.variant });
function emit(extra) { pont.emettre(extra); $('progress').textContent = focusOnly ? (ratio() ? 'Objectif validé' : '') : `${S.completed.size} / 8`; }
const feedback = (text, error = false) => bulle($('feedback'), text, error ? 'bad' : '');
const scene = () => (performance.now() - S.ouvert) / 1000;
const redraw = () => { S.dirty = true; };

// ── Panneaux : réglages (bas gauche) et réponse (haut droite) ───────────────
function controls() {
  const box = $('controls'); box.replaceChildren();
  const add = (key, label, min, max, step, unit) => box.append(curseur({ id: key, label, min, max, step, valeur: S.params[key], unite: unit, onchange: v => setParameters({ [key]: v }) }));
  if (S.variant === 'medium') { add('tension', 'Tension T', 1, 9, 1, 'N'); add('density', 'Masse linéique μ', .1, .5, .05, 'kg/m'); add('amplitude', 'Amplitude', .3, 1.5, .1, ''); }
  else if (S.variant === 'vacuum') add('air', 'Air restant', 0, 100, 10, '%');
  else if (S.variant === 'superposition') {
    const c = document.createElement('div'); c.className = 'choix';
    c.innerHTML = `<label><input type="radio" name="sign" value="-1"> signe opposé</label><label><input type="radio" name="sign" value="1"> même signe</label>`;
    c.querySelector(`[value="${S.params.sign}"]`).checked = true;
    c.addEventListener('change', e => setParameters({ sign: Number(e.target.value) })); box.append(c);
  }
  else if (S.variant !== 'progressive') add('amplitude', 'Amplitude', .3, 1.5, .1, '');
  $('settings').hidden = !box.children.length;
}
function responses() {
  ecrire($('question'), variants[S.variant][3]); const r = $('response'); r.replaceChildren();
  if (S.variant === 'progressive') {
    r.innerHTML = '<label class="craie-champ">τ = <input id="delayAnswer" type="text" inputmode="decimal" autocomplete="off" placeholder="0,00"> s</label><label class="craie-champ">v = <input id="speedAnswer" type="text" inputmode="decimal" autocomplete="off" placeholder="0,0"> m·s⁻¹</label>';
  } else {
    const options = variants[S.variant][4], offset = Object.keys(variants).indexOf(S.variant) % options.length, c = document.createElement('div'); c.className = 'choix';
    options.map((_, i) => (i + offset) % options.length).forEach(i => { const l = document.createElement('label'); l.innerHTML = `<input type="radio" name="choice" value="${i}"> `; l.append(options[i]); c.append(l); });
    r.append(c);
  }
  r.oninput = () => { S.validated = false; };
  updateHistory();
}
function updateHistory() { $('history').textContent = S.variant === 'progressive' ? S.measurements.slice(-2).map(m => `AB ${fr(m.distance_m)} m : τ ${fr(m.student_delay_s, 3)} s ; v ${fr(m.student_speed_m_s, 1)} m/s`).join(' · ') : ''; }

// ── Actions ──────────────────────────────────────────────────────────────────
function duration() { return S.variant === 'progressive' ? 10.7 / S.params.speed : S.variant === 'medium' ? 10.7 / speed(S.params.tension, S.params.density) : 5; }
function acquired() { return S.variant === 'progressive' && !!S.trial && S.time >= (S.trial.sensor2 + .65) / S.trial.speed; }
function observe() {
  if (S.time < Math.min(S.variant === 'superposition' ? 4 : .4, duration())) return;
  S.observed = true;
  const key = S.variant === 'vacuum' ? S.params.air : S.variant === 'medium' ? `${S.params.tension}/${S.params.density}/${S.params.amplitude}` : S.variant === 'superposition' ? S.params.sign : 'seen';
  (S.visits[S.variant] ??= new Set()).add(key);
}
function runLabel() { $('run').textContent = S.running ? 'Pause' : S.trial && S.time > 0 && S.time < duration() ? 'Reprendre' : 'Lancer'; }
function reset(keepScene = true) {
  S.running = false; S.stopAt = null; S.time = 0; S.observed = false; S.validated = false; S.trial = null; S.status = 'idle'; S.marques = { a: null, b: null, resultat: null };
  if (!keepScene) S.ouvert = performance.now();
  runLabel(); log('reset'); feedback('Nouvel essai : lance, puis observe la perturbation.'); redraw(); emit();
}
function setVariant(variant) {
  if (!variants[variant]) return;
  S.variant = variant; const v = variants[variant];
  onglets($('onglets'), config.variants, variant, setVariant, S.completed);
  ecrire($('title'), v[1]); ecrire($('objective'), v[2], { vitesse: 60 });
  controls(); responses(); reset(false); log('set_variant', { variant_id: variant }); emit();
}
function setParameters(values) {
  let changed = false;
  for (const [raw, value] of Object.entries(values || {})) {
    const key = commandMap[raw] || raw, bounds = numericLimits[key];
    if (!bounds || !Number.isFinite(Number(value))) continue;
    const v = Math.min(bounds[1], Math.max(bounds[0], Number(value)));
    if (key === 'sign' && v !== -1 && v !== 1) continue;
    if (S.params[key] !== v) { S.params[key] = v; changed = true; }
  }
  if (changed) { reset(); controls(); log('set_parameters', { ...S.params }); emit(); }
}
function launch() { S.time = 0; S.stopAt = null; S.running = true; S.observed = false; S.validated = false; S.trial = { ...S.params }; S.status = 'running'; S.marques = { a: null, b: null, resultat: null }; runLabel(); log('fire_pulse', { ...S.trial }); feedback('Observe. Tu peux mettre en pause et avancer pas à pas.'); emit(); }
function pause() { if (!S.trial) return; S.running = !S.running; if (S.time >= duration()) S.running = false; if (S.status !== 'finished') S.status = S.running ? 'running' : 'paused'; runLabel(); log('pause'); emit(); }
function toggleRun() { if (S.running) pause(); else if (S.trial && S.time > 0 && S.time < duration()) pause(); else launch(); }
function step() { if (!S.trial) S.trial = { ...S.params }; S.running = false; S.time = Math.min(duration(), S.time + .1); if (S.status !== 'finished') S.status = 'paused'; observe(); runLabel(); redraw(); log('step'); emit(); }
const clampTime = t => Math.min(duration(), Math.max(0, Number(t) || 0));
function setTime(t) { const target = clampTime(t); if (!S.trial) S.trial = { ...S.params }; S.running = false; S.stopAt = null; S.time = target; if (S.status !== 'finished') S.status = 'paused'; observe(); runLabel(); redraw(); log('set_time', { time_s: target }); feedback(`Arrêt à t = ${fr(target)} s. Observe, puis reprends ou avance pas à pas.`); emit(); }
function runUntil(t) { const target = clampTime(t); if (!S.trial || S.time >= target) launch(); S.stopAt = target; S.running = true; S.status = 'running'; runLabel(); log('run_until', { time_s: target }); emit(); }
const number = elId => nombre($(elId)?.value);
function readAnswer() { if (S.variant === 'progressive') return { delay_s: Number.isFinite(number('delayAnswer')) ? number('delayAnswer') : null, speed_m_s: Number.isFinite(number('speedAnswer')) ? number('speedAnswer') : null }; return { choice: document.querySelector('input[name=choice]:checked')?.value ?? null }; }
function complete() { S.completed.add(S.variant); S.status = 'finished'; onglets($('onglets'), config.variants, S.variant, setVariant, S.completed); feedback('Objectif validé. Explique maintenant ton observation au tuteur.', false); $('feedback').dataset.kind = 'good'; emit({ correct: true }); }
function check() {
  S.attempts++; log('check', { answer: readAnswer() });
  if (!S.observed) { feedback('Lance et observe l’expérience avant de répondre.', true); emit({ correct: false }); return; }
  if (S.variant === 'progressive') {
    const result = assess(S.trial, S.time, { delay: number('delayAnswer'), speed: number('speedAnswer') });
    S.validated = result.correct; feedback(result.reason, !result.correct); emit({ correct: result.correct });
    if (result.correct) { S.marques.resultat = scene(); redraw(); recordMeasurement(); }
    return;
  }
  const visits = S.visits[S.variant];
  if (S.variant === 'vacuum' && !(visits?.has(100) && visits?.has(0))) { feedback('Compare une observation à 100 % d’air et une à 0 %.', true); emit({ correct: false }); return; }
  if (S.variant === 'superposition' && !(visits?.has(-1) && visits?.has(1))) { feedback('Observe les deux cas : même signe et signe opposé.', true); emit({ correct: false }); return; }
  if (S.variant === 'medium') {
    const trials = [...(visits || [])].map(x => x.split('/').map(Number));
    const amplitudeOnly = trials.some(a => trials.some(b => a[0] === b[0] && a[1] === b[1] && a[2] !== b[2]));
    const mediumOnly = trials.some(a => trials.some(b => a[2] === b[2] && ((a[0] !== b[0] && a[1] === b[1]) || (a[0] === b[0] && a[1] !== b[1]))));
    if (!amplitudeOnly || !mediumOnly) { feedback('Compare le milieu en gardant l’amplitude fixe, puis change seulement l’amplitude.', true); emit({ correct: false }); return; }
  }
  const correct = readAnswer().choice !== null && Number(readAnswer().choice) === variants[S.variant][5];
  if (correct) complete(); else { feedback('Réessaie en comparant les mouvements et les directions.', true); emit({ correct: false }); }
}
function recordMeasurement() {
  if (!S.validated || !acquired()) { feedback('Termine l’acquisition et vérifie ton calcul avant de l’enregistrer.', true); return; }
  const result = assess(S.trial, S.time, { delay: number('delayAnswer'), speed: number('speedAnswer') }); if (!result.correct) return;
  const a = arrivals(S.trial), item = { distance_m: a.distance, arrival_1_s: a.a, arrival_2_s: a.b, student_delay_s: number('delayAnswer'), student_speed_m_s: number('speedAnswer'), parameters: { ...S.trial } };
  S.measurements.push(item); S.measurements = S.measurements.slice(-12); S.validated = false; log('record_measurement', item); updateHistory();
  if (S.measurements.some(m => m.distance_m !== item.distance_m && m.parameters.speed === item.parameters.speed)) complete();
  else { feedback('Calcul juste, essai noté. Glisse B à une autre distance, relance et compare.'); $('feedback').dataset.kind = 'good'; emit(); }
}
function hint() { S.hints++; feedback(variants[S.variant][6]); log('reveal_hint'); emit(); }
function executer(command, p) {
  if (command === 'set_variant') setVariant(p.variant_id);
  else if (command === 'set_parameters') setParameters(p);
  else if (command === 'start' || command === 'fire_pulse') launch();
  else if (command === 'pause') pause();
  else if (command === 'step') step();
  else if (command === 'run_until') runUntil(p.time_s ?? p.time);
  else if (command === 'set_time') setTime(p.time_s ?? p.time);
  else if (command === 'reset') reset();
  else if (command === 'check') check();
  else if (command === 'record_measurement') recordMeasurement();
  else if (command === 'reveal_hint') hint();
}

// ── Dessin à la craie ────────────────────────────────────────────────────────
// Repère logique 760 × 380 centré dans le canvas ; les poignées A et B se saisissent sur la corde.
const canvas = $('canvas'), craie = new Craie(canvas, { onresize: redraw });
const L = 45, R = 710, geom = { s: 1, ox: 0, oy: 0 };
const toLogical = (x, y) => [(x - geom.ox) / geom.s, (y - geom.oy) / geom.s];
const xOf = m => L + (R - L) * m / 10;
function draw() {
  const W = craie.W, H = craie.H; if (W < 1 || H < 1) return true;
  const temps = scene();
  craie.debut(7, temps);
  const c = craie.ctx, s = Math.min(W / 760, H / 380); geom.s = s; geom.ox = (W - 760 * s) / 2; geom.oy = (H - 380 * s) / 2;
  c.translate(geom.ox, geom.oy); c.scale(s, s);
  const p = S.params, t = S.time, amp = 38 * p.amplitude;
  if (['cord', 'medium', 'progressive'].includes(S.variant)) {
    const v = S.variant === 'medium' ? speed(p.tension, p.density) : p.speed, centre = v * t, y = S.variant === 'progressive' ? 95 : 185;
    craie.fleche(170, y - 70, 420, y - 70, { couleur: 'vert', largeur: 2 }).texte('sens de propagation', 295, y - 80, { couleur: 'vert', taille: 17, align: 'center' });
    craie.ligne(L, y, R, y, { couleur: 'faible', largeur: 1.5 }).texte('S', L - 22, y + 6, { taille: 18 });
    craie.direct(() => {
      craie.courbe(u => [L + (R - L) * u, y - pulse(u * 10, centre) * amp], 180, { couleur: 'cyan', largeur: 2.6 });
      if (S.variant !== 'progressive') { const px = 4; craie.point(xOf(px), y - pulse(px, centre) * amp, 6, 'orange'); craie.ligne(xOf(px), y + 28, xOf(px), y - 65, { couleur: 'orange', largeur: 1, pointille: [4, 5] }); }
    });
    if (S.variant === 'progressive') {
      const a = arrivals(p), dates = S.trial ? arrivals(S.trial) : a;
      [[p.sensor1, 'A', 'cyan'], [p.sensor2, 'B', 'jaune']].forEach(([x, nom, col]) => {
        craie.rect(xOf(x) - 11, y - 34, 22, 68, { couleur: col, arrondi: 7, largeur: 2.2 }).texte(nom, xOf(x), y + 56, { couleur: col, taille: 19, align: 'center' });
      });
      craie.cote(xOf(p.sensor1), y + 66, xOf(p.sensor2), y + 66, `AB = ${fr(a.distance)} m`, { couleur: 'blanc', largeur: 1.6, taille: 17, dessous: true });
      const total = 10.7 / p.speed, gx = 95, gw = 560;
      [['yA', dates.a, 'cyan', 'a'], ['yB', dates.b, 'jaune', 'b']].forEach(([nom, arrivee, col, cle], i) => {
        const gy = 262 + i * 70;
        craie.axe(gx, gy, gx + gw + 30, gy, [0, 1, 2, 3, 4].map(j => [j / 4 * gw / (gw + 30), fr(j * total / 4, 2)]), { taille: 12 }).texte(nom, gx - 30, gy + 5, { couleur: col, taille: 16 }).texte('t (s)', gx + gw + 36, gy + 5, { couleur: 'faible', taille: 13 });
        craie.direct(() => { if (S.trial) craie.courbe(u => [gx + u * gw, gy - (u * total <= t ? pulse(S.trial.speed * u * total, S.trial.speed * arrivee) : 0) * 30], 160, { couleur: col, largeur: 2 }); });
        if (S.trial && t >= arrivee) {
          if (S.marques[cle] == null) S.marques[cle] = temps;
          craie.depuis(S.marques[cle]);
          craie.ligne(gx + arrivee / total * gw, gy, gx + arrivee / total * gw, gy - 36, { couleur: col, largeur: 1, pointille: [3, 4] });
          craie.texte(`t${nom[1]} = ${fr(arrivee, 2)} s`, gx + arrivee / total * gw + 8, gy - 30, { couleur: col, taille: 16 });
        }
      });
      if (S.trial && t >= dates.a) { craie.depuis(S.marques.a); craie.texte(`A : ${fr(dates.a, 2)} s`, xOf(p.sensor1), y - 44, { couleur: 'cyan', taille: 15, align: 'center' }); }
      if (S.trial && t >= dates.b) { craie.depuis(S.marques.b); craie.texte(`B : ${fr(dates.b, 2)} s`, xOf(p.sensor2), y - 44, { couleur: 'jaune', taille: 15, align: 'center' }); }
      if (S.marques.resultat != null && S.trial) {
        const tau = dates.b - dates.a; craie.depuis(S.marques.resultat);
        craie.texte(`τ = tB − tA = ${fr(tau, 2)} s`, 60, 214, { couleur: 'violet', taille: 18 }).pause(.2).texte(`v = AB / τ = ${fr(S.trial.sensor2 - S.trial.sensor1)} / ${fr(tau, 2)} = ${fr((S.trial.sensor2 - S.trial.sensor1) / tau, 1)} m·s⁻¹`, 330, 214, { couleur: 'violet', taille: 18, max: 380 });
      }
    } else {
      craie.texte('point matériel repéré', 285, 290, { couleur: 'orange', taille: 16 });
      craie.axe(L, 232, R + 20, 232, [0, 2, 4, 6, 8, 10].map(m => [(xOf(m) - L) / (R + 20 - L), String(m)]), { taille: 13 }).texte('x (m)', R + 20, 222, { couleur: 'faible', taille: 13, align: 'right' });
      craie.texte(S.variant === 'medium' ? `corde idéale : v = √(T/μ) = ${fr(v)} m·s⁻¹ ; l’amplitude ne change pas v` : 'le point orange monte puis redescend sur place ; la perturbation avance', R + 20, 352, { couleur: 'faible', taille: 15, align: 'right', max: 440 });
    }
  } else if (S.variant === 'spring' || S.variant === 'sound') {
    const sound = S.variant === 'sound', y = 185;
    const shift = x => sound ? .2 * p.amplitude * Math.sin(2 * Math.PI * (x / 2 - t)) : springPosition(x, 2 * t, p.amplitude) - x;
    craie.fleche(150, 60, 330, 60, { couleur: 'vert', largeur: 2 }).texte('sens de propagation', 240, 48, { couleur: 'vert', taille: 17, align: 'center' });
    craie.texte(sound ? 'membrane' : 'spires', 18, 110, { taille: 16 });
    craie.direct(() => {
      for (let row = 0; row < (sound ? 4 : 1); row++) for (let i = 0; i <= 75; i++) {
        const x = i / 75 * 10, xx = xOf(x + shift(x)), yy = sound ? 130 + row * 36 : y;
        if (sound) craie.point(xx, yy, 3, i === 30 ? 'orange' : 'bleu'); else craie.ligne(xx, yy - 40, xx, yy + 40, { couleur: i === 30 ? 'orange' : 'bleu', largeur: 2, tremble: .3 });
      }
      if (sound) craie.ligne(34 + 8 * Math.sin(2 * Math.PI * t), 110, 34 + 8 * Math.sin(2 * Math.PI * t), 250, { largeur: 6 });
    });
    craie.fleche(330, 300, 390, 300, { couleur: 'orange' }).fleche(390, 320, 330, 320, { couleur: 'orange' }).texte('mouvement local ↔', 360, 350, { couleur: 'orange', taille: 16, align: 'center' });
    craie.texte(sound ? 'zones resserrées : compressions ; zones espacées : dilatations' : 'chaque spire oscille autour de sa position de repos', R + 20, 372, { couleur: 'faible', taille: 15, align: 'right', max: 440 });
  } else if (S.variant === 'water') {
    const cx = 350, cy = 180;
    craie.texte('surface vue du dessus', 350, 350, { couleur: 'faible', taille: 16, align: 'center' });
    craie.point(cx, cy, 6, 'bleu').texte('S · impact', cx + 14, cy + 6, { taille: 16 });
    craie.fleche(cx, cy, cx + 150, cy, { couleur: 'vert' }).fleche(cx, cy, cx, cy - 120, { couleur: 'vert' });
    craie.direct(() => { for (let r = 0; r < 4; r++) { const radius = 70 * t - r * 28; if (radius > 0 && radius < 165) craie.cercle(cx, cy, radius, { couleur: 'cyan', largeur: 2.6 }); } });
  } else if (S.variant === 'vacuum') {
    craie.trait([[160, 300], [160, 160], [175, 60], [300, 32], [425, 60], [440, 160], [440, 300]], { couleur: 'bleu', largeur: 3 }).ligne(140, 304, 460, 304, { largeur: 6 });
    craie.texte('source vibrante', 300, 335, { taille: 16, align: 'center' }).texte('transmission par l’air', 480, 130, { taille: 16 });
    craie.rect(485, 150, 190, 25, { couleur: 'faible', arrondi: 4 });
    craie.direct(() => {
      for (let i = 0; i < Math.round(p.air * .6); i++) craie.point(185 + (i * 47 % 230), 100 + (i * 31 % 170), 2, 'cyan');
      const w = Math.sin(t * 15) * 4; craie.rect(265 + w, 175, 68, 65, { couleur: 'orange', arrondi: 6 });
      c.globalAlpha = .55; c.fillStyle = craie.couleur('cyan'); c.fillRect(487, 152, 186 * p.air / 100, 21); c.globalAlpha = 1;
    });
    craie.texte(p.air === 0 ? 'nulle dans ce modèle' : p.air < 50 ? 'affaiblie' : 'présente', 485, 205, { couleur: 'jaune', taille: 16 }).texte(`${p.air} % d’air`, 485, 240, { couleur: 'faible', taille: 15 });
    craie.texte('modèle qualitatif : la jauge n’est pas une mesure en décibels', R + 20, 372, { couleur: 'faible', taille: 14, align: 'right', max: 440 });
  } else if (S.variant === 'superposition') {
    const a = x => pulse(x, 2 * t, .85), b = x => pulse(x, 10 - 2 * t, .85 * p.sign);
    craie.texte('impulsion 1 →', 55, 32, { couleur: 'bleu', taille: 16 }).texte('← impulsion 2', 55, 127, { couleur: 'orange', taille: 16 }).texte('somme des déplacements', 55, 222, { couleur: 'vert', taille: 16 });
    [85, 180, 285].forEach(y => craie.ligne(L, y, R, y, { couleur: 'tresfaible', largeur: 1 }));
    craie.direct(() => {
      craie.courbe(u => [L + (R - L) * u, 85 - a(u * 10) * 38], 180, { couleur: 'bleu', largeur: 2.4 });
      craie.courbe(u => [L + (R - L) * u, 180 - b(u * 10) * 38], 180, { couleur: 'orange', largeur: 2.4 });
      craie.courbe(u => [L + (R - L) * u, 285 - (a(u * 10) + b(u * 10)) * 38], 180, { couleur: 'vert', largeur: 2.6 });
    });
    craie.texte('au croisement : double amplitude si mêmes signes, déplacement nul si signes opposés', R + 20, 362, { couleur: 'faible', taille: 14, align: 'right', max: 440 });
  }
  craie.direct(() => craie.texte(`t = ${fr(t)} s`, R + 20, 24, { couleur: 'jaune', taille: 17, align: 'right' }));
  return craie.fin();
}
glisser(canvas, {
  toucher: (x, y) => {
    if (S.variant !== 'progressive') return null; const [lx, ly] = toLogical(x, y);
    if (Math.abs(ly - 95) > 48) return null;
    if (Math.abs(lx - xOf(S.params.sensor1)) < 20) return 'sensor1'; if (Math.abs(lx - xOf(S.params.sensor2)) < 20) return 'sensor2'; return null;
  },
  bouger: (idx, x) => { const [lx] = toLogical(x, 0); const m = Math.round((lx - L) / (R - L) * 10 * 10) / 10; if (S.params[idx] !== m) setParameters({ [idx]: m }); },
});
$('onglets').addEventListener('click', e => { const b = e.target.closest('[data-variant]'); if (b) setVariant(b.dataset.variant); });
$('run').onclick = toggleRun; $('step').onclick = step; $('reset').onclick = () => reset(); $('check').onclick = check; $('hint').onclick = hint;
let previous = performance.now(), lastEmit = 0;
function frame(now) {
  const dt = Math.min(.1, (now - previous) / 1000); previous = now;
  if (S.running) {
    S.time = Math.min(duration(), S.time + dt); observe();
    if (S.stopAt !== null && S.time >= S.stopAt) { S.time = S.stopAt; S.stopAt = null; S.running = false; if (S.status !== 'finished') S.status = 'paused'; runLabel(); feedback(`Arrêt à t = ${fr(S.time)} s. Observe, puis reprends ou avance pas à pas.`); emit(); }
    else if (S.time >= duration()) { S.running = false; runLabel(); feedback(S.variant === 'progressive' ? 'Les deux dates sont écrites : calcule τ puis v, et vérifie.' : 'Observation terminée : réponds à la question.'); emit(); }
    if (S.running && now - lastEmit > 500) { lastEmit = now; emit(); }
    S.dirty = true;
  }
  if (S.dirty) { S.dirty = !draw(); $('clock').innerHTML = `t = <b>${fr(S.time)}</b> s`; }
  requestAnimationFrame(frame);
}
setVariant(initial); requestAnimationFrame(frame);
