/*
 * Tableau large (15 novembre 2026, « mieux exploiter tout le tableau, grands calibres de texte, simulations agrandies ») :
 * une vue dessinée pour le cadre 760 × 420 est découpée en ZONES (rectangles du dessin d'origine) rangées en COLONNES
 * sur toute la largeur du tableau (scene.L, de 760 à 1292). Chaque colonne prend la plus grande échelle qui tient dans
 * la hauteur (bornée à `max`), puis l'ensemble est réduit s'il dépasse la largeur. La figure grandit vers le bas, les
 * textes vont à côté, plus gros. Sous L_MIN (grand écran 1920 × 1080, déjà haut) : la disposition d'origine.
 *
 *   Zones.dessiner(c, L, spec, fn) : fn() dessine la vue comme avant ; elle est rejouée une fois par zone, découpée et
 *   transformée (craie, peinture et repères suivent la même transformation : le professeur pointe au bon endroit).
 *   spec = { cols: [[[x0, y0, x1, y1], …], …], max?: 1.7, gap?: 26, vgap?: 14, centre?: true, top?: 40, haut?: false }
 *   (top : marge du haut ; 10 depuis que le titre interne est retiré sur un tableau large).
 *   Une zone peut exclure des parties d'elle-même : [x0, y0, x1, y1, [[ex0, ey0, ex1, ey1], …]] (rectangles dans la zone).
 *   [.., exclus, xDecoupe] : la zone compte pour sa largeur mais n'est coupée qu'à xDecoupe (une phrase qui s'allonge à l'écran).
 *   Un repère dont le centre n'est dans aucune zone va dans celle qu'il recouvre le plus.
 *   spec.pxMin : plancher des textes à l'écran dans les zones (17 px par défaut) ; une colonne objet peut avoir le sien
 *   (pxMin : 15 pour une figure aux étiquettes serrées).
 *   Zones.vers(x, y) : point du dessin d'origine → point du tableau large (dernière disposition), pour les clics.
 */
