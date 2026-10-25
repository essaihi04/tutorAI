// TP « Mitose dans la racine d'oignon » — dessiné au tableau.
// Le modèle (protocole, champ, phases, indice mitotique, durées, ADN) est dans model.js ;
// le dessin à la craie et le pont tuteur dans shared/tableau/tableau.js.
import {
  PHASES, PHASE_LABELS, PROTOCOL, COLS, ROWS, rng, assessOrder, generateField, counts, assessIdentification,
  assessIndex, assessDuration, DNA_CHOICES, assessDna, dnaQuantity,
} from './model.js';

const { Craie, fr, nombre, bulle, ecrire, onglets, curseur, glisser, protocole } = window.Tableau;
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
const OBJECTIFS = ['Ordonne les étapes du protocole pour obtenir une lame observable.', 'Repère la zone de division à ×10, passe à ×40 et fais la mise au point.', 'Cinq cellules sont numérotées : donne la phase de chacune.', 'Calcule l’indice mitotique et la durée de la métaphase.', 'Interprète la quantité d’ADN au cours du cycle.'];

const field = generateField(7);
const C = counts(field);
const TOTAL = Object.values(C).reduce((a, b) => a + b, 0);
const shuffledProtocol = (() => { const r = rng(11), list = PROTOCOL.map(s => s.id); for (let i = list.length - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [list[i], list[j]] = [list[j], list[i]]; } return list; })();

const fresh = () => ({
  step: 0, done: new Set(), status: 'idle',
  sequence: [], objective: 10, focus: 0.95, view: { x: FW / 2, y: FH / 2 }, selected: null,
  identified: {}, answers: { index: null, duration: null, dna: null }, validated: { index: false, duration: false, dna: false },
  attempts: 0, hints: 0, hintIndex: 0, lame: null, adn: null, dirty: true,
});
let S = fresh();
const ouvert = performance.now();
const scene = () => (performance.now() - ouvert) / 1000;

const sharp = () => Math.abs(S.focus - field.focus) < SHARP;
const prepared = () => S.done.has(0);
const progress = () => S.done.size / STEPS.length;
const feedback = (text, kind = '') => bulle($('feedback'), text, kind);
const redraw = () => { S.dirty = true; };

