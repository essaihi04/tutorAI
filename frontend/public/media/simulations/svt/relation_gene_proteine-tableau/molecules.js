/*
 * Peinture des molécules et des milieux du cours « Expression de l’information génétique » (2 Bac PC BIOF, 11 novembre 2026).
 * Règle 7 du skill simulations-au-tableau : le vivant est PEINT (dégradés, ombres), la craie sert aux légendes.
 * Un seul code couleur dans toutes les simulations du cours :
 *   ADN : squelette bleu-violet ; ARNm : squelette orange ; bases A rouge, T jaune, C bleu, G vert, U magenta ;
 *   ribosome : deux sous-unités turquoise ; ARNt vert pâle ; acides aminés en perles colorées, méthionine rouge ;
 *   nucléoplasme bleuté, cytoplasme rosé ; mutation en rouge vif (craie « rouge »).
 * Rien d’hors programme : ni sites A / P / E, ni ARNt en trèfle, ni promoteur.
 * Toutes les fonctions prennent le contexte brut `x` (craie.ctx, à appeler dans craie.direct).
 */
(function () {
  'use strict';
  const TAU = Math.PI * 2;
  const BASE = { A: '#dc2626', T: '#ca8a04', C: '#2563eb', G: '#16a34a', U: '#c026d3' };
  const COMP_ADN = { A: 'T', T: 'A', C: 'G', G: 'C' };
  const COMP_ARN = { A: 'U', T: 'A', C: 'G', G: 'C' };   // base de l’ARNm posée en face d’une base du brin transcrit
  const SQUELETTE = { adn: ['#a5b4fc', '#4f46e5'], arn: ['#fdba74', '#ea580c'] };
  // couleurs des perles (acides aminés) : stables d’une simulation à l’autre
  const AA = { Met: '#ef4444', Arg: '#3b82f6', Ser: '#22c55e', Gln: '#a855f7', Glu: '#f59e0b', Val: '#14b8a6', Leu: '#ec4899', Trp: '#84cc16',
    Phe: '#f97316', Pro: '#06b6d4', Gly: '#eab308', His: '#8b5cf6', Asn: '#10b981', Ala: '#0ea5e9', Ile: '#d946ef', Thr: '#65a30d', Lys: '#e11d48',
    Cys: '#facc15', Tyr: '#fb7185', Asp: '#f43f5e' };
  const couleurAA = n => AA[n] || '#94a3b8';

  /** Code génétique complet (codon de l’ARNm → abréviation à trois lettres ; « Stop » pour UAA, UAG, UGA). */
  const CODE = {};
  (function () {
    const L = 'UCAG';
    const t = [
      'Phe Phe Leu Leu Ser Ser Ser Ser Tyr Tyr Stop Stop Cys Cys Stop Trp',
      'Leu Leu Leu Leu Pro Pro Pro Pro His His Gln Gln Arg Arg Arg Arg',
      'Ile Ile Ile Met Thr Thr Thr Thr Asn Asn Lys Lys Ser Ser Arg Arg',
      'Val Val Val Val Ala Ala Ala Ala Asp Asp Glu Glu Gly Gly Gly Gly'];
    // ligne = 1re lettre ; dans la ligne : 2e lettre (U C A G) × 3e lettre (U C A G)
    for (let i = 0; i < 4; i++) { const m = t[i].split(' '); let j = 0; for (const b2 of L) for (const b3 of L) CODE[L[i] + b2 + b3] = m[j++]; }
  })();
  const traduire = codon => CODE[String(codon).toUpperCase().replace(/T/g, 'U')] || '?';

  function sphere(x, cx, cy, r, coul, a = 1) {
    x.save(); x.globalAlpha *= a;
    const g = x.createRadialGradient(cx - r * .35, cy - r * .4, r * .1, cx, cy, r);
    g.addColorStop(0, '#ffffff'); g.addColorStop(.25, coul); g.addColorStop(1, ombre(coul, .45));
    x.fillStyle = g; x.beginPath(); x.arc(cx, cy, r, 0, TAU); x.fill();
    x.restore();
  }
  /** Assombrit une couleur #rrggbb (f de 0 à 1 = part gardée). */
  function ombre(c, f) {
    const n = parseInt(c.slice(1), 16), r = (n >> 16) & 255, g = (n >> 8) & 255, b = n & 255;
    return `rgb(${Math.round(r * f)},${Math.round(g * f)},${Math.round(b * f)})`;
  }

  /**
   * Un brin d’acide nucléique horizontal : squelette ombré (type 'adn' ou 'arn') de x0 à x0 + n·pas, à la hauteur y ;
   * chaque base est un bâtonnet coloré qui part du squelette vers `sens` (+1 vers le bas, −1 vers le haut), longueur `lb`,
   * avec sa lettre écrite dedans. `lettres` = chaîne ; un caractère ' ' ou '-' laisse la place vide. `de`/`a` : bases visibles.
   * o.rouge = Set d’indices entourés de rouge (mutation) ; o.alpha.
   */
  function brin(x, x0, y, pas, lettres, type, sens, o = {}) {
    const n = lettres.length, lb = o.lb ?? 20, de = o.de ?? 0, a = o.a ?? n, al = o.alpha ?? 1;
    if (a <= de || al <= 0) return;
    x.save(); x.globalAlpha *= al;
    // bases
    for (let i = de; i < a; i++) {
      const L = lettres[i]; if (!BASE[L]) continue;
      const px = x0 + (i + .5) * pas;
      const g = x.createLinearGradient(px - 5, 0, px + 5, 0); g.addColorStop(0, ombre(BASE[L], .75)); g.addColorStop(.45, BASE[L]); g.addColorStop(1, ombre(BASE[L], .6));
      x.fillStyle = g; const y1 = y, y2 = y + sens * lb;
      x.beginPath(); x.roundRect ? x.roundRect(px - Math.min(6, pas * .32), Math.min(y1, y2), 2 * Math.min(6, pas * .32), Math.abs(y2 - y1), 3) : x.rect(px - 6, Math.min(y1, y2), 12, Math.abs(y2 - y1)); x.fill();
      if (o.lettres !== false) {
        x.fillStyle = '#fff'; x.font = `700 ${Math.round(Math.min(13, pas * .62))}px sans-serif`; x.textAlign = 'center'; x.textBaseline = 'middle';
        x.fillText(L, px, y + sens * lb * .55);
      }
      if (o.rouge && o.rouge.has(i)) { x.strokeStyle = '#ff2d2d'; x.lineWidth = 2.4; x.beginPath(); x.ellipse(px, y + sens * lb * .5, pas * .5, lb * .75, 0, 0, TAU); x.stroke(); }
    }
    // squelette (sucre-phosphate) : un ruban ombré
    const [cl, cf] = SQUELETTE[type] || SQUELETTE.adn, xa = x0 + de * pas, xb = x0 + a * pas;
    const gs = x.createLinearGradient(0, y - 5, 0, y + 5); gs.addColorStop(0, cl); gs.addColorStop(.5, cf); gs.addColorStop(1, ombre(cf.length === 7 ? cf : '#4f46e5', .55));
    x.strokeStyle = gs; x.lineWidth = o.epaisseur ?? 7; x.lineCap = 'round'; x.beginPath(); x.moveTo(xa + 2, y); x.lineTo(xb - 2, y); x.stroke();
    x.strokeStyle = 'rgba(255,255,255,.45)'; x.lineWidth = 1.4; x.beginPath(); x.moveTo(xa + 4, y - 2); x.lineTo(xb - 4, y - 2); x.stroke();
    x.restore();
  }

  /** Nucléotide libre (petit rond-squelette + bâtonnet de base), pour l’ARN : rond orange ; pour l’ADN : rond violet. */
  function nucleotide(x, px, py, L, type = 'arn', ang = -Math.PI / 2, a = 1) {
    x.save(); x.globalAlpha *= a; x.translate(px, py); x.rotate(ang + Math.PI / 2);
    x.fillStyle = BASE[L] || '#999'; x.beginPath(); x.rect(-4, -16, 8, 14); x.fill();
    sphere(x, 0, 2, 5, (SQUELETTE[type] || SQUELETTE.arn)[1]);
    x.translate(0, -9); x.rotate(-(ang + Math.PI / 2)); x.fillStyle = '#fff'; x.font = '700 8px sans-serif'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText(L, 0, .5);
    x.restore();
  }

  /**
   * Ribosome posé sur un ARNm horizontal à la hauteur y : la grande sous-unité au-dessus, la petite au-dessous.
   * (cx, y) = centre ; s = échelle (1 → 96 px de large) ; o.petite / o.grande (alpha de chaque sous-unité) ; o.dy : écart vertical.
   */
  function ribosome(x, cx, y, s = 1, o = {}) {
    const ap = o.petite ?? 1, ag = o.grande ?? 1, dyg = (o.dyg ?? 0), dyp = (o.dyp ?? 0);
    const sous = (cy, rx, ry, a, haut) => {
      if (a <= 0) return;
      x.save(); x.globalAlpha *= a;
      const g = x.createRadialGradient(cx - rx * .35, cy - ry * .45, 3, cx, cy, Math.max(rx, ry));
      g.addColorStop(0, '#ccfbf1'); g.addColorStop(.45, '#2dd4bf'); g.addColorStop(1, '#0f766e');
      x.fillStyle = g; x.beginPath();
      // forme un peu bosselée (pas un simple ovale)
      for (let i = 0; i <= 40; i++) { const t = i / 40 * TAU, r = 1 + .05 * Math.sin(t * 5 + (haut ? 1 : 2)); const px = cx + Math.cos(t) * rx * r, py = cy + Math.sin(t) * ry * r; i ? x.lineTo(px, py) : x.moveTo(px, py); }
      x.closePath(); x.fill();
      x.strokeStyle = 'rgba(15,80,75,.7)'; x.lineWidth = 1.2; x.stroke();
      x.restore();
    };
    sous(y - 30 * s + dyg, 50 * s, 36 * s, ag, true);
    sous(y + 16 * s + dyp, 46 * s, 18 * s, ap, false);
  }

  /**
   * ARNt simplifié (programme : un acide aminé en haut, un anticodon en bas — pas de trèfle).
   * (cx, yb) = milieu du bas de l’anticodon (les bases pointent vers le bas, sur le codon) ; `aa` : nom de l’acide aminé ou null.
   */
  function arnt(x, cx, yb, anticodon, aa, o = {}) {
    const a = o.alpha ?? 1; if (a <= 0) return;
    x.save(); x.globalAlpha *= a;
    const pas = o.pas ?? 16, w = pas * 3 + 8, h = 46;
    // corps
    const g = x.createLinearGradient(cx - w / 2, 0, cx + w / 2, 0); g.addColorStop(0, '#4d7c0f'); g.addColorStop(.4, '#bef264'); g.addColorStop(1, '#3f6212');
    x.fillStyle = g; x.beginPath();
    x.moveTo(cx - w / 2, yb - 18); x.lineTo(cx - w / 2 + 6, yb - h); x.lineTo(cx - 6, yb - h - 6); x.lineTo(cx - 5, yb - h - 26); x.lineTo(cx + 5, yb - h - 26); x.lineTo(cx + 6, yb - h - 6); x.lineTo(cx + w / 2 - 6, yb - h); x.lineTo(cx + w / 2, yb - 18); x.closePath(); x.fill();
    x.strokeStyle = 'rgba(40,70,10,.8)'; x.lineWidth = 1.1; x.stroke();
    // anticodon : trois bases tournées vers le bas
    for (let i = 0; i < 3; i++) {
      const L = anticodon[i], px = cx + (i - 1) * pas;
      x.fillStyle = BASE[L] || '#888'; x.beginPath(); x.rect(px - 5, yb - 18, 10, 18); x.fill();
      x.fillStyle = '#fff'; x.font = '700 10px sans-serif'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText(L, px, yb - 8);
    }
    if (aa) sphere(x, cx, yb - h - 36, o.r ?? 11, couleurAA(aa));
    x.restore();
  }

  /** Une perle d’acide aminé avec son abréviation (peinte, petite) ; o.noir : texte sombre. */
  function perle(x, cx, cy, r, nom, o = {}) {
    sphere(x, cx, cy, r, couleurAA(nom), o.alpha ?? 1);
    if (o.texte !== false && r >= 9) {
      x.save(); x.globalAlpha *= (o.alpha ?? 1); x.fillStyle = '#fff'; x.font = `700 ${Math.round(r * .72)}px sans-serif`; x.textAlign = 'center'; x.textBaseline = 'middle';
      x.shadowColor = 'rgba(0,0,0,.6)'; x.shadowBlur = 2; x.fillText(nom, cx, cy + .5); x.restore();
    }
  }
  /** Une chaîne d’acides aminés : pts = [[x,y],…], noms = […] ; liaisons peptidiques en traits clairs. */
  function chaine(x, pts, noms, r = 10, o = {}) {
    x.save(); x.globalAlpha *= (o.alpha ?? 1);
    x.strokeStyle = o.liaison || 'rgba(255,255,255,.75)'; x.lineWidth = 2.4;
    for (let i = 1; i < pts.length; i++) { x.beginPath(); x.moveTo(pts[i - 1][0], pts[i - 1][1]); x.lineTo(pts[i][0], pts[i][1]); x.stroke(); }
    x.restore();
    pts.forEach((p, i) => perle(x, p[0], p[1], r, noms[i], o));
  }

  /** Nucléoplasme bleuté (disque ou rectangle arrondi) avec enveloppe double et pores (o.pores = nombre). */
  function noyau(x, cx, cy, rx, ry, o = {}) {
    x.save(); x.globalAlpha *= (o.alpha ?? 1);
    const g = x.createRadialGradient(cx - rx * .3, cy - ry * .3, 4, cx, cy, Math.max(rx, ry));
    g.addColorStop(0, 'rgba(219,234,254,.75)'); g.addColorStop(.7, 'rgba(147,197,253,.55)'); g.addColorStop(1, 'rgba(96,165,250,.6)');
    x.fillStyle = g; x.beginPath(); x.ellipse(cx, cy, rx, ry, 0, 0, TAU); x.fill();
    x.strokeStyle = 'rgba(59,130,246,.9)'; x.lineWidth = 2; x.beginPath(); x.ellipse(cx, cy, rx, ry, 0, 0, TAU); x.stroke();
    x.strokeStyle = 'rgba(59,130,246,.55)'; x.lineWidth = 1.2; x.beginPath(); x.ellipse(cx, cy, rx + 4, ry + 4, 0, 0, TAU); x.stroke();
    const np = o.pores ?? 10;
    for (let i = 0; i < np; i++) { const t = i / np * TAU + (o.phase ?? .3), px = cx + Math.cos(t) * (rx + 2), py = cy + Math.sin(t) * (ry + 2); x.fillStyle = 'rgba(255,255,255,.95)'; x.beginPath(); x.arc(px, py, 3.2, 0, TAU); x.fill(); x.strokeStyle = 'rgba(37,99,235,.9)'; x.lineWidth = 1; x.stroke(); }
    x.restore();
  }
  /** Position du pore n° i (mêmes réglages que noyau()). */
  function pore(cx, cy, rx, ry, i, np = 10, phase = .3) { const t = i / np * TAU + phase; return [cx + Math.cos(t) * (rx + 2), cy + Math.sin(t) * (ry + 2)]; }
  /** Cytoplasme rosé (ellipse) avec membrane et granulations. */
  function cytoplasme(x, cx, cy, rx, ry, o = {}) {
    x.save(); x.globalAlpha *= (o.alpha ?? 1);
    const g = x.createRadialGradient(cx - rx * .3, cy - ry * .35, 6, cx, cy, Math.max(rx, ry));
    g.addColorStop(0, 'rgba(255,228,236,.55)'); g.addColorStop(.75, 'rgba(249,168,212,.42)'); g.addColorStop(1, 'rgba(219,112,160,.5)');
    x.fillStyle = g; x.beginPath(); x.ellipse(cx, cy, rx, ry, 0, 0, TAU); x.fill();
    x.strokeStyle = 'rgba(190,70,120,.85)'; x.lineWidth = 2; x.stroke();
    x.fillStyle = 'rgba(160,80,110,.25)';
    for (let i = 0; i < 40; i++) { const a2 = i * 2.39996, r = .3 + .62 * ((i * 37) % 23) / 23; x.beginPath(); x.arc(cx + Math.cos(a2) * rx * r, cy + Math.sin(a2) * ry * r, 1.2, 0, TAU); x.fill(); }
    x.restore();
  }
  /** Un fond rectangulaire arrondi peint (cadre d’une vue) : 'noyau' bleuté ou 'cytoplasme' rosé. */
  function milieu(x, x0, y0, w, h, type, a = 1) {
    x.save(); x.globalAlpha *= a;
    const g = x.createLinearGradient(x0, y0, x0, y0 + h);
    if (type === 'noyau') { g.addColorStop(0, 'rgba(191,219,254,.30)'); g.addColorStop(1, 'rgba(96,165,250,.22)'); }
    else { g.addColorStop(0, 'rgba(252,231,243,.26)'); g.addColorStop(1, 'rgba(244,114,182,.18)'); }
    x.fillStyle = g; x.beginPath(); x.roundRect ? x.roundRect(x0, y0, w, h, 14) : x.rect(x0, y0, w, h); x.fill();
    x.restore();
  }

  /** Hématie : f = 0 disque biconcave (vue de face, centre plus clair) ; f = 1 faucille. ang = orientation. */
  function hematie(x, cx, cy, r, f = 0, ang = 0, a = 1) {
    x.save(); x.globalAlpha *= a; x.translate(cx, cy); x.rotate(ang);
    if (f < .5) {
      const g = x.createRadialGradient(0, 0, r * .1, 0, 0, r);
      g.addColorStop(0, '#f87171'); g.addColorStop(.45, '#dc2626'); g.addColorStop(.85, '#b91c1c'); g.addColorStop(1, '#7f1d1d');
      x.fillStyle = g; x.beginPath(); x.ellipse(0, 0, r, r * (1 - f * .6), 0, 0, TAU); x.fill();
      x.fillStyle = 'rgba(254,202,202,.35)'; x.beginPath(); x.ellipse(0, 0, r * .42, r * .42 * (1 - f * .6), 0, 0, TAU); x.fill();
    } else {
      // faucille : un croissant pointu
      const g = x.createLinearGradient(0, -r, 0, r); g.addColorStop(0, '#ef4444'); g.addColorStop(1, '#7f1d1d');
      x.fillStyle = g; x.beginPath();
      x.moveTo(-r * 1.25, r * .15); x.quadraticCurveTo(0, -r * 1.25, r * 1.25, r * .15); x.quadraticCurveTo(0, -r * .35, -r * 1.25, r * .15); x.fill();
      x.strokeStyle = 'rgba(80,10,10,.6)'; x.lineWidth = 1; x.stroke();
    }
    x.restore();
  }
  /** Vaisseau sanguin horizontal (plasma, paroi rosée) entre x0 et x1, centré en y, demi-hauteur h ; o.etranglement (x, demi-hauteur). */
  function vaisseau(x, x0, x1, y, h, o = {}) {
    x.save(); x.globalAlpha *= (o.alpha ?? 1);
    const ht = px => { if (!o.etranglement) return h; const [ex, eh] = o.etranglement, d = Math.abs(px - ex); return d > 60 ? h : eh + (h - eh) * (d / 60) ** 2; };
    const haut = [], bas = [];
    for (let px = x0; px <= x1; px += 6) { haut.push([px, y - ht(px)]); bas.push([px, y + ht(px)]); }
    const g = x.createLinearGradient(0, y - h, 0, y + h); g.addColorStop(0, 'rgba(254,226,226,.35)'); g.addColorStop(.5, 'rgba(254,242,242,.18)'); g.addColorStop(1, 'rgba(254,226,226,.35)');
    x.fillStyle = g; x.beginPath(); haut.forEach(([px, py], i) => (i ? x.lineTo(px, py) : x.moveTo(px, py))); for (let i = bas.length - 1; i >= 0; i--) x.lineTo(bas[i][0], bas[i][1]); x.closePath(); x.fill();
    x.strokeStyle = 'rgba(251,113,133,.9)'; x.lineWidth = 5; x.lineCap = 'round';
    for (const ligne of [haut, bas]) { x.beginPath(); ligne.forEach(([px, py], i) => (i ? x.lineTo(px, py) : x.moveTo(px, py))); x.stroke(); }
    x.restore();
    return ht;
  }
  /** Point noir d’autoradiographie (grain d’argent) — quelques pixels sombres et flous. */
  function grain(x, px, py, a = 1) { x.save(); x.globalAlpha *= a; x.fillStyle = 'rgba(10,10,10,.9)'; x.beginPath(); x.arc(px, py, 2.1, 0, TAU); x.fill(); x.fillStyle = 'rgba(10,10,10,.35)'; x.beginPath(); x.arc(px + .8, py - .6, 3.4, 0, TAU); x.fill(); x.restore(); }

  window.Molecules = { BASE, COMP_ADN, COMP_ARN, AA, CODE, traduire, couleurAA, sphere, ombre, brin, nucleotide, ribosome, arnt, perle, chaine,
    noyau, pore, cytoplasme, milieu, hematie, vaisseau, grain };
})();
