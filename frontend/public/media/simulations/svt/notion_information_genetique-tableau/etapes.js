/*
 * Moteur commun des simulations du cours « Notion de l’information génétique » (2 Bac PC BIOF, 11 novembre 2026).
 * Une simulation = des VUES ; chaque vue = une scène qui se joue de 0 à `fin` secondes, avec des MOMENTS nommés
 * (instants calculés par la vue) sur lesquels le tuteur fige la scène (`play_until {moment}`), comme structure.html du
 * cours du muscle. Le moteur fait le reste, pareil pour toutes les pages :
 *   - un seul bouton #run qui cycle (Lancer → Pause → Reprendre → Rejouer), une bulle #feedback ;
 *   - le protocole du tuteur (Tableau.protocole) : start, reset, pause, resume, set_time, set_parameters, play_until (+ highlight du kit) ;
 *   - l’état : simulation_status, ce_qui_se_voit, current_variant, time_s, parameters, moments ;
 *   - un moment peut porter des réglages (`reglages`) : ils sont posés, puis la scène rejoue jusqu’à cet instant et se fige ;
 *   - l’écriture en direct : `ecrit(c, nom, tEv)` fait apparaître un groupe de légendes à son instant, écrit trait par trait ;
 *   - les poignées glissées sur le dessin (Tableau.glisser), en coordonnées du cadre 760 × 420.
 *
 * Utilisation :
 *   Etapes.lancer({ id, titre, vues: { <nom>: { titre, fin, moments: {nom: t}, motifs: {nom: 'phrase'}, reglages: {moment: {param: v}},
 *     dessiner(c, k), voit(k) → [phrases], explication: [{repere, texte}], texte, conclusion } }, parametres: { nom: {defaut, schema, lire(v)} },
 *     poignees: { toucher(x, y, k) → id|null, bouger(id, x, y, k), lacher(id, k) }, apresReglage(k, cles) }).
 *   k = { t, S, P (paramètres), vue, ecrit, T, rampe, lisse, entre, fin }.
 */
