// La salle de TP et le matériel du dipôle RC, en géométries Three.js simples.
// Unités : mètres. Le plateau de la paillasse est à y = 0,90.
import * as THREE from 'three';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';

export const BENCH_Y = 0.9;

export function canvasTexture(width, height, draw) {
  const canvas = document.createElement('canvas');
  canvas.width = width; canvas.height = height;
  const ctx = canvas.getContext('2d');
  const texture = new THREE.CanvasTexture(canvas);
  texture.colorSpace = THREE.SRGBColorSpace;
  texture.anisotropy = 4;
  const redraw = (...args) => { draw(ctx, width, height, ...args); texture.needsUpdate = true; };
  redraw();
  return { canvas, ctx, texture, redraw };
}

const mat = (color, extra = {}) => new THREE.MeshStandardMaterial({ color, roughness: 0.6, metalness: 0.05, ...extra });
function box(w, h, d, material, radius = 0) {
  const geometry = radius ? new RoundedBoxGeometry(w, h, d, 3, radius) : new THREE.BoxGeometry(w, h, d);
  const mesh = new THREE.Mesh(geometry, material);
  mesh.castShadow = true; mesh.receiveShadow = true;
  return mesh;
}
function cylinder(r, h, material, segments = 24) {
  const mesh = new THREE.Mesh(new THREE.CylinderGeometry(r, r, h, segments), material);
  mesh.castShadow = true; mesh.receiveShadow = true;
  return mesh;
}
function at(mesh, x, y, z) { mesh.position.set(x, y, z); return mesh; }

function sign(text, color) {
  return canvasTexture(256, 320, (ctx, w, h) => {
    ctx.fillStyle = '#ffffff'; ctx.fillRect(0, 0, w, h);
    ctx.strokeStyle = color; ctx.lineWidth = 18; ctx.beginPath(); ctx.arc(w / 2, 120, 84, 0, Math.PI * 2); ctx.stroke();
    if (color === '#dc2626') { ctx.beginPath(); ctx.moveTo(w / 2 - 60, 60); ctx.lineTo(w / 2 + 60, 180); ctx.stroke(); }
    ctx.fillStyle = '#111827'; ctx.font = 'bold 26px system-ui'; ctx.textAlign = 'center';
    text.split('\n').forEach((line, i) => ctx.fillText(line, w / 2, 250 + i * 32));
  }).texture;
}

/** Salle : sol, murs, fenêtres, paillasses du fond, tabourets, panneaux de sécurité. */
export function buildRoom(scene) {
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(16, 16), mat(0xb9c0c7, { roughness: 0.9 }));
  floor.rotation.x = -Math.PI / 2; floor.receiveShadow = true; scene.add(floor);
  const wallMat = mat(0xeef1f4, { roughness: 0.95 });
  const back = new THREE.Mesh(new THREE.PlaneGeometry(16, 3.4), wallMat); back.position.set(0, 1.7, -3.2); scene.add(back);
  const left = new THREE.Mesh(new THREE.PlaneGeometry(16, 3.4), wallMat); left.rotation.y = Math.PI / 2; left.position.set(-5, 1.7, 0); scene.add(left);
  const right = left.clone(); right.rotation.y = -Math.PI / 2; right.position.x = 5; scene.add(right);
  // Fenêtres lumineuses sur le mur de gauche.
  for (const z of [-2, 0.2]) {
    const win = new THREE.Mesh(new THREE.PlaneGeometry(1.6, 1.2), new THREE.MeshBasicMaterial({ color: 0xe0f2fe }));
    win.rotation.y = Math.PI / 2; win.position.set(-4.98, 1.9, z); scene.add(win);
  }
  // Paillasses et placards du fond : de la profondeur, sans détourner l'attention.
  const cabinet = mat(0xf8fafc), top = mat(0x4b5563, { roughness: 0.4 });
  for (const x of [-2.6, 0, 2.6]) {
    scene.add(at(box(2.2, 0.85, 0.7, cabinet, 0.02), x, 0.425, -2.75));
    scene.add(at(box(2.3, 0.04, 0.75, top), x, 0.87, -2.75));
    scene.add(at(box(2.2, 0.6, 0.35, cabinet, 0.02), x, 2.1, -3.0));
  }
  for (const x of [-2.4, 2.4]) {
    scene.add(at(box(2.6, 0.85, 0.8, cabinet, 0.02), x, 0.425, -1.35));
    scene.add(at(box(2.7, 0.04, 0.85, top), x, 0.87, -1.35));
  }
  // Panneaux de sécurité.
  [['Interdit\nde fumer', '#dc2626', -1.6], ['Interdit\nde manger', '#dc2626', -1.1], ['Lunettes\nobligatoires', '#2563eb', 1.3]].forEach(([text, color, x]) => {
    const plate = new THREE.Mesh(new THREE.PlaneGeometry(0.32, 0.4), new THREE.MeshStandardMaterial({ map: sign(text, color) }));
    plate.position.set(x, 1.75, -3.18); scene.add(plate);
  });
  // Tabourets devant la paillasse.
  const seat = mat(0x1f2937), leg = mat(0x9ca3af, { metalness: 0.6, roughness: 0.3 });
  for (const x of [-0.9, 0.9]) {
    scene.add(at(cylinder(0.17, 0.06, seat), x, 0.66, 0.85));
    scene.add(at(cylinder(0.025, 0.63, leg), x, 0.315, 0.85));
    scene.add(at(cylinder(0.2, 0.02, leg), x, 0.01, 0.85));
  }
}

