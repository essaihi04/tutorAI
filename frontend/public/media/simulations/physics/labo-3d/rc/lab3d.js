import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { BENCH_Y, buildRoom, buildBench, buildPowerSupply, buildBoard, buildTray, buildVoltmeter, buildLaptop, makeCable } from './scene.js';
import {
  tau, chargeVoltage, dischargeVoltage, current, energy, tangentAtOrigin, reading,
  assessPrediction, assessTau, assessCapacitance, duration, niceStep,
} from '../../tp/rc/model.js';

const $ = id => document.getElementById(id);
const id = 'physics_rc_lab3d';
const RESISTANCES = [470, 1000, 2200, 4700];
const CAPACITANCES = [100, 470, 1000];
const STEPS = ['Prédire', 'Brancher', 'Composants', 'Voltmètre', 'Charger', 'Mesurer', 'Lire τ', 'Calculer C', 'Décharge'];
const SIM_PER_REAL = 1 / 8; // 5τ défilent en 8 s
const REQUIRED = { 'e+|ps+': 0xdc2626, 'e-|ps-': 0x111827, 'v+|vm+': 0xdc2626, 'v-|vm-': 0x111827 };
const pairKey = (a, b) => [a, b].sort().join('|');
const fmt = (v, d = 2) => Number(v).toLocaleString('fr-FR', { minimumFractionDigits: d, maximumFractionDigits: d });
const fmtOhms = r => r >= 1000 ? `${String(r / 1000).replace('.', ',')} kΩ` : `${r} Ω`;

// ── État ─────────────────────────────────────────────────────────────────────
const fresh = () => ({
  step: 0, done: new Set(), status: 'idle',
  params: { emf: 0, resistance: null, capacitance: null },
  cables: new Map(), pending: null,
  switchPos: 2, mode: 'charge', t: 0, running: false, u0: 0, auto: false, nextAuto: 0,
  measurements: { charge: [], discharge: [] },
  show: { model: false, line: false, tangent: false }, cursor: null,
  answers: { prediction: null, tau63: null, tauTangent: null, capacitance: null, tauDischarge: null },
  validated: { tau63: false, tauTangent: false, capacitance: false, tauDischarge: false },
  attempts: 0, hints: 0, hintIndex: 0, actions: [],
});
let S = fresh();
const ready = () => S.params.resistance && S.params.capacitance;
const tauS = () => ready() ? tau(S.params.resistance, S.params.capacitance) : 1;
const span = () => duration(tauS());
const fmtT = v => fmt(v, tauS() < 0.5 ? 3 : 2);
const exact = (t = S.t) => !ready() ? 0 : S.mode === 'charge' ? chargeVoltage(S.params.emf, tauS(), t) : dischargeVoltage(S.u0, tauS(), t);
const points = () => S.measurements[S.mode];
const connected = key => S.cables.has(key);
const supplyOk = () => connected('e+|ps+') && connected('e-|ps-');
const meterOk = () => connected('v+|vm+') && connected('v-|vm-');
const measureReady = () => S.measurements.charge.length >= 8 && S.measurements.charge.at(-1).t >= 3 * tauS();
const progress = () => S.done.size / STEPS.length;
function log(action, details = {}) { S.actions.push({ action, details, step: S.step, timestamp: Date.now() }); S.actions = S.actions.slice(-100); }

// ── Rendu 3D ─────────────────────────────────────────────────────────────────
const stage = $('stage');
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.05;
renderer.outputColorSpace = THREE.SRGBColorSpace;
stage.append(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color(0xdfe6ec);
const camera = new THREE.PerspectiveCamera(42, 1, 0.05, 40);
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true; controls.enablePan = false;
controls.minDistance = 0.45; controls.maxDistance = 3.2;
controls.minPolarAngle = 0.35; controls.maxPolarAngle = 1.42;
const VIEWS = {
  paillasse: { label: 'paillasse', pos: [0.05, 1.62, 1.62], target: [-0.05, 0.98, -0.05] },
  montage: { label: 'montage', pos: [-0.22, 1.36, 0.58], target: [-0.2, 0.92, 0.0] },
  ordinateur: { label: 'ordinateur', pos: [0.72, 1.26, 0.42], target: [0.98, 1.0, -0.16] },
};
let view = 'paillasse', camTween = null;
function setView(name, instant = false) {
  if (!VIEWS[name]) return;
  view = name; const v = VIEWS[name];
  const to = { pos: new THREE.Vector3(...v.pos), target: new THREE.Vector3(...v.target) };
  if (instant) { camera.position.copy(to.pos); controls.target.copy(to.target); controls.update(); }
  else camTween = { from: { pos: camera.position.clone(), target: controls.target.clone() }, to, t0: performance.now(), dur: 900 };
  $('views').textContent = `Vue : ${v.label}`;
}

scene.add(new THREE.HemisphereLight(0xffffff, 0xaab3bd, 1.25));
const sun = new THREE.DirectionalLight(0xffffff, 1.7);
sun.position.set(-2.5, 4.2, 2.4); sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048); Object.assign(sun.shadow.camera, { left: -2.2, right: 2.2, top: 2, bottom: -2, near: 0.5, far: 10 });
sun.shadow.bias = -0.0004; scene.add(sun);
const fill = new THREE.DirectionalLight(0xe0f2fe, 0.5); fill.position.set(3, 2.5, 2); scene.add(fill);

buildRoom(scene); buildBench(scene);
const ps = buildPowerSupply(scene);
const board = buildBoard(scene);
const tray = buildTray(scene, RESISTANCES, CAPACITANCES);
const meter = buildVoltmeter(scene);
const laptop = buildLaptop(scene, drawLaptop);
const terminals = { ...ps.terminals, ...board.pins, ...meter.terminals };
board.setLever(2); board.lever.rotation.y = board.lever.userData.targetAngle;

