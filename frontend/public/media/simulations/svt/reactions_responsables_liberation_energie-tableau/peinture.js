/*
 * Milieux vivants PEINTS du cours « Libération de l'énergie » (règle 7 du skill simulations-au-tableau, 9 novembre 2026) :
 * la cellule, son hyaloplasme, la mitochondrie (deux membranes, crêtes, matrice), la membrane interne (double couche),
 * les protéines de la membrane, la sphère pédonculée, une solution dans un bécher, des levures, des molécules en billes.
 * La craie reste pour les légendes, les flèches, les axes : on peint d'abord le milieu, puis la craie par-dessus.
 *
 * Ce module ne fait que peindre, avec le contexte brut (`craie.ctx`, dans `craie.direct`). Un dégradé par objet,
 * jamais de boucle par pixel. Les petites granulations sont tirées d'un générateur déterministe : l'image ne
 * scintille pas d'une image à l'autre. Rien n'est hors programme : aucun nom de complexe, aucune molécule nommée.
 */
(function () {
  'use strict';
  const TAU = Math.PI * 2;
  function graine(seed) { let s = (seed >>> 0) || 1; return () => { s = (Math.imul(s, 1664525) + 1013904223) >>> 0; return s / 4294967296; }; }
  const rgba = (c, a) => `rgba(${c[0]},${c[1]},${c[2]},${a})`;

  /* Les teintes (lisibles sur le tableau vert sombre, jamais plus claires que la craie). */
  /* Palette ravivée le 16 novembre 2026 (« couleurs vives, agréables ») : hyaloplasme vert d'eau frais, mitochondrie corail
   * à matrice bleu lumineux, membranes dorées. */
  const T = {
    hyalo: [96, 200, 150], membrane: [250, 204, 96], noyau: [150, 110, 220],
    mitoExt: [240, 100, 62], mitoEsp: [255, 176, 110], matrice: [86, 180, 236], crete: [255, 222, 150],
    proteine: [160, 120, 240], sphere: [252, 196, 70], eau: [60, 160, 210], levure: [236, 200, 130],
  };


  /** Une cellule vue en coupe : membrane plasmique, hyaloplasme granuleux, noyau facultatif ({noyau: {x, y, r}}). */
  function cellule(ctx, cx, cy, rx, ry, o = {}) {
    const r = graine(o.graine || 11), ang = o.angle || 0, R = Math.max(rx, ry);
    ctx.save();
    // ombre douce : la cellule est posée sur le tableau
    ctx.save(); ctx.shadowColor = 'rgba(0,0,0,.45)'; ctx.shadowBlur = 18; ctx.shadowOffsetY = 6;
    ctx.fillStyle = 'rgba(12,40,30,.55)'; ctx.beginPath(); ctx.ellipse(cx, cy, rx, ry, ang, 0, TAU); ctx.fill(); ctx.restore();
    ctx.beginPath(); ctx.ellipse(cx, cy, rx, ry, ang, 0, TAU);
    const g = ctx.createRadialGradient(cx - rx * .3, cy - ry * .35, 4, cx, cy, R);
    g.addColorStop(0, rgba([170, 240, 200], .50)); g.addColorStop(.55, rgba(T.hyalo, .36)); g.addColorStop(1, rgba([40, 130, 110], .34));
    ctx.fillStyle = g; ctx.fill();
    ctx.clip();
    // granulations du hyaloplasme
    ctx.fillStyle = rgba([220, 255, 230], .20);
    for (let k = 0; k < (o.grains ?? 90); k++) {
      const a = r() * TAU, d = Math.sqrt(r()), x = cx + Math.cos(a) * rx * d, y = cy + Math.sin(a) * ry * d;
      ctx.beginPath(); ctx.arc(x, y, .8 + r() * 1.6, 0, TAU); ctx.fill();
    }
    // reflet large en haut à gauche (volume)
    const h = ctx.createRadialGradient(cx - rx * .4, cy - ry * .5, 2, cx - rx * .4, cy - ry * .5, R * .7);
    h.addColorStop(0, 'rgba(255,255,255,.14)'); h.addColorStop(1, 'rgba(255,255,255,0)'); ctx.fillStyle = h; ctx.fillRect(cx - R, cy - R, 2 * R, 2 * R);
    if (o.noyau) {
      const n = o.noyau, gn = ctx.createRadialGradient(n.x - n.r * .3, n.y - n.r * .3, 2, n.x, n.y, n.r);
      gn.addColorStop(0, rgba([210, 180, 255], .85)); gn.addColorStop(.6, rgba(T.noyau, .7)); gn.addColorStop(1, rgba([90, 60, 160], .7));
      ctx.fillStyle = gn; ctx.beginPath(); ctx.arc(n.x, n.y, n.r, 0, TAU); ctx.fill();
      ctx.strokeStyle = rgba([225, 205, 255], .7); ctx.lineWidth = 2; ctx.stroke();
      ctx.fillStyle = rgba([80, 40, 140], .55); ctx.beginPath(); ctx.arc(n.x + n.r * .25, n.y + n.r * .15, n.r * .28, 0, TAU); ctx.fill();   // nucléole
    }
    ctx.restore();
    // membrane plasmique : un liseré doré net, doublé d'un trait fin
    ctx.save(); ctx.lineWidth = 3; ctx.strokeStyle = rgba(T.membrane, .95);
    ctx.beginPath(); ctx.ellipse(cx, cy, rx, ry, ang, 0, TAU); ctx.stroke();
    ctx.lineWidth = 1; ctx.strokeStyle = rgba([255, 240, 190], .5);
    ctx.beginPath(); ctx.ellipse(cx, cy, Math.max(1, rx - 4), Math.max(1, ry - 4), ang, 0, TAU); ctx.stroke();
    ctx.restore();
  }

  /** Chemin de la membrane interne repliée en crêtes, à l'intérieur d'une mitochondrie (cx, cy, rx, ry). */
  function cheminCretes(ctx, cx, cy, rx, ry, n) {
    const ix = rx - 9, iy = ry - 9, prof = iy * .78;
    ctx.beginPath();
    const N = 240;
    for (let i = 0; i <= N; i++) {
      const a = i / N * TAU;
      let x = cx + Math.cos(a) * ix, y = cy + Math.sin(a) * iy;
      // les crêtes : la membrane s'enfonce vers le centre par endroits, alternativement du haut et du bas
      const u = (Math.cos(a) + 1) / 2;                       // 0..1 de gauche à droite
      const k = u * n, frac = k - Math.floor(k), dent = Math.max(0, 1 - Math.abs(frac - .5) * 5);
      const haut = Math.sin(a) < 0, pair = Math.floor(k) % 2 === 0;
      if ((haut && pair) || (!haut && !pair)) { const f = dent * prof * (1 - Math.abs(Math.cos(a)) * .5); y = y + (haut ? f : -f); }
      i ? ctx.lineTo(x, y) : ctx.moveTo(x, y);
    }
    ctx.closePath();
  }

  /** Une mitochondrie en coupe longitudinale : membrane externe, espace intermembranaire, membrane interne en crêtes, matrice. */
  function mitochondrie(ctx, cx, cy, rx, ry, o = {}) {
    const n = o.cretes ?? 7, r = graine(o.graine || 5);
    ctx.save();
    if (o.angle) { ctx.translate(cx, cy); ctx.rotate(o.angle); ctx.translate(-cx, -cy); }
    // membrane externe et espace intermembranaire (ombre portée douce : l'organite a du volume)
    ctx.save(); ctx.shadowColor = 'rgba(0,0,0,.45)'; ctx.shadowBlur = Math.min(14, ry * .5); ctx.shadowOffsetY = Math.min(5, ry * .18);
    ctx.fillStyle = 'rgba(90,30,15,.9)'; ctx.beginPath(); ctx.ellipse(cx, cy, rx, ry, 0, 0, TAU); ctx.fill(); ctx.restore();
    ctx.beginPath(); ctx.ellipse(cx, cy, rx, ry, 0, 0, TAU);
    const g = ctx.createLinearGradient(cx, cy - ry, cx, cy + ry);
    g.addColorStop(0, rgba([255, 205, 140], .95)); g.addColorStop(.5, rgba(T.mitoEsp, .92)); g.addColorStop(1, rgba(T.mitoExt, .92));
    ctx.fillStyle = g; ctx.fill();
    ctx.lineWidth = Math.max(1.6, Math.min(3, ry * .12)); ctx.strokeStyle = rgba([200, 60, 30], 1); ctx.stroke();
    // matrice (à l'intérieur de la membrane interne)
    cheminCretes(ctx, cx, cy, rx, ry, n);
    const gm = ctx.createRadialGradient(cx - rx * .25, cy - ry * .3, 3, cx, cy, Math.max(rx, ry));
    gm.addColorStop(0, rgba([170, 225, 255], .96)); gm.addColorStop(.6, rgba(T.matrice, .92)); gm.addColorStop(1, rgba([40, 110, 180], .92));
    ctx.fillStyle = gm; ctx.fill();
    ctx.lineWidth = Math.max(1.2, Math.min(2.4, ry * .1)); ctx.strokeStyle = rgba(T.crete, 1); ctx.stroke();
    // granules de la matrice
    ctx.save(); cheminCretes(ctx, cx, cy, rx, ry, n); ctx.clip(); ctx.fillStyle = rgba([235, 248, 255], .30);
    for (let k = 0; k < (o.grains ?? Math.round(rx * ry / 120)); k++) { ctx.beginPath(); ctx.arc(cx + (r() * 2 - 1) * rx, cy + (r() * 2 - 1) * ry, .7 + r() * 1.3, 0, TAU); ctx.fill(); }
    ctx.restore();
    // reflet sur le dessus
    ctx.save(); ctx.beginPath(); ctx.ellipse(cx, cy, rx, ry, 0, 0, TAU); ctx.clip();
    const h = ctx.createLinearGradient(0, cy - ry, 0, cy); h.addColorStop(0, 'rgba(255,255,255,.28)'); h.addColorStop(1, 'rgba(255,255,255,0)');
    ctx.fillStyle = h; ctx.beginPath(); ctx.ellipse(cx - rx * .1, cy - ry * .55, rx * .75, ry * .4, 0, 0, TAU); ctx.fill(); ctx.restore();
    ctx.restore();
  }

  /**
   * La membrane interne vue de près (bande horizontale) : deux rangées de têtes de phospholipides et leurs queues.
   * (x, y) coin haut-gauche, w largeur, h épaisseur. Le haut et le bas sont les deux compartiments (la page les nomme).
   */
  function membrane(ctx, x, y, w, h, o = {}) {
    ctx.save();
    const g = ctx.createLinearGradient(0, y, 0, y + h);
    g.addColorStop(0, rgba(T.membrane, .30)); g.addColorStop(.5, rgba(T.membrane, .14)); g.addColorStop(1, rgba(T.membrane, .30));
    ctx.fillStyle = g; ctx.fillRect(x, y, w, h);
    const pas = o.pas || 9, rt = Math.min(4, h / 6);
    ctx.strokeStyle = rgba(T.membrane, .6); ctx.lineWidth = 1;
    for (let px = x + pas / 2; px < x + w; px += pas) {
      ctx.beginPath(); ctx.moveTo(px, y + rt); ctx.lineTo(px - 1, y + h / 2 - 1); ctx.moveTo(px + 2, y + rt); ctx.lineTo(px + 3, y + h / 2 - 1);
      ctx.moveTo(px, y + h - rt); ctx.lineTo(px - 1, y + h / 2 + 1); ctx.moveTo(px + 2, y + h - rt); ctx.lineTo(px + 3, y + h / 2 + 1); ctx.stroke();
    }
    for (const yy of [y + rt, y + h - rt]) {
      for (let px = x + pas / 2; px < x + w; px += pas) {
        const gt = ctx.createRadialGradient(px, yy - 1, .5, px + 1, yy, rt);
        gt.addColorStop(0, rgba([255, 244, 200], 1)); gt.addColorStop(1, rgba([220, 150, 40], .95));
        ctx.fillStyle = gt; ctx.beginPath(); ctx.arc(px + 1, yy, rt, 0, TAU); ctx.fill();
      }
    }
    ctx.restore();
  }

  /** Une protéine de la membrane (transporteur) : masse arrondie traversant la membrane. */
  function proteine(ctx, cx, cy, w, h, o = {}) {
    const c = o.couleur || T.proteine, a = o.alpha ?? .9, rr = Math.min(w, h) * .45;
    const chemin = () => { ctx.beginPath(); if (ctx.roundRect) ctx.roundRect(cx - w / 2, cy - h / 2, w, h, rr); else ctx.rect(cx - w / 2, cy - h / 2, w, h); };
    ctx.save(); ctx.globalAlpha = Math.min(1, a / .85);
    // ombre posée, corps en volume (clair en haut, foncé en bas), liseré, reflet
    ctx.fillStyle = 'rgba(0,0,0,.28)'; ctx.beginPath(); ctx.ellipse(cx + 1.5, cy + h * .56, w * .44, Math.max(1.5, h * .14), 0, 0, TAU); ctx.fill();
    const g = ctx.createLinearGradient(0, cy - h / 2, 0, cy + h / 2);
    g.addColorStop(0, rgba(c.map(v => Math.min(255, v + 85)), 1)); g.addColorStop(.45, rgba(c, 1)); g.addColorStop(1, rgba(c.map(v => v * .5), 1));
    ctx.fillStyle = g; chemin(); ctx.fill();
    ctx.strokeStyle = rgba(c.map(v => v * .4), .9); ctx.lineWidth = 1; ctx.stroke();
    ctx.fillStyle = 'rgba(255,255,255,.32)'; ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(cx - w / 2 + rr * .6, cy - h / 2 + Math.min(2, h * .1), Math.max(1, w - rr * 1.2), h * .26, h * .13); ctx.fill();
    ctx.restore();
  }

  /** Une bille ombrée (molécule, atome de carbone, ion, phosphate). */
  function bille(ctx, x, y, r, c = [250, 204, 21], o = {}) {
    ctx.save(); ctx.globalAlpha = o.alpha ?? 1;
    ctx.fillStyle = 'rgba(0,0,0,.25)'; ctx.beginPath(); ctx.ellipse(x + r * .25, y + r * .9, r * .8, r * .25, 0, 0, TAU); ctx.fill();
    const g = ctx.createRadialGradient(x - r * .35, y - r * .35, r * .1, x, y, r);
    g.addColorStop(0, rgba(c.map(v => Math.min(255, v + 120)), 1)); g.addColorStop(.5, rgba(c, 1)); g.addColorStop(1, rgba(c.map(v => v * .5), 1));
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.fill();
    if (r >= 5) { ctx.fillStyle = 'rgba(255,255,255,.55)'; ctx.beginPath(); ctx.ellipse(x - r * .35, y - r * .42, r * .22, r * .14, -.6, 0, TAU); ctx.fill(); }
    ctx.restore();
  }

  /** Une liaison entre deux atomes : un petit bâton peint (ombre, corps, reflet), à dessiner AVANT les billes. */
  function liaison(ctx, x1, y1, x2, y2, o = {}) {
    const e = o.epaisseur ?? 4.5;
    ctx.save(); ctx.globalAlpha = o.alpha ?? 1; ctx.lineCap = 'round';
    ctx.strokeStyle = 'rgba(40,40,30,.75)'; ctx.lineWidth = e + 1.6; ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();
    ctx.strokeStyle = rgba(o.couleur || [200, 200, 190], 1); ctx.lineWidth = e; ctx.stroke();
    ctx.strokeStyle = 'rgba(255,255,255,.55)'; ctx.lineWidth = e * .3; ctx.beginPath(); ctx.moveTo(x1, y1 - e * .2); ctx.lineTo(x2, y2 - e * .2); ctx.stroke();
    ctx.restore();
  }
  /** Une capsule peinte (transporteur, molécule porteuse) : volume, ombre posée ; o.lueur : halo quand elle est chargée. */
  function capsule(ctx, cx, cy, w, h, c, o = {}) {
    const a = o.alpha ?? 1, r = h / 2;
    ctx.save(); ctx.globalAlpha = a;
    if (o.lueur) { const gl = ctx.createRadialGradient(cx, cy, 2, cx, cy, w * .8); gl.addColorStop(0, rgba(c, .35 * o.lueur)); gl.addColorStop(1, rgba(c, 0)); ctx.fillStyle = gl; ctx.beginPath(); ctx.ellipse(cx, cy, w * .8, h * 1.4, 0, 0, TAU); ctx.fill(); }
    ctx.fillStyle = 'rgba(0,0,0,.3)'; ctx.beginPath(); ctx.ellipse(cx + 2, cy + h * .62, w * .46, h * .2, 0, 0, TAU); ctx.fill();
    const g = ctx.createLinearGradient(0, cy - r, 0, cy + r);
    g.addColorStop(0, rgba(c.map(v => Math.min(255, v + 90)), 1)); g.addColorStop(.45, rgba(c, 1)); g.addColorStop(1, rgba(c.map(v => v * .5), 1));
    ctx.fillStyle = g; ctx.beginPath(); if (ctx.roundRect) ctx.roundRect(cx - w / 2, cy - r, w, h, r); else ctx.rect(cx - w / 2, cy - r, w, h); ctx.fill();
    ctx.strokeStyle = rgba(c.map(v => v * .4), .9); ctx.lineWidth = 1; ctx.stroke();
    ctx.fillStyle = 'rgba(255,255,255,.35)'; ctx.beginPath(); if (ctx.roundRect) ctx.roundRect(cx - w / 2 + r * .6, cy - r + 2, w - r * 1.2, h * .28, h * .14); ctx.fill();
    ctx.restore();
  }

  /**
   * La sphère pédonculée (ATP synthase) dans une membrane horizontale : un pied qui traverse la membrane et une tête
   * ronde du côté `tete` (+1 = vers le bas, −1 = vers le haut). (x, yMembrane) = milieu de la membrane.
   */
  function spherePedonculee(ctx, x, yM, ep, tete = 1, o = {}) {
    const r = o.r || 15, pied = ep * .9 + 10;
    proteine(ctx, x, yM, 16, ep + 6, { couleur: [200, 150, 80] });
    ctx.save(); ctx.strokeStyle = rgba(T.sphere, .9); ctx.lineWidth = 5; ctx.lineCap = 'round';
    ctx.beginPath(); ctx.moveTo(x, yM); ctx.lineTo(x, yM + tete * pied); ctx.stroke(); ctx.restore();
    bille(ctx, x, yM + tete * (pied + r - 2), r, T.sphere, { alpha: o.alpha ?? .95 });
  }

  /** Un bécher (verre peint) avec sa solution : (x, y) haut-gauche du verre, w, h ; niveau = part remplie (0..1). */
  function becher(ctx, x, y, w, h, o = {}) {
    const niveau = o.niveau ?? .7, c = o.teinte || T.eau, ys = y + h * (1 - niveau);
    ctx.save();
    // solution
    const g = ctx.createLinearGradient(0, ys, 0, y + h);
    g.addColorStop(0, rgba(c.map(v => Math.min(255, v + 40)), o.alpha ?? .45)); g.addColorStop(1, rgba(c, (o.alpha ?? .45) + .15));
    ctx.fillStyle = g; ctx.beginPath(); ctx.moveTo(x + 3, ys); ctx.lineTo(x + w - 3, ys); ctx.lineTo(x + w - 3, y + h - 8);
    ctx.quadraticCurveTo(x + w - 3, y + h - 3, x + w - 8, y + h - 3); ctx.lineTo(x + 8, y + h - 3); ctx.quadraticCurveTo(x + 3, y + h - 3, x + 3, y + h - 8); ctx.closePath(); ctx.fill();
    // ménisque
    ctx.strokeStyle = rgba([220, 240, 250], .55); ctx.lineWidth = 1.5; ctx.beginPath(); ctx.moveTo(x + 4, ys - 2); ctx.quadraticCurveTo(x + w / 2, ys + 3, x + w - 4, ys - 2); ctx.stroke();
    // verre
    ctx.strokeStyle = rgba([220, 235, 245], .55); ctx.lineWidth = 2.2;
    ctx.beginPath(); ctx.moveTo(x - 4, y); ctx.lineTo(x, y + 4); ctx.lineTo(x, y + h - 8); ctx.quadraticCurveTo(x, y + h, x + 8, y + h); ctx.lineTo(x + w - 8, y + h); ctx.quadraticCurveTo(x + w, y + h, x + w, y + h - 8); ctx.lineTo(x + w, y + 4); ctx.lineTo(x + w + 4, y); ctx.stroke();
    // reflet du verre
    ctx.strokeStyle = 'rgba(255,255,255,.12)'; ctx.lineWidth = 5; ctx.beginPath(); ctx.moveTo(x + 9, y + 10); ctx.lineTo(x + 9, y + h - 14); ctx.stroke();
    ctx.restore();
    return { surface: ys };
  }

  /** Une levure : cellule ovale à paroi épaisse, vacuole, petit bourgeon facultatif ; `mitos` petites mitochondries. */
  function levure(ctx, x, y, r, o = {}) {
    const rr = graine(o.graine || Math.round(x * 7 + y * 13));
    ctx.save(); ctx.translate(x, y); ctx.rotate(o.angle ?? (rr() - .5));
    const g = ctx.createRadialGradient(-r * .3, -r * .3, 1, 0, 0, r * 1.2);
    g.addColorStop(0, rgba([240, 224, 180], .85)); g.addColorStop(1, rgba(T.levure, .7));
    ctx.fillStyle = g; ctx.beginPath(); ctx.ellipse(0, 0, r * 1.12, r, 0, 0, TAU); ctx.fill();
    ctx.strokeStyle = rgba([150, 120, 70], .8); ctx.lineWidth = Math.max(1, r * .14); ctx.stroke();
    if (o.bourgeon !== false && rr() > .45) { ctx.beginPath(); ctx.ellipse(r * 1.25, -r * .35, r * .42, r * .36, 0, 0, TAU); ctx.fillStyle = rgba(T.levure, .8); ctx.fill(); ctx.stroke(); }
    ctx.fillStyle = rgba([170, 190, 200], .45); ctx.beginPath(); ctx.ellipse(r * .15, r * .1, r * .38, r * .32, 0, 0, TAU); ctx.fill();
    for (let k = 0; k < (o.mitos || 0); k++) { const a = rr() * TAU; ctx.fillStyle = rgba(T.mitoExt, .8); ctx.beginPath(); ctx.ellipse(Math.cos(a) * r * .6, Math.sin(a) * r * .55, r * .2, r * .1, a, 0, TAU); ctx.fill(); }
    ctx.restore();
  }

  /** Une bulle de gaz dans un liquide. */
  function bulleGaz(ctx, x, y, r) {
    ctx.save(); ctx.strokeStyle = 'rgba(230,245,255,.6)'; ctx.lineWidth = 1.2; ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.stroke();
    ctx.fillStyle = 'rgba(255,255,255,.5)'; ctx.beginPath(); ctx.arc(x - r * .35, y - r * .35, r * .3, 0, TAU); ctx.fill(); ctx.restore();
  }

  /** Un éclat d'énergie (petite étoile lumineuse) : quand une liaison se rompt, quand l'énergie sort. */
  function eclat(ctx, x, y, r, a = 1) {
    ctx.save(); ctx.globalAlpha = a;
    const g = ctx.createRadialGradient(x, y, 0, x, y, r);
    g.addColorStop(0, 'rgba(255,250,200,.95)'); g.addColorStop(.4, 'rgba(250,204,21,.55)'); g.addColorStop(1, 'rgba(250,204,21,0)');
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.fill(); ctx.restore();
  }

  /* ── Fonds et cartes communs (16 novembre 2026, refonte « un seul style agréable ») ── */
  const GR = (() => { const r = graine(77), out = []; for (let i = 0; i < 400; i++) out.push([r(), r(), .7 + r() * 1.6, r()]); return out; })();
  /** La matrice peinte : bleu lumineux doux, plus clair vers (cx, cy), granules clairs et quelques denses. */
  function fondMatrice(ctx, x, y, w, h, o = {}) {
    const cx = o.cx ?? x + w / 2, cy = o.cy ?? y + h / 2;
    ctx.save(); ctx.beginPath(); if (o.arrondi && ctx.roundRect) ctx.roundRect(x, y, w, h, o.arrondi); else ctx.rect(x, y, w, h); ctx.clip();
    const g = ctx.createRadialGradient(cx, cy, 20, cx + 60, cy + 30, Math.max(w, h) * .9);
    g.addColorStop(0, 'rgba(96,190,245,.62)'); g.addColorStop(.45, 'rgba(52,140,210,.50)'); g.addColorStop(1, 'rgba(22,72,128,.42)');
    ctx.fillStyle = g; ctx.fillRect(x, y, w, h);
    const n = Math.round(w * h / 1800);
    for (let i = 0; i < Math.min(n, GR.length); i++) {
      const [u, v, r, k] = GR[i]; ctx.fillStyle = k < .82 ? 'rgba(225,245,255,.22)' : 'rgba(20,60,110,.35)';
      ctx.beginPath(); ctx.arc(x + u * w, y + v * h, k < .82 ? r : r + 1.4, 0, TAU); ctx.fill();
    }
    ctx.restore();
  }
  /** Le hyaloplasme peint : vert d'eau lumineux, granules. */
  function fondHyalo(ctx, x, y, w, h, o = {}) {
    ctx.save(); ctx.beginPath(); if (o.arrondi && ctx.roundRect) ctx.roundRect(x, y, w, h, o.arrondi); else ctx.rect(x, y, w, h); ctx.clip();
    const g = ctx.createLinearGradient(x, y, x + w, y + h); g.addColorStop(0, rgba(T.hyalo, .40)); g.addColorStop(1, rgba(T.hyalo, .22));
    ctx.fillStyle = g; ctx.fillRect(x, y, w, h);
    const n = Math.round(w * h / 1600);
    for (let i = 0; i < Math.min(n, GR.length); i++) { const [u, v, r] = GR[GR.length - 1 - i]; ctx.fillStyle = 'rgba(210,240,200,.20)'; ctx.beginPath(); ctx.arc(x + u * w, y + v * h, r, 0, TAU); ctx.fill(); }
    ctx.restore();
  }
  /**
   * Une carte (tableau, compteur, bilan) : fond bleu nuit, bord doré, ombre douce ; o.entete = hauteur d'un en-tête doré
   * (le titre s'écrit dessus en sombre et gras) ; o.rayures = liste des y de lignes à éclaircir une sur deux (hauteur o.pas).
   */
  function carte(ctx, x, y, w, h, o = {}) {
    ctx.save();
    ctx.shadowColor = 'rgba(0,0,0,.45)'; ctx.shadowBlur = 14; ctx.shadowOffsetY = 5;
    const g = ctx.createLinearGradient(0, y, 0, y + h); g.addColorStop(0, `rgba(14,32,58,${o.alpha ?? .94})`); g.addColorStop(1, `rgba(8,22,42,${o.alpha ?? .94})`);
    ctx.fillStyle = g; ctx.beginPath(); if (ctx.roundRect) ctx.roundRect(x, y, w, h, o.arrondi ?? 16); else ctx.rect(x, y, w, h); ctx.fill(); ctx.shadowColor = 'transparent';
    ctx.save(); ctx.clip();
    if (o.entete) { const gh = ctx.createLinearGradient(0, y, 0, y + o.entete); gh.addColorStop(0, o.clair || '#fde68a'); gh.addColorStop(1, o.fonce || '#f59e0b'); ctx.fillStyle = gh; ctx.fillRect(x, y, w, o.entete); }
    if (o.rayures) { ctx.fillStyle = 'rgba(255,255,255,.05)'; o.rayures.forEach((yy, i) => { if (i % 2 === 0) ctx.fillRect(x, yy, w, o.pas || 30); }); }
    ctx.restore();
    ctx.lineWidth = 2; ctx.strokeStyle = o.bord || 'rgba(250,204,21,.85)'; ctx.beginPath(); if (ctx.roundRect) ctx.roundRect(x, y, w, h, o.arrondi ?? 16); else ctx.rect(x, y, w, h); ctx.stroke();
    ctx.restore();
  }
  /** Une molécule de CO2 peinte : O = C = O (carbone gris, oxygènes rouges). */
  function co2(ctx, x, y, k = 1, a = 1) {
    if (a <= 0) return;
    liaison(ctx, x - 9 * k, y, x + 9 * k, y, { alpha: a, epaisseur: 3 * k });
    bille(ctx, x - 10 * k, y, 5 * k, [235, 85, 70], { alpha: a }); bille(ctx, x + 10 * k, y, 5 * k, [235, 85, 70], { alpha: a }); bille(ctx, x, y, 6 * k, [150, 160, 175], { alpha: a });
  }

  window.SVTPeinture = { T, graine, rgba, cellule, mitochondrie, cheminCretes, membrane, proteine, bille, liaison, capsule, spherePedonculee, becher, levure, bulleGaz, eclat,
    fondMatrice, fondHyalo, carte, co2 };
})();