(function () {
  'use strict';
  const lisse = x => (x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x));
  const rampe = (t, a, d) => lisse((t - a) / d);
  const TAU = Math.PI * 2;
  const entre = (a, b, u) => a + (b - a) * u;

  function lancer(def) {
    const { fr, bulle, protocole } = window.Tableau;
    const $ = id => document.getElementById(id);
    const noms = Object.keys(def.vues);
    const demandee = new URLSearchParams(location.search).get('vue');
    const P = {};
    for (const [n, d] of Object.entries(def.parametres || {})) P[n] = d.defaut;
    if (def.auDepart) def.auDepart(P);   // optionnel (14 novembre 2026) : une page lit ses réglages de départ (ex. ?conclusions=false)
    const S = { vue: noms.includes(demandee) ? demandee : noms[0], t: 0, running: false, jusqua: null, motif: '', fait: false, emis: 0, vu: {}, P };
    const V = () => def.vues[S.vue];
    let scene = null;
    const horloge = () => (performance.now() - scene.ouvert) / 1000;
    function ecrit(c, nom, tEv) { if (S.t < tEv - 1e-6) return false; if (!(nom in S.vu)) S.vu[nom] = horloge(); c.depuis(S.vu[nom]); return true; }
    const dureeTexte = s => Math.min(1.2, Math.max(.3, String(s).length / 28));
    const T = (c, s, x, y, o = {}) => c.texte(s, x, y, { duree: dureeTexte(s), ...o });
    /* ── Tableau large (15 novembre 2026, « mieux exploiter tout le tableau, grands calibres de texte ») ──────────────
     * Le cadre prend le format du tableau (scene.L de 760 à 1596, hauteur 420 ; option `large` de commun.js).
     * Une vue qui déclare `blocs` et `disposition` voit son dessin d'origine (prévu pour 760 × 420) découpé en BLOCS quand
     * le tableau est large (L ≥ 1000, écran 1366 × 613) : chaque bloc = une boîte du dessin d'origine [x0, y0, x1, y1, zmax?]
     * qu'on reprend, posée ailleurs et agrandie. Le dessin de la vue est rejoué une fois par bloc, dans le repère du bloc
     * (translate + scale) et découpé à sa boîte : la peinture, la craie, l'écriture en direct ET les repères du professeur
     * suivent sans rien changer au code de la vue (un repère appartient au bloc qui contient son centre). Deux boîtes qui se
     * chevauchent : la plus petite garde la partie commune (un texte sorti de la figure n'est pas dessiné deux fois).
     * `disposition` : { haut: [noms] (bandeau du haut, en ligne, agrandi jusqu'à zhaut), colonnes: [[noms empilés], …] } ;
     * chaque colonne grandit autant que la hauteur le permet (borné par zmax, 1,7 par défaut) ; si la largeur manque, toutes
     * rétrécissent ensemble ; le reste de la largeur va aux écarts. Tableau étroit (L < 1000, grand écran 1920 × 1080) :
     * disposition d'origine, centrée. Une vue sans `blocs` est simplement centrée dans le cadre large. */
    const POSES = {};   // vue → { L, map: nom → {x0,y0,X,Y,z} }
    const estLarge = v => scene.L >= 1000 && !!(v.blocs && v.disposition);
    function disposer(v, L) {
      const B = v.blocs, memo = POSES[S.vue]; if (memo && memo.L === L && memo.B === B) return memo.map;
      const map = {};
      const D = typeof v.disposition === 'function' ? v.disposition(L) : v.disposition;
      const M = D.marge ?? 12, E = D.ecart ?? 22, HT = 420;
      const dim = n => { const b = B[n]; return { w: b[2] - b[0], h: b[3] - b[1], zmax: b[4] || D.zmax || 1.7 }; };
      let y = M;
      if (D.haut) {   // bandeau du haut : les blocs en ligne, à gauche
        let x = M, hMax = 0;
        for (const n of D.haut) { const d = dim(n), z = Math.min(d.zmax, D.zhaut || 1.3); map[n] = { x0: B[n][0], y0: B[n][1], X: x, Y: M, z }; x += d.w * z + E; hMax = Math.max(hMax, d.h * z); }
        y = M + hMax + (D.sousHaut ?? 4);
      }
      // `pleine` : les colonnes après la première (à droite du titre) prennent toute la hauteur
      const cols = D.colonnes.map((col, i) => {
        const y0 = D.pleine && i > 0 ? M : y, Ha = HT - y0 - M;
        const ds = col.map(dim), w = Math.max(...ds.map(d => d.w)), h = ds.reduce((a, d) => a + d.h, 0);
        return { col, ds, w, y0, Ha, z: Math.min(Math.min(...ds.map(d => d.zmax)), (Ha - E * (col.length - 1)) / h) };
      });
      const gaps = E * (cols.length - 1), somme = cols.reduce((a, c) => a + c.w * c.z, 0);
      const f = Math.min(1, (L - 2 * M - gaps) / somme);
      cols.forEach(c => { c.z *= f; });
      const reste = L - 2 * M - cols.reduce((a, c) => a + c.w * c.z, 0), ecart = reste / Math.max(1, cols.length + 1);
      let x = M + ecart;
      for (const c of cols) {
        const hz = c.ds.reduce((a, d) => a + d.h * c.z, 0) + E * (c.col.length - 1);
        let yy = c.y0 + Math.max(0, (c.Ha - hz) / 2);
        c.col.forEach((n, i) => { const d = c.ds[i]; map[n] = { x0: B[n][0], y0: B[n][1], X: x + (c.w - d.w) * c.z / 2, Y: yy, z: c.z }; yy += d.h * c.z + E; });
        x += c.w * c.z + ecart;
      }
      POSES[S.vue] = { L, B, map };
      return map;
    }
    /** Le dessin de la vue rejoué bloc par bloc (tableau large). */
    function dessinerBlocs(c, v) {
      const blocs = v.blocs, map = disposer(v, scene.L), x = c.ctx, e = c.echelle, cadre = c.cadre;
      let complet = true, tip = null, cur = 0;
      for (const [nom, p] of Object.entries(map)) {
        const b = blocs[nom];
        c.cur = 0; c.tip = null; c.complet = true;
        x.save(); x.translate(p.X - p.x0 * p.z, p.Y - p.y0 * p.z); x.scale(p.z, p.z);
        // un bloc plus petit qui chevauche celui-ci (un texte sorti de la figure) en est retiré : il est dessiné à sa place
        const dans = (q, px, py) => px >= q[0] && px < q[2] && py >= q[1] && py < q[3], aire = q => (q[2] - q[0]) * (q[3] - q[1]);
        const trous = Object.entries(blocs).filter(([n, q]) => n !== nom && aire(q) < aire(b) && q[0] < b[2] && q[2] > b[0] && q[1] < b[3] && q[3] > b[1]).map(([, q]) => q);
        // La découpe : la peinture et les traits sont coupés à la boîte du bloc (moins ses trous) ; un TEXTE est écrit en
        // entier par le bloc qui contient son point d'ancrage (le plancher de 15 px à l'écran peut l'élargir au-delà de
        // sa boîte d'origine : il n'est jamais coupé) et, dans les autres blocs, il est « écrit » invisible pour que
        // l'écriture en direct garde le même rythme dans chaque passe.
        const decouper = () => {
          x.beginPath(); x.rect(b[0], b[1], b[2] - b[0], b[3] - b[1]);
          // (chaque trou réduit à sa partie commune avec ce bloc : en pair-impair, un morceau qui déborde serait ajouté)
          for (const q of trous) { const x0 = Math.max(q[0], b[0]), y0 = Math.max(q[1], b[1]); x.rect(x0, y0, Math.min(q[2], b[2]) - x0, Math.min(q[3], b[3]) - y0); }
          x.clip('evenodd');
        };
        if (e) c.echelle = e * p.z; c.cadre = null;
        const dedans = (px, py) => dans(b, px, py) && !trous.some(q => dans(q, px, py));
        const proto = Object.getPrototypeOf(c), coupe = nomF => function (...a) { x.save(); decouper(); try { return proto[nomF].apply(this, a); } finally { x.restore(); } };
        for (const nomF of ['direct', 'trait', 'rect', 'cercle', 'point']) c[nomF] = coupe(nomF);
        c.texte = function (s, tx, ty, o = {}) { return proto.texte.call(this, s, tx, ty, dedans(tx, ty - (o.taille ?? 18) * .35) ? o : { ...o, alpha: 0 }); };
        c.repere = function (id, rx, ry, w, h, label) { return dedans(rx + w / 2, ry + h / 2) ? proto.repere.call(this, id, rx, ry, w, h, label) : this; };
        try { v.dessiner(c, k()); }
        finally { x.restore(); c.echelle = e; c.cadre = cadre; for (const f of ['direct', 'trait', 'rect', 'cercle', 'point', 'texte', 'repere']) delete c[f]; }
        complet = complet && c.complet; cur = Math.max(cur, c.cur);
        if (c.tip && dedans(c.tip[0], c.tip[1])) tip = [p.X + (c.tip[0] - p.x0) * p.z, p.Y + (c.tip[1] - p.y0) * p.z];
      }
      c.complet = complet; c.tip = tip; c.cur = cur;
    }
    /** Point du cadre → point du dessin d'origine (poignées glissées). */
    function versOrigine(X, Y) {
      const v = V();
      if (!estLarge(v)) return [X - (scene.L - 760) / 2, Y];
      const aire = q => (q[2] - q[0]) * (q[3] - q[1]);
      const tri = Object.entries(disposer(v, scene.L)).sort(([a], [b]) => aire(v.blocs[a]) - aire(v.blocs[b]));   // le plus petit d'abord
      for (const [nom, p] of tri) {
        const b = v.blocs[nom], x = (X - p.X) / p.z + p.x0, y = (Y - p.Y) / p.z + p.y0;
        if (x >= b[0] - 8 && x < b[2] + 8 && y >= b[1] - 8 && y < b[3] + 8) return [x, y];
      }
      // entre deux blocs (une pièce glissée de l'un à l'autre) : le bloc posé le plus proche
      let mieux = null, dMin = Infinity;
      for (const [nom, p] of tri) {
        const b = v.blocs[nom], X0 = p.X, Y0 = p.Y, X1 = p.X + (b[2] - b[0]) * p.z, Y1 = p.Y + (b[3] - b[1]) * p.z;
        const d = Math.hypot(Math.max(X0 - X, 0, X - X1), Math.max(Y0 - Y, 0, Y - Y1));
        if (d < dMin) { dMin = d; mieux = [(X - p.X) / p.z + p.x0, (Y - p.Y) / p.z + p.y0]; }
      }
      return mieux || [X, Y];
    }
    const k = () => ({ t: S.t, S, P, vue: S.vue, ecrit, T, rampe, lisse, entre, fin: V().fin, fr });

    const canvas = $('canvas');
    scene = window.GenetiqueTableau.Scene(canvas, (c) => {
      scene.cadre(def.graine || 17);
      const v = V();
      if (estLarge(v)) dessinerBlocs(c, v);
      else if (scene.L > 760) { c.ctx.save(); c.ctx.translate((scene.L - 760) / 2, 0); try { v.dessiner(c, k()); } finally { c.ctx.restore(); } }
      else v.dessiner(c, k());
      return c.fin();
    }, { large: true });
    const FIN = () => V().fin;
    scene.avancer = dt => {
      if (!S.running) return false;
      S.t = Math.min(FIN(), S.t + dt);
      if (S.jusqua != null && S.t >= S.jusqua - 1e-9) {
        S.t = S.jusqua; S.running = false; S.jusqua = null; $('run').textContent = S.t >= FIN() - 1e-6 ? 'Rejouer' : 'Reprendre';
        if (S.t >= FIN() - 1e-6) S.fait = true;
        bulle($('feedback'), 'Arrêt sur image : ' + (S.motif || `t = ${fr(S.t, 1)} s`) + '.'); pont.noter('pause', { time_s: +S.t.toFixed(2) }); pont.emettre();
        return true;
      }
      if (S.t >= FIN()) { S.running = false; S.fait = true; $('run').textContent = 'Rejouer'; bulle($('feedback'), V().conclusion || 'Fin.', 'good'); pont.emettre(); }
      else if (performance.now() - S.emis > 500) { S.emis = performance.now(); pont.emettre(); }
      return true;
    };
    function statut() { return S.running ? 'running' : (S.fait ? 'finished' : (S.t > 0 ? 'paused' : 'idle')); }
    function ceQuiSeVoit() {
      const v = V(), t = S.t;
      const tete = `Vue « ${v.titre} », t = ${fr(t, 1)} s${S.running ? ' (la scène avance)' : S.fait ? ' (fin)' : t > 0 ? ' (arrêt sur image)' : ' (pas encore lancée)'}.`;
      return [tete, ...(v.voit ? v.voit(k()) : [])].filter(Boolean).join(' ');
    }
    function start() { S.jusqua = null; S.vu = {}; S.t = 0; S.running = true; S.fait = false; $('run').textContent = 'Pause'; scene.sale = true; bulle($('feedback'), (V().titre || '') + ' : observe…'); pont.noter('start'); pont.emettre(); }
    function reset() { start(); }
    function pause() { if (!S.running) return; S.running = false; S.jusqua = null; $('run').textContent = 'Reprendre'; bulle($('feedback'), 'Arrêt sur image.'); pont.noter('pause', { time_s: +S.t.toFixed(2) }); pont.emettre(); }
    function resume() { if (S.running) return; if (S.fait || S.t >= FIN()) return start(); S.running = true; $('run').textContent = 'Pause'; bulle($('feedback'), 'Observe…'); pont.noter('resume'); pont.emettre(); }
    function poser(p, rejouer) {
      const cles = [];
      if (p.vue && def.vues[p.vue] && p.vue !== S.vue) { S.vue = p.vue; cles.push('vue'); S.vu = {}; S.t = 0; S.fait = false; }
      for (const [n, d] of Object.entries(def.parametres || {})) {
        if (!(n in p)) continue;
        const v = d.lire ? d.lire(p[n], S) : p[n];
        if (v === undefined || v === null || (typeof v === 'number' && !Number.isFinite(v))) continue;
        if (P[n] !== v) { P[n] = v; cles.push(n); }
      }
      if (def.apresReglage) def.apresReglage(k(), cles);
      if (def.auReglage) def.auReglage(P, cles);
      scene.sale = true;
      return cles;
    }
    function playUntil(p) {
      const v = V(); let nom = p.moment;
      if (nom && !(nom in v.moments)) {   // un moment d’une autre vue : on change de vue
        const autre = noms.find(n => def.vues[n].moments && nom in def.vues[n].moments);
        if (autre) { S.vue = autre; S.vu = {}; S.t = 0; S.fait = false; } else nom = null;
      }
      const vv = V(), ok = nom && nom in vv.moments;
      let rejoue = false;
      if (ok && vv.reglages && vv.reglages[nom]) { if (poser(vv.reglages[nom]).length) rejoue = true; }
      const extra = { ...p }; delete extra.moment; delete extra.time_s;
      if (Object.keys(extra).length && poser(extra).length) rejoue = true;
      const cible = ok ? vv.moments[nom] : +p.time_s;
      if (!Number.isFinite(cible)) return;
      rejoue = rejoue || S.fait || S.t >= cible - 1e-4;
      if (rejoue) { S.vu = {}; S.t = 0; }
      S.jusqua = Math.min(FIN(), Math.max(.001, cible)); S.motif = ok ? ((vv.motifs && vv.motifs[nom]) || nom.replace(/_/g, ' ')) : '';
      S.running = true; S.fait = false; $('run').textContent = 'Pause'; scene.sale = true;
      bulle($('feedback'), rejoue ? 'On reprend depuis le début… observe.' : 'Observe…');
      pont.noter('play_until', { moment: ok ? nom : null, time_s: S.jusqua }); pont.emettre();
    }
    function setTime(p) {
      const t = +p.time_s; if (!Number.isFinite(t)) return;
      S.running = false; S.jusqua = null; S.vu = {}; S.t = Math.min(FIN(), Math.max(0, t)); S.fait = S.t >= FIN();
      $('run').textContent = S.fait ? 'Rejouer' : 'Reprendre'; scene.sale = true;
      bulle($('feedback'), `Arrêt sur image : t = ${fr(S.t, 1)} s.`); pont.noter('set_time', { time_s: S.t }); pont.emettre();
    }
    function setParameters(p) {
      const cles = poser(p || {});
      pont.noter('set_parameters', { ...p });
      if (cles.length) {
        const v = V();
        if (v.surReglage) v.surReglage(k(), cles, { playUntil, start, setTime });
        else if (S.t > 0 || S.fait) { S.vu = {}; S.t = 0; S.jusqua = null; S.running = true; S.fait = false; $('run').textContent = 'Pause'; bulle($('feedback'), 'Nouveau réglage : on rejoue… observe.'); }
      }
      pont.emettre();
    }
    $('run').onclick = () => (S.running ? pause() : (S.t > 0 && S.t < FIN() && !S.fait ? resume() : start()));

    if (def.poignees) {
      const pg = def.poignees;
      // coordonnées du dessin d'origine (760 × 420), quel que soit le placement (centré ou en blocs)
      const loc = (x, y) => { const [lx, ly] = scene.local(x, y); return versOrigine(lx, ly); };
      window.Tableau.glisser(canvas, {
        toucher: (x, y) => { const [lx, ly] = loc(x, y); return pg.toucher(lx, ly, k()); },
        bouger: (id, x, y) => { const [lx, ly] = loc(x, y); pg.bouger(id, lx, ly, k(), { poser, playUntil, setTime, start }); scene.sale = true; },
        lacher: (id) => { if (pg.lacher) pg.lacher(id, k(), { poser, playUntil, setTime, start }); pont.noter('glisser', { poignee: id, parameters: { ...P } }); pont.emettre(); scene.sale = true; },
      });
    }

    const expl = {}; for (const n of noms) expl[n] = def.vues[n].explication || [];
    window.Tableau.explication(expl);
    const commandes = ['start', 'reset', 'pause', 'resume', 'set_time', 'set_parameters', 'play_until'];
    const schemaParams = { vue: noms.join(' | ') };
    for (const [n, d] of Object.entries(def.parametres || {})) schemaParams[n] = d.schema || String(d.defaut);
    const tousMoments = noms.map(n => `${n} : ${Object.keys(def.vues[n].moments).join(', ')}`).join(' ; ');
    const config = { id: def.id, version: '1.0', title: def.titre, variants: noms.map(n => ({ id: n, label: def.vues[n].titre })), commands: commandes,
      command_schema: {
        set_parameters: schemaParams,
        set_time: { time_s: '0..fin de la vue (arrêt sur cet instant, en s de la scène)' },
        play_until: { moment: tousMoments + ' (rejoue et se fige à cet instant ; un moment d’une autre vue change de vue)', time_s: 'ou un instant en s' } } };
    const pont = protocole({ id: def.id, commandes, config,
      texte: noms.map(n => def.vues[n].texte || def.vues[n].titre).join(' | '),
      etat: () => ({ simulation_status: statut(), ce_qui_se_voit: ceQuiSeVoit(), current_variant: S.vue,
        time_s: +S.t.toFixed(2), parameters: { vue: S.vue, ...P }, moments: { ...V().moments } }),
      progression: () => (S.fait ? 1 : Math.min(1, S.t / FIN())),
      executer: (cmd, p) => ({ start, reset, pause, resume, set_time: () => setTime(p), set_parameters: () => setParameters(p), play_until: () => playUntil(p) })[cmd]?.() });
    bulle($('feedback'), (V().titre || def.titre) + '…');
    // Une vue peut attendre le tuteur (`autoDepart: false`, 14 novembre 2026) : rien ne se joue avant son premier geste,
    // sinon le résultat d'une expérience passerait sous les yeux de l'élève avant d'être dit. Par défaut : départ seul.
    setTimeout(() => { if (!S.running && S.t === 0 && V().autoDepart !== false) start(); }, 1600);
    window.__etapes = { S, P, scene, playUntil, setTime, setParameters, etat: () => ({ ce_qui_se_voit: ceQuiSeVoit(), moments: V().moments, statut: statut() }) };
    return window.__etapes;
  }

  /* ── Petits outils de peinture partagés (règle 7 : le vivant peint, la craie pour les légendes) ── */
  const Peint = {
    /** Cellule animale : cytoplasme rosé translucide, membrane plus sombre, quelques granulations. */
    cellule(x, cx, cy, rx, ry, a = 1, teinte) {
      x.save(); x.globalAlpha = a;
      const g = x.createRadialGradient(cx - rx * .3, cy - ry * .35, 4, cx, cy, Math.max(rx, ry));
      const t = teinte || ['rgba(255,214,222,.55)', 'rgba(244,170,190,.45)', 'rgba(214,120,150,.5)'];
      g.addColorStop(0, t[0]); g.addColorStop(.7, t[1]); g.addColorStop(1, t[2]);
      x.fillStyle = g; x.beginPath(); x.ellipse(cx, cy, rx, ry, 0, 0, Math.PI * 2); x.fill();
      x.strokeStyle = 'rgba(150,60,95,.8)'; x.lineWidth = 1.6; x.stroke();
      x.fillStyle = 'rgba(160,80,110,.28)';
      for (let i = 0; i < 26; i++) { const a2 = i * 2.39996, r = .25 + .65 * ((i * 37) % 23) / 23; x.beginPath(); x.arc(cx + Math.cos(a2) * rx * r, cy + Math.sin(a2) * ry * r, 1.3, 0, Math.PI * 2); x.fill(); }
      x.restore();
    },
    /** Noyau en interphase : violet-mauve, enveloppe double, pores, nucléole, chromatine en fins filaments. */
    noyau(x, cx, cy, r, a = 1, o = {}) {
      x.save(); x.globalAlpha = a;
      const g = x.createRadialGradient(cx - r * .3, cy - r * .3, 2, cx, cy, r);
      g.addColorStop(0, 'rgba(226,200,240,.85)'); g.addColorStop(1, 'rgba(160,110,200,.75)');
      x.fillStyle = g; x.beginPath(); x.arc(cx, cy, r, 0, Math.PI * 2); x.fill();
      if (o.chromatine !== false) {
        // chromatine : fins filaments enchevêtrés (marches aléatoires lissées, déterministes)
        let s = 12345; const rnd = () => { s = (Math.imul(s, 1103515245) + 12345) >>> 0; return s / 4294967296; };
        x.lineWidth = Math.max(.7, r / 46); x.lineCap = 'round';
        for (let j = 0; j < 9; j++) {
          let px = cx + (rnd() - .5) * r, py = cy + (rnd() - .5) * r, ang = rnd() * TAU;
          const pts = [[px, py]];
          for (let i = 0; i < 34; i++) {
            ang += (rnd() - .5) * 1.6; px += Math.cos(ang) * r * .09; py += Math.sin(ang) * r * .09;
            const d = Math.hypot(px - cx, py - cy); if (d > r * .86) { ang += Math.PI; px = cx + (px - cx) * .84 * r / d; py = cy + (py - cy) * .84 * r / d; }
            pts.push([px, py]);
          }
          x.strokeStyle = j % 2 ? 'rgba(95,40,140,.55)' : 'rgba(120,60,170,.45)'; x.beginPath(); x.moveTo(pts[0][0], pts[0][1]);
          for (let i = 1; i < pts.length - 1; i++) x.quadraticCurveTo(pts[i][0], pts[i][1], (pts[i][0] + pts[i + 1][0]) / 2, (pts[i][1] + pts[i + 1][1]) / 2);
          x.stroke();
        }
      }
      if (o.nucleole !== false) { const gn = x.createRadialGradient(cx + r * .2, cy - r * .1, 1, cx + r * .25, cy - r * .05, r * .22); gn.addColorStop(0, 'rgba(120,50,150,.95)'); gn.addColorStop(1, 'rgba(70,20,100,.9)'); x.fillStyle = gn; x.beginPath(); x.arc(cx + r * .25, cy - r * .05, r * .2, 0, Math.PI * 2); x.fill(); }
      x.strokeStyle = 'rgba(90,40,130,.9)'; x.lineWidth = Math.max(1, r / 30); x.beginPath(); x.arc(cx, cy, r, 0, Math.PI * 2); x.stroke();
      if (o.double) { x.beginPath(); x.arc(cx, cy, r + Math.max(2, r / 22), 0, Math.PI * 2); x.stroke();
        x.fillStyle = 'rgba(255,240,250,.95)'; for (let i = 0; i < 12; i++) { const a2 = i * Math.PI / 6 + .2; x.beginPath(); x.arc(cx + Math.cos(a2) * (r + r / 44 + 1), cy + Math.sin(a2) * (r + r / 44 + 1), Math.max(1.6, r / 26), 0, Math.PI * 2); x.fill(); } }
      x.restore();
    },
    /** Un chromosome peint : `pts` = ligne médiane [[x,y],…] d’une chromatide ; deux chromatides si `deux` (écart `ecart`). */
    chromatide(x, pts, couleur, epaisseur = 7, a = 1) {
      x.save(); x.globalAlpha = a; x.lineCap = 'round'; x.lineJoin = 'round';
      x.strokeStyle = couleur[1]; x.lineWidth = epaisseur; x.beginPath(); pts.forEach(([px, py], i) => (i ? x.lineTo(px, py) : x.moveTo(px, py))); x.stroke();
      x.strokeStyle = couleur[0]; x.lineWidth = epaisseur * .45; x.beginPath(); pts.forEach(([px, py], i) => (i ? x.lineTo(px - epaisseur * .15, py - epaisseur * .15) : x.moveTo(px - epaisseur * .15, py - epaisseur * .15))); x.stroke();
      x.restore();
    },
    VIOLET: ['#e9c8ff', '#7e22ce'], BLEU: ['#c7d2fe', '#4338ca'],
    /** Chromosome en bâtonnet (centre cx,cy, longueur L, angle a) ; deux chromatides si `deux`, reliées au centromère (position c ∈ 0..1). */
    chromosome(x, cx, cy, L, ang, couleur, o = {}) {
      const e = o.epaisseur || 7, c = o.centromere ?? .4, deux = o.deux, ec = o.ecart ?? e * .75, al = o.alpha ?? 1;
      const ux = Math.cos(ang), uy = Math.sin(ang), nx = -uy, ny = ux;
      const ligne = (d) => { const pts = []; for (let i = 0; i <= 12; i++) { const s = i / 12, off = deux ? d * (ec * (0.35 + 0.65 * Math.min(1, Math.abs(s - c) * 4))) : 0; pts.push([cx + ux * (s - .5) * L + nx * off, cy + uy * (s - .5) * L + ny * off]); } return pts; };
      if (deux) { Peint.chromatide(x, ligne(-1), couleur, e, al); Peint.chromatide(x, ligne(1), couleur, e, al); }
      else Peint.chromatide(x, ligne(0), couleur, e, al);
      x.save(); x.globalAlpha = al; x.fillStyle = 'rgba(40,10,60,.85)'; x.beginPath(); x.arc(cx + ux * (c - .5) * L, cy + uy * (c - .5) * L, e * .42, 0, Math.PI * 2); x.fill(); x.restore();
    },
    /** Bulle lumineuse (UV, radioactivité). */
    halo(x, cx, cy, r, couleur, a = 1) { x.save(); x.globalAlpha = a; const g = x.createRadialGradient(cx, cy, 0, cx, cy, r); g.addColorStop(0, couleur); g.addColorStop(1, 'rgba(0,0,0,0)'); x.fillStyle = g; x.beginPath(); x.arc(cx, cy, r, 0, Math.PI * 2); x.fill(); x.restore(); },
    /** Souris simple ombrée ; `morte` = couchée sur le dos, pattes en l’air. */
    souris(x, cx, cy, s = 1, morte = false, a = 1) {
      x.save(); x.globalAlpha = a; x.translate(cx, cy); x.scale(s, s); if (morte) x.scale(1, -1);
      const g = x.createRadialGradient(-6, -8, 2, 0, 0, 26); g.addColorStop(0, '#e5e7eb'); g.addColorStop(1, '#6b7280');
      x.fillStyle = g; x.beginPath(); x.ellipse(0, 0, 24, 13, 0, 0, Math.PI * 2); x.fill();
      x.beginPath(); x.ellipse(24, -4, 11, 8, -.2, 0, Math.PI * 2); x.fill();
      x.fillStyle = '#f9a8d4'; x.beginPath(); x.arc(22, -13, 4.5, 0, Math.PI * 2); x.fill(); x.beginPath(); x.arc(34, -2, 2, 0, Math.PI * 2); x.fill();
      x.fillStyle = '#111'; x.beginPath(); x.arc(28, -6, 1.5, 0, Math.PI * 2); x.fill();
      x.strokeStyle = '#9ca3af'; x.lineWidth = 1.6; x.beginPath(); x.moveTo(-24, 2); x.quadraticCurveTo(-40, 0, -46, 10); x.stroke();
      x.strokeStyle = '#6b7280'; x.lineWidth = 2.2; for (const px of [-12, 12]) { x.beginPath(); x.moveTo(px, 10); x.lineTo(px + (morte ? 0 : 2), 17); x.stroke(); }
      x.restore();
    },
    /** Tube à essai en verre avec liquide teinté. */
    tube(x, cx, y0, h, w, liquide, a = 1, niveau = .55) {
      x.save(); x.globalAlpha = a;
      const yl = y0 + h * (1 - niveau);
      const gl = x.createLinearGradient(cx - w / 2, 0, cx + w / 2, 0); gl.addColorStop(0, liquide[0]); gl.addColorStop(.5, liquide[1]); gl.addColorStop(1, liquide[0]);
      x.fillStyle = gl; x.beginPath(); x.moveTo(cx - w / 2, yl); x.lineTo(cx - w / 2, y0 + h - w / 2); x.arc(cx, y0 + h - w / 2, w / 2, Math.PI, 0, true); x.lineTo(cx + w / 2, yl); x.closePath(); x.fill();
      x.strokeStyle = 'rgba(220,235,245,.75)'; x.lineWidth = 1.4; x.beginPath(); x.moveTo(cx - w / 2, y0); x.lineTo(cx - w / 2, y0 + h - w / 2); x.arc(cx, y0 + h - w / 2, w / 2, Math.PI, 0, true); x.lineTo(cx + w / 2, y0); x.stroke();
      x.strokeStyle = 'rgba(255,255,255,.45)'; x.lineWidth = 1.2; x.beginPath(); x.moveTo(cx - w / 2 + 3, y0 + 4); x.lineTo(cx - w / 2 + 3, y0 + h - w / 2); x.stroke();
      x.restore();
    },
  };

  window.Etapes = { lancer, lisse, rampe, entre, Peint };
})();
