/*
 * MathsCompte — compter ou parcourir en allumant, un élément à la fois (18-19 novembre 2026).
 *
 * Règle 16 de la skill simulations-au-tableau et règle 44 de la skill professeur : quand l'élève doit compter ou
 * parcourir (termes d'une suite, points, arbres, traversées de l'axe, lignes d'un tableau, pas d'un angle…), chaque élément
 * s'ALLUME à son tour — un anneau lumineux de sa couleur, un léger fond, et son numéro courant « 1, 2, 3… » écrit proprement
 * dans une pastille — et reste allumé ; le total s'écrit une fois, à la fin. Jamais de chiffres griffonnés, jamais tout
 * d'un coup. Chaque élément est un MOMENT nommé (`<prefixe>_1`, `<prefixe>_2`…, puis `<prefixe>_total`) et un REPÈRE
 * (même nom) : le tuteur s'arrête dessus (`play_until`), le montre (`highlight` / `allume`) et rejoue le compte.
 *
 * Chargement : après maths-tableau.js →  <script src="/media/simulations/maths/commun/compter.js"></script>
 *
 *   MathsCompte.compter(c, K, elements, options)
 *     elements : [{ x, y, r } (un rond)  |  { x, y, w, h } (un rectangle, x/y = coin haut gauche) , libelle?, n? (numéro
 *                imposé, ex. 2022 pour le dernier après « ⋮ »), pos?, bx?/by? (pastille à cet endroit) ]
 *                en coordonnées du dessin (celles de c.cercle / c.rect)
 *     options  : { prefixe: 'compte', couleur: 'jaune', pas: .45 (s entre deux éléments), pos: 'haut'|'bas'|'droite'|'gauche',
 *                  numero: true, total: { t: '3 arbres', x, y, taille, couleur } }
 *   → renvoie la liste des noms de moments.
 */
(function () {
  'use strict';
  const MT = () => window.MathsTableau || {};
  function lueur(c, coul, fn, k) { const L = MT().lueur; return L ? L(c, coul, fn, k) : fn(); }

  /** Le centre et le rayon (approché) d'un élément. */
  function geom(e) {
    if (e.w != null) return { cx: e.x + e.w / 2, cy: e.y + e.h / 2, rx: e.w / 2, ry: e.h / 2, rect: true };
    const r = e.r ?? 14; return { cx: e.x, cy: e.y, rx: r, ry: r, rect: false };
  }

  /** Allume UN élément (anneau, fond, pastille avec le numéro n). Dessin de craie : il prend son temps d'écriture. */
  function allumer(c, e, n, o = {}) {
    const coul = o.couleur || 'jaune', g = geom(e);
    // les fonds ne prennent pas de temps d'écriture : on ne les peint qu'une fois la craie arrivée à cet élément
    const vu = () => !Number.isFinite(c.t) || c.t > c.cur;
    const fond = vu() ? { fond: coul, fondAlpha: .14 } : {};
    lueur(c, coul, () => {
      if (g.rect) c.rect(e.x - 3, e.y - 3, e.w + 6, e.h + 6, { couleur: coul, largeur: 2.6, arrondi: 8, ...fond });
      else c.cercle(g.cx, g.cy, g.rx + 4, { couleur: coul, largeur: 2.6, ...fond });
    }, 1.8);
    if (o.numero === false || n == null) return;
    const R = o.rayonPastille || 12, pos = e.pos || o.pos || 'haut';
    let px = pos === 'droite' ? g.cx + g.rx + R + 8 : pos === 'gauche' ? g.cx - g.rx - R - 8 : g.cx;
    let py = pos === 'bas' ? g.cy + g.ry + R + 8 : pos === 'haut' ? g.cy - g.ry - R - 8 : g.cy;
    if (e.bx != null) { px = e.bx; py = e.by ?? g.cy; } else if (e.by != null) py = e.by;   // pastille placée ailleurs (une marge libre)
    c.cercle(px, py, R, { couleur: coul, largeur: 1.8, ...(vu() ? { fond: '#10231b', fondAlpha: .92 } : {}) });
    c.texte(String(n), px, py + 6, { couleur: coul, taille: o.taille || 17, align: 'center' });
  }

  function compter(c, K, elements, o = {}) {
    const pre = o.prefixe || 'compte', noms = [];
    elements.forEach((e, i) => {
      c.pause(i === 0 ? (o.avant ?? .2) : (o.pas ?? .45));
      allumer(c, e, e.n ?? i + 1, o);   // e.n : un numéro imposé (le dernier d’une longue liste : 2022)
      const g = geom(e), nom = `${pre}_${i + 1}`;
      c.repere(nom, g.cx - g.rx - 6, g.cy - g.ry - 6, 2 * g.rx + 12, 2 * g.ry + 12, e.libelle || `élément ${i + 1}`);
      K.marque(nom); noms.push(nom);
    });
    if (o.total) {
      const t = o.total; c.pause(o.pas ?? .45);
      c.texte(t.t, t.x, t.y, { couleur: t.couleur || o.couleur || 'jaune', taille: t.taille || 21, align: t.align });
      if (t.repere !== false) c.repere(`${pre}_total`, t.x - (t.align === 'center' ? 90 : 4), t.y - 24, t.l || 190, 32, t.t);
      K.marque(`${pre}_total`); noms.push(`${pre}_total`);
    }
    return noms;
  }

  window.MathsCompte = { compter, allumer };
})();
