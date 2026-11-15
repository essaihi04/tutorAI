/*
 * Tableau large (15 novembre 2026, « mieux exploiter tout le tableau, grands calibres de texte, simulations agrandies ») :
 * quand le cadre prend le format du tableau (Scene(..., { large: true }), scene.L ≥ SEUIL, portable 1366 × 613), chaque page
 * à déroulé se dispose en deux parties :
 *   - à GAUCHE, une colonne d'écriture : les phrases écrites au fil du déroulé (coupées à la ligne, plusieurs étapes gardées) ;
 *   - au CENTRE et à DROITE, la figure de la vue (`src` = sa boîte dans le dessin d'origine 760 × 420) agrandie pour remplir
 *     toute la hauteur et le reste de la largeur.
 * Deuxième passe (« agrandir les figures elles-mêmes ») : les tailles sont choisies en pixels À L'ÉCRAN (u(px) = px / scene.s) :
 * l'écriture de la colonne va de 22 à 18 px (la plus grande qui laisse tenir toutes les étapes de la vue), le titre interne est
 * retiré (le titre de la diapositive le dit déjà), et dans la figure agrandie aucun texte ne descend sous 17 px à l'écran
 * (craie.echelle = échelle réelle de la figure). La figure est dessinée avec une transformation du contexte : les repères
 * pointés par le professeur (craie.repere lit la transformation courante) suivent tout seuls. Sous SEUIL (grand écran
 * 1920 × 1080, déjà haut), rien ne change.
 */
