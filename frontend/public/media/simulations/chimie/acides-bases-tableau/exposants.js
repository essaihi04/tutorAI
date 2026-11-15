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

/*
 * Recomposition sur la largeur du tableau (15 novembre 2026, « mieux exploiter tout le tableau, grands calibres de texte,
 * simulations agrandies ») : les pages de ce dossier dessinent dans un cadre 760 × 420. Avec Scene(…, { large: true }),
 * le cadre fait L × 420 (L de 1000 à 1596 sur un écran d'ordinateur). Recompose(c, scene, blocs) découpe le dessin en
 * blocs (rectangles du cadre 760 × 420, dans l'ordre de lecture) et les range en colonnes sur toute la largeur, chaque
 * bloc agrandi du même facteur k (le plus grand qui tient). Chaque trait, texte, point et repère suit le bloc où il
 * tombe (son point d'ancrage) : les repères pointés par le professeur suivent donc les nouvelles positions.
 *   blocs : [{ r: [x, y, w, h], haut?: true (bande du haut : le titre), direct?: true (reçoit les dessins peints
 *            c.direct), centre?: true (centré dans sa colonne) }] ; o.cols : partition imposée ([[0, 1], [2, 3]]) ;
 *            o.kMax (2,2 par défaut), o.kHaut (1,25 : le titre) ; bloc.e : noms d'étapes du déroulé (o.M.etape) dont
 *            tout le dessin va dans ce bloc, quel que soit son point d'ancrage (une fraction, une flèche restent avec leur ligne).
 *   bloc.etire (true = jusqu'à 1,8, ou un nombre) : un graphe ; la largeur libre l'étire en x (traits écartés, textes
 *            et points non déformés).
 *   L < 1000 (grand écran, cadre déjà haut) ou blocs absents : rien ne change, disposition d'origine.
 */
