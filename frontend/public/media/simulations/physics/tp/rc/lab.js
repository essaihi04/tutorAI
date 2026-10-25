// TP dipôle RC — laboratoire dessiné au tableau.
// Le modèle physique est dans model.js ; le dessin à la craie et le pont tuteur dans shared/tableau/tableau.js.
import {
  LIMITS, bounded, tau, chargeVoltage, dischargeVoltage, current, energy, tangentAtOrigin,
  reading, percentError, assessPrediction, assessTau, assessCapacitance, duration, niceStep,
} from './model.js';

const { Craie, fr, nombre, bulle, ecrire, curseur, protocole } = window.Tableau;
const $ = id => document.getElementById(id);
const id = 'physics_rc_tp_lab';
const RESISTANCES = [100, 220, 470, 1000, 2200, 4700, 10000];
const CAPACITANCES = [10, 47, 100, 220, 470, 1000];
const STEPS = ['Prédire', 'Monter', 'Mesurer', 'Lire τ', 'Calculer C', 'Décharge'];
const HINTS = [
  ['τ = R·C : que devient ce produit si R double et C ne change pas ?'],
  ['Choisis E, R et C, puis bascule K en position 1 (clique sur l’interrupteur) : le condensateur se charge.'],
  ['Relève au moins 8 points, jusqu’à environ 3τ : la courbe doit atteindre son palier.', 'L’acquisition automatique relève un point à intervalle régulier, comme une ExAO.'],
  ['Calcule 0,63 × E, puis clique sur la courbe à cette tension pour lire t.', 'Affiche la tangente à l’origine : elle coupe la droite u = E à t = τ.'],
  ['C = τ / R. τ en secondes, R en ohms : C sort en farads, à convertir en µF.'],
  ['Bascule K en position 2 : le condensateur se décharge dans R.', 'À t = τ, u_C vaut 0,37 × U₀.'],
];
const SIM_SECONDS_PER_REAL_SECOND = 1 / 8; // 5τ défilent en 8 s, quelle que soit la valeur de τ

const fresh = () => ({
  step: 0, done: new Set(), status: 'idle',
  params: { emf: 6, resistance: 1000, capacitance: 470 },
  switchPos: 2, mode: 'charge', t: 0, running: false, u0: 0, auto: false, nextAuto: 0,
  measurements: { charge: [], discharge: [] },
  show: { model: false, line: false, tangent: false }, shownAt: {}, cursor: null,
  answers: { prediction: null, tau63: null, tauTangent: null, capacitance: null, tauDischarge: null },
  validated: { tau63: false, tauTangent: false, capacitance: false, tauDischarge: false, predictionChecked: false },
  attempts: 0, hints: 0, hintIndex: 0,
  ouvert: performance.now(), dirty: true,
});
let S = fresh();
let runUntil = () => {}; // défini avec l'animation, plus bas

const tauS = () => tau(S.params.resistance, S.params.capacitance);
const span = () => duration(tauS());
const fmt = (v, d = 2) => fr(Number(v), d);
const fmtT = v => fmt(v, tauS() < 0.5 ? 3 : 2);
const exact = (t = S.t) => S.mode === 'charge' ? chargeVoltage(S.params.emf, tauS(), t) : dischargeVoltage(S.u0, tauS(), t);
const points = () => S.measurements[S.mode];
const scene = () => (performance.now() - S.ouvert) / 1000;
const redraw = () => { S.dirty = true; };

// ── Contrat tuteur ───────────────────────────────────────────────────────────
const commands = ['start', 'set_parameters', 'set_switch', 'record_measurement', 'auto_acquire', 'pause', 'run_until',
  'show_model', 'show_63', 'show_tangent', 'read_at', 'check', 'go_to_step', 'reveal_hint', 'reset'];
