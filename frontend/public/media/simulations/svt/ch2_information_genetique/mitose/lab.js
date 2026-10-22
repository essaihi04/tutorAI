import {
  PHASES, PHASE_LABELS, PROTOCOL, COLS, ROWS, rng, assessOrder, generateField, counts, assessIdentification,
  assessIndex, assessDuration, DNA_CHOICES, assessDna, dnaQuantity,
} from './model.js';

const $ = id => document.getElementById(id);
const id = 'svt_mitosis_tp_lab';
const STEPS = ['Préparer', 'Observer', 'Identifier', 'Calculer', 'Interpréter'];
const CW = 64, CH = 46, FW = COLS * CW, FH = ROWS * CH;
const CYCLE_HOURS = 20;
const SHARP = 0.06;
const HINTS = [
  ['Il faut d’abord arrêter les divisions, puis rendre les cellules séparables, puis colorer, et enfin étaler.'],
  ['À l’objectif ×10, repère la zone où les noyaux sont nombreux, puis passe à ×40.', 'Tourne la mise au point lentement : l’image devient nette à un seul réglage.'],
  ['Regarde d’abord l’état des chromosomes : invisibles (chromatine diffuse), filaments, plaque au centre, deux lots qui s’écartent, ou deux noyaux.'],
  ['IM = cellules en division / total × 100. Les cellules en division sont toutes celles qui ne sont pas en interphase.', 'Durée d’une phase = (cellules dans cette phase / total) × durée du cycle.'],
  ['La phase S de l’interphase double l’ADN ; la séparation des chromatides le répartit entre deux cellules.'],
];

const field = generateField(7);
const C = counts(field);
const shuffledProtocol = (() => { const r = rng(11), list = PROTOCOL.map(s => s.id); for (let i = list.length - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [list[i], list[j]] = [list[j], list[i]]; } return list; })();

const fresh = () => ({
  step: 0, done: new Set(), status: 'idle',
  sequence: [], objective: 10, focus: 0.95, view: { x: FW / 2, y: FH / 2 }, selected: null,
  identified: {}, answers: { index: null, duration: null, dna: null }, validated: { index: false, duration: false, dna: false },
  attempts: 0, hints: 0, hintIndex: 0, actions: [],
});
let S = fresh();

const sharp = () => Math.abs(S.focus - field.focus) < SHARP;
const prepared = () => S.done.has(0);
const progress = () => S.done.size / STEPS.length;
function log(action, details = {}) { S.actions.push({ action, details, step: S.step, timestamp: Date.now() }); S.actions = S.actions.slice(-80); }
function feedback(text, kind = '') { $('feedback').textContent = text; $('feedback').dataset.kind = kind; }

// ── Contrat tuteur ───────────────────────────────────────────────────────────
const commands = ['start', 'protocol_add', 'protocol_undo', 'set_objective', 'set_focus', 'pan', 'center_on', 'check', 'go_to_step', 'reveal_hint', 'reset'];
window.SIMULATION_CONFIG = {
  id, version: '1.0', title: 'TP — La mitose dans la racine d’oignon',
  variants: [{ id: 'tp_mitose', label: 'TP mitose', objective: 'Préparer la lame, identifier les phases, calculer l’indice mitotique et la durée d’une phase, interpréter la quantité d’ADN.' }],
  commands,
  command_schema: {
    protocol_add: { step_id: PROTOCOL.map(s => s.id).join(' | ') },
    set_objective: { objective: '10 | 40' }, set_focus: { value: '0..1' }, pan: { dx: '-1 | 0 | 1', dy: '-1 | 0 | 1' },
    center_on: { cell: '1..5 (cellules repérées)' },
    check: { field: 'identify | index | duration | dna', cell: '1..5 (pour identify)', answer: 'phase | nombre | choix' },
    go_to_step: { step: '0..4' },
  },
};
function snapshot() {
  return {
    simulation_status: S.status, current_variant: 'tp_mitose', step: S.step, step_label: STEPS[S.step], steps_done: [...S.done].map(i => STEPS[i]),
    protocol_sequence: S.sequence, objective: S.objective, focus: +S.focus.toFixed(2), image_sharp: sharp(),
    identified: S.identified, counts: S.done.has(2) ? C : null, cycle_hours: CYCLE_HOURS,
    student_answers: S.answers, validated: S.validated, attempts: S.attempts, hints_used: S.hints, objective_progress: progress(),
  };
}
let lastEmit = 0;
function emit(force = false) {
  const now = Date.now(); if (!force && now - lastEmit < 300) return; lastEmit = now;
  parent.postMessage({ type: 'simulation_state', simulation_id: id, current_state: snapshot(), student_actions: S.actions, objective_progress: progress(), timestamp: now }, '*');
}
function manifest() {
  window.__SIMULATION_MANIFEST_SENT__ = true; // évite le manifeste de secours de MediaViewer
  parent.postMessage({ type: 'simulation_manifest', simulation_id: id,
    capabilities: { commands, config: window.SIMULATION_CONFIG, globals: ['executeAICommand'], command_schema: window.SIMULATION_CONFIG.command_schema },
    page_text: 'TP en cinq étapes : ordonner le protocole de préparation, observer au microscope (×10 puis ×40, mise au point), identifier cinq cellules repérées, calculer l’indice mitotique et la durée de la métaphase, interpréter la quantité d’ADN.' }, '*');
}

