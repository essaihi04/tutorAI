/*
 * LEXIQUE VISUEL COMMUN — CHIMIE (18 novembre 2026 ; skill simulations-au-tableau règle 15, professeur règle 43).
 * Fiches : docs/lexique-visuel/ (becher, ph-metre, conductimetre, verrerie, solutions, + les atomes et ions de lexique.js).
 * La verrerie et les appareils les plus répandus des cours de chimie, copiés mot pour mot (aucune page ne change d'aspect) :
 *
 *   <script src="/media/simulations/shared/lexique/lexique-chimie.js"></script>
 *   Lexique.chimie.becher(ctx, {x, y, w, h}, niveau, [r, g, b, a])   // bécher peint (renvoie la hauteur de la surface)
 *   Lexique.chimie.phmetre(c, {x, y, w, h}, '3,4')                    // pH-mètre (objet Craie : il peint dans c.direct)
 *   Lexique.chimie.appareil(c, {x, y, w, h}, '2,49 mS')               // conductimètre
 *   Lexique.chimie.SOLUTIONS.incolore, Lexique.chimie.BBT.jaune        // les teintes des solutions
 * Les atomes, molécules et ions (C jaune, H blanc, O rouge, H⁺ rose, H₃O⁺, HO⁻, électron) sont dans lexique.js.
 */
