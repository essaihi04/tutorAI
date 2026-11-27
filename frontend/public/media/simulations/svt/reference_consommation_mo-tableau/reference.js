/*
 * Commun aux pages du cours de référence SVT « Consommation de la matière organique et flux d'énergie »
 * (27 novembre 2026, docs/reference-svt/ARCHITECTURE.md). Chargé APRÈS tableau.js, commun.js, lexique.js, peinture.js
 * (du dossier voisin ../reactions_responsables_liberation_energie-tableau/) et demarche.js.
 *
 * Deux sessions écrivent ici : on AJOUTE des fonctions, on ne modifie jamais celles qui existent.
 *
 * ── 1. Ref.page(o) : une page racontée, pilotée par la voix ────────────────────────────────────────────────────────────
 *   const page = Ref.page({
 *     id: 'svt_reference_exao_levures_exp1', vue: 'exp1', titre: 'ExAO — expérience 1',
 *     moments: [['axes', 6, 'les deux axes sont lus'], ['avant', 11, 'avant le glucose : deux paliers'], …],   // dans l'ordre
 *     dessiner(c, e) { … },             // e = l'environnement (voir plus bas)
 *     foyer(e) { return { x, y, w, h }; },   // téléphone en paysage : la boîte du dessin à montrer pour l'étape en cours
 *     voit(e) { return '…'; },          // ce qui se voit, en mots (ce_qui_se_voit)
 *     vivant(e) { return true; },       // la scène bouge même à l'arrêt (barreau qui tourne, bulles)
 *     texte: '…', explications: [{ repere, texte }], accroche: '…', fini: '…',
 *     params: { schema: { … }, lire: () => ({ … }), regler: (p) => true },   // set_parameters (facultatif)
 *     comptes: { mitos: ['mito_1', …] }, numero: 'pastille',                 // comptes allumés (Allumage)
 *     lueurs(e) { return […]; },        // ce que la page allume elle-même (lum.compte)
 *   });
 *   Un moment = l'instant (en s de la scène) où l'animation de son étape est TERMINÉE ; son animation occupe l'intervalle
 *   [moment précédent, lui]. Figée sur un moment, la page ne montre rien de l'étape suivante (arrêt pour l'observation).
 *   L'environnement e : t, L (largeur du cadre : 760 à ~1600), compact (téléphone), M (moments), ordre (noms),
 *     vu(id) (le moment est atteint), des(id) (son animation a commencé), p(id, a = 0, b = 1) (avancement 0..1 de son
 *     animation, entre les fractions a et b), d(id, a, b) (le même, adouci), etape() (nom de l'étape en cours),
 *     ecrire(c, cle, fn) (écrit à la craie à partir de maintenant), horloge (s réelles, pour ce qui bouge sans cesse).
 *   Renvoie { scene, chrono, pont, M, lum, env }.
 *   Commandes : start, reset, pause, resume, set_time {time_s | moment}, play_until {moment | time_s, duree_s}, allume, eteins,
 *   set_parameters {demarche: 1..6, …}. ?depart=<moment> ouvre la page figée sur ce moment (kit + Chrono).
 *
 * ── 2. Ref.pchip(points) : courbe lisse et monotone passant exactement par les points d'un document ──────────────────
 * ── 3. Peinture réaliste du matériel d'ExAO : cuve, barreau, agitateur, sonde, seringue, cable, boitier (interface),
 *       ordinateur, loupe, bulles — et Ref.fiche (texte seul, pour le téléphone). ─────────────────────────────────────
 */
