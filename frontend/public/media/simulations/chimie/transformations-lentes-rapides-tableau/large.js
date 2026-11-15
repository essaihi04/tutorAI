/*
 * Tableau large (15 novembre 2026, « mieux exploiter tout le tableau, grands calibres de texte, simulations agrandies ») :
 * quand le cadre prend le format du tableau (Scene(..., { large: true }), scene.L ≥ SEUIL, portable 1366 × 613), chaque page
 * à déroulé se dispose en deux parties :
 *   - à GAUCHE, une colonne d'écriture : le titre, puis les phrases écrites au fil du déroulé (coupées à la ligne, plus grandes,
 *     plusieurs étapes gardées au tableau) ;
 *   - au CENTRE et à DROITE, la figure de la vue (`src` = sa boîte dans le dessin d'origine 760 × 420) agrandie pour remplir
 *     toute la hauteur et le reste de la largeur.
 * La figure est dessinée avec une transformation du contexte : les repères pointés par le professeur (craie.repere lit la
 * transformation courante) suivent tout seuls. Sous SEUIL (grand écran 1920 × 1080, déjà haut), rien ne change.
 */
(function () {
  'use strict';
  const SEUIL = 1000, VH = 420, MARGE = 10;
  let G = null;     // la disposition de l'image en cours (null : disposition d'origine)
  let D = null;     // disposition d'origine dans un cadre un peu plus large que 760 : le dessin est centré (décalage en x)
  let DERNIER = { tx: 0, ty: 0, k: 1 };   // transformation de la figure à la dernière image (pour les glisser de la page)

  /** Coupe `s` en lignes de largeur ≤ max (mesure : mesurer(s) en unités du dessin). */
  function couper(s, max, mesurer) {
    const mots = String(s).split(' '), out = []; let ligne = '';
    for (const m of mots) { const essai = ligne ? ligne + ' ' + m : m; if (ligne && mesurer(essai) > max) { out.push(ligne); ligne = m; } else ligne = essai; }
    if (ligne) out.push(ligne);
    return out;
  }

  /**
   * Début de l'image (après scene.cadre) : o.src = [x0, y0, x1, y1] (boîte de la figure, sans titre ni zone d'écriture),
   * o.col (largeur mini de la colonne, défaut 330), o.kMax (agrandissement maxi, défaut 1.7), o.ecrire(c, s, x, y, opts)
   * (écriture chimique de la page), o.taille (phrases, défaut 21), o.titre (taille du titre, défaut 24).
   */
  function debut(c, scene, o = {}) {
    G = null; D = null;
    const L = scene.L || 760;
    if (L < SEUIL || !o.src) {
      DERNIER = { tx: 0, ty: 0, k: 1 };
      if (L > 760) { D = (L - 760) / 2; c.ctx.save(); c.ctx.translate(D, 0); DERNIER.tx = D; }
      return null;
    }
    const [x0, y0, x1, y1] = o.src, w = x1 - x0, h = y1 - y0, kMax = o.kMax ?? 1.9;
    const kH = Math.min(kMax, (VH - 2 * MARGE) / h);
    // La colonne prend ce que la figure, à pleine hauteur, laisse libre (bornée).
    let col = Math.max(o.col ?? 330, Math.min(o.colMax ?? Math.max(460, L * .32), L - w * kH - 2 * MARGE));
    const k = Math.min(kH, (L - col - 2 * MARGE) / w);
    const tx = col + ((L - col) - w * k) / 2 - x0 * k, ty = (VH - h * k) / 2 - y0 * k;
    const ctx = c.ctx, base = ctx.getTransform();
    G = { c, L, col, k, tx, ty, base, y: 0, bas: o.basCol ?? VH - MARGE, taille: o.taille ?? 22, tTitre: o.titre ?? 26, ecrire: o.ecrire || ((cc, s, x, y, op) => cc.texte(s, x, y, op)) };
    ctx.save(); ctx.translate(tx, ty); ctx.scale(k, k);
    DERNIER = { tx, ty, k };
    G.y = 34;
    return G;
  }
  /** Fin de l'image : le contexte revient au cadre ; le bout de craie est ramené dans le repère du cadre. */
  function fin(c) {
    if (D != null) { if (c.tip) c.tip = [c.tip[0] + D, c.tip[1]]; c.ctx.restore(); D = null; }
    if (!G) return;
    if (c.tip) c.tip = [G.tx + G.k * c.tip[0], G.ty + G.k * c.tip[1]];
    c.ctx.restore(); G = null;
  }
  /** Exécute fn dans la colonne de gauche (repère du cadre, sans l'agrandissement de la figure). */
  function colonne(fn) {
    const c = G.c, ctx = c.ctx, avant = c.tip; c.tip = null;
    ctx.save(); ctx.setTransform(G.base);
    try { fn(); } finally {
      ctx.restore();
      c.tip = c.tip ? [(c.tip[0] - G.tx) / G.k, (c.tip[1] - G.ty) / G.k] : avant;
    }
  }
  /** Taille vraiment écrite (le kit ne descend pas sous tailleMin px à l'écran). */
  const eff = (c, t) => (c.echelle >= .3 && c.tailleMin ? Math.max(t, c.tailleMin / c.echelle) : t);
  const mesureur = (c, taille) => s => { c.ctx.font = `${taille}px ${window.Tableau.POLICE}`; return c.ctx.measureText(String(s).replace(/[_{}^]/g, '')).width; };
  /** Le titre de la vue, en haut de la colonne (coupé à la ligne). */
  function titre(c, s, x, y, o = {}) {
    if (!G) return c.texte(s, x, y, o);
    const t = eff(c, G.tTitre), max = G.col - 24;
    colonne(() => {
      for (const l of couper(s, max, mesureur(c, t))) { G.ecrire(c, l, 16, G.y, { ...o, taille: t, max: undefined }); G.y += t * 1.25; }
      G.y += 14;
    });
  }
  /**
   * Zone d'écriture dans la colonne : `liste` comme zoneEcriture ; `k` = index de la dernière étape écrite ; `etape(e, fnLignes)`
   * enveloppe l'écriture de l'étape (M.etape de la page, avec e.plus dans la figure). On garde les dernières étapes qui tiennent.
   * Renvoie les textes visibles.
   */
  function zone(c, liste, k, etape, cache) {
    const t = eff(c, G.taille), pas = t * 1.3, max = G.col - 26, mes = mesureur(c, t);
    const blocs = liste.map(e => e.lignes.map(([s, col]) => [couper(s, max, mes), col]));
    const hauteur = j => blocs[j].reduce((a, [ls]) => a + ls.length * pas, 0) + 8;
    const dispo = G.bas - G.y + t * .9, garde = new Set();
    let h = 0;
    for (let j = k; j >= 0; j--) { const hj = hauteur(j); if (h + hj > dispo) break; garde.add(j); h += hj; }
    let y = G.y; const vues = [];
    liste.forEach((e, j) => {
      if (j > k) return;
      etape(e, () => {
        if (garde.has(j)) colonne(() => {
          for (const [ls, col] of blocs[j]) for (const l of ls) { G.ecrire(c, l, 16, y, { couleur: col, taille: t, alpha: cache && cache(e.nom) ? 0 : undefined }); y += pas; }
          y += 8;
        });
        if (garde.has(j)) vues.push(...e.lignes.map(l => l[0]));
      });
    });
    return vues;
  }
  /** Une phrase écrite dans la colonne, sous ce qui y est déjà ; rend sa boîte [x, y, w, h] (repère du cadre). */
  function phrase(c, s, o = {}) {
    const t = eff(c, o.taille ?? G.taille), ls = couper(s, G.col - 26, mesureur(c, t)), y0 = G.y;
    colonne(() => { for (const l of ls) { G.ecrire(c, l, 16, G.y, { ...o, taille: t }); G.y += t * 1.3; } G.y += 8; });
    return [10, y0 - t, G.col - 14, G.y - y0];
  }
  /** Repère d'une boîte de la colonne (repère du cadre). */
  function repere(c, id, b, label) { colonne(() => c.repere(id, b[0], b[1], b[2], b[3], label)); }
  /** Coordonnées CSS du canvas → coordonnées du dessin d'origine de la figure (scene.local puis la transformation de la figure). */
  function local(scene, px, py) { const [x, y] = scene.local(px, py); return [(x - DERNIER.tx) / DERNIER.k, (y - DERNIER.ty) / DERNIER.k]; }
  /**
   * Dessine fn dans la colonne, sous ce qui y est écrit : la boîte `src` du dessin d'origine est agrandie (sans dépasser kMax)
   * pour tenir dans la largeur de la colonne et la hauteur qui reste (jusqu'à G.bas). Les repères posés dans fn suivent.
   */
  function groupe(c, src, fn, kMax = 1.6) {
    const [x0, y0, x1, y1] = src, w = x1 - x0, h = y1 - y0, haut = G.bas - G.y, larg = G.col - 24;
    const k = Math.max(.4, Math.min(kMax, larg / w, haut / h)), dx = 12 + (larg - w * k) / 2 - x0 * k, dy = G.y - y0 * k;
    colonne(() => {
      const ctx = c.ctx, avant = c.tip; c.tip = null; ctx.save(); ctx.translate(dx, dy); ctx.scale(k, k);
      try { fn(); } finally { ctx.restore(); c.tip = c.tip ? [dx + k * c.tip[0], dy + k * c.tip[1]] : avant; }
    });
  }
  window.TLRLarge = { local, phrase, groupe, repere, debut, fin, colonne, titre, zone, couper, actif: () => !!G, get G() { return G; } };
})();