/** La paillasse de l'élève. */
export function buildBench(scene) {
  scene.add(at(box(3.0, 0.05, 0.9, mat(0x374151, { roughness: 0.35 }), 0.01), 0, BENCH_Y - 0.025, -0.02));
  const body = mat(0xf1f5f9);
  scene.add(at(box(2.9, 0.82, 0.8, body, 0.02), 0, 0.43, -0.05));
  for (const x of [-1.05, -0.35, 0.35, 1.05]) {
    scene.add(at(box(0.62, 0.34, 0.01, mat(0xe2e8f0), 0.005), x, 0.62, 0.355));
    scene.add(at(box(0.12, 0.015, 0.02, mat(0x94a3b8, { metalness: 0.5 })), x, 0.75, 0.365));
  }
}

function terminal(color, label, id) {
  const group = new THREE.Group();
  const base = cylinder(0.009, 0.006, mat(0x111827)); base.rotation.x = Math.PI / 2; group.add(base);
  const cap = cylinder(0.007, 0.016, mat(color, { roughness: 0.35 })); cap.rotation.x = Math.PI / 2; cap.position.z = 0.009; group.add(cap);
  cap.userData.interactive = { type: 'terminal', id, label };
  group.userData.tip = cap;
  return group;
}

/** Alimentation stabilisée : écran, bouton de réglage, bornes + et −. */
export function buildPowerSupply(scene) {
  const g = new THREE.Group(); g.position.set(-0.88, BENCH_Y, -0.16); scene.add(g);
  g.add(at(box(0.3, 0.15, 0.22, mat(0xe5e7eb), 0.012), 0, 0.075, 0));
  g.add(at(box(0.28, 0.13, 0.002, mat(0x1f2937)), 0, 0.075, 0.111));
  const lcd = canvasTexture(256, 112, (ctx, w, h, volts = 0, on = true) => {
    ctx.fillStyle = '#0b2b1a'; ctx.fillRect(0, 0, w, h);
    ctx.fillStyle = on ? '#4ade80' : '#14532d'; ctx.font = 'bold 64px ui-monospace, Consolas, monospace'; ctx.textAlign = 'right';
    ctx.fillText(volts.toFixed(1).replace('.', ','), w - 52, 78); ctx.font = 'bold 34px system-ui'; ctx.fillText('V', w - 14, 78);
  });
  const screen = new THREE.Mesh(new THREE.PlaneGeometry(0.12, 0.052), new THREE.MeshBasicMaterial({ map: lcd.texture }));
  screen.position.set(-0.06, 0.1, 0.113); g.add(screen);
  const label = canvasTexture(256, 40, (ctx, w, h) => { ctx.fillStyle = '#e5e7eb'; ctx.font = 'bold 22px system-ui'; ctx.fillText('ALIMENTATION 0 – 12 V', 6, 28); });
  const labelMesh = new THREE.Mesh(new THREE.PlaneGeometry(0.12, 0.019), new THREE.MeshBasicMaterial({ map: label.texture, transparent: true }));
  labelMesh.position.set(-0.06, 0.045, 0.113); g.add(labelMesh);
  const knob = new THREE.Group(); knob.position.set(0.075, 0.1, 0.113); g.add(knob);
  const knobBody = cylinder(0.022, 0.02, mat(0x111827, { roughness: 0.4 }), 32); knobBody.rotation.x = Math.PI / 2; knobBody.position.z = 0.01; knob.add(knobBody);
  const mark = box(0.004, 0.016, 0.003, mat(0xf8fafc)); mark.position.set(0, 0.011, 0.021); knob.add(mark);
  knobBody.userData.interactive = { type: 'knob', id: 'emf', label: 'Bouton de réglage de E (glisser ou molette)' };
  const plus = terminal(0xdc2626, 'Borne + du générateur', 'ps+'); plus.position.set(0.05, 0.035, 0.113); g.add(plus);
  const minus = terminal(0x111827, 'Borne − du générateur', 'ps-'); minus.position.set(0.1, 0.035, 0.113); g.add(minus);
  return { group: g, lcd, knob, terminals: { 'ps+': plus.userData.tip, 'ps-': minus.userData.tip } };
}

