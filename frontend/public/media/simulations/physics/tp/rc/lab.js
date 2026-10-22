import {
  LIMITS, bounded, tau, chargeVoltage, dischargeVoltage, current, energy, tangentAtOrigin,
  reading, percentError, assessPrediction, assessTau, assessCapacitance, duration, niceStep,
} from './model.js';

const $ = id => document.getElementById(id);
const id = 'physics_rc_tp_lab';
const RESISTANCES = [100, 220, 470, 1000, 2200, 4700, 10000];
const CAPACITANCES = [10, 47, 100, 220, 470, 1000];
const STEPS = ['Prédire', 'Monter', 'Mesurer', 'Lire τ', 'Calculer C', 'Décharge'];
const HINTS = [
  ['τ = R·C : que devient ce produit si R double et C ne change pas ?'],
  ['Choisis E, R et C, puis bascule K en position 1 : le condensateur se charge.'],
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
  show: { model: false, line: false, tangent: false }, cursor: null,
  answers: { prediction: null, tau63: null, tauTangent: null, capacitance: null, tauDischarge: null },
  validated: { tau63: false, tauTangent: false, capacitance: false, tauDischarge: false, predictionChecked: false },
  attempts: 0, hints: 0, hintIndex: 0, actions: [],
});
let S = fresh();
let runUntil = () => {}; // défini avec l'animation, plus bas

const tauS = () => tau(S.params.resistance, S.params.capacitance);
const span = () => duration(tauS());
const fmt = (v, d = 2) => Number(v).toLocaleString('fr-FR', { minimumFractionDigits: d, maximumFractionDigits: d });
const fmtT = v => fmt(v, tauS() < 0.5 ? 3 : 2);
const exact = (t = S.t) => S.mode === 'charge' ? chargeVoltage(S.params.emf, tauS(), t) : dischargeVoltage(S.u0, tauS(), t);
const points = () => S.measurements[S.mode];

function log(action, details = {}) {
  S.actions.push({ action, details, step: S.step, timestamp: Date.now() });
  S.actions = S.actions.slice(-80);
}

// ── Contrat tuteur ───────────────────────────────────────────────────────────
const commands = ['start', 'set_parameters', 'set_switch', 'record_measurement', 'auto_acquire', 'pause', 'run_until',
  'show_model', 'show_63', 'show_tangent', 'read_at', 'check', 'go_to_step', 'reveal_hint', 'reset'];
window.SIMULATION_CONFIG = {
  id, version: '1.0', title: 'TP — Charge et décharge d’un condensateur',
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
const progress = () => S.done.size / STEPS.length;
let lastEmit = 0;
function emit(force = false) {
  const now = Date.now();
  if (!force && now - lastEmit < 400) return;
  lastEmit = now;
  parent.postMessage({ type: 'simulation_state', simulation_id: id, current_state: snapshot(), student_actions: S.actions, objective_progress: progress(), timestamp: now }, '*');
}
function manifest() {
  window.__SIMULATION_MANIFEST_SENT__ = true; // évite le manifeste de secours de MediaViewer
  parent.postMessage({ type: 'simulation_manifest', simulation_id: id,
    capabilities: { commands, config: window.SIMULATION_CONFIG, globals: ['executeAICommand'], command_schema: window.SIMULATION_CONFIG.command_schema },
    page_text: 'TP en six étapes : prédire l’effet de R sur τ, monter le circuit, relever u_C, lire τ par 63 % et par la tangente, calculer C et l’écart, étudier la décharge (37 %). Les réponses sont saisies par l’élève et vérifiées à 5 %.' }, '*');
}

// ── Actions ─────────────────────────────────────────────────────────────────
function feedback(text, kind = '') { $('feedback').textContent = text; $('feedback').dataset.kind = kind; }
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
    measurements: { charge: [], discharge: [] },
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
    S.measurements.discharge = []; S.cursor = null; S.show = { model: false, line: false, tangent: false };
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
  renderPanel(); syncTools(); drawGraph(); emit();
}

function toggleShow(key, value) {
  S.show[key] = value ?? !S.show[key];
  log('show_' + key, { value: S.show[key] });
  syncTools(); drawGraph(); emit();
}

