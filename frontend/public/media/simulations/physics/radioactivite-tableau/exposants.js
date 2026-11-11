/*
 * Exposants écrits à la craie (10 novembre 2026) : la police du tableau (Patrick Hand) n’a pas « ⁻ » ni « ⁶ » et ses
 * « ² ³ » sont minuscules ; « 25×10⁻⁶ s » s’affichait avec des chiffres de deux polices. Ce module, chargé APRÈS
 * tableau.js, écrit tout exposant (« 10⁻³ », ou « 10^{-3} ») comme un indice inversé : plus petit et plus haut, même police.
 * Il ne modifie pas le kit : il complète Craie.texte pour les pages de ce dossier qui le chargent.
 */
(function () {
  'use strict';
  const T = window.Tableau; if (!T || T.Craie.__exposants) return;
  const C = T.Craie, P = C.prototype, segmentsKit = C.segments, texteKit = P.texte;
  const CHIFFRES = { '⁻': '−', '⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4', '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9' };
  const SUP = /[⁻⁰¹²³⁴⁵⁶⁷⁸⁹]|\^/;
  C.__exposants = true;
  /** Découpe « ^{…} » en exposant, puis laisse le kit découper les indices (« y_M »). */
  C.segments = function (s) {
    const out = [], re = /\^(\{[^}]+\}|[-−]?[0-9]+)/g; let i = 0, m;
    while ((m = re.exec(s))) {
      if (m.index > i) out.push(...segmentsKit(s.slice(i, m.index)));
      out.push({ t: m[1].replace(/[{}]/g, '').replace('-', '−'), sub: false, sup: true }); i = re.lastIndex;
    }
    if (i < s.length) out.push(...segmentsKit(s.slice(i)));
    return out;
  };
  P.texte = function (s, x, y, o = {}) {
    s = String(s);
    if (!SUP.test(s)) return texteKit.call(this, s, x, y, o);
    s = s.replace(/[⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+/g, (g) => '^{' + [...g].map((ch) => CHIFFRES[ch]).join('') + '}');
    let taille = o.taille ?? 18;
    this.ctx.font = `${o.gras ? '700 ' : ''}${taille}px ${T.POLICE}`;
    this._verifierCadre(s.replace(/[_^{}]/g, ''), x, y, taille, o.align);
    if (this.echelle && this.tailleMin) taille = Math.max(taille, this.tailleMin / this.echelle);
    return this._texteIndices(s, x, y, o, taille);
  };
  /** Même écriture que le kit, avec en plus les exposants (plus petits, relevés). */
  P._texteIndices = function (s, x, y, o, taille) {
    const c = this.ctx, segs = C.segments(s), police = (t) => `${o.gras ? '700 ' : ''}${t}px ${T.POLICE}`;
    const petit = taille * .62, tailleDe = (seg) => (seg.sub || seg.sup ? petit : taille);
    const largeur = (seg) => { c.font = police(tailleDe(seg)); return c.measureText(seg.t).width; };
    const total = segs.reduce((w, seg) => w + largeur(seg), 0);
    if (o.max && total > o.max) return this._texteIndices(s, x, y, { ...o, max: 0 }, Math.max(10, taille * o.max / total));
    const plain = segs.map((seg) => seg.t).join('');
    const part = this._part(o.duree ?? Math.max(.1, plain.length / 16));
    if (part <= 0) return this;
    let reste = part < 1 ? Math.max(1, Math.ceil(part * plain.length)) : plain.length;
    c.fillStyle = this.couleur(o.couleur); c.globalAlpha = o.alpha ?? .96; c.textBaseline = o.base || 'alphabetic';
    c.shadowColor = 'rgba(255,255,255,.25)'; c.shadowBlur = 1; c.textAlign = 'left';
    let px = (o.align === 'center') ? x - total / 2 : (o.align === 'right') ? x - total : x;
    for (const seg of segs) {
      if (reste <= 0) break;
      const t = seg.t.slice(0, reste); reste -= seg.t.length;
      c.font = police(tailleDe(seg));
      c.fillText(t, px, y + (seg.sub ? taille * .28 : seg.sup ? -taille * .42 : 0));
      px += c.measureText(t).width;
      if (t.length < seg.t.length) break;
    }
    if (part < 1) this.tip = [px, y - taille * .3];
    c.shadowBlur = 0; c.globalAlpha = 1;
    return this;
  };
})();