(function () {
  'use strict';
  const L_MIN = 1000, H = 420, MARGE = 8;
  let derniere = null, ecran = null, courant = null;   // courant : rectangle (px du canvas) de la zone en cours de dessin (mesure)   // ecran : rectangles des zones en pixels du canvas (mesure)
  /* Deuxième passe (15 novembre 2026, « agrandir les figures elles-mêmes ») : une colonne peut être un objet
   *   { zs: [zones…], t: taille }   colonne de TEXTE : `t` est la taille d'écriture du dessin d'origine ; son échelle est
   *                                 choisie pour que ce texte fasse `px` (spec.px, 20 par défaut) pixels À L'ÉCRAN
   *                                 (e = échelle de la scène, passée par dessiner) ;
   *   { zs: [zones…], max: m }      colonne de FIGURE : la plus grande échelle qui tient dans la hauteur, bornée à m.
   * Si le tout dépasse la largeur, ce sont d'abord les figures qui rétrécissent (le texte garde sa taille à l'écran),
   * puis l'ensemble. Une colonne donnée comme simple tableau garde l'ancien comportement (spec.max). */
  function disposer(L, spec, e = 1) {
    const top = spec.top ?? 10, gap = spec.gap ?? 26, vgap = spec.vgap ?? 14, smax = spec.max ?? 1.7;
    const cols = spec.cols.map(k => {
      const o = Array.isArray(k) ? { zs: k } : k, zs = o.zs;
      const w = Math.max(...zs.map(z => z[2] - z[0])), h = zs.reduce((s, z) => s + z[3] - z[1], 0) + vgap * (zs.length - 1);
      const borne = o.t ? (o.px ?? spec.px ?? 20) / (o.t * (e || 1)) : (o.max ?? smax);
      return { zs, w, h, texte: !!o.t, pxMin: o.pxMin, s: Math.min(borne, (H - top - MARGE) / h) };
    });
    const dispo = L - 2 * MARGE, total = () => cols.reduce((s, k) => s + k.w * k.s, 0) + gap * (cols.length - 1);
    let trop = total() - dispo;
    if (trop > 0) {                                   // les figures rétrécissent d'abord (jusqu'à 60 % de leur échelle)
      const fig = cols.filter(k => !k.texte && cols.some(q => q.texte)), wf = fig.reduce((s, k) => s + k.w * k.s, 0);
      if (wf > 0) { const r = Math.max(.6, (wf - trop) / wf); fig.forEach(k => { k.s *= r; }); }
    }
    const largeur = total();
    const f = largeur > dispo ? dispo / largeur : 1;
    let x = (L - Math.min(largeur * f, dispo)) / 2;
    const out = [];
    for (const k of cols) {
      const s = k.s * f, hTot = k.h * s;
      let y = spec.haut ? top : top + (H - top - MARGE - hTot) / 2;
      for (const z of k.zs) {
        const dx = spec.centre === false ? x : x + (k.w - (z[2] - z[0])) * s / 2;
        out.push({ src: z, dx, dy: y, s, pxMin: k.pxMin });
        y += (z[3] - z[1]) * s + vgap * s;
      }
      x += k.w * s + gap * f;
    }
    return out;
  }
  /** Spec d'une vue « phrases écrites au fil du déroulé + figure » (pages à M.colonne) : à gauche une colonne de texte
   *  (hors du cadre 760, x ≥ 796) dont l'écriture fait `px` pixels à l'écran et dont la hauteur couvre tout le tableau,
   *  large de `part` du tableau ; à droite les colonnes de figure `fig`, agrandies (bornées à `max`). Renvoie la spec
   *  avec `colonne` = { x, w, y0, pas, taille, bas } à donner à M.colonne. e = échelle de la scène. */
  function avecColonne(L, e, fig, o = {}) {
    const top = o.top ?? 10, px = o.px ?? 20, t = o.taille ?? 19, st = px / (t * (e || 1));
    const h = Math.floor((H - top - MARGE) / st), w = Math.round(Math.max(190, (o.part ?? .24) * L / st));
    const colonne = { x: 800, w: w - 8, y0: 46 + Math.round(t * 1.05), pas: Math.round(t * 1.32), taille: t, bas: 46 + h - 6 };
    return { top, gap: o.gap ?? 22, cols: [{ zs: [[796, 46, 796 + w, 46 + h]], t, px }, ...fig.map(zs => ({ zs, max: o.max ?? 2.2, pxMin: o.pxMinFig }))], colonne };
  }
  const dedans = (z, x, y) => x >= z.src[0] && x <= z.src[2] && y >= z.src[1] && y <= z.src[3];
  const recouvre = (z, x, y, w, h) => Math.max(0, Math.min(z.src[2], x + w) - Math.max(z.src[0], x)) * Math.max(0, Math.min(z.src[3], y + h) - Math.max(z.src[1], y));
  function dessiner(c, L, spec, fn) {
    if (!spec || !(L >= L_MIN)) { derniere = null; ecran = null; return fn(); }
    const Z = disposer(L, spec, c.echelle || 1); derniere = Z;
    const ctx = c.ctx, base = ctx.getTransform(), etat = { t: c.t, cur: c.cur, tip: c.tip, complet: c.complet };
    const repere = c.repere, vus = new Set(), orphelins = {};
    ecran = Z.map(z => { const p = base.transformPoint(new DOMPoint(z.dx, z.dy)), q = base.transformPoint(new DOMPoint(z.dx + (z.src[2] - z.src[0]) * z.s, z.dy + (z.src[3] - z.src[1]) * z.s)); return [p.x, p.y, q.x, q.y].map(Math.round); });
    let tip = null, fin = null;
    const poser = z => { ctx.setTransform(base); ctx.translate(z.dx, z.dy); ctx.scale(z.s, z.s); ctx.translate(-z.src[0], -z.src[1]); };
    Z.forEach((z, i) => {
      Object.assign(c, etat); c.tip = null;
      courant = ecran[i];
      ctx.save(); poser(z);
      // une zone qui touche un bord du cadre 760 × 420 n'est pas coupée de ce côté (texte grossi par le plancher de 15 px)
      const k0 = z.src[0] <= 16 ? -40 : z.src[0], k1 = z.src[5] ?? (z.src[2] >= 740 && z.src[2] <= 770 ? 792 : z.src[2]);   // z[5] : bord droit de la découpe, si le texte peut déborder sans gêner
      const h0 = z.src[1] <= 8 ? -20 : z.src[1], h1 = z.src[3] >= 400 && z.src[3] <= 420 ? 440 : z.src[3];
      ctx.beginPath(); ctx.rect(k0, h0, k1 - k0, h1 - h0);
      for (const e of z.src[4] || []) ctx.rect(e[0], e[1], e[2] - e[0], e[3] - e[1]);   // parties exclues (dessinées par une autre zone)
      ctx.clip('evenodd');
      c.repere = function (id, x, y, w, h, label) {
        if (dedans(z, x + w / 2, y + h / 2)) { vus.add(id); return repere.call(this, id, x, y, w, h, label); }
        const a = recouvre(z, x, y, w, h); if (!orphelins[id] || a > orphelins[id].a) orphelins[id] = { a, i, args: [id, x, y, w, h, label] };
        return this;
      };
      // plancher d'écriture À L'ÉCRAN dans la zone (échelle de la scène × échelle de la zone) : spec.pxMin, 17 px par défaut
      const e0 = c.echelle, m0 = c.tailleMin;
      if (e0) { c.echelle = e0 * z.s; c.tailleMin = Math.max(m0 || 0, z.pxMin ?? spec.pxMin ?? 17); }
      try { fn(); } finally { c.repere = repere; c.echelle = e0; c.tailleMin = m0; ctx.restore(); }
      if (c.tip && dedans(z, c.tip[0], c.tip[1])) tip = [z.dx + (c.tip[0] - z.src[0]) * z.s, z.dy + (c.tip[1] - z.src[1]) * z.s];
      fin = { t: c.t, cur: c.cur, complet: c.complet };
    });
    courant = null;
    for (const [id, o] of Object.entries(orphelins)) {
      if (vus.has(id)) continue;
      ctx.save(); poser(Z[o.i]); repere.apply(c, o.args); ctx.restore();
    }
    Object.assign(c, fin); c.tip = tip;
  }
  function vers(x, y) {
    if (!derniere) return [x, y];
    const z = derniere.find(k => dedans(k, x, y)); if (!z) return [x, y];
    return [z.dx + (x - z.src[0]) * z.s, z.dy + (y - z.src[1]) * z.s];
  }
  /** Point du tableau large → point du dessin d'origine (pour un clic) ; null hors des zones. */
  function depuis(x, y) {
    if (!derniere) return [x, y];
    for (const z of derniere) {
      const u = z.src[0] + (x - z.dx) / z.s, v = z.src[1] + (y - z.dy) / z.s;
      if (dedans(z, u, v)) return [u, v];
    }
    return null;
  }
  window.Zones = { dessiner, disposer, avecColonne, vers, depuis, L_MIN, derniere: () => derniere, ecran: () => ecran, courant: () => courant };
})();
