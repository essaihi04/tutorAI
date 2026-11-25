/*
 * Commun aux simulations du cours « Modèle de l'atome » (Tronc Commun sciences, option française, chimie), novembre 2026.
 *
 *  - Atome.Scene    : cadre virtuel 760 × 420 en mode large (scene.L de 760 à 1596, hauteur 420), texte jamais sous 15 px à
 *                     l'écran, boucle qui ne redessine que lorsqu'il le faut (même kit que le cours de SVT « sortie écologique »).
 *  - Atome.sim(o)   : une simulation « à moments » : un temps de scène S.t, des moments nommés, un seul bouton
 *                     (Lancer → Pause → Reprendre → Rejouer), les commandes start / pause / resume / reset /
 *                     play_until {moment | time_s} / set_time {time_s} / set_parameters {conclusions, …}, l'état
 *                     `ce_qui_se_voit`, la vue lue dans `?vue=`. Ce qui apparaît à un moment s'écrit à la craie à partir de
 *                     l'instant où ce moment est atteint (S.ecrit(c, nom)).
 *  - Atome.P        : les objets du cours, peints — UN SEUL DESSIN PAR OBJET dans tout le cours (et dans tout le site : les
 *                     particules viennent du lexique commun shared/lexique/lexique.js) :
 *                       proton   = bille ROSE marquée « + »  (Lexique.proton ; le même rose que l'ion H⁺ des autres cours)
 *                       neutron  = bille GRISE               (Lexique.neutron)
 *                       électron = petite bille BLEU CIEL « e− » (Lexique.electron)
 *                       noyau    = amas serré de protons et de neutrons, avec un halo rose (P.noyau)
 *                       atome    = noyau au centre + nuage bleu ciel d'électrons (P.nuage) ou couches K, L, M (P.couche)
 *                     charge + : rose ; charge − : bleu ciel (même code que les particules) ; particule α : orange.
 *  - Atome.lueur    : allumer en comptant (halo jaune doux).
 *  - Atome.notation : l'écriture ᴬ_Z X à la craie (A en haut à gauche, Z en bas à gauche).
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
    S.momentDe = nom => { const m = M(); return nom in m ? m[nom] : null; };
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
  const Lx = () => window.Lexique || {};
  const P = {};
  P.ombre = (ctx, fn, b = 6) => { ctx.save(); ctx.shadowColor = 'rgba(0,0,0,.35)'; ctx.shadowBlur = b; ctx.shadowOffsetX = 2; ctx.shadowOffsetY = 2; fn(); ctx.restore(); };
  /** Sphère ombrée (dégradé radial, reflet). c = [r, g, b]. */
  function boule(ctx, x, y, r, c, a = 1) {
    ctx.save(); ctx.globalAlpha *= a;
    ctx.fillStyle = 'rgba(0,0,0,.22)'; ctx.beginPath(); ctx.ellipse(x + r * .2, y + r * .92, r * .8, r * .22, 0, 0, TAU); ctx.fill();
    const g = ctx.createRadialGradient(x - r * .35, y - r * .4, r * .08, x, y, r);
    g.addColorStop(0, `rgb(${c.map(v => Math.min(255, v + 110)).join(',')})`); g.addColorStop(.5, `rgb(${c.join(',')})`); g.addColorStop(1, `rgb(${c.map(v => Math.round(v * .45)).join(',')})`);
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.fill();
    ctx.fillStyle = 'rgba(255,255,255,.5)'; ctx.beginPath(); ctx.ellipse(x - r * .35, y - r * .42, r * .24, r * .15, -.6, 0, TAU); ctx.fill();
    ctx.restore();
  }
  const COUL = { proton: [244, 114, 182], neutron: [160, 168, 180], electron: [96, 200, 250], alpha: [251, 146, 60], or: [234, 179, 8],
    carbone: [250, 204, 21], oxygene: [235, 85, 70], hydrogene: [235, 240, 245], azote: [96, 130, 240] };
  const POLICE = "'Patrick Hand','Caveat','Segoe Print','Comic Sans MS',cursive";
  function inscrire(ctx, s, x, y, t, couleur = '#0b1f2a', a = 1) {
    ctx.save(); ctx.globalAlpha *= a; ctx.fillStyle = couleur; ctx.font = `700 ${t}px ${POLICE}`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillText(s, x, y + 1); ctx.restore();
  }
  /* ── Les particules (lexique commun) ── */
  /** Le PROTON : bille rose marquée « + » ; o.numero : son numéro (on compte en allumant) écrit à la place du « + ». */
  P.proton = (ctx, x, y, r = 9, o = {}) => {
    const L = Lx();
    if (L.proton) L.proton(ctx, x, y, { r, texte: false, alpha: o.alpha ?? 1 }); else boule(ctx, x, y, r, COUL.proton, o.alpha ?? 1);
    if (o.texte !== false && r >= 6) inscrire(ctx, o.numero != null ? String(o.numero) : '+', x, y, Math.max(10, r * (o.numero != null ? 1.15 : 1.45)), '#3b0a24', o.alpha ?? 1);
  };
  /** Le NEUTRON : bille grise ; o.numero écrit dessus quand on le compte. */
  P.neutron = (ctx, x, y, r = 9, o = {}) => {
    const L = Lx();
    if (L.neutron) L.neutron(ctx, x, y, { r, alpha: o.alpha ?? 1 }); else boule(ctx, x, y, r, COUL.neutron, o.alpha ?? 1);
    if (o.numero != null && r >= 6) inscrire(ctx, String(o.numero), x, y, Math.max(10, r * 1.15), '#111827', o.alpha ?? 1);
  };
  /** L'ÉLECTRON : petite bille bleu ciel « e− » (o.numero : son numéro écrit dessus). */
  P.electron = (ctx, x, y, r = 7, o = {}) => {
    const L = Lx();
    if (o.numero != null) {
      if (L.electron) L.electron(ctx, x, y, { r, texte: false, alpha: o.alpha ?? 1 }); else boule(ctx, x, y, r, COUL.electron, o.alpha ?? 1);
      inscrire(ctx, String(o.numero), x, y, Math.max(10, r * 1.2), '#06283d', o.alpha ?? 1); return;
    }
    if (L.electron) L.electron(ctx, x, y, { r, texte: o.texte, alpha: o.alpha ?? 1 }); else boule(ctx, x, y, r, COUL.electron, o.alpha ?? 1);
  };
  /** La particule ALPHA (chargée +) : petite bille orange qui brille. */
  P.alpha = (ctx, x, y, r = 5, a = 1) => {
    ctx.save(); ctx.globalAlpha *= a; ctx.shadowColor = 'rgba(251,146,60,.95)'; ctx.shadowBlur = 10; boule(ctx, x, y, r, COUL.alpha); ctx.restore();
  };
  /** Une boule chargée (prérequis) : rose « + » ou bleu ciel « − », signe écrit en grand. */
  P.charge = (ctx, x, y, r, signe, a = 1) => {
    P.ombre(ctx, () => boule(ctx, x, y, r, signe > 0 ? COUL.proton : COUL.electron, a), 8);
    inscrire(ctx, signe > 0 ? '+' : '−', x, y, r * 1.25, signe > 0 ? '#3b0a24' : '#06283d', a);
  };
  /** Une sphère pleine de Dalton (couleur c). */
  P.sphere = (ctx, x, y, r, c, a = 1) => P.ombre(ctx, () => boule(ctx, x, y, r, c, a), 6);

  /**
   * Positions des nucléons d'un noyau de Z protons et N neutrons : un amas serré (spirale de tournesol), protons et
   * neutrons mêlés de façon fixe. Renvoie [{x, y, t: 'p' | 'n', k}] (k : rang parmi les protons ou les neutrons, 1…).
   */
  function nucleons(cx, cy, Z, N, r) {
    const n = Z + N, out = [], ordre = [];
    let p = 0, q = 0;
    for (let i = 0; i < n; i++) {
      const prendP = q >= N || (p < Z && (p + .5) / Z <= (q + .5) / N);
      if (prendP) { ordre.push('p'); p++; } else { ordre.push('n'); q++; }
    }
    let kp = 0, kn = 0;
    for (let i = 0; i < n; i++) {
      const rr = n === 1 ? 0 : r * 1.9 * Math.sqrt(i + .35) * .55, a = i * 2.39996;
      const t = ordre[i]; out.push({ x: cx + rr * Math.cos(a), y: cy + rr * Math.sin(a), t, k: t === 'p' ? ++kp : ++kn });
    }
    return out;
  }
  P.nucleons = nucleons;
  /**
   * Le NOYAU : amas de Z protons (rose « + ») et N neutrons (gris), halo rose doux. o.r rayon d'une bille ;
   * o.numeros : { p: n1, n: n2 } — les n1 premiers protons et n2 premiers neutrons portent leur numéro et s'allument ;
   * o.pale : 'p' | 'n' (cette famille est pâlie). Renvoie { pos, R } (R : rayon de l'amas).
   */
  P.noyau = (ctx, cx, cy, Z, N, o = {}) => {
    const r = o.r ?? 9, pos = nucleons(cx, cy, Z, N, r), a = o.alpha ?? 1;
    const R = pos.reduce((m, q) => Math.max(m, Math.hypot(q.x - cx, q.y - cy)), 0) + r;
    ctx.save(); ctx.globalAlpha *= a;
    const g = ctx.createRadialGradient(cx, cy, R * .3, cx, cy, R * 1.6); g.addColorStop(0, 'rgba(244,114,182,.28)'); g.addColorStop(1, 'rgba(244,114,182,0)');
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(cx, cy, R * 1.6, 0, TAU); ctx.fill(); ctx.restore();
    const nums = o.numeros || {};
    [...pos].sort((u, v) => u.y - v.y).forEach(q => {
      const lit = q.t === 'p' ? q.k <= (nums.p || 0) : q.k <= (nums.n || 0);
      const al = a * (o.pale === q.t ? .22 : 1);
      if (lit && al > .3) P.halo(ctx, q.x, q.y, r * 1.3, q.k === (q.t === 'p' ? nums.p : nums.n));
      if (q.t === 'p') P.proton(ctx, q.x, q.y, r, { alpha: al, numero: lit ? q.k : null, texte: r >= 6 });
      else P.neutron(ctx, q.x, q.y, r, { alpha: al, numero: lit ? q.k : null });
    });
    return { pos, R };
  };
  /** Le NUAGE électronique : une brume bleu ciel, plus dense près du noyau (o.alpha, o.graine, o.points). */
  P.nuage = (ctx, cx, cy, R, o = {}) => {
    const r = graine(o.graine || 9), a = o.alpha ?? 1;
    ctx.save(); ctx.globalAlpha *= a;
    const g = ctx.createRadialGradient(cx, cy, 0, cx, cy, R); g.addColorStop(0, 'rgba(96,200,250,.32)'); g.addColorStop(.6, 'rgba(96,200,250,.13)'); g.addColorStop(1, 'rgba(96,200,250,0)');
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(cx, cy, R, 0, TAU); ctx.fill();
    ctx.fillStyle = 'rgba(165,225,255,.85)';
    const n = o.points ?? 260;
    for (let i = 0; i < n; i++) { const u = r(), d = R * Math.pow(u, .75) * .98, an = r() * TAU, rr = .9 + r() * 1.3; ctx.globalAlpha = a * (1 - d / R) * .9; ctx.beginPath(); ctx.arc(cx + d * Math.cos(an), cy + d * Math.sin(an), rr, 0, TAU); ctx.fill(); }
    ctx.restore();
  };
  /** Une COUCHE électronique (anneau lumineux fin) de rayon R ; o.alpha, o.vive (allumée). */
  P.couche = (ctx, cx, cy, R, o = {}) => {
    ctx.save(); ctx.globalAlpha *= o.alpha ?? 1;
    ctx.strokeStyle = o.vive ? 'rgba(250,204,21,.95)' : 'rgba(186,230,253,.6)'; ctx.lineWidth = o.vive ? 3 : 2;
    if (o.vive) { ctx.shadowColor = 'rgba(250,204,21,.8)'; ctx.shadowBlur = 12; }
    ctx.beginPath(); ctx.arc(cx, cy, R, 0, TAU); ctx.stroke(); ctx.restore();
  };
  /** Les places des électrons d'une couche de capacité `cap` (2 : en haut et en bas ; 8 : 4 paires aux points cardinaux). */
  P.places = (cx, cy, R, cap) => {
    const out = [];
    for (let i = 0; i < cap; i++) {
      let a;
      if (cap <= 2) a = -Math.PI / 2 + i * Math.PI;
      else { const paire = [0, 2, 1, 3][Math.floor(i / 2) % 4], cote = i % 2 ? 1 : -1; a = -Math.PI / 2 + paire * Math.PI / 2 + cote * Math.min(.32, 24 / R); }
      out.push({ x: cx + R * Math.cos(a), y: cy + R * Math.sin(a) });
    }
    return out;
  };
  /** Feuille d'or vue de profil (mince, dorée, reflets). */
  P.feuilleOr = (ctx, x, y, w, h, a = 1) => {
    ctx.save(); ctx.globalAlpha *= a;
    const g = ctx.createLinearGradient(x, y, x + w, y + h); g.addColorStop(0, '#fff2a8'); g.addColorStop(.35, '#eab308'); g.addColorStop(.7, '#a16207'); g.addColorStop(1, '#fde047');
    P.ombre(ctx, () => { ctx.fillStyle = g; ctx.fillRect(x, y, w, h); }, 6);
    ctx.fillStyle = 'rgba(255,255,255,.45)'; ctx.fillRect(x + w * .2, y + 4, Math.max(1, w * .2), h - 8);
    ctx.restore();
  };
  /** Boîte de plomb (source de particules α) : bloc gris sombre percé d'un trou ; le trou en (x + w, y + h/2). */
  P.boitePlomb = (ctx, x, y, w, h, a = 1) => {
    ctx.save(); ctx.globalAlpha *= a;
    const g = ctx.createLinearGradient(x, y, x, y + h); g.addColorStop(0, '#9ca3af'); g.addColorStop(.5, '#4b5563'); g.addColorStop(1, '#1f2937');
    P.ombre(ctx, () => { ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(x, y, w, h, 6); ctx.fill(); }, 8);
    ctx.fillStyle = '#0b0f14'; ctx.fillRect(x + w * .55, y + h / 2 - 5, w * .45, 10);
    const s = ctx.createRadialGradient(x + w * .45, y + h / 2, 1, x + w * .45, y + h / 2, 12); s.addColorStop(0, '#fde68a'); s.addColorStop(1, 'rgba(251,146,60,0)');
    ctx.fillStyle = s; ctx.beginPath(); ctx.arc(x + w * .45, y + h / 2, 12, 0, TAU); ctx.fill();
    ctx.restore();
  };
  /** Une flamme qui danse (t : temps) au-dessus de (x, y), hauteur h. */
  P.flamme = (ctx, x, y, h, t = 0, a = 1) => {
    ctx.save(); ctx.globalAlpha *= a;
    for (const [k, c0, c1] of [[1, 'rgba(249,115,22,.85)', 'rgba(220,38,38,0)'], [.62, 'rgba(253,224,71,.95)', 'rgba(249,115,22,0)'], [.3, 'rgba(255,255,240,.95)', 'rgba(253,224,71,0)']]) {
      const hh = h * k * (1 + .08 * Math.sin(t * 9 + k * 5)), ww = h * .42 * k;
      const g = ctx.createRadialGradient(x, y - hh * .3, 1, x, y - hh * .35, hh * .8); g.addColorStop(0, c0); g.addColorStop(1, c1);
      ctx.fillStyle = g; ctx.beginPath(); ctx.moveTo(x - ww, y); ctx.quadraticCurveTo(x - ww * 1.1, y - hh * .55, x + Math.sin(t * 7) * ww * .3, y - hh);
      ctx.quadraticCurveTo(x + ww * 1.1, y - hh * .55, x + ww, y); ctx.closePath(); ctx.fill();
    }
    ctx.restore();
  };
  /** Une bûche peinte (écorce, cernes au bout) ; o.brule : 0 → 1 (noircit), o.a : angle. */
  P.buche = (ctx, x, y, w, h, o = {}) => {
    ctx.save(); ctx.globalAlpha *= o.alpha ?? 1; ctx.translate(x, y); ctx.rotate(o.a || 0);
    const brule = o.brule || 0, g = ctx.createLinearGradient(0, -h / 2, 0, h / 2);
    const m = (c1, c2) => c1.map((v, i) => Math.round(v + (c2[i] - v) * brule));
    g.addColorStop(0, `rgb(${m([160, 110, 60], [60, 40, 30]).join(',')})`); g.addColorStop(.5, `rgb(${m([110, 70, 35], [35, 25, 20]).join(',')})`); g.addColorStop(1, `rgb(${m([70, 42, 20], [20, 15, 12]).join(',')})`);
    P.ombre(ctx, () => { ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(-w / 2, -h / 2, w, h, h / 2); ctx.fill(); }, 6);
    ctx.strokeStyle = 'rgba(40,25,10,.5)'; ctx.lineWidth = 1.4;
    for (let i = -3; i <= 3; i++) { ctx.beginPath(); ctx.moveTo(-w / 2 + h / 2, i * h / 8); ctx.lineTo(w / 2 - h / 2, i * h / 8 + 2); ctx.stroke(); }
    const ge = ctx.createRadialGradient(w / 2 - h * .45, 0, 1, w / 2 - h * .45, 0, h / 2); ge.addColorStop(0, '#e9c891'); ge.addColorStop(1, '#a0703c');
    ctx.fillStyle = ge; ctx.beginPath(); ctx.ellipse(w / 2 - h * .45, 0, h * .32, h / 2 - 1, 0, 0, TAU); ctx.fill();
    ctx.strokeStyle = 'rgba(110,70,35,.6)'; for (const k of [.12, .22]) { ctx.beginPath(); ctx.ellipse(w / 2 - h * .45, 0, h * k * 1.1, h * k * 1.6, 0, 0, TAU); ctx.stroke(); }
    ctx.restore();
  };
  /** Un panache de fumée grise (t : temps). */
  P.fumee = (ctx, x, y, h, t = 0, a = 1) => {
    ctx.save();
    for (let i = 0; i < 9; i++) {
      const u = ((t * .35 + i / 9) % 1), yy = y - u * h, xx = x + Math.sin(u * 6 + i) * 12 * u, r = 8 + u * 22;
      ctx.globalAlpha = a * (1 - u) * .6; const g = ctx.createRadialGradient(xx, yy, 1, xx, yy, r); g.addColorStop(0, 'rgba(203,213,225,.9)'); g.addColorStop(1, 'rgba(148,163,184,0)');
      ctx.fillStyle = g; ctx.beginPath(); ctx.arc(xx, yy, r, 0, TAU); ctx.fill();
    }
    ctx.restore();
  };
  /** Des gouttelettes de vapeur d'eau (bleues, montent). */
  P.vapeur = (ctx, x, y, h, t = 0, a = 1) => {
    ctx.save();
    for (let i = 0; i < 8; i++) {
      const u = ((t * .4 + i / 8) % 1), yy = y - u * h, xx = x + Math.sin(u * 5 + i * 2) * 10;
      ctx.globalAlpha = a * (1 - u) * .9; ctx.fillStyle = 'rgba(125,211,252,.95)'; ctx.beginPath(); ctx.moveTo(xx, yy - 7); ctx.quadraticCurveTo(xx + 5, yy, xx, yy + 4); ctx.quadraticCurveTo(xx - 5, yy, xx, yy - 7); ctx.fill();
    }
    ctx.restore();
  };
  /** Un tas de cendre grise. */
  P.cendre = (ctx, x, y, w, h, a = 1) => {
    ctx.save(); ctx.globalAlpha *= a; const r = graine(4);
    const g = ctx.createLinearGradient(0, y - h, 0, y); g.addColorStop(0, '#d4d4d8'); g.addColorStop(1, '#71717a');
    ctx.fillStyle = g; ctx.beginPath(); ctx.moveTo(x - w / 2, y); ctx.quadraticCurveTo(x, y - h * 2, x + w / 2, y); ctx.closePath(); ctx.fill();
    ctx.fillStyle = 'rgba(63,63,70,.6)'; for (let i = 0; i < 18; i++) { ctx.beginPath(); ctx.arc(x + (r() - .5) * w * .7, y - r() * h * .8, 1 + r() * 1.5, 0, TAU); ctx.fill(); }
    ctx.restore();
  };
  /** Le « pain aux raisins » de Thomson : boule de matière positive (rose pâle, pâte) ; les électrons sont posés par la page. */
  P.pain = (ctx, cx, cy, R, a = 1) => {
    ctx.save(); ctx.globalAlpha *= a; const r = graine(12);
    P.ombre(ctx, () => {
      const g = ctx.createRadialGradient(cx - R * .35, cy - R * .4, R * .1, cx, cy, R); g.addColorStop(0, '#fde2ec'); g.addColorStop(.55, '#f0a6c4'); g.addColorStop(1, '#9d4a6d');
      ctx.fillStyle = g; ctx.beginPath(); ctx.arc(cx, cy, R, 0, TAU); ctx.fill();
    }, 12);
    ctx.fillStyle = 'rgba(255,255,255,.18)'; for (let i = 0; i < 40; i++) { const d = R * Math.sqrt(r()) * .9, an = r() * TAU; ctx.beginPath(); ctx.arc(cx + d * Math.cos(an), cy + d * Math.sin(an), 1.5 + r() * 2.5, 0, TAU); ctx.fill(); }
    ctx.restore();
  };
  /** Une balance à fléau peinte, centrée en cx, socle en yBas ; angle du fléau (rad, + : plateau droit plus bas). Renvoie les plateaux. */
  P.balance = (ctx, cx, yBas, w, angle = 0, a = 1) => {
    ctx.save(); ctx.globalAlpha *= a;
    const hp = w * .55, yP = yBas - hp, met = (x0, y0, x1, y1) => { const g = ctx.createLinearGradient(x0, y0, x1, y1); g.addColorStop(0, '#e5e7eb'); g.addColorStop(.5, '#9ca3af'); g.addColorStop(1, '#4b5563'); return g; };
    P.ombre(ctx, () => { ctx.fillStyle = met(cx - w * .2, yBas, cx + w * .2, yBas); ctx.beginPath(); ctx.roundRect(cx - w * .2, yBas - 12, w * .4, 12, 4); ctx.fill(); });
    ctx.fillStyle = met(cx - 6, 0, cx + 6, 0); ctx.fillRect(cx - 5, yP, 10, hp - 12);
    const dx = Math.cos(angle) * w / 2, dy = Math.sin(angle) * w / 2, g = { x: cx - dx, y: yP - dy }, d = { x: cx + dx, y: yP + dy };
    ctx.strokeStyle = '#d1d5db'; ctx.lineWidth = 6; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(g.x, g.y); ctx.lineTo(d.x, d.y); ctx.stroke();
    boule(ctx, cx, yP, 8, [234, 179, 8]);
    const plateaux = [];
    for (const p of [g, d]) {
      ctx.strokeStyle = 'rgba(209,213,219,.8)'; ctx.lineWidth = 1.4; const py = p.y + w * .28;
      ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(p.x - w * .16, py); ctx.moveTo(p.x, p.y); ctx.lineTo(p.x + w * .16, py); ctx.stroke();
      P.ombre(ctx, () => { ctx.fillStyle = met(p.x - w * .18, py, p.x + w * .18, py); ctx.beginPath(); ctx.ellipse(p.x, py, w * .19, 6, 0, 0, TAU); ctx.fill(); });
      plateaux.push({ x: p.x, y: py - 4 });
    }
    ctx.restore();
    return { gauche: plateaux[0], droite: plateaux[1], pivot: { x: cx, y: yP } };
  };
  /** Un stade vu de dessus (tribunes, piste, pelouse rayée), dans le rectangle (x, y, w, h). */
  P.stade = (ctx, x, y, w, h, a = 1) => {
    ctx.save(); ctx.globalAlpha *= a; const cx = x + w / 2, cy = y + h / 2;
    const ov = (k, f) => { ctx.fillStyle = f; ctx.beginPath(); ctx.ellipse(cx, cy, w / 2 * k, h / 2 * k, 0, 0, TAU); ctx.fill(); };
    P.ombre(ctx, () => ov(1, '#64748b'), 10);
    const gt = ctx.createRadialGradient(cx, cy, h * .2, cx, cy, w / 2); gt.addColorStop(0, '#94a3b8'); gt.addColorStop(1, '#475569'); ov(.98, gt);
    for (let i = 0; i < 4; i++) { ctx.strokeStyle = 'rgba(30,41,59,.35)'; ctx.lineWidth = 1; ctx.beginPath(); ctx.ellipse(cx, cy, w / 2 * (.8 + i * .05), h / 2 * (.8 + i * .05), 0, 0, TAU); ctx.stroke(); }
    ov(.78, '#b45309'); ov(.72, '#15803d');
    ctx.save(); ctx.beginPath(); ctx.ellipse(cx, cy, w / 2 * .72, h / 2 * .72, 0, 0, TAU); ctx.clip();
    for (let i = -6; i < 6; i++) { if (i % 2) { ctx.fillStyle = 'rgba(134,239,172,.18)'; ctx.fillRect(cx + i * w * .06, y, w * .06, h); } }
    ctx.strokeStyle = 'rgba(255,255,255,.75)'; ctx.lineWidth = 1.5; ctx.strokeRect(cx - w * .3, cy - h * .25, w * .6, h * .5); ctx.beginPath(); ctx.moveTo(cx, cy - h * .25); ctx.lineTo(cx, cy + h * .25); ctx.stroke();
    ctx.beginPath(); ctx.arc(cx, cy, h * .1, 0, TAU); ctx.stroke(); ctx.restore();
    ctx.restore();
  };
  /** Allumer une bille : halo jaune doux autour de (x, y), rayon r ; vive : la dernière allumée, plus brillante. */
  P.halo = (ctx, x, y, r, vive = false) => { ctx.save(); ctx.shadowColor = 'rgba(250,204,21,.95)'; ctx.shadowBlur = vive ? 18 : 10; ctx.fillStyle = `rgba(250,204,21,${vive ? .45 : .28})`; ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.fill(); ctx.restore(); };

  /**
   * L'écriture ᴬ_Z X à la craie : X en grand à (x, y) (ligne de base), A en haut à gauche, Z en bas à gauche, la charge
   * d'un ion en haut à droite. o : taille, couleurs {A, Z, X, q}, q (« + », « 2− »…). Renvoie { x0, x1 } (bords écrits).
   */
  function notation(c, A, Z, X, x, y, o = {}) {
    const t = o.taille || 40, k = o.couleurs || {}, ti = t * .55;
    const wA = A === '' || A == null ? 0 : c.largeurTexte(String(A), ti), wZ = Z === '' || Z == null ? 0 : c.largeurTexte(String(Z), ti);
    if (wA) c.texte(String(A), x - 3, y - t * .5, { couleur: k.A || 'jaune', taille: ti, align: 'right' });
    if (wZ) c.texte(String(Z), x - 3, y + ti * .3, { couleur: k.Z || 'rose', taille: ti, align: 'right' });
    c.texte(X, x, y, { couleur: k.X || 'blanc', taille: t, gras: true });
    const wX = c.largeurTexte(X, t) * 1.05;
    if (o.q) c.texte(o.q, x + wX + 2, y - t * .5, { couleur: k.q || 'jaune', taille: ti });
    return { x0: x - 3 - Math.max(wA, wZ), x1: x + wX + (o.q ? c.largeurTexte(o.q, ti) + 2 : 0) };
  }

  /** Les atomes du cours (Z ≤ 18) : symbole, nom. */
  const ELEMENTS = { 1: ['H', 'hydrogène'], 2: ['He', 'hélium'], 3: ['Li', 'lithium'], 6: ['C', 'carbone'], 7: ['N', 'azote'], 8: ['O', 'oxygène'], 10: ['Ne', 'néon'], 11: ['Na', 'sodium'], 12: ['Mg', 'magnésium'], 13: ['Al', 'aluminium'], 16: ['S', 'soufre'], 17: ['Cl', 'chlore'], 18: ['Ar', 'argon'] };
  /** La répartition de n électrons (Z ≤ 18) : [K, L, M] (couches vides à la fin retirées). */
  function repartition(n) { const k = Math.min(2, n), l = Math.max(0, Math.min(8, n - 2)), m = Math.max(0, n - 10); return [k, l, m].filter((v, i) => v > 0 || i === 0); }
  const EXP = { 0: '⁰', 1: '¹', 2: '²', 3: '³', 4: '⁴', 5: '⁵', 6: '⁶', 7: '⁷', 8: '⁸', 9: '⁹' };
  const exposant = n => String(n).split('').map(ch => EXP[ch] || ch).join('');
  /** « (K)²(L)⁶ » en exposants Unicode. */
  function structure(n) { return repartition(n).map((v, i) => `(${'KLM'[i]})${exposant(v)}`).join(''); }


  /* ── Ajouts (session cloud, 25/11/2026) : l'atome entier, le comptage, le tableau de méthode ── */
  /**
   * Places FIXES de n électrons dans le nuage de rayon R autour de (cx, cy), entre .42·R et .88·R ; t (s) les fait
   * tourner lentement (le nuage vit). Toujours les mêmes places pour un même (n, graine) : un électron compté garde sa place.
   */
  P.placesNuage = (cx, cy, R, n, o = {}) => {
    const r = graine(o.graine || 21), out = [], t = o.t || 0;
    for (let i = 0; i < n; i++) {
      const a0 = i / Math.max(1, n) * TAU + (r() - .5) * .5, d = R * (.42 + .46 * r()), w = (.18 + .1 * r()) * (i % 2 ? 1 : -1);
      out.push({ x: cx + d * Math.cos(a0 + w * t), y: cy + d * Math.sin(a0 + w * t) * .92 });
    }
    return out;
  };
  /**
   * L'ATOME entier : nuage bleu ciel, noyau (Z protons, N neutrons) au centre, n électrons (défaut Z) dans le nuage.
   * o : R (nuage), rn (bille du noyau), re (électron), t (rotation), ne (nombre d'électrons), litE (k premiers
   * électrons allumés et numérotés), numeros / pale (noyau), alphaE. Renvoie { noyau, elec }.
   */
  P.atome = (ctx, cx, cy, Z, N, o = {}) => {
    const R = o.R || 120, n = o.ne ?? Z;
    P.nuage(ctx, cx, cy, R, { points: o.points ?? Math.round(R * 1.3), graine: o.graine || 9, alpha: o.alphaNuage ?? 1 });
    const noyau = P.noyau(ctx, cx, cy, Z, N, { r: o.rn ?? 4, numeros: o.numeros, pale: o.pale, alpha: o.alphaNoyau ?? 1 });
    const elec = P.placesNuage(cx, cy, R, n, { t: o.t || 0, graine: o.graineE || 21 });
    const lit = o.litE || 0;
    elec.forEach((q, i) => {
      if (i < lit) P.halo(ctx, q.x, q.y, (o.re || 8) * 1.5, i === lit - 1);
      P.electron(ctx, q.x, q.y, o.re || 8, { numero: i < lit ? i + 1 : null, alpha: o.alphaE ?? 1 });
    });
    return { noyau, elec };
  };
  /**
   * Un noyau qu'on COMPTE : mode 'tous' (nucléons, dans l'ordre des places), 'p' (protons), 'n' (neutrons) ; k = nombre
   * déjà allumé (chacun garde son numéro et sa lueur, le dernier plus vif) ; la famille non comptée est pâlie si o.palir.
   */
  P.noyauCompte = (ctx, cx, cy, Z, N, r, mode, k, o = {}) => {
    const pos = nucleons(cx, cy, Z, N, r), a = o.alpha ?? 1;
    const R = pos.reduce((m, q) => Math.max(m, Math.hypot(q.x - cx, q.y - cy)), 0) + r;
    ctx.save(); ctx.globalAlpha *= a;
    const g = ctx.createRadialGradient(cx, cy, R * .3, cx, cy, R * 1.6); g.addColorStop(0, 'rgba(244,114,182,.28)'); g.addColorStop(1, 'rgba(244,114,182,0)');
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(cx, cy, R * 1.6, 0, TAU); ctx.fill(); ctx.restore();
    const rang = q => mode === 'tous' ? pos.indexOf(q) + 1 : (q.t === mode ? q.k : 0);
    [...pos].sort((u, v) => u.y - v.y).forEach(q => {
      const n = rang(q), lit = n > 0 && n <= k, al = a * (o.palir && mode !== 'tous' && q.t !== mode ? .25 : 1);
      if (lit) P.halo(ctx, q.x, q.y, r * 1.35, n === Math.floor(k));
      if (q.t === 'p') P.proton(ctx, q.x, q.y, r, { alpha: al, numero: lit ? n : null });
      else P.neutron(ctx, q.x, q.y, r, { alpha: al, numero: lit ? n : null });
    });
    return { pos, R };
  };
  /** Comptage : nombre allumé à l'instant, n éléments comptés pendant les d secondes qui MÈNENT au moment `nom`. */
  const compte = (S, M, nom, n, d) => (S.t <= 0 || S.t >= M[nom] ? n : Math.max(0, Math.min(n, Math.floor((S.t - (M[nom] - d)) / d * n + 1e-6))));
  /** Durée d'un comptage de n éléments (assez lente pour que l'œil suive, jamais plus de 6 s). */
  const dureeCompte = n => Math.min(6, .5 + n * .32);
  /** Un nombre qui vole de (x0, y0) à (x1, y1) pendant les .8 s qui MÈNENT au moment `nom` : à l'arrêt sur ce moment, il est
   *  posé dans sa case (et y reste). Renvoie true quand il est arrivé. */
  function vole(c, S, nom, txt, x0, y0, x1, y1, o = {}) {
    const m = S.momentDe ? S.momentDe(nom) : null;
    const u = S.t <= 0 || S.a(nom) ? 1 : (m == null ? 0 : Math.max(0, Math.min(1, (S.t - (m - .8)) / .8)));
    if (u <= 0) return false;
    const st = Object.assign({ couleur: 'jaune', taille: 22, align: 'center', gras: true }, o);
    if (u < 1) { c.direct(() => c.texte(txt, x0 + (x1 - x0) * A_doux(u), y0 + (y1 - y0) * A_doux(u), Object.assign({}, st, { duree: .01 }))); S.scene.sale = true; return false; }
    c.direct(() => c.texte(txt, x1, y1, Object.assign({}, st, { duree: .01 })));
    return true;
  }
  const A_doux = u => (u <= 0 ? 0 : u >= 1 ? 1 : u * u * (3 - 2 * u));
  /** Progression 0..1 pendant les d secondes qui MÈNENT au moment `nom` (ce que la voix nomme est fini à l'arrêt). */
  const avant = (S, nom, d = 1) => { if (S.t <= 0) return 1; const m = S.momentDe(nom); return m == null ? 0 : Math.max(0, Math.min(1, (S.t - (m - d)) / d)); };

  window.Atome = { compte, dureeCompte, vole, avant, Scene, VW, VH, TAU, lueur, lignes, sim, param, doux, graine, P, boule, notation, ELEMENTS, repartition, structure, exposant, COUL };
})();