// Chaque objet interactif reçoit sa propre matière, pour pouvoir le surligner seul.
const interactive = [];
scene.traverse(o => { if (o.isMesh && o.userData.interactive) { o.material = o.material.clone(); interactive.push(o); } });

// ── Professeur ───────────────────────────────────────────────────────────────
let mixer = null, talkAction = null, idleAction = null, talkUntil = 0;
new GLTFLoader().load('/media/avatar/moalim-professeur.glb', gltf => {
  const model = gltf.scene;
  const box = new THREE.Box3().setFromObject(model), size = box.getSize(new THREE.Vector3());
  model.scale.setScalar(1.72 / size.y);
  const box2 = new THREE.Box3().setFromObject(model);
  model.position.set(-1.92, -box2.min.y, -0.12); model.rotation.y = 0.65;
  model.traverse(o => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } });
  scene.add(model);
  mixer = new THREE.AnimationMixer(model);
  const idle = gltf.animations.find(a => a.name === 'Idle'), talking = gltf.animations.find(a => a.name === 'Talking');
  if (idle) { idleAction = mixer.clipAction(idle); idleAction.play(); }
  if (talking) { talkAction = mixer.clipAction(talking); talkAction.setEffectiveWeight(0); talkAction.play(); }
}, undefined, () => {});

function say(text, kind = '', actions = []) {
  $('bubble-text').textContent = text; $('bubble').dataset.kind = kind;
  const box = $('bubble-actions'); box.innerHTML = '';
  for (const [label, fn, control] of actions) {
    const b = document.createElement('button'); b.textContent = label; b.onclick = fn;
    if (control) b.dataset.professorControl = control;
    box.append(b);
  }
  talkUntil = performance.now() + Math.min(6000, 900 + text.length * 45);
}

// ── Contrat tuteur ───────────────────────────────────────────────────────────
const commands = ['start', 'predict', 'connect', 'disconnect', 'place_component', 'set_emf', 'set_switch', 'record_measurement', 'auto_acquire',
  'pause', 'run_until', 'open_screen', 'close_screen', 'show_model', 'show_63', 'show_tangent', 'read_at', 'check', 'set_view', 'reveal_hint', 'reset'];
window.SIMULATION_CONFIG = {
  id, version: '1.0', title: 'Labo 3D — Charge et décharge d’un condensateur',
  variants: [{ id: 'lab3d_rc', label: 'Labo 3D dipôle RC', objective: 'Brancher le montage, mesurer u_C, déterminer τ par deux méthodes, en déduire C, étudier la décharge.' }],
  commands,
  command_schema: {
    predict: { answer: 'double | half | same' },
    connect: { from: 'ps+ | ps- | vm+ | vm-', to: 'e+ | e- | v+ | v-' },
    place_component: { kind: 'r | c', value: `R : ${RESISTANCES.join(' | ')} Ω ; C : ${CAPACITANCES.join(' | ')} µF` },
    set_emf: { value: '0..12 V' }, set_switch: { position: '1 | 2' }, run_until: { time_s: '0..5τ' }, read_at: { time_s: '0..5τ' },
    check: { field: 'tau63 | tauTangent | capacitance | tauDischarge', answer: 'nombre' }, set_view: { view: 'paillasse | montage | ordinateur' },
  },
};
function snapshot() {
  return {
    simulation_status: S.status, current_variant: 'lab3d_rc', step: S.step, step_label: STEPS[S.step], steps_done: [...S.done].map(i => STEPS[i]),
    parameters: { emf_v: S.params.emf, resistance_ohm: S.params.resistance, capacitance_uf: S.params.capacitance },
    cables: [...S.cables.keys()], supply_connected: supplyOk(), voltmeter_connected: meterOk(),
    switch_position: S.switchPos, mode: S.mode, time_s: +S.t.toFixed(4), tau_s: ready() ? +tauS().toFixed(4) : null,
    u_c_v: +exact().toFixed(3), measurements: S.measurements, student_answers: S.answers, validated: S.validated,
    attempts: S.attempts, hints_used: S.hints, view, objective_progress: progress(),
  };
}
let lastEmit = 0;
function emit(force = false) {
  const now = Date.now(); if (!force && now - lastEmit < 400) return; lastEmit = now;
  parent.postMessage({ type: 'simulation_state', simulation_id: id, current_state: snapshot(), student_actions: S.actions, objective_progress: progress(), timestamp: now }, '*');
}
function manifest() {
  window.__SIMULATION_MANIFEST_SENT__ = true; // évite le manifeste de secours de MediaViewer
  parent.postMessage({ type: 'simulation_manifest', simulation_id: id,
    capabilities: { commands, config: window.SIMULATION_CONFIG, globals: ['executeAICommand'], command_schema: window.SIMULATION_CONFIG.command_schema },
    page_text: 'Labo 3D : l’élève branche l’alimentation et le voltmètre avec des câbles, pose R et C sur la plaque, règle E au bouton, bascule K, relève u_C, puis exploite la courbe sur l’ordinateur (63 %, tangente, C = τ/R, décharge à 37 %).' }, '*');
}

// ── Déroulé guidé ────────────────────────────────────────────────────────────
function complete(i) { S.done.add(i); }
function advance() {
  // Les branchements et les composants peuvent se faire dans n'importe quel ordre :
  // l'étape courante est la première qui n'est pas encore faite.
  if (S.step >= 1 && S.step <= 4) {
    if (supplyOk()) complete(1); else S.done.delete(1);
    if (ready()) complete(2); else S.done.delete(2);
    if (meterOk()) complete(3); else S.done.delete(3);
    const next = [1, 2, 3].find(i => !S.done.has(i)) ?? 4;
    if (next !== S.step) { S.step = next; guide(); }
  }
  renderSteps(); renderMenu(); emit(true);
}

