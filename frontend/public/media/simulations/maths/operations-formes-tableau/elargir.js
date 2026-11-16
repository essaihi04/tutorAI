/*
 * Tableau large (15 novembre 2026, « mieux exploiter tout le tableau, grands calibres de texte ») — cours
 * math_ch6_nombres_complexes. À charger APRÈS maths-tableau.js et AVANT la page : MathsTableau.page est enveloppée.
 *
 * Sur un tableau large (portable 1366 × 613 : canvas ≈ 3,2 : 1), une vue « figure + colonne de calculs » laissait de grands
 * vides à gauche et à droite : le cadre 760 × 420 est mis à l'échelle de la HAUTEUR. Ici, sans rien changer au dessin des
 * vues, chaque trait, point, texte et repère est rangé dans une ZONE et redessiné à sa place sur toute la largeur :
 *   à GAUCHE  le titre et le début de la colonne (les phrases écrites en premier),
 *   au CENTRE la figure, sur toute la hauteur,
 *   à DROITE  la suite de la colonne (le résultat encadré),
 * le texte agrandi par rapport à la figure. La boîte de l'encre du kit (ajuster) remplit alors le tableau.
 * Les instants (moments, play_until), les repères pointés par le professeur (ils suivent leur zone), les poignées
 * (transformées dans les deux sens) ne changent pas. Tableau haut (grand écran 1920 × 1080, canvas ≈ 2 : 1) : rien ne
 * change, la disposition d'origine y remplit déjà l'écran.
 *
 * Réglages par vue : `elargir: false` (vue laissée telle quelle) ou `elargir: { xr, cote: 'droite' | 'gauche', coupe, seul, bandeau }`
 *   (pas `large`, que le kit transmet à sa Scene : ici le cadre reste 760 × 420, la boîte de l'encre (ajuster) fait le reste)
 *   xr    abscisse (cadre 760) qui sépare la figure de la colonne (sinon : le plus large couloir vide, cherché seul) ;
 *   cote  côté de la colonne dans la vue d'origine (droite par défaut) ;
 *   coupe ordonnée où la colonne se coupe en deux (sinon : le couloir horizontal qui équilibre les deux moitiés) ;
 *   seul  true : la colonne n'est pas coupée (figure à gauche, colonne entière à droite, agrandie).
 */