(function () {
  'use strict';
  const SEUIL = 1000, VH = 420, MARGE = 10, PX_FIG = 17;
  let G = null;     // la disposition de l'image en cours (null : disposition d'origine)
  let D = null;     // disposition d'origine dans un cadre un peu plus large que 760 : le dessin est centré (décalage en x)
  let DERNIER = { tx: 0, ty: 0, k: 1 };   // transformation de la figure à la dernière image (pour les glisser de la page)

  /** Coupe `s` en lignes de largeur ≤ max (mesure : mesurer(s) en unités du dessin). */
  function couper(s, max, mesurer) {
    const mots = String(s).replace(/ ([=≈×→⇌<>≤≥:;]) /g, ' $1 ').replace(/(\d) (?=(mmol|mol|min|mL|L|s|h|K|°C|e⁻)\b)/g, '$1 ').split(' '), out = []; let ligne = '';
    for (const m of mots) { const essai = ligne ? ligne + ' ' + m : m; if (ligne && mesurer(essai) > max) { out.push(ligne); ligne = m; } else ligne = essai; }
    if (ligne) out.push(ligne);
    return out.map(l => l.replace(/ /g, ' '));
  }

  /**
   * Début de l'image (après scene.cadre) : o.src = [x0, y0, x1, y1] (boîte de la figure, sans titre ni zone d'écriture),
   * o.part (part maxi de la largeur pour la figure), o.colMin (largeur mini de la colonne en px écran, défaut 300 ; 0 : pas de colonne),
   * o.kMax (agrandissement maxi, défaut 3), o.ecrire(c, s, x, y, opts) (écriture chimique de la page), o.basCol (bas de la colonne).
   */
  function debut(c, scene, o = {}) {
    G = null; D = null;
    const L = scene.L || 760;
    if (L < SEUIL || !o.src) {
      DERNIER = { tx: 0, ty: 0, k: 1 };
      if (L > 760) { D = (L - 760) / 2; c.ctx.save(); c.ctx.translate(D, 0); DERNIER.tx = D; }
      return null;
    }
    const s = c.echelle || scene.s || 1, u = px => px / s;
    const [x0, y0, x1, y1] = o.src, w = x1 - x0, h = y1 - y0;
    // La figure : toute la hauteur (au plus o.part de la largeur) ; la colonne garde au moins colMin px à l'écran.
    // Sans colonne (o.colMin = 0 : la page n'y écrit rien), la figure est centrée.
    const colMin = u(o.colMin ?? 300), k = Math.min(o.kMax ?? 3, (VH - 2 * MARGE) / h, (L - colMin - 3 * MARGE) / w, o.part ? L * o.part / w : Infinity);
    const col = L - w * k - 3 * MARGE;
    const tx = (o.colMin === 0 ? (L - w * k) / 2 : col + 2 * MARGE) - x0 * k, ty = (VH - h * k) / 2 - y0 * k;
    const ctx = c.ctx, base = ctx.getTransform();
    G = { c, L, s, u, col, k, tx, ty, base, y: 0, bas: o.basCol ?? VH - MARGE, px: 20, taille: u(20), ecrire: o.ecrire || ((cc, t, x, y, op) => cc.texte(t, x, y, op)),
      echelle: c.echelle, tailleMin: c.tailleMin };
    ctx.save(); ctx.translate(tx, ty); ctx.scale(k, k);
    figure(c, k);
    DERNIER = { tx, ty, k };
    G.y = u(12);
    return G;
  }
  /** Dans la figure agrandie : la craie connaît sa vraie échelle, aucun texte sous PX_FIG px à l'écran. */
  function figure(c, k) { if (G.echelle) { c.echelle = G.echelle * k; c.tailleMin = Math.max(G.tailleMin || 0, PX_FIG); } }
  /** Fin de l'image : le contexte revient au cadre ; le bout de craie est ramené dans le repère du cadre. */
  function fin(c) {
    if (D != null) { if (c.tip) c.tip = [c.tip[0] + D, c.tip[1]]; c.ctx.restore(); D = null; }
    if (!G) return;
    if (c.tip) c.tip = [G.tx + G.k * c.tip[0], G.ty + G.k * c.tip[1]];
    c.echelle = G.echelle; c.tailleMin = G.tailleMin;
    c.ctx.restore(); G = null;
  }
  /** Exécute fn dans la colonne de gauche (repère du cadre, sans l'agrandissement de la figure). */
  function colonne(fn) {
    const c = G.c, ctx = c.ctx, avant = c.tip, e = c.echelle, m = c.tailleMin; c.tip = null;
    ctx.save(); ctx.setTransform(G.base); c.echelle = G.echelle; c.tailleMin = G.tailleMin;
    try { fn(); } finally {
      ctx.restore(); c.echelle = e; c.tailleMin = m;
      c.tip = c.tip ? [(c.tip[0] - G.tx) / G.k, (c.tip[1] - G.ty) / G.k] : avant;
    }
  }
  const mesureur = (c, taille) => s => { c.ctx.font = `${taille}px ${window.Tableau.POLICE}`; return c.ctx.measureText(String(s).replace(/[_{}^]/g, '')).width; };
  /** Le titre de la vue : retiré sur le tableau large (le titre de la diapositive le dit déjà). */
  function titre(c, s, x, y, o = {}) {
    if (!G) return c.texte(s, x, y, o);
  }
  /**
   * Zone d'écriture dans la colonne : `liste` comme zoneEcriture ; `k` = index de la dernière étape écrite ; `etape(e, fnLignes)`
   * enveloppe l'écriture de l'étape (M.etape de la page, avec e.plus dans la figure). La taille (22 → 18 px à l'écran) est la
   * plus grande où TOUTES les étapes de la vue tiennent (elle ne change pas au fil du déroulé) ; sinon 18 px et on garde les
   * dernières étapes qui tiennent. Renvoie les textes visibles.
   */
  function zone(c, liste, k, etape, cache) {
    const max = G.col - 6, dispo = G.bas - G.y;
    let choix = null;
    for (const px of [22, 21, 20, 19, 18]) {
      const t = G.u(px), pas = t * 1.24, ecart = G.u(8), mes = mesureur(c, t);
      const blocs = liste.map(e => e.lignes.map(([s, col]) => [couper(s, max, mes), col]));
      const hauteur = j => blocs[j].reduce((a, [ls]) => a + ls.length * pas, 0) + ecart;
      choix = { t, pas, ecart, blocs, hauteur };
      if (blocs.reduce((a, _, j) => a + hauteur(j), 0) - ecart - pas + t <= dispo) break;
    }
    const { t, pas, ecart, blocs, hauteur } = choix;
    G.taille = t;
    const garde = new Set();
    let h = 0;
    for (let j = k; j >= 0; j--) { const hj = hauteur(j); if (h + hj - ecart - pas + t > dispo && garde.size) break; garde.add(j); h += hj; }
    let y = G.y + t * .9; const vues = [];
    liste.forEach((e, j) => {
      if (j > k) return;
      etape(e, () => {
        if (garde.has(j)) colonne(() => {
          for (const [ls, col] of blocs[j]) for (const l of ls) { G.ecrire(c, l, MARGE, y, { couleur: col, taille: t, alpha: cache && cache(e.nom) ? 0 : undefined }); y += pas; }
          y += ecart;
        });
        if (garde.has(j)) vues.push(...e.lignes.map(l => l[0]));
      });
    });
    return vues;
  }
  /** Taille à l'écran d'une phrase de la colonne (o.px, ou o.taille de l'ancien dessin ramenée entre 18 et 22 px). */
  const pxDe = o => o.px ?? Math.min(22, Math.max(18, o.taille ?? 20));
  /** Une phrase écrite dans la colonne, sous ce qui y est déjà ; rend sa boîte [x, y, w, h] (repère du cadre). */
  function phrase(c, s, o = {}) {
    const t = G.u(pxDe(o)), ls = couper(s, G.col - 6, mesureur(c, t)), y0 = G.y;
    colonne(() => { for (const l of ls) { G.y += t; G.ecrire(c, l, MARGE, G.y, { ...o, taille: t }); G.y += t * .24; } G.y += G.u(8); });
    return [MARGE - 4, y0, G.col + 4, G.y - y0];
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
    const [x0, y0, x1, y1] = src, w = x1 - x0, h = y1 - y0, haut = G.bas - G.y, larg = G.col;
    const k = Math.max(.4, Math.min(kMax, larg / w, haut / h)), dx = MARGE + (larg - w * k) / 2 - x0 * k, dy = G.y - y0 * k;
    colonne(() => {
      const ctx = c.ctx, avant = c.tip; c.tip = null; ctx.save(); ctx.translate(dx, dy); ctx.scale(k, k);
      if (G.echelle) { c.echelle = G.echelle * k; c.tailleMin = Math.max(G.tailleMin || 0, PX_FIG); }
      try { fn(); } finally { ctx.restore(); c.tip = c.tip ? [dx + k * c.tip[0], dy + k * c.tip[1]] : avant; }
    });
  }
  window.TLRLarge = { local, phrase, groupe, repere, debut, fin, colonne, titre, zone, couper, actif: () => !!G, get G() { return G; } };
})();