/* ── Mosaïque du tableau large (15 novembre 2026) : ici plutôt que dans un fichier à part (un nouveau .js de public/ n'est pas servi par le serveur de dev). ── */
/*
 * Mosaïque : une page dessinée pour le cadre 760 × 420 est rangée sur toute la largeur du tableau (15 novembre 2026,
 * « la simulation n'occupe qu'une bande étroite, les textes sont minuscules »).
 * Avec Scene(..., { large: true }), le cadre fait scene.L de large (≈ 1220 sur un portable 1366 × 613). La page est
 * découpée en blocs (rectangles du dessin d'origine) posés en colonnes, chacun agrandi autant que la hauteur le permet :
 * la figure prend toute la hauteur, les textes passent à côté, plus gros. Rien n'est redessiné autrement : chaque bloc
 * rejoue le dessin de la page sous une transformation (translation + échelle) avec une découpe, donc les repères pointés
 * par le tuteur (craie.repere lit la transformation du contexte) suivent tout seuls, et scene.local renvoie les
 * coordonnées d'origine (poignées, clics).
 *
 *   const MOS = SVTLarge.Mosaique(scene, (L) => L >= 1000 ? { colonnes: [[[0, 0, 470, 420]], [[470, 40, 290, 200], [470, 240, 290, 180]]] } : null);
 *   Scene(canvas, (c) => { scene.cadre(31); MOS.dessiner(c, () => dessiner(c)); return c.fin(); }, { large: true });
 *
 * Une colonne = liste de rectangles [x, y, w, h] empilés (même échelle dans la colonne) ; option par colonne
 * { blocs: [...], max: 1.6 } pour borner l'agrandissement ; `police: 1.15` grossit en plus les textes de la craie. Sous L < 1000 (grand écran, déjà haut) : dessin d'origine.
 */
