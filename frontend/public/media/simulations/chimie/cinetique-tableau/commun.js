/*
 * Commun aux simulations de la radioactivité (copie de ondes-lumineuses-tableau/commun.js) : cadre virtuel 760 × 420 mis à l'échelle sans
 * rien couper, texte jamais plus petit que 15 px à l'écran, boucle d'image qui
 * ne redessine que lorsqu'il le faut.
 */
(function () {
  'use strict';
  const VW = 760, VH = 420;
  /* Agrandissement du 15 novembre 2026 (« la simulation n'occupe qu'une bande étroite, les textes sont minuscules ») :
   *  - texte jamais plus petit que TAILLE_MIN px à l'écran (15 ; c'était 11) ;
   *  - Scene(canvas, dessiner, { large: true }) : le cadre prend le format du tableau, scene.L va de 760 à 760 × L_MAX
   *    (hauteur toujours 420) ; la page place ses blocs avec scene.L (figure à gauche, légende et calculs à droite)
   *    au lieu de les empiler. Sans `large`, un dessin prévu pour 760 × 420 est centré comme avant ;
   *  - { ajuster: true } : la boîte de l'encre de l'image complète (dessinée une fois, `complet(fn)` met la page à
   *    son état final le temps de fn) remplit le tableau, l'agrandissement est borné à ZOOM_MAX × le cadre entier ;
   *    scene.remesurer() après un changement de vue (la boîte ne fait que grandir). */
  const TAILLE_MIN = 15, L_MAX = 2.1, MARGE = 14, ZOOM_MAX = 2;
  function Scene(canvas, dessiner, options = {}) {
    // `scene` existe avant la craie : le premier redimensionnement la marque déjà « à redessiner ».
    const scene = { sale: true, boite: null, mesurant: false, L: VW };
    const craie = new window.Tableau.Craie(canvas, { onresize: () => { scene.sale = true; } });
    /* Plancher du texte gardé à 15 px à l'écran (18 novembre 2026, « le texte est plus grand que la simulation » : sur un
     * cadre de 230 px de haut, le kit réduisait le plancher jusqu'à 45 % et les étiquettes tombaient à ~9 px). Le kit
     * réduit toujours un plancher plus haut (18 → 15 sur un petit tableau), mais jamais sous TAILLE_MIN. */
    Object.defineProperty(craie, 'tailleMin', {
      configurable: true,
      get() {
        const brut = this._tailleMinBrut || 0;
        if (!brut) return brut;
        const f = Math.min(1, Math.max(.45, Math.min((this.W || 900) / 900, (this.H || 400) / 400)));
        // Très petit cadre (téléphone : le dessin de 760 de large réduit sous 0,55) : le plancher suit l'échelle, jamais
        // sous 11 px — à 15 px, les étiquettes d'un dessin prévu pour 760 × 420 se chevaucheraient.
        const s = Math.min((this.W || VW) / Math.max(VW, scene.L || VW), (this.H || VH) / VH);
        const plancher = s >= .55 ? TAILLE_MIN : Math.max(11, TAILLE_MIN * s / .55);
        const rendu = Math.max(Math.min(brut, plancher), brut * f);
        this._tailleMinLu = [brut, rendu];
        return rendu;
      },
      set(v) { const lu = this._tailleMinLu; this._tailleMinBrut = lu && v === lu[1] ? lu[0] : v; },
    });
    /* Courbes de graphe nettes et lumineuses (17 novembre 2026, « couleurs vives, facile à lire ») : une courbe tracée
     * par craie.courbe avec `net: true` garde son écriture progressive et sa durée (même longueur), mais sans tremblé,
     * avec un halo doux de sa couleur. Les autres courbes (flèches, cartes) restent à la craie. */
    const courbeCraie = craie.courbe;
    craie.courbe = function (fn, n, o = {}) {
      if (o.net !== true) return courbeCraie.call(this, fn, n, o);
      const ctx = this.ctx;
      ctx.save(); ctx.shadowColor = this.couleur(o.couleur); ctx.shadowBlur = o.pointille ? 5 : 10;
      try { return courbeCraie.call(this, fn, n, { ...o, tremble: 0 }); } finally { ctx.restore(); }
    };
    /* La boîte de l'encre (coordonnées du cadre) : l'image complète dessinée une fois, traits et textes relevés. */
    function mesurer() {
      const b = { x0: Infinity, y0: Infinity, x1: -Infinity, y1: -Infinity };
      const pt = (x, y, m = 0) => { if (!Number.isFinite(x) || !Number.isFinite(y)) return; b.x0 = Math.min(b.x0, x - m); b.y0 = Math.min(b.y0, y - m); b.x1 = Math.max(b.x1, x + m); b.y1 = Math.max(b.y1, y + m); };
      const { trait, texte, point } = craie;
      craie.trait = function (pts, o = {}) { const m = (o.largeur ?? 2.4) / 2 + 1; for (const p of pts || []) pt(p[0], p[1], m); return trait.call(this, pts, o); };
      craie.point = function (x, y, r = 4, c) { pt(x, y, r); return point.call(this, x, y, r, c); };
      craie.texte = function (s, x, y, o = {}) {
        const t = o.taille ?? 18; this.ctx.font = `${o.gras ? '700 ' : ''}${t}px ${window.Tableau.POLICE}`;
        let l = this.ctx.measureText(String(s).replace(/_/g, '')).width; if (o.max && l > o.max) l = o.max;
        const x0 = o.align === 'center' ? x - l / 2 : o.align === 'right' ? x - l : x;
        pt(x0, y - t * 0.95); pt(x0 + l, y + t * 0.35);
        return texte.call(this, s, x, y, o);
      };
      const t = scene.ouvert;
      scene.mesurant = true; scene.ouvert = -1e9;
      try { (options.complet || (f => f()))(() => dessiner(craie, scene)); } catch (e) { console.warn('[tableau] mesure de la boîte', e); }
      finally {
        // On rend la main au prototype (pas une copie figée) : une écriture installée plus tard (états physiques) s'applique aussi.
        for (const [k, f] of [['trait', trait], ['texte', texte], ['point', point]]) { if (f === Object.getPrototypeOf(craie)[k]) delete craie[k]; else craie[k] = f; }
        scene.mesurant = false; scene.ouvert = t;
      }
      if (!(b.x1 > b.x0 && b.y1 > b.y0)) return null;
      const n = { x0: Math.max(0, b.x0 - MARGE), y0: Math.max(0, b.y0 - MARGE), x1: Math.min(scene.L, b.x1 + MARGE), y1: Math.min(VH, b.y1 + MARGE) };
      const a = scene.boite;
      return a ? { x0: Math.min(a.x0, n.x0), y0: Math.min(a.y0, n.y0), x1: Math.max(a.x1, n.x1), y1: Math.max(a.y1, n.y1) } : n;
    }
    Object.assign(scene, {
      craie, sale: true, ouvert: performance.now(), s: 1, ox: 0, oy: 0, VH,
      /** Prépare l'image : écriture en direct depuis l'ouverture, puis cadre mis à l'échelle. */
      cadre(graine = 7) {
        const W = craie.W, H = craie.H;
        const L = options.large ? Math.round(Math.min(VW * L_MAX, Math.max(VW, VH * W / Math.max(1, H)))) : VW;
        if (L !== scene.L) { scene.L = L; scene.boite = null; }
        if (options.ajuster && !scene.mesurant && !scene.boite && W > 1) scene.boite = mesurer();
        craie.debut(graine, (performance.now() - scene.ouvert) / 1000);
        if (scene.mesurant) { scene.s = 1; scene.ox = 0; scene.oy = 0; craie.echelle = 1; craie.tailleMin = 0; craie.cadre = null; return craie; }
        const k = scene.boite || { x0: 0, y0: 0, x1: L, y1: VH };
        const sCadre = Math.min(W / L, H / VH), bw = k.x1 - k.x0, bh = k.y1 - k.y0;
        const s = Math.min(W / bw, H / bh, sCadre * ZOOM_MAX);
        scene.s = s; scene.ox = (W - bw * s) / 2 - k.x0 * s; scene.oy = (H - bh * s) / 2 - k.y0 * s;
        craie.ctx.translate(scene.ox, scene.oy); craie.ctx.scale(s, s);
        craie.echelle = s; craie.tailleMin = TAILLE_MIN;
        craie.cadre = { w: L, h: VH, haut: 0 };    // tout texte reste dans le cadre du dessin (rien de coupé au bord)
        return craie;
      },
      /** La construction a changé de forme (réglage, vue) : la boîte sera remesurée (elle ne fait que grandir). */
      remesurer() { if (options.ajuster) { const n = mesurer(); if (n) scene.boite = n; scene.sale = true; } },
      /** Coordonnées CSS du canvas → coordonnées du dessin. */
      local(x, y) { return [(x - scene.ox) / scene.s, (y - scene.oy) / scene.s]; },
      reecrire() { scene.ouvert = performance.now(); scene.sale = true; },
      /** L'image complète de la scène (tout écrit, d'un coup), en PNG : pour imprimer ou télécharger. */
      image() {
        const t = scene.ouvert; scene.ouvert = -1e9;
        try { dessiner(craie, scene); return canvas.toDataURL('image/png'); } finally { scene.ouvert = t; scene.sale = true; }
      },
    });
    let avant = performance.now();
    // Première image au prochain rafraîchissement : la page a fini de déclarer sa scène.
    requestAnimationFrame(function image(maintenant) {
      const dt = Math.min(0.1, Math.max(0, (maintenant - avant) / 1000)); avant = maintenant;
      const anime = scene.avancer ? scene.avancer(dt) : false;
      if ((scene.sale || anime) && craie.W > 1) scene.sale = !dessiner(craie, scene);
      requestAnimationFrame(image);
    });
    return scene;
  }
  window.OndesTableau = { Scene, VW, VH };
})();

