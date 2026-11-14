/*
 * Myogramme — commun à myographe.html, intensite.html et sommation.html (cours « Rôle du muscle strié squelettique »).
 *
 * 1. Le modèle (exact, le rendu ne le change jamais) :
 *    secousse de référence : latence 0,01 s, contraction 0,04 s (sommet à 0,05 s), relâchement 0,05 s (retour à 0,10 s),
 *    amplitude 20 mm. Montée rapide (0,04 s) et descente plus lente (0,05 s, un peu plus « traînante ») : forme lisse
 *    et asymétrique. Plusieurs stimulations de même intensité : les secousses se superposent ; une stimulation qui tombe
 *    pendant la latence de la précédente reste sans effet visible ; chaque secousse ajoutée pendant la contraction ou le
 *    relâchement d'une autre est un peu plus forte (le muscle est déjà activé) ; saturation douce : le plateau du tétanos
 *    parfait vaut environ 3 × la secousse isolée (≈ 60 mm). Valeurs vérifiées : Δ = 0,03 s → un seul sommet ≈ 38 mm ;
 *    Δ = 0,07 s → deux sommets 20 puis ≈ 31 mm ; 15 Hz → plateau dentelé ≈ 14–32 mm ; 40 Hz → plateau lisse ≈ 60 mm.
 * 2. Le dessin à la craie : axes, ligne du temps en dents, signal d'excitation, accolades.
 * 3. La peinture (règle 7) avec le canvas brut : muscle rose-rouge à fibres fines, tendon blanc nacré, os ivoire,
 *    papier clair du cylindre, encre du stylet, boîtier de l'excitateur, coupe transversale (fibres polygonales).
 *    Un dégradé par objet, aucune boucle par pixel.
 */
