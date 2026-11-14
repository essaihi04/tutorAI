/*
 * Peinture des molécules de la contraction (cours « Rôle du muscle strié squelettique », 10 novembre 2026) :
 * actine en perles rouge-orangé torsadées, fil de tropomyosine, blocs de troponine, filament épais et têtes de
 * myosine bleues renflées, réticulum sarcoplasmique translucide, billes de Ca²⁺ jaunes brillantes, pastille ATP verte,
 * cuve de liquide bleuté, fibre rose striée à noyaux violets. Canvas brut (à appeler dans craie.direct, AVANT la craie) ;
 * un dégradé par objet, aucune boucle par pixel. Les formes sont pour l'œil : elles ne changent aucun instant du modèle.
 * Utilisé par calcium.html, cycle.html et exigences.html.
 */
(function () {
  'use strict';
  const TAU = Math.PI * 2;
  const lerp = (a, b, f) => a + (b - a) * f;

  /** Sphère ombrée (un dégradé radial). */
  function perle(ctx, x, y, r, clair, moyen, sombre) {
    const g = ctx.createRadialGradient(x - r * .35, y - r * .4, r * .1, x, y, r);
    g.addColorStop(0, clair); g.addColorStop(.55, moyen); g.addColorStop(1, sombre);
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.fill();
  }

  /*
   * Filament fin : géométrie (sans dessin). Les perles sont numérotées k ; elles glissent avec dx.
   * o : x0, x1, y, dx, pas, r, amp, ouverture (0 = tropomyosine sur les sites, 1 = sites libérés),
   *     sitesTous (une perle sur sitesTous porte un site, vers le bas), tnTous / tnDecal (troponine).
   */
  function geoFin(o) {
    const pas = o.pas ?? 12, r = o.r ?? 7, amp = o.amp ?? 4.6, dx = o.dx ?? 0, ouv = o.ouverture ?? 0;
    const sitesTous = o.sitesTous ?? 3, tnTous = o.tnTous ?? 14, tnDecal = o.tnDecal ?? 7;
    const kMin = Math.floor((o.x0 - dx - o.X0) / pas) - 2, kMax = Math.ceil((o.x1 - dx - o.X0) / pas) + 2;
    const ySite = o.y + amp + r * .55, yTropoRepos = ySite + 1, yTropoOuvert = o.y + 1.5;
    const yTropo = lerp(yTropoRepos, yTropoOuvert, ouv);
    const sites = [], troponines = [];
    for (let k = kMin; k <= kMax; k++) {
      const x = o.X0 + k * pas + dx;
      if (x < o.x0 + 3 || x > o.x1 - 3) continue;
      if (((k % sitesTous) + sitesTous) % sitesTous === 0) sites.push({ k, x, y: ySite });
      if (((k % tnTous) + tnTous) % tnTous === tnDecal) troponines.push({ k, x, y: yTropo + 2.5 });
    }
    return { pas, r, amp, dx, ouv, kMin, kMax, ySite, yTropo, sites, troponines };
  }

  /** Perles d'actine, deux chaînes torsadées ; `marque` : la perle k colorée en repère mobile. */
  function actine(ctx, o, g = geoFin(o)) {
    const { pas, r, amp } = g, alpha = o.alpha ?? 1;
    ctx.save(); ctx.globalAlpha *= alpha;
    ctx.beginPath(); ctx.rect(o.x0, o.y - 40, o.x1 - o.x0, 80); ctx.clip();
    const perles = [];
    for (let k = g.kMin; k <= g.kMax; k++) {
      const x = o.X0 + k * pas + o.dx, ph = TAU * k / 13;
      perles.push({ x, y: o.y + amp * Math.sin(ph), p: Math.cos(ph), k, brin: 0 });
      perles.push({ x: x + pas / 2, y: o.y - amp * Math.sin(ph + .5), p: -Math.cos(ph + .5), k, brin: 1 });
    }
    perles.sort((a, b) => a.p - b.p);
    for (const b of perles) {
      const f = .78 + .22 * (b.p + 1) / 2, rr = r * f;
      if (o.marque != null && b.k === o.marque && b.brin === 0) perle(ctx, b.x, b.y, rr + .6, '#fff7ed', '#f5f5f4', '#a8a29e');
      else if (b.p >= 0) perle(ctx, b.x, b.y, rr, '#ffd2b0', '#f0703a', '#9a2d12');
      else perle(ctx, b.x, b.y, rr, '#e7a283', '#b4502c', '#6b200e');
    }
    ctx.restore();
  }

  /** Sites de fixation de la myosine sur l'actine : en couleur selon l'ouverture (cachés sous la tropomyosine au repos). */
  function sites(ctx, o, g = geoFin(o)) {
    const a = .2 + .8 * g.ouv;
    ctx.save(); ctx.globalAlpha *= a * (o.alpha ?? 1);
    for (const s of g.sites) {
      ctx.shadowColor = 'rgba(103,232,249,.9)'; ctx.shadowBlur = 6 * g.ouv;
      perle(ctx, s.x, s.y + 2, 3.8, '#ecfeff', '#22d3ee', '#0e7490');
    }
    ctx.restore();
  }

  /** Fil de tropomyosine enroulé le long de l'actine (cordon pâle à reflet). */
  function tropomyosine(ctx, o, g = geoFin(o)) {
    ctx.save(); ctx.globalAlpha *= o.alpha ?? 1;
    ctx.beginPath(); ctx.rect(o.x0, o.y - 40, o.x1 - o.x0, 80); ctx.clip();
    const pts = [];
    for (let x = o.x0 - 4; x <= o.x1 + 4; x += 4) pts.push([x, g.yTropo + 1.3 * Math.sin((x - o.dx) / 9)]);
    for (const [w, c] of [[6.4, '#8a6a3c'], [4.2, '#e9cf9a'], [1.4, '#fff6dc']]) {
      ctx.strokeStyle = c; ctx.lineWidth = w; ctx.lineCap = 'round'; ctx.beginPath();
      pts.forEach(([x, y], i) => (i ? ctx.lineTo(x, y - (w < 2 ? 1 : 0)) : ctx.moveTo(x, y))); ctx.stroke();
    }
    ctx.restore();
  }

  /** Blocs de troponine (trois lobes violets), posés sur la tropomyosine. */
  function troponine(ctx, o, g = geoFin(o)) {
    ctx.save(); ctx.globalAlpha *= o.alpha ?? 1;
    for (const t of g.troponines) {
      const gr = ctx.createLinearGradient(t.x, t.y - 7, t.x, t.y + 7);
      gr.addColorStop(0, '#ddd6fe'); gr.addColorStop(.5, '#8b5cf6'); gr.addColorStop(1, '#4c1d95');
      ctx.fillStyle = gr;
      ctx.beginPath(); ctx.roundRect(t.x - 9, t.y - 6, 18, 12, 4); ctx.fill();
      ctx.beginPath(); ctx.arc(t.x - 7.5, t.y + 5, 4.6, 0, TAU); ctx.fill(); ctx.beginPath(); ctx.arc(t.x + 7.5, t.y + 5, 4.6, 0, TAU); ctx.fill();
    }
    ctx.restore();
  }
  /** Places où se fixent les Ca²⁺ sur une troponine (deux par bloc). */
  const placesCa = (t) => [{ x: t.x - 5.5, y: t.y - 9 }, { x: t.x + 5.5, y: t.y - 9 }];

  /** Filament fin complet ; `caFixe` (0..1) : Ca²⁺ dessinés sur chaque troponine. Renvoie la géométrie. */
  function filamentFin(ctx, o) {
    const g = geoFin(o);
    actine(ctx, o, g); if (o.sites !== false) sites(ctx, o, g);
    if (o.tropomyosine !== false) tropomyosine(ctx, o, g);
    if (o.troponine !== false) troponine(ctx, o, g);
    if (o.caFixe > 0) for (const t of g.troponines) for (const p of placesCa(t)) ca(ctx, p.x, p.y, 4.6, o.caFixe);
    return g;
  }

  /** Ion Ca²⁺ : petite bille jaune brillante. */
  function ca(ctx, x, y, r = 4.2, alpha = 1) {
    ctx.save(); ctx.globalAlpha *= alpha; ctx.shadowColor = 'rgba(250,204,21,.85)'; ctx.shadowBlur = 7;
    perle(ctx, x, y, r, '#fffbe0', '#facc15', '#a16207'); ctx.restore();
  }

  /** Filament épais : faisceau de molécules de myosine (bâtonnet bleu). */
  function filamentEpais(ctx, x0, x1, y, o = {}) {
    const h = o.h ?? 14;
    ctx.save(); ctx.globalAlpha *= o.alpha ?? 1;
    const g = ctx.createLinearGradient(0, y - h / 2, 0, y + h / 2);
    g.addColorStop(0, '#bfdbfe'); g.addColorStop(.35, '#3b82f6'); g.addColorStop(1, '#1e3a8a');
    ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(x0, y - h / 2, x1 - x0, h, h / 2); ctx.fill();
    ctx.strokeStyle = 'rgba(219,234,254,.35)'; ctx.lineWidth = 1;
    for (const f of [-.18, .2]) { ctx.beginPath(); ctx.moveTo(x0 + 6, y + f * h); ctx.lineTo(x1 - 6, y + f * h); ctx.stroke(); }
    ctx.restore();
  }

  /*
   * Tête de myosine : un cou (bâtonnet) depuis la base B sur le filament épais, une tête renflée dont la pointe P
   * est le site de fixation de l'actine ; `angle` = direction base de la tête → pointe (rad). Renvoie les points utiles.
   */
  function tete(ctx, B, P, angle, o = {}) {
    const L = o.L ?? 46, ry = o.ry ?? 11, u = [Math.cos(angle), Math.sin(angle)], n = [-u[1], u[0]];
    const H = [P.x - u[0] * L, P.y - u[1] * L], C = [P.x - u[0] * L / 2, P.y - u[1] * L / 2];
    ctx.save(); ctx.globalAlpha *= o.alpha ?? 1;
    // Cou
    const cx = B.x, cy = (B.y + H[1]) / 2;
    for (const [w, c] of [[o.cou ?? 7, '#1e40af'], [(o.cou ?? 7) * .45, '#93c5fd']]) {
      ctx.strokeStyle = c; ctx.lineWidth = w; ctx.lineCap = 'round';
      ctx.beginPath(); ctx.moveTo(B.x, B.y); ctx.quadraticCurveTo(cx, cy, H[0], H[1]); ctx.stroke();
    }
    // Tête renflée
    ctx.translate(C[0], C[1]); ctx.rotate(angle);
    const g = ctx.createRadialGradient(-L * .1, -ry * .45, 1, 0, 0, L * .6);
    g.addColorStop(0, '#dbeafe'); g.addColorStop(.45, '#3b82f6'); g.addColorStop(1, '#1e3a8a');
    ctx.fillStyle = g; ctx.beginPath(); ctx.ellipse(0, 0, L / 2, ry, 0, 0, TAU); ctx.fill();
    ctx.restore();
    const cote = n[0] >= 0 ? 1 : -1;     // le site de l'ATP est sur le flanc droit de la tête
    return { H: { x: H[0], y: H[1] }, C: { x: C[0], y: C[1] }, siteAtp: { x: C[0] + cote * n[0] * (ry - 1), y: C[1] + cote * n[1] * (ry - 1) }, pointe: { x: P.x, y: P.y } };
  }
  /** Le creux du site de l'ATP (petite poche sombre) et le site de l'actine (pointe claire). */
  function sitesTete(ctx, T, o = {}) {
    ctx.save(); ctx.globalAlpha *= o.alpha ?? 1;
    perle(ctx, T.siteAtp.x, T.siteAtp.y, o.r ?? 4, '#bbf7d0', '#15803d', '#052e16');
    perle(ctx, T.pointe.x, T.pointe.y, o.r ?? 4, '#ecfeff', '#22d3ee', '#0e7490');
    ctx.restore();
  }

  /** Pastille ATP (verte, étiquetée) ; « ADP », « Pi » en pastilles plus pâles. */
  function pastille(ctx, x, y, texte = 'ATP', o = {}) {
    const r = o.r ?? 11, pale = texte !== 'ATP';
    ctx.save(); ctx.globalAlpha *= o.alpha ?? 1;
    ctx.shadowColor = pale ? 'rgba(0,0,0,0)' : 'rgba(74,222,128,.7)'; ctx.shadowBlur = pale ? 0 : 6;
    perle(ctx, x, y, r, pale ? '#ecfccb' : '#dcfce7', pale ? '#a3c96b' : '#22c55e', pale ? '#4d6b1f' : '#14532d');
    ctx.shadowBlur = 0; ctx.fillStyle = pale ? '#1a2e05' : '#052e16';
    ctx.font = `700 ${Math.round(r * (texte.length > 2 ? .82 : 1))}px system-ui, sans-serif`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillText(texte, x, y + .5); ctx.restore();
  }

  /** Éclat d'énergie (hydrolyse de l'ATP), f de 0 à 1. */
  function eclat(ctx, x, y, f) {
    if (f <= 0) return;
    const a = Math.sin(Math.PI * Math.min(1, f)), R = 10 + 22 * f;
    ctx.save(); ctx.globalAlpha *= a;
    const g = ctx.createRadialGradient(x, y, 0, x, y, R);
    g.addColorStop(0, 'rgba(255,255,255,.95)'); g.addColorStop(.35, 'rgba(253,224,71,.7)'); g.addColorStop(1, 'rgba(253,224,71,0)');
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, R, 0, TAU); ctx.fill();
    ctx.strokeStyle = 'rgba(254,240,138,.9)'; ctx.lineWidth = 2;
    for (let i = 0; i < 8; i++) { const t = i / 8 * TAU + .2; ctx.beginPath(); ctx.moveTo(x + Math.cos(t) * R * .45, y + Math.sin(t) * R * .45); ctx.lineTo(x + Math.cos(t) * R * .95, y + Math.sin(t) * R * .95); ctx.stroke(); }
    ctx.restore();
  }

  /** Réticulum sarcoplasmique : sac membranaire translucide ; `excite` (0..1) éclaire sa membrane. */
  function reticulum(ctx, x, y, w, h, o = {}) {
    const pts = [], n = 64, cx = x + w / 2, cy = y + h / 2;
    for (let i = 0; i < n; i++) {
      const a = i / n * TAU, c = Math.cos(a), s = Math.sin(a);
      const k = 1 + .035 * Math.sin(5 * a + 1) + .02 * Math.sin(11 * a);
      pts.push([cx + Math.sign(c) * Math.pow(Math.abs(c), .35) * w / 2 * k, cy + Math.sign(s) * Math.pow(Math.abs(s), .55) * h / 2 * k]);
    }
    ctx.save(); ctx.globalAlpha *= o.alpha ?? 1;
    const chemin = () => { ctx.beginPath(); pts.forEach(([px, py], i) => (i ? ctx.lineTo(px, py) : ctx.moveTo(px, py))); ctx.closePath(); };
    const g = ctx.createLinearGradient(0, y, 0, y + h);
    g.addColorStop(0, 'rgba(186,230,253,.20)'); g.addColorStop(1, 'rgba(125,211,252,.08)');
    chemin(); ctx.fillStyle = g; ctx.fill();
    const e = o.excite ?? 0;
    ctx.shadowColor = `rgba(250,204,21,${.8 * e})`; ctx.shadowBlur = 10 * e;
    ctx.strokeStyle = e > 0 ? `rgba(${lerp(186, 253, e)},${lerp(230, 224, e)},${lerp(253, 71, e)},.75)` : 'rgba(186,230,253,.6)';
    ctx.lineWidth = 3.2; chemin(); ctx.stroke();
    ctx.shadowBlur = 0; ctx.strokeStyle = 'rgba(224,242,254,.28)'; ctx.lineWidth = 1.2;
    ctx.save(); ctx.translate(cx, cy); ctx.scale(.965, .9); ctx.translate(-cx, -cy); chemin(); ctx.stroke(); ctx.restore();
    ctx.restore();
  }

  /** Cuve de verre remplie d'un liquide légèrement bleuté (niveau en y). */
  function cuve(ctx, x, y, w, h, niveau) {
    ctx.save();
    const g = ctx.createLinearGradient(0, niveau, 0, y + h);
    g.addColorStop(0, 'rgba(147,197,253,.30)'); g.addColorStop(1, 'rgba(59,130,246,.38)');
    ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(x + 2, niveau, w - 4, y + h - niveau - 2, [0, 0, 8, 8]); ctx.fill();
    ctx.strokeStyle = 'rgba(224,242,254,.75)'; ctx.lineWidth = 1.6; ctx.beginPath(); ctx.moveTo(x + 3, niveau); ctx.lineTo(x + w - 3, niveau); ctx.stroke();
    ctx.fillStyle = 'rgba(255,255,255,.06)'; ctx.fillRect(x + 8, niveau + 6, 10, y + h - niveau - 18);
    ctx.strokeStyle = 'rgba(226,232,240,.55)'; ctx.lineWidth = 2.4;
    ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x, y + h - 8); ctx.quadraticCurveTo(x, y + h, x + 8, y + h); ctx.lineTo(x + w - 8, y + h); ctx.quadraticCurveTo(x + w, y + h, x + w, y + h - 8); ctx.lineTo(x + w, y); ctx.stroke();
    ctx.restore();
  }

  /** Fibre musculaire isolée, verticale (de yHaut à yBas, largeur w) : rose, striée, noyaux violets sur les bords. */
  function fibre(ctx, x, yHaut, yBas, w) {
    const L = yBas - yHaut;
    ctx.save();
    const g = ctx.createLinearGradient(x - w / 2, 0, x + w / 2, 0);
    g.addColorStop(0, '#a83a50'); g.addColorStop(.3, '#ec8f9e'); g.addColorStop(.55, '#f6b3bd'); g.addColorStop(1, '#9b3046');
    ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(x - w / 2, yHaut, w, L, w / 2.4); ctx.fill();
    ctx.beginPath(); ctx.roundRect(x - w / 2, yHaut, w, L, w / 2.4); ctx.clip();
    // Striation : le nombre de sarcomères dessinés est fixe, ils se resserrent quand la fibre raccourcit.
    const n = 22, p = L / n;
    ctx.fillStyle = 'rgba(110,20,40,.32)';
    for (let i = 0; i < n; i++) ctx.fillRect(x - w / 2, yHaut + i * p + p * .2, w, p * .45);
    ctx.fillStyle = 'rgba(255,240,245,.18)';
    for (let i = 0; i < n; i++) ctx.fillRect(x - w / 2, yHaut + i * p + p * .8, w, p * .1);
    // Noyaux sur les bords
    for (let i = 0; i < 4; i++) {
      const yy = yHaut + L * (.14 + i * .24), xx = x + (i % 2 ? 1 : -1) * (w / 2 - 3);
      const gn = ctx.createRadialGradient(xx - 1, yy - 2, .5, xx, yy, 6);
      gn.addColorStop(0, '#d8b4fe'); gn.addColorStop(.6, '#7e22ce'); gn.addColorStop(1, '#3b0764');
      ctx.fillStyle = gn; ctx.beginPath(); ctx.ellipse(xx, yy, 2.8, 6.5, 0, 0, TAU); ctx.fill();
    }
    ctx.restore();
  }

  window.MoleculesPeintes = { perle, geoFin, actine, sites, tropomyosine, troponine, placesCa, filamentFin, ca, filamentEpais, tete, sitesTete, pastille, eclat, reticulum, cuve, fibre, lerp };
})();
