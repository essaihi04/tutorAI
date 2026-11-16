/*
 * Commun aux simulations de la radioactivité (copie de ondes-lumineuses-tableau/commun.js) : cadre virtuel 760 × 420 mis à l'échelle sans
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
    /* Courbes nettes et lumineuses (16 novembre 2026, « plus agréable, couleurs vives ») : toute courbe tracée par
     * craie.courbe (≥ 40 points) garde son écriture progressive et sa durée, mais sans tremblé, avec un halo doux de sa
     * couleur. Option `aire: yBase` : une aire en dégradé, de la courbe jusqu'à la ligne yBase, se remplit au rythme du tracé. */
    const courbeCraie = craie.courbe;
    craie.courbe = function (fn, n, o = {}) {
      if (o.net === false || (n < 40 && o.net !== true)) return courbeCraie.call(this, fn, n, o);
      const ctx = this.ctx, teinte = this.couleur(o.couleur);
      if (o.aire !== undefined && !scene.mesurant) {
        const pts = []; for (let i = 0; i <= n; i++) { const p = fn(i / n); if (p) pts.push(p); }
        let L = 0; const cum = [0]; for (let i = 1; i < pts.length; i++) { L += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); cum.push(L); }
        const duree = Math.max(.02, o.duree ?? Math.max(.08, L / 650));
        const part = !Number.isFinite(this.t) || this.t >= this.cur + duree ? 1 : this.t <= this.cur ? 0 : (this.t - this.cur) / duree;
        const vus = pts.filter((_, i) => cum[i] <= L * part + 1e-9);
        if (vus.length > 1) {
          let haut = Infinity, bas = -Infinity; for (const p of vus) { haut = Math.min(haut, p[1]); bas = Math.max(bas, p[1]); }
          const y0 = Math.min(haut, o.aire), y1 = Math.max(bas, o.aire, y0 + 1);
          const rgb = /^#[0-9a-f]{6}$/i.test(teinte) ? [1, 3, 5].map(k => parseInt(teinte.slice(k, k + 2), 16)).join(',') : '226,232,240';
          const g = ctx.createLinearGradient(0, y0, 0, y1), dessus = o.aire >= (haut + bas) / 2;   // courbe au-dessus de la base (cas courant)
          g.addColorStop(dessus ? 0 : 1, `rgba(${rgb},${o.aireAlpha ?? .3})`); g.addColorStop(dessus ? 1 : 0, `rgba(${rgb},.03)`);
          ctx.save(); ctx.fillStyle = g; ctx.beginPath(); ctx.moveTo(vus[0][0], o.aire);
          for (const p of vus) ctx.lineTo(p[0], p[1]);
          ctx.lineTo(vus[vus.length - 1][0], o.aire); ctx.closePath(); ctx.fill(); ctx.restore();
        }
      }
      ctx.save(); ctx.shadowColor = teinte; ctx.shadowBlur = o.pointille ? 5 : 10;
      try { return courbeCraie.call(this, fn, n, { tremble: 0, ...o }); } finally { ctx.restore(); }
    };
    /* La boîte de l'encre (coordonnées du cadre) : l'image complète dessinée une fois, traits et textes relevés. */
    function mesurer() {
      const b = { x0: Infinity, y0: Infinity, x1: -Infinity, y1: -Infinity };
      const pt = (x, y, m = 0) => { if (!Number.isFinite(x) || !Number.isFinite(y)) return; b.x0 = Math.min(b.x0, x - m); b.y0 = Math.min(b.y0, y - m); b.x1 = Math.max(b.x1, x + m); b.y1 = Math.max(b.y1, y + m); };
      const { trait, texte, point } = craie;
      craie.trait = function (pts, o = {}) { const m = (o.largeur ?? 2.4) / 2 + 1; for (const p of pts || []) pt(p[0], p[1], m); return trait.call(this, pts, o); };
      craie.point = function (x, y, r = 4, c) { pt(x, y, r); return point.call(this, x, y, r, c); };
      craie.texte = function (s, x, y, o = {}) {
        const t = o.taille ?? 18; this.ctx.font = `${o.gras ? '700 ' : ''}${t}px ${window.Tableau.POLICE}`;
        let l = this.ctx.measureText(String(s).replace(/_/g, '')).width; if (o.max && l > o.max) l = o.max;
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
  window.OndesTableau = { Scene, VW, VH };
})();
