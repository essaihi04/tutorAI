/*
 * Filaments peints du sarcomère (cours « Rôle du muscle strié squelettique », 10 novembre 2026).
 * Règle 7 : le vivant est PEINT avec le canvas brut, avant la craie.
 *   - actine : deux chapelets de perles rouge-orangé enroulés l'un autour de l'autre (filament fin) ;
 *   - myosine : bâtonnet bleu à têtes renflées, sans têtes au milieu (filament épais) ;
 *   - strie Z : trait sombre en zigzag ;
 *   - électronographie : bandes grises dont la densité suit les filaments présents
 *     (rien : très clair ; actine seule : clair ; myosine seule : gris moyen ; actine + myosine : sombre ; strie Z : noir).
 * Les perles et les têtes sont des petites images préparées une fois (pas de dégradé par perle à chaque image).
 * Unités : µm pour la géométrie (`geo`), px du dessin pour le tracé (X(u) = cx + u·k).
 */
(function () {
  'use strict';
  const ACTINE = 1.0, MYOSINE = 1.5;       // longueurs constantes (µm)

  function sprite(w, h, peindre) {
    const k = 4, c = document.createElement('canvas'); c.width = w * k; c.height = h * k;
    const x = c.getContext('2d'); x.scale(k, k); peindre(x, w, h); return c;
  }
  const perle = (gris) => sprite(8, 8, (x) => {
    const g = x.createRadialGradient(2.9, 2.6, .3, 4, 4, 4);
    if (gris) { g.addColorStop(0, '#e5e5e5'); g.addColorStop(.55, '#a3a3a3'); g.addColorStop(1, '#5c5c5c'); }
    else { g.addColorStop(0, '#ffd0b0'); g.addColorStop(.45, '#f26a2e'); g.addColorStop(1, '#9a2c0c'); }
    x.fillStyle = g; x.beginPath(); x.arc(4, 4, 3.85, 0, Math.PI * 2); x.fill();
  });
  const tete = (gris) => sprite(12, 8, (x) => {
    const g = x.createRadialGradient(5, 3, .4, 6, 4, 6);
    if (gris) { g.addColorStop(0, '#ececec'); g.addColorStop(.5, '#a8a8a8'); g.addColorStop(1, '#626262'); }
    else { g.addColorStop(0, '#dbeafe'); g.addColorStop(.45, '#4f8ef7'); g.addColorStop(1, '#1e3a8a'); }
    x.fillStyle = g; x.beginPath(); x.ellipse(6, 4, 5.6, 3.4, 0, 0, Math.PI * 2); x.fill();
  });
  let SP = null;
  // Les petites images sont vérifiées une fois : si le navigateur les a rendues vides (canvas pas encore prêt), on les refait.
  function sprites() {
    if (SP && SP.ok) return SP;
    SP = { perle: perle(false), perleG: perle(true), tete: tete(false), teteG: tete(true), grain: grain() };
    try { SP.ok = SP.perle.getContext('2d').getImageData(16, 16, 1, 1).data[3] > 0 && SP.tete.getContext('2d').getImageData(24, 16, 1, 1).data[3] > 0; } catch (_) { SP.ok = true; }
    return SP;
  }
  function grain() {
    // Grain de la photo : un petit motif aléatoire préparé une fois, posé en motif très léger.
    const c = document.createElement('canvas'); c.width = c.height = 64; const x = c.getContext('2d');
    let s = 12345; const r = () => ((s = (Math.imul(s, 1664525) + 1013904223) >>> 0) / 4294967296);
    for (let i = 0; i < 700; i++) { const v = Math.round(r() * 255); x.fillStyle = `rgba(${v},${v},${v},.5)`; x.fillRect(r() * 64, r() * 64, 1.2, 1.2); }
    return c;
  }

  /** Filament fin d'actine de xa à xb (px), centré sur y : deux chapelets torsadés. */
  function actine(ctx, xa, xb, y, o = {}) {
    const S = sprites(), img = o.gris ? S.perleG : S.perle, pas = 5.2, n = Math.floor(Math.abs(xb - xa) / pas), sens = xb >= xa ? 1 : -1;
    const amp = 2.3, periode = 34, r = 3.1, arriere = [], avant = [];
    for (let i = 0; i <= n; i++) {
      const x = xa + sens * i * pas, ph = (i * pas) / periode * Math.PI * 2 + (o.phase || 0);
      for (const brin of [0, 1]) {
        const a = ph + brin * Math.PI, yy = y + amp * Math.sin(a), devant = Math.cos(a) > 0;
        (devant ? avant : arriere).push([x + (brin ? pas / 2 : 0) * sens, yy]);
      }
    }
    ctx.save(); ctx.globalAlpha = (o.alpha ?? 1) * .78;
    for (const [x, yy] of arriere) ctx.drawImage(img, x - r * .86, yy - r * .86, 2 * r * .86, 2 * r * .86);
    ctx.globalAlpha = o.alpha ?? 1;
    for (const [x, yy] of avant) ctx.drawImage(img, x - r, yy - r, 2 * r, 2 * r);
    ctx.restore();
  }

  /** Filament épais de myosine de xa à xb (px) : bâtonnet bleu, têtes tournées vers les bouts, milieu nu. */
  function myosine(ctx, xa, xb, y, o = {}) {
    const S = sprites(), img = o.gris ? S.teteG : S.tete, x1 = Math.min(xa, xb), x2 = Math.max(xa, xb), m = (x1 + x2) / 2, L = x2 - x1;
    ctx.save(); ctx.globalAlpha = o.alpha ?? 1;
    const g = ctx.createLinearGradient(0, y - 3.5, 0, y + 3.5);
    if (o.gris) { g.addColorStop(0, '#d4d4d4'); g.addColorStop(.5, '#8a8a8a'); g.addColorStop(1, '#4a4a4a'); }
    else { g.addColorStop(0, '#93c5fd'); g.addColorStop(.45, '#2f6fe0'); g.addColorStop(1, '#1e3a8a'); }
    // Têtes : de part et d'autre, tournées vers la strie Z la plus proche (inclinées vers le bout du filament).
    const nu = L * .1, pas = 8.6;
    ctx.strokeStyle = o.gris ? '#7a7a7a' : '#2b5fc4'; ctx.lineWidth = 1.3;
    for (const cote of [-1, 1]) {
      for (let d = nu, i = 0; d < L / 2 - 2; d += pas, i++) {
        const x = m + cote * d, haut = i % 2 ? -1 : 1, nx = x + cote * 4.2, ny = y + haut * 6.2;
        ctx.beginPath(); ctx.moveTo(x, y + haut * 2); ctx.lineTo(nx, ny); ctx.stroke();
        ctx.save(); ctx.translate(nx + cote * 1.6, ny + haut * .8); ctx.rotate(cote * haut * .55); ctx.drawImage(img, -4.2, -2.6, 8.4, 5.2); ctx.restore();
      }
    }
    ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(x1, y - 3.3, L, 6.6, 3.3); ctx.fill();
    ctx.restore();
  }

  /** Strie Z peinte : trait sombre en zigzag de y1 à y2 (ou horizontal si `horizontal`). */
  function strieZ(ctx, x, y1, y2, o = {}) {
    ctx.save(); ctx.globalAlpha = o.alpha ?? 1; ctx.lineJoin = 'round';
    const pts = []; for (let y = y1, i = 0; y <= y2 + .1; y += 5, i++) pts.push([x + (i % 2 ? 2.6 : -2.6), y]);
    for (const [w, col] of [[4.4, o.gris ? '#3a3a3a' : '#2a2140'], [1.4, o.gris ? '#8a8a8a' : '#8b7bb8']]) {
      ctx.strokeStyle = col; ctx.lineWidth = w; ctx.beginPath(); pts.forEach(([a, b], i) => (i ? ctx.lineTo(a, b) : ctx.moveTo(a, b))); ctx.stroke();
    }
    ctx.restore();
  }

  /** Géométrie d'un sarcomère de longueur L (µm), la myosine fixe au centre (u = 0) ; voisins compris. */
  function geo(L) {
    const zl = -L / 2, zr = L / 2;
    return {
      L, z: [zl, zr],
      actine: [[zl - ACTINE, zl], [zl, zl + ACTINE], [zr - ACTINE, zr], [zr, zr + ACTINE]],
      myosine: [[-MYOSINE / 2, MYOSINE / 2], [-L - MYOSINE / 2, -L + MYOSINE / 2], [L - MYOSINE / 2, L + MYOSINE / 2]],
      A: MYOSINE, I: L - MYOSINE, H: Math.max(0, L - 2 * ACTINE),
    };
  }
  /** Même motif répété : sarcomères centrés en m·L pour m = −n..n (une myofibrille entière). */
  function geoPeriodique(L, n) {
    const G = { L, z: [], actine: [], myosine: [], A: MYOSINE, I: L - MYOSINE, H: Math.max(0, L - 2 * ACTINE) };
    for (let m = -n; m <= n; m++) {
      const c = m * L; G.myosine.push([c - MYOSINE / 2, c + MYOSINE / 2]);
      const z = c + L / 2; G.z.push(z); G.actine.push([z - ACTINE, z], [z, z + ACTINE]);
      if (m === -n) { const z0 = c - L / 2; G.z.push(z0); G.actine.push([z0 - ACTINE, z0], [z0, z0 + ACTINE]); }
    }
    return G;
  }
  const dans = (u, iv) => iv.some(([a, b]) => u > a && u < b);

  /**
   * Électronographie : bande grise de x0 à x1 (px), hauteur h ; `G` = géométrie en µm ; X(u) → px.
   * `present` : {actine, myosine} (construire : les filaments pas encore posés ne foncent pas la bande).
   */
  function electro(ctx, x0, x1, y, h, G, X, o = {}) {
    const S = sprites(), pr = o.present || { actine: 1, myosine: 1, z: 1 };
    const cuts = new Set([x0, x1]);
    for (const iv of [...G.actine, ...G.myosine]) for (const u of iv) { const x = X(u); if (x > x0 && x < x1) cuts.add(x); }
    const xs = [...cuts].sort((a, b) => a - b);
    ctx.save(); ctx.globalAlpha = o.alpha ?? 1;
    ctx.beginPath(); ctx.rect(x0, y, x1 - x0, h); ctx.clip();
    const niveau = (a, m) => 214 - 40 * a - 90 * m - (a > 0 && m > 0 ? 34 * Math.min(a, m) : 0);   // gris 0..255
    for (let i = 0; i < xs.length - 1; i++) {
      const xa = xs[i], xb = xs[i + 1]; if (xb - xa < .2) continue;
      const u = ((xa + xb) / 2 - X(0)) / ((X(1) - X(0)) || 1);
      const a = dans(u, G.actine) ? pr.actine : 0, m = dans(u, G.myosine) ? pr.myosine : 0, v = niveau(a, m);
      const g = ctx.createLinearGradient(0, y, 0, y + h);
      const c = (d) => { const w = Math.max(0, Math.min(255, Math.round(v + d))); return `rgb(${w},${w},${w})`; };
      g.addColorStop(0, c(-18)); g.addColorStop(.5, c(10)); g.addColorStop(1, c(-24));
      ctx.fillStyle = g; ctx.fillRect(xa, y, xb - xa + .6, h);
    }
    if (pr.z) {
      ctx.globalAlpha = (o.alpha ?? 1) * pr.z;
      for (const z of G.z) { const x = X(z); ctx.fillStyle = '#1b1b1b'; ctx.fillRect(x - 1.6, y, 3.2, h); }
    }
    ctx.globalAlpha = (o.alpha ?? 1) * .22; ctx.fillStyle = ctx.createPattern(S.grain, 'repeat'); ctx.fillRect(x0, y, x1 - x0, h);
    ctx.restore();
  }

  /** Estompe les bords gauche et droit d'une zone déjà peinte (le filament continue au-delà). */
  function estomper(ctx, x0, x1, y0, y1, l = 26) {
    ctx.save(); ctx.globalCompositeOperation = 'destination-out';
    for (const [a, b] of [[x0, x0 + l], [x1, x1 - l]]) {
      const g = ctx.createLinearGradient(a, 0, b, 0); g.addColorStop(0, 'rgba(0,0,0,1)'); g.addColorStop(1, 'rgba(0,0,0,0)');
      ctx.fillStyle = g; ctx.fillRect(Math.min(a, b) - 1, y0, l + 1, y1 - y0);
    }
    ctx.restore();
  }

  /**
   * Un bloc « sarcomère » : filaments (rangées actine / myosine alternées), stries Z, avec voisins coupés.
   *   o = { cx, k (px/µm), L, W (demi-largeur de la fenêtre, µm), rangs: [{y, type:'actine'|'myosine'}], zy1, zy2,
   *         gris, alpha, actine: part 0..1 (pousse depuis les stries Z), myosine: 0..1 (apparaît), z: 0..1 }
   */
  function bloc(ctx, o) {
    const G = geo(o.L), X = (u) => o.cx + u * o.k, x0 = X(-o.W), x1 = X(o.W);
    const pa = o.actine ?? 1, pm = o.myosine ?? 1, pz = o.z ?? 1;
    ctx.save(); ctx.beginPath(); ctx.rect(x0, o.zy1 - 12, x1 - x0, o.zy2 - o.zy1 + 24); ctx.clip();
    for (const r of o.rangs) {
      if (r.type === 'myosine' && pm > 0) {
        for (const [a, b] of G.myosine) myosine(ctx, X(a), X(b), r.y + (1 - pm) * -14, { gris: o.gris, alpha: (o.alpha ?? 1) * pm });
      }
    }
    for (const r of o.rangs) {
      if (r.type === 'actine' && pa > 0) {
        for (const z of G.z) for (const s of [-1, 1]) actine(ctx, X(z), X(z + s * ACTINE * pa), r.y, { gris: o.gris, alpha: o.alpha, phase: z * 3 + (s > 0 ? 0 : 1.3) + r.y * .07 });
      }
    }
    if (pz > 0) for (const z of G.z) strieZ(ctx, X(z), o.zy1, o.zy2, { gris: o.gris, alpha: (o.alpha ?? 1) * pz });
    ctx.restore();
    if (o.estompe !== false) estomper(ctx, x0, x1, o.zy1 - 14, o.zy2 + 14);
    return { G, X, x0, x1 };
  }

  window.Filaments = { ACTINE, MYOSINE, actine, myosine, strieZ, geo, geoPeriodique, electro, estomper, bloc };
})();
