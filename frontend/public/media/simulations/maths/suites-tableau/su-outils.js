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
 */
(function () {
  'use strict';
  const nettoyer = (s) => String(s).replace(/[_^{}]/g, '');
  const SU = {
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
