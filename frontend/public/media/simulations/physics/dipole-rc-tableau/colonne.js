/*
 * Tableau large (15 novembre 2026, « la simulation n’occupe qu’une bande étroite, les textes sont minuscules ») :
 * la page passe en Scene(canvas, dessiner, { large: true }) et appelle RCColonne.debut(c) juste après scene.cadre().
 *  - tableau large (scene.L ≥ 1000, portable 1366 × 613) : les phrases du déroulé, écrites en bas du dessin, passent
 *    dans une colonne à GAUCHE, coupées à la ligne ; le dessin (montage, graphe) se décale à droite et s’agrandit pour
 *    occuper toute la hauteur (zoom = ce que permet la place gagnée en bas) ;
 *  - grand écran (L < 1000) : disposition d’origine, centrée dans le cadre.
 * Les repères suivent (transformation du dessin ; ceux d’une phrase passée dans la colonne prennent sa place) et
 * scene.local() rend toujours les coordonnées d’origine (poignées).
 * Options : boite (zone du dessin gardée, coordonnées d’origine) { x0, y0, x1, y1 } ; colonne (largeur, défaut 270) ;
 * versColonne(s, x, y, o) → la phrase passe-t-elle dans la colonne ? ; agrandir (taille des phrases, défaut 1.08).
 * Une phrase écrite avec { encadre: couleur } garde son cadre dans la colonne (la page ne dessine alors pas le sien : COL.k.st.on).
 */
(function () {
  'use strict';
  const VW = 760, VH = 420, L_MIN = 1000;
  function RCColonne(scene, opt) {
    const craie = scene.craie, texte = craie.texte, repere = craie.repere;
    const st = { on: false, z: 1, mx: 0, my: 0, dx: 0, dy: 0, ycol: 0, liste: [], o: opt, b: null };
    /** Coupe une phrase en lignes de largeur ≤ max (aux espaces ; indices et exposants comptés plus petits). */
    function largeur(c, s, t) {
      const seg = window.Tableau.Craie.segments(String(s));
      return seg.reduce((w, g) => w + c.largeurTexte(g.t, g.sub || g.sup ? t * .62 : t), 0);
    }
    function couper(c, s, t, max) {
      const mots = String(s).split(' '), out = []; let l = '';
      for (const m of mots) { const e = l ? l + ' ' + m : m; if (l && largeur(c, e, t) > max) { out.push(l); l = m; } else l = e; }
      if (l) out.push(l);
      return out;
    }
    craie.texte = function (s, x, y, o = {}) {
      const O = st.o;
      if (!st.on || !O.versColonne(String(s), x, y, o)) return texte.call(this, s, x, y, o);
      const t = (o.taille ?? 18) * (O.agrandir ?? 1.08), cw = (O.colonne ?? 270) - 22;
      const lignes = couper(this, s, t, cw), x0 = st.b.x0 - (O.colonne ?? 270) + 6, y0 = st.ycol;
      const o2 = { ...o, taille: t, align: 'left' }; delete o2.max; delete o2.encadre;
      if (o.encadre) st.ycol += 6;
      for (const l of lignes) { st.ycol += t * 1.22; texte.call(this, l, x0, st.ycol, o2); }
      // { encadre: couleur } : le résultat garde son cadre dans la colonne.
      if (o.encadre) { const w = Math.max(...lignes.map(l => largeur(this, l, t))); this.rect(x0 - 7, y0 + 6 + t * .1, w + 14, st.ycol - y0 - 6 + t * .3, { couleur: o.encadre, largeur: 1.4, arrondi: 8 }); st.ycol += 6; }
      st.liste.push({ y, rect: { x: x0 - 4, y: y0 + t * .2, w: cw + 8, h: st.ycol - y0 + t * .2 } });
      st.ycol += t * .5;
      return this;
    };
    craie.repere = function (id, x, y, w, h, label) {
      if (st.on && y + h / 2 >= st.b.y1 - 10) {
        const l = st.liste.filter(e => e.y >= y - 6 && e.y <= y + h + 30);
        if (l.length) {
          const x0 = Math.min(...l.map(e => e.rect.x)), y0 = Math.min(...l.map(e => e.rect.y));
          const x1 = Math.max(...l.map(e => e.rect.x + e.rect.w)), y1 = Math.max(...l.map(e => e.rect.y + e.rect.h));
          return repere.call(this, id, x0, y0, x1 - x0, y1 - y0, label);
        }
      }
      return repere.call(this, id, x, y, w, h, label);
    };
    const local = scene.local;
    scene.local = function (px, py) {
      const [a, b] = local.call(scene, px, py);
      return [(a - st.mx) / st.z + st.dx, (b - st.my) / st.z + st.dy];
    };
    return {
      st,
      /** À appeler juste après scene.cadre() : pose la transformation de l’image (colonne ou centrage). */
      debut(c) {
        const O = st.o, L = scene.L || VW;
        st.liste = [];
        st.on = L >= L_MIN && (!O.actif || O.actif());
        if (!st.on) {                                   // grand écran : dessin d’origine, centré dans le cadre large
          st.z = 1; st.mx = (L - VW) / 2; st.my = 0; st.dx = 0; st.dy = 0;
          c.ctx.translate(st.mx, 0);
          return;
        }
        const b = st.b = typeof O.boite === 'function' ? O.boite() : O.boite, cw = O.colonne ?? 270;
        const w = cw + (b.x1 - b.x0), h = b.y1 - b.y0;
        st.z = Math.min(L / w, VH / h, O.zoomMax ?? 1.6);
        st.mx = (L - w * st.z) / 2 + cw * st.z; st.my = (VH - h * st.z) / 2;
        st.dx = b.x0; st.dy = b.y0;
        c.ctx.translate(st.mx, st.my); c.ctx.scale(st.z, st.z); c.ctx.translate(-b.x0, -b.y0);
        if (c.echelle) c.echelle *= st.z;
        c.cadre = null;
        st.ycol = b.y0 + (O.hautColonne ?? 30);
      },
    };
  }
  window.RCColonne = RCColonne;
})();
