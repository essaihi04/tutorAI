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
      finally { craie.trait = trait; craie.texte = texte; craie.point = point; scene.mesurant = false; scene.ouvert = t; }
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
  /* Couleurs habituelles des modèles moléculaires, un peu adoucies pour le tableau noir. */
  const EL = {
    H: { c: [236, 240, 244], r: 3.3 }, Hp: { c: [250, 204, 21], r: 3.5 }, O: { c: [222, 52, 52], r: 5.2 }, C: { c: [88, 93, 102], r: 5.4 },
    N: { c: [59, 102, 236], r: 5.3 }, I: { c: [134, 72, 228], r: 7.4 }, Na: { c: [171, 120, 242], r: 6 }, Cl: { c: [74, 196, 98], r: 6.6 },
    Cu: { c: [205, 112, 52], r: 6 }, Zn: { c: [168, 178, 190], r: 6 }, S: { c: [234, 196, 52], r: 6.2 }, Fe: { c: [224, 130, 60], r: 6 }, Mn: { c: [156, 84, 190], r: 6 },
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
    /* L'acide éthanoïque : CH₃ à gauche, C du groupe carboxyle, =O en haut, –O–H à droite (le H acide en jaune : c'est lui qui part). */
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
  const doux = p => { p = Math.min(1, Math.max(0, p)); return p < .5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2; };
  window.Rendu = { EL, MODELES, atome, molecule, lentille, choc, fiole, flacon, doux, rgba };
})();