(function () {
  'use strict';
  const VH = 420, ECART = 18, HAUT = 6;
  function Mosaique(scene, disposition) {
    let cleL = null, blocs = null;
    function calculer(L) {
      const d = disposition(L);
      if (!d) return null;
      if (d.blocs) {   // placement à la main : { src: [x, y, w, h], X, Y, s, police }
        const out = d.blocs.map(b => ({ x: b.src[0], y: b.src[1], w: b.src[2], h: b.src[3], X: b.X, Y: b.Y, s: b.s, police: b.police }));
        out.police = d.police || 1; return out;
      }
      if (d.lignes) return lignes(d, L);
      const cols = d.colonnes.map(c => (Array.isArray(c) ? { blocs: c } : c));
      const gap = d.ecart ?? ECART;
      for (const c of cols) {
        c.H = c.blocs.reduce((s, b) => s + b[3], 0);
        c.Wsrc = Math.max(...c.blocs.map(b => b[2]));
        c.s = Math.min(c.max ?? 2, (VH - 2 * HAUT - gap * (c.blocs.length - 1)) / c.H);
      }
      const libre = L - gap * (cols.length + 1);
      const somme = cols.reduce((s, c) => s + c.Wsrc * c.s, 0);
      if (somme > libre) for (const c of cols) c.s *= libre / somme;
      const total = cols.reduce((s, c) => s + c.Wsrc * c.s, 0);
      const g = (L - total) / (cols.length + 1);
      const out = []; let X = g;
      for (const c of cols) {
        const h = c.H * c.s + gap * (c.blocs.length - 1);
        let Y = (VH - h) / 2;
        for (const [x, y, w, hh] of c.blocs) {
          const cx = c.align === 'gauche' ? X : X + (c.Wsrc - w) * c.s / 2;
          out.push({ x, y, w, h: hh, X: cx, Y, s: c.s, police: c.police });
          Y += hh * c.s + gap;
        }
        X += c.Wsrc * c.s + g;
      }
      out.police = d.police || 1;
      return out;
    }
    /* Rangées : d.lignes = [[item, …], …] ; item = [x, y, w, h] ou { r: [x, y, w, h], k: 1.3, police } (k : agrandi
     * k fois plus que la rangée) ou { pile: [[x, y, w, h], …], k } (rectangles empilés). Une échelle par rangée, la plus
     * grande qui tient en largeur (bornée par d.max), puis toutes réduites ensemble pour tenir en hauteur. */
    function lignes(d, L) {
      const gap = d.ecart ?? ECART, out = [];
      const rows = d.lignes.map(row => row.map(it => {
        const o = Array.isArray(it) ? { r: it } : it, pile = o.pile || [o.r];
        return { pile, k: o.k || 1, police: o.police, w: Math.max(...pile.map(r => r[2])), h: pile.reduce((a, r) => a + r[3], 0) };
      }));
      for (const row of rows) {
        row.s = Math.min(d.max ?? 1.6, (L - gap * (row.length + 1)) / row.reduce((a, it) => a + it.w * it.k, 0));
        row.H = Math.max(...row.filter(it => it.k === 1).map(it => it.h * row.s), 0) || Math.max(...row.map(it => it.h * it.k * row.s));
      }
      const libre = VH - 2 * HAUT - gap * (rows.length - 1), tot = rows.reduce((a, r) => a + r.H, 0);
      if (tot > libre) for (const r of rows) { r.s *= libre / tot; r.H *= libre / tot; }
      let Y = (VH - rows.reduce((a, r) => a + r.H, 0) - gap * (rows.length - 1)) / 2;
      for (const row of rows) {
        for (const it of row) it.s = Math.min(row.s * it.k, row.H / it.h, (d.max ?? 1.6) * 1.2);   // un item agrandi reste dans la hauteur de sa rangée
        const larg = row.reduce((a, it) => a + it.w * it.s, 0), g = (L - larg) / (row.length + 1);
        let X = g;
        for (const it of row) {
          const s = it.s; let y = Y + (row.H - it.h * s) / 2;
          for (const [x0, y0, w, h] of it.pile) { out.push({ x: x0, y: y0, w, h, X: X + (it.w - w) * s / 2, Y: y, s, police: it.police }); y += h * s; }
          X += it.w * s + g;
        }
        Y += row.H + gap;
      }
      out.police = d.police || 1;
      return out;
    }
    function actuels() {
      if (scene.L !== cleL) { cleL = scene.L; blocs = calculer(scene.L); scene.sale = true; }
      return blocs;
    }
    const M = {
      actif: () => !!actuels(),
      blocs: () => actuels(),
      /** Dessine `fn` (le dessin d'origine) une fois par bloc, ou une seule fois sans mosaïque. */
      dessiner(c, fn) {
        const B = actuels();
        if (!B) {   // sans mosaïque : le dessin d'origine, centré dans le cadre (large : L un peu plus grand que 760)
          const dx = Math.max(0, (scene.L - 760) / 2); if (!dx) return fn();
          c.ctx.save(); c.ctx.translate(dx, 0); try { fn(); } finally { c.ctx.restore(); }
          if (c.tip) c.tip = [c.tip[0] + dx, c.tip[1]];
          return;
        }
        const ctx = c.ctx, cur0 = c.cur; let curMax = cur0, tip = null, complet = true;
        // police : les textes un peu plus gros que dans le dessin d'origine (la mosaïque leur laisse la place).
        const texte = c.texte, repere = c.repere, k = B.police;
        // Un repère est déclaré par le seul bloc qui en montre la plus grande part (le tuteur le pointe là).
        const part = (b, x, y, w, h) => Math.max(0, Math.min(b.x + b.w, x + w) - Math.max(b.x, x)) * Math.max(0, Math.min(b.y + b.h, y + h) - Math.max(b.y, y));
        let ici = null;
        c.repere = function (id, x, y, w, h, label) {
          const xa = Math.min(x, x + w), ya = Math.min(y, y + h), wa = Math.abs(w), ha = Math.abs(h);
          let m = -1, meilleur = null; for (const b of B) { const p = part(b, xa, ya, Math.max(wa, 1), Math.max(ha, 1)); if (p > m) { m = p; meilleur = b; } }
          if (meilleur !== ici) return this;
          return repere.call(this, id, x, y, w, h, label);
        };
        let kb = k; const e0 = c.echelle;   // le minimum lisible (15 px à l'écran) tient compte de l'échelle du bloc
        // une fraction « ⟦num|dén⟧ » s'écrit en morceaux qui repassent par c.texte : déjà à la bonne taille, ils ne sont pas regrossis
        c.texte = function (s, x, y, o = {}) {
          if (kb === 1 || this._dansFraction) return texte.call(this, s, x, y, o);
          const fr = String(s).includes('⟦'); if (fr) this._dansFraction = true;
          try { return texte.call(this, s, x, y, { ...o, taille: (o.taille ?? 18) * kb, max: o.max && o.max * kb }); } finally { if (fr) this._dansFraction = false; }
        };
        try { B.forEach((b, i) => {
          ici = b; kb = b.police ?? k; if (e0) c.echelle = e0 * b.s; c.cur = cur0; c.tip = null; c.complet = true; c.r = window.Tableau.graine(97 + 13 * i);
          ctx.save();
          ctx.translate(b.X, b.Y); ctx.scale(b.s, b.s); ctx.translate(-b.x, -b.y);
          ctx.beginPath(); ctx.rect(b.x, b.y, b.w, b.h); ctx.clip();
          try { fn(); } finally { ctx.restore(); }
          curMax = Math.max(curMax, c.cur); complet = complet && c.complet;
          if (c.tip) tip = [b.X + (c.tip[0] - b.x) * b.s, b.Y + (c.tip[1] - b.y) * b.s];
        }); } finally { c.texte = texte; c.repere = repere; c.echelle = e0; }
        c.cur = curMax; c.tip = tip; c.complet = complet;
      },
      /** Coordonnées du cadre large → coordonnées du dessin d'origine. */
      versOrigine(x, y) {
        const B = actuels(); if (!B) return [x - Math.max(0, (scene.L - 760) / 2), y];
        let best = null, dmin = Infinity;
        for (const b of B) {
          const x0 = b.X, y0 = b.Y, x1 = b.X + b.w * b.s, y1 = b.Y + b.h * b.s;
          const d = Math.hypot(Math.max(x0 - x, 0, x - x1), Math.max(y0 - y, 0, y - y1));
          if (d < dmin) { dmin = d; best = b; }
        }
        return [best.x + (x - best.X) / best.s, best.y + (y - best.Y) / best.s];
      },
    };
    const local0 = scene.local.bind(scene);
    scene.local = (x, y) => { const [a, b] = local0(x, y); return M.versOrigine(a, b); };
    return M;
  }
  window.SVTLarge = { Mosaique };
})();
