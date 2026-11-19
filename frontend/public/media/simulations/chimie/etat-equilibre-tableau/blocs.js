/*
 * blocs.js — tableau large en BLOCS (15 novembre 2026, deuxième passe « agrandir les figures elles-mêmes »).
 *
 * Les vues de ce dossier sont dessinées pour un cadre 760 × 420. Sur un tableau large (scene.L ≥ 1000, écran
 * d'ordinateur portable), une vue qui déclare une disposition en blocs est redistribuée SANS réécrire son dessin :
 *   def = { cols: [ [bloc, …], … ], marge, ecart, enleve: [[x0, y0, x1, y1], …], direct: i }
 *   bloc = { r: [x0, y0, x1, y1] (rectangle du dessin d'origine), k: agrandissement maximal (défaut 2,2), centre: bool,
 *            prio: bool (ce bloc est essayé en premier quand des rectangles se chevauchent) }
 * Chaque colonne empile ses blocs ; elle est agrandie au plus possible (toute la hauteur, au plus k), puis toutes
 * les colonnes sont réduites ensemble si elles ne tiennent pas en largeur, et les colonnes se répartissent la place.
 * Chaque appel de craie (texte, trait, rect, flèche, point, repère…) est placé par le bloc qui contient son point
 * d'ancrage (le plus proche sinon) : la figure grandit dans sa colonne, les colonnes de texte dans la leur, et les
 * repères du professeur suivent (ils sont posés avec la transformation courante). Les appels ancrés dans un rectangle
 * `enleve` (le titre interne : le titre de la diapositive le dit déjà) ne sont pas dessinés. Les peintures directes
 * (c.direct : verrerie, appareils) prennent le bloc `direct` (index à plat, défaut 0) ou celui donné par
 * def.directs[n] pour le n-ième appel de l'image.
 * Sinon (L < 1000, mesure de la boîte de l'encre, vue sans blocs) rien ne change.
 */
