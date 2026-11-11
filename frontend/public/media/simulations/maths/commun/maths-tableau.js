/*
 * MathsTableau — kit commun des constructions de mathématiques « au tableau » (2ᵉ Bac PC BIOF, 10 novembre 2026).
 *
 * En maths, la « simulation » est une construction à la craie qui s'écrit pas à pas, comme un professeur :
 * repère, courbe tracée en direct, point qui glisse, pointillés de projection, tangente, asymptote, escalier d'une suite,
 * lignes d'un calcul… Chaque page déclare ses VUES (?vue=…) ; chaque vue est une fonction de dessin qui suit l'horloge
 * de la scène (S.tw) et marque ses MOMENTS nommés (`K.marque('nom')`) : le tuteur fige la construction sur un moment
 * (`play_until {moment}`), sur un instant (`set_time {time_s}`), change un paramètre (`set_parameters`), montre un repère
 * (`highlight {target}`, ajouté par le kit). L'élève glisse les poignées dessinées (pas de curseurs).
 *
 * Chargement :  tableau.js (kit commun) → exposants.js → maths-tableau.js, puis la page :
 *   MathsTableau.page({
 *     id: 'lc_traversee', titre: 'Le théorème des valeurs intermédiaires',
 *     texte: 'description pour le tuteur',
 *     vues: {
 *       une: {
 *         titre: 'Une courbe continue qui traverse l’axe',
 *         params: { a: { min: -1, max: 1, pas: 0.1, defaut: 0 } },        // réglables (set_parameters, poignées)
 *         dessiner(c, K) { … K.marque('courbe_tracee') … },               // c = la craie (Tableau.Craie), K = l'aide
 *         decrire: { courbe_tracee: 'phrase de ce qui se voit après ce moment', … },   // ou (K) => ({…})
 *         poignees(K) { return [{ id: 'a', x, y, bouger: (x, y) => ({ a: … }) }]; },  // coordonnées du dessin
 *         lecture(K) { return 'f(a) = …' },                                // une phrase sur les valeurs actuelles (facultatif)
 *       },
 *     },
 *   });
 *
 * Aide K (dans dessiner) :
 *   K.P                         paramètres courants ;  K.vu('nom') : le moment est-il atteint ?
 *   K.marque('nom')             le moment « nom » = l'instant d'écriture courant (la craie a fini ce qui précède)
 *   K.anime(duree, p => …)      réserve `duree` s dans l'écriture ; appelle la fonction avec p de 0 à 1 (dessin direct) :
 *                               un point qui glisse, une courbe qui avance ; figée après, p = 1
 *   K.axes({x0,y0,w,h,xmin,xmax,ymin,ymax,gx,gy,nomx,nomy}) → G : G.X(x), G.Y(y), G.inv(px,py) ; trace le repère
 *   K.grille({…}) / MathsTableau.grille({…})  le même G sans rien dessiner (pour les poignées)
 *   K.courbe(G, f, a, b, o)     trace y = f(x) entre a et b (coupée hors du cadre et aux sauts) ; o.couleur, o.largeur
 *   K.courbePart(G, f, a, b, p, o)  la même, tracée jusqu'à la fraction p (dans K.anime)
 *   K.proj(G, x, y, o)          pointillés de (x ; y) vers les deux axes, avec les libellés o.lx, o.ly
 *   K.rond(G, x, y, plein, couleur)  point plein ou rond vide (borne exclue, trou)
 *   K.lignes(x, y, [ {t, couleur, taille, moment, dx} ], interligne)  lignes d'un calcul écrites l'une après l'autre ;
 *                               une ligne avec `moment` marque ce moment juste après elle
 *   K.titre('texte')            titre de la vue en haut à gauche
 *   K.fr(v, d)                  nombre à la française (virgule), sans zéros inutiles
 */