// ── Actions ─────────────────────────────────────────────────────────────────
function goTo(step) { S.step = Math.max(0, Math.min(STEPS.length - 1, step)); S.hintIndex = 0; if (S.step >= 1 && S.status === 'idle') S.status = 'running'; render(); emit(true); }

function protocolAdd(stepId) {
  if (prepared() || !PROTOCOL.some(s => s.id === stepId) || S.sequence.includes(stepId)) return;
  S.attempts++;
  const result = assessOrder([...S.sequence, stepId]);
  log('protocol_add', { step_id: stepId, correct: result.correct || result.position > S.sequence.length });
  if (!result.correct && result.position === S.sequence.length) { feedback(result.reason, 'bad'); renderPanel(); emit(true); return; }
  S.sequence.push(stepId);
  const done = PROTOCOL.find(s => s.id === stepId);
  if (result.correct) { S.done.add(0); feedback(result.reason + ' ' + done.why, 'good'); goTo(1); return; }
  feedback(`Bien : ${done.why}`, 'good');
  renderPanel(); emit(true);
}

function setObjective(value) {
  const obj = Number(value) === 40 ? 40 : 10;
  if (!prepared()) { feedback('Prépare d’abord la lame.', 'bad'); return; }
  if (obj === S.objective) return;
  S.objective = obj; log('set_objective', { objective: obj });
  if (obj === 40) feedback(sharp() ? 'Objectif ×40 : les cellules sont nettes.' : 'Objectif ×40. Refais la mise au point.');
  syncTools(); draw(); renderPanel(); emit(true);
}
function setFocus(value) {
  S.focus = Math.max(0, Math.min(1, Number(value))); if (!Number.isFinite(S.focus)) return;
  syncTools(); draw(); if (S.step === 1) renderPanel(); emit();
}
function clampView() {
  // Jusqu'au centre des cellules du bord : toute cellule repérée peut être mise au centre.
  S.view.x = Math.max(CW / 2, Math.min(FW - CW / 2, S.view.x)); S.view.y = Math.max(CH / 2, Math.min(FH - CH / 2, S.view.y));
}
function pan(dx, dy) { S.view.x += Number(dx) * CW; S.view.y += Number(dy) * CH; clampView(); log('pan', { dx, dy }); draw(); emit(); }
function centerOn(n) {
  const index = field.marked[Number(n) - 1]; if (index === undefined) return;
  const cell = field.cells[index];
  S.view = { x: cell.col * CW + CW / 2, y: cell.row * CH + CH / 2 }; clampView();
  S.selected = Number(n); if (S.objective !== 40 && prepared()) S.objective = 40;
  log('center_on', { cell: Number(n) }); syncTools(); draw(); renderPanel(); emit(true);
}

