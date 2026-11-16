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
    /* Deuxième passe (15 novembre 2026, « agrandir les figures elles-mêmes, pas seulement le texte autour ») : une colonne
     * de la disposition peut être une COLONNE DE TEXTE, `{ texte: [noms de blocs] }`. Les phrases écrites dans ces blocs
     * par le dessin d'origine ne sont plus agrandies telles quelles : elles sont relevées (à chaque moment de la vue et à
     * la fin), remises en paragraphes (une ligne qui commence par une minuscule continue la phrase d'avant) et récrites
     * en colonne, coupées à la ligne, à une taille choisie EN PIXELS À L'ÉCRAN (u(px) = px / échelle) : on prend la plus
     * grande écriture (22 → 17 px) qui fait tenir la colonne en hauteur, avec la figure la plus grande possible (pleine
     * hauteur, au moins la moitié de la largeur), comme `disposer` de chimie/transformations-deux-sens-tableau. L'écriture
     * en direct garde son rythme (un texte coupé en morceaux partage sa durée), les repères posés sur ces phrases les
     * suivent. Les traits de ces blocs (cadres, soulignés) ne sont pas repris. `disposition` peut aussi être une fonction
     * (L, k) : la disposition change alors avec la scène (ex. une animation, puis un tableau). */
    const POSES = {};   // vue → { cle, map: nom → {x0,y0,X,Y,z} | {texte, X, Y, lay} }
    /* (17 novembre 2026) Cadre du lecteur de cours, ~1025 px de large (L entre 800 et 1000) : les blocs servent aussi là,
     * mais seulement s'ils AGRANDISSENT la figure (toutes les figures à l'échelle ≥ 1) ; sinon la disposition d'origine,
     * centrée, reste la plus grande. */
    const estLarge = v => {
      if (!(v.blocs && v.disposition)) return false;
      if (scene.L >= 1000) return true;
      if (scene.L < 800) return false;
      try { const figs = Object.values(disposer(v, scene.L, scene.craie)).filter(p => !p.texte); return figs.length > 0 && figs.every(p => p.z >= 1); } catch (_) { return false; }
    };
    const estTexte = col => !!col && !Array.isArray(col) && Array.isArray(col.texte);
    const dispoDe = v => (typeof v.disposition === 'function' ? v.disposition(scene.L, k()) : v.disposition);
    const dansB = (q, px, py) => px >= q[0] && px < q[2] && py >= q[1] && py < q[3];
    const cleT = (nom, x, y) => nom + '|' + Math.round(x) + ',' + Math.round(y);
    const RELEVES = {};
    /** Les phrases des blocs de texte, relevées à chaque moment de la vue (sans rien dessiner) : nom → [{s, x, y, taille…}]. */
    function relever(c, v) {
      const cle = S.vue + '|' + JSON.stringify(P), memo = RELEVES[cle];
      if (memo && memo.B === v.blocs) return memo.par;
      const B = v.blocs, par = {}, x = c.ctx;
      const temps = [...new Set([...Object.values(v.moments || {}), v.fin])].filter(Number.isFinite).sort((a, b) => a - b);
      const sv = { t: S.t, vu: S.vu, cur: c.cur, ct: c.t, tip: c.tip, complet: c.complet };
      const rien = function () { return this; }, FN = ['direct', 'trait', 'rect', 'cercle', 'point', 'repere', 'texte'];
      try {
        for (const t of temps) {
          S.t = t; S.vu = {};
          const D = dispoDe(v), noms = (D.colonnes || []).filter(estTexte).flatMap(col => col.texte);
          if (!noms.length) continue;
          x.save(); x.beginPath(); x.rect(0, 0, 0, 0); x.clip();
          for (const f of FN) c[f] = rien;
          c.texte = function (s, tx, ty, o = {}) {
            const ta = o.taille ?? 18, ay = ty - ta * .35, nom = noms.find(n => B[n] && dansB(B[n], tx, ay));
            if (nom) {
              const L = (par[nom] ||= {}), q = cleT(nom, tx, ty), a = L[q]; s = String(s);
              if (!a || s.length > a.s.length) L[q] = { cle: q, s, x: tx, y: ty, taille: ta, align: o.align || 'left', couleur: o.couleur, gras: o.gras };
            }
            return this;
          };
          try { v.dessiner(c, k()); } catch (e) { console.warn('[etapes] relevé des textes', e); }
          finally { x.restore(); for (const f of FN) delete c[f]; }
        }
      } finally { S.t = sv.t; S.vu = sv.vu; c.cur = sv.cur; c.t = sv.ct; c.tip = sv.tip; c.complet = sv.complet; }
      for (const n of Object.keys(par)) par[n] = Object.values(par[n]);
      RELEVES[cle] = { B, par };
      return par;
    }
    /** Les phrases d'un bloc remises en paragraphes : [{runs, taille, ecart}]. */
    function paragraphes(c, items) {
      const gauche = it => { const l = c.largeurTexte(it.s, it.taille); return it.align === 'center' ? it.x - l / 2 : it.align === 'right' ? it.x - l : it.x; };
      const lignes = [];
      for (const it of items.map(o => ({ ...o, alias: undefined })).sort((a, b) => a.y - b.y || a.x - b.x)) {
        const l = lignes.find(q => Math.abs(q.y - it.y) <= Math.max(q.taille, it.taille) * .45);
        // deux phrases au même endroit (l'une remplace l'autre au fil de la scène) : une seule place, la plus longue
        const autre = l && l.runs.find(r => Math.abs(r.x - it.x) < 4 && r.align === it.align);
        if (autre) {
          const [garde, laisse] = autre.s.length >= it.s.length ? [autre, it] : [it, autre];
          garde.alias = [...(garde.alias || []), laisse.cle, ...(laisse.alias || [])];
          if (garde === it) l.runs[l.runs.indexOf(autre)] = it;
          continue;
        }
        if (l) { l.runs.push(it); l.taille = Math.max(l.taille, it.taille); } else lignes.push({ y: it.y, taille: it.taille, runs: [it] });
      }
      lignes.sort((a, b) => a.y - b.y);
      // deux morceaux d'une même ligne très écartés (deux légendes côte à côte) : deux paragraphes
      const morceaux = [];
      for (const l of lignes) {
        l.runs.sort((a, b) => gauche(a) - gauche(b));
        let cur = null, fin = -Infinity;
        for (const r of l.runs) {
          const g = gauche(r);
          if (!cur || g - fin > 1.5 * l.taille) { cur = { y: l.y, taille: l.taille, runs: [] }; morceaux.push(cur); }
          cur.runs.push(r); fin = Math.max(fin, g + c.largeurTexte(r.s, r.taille));
        }
      }
      const paras = []; let prev = null;
      for (const l of morceaux) {
        const debut = l.runs[0].s.trim(), fin = prev ? prev.runs[prev.runs.length - 1].s.trim() : '';
        const suite = prev && l.y - prev.y > .3 * l.taille && l.y - prev.y <= 1.8 * Math.max(l.taille, prev.taille) && (/^[a-zàâçéèêëîïôûùüÿœ(«]/.test(debut) || /,$/.test(fin)) && l.runs[0].couleur === prev.runs[prev.runs.length - 1].couleur && !/ = /.test(debut);
        if (suite) paras[paras.length - 1].runs.push(...l.runs);
        else paras.push({ runs: [...l.runs], taille: l.taille, ecart: !prev || l.y - prev.y > 1.95 * l.taille });
        prev = l;
      }
      return paras;
    }
    /** Compose des paragraphes dans une colonne de largeur W, écriture t (cadre) : { h, pieces: cle → [{dx, dy, s, taille}] }. */
    function composer(c, paras, W, t, base) {
      const pieces = {}, boites = {}; let y = 0;
      const larg = (s, ta, gras) => { c.ctx.font = `${gras ? '700 ' : ''}${ta}px ${window.Tableau.POLICE}`; return c.ctx.measureText(s).width; };
      paras.forEach((p, i) => {
        const ta = t * Math.min(1.2, Math.max(.92, p.taille / base)), pas = ta * 1.24, esp = larg(' ', ta);
        if (i) y += (p.ecart ? ta * .5 : ta * .12);
        y += ta; let lx = 0, ly = y;
        for (const r of p.runs) {
          const L = (pieces[r.cle] ||= []);
          for (const m of r.s.trim().split(/\s+/)) {
            if (!m) continue;
            const w = larg(m, ta, r.gras);
            if (lx > 0 && lx + esp + w > W) { ly += pas; lx = 0; }
            const x0 = lx > 0 ? lx + esp : 0, der = L[L.length - 1];
            if (der && der.dy === ly && Math.abs(der.dx + der.w - (x0 - esp)) < .5) { der.s += ' ' + m; der.w = x0 + w - der.dx; }
            else L.push({ dx: x0, dy: ly, s: m, w, taille: ta });
            lx = x0 + w;
            const b = (boites[r.cle] ||= [Infinity, Infinity, -Infinity, -Infinity]);
            b[0] = Math.min(b[0], x0); b[1] = Math.min(b[1], ly - ta * .95); b[2] = Math.max(b[2], x0 + w); b[3] = Math.max(b[3], ly + ta * .3);
          }
        }
        y = ly;
        for (const r of p.runs) for (const a of r.alias || []) { pieces[a] = pieces[r.cle]; boites[a] = boites[r.cle]; }
      });
      return { h: y + t * .35, pieces, boites };
    }
    function disposer(v, L, c) {
      const B = v.blocs, D = dispoDe(v), mixte = D.colonnes.some(estTexte);
      const par = mixte ? relever(c, v) : null;
      const cle = [L, (scene.s || 1).toFixed(4), JSON.stringify(D)].join('|'), memo = POSES[S.vue];
      if (memo && memo.cle === cle && memo.B === B && memo.par === par) return memo.map;
      const map = mixte ? disposerMixte(v, D, L, c, par) : disposerBlocs(v, D, L);
      POSES[S.vue] = { cle, B, par, map };
      return map;
    }
    function disposerBlocs(v, D, L) {
      const B = v.blocs, map = {};
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
      return map;
    }
    /** Colonnes de figure (mises à l'échelle, pleine hauteur) et colonnes de texte (récrites à la ligne). */
    function disposerMixte(v, D, L, c, par) {
      const B = v.blocs, map = {}, s = scene.s || 1, u = px => px / s;
      const M = D.marge ?? 12, E = D.ecart ?? 22, HT = 420, Ha = HT - 2 * M;
      const dim = n => { const b = B[n]; return { w: b[2] - b[0], h: b[3] - b[1], zmax: b[4] || D.zmax || 3 }; };
      const cols = D.colonnes.map(col => {
        if (estTexte(col)) {
          const items = col.texte.map(n => paragraphes(c, par[n] || [])).flat();
          const tailles = col.texte.flatMap(n => (par[n] || []).map(it => it.taille)).sort((a, b) => a - b);
          // `haut` : des blocs de figure posés en tête de la colonne de texte (une image et sa légende), à sa largeur
          const haut = (col.haut || []).map(n => ({ n, ...dim(n) })), bas = (col.bas || []).map(n => ({ n, ...dim(n) }));
          haut.push(...bas.map(d => ({ ...d, bas: true })));
          return { texte: col.texte, haut, paras: items, base: tailles.length ? tailles[Math.floor(tailles.length / 2)] : 16, poids: col.poids || 1, max: col.max };
        }
        const ds = col.map(dim), w = Math.max(...ds.map(d => d.w)), h = ds.reduce((a, d) => a + d.h, 0);
        return { col, ds, w, z0: Math.min(Math.min(...ds.map(d => d.zmax)), (Ha - E * (col.length - 1)) / h) };
      });
      const fig = cols.filter(q => !q.texte), txt = cols.filter(q => q.texte), gaps = E * (cols.length - 1);
      const figN = fig.reduce((a, q) => a + q.w * q.z0, 0), fig0 = Math.min(figN, (D.partMax ?? .64) * L);
      let choix = null;
      essai: for (const px of D.tailles || [22, 21, 20, 19, 18, 17]) {
        for (const f of [1, .94, .88, .82, .76, .7, .64, .58, .52]) {
          const figW = fig0 * f;
          if (f < 1 && figW < (D.partMin ?? .5) * L) break;
          const t = u(px), libre = L - 2 * M - gaps - figW, poids = txt.reduce((a, q) => a + q.poids, 0);
          if (libre < txt.length * t * (D.colMin ?? 8.5)) continue;
          const lays = txt.map(q => {
            const W = Math.min(libre * q.poids / poids, t * (q.max || 24));
            const lay = composer(c, q.paras, W, t, q.base), sh = q.haut.reduce((a, d) => a + d.h, 0);
            const zh = q.haut.length ? Math.min(...q.haut.map(d => Math.min(d.zmax, W / d.w)), (Ha - lay.h - E * q.haut.length) / sh) : 0;
            const hh = q.haut.reduce((a, d) => a + d.h * zh + E, 0);
            return { W, zh: q.haut.length && zh < (D.zhautMin ?? .9) ? -1 : zh, hh, lay };
          });
          choix = { px, f, t, lays };
          if (lays.every(l => l.zh >= 0 && l.lay.h + l.hh <= Ha + .5)) break essai;
        }
      }
      if (!choix) return disposerBlocs(v, { ...D, colonnes: D.colonnes.filter(q => !estTexte(q)) }, L);
      fig.forEach(q => { q.z = q.z0 * choix.f * fig0 / figN; q.lw = q.w * q.z; });
      txt.forEach((q, i) => { Object.assign(q, { lay: choix.lays[i].lay, lw: choix.lays[i].W, zh: choix.lays[i].zh, hh: choix.lays[i].hh }); });
      const reste = L - 2 * M - gaps - cols.reduce((a, q) => a + q.lw, 0), ecart = Math.max(0, reste) / (cols.length + 1);
      let x = M + ecart + (reste < 0 ? reste / 2 : 0);
      for (const q of cols) {
        if (q.texte) {
          let Y = M + Math.max(0, (Ha - q.lay.h - q.hh) / 2);
          for (const d of q.haut.filter(d => !d.bas)) { map[d.n] = { x0: B[d.n][0], y0: B[d.n][1], X: x + (q.lw - d.w * q.zh) / 2, Y, z: q.zh }; Y += d.h * q.zh + E; }
          for (const n of q.texte) map[n] = { texte: true, X: x, Y, W: q.lw, lay: q.lay, px: choix.px };
          Y += q.lay.h + E;
          for (const d of q.haut.filter(d => d.bas)) { map[d.n] = { x0: B[d.n][0], y0: B[d.n][1], X: x + (q.lw - d.w * q.zh) / 2, Y, z: q.zh }; Y += d.h * q.zh + E; }
        } else {
          const hz = q.ds.reduce((a, d) => a + d.h * q.z, 0) + E * (q.col.length - 1);
          let yy = M + Math.max(0, (Ha - hz) / 2);
          q.col.forEach((n, i) => { const d = q.ds[i]; map[n] = { x0: B[n][0], y0: B[n][1], X: x + (q.w - d.w) * q.z / 2, Y: yy, z: q.z }; yy += d.h * q.z + E; });
        }
        x += q.lw + E + ecart;
      }
      return map;
    }
    const PIECES_FN = ['direct', 'trait', 'rect', 'cercle', 'point'];
    /** Le dessin de la vue rejoué bloc par bloc (tableau large). */
    function dessinerBlocs(c, v) {
      const blocs = v.blocs, map = disposer(v, scene.L, c), x = c.ctx, e = c.echelle, cadre = c.cadre;
      const aire = q => (q[2] - q[0]) * (q[3] - q[1]);
      const recouvre = (q, b) => q[0] < b[2] && q[2] > b[0] && q[1] < b[3] && q[3] > b[1];
      let complet = true, tip = null, cur = 0;
      const proto = Object.getPrototypeOf(c);
      for (const [nom, p] of Object.entries(map)) {
        const b = blocs[nom];
        c.cur = 0; c.tip = null; c.complet = true;
        // un bloc plus petit qui chevauche celui-ci (un texte sorti de la figure) en est retiré : il est dessiné à sa place ;
        // un bloc de texte est toujours retiré des figures
        const trous = Object.entries(map).filter(([n, q]) => n !== nom && recouvre(blocs[n], b) && (aire(blocs[n]) < aire(b) || (q.texte && !p.texte))).map(([n]) => blocs[n]);
        const dedans = (px, py) => dansB(b, px, py) && !trous.some(q => dansB(q, px, py));
        x.save();
        if (p.texte) {
          // ── colonne de texte : les traits du bloc avancent l'horloge sans rien dessiner, les phrases sont récrites ──
          const lay = p.lay, coupeTout = nomF => function (...a) { x.save(); x.beginPath(); x.rect(0, 0, 0, 0); x.clip(); try { return proto[nomF].apply(this, a); } finally { x.restore(); } };
          for (const nomF of PIECES_FN) c[nomF] = coupeTout(nomF);
          c.cadre = null;
          c.texte = function (s, tx, ty, o = {}) {
            const ta = o.taille ?? 18; s = String(s);
            if (!dedans(tx, ty - ta * .35)) return proto.texte.call(this, s, tx, ty, { ...o, alpha: 0 });
            const pcs = lay.pieces[cleT(nom, tx, ty)], duree = o.duree ?? Math.max(.1, s.length / 28), opt = { couleur: o.couleur, gras: o.gras, alpha: o.alpha };
            if (!pcs || !pcs.length) return proto.texte.call(this, s, tx, ty, { ...o, alpha: 0 });
            const tout = pcs.map(q => q.s).join(' ');
            if (tout.replace(/\s+/g, ' ') !== s.trim().replace(/\s+/g, ' ')) return proto.texte.call(this, s, p.X + pcs[0].dx, p.Y + pcs[0].dy, { ...opt, taille: pcs[0].taille, duree });
            for (const q of pcs) proto.texte.call(this, q.s, p.X + q.dx, p.Y + q.dy, { ...opt, taille: q.taille, duree: duree * Math.max(1, q.s.length) / Math.max(1, tout.length) });
            return this;
          };
          c.repere = function (id, rx, ry, w, h, label) {
            if (!dedans(rx + w / 2, ry + h / 2)) return this;
            const R = [Infinity, Infinity, -Infinity, -Infinity]; let proche = null, dMin = Infinity;
            for (const [q, bt] of Object.entries(lay.boites)) {
              if (!q.startsWith(nom + '|')) continue;
              const [ax, ay] = q.slice(nom.length + 1).split(',').map(Number);
              if (ax >= rx - 6 && ax <= rx + w + 6 && ay >= ry - 6 && ay <= ry + h + 6) { R[0] = Math.min(R[0], bt[0]); R[1] = Math.min(R[1], bt[1]); R[2] = Math.max(R[2], bt[2]); R[3] = Math.max(R[3], bt[3]); }
              const d = Math.hypot(ax - (rx + w / 2), ay - (ry + h / 2)); if (d < dMin) { dMin = d; proche = bt; }
            }
            const r = R[0] < Infinity ? R : proche; if (!r) return this;
            return proto.repere.call(this, id, p.X + r[0] - 4, p.Y + r[1] - 3, r[2] - r[0] + 8, r[3] - r[1] + 6, label);
          };
          try { v.dessiner(c, k()); }
          finally { x.restore(); c.cadre = cadre; for (const f of [...PIECES_FN, 'texte', 'repere']) delete c[f]; }
          complet = complet && c.complet; cur = Math.max(cur, c.cur);
          if (c.tip) tip = c.tip;
          continue;
        }
        x.translate(p.X - p.x0 * p.z, p.Y - p.y0 * p.z); x.scale(p.z, p.z);
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
        const coupe = nomF => function (...a) { x.save(); decouper(); try { return proto[nomF].apply(this, a); } finally { x.restore(); } };
        for (const nomF of PIECES_FN) c[nomF] = coupe(nomF);
        c.texte = function (s, tx, ty, o = {}) { return proto.texte.call(this, s, tx, ty, dedans(tx, ty - (o.taille ?? 18) * .35) ? o : { ...o, alpha: 0 }); };
        c.repere = function (id, rx, ry, w, h, label) { return dedans(rx + w / 2, ry + h / 2) ? proto.repere.call(this, id, rx, ry, w, h, label) : this; };
        try { v.dessiner(c, k()); }
        finally { x.restore(); c.echelle = e; c.cadre = cadre; for (const f of [...PIECES_FN, 'texte', 'repere']) delete c[f]; }
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
      const tri = Object.entries(disposer(v, scene.L, scene.craie)).filter(([, p]) => !p.texte).sort(([a], [b]) => aire(v.blocs[a]) - aire(v.blocs[b]));   // le plus petit d'abord
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
      if (estLarge(v)) { dessinerBlocs(c, v); return c.fin(); }
      // (17 novembre 2026, règle 9 : « pas de titre interne qui répète la diapositive ») hors disposition en blocs, le titre
      // de la vue (écrit en cyan tout en haut à gauche) est écrit invisible : l'écriture en direct garde son rythme.
      const texte = Object.getPrototypeOf(c).texte;
      c.texte = function (t, tx, ty, o = {}) { return texte.call(this, t, tx, ty, ty <= 30 && tx <= 20 && o.couleur === 'cyan' ? { ...o, alpha: 0 } : o); };
      try {
        if (scene.L > 760) { c.ctx.save(); c.ctx.translate((scene.L - 760) / 2, 0); try { v.dessiner(c, k()); } finally { c.ctx.restore(); } }
        else v.dessiner(c, k());
      } finally { delete c.texte; }
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
    window.__etapes = { S, P, scene, POSES, RELEVES, playUntil, setTime, setParameters, etat: () => ({ ce_qui_se_voit: ceQuiSeVoit(), moments: V().moments, statut: statut() }) };
    return window.__etapes;
  }

  /* ── Petits outils de peinture partagés (règle 7 : le vivant peint, la craie pour les légendes) ── */
  const rgb = c => { const n = parseInt(String(c).slice(1), 16); return [(n >> 16) & 255, (n >> 8) & 255, n & 255]; };
  /** Mélange une couleur #rrggbb vers le noir (f < 0) ou le blanc (f > 0) ; |f| de 0 à 1. */
  const teinte = (c, f) => { const v = rgb(c).map(k => Math.round(f < 0 ? k * (1 + f) : k + (255 - k) * f)); return `rgb(${v[0]},${v[1]},${v[2]})`; };
  const Peint = {
    teinte,
    /**
     * Un tube peint le long d’un chemin (squelette d’un brin d’ADN, filament) : ombre douce, bord foncé, corps coloré,
     * reflet clair décalé vers la lumière (en haut à gauche). `chemin()` trace le chemin (beginPath compris) ;
     * o.reflet = [dx, dy] du reflet (par défaut vers le haut), o.ombre = false pour ne pas poser d’ombre.
     */
    ruban(x, chemin, couleur, ep = 6, a = 1, o = {}) {
      if (a <= 0) return;
      x.save(); x.globalAlpha *= a; x.lineCap = o.cap || 'round'; x.lineJoin = 'round';
      if (o.ombre !== false) { x.shadowColor = 'rgba(0,0,0,.45)'; x.shadowBlur = ep * .9; x.shadowOffsetY = ep * .3; }
      x.strokeStyle = teinte(couleur, -.5); x.lineWidth = ep; chemin(); x.stroke();
      x.shadowColor = 'transparent';
      x.strokeStyle = couleur; x.lineWidth = ep * .66; chemin(); x.stroke();
      const [dx, dy] = o.reflet || [0, -ep * .17];
      x.translate(dx, dy); x.strokeStyle = teinte(couleur, .55); x.globalAlpha *= .85; x.lineWidth = Math.max(.8, ep * .22); chemin(); x.stroke();
      x.restore();
    },
    /** Une base azotée en bâtonnet arrondi de (x1,y1) à (x2,y2), ombrée en volume (reflet sur le côté gauche du bâtonnet). */
    barreau(x, x1, y1, x2, y2, couleur, ep = 6, a = 1) {
      const L = Math.hypot(x2 - x1, y2 - y1) || 1, nx = -(y2 - y1) / L, ny = (x2 - x1) / L, s = nx + ny > 0 ? -1 : 1;
      Peint.ruban(x, () => { x.beginPath(); x.moveTo(x1, y1); x.lineTo(x2, y2); }, couleur, ep, a, { cap: 'butt', ombre: false, reflet: [s * nx * ep * .17, s * ny * ep * .17] });
    },
    /** Une bille peinte (nucléotide libre, molécule) : dégradé sphérique, reflet, ombre portée légère. */
    bille(x, cx, cy, r, couleur, a = 1) {
      if (a <= 0) return;
      x.save(); x.globalAlpha *= a;
      x.fillStyle = 'rgba(0,0,0,.28)'; x.beginPath(); x.ellipse(cx + r * .15, cy + r * .75, r * .9, r * .32, 0, 0, Math.PI * 2); x.fill();
      const g = x.createRadialGradient(cx - r * .35, cy - r * .4, r * .08, cx, cy, r);
      g.addColorStop(0, teinte(couleur, .7)); g.addColorStop(.35, couleur); g.addColorStop(1, teinte(couleur, -.55));
      x.fillStyle = g; x.beginPath(); x.arc(cx, cy, r, 0, Math.PI * 2); x.fill();
      x.restore();
    },
    /** Cellule animale : cytoplasme lumineux (rose corail par défaut), membrane nette à double bord, ombre douce, granulations.
     *  (17 novembre 2026 : couleurs plus vives et volume — halo clair en haut à gauche, bord plus dense, liseré brillant.) */
    cellule(x, cx, cy, rx, ry, a = 1, teinte) {
      if (a <= 0) return;
      x.save(); x.globalAlpha *= a;
      const R = Math.max(rx, ry), t = teinte || ['rgba(255,226,214,.92)', 'rgba(255,150,150,.82)', 'rgba(226,84,116,.88)'];
      // ombre portée douce : la cellule se détache du tableau
      x.save(); x.shadowColor = 'rgba(0,0,0,.5)'; x.shadowBlur = R * .22; x.shadowOffsetY = R * .06;
      const g = x.createRadialGradient(cx - rx * .3, cy - ry * .35, R * .05, cx, cy, R);
      g.addColorStop(0, t[0]); g.addColorStop(.62, t[1]); g.addColorStop(1, t[2]);
      x.fillStyle = g; x.beginPath(); x.ellipse(cx, cy, rx, ry, 0, 0, Math.PI * 2); x.fill(); x.restore();
      // granulations du cytoplasme (deux tons) et reflet
      x.save(); x.beginPath(); x.ellipse(cx, cy, rx, ry, 0, 0, Math.PI * 2); x.clip();
      for (let i = 0; i < 30; i++) { const a2 = i * 2.39996, r = .22 + .68 * ((i * 37) % 23) / 23; x.fillStyle = i % 3 ? 'rgba(150,40,80,.3)' : 'rgba(255,245,235,.4)'; x.beginPath(); x.arc(cx + Math.cos(a2) * rx * r, cy + Math.sin(a2) * ry * r, Math.max(1.1, R / 46), 0, Math.PI * 2); x.fill(); }
      const h = x.createRadialGradient(cx - rx * .38, cy - ry * .48, 1, cx - rx * .38, cy - ry * .48, R * .6); h.addColorStop(0, 'rgba(255,255,255,.32)'); h.addColorStop(1, 'rgba(255,255,255,0)');
      x.fillStyle = h; x.fillRect(cx - rx, cy - ry, 2 * rx, 2 * ry); x.restore();
      // membrane plasmique : bord foncé + liseré clair
      const e = Math.max(1.6, R / 34);
      x.strokeStyle = 'rgba(136,28,72,.95)'; x.lineWidth = e; x.beginPath(); x.ellipse(cx, cy, rx, ry, 0, 0, Math.PI * 2); x.stroke();
      x.strokeStyle = 'rgba(255,214,224,.7)'; x.lineWidth = e * .45; x.beginPath(); x.ellipse(cx, cy, Math.max(1, rx - e * .9), Math.max(1, ry - e * .9), 0, 0, Math.PI * 2); x.stroke();
      x.restore();
    },
    /** Noyau en interphase : violet-mauve, enveloppe double, pores, nucléole, chromatine en fins filaments. */
    noyau(x, cx, cy, r, a = 1, o = {}) {
      x.save(); x.globalAlpha = a;
      const g = x.createRadialGradient(cx - r * .3, cy - r * .3, 2, cx, cy, r);
      g.addColorStop(0, 'rgba(240,214,255,.97)'); g.addColorStop(.6, 'rgba(190,132,246,.94)'); g.addColorStop(1, 'rgba(124,58,216,.94)');
      x.save(); x.shadowColor = 'rgba(30,0,60,.55)'; x.shadowBlur = r * .3; x.shadowOffsetY = r * .08;
      x.fillStyle = g; x.beginPath(); x.arc(cx, cy, r, 0, Math.PI * 2); x.fill(); x.restore();
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
          x.strokeStyle = j % 2 ? 'rgba(76,20,140,.7)' : 'rgba(104,40,170,.6)'; x.beginPath(); x.moveTo(pts[0][0], pts[0][1]);
          for (let i = 1; i < pts.length - 1; i++) x.quadraticCurveTo(pts[i][0], pts[i][1], (pts[i][0] + pts[i + 1][0]) / 2, (pts[i][1] + pts[i + 1][1]) / 2);
          x.stroke();
        }
      }
      if (o.nucleole !== false) { const gn = x.createRadialGradient(cx + r * .2, cy - r * .1, 1, cx + r * .25, cy - r * .05, r * .22); gn.addColorStop(0, 'rgba(168,85,247,1)'); gn.addColorStop(.35, 'rgba(107,33,168,1)'); gn.addColorStop(1, 'rgba(59,7,100,1)'); x.fillStyle = gn; x.beginPath(); x.arc(cx + r * .25, cy - r * .05, r * .2, 0, Math.PI * 2); x.fill(); }
      { const hn = x.createRadialGradient(cx - r * .4, cy - r * .45, 1, cx - r * .4, cy - r * .45, r * .7); hn.addColorStop(0, 'rgba(255,255,255,.3)'); hn.addColorStop(1, 'rgba(255,255,255,0)'); x.fillStyle = hn; x.beginPath(); x.arc(cx, cy, r, 0, Math.PI * 2); x.fill(); }   // reflet : un volume
      x.strokeStyle = 'rgba(76,29,149,.98)'; x.lineWidth = Math.max(1.2, r / 24); x.beginPath(); x.arc(cx, cy, r, 0, Math.PI * 2); x.stroke();
      if (o.double) { x.beginPath(); x.arc(cx, cy, r + Math.max(2, r / 22), 0, Math.PI * 2); x.stroke();
        x.fillStyle = 'rgba(255,240,250,.95)'; for (let i = 0; i < 12; i++) { const a2 = i * Math.PI / 6 + .2; x.beginPath(); x.arc(cx + Math.cos(a2) * (r + r / 44 + 1), cy + Math.sin(a2) * (r + r / 44 + 1), Math.max(1.6, r / 26), 0, Math.PI * 2); x.fill(); } }
      x.restore();
    },
    /** Un chromosome peint : `pts` = ligne médiane [[x,y],…] d’une chromatide ; deux chromatides si `deux` (écart `ecart`). */
    chromatide(x, pts, couleur, epaisseur = 7, a = 1) {
      if (a <= 0) return;
      x.save(); x.globalAlpha *= a; x.lineCap = 'round'; x.lineJoin = 'round';
      const trace = (dx = 0, dy = 0) => { x.beginPath(); pts.forEach(([px, py], i) => (i ? x.lineTo(px + dx, py + dy) : x.moveTo(px + dx, py + dy))); };
      // (17 novembre 2026) trois couches : contour sombre avec ombre douce, corps vif, reflet clair → un bâtonnet en volume
      x.save(); x.shadowColor = 'rgba(0,0,0,.45)'; x.shadowBlur = epaisseur * .6; x.shadowOffsetY = epaisseur * .18;
      x.strokeStyle = teinte(couleur[1], -.45); x.lineWidth = epaisseur; trace(); x.stroke(); x.restore();
      x.strokeStyle = couleur[1]; x.lineWidth = epaisseur * .78; trace(); x.stroke();
      x.strokeStyle = couleur[0]; x.lineWidth = epaisseur * .34; trace(-epaisseur * .15, -epaisseur * .15); x.stroke();
      x.restore();
    },
    VIOLET: ['#f0d4ff', '#9333ea'], BLEU: ['#c7d2fe', '#4f46e5'],
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
      if (a <= 0) return;
      x.save(); x.globalAlpha *= a; x.translate(cx, cy); x.scale(s, s);
      if (!morte) { x.fillStyle = 'rgba(0,0,0,.3)'; x.beginPath(); x.ellipse(2, 16, 30, 4, 0, 0, Math.PI * 2); x.fill(); }
      if (morte) x.scale(1, -1);
      const TAU2 = Math.PI * 2, pel = morte ? ['#d1d5db', '#9ca3af', '#4b5563'] : ['#ffffff', '#e5e7eb', '#8b95a5'];
      // queue rose
      x.strokeStyle = '#f9a8d4'; x.lineWidth = 2.4; x.lineCap = 'round'; x.beginPath(); x.moveTo(-22, 3); x.bezierCurveTo(-34, 2, -36, 12, -48, 8); x.stroke();
      // pattes
      x.fillStyle = '#f9a8d4'; for (const px of [-12, 12]) { x.beginPath(); x.ellipse(px + (morte ? 0 : 2), 13, 4.5, 2.6, 0, 0, TAU2); x.fill(); }
      // corps en poire, tête pointue
      const g = x.createRadialGradient(-6, -8, 2, 0, 0, 30); g.addColorStop(0, pel[0]); g.addColorStop(.55, pel[1]); g.addColorStop(1, pel[2]);
      x.fillStyle = g; x.beginPath(); x.ellipse(-2, 0, 23, 13.5, 0, 0, TAU2); x.fill();
      x.beginPath(); x.moveTo(12, -11); x.quadraticCurveTo(30, -12, 38, -1); x.quadraticCurveTo(30, 8, 12, 10); x.closePath(); x.fill();
      // oreilles (une derrière, une devant) rose à l'intérieur
      for (const [ox, oy, r] of [[17, -13, 5.5], [22, -12, 6.5]]) { x.fillStyle = pel[1]; x.beginPath(); x.arc(ox, oy, r, 0, TAU2); x.fill(); x.fillStyle = '#fbcfe8'; x.beginPath(); x.arc(ox, oy, r * .6, 0, TAU2); x.fill(); }
      // museau, moustaches, œil (une croix si elle est morte)
      x.fillStyle = '#f472b6'; x.beginPath(); x.arc(38, -1, 2.2, 0, TAU2); x.fill();
      x.strokeStyle = 'rgba(255,255,255,.7)'; x.lineWidth = .7; for (const dy of [-4, 0, 4]) { x.beginPath(); x.moveTo(34, 0); x.lineTo(43, dy + 1); x.stroke(); }
      if (morte) { x.strokeStyle = '#111827'; x.lineWidth = 1.4; x.beginPath(); x.moveTo(27, -6); x.lineTo(31, -2); x.moveTo(31, -6); x.lineTo(27, -2); x.stroke(); }
      else { x.fillStyle = '#111827'; x.beginPath(); x.arc(29, -4, 1.9, 0, TAU2); x.fill(); x.fillStyle = '#fff'; x.beginPath(); x.arc(29.6, -4.6, .6, 0, TAU2); x.fill(); }
      x.restore();
    },
    /** Tube à essai en verre avec liquide teinté. */
    tube(x, cx, y0, h, w, liquide, a = 1, niveau = .55) {
      x.save(); x.globalAlpha = a;
      const yl = y0 + h * (1 - niveau);
      const gl = x.createLinearGradient(cx - w / 2, 0, cx + w / 2, 0); gl.addColorStop(0, liquide[0]); gl.addColorStop(.5, liquide[1]); gl.addColorStop(1, liquide[0]);
      x.fillStyle = gl; x.beginPath(); x.moveTo(cx - w / 2, yl); x.lineTo(cx - w / 2, y0 + h - w / 2); x.arc(cx, y0 + h - w / 2, w / 2, Math.PI, 0, true); x.lineTo(cx + w / 2, yl); x.closePath(); x.fill();
      x.strokeStyle = 'rgba(220,235,245,.75)'; x.lineWidth = 1.4; x.beginPath(); x.moveTo(cx - w / 2, y0); x.lineTo(cx - w / 2, y0 + h - w / 2); x.arc(cx, y0 + h - w / 2, w / 2, Math.PI, 0, true); x.lineTo(cx + w / 2, y0); x.stroke();
      x.strokeStyle = 'rgba(255,255,255,.6)'; x.lineWidth = Math.max(1.2, w * .1); x.lineCap = 'round'; x.beginPath(); x.moveTo(cx - w / 2 + w * .2, y0 + 4); x.lineTo(cx - w / 2 + w * .2, y0 + h - w / 2); x.stroke();
      x.strokeStyle = 'rgba(255,255,255,.55)'; x.lineWidth = 1; x.beginPath(); x.ellipse(cx, yl, w / 2 - 1, Math.max(.8, w * .08), 0, 0, Math.PI * 2); x.stroke();   // ménisque
      x.strokeStyle = 'rgba(226,240,250,.85)'; x.lineWidth = 1.6; x.beginPath(); x.ellipse(cx, y0, w / 2 + 1.5, Math.max(1, w * .1), 0, 0, Math.PI * 2); x.stroke();   // bord du verre
      x.restore();
    },
  };

  window.Etapes = { lancer, lisse, rampe, entre, Peint };
})();
