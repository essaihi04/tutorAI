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


  /* ══ Le laboratoire de la synthèse (25 novembre 2026, cours /TCF « Synthèse d’une espèce chimique ») ══════════════
   * Fiches : docs/lexique-visuel/montage-reflux.md, ccm.md, filtration.md. Copiés mot pour mot du cours (aucune page ne
   * change d’aspect) ; chaque cours qui chauffe à reflux, fait une CCM ou filtre les dessine PAR ICI :
   *   Lexique.chimie.montageReflux(ctx, cx, yTable, { s, k, couches, ponce, bulles, agite, chaud, phase, ouvert, vapeur })
   *   ballon, refrigerant (eau froide : entrée EN BAS, sortie EN HAUT), potence, chauffeBallon, elevateur, tuyau, ponce,
   *   gouttelette, vapeur, flacon (+ picto corrosif), eprouvette, tube, thermometre, balance, flocons (précipité),
   *   entonnoir (+ papier filtre : la filtration), plaque (CCM), cuve + cuveDevant (cuve de chromatographie), capillaire,
   *   lampeUV, diiode ; LIQUIDES : les teintes des liquides (huile dorée, éthanol, soude, mélange, eau salée, éluant…).
   * Coordonnées du cadre virtuel, contexte brut (dans craie.direct). */
  const Labo = (function () {
    const TAU = Math.PI * 2, L = {};
    function graine(seed) { let s = (seed >>> 0) || 1; return () => { s = (Math.imul(s, 1664525) + 1013904223) >>> 0; return s / 4294967296; }; }
    const rgba = ([r, g, b, a = 1], k = 1) => `rgba(${Math.round(r)},${Math.round(g)},${Math.round(b)},${Math.max(0, Math.min(1, a * k)).toFixed(3)})`;
    const clair = (c, k) => [c[0] + (255 - c[0]) * k, c[1] + (255 - c[1]) * k, c[2] + (255 - c[2]) * k, c[3] ?? 1];
    const fonce = (c, k) => [c[0] * (1 - k), c[1] * (1 - k), c[2] * (1 - k), c[3] ?? 1];
    /** Les teintes des liquides (toujours les mêmes) : huile dorée, éthanol et soude incolores (eau un peu bleutée),
     *  mélange réactionnel jaune pâle, eau salée, éluant, eau du réfrigérant. */
    L.LIQUIDES = {
      huile: [234, 179, 8, .72], ethanol: [186, 230, 253, .34], soude: [167, 214, 248, .40], melange: [250, 224, 140, .60],
      savonneux: [254, 243, 199, .70], salee: [147, 197, 253, .42], eau: [96, 165, 250, .45], eluant: [191, 219, 254, .45],
      produit: [253, 224, 71, .55], acide: [220, 252, 231, .40], alcool: [224, 231, 255, .40],
    };
    L.ombre = (ctx, fn, b = 6) => { ctx.save(); ctx.shadowColor = 'rgba(0,0,0,.35)'; ctx.shadowBlur = b; ctx.shadowOffsetX = 2; ctx.shadowOffsetY = 2; fn(); ctx.restore(); };
    function boule(ctx, x, y, r, c0, c1, c2) {
      const g = ctx.createRadialGradient(x - r * .35, y - r * .4, r * .1, x, y, r);
      g.addColorStop(0, c0); g.addColorStop(.55, c1); g.addColorStop(1, c2);
      ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.fill();
    }
    /** Texte écrit SUR un objet clair (étiquette d’un flacon, afficheur) : foncé et gras. */
    L.ecrit = (ctx, s, x, y, taille = 14, couleur = '#0b1f2a', align = 'center') => {
      ctx.save(); ctx.font = `700 ${taille}px ${(window.Tableau && window.Tableau.POLICE) || 'sans-serif'}`; ctx.fillStyle = couleur; ctx.textAlign = align; ctx.textBaseline = 'middle';
      ctx.fillText(s, x, y); ctx.restore();
    };
    function liquide(ctx, forme, x0, x1, ys, yb, col, menisque = true) {
      ctx.save(); forme(); ctx.clip();
      const g = ctx.createLinearGradient(x0, 0, x1, 0);
      g.addColorStop(0, rgba(fonce(col, .5), 1.35)); g.addColorStop(.42, rgba(clair(col, .2))); g.addColorStop(1, rgba(fonce(col, .5), 1.35));
      ctx.fillStyle = g; ctx.fillRect(x0 - 2, ys, x1 - x0 + 4, yb - ys + 2);
      ctx.restore();
      if (menisque) { ctx.fillStyle = rgba(clair(col, .45), 1.2); ctx.beginPath(); ctx.ellipse((x0 + x1) / 2, ys, Math.max(1, (x1 - x0) / 2 - 1), 2.6, 0, 0, TAU); ctx.fill(); }
    }
    L.liquide = liquide;
    /**
     * Le ballon (fond rond) : même dessin que le ballon réactionnel de la chimie de 2ᵉ Bac (chimie/shared/chem-lab.js) —
     * verre net, reflet en arc, col droit. (x, y) = centre de la panse, r = rayon.
     * o.couches = [{ f, col }] du bas vers le haut (f = fraction de la hauteur de la panse), o.ponce = grains au fond,
     * o.bulles = phase (s) de l'ébullition, o.agite (0..1) = force de l'ébullition, o.flocons.
     * Renvoie { haut } : le haut du col (où se pose le réfrigérant).
     */
    L.ballon = (ctx, x, y, r, o = {}) => {
      const lc = r * .3, th = Math.asin(lc / r), yN = y - r * Math.cos(th), haut = y - r * 1.75;
      const forme = () => { ctx.beginPath(); ctx.moveTo(x - lc, haut); ctx.lineTo(x - lc, yN); ctx.arc(x, y, r, -Math.PI / 2 - th, -Math.PI / 2 + th - TAU, true); ctx.lineTo(x + lc, haut); };
      const panse = () => { ctx.beginPath(); ctx.arc(x, y, r - 1.5, 0, TAU); };
      ctx.save();
      ctx.fillStyle = 'rgba(0,0,0,.25)'; ctx.beginPath(); ctx.ellipse(x + 3, y + r + 3, r * .55, 4, 0, 0, TAU); ctx.fill();
      forme(); ctx.fillStyle = 'rgba(190,220,240,.09)'; ctx.fill();
      let bas = y + r;
      (o.couches || []).forEach((cc, i) => {
        const ys = y + r - 2 * r * Math.min(1, cc.f);
        liquide(ctx, panse, x - r, x + r, ys, bas, cc.col, i === (o.couches.length - 1));
        bas = ys;
      });
      const niv = (o.couches || []).length ? y + r - 2 * r * Math.min(1, o.couches[o.couches.length - 1].f) : y + r;
      if (o.ponce) { const R = graine(9); for (let i = 0; i < 5; i++) L.ponce(ctx, x - r * .35 + i * r * .17, y + r - 7 - R() * 3, 4 + R() * 1.6); }
      if (o.bulles != null && o.couches && o.couches.length) {
        const n = Math.round(4 + 10 * (o.agite ?? .6));
        ctx.save(); panse(); ctx.clip();
        for (let i = 0; i < n; i++) {
          const f = ((o.bulles * (0.5 + (o.agite ?? .6)) * .9) + i * .137) % 1, br = 1.6 + (i % 3) * (o.agite ?? .6) * 1.3;
          const bx = x - r * .55 + r * 1.1 * ((i * 37 % 100) / 100) + Math.sin(f * 9 + i) * 2, by = y + r - 6 - f * (y + r - 6 - niv);
          ctx.globalAlpha = Math.min(1, (1 - f) * 3) * .85; ctx.strokeStyle = 'rgba(255,255,255,.85)'; ctx.lineWidth = 1;
          ctx.beginPath(); ctx.arc(bx, by, br, 0, TAU); ctx.stroke();
        }
        ctx.restore();
      }
      if (o.flocons) L.flocons(ctx, x - r * .6, niv - 4, r * 1.2, 12, 14, o.flocons);
      ctx.strokeStyle = 'rgba(225,240,252,.88)'; ctx.lineWidth = 2; ctx.lineJoin = 'round'; forme(); ctx.stroke();
      ctx.strokeStyle = 'rgba(255,255,255,.4)'; ctx.lineWidth = 3.5; ctx.lineCap = 'round'; ctx.beginPath(); ctx.arc(x, y, r * .76, Math.PI * 1.08, Math.PI * 1.4); ctx.stroke();
      ctx.lineWidth = 1.4; ctx.beginPath(); ctx.moveTo(x - lc + 2.5, haut + 4); ctx.lineTo(x - lc + 2.5, yN - 4); ctx.stroke();
      ctx.strokeStyle = 'rgba(240,248,255,.9)'; ctx.lineWidth = 2; ctx.beginPath(); ctx.ellipse(x, haut, lc + 2, 2.2, 0, 0, TAU); ctx.stroke();
      ctx.restore();
      return { haut, niveau: niv, lc };
    };
    /** Un grain de pierre ponce : petit caillou gris clair, poreux. */
    L.ponce = (ctx, x, y, r) => {
      ctx.save();
      const g = ctx.createRadialGradient(x - r * .3, y - r * .3, r * .1, x, y, r); g.addColorStop(0, '#f1f5f9'); g.addColorStop(.6, '#b6bcc4'); g.addColorStop(1, '#7c8591');
      ctx.fillStyle = g; ctx.beginPath(); ctx.ellipse(x, y, r, r * .75, .4, 0, TAU); ctx.fill();
      ctx.fillStyle = 'rgba(71,85,105,.6)'; for (let i = 0; i < 3; i++) { ctx.beginPath(); ctx.arc(x - r * .3 + i * r * .3, y + (i % 2 ? -1 : 1) * r * .2, r * .14, 0, TAU); ctx.fill(); }
      ctx.restore();
    };
    /**
     * Le réfrigérant à boules (vertical) : manchon de verre (eau froide bleue quand o.eau), tube intérieur à boules,
     * deux tubulures sur la droite : entrée de l'eau en BAS, sortie en HAUT. o.phase fait couler l'eau (flèches claires).
     * Renvoie { entree: [x, y], sortie: [x, y], bas, haut, w }.
     */
    L.refrigerant = (ctx, x, yHaut, yBas, o = {}) => {
      const w = o.w || 30, h = yBas - yHaut, nb = o.boules || 5, ye = yBas - 22, ysor = yHaut + 22;
      ctx.save();
      // tubulures
      const tub = (yy) => { ctx.fillStyle = 'rgba(190,220,240,.16)'; ctx.fillRect(x + w / 2 - 1, yy - 5, 18, 10); ctx.strokeStyle = 'rgba(225,240,252,.85)'; ctx.lineWidth = 1.5; ctx.strokeRect(x + w / 2 - 1, yy - 5, 18, 10); };
      tub(ye); tub(ysor);
      // manchon
      ctx.fillStyle = 'rgba(190,220,240,.10)'; ctx.beginPath(); ctx.roundRect(x - w / 2, yHaut + 8, w, h - 16, 8); ctx.fill();
      if (o.eau) {
        const ge = ctx.createLinearGradient(x - w / 2, 0, x + w / 2, 0); ge.addColorStop(0, 'rgba(37,99,235,.55)'); ge.addColorStop(.45, 'rgba(147,197,253,.42)'); ge.addColorStop(1, 'rgba(37,99,235,.55)');
        const hEau = (h - 20) * Math.min(1, o.eau);
        ctx.fillStyle = ge; ctx.beginPath(); ctx.roundRect(x - w / 2 + 2, yBas - 10 - hEau, w - 4, hEau, 6); ctx.fill();
        if (o.phase != null && o.eau >= 1) {
          ctx.strokeStyle = 'rgba(219,234,254,.55)'; ctx.lineWidth = 1.2;
          for (let i = 0; i < 6; i++) { const f = ((o.phase * .35) + i / 6) % 1, yy = yBas - 14 - f * (h - 30), xx = x + (i % 2 ? w * .3 : -w * .3); ctx.beginPath(); ctx.moveTo(xx - 3, yy + 4); ctx.lineTo(xx, yy); ctx.lineTo(xx + 3, yy + 4); ctx.stroke(); }
        }
      }
      // tube intérieur à boules
      const pas = (h - 40) / nb, rb = Math.min(w * .34, pas * .42);
      ctx.fillStyle = 'rgba(225,240,252,.18)'; ctx.strokeStyle = 'rgba(225,240,252,.85)'; ctx.lineWidth = 1.3;
      ctx.fillRect(x - 3, yHaut, 6, h + 14); ctx.strokeRect(x - 3, yHaut, 6, h + 14);
      for (let i = 0; i < nb; i++) { const yy = yHaut + 20 + pas * (i + .5); ctx.beginPath(); ctx.ellipse(x, yy, rb, rb * 1.05, 0, 0, TAU); ctx.fillStyle = 'rgba(225,240,252,.22)'; ctx.fill(); ctx.stroke(); }
      ctx.strokeStyle = 'rgba(225,240,252,.9)'; ctx.lineWidth = 1.9; ctx.beginPath(); ctx.roundRect(x - w / 2, yHaut + 8, w, h - 16, 8); ctx.stroke();
      ctx.strokeStyle = 'rgba(255,255,255,.35)'; ctx.lineWidth = 2.5; ctx.beginPath(); ctx.moveTo(x - w / 2 + 4, yHaut + 16); ctx.lineTo(x - w / 2 + 4, yBas - 16); ctx.stroke();
      ctx.restore();
      return { entree: [x + w / 2 + 17, ye], sortie: [x + w / 2 + 17, ysor], bas: yBas + 14, haut: yHaut, w, boules: Array.from({ length: nb }, (_, i) => yHaut + 20 + pas * (i + .5)), rb };
    };
    /** Un tuyau souple (caoutchouc) passant par pts ; o.eau : l'eau qui y coule (bleu). */
    L.tuyau = (ctx, pts, o = {}) => {
      ctx.save(); ctx.lineCap = 'round'; ctx.lineJoin = 'round';
      const trace = () => { ctx.beginPath(); pts.forEach(([px, py], i) => (i ? ctx.lineTo(px, py) : ctx.moveTo(px, py))); ctx.stroke(); };
      ctx.strokeStyle = '#7f1d1d'; ctx.lineWidth = 8; trace();
      ctx.strokeStyle = o.eau ? '#3b82f6' : '#b45309'; ctx.lineWidth = 5; trace();
      ctx.strokeStyle = 'rgba(255,255,255,.25)'; ctx.lineWidth = 1.4; trace();
      ctx.restore();
    };
    /** La potence : socle lourd, tige métallique ; o.pinces = [{ y, x2, ouverture }] noix + pince qui tient la verrerie en x2. */
    L.potence = (ctx, x, yBase, h, o = {}) => {
      ctx.save();
      L.ombre(ctx, () => { const g = ctx.createLinearGradient(0, yBase - 12, 0, yBase); g.addColorStop(0, '#64748b'); g.addColorStop(1, '#1e293b'); ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(x - 26, yBase - 12, o.socle || 120, 12, 3); ctx.fill(); }, 5);
      const gt = ctx.createLinearGradient(x - 4, 0, x + 4, 0); gt.addColorStop(0, '#94a3b8'); gt.addColorStop(.5, '#f1f5f9'); gt.addColorStop(1, '#64748b');
      ctx.fillStyle = gt; ctx.fillRect(x - 3.5, yBase - 12 - h, 7, h);
      for (const p of (o.pinces || [])) {
        const xa = Math.min(x, p.x2), xb = Math.max(x, p.x2);
        ctx.fillStyle = '#475569'; ctx.fillRect(x - 8, p.y - 7, 16, 14);           // noix
        const gb = ctx.createLinearGradient(0, p.y - 3, 0, p.y + 3); gb.addColorStop(0, '#cbd5e1'); gb.addColorStop(1, '#64748b');
        ctx.fillStyle = gb; ctx.fillRect(xa, p.y - 2.5, xb - xa - (p.ouverture || 12), 5);
        ctx.strokeStyle = '#334155'; ctx.lineWidth = 3; ctx.lineCap = 'round';
        const xp = p.x2, op = p.ouverture || 12; ctx.beginPath(); ctx.moveTo(xp - op - 2, p.y - 2); ctx.quadraticCurveTo(xp - op * .2, p.y - 12, xp + op, p.y - 7); ctx.moveTo(xp - op - 2, p.y + 2); ctx.quadraticCurveTo(xp - op * .2, p.y + 12, xp + op, p.y + 7); ctx.stroke();
      }
      ctx.restore();
    };
    /** Le chauffe-ballon : coque sombre, cuvette qui rougeoie quand il chauffe, bouton et voyant. */
    L.chauffeBallon = (ctx, x, y, w, h, chaud = 0) => {
      ctx.save();
      L.ombre(ctx, () => { const g = ctx.createLinearGradient(0, y, 0, y + h); g.addColorStop(0, '#4b5563'); g.addColorStop(1, '#111827'); ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(x - w / 2, y, w, h, 9); ctx.fill(); }, 8);
      const gl = ctx.createRadialGradient(x, y + 4, 4, x, y + 4, w * .5); gl.addColorStop(0, `rgba(251,146,60,${.25 + .6 * chaud})`); gl.addColorStop(1, 'rgba(251,146,60,0)');
      ctx.fillStyle = gl; ctx.beginPath(); ctx.ellipse(x, y + 6, w * .46, h * .32, 0, 0, TAU); ctx.fill();
      ctx.fillStyle = '#1f2937'; ctx.beginPath(); ctx.arc(x + w * .32, y + h * .62, 6, 0, TAU); ctx.fill(); ctx.strokeStyle = '#9ca3af'; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.moveTo(x + w * .32, y + h * .62); ctx.lineTo(x + w * .32 + 4, y + h * .62 - 4); ctx.stroke();
      ctx.fillStyle = chaud > .1 ? '#ef4444' : '#7f1d1d'; ctx.beginPath(); ctx.arc(x - w * .32, y + h * .62, 3.5, 0, TAU); ctx.fill();
      ctx.restore();
    };
    /** Le support élévateur (ciseaux) : plateau, croisillons, socle. */
    L.elevateur = (ctx, x, y, w, h) => {
      ctx.save();
      const met = (yy, hh) => { const g = ctx.createLinearGradient(0, yy, 0, yy + hh); g.addColorStop(0, '#e2e8f0'); g.addColorStop(1, '#64748b'); ctx.fillStyle = g; ctx.fillRect(x - w / 2, yy, w, hh); };
      met(y, 6); met(y + h - 6, 6);
      ctx.strokeStyle = '#94a3b8'; ctx.lineWidth = 3;
      ctx.beginPath(); ctx.moveTo(x - w * .4, y + 6); ctx.lineTo(x + w * .4, y + h - 6); ctx.moveTo(x + w * .4, y + 6); ctx.lineTo(x - w * .4, y + h - 6); ctx.stroke();
      ctx.fillStyle = '#475569'; ctx.beginPath(); ctx.arc(x, y + h / 2, 3.5, 0, TAU); ctx.fill();
      ctx.restore();
    };
    /** Une goutte (liquide condensé qui retombe). */
    L.gouttelette = (ctx, x, y, s, col = [147, 197, 253, .9]) => {
      ctx.save(); ctx.fillStyle = rgba(col); ctx.beginPath(); ctx.moveTo(x, y - s * 1.6); ctx.quadraticCurveTo(x + s, y - s * .2, x, y + s * .6); ctx.quadraticCurveTo(x - s, y - s * .2, x, y - s * 1.6); ctx.fill();
      ctx.fillStyle = 'rgba(255,255,255,.7)'; ctx.beginPath(); ctx.arc(x - s * .25, y - s * .2, s * .22, 0, TAU); ctx.fill(); ctx.restore();
    };
    /** Une volute de vapeur (blanche, légère). */
    L.vapeur = (ctx, x, y, s, a = .5) => {
      ctx.save(); const g = ctx.createRadialGradient(x, y, 1, x, y, s); g.addColorStop(0, `rgba(241,245,249,${a})`); g.addColorStop(1, 'rgba(241,245,249,0)');
      ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, s, 0, TAU); ctx.fill(); ctx.restore();
    };
    /** Un flacon de produit (verre, bouchon, étiquette avec son nom ; o.danger = 'corrosif' : pictogramme). */
    L.flacon = (ctx, x, y, w, h, o = {}) => {
      const col = o.col || L.LIQUIDES.ethanol, cou = w * .38, ye = y + h * .22;
      const forme = () => { ctx.beginPath(); ctx.moveTo(x - cou / 2, y); ctx.lineTo(x - cou / 2, ye); ctx.quadraticCurveTo(x - w / 2, ye + 4, x - w / 2, ye + 14); ctx.lineTo(x - w / 2, y + h - 6); ctx.quadraticCurveTo(x - w / 2, y + h, x - w / 2 + 6, y + h); ctx.lineTo(x + w / 2 - 6, y + h); ctx.quadraticCurveTo(x + w / 2, y + h, x + w / 2, y + h - 6); ctx.lineTo(x + w / 2, ye + 14); ctx.quadraticCurveTo(x + w / 2, ye + 4, x + cou / 2, ye); ctx.lineTo(x + cou / 2, y); };
      ctx.save();
      ctx.fillStyle = 'rgba(0,0,0,.25)'; ctx.beginPath(); ctx.ellipse(x + 3, y + h + 3, w * .5, 4, 0, 0, TAU); ctx.fill();
      forme(); ctx.fillStyle = 'rgba(190,220,240,.10)'; ctx.fill();
      liquide(ctx, () => { forme(); ctx.closePath(); }, x - w / 2, x + w / 2, y + h * (1 - (o.niveau ?? .7)), y + h, col);
      ctx.strokeStyle = 'rgba(225,240,252,.85)'; ctx.lineWidth = 1.8; forme(); ctx.stroke();
      ctx.fillStyle = o.bouchon || '#1e3a8a'; ctx.beginPath(); ctx.roundRect(x - cou / 2 - 2, y - 10, cou + 4, 12, 3); ctx.fill();
      // étiquette
      const ly = y + h * (o.danger ? .36 : .42), lh = h * (o.danger ? .26 : .34);
      ctx.fillStyle = '#fefce8'; ctx.beginPath(); ctx.roundRect(x - w / 2 + 4, ly, w - 8, lh, 3); ctx.fill();
      ctx.strokeStyle = 'rgba(0,0,0,.2)'; ctx.lineWidth = 1; ctx.stroke();
      if (o.nom) L.ecrit(ctx, o.nom, x, ly + lh / 2, Math.max(o.taille || 14, Math.min(lh * .62, (w - 10) / Math.max(1, o.nom.length) * 1.7)));
      if (o.danger === 'corrosif') L.picto(ctx, x, y + h * .8, Math.min(w * .2, h * .11));
      ctx.strokeStyle = 'rgba(255,255,255,.4)'; ctx.lineWidth = 3; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(x - w / 2 + 6, ye + 18); ctx.lineTo(x - w / 2 + 6, y + h - 10); ctx.stroke();
      ctx.restore();
    };
    /** Pictogramme de danger « corrosif » (losange rouge, fond blanc, gouttes qui rongent une main). */
    L.picto = (ctx, x, y, s) => {
      ctx.save(); ctx.translate(x, y); ctx.rotate(Math.PI / 4);
      ctx.fillStyle = '#fff'; ctx.fillRect(-s * .72, -s * .72, s * 1.44, s * 1.44); ctx.strokeStyle = '#dc2626'; ctx.lineWidth = s * .2; ctx.strokeRect(-s * .72, -s * .72, s * 1.44, s * 1.44);
      ctx.rotate(-Math.PI / 4); ctx.fillStyle = '#111'; ctx.fillRect(-s * .5, s * .15, s, s * .22); ctx.beginPath(); ctx.arc(-s * .2, -s * .25, s * .13, 0, TAU); ctx.arc(s * .2, -s * .15, s * .13, 0, TAU); ctx.fill();
      ctx.restore();
    };
    /** Une éprouvette graduée (niveau 0..1, couleur du liquide). */
    L.eprouvette = (ctx, x, y, w, h, niveau, col, o = {}) => {
      const forme = () => { ctx.beginPath(); ctx.moveTo(x - w / 2, y); ctx.lineTo(x - w / 2, y + h - 6); ctx.lineTo(x + w / 2, y + h - 6); ctx.lineTo(x + w / 2, y); };
      ctx.save();
      ctx.fillStyle = 'rgba(190,220,240,.10)'; forme(); ctx.fill();
      if (niveau > 0) liquide(ctx, () => { ctx.beginPath(); ctx.rect(x - w / 2 + 1.5, y, w - 3, h - 7.5); }, x - w / 2, x + w / 2, y + (h - 8) * (1 - niveau), y + h - 7, col);
      ctx.strokeStyle = 'rgba(225,240,252,.6)'; ctx.lineWidth = 1;
      for (let i = 1; i < 10; i++) { const yy = y + (h - 8) * i / 10; ctx.beginPath(); ctx.moveTo(x + w / 2 - (i % 5 ? 5 : 9), yy); ctx.lineTo(x + w / 2, yy); ctx.stroke(); }
      ctx.strokeStyle = 'rgba(225,240,252,.88)'; ctx.lineWidth = 1.8; forme(); ctx.stroke();
      ctx.fillStyle = 'rgba(190,220,240,.35)'; ctx.beginPath(); ctx.ellipse(x, y + h - 3, w * .9, 4, 0, 0, TAU); ctx.fill();
      ctx.strokeStyle = 'rgba(255,255,255,.4)'; ctx.lineWidth = 2.5; ctx.beginPath(); ctx.moveTo(x - w / 2 + 3, y + 6); ctx.lineTo(x - w / 2 + 3, y + h - 12); ctx.stroke();
      ctx.restore();
    };
    /** Des flocons de savon (solide blanc qui apparaît : le précipité). */
    L.flocons = (ctx, x, y, w, h, n, f = 1) => {
      const R = graine(31); ctx.save(); ctx.globalAlpha = Math.min(1, f);
      for (let i = 0; i < n; i++) { const px = x + R() * w, py = y + R() * h, s = 3 + R() * 4; const g = ctx.createRadialGradient(px - 1, py - 1, .5, px, py, s); g.addColorStop(0, '#ffffff'); g.addColorStop(1, '#e7e1c8'); ctx.fillStyle = g; ctx.beginPath(); ctx.ellipse(px, py, s, s * .7, R() * 3, 0, TAU); ctx.fill(); }
      ctx.restore();
    };
    /** Un entonnoir avec son papier filtre ; o.solide (0..1) : le savon retenu ; o.goutte (phase) : le filtrat qui coule. */
    L.entonnoir = (ctx, x, y, w, h, o = {}) => {
      ctx.save();
      const cone = () => { ctx.beginPath(); ctx.moveTo(x - w / 2, y); ctx.lineTo(x + w / 2, y); ctx.lineTo(x + 6, y + h * .62); ctx.lineTo(x + 6, y + h); ctx.lineTo(x - 6, y + h); ctx.lineTo(x - 6, y + h * .62); ctx.closePath(); };
      ctx.fillStyle = 'rgba(190,220,240,.12)'; cone(); ctx.fill();
      // papier filtre (blanc, plissé)
      ctx.fillStyle = '#f8fafc'; ctx.beginPath(); ctx.moveTo(x - w / 2 + 5, y + 3); ctx.lineTo(x + w / 2 - 5, y + 3); ctx.lineTo(x, y + h * .58); ctx.closePath(); ctx.fill();
      ctx.strokeStyle = 'rgba(148,163,184,.6)'; ctx.lineWidth = 1; for (let i = -2; i <= 2; i++) { ctx.beginPath(); ctx.moveTo(x + i * w * .09, y + 4); ctx.lineTo(x, y + h * .56); ctx.stroke(); }
      if (o.solide) L.flocons(ctx, x - w * .28, y + h * .12, w * .56, h * .22, Math.round(14 * o.solide), 1);
      ctx.strokeStyle = 'rgba(225,240,252,.88)'; ctx.lineWidth = 1.8; cone(); ctx.stroke();
      if (o.goutte != null) { const f = (o.goutte * .8) % 1; L.gouttelette(ctx, x, y + h + 6 + f * (o.chute || 40), 3.5, L.LIQUIDES.salee.slice(0, 3).concat([.9])); }
      ctx.restore();
    };
    /** Un thermomètre (frac 0..1 : hauteur de la colonne rouge). */
    L.thermometre = (ctx, x, y, h, frac) => {
      ctx.save();
      ctx.fillStyle = 'rgba(241,245,249,.25)'; ctx.beginPath(); ctx.roundRect(x - 6, y, 12, h, 6); ctx.fill();
      ctx.strokeStyle = 'rgba(241,245,249,.85)'; ctx.lineWidth = 1.5; ctx.stroke();
      boule(ctx, x, y + h + 4, 9, '#fecaca', '#ef4444', '#991b1b');
      ctx.fillStyle = '#ef4444'; const hh = (h - 10) * Math.max(0, Math.min(1, frac)); ctx.fillRect(x - 2.5, y + h - hh, 5, hh + 4);
      ctx.strokeStyle = 'rgba(241,245,249,.6)'; ctx.lineWidth = 1; for (let i = 1; i < 10; i++) { const yy = y + h - 4 - (h - 14) * i / 10; ctx.beginPath(); ctx.moveTo(x + 6, yy); ctx.lineTo(x + (i % 5 ? 10 : 14), yy); ctx.stroke(); }
      ctx.restore();
    };
    /** Une balance électronique ; l'afficheur montre `aff` (texte vert sur fond sombre). */
    L.balance = (ctx, x, y, w, h, aff = '0 g') => {
      ctx.save();
      L.ombre(ctx, () => { const g = ctx.createLinearGradient(0, y, 0, y + h); g.addColorStop(0, '#e5e7eb'); g.addColorStop(1, '#9ca3af'); ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(x - w / 2, y, w, h, 8); ctx.fill(); }, 6);
      const gp = ctx.createLinearGradient(0, y - 8, 0, y); gp.addColorStop(0, '#f8fafc'); gp.addColorStop(1, '#94a3b8'); ctx.fillStyle = gp; ctx.beginPath(); ctx.roundRect(x - w * .38, y - 8, w * .76, 8, 3); ctx.fill();
      ctx.fillStyle = '#0f172a'; ctx.beginPath(); ctx.roundRect(x - w * .3, y + h * .3, w * .6, h * .48, 4); ctx.fill();
      L.ecrit(ctx, aff, x, y + h * .54, Math.min(22, h * .36), '#4ade80');
      ctx.restore();
    };
    /** La plaque de CCM : couche blanche de gel de silice sur un support ; o.ligne / o.front : hauteurs (fraction depuis
     *  le bas) de la ligne de dépôt et du front ; o.mouille (0..1) : zone mouillée par l'éluant ; o.taches = [{ u, v, col,
     *  a, r, croix }] (u : position horizontale 0..1, v : hauteur 0..1 depuis le bas). */
    L.plaque = (ctx, x, y, w, h, o = {}) => {
      ctx.save();
      L.ombre(ctx, () => { ctx.fillStyle = '#f8fafc'; ctx.fillRect(x, y, w, h); }, 5);
      const R = graine(13); ctx.fillStyle = 'rgba(148,163,184,.12)'; for (let i = 0; i < w * h / 120; i++) ctx.fillRect(x + R() * w, y + R() * h, 1.2, 1.2);
      const Y = v => y + h - v * h;
      if (o.mouille) { const g = ctx.createLinearGradient(0, y + h, 0, Y(o.mouille)); g.addColorStop(0, 'rgba(148,163,184,.30)'); g.addColorStop(1, 'rgba(148,163,184,.16)'); ctx.fillStyle = g; ctx.fillRect(x, Y(o.mouille), w, h - (Y(o.mouille) - y)); }
      if (o.ligne != null) { ctx.strokeStyle = 'rgba(71,85,105,.85)'; ctx.lineWidth = 1.3; ctx.beginPath(); ctx.moveTo(x + 4, Y(o.ligne)); ctx.lineTo(x + w - 4, Y(o.ligne)); ctx.stroke(); }
      if (o.front != null) { ctx.strokeStyle = 'rgba(71,85,105,.85)'; ctx.lineWidth = 1.3; ctx.setLineDash([5, 3]); ctx.beginPath(); ctx.moveTo(x + 4, Y(o.front)); ctx.lineTo(x + w - 4, Y(o.front)); ctx.stroke(); ctx.setLineDash([]); }
      for (const t of (o.taches || [])) {
        const tx = x + t.u * w, ty = Y(t.v), r = t.r || 6, a = t.a ?? 1;
        if (a <= 0) continue;
        if (t.croix) { ctx.strokeStyle = `rgba(30,41,59,${.85 * a})`; ctx.lineWidth = 1.6; ctx.beginPath(); ctx.moveTo(tx - 4, ty - 4); ctx.lineTo(tx + 4, ty + 4); ctx.moveTo(tx + 4, ty - 4); ctx.lineTo(tx - 4, ty + 4); ctx.stroke(); continue; }
        const col = t.col || [71, 85, 105];
        const g = ctx.createRadialGradient(tx, ty, 1, tx, ty, r); g.addColorStop(0, rgba(col.concat([.95 * a]))); g.addColorStop(1, rgba(col.concat([.35 * a])));
        ctx.fillStyle = g; ctx.beginPath(); ctx.ellipse(tx, ty, r * 1.15, r * .85, 0, 0, TAU); ctx.fill();
        if (t.cerne) { ctx.strokeStyle = `rgba(71,85,105,${a})`; ctx.lineWidth = 1.3; ctx.beginPath(); ctx.ellipse(tx, ty, r * 1.6, r * 1.25, 0, 0, TAU); ctx.stroke(); }
      }
      ctx.strokeStyle = 'rgba(148,163,184,.9)'; ctx.lineWidth = 1; ctx.strokeRect(x, y, w, h);
      ctx.restore();
    };
    /** La cuve de chromatographie : bocal de verre, éluant au fond (hauteur he), couvercle (o.couvercle 0..1 : posé). */
    L.cuve = (ctx, x, y, w, h, he, o = {}) => {
      ctx.save();
      ctx.fillStyle = 'rgba(0,0,0,.25)'; ctx.beginPath(); ctx.ellipse(x + w / 2 + 3, y + h + 3, w * .5, 5, 0, 0, TAU); ctx.fill();
      ctx.fillStyle = 'rgba(190,220,240,.10)'; ctx.fillRect(x, y, w, h);
      if (he > 0) liquide(ctx, () => { ctx.beginPath(); ctx.rect(x + 2, y, w - 4, h - 2); }, x, x + w, y + h - he, y + h - 2, L.LIQUIDES.eluant);
      ctx.restore();
    };
    /** Le devant de la cuve (verre, reflets) et le couvercle : à peindre APRÈS la plaque, pour qu'elle soit dedans. */
    L.cuveDevant = (ctx, x, y, w, h, o = {}) => {
      ctx.save();
      ctx.strokeStyle = 'rgba(225,240,252,.88)'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x, y + h); ctx.lineTo(x + w, y + h); ctx.lineTo(x + w, y); ctx.stroke();
      ctx.strokeStyle = 'rgba(255,255,255,.3)'; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(x + 6, y + 10); ctx.lineTo(x + 6, y + h - 10); ctx.stroke();
      if (o.couvercle) {
        const k = Math.min(1, o.couvercle), yc = y - 6 - (1 - k) * 60, xc = x + (1 - k) * 30;
        ctx.globalAlpha = Math.min(1, k * 2);
        const g = ctx.createLinearGradient(0, yc, 0, yc + 10); g.addColorStop(0, 'rgba(226,232,240,.9)'); g.addColorStop(1, 'rgba(148,163,184,.7)');
        ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(xc - 6, yc, w + 12, 10, 4); ctx.fill();
        ctx.fillStyle = 'rgba(100,116,139,.9)'; ctx.beginPath(); ctx.roundRect(xc + w / 2 - 12, yc - 7, 24, 8, 3); ctx.fill();
      }
      ctx.restore();
    };
    /** La lampe UV (boîtier, tube violet qui brille quand allumée). */
    L.lampeUV = (ctx, x, y, w, allume = 0) => {
      ctx.save();
      L.ombre(ctx, () => { const g = ctx.createLinearGradient(0, y, 0, y + 26); g.addColorStop(0, '#475569'); g.addColorStop(1, '#0f172a'); ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(x - w / 2, y, w, 26, 6); ctx.fill(); }, 6);
      ctx.fillStyle = allume ? '#c4b5fd' : '#4c1d95'; ctx.fillRect(x - w / 2 + 8, y + 18, w - 16, 6);
      if (allume) { const g = ctx.createLinearGradient(0, y + 24, 0, y + 24 + 120); g.addColorStop(0, `rgba(167,139,250,${.45 * allume})`); g.addColorStop(1, 'rgba(167,139,250,0)'); ctx.fillStyle = g; ctx.beginPath(); ctx.moveTo(x - w / 2 + 8, y + 24); ctx.lineTo(x + w / 2 - 8, y + 24); ctx.lineTo(x + w / 2 + 20, y + 144); ctx.lineTo(x - w / 2 - 20, y + 144); ctx.closePath(); ctx.fill(); }
      ctx.restore();
    };
    /** Le capillaire (tube fin de verre) qui dépose une goutte. */
    L.capillaire = (ctx, x, y, l = 60, col = [100, 116, 139]) => {
      ctx.save(); ctx.strokeStyle = 'rgba(225,240,252,.9)'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + l * .35, y - l); ctx.stroke();
      ctx.strokeStyle = rgba(col.concat([.8])); ctx.lineWidth = 1.4; ctx.beginPath(); ctx.moveTo(x + 1, y - 2); ctx.lineTo(x + l * .12, y - l * .35); ctx.stroke(); ctx.restore();
    };
    /** Le flacon de diiode (cristaux violet-noir, vapeurs brunes) pour révéler les taches. */
    L.diiode = (ctx, x, y, w, h, k = 1) => {
      ctx.save();
      ctx.fillStyle = 'rgba(190,220,240,.10)'; ctx.fillRect(x, y, w, h);
      const g = ctx.createLinearGradient(0, y, 0, y + h); g.addColorStop(0, `rgba(146,64,14,${.10 * k})`); g.addColorStop(1, `rgba(146,64,14,${.38 * k})`); ctx.fillStyle = g; ctx.fillRect(x + 2, y + 6, w - 4, h - 8);
      const R = graine(5); for (let i = 0; i < 9; i++) { ctx.fillStyle = i % 2 ? '#1e1b4b' : '#3b0764'; const cx = x + 10 + R() * (w - 20), cy = y + h - 6 - R() * 6; ctx.beginPath(); ctx.moveTo(cx - 4, cy); ctx.lineTo(cx, cy - 4); ctx.lineTo(cx + 4, cy); ctx.lineTo(cx, cy + 3); ctx.closePath(); ctx.fill(); }
      ctx.restore();
    };
    /** Un tube à essais (o.niveau, o.col, o.couches). */
    L.tube = (ctx, x, y, w, h, o = {}) => {
      ctx.save();
      const forme = () => { ctx.beginPath(); ctx.moveTo(x - w / 2, y); ctx.lineTo(x - w / 2, y + h - w / 2); ctx.arc(x, y + h - w / 2, w / 2, Math.PI, 0, true); ctx.lineTo(x + w / 2, y); };
      ctx.fillStyle = 'rgba(190,220,240,.10)'; forme(); ctx.fill();
      let bas = y + h;
      (o.couches || []).forEach((cc, i) => { const ys = y + h - (h - 6) * cc.f; liquide(ctx, () => { forme(); ctx.closePath(); }, x - w / 2, x + w / 2, ys, bas, cc.col, i === o.couches.length - 1); bas = ys; });
      ctx.strokeStyle = 'rgba(225,240,252,.9)'; ctx.lineWidth = 1.8; forme(); ctx.stroke();
      ctx.strokeStyle = 'rgba(255,255,255,.4)'; ctx.lineWidth = 2.5; ctx.beginPath(); ctx.moveTo(x - w / 2 + 3, y + 6); ctx.lineTo(x - w / 2 + 3, y + h - w); ctx.stroke();
      ctx.restore();
    };

    /**
     * LE MONTAGE DU CHAUFFAGE À REFLUX, assemblé (même dessin dans toutes les diapos : montage, reflux, application).
     * (cx, yb) = milieu du ballon, niveau de la table ; s = échelle. o.k = { potence, elevateur, chauffe, ballon,
     * refrigerant, tuyaux, eau } (0..1 : apparition de chaque pièce ; absent = 1). o.couches / o.ponce / o.bulles /
     * o.agite : le contenu du ballon ; o.chaud (0..1) ; o.phase : l'eau qui coule ; o.ouvert : sans réfrigérant (le col
     * reste ouvert) ; o.vapeur = { t, k } : les vapeurs montent (k 0..1), se condensent sur les boules et retombent en
     * gouttes (o.vapeur.gouttes 0..1). Renvoie la géométrie : points d'attache des légendes et boîtes des repères.
     */
    L.montageReflux = (ctx, cx, yb, o = {}) => {
      const s = o.s || 1, k = Object.assign({ potence: 1, elevateur: 1, chauffe: 1, ballon: 1, refrigerant: 1, tuyaux: 1, eau: 1 }, o.k || {});
      const xp = cx - 92 * s, r = 44 * s, yE = yb - 50 * s, yC = yE - 46 * s, yBal = yC + 16 * s - r, haut = yBal - 1.75 * r;
      const yRb = haut - 4 * s, yRh = yRb - 172 * s, wR = 30 * s;
      const G = { s, xp, r, yBal, haut, yRb, yRh, cx, yb, wR };
      const fondu = (a, fn) => { if (a <= 0) return; ctx.save(); ctx.globalAlpha *= Math.min(1, a); fn(); ctx.restore(); };
      fondu(k.potence, () => L.potence(ctx, xp, yb, 352 * s, { socle: 130 * s, pinces: [
        ...(k.ballon >= 1 ? [{ y: haut + 14 * s, x2: cx, ouverture: 13 * s }] : []),
        ...(!o.ouvert && k.refrigerant >= 1 ? [{ y: yRh + 64 * s, x2: cx, ouverture: 17 * s }] : []) ] }));
      fondu(k.elevateur, () => L.elevateur(ctx, cx, yE, 116 * s, 50 * s));
      fondu(k.chauffe, () => L.chauffeBallon(ctx, cx, yC, 124 * s, 46 * s, o.chaud || 0));
      fondu(k.ballon, () => L.ballon(ctx, cx, yBal, r, { couches: o.couches, ponce: o.ponce, bulles: o.bulles, agite: o.agite, flocons: o.flocons }));
      let R = null;
      if (!o.ouvert) fondu(k.refrigerant, () => { R = L.refrigerant(ctx, cx, yRh, yRb, { w: wR, eau: k.eau * (o.eauNiveau ?? 1), phase: o.phase, boules: 5 }); });
      if (!R) R = { entree: [cx + wR / 2 + 17, yRb - 22 * s], sortie: [cx + wR / 2 + 17, yRh + 22 * s], boules: [], rb: 0 };
      G.R = R;
      if (!o.ouvert) fondu(k.tuyaux, () => {
        L.tuyau(ctx, [R.entree, [cx + 74 * s, R.entree[1]], [cx + 74 * s, yb - 6 * s]], { eau: k.eau > .5 });
        L.tuyau(ctx, [R.sortie, [cx + 96 * s, R.sortie[1]], [cx + 96 * s, yb - 6 * s]], { eau: k.eau > .5 });
      });
      // vapeurs, condensation, gouttes
      const v = o.vapeur;
      if (v && v.k > 0) {
        const t = v.t || 0, hautMax = o.ouvert ? haut - 120 * s : yRh + 60 * s;
        for (let i = 0; i < 10; i++) {
          const f = ((t * .45) + i / 10) % 1, yy = yBal - r * .2 - f * (yBal - r * .2 - hautMax), xx = cx + Math.sin(f * 7 + i) * 5 * s;
          if (o.ouvert || yy > yRh + 60 * s) L.vapeur(ctx, xx, yy, (10 + 8 * f) * s, .85 * v.k * (o.ouvert ? 1 : (1 - f * .5)));
        }
        if (!o.ouvert && (v.condense || 0) > 0) {
          ctx.save(); ctx.globalAlpha *= Math.min(1, v.condense);
          for (const yb2 of R.boules.slice(1)) { L.gouttelette(ctx, cx - R.rb * .55, yb2 + R.rb * .4, 2.8 * s); L.gouttelette(ctx, cx + R.rb * .5, yb2 + R.rb * .2, 2.4 * s); }
          ctx.restore();
        }
        if (!o.ouvert && (v.gouttes || 0) > 0) {
          for (let i = 0; i < 4; i++) { const f = ((t * .6) + i / 4) % 1, yy = yRh + 90 * s + f * (yBal - r * .3 - yRh - 90 * s); L.gouttelette(ctx, cx + 1, yy, 3.4 * s * Math.min(1, v.gouttes)); }
        }
      }
      G.boites = {
        potence: [xp - 26 * s, yb - 360 * s, 40 * s, 360 * s], elevateur: [cx - 60 * s, yE, 120 * s, 50 * s], chauffe: [cx - 64 * s, yC, 128 * s, 46 * s],
        ballon: [cx - r - 4 * s, haut, 2 * r + 8 * s, yBal + r - haut + 4 * s], refrigerant: [cx - wR / 2 - 4 * s, yRh, wR + 8 * s, yRb - yRh + 8 * s],
        entree: [R.entree[0] - 6 * s, R.entree[1] - 12 * s, 40 * s, 24 * s], sortie: [R.sortie[0] - 6 * s, R.sortie[1] - 12 * s, 40 * s, 24 * s],
      };
      G.ancres = {
        potence: [xp, yb - 330 * s], sortie: [R.sortie[0] + 10 * s, R.sortie[1]], refrigerant: [cx + wR / 2, (yRh + yRb) / 2 - 20 * s],
        entree: [R.entree[0] + 10 * s, R.entree[1]], ballon: [cx + r * .8, yBal - r * .3], chauffe: [cx + 62 * s, yC + 26 * s], elevateur: [cx + 58 * s, yE + 30 * s],
      };
      return G;
    };

    return L;
  })();

  /* Les ions d’une eau minérale (25 novembre 2026) : une couleur fixe par ion, la charge écrite dessus en sombre et gras.
   * Ca²⁺ garde la couleur du calcium du lexique commun (lexique.js, `C.calcium`) ; aucune ne reprend une couleur qui a déjà
   * un sens (jaune = carbone, rose = proton, bleu ciel = électron). */
  const IONS = { 'Ca²⁺': [207, 219, 232], 'Mg²⁺': [94, 234, 212], 'Na⁺': [192, 132, 252], 'Cl⁻': [134, 239, 172] };
  function ion(ctx, x, y, r, nom) {
    const col = (nom === 'Ca²⁺' && window.Lexique.C && window.Lexique.C.calcium) || IONS[nom] || [203, 213, 225];
    ctx.save();
    ctx.fillStyle = 'rgba(0,0,0,.22)'; ctx.beginPath(); ctx.arc(x + r * .2, y + r * .3, r, 0, Math.PI * 2); ctx.fill();
    const g = ctx.createRadialGradient(x - r * .38, y - r * .42, r * .08, x, y, r);
    g.addColorStop(0, rgba(eclair([...col, 1], .8))); g.addColorStop(.35, rgba(eclair([...col, 1], .2))); g.addColorStop(.75, rgba([...col, 1])); g.addColorStop(1, rgba(sombre([...col, 1], .42)));
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.fill();
    ctx.font = `700 ${Math.max(10, r * 1.1)}px ${(window.Tableau && window.Tableau.POLICE) || 'sans-serif'}`; ctx.fillStyle = '#0b1f2a'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillText(nom, x, y + 1); ctx.restore();
  }

  /* Les teintes des solutions (une seule valeur par sens) : incolore = eau claire un peu bleutée ; BBT ; ions colorés. */
  const SOLUTIONS = { incolore: [112, 194, 248, .36], cuivre: [58, 123, 213, .84], permanganate: [123, 42, 140, .9], diiode: [138, 75, 18, .9] };
  const BBT = { jaune: [246, 206, 42, .62], vert: [64, 168, 84, .6], bleu: [44, 96, 208, .64] };

  window.Lexique.chimie = Object.assign(Peint, Labo, { ion, IONS, phmetre, ecranPH, sonde, appareil, conductimetre: appareil, cellule, bulles, SOLUTIONS, BBT, rgba, eclair, sombre });
})();
