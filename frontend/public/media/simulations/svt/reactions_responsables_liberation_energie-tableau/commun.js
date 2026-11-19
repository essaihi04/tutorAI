/*
 * Commun aux simulations du cours SVT « Libération de l'énergie emmagasinée dans la matière organique »
 * (2ᵉ Bac PC BIOF, 10 novembre 2026). Repris de physics/ondes-periodiques-tableau/commun.js :
 *   - Scene : cadre virtuel 760 × 420 mis à l'échelle sans rien couper, texte jamais plus petit que 15 px à l'écran,
 *     boucle d'image qui ne redessine que lorsqu'il le faut (scene.avancer(dt) renvoie true tant que ça bouge).
 *   - Chrono : la ligne de temps d'une simulation « racontée » (t de 0 à fin, en secondes de la scène), avec les
 *     commandes du tuteur start / pause / resume / set_time / play_until {moment | time_s} et le bouton unique
 *     Lancer → Pause → Reprendre → Rejouer. Les moments viennent de la page (calculés à partir de la biologie).
 *
 *   const chrono = SVTTableau.Chrono({ fin: () => 12, moments: () => ({ a: 2, b: 5 }), motifs: { a: '…' },
 *     bouton: $('run'), bulle: $('feedback'), pont: () => pont, vitesse: 1, fini: () => '…message de fin…' });
 *   scene.avancer = chrono.avancer;   // dans la boucle
 *   executer: { start: chrono.start, pause: chrono.pause, resume: chrono.resume, reset: chrono.start,
 *               set_time: () => chrono.setTime(p), play_until: () => chrono.playUntil(p) }
 *   Diapositive pilotée (17 novembre 2026) : debut: () => instant de départ (?depart=), saut: () => ecrit.rattraper(),
 *   reset: chrono.preparer (figé au départ) ; play_until accepte aussi { depuis, duree_s } ; set_time accepte { moment }.
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
    /* Courbes nettes et lumineuses (17 novembre 2026, « plus agréable, couleurs vives ») — sur demande seulement :
     * craie.courbe(fn, n, { net: true, … }) garde l'écriture progressive et la durée d'une courbe de craie, sans tremblé,
     * avec un halo doux de sa couleur. Option `aire: yBase` : aire en dégradé entre la courbe et la ligne yBase, qui se
     * remplit au rythme du tracé (aireAlpha : opacité du haut, .28 par défaut). Sans `net`, rien ne change. */
    const courbeCraie = craie.courbe;
    craie.courbe = function (fn, n, o = {}) {
      if (o.net !== true) return courbeCraie.call(this, fn, n, o);
      const ctx = this.ctx, teinte = this.couleur(o.couleur);
      if (o.aire !== undefined && !scene.mesurant) {
        const pts = []; for (let i = 0; i <= n; i++) { const p = fn(i / n); if (p) pts.push(p); }
        let L = 0; const cum = [0]; for (let i = 1; i < pts.length; i++) { L += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); cum.push(L); }
        const duree = Math.max(.02, o.duree ?? Math.max(.08, L / 650));
        const part = !Number.isFinite(this.t) || this.t >= this.cur + duree ? 1 : this.t <= this.cur ? 0 : (this.t - this.cur) / duree;
        const vus = pts.filter((_, i) => cum[i] <= L * part + 1e-9);
        if (vus.length > 1) {
          let haut = Infinity; for (const p of vus) haut = Math.min(haut, p[1]);
          const rgb = /^#[0-9a-f]{6}$/i.test(teinte) ? [1, 3, 5].map(k => parseInt(teinte.slice(k, k + 2), 16)).join(',') : '226,232,240';
          const g = ctx.createLinearGradient(0, Math.min(haut, o.aire - 1), 0, o.aire);
          g.addColorStop(0, `rgba(${rgb},${o.aireAlpha ?? .28})`); g.addColorStop(1, `rgba(${rgb},.02)`);
          ctx.save(); ctx.fillStyle = g; ctx.beginPath(); ctx.moveTo(vus[0][0], o.aire);
          for (const p of vus) ctx.lineTo(p[0], p[1]);
          ctx.lineTo(vus[vus.length - 1][0], o.aire); ctx.closePath(); ctx.fill(); ctx.restore();
        }
      }
      ctx.save(); ctx.shadowColor = teinte; ctx.shadowBlur = o.pointille ? 5 : 10;
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
      scene.mesurant = true; window.__mesureEnCours = true; scene.ouvert = -1e9;
      try { (options.complet || (f => f()))(() => dessiner(craie, scene)); } catch (e) { console.warn('[tableau] mesure de la boîte', e); }
      finally { craie.trait = trait; craie.texte = texte; craie.point = point; scene.mesurant = false; window.__mesureEnCours = false; scene.ouvert = t; }
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
        /* Le kit baisse le plancher du texte dès que le tableau fait moins de 900 × 400 (téléphone). Le cadre que le lecteur
         * donne à la simulation sur un bureau peu haut, à côté de la colonne des cartes (≈ 850 × 350), est encore un bureau :
         * le texte y reste à 15 px au moins (la simulation d'abord, 18 novembre 2026) ; sous ~75 %, la baisse du kit joue. */
        const fPlancher = Math.min(1, Math.max(.45, Math.min((W || 900) / 900, (H || 400) / 400)));
        craie.echelle = s; craie.tailleMin = fPlancher >= .75 ? TAILLE_MIN / fPlancher : TAILLE_MIN;
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

  const fr = (v, d = 1) => (Number.isFinite(v) ? v.toFixed(d).replace('.', ',') : '—');

  /* Ligne de temps pilotable par le tuteur. Toutes les durées en secondes de la scène. */
  function Chrono(o) {
    const C = { t: 0, running: false, jusqua: null, motif: '', fait: false, emis: 0, v: 1, suspendu: null, fige: false };
    const pont = () => (o.pont ? o.pont() : null);
    const noter = (a, d) => { const p = pont(); if (p) { p.noter(a, d); p.emettre(); } };
    const texteBouton = (s) => { if (o.bouton) o.bouton.textContent = s; };
    const dire = (s, kind) => { if (o.bulle && s) window.Tableau.bulle(o.bulle, s, kind); };
    const fin = () => o.fin();
    /* Le point de départ de la diapositive (17 novembre 2026), option `debut: () => instant` : une page ouverte avec
     * ?depart=<moment> commence figée sur cet instant, tout ce qui précède déjà au tableau ; `start` et `preparer` (reset)
     * y reviennent au lieu de zéro. (`depart` reste le texte de la bulle au lancement.) */
    const PARAM = new URLSearchParams(location.search).get('depart');
    C.pilote = !!o.debut || PARAM != null;     // la diapositive pilote la scène : pas de lancement automatique
    /* Un instant donné par son nom de moment ou en secondes. */
    const instantDe = (v) => { if (v == null || v === '') return NaN; const M = o.moments(); return v in M ? +M[v] : +v; };
    const depart = () => Math.max(0, Math.min(fin(), +(o.debut ? o.debut() : instantDe(PARAM)) || 0));
    /* Un saut dans le temps : ce qui est déjà arrivé est au tableau tout de suite (pas réécrit trait par trait). */
    const sauter = (t) => { C.t = Math.min(fin(), Math.max(0, t)); if (C.t > 0) { APPARITIONS.forEach(a => a.rattraper()); o.saut && o.saut(); } };
    C.avancer = (dt) => {
      if (!C.running) return false;
      C.t = Math.min(fin(), C.t + dt * (o.vitesse || 1) * (C.v || 1));
      if (C.jusqua != null && C.t >= C.jusqua) {
        C.t = C.jusqua; C.running = false; C.jusqua = null; C.v = 1; texteBouton('Reprendre');
        dire('Arrêt sur image : ' + (C.motif || `t = ${fr(C.t)} s`) + '.');
        noter('pause', { time_s: +C.t.toFixed(2) });
        o.apres && o.apres();
        return true;
      }
      if (C.t >= fin()) { C.running = false; C.fait = true; C.v = 1; texteBouton('Rejouer'); dire(o.fini ? o.fini() : 'Terminé.', 'good'); noter('fin', {}); o.apres && o.apres(); }
      else if (performance.now() - C.emis > 500) { C.emis = performance.now(); const p = pont(); p && p.emettre(); }
      return true;
    };
    C.start = () => {
      C.jusqua = null; C.suspendu = null; C.fige = false; C.v = 1; C.running = true; C.fait = false; texteBouton('Pause'); dire(depart() > 0 ? 'Observe…' : (o.depart || 'Observe…'));
      o.reinit && o.reinit(); const d = depart(); if (d > 0) sauter(d); else C.t = 0; noter('start', {});
    };
    /* Revient au point de départ, figé (reset d'une diapositive pilotée : Réécouter rejoue la voix et ses commandes). */
    C.preparer = () => {
      C.running = false; C.jusqua = null; C.suspendu = null; C.fige = false; C.v = 1; C.fait = false;
      o.reinit && o.reinit(); sauter(depart()); texteBouton(C.t > 0 ? 'Reprendre' : 'Lancer');
      const M = o.moments(), nom = Object.keys(M).find(k => Math.abs(M[k] - C.t) < 1e-6);
      if (C.t > 0) dire('Arrêt sur image : ' + ((nom && (o.motifs || {})[nom]) || `t = ${fr(C.t)} s`) + '.');
      noter('reset', { time_s: +C.t.toFixed(2) });
    };
    /* Une pause garde l'instant visé : la reprise s'arrête au même moment (la voix coupée puis reprise ne fait plus
     * courir la scène au-delà de ce que dit le tuteur). Une pause reçue sur une scène déjà figée ne fait rien, et la
     * reprise qui suit non plus. */
    C.pause = () => {
      if (!C.running) { C.fige = true; return; }
      C.suspendu = C.jusqua != null ? { jusqua: C.jusqua, motif: C.motif, v: C.v } : null;
      C.running = false; C.jusqua = null; texteBouton('Reprendre'); dire('Arrêt sur image.'); noter('pause', { time_s: +C.t.toFixed(2) });
    };
    C.resume = () => {
      if (C.running) return;
      if (C.fige) { C.fige = false; return; }
      if (C.fait || C.t >= fin()) return C.start();
      if (C.suspendu) { C.jusqua = C.suspendu.jusqua; C.motif = C.suspendu.motif; C.v = C.suspendu.v; C.suspendu = null; }
      C.running = true; texteBouton('Pause'); dire('Observe…'); noter('resume', {});
    };
    /* set_time {time_s | moment} : arrêt sur cet instant. */
    C.setTime = (p) => {
      const t = instantDe(p && (p.moment != null ? p.moment : p.time_s)); if (!Number.isFinite(t)) return;
      C.running = false; C.jusqua = null; C.suspendu = null; C.fige = false; C.v = 1;
      if (t < C.t) { o.reinit && o.reinit(); }
      sauter(t); C.fait = C.t >= fin();
      texteBouton(C.fait ? 'Rejouer' : 'Reprendre'); dire(`Arrêt sur image : t = ${fr(C.t)} s.`); noter('set_time', { time_s: C.t });
    };
    /* Rejoue (depuis le départ si l'instant est passé) et se fige sur l'instant nommé.
     *   depuis : moment ou instant d'où partir (saut en avant, ce qui précède est déjà au tableau) ;
     *   duree_s : durée voulue de l'animation (la scène va plus vite ou plus lentement, entre ×0,25 et ×4),
     *             pour que ce qui est montré tienne dans la phrase qui le dit. */
    C.playUntil = (p) => {
      const M = o.moments(), nom = p && p.moment in M ? p.moment : null, cible = nom ? M[nom] : +(p && p.time_s);
      if (!Number.isFinite(cible)) return;
      if (C.fait || C.t >= cible - 1e-3) { o.reinit && o.reinit(); sauter(depart()); }
      const d = instantDe(p && p.depuis);
      if (Number.isFinite(d) && d > C.t && d < cible) sauter(d);
      C.jusqua = Math.min(fin(), Math.max(0.001, cible)); C.motif = nom ? ((o.motifs || {})[nom] || nom) : '';
      const duree = +(p && p.duree_s);
      C.v = Number.isFinite(duree) && duree > 0 ? Math.max(.25, Math.min(4, (C.jusqua - C.t) / duree / (o.vitesse || 1))) : 1;   // durée réelle, même si la page fait défiler son temps plus vite (exao : o.vitesse)
      C.suspendu = null; C.fige = false;
      C.running = true; C.fait = false; texteBouton('Pause'); dire('Observe…');
      noter('play_until', { moment: nom, time_s: C.jusqua });
    };
    /* reset : figé au départ dans une diapositive pilotée, sinon rejoue depuis zéro (comme avant). */
    C.reset = () => (C.pilote ? C.preparer() : C.start());
    // Diapositive pilotée : la page s'ouvre figée sur son point de départ (après la fin du script de la page).
    if (C.pilote) setTimeout(() => { if (!C.running && C.t === 0) C.preparer(); }, 0);
    C.clic = () => { C.fige = false; C.suspendu = null; return C.running ? C.pause() : (C.t > 0 && C.t < fin() && !C.fait ? C.resume() : C.start()); };
    C.statut = () => (C.running ? 'running' : C.fait ? 'finished' : C.t > 0 ? 'paused' : 'idle');
    /* Part (0..1) d'une phase [a, b] à l'instant courant. */
    C.part = (a, b, t = C.t) => Math.max(0, Math.min(1, (t - a) / Math.max(1e-6, b - a)));
    return C;
  }

  /*
   * Ce qui apparaît PENDANT l'expérience s'écrit à la craie à partir de l'instant où cela arrive (comme le professeur
   * qui écrit au moment où il le dit), pas d'un coup :
   *   const ecrit = SVTTableau.Apparitions(scene);
   *   ecrit.ecrire(c, 'label_pyruvate', () => { c.texte(…); c.fleche(…); });   // dans dessiner(), seulement quand t ≥ la phase
   *   ecrit.oublier();                                                          // au start / quand on revient en arrière
   */
  const APPARITIONS = [];
  function Apparitions(scene) {
    const APP = {};
    const maintenant = () => (performance.now() - scene.ouvert) / 1000;
    let instantJusqua = -Infinity;
    const A = {
      ecrire(c, cle, fn) {
        // après un saut dans le temps, ce qui est déjà arrivé est au tableau d'un coup (pas réécrit trait par trait)
        if (!(cle in APP)) APP[cle] = maintenant() < instantJusqua ? -1e9 : maintenant();
        const cur = c.cur; c.depuis(APP[cle]); try { fn(); } finally { c.cur = cur; }
      },
      oublier() { for (const k of Object.keys(APP)) delete APP[k]; scene.sale = true; },
      /* Saut dans le temps (?depart=, play_until {depuis}, set_time) : tout ce qui est déjà écrit et ce qui apparaît dans
       * l'image qui suit est montré entier ; ce qui arrive ensuite s'écrit de nouveau à la craie, à son instant. */
      rattraper() { scene.ouvert -= 1e7; instantJusqua = maintenant() + 0.25; scene.sale = true; },
      APP,
    };
    APPARITIONS.push(A);
    return A;
  }

  /*
   * Allumer ce que l'on montre, ce que l'on compte (19 novembre 2026 ; simulations-au-tableau règles 16 et 17, professeur
   * règles 44 et 45). Le lecteur envoie pendant une démonstration jouée sur la figure :
   *   { command: 'eteins', parameters: {} } à l'ouverture, puis { command: 'allume', parameters: { cible, ligne, texte } }
   *   à l'instant où la ligne s'écrit (cible : un id de repère ou de moment, ou une liste).
   * La page les exécute elle-même (elle met 'allume' et 'eteins' dans ses commandes) :
   *   const lum = SVTTableau.Allumage(scene, chrono, { avant: () => { R.conclusions = true; }, comptes: { atp: ['atp_1', …] } });
   *   executer: { …, allume: () => lum.allume(p), eteins: lum.eteins }   ;  dans dessiner(c), juste avant c.fin() : lum.lueurs(c)
   *   etat: () => ({ …, allumes: lum.liste() })
   * allume : chaque cible qui est un moment pas encore passé est jouée jusqu'à lui (play_until, jamais en arrière) ; chaque
   * cible qui est un repère reçoit une lueur jaune douce qui RESTE, la dernière plus vive. Une cible d'un compte
   * (comptes.<nom> = liste ordonnée de repères) reçoit en plus son numéro courant « 1, 2, 3… », écrit proprement à la
   * craie à côté d'elle, dans l'ordre où elle a été allumée. eteins (et reset) éteint tout.
   */
  function Allumage(scene, chrono, o = {}) {
    const craie = scene.craie, RECTS = {}, allumes = [], comptes = o.comptes || {};
    let dernier = null;
    const repere = craie.repere;
    craie.repere = function (id, x, y, w, h, label) { RECTS[id] = [x, y, w, h]; return repere.call(this, id, x, y, w, h, label); };
    const groupeDe = (id) => Object.keys(comptes).find(g => comptes[g].includes(id));
    const L = {
      allume(p) {
        const cibles = [].concat((p && (p.cible ?? p.target ?? p.repere)) ?? []).map(String).filter(Boolean);
        if (!cibles.length) return;
        o.avant && o.avant(cibles, p);
        for (const id of cibles) { const i = allumes.indexOf(id); if (i >= 0) allumes.splice(i, 1); allumes.push(id); }
        dernier = cibles[cibles.length - 1];
        const M = chrono && o.moments !== false ? (o.moments ? o.moments() : null) : null;
        if (M) {
          // le moment le plus lointain parmi les cibles, s'il n'est pas déjà passé
          const futurs = cibles.filter(id => id in M && +M[id] > chrono.t + 1e-3).sort((a, b) => M[a] - M[b]);
          if (futurs.length) chrono.playUntil({ moment: futurs[futurs.length - 1] });
        }
        scene.sale = true;
      },
      eteins() { allumes.length = 0; dernier = null; scene.sale = true; },
      liste: () => allumes.slice(),
      dernier: () => dernier,
      estAllume: (id) => allumes.includes(id),
      /** Le rang (1, 2, 3…) d'une cible dans son compte, dans l'ordre d'allumage (0 si éteinte). */
      rang(id) { const g = groupeDe(id); if (!g) return 0; return allumes.filter(a => comptes[g].includes(a)).indexOf(id) + 1; },
      /** Combien d'éléments d'un compte sont allumés. */
      combien: (g) => allumes.filter(a => (comptes[g] || []).includes(a)).length,
      /** Les lueurs, dessinées par-dessus la scène (appeler juste avant c.fin()), puis les repères de l'image sont oubliés. */
      /*  auto : ce que la page allume elle-même au fil de son temps (un compte joué par la scène, voir compte()) :
       *  [{ id, n?, fort?, teinte? }] — n, le numéro courant écrit à côté ; fort, l'élément que l'on vient de compter ;
       *  teinte, la couleur de la pastille (un compte par couleur quand plusieurs comptes se suivent). */
      lueurs(c, auto = []) {
        if (!scene.mesurant) {
          const liste = auto.map(a => ({ id: a.id, fort: !!a.fort, n: a.n || 0, teinte: a.teinte }))
            .concat(allumes.filter(id => !auto.some(a => a.id === id)).map(id => ({ id, fort: id === dernier, n: L.rang(id) })));
          for (const { id, fort, n, teinte } of liste) {
            const r = RECTS[id]; if (!r) continue;
            L.lueur(c, r, fort);
            if (n) L.numero(c, r, n, teinte);
          }
        }
        for (const k of Object.keys(RECTS)) delete RECTS[k];
      },
      /** Une lueur jaune douce sur un rectangle [x, y, w, h] du dessin (fort : la dernière, plus vive). */
      lueur(c, [x, y, w, h], fort) {
        const g = c.ctx, rr = Math.min(12, w / 3, h / 3);
        g.save();
        g.beginPath(); g.roundRect ? g.roundRect(x - 3, y - 3, w + 6, h + 6, rr) : g.rect(x - 3, y - 3, w + 6, h + 6);
        g.fillStyle = fort ? 'rgba(255,226,110,.17)' : 'rgba(255,226,110,.09)'; g.fill();
        g.shadowColor = 'rgba(255,220,100,.95)'; g.shadowBlur = fort ? 18 : 9;
        g.strokeStyle = fort ? 'rgba(255,232,130,.98)' : 'rgba(255,232,130,.6)'; g.lineWidth = fort ? 3 : 2; g.stroke();
        g.restore();
      },
      /** Le numéro courant d'un élément compté, écrit proprement : à côté (à droite) ou, option numero: 'pastille' (éléments
       *  serrés), dans une pastille jaune posée sur le coin haut droit de l'élément. Jamais sous 15 px à l'écran. */
      numero(c, [x, y, w, h], n, teinte = '#ffe27a') {
        const g = c.ctx, s = String(n), ech = Math.max(.1, scene.s || 1);
        g.save(); g.textBaseline = 'alphabetic';
        if (o.numero === 'pastille') {
          const t = Math.max(13, 15.5 / ech), r = t * (s.length > 1 ? .85 : .7);
          const cx = Math.min(x + w - 2, (scene.L || 760) - r - 1), cy = Math.max(r + 1, y + 1);
          g.beginPath(); g.arc(cx, cy, r, 0, Math.PI * 2); g.fillStyle = teinte; g.shadowColor = 'rgba(255,220,100,.9)'; g.shadowBlur = 8; g.fill();
          g.shadowBlur = 0; g.font = `700 ${t}px ${window.Tableau.POLICE}`; g.fillStyle = '#2b1d00'; g.textAlign = 'center';
          g.fillText(s, cx, cy + t * .36);
        } else if (o.numero === 'dessous') {   // sous l'élément, centré (une rangée d'éléments serrés : billes de carbone)
          const t = Math.max(18, 17 / ech);
          g.font = `700 ${t}px ${window.Tableau.POLICE}`; g.fillStyle = c.couleur('jaune'); g.textAlign = 'center';
          g.shadowColor = 'rgba(255,220,100,.8)'; g.shadowBlur = 6;
          g.fillText(s, x + w / 2, y + h + t * .95);
        } else {
          const t = Math.max(18, Math.min(26, h * .6), 17 / ech);
          g.font = `700 ${t}px ${window.Tableau.POLICE}`; g.fillStyle = c.couleur('jaune'); g.globalAlpha = .96;
          g.shadowColor = 'rgba(255,220,100,.8)'; g.shadowBlur = 6;
          const xn = Math.min(x + w + 4, (scene.L || 760) - g.measureText(s).width - 2);
          g.fillText(s, xn, Math.max(t, y + t * .85));
        }
        g.restore();
      },
      /** Un compte joué par la scène : ids comptés un à un à partir de `debut`, un tous les `pas` (s de la scène) ; renvoie
       *  les entrées pour lueurs(c, auto) (numéro courant ; le dernier compté plus vif tant que le compte se fait). */
      compte(t, ids, debut, pas) {
        const k = ids.filter((_, i) => t >= debut + i * pas - 1e-6).length;
        return ids.slice(0, k).map((id, i) => ({ id, n: i + 1, fort: i === k - 1 && t < debut + ids.length * pas + .6 }));
      },
    };
    return L;
  }

  /* Interpolation douce. */
  const doux = (u) => (u <= 0 ? 0 : u >= 1 ? 1 : u * u * (3 - 2 * u));
  const mix = (a, b, u) => a + (b - a) * u;

  window.SVTTableau = { Scene, Chrono, Apparitions, Allumage, VW, VH, fr, doux, mix };
})();