function readAt(t) {
  const tt = Math.max(0, Math.min(span(), Number(t)));
  if (!Number.isFinite(tt)) return;
  S.cursor = { t: tt, u: exact(tt) };
  $('cursor-reading').textContent = `t = ${fmtT(tt)} s · u_C = ${fmt(S.cursor.u)} V`;
  log('read_at', { t: +tt.toFixed(4) });
  drawGraph(); emit();
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

window.executeAICommand = (command, p = {}) => {
  switch (command) {
    case 'start': if (S.step === 0) goTo(1); else if (!S.running && S.t < span() && S.t > 0) { S.running = true; S.status = 'running'; render(); } break;
    case 'pause': S.running = false; if (S.status !== 'finished') S.status = 'paused'; render(); emit(true); break;
    case 'set_parameters': setParameters(p); break;
    case 'set_switch': setSwitch(p.position); break;
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
    default: return { ok: false, error: 'Commande inconnue' };
  }
  return { ok: true, state: snapshot() };
};
window.addEventListener('message', event => {
  if (event.source !== parent || event.data?.type !== 'simulation_control') return;
  if (event.data.simulation_id && event.data.simulation_id !== id) return;
  window.executeAICommand(event.data.command, event.data.parameters || {});
});

// ── Rendu ────────────────────────────────────────────────────────────────────
function renderSteps() {
  $('steps').innerHTML = STEPS.map((label, i) =>
    `<li data-state="${S.done.has(i) ? 'done' : i === S.step ? 'current' : 'todo'}">${label}</li>`).join('');
}

function table(list) {
  if (!list.length) return '<p class="hint-text">Aucun point relevé.</p>';
  return `<div class="table-wrap"><table><thead><tr><th>n°</th><th>t (s)</th><th>u_C (V)</th></tr></thead><tbody>${
    list.map((p, i) => `<tr><td>${i + 1}</td><td>${fmtT(p.t)}</td><td>${fmt(p.u)}</td></tr>`).join('')}</tbody></table></div>`;
}

function field(key, label, unit) {
  const ok = S.validated[key];
  return `<div class="field"><label for="f-${key}">${label}</label><input id="f-${key}" inputmode="decimal" value="${S.answers[key] ?? ''}" ${ok ? 'disabled' : ''}><span>${unit}</span>
    <button data-check="${key}" data-professor-control="check" ${ok ? 'disabled' : ''}>${ok ? 'Validé ✓' : 'Vérifier'}</button></div>`;
}

function measureReady() {
  const list = S.measurements.charge;
  return list.length >= 8 && list[list.length - 1].t >= 3 * tauS();
}

function renderPanel() {
  const p = S.params;
  const panels = [
    () => `<h2>1. Prédire</h2><p class="question">On double la résistance R, sans changer C. La durée caractéristique de la charge τ…</p>
      <div class="choices">${[['double', 'double'], ['half', 'est divisée par deux'], ['same', 'ne change pas']]
        .map(([v, l]) => `<button data-predict="${v}" data-professor-control="check">${l}</button>`).join('')}</div>
      <p>Pas de note ici : la mesure tranchera.</p>`,
    () => `<h2>2. Monter le circuit</h2><p>Règle le générateur et choisis les composants.</p>
      <label class="control"><span>Tension E <b>${p.emf} V</b></span><input type="range" min="${LIMITS.emf[0]}" max="${LIMITS.emf[1]}" step="1" value="${p.emf}" data-param="emf_v" data-professor-control="set_parameters"></label>
      <label class="control"><span>Résistance R <b>${p.resistance} Ω</b></span><input type="range" min="0" max="${RESISTANCES.length - 1}" step="1" value="${RESISTANCES.indexOf(p.resistance)}" data-param="resistance_ohm" data-professor-control="set_parameters"></label>
      <label class="control"><span>Capacité C <b>${p.capacitance} µF</b></span><input type="range" min="0" max="${CAPACITANCES.length - 1}" step="1" value="${CAPACITANCES.indexOf(p.capacitance)}" data-param="capacitance_uf" data-professor-control="set_parameters"></label>
      <p>Puis <b>bascule K en position 1</b> (clique sur l’interrupteur) pour lancer la charge.</p>
      <button class="primary" data-switch="1" data-professor-control="set_switch">K → position 1</button>`,
    () => `<h2>3. Mesurer u_C</h2><p>Le voltmètre lit u_C. Relève des points pendant la charge.</p>
      <div class="actions"><button class="primary" id="record-btn" data-professor-control="record_measurement" ${S.switchPos === 1 || S.t > 0 ? '' : 'disabled'}>Relever u_C</button>
      <button id="auto-btn" aria-pressed="${S.auto}" data-professor-control="auto_acquire">Acquisition automatique</button>
      <button id="run-btn" data-professor-control="start pause">${S.running ? 'Pause' : 'Reprendre'}</button></div>
      ${table(S.measurements.charge)}
      <p>${S.measurements.charge.length} point(s). Il en faut au moins 8, jusqu’au palier.</p>
      <button class="primary" id="next-btn" data-professor-control="go_to_step" ${measureReady() ? '' : 'disabled'}>Exploiter la courbe →</button>`,
    () => `<h2>4. Lire τ sur la courbe</h2><p>E = ${p.emf} V. Utilise les outils sous la courbe et clique dessus pour lire.</p>
      <p class="formula">u_C(τ) = 0,63 × E</p>
      ${field('tau63', 'τ par la méthode des 63 % :', 's')}
      ${field('tauTangent', 'τ par la tangente à l’origine :', 's')}
      <button class="primary" id="next-btn" data-professor-control="go_to_step" ${S.done.has(3) ? '' : 'disabled'}>Calculer C →</button>`,
    () => `<h2>5. Calculer C</h2><p>R = ${p.resistance} Ω. Valeur nominale indiquée sur le condensateur : ${p.capacitance} µF.</p>
      <p class="formula">τ = R · C  ⇒  C = τ / R</p>
      ${field('capacitance', 'C =', 'µF')}
      ${S.validated.capacitance ? `<p>Retour à ta prédiction : que donnerait R doublé ?</p><button id="confront-btn" data-professor-control="check">Confronter ma prédiction</button>` : ''}
      <button class="primary" id="next-btn" data-professor-control="go_to_step" ${S.done.has(4) ? '' : 'disabled'}>Étudier la décharge →</button>`,
    () => `<h2>6. La décharge</h2>${S.mode === 'charge'
        ? `<p>Le condensateur est chargé. <b>Bascule K en position 2</b> : il se décharge dans R.</p><button class="primary" data-switch="2" data-professor-control="set_switch">K → position 2</button>`
        : `<p>U₀ = ${fmt(S.u0)} V.</p><p class="formula">u_C(τ) = 0,37 × U₀</p>
      <div class="actions"><button class="primary" id="record-btn" data-professor-control="record_measurement">Relever u_C</button><button id="auto-btn" aria-pressed="${S.auto}" data-professor-control="auto_acquire">Acquisition automatique</button></div>
      ${table(S.measurements.discharge)}
      ${field('tauDischarge', 'τ lu pendant la décharge :', 's')}
      ${S.status === 'finished' ? `<p><b>TP terminé.</b> Énergie stockée au départ : ½·C·U₀² = ${fmt(energy(p.capacitance, S.u0), 1)} mJ.</p>` : ''}`}`,
  ];
  $('panel').innerHTML = panels[S.step]();
  bindPanel();
}

function bindPanel() {
  $('panel').querySelectorAll('[data-predict]').forEach(b => b.onclick = () => check('prediction', b.dataset.predict));
  $('panel').querySelectorAll('[data-param]').forEach(input => input.onchange = () => {
    const key = input.dataset.param, v = Number(input.value);
    setParameters({ [key]: key === 'resistance_ohm' ? RESISTANCES[v] : key === 'capacitance_uf' ? CAPACITANCES[v] : v });
  });
  $('panel').querySelectorAll('[data-switch]').forEach(b => b.onclick = () => setSwitch(b.dataset.switch));
  $('panel').querySelectorAll('[data-check]').forEach(b => b.onclick = () => check(b.dataset.check, $('f-' + b.dataset.check).value));
  $('panel').querySelectorAll('.field input').forEach(input => input.onkeydown = e => { if (e.key === 'Enter') check(input.id.slice(2), input.value); });
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

function renderCircuit() {
  const blade = $('switch-blade');
  blade.setAttribute('x2', S.switchPos === 1 ? '155' : '154');
  blade.setAttribute('y2', S.switchPos === 1 ? '42' : '86');
  $('emf-label').textContent = `E = ${S.params.emf} V`;
  $('meter-reading').textContent = `u_C = ${fmt(exact())} V`;
  $('clock').textContent = `t = ${fmtT(S.t)} s`;
}

function render() { renderSteps(); renderPanel(); renderCircuit(); syncTools(); drawGraph(); }

// ── Courbe ───────────────────────────────────────────────────────────────────
const canvas = $('graph'), ctx = canvas.getContext('2d');
const PAD = { l: 48, r: 14, t: 14, b: 32 };
function frame() {
  const w = canvas.clientWidth, h = canvas.clientHeight, dpr = devicePixelRatio || 1;
  if (canvas.width !== Math.round(w * dpr) || canvas.height !== Math.round(h * dpr)) { canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr); }
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  const uMax = S.mode === 'charge' ? S.params.emf * 1.12 : Math.max(S.u0, 1) * 1.12;
  return { w, h, uMax, x: t => PAD.l + t / span() * (w - PAD.l - PAD.r), y: u => h - PAD.b - u / uMax * (h - PAD.t - PAD.b) };
}

function drawGraph() {
  const f = frame(), { w, h, x, y, uMax } = f, T = span(), tauV = tauS();
  ctx.clearRect(0, 0, w, h);
  ctx.font = '11px system-ui'; ctx.fillStyle = '#94a3b8'; ctx.strokeStyle = '#1e293b'; ctx.lineWidth = 1;
  // Graduation « ronde » indépendante de τ : graduer en multiples de τ donnerait la réponse.
  const stepT = niceStep(T, 8);
  const decimals = Math.max(0, -Math.floor(Math.log10(stepT)));
  for (let t = 0; t <= T + 1e-9; t += stepT) {
    const gx = x(t); ctx.beginPath(); ctx.moveTo(gx, PAD.t); ctx.lineTo(gx, h - PAD.b); ctx.stroke();
    ctx.fillText(fmt(t, decimals), gx - 10, h - PAD.b + 14);
  }
  const stepU = uMax > 8 ? 2 : 1;
  for (let u = 0; u <= uMax; u += stepU) {
    const gy = y(u); ctx.beginPath(); ctx.moveTo(PAD.l, gy); ctx.lineTo(w - PAD.r, gy); ctx.stroke();
    ctx.fillText(fmt(u, 0), PAD.l - 18, gy + 4);
  }
  ctx.strokeStyle = '#94a3b8'; ctx.beginPath(); ctx.moveTo(PAD.l, PAD.t); ctx.lineTo(PAD.l, h - PAD.b); ctx.lineTo(w - PAD.r, h - PAD.b); ctx.stroke();
  ctx.fillText('u_C (V)', 4, PAD.t + 4); ctx.fillText('t (s)', w - PAD.r - 26, h - 6);

  const top = S.mode === 'charge' ? S.params.emf : S.u0;
  if (S.show.model) {
    ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 2; ctx.beginPath();
    for (let i = 0; i <= 200; i++) { const t = i / 200 * T; const u = exact(t); i ? ctx.lineTo(x(t), y(u)) : ctx.moveTo(x(t), y(u)); }
    ctx.stroke();
  }
  if (S.show.line) {
    const level = S.mode === 'charge' ? 0.63 * top : 0.37 * top;
    ctx.strokeStyle = '#fde68a'; ctx.setLineDash([5, 4]); ctx.lineWidth = 1.2;
    ctx.beginPath(); ctx.moveTo(PAD.l, y(level)); ctx.lineTo(w - PAD.r, y(level)); ctx.stroke(); ctx.setLineDash([]);
    ctx.fillStyle = '#fde68a'; ctx.fillText(S.mode === 'charge' ? '0,63 E' : '0,37 U₀', w - PAD.r - 46, y(level) - 4);
  }
  if (S.show.tangent) {
    ctx.strokeStyle = '#c084fc'; ctx.lineWidth = 1.4;
    ctx.beginPath();
    if (S.mode === 'charge') { ctx.moveTo(x(0), y(0)); ctx.lineTo(x(Math.min(T, tauV * 1.15)), y(tangentAtOrigin(top, tauV, Math.min(T, tauV * 1.15)))); }
    else { ctx.moveTo(x(0), y(top)); ctx.lineTo(x(tauV), y(0)); } // la tangente à l'origine coupe u = 0 à t = τ
    ctx.stroke();
    ctx.setLineDash([3, 3]); ctx.beginPath();
    const asym = S.mode === 'charge' ? top : 0; ctx.moveTo(PAD.l, y(asym)); ctx.lineTo(w - PAD.r, y(asym)); ctx.stroke(); ctx.setLineDash([]);
    ctx.fillStyle = '#c084fc'; ctx.fillText(S.mode === 'charge' ? 'u = E' : 'u = 0', w - PAD.r - 34, y(asym) - 4);
  }
  ctx.fillStyle = '#f97316';
  for (const p of points()) { ctx.beginPath(); ctx.arc(x(p.t), y(p.u), 3.2, 0, Math.PI * 2); ctx.fill(); }
  if (S.running || S.t > 0) {
    ctx.fillStyle = '#4ade80'; ctx.beginPath(); ctx.arc(x(S.t), y(exact()), 3, 0, Math.PI * 2); ctx.fill();
  }
  if (S.cursor) {
    ctx.strokeStyle = '#fde68a'; ctx.lineWidth = 1; ctx.setLineDash([2, 3]);
    ctx.beginPath(); ctx.moveTo(x(S.cursor.t), h - PAD.b); ctx.lineTo(x(S.cursor.t), y(S.cursor.u)); ctx.lineTo(PAD.l, y(S.cursor.u)); ctx.stroke(); ctx.setLineDash([]);
  }
}

canvas.addEventListener('click', event => {
  if (points().length < 2) { $('cursor-reading').textContent = 'Relève d’abord des points.'; return; }
  const f = frame(), rect = canvas.getBoundingClientRect();
  const t = (event.clientX - rect.left - PAD.l) / (f.w - PAD.l - PAD.r) * span();
  readAt(t);
});
$('show-model').onclick = () => toggleShow('model');
$('show-63').onclick = () => toggleShow('line');
$('show-tangent').onclick = () => toggleShow('tangent');
$('switch').addEventListener('click', () => setSwitch(S.switchPos === 1 ? 2 : 1));
$('switch').addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); setSwitch(S.switchPos === 1 ? 2 : 1); } });
$('hint').onclick = hint;
$('reset').onclick = reset;
addEventListener('resize', drawGraph);

