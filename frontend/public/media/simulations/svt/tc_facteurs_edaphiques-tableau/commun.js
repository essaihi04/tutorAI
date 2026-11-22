/*
 * Commun aux simulations du cours « Les facteurs édaphiques et leurs relations avec les êtres vivants » (Tronc commun
 * sciences, SVT, novembre 2026). Repris du kit du cours du muscle (svt/role_muscle_strie_squelettique-tableau :
 * commun.js pour la scène, recit.js pour la ligne de temps) :
 *   - Scene(canvas, dessiner, { large }) : cadre virtuel 760 × 420 (jusqu’à 760 × 2,1 en large), mis à l’échelle sans
 *     rien couper, texte jamais sous 15 px à l’écran (le kit baisse ce plancher sur un téléphone) ;
 *   - Chrono : ligne de temps pilotable (start, pause, resume, reset, set_time, play_until {moment}), bouton unique
 *     Lancer → Pause → Reprendre → Rejouer, ?depart=<moment> ouvre la page figée ;
 *   - Apparitions : ce qui arrive s’écrit à la craie à partir de l’instant où cela arrive.
 * Et le LEXIQUE DU COURS (un objet, un seul dessin, dans toutes les pages du cours) — peint avant la craie :
 *   sable = grains beiges ronds (les plus gros) ; limon = petits grains brique ; argile = poudre gris-brun très fine ;
 *   matière organique / humus = débris brun très foncé ; eau = bleu (teinte Lexique.T.eau) ; air = bulles blanches ;
 *   complexe argilo-humique (CAH) = disque orange marqué de charges « − » ; cations = billes marquées (Ca²⁺ = la bille
 *   nacrée du lexique commun, H⁺ = le proton rose du lexique commun ; K⁺, Na⁺, Mg²⁺ : ajoutés ici, à reporter dans le
 *   lexique commun, voir le compte rendu du cours) ; plante peinte (feuilles vertes, flétrie = feuilles tombantes jaunies).
 */