// ── Plaque de montage ───────────────────────────────────────────────────────
const BOARD = { x: -0.16, z: 0.06, w: 0.5, d: 0.32, top: BENCH_Y + 0.016 };
const UV = { 'e+': [70, 120], 'e-': [70, 520], k1: [260, 120], k2: [260, 240], kc: [360, 120], r1: [450, 120], r2: [650, 120], 'c+': [850, 250], 'c-': [850, 400], 'v+': [945, 250], 'v-': [945, 400] };
export function boardPoint([u, v], lift = 0) {
  return new THREE.Vector3(BOARD.x + (u / 1000 - 0.5) * BOARD.w, BOARD.top + lift, BOARD.z + (v / 640 - 0.5) * BOARD.d);
}

export function buildBoard(scene) {
  const print = canvasTexture(1000, 640, (ctx, w, h) => {
    ctx.fillStyle = '#f8fafc'; ctx.fillRect(0, 0, w, h);
    ctx.strokeStyle = '#cbd5e1'; ctx.lineWidth = 1;
    for (let x = 20; x < w; x += 40) for (let y = 20; y < h; y += 40) { ctx.beginPath(); ctx.arc(x, y, 3, 0, Math.PI * 2); ctx.stroke(); }
    ctx.strokeStyle = '#0f172a'; ctx.lineWidth = 7; ctx.lineCap = 'round';
    const line = (...pts) => { ctx.beginPath(); pts.forEach(([x, y], i) => i ? ctx.lineTo(x, y) : ctx.moveTo(x, y)); ctx.stroke(); };
    line(UV['e+'], UV.k1); line(UV.kc, UV.r1); line(UV.r2, [850, 120], UV['c+']); line(UV['c-'], [850, 520], UV['e-']);
    line(UV.k2, [260, 520]); line(UV['c+'], UV['v+']); line(UV['c-'], UV['v-']);
    ctx.fillStyle = '#0f172a'; ctx.font = 'bold 30px system-ui';
    ctx.fillText('E+', 40, 85); ctx.fillText('E−', 40, 585); ctx.fillText('K', 330, 80); ctx.fillText('1', 228, 100); ctx.fillText('2', 222, 270);
    ctx.fillText('R', 535, 80); ctx.fillText('C', 790, 335); ctx.fillText('V', 965, 335);
    ctx.font = '22px system-ui'; ctx.fillStyle = '#475569'; ctx.fillText('Plaque de montage — dipôle RC', 380, 610);
    // Emplacements : rectangles en pointillés.
    ctx.setLineDash([10, 8]); ctx.lineWidth = 3; ctx.strokeStyle = '#64748b';
    ctx.strokeRect(470, 95, 160, 50); ctx.strokeRect(815, 270, 70, 110); ctx.setLineDash([]);
  });
  const board = box(BOARD.w, 0.016, BOARD.d, [mat(0x166534), mat(0x166534), new THREE.MeshStandardMaterial({ map: print.texture, roughness: 0.7 }), mat(0x166534), mat(0x166534), mat(0x166534)]);
  board.position.set(BOARD.x, BENCH_Y + 0.008, BOARD.z); scene.add(board);
  const pins = {};
  const pinMat = mat(0xd4a017, { metalness: 0.8, roughness: 0.3 });
  const labels = { 'e+': 'Borne E+ de la plaque', 'e-': 'Borne E− de la plaque', 'v+': 'Borne de mesure côté + du condensateur', 'v-': 'Borne de mesure côté − du condensateur' };
  for (const key of ['e+', 'e-', 'v+', 'v-']) {
    const pin = cylinder(0.008, 0.016, pinMat); pin.position.copy(boardPoint(UV[key], 0.008));
    pin.userData.interactive = { type: 'terminal', id: key, label: labels[key] }; scene.add(pin); pins[key] = pin;
  }
  for (const key of ['k1', 'k2', 'kc', 'r1', 'r2', 'c+', 'c-']) { const pad = cylinder(0.006, 0.004, pinMat); pad.position.copy(boardPoint(UV[key], 0.002)); scene.add(pad); }
  // Interrupteur K : un levier qui pivote vers la position 1 ou 2.
  const lever = new THREE.Group(); lever.position.copy(boardPoint(UV.kc, 0.01)); scene.add(lever);
  lever.add(at(cylinder(0.012, 0.012, mat(0x334155)), 0, 0, 0));
  const arm = box(0.052, 0.008, 0.012, mat(0xf59e0b, { roughness: 0.4 }), 0.003); arm.position.x = -0.026; lever.add(arm);
  arm.userData.interactive = { type: 'switch', id: 'k', label: 'Interrupteur K : cliquer pour basculer' };
  lever.children[0].userData.interactive = arm.userData.interactive;
  const target = p => { const a = boardPoint(UV.kc), b = boardPoint(UV[p]); return Math.atan2(-(b.z - a.z), -(b.x - a.x)); };
  const angles = { 1: target('k1'), 2: target('k2') };
  return {
    pins, lever, slots: { r: boardPoint([550, 120], 0.012), c: boardPoint([850, 325], 0.0) },
    setLever: pos => { lever.userData.targetAngle = -angles[pos]; },
    print,
  };
}

