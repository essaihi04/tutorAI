/*
 * Commun aux simulations du cours « Notion de l'information génétique » (copie du kit des ondes) : cadre virtuel 760 × 420 mis à l'échelle sans
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
  /* « La simulation d'abord » (18 novembre 2026 : « le texte est plus grand que la simulation ; donner davantage de taille
   *  aux simulations ») :
   *  - le plancher du texte est 15 px à l'écran, toujours : le kit le baissait sous 400 px de haut (13 px sur un écran de
   *    bureau peu haut, 9,5 px sous une question) ; la place se gagne en agrandissant le dessin, pas en rétrécissant le texte ;
   *  - `ajuster` peut être une fonction (L) → vrai/faux : le moteur des étapes zoome sur l'encre les vues dessinées d'un
   *    seul tenant et laisse les vues découpées en blocs remplir le cadre elles-mêmes ;
   *  - la boîte de l'encre est mesurée AU PIXEL (image complète peinte sur un canevas à part) : la peinture du vivant
   *    (cellules, chromosomes, bactéries) compte comme la craie, rien de peint n'est coupé au bord. */
  function Scene(canvas, dessiner, options = {}) {
    // `scene` existe avant la craie : le premier redimensionnement la marque déjà « à redessiner ».
    const scene = { sale: true, boite: null, mesurant: false, L: VW };
    const craie = new window.Tableau.Craie(canvas, { onresize: () => { scene.sale = true; } });
    Object.defineProperty(craie, 'tailleMin', { configurable: true, get() { return this._plancher || 0; }, set(v) { this._plancher = v; } });
    const ajuste = () => (typeof options.ajuster === 'function' ? !!options.ajuster(scene.L) : !!options.ajuster);
    const PX = 420, PY = 220;   // marge du canevas de mesure autour du cadre
    /* La boîte de l'encre (coordonnées du cadre) : l'image complète peinte une fois (ou à plusieurs instants, `complet`)
     * sur un canevas à part, sans effacer entre deux instants ; les pixels non transparents donnent la boîte. */
    function mesurer(sEst) {
      scene.sMesure = sEst || 1;
      const off = document.createElement('canvas');
      off.width = Math.round(scene.L + 2 * PX); off.height = VH + 2 * PY;
      const g = off.getContext('2d'); g.clearRect = function () { return this; }; g.__echelle = scene.sMesure;   // les lettres peintes du lexique suivent l'échelle réelle
      // un point de rayon nul (`encre` d'une vue, boîte d'un bloc) ne peint rien : il est relevé à part
      const pts = [], point = craie.point;
      craie.point = function (x, y, r = 4, c) { if (!r) { const m = this.ctx.getTransform(); pts.push([m.a * x + m.c * y + m.e, m.b * x + m.d * y + m.f]); } return point.call(this, x, y, r, c); };
      const sv = { ctx: craie.ctx, W: craie.W, H: craie.H, repere: Object.prototype.hasOwnProperty.call(craie, 'repere') ? craie.repere : null, ouvert: scene.ouvert };
      craie.ctx = g; craie.W = off.width; craie.H = off.height; craie.repere = function () { return this; };
      scene.mesurant = true; scene.ouvert = -1e9;
      try { (options.complet || (f => f()))(() => dessiner(craie, scene)); } catch (e) { console.warn('[tableau] mesure de la boîte', e); }
      finally { delete craie.point; Object.assign(craie, { ctx: sv.ctx, W: sv.W, H: sv.H }); if (sv.repere) craie.repere = sv.repere; else delete craie.repere; scene.mesurant = false; scene.ouvert = sv.ouvert; }
      let im; try { im = g.getImageData(0, 0, off.width, off.height).data; } catch (_) { return null; }
      const b = { x0: Infinity, y0: Infinity, x1: -Infinity, y1: -Infinity };
      for (let y = 0; y < off.height; y += 2) for (let x = 0; x < off.width; x += 2) {
        if (im[(y * off.width + x) * 4 + 3] > 24) { if (x < b.x0) b.x0 = x; if (x > b.x1) b.x1 = x; if (y < b.y0) b.y0 = y; if (y > b.y1) b.y1 = y; }
      }
      for (const [x, y] of pts) { b.x0 = Math.min(b.x0, x); b.x1 = Math.max(b.x1, x); b.y0 = Math.min(b.y0, y); b.y1 = Math.max(b.y1, y); }
      if (!(b.x1 > b.x0 && b.y1 > b.y0)) return null;
      const n = { x0: b.x0 - PX - MARGE, y0: b.y0 - PY - MARGE, x1: b.x1 - PX + MARGE, y1: b.y1 - PY + MARGE };
      const a = scene.boite;
      return a ? { x0: Math.min(a.x0, n.x0), y0: Math.min(a.y0, n.y0), x1: Math.max(a.x1, n.x1), y1: Math.max(a.y1, n.y1) } : n;
    }
    Object.assign(scene, {
      craie, sale: true, ouvert: performance.now(), s: 1, ox: 0, oy: 0, VH,
      /** Prépare l'image : écriture en direct depuis l'ouverture, puis cadre mis à l'échelle. */
      cadre(graine = 7) {
        const W = craie.W, H = craie.H;
        // pendant la mesure, le canevas à part n'a pas la forme du tableau : le cadre garde sa largeur
        const L = scene.mesurant ? scene.L : options.large ? Math.round(Math.min(VW * L_MAX, Math.max(VW, VH * W / Math.max(1, H)))) : VW;
        if (L !== scene.L) { scene.L = L; scene.boite = null; }
        const aj = !scene.mesurant && ajuste();
        if (aj && !scene.boite && W > 1) {
          // le texte garde 15 px à l'écran : mesuré à l'échelle du cadre, puis remesuré si le zoom final est plus petit
          const s0 = Math.min(W / L, H / VH), echelleDe = b => Math.min(W / (b.x1 - b.x0), H / (b.y1 - b.y0), s0 * ZOOM_MAX);
          let b = mesurer(s0);
          if (b && echelleDe(b) < s0 * .97) { const s1 = echelleDe(b); scene.boite = null; b = mesurer(s1) || b; }
          scene.boite = b;
        }
        scene.zoom = aj && !!scene.boite;
        craie.debut(graine, (performance.now() - scene.ouvert) / 1000);
        if (scene.mesurant) { craie.ctx.setTransform(1, 0, 0, 1, PX, PY); scene.s = scene.sMesure; scene.ox = 0; scene.oy = 0; craie.echelle = scene.sMesure; craie.tailleMin = TAILLE_MIN; craie.cadre = null; return craie; }
        const k = scene.zoom ? scene.boite : { x0: 0, y0: 0, x1: L, y1: VH };
        const sCadre = Math.min(W / L, H / VH), bw = k.x1 - k.x0, bh = k.y1 - k.y0;
        const s = Math.min(W / bw, H / bh, sCadre * ZOOM_MAX);
        scene.s = s; scene.ox = (W - bw * s) / 2 - k.x0 * s; scene.oy = (H - bh * s) / 2 - k.y0 * s;
        craie.ctx.translate(scene.ox, scene.oy); craie.ctx.scale(s, s);
        craie.echelle = s; craie.tailleMin = TAILLE_MIN;
        craie.cadre = scene.zoom ? null : { w: L, h: VH, haut: 0 };    // tout texte reste dans le cadre du dessin (rien de coupé au bord)
        return craie;
      },
      /** La construction a changé de forme (réglage, vue) : la boîte sera remesurée (elle ne fait que grandir). */
      remesurer() { if (ajuste()) { const n = mesurer(scene.s); if (n) scene.boite = n; scene.sale = true; } },
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
  window.GenetiqueTableau = { Scene, VW, VH };
})();
