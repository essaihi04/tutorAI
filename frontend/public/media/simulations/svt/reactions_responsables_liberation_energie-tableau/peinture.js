/*
 * Milieux vivants PEINTS du cours « Libération de l'énergie » (règle 7 du skill simulations-au-tableau, 9 novembre 2026) :
 * la cellule, son hyaloplasme, la mitochondrie (deux membranes, crêtes, matrice), la membrane interne (double couche),
 * les protéines de la membrane, la sphère pédonculée, une solution dans un bécher, des levures, des molécules en billes.
 * La craie reste pour les légendes, les flèches, les axes : on peint d'abord le milieu, puis la craie par-dessus.
 *
 * Ce module ne fait que peindre, avec le contexte brut (`craie.ctx`, dans `craie.direct`). Un dégradé par objet,
 * jamais de boucle par pixel. Les petites granulations sont tirées d'un générateur déterministe : l'image ne
 * scintille pas d'une image à l'autre. Rien n'est hors programme : aucun nom de complexe, aucune molécule nommée.
 */
(function () {
  'use strict';
  /* 18 novembre 2026 (règle 15 du skill, lexique visuel commun) : la peinture de base (billes, liaisons, capsules, cellule,
   * mitochondrie, membrane, protéine, sphère pédonculée, bécher, levure, bulle, éclat) vient du module partagé
   * /media/simulations/shared/lexique/lexique.js, chargé AVANT ce fichier ; ici ne restent que les fonds et cartes du cours. */
  const L = window.Lexique;
  if (!L) throw new Error('Lexique manquant : charger /media/simulations/shared/lexique/lexique.js avant peinture.js');
  const TAU = Math.PI * 2, { T, graine, rgba, cellule, mitochondrie, cheminCretes, membrane, proteine, bille, liaison, capsule, spherePedonculee, becher, levure, bulleGaz, eclat } = L;

  /* ── Fonds et cartes communs (16 novembre 2026, refonte « un seul style agréable ») ── */
  const GR = (() => { const r = graine(77), out = []; for (let i = 0; i < 400; i++) out.push([r(), r(), .7 + r() * 1.6, r()]); return out; })();
  /** La matrice peinte : bleu lumineux doux, plus clair vers (cx, cy), granules clairs et quelques denses. */
  function fondMatrice(ctx, x, y, w, h, o = {}) {
    const cx = o.cx ?? x + w / 2, cy = o.cy ?? y + h / 2;
    ctx.save(); ctx.beginPath(); if (o.arrondi && ctx.roundRect) ctx.roundRect(x, y, w, h, o.arrondi); else ctx.rect(x, y, w, h); ctx.clip();
    const g = ctx.createRadialGradient(cx, cy, 20, cx + 60, cy + 30, Math.max(w, h) * .9);
    g.addColorStop(0, 'rgba(96,190,245,.62)'); g.addColorStop(.45, 'rgba(52,140,210,.50)'); g.addColorStop(1, 'rgba(22,72,128,.42)');
    ctx.fillStyle = g; ctx.fillRect(x, y, w, h);
    const n = Math.round(w * h / 1800);
    for (let i = 0; i < Math.min(n, GR.length); i++) {
      const [u, v, r, k] = GR[i]; ctx.fillStyle = k < .82 ? 'rgba(225,245,255,.22)' : 'rgba(20,60,110,.35)';
      ctx.beginPath(); ctx.arc(x + u * w, y + v * h, k < .82 ? r : r + 1.4, 0, TAU); ctx.fill();
    }
    ctx.restore();
  }
  /** Le hyaloplasme peint : vert d'eau lumineux, granules. */
  function fondHyalo(ctx, x, y, w, h, o = {}) {
    ctx.save(); ctx.beginPath(); if (o.arrondi && ctx.roundRect) ctx.roundRect(x, y, w, h, o.arrondi); else ctx.rect(x, y, w, h); ctx.clip();
    const g = ctx.createLinearGradient(x, y, x + w, y + h); g.addColorStop(0, rgba(T.hyalo, .40)); g.addColorStop(1, rgba(T.hyalo, .22));
    ctx.fillStyle = g; ctx.fillRect(x, y, w, h);
    const n = Math.round(w * h / 1600);
    for (let i = 0; i < Math.min(n, GR.length); i++) { const [u, v, r] = GR[GR.length - 1 - i]; ctx.fillStyle = 'rgba(210,240,200,.20)'; ctx.beginPath(); ctx.arc(x + u * w, y + v * h, r, 0, TAU); ctx.fill(); }
    ctx.restore();
  }
  /**
   * Une carte (tableau, compteur, bilan) : fond bleu nuit, bord doré, ombre douce ; o.entete = hauteur d'un en-tête doré
   * (le titre s'écrit dessus en sombre et gras) ; o.rayures = liste des y de lignes à éclaircir une sur deux (hauteur o.pas).
   */
  function carte(ctx, x, y, w, h, o = {}) {
    ctx.save();
    ctx.shadowColor = 'rgba(0,0,0,.45)'; ctx.shadowBlur = 14; ctx.shadowOffsetY = 5;
    const g = ctx.createLinearGradient(0, y, 0, y + h); g.addColorStop(0, `rgba(14,32,58,${o.alpha ?? .94})`); g.addColorStop(1, `rgba(8,22,42,${o.alpha ?? .94})`);
    ctx.fillStyle = g; ctx.beginPath(); if (ctx.roundRect) ctx.roundRect(x, y, w, h, o.arrondi ?? 16); else ctx.rect(x, y, w, h); ctx.fill(); ctx.shadowColor = 'transparent';
    ctx.save(); ctx.clip();
    if (o.entete) { const gh = ctx.createLinearGradient(0, y, 0, y + o.entete); gh.addColorStop(0, o.clair || '#fde68a'); gh.addColorStop(1, o.fonce || '#f59e0b'); ctx.fillStyle = gh; ctx.fillRect(x, y, w, o.entete); }
    if (o.rayures) { ctx.fillStyle = 'rgba(255,255,255,.05)'; o.rayures.forEach((yy, i) => { if (i % 2 === 0) ctx.fillRect(x, yy, w, o.pas || 30); }); }
    ctx.restore();
    ctx.lineWidth = 2; ctx.strokeStyle = o.bord || 'rgba(250,204,21,.85)'; ctx.beginPath(); if (ctx.roundRect) ctx.roundRect(x, y, w, h, o.arrondi ?? 16); else ctx.rect(x, y, w, h); ctx.stroke();
    ctx.restore();
  }
  /** Le CO₂ du lexique (O = C = O, carbone jaune) ; ancienne signature co2(ctx, x, y, k, a) gardée. */
  const co2 = (ctx, x, y, k = 1, a = 1) => L.co2(ctx, x, y, { echelle: k, alpha: a });

  window.SVTPeinture = { T, graine, rgba, cellule, mitochondrie, cheminCretes, membrane, proteine, bille, liaison, capsule, spherePedonculee, becher, levure, bulleGaz, eclat,
    fondMatrice, fondHyalo, carte, co2 };
})();