// ── Composants : résistances (code couleur) et condensateurs ─────────────────
const BAND = { 0: '#111111', 1: '#7c3f1d', 2: '#dc2626', 3: '#f97316', 4: '#facc15', 5: '#16a34a', 6: '#2563eb', 7: '#7c3aed', 8: '#6b7280', 9: '#f8fafc' };
const NAMES = { 0: 'noir', 1: 'marron', 2: 'rouge', 3: 'orange', 4: 'jaune', 5: 'vert', 6: 'bleu', 7: 'violet', 8: 'gris', 9: 'blanc' };
export function colourCode(ohms) {
  const exp = Math.floor(Math.log10(ohms)) - 1;
  const digits = String(Math.round(ohms / 10 ** exp)).padStart(2, '0');
  return [Number(digits[0]), Number(digits[1]), exp];
}
function formatOhms(ohms) { return ohms >= 1000 ? `${String(ohms / 1000).replace('.', ',')} kΩ` : `${ohms} Ω`; }

export function makeResistor(ohms) {
  const g = new THREE.Group();
  const body = cylinder(0.0075, 0.05, mat(0xe7d3b0), 20); body.rotation.z = Math.PI / 2; g.add(body);
  const code = colourCode(ohms);
  [...code, 'gold'].forEach((c, i) => {
    const band = cylinder(0.0078, 0.004, c === 'gold' ? mat(0xc8a43a, { metalness: 0.7, roughness: 0.3 }) : mat(BAND[c]), 20);
    band.rotation.z = Math.PI / 2; band.position.x = -0.016 + i * 0.009 + (i === 3 ? 0.006 : 0); g.add(band);
  });
  for (const side of [-1, 1]) { const lead = cylinder(0.0012, 0.03, mat(0xd1d5db, { metalness: 0.8 }), 8); lead.rotation.z = Math.PI / 2; lead.position.x = side * 0.04; g.add(lead); }
  const label = `Résistance ${formatOhms(ohms)} — ${code.slice(0, 2).map(d => NAMES[d]).join(', ')}, ${NAMES[code[2]]} (multiplicateur), or`;
  g.traverse(o => { if (o.isMesh) o.userData.interactive = { type: 'component', kind: 'r', value: ohms, label }; });
  return g;
}

