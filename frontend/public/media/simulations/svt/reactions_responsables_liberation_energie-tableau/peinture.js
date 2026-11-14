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
  const T = {
    hyalo: [120, 160, 110], membrane: [214, 186, 120], noyau: [120, 96, 160],
    mitoExt: [196, 98, 58], mitoEsp: [232, 170, 110], matrice: [120, 170, 196], crete: [240, 206, 150],
    proteine: [150, 120, 200], sphere: [240, 190, 90], eau: [70, 140, 170], levure: [214, 190, 140],
  };

  /** Une cellule vue en coupe : membrane plasmique, hyaloplasme granuleux, noyau facultatif ({noyau: {x, y, r}}). */
  function cellule(ctx, cx, cy, rx, ry, o = {}) {
    const r = graine(o.graine || 11);
    ctx.save();
    ctx.beginPath(); ctx.ellipse(cx, cy, rx, ry, o.angle || 0, 0, TAU);
    const g = ctx.createRadialGradient(cx - rx * .25, cy - ry * .3, 4, cx, cy, Math.max(rx, ry));
    g.addColorStop(0, rgba(T.hyalo, .30)); g.addColorStop(.7, rgba(T.hyalo, .20)); g.addColorStop(1, rgba(T.hyalo, .10));
    ctx.fillStyle = g; ctx.fill();
    ctx.clip();
    // granulations du hyaloplasme
    ctx.fillStyle = rgba([200, 220, 180], .16);
    for (let k = 0; k < (o.grains ?? 90); k++) {
      const a = r() * TAU, d = Math.sqrt(r()), x = cx + Math.cos(a) * rx * d, y = cy + Math.sin(a) * ry * d;
      ctx.beginPath(); ctx.arc(x, y, .8 + r() * 1.6, 0, TAU); ctx.fill();
    }
    if (o.noyau) {
      const n = o.noyau, gn = ctx.createRadialGradient(n.x - n.r * .3, n.y - n.r * .3, 2, n.x, n.y, n.r);
      gn.addColorStop(0, rgba(T.noyau, .55)); gn.addColorStop(1, rgba(T.noyau, .28));
      ctx.fillStyle = gn; ctx.beginPath(); ctx.arc(n.x, n.y, n.r, 0, TAU); ctx.fill();
      ctx.strokeStyle = rgba([200, 180, 240], .45); ctx.lineWidth = 2; ctx.stroke();
    }
    ctx.restore();
    // membrane plasmique : deux traits fins rapprochés
    ctx.save(); ctx.lineWidth = 2.2; ctx.strokeStyle = rgba(T.membrane, .75);
    ctx.beginPath(); ctx.ellipse(cx, cy, rx, ry, o.angle || 0, 0, TAU); ctx.stroke();
    ctx.lineWidth = 1; ctx.strokeStyle = rgba(T.membrane, .4);
    ctx.beginPath(); ctx.ellipse(cx, cy, rx - 4, ry - 4, o.angle || 0, 0, TAU); ctx.stroke();
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
    // membrane externe et espace intermembranaire
    ctx.beginPath(); ctx.ellipse(cx, cy, rx, ry, 0, 0, TAU);
    const g = ctx.createLinearGradient(cx, cy - ry, cx, cy + ry);
    g.addColorStop(0, rgba(T.mitoEsp, .55)); g.addColorStop(1, rgba(T.mitoExt, .55));
    ctx.fillStyle = g; ctx.fill();
    ctx.lineWidth = 2.6; ctx.strokeStyle = rgba(T.mitoExt, .95); ctx.stroke();
    // matrice (à l'intérieur de la membrane interne)
    cheminCretes(ctx, cx, cy, rx, ry, n);
    const gm = ctx.createRadialGradient(cx - rx * .2, cy - ry * .2, 3, cx, cy, Math.max(rx, ry));
    gm.addColorStop(0, rgba(T.matrice, .62)); gm.addColorStop(1, rgba(T.matrice, .38));
    ctx.fillStyle = gm; ctx.fill();
    ctx.lineWidth = 2.2; ctx.strokeStyle = rgba(T.crete, .9); ctx.stroke();
    // granules de la matrice
    ctx.save(); cheminCretes(ctx, cx, cy, rx, ry, n); ctx.clip(); ctx.fillStyle = rgba([230, 240, 250], .22);
    for (let k = 0; k < (o.grains ?? Math.round(rx * ry / 120)); k++) { ctx.beginPath(); ctx.arc(cx + (r() * 2 - 1) * rx, cy + (r() * 2 - 1) * ry, .7 + r() * 1.3, 0, TAU); ctx.fill(); }
    ctx.restore();
    ctx.restore();
  }

  /**
   * La membrane interne vue de près (bande horizontale) : deux rangées de têtes de phospholipides et leurs queues.
   * (x, y) coin haut-gauche, w largeur, h épaisseur. Le haut et le bas sont les deux compartiments (la page les nomme).
   */
  function membrane(ctx, x, y, w, h, o = {}) {
    ctx.save();
    const g = ctx.createLinearGradient(0, y, 0, y + h);
    g.addColorStop(0, rgba(T.membrane, .18)); g.addColorStop(.5, rgba(T.membrane, .08)); g.addColorStop(1, rgba(T.membrane, .18));
    ctx.fillStyle = g; ctx.fillRect(x, y, w, h);
    const pas = o.pas || 9, rt = Math.min(4, h / 6);
    ctx.strokeStyle = rgba(T.membrane, .35); ctx.lineWidth = 1;
    for (let px = x + pas / 2; px < x + w; px += pas) {
      ctx.beginPath(); ctx.moveTo(px, y + rt); ctx.lineTo(px - 1, y + h / 2 - 1); ctx.moveTo(px + 2, y + rt); ctx.lineTo(px + 3, y + h / 2 - 1);
      ctx.moveTo(px, y + h - rt); ctx.lineTo(px - 1, y + h / 2 + 1); ctx.moveTo(px + 2, y + h - rt); ctx.lineTo(px + 3, y + h / 2 + 1); ctx.stroke();
    }
    for (const yy of [y + rt, y + h - rt]) {
      for (let px = x + pas / 2; px < x + w; px += pas) {
        const gt = ctx.createRadialGradient(px, yy - 1, .5, px + 1, yy, rt);
        gt.addColorStop(0, rgba([250, 230, 180], .9)); gt.addColorStop(1, rgba(T.membrane, .6));
        ctx.fillStyle = gt; ctx.beginPath(); ctx.arc(px + 1, yy, rt, 0, TAU); ctx.fill();
      }
    }
    ctx.restore();
  }

  /** Une protéine de la membrane (transporteur) : masse arrondie traversant la membrane. */
  function proteine(ctx, cx, cy, w, h, o = {}) {
    const c = o.couleur || T.proteine;
    ctx.save();
    const g = ctx.createRadialGradient(cx - w * .25, cy - h * .25, 2, cx, cy, Math.max(w, h) * .7);
    g.addColorStop(0, rgba(c.map(v => Math.min(255, v + 60)), o.alpha ?? .9)); g.addColorStop(1, rgba(c, (o.alpha ?? .9) * .8));
    ctx.fillStyle = g;
    ctx.beginPath();
    if (ctx.roundRect) ctx.roundRect(cx - w / 2, cy - h / 2, w, h, Math.min(w, h) * .45); else ctx.rect(cx - w / 2, cy - h / 2, w, h);
    ctx.fill();
    ctx.strokeStyle = rgba([255, 255, 255], .25); ctx.lineWidth = 1; ctx.stroke();
    ctx.restore();
  }

  /** Une bille ombrée (molécule, atome de carbone, ion, phosphate). */
  function bille(ctx, x, y, r, c = [250, 204, 21], o = {}) {
    ctx.save(); ctx.globalAlpha = o.alpha ?? 1;
    ctx.fillStyle = 'rgba(0,0,0,.25)'; ctx.beginPath(); ctx.ellipse(x + r * .25, y + r * .9, r * .8, r * .25, 0, 0, TAU); ctx.fill();
    const g = ctx.createRadialGradient(x - r * .35, y - r * .35, r * .1, x, y, r);
    g.addColorStop(0, rgba(c.map(v => Math.min(255, v + 90)), 1)); g.addColorStop(.6, rgba(c, 1)); g.addColorStop(1, rgba(c.map(v => v * .55), 1));
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.fill();
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

  window.SVTPeinture = { T, graine, rgba, cellule, mitochondrie, cheminCretes, membrane, proteine, bille, spherePedonculee, becher, levure, bulleGaz, eclat };
})();
