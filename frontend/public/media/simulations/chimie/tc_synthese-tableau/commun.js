/*
 * Commun aux simulations du cours « Synthèse d'une espèce chimique » (Tronc Commun Sciences, option française,
 * chimie, novembre 2026). Même moteur que le cours de TC SVT « La sortie écologique » (svt/tc_sortie_ecologique-tableau).
 *
 *  - Synthese.Scene  : cadre virtuel 760 × 420 en mode large (scene.L de 760 à 1596, hauteur 420), texte jamais sous
 *                      15 px à l'écran ; dans le petit cadre du téléphone en paysage (scene.petit), l'étape en cours seule.
 *  - Synthese.sim(o) : simulation « à moments » (Lancer → Pause → Reprendre → Rejouer ; start / pause / resume / reset /
 *                      play_until {moment | time_s} / set_time / set_parameters {conclusions, …} ; `ce_qui_se_voit`).
 *  - Synthese.P      : les objets du cours peints en couleur, UN SEUL DESSIN par objet dans toutes les diapos :
 *                      ballon (celui de chem-lab.js, 2ᵉ Bac), réfrigérant à boules (entrée de l'eau en bas, sortie en
 *                      haut, à droite), potence, chauffe-ballon, support élévateur, tuyaux, pierre ponce, flacons
 *                      (huile, éthanol, soude avec pictogramme corrosif), éprouvette graduée, bécher (lexique commun),
 *                      entonnoir et papier filtre, flocons et pain de savon, plaque de CCM, cuve et couvercle,
 *                      capillaire, lampe UV, thermomètre, balance, lunettes, gant, jasmin, parfum, usine, bouteille en
 *                      plastique, peinture, médicaments, verre d'eau, molécule d'eau (O rouge, H blancs), ions, tube.
 *                      Couleurs des liquides : P.LIQ (huile dorée, éthanol et soude incolores, mélange jaune pâle…).
 *  - Synthese.lueur  : allumer en comptant (halo jaune doux, numéro écrit proprement à côté).
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
      g.fillStyle = `rgba(${couleur}, ${vive ? 0.07 : 0.04})`; arrondi(g, x, y, w, h, 8); g.fill(); g.restore();
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


  /* ── Les objets du cours, peints (un objet, un seul dessin dans toutes les diapos) ─────────────────────────── */
  function graine(seed) { let s = (seed >>> 0) || 1; return () => { s = (Math.imul(s, 1664525) + 1013904223) >>> 0; return s / 4294967296; }; }
  const P = {};
  const rgba = ([r, g, b, a = 1], k = 1) => `rgba(${Math.round(r)},${Math.round(g)},${Math.round(b)},${Math.max(0, Math.min(1, a * k)).toFixed(3)})`;
  const clair = (c, k) => [c[0] + (255 - c[0]) * k, c[1] + (255 - c[1]) * k, c[2] + (255 - c[2]) * k, c[3] ?? 1];
  const fonce = (c, k) => [c[0] * (1 - k), c[1] * (1 - k), c[2] * (1 - k), c[3] ?? 1];
  P.rgba = rgba; P.clair = clair; P.fonce = fonce;
  /** Les couleurs des liquides du cours (toujours les mêmes) : huile dorée, éthanol et soude incolores (eau un peu
   *  bleutée), mélange réactionnel jaune pâle, eau salée, éluant, eau du réfrigérant. */
  P.LIQ = {
    huile: [234, 179, 8, .72], ethanol: [186, 230, 253, .34], soude: [167, 214, 248, .40], melange: [250, 224, 140, .60],
    savonneux: [254, 243, 199, .70], salee: [147, 197, 253, .42], eau: [96, 165, 250, .45], eluant: [191, 219, 254, .45],
    produit: [253, 224, 71, .55], acide: [220, 252, 231, .40], alcool: [224, 231, 255, .40],
  };
  P.ombre = (ctx, fn, b = 6) => { ctx.save(); ctx.shadowColor = 'rgba(0,0,0,.35)'; ctx.shadowBlur = b; ctx.shadowOffsetX = 2; ctx.shadowOffsetY = 2; fn(); ctx.restore(); };
  function boule(ctx, x, y, r, c0, c1, c2) {
    const g = ctx.createRadialGradient(x - r * .35, y - r * .4, r * .1, x, y, r);
    g.addColorStop(0, c0); g.addColorStop(.55, c1); g.addColorStop(1, c2);
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.fill();
  }
  /** Une sphère colorée (entité d'une espèce : bille d'une molécule), col = [r, g, b]. */
  P.sphere = (ctx, x, y, r, col, a = 1) => {
    ctx.save(); ctx.globalAlpha *= a;
    ctx.fillStyle = 'rgba(0,0,0,.22)'; ctx.beginPath(); ctx.arc(x + r * .2, y + r * .3, r, 0, TAU); ctx.fill();
    const g = ctx.createRadialGradient(x - r * .38, y - r * .42, r * .08, x, y, r);
    g.addColorStop(0, rgba(clair(col, .8))); g.addColorStop(.3, rgba(clair(col, .22))); g.addColorStop(.72, rgba(col)); g.addColorStop(1, rgba(fonce(col, .42)));
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.fill(); ctx.restore();
  };
  /** Texte écrit SUR un objet peint (étiquette) : foncé et gras sur un objet clair. */
  P.ecrit = (ctx, s, x, y, taille = 14, couleur = '#0b1f2a', align = 'center') => {
    ctx.save(); ctx.font = `700 ${taille}px ${window.Tableau.POLICE}`; ctx.fillStyle = couleur; ctx.textAlign = align; ctx.textBaseline = 'middle';
    ctx.fillText(s, x, y); ctx.restore();
  };
  function liquide(ctx, forme, x0, x1, ys, yb, col, menisque = true) {
    ctx.save(); forme(); ctx.clip();
    const g = ctx.createLinearGradient(x0, 0, x1, 0);
    g.addColorStop(0, rgba(fonce(col, .5), 1.35)); g.addColorStop(.42, rgba(clair(col, .2))); g.addColorStop(1, rgba(fonce(col, .5), 1.35));
    ctx.fillStyle = g; ctx.fillRect(x0 - 2, ys, x1 - x0 + 4, yb - ys + 2);
    ctx.restore();
    if (menisque) { ctx.fillStyle = rgba(clair(col, .45), 1.2); ctx.beginPath(); ctx.ellipse((x0 + x1) / 2, ys, Math.max(1, (x1 - x0) / 2 - 1), 2.6, 0, 0, TAU); ctx.fill(); }
  }
  P.liquide = liquide;

  /**
   * Le ballon (fond rond) : même dessin que le ballon réactionnel de la chimie de 2ᵉ Bac (chimie/shared/chem-lab.js) —
   * verre net, reflet en arc, col droit. (x, y) = centre de la panse, r = rayon.
   * o.couches = [{ f, col }] du bas vers le haut (f = fraction de la hauteur de la panse), o.ponce = grains au fond,
   * o.bulles = phase (s) de l'ébullition, o.agite (0..1) = force de l'ébullition, o.flocons.
   * Renvoie { haut } : le haut du col (où se pose le réfrigérant).
   */
  P.ballon = (ctx, x, y, r, o = {}) => {
    const lc = r * .3, th = Math.asin(lc / r), yN = y - r * Math.cos(th), haut = y - r * 1.75;
    const forme = () => { ctx.beginPath(); ctx.moveTo(x - lc, haut); ctx.lineTo(x - lc, yN); ctx.arc(x, y, r, -Math.PI / 2 - th, -Math.PI / 2 + th - TAU, true); ctx.lineTo(x + lc, haut); };
    const panse = () => { ctx.beginPath(); ctx.arc(x, y, r - 1.5, 0, TAU); };
    ctx.save();
    ctx.fillStyle = 'rgba(0,0,0,.25)'; ctx.beginPath(); ctx.ellipse(x + 3, y + r + 3, r * .55, 4, 0, 0, TAU); ctx.fill();
    forme(); ctx.fillStyle = 'rgba(190,220,240,.09)'; ctx.fill();
    let bas = y + r;
    (o.couches || []).forEach((cc, i) => {
      const ys = y + r - 2 * r * Math.min(1, cc.f);
      liquide(ctx, panse, x - r, x + r, ys, bas, cc.col, i === (o.couches.length - 1));
      bas = ys;
    });
    const niv = (o.couches || []).length ? y + r - 2 * r * Math.min(1, o.couches[o.couches.length - 1].f) : y + r;
    if (o.ponce) { const R = graine(9); for (let i = 0; i < 5; i++) P.ponce(ctx, x - r * .35 + i * r * .17, y + r - 7 - R() * 3, 4 + R() * 1.6); }
    if (o.bulles != null && o.couches && o.couches.length) {
      const n = Math.round(4 + 10 * (o.agite ?? .6));
      ctx.save(); panse(); ctx.clip();
      for (let i = 0; i < n; i++) {
        const f = ((o.bulles * (0.5 + (o.agite ?? .6)) * .9) + i * .137) % 1, br = 1.6 + (i % 3) * (o.agite ?? .6) * 1.3;
        const bx = x - r * .55 + r * 1.1 * ((i * 37 % 100) / 100) + Math.sin(f * 9 + i) * 2, by = y + r - 6 - f * (y + r - 6 - niv);
        ctx.globalAlpha = Math.min(1, (1 - f) * 3) * .85; ctx.strokeStyle = 'rgba(255,255,255,.85)'; ctx.lineWidth = 1;
        ctx.beginPath(); ctx.arc(bx, by, br, 0, TAU); ctx.stroke();
      }
      ctx.restore();
    }
    if (o.flocons) P.flocons(ctx, x - r * .6, niv - 4, r * 1.2, 12, 14, o.flocons);
    ctx.strokeStyle = 'rgba(225,240,252,.88)'; ctx.lineWidth = 2; ctx.lineJoin = 'round'; forme(); ctx.stroke();
    ctx.strokeStyle = 'rgba(255,255,255,.4)'; ctx.lineWidth = 3.5; ctx.lineCap = 'round'; ctx.beginPath(); ctx.arc(x, y, r * .76, Math.PI * 1.08, Math.PI * 1.4); ctx.stroke();
    ctx.lineWidth = 1.4; ctx.beginPath(); ctx.moveTo(x - lc + 2.5, haut + 4); ctx.lineTo(x - lc + 2.5, yN - 4); ctx.stroke();
    ctx.strokeStyle = 'rgba(240,248,255,.9)'; ctx.lineWidth = 2; ctx.beginPath(); ctx.ellipse(x, haut, lc + 2, 2.2, 0, 0, TAU); ctx.stroke();
    ctx.restore();
    return { haut, niveau: niv, lc };
  };
  /** Un grain de pierre ponce : petit caillou gris clair, poreux. */
  P.ponce = (ctx, x, y, r) => {
    ctx.save();
    const g = ctx.createRadialGradient(x - r * .3, y - r * .3, r * .1, x, y, r); g.addColorStop(0, '#f1f5f9'); g.addColorStop(.6, '#b6bcc4'); g.addColorStop(1, '#7c8591');
    ctx.fillStyle = g; ctx.beginPath(); ctx.ellipse(x, y, r, r * .75, .4, 0, TAU); ctx.fill();
    ctx.fillStyle = 'rgba(71,85,105,.6)'; for (let i = 0; i < 3; i++) { ctx.beginPath(); ctx.arc(x - r * .3 + i * r * .3, y + (i % 2 ? -1 : 1) * r * .2, r * .14, 0, TAU); ctx.fill(); }
    ctx.restore();
  };
  /**
   * Le réfrigérant à boules (vertical) : manchon de verre (eau froide bleue quand o.eau), tube intérieur à boules,
   * deux tubulures sur la droite : entrée de l'eau en BAS, sortie en HAUT. o.phase fait couler l'eau (flèches claires).
   * Renvoie { entree: [x, y], sortie: [x, y], bas, haut, w }.
   */
  P.refrigerant = (ctx, x, yHaut, yBas, o = {}) => {
    const w = o.w || 30, h = yBas - yHaut, nb = o.boules || 5, ye = yBas - 22, ysor = yHaut + 22;
    ctx.save();
    // tubulures
    const tub = (yy) => { ctx.fillStyle = 'rgba(190,220,240,.16)'; ctx.fillRect(x + w / 2 - 1, yy - 5, 18, 10); ctx.strokeStyle = 'rgba(225,240,252,.85)'; ctx.lineWidth = 1.5; ctx.strokeRect(x + w / 2 - 1, yy - 5, 18, 10); };
    tub(ye); tub(ysor);
    // manchon
    ctx.fillStyle = 'rgba(190,220,240,.10)'; ctx.beginPath(); ctx.roundRect(x - w / 2, yHaut + 8, w, h - 16, 8); ctx.fill();
    if (o.eau) {
      const ge = ctx.createLinearGradient(x - w / 2, 0, x + w / 2, 0); ge.addColorStop(0, 'rgba(37,99,235,.55)'); ge.addColorStop(.45, 'rgba(147,197,253,.42)'); ge.addColorStop(1, 'rgba(37,99,235,.55)');
      const hEau = (h - 20) * Math.min(1, o.eau);
      ctx.fillStyle = ge; ctx.beginPath(); ctx.roundRect(x - w / 2 + 2, yBas - 10 - hEau, w - 4, hEau, 6); ctx.fill();
      if (o.phase != null && o.eau >= 1) {
        ctx.strokeStyle = 'rgba(219,234,254,.55)'; ctx.lineWidth = 1.2;
        for (let i = 0; i < 6; i++) { const f = ((o.phase * .35) + i / 6) % 1, yy = yBas - 14 - f * (h - 30), xx = x + (i % 2 ? w * .3 : -w * .3); ctx.beginPath(); ctx.moveTo(xx - 3, yy + 4); ctx.lineTo(xx, yy); ctx.lineTo(xx + 3, yy + 4); ctx.stroke(); }
      }
    }
    // tube intérieur à boules
    const pas = (h - 40) / nb, rb = Math.min(w * .34, pas * .42);
    ctx.fillStyle = 'rgba(225,240,252,.18)'; ctx.strokeStyle = 'rgba(225,240,252,.85)'; ctx.lineWidth = 1.3;
    ctx.fillRect(x - 3, yHaut, 6, h + 14); ctx.strokeRect(x - 3, yHaut, 6, h + 14);
    for (let i = 0; i < nb; i++) { const yy = yHaut + 20 + pas * (i + .5); ctx.beginPath(); ctx.ellipse(x, yy, rb, rb * 1.05, 0, 0, TAU); ctx.fillStyle = 'rgba(225,240,252,.22)'; ctx.fill(); ctx.stroke(); }
    ctx.strokeStyle = 'rgba(225,240,252,.9)'; ctx.lineWidth = 1.9; ctx.beginPath(); ctx.roundRect(x - w / 2, yHaut + 8, w, h - 16, 8); ctx.stroke();
    ctx.strokeStyle = 'rgba(255,255,255,.35)'; ctx.lineWidth = 2.5; ctx.beginPath(); ctx.moveTo(x - w / 2 + 4, yHaut + 16); ctx.lineTo(x - w / 2 + 4, yBas - 16); ctx.stroke();
    ctx.restore();
    return { entree: [x + w / 2 + 17, ye], sortie: [x + w / 2 + 17, ysor], bas: yBas + 14, haut: yHaut, w, boules: Array.from({ length: nb }, (_, i) => yHaut + 20 + pas * (i + .5)), rb };
  };
  /** Un tuyau souple (caoutchouc) passant par pts ; o.eau : l'eau qui y coule (bleu). */
  P.tuyau = (ctx, pts, o = {}) => {
    ctx.save(); ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    const trace = () => { ctx.beginPath(); pts.forEach(([px, py], i) => (i ? ctx.lineTo(px, py) : ctx.moveTo(px, py))); ctx.stroke(); };
    ctx.strokeStyle = '#7f1d1d'; ctx.lineWidth = 8; trace();
    ctx.strokeStyle = o.eau ? '#3b82f6' : '#b45309'; ctx.lineWidth = 5; trace();
    ctx.strokeStyle = 'rgba(255,255,255,.25)'; ctx.lineWidth = 1.4; trace();
    ctx.restore();
  };
  /** La potence : socle lourd, tige métallique ; o.pinces = [{ y, x2, ouverture }] noix + pince qui tient la verrerie en x2. */
  P.potence = (ctx, x, yBase, h, o = {}) => {
    ctx.save();
    P.ombre(ctx, () => { const g = ctx.createLinearGradient(0, yBase - 12, 0, yBase); g.addColorStop(0, '#64748b'); g.addColorStop(1, '#1e293b'); ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(x - 26, yBase - 12, o.socle || 120, 12, 3); ctx.fill(); }, 5);
    const gt = ctx.createLinearGradient(x - 4, 0, x + 4, 0); gt.addColorStop(0, '#94a3b8'); gt.addColorStop(.5, '#f1f5f9'); gt.addColorStop(1, '#64748b');
    ctx.fillStyle = gt; ctx.fillRect(x - 3.5, yBase - 12 - h, 7, h);
    for (const p of (o.pinces || [])) {
      const xa = Math.min(x, p.x2), xb = Math.max(x, p.x2);
      ctx.fillStyle = '#475569'; ctx.fillRect(x - 8, p.y - 7, 16, 14);           // noix
      const gb = ctx.createLinearGradient(0, p.y - 3, 0, p.y + 3); gb.addColorStop(0, '#cbd5e1'); gb.addColorStop(1, '#64748b');
      ctx.fillStyle = gb; ctx.fillRect(xa, p.y - 2.5, xb - xa - (p.ouverture || 12), 5);
      ctx.strokeStyle = '#334155'; ctx.lineWidth = 3; ctx.lineCap = 'round';
      const xp = p.x2, op = p.ouverture || 12; ctx.beginPath(); ctx.moveTo(xp - op - 2, p.y - 2); ctx.quadraticCurveTo(xp - op * .2, p.y - 12, xp + op, p.y - 7); ctx.moveTo(xp - op - 2, p.y + 2); ctx.quadraticCurveTo(xp - op * .2, p.y + 12, xp + op, p.y + 7); ctx.stroke();
    }
    ctx.restore();
  };
  /** Le chauffe-ballon : coque sombre, cuvette qui rougeoie quand il chauffe, bouton et voyant. */
  P.chauffeBallon = (ctx, x, y, w, h, chaud = 0) => {
    ctx.save();
    P.ombre(ctx, () => { const g = ctx.createLinearGradient(0, y, 0, y + h); g.addColorStop(0, '#4b5563'); g.addColorStop(1, '#111827'); ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(x - w / 2, y, w, h, 9); ctx.fill(); }, 8);
    const gl = ctx.createRadialGradient(x, y + 4, 4, x, y + 4, w * .5); gl.addColorStop(0, `rgba(251,146,60,${.25 + .6 * chaud})`); gl.addColorStop(1, 'rgba(251,146,60,0)');
    ctx.fillStyle = gl; ctx.beginPath(); ctx.ellipse(x, y + 6, w * .46, h * .32, 0, 0, TAU); ctx.fill();
    ctx.fillStyle = '#1f2937'; ctx.beginPath(); ctx.arc(x + w * .32, y + h * .62, 6, 0, TAU); ctx.fill(); ctx.strokeStyle = '#9ca3af'; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.moveTo(x + w * .32, y + h * .62); ctx.lineTo(x + w * .32 + 4, y + h * .62 - 4); ctx.stroke();
    ctx.fillStyle = chaud > .1 ? '#ef4444' : '#7f1d1d'; ctx.beginPath(); ctx.arc(x - w * .32, y + h * .62, 3.5, 0, TAU); ctx.fill();
    ctx.restore();
  };
  /** Le support élévateur (ciseaux) : plateau, croisillons, socle. */
  P.elevateur = (ctx, x, y, w, h) => {
    ctx.save();
    const met = (yy, hh) => { const g = ctx.createLinearGradient(0, yy, 0, yy + hh); g.addColorStop(0, '#e2e8f0'); g.addColorStop(1, '#64748b'); ctx.fillStyle = g; ctx.fillRect(x - w / 2, yy, w, hh); };
    met(y, 6); met(y + h - 6, 6);
    ctx.strokeStyle = '#94a3b8'; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(x - w * .4, y + 6); ctx.lineTo(x + w * .4, y + h - 6); ctx.moveTo(x + w * .4, y + 6); ctx.lineTo(x - w * .4, y + h - 6); ctx.stroke();
    ctx.fillStyle = '#475569'; ctx.beginPath(); ctx.arc(x, y + h / 2, 3.5, 0, TAU); ctx.fill();
    ctx.restore();
  };
  /** Une goutte (liquide condensé qui retombe). */
  P.goutte = (ctx, x, y, s, col = [147, 197, 253, .9]) => {
    ctx.save(); ctx.fillStyle = rgba(col); ctx.beginPath(); ctx.moveTo(x, y - s * 1.6); ctx.quadraticCurveTo(x + s, y - s * .2, x, y + s * .6); ctx.quadraticCurveTo(x - s, y - s * .2, x, y - s * 1.6); ctx.fill();
    ctx.fillStyle = 'rgba(255,255,255,.7)'; ctx.beginPath(); ctx.arc(x - s * .25, y - s * .2, s * .22, 0, TAU); ctx.fill(); ctx.restore();
  };
  /** Une volute de vapeur (blanche, légère). */
  P.vapeur = (ctx, x, y, s, a = .5) => {
    ctx.save(); const g = ctx.createRadialGradient(x, y, 1, x, y, s); g.addColorStop(0, `rgba(241,245,249,${a})`); g.addColorStop(1, 'rgba(241,245,249,0)');
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, s, 0, TAU); ctx.fill(); ctx.restore();
  };
  /** Un flacon de produit (verre, bouchon, étiquette avec son nom ; o.danger = 'corrosif' : pictogramme). */
  P.flacon = (ctx, x, y, w, h, o = {}) => {
    const col = o.col || P.LIQ.ethanol, cou = w * .38, ye = y + h * .22;
    const forme = () => { ctx.beginPath(); ctx.moveTo(x - cou / 2, y); ctx.lineTo(x - cou / 2, ye); ctx.quadraticCurveTo(x - w / 2, ye + 4, x - w / 2, ye + 14); ctx.lineTo(x - w / 2, y + h - 6); ctx.quadraticCurveTo(x - w / 2, y + h, x - w / 2 + 6, y + h); ctx.lineTo(x + w / 2 - 6, y + h); ctx.quadraticCurveTo(x + w / 2, y + h, x + w / 2, y + h - 6); ctx.lineTo(x + w / 2, ye + 14); ctx.quadraticCurveTo(x + w / 2, ye + 4, x + cou / 2, ye); ctx.lineTo(x + cou / 2, y); };
    ctx.save();
    ctx.fillStyle = 'rgba(0,0,0,.25)'; ctx.beginPath(); ctx.ellipse(x + 3, y + h + 3, w * .5, 4, 0, 0, TAU); ctx.fill();
    forme(); ctx.fillStyle = 'rgba(190,220,240,.10)'; ctx.fill();
    liquide(ctx, () => { forme(); ctx.closePath(); }, x - w / 2, x + w / 2, y + h * (1 - (o.niveau ?? .7)), y + h, col);
    ctx.strokeStyle = 'rgba(225,240,252,.85)'; ctx.lineWidth = 1.8; forme(); ctx.stroke();
    ctx.fillStyle = o.bouchon || '#1e3a8a'; ctx.beginPath(); ctx.roundRect(x - cou / 2 - 2, y - 10, cou + 4, 12, 3); ctx.fill();
    // étiquette
    const ly = y + h * (o.danger ? .36 : .42), lh = h * (o.danger ? .26 : .34);
    ctx.fillStyle = '#fefce8'; ctx.beginPath(); ctx.roundRect(x - w / 2 + 4, ly, w - 8, lh, 3); ctx.fill();
    ctx.strokeStyle = 'rgba(0,0,0,.2)'; ctx.lineWidth = 1; ctx.stroke();
    if (o.nom) P.ecrit(ctx, o.nom, x, ly + lh / 2, Math.max(o.taille || 14, Math.min(lh * .62, (w - 10) / Math.max(1, o.nom.length) * 1.7)));
    if (o.danger === 'corrosif') P.picto(ctx, x, y + h * .8, Math.min(w * .2, h * .11));
    ctx.strokeStyle = 'rgba(255,255,255,.4)'; ctx.lineWidth = 3; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(x - w / 2 + 6, ye + 18); ctx.lineTo(x - w / 2 + 6, y + h - 10); ctx.stroke();
    ctx.restore();
  };
  /** Pictogramme de danger « corrosif » (losange rouge, fond blanc, gouttes qui rongent une main). */
  P.picto = (ctx, x, y, s) => {
    ctx.save(); ctx.translate(x, y); ctx.rotate(Math.PI / 4);
    ctx.fillStyle = '#fff'; ctx.fillRect(-s * .72, -s * .72, s * 1.44, s * 1.44); ctx.strokeStyle = '#dc2626'; ctx.lineWidth = s * .2; ctx.strokeRect(-s * .72, -s * .72, s * 1.44, s * 1.44);
    ctx.rotate(-Math.PI / 4); ctx.fillStyle = '#111'; ctx.fillRect(-s * .5, s * .15, s, s * .22); ctx.beginPath(); ctx.arc(-s * .2, -s * .25, s * .13, 0, TAU); ctx.arc(s * .2, -s * .15, s * .13, 0, TAU); ctx.fill();
    ctx.restore();
  };
  /** Une éprouvette graduée (niveau 0..1, couleur du liquide). */
  P.eprouvette = (ctx, x, y, w, h, niveau, col, o = {}) => {
    const forme = () => { ctx.beginPath(); ctx.moveTo(x - w / 2, y); ctx.lineTo(x - w / 2, y + h - 6); ctx.lineTo(x + w / 2, y + h - 6); ctx.lineTo(x + w / 2, y); };
    ctx.save();
    ctx.fillStyle = 'rgba(190,220,240,.10)'; forme(); ctx.fill();
    if (niveau > 0) liquide(ctx, () => { ctx.beginPath(); ctx.rect(x - w / 2 + 1.5, y, w - 3, h - 7.5); }, x - w / 2, x + w / 2, y + (h - 8) * (1 - niveau), y + h - 7, col);
    ctx.strokeStyle = 'rgba(225,240,252,.6)'; ctx.lineWidth = 1;
    for (let i = 1; i < 10; i++) { const yy = y + (h - 8) * i / 10; ctx.beginPath(); ctx.moveTo(x + w / 2 - (i % 5 ? 5 : 9), yy); ctx.lineTo(x + w / 2, yy); ctx.stroke(); }
    ctx.strokeStyle = 'rgba(225,240,252,.88)'; ctx.lineWidth = 1.8; forme(); ctx.stroke();
    ctx.fillStyle = 'rgba(190,220,240,.35)'; ctx.beginPath(); ctx.ellipse(x, y + h - 3, w * .9, 4, 0, 0, TAU); ctx.fill();
    ctx.strokeStyle = 'rgba(255,255,255,.4)'; ctx.lineWidth = 2.5; ctx.beginPath(); ctx.moveTo(x - w / 2 + 3, y + 6); ctx.lineTo(x - w / 2 + 3, y + h - 12); ctx.stroke();
    ctx.restore();
  };
  /** Un bécher : celui du lexique commun de chimie (shared/lexique/lexique-chimie.js). */
  P.becher = (ctx, x, y, w, h, niveau, col) => {
    if (window.Lexique && window.Lexique.chimie && window.Lexique.chimie.becher) return window.Lexique.chimie.becher(ctx, { x, y, w, h }, niveau, col);
    return y + h;
  };
  /** Un filet de liquide versé. */
  P.filet = (ctx, x, y1, y2, col) => { ctx.save(); ctx.fillStyle = rgba(col, 2.2); ctx.fillRect(x - 1.8, y1, 3.6, Math.max(0, y2 - y1)); ctx.restore(); };
  /** Des flocons de savon (solide blanc qui apparaît : le précipité). */
  P.flocons = (ctx, x, y, w, h, n, f = 1) => {
    const R = graine(31); ctx.save(); ctx.globalAlpha = Math.min(1, f);
    for (let i = 0; i < n; i++) { const px = x + R() * w, py = y + R() * h, s = 3 + R() * 4; const g = ctx.createRadialGradient(px - 1, py - 1, .5, px, py, s); g.addColorStop(0, '#ffffff'); g.addColorStop(1, '#e7e1c8'); ctx.fillStyle = g; ctx.beginPath(); ctx.ellipse(px, py, s, s * .7, R() * 3, 0, TAU); ctx.fill(); }
    ctx.restore();
  };
  /** Un entonnoir avec son papier filtre ; o.solide (0..1) : le savon retenu ; o.goutte (phase) : le filtrat qui coule. */
  P.entonnoir = (ctx, x, y, w, h, o = {}) => {
    ctx.save();
    const cone = () => { ctx.beginPath(); ctx.moveTo(x - w / 2, y); ctx.lineTo(x + w / 2, y); ctx.lineTo(x + 6, y + h * .62); ctx.lineTo(x + 6, y + h); ctx.lineTo(x - 6, y + h); ctx.lineTo(x - 6, y + h * .62); ctx.closePath(); };
    ctx.fillStyle = 'rgba(190,220,240,.12)'; cone(); ctx.fill();
    // papier filtre (blanc, plissé)
    ctx.fillStyle = '#f8fafc'; ctx.beginPath(); ctx.moveTo(x - w / 2 + 5, y + 3); ctx.lineTo(x + w / 2 - 5, y + 3); ctx.lineTo(x, y + h * .58); ctx.closePath(); ctx.fill();
    ctx.strokeStyle = 'rgba(148,163,184,.6)'; ctx.lineWidth = 1; for (let i = -2; i <= 2; i++) { ctx.beginPath(); ctx.moveTo(x + i * w * .09, y + 4); ctx.lineTo(x, y + h * .56); ctx.stroke(); }
    if (o.solide) P.flocons(ctx, x - w * .28, y + h * .12, w * .56, h * .22, Math.round(14 * o.solide), 1);
    ctx.strokeStyle = 'rgba(225,240,252,.88)'; ctx.lineWidth = 1.8; cone(); ctx.stroke();
    if (o.goutte != null) { const f = (o.goutte * .8) % 1; P.goutte(ctx, x, y + h + 6 + f * (o.chute || 40), 3.5, P.LIQ.salee.slice(0, 3).concat([.9])); }
    ctx.restore();
  };
  /** Le savon obtenu : un pain pâle, arrondi, avec un reflet. */
  P.savon = (ctx, x, y, w, h) => {
    ctx.save();
    P.ombre(ctx, () => { const g = ctx.createLinearGradient(0, y, 0, y + h); g.addColorStop(0, '#fffbeb'); g.addColorStop(1, '#e9dcae'); ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(x - w / 2, y, w, h, h * .45); ctx.fill(); }, 6);
    ctx.fillStyle = 'rgba(255,255,255,.7)'; ctx.beginPath(); ctx.ellipse(x - w * .18, y + h * .3, w * .2, h * .12, -.1, 0, TAU); ctx.fill();
    for (let i = 0; i < 4; i++) { ctx.strokeStyle = 'rgba(255,255,255,.8)'; ctx.lineWidth = 1; ctx.beginPath(); ctx.arc(x + w * .25 + i * 6, y - 4 - i * 5, 2.5 + i, 0, TAU); ctx.stroke(); }
    ctx.restore();
  };
  /** Un thermomètre (frac 0..1 : hauteur de la colonne rouge). */
  P.thermometre = (ctx, x, y, h, frac) => {
    ctx.save();
    ctx.fillStyle = 'rgba(241,245,249,.25)'; ctx.beginPath(); ctx.roundRect(x - 6, y, 12, h, 6); ctx.fill();
    ctx.strokeStyle = 'rgba(241,245,249,.85)'; ctx.lineWidth = 1.5; ctx.stroke();
    boule(ctx, x, y + h + 4, 9, '#fecaca', '#ef4444', '#991b1b');
    ctx.fillStyle = '#ef4444'; const hh = (h - 10) * Math.max(0, Math.min(1, frac)); ctx.fillRect(x - 2.5, y + h - hh, 5, hh + 4);
    ctx.strokeStyle = 'rgba(241,245,249,.6)'; ctx.lineWidth = 1; for (let i = 1; i < 10; i++) { const yy = y + h - 4 - (h - 14) * i / 10; ctx.beginPath(); ctx.moveTo(x + 6, yy); ctx.lineTo(x + (i % 5 ? 10 : 14), yy); ctx.stroke(); }
    ctx.restore();
  };
  /** Une balance électronique ; l'afficheur montre `aff` (texte vert sur fond sombre). */
  P.balance = (ctx, x, y, w, h, aff = '0 g') => {
    ctx.save();
    P.ombre(ctx, () => { const g = ctx.createLinearGradient(0, y, 0, y + h); g.addColorStop(0, '#e5e7eb'); g.addColorStop(1, '#9ca3af'); ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(x - w / 2, y, w, h, 8); ctx.fill(); }, 6);
    const gp = ctx.createLinearGradient(0, y - 8, 0, y); gp.addColorStop(0, '#f8fafc'); gp.addColorStop(1, '#94a3b8'); ctx.fillStyle = gp; ctx.beginPath(); ctx.roundRect(x - w * .38, y - 8, w * .76, 8, 3); ctx.fill();
    ctx.fillStyle = '#0f172a'; ctx.beginPath(); ctx.roundRect(x - w * .3, y + h * .3, w * .6, h * .48, 4); ctx.fill();
    P.ecrit(ctx, aff, x, y + h * .54, Math.min(22, h * .36), '#4ade80');
    ctx.restore();
  };
  /** La plaque de CCM : couche blanche de gel de silice sur un support ; o.ligne / o.front : hauteurs (fraction depuis
   *  le bas) de la ligne de dépôt et du front ; o.mouille (0..1) : zone mouillée par l'éluant ; o.taches = [{ u, v, col,
   *  a, r, croix }] (u : position horizontale 0..1, v : hauteur 0..1 depuis le bas). */
  P.plaque = (ctx, x, y, w, h, o = {}) => {
    ctx.save();
    P.ombre(ctx, () => { ctx.fillStyle = '#f8fafc'; ctx.fillRect(x, y, w, h); }, 5);
    const R = graine(13); ctx.fillStyle = 'rgba(148,163,184,.12)'; for (let i = 0; i < w * h / 120; i++) ctx.fillRect(x + R() * w, y + R() * h, 1.2, 1.2);
    const Y = v => y + h - v * h;
    if (o.mouille) { const g = ctx.createLinearGradient(0, y + h, 0, Y(o.mouille)); g.addColorStop(0, 'rgba(148,163,184,.30)'); g.addColorStop(1, 'rgba(148,163,184,.16)'); ctx.fillStyle = g; ctx.fillRect(x, Y(o.mouille), w, h - (Y(o.mouille) - y)); }
    if (o.ligne != null) { ctx.strokeStyle = 'rgba(71,85,105,.85)'; ctx.lineWidth = 1.3; ctx.beginPath(); ctx.moveTo(x + 4, Y(o.ligne)); ctx.lineTo(x + w - 4, Y(o.ligne)); ctx.stroke(); }
    if (o.front != null) { ctx.strokeStyle = 'rgba(71,85,105,.85)'; ctx.lineWidth = 1.3; ctx.setLineDash([5, 3]); ctx.beginPath(); ctx.moveTo(x + 4, Y(o.front)); ctx.lineTo(x + w - 4, Y(o.front)); ctx.stroke(); ctx.setLineDash([]); }
    for (const t of (o.taches || [])) {
      const tx = x + t.u * w, ty = Y(t.v), r = t.r || 6, a = t.a ?? 1;
      if (a <= 0) continue;
      if (t.croix) { ctx.strokeStyle = `rgba(30,41,59,${.85 * a})`; ctx.lineWidth = 1.6; ctx.beginPath(); ctx.moveTo(tx - 4, ty - 4); ctx.lineTo(tx + 4, ty + 4); ctx.moveTo(tx + 4, ty - 4); ctx.lineTo(tx - 4, ty + 4); ctx.stroke(); continue; }
      const col = t.col || [71, 85, 105];
      const g = ctx.createRadialGradient(tx, ty, 1, tx, ty, r); g.addColorStop(0, rgba(col.concat([.95 * a]))); g.addColorStop(1, rgba(col.concat([.35 * a])));
      ctx.fillStyle = g; ctx.beginPath(); ctx.ellipse(tx, ty, r * 1.15, r * .85, 0, 0, TAU); ctx.fill();
      if (t.cerne) { ctx.strokeStyle = `rgba(71,85,105,${a})`; ctx.lineWidth = 1.3; ctx.beginPath(); ctx.ellipse(tx, ty, r * 1.6, r * 1.25, 0, 0, TAU); ctx.stroke(); }
    }
    ctx.strokeStyle = 'rgba(148,163,184,.9)'; ctx.lineWidth = 1; ctx.strokeRect(x, y, w, h);
    ctx.restore();
  };
  /** La cuve de chromatographie : bocal de verre, éluant au fond (hauteur he), couvercle (o.couvercle 0..1 : posé). */
  P.cuve = (ctx, x, y, w, h, he, o = {}) => {
    ctx.save();
    ctx.fillStyle = 'rgba(0,0,0,.25)'; ctx.beginPath(); ctx.ellipse(x + w / 2 + 3, y + h + 3, w * .5, 5, 0, 0, TAU); ctx.fill();
    ctx.fillStyle = 'rgba(190,220,240,.10)'; ctx.fillRect(x, y, w, h);
    if (he > 0) liquide(ctx, () => { ctx.beginPath(); ctx.rect(x + 2, y, w - 4, h - 2); }, x, x + w, y + h - he, y + h - 2, P.LIQ.eluant);
    ctx.restore();
  };
  /** Le devant de la cuve (verre, reflets) et le couvercle : à peindre APRÈS la plaque, pour qu'elle soit dedans. */
  P.cuveDevant = (ctx, x, y, w, h, o = {}) => {
    ctx.save();
    ctx.strokeStyle = 'rgba(225,240,252,.88)'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x, y + h); ctx.lineTo(x + w, y + h); ctx.lineTo(x + w, y); ctx.stroke();
    ctx.strokeStyle = 'rgba(255,255,255,.3)'; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(x + 6, y + 10); ctx.lineTo(x + 6, y + h - 10); ctx.stroke();
    if (o.couvercle) {
      const k = Math.min(1, o.couvercle), yc = y - 6 - (1 - k) * 60, xc = x + (1 - k) * 30;
      ctx.globalAlpha = Math.min(1, k * 2);
      const g = ctx.createLinearGradient(0, yc, 0, yc + 10); g.addColorStop(0, 'rgba(226,232,240,.9)'); g.addColorStop(1, 'rgba(148,163,184,.7)');
      ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(xc - 6, yc, w + 12, 10, 4); ctx.fill();
      ctx.fillStyle = 'rgba(100,116,139,.9)'; ctx.beginPath(); ctx.roundRect(xc + w / 2 - 12, yc - 7, 24, 8, 3); ctx.fill();
    }
    ctx.restore();
  };
  /** La lampe UV (boîtier, tube violet qui brille quand allumée). */
  P.lampeUV = (ctx, x, y, w, allume = 0) => {
    ctx.save();
    P.ombre(ctx, () => { const g = ctx.createLinearGradient(0, y, 0, y + 26); g.addColorStop(0, '#475569'); g.addColorStop(1, '#0f172a'); ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(x - w / 2, y, w, 26, 6); ctx.fill(); }, 6);
    ctx.fillStyle = allume ? '#c4b5fd' : '#4c1d95'; ctx.fillRect(x - w / 2 + 8, y + 18, w - 16, 6);
    if (allume) { const g = ctx.createLinearGradient(0, y + 24, 0, y + 24 + 120); g.addColorStop(0, `rgba(167,139,250,${.45 * allume})`); g.addColorStop(1, 'rgba(167,139,250,0)'); ctx.fillStyle = g; ctx.beginPath(); ctx.moveTo(x - w / 2 + 8, y + 24); ctx.lineTo(x + w / 2 - 8, y + 24); ctx.lineTo(x + w / 2 + 20, y + 144); ctx.lineTo(x - w / 2 - 20, y + 144); ctx.closePath(); ctx.fill(); }
    ctx.restore();
  };
  /** Le capillaire (tube fin de verre) qui dépose une goutte. */
  P.capillaire = (ctx, x, y, l = 60, col = [100, 116, 139]) => {
    ctx.save(); ctx.strokeStyle = 'rgba(225,240,252,.9)'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + l * .35, y - l); ctx.stroke();
    ctx.strokeStyle = rgba(col.concat([.8])); ctx.lineWidth = 1.4; ctx.beginPath(); ctx.moveTo(x + 1, y - 2); ctx.lineTo(x + l * .12, y - l * .35); ctx.stroke(); ctx.restore();
  };
  /** Des lunettes de protection (vues de face). */
  P.lunettes = (ctx, x, y, s) => {
    ctx.save(); ctx.lineWidth = s * .08;
    const g = ctx.createLinearGradient(0, y - s * .3, 0, y + s * .3); g.addColorStop(0, 'rgba(186,230,253,.55)'); g.addColorStop(1, 'rgba(56,189,248,.35)');
    ctx.fillStyle = g; ctx.strokeStyle = '#f59e0b';
    ctx.beginPath(); ctx.roundRect(x - s * .62, y - s * .26, s * 1.24, s * .52, s * .22); ctx.fill(); ctx.stroke();
    ctx.strokeStyle = '#f59e0b'; ctx.beginPath(); ctx.moveTo(x, y - s * .2); ctx.lineTo(x, y + s * .1); ctx.stroke();
    ctx.strokeStyle = '#92400e'; ctx.lineWidth = s * .06; ctx.beginPath(); ctx.moveTo(x - s * .62, y); ctx.lineTo(x - s * .85, y - s * .05); ctx.moveTo(x + s * .62, y); ctx.lineTo(x + s * .85, y - s * .05); ctx.stroke();
    ctx.fillStyle = 'rgba(255,255,255,.6)'; ctx.beginPath(); ctx.ellipse(x - s * .35, y - s * .1, s * .14, s * .05, -.3, 0, TAU); ctx.fill();
    ctx.restore();
  };
  /** Un gant de protection (bleu, nitrile). */
  P.gant = (ctx, x, y, s) => {
    ctx.save(); P.ombre(ctx, () => {
      const g = ctx.createLinearGradient(x - s * .4, 0, x + s * .4, 0); g.addColorStop(0, '#1d4ed8'); g.addColorStop(.5, '#60a5fa'); g.addColorStop(1, '#1e40af'); ctx.fillStyle = g;
      ctx.beginPath(); ctx.roundRect(x - s * .3, y - s * .1, s * .6, s * .6, s * .12); ctx.fill();
      for (let i = 0; i < 4; i++) { ctx.beginPath(); ctx.roundRect(x - s * .3 + i * s * .155, y - s * .55, s * .13, s * .5, s * .065); ctx.fill(); }
      ctx.beginPath(); ctx.ellipse(x + s * .38, y + s * .05, s * .1, s * .25, -.6, 0, TAU); ctx.fill();
      ctx.fillStyle = '#1e3a8a'; ctx.fillRect(x - s * .32, y + s * .45, s * .64, s * .2);
    }, 4); ctx.restore();
  };
  /** Une fleur de jasmin (cinq pétales blancs, cœur jaune pâle). */
  P.jasmin = (ctx, x, y, s) => {
    ctx.save();
    for (let i = 0; i < 5; i++) { const a = -Math.PI / 2 + i * TAU / 5; ctx.save(); ctx.translate(x + Math.cos(a) * s * .42, y + Math.sin(a) * s * .42); ctx.rotate(a + Math.PI / 2); const g = ctx.createRadialGradient(0, 0, 1, 0, 0, s * .45); g.addColorStop(0, '#ffffff'); g.addColorStop(1, '#e2e8f0'); ctx.fillStyle = g; ctx.beginPath(); ctx.ellipse(0, 0, s * .26, s * .44, 0, 0, TAU); ctx.fill(); ctx.restore(); }
    boule(ctx, x, y, s * .16, '#fef9c3', '#fde047', '#ca8a04');
    ctx.restore();
  };
  /** Une feuille verte. */
  P.feuille = (ctx, x, y, s, a = 0) => {
    ctx.save(); ctx.translate(x, y); ctx.rotate(a); const g = ctx.createLinearGradient(-s, 0, s, 0); g.addColorStop(0, '#166534'); g.addColorStop(1, '#4ade80');
    ctx.fillStyle = g; ctx.beginPath(); ctx.moveTo(-s, 0); ctx.quadraticCurveTo(0, -s * .55, s, 0); ctx.quadraticCurveTo(0, s * .55, -s, 0); ctx.fill();
    ctx.strokeStyle = 'rgba(220,252,231,.6)'; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(-s * .9, 0); ctx.lineTo(s * .9, 0); ctx.stroke(); ctx.restore();
  };
  /** Un petit flacon de parfum (verre, bouchon doré). */
  P.parfum = (ctx, x, y, s, col = [253, 230, 138, .55]) => {
    ctx.save();
    const forme = () => { ctx.beginPath(); ctx.roundRect(x - s * .4, y - s * .45, s * .8, s * .9, s * .2); };
    ctx.fillStyle = 'rgba(190,220,240,.12)'; forme(); ctx.fill();
    liquide(ctx, forme, x - s * .4, x + s * .4, y - s * .2, y + s * .45, col, false);
    ctx.strokeStyle = 'rgba(225,240,252,.9)'; ctx.lineWidth = 1.6; forme(); ctx.stroke();
    boule(ctx, x, y - s * .62, s * .2, '#fef3c7', '#f59e0b', '#92400e');
    ctx.restore();
  };
  /** Une usine (bâtiments, cheminées, fumée), pour la chimie lourde. */
  P.usine = (ctx, x, y, s, phase = 0) => {
    ctx.save();
    P.ombre(ctx, () => {
      const g = ctx.createLinearGradient(0, y - s * .5, 0, y); g.addColorStop(0, '#94a3b8'); g.addColorStop(1, '#475569'); ctx.fillStyle = g;
      ctx.fillRect(x - s * .6, y - s * .35, s * 1.2, s * .35);
      ctx.beginPath(); ctx.moveTo(x - s * .6, y - s * .35); for (let i = 0; i < 3; i++) { ctx.lineTo(x - s * .6 + i * s * .4, y - s * .55); ctx.lineTo(x - s * .6 + (i + 1) * s * .4, y - s * .35); } ctx.fill();
      ctx.fillStyle = '#64748b'; ctx.fillRect(x + s * .35, y - s * .95, s * .12, s * .6); ctx.fillRect(x + s * .12, y - s * .8, s * .1, s * .45);
      // cuves de stockage
      for (const dx of [-.85, -.68]) { const gc = ctx.createLinearGradient(x + dx * s - s * .08, 0, x + dx * s + s * .08, 0); gc.addColorStop(0, '#cbd5e1'); gc.addColorStop(.5, '#f8fafc'); gc.addColorStop(1, '#94a3b8'); ctx.fillStyle = gc; ctx.beginPath(); ctx.roundRect(x + dx * s - s * .08, y - s * .42, s * .16, s * .42, s * .05); ctx.fill(); }
    }, 6);
    ctx.fillStyle = '#fde68a'; for (let i = 0; i < 5; i++) ctx.fillRect(x - s * .5 + i * s * .22, y - s * .22, s * .1, s * .08);
    for (let i = 0; i < 4; i++) { const f = ((phase * .4) + i / 4) % 1; P.vapeur(ctx, x + s * .41 + f * s * .25, y - s * .98 - f * s * .5, s * (.08 + f * .14), .55 * (1 - f)); }
    ctx.restore();
  };
  /** Une bouteille en plastique (chimie lourde : les plastiques). */
  P.bouteille = (ctx, x, y, s, col = [125, 211, 252]) => {
    ctx.save();
    const forme = () => { ctx.beginPath(); ctx.moveTo(x - s * .1, y - s); ctx.lineTo(x - s * .1, y - s * .85); ctx.quadraticCurveTo(x - s * .28, y - s * .75, x - s * .28, y - s * .55); ctx.lineTo(x - s * .28, y); ctx.lineTo(x + s * .28, y); ctx.lineTo(x + s * .28, y - s * .55); ctx.quadraticCurveTo(x + s * .28, y - s * .75, x + s * .1, y - s * .85); ctx.lineTo(x + s * .1, y - s); ctx.closePath(); };
    const g = ctx.createLinearGradient(x - s * .3, 0, x + s * .3, 0); g.addColorStop(0, rgba(col.concat([.35]))); g.addColorStop(.4, rgba(clair(col, .6).slice(0, 3).concat([.5]))); g.addColorStop(1, rgba(col.concat([.45])));
    ctx.fillStyle = g; forme(); ctx.fill(); ctx.strokeStyle = 'rgba(224,242,254,.9)'; ctx.lineWidth = 1.5; forme(); ctx.stroke();
    ctx.fillStyle = '#2563eb'; ctx.fillRect(x - s * .12, y - s * 1.08, s * .24, s * .1);
    ctx.fillStyle = 'rgba(255,255,255,.7)'; ctx.fillRect(x - s * .28, y - s * .45, s * .56, s * .16);
    ctx.restore();
  };
  /** Un pot de peinture ouvert (chimie des spécialités). */
  P.peinture = (ctx, x, y, s, col = [239, 68, 68]) => {
    ctx.save();
    P.ombre(ctx, () => { const g = ctx.createLinearGradient(x - s * .4, 0, x + s * .4, 0); g.addColorStop(0, '#94a3b8'); g.addColorStop(.45, '#f1f5f9'); g.addColorStop(1, '#64748b'); ctx.fillStyle = g; ctx.fillRect(x - s * .4, y - s * .7, s * .8, s * .7); ctx.beginPath(); ctx.ellipse(x, y, s * .4, s * .1, 0, 0, Math.PI); ctx.fill(); }, 5);
    ctx.fillStyle = rgba(col); ctx.beginPath(); ctx.ellipse(x, y - s * .7, s * .4, s * .1, 0, 0, TAU); ctx.fill();
    ctx.fillStyle = rgba(fonce(col, .15)); ctx.beginPath(); ctx.moveTo(x - s * .4, y - s * .7); ctx.quadraticCurveTo(x - s * .44, y - s * .45, x - s * .38, y - s * .3); ctx.quadraticCurveTo(x - s * .34, y - s * .5, x - s * .3, y - s * .66); ctx.fill();
    ctx.fillStyle = rgba(col); ctx.fillRect(x - s * .4, y - s * .45, s * .8, s * .18);
    ctx.restore();
  };
  /** Des médicaments : comprimés et gélules (chimie fine). */
  P.medicaments = (ctx, x, y, s) => {
    ctx.save();
    const gel = (gx, gy, a, c1, c2) => { ctx.save(); ctx.translate(gx, gy); ctx.rotate(a); P.ombre(ctx, () => { ctx.fillStyle = c1; ctx.beginPath(); ctx.roundRect(-s * .22, -s * .09, s * .22, s * .18, [s * .09, 0, 0, s * .09]); ctx.fill(); ctx.fillStyle = c2; ctx.beginPath(); ctx.roundRect(0, -s * .09, s * .22, s * .18, [0, s * .09, s * .09, 0]); ctx.fill(); }, 3); ctx.fillStyle = 'rgba(255,255,255,.5)'; ctx.fillRect(-s * .17, -s * .06, s * .3, s * .03); ctx.restore(); };
    const comp = (cx, cy) => { boule(ctx, cx, cy, s * .12, '#ffffff', '#f1f5f9', '#cbd5e1'); ctx.strokeStyle = 'rgba(148,163,184,.8)'; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(cx - s * .08, cy); ctx.lineTo(cx + s * .08, cy); ctx.stroke(); };
    gel(x - s * .2, y - s * .1, -.4, '#ef4444', '#fef2f2'); gel(x + s * .25, y - s * .25, .3, '#3b82f6', '#eff6ff');
    comp(x + s * .05, y + s * .12); comp(x - s * .32, y + s * .2); comp(x + s * .35, y + s * .1);
    ctx.restore();
  };
  /** Un verre d'eau (liquide bleuté). */
  P.verre = (ctx, x, y, w, h, col = P.LIQ.eau) => {
    ctx.save();
    const forme = () => { ctx.beginPath(); ctx.moveTo(x - w / 2, y); ctx.lineTo(x - w * .4, y + h); ctx.lineTo(x + w * .4, y + h); ctx.lineTo(x + w / 2, y); };
    ctx.fillStyle = 'rgba(190,220,240,.08)'; forme(); ctx.fill();
    liquide(ctx, () => { forme(); ctx.closePath(); }, x - w / 2, x + w / 2, y + h * .2, y + h, col);
    ctx.strokeStyle = 'rgba(225,240,252,.9)'; ctx.lineWidth = 1.8; forme(); ctx.stroke();
    ctx.strokeStyle = 'rgba(255,255,255,.4)'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(x - w * .4, y + 8); ctx.lineTo(x - w * .34, y + h - 8); ctx.stroke();
    ctx.restore();
  };
  /** Une molécule d'eau H₂O (un O rouge, deux H blancs) — couleurs du lexique commun. */
  P.eau = (ctx, x, y, s, a = 0) => {
    ctx.save(); ctx.translate(x, y); ctx.rotate(a);
    P.sphere(ctx, -s * .62, s * .42, s * .5, [241, 245, 249]); P.sphere(ctx, s * .62, s * .42, s * .5, [241, 245, 249]);
    P.sphere(ctx, 0, 0, s * .75, [239, 68, 68]);
    ctx.restore();
  };
  /** Un ion (sphère colorée + sa charge écrite dessus). */
  P.ion = (ctx, x, y, r, col, charge) => { P.sphere(ctx, x, y, r, col); P.ecrit(ctx, charge, x, y + 1, Math.max(10, r * 1.1), '#0b1f2a'); };
  /** Un pain de glace / un cristal de sel : petit cube translucide. */
  P.cristal = (ctx, x, y, s) => {
    ctx.save(); ctx.fillStyle = 'rgba(241,245,249,.85)'; ctx.beginPath(); ctx.moveTo(x - s, y - s * .4); ctx.lineTo(x, y - s); ctx.lineTo(x + s, y - s * .4); ctx.lineTo(x, y + s * .2); ctx.closePath(); ctx.fill();
    ctx.fillStyle = 'rgba(203,213,225,.85)'; ctx.beginPath(); ctx.moveTo(x - s, y - s * .4); ctx.lineTo(x, y + s * .2); ctx.lineTo(x, y + s); ctx.lineTo(x - s, y + s * .4); ctx.closePath(); ctx.fill();
    ctx.fillStyle = 'rgba(148,163,184,.85)'; ctx.beginPath(); ctx.moveTo(x + s, y - s * .4); ctx.lineTo(x, y + s * .2); ctx.lineTo(x, y + s); ctx.lineTo(x + s, y + s * .4); ctx.closePath(); ctx.fill();
    ctx.restore();
  };
  /** Un tube à essais (o.niveau, o.col, o.couches). */
  P.tube = (ctx, x, y, w, h, o = {}) => {
    ctx.save();
    const forme = () => { ctx.beginPath(); ctx.moveTo(x - w / 2, y); ctx.lineTo(x - w / 2, y + h - w / 2); ctx.arc(x, y + h - w / 2, w / 2, Math.PI, 0, true); ctx.lineTo(x + w / 2, y); };
    ctx.fillStyle = 'rgba(190,220,240,.10)'; forme(); ctx.fill();
    let bas = y + h;
    (o.couches || []).forEach((cc, i) => { const ys = y + h - (h - 6) * cc.f; liquide(ctx, () => { forme(); ctx.closePath(); }, x - w / 2, x + w / 2, ys, bas, cc.col, i === o.couches.length - 1); bas = ys; });
    ctx.strokeStyle = 'rgba(225,240,252,.9)'; ctx.lineWidth = 1.8; forme(); ctx.stroke();
    ctx.strokeStyle = 'rgba(255,255,255,.4)'; ctx.lineWidth = 2.5; ctx.beginPath(); ctx.moveTo(x - w / 2 + 3, y + 6); ctx.lineTo(x - w / 2 + 3, y + h - w); ctx.stroke();
    ctx.restore();
  };

  /**
   * LE MONTAGE DU CHAUFFAGE À REFLUX, assemblé (même dessin dans toutes les diapos : montage, reflux, application).
   * (cx, yb) = milieu du ballon, niveau de la table ; s = échelle. o.k = { potence, elevateur, chauffe, ballon,
   * refrigerant, tuyaux, eau } (0..1 : apparition de chaque pièce ; absent = 1). o.couches / o.ponce / o.bulles /
   * o.agite : le contenu du ballon ; o.chaud (0..1) ; o.phase : l'eau qui coule ; o.ouvert : sans réfrigérant (le col
   * reste ouvert) ; o.vapeur = { t, k } : les vapeurs montent (k 0..1), se condensent sur les boules et retombent en
   * gouttes (o.vapeur.gouttes 0..1). Renvoie la géométrie : points d'attache des légendes et boîtes des repères.
   */
  P.montage = (ctx, cx, yb, o = {}) => {
    const s = o.s || 1, k = Object.assign({ potence: 1, elevateur: 1, chauffe: 1, ballon: 1, refrigerant: 1, tuyaux: 1, eau: 1 }, o.k || {});
    const xp = cx - 92 * s, r = 44 * s, yE = yb - 50 * s, yC = yE - 46 * s, yBal = yC + 16 * s - r, haut = yBal - 1.75 * r;
    const yRb = haut - 4 * s, yRh = yRb - 172 * s, wR = 30 * s;
    const G = { s, xp, r, yBal, haut, yRb, yRh, cx, yb, wR };
    const fondu = (a, fn) => { if (a <= 0) return; ctx.save(); ctx.globalAlpha *= Math.min(1, a); fn(); ctx.restore(); };
    fondu(k.potence, () => P.potence(ctx, xp, yb, 352 * s, { socle: 130 * s, pinces: [
      ...(k.ballon >= 1 ? [{ y: haut + 14 * s, x2: cx, ouverture: 13 * s }] : []),
      ...(!o.ouvert && k.refrigerant >= 1 ? [{ y: yRh + 64 * s, x2: cx, ouverture: 17 * s }] : []) ] }));
    fondu(k.elevateur, () => P.elevateur(ctx, cx, yE, 116 * s, 50 * s));
    fondu(k.chauffe, () => P.chauffeBallon(ctx, cx, yC, 124 * s, 46 * s, o.chaud || 0));
    fondu(k.ballon, () => P.ballon(ctx, cx, yBal, r, { couches: o.couches, ponce: o.ponce, bulles: o.bulles, agite: o.agite, flocons: o.flocons }));
    let R = null;
    if (!o.ouvert) fondu(k.refrigerant, () => { R = P.refrigerant(ctx, cx, yRh, yRb, { w: wR, eau: k.eau * (o.eauNiveau ?? 1), phase: o.phase, boules: 5 }); });
    if (!R) R = { entree: [cx + wR / 2 + 17, yRb - 22 * s], sortie: [cx + wR / 2 + 17, yRh + 22 * s], boules: [], rb: 0 };
    G.R = R;
    if (!o.ouvert) fondu(k.tuyaux, () => {
      P.tuyau(ctx, [R.entree, [cx + 74 * s, R.entree[1]], [cx + 74 * s, yb - 6 * s]], { eau: k.eau > .5 });
      P.tuyau(ctx, [R.sortie, [cx + 96 * s, R.sortie[1]], [cx + 96 * s, yb - 6 * s]], { eau: k.eau > .5 });
    });
    // vapeurs, condensation, gouttes
    const v = o.vapeur;
    if (v && v.k > 0) {
      const t = v.t || 0, hautMax = o.ouvert ? haut - 120 * s : yRh + 60 * s;
      for (let i = 0; i < 10; i++) {
        const f = ((t * .45) + i / 10) % 1, yy = yBal - r * .2 - f * (yBal - r * .2 - hautMax), xx = cx + Math.sin(f * 7 + i) * 5 * s;
        if (o.ouvert || yy > yRh + 60 * s) P.vapeur(ctx, xx, yy, (10 + 8 * f) * s, .85 * v.k * (o.ouvert ? 1 : (1 - f * .5)));
      }
      if (!o.ouvert && (v.condense || 0) > 0) {
        ctx.save(); ctx.globalAlpha *= Math.min(1, v.condense);
        for (const yb2 of R.boules.slice(1)) { P.goutte(ctx, cx - R.rb * .55, yb2 + R.rb * .4, 2.8 * s); P.goutte(ctx, cx + R.rb * .5, yb2 + R.rb * .2, 2.4 * s); }
        ctx.restore();
      }
      if (!o.ouvert && (v.gouttes || 0) > 0) {
        for (let i = 0; i < 4; i++) { const f = ((t * .6) + i / 4) % 1, yy = yRh + 90 * s + f * (yBal - r * .3 - yRh - 90 * s); P.goutte(ctx, cx + 1, yy, 3.4 * s * Math.min(1, v.gouttes)); }
      }
    }
    G.boites = {
      potence: [xp - 26 * s, yb - 360 * s, 40 * s, 360 * s], elevateur: [cx - 60 * s, yE, 120 * s, 50 * s], chauffe: [cx - 64 * s, yC, 128 * s, 46 * s],
      ballon: [cx - r - 4 * s, haut, 2 * r + 8 * s, yBal + r - haut + 4 * s], refrigerant: [cx - wR / 2 - 4 * s, yRh, wR + 8 * s, yRb - yRh + 8 * s],
      entree: [R.entree[0] - 6 * s, R.entree[1] - 12 * s, 40 * s, 24 * s], sortie: [R.sortie[0] - 6 * s, R.sortie[1] - 12 * s, 40 * s, 24 * s],
    };
    G.ancres = {
      potence: [xp, yb - 330 * s], sortie: [R.sortie[0] + 10 * s, R.sortie[1]], refrigerant: [cx + wR / 2, (yRh + yRb) / 2 - 20 * s],
      entree: [R.entree[0] + 10 * s, R.entree[1]], ballon: [cx + r * .8, yBal - r * .3], chauffe: [cx + 62 * s, yC + 26 * s], elevateur: [cx + 58 * s, yE + 30 * s],
    };
    return G;
  };

  /**
   * Une vue « en cases » : chaque case (un objet peint + son titre + 1-2 lignes) paraît à son moment, la case en cours
   * s'allume. Grand cadre : les cases côte à côte (o.lignes rangées) ; petit cadre (téléphone) : la case en cours seule,
   * en grand. CASES = [{ id, titre, l1, l2, coul, peindre(g, x, y, k, S) }] — k = taille de la case (px du dessin).
   * Les repères portent l'id de la case. o.bas : une conclusion écrite en bas au moment o.basMoment.
   */
  function cases(c, S, scene, CASES, o = {}) {
    const pt = scene.petit, L = scene.L, tous = S.t <= 0, n = CASES.length, rangs = o.rangs || 1, parRang = Math.ceil(n / rangs);
    let courant = -1; CASES.forEach((k, i) => { if (!tous && S.a(k.id)) courant = i; });
    const hBas = o.bas && !pt ? 40 : 0, H = 420 - 8 - hBas, hr = H / rangs;
    CASES.forEach((k, i) => {
      let x, y, w, h;
      if (pt) { if (!tous && i !== courant) return; if (tous && i !== n - 1) return; x = 10; y = 6; w = L - 20; h = 404; }
      else { const rg = Math.floor(i / parRang), col = i % parRang, nn = Math.min(parRang, n - rg * parRang); w = (L - 16) / parRang; x = 8 + col * w + (parRang - nn) * w / 2; y = 4 + rg * hr; h = hr - 6; }
      c.repere(k.id, x, y, w, h, k.titre);
      if (!tous && !S.ecrit(c, k.id)) return;
      if (!tous && i === courant && !pt && !(o.basMoment && S.a(o.basMoment))) lueur(c, x + 2, y + 2, w - 4, h - 4, { vive: true });
      const tt = pt ? 34 : Math.min(21, w / 9), lt = pt ? 28 : Math.min(18, w / 10.5);
      const nl = (k.l1 ? 1 : 0) + (k.l2 ? 1 : 0), hTexte = tt + 10 + nl * (lt + 8);
      c.texte(k.titre, x + w / 2, y + tt + 4, { couleur: k.coul || 'jaune', taille: tt, gras: true, align: 'center', max: w - 12 });
      const kk = Math.min(w * .95, h - hTexte - 10) * (o.zoom || 1.1);
      c.direct(() => { const g = c.ctx; g.save(); k.peindre(g, x + w / 2, y + tt + 12 + (h - hTexte - 12) / 2, kk, S, tous ? 99 : S.t - (o.M || {})[k.id]); g.restore(); });
      const visible = !k.cache || S.conclusions;
      if (visible && k.l1) c.texte(k.l1, x + w / 2, y + h - 10 - (k.l2 ? lt + 8 : 0), { couleur: k.c1 || 'blanc', taille: lt, align: 'center', max: w - 12 });
      if (visible && k.l2) c.texte(k.l2, x + w / 2, y + h - 10, { couleur: k.c2 || k.c1 || 'blanc', taille: lt, align: 'center', max: w - 12 });
    });
    if (o.bas && !pt && (tous || S.ecrit(c, o.basMoment)) && S.conclusions) {
      c.texte(o.bas, L / 2, 410, { couleur: o.basCoul || 'vert', taille: 20, gras: true, align: 'center', max: L - 20 });
      c.repere(o.basMoment, 20, 388, L - 40, 30, o.bas);
    }
  }

  window.Synthese = { Scene, VW, VH, TAU, lueur, lignes, sim, param, doux, graine, P, boule, cases };
})();