const config = {
  id, version: '2.0', title: 'TP — Charge et décharge d’un condensateur',
  variants: [{ id: 'tp_rc', label: 'TP dipôle RC', objective: 'Déterminer τ par deux méthodes, en déduire C, étudier la décharge.' }],
  commands,
  command_schema: {
    set_parameters: { emf_v: '2..12', resistance_ohm: RESISTANCES.join(' | '), capacitance_uf: CAPACITANCES.join(' | ') },
    set_switch: { position: '1 (charge) | 2 (décharge)' },
    read_at: { time_s: '0..5τ' },
    run_until: { time_s: '0..5τ (avance le temps puis met en pause)' },
    check: { field: 'prediction | tau63 | tauTangent | capacitance | tauDischarge', answer: 'nombre ou choix' },
    go_to_step: { step: '0..5' },
  },
};
const progress = () => S.done.size / STEPS.length;
function snapshot() {
  return {
    simulation_status: S.status, current_variant: 'tp_rc', step: S.step, step_label: STEPS[S.step],
    steps_done: [...S.done].map(i => STEPS[i]),
    parameters: { emf_v: S.params.emf, resistance_ohm: S.params.resistance, capacitance_uf: S.params.capacitance },
    switch_position: S.switchPos, mode: S.mode, time_s: +S.t.toFixed(4), tau_s: +tauS().toFixed(4),
    u_c_v: +exact().toFixed(3), measurements: S.measurements, student_answers: S.answers,
    validated: S.validated, attempts: S.attempts, hints_used: S.hints, objective_progress: progress(),
  };
}
const pont = protocole({ id, commandes: commands, config, etat: snapshot, progression: progress, executer,
  texte: 'TP en six étapes, dessiné au tableau : prédire l’effet de R sur τ, monter le circuit (E, R, C, K), relever u_C, lire τ par 63 % et par la tangente, calculer C et l’écart, étudier la décharge (37 %). L’interrupteur K se bascule en cliquant dessus sur le schéma. Les réponses sont saisies par l’élève et vérifiées à 5 %.' });
const log = (action, details = {}) => pont.noter(action, { ...details, step: S.step });
let lastEmit = 0;
function emit(force = false) {
  const now = Date.now();
  if (!force && now - lastEmit < 400) return;
  lastEmit = now; pont.emettre();
}

// ── Actions ─────────────────────────────────────────────────────────────────
function feedback(text, kind = '') { bulle($('feedback'), text, kind); }
function goTo(step) {
  if (S.step === 2 && step > 2 && measureReady()) complete(2);
  S.step = Math.max(0, Math.min(STEPS.length - 1, step)); S.hintIndex = 0; render(); emit(true);
}
function complete(step) { S.done.add(step); }

function setParameters(p) {
  const before = { ...S.params };
  if (p.emf_v !== undefined || p.emf !== undefined) S.params.emf = Math.round(bounded(Number(p.emf_v ?? p.emf), LIMITS.emf));
  const r = Number(p.resistance_ohm ?? p.resistance);
  if (RESISTANCES.includes(r)) S.params.resistance = r;
  const c = Number(p.capacitance_uf ?? p.capacitance);
  if (CAPACITANCES.includes(c)) S.params.capacitance = c;
  if (JSON.stringify(before) === JSON.stringify(S.params)) return;
  // Un nouveau montage annule les mesures : elles ne décrivent plus ce circuit.
  Object.assign(S, { running: false, t: 0, u0: 0, mode: 'charge', switchPos: 2, status: 'idle', cursor: null,
    measurements: { charge: [], discharge: [] }, show: { model: false, line: false, tangent: false }, shownAt: {},
    validated: { tau63: false, tauTangent: false, capacitance: false, tauDischarge: false, predictionChecked: S.validated.predictionChecked } });
  [2, 3, 4, 5].forEach(i => S.done.delete(i));
  log('set_parameters', { ...S.params });
  if (S.step > 1) S.step = 1;
  feedback('Nouveau montage : les mesures précédentes sont effacées.');
  render(); emit(true);
}

function setSwitch(position) {
  const pos = Number(position) === 1 ? 1 : 2;
  if (pos === S.switchPos) return;
  if (S.step < 1) { feedback('Commence par ta prédiction.', 'bad'); return; }
  if (pos === 1) {
    if (S.step > 2 && S.step < 5) { feedback('La charge est enregistrée. Pour l’étude de la décharge, termine d’abord les lectures.', 'bad'); return; }
    S.switchPos = 1; S.mode = 'charge'; S.t = 0; S.u0 = 0; S.running = true; S.status = 'running'; S.nextAuto = 0;
    S.measurements.charge = []; S.cursor = null;
    complete(1); if (S.step < 2) S.step = 2;
    log('set_switch', { position: 1 });
    feedback('K en position 1 : le condensateur se charge. Relève u_C pendant la charge.');
  } else {
    if (S.step < 5) {
      if (S.mode === 'charge' && S.t > 0) { S.switchPos = 2; S.running = false; S.status = 'paused'; render(); log('set_switch', { position: 2 }); feedback('K en position 2 : la charge est interrompue. Pour l’étude de la décharge, attends l’étape 6.'); emit(true); }
      return;
    }
    S.u0 = chargeVoltage(S.params.emf, tauS(), Math.max(S.t, span()));
    S.switchPos = 2; S.mode = 'discharge'; S.t = 0; S.running = true; S.status = 'running'; S.nextAuto = 0;
    S.measurements.discharge = []; S.cursor = null; S.show = { model: false, line: false, tangent: false }; S.shownAt = {};
    log('set_switch', { position: 2 });
    feedback(`K en position 2 : le condensateur se décharge dans R depuis U₀ = ${fmt(S.u0)} V.`);
  }
  render(); emit(true);
}

