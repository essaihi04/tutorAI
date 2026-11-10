/*
 * Eau peinte de la cuve à ondes — commun à cuve.html, stroboscope.html et fente.html
 * (cours « Ondes mécaniques progressives périodiques », 10 novembre 2026).
 *
 * Règle 7 du skill simulations-au-tableau : le milieu est PEINT (pas dessiné à la craie), dans son cadre seulement.
 * Ce module ne fait que peindre : la page calcule la physique (y = A sin 2πN(t − r/v), bords absorbants, ni
 * amortissement ni réflexion) et lui passe, pour chaque coordonnée u (px), l'élévation h et la pente s normalisées.
 * La teinte d'une ride suit la pente (côté éclairé clair, autre côté sombre), un fin liseré clair marque chaque crête.
 * Un affaiblissement éventuel (amp < 1) est pour l'œil seulement : il ne change ni λ, ni N, ni v.
 *
 * Rendu léger : un dégradé (radial ou linéaire) par couche et par image, jamais de boucle par pixel.
 */
(function () {
  'use strict';
  const EAU = [14, 74, 92], CLAIR = [150, 220, 235], SOMBRE = [4, 30, 42];
  const borne = (k) => Math.max(0, Math.min(1, k));
  const mix = (a, b, k) => a.map((v, i) => Math.round(v + (b[i] - v) * borne(k)));

  /** Couleur d'un anneau d'eau : h = élévation (−1..1), s = pente normalisée (−1..1), amp = amplitude vue (0..1). */
  function teinte(h, s, amp = 1) {
    const p = s * amp, e = h * amp;
    const c = p > 0 ? mix(EAU, CLAIR, p * .95 + e * .18) : mix(EAU, SOMBRE, -p * .95 - e * .1);
    const a = Math.min(.86, Math.abs(p) * .82 + Math.abs(e) * .22);
    return `rgba(${c[0]},${c[1]},${c[2]},${a.toFixed(3)})`;
  }

  /** Chemin du cadre de l'eau (coins arrondis). */
  function chemin(ctx, r) {
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(r.x, r.y, r.w, r.h, 8); else ctx.rect(r.x, r.y, r.w, r.h);
  }

  /** Le fond du bassin (dégradé) et, si `reflets`, des reflets lents du ciel (alpha ≈ 0,035). À appeler clip posé. */
  function fond(ctx, r, o = {}) {
    const g = ctx.createLinearGradient(r.x, r.y, r.x + r.w, r.y + r.h);
    g.addColorStop(0, 'rgb(18,88,108)'); g.addColorStop(.55, 'rgb(12,66,84)'); g.addColorStop(1, 'rgb(8,48,64)');
    ctx.fillStyle = g; ctx.fillRect(r.x, r.y, r.w, r.h);
    if (o.reflets === false) return;
    ctx.save(); ctx.globalAlpha = .035; ctx.fillStyle = '#bfefff';
    const now = o.temps ?? performance.now();
    for (let k = 0; k < 8; k++) {
      const cx = r.x + ((k * 97 + now * .006 * (1 + k % 3)) % (r.w + 80)) - 40, cy = r.y + 26 + (k * 53) % Math.max(20, r.h - 40);
      ctx.beginPath(); ctx.ellipse(cx, cy, 40 + 9 * (k % 4), 7 + 2 * (k % 3), -.35, 0, Math.PI * 2); ctx.fill();
    }
    ctx.restore();
  }

  /**
   * Une couche de rides peinte d'un seul dégradé.
   *   c.forme  'radial' (centre c.x, c.y) ou 'lineaire' (origine x = c.x, propagation vers +x, ou −x si c.sens = −1)
   *   c.umax   étendue du dégradé (px) ; c.pas : écart entre deux arrêts de couleur (px, ~λ/12)
   *   c.onde(u) → { h, s, amp } ou null (eau calme) ; c.zone : rectangle à remplir (le clip limite déjà).
   */
  function rides(ctx, c) {
    const n = Math.max(48, Math.min(720, Math.ceil(c.umax / (c.pas || 2.5))));
    const g = c.forme === 'radial' ? ctx.createRadialGradient(c.x, c.y, 0, c.x, c.y, c.umax) : ctx.createLinearGradient(c.x, 0, c.x + (c.sens || 1) * c.umax, 0);
    for (let k = 0; k <= n; k++) {
      const o = c.onde(c.umax * k / n);
      g.addColorStop(k / n, o ? teinte(o.h, o.s, o.amp ?? 1) : 'rgba(14,74,92,0)');
    }
    ctx.fillStyle = g; ctx.fillRect(c.zone.x, c.zone.y, c.zone.w, c.zone.h);
  }

  /** Les liserés de lumière sur les crêtes : `liste` = [{ u, a }] (u en px depuis l'origine de la couche, a = opacité). */
  function liseres(ctx, c, liste) {
    ctx.save(); ctx.lineWidth = c.largeur || 1.3;
    for (const { u, a } of liste) {
      if (!(u > 0.5) || !(a > .02)) continue;
      ctx.strokeStyle = `rgba(225,250,255,${Math.min(.75, a).toFixed(3)})`; ctx.beginPath();
      if (c.forme === 'radial') ctx.arc(c.x - .8, c.y - .8, u, 0, Math.PI * 2);
      else { const x = c.x + (c.sens || 1) * u - .8; ctx.moveTo(x, c.zone.y); ctx.lineTo(x, c.zone.y + c.zone.h); }
      ctx.stroke();
    }
    ctx.restore();
  }

  /*
   * Couche masquée selon l'angle (onde diffractée : plus faible sur les côtés). On peint la couche sur un calque,
   * on n'en garde que la part donnée par un dégradé conique, puis on pose le calque sur le canvas. Un calque, un
   * dégradé conique : rien par pixel. `m` = { x, y, depart (rad), alpha(θ) → 0..1 }.
   */
  let calque = null;
  function masque(ctx, dessiner, m) {
    const cv = ctx.canvas;
    if (!calque) calque = document.createElement('canvas');
    if (calque.width !== cv.width || calque.height !== cv.height) { calque.width = cv.width; calque.height = cv.height; }
    const o = calque.getContext('2d');
    o.setTransform(1, 0, 0, 1, 0, 0); o.clearRect(0, 0, calque.width, calque.height);
    o.setTransform(ctx.getTransform());
    o.save(); dessiner(o); o.restore();
    if (o.createConicGradient) {
      o.globalCompositeOperation = 'destination-in';
      const g = o.createConicGradient(m.depart, m.x, m.y), N = 72;
      for (let k = 0; k <= N; k++) g.addColorStop(k / N, `rgba(0,0,0,${borne(m.alpha(m.depart + 2 * Math.PI * k / N)).toFixed(3)})`);
      o.fillStyle = g; o.fillRect(-4000, -4000, 8000, 8000);
      o.globalCompositeOperation = 'source-over';
    }
    ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.drawImage(calque, 0, 0); ctx.restore();
  }

  /** Assombrit l'eau (pièce noire, stroboscope) : `a` = 0 (éclairée) … 1 (noir complet). */
  function nuit(ctx, r, a) {
    if (a <= 0) return;
    ctx.save(); chemin(ctx, r); ctx.fillStyle = `rgba(2,8,12,${borne(a).toFixed(3)})`; ctx.fill(); ctx.restore();
  }

  /*
   * Vue de côté (coupe) : une tranche d'eau remplie sous la surface (claire en haut, sombre en profondeur) et un
   * liseré clair sur la surface. z = { x0, x1, y (niveau au repos), bas, k (px pour une élévation 1) } ; f(x) → élévation.
   */
  function cote(ctx, z, f, n = 240) {
    ctx.save();
    ctx.beginPath(); ctx.moveTo(z.x0, z.bas);
    for (let i = 0; i <= n; i++) { const x = z.x0 + (z.x1 - z.x0) * i / n; ctx.lineTo(x, z.y - z.k * f(x)); }
    ctx.lineTo(z.x1, z.bas); ctx.closePath();
    const g = ctx.createLinearGradient(0, z.y - z.k, 0, z.bas);
    g.addColorStop(0, 'rgba(60,170,200,.8)'); g.addColorStop(.35, 'rgba(18,96,122,.86)'); g.addColorStop(1, 'rgba(6,40,56,.93)');
    ctx.fillStyle = g; ctx.fill();
    ctx.beginPath();
    for (let i = 0; i <= n; i++) { const x = z.x0 + (z.x1 - z.x0) * i / n, y = z.y - z.k * f(x); i ? ctx.lineTo(x, y) : ctx.moveTo(x, y); }
    ctx.strokeStyle = 'rgba(200,245,255,.9)'; ctx.lineWidth = 2; ctx.stroke();
    // Le fond de la cuve (verre), sous l'eau.
    ctx.fillStyle = 'rgba(190,215,225,.35)'; ctx.fillRect(z.x0 - 4, z.bas, z.x1 - z.x0 + 8, 4);
    ctx.restore();
  }

  // ── Objets peints (métal, plastique) ─────────────────────────────────────
  function metal(ctx, x0, y0, x1, y1) {
    const g = ctx.createLinearGradient(x0, y0, x1, y1);
    g.addColorStop(0, '#d5dde3'); g.addColorStop(.45, '#8d99a3'); g.addColorStop(1, '#4b5660'); return g;
  }
  /** Le boîtier du vibreur, vu de dessus ou de côté. */
  function boitier(ctx, x, y, w, h) {
    ctx.save();
    ctx.fillStyle = 'rgba(0,10,16,.35)'; ctx.fillRect(x + 3, y + 4, w, h);
    const g = ctx.createLinearGradient(x, y, x, y + h); g.addColorStop(0, '#5b6670'); g.addColorStop(1, '#2c343b');
    ctx.fillStyle = g; ctx.beginPath(); if (ctx.roundRect) ctx.roundRect(x, y, w, h, 4); else ctx.rect(x, y, w, h); ctx.fill();
    ctx.fillStyle = 'rgba(255,255,255,.18)'; ctx.fillRect(x + 3, y + 2, w - 6, 2);
    ctx.restore();
  }
  /** Bras horizontal du vibreur (de (x0,y) à (x1,y)), vu de dessus. */
  function bras(ctx, x0, x1, y, e = 5) {
    ctx.save(); ctx.fillStyle = 'rgba(0,10,16,.3)'; ctx.fillRect(Math.min(x0, x1) + 3, y - e / 2 + 4, Math.abs(x1 - x0), e);
    ctx.fillStyle = metal(ctx, 0, y - e / 2, 0, y + e / 2); ctx.fillRect(Math.min(x0, x1), y - e / 2, Math.abs(x1 - x0), e); ctx.restore();
  }
  /** La pointe du vibreur vue de dessus : une petite bille de métal qui touche l'eau en S. */
  function pointe(ctx, x, y, r = 5) {
    ctx.save();
    ctx.fillStyle = 'rgba(0,15,25,.35)'; ctx.beginPath(); ctx.ellipse(x + 2, y + 3, r * 1.1, r * .8, 0, 0, Math.PI * 2); ctx.fill();
    const g = ctx.createRadialGradient(x - r * .35, y - r * .4, r * .1, x, y, r);
    g.addColorStop(0, '#ffffff'); g.addColorStop(.35, '#b9c3cb'); g.addColorStop(1, '#4b5660');
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.fill(); ctx.restore();
  }
  /** La réglette vue de dessus : une lame de métal posée dans l'eau, de y0 à y1, à l'abscisse x. */
  function reglette(ctx, x, y0, y1, e = 6) {
    ctx.save(); ctx.fillStyle = 'rgba(0,15,25,.35)'; ctx.fillRect(x - e / 2 + 3, y0 + 3, e, y1 - y0);
    ctx.fillStyle = metal(ctx, x - e / 2, 0, x + e / 2, 0); ctx.fillRect(x - e / 2, y0, e, y1 - y0);
    ctx.fillStyle = 'rgba(255,255,255,.35)'; ctx.fillRect(x - e / 2 + 1, y0, 1.2, y1 - y0); ctx.restore();
  }
  /** Vue de côté : la tige du vibreur (ou la tranche de la réglette) qui plonge dans l'eau. */
  function tige(ctx, x, yHaut, yBas, e = 4) {
    ctx.save(); ctx.fillStyle = metal(ctx, x - e / 2, 0, x + e / 2, 0); ctx.fillRect(x - e / 2, yHaut, e, yBas - yHaut);
    ctx.restore();
  }
  /** Une paroi (obstacle) vue de dessus : un bloc de plexiglas sombre de x à x + e, de y0 à y1. */
  function paroi(ctx, x, y0, y1, e = 10) {
    if (y1 - y0 < 1) return;
    ctx.save(); ctx.fillStyle = 'rgba(0,12,20,.4)'; ctx.fillRect(x + 3, y0 + 3, e, y1 - y0);
    const g = ctx.createLinearGradient(x, 0, x + e, 0); g.addColorStop(0, '#9aa7b1'); g.addColorStop(.5, '#6c7883'); g.addColorStop(1, '#3d4750');
    ctx.fillStyle = g; ctx.fillRect(x, y0, e, y1 - y0);
    ctx.fillStyle = 'rgba(255,255,255,.3)'; ctx.fillRect(x + 1, y0, 1.4, y1 - y0); ctx.restore();
  }
  /*
   * Une règle transparente posée sur l'eau, horizontale : le zéro sous xa, graduée en cm et demi-cm (pxCm px par cm),
   * bord gradué en y (les graduations descendent). `a` = opacité (la règle glisse en place).
   */
  function regle(ctx, xa, xb, y, pxCm, a = 1, marge = 14) {
    const x0 = xa - marge, x1 = xb + marge, h = 22;
    ctx.save(); ctx.globalAlpha = a;
    ctx.fillStyle = 'rgba(0,10,16,.25)'; ctx.fillRect(x0 + 3, y + 3, x1 - x0, h);
    const g = ctx.createLinearGradient(0, y, 0, y + h); g.addColorStop(0, 'rgba(250,246,225,.86)'); g.addColorStop(1, 'rgba(225,218,190,.78)');
    ctx.fillStyle = g; ctx.fillRect(x0, y, x1 - x0, h);
    ctx.strokeStyle = 'rgba(60,50,30,.85)'; ctx.lineWidth = 1; ctx.beginPath();
    const n = Math.floor((x1 - xa) / (pxCm / 2));
    for (let i = -Math.floor(marge / (pxCm / 2)); i <= n; i++) {
      const x = xa + i * pxCm / 2, l = i % 2 === 0 ? 8 : 4.5;
      if (x < x0 + 1 || x > x1 - 1) continue;
      ctx.moveTo(x, y); ctx.lineTo(x, y + l);
    }
    ctx.stroke();
    ctx.fillStyle = 'rgba(50,40,20,.95)'; ctx.font = '11px sans-serif'; ctx.textAlign = 'center';
    for (let i = 0; xa + i * pxCm <= x1 - 4; i++) ctx.fillText(String(i), xa + i * pxCm, y + h - 3);
    ctx.restore();
  }
  /** Une molette peinte (réglage) : centre, rayon, angle de l'encoche. */
  function molette(ctx, x, y, r, angle) {
    ctx.save();
    ctx.fillStyle = 'rgba(0,10,16,.35)'; ctx.beginPath(); ctx.arc(x + 2, y + 3, r, 0, Math.PI * 2); ctx.fill();
    const g = ctx.createRadialGradient(x - r * .3, y - r * .35, r * .1, x, y, r);
    g.addColorStop(0, '#9aa5ae'); g.addColorStop(1, '#2f373e');
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = '#facc15'; ctx.lineWidth = 2.4; ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + r * .8 * Math.cos(angle), y + r * .8 * Math.sin(angle)); ctx.stroke();
    ctx.restore();
  }
  /** La lampe du stroboscope ; `eclat` (0..1) : lueur de l'éclair. */
  function lampe(ctx, x, y, eclat) {
    ctx.save();
    boitier(ctx, x - 34, y - 20, 68, 40);
    const g = ctx.createRadialGradient(x - 40, y, 2, x - 40, y, 16);
    g.addColorStop(0, eclat > .05 ? '#ffffff' : '#7d8a94'); g.addColorStop(1, eclat > .05 ? 'rgba(255,250,220,.9)' : '#38424a');
    ctx.fillStyle = g; ctx.beginPath(); ctx.ellipse(x - 38, y, 8, 15, 0, 0, Math.PI * 2); ctx.fill();
    if (eclat > .02) {
      const h = ctx.createRadialGradient(x - 40, y, 4, x - 40, y, 120);
      h.addColorStop(0, `rgba(255,252,230,${(.75 * eclat).toFixed(3)})`); h.addColorStop(1, 'rgba(255,252,230,0)');
      ctx.fillStyle = h; ctx.beginPath(); ctx.arc(x - 40, y, 120, 0, Math.PI * 2); ctx.fill();
    }
    ctx.restore();
  }

  window.EauPeinte = { teinte, chemin, fond, rides, liseres, masque, nuit, cote, boitier, bras, pointe, reglette, tige, paroi, regle, molette, lampe };
})();
