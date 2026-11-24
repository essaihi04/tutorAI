/*
 * Les êtres vivants et les objets réels du cours « Les facteurs édaphiques » (activités 4 à 7, novembre 2026), peints
 * en couleur avant la craie (règle de l’utilisateur : un être vivant ou un objet réel = croquis peint, jamais deux traits
 * de craie ; un objet, un seul dessin dans tout le cours). Chargé APRÈS commun.js : ajoute à window.SolTableau.
 *   Animaux : campagnol, carabe, acarien, nematode, cloporte, araignee, iule, escargot, fourmi, lievre (le lombric = ST.ver).
 *   Plantes : chene (chêne-liège : houppier, tronc, racine pivotante), plantule, mousse, herbe, arbre.
 *   Objets : lampe, petri, feuilleMorte, flamme, chevre, nuage.
 *   Microflore : mycelium, bacterie.
 *   Tableau de données dessiné vide puis rempli en animation : tableauAnime (les cases s’allument, les nombres volent).
 * Chaque fonction peint sur le contexte brut `g` (à appeler dans craie.direct) ; `k` = échelle (1 = taille de référence).
 * Les fonctions des arthropodes renvoient la position de leurs paires de pattes, pour les compter en les allumant.
 */
(function () {
  'use strict';
  const ST = window.SolTableau, TAU = Math.PI * 2, { rgba, graine } = ST;
  const ombre = (g, x, y, rx, ry, a = .28) => { g.save(); g.fillStyle = `rgba(0,0,0,${a})`; g.beginPath(); g.ellipse(x, y, rx, ry, 0, 0, TAU); g.fill(); g.restore(); };
  const rad = (g, x, y, r, c0, c1, dx = -.35, dy = -.4) => { const gr = g.createRadialGradient(x + r * dx, y + r * dy, r * .08, x, y, r * 1.15); gr.addColorStop(0, c0); gr.addColorStop(1, c1); return gr; };
  const patte = (g, pts, l = 1.6, c = '#9a7a58') => { g.strokeStyle = c; g.lineWidth = l; g.lineCap = 'round'; g.lineJoin = 'round'; g.beginPath(); pts.forEach(([x, y], i) => (i ? g.lineTo(x, y) : g.moveTo(x, y))); g.stroke(); };

  /** Le campagnol (petit rongeur brun), tourné vers la droite (o.sens = -1 : vers la gauche). Taille de référence ≈ 70 × 34. */
  function campagnol(g, x, y, k = 1, o = {}) {
    const s = o.sens || 1; g.save(); g.translate(x, y); g.scale(k * s, k); g.globalAlpha *= o.alpha ?? 1;
    ombre(g, 0, 15, 30, 5);
    g.strokeStyle = '#c9a089'; g.lineWidth = 2.2; g.lineCap = 'round'; g.beginPath(); g.moveTo(-26, 6); g.quadraticCurveTo(-40, 8, -46, 2); g.stroke();
    g.fillStyle = rad(g, -4, -2, 28, '#b98a5e', '#6e4a2c'); g.beginPath(); g.ellipse(-4, 0, 27, 15, 0, 0, TAU); g.fill();
    g.fillStyle = rad(g, 22, -2, 13, '#c49a6c', '#7a5232'); g.beginPath(); g.ellipse(20, -1, 13, 10, .15, 0, TAU); g.fill();
    g.fillStyle = '#e8c3b0'; g.beginPath(); g.ellipse(33, 2, 3.2, 2.6, 0, 0, TAU); g.fill();
    g.fillStyle = '#5a3b22'; g.beginPath(); g.ellipse(14, -10, 5, 6, -.3, 0, TAU); g.fill(); g.fillStyle = '#d9a48c'; g.beginPath(); g.ellipse(14, -10, 2.6, 3.4, -.3, 0, TAU); g.fill();
    g.fillStyle = '#111'; g.beginPath(); g.arc(24, -4, 2.4, 0, TAU); g.fill(); g.fillStyle = '#fff'; g.beginPath(); g.arc(24.7, -4.8, .8, 0, TAU); g.fill();
    g.fillStyle = '#e9d4c6'; for (const px of [-18, 10]) { g.beginPath(); g.ellipse(px, 14, 4, 2.2, 0, 0, TAU); g.fill(); }
    g.strokeStyle = 'rgba(255,255,255,.35)'; g.lineWidth = .8; for (const a of [-.25, 0, .25]) { g.beginPath(); g.moveTo(32, 1); g.lineTo(42, 1 + a * 14); g.stroke(); }
    g.restore();
  }

  /** Le carabe : insecte, élytres métalliques (o.teinte = [r,g,b]), 3 paires de pattes, 1 paire d’antennes. Longueur ≈ 70 k. */
  function carabe(g, x, y, k = 1, o = {}) {
    const c = o.teinte || [40, 110, 90], P = [];
    g.save(); g.translate(x, y); g.scale(k, k); g.globalAlpha *= o.alpha ?? 1;
    ombre(g, 2, 6, 34, 14, .25);
    const pattes = [[-6, -10, -2, -24, -12, -32], [4, -10, 10, -24, 18, -32], [12, -9, 22, -20, 34, -26]];
    pattes.forEach(([x0, y0, x1, y1, x2, y2], i) => { patte(g, [[x0, y0], [x1, y1], [x2, y2]], 2.2); patte(g, [[x0, -y0], [x1, -y1], [x2, -y2]], 2.2); P.push([x0, 0]); });
    patte(g, [[30, -4], [42, -12], [52, -18]], 1.4); patte(g, [[30, 4], [42, 12], [52, 18]], 1.4);
    g.fillStyle = rad(g, -12, 0, 26, rgba(c.map(v => Math.min(255, v + 90)), 1), rgba(c.map(v => v * .35), 1)); g.beginPath(); g.ellipse(-12, 0, 26, 13, 0, 0, TAU); g.fill();
    g.strokeStyle = 'rgba(255,255,255,.35)'; g.lineWidth = 1; g.beginPath(); g.moveTo(-36, 0); g.lineTo(13, 0); g.stroke();
    for (const dy of [-6, 6]) { g.beginPath(); g.moveTo(-32, dy * .9); g.quadraticCurveTo(-12, dy * 1.3, 8, dy * .9); g.stroke(); }
    g.fillStyle = rad(g, 18, 0, 9, rgba(c.map(v => Math.min(255, v + 60)), 1), rgba(c.map(v => v * .3), 1)); g.beginPath(); g.ellipse(18, 0, 9, 8, 0, 0, TAU); g.fill();
    g.fillStyle = '#1b1b1b'; g.beginPath(); g.ellipse(29, 0, 6, 5, 0, 0, TAU); g.fill();
    g.restore();
    return P.map(([px, py]) => [x + px * k, y + py * k]);
  }

  /** Un acarien (mésofaune) : corps rond brun-orangé, 4 paires de pattes, pas d’antennes. Taille ≈ 24 k. */
  function acarien(g, x, y, k = 1, o = {}) {
    const P = []; g.save(); g.translate(x, y); g.scale(k, k); g.globalAlpha *= o.alpha ?? 1;
    for (let i = 0; i < 4; i++) { const bx = -6 + i * 4, d = (i - 1.5); for (const s of [-1, 1]) patte(g, [[bx, s * 6], [bx + d * 6, s * 13], [bx + d * 11, s * 18]], 1.3, '#7a4a20'); P.push([bx, 0]); }
    g.fillStyle = rad(g, 0, 0, 10, '#f3b45a', '#8a4a14'); g.beginPath(); g.ellipse(0, 0, 10, 9, 0, 0, TAU); g.fill();
    g.fillStyle = 'rgba(255,255,255,.5)'; g.beginPath(); g.arc(-3, -3, 2.2, 0, TAU); g.fill();
    g.restore(); return P.map(([px, py]) => [x + px * k, y + py * k]);
  }

  /** Un nématode (microfaune) : petit ver translucide vert pâle, en S. Longueur ≈ 60 k. */
  function nematode(g, x, y, k = 1, o = {}) {
    g.save(); g.translate(x, y); g.scale(k, k); g.globalAlpha *= o.alpha ?? 1; g.lineCap = 'round';
    const ph = o.phase || 0, pts = []; for (let i = 0; i <= 24; i++) { const u = i / 24; pts.push([-30 + u * 60, Math.sin(u * 6.5 + ph) * 9]); }
    for (const [w, c] of [[7, 'rgba(60,110,60,.75)'], [5, 'rgba(170,215,150,.95)'], [1.5, 'rgba(240,255,230,.7)']]) { g.strokeStyle = c; g.lineWidth = w; g.beginPath(); pts.forEach(([a, b], i) => (i ? g.lineTo(a, b) : g.moveTo(a, b))); g.stroke(); }
    g.restore();
  }

  /** Le cloporte (crustacé) : ovale gris segmenté, 7 paires de pattes, 1 paire d’antennes. Longueur ≈ 64 k. */
  function cloporte(g, x, y, k = 1, o = {}) {
    const P = []; g.save(); g.translate(x, y); g.scale(k, k); g.globalAlpha *= o.alpha ?? 1;
    ombre(g, 0, 5, 32, 13, .25);
    for (let i = 0; i < 7; i++) { const px = -20 + i * 6.5; patte(g, [[px, -10], [px - 2, -17], [px - 5, -21]], 1.4, '#3a3a40'); patte(g, [[px, 10], [px - 2, 17], [px - 5, 21]], 1.4, '#3a3a40'); P.push([px, 0]); }
    patte(g, [[28, -4], [38, -12], [44, -12]], 1.4, '#3a3a40'); patte(g, [[28, 4], [38, 12], [44, 12]], 1.4, '#3a3a40');
    g.fillStyle = rad(g, 0, 0, 30, '#c4c8d0', '#4b4f58'); g.beginPath(); g.ellipse(0, 0, 30, 14, 0, 0, TAU); g.fill();
    g.strokeStyle = 'rgba(30,30,35,.6)'; g.lineWidth = 1.1; for (let i = -3; i <= 3; i++) { const px = i * 7.5; g.beginPath(); g.moveTo(px, -Math.sqrt(Math.max(0, 1 - (px / 30) ** 2)) * 14); g.lineTo(px, Math.sqrt(Math.max(0, 1 - (px / 30) ** 2)) * 14); g.stroke(); }
    g.restore(); return P.map(([px, py]) => [x + px * k, y + py * k]);
  }

  /** L’araignée (arachnide) : céphalothorax + abdomen bruns, 4 paires de pattes, pas d’antennes. Taille ≈ 80 k. */
  function araignee(g, x, y, k = 1, o = {}) {
    const P = []; g.save(); g.translate(x, y); g.scale(k, k); g.globalAlpha *= o.alpha ?? 1;
    ombre(g, -6, 8, 30, 10, .22);
    // 4 paires de pattes attachées le long du céphalothorax (de l’arrière vers l’avant), en éventail
    [-1.2, -.4, .4, 1.2].forEach((d, i) => { const bx = -12 + i * 9; for (const s of [-1, 1]) patte(g, [[bx, s * 5], [bx + d * 14, s * 22], [bx + d * 30, s * 34]], 1.8, '#9a7a58'); P.push([bx, 0]); });
    g.fillStyle = rad(g, -30, 0, 15, '#a5794f', '#3c2614'); g.beginPath(); g.ellipse(-30, 0, 16, 12, 0, 0, TAU); g.fill();
    g.fillStyle = rad(g, 2, 0, 15, '#9a7350', '#3a2716'); g.beginPath(); g.ellipse(2, 0, 16, 9, 0, 0, TAU); g.fill();
    g.fillStyle = 'rgba(0,0,0,.6)'; g.beginPath(); g.arc(16, -2, 1.3, 0, TAU); g.arc(16, 2, 1.3, 0, TAU); g.fill();
    g.restore(); return P.map(([px, py]) => [x + px * k, y + py * k]);
  }

  /** L’iule (myriapode) : long corps noir cylindrique en anneaux, très nombreuses pattes rouges (plus de 15 paires). */
  function iule(g, x, y, k = 1, o = {}) {
    const P = []; g.save(); g.translate(x, y); g.scale(k, k); g.globalAlpha *= o.alpha ?? 1;
    ombre(g, 0, 9, 62, 7, .22);
    for (let i = 0; i < 26; i++) { const px = -56 + i * 4.4; patte(g, [[px, 4], [px - 1, 11]], 1.2, '#c0462c'); P.push([px, 0]); }
    g.fillStyle = (() => { const gr = g.createLinearGradient(0, -8, 0, 8); gr.addColorStop(0, '#6b6f78'); gr.addColorStop(.35, '#2b2d33'); gr.addColorStop(1, '#0f1013'); return gr; })();
    g.beginPath(); g.ellipse(0, 0, 62, 8, 0, 0, TAU); g.fill();
    g.strokeStyle = 'rgba(160,165,175,.45)'; g.lineWidth = 1; for (let i = -13; i <= 13; i++) { g.beginPath(); g.moveTo(i * 4.4, -7); g.lineTo(i * 4.4, 7); g.stroke(); }
    patte(g, [[60, -3], [68, -10]], 1.2, '#3a3a40'); patte(g, [[60, 3], [68, 10]], 1.2, '#3a3a40');
    g.restore(); return P.map(([px, py]) => [x + px * k, y + py * k]);
  }

  /** L’escargot (mollusque) : coquille brune en spirale, corps mou beige, tentacules. Taille ≈ 80 k. */
  function escargot(g, x, y, k = 1, o = {}) {
    g.save(); g.translate(x, y); g.scale(k, k); g.globalAlpha *= o.alpha ?? 1;
    ombre(g, 0, 14, 40, 5, .25);
    g.fillStyle = (() => { const gr = g.createLinearGradient(0, 4, 0, 14); gr.addColorStop(0, '#d9c3a0'); gr.addColorStop(1, '#9c8463'); return gr; })();
    g.beginPath(); g.moveTo(-36, 13); g.quadraticCurveTo(-10, 2, 26, 4); g.quadraticCurveTo(36, 0, 38, -10); g.quadraticCurveTo(44, 8, 30, 13); g.closePath(); g.fill();
    patte(g, [[34, -6], [40, -22]], 2.2, '#b49b78'); patte(g, [[30, -6], [32, -20]], 2.2, '#b49b78');
    g.fillStyle = '#2a1d10'; g.beginPath(); g.arc(40, -22, 2.2, 0, TAU); g.arc(32, -20, 2, 0, TAU); g.fill();
    g.fillStyle = rad(g, -4, -10, 22, '#e0a95e', '#6b3d14'); g.beginPath(); g.arc(-4, -10, 21, 0, TAU); g.fill();
    g.strokeStyle = 'rgba(60,30,10,.75)'; g.lineWidth = 2; g.beginPath();
    for (let i = 0; i <= 60; i++) { const a = i / 60 * TAU * 2.4, r = 18 * (1 - i / 66); i ? g.lineTo(-4 + Math.cos(a) * r, -10 + Math.sin(a) * r) : g.moveTo(-4 + Math.cos(a) * r, -10 + Math.sin(a) * r); } g.stroke();
    g.restore();
  }

  /** La fourmi noire (insecte) : 3 parties, 3 paires de pattes, antennes coudées. Longueur ≈ 50 k. */
  function fourmi(g, x, y, k = 1, o = {}) {
    const P = []; g.save(); g.translate(x, y); g.scale(k, k); g.globalAlpha *= o.alpha ?? 1;
    for (const px of [-2, 3, 8]) { patte(g, [[px, -3], [px - 4, -14], [px - 10, -20]], 1.3, '#151515'); patte(g, [[px, 3], [px - 4, 14], [px - 10, 20]], 1.3, '#151515'); P.push([px, 0]); }
    patte(g, [[18, -3], [24, -12], [30, -10]], 1.1, '#151515'); patte(g, [[18, 3], [24, 12], [30, 10]], 1.1, '#151515');
    for (const [cx, rx, ry] of [[-16, 10, 7], [3, 7, 4], [16, 5.5, 5]]) { g.fillStyle = rad(g, cx, 0, rx, '#5a5a5a', '#0a0a0a'); g.beginPath(); g.ellipse(cx, 0, rx, ry, 0, 0, TAU); g.fill(); }
    g.restore(); return P.map(([px, py]) => [x + px * k, y + py * k]);
  }

  /** Le lièvre (mégafaune), assis, tourné vers la droite. Hauteur ≈ 70 k. */
  function lievre(g, x, y, k = 1, o = {}) {
    g.save(); g.translate(x, y); g.scale(k, k); g.globalAlpha *= o.alpha ?? 1;
    ombre(g, 0, 2, 34, 5);
    g.fillStyle = rad(g, -6, -22, 30, '#c9a37a', '#6d4c2e'); g.beginPath(); g.ellipse(-6, -20, 28, 20, 0, 0, TAU); g.fill();
    g.fillStyle = rad(g, 18, -40, 14, '#cfa77c', '#755234'); g.beginPath(); g.ellipse(18, -40, 13, 11, .2, 0, TAU); g.fill();
    for (const [dx, a] of [[10, -.25], [16, .05]]) { g.save(); g.translate(dx, -48); g.rotate(a); g.fillStyle = '#8a6440'; g.beginPath(); g.ellipse(0, -18, 5, 18, 0, 0, TAU); g.fill(); g.fillStyle = '#e2b9a0'; g.beginPath(); g.ellipse(0, -18, 2.4, 13, 0, 0, TAU); g.fill(); g.restore(); }
    g.fillStyle = '#111'; g.beginPath(); g.arc(24, -42, 2.3, 0, TAU); g.fill();
    g.fillStyle = '#f2ece4'; g.beginPath(); g.arc(-33, -16, 6, 0, TAU); g.fill();
    g.fillStyle = '#6d4c2e'; g.beginPath(); g.ellipse(-12, -2, 14, 4, 0, 0, TAU); g.fill();
    g.restore();
  }

  /** Une feuille morte (litière), brune ; o.trous 0..1 (rongée), o.nervures : seules les nervures restent. Longueur ≈ 60 k. */
  function feuilleMorte(g, x, y, k = 1, o = {}) {
    const rr = graine(o.graine ?? 5); g.save(); g.translate(x, y); g.rotate(o.angle || 0); g.scale(k, k); g.globalAlpha *= o.alpha ?? 1;
    const forme = () => { g.beginPath(); g.moveTo(-30, 0); g.quadraticCurveTo(-5, -20, 30, 0); g.quadraticCurveTo(-5, 20, -30, 0); g.closePath(); };
    const nerv = (a) => { g.strokeStyle = `rgba(${o.nervures ? '214,186,140' : '90,55,25'},${a})`; g.lineWidth = o.nervures ? 1.6 : 1; g.beginPath(); g.moveTo(-34, 0); g.lineTo(30, 0); for (let i = -3; i <= 3; i++) { if (!i) continue; const px = -15 + Math.abs(i) * 8; g.moveTo(px - 6, 0); g.lineTo(px + 4, Math.sign(i) * (13 - Math.abs(i) * 2.5)); } g.stroke(); };
    if (!o.nervures) {
      forme(); g.fillStyle = rad(g, -4, -4, 30, o.couleur || '#c08a3e', '#6b3f17'); g.fill();
      const tr = o.trous || 0; if (tr > 0) { g.save(); forme(); g.clip(); g.globalCompositeOperation = 'destination-out'; for (let i = 0; i < Math.round(tr * 14); i++) { g.beginPath(); g.arc(-24 + rr() * 48, -9 + rr() * 18, 2 + rr() * 3.5, 0, TAU); g.fill(); } g.restore(); }
      nerv(.7);
    } else nerv(.95);
    g.restore();
  }

  /** Le chêne-liège peint : houppier vert, tronc à l’écorce de liège, racine pivotante (o.racine = longueur sous le sol).
   *  o.etat : 'sain' | 'fletri' (feuillage jauni, clairsemé) | 'asphyxie' (racine brunie). h = hauteur au-dessus du sol. */
  function chene(g, x, ySol, h, o = {}) {
    const et = o.etat || 'sain', rr = graine(o.graine ?? Math.round(x)); g.save(); g.globalAlpha *= o.alpha ?? 1;
    if (o.racine) {
      g.strokeStyle = et === 'asphyxie' ? '#4a3020' : '#b88a5a'; g.lineCap = 'round';
      g.lineWidth = Math.max(2, h * .05); g.beginPath(); g.moveTo(x, ySol); g.quadraticCurveTo(x + 3, ySol + o.racine * .5, x - 2, ySol + o.racine); g.stroke();
      g.lineWidth = Math.max(1, h * .022); for (let i = 1; i <= 4; i++) { const yy = ySol + o.racine * i / 5, s = i % 2 ? 1 : -1, l = (o.tracante ?? .35) * h * (1 - i / 7); g.beginPath(); g.moveTo(x, yy); g.quadraticCurveTo(x + s * l * .6, yy + 4, x + s * l, yy + 12); g.stroke(); }
    }
    const tr = h * .42; g.fillStyle = (() => { const gr = g.createLinearGradient(x - h * .05, 0, x + h * .05, 0); gr.addColorStop(0, '#5b3b22'); gr.addColorStop(.5, '#a77a4c'); gr.addColorStop(1, '#4d3019'); return gr; })();
    g.beginPath(); g.moveTo(x - h * .05, ySol); g.lineTo(x - h * .03, ySol - tr); g.lineTo(x + h * .03, ySol - tr); g.lineTo(x + h * .05, ySol); g.fill();
    const vert = et === 'sain' ? ['#8fd46f', '#2c6e2c'] : et === 'fletri' ? ['#d9c36a', '#7d6a2a'] : ['#a6b46a', '#4b5a26'];
    const n = et === 'sain' ? 7 : 4;
    for (let i = 0; i < n; i++) { const a = rr() * TAU, d = rr() * h * .2, r = h * (.16 + rr() * .08), cx = x + Math.cos(a) * d, cy = ySol - h * .68 + Math.sin(a) * d * .6; g.fillStyle = rad(g, cx, cy, r, vert[0], vert[1]); g.beginPath(); g.arc(cx, cy, r, 0, TAU); g.fill(); }
    g.restore();
  }
  /** Une plantule (jeune plant) : tige et deux feuilles ; o.fletrie 0..1. */
  function plantule(g, x, ySol, h, o = {}) { ST.plante(g, x, ySol, h, { fletrie: o.fletrie || 0, alpha: o.alpha }); }

  /** Mousses et lichens (végétation pionnière) : coussinets verts / plaques gris-vert sur la roche. */
  function mousse(g, x, y, k = 1, o = {}) {
    const rr = graine(o.graine ?? Math.round(x * 3)); g.save(); g.globalAlpha *= o.alpha ?? 1;
    for (let i = 0; i < 7; i++) { const cx = x + (rr() - .5) * 26 * k, cy = y - rr() * 6 * k, r = (4 + rr() * 5) * k; g.fillStyle = rad(g, cx, cy, r, o.lichen ? '#d8dcae' : '#9be06a', o.lichen ? '#7e8a5a' : '#2f7a26'); g.beginPath(); g.arc(cx, cy, r, Math.PI, TAU); g.fill(); }
    g.restore();
  }
  /** Une touffe d’herbe. */
  function herbe(g, x, y, k = 1, o = {}) {
    g.save(); g.globalAlpha *= o.alpha ?? 1; g.strokeStyle = o.sec ? '#b8a25a' : '#5fae47'; g.lineWidth = 1.6 * k; g.lineCap = 'round';
    for (let i = -3; i <= 3; i++) { g.beginPath(); g.moveTo(x + i * 1.5 * k, y); g.quadraticCurveTo(x + i * 3 * k, y - 8 * k, x + i * 5 * k, y - (12 + (3 - Math.abs(i)) * 2) * k); g.stroke(); }
    g.restore();
  }
  /** Un arbre de forêt (forme simple peinte) ; o.coupe : seule la souche reste ; o.brule 0..1 : noirci. */
  function arbre(g, x, ySol, h, o = {}) {
    g.save(); g.globalAlpha *= o.alpha ?? 1;
    if (o.coupe) { g.fillStyle = '#6b4a2a'; g.fillRect(x - h * .06, ySol - h * .1, h * .12, h * .1); g.fillStyle = '#d8b07a'; g.beginPath(); g.ellipse(x, ySol - h * .1, h * .06, h * .02, 0, 0, TAU); g.fill(); g.restore(); return; }
    const b = o.brule || 0;
    g.fillStyle = b > .5 ? '#2a2018' : '#6b4a2a'; g.fillRect(x - h * .035, ySol - h * .45, h * .07, h * .45);
    if (b < .95) { const c0 = b ? `rgb(${Math.round(110 - 70 * b)},${Math.round(190 - 150 * b)},${Math.round(90 - 60 * b)})` : '#7cc95e', c1 = b ? '#1c1a14' : '#24602a';
      g.globalAlpha *= 1 - b * .7; for (const [dx, dy, r] of [[0, -.72, .26], [-.16, -.55, .2], [.16, -.55, .2]]) { g.fillStyle = rad(g, x + dx * h, ySol + dy * h, r * h, c0, c1); g.beginPath(); g.arc(x + dx * h, ySol + dy * h, r * h, 0, TAU); g.fill(); } }
    g.restore();
  }

  /** La lampe (abat-jour et ampoule) ; o.allumee 0..1 : halo de lumière et de chaleur. Largeur ≈ 90 k. */
  function lampe(g, x, y, k = 1, o = {}) {
    const a = o.allumee || 0; g.save(); g.translate(x, y); g.scale(k, k);
    if (a > 0) { const gr = g.createRadialGradient(0, 14, 2, 0, 30, 120); gr.addColorStop(0, `rgba(255,236,150,${.55 * a})`); gr.addColorStop(1, 'rgba(255,200,80,0)'); g.fillStyle = gr; g.beginPath(); g.moveTo(-44, 6); g.lineTo(44, 6); g.lineTo(80, 120); g.lineTo(-80, 120); g.closePath(); g.fill(); }
    g.fillStyle = (() => { const gr = g.createLinearGradient(0, -14, 0, 8); gr.addColorStop(0, '#f1f5f9'); gr.addColorStop(1, '#94a3b8'); return gr; })();
    g.beginPath(); g.moveTo(-10, -14); g.lineTo(10, -14); g.lineTo(46, 6); g.lineTo(-46, 6); g.closePath(); g.fill();
    g.fillStyle = a > 0 ? rad(g, 0, 14, 12, '#fffbe6', '#f6c343', -.2, -.2) : rad(g, 0, 14, 12, '#ffffff', '#cbd5e1');
    if (a > 0) { g.shadowColor = '#fde68a'; g.shadowBlur = 24 * a; }
    g.beginPath(); g.arc(0, 15, 11, 0, TAU); g.fill(); g.restore();
  }

  /** Une boîte de Pétri vue de dessus : verre, contenu (fonction de dessin dans le disque). */
  function petri(g, x, y, r, contenu, o = {}) {
    g.save(); ombre(g, x + r * .05, y + r * .08, r * 1.02, r * .98, .25);
    g.fillStyle = 'rgba(220,235,245,.18)'; g.beginPath(); g.arc(x, y, r, 0, TAU); g.fill();
    if (contenu) { g.save(); g.beginPath(); g.arc(x, y, r * .92, 0, TAU); g.clip(); contenu(g); g.restore(); }
    g.strokeStyle = 'rgba(235,245,255,.85)'; g.lineWidth = 3; g.beginPath(); g.arc(x, y, r, 0, TAU); g.stroke();
    g.strokeStyle = 'rgba(255,255,255,.45)'; g.lineWidth = 2; g.beginPath(); g.arc(x, y, r * .93, -2.6, -1.5); g.stroke();
    g.restore();
  }

  /** Le mycélium : filaments blancs ramifiés qui partent de (x, y) ; u 0..1 = croissance. */
  function mycelium(g, x, y, R, u = 1, o = {}) {
    const rr = graine(o.graine ?? 9); g.save(); g.globalAlpha *= o.alpha ?? 1; g.strokeStyle = 'rgba(250,250,245,.9)'; g.lineCap = 'round';
    const branche = (x0, y0, a, l, n) => { if (n <= 0 || l < 3) return; const x1 = x0 + Math.cos(a) * l, y1 = y0 + Math.sin(a) * l; g.lineWidth = Math.max(.6, n * .45); g.beginPath(); g.moveTo(x0, y0); g.quadraticCurveTo((x0 + x1) / 2 + (rr() - .5) * l * .3, (y0 + y1) / 2 + (rr() - .5) * l * .3, x1, y1); g.stroke();
      branche(x1, y1, a + (rr() - .5) * .9, l * .78, n - 1); if (rr() > .35) branche(x1, y1, a + (rr() > .5 ? .7 : -.7), l * .6, n - 2); };
    const n = Math.max(1, Math.round(u * 5)); for (let i = 0; i < 9; i++) branche(x, y, i / 9 * TAU + rr() * .3, R * .22 * u, n);
    g.restore();
  }
  /** Une bactérie : petit bâtonnet cyan (vue au microscope électronique). */
  function bacterie(g, x, y, k = 1, a = 0, o = {}) {
    g.save(); g.translate(x, y); g.rotate(a); g.scale(k, k); g.globalAlpha *= o.alpha ?? 1;
    g.fillStyle = rad(g, 0, 0, 9, '#c8fbff', '#2a9fb0'); g.beginPath(); if (g.roundRect) g.roundRect(-9, -3.6, 18, 7.2, 3.6); else g.rect(-9, -3.6, 18, 7.2); g.fill();
    g.restore();
  }

  /** Une flamme (incendie), hauteur h, vacillante avec la phase f. */
  function flamme(g, x, y, h, f = 0, a = 1) {
    g.save(); g.globalAlpha *= a; const w = h * .45, dx = Math.sin(f * 7) * h * .06;
    const gr = g.createLinearGradient(0, y, 0, y - h); gr.addColorStop(0, '#f97316'); gr.addColorStop(.6, '#fbbf24'); gr.addColorStop(1, 'rgba(254,240,138,.2)');
    g.fillStyle = gr; g.beginPath(); g.moveTo(x - w, y); g.quadraticCurveTo(x - w * .6, y - h * .6, x + dx, y - h); g.quadraticCurveTo(x + w * .6, y - h * .6, x + w, y); g.closePath(); g.fill(); g.restore();
  }
  /** Une chèvre (surpâturage), tête vers le bas qui broute. Longueur ≈ 60 k. */
  function chevre(g, x, y, k = 1, o = {}) {
    g.save(); g.translate(x, y); g.scale(k * (o.sens || 1), k); g.globalAlpha *= o.alpha ?? 1;
    ombre(g, 0, 2, 26, 4);
    g.fillStyle = '#3a2a20'; for (const px of [-16, -10, 10, 16]) g.fillRect(px - 1.6, -14, 3.2, 14);
    g.fillStyle = rad(g, 0, -20, 24, '#7a5a44', '#2e2018'); g.beginPath(); g.ellipse(0, -20, 22, 10, 0, 0, TAU); g.fill();
    g.fillStyle = '#3e2c22'; g.beginPath(); g.ellipse(26, -8 + (o.broute ? 4 : -10), 7, 5, .7, 0, TAU); g.fill();
    g.strokeStyle = '#3e2c22'; g.lineWidth = 6; g.lineCap = 'round'; g.beginPath(); g.moveTo(18, -22); g.lineTo(25, -8 + (o.broute ? 4 : -10)); g.stroke();
    g.strokeStyle = '#d6cbb8'; g.lineWidth = 1.6; g.beginPath(); g.moveTo(24, -12 + (o.broute ? 4 : -10)); g.lineTo(20, -20 + (o.broute ? 4 : -10)); g.stroke();
    g.restore();
  }
  /** Un nuage de pluie gris. */
  function nuage(g, x, y, k = 1, a = 1) {
    g.save(); g.globalAlpha *= a; for (const [dx, dy, r] of [[-22, 4, 16], [0, -6, 22], [24, 4, 17], [8, 8, 16]]) { g.fillStyle = rad(g, x + dx * k, y + dy * k, r * k, '#e5e7eb', '#6b7280'); g.beginPath(); g.arc(x + dx * k, y + dy * k, r * k, 0, TAU); g.fill(); } g.restore();
  }

  /**
   * Un tableau de données dessiné vide (à la craie) puis rempli en animation (règle 35 de l’utilisateur) :
   *   T = { cle, x, y, cols: [largeurs], lignes: [hauteurs], entetes: [{l, c, texte, couleur?}], cellules: [{l, c, texte, t, de: [x, y], couleur?}],
   *         tTrace, taille }
   * Le cadre s’écrit à `tTrace` ; chaque cellule : à l’instant `t`, sa case s’allume et le nombre vole depuis `de` (là où il a
   * été produit) jusqu’au centre de sa case (0,9 s), puis reste écrit. Renvoie rect(l, c) = la boîte d’une case (repères).
   */
  function tableauAnime(c, ecrit, t, T) {
    const X = [T.x]; T.cols.forEach(w => X.push(X[X.length - 1] + w)); const Y = [T.y]; T.lignes.forEach(h => Y.push(Y[Y.length - 1] + h));
    const rect = (l, k, n = 1) => ({ x: X[k], y: Y[l], w: X[k + n] - X[k], h: Y[l + 1] - Y[l] });
    const taille = T.taille || 18;
    if (t >= T.tTrace) ecrit.ecrire(c, T.cle + '_grille', () => {
      c.rect(X[0], Y[0], X[X.length - 1] - X[0], Y[Y.length - 1] - Y[0], { couleur: 'blanc', largeur: 2, arrondi: 4 });
      for (let i = 1; i < Y.length - 1; i++) c.ligne(X[0], Y[i], X[X.length - 1], Y[i], { couleur: 'faible', largeur: 1.5 });
      for (let i = 1; i < X.length - 1; i++) c.ligne(X[i], Y[0], X[i], Y[Y.length - 1], { couleur: 'faible', largeur: 1.5 });
      (T.entetes || []).forEach(E => { const r = rect(E.l, E.c, E.n || 1); (E.lignes || [E.texte]).forEach((s, j, A) => c.texte(s, r.x + r.w / 2, r.y + r.h / 2 + 6 + (j - (A.length - 1) / 2) * (taille + 2), { couleur: E.couleur || 'cyan', taille, align: 'center', max: r.w - 8 })); });
    });
    (T.cellules || []).forEach((C, i) => {
      if (t < C.t) return;
      const r = rect(C.l, C.c), cx = r.x + r.w / 2, cy = r.y + r.h / 2 + 6, u = ST.doux((t - C.t) / .9);
      if (t < C.t + 1.6) ST.lueur(c, r.x + 3, r.y + 3, r.w - 6, r.h - 6, t < C.t + 1);
      if (u < 1 && C.de) c.direct(() => c.texte(C.texte, ST.mix(C.de[0], cx, u), ST.mix(C.de[1], cy, u), { couleur: C.couleur || 'jaune', taille: taille + 2, align: 'center', gras: true }));
      else c.direct(() => c.texte(C.texte, cx, cy, { couleur: C.couleur || 'jaune', taille, align: 'center', gras: true, max: r.w - 8 }));
    });
    return rect;
  }

  /** Compter en allumant (règle 16) : chaque objet i s’allume à t0 + i·pas, son numéro écrit à côté ; renvoie le compte. */
  function compter(c, t, t0, pas, boites, o = {}) {
    let n = 0;
    boites.forEach((b, i) => {
      const ti = t0 + i * pas; if (t < ti) return; n = i + 1;
      ST.lueur(c, b.x, b.y, b.w, b.h, t < ti + pas || (o.dernier && i === boites.length - 1 && t < ti + 1.2));
      c.direct(() => c.texte(String(i + 1), b.x + b.w + (o.dx ?? 4), b.y + (o.dy ?? 14), { couleur: 'jaune', taille: o.taille || 16, gras: true }));
    });
    return n;
  }

  Object.assign(ST, { campagnol, carabe, acarien, nematode, cloporte, araignee, iule, escargot, fourmi, lievre, feuilleMorte, chene, plantule,
    mousse, herbe, arbre, lampe, petri, mycelium, bacterie, flamme, chevre, nuage, tableauAnime, compter, ombrePeinte: ombre });
})();
