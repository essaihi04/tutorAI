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
  /* Les objets de labo (montage à reflux, réfrigérant, chauffe-ballon, CCM, filtration, verrerie) sont dessinés PAR le
   * lexique commun (shared/lexique/lexique-chimie.js, chargé avant ce fichier) : ici, de simples renvois. */
  const LC = () => window.Lexique.chimie;
  P.LIQ = LC().LIQUIDES;
  P.ombre = (...a) => LC().ombre(...a);
  function boule(ctx, x, y, r, c0, c1, c2) {
    const g = ctx.createRadialGradient(x - r * .35, y - r * .4, r * .1, x, y, r);
    g.addColorStop(0, c0); g.addColorStop(.55, c1); g.addColorStop(1, c2);
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.fill();
  }
  /** Une bille colorée (entité d'une espèce) : la bille du lexique commun (lexique.js), col = [r, g, b]. */
  P.sphere = (ctx, x, y, r, col, a = 1) => window.Lexique.bille(ctx, x, y, r, col.slice(0, 3), { alpha: a });
  /** Texte écrit SUR un objet peint (étiquette) : foncé et gras sur un objet clair. */
  P.ecrit = (ctx, s, x, y, taille = 14, couleur = '#0b1f2a', align = 'center') => {
    ctx.save(); ctx.font = `700 ${taille}px ${window.Tableau.POLICE}`; ctx.fillStyle = couleur; ctx.textAlign = align; ctx.textBaseline = 'middle';
    ctx.fillText(s, x, y); ctx.restore();
  };
  const liquide = (...a) => LC().liquide(...a);
  P.liquide = liquide;

  P.ballon = (...a) => LC().ballon(...a);
  P.ponce = (...a) => LC().ponce(...a);
  P.refrigerant = (...a) => LC().refrigerant(...a);
  P.tuyau = (...a) => LC().tuyau(...a);
  P.potence = (...a) => LC().potence(...a);
  P.chauffeBallon = (...a) => LC().chauffeBallon(...a);
  P.elevateur = (...a) => LC().elevateur(...a);
  P.goutte = (...a) => LC().gouttelette(...a);
  P.vapeur = (...a) => LC().vapeur(...a);
  P.flacon = (...a) => LC().flacon(...a);
  P.picto = (...a) => LC().picto(...a);
  P.eprouvette = (...a) => LC().eprouvette(...a);
  /** Un bécher : celui du lexique commun de chimie (shared/lexique/lexique-chimie.js). */
  P.becher = (ctx, x, y, w, h, niveau, col) => {
    if (window.Lexique && window.Lexique.chimie && window.Lexique.chimie.becher) return window.Lexique.chimie.becher(ctx, { x, y, w, h }, niveau, col);
    return y + h;
  };
  /** Un filet de liquide versé : celui du lexique commun. */
  P.filet = (ctx, x, y1, y2, col) => LC().filet(ctx, x, y1, y2, col);
  P.flocons = (...a) => LC().flocons(...a);
  P.entonnoir = (...a) => LC().entonnoir(...a);
  /** Le savon obtenu : un pain pâle, arrondi, avec un reflet. */
  P.savon = (ctx, x, y, w, h) => {
    ctx.save();
    P.ombre(ctx, () => { const g = ctx.createLinearGradient(0, y, 0, y + h); g.addColorStop(0, '#fffbeb'); g.addColorStop(1, '#e9dcae'); ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(x - w / 2, y, w, h, h * .45); ctx.fill(); }, 6);
    ctx.fillStyle = 'rgba(255,255,255,.7)'; ctx.beginPath(); ctx.ellipse(x - w * .18, y + h * .3, w * .2, h * .12, -.1, 0, TAU); ctx.fill();
    for (let i = 0; i < 4; i++) { ctx.strokeStyle = 'rgba(255,255,255,.8)'; ctx.lineWidth = 1; ctx.beginPath(); ctx.arc(x + w * .25 + i * 6, y - 4 - i * 5, 2.5 + i, 0, TAU); ctx.stroke(); }
    ctx.restore();
  };
  P.thermometre = (...a) => LC().thermometre(...a);
  P.balance = (...a) => LC().balance(...a);
  P.plaque = (...a) => LC().plaque(...a);
  P.cuve = (...a) => LC().cuve(...a);
  P.cuveDevant = (...a) => LC().cuveDevant(...a);
  P.lampeUV = (...a) => LC().lampeUV(...a);
  P.capillaire = (...a) => LC().capillaire(...a);
  /** Un crayon à papier (corps jaune, pointe de graphite) : on trace la ligne de dépôt et on entoure les taches. */
  P.crayon = (ctx, x, y, l = 70, a = -0.9) => {
    ctx.save(); ctx.translate(x, y); ctx.rotate(a);
    P.ombre(ctx, () => { const g = ctx.createLinearGradient(0, -5, 0, 5); g.addColorStop(0, '#fde68a'); g.addColorStop(.5, '#f59e0b'); g.addColorStop(1, '#b45309'); ctx.fillStyle = g; ctx.fillRect(12, -5, l - 20, 10); }, 4);
    ctx.fillStyle = '#f5d0a9'; ctx.beginPath(); ctx.moveTo(12, -5); ctx.lineTo(0, 0); ctx.lineTo(12, 5); ctx.closePath(); ctx.fill();
    ctx.fillStyle = '#334155'; ctx.beginPath(); ctx.moveTo(4, -1.7); ctx.lineTo(0, 0); ctx.lineTo(4, 1.7); ctx.closePath(); ctx.fill();
    ctx.fillStyle = '#f9a8d4'; ctx.fillRect(l - 8, -5, 8, 10); ctx.fillStyle = '#cbd5e1'; ctx.fillRect(l - 12, -5, 4, 10);
    ctx.restore();
  };
  /** Une règle graduée verticale (plastique clair) : zéro en y0, `n` centimètres vers le haut, `pc` px par cm. */
  P.regle = (ctx, x, y0, n, pc) => {
    ctx.save();
    const top = y0 - (n + .4) * pc, bot = y0 + .6 * pc;
    P.ombre(ctx, () => { const g = ctx.createLinearGradient(x, 0, x + 30, 0); g.addColorStop(0, 'rgba(254,249,195,.92)'); g.addColorStop(1, 'rgba(253,230,138,.85)'); ctx.fillStyle = g; ctx.fillRect(x, top, 30, bot - top); }, 4);
    ctx.strokeStyle = '#78350f'; ctx.lineWidth = 1.2;
    for (let i = 0; i <= n * 2; i++) { const yy = y0 - i * pc / 2; ctx.beginPath(); ctx.moveTo(x + 30, yy); ctx.lineTo(x + 30 - (i % 2 ? 6 : 12), yy); ctx.stroke(); }
    ctx.restore();
  };
  P.diiode = (...a) => LC().diiode(...a);
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
  /** Une molécule d'eau H₂O : celle du lexique commun (lexique.js : un O rouge, deux H blancs), tournée de `a`. */
  P.eau = (ctx, x, y, s, a = 0) => { ctx.save(); ctx.translate(x, y); ctx.rotate(a); window.Lexique.h2o(ctx, 0, 0, { echelle: s / 8 }); ctx.restore(); };
  /** Un ion (Ca²⁺, Mg²⁺, Na⁺, Cl⁻…) : celui du lexique commun (sa couleur fixe, sa charge écrite dessus). */
  P.ion = (ctx, x, y, r, nom) => LC().ion(ctx, x, y, r, nom);
  /** Un pain de glace / un cristal de sel : petit cube translucide. */
  P.cristal = (ctx, x, y, s) => {
    ctx.save(); ctx.fillStyle = 'rgba(241,245,249,.85)'; ctx.beginPath(); ctx.moveTo(x - s, y - s * .4); ctx.lineTo(x, y - s); ctx.lineTo(x + s, y - s * .4); ctx.lineTo(x, y + s * .2); ctx.closePath(); ctx.fill();
    ctx.fillStyle = 'rgba(203,213,225,.85)'; ctx.beginPath(); ctx.moveTo(x - s, y - s * .4); ctx.lineTo(x, y + s * .2); ctx.lineTo(x, y + s); ctx.lineTo(x - s, y + s * .4); ctx.closePath(); ctx.fill();
    ctx.fillStyle = 'rgba(148,163,184,.85)'; ctx.beginPath(); ctx.moveTo(x + s, y - s * .4); ctx.lineTo(x, y + s * .2); ctx.lineTo(x, y + s); ctx.lineTo(x + s, y + s * .4); ctx.closePath(); ctx.fill();
    ctx.restore();
  };
  P.tube = (...a) => LC().tube(...a);
  P.montage = (...a) => LC().montageReflux(...a);
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
