/*
 * Commun aux simulations du cours SVT « Libération de l'énergie emmagasinée dans la matière organique »
 * (2ᵉ Bac PC BIOF, 10 novembre 2026). Repris de physics/ondes-periodiques-tableau/commun.js :
 *   - Scene : cadre virtuel 760 × 420 mis à l'échelle sans rien couper, texte jamais plus petit que 11 px à l'écran,
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
 */
(function () {
  'use strict';
  const VW = 760, VH = 420;
  function Scene(canvas, dessiner) {
    const scene = { sale: true };
    const craie = new window.Tableau.Craie(canvas, { onresize: () => { scene.sale = true; } });
    Object.assign(scene, {
      craie, sale: true, ouvert: performance.now(), s: 1, ox: 0, oy: 0,
      cadre(graine = 7) {
        const W = craie.W, H = craie.H;
        craie.debut(graine, (performance.now() - scene.ouvert) / 1000);
        const s = Math.min(W / VW, H / VH);
        scene.s = s; scene.ox = (W - VW * s) / 2; scene.oy = (H - VH * s) / 2;
        craie.ctx.translate(scene.ox, scene.oy); craie.ctx.scale(s, s);
        craie.echelle = s; craie.tailleMin = 11;
        craie.cadre = { w: VW, h: VH, haut: 0 };
        return craie;
      },
      local(x, y) { return [(x - scene.ox) / scene.s, (y - scene.oy) / scene.s]; },
      reecrire() { scene.ouvert = performance.now(); scene.sale = true; },
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

  const fr = (v, d = 1) => (Number.isFinite(v) ? v.toFixed(d).replace('.', ',') : '—');

  /* Ligne de temps pilotable par le tuteur. Toutes les durées en secondes de la scène. */
  function Chrono(o) {
    const C = { t: 0, running: false, jusqua: null, motif: '', fait: false, emis: 0 };
    const pont = () => (o.pont ? o.pont() : null);
    const noter = (a, d) => { const p = pont(); if (p) { p.noter(a, d); p.emettre(); } };
    const texteBouton = (s) => { if (o.bouton) o.bouton.textContent = s; };
    const dire = (s, kind) => { if (o.bulle && s) window.Tableau.bulle(o.bulle, s, kind); };
    const fin = () => o.fin();
    C.avancer = (dt) => {
      if (!C.running) return false;
      C.t = Math.min(fin(), C.t + dt * (o.vitesse || 1));
      if (C.jusqua != null && C.t >= C.jusqua) {
        C.t = C.jusqua; C.running = false; C.jusqua = null; texteBouton('Reprendre');
        dire('Arrêt sur image : ' + (C.motif || `t = ${fr(C.t)} s`) + '.');
        noter('pause', { time_s: +C.t.toFixed(2) });
        o.apres && o.apres();
        return true;
      }
      if (C.t >= fin()) { C.running = false; C.fait = true; texteBouton('Rejouer'); dire(o.fini ? o.fini() : 'Terminé.', 'good'); noter('fin', {}); o.apres && o.apres(); }
      else if (performance.now() - C.emis > 500) { C.emis = performance.now(); const p = pont(); p && p.emettre(); }
      return true;
    };
    C.start = () => { C.jusqua = null; C.t = 0; C.running = true; C.fait = false; texteBouton('Pause'); dire(o.depart || 'Observe…'); o.reinit && o.reinit(); noter('start', {}); };
    C.pause = () => { if (!C.running) return; C.running = false; C.jusqua = null; texteBouton('Reprendre'); dire('Arrêt sur image.'); noter('pause', { time_s: +C.t.toFixed(2) }); };
    C.resume = () => { if (C.running) return; if (C.fait || C.t >= fin()) return C.start(); C.running = true; texteBouton('Pause'); dire('Observe…'); noter('resume', {}); };
    C.setTime = (p) => {
      const t = +p.time_s; if (!Number.isFinite(t)) return;
      C.running = false; C.jusqua = null; C.t = Math.min(fin(), Math.max(0, t)); C.fait = C.t >= fin();
      texteBouton(C.fait ? 'Rejouer' : 'Reprendre'); dire(`Arrêt sur image : t = ${fr(C.t)} s.`); noter('set_time', { time_s: C.t });
    };
    /* Rejoue (depuis zéro si l'instant est passé) et se fige sur l'instant nommé. */
    C.playUntil = (p) => {
      const M = o.moments(), nom = p && p.moment in M ? p.moment : null, cible = nom ? M[nom] : +(p && p.time_s);
      if (!Number.isFinite(cible)) return;
      if (C.fait || C.t >= cible - 1e-3) { C.t = 0; o.reinit && o.reinit(); }
      C.jusqua = Math.min(fin(), Math.max(0.001, cible)); C.motif = nom ? ((o.motifs || {})[nom] || nom) : '';
      C.running = true; C.fait = false; texteBouton('Pause'); dire('Observe…');
      noter('play_until', { moment: nom, time_s: C.jusqua });
    };
    C.clic = () => (C.running ? C.pause() : (C.t > 0 && C.t < fin() && !C.fait ? C.resume() : C.start()));
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
  function Apparitions(scene) {
    const APP = {};
    const maintenant = () => (performance.now() - scene.ouvert) / 1000;
    return {
      ecrire(c, cle, fn) {
        if (!(cle in APP)) APP[cle] = maintenant();
        const cur = c.cur; c.depuis(APP[cle]); try { fn(); } finally { c.cur = cur; }
      },
      oublier() { for (const k of Object.keys(APP)) delete APP[k]; scene.sale = true; },
      APP,
    };
  }

  /* Interpolation douce. */
  const doux = (u) => (u <= 0 ? 0 : u >= 1 ? 1 : u * u * (3 - 2 * u));
  const mix = (a, b, u) => a + (b - a) * u;

  window.SVTTableau = { Scene, Chrono, Apparitions, VW, VH, fr, doux, mix };
})();