export function makeCapacitor(uf) {
  const g = new THREE.Group();
  const r = 0.008 + Math.log10(uf) * 0.003, h = 0.028 + Math.log10(uf) * 0.008;
  const sleeve = canvasTexture(256, 128, (ctx, w, hh) => {
    ctx.fillStyle = '#1d4ed8'; ctx.fillRect(0, 0, w, hh);
    ctx.fillStyle = '#e2e8f0'; ctx.fillRect(0, 0, 40, hh);
    ctx.fillStyle = '#1d4ed8'; ctx.font = 'bold 30px system-ui'; ctx.fillText('−', 10, 74);
    ctx.fillStyle = '#f8fafc'; ctx.font = 'bold 34px system-ui'; ctx.fillText(`${uf} µF`, 60, 60); ctx.font = '22px system-ui'; ctx.fillText('16 V', 60, 96);
  });
  const body = cylinder(r, h, new THREE.MeshStandardMaterial({ map: sleeve.texture, roughness: 0.45 }), 28); body.position.y = h / 2 + 0.006; g.add(body);
  const topCap = cylinder(r * 0.98, 0.002, mat(0x9ca3af, { metalness: 0.7 })); topCap.position.y = h + 0.007; g.add(topCap);
  for (const side of [-1, 1]) { const lead = cylinder(0.0011, 0.012, mat(0xd1d5db, { metalness: 0.8 }), 8); lead.position.set(side * r * 0.45, 0.002, 0); g.add(lead); }
  const label = `Condensateur électrochimique ${uf} µF (polarisé)`;
  g.traverse(o => { if (o.isMesh) o.userData.interactive = { type: 'component', kind: 'c', value: uf, label }; });
  return g;
}

export function buildTray(scene, resistances, capacitances) {
  const tray = at(box(0.5, 0.02, 0.15, mat(0xcbd5e1), 0.006), 0.55, BENCH_Y + 0.01, 0.24); scene.add(tray);
  const homes = new Map(), items = [];
  resistances.forEach((ohms, i) => {
    const piece = makeResistor(ohms); const home = new THREE.Vector3(0.36 + i * 0.065, BENCH_Y + 0.03, 0.24);
    piece.position.copy(home); piece.rotation.y = Math.PI / 2; scene.add(piece); homes.set(piece, { position: home, rotation: Math.PI / 2 }); items.push(piece);
  });
  capacitances.forEach((uf, i) => {
    const piece = makeCapacitor(uf); const home = new THREE.Vector3(0.62 + i * 0.065, BENCH_Y + 0.02, 0.24);
    piece.position.copy(home); scene.add(piece); homes.set(piece, { position: home, rotation: 0 }); items.push(piece);
  });
  return { items, homes };
}