/*
 * Rendu peint commun du dossier (16 novembre 2026 : « des animations plus réalistes, plus attractives, avec de belles couleurs ») :
 * molécules et ions en sphères ombrées aux couleurs habituelles (H blanc, O rouge, C noir, N bleu, I violet, Na violet clair,
 * Cl vert, Cu orangé), lentille de loupe, fiole jaugée et petit flacon en verre peint, éclair d'un choc efficace, glissements
 * adoucis. Peint sur c.ctx dans c.direct, SOUS la craie : la craie garde les légendes, les flèches et les écritures.
 *   Rendu.atome(ctx, x, y, r, el, a)            une sphère ombrée de l'élément el ('H', 'O', 'C', 'N', 'I', 'Na', 'Cl', 'Cu', 'Zn', 'Hp' = H⁺ jaune).
 *   Rendu.molecule(ctx, nom, x, y, k, ang, a)   un modèle moléculaire (voir MODELES) centré en x, y ; k : échelle (1 ≈ 12 px), ang : rotation.
 *   Rendu.lentille(ctx, cx, cy, r, teinte)       le fond de la loupe (solution vue de très près), à peindre avant les molécules.
 *   Rendu.choc(ctx, x, y, r, a)                  l'éclair d'un choc efficace (étoile jaune-blanc qui s'efface).
 *   Rendu.fiole(ctx, cx, yHaut, yBas, R, o)       fiole jaugée : col, trait de jauge, panse ; o = { surface, liquide: [r, g, b, a], bouchon }.
 *   Rendu.flacon(ctx, x, y, w, h, col, a)        petit flacon de verre (pilulier) contenant une solution de couleur col [r, g, b, a].
 *   Rendu.doux(p)                                p (0 → 1) adouci : départ et arrivée en douceur.
 */
