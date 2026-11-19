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
    /* Plancher VRAI de 15 px à l'écran (18 novembre 2026, « le texte est plus grand que la simulation », écran de bureau
     * peu haut ~1360 × 560) : le kit baisse son plancher jusqu'à 45 % quand le canvas fait moins de 900 × 400 px
     * (getter `tailleMin` de tableau.js) ; dans le lecteur, le cadre ne fait que 280 à 350 px de haut, et les étiquettes
     * tombaient à 9-11 px. Sur la craie de ce dossier (rien de partagé n'est changé), la valeur posée est la valeur
     * rendue dès que le canvas fait au moins 640 × 260 px (le cadre du lecteur sur un écran de bureau, même bas) ; en
     * dessous (téléphone en paysage, canvas ~530 × 195), le plancher baisse avec le cadre, jamais sous 75 % (11 px) :
     * le dessin de 760 × 420 n'y a pas la place d'écrire tout à 15 px sans chevauchement (le kit descendait à 45 %). */
    Object.defineProperty(craie, 'tailleMin', {
      get() { const v = this._plancher15 || 0; return v && v * Math.min(1, Math.max(.75, Math.min((this.W || 640) / 640, (this.H || 260) / 260))); },
      set(v) { this._plancher15 = v; }, configurable: true });
    /* Indices et exposants (62 % de la ligne) : jamais sous le plancher non plus (N₀, 10²⁰, e^(−λt) restaient à 9 px).
     * Même écriture que le kit et exposants.js, sur cette craie seulement ; une page peut encore remplacer ces fonctions
     * (national.html, bilan.html le font avec le même calcul). */
    const CHIFFRES = { '⁻': '−', '⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4', '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9' };
    const EXPO = t => String(t).replace(/[⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+/g, g => '^{' + [...g].map(ch => CHIFFRES[ch]).join('') + '}');
    const petitDe = (k, t) => Math.max(t * .62, k.echelle && k.tailleMin ? k.tailleMin / k.echelle : 0);
    craie._largeur = function (s, taille, gras) {
      const c = this.ctx, T = window.Tableau;
      return T.Craie.segments(EXPO(s)).reduce((w, seg) => { c.font = `${gras ? '700 ' : ''}${seg.sub || seg.sup ? petitDe(this, taille) : taille}px ${T.POLICE}`; return w + c.measureText(seg.t).width; }, 0);
    };
    /* ᴬ_Z X (noyaux.js) : A et Z, tenus au plancher, s'écartent d'autant (sinon, agrandis, ils se chevauchent :
     * « ²⁰⁸₈₂Pb » écrit « 208 » sur « 82 ») ; même calcul que national.html. */
    const azT = (k, t) => Math.max(t * .6, k.echelle && k.tailleMin ? k.tailleMin / k.echelle : 0);
    const lg = (k, s, t) => { k.ctx.font = `${t}px ${window.Tableau.POLICE}`; return k.ctx.measureText(String(s).replace('-', '−')).width; };
    craie.largeurNucleide = function (X, A, Z, taille = 18) { const p = azT(this, taille); return Math.max(lg(this, A, p), lg(this, Z, p)) + 1.5 + lg(this, X, Math.max(taille, azT(this, 0))); };
    craie.nucleide = function (X, A, Z, x, y, o = {}) {
      const taille = o.taille ?? 18, p = azT(this, taille), plus = p - taille * .6;
      const wAZ = Math.max(lg(this, A, p), lg(this, Z, p)), xs = x + wAZ + 1.5, cAZ = o.couleurAZ || o.couleur, d = o.duree != null ? o.duree / 3 : undefined;
      this.texte(String(A).replace('-', '−'), xs - 1, y - taille * .42 - plus * .9, { taille: p, couleur: cAZ, align: 'right', duree: d, gras: o.gras });
      this.texte(String(Z).replace('-', '−'), xs - 1, y + taille * .22 + plus * .5, { taille: p, couleur: cAZ, align: 'right', duree: d, gras: o.gras });
      this.texte(X, xs, y, { taille, couleur: o.couleur, duree: d, gras: o.gras });
      return xs + lg(this, X, Math.max(taille, azT(this, 0)));
    };
    craie._texteIndices = function (s, x, y, o, taille) {
      const c = this.ctx, T = window.Tableau, segs = T.Craie.segments(s), police = t => `${o.gras ? '700 ' : ''}${t}px ${T.POLICE}`;
      const petit = petitDe(this, taille), tailleDe = seg => (seg.sub || seg.sup ? petit : taille);
      const total = segs.reduce((w, seg) => { c.font = police(tailleDe(seg)); return w + c.measureText(seg.t).width; }, 0);
      if (o.max && total > o.max) return this._texteIndices(s, x, y, { ...o, max: 0 }, Math.max(10, taille * o.max / total));
      const plain = segs.map(seg => seg.t).join('');
      const part = this._part(o.duree ?? Math.max(.1, plain.length / 16));
      if (part <= 0) return this;
      let reste = part < 1 ? Math.max(1, Math.ceil(part * plain.length)) : plain.length;
      c.fillStyle = this.couleur(o.couleur); c.globalAlpha = o.alpha ?? .96; c.textBaseline = o.base || 'alphabetic';
      c.shadowColor = 'rgba(255,255,255,.25)'; c.shadowBlur = 1; c.textAlign = 'left';
      let px = o.align === 'center' ? x - total / 2 : o.align === 'right' ? x - total : x;
      for (const seg of segs) {
        if (reste <= 0) break;
        const t = seg.t.slice(0, reste); reste -= seg.t.length;
        c.font = police(tailleDe(seg));
        c.fillText(t, px, y + (seg.sub ? taille * .28 : seg.sup ? -taille * .42 : 0));
        px += c.measureText(t).width;
        if (t.length < seg.t.length) break;
      }
      if (part < 1) this.tip = [px, y - taille * .3];
      c.shadowBlur = 0; c.globalAlpha = 1;
      return this;
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

  /* ── Courbes nettes et lumineuses (16 novembre 2026, « plus agréable, couleurs vives ») ───────────────────
   * Net.courbe(c, fn, n, o, aire) trace la MÊME courbe de craie que c.courbe (même durée d'écriture : les instants
   * ne bougent pas), entourée d'un halo de sa couleur ; `aire` = { base: y, rgb: 'r,g,b', alpha } pose en plus un
   * dégradé doux sous la courbe, qui avance avec le tracé. Net.halo(c, couleur, fn) : halo autour de ce que fn dessine. */
  const Net = {
    halo(c, couleur, fn, flou = 10) {
      const ctx = c.ctx; ctx.save(); ctx.shadowColor = c.couleur(couleur); ctx.shadowBlur = flou * (devicePixelRatio || 1) * (c.echelle || 1);
      try { fn(); } finally { ctx.restore(); }
    },
    courbe(c, fn, n, o = {}, aire) {
      const cur0 = c.cur;
      Net.halo(c, o.couleur, () => c.courbe(fn, n, o), o.flou ?? 9);
      if (!aire) return c;
      const part = !Number.isFinite(c.t) ? 1 : Math.max(0, Math.min(1, (c.t - cur0) / Math.max(1e-6, c.cur - cur0)));
      if (part <= 0) return c;
      const pts = []; for (let i = 0; i <= n; i++) { const p = fn(i / n); if (p) pts.push(p); }
      const m = Math.max(2, Math.round(pts.length * part)), vus = pts.slice(0, m);
      if (vus.length < 2) return c;
      const ctx = c.ctx, haut = Math.min(...pts.map(p => p[1])), bas = aire.base, a = aire.alpha ?? .3;
      ctx.save(); ctx.globalCompositeOperation = 'destination-over';   // sous la craie déjà écrite (axes, graduations, courbe)
      const g = ctx.createLinearGradient(0, Math.min(haut, bas), 0, Math.max(haut, bas));
      const [g0, g1] = haut <= bas ? [a, 0] : [0, a];
      g.addColorStop(0, `rgba(${aire.rgb},${g0})`); g.addColorStop(1, `rgba(${aire.rgb},${g1})`);
      ctx.fillStyle = g; ctx.beginPath(); ctx.moveTo(vus[0][0], bas); vus.forEach(p => ctx.lineTo(p[0], p[1])); ctx.lineTo(vus[vus.length - 1][0], bas); ctx.closePath(); ctx.fill();
      ctx.restore(); return c;
    },
    /** Perle ombrée (point remarquable) : rgb clair, moyen, sombre. */
    perle(ctx, x, y, r, t = ['#fff7c2', '#facc15', '#854d0e']) {
      ctx.save();
      ctx.fillStyle = 'rgba(0,0,0,.3)'; ctx.beginPath(); ctx.ellipse(x + 1.5, y + 3.5, r, r * .7, 0, 0, Math.PI * 2); ctx.fill();
      const g = ctx.createRadialGradient(x - r * .35, y - r * .4, r * .1, x, y, r); g.addColorStop(0, t[0]); g.addColorStop(.45, t[1]); g.addColorStop(1, t[2]);
      ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = 'rgba(255,255,255,.7)'; ctx.beginPath(); ctx.ellipse(x - r * .38, y - r * .42, r * .22, r * .14, -.6, 0, Math.PI * 2); ctx.fill();
      ctx.restore();
    },
  };
  window.OndesTableau = { Scene, VW, VH, Net };
})();
