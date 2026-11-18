/*
 * Récit pilotable du cours « Rôle du muscle strié squelettique » (18 novembre 2026, logique du cours) : la ligne de temps
 * (Chrono) et l'écriture à la craie au moment où la chose arrive (Apparitions), reprises telles quelles de
 * svt/reactions_responsables_liberation_energie-tableau/commun.js pour les pages nouvelles du chapitre (atpase.html,
 * national.html). Commandes du tuteur : start / pause / resume / reset / set_time / play_until {moment | time_s,
 * depuis, duree_s} ; bouton unique Lancer → Pause → Reprendre → Rejouer ; ?depart=<moment> ouvre la page figée.
 */
(function () {
  'use strict';
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

  /* Interpolation douce. */
  const doux = (u) => (u <= 0 ? 0 : u >= 1 ? 1 : u * u * (3 - 2 * u));
  const mix = (a, b, u) => a + (b - a) * u;

  window.MuscleRecit = { Chrono, Apparitions, fr, doux, mix };
})();
