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
  /*
   * La caméra (18 novembre 2026, « la simulation d'abord, le texte compact » : sur un écran peu haut, le dessin restait
   * petit au milieu de son cadre et ses étiquettes tombaient à 8 px). Elle agit sous TOUTES les mises en page des pages
   * (cadre() de ce fichier, cadres propres des pages, colonne.js, zones.js…). Elle est demandée par la page :
   * Scene(canvas, dessiner, { camera: f => { mettre l'état final ; f() ; remettre } }) — sans état final connu, un dessin
   * écrit pas à pas serait d'abord agrandi sur ses premières lignes, puis rétréci à chaque ajout :
   *  - chaque image dessinée est relevée au niveau du contexte (traits, remplissages, textes, images : tout ce qui
   *    touche le canvas, dessins du lexique compris) ; la boîte de l'encre, en px du canvas sans caméra, ne fait que
   *    grandir (elle inclut donc l'état final dessiné par les calculs de départ des pages) ;
   *  - Craie.debut() pose ensuite un agrandissement Z (≤ ZOOM_CAMERA) qui fait remplir le cadre à cette boîte ;
   *  - le plancher du texte reste 15 px À L'ÉCRAN quelle que soit la taille du cadre (le kit le baissait jusqu'à 45 %
   *    sous 900 × 400 px) : tailleMin rend 15 / Z, puisque la caméra agrandit ensuite d'autant ;
   *  - les passes de mesure (tailleMin = 0) ne sont pas relevées ; un redimensionnement oublie la boîte ;
   *  - sur un cadre de téléphone (moins de 700 × 250 px), les phrases se taisent (compact) : la voix les dit.
   * scene.local() et les repères (getTransform) suivent la caméra.
   */
  const ZOOM_CAMERA = 2.4, MARGE_CAMERA = 8;
  /** Le plancher du texte : 15 px À L'ÉCRAN, quelle que soit la taille du cadre (divisé par l'agrandissement de la caméra). */
  function plancher(craie, cam) {
    Object.defineProperty(craie, 'tailleMin', {
      configurable: true,
      get() { return this._tmFixe ? this._tmFixe / cam.Z : 0; },
      // relire puis remettre la valeur rendue (« const t = c.tailleMin; … c.tailleMin = t ») ne la change pas
      set(v) { this._tmFixe = v > 0 ? (this._tmLu && Math.abs(v - this._tmLu) < 1e-9 ? this._tmFixe : v) : 0; this._tmLu = this._tmFixe ? this._tmFixe / cam.Z : 0; },
    });
  }
  function Camera(craie, scene, actif) {
    const ctx = craie.ctx, proto = CanvasRenderingContext2D.prototype;
    const cam = { Z: 1, tx: 0, ty: 0, boite: null, image: null, chemin: [], apres() {}, oublier() {}, versPage: (x, y) => [x, y] };
    const vide = () => ({ x0: Infinity, y0: Infinity, x1: -Infinity, y1: -Infinity });
    // point du dessin → px CSS du canvas SANS la caméra
    function noter(b, x, y, m = 0) {
      if (!b || !Number.isFinite(x) || !Number.isFinite(y)) return;
      const t = ctx.getTransform(), d = window.devicePixelRatio || 1;
      const X = ((t.a * x + t.c * y + t.e) / d - cam.tx) / cam.Z, Y = ((t.b * x + t.d * y + t.f) / d - cam.ty) / cam.Z;
      const k = m * Math.hypot(t.a, t.b) / d / cam.Z;
      b.x0 = Math.min(b.x0, X - k); b.y0 = Math.min(b.y0, Y - k); b.x1 = Math.max(b.x1, X + k); b.y1 = Math.max(b.y1, Y + k);
      if (window.__traceCamera && (X + k > b.x1 - 1 || X - k < b.x0 + 1)) window.__traceCamera.push([Math.round(X), Math.round(Y), Math.round(k), new Error().stack.split('\n').slice(2, 5).join(' | ')]);
    }
    const releve = () => cam.image && craie._tmFixe > 0;
    // les chemins : leurs points comptent quand ils sont tracés ou remplis (pas pour un clip)
    const surChemin = (nom, pts) => {
      const o = proto[nom];
      ctx[nom] = function (...a) { if (releve()) for (const [i, j, r] of pts(a)) cam.chemin.push([i, j, r]); return o.apply(this, a); };
    };
    surChemin('moveTo', a => [[a[0], a[1], 0]]);
    surChemin('lineTo', a => [[a[0], a[1], 0]]);
    surChemin('arc', a => [[a[0], a[1], a[2]]]);
    surChemin('ellipse', a => [[a[0], a[1], Math.max(a[2], a[3])]]);
    surChemin('rect', a => [[a[0], a[1], 0], [a[0] + a[2], a[1] + a[3], 0]]);
    surChemin('roundRect', a => [[a[0], a[1], 0], [a[0] + a[2], a[1] + a[3], 0]]);
    surChemin('quadraticCurveTo', a => [[a[0], a[1], 0], [a[2], a[3], 0]]);
    surChemin('bezierCurveTo', a => [[a[0], a[1], 0], [a[2], a[3], 0], [a[4], a[5], 0]]);
    surChemin('arcTo', a => [[a[0], a[1], 0], [a[2], a[3], 0]]);
    const beginPath = proto.beginPath;
    ctx.beginPath = function () { cam.chemin = []; return beginPath.call(this); };
    for (const nom of ['stroke', 'fill']) {
      const o = proto[nom];
      ctx[nom] = function (...a) {
        if (releve() && !(a[0] instanceof Path2D)) { const m = nom === 'stroke' ? this.lineWidth / 2 : 0; for (const [x, y, r] of cam.chemin) noter(cam.image, x, y, r + m); }
        return o.apply(this, a);
      };
    }
    for (const nom of ['fillRect', 'strokeRect']) {
      const o = proto[nom];
      ctx[nom] = function (x, y, w, h) { if (releve()) { noter(cam.image, x, y); noter(cam.image, x + w, y + h); } return o.call(this, x, y, w, h); };
    }
    for (const nom of ['fillText', 'strokeText']) {
      const o = proto[nom];
      ctx[nom] = function (s, x, y, max) {
        if (releve() && String(s).trim()) {
          const m = /([\d.]+)px/.exec(this.font), t = m ? +m[1] : 16;
          let w = this.measureText(String(s)).width; if (max !== undefined && w > max) w = max;
          const al = this.textAlign, x0 = al === 'center' ? x - w / 2 : al === 'right' || al === 'end' ? x - w : x;
          const bl = this.textBaseline, y0 = bl === 'top' || bl === 'hanging' ? y : bl === 'middle' ? y - t * .6 : bl === 'bottom' ? y - t * 1.2 : y - t;
          noter(cam.image, x0, y0); noter(cam.image, x0 + w, y0 + t * 1.25);
        }
        return max === undefined ? o.call(this, s, x, y) : o.call(this, s, x, y, max);
      };
    }
    const drawImage = proto.drawImage;
    ctx.drawImage = function (img, ...a) {
      if (releve()) {
        const [x, y, w, h] = a.length >= 8 ? a.slice(4) : a.length >= 4 ? a : [a[0], a[1], img.width, img.height];
        noter(cam.image, x, y); noter(cam.image, x + w, y + h);
      }
      return drawImage.call(this, img, ...a);
    };
    plancher(craie, cam);
    if (!actif) return cam;
    // le plancher du texte : 15 px à l'écran, quelle que soit la taille du cadre (la caméra agrandit ensuite de Z)
    // chaque image : effacée par debut(), puis la caméra est posée sous la mise en page de la page
    const debut = craie.debut;
    craie.debut = function (...a) {
      const r = debut.apply(this, a);
      cam.image = vide(); cam.chemin = [];
      ctx.translate(cam.tx, cam.ty); ctx.scale(cam.Z, cam.Z);
      return r;
    };
    // une image finie : sa boîte rejoint celle de la scène ; si l'agrandissement change, on redessine
    cam.apres = function () {
      const b = cam.image; cam.image = null;
      if (!b || !(b.x1 > b.x0 && b.y1 > b.y0)) return;
      const W = craie.W, H = craie.H;
      const n = { x0: Math.max(0, b.x0), y0: Math.max(0, b.y0), x1: Math.min(W, b.x1), y1: Math.min(H, b.y1) };
      if (!(n.x1 > n.x0 && n.y1 > n.y0)) return;
      const a = cam.boite;
      const u = a ? { x0: Math.min(a.x0, n.x0), y0: Math.min(a.y0, n.y0), x1: Math.max(a.x1, n.x1), y1: Math.max(a.y1, n.y1) } : n;
      if (a && u.x0 >= a.x0 - .5 && u.y0 >= a.y0 - .5 && u.x1 <= a.x1 + .5 && u.y1 <= a.y1 + .5) return;
      cam.boite = u;
      const bw = u.x1 - u.x0, bh = u.y1 - u.y0;
      const Z = Math.max(1, Math.min((W - 2 * MARGE_CAMERA) / bw, (H - 2 * MARGE_CAMERA) / bh, ZOOM_CAMERA));
      const tx = (W - bw * Z) / 2 - u.x0 * Z, ty = (H - bh * Z) / 2 - u.y0 * Z;
      if (Math.abs(Z - cam.Z) > .01 || Math.abs(tx - cam.tx) > 1 || Math.abs(ty - cam.ty) > 1) {
        cam.Z = Z; cam.tx = tx; cam.ty = ty; scene.sale = true;
        if (craie._tmFixe) craie._tmLu = craie._tmFixe / Z;
      }
    };
    cam.oublier = function () { cam.boite = null; cam.Z = 1; cam.tx = 0; cam.ty = 0; scene.sale = true; };
    /** px CSS du canvas → px CSS sans la caméra (ce que la mise en page de la page connaît). */
    cam.versPage = (x, y) => [(x - cam.tx) / cam.Z, (y - cam.ty) / cam.Z];
    return cam;
  }
  /*
   * Un texte trop long pour sa largeur `max` (18 novembre 2026) : le kit le rétrécissait, jusqu'à 10 unités du dessin
   * (8 px à l'écran sur un téléphone). Il passe plutôt sur DEUX lignes, coupé à un « ; », un « : », une virgule ou un
   * espace près du milieu, centrées sur la ligne d'origine ; un texte à peine trop long (≤ 15 %, ≤ 30 % pour une ligne à
   * fraction, qui ne se coupe jamais) dépasse un peu sa largeur ; sans coupure possible, il garde le plancher.
   */
  /** Un cadre de téléphone en paysage (≈ 560 × 210 px) : à 15 px, il n'y a pas la place d'écrire des phrases. */
  const compact = c => c.tailleMin > 0 && (c.W < 700 || c.H < 250);
  /** Une phrase, pas une formule : au moins cinq mots de deux lettres ou plus (« le courant change de sens »). */
  const prose = s => (String(s).replace(/⟦[^⟧]*⟧|[_^]\{[^}]*\}|[_^]\S/g, ' ').match(/[A-Za-zÀ-ÿœ’']{2,}/g) || []).length >= 5;
  function deuxLignes(craie) {
    const texte = craie.texte;
    const largeur = (c, s, t) => {
      if (String(s).includes('⟦')) return c.largeurTexte(s, t);
      return window.Tableau.Craie.segments(String(s)).reduce((w, g) => w + (c._largeur ? c._largeur(g.t, g.sub || g.sup ? t * .62 : t) : c.largeurTexte(g.t, t)), 0);
    };
    craie.texte = function (s, x, y, o = {}) {
      s = String(s);
      // cadre de téléphone : les phrases (5 mots ou plus) se taisent, la voix les dit ; formules, valeurs, noms restent
      if (!o.__ligne && !o.encadre && !o.garder && compact(this) && prose(s)) return this;
      if (!o.max || o.plancher === false || o.__ligne || !this.echelle || !this.tailleMin) return texte.call(this, s, x, y, o);
      const t = Math.max(o.taille ?? 18, this.tailleMin / this.echelle), w = largeur(this, s, t);
      if (w <= o.max * 1.04) return texte.call(this, s, x, y, o);
      // un peu trop long : il dépasse légèrement sa largeur plutôt que de rétrécir ; une ligne à fraction ne se coupe pas
      if (w <= o.max * 1.15 || (s.includes('⟦') && w <= o.max * 1.3)) return texte.call(this, s, x, y, { ...o, max: w + 1 });
      if (s.includes('⟦')) return texte.call(this, s, x, y, o);
      // les coupures possibles : hors d'une fraction ⟦…⟧ et d'un exposant ^(…) / indice _{…}
      let prof = 0, best = null;
      for (let i = 1; i < s.length - 1; i++) {
        const ch = s[i];
        if (ch === '⟦' || ch === '(' || ch === '{') prof++;
        else if (ch === '⟧' || ch === ')' || ch === '}') prof = Math.max(0, prof - 1);
        if (prof || ch !== ' ') continue;
        const avant = s[i - 1], poids = avant === ';' ? 0 : avant === ':' ? .02 : avant === ',' ? .04 : .08;
        const a = s.slice(0, i).trimEnd(), b = s.slice(i + 1).trimStart(), m = Math.max(largeur(this, a, t), largeur(this, b, t));
        const score = m * (1 + poids);
        if (!best || score < best.score) best = { a, b, m, score };
      }
      if (!best) return texte.call(this, s, x, y, { ...o, max: Math.max(o.max, w) });
      const lh = t * (s.includes('⟦') ? 1.7 : 1.12), max = Math.max(o.max, best.m);
      texte.call(this, best.a, x, y - lh / 2, { ...o, max, __ligne: true });
      return texte.call(this, best.b, x, y + lh / 2, { ...o, max, __ligne: true });
    };
  }
  function Scene(canvas, dessiner, options = {}) {
    // `scene` existe avant la craie : le premier redimensionnement la marque déjà « à redessiner ».
    const scene = { sale: true, boite: null, mesurant: false, L: VW };
    const craie = new window.Tableau.Craie(canvas, { onresize: () => { scene.sale = true; if (scene.camera) scene.camera.oublier(); } });
    const camera = Camera(craie, scene, typeof options.camera === 'function');
    scene.camera = camera;
    deuxLignes(craie);
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
        // une fraction « ⟦num|dén⟧ » : largeur du kit, et ses deux étages montent et descendent plus loin
        const fr = String(s).includes('⟦');
        let l = fr ? this.largeurTexte(s, t) : this.ctx.measureText(String(s).replace(/_/g, '')).width; if (o.max && l > o.max) l = o.max;
        const x0 = o.align === 'center' ? x - l / 2 : o.align === 'right' ? x - l : x;
        pt(x0, y - t * (fr ? 1.25 : 0.95)); pt(x0 + l, y + t * (fr ? 0.65 : 0.35));
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
      local(x, y) { [x, y] = camera.versPage(x, y); return [(x - scene.ox) / scene.s, (y - scene.oy) / scene.s]; },
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
      if ((scene.sale || anime) && craie.W > 1) {
        // la caméra relève d'abord l'image FINALE de la page (options.camera met la page à son état final le temps de fn)
        if (options.camera && !camera.boite) {
          const t = scene.ouvert; scene.ouvert = -1e9;
          try { options.camera(() => dessiner(craie, scene)); camera.apres(); } catch (e) { console.warn('[tableau] caméra', e); } finally { scene.ouvert = t; }
        }
        scene.sale = !dessiner(craie, scene); camera.apres();
      }
      requestAnimationFrame(image);
    });
    return scene;
  }
  window.OndesTableau = { Scene, VW, VH };
})();
