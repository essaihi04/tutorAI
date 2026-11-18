/*
 * Outils communs aux constructions du cours « Limites et continuité » (math_ch1_limites_continuite), 10 novembre 2026.
 * Chargé après maths-tableau.js. Ne modifie pas le kit : il ajoute ce qui manquait à ce chapitre.
 *   LC.limite(c, x, y, sous, suite, o)   « lim » avec, dessous en petit, « x → a » ; puis la suite ; renvoie le x de fin
 *   LC.temps(c)                          instant d'écriture courant (Infinity quand la construction est écrite d'un coup)
 *   LC.piste(t, [[t0, duree, de, a], …]) valeur animée au temps t (null avant le premier segment) ; ease en cosinus
 *   LC.tabVar(c, x, y, w, nom, xs, vals, o)  tableau de variations à la craie (vals : [[texte, 'h'|'b'], …])
 *   LC.boite(c, x, y, w, h, texte, o)    une « machine » : cadre arrondi et texte centré
 *   LC.segment(c, G, a, b, o)            un intervalle en trait épais sur l'axe des abscisses (o.vertical : sur l'axe des ordonnées)
 */
(function () {
  'use strict';
  const LC = {};
  LC.temps = (c) => (Number.isFinite(c.t) ? c.t : Infinity);
  LC.piste = (t, segs) => {
    let v = null;
    for (const [t0, d, de, a] of segs) {
      if (t < t0) break;
      const p = d > 0 ? Math.min(1, (t - t0) / d) : 1, e = (1 - Math.cos(Math.PI * p)) / 2;
      v = de + (a - de) * e;
    }
    return v;
  };
  LC.limite = function (c, x, y, sous, suite, o = {}) {
    const t = o.taille || 19, ts = Math.max(11, Math.round(t * 0.62)), coul = o.couleur || 'blanc';
    // tailles vraiment écrites (plancher du petit tableau) : « x → a » reste SOUS « lim », sans le toucher
    const te = window.MathsTableau.tailleEcrite(c, t), tse = window.MathsTableau.tailleEcrite(c, ts);
    c.texte('lim', x, y, { couleur: coul, taille: t, duree: o.duree });
    const wl = c.largeurTexte('lim', te), ws = c.largeurTexte(sous.replace(/[_^{}]/g, ''), tse);
    c.texte(sous, x + wl / 2, y + Math.max(t * 0.8, te * .3 + tse * .95), { couleur: coul, taille: ts, align: 'center', duree: .2 });
    const x2 = x + wl / 2 + Math.max(wl / 2, ws / 2) + 7;
    if (suite) c.texte(suite, x2, y, { couleur: coul, taille: t, max: o.max, duree: o.duree });
    return x2 + (suite ? c.largeurTexte(suite.replace(/[_^{}]/g, ''), te) : 0);
  };
  LC.tabVar = function (c, x, y, w, nom, xs, vals, o = {}) {
    const h1 = o.h1 || 28, h2 = o.h2 || 64, g = o.gauche || 50, coul = o.couleur || 'cyan', tl = o.taille || 15;
    c.rect(x, y, w, h1 + h2, { couleur: 'faible', arrondi: 4, largeur: 1.4 });
    c.ligne(x, y + h1, x + w, y + h1, { couleur: 'faible', largeur: 1.2 });
    c.ligne(x + g, y, x + g, y + h1 + h2, { couleur: 'faible', largeur: 1.2 });
    c.texte('x', x + g / 2, y + 19, { couleur: 'faible', taille: tl, align: 'center' });
    c.texte(nom, x + g / 2, y + h1 + h2 / 2 + 6, { couleur: 'faible', taille: tl, align: 'center' });
    const n = xs.length, pas = (w - g - 34) / Math.max(1, n - 1), X = (i) => x + g + 17 + i * pas;
    const Y = (p) => (p === 'h' ? y + h1 + 20 : y + h1 + h2 - 8);
    xs.forEach((s, i) => c.texte(s, X(i), y + 19, { couleur: 'blanc', taille: tl, align: 'center' }));
    vals.forEach((v, i) => {
      c.texte(v[0], X(i), Y(v[1]), { couleur: coul, taille: tl, align: 'center' });
      if (i < n - 1) {
        const a = vals[i][1], b = vals[i + 1][1];
        const ya = a === 'h' ? Y('h') + 4 : Y('b') - 14, yb = b === 'h' ? Y('h') + 4 : Y('b') - 14;
        c.fleche(X(i) + 18, ya, X(i + 1) - 18, yb, { couleur: coul, largeur: 1.6, tete: 8 });
      }
    });
    return { X, Y, h: h1 + h2 };
  };
  LC.boite = function (c, x, y, w, h, texte, o = {}) {
    c.rect(x, y, w, h, { couleur: o.couleur || 'cyan', arrondi: 10, largeur: 2 });
    c.texte(texte, x + w / 2, y + h / 2 + 7, { couleur: o.couleurTexte || 'blanc', taille: o.taille || 19, align: 'center', max: w - 10 });
  };
  LC.segment = function (c, G, a, b, o = {}) {
    const coul = o.couleur || 'jaune', l = o.largeur || 6;
    if (o.vertical) { const x = G.X(Math.min(Math.max(0, G.xmin), G.xmax)); c.ligne(x, G.Y(a), x, G.Y(b), { couleur: coul, largeur: l, alpha: o.alpha ?? .75, duree: o.duree }); }
    else { const y = G.Y(Math.min(Math.max(0, G.ymin), G.ymax)); c.ligne(G.X(a), y, G.X(b), y, { couleur: coul, largeur: l, alpha: o.alpha ?? .75, duree: o.duree }); }
  };
  /* Tableau large (15 novembre 2026, « grands vides à gauche et à droite, textes minuscules ») : sur un tableau en
   * bandeau (portable 1366 × 613), le cadre prend la largeur du tableau, L de 760 à 1596 (même formule que le kit,
   * option `large` de Scene). LC.L(c) donne L à tout moment, mesure comprise ; K.large = L ≥ 1000. Les pages placent la
   * figure plus large et la colonne de texte plus à droite avec `LC.e(K)` = L − 760 (0 sur un tableau haut : la
   * disposition d'origine, déjà bonne en 1920 × 1080), et écrivent plus gros avec `LC.t(K, taille)`. */
  LC.L = (c) => Math.round(Math.min(760 * 2.1, Math.max(760, 420 * c.W / Math.max(1, c.H))));
  LC.e = (K) => { const L = LC.L(K.c); return L >= 1000 ? L - 760 : 0; };
  LC.t = (K, t) => (LC.L(K.c) >= 1000 ? Math.round(t * 1.35) : t);
  /* Disposition type « figure à gauche, texte à droite » : la figure prend 60 % de la largeur gagnée, la colonne de
   * texte se décale de 67 % (elle garde ~450 de large pour un texte 1,35 fois plus gros). */
  /* Disposition type « schéma sur toute la largeur » : les abscisses et les largeurs × k = L / 760 (1 sur un tableau haut). */
  LC.k = (K) => { const L = LC.L(K.c); return L >= 1000 ? L / 760 : 1; };
  LC.gw = (K, w) => w + LC.e(K) * 0.6;
  LC.col = (K, x) => x + LC.e(K) * 0.67;
  /* L'aide K, élargie : titre plus gros, lignes de calcul plus grosses (et sans la largeur max de 760), graduations des
   * axes plus grosses ; tout le reste du kit inchangé. */
  LC.etendre = function (c, K) {
    const L = LC.L(c), large = L >= 1000;
    K.L = L; K.large = large;
    if (!large) return K;
    K.titre = (s) => { if (window.MathsTableau.titreRepete(s)) { c.pause(window.MathsTableau.tempsTitre(s)); return K; } c.texte(s, 20, 34, { couleur: 'cyan', taille: 26, max: L - 40 }); return K; };
    K.lignes = (x, y, liste, inter = 30) => {
      for (const l of liste) {
        const t = Math.round((l.taille || 19) * 1.45);
        if (l.pause) c.pause(l.pause);
        if (l.t) c.texte(l.t, x + (l.dx || 0), y, { couleur: l.couleur || 'blanc', taille: t, max: l.max ? l.max * 1.45 : (L - x - 16) });
        if (l.cadre) { const w = Math.min(L - x - 8, c.largeurTexte(l.t, t) + 16); c.rect(x + (l.dx || 0) - 8, y - t - 2, w, t + 12, { couleur: l.cadre, arrondi: 6, largeur: 1.4 }); }
        if (l.repere) c.repere(l.repere, x + (l.dx || 0) - 4, y - t - 3, Math.min(L - x - 10, c.largeurTexte(l.t || '', t) + 10), t * 1.55, l.label || l.t);
        if (l.moment) K.marque(l.moment);
        y += (l.inter ?? inter) * 1.15;
      }
      return y;
    };
    const axes = K.axes;
    K.axes = (o) => {
      const texte = c.texte;
      c.texte = function (s, x, y, oo = {}) { return texte.call(this, s, x, y, { ...oo, taille: Math.round((oo.taille || 18) * 1.25) }); };
      try { return axes(o); } finally { c.texte = texte; }
    };
    return K;
  };
  /* MathsTableau.page avec le tableau large (le kit transmet `def.large` à sa Scene) et l'aide K élargie. */
  LC.page = function (def) {
    for (const V of Object.values(def.vues)) {
      const d = V.dessiner;
      if (d) V.dessiner = function (c, K) { LC.etendre(c, K); return d.call(this, c, K); };
    }
    return window.MathsTableau.page({ ...def, large: true });
  };
  window.LC = LC;
})();
