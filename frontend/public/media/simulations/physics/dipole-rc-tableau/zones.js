/*
 * Tableau large par zones (15 novembre 2026, « mieux exploiter tout le tableau, grands calibres de texte ») :
 * pour les pages « graphe + panneau Lecture » dessinées dans le cadre 760 × 420. Sur un tableau large
 * (L = 760 → 1596 ; actif dès L ≥ 1000), chaque zone du dessin d’origine est reportée dans un rectangle du cadre
 * large : le graphe s’étire sur la largeur, le panneau de lecture est coupé en deux colonnes, écrites plus gros.
 * Tout passe par les primitives de la craie (trait, texte, point, repère), remappées zone par zone ; la page
 * n’a pas à changer ses coordonnées. scene.local() rend les coordonnées d’origine (poignées).
 * Grand écran (L < 1000) : disposition d’origine, centrée.
 *
 *   scene.cadre = RCZones(scene, () => S.t, (L) => ({ zones: [...], panneau: {x, y, w, h} }) | null);
 *   zone : { src: {x, y, w, h} (coordonnées d’origine), dst: {x, y, w, h} (cadre large), kt (taille du texte),
 *            cadre: true (dessiner le cadre de la zone à la place du cadre d’origine `panneau`) }
 */
(function () {
  'use strict';
  const VW = 760, VH = 420, L_MAX = 2.1, L_MIN = 1000;
  function RCZones(scene, horloge, disposition) {
    const craie = scene.craie, P = Object.getPrototypeOf(craie);
    const st = { on: false, zones: [], panneau: null };
    const dans = (r, x, y) => x >= r.x - 1e-6 && x <= r.x + r.w + 1e-6 && y >= r.y - 1e-6 && y <= r.y + r.h + 1e-6;
    function zoneDe(x, y) {
      let best = null, d = Infinity;
      for (const z of st.zones) {
        if (dans(z.src, x, y)) return z;
        const dx = Math.max(z.src.x - x, 0, x - z.src.x - z.src.w), dy = Math.max(z.src.y - y, 0, y - z.src.y - z.src.h), e = dx * dx + dy * dy;
        if (e < d) { d = e; best = z; }
      }
      return best;
    }
    const map = (z, x, y) => [z.dst.x + (x - z.src.x) * z.ax, z.dst.y + (y - z.src.y) * z.ay];
    const prepa = z => { z.ax = z.dst.w / z.src.w; z.ay = z.dst.h / z.src.h; z.kt = z.kt ?? Math.min(z.ax, z.ay); return z; };
    let brut = false;                                   // dessin direct (cadres des zones) : pas de remappage
    craie.trait = function (pts, o = {}) {
      if (!st.on || brut || !pts || !pts.length) return P.trait.call(this, pts, o);
      const pn = st.panneau;
      if (pn && pts.length > 8) {                       // le cadre d’origine du panneau → les cadres des zones
        const xs = pts.map(p => p[0]), ys = pts.map(p => p[1]);
        if (Math.abs(Math.min(...xs) - pn.x) < 3 && Math.abs(Math.max(...xs) - pn.x - pn.w) < 3 && Math.abs(Math.min(...ys) - pn.y) < 3 && Math.abs(Math.max(...ys) - pn.y - pn.h) < 3) {
          brut = true;
          try {
            const cz = st.zones.filter(z => z.cadre), bas = Math.max(...cz.map(z => map(z, 0, Math.min(pn.y + pn.h, z.src.y + z.src.h))[1]));
            for (const z of cz) {   // les colonnes du panneau ont la même hauteur
              const [a, b] = map(z, pn.x, Math.max(pn.y, z.src.y)), [c] = map(z, pn.x + pn.w, 0), d = bas;
              const haut = z.src.y > pn.y ? 14 : 0;     // 2e colonne : la première ligne déborde au-dessus de la coupe
              this.rect(a, b - haut, c - a, d - b + haut, { ...o, duree: (o.duree ?? .4) / 2 });
            }
          } finally { brut = false; }
          return this;
        }
      }
      const z = zoneDe(pts[0][0], pts[0][1]);
      return P.trait.call(this, pts.map(p => map(z, p[0], p[1])), o);
    };
    craie.texte = function (s, x, y, o = {}) {
      if (!st.on || brut) return P.texte.call(this, s, x, y, o);
      const z = zoneDe(x, y), [X, Y] = map(z, x, y), o2 = { ...o, taille: (o.taille ?? 18) * z.kt };
      if (o.max) o2.max = o.max * z.ax;
      return P.texte.call(this, s, X, Y, o2);
    };
    craie.point = function (x, y, r = 4, c) {
      if (!st.on || brut) return P.point.call(this, x, y, r, c);
      const z = zoneDe(x, y), [X, Y] = map(z, x, y);
      return P.point.call(this, X, Y, r * Math.min(1.4, z.kt), c);
    };
    craie.repere = function (id, x, y, w, h, label) {
      if (!st.on) return P.repere.call(this, id, x, y, w, h, label);
      const z = zoneDe(x + w / 2, y + h / 2), [X, Y] = map(z, x, y);
      return P.repere.call(this, id, X, Y, w * z.ax, h * z.ay, label);
    };
    scene.local = function (px, py) {
      const fx = (px - scene.ox) / scene.s, fy = (py - scene.oy) / scene.s;
      if (!st.on) return [fx, fy];
      const z = st.zones.find(q => dans(q.dst, fx, fy)) || st.zones[0];
      return [z.src.x + (fx - z.dst.x) / z.ax, z.src.y + (fy - z.dst.y) / z.ay];
    };
    /** Un dessin peint (ctx brut) à la place de sa zone : fn() s’exécute sous la transformation de la zone de (x, y). */
    scene.peindreDans = function (x, y, fn) {
      if (!st.on) return fn();
      const z = zoneDe(x, y), ctx = craie.ctx;
      ctx.save(); ctx.transform(z.ax, 0, 0, z.ay, z.dst.x - z.src.x * z.ax, z.dst.y - z.src.y * z.ay);
      try { return fn(); } finally { ctx.restore(); }
    };
    /** Le cadre de l’image (remplace scene.cadre de la page). */
    return function cadre(graine) {
      const W = craie.W, H = craie.H;
      const L = Math.round(Math.min(VW * L_MAX, Math.max(VW, VH * W / Math.max(1, H))));
      scene.L = L;
      const d = L >= L_MIN ? disposition(L) : null;
      st.on = !!d; st.zones = d ? d.zones.map(prepa) : []; st.panneau = d ? d.panneau || null : null;
      const FW = d ? Math.min(L, d.largeur || L) : VW;   // d.largeur : dessin moins large que le cadre, centré
      craie.debut(graine, horloge());
      const s = Math.min(W / FW, H / VH) || 1;
      scene.s = s; scene.ox = (W - FW * s) / 2; scene.oy = (H - VH * s) / 2;
      craie.ctx.translate(scene.ox, scene.oy); craie.ctx.scale(s, s);
      craie.echelle = s; craie.tailleMin = 15; craie.cadre = d ? null : { w: VW, h: VH, haut: 0 };
      return craie;
    };
  }
  /**
   * Disposition type « graphe à gauche + panneau Lecture à droite » (panneau pn = {x, y, w, h} du cadre d’origine) :
   * le panneau est coupé en deux colonnes à l’ordonnée ys() (entre deux lignes), écrites k fois plus gros ;
   * le graphe prend toute la largeur qui reste. Si la place manque (k < 1,15), panneau d’un bloc, graphe élargi.
   */
  RCZones.grapheEtPanneau = (pn, ys) => (L) => {
    const gx = pn.x - 4, M = 10, GAP = 26, cw = VW - gx;
    const y = ys(), k = Math.min(1.5, (L - 560) / (2 * cw + GAP), (VH - 10) / y, (VH - 20) / (VH - 8 - y + pn.y));
    if (k < 1.15) {
      const gw = L - cw - M;
      return { panneau: null, zones: [
        { src: { x: 0, y: 0, w: gx, h: VH }, dst: { x: 0, y: 0, w: gw, h: VH }, kt: 1 },
        { src: { x: gx, y: 0, w: cw, h: VH }, dst: { x: gw, y: 0, w: cw, h: VH } }] };
    }
    const pw = cw * k, x2 = L - M - pw, x1 = x2 - GAP - pw, gw = x1 - M;
    return { panneau: pn, zones: [
      { src: { x: 0, y: 0, w: gx, h: VH }, dst: { x: 0, y: 0, w: gw, h: VH }, kt: 1 },
      { src: { x: gx, y: 0, w: cw, h: y }, dst: { x: x1, y: 0, w: pw, h: y * k }, cadre: true },
      { src: { x: gx, y, w: cw, h: VH - y }, dst: { x: x2, y: pn.y * k + 14, w: pw, h: (VH - y) * k }, cadre: true }] };
  };
  /** Disposition « tout étiré » : le dessin entier s’étire sur la largeur (textes à leur taille). */
  RCZones.etirer = (L) => ({ panneau: null, zones: [{ src: { x: 0, y: 0, w: VW, h: VH }, dst: { x: 0, y: 0, w: L, h: VH }, kt: 1 }] });
  /**
   * Disposition « partie peinte à gauche, à l’identique (le peint ne suit pas le remappage), le reste à droite » :
   * xg = limite de la partie gauche ; la partie droite s’étire (ax ≤ axMax) ou grandit (iso : k ≤ kMax, recadrée en y).
   */
  RCZones.gaucheFixe = (xg, o = {}) => (L) => {
    const cw = VW - xg;
    if (o.iso) {
      const y0 = o.y0 ?? 0, y1 = o.y1 ?? VH, k = Math.min(o.kMax ?? 1.3, (VH - 8) / (y1 - y0), (L - xg - 30) / cw);
      return { largeur: xg + 30 + cw * k, zones: [
        { src: { x: 0, y: 0, w: xg, h: VH }, dst: { x: 0, y: 0, w: xg, h: VH }, kt: 1 },
        { src: { x: xg, y: y0, w: cw, h: y1 - y0 }, dst: { x: xg + 30, y: (VH - (y1 - y0) * k) / 2, w: cw * k, h: (y1 - y0) * k } }] };
    }
    const ax = Math.min(o.axMax ?? 1.7, (L - xg - 10) / cw);
    return { largeur: xg + cw * ax + 10, zones: [
      { src: { x: 0, y: 0, w: xg, h: VH }, dst: { x: 0, y: 0, w: xg, h: VH }, kt: 1 },
      { src: { x: xg, y: 0, w: cw, h: VH }, dst: { x: xg, y: 0, w: cw * ax, h: VH }, kt: o.kt ?? 1 }] };
  };
  window.RCZones = RCZones;
})();