function guide() {
  const g = {
    0: () => say('Bienvenue au labo. Avant de manipuler : si on double la résistance R sans changer C, la durée de charge τ…', '', [
      ['double', () => predict('double'), 'predict'], ['est divisée par deux', () => predict('half'), 'predict'], ['ne change pas', () => predict('same'), 'predict']]),
    1: () => say('Branche l’alimentation sur la plaque : clique sur la borne + rouge du générateur, puis sur la borne E+ de la plaque. Fais de même pour la borne − et E−.'),
    2: () => say('Prends une résistance et un condensateur dans le plateau à droite : clique dessus pour les poser sur la plaque. Survole-les pour lire leur valeur.'),
    3: () => say('Branche le voltmètre en dérivation aux bornes du condensateur : borne V vers le côté +, borne COM vers le côté −.'),
    4: () => say('Tourne le bouton de l’alimentation pour régler E (glisse dessus ou utilise la molette), puis bascule l’interrupteur K sur la position 1.'),
    5: () => say('La charge commence. Relève u_C au fil du temps avec « Relever u_C », ou lance l’acquisition automatique. Il faut au moins 8 points, jusqu’au palier.'),
    6: () => say('Passe à l’ordinateur : trace la courbe, puis détermine τ par la méthode des 63 % et par la tangente à l’origine.', '', [['Ouvrir l’écran', openScreen, 'open_screen']]),
    7: () => say('Calcule maintenant C à partir de τ et de R, sur l’écran de l’ordinateur.', '', [['Ouvrir l’écran', openScreen, 'open_screen']]),
    8: () => say(S.mode === 'charge' ? 'Le condensateur est chargé. Bascule K sur la position 2 : il va se décharger dans R.' : 'Relève la décharge, puis lis τ à 37 % de U₀ sur l’ordinateur.', '', S.mode === 'discharge' ? [['Ouvrir l’écran', openScreen, 'open_screen']] : []),
  }[S.step];
  g?.();
}

function predict(answer) {
  if (S.step !== 0) return;
  S.answers.prediction = answer; S.attempts++;
  const r = assessPrediction(answer); log('predict', { answer });
  complete(0); S.step = 1; S.status = 'running';
  say(r.reason + ' Maintenant, au montage.', ''); setTimeout(() => { if (S.step === 1) guide(); }, 2600);
  advance();
}

// ── Branchements ─────────────────────────────────────────────────────────────
const deviceOf = t => t.startsWith('ps') ? 'ps' : t.startsWith('vm') ? 'vm' : 'board';
function wrongPair(a, b) {
  const [x, y] = [a, b].sort((p, q) => deviceOf(p).localeCompare(deviceOf(q)));
  const dx = deviceOf(x), dy = deviceOf(y);
  if (dx === dy) return 'Relie deux appareils différents : un câble va d’une borne à une autre.';
  if (dx === 'ps' && dy === 'vm') return 'Le voltmètre se branche aux bornes du condensateur, pas directement sur le générateur.';
  if (dx === 'board' && dy === 'ps') return y === 'ps+' && x === 'e-' || y === 'ps-' && x === 'e+'
    ? 'Polarité inversée : la borne + du générateur va à E+. Un condensateur électrochimique branché à l’envers peut être détruit.'
    : 'Le générateur alimente la plaque par ses bornes E+ et E−.';
  if (dx === 'board' && dy === 'vm') return x === 'v+' || x === 'v-'
    ? 'Voltmètre inversé : il afficherait une tension négative. La borne V va du côté + du condensateur.'
    : 'Pour mesurer u_C, branche le voltmètre aux bornes du condensateur (bornes V à droite de la plaque).';
  return 'Ce branchement ne correspond pas au montage.';
}
const cableMeshes = new Map();
function connect(a, b) {
  if (!terminals[a] || !terminals[b] || a === b) return;
  const key = pairKey(a, b); S.attempts++;
  if (!REQUIRED[key]) { log('connect', { from: a, to: b, correct: false }); say(wrongPair(a, b), 'bad'); return; }
  if (S.cables.has(key)) return;
  const p1 = terminals[a].getWorldPosition(new THREE.Vector3()), p2 = terminals[b].getWorldPosition(new THREE.Vector3());
  const mesh = makeCable(p1, p2, REQUIRED[key]); scene.add(mesh);
  S.cables.set(key, true); cableMeshes.set(key, mesh);
  log('connect', { from: a, to: b, correct: true });
  say(supplyOk() && S.step === 1 ? 'Alimentation branchée.' : meterOk() && S.step === 3 ? 'Voltmètre branché en dérivation aux bornes de C.' : 'Câble branché.', 'good');
  advance(); if (S.step <= 4) setTimeout(guide, 1400);
}
function disconnect(key) {
  if (S.step >= 5) { say('Ne débranche rien pendant la mesure.', 'bad'); return; }
  const mesh = cableMeshes.get(key); if (!mesh) return;
  scene.remove(mesh); mesh.geometry.dispose(); cableMeshes.delete(key); S.cables.delete(key);
  log('disconnect', { cable: key }); say('Câble débranché.'); advance();
}
function clickTerminal(tid) {
  const existing = [...S.cables.keys()].find(k => k.split('|').includes(tid));
  if (!S.pending && existing) { disconnect(existing); return; }
  if (!S.pending) { S.pending = tid; highlight(terminals[tid], 0xfde68a, 0.9); say('Choisis maintenant la borne d’arrivée du câble.'); return; }
  const from = S.pending; S.pending = null; highlight(terminals[from], 0, 0);
  if (from === tid) { say('Câble annulé.'); return; }
  connect(from, tid);
}

