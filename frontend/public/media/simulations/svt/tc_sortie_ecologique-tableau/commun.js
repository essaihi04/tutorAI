/*
 * Commun aux simulations du cours « La sortie écologique » (Tronc commun sciences BIOF, SVT, unité 1), novembre 2026.
 *
 *  - Sortie.Scene    : cadre virtuel 760 × 420 en mode large (scene.L de 760 à 1596, hauteur 420), texte jamais sous
 *                      15 px à l'écran, boucle qui ne redessine que lorsqu'il le faut (copie du kit du cours du muscle).
 *  - Sortie.sim(o)   : une simulation « à moments » : un temps de scène S.t, des moments nommés, un seul bouton
 *                      (Lancer → Pause → Reprendre → Rejouer), les commandes start / pause / resume / reset /
 *                      play_until {moment | time_s} / set_time {time_s} / set_parameters {conclusions, …}, l'état
 *                      `ce_qui_se_voit`, la vue lue dans `?vue=`. Ce qui apparaît à un moment s'écrit à la craie à partir
 *                      de l'instant où ce moment est atteint (S.ecrit(c, nom)).
 *  - Sortie.P        : les objets du cours peints en couleur (règle du réalisme) — un seul dessin par objet dans tout le
 *                      cours : chêne-liège, olivier, arbuste, herbe, asphodèle, palmier nain (doum), mousse, lichen,
 *                      champignon, racines, bulbe, thuya, typha, roseau, jonc, plante immergée, personne, lapin, oiseau,
 *                      poisson, ver (même teinte que le ver du cours « facteurs édaphiques »), coquillage, sol, eau.
 *                      À verser dans le lexique commun (shared/lexique/) quand il aura sa fiche « végétaux ».
 *  - Sortie.lueur    : allumer en comptant (halo jaune doux, numéro écrit proprement à côté).
 */
