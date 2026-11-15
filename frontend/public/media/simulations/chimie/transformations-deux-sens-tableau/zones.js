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
 *   (top : hauteur laissée au titre, que la page écrit elle-même en haut à gauche du tableau large).
 *   Une zone peut exclure des parties d'elle-même : [x0, y0, x1, y1, [[ex0, ey0, ex1, ey1], …]] (rectangles dans la zone).
 *   [.., exclus, xDecoupe] : la zone compte pour sa largeur mais n'est coupée qu'à xDecoupe (une phrase qui s'allonge à l'écran).
 *   Un repère dont le centre n'est dans aucune zone va dans celle qu'il recouvre le plus.
 *   Zones.vers(x, y) : point du dessin d'origine → point du tableau large (dernière disposition), pour les clics.
 */
(function () {
  'use strict';
  const L_MIN = 1000, H = 420, MARGE = 8;
  let derniere = null;
  function disposer(L, spec) {
    const top = spec.top ?? 40, gap = spec.gap ?? 26, vgap = spec.vgap ?? 14, smax = spec.max ?? 1.7;
    const cols = spec.cols.map(zs => {
      const w = Math.max(...zs.map(z => z[2] - z[0])), h = zs.reduce((s, z) => s + z[3] - z[1], 0) + vgap * (zs.length - 1);
      return { zs, w, h, s: Math.min(smax, (H - top - MARGE) / h) };
    });
    const largeur = cols.reduce((s, k) => s + k.w * k.s, 0) + gap * (cols.length - 1), dispo = L - 2 * MARGE;
    const f = largeur > dispo ? dispo / largeur : 1;
    let x = (L - Math.min(largeur * f, dispo)) / 2;
    const out = [];
    for (const k of cols) {
      const s = k.s * f, hTot = k.h * s;
      let y = spec.haut ? top : top + (H - top - MARGE - hTot) / 2;
      for (const z of k.zs) {
        const dx = spec.centre === false ? x : x + (k.w - (z[2] - z[0])) * s / 2;
        out.push({ src: z, dx, dy: y, s });
        y += (z[3] - z[1]) * s + vgap * s;
      }
      x += k.w * s + gap * f;
    }
    return out;
  }
  const dedans = (z, x, y) => x >= z.src[0] && x <= z.src[2] && y >= z.src[1] && y <= z.src[3];
  const recouvre = (z, x, y, w, h) => Math.max(0, Math.min(z.src[2], x + w) - Math.max(z.src[0], x)) * Math.max(0, Math.min(z.src[3], y + h) - Math.max(z.src[1], y));
  function dessiner(c, L, spec, fn) {
    if (!spec || !(L >= L_MIN)) { derniere = null; return fn(); }
    const Z = disposer(L, spec); derniere = Z;
    const ctx = c.ctx, base = ctx.getTransform(), etat = { t: c.t, cur: c.cur, tip: c.tip, complet: c.complet };
    const repere = c.repere, vus = new Set(), orphelins = {};
    let tip = null, fin = null;
    const poser = z => { ctx.setTransform(base); ctx.translate(z.dx, z.dy); ctx.scale(z.s, z.s); ctx.translate(-z.src[0], -z.src[1]); };
    Z.forEach((z, i) => {
      Object.assign(c, etat); c.tip = null;
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
      try { fn(); } finally { c.repere = repere; ctx.restore(); }
      if (c.tip && dedans(z, c.tip[0], c.tip[1])) tip = [z.dx + (c.tip[0] - z.src[0]) * z.s, z.dy + (c.tip[1] - z.src[1]) * z.s];
      fin = { t: c.t, cur: c.cur, complet: c.complet };
    });
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
  window.Zones = { dessiner, disposer, vers, depuis, L_MIN };
})();
