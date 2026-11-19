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

/* ─── Tableau large (RadioLarge) : placé ici parce que le serveur de dev ne servait pas un nouveau fichier .js ───
 * (liste des fichiers publics figée au démarrage) ; noyaux.js est chargé par toutes les pages de la radioactivité. */
/*
 * Tableau large (15 novembre 2026, demande de l'utilisateur : « mieux exploiter tout le tableau, grands calibres de
 * texte, simulations agrandies »). Les pages de la radioactivité dessinent dans l'ancien cadre 760 × 420. Avec
 * Scene(…, { large: true }) le cadre fait L × 420 (L jusqu'à 1292 sur un portable 1366 × 613) : chaque page découpe
 * son dessin en BLOCS (rectangles de l'ancien cadre) et pose chaque bloc, agrandi, dans une case du tableau large
 * (figure au centre sur toute la hauteur, textes à côté). Le dessin est rejoué une fois par bloc, rogné au bloc,
 * avec la même horloge d'écriture et le même tremblement : rien ne change dans le déroulé ni dans le contrat avec le
 * tuteur. Les repères suivent (réunion des morceaux posés), le pointeur aussi (scene.local renvoie les coordonnées
 * de l'ancien cadre).
 *
 *   RadioLarge.dessiner(c, scene, graine, blocs, corps)
 *     blocs : [{ src: [x0, y0, x1, y1], dst: [x0, y0, x1, y1], ax?: 0..1, ay?: 0..1 }] (dst dans le cadre L × 420 ;
 *             le bloc garde ses proportions, ax / ay : où il se cale dans sa case, 0,5 = centré)
 *     ou null : disposition d'origine, centrée dans le cadre.
 *   RadioLarge.large(scene) : vrai quand le tableau est assez large pour la disposition en blocs (L ≥ 1000).
 */
