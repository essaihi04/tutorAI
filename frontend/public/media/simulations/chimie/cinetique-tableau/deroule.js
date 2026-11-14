/*
 * Petites manips à la craie (14 novembre 2026, professeur règle 28) : un déroulé en étapes nommées, un bouton, un ou deux curseurs.
 * Chargé APRÈS tableau.js, commun.js et exposants.js. Copie identique dans les dossiers chimie/cinetique-tableau,
 * transformations-deux-sens-tableau, etat-equilibre-tableau et acides-bases-tableau.
 *
 *   Formules chimiques : « H₃O⁺ », « SO₄²⁻ » écrits avec indices et charges à la craie (notation « _{3} » et « ^{+} » du kit).
 *   Deroule(o) : o.etapes() → [{nom, duree, motif, bulle?}] ; o.dessiner(c, D) ; o.voir(D) ; o.params() ; o.appliquer(p) → bool ;
 *                o.depart, o.messageFin, o.texte, o.id, o.titre, o.schema, o.explication, o.variante (?vue=).
 *   Le tuteur : play_until {moment} (joue jusqu'à la fin de cette étape et s'y fige ; une étape déjà montrée ne rejoue pas),
 *   set_parameters (le curseur, sans rembobiner), set_time {time_s}, start, pause, resume, reset, highlight {target}.
 *   D.p(nom) : part jouée de l'étape (0 → 1) ; D.vu(nom) ; D.commence(nom) ; D.ecrire(c, nom) : ce qui suit s'écrit à la craie
 *   à partir du moment où l'étape a commencé (d'un coup si on y a sauté).
 */