/* ── Mosaïque du tableau large (15 novembre 2026) : ici plutôt que dans un fichier à part (un nouveau .js de public/ n'est pas servi par le serveur de dev). ── */
/*
 * Mosaïque : une page dessinée pour le cadre 760 × 420 est rangée sur toute la largeur du tableau (15 novembre 2026,
 * « la simulation n'occupe qu'une bande étroite, les textes sont minuscules »).
 * Avec Scene(..., { large: true }), le cadre fait scene.L de large (≈ 1220 sur un portable 1366 × 613). La page est
 * découpée en blocs (rectangles du dessin d'origine) posés en colonnes, chacun agrandi autant que la hauteur le permet :
 * la figure prend toute la hauteur, les textes passent à côté, plus gros. Rien n'est redessiné autrement : chaque bloc
 * rejoue le dessin de la page sous une transformation (translation + échelle) avec une découpe, donc les repères pointés
 * par le tuteur (craie.repere lit la transformation du contexte) suivent tout seuls, et scene.local renvoie les
 * coordonnées d'origine (poignées, clics).
 *
 *   const MOS = SVTLarge.Mosaique(scene, (L) => L >= 1000 ? { colonnes: [[[0, 0, 470, 420]], [[470, 40, 290, 200], [470, 240, 290, 180]]] } : null);
 *   Scene(canvas, (c) => { scene.cadre(31); MOS.dessiner(c, () => dessiner(c)); return c.fin(); }, { large: true });
 *
 * Une colonne = liste de rectangles [x, y, w, h] empilés (même échelle dans la colonne) ; option par colonne
 * { blocs: [...], max: 1.6 } pour borner l'agrandissement ; `police: 1.15` grossit en plus les textes de la craie. Sous L < 1000 (grand écran, déjà haut) : dessin d'origine.
 */
