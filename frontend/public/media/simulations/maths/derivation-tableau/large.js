/*
 * Tableau large pour les constructions du cours « Dérivation et étude des fonctions » (15 novembre 2026).
 *
 * Problème (écran 1366 × 613) : le tableau est environ 3,2 fois plus large que haut (jusqu'à 4 avec la bande de
 * formules) ; une construction dessinée dans le cadre 760 × 420 (repère à gauche, phrases empilées à droite) est bornée
 * par la HAUTEUR : grands vides à gauche et à droite, textes petits. Le kit (maths-tableau.js, option `ajuster`) agrandit
 * la boîte de l'encre jusqu'aux bords.
 *
 * Ici, quand le tableau est large (largeur/hauteur ≥ 2,3), la construction est redisposée SANS changer son code :
 *   - zone gauche (le repère et ce qui l'entoure) : sur toute la hauteur, un peu élargie ;
 *   - zone droite (les phrases, à droite du repère) : coupée en colonnes là où il y a un blanc entre deux lignes, posées
 *     côte à côte, avec une échelle commune k (textes plus grands à l'écran qu'avant) ; le titre au-dessus d'elles.
 * Le plan est AUTOMATIQUE : à la mesure de la boîte (kit, construction complète), la vue est dessinée une fois « à blanc »
 * par un enregistreur qui relève la boîte de chaque trait et de chaque texte ; on en tire la limite du repère, les blancs
 * de la colonne des phrases et le meilleur découpage (0, 1 ou 2 coupes). Pas de gain (k < 0,6) : rien ne change.
 * Le dessin passe ensuite par un intermédiaire (Proxy de la craie) qui transforme les coordonnées selon la zone du point
 * d'ancrage ; les aides K (axes, courbe, proj, rond, lignes, titre) sont refaites par-dessus cet intermédiaire.
 * Les repères (c.repere) suivent la transformation (mêmes ids) ; les poignées aussi (aller et retour).
 * Grand écran (1920 × 1080, tableau ~2 : 1) : rien ne change.
 *
 * Usage :  <script src="…/large.js"> après maths-tableau.js, puis, avant MathsTableau.page :
 *   Large.config({ vue1: true, vue2: { col: 430 } })   // true = plan automatique ; options pour forcer :
 *   col (abscisse où commencent les phrases), coupes ([y…]), kmin (gain minimal, défaut .6),
 *   iso (repère non étiré : même échelle en x et en y, pour le miroir y = x) ;
 *   zones (plan écrit à la main, voir manuel()) pour une construction sans repère.
 */
