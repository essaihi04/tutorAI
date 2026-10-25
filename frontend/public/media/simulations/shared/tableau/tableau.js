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
      return this;
    }
    /** Dessine le bout de craie au point d'écriture ; renvoie true quand tout est écrit. */
    fin() {
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
    texte(s, x, y, o = {}) {
      const c = this.ctx; let taille = o.taille ?? 18; s = String(s);
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
    const noter = (action, details = {}) => { actions.push({ action, details, timestamp: Date.now() }); if (actions.length > 80) actions.splice(0, actions.length - 80); };
    const emettre = (extra = {}) => {
      try { parent.postMessage({ type: 'simulation_state', simulation_id: id, current_state: { ...etat(), ...extra }, student_actions: actions.slice(), objective_progress: progression(), timestamp: Date.now() }, '*'); } catch (_) { /* hors iframe */ }
    };
    const manifeste = () => {
      window.__SIMULATION_MANIFEST_SENT__ = true;
      try { parent.postMessage({ type: 'simulation_manifest', simulation_id: id, capabilities: { commands: commandes, config, globals: ['executeAICommand'], command_schema: config.command_schema || {}, state_schema: config.state_schema || {} }, page_text: texte }, '*'); } catch (_) { /* hors iframe */ }
    };
    window.SIMULATION_CONFIG = config;
    window.executeAICommand = (cmd, p = {}) => { if (!commandes.includes(cmd)) return; appuyer(cmd); executer(cmd, p || {}); };
    window.addEventListener('message', (e) => {
      if (e.source !== parent) return; const d = e.data;
      if (d && d.type === 'simulation_control' && (!d.simulation_id || d.simulation_id === id)) window.executeAICommand(d.command, d.parameters || {});
    });
    manifeste(); setTimeout(manifeste, 350);
    return { noter, emettre, manifeste, actions };
  }
  /** Bulle de retour, écrite lettre par lettre (jaune ; rouge si erreur, verte si réussite). */
  function bulle(el, texte, kind = '') { if (kind) el.dataset.kind = kind; else delete el.dataset.kind; ecrire(el, texte); }

  window.Tableau = { Craie, COULEURS, POLICE, ecrire, bouton, boutons, onglets, curseur, glisser, appuyer, protocole, bulle, fr, nombre, graine };
})();