// ── Contrat tuteur ───────────────────────────────────────────────────────────
const commands = ['start', 'next', 'protocol_add', 'protocol_undo', 'set_objective', 'set_focus', 'pan', 'center_on', 'check', 'go_to_step', 'reveal_hint', 'reset'];
const config = {
  id, version: '2.0', title: 'TP — La mitose dans la racine d’oignon',
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
const pont = protocole({ id, commandes: commands, config, etat: snapshot, progression: progress, executer,
  texte: 'TP en cinq étapes, dessiné au tableau : ordonner le protocole de préparation, observer au microscope (×10 puis ×40, mise au point, lame déplacée en la glissant), identifier cinq cellules repérées, calculer l’indice mitotique et la durée de la métaphase, interpréter la quantité d’ADN.' });
const log = (action, details = {}) => pont.noter(action, { ...details, step: S.step });
let lastEmit = 0;
function emit(force = false) { const now = Date.now(); if (!force && now - lastEmit < 300) return; lastEmit = now; pont.emettre(); }

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
  if (result.correct) { S.done.add(0); S.lame = scene(); feedback(result.reason + ' ' + done.why, 'good'); goTo(1); return; }
  feedback(`Bien : ${done.why}`, 'good');
  renderPanel(); emit(true);
}
function protocolUndo() { if (!prepared() && S.sequence.length) { S.sequence.pop(); log('protocol_undo'); renderPanel(); emit(true); } }
function setObjective(value) {
  const obj = Number(value) === 40 ? 40 : 10;
  if (!prepared()) { feedback('Prépare d’abord la lame.', 'bad'); return; }
  if (obj === S.objective) return;
  S.objective = obj; log('set_objective', { objective: obj });
  if (obj === 40) feedback(sharp() ? 'Objectif ×40 : les cellules sont nettes.' : 'Objectif ×40. Refais la mise au point.');
  syncTools(); redraw(); renderPanel(); emit(true);
}
function setFocus(value) {
  S.focus = Math.max(0, Math.min(1, Number(value))); if (!Number.isFinite(S.focus)) return;
  syncTools(); redraw(); if (S.step === 1) renderPanel(); emit();
}
function clampView() { S.view.x = Math.max(CW / 2, Math.min(FW - CW / 2, S.view.x)); S.view.y = Math.max(CH / 2, Math.min(FH - CH / 2, S.view.y)); }
function pan(dx, dy) { S.view.x += Number(dx) * CW; S.view.y += Number(dy) * CH; clampView(); log('pan', { dx, dy }); redraw(); emit(); }
function centerOn(n) {
  const index = field.marked[Number(n) - 1]; if (index === undefined) return;
  const cell = field.cells[index];
  S.view = { x: cell.col * CW + CW / 2, y: cell.row * CH + CH / 2 }; clampView();
  S.selected = Number(n); if (S.objective !== 40 && prepared()) S.objective = 40;
  log('center_on', { cell: Number(n) }); syncTools(); redraw(); renderPanel(); emit(true);
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
    if (result.correct) { S.done.add(4); S.status = 'finished'; S.adn = scene(); }
  } else return;
  if (S.validated.index && S.validated.duration) S.done.add(3);
  log('check', { field: fieldName, answer, cell: cellNumber, correct: result.correct });
  feedback(result.reason, result.correct ? 'good' : 'bad');
  renderPanel(); renderSteps(); redraw(); emit(true);
}
function hint() {
  const list = HINTS[S.step]; feedback('Indice : ' + list[Math.min(S.hintIndex, list.length - 1)]);
  S.hintIndex++; S.hints++; log('reveal_hint', { step: S.step }); emit(true);
}
function reset() { S = fresh(); log('reset'); feedback('Nouveau TP. Commence par la préparation de la lame.'); render(); emit(true); }
function next() { if (S.step === 1) S.done.add(1); goTo(S.step + 1); }
function executer(command, p) {
  switch (command) {
    case 'start': if (S.step === 0 && prepared()) goTo(1); break;
    case 'next': if (!$('next-btn').disabled) next(); break;
    case 'protocol_add': protocolAdd(p.step_id); break;
    case 'protocol_undo': protocolUndo(); break;
    case 'set_objective': setObjective(p.objective); break;
    case 'set_focus': setFocus(p.value); break;
    case 'pan': pan(p.dx ?? 0, p.dy ?? 0); break;
    case 'center_on': centerOn(p.cell); break;
    case 'check': check(p.field, p.answer, p.cell); break;
    case 'go_to_step': goTo(Number(p.step)); break;
    case 'reveal_hint': hint(); break;
    case 'reset': reset(); break;
  }
}