(function () {
  'use strict';
  const T = window.Tableau;
  /* ── Formules chimiques : indices ₂ et charges ⁺ ⁻ ²⁻ (copie de transformations-deux-sens-tableau/avancement.html) ── */
  if (!T.Craie.__chim) {
    const C = T.Craie, P = C.prototype, texteAvant = P.texte, segAvant = C.segments;
    const SUP = { '⁺': '+', '⁻': '−', '⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4', '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9' };
    const SUB = { '₀': '0', '₁': '1', '₂': '2', '₃': '3', '₄': '4', '₅': '5', '₆': '6', '₇': '7', '₈': '8', '₉': '9' };
    const chim = s => String(s).replace(/[⁺⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+/g, g => '^{' + [...g].map(ch => SUP[ch]).join('') + '}')
      .replace(/[₀₁₂₃₄₅₆₇₈₉]+/g, g => '_{' + [...g].map(ch => SUB[ch]).join('') + '}');
    C.segments = function (s) {
      const out = [], re = /_\{([^}]+)\}/g; let i = 0, m;
      while ((m = re.exec(s))) { if (m.index > i) out.push(...segAvant(s.slice(i, m.index))); out.push({ t: m[1], sub: true }); i = re.lastIndex; }
      if (i < s.length) out.push(...segAvant(s.slice(i)));
      return out;
    };
    P.texte = function (s, x, y, o) { return texteAvant.call(this, chim(s), x, y, o); };
    C.__chim = true; window.chim = chim;
  }

  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
  const ECRITURE = 2.5;   // la craie écrit 2,5 fois plus vite que le kit par défaut
  /** « 3,9·10⁻⁴ » : mantisse à `d` décimales et puissance de dix en exposant. */
  function sci(v, d = 1) {
    if (!(v > 0)) return '0';
    let e = Math.floor(Math.log10(v)), m = v / 10 ** e;
    if (+m.toFixed(d) >= 10) { m /= 10; e += 1; }
    if (e === 0) return T.fr(m, d);
    const exp = String(e).replace('-', '⁻').replace(/\d/g, ch => '⁰¹²³⁴⁵⁶⁷⁸⁹'[ch]);
    return `${T.fr(m, d)}·10${exp}`;
  }

  function Deroule(o) {
    const $ = id => document.getElementById(id);
    const q = new URLSearchParams(location.search);
    const S = { vue: o.vues && o.vues.includes(q.get('vue')) ? q.get('vue') : (o.vues ? o.vues[0] : ''), t: 0, running: false, pause: false,
      fait: false, jusqua: null, motif: '', apparu: {}, emis: 0, dit: '' };
    let ET = [], FIN = 0, MOM = {};
    function construire() {
      let s = 0;
      ET = o.etapes(S.vue).map(e => { const d = { ...e, debut: s, fin: s + e.duree }; s = d.fin; return d; });
      FIN = s; MOM = Object.fromEntries(ET.map(e => [e.nom, e.fin])); MOM.fin = FIN;
    }
    construire();
    const ev = nom => ET.find(e => e.nom === nom);
    let scene = null, pont = null;
    const tc = () => (performance.now() - scene.ouvert) / 1000 * ECRITURE;
    const D = {
      S, sci, clamp,
      p(nom) { const e = ev(nom); return e ? clamp((S.t - e.debut) / e.duree, 0, 1) : 0; },
      vu(nom) { const e = ev(nom); return !!e && S.t >= e.fin - 1e-6; },
      commence(nom) { const e = ev(nom); return !!e && S.t > e.debut + 1e-6; },
      ecrire(c, nom) { const a = S.apparu[nom]; if (a != null) c.depuis(a); return c; },
      moments: () => ({ ...MOM }),
    };
    const dire = (texte, kind = '') => { S.dit = texte; T.bulle($('feedback'), texte, kind); };
    const etiquette = () => { $('run').textContent = S.running ? 'Pause' : S.pause ? 'Reprendre' : S.fait ? 'Rejouer' : (o.bouton || 'Lancer'); };
    const emettre = () => pont && pont.emettre();
    const noter = (a, d) => pont && pont.noter(a, d);
    scene = window.OndesTableau.Scene($('canvas'), c => o.dessiner(c, D));
    const cadreBase = scene.cadre;
    scene.cadre = function (g) { const k = cadreBase.call(scene, g); if (Number.isFinite(k.t)) k.t *= ECRITURE; return k; };
    D.scene = scene;
    function finir() { S.t = FIN; S.running = false; S.pause = false; S.fait = true; S.jusqua = null; etiquette(); dire(o.messageFin(D), 'good'); noter('finished', o.params()); emettre(); }
    scene.avancer = dt => {
      if (!S.running) return !!(o.anime && o.anime(D));
      const avant = S.t; S.t = Math.min(FIN, S.t + dt);
      for (const e of ET) if (avant <= e.debut + 1e-9 && S.t > e.debut) { S.apparu[e.nom] = tc(); if (e.bulle) dire(e.bulle(D)); }
      if (S.jusqua != null && S.t >= S.jusqua - 1e-9) {
        S.t = S.jusqua; S.jusqua = null;
        if (S.t >= FIN - 1e-9) { finir(); return true; }
        S.running = false; S.pause = true; etiquette(); dire('Arrêt sur image : ' + (S.motif || 'instant choisi') + '.');
        noter('pause', { time_s: +S.t.toFixed(2) }); emettre(); return true;
      }
      if (S.t >= FIN - 1e-9) { finir(); return true; }
      if (performance.now() - S.emis > 500) { S.emis = performance.now(); emettre(); }
      return true;
    };
    function start() { S.t = 0; S.apparu = {}; S.jusqua = null; S.motif = ''; S.running = true; S.pause = false; S.fait = false; etiquette(); dire(o.depart(D)); noter('start', o.params()); emettre(); }
    function pause() { if (!S.running) return; S.running = false; S.pause = true; etiquette(); dire('Arrêt sur image.'); noter('pause', { time_s: +S.t.toFixed(2) }); emettre(); }
    function resume() { if (S.running) return; if (!S.pause) return start(); S.running = true; S.pause = false; etiquette(); noter('resume'); emettre(); }
    function reset() { S.t = 0; S.apparu = {}; S.jusqua = null; S.running = false; S.pause = false; S.fait = false; scene.reecrire(); etiquette(); dire(o.accueil ? o.accueil(D) : o.depart(D)); noter('reset'); emettre(); }
    function setTime(p) {
      const t = +p.time_s; if (!Number.isFinite(t)) return;
      S.running = false; S.jusqua = null; S.t = clamp(t, 0, FIN); S.fait = S.t >= FIN - 1e-6; S.pause = !S.fait && S.t > 0;
      for (const e of ET) if (e.debut >= S.t) delete S.apparu[e.nom];
      etiquette(); scene.sale = true; noter('set_time', { time_s: S.t }); emettre();
    }
    function playUntil(p) {
      const nom = p && p.moment in MOM ? p.moment : null, cible = nom ? MOM[nom] : +(p && p.time_s);
      if (!Number.isFinite(cible)) { dire(`Moment inconnu : ${p && p.moment}.`, 'bad'); emettre(); return; }
      S.motif = nom ? ((ev(nom) && ev(nom).motif) || (nom === 'fin' ? 'tout est montré' : nom)) : '';
      if (S.fait || S.t >= cible - 1e-3) { scene.sale = true; if (nom) dire('On regarde : ' + S.motif + '.'); noter('play_until', { moment: nom, deja: true }); emettre(); return; }
      S.jusqua = cible; S.running = true; S.pause = false; etiquette();
      noter('play_until', { moment: nom, time_s: +cible.toFixed(2) }); emettre();
    }
    function setParameters(p) {
      if (!o.appliquer(p || {}, D)) return;
      scene.sale = true; noter('set_parameters', o.params()); if (o.apresReglage) dire(o.apresReglage(D)); emettre();
    }
    Object.assign(D, { start, pause, resume, reset, setTime, playUntil, setParameters, dire, emettre, noter, etiquette });
    $('run').onclick = () => (S.running ? pause() : S.pause ? resume() : start());
    if (o.explication) T.explication(o.explication);
    const commandes = ['start', 'pause', 'resume', 'reset', 'set_time', 'set_parameters', 'play_until'];
    const config = { id: o.id, version: '1.0', title: o.titre, variants: o.vues && o.vues.length > 1 ? o.vues.map(id => ({ id, label: id })) : [],
      commands: commandes,
      command_schema: { set_parameters: o.schema || {}, set_time: { time_s: '0..fin, en s (voir moments)' },
        play_until: { moment: Object.keys(MOM).join(' | ') + ' (joue jusqu’à la fin de cette étape et s’y fige ; une étape déjà montrée ne rejoue pas)' } } };
    pont = T.protocole({ id: o.id, commandes, config, texte: o.texte,
      etat: () => ({ simulation_status: S.running ? 'running' : S.fait ? 'finished' : S.pause ? 'paused' : 'idle',
        ce_qui_se_voit: o.voir(D) + (S.dit ? ` La bulle dit : « ${S.dit} »` : ''), current_variant: S.vue || undefined,
        time_s: +S.t.toFixed(2), parameters: o.params(),
        moments: Object.fromEntries(Object.entries(MOM).map(([k, v]) => [k, +v.toFixed(2)])) }),
      progression: () => (S.fait ? 1 : 0),
      executer: (cmd, p) => ({ start, pause, resume, reset, set_time: () => setTime(p), set_parameters: () => setParameters(p), play_until: () => playUntil(p) })[cmd]?.() });
    etiquette(); dire(o.accueil ? o.accueil(D) : o.depart(D));
    return D;
  }
  window.Deroule = Deroule;
  window.Deroule.sci = sci;
})();
