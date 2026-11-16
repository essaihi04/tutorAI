/*
 * Tableau — kit commun des laboratoires « dessinés au tableau ».
 *
 *   Tableau.Craie       : dessin à la craie sur un canvas (traits tremblés, flèches, cadres, écriture).
 *                         Le dessin s'écrit EN DIRECT : chaque trait se trace, chaque texte s'écrit lettre
 *                         par lettre, dans l'ordre des appels, comme un professeur au tableau.
 *   Tableau.ecrire      : écrit un texte HTML lettre par lettre (bulle, titre, question).
 *   Tableau.protocole   : pont avec le tuteur (manifeste, état, commandes `simulation_control`),
 *                         le bouton visé clignote quand la commande arrive (le professeur « appuie »).
 *   Tableau.boutons     : barre de boutons à la craie marqués `data-professor-control`.
 *   Tableau.onglets     : choix d'expérience (une craie soulignée), marqués `data-variant`.
 *   Tableau.curseur     : un réglage (trait de craie + point).
 *   Tableau.glisser     : poignées déplaçables directement sur le dessin (moins de boutons).
 *   Tableau.nombre      : lecture d'une saisie « 0,020 » → 0.02 ;  Tableau.fr : format français.
 *   Repères pointables  : craie.repere(id, x, y, w, h, label) pendant le dessin (ou Tableau.reperes({id: {label, rect}})) ;
 *                         le professeur animé vole jusqu'au repère et le montre du doigt (commande `highlight`
 *                         {target: id}), le kit l'entoure à la craie (Tableau.surligner). Tableau.explication(...)
 *                         donne au tuteur le script d'explication (repère → phrase), envoyé dans le manifeste.
 *
 * Écriture en direct — dans la boucle de rendu :
 *     craie.debut(graine, tempsDepuisOuvertureDeLaScene)   // secondes ; omis = tout est déjà écrit
 *     craie.texte(...); craie.ligne(...); …                 // chaque appel prend sa place dans le temps
 *     craie.direct(() => { … })                             // parties animées (dessinées d'un coup)
 *     if (!craie.fin()) requestAnimationFrame(...)          // fin() dessine le bout de craie, renvoie « tout écrit ? »
 *
 * Chaque page charge aussi /media/simulations/professor-locate.js : le professeur animé localise
 * le bouton d'une commande, vole jusqu'à lui et l'appuie avant que la commande ne parte.
 */