// ── Panneau de l'étape ───────────────────────────────────────────────────────
function renderSteps() {
  onglets($('steps'), STEPS.map((label, i) => ({ id: 'step' + i, label: `${i + 1}. ${label}` })), 'step' + S.step, v => goTo(Number(v.slice(4))), new Set([...S.done].map(i => 'step' + i)));
}
function renderPanel() {
  const panel = $('panel');
  const titles = ['1. Préparer la lame', '2. Observer', '3. Identifier les phases', '4. Calculer', '5. Interpréter'];
  const bodies = [
    () => `<p>Clique les étapes du protocole dans l’ordre.</p>
      <ol class="sequence">${S.sequence.map(sid => `<li>${PROTOCOL.find(s => s.id === sid).label}</li>`).join('')}</ol>
      <div class="protocole">${shuffledProtocol.filter(sid => !S.sequence.includes(sid)).map(sid =>
        `<button class="craie-btn secondaire" data-protocol="${sid}" data-professor-control="protocol_add">${PROTOCOL.find(s => s.id === sid).label}</button>`).join('')}</div>`,
    () => `<p>Lame : méristème de racine d’oignon, coloré à l’orcéine.</p>
      <p>1. À l’objectif ×10, repère la zone de cellules en division.<br>2. Passe à l’objectif ×40.<br>3. Règle la mise au point jusqu’à une image nette.<br>4. Glisse la lame pour explorer le champ.</p>
      <p class="formule">${S.objective === 40 ? (sharp() ? 'Image nette à ×40.' : 'Image floue : ajuste la mise au point.') : 'Objectif actuel : ×10.'}</p>`,
    () => `<p>Cinq cellules sont numérotées sur la lame. Choisis-en une (elle se place au centre), puis sa phase.</p>
      <nav class="onglets cellules" data-professor-control="center_on">${field.marked.map((_, i) => { const n = i + 1, r = S.identified[n];
        return `<button class="onglet ${r?.correct ? 'ok' : ''}" data-see="${n}" aria-pressed="${S.selected === n}">cellule ${n}${r?.correct ? ' ✓' : ''}</button>`; }).join('')}</nav>
      ${S.selected && !S.identified[S.selected]?.correct ? `<div class="choix" data-professor-control="check">${PHASES.map(ph => `<label><input type="radio" name="phase" value="${ph}"> ${PHASE_LABELS[ph]}</label>`).join('')}</div>`
        : S.selected ? `<p class="formule">Cellule ${S.selected} : ${PHASE_LABELS[S.identified[S.selected].answer]} ✓</p>` : '<p class="legende">Clique un numéro.</p>'}`,
    () => `<p>Comptage du champ entier :</p>
      <table class="lecture-table"><thead><tr><th>Phase</th><th>Cellules</th></tr></thead><tbody>${PHASES.map(ph => `<tr><td>${PHASE_LABELS[ph]}</td><td>${C[ph]}</td></tr>`).join('')}
      <tr><td><b>Total</b></td><td><b>${TOTAL}</b></td></tr></tbody></table>
      <p>Durée du cycle cellulaire : ${CYCLE_HOURS} h.</p>
      ${champ('index', 'IM =', '%')}${champ('duration', 'Durée de la métaphase =', 'min')}
      <div class="champ-ligne"><button class="craie-btn attention" id="check" data-professor-control="check" ${S.validated.index && S.validated.duration ? 'disabled' : ''}>Vérifier</button></div>`,
    () => `<p>Au cours d’un cycle cellulaire, la quantité d’ADN d’une cellule est…</p>
      <div class="choix" data-professor-control="check">${DNA_CHOICES.map(c => `<label><input type="radio" name="dna" value="${c.id}" ${S.answers.dna === c.id ? 'checked' : ''} ${S.validated.dna ? 'disabled' : ''}> ${c.label}</label>`).join('')}</div>
      ${S.validated.dna ? '<canvas id="dna" role="img" aria-label="Quantité d’ADN par cellule au cours du cycle"></canvas><p class="formule">TP terminé : la mitose conserve l’information génétique, chaque cellule fille reçoit une copie complète de l’ADN.</p>' : ''}`,
  ];
  panel.innerHTML = `<h3 id="panel-title"></h3>${bodies[S.step]()}`;
  ecrire($('panel-title'), titles[S.step], { vitesse: 40 });
  const all = sel => panel.querySelectorAll(sel);
  all('[data-protocol]').forEach(b => b.onclick = () => protocolAdd(b.dataset.protocol));
  all('[data-see]').forEach(b => b.onclick = () => centerOn(b.dataset.see));
  all('input[name=phase]').forEach(r => r.onchange = () => check('identify', r.value, S.selected));
  all('input[name=dna]').forEach(r => r.onchange = () => check('dna', r.value));
  const verify = $('check');
  if (verify) verify.onclick = () => { for (const key of ['index', 'duration']) { const input = $('f-' + key); if (input && !S.validated[key] && input.value.trim()) { check(key, input.value); return; } } feedback('Saisis IM puis la durée de la métaphase.', 'bad'); };
  all('.champ-ligne input').forEach(input => input.onkeydown = e => { if (e.key === 'Enter') check(input.id.slice(2), input.value); });
  if (S.validated.dna && $('dna')) drawDna();
  const nextBtn = $('next-btn');
  const labels = ['Observer →', 'Identifier les phases →', 'Compter et calculer →', 'Interpréter →', 'TP terminé ✓'];
  nextBtn.textContent = labels[S.step];
  nextBtn.disabled = S.step === 0 ? !prepared() : S.step === 1 ? !(S.objective === 40 && sharp()) : S.step === 2 ? !S.done.has(2) : S.step === 3 ? !S.done.has(3) : true;
  $('undo').hidden = !(S.step === 0 && !prepared() && S.sequence.length);
  ecrire($('objective'), OBJECTIFS[S.step], { vitesse: 70 });
}
const champ = (key, label, unit) => `<div class="champ-ligne"><label class="craie-champ">${label} <input id="f-${key}" inputmode="decimal" autocomplete="off" value="${S.answers[key] ?? ''}" ${S.validated[key] ? 'disabled' : ''}> ${unit}</label>${S.validated[key] ? '<span class="valide">✓ validé</span>' : ''}</div>`;