(function () {
  'use strict';
  const VH = 420, MARGE = 12, ECART = 34, ECART_V = 12;
  const dedans = (r, x, y, t = 4) => x >= r[0] - t && x <= r[0] + r[2] + t && y >= r[1] - t && y <= r[1] + r[3] + t;
  function disposer(L, blocs, o) {
    const haut = blocs.map((b, i) => [b, i]).filter(([b]) => b.haut), corps = blocs.map((b, i) => [b, i]).filter(([b]) => !b.haut);
    const out = new Array(blocs.length);
    const kH = o.kHaut ?? 1.25; let yH = 6, xH = MARGE, hH = 0;
    for (const [b, i] of haut) { out[i] = { k: kH, x: xH, y: yH }; xH += b.r[2] * kH + ECART; hH = Math.max(hH, b.r[3] * kH); }
    const y0 = haut.length ? yH + hH + 8 : MARGE, H = VH - MARGE - y0, W = L - 2 * MARGE, n = corps.length;
    if (!n) return out;
    const parts = [];
    if (o.cols) parts.push(o.cols.map(col => col.map(j => corps.findIndex(([, i]) => i === j))));
    else for (let nc = 1; nc <= Math.min(o.colsMax ?? 3, n); nc++) {
      const rec = (deb, reste, acc) => {
        if (reste === 1) { parts.push([...acc, range(deb, n)]); return; }
        for (let f = deb + 1; f <= n - reste + 1; f++) rec(f, reste - 1, [...acc, range(deb, f)]);
      };
      rec(0, nc, []);
    }
    function range(a, b) { const r = []; for (let i = a; i < b; i++) r.push(i); return r; }
    let mieux = null;
    for (const p of parts) {
      const cw = p.map(col => Math.max(...col.map(j => corps[j][0].r[2]))), ch = p.map(col => col.reduce((s, j) => s + corps[j][0].r[3], 0) + ECART_V * (col.length - 1));
      const k = Math.min(o.kMax ?? 2.2, H / Math.max(...ch), (W - ECART * (p.length - 1)) / cw.reduce((a, b) => a + b, 0));
      if (!mieux || k > mieux.k * 1.03) mieux = { p, cw, ch, k };
    }
    const { p, cw, ch, k } = mieux, f = {};
    /* Chaque colonne prend la hauteur du tableau : son propre facteur (les textes à côté d'un graphe grandissent),
     * borné par la largeur ; une colonne qui contient un graphe étiré garde k et reçoit la largeur restante. */
    const aE = col => col.some(j => corps[j][0].etire), kTexte = o.kTexte ?? 1.7;
    let kc = p.map((col, ci) => aE(col) ? k : Math.max(k, Math.min(kTexte, o.kMax ?? 2.2, H / ch[ci])));
    const larg = () => kc.reduce((s, kk, ci) => s + kk * cw[ci], 0);
    if (larg() > W - ECART * (p.length - 1)) {
      const sansE = p.map((col, ci) => (aE(col) ? 0 : (kc[ci] - k) * cw[ci])).reduce((a, b) => a + b, 0), trop = larg() - (W - ECART * (p.length - 1));
      kc = kc.map((kk, ci) => (aE(p[ci]) ? kk : kk - (kk - k) * Math.min(1, trop / Math.max(1e-6, sansE))));
    }
    let libre = W - ECART * (p.length - 1) - larg();
    // Blocs « etire » (un graphe) : la place libre en largeur les étire (les textes gardent leur forme, seul l'écart grandit).
    const colsE = p.map((col, ci) => [ci, col.filter(j => corps[j][0].etire)]).filter(([, l]) => l.length);
    if (colsE.length && libre > 0) {
      const part = libre * .85 / colsE.length;
      for (const [ci, l] of colsE) {
        let w = cw[ci];
        for (const j of l) { const b = corps[j][0], fm = b.etire === true ? 1.8 : b.etire; f[j] = Math.min(fm, (cw[ci] * kc[ci] + part) / (b.r[2] * kc[ci])); w = Math.max(w, b.r[2] * f[j]); }
        libre -= (w - cw[ci]) * kc[ci]; cw[ci] = w;
      }
    }
    const g = libre / (p.length + 1);
    let x = MARGE + g;
    p.forEach((col, ci) => {
      const k = kc[ci], hs = col.map(j => corps[j][0].r[3] * k), reste = H - hs.reduce((a, b) => a + b, 0) - ECART_V * (col.length - 1);
      const vg = Math.min(reste / (col.length + 1), 28); let y = y0 + (reste - vg * (col.length - 1)) / 2;
      col.forEach((j, n2) => {
        const [b, i] = corps[j], w = b.r[2] * k * (f[j] || 1);
        out[i] = { k, f: f[j] || 1, x: b.centre ? x + (cw[ci] * k - w) / 2 : x, y };
        y += hs[n2] + ECART_V + vg;
      });
      x += cw[ci] * k + ECART + g;
    });
    return out;
  }
  function installer(c) {
    if (c.__rcPose) return; c.__rcPose = true;
    let prof = 0;
    /* Un dessin peint (c.direct) : on le « sonde » une fois sans rien tracer pour savoir où il tombe (centre de ses points). */
    const ctx = c.ctx, TRACE = ['moveTo', 'lineTo', 'arc', 'rect', 'roundRect', 'ellipse', 'fillRect', 'strokeRect', 'quadraticCurveTo', 'bezierCurveTo', 'fillText', 'drawImage'];
    const MUET = ['fill', 'stroke', 'fillRect', 'strokeRect', 'fillText', 'strokeText', 'drawImage', 'clearRect'];
    function sonder(fn) {
      const base = ctx.getTransform().inverse(), pts = [], avant = {};
      for (const h of new Set([...TRACE, ...MUET])) {
        avant[h] = ctx[h];
        ctx[h] = function (...a) {
          if (TRACE.includes(h)) {
            const m = ctx.getTransform(), xy = h === 'fillText' ? [[a[1], a[2]]] : h === 'drawImage' ? [[a[a.length > 5 ? 5 : 1], a[a.length > 5 ? 6 : 2]]]
              : h === 'arc' || h === 'ellipse' ? [[a[0], a[1]]] : /[Rr]ect/.test(h) ? [[a[0] + a[2] / 2, a[1] + a[3] / 2]] : [[a[a.length - 2], a[a.length - 1]]];
            for (const [px, py] of xy) if (Number.isFinite(px) && Number.isFinite(py)) { const q = base.transformPoint(m.transformPoint(new DOMPoint(px, py))); pts.push([q.x, q.y]); }
          }
          if (!MUET.includes(h)) return avant[h].apply(ctx, a);
        };
      }
      ctx.save(); prof++;
      try { c.direct.__orig(fn); } catch (e) { /* une sonde ne casse jamais l'image */ } finally { prof--; ctx.restore(); for (const h in avant) ctx[h] = avant[h]; }
      if (!pts.length) return null;
      const xs = pts.map(q => q[0]).sort((u, v) => u - v), ys = pts.map(q => q[1]).sort((u, v) => u - v);
      return [(xs[0] + xs[xs.length - 1]) / 2, (ys[0] + ys[ys.length - 1]) / 2];
    }
    /* Un dessin peint dans un bloc étiré : ses points s'écartent en x (rayons, textes et largeurs de trait inchangés). */
    const ETIRE = { moveTo: [0], lineTo: [0], quadraticCurveTo: [0, 2], bezierCurveTo: [0, 2, 4], arc: [0], ellipse: [0], fillText: [1], strokeText: [1], rect: [0, 'w2'], roundRect: [0, 'w2'], fillRect: [0, 'w2'], strokeRect: [0, 'w2'] };
    let gardes = null, baseM = null;
    const pile = [];
    function etirerCtx(x0, f) {
      gardes = {};
      for (const h in ETIRE) {
        gardes[h] = ctx[h];
        ctx[h] = function (...a) { for (const j of ETIRE[h]) { if (j === 'w2') a[2] *= f; else a[j] = x0 + (a[j] - x0) * f; } return gardes[h].apply(ctx, a); };
      }
    }
    function rendreCtx() { if (gardes) for (const h in gardes) ctx[h] = gardes[h]; gardes = null; }
    /* L'encre réelle de chaque bloc (cadre d'origine) : un bloc dont le dessin déborde de son rectangle est agrandi
     * à l'image suivante (rien ne sort du tableau, même si le rectangle déclaré est un peu juste). */
    function encre(R, i, nom, a) {
      let x0, y0, x1, y1;
      if (nom === 'texte') {
        const o = a[3] || {}; let t = o.taille ?? 18; if (c.echelle && c.tailleMin) t = Math.max(t, c.tailleMin / c.echelle);
        ctx.save(); ctx.font = `${t}px ${window.Tableau.POLICE}`; let l = ctx.measureText(String(a[0]).replace(/[_^{}]/g, '')).width; ctx.restore();
        if (o.max) l = Math.min(l, o.max);
        x0 = o.align === 'center' ? a[1] - l / 2 : o.align === 'right' ? a[1] - l : a[1]; x1 = x0 + l; y0 = a[2] - t * .95; y1 = a[2] + t * .4;
      } else if (nom === 'trait') { const p = a[0] || []; if (!p.length) return; x0 = Math.min(...p.map(q => q[0])); x1 = Math.max(...p.map(q => q[0])); y0 = Math.min(...p.map(q => q[1])); y1 = Math.max(...p.map(q => q[1])); }
      else if (nom === 'point') { const r = a[2] ?? 4; x0 = a[0] - r; x1 = a[0] + r; y0 = a[1] - r; y1 = a[1] + r; }
      else return;
      if (![x0, y0, x1, y1].every(Number.isFinite)) return;
      const r = R.blocs[i].r, e = R.ext[i] || [r[0], r[1], r[0] + r[2], r[1] + r[3]];
      const n = [Math.min(e[0], x0 - 2), Math.min(e[1], y0 - 2), Math.max(e[2], x1 + 2), Math.max(e[3], y1 + 2)];
      if (n[0] < e[0] - .5 || n[1] < e[1] - .5 || n[2] > e[2] + .5 || n[3] > e[3] + .5) { R.ext[i] = n; R.change = true; }
    }
    const avec = (nom, ancre) => {
      const orig = c[nom].bind(c);
      c[nom] = function (...a) {
        const R = c.__rc; if (!R || prof > 0) return orig(...a);
        let i = -1;
        const cand = c.__rcEtape != null ? R.parEtape[c.__rcEtape] : null, [x, y] = ancre(...a), ok = Number.isFinite(x) && Number.isFinite(y);
        // Le bloc « direct » (un montage peint) garde tout ce qui tombe dans son cadre, quelle que soit l'étape.
        const seul = R.blocs.length === 1, q = nom === 'direct' && !seul ? sonder(a[0]) : ok ? [x, y] : null, D = R.direct >= 0 ? R.blocs[R.direct].r : null;
        if (seul) i = 0;   // disposition d'origine centrée : un seul bloc, pas de sonde
        else if (q && D && dedans(D, q[0], q[1], 0)) i = R.direct;
        else if (cand && cand.length === 1) i = cand[0];
        else if (nom === 'direct') { i = q ? R.trouver(q[0], q[1], cand || undefined) : cand ? (cand.includes(R.direct) ? R.direct : cand[0]) : R.direct; }
        else if (cand) i = ok ? R.trouver(x, y, cand) : cand[0];
        else if (ok) i = R.trouver(x, y);
        const P = i >= 0 ? R.pos[i] : null; if (!P) return orig(...a);
        const b = R.blocs[i].r, tip = c.tip, f = P.f || 1, ext = pile.length ? pile[pile.length - 1] : null, estD = nom === 'direct';
        encre(R, i, nom, a);
        // Dans un dessin peint, chaque trait ou texte de craie retrouve SON bloc (le repère du cadre est remis d'abord).
        if (ext && ext.f !== 1) rendreCtx();
        ctx.save();
        if (ext) ctx.setTransform(baseM); else baseM = ctx.getTransform();
        ctx.translate(P.x - b[0] * P.k, P.y - b[1] * P.k); ctx.scale(P.k, P.k);
        if (f !== 1 && !estD) {
          // Bloc étiré : les points s'écartent en x, les textes et les points gardent leur forme.
          const X = v => b[0] + (v - b[0]) * f;
          if (nom === 'texte' || nom === 'point') a[1 - (nom === 'point')] = X(a[1 - (nom === 'point')]);
          else if (nom === 'trait') a[0] = (a[0] || []).map(q => [X(q[0]), q[1]]);
          else if (nom === 'repere') { a[1] = X(a[1]); a[3] *= f; }
        }
        if (estD) { pile.push({ x0: b[0], f }); if (f !== 1) etirerCtx(b[0], f); } else prof++;
        try { return orig(...a); } finally {
          if (estD) { if (f !== 1) rendreCtx(); pile.pop(); } else prof--;
          ctx.restore();
          if (ext && ext.f !== 1) etirerCtx(ext.x0, ext.f);
          if (c.tip && c.tip !== tip) c.tip = [P.x + (c.tip[0] - b[0]) * P.k, P.y + (c.tip[1] - b[1]) * P.k];
        }
      };
    };
    avec('texte', (s, x, y, o = {}) => [x, y - (o.taille ?? 18) * .35]);
    avec('trait', pts => (pts && pts[0]) || [NaN, NaN]);
    avec('point', (x, y) => [x, y]);
    avec('repere', (id, x, y, w, h) => [x + w / 2, y + h / 2]);
    const directOrig = c.direct.bind(c);
    avec('direct', () => [NaN, NaN]);
    c.direct.__orig = directOrig;
  }
  /** Disposition d'origine (760 × 420) centrée dans un tableau plus large. */
  function centrer(c, scene) {
    const L = scene.L || 760;
    if (!(L > 761)) { c.__rc = null; return null; }
    if (!c.__rcCentre || c.__rcCentre.L !== L) c.__rcCentre = { L, R: { blocs: [{ r: [0, 0, 760, 420] }], pos: [{ k: 1, f: 1, x: (L - 760) / 2, y: 0 }], parEtape: {}, ext: [], change: false, direct: -1, trouver: () => 0 } };
    c.__rc = c.__rcCentre.R;
    return null;
  }
  /** Point du tableau large → point du cadre d'origine (poignées que l'on glisse à la souris). */
  function inverse(R, X, Y) {
    let mieux = null;
    R.blocs.forEach((b, i) => {
      const P = R.pos[i]; if (!P || b.haut) return;
      const r = b.r, e = R.ext[i] || [r[0], r[1], r[0] + r[2], r[1] + r[3]];
      const sx = r[0] + (X - P.x) / (P.k * (P.f || 1)), sy = r[1] + (Y - P.y) / P.k;
      const d = Math.hypot(Math.max(e[0] - sx, 0, sx - e[2]), Math.max(e[1] - sy, 0, sy - e[3])) * P.k;
      if (!mieux || d < mieux.d) mieux = { d, p: [sx, sy] };
    });
    return mieux ? mieux.p : [X, Y];
  }
  function Recompose(c, scene, blocs, o = {}) {
    installer(c);
    if (!scene.__rcLocal) {
      const local = scene.local; scene.__rcLocal = true;
      // « bouger » des pages ne passe que x (y = 0) : on garde la hauteur du dernier point touché pour choisir le bloc.
      let yVu = null;
      scene.local = function (x, y) {
        if (y !== 0) yVu = y; const p = local.call(scene, x, y === 0 && yVu != null ? yVu : y);
        return c.__rc ? inverse(c.__rc, p[0], p[1]) : p;
      };
    }
    if (o.M && !o.M.__rcEtape) {
      const M = o.M, etape = M.etape; M.__rcEtape = true;
      M.etape = function (cc, nom, fn) { const a = cc.__rcEtape; cc.__rcEtape = nom; try { return etape.call(this, cc, nom, fn); } finally { cc.__rcEtape = a; } };
    }
    const opts = { ...o }; delete opts.M; o = opts;
    if (!blocs || !blocs.length || !(scene.L >= 1000)) return centrer(c, scene);
    const cleB = JSON.stringify(blocs), cle = scene.L + cleB + JSON.stringify(o);
    const EXT = (c.__rcExt ||= {}), ext = (EXT[cleB] ||= []);
    if (c.__rcCache && c.__rcCache.R.change) { c.__rcCache = null; scene.sale = true; }
    if (!c.__rcCache || c.__rcCache.cle !== cle) {
      // disposition sur l'encre relevée (le rectangle déclaré, agrandi s'il le faut) ; le classement garde le rectangle déclaré
      const pos = disposer(scene.L, blocs.map((b, i) => (ext[i] ? { ...b, r: [ext[i][0], ext[i][1], ext[i][2] - ext[i][0], ext[i][3] - ext[i][1]] } : b)), o)
        .map((P, i) => (P && ext[i] ? { ...P, x: P.x + (blocs[i].r[0] - ext[i][0]) * P.k * (P.f || 1), y: P.y + (blocs[i].r[1] - ext[i][1]) * P.k } : P));
      const parEtape = {}; blocs.forEach((b, i) => (b.e || []).forEach(n => { (parEtape[n] ||= []).push(i); }));
      c.__rcCache = { cle, R: { blocs, pos, parEtape, ext, change: false, direct: blocs.findIndex(b => b.direct),
        trouver(x, y, parmi) {
          const ids = parmi || blocs.map((b, j) => j);
          let i = ids.find(j => dedans(blocs[j].r, x, y, 0)); if (i != null) return i;
          i = ids.find(j => dedans(blocs[j].r, x, y, 6)); if (i != null) return i;
          let d = Infinity; ids.forEach(j => { const b = blocs[j]; const dx = Math.max(b.r[0] - x, 0, x - b.r[0] - b.r[2]), dy = Math.max(b.r[1] - y, 0, y - b.r[1] - b.r[3]), e = Math.hypot(dx, dy); if (e < d) { d = e; i = j; } });
          return i;
        },
        /** Point du cadre d'origine → point du tableau large (pour un dessin fait à la main hors des blocs). */
        vers(x, y) { const i = this.trouver(x, y), P = pos[i], b = blocs[i].r; return [P.x + (x - b[0]) * P.k, P.y + (y - b[1]) * P.k]; } } };
    }
    // Rien à gagner (aucun bloc agrandi ou étiré d'au moins 15 %, ou un bloc qui rapetisse) : la disposition d'origine, centrée.
    // (un graphe étiré peut perdre un peu de hauteur : jusqu'à 12 %, s'il gagne en largeur)
    const R = c.__rcCache.R, corps = R.pos.map((P, i) => [P, blocs[i]]).filter(([P, b]) => P && !b.haut);
    const ok = corps.every(([P, b]) => P.k >= (b.etire ? .88 : .97)), gain = Math.max(...corps.map(([P]) => P.k * (P.f || 1)));
    if (!(ok && gain >= 1.15)) return centrer(c, scene);
    c.__rc = R;
    return c.__rc;
  }
  window.Recompose = Recompose;
})();