(function () {
  'use strict';
  const TAU = Math.PI * 2;
  const LAT = 0.01, CON = 0.04, REL = 0.05, AMP = 20;
  const GAIN = 0.7, PLAFOND = 62, QUEUE = 1.6;

  /* ── 1. Modèle ─────────────────────────────────────────────────────────── */
  /** Secousse unité (0..1), `tau` s après la stimulation ; o.rel / o.con / o.lat changent une phase (fatigue). */
  function unite(tau, o = {}) {
    const lat = o.lat ?? LAT, con = o.con ?? CON, rel = o.rel ?? REL;
    if (!(tau > lat)) return 0;
    const u = tau - lat;
    if (u < con) return (1 - Math.cos(Math.PI * u / con)) / 2;
    const v = (u - con) / rel;
    if (v >= 1) return 0;
    return (1 + Math.cos(Math.PI * v)) / 2 * (1 + QUEUE * v * v);   // décroissante de 1 à 0 (vérifié), queue un peu traînante
  }
  /** Secousse en mm (o.amp : amplitude, 20 mm par défaut). */
  const secousse = (tau, o = {}) => (o.amp ?? AMP) * unite(tau, o);
  const sat0 = L => L / Math.pow(1 + Math.pow(L / PLAFOND, 4), 0.25);
  const saturer = L => sat0(L) * AMP / sat0(AMP);            // une secousse isolée garde ses 20 mm
  /** Phase de la secousse précédente où tombe une stimulation, Δ s après elle. */
  function phase(d) { return d < LAT ? 'latence' : d < LAT + CON ? 'contraction' : d < LAT + CON + REL ? 'relachement' : 'apres'; }
  const NOM_PHASE = { latence: 'la latence', contraction: 'la contraction', relachement: 'le relâchement', apres: 'après la fin' };
  /** Train de stimulations de même intensité : { efficaces, ignorees, y(t) en mm }. */
  function train(stims) {
    const efficaces = [], ignorees = [];
    for (const s of stims.slice().sort((a, b) => a - b)) {
      const prec = efficaces[efficaces.length - 1];
      if (prec && s - prec.t < LAT) { ignorees.push(s); continue; }      // pendant la latence : sans effet visible
      const r = efficaces.reduce((a, e) => a + unite(s - e.t), 0);         // le muscle est déjà activé
      efficaces.push({ t: s, g: 1 + GAIN * r });
    }
    const y = t => saturer(efficaces.reduce((a, e) => a + AMP * e.g * unite(t - e.t), 0));
    return { efficaces, ignorees, y };
  }
  /** Sommets locaux d'une courbe y(t) sur [a, b] (au pas dt), au-dessus de `min` mm. */
  function sommets(y, a, b, dt = 0.0005, min = 0.5) {
    const out = []; let p2 = y(a), p1 = y(a + dt);
    for (let t = a + 2 * dt; t <= b; t += dt) { const v = y(t); if (p1 > p2 && p1 >= v && p1 > min) out.push({ t: t - dt, y: p1 }); p2 = p1; p1 = v; }
    return out;
  }
  function creux(y, a, b, dt = 0.0005) { let m = Infinity, tm = a; for (let t = a; t <= b; t += dt) { const v = y(t); if (v < m) { m = v; tm = t; } } return { t: tm, y: m }; }

  /* ── 2. Craie : repère d'un graphe G = { x0 (x de t = 0), px (px/s), y0 (ligne de base), py (px/mm) } ── */
  const X = (G, t) => G.x0 + t * G.px, Y = (G, mm) => G.y0 - mm * G.py;
  /** Axes : amplitude (mm) verticale en xa, temps horizontal de xa à xb ; graduations [[valeur, libellé]]. */
  function axes(c, G, o) {
    const xa = o.xa, xb = o.xb, haut = o.haut;
    c.fleche(xa, G.y0, xb, G.y0, { couleur: 'faible', largeur: 1.6 });
    c.fleche(xa, G.y0, xa, haut, { couleur: 'faible', largeur: 1.6 });
    for (const [v, lib] of o.mm || []) { const y = Y(G, v); c.ligne(xa - 4, y, xa + 4, y, { couleur: 'faible', largeur: 1.3, duree: .03 }); if (lib != null) c.texte(lib, xa - 7, y + 5, { couleur: 'faible', taille: o.taille ?? 13, align: 'right', duree: .08 }); }
    for (const [v, lib] of o.t || []) { const x = X(G, v); c.ligne(x, G.y0 - 4, x, G.y0 + 4, { couleur: 'faible', largeur: 1.3, duree: .03 }); if (lib != null) c.texte(lib, x, G.y0 + 19, { couleur: 'faible', taille: o.taille ?? 13, align: 'center', duree: .08 }); }
    if (o.titreMm) c.texte(o.titreMm, o.titreMmX ?? xa - 8, o.titreMmY ?? haut + 4, { couleur: 'faible', taille: 13, align: o.titreMmAlign || 'right' });
    if (o.titreT) c.texte(o.titreT, xb, G.y0 + 19, { couleur: 'faible', taille: 13, align: 'right' });
  }
  /** Ligne du temps en dents (créneaux) de `pas` s, de xa à xb, posée en y (hauteur 7 px). */
  function ligneTemps(c, G, y, xa, xb, pas, o = {}) {
    const d = pas * G.px, pts = [[xa, y]];
    const k0 = Math.ceil((xa - G.x0) / d);
    for (let k = k0; X(G, k * pas) + d / 2 <= xb; k++) {
      const x = X(G, k * pas);
      if (x < xa) continue;
      pts.push([x, y], [x, y - 7], [x + d / 2, y - 7], [x + d / 2, y]);
    }
    pts.push([xb, y]);
    c.trait(pts, { couleur: o.couleur || 'blanc', largeur: 1.4, tremble: .25, duree: o.duree });
  }
  /** Signal d'excitation : trait horizontal avec un petit créneau à chaque stimulation déjà arrivée (t ≤ tNow). */
  function signal(c, G, y, xa, xb, stims, tNow, o = {}) {
    const pts = [[xa, y]], w = Math.max(3, (o.largeurS ?? 0.002) * G.px);
    for (const s of stims.slice().sort((a, b) => a - b)) {
      if (s > tNow + 1e-9) break;
      const x = X(G, s); pts.push([x, y], [x, y - 12], [x + w, y - 12], [x + w, y]);
    }
    pts.push([xb, y]);
    c.trait(pts, { couleur: o.couleur || 'jaune', largeur: 1.6, tremble: .2 });
  }
  /** Courbe à la craie y(t) (mm) de ta à tb. */
  function courbe(c, G, y, ta, tb, o = {}) {
    if (!(tb > ta)) return;
    const n = Math.max(8, Math.ceil((tb - ta) * G.px / (o.pas ?? 2)));
    c.courbe(u => { const t = ta + (tb - ta) * u; return [X(G, t), Y(G, y(t))]; }, n, { couleur: o.couleur || 'blanc', largeur: o.largeur ?? 2.4, tremble: o.tremble ?? .15, pointille: o.pointille, alpha: o.alpha });
  }
  /** Accolade horizontale de x1 à x2 ; pointe vers le bas (texte dessous) si `bas`, sinon vers le haut. */
  function accolade(c, x1, x2, y, o = {}) {
    const s = o.bas === false ? -1 : 1, h = o.h ?? 7, m = (x1 + x2) / 2, r = Math.min(8, (x2 - x1) / 4);
    const pts = [[x1, y - s * h * .2], [x1 + r * .3, y + s * h * .45], [x1 + r, y + s * h * .55], [m - r, y + s * h * .55], [m - r * .3, y + s * h * .7], [m, y + s * h * 1.3],
      [m + r * .3, y + s * h * .7], [m + r, y + s * h * .55], [x2 - r, y + s * h * .55], [x2 - r * .3, y + s * h * .45], [x2, y - s * h * .2]];
    c.trait(pts, { couleur: o.couleur || 'jaune', largeur: o.largeur ?? 1.6, tremble: .2 });
  }

  /* ── 3. Peinture (canvas brut, dans craie.direct, AVANT la craie) ─────────────────────────────────── */
  function graine(seed) { let s = (seed >>> 0) || 1; return () => { s = (Math.imul(s, 1664525) + 1013904223) >>> 0; return s / 4294967296; }; }
  /** Os ivoire (bout de fémur tenu par la pince) : capsule horizontale. */
  function os(ctx, x, y, w, h) {
    ctx.save();
    const g = ctx.createLinearGradient(x, y, x, y + h);
    g.addColorStop(0, '#fbf5e4'); g.addColorStop(.45, '#efe2bf'); g.addColorStop(1, '#b9a679');
    ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(x, y, w, h, h / 2); ctx.fill();
    ctx.strokeStyle = 'rgba(90,70,30,.45)'; ctx.lineWidth = 1; ctx.stroke();
    ctx.restore();
  }
  /** Demi-largeur du muscle le long de sa longueur (s de 0 en haut à 1 au tendon). */
  const profil = (s, hw) => 2.6 + (hw - 2.6) * Math.pow(Math.sin(Math.PI * Math.pow(s, .78)), .85) + 4 * Math.pow(1 - s, 6);
  /**
   * Muscle gastrocnémien de grenouille suspendu : ventre rose-rouge (dégradé, fibres fines), tendon blanc nacré dessous.
   * o = { cx, haut, L (longueur du ventre), hw (demi-largeur maxi), tendon (longueur), excite (0..1 : teinte plus vive) }.
   */
  function muscle(ctx, o) {
    const { cx, haut, L, hw } = o, n = 28, bas = haut + L, ex = o.excite || 0;
    const bord = sgn => { const pts = []; for (let i = 0; i <= n; i++) { const s = i / n; pts.push([cx + sgn * profil(s, hw), haut + s * L]); } return pts; };
    const gauche = bord(-1), droite = bord(1);
    ctx.save();
    // ombre portée sur le tableau (pour l'œil)
    ctx.fillStyle = 'rgba(0,0,0,.22)'; ctx.beginPath(); ctx.ellipse(cx + 4, haut + L * .45 + 5, hw * .95, L * .48, 0, 0, TAU); ctx.fill();
    // le tendon (sous le bas du ventre), blanc nacré
    const tl = o.tendon ?? 26, tw = 3.2;
    const gt = ctx.createLinearGradient(cx - tw, 0, cx + tw, 0);
    gt.addColorStop(0, '#9aa3b5'); gt.addColorStop(.3, '#f1f3fa'); gt.addColorStop(.5, '#ffffff'); gt.addColorStop(.68, '#f3e9f2'); gt.addColorStop(1, '#a5adbf');
    ctx.fillStyle = gt; ctx.beginPath();
    ctx.moveTo(cx - tw, bas - 6); ctx.lineTo(cx + tw, bas - 6); ctx.lineTo(cx + 1.6, bas + tl); ctx.lineTo(cx - 1.6, bas + tl); ctx.closePath(); ctx.fill();
    ctx.strokeStyle = 'rgba(255,255,255,.55)'; ctx.lineWidth = .7; ctx.beginPath(); ctx.moveTo(cx - .6, bas - 4); ctx.lineTo(cx - .4, bas + tl - 2); ctx.stroke();
    // le ventre
    ctx.beginPath(); gauche.forEach(([x, y], i) => (i ? ctx.lineTo(x, y) : ctx.moveTo(x, y))); for (let i = droite.length - 1; i >= 0; i--) ctx.lineTo(droite[i][0], droite[i][1]); ctx.closePath();
    const g = ctx.createLinearGradient(cx - hw, 0, cx + hw, 0);
    const a = ex * .35;
    g.addColorStop(0, `rgb(${110 + 30 * a},${24},${34})`); g.addColorStop(.22, `rgb(${188 + 40 * a},${58 - 10 * a},${70 - 10 * a})`);
    g.addColorStop(.46, `rgb(${226 + 20 * a},${122 - 20 * a},${126 - 20 * a})`); g.addColorStop(.7, `rgb(${196 + 40 * a},${64 - 10 * a},${76 - 10 * a})`); g.addColorStop(1, `rgb(${102 + 30 * a},${20},${30})`);
    ctx.fillStyle = g; ctx.fill();
    ctx.save(); ctx.clip();
    // fibres fines le long du muscle
    ctx.lineWidth = .7;
    for (let k = -6; k <= 6; k++) {
      const f = k / 7; ctx.strokeStyle = k % 2 ? 'rgba(255,205,205,.20)' : 'rgba(90,10,20,.22)';
      ctx.beginPath(); for (let i = 0; i <= n; i++) { const s = i / n, x = cx + f * profil(s, hw), y = haut + s * L; i ? ctx.lineTo(x, y) : ctx.moveTo(x, y); } ctx.stroke();
    }
    // reflet
    ctx.strokeStyle = 'rgba(255,235,235,.30)'; ctx.lineWidth = 2.2;
    ctx.beginPath(); for (let i = 3; i <= n - 6; i++) { const s = i / n, x = cx - .4 * profil(s, hw), y = haut + s * L; i > 3 ? ctx.lineTo(x, y) : ctx.moveTo(x, y); } ctx.stroke();
    ctx.restore();
    ctx.strokeStyle = 'rgba(60,8,16,.65)'; ctx.lineWidth = 1; ctx.stroke();
    ctx.restore();
    return { bas: bas + tl, bord: s => profil(s, hw) };
  }
  /** Tige ou barre métallique (support, levier) : un dégradé perpendiculaire à la barre. */
  function barre(ctx, x1, y1, x2, y2, ep, teinte = 'acier') {
    const a = Math.atan2(y2 - y1, x2 - x1), nx = -Math.sin(a) * ep / 2, ny = Math.cos(a) * ep / 2;
    const g = ctx.createLinearGradient(x1 + nx, y1 + ny, x1 - nx, y1 - ny);
    const c = teinte === 'laiton' ? ['#6b5520', '#e8cf7a', '#9c7d2e'] : ['#4b5563', '#d1d5db', '#6b7280'];
    g.addColorStop(0, c[0]); g.addColorStop(.45, c[1]); g.addColorStop(1, c[2]);
    ctx.save(); ctx.fillStyle = g; ctx.beginPath(); ctx.moveTo(x1 + nx, y1 + ny); ctx.lineTo(x2 + nx, y2 + ny); ctx.lineTo(x2 - nx, y2 - ny); ctx.lineTo(x1 - nx, y1 - ny); ctx.closePath(); ctx.fill(); ctx.restore();
  }
  /** Le papier clair du cylindre (face avant d'un tambour vertical) : ombré sur les bords, couvercles métalliques. */
  function cylindre(ctx, x, y, w, h, o = {}) {
    ctx.save();
    ctx.fillStyle = 'rgba(0,0,0,.25)'; ctx.beginPath(); ctx.ellipse(x + w / 2 + 4, y + h + 4, w / 2, 5, 0, 0, TAU); ctx.fill();
    const g = ctx.createLinearGradient(x, 0, x + w, 0);
    g.addColorStop(0, '#9e9886'); g.addColorStop(.18, '#ddd6c2'); g.addColorStop(.45, '#f4efe1'); g.addColorStop(.8, '#d8d0bb'); g.addColorStop(1, '#8d8774');
    ctx.fillStyle = g; ctx.fillRect(x, y, w, h);
    if (o.ry !== 0) {
      const ry = o.ry ?? 5, gc = ctx.createLinearGradient(x, 0, x + w, 0);
      gc.addColorStop(0, '#4b5563'); gc.addColorStop(.5, '#cbd5e1'); gc.addColorStop(1, '#475569');
      ctx.fillStyle = gc; ctx.beginPath(); ctx.ellipse(x + w / 2, y, w / 2, ry, 0, 0, TAU); ctx.fill();
      ctx.beginPath(); ctx.ellipse(x + w / 2, y + h, w / 2, ry, 0, 0, Math.PI); ctx.fill();
    }
    ctx.restore();
  }
  /** Encre du stylet sur le papier (trait sombre fin), points [[x,y]…]. */
  function encre(ctx, pts, l = 1.4) {
    if (pts.length < 2) return;
    ctx.save(); ctx.strokeStyle = '#2b201a'; ctx.lineWidth = l; ctx.lineJoin = 'round'; ctx.lineCap = 'round';
    ctx.beginPath(); pts.forEach(([x, y], i) => (i ? ctx.lineTo(x, y) : ctx.moveTo(x, y))); ctx.stroke(); ctx.restore();
  }
  /** Boîtier de l'excitateur : boîte sombre, cadran, deux bornes (rouge, noire). Renvoie la position des bornes. */
  function excitateur(ctx, x, y, w, h, o = {}) {
    ctx.save();
    ctx.fillStyle = 'rgba(0,0,0,.25)'; ctx.beginPath(); ctx.roundRect(x + 3, y + 4, w, h, 6); ctx.fill();
    const g = ctx.createLinearGradient(x, y, x, y + h);
    g.addColorStop(0, '#3a4554'); g.addColorStop(1, '#161c25');
    ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(x, y, w, h, 6); ctx.fill();
    ctx.strokeStyle = 'rgba(203,213,225,.35)'; ctx.lineWidth = 1; ctx.stroke();
    const bornes = o.bornes || [[x + 10, y + h - 9], [x + 22, y + h - 9]];
    bornes.forEach(([bx, by], i) => { const gb = ctx.createRadialGradient(bx - 1, by - 1, .5, bx, by, 4); gb.addColorStop(0, i ? '#9ca3af' : '#fecaca'); gb.addColorStop(1, i ? '#111827' : '#b91c1c'); ctx.fillStyle = gb; ctx.beginPath(); ctx.arc(bx, by, 3.6, 0, TAU); ctx.fill(); });
    if (o.cadran !== false) {
      const cx = o.cadranX ?? x + w - 16, cy = o.cadranY ?? y + h / 2, r = 8;
      const gc = ctx.createRadialGradient(cx - 2, cy - 2, 1, cx, cy, r); gc.addColorStop(0, '#e5e7eb'); gc.addColorStop(1, '#6b7280');
      ctx.fillStyle = gc; ctx.beginPath(); ctx.arc(cx, cy, r, 0, TAU); ctx.fill();
      ctx.strokeStyle = '#111827'; ctx.lineWidth = 1.4; ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(cx + r * .7 * Math.cos(o.angle ?? -2.2), cy + r * .7 * Math.sin(o.angle ?? -2.2)); ctx.stroke();
    }
    if (o.voyant) { ctx.fillStyle = '#fde047'; ctx.shadowColor = '#fde047'; ctx.shadowBlur = 10; ctx.beginPath(); ctx.arc(x + w - 10, y + 8, 3, 0, TAU); ctx.fill(); ctx.shadowBlur = 0; }
    ctx.restore();
    return bornes;
  }
  /** Un fil électrique souple (rouge ou noir) entre deux points. */
  function fil(ctx, x1, y1, x2, y2, couleur, creux = 10) {
    ctx.save(); ctx.strokeStyle = couleur; ctx.lineWidth = 1.8; ctx.lineCap = 'round';
    ctx.beginPath(); ctx.moveTo(x1, y1); ctx.quadraticCurveTo((x1 + x2) / 2, Math.max(y1, y2) + creux, x2, y2); ctx.stroke(); ctx.restore();
  }
  /** Étincelle d'excitation (petite étoile jaune brillante). */
  function eclair(ctx, x, y, r = 7) {
    ctx.save(); ctx.fillStyle = '#fef08a'; ctx.shadowColor = '#facc15'; ctx.shadowBlur = 14; ctx.beginPath();
    for (let i = 0; i < 10; i++) { const a = i / 10 * TAU, rr = i % 2 ? r * .35 : r; ctx[i ? 'lineTo' : 'moveTo'](x + rr * Math.cos(a), y + rr * Math.sin(a)); }
    ctx.closePath(); ctx.fill(); ctx.restore();
  }

  /* ── Coupe transversale du muscle : ~40 fibres polygonales (cellules de Voronoï calculées une fois) ── */
  function coupe(cx, cy, r, n = 40, seed = 5) {
    const rnd = graine(seed), germes = [];
    for (let i = 0; i < n; i++) {       // spirale de tournesol, un peu secouée : des polygones de taille voisine
      const rr = r * .93 * Math.sqrt((i + .5) / n), a = i * 2.39996 + (rnd() - .5) * .5;
      germes.push([cx + rr * Math.cos(a) + (rnd() - .5) * 4, cy + rr * Math.sin(a) + (rnd() - .5) * 4]);
    }
    const contour = []; for (let i = 0; i < 48; i++) { const a = i / 48 * TAU; contour.push([cx + r * Math.cos(a), cy + r * Math.sin(a)]); }
    const couper = (poly, p, q) => {   // garde le côté de p par rapport à la médiatrice de [p q]
      const mx = (p[0] + q[0]) / 2, my = (p[1] + q[1]) / 2, nx = q[0] - p[0], ny = q[1] - p[1], out = [];
      const f = P => (P[0] - mx) * nx + (P[1] - my) * ny;
      for (let i = 0; i < poly.length; i++) {
        const A = poly[i], B = poly[(i + 1) % poly.length], fa = f(A), fb = f(B);
        if (fa <= 0) out.push(A);
        if ((fa < 0) !== (fb < 0) && fa !== fb) { const k = fa / (fa - fb); out.push([A[0] + (B[0] - A[0]) * k, A[1] + (B[1] - A[1]) * k]); }
      }
      return out;
    };
    const fibres = germes.map((p, i) => {
      let poly = contour.slice();
      germes.forEach((q, j) => { if (j !== i) poly = couper(poly, p, q); });
      // le polygone resserré vers son centre : un fin liseré entre deux fibres
      const gx = poly.reduce((s, P) => s + P[0], 0) / poly.length, gy = poly.reduce((s, P) => s + P[1], 0) / poly.length;
      const serre = poly.map(([x, y]) => [gx + (x - gx) * .86, gy + (y - gy) * .86]);
      const sommet = serre[Math.floor(rnd() * serre.length)];
      return { poly: serre, gx, gy, noyau: [gx + (sommet[0] - gx) * .78, gy + (sommet[1] - gy) * .78], seuil: rnd() };
    });
    // ordre de recrutement : les fibres au seuil le plus bas répondent d'abord
    const ordre = fibres.map((f, i) => i).sort((a, b) => fibres[a].seuil - fibres[b].seuil);
    ordre.forEach((i, k) => { fibres[i].rang = k; });
    return { cx, cy, r, fibres };
  }
  /** Peint la coupe : `nAllumees` fibres excitées (rouge vif), `eclat` 0..1 (au moment de la réponse). */
  function peindreCoupe(ctx, C, nAllumees, eclat = 0) {
    ctx.save();
    ctx.fillStyle = 'rgba(0,0,0,.25)'; ctx.beginPath(); ctx.arc(C.cx + 4, C.cy + 5, C.r + 3, 0, TAU); ctx.fill();
    const gf = ctx.createRadialGradient(C.cx - C.r * .3, C.cy - C.r * .3, 4, C.cx, C.cy, C.r + 4);
    gf.addColorStop(0, '#f6d9d6'); gf.addColorStop(1, '#c99b98');
    ctx.fillStyle = gf; ctx.beginPath(); ctx.arc(C.cx, C.cy, C.r + 3, 0, TAU); ctx.fill();
    ctx.strokeStyle = 'rgba(120,40,50,.6)'; ctx.lineWidth = 1.5; ctx.stroke();
    for (const f of C.fibres) {
      const on = f.rang < nAllumees;
      const g = ctx.createRadialGradient(f.gx - 3, f.gy - 3, 1, f.gx, f.gy, 16);
      if (on) { g.addColorStop(0, '#ff8a80'); g.addColorStop(1, '#d4111f'); } else { g.addColorStop(0, '#f2bcbc'); g.addColorStop(1, '#cf8086'); }
      ctx.fillStyle = g;
      if (on && eclat > 0) { ctx.shadowColor = '#ff3b3b'; ctx.shadowBlur = 10 * eclat; }
      ctx.beginPath(); f.poly.forEach(([x, y], i) => (i ? ctx.lineTo(x, y) : ctx.moveTo(x, y))); ctx.closePath(); ctx.fill();
      ctx.shadowBlur = 0;
      ctx.strokeStyle = on ? 'rgba(255,220,200,.55)' : 'rgba(255,240,240,.5)'; ctx.lineWidth = .8; ctx.stroke();
      ctx.fillStyle = '#6d3a9c'; ctx.beginPath(); ctx.ellipse(f.noyau[0], f.noyau[1], 2.1, 1.4, Math.atan2(f.noyau[1] - f.gy, f.noyau[0] - f.gx) + Math.PI / 2, 0, TAU); ctx.fill();
    }
    ctx.restore();
  }

  window.Myogramme = { LAT, CON, REL, AMP, unite, secousse, saturer, phase, NOM_PHASE, train, sommets, creux,
    X, Y, axes, ligneTemps, signal, courbe, accolade,
    peindre: { os, muscle, barre, cylindre, encre, excitateur, fil, eclair, coupe: peindreCoupe }, coupe, graine };
})();
