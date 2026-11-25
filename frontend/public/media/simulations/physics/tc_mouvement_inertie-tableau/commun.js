/*
 * Commun aux simulations du cours « Le mouvement et le principe d'inertie » (Tronc Commun Sciences, option française,
 * physique, chapitres 3 et 4 du livre), 25 novembre 2026.
 *
 *  - Mvt.Scene / Mvt.sim : cadre virtuel 760 × 420 en mode large, texte jamais sous 15 px à l'écran, simulation « à
 *    moments » (un temps de scène S.t, des moments nommés, un seul bouton Lancer → Pause → Reprendre → Rejouer, les
 *    commandes start / pause / resume / reset / play_until / set_time / set_parameters {conclusions}, `ce_qui_se_voit`,
 *    la vue lue dans `?vue=`). Même mécanique que le cours « La sortie écologique » (svt/tc_sortie_ecologique-tableau).
 *  - Mvt.panneau : la colonne d'écriture à droite (une ligne par moment) ; dans le petit cadre (téléphone en paysage),
 *    seulement la dernière ligne, en grand.
 *  - Mvt.P : les objets du cours, peints, UN SEUL DESSIN par objet dans tout le cours (règle « un objet, un seul dessin ») :
 *      table à coussin d'air (vue de dessus, et vue d'ensemble avec soufflerie et générateur d'impulsions),
 *      autoporteur (dessus : disque métal, éclateur central A rouge, éclateur B orange ; côté : cylindre sur coussin d'air),
 *      point d'enregistrement (point jaune cerclé de sombre), règle graduée, chronomètre, bus, personne, voiture, roue de
 *      vélo et sa valve rouge, ballon, grue, bloc de béton, seau, livre, caisse, boule, haltère, marteau, tige à deux masses,
 *      sphère / cylindre / disque.
 *  - Les couleurs gardent leur sens dans tout le cours ET dans tous les cours de mécanique : elles sont lues dans le
 *    lexique (Mvt.COUL ← Lexique.physique.MECANIQUE, Lexique.maths.ROLES, Lexique.physique.ECRITURE ; fiche
 *    docs/lexique-visuel/mecanique.md) : v⃗ vert · P⃗ rouge · R⃗ bleu · T⃗ orange · F⃗ violet · OM⃗ rose · i⃗ j⃗ cyan ·
 *    G point rose · points de l'enregistrement jaunes · trajectoire cyan en pointillé · éclateur A rouge, B orange ;
 *    graphes : courbe cyan, points jaunes, triangle de pente orange ; craie : titres et mots-clés jaune, légendes et
 *    données blanc, résultats et conclusions vert, pièges rose.
 *  - Les objets de la mécanique (point d'enregistrement, G, table à coussin d'air, autoporteur, règle, chronomètre)
 *    sont dessinés par Lexique.physique.mecanique ; Mvt.P les reprend sous le même nom.
 *  - Mvt.vecteur : une flèche épaisse à la craie et son nom surmonté d'une petite flèche (v⃗₃, P⃗, OM⃗).
 */