/** Voltmètre numérique. */
export function buildVoltmeter(scene) {
  const g = new THREE.Group(); g.position.set(0.36, BENCH_Y, -0.22); g.rotation.x = -0.12; scene.add(g);
  g.add(at(box(0.11, 0.18, 0.045, mat(0xfacc15, { roughness: 0.5 }), 0.012), 0, 0.09, 0));
  g.add(at(box(0.09, 0.15, 0.003, mat(0x1f2937)), 0, 0.095, 0.023));
  const lcd = canvasTexture(256, 112, (ctx, w, h, text = '----') => {
    ctx.fillStyle = '#9ca38f'; ctx.fillRect(0, 0, w, h);
    ctx.fillStyle = '#111827'; ctx.font = 'bold 66px ui-monospace, Consolas, monospace'; ctx.textAlign = 'right'; ctx.fillText(text, w - 46, 80);
    ctx.font = 'bold 30px system-ui'; ctx.fillText('V', w - 12, 80);
  });
  const screen = new THREE.Mesh(new THREE.PlaneGeometry(0.08, 0.035), new THREE.MeshBasicMaterial({ map: lcd.texture }));
  screen.position.set(0, 0.145, 0.026); g.add(screen);
  const dial = cylinder(0.022, 0.008, mat(0x111827)); dial.rotation.x = Math.PI / 2; dial.position.set(0, 0.09, 0.027); g.add(dial);
  const vPlus = terminal(0xdc2626, 'Borne V du voltmètre', 'vm+'); vPlus.position.set(-0.025, 0.035, 0.024); g.add(vPlus);
  const vCom = terminal(0x111827, 'Borne COM du voltmètre', 'vm-'); vCom.position.set(0.025, 0.035, 0.024); g.add(vCom);
  return { lcd, terminals: { 'vm+': vPlus.userData.tip, 'vm-': vCom.userData.tip } };
}

/** Ordinateur d'acquisition : son écran affiche la courbe en direct. */
export function buildLaptop(scene, drawScreen) {
  const g = new THREE.Group(); g.position.set(1.0, BENCH_Y, -0.12); g.rotation.y = -0.35; scene.add(g);
  g.add(at(box(0.34, 0.014, 0.24, mat(0x334155, { metalness: 0.3 }), 0.006), 0, 0.007, 0));
  const lid = new THREE.Group(); lid.position.set(0, 0.014, -0.115); lid.rotation.x = -0.25; g.add(lid);
  lid.add(at(box(0.34, 0.23, 0.01, mat(0x334155, { metalness: 0.3 }), 0.006), 0, 0.115, 0));
  const screen = canvasTexture(640, 420, drawScreen);
  const plane = new THREE.Mesh(new THREE.PlaneGeometry(0.31, 0.2), new THREE.MeshBasicMaterial({ map: screen.texture }));
  plane.position.set(0, 0.115, 0.0055); lid.add(plane);
  plane.userData.interactive = { type: 'laptop', id: 'screen', label: 'Ordinateur d’acquisition : ouvrir le logiciel' };
  return { screen };
}

/** Câble souple entre deux points, avec un léger affaissement. */
export function makeCable(from, to, color) {
  const mid = from.clone().lerp(to, 0.5);
  mid.y = Math.min(from.y, to.y) - 0.03 - from.distanceTo(to) * 0.08;
  mid.z += 0.04;
  const curve = new THREE.CatmullRomCurve3([
    from.clone(), from.clone().add(new THREE.Vector3(0, 0.025, 0.02)), mid, to.clone().add(new THREE.Vector3(0, 0.025, 0.02)), to.clone(),
  ]);
  curve.points.forEach(p => { p.y = Math.max(p.y, BENCH_Y + 0.006); });
  const mesh = new THREE.Mesh(new THREE.TubeGeometry(curve, 48, 0.0035, 8), new THREE.MeshStandardMaterial({ color, roughness: 0.5, emissive: color, emissiveIntensity: 0 }));
  mesh.castShadow = true;
  return mesh;
}