// ── Composants ───────────────────────────────────────────────────────────────
const tweens = [];
const placed = { r: null, c: null };
function moveTo(obj, position, rotationY) {
  tweens.push({ obj, from: obj.position.clone(), to: position.clone(), r0: obj.rotation.y, r1: rotationY, t0: performance.now(), dur: 650 });
}
function placeComponent(kind, value) {
  if (S.step >= 5) { say('Pour changer de composant, recommence le TP : les mesures ne décriraient plus ce circuit.', 'bad'); return; }
  const piece = tray.items.find(p => { let i; p.traverse(o => { i ??= o.userData.interactive; }); return i?.kind === kind && i.value === Number(value); });
  if (!piece) return;
  if (placed[kind] && placed[kind] !== piece) { const home = tray.homes.get(placed[kind]); moveTo(placed[kind], home.position, home.rotation); }
  placed[kind] = piece;
  moveTo(piece, kind === 'r' ? board.slots.r : board.slots.c, kind === 'r' ? 0 : Math.PI / 2);
  if (kind === 'r') S.params.resistance = Number(value); else S.params.capacitance = Number(value);
  log('place_component', { kind, value: Number(value) });
  say(kind === 'r' ? `Résistance posée : R = ${fmtOhms(Number(value))}.` : `Condensateur posé : C = ${value} µF.`, 'good');
  advance(); if (S.step <= 4) setTimeout(guide, 1400);
}

// ── Réglages et interrupteur ─────────────────────────────────────────────────
function setEmf(value) {
  if (S.step >= 5 && S.mode === 'charge' && S.t > 0 && S.status !== 'finished') { say('Ne change pas E pendant la mesure.', 'bad'); return; }
  S.params.emf = Math.round(Math.max(0, Math.min(12, Number(value))) * 2) / 2;
  ps.knob.rotation.z = -S.params.emf / 12 * Math.PI * 1.5;
  ps.lcd.redraw(S.params.emf); renderMenu(); emit();
}
function setSwitch(position) {
  const pos = Number(position) === 1 ? 1 : 2;
  if (pos === S.switchPos) return;
  if (pos === 1) {
    if (S.step < 4) { say('Termine d’abord le montage.', 'bad'); return; }
    if (S.step >= 8) { say('La charge est déjà étudiée : place K sur 2 pour la décharge.', 'bad'); return; }
    if (S.params.emf <= 0) { say('E = 0 V : règle d’abord la tension du générateur avec le bouton.', 'bad'); return; }
    S.switchPos = 1; board.setLever(1); S.mode = 'charge'; S.t = 0; S.u0 = 0; S.running = true; S.nextAuto = 0; S.measurements.charge = []; S.cursor = null;
    complete(4); S.step = 5; log('set_switch', { position: 1 }); guide();
  } else {
    S.switchPos = 2; board.setLever(2); log('set_switch', { position: 2 });
    if (S.step === 8 && S.mode === 'charge') {
      S.u0 = chargeVoltage(S.params.emf, tauS(), Math.max(S.t, span()));
      S.mode = 'discharge'; S.t = 0; S.running = true; S.nextAuto = 0; S.measurements.discharge = []; S.cursor = null; S.show = { model: false, line: false, tangent: false };
      guide();
    } else { S.running = false; say('K en position 2 : la charge est interrompue.'); }
  }
  renderMenu(); renderScreen(); emit(true);
}

// ── Mesures ──────────────────────────────────────────────────────────────────
function record(manual = true) {
  if (!(S.switchPos === 1 || S.mode === 'discharge') || !ready()) { if (manual) say('Il n’y a rien à mesurer : bascule d’abord K sur 1.', 'bad'); return; }
  if (!meterOk()) { if (manual) say('Le voltmètre n’est pas branché : il ne peut rien lire.', 'bad'); return; }
  const list = points(), t = +S.t.toFixed(4);
  if (list.some(p => Math.abs(p.t - t) < 1e-6)) return;
  list.push({ t, u: reading(exact(t), t * 1000 + list.length) }); list.sort((a, b) => a.t - b.t);
  if (manual) log('record_measurement', { t, mode: S.mode });
  if (S.step === 5 && measureReady()) { complete(5); S.step = 6; guide(); renderSteps(); }
  renderMenu(); renderScreen(); emit();
}
function advanceTo(target) {
  if (!ready()) return;
  S.t = Math.min(span(), Math.max(S.t, target));
  if (S.auto) while (S.nextAuto <= S.t + 1e-9 && S.nextAuto <= span()) {
    const keep = S.t; S.t = S.nextAuto; record(false); S.t = keep; S.nextAuto = +(S.nextAuto + niceStep(span(), 20)).toFixed(6);
  }
  if (S.t >= span() && S.running) {
    S.running = false;
    if (S.mode === 'charge' && !measureReady() && S.step === 5) say('Le condensateur est chargé : u_C ≈ E et le courant est nul. Il te manque des points : recommence la charge (K sur 2 puis sur 1).', 'bad');
    else if (S.mode === 'charge') say('Le condensateur est chargé : u_C ≈ E, le courant est nul.');
  }
  renderMenu();
}