(function () {
  'use strict';
  const rgba = (c, a) => `rgba(${Math.round(c[0])},${Math.round(c[1])},${Math.round(c[2])},${a})`;
  const clair = (c, k) => c.map(v => v + (255 - v) * k);
  const fonce = (c, k) => c.map(v => v * k);
  /* Couleurs des atomes : celles du lexique visuel commun du site (docs/lexique-visuel/, 18 novembre 2026) — C jaune (le
   * carbone du glucose, dans toutes les matières), H blanc, O rouge, H⁺ rose (le proton) ; le soufre en ocre, pour ne pas
   * prendre le jaune du carbone. */
  const EL = {
    H: { c: [235, 240, 245], r: 3.3 }, Hp: { c: [244, 114, 182], r: 3.5 }, O: { c: [235, 85, 70], r: 5.2 }, C: { c: [250, 204, 21], r: 5.4 },
    N: { c: [59, 102, 236], r: 5.3 }, I: { c: [134, 72, 228], r: 7.4 }, Na: { c: [171, 120, 242], r: 6 }, Cl: { c: [74, 196, 98], r: 6.6 },
    Cu: { c: [205, 112, 52], r: 6 }, Zn: { c: [168, 178, 190], r: 6 }, S: { c: [196, 156, 70], r: 6.2 }, Fe: { c: [224, 130, 60], r: 6 }, Mn: { c: [156, 84, 190], r: 6 },
    Al: { c: [190, 196, 206], r: 6 }, K: { c: [143, 64, 212], r: 7 },
  };
  /** Une sphère ombrée : reflet net en haut à gauche, cœur coloré, bord sombre, petite ombre portée. */
  function atome(ctx, x, y, r, el, a = 1) {
    const e = EL[el] || { c: el, r }, c = e.c;
    ctx.save(); ctx.globalAlpha *= a;
    ctx.fillStyle = 'rgba(0,0,0,.22)'; ctx.beginPath(); ctx.ellipse(x + r * .18, y + r * .32, r * 1.02, r * .98, 0, 0, Math.PI * 2); ctx.fill();
    const g = ctx.createRadialGradient(x - r * .38, y - r * .42, r * .08, x, y, r * 1.02);
    g.addColorStop(0, rgba(clair(c, .82), 1)); g.addColorStop(.28, rgba(clair(c, .25), 1)); g.addColorStop(.7, rgba(c, 1)); g.addColorStop(1, rgba(fonce(c, .42), 1));
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = 'rgba(255,255,255,.55)'; ctx.beginPath(); ctx.ellipse(x - r * .36, y - r * .42, r * .26, r * .16, -.6, 0, Math.PI * 2); ctx.fill();
    ctx.restore();
  }
  /* Modèles (positions en px pour k = 1, z pour l'ordre de peinture : le plus petit est peint d'abord, derrière). */
  const MODELES = {
    H2O: [['O', 0, 0, 0], ['H', -5.6, 3.8, 1], ['H', 5.6, 3.8, 1]],
    H3O: [['O', 0, 0, 0], ['H', -5.8, 3.4, 1], ['H', 5.8, 3.4, 1], ['H', 0, -6.2, -1]],
    HO: [['O', 0, 0, 0], ['H', 5.4, -3.4, 1]],
    H2O2: [['O', -3.6, 0, 0], ['O', 3.6, 0, 0], ['H', -6.8, 4.6, 1], ['H', 6.8, -4.6, 1]],
    I: [['I', 0, 0, 0]], I2: [['I', -5.2, 0, 0], ['I', 5.2, 0, 1]],
    Na: [['Na', 0, 0, 0]], Cl: [['Cl', 0, 0, 0]], Cu: [['Cu', 0, 0, 0]], Zn: [['Zn', 0, 0, 0]], Hp: [['Hp', 0, 0, 0]],
    NH3: [['N', 0, 0, 0], ['H', -5.8, 3.2, 1], ['H', 5.8, 3.2, 1], ['H', 0, -6.2, -1]],
    NH4: [['N', 0, 0, 0], ['H', -5.8, 3.6, 1], ['H', 5.8, 3.6, 1], ['H', -3, -5.6, -1], ['H', 3.4, -5.4, 1]],
    /* L'acide éthanoïque : CH₃ à gauche, C du groupe carboxyle, =O en haut, –O–H à droite (le H acide en rose, la couleur du H⁺ : c'est lui qui part). */
    CH3COOH: [['H', -12.6, -3.6, -1], ['H', -12.2, 4.6, 1], ['H', -8.2, -6.6, -1], ['C', -6.6, .4, 0], ['C', 2.6, .4, 0], ['O', 6.4, -6.8, 1], ['O', 8.6, 4.6, 1], ['Hp', 13.6, 3.2, 2]],
    CH3COO: [['H', -12.6, -3.6, -1], ['H', -12.2, 4.6, 1], ['H', -8.2, -6.6, -1], ['C', -6.6, .4, 0], ['C', 2.6, .4, 0], ['O', 6.4, -6.8, 1], ['O', 8.6, 4.6, 1]],
    HCOOH: [['H', -6.6, 2.8, -1], ['C', -1.6, .4, 0], ['O', 2.2, -6.8, 1], ['O', 4.4, 4.6, 1], ['Hp', 9.4, 3.2, 2]],
    S2O3: [['S', -3, 0, 0], ['S', 6, -2, 1], ['O', -8, -4, 1], ['O', -6, 6, 1], ['O', -1, -7, -1]],
  };
  /** Un modèle moléculaire peint (nom : clé de MODELES, sans charge : 'H3O' pour H₃O⁺, 'HO' pour HO⁻, 'CH3COO' pour CH₃COO⁻). */
  function molecule(ctx, nom, x, y, k = 1, ang = 0, a = 1, o = {}) {
    const m = MODELES[nom]; if (!m || !(a > 0)) return;
    const co = Math.cos(ang), si = Math.sin(ang);
    const pts = m.map(([el, dx, dy, z], i) => ({ el: o.sansProton && el === 'Hp' ? null : (o.hBlanc && el === 'Hp' ? 'H' : el), x: x + (dx * co - dy * si) * k, y: y + (dx * si + dy * co) * k, z, i }))
      .filter(p => p.el).sort((p, q) => p.z - q.z || p.i - q.i);
    for (const p of pts) atome(ctx, p.x, p.y, (EL[p.el]?.r ?? 5) * k, p.el, a);
  }
  /** Fond de loupe : la solution vue de très près (légère teinte), assombrie au bord, reflet en croissant. */
  function lentille(ctx, cx, cy, r, teinte = [150, 190, 225]) {
    ctx.save();
    const g = ctx.createRadialGradient(cx - r * .25, cy - r * .3, r * .1, cx, cy, r);
    g.addColorStop(0, rgba(clair(teinte, .35), .2)); g.addColorStop(.75, rgba(teinte, .13)); g.addColorStop(1, rgba(fonce(teinte, .5), .3));
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = 'rgba(255,255,255,.16)'; ctx.lineWidth = Math.max(3, r * .06); ctx.lineCap = 'round';
    ctx.beginPath(); ctx.arc(cx, cy, r * .82, Math.PI * 1.1, Math.PI * 1.4); ctx.stroke();
    ctx.restore();
  }
  /** L'éclair d'un choc efficace : étoile jaune-blanc à huit branches, a de 1 (choc) à 0 (effacé). */
  function choc(ctx, x, y, r = 9, a = 1) {
    if (!(a > 0)) return;
    ctx.save(); ctx.globalAlpha *= a;
    const g = ctx.createRadialGradient(x, y, 0, x, y, r * 1.6); g.addColorStop(0, 'rgba(255,255,230,.95)'); g.addColorStop(.35, 'rgba(253,224,71,.55)'); g.addColorStop(1, 'rgba(253,224,71,0)');
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r * 1.6, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = 'rgba(255,250,200,.95)'; ctx.beginPath();
    for (let i = 0; i < 16; i++) { const an = i * Math.PI / 8, rr = i % 2 ? r * .32 : (i % 4 ? r * .8 : r * 1.15); ctx.lineTo(x + Math.cos(an) * rr, y + Math.sin(an) * rr); }
    ctx.closePath(); ctx.fill(); ctx.restore();
  }
  /** Verre : contour clair, reflet vertical. */
  function verre(ctx, chemin, x, y, h) {
    ctx.strokeStyle = 'rgba(225,240,252,.85)'; ctx.lineWidth = 1.8; chemin(); ctx.stroke();
    const g = ctx.createLinearGradient(x, 0, x + 8, 0); g.addColorStop(0, 'rgba(255,255,255,.42)'); g.addColorStop(1, 'rgba(255,255,255,0)');
    ctx.fillStyle = g; ctx.fillRect(x, y, 8, h);
  }
  /** Fiole jaugée : col étroit (cx, yHaut → yCol), trait de jauge, panse ronde de rayon R posée sur yBas. */
  function fiole(ctx, cx, yHaut, yBas, R, o = {}) {
    const lc = Math.max(5, R * .17), cy = yBas - R * .92, yCol = cy - R * .86, a = o.a ?? 1;
    ctx.save(); ctx.globalAlpha *= a;
    const forme = () => {
      ctx.beginPath(); ctx.moveTo(cx - lc, yHaut); ctx.lineTo(cx - lc, yCol);
      ctx.bezierCurveTo(cx - lc, yCol + R * .3, cx - R, cy - R * .55, cx - R, cy + R * .05);
      ctx.bezierCurveTo(cx - R, yBas - R * .12, cx - R * .55, yBas, cx, yBas);
      ctx.bezierCurveTo(cx + R * .55, yBas, cx + R, yBas - R * .12, cx + R, cy + R * .05);
      ctx.bezierCurveTo(cx + R, cy - R * .55, cx + lc, yCol + R * .3, cx + lc, yCol); ctx.lineTo(cx + lc, yHaut);
    };
    ctx.fillStyle = 'rgba(0,0,0,.28)'; ctx.beginPath(); ctx.ellipse(cx + 3, yBas + 3, R * .8, 4, 0, 0, Math.PI * 2); ctx.fill();
    forme(); ctx.fillStyle = 'rgba(190,220,240,.08)'; ctx.fill();
    if (o.surface != null && o.liquide) {
      const [r, g, b, al] = o.liquide, ys = Math.max(yHaut + 4, o.surface);
      ctx.save(); forme(); ctx.closePath(); ctx.clip();
      const gr = ctx.createLinearGradient(cx - R, 0, cx + R, 0);
      gr.addColorStop(0, rgba(fonce([r, g, b], .62), Math.min(1, al + .15))); gr.addColorStop(.4, rgba(clair([r, g, b], .15), al)); gr.addColorStop(1, rgba(fonce([r, g, b], .6), Math.min(1, al + .15)));
      ctx.fillStyle = gr; ctx.fillRect(cx - R - 2, ys, 2 * R + 4, yBas - ys + 2);
      ctx.restore();
      const lw = ys < yCol ? lc : R * .9;
      ctx.fillStyle = rgba(clair([r, g, b], .4), Math.min(1, al + .1)); ctx.beginPath(); ctx.ellipse(cx, ys, lw - 1, ys < yCol ? 1.6 : 3, 0, 0, Math.PI * 2); ctx.fill();
    }
    ctx.strokeStyle = 'rgba(225,240,252,.85)'; ctx.lineWidth = 1.8; ctx.lineJoin = 'round'; forme(); ctx.stroke();
    // Reflets : un long sur la panse, un fin sur le col.
    ctx.strokeStyle = 'rgba(255,255,255,.4)'; ctx.lineWidth = 3; ctx.lineCap = 'round';
    ctx.beginPath(); ctx.arc(cx, cy + R * .05, R * .74, Math.PI * 1.05, Math.PI * 1.38); ctx.stroke();
    ctx.lineWidth = 1.4; ctx.beginPath(); ctx.moveTo(cx - lc + 2.4, yHaut + 6); ctx.lineTo(cx - lc + 2.4, yCol - 4); ctx.stroke();
    // Trait de jauge (gravé tout autour du col) et col évasé.
    const yj = o.jauge ?? (yHaut + (yCol - yHaut) * .45);
    ctx.strokeStyle = 'rgba(240,248,255,.95)'; ctx.lineWidth = 1.6; ctx.beginPath(); ctx.ellipse(cx, yj, lc + 1.5, 2, 0, 0, Math.PI * 2); ctx.stroke();
    ctx.lineWidth = 2; ctx.beginPath(); ctx.ellipse(cx, yHaut, lc + 1.6, 1.8, 0, 0, Math.PI * 2); ctx.stroke();
    if (o.bouchon) {
      const g = ctx.createLinearGradient(cx - lc - 3, 0, cx + lc + 3, 0); g.addColorStop(0, '#2a6f97'); g.addColorStop(.45, '#5fb3e0'); g.addColorStop(1, '#1d4f6e');
      ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(cx - lc - 2.5, yHaut - 10, 2 * lc + 5, 12, 3); ctx.fill();
    }
    ctx.restore();
    return { yCol, cy };
  }
  /** Petit flacon (pilulier) : verre épais, solution colorée col [r, g, b, a] au deux tiers, bouchon. */
  function flacon(ctx, x, y, w, h, col, a = 1) {
    ctx.save(); ctx.globalAlpha *= a;
    const yb = y + h, yg = y + 9;
    ctx.fillStyle = 'rgba(0,0,0,.28)'; ctx.beginPath(); ctx.ellipse(x + w / 2 + 3, yb + 2, w * .52, 3.5, 0, 0, Math.PI * 2); ctx.fill();
    const corps = () => { ctx.beginPath(); ctx.roundRect(x, yg, w, yb - yg, [4, 4, 9, 9]); };
    corps(); ctx.fillStyle = 'rgba(190,220,240,.1)'; ctx.fill();
    if (col) {
      const ys = yg + (yb - yg) * .3, [r, g, b, al] = col;
      ctx.save(); corps(); ctx.clip();
      const gr = ctx.createLinearGradient(x, 0, x + w, 0);
      gr.addColorStop(0, rgba(fonce([r, g, b], .65), Math.min(1, al + .12))); gr.addColorStop(.42, rgba(clair([r, g, b], .18), al)); gr.addColorStop(1, rgba(fonce([r, g, b], .62), Math.min(1, al + .12)));
      ctx.fillStyle = gr; ctx.fillRect(x, ys, w, yb - ys); ctx.restore();
      ctx.fillStyle = rgba(clair([r, g, b], .4), Math.min(1, al + .1)); ctx.beginPath(); ctx.ellipse(x + w / 2, ys, w / 2 - 2, 2.6, 0, 0, Math.PI * 2); ctx.fill();
    }
    ctx.strokeStyle = 'rgba(225,240,252,.85)'; ctx.lineWidth = 1.8; corps(); ctx.stroke();
    const gl = ctx.createLinearGradient(x + 3, 0, x + 11, 0); gl.addColorStop(0, 'rgba(255,255,255,.45)'); gl.addColorStop(1, 'rgba(255,255,255,0)');
    ctx.fillStyle = gl; ctx.fillRect(x + 3, yg + 5, 8, yb - yg - 12);
    const gb = ctx.createLinearGradient(0, y, 0, yg + 1); gb.addColorStop(0, '#5b6673'); gb.addColorStop(1, '#2c333a');
    ctx.fillStyle = gb; ctx.beginPath(); ctx.roundRect(x + w * .14, y, w * .72, yg - y + 1, 3); ctx.fill();
    ctx.restore();
  }
  /** Barre de diagramme peinte : dégradé de la couleur de craie `nom` (ou [r, g, b]), reflet à gauche, plus sombre en bas. */
  function barre(c, x, y, w, h, nom, a = 1) {
    if (!(h > .5) || !(w > .5)) return;
    let col = nom;
    if (!Array.isArray(col)) { const s = c.couleur(nom); if (s[0] === '#') { const n = parseInt(s.slice(1), 16); col = [n >> 16 & 255, n >> 8 & 255, n & 255]; } else col = (s.match(/[\d.]+/g) || [200, 200, 200]).slice(0, 3).map(Number); }
    const ctx = c.ctx; ctx.save(); ctx.globalAlpha *= a;
    const g = ctx.createLinearGradient(x, 0, x + w, 0);
    g.addColorStop(0, rgba(fonce(col, .62), .9)); g.addColorStop(.3, rgba(clair(col, .28), .9)); g.addColorStop(.55, rgba(col, .9)); g.addColorStop(1, rgba(fonce(col, .5), .9));
    ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(x, y, w, h, Math.min(3, w / 2, h / 2)); ctx.fill();
    const v = ctx.createLinearGradient(0, y, 0, y + h); v.addColorStop(0, 'rgba(255,255,255,.18)'); v.addColorStop(.25, 'rgba(255,255,255,0)'); v.addColorStop(1, 'rgba(0,0,0,.22)');
    ctx.fillStyle = v; ctx.fill(); ctx.restore();
  }
  const doux = p => { p = Math.min(1, Math.max(0, p)); return p < .5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2; };
  window.Rendu = { EL, MODELES, atome, molecule, lentille, choc, fiole, flacon, barre, doux, rgba };
})();