(function () {
  'use strict';
  const VW = 760, VH = 420, TAU = Math.PI * 2;
  const TAILLE_MIN = 15, L_MAX = 2.1;

  /* ── La scène (cadre virtuel, plancher du texte) ───────────────────────────────────────────────────────────── */
  function Scene(canvas, dessiner, options = {}) {
    const scene = { sale: true, L: VW };
    const craie = new window.Tableau.Craie(canvas, { onresize: () => { scene.sale = true; } });
    // le kit récent réduit lui-même le plancher (accesseur tailleMin) ; l'ancien non
    const KIT_REDUIT = !!(Object.getOwnPropertyDescriptor(window.Tableau.Craie.prototype, 'tailleMin') || {}).get;
    /* L'écriture à la craie reste en direct, mais plus vive (≈ 34 lettres/s au lieu de 16) : les étiquettes fixes d'une
     * figure sont écrites avant que la voix n'arrive au premier moment. */
    const texte0 = craie.texte;
    craie.texte = function (s, x, y, o = {}) {
      if (o.duree == null) o = Object.assign({}, o, { duree: Math.max(.06, String(s).replace(/[⟦⟧|_]/g, '').length / (options.lettres || 34)) });
      return texte0.call(this, s, x, y, o);
    };
    const trait0 = craie.trait;
    craie.trait = function (pts, o = {}) {
      if (o.duree == null && pts && pts.length > 1) { let l = 0; for (let i = 1; i < pts.length; i++) l += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); o = Object.assign({}, o, { duree: Math.max(.05, l / (options.vitesseTrait || 1500)) }); }
      return trait0.call(this, pts, o);
    };
    Object.assign(scene, {
      craie, ouvert: performance.now(), s: 1, ox: 0, oy: 0, VH,
      cadre(graine = 7) {
        const W = craie.W, H = craie.H;
        const L = options.large === false ? VW : Math.round(Math.min(VW * L_MAX, Math.max(VW, VH * W / Math.max(1, H))));
        scene.L = L;
        craie.debut(graine, (performance.now() - scene.ouvert) / 1000);
        const s = Math.min(W / L, H / VH);
        scene.s = s; scene.ox = (W - L * s) / 2; scene.oy = (H - VH * s) / 2;
        craie.ctx.translate(scene.ox, scene.oy); craie.ctx.scale(s, s);
        /* Le kit baisse le plancher du texte sous 900 × 400 px (jusqu'à 45 %) : on le compense entièrement, le texte reste
         * à 15 px à l'écran même dans le petit cadre du lecteur sur téléphone en paysage (≈ 429 × 250, 22 novembre 2026).
         * Dans ce petit cadre (scene.petit), chaque page ne garde que l'essentiel de l'étape en cours, en grand. */
        const fKit = Math.min(1, Math.max(.45, Math.min((W || 900) / 900, (H || 400) / 400)));
        craie.echelle = s; craie.tailleMin = KIT_REDUIT ? TAILLE_MIN / fKit : TAILLE_MIN;
        scene.petit = W < 520 || H < 320;
        scene.plancher = TAILLE_MIN / s;   // la plus petite taille (unités du dessin) qui fait 15 px à l'écran
        craie.cadre = { w: L, h: VH, haut: 0 };
        return craie;
      },
      local(x, y) { return [(x - scene.ox) / scene.s, (y - scene.oy) / scene.s]; },
      reecrire() { scene.ouvert = performance.now(); scene.sale = true; },
      maintenant() { return (performance.now() - scene.ouvert) / 1000; },
      image() {
        const t = scene.ouvert; scene.ouvert = -1e9;
        try { dessiner(craie, scene); return canvas.toDataURL('image/png'); } finally { scene.ouvert = t; scene.sale = true; }
      },
    });
    let avant = performance.now();
    requestAnimationFrame(function image(maintenant) {
      const dt = Math.min(0.1, Math.max(0, (maintenant - avant) / 1000)); avant = maintenant;
      const anime = scene.avancer ? scene.avancer(dt) : false;
      if ((scene.sale || anime) && craie.W > 1) scene.sale = !dessiner(craie, scene);
      requestAnimationFrame(image);
    });
    return scene;
  }

  /* ── Allumer en comptant ─────────────────────────────────────────────────────────────────────────────────── */
  function arrondi(g, x, y, w, h, r) {
    r = Math.min(r, w / 2, h / 2);
    g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r);
    g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath();
  }
  function lueur(c, x, y, w, h, o = {}) {
    const vive = !!o.vive, couleur = o.couleur || '250, 204, 21';
    c.direct(() => {
      const g = c.ctx;
      g.save(); g.shadowColor = `rgba(${couleur}, .85)`; g.shadowBlur = vive ? 20 : 10;
      g.fillStyle = `rgba(${couleur}, ${vive ? 0.20 : 0.11})`; arrondi(g, x, y, w, h, 8); g.fill(); g.restore();
      g.save(); g.strokeStyle = `rgba(${couleur}, ${vive ? 0.95 : 0.55})`; g.lineWidth = vive ? 2.6 : 1.6;
      arrondi(g, x, y, w, h, 8); g.stroke(); g.restore();
      if (o.numero != null) c.texte(String(o.numero), o.nx ?? x - 6, o.ny ?? y + Math.min(h, 24) - 4,
        { couleur: 'jaune', taille: o.taille || 20, align: o.align || (o.nx == null ? 'right' : 'center'), gras: true });
    });
  }
  /** Coupe un texte en lignes qui tiennent dans `max` (mesure du kit). */
  function lignes(c, s, max, taille) {
    const mots = String(s).split(' '), out = []; let l = '';
    for (const m of mots) { const essai = l ? l + ' ' + m : m; if (l && c.largeurTexte(essai, taille) > max) { out.push(l); l = m; } else l = essai; }
    if (l) out.push(l);
    return out;
  }

  /* ── La simulation à moments ─────────────────────────────────────────────────────────────────────────────── */
  function param(nom, defaut = '') { try { return new URLSearchParams(location.search).get(nom) ?? defaut; } catch (_) { return defaut; } }
  const doux = u => (u <= 0 ? 0 : u >= 1 ? 1 : u * u * (3 - 2 * u));

  function sim(o) {
    const { bulle, protocole } = window.Tableau;
    const $ = id => document.getElementById(id);
    const S = { t: 0, running: false, pause: false, fait: false, jusqua: null, motif: '', emis: 0, vu: {}, conclusions: true, vue: o.vue || param('vue', o.vueDefaut || ''), p: {} };
    const M = () => (typeof o.moments === 'function' ? o.moments(S) : o.moments);
    const FIN = () => (typeof o.fin === 'function' ? o.fin(S) : o.fin);
    const canvas = $('canvas'), btn = $('run'), fb = $('feedback');
    const LANCER = o.lancer || 'Lancer';
    let scene;
    function marquer(instant) {
      const m = M(), now = instant ? -1e9 : scene.maintenant();
      for (const k in m) if (S.t >= m[k] - 1e-6 && S.vu[k] == null) S.vu[k] = now;
    }
    /** Le moment `nom` est-il atteint ? Si oui, la craie écrit la suite à partir de cet instant. */
    S.ecrit = (c, nom) => { const m = M(); if (!(nom in m) || S.t < m[nom] - 1e-6) return false; if (S.vu[nom] != null) c.depuis(S.vu[nom]); return true; };
    S.a = nom => { const m = M(); return nom in m && S.t >= m[nom] - 1e-6; };
    /** Progression 0..1 sur `d` secondes de scène après le moment `nom` (adoucie). */
    S.k = (nom, d = 1) => { const m = M(); return nom in m ? doux((S.t - m[nom]) / d) : 0; };
    S.kl = (nom, d = 1) => { const m = M(); return nom in m ? Math.max(0, Math.min(1, (S.t - m[nom]) / d)) : 0; };
    scene = Scene(canvas, (c) => { scene.cadre(o.graine || 7); o.dessiner(c, S, scene); return c.fin(); }, { large: o.large !== false });
    S.scene = scene;
    const etiquette = (txt) => { if (btn) btn.textContent = txt; };
    scene.avancer = dt => {
      if (!S.running) return false;
      S.t = Math.min(FIN(), S.t + dt); marquer();
      if (S.jusqua != null && S.t >= S.jusqua - 1e-6) {
        S.t = S.jusqua; S.jusqua = null; S.running = false; S.pause = true; etiquette('Reprendre');
        bulle(fb, 'Arrêt sur image : ' + (S.motif || 'instant choisi') + '.'); pont.noter('pause'); pont.emettre(); return true;
      }
      if (S.t >= FIN()) {
        S.running = false; S.fait = true; etiquette('Rejouer');
        bulle(fb, (typeof o.fini === 'function' ? o.fini(S) : o.fini) || 'Terminé.', 'good'); pont.noter('finished'); pont.emettre();
      } else if (performance.now() - S.emis > 450) { S.emis = performance.now(); pont.emettre(); }
      return true;
    };
    function start() { S.jusqua = null; S.t = 0; S.vu = {}; S.running = true; S.pause = false; S.fait = false; scene.reecrire(); etiquette('Pause'); bulle(fb, o.debut || 'Regarde…'); pont.noter('start'); pont.emettre(); }
    function pause() { if (!S.running) return; S.jusqua = null; S.running = false; S.pause = true; etiquette('Reprendre'); bulle(fb, 'Arrêt sur image.'); pont.noter('pause'); pont.emettre(); }
    function resume() { if (S.running) return; if (!S.pause || S.fait) return start(); S.running = true; S.pause = false; etiquette('Pause'); pont.noter('resume'); pont.emettre(); }
    function reset() { S.t = 0; S.vu = {}; S.running = false; S.pause = false; S.fait = false; S.jusqua = null; scene.reecrire(); etiquette(LANCER); bulle(fb, o.accueil || ''); pont.noter('reset'); pont.emettre(); }
    function playUntil(p) {
      const m = M(), nom = p.moment != null && p.moment in m ? p.moment : null, cible = nom ? m[nom] : +p.time_s;
      if (!Number.isFinite(cible)) return;
      if (S.fait || S.t > cible + 1e-3) { S.t = 0; S.vu = {}; scene.reecrire(); }
      S.jusqua = Math.min(FIN(), cible); S.motif = nom ? ((o.motifs || {})[nom] || nom) : ''; S.running = true; S.pause = false; S.fait = false;
      etiquette('Pause'); bulle(fb, 'Observe…'); pont.noter('play_until', { moment: nom }); pont.emettre();
    }
    function setTime(p) {
      const v = +p.time_s; if (!Number.isFinite(v)) return;
      S.t = Math.max(0, Math.min(FIN(), v)); S.vu = {}; marquer(true); S.running = false; S.jusqua = null;
      S.fait = S.t >= FIN(); S.pause = !S.fait; etiquette(S.fait ? 'Rejouer' : 'Reprendre'); scene.sale = true; pont.noter('set_time', { time_s: S.t }); pont.emettre();
    }
    function setParameters(p) {
      if (typeof p.conclusions === 'boolean') S.conclusions = p.conclusions;
      if (o.parametres) o.parametres(p, S);
      scene.sale = true; pont.noter('set_parameters', p); pont.emettre();
    }
    if (btn) btn.onclick = () => (S.running ? pause() : S.pause ? resume() : start());
    if (o.explication) window.Tableau.explication(o.explication);
    const commandes = ['start', 'pause', 'resume', 'reset', 'play_until', 'set_time', 'set_parameters'];
    const schema = Object.assign({
      play_until: { moment: Object.keys(M()).join(' | ') + ' (rejoue et se fige à cet instant clé)' },
      set_time: { time_s: '0..' + FIN() },
      set_parameters: Object.assign({ conclusions: 'true | false (false : la conclusion écrite reste cachée tant que la question est ouverte)' }, o.schemaParametres || {}),
    });
    const config = { id: o.id, version: '1.0', title: o.titre, variants: [{ id: S.vue || 'principale', label: S.vue || 'principale' }], commands: commandes, command_schema: schema };
    const pont = protocole({
      id: o.id, commandes, config, texte: o.texte,
      etat: () => ({ simulation_status: S.running ? 'running' : S.pause ? 'paused' : (S.fait ? 'finished' : 'idle'), ce_qui_se_voit: o.ceQuiSeVoit(S),
        moments: M(), time_s: +S.t.toFixed(2), current_variant: S.vue || 'principale', parameters: Object.assign({ conclusions: S.conclusions, vue: S.vue }, o.etatParametres ? o.etatParametres(S) : {}) }),
      progression: () => (S.fait ? 1 : S.t / FIN()),
      executer: (cmd, p) => ({ start, pause, resume, reset, play_until: () => playUntil(p), set_time: () => setTime(p), set_parameters: () => setParameters(p) })[cmd]?.(),
    });
    S.pont = pont;
    etiquette(LANCER); bulle(fb, o.accueil || '');
    if (o.apres) o.apres(S, scene, pont);
    return S;
  }

  /* ── Les objets du cours, peints ──────────────────────────────────────────────────────────────────────────── */
  function graine(seed) { let s = (seed >>> 0) || 1; return () => { s = (Math.imul(s, 1664525) + 1013904223) >>> 0; return s / 4294967296; }; }
  const P = {};
  P.ombre = (ctx, fn, b = 6) => { ctx.save(); ctx.shadowColor = 'rgba(0,0,0,.35)'; ctx.shadowBlur = b; ctx.shadowOffsetX = 2; ctx.shadowOffsetY = 2; fn(); ctx.restore(); };
  function boule(ctx, x, y, r, c0, c1, c2) {
    const g = ctx.createRadialGradient(x - r * .35, y - r * .4, r * .1, x, y, r);
    g.addColorStop(0, c0); g.addColorStop(.55, c1); g.addColorStop(1, c2);
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.fill();
  }
  const FEUILLAGES = {
    chene: ['#8fcf6a', '#3f8a35', '#1f4d1d'],
    olivier: ['#c9dcc0', '#7f9f84', '#405a48'],
    pistachier: ['#e3e98a', '#9fb544', '#56661f'],
    lentisque: ['#9bd27a', '#3f8f3a', '#20501f'],
    ciste: ['#c6dca4', '#7ea05c', '#47602f'],
    ajonc: ['#a8d86f', '#4e9a33', '#285a1c'],
  };
  /** Un arbre : tronc (liège crevassé pour le chêne-liège) et houppier en boules de feuillage. h = hauteur totale. */
  P.arbre = (ctx, x, yb, h, o = {}) => {
    const sorte = o.sorte || 'chene', F = FEUILLAGES[sorte] || FEUILLAGES.chene, r = graine(o.graine ?? Math.round(x * 7 + h));
    const lt = Math.max(3, h * .085), ht = h * .52, R = h * .27;
    ctx.save(); ctx.globalAlpha = o.alpha ?? 1;
    P.ombre(ctx, () => {
      const g = ctx.createLinearGradient(x - lt, 0, x + lt, 0);
      if (sorte === 'chene') { g.addColorStop(0, '#5d4a3a'); g.addColorStop(.45, '#a58f74'); g.addColorStop(1, '#4b3a2c'); }
      else { g.addColorStop(0, '#5a4636'); g.addColorStop(.5, '#8a6d52'); g.addColorStop(1, '#4a3828'); }
      ctx.fillStyle = g; ctx.beginPath();
      ctx.moveTo(x - lt * 1.3, yb); ctx.quadraticCurveTo(x - lt * .7, yb - ht * .5, x - lt * .6, yb - ht);
      ctx.lineTo(x + lt * .6, yb - ht); ctx.quadraticCurveTo(x + lt * .7, yb - ht * .5, x + lt * 1.3, yb); ctx.closePath(); ctx.fill();
    });
    if (sorte === 'chene' && h > 40) {   // le liège : crevasses sombres
      ctx.strokeStyle = 'rgba(40,28,20,.55)'; ctx.lineWidth = 1;
      for (let i = 0; i < 6; i++) { const yy = yb - ht * (.1 + .13 * i); ctx.beginPath(); ctx.moveTo(x - lt * .6, yy); ctx.lineTo(x + lt * (.2 - r() * .5), yy - 4); ctx.lineTo(x + lt * .6, yy - 1); ctx.stroke(); }
    }
    // branches
    ctx.strokeStyle = '#6b5440'; ctx.lineWidth = Math.max(1.5, lt * .45); ctx.lineCap = 'round';
    for (const s of [-1, 1]) { ctx.beginPath(); ctx.moveTo(x, yb - ht * .9); ctx.quadraticCurveTo(x + s * R * .3, yb - ht * 1.05, x + s * R * .6, yb - ht * 1.25); ctx.stroke(); }
    const cy = yb - h + R * 1.05, blobs = [[0, 0, 1], [-.6, .25, .72], [.62, .22, .75], [-.3, -.35, .7], [.35, -.38, .66], [0, .42, .7]];
    P.ombre(ctx, () => { ctx.fillStyle = F[2]; ctx.beginPath(); for (const [dx, dy, k] of blobs) { ctx.moveTo(x + dx * R + k * R * .8, cy + dy * R); ctx.arc(x + dx * R, cy + dy * R, k * R * .8, 0, TAU); } ctx.fill(); }, 8);
    for (const [dx, dy, k] of blobs) boule(ctx, x + dx * R - 1, cy + dy * R - 1, k * R * .75, F[0], F[1], F[2]);
    if (sorte === 'olivier') { ctx.fillStyle = 'rgba(40,50,60,.8)'; for (let i = 0; i < 6; i++) { ctx.beginPath(); ctx.arc(x + (r() - .5) * R * 1.4, cy + (r() - .5) * R, Math.max(1, R * .06), 0, TAU); ctx.fill(); } }
    ctx.restore();
  };
  /** Un arbuste (ciste, ajonc, lentisque) : plusieurs tiges, boules de feuillage basses, fleurs selon l'espèce. */
  P.arbuste = (ctx, x, yb, h, o = {}) => {
    const sorte = o.sorte || 'ciste', F = FEUILLAGES[sorte] || FEUILLAGES.ciste, r = graine(o.graine ?? Math.round(x * 5 + h * 3));
    ctx.save(); ctx.globalAlpha = o.alpha ?? 1;
    ctx.strokeStyle = '#6b5440'; ctx.lineWidth = Math.max(1.2, h * .04); ctx.lineCap = 'round';
    for (let i = -2; i <= 2; i++) { ctx.beginPath(); ctx.moveTo(x + i * 2, yb); ctx.quadraticCurveTo(x + i * h * .08, yb - h * .4, x + i * h * .16, yb - h * .65); ctx.stroke(); }
    const R = h * .26, pts = [[0, -.78, 1], [-.45, -.55, .85], [.45, -.55, .85], [-.25, -.35, .7], [.28, -.32, .72]];
    P.ombre(ctx, () => { ctx.fillStyle = F[2]; ctx.beginPath(); for (const [dx, dy, k] of pts) { ctx.moveTo(x + dx * h + k * R, yb + dy * h); ctx.arc(x + dx * h, yb + dy * h, k * R, 0, TAU); } ctx.fill(); });
    for (const [dx, dy, k] of pts) boule(ctx, x + dx * h, yb + dy * h, k * R * .95, F[0], F[1], F[2]);
    const fleur = sorte === 'ciste' ? '#fff7f7' : sorte === 'ajonc' ? '#facc15' : null;
    if (fleur) { for (let i = 0; i < 9; i++) { const a = r() * TAU, d = r() * h * .45; P.fleur(ctx, x + Math.cos(a) * d * .9, yb - h * .58 + Math.sin(a) * d * .5, Math.max(1.6, h * .045), fleur, 5); } }
    ctx.restore();
  };
  /** Une petite fleur (5 pétales par défaut). */
  P.fleur = (ctx, x, y, r, couleur, n = 5) => {
    ctx.fillStyle = couleur;
    for (let i = 0; i < n; i++) { const a = i / n * TAU; ctx.beginPath(); ctx.ellipse(x + Math.cos(a) * r * .7, y + Math.sin(a) * r * .7, r * .6, r * .4, a, 0, TAU); ctx.fill(); }
    ctx.fillStyle = '#f59e0b'; ctx.beginPath(); ctx.arc(x, y, r * .38, 0, TAU); ctx.fill();
  };
  /** Une touffe d'herbe (graminée) : brins courbes, épis si o.epi. */
  P.herbe = (ctx, x, yb, h, o = {}) => {
    const r = graine(o.graine ?? Math.round(x * 11 + 3)), n = o.n ?? 7;
    ctx.save(); ctx.globalAlpha = o.alpha ?? 1; ctx.lineCap = 'round';
    for (let i = 0; i < n; i++) {
      const dx = (i - (n - 1) / 2) * h * .07, hh = h * (.7 + r() * .3), pench = (r() - .5) * h * .5;
      const g = ctx.createLinearGradient(0, yb, 0, yb - hh); g.addColorStop(0, '#3f7d2a'); g.addColorStop(1, o.sec ? '#d9c97a' : '#a3e070');
      ctx.strokeStyle = g; ctx.lineWidth = Math.max(1.2, h * .045);
      ctx.beginPath(); ctx.moveTo(x + dx, yb); ctx.quadraticCurveTo(x + dx + pench * .3, yb - hh * .6, x + dx + pench, yb - hh); ctx.stroke();
      if (o.epi && i % 2 === 0) { ctx.fillStyle = '#d6c27a'; ctx.beginPath(); ctx.ellipse(x + dx + pench, yb - hh - h * .06, h * .03, h * .09, Math.atan2(pench, hh) * .6, 0, TAU); ctx.fill(); }
    }
    ctx.restore();
  };
  /** L'asphodèle : hampe, fleurs blanches en étoile, feuilles en ruban, bulbe sous le sol si o.bulbe. */
  P.asphodele = (ctx, x, yb, h, o = {}) => {
    ctx.save(); ctx.globalAlpha = o.alpha ?? 1; ctx.lineCap = 'round';
    for (const s of [-1, 1, -.4, .5]) { ctx.strokeStyle = '#5c9a3a'; ctx.lineWidth = Math.max(1.5, h * .05); ctx.beginPath(); ctx.moveTo(x, yb); ctx.quadraticCurveTo(x + s * h * .15, yb - h * .3, x + s * h * .3, yb - h * .45); ctx.stroke(); }
    ctx.strokeStyle = '#6aa84a'; ctx.lineWidth = Math.max(1.2, h * .03); ctx.beginPath(); ctx.moveTo(x, yb); ctx.lineTo(x + 1, yb - h); ctx.stroke();
    for (let i = 0; i < 7; i++) P.fleur(ctx, x + (i % 2 ? 4 : -4) * h / 60, yb - h * (.62 + i * .055), Math.max(1.6, h * .045), '#fdfdfd', 6);
    if (o.bulbe) P.bulbe(ctx, x, yb + h * .12, h * .1);
    ctx.restore();
  };
  P.bulbe = (ctx, x, y, r) => {
    P.ombre(ctx, () => boule(ctx, x, y, r, '#fff1d6', '#d9b98a', '#9c7a4e'), 4);
    ctx.strokeStyle = 'rgba(214,190,150,.9)'; ctx.lineWidth = 1;
    for (let i = -2; i <= 2; i++) { ctx.beginPath(); ctx.moveTo(x + i * r * .2, y + r * .8); ctx.quadraticCurveTo(x + i * r * .4, y + r * 1.5, x + i * r * .55, y + r * 2.1); ctx.stroke(); }
  };
  /** Le palmier nain (doum, Chamaerops humilis) : palmes en éventail sur un court stipe. */
  P.palmier = (ctx, x, yb, h, o = {}) => {
    ctx.save(); ctx.globalAlpha = o.alpha ?? 1; ctx.lineCap = 'round';
    ctx.fillStyle = '#7a5b3c'; ctx.fillRect(x - h * .05, yb - h * .25, h * .1, h * .25);
    for (let i = 0; i < 7; i++) {
      const a = -Math.PI / 2 + (i - 3) * .38, px = x + Math.cos(a) * h * .55, py = yb - h * .25 + Math.sin(a) * h * .7;
      ctx.strokeStyle = '#3d7a2c'; ctx.lineWidth = Math.max(1, h * .025); ctx.beginPath(); ctx.moveTo(x, yb - h * .25); ctx.lineTo(px, py); ctx.stroke();
      ctx.fillStyle = i % 2 ? '#5fae45' : '#4a9a38';
      ctx.beginPath(); ctx.moveTo(px, py);
      for (let k = -3; k <= 3; k++) { const b = a + k * .13; ctx.lineTo(px + Math.cos(b) * h * .25, py + Math.sin(b) * h * .25); }
      ctx.closePath(); ctx.fill();
    }
    ctx.restore();
  };
  /** La mousse : un coussin vert bosselé, au ras du sol. */
  P.mousse = (ctx, x, yb, w, o = {}) => {
    const r = graine(o.graine ?? Math.round(x * 3 + 1));
    ctx.save(); ctx.globalAlpha = o.alpha ?? 1;
    P.ombre(ctx, () => { ctx.fillStyle = '#2e6b22'; ctx.beginPath(); ctx.ellipse(x, yb - w * .1, w / 2, w * .16, 0, Math.PI, 0); ctx.fill(); }, 4);
    for (let i = 0; i < 16; i++) { const px = x + (r() - .5) * w * .9, py = yb - w * .06 - r() * w * .12; boule(ctx, px, py, w * .07, '#b7e58a', '#58a23c', '#2e6b22'); }
    ctx.restore();
  };
  /** Un lichen : tache lobée jaune-orangé (ou grise) collée sur un support. */
  P.lichen = (ctx, x, y, r, o = {}) => {
    const rr = graine(o.graine ?? Math.round(x * 13 + y)), c = o.gris ? ['#e5e9e0', '#a9b3a3', '#6f7a6a'] : ['#fff3a0', '#e8c22a', '#a8820f'];
    ctx.save(); ctx.globalAlpha = o.alpha ?? 1;
    for (let i = 0; i < 9; i++) { const a = rr() * TAU, d = rr() * r * .7; boule(ctx, x + Math.cos(a) * d, y + Math.sin(a) * d * .8, r * (.25 + rr() * .2), c[0], c[1], c[2]); }
    ctx.restore();
  };
  P.champignon = (ctx, x, yb, s, o = {}) => {
    ctx.save(); ctx.globalAlpha = o.alpha ?? 1;
    ctx.fillStyle = '#f3ead8'; ctx.fillRect(x - s * .12, yb - s * .55, s * .24, s * .55);
    P.ombre(ctx, () => { const g = ctx.createLinearGradient(0, yb - s, 0, yb - s * .5); g.addColorStop(0, '#f6c870'); g.addColorStop(1, '#b77a2e'); ctx.fillStyle = g; ctx.beginPath(); ctx.ellipse(x, yb - s * .55, s * .45, s * .35, 0, Math.PI, 0); ctx.fill(); }, 3);
    ctx.restore();
  };
  /** Des racines brunes ramifiées sous un point du sol. */
  P.racines = (ctx, x, yb, prof, larg, o = {}) => {
    const r = graine(o.graine ?? Math.round(x * 17 + prof));
    ctx.save(); ctx.globalAlpha = o.alpha ?? 1; ctx.lineCap = 'round';
    const branche = (x0, y0, a, l, w, n) => {
      if (n <= 0 || l < 4) return;
      const x1 = x0 + Math.cos(a) * l, y1 = y0 + Math.sin(a) * l;
      ctx.strokeStyle = n > 2 ? '#8a6a48' : '#c9a982'; ctx.lineWidth = w; ctx.beginPath(); ctx.moveTo(x0, y0);
      ctx.quadraticCurveTo((x0 + x1) / 2 + (r() - .5) * l * .3, (y0 + y1) / 2, x1, y1); ctx.stroke();
      branche(x1, y1, a - .35 - r() * .3, l * .7, w * .65, n - 1); branche(x1, y1, a + .35 + r() * .3, l * .7, w * .65, n - 1);
    };
    for (const a of [Math.PI / 2, Math.PI / 2 - .7, Math.PI / 2 + .7]) branche(x, yb, a, prof * .45, Math.max(1, larg), 4);
    ctx.restore();
  };
  /** Le rhizome : tige souterraine horizontale avec ses racines. */
  P.rhizome = (ctx, x, y, l) => {
    ctx.save(); ctx.lineCap = 'round'; ctx.strokeStyle = '#b8895a'; ctx.lineWidth = 5; ctx.beginPath(); ctx.moveTo(x - l / 2, y); ctx.quadraticCurveTo(x, y + 4, x + l / 2, y - 2); ctx.stroke();
    ctx.strokeStyle = '#d9b98a'; ctx.lineWidth = 1;
    for (let i = 0; i < 6; i++) { const px = x - l / 2 + i * l / 5; ctx.beginPath(); ctx.moveTo(px, y + 2); ctx.lineTo(px + 3, y + 12); ctx.stroke(); }
    ctx.restore();
  };
  /** Le thuya : arbre conique vert olive. */
  P.thuya = (ctx, x, yb, h, o = {}) => {
    ctx.save(); ctx.globalAlpha = o.alpha ?? 1;
    ctx.fillStyle = '#6b5440'; ctx.fillRect(x - h * .04, yb - h * .2, h * .08, h * .2);
    P.ombre(ctx, () => {
      const g = ctx.createLinearGradient(x - h * .22, 0, x + h * .22, 0); g.addColorStop(0, '#3c5a24'); g.addColorStop(.45, '#8fae4a'); g.addColorStop(1, '#2d4519');
      ctx.fillStyle = g; ctx.beginPath(); ctx.moveTo(x, yb - h); ctx.quadraticCurveTo(x + h * .26, yb - h * .45, x + h * .2, yb - h * .15);
      ctx.lineTo(x - h * .2, yb - h * .15); ctx.quadraticCurveTo(x - h * .26, yb - h * .45, x, yb - h); ctx.fill();
    });
    ctx.restore();
  };
  /** Petit arbuste à fleurs roses (tizra). */
  P.tizra = (ctx, x, yb, h, o = {}) => {
    ctx.save(); ctx.globalAlpha = o.alpha ?? 1; ctx.lineCap = 'round'; ctx.strokeStyle = '#4f8a35'; ctx.lineWidth = Math.max(1.2, h * .06);
    ctx.beginPath(); ctx.moveTo(x, yb); ctx.lineTo(x, yb - h * .8); ctx.stroke();
    for (const s of [-1, 1]) { ctx.beginPath(); ctx.moveTo(x, yb - h * .35); ctx.quadraticCurveTo(x + s * h * .2, yb - h * .45, x + s * h * .28, yb - h * .6); ctx.stroke(); }
    P.fleur(ctx, x, yb - h * .85, Math.max(2, h * .14), '#ec4899', 6);
    ctx.restore();
  };
  /** Les plantes de la daya : typha (massette), roseau (phragmite), jonc, plante immergée. */
  P.typha = (ctx, x, yb, h, o = {}) => {
    ctx.save(); ctx.globalAlpha = o.alpha ?? 1; ctx.lineCap = 'round';
    for (const s of [-1, -.4, .5, 1]) { ctx.strokeStyle = '#4f9a3a'; ctx.lineWidth = Math.max(1.5, h * .03); ctx.beginPath(); ctx.moveTo(x, yb); ctx.quadraticCurveTo(x + s * h * .12, yb - h * .45, x + s * h * .22, yb - h * .8); ctx.stroke(); }
    ctx.strokeStyle = '#5d8a3a'; ctx.lineWidth = Math.max(1.2, h * .02); ctx.beginPath(); ctx.moveTo(x, yb); ctx.lineTo(x, yb - h); ctx.stroke();
    const g = ctx.createLinearGradient(x - h * .04, 0, x + h * .04, 0); g.addColorStop(0, '#4a2a14'); g.addColorStop(.5, '#8a5a32'); g.addColorStop(1, '#3a200e');
    P.ombre(ctx, () => { ctx.fillStyle = g; ctx.beginPath(); ctx.ellipse(x, yb - h * .82, h * .045, h * .11, 0, 0, TAU); ctx.fill(); }, 3);
    ctx.restore();
  };
  P.roseau = (ctx, x, yb, h, o = {}) => {
    ctx.save(); ctx.globalAlpha = o.alpha ?? 1; ctx.lineCap = 'round';
    ctx.strokeStyle = '#8fae4a'; ctx.lineWidth = Math.max(1.2, h * .025); ctx.beginPath(); ctx.moveTo(x, yb); ctx.quadraticCurveTo(x + h * .05, yb - h * .5, x + h * .08, yb - h); ctx.stroke();
    for (let i = 0; i < 5; i++) { const yy = yb - h * (.25 + i * .14), s = i % 2 ? 1 : -1; ctx.strokeStyle = '#a5c85a'; ctx.lineWidth = Math.max(1.2, h * .02); ctx.beginPath(); ctx.moveTo(x + h * .02 * i / 4, yy); ctx.quadraticCurveTo(x + s * h * .12, yy - h * .02, x + s * h * .22, yy + h * .04); ctx.stroke(); }
    ctx.fillStyle = '#c9a36a'; ctx.beginPath(); ctx.ellipse(x + h * .1, yb - h * 1.02, h * .05, h * .09, .3, 0, TAU); ctx.fill();
    ctx.restore();
  };
  P.jonc = (ctx, x, yb, h, o = {}) => {
    ctx.save(); ctx.globalAlpha = o.alpha ?? 1; ctx.lineCap = 'round';
    for (let i = -3; i <= 3; i++) { ctx.strokeStyle = i % 2 ? '#3f8a35' : '#5aa845'; ctx.lineWidth = Math.max(1, h * .03); ctx.beginPath(); ctx.moveTo(x + i * 1.5, yb); ctx.quadraticCurveTo(x + i * h * .05, yb - h * .6, x + i * h * .1, yb - h); ctx.stroke(); }
    ctx.restore();
  };
  P.immergee = (ctx, x, yb, h, o = {}) => {
    ctx.save(); ctx.globalAlpha = o.alpha ?? 1; ctx.lineCap = 'round';
    ctx.strokeStyle = '#2f7a4a'; ctx.lineWidth = Math.max(1.2, h * .03); ctx.beginPath(); ctx.moveTo(x, yb); ctx.bezierCurveTo(x - h * .15, yb - h * .35, x + h * .15, yb - h * .65, x, yb - h); ctx.stroke();
    for (let i = 0; i < 8; i++) { const t = .15 + i * .1, yy = yb - h * t, xx = x + Math.sin(t * 6) * h * .08, s = i % 2 ? 1 : -1;
      ctx.fillStyle = i % 2 ? 'rgba(80,170,110,.9)' : 'rgba(60,140,90,.9)'; ctx.beginPath(); ctx.ellipse(xx + s * h * .07, yy, h * .08, h * .025, s * .5, 0, TAU); ctx.fill(); }
    ctx.restore();
  };
  /** Une personne debout, de profil vers la droite ; o.vise : le bras levé à l'œil (croix du bûcheron). Renvoie l'œil. */
  P.personne = (ctx, x, yb, h, o = {}) => {
    const tete = h * .12, epaule = yb - h * .8, hanche = yb - h * .47, oeil = [x + tete * .45, yb - h * .9];
    ctx.save(); ctx.globalAlpha = o.alpha ?? 1; ctx.lineCap = 'round';
    P.ombre(ctx, () => {
      ctx.strokeStyle = '#334155'; ctx.lineWidth = h * .09;   // jambes (pantalon)
      ctx.beginPath(); ctx.moveTo(x - h * .02, hanche); ctx.lineTo(x - h * .06, yb - 2); ctx.moveTo(x + h * .02, hanche); ctx.lineTo(x + h * .07, yb - 2); ctx.stroke();
      ctx.fillStyle = '#1f2937'; ctx.beginPath(); ctx.ellipse(x - h * .04, yb - 2, h * .06, h * .025, 0, 0, TAU); ctx.ellipse(x + h * .1, yb - 2, h * .06, h * .025, 0, 0, TAU); ctx.fill();
      const g = ctx.createLinearGradient(x - h * .1, 0, x + h * .1, 0); g.addColorStop(0, '#1d4ed8'); g.addColorStop(.5, '#3b82f6'); g.addColorStop(1, '#1e3a8a');
      ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(x - h * .085, epaule, h * .17, hanche - epaule + h * .03, h * .04); ctx.fill();
      ctx.fillStyle = '#e0ac83'; ctx.beginPath(); ctx.arc(x, yb - h * .9, tete, 0, TAU); ctx.fill();
      ctx.fillStyle = '#3b2a1e'; ctx.beginPath(); ctx.arc(x - tete * .15, yb - h * .9 - tete * .25, tete * .95, Math.PI * .95, Math.PI * 2.05); ctx.fill();
    }, 5);
    ctx.strokeStyle = '#3b82f6'; ctx.lineWidth = h * .055;   // bras
    if (o.vise) { ctx.beginPath(); ctx.moveTo(x + h * .02, epaule + h * .05); ctx.lineTo(oeil[0] + h * .1, oeil[1] + h * .05); ctx.stroke(); }
    else { ctx.beginPath(); ctx.moveTo(x, epaule + h * .04); ctx.lineTo(x + h * .03, hanche); ctx.stroke(); }
    ctx.fillStyle = '#1f2937'; ctx.beginPath(); ctx.arc(oeil[0], oeil[1], Math.max(1.2, h * .012), 0, TAU); ctx.fill();
    ctx.restore();
    return oeil;
  };
  P.lapin = (ctx, x, yb, s, o = {}) => {
    ctx.save(); ctx.globalAlpha = o.alpha ?? 1;
    P.ombre(ctx, () => {
      boule(ctx, x, yb - s * .35, s * .38, '#e7d5c0', '#a88c70', '#6d5743');
      boule(ctx, x + s * .38, yb - s * .62, s * .2, '#e7d5c0', '#a88c70', '#6d5743');
      ctx.fillStyle = '#a88c70'; ctx.beginPath(); ctx.ellipse(x + s * .36, yb - s * .95, s * .06, s * .2, -.2, 0, TAU); ctx.ellipse(x + s * .46, yb - s * .93, s * .06, s * .2, .2, 0, TAU); ctx.fill();
      ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(x - s * .38, yb - s * .38, s * .1, 0, TAU); ctx.fill();
    }, 4);
    ctx.fillStyle = '#111'; ctx.beginPath(); ctx.arc(x + s * .45, yb - s * .66, s * .03, 0, TAU); ctx.fill();
    ctx.restore();
  };
  P.oiseau = (ctx, x, y, s, o = {}) => {
    ctx.save(); ctx.globalAlpha = o.alpha ?? 1;
    P.ombre(ctx, () => {
      ctx.fillStyle = '#8a5a32'; ctx.beginPath(); ctx.ellipse(x, y, s * .4, s * .16, 0, 0, TAU); ctx.fill();
      ctx.fillStyle = '#6b4424'; ctx.beginPath(); ctx.moveTo(x - s * .1, y - s * .05); ctx.quadraticCurveTo(x - s * .4, y - s * .5, x - s * .8, y - s * .35); ctx.quadraticCurveTo(x - s * .4, y - s * .12, x - s * .1, y + s * .02); ctx.fill();
      ctx.beginPath(); ctx.moveTo(x + s * .1, y - s * .05); ctx.quadraticCurveTo(x + s * .4, y - s * .5, x + s * .8, y - s * .35); ctx.quadraticCurveTo(x + s * .4, y - s * .12, x + s * .1, y + s * .02); ctx.fill();
      boule(ctx, x + s * .38, y - s * .05, s * .13, '#d6b48a', '#8a5a32', '#5a3a1e');
    }, 4);
    ctx.fillStyle = '#f59e0b'; ctx.beginPath(); ctx.moveTo(x + s * .5, y - s * .07); ctx.lineTo(x + s * .62, y - s * .02); ctx.lineTo(x + s * .5, y + s * .01); ctx.fill();
    ctx.restore();
  };
  P.poisson = (ctx, x, y, s, o = {}) => {
    ctx.save(); ctx.globalAlpha = o.alpha ?? 1;
    const g = ctx.createLinearGradient(0, y - s * .2, 0, y + s * .2); g.addColorStop(0, '#fbbf24'); g.addColorStop(1, '#ea580c');
    ctx.fillStyle = g; ctx.beginPath(); ctx.ellipse(x, y, s * .4, s * .17, 0, 0, TAU); ctx.fill();
    ctx.beginPath(); ctx.moveTo(x - s * .35, y); ctx.lineTo(x - s * .6, y - s * .16); ctx.lineTo(x - s * .6, y + s * .16); ctx.fill();
    ctx.fillStyle = '#111'; ctx.beginPath(); ctx.arc(x + s * .25, y - s * .03, s * .03, 0, TAU); ctx.fill();
    ctx.restore();
  };
  /** Un ver (annélide) le long d'un chemin de points : même teinte que le ver du cours des facteurs édaphiques. */
  P.ver = (ctx, pts, o = {}) => {
    const e = o.e ?? 6;
    ctx.save(); ctx.globalAlpha = o.alpha ?? 1; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    ctx.strokeStyle = 'rgba(60,20,20,.6)'; ctx.lineWidth = e + 2; ctx.beginPath(); pts.forEach(([x, y], i) => (i ? ctx.lineTo(x, y) : ctx.moveTo(x, y))); ctx.stroke();
    ctx.strokeStyle = o.teinte || 'rgb(196,110,110)'; ctx.lineWidth = e; ctx.stroke();
    ctx.strokeStyle = 'rgba(255,220,220,.45)'; ctx.lineWidth = e * .3; ctx.stroke();
    ctx.strokeStyle = 'rgba(110,40,40,.5)'; ctx.lineWidth = 1;
    for (let i = 1; i < pts.length - 1; i++) { const [x0, y0] = pts[i - 1], [x1, y1] = pts[i + 1], a = Math.atan2(y1 - y0, x1 - x0) + Math.PI / 2; ctx.beginPath(); ctx.moveTo(pts[i][0] + Math.cos(a) * e / 2, pts[i][1] + Math.sin(a) * e / 2); ctx.lineTo(pts[i][0] - Math.cos(a) * e / 2, pts[i][1] - Math.sin(a) * e / 2); ctx.stroke(); }
    ctx.restore();
  };
  /** Un ver ondulé centré en (x, y), longueur l, orientation a. */
  P.verOndule = (ctx, x, y, l, a = 0, o = {}) => {
    const pts = []; for (let i = 0; i <= 10; i++) { const u = i / 10 - .5, px = u * l, py = Math.sin(u * 9 + (o.phase || 0)) * l * .08; pts.push([x + px * Math.cos(a) - py * Math.sin(a), y + px * Math.sin(a) + py * Math.cos(a)]); }
    P.ver(ctx, pts, o);
  };
  /** Un coquillage bivalve (mollusque) vu de dessus. */
  P.coquillage = (ctx, x, y, s, o = {}) => {
    ctx.save(); ctx.globalAlpha = o.alpha ?? 1; ctx.translate(x, y); ctx.rotate(o.a || 0);
    P.ombre(ctx, () => { const g = ctx.createRadialGradient(-s * .1, -s * .2, s * .05, 0, 0, s * .5); g.addColorStop(0, '#fff7ed'); g.addColorStop(.6, o.teinte || '#d6b48a'); g.addColorStop(1, '#8a6a48'); ctx.fillStyle = g; ctx.beginPath(); ctx.ellipse(0, 0, s * .5, s * .38, 0, 0, TAU); ctx.fill(); }, 3);
    ctx.strokeStyle = 'rgba(90,60,30,.45)'; ctx.lineWidth = 1;
    for (let i = -2; i <= 2; i++) { ctx.beginPath(); ctx.moveTo(0, s * .3); ctx.lineTo(i * s * .18, -s * .32); ctx.stroke(); }
    ctx.restore();
  };
  /** Une bande de sol peinte (dégradé brun, cailloux). */
  P.sol = (ctx, x, y, w, h, o = {}) => {
    const r = graine(o.graine ?? 5);
    ctx.save(); ctx.globalAlpha = o.alpha ?? 1;
    const g = ctx.createLinearGradient(0, y, 0, y + h); g.addColorStop(0, o.haut || '#c9a479'); g.addColorStop(1, o.bas || '#8a6440');
    ctx.fillStyle = g; ctx.fillRect(x, y, w, h);
    for (let i = 0; i < w * h / 900; i++) { const px = x + r() * w, py = y + 6 + r() * (h - 10); ctx.fillStyle = r() > .5 ? 'rgba(110,78,48,.8)' : 'rgba(150,112,72,.8)'; ctx.beginPath(); ctx.ellipse(px, py, 3 + r() * 6, 2 + r() * 3, r() * 3, 0, TAU); ctx.fill(); }
    ctx.restore();
  };
  /** Une pierre (roche) peinte. */
  P.pierre = (ctx, x, y, r, o = {}) => { ctx.save(); ctx.globalAlpha = o.alpha ?? 1; P.ombre(ctx, () => { const g = ctx.createRadialGradient(x - r * .3, y - r * .3, r * .1, x, y, r); g.addColorStop(0, '#e2ddd3'); g.addColorStop(.6, '#a39b8c'); g.addColorStop(1, '#6b6457'); ctx.fillStyle = g; ctx.beginPath(); ctx.ellipse(x, y, r, r * .62, 0, 0, TAU); ctx.fill(); }, 4); ctx.restore(); };
  P.soleil = (ctx, x, y, r, o = {}) => {
    ctx.save(); ctx.globalAlpha = o.alpha ?? 1;
    const g = ctx.createRadialGradient(x, y, r * .2, x, y, r * 2.2); g.addColorStop(0, 'rgba(253,224,71,.55)'); g.addColorStop(1, 'rgba(253,224,71,0)');
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r * 2.2, 0, TAU); ctx.fill();
    boule(ctx, x, y, r, '#fffbe0', '#fde047', '#f59e0b');
    ctx.restore();
  };
  P.nuage = (ctx, x, y, s, o = {}) => {
    ctx.save(); ctx.globalAlpha = o.alpha ?? 1;
    for (const [dx, dy, k] of [[0, 0, .35], [-.35, .08, .25], [.35, .08, .27], [.15, -.15, .25]]) boule(ctx, x + dx * s, y + dy * s, k * s, '#f1f5f9', '#cbd5e1', '#94a3b8');
    if (o.pluie) { ctx.strokeStyle = 'rgba(147,197,253,.85)'; ctx.lineWidth = 1.6; for (let i = 0; i < 9; i++) { const px = x - s * .5 + i * s * .12, py = y + s * .3 + ((i * 7 + (o.phase || 0) * 40) % (s * .5)); ctx.beginPath(); ctx.moveTo(px, py); ctx.lineTo(px - 3, py + 9); ctx.stroke(); } }
    ctx.restore();
  };

  window.Sortie = { Scene, VW, VH, TAU, lueur, lignes, sim, param, doux, graine, P, boule };
})();