function check(fieldName, answer, cellNumber) {
  S.attempts++;
  let result;
  if (fieldName === 'identify') {
    const n = Number(cellNumber), index = field.marked[n - 1];
    if (index === undefined || !PHASES.includes(answer)) return;
    result = assessIdentification(field.cells[index].phase, answer);
    S.identified[n] = { answer, correct: result.correct };
    if (field.marked.every((_, i) => S.identified[i + 1]?.correct)) { S.done.add(2); result = { ...result, reason: result.reason + ' Les cinq cellules sont identifiées.' }; }
  } else if (fieldName === 'index') {
    S.answers.index = answer; result = assessIndex(answer, C); S.validated.index = result.correct;
  } else if (fieldName === 'duration') {
    S.answers.duration = answer; result = assessDuration(answer, C, 'metaphase', CYCLE_HOURS); S.validated.duration = result.correct;
  } else if (fieldName === 'dna') {
    S.answers.dna = answer; result = assessDna(answer); S.validated.dna = result.correct;
    if (result.correct) { S.done.add(4); S.status = 'finished'; }
  } else return;
  if (S.validated.index && S.validated.duration) S.done.add(3);
  log('check', { field: fieldName, answer, cell: cellNumber, correct: result.correct });
  feedback(result.reason, result.correct ? 'good' : 'bad');
  renderPanel(); renderSteps(); draw(); emit(true);
}

function hint() {
  const list = HINTS[S.step]; feedback('Indice : ' + list[Math.min(S.hintIndex, list.length - 1)]);
  S.hintIndex++; S.hints++; log('reveal_hint', { step: S.step }); emit(true);
}
function reset() { S = fresh(); log('reset'); feedback('Nouveau TP. Commence par la préparation de la lame.'); render(); emit(true); }