(function () {
  'use strict';
  const VW = 760, VH = 420, TAILLE_MIN = 15, L_MAX = 2.1, BANDEAU = 24;
  const TAU = Math.PI * 2;

  /* ───────────── Scène (copie du kit du muscle, sans l’option « ajuster ») ───────────── */
  function Scene(canvas, dessiner, options = {}) {
    const scene = { sale: true, L: VW };
    const craie = new window.Tableau.Craie(canvas, { onresize: () => { scene.sale = true; } });
    Object.assign(scene, {
      craie, ouvert: performance.now(), s: 1, ox: 0, oy: 0, VH,
      cadre(graine = 7) {
        const W = craie.W, H = craie.H;
        const L = options.large ? Math.round(Math.min(VW * L_MAX, Math.max(VW, VH * W / Math.max(1, H)))) : VW;
        scene.L = L;
        /* Petit cadre (téléphone en paysage : le lecteur donne ~429 × 250 px, 22 novembre 2026) : mode COMPACT. La page
         * ne garde que l'essentiel de l'étape (scene.foyer(L) = la boîte du dessin à montrer, en unités du cadre), le reste
         * du texte est dit par la voix ; une seule ligne en bas (scene.bandeau) dit l'étape ; le texte reste ≥ 15 px. */
        scene.compact = W < 520 || H < 320;
        if (scene._clip) { craie.ctx.restore(); scene._clip = false; }   // la découpe de l'image précédente
        craie.debut(graine, (performance.now() - scene.ouvert) / 1000);
        const Hd = scene.compact && scene.bandeau ? H - BANDEAU : H;
        const k = scene.compact && scene.foyer ? (typeof scene.foyer === 'function' ? scene.foyer(L) : scene.foyer) : null;
        let s;
        if (k) { s = Math.min(W / k.w, Hd / k.h); scene.ox = (W - k.w * s) / 2 - k.x * s; scene.oy = (Hd - k.h * s) / 2 - k.y * s; }
        else { s = Math.min(W / L, Hd / VH); scene.ox = (W - L * s) / 2; scene.oy = (Hd - VH * s) / 2; }
        scene.s = s;
        craie.ctx.translate(scene.ox, scene.oy); craie.ctx.scale(s, s);
        // compact : rien hors du foyer (le reste de la scène, coupé au bord, serait du texte tronqué)
        if (k) { craie.ctx.save(); craie.ctx.beginPath(); craie.ctx.rect(k.x, k.y, k.w, k.h); craie.ctx.clip(); scene._clip = true; }
        const fPlancher = Math.min(1, Math.max(.45, Math.min((W || 900) / 900, (H || 400) / 400)));
        craie.echelle = s;
        if (scene.compact) { craie._tailleMinBrut = TAILLE_MIN / fPlancher; craie._tailleMinLu = null; }   // 15 px à l'écran, sans la baisse du kit
        else craie.tailleMin = fPlancher >= .75 ? TAILLE_MIN / fPlancher : TAILLE_MIN;
        craie.cadre = { w: L, h: VH, haut: 0 };
        return craie;
      },
      local(x, y) { return [(x - scene.ox) / scene.s, (y - scene.oy) / scene.s]; },
      reecrire() { scene.ouvert = performance.now(); scene.sale = true; },
      image() {
        const t = scene.ouvert; scene.ouvert = -1e9;
        try { dessiner(craie, scene); return canvas.toDataURL('image/png'); } finally { scene.ouvert = t; scene.sale = true; }
      },
    });
    /* La ligne du bas en mode compact : l'étape en cours, 15 px au moins, coupée par « … » si elle est trop longue. */
    function bandeau() {
      let txt = scene.bandeau(); if (!txt) return;
      if (scene._clip) { craie.ctx.restore(); scene._clip = false; }
      const g = craie.ctx, d = devicePixelRatio || 1, W = craie.W, H = craie.H;
      g.save(); g.setTransform(d, 0, 0, d, 0, 0);
      g.fillStyle = 'rgba(0,0,0,.3)'; g.fillRect(0, H - BANDEAU, W, BANDEAU);
      g.font = `16px ${window.Tableau.POLICE}`;
      if (g.measureText(txt).width > W - 10) { g.font = `15px ${window.Tableau.POLICE}`; while (txt.length > 4 && g.measureText(txt + '…').width > W - 10) txt = txt.slice(0, -1); if (txt !== scene.bandeau()) txt += '…'; }
      g.fillStyle = '#facc15'; g.textAlign = 'center'; g.textBaseline = 'alphabetic'; g.fillText(txt, W / 2, H - 7);
      g.restore();
    }
    let avant = performance.now();
    requestAnimationFrame(function image(maintenant) {
      const dt = Math.min(0.1, Math.max(0, (maintenant - avant) / 1000)); avant = maintenant;
      const anime = scene.avancer ? scene.avancer(dt) : false;
      if ((scene.sale || anime) && craie.W > 1) { scene.sale = !dessiner(craie, scene); if (scene.compact && scene.bandeau) bandeau(); }
      requestAnimationFrame(image);
    });
    return scene;
  }

  /* ───────────── Ligne de temps pilotable (copie de recit.js du muscle) ───────────── */
  const fr = (v, d = 1) => (Number.isFinite(v) ? v.toFixed(d).replace('.', ',') : '—');
  const APPARITIONS = [];
  function Chrono(o) {
    const C = { t: 0, running: false, jusqua: null, motif: '', fait: false, emis: 0, v: 1, suspendu: null, fige: false };
    const pont = () => (o.pont ? o.pont() : null);
    const noter = (a, d) => { const p = pont(); if (p) { p.noter(a, d); p.emettre(); } };
    const texteBouton = (s) => { if (o.bouton) o.bouton.textContent = s; };
    const dire = (s, kind) => { if (o.bulle && s) window.Tableau.bulle(o.bulle, s, kind); };
    const fin = () => o.fin();
    const PARAM = new URLSearchParams(location.search).get('depart');
    C.pilote = PARAM != null;
    const instantDe = (v) => { if (v == null || v === '') return NaN; const M = o.moments(); return v in M ? +M[v] : +v; };
    const depart = () => Math.max(0, Math.min(fin(), +instantDe(PARAM) || 0));
    const sauter = (t) => { C.t = Math.min(fin(), Math.max(0, t)); if (C.t > 0) { APPARITIONS.forEach(a => a.rattraper()); o.saut && o.saut(); } };
    C.avancer = (dt) => {
      if (!C.running) return false;
      C.t = Math.min(fin(), C.t + dt * (C.v || 1));
      if (C.jusqua != null && C.t >= C.jusqua) {
        C.t = C.jusqua; C.running = false; C.jusqua = null; C.v = 1; texteBouton('Reprendre');
        dire('Arrêt sur image : ' + (C.motif || `t = ${fr(C.t)} s`) + '.');
        noter('pause', { time_s: +C.t.toFixed(2) });
        return true;
      }
      if (C.t >= fin()) { C.running = false; C.fait = true; C.v = 1; texteBouton('Rejouer'); dire(o.fini ? o.fini() : 'Terminé.', 'good'); noter('fin', {}); }
      else if (performance.now() - C.emis > 500) { C.emis = performance.now(); const p = pont(); p && p.emettre(); }
      return true;
    };
    C.start = () => {
      C.jusqua = null; C.suspendu = null; C.fige = false; C.v = 1; C.running = true; C.fait = false; texteBouton('Pause'); dire(depart() > 0 ? 'Observe…' : (o.depart || 'Observe…'));
      o.reinit && o.reinit(); const d = depart(); if (d > 0) sauter(d); else C.t = 0; noter('start', {});
    };
    C.preparer = () => {
      C.running = false; C.jusqua = null; C.suspendu = null; C.fige = false; C.v = 1; C.fait = false;
      o.reinit && o.reinit(); sauter(depart()); texteBouton(C.t > 0 ? 'Reprendre' : 'Lancer');
      const M = o.moments(), nom = Object.keys(M).find(k => Math.abs(M[k] - C.t) < 1e-6);
      if (C.t > 0) dire('Arrêt sur image : ' + ((nom && (o.motifs || {})[nom]) || `t = ${fr(C.t)} s`) + '.');
      noter('reset', { time_s: +C.t.toFixed(2) });
    };
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
    C.setTime = (p) => {
      const t = instantDe(p && (p.moment != null ? p.moment : p.time_s)); if (!Number.isFinite(t)) return;
      C.running = false; C.jusqua = null; C.suspendu = null; C.fige = false; C.v = 1;
      if (t < C.t) { o.reinit && o.reinit(); }
      sauter(t); C.fait = C.t >= fin();
      texteBouton(C.fait ? 'Rejouer' : 'Reprendre'); dire(`Arrêt sur image : t = ${fr(C.t)} s.`); noter('set_time', { time_s: C.t });
    };
    C.playUntil = (p) => {
      const M = o.moments(), nom = p && p.moment in M ? p.moment : null, cible = nom ? M[nom] : +(p && p.time_s);
      if (!Number.isFinite(cible)) return;
      if (C.fait || C.t >= cible - 1e-3) { o.reinit && o.reinit(); sauter(depart()); }
      const d = instantDe(p && p.depuis);
      if (Number.isFinite(d) && d > C.t && d < cible) sauter(d);
      C.jusqua = Math.min(fin(), Math.max(0.001, cible)); C.motif = nom ? ((o.motifs || {})[nom] || nom) : '';
      const duree = +(p && p.duree_s);
      C.v = Number.isFinite(duree) && duree > 0 ? Math.max(.25, Math.min(4, (C.jusqua - C.t) / duree)) : 1;
      C.suspendu = null; C.fige = false;
      C.running = true; C.fait = false; texteBouton('Pause'); dire('Observe…');
      noter('play_until', { moment: nom, time_s: C.jusqua });
    };
    C.reset = () => (C.pilote ? C.preparer() : C.start());
    if (C.pilote) setTimeout(() => { if (!C.running && C.t === 0) C.preparer(); }, 0);
    C.clic = () => { C.fige = false; C.suspendu = null; return C.running ? C.pause() : (C.t > 0 && C.t < fin() && !C.fait ? C.resume() : C.start()); };
    C.statut = () => (C.running ? 'running' : C.fait ? 'finished' : C.t > 0 ? 'paused' : 'idle');
    C.part = (a, b, t = C.t) => Math.max(0, Math.min(1, (t - a) / Math.max(1e-6, b - a)));
    return C;
  }
  function Apparitions(scene) {
    const APP = {};
    const maintenant = () => (performance.now() - scene.ouvert) / 1000;
    let instantJusqua = -Infinity;
    const A = {
      ecrire(c, cle, fn) {
        if (!(cle in APP)) APP[cle] = maintenant() < instantJusqua ? -1e9 : maintenant();
        const cur = c.cur; c.depuis(APP[cle]); try { fn(); } finally { c.cur = cur; }
      },
      oublier() { for (const k of Object.keys(APP)) delete APP[k]; scene.sale = true; },
      rattraper() { scene.ouvert -= 1e7; instantJusqua = maintenant() + 0.25; scene.sale = true; },
      APP,
    };
    APPARITIONS.push(A);
    return A;
  }
  const doux = (u) => (u <= 0 ? 0 : u >= 1 ? 1 : u * u * (3 - 2 * u));
  const mix = (a, b, u) => a + (b - a) * u;

  /* Le protocole commun d’une page à ligne de temps : bouton, bulle, commandes, état. */
  function brancher({ id, titre, M, FIN, motifs, texte, voir, params, setParams, explication, depart, fini, vue, bandeau }) {
    const $ = (k) => document.getElementById(k);
    const R = params || {};
    let pont = null;
    const scene = brancher.scene;
    const chrono = Chrono({ fin: () => FIN, moments: () => M, motifs, bouton: $('run'), bulle: $('feedback'), pont: () => pont,
      depart, reinit: () => brancher.ecrit && brancher.ecrit.oublier(), fini });
    scene.avancer = (dt) => { const a = chrono.avancer(dt); if (a) scene.sale = true; return a; };
    // la ligne du bas en mode compact : le motif du dernier moment atteint (la page peut la réécrire : `bandeau(t, motif)`)
    scene.bandeau = () => {
      const t = chrono.t, noms = Object.keys(M).sort((a, b) => M[a] - M[b]).filter(k => M[k] <= t + 1e-3);
      let m = noms.length ? (motifs || {})[noms[noms.length - 1]] || '' : (depart || '');
      if (bandeau) m = bandeau(t, m);
      return m ? m.charAt(0).toUpperCase() + m.slice(1) : '';
    };
    $('run').onclick = chrono.clic;
    if (explication) window.Tableau.explication(explication);
    const commandes = ['start', 'pause', 'resume', 'reset', 'set_time', 'play_until', 'set_parameters'];
    const schema = { play_until: { moment: Object.keys(M).join(' | ') } };
    if (setParams) schema.set_parameters = setParams.schema;
    const config = { id, version: '1.0', title: titre, variants: [{ id: vue || 'principale', label: vue || 'principale' }], commands: commandes, command_schema: schema };
    pont = window.Tableau.protocole({ id, commandes, config, texte,
      etat: () => ({ simulation_status: chrono.statut(), ce_qui_se_voit: voir(chrono.t), moments: M, time_s: +chrono.t.toFixed(2), current_variant: vue || 'principale', parameters: { ...R } }),
      progression: () => (chrono.statut() === 'finished' ? 1 : chrono.t / FIN),
      executer: (cmd, p) => ({ start: chrono.start, pause: chrono.pause, resume: chrono.resume, reset: chrono.reset,
        set_time: () => chrono.setTime(p), play_until: () => chrono.playUntil(p),
        set_parameters: () => { if (setParams) setParams.appliquer(p || {}, R); scene.sale = true; } })[cmd]?.() });
    return { chrono, pont, R };
  }

  /* ───────────── Le lexique du cours : objets peints ───────────── */
  const rgba = (c, a) => `rgba(${c[0]},${c[1]},${c[2]},${a})`;
  function graine(seed) { let s = (seed >>> 0) || 1; return () => { s = (Math.imul(s, 1664525) + 1013904223) >>> 0; return s / 4294967296; }; }
  const SOL = {
    sable: { c: [226, 190, 128], bord: [150, 112, 60], r: 7 },
    limon: { c: [184, 98, 62], bord: [110, 52, 30], r: 3.6 },
    argile: { c: [128, 112, 100], bord: [80, 68, 60], r: 1.6 },
    humus: { c: [72, 50, 32], bord: [40, 26, 16], r: 4 },
    eau: [60, 160, 210],
    cah: [242, 150, 50],
  };
  /** Un grain de sol peint (forme irrégulière, ombre, reflet) : type 'sable' | 'limon' | 'argile' | 'humus'. */
  function grain(ctx, x, y, type = 'sable', o = {}) {
    const T = SOL[type] || SOL.sable, r = (o.r ?? T.r) * (o.echelle ?? 1), rr = graine(o.graine ?? Math.round(x * 13 + y * 7));
    const n = type === 'humus' ? 5 : 7, pts = [];
    for (let i = 0; i < n; i++) { const a = i / n * TAU + rr() * .5, d = r * (.75 + rr() * .4) * (type === 'humus' ? (i % 2 ? .55 : 1.2) : 1); pts.push([x + Math.cos(a) * d, y + Math.sin(a) * d]); }
    ctx.save(); ctx.globalAlpha = o.alpha ?? 1;
    const g = ctx.createRadialGradient(x - r * .35, y - r * .4, r * .1, x, y, r * 1.2);
    g.addColorStop(0, rgba(T.c.map(v => Math.min(255, v + 45)), 1)); g.addColorStop(1, rgba(T.c.map(v => v * .8), 1));
    ctx.fillStyle = g; ctx.beginPath(); pts.forEach(([px, py], i) => (i ? ctx.lineTo(px, py) : ctx.moveTo(px, py))); ctx.closePath(); ctx.fill();
    if (r > 3) { ctx.strokeStyle = rgba(T.bord, .9); ctx.lineWidth = Math.max(.6, r * .12); ctx.stroke(); }
    ctx.restore();
  }
  /** Une zone remplie de grains d’un type (couche de sédiment, échantillon) : rectangle (x, y, w, h), densité 0..1. */
  function remplir(ctx, x, y, w, h, type, o = {}) {
    const T = SOL[type], rr = graine(o.graine ?? 17), r = T.r * (o.echelle ?? 1);
    ctx.save(); ctx.beginPath(); ctx.rect(x, y, w, h); ctx.clip();
    const fond = ctx.createLinearGradient(0, y, 0, y + h);
    fond.addColorStop(0, rgba(T.c.map(v => v * .85), o.alpha ?? 1)); fond.addColorStop(1, rgba(T.c.map(v => v * .62), o.alpha ?? 1));
    ctx.fillStyle = fond; ctx.fillRect(x, y, w, h);
    if (type !== 'argile') {
      const n = Math.round(w * h / (r * r * 3.2) * (o.densite ?? .8));
      for (let i = 0; i < Math.min(n, 900); i++) grain(ctx, x + rr() * w, y + rr() * h, type, { r, graine: i * 31 + 7, alpha: o.alpha });
    } else {
      for (let i = 0; i < Math.min(1200, w * h / 9); i++) { ctx.fillStyle = rgba(rr() > .5 ? T.bord : T.c.map(v => Math.min(255, v + 30)), .45 * (o.alpha ?? 1)); ctx.fillRect(x + rr() * w, y + rr() * h, 1.6, 1.6); }
    }
    ctx.restore();
  }
  /** Eau peinte dans un rectangle (plus claire en haut), avec un reflet de surface. */
  function eauPeinte(ctx, x, y, w, h, o = {}) {
    const c = o.teinte || SOL.eau, a = o.alpha ?? .55;
    const g = ctx.createLinearGradient(0, y, 0, y + h);
    g.addColorStop(0, rgba(c.map(v => Math.min(255, v + 50)), a * .75)); g.addColorStop(1, rgba(c, a));
    ctx.save(); ctx.fillStyle = g; ctx.fillRect(x, y, w, h);
    if (o.surface !== false) { ctx.strokeStyle = 'rgba(225,245,255,.75)'; ctx.lineWidth = 1.6; ctx.beginPath(); ctx.moveTo(x + 2, y + 1); ctx.lineTo(x + w - 2, y + 1); ctx.stroke(); }
    ctx.restore();
  }
  /** Le complexe argilo-humique : disque orange (comme le manuel), granuleux, marqué de charges « − » sur son bord. */
  function cah(ctx, x, y, r, o = {}) {
    ctx.save(); ctx.globalAlpha = o.alpha ?? 1;
    ctx.fillStyle = 'rgba(0,0,0,.25)'; ctx.beginPath(); ctx.ellipse(x + r * .1, y + r * 1.02, r * .85, r * .2, 0, 0, TAU); ctx.fill();
    const g = ctx.createRadialGradient(x - r * .35, y - r * .35, r * .1, x, y, r);
    g.addColorStop(0, 'rgba(255,214,150,1)'); g.addColorStop(.55, rgba(SOL.cah, 1)); g.addColorStop(1, 'rgba(170,90,20,1)');
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.fill();
    const rr = graine(7); ctx.fillStyle = 'rgba(90,50,20,.35)';
    for (let i = 0; i < 40; i++) { const a = rr() * TAU, d = rr() * r * .85; ctx.beginPath(); ctx.arc(x + Math.cos(a) * d, y + Math.sin(a) * d, 1.4, 0, TAU); ctx.fill(); }
    if (o.charges !== false) {
      const n = o.n ?? 10;
      ctx.font = `700 ${o.taille ?? Math.max(15, r * .32)}px Arial, sans-serif`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      for (let i = 0; i < n; i++) { const a = i / n * TAU + .2; ctx.fillStyle = '#1e3a8a'; ctx.fillText('−', x + Math.cos(a) * r * .78, y + Math.sin(a) * r * .78); }
    }
    ctx.restore();
  }
  /** Couleurs des ions du cours. */
  const IONS = {
    'K+': { c: [190, 110, 235], t: 'K⁺', encre: '#1a0838' },
    'Na+': { c: [140, 170, 215], t: 'Na⁺', encre: '#0b1f2a' },
    'Mg2+': { c: [130, 210, 110], t: 'Mg²⁺', encre: '#0b2a0b' },
    'Ca2+': { c: [207, 219, 232], t: 'Ca²⁺', encre: '#0b1f2a' },
    'H+': { c: [244, 114, 182], t: 'H⁺', encre: '#3b0a24' },
    'bleu': { c: [40, 90, 220], t: '+', encre: '#ffffff' },
    'eosine': { c: [235, 70, 80], t: '−', encre: '#ffffff' },
  };
  /** Un ion : bille peinte marquée (cation « + », anion « − »). Ca²⁺ et H⁺ reprennent le lexique commun quand il est chargé. */
  function ion(ctx, x, y, nom, o = {}) {
    const I = IONS[nom] || IONS['K+'], r = (o.r ?? 11) * (o.echelle ?? 1), a = o.alpha ?? 1;
    if (a <= .02) return;
    const L = window.Lexique;
    if (L && nom === 'H+' && L.proton) { L.proton(ctx, x, y, { r, alpha: a }); return; }
    if (L && L.bille) L.bille(ctx, x, y, r, I.c, { alpha: a });
    else { ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = rgba(I.c, 1); ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.fill(); ctx.restore(); }
    if (o.texte !== false) {
      ctx.save(); ctx.globalAlpha = a; ctx.fillStyle = I.encre; ctx.font = `700 ${Math.max(9, r * (I.t.length > 2 ? .8 : 1.1))}px Arial, sans-serif`;
      ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(I.t, x, y + 1); ctx.restore();
    }
  }
  /** Une plante peinte posée sur le sol en (x, ySol), hauteur h ; o.fletrie 0..1 : les feuilles tombent et jaunissent. */
  function plante(ctx, x, ySol, h, o = {}) {
    const f = Math.max(0, Math.min(1, o.fletrie || 0)), a = o.alpha ?? 1;
    ctx.save(); ctx.globalAlpha = a; ctx.lineCap = 'round';
    const tige = [x, ySol, x + f * h * .12, ySol - h * (1 - f * .25)];
    // racines
    ctx.strokeStyle = 'rgba(214,190,150,.9)'; ctx.lineWidth = 1.6;
    for (let i = -2; i <= 2; i++) { ctx.beginPath(); ctx.moveTo(x, ySol); ctx.quadraticCurveTo(x + i * 6, ySol + 14, x + i * 11, ySol + 24 + Math.abs(i) * -3); ctx.stroke(); }
    ctx.strokeStyle = 'rgb(70,140,60)'; ctx.lineWidth = Math.max(2.5, h * .04);
    ctx.beginPath(); ctx.moveTo(tige[0], tige[1]); ctx.quadraticCurveTo(x + f * h * .2, ySol - h * .55, tige[2], tige[3]); ctx.stroke();
    const vert = [Math.round(80 + 140 * f), Math.round(170 - 10 * f), Math.round(70 - 30 * f)];
    for (let k = 0; k < 4; k++) {
      const yy = ySol - h * (.3 + k * .18) * (1 - f * .25), cote = k % 2 ? 1 : -1, lg = h * (.32 - k * .04);
      // saine : la feuille monte en biais ; flétrie : elle pend vers le bas
      const ang = cote > 0 ? -.55 + f * 1.75 : Math.PI + .55 - f * 1.75;
      const xb = x + f * h * .12 * (k + 1) / 4;
      ctx.save(); ctx.translate(xb, yy); ctx.rotate(ang);
      const g = ctx.createLinearGradient(0, 0, lg, 0); g.addColorStop(0, rgba(vert.map(v => v * .7), 1)); g.addColorStop(1, rgba(vert, 1));
      ctx.fillStyle = g; ctx.beginPath(); ctx.moveTo(0, 0); ctx.quadraticCurveTo(lg * .5, -lg * .32, lg, 0); ctx.quadraticCurveTo(lg * .5, lg * .32, 0, 0); ctx.fill();
      ctx.strokeStyle = 'rgba(255,255,255,.25)'; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(2, 0); ctx.lineTo(lg * .9, 0); ctx.stroke();
      ctx.restore();
    }
    ctx.restore();
  }
  /** Un ver de terre peint le long d’un chemin de points (anneaux visibles). */
  function ver(ctx, pts, o = {}) {
    ctx.save(); ctx.globalAlpha = o.alpha ?? 1; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    ctx.strokeStyle = 'rgba(60,20,20,.6)'; ctx.lineWidth = (o.e ?? 7) + 2; ctx.beginPath(); pts.forEach(([x, y], i) => (i ? ctx.lineTo(x, y) : ctx.moveTo(x, y))); ctx.stroke();
    ctx.strokeStyle = 'rgb(196,110,110)'; ctx.lineWidth = o.e ?? 7; ctx.stroke();
    ctx.strokeStyle = 'rgba(255,220,220,.45)'; ctx.lineWidth = (o.e ?? 7) * .3; ctx.stroke();
    ctx.strokeStyle = 'rgba(110,40,40,.5)'; ctx.lineWidth = 1;
    for (let i = 1; i < pts.length - 1; i++) { const [x0, y0] = pts[i - 1], [x1, y1] = pts[i + 1], a = Math.atan2(y1 - y0, x1 - x0) + Math.PI / 2, e = (o.e ?? 7) / 2; ctx.beginPath(); ctx.moveTo(pts[i][0] + Math.cos(a) * e, pts[i][1] + Math.sin(a) * e); ctx.lineTo(pts[i][0] - Math.cos(a) * e, pts[i][1] - Math.sin(a) * e); ctx.stroke(); }
    ctx.restore();
  }
  /** Une goutte d’eau. */
  function goutte(ctx, x, y, r = 4, a = 1) {
    ctx.save(); ctx.globalAlpha = a; const g = ctx.createRadialGradient(x - r * .3, y - r * .2, .5, x, y, r * 1.3);
    g.addColorStop(0, 'rgba(220,245,255,1)'); g.addColorStop(1, rgba(SOL.eau, 1)); ctx.fillStyle = g;
    ctx.beginPath(); ctx.moveTo(x, y - r * 1.8); ctx.quadraticCurveTo(x + r, y - r * .2, x, y + r); ctx.quadraticCurveTo(x - r, y - r * .2, x, y - r * 1.8); ctx.fill(); ctx.restore();
  }
  /** Une bulle d’air dans l’eau. */
  function bulle(ctx, x, y, r) {
    ctx.save(); ctx.strokeStyle = 'rgba(235,248,255,.8)'; ctx.lineWidth = 1.3; ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.stroke();
    ctx.fillStyle = 'rgba(255,255,255,.55)'; ctx.beginPath(); ctx.arc(x - r * .35, y - r * .35, r * .3, 0, TAU); ctx.fill(); ctx.restore();
  }
  /** Lueur jaune douce derrière un objet compté (règle 16), son numéro écrit à côté par la page. */
  function lueur(c, x, y, w, h, vive) {
    c.direct(() => {
      const g = c.ctx; g.save(); g.shadowColor = 'rgba(250,204,21,.85)'; g.shadowBlur = vive ? 20 : 10;
      g.strokeStyle = `rgba(250,204,21,${vive ? .95 : .55})`; g.lineWidth = vive ? 2.6 : 1.6;
      g.beginPath(); if (g.roundRect) g.roundRect(x, y, w, h, 8); else g.rect(x, y, w, h); g.stroke(); g.restore();
    });
  }

  window.SolTableau = { Scene, VW, VH, Chrono, Apparitions, brancher, fr, doux, mix, rgba, graine,
    SOL, IONS, grain, remplir, eauPeinte, cah, ion, plante, ver, goutte, bulle, lueur };
})();