(function () {
  'use strict';
  const TEXTE_MIN = 18;   // px à l'écran, textes d'une vue en blocs (def.texteMin pour une vue serrée)
  const PRIM = ['texte', 'trait', 'ligne', 'fleche', 'cote', 'rect', 'cercle', 'courbe', 'point', 'repere', 'axe', 'direct'];
  const ancre = {
    texte: (s, x, y, o = {}) => [x, y - (o.taille ?? 18) * .35],
    trait: pts => { if (!pts || !pts.length) return null; let a = 1e9, b = -1e9, c = 1e9, d = -1e9; for (const p of pts) { a = Math.min(a, p[0]); b = Math.max(b, p[0]); c = Math.min(c, p[1]); d = Math.max(d, p[1]); } return [(a + b) / 2, (c + d) / 2]; },
    ligne: (x1, y1, x2, y2) => [(x1 + x2) / 2, (y1 + y2) / 2],
    fleche: (x1, y1, x2, y2) => [(x1 + x2) / 2, (y1 + y2) / 2],
    cote: (x1, y1, x2, y2) => [(x1 + x2) / 2, (y1 + y2) / 2],
    axe: (x1, y1, x2, y2) => [(x1 + x2) / 2, (y1 + y2) / 2],
    rect: (x, y, w, h) => [x + w / 2, y + h / 2],
    cercle: (x, y) => [x, y],
    point: (x, y) => [x, y],
    courbe: fn => { const p = fn(.5) || fn(0) || fn(1); return p || null; },
    repere: (id, x, y, w, h) => [x + w / 2, y + h / 2],
  };
  const dans = (r, p) => p[0] >= r[0] && p[0] <= r[2] && p[1] >= r[1] && p[1] <= r[3];
  const dist = (r, p) => Math.hypot(Math.max(r[0] - p[0], 0, p[0] - r[2]), Math.max(r[1] - p[1], 0, p[1] - r[3]));

  /** Calcule la place de chaque bloc : { blocs: [{ r, k, dx, dy }] } dans le cadre L × 420. */
  function disposer(def, L, H = 420) {
    const m = def.marge ?? 14, e = def.ecart ?? 26, ev = def.ecartV ?? 14;
    const cols = def.cols.map(bl => {
      const w = Math.max(...bl.map(b => b.r[2] - b.r[0])), h = bl.reduce((s, b) => s + b.r[3] - b.r[1], 0) + ev * (bl.length - 1);
      const kmax = Math.min(...bl.map(b => b.k ?? 2.2));
      return { bl, w, h, k: Math.min(kmax, (H - 2 * m - ev * (bl.length - 1)) / (h - ev * (bl.length - 1))) };
    });
    let tot = cols.reduce((s, c) => s + c.w * c.k, 0) + e * (cols.length - 1);
    const place = L - 2 * m;
    if (tot > place) { const f = (place - e * (cols.length - 1)) / (tot - e * (cols.length - 1)); cols.forEach(c => { c.k *= f; }); tot = place; }
    const libre = (place - tot) / (cols.length + 1);
    const out = []; let x = m + libre;
    for (const c of cols) {
      const hh = c.h * c.k - ev * (c.bl.length - 1) * (c.k - 1);
      let y = def.haut ? m : Math.max(m, (H - hh) / 2);
      for (const b of c.bl) {
        const w = (b.r[2] - b.r[0]) * c.k, dx = x + (b.centre ? (c.w * c.k - w) / 2 : 0) - b.r[0] * c.k, dy = y - b.r[1] * c.k;
        out.push({ r: b.r, k: c.k, dx, dy, prio: !!b.prio, dest: [x, y, x + c.w * c.k, y + (b.r[3] - b.r[1]) * c.k] });
        y += (b.r[3] - b.r[1]) * c.k + ev;
      }
      x += c.w * c.k + e + libre;
    }
    return out;
  }

  const ETAT = new WeakMap();
  /** À appeler juste après scene.cadre() : renvoie true si la vue est disposée en blocs (tableau large). */
  function poser(c, scene, def) {
    let st = ETAT.get(c);
    if (!st) { st = { actif: false }; ETAT.set(c, st); }
    st.actif = false;
    if (typeof def === 'function') def = def(scene.L);
    if (!def || scene.mesurant || scene.L < 1000 || !(c.W > 1)) { if (st.localAvant) { scene.local = st.localAvant; st.localAvant = null; } return false; }
    installer(c, st);                               // (re)pose les enveloppes : la mesure de l'encre remet les siennes
    const L = scene.L, s0 = Math.min(c.W / L, c.H / 420), ox = (c.W - L * s0) / 2, oy = (c.H - 420 * s0) / 2, d = devicePixelRatio || 1;
    c.ctx.setTransform(d, 0, 0, d, 0, 0); c.ctx.translate(ox, oy); c.ctx.scale(s0, s0);
    scene.s = s0; scene.ox = ox; scene.oy = oy; c.echelle = s0; c.cadre = null;
    if (!def.enleve) def = { ...def, enleve: [[0, 0, 760, 36]] };   // le titre interne (défaut)
    st.base = c.ctx.getTransform(); st.blocs = disposer(def, L); st.def = def; st.nDirect = 0; st.actif = true;
    /* (18 novembre 2026) Le plancher des blocs vaut aussi pour les MESURES faites hors des appels de craie (largeur
     * d'un côté d'équation, place d'une flèche) : mesurées au plancher de la craie (15 px) et écrites à celui des blocs
     * (18 px), les équations débordaient sur leur flèche ⇌. scene.cadre() remet le plancher à chaque image. */
    c.tailleMin = Math.max(c.tailleMin || 0, def.texteMin ?? TEXTE_MIN);
    if (!st.localAvant) {
      st.localAvant = scene.local;
      scene.local = (x, y) => {                       // pointeur → coordonnées du dessin d'origine (poignées des curseurs)
        const X = (x - scene.ox) / scene.s, Y = (y - scene.oy) / scene.s;
        if (!st.actif) return [X, Y];
        const b = st.blocs.find(q => dans(q.dest, [X, Y])) || st.blocs.reduce((a, q) => (dist(q.dest, [X, Y]) < dist(a.dest, [X, Y]) ? q : a));
        return [(X - b.dx) / b.k, (Y - b.dy) / b.k];
      };
    }
    return def;
  }
  function blocDe(st, p) {
    let best = null, bd = 1e9;
    for (const b of st.blocs) if (b.prio && dans(b.r, p)) return b;   // bloc prioritaire (il chevauche la figure)
    for (const b of st.blocs) { if (dans(b.r, p)) return b; const dd = dist(b.r, p); if (dd < bd) { bd = dd; best = b; } }
    return best;
  }
  /** Peinture directe : on la joue une fois « à blanc » (rien n'est peint) pour savoir où elle tombe. */
  const DESSINE = ['fill', 'stroke', 'fillText', 'strokeText', 'drawImage', 'fillRect', 'strokeRect', 'clearRect', 'putImageData'];
  const POINTS = ['moveTo', 'lineTo', 'arc', 'ellipse', 'rect', 'roundRect', 'fillRect', 'strokeRect', 'quadraticCurveTo', 'bezierCurveTo', 'fillText', 'drawImage', 'arcTo'];
  function sonder(c, f, a) {
    const ctx = c.ctx, bb = [1e9, 1e9, -1e9, -1e9], sauve = {};
    const note = (x, y) => { if (Number.isFinite(x) && Number.isFinite(y)) { const m = ctx.getTransform(), q = st0.base.inverse().multiply(m).transformPoint(new DOMPoint(x, y)); bb[0] = Math.min(bb[0], q.x); bb[1] = Math.min(bb[1], q.y); bb[2] = Math.max(bb[2], q.x); bb[3] = Math.max(bb[3], q.y); } };
    const st0 = ETAT.get(c), proto = Object.getPrototypeOf(ctx);
    for (const n of new Set(DESSINE.concat(POINTS))) {
      sauve[n] = Object.prototype.hasOwnProperty.call(ctx, n) ? ctx[n] : undefined;
      ctx[n] = function (...v) {
        if (n === 'fillText' || n === 'strokeText') note(v[1], v[2]);
        else if (n === 'drawImage') note(v[v.length >= 5 ? (v.length >= 9 ? 5 : 1) : 1], v[v.length >= 9 ? 6 : 2]);
        else if (n === 'bezierCurveTo') note(v[4], v[5]); else if (n === 'quadraticCurveTo') note(v[2], v[3]);
        else if (POINTS.includes(n)) note(v[0], v[1]);
        if (!DESSINE.includes(n)) return proto[n].apply(ctx, v);
      };
    }
    const t = c.t, cur = c.cur, tip = c.tip, comp = c.complet, tm = c.tailleMin; st0.sonde = true;
    c.tailleMin = Math.max(tm || 0, st0.def.texteMin ?? TEXTE_MIN);   // même plancher qu'au vrai dessin
    ctx.save(); ctx.setTransform(st0.base);
    try { f.apply(c, a); } catch (e) { /* rien */ } finally {
      ctx.restore(); st0.sonde = false; c.t = t; c.cur = cur; c.tip = tip; c.complet = comp; c.tailleMin = tm;
      for (const n of Object.keys(sauve)) { if (sauve[n] === undefined) delete ctx[n]; else ctx[n] = sauve[n]; }
    }
    return bb[2] >= bb[0] ? [(bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2] : null;
  }
  function installer(c, st) {
    let prof = 0;
    for (const nom of PRIM) {
      if (typeof c[nom] !== 'function' || c[nom].__bloc) continue;
      const propre = Object.prototype.hasOwnProperty.call(c, nom) && c[nom] !== Object.getPrototypeOf(c)[nom] ? c[nom] : null;
      c[nom] = function (...a) {
        const f = propre || Object.getPrototypeOf(this)[nom];   // le prototype lu à chaque appel (outils de mesure)
        if (st.sonde && nom === 'repere') return this;
        if (!st.actif || st.sonde || prof > 0 && nom !== 'direct' && st.dansDirect !== prof) return f.apply(this, a);
        let b;
        if (nom === 'direct') {
          const i = st.def.directs ? st.def.directs[st.nDirect] : undefined; st.nDirect++;
          if (i != null) b = st.blocs[i];
          else { const p = sonder(this, f, a); b = p ? blocDe(st, p) : st.blocs[st.def.direct ?? 0]; }
          if (!b) b = st.blocs[0];
        } else {
          const p = ancre[nom] && ancre[nom](...a); if (!p || !Number.isFinite(p[0])) return f.apply(this, a);
          if (st.def.enleve && st.def.enleve.some(r => dans(r, p))) return this;
          b = blocDe(st, p);
        }
        const ctx = this.ctx, avant = ctx.getTransform(), tip = this.tip;
        ctx.setTransform(st.base); ctx.translate(b.dx, b.dy); ctx.scale(b.k, b.k);
        const ech = this.echelle; this.echelle = ech * b.k;   // texte jamais sous 15 px : à l'échelle du bloc
        // Troisième passe (texte 18-22 px à l'écran) : plancher def.texteMin (défaut 18 px écran) au lieu des 15 de la craie.
        const tmin = this.tailleMin; this.tailleMin = Math.max(tmin || 0, st.def.texteMin ?? TEXTE_MIN);
        prof++; if (nom === 'direct') st.dansDirect = prof;
        try { return f.apply(this, a); }
        finally {
          prof--; if (nom === 'direct') st.dansDirect = 0;
          this.echelle = ech; this.tailleMin = tmin;
          if (this.tip && this.tip !== tip) this.tip = [b.dx + this.tip[0] * b.k, b.dy + this.tip[1] * b.k];
          ctx.setTransform(avant);
        }
      };
      c[nom].__bloc = true;
    }
  }
  window.Blocs = { poser, disposer };
})();