(function () {
  'use strict';
  const VH = 420, ECART = 18, HAUT = 6;
  function Mosaique(scene, disposition) {
    let cleL = null, blocs = null;
    function calculer(L) {
      const d = disposition(L);
      if (!d) return null;
      if (d.blocs) {   // placement à la main : { src: [x, y, w, h], X, Y, s, police }
        const out = d.blocs.map(b => ({ x: b.src[0], y: b.src[1], w: b.src[2], h: b.src[3], X: b.X, Y: b.Y, s: b.s, police: b.police }));
        out.police = d.police || 1; return out;
      }
      if (d.lignes) return lignes(d, L);
      const cols = d.colonnes.map(c => (Array.isArray(c) ? { blocs: c } : c));
      const gap = d.ecart ?? ECART;
      for (const c of cols) {
        c.H = c.blocs.reduce((s, b) => s + b[3], 0);
        c.Wsrc = Math.max(...c.blocs.map(b => b[2]));
        c.s = Math.min(c.max ?? 2, (VH - 2 * HAUT - gap * (c.blocs.length - 1)) / c.H);
      }
      const libre = L - gap * (cols.length + 1);
      const somme = cols.reduce((s, c) => s + c.Wsrc * c.s, 0);
      if (somme > libre) for (const c of cols) c.s *= libre / somme;
      const total = cols.reduce((s, c) => s + c.Wsrc * c.s, 0);
      const g = (L - total) / (cols.length + 1);
      const out = []; let X = g;
      for (const c of cols) {
        const h = c.H * c.s + gap * (c.blocs.length - 1);
        let Y = (VH - h) / 2;
        for (const [x, y, w, hh] of c.blocs) {
          const cx = c.align === 'gauche' ? X : X + (c.Wsrc - w) * c.s / 2;
          out.push({ x, y, w, h: hh, X: cx, Y, s: c.s, police: c.police });
          Y += hh * c.s + gap;
        }
        X += c.Wsrc * c.s + g;
      }
      out.police = d.police || 1;
      return out;
    }
    /* Rangées : d.lignes = [[item, …], …] ; item = [x, y, w, h] ou { r: [x, y, w, h], k: 1.3, police } (k : agrandi
     * k fois plus que la rangée) ou { pile: [[x, y, w, h], …], k } (rectangles empilés). Une échelle par rangée, la plus
     * grande qui tient en largeur (bornée par d.max), puis toutes réduites ensemble pour tenir en hauteur. */
    function lignes(d, L) {
      const gap = d.ecart ?? ECART, out = [];
      const rows = d.lignes.map(row => row.map(it => {
        const o = Array.isArray(it) ? { r: it } : it, pile = o.pile || [o.r];
        return { pile, k: o.k || 1, police: o.police, w: Math.max(...pile.map(r => r[2])), h: pile.reduce((a, r) => a + r[3], 0) };
      }));
      for (const row of rows) {
        row.s = Math.min(d.max ?? 1.6, (L - gap * (row.length + 1)) / row.reduce((a, it) => a + it.w * it.k, 0));
        row.H = Math.max(...row.filter(it => it.k === 1).map(it => it.h * row.s), 0) || Math.max(...row.map(it => it.h * it.k * row.s));
      }
      const libre = VH - 2 * HAUT - gap * (rows.length - 1), tot = rows.reduce((a, r) => a + r.H, 0);
      if (tot > libre) for (const r of rows) { r.s *= libre / tot; r.H *= libre / tot; }
      let Y = (VH - rows.reduce((a, r) => a + r.H, 0) - gap * (rows.length - 1)) / 2;
      for (const row of rows) {
        for (const it of row) it.s = Math.min(row.s * it.k, row.H / it.h, (d.max ?? 1.6) * 1.2);   // un item agrandi reste dans la hauteur de sa rangée
        const larg = row.reduce((a, it) => a + it.w * it.s, 0), g = (L - larg) / (row.length + 1);
        let X = g;
        for (const it of row) {
          const s = it.s; let y = Y + (row.H - it.h * s) / 2;
          for (const [x0, y0, w, h] of it.pile) { out.push({ x: x0, y: y0, w, h, X: X + (it.w - w) * s / 2, Y: y, s, police: it.police }); y += h * s; }
          X += it.w * s + g;
        }
        Y += row.H + gap;
      }
      out.police = d.police || 1;
      return out;
    }
    function actuels() {
      if (scene.L !== cleL) { cleL = scene.L; blocs = calculer(scene.L); scene.sale = true; }
      return blocs;
    }
    const M = {
      actif: () => !!actuels(),
      blocs: () => actuels(),
      /** Dessine `fn` (le dessin d'origine) une fois par bloc, ou une seule fois sans mosaïque. */
      dessiner(c, fn) {
        const B = actuels();
        if (!B) {   // sans mosaïque : le dessin d'origine, centré dans le cadre (large : L un peu plus grand que 760)
          const dx = Math.max(0, (scene.L - 760) / 2); if (!dx) return fn();
          c.ctx.save(); c.ctx.translate(dx, 0); try { fn(); } finally { c.ctx.restore(); }
          if (c.tip) c.tip = [c.tip[0] + dx, c.tip[1]];
          return;
        }
        const ctx = c.ctx, cur0 = c.cur; let curMax = cur0, tip = null, complet = true;
        // police : les textes un peu plus gros que dans le dessin d'origine (la mosaïque leur laisse la place).
        const texte = c.texte, repere = c.repere, k = B.police;
        // Un repère est déclaré par le seul bloc qui en montre la plus grande part (le tuteur le pointe là).
        const part = (b, x, y, w, h) => Math.max(0, Math.min(b.x + b.w, x + w) - Math.max(b.x, x)) * Math.max(0, Math.min(b.y + b.h, y + h) - Math.max(b.y, y));
        let ici = null;
        c.repere = function (id, x, y, w, h, label) {
          const xa = Math.min(x, x + w), ya = Math.min(y, y + h), wa = Math.abs(w), ha = Math.abs(h);
          let m = -1, meilleur = null; for (const b of B) { const p = part(b, xa, ya, Math.max(wa, 1), Math.max(ha, 1)); if (p > m) { m = p; meilleur = b; } }
          if (meilleur !== ici) return this;
          return repere.call(this, id, x, y, w, h, label);
        };
        let kb = k; const e0 = c.echelle;   // le minimum lisible (15 px à l'écran) tient compte de l'échelle du bloc
        // une fraction « ⟦num|dén⟧ » s'écrit en morceaux qui repassent par c.texte : déjà à la bonne taille, ils ne sont pas regrossis
        c.texte = function (s, x, y, o = {}) {
          if (kb === 1 || this._dansFraction) return texte.call(this, s, x, y, o);
          const fr = String(s).includes('⟦'); if (fr) this._dansFraction = true;
          try { return texte.call(this, s, x, y, { ...o, taille: (o.taille ?? 18) * kb, max: o.max && o.max * kb }); } finally { if (fr) this._dansFraction = false; }
        };
        try { B.forEach((b, i) => {
          ici = b; kb = b.police ?? k; if (e0) c.echelle = e0 * b.s; c.cur = cur0; c.tip = null; c.complet = true; c.r = window.Tableau.graine(97 + 13 * i);
          ctx.save();
          ctx.translate(b.X, b.Y); ctx.scale(b.s, b.s); ctx.translate(-b.x, -b.y);
          ctx.beginPath(); ctx.rect(b.x, b.y, b.w, b.h); ctx.clip();
          try { fn(); } finally { ctx.restore(); }
          curMax = Math.max(curMax, c.cur); complet = complet && c.complet;
          if (c.tip) tip = [b.X + (c.tip[0] - b.x) * b.s, b.Y + (c.tip[1] - b.y) * b.s];
        }); } finally { c.texte = texte; c.repere = repere; c.echelle = e0; }
        c.cur = curMax; c.tip = tip; c.complet = complet;
      },
      /** Coordonnées du cadre large → coordonnées du dessin d'origine. */
      versOrigine(x, y) {
        const B = actuels(); if (!B) return [x - Math.max(0, (scene.L - 760) / 2), y];
        let best = null, dmin = Infinity;
        for (const b of B) {
          const x0 = b.X, y0 = b.Y, x1 = b.X + b.w * b.s, y1 = b.Y + b.h * b.s;
          const d = Math.hypot(Math.max(x0 - x, 0, x - x1), Math.max(y0 - y, 0, y - y1));
          if (d < dmin) { dmin = d; best = b; }
        }
        return [best.x + (x - best.X) / best.s, best.y + (y - best.Y) / best.s];
      },
    };
    const local0 = scene.local.bind(scene);
    scene.local = (x, y) => { const [a, b] = local0(x, y); return M.versOrigine(a, b); };
    return M;
  }
  window.SVTLarge = { Mosaique };
})();
