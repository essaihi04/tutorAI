/*
 * LEXIQUE VISUEL COMMUN DU SITE (18 novembre 2026) — skill simulations-au-tableau, règle 15 ; professeur, règle 43.
 *
 * « Une fois qu'un élément est modélisé ou représenté sous une forme, il doit rester sous la même forme dans tout le cours,
 * et dans tous les cours de toutes les matières. » Chaque objet (molécule, organite, ion, transporteur, composant,
 * particule) a UNE fonction ici ; aucune simulation ne le redessine localement. Fiches : docs/lexique-visuel/<élément>.md.
 *
 * Usage : <script src="/media/simulations/shared/lexique/lexique.js"></script> puis, dans `craie.direct` (contexte brut,
 * coordonnées du cadre virtuel) : `Lexique.glucose(ctx, x, y, { echelle, alpha, etat, forme, coupe })`.
 * Toutes les fonctions peignent (règle 32 du professeur : réaliste, en couleur, ombre et reflet) et renvoient la géométrie
 * utile (positions des atomes, boîte) pour poser un repère ou une légende à la craie À CÔTÉ.
 *
 * Le code des couleurs (une couleur garde son sens partout) :
 *   jaune  #facc15 [250,204,21]  un atome de CARBONE (glucose = 6 billes jaunes en chaîne droite ; ses produits gardent ses billes)
 *   blanc  [235,240,245]         un atome d'HYDROGÈNE
 *   rouge  [235,85,70]           un atome d'OXYGÈNE (O₂, H₂O, CO₂, H₃O⁺, HO⁻)
 *   rose   [244,114,182]         un PROTON / ion H⁺ (« H+ » écrit dessus) ; le proton du noyau atomique est le même
 *   bleu ciel [96,200,250]       un ÉLECTRON (« e− » écrit dessus)
 *   gris   [160,168,180]         un NEUTRON ; ADP (carte vide)
 *   doré   [250,190,60]          l'ATP (carte d'énergie pleine) ; orange [240,140,60] le phosphate Pi
 *   cyan   [34,190,220]          le transporteur NAD⁺ / NADH,H⁺ (le « taxi ») ; vert [110,200,90] FAD / FADH₂
 *   violet [160,120,240]         une PROTÉINE (transporteur membranaire, enzyme) ; indigo [110,120,230] le coenzyme A
 * Rien n'est hors programme ici : aucun nom de complexe, aucune molécule intermédiaire nommée.
 */