let focusEl = null;
function syncTools() {
  $('obj10').setAttribute('aria-pressed', String(S.objective === 10));
  $('obj40').setAttribute('aria-pressed', String(S.objective === 40));
  $('obj10').disabled = $('obj40').disabled = !prepared();
  if (!focusEl) {
    focusEl = curseur({ id: 'focus', label: 'mise au point', min: 0, max: 1, step: .01, valeur: S.focus, decimales: 2, commande: 'set_focus' });
    focusEl.input.addEventListener('input', e => setFocus(e.target.value));
    $('focus-box').append(focusEl);
  }
  focusEl.maj(S.focus); focusEl.input.disabled = !prepared();
  $('scope-status').textContent = !prepared() ? 'pas encore de lame sur la platine' : `×${S.objective} · ${sharp() ? 'image nette' : 'image floue'}`;
}
function render() { renderSteps(); renderPanel(); syncTools(); redraw(); }

// ── Champ du microscope, à la craie ──────────────────────────────────────────
const canvas = $('scope'), craie = new Craie(canvas, { onresize: redraw });
const details = field.cells.map(cell => {
  const r = rng(field.seed * 1000 + cell.index * 31);
  return {
    dots: Array.from({ length: 10 }, () => [(r() - 0.5) * 18, (r() - 0.5) * 14]),
    threads: Array.from({ length: 6 }, () => { const a = r() * Math.PI * 2, x = Math.cos(a) * 5 * r(), y = Math.sin(a) * 4 * r(); return [x, y, Math.max(-11, Math.min(11, x + (r() - 0.5) * 14)), Math.max(-8, Math.min(8, y + (r() - 0.5) * 10))]; }),
    rods: Array.from({ length: 7 }, (_, k) => [(r() - 0.5) * 2.5, -11 + k * 3.6 + (r() - 0.5) * 1.2, (r() - 0.5) * 0.6]),
  };
});
function geometry() {
  const w = craie.W, h = craie.H, d = Math.min(w, h) - 12, cx = w / 2, cy = h / 2;
  const scale = S.objective === 10 ? d * 0.86 / FW : d / (CW * 3.4);
  const view = S.objective === 10 ? { x: FW / 2, y: FH / 2 } : S.view;
  return { w, h, d, cx, cy, scale, view };
}
const CELL = { duree: .035, tremble: .6 };
function drawCell(cell, x0, y0) {
  const dt = details[cell.index], c = craie.ctx;
  c.save(); c.translate(x0 + CW / 2, y0 + CH / 2); c.rotate(cell.angle * 0.12);
  craie.rect(-CW / 2 + 2, -CH / 2 + 2, CW - 4, CH - 4, { couleur: 'faible', largeur: 1.3, arrondi: 4, ...CELL });
  switch (cell.phase) {
    case 'interphase':
      craie.cercle(0, 0, 10 * cell.stretch, { couleur: 'rose', largeur: 1.4, depart: cell.tilt, ...CELL });
      for (const [x, y] of dt.dots.slice(0, 6)) craie.point(x * .5, y * .5, 1, 'rose');
      craie.point(3, -2, 2.4, 'violet');
      break;
    case 'prophase':
      craie.cercle(0, 0, 12.5, { couleur: 'rose', largeur: 1.1, depart: cell.tilt, ...CELL });
      for (const [x, y, x2, y2] of dt.threads) craie.ligne(x, y, x2, y2, { couleur: 'violet', largeur: 2, ...CELL });
      break;
    case 'metaphase':
      for (let k = -2; k <= 2; k += 2) craie.trait([[-25, 0], [0, k * 4], [25, 0]], { couleur: 'tresfaible', largeur: .8, ...CELL });
      for (const [x, y, a] of dt.rods) craie.ligne(x - 3.5, y + a * 4, x + 3.5, y - a * 4, { couleur: 'violet', largeur: 2.8, ...CELL });
      break;
    case 'anaphase':
      for (let k = -1; k <= 1; k++) craie.ligne(-25, 0, 25, k * 3, { couleur: 'tresfaible', largeur: .8, ...CELL });
      for (const side of [-1, 1]) for (const [x, y] of dt.rods) { const vx = side * (15 + x), vy = y * .85; craie.trait([[vx - side * 6, vy - 3], [vx, vy], [vx - side * 6, vy + 3]], { couleur: 'violet', largeur: 2, ...CELL }); }
      break;
    case 'telophase':
      for (const side of [-1, 1]) { craie.cercle(side * 17, 0, 8.5, { couleur: 'rose', largeur: 1.4, ...CELL }); for (const [x, y] of dt.dots.slice(0, 5)) craie.point(side * 17 + x * .3, y * .5, 1.3, 'violet'); }
      craie.ligne(0, -CH / 2 + 6, 0, CH / 2 - 6, { couleur: 'faible', largeur: 1.4, pointille: [4, 3], ...CELL });
      break;
  }
  c.restore();
}
function draw() {
  const { w, h, d, cx, cy, scale, view } = geometry(); if (w < 1 || h < 1) return true;
  craie.debut(3, scene());
  const c = craie.ctx;
  craie.cercle(cx, cy, d / 2, { couleur: 'blanc', largeur: 3, duree: 1 }).texte('champ du microscope', cx, cy + d / 2 + 20, { couleur: 'faible', taille: 14, align: 'center', duree: .6 });
  if (!prepared()) { craie.texte('pas encore de lame', cx, cy - 8, { couleur: 'faible', taille: 20, align: 'center' }).texte('prépare-la d’abord', cx, cy + 18, { couleur: 'faible', taille: 16, align: 'center' }); return craie.fin(); }
  craie.depuis(S.lame ?? 0);
  c.save(); c.beginPath(); c.arc(cx, cy, d / 2 - 2, 0, Math.PI * 2); c.clip();
  const blur = Math.min(10, Math.abs(S.focus - field.focus) * (S.objective === 40 ? 34 : 14));
  c.filter = blur > 0.25 ? `blur(${blur.toFixed(1)}px)` : 'none';
  c.translate(cx, cy); c.scale(scale, scale); c.translate(-view.x, -view.y);
  for (const cell of field.cells) drawCell(cell, cell.col * CW, cell.row * CH);
  c.filter = 'none';
  c.restore();
  if (S.step >= 2 && S.objective === 40) {
    craie.direct(() => field.marked.forEach((index, i) => {
      const cell = field.cells[index];
      const sx = cx + (cell.col * CW + 9 - view.x) * scale, sy = cy + (cell.row * CH + 9 - view.y) * scale;
      if (Math.hypot(sx - cx, sy - cy) > d / 2 - 12) return;
      const ok = S.identified[i + 1]?.correct, col = ok ? 'vert' : S.selected === i + 1 ? 'jaune' : 'cyan';
      craie.cercle(sx, sy, 10, { couleur: col, largeur: 1.6, fond: '#0a1410', fondAlpha: .85 }).texte(String(i + 1), sx, sy + 5, { couleur: col, taille: 15, align: 'center' });
    }));
  }
  return craie.fin();
}
// Glisser la lame (×40) ; un clic sur un numéro sélectionne la cellule.
let last = null, moved = 0;
glisser(canvas, {
  toucher: () => (prepared() && S.objective === 40 ? 'lame' : null),
  bouger: (_, x, y) => { if (last) { const { scale } = geometry(); S.view.x -= (x - last[0]) / scale; S.view.y -= (y - last[1]) / scale; clampView(); moved += Math.abs(x - last[0]) + Math.abs(y - last[1]); redraw(); } last = [x, y]; },
  lacher: () => {
    const wasDrag = moved > 3, [x, y] = last || [0, 0]; last = null; moved = 0;
    if (wasDrag) { log('pan_drag'); emit(); return; }
    if (S.step < 2) return;
    const g = geometry(), wx = g.view.x + (x - g.cx) / g.scale, wy = g.view.y + (y - g.cy) / g.scale;
    const n = field.marked.findIndex(index => { const cc = field.cells[index]; return wx >= cc.col * CW && wx < (cc.col + 1) * CW && wy >= cc.row * CH && wy < (cc.row + 1) * CH; });
    if (n >= 0) centerOn(n + 1);
  },
});
canvas.addEventListener('pointerdown', e => { const r = canvas.getBoundingClientRect(); last = [e.clientX - r.left, e.clientY - r.top]; moved = 0; });