function record(manual = true) {
  if (!(S.t > 0) && S.mode === 'charge' && S.switchPos !== 1) { feedback('Bascule d’abord K en position 1.', 'bad'); return; }
  const list = points();
  const t = +S.t.toFixed(4);
  if (list.some(p => Math.abs(p.t - t) < 1e-6)) return;
  list.push({ t, u: reading(exact(t), t * 1000 + list.length) });
  list.sort((a, b) => a.t - b.t);
  if (manual) log('record_measurement', { t, mode: S.mode });
  renderPanel(); syncTools(); redraw(); emit();
}

function toggleShow(key, value) {
  S.show[key] = value ?? !S.show[key];
  if (S.show[key]) S.shownAt[key] = scene();
  log('show_' + key, { value: S.show[key] });
  syncTools(); redraw(); emit();
}

function readAt(t) {
  const tt = Math.max(0, Math.min(span(), Number(t)));
  if (!Number.isFinite(tt)) return;
  S.cursor = { t: tt, u: exact(tt) };
  $('cursor-reading').textContent = `t = ${fmtT(tt)} s · u_C = ${fmt(S.cursor.u)} V`;
  log('read_at', { t: +tt.toFixed(4) });
  redraw(); emit();
}

function check(field, answer) {
  S.attempts++;
  let result;
  if (field === 'prediction') {
    S.answers.prediction = answer;
    result = assessPrediction(answer);
    complete(0); feedback(result.reason, ''); log('check', { field, answer });
    goTo(1); return;
  }
  if (field === 'tau63' || field === 'tauTangent') {
    S.answers[field] = answer;
    result = assessTau(answer, tauS(), field === 'tauTangent' ? 'tangent' : 'percent');
    S.validated[field] = result.correct;
    if (S.validated.tau63 && S.validated.tauTangent) complete(3);
  } else if (field === 'capacitance') {
    S.answers.capacitance = answer;
    const measuredTau = Number(String(S.answers.tau63 ?? '').replace(',', '.')) || tauS();
    result = assessCapacitance(answer, measuredTau, S.params.resistance, S.params.capacitance);
    S.validated.capacitance = result.correct;
    if (result.correct) complete(4);
  } else if (field === 'tauDischarge') {
    S.answers.tauDischarge = answer;
    result = assessTau(answer, tauS(), 'discharge');
    S.validated.tauDischarge = result.correct;
    if (result.correct) { complete(5); S.status = 'finished'; }
  } else return;
  log('check', { field, answer, correct: result.correct });
  feedback(result.reason, result.correct ? 'good' : 'bad');
  renderPanel(); renderSteps(); emit(true);
}

function confrontPrediction() {
  const t1 = tauS(), t2 = tau(S.params.resistance * 2, S.params.capacitance);
  S.validated.predictionChecked = true;
  log('confront_prediction', { tau_s: t1, tau_double_r_s: t2 });
  const said = { double: 'que τ double', half: 'que τ diminue de moitié', same: 'que τ ne change pas' }[S.answers.prediction] ?? 'rien';
  feedback(`Avec R = ${S.params.resistance * 2} Ω, le modèle donne τ = ${fmtT(t2)} s, soit ${fmt(t2 / t1, 1)} fois plus. Tu avais prédit ${said}.`, S.answers.prediction === 'double' ? 'good' : 'bad');
  renderPanel(); emit(true);
}

function hint() {
  const list = HINTS[S.step];
  const text = list[Math.min(S.hintIndex, list.length - 1)];
  S.hintIndex++; S.hints++;
  log('reveal_hint', { step: S.step });
  feedback('Indice : ' + text);
  emit(true);
}

