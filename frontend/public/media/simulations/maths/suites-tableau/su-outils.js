/*
 * Petits outils communs aux constructions du cours « Suites numériques » (math_ch3_suites_numeriques), 11 novembre 2026.
 * Chargé APRÈS maths-tableau.js. Ne modifie pas le kit : il ajoute window.SU.
 *   SU.points(c, G, vals, o)      points ISOLÉS (n ; uₙ) écrits l'un après l'autre ; un point hors du cadre → flèche au bord
 *   SU.hligne(c, G, y, o)         droite horizontale (plafond, plancher, limite) avec son libellé
 *   SU.accolade(c, x, y1, y2, o)  accolade verticale (ouverte vers la gauche par défaut, o.gauche pour l'autre sens)
 *   SU.barre(c, x, y, w, o)       barre un mot écrit (trait oblique)
 *   SU.morceaux(c, x, y, liste, o) écrit une ligne en morceaux de couleurs différentes ([{t, couleur}]) ; renvoie les x
 *   SU.larg(c, s, taille)         largeur d'un texte à la craie (sans « _ », « ^ », accolades)
 *   SU.suite(u0, f, n)            [u0, f(u0), …] (n + 1 termes)
 *   SU.large(c)                   le tableau est-il large (portable 1366×613 : canvas ≈ 3,2:1) ? (15 novembre 2026)
 *   SU.Y(lg, y) / SU.H(lg, h)     une ordonnée / une hauteur du dessin d'origine, tassée quand le tableau est large
 *   SU.opt(lg, o)                 options d'un repère (y0, h) tassées
 *   SU.lignes(K, lg, x, y, l, i)  K.lignes, tassé (ordonnée, interlignes, taille × 0,9) quand le tableau est large
 *
 * Tableau large (15 novembre 2026, « grands vides à gauche et à droite, textes minuscules ») : le kit (`ajuster`) agrandit
 * la boîte de l'encre jusqu'aux bords, mais le cadre reste large de 760 : une construction de 760 × 350 est donc limitée
 * par la HAUTEUR sur un tableau de 3,2:1 et laisse 40 % de la largeur vide. Quand SU.large(c) est vrai, chaque vue se
 * dispose plus basse et plus étalée (environ 760 × 250 : figure moins haute, notes rangées à côté, interlignes serrés) :
 * le kit l'agrandit alors d'environ 1,4 et elle remplit tout le tableau. Sur un grand écran (1920×1080, ≈ 2:1), la
 * disposition d'origine reste. Quand le format change, la boîte de l'encre est remesurée (sinon l'ancienne resterait).
 */
(function () {
  'use strict';
  const nettoyer = (s) => String(s).replace(/[_^{}]/g, '');
  let dernier = null;
  const SU = {
    TASSE: .64,
    Y(lg, y) { return lg ? 46 + (y - 46) * SU.TASSE : y; },
    H(lg, h) { return lg ? h * SU.TASSE : h; },
    opt(lg, o) { return lg ? { ...o, y0: SU.Y(true, o.y0), h: o.h * SU.TASSE } : o; },
    lignes(K, lg, x, y, liste, inter = 30) {
      if (!lg) return K.lignes(x, y, liste, inter);
      return K.lignes(x, SU.Y(true, y), liste.map(l => ({ ...l, taille: (l.taille || 19) * .9, inter: l.inter != null ? l.inter * .74 : undefined })), inter * .74);
    },
    large(c) {
      const lg = c.W > 1 && c.W / Math.max(1, c.H) > 2.5;
      const sc = window.__maths && window.__maths.scene;
      if (dernier !== null && dernier !== lg && sc && !sc.mesurant) { sc.boite = null; sc.sale = true; }
      dernier = lg;
      return lg;
    },
    larg(c, s, taille = 18) { return c.largeurTexte(nettoyer(s), taille); },
    suite(u0, f, n) { const r = [u0]; for (let i = 0; i < n; i++) r.push(f(r[r.length - 1])); return r; },
    points(c, G, vals, o = {}) {
      const coul = o.couleur || 'cyan';
      let sorti = false;
      vals.forEach(([x, y], i) => {
        if (o.pas) c.pause(o.pas);
        if (!Number.isFinite(y) || y > G.ymax || y < G.ymin) {
          if (sorti || o.sansFleche) return; sorti = true;
          const haut = !(y < G.ymin), yb = haut ? G.Y(G.ymax) : G.Y(G.ymin);
          c.fleche(G.X(x), yb + (haut ? 22 : -22), G.X(x), yb + (haut ? -4 : 4), { couleur: coul, largeur: 1.8, tete: 8 });
          if (o.horsTexte) c.texte(o.horsTexte, G.X(x) + 8, yb + (haut ? 8 : -2), { couleur: coul, taille: o.taille || 15 });
          return;
        }
        c.point(G.X(x), G.Y(y), o.r || 4.5, coul);
        const e = o.etiq ? o.etiq(i, x, y) : null;
        if (e) c.texte(e, G.X(x) + (o.dx ?? 7), G.Y(y) + (o.dy ?? -9), { couleur: coul, taille: o.taille || 14 });
      });
    },
    hligne(c, G, y, o = {}) {
      const coul = o.couleur || 'orange', x0 = G.X(o.x0 ?? G.xmin), x1 = G.X(o.x1 ?? G.xmax);
      c.ligne(x0, G.Y(y), x1, G.Y(y), { couleur: coul, largeur: o.largeur || 2, pointille: o.plein ? undefined : (o.pointille || [9, 6]) });
      if (o.label) c.texte(o.label, o.lx ?? x1, G.Y(y) + (o.ly ?? -9), { couleur: coul, taille: o.taille || 15, align: o.align || 'right' });
    },
    accolade(c, x, y1, y2, o = {}) {
      const s = o.gauche ? -1 : 1, m = (y1 + y2) / 2, e = 9 * s;
      c.trait([[x, y1], [x + e, y1 + 8], [x + e, m - 8], [x + 2 * e, m], [x + e, m + 8], [x + e, y2 - 8], [x, y2]], { couleur: o.couleur || 'jaune', largeur: o.largeur || 2, tremble: .4 });
    },
    barre(c, x, y, w, o = {}) { c.ligne(x - 3, y + 2, x + w + 3, y - 14, { couleur: o.couleur || 'rouge', largeur: o.largeur || 2.4 }); },
    morceaux(c, x, y, liste, o = {}) {
      const xs = [];
      for (const m of liste) {
        xs.push(x);
        c.texte(m.t, x, y, { couleur: m.couleur || 'blanc', taille: o.taille || 19 });
        x += SU.larg(c, m.t, o.taille || 19);
      }
      xs.push(x);
      return xs;
    },
  };
  window.SU = SU;
})();