// ── Courbe de l'ADN (étape 5), écrite en direct ──────────────────────────────
let dnaCraie = null;
function drawDna() {
  const cv = $('dna'); if (!cv) return;
  if (!dnaCraie || dnaCraie.canvas !== cv) dnaCraie = new Craie(cv, { onresize: () => drawDna() });
  const k = dnaCraie, W = k.W, H = k.H; if (W < 1) return;
  k.debut(5, scene() - (S.adn ?? 0));
  const x0 = 28, x1 = W - 10, y0 = H - 22, y1 = 8, X = u => x0 + (x1 - x0) * u, Y = q => y0 - (y0 - y1) * q / 2.3;
  k.fleche(x0, y0, x1, y0, { couleur: 'faible', largeur: 1.5 }).fleche(x0, y0, x0, y1, { couleur: 'faible', largeur: 1.5 });
  k.texte('temps', x1 - 4, y0 + 16, { couleur: 'faible', taille: 13, align: 'right' }).texte('q', x0 - 8, Y(1) + 5, { couleur: 'faible', taille: 13, align: 'right' }).texte('2q', x0 - 8, Y(2) + 5, { couleur: 'faible', taille: 13, align: 'right' });
  k.rect(X(.4), y1, X(.7) - X(.4), y0 - y1, { couleur: 'vert', largeur: 1, fond: 'vert', fondAlpha: .08, arrondi: 2, pointille: [3, 4] }).texte('phase S', X(.55), y0 + 16, { couleur: 'vert', taille: 13, align: 'center' });
  k.rect(X(.8), y1, X(1) - X(.8), y0 - y1, { couleur: 'rose', largeur: 1, fond: 'rose', fondAlpha: .08, arrondi: 2, pointille: [3, 4] }).texte('mitose', X(.9), y0 + 16, { couleur: 'rose', taille: 13, align: 'center' });
  k.courbe(u => [X(u), Y(dnaQuantity(u))], 100, { couleur: 'jaune', largeur: 2.6 });
  if (!k.fin()) requestAnimationFrame(drawDna);
}

$('obj10').onclick = () => setObjective(10);
$('obj40').onclick = () => setObjective(40);
$('hint').onclick = hint;
$('reset').onclick = reset;
$('undo').onclick = protocolUndo;
$('next-btn').onclick = next;
function frame() { if (S.dirty) S.dirty = !draw(); requestAnimationFrame(frame); }
feedback('Commence par préparer la lame : clique les étapes dans l’ordre.');
render(); emit(true); requestAnimationFrame(frame);