// ── Écran d'acquisition ──────────────────────────────────────────────────────
function openScreen() { $('screen').hidden = false; log('open_screen'); renderScreen(); drawGraph(); emit(true); }
function closeScreen() { $('screen').hidden = true; emit(true); }
function toggleShow(key, value) { S.show[key] = value ?? !S.show[key]; log('show_' + key, { value: S.show[key] }); renderScreen(); drawGraph(); emit(); }
function readAt(t) {
  if (!ready()) return;
  const tt = Math.max(0, Math.min(span(), Number(t))); if (!Number.isFinite(tt)) return;
  S.cursor = { t: tt, u: exact(tt) };
  $('cursor-reading').textContent = `t = ${fmtT(tt)} s · u_C = ${fmt(S.cursor.u)} V`;
  log('read_at', { t: +tt.toFixed(4) }); drawGraph(); emit();
}
function check(field, answer) {
  S.attempts++;
  let r;
  if (field === 'tau63' || field === 'tauTangent') {
    if (S.step !== 6) return;
    S.answers[field] = answer; r = assessTau(answer, tauS(), field === 'tauTangent' ? 'tangent' : 'percent'); S.validated[field] = r.correct;
    if (S.validated.tau63 && S.validated.tauTangent) { complete(6); S.step = 7; }
  } else if (field === 'capacitance') {
    if (S.step !== 7) return;
    S.answers.capacitance = answer;
    const measured = Number(String(S.answers.tau63 ?? '').replace(',', '.')) || tauS();
    r = assessCapacitance(answer, measured, S.params.resistance, S.params.capacitance); S.validated.capacitance = r.correct;
    if (r.correct) {
      complete(7); S.step = 8;
      const t2 = tau(S.params.resistance * 2, S.params.capacitance);
      const said = { double: 'que τ double', half: 'que τ diminue de moitié', same: 'que τ ne change pas' }[S.answers.prediction] ?? 'rien';
      r = { correct: true, reason: `${r.reason} Et ta prédiction ? Avec R doublé, τ vaudrait ${fmtT(t2)} s, deux fois plus : tu avais prédit ${said}.` };
    }
  } else if (field === 'tauDischarge') {
    if (S.step !== 8 || S.mode !== 'discharge') return;
    S.answers.tauDischarge = answer; r = assessTau(answer, tauS(), 'discharge'); S.validated.tauDischarge = r.correct;
    if (r.correct) { complete(8); S.status = 'finished'; r = { correct: true, reason: `${r.reason} TP terminé : le condensateur avait stocké ½·C·U₀² = ${fmt(energy(S.params.capacitance, S.u0), 1)} mJ.` }; }
  } else return;
  log('check', { field, answer, correct: r.correct });
  say(r.reason, r.correct ? 'good' : 'bad');
  if (r.correct && S.step <= 8 && S.status !== 'finished' && (field === 'tauTangent' || field === 'tau63') && S.step === 7) setTimeout(guide, 2600);
  if (r.correct && field === 'capacitance') setTimeout(guide, 5200);
  renderSteps(); renderScreen(); emit(true);
}
function hint() {
  const H = {
    0: 'τ = R·C : que devient ce produit si R double ?', 1: 'Un câble part de la borne + rouge de l’alimentation et arrive sur la borne E+ de la plaque.',
    2: 'Survole les composants du plateau : leur valeur s’affiche. Clique pour les poser.', 3: 'Le voltmètre se branche en dérivation : ses deux bornes aux deux bornes de C.',
    4: 'Glisse horizontalement sur le bouton noir de l’alimentation, puis clique sur le levier orange de K.', 5: 'L’acquisition automatique relève un point à intervalle régulier.',
    6: 'Calcule 0,63 × E, puis clique sur la courbe à cette tension. La tangente coupe u = E à t = τ.', 7: 'C = τ / R, avec τ en s et R en Ω : le résultat est en F, à convertir en µF.',
    8: 'À t = τ, pendant la décharge, u_C = 0,37 × U₀.',
  };
  S.hints++; log('reveal_hint', { step: S.step }); say('Indice : ' + H[S.step]); emit(true);
}
function reset() {
  for (const mesh of cableMeshes.values()) scene.remove(mesh);
  cableMeshes.clear();
  for (const kind of ['r', 'c']) if (placed[kind]) { const h = tray.homes.get(placed[kind]); moveTo(placed[kind], h.position, h.rotation); placed[kind] = null; }
  S = fresh(); board.setLever(2); setEmf(0); closeScreen(); log('reset'); guide(); advance(); renderScreen();
}

window.executeAICommand = (command, p = {}) => {
  switch (command) {
    case 'start': if (S.step === 0) guide(); break;
    case 'predict': predict(p.answer); break;
    case 'connect': connect(p.from, p.to); break;
    case 'disconnect': disconnect(pairKey(p.from, p.to)); break;
    case 'place_component': placeComponent(p.kind, p.value); break;
    case 'set_emf': setEmf(p.value); break;
    case 'set_switch': setSwitch(p.position); break;
    case 'record_measurement': record(); break;
    case 'auto_acquire': S.auto = p.enabled ?? !S.auto; log('auto_acquire', { enabled: S.auto }); renderMenu(); emit(true); break;
    case 'pause': S.running = false; renderMenu(); emit(true); break;
    case 'run_until': if (S.switchPos === 1 || S.mode === 'discharge') { advanceTo(Number(p.time_s)); if (S.t < span()) S.running = false; } emit(true); break;
    case 'open_screen': openScreen(); break;
    case 'close_screen': closeScreen(); break;
    case 'show_model': toggleShow('model', p.enabled); break;
    case 'show_63': toggleShow('line', p.enabled); break;
    case 'show_tangent': toggleShow('tangent', p.enabled); break;
    case 'read_at': readAt(p.time_s); break;
    case 'check': check(p.field, p.answer); break;
    case 'set_view': setView(p.view); break;
    case 'reveal_hint': hint(); break;
    case 'reset': reset(); break;
    default: return { ok: false, error: 'Commande inconnue' };
  }
  return { ok: true, state: snapshot() };
};
window.addEventListener('message', e => {
  if (e.source !== parent || e.data?.type !== 'simulation_control') return;
  if (e.data.simulation_id && e.data.simulation_id !== id) return;
  window.executeAICommand(e.data.command, e.data.parameters || {});
});