/*
 * États physiques dans les équations (règle du 16 novembre 2026 : « ajouter dans les équations l'état physique de chaque
 * élément », comme HCOOH(aq) + H₂O(l) ⇌ HCOO⁻(aq) + H₃O⁺(aq)). Au tableau seulement : la voix, la bulle et l'état envoyé
 * au tuteur gardent les équations sans états. Chaque espèce d'une équation (deux côtés autour de →, ⇌, ←) reçoit son
 * état, écrit en petit et en bas : H₂O (l) ; ions, molécules dissoutes (aq) ; métaux et précipités (s) ; H₂, HCl (g) ;
 * estérification (pas d'ion, un alcool ou un ester) : tout (l). e⁻, Ox, Red et les lettres A, C, D restent sans état.
 * La durée d'écriture reste celle de l'équation sans états : les instants des moments ne bougent pas.
 *   Etats.annote(s) : le texte avec les états (« (aq) ») ; Etats.cotes(gauche, droite) : deux côtés dessinés à part ;
 *   Etats.morceaux(liste) : une ligne à morceaux [côté, '⇌', côté…].
 */
(function () {
  'use strict';
  const T = window.Tableau; if (!T || T.Craie.__etats) return;
  const C = T.Craie, P = C.prototype; C.__etats = true;
  const SOLIDES = new Set(['Cu', 'Zn', 'Mg', 'Al', 'Ag', 'Fe', 'Pb', 'Ni', 'Sn', 'AgCl', 'CaF₂', 'Pt']);
  const GAZ = new Set(['H₂', 'O₂', 'Cl₂', 'HCl']);
  const EXCLUS = new Set(['A', 'C', 'D', 'I', 'Ox', 'Red', 'Réd']);
  const ETAT = String.raw`\((?:aq|l|s|g)\)`, FL = '(?:→|⇌|⇄|⇋|←)';
  const ESPECE = String.raw`(?:\((?:CH₃|C₂H₅)\)[₀-₉]*)?[A-Z](?:[A-Za-z₀-₉()–\-]*?[₀-₉A-Za-z)])?(?:[⁰¹²³⁴⁵⁶⁷⁸⁹]*[⁺⁻])?|e⁻`;
  const TERME = String.raw`(?:\d+\s?)?(?:${ESPECE})(?:\s?${ETAT})?`;
  const COTE = String.raw`${TERME}(?:\s*\+\s*${TERME})*`;
  const EQ = new RegExp(String.raw`(?<![\w₀-₉⁺⁻\[/])(${COTE})(\s*${FL}\s*)(${COTE})(?![\w₀-₉⁺⁻\]/·])`, 'g');
  const RE_COTE = new RegExp(`^${COTE}$`), RE_TERME = new RegExp(String.raw`^(\d+\s?)?(.*?)(\s?${ETAT})?$`);
  const decoupe = s => s.split(/\s*\+\s*/);
  const formule = t => { const m = t.trim().match(RE_TERME); return [m[1] || '', m[2], m[3] || '']; };
  const ion = f => /[⁺⁻]$/.test(f) && f !== 'e⁻';
  function etat(f, eq, ester) {
    if (f === 'e⁻') return '';
    if (EXCLUS.has(f)) return null;
    if (f === 'H₂O' || ester) return '(l)';
    if (ion(f)) return '(aq)';
    if (SOLIDES.has(f)) return '(s)';
    if (GAZ.has(f)) return '(g)';
    if (f === 'B' && !eq.includes('H₂O')) return null;
    return '(aq)';
  }
  function annoteEq(g, fl, d) {
    const eq = g + fl + d, fs = decoupe(g).concat(decoupe(d)).map(t => formule(t)[1]);
    if (fs.some(f => EXCLUS.has(f))) return null;
    const ions = fs.some(ion), ester = !ions && fs.some(f => /COO[A-Z(]|OH$/.test(f) && !f.endsWith('COOH'));
    const cote = s => {
      const out = [];
      for (const t of s.split(/(\s*\+\s*)/)) {
        if (/^\s*\+\s*$/.test(t)) { out.push(t); continue; }
        const [k, f, e] = formule(t);
        if (e) { out.push(t); continue; }
        const st = etat(f, eq, ester); if (st == null) return null;
        out.push(k + f + st);
      }
      return out.join('');
    };
    const a = cote(g), b = cote(d);
    return a == null || b == null ? null : a + fl + b;
  }
  const annote = s => String(s).replace(EQ, (m, g, fl, d) => annoteEq(g, fl, d) ?? m);
  /** Deux côtés dessinés à part (fonctions eqn, eqf de la page) : annotés ensemble, rendus séparés. */
  let pret = false;   // rien n'est annoté avant que la page soit chargée (sa mesure des durées se fait sans les états)
  const VUS = new Map(), ORIG = new Map();   // côté d'origine → côté annoté ; annoté → d'origine (durée d'écriture inchangée)
  const retiens = (o, a) => { if (a !== o) { VUS.set(o, a); ORIG.set(a, o); } return a; };
  function cotes(g, d) {
    if (!pret || typeof g !== 'string' || typeof d !== 'string' || !RE_COTE.test(g.trim()) || !RE_COTE.test(d.trim())) return [g, d];
    const r = annoteEq(g, ' → ', d); if (!r) return [g, d];
    const i = r.lastIndexOf(' → ');
    return [retiens(g, r.slice(0, i)), retiens(d, r.slice(i + 3))];
  }
  const piece = p => (typeof p === 'string' && VUS.has(p) ? VUS.get(p) : p);
  /** Ligne à morceaux : autour de chaque flèche, les morceaux voisins (côtés entiers « A + B », ou termes un à un
   *  « A », « + », « B ») forment l'équation ; chaque morceau reçoit les états de ses espèces. */
  function morceaux(liste) {
    if (!pret || !Array.isArray(liste)) return liste;
    const out = liste.slice(), estF = p => /^(→|⇌|←)$/.test(p), ok = p => typeof p === 'string' && (p.trim() === '+' || RE_COTE.test(p.trim()));
    out.forEach((p, i) => {
      if (!estF(p)) return;
      let a = i, b = i;
      while (a - 1 >= 0 && ok(out[a - 1]) && !estF(out[a - 1])) a--;
      while (b + 1 < out.length && ok(out[b + 1]) && !estF(out[b + 1])) b++;
      if (a === i || b === i) return;
      const g = out.slice(a, i).join(' ').replace(/\s*\+\s*/g, ' + '), d = out.slice(i + 1, b + 1).join(' ').replace(/\s*\+\s*/g, ' + ');
      if (!RE_COTE.test(g.trim()) || !RE_COTE.test(d.trim())) return;
      const r = annoteEq(g.trim(), ' → ', d.trim()); if (!r) return;
      const k = r.lastIndexOf(' → '), termes = decoupe(r.slice(0, k)).concat(decoupe(r.slice(k + 3)));
      let n = 0;
      for (let m = a; m <= b; m++) {
        if (m === i) continue;
        const q = out[m]; if (q.trim() === '+') continue;
        const nb = decoupe(q.trim()).length, part = termes.slice(n, n + nb).join(' + '); n += nb;
        out[m] = retiens(q, nb === 1 ? q.replace(q.trim(), part) : part);
      }
    });
    return out;
  }
  /** Liste de termes d'une équation (« H₂O₂ », « + », « ⇌ »…) : l'état de chaque terme (« (aq) », ou ''), ou null. */
  function liste(txts) {
    if (!pret) return null;
    const s = txts.join(' '), a = annote(s); if (a === s) return null;
    const b = a.split(' '); if (b.length !== txts.length) return null;
    return b.map((t, i) => t.slice(txts[i].length));
  }
  /** Ajoute un état au dernier morceau d'un terme (« H₂O » → « H₂O_{(l)} ») ; sa durée d'écriture reste celle de « H₂O ». */
  const ajoute = (p, e) => retiens(p, p + '_{' + e + '}');
  /** « X(aq) » écrit en petit et en bas : « X_{(aq)} ». */
  const marque = s => String(s).replace(new RegExp(`(?<=[A-Za-z₀-₉⁺⁻)}])\\s?(${ETAT})`, 'g'), '_{$1}');
  const plain = s => String(s).replace(/[_^]\{([^}]*)\}/g, '$1').replace(/[_^]/g, '').length;
  /** Largeur approchée d'un texte annoté (états en petit). */
  function largeur(ctx, s, taille) {
    ctx.font = `${taille}px ${T.POLICE}`;
    const etats = (String(s).match(new RegExp(ETAT, 'g')) || []).join('');
    return ctx.measureText(String(s).replace(new RegExp(ETAT, 'g'), '').replace(/[_^{}]/g, '')).width + ctx.measureText(etats).width * .62;
  }
  /** Équation en deux côtés (eqn, eqf) : taille réduite si, avec les états, elle sortirait du cadre. */
  function ajuste(c, x, g, d, o = {}, fl = 56) {
    const k = c.cadre; if (!k || typeof g !== 'string' || typeof d !== 'string' || !/\((?:aq|l|s|g)\)/.test(g + d)) return o;
    const t = o.taille ?? 17, w = largeur(c.ctx, g, t) + largeur(c.ctx, d, t) + fl;
    const x0 = o.align === 'center' ? x - w / 2 : o.align === 'right' ? x - w : x, x1 = x0 + w;
    const place = o.align === 'center' ? 2 * Math.min(x - 4, k.w - 4 - x) : o.align === 'right' ? x - 4 : k.w - 4 - x;
    return x1 > k.w - 4 || x0 < 4 ? { ...o, taille: Math.max(12, t * Math.min(1, (place - fl) / (w - fl))) } : o;
  }
  window.Etats = { annote, cotes, morceaux, piece, liste, ajoute, ajuste, marque };

  /* Indice « _{…} » derrière n'importe quel caractère (« H₃O⁺_{(aq)} ») : le kit ne le découpe que derrière une lettre. */
  const segKit = C.segments;
  C.segments = function (s) {
    const out = [], re = /(^|[^A-Za-zτθΔλωφ])_\{([^}]+)\}/g; let i = 0, m;
    while ((m = re.exec(s))) { if (m.index + m[1].length > i) out.push(...segKit(s.slice(i, m.index + m[1].length))); out.push({ t: m[2], sub: true }); i = re.lastIndex; }
    if (i < s.length) out.push(...segKit(s.slice(i)));
    return out;
  };
  const texteKit = P.texte;
  P.texte = function (s, x, y, o = {}) {
    s = String(s);
    if (!/(^|[^A-Za-zτθΔλωφ])_\{/.test(s) || /\^|[⁻⁰¹²³⁴⁵⁶⁷⁸⁹]/.test(s)) return texteKit.call(this, s, x, y, o);
    let taille = o.taille ?? 18;
    this.ctx.font = `${o.gras ? '700 ' : ''}${taille}px ${T.POLICE}`;
    this._verifierCadre(s.replace(/[_{}]/g, ''), x, y, taille, o.align);
    if (this.echelle && this.tailleMin) taille = Math.max(taille, this.tailleMin / this.echelle);
    return this._texteIndices(s, x, y, o, taille);
  };
  /* Une fois la page chargée (ses propres écritures chimiques installées), la couche la plus haute ajoute les états. */
  function installer() {
    pret = true;
    const avant = P.texte;
    P.texte = function (s, x, y, o = {}) {
      s = String(s);
      if (/^_\{\((?:aq|l|s|g)\)\}$/.test(s)) return avant.call(this, s, x, y, { ...o, duree: .001 });   // un état seul (pages à termes)
      const a = annote(s);
      if (a === s && !/\((?:aq|l|s|g)\)/.test(a)) return avant.call(this, s, x, y, o);
      const o2 = { ...o, duree: o.duree ?? Math.max(.1, plain(ORIG.get(s) ?? s) / 16) };
      const k = this.cadre;
      if (k && a !== s) {   // un texte qui s'allonge avec ses états ne sort pas du cadre
        const t = o.taille ?? 18, w = largeur(this.ctx, a, t), x0 = o.align === 'center' ? x - w / 2 : o.align === 'right' ? x - w : x;
        if (x0 + w > k.w - 4 || x0 < 4) o2.max = Math.min(o.max ?? Infinity, o.align === 'center' ? 2 * Math.min(x - 4, k.w - 4 - x) : o.align === 'right' ? x - 4 : k.w - 4 - x);
      }
      return avant.call(this, marque(a), x, y, o2);
    };
    if (typeof window.chim === 'function') { const chim = window.chim; window.chim = s => chim(marque(annote(s))); }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', installer); else installer();
})();