(function () {
  'use strict';
  const VW = 760, TOP = 34, ECART = 16;
  const fr = (v, d = 2) => window.MathsTableau.fr(v, d);
  let ETAT = null;   // le plan de la dernière image (pour les poignées)
  const DRAP = { gauche: false };   // vrai pendant que K.axes trace le repère : tout va dans la zone gauche

  function actif(c) { return c.W > 1 && c.H > 1 && c.W / c.H >= 2.3; }

  /* ── l'enregistreur : relève les boîtes (coordonnées d'origine) et leur point d'ancrage ── */
  function enregistreur(c0, items) {
    const box = (ax, ay, x0, y0, x1, y1) => items.push({ g: DRAP.gauche, ax, ay, x0: Math.min(x0, x1), y0: Math.min(y0, y1), x1: Math.max(x0, x1), y1: Math.max(y0, y1) });
    const nuage = (pts) => { if (!pts || !pts.length) return; let a = 1e9, b = 1e9, c = -1e9, d = -1e9; for (const [x, y] of pts) { a = Math.min(a, x); b = Math.min(b, y); c = Math.max(c, x); d = Math.max(d, y); } box(pts[0][0], pts[0][1], a, b, c, d); };
    let px;
    const over = {
      texte(s, x, y, o = {}) {
        const t = o.taille ?? 18; let l = c0.largeurTexte(String(s).replace(/[_^{}]/g, ''), t); if (o.max && l > o.max) l = o.max;
        const x0 = o.align === 'center' ? x - l / 2 : o.align === 'right' ? x - l : x;
        box(x, y, x0, y - t * .95, x0 + l, y + t * .3); return px;
      },
      trait(pts) { nuage(pts); return px; },
      ligne(x1, y1, x2, y2) { box(x1, y1, x1, y1, x2, y2); return px; },
      fleche(x1, y1, x2, y2) { box(x1, y1, x1 - 6, y1 - 6, x2 + 6, y2 + 6); return px; },
      cote(x1, y1, x2, y2) { box(x1, y1, x1, y1 - 20, x2, y2 + 6); return px; },
      rect(x, y, w, h) { box(x + Math.min(w, 2), y + Math.min(h, 2), x, y, x + w, y + h); return px; },
      cercle(x, y, r) { box(x, y, x - r, y - r, x + r, y + r); return px; },
      point(x, y, r = 4) { box(x, y, x - r, y - r, x + r, y + r); return px; },
      courbe(fn, n) { const p = []; for (let i = 0; i <= n; i++) { const q = fn(i / n); if (q) p.push(q); } nuage(p); return px; },
      repere() { return px; },
      __bloc(x, y, w, h) { box(x, y, x, y, x + w, y + h); },
      __remplir() { return px; },
    };
    px = new Proxy(c0, { get(t, k) { if (k in over) return over[k]; const v = t[k]; return typeof v === 'function' ? v.bind(t) : v; }, set(t, k, v) { t[k] = v; return true; } });
    return px;
  }

  /* ── le plan automatique ── */
  function analyser(items, axes, o) {
    if (!axes.length && o.col == null) return null;   // sans repère, il faut dire où commencent les phrases
    const gR = axes.length ? Math.max(...axes.map((a) => a.x0 + a.w)) + 28 : o.col, gL = axes.length ? Math.min(...axes.map((a) => a.x0)) : 0;
    // repère à gauche, phrases à droite (le plus courant) ; ou l'inverse : repère à droite, phrases à gauche (miroir)
    const miroir = gL > 300;
    const X = o.col ?? (miroir ? gL - 34 : gR - 4);
    const phrase = (i) => !i.g && (miroir ? i.ax < X - 10 : i.ax >= X - 10);
    const R = items.filter(phrase), G = items.filter((i) => !phrase(i));
    if (R.length < 2) return null;
    // les blancs verticaux de la colonne des phrases
    const iv = R.map((i) => [i.y0, i.y1]).sort((a, b) => a[0] - b[0]), blocs = [];
    for (const [a, b] of iv) { const d = blocs[blocs.length - 1]; if (d && a <= d[1] + 2) d[1] = Math.max(d[1], b); else blocs.push([a, b]); }
    const coupes = o.coupes ? [o.coupes] : [[]];
    if (!o.coupes) for (let i = 1; i < blocs.length; i++) { coupes.push([(blocs[i - 1][1] + blocs[i][0]) / 2]); for (let j = i + 1; j < blocs.length; j++) coupes.push([(blocs[i - 1][1] + blocs[i][0]) / 2, (blocs[j - 1][1] + blocs[j][0]) / 2]); }
    const sx0 = Math.min(...R.map((i) => i.x0)), droite = Math.max(...R.map((i) => i.x1)), Wsrc = Math.max(40, droite - sx0);
    return { X, miroir, sx0, Wsrc, R, G, axes, coupes, kmin: o.kmin ?? .6, iso: !!o.iso };
  }
  function plan(c, A) {
    const Hw = Math.max(150, Math.min(420, VW * c.H / c.W));
    // zone du repère : boîte de ce qui l'entoure, sur toute la hauteur ; la largeur qu'elle demande (étirement ≤ 1,45)
    const gb = [...A.G, ...A.axes.map((a) => ({ x0: a.x0 - 34, y0: a.y0 - 22, x1: a.x0 + a.w + 26, y1: a.y0 + a.h + 26 }))];
    const g0 = Math.max(A.miroir ? A.X : 0, Math.min(...gb.map((i) => i.x0))), g1 = Math.min(A.miroir ? VW : A.X, Math.max(...gb.map((i) => i.x1)));
    const h0 = Math.max(0, Math.min(...gb.map((i) => i.y0))), h1 = Math.min(430, Math.max(...gb.map((i) => i.y1)));
    const sy = (Hw - 8) / Math.max(40, h1 - h0), etire = A.iso ? 1 : 1.45, reserve = Math.max(A.iso ? 200 : 260, Math.min(340, (g1 - g0) * sy * etire + 26));
    let best = null;
    for (const cps of A.coupes) {
      const ys = [-1e9, ...cps, 1e9], cols = [];
      for (let i = 0; i < ys.length - 1; i++) {
        const its = A.R.filter((it) => it.ay >= ys[i] && it.ay < ys[i + 1]);
        if (!its.length) { cols.length = 0; break; }
        cols.push({ a: ys[i], b: ys[i + 1], top: Math.min(...its.map((it) => it.y0)), bas: Math.max(...its.map((it) => it.y1)) });
      }
      if (!cols.length) continue;
      const n = cols.length, hmax = Math.max(...cols.map((q) => q.bas - q.top));
      const k = Math.min(1.1, (Hw - TOP - 4) / hmax, (VW - 8 - reserve - 14 - ECART * (n - 1)) / (n * A.Wsrc));
      // une colonne presque vide n'aide pas : on pénalise les colonnes déséquilibrées
      const hs = cols.map((q) => q.bas - q.top), note = k * (1 - .35 * (1 - Math.min(...hs) / Math.max(...hs)));
      if (!best || note > best.note * 1.04) best = { k, cols, note };
    }
    if (!best || best.k < A.kmin) return null;
    const { k, cols } = best, n = cols.length;
    const larg = n * A.Wsrc * k + ECART * (n - 1), xr0 = A.miroir ? 8 : VW - 8 - larg;
    const zones = cols.map((q, i) => ({ a: q.a, b: q.b, sx0: A.sx0, sy0: q.top, tx: xr0 + i * (A.Wsrc * k + ECART), ty: TOP + 4, sx: k, sy: k, kt: k }));
    const dispo = VW - larg - 8 - 18 - 4, gx = A.miroir ? 8 + larg + 18 : 4;   // place du repère : à côté des colonnes
    const sx = Math.min(dispo / Math.max(40, g1 - g0), sy * etire);
    const zg = { sx0: g0, sy0: h0, tx: gx + (dispo - (g1 - g0) * sx) / 2, ty: 4, sx, sy, kt: Math.max(.72, Math.min(.9, sy * 1.2)) };
    return { Hw, k, xr0, larg, zones, zg, X: A.X, miroir: A.miroir };
  }
  function zone(P, x, y) { if (DRAP.gauche || (P.miroir ? x >= P.X - 10 : x < P.X - 10)) return P.zg; return P.zones.find((z) => y >= z.a && y < z.b) || P.zones[P.zones.length - 1]; }
  const map = (z, x, y) => [z.tx + (x - z.sx0) * z.sx, z.ty + (y - z.sy0) * z.sy];
  const depuis = (P, X, Y) => { const z = P.zg; return [z.sx0 + (X - z.tx) / z.sx, z.sy0 + (Y - z.ty) / z.sy]; };

  /* ── l'intermédiaire de la craie : chaque tracé est transformé selon la zone de son point d'ancrage ── */
  function craie(c0, P) {
    const Z = (x, y) => zone(P, x, y);
    const over = {
      texte(s, x, y, o = {}) { const z = Z(x, y), [X, Y] = map(z, x, y); return c0.texte(s, X, Y, { ...o, taille: (o.taille ?? 18) * z.kt, max: o.max ? o.max * (z === P.zg ? z.sx : z.kt) : o.max }); },
      trait(pts, o = {}) { if (!pts || !pts.length) return c0; const z = Z(pts[0][0], pts[0][1]); return c0.trait(pts.map((p) => map(z, p[0], p[1])), o); },
      ligne(x1, y1, x2, y2, o) { const z = Z(x1, y1), a = map(z, x1, y1), b = map(z, x2, y2); return c0.ligne(a[0], a[1], b[0], b[1], o); },
      fleche(x1, y1, x2, y2, o = {}) { const z = Z(x1, y1), a = map(z, x1, y1), b = map(z, x2, y2); return c0.fleche(a[0], a[1], b[0], b[1], { ...o, tete: (o.tete ?? 11) * Math.max(.75, z.kt) }); },
      cote(x1, y1, x2, y2, s, o = {}) { const z = Z(x1, y1), a = map(z, x1, y1), b = map(z, x2, y2); return c0.cote(a[0], a[1], b[0], b[1], s, { ...o, taille: (o.taille ?? 18) * z.kt }); },
      rect(x, y, w, h, o = {}) { const z = Z(x + Math.min(w, 2), y + Math.min(h, 2)), a = map(z, x, y); return c0.rect(a[0], a[1], w * z.sx, h * z.sy, { ...o, arrondi: (o.arrondi ?? 8) * z.kt }); },
      cercle(x, y, r, o) { const z = Z(x, y), [X, Y] = map(z, x, y); return c0.cercle(X, Y, r * Math.max(.75, z.kt), o); },
      point(x, y, r = 4, coul) { const z = Z(x, y), [X, Y] = map(z, x, y); return c0.point(X, Y, r * Math.max(.85, z.kt), coul); },
      courbe(fn, n, o) { let z = null; return c0.courbe((u) => { const p = fn(u); if (!p) return p; z = z || Z(p[0], p[1]); return map(z, p[0], p[1]); }, n, o); },
      repere(id, x, y, w, h, l) { const z = Z(x + Math.min(w, 2), y + Math.min(h, 2)), a = map(z, x, y); return c0.repere(id, a[0], a[1], w * z.sx, h * z.sy, l); },
      __bloc(x, y, w, h, coul, o) { const z = Z(x, y), a = map(z, x, y); return BLOC(c0, a[0], a[1], w * z.sx, h * z.sy, coul, o); },
      // zones colorées du kit (MathsTableau.remplir, 16 novembre 2026) : transformées comme un trait
      __remplir(pts, o) { const z = Z(pts[0][0], pts[0][1]); return window.MathsTableau.peint(c0, c0.ctx, pts.map((p) => map(z, p[0], p[1])), o); },
    };
    /* Peinture directe sur le contexte (c.ctx : remplissages, MathsTableau.peindre) : le contexte rendu porte la
     * transformation de la zone du repère ; chaque tracé de la craie remet d'abord la transformation de la scène. */
    const base = c0.ctx.getTransform(), zg = P.zg;
    const scene = () => c0.ctx.setTransform(base);
    for (const [k, f] of Object.entries(over)) over[k] = function (...a) { scene(); return f.apply(this, a); };
    return new Proxy(c0, {
      get(t, k) {
        if (k in over) return over[k];
        if (k === 'ctx') { const x = t.ctx; x.setTransform(base); x.translate(zg.tx - zg.sx0 * zg.sx, zg.ty - zg.sy0 * zg.sy); x.scale(zg.sx, zg.sy); return x; }
        if (k === '__scene') return scene;
        const v = t[k]; return typeof v === 'function' ? v.bind(t) : v;
      },
      set(t, k, v) { t[k] = v; return true; },
    });
  }

  /* ── les aides K refaites sur l'intermédiaire (copie de maths-tableau.js, même rendu) ── */
  function aides(K, c, c0, P, axes) {
    const K2 = Object.create(K);
    K2.c = c;
    K2.titre = (s) => { if (window.MathsTableau.titreRepete(s)) { c0.pause(window.MathsTableau.tempsTitre(s)); return K2; } if (P) c0.texte(s, P.xr0, 26, { couleur: 'cyan', taille: 20 * Math.min(1.1, Math.max(.85, P.k * 1.1)), max: P.larg }); return K2; };
    K2.axes = (o) => {
      const g = K.grille(o);
      if (axes) axes.push({ x0: g.x0, y0: g.y0, w: g.w, h: g.h });
      DRAP.gauche = true;
      try { traceAxes(g); } finally { DRAP.gauche = false; }
      return g;
    };
    const traceAxes = (g) => {
      const ax = Math.min(Math.max(0, g.ymin), g.ymax), ay = Math.min(Math.max(0, g.xmin), g.xmax);
      const yA = g.Y(ax), xA = g.X(ay);
      if (g.quadrillage) for (let x = Math.ceil(g.xmin); x <= g.xmax; x++) c.ligne(g.X(x), g.y0, g.X(x), g.y0 + g.h, { couleur: 'tresfaible', largeur: .8, duree: .02 });
      c.fleche(g.x0 - 6, yA, g.x0 + g.w + 14, yA, { couleur: 'faible', largeur: 1.6 });
      c.fleche(xA, g.y0 + g.h + 6, xA, g.y0 - 14, { couleur: 'faible', largeur: 1.6 });
      c.texte(g.nomx, g.x0 + g.w + 18, yA + 18, { couleur: 'faible', taille: 16 });
      c.texte(g.nomy, xA - 18, g.y0 - 6, { couleur: 'faible', taille: 16 });
      for (const v of g.gx || []) { const [x, l] = Array.isArray(v) ? v : [v, fr(v)]; c.ligne(g.X(x), yA - 4, g.X(x), yA + 4, { couleur: 'faible', largeur: 1.2, duree: .02 }); if (l !== '') c.texte(l, g.X(x), yA + 19, { couleur: 'faible', taille: 15, align: 'center', duree: .05 }); }
      for (const v of g.gy || []) { const [y, l] = Array.isArray(v) ? v : [v, fr(v)]; c.ligne(xA - 4, g.Y(y), xA + 4, g.Y(y), { couleur: 'faible', largeur: 1.2, duree: .02 }); if (l !== '') c.texte(l, xA - 8, g.Y(y) + 5, { couleur: 'faible', taille: 15, align: 'right', duree: .05 }); }
      if (g.origine !== false && g.xmin < 0 && g.ymin < 0) c.texte('O', xA - 14, yA + 17, { couleur: 'faible', taille: 15 });
      return g;
    };
    K2.courbe = (G, f, a, b, o = {}) => { for (const m of K._points(G, f, a, b, o.n || 160)) window.MathsTableau.trace(c, m, { tremble: .35, couleur: o.couleur || 'cyan', largeur: o.largeur ?? 2.6, pointille: o.pointille, duree: o.duree }); return K2; };
    K2.courbePart = (G, f, a, b, p, o = {}) => {
      if (p <= 0) return K2;
      const bb = a + (b - a) * p;
      for (const m of K._points(G, f, a, bb, Math.max(4, Math.round((o.n || 160) * p)))) window.MathsTableau.trace(c, m, { tremble: .35, couleur: o.couleur || 'cyan', largeur: o.largeur ?? 2.6, pointille: o.pointille });
      return K2;
    };
    K2.proj = (G, x, y, o = {}) => {
      const ax = Math.min(Math.max(0, G.ymin), G.ymax), ay = Math.min(Math.max(0, G.xmin), G.xmax), coul = o.couleur || 'faible';
      if (o.versX !== false) c.ligne(G.X(x), G.Y(y), G.X(x), G.Y(ax), { couleur: coul, largeur: 1.3, pointille: [5, 5] });
      if (o.versY !== false) c.ligne(G.X(x), G.Y(y), G.X(ay), G.Y(y), { couleur: coul, largeur: 1.3, pointille: [5, 5] });
      if (o.lx) c.texte(o.lx, G.X(x), G.Y(ax) + (y < ax ? -10 : 20), { couleur: o.couleurTexte || coul, taille: o.taille || 15, align: 'center' });
      if (o.ly) c.texte(o.ly, G.X(ay) - 8, G.Y(y) + 5, { couleur: o.couleurTexte || coul, taille: o.taille || 15, align: 'right' });
      return K2;
    };
    K2.rond = (G, x, y, plein = true, couleur = 'jaune') => { window.MathsTableau.pastille(c, G.X(x), G.Y(y), plein, couleur); return K2; };
    K2.lignes = (x, y, liste, inter = 30) => {
      for (const l of liste) {
        if (l.pause) c.pause(l.pause);
        if (l.t) c.texte(l.t, x + (l.dx || 0), y, { couleur: l.couleur || 'blanc', taille: l.taille || 19, max: l.max || (VW - x - 16) });
        if (l.cadre) { const w = c.largeurTexte(l.t, l.taille || 19) + 16; c.rect(x + (l.dx || 0) - 8, y - (l.taille || 19) - 2, w, (l.taille || 19) + 12, { couleur: l.cadre, arrondi: 6, largeur: 1.4 }); }
        if (l.repere) c.repere(l.repere, x + (l.dx || 0) - 4, y - 22, Math.min(VW - x - 10, c.largeurTexte(l.t || '', l.taille || 19) + 10), 30, l.label || l.t);
        if (l.moment) K.marque(l.moment);
        y += l.inter ?? inter;
      }
      return y;
    };
    return K2;
  }

  /* Plan écrit à la main : o.zones = [[a, b, sx0, sy0, tx, ty, k], …] : ce qui est ancré entre les ordonnées a et b
   * est déplacé de (sx0, sy0) vers (tx, ty) et mis à l'échelle k ; tout le reste du dessin reste à sa place. */
  function manuel(o) {
    const zones = o.zones.map(([a, b, sx0, sy0, tx, ty, k]) => ({ a, b, sx0, sy0, tx, ty, sx: k, sy: k, kt: k }));
    return { X: -1e9, miroir: false, zg: { sx0: 0, sy0: 0, tx: 0, ty: 0, sx: 1, sy: 1, kt: 1 }, zones, xr0: o.titre ?? 20, larg: 700, k: zones[0].kt };
  }

  /* ── les vues : le plan se calcule à la mesure de la boîte (construction complète), une fois par taille de tableau ── */
  function vues(V, cfg) {
    for (const [nom, v] of Object.entries(V)) {
      const o = cfg[nom] === true ? {} : cfg[nom]; if (!o) continue;
      const dessiner = v.dessiner, poignees = v.poignees;
      let cle = null, P = null;
      v.dessiner = function (c0, K) {
        if (!actif(c0)) { ETAT = null; return dessiner.call(this, c0, K); }
        if (o.zones && !P) P = manuel(o);
        const m = window.__maths, k = `${Math.round(c0.W)}x${Math.round(c0.H)}:${document.fonts ? document.fonts.status : ''}`;   // police chargée : mesures refaites
        if (!o.zones && cle !== k && m) {
          // à blanc : relever les boîtes de la construction COMPLÈTE (temps du tableau et de la craie rétablis après)
          const items = [], axes = [], sauve = { cur: c0.cur, complet: c0.complet, tip: c0.tip, t: c0.t }, tw = m.S.tw;
          try { m.S.tw = 1e6; c0.t = Infinity; const cr = enregistreur(c0, items); dessiner.call(this, cr, aides(K, cr, c0, null, axes)); const A = analyser(items, axes, o); P = A && plan(c0, A); }
          catch (e) { console.warn('[large] plan', e); P = null; }
          finally { Object.assign(c0, sauve); m.S.tw = tw; }
          cle = k;
          // nouvelle disposition : la boîte de l'encre du kit est mesurée à nouveau à l'image suivante
          if (!m.scene.mesurant) { m.scene.boite = null; m.scene.sale = true; }
        }
        ETAT = P;
        if (!P) return dessiner.call(this, c0, K);
        const c = craie(c0, P);
        try { return dessiner.call(this, c, aides(K, c, c0, P)); } finally { c.__scene(); }
      };
      if (poignees) v.poignees = function (K) {
        const hs = poignees.call(this, K) || [], P = ETAT;
        if (!P) return hs;
        return hs.map((h) => { const [X, Y] = map(P.zg, h.x, h.y); return { ...h, x: X, y: Y, bouger: (x, y) => h.bouger(...depuis(P, x, y)) }; });
      };
    }
    return V;
  }

  let BLOC = null;
  /* Une page entière : MathsTableau.page enveloppe ses vues avec `cfg` (à appeler avant MathsTableau.page).
   * MathsTableau.bloc (peinture directe sur le contexte) passe aussi par l'intermédiaire quand il y en a un. */
  function config(cfg) {
    const MT = window.MathsTableau, page = MT.page;
    if (!BLOC) { BLOC = MT.bloc; MT.bloc = (c, ...a) => (c.__bloc ? c.__bloc(...a) : BLOC(c, ...a)); }
    MT.page = (def) => page({ ...def, vues: vues(def.vues, cfg) });
  }

  window.Large = { actif, vues, config, etat: () => ETAT };
})();