function reset() { S = fresh(); log('reset'); feedback('Nouveau TP. Commence par prédire.'); render(); emit(true); }

function executer(command, p = {}) {
  switch (command) {
    case 'start': if (S.step === 0) goTo(1); else if (!S.running && S.t < span() && S.t > 0) { S.running = true; S.status = 'running'; render(); } break;
    case 'pause': S.running = false; if (S.status !== 'finished') S.status = 'paused'; render(); emit(true); break;
    case 'set_parameters': setParameters(p); break;
    case 'set_switch': setSwitch(p.position ?? (S.switchPos === 1 ? 2 : 1)); break;
    case 'record_measurement': record(); break;
    case 'auto_acquire': S.auto = p.enabled ?? !S.auto; log('auto_acquire', { enabled: S.auto }); renderPanel(); emit(true); break;
    case 'show_model': toggleShow('model', p.enabled); break;
    case 'show_63': toggleShow('line', p.enabled); break;
    case 'show_tangent': toggleShow('tangent', p.enabled); break;
    case 'read_at': readAt(p.time_s); break;
    case 'run_until': runUntil(p.time_s); break;
    case 'check': check(p.field, p.answer); break;
    case 'go_to_step': goTo(Number(p.step)); break;
    case 'reveal_hint': hint(); break;
    case 'reset': reset(); break;
  }
}

