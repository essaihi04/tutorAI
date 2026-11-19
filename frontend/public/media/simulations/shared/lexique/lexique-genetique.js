/*
 * LEXIQUE VISUEL COMMUN — GÉNÉTIQUE (ADN, ARN, bases, nucléotides, ribosome, ARNt, acides aminés, protéine, noyau, cytoplasme, hématie)
 * (18 novembre 2026 ; skill simulations-au-tableau règle 15). Fiches : docs/lexique-visuel/. Module partagé par tous les
 * cours : <script src="/media/simulations/shared/lexique/lexique-genetique.js"></script> → window.Molecules (et window.Lexique.genetique).
 * Il était le module local d'un seul cours ; tout nouveau cours de SVT qui dessine ces objets l'utilise au lieu de les redessiner.
 */
/*
 * Peinture des molécules et des milieux du cours « Expression de l’information génétique » (2 Bac PC BIOF, 11 novembre 2026).
 * Règle 7 du skill simulations-au-tableau : le vivant est PEINT (dégradés, ombres), la craie sert aux légendes.
 * Un seul code couleur dans toutes les simulations du cours :
 *   ADN : squelette bleu-violet ; ARNm : squelette orange ; bases A rouge, T jaune, C bleu, G vert, U magenta ;
 *   ribosome : deux sous-unités turquoise ; ARNt vert pâle ; acides aminés en perles colorées, méthionine rouge ;
 *   nucléoplasme violet (le noyau de tous les cours), cytoplasme rosé ; mutation en rouge vif (craie « rouge »).
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

  /* Lisibilité (16 novembre 2026, règle 10 du skill) : une lettre écrite SUR une peinture prend une encre sombre et grasse si
   * la peinture est claire (jaune, vert, orange…), blanche (avec une ombre fine) seulement si elle est foncée. */
  const ENCRE = '#0b1f2a';
  function clarte(c) {
    const n = parseInt(String(c).slice(1), 16), f = v => { v /= 255; return v <= .03928 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4; };
    return .2126 * f((n >> 16) & 255) + .7152 * f((n >> 8) & 255) + .0722 * f(n & 255);
  }
  // encre sombre si elle contraste nettement mieux que le blanc (le blanc garde l'avantage sur les rouges et les bleus saturés)
  const encre = c => { if (!(typeof c === 'string' && c[0] === '#' && c.length === 7)) return '#fff'; const L = clarte(c); return (L + .05) / .063 > 1.25 * 1.05 / (L + .05) ? ENCRE : '#fff'; };
  /* Plancher des lettres peintes (19 novembre 2026, règle 18 du skill : tout texte d'une simulation fait au moins 15 px une
   * fois affiché dans le lecteur, aussi à 1366 × 560 et sur un téléphone en paysage 724 × 350). Une lettre peinte SUR un
   * objet (base, anticodon, acide aminé) prend au moins PLANCHER px à l'écran, d'après l'échelle réelle du contexte
   * (`ctx.getTransform()` ÷ devicePixelRatio ; pendant la mesure de la boîte de l'encre, `ctx.__echelle`, posé par le
   * commun.js du cours). L'objet grandit avec sa lettre (règle 10 : le texte tient dans sa forme) : bâtonnet de base plus
   * large et plus long, anticodon plus grand, perle d'acide aminé de rayon plus grand. Les dimensions sont calculées ici
   * (`gabarit`, `perleRayon`, `arntHauteur`) pour que les pages placent leurs objets d'après elles (règle 15 : un même
   * objet, un même dessin et les mêmes proportions dans tous les cours). */
  const PLANCHER = 15;
  /** Échelle écran du contexte : px CSS à l'écran pour 1 unité du dessin. */
  function echelleEcran(x) {
    if (x && x.__echelle) return x.__echelle;
    if (!x || !x.getTransform) return 1;
    const m = x.getTransform(), k = Math.hypot(m.a, m.b) / (window.devicePixelRatio || 1);
    return k > 1e-6 ? k : 1;
  }
  /** Taille d'une lettre peinte (unités du dessin) : la taille voulue, jamais sous PLANCHER px à l'écran. */
  const taillePeinte = (x, t) => Math.max(t, PLANCHER / echelleEcran(x));
  /** Écrit s centré en (px, py) sur une peinture de couleur `fond`, police grasse de `taille` (jamais sous 15 px à l'écran), encre choisie par encre(). */
  function lettreSur(x, s, px, py, fond, taille) {
    x.save(); const e = encre(fond); x.fillStyle = e; x.font = `700 ${taillePeinte(x, taille)}px sans-serif`; x.textAlign = 'center'; x.textBaseline = 'middle';
    if (e === '#fff') { x.shadowColor = 'rgba(0,0,0,.6)'; x.shadowBlur = 2; }
    x.fillText(s, px, py); x.restore();
  }

  /** Un fond sombre arrondi sous une légende à la craie posée SUR une peinture (cellule, noyau, fond de vue) : elle reste lisible.
   *  (px, py) = point d'ancrage de la craie (ligne de base), align comme pour craie.texte. */
  function pastille(x, s, px, py, taille, align = 'left', a = 1) {
    const w = String(s).replace(/_\{?|\}/g, '').length * taille * .5 + 14, x0 = align === 'center' ? px - w / 2 : align === 'right' ? px - w + 7 : px - 7;
    x.save(); x.globalAlpha *= a; x.fillStyle = 'rgba(10,18,26,.72)'; x.beginPath();
    if (x.roundRect) x.roundRect(x0, py - taille * .95, w, taille * 1.35, Math.min(9, taille * .55)); else x.rect(x0, py - taille * .95, w, taille * 1.35);
    x.fill(); x.restore();
  }

  function sphere(x, cx, cy, r, coul, a = 1) {
    x.save(); x.globalAlpha *= a;
    x.fillStyle = 'rgba(0,0,0,.25)'; x.beginPath(); x.ellipse(cx + r * .12, cy + r * .78, r * .85, r * .3, 0, 0, TAU); x.fill();   // ombre posée (16 novembre 2026)
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
   * Dimensions d'une base portant sa lettre, au pas `pas` et à la longueur voulue `lb` (unités du dessin) :
   * t = taille de la lettre, w = demi-largeur du bâtonnet, lb = longueur réelle (la lettre y tient), yl = distance du
   * squelette au centre de la lettre. Sans lettre, la base garde ses dimensions d'origine.
   */
  function gabarit(x, pas, lb = 20, lettre = true) {
    const w0 = Math.min(6, pas * .32);
    if (!lettre) return { t: 0, w: w0, lb, yl: lb * .55 };
    const t = taillePeinte(x, Math.min(13, pas * .62));
    const w = Math.max(w0, Math.min(t * .44, pas * .47)), l = Math.max(lb, t * .72 + 6.5);   // hauteur des capitales ≈ 0,72 em, le squelette couvre 3,5
    return { t, w, lb: l, yl: l === lb ? lb * .55 : (3.5 + l) / 2 };
  }
  /** Une base : bâtonnet coloré qui part du squelette (px, y) vers `sens` (+1 bas, −1 haut), sa lettre dedans.
   *  o.lettre (vrai), o.rouge (base entourée de rouge : mutation), o.alpha. Même dessin dans brin() et dans les pages. */
  function base(x, px, y, L, sens, pas, lb = 20, o = {}) {
    const col = BASE[L]; if (!col || (o.alpha ?? 1) <= 0) return;
    const G = gabarit(x, pas, lb, o.lettre !== false), w = G.w, l = G.lb;
    x.save(); x.globalAlpha *= (o.alpha ?? 1);
    const g = x.createLinearGradient(px - w, 0, px + w, 0); g.addColorStop(0, ombre(col, .75)); g.addColorStop(.45, col); g.addColorStop(1, ombre(col, .6));
    x.fillStyle = g; const y1 = y, y2 = y + sens * l;
    x.beginPath(); x.roundRect ? x.roundRect(px - w, Math.min(y1, y2), 2 * w, l, 3) : x.rect(px - w, Math.min(y1, y2), 2 * w, l); x.fill();
    x.fillStyle = 'rgba(255,255,255,.28)'; x.fillRect(px - w + 1.5, Math.min(y1, y2) + 2, 1.6, Math.max(0, l - 4));
    if (o.lettre !== false) lettreSur(x, L, px, y + sens * G.yl, col, G.t);
    if (o.rouge) { x.strokeStyle = '#ff2d2d'; x.lineWidth = 2.4; x.beginPath(); x.ellipse(px, y + sens * l * .5, Math.max(pas * .5, w + 3), l * .75, 0, 0, TAU); x.stroke(); }
    x.restore();
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
    for (let i = de; i < a; i++) base(x, x0 + (i + .5) * pas, y, lettres[i], sens, pas, lb, { lettre: o.lettres !== false, rouge: o.rouge && o.rouge.has(i) });
    // squelette (sucre-phosphate) : un ruban ombré
    const [cl, cf] = SQUELETTE[type] || SQUELETTE.adn, xa = x0 + de * pas, xb = x0 + a * pas;
    const gs = x.createLinearGradient(0, y - 5, 0, y + 5); gs.addColorStop(0, cl); gs.addColorStop(.5, cf); gs.addColorStop(1, ombre(cf.length === 7 ? cf : '#4f46e5', .55));
    // (16 novembre 2026) le squelette en tube : ombre portée douce, bord foncé, corps en dégradé, reflet net
    const ep = o.epaisseur ?? 7;
    x.save(); x.shadowColor = 'rgba(0,0,0,.4)'; x.shadowBlur = ep; x.shadowOffsetY = ep * .35;
    x.strokeStyle = ombre(cf.length === 7 ? cf : '#4f46e5', .45); x.lineWidth = ep + 2; x.lineCap = 'round'; x.beginPath(); x.moveTo(xa + 2, y); x.lineTo(xb - 2, y); x.stroke(); x.restore();
    x.strokeStyle = gs; x.lineWidth = ep; x.lineCap = 'round'; x.beginPath(); x.moveTo(xa + 2, y); x.lineTo(xb - 2, y); x.stroke();
    x.strokeStyle = 'rgba(255,255,255,.6)'; x.lineWidth = Math.max(1.2, ep * .22); x.beginPath(); x.moveTo(xa + 4, y - ep * .22); x.lineTo(xb - 4, y - ep * .22); x.stroke();
    x.restore();
  }

  /** Nucléotide libre (petit rond-squelette + bâtonnet de base), pour l’ARN : rond orange ; pour l’ADN : rond violet. */
  function nucleotide(x, px, py, L, type = 'arn', ang = -Math.PI / 2, a = 1) {
    const N = gabaritNucleotide(x);
    x.save(); x.globalAlpha *= a; x.translate(px, py); x.rotate(ang + Math.PI / 2);
    x.fillStyle = BASE[L] || '#999'; x.beginPath(); x.rect(-N.w, -N.l - 2, 2 * N.w, N.l); x.fill();
    sphere(x, 0, 2, 5, (SQUELETTE[type] || SQUELETTE.arn)[1]);
    x.translate(0, -2 - N.l / 2); x.rotate(-(ang + Math.PI / 2)); lettreSur(x, L, 0, .5, BASE[L], N.t);
    x.restore();
  }
  /** Dimensions d'un nucléotide libre : t lettre, w demi-largeur, l longueur de la base (sans la sphère). */
  function gabaritNucleotide(x, t0 = 10) { const t = taillePeinte(x, t0); return { t, w: Math.max(4, t * .44), l: Math.max(14, t * .72 + 5) }; }

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
      x.closePath(); x.shadowColor = 'rgba(0,0,0,.45)'; x.shadowBlur = 10 * s; x.shadowOffsetY = 4 * s; x.fill(); x.shadowColor = 'transparent';
      x.strokeStyle = 'rgba(15,80,75,.7)'; x.lineWidth = 1.2; x.stroke();
      // reflet doux et bord assombri : un volume, pas un ovale plat
      x.save(); x.clip();
      const sb = x.createRadialGradient(cx, cy, Math.min(rx, ry) * .5, cx, cy, Math.max(rx, ry) * 1.05); sb.addColorStop(0, 'rgba(0,40,40,0)'); sb.addColorStop(1, 'rgba(0,40,40,.35)'); x.fillStyle = sb; x.fillRect(cx - rx * 1.1, cy - ry * 1.1, 2.2 * rx, 2.2 * ry);
      const h = x.createRadialGradient(cx - rx * .4, cy - ry * .5, 1, cx - rx * .4, cy - ry * .5, rx * .55); h.addColorStop(0, 'rgba(255,255,255,.4)'); h.addColorStop(1, 'rgba(255,255,255,0)');
      x.fillStyle = h; x.fillRect(cx - rx, cy - ry, 2 * rx, 2 * ry); x.restore();
      x.restore();
    };
    sous(y - 30 * s + dyg, 50 * s, 36 * s, ag, true);
    sous(y + 16 * s + dyp, 46 * s, 18 * s, ap, false);
  }

  /**
   * ARNt simplifié (programme : un acide aminé en haut, un anticodon en bas — pas de trèfle).
   * (cx, yb) = milieu du bas de l’anticodon (les bases pointent vers le bas, sur le codon) ; `aa` : nom de l’acide aminé ou null.
   * o.lettres = false : l’anticodon sans ses lettres (petite icône, comme brin(…, { lettres: false })).
   */
  function arnt(x, cx, yb, anticodon, aa, o = {}) {
    const a = o.alpha ?? 1; if (a <= 0) return;
    x.save(); x.globalAlpha *= a;
    const pas = o.pas ?? 16, w = pas * 3 + 8, A = o.lettres === false ? { t: 0, bw: 5.5, bh: 18, h: 46 } : gabaritAnticodon(x, pas), h = A.h;
    // corps (17 novembre 2026) : une silhouette arrondie d’un seul tenant — tige fine en haut (porte l’acide aminé),
    // base large en bas (porte l’anticodon) — vert vif, ombre posée, reflet : on la reconnaît d’un coup d’œil
    const yt = yb - h - 26, ye = yb - h + 4, yl = yb - A.bh + 2, r = 6;
    const forme = () => {
      x.beginPath(); x.moveTo(cx - 5, yt + 3); x.quadraticCurveTo(cx - 5, yt, cx, yt); x.quadraticCurveTo(cx + 5, yt, cx + 5, yt + 3);
      x.lineTo(cx + 5, ye - 12); x.bezierCurveTo(cx + 5, ye, cx + w / 2, ye - 4, cx + w / 2, ye + 12);
      x.lineTo(cx + w / 2, yl - r); x.quadraticCurveTo(cx + w / 2, yl, cx + w / 2 - r, yl); x.lineTo(cx - w / 2 + r, yl); x.quadraticCurveTo(cx - w / 2, yl, cx - w / 2, yl - r);
      x.lineTo(cx - w / 2, ye + 12); x.bezierCurveTo(cx - w / 2, ye - 4, cx - 5, ye, cx - 5, ye - 12); x.closePath();
    };
    x.save(); x.shadowColor = 'rgba(0,0,0,.4)'; x.shadowBlur = 6; x.shadowOffsetY = 2;
    const g = x.createLinearGradient(cx - w / 2, 0, cx + w / 2, 0); g.addColorStop(0, '#3f8f12'); g.addColorStop(.38, '#b6f24a'); g.addColorStop(.62, '#84cc16'); g.addColorStop(1, '#2f6f0e');
    x.fillStyle = g; forme(); x.fill(); x.restore();
    x.strokeStyle = 'rgba(30,70,8,.85)'; x.lineWidth = 1.1; forme(); x.stroke();
    x.strokeStyle = 'rgba(255,255,255,.5)'; x.lineWidth = 1.6; x.lineCap = 'round'; x.beginPath(); x.moveTo(cx - 2, yt + 5); x.lineTo(cx - 2, ye - 12); x.moveTo(cx - w / 2 + 5, ye + 12); x.lineTo(cx - w / 2 + 5, yl - 7); x.stroke();
    // anticodon : trois bases tournées vers le bas
    for (let i = 0; i < 3; i++) {
      const L = anticodon[i], px = cx + (i - 1) * pas;
      x.fillStyle = BASE[L] || '#888'; x.beginPath(); x.roundRect ? x.roundRect(px - A.bw, yb - A.bh, 2 * A.bw, A.bh, [0, 0, 3, 3]) : x.rect(px - A.bw, yb - A.bh, 2 * A.bw, A.bh); x.fill();
      x.fillStyle = 'rgba(255,255,255,.28)'; x.fillRect(px - A.bw + 1.5, yb - A.bh + 1, 1.6, A.bh - 4);
      if (o.lettres !== false) lettreSur(x, L, px, yb - (A.bh - 2) / 2, BASE[L] || '#888888', A.t);
    }
    if (aa) sphere(x, cx, yb - h - 36, o.r ?? 11, couleurAA(aa));
    x.restore();
  }

  /** Dimensions de l'anticodon d'un ARNt au pas `pas` : t lettre, bw demi-largeur et bh hauteur d'une base,
   *  h hauteur du corps (46 au dessin d'origine ; l'acide aminé porté est à yb − h − 36). */
  function gabaritAnticodon(x, pas = 16) {
    const t = taillePeinte(x, 10), bw = Math.max(5.5, Math.min(t * .44, pas * .47)), bh = Math.max(18, t * .72 + 6);
    return { t, bw, bh, h: Math.max(46, bh + 28) };
  }
  const arntHauteur = (x, pas = 16) => gabaritAnticodon(x, pas).h;

  /** Rayon réel d'une perle d'acide aminé qui porte son nom (le nom tient dedans) ; r sans nom. */
  function perleRayon(x, r, nom, texte = true) {
    if (!texte || r < 9 || !nom) return r;
    const t = taillePeinte(x, Math.round(r * .72));
    if (t <= Math.round(r * .72)) return r;
    x.save(); x.font = `700 ${t}px sans-serif`; const lw = x.measureText(nom).width; x.restore();
    return Math.max(r, lw / 2 + 3, t * .62);
  }
  /** Une perle d’acide aminé avec son abréviation (peinte, petite) ; o.noir : texte sombre. */
  function perle(x, cx, cy, r, nom, o = {}) {
    const R = perleRayon(x, r, nom, o.texte !== false);
    sphere(x, cx, cy, R, couleurAA(nom), o.alpha ?? 1);
    if (o.texte !== false && r >= 9) {
      x.save(); x.globalAlpha *= (o.alpha ?? 1); lettreSur(x, nom, cx, cy + .5, couleurAA(nom), Math.round(r * .72)); x.restore();
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

  /** Nucléoplasme VIOLET (comme le noyau de tous les cours : lexique visuel commun, 18/11/2026 — il était bleu ici et violet
   *  dans Etapes.Peint.noyau du même cours), enveloppe double et pores (o.pores = nombre). */
  function noyau(x, cx, cy, rx, ry, o = {}) {
    x.save(); x.globalAlpha *= (o.alpha ?? 1);
    const g = x.createRadialGradient(cx - rx * .3, cy - ry * .3, 4, cx, cy, Math.max(rx, ry));
    g.addColorStop(0, 'rgba(240,214,255,.85)'); g.addColorStop(.55, 'rgba(190,132,246,.72)'); g.addColorStop(1, 'rgba(124,58,216,.74)');
    x.fillStyle = g; x.beginPath(); x.ellipse(cx, cy, rx, ry, 0, 0, TAU); x.fill();
    x.strokeStyle = 'rgba(76,29,149,.95)'; x.lineWidth = 2.2; x.beginPath(); x.ellipse(cx, cy, rx, ry, 0, 0, TAU); x.stroke();
    x.strokeStyle = 'rgba(255,255,255,.3)'; x.lineWidth = 1.6; x.beginPath(); x.ellipse(cx, cy, rx * .86, ry * .86, 0, Math.PI * 1.08, Math.PI * 1.45); x.stroke();   // reflet
    x.strokeStyle = 'rgba(192,132,252,.8)'; x.lineWidth = 1.3; x.beginPath(); x.ellipse(cx, cy, rx + 4, ry + 4, 0, 0, TAU); x.stroke();
    const np = o.pores ?? 10;
    for (let i = 0; i < np; i++) { const t = i / np * TAU + (o.phase ?? .3), px = cx + Math.cos(t) * (rx + 2), py = cy + Math.sin(t) * (ry + 2); x.fillStyle = 'rgba(255,255,255,.95)'; x.beginPath(); x.arc(px, py, 3.2, 0, TAU); x.fill(); x.strokeStyle = 'rgba(124,58,216,.9)'; x.lineWidth = 1; x.stroke(); }
    x.restore();
  }
  /** Position du pore n° i (mêmes réglages que noyau()). */
  function pore(cx, cy, rx, ry, i, np = 10, phase = .3) { const t = i / np * TAU + phase; return [cx + Math.cos(t) * (rx + 2), cy + Math.sin(t) * (ry + 2)]; }
  /** Cytoplasme rosé (ellipse) avec membrane et granulations. */
  function cytoplasme(x, cx, cy, rx, ry, o = {}) {
    x.save(); x.globalAlpha *= (o.alpha ?? 1);
    const g = x.createRadialGradient(cx - rx * .3, cy - ry * .35, 6, cx, cy, Math.max(rx, ry));
    g.addColorStop(0, 'rgba(255,214,200,.62)'); g.addColorStop(.6, 'rgba(253,150,150,.5)'); g.addColorStop(1, 'rgba(236,72,130,.56)');   // (17 novembre 2026) rose pêche vif
    x.fillStyle = g; x.beginPath(); x.ellipse(cx, cy, rx, ry, 0, 0, TAU); x.fill();
    x.strokeStyle = 'rgba(190,24,93,.95)'; x.lineWidth = 2.4; x.stroke();
    x.strokeStyle = 'rgba(255,255,255,.28)'; x.lineWidth = 2; x.beginPath(); x.ellipse(cx, cy, rx * .93, ry * .9, 0, Math.PI * 1.1, Math.PI * 1.42); x.stroke();
    x.fillStyle = 'rgba(157,23,77,.3)';
    for (let i = 0; i < 40; i++) { const a2 = i * 2.39996, r = .3 + .62 * ((i * 37) % 23) / 23; x.beginPath(); x.arc(cx + Math.cos(a2) * rx * r, cy + Math.sin(a2) * ry * r, 1.2, 0, TAU); x.fill(); }
    x.restore();
  }
  /** Un fond rectangulaire arrondi peint (cadre d’une vue) : 'noyau' violet (lexique visuel commun, 18/11/2026 ; il était bleu) ou 'cytoplasme' rosé. */
  function milieu(x, x0, y0, w, h, type, a = 1) {
    x.save(); x.globalAlpha *= a;
    const g = x.createLinearGradient(x0, y0, x0, y0 + h);
    // (17 novembre 2026) teintes franches au lieu d’un gris délavé : nucléoplasme bleu, cytoplasme rose pêche ; un halo clair
    // en haut à gauche et un liseré donnent un milieu « éclairé », les écritures à la craie restent bien lisibles dessus
    const noy = type === 'noyau';
    if (noy) { g.addColorStop(0, 'rgba(168,110,240,.32)'); g.addColorStop(1, 'rgba(109,40,217,.28)'); }
    else { g.addColorStop(0, 'rgba(255,130,150,.22)'); g.addColorStop(1, 'rgba(236,60,140,.20)'); }   // (règle 10) un peu plus sombre : les craies colorées s'y lisent
    const forme = () => { x.beginPath(); x.roundRect ? x.roundRect(x0, y0, w, h, 14) : x.rect(x0, y0, w, h); };
    x.fillStyle = noy ? 'rgba(24,10,56,.58)' : 'rgba(52,10,32,.64)'; forme(); x.fill();   // base sombre : la teinte ne vire pas au gris-brun sur le vert du tableau
    x.fillStyle = g; forme(); x.fill();
    x.save(); forme(); x.clip();
    const hl = x.createRadialGradient(x0 + w * .22, y0 + h * .12, 4, x0 + w * .22, y0 + h * .12, Math.max(w, h) * .7);
    hl.addColorStop(0, noy ? 'rgba(225,200,255,.20)' : 'rgba(255,215,190,.20)'); hl.addColorStop(1, 'rgba(255,255,255,0)');
    x.fillStyle = hl; x.fillRect(x0, y0, w, h);
    x.fillStyle = noy ? 'rgba(235,215,255,.16)' : 'rgba(255,220,225,.16)';
    for (let i = 0; i < 46; i++) { x.beginPath(); x.arc(x0 + (i * 61.7 + 23) % w, y0 + (i * 139.3 + 11) % h, 1 + (i % 3) * .5, 0, TAU); x.fill(); }   // granulations fixes
    x.restore();
    x.strokeStyle = noy ? 'rgba(192,132,252,.55)' : 'rgba(251,113,133,.5)'; x.lineWidth = 1.4; forme(); x.stroke();
    x.restore();
  }

  /** Hématie : f = 0 disque biconcave (vue de face, centre plus clair) ; f = 1 faucille. ang = orientation. */
  function hematie(x, cx, cy, r, f = 0, ang = 0, a = 1) {
    x.save(); x.globalAlpha *= a; x.translate(cx, cy); x.rotate(ang);
    if (f < .5) {
      x.fillStyle = 'rgba(0,0,0,.28)'; x.beginPath(); x.ellipse(r * .1, r * .16, r, r * (1 - f * .6), 0, 0, TAU); x.fill();   // ombre (17 novembre 2026)
      const g = x.createRadialGradient(0, 0, r * .1, 0, 0, r);
      g.addColorStop(0, '#b91c1c'); g.addColorStop(.38, '#ef4444'); g.addColorStop(.8, '#f43f3f'); g.addColorStop(1, '#991b1b');   // creux central sombre, bourrelet vif
      x.fillStyle = g; x.beginPath(); x.ellipse(0, 0, r, r * (1 - f * .6), 0, 0, TAU); x.fill();
      x.strokeStyle = 'rgba(255,220,220,.55)'; x.lineWidth = Math.max(1, r * .13); x.lineCap = 'round'; x.beginPath(); x.ellipse(0, 0, r * .74, r * .74 * (1 - f * .6), 0, Math.PI * 1.1, Math.PI * 1.55); x.stroke();
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
    const g = x.createLinearGradient(0, y - h, 0, y + h); g.addColorStop(0, 'rgba(254,205,160,.42)'); g.addColorStop(.5, 'rgba(254,240,200,.24)'); g.addColorStop(1, 'rgba(254,190,150,.44)');   // plasma jaune pâle
    x.fillStyle = g; x.beginPath(); haut.forEach(([px, py], i) => (i ? x.lineTo(px, py) : x.moveTo(px, py))); for (let i = bas.length - 1; i >= 0; i--) x.lineTo(bas[i][0], bas[i][1]); x.closePath(); x.fill();
    x.lineCap = 'round'; x.lineJoin = 'round';
    for (const [lw, col] of [[7, '#9f1239'], [4.6, '#fb7185'], [1.4, 'rgba(255,228,230,.8)']]) {   // paroi en volume (17 novembre 2026)
      x.strokeStyle = col; x.lineWidth = lw;
      for (const ligne of [haut, bas]) { x.beginPath(); ligne.forEach(([px, py], i) => (i ? x.lineTo(px, py - (lw < 2 ? 1 : 0)) : x.moveTo(px, py - (lw < 2 ? 1 : 0)))); x.stroke(); }
    }
    x.restore();
    return ht;
  }
  /** Point noir d’autoradiographie (grain d’argent) — quelques pixels sombres et flous. */
  function grain(x, px, py, a = 1) { x.save(); x.globalAlpha *= a; x.fillStyle = 'rgba(10,10,10,.9)'; x.beginPath(); x.arc(px, py, 2.1, 0, TAU); x.fill(); x.fillStyle = 'rgba(10,10,10,.35)'; x.beginPath(); x.arc(px + .8, py - .6, 3.4, 0, TAU); x.fill(); x.restore(); }

  window.Molecules = { PLANCHER, echelleEcran, taillePeinte, gabarit, base, gabaritNucleotide, gabaritAnticodon, arntHauteur, perleRayon, pastille, encre, lettreSur, ENCRE, BASE, COMP_ADN, COMP_ARN, AA, CODE, traduire, couleurAA, sphere, ombre, brin, nucleotide, ribosome, arnt, perle, chaine,
    noyau, pore, cytoplasme, milieu, hematie, vaisseau, grain };
  window.Lexique = window.Lexique || {}; window.Lexique.genetique = window.Molecules;
})();