// ── Interface 2D ─────────────────────────────────────────────────────────────
function renderSteps() {
  $('steps').innerHTML = STEPS.map((label, i) => `<li data-state="${S.done.has(i) ? 'done' : i === S.step ? 'current' : 'todo'}">${label}</li>`).join('');
}
function renderMenu() {
  const ms = Math.round(S.t * 1000), mm = String(Math.floor(ms / 60000)).padStart(2, '0'), ss = String(Math.floor(ms / 1000) % 60).padStart(2, '0');
  $('clock').textContent = `${mm}:${ss},${String(ms % 1000).padStart(3, '0')}`;
  $('v-emf').textContent = `${fmt(S.params.emf, 1)} V`;
  $('v-r').textContent = S.params.resistance ? fmtOhms(S.params.resistance) : '—';
  $('v-c').textContent = S.params.capacitance ? `${S.params.capacitance} µF` : '—';
  const shown = meterOk() ? fmt(exact()) : '----';
  $('v-uc').textContent = meterOk() ? `${shown} V` : 'non branché';
  $('v-k').textContent = `position ${S.switchPos}`;
  const canRecord = (S.switchPos === 1 || S.mode === 'discharge') && ready() && meterOk();
  $('record').disabled = !canRecord; $('auto').disabled = !canRecord; $('auto').setAttribute('aria-pressed', String(S.auto));
  const list = points();
  $('n-points').textContent = list.length;
  $('table').innerHTML = list.length ? `<table><thead><tr><th>n°</th><th>t (s)</th><th>u_C (V)</th></tr></thead><tbody>${list.map((pt, i) => `<tr><td>${i + 1}</td><td>${fmtT(pt.t)}</td><td>${fmt(pt.u)}</td></tr>`).join('')}</tbody></table>` : '<p>Aucun point.</p>';
  meter.lcd.redraw(meterOk() ? fmt(exact()) : '----');
}
const fieldHtml = (key, label, unit) => `<div class="field"><label for="f-${key}">${label}</label><input id="f-${key}" inputmode="decimal" value="${S.answers[key] ?? ''}" ${S.validated[key] ? 'disabled' : ''}> ${unit}
  <button data-check="${key}" data-professor-control="check" ${S.validated[key] ? 'disabled' : ''}>${S.validated[key] ? 'Validé ✓' : 'Vérifier'}</button></div>`;
function renderScreen() {
  const discharge = S.mode === 'discharge';
  $('show-line').textContent = discharge ? 'Ligne 0,37 U₀' : 'Ligne 0,63 E';
  [['show-model', 'model'], ['show-line', 'line'], ['show-tangent', 'tangent']].forEach(([el, key]) => { $(el).setAttribute('aria-pressed', String(S.show[key])); $(el).disabled = points().length < 2; });
  let html;
  if (S.step < 6) html = `<p>Les points relevés s’affichent ici. ${S.step === 5 ? 'Continue la mesure jusqu’au palier.' : ''}</p>`;
  else if (S.step === 6) html = `<p class="formula">u_C(τ) = 0,63 × E</p>${fieldHtml('tau63', 'τ par la méthode des 63 %', 's')}${fieldHtml('tauTangent', 'τ par la tangente à l’origine', 's')}`;
  else if (S.step === 7) html = `<p>R = ${fmtOhms(S.params.resistance)}. Valeur inscrite sur le condensateur : ${S.params.capacitance} µF.</p><p class="formula">τ = R · C ⇒ C = τ / R</p>${fieldHtml('capacitance', 'C =', 'µF')}`;
  else html = discharge ? `<p>U₀ = ${fmt(S.u0)} V</p><p class="formula">u_C(τ) = 0,37 × U₀</p>${fieldHtml('tauDischarge', 'τ lu pendant la décharge', 's')}` : '<p>Bascule K sur la position 2 pour la décharge.</p>';
  $('answers').innerHTML = html;
  $('answers').querySelectorAll('[data-check]').forEach(b => b.onclick = () => check(b.dataset.check, $('f-' + b.dataset.check).value));
  $('answers').querySelectorAll('input').forEach(i => i.onkeydown = e => { if (e.key === 'Enter') check(i.id.slice(2), i.value); });
}