// ── Panneau d'étapes (à droite, écrit à la craie) ────────────────────────────
function renderSteps() {
  $('steps').innerHTML = STEPS.map((label, i) =>
    `<li data-state="${S.done.has(i) ? 'done' : i === S.step ? 'current' : 'todo'}">${label}</li>`).join('');
}
function table(list) {
  if (!list.length) return '<p class="hint-text">Aucun point relevé.</p>';
  return `<div class="table-wrap"><table class="lecture-table"><thead><tr><th>n°</th><th>t (s)</th><th>u_C (V)</th></tr></thead><tbody>${
    list.map((p, i) => `<tr><td>${i + 1}</td><td>${fmtT(p.t)}</td><td>${fmt(p.u)}</td></tr>`).join('')}</tbody></table></div>`;
}
function field(key, label, unit) {
  const ok = S.validated[key];
  return `<div class="champ-ligne"><label class="craie-champ" for="f-${key}">${label} <input id="f-${key}" inputmode="decimal" autocomplete="off" value="${S.answers[key] ?? ''}" ${ok ? 'disabled' : ''}> ${unit}</label>
    <button class="craie-btn ${ok ? 'principal' : 'attention'}" data-check="${key}" data-professor-control="check" ${ok ? 'disabled' : ''}>${ok ? 'Validé ✓' : 'Vérifier'}</button></div>`;
}
function measureReady() {
  const list = S.measurements.charge;
  return list.length >= 8 && list[list.length - 1].t >= 3 * tauS();
}
function renderPanel() {
  const p = S.params;
  const panels = [
    () => `<h2>1. Prédire</h2><p class="question">On double la résistance R, sans changer C. La durée caractéristique de la charge τ…</p>
      <div class="choix-btn">${[['double', 'double'], ['half', 'est divisée par deux'], ['same', 'ne change pas']]
        .map(([v, l]) => `<button class="craie-btn" data-predict="${v}" data-professor-control="check">${l}</button>`).join('')}</div>
      <p>Pas de note ici : la mesure tranchera.</p>`,
    () => `<h2>2. Monter le circuit</h2><p>Règle le générateur et choisis les composants, puis <b>clique sur K</b> pour le mettre en position 1.</p><div id="reglages"></div>`,
    () => `<h2>3. Mesurer u_C</h2><p>Le voltmètre lit u_C. Relève des points pendant la charge.</p>
      <div class="actions"><button class="craie-btn principal" id="record-btn" data-professor-control="record_measurement" ${S.switchPos === 1 || S.t > 0 ? '' : 'disabled'}>Relever u_C</button>
      <button class="craie-btn secondaire" id="auto-btn" aria-pressed="${S.auto}" data-professor-control="auto_acquire">Acquisition auto</button>
      <button class="craie-btn secondaire" id="run-btn" data-professor-control="start pause">${S.running ? 'Pause' : 'Reprendre'}</button></div>
      ${table(S.measurements.charge)}
      <p class="legende">${S.measurements.charge.length} point(s). Il en faut au moins 8, jusqu’au palier.</p>
      <button class="craie-btn attention suite" id="next-btn" data-professor-control="go_to_step" ${measureReady() ? '' : 'disabled'}>Exploiter la courbe →</button>`,
    () => `<h2>4. Lire τ sur la courbe</h2><p>E = ${p.emf} V. Utilise les outils sous la courbe et clique dessus pour lire.</p>
      <p class="formule">u_C(τ) = 0,63 × E</p>
      ${field('tau63', 'τ (63 %) =', 's')}
      ${field('tauTangent', 'τ (tangente) =', 's')}
      <button class="craie-btn attention suite" id="next-btn" data-professor-control="go_to_step" ${S.done.has(3) ? '' : 'disabled'}>Calculer C →</button>`,
    () => `<h2>5. Calculer C</h2><p>R = ${p.resistance} Ω. Valeur nominale indiquée sur le condensateur : ${p.capacitance} µF.</p>
      <p class="formule">τ = R · C  ⇒  C = τ / R</p>
      ${field('capacitance', 'C =', 'µF')}
      ${S.validated.capacitance ? `<p>Retour à ta prédiction : que donnerait R doublé ?</p><button class="craie-btn secondaire" id="confront-btn" data-professor-control="check">Confronter ma prédiction</button>` : ''}
      <button class="craie-btn attention suite" id="next-btn" data-professor-control="go_to_step" ${S.done.has(4) ? '' : 'disabled'}>Étudier la décharge →</button>`,
    () => `<h2>6. La décharge</h2>${S.mode === 'charge'
        ? `<p>Le condensateur est chargé. <b>Clique sur K</b> pour le mettre en position 2 : il se décharge dans R.</p>`
        : `<p>U₀ = ${fmt(S.u0)} V.</p><p class="formule">u_C(τ) = 0,37 × U₀</p>
      <div class="actions"><button class="craie-btn principal" id="record-btn" data-professor-control="record_measurement">Relever u_C</button><button class="craie-btn secondaire" id="auto-btn" aria-pressed="${S.auto}" data-professor-control="auto_acquire">Acquisition auto</button></div>
      ${table(S.measurements.discharge)}
      ${field('tauDischarge', 'τ (décharge) =', 's')}
      ${S.status === 'finished' ? `<p><b>TP terminé.</b> Énergie stockée au départ : ½·C·U₀² = ${fmt(energy(p.capacitance, S.u0), 1)} mJ.</p>` : ''}`}`,
  ];
  $('panel').innerHTML = panels[S.step]();
  if (S.step === 1) {
    const box = $('reglages');
    const add = (key, label, min, max, step, valeur, unite, lire, decimales) => {
      const el = curseur({ id: key, label, min, max, step, valeur, unite, decimales, onchange: v => setParameters({ [key]: lire(v) }) });
      el.dataset.professorControl = 'set_parameters';
      if (lire !== Number) { el.querySelector('b').textContent = `${lire(valeur)} ${unite}`; el.input.addEventListener('input', () => { el.querySelector('b').textContent = `${lire(Number(el.input.value))} ${unite}`; }); }
      box.append(el);
    };
    add('emf_v', 'Tension E', LIMITS.emf[0], LIMITS.emf[1], 1, p.emf, 'V', Number, 0);
    add('resistance_ohm', 'Résistance R', 0, RESISTANCES.length - 1, 1, RESISTANCES.indexOf(p.resistance), 'Ω', v => RESISTANCES[v], 0);
    add('capacitance_uf', 'Capacité C', 0, CAPACITANCES.length - 1, 1, CAPACITANCES.indexOf(p.capacitance), 'µF', v => CAPACITANCES[v], 0);
  }
  bindPanel();
  // Le titre de l'étape s'écrit à la craie une seule fois, quand on arrive à l'étape.
  const h2 = $('panel').querySelector('h2');
  if (h2 && renderPanel.ecrit !== S.step + ':' + S.mode) { renderPanel.ecrit = S.step + ':' + S.mode; ecrire(h2, h2.textContent, { vitesse: 40 }); }
}
function bindPanel() {
  $('panel').querySelectorAll('[data-predict]').forEach(b => b.onclick = () => check('prediction', b.dataset.predict));
  $('panel').querySelectorAll('[data-check]').forEach(b => b.onclick = () => check(b.dataset.check, $('f-' + b.dataset.check).value));
  $('panel').querySelectorAll('.craie-champ input').forEach(input => input.onkeydown = e => { if (e.key === 'Enter') check(input.id.slice(2), input.value); });
  const on = (elId, fn) => { const el = $(elId); if (el) el.onclick = fn; };
  on('record-btn', () => record());
  on('auto-btn', () => window.executeAICommand('auto_acquire'));
  on('run-btn', () => window.executeAICommand(S.running ? 'pause' : 'start'));
  on('next-btn', () => { complete(S.step === 2 ? 2 : S.step); goTo(S.step + 1); });
  on('confront-btn', confrontPrediction);
}
function syncTools() {
  const discharge = S.mode === 'discharge';
  $('show-63').textContent = discharge ? 'Ligne 0,37 U₀' : 'Ligne 0,63 E';
  [['show-model', 'model'], ['show-63', 'line'], ['show-tangent', 'tangent']].forEach(([el, key]) => {
    $(el).setAttribute('aria-pressed', String(S.show[key]));
    $(el).disabled = points().length < 2;
  });
}
function render() { renderSteps(); renderPanel(); syncTools(); redraw(); }

