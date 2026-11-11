/*
 * Écriture des noyaux à la craie (radioactivité, 10 novembre 2026) : la notation ᴬ_Z X s'écrit comme au tableau,
 * A en haut à gauche, Z en bas à gauche, alignés à droite contre le symbole. Chargé APRÈS tableau.js et exposants.js.
 *
 *   craie.nucleide('U', 238, 92, x, y, o)          → x de fin ; x = bord gauche du bloc (A/Z compris), y = ligne de base
 *   craie.noyaux('[238,92]U → [234,90]Th + [4,2]He', x, y, o)   → x de fin ; texte libre entre les [A,Z]Symbole
 *   craie.largeurNoyaux(s, taille)                   → largeur, pour centrer : x = centre − largeur / 2
 *
 * o : taille (18), couleur, couleurAZ (sinon la même), duree (sinon au rythme de la craie), gras.
 * Z négatif (électron ⁰₋₁e) : écrire [0,-1]e ; le moins est un vrai « − ».
 */
(function () {
  'use strict';
  const T = window.Tableau; if (!T || T.Craie.__noyaux) return;
  const P = T.Craie.prototype;
  T.Craie.__noyaux = true;
  const RE = /\[(-?\d+)\s*,\s*([-+−]?\d+)\]([A-Za-zαβγ]+)/g;
  const txt = (v) => String(v).replace('-', '−');
  function morceaux(s) {
    const out = []; let i = 0, m; RE.lastIndex = 0;
    while ((m = RE.exec(s))) {
      if (m.index > i) out.push({ t: s.slice(i, m.index) });
      out.push({ A: m[1], Z: m[2], X: m[3] }); i = RE.lastIndex;
    }
    if (i < s.length) out.push({ t: s.slice(i) });
    return out;
  }
  P.largeurNucleide = function (X, A, Z, taille = 18) {
    const p = taille * .6;
    return Math.max(this.largeurTexte(txt(A), p), this.largeurTexte(txt(Z), p)) + 1.5 + this.largeurTexte(X, taille);
  };
  P.nucleide = function (X, A, Z, x, y, o = {}) {
    const taille = o.taille ?? 18, p = taille * .6;
    const wAZ = Math.max(this.largeurTexte(txt(A), p), this.largeurTexte(txt(Z), p));
    const xs = x + wAZ + 1.5, cAZ = o.couleurAZ || o.couleur;
    const d = o.duree != null ? o.duree / 3 : undefined;
    this.texte(txt(A), xs - 1, y - taille * .42, { taille: p, couleur: cAZ, align: 'right', duree: d, gras: o.gras });
    this.texte(txt(Z), xs - 1, y + taille * .22, { taille: p, couleur: cAZ, align: 'right', duree: d, gras: o.gras });
    this.texte(X, xs, y, { taille, couleur: o.couleur, duree: d, gras: o.gras });
    return xs + this.largeurTexte(X, taille);
  };
  P.largeurNoyaux = function (s, taille = 18) {
    return morceaux(String(s)).reduce((w, m) => w + (m.t != null ? this.largeurTexte(m.t, taille) : this.largeurNucleide(m.X, m.A, m.Z, taille)), 0);
  };
  P.noyaux = function (s, x, y, o = {}) {
    const taille = o.taille ?? 18; let px = o.align === 'center' ? x - this.largeurNoyaux(s, taille) / 2 : x;
    const oo = { ...o, align: 'left' };
    for (const m of morceaux(String(s))) {
      if (m.t != null) { this.texte(m.t, px, y, oo); px += this.largeurTexte(m.t, taille); }
      else px = this.nucleide(m.X, m.A, m.Z, px, y, oo);
    }
    return px;
  };
})();