(function () {
  'use strict';
  const T = window.Tableau;
  const VW = 760, VH = 420;
  const $ = (id) => document.getElementById(id);

  /* Scène : même cadre que les ondes (760 × 420 mis à l'échelle, rien de coupé) ; boucle d'image à la demande. */
  function Scene(canvas, dessiner) {
    const scene = { sale: true };
    const craie = new T.Craie(canvas, { onresize: () => { scene.sale = true; } });
    Object.assign(scene, {
      craie, ouvert: performance.now(), s: 1, ox: 0, oy: 0, horloge: null,
      cadre(graine = 7) {
        const W = craie.W, H = craie.H;
        craie.debut(graine, scene.horloge ? scene.horloge() : (performance.now() - scene.ouvert) / 1000);
        const s = Math.min(W / VW, H / VH);
        scene.s = s; scene.ox = (W - VW * s) / 2; scene.oy = (H - VH * s) / 2;
        craie.ctx.translate(scene.ox, scene.oy); craie.ctx.scale(s, s);
        craie.echelle = s; craie.tailleMin = 11; craie.cadre = { w: VW, h: VH, haut: 0 };
        return craie;
      },
      local(x, y) { return [(x - scene.ox) / scene.s, (y - scene.oy) / scene.s]; },
      reecrire() { scene.ouvert = performance.now(); scene.sale = true; },
      image() {
        const h = scene.horloge, t = scene.ouvert; scene.horloge = null; scene.ouvert = -1e9;
        try { dessiner(craie, scene); return canvas.toDataURL('image/png'); } finally { scene.horloge = h; scene.ouvert = t; scene.sale = true; }
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

  const fr = (v, d = 2) => {
    if (!Number.isFinite(v)) return v > 0 ? '+∞' : v < 0 ? '−∞' : '—';
    let s = (+v.toFixed(d)).toString();
    return s.replace('-', '−').replace('.', ',');
  };

  /* Un repère sans dessin : G.X(x), G.Y(y), G.inv(px, py) (pour les poignées). */
  function grille(o) {
    const g = { x0: 60, y0: 60, w: 420, h: 300, xmin: -1, xmax: 5, ymin: -2, ymax: 6, nomx: 'x', nomy: 'y', ...o };
    g.X = (x) => g.x0 + (x - g.xmin) / (g.xmax - g.xmin) * g.w;
    g.Y = (y) => g.y0 + g.h - (y - g.ymin) / (g.ymax - g.ymin) * g.h;
    g.inv = (px, py) => [g.xmin + (px - g.x0) / g.w * (g.xmax - g.xmin), g.ymin + (g.y0 + g.h - py) / g.h * (g.ymax - g.ymin)];
    return g;
  }

  /* L'aide K, refaite à chaque image. */
  function aide(c, S, M) {
    const K = {
      P: S.P, c, fr,
      vu: (nom) => M[nom] !== undefined && S.tw >= M[nom] - 1e-6,
      marque: (nom) => { S._MM[nom] = c.cur; },
      anime(duree, fn) {
        const t = c.t, debut = c.cur;
        let p = 1;
        if (Number.isFinite(t)) { c.cur += duree; p = t <= debut ? 0 : Math.min(1, (t - debut) / duree); if (p < 1) c.complet = false; }
        if (p > 0) c.direct(() => fn(p));
        return p;
      },
      titre(s) { c.texte(s, 20, 30, { couleur: 'cyan', taille: 20, max: 720 }); return K; },
      grille,
      axes(o) {
        const g = grille(o);
        const ax = Math.min(Math.max(0, g.ymin), g.ymax), ay = Math.min(Math.max(0, g.xmin), g.xmax);
        const yA = g.Y(ax), xA = g.X(ay);
        if (g.quadrillage) for (let x = Math.ceil(g.xmin); x <= g.xmax; x++) c.ligne(g.X(x), g.y0, g.X(x), g.y0 + g.h, { couleur: 'tresfaible', largeur: .8, duree: .02 });
        c.fleche(g.x0 - 6, yA, g.x0 + g.w + 14, yA, { couleur: 'faible', largeur: 1.6 });
        c.fleche(xA, g.y0 + g.h + 6, xA, g.y0 - 14, { couleur: 'faible', largeur: 1.6 });
        c.texte(g.nomx, g.x0 + g.w + 18, yA + 18, { couleur: 'faible', taille: 16 });
        c.texte(g.nomy, xA - 18, g.y0 - 6, { couleur: 'faible', taille: 16 });
        for (const v of g.gx || []) { const [x, l] = Array.isArray(v) ? v : [v, fr(v)]; c.ligne(g.X(x), yA - 4, g.X(x), yA + 4, { couleur: 'faible', largeur: 1.2, duree: .02 }); if (l !== '') c.texte(l, g.X(x), yA + 19, { couleur: 'faible', taille: 14, align: 'center', duree: .05 }); }
        for (const v of g.gy || []) { const [y, l] = Array.isArray(v) ? v : [v, fr(v)]; c.ligne(xA - 4, g.Y(y), xA + 4, g.Y(y), { couleur: 'faible', largeur: 1.2, duree: .02 }); if (l !== '') c.texte(l, xA - 8, g.Y(y) + 5, { couleur: 'faible', taille: 14, align: 'right', duree: .05 }); }
        if (g.origine !== false && g.xmin < 0 && g.ymin < 0) c.texte('O', xA - 14, yA + 17, { couleur: 'faible', taille: 14 });
        return g;
      },
      _points(G, f, a, b, n) {
        const morceaux = [[]]; const ymarge = (G.ymax - G.ymin) * .06;
        let prec = null;
        for (let i = 0; i <= n; i++) {
          const x = a + (b - a) * i / n, y = f(x);
          const dedans = Number.isFinite(y) && y >= G.ymin - ymarge && y <= G.ymax + ymarge;
          const saut = prec !== null && Number.isFinite(y) && Math.abs(G.Y(y) - G.Y(prec)) > G.h * .45;
          if (!dedans || saut) { if (morceaux[morceaux.length - 1].length) morceaux.push([]); if (!dedans) { prec = null; continue; } }
          morceaux[morceaux.length - 1].push([G.X(x), G.Y(Math.min(G.ymax + ymarge, Math.max(G.ymin - ymarge, y)))]);
          prec = y;
        }
        return morceaux.filter((m) => m.length > 1);
      },
      courbe(G, f, a, b, o = {}) {
        for (const m of K._points(G, f, a, b, o.n || 160)) c.trait(m, { tremble: .35, couleur: o.couleur || 'cyan', largeur: o.largeur ?? 2.6, pointille: o.pointille, duree: o.duree });
        return K;
      },
      courbePart(G, f, a, b, p, o = {}) {
        if (p <= 0) return K;
        const bb = a + (b - a) * p;
        for (const m of K._points(G, f, a, bb, Math.max(4, Math.round((o.n || 160) * p)))) c.trait(m, { tremble: .35, couleur: o.couleur || 'cyan', largeur: o.largeur ?? 2.6, pointille: o.pointille });
        return K;
      },
      proj(G, x, y, o = {}) {
        const ax = Math.min(Math.max(0, G.ymin), G.ymax), ay = Math.min(Math.max(0, G.xmin), G.xmax);
        const coul = o.couleur || 'faible';
        if (o.versX !== false) c.ligne(G.X(x), G.Y(y), G.X(x), G.Y(ax), { couleur: coul, largeur: 1.3, pointille: [5, 5] });
        if (o.versY !== false) c.ligne(G.X(x), G.Y(y), G.X(ay), G.Y(y), { couleur: coul, largeur: 1.3, pointille: [5, 5] });
        if (o.lx) c.texte(o.lx, G.X(x), G.Y(ax) + (y < ax ? -10 : 20), { couleur: o.couleurTexte || coul, taille: o.taille || 15, align: 'center' });
        if (o.ly) c.texte(o.ly, G.X(ay) - 8, G.Y(y) + 5, { couleur: o.couleurTexte || coul, taille: o.taille || 15, align: 'right' });
        return K;
      },
      rond(G, x, y, plein = true, couleur = 'jaune') {
        const px = G.X(x), py = G.Y(y);
        if (plein) c.point(px, py, 5, couleur); else c.cercle(px, py, 5.5, { couleur, largeur: 2 });
        return K;
      },
      lignes(x, y, liste, inter = 30) {
        for (const l of liste) {
          if (l.pause) c.pause(l.pause);
          if (l.t) c.texte(l.t, x + (l.dx || 0), y, { couleur: l.couleur || 'blanc', taille: l.taille || 19, max: l.max || (VW - x - 16) });
          if (l.cadre) { const w = c.largeurTexte(l.t, l.taille || 19) + 16; c.rect(x + (l.dx || 0) - 8, y - (l.taille || 19) - 2, w, (l.taille || 19) + 12, { couleur: l.cadre, arrondi: 6, largeur: 1.4 }); }
          if (l.repere) c.repere(l.repere, x + (l.dx || 0) - 4, y - 22, Math.min(VW - x - 10, c.largeurTexte(l.t || '', l.taille || 19) + 10), 30, l.label || l.t);
          if (l.moment) K.marque(l.moment);
          y += l.inter ?? inter;
        }
        return y;
      },
    };
    return K;
  }

  function page(def) {
    const P0 = new URLSearchParams(location.search);
    const noms = Object.keys(def.vues);
    const vue = def.vues[P0.get('vue')] ? P0.get('vue') : (def.defaut || noms[0]);
    const V = def.vues[vue];
    const VITESSE = def.vitesse || 1.5;
    const params0 = {};
    for (const [k, p] of Object.entries(V.params || {})) { const u = P0.get(k); params0[k] = u !== null && Number.isFinite(+u.replace(',', '.')) ? +u.replace(',', '.') : p.defaut; }
    const S = { tw: 0, running: true, pause: false, fait: false, jusqua: null, motif: '', emis: 0, P: { ...params0 }, _MM: {}, glisse: null };
    let M = {};

    document.body.insertAdjacentHTML('afterbegin', '');
    const canvas = $('canvas');
    const scene = Scene(canvas, dessiner);
    scene.horloge = () => S.tw;
    const craie = scene.craie;

    function dessiner(c) {
      scene.cadre(def.graine || 23);
      S._MM = {};
      const K = aide(c, S, M);
      V.dessiner(c, K);
      M = S._MM;
      if (M.fin === undefined) M.fin = c.cur;
      return c.fin() || !S.running;
    }
    const etapes = () => Object.keys(M).sort((a, b) => M[a] - M[b]);
    const etiquette = () => { $('run').textContent = S.running ? 'Pause' : S.pause ? 'Reprendre' : 'Réécrire'; };
    const descr = () => (typeof V.decrire === 'function' ? V.decrire(aide(craie, S, M)) : V.decrire) || {};
    function ceQuiSeVoit() {
      const D = descr(), faites = etapes().filter((n) => S.tw >= M[n] - 1e-6 || S.fait);
      const m = [`${def.titre} — ${V.titre}.`];
      if (!faites.length) m.push(S.running ? 'La construction commence à s’écrire à la craie.' : 'Rien d’écrit encore.');
      for (const n of faites) if (D[n]) m.push(D[n]);
      if (V.lecture) m.push(V.lecture(aide(craie, S, M)));
      if (V.params && Object.keys(V.params).length) m.push('Réglages : ' + Object.entries(S.P).map(([k, v]) => `${k} = ${fr(v, 3)}`).join(', ') + '.');
      m.push(S.running ? 'La craie écrit encore.' : S.pause ? `Arrêt sur image : ${S.motif || (faites.length ? faites[faites.length - 1] : 'début')}.` : 'Construction complète.');
      return m.join(' ');
    }
    scene.avancer = (dt) => {
      if (!S.running) return false;
      S.tw += dt * VITESSE;
      if (S.jusqua != null && S.tw >= S.jusqua) {
        S.tw = S.jusqua; S.jusqua = null; S.running = false;
        if (S.tw >= M.fin - 1e-6) { S.pause = false; S.fait = true; etiquette(); T.bulle($('feedback'), V.finale || 'Construction complète.'); pont.noter('measurement', { vue }); pont.emettre(); return true; }
        S.pause = true; etiquette();
        T.bulle($('feedback'), 'Arrêt sur image : ' + (S.motif || 'instant choisi') + '.'); pont.noter('pause', { moment: S.motif }); pont.emettre();
        return true;
      }
      if (M.fin !== undefined && S.tw >= M.fin + 0.05) {
        S.running = false; S.pause = false; S.fait = true; etiquette(); if (V.finale) T.bulle($('feedback'), V.finale); pont.noter('measurement', { vue }); pont.emettre();
      } else if (performance.now() - S.emis > 500) { S.emis = performance.now(); pont.emettre(); }
      return true;
    };
    function calculer() { const t = S.tw, r = S.running; S.tw = 1e6; dessiner(craie); S.tw = t; S.running = r; scene.sale = true; }
    function start() { S.tw = 0; S.jusqua = null; S.motif = ''; S.running = true; S.pause = false; S.fait = false; etiquette(); T.bulle($('feedback'), ''); pont.noter('start', { vue }); pont.emettre(); }
    function reset() { S.P = { ...params0 }; start(); }
    function pause() { if (!S.running) return; S.running = false; S.pause = true; S.jusqua = null; etiquette(); pont.noter('pause'); pont.emettre(); }
    function resume() { if (S.running) return; if (!S.pause) return start(); S.running = true; S.pause = false; etiquette(); pont.noter('resume'); pont.emettre(); }
    function playUntil(p) {
      calculer();
      const nom = p.moment in M ? p.moment : null, cible = nom ? M[nom] : +p.time_s;
      if (!Number.isFinite(cible)) return;
      if (S.fait || !(S.running || S.pause) || S.tw >= cible - 1e-3) { S.tw = 0; S.fait = false; }
      S.jusqua = cible; S.motif = nom ? ((V.motifs || {})[nom] || nom.replace(/_/g, ' ')) : `t = ${fr(cible, 1)} s`;
      S.running = true; S.pause = false; etiquette(); T.bulle($('feedback'), '');
      pont.noter('play_until', { moment: nom }); pont.emettre();
    }
    function setTime(p) {
      calculer(); const t = +p.time_s; if (!Number.isFinite(t)) return;
      S.tw = Math.max(0, Math.min(t, M.fin)); S.running = false; S.pause = S.tw < M.fin; S.fait = !S.pause; S.jusqua = null; etiquette(); scene.sale = true;
      pont.noter('set_time', { time_s: t }); pont.emettre();
    }
    function borne(k, v) { const d = (V.params || {})[k]; if (!d) return null; v = Math.min(d.max, Math.max(d.min, +v)); if (d.pas) v = Math.round((v - d.min) / d.pas) * d.pas + d.min; return +v.toFixed(6); }
    function setParameters(p, par) {
      let change = false;
      for (const [k, v] of Object.entries(p || {})) { const b = borne(k, v); if (b !== null && Number.isFinite(b) && b !== S.P[k]) { S.P[k] = b; change = true; } }
      if (!change) return;
      calculer();
      if (S.fait) S.tw = M.fin;     // construction finie : elle reste entière, avec les nouvelles valeurs
      scene.sale = true; pont.noter('set_parameters', { ...S.P, par }); pont.emettre();
    }
    $('run').onclick = () => (S.running ? pause() : S.pause ? resume() : start());

    // Poignées : l'élève glisse un point du dessin (pas de curseur).
    if (V.poignees) {
      T.glisser(canvas, {
        toucher(x, y) {
          const [lx, ly] = scene.local(x, y);
          const hs = V.poignees(aide(craie, S, M)) || [];
          const h = hs.find((q) => Math.hypot(q.x - lx, q.y - ly) < 18);
          return h ? h.id : null;
        },
        bouger(id, x, y) {
          const [lx, ly] = scene.local(x, y);
          const h = (V.poignees(aide(craie, S, M)) || []).find((q) => q.id === id); if (!h) return;
          const nv = h.bouger(lx, ly) || {};
          if (!S.fait) { S.tw = 1e6; S.running = false; S.pause = false; S.fait = true; etiquette(); }
          for (const [k, v] of Object.entries(nv)) { const b = borne(k, v); if (b !== null) S.P[k] = b; }
          calculer(); S.tw = M.fin; scene.sale = true;
        },
        lacher() { pont.noter('set_parameters', { ...S.P }); T.bulle($('feedback'), V.lecture ? V.lecture(aide(craie, S, M)) : 'Nouveau réglage.'); pont.emettre(); },
      });
    }

    const commandes = ['start', 'reset', 'pause', 'resume', 'play_until', 'set_time'].concat(V.params && Object.keys(V.params).length ? ['set_parameters'] : []);
    const schema = { play_until: { moment: '(moments de la vue, voir state.moments) — réécrit la construction et s’arrête sur ce moment' }, set_time: { time_s: '0..durée de l’écriture' } };
    if (V.params) schema.set_parameters = Object.fromEntries(Object.entries(V.params).map(([k, d]) => [k, `${d.min}..${d.max}` + (d.pas ? ` (pas ${d.pas})` : '') + (d.sens ? ' : ' + d.sens : '')]));
    const config = { id: def.id + '_' + vue, version: '1.0', title: def.titre + ' — ' + V.titre, variants: noms.map((n) => ({ id: n, label: def.vues[n].titre })), commands: commandes, command_schema: schema };
    if (V.explication) T.explication({ [vue]: V.explication });
    const pont = T.protocole({ id: config.id, commandes, config,
      texte: `${def.texte || def.titre}. Vue « ${vue} » : ${V.titre}.` + (V.texte ? ' ' + V.texte : ''),
      etat: () => ({ simulation_status: S.running ? 'running' : S.pause ? 'paused' : 'finished', ce_qui_se_voit: ceQuiSeVoit(), current_variant: vue,
        parameters: { ...S.P }, time_s: +S.tw.toFixed(2), moments: Object.fromEntries(etapes().map((n) => [n, +M[n].toFixed(2)])),
        moments_atteints: etapes().filter((n) => S.tw >= M[n] - 1e-6) }),
      progression: () => (S.fait ? 1 : M.fin ? Math.min(1, S.tw / M.fin) : 0),
      executer: (cmd, p) => ({ start, reset, pause, resume, play_until: () => playUntil(p), set_time: () => setTime(p), set_parameters: () => setParameters(p, 'tuteur') })[cmd]?.() });
    etiquette();
    window.__maths = { S, get M() { return M; }, scene, vue, def };
    return { S, scene, pont };
  }

  window.MathsTableau = { Scene, page, fr, grille, VW, VH };
  window.OndesTableau = window.OndesTableau || { Scene, VW, VH };   // bilan.html / carte.html du kit des ondes s'y appuient
})();