// ── Dessin à la craie : circuit (en haut) et courbe u_C(t) (en bas) ──────────
const canvas = $('board');
let craie = null;
craie = new Craie(canvas, { onresize: () => { if (!craie) return; redraw(); placeSwitch(); } });
// Repère logique du circuit : 420 × 210, placé dans la bande haute du canvas.
const geom = { s: 1, ox: 0, oy: 0, graph: { l: 0, r: 0, t: 0, b: 0 } };
const LOOPS = {
  charge: [[60, 85], [60, 40], [260, 40], [370, 40], [370, 170], [60, 170], [60, 85]],
  discharge: [[370, 90], [370, 40], [150, 40], [150, 170], [370, 170], [370, 90]],
};
function layout() {
  const W = craie.W, H = craie.H, hCircuit = Math.min(H * .42, W * 210 / 420 * .9);
  geom.s = Math.min((W - 10) / 420, hCircuit / 210); geom.ox = (W - 420 * geom.s) / 2; geom.oy = 4;
  const top = geom.oy + 210 * geom.s + 6;
  geom.graph = { l: 54, r: W - 16, t: top + 18, b: H - 34 };
}
function placeSwitch() {
  layout();
  const z = $('switch'); z.style.left = `${geom.ox + 128 * geom.s}px`; z.style.top = `${geom.oy + 16 * geom.s}px`;
  z.style.width = `${98 * geom.s}px`; z.style.height = `${86 * geom.s}px`;
}
function pathPoint(loop, dist) {
  let total = 0; const segs = [];
  for (let i = 0; i < loop.length - 1; i++) { const l = Math.hypot(loop[i + 1][0] - loop[i][0], loop[i + 1][1] - loop[i][1]); segs.push(l); total += l; }
  let d = ((dist % total) + total) % total;
  for (let i = 0; i < segs.length; i++) {
    if (d <= segs[i]) { const f = segs[i] ? d / segs[i] : 0; return [loop[i][0] + (loop[i + 1][0] - loop[i][0]) * f, loop[i][1] + (loop[i + 1][1] - loop[i][1]) * f, total]; }
    d -= segs[i];
  }
  return [loop[0][0], loop[0][1], total];
}
let electronOffset = 0;
function gx(t) { const g = geom.graph; return g.l + t / span() * (g.r - g.l); }
function gy(u, uMax) { const g = geom.graph; return g.b - u / uMax * (g.b - g.t); }
function uMaxOf() { return S.mode === 'charge' ? S.params.emf * 1.12 : Math.max(S.u0, 1) * 1.12; }

