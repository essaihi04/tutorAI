/*
 * LnLarge — le tableau large pour les constructions du cours « Fonctions logarithmiques » (15 novembre 2026).
 *
 * « Mieux exploiter tout le tableau, grands calibres de texte, simulations agrandies » : sur un portable (1366×613),
 * le cadre de la scène fait ~3,2 fois plus large que haut ; le cadre fixe 760 × 420 n'en remplissait que 60 %.
 * MathsTableau.page() ne transmet pas l'option `large` du kit : cette aide fait la même chose depuis la page.
 *   - `LnLarge.actif` : la fenêtre est large (rapport ≥ 2,2) au chargement → la page désactive `ajuster`
 *     (`ajuster: !LnLarge.actif`) et place ses blocs sur toute la largeur ;
 *   - `LnLarge.ouvrir(c)` au début de chaque dessin : renvoie L (760 à 1292, hauteur 420) ; les coordonnées du dessin
 *     vont alors de 0 à L (le contexte est décalé de (L − 760) / 2) ; repères et garde-fou du cadre suivent ;
 *   - `LnLarge.poignees(fn)` : enveloppe les poignées (coordonnées du dessin ↔ coordonnées du cadre du kit).
 * Grand écran (1920×1080, rapport ~1,9) : rien ne change, L = 760, `ajuster` reste en service.
 */
(function () {
  'use strict';
  const VW = 760, VH = 420, L_MAX = 1292;
  const actif = innerWidth / Math.max(1, innerHeight) >= 2.2;
  const LnLarge = {
    actif, L: VW, dx: 0,
    ouvrir(c, lmax = L_MAX) {   // lmax : jusqu’à 1596 pour une page faite pour s’étaler (bilan, carte)
      if (!actif || !c.echelle || !(c.W > 1)) { LnLarge.L = VW; LnLarge.dx = 0; return VW; }
      const L = Math.round(Math.min(lmax, Math.max(VW, c.W / c.echelle)));
      const dx = (L - VW) / 2;
      if (dx) c.ctx.translate(-dx, 0);
      c.cadre = { w: L, h: VH, haut: 0 };
      LnLarge.L = L; LnLarge.dx = dx;
      return L;
    },
    /** La plus petite taille que la craie écrit vraiment (tailleMin du kit, en unités du dessin) : à prendre pour mesurer. */
    min(c) { return c.tailleMin && c.echelle ? c.tailleMin / c.echelle : 0; },
    /** t(L) : interpole entre la valeur du cadre d'origine (L = 760) et celle du tableau large (L = 1292). */
    t(a, b) { return a + (b - a) * Math.max(0, Math.min(1, (LnLarge.L - VW) / (L_MAX - VW))); },
    /**
     * Une colonne de texte agrandie : ce que `fn` écrit autour de (x0 ; y0) est reporté en (nx ; ny), agrandi k fois
     * (textes, cadres, repères ; la pointe de la craie suit). Inactif (k = 1, rien ne bouge) hors du tableau large.
     */
    colonne(c, x0, y0, k, nx, ny, fn) {
      if (!actif || (k === 1 && nx === x0 && ny === y0)) return fn();
      const ctx = c.ctx, cadre = c.cadre, tip = c.tip;
      ctx.save(); ctx.translate(nx, ny); ctx.scale(k, k); ctx.translate(-x0, -y0);
      c.cadre = null;
      try { return fn(); } finally {
        ctx.restore(); c.cadre = cadre;
        if (c.tip && c.tip !== tip) c.tip = [nx + (c.tip[0] - x0) * k, ny + (c.tip[1] - y0) * k];
      }
    },
    /** Le titre de la vue : celui du kit, plus grand sur le tableau large. */
    titre(c, K, s) {
      if (!actif || LnLarge.L < 1000 || window.MathsTableau.titreRepete(s)) return K.titre(s);
      c.texte(s, 22, 36, { couleur: 'cyan', taille: 26, max: LnLarge.L - 40 });
      return K;
    },
    poignees(fn) {
      return (K) => (fn(K) || []).map((q) => ({ ...q, x: q.x - LnLarge.dx, bouger: (x, y) => q.bouger(x + LnLarge.dx, y) }));
    },
  };
  window.LnLarge = LnLarge;
})();