// Courbe : la même sur l'écran du portable (texture) et dans la fenêtre agrandie.
function plot(ctx, w, h, big) {
  const PAD = big ? { l: 48, r: 14, t: 14, b: 32 } : { l: 40, r: 12, t: 46, b: 28 };
  ctx.fillStyle = '#0a1020'; ctx.fillRect(0, 0, w, h);
  if (!big) { ctx.fillStyle = '#38bdf8'; ctx.font = 'bold 22px system-ui'; ctx.fillText('Acquisition u_C(t)', 14, 30); }
  if (!ready()) { ctx.fillStyle = '#94a3b8'; ctx.font = '18px system-ui'; ctx.fillText('En attente du montage…', PAD.l + 10, h / 2); return null; }
  const T = span(), top = S.mode === 'charge' ? S.params.emf : S.u0, uMax = Math.max(top, 1) * 1.12;
  const x = t => PAD.l + t / T * (w - PAD.l - PAD.r), y = u => h - PAD.b - u / uMax * (h - PAD.t - PAD.b);
  ctx.font = `${big ? 11 : 15}px system-ui`; ctx.fillStyle = '#94a3b8'; ctx.strokeStyle = '#1e293b'; ctx.lineWidth = 1;
  const stepT = niceStep(T, 8), dec = Math.max(0, -Math.floor(Math.log10(stepT)));
  for (let t = 0; t <= T + 1e-9; t += stepT) { ctx.beginPath(); ctx.moveTo(x(t), PAD.t); ctx.lineTo(x(t), h - PAD.b); ctx.stroke(); ctx.fillText(fmt(t, dec), x(t) - 10, h - PAD.b + (big ? 14 : 20)); }
  const stepU = uMax > 8 ? 2 : 1;
  for (let u = 0; u <= uMax; u += stepU) { ctx.beginPath(); ctx.moveTo(PAD.l, y(u)); ctx.lineTo(w - PAD.r, y(u)); ctx.stroke(); ctx.fillText(fmt(u, 0), PAD.l - (big ? 18 : 22), y(u) + 4); }
  ctx.strokeStyle = '#94a3b8'; ctx.beginPath(); ctx.moveTo(PAD.l, PAD.t); ctx.lineTo(PAD.l, h - PAD.b); ctx.lineTo(w - PAD.r, h - PAD.b); ctx.stroke();
  if (big) { ctx.fillText('u_C (V)', 4, PAD.t + 4); ctx.fillText('t (s)', w - PAD.r - 26, h - 6); }
  const tauV = tauS();
  if (S.show.model) { ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 2; ctx.beginPath(); for (let i = 0; i <= 200; i++) { const t = i / 200 * T; i ? ctx.lineTo(x(t), y(exact(t))) : ctx.moveTo(x(t), y(exact(t))); } ctx.stroke(); }
  if (S.show.line) {
    const level = S.mode === 'charge' ? 0.63 * top : 0.37 * top;
    ctx.strokeStyle = '#fde68a'; ctx.setLineDash([5, 4]); ctx.beginPath(); ctx.moveTo(PAD.l, y(level)); ctx.lineTo(w - PAD.r, y(level)); ctx.stroke(); ctx.setLineDash([]);
  }
  if (S.show.tangent) {
    ctx.strokeStyle = '#c084fc'; ctx.lineWidth = 1.5; ctx.beginPath();
    if (S.mode === 'charge') { const t1 = Math.min(T, tauV * 1.15); ctx.moveTo(x(0), y(0)); ctx.lineTo(x(t1), y(tangentAtOrigin(top, tauV, t1))); }
    else { ctx.moveTo(x(0), y(top)); ctx.lineTo(x(tauV), y(0)); }
    ctx.stroke(); ctx.setLineDash([3, 3]); const asym = S.mode === 'charge' ? top : 0;
    ctx.beginPath(); ctx.moveTo(PAD.l, y(asym)); ctx.lineTo(w - PAD.r, y(asym)); ctx.stroke(); ctx.setLineDash([]);
  }
  ctx.fillStyle = '#f97316';
  for (const p of points()) { ctx.beginPath(); ctx.arc(x(p.t), y(p.u), big ? 3.2 : 4, 0, Math.PI * 2); ctx.fill(); }
  if (S.t > 0 && meterOk()) { ctx.fillStyle = '#4ade80'; ctx.beginPath(); ctx.arc(x(S.t), y(exact()), big ? 3 : 4, 0, Math.PI * 2); ctx.fill(); }
  if (big && S.cursor) {
    ctx.strokeStyle = '#fde68a'; ctx.setLineDash([2, 3]); ctx.beginPath();
    ctx.moveTo(x(S.cursor.t), h - PAD.b); ctx.lineTo(x(S.cursor.t), y(S.cursor.u)); ctx.lineTo(PAD.l, y(S.cursor.u)); ctx.stroke(); ctx.setLineDash([]);
  }
  return { PAD, T };
}
function drawLaptop(ctx, w, h) { plot(ctx, w, h, false); }
const graph = $('graph'), gctx = graph.getContext('2d');
let graphFrame = null;
function drawGraph() {
  if ($('screen').hidden) return;
  const w = graph.clientWidth, h = graph.clientHeight, dpr = devicePixelRatio || 1;
  if (graph.width !== Math.round(w * dpr) || graph.height !== Math.round(h * dpr)) { graph.width = Math.round(w * dpr); graph.height = Math.round(h * dpr); }
  gctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  graphFrame = plot(gctx, w, h, true); graphFrame && (graphFrame.w = w);
}
graph.addEventListener('click', e => {
  if (!graphFrame || points().length < 2) { $('cursor-reading').textContent = 'Relève d’abord des points.'; return; }
  const rect = graph.getBoundingClientRect(), { PAD, T, w } = graphFrame;
  readAt((e.clientX - rect.left - PAD.l) / (w - PAD.l - PAD.r) * T);
});