function draw() {
  const W = craie.W, H = craie.H; if (W < 1 || H < 1) return true;
  layout();
  const temps = scene();
  craie.debut(11, temps);
  const c = craie.ctx;
  // — Circuit —
  c.save(); c.translate(geom.ox, geom.oy); c.scale(geom.s, geom.s);
  const sw = { largeur: 2.3 / Math.sqrt(geom.s) * .9 };
  craie.trait([[60, 85], [60, 40], [146, 40]], sw).trait([[214, 40], [260, 40]], sw).trait([[320, 40], [370, 40], [370, 90]], sw).trait([[370, 120], [370, 170], [60, 170], [60, 125]], sw);
  craie.ligne(150, 94, 150, 170, { ...sw, pointille: [4, 4], couleur: 'faible' });
  craie.ligne(44, 85, 76, 85, { largeur: 3 }).ligne(50, 125, 70, 125, { largeur: 6 });
  craie.texte(`E = ${S.params.emf} V`, 6, 112, { taille: 15, couleur: 'jaune' });
  craie.point(150, 40, 3.5).point(150, 90, 3.5).point(210, 40, 3.5);
  craie.texte('K', 168, 24, { taille: 15 }).texte('1', 134, 32, { taille: 12, couleur: 'faible' }).texte('2', 132, 100, { taille: 12, couleur: 'faible' });
  craie.rect(260, 30, 60, 20, { arrondi: 3 }).texte('R', 283, 22, { taille: 15 });
  craie.ligne(352, 90, 388, 90, { largeur: 4 }).ligne(352, 120, 388, 120, { largeur: 4 }).texte('C', 394, 110, { taille: 15 });
  craie.cercle(300, 105, 20, { couleur: 'cyan' }).texte('V', 300, 111, { taille: 15, align: 'center', couleur: 'cyan' });
  craie.trait([[300, 85], [300, 66], [370, 66]], { couleur: 'cyan', largeur: 1.4, pointille: [3, 3] }).trait([[300, 125], [300, 150], [370, 150]], { couleur: 'cyan', largeur: 1.4, pointille: [3, 3] });
  craie.direct(() => {
    const bx = S.switchPos === 1 ? 155 : 154, by = S.switchPos === 1 ? 42 : 86;
    craie.ligne(210, 40, bx, by, { couleur: 'jaune', largeur: 3.2 });
    craie.texte(`u_C = ${fmt(exact())} V`, 250, 200, { taille: 15, couleur: 'jaune', align: 'center' });
    const i = Math.abs(current(S.mode, S.mode === 'charge' ? S.params.emf : S.u0, S.params.resistance, tauS(), S.t));
    const i0 = S.params.emf / S.params.resistance * 1000;
    if ((S.running || S.t > 0) && i / i0 > 0.01 && S.t < span()) {
      const loop = LOOPS[S.mode], [, , total] = pathPoint(loop, 0);
      const [ex, ey] = pathPoint(loop, S.mode === 'charge' ? electronOffset : total - electronOffset);
      craie.point(ex, ey, 4, 'cyan');
    }
  });
  c.restore();
  // — Courbe u_C(t) —
  const g = geom.graph, T = span(), tauV = tauS(), uMax = uMaxOf();
  const stepT = niceStep(T, 8), decimals = Math.max(0, -Math.floor(Math.log10(stepT)));
  const gradT = []; for (let t = 0; t <= T + 1e-9; t += stepT) gradT.push([t / T * (g.r - g.l) / (g.r - g.l + 14), fmt(t, decimals)]);
  const stepU = uMax > 8 ? 2 : 1, gradU = []; for (let u = 0; u <= uMax; u += stepU) gradU.push([u / uMax * (g.b - g.t) / (g.b - g.t + 14), fmt(u, 0)]);
  craie.axe(g.l, g.b, g.r + 14, g.b, gradT, { taille: 12 }).texte('t (s)', g.r + 14, g.b - 8, { taille: 12, couleur: 'faible', align: 'right' });
  craie.axe(g.l, g.b, g.l, g.t - 14, gradU, { taille: 12, vertical: true }).texte('u_C (V)', g.l + 6, g.t - 4, { taille: 12, couleur: 'faible' });
  const top = S.mode === 'charge' ? S.params.emf : S.u0;
  if (S.show.model) {
    craie.depuis(S.shownAt.model);
    craie.courbe(u => [gx(u * T), gy(exact(u * T), uMax)], 120, { couleur: 'cyan', largeur: 2.2 });
  }
  if (S.show.line) {
    const level = S.mode === 'charge' ? 0.63 * top : 0.37 * top; craie.depuis(S.shownAt.line);
    craie.ligne(g.l, gy(level, uMax), g.r, gy(level, uMax), { couleur: 'jaune', largeur: 1.4, pointille: [5, 4] });
    craie.texte(S.mode === 'charge' ? '0,63 E' : '0,37 U₀', g.r - 4, gy(level, uMax) - 5, { taille: 14, couleur: 'jaune', align: 'right' });
  }
  if (S.show.tangent) {
    craie.depuis(S.shownAt.tangent);
    if (S.mode === 'charge') { const te = Math.min(T, tauV * 1.15); craie.ligne(gx(0), gy(0, uMax), gx(te), gy(tangentAtOrigin(top, tauV, te), uMax), { couleur: 'violet', largeur: 1.6 }); }
    else craie.ligne(gx(0), gy(top, uMax), gx(tauV), gy(0, uMax), { couleur: 'violet', largeur: 1.6 });
    const asym = S.mode === 'charge' ? top : 0;
    craie.ligne(g.l, gy(asym, uMax), g.r, gy(asym, uMax), { couleur: 'violet', largeur: 1.2, pointille: [3, 3] });
    craie.texte(S.mode === 'charge' ? 'u = E' : 'u = 0', g.r - 4, gy(asym, uMax) - 5, { taille: 14, couleur: 'violet', align: 'right' });
  }
  craie.direct(() => {
    for (const p of points()) craie.point(gx(p.t), gy(p.u, uMax), 3.4, 'orange');
    if (S.running || S.t > 0) craie.point(gx(S.t), gy(exact(), uMax), 3.2, 'vert');
    if (S.cursor) {
      craie.trait([[gx(S.cursor.t), g.b], [gx(S.cursor.t), gy(S.cursor.u, uMax)], [g.l, gy(S.cursor.u, uMax)]], { couleur: 'jaune', largeur: 1, pointille: [2, 3], tremble: 0 });
    }
  });
  return craie.fin();
}