(function () {
  'use strict';
  const VW = 760, VH = 420, SEUIL = 1000;
  const large = scene => scene.L >= SEUIL;
  function poser(b) {
    const [sx0, sy0, sx1, sy1] = b.src, [dx0, dy0, dx1, dy1] = b.dst;
    const k = Math.min((dx1 - dx0) / (sx1 - sx0), (dy1 - dy0) / (sy1 - sy0), b.kmax ?? 9);
    const ax = b.ax ?? .5, ay = b.ay ?? .5;
    const tx = dx0 + ((dx1 - dx0) - (sx1 - sx0) * k) * ax - sx0 * k, ty = dy0 + ((dy1 - dy0) - (sy1 - sy0) * k) * ay - sy0 * k;
    return { ...b, k, tx, ty };
  }
  const inter = (r, s) => { const x0 = Math.max(r[0], s[0]), y0 = Math.max(r[1], s[1]), x1 = Math.min(r[2], s[2]), y1 = Math.min(r[3], s[3]); return x1 > x0 && y1 > y0 ? [x0, y0, x1, y1] : null; };
  function dessiner(c, scene, graine, blocs, corps) {
    if (!blocs) {
      // Disposition d'origine : l'ancien cadre centré dans le cadre (L peut dépasser 760 sur un grand écran).
      const dx = (scene.L - VW) / 2; scene._blocs = [{ src: [0, 0, VW, VH], k: 1, tx: dx, ty: 0 }];
      c.ctx.save(); c.ctx.translate(dx, 0);
      try { corps(); } finally { c.ctx.restore(); }
      if (c.tip && dx) c.tip = [c.tip[0] + dx, c.tip[1]];
      return;
    }
    const P = blocs.map(poser); scene._blocs = P;
    const cur0 = c.cur, repere = c.repere, notes = new Map();
    let tip = null, complet = true;
    c.repere = function (id, x, y, w, h, label) { if (!notes.has(id)) notes.set(id, { r: [Math.min(x, x + w), Math.min(y, y + h), Math.max(x, x + w), Math.max(y, y + h)], label }); return this; };
    try {
      for (const b of P) {
        c.cur = cur0; c.tip = null; c.complet = true; c.r = window.Tableau.graine(graine);
        c.ctx.save();
        c.ctx.translate(b.tx, b.ty); c.ctx.scale(b.k, b.k);
        c.ctx.beginPath(); c.ctx.rect(b.src[0], b.src[1], b.src[2] - b.src[0], b.src[3] - b.src[1]); c.ctx.clip();
        const echelle = c.echelle; c.echelle = echelle * b.k;      // le minimum de 15 px à l'écran tient compte du bloc
        try { corps(); } finally { c.ctx.restore(); c.echelle = echelle; }
        complet = complet && c.complet;
        if (c.tip && c.tip[0] >= b.src[0] && c.tip[0] <= b.src[2] && c.tip[1] >= b.src[1] && c.tip[1] <= b.src[3]) tip = [b.tx + c.tip[0] * b.k, b.ty + c.tip[1] * b.k];
      }
    } finally { c.repere = repere; }
    c.complet = complet; c.tip = tip;
    // Chaque repère : la réunion de ses morceaux posés (un repère à cheval sur deux blocs les entoure tous les deux).
    for (const [id, { r, label }] of notes) {
      let u = null;
      for (const b of P) {
        const i = inter(r, b.src); if (!i) continue;
        const q = [b.tx + i[0] * b.k, b.ty + i[1] * b.k, b.tx + i[2] * b.k, b.ty + i[3] * b.k];
        u = u ? [Math.min(u[0], q[0]), Math.min(u[1], q[1]), Math.max(u[2], q[2]), Math.max(u[3], q[3])] : q;
      }
      if (!u) { const b = P[0]; u = [b.tx + r[0] * b.k, b.ty + r[1] * b.k, b.tx + r[2] * b.k, b.ty + r[3] * b.k]; }
      repere.call(c, id, u[0], u[1], u[2] - u[0], u[3] - u[1], label);
    }
  }
  /** Le pointeur : coordonnées du cadre → coordonnées de l'ancien cadre 760 × 420 (dans le bloc touché). */
  function brancher(scene) {
    const local = scene.local;
    scene.local = (px, py) => {
      const [x, y] = local(px, py), P = scene._blocs || [];
      for (const b of P) {
        const u = (x - b.tx) / b.k, v = (y - b.ty) / b.k;
        if (u >= b.src[0] - 20 && u <= b.src[2] + 20 && v >= b.src[1] - 20 && v <= b.src[3] + 20) return [u, v];
      }
      const b = P[0]; return b ? [(x - b.tx) / b.k, (y - b.ty) / b.k] : [x, y];
    };
    return scene;
  }
  /** Une phrase coupée en lignes de largeur ≤ max ; `mesure(s)` donne la largeur d'un morceau (craie ou formule). */
  function couper(s, max, mesure) {
    const mots = String(s).split(' '), out = []; let l = '';
    for (const m of mots) { const e = l ? l + ' ' + m : m; if (l && mesure(e) > max) { out.push(l); l = m; } else l = e; }
    if (l) out.push(l);
    return out;
  }
  /** Colonne de texte du tableau large : source virtuelle à droite de l'ancien cadre (x ≥ X0), largeur `w` (source). */
  const X0 = 800, COLW = 270, COLD = 310;
  /**
   * Une phrase écrite dans la colonne de texte (source x = X0, largeur COLW), coupée à la ligne, dans la case `rang`
   * sur `n` cases égales (de haut en bas). o.taille, o.couleur, o.duree ; `mesure` pour une formule (noyaux).
   * Renvoie le rectangle écrit [x, y, w, h] (pour le repère). `ecrire(ligne, x, y, oo)` remplace c.texte si fourni.
   */
  function enColonne(c, s, rang, n, o = {}, ecrire, mesure) {
    // coupée à la taille vraiment écrite (18 novembre 2026 : le plancher de 15 px à l’écran grossit le texte sur un petit
    // tableau ; mesurée à la taille demandée, la ligne débordait de la colonne, coupée au bord du cadre)
    const t = o.taille ?? 18, tv = Math.max(t, c.echelle && c.tailleMin ? c.tailleMin / c.echelle : 0), h = 392 / n, y0 = 14 + rang * h, pas = tv * 1.32;
    const lignes = couper(s, COLW, mesure || (e => c.largeurTexte(String(e).replace(/[_^{}]/g, ''), tv)));
    const duree = o.duree != null ? o.duree / lignes.length : undefined;
    lignes.forEach((l, i) => { const oo = { ...o, align: 'left', max: undefined, duree }; ecrire ? ecrire(l, X0, y0 + tv + i * pas, oo) : c.texte(l, X0, y0 + tv + i * pas, oo); });
    return [X0 - 6, y0 - 4, COLW + 12, lignes.length * pas + 12];
  }
  /** Disposition type : la figure `src` (ancien cadre) agrandie à gauche, la colonne de texte à droite. */
  function blocsStd(scene, src = [0, 0, 760, 420], o = {}) {
    const L = scene.L, d = o.colonne ?? COLD;
    return [
      { src, dst: [0, 0, L - d, 420], ax: o.ax ?? .5 },
      { src: [X0 - 8, 0, X0 + COLW + 8, 420], dst: [L - d + 4, 0, L, 420], ax: 0, ay: 0 },
    ];
  }
  /**
   * Une ligne du bas de l'ancien cadre : à sa place (x, y) sur un tableau étroit ; dans la case `rang` / `n` de la
   * colonne (4 px plus grosse, coupée à la ligne) quand `actif`. `ecrire(s, x, y, o)` et `mesure(s, taille)` pour
   * une formule (noyaux) ; sinon c.texte.
   */
  function ligne(actif, c, s, x, y, o, rang, n, ecrire, mesure) {
    if (!actif) return ecrire ? ecrire(s, x, y, o) : c.texte(s, x, y, o);
    const t = (o.taille ?? 18) + 4;
    return enColonne(c, s, rang, n, { ...o, taille: t }, ecrire, mesure && (e => mesure(e, t)));
  }
  window.RadioLarge = { dessiner, brancher, large, couper, enColonne, ligne, blocsStd, X0, COLW, COLD, SEUIL };
})();