(function () {
  'use strict';
  const VW = 760, VH = 420, TAU = Math.PI * 2;
  const TAILLE_MIN = 15, L_MAX = 2.1;
  /* Les couleurs viennent du lexique (Lexique.physique.MECANIQUE, Lexique.maths.ROLES, Lexique.physique.ECRITURE) :
   * la page charge lexique-physique.js et lexique-maths.js AVANT ce fichier. */
  const LP = window.Lexique.physique, ME = LP.MECANIQUE, ROLES = window.Lexique.maths.ROLES, ECR = LP.ECRITURE;
  const COUL = { v: ME.v, P: ME.P, R: ME.R, T: ME.T, F: ME.F, OM: ME.OM, u: ME.i, G: ME.G, A: ME.eclateurA, B: ME.eclateurB, pt: ME.point,
    traj: ME.trajectoire, courbe: ROLES.courbe, pointG: ROLES.point, pente: ROLES.tangente, axes: ROLES.axes,
    titre: ECR.titre, legende: ECR.legende, donnee: ECR.donnee, relation: ECR.relation, res: ECR.resultat, concl: ECR.conclusion, piege: ECR.piege };
  const HEX = window.Tableau.COULEURS;

  /* ── La scène ──────────────────────────────────────────────────────────────────────────────────────────────── */
  function Scene(canvas, dessiner, options = {}) {
    const scene = { sale: true, L: VW };
    const craie = new window.Tableau.Craie(canvas, { onresize: () => { scene.sale = true; } });
    const KIT_REDUIT = !!(Object.getOwnPropertyDescriptor(window.Tableau.Craie.prototype, 'tailleMin') || {}).get;
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
        const fKit = Math.min(1, Math.max(.45, Math.min((W || 900) / 900, (H || 400) / 400)));
        craie.echelle = s; craie.tailleMin = KIT_REDUIT ? TAILLE_MIN / fKit : TAILLE_MIN;
        scene.petit = W < 520 || H < 320;
        scene.plancher = TAILLE_MIN / s;
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
      g.fillStyle = `rgba(${couleur}, ${vive ? 0.20 : 0.11})`; arrondi(g, x, y, w, h, o.r ?? 8); g.fill(); g.restore();
      g.save(); g.strokeStyle = `rgba(${couleur}, ${vive ? 0.95 : 0.55})`; g.lineWidth = vive ? 2.6 : 1.6;
      arrondi(g, x, y, w, h, o.r ?? 8); g.stroke(); g.restore();
      if (o.numero != null) c.texte(String(o.numero), o.nx ?? x - 6, o.ny ?? y + Math.min(h, 24) - 4,
        { couleur: 'jaune', taille: o.taille || 20, align: o.align || (o.nx == null ? 'right' : 'center'), gras: true });
    });
  }
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
    S.ecrit = (c, nom) => { const m = M(); if (!(nom in m) || S.t < m[nom] - 1e-6) return false; if (S.vu[nom] != null) c.depuis(S.vu[nom]); return true; };
    S.a = nom => { const m = M(); return nom in m && S.t >= m[nom] - 1e-6; };
    S.k = (nom, d = 1) => { const m = M(); return nom in m ? doux((S.t - m[nom]) / d) : 0; };
    S.kl = (nom, d = 1) => { const m = M(); return nom in m ? Math.max(0, Math.min(1, (S.t - m[nom]) / d)) : 0; };
    /** le dernier moment atteint (dans l'ordre des temps) */
    S.dernier = () => { const m = M(); let best = null; for (const k in m) if (S.t >= m[k] - 1e-6 && (best == null || m[k] >= m[best])) best = k; return best; };
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
      set_parameters: Object.assign({ conclusions: 'true | false (false : le résultat écrit reste caché tant que la question est ouverte)' }, o.schemaParametres || {}),
    });
    const config = { id: o.id, version: '1.0', title: o.titre, variants: [{ id: S.vue || 'principale', label: S.vue || 'principale' }], commands: commandes, command_schema: schema };
    const pont = protocole({
      id: o.id, commandes, config, texte: o.texte,
      etat: () => ({ simulation_status: S.running ? 'running' : S.pause ? 'paused' : (S.fait ? 'finished' : 'idle'), ce_qui_se_voit: o.ceQuiSeVoit(S),
        moments: M(), time_s: +S.t.toFixed(2), current_variant: S.vue || 'principale', parameters: Object.assign({ conclusions: S.conclusions, vue: S.vue }, o.etatParametres ? o.etatParametres(S) : {}) }),
      progression: () => (S.fait ? 1 : S.t / FIN()),
      executer: (cmd, p) => ({ start, pause, resume, reset, play_until: () => playUntil(p), set_time: () => setTime(p), set_parameters: () => setParameters(p) })[cmd]?.(),
    });
    S.pont = pont; window.__S = S; window.__M = M;   // pour les captures de contrôle
    etiquette(LANCER); bulle(fb, o.accueil || '');
    if (o.apres) o.apres(S, scene, pont);
    return S;
  }

  /**
   * Une simulation à plusieurs vues : `vues = { nom: { moments, fin, dessiner, motifs, accueil, fini, voir, texte } }`.
   * La vue est lue dans `?vue=` (la première par défaut).
   */
  function vues(id, defs, commun = {}) {
    const noms = Object.keys(defs), v = noms.includes(param('vue')) ? param('vue') : noms[0], d = defs[v];
    return sim(Object.assign({
      id: id + '_' + v, titre: d.titre || id, vue: v, moments: d.moments, fin: d.fin, graine: d.graine || 17, motifs: d.motifs || {},
      accueil: d.accueil || '', fini: d.fini || 'Terminé.', dessiner: d.dessiner, ceQuiSeVoit: d.voir, texte: d.texte || '',
      explication: d.explication, parametres: d.parametres, schemaParametres: d.schemaParametres, etatParametres: d.etatParametres, apres: d.apres, lancer: d.lancer,
    }, commun));
  }

  /**
   * La colonne d'écriture : `items = [{ m: moment, t: texte (fractions ⟦a|b⟧ permises), c: couleur, g: gras, r: repère,
   * conclusion: true }]`. Grand cadre : chaque ligne s'écrit à son moment, l'une sous l'autre, dans (x, y, w).
   * Petit cadre : seule la dernière ligne atteinte (o.petit = n lignes) s'écrit, en grand, en (o.px, o.py).
   */
  function panneau(c, S, scene, x, y, w, items, o = {}) {
    const dy = o.dy ?? 34, taille = o.taille ?? 19;
    const vus = items.filter(it => (S.t <= 0 && !o.vide) || S.a(it.m)).filter(it => !it.conclusion || S.conclusions);
    if (scene.petit) {
      const n = o.petit ?? 1, derniers = vus.slice(-n), tp = o.taillePetit ?? 30;
      derniers.forEach((it, k) => {
        const yy = (o.py ?? 40) + k * (tp * (/⟦/.test(it.t) ? 2.1 : 1.35));
        if (S.t > 0) S.ecrit(c, it.m);
        texteV(c, it.t, o.px ?? x, yy + (/⟦/.test(it.t) ? tp * .45 : 0), { couleur: it.c || 'blanc', taille: tp, gras: it.g, max: o.pw ?? w });
        if (it.r) c.repere(it.r, (o.px ?? x) - 4, yy - tp, (o.pw ?? w) + 8, tp * (/⟦/.test(it.t) ? 2.1 : 1.3), it.lab || it.t.replace(/[⟦⟧^]/g, '').replace('|', '/'));
      });
      return;
    }
    let yy = y;
    items.forEach(it => {
      const frac = /⟦/.test(it.t), h = frac ? dy * 1.55 : dy;
      if (it.conclusion && !S.conclusions) { yy += h; return; }
      if (S.t > 0 && !S.ecrit(c, it.m)) { yy += h; return; }
      texteV(c, it.t, x, yy + (frac ? dy * .45 : 0), { couleur: it.c || 'blanc', taille: it.taille || taille, gras: it.g, max: w });
      if (it.r) c.repere(it.r, x - 4, yy - taille, w + 8, h - 4, it.lab || it.t.replace(/[⟦⟧^]/g, '').replace('|', '/'));
      yy += h;
    });
  }

  /* ── Vecteurs à la craie ─────────────────────────────────────────────────────────────────────────────────── */
  /**
   * Un texte à la craie où « ^X » écrit un vecteur : la lettre (ou « OM », « v_3 ») surmontée d'une petite flèche.
   * « ^P + ^R = ^0 », « ^OM = x·^i + y·^j ». Les fractions ⟦a|b⟧ restent permises hors des vecteurs.
   */
  function texteV(c, s, x, y, o = {}) {
    s = String(s);
    if (!s.includes('^')) return c.texte(s, x, y, o);
    let t = o.taille || 18;
    if (o.plancher !== false && c.echelle && c.tailleMin) t = Math.max(t, c.tailleMin / c.echelle);
    const parts = s.split(/(\^[A-Za-z0-9]+(?:_\{[^}]+\}|_[A-Za-z0-9]+)?)/).filter(Boolean);
    const larg = p => (p.includes('⟦') ? c.largeurTexte(p, t) : c._largeur(p.replace(/^\^/, ''), t, o.gras));
    let total = parts.reduce((w, p) => w + larg(p), 0);
    if (o.max && total > o.max) { t = Math.max(10, t * o.max / total); total = parts.reduce((w, p) => w + larg(p), 0); }
    let px = o.align === 'center' ? x - total / 2 : o.align === 'right' ? x - total : x;
    for (const p of parts) {
      const w = larg(p), vect = p[0] === '^', nom = vect ? p.slice(1) : p;
      c.texte(nom, px, y, Object.assign({}, o, { taille: t, align: 'left', max: 0, plancher: false }));
      if (vect) {
        const base = nom.replace(/_.*/, ''), wb = c._largeur(base, t, o.gras), ya = y - t * .95;
        c.fleche(px + t * .04, ya, px + Math.max(wb, t * .5), ya, { couleur: o.couleur || 'blanc', largeur: Math.max(1.4, t * .07), tete: Math.max(4, t * .22), duree: .06 });
      }
      px += w;
    }
  }
  /** Le nom d'un vecteur : « v_3 » → v⃗₃ (texte et petite flèche au-dessus). */
  function nomVecteur(c, nom, x, y, o = {}) {
    texteV(c, '^' + nom, x, y, { couleur: o.couleur || 'blanc', taille: o.taille || 20, gras: true, align: o.align || 'left' });
  }
  /** Un vecteur : flèche épaisse de (x1, y1) à (x2, y2), son nom à `o.nom` posé en `o.nx, o.ny` (sinon au bout). */
  function vecteur(c, x1, y1, x2, y2, o = {}) {
    const coul = LM.fleche(c, x1, y1, x2, y2, o);
    if (o.nom) nomVecteur(c, o.nom, o.nx ?? x2 + 8, o.ny ?? y2 - 6, { couleur: coul, taille: o.taille || 20, align: o.align });
  }

  /* ── Graphique (papier millimétré sur le tableau) ──────────────────────────────────────────────────────────── */
  /** Un repère gradué : renvoie { X(v), Y(v) } ; `ax = {min,max,pas,nom,unite}`, `ay` idem. */
  function graphique(c, x, y, w, h, ax, ay, o = {}) {
    const X = v => x + (v - ax.min) / (ax.max - ax.min) * w, Y = v => y + h - (v - ay.min) / (ay.max - ay.min) * h;
    c.direct(() => {
      const g = c.ctx; g.save(); g.strokeStyle = 'rgba(148,163,184,.16)'; g.lineWidth = 1;
      for (let v = ax.min; v <= ax.max + 1e-9; v += ax.pas) { g.beginPath(); g.moveTo(X(v), y); g.lineTo(X(v), y + h); g.stroke(); }
      for (let v = ay.min; v <= ay.max + 1e-9; v += ay.pas) { g.beginPath(); g.moveTo(x, Y(v)); g.lineTo(x + w, Y(v)); g.stroke(); }
      g.restore();
    });
    const tg = o.taille || 15, pt = o.petit;
    c.fleche(X(ax.min), Y(Math.max(ay.min, 0)), x + w + 14, Y(Math.max(ay.min, 0)), { couleur: 'blanc', largeur: 1.8 });
    c.fleche(X(Math.max(ax.min, 0)), y + h, X(Math.max(ax.min, 0)), y - 14, { couleur: 'blanc', largeur: 1.8 });
    (ax.lab || []).forEach(v => c.texte(String(v).replace('.', ','), X(v), Y(Math.max(ay.min, 0)) + tg + 6, { couleur: 'faible', taille: tg, align: 'center', duree: .05 }));
    (ay.lab || []).forEach(v => c.texte(String(v).replace('.', ','), X(Math.max(ax.min, 0)) - 6, Y(v) + tg * .35, { couleur: 'faible', taille: tg, align: 'right', duree: .05 }));
    c.texte(ax.nom + (ax.unite ? ' (' + ax.unite + ')' : ''), x + w + (pt ? -4 : 4), Y(Math.max(ay.min, 0)) - 12, { couleur: 'cyan', taille: o.tailleNom || 17, align: pt ? 'right' : 'left' });
    c.texte(ay.nom + (ay.unite ? ' (' + ay.unite + ')' : ''), X(Math.max(ax.min, 0)) + 10, y - 6, { couleur: 'cyan', taille: o.tailleNom || 17 });
    return { X, Y };
  }

  /* ── Les objets du cours, peints ──────────────────────────────────────────────────────────────────────────── */
  const P = {};
  const LM = LP.mecanique;
  P.ombre = LM.ombre;
  const boule = LM.boule;
  P.boule = boule;
  P.point = (...a) => LM.point(...a);
  P.etincelle = (...a) => LM.etincelle(...a);
  P.table = (...a) => LM.table(...a);
  P.autoporteur = (...a) => LM.autoporteur(...a);
  P.autoporteurCote = (...a) => LM.autoporteurCote(...a);
  P.G = (...a) => LM.G(...a);
  P.regle = (...a) => LM.regle(...a);
  P.chrono = (...a) => LM.chrono(...a);
  /** Une personne debout (o.assis : assise ; o.marche : jambes écartées ; o.couleur du haut). Regarde vers o.sens (1 droite). */
  P.personne = (ctx, x, yb, h, o = {}) => {
    const s = o.sens || 1, haut = o.couleur || '#3b82f6';
    ctx.save(); ctx.globalAlpha = o.alpha ?? 1; ctx.lineCap = 'round';
    const tete = h * .11, epaule = yb - h * .8, hanche = o.assis ? yb - h * .38 : yb - h * .47;
    P.ombre(ctx, () => {
      ctx.strokeStyle = '#334155'; ctx.lineWidth = h * .09;
      if (o.assis) { ctx.beginPath(); ctx.moveTo(x, hanche); ctx.lineTo(x + s * h * .25, hanche); ctx.lineTo(x + s * h * .25, yb); ctx.stroke(); }
      else { const e = o.marche ? h * .12 : h * .04; ctx.beginPath(); ctx.moveTo(x, hanche); ctx.lineTo(x - e, yb); ctx.moveTo(x, hanche); ctx.lineTo(x + e, yb); ctx.stroke(); }
      const g = ctx.createLinearGradient(x - h * .1, 0, x + h * .1, 0); g.addColorStop(0, haut); g.addColorStop(1, '#1e293b');
      ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(x - h * .085, epaule, h * .17, hanche - epaule + h * .03, h * .04); ctx.fill();
      ctx.fillStyle = '#e0ac83'; ctx.beginPath(); ctx.arc(x + s * h * .01, epaule - tete * 1.1, tete, 0, TAU); ctx.fill();
      ctx.fillStyle = '#3b2a1e'; ctx.beginPath(); ctx.arc(x - s * tete * .15, epaule - tete * 1.35, tete * .95, Math.PI * .95, Math.PI * 2.05); ctx.fill();
    }, 4);
    ctx.strokeStyle = haut; ctx.lineWidth = h * .055; ctx.beginPath(); ctx.moveTo(x, epaule + h * .04);
    if (o.bras === 'pousse') ctx.lineTo(x + s * h * .3, epaule + h * .12); else ctx.lineTo(x + s * h * .05, hanche);
    ctx.stroke();
    ctx.fillStyle = '#111'; ctx.beginPath(); ctx.arc(x + s * tete * .5, epaule - tete * 1.15, Math.max(1, h * .012), 0, TAU); ctx.fill();
    ctx.restore();
  };
  /** Le bus vu de côté (roule vers la droite) : renvoie la ligne du plancher et les places. */
  P.bus = (ctx, x, yb, w, h, o = {}) => {
    ctx.save();
    P.ombre(ctx, () => {
      const g = ctx.createLinearGradient(0, yb - h, 0, yb); g.addColorStop(0, '#fde68a'); g.addColorStop(.55, '#f59e0b'); g.addColorStop(1, '#b45309');
      ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(x, yb - h, w, h * .86, [14, 22, 6, 6]); ctx.fill();
    }, 10);
    ctx.fillStyle = '#1e3a8a'; ctx.fillRect(x, yb - h * .3, w, h * .07);
    // vitres (intérieur visible)
    ctx.fillStyle = 'rgba(186,230,253,.28)'; ctx.strokeStyle = '#78350f'; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.roundRect(x + w * .03, yb - h * .9, w * .9, h * .5, 6); ctx.fill(); ctx.stroke();
    ctx.fillStyle = 'rgba(186,230,253,.5)'; ctx.beginPath(); ctx.roundRect(x + w * .94, yb - h * .9, w * .05, h * .42, [4, 10, 2, 2]); ctx.fill();
    for (const k of [.27, .51, .75]) { ctx.beginPath(); ctx.moveTo(x + w * (.03 + .9 * k), yb - h * .9); ctx.lineTo(x + w * (.03 + .9 * k), yb - h * .4); ctx.stroke(); }
    for (const fx of [.17, .82]) {
      const rx = x + w * fx, ry = yb - h * .08, rr = h * .14;
      P.ombre(ctx, () => boule(ctx, rx, ry, rr, '#64748b', '#1f2937', '#020617'), 5);
      ctx.fillStyle = '#cbd5e1'; ctx.beginPath(); ctx.arc(rx, ry, rr * .45, 0, TAU); ctx.fill();
      if (o.roue != null) { ctx.strokeStyle = '#334155'; ctx.lineWidth = 2; for (let k = 0; k < 3; k++) { const a = o.roue + k * TAU / 3; ctx.beginPath(); ctx.moveTo(rx, ry); ctx.lineTo(rx + Math.cos(a) * rr * .45, ry + Math.sin(a) * rr * .45); ctx.stroke(); } }
    }
    ctx.restore();
    return { plancher: yb - h * .4 };
  };
  /** La voiture vue de côté (vers la droite). */
  P.voiture = (ctx, x, yb, w, o = {}) => {
    const h = w * .42; ctx.save(); ctx.globalAlpha = o.alpha ?? 1;
    P.ombre(ctx, () => {
      const g = ctx.createLinearGradient(0, yb - h, 0, yb); g.addColorStop(0, '#fca5a5'); g.addColorStop(.5, '#dc2626'); g.addColorStop(1, '#7f1d1d');
      ctx.fillStyle = g; ctx.beginPath(); ctx.moveTo(x, yb - h * .25); ctx.lineTo(x + w * .05, yb - h * .55); ctx.lineTo(x + w * .3, yb - h * .6); ctx.lineTo(x + w * .42, yb - h);
      ctx.lineTo(x + w * .72, yb - h); ctx.lineTo(x + w * .86, yb - h * .58); ctx.lineTo(x + w, yb - h * .5); ctx.lineTo(x + w, yb - h * .2); ctx.closePath(); ctx.fill();
    }, 6);
    ctx.fillStyle = 'rgba(186,230,253,.75)'; ctx.beginPath(); ctx.moveTo(x + w * .45, yb - h * .92); ctx.lineTo(x + w * .69, yb - h * .92); ctx.lineTo(x + w * .8, yb - h * .6); ctx.lineTo(x + w * .37, yb - h * .6); ctx.closePath(); ctx.fill();
    for (const fx of [.22, .8]) { boule(ctx, x + w * fx, yb - h * .15, h * .26, '#64748b', '#1f2937', '#020617'); ctx.fillStyle = '#cbd5e1'; ctx.beginPath(); ctx.arc(x + w * fx, yb - h * .15, h * .11, 0, TAU); ctx.fill(); }
    ctx.restore();
  };
  /** La roue de vélo : jante, rayons, pneu, et la valve (point rouge) à l'angle `a`. Renvoie la position de la valve. */
  P.roue = (ctx, cx, cy, r, a, o = {}) => {
    ctx.save(); ctx.globalAlpha = o.alpha ?? 1;
    ctx.strokeStyle = '#111827'; ctx.lineWidth = r * .12; ctx.beginPath(); ctx.arc(cx, cy, r, 0, TAU); ctx.stroke();
    ctx.strokeStyle = '#94a3b8'; ctx.lineWidth = r * .04; ctx.beginPath(); ctx.arc(cx, cy, r * .9, 0, TAU); ctx.stroke();
    ctx.strokeStyle = 'rgba(203,213,225,.75)'; ctx.lineWidth = 1;
    for (let k = 0; k < 16; k++) { const b = a + k * TAU / 16; ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(cx + Math.cos(b) * r * .9, cy + Math.sin(b) * r * .9); ctx.stroke(); }
    boule(ctx, cx, cy, r * .1, '#e2e8f0', '#64748b', '#1f2937');
    const vx = cx + Math.cos(a) * r * .9, vy = cy + Math.sin(a) * r * .9;
    boule(ctx, vx, vy, Math.max(3.5, r * .08), '#fecaca', '#dc2626', '#7f1d1d');
    ctx.restore();
    return [vx, vy];
  };
  /** Le ballon de football (blanc, pentagones sombres). */
  P.ballon = (ctx, x, y, r, rot = 0) => {
    ctx.save(); P.ombre(ctx, () => boule(ctx, x, y, r, '#ffffff', '#e5e7eb', '#9ca3af'), 6);
    ctx.fillStyle = '#1f2937';
    const pent = (px, py, s, a) => { ctx.beginPath(); for (let i = 0; i < 5; i++) { const b = a + i * TAU / 5; ctx[i ? 'lineTo' : 'moveTo'](px + Math.cos(b) * s, py + Math.sin(b) * s); } ctx.closePath(); ctx.fill(); };
    pent(x, y, r * .32, rot); for (let i = 0; i < 5; i++) { const b = rot + i * TAU / 5 + Math.PI / 5; const d = r * .78; if (Math.cos(b) * d + x > x - r && true) { ctx.save(); ctx.beginPath(); ctx.arc(x, y, r * .97, 0, TAU); ctx.clip(); pent(x + Math.cos(b) * d, y + Math.sin(b) * d, r * .26, b); ctx.restore(); } }
    ctx.restore();
  };
  /** Une caisse en bois. */
  P.caisse = (ctx, x, yb, w, h) => {
    ctx.save(); P.ombre(ctx, () => { const g = ctx.createLinearGradient(x, 0, x + w, 0); g.addColorStop(0, '#b45309'); g.addColorStop(.5, '#d97706'); g.addColorStop(1, '#92400e'); ctx.fillStyle = g; ctx.fillRect(x, yb - h, w, h); }, 8);
    ctx.strokeStyle = 'rgba(69,26,3,.7)'; ctx.lineWidth = 3; ctx.strokeRect(x + 3, yb - h + 3, w - 6, h - 6);
    ctx.beginPath(); ctx.moveTo(x + 4, yb - h + 4); ctx.lineTo(x + w - 4, yb - 4); ctx.moveTo(x + w - 4, yb - h + 4); ctx.lineTo(x + 4, yb - 4); ctx.stroke();
    ctx.restore();
  };
  /** Un sol (bande peinte) ou un plan de table (bois). */
  P.sol = (ctx, x, y, w, h, o = {}) => {
    ctx.save(); const g = ctx.createLinearGradient(0, y, 0, y + h);
    if (o.bois) { g.addColorStop(0, '#d6a46a'); g.addColorStop(1, '#8a5a2b'); } else if (o.route) { g.addColorStop(0, '#4b5563'); g.addColorStop(1, '#1f2937'); } else { g.addColorStop(0, '#a3a3a3'); g.addColorStop(1, '#525252'); }
    ctx.fillStyle = g; ctx.fillRect(x, y, w, h);
    if (o.route) { ctx.strokeStyle = 'rgba(250,250,250,.8)'; ctx.lineWidth = 3; ctx.setLineDash([22, 18]); ctx.lineDashOffset = o.decalage || 0; ctx.beginPath(); ctx.moveTo(x, y + h * .55); ctx.lineTo(x + w, y + h * .55); ctx.stroke(); ctx.setLineDash([]); }
    if (o.bois) { ctx.strokeStyle = 'rgba(92,51,23,.35)'; ctx.lineWidth = 1; for (let i = 1; i < 4; i++) { ctx.beginPath(); ctx.moveTo(x, y + h * i / 4); ctx.bezierCurveTo(x + w * .3, y + h * i / 4 - 3, x + w * .6, y + h * i / 4 + 3, x + w, y + h * i / 4); ctx.stroke(); } }
    ctx.restore();
  };
  /** Un livre posé (couverture bleue, tranche des pages). */
  P.livre = (ctx, x, yb, w, h) => {
    ctx.save(); P.ombre(ctx, () => { ctx.fillStyle = '#1d4ed8'; ctx.beginPath(); ctx.roundRect(x, yb - h, w, h, 3); ctx.fill(); }, 6);
    ctx.fillStyle = '#f8fafc'; ctx.fillRect(x + 4, yb - h * .7, w - 6, h * .45);
    ctx.strokeStyle = 'rgba(100,116,139,.6)'; ctx.lineWidth = .8; for (let i = 1; i < 5; i++) { ctx.beginPath(); ctx.moveTo(x + 4, yb - h * .7 + i * h * .09); ctx.lineTo(x + w - 2, yb - h * .7 + i * h * .09); ctx.stroke(); }
    ctx.restore();
  };
  /** Le bloc de béton (gris, granuleux). */
  P.bloc = (ctx, x, yb, w, h) => {
    ctx.save(); P.ombre(ctx, () => { const g = ctx.createLinearGradient(x, yb - h, x + w, yb); g.addColorStop(0, '#d4d4d8'); g.addColorStop(.6, '#a1a1aa'); g.addColorStop(1, '#52525b'); ctx.fillStyle = g; ctx.fillRect(x, yb - h, w, h); }, 8);
    ctx.fillStyle = 'rgba(63,63,70,.35)'; for (let i = 0; i < 40; i++) { const px = x + ((i * 37) % 97) / 97 * w, py = yb - h + ((i * 53) % 89) / 89 * h; ctx.fillRect(px, py, 2, 2); }
    ctx.restore();
  };
  /** La grue : mât en treillis jaune, flèche horizontale, chariot ; renvoie le point du chariot. */
  P.grue = (ctx, x, yb, h, l) => {
    ctx.save(); ctx.strokeStyle = '#f59e0b'; ctx.lineWidth = 3;
    const w = 22;
    ctx.fillStyle = '#525252'; ctx.fillRect(x - w, yb - 8, w * 2, 8);
    ctx.beginPath(); ctx.moveTo(x - w / 2, yb - 8); ctx.lineTo(x - w / 2, yb - h); ctx.moveTo(x + w / 2, yb - 8); ctx.lineTo(x + w / 2, yb - h); ctx.stroke();
    ctx.lineWidth = 1.5; for (let yy = yb - 8; yy > yb - h; yy -= w) { ctx.beginPath(); ctx.moveTo(x - w / 2, yy); ctx.lineTo(x + w / 2, yy - w); ctx.moveTo(x - w / 2, yy - w); ctx.lineTo(x + w / 2, yy - w); ctx.stroke(); }
    ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(x - l * .25, yb - h); ctx.lineTo(x + l, yb - h); ctx.moveTo(x - l * .25, yb - h + 14); ctx.lineTo(x + l, yb - h + 14); ctx.stroke();
    ctx.lineWidth = 1.4; for (let xx = x - l * .25; xx < x + l; xx += 16) { ctx.beginPath(); ctx.moveTo(xx, yb - h); ctx.lineTo(xx + 16, yb - h + 14); ctx.stroke(); }
    ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(x, yb - h - 30); ctx.lineTo(x + l * .8, yb - h); ctx.moveTo(x, yb - h - 30); ctx.lineTo(x - l * .25, yb - h); ctx.stroke();
    ctx.fillStyle = '#525252'; ctx.fillRect(x - l * .25, yb - h + 14, 30, 22);
    ctx.fillStyle = '#334155'; ctx.fillRect(x + l * .72 - 10, yb - h + 14, 20, 8);
    ctx.restore();
    return [x + l * .72, yb - h + 22];
  };
  /** Le seau (métal galvanisé) avec son anse ; renvoie le point d'attache de la corde. */
  P.seau = (ctx, x, yb, w) => {
    const h = w * .9; ctx.save();
    P.ombre(ctx, () => { const g = ctx.createLinearGradient(x - w / 2, 0, x + w / 2, 0); g.addColorStop(0, '#64748b'); g.addColorStop(.4, '#e2e8f0'); g.addColorStop(1, '#475569'); ctx.fillStyle = g; ctx.beginPath(); ctx.moveTo(x - w / 2, yb - h); ctx.lineTo(x + w / 2, yb - h); ctx.lineTo(x + w * .38, yb); ctx.lineTo(x - w * .38, yb); ctx.closePath(); ctx.fill(); }, 6);
    ctx.fillStyle = '#38bdf8'; ctx.beginPath(); ctx.ellipse(x, yb - h, w / 2, w * .09, 0, 0, TAU); ctx.fill();
    ctx.strokeStyle = '#334155'; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(x, yb - h, w / 2, Math.PI, 0); ctx.stroke();
    ctx.restore();
    return [x, yb - h - w / 2];
  };
  /** Sphère, cylindre, disque homogènes (vus en perspective douce). */
  P.sphere = (ctx, x, y, r) => P.ombre(ctx, () => boule(ctx, x, y, r, '#e0f2fe', '#38bdf8', '#0c4a6e'), 10);
  P.cylindre = (ctx, x, y, r, h) => {
    ctx.save(); P.ombre(ctx, () => { const g = ctx.createLinearGradient(x - r, 0, x + r, 0); g.addColorStop(0, '#166534'); g.addColorStop(.4, '#86efac'); g.addColorStop(1, '#14532d'); ctx.fillStyle = g; ctx.fillRect(x - r, y - h / 2, 2 * r, h); ctx.beginPath(); ctx.ellipse(x, y + h / 2, r, r * .3, 0, 0, Math.PI); ctx.fill(); }, 8);
    ctx.fillStyle = '#bbf7d0'; ctx.beginPath(); ctx.ellipse(x, y - h / 2, r, r * .3, 0, 0, TAU); ctx.fill(); ctx.restore();
  };
  P.disque = (ctx, x, y, r) => {
    ctx.save(); P.ombre(ctx, () => { ctx.fillStyle = '#7c2d12'; ctx.beginPath(); ctx.ellipse(x, y + 6, r, r * .42, 0, 0, TAU); ctx.fill(); }, 8);
    const g = ctx.createRadialGradient(x - r * .3, y - r * .1, r * .1, x, y, r); g.addColorStop(0, '#fed7aa'); g.addColorStop(1, '#ea580c');
    ctx.fillStyle = g; ctx.beginPath(); ctx.ellipse(x, y, r, r * .42, 0, 0, TAU); ctx.fill(); ctx.restore();
  };
  /** Une masse (cylindre de laiton) vue de face, centrée en (x, y). */
  P.masse = (ctx, x, y, r, h) => {
    ctx.save(); P.ombre(ctx, () => { const g = ctx.createLinearGradient(x - r, 0, x + r, 0); g.addColorStop(0, '#78350f'); g.addColorStop(.4, '#fcd34d'); g.addColorStop(1, '#92400e'); ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(x - r, y - h / 2, 2 * r, h, 4); ctx.fill(); }, 7);
    ctx.restore();
  };
  /** Une barre métallique horizontale de x1 à x2. */
  P.barre = (ctx, x1, x2, y, e = 8) => { ctx.save(); const g = ctx.createLinearGradient(0, y - e / 2, 0, y + e / 2); g.addColorStop(0, '#e5e7eb'); g.addColorStop(.5, '#9ca3af'); g.addColorStop(1, '#4b5563'); ctx.fillStyle = g; ctx.fillRect(x1, y - e / 2, x2 - x1, e); ctx.restore(); };
  /** Le marteau : manche en bois de x1 à x2, tête en acier centrée en x2. */
  P.marteau = (ctx, x1, x2, y, e = 16, tete = [46, 90]) => {
    ctx.save(); P.ombre(ctx, () => { const g = ctx.createLinearGradient(0, y - e / 2, 0, y + e / 2); g.addColorStop(0, '#f2c48d'); g.addColorStop(.5, '#c2864a'); g.addColorStop(1, '#7c4a1e'); ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(x1, y - e / 2, x2 - x1, e, e / 2); ctx.fill(); }, 6);
    P.ombre(ctx, () => { const g = ctx.createLinearGradient(x2 - tete[0] / 2, 0, x2 + tete[0] / 2, 0); g.addColorStop(0, '#334155'); g.addColorStop(.45, '#e2e8f0'); g.addColorStop(1, '#1e293b'); ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(x2 - tete[0] / 2, y - tete[1] / 2, tete[0], tete[1], 6); ctx.fill(); }, 8);
    ctx.restore();
  };
  /** Le dynamomètre / crochet : un fil vertical (craie) se dessine dans la page. Le sol d'un puits : margelle de pierre. */
  P.margelle = (ctx, x, yb, w) => {
    ctx.save(); for (let i = 0; i < 6; i++) { const bx = x - w / 2 + i * w / 6; P.ombre(ctx, () => { const g = ctx.createLinearGradient(bx, yb - 30, bx, yb); g.addColorStop(0, '#d6d3d1'); g.addColorStop(1, '#78716c'); ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(bx + 1, yb - 30, w / 6 - 2, 30, 3); ctx.fill(); }, 4); }
    ctx.restore();
  };

  window.Mvt = { Scene, VW, VH, TAU, COUL, HEX, ME, ROLES, ECR, lueur, lignes, sim, vues, param, doux, P, panneau, vecteur, nomVecteur, texteV, graphique, arrondi };
})();