(function () {
  'use strict';
  if (window.Tableau) return;

  const COULEURS = {
    blanc: '#e2e8f0', cyan: '#22d3ee', jaune: '#facc15', vert: '#4ade80', violet: '#c084fc',
    orange: '#fb923c', bleu: '#60a5fa', rouge: '#f87171', rose: '#f472b6',
    faible: 'rgba(226,232,240,.5)', tresfaible: 'rgba(226,232,240,.22)',
  };
  const POLICE = "'Patrick Hand','Caveat','Segoe Print','Bradley Hand','Chalkboard SE','Comic Sans MS',cursive";
  const VITESSE_TRAIT = 650;   // px de craie par seconde
  const VITESSE_LETTRES = 16;  // lettres par seconde
  const REDUIT = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Générateur déterministe : le tremblement d'un trait ne change pas d'une image à l'autre.
  function graine(seed) {
    let s = (seed >>> 0) || 1;
    return () => { s = (Math.imul(s, 1664525) + 1013904223) >>> 0; return s / 4294967296; };
  }
  const fr = (v, d = 2) => (Number.isFinite(v) ? v.toFixed(d).replace('.', ',') : '—');
  const nombre = (s) => { const t = String(s ?? '').trim().replace(',', '.').replace(/\s/g, ''); return t ? Number(t) : NaN; };

  class Craie {
    constructor(canvas, options = {}) {
      this.canvas = canvas; this.ctx = canvas.getContext('2d'); this.W = 0; this.H = 0;
      this.onresize = options.onresize || null; this.r = graine(1);
      this.t = Infinity; this.cur = 0; this.tip = null; this.complet = true;
      this._ro = new ResizeObserver(() => this.resize()); this._ro.observe(canvas);
      this.resize();
      if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => this.onresize && this.onresize());
    }
    /**
     * Le plancher du texte (px écran) que chaque labo fixe (`craie.tailleMin = 18`) suit la taille du tableau
     * (16 novembre 2026, téléphone en paysage) : sur un petit tableau, le dessin rétrécit et un texte gardé à 18 px
     * déborde sur ses voisins. En dessous de 900 × 400 px, le plancher baisse dans la même proportion (jamais sous
     * 60 %). Relire puis remettre la valeur (`const t = c.tailleMin; … c.tailleMin = t`) ne la réduit pas deux fois.
     */
    get tailleMin() {
      const brut = this._tailleMinBrut || 0;
      if (!brut) return brut;
      const f = Math.min(1, Math.max(.6, Math.min((this.W || 900) / 900, (this.H || 400) / 400)));
      const rendu = brut * f;
      this._tailleMinLu = [brut, rendu];
      return rendu;
    }
    set tailleMin(v) {
      const lu = this._tailleMinLu;
      this._tailleMinBrut = lu && v === lu[1] ? lu[0] : v;
    }
    resize() {
      const rect = this.canvas.getBoundingClientRect(), d = devicePixelRatio || 1;
      this.W = rect.width; this.H = rect.height;
      this.canvas.width = Math.max(1, Math.round(rect.width * d)); this.canvas.height = Math.max(1, Math.round(rect.height * d));
      if (this.onresize) this.onresize();
    }
    /** Efface et prépare une image ; `seed` fixe le tremblement, `temps` (s) fait avancer l'écriture en direct. */
    debut(seed = 1, temps) {
      const c = this.ctx, d = devicePixelRatio || 1;
      c.setTransform(d, 0, 0, d, 0, 0); c.clearRect(0, 0, this.W, this.H);
      c.lineCap = 'round'; c.lineJoin = 'round'; c.globalAlpha = 1; this.r = graine(seed);
      this.t = REDUIT || temps === undefined ? Infinity : Math.max(0, temps); this.cur = 0; this.tip = null; this.complet = true;
      this._reperesImage = new Set();   // les repères de cette image ; ceux de l'image précédente non redessinés seront oubliés à fin()
      return this;
    }
    /** Dessine le bout de craie au point d'écriture ; renvoie true quand tout est écrit. */
    fin() {
      // Un repère d'une variante précédente, non redessiné dans cette image, n'est plus pointable.
      if (this._reperesImage) for (const id of Object.keys(REPERES)) { if (REPERES[id].craie === this && !this._reperesImage.has(id)) delete REPERES[id]; }
      if (this.tip) {
        const c = this.ctx, [x, y] = this.tip;
        c.globalAlpha = .9; c.fillStyle = '#fff'; c.shadowColor = '#fff'; c.shadowBlur = 8;
        c.beginPath(); c.arc(x, y, 2.2, 0, Math.PI * 2); c.fill(); c.shadowBlur = 0; c.globalAlpha = 1;
      }
      return this.complet;
    }
    /** Durée totale (s) de l'écriture d'une image : rejouer `debut` avec ce temps l'affiche entière. */
    duree() { return this.cur; }
    /** Un silence : le professeur marque une pause avant le trait suivant. */
    pause(s = .3) { if (Number.isFinite(this.t)) this.cur += s; return this; }
    /** Un élément apparu plus tard (à `apparu` s de la scène) s'écrit à partir de cet instant, pas d'un coup. */
    depuis(apparu) { if (Number.isFinite(this.t) && Number.isFinite(apparu)) this.cur = Math.max(this.cur, apparu); return this; }
    /** Dessine `fn` d'un coup, hors séquence (éléments animés : impulsion, aiguille, particules). */
    direct(fn) { const t = this.t, cur = this.cur; this.t = Infinity; try { fn(this); } finally { this.t = t; this.cur = cur; } return this; }
    /** Place un élément dans le temps : renvoie sa part écrite, de 0 à 1. */
    _part(duree) {
      if (!Number.isFinite(this.t)) return 1;
      const debut = this.cur; this.cur += Math.max(.02, duree);
      if (this.t >= this.cur) return 1;
      this.complet = false;
      return this.t <= debut ? 0 : (this.t - debut) / (this.cur - debut);
    }
    couleur(c) { return COULEURS[c] || c || COULEURS.blanc; }
    /** Trait de craie passant par `points` ([[x,y],…]) : deux passes, léger tremblement, tracé progressif. */
    trait(points, o = {}) {
      const c = this.ctx, largeur = o.largeur ?? 2.4, tremble = (o.tremble ?? 1) * .55;
      if (points.length < 2) return this;
      const src = o.ferme ? points.concat([points[0]]) : points;
      let L = 0; for (let i = 0; i < src.length - 1; i++) L += Math.hypot(src[i + 1][0] - src[i][0], src[i + 1][1] - src[i][1]);
      const part = this._part(o.duree ?? Math.max(.08, L / VITESSE_TRAIT));
      if (part <= 0) return this;
      const limite = L * part, pts = []; let parcouru = 0;
      for (let i = 0; i < src.length - 1 && parcouru < limite; i++) {
        const [x1, y1] = src[i], [x2, y2] = src[i + 1], seg = Math.hypot(x2 - x1, y2 - y1), n = Math.max(1, Math.ceil(seg / 14));
        for (let j = 0; j < n; j++) {
          const t = j / n, pos = parcouru + seg * t;
          if (pos > limite) break;
          pts.push([x1 + (x2 - x1) * t + (this.r() - .5) * tremble, y1 + (y2 - y1) * t + (this.r() - .5) * tremble]);
        }
        if (parcouru + seg <= limite) pts.push([x2, y2]);
        else { const f = (limite - parcouru) / seg; pts.push([x1 + (x2 - x1) * f, y1 + (y2 - y1) * f]); }
        parcouru += seg;
      }
      if (pts.length < 2) return this;
      if (part < 1) this.tip = pts[pts.length - 1];
      c.strokeStyle = this.couleur(o.couleur); c.setLineDash(o.pointille || []);
      for (const [w, a] of [[largeur, o.alpha ?? .92], [largeur * .5, .3]]) {
        c.globalAlpha = a; c.lineWidth = w; c.beginPath();
        pts.forEach(([x, y], i) => (i ? c.lineTo(x + (w === largeur ? 0 : .6), y + (w === largeur ? 0 : -.5)) : c.moveTo(x, y)));
        c.stroke();
      }
      c.globalAlpha = 1; c.setLineDash([]);
      return this;
    }
    ligne(x1, y1, x2, y2, o) { return this.trait([[x1, y1], [x2, y2]], o); }
    /** Flèche simple (tête à l'arrivée). */
    fleche(x1, y1, x2, y2, o = {}) {
      const a = Math.atan2(y2 - y1, x2 - x1), t = o.tete ?? 11;
      this.ligne(x1, y1, x2, y2, o);
      this.trait([[x2 - t * Math.cos(a - .45), y2 - t * Math.sin(a - .45)], [x2, y2], [x2 - t * Math.cos(a + .45), y2 - t * Math.sin(a + .45)]], { ...o, duree: .1 });
      return this;
    }
    /** Cote ↔ entre deux points, texte au milieu (au-dessus par défaut, `dessous` sinon). */
    cote(x1, y1, x2, y2, texte, o = {}) {
      const a = Math.atan2(y2 - y1, x2 - x1), t = 9;
      this.ligne(x1, y1, x2, y2, o);
      for (const [x, y, s] of [[x1, y1, 1], [x2, y2, -1]]) {
        this.trait([[x + s * t * Math.cos(a - .5), y + s * t * Math.sin(a - .5)], [x, y], [x + s * t * Math.cos(a + .5), y + s * t * Math.sin(a + .5)]], { ...o, duree: .08 });
      }
      if (texte) this.texte(texte, (x1 + x2) / 2, (y1 + y2) / 2 + (o.dessous ? 20 : -8), { couleur: o.couleur, align: 'center', taille: o.taille });
      return this;
    }
    /** Cadre arrondi tracé à main levée (`fond` : couleur de remplissage légère). */
    rect(x, y, w, h, o = {}) {
      const r = Math.min(o.arrondi ?? 8, w / 2, h / 2), pts = [];
      const coin = (cx, cy, a0) => { for (let i = 0; i <= 4; i++) { const a = a0 + i / 4 * Math.PI / 2; pts.push([cx + r * Math.cos(a), cy + r * Math.sin(a)]); } };
      coin(x + w - r, y + r, -Math.PI / 2); coin(x + w - r, y + h - r, 0); coin(x + r, y + h - r, Math.PI / 2); coin(x + r, y + r, Math.PI);
      if (o.fond) { const c = this.ctx; c.globalAlpha = o.fondAlpha ?? .12; c.fillStyle = this.couleur(o.fond); c.beginPath(); pts.forEach(([px, py], i) => (i ? c.lineTo(px, py) : c.moveTo(px, py))); c.closePath(); c.fill(); c.globalAlpha = 1; }
      return this.trait(pts, { ...o, ferme: true });
    }
    cercle(cx, cy, r, o = {}) {
      const pts = []; const n = Math.max(16, Math.round(r / 2));
      for (let i = 0; i <= n; i++) { const a = i / n * Math.PI * 2 + (o.depart ?? -.3); pts.push([cx + r * Math.cos(a), cy + r * Math.sin(a)]); }
      if (o.fond) { const c = this.ctx; c.globalAlpha = o.fondAlpha ?? .15; c.fillStyle = this.couleur(o.fond); c.beginPath(); c.arc(cx, cy, r, 0, Math.PI * 2); c.fill(); c.globalAlpha = 1; }
      return this.trait(pts, o);
    }
    /** Courbe : `fn(u)` renvoie [x, y] pour u de 0 à 1 (ou null pour sauter). */
    courbe(fn, n, o = {}) { const pts = []; for (let i = 0; i <= n; i++) { const p = fn(i / n); if (p) pts.push(p); } return this.trait(pts, { tremble: .4, ...o }); }
    point(x, y, r = 4, couleur = 'blanc') {
      if (this._part(.06) <= 0) return this;
      const c = this.ctx; c.fillStyle = this.couleur(couleur); c.globalAlpha = .95; c.beginPath(); c.arc(x, y, r, 0, Math.PI * 2); c.fill(); c.globalAlpha = 1; return this;
    }
    /** Écriture à la craie, lettre par lettre. Options : couleur, taille, align, base, alpha, gras, max (largeur max). */
    /** « y_M(t) », « t_S », « x_{AB} » : la lettre suivie d'un indice, écrit plus petit et plus bas (jamais de « _ » au tableau). */
    static segments(s) {
      const out = [], re = /([A-Za-zτθΔλωφ])_(\{[^}]+\}|[A-Za-z0-9]+)/g; let i = 0, m;
      while ((m = re.exec(s))) {
        if (m.index > i) out.push({ t: s.slice(i, m.index), sub: false });
        out.push({ t: m[1], sub: false }); out.push({ t: m[2].replace(/[{}]/g, ''), sub: true }); i = re.lastIndex;
      }
      if (i < s.length) out.push({ t: s.slice(i), sub: false });
      return out;
    }
    _texteIndices(s, x, y, o, taille) {
      const c = this.ctx, segs = Craie.segments(s), police = (t) => `${o.gras ? '700 ' : ''}${t}px ${POLICE}`;
      const petit = taille * .62, largeur = (seg) => { c.font = police(seg.sub ? petit : taille); return c.measureText(seg.t).width; };
      let total = segs.reduce((w, seg) => w + largeur(seg), 0);
      if (o.max && total > o.max) { taille = Math.max(10, taille * o.max / total); return this._texteIndices(s, x, y, { ...o, max: 0 }, taille); }
      const plain = segs.map(seg => seg.t).join('');
      const part = this._part(o.duree ?? Math.max(.1, plain.length / VITESSE_LETTRES));
      if (part <= 0) return this;
      let reste = part < 1 ? Math.max(1, Math.ceil(part * plain.length)) : plain.length;
      c.fillStyle = this.couleur(o.couleur); c.globalAlpha = o.alpha ?? .96; c.textBaseline = o.base || 'alphabetic';
      c.shadowColor = 'rgba(255,255,255,.25)'; c.shadowBlur = 1; c.textAlign = 'left';
      let px = (o.align === 'center') ? x - total / 2 : (o.align === 'right') ? x - total : x;
      for (const seg of segs) {
        if (reste <= 0) break;
        const t = seg.t.slice(0, reste); reste -= seg.t.length;
        c.font = police(seg.sub ? petit : taille);
        c.fillText(t, px, y + (seg.sub ? taille * .28 : 0));
        px += c.measureText(t).width;
        if (t.length < seg.t.length) break;
      }
      if (part < 1) this.tip = [px, y - taille * .3];
      c.shadowBlur = 0; c.globalAlpha = 1;
      return this;
    }
    /**
     * Garde-fou (8 novembre 2026, « sens de propagation » caché sous la barre) : un labo qui déclare son cadre
     * (`craie.cadre = { w, h, haut }`, `haut` = zone réservée à la barre du bouton) est prévenu dans la console de
     * tout texte qui en sort. `window.__horsCadre` garde la liste pour les vérifications automatiques.
     */
    _verifierCadre(s, x, y, taille, align) {
      const k = this.cadre; if (!k) return;
      const l = this.ctx.measureText(s).width, x0 = align === 'center' ? x - l / 2 : align === 'right' ? x - l : x;
      if (x0 < -2 || x0 + l > k.w + 2 || y - taille < (k.haut ?? 0) || y + taille * .3 > k.h + 2) {
        (window.__horsCadre ||= []).includes(s) || (window.__horsCadre.push(s), console.warn('[tableau] texte hors cadre :', s, { x: Math.round(x0), y: Math.round(y), largeur: Math.round(l) }));
      }
    }
    texte(s, x, y, o = {}) {
      const c = this.ctx; let taille = o.taille ?? 18; s = String(s);
      c.font = `${o.gras ? '700 ' : ''}${taille}px ${POLICE}`; this._verifierCadre(s.replace(/_/g, ''), x, y, taille, o.align);
      if (this.echelle && this.tailleMin && /_/.test(s)) taille = Math.max(taille, this.tailleMin / this.echelle);
      if (/[A-Za-zτθΔλωφ]_/.test(s)) return this._texteIndices(s, x, y, o, taille);
      // Petit écran : un labo peut fixer `craie.echelle` (facteur appliqué au repère) et `craie.tailleMin` (px écran) pour rester lisible.
      if (this.echelle && this.tailleMin) taille = Math.max(taille, this.tailleMin / this.echelle);
      c.font = `${o.gras ? '700 ' : ''}${taille}px ${POLICE}`;
      if (o.max && c.measureText(s).width > o.max) { taille = Math.max(10, taille * o.max / c.measureText(s).width); c.font = `${o.gras ? '700 ' : ''}${taille}px ${POLICE}`; }
      const part = this._part(o.duree ?? Math.max(.1, s.length / VITESSE_LETTRES));
      if (part <= 0) return this;
      const n = part < 1 ? Math.max(1, Math.ceil(part * s.length)) : s.length, visible = s.slice(0, n);
      c.fillStyle = this.couleur(o.couleur); c.globalAlpha = o.alpha ?? .96; c.textAlign = o.align || 'left'; c.textBaseline = o.base || 'alphabetic';
      c.shadowColor = 'rgba(255,255,255,.25)'; c.shadowBlur = 1;
      // Le texte s'écrit depuis le début même s'il est centré : on fixe son point de départ sur le texte complet.
      const largeurTotale = c.measureText(s).width, depart = c.textAlign === 'center' ? x - largeurTotale / 2 : c.textAlign === 'right' ? x - largeurTotale : x;
      c.textAlign = 'left'; c.fillText(visible, depart, y);
      if (part < 1) this.tip = [depart + c.measureText(visible).width, y - taille * .3];
      c.shadowBlur = 0; c.globalAlpha = 1; c.textAlign = 'left'; c.textBaseline = 'alphabetic';
      return this;
    }
    /** Déclare un repère pointable par le professeur, en coordonnées du dessin courant (transformées en px de la page). */
    repere(id, x, y, w, h, label) {
      const m = this.ctx.getTransform(), d = devicePixelRatio || 1, b = this.canvas.getBoundingClientRect();
      const p1 = m.transformPoint(new DOMPoint(x, y)), p2 = m.transformPoint(new DOMPoint(x + w, y + h));
      const r = { x: b.left + Math.min(p1.x, p2.x) / d, y: b.top + Math.min(p1.y, p2.y) / d, width: Math.abs(p2.x - p1.x) / d, height: Math.abs(p2.y - p1.y) / d };
      const existant = REPERES[id] || {};
      REPERES[id] = { label: label || existant.label || id, rect: r, craie: this };
      if (this._reperesImage) this._reperesImage.add(id);
      return this;
    }
    largeurTexte(s, taille = 18) { this.ctx.font = `${taille}px ${POLICE}`; return this.ctx.measureText(String(s)).width; }
    /** Axe gradué : de (x0,y0) vers (x1,y1), `graduations` = [[fraction, libellé], …]. */
    axe(x0, y0, x1, y1, graduations = [], o = {}) {
      this.fleche(x0, y0, x1, y1, { couleur: o.couleur || 'faible', largeur: 1.6 });
      const a = Math.atan2(y1 - y0, x1 - x0), nx = Math.sin(a) * 5, ny = -Math.cos(a) * 5;
      for (const [f, lib] of graduations) {
        const x = x0 + (x1 - x0) * f, y = y0 + (y1 - y0) * f;
        this.ligne(x - nx, y - ny, x + nx, y + ny, { couleur: o.couleur || 'faible', largeur: 1.4, duree: .04 });
        if (lib != null) this.texte(lib, x + (o.vertical ? -10 : 0), y + (o.vertical ? 5 : 20), { couleur: o.couleur || 'faible', taille: o.taille ?? 14, align: o.vertical ? 'right' : 'center', duree: .12 });
      }
      return this;
    }
  }

  // ── Repères pointables et script d'explication ───────────────────────────
  const REPERES = {};           // id → { label, rect: {x,y,width,height} en px de la page | () => rect | HTMLElement }
  let EXPLICATION = null;       // [{ repere, texte, variante? }] ou { variante: [{ repere, texte }] }
  /** Enregistre des repères DOM ou calculés : `{ id: { label, rect: () => ({x,y,width,height}) | HTMLElement } }`. */
  function reperes(defs) { for (const [id, d] of Object.entries(defs || {})) REPERES[id] = { label: d.label || id, rect: d.rect || d.element || d }; }
  /** Un panneau HTML marqué `data-professor-point="id"` (libellé : data-professor-label, son titre, ou l'id). */
  function elementRepere(id) {
    const sel = String(id || '').replace(/[^\w-]/g, '');
    return sel ? document.querySelector(`[data-professor-point~="${sel}"]`) : null;
  }
  /** Rectangle (px de la page) d'un repère dessiné ou d'un panneau HTML, ou null. */
  function rectRepere(id) {
    const r = REPERES[String(id || '')];
    let rect = r ? (typeof r.rect === 'function' ? r.rect() : r.rect) : elementRepere(id);
    if (rect && rect.getBoundingClientRect) rect = rect.getBoundingClientRect();
    if (!rect || !(rect.width > 0) || !(rect.height > 0)) return null;
    return { x: rect.x ?? rect.left, y: rect.y ?? rect.top, width: rect.width, height: rect.height };
  }
  /** Libellés des repères (dessinés et panneaux HTML), pour le manifeste. */
  function listeReperes() {
    const out = {};
    for (const [id, r] of Object.entries(REPERES)) out[id] = r.label;
    document.querySelectorAll('[data-professor-point]').forEach((el) => {
      for (const id of el.dataset.professorPoint.split(/\s+/)) {
        if (id && !out[id]) out[id] = el.dataset.professorLabel || el.querySelector('h2, h3, summary')?.textContent?.trim() || el.getAttribute('aria-label') || id;
      }
    });
    return out;
  }
  /** Script d'explication de la simulation pour le tuteur : il dit chaque phrase en pointant le repère. */
  function explication(script) { EXPLICATION = script; }
  // ── Entourage à la craie : il serre le repère sans empiéter sur ses voisins ──
  const inter = (a, b) => a.l < b.r && b.l < a.r && a.t < b.b && b.t < a.b;
  const boite = (r) => ({ l: r.left ?? r.x, t: r.top ?? r.y, r: (r.left ?? r.x) + r.width, b: (r.top ?? r.y) + r.height });
  /** Boîtes (px de la page) des autres éléments visibles : repères voisins, textes HTML/SVG, images, boutons. */
  function obstacles(id, cible) {
    const out = [], c = boite(cible), el = elementRepere(id);
    const contient = (a, b) => a.l <= b.l + 1 && a.r >= b.r - 1 && a.t <= b.t + 1 && a.b >= b.b - 1;
    const ajouter = (o) => {
      if (!(o.r - o.l > 0.5 && o.b - o.t > 0.5)) return;
      if (contient(o, c) || contient(c, o)) return;           // un cadre qui contient le repère, ou un morceau du repère
      out.push(o);
    };
    for (const k of Object.keys(REPERES)) { if (k !== String(id)) { const r = rectRepere(k); if (r) ajouter(boite(r)); } }
    const feuilles = document.body.querySelectorAll('h1,h2,h3,h4,p,span,li,td,th,label,button,small,strong,em,b,i,sub,sup,output,figcaption,legend,summary,img,svg text,svg image,.katex,mjx-container,[data-professor-point]');
    for (const n of feuilles) {
      if (n.closest('.repere-anneau') || (el && (el.contains(n) || n.contains(el)))) continue;
      if (!n.closest('svg') && !n.matches('img') && !n.textContent.trim()) continue;
      const cs = getComputedStyle(n); if (cs.visibility === 'hidden' || cs.display === 'none' || +cs.opacity === 0) continue;
      ajouter(boite(n.getBoundingClientRect()));
    }
    return out;
  }
  /** Distance (px) jusqu'à la première trace de craie sur la toile du repère, de chaque côté, jusqu'à `max`. */
  function encreAutour(id, c, max) {
    const libre = { l: max, t: max, r: max, b: max }, cr = REPERES[id] && REPERES[id].craie;
    if (!cr || !cr.canvas) return libre;
    try {
      const cv = cr.canvas, br = cv.getBoundingClientRect(), d = cv.width / Math.max(1, br.width);
      const x0 = Math.max(0, Math.floor((c.l - max - br.left) * d)), y0 = Math.max(0, Math.floor((c.t - max - br.top) * d));
      const x1 = Math.min(cv.width, Math.ceil((c.r + max - br.left) * d)), y1 = Math.min(cv.height, Math.ceil((c.b + max - br.top) * d));
      if (x1 <= x0 || y1 <= y0) return libre;
      const px = cv.getContext('2d').getImageData(x0, y0, x1 - x0, y1 - y0).data, w = x1 - x0;
      const encre = (X, Y) => { const i = ((Y - y0) * w + (X - x0)) * 4 + 3; return px[i] > 60; };
      const cl = (c.l - br.left) * d, ct = (c.t - br.top) * d, crr = (c.r - br.left) * d, cb = (c.b - br.top) * d;
      for (let Y = y0; Y < y1; Y++) for (let X = x0; X < x1; X++) {
        if (X >= cl && X < crr && Y >= ct && Y < cb) continue;            // dans le repère lui-même
        const dedansX = X >= cl - 2 && X < crr + 2, dedansY = Y >= ct - 2 && Y < cb + 2;
        if (!dedansX && !dedansY) continue;                                 // coins : non concernés par le tracé
        if (!encre(X, Y)) continue;
        if (dedansX && Y < ct) libre.t = Math.min(libre.t, (ct - Y) / d);
        if (dedansX && Y >= cb) libre.b = Math.min(libre.b, (Y - cb) / d);
        if (dedansY && X < cl) libre.l = Math.min(libre.l, (cl - X) / d);
        if (dedansY && X >= crr) libre.r = Math.min(libre.r, (X - crr) / d);
      }
    } catch (_) { /* toile illisible : on garde la marge par défaut */ }
    return libre;
  }
  /** Resserre un repère dessiné sur la craie réellement tracée dans sa boîte (les boîtes déclarées sont souvent larges). */
  function serrer(id, rect) {
    const cr = rect && REPERES[id] && REPERES[id].craie; if (!cr || !cr.canvas) return rect;
    if (cr.complet === false) return rect;                                 // craie encore en train d'écrire : la boîte déclarée fait foi
    try {
      const cv = cr.canvas, br = cv.getBoundingClientRect(), d = cv.width / Math.max(1, br.width);
      const x0 = Math.max(0, Math.floor((rect.x - br.left) * d)), y0 = Math.max(0, Math.floor((rect.y - br.top) * d));
      const x1 = Math.min(cv.width, Math.ceil((rect.x + rect.width - br.left) * d)), y1 = Math.min(cv.height, Math.ceil((rect.y + rect.height - br.top) * d));
      if (x1 <= x0 || y1 <= y0) return rect;
      const px = cv.getContext('2d').getImageData(x0, y0, x1 - x0, y1 - y0).data, w = x1 - x0;
      let l = Infinity, t = Infinity, r = -1, b = -1;
      for (let i = 3, k = 0; i < px.length; i += 4, k++) if (px[i] > 60) { const X = k % w, Y = (k / w) | 0; if (X < l) l = X; if (X > r) r = X; if (Y < t) t = Y; if (Y > b) b = Y; }
      if (r < 0) return rect;                                              // rien de tracé : on garde la boîte déclarée
      let nx = br.left + (x0 + l) / d, ny = br.top + (y0 + t) / d, nw = (r - l + 1) / d, nh = (b - t + 1) / d;
      const MIN = 14;                                                      // un point ou un trait fin garde une boîte visible
      if (nw < MIN) { nx -= (MIN - nw) / 2; nw = MIN; } if (nh < MIN) { ny -= (MIN - nh) / 2; nh = MIN; }
      return { x: nx, y: ny, width: nw, height: nh };
    } catch (_) { return rect; }
  }
  /** Vrai si la toile du repère porte de la craie dans la boîte `b` (px de la page). */
  function encreDans(id, b) {
    const cr = REPERES[id] && REPERES[id].craie; if (!cr || !cr.canvas) return false;
    try {
      const cv = cr.canvas, br = cv.getBoundingClientRect(), d = cv.width / Math.max(1, br.width);
      const x0 = Math.max(0, Math.floor((b.l - br.left) * d)), y0 = Math.max(0, Math.floor((b.t - br.top) * d));
      const x1 = Math.min(cv.width, Math.ceil((b.r - br.left) * d)), y1 = Math.min(cv.height, Math.ceil((b.b - br.top) * d));
      if (x1 <= x0 || y1 <= y0) return false;
      const px = cv.getContext('2d').getImageData(x0, y0, x1 - x0, y1 - y0).data;
      for (let i = 3; i < px.length; i += 4) if (px[i] > 60) return true;
    } catch (_) { /* toile illisible */ }
    return false;
  }
  /** Marge de chaque côté : petite, et au plus la moitié de l'écart avec le voisin le plus proche. */
  function marges(id, rect, voisins) {
    const c = boite(rect), base = Math.max(3, Math.min(7, Math.min(rect.width, rect.height) * .18)), m = { l: base, t: base, r: base, b: base };
    const encre = encreAutour(id, c, base * 2 + 2);
    for (const k of ['l', 't', 'r', 'b']) m[k] = Math.min(m[k], encre[k] / 2);
    for (const o of voisins) {
      if (inter(o, c)) continue;                                           // chevauchement déjà présent dans la page
      const recX = o.l < c.r && o.r > c.l, recY = o.t < c.b && o.b > c.t;
      if (recX && o.b <= c.t) m.t = Math.min(m.t, (c.t - o.b) / 2);
      if (recX && o.t >= c.b) m.b = Math.min(m.b, (o.t - c.b) / 2);
      if (recY && o.r <= c.l) m.l = Math.min(m.l, (c.l - o.r) / 2);
      if (recY && o.l >= c.r) m.r = Math.min(m.r, (o.l - c.r) / 2);
    }
    for (const k of ['l', 't', 'r', 'b']) m[k] = Math.max(0, m[k]);
    return m;
  }
  /** Libellé lisible d'un repère (sans la mention interne « (au moment …) ») ; vide s'il répète le texte montré. */
  function libelleCourt(id) {
    let s = REPERES[id] ? REPERES[id].label : (elementRepere(id)?.dataset.professorLabel || '');
    s = String(s || '').replace(/\s*\(au moment[^)]*\)\s*$/i, '').trim();
    return s && s !== id && s.length <= 48 ? s : '';
  }
  /** Entoure un repère à la craie pendant `duree` ms : le professeur vient de le montrer. */
  function surligner(id, duree = 4500) {
    const rect = serrer(id, rectRepere(id)); if (!rect) return false;
    document.querySelectorAll('.repere-anneau').forEach((el) => el.remove());
    const voisins = obstacles(id, rect), m = marges(id, rect, voisins);
    const w = rect.width + m.l + m.r, h = rect.height + m.t + m.b;
    // Rectangle arrondi : il suit la boîte réelle (une ellipse coupe les coins du texte et déborde sur les côtés).
    // Les rayons restent dans la marge disponible pour ne pas mordre sur le repère.
    const rayon = Math.max(2, Math.min(h / 2, w / 2, 4 + Math.min(m.l, m.t, m.r, m.b) * 1.6));
    const el = document.createElement('div'); el.className = 'repere-anneau'; el.setAttribute('aria-hidden', 'true');
    Object.assign(el.style, { left: (rect.x - m.l + scrollX) + 'px', top: (rect.y - m.t + scrollY) + 'px', width: w + 'px', height: h + 'px',
      borderRadius: `${rayon * 1.1}px ${rayon * .9}px ${rayon * 1.05}px ${rayon * .95}px` });
    document.body.append(el);
    // Le libellé ne s'écrit que dans une place libre (dessous, sinon dessus), entièrement dans l'écran.
    const label = libelleCourt(id);
    if (label) {
      const s = document.createElement('span'); s.textContent = label; el.append(s);
      const anneau = { l: rect.x - m.l, t: rect.y - m.t, r: rect.x - m.l + w, b: rect.y - m.t + h }, lw = s.offsetWidth, lh = s.offsetHeight, cx = (anneau.l + anneau.r) / 2;
      const gauche = Math.max(4, Math.min(innerWidth - 4 - lw, cx - lw / 2));
      const places = [{ t: anneau.b + 2, cote: 'dessous' }, { t: anneau.t - 2 - lh, cote: 'dessus' }];
      const ok = places.find((p) => {
        const b = { l: gauche, r: gauche + lw, t: p.t, b: p.t + lh };
        if (b.t < 0 || b.b > innerHeight || lw > innerWidth - 8) return false;
        if (voisins.some((o) => inter(o, b))) return false;
        return !encreDans(id, b);
      });
      if (ok) { s.dataset.cote = ok.cote; const bord = parseFloat(getComputedStyle(el).borderLeftWidth) || 0;
        s.style.left = (gauche - anneau.l - bord) + 'px'; s.style.top = (ok.t - anneau.t - bord) + 'px'; }
      else s.remove();
    }
    setTimeout(() => el.remove(), duree);
    return true;
  }
  const COMMANDES_POINTAGE = ['highlight', 'point', 'montrer', 'show'];
  const cibleDe = (p) => p && (p.target || p.repere || p.element || p.id || p.variant_id);

  /** Écrit `texte` dans `el` lettre par lettre (annule une écriture en cours sur le même élément). */
  function ecrire(el, texte, { vitesse = 28, apres } = {}) {
    if (!el) return;
    if (el._ecriture) { clearInterval(el._ecriture); el._ecriture = null; }
    texte = String(texte ?? '');
    if (REDUIT || !texte) { el.textContent = texte; apres && apres(); return; }
    let i = 0; el.textContent = ''; el.classList.add('en-cours');
    el._ecriture = setInterval(() => {
      i++; el.textContent = texte.slice(0, i);
      if (i >= texte.length) { clearInterval(el._ecriture); el._ecriture = null; el.classList.remove('en-cours'); apres && apres(); }
    }, 1000 / vitesse);
  }

  /** Bouton à la craie. `commande` = commandes séparées par des espaces (data-professor-control). */
  function bouton({ id, label, commande, classe = '', onclick, title, cache = false, pressed }) {
    const b = document.createElement('button');
    b.type = 'button'; b.className = ('craie-btn ' + classe).trim(); b.textContent = label;
    if (id) b.id = id; if (commande) b.dataset.professorControl = commande; if (title) b.title = title;
    if (pressed !== undefined) b.setAttribute('aria-pressed', String(pressed));
    if (cache) b.hidden = true; if (onclick) b.addEventListener('click', onclick);
    return b;
  }
  function boutons(conteneur, liste) {
    const out = {};
    for (const d of liste) {
      if (d === 'espace') { const s = document.createElement('span'); s.className = 'espace'; conteneur.append(s); continue; }
      if (d && d.nodeType) { conteneur.append(d); continue; }
      const b = bouton(d); conteneur.append(b); if (d.id) out[d.id] = b;
    }
    return out;
  }
  /** Onglets d'expériences : `variantes` = [{id, label}], `faits` = Set des validées. */
  function onglets(conteneur, variantes, actif, onSelect, faits) {
    conteneur.replaceChildren();
    for (const v of variantes) {
      const b = document.createElement('button');
      b.type = 'button'; b.className = 'onglet' + (faits && faits.has(v.id) ? ' fait' : ''); b.id = v.id; b.dataset.variant = v.id;
      b.textContent = v.label; b.setAttribute('aria-pressed', String(v.id === actif));
      b.addEventListener('click', () => onSelect(v.id)); conteneur.append(b);
    }
  }
  /** Curseur (trait de craie + point). Renvoie l'élément ; `el.maj(valeur)` pour l'actualiser. */
  function curseur({ id, label, min, max, step, valeur, unite = '', onchange, decimales, commande }) {
    const el = document.createElement('label'); el.className = 'curseur'; if (commande) el.dataset.professorControl = commande;
    const d = decimales ?? (String(step).split('.')[1] || '').length;
    el.innerHTML = `<span>${label}<b></b></span><input type="range" min="${min}" max="${max}" step="${step}" value="${valeur}" ${id ? `id="${id}" name="${id}"` : ''} aria-label="${label}">`;
    const b = el.querySelector('b'), input = el.querySelector('input');
    const maj = (v) => { if (v !== undefined) input.value = String(v); b.textContent = `${fr(Number(input.value), d)} ${unite}`.trim(); };
    input.addEventListener('input', () => maj());
    input.addEventListener('change', () => onchange && onchange(Number(input.value)));
    maj(); el.maj = maj; el.input = input; return el;
  }
  /**
   * Poignées déplaçables sur un canvas : `toucher(x,y)` → identifiant ou null, `bouger(id,x,y)`, `lacher(id)`.
   * Coordonnées en px CSS du canvas. Le curseur devient une main au survol d'une poignée.
   */
  function glisser(canvas, { toucher, bouger, lacher }) {
    let actif = null;
    const pos = (e) => { const r = canvas.getBoundingClientRect(); return [e.clientX - r.left, e.clientY - r.top]; };
    canvas.addEventListener('pointerdown', (e) => { const [x, y] = pos(e); actif = toucher(x, y); if (actif == null) return; canvas.setPointerCapture(e.pointerId); canvas.style.cursor = 'grabbing'; e.preventDefault(); });
    canvas.addEventListener('pointermove', (e) => { const [x, y] = pos(e); if (actif != null) { bouger(actif, x, y); e.preventDefault(); } else canvas.style.cursor = toucher(x, y) != null ? 'grab' : ''; });
    const fin = (e) => { if (actif == null) return; const id = actif; actif = null; canvas.style.cursor = ''; try { canvas.releasePointerCapture(e.pointerId); } catch (_) { /* déjà relâché */ } lacher && lacher(id); };
    canvas.addEventListener('pointerup', fin); canvas.addEventListener('pointercancel', fin);
  }
  /** Le bouton d'une commande clignote : le professeur vient d'appuyer dessus. */
  function appuyer(commande) {
    const cmd = String(commande || '').replace(/[^a-z_]/g, '');
    const el = cmd && document.querySelector(`[data-professor-control~="${cmd}"]`);
    if (!el) return;
    el.classList.remove('presse'); void el.offsetWidth; el.classList.add('presse');
    setTimeout(() => el.classList.remove('presse'), 500);
  }
  /**
   * Pont avec le tuteur.
   *   id, commandes, config (SIMULATION_CONFIG), texte (page_text), etat() → current_state,
   *   progression() → 0..1, executer(cmd, params).
   * Renvoie { noter, emettre, manifeste, actions }.
   */
  function protocole({ id, commandes, config, texte, etat, progression, executer }) {
    const actions = [];
    // Qui a la main : le tuteur (commande reçue) ou l'élève (il touche la page). Chaque action et l'état le disent,
    // pour que le tuteur réagisse à ce que l'élève a fait lui-même, et pas à ses propres gestes.
    let main = 'personne';                        // personne n'a encore touché la scène
    const prendreMain = () => { main = 'eleve'; };
    document.addEventListener('pointerdown', prendreMain, true);
    document.addEventListener('keydown', prendreMain, true);
    const noter = (action, details = {}) => { actions.push({ action, details, par: main, timestamp: Date.now() }); if (actions.length > 80) actions.splice(0, actions.length - 80); };
    const emettre = (extra = {}) => {
      try { parent.postMessage({ type: 'simulation_state', simulation_id: id, current_state: { ...etat(), derniere_main: main, ...extra }, student_actions: actions.slice(), objective_progress: progression(), timestamp: Date.now() }, '*'); } catch (_) { /* hors iframe */ }
    };
    const manifeste = () => {
      window.__SIMULATION_MANIFEST_SENT__ = true;
      const toutes = commandes.includes('highlight') ? commandes : commandes.concat(['highlight']);
      const schema = { ...(config.command_schema || {}) };
      if (Object.keys(REPERES).length) schema.highlight = { target: Object.keys(REPERES).join(' | ') };
      try { parent.postMessage({ type: 'simulation_manifest', simulation_id: id, capabilities: { commands: toutes, config, globals: ['executeAICommand'], command_schema: schema, state_schema: config.state_schema || {}, reperes: listeReperes(), explication: EXPLICATION || undefined }, page_text: texte }, '*'); } catch (_) { /* hors iframe */ }
    };
    window.SIMULATION_CONFIG = config;
    window.executeAICommand = (cmd, p = {}) => {
      p = p || {};
      main = 'tuteur';
      // Le professeur montre un repère du doigt : le kit l'entoure à la craie, le labo peut en faire plus.
      const pointage = COMMANDES_POINTAGE.includes(cmd) && surligner(cibleDe(p));
      if (!commandes.includes(cmd)) { if (pointage) noter('highlight', { target: cibleDe(p) }); return; }
      if (!pointage) appuyer(cmd);
      executer(cmd, p);
    };
    window.addEventListener('message', (e) => {
      if (e.source !== parent) return; const d = e.data;
      if (d && d.type === 'simulation_control' && (!d.simulation_id || d.simulation_id === id)) window.executeAICommand(d.command, d.parameters || {});
      // Le lecteur demande le manifeste à jour (les repères dessinés plus tard, après un arrêt ou une mesure).
      if (d && d.type === 'simulation_manifest_request') manifeste();
    });
    // Les repères sont connus après le premier dessin : le manifeste est renvoyé une fois complet.
    manifeste(); setTimeout(manifeste, 350); setTimeout(manifeste, 1800);
    return { noter, emettre, manifeste, actions };
  }
  /** Bulle de retour, écrite lettre par lettre (jaune ; rouge si erreur, verte si réussite). */
  function bulle(el, texte, kind = '') { if (kind) el.dataset.kind = kind; else delete el.dataset.kind; ecrire(el, texte); }

  window.Tableau = { Craie, COULEURS, POLICE, ecrire, bouton, boutons, onglets, curseur, glisser, appuyer, protocole, bulle, fr, nombre, graine,
    reperes, rectRepere, listeReperes, explication, surligner, REPERES };
})();