(function () {
  'use strict';
  window.Lexique = window.Lexique || {};
  if (window.Lexique.chimie) return;
  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
  const lerp = (a, b, f) => a + (b - a) * f;
  const rgba = ([r, g, b, a], k = 1) => `rgba(${Math.round(r)},${Math.round(g)},${Math.round(b)},${(a * k).toFixed(3)})`;
  const eclair = (c, k) => [lerp(c[0], 255, k), lerp(c[1], 255, k), lerp(c[2], 255, k), c[3]];
  const sombre = (c, k) => [c[0] * (1 - k), c[1] * (1 - k), c[2] * (1 - k), Math.min(1, c[3] * (1 + k * .4))];
  const ecranPH = A => ({ x: A.x + 10, y: A.y + 9, w: A.w - 20, h: 34 });

  /* ── Verrerie peinte ── */
  const Peint = {
    sphere(ctx, x, y, r, [clair, milieu, foncé], a = 1) {
      ctx.save(); ctx.globalAlpha = a;
      const g = ctx.createRadialGradient(x - r * .35, y - r * .4, r * .1, x, y, r); g.addColorStop(0, clair); g.addColorStop(.45, milieu); g.addColorStop(1, foncé);
      ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.fill(); ctx.restore();
    },
    /** Bécher vu de face : verre, solution (dégradé, ménisque, reflet), bec, graduations. niveau 0 → 1. */
    becher(ctx, B, niveau, col, a = 1) {
      // Bécher repeint (16 novembre 2026, « plus réaliste, couleurs vives ») : verre net à bord ourlé, eau claire et lumineuse
      // (une solution incolore se voit comme de l'eau légèrement bleutée, plus un voile gris), ménisque, reflets francs.
      const { x, y, w, h } = B, ep = 3, fond = y + h, yS = fond - ep - niveau * (h - 16);
      // Solution incolore (ou presque) : peinte comme une eau claire un peu bleutée ; le bleu s'efface en douceur dès qu'une teinte apparaît.
      const pale = Math.min(col[0], col[1], col[2]) >= 180 ? Math.min(1, Math.max(0, (.27 - col[3]) / .1)) : 0;
      const c3 = pale > 0 ? [col[0] + (112 - col[0]) * pale, col[1] + (194 - col[1]) * pale, col[2] + (248 - col[2]) * pale, col[3] + (.36 - col[3]) * pale] : col;
      ctx.save(); ctx.globalAlpha = a;
      ctx.fillStyle = 'rgba(0,0,0,.26)'; ctx.beginPath(); ctx.ellipse(x + w / 2 + 3, fond + 4, w / 2, 4.5, 0, 0, 7); ctx.fill();
      ctx.fillStyle = 'rgba(200,228,250,.07)'; ctx.beginPath(); ctx.roundRect(x, y, w, h, [2, 2, 10, 10]); ctx.fill();
      if (niveau > .004) {
        ctx.save(); ctx.beginPath(); ctx.roundRect(x + ep, y, w - 2 * ep, h - ep, [0, 0, 8, 8]); ctx.clip();
        const g = ctx.createLinearGradient(x, 0, x + w, 0);
        g.addColorStop(0, rgba(sombre(c3, .3))); g.addColorStop(.3, rgba(eclair(c3, .12))); g.addColorStop(.62, rgba(eclair(c3, .3))); g.addColorStop(1, rgba(sombre(c3, .28)));
        ctx.fillStyle = g; ctx.fillRect(x, yS, w, fond - yS);
        const v = ctx.createLinearGradient(0, yS, 0, fond); v.addColorStop(0, 'rgba(255,255,255,.1)'); v.addColorStop(.5, 'rgba(255,255,255,0)'); v.addColorStop(1, 'rgba(0,0,0,.16)');
        ctx.fillStyle = v; ctx.fillRect(x, yS, w, fond - yS);
        ctx.fillStyle = 'rgba(255,255,255,.1)'; ctx.fillRect(x + w * .64, yS + 5, w * .08, Math.max(0, fond - yS - 10));
        ctx.restore();
        ctx.fillStyle = rgba(eclair(c3, .45), 1.25); ctx.beginPath(); ctx.ellipse(x + w / 2, yS, w / 2 - ep, 3.2, 0, 0, 7); ctx.fill();
        ctx.strokeStyle = 'rgba(255,255,255,.5)'; ctx.lineWidth = 1; ctx.beginPath(); ctx.ellipse(x + w / 2, yS, w / 2 - ep - 1, 3.2, 0, Math.PI * 1.05, Math.PI * 1.95); ctx.stroke();
      }
      ctx.fillStyle = 'rgba(220,238,250,.3)'; ctx.fillRect(x + 8, fond - 3, w - 16, 3);
      ctx.strokeStyle = 'rgba(232,243,252,.9)'; ctx.lineWidth = 2.2; ctx.lineJoin = 'round'; ctx.lineCap = 'round';
      ctx.beginPath(); ctx.moveTo(x - 6, y - 4); ctx.quadraticCurveTo(x - 1, y - 2, x, y + 5); ctx.lineTo(x, fond - 10); ctx.quadraticCurveTo(x, fond, x + 10, fond);
      ctx.lineTo(x + w - 10, fond); ctx.quadraticCurveTo(x + w, fond, x + w, fond - 10); ctx.lineTo(x + w, y); ctx.stroke();
      ctx.strokeStyle = 'rgba(240,248,255,.55)'; ctx.lineWidth = 1.4; ctx.beginPath(); ctx.ellipse(x + w / 2, y + 1, w / 2, 2.4, 0, 0, Math.PI); ctx.stroke();
      const gl = ctx.createLinearGradient(x + w * .09, 0, x + w * .2, 0); gl.addColorStop(0, 'rgba(255,255,255,.34)'); gl.addColorStop(1, 'rgba(255,255,255,0)');
      ctx.fillStyle = gl; ctx.fillRect(x + w * .09, y + 12, w * .11, h - 28);
      ctx.strokeStyle = 'rgba(232,243,252,.5)'; ctx.lineWidth = 1;
      for (let k = 1; k <= 4; k++) { const gy = fond - 8 - k * (h - 24) / 5; ctx.beginPath(); ctx.moveTo(x + w - (k % 2 ? 12 : 16), gy); ctx.lineTo(x + w - 4, gy); ctx.stroke(); }
      ctx.restore();
      return yS;
    },
    /** Eau d’un bain (cristallisoir) peinte PAR-DESSUS le bécher : il paraît plongé dedans. */
    bain(ctx, B, ySurf, col, a = 1) {
      const { x, y, w, h } = B, fond = y + h;
      ctx.save(); ctx.globalAlpha = a;
      const g = ctx.createLinearGradient(0, ySurf, 0, fond); g.addColorStop(0, rgba(eclair(col, .2))); g.addColorStop(1, rgba(sombre(col, .3)));
      ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(x + 3, ySurf, w - 6, fond - ySurf - 3, [0, 0, 12, 12]); ctx.fill();
      ctx.strokeStyle = 'rgba(255,255,255,.3)'; ctx.lineWidth = 1.2; ctx.beginPath(); ctx.moveTo(x + 5, ySurf); ctx.lineTo(x + w - 5, ySurf); ctx.stroke();
      ctx.strokeStyle = 'rgba(225,238,250,.7)'; ctx.lineWidth = 2.2;
      ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x, fond - 14); ctx.quadraticCurveTo(x, fond, x + 14, fond); ctx.lineTo(x + w - 14, fond); ctx.quadraticCurveTo(x + w, fond, x + w, fond - 14); ctx.lineTo(x + w, y); ctx.stroke();
      ctx.fillStyle = 'rgba(255,255,255,.1)'; ctx.fillRect(x + 7, y + 8, 4, h - 22);
      ctx.restore();
    },
    goutte(ctx, x, y, col, a = 1) {
      ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = rgba(col, 1.5);
      ctx.beginPath(); ctx.moveTo(x, y - 6); ctx.quadraticCurveTo(x + 4, y, x, y + 3.5); ctx.quadraticCurveTo(x - 4, y, x, y - 6); ctx.fill();
      ctx.fillStyle = 'rgba(255,255,255,.6)'; ctx.fillRect(x - 1.2, y - 1, 1.2, 1.6); ctx.restore();
    },
    /** Filet de liquide qui coule (versement). */
    filet(ctx, x, y1, y2, col, a = 1) { ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = rgba(col, 2.2); ctx.fillRect(x - 1.6, y1, 3.2, y2 - y1); ctx.restore(); },
    /** Compte-gouttes (pointe en (x, yp)), poire noire. */
    compteGouttes(ctx, x, yp, col, a = 1) {
      ctx.save(); ctx.globalAlpha = a;
      ctx.fillStyle = rgba(col, 1.4); ctx.fillRect(x - 2.5, yp - 30, 5, 26);
      ctx.strokeStyle = 'rgba(225,238,250,.85)'; ctx.lineWidth = 1.5;
      ctx.beginPath(); ctx.moveTo(x - 1, yp); ctx.lineTo(x - 4, yp - 14); ctx.lineTo(x - 4, yp - 46); ctx.moveTo(x + 1, yp); ctx.lineTo(x + 4, yp - 14); ctx.lineTo(x + 4, yp - 46); ctx.stroke();
      const g = ctx.createRadialGradient(x - 3, yp - 58, 1, x, yp - 54, 11); g.addColorStop(0, '#6b6b6b'); g.addColorStop(.5, '#2a2a2a'); g.addColorStop(1, '#050505');
      ctx.fillStyle = g; ctx.beginPath(); ctx.ellipse(x, yp - 56, 7.5, 11, 0, 0, 7); ctx.fill();
      ctx.restore();
    },
    /** Pipette jaugée (pointe en (x, yp)), poire rouge en haut ; `rempli` 0 → 1 de solution `col`. */
    pipette(ctx, x, yp, rempli, col, a = 1) {
      if (a <= 0) return;
      const L = 92, yH = yp - L;
      ctx.save(); ctx.globalAlpha = a;
      if (rempli > 0) { ctx.fillStyle = rgba(col, 1.2); ctx.fillRect(x - 2.4, yp - 4 - rempli * (L - 26), 4.8, rempli * (L - 26)); }
      ctx.strokeStyle = 'rgba(225,238,250,.85)'; ctx.lineWidth = 1.6;
      ctx.beginPath(); ctx.moveTo(x - 1.2, yp); ctx.lineTo(x - 3.5, yp - 10); ctx.lineTo(x - 3.5, yH + 18); ctx.moveTo(x + 1.2, yp); ctx.lineTo(x + 3.5, yp - 10); ctx.lineTo(x + 3.5, yH + 18); ctx.stroke();
      ctx.strokeStyle = 'rgba(255,255,255,.7)'; ctx.beginPath(); ctx.moveTo(x - 5, yp - 58); ctx.lineTo(x + 5, yp - 58); ctx.stroke();   // trait de jauge
      const g = ctx.createRadialGradient(x - 3, yH + 4, 1, x, yH + 8, 11); g.addColorStop(0, '#ff9a8a'); g.addColorStop(.5, '#d33a2c'); g.addColorStop(1, '#6e1209');
      ctx.fillStyle = g; ctx.beginPath(); ctx.ellipse(x, yH + 8, 8, 11, 0, 0, 7); ctx.fill();
      ctx.fillStyle = '#8e1d12'; ctx.fillRect(x - 4, yH + 17, 8, 4);
      ctx.restore();
    },
    glacon(ctx, x, y, s, ang, a = 1) {
      ctx.save(); ctx.globalAlpha = a; ctx.translate(x, y); ctx.rotate(ang);
      const g = ctx.createLinearGradient(-s / 2, -s / 2, s / 2, s / 2); g.addColorStop(0, 'rgba(245,252,255,.85)'); g.addColorStop(1, 'rgba(170,215,240,.55)');
      ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(-s / 2, -s / 2, s, s * .85, 4); ctx.fill();
      ctx.strokeStyle = 'rgba(255,255,255,.85)'; ctx.lineWidth = 1; ctx.stroke();
      ctx.fillStyle = 'rgba(255,255,255,.7)'; ctx.fillRect(-s / 2 + 3, -s / 2 + 3, s * .3, 2);
      ctx.restore();
    }
  };

  /* ── Appareils (pH-mètre, sonde, conductimètre et sa cellule, bulles de gaz) ── */
  function phmetre(c, A, texte) {
    c.direct(() => {
      const ctx = c.ctx, { x, y, w, h } = A; ctx.save();
      ctx.fillStyle = 'rgba(0,0,0,.25)'; ctx.beginPath(); ctx.roundRect(x + 4, y + 5, w, h, 9); ctx.fill();
      const g = ctx.createLinearGradient(0, y, 0, y + h); g.addColorStop(0, '#a9b1b8'); g.addColorStop(1, '#6b737b');
      ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(x, y, w, h, 9); ctx.fill();
      ctx.strokeStyle = 'rgba(255,255,255,.35)'; ctx.lineWidth = 1.2; ctx.stroke();
      const e = { x: x + 10, y: y + 9, w: w - 20, h: 34 }, ge = ctx.createLinearGradient(0, e.y, 0, e.y + e.h); ge.addColorStop(0, '#b9f0a0'); ge.addColorStop(1, '#79c36a');
      ctx.fillStyle = ge; ctx.beginPath(); ctx.roundRect(e.x, e.y, e.w, e.h, 4); ctx.fill();
      ctx.fillStyle = 'rgba(255,255,255,.25)'; ctx.fillRect(e.x + 3, e.y + 3, e.w - 6, 3);
      ctx.fillStyle = '#12300c'; ctx.font = '700 21px "Courier New", monospace'; ctx.textAlign = 'right'; ctx.textBaseline = 'middle';
      ctx.fillText(texte, e.x + e.w - 7, e.y + e.h / 2 + 1);
      ctx.fillStyle = '#05080b'; ctx.font = '700 13px Arial, sans-serif'; ctx.textAlign = 'left'; ctx.fillText('pH-mètre', x + 10, y + h - 10);
      Peint.sphere(ctx, x + w - 16, y + h - 12, 5.5, ['#e5e9ec', '#9aa3ab', '#4a5158']);
      ctx.restore();
    });
  }
  function sonde(ctx, x, yH, yB) {
    ctx.save();
    ctx.fillStyle = '#2f353b'; ctx.beginPath(); ctx.roundRect(x - 6, yH, 12, 22, 3); ctx.fill();
    const g = ctx.createLinearGradient(x - 5, 0, x + 5, 0); g.addColorStop(0, 'rgba(210,230,250,.35)'); g.addColorStop(.5, 'rgba(240,248,255,.12)'); g.addColorStop(1, 'rgba(210,230,250,.4)');
    ctx.fillStyle = g; ctx.fillRect(x - 5, yH + 22, 10, yB - yH - 28);
    ctx.strokeStyle = 'rgba(225,238,250,.8)'; ctx.lineWidth = 1.2; ctx.strokeRect(x - 5, yH + 22, 10, yB - yH - 28);
    const gb = ctx.createRadialGradient(x - 2, yB - 4, 1, x, yB - 2, 7); gb.addColorStop(0, 'rgba(255,255,255,.75)'); gb.addColorStop(1, 'rgba(190,215,240,.35)');
    ctx.fillStyle = gb; ctx.beginPath(); ctx.arc(x, yB - 3, 6.5, 0, 7); ctx.fill(); ctx.strokeStyle = 'rgba(225,238,250,.85)'; ctx.stroke();
    ctx.fillStyle = 'rgba(160,170,180,.7)'; ctx.fillRect(x - 1, yH + 26, 2, yB - yH - 34);
    ctx.restore();
  }
  function appareil(c, A, texte, o = {}) {
    c.direct(() => {
      const ctx = c.ctx, { x, y, w, h } = A; ctx.save();
      ctx.fillStyle = 'rgba(0,0,0,.25)'; ctx.beginPath(); ctx.roundRect(x + 4, y + 5, w, h, 9); ctx.fill();
      const g = ctx.createLinearGradient(0, y, 0, y + h); g.addColorStop(0, '#4d565f'); g.addColorStop(1, '#22272d');
      ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(x, y, w, h, 9); ctx.fill();
      ctx.strokeStyle = 'rgba(255,255,255,.25)'; ctx.lineWidth = 1.2; ctx.stroke();
      const e = ecran(A), ge = ctx.createLinearGradient(0, e.y, 0, e.y + e.h); ge.addColorStop(0, '#c2e0ae'); ge.addColorStop(1, '#8fb47c');
      ctx.fillStyle = ge; ctx.beginPath(); ctx.roundRect(e.x, e.y, e.w, e.h, 4); ctx.fill();
      ctx.fillStyle = 'rgba(255,255,255,.25)'; ctx.fillRect(e.x + 3, e.y + 3, e.w - 6, 3);
      ctx.fillStyle = '#16260f'; ctx.font = `700 ${o.taille ?? 21}px "Courier New", monospace`; ctx.textAlign = 'right'; ctx.textBaseline = 'middle';
      ctx.fillText(texte, e.x + e.w - 7, e.y + e.h / 2 + 1);
      for (let i = 0; i < 2; i++) Peint.sphere(ctx, x + 18 + i * 22, y + h - 13, 6, ['#e5e9ec', '#9aa3ab', '#4a5158']);
      ctx.restore();
    });
  }
  function cellule(ctx, cx, yH, yP, L = 26, hp = 46) {
    ctx.save();
    const g = ctx.createLinearGradient(cx - 12, 0, cx + 12, 0); g.addColorStop(0, '#2c3238'); g.addColorStop(.4, '#6b747d'); g.addColorStop(1, '#22272c');
    ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(cx - 9, yH, 18, yP - yH, 3); ctx.fill();
    for (const s of [-1, 1]) {
      const px = cx + s * L / 2 - (s < 0 ? 5 : 0), gp = ctx.createLinearGradient(px, 0, px + 5, 0);
      gp.addColorStop(0, '#8e979f'); gp.addColorStop(.5, '#eef2f5'); gp.addColorStop(1, '#7b848c');
      ctx.fillStyle = gp; ctx.fillRect(px, yP, 5, hp);
      ctx.fillStyle = '#3a4046'; ctx.fillRect(cx + s * 6 - 1.5, yP - 2, 3, 6);
      ctx.fillRect(Math.min(cx + s * 6, px + 2.5) - 1, yP, Math.abs(px + 2.5 - (cx + s * 6)) + 2, 3);
    }
    ctx.restore();
  }
  function bulles(ctx, x0, x1, yb, ys, t, k, n = 10) {
    if (k <= 0) return;
    ctx.save();
    for (let i = 0; i < n; i++) {
      if (i / n > k) break;
      const ph = ((t * (.5 + (i * 37 % 10) / 20) + i * .29) % 1 + 1) % 1, y = yb - ph * (yb - ys), x = x0 + ((i * 53 % 17) / 17) * (x1 - x0) + Math.sin(t * 3 + i) * 2.5, r = 1.6 + ph * 2.2;
      ctx.strokeStyle = 'rgba(240,248,255,.75)'; ctx.lineWidth = 1; ctx.fillStyle = 'rgba(220,240,255,.18)';
      ctx.beginPath(); ctx.arc(x, y, r, 0, 7); ctx.fill(); ctx.stroke();
      ctx.fillStyle = 'rgba(255,255,255,.8)'; ctx.fillRect(x - r * .45, y - r * .5, 1, 1);
    }
    ctx.restore();
  }

  /* Les teintes des solutions (une seule valeur par sens) : incolore = eau claire un peu bleutée ; BBT ; ions colorés. */
  const SOLUTIONS = { incolore: [112, 194, 248, .36], cuivre: [58, 123, 213, .84], permanganate: [123, 42, 140, .9], diiode: [138, 75, 18, .9] };
  const BBT = { jaune: [246, 206, 42, .62], vert: [64, 168, 84, .6], bleu: [44, 96, 208, .64] };

  window.Lexique.chimie = Object.assign(Peint, { phmetre, ecranPH, sonde, appareil, conductimetre: appareil, cellule, bulles, SOLUTIONS, BBT, rgba, eclair, sombre });
})();