(function () {
  'use strict';
  const MT = window.MathsTableau; if (!MT || MT.__elargi) return;
  MT.__elargi = true;
  const T = window.Tableau;
  const SEUIL = 2.45;          // canvas plus large que 2,45 × sa hauteur : tableau large
  const VW = 760, MIN_ECRAN = 15;
  const pageOrig = MT.page;
  MT.page = function (def) {
    const P0 = new URLSearchParams(location.search);
    if (def.elargir !== false && P0.get('elargir') !== '0') {
      for (const V of Object.values(def.vues)) if (V.elargir !== false) envelopper(V, V.elargir || {});
    }
    return pageOrig(def);
  };

  const PRIM = ['trait', 'point', 'texte', 'repere', 'rect', 'cercle', '__remplir'];
  function sauver(c) { const d = {}; for (const k of PRIM) d[k] = Object.getOwnPropertyDescriptor(c, k); return d; }
  function rendre(c, d) { for (const k of PRIM) { if (d[k]) Object.defineProperty(c, k, d[k]); else delete c[k]; } }

  /** Boîte d'un texte (cadre d'origine), taille minimale `tmin`. */
  function boiteTexte(c, s, x, y, o, tmin) {
    let t = o.taille ?? 18; if (tmin) t = Math.max(t, tmin);
    c.ctx.font = `${o.gras ? '700 ' : ''}${t}px ${T.POLICE}`;
    let l = c.ctx.measureText(String(s).replace(/_/g, '').replace(/[{}]/g, '')).width; if (o.max && l > o.max) l = o.max;
    const x0 = o.align === 'center' ? x - l / 2 : o.align === 'right' ? x - l : x;
    return { x0, y0: y - t * 0.95, x1: x0 + l, y1: y + t * 0.35 };
  }
  /** Le titre de la vue (K.titre, en (20 ; 30), éventuellement en plusieurs morceaux et ses barres) ou le bandeau du haut. */
  const estTitre = (b, opt) => (b.y1 <= 36 && b.x0 < 400) || (opt.bandeau && b.y1 <= opt.bandeau);
  const centre = (b) => [(b.x0 + b.x1) / 2, (b.y0 + b.y1) / 2];
  const union = (bs) => bs.reduce((u, b) => ({ x0: Math.min(u.x0, b.x0), y0: Math.min(u.y0, b.y0), x1: Math.max(u.x1, b.x1), y1: Math.max(u.y1, b.y1) }), { x0: Infinity, y0: Infinity, x1: -Infinity, y1: -Infinity });
  const vide = (b) => !(b.x1 > b.x0);

  /** Passe d'enregistrement : la construction complète, rien n'est dessiné ; chaque élément et sa boîte. */
  function enregistrer(c, K, orig, V, opt) {
    const items = [], d = sauver(c), garde = { t: c.t, cur: c.cur, complet: c.complet, tip: c.tip };
    const pts = (P, m) => { const b = union(P.filter(p => Number.isFinite(p[0]) && Number.isFinite(p[1])).map(p => ({ x0: p[0] - m, y0: p[1] - m, x1: p[0] + m, y1: p[1] + m }))); return b; };
    const pousser = (it) => { it.titre = (it.texte && it.texte.y === 30 && it.texte.x < 380) || estTitre(it.b, opt); items.push(it); };
    c.trait = function (P, o = {}) { if (P && P.length > 1) pousser({ b: pts(P, (o.largeur ?? 2.4) / 2 + 1) }); return this; };
    c.point = function (x, y, r = 4) { pousser({ b: { x0: x - r, y0: y - r, x1: x + r, y1: y + r } }); return this; };
    c.texte = function (s, x, y, o = {}) { pousser({ b: boiteTexte(this, s, x, y, o, 0), texte: { s: String(s), x, y, o } }); return this; };
    c.rect = function (x, y, w, h) { pousser({ b: { x0: x - 2, y0: y - 2, x1: x + w + 2, y1: y + h + 2 } }); return this; };
    c.cercle = function (x, y, r) { pousser({ b: { x0: x - r - 2, y0: y - r - 2, x1: x + r + 2, y1: y + r + 2 } }); return this; };
    c.repere = function () { return this; };
    c.t = Infinity;
    try { orig.call(V, c, K); } catch (e) { console.warn('[elargir] enregistrement', e); items.length = 0; }
    finally { rendre(c, d); Object.assign(c, garde); }
    return items.filter(it => Number.isFinite(it.b.x0) && it.b.x1 >= it.b.x0);
  }

  /** Le couloir vertical vide le plus large entre 170 et 650 : la frontière figure / colonne. */
  function couloirX(items) {
    const iv = items.filter(i => !i.titre).map(i => [i.b.x0, i.b.x1]).sort((a, b) => a[0] - b[0]);
    let best = null, fin = -Infinity;
    for (const [a, b] of iv) {
      if (a > fin && fin > -Infinity) { const m = (a + fin) / 2; if (m > 170 && m < 650 && (!best || a - fin > best.l)) best = { x: m, l: a - fin }; }
      fin = Math.max(fin, b);
    }
    return best ? best.x : null;
  }
  /** Coupe la colonne en deux à un couloir horizontal vide, en équilibrant les hauteurs. */
  function coupeY(items) {
    const iv = items.map(i => [i.b.y0, i.b.y1]).sort((a, b) => a[0] - b[0]);
    const haut = iv.length ? iv[0][0] : 0, bas = Math.max(...iv.map(v => v[1]));
    let best = null, fin = -Infinity;
    for (const [a, b] of iv) {
      if (a > fin && fin > -Infinity) { const m = (a + fin) / 2, h = Math.max(fin - haut, bas - a); if (!best || h < best.h) best = { y: m, h }; }
      fin = Math.max(fin, b);
    }
    return best ? best.y : null;
  }

  /** La disposition : zones (cadre d'origine) → place sur le tableau large. */
  function disposer(c, items, opt, rho, ancien) {
    const cote = opt.cote || 'droite';
    const xr = opt.xr ?? couloirX(items);
    if (xr == null) return null;
    const corps = items.filter(i => !i.titre), titres = items.filter(i => i.titre);
    const dansCol = (i) => { const [cx] = centre(i.b); return cote === 'droite' ? cx >= xr : cx < xr; };
    const fig = corps.filter(i => !dansCol(i)), col = corps.filter(dansCol);
    if (!fig.length || !col.length) return null;
    let coupe = opt.seul ? null : (opt.coupe ?? coupeY(col));
    if (ancien && ancien.coupe !== undefined) coupe = ancien.coupe;
    const zA = coupe == null ? [] : col.filter(i => centre(i.b)[1] < coupe), zB = coupe == null ? col : col.filter(i => centre(i.b)[1] >= coupe);
    // Les boîtes ne font que grandir (un réglage, un point glissé) : rien ne saute.
    const g = (a, b) => (a && !vide(a) ? union([a, b]) : b);
    let F = union(fig.map(i => i.b)), A = zA.length ? union(zA.map(i => i.b)) : null, B = union(zB.map(i => i.b));
    if (ancien) { F = g(ancien.raw.F, F); B = g(ancien.raw.B, B); if (A) A = g(ancien.raw.A, A); }
    const Tt = titres.length ? union(titres.map(i => i.b)) : null;
    const W = VW - 16, gap = 26;
    const tW = Tt ? Tt.x1 - Tt.x0 : 0, bandeau = !!opt.bandeau && !!Tt;
    // bandeau : le haut de la vue (titre, règles) sur toute la largeur, au-dessus des trois zones
    const aB = bandeau ? Math.min(1.45, W / Math.max(1, tW)) : 0;
    const Ytop = bandeau ? 8 + (Tt.y1 - Tt.y0) * aB + 10 : 8, Y1 = VW / rho - 16, H = Y1 - Ytop;   // hauteur utile (cadre 760 de large)
    const tH = Tt && !bandeau ? 30 : 0;
    // Titre au-dessus de la zone gauche (ou de la droite si la colonne n'est pas coupée).
    const fmax = Math.min(H / (F.y1 - F.y0), 2.2);
    let mieux = null;
    for (let i = 0; i <= 24; i++) {
      const f = fmax * (1 - i * 0.022);
      const wF = (F.x1 - F.x0) * f;
      const reste = W - wF - (A ? 2 : 1) * gap;
      const hA = A ? (A.y1 - A.y0) : 0, hB = B.y1 - B.y0;
      const kh = Math.min(A ? (H - tH * 1.1) / hA : Infinity, (H - (A ? 0 : tH * 1.1)) / hB);
      const kw = reste / ((A ? A.x1 - A.x0 : 0) + (B.x1 - B.x0));
      const k = Math.min(kh, kw, 1.9);
      if (!(k > 0)) continue;
      const score = 0.6 * Math.log(k) + 0.4 * Math.log(f);
      if (!mieux || score > mieux.score) mieux = { f, k, score };
    }
    if (!mieux) return null;
    const { f, k } = mieux;
    // Garde-fou : la disposition large n'est gardée que si le texte y gagne vraiment (≥ 12 %) sans trop rapetisser la figure,
    // par rapport à la boîte de l'encre d'origine mise à l'échelle par le kit (ajuster).
    if (c.W > 1 && c.H > 1) {
      const tout = union(items.map(i => i.b)), M = 14;
      const bw = Math.min(VW, tout.x1 + M) - Math.max(0, tout.x0 - M), bh = Math.min(420, tout.y1 + M) - Math.max(0, tout.y0 - M);
      const sOld = Math.min(c.W / bw, c.H / bh, 2.2 * Math.min(c.W / VW, c.H / 420)), sNew = c.W / VW;
      if (k * sNew < 1.1 * sOld || f * sNew < 0.7 * sOld) return null;
    }
    const larg = (Z, a) => (Z ? (Z.x1 - Z.x0) * a : 0);
    const used = larg(A, k) + larg(F, f) + larg(B, k);
    const nGap = A ? 2 : 1, libre = W - used;
    const gp = Math.min(70, libre / (nGap + 0.6)), marge = (libre - gp * nGap) / 2;
    let x = 8 + Math.max(0, marge);
    const Z = {}, place = (nom, R, a, X, Y) => { Z[nom] = { a, tx: X - a * R.x0, ty: Y - a * R.y0 }; };
    const hF = (F.y1 - F.y0) * f;
    // le titre : au-dessus de la zone gauche (ou de la droite si la colonne n'est pas coupée), réduit s'il est trop long
    const aT = !Tt ? 0 : bandeau ? aB : Math.min(k * 1.05, Math.max(0.7, ((A ? larg(A, k) + gp * 0.8 : larg(B, k))) / Math.max(1, tW)));
    const sousTitre = Tt && !bandeau ? Ytop + (Tt.y1 - Tt.y0) * aT + 10 : Ytop;
    if (A) { place('A', A, k, x, sousTitre); Z.titreX = x; x += larg(A, k) + gp; }
    place('F', F, f, x, Ytop + Math.max(0, (H - hF) / 2)); x += larg(F, f) + gp;
    const hB = (B.y1 - B.y0) * k;
    place('B', B, k, x, A ? Ytop + Math.max(0, (H - hB) / 2) : sousTitre); if (!A) Z.titreX = x;
    if (bandeau) Z.T = { a: aT, tx: 8 + (W - tW * aT) / 2 - aT * Tt.x0, ty: 8 - aT * Tt.y0 };
    else if (Tt) Z.T = { a: aT, tx: Z.titreX - aT * Tt.x0, ty: Ytop - aT * Tt.y0 };   // le haut du titre sur Ytop
    return { Z, xr, cote, coupe: coupe == null ? null : coupe, raw: { F, A, B }, f, k, opt };
  }

  function envelopper(V, opt) {
    const orig = V.dessiner;
    let mode = null, rho = 3, lay = null, cle = null;
    // la police de craie arrive après la première image : la disposition est recalculée avec les vraies largeurs
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => { cle = null; });
    V.dessiner = function (c, K) {
      if (mode === null && c.W > 1 && c.H > 1) { rho = c.W / c.H; mode = rho >= SEUIL ? 'large' : 'haut'; }
      if (mode !== 'large') return orig.call(this, c, K);
      const k = JSON.stringify(K.P || {});
      if (k !== cle) {
        cle = k;
        const items = enregistrer(c, K, orig, this, opt);
        let l = disposer(c, items, opt, rho, lay);
        // deuxième passe : les petits textes passent à la taille minimale de l'écran (15 px) une fois l'échelle connue
        if (l) {
          const e = c.W / VW;
          for (const it of items) if (it.texte) {
            const z = it.titre ? l.Z.T : zoneDe(l, it.b);
            if (z) it.b = boiteTexte(c, it.texte.s, it.texte.x, it.texte.y, it.texte.o, MIN_ECRAN / (e * z.a));
          }
          l = disposer(c, items, opt, rho, lay);
        }
        lay = l || lay;   // un réglage qui ne tient plus garde la disposition d'avant (rien ne saute)
        window.__elargir = lay;
      }
      if (!lay) return orig.call(this, c, K);
      return dessinerZones(c, K, orig, lay, this);
    };
    if (V.poignees) {
      const pOrig = V.poignees;
      V.poignees = function (K) {
        const hs = pOrig.call(this, K) || [];
        if (mode !== 'large' || !lay) return hs;
        const z = lay.Z.F;
        return hs.map(h => ({ ...h, x: z.a * h.x + z.tx, y: z.a * h.y + z.ty, bouger: (px, py) => h.bouger((px - z.tx) / z.a, (py - z.ty) / z.a) }));
      };
    }
  }

  function zoneDe(lay, b) {
    if (lay.Z.T && estTitre(b, lay.opt)) return lay.Z.T;
    const [cx, cy] = centre(b);
    const dansCol = lay.cote === 'droite' ? cx >= lay.xr : cx < lay.xr;
    if (!dansCol) return lay.Z.F;
    if (lay.coupe != null && cy < lay.coupe) return lay.Z.A;
    return lay.Z.B;
  }

  /** Dessin réel : chaque élément sous la transformation de sa zone. */
  function dessinerZones(c, K, orig, lay, V) {
    const ctx = c.ctx, M0 = ctx.getTransform(), mesure = !c.cadre, e0 = c.echelle;
    const d = sauver(c);
    const base = {}; for (const k of PRIM) base[k] = c[k];
    let dedans = 0;
    const zTexte = (s, x, y, o) => (y === 30 && x < 380 && lay.Z.T) ? lay.Z.T : zoneDe(lay, boiteTexte(c, s, x, y, o || {}, 0));
    const zPts = (P) => zoneDe(lay, union(P.map(p => ({ x0: p[0], y0: p[1], x1: p[0], y1: p[1] }))));
    const map = (z, x, y) => [z.a * x + z.tx, z.a * y + z.ty];
    function sous(z, fn) {
      dedans++;
      const tip = c.tip;
      ctx.setTransform(M0); ctx.translate(z.tx, z.ty); ctx.scale(z.a, z.a); if (e0) c.echelle = e0 * z.a;
      try { return fn(); } finally {
        ctx.setTransform(M0); c.echelle = e0; dedans--;
        if (c.tip && c.tip !== tip) c.tip = map(z, c.tip[0], c.tip[1]);
      }
    }
    if (mesure) {
      // la mesure de la boîte (kit) : les coordonnées sont transformées, l'enregistreur du kit relève l'encre à sa place
      c.trait = function (P, o = {}) { if (!P || P.length < 2) return base.trait.call(this, P, o); const z = zPts(P); return base.trait.call(this, P.map(p => map(z, p[0], p[1])), { ...o, largeur: (o.largeur ?? 2.4) * z.a }); };
      c.point = function (x, y, r = 4, col) { const z = zoneDe(lay, { x0: x, y0: y, x1: x, y1: y }); const [X, Y] = map(z, x, y); return base.point.call(this, X, Y, r * z.a, col); };
      c.texte = function (s, x, y, o = {}) { const z = zTexte(s, x, y, o); const [X, Y] = map(z, x, y); return base.texte.call(this, s, X, Y, { ...o, taille: (o.taille ?? 18) * z.a, max: o.max ? o.max * z.a : o.max }); };
    } else {
      c.trait = function (P, o) { if (dedans || !P || P.length < 2) return base.trait.call(this, P, o); return sous(zPts(P), () => base.trait.call(this, P, o)); };
      c.point = function (x, y, r, col) { if (dedans) return base.point.call(this, x, y, r, col); return sous(zoneDe(lay, { x0: x, y0: y, x1: x, y1: y }), () => base.point.call(this, x, y, r, col)); };
      c.texte = function (s, x, y, o) { if (dedans) return base.texte.call(this, s, x, y, o); return sous(zTexte(s, x, y, o), () => base.texte.call(this, s, x, y, o)); };
      c.rect = function (x, y, w, h, o) { if (dedans) return base.rect.call(this, x, y, w, h, o); return sous(zoneDe(lay, { x0: x, y0: y, x1: x + w, y1: y + h }), () => base.rect.call(this, x, y, w, h, o)); };
      c.cercle = function (x, y, r, o) { if (dedans) return base.cercle.call(this, x, y, r, o); return sous(zoneDe(lay, { x0: x - r, y0: y - r, x1: x + r, y1: y + r }), () => base.cercle.call(this, x, y, r, o)); };
      // zones colorées du kit (MathsTableau.remplir, 16 novembre 2026) : rangées dans la zone de leurs points, comme un trait
      c.__remplir = function (P, o) { if (dedans) return MT.peint(this, ctx, P, o); return sous(zPts(P), () => MT.peint(this, ctx, P, o)); };
    }
    c.repere = function (id, x, y, w, h, label) {
      const z = zoneDe(lay, { x0: x, y0: y, x1: x + w, y1: y + h });
      if (mesure) { const [X, Y] = map(z, x, y); return base.repere.call(this, id, X, Y, w * z.a, h * z.a, label); }
      return sous(z, () => base.repere.call(this, id, x, y, w, h, label));
    };
    try { return orig.call(V, c, K); } finally { rendre(c, d); ctx.setTransform(M0); c.echelle = e0; }
  }
})();
