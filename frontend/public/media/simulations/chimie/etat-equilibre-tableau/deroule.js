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
    // 15 novembre 2026 : cadre au format du tableau, la boîte de l'encre de l'image complète remplit le tableau.
    scene = window.OndesTableau.Scene($('canvas'), c => o.dessiner(c, D), o.scene || { large: true, ajuster: true, complet: f => { const t = S.t; S.t = 1e9; try { f(); } finally { S.t = t; } } });
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

  /*
   * La verrerie et le matériel PEINTS (professeur règle 32, 14 novembre 2026 : du réalisme, en couleurs, pas un croquis pauvre).
   * Peint sur c.ctx dans c.direct, sous la craie ; la craie garde les légendes, les valeurs, les flèches, les courbes.
   *   Peinture.becher(ctx, x, y, w, h, { surface, liquide: [r, g, b, a] }) : bécher en verre, bord en haut à y, fond à y + h.
   *   Peinture.tube(ctx, cx, yHaut, yBas, w, { surface, liquide }) : tube à essai.
   *   Peinture.phmetre(ctx, ecran {x, y, w, h}, sonde {x, yHaut, yBas}) : boîtier, écran à cristaux, câble, électrode de verre.
   *   Peinture.thermometre(ctx, x, yHaut, yBas, part) : tube de verre, réservoir, colonne rouge (part 0 → 1).
   *   Peinture.loupeFond / loupeCadre(ctx, cx, cy, r) : la lentille (avant les molécules) puis la monture et le manche (après).
   *   Peinture.sphere(ctx, x, y, r, [r, g, b]) : un atome ou un ion ombré ; Peinture.CPK : couleurs conventionnelles.
   *   Peinture.goutte(ctx, x, y, r) : une goutte d'eau qui tombe.
   */
  const rgba = (c, a) => `rgba(${c[0]},${c[1]},${c[2]},${a})`;
  const fonce = (c, k) => c.map(v => Math.round(v * k));
  const clair = (c, k) => c.map(v => Math.round(v + (255 - v) * k));
  function cheminBecher(ctx, x, y, w, h, r) {
    ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x, y + h - r); ctx.quadraticCurveTo(x, y + h, x + r, y + h);
    ctx.lineTo(x + w - r, y + h); ctx.quadraticCurveTo(x + w, y + h, x + w, y + h - r); ctx.lineTo(x + w, y);
  }
  const Peinture = {
    CPK: { O: [220, 38, 38], H: [240, 240, 240], C: [72, 72, 78], I: [124, 58, 237], N: [59, 90, 246] },
    sphere(ctx, x, y, r, c) {
      const g = ctx.createRadialGradient(x - r * .38, y - r * .4, r * .12, x, y, r);
      g.addColorStop(0, rgba(clair(c, .75), 1)); g.addColorStop(.45, rgba(c, 1)); g.addColorStop(1, rgba(fonce(c, .45), 1));
      ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.fill();
    },
    /** Liquide dans un récipient (chemin `forme` déjà fermé par l'appelant) : plus sombre aux bords, ménisque clair en haut. */
    liquide(ctx, x0, x1, ys, yb, c, a, forme) {
      ctx.save(); forme(); ctx.clip();
      const g = ctx.createLinearGradient(x0, 0, x1, 0);
      g.addColorStop(0, rgba(fonce(c, .72), Math.min(1, a + .12))); g.addColorStop(.35, rgba(c, a)); g.addColorStop(.6, rgba(clair(c, .18), a)); g.addColorStop(1, rgba(fonce(c, .68), Math.min(1, a + .15)));
      ctx.fillStyle = g; ctx.fillRect(x0, ys, x1 - x0, yb - ys + 2);
      ctx.restore();
      // Le ménisque : la surface vue un peu par-dessus.
      ctx.fillStyle = rgba(clair(c, .35), Math.min(1, a * .9 + .08)); ctx.beginPath(); ctx.ellipse((x0 + x1) / 2, ys, (x1 - x0) / 2, 3.2, 0, 0, Math.PI * 2); ctx.fill();
      ctx.strokeStyle = rgba(clair(c, .6), .55); ctx.lineWidth = 1; ctx.stroke();
    },
    becher(ctx, x, y, w, h, o = {}) {
      ctx.save();
      ctx.fillStyle = 'rgba(0,0,0,.3)'; ctx.beginPath(); ctx.ellipse(x + w / 2 + 3, y + h + 3, w * .56, 4.5, 0, 0, Math.PI * 2); ctx.fill();
      // Le verre vu par transparence : un léger voile bleuté.
      cheminBecher(ctx, x, y, w, h, 7); ctx.closePath(); ctx.fillStyle = 'rgba(190,220,240,.09)'; ctx.fill();
      if (o.surface != null && o.liquide) {
        const [r, g, b, a] = o.liquide;
        Peinture.liquide(ctx, x + 2, x + w - 2, Math.max(y + 4, o.surface), y + h - 2, [r, g, b], a, () => { cheminBecher(ctx, x + 2, y, w - 4, h - 2, 6); ctx.closePath(); });
      }
      // Fond épais, parois, reflets.
      ctx.fillStyle = 'rgba(220,238,250,.28)'; ctx.fillRect(x + 6, y + h - 3, w - 12, 3);
      ctx.strokeStyle = 'rgba(225,240,252,.8)'; ctx.lineWidth = 1.8; cheminBecher(ctx, x, y, w, h, 7); ctx.stroke();
      let g = ctx.createLinearGradient(x + 3, 0, x + 12, 0); g.addColorStop(0, 'rgba(255,255,255,.5)'); g.addColorStop(1, 'rgba(255,255,255,0)');
      ctx.fillStyle = g; ctx.fillRect(x + 3, y + 8, 9, h - 18);
      ctx.strokeStyle = 'rgba(255,255,255,.35)'; ctx.lineWidth = 1.2; ctx.beginPath(); ctx.moveTo(x + w - 5, y + 10); ctx.lineTo(x + w - 5, y + h - 14); ctx.stroke();
      // Graduations et bec verseur.
      ctx.strokeStyle = 'rgba(235,245,255,.45)'; ctx.lineWidth = 1;
      for (let k = 1; k <= 3; k++) { const yy = y + h - k * h / 4.2; ctx.beginPath(); ctx.moveTo(x + w - 18, yy); ctx.lineTo(x + w - 9, yy); ctx.stroke(); }
      ctx.strokeStyle = 'rgba(240,248,255,.9)'; ctx.lineWidth = 2.2; ctx.beginPath(); ctx.ellipse(x + w / 2, y, w / 2, 2.6, 0, Math.PI, 2 * Math.PI); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(x, y); ctx.quadraticCurveTo(x - 6, y - 1, x - 7, y - 5); ctx.stroke();
      ctx.restore();
    },
    tube(ctx, cx, yh, yb, w, o = {}) {
      const x = cx - w / 2, r = w / 2;
      const forme = (dx = 0) => { ctx.beginPath(); ctx.moveTo(x + dx, yh); ctx.lineTo(x + dx, yb - r); ctx.arc(cx, yb - r, r - dx, Math.PI, 0, true); ctx.lineTo(x + w - dx, yh); };
      ctx.save();
      forme(); ctx.fillStyle = 'rgba(190,220,240,.1)'; ctx.fill();
      if (o.surface != null && o.liquide) {
        const [rr, gg, bb, a] = o.liquide;
        ctx.save(); forme(1.2); ctx.closePath(); ctx.clip();
        const g = ctx.createLinearGradient(x, 0, x + w, 0);
        g.addColorStop(0, rgba(fonce([rr, gg, bb], .7), Math.min(1, a + .1))); g.addColorStop(.4, rgba(clair([rr, gg, bb], .2), a)); g.addColorStop(1, rgba(fonce([rr, gg, bb], .62), Math.min(1, a + .1)));
        ctx.fillStyle = g; ctx.fillRect(x, o.surface, w, yb - o.surface); ctx.restore();
        ctx.fillStyle = rgba(clair([rr, gg, bb], .4), a); ctx.beginPath(); ctx.ellipse(cx, o.surface, r - 1.2, 1.8, 0, 0, Math.PI * 2); ctx.fill();
      }
      ctx.strokeStyle = 'rgba(225,240,252,.85)'; ctx.lineWidth = 1.4; forme(); ctx.stroke();
      ctx.strokeStyle = 'rgba(255,255,255,.55)'; ctx.lineWidth = 1.2; ctx.beginPath(); ctx.moveTo(x + 2.6, yh + 3); ctx.lineTo(x + 2.6, yb - r - 1); ctx.stroke();
      ctx.strokeStyle = 'rgba(240,248,255,.9)'; ctx.lineWidth = 1.8; ctx.beginPath(); ctx.ellipse(cx, yh, r + .8, 1.6, 0, 0, Math.PI * 2); ctx.stroke();
      ctx.restore();
    },
    phmetre(ctx, e, s) {
      ctx.save();
      // Le câble, du boîtier à l'électrode.
      ctx.strokeStyle = '#1b1f24'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(e.x + e.w + 6, e.y + e.h * .55);
      ctx.bezierCurveTo(e.x + e.w + 28, e.y + e.h * .55, s.x + 24, s.yHaut - 2, s.x + 4, s.yHaut + 5); ctx.stroke();
      // Le boîtier (gris anthracite) et son écran à cristaux liquides.
      ctx.shadowColor = 'rgba(0,0,0,.4)'; ctx.shadowBlur = 7; ctx.shadowOffsetX = 2; ctx.shadowOffsetY = 3;
      let g = ctx.createLinearGradient(0, e.y - 6, 0, e.y + e.h + 10); g.addColorStop(0, '#5b6673'); g.addColorStop(.5, '#3a434d'); g.addColorStop(1, '#252c33');
      ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(e.x - 6, e.y - 6, e.w + 12, e.h + 14, 7); ctx.fill(); ctx.restore(); ctx.save();
      g = ctx.createLinearGradient(0, e.y, 0, e.y + e.h); g.addColorStop(0, '#22402f'); g.addColorStop(1, '#10251a');
      ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(e.x, e.y, e.w, e.h, 4); ctx.fill();
      ctx.strokeStyle = 'rgba(0,0,0,.5)'; ctx.lineWidth = 1.2; ctx.stroke();
      ctx.fillStyle = 'rgba(255,255,255,.07)'; ctx.beginPath(); ctx.roundRect(e.x + 2, e.y + 2, e.w - 4, e.h * .38, 3); ctx.fill();
      for (const [dx, col] of [[e.w * .3, '#c0392b'], [e.w * .7, '#7f8c8d']]) { ctx.fillStyle = col; ctx.beginPath(); ctx.arc(e.x + dx, e.y + e.h + 4.5, 2.2, 0, Math.PI * 2); ctx.fill(); }
      // L'électrode : corps noir, tige de verre, boule sensible en bas.
      g = ctx.createLinearGradient(s.x - 5, 0, s.x + 5, 0); g.addColorStop(0, '#111'); g.addColorStop(.4, '#4a4f55'); g.addColorStop(1, '#111');
      const yc = s.yHaut + (s.yBas - s.yHaut) * .42;
      ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(s.x - 5, s.yHaut, 10, yc - s.yHaut, 3); ctx.fill();
      ctx.fillStyle = 'rgba(200,228,245,.32)'; ctx.fillRect(s.x - 3.5, yc, 7, s.yBas - yc - 4);
      ctx.strokeStyle = 'rgba(230,245,255,.75)'; ctx.lineWidth = 1; ctx.strokeRect(s.x - 3.5, yc, 7, s.yBas - yc - 4);
      ctx.strokeStyle = 'rgba(240,240,240,.6)'; ctx.beginPath(); ctx.moveTo(s.x, yc + 3); ctx.lineTo(s.x, s.yBas - 4); ctx.stroke();
      g = ctx.createRadialGradient(s.x - 2, s.yBas - 2, 1, s.x, s.yBas, 6); g.addColorStop(0, 'rgba(255,255,255,.75)'); g.addColorStop(1, 'rgba(180,215,240,.35)');
      ctx.fillStyle = g; ctx.beginPath(); ctx.arc(s.x, s.yBas, 5.5, 0, Math.PI * 2); ctx.fill(); ctx.strokeStyle = 'rgba(230,245,255,.8)'; ctx.stroke();
      ctx.restore();
    },
    thermometre(ctx, x, yh, yb, part) {
      ctx.save();
      const tete = yb - 6, top = yh + 4 + (tete - yh - 10) * (1 - part);
      ctx.fillStyle = 'rgba(215,235,250,.22)'; ctx.beginPath(); ctx.roundRect(x - 3.5, yh, 7, yb - yh, 3.5); ctx.fill();
      ctx.strokeStyle = 'rgba(230,245,255,.8)'; ctx.lineWidth = 1.2; ctx.stroke();
      const g = ctx.createLinearGradient(x - 2, 0, x + 2, 0); g.addColorStop(0, '#8f1010'); g.addColorStop(.5, '#ef4444'); g.addColorStop(1, '#8f1010');
      ctx.fillStyle = g; ctx.fillRect(x - 1.4, top, 2.8, tete - top);
      Peinture.sphere(ctx, x, yb, 5.2, [220, 30, 30]);
      ctx.strokeStyle = 'rgba(240,248,255,.55)'; ctx.lineWidth = .8;
      for (let k = 0; k < 6; k++) { const yy = yh + 8 + k * (tete - yh - 14) / 5; ctx.beginPath(); ctx.moveTo(x + 3.5, yy); ctx.lineTo(x + (k % 2 ? 6 : 8), yy); ctx.stroke(); }
      ctx.restore();
    },
    loupeFond(ctx, cx, cy, r) {
      const g = ctx.createRadialGradient(cx - r * .3, cy - r * .3, r * .1, cx, cy, r);
      g.addColorStop(0, 'rgba(210,235,255,.16)'); g.addColorStop(1, 'rgba(120,170,210,.22)');
      ctx.save(); ctx.fillStyle = g; ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2); ctx.fill(); ctx.restore();
    },
    loupeCadre(ctx, cx, cy, r, angle = Math.PI / 4) {
      ctx.save();
      const c = Math.cos(angle), s = Math.sin(angle), x0 = cx + (r + 4) * c, y0 = cy + (r + 4) * s, L = r * .5;
      // Le manche : virole métallique puis poignée en bois sombre.
      ctx.lineCap = 'round';
      ctx.strokeStyle = '#9aa4ae'; ctx.lineWidth = 9; ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(x0 + 10 * c, y0 + 10 * s); ctx.stroke();
      ctx.strokeStyle = '#5a3418'; ctx.lineWidth = 11; ctx.beginPath(); ctx.moveTo(x0 + 12 * c, y0 + 12 * s); ctx.lineTo(x0 + L * c, y0 + L * s); ctx.stroke();
      ctx.strokeStyle = 'rgba(255,220,180,.3)'; ctx.lineWidth = 2.5; ctx.beginPath(); ctx.moveTo(x0 + 13 * c - 2.5 * s, y0 + 13 * s + 2.5 * c); ctx.lineTo(x0 + (L - 2) * c - 2.5 * s, y0 + (L - 2) * s + 2.5 * c); ctx.stroke();
      // Le reflet sur le verre, puis la monture chromée.
      ctx.strokeStyle = 'rgba(255,255,255,.28)'; ctx.lineWidth = 5; ctx.beginPath(); ctx.arc(cx, cy, r * .8, Math.PI * 1.08, Math.PI * 1.42); ctx.stroke();
      const g = ctx.createLinearGradient(cx - r, cy - r, cx + r, cy + r);
      g.addColorStop(0, '#eef2f5'); g.addColorStop(.35, '#8d979f'); g.addColorStop(.6, '#d5dbe0'); g.addColorStop(1, '#59626a');
      ctx.strokeStyle = g; ctx.lineWidth = 6; ctx.beginPath(); ctx.arc(cx, cy, r + 1, 0, Math.PI * 2); ctx.stroke();
      ctx.strokeStyle = 'rgba(0,0,0,.35)'; ctx.lineWidth = 1; ctx.beginPath(); ctx.arc(cx, cy, r + 4.2, 0, Math.PI * 2); ctx.stroke();
      ctx.restore();
    },
    goutte(ctx, x, y, r) {
      ctx.save();
      const g = ctx.createRadialGradient(x - r * .35, y - r * .1, r * .1, x, y + r * .2, r * 1.2);
      g.addColorStop(0, 'rgba(235,248,255,.95)'); g.addColorStop(1, 'rgba(96,165,250,.85)');
      ctx.fillStyle = g; ctx.beginPath(); ctx.moveTo(x, y - r * 2); ctx.quadraticCurveTo(x + r * 1.1, y - r * .2, x + r, y + r * .3);
      ctx.arc(x, y + r * .3, r, 0, Math.PI); ctx.quadraticCurveTo(x - r * 1.1, y - r * .2, x, y - r * 2); ctx.fill();
      ctx.restore();
    },
  };
  window.Peinture = Peinture;
})();