(function () {
  'use strict';
  const TAU = Math.PI * 2;
  const $ = (id) => document.getElementById(id);
  const rgba = (c, a) => `rgba(${Math.round(c[0])},${Math.round(c[1])},${Math.round(c[2])},${a})`;
  const clair = (c, k) => c.map(v => Math.min(255, v + k));
  const sombre = (c, k) => c.map(v => v * k);
  const doux = (u) => (u <= 0 ? 0 : u >= 1 ? 1 : u * u * (3 - 2 * u));
  const mix = (a, b, u) => a + (b - a) * u;
  const borne = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
  function graine(seed) { let s = (seed >>> 0) || 1; return () => { s = (Math.imul(s, 1664525) + 1013904223) >>> 0; return s / 4294967296; }; }
  function rr(ctx, x, y, w, h, r) { ctx.beginPath(); if (ctx.roundRect) ctx.roundRect(x, y, w, h, r); else ctx.rect(x, y, w, h); }

  /* ════════════════════════════ 1. La page racontée ════════════════════════════ */
  function page(o) {
    const { bulle, protocole } = window.Tableau, { Scene, Chrono, Apparitions, Allumage } = window.SVTTableau;
    const Dem = window.Demarche || { dessiner() {}, reserve: () => ({ w: 0, h: 0 }), texte: () => '', regler() {}, etape: 0 };
    const canvas = $('canvas'), bouton = $('run'), bulleEl = $('feedback');
    const ordre = o.moments.map(m => m[0]);
    const M = Object.fromEntries(o.moments.map(m => [m[0], m[1]]));
    const MOTIFS = Object.fromEntries(o.moments.map(m => [m[0], m[2] || m[0]]));
    const FIN = o.fin ?? (o.moments[o.moments.length - 1][1] + .3);
    const debutDe = (id) => { const i = ordre.indexOf(id); return i <= 0 ? 0 : M[ordre[i - 1]]; };
    let pont = null, chrono = null, foyerCur = null, foyerT = 0, bandeauH = 0, bandeauTexte = '', bandeauDepuis = 0;
    /* Téléphone : la phrase de l'étape (e.bandeau = { texte, couleur, repere, label }) est écrite en bas du canvas, en pixels
     * de l'écran (15 px, deux ou trois lignes au plus) ; la figure zoomée (foyer) garde le reste de la hauteur. */
    function dessinerBandeau(c) {
      const b = env.compact ? env.bandeau : null;
      if (!b || !b.texte) { if (bandeauH) { bandeauH = 0; return true; } return false; }
      const ctx = c.ctx, d = window.devicePixelRatio || 1, W = c.W, H = c.H, t = 15, pas = 18;
      const plat = String(b.texte).replace(/_\{([^}]*)\}/g, (m, k) => k.replace(/[0-9]/g, ch => '₀₁₂₃₄₅₆₇₈₉'[+ch]));
      ctx.save(); ctx.setTransform(d, 0, 0, d, 0, 0); ctx.font = `700 ${t}px ${window.Tableau.POLICE}`;
      const rangs = []; let cur = '';
      for (const m of plat.split(' ')) { const essai = cur ? cur + ' ' + m : m; if (cur && ctx.measureText(essai).width > W - 16) { rangs.push(cur); cur = m; } else cur = essai; }
      if (cur) rangs.push(cur);
      const h = rangs.length * pas + 6, change = h !== bandeauH;
      if (plat !== bandeauTexte) { bandeauTexte = plat; bandeauDepuis = env.horloge; }
      const a = Math.min(1, (env.horloge - bandeauDepuis) / .4);
      ctx.fillStyle = 'rgba(6,26,20,.86)'; rr(ctx, 2, H - h - 1, W - 4, h, 6); ctx.fill();
      ctx.globalAlpha = a; ctx.fillStyle = window.Tableau.COULEURS[b.couleur] || b.couleur || '#e2e8f0'; ctx.textAlign = 'center'; ctx.textBaseline = 'alphabetic';
      rangs.forEach((s, i) => ctx.fillText(s, W / 2, H - h + 14 + i * pas));
      if (b.repere) c.repere(b.repere, 2, H - h - 1, W - 4, h, b.label || plat);
      ctx.restore();
      bandeauH = h;
      return change || a < 1;
    }
    const env = {
      t: 0, L: 760, compact: false, M, ordre, FIN, horloge: 0,
      vu: (id) => env.t >= M[id] - 1e-6,
      des: (id) => env.t > debutDe(id) + 1e-4,
      p: (id, a = 0, b = 1) => { const t0 = debutDe(id), d = M[id] - t0; return borne((env.t - (t0 + a * d)) / Math.max(1e-6, (b - a) * d)); },
      d: (id, a = 0, b = 1) => doux(env.p(id, a, b)),
      etape: () => ordre.find(id => env.t <= M[id] + 1e-6) || ordre[ordre.length - 1],
      debutDe, tmin: 0, tf: (b) => Math.max(b, env.tmin), bandeau: null,
      ecrire: (c, cle, fn) => ecrit.ecrire(c, cle, fn),
    };
    const scene = Scene(canvas, (c) => {
      scene.cadre(o.graine || 31);
      env.t = chrono.t; env.L = scene.L; env.horloge = performance.now() / 1000;
      env.compact = !scene.mesurant && (c.W < 560 || c.H < 300);
      let glisse = false;
      if (env.compact && o.foyer) {
        const cible = o.foyer(env);
        if (cible) {
          const dt = Math.min(.1, Math.max(0, env.horloge - foyerT)); foyerT = env.horloge;
          if (!foyerCur) foyerCur = { ...cible };
          else {
            const k = 1 - Math.exp(-dt * 6);
            for (const a of ['x', 'y', 'w', 'h']) { foyerCur[a] += (cible[a] - foyerCur[a]) * k; if (Math.abs(cible[a] - foyerCur[a]) > .6) glisse = true; else foyerCur[a] = cible[a]; }
          }
          const d = window.devicePixelRatio || 1, W = c.W, H = c.H, haut = Dem.reserve(c).h, f = foyerCur;
          const s = Math.min(W / f.w, (H - haut - bandeauH) / f.h);
          scene.s = s; scene.ox = (W - f.w * s) / 2 - f.x * s; scene.oy = haut + (H - haut - bandeauH - f.h * s) / 2 - f.y * s;
          c.ctx.setTransform(d, 0, 0, d, 0, 0); c.ctx.translate(scene.ox, scene.oy); c.ctx.scale(s, s);
          c.echelle = s;
          // 15 px à l'écran, sans la baisse que le kit applique aux petits tableaux
          c._tailleMinBrut = 15 / Math.min(1, Math.max(.45, Math.min((W || 900) / 900, (H || 400) / 400))); c._tailleMinLu = null;
          c.cadre = null;
        }
      } else foyerCur = null;
      env.tmin = c.tailleMin && c.echelle ? c.tailleMin / c.echelle : 0; env.bandeau = null;
      o.dessiner(c, env);
      lum.lueurs(c, o.lueurs ? (o.lueurs(env) || []) : []);
      if (dessinerBandeau(c)) glisse = true;
      Dem.dessiner(c);
      const complet = c.fin();
      return complet && !glisse && !(o.vivant && o.vivant(env));
    }, { large: o.large !== false });
    const ecrit = Apparitions(scene);
    chrono = Chrono({ fin: () => FIN, moments: () => M, motifs: MOTIFS, bouton, bulle: bulleEl, pont: () => pont, vitesse: o.vitesse || 1,
      depart: o.accroche || 'Observe…', reinit: () => { ecrit.oublier(); o.reinit && o.reinit(); }, fini: () => o.fini || 'Terminé.' });
    scene.avancer = chrono.avancer;
    const lum = Allumage(scene, chrono, { moments: () => M, comptes: o.comptes, numero: o.numero });
    if (o.explications) window.Tableau.explication({ [o.vue || 'vue']: o.explications });
    bouton.onclick = chrono.clic;

    const params = () => Object.assign({ demarche: Dem.etape || 0 }, o.params && o.params.lire ? o.params.lire() : {});
    function setParameters(p) {
      let change = false;
      if (p && 'demarche' in p) { Dem.regler(p.demarche); change = true; }
      if (o.params && o.params.regler && o.params.regler(p || {}, { chrono, scene, ecrit }) !== false) change = true;
      if (change) { scene.sale = true; pont.noter('set_parameters', params()); pont.emettre(); }
    }
    const commandes = ['start', 'reset', 'pause', 'resume', 'set_time', 'play_until', 'set_parameters', 'allume', 'eteins'];
    const config = { id: o.id, version: '1.0', title: o.titre || o.id, variants: [{ id: o.vue || 'vue', label: o.vue || 'vue' }], commands: commandes,
      command_schema: {
        set_time: { time_s: `0..${FIN} (s de la scène ; arrêt sur cet instant)`, moment: ordre.join(' | ') },
        play_until: { moment: ordre.join(' | ') + ' (joue jusqu’à ce moment et se fige)', time_s: 'ou un instant en s de la scène', duree_s: 'durée voulue de l’animation (facultatif)' },
        set_parameters: Object.assign({ demarche: '1..6 (étape de la démarche allumée en haut à droite ; 0 : rien)' }, (o.params && o.params.schema) || {}),
        allume: { cible: 'repère ou moment (ou liste)' }, eteins: {} } };
    const voit = () => {
      let s = '';
      try { s = o.voit ? o.voit(env) : ''; } catch (e) { s = ''; }
      const etat = chrono.running ? ' (l’animation joue)' : chrono.fait ? ' (fin)' : ' (figée)';
      const dem = Dem.texte ? Dem.texte() : '';
      return `${s}${etat}${dem ? ' ' + dem : ''}${lum.liste().length ? ' Allumé : ' + lum.liste().join(', ') + '.' : ''}`;
    };
    pont = protocole({ id: o.id, commandes, config, texte: o.texte || o.titre || '',
      etat: () => { env.t = chrono.t; return Object.assign({ simulation_status: chrono.statut(), ce_qui_se_voit: voit(), allumes: lum.liste(), current_variant: o.vue || 'vue',
        time_s: +chrono.t.toFixed(3), moments: M, etape: env.etape(), parameters: params() }, o.etat ? o.etat(env) : {}); },
      progression: () => chrono.t / FIN,
      executer: (cmd, p) => ({
        start: chrono.start, reset: () => { lum.eteins(); chrono.reset(); }, pause: chrono.pause, resume: chrono.resume,
        set_time: () => { chrono.setTime(p); scene.sale = true; const nom = ordre.find(k => Math.abs(M[k] - chrono.t) < 1e-6); if (nom) bulle(bulleEl, 'Arrêt sur image : ' + MOTIFS[nom] + '.'); },
        play_until: () => chrono.playUntil(p), set_parameters: () => setParameters(p || {}),
        allume: () => { lum.allume(p); pont.noter('allume', { cible: p && p.cible }); pont.emettre(); }, eteins: () => { lum.eteins(); pont.emettre(); },
      })[cmd]?.() });
    if (o.accueil) bulle(bulleEl, o.accueil);
    setTimeout(() => { if (!chrono.pilote && !chrono.running && chrono.t === 0) chrono.start(); }, 1600);
    window.__sim = { chrono, scene, M, env, lum, ordre };
    return { scene, chrono, pont, M, lum, env, ecrit };
  }

  /* ════════════════════════════ 2. Courbes des documents ════════════════════════════ */
  /** Interpolation cubique monotone (Fritsch–Carlson) : f(x) passe par chaque point [x, y], sans dépassement. */
  function pchip(pts) {
    const n = pts.length, x = pts.map(p => p[0]), y = pts.map(p => p[1]), h = [], dl = [], m = new Array(n).fill(0);
    for (let i = 0; i < n - 1; i++) { h.push(x[i + 1] - x[i]); dl.push((y[i + 1] - y[i]) / h[i]); }
    m[0] = dl[0]; m[n - 1] = dl[n - 2];
    for (let i = 1; i < n - 1; i++) m[i] = dl[i - 1] * dl[i] <= 0 ? 0 : 3 * (h[i - 1] + h[i]) / ((2 * h[i] + h[i - 1]) / dl[i - 1] + (h[i] + 2 * h[i - 1]) / dl[i]);
    if (dl[0] === 0) m[0] = 0; if (dl[n - 2] === 0) m[n - 1] = 0;
    return (v) => {
      if (v <= x[0]) return y[0]; if (v >= x[n - 1]) return y[n - 1];
      let i = 0; while (i < n - 2 && v > x[i + 1]) i++;
      const t = (v - x[i]) / h[i], t2 = t * t, t3 = t2 * t;
      return (2 * t3 - 3 * t2 + 1) * y[i] + (t3 - 2 * t2 + t) * h[i] * m[i] + (-2 * t3 + 3 * t2) * y[i + 1] + (t3 - t2) * h[i] * m[i + 1];
    };
  }

  /* ════════════════════════════ 3. Le matériel d'ExAO, peint ════════════════════════════ */
  /**
   * La cuve du bioréacteur (verre épais, vue de côté) : (x, y) coin haut gauche du verre, w, h.
   *   o.niveau (0..1), o.teinte [r,g,b], o.alpha, o.trouble (0..1, levures en suspension), o.phase (s, pour le lent brassage),
   *   o.vortex (0..1, creux de la surface quand le barreau tourne), o.couvercle (plaque à orifices), o.bouchon (cuve fermée),
   *   o.derriere(ctx) : ce qui trempe (sondes, aiguille) — peint AVANT le liquide, donc vu à travers lui ;
   *   dedans(ctx, g) : ce qui est dans le liquide (bulles, barreau, particules) — peint APRÈS le liquide.
   * Renvoie g = { x0, x1 (parois intérieures), surface (y du liquide), fond (y du fond intérieur) }.
   */
  function cuve(ctx, x, y, w, h, o = {}, dedans) {
    const niveau = o.niveau ?? .78, c = o.teinte || [205, 186, 140], a = o.alpha ?? .5, e = 7, rb = 16;
    const ys = y + h * (1 - niveau), g = { x0: x + 6, x1: x + w - 6, surface: ys, fond: y + h - 7 };
    const corps = () => { ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x, y + h - rb); ctx.quadraticCurveTo(x, y + h, x + rb, y + h); ctx.lineTo(x + w - rb, y + h); ctx.quadraticCurveTo(x + w, y + h, x + w, y + h - rb); ctx.lineTo(x + w, y); };
    const liquide = () => { ctx.beginPath(); ctx.moveTo(x + 4, ys); ctx.lineTo(x + 4, y + h - rb); ctx.quadraticCurveTo(x + 4, y + h - 4, x + rb, y + h - 4); ctx.lineTo(x + w - rb, y + h - 4); ctx.quadraticCurveTo(x + w - 4, y + h - 4, x + w - 4, y + h - rb); ctx.lineTo(x + w - 4, ys); ctx.closePath(); };
    ctx.save();
    // ombre posée
    ctx.fillStyle = 'rgba(0,0,0,.28)'; ctx.beginPath(); ctx.ellipse(x + w / 2, y + h + 2, w * .52, 5, 0, 0, TAU); ctx.fill();
    // le verre du fond (très léger) et le bord arrière
    corps(); ctx.closePath(); ctx.fillStyle = 'rgba(210,235,245,.055)'; ctx.fill();
    ctx.strokeStyle = 'rgba(225,240,250,.28)'; ctx.lineWidth = 1.2; ctx.beginPath(); ctx.ellipse(x + w / 2, y, w / 2, e, 0, Math.PI, TAU); ctx.stroke();
    if (o.derriere) o.derriere(ctx, g);
    // le liquide
    const gl = ctx.createLinearGradient(0, ys, 0, y + h);
    gl.addColorStop(0, rgba(clair(c, 34), a)); gl.addColorStop(.55, rgba(c, a + .08)); gl.addColorStop(1, rgba(sombre(c, .72), a + .16));
    liquide(); ctx.fillStyle = gl; ctx.fill();
    // le trouble : des levures en suspension, lentement brassées
    if (o.trouble) {
      ctx.save(); liquide(); ctx.clip();
      const r = graine(o.graine || 41), ph = o.phase || 0, n = Math.round(w * (y + h - ys) / 210);
      for (let k = 0; k < n; k++) {
        const u = r(), v = r(), s = r(), px = x + 6 + ((u + ph * (.012 + .02 * s)) % 1) * (w - 12), py = ys + 6 + v * (y + h - ys - 14) + Math.sin(ph * (.6 + s) + k) * 2.2;
        ctx.fillStyle = rgba(clair(c, 48), (.16 + .3 * s) * o.trouble); ctx.beginPath(); ctx.ellipse(px, py, 1.3 + s * 1.2, 1 + s, 0, 0, TAU); ctx.fill();
      }
      ctx.restore();
    }
    if (dedans) { ctx.save(); liquide(); ctx.clip(); dedans(ctx, g); ctx.restore(); }
    // la surface : une ellipse plus claire, son ménisque, le creux du brassage
    ctx.fillStyle = rgba(clair(c, 60), a * .55); ctx.beginPath(); ctx.ellipse(x + w / 2, ys, w / 2 - 4, e - 1, 0, 0, TAU); ctx.fill();
    ctx.strokeStyle = 'rgba(245,250,255,.6)'; ctx.lineWidth = 1.4; ctx.beginPath(); ctx.ellipse(x + w / 2, ys, w / 2 - 4, e - 1, 0, 0, Math.PI); ctx.stroke();
    ctx.strokeStyle = 'rgba(245,250,255,.5)'; ctx.lineWidth = 1.1;
    ctx.beginPath(); ctx.moveTo(x + 4, ys - 3); ctx.quadraticCurveTo(x + 6, ys + 1, x + 12, ys + 2); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(x + w - 4, ys - 3); ctx.quadraticCurveTo(x + w - 6, ys + 1, x + w - 12, ys + 2); ctx.stroke();
    if (o.vortex) {
      const v = o.vortex; ctx.fillStyle = rgba(sombre(c, .55), .3 * v); ctx.beginPath(); ctx.ellipse(x + w / 2, ys + 1, w * .13 * v, 2.6, 0, 0, TAU); ctx.fill();
      ctx.strokeStyle = `rgba(245,250,255,${.3 * v})`; ctx.lineWidth = 1; ctx.beginPath(); ctx.ellipse(x + w / 2, ys + 1, w * .26, 4, 0, .3, 2.6); ctx.stroke();
    }
    // les parois : deux traits (épaisseur du verre), le fond, le bord avant
    const paroi = ctx.createLinearGradient(x, 0, x + w, 0);
    paroi.addColorStop(0, 'rgba(235,246,252,.85)'); paroi.addColorStop(.5, 'rgba(235,246,252,.5)'); paroi.addColorStop(1, 'rgba(235,246,252,.8)');
    ctx.strokeStyle = paroi; ctx.lineWidth = 2.4; corps(); ctx.stroke();
    ctx.strokeStyle = 'rgba(235,246,252,.3)'; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(x + 4, y + 3); ctx.lineTo(x + 4, y + h - rb); ctx.quadraticCurveTo(x + 4, y + h - 4, x + rb, y + h - 4); ctx.lineTo(x + w - rb, y + h - 4); ctx.quadraticCurveTo(x + w - 4, y + h - 4, x + w - 4, y + h - rb); ctx.lineTo(x + w - 4, y + 3); ctx.stroke();
    ctx.strokeStyle = 'rgba(240,248,252,.75)'; ctx.lineWidth = 2; ctx.beginPath(); ctx.ellipse(x + w / 2, y, w / 2, e, 0, 0, Math.PI); ctx.stroke();
    // les reflets : une bande douce à gauche, un filet à droite, une « fenêtre » en haut
    const rg = ctx.createLinearGradient(x + 7, 0, x + 25, 0); rg.addColorStop(0, 'rgba(255,255,255,0)'); rg.addColorStop(.45, 'rgba(255,255,255,.24)'); rg.addColorStop(1, 'rgba(255,255,255,0)');
    ctx.fillStyle = rg; rr(ctx, x + 7, y + 12, 18, h - 34, 9); ctx.fill();
    ctx.fillStyle = 'rgba(255,255,255,.1)'; rr(ctx, x + w - 15, y + 18, 5, h - 50, 3); ctx.fill();
    ctx.fillStyle = 'rgba(255,255,255,.2)'; ctx.beginPath(); ctx.moveTo(x + 30, y + 16); ctx.lineTo(x + 44, y + 14); ctx.lineTo(x + 42, y + 34); ctx.lineTo(x + 30, y + 37); ctx.closePath(); ctx.fill();
    // les graduations gravées
    if (o.graduations !== false) {
      ctx.strokeStyle = 'rgba(240,248,252,.42)'; ctx.lineWidth = 1;
      for (let k = 1; k <= 7; k++) { const gy = y + h - 10 - k * (h - 30) / 8, l = k % 2 ? 7 : 12; ctx.beginPath(); ctx.moveTo(x + w - 22, gy); ctx.lineTo(x + w - 22 + l, gy); ctx.stroke(); }
    }
    // le couvercle (plaque percée) ou le bouchon (cuve fermée, étanche)
    if (o.bouchon) {
      const gb = ctx.createLinearGradient(0, y - 20, 0, y + 10); gb.addColorStop(0, 'rgba(214,118,84,1)'); gb.addColorStop(.5, 'rgba(176,84,58,1)'); gb.addColorStop(1, 'rgba(112,48,34,1)');
      ctx.fillStyle = gb; ctx.beginPath(); ctx.moveTo(x - 5, y - 20); ctx.lineTo(x + w + 5, y - 20); ctx.lineTo(x + w - 3, y + 9); ctx.lineTo(x + 3, y + 9); ctx.closePath(); ctx.fill();
      ctx.strokeStyle = 'rgba(70,28,20,.9)'; ctx.lineWidth = 1.2; ctx.stroke();
      ctx.fillStyle = 'rgba(255,220,200,.35)'; rr(ctx, x + 4, y - 18, w - 8, 4, 2); ctx.fill();
      ctx.strokeStyle = 'rgba(70,28,20,.45)'; ctx.lineWidth = 1; for (const k of [-6, 2]) { ctx.beginPath(); ctx.moveTo(x - 2, y + k); ctx.lineTo(x + w + 2, y + k); ctx.stroke(); }
    } else if (o.couvercle) {
      const gc = ctx.createLinearGradient(0, y - 12, 0, y + 2); gc.addColorStop(0, 'rgba(130,138,152,1)'); gc.addColorStop(1, 'rgba(58,62,74,1)');
      ctx.fillStyle = gc; rr(ctx, x - 5, y - 11, w + 10, 12, 3); ctx.fill(); ctx.strokeStyle = 'rgba(22,24,30,.9)'; ctx.lineWidth = 1; ctx.stroke();
      ctx.fillStyle = 'rgba(255,255,255,.25)'; rr(ctx, x - 2, y - 10, w + 4, 2.5, 1); ctx.fill();
    }
    ctx.restore();
    return g;
  }

  /** Le barreau aimanté (blanc) posé au fond de la cuve : il tourne autour de la verticale (angle en rad), vu de côté. */
  function barreau(ctx, cx, cy, len, ang, o = {}) {
    const k = Math.abs(Math.cos(ang)), rx = len / 2 * k + 4.5 * (1 - k), a = o.alpha ?? 1;
    ctx.save(); ctx.globalAlpha = a;
    if (o.tourne !== false) { ctx.fillStyle = 'rgba(255,255,255,.13)'; ctx.beginPath(); ctx.ellipse(cx, cy, len / 2, 4.2, 0, 0, TAU); ctx.fill(); }
    ctx.fillStyle = 'rgba(0,0,0,.3)'; ctx.beginPath(); ctx.ellipse(cx, cy + 4.5, rx, 1.8, 0, 0, TAU); ctx.fill();
    const g = ctx.createLinearGradient(0, cy - 4.5, 0, cy + 4.5); g.addColorStop(0, '#ffffff'); g.addColorStop(.5, '#e6e9ee'); g.addColorStop(1, '#9aa1ad');
    ctx.fillStyle = g; rr(ctx, cx - rx, cy - 4.5, rx * 2, 9, 4.5); ctx.fill();
    ctx.fillStyle = 'rgba(120,128,140,.8)'; ctx.fillRect(cx - 1.4, cy - 4.5, 2.8, 9);
    ctx.restore();
  }

  /** L'agitateur magnétique (le socle sur lequel la cuve est posée) : plateau, bouton de vitesse, voyant. */
  function agitateur(ctx, x, y, w, h, o = {}) {
    ctx.save();
    ctx.fillStyle = 'rgba(0,0,0,.3)'; ctx.beginPath(); ctx.ellipse(x + w / 2, y + h + 2, w * .52, 4, 0, 0, TAU); ctx.fill();
    const gp = ctx.createLinearGradient(0, y, 0, y + 8); gp.addColorStop(0, 'rgba(236,240,246,1)'); gp.addColorStop(1, 'rgba(150,158,172,1)');
    ctx.fillStyle = gp; rr(ctx, x, y, w, 8, 3); ctx.fill();
    const gc = ctx.createLinearGradient(0, y + 7, 0, y + h); gc.addColorStop(0, 'rgba(86,98,122,1)'); gc.addColorStop(.5, 'rgba(58,68,90,1)'); gc.addColorStop(1, 'rgba(32,38,54,1)');
    ctx.fillStyle = gc; rr(ctx, x + 3, y + 7, w - 6, h - 7, 5); ctx.fill(); ctx.strokeStyle = 'rgba(14,18,28,.9)'; ctx.lineWidth = 1; ctx.stroke();
    ctx.fillStyle = 'rgba(255,255,255,.1)'; rr(ctx, x + 6, y + 9, w - 12, 3, 1.5); ctx.fill();
    // le bouton de vitesse et son repère
    const bx = x + w * .26, by = y + 7 + (h - 7) * .52, br = Math.min(9.5, (h - 9) * .42), an = o.vitesse ? -.9 + 2 * o.vitesse : -2.2;
    ctx.strokeStyle = 'rgba(220,226,236,.5)'; ctx.lineWidth = 1; ctx.beginPath(); ctx.arc(bx, by, br + 3, Math.PI * .8, Math.PI * 2.2); ctx.stroke();
    const gb = ctx.createRadialGradient(bx - 2, by - 2, 1, bx, by, br); gb.addColorStop(0, '#e8ecf2'); gb.addColorStop(1, '#6b7486');
    ctx.fillStyle = gb; ctx.beginPath(); ctx.arc(bx, by, br, 0, TAU); ctx.fill();
    ctx.strokeStyle = '#1b2030'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(bx, by); ctx.lineTo(bx + Math.cos(an) * br * .85, by + Math.sin(an) * br * .85); ctx.stroke();
    // le voyant
    const lx = x + w * .74;
    if (o.marche) { const gl = ctx.createRadialGradient(lx, by, 0, lx, by, 11); gl.addColorStop(0, 'rgba(74,222,128,.75)'); gl.addColorStop(1, 'rgba(74,222,128,0)'); ctx.fillStyle = gl; ctx.beginPath(); ctx.arc(lx, by, 11, 0, TAU); ctx.fill(); }
    ctx.fillStyle = o.marche ? '#86efac' : '#3a4a40'; ctx.beginPath(); ctx.arc(lx, by, 3.4, 0, TAU); ctx.fill();
    ctx.fillStyle = 'rgba(20,24,34,1)'; ctx.fillRect(x + 12, y + h, 16, 3); ctx.fillRect(x + w - 28, y + h, 16, 3);
    ctx.restore();
  }

  /** Une sonde : tête sombre baguée de la couleur de sa grandeur, tige métallique, pointe sensible. (x, yH) haut de la tête. */
  function sonde(ctx, x, yH, yB, o = {}) {
    const c = o.couleur || [34, 211, 238], a = o.alpha ?? 1;
    ctx.save(); ctx.globalAlpha = a;
    const gt = ctx.createLinearGradient(x - 5, 0, x + 5, 0); gt.addColorStop(0, 'rgba(88,94,108,1)'); gt.addColorStop(.38, 'rgba(226,230,238,1)'); gt.addColorStop(.6, 'rgba(168,174,188,1)'); gt.addColorStop(1, 'rgba(62,66,80,1)');
    ctx.fillStyle = gt; rr(ctx, x - 5, yH + 20, 10, yB - yH - 30, 2); ctx.fill();
    const gp = ctx.createLinearGradient(x - 5, 0, x + 5, 0); gp.addColorStop(0, 'rgba(40,44,54,1)'); gp.addColorStop(.45, 'rgba(110,116,130,1)'); gp.addColorStop(1, 'rgba(30,32,42,1)');
    ctx.fillStyle = gp; ctx.beginPath(); ctx.moveTo(x - 5, yB - 12); ctx.lineTo(x + 5, yB - 12); ctx.lineTo(x + 5, yB - 4); ctx.quadraticCurveTo(x + 5, yB, x, yB); ctx.quadraticCurveTo(x - 5, yB, x - 5, yB - 4); ctx.closePath(); ctx.fill();
    ctx.fillStyle = rgba(clair(c, 60), .95); ctx.beginPath(); ctx.ellipse(x, yB - 1.5, 3.2, 1.8, 0, 0, TAU); ctx.fill();
    const gh = ctx.createLinearGradient(x - 8, 0, x + 8, 0); gh.addColorStop(0, 'rgba(22,24,32,1)'); gh.addColorStop(.4, 'rgba(92,98,112,1)'); gh.addColorStop(1, 'rgba(18,20,28,1)');
    ctx.fillStyle = gh; rr(ctx, x - 8, yH, 16, 22, 3); ctx.fill();
    ctx.fillStyle = rgba(c, 1); ctx.fillRect(x - 8, yH + 13, 16, 5);
    ctx.fillStyle = 'rgba(255,255,255,.35)'; ctx.fillRect(x - 8, yH + 13, 16, 1.4);
    ctx.fillStyle = 'rgba(30,32,40,1)'; rr(ctx, x - 3.5, yH - 6, 7, 7, 2); ctx.fill();
    ctx.restore();
  }

  /** Une seringue verticale : corps gradué (yH..yB), aiguille jusqu'à yA ; `enfonce` 0..1 ; `teinte` du liquide. */
  function seringue(ctx, x, yH, yB, yA, enfonce, teinte = [250, 220, 120], o = {}) {
    const w = 15, Lc = yB - yH, yp = mix(yH + 5, yB - 9, borne(enfonce)), a = o.alpha ?? 1;
    ctx.save(); ctx.globalAlpha = a;
    ctx.strokeStyle = 'rgba(214,220,230,.95)'; ctx.lineWidth = 1.3; ctx.beginPath(); ctx.moveTo(x, yB + 8); ctx.lineTo(x, yA); ctx.stroke();           // l'aiguille
    ctx.fillStyle = rgba(teinte, .7); ctx.fillRect(x - w / 2 + 2, yp, w - 4, yB - yp - 1);                                                      // le liquide
    ctx.fillStyle = 'rgba(38,42,52,1)'; rr(ctx, x - w / 2 + 1.5, yp - 5, w - 3, 6, 1.5); ctx.fill();                                               // le joint du piston
    ctx.strokeStyle = 'rgba(226,230,238,.95)'; ctx.lineWidth = 3.4; ctx.beginPath(); ctx.moveTo(x, yp - 5); ctx.lineTo(x, yp - 5 - Lc * .6); ctx.stroke();
    ctx.fillStyle = 'rgba(226,230,238,1)'; rr(ctx, x - 10, yp - 9 - Lc * .6, 20, 4.5, 2); ctx.fill();
    const gv = ctx.createLinearGradient(x - w / 2, 0, x + w / 2, 0); gv.addColorStop(0, 'rgba(235,245,252,.38)'); gv.addColorStop(.3, 'rgba(255,255,255,.1)'); gv.addColorStop(1, 'rgba(235,245,252,.3)');
    ctx.fillStyle = gv; ctx.fillRect(x - w / 2, yH, w, Lc);
    ctx.strokeStyle = 'rgba(232,242,250,.85)'; ctx.lineWidth = 1.5; ctx.strokeRect(x - w / 2, yH, w, Lc);
    ctx.lineWidth = 2.2; ctx.beginPath(); ctx.moveTo(x - w / 2 - 5, yH); ctx.lineTo(x + w / 2 + 5, yH); ctx.stroke();
    ctx.strokeStyle = 'rgba(232,242,250,.5)'; ctx.lineWidth = 1;
    for (let k = 1; k < 6; k++) { const gy = yH + Lc * k / 6; ctx.beginPath(); ctx.moveTo(x - w / 2, gy); ctx.lineTo(x - w / 2 + (k % 2 ? 4 : 7), gy); ctx.stroke(); }
    ctx.fillStyle = 'rgba(214,220,230,.9)'; ctx.beginPath(); ctx.moveTo(x - 4.5, yB); ctx.lineTo(x + 4.5, yB); ctx.lineTo(x + 1.6, yB + 8); ctx.lineTo(x - 1.6, yB + 8); ctx.closePath(); ctx.fill();
    ctx.restore();
  }

  /** Un câble souple : courbe de Bézier [x0, y0, cx1, cy1, cx2, cy2, x1, y1] (ou plusieurs à la suite), gaine colorée. */
  function cable(ctx, pts, couleur = [60, 64, 78], o = {}) {
    const a = o.alpha ?? 1, e = o.epaisseur ?? 3.2;
    const chemin = () => { ctx.beginPath(); ctx.moveTo(pts[0], pts[1]); for (let i = 2; i + 5 < pts.length; i += 6) ctx.bezierCurveTo(pts[i], pts[i + 1], pts[i + 2], pts[i + 3], pts[i + 4], pts[i + 5]); };
    ctx.save(); ctx.globalAlpha = a; ctx.lineCap = 'round';
    if (o.part != null && o.part < 1) { ctx.setLineDash([o.part * (o.longueur || 600), 4000]); }
    ctx.strokeStyle = 'rgba(8,10,16,.75)'; ctx.lineWidth = e + 1.8; chemin(); ctx.stroke();
    ctx.strokeStyle = rgba(couleur, 1); ctx.lineWidth = e; chemin(); ctx.stroke();
    ctx.strokeStyle = 'rgba(255,255,255,.3)'; ctx.lineWidth = e * .3; ctx.translate(-.6, -.8); chemin(); ctx.stroke();
    ctx.restore();
  }

  /** Le boîtier d'interface (ExAO) : prises devant, voyants. Renvoie les points de branchement { entrees: [[x,y],…], sortie }. */
  function boitier(ctx, x, y, w, h, o = {}) {
    const a = o.alpha ?? 1;
    ctx.save(); ctx.globalAlpha = a;
    ctx.fillStyle = 'rgba(0,0,0,.3)'; ctx.beginPath(); ctx.ellipse(x + w / 2, y + h + 2, w * .52, 3.5, 0, 0, TAU); ctx.fill();
    const g = ctx.createLinearGradient(0, y, 0, y + h); g.addColorStop(0, 'rgba(92,118,168,1)'); g.addColorStop(.18, 'rgba(58,82,128,1)'); g.addColorStop(1, 'rgba(26,40,70,1)');
    ctx.fillStyle = g; rr(ctx, x, y, w, h, 5); ctx.fill(); ctx.strokeStyle = 'rgba(10,16,30,.95)'; ctx.lineWidth = 1; ctx.stroke();
    ctx.fillStyle = 'rgba(255,255,255,.16)'; rr(ctx, x + 3, y + 2, w - 6, 3, 1.5); ctx.fill();
    ctx.fillStyle = 'rgba(16,24,44,.9)'; rr(ctx, x + 5, y + h * .34, w - 10, h * .5, 3); ctx.fill();
    const py = y + h * .59, entrees = [[x + w * .2, py], [x + w * .42, py]], sortie = [x + w, y + h * .5];
    for (const [px, pyy] of entrees) { ctx.fillStyle = 'rgba(190,198,212,1)'; ctx.beginPath(); ctx.arc(px, pyy, 5, 0, TAU); ctx.fill(); ctx.fillStyle = 'rgba(12,14,20,1)'; ctx.beginPath(); ctx.arc(px, pyy, 3, 0, TAU); ctx.fill(); }
    const led = (lx, c, on) => { if (on) { const gl = ctx.createRadialGradient(lx, py, 0, lx, py, 9); gl.addColorStop(0, rgba(c, .8)); gl.addColorStop(1, rgba(c, 0)); ctx.fillStyle = gl; ctx.beginPath(); ctx.arc(lx, py, 9, 0, TAU); ctx.fill(); } ctx.fillStyle = on ? rgba(clair(c, 70), 1) : 'rgba(50,58,70,1)'; ctx.beginPath(); ctx.arc(lx, py, 2.8, 0, TAU); ctx.fill(); };
    led(x + w * .68, [74, 222, 128], o.marche !== false);
    led(x + w * .84, [250, 190, 60], !!o.mesure && Math.floor((o.phase || 0) * 5) % 2 === 0);
    ctx.restore();
    return { entrees, sortie };
  }

  /**
   * L'ordinateur : un écran plat sur son pied. (x, y, w, h) = le boîtier de l'écran ; o.allume 0..1 ; o.pied (hauteur du pied).
   * Renvoie la dalle { x, y, w, h } (là où la page trace ses courbes).
   */
  function ordinateur(ctx, x, y, w, h, o = {}) {
    const al = o.allume ?? 1, pied = o.pied ?? 30, cx = x + w / 2, a = o.alpha ?? 1;
    const d = { x: x + 9, y: y + 9, w: w - 18, h: h - 24 };
    ctx.save(); ctx.globalAlpha = a;
    // le pied
    ctx.fillStyle = 'rgba(0,0,0,.3)'; ctx.beginPath(); ctx.ellipse(cx, y + h + pied + 3, 84, 5, 0, 0, TAU); ctx.fill();
    const gp = ctx.createLinearGradient(cx - 22, 0, cx + 22, 0); gp.addColorStop(0, 'rgba(52,56,68,1)'); gp.addColorStop(.5, 'rgba(120,126,140,1)'); gp.addColorStop(1, 'rgba(44,48,58,1)');
    ctx.fillStyle = gp; ctx.beginPath(); ctx.moveTo(cx - 16, y + h - 2); ctx.lineTo(cx + 16, y + h - 2); ctx.lineTo(cx + 24, y + h + pied - 4); ctx.lineTo(cx - 24, y + h + pied - 4); ctx.closePath(); ctx.fill();
    const gs = ctx.createLinearGradient(0, y + h + pied - 6, 0, y + h + pied + 3); gs.addColorStop(0, 'rgba(150,156,170,1)'); gs.addColorStop(1, 'rgba(52,56,68,1)');
    ctx.fillStyle = gs; rr(ctx, cx - 74, y + h + pied - 6, 148, 9, 4.5); ctx.fill();
    // le boîtier
    ctx.save(); ctx.shadowColor = 'rgba(0,0,0,.5)'; ctx.shadowBlur = 14; ctx.shadowOffsetY = 5;
    const gb = ctx.createLinearGradient(0, y, 0, y + h); gb.addColorStop(0, 'rgba(74,78,92,1)'); gb.addColorStop(1, 'rgba(28,30,40,1)');
    ctx.fillStyle = gb; rr(ctx, x, y, w, h, 9); ctx.fill(); ctx.restore();
    ctx.strokeStyle = 'rgba(150,156,172,.55)'; ctx.lineWidth = 1; rr(ctx, x + .5, y + .5, w - 1, h - 1, 9); ctx.stroke();
    // la dalle
    const ge = ctx.createLinearGradient(0, d.y, 0, d.y + d.h);
    ge.addColorStop(0, rgba([mix(16, 12, al), mix(18, 30, al), mix(22, 56, al)], 1)); ge.addColorStop(1, rgba([mix(10, 5, al), mix(11, 14, al), mix(14, 30, al)], 1));
    ctx.fillStyle = ge; rr(ctx, d.x, d.y, d.w, d.h, 3); ctx.fill();
    if (al > 0) { const gl = ctx.createRadialGradient(d.x + d.w * .5, d.y + d.h * .45, 10, d.x + d.w * .5, d.y + d.h * .5, d.w * .7); gl.addColorStop(0, `rgba(70,130,200,${.13 * al})`); gl.addColorStop(1, 'rgba(70,130,200,0)'); ctx.fillStyle = gl; ctx.fillRect(d.x, d.y, d.w, d.h); }
    // le reflet de la vitre
    ctx.save(); rr(ctx, d.x, d.y, d.w, d.h, 3); ctx.clip();
    ctx.fillStyle = 'rgba(255,255,255,.035)'; ctx.beginPath(); ctx.moveTo(d.x, d.y); ctx.lineTo(d.x + d.w * .46, d.y); ctx.lineTo(d.x + d.w * .2, d.y + d.h); ctx.lineTo(d.x, d.y + d.h); ctx.closePath(); ctx.fill();
    ctx.restore();
    // le voyant
    ctx.fillStyle = al > .2 ? '#4ade80' : '#4a4f5c'; ctx.beginPath(); ctx.arc(x + w - 18, y + h - 7.5, 2.2, 0, TAU); ctx.fill();
    ctx.fillStyle = 'rgba(190,196,210,.5)'; rr(ctx, cx - 14, y + h - 9, 28, 3, 1.5); ctx.fill();
    ctx.restore();
    return d;
  }

  /** Une loupe : ce que `fn(ctx)` peint est vu dans le verre (découpé au disque). o.fond [r,g,b] du milieu, o.manche (angle). */
  function loupe(ctx, cx, cy, r, fn, o = {}) {
    const a = o.alpha ?? 1, am = o.manche ?? .9;
    ctx.save(); ctx.globalAlpha = a;
    if (o.manche !== false) {
      const x1 = cx + Math.cos(am) * (r + 2), y1 = cy + Math.sin(am) * (r + 2), x2 = cx + Math.cos(am) * (r + (o.longueur ?? r * .7)), y2 = cy + Math.sin(am) * (r + (o.longueur ?? r * .7));
      ctx.lineCap = 'round'; ctx.strokeStyle = 'rgba(20,14,10,.9)'; ctx.lineWidth = 10; ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();
      ctx.strokeStyle = 'rgba(122,78,44,1)'; ctx.lineWidth = 7.5; ctx.stroke();
      ctx.strokeStyle = 'rgba(214,160,110,.6)'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(x1 - 1.5, y1 - 1.5); ctx.lineTo(x2 - 1.5, y2 - 1.5); ctx.stroke();
    }
    ctx.save(); ctx.shadowColor = 'rgba(0,0,0,.5)'; ctx.shadowBlur = 12; ctx.shadowOffsetY = 4;
    const f = o.fond || [150, 136, 100], g = ctx.createRadialGradient(cx - r * .3, cy - r * .3, 3, cx, cy, r);
    g.addColorStop(0, rgba(clair(f, 26), o.opaque ?? .96)); g.addColorStop(1, rgba(sombre(f, .62), o.opaque ?? .96));
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(cx, cy, r, 0, TAU); ctx.fill(); ctx.restore();
    ctx.save(); ctx.beginPath(); ctx.arc(cx, cy, r - 1, 0, TAU); ctx.clip(); if (fn) fn(ctx); ctx.restore();
    // le verre : reflet en croissant, puis la monture
    ctx.strokeStyle = 'rgba(255,255,255,.22)'; ctx.lineWidth = 5; ctx.lineCap = 'round'; ctx.beginPath(); ctx.arc(cx, cy, r - 8, Math.PI * 1.08, Math.PI * 1.42); ctx.stroke();
    const gm = ctx.createLinearGradient(cx - r, cy - r, cx + r, cy + r); gm.addColorStop(0, '#f1f4f8'); gm.addColorStop(.5, '#8a93a4'); gm.addColorStop(1, '#3d4452');
    ctx.strokeStyle = gm; ctx.lineWidth = 4.5; ctx.beginPath(); ctx.arc(cx, cy, r, 0, TAU); ctx.stroke();
    ctx.strokeStyle = 'rgba(10,12,18,.7)'; ctx.lineWidth = 1; ctx.beginPath(); ctx.arc(cx, cy, r + 2.6, 0, TAU); ctx.stroke();
    ctx.restore();
  }

  /** Des bulles qui montent dans une zone { x0, x1, haut, bas } : n bulles, déterministes, phase en s. */
  function bulles(ctx, zone, n, phase, o = {}) {
    const r = graine(o.graine || 9), H = zone.bas - zone.haut;
    for (let k = 0; k < n; k++) {
      const u = r(), v = r(), s = r(), vit = (o.vitesse ?? 26) * (.6 + s * .8);
      const y = zone.bas - ((v * H + phase * vit) % H), x = zone.x0 + 4 + u * (zone.x1 - zone.x0 - 8) + Math.sin(phase * 2 + k) * 2.4, rad = (o.rayon ?? 2) + s * (o.variation ?? 2);
      const al = Math.min(1, (zone.bas - y) / 14, (y - zone.haut) / 8) * (o.alpha ?? 1); if (al <= 0) continue;
      ctx.save(); ctx.globalAlpha = al;
      ctx.strokeStyle = 'rgba(235,248,255,.75)'; ctx.lineWidth = 1.1; ctx.beginPath(); ctx.arc(x, y, rad, 0, TAU); ctx.stroke();
      ctx.fillStyle = 'rgba(255,255,255,.14)'; ctx.fill();
      ctx.fillStyle = 'rgba(255,255,255,.7)'; ctx.beginPath(); ctx.arc(x - rad * .35, y - rad * .35, rad * .28, 0, TAU); ctx.fill();
      ctx.restore();
    }
  }

  /**
   * Téléphone en paysage, étape de texte seul : des lignes écrites à la craie dans la boîte (x, y, w), l'une sous l'autre,
   * coupées aux mots pour tenir dans la largeur. lignes = [{ texte, couleur, cle, quand (false = pas encore) , cadre }].
   * Renvoie le y après la dernière ligne.
   */
  function fiche(c, e, lignes, o = {}) {
    const x = o.x ?? 10, w = o.w ?? 400, taille = o.taille ?? 17, pas = o.pas ?? taille * 1.32;
    let y = (o.y ?? 12) + taille;
    for (const l of lignes) {
      if (l.quand === false) continue;
      const tl = Math.max(taille, c.echelle && c.tailleMin ? c.tailleMin / c.echelle : 0), mots = String(l.texte).split(' '), rangs = []; let cur = '';
      for (const m of mots) { const essai = cur ? cur + ' ' + m : m; if (cur && c.largeurTexte(essai.replace(/_\{([^}]*)\}/g, '$1'), tl) > w) { rangs.push(cur); cur = m; } else cur = essai; }
      if (cur) rangs.push(cur);
      const y0 = y;
      e.ecrire(c, 'fiche_' + (l.cle || l.texte), () => { rangs.forEach((s, i) => c.texte(s, x, y0 + i * pas * (tl / taille), { couleur: l.couleur || 'blanc', taille, gras: l.gras })); });
      if (l.repere) c.repere(l.repere, x - 4, y0 - tl, w + 8, rangs.length * pas * (tl / taille) + 4, l.label || l.texte);
      y += rangs.length * pas * (tl / taille) + (o.espace ?? 6);
    }
    return y;
  }

  window.Ref = { page, pchip, cuve, barreau, agitateur, sonde, seringue, cable, boitier, ordinateur, loupe, bulles, fiche,
    rgba, clair, sombre, doux, mix, borne, graine, rr, TAU };
})();