// ── Pointeur : survol, clic, bouton de réglage ───────────────────────────────
const raycaster = new THREE.Raycaster(), pointer = new THREE.Vector2();
let hovered = null, down = null, knobDrag = null;
function pick(e) {
  const r = renderer.domElement.getBoundingClientRect();
  pointer.set((e.clientX - r.left) / r.width * 2 - 1, -(e.clientY - r.top) / r.height * 2 + 1);
  raycaster.setFromCamera(pointer, camera);
  return raycaster.intersectObjects(interactive, false)[0]?.object ?? null;
}
function rootOf(o) { let n = o; while (n.parent && n.parent !== scene) n = n.parent; return n; }
function highlight(mesh, color, intensity) {
  const info = mesh.userData.interactive;
  const targets = info.type === 'component' ? (() => { const list = []; rootOf(mesh).traverse(o => { if (o.isMesh) list.push(o); }); return list; })() : [mesh];
  for (const m of targets) if (m.material.emissive) { m.material.emissive.setHex(color); m.material.emissiveIntensity = intensity; }
}
renderer.domElement.addEventListener('pointerdown', e => {
  down = { x: e.clientX, y: e.clientY };
  const hit = pick(e);
  if (hit?.userData.interactive.type === 'knob') { knobDrag = { x: e.clientX, emf: S.params.emf }; controls.enabled = false; }
});
renderer.domElement.addEventListener('pointermove', e => {
  if (knobDrag) { setEmf(knobDrag.emf + (e.clientX - knobDrag.x) / 18); return; }
  const hit = pick(e);
  if (hovered && hovered !== hit && !(S.pending && terminals[S.pending] === hovered)) highlight(hovered, 0, 0);
  hovered = hit;
  const tip = $('tooltip');
  if (hit) {
    highlight(hit, 0x38bdf8, 0.45);
    const info = hit.userData.interactive;
    tip.textContent = info.type === 'knob' ? `Réglage de E : ${fmt(S.params.emf, 1)} V (glisser ou molette)` : info.label;
    tip.style.left = e.clientX + 'px'; tip.style.top = e.clientY + 'px'; tip.hidden = false;
    renderer.domElement.style.cursor = 'pointer';
  } else { tip.hidden = true; renderer.domElement.style.cursor = ''; }
});
renderer.domElement.addEventListener('pointerup', e => {
  if (knobDrag) { knobDrag = null; controls.enabled = true; log('set_emf', { value: S.params.emf }); advance(); return; }
  if (!down || Math.hypot(e.clientX - down.x, e.clientY - down.y) > 6) return;
  const hit = pick(e); if (!hit) return;
  const info = hit.userData.interactive;
  if (info.type === 'terminal') clickTerminal(info.id);
  else if (info.type === 'component') placeComponent(info.kind, info.value);
  else if (info.type === 'switch') setSwitch(S.switchPos === 1 ? 2 : 1);
  else if (info.type === 'laptop') openScreen();
});
renderer.domElement.addEventListener('wheel', e => {
  const hit = pick(e);
  if (hit?.userData.interactive.type === 'knob') { e.preventDefault(); e.stopPropagation(); setEmf(S.params.emf + (e.deltaY < 0 ? 0.5 : -0.5)); }
}, { passive: false, capture: true });

$('record').onclick = () => record();
$('auto').onclick = () => window.executeAICommand('auto_acquire');
$('open-screen').onclick = openScreen;
$('close-screen').onclick = closeScreen;
$('show-model').onclick = () => toggleShow('model');
$('show-line').onclick = () => toggleShow('line');
$('show-tangent').onclick = () => toggleShow('tangent');
$('hint').onclick = hint;
$('reset').onclick = reset;
$('views').onclick = () => setView({ paillasse: 'montage', montage: 'ordinateur', ordinateur: 'paillasse' }[view]);
$('menu-toggle').onclick = () => { const body = $('menu-body'); body.hidden = !body.hidden; $('menu-toggle').setAttribute('aria-expanded', String(!body.hidden)); $('menu-toggle').textContent = body.hidden ? '▸' : '▾'; };

function resize() {
  const w = innerWidth, h = innerHeight;
  renderer.setSize(w, h); camera.aspect = w / h;
  camera.fov = w < 760 ? 58 : 42; camera.updateProjectionMatrix(); drawGraph();
}
addEventListener('resize', resize);

// ── Boucle ───────────────────────────────────────────────────────────────────
let last = performance.now(), laptopTimer = 0;
function frame(now) {
  const dt = Math.min(0.05, (now - last) / 1000); last = now;
  if (S.running && ready()) advanceTo(S.t + dt * span() * SIM_PER_REAL);
  if (S.running || S.t > 0) renderMenu();
  for (let i = tweens.length - 1; i >= 0; i--) {
    const tw = tweens[i], k = Math.min(1, (now - tw.t0) / tw.dur), e = k < 0.5 ? 2 * k * k : 1 - (-2 * k + 2) ** 2 / 2;
    tw.obj.position.lerpVectors(tw.from, tw.to, e); tw.obj.position.y += Math.sin(Math.PI * k) * 0.08; tw.obj.rotation.y = tw.r0 + (tw.r1 - tw.r0) * e;
    if (k >= 1) tweens.splice(i, 1);
  }
  const lever = board.lever; lever.rotation.y += (lever.userData.targetAngle - lever.rotation.y) * Math.min(1, dt * 12);
  // Les câbles de l'alimentation s'éclairent avec le courant.
  if (ready()) {
    const i = Math.abs(current(S.mode, S.mode === 'charge' ? S.params.emf : S.u0, S.params.resistance, tauS(), S.t)) / Math.max(1e-9, S.params.emf / S.params.resistance * 1000);
    const glow = (S.running && S.t < span()) ? i * 0.8 : 0;
    for (const key of ['e+|ps+', 'e-|ps-']) { const m = cableMeshes.get(key); if (m) m.material.emissiveIntensity = S.mode === 'charge' ? glow : 0; }
  }
  laptopTimer += dt; if (laptopTimer > 0.15) { laptopTimer = 0; laptop.screen.redraw(); if (!$('screen').hidden) drawGraph(); }
  if (camTween) {
    const k = Math.min(1, (now - camTween.t0) / camTween.dur), e = 1 - (1 - k) ** 3;
    camera.position.lerpVectors(camTween.from.pos, camTween.to.pos, e); controls.target.lerpVectors(camTween.from.target, camTween.to.target, e);
    if (k >= 1) camTween = null;
  }
  if (mixer) {
    const talking = now < talkUntil;
    talkAction?.setEffectiveWeight(THREE.MathUtils.lerp(talkAction.getEffectiveWeight(), talking ? 1 : 0, Math.min(1, dt * 6)));
    idleAction?.setEffectiveWeight(1 - (talkAction?.getEffectiveWeight() ?? 0));
    mixer.update(dt);
  }
  controls.update();
  renderer.render(scene, camera);
  requestAnimationFrame(frame);
}

resize(); setView('paillasse', true); setEmf(0);
renderSteps(); renderMenu(); renderScreen(); guide(); manifest(); emit(true);
$('loading').hidden = true;
requestAnimationFrame(frame);