(function () {
  'use strict';
  if (window.Lexique) return;   // chargé deux fois : on garde le premier
  const TAU = Math.PI * 2;
  function graine(seed) { let s = (seed >>> 0) || 1; return () => { s = (Math.imul(s, 1664525) + 1013904223) >>> 0; return s / 4294967296; }; }
  const rgba = (c, a) => `rgba(${c[0]},${c[1]},${c[2]},${a})`;
  const POLICE = "'Patrick Hand','Caveat','Segoe Print','Bradley Hand','Chalkboard SE','Comic Sans MS',cursive";
  const ENCRE = '#0b1f2a';

  /* Les teintes des milieux vivants (palette du 16 novembre 2026, lisible sur le tableau vert sombre). */
  const T = {
    hyalo: [96, 200, 150], membrane: [250, 204, 96], noyau: [150, 110, 220],
    mitoExt: [240, 100, 62], mitoEsp: [255, 176, 110], matrice: [86, 180, 236], crete: [255, 222, 150],
    proteine: [160, 120, 240], sphere: [252, 196, 70], eau: [60, 160, 210], levure: [236, 200, 130],
  };
  /* Le code des couleurs des objets (voir l'en-tête). */
  const C = {
    carbone: [250, 204, 21], hydrogene: [235, 240, 245], oxygene: [235, 85, 70], azote: [96, 130, 240], phosphore: [240, 140, 60],
    proton: [244, 114, 182], electron: [96, 200, 250], neutron: [160, 168, 180],
    atp: [250, 190, 60], adp: [150, 150, 150], pi: [240, 140, 60], adenosine: [150, 120, 200],
    nad: [34, 190, 220], fad: [110, 200, 90], coa: [110, 120, 230], proteine: T.proteine,
  };

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

  /* ───────────────────────── Texte peint (étiquette DANS un objet) ───────────────────────── */
  /** Écrit `s` centré en (x, y) : sombre et gras sur un objet clair (règle 10). Indices : « FADH_{2} » → FADH₂. */
  function etiquette(ctx, s, x, y, o = {}) {
    const t = o.taille ?? 15, a = o.alpha ?? 1;
    if (a <= .02 || !s) return;
    const segs = []; String(s).replace(/_\{([^}]*)\}|\^\{([^}]*)\}|([^_^]+|[_^])/g, (m, sub, sup, n) => { segs.push(sub != null ? { t: sub, d: .28 } : sup != null ? { t: sup, d: -.38 } : { t: n, d: 0 }); });
    ctx.save(); ctx.globalAlpha *= a; ctx.fillStyle = o.couleur || ENCRE; ctx.textBaseline = 'middle';
    const font = (seg) => `${o.gras === false ? '' : '700 '}${seg.d ? t * .66 : t}px ${POLICE}`;
    let w = 0; for (const seg of segs) { ctx.font = font(seg); w += ctx.measureText(seg.t).width; }
    let px = x - w / 2; ctx.textAlign = 'left';
    for (const seg of segs) { ctx.font = font(seg); ctx.fillText(seg.t, px, y + 1 + seg.d * t); px += ctx.measureText(seg.t).width; }
    ctx.restore();
    return w;
  }

  /* ───────────────────────── Atomes ───────────────────────── */
  /* Rayons à l'échelle 1 (cadre virtuel 760 × 420) : le carbone du glucose fait 12 px, la chaîne a un pas de 28 px. */
  const R = { C: 12, H: 5, O: 9, N: 10, P: 9 };
  const PAS = 28;
  const COUL_ATOME = { C: C.carbone, H: C.hydrogene, O: C.oxygene, N: C.azote, P: C.phosphore };
  /** Un atome en bille peinte : 'C' jaune, 'H' blanc, 'O' rouge, 'N' bleu, 'P' orange. */
  function atome(ctx, x, y, el = 'C', o = {}) {
    const r = (o.r ?? R[el] ?? 8) * (o.echelle ?? 1);
    bille(ctx, x, y, r, o.couleur || COUL_ATOME[el] || [200, 200, 200], { alpha: o.alpha ?? 1 });
    return { x, y, r };
  }
  /** Les positions d'une chaîne droite de n atomes centrée en (x, y) (angle en radians, pas = 28 × échelle). */
  function positionsChaine(n, x, y, o = {}) {
    const e = o.echelle ?? 1, p = (o.pas ?? PAS) * e, a = o.angle || 0, out = [];
    for (let i = 0; i < n; i++) { const d = (i - (n - 1) / 2) * p; out.push([x + Math.cos(a) * d, y + Math.sin(a) * d]); }
    return out;
  }
  /**
   * Une chaîne de carbones (billes jaunes reliées) aux positions `pts` ; o.liaisons : alpha de chaque liaison (1 par défaut,
   * 0 = rompue) ; o.alphas : alpha de chaque atome. Les liaisons d'abord, les billes par-dessus.
   */
  function chaine(ctx, pts, o = {}) {
    const e = o.echelle ?? 1, a = o.alpha ?? 1;
    if (a <= .02) return pts;
    for (let i = 0; i < pts.length - 1; i++) {
      const al = a * (o.liaisons ? (o.liaisons[i] ?? 1) : 1);
      if (al > .02) liaison(ctx, pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], { alpha: al, epaisseur: 4.5 * e });
    }
    pts.forEach(([x, y], i) => { const ai = a * (o.alphas ? (o.alphas[i] ?? 1) : 1); if (ai > .02) bille(ctx, x, y, R.C * e, o.couleur || C.carbone, { alpha: ai }); });
    return pts;
  }
  /** Boîte englobante d'une liste de points (marge = rayon). */
  function boite(pts, r) {
    const xs = pts.map(p => p[0]), ys = pts.map(p => p[1]);
    return { x: Math.min(...xs) - r, y: Math.min(...ys) - r, w: Math.max(...xs) - Math.min(...xs) + 2 * r, h: Math.max(...ys) - Math.min(...ys) + 2 * r };
  }
  /** Atténuation d'un objet transformé (règle 13) : 'degrade' / 'oxyde' / 'consomme' → pâli à 32 %. */
  const alphaEtat = (o) => (o.alpha ?? 1) * (o.etat === 'degrade' || o.etat === 'consomme' ? .32 : 1);

  /* ───────────────────────── Formules écrites (formes « brute », « semi-développée »…) ───────────────────────── */
  /** Écrit des lignes de formule (à la craie claire) centrées en (x, y) ; pour une équation au tableau, préférer `craie.texte`. */
  function formule(ctx, lignes, x, y, o = {}) {
    const t = (o.taille ?? 18) * (o.echelle ?? 1), h = t * 1.25;
    lignes.forEach((s, i) => etiquette(ctx, s, x, y + (i - (lignes.length - 1) / 2) * h, { taille: t, couleur: o.couleur || '#facc15', gras: false, alpha: o.alpha }));
    return { x: x - 4 * t, y: y - lignes.length * h / 2, w: 8 * t, h: lignes.length * h };
  }
  /** Une formule développée en grille : `grille` = lignes de texte où chaque caractère est un atome ou un trait (|, −, =). */
  function grille(ctx, grille, x, y, o = {}) {
    const t = (o.taille ?? 17) * (o.echelle ?? 1), dx = t * .72, dy = t * 1.15, H = grille.length, W = Math.max(...grille.map(l => l.length));
    ctx.save(); ctx.globalAlpha *= (o.alpha ?? 1); ctx.font = `${t}px ${POLICE}`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    grille.forEach((l, j) => [...l].forEach((ch, i) => {
      if (ch === ' ') return;
      ctx.fillStyle = ch === 'C' ? '#facc15' : ch === 'O' ? '#fca5a5' : ch === 'H' ? '#e2e8f0' : 'rgba(226,232,240,.8)';
      ctx.fillText(ch, x + (i - (W - 1) / 2) * dx, y + (j - (H - 1) / 2) * dy);
    }));
    ctx.restore();
    return { x: x - W * dx / 2, y: y - H * dy / 2, w: W * dx, h: H * dy };
  }

  /* ───────────────────────── Molécules organiques (forme « billes » des animations) ───────────────────────── */
  /**
   * LE GLUCOSE : une chaîne DROITE de 6 billes jaunes (carbones) liées. (x, y) = milieu de la chaîne.
   * o.echelle (1 → billes de 12 px, pas de 28 px), o.alpha, o.angle, o.etat ('degrade' : pâli, règle 13),
   * o.coupe (0..1) : la liaison du milieu se rompt et les deux moitiés de 3 s'écartent de o.ecart (px, défaut 1 pas)
   * — ce sont les deux acides pyruviques. o.forme : 'billes' (défaut), 'brute', 'semi_developpee', 'developpee', 'cyclique'.
   * Renvoie { atomes, boite }.
   */
  function glucose(ctx, x, y, o = {}) {
    const f = o.forme || 'billes', e = o.echelle ?? 1;
    if (f === 'brute') return formule(ctx, ['C_{6}H_{12}O_{6}'], x, y, o);
    if (f === 'semi_developpee') return formule(ctx, ['CH_{2}OH–(CHOH)_{4}–CHO'], x, y, o);
    if (f === 'developpee') return grille(ctx, [
      '    H   O  ', '     \\ //  ', '      C    ', '      |    ', '  H – C – OH', '      |    ', ' HO – C – H ', '      |    ',
      '  H – C – OH', '      |    ', '  H – C – OH', '      |    ', '  H – C – OH', '      |    ', '      H    '], x, y, { ...o, taille: (o.taille ?? 13) });
    if (f === 'cyclique') return cycleGlucose(ctx, x, y, o);
    const a = alphaEtat(o), u = Math.max(0, Math.min(1, o.coupe || 0)), ec = (o.ecart ?? PAS) * e * u;
    const pts = positionsChaine(6, x, y, o).map(([px, py], i) => {
      const s = i < 3 ? -1 : 1, an = o.angle || 0;
      return [px + s * ec * Math.cos(an), py + s * ec * Math.sin(an)];
    });
    chaine(ctx, pts, { echelle: e, alpha: a, liaisons: [1, 1, 1 - u, 1, 1] });
    return { atomes: pts, boite: boite(pts, R.C * e) };
  }
  /** Forme cyclique (celle du manuel, montrée une fois) : l'hexagone à 5 carbones et 1 oxygène, le 6e carbone en CH₂OH. */
  function cycleGlucose(ctx, x, y, o = {}) {
    const e = o.echelle ?? 1, r = 34 * e, a = o.alpha ?? 1, pts = [];
    for (let i = 0; i < 6; i++) { const an = -Math.PI / 2 + Math.PI / 6 + i * TAU / 6; pts.push([x + Math.cos(an) * r, y + Math.sin(an) * r * .62]); }
    for (let i = 0; i < 6; i++) liaison(ctx, pts[i][0], pts[i][1], pts[(i + 1) % 6][0], pts[(i + 1) % 6][1], { alpha: a, epaisseur: 4 * e });
    const c6 = [pts[5][0] - 4 * e, pts[5][1] - 30 * e];
    liaison(ctx, pts[5][0], pts[5][1], c6[0], c6[1], { alpha: a, epaisseur: 4 * e });
    pts.forEach(([px, py], i) => bille(ctx, px, py, (i === 0 ? R.O : R.C * .8) * e, i === 0 ? C.oxygene : C.carbone, { alpha: a }));
    bille(ctx, c6[0], c6[1], R.C * .8 * e, C.carbone, { alpha: a });
    return { atomes: pts.concat([c6]), boite: boite(pts.concat([c6]), R.C * e) };
  }
  /**
   * L'ACIDE PYRUVIQUE : 3 billes jaunes liées — la moitié de la chaîne du glucose, coupée dedans.
   * o.forme : 'billes' (défaut), 'brute' (C₃H₄O₃), 'semi_developpee' (CH₃–CO–COOH). o.alphas : par carbone (le 3e part en CO₂).
   */
  function acidePyruvique(ctx, x, y, o = {}) {
    const f = o.forme || 'billes', e = o.echelle ?? 1;
    if (f === 'brute') return formule(ctx, ['C_{3}H_{4}O_{3}'], x, y, o);
    if (f === 'semi_developpee') return formule(ctx, ['CH_{3}–CO–COOH'], x, y, o);
    const pts = positionsChaine(3, x, y, o);
    chaine(ctx, pts, { echelle: e, alpha: alphaEtat(o), liaisons: o.liaisons, alphas: o.alphas });
    return { atomes: pts, boite: boite(pts, R.C * e) };
  }
  /** Deux hydrogènes (billes blanches) posés au-dessus de (x, y) : ce que le NADH,H⁺ rend en fermentation. */
  function deuxH(ctx, x, y, e, a) {
    const pts = [[x - 10 * e, y - 19 * e], [x + 10 * e, y - 19 * e]];
    for (const [hx, hy] of pts) { liaison(ctx, x, y, hx, hy, { alpha: a * .8, epaisseur: 2.6 * e }); bille(ctx, hx, hy, R.H * e, C.hydrogene, { alpha: a }); }
    return pts;
  }
  /** L'ACIDE LACTIQUE : la chaîne de 3 carbones de l'acide pyruvique + 2 hydrogènes (blancs) sur le carbone du milieu. */
  function acideLactique(ctx, x, y, o = {}) {
    const f = o.forme || 'billes', e = o.echelle ?? 1, a = alphaEtat(o);
    if (f === 'brute') return formule(ctx, ['C_{3}H_{6}O_{3}'], x, y, o);
    if (f === 'semi_developpee') return formule(ctx, ['CH_{3}–CHOH–COOH'], x, y, o);
    const pts = positionsChaine(3, x, y, o);
    const h = deuxH(ctx, pts[1][0], pts[1][1], e, a);
    chaine(ctx, pts, { echelle: e, alpha: a });
    return { atomes: pts, hydrogenes: h, boite: boite(pts.concat(h), R.C * e) };
  }
  /** L'ÉTHANOL : 2 carbones (le 3e de l'acide pyruvique est parti en CO₂) + 2 hydrogènes entre eux. */
  function ethanol(ctx, x, y, o = {}) {
    const f = o.forme || 'billes', e = o.echelle ?? 1, a = alphaEtat(o);
    if (f === 'brute') return formule(ctx, ['C_{2}H_{6}O'], x, y, o);
    if (f === 'semi_developpee') return formule(ctx, ['CH_{3}–CH_{2}OH'], x, y, o);
    const pts = positionsChaine(2, x, y, o);
    const h = deuxH(ctx, x, y, e, a);
    chaine(ctx, pts, { echelle: e, alpha: a });
    return { atomes: pts, hydrogenes: h, boite: boite(pts.concat(h), R.C * e) };
  }
  /** Une molécule organique quelconque (RH₂, nutriment non nommé) : chaîne droite de n carbones (défaut 4, jamais 6 = glucose). */
  function moleculeOrganique(ctx, x, y, o = {}) {
    const e = o.echelle ?? 1, pts = positionsChaine(o.n ?? 4, x, y, o);
    chaine(ctx, pts, { echelle: e, alpha: alphaEtat(o) });
    return { atomes: pts, boite: boite(pts, R.C * e) };
  }

  /* ───────────────────────── Petites molécules minérales ───────────────────────── */
  /** LE DIOXYDE DE CARBONE : O = C = O, carbone JAUNE (il vient du glucose) entre deux oxygènes rouges ; o.bulle : sa bulle de gaz. */
  function co2(ctx, x, y, o = {}) {
    if (typeof o === 'number') o = { echelle: o, alpha: arguments[4] ?? 1 };   // ancienne signature co2(ctx, x, y, k, a)
    const k = o.echelle ?? 1, a = o.alpha ?? 1;
    if (a <= 0) return;
    liaison(ctx, x - 10 * k, y, x + 10 * k, y, { alpha: a, epaisseur: 3 * k });
    bille(ctx, x - 10 * k, y, 5 * k, C.oxygene, { alpha: a }); bille(ctx, x + 10 * k, y, 5 * k, C.oxygene, { alpha: a }); bille(ctx, x, y, 6 * k, C.carbone, { alpha: a });
    if (o.bulle) bulleGaz(ctx, x, y, 16 * k);
    return { boite: { x: x - 16 * k, y: y - 7 * k, w: 32 * k, h: 14 * k } };
  }
  /** L'EAU : un oxygène rouge et deux hydrogènes blancs en V. */
  function h2o(ctx, x, y, o = {}) {
    const k = o.echelle ?? 1, a = o.alpha ?? 1;
    if (a <= 0) return;
    bille(ctx, x - 6 * k, y + 5 * k, 3.6 * k, C.hydrogene, { alpha: a }); bille(ctx, x + 6 * k, y + 5 * k, 3.6 * k, C.hydrogene, { alpha: a });
    bille(ctx, x, y, 6 * k, C.oxygene, { alpha: a });
    return { boite: { x: x - 10 * k, y: y - 6 * k, w: 20 * k, h: 15 * k } };
  }
  /** LE DIOXYGÈNE : deux oxygènes rouges liés ; o.demi : un seul atome (½ O₂). */
  function o2(ctx, x, y, o = {}) {
    const k = o.echelle ?? 1, a = o.alpha ?? 1;
    if (a <= 0) return;
    if (o.demi) { bille(ctx, x, y, 6 * k, C.oxygene, { alpha: a }); return { boite: { x: x - 6 * k, y: y - 6 * k, w: 12 * k, h: 12 * k } }; }
    liaison(ctx, x - 6 * k, y, x + 6 * k, y, { alpha: a, epaisseur: 3 * k });
    bille(ctx, x - 6 * k, y, 6 * k, C.oxygene, { alpha: a }); bille(ctx, x + 6 * k, y, 6 * k, C.oxygene, { alpha: a });
    return { boite: { x: x - 12 * k, y: y - 6 * k, w: 24 * k, h: 12 * k } };
  }
  /** Un HYDROGÈNE (atome H transporté) : petite bille blanche. */
  function hydrogene(ctx, x, y, o = {}) { const k = o.echelle ?? 1; bille(ctx, x, y, R.H * k, C.hydrogene, { alpha: o.alpha ?? 1 }); }
  /** Un PROTON / ion H⁺ : bille rose marquée « H+ » (o.texte : false pour une bille trop petite ; o.nom : « p » dans un noyau). */
  function proton(ctx, x, y, o = {}) {
    const r = (o.r ?? 7) * (o.echelle ?? 1), a = o.alpha ?? 1;
    bille(ctx, x, y, r, C.proton, { alpha: a });
    if (o.texte !== false && r >= 6) etiquette(ctx, o.nom ?? 'H+', x, y, { taille: Math.max(9, r * 1.3), couleur: '#3b0a24', alpha: a });
  }
  /** Un ÉLECTRON : petite bille bleu ciel marquée « e− ». */
  function electron(ctx, x, y, o = {}) {
    const r = (o.r ?? 6) * (o.echelle ?? 1), a = o.alpha ?? 1;
    bille(ctx, x, y, r, C.electron, { alpha: a });
    if (o.texte !== false && r >= 5.5) etiquette(ctx, 'e−', x, y, { taille: Math.max(9, r * 1.5), couleur: '#06283d', alpha: a });
  }
  /** Un NEUTRON : bille grise (noyau atomique). */
  function neutron(ctx, x, y, o = {}) {
    const r = (o.r ?? 7) * (o.echelle ?? 1), a = o.alpha ?? 1;
    bille(ctx, x, y, r, C.neutron, { alpha: a });
    if (o.texte && r >= 6) etiquette(ctx, 'n', x, y, { taille: r * 1.3, alpha: a });
  }
  /** L'ion OXONIUM H₃O⁺ : l'eau (O rouge + H blancs) avec un 3e H et la charge + (anneau rose). */
  function h3o(ctx, x, y, o = {}) {
    const k = o.echelle ?? 1, a = o.alpha ?? 1;
    ctx.save(); ctx.globalAlpha *= a; ctx.strokeStyle = rgba(C.proton, .8); ctx.lineWidth = 1.6 * k; ctx.beginPath(); ctx.arc(x, y + 1 * k, 13 * k, 0, TAU); ctx.stroke(); ctx.restore();
    for (const an of [-Math.PI / 2, Math.PI / 6, 5 * Math.PI / 6]) bille(ctx, x + Math.cos(an) * 7 * k, y + Math.sin(an) * 7 * k, 3.6 * k, C.hydrogene, { alpha: a });
    bille(ctx, x, y, 6 * k, C.oxygene, { alpha: a });
    if (o.texte !== false) etiquette(ctx, '+', x + 13 * k, y - 11 * k, { taille: 13 * k, couleur: '#f9a8d4', alpha: a });
    return { boite: { x: x - 14 * k, y: y - 14 * k, w: 28 * k, h: 28 * k } };
  }
  /** L'ion HYDROXYDE HO⁻ : un O rouge, un H blanc, la charge − (anneau bleu ciel). */
  function ho(ctx, x, y, o = {}) {
    const k = o.echelle ?? 1, a = o.alpha ?? 1;
    ctx.save(); ctx.globalAlpha *= a; ctx.strokeStyle = rgba(C.electron, .8); ctx.lineWidth = 1.6 * k; ctx.beginPath(); ctx.arc(x - 2 * k, y, 12 * k, 0, TAU); ctx.stroke(); ctx.restore();
    bille(ctx, x + 6 * k, y - 4 * k, 3.6 * k, C.hydrogene, { alpha: a });
    bille(ctx, x - 2 * k, y, 6 * k, C.oxygene, { alpha: a });
    if (o.texte !== false) etiquette(ctx, '−', x + 11 * k, y - 11 * k, { taille: 14 * k, couleur: '#7dd3fc', alpha: a });
    return { boite: { x: x - 14 * k, y: y - 12 * k, w: 26 * k, h: 24 * k } };
  }

  /* ───────────────────────── Énergie : ATP, ADP, Pi ───────────────────────── */
  /**
   * L'ATP : une CARTE d'énergie dorée marquée « ATP » (forme 'carte', défaut, 50 × 22 à l'échelle 1) ; o.etat 'adp' : carte
   * grise « ADP » (déchargée). Forme 'bille' (foule de molécules, sans texte) : bille dorée qui brille ; l'ADP y est une bille
   * grise suivie d'un petit Pi orange. Forme 'developpee' : adénosine (violet) + 3 phosphates orange en chaîne.
   */
  function atp(ctx, x, y, o = {}) {
    const f = o.forme || 'carte', k = o.echelle ?? 1, a = o.alpha ?? 1, adp = o.etat === 'adp';
    if (a <= .02) return;
    if (f === 'bille') {
      if (adp) { bille(ctx, x, y, 5.5 * k, C.adp, { alpha: a }); bille(ctx, x + 9 * k, y + 2 * k, 3.4 * k, C.pi, { alpha: a }); }
      else { bille(ctx, x, y, 6.5 * k, C.atp, { alpha: a }); if (o.eclat !== false) eclat(ctx, x, y, 12 * k, .35 * a); }
      return { boite: { x: x - 7 * k, y: y - 7 * k, w: 14 * k, h: 14 * k } };
    }
    if (f === 'developpee') {
      const n = adp ? 2 : 3, w = 60 * k, h = 30 * k, pr = 10 * k;
      proteine(ctx, x - w / 2, y, w, h, { couleur: C.adenosine, alpha: a });
      etiquette(ctx, 'adénosine', x - w / 2, y, { taille: 13 * k, couleur: '#1a0838', alpha: a });
      for (let i = 0; i < n; i++) { const px = x + 14 * k + i * 24 * k; liaison(ctx, px - 24 * k + (i ? 0 : 8 * k), y, px, y, { alpha: a, epaisseur: 4 * k }); }
      for (let i = 0; i < n; i++) { const px = x + 14 * k + i * 24 * k; bille(ctx, px, y, pr, C.pi, { alpha: a }); etiquette(ctx, 'P', px, y, { taille: 12 * k, couleur: '#2a1400', alpha: a }); }
      return { boite: { x: x - w, y: y - h / 2, w: w + 14 * k + n * 24 * k, h } };
    }
    const w = (o.w ?? 50) * k, h = (o.h ?? 22) * k;
    proteine(ctx, x, y, w, h, { couleur: adp ? C.adp : C.atp, alpha: .85 * a });
    if (o.texte !== false) etiquette(ctx, adp ? 'ADP' : 'ATP', x, y, { taille: (o.taille ?? 15) * k, couleur: adp ? '#f8fafc' : '#3c2800', alpha: a });
    return { boite: { x: x - w / 2, y: y - h / 2, w, h } };
  }
  /** Le PHOSPHATE inorganique Pi : bille orange marquée « Pi ». */
  function pi(ctx, x, y, o = {}) {
    const r = (o.r ?? 8) * (o.echelle ?? 1), a = o.alpha ?? 1;
    bille(ctx, x, y, r, C.pi, { alpha: a });
    if (o.texte !== false && r >= 7) etiquette(ctx, 'Pi', x, y, { taille: Math.max(9, r * 1.15), couleur: '#2a1400', alpha: a });
    return { boite: { x: x - r, y: y - r, w: 2 * r, h: 2 * r } };
  }

  /* ───────────────────────── Transporteurs d'hydrogène (« taxis ») ───────────────────────── */
  function taxi(ctx, x, y, o, couleur, vide, plein) {
    const k = o.echelle ?? 1, a = o.alpha ?? 1, charge = o.etat === 'reduit', h = (o.h ?? 24) * k;
    const w = (o.w ?? (charge ? o.wPlein : o.wVide)) * k;
    if (a <= .02) return;
    capsule(ctx, x, y, w, h, couleur, { alpha: a, lueur: charge ? (o.lueur ?? 1) : 0 });
    if (o.texte !== false) etiquette(ctx, charge ? plein : vide, x, y, { taille: (o.taille ?? 15) * k, alpha: a });
    return { boite: { x: x - w / 2, y: y - h / 2, w, h } };
  }
  /** Le NAD⁺ (etat 'oxyde', capsule cyan courte « NAD+ ») / NADH,H⁺ (etat 'reduit', capsule cyan longue et lumineuse). */
  const nad = (ctx, x, y, o = {}) => taxi(ctx, x, y, { wVide: 54, wPlein: 82, ...o }, C.nad, 'NAD+', 'NADH,H+');
  /** Le FAD (etat 'oxyde') / FADH₂ (etat 'reduit') : capsule VERTE (l'autre taxi). */
  const fad = (ctx, x, y, o = {}) => taxi(ctx, x, y, { wVide: 48, wPlein: 70, ...o }, C.fad, 'FAD', 'FADH_{2}');
  /** Le coenzyme A : capsule indigo « CoA ». */
  const coa = (ctx, x, y, o = {}) => taxi(ctx, x, y, { wVide: 48, wPlein: 48, ...o, etat: 'oxyde' }, C.coa, 'CoA', 'CoA');

  window.Lexique = {
    version: '2026-11-18', T, C, R, PAS, POLICE, ENCRE, graine, rgba,
    // peinture de base
    bille, liaison, capsule, eclat, bulleGaz, etiquette, formule,
    // milieux vivants
    cellule, mitochondrie, cheminCretes, membrane, proteine, spherePedonculee, becher, levure,
    // atomes et molécules
    atome, positionsChaine, chaine, glucose, acidePyruvique, acideLactique, ethanol, moleculeOrganique,
    co2, h2o, o2, hydrogene, proton, electron, neutron, h3o, ho,
    atp, pi, nad, fad, coa,
  };
})();