// Clic sur la courbe : lecture d'un point ; sur K : bascule (zone HTML visible pour le professeur).
canvas.addEventListener('click', event => {
  const rect = canvas.getBoundingClientRect(), x = event.clientX - rect.left, y = event.clientY - rect.top, g = geom.graph;
  if (y < g.t - 14) return;
  if (points().length < 2) { $('cursor-reading').textContent = 'Relève d’abord des points.'; return; }
  readAt((x - g.l) / (g.r - g.l) * span());
});
canvas.addEventListener('mousemove', event => { const rect = canvas.getBoundingClientRect(); canvas.style.cursor = event.clientY - rect.top >= geom.graph.t - 14 ? 'crosshair' : ''; });
$('switch').addEventListener('click', () => setSwitch(S.switchPos === 1 ? 2 : 1));
$('switch').addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); setSwitch(S.switchPos === 1 ? 2 : 1); } });
$('show-model').onclick = () => toggleShow('model');
$('show-63').onclick = () => toggleShow('line');
$('show-tangent').onclick = () => toggleShow('tangent');
$('hint').onclick = hint;
$('reset').onclick = reset;

// ── Animation ────────────────────────────────────────────────────────────────
/** Fait avancer le temps simulé, relève les points automatiques au passage. */
function advanceTo(target) {
  S.t = Math.min(span(), Math.max(S.t, target));
  if (S.auto) while (S.nextAuto <= S.t + 1e-9 && S.nextAuto <= span()) {
    const keep = S.t; S.t = S.nextAuto; record(false); S.t = keep; S.nextAuto = +(S.nextAuto + niceStep(span(), 20)).toFixed(6);
  }
  if (S.t >= span()) { S.running = false; S.status = 'paused'; feedback(S.mode === 'charge' ? 'Le condensateur est chargé : u_C ≈ E. Le courant est nul.' : 'Le condensateur est déchargé.'); renderPanel(); emit(true); }
  redraw(); emit();
}
runUntil = target => {
  if (!(S.switchPos === 1 || S.mode === 'discharge')) return;
  advanceTo(Number(target));
  if (S.t < span()) { S.running = false; S.status = 'paused'; renderPanel(); }
  emit(true);
};
let last = performance.now();
function tick(now) {
  const dt = Math.min(0.05, (now - last) / 1000); last = now;
  if (S.running) advanceTo(S.t + dt * span() * SIM_SECONDS_PER_REAL_SECOND);
  const i = Math.abs(current(S.mode, S.mode === 'charge' ? S.params.emf : S.u0, S.params.resistance, tauS(), S.t));
  const i0 = S.params.emf / S.params.resistance * 1000;
  if ((S.running || S.t > 0) && i / i0 > 0.01 && S.t < span()) { electronOffset += dt * 160 * (i / i0); S.dirty = true; }
  if (S.dirty) { S.dirty = !draw(); $('clock').innerHTML = `t = <b>${fmtT(S.t)}</b> s`; }
  requestAnimationFrame(tick);
}

feedback('Commence par prédire : la mesure tranchera.');
placeSwitch(); render(); emit(true);
requestAnimationFrame(tick);