// ── Animation ────────────────────────────────────────────────────────────────
/** Fait avancer le temps simulé, relève les points automatiques au passage. */
function advanceTo(target) {
  S.t = Math.min(span(), Math.max(S.t, target));
  if (S.auto) while (S.nextAuto <= S.t + 1e-9 && S.nextAuto <= span()) {
    const keep = S.t; S.t = S.nextAuto; record(false); S.t = keep; S.nextAuto = +(S.nextAuto + niceStep(span(), 20)).toFixed(6);
  }
  if (S.t >= span()) { S.running = false; S.status = 'paused'; feedback(S.mode === 'charge' ? 'Le condensateur est chargé : u_C ≈ E. Le courant est nul.' : 'Le condensateur est déchargé.'); renderPanel(); emit(true); }
  renderCircuit(); drawGraph(); emit();
}
runUntil = target => {
  if (!(S.switchPos === 1 || S.mode === 'discharge')) return;
  advanceTo(Number(target));
  if (S.t < span()) { S.running = false; S.status = 'paused'; renderPanel(); }
  emit(true);
};

let last = performance.now(), electronOffset = 0;
function tick(now) {
  const dt = Math.min(0.05, (now - last) / 1000); last = now;
  if (S.running) advanceTo(S.t + dt * span() * SIM_SECONDS_PER_REAL_SECOND);
  const i = Math.abs(current(S.mode, S.mode === 'charge' ? S.params.emf : S.u0, S.params.resistance, tauS(), S.t));
  const i0 = S.params.emf / S.params.resistance * 1000;
  const loop = $(S.mode === 'charge' ? 'loop-charge' : 'loop-discharge');
  const electron = $('electron');
  if ((S.running || S.t > 0) && i / i0 > 0.01 && S.t < span()) {
    electronOffset = (electronOffset + dt * 160 * (i / i0)) % loop.getTotalLength();
    const pt = loop.getPointAtLength(S.mode === 'charge' ? electronOffset : loop.getTotalLength() - electronOffset);
    electron.setAttribute('cx', pt.x); electron.setAttribute('cy', pt.y);
  } else { electron.setAttribute('cx', -10); electron.setAttribute('cy', -10); }
  requestAnimationFrame(tick);
}

feedback('Commence par prédire : la mesure tranchera.');
render(); manifest(); emit(true);
requestAnimationFrame(tick);
