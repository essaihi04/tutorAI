/*
 * Commun aux manips des ondes : cadre virtuel 760 × 420 mis à l'échelle sans
 * rien couper, texte jamais plus petit que 15 px à l'écran, boucle d'image qui
 * ne redessine que lorsqu'il le faut.
 */
(function () {
  'use strict';
  const VW = 760, VH = 420;
  /* Agrandissement du 15 novembre 2026 (« la simulation n'occupe qu'une bande étroite, les textes sont minuscules ») :
   *  - texte jamais plus petit que TAILLE_MIN px à l'écran (15 ; c'était 11) ;
   *  - Scene(canvas, dessiner, { large: true }) : le cadre prend le format du tableau, scene.L va de 760 à 760 × L_MAX
   *    (hauteur toujours 420) ; la page place ses blocs avec scene.L (figure à gauche, légende et calculs à droite)
   *    au lieu de les empiler. Sans `large`, un dessin prévu pour 760 × 420 est centré comme avant ;
   *  - { ajuster: true } : la boîte de l'encre de l'image complète (dessinée une fois, `complet(fn)` met la page à
   *    son état final le temps de fn) remplit le tableau, l'agrandissement est borné à ZOOM_MAX × le cadre entier ;
   *    scene.remesurer() après un changement de vue (la boîte ne fait que grandir). */
  const TAILLE_MIN = 15, L_MAX = 2.1, MARGE = 14, ZOOM_MAX = 2;
  function Scene(canvas, dessiner, options = {}) {
    // `scene` existe avant la craie : le premier redimensionnement la marque déjà « à redessiner ».
    const scene = { sale: true, boite: null, mesurant: false, L: VW };
    const craie = new window.Tableau.Craie(canvas, { onresize: () => { scene.sale = true; } });
    /* La boîte de l'encre (coordonnées du cadre) : l'image complète dessinée une fois, traits et textes relevés. */
    function mesurer() {
      const b = { x0: Infinity, y0: Infinity, x1: -Infinity, y1: -Infinity };
      const pt = (x, y, m = 0) => { if (!Number.isFinite(x) || !Number.isFinite(y)) return; b.x0 = Math.min(b.x0, x - m); b.y0 = Math.min(b.y0, y - m); b.x1 = Math.max(b.x1, x + m); b.y1 = Math.max(b.y1, y + m); };
      const { trait, texte, point } = craie;
      craie.trait = function (pts, o = {}) { const m = (o.largeur ?? 2.4) / 2 + 1; for (const p of pts || []) pt(p[0], p[1], m); return trait.call(this, pts, o); };
      craie.point = function (x, y, r = 4, c) { pt(x, y, r); return point.call(this, x, y, r, c); };
      craie.texte = function (s, x, y, o = {}) {
        const t = o.taille ?? 18; this.ctx.font = `${o.gras ? '700 ' : ''}${t}px ${window.Tableau.POLICE}`;
        let l = String(s).includes('⟦') ? this.largeurTexte(String(s).replace(/_/g, ''), t) : this.ctx.measureText(String(s).replace(/_/g, '')).width; if (o.max && l > o.max) l = o.max;   // « ⟦num|dén⟧ » : fraction sur deux étages
        const x0 = o.align === 'center' ? x - l / 2 : o.align === 'right' ? x - l : x;
        pt(x0, y - t * 0.95); pt(x0 + l, y + t * 0.35);
        return texte.call(this, s, x, y, o);
      };
      const t = scene.ouvert;
      scene.mesurant = true; scene.ouvert = -1e9;
      try { (options.complet || (f => f()))(() => dessiner(craie, scene)); } catch (e) { console.warn('[tableau] mesure de la boîte', e); }
      finally { craie.trait = trait; craie.texte = texte; craie.point = point; scene.mesurant = false; scene.ouvert = t; }
      if (!(b.x1 > b.x0 && b.y1 > b.y0)) return null;
      const n = { x0: Math.max(0, b.x0 - MARGE), y0: Math.max(0, b.y0 - MARGE), x1: Math.min(scene.L, b.x1 + MARGE), y1: Math.min(VH, b.y1 + MARGE) };
      const a = scene.boite;
      return a ? { x0: Math.min(a.x0, n.x0), y0: Math.min(a.y0, n.y0), x1: Math.max(a.x1, n.x1), y1: Math.max(a.y1, n.y1) } : n;
    }
    Object.assign(scene, {
      craie, sale: true, ouvert: performance.now(), s: 1, ox: 0, oy: 0, VH,
      /** Prépare l'image : écriture en direct depuis l'ouverture, puis cadre mis à l'échelle. */
      cadre(graine = 7) {
        const W = craie.W, H = craie.H;
        const L = options.large ? Math.round(Math.min(VW * L_MAX, Math.max(VW, VH * W / Math.max(1, H)))) : VW;
        if (L !== scene.L) { scene.L = L; scene.boite = null; }
        if (options.ajuster && !scene.mesurant && !scene.boite && W > 1) scene.boite = mesurer();
        craie.debut(graine, (performance.now() - scene.ouvert) / 1000);
        if (scene.mesurant) { scene.s = 1; scene.ox = 0; scene.oy = 0; craie.echelle = 1; craie.tailleMin = 0; craie.cadre = null; return craie; }
        const k = scene.boite || { x0: 0, y0: 0, x1: L, y1: VH };
        const sCadre = Math.min(W / L, H / VH), bw = k.x1 - k.x0, bh = k.y1 - k.y0;
        const s = Math.min(W / bw, H / bh, sCadre * ZOOM_MAX);
        scene.s = s; scene.ox = (W - bw * s) / 2 - k.x0 * s; scene.oy = (H - bh * s) / 2 - k.y0 * s;
        craie.ctx.translate(scene.ox, scene.oy); craie.ctx.scale(s, s);
        craie.echelle = s; craie.tailleMin = TAILLE_MIN;
        craie.cadre = { w: L, h: VH, haut: 0 };    // tout texte reste dans le cadre du dessin (rien de coupé au bord)
        return craie;
      },
      /** La construction a changé de forme (réglage, vue) : la boîte sera remesurée (elle ne fait que grandir). */
      remesurer() { if (options.ajuster) { const n = mesurer(); if (n) scene.boite = n; scene.sale = true; } },
      /** Coordonnées CSS du canvas → coordonnées du dessin. */
      local(x, y) { return [(x - scene.ox) / scene.s, (y - scene.oy) / scene.s]; },
      reecrire() { scene.ouvert = performance.now(); scene.sale = true; },
      /** L'image complète de la scène (tout écrit, d'un coup), en PNG : pour imprimer ou télécharger. */
      image() {
        const t = scene.ouvert; scene.ouvert = -1e9;
        try { dessiner(craie, scene); return canvas.toDataURL('image/png'); } finally { scene.ouvert = t; scene.sale = true; }
      },
    });
    let avant = performance.now();
    // Première image au prochain rafraîchissement : la page a fini de déclarer sa scène.
    requestAnimationFrame(function image(maintenant) {
      const dt = Math.min(0.1, Math.max(0, (maintenant - avant) / 1000)); avant = maintenant;
      const anime = scene.avancer ? scene.avancer(dt) : false;
      if ((scene.sale || anime) && craie.W > 1) scene.sale = !dessiner(craie, scene);
      requestAnimationFrame(image);
    });
    return scene;
  }

  /* ── Peinture des objets réels (16 novembre 2026, « plus réaliste, plus attractif ») ────────────────────────
   * Canvas brut, appelé dans craie.direct(() => …) AVANT la craie : la craie (légendes, flèches, axes) passe
   * par-dessus. Mêmes teintes que les ondes périodiques (corde de chanvre, perles ombrées, écran vert). */
  const P = {
    lin(ctx, x0, y0, x1, y1, arrets) { const g = ctx.createLinearGradient(x0, y0, x1, y1); arrets.forEach(([o, c]) => g.addColorStop(o, c)); return g; },
    rr(ctx, x, y, w, h, r) { ctx.beginPath(); if (ctx.roundRect) ctx.roundRect(x, y, w, h, r); else ctx.rect(x, y, w, h); },
    /** Corde de chanvre éclairée par le haut, passant par `pts` ([[x,y],…]), avec son ombre portée. */
    corde(ctx, pts, w = 5.5, alpha = 1) {
      const chemin = (dx, dy) => { ctx.beginPath(); pts.forEach(([px, py], i) => (i ? ctx.lineTo(px + dx, py + dy) : ctx.moveTo(px + dx, py + dy))); };
      ctx.save(); ctx.globalAlpha = alpha; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
      chemin(2, 6); ctx.strokeStyle = 'rgba(0,0,0,.28)'; ctx.lineWidth = w + 2; ctx.stroke();
      chemin(0, 1); ctx.strokeStyle = '#6b4521'; ctx.lineWidth = w; ctx.stroke();
      chemin(0, -.4); ctx.strokeStyle = '#c99a5b'; ctx.lineWidth = w - 1.8; ctx.stroke();
      chemin(0, 0); ctx.setLineDash([2, 4]); ctx.strokeStyle = 'rgba(92,58,26,.55)'; ctx.lineWidth = w - 2.4; ctx.stroke(); ctx.setLineDash([]);
      chemin(0, -w * .3); ctx.strokeStyle = 'rgba(255,238,205,.78)'; ctx.lineWidth = 1.1; ctx.stroke();
      ctx.restore();
    },
    /** Perle (sphère ombrée) : orange, jaune, rouge, violet, cyan. */
    perle(ctx, x, y, r, teinte = 'orange') {
      const T = { orange: ['#ffe2c2', '#f97316', '#7c2d12'], jaune: ['#fff7c2', '#facc15', '#854d0e'], rouge: ['#ffd5cc', '#ef4444', '#7f1d1d'],
        violet: ['#ede9fe', '#8b5cf6', '#3b1d7a'], cyan: ['#e0fbff', '#22d3ee', '#155e75'], gris: ['#f1f5f9', '#94a3b8', '#334155'] }[teinte] || ['#ffe2c2', '#f97316', '#7c2d12'];
      ctx.save();
      ctx.fillStyle = 'rgba(0,0,0,.3)'; ctx.beginPath(); ctx.ellipse(x + 2, y + 5, r, r * .7, 0, 0, Math.PI * 2); ctx.fill();
      const g = ctx.createRadialGradient(x - r * .35, y - r * .4, r * .1, x, y, r);
      g.addColorStop(0, T[0]); g.addColorStop(.45, T[1]); g.addColorStop(1, T[2]);
      ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = 'rgba(255,255,255,.7)'; ctx.beginPath(); ctx.ellipse(x - r * .38, y - r * .42, r * .22, r * .14, -.6, 0, Math.PI * 2); ctx.fill();
      ctx.restore();
    },
    /** Poignée en bois tenue en S : elle monte et descend avec le bout de la corde (y). */
    poignee(ctx, x, y) {
      const w = 13, h = 46;
      ctx.save();
      ctx.fillStyle = 'rgba(0,0,0,.3)'; P.rr(ctx, x - w / 2 + 3, y - h / 2 + 5, w, h, 6); ctx.fill();
      ctx.fillStyle = P.lin(ctx, x - w / 2, 0, x + w / 2, 0, [[0, '#5a3216'], [.35, '#c8894a'], [.6, '#b0733b'], [1, '#4a2810']]);
      P.rr(ctx, x - w / 2, y - h / 2, w, h, 6); ctx.fill();
      ctx.strokeStyle = 'rgba(70,35,10,.4)'; ctx.lineWidth = .7;
      for (const d of [-2.5, 1, 3.5]) { ctx.beginPath(); ctx.moveTo(x + d, y - h / 2 + 5); ctx.quadraticCurveTo(x + d + 1, y, x + d - .5, y + h / 2 - 5); ctx.stroke(); }
      ctx.fillStyle = P.lin(ctx, x - w / 2, 0, x + w / 2, 0, [[0, '#4b5563'], [.5, '#e5e7eb'], [1, '#4b5563']]);   // bague de serrage de la corde
      ctx.fillRect(x - w / 2 - 1, y - 3.5, w + 2, 7);
      ctx.restore();
    },
    /** Micro sur pied : grille noire, bague métallique, pied ; `teinte` = couleur de la bague (repère de voie). */
    micro(ctx, x0, y0, teinte = '#22d3ee', k = 1.25) {
      const x = 0, y = 0;
      ctx.save(); ctx.translate(x0, y0); ctx.scale(k, k);
      ctx.fillStyle = 'rgba(0,0,0,.3)'; ctx.beginPath(); ctx.ellipse(x + 2, y + 38, 15, 4, 0, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = P.lin(ctx, x - 2, 0, x + 2, 0, [[0, '#4b5563'], [.5, '#e5e7eb'], [1, '#4b5563']]); ctx.fillRect(x - 2, y + 10, 4, 26);
      ctx.fillStyle = P.lin(ctx, 0, y + 33, 0, y + 38, [[0, '#9ca3af'], [1, '#1f2937']]); P.rr(ctx, x - 13, y + 33, 26, 5, 2.5); ctx.fill();
      ctx.fillStyle = P.lin(ctx, x - 6, 0, x + 6, 0, [[0, '#1f2937'], [.5, '#6b7280'], [1, '#111827']]); P.rr(ctx, x - 5.5, y + 4, 11, 10, 2); ctx.fill();
      ctx.fillStyle = teinte; ctx.fillRect(x - 5.5, y + 7, 11, 2.5);
      const g = ctx.createRadialGradient(x - 3.5, y - 4, 1, x, y, 11);
      g.addColorStop(0, '#6b7280'); g.addColorStop(.6, '#1f2937'); g.addColorStop(1, '#0b0f14');
      ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y - 1, 10, 0, Math.PI * 2); ctx.fill();
      ctx.save(); ctx.beginPath(); ctx.arc(x, y - 1, 10, 0, Math.PI * 2); ctx.clip(); ctx.strokeStyle = 'rgba(160,170,180,.35)'; ctx.lineWidth = .6;
      for (let k = -10; k <= 10; k += 3) { ctx.beginPath(); ctx.moveTo(x + k, y - 11); ctx.lineTo(x + k, y + 9); ctx.stroke(); ctx.beginPath(); ctx.moveTo(x - 10, y - 1 + k); ctx.lineTo(x + 10, y - 1 + k); ctx.stroke(); }
      ctx.restore();
      ctx.fillStyle = 'rgba(255,255,255,.35)'; ctx.beginPath(); ctx.ellipse(x - 4, y - 5, 3, 2, -.6, 0, Math.PI * 2); ctx.fill();
      ctx.restore();
    },
    /** Oscilloscope : boîtier gris, écran vert sombre et sa grille fine (nx × ny divisions) dans (x, y, w, h). */
    oscillo(ctx, x, y, w, h, nx = 10, ny = 6) {
      const m = 9;
      ctx.save();
      ctx.fillStyle = 'rgba(0,0,0,.35)'; P.rr(ctx, x - m + 5, y - m + 7, w + 2 * m, h + 2 * m, 10); ctx.fill();
      ctx.fillStyle = P.lin(ctx, 0, y - m, 0, y + h + m, [[0, '#6b7480'], [.5, '#3b434c'], [1, '#22282e']]);
      P.rr(ctx, x - m, y - m, w + 2 * m, h + 2 * m, 10); ctx.fill();
      ctx.strokeStyle = 'rgba(255,255,255,.18)'; ctx.lineWidth = 1; ctx.stroke();
      const g = ctx.createRadialGradient(x + w / 2, y + h / 2, 10, x + w / 2, y + h / 2, Math.max(w, h) * .7);
      g.addColorStop(0, '#12382a'); g.addColorStop(1, '#06180f');
      ctx.fillStyle = g; P.rr(ctx, x, y, w, h, 5); ctx.fill();
      ctx.strokeStyle = 'rgba(134,239,172,.16)'; ctx.lineWidth = 1;
      for (let i = 1; i < nx; i++) { ctx.beginPath(); ctx.moveTo(x + i * w / nx, y); ctx.lineTo(x + i * w / nx, y + h); ctx.stroke(); }
      for (let j = 1; j < ny; j++) { ctx.beginPath(); ctx.moveTo(x, y + j * h / ny); ctx.lineTo(x + w, y + j * h / ny); ctx.stroke(); }
      ctx.fillStyle = 'rgba(255,255,255,.04)'; ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + w * .55, y); ctx.lineTo(x + w * .3, y + h); ctx.lineTo(x, y + h); ctx.fill();   // reflet de la vitre
      ctx.restore();
    },
    /** Trace lumineuse nette (sur l'écran vert ou un graphe) : un cœur clair et un halo de la couleur. */
    trace(ctx, pts, couleur, w = 2.2) {
      if (pts.length < 2) return;
      ctx.save(); ctx.lineCap = 'round'; ctx.lineJoin = 'round';
      const chemin = () => { ctx.beginPath(); pts.forEach(([px, py], i) => (i ? ctx.lineTo(px, py) : ctx.moveTo(px, py))); };
      ctx.shadowColor = couleur; ctx.shadowBlur = 8; chemin(); ctx.strokeStyle = couleur; ctx.lineWidth = w; ctx.stroke();
      ctx.shadowBlur = 0; chemin(); ctx.strokeStyle = 'rgba(255,255,255,.55)'; ctx.lineWidth = w * .35; ctx.stroke();
      ctx.restore();
    },
    /** Arc de son (ou d'ultrasons) : un front lumineux doux, centré en (x, y), de rayon r, entre les angles a0 et a1. */
    front(ctx, x, y, r, a0, a1, couleur = '250,204,21', alpha = 1) {
      if (r <= 2) return;
      ctx.save(); ctx.lineCap = 'round';
      for (const [w, a] of [[9, .12], [4.5, .3], [1.8, .9]]) { ctx.strokeStyle = `rgba(${couleur},${a * alpha})`; ctx.lineWidth = w; ctx.beginPath(); ctx.arc(x, y, r, a0, a1); ctx.stroke(); }
      ctx.restore();
    },
  };
  /** Adoucit un mouvement (départ et arrivée en douceur). */
  P.doux = u => (u <= 0 ? 0 : u >= 1 ? 1 : u * u * (3 - 2 * u));
  /* Fraction « ⟦num|dén⟧ » écrite à la taille t : ce qu'elle dépasse au-dessus (haut) et au-dessous (bas) d'une ligne
   * ordinaire, en px du cadre, d'après la taille réellement écrite par la craie (étages jamais sous la taille minimale
   * à l'écran : en téléphone, ils sont presque aussi grands que la ligne). Sert à écarter les lignes voisines.
   * `s` (facultatif) : la formule ; un numérateur à indice (« ⟦d_2 − d_1|n⟧ ») est écrit un peu plus haut par la craie. */
  function etages(c, t, s = '') {
    const T = c.echelle && c.tailleMin ? Math.max(t, c.tailleMin / c.echelle) : t, tf = c._tailleEtage ? c._tailleEtage(T) : T * .78;
    const indice = /⟦[^|⟧]*_/.test(s) ? tf * .35 : 0;
    return { T, haut: Math.max(0, .32 * T + 1.05 * tf - .75 * T) + indice, bas: Math.max(0, 1.15 * tf - .52 * T) };
  }
  window.OndesTableau = { Scene, VW, VH, P, etages };
})();