window.executeAICommand = (command, p = {}) => {
  switch (command) {
    case 'start': if (S.step === 0 && prepared()) goTo(1); break;
    case 'protocol_add': protocolAdd(p.step_id); break;
    case 'protocol_undo': if (!prepared() && S.sequence.length) { S.sequence.pop(); renderPanel(); emit(true); } break;
    case 'set_objective': setObjective(p.objective); break;
    case 'set_focus': setFocus(p.value); break;
    case 'pan': pan(p.dx ?? 0, p.dy ?? 0); break;
    case 'center_on': centerOn(p.cell); break;
    case 'check': check(p.field, p.answer, p.cell); break;
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

// ── Panneau ──────────────────────────────────────────────────────────────────
function renderSteps() {
  $('steps').innerHTML = STEPS.map((label, i) => `<li data-state="${S.done.has(i) ? 'done' : i === S.step ? 'current' : 'todo'}">${label}</li>`).join('');
}
const fieldInput = (key, label, unit) => `<div class="field"><label for="f-${key}">${label}</label><input id="f-${key}" inputmode="decimal" value="${S.answers[key] ?? ''}" ${S.validated[key] ? 'disabled' : ''}><span>${unit}</span>
  <button data-check="${key}" data-professor-control="check" ${S.validated[key] ? 'disabled' : ''}>${S.validated[key] ? 'Validé ✓' : 'Vérifier'}</button></div>`;

function dnaSvg() {
  const pts = Array.from({ length: 101 }, (_, i) => { const x = i / 100; return `${20 + x * 270},${100 - dnaQuantity(x) * 38}`; }).join(' ');
  return `<svg class="dna" viewBox="0 0 300 120" role="img" aria-label="Quantité d’ADN par cellule au cours du cycle">
    <line x1="20" y1="100" x2="295" y2="100" stroke="#94a3b8"/><line x1="20" y1="8" x2="20" y2="100" stroke="#94a3b8"/>
    <text x="24" y="14" fill="#94a3b8" font-size="10">Quantité d’ADN</text><text x="296" y="96" text-anchor="end" fill="#94a3b8" font-size="10">temps</text>
    <text x="4" y="66" fill="#94a3b8" font-size="10">q</text><text x="2" y="28" fill="#94a3b8" font-size="10">2q</text>
    <rect x="128" y="8" width="81" height="92" fill="#34d39914"/><text x="150" y="112" fill="#34d399" font-size="9">phase S</text>
    <rect x="236" y="8" width="54" height="92" fill="#f472b614"/><text x="248" y="112" fill="#f472b6" font-size="9">mitose</text>
    <polyline points="${pts}" fill="none" stroke="#fde68a" stroke-width="2.5"/></svg>`;
}

function renderPanel() {
  const panels = [
    () => `<h2>1. Préparer la lame</h2><p>Clique les étapes du protocole dans l’ordre.</p>
      <ol class="sequence">${S.sequence.map(sid => `<li>${PROTOCOL.find(s => s.id === sid).label}</li>`).join('') || '<li style="list-style:none;color:#94a3b8">Aucune étape choisie.</li>'}</ol>
      <div class="protocol">${shuffledProtocol.filter(sid => !S.sequence.includes(sid)).map(sid =>
        `<button data-protocol="${sid}" data-professor-control="protocol_add">${PROTOCOL.find(s => s.id === sid).label}</button>`).join('')}</div>`,
    () => `<h2>2. Observer</h2><p>Lame : méristème de racine d’oignon, coloré à l’orcéine.</p>
      <p>1. À l’objectif ×10, repère la zone de cellules en division.</p><p>2. Passe à l’objectif ×40.</p><p>3. Règle la mise au point jusqu’à une image nette.</p>
      <p>${S.objective === 40 ? (sharp() ? '<b style="color:#4ade80">Image nette à ×40.</b>' : 'Image floue : ajuste la mise au point.') : 'Objectif actuel : ×10.'}</p>
      <button class="primary" id="next-btn" data-professor-control="go_to_step" ${S.objective === 40 && sharp() ? '' : 'disabled'}>Identifier les phases →</button>`,
    () => `<h2>3. Identifier les phases</h2><p>Cinq cellules sont numérotées sur la lame. Clique sur « Voir », puis choisis sa phase.</p>
      ${field.marked.map((_, i) => { const n = i + 1, r = S.identified[n];
        return `<div class="cell-row" data-ok="${r?.correct ?? ''}"><strong>Cellule ${n}</strong><button data-see="${n}" data-professor-control="center_on" aria-pressed="${S.selected === n}">Voir</button>${
          r?.correct ? `<span style="color:#4ade80">${PHASE_LABELS[r.answer]} ✓</span>` : PHASES.map(ph => `<button data-identify="${n}" data-phase="${ph}" data-professor-control="check">${PHASE_LABELS[ph]}</button>`).join('')}</div>`; }).join('')}
      <button class="primary" id="next-btn" data-professor-control="go_to_step" ${S.done.has(2) ? '' : 'disabled'}>Compter et calculer →</button>`,
    () => `<h2>4. Calculer</h2><p>Un comptage du champ entier donne :</p>
      <table><thead><tr><th>Phase</th><th>Cellules</th></tr></thead><tbody>${PHASES.map(ph => `<tr><td>${PHASE_LABELS[ph]}</td><td>${C[ph]}</td></tr>`).join('')}
      <tr><td><b>Total</b></td><td><b>${Object.values(C).reduce((a, b) => a + b, 0)}</b></td></tr></tbody></table>
      <p>Durée du cycle cellulaire dans ce méristème : ${CYCLE_HOURS} h.</p>
      ${fieldInput('index', 'Indice mitotique IM =', '%')}
      ${fieldInput('duration', 'Durée de la métaphase =', 'min')}
      <button class="primary" id="next-btn" data-professor-control="go_to_step" ${S.done.has(3) ? '' : 'disabled'}>Interpréter →</button>`,
    () => `<h2>5. Interpréter</h2><p class="question">Au cours d’un cycle cellulaire, la quantité d’ADN d’une cellule est…</p>
      <div class="choices">${DNA_CHOICES.map(c => `<button data-dna="${c.id}" data-professor-control="check" aria-pressed="${S.answers.dna === c.id}" ${S.validated.dna ? 'disabled' : ''}>${c.label}</button>`).join('')}</div>
      ${S.validated.dna ? `${dnaSvg()}<p><b>TP terminé.</b> La mitose conserve l’information génétique : chaque cellule fille reçoit une copie complète de l’ADN.</p>` : ''}`,
  ];
  $('panel').innerHTML = panels[S.step]();
  const all = sel => $('panel').querySelectorAll(sel);
  all('[data-protocol]').forEach(b => b.onclick = () => protocolAdd(b.dataset.protocol));
  all('[data-see]').forEach(b => b.onclick = () => centerOn(b.dataset.see));
  all('[data-identify]').forEach(b => b.onclick = () => check('identify', b.dataset.phase, b.dataset.identify));
  all('[data-check]').forEach(b => b.onclick = () => check(b.dataset.check, $('f-' + b.dataset.check).value));
  all('.field input').forEach(input => input.onkeydown = e => { if (e.key === 'Enter') check(input.id.slice(2), input.value); });
  all('[data-dna]').forEach(b => b.onclick = () => check('dna', b.dataset.dna));
  const next = $('next-btn');
  if (next) next.onclick = () => { if (S.step === 1) S.done.add(1); goTo(S.step + 1); };
}

function syncTools() {
  $('obj10').setAttribute('aria-pressed', String(S.objective === 10));
  $('obj40').setAttribute('aria-pressed', String(S.objective === 40));
  ['obj10', 'obj40', 'focus'].forEach(el => { $(el).disabled = !prepared(); });
  document.querySelectorAll('[data-pan]').forEach(b => { b.disabled = !prepared() || S.objective !== 40; });
  $('focus').value = S.focus;
  $('scope-status').textContent = !prepared() ? 'Pas encore de lame sur la platine'
    : `Objectif ×${S.objective} · ${sharp() ? 'image nette' : 'image floue'}`;
}
function render() { renderSteps(); renderPanel(); syncTools(); draw(); }

// ── Microscope ───────────────────────────────────────────────────────────────
const canvas = $('scope'), ctx = canvas.getContext('2d');
const CHROMATIN = '#6b1238';
const details = field.cells.map(cell => {
  const r = rng(field.seed * 1000 + cell.index * 31);
  return {
    dots: Array.from({ length: 16 }, () => [(r() - 0.5) * 18, (r() - 0.5) * 14, 0.6 + r() * 0.9]),
    threads: Array.from({ length: 7 }, () => { const a = r() * Math.PI * 2, x = Math.cos(a) * 5 * r(), y = Math.sin(a) * 4 * r(); return [x, y, x + (r() - 0.5) * 14, y + (r() - 0.5) * 10, x + (r() - 0.5) * 8, y + (r() - 0.5) * 8]; }),
    rods: Array.from({ length: 8 }, (_, k) => [(r() - 0.5) * 2.5, -12 + k * 3.4 + (r() - 0.5) * 1.2, (r() - 0.5) * 0.6]),
  };
});

function geometry() {
  const w = canvas.clientWidth, h = canvas.clientHeight, dpr = devicePixelRatio || 1;
  if (canvas.width !== Math.round(w * dpr) || canvas.height !== Math.round(h * dpr)) { canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr); }
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  const d = Math.min(w, h) - 12, cx = w / 2, cy = h / 2;
  const scale = S.objective === 10 ? d * 0.86 / FW : d / (CW * 3.4);
  const view = S.objective === 10 ? { x: FW / 2, y: FH / 2 } : S.view;
  return { w, h, d, cx, cy, scale, view };
}

function drawCell(cell, x0, y0) {
  const dt = details[cell.index];
  ctx.save();
  ctx.translate(x0 + CW / 2, y0 + CH / 2); ctx.rotate(cell.angle * 0.12);
  ctx.fillStyle = `hsl(335, 60%, ${92 + cell.shade * 4}%)`; ctx.strokeStyle = '#a07a5c'; ctx.lineWidth = 1.4;
  ctx.beginPath(); ctx.roundRect(-CW / 2 + 1, -CH / 2 + 1, CW - 2, CH - 2, 3); ctx.fill(); ctx.stroke();
  ctx.lineCap = 'round';
  switch (cell.phase) {
    case 'interphase':
      ctx.fillStyle = '#e9a8c4'; ctx.beginPath(); ctx.ellipse(0, 0, 11 * cell.stretch, 9, cell.tilt, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = '#b4527f'; for (const [x, y, s] of dt.dots) { ctx.globalAlpha = 0.55; ctx.beginPath(); ctx.arc(x * 0.55, y * 0.55, s * 0.7, 0, Math.PI * 2); ctx.fill(); }
      ctx.globalAlpha = 1; ctx.fillStyle = CHROMATIN; ctx.beginPath(); ctx.arc(3, -2, 3, 0, Math.PI * 2); ctx.fill();
      break;
    case 'prophase':
      ctx.fillStyle = '#f2c4d8'; ctx.strokeStyle = '#c56b98'; ctx.lineWidth = 0.8;
      ctx.beginPath(); ctx.ellipse(0, 0, 13.5, 11, cell.tilt, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
      ctx.strokeStyle = CHROMATIN; ctx.lineWidth = 2.1;
      for (const [x, y, x2, y2, qx, qy] of dt.threads) { ctx.beginPath(); ctx.moveTo(x, y); ctx.quadraticCurveTo(qx, qy, Math.max(-11, Math.min(11, x2)), Math.max(-8, Math.min(8, y2))); ctx.stroke(); }
      break;
    case 'metaphase':
      ctx.strokeStyle = '#d9b3c7'; ctx.lineWidth = 0.6;
      for (let k = -3; k <= 3; k++) { ctx.beginPath(); ctx.moveTo(-26, 0); ctx.quadraticCurveTo(-8, k * 5, 0, k * 4); ctx.quadraticCurveTo(8, k * 5, 26, 0); ctx.stroke(); }
      ctx.strokeStyle = CHROMATIN; ctx.lineWidth = 3.2;
      for (const [x, y, a] of dt.rods) { ctx.beginPath(); ctx.moveTo(x - 3.5, y + a * 4); ctx.lineTo(x + 3.5, y - a * 4); ctx.stroke(); }
      break;
    case 'anaphase':
      ctx.strokeStyle = '#d9b3c7'; ctx.lineWidth = 0.6;
      for (let k = -2; k <= 2; k++) { ctx.beginPath(); ctx.moveTo(-26, 0); ctx.lineTo(26, k * 3); ctx.stroke(); }
      ctx.strokeStyle = CHROMATIN; ctx.lineWidth = 2.2;
      for (const side of [-1, 1]) for (const [x, y] of dt.rods) {
        const vx = side * (15 + x), vy = y * 0.85;
        ctx.beginPath(); ctx.moveTo(vx - side * 6, vy - 3); ctx.lineTo(vx, vy); ctx.lineTo(vx - side * 6, vy + 3); ctx.stroke();
      }
      break;
    case 'telophase':
      for (const side of [-1, 1]) {
        ctx.fillStyle = '#d985ac'; ctx.beginPath(); ctx.ellipse(side * 17, 0, 8, 10, 0, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = CHROMATIN; for (const [x, y, s] of dt.dots.slice(0, 9)) { ctx.globalAlpha = 0.7; ctx.beginPath(); ctx.arc(side * 17 + x * 0.35, y * 0.55, s * 0.8, 0, Math.PI * 2); ctx.fill(); }
        ctx.globalAlpha = 1;
      }
      ctx.strokeStyle = '#a07a5c'; ctx.lineWidth = 1.6; ctx.setLineDash([4, 2]);
      ctx.beginPath(); ctx.moveTo(0, -CH / 2 + 6); ctx.lineTo(0, CH / 2 - 6); ctx.stroke(); ctx.setLineDash([]);
      break;
  }
  ctx.restore();
}

function draw() {
  const g = geometry(), { w, h, d, cx, cy, scale, view } = g;
  ctx.clearRect(0, 0, w, h);
  ctx.fillStyle = '#05080f'; ctx.fillRect(0, 0, w, h);
  ctx.save();
  ctx.beginPath(); ctx.arc(cx, cy, d / 2, 0, Math.PI * 2); ctx.clip();
  const light = ctx.createRadialGradient(cx, cy, d * 0.05, cx, cy, d / 2);
  light.addColorStop(0, '#fffaf2'); light.addColorStop(1, '#f1dfc8');
  ctx.fillStyle = light; ctx.fillRect(cx - d / 2, cy - d / 2, d, d);
  if (prepared()) {
    const blur = Math.min(10, Math.abs(S.focus - field.focus) * (S.objective === 40 ? 34 : 14));
    ctx.filter = blur > 0.25 ? `blur(${blur.toFixed(1)}px)` : 'none';
    ctx.translate(cx, cy); ctx.scale(scale, scale); ctx.translate(-view.x, -view.y);
    for (const cell of field.cells) drawCell(cell, cell.col * CW, cell.row * CH);
    ctx.filter = 'none';
  }
  ctx.restore();
  // Numéros des cellules repérées : posés sur l'image, toujours lisibles.
  if (prepared() && S.step >= 2 && S.objective === 40) {
    ctx.font = 'bold 13px system-ui'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    field.marked.forEach((index, i) => {
      const cell = field.cells[index];
      const sx = cx + (cell.col * CW + 8 - view.x) * scale, sy = cy + (cell.row * CH + 8 - view.y) * scale;
      if (Math.hypot(sx - cx, sy - cy) > d / 2 - 12) return;
      const ok = S.identified[i + 1]?.correct;
      ctx.fillStyle = ok ? '#166534' : S.selected === i + 1 ? '#b45309' : '#0f172a';
      ctx.beginPath(); ctx.arc(sx, sy, 11, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = '#fff'; ctx.fillText(String(i + 1), sx, sy + 0.5);
    });
  }
  ctx.strokeStyle = '#1e293b'; ctx.lineWidth = 6; ctx.beginPath(); ctx.arc(cx, cy, d / 2 + 2, 0, Math.PI * 2); ctx.stroke();
}

// Glisser pour déplacer la lame (×40), cliquer sur un numéro pour sélectionner.
let drag = null;
canvas.addEventListener('pointerdown', e => { if (S.objective === 40 && prepared()) { drag = { x: e.clientX, y: e.clientY, moved: false }; canvas.setPointerCapture(e.pointerId); } });
canvas.addEventListener('pointermove', e => {
  if (!drag) return;
  const { scale } = geometry(), dx = e.clientX - drag.x, dy = e.clientY - drag.y;
  if (Math.abs(dx) + Math.abs(dy) > 3) drag.moved = true;
  S.view.x -= dx / scale; S.view.y -= dy / scale; clampView(); drag.x = e.clientX; drag.y = e.clientY; draw();
});
canvas.addEventListener('pointerup', e => {
  const wasDrag = drag?.moved; drag = null;
  if (wasDrag || S.step < 2 || S.objective !== 40) { if (wasDrag) { log('pan_drag'); emit(); } return; }
  const g = geometry(), rect = canvas.getBoundingClientRect();
  const wx = g.view.x + (e.clientX - rect.left - g.cx) / g.scale, wy = g.view.y + (e.clientY - rect.top - g.cy) / g.scale;
  const n = field.marked.findIndex(index => { const c = field.cells[index]; return wx >= c.col * CW && wx < (c.col + 1) * CW && wy >= c.row * CH && wy < (c.row + 1) * CH; });
  if (n >= 0) centerOn(n + 1);
});
$('obj10').onclick = () => setObjective(10);
$('obj40').onclick = () => setObjective(40);
$('focus').oninput = e => setFocus(e.target.value);
document.querySelectorAll('[data-pan]').forEach(b => b.onclick = () => { const [dx, dy] = b.dataset.pan.split(',').map(Number); pan(dx, dy); });
$('hint').onclick = hint;
$('reset').onclick = reset;
addEventListener('resize', draw);

feedback('Commence par préparer la lame : clique les étapes dans l’ordre.');
render(); manifest(); emit(true);
