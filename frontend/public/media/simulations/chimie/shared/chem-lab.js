/*
 * Laboratoires de chimie — moteur partagé, dessiné au tableau.
 * Chaque page fournit window.CHEM_LAB_CONFIG (missions, modèles, paramètres) ; ce script dessine le montage
 * et la courbe à la craie (shared/tableau/tableau.js), écrit en direct, et garde le pont avec le tuteur :
 * manifeste, état (variables, measurements, student_prediction, trial_history…) et commandes
 * start / run_trial / reset / set_variant / set_parameters / highlight / get_state / set_prediction.
 */
/*
 * États physiques dans les équations (règle du 16 novembre 2026 : « ajouter dans les équations l'état physique de chaque
 * élément », comme HCOOH(aq) + H₂O(l) ⇌ HCOO⁻(aq) + H₃O⁺(aq)). Au tableau seulement : la voix, la bulle et l'état envoyé
 * au tuteur gardent les équations sans états. Chaque espèce d'une équation (deux côtés autour de →, ⇌, ←) reçoit son
 * état, écrit en petit et en bas : H₂O (l) ; ions, molécules dissoutes (aq) ; métaux et précipités (s) ; H₂, HCl (g) ;
 * estérification (pas d'ion, un alcool ou un ester) : tout (l). e⁻, Ox, Red et les lettres A, C, D restent sans état.
 * La durée d'écriture reste celle de l'équation sans états : les instants des moments ne bougent pas.
 *   Etats.annote(s) : le texte avec les états (« (aq) ») ; Etats.cotes(gauche, droite) : deux côtés dessinés à part ;
 *   Etats.morceaux(liste) : une ligne à morceaux [côté, '⇌', côté…].
 */
(function () {
  'use strict';
  const T = window.Tableau; if (!T || T.Craie.__etats) return;
  const C = T.Craie, P = C.prototype; C.__etats = true;
  const SOLIDES = new Set(['Cu', 'Zn', 'Mg', 'Al', 'Ag', 'Fe', 'Pb', 'Ni', 'Sn', 'AgCl', 'CaF₂', 'Pt']);
  const GAZ = new Set(['H₂', 'O₂', 'Cl₂', 'HCl']);
  const EXCLUS = new Set(['A', 'C', 'D', 'I', 'Ox', 'Red', 'Réd']);
  const ETAT = String.raw`\((?:aq|l|s|g)\)`, FL = '(?:→|⇌|⇄|⇋|←)';
  const ESPECE = String.raw`(?:\((?:CH₃|C₂H₅)\)[₀-₉]*)?[A-Z](?:[A-Za-z₀-₉()–\-]*?[₀-₉A-Za-z)])?(?:[⁰¹²³⁴⁵⁶⁷⁸⁹]*[⁺⁻])?|e⁻`;
  const TERME = String.raw`(?:\d+\s?)?(?:${ESPECE})(?:\s?${ETAT})?`;
  const COTE = String.raw`${TERME}(?:\s*\+\s*${TERME})*`;
  const EQ = new RegExp(String.raw`(?<![\w₀-₉⁺⁻\[/])(${COTE})(\s*${FL}\s*)(${COTE})(?![\w₀-₉⁺⁻\]/·])`, 'g');
  const RE_COTE = new RegExp(`^${COTE}$`), RE_TERME = new RegExp(String.raw`^(\d+\s?)?(.*?)(\s?${ETAT})?$`);
  const decoupe = s => s.split(/\s*\+\s*/);
  const formule = t => { const m = t.trim().match(RE_TERME); return [m[1] || '', m[2], m[3] || '']; };
  const ion = f => /[⁺⁻]$/.test(f) && f !== 'e⁻';
  function etat(f, eq, ester) {
    if (f === 'e⁻') return '';
    if (EXCLUS.has(f)) return null;
    if (f === 'H₂O' || ester) return '(l)';
    if (ion(f)) return '(aq)';
    if (SOLIDES.has(f)) return '(s)';
    if (GAZ.has(f)) return '(g)';
    if (f === 'B' && !eq.includes('H₂O')) return null;
    return '(aq)';
  }
  function annoteEq(g, fl, d) {
    const eq = g + fl + d, fs = decoupe(g).concat(decoupe(d)).map(t => formule(t)[1]);
    if (fs.some(f => EXCLUS.has(f))) return null;
    const ions = fs.some(ion), ester = !ions && fs.some(f => /COO[A-Z(]|OH$/.test(f) && !f.endsWith('COOH'));
    const cote = s => {
      const out = [];
      for (const t of s.split(/(\s*\+\s*)/)) {
        if (/^\s*\+\s*$/.test(t)) { out.push(t); continue; }
        const [k, f, e] = formule(t);
        if (e) { out.push(t); continue; }
        const st = etat(f, eq, ester); if (st == null) return null;
        out.push(k + f + st);
      }
      return out.join('');
    };
    const a = cote(g), b = cote(d);
    return a == null || b == null ? null : a + fl + b;
  }
  const annote = s => String(s).replace(EQ, (m, g, fl, d) => annoteEq(g, fl, d) ?? m);
  /** Deux côtés dessinés à part (fonctions eqn, eqf de la page) : annotés ensemble, rendus séparés. */
  let pret = false;   // rien n'est annoté avant que la page soit chargée (sa mesure des durées se fait sans les états)
  const VUS = new Map(), ORIG = new Map();   // côté d'origine → côté annoté ; annoté → d'origine (durée d'écriture inchangée)
  const retiens = (o, a) => { if (a !== o) { VUS.set(o, a); ORIG.set(a, o); } return a; };
  function cotes(g, d) {
    if (!pret || typeof g !== 'string' || typeof d !== 'string' || !RE_COTE.test(g.trim()) || !RE_COTE.test(d.trim())) return [g, d];
    const r = annoteEq(g, ' → ', d); if (!r) return [g, d];
    const i = r.lastIndexOf(' → ');
    return [retiens(g, r.slice(0, i)), retiens(d, r.slice(i + 3))];
  }
  const piece = p => (typeof p === 'string' && VUS.has(p) ? VUS.get(p) : p);
  /** Ligne à morceaux : autour de chaque flèche, les morceaux voisins (côtés entiers « A + B », ou termes un à un
   *  « A », « + », « B ») forment l'équation ; chaque morceau reçoit les états de ses espèces. */
  function morceaux(liste) {
    if (!pret || !Array.isArray(liste)) return liste;
    const out = liste.slice(), estF = p => /^(→|⇌|←)$/.test(p), ok = p => typeof p === 'string' && (p.trim() === '+' || RE_COTE.test(p.trim()));
    out.forEach((p, i) => {
      if (!estF(p)) return;
      let a = i, b = i;
      while (a - 1 >= 0 && ok(out[a - 1]) && !estF(out[a - 1])) a--;
      while (b + 1 < out.length && ok(out[b + 1]) && !estF(out[b + 1])) b++;
      if (a === i || b === i) return;
      const g = out.slice(a, i).join(' ').replace(/\s*\+\s*/g, ' + '), d = out.slice(i + 1, b + 1).join(' ').replace(/\s*\+\s*/g, ' + ');
      if (!RE_COTE.test(g.trim()) || !RE_COTE.test(d.trim())) return;
      const r = annoteEq(g.trim(), ' → ', d.trim()); if (!r) return;
      const k = r.lastIndexOf(' → '), termes = decoupe(r.slice(0, k)).concat(decoupe(r.slice(k + 3)));
      let n = 0;
      for (let m = a; m <= b; m++) {
        if (m === i) continue;
        const q = out[m]; if (q.trim() === '+') continue;
        const nb = decoupe(q.trim()).length, part = termes.slice(n, n + nb).join(' + '); n += nb;
        out[m] = retiens(q, nb === 1 ? q.replace(q.trim(), part) : part);
      }
    });
    return out;
  }
  /** Liste de termes d'une équation (« H₂O₂ », « + », « ⇌ »…) : l'état de chaque terme (« (aq) », ou ''), ou null. */
  function liste(txts) {
    if (!pret) return null;
    const s = txts.join(' '), a = annote(s); if (a === s) return null;
    const b = a.split(' '); if (b.length !== txts.length) return null;
    return b.map((t, i) => t.slice(txts[i].length));
  }
  /** Ajoute un état au dernier morceau d'un terme (« H₂O » → « H₂O_{(l)} ») ; sa durée d'écriture reste celle de « H₂O ». */
  const ajoute = (p, e) => retiens(p, p + '_{' + e + '}');
  /** « X(aq) » écrit en petit et en bas : « X_{(aq)} ». */
  const marque = s => String(s).replace(new RegExp(`(?<=[A-Za-z₀-₉⁺⁻)}])\\s?(${ETAT})`, 'g'), '_{$1}');
  const plain = s => String(s).replace(/[_^]\{([^}]*)\}/g, '$1').replace(/[_^]/g, '').length;
  /** Largeur approchée d'un texte annoté (états en petit). */
  function largeur(ctx, s, taille) {
    ctx.font = `${taille}px ${T.POLICE}`;
    const etats = (String(s).match(new RegExp(ETAT, 'g')) || []).join('');
    return ctx.measureText(String(s).replace(new RegExp(ETAT, 'g'), '').replace(/[_^{}]/g, '')).width + ctx.measureText(etats).width * .62;
  }
  /** Équation en deux côtés (eqn, eqf) : taille réduite si, avec les états, elle sortirait du cadre. */
  function ajuste(c, x, g, d, o = {}, fl = 56) {
    const k = c.cadre; if (!k || typeof g !== 'string' || typeof d !== 'string' || !/\((?:aq|l|s|g)\)/.test(g + d)) return o;
    const t = o.taille ?? 17, w = largeur(c.ctx, g, t) + largeur(c.ctx, d, t) + fl;
    const x0 = o.align === 'center' ? x - w / 2 : o.align === 'right' ? x - w : x, x1 = x0 + w;
    const place = o.align === 'center' ? 2 * Math.min(x - 4, k.w - 4 - x) : o.align === 'right' ? x - 4 : k.w - 4 - x;
    return x1 > k.w - 4 || x0 < 4 ? { ...o, taille: Math.max(12, t * Math.min(1, (place - fl) / (w - fl))) } : o;
  }
  window.Etats = { annote, cotes, morceaux, piece, liste, ajoute, ajuste, marque };

  /* Indice « _{…} » derrière n'importe quel caractère (« H₃O⁺_{(aq)} ») : le kit ne le découpe que derrière une lettre. */
  const segKit = C.segments;
  C.segments = function (s) {
    const out = [], re = /(^|[^A-Za-zτθΔλωφ])_\{([^}]+)\}/g; let i = 0, m;
    while ((m = re.exec(s))) { if (m.index + m[1].length > i) out.push(...segKit(s.slice(i, m.index + m[1].length))); out.push({ t: m[2], sub: true }); i = re.lastIndex; }
    if (i < s.length) out.push(...segKit(s.slice(i)));
    return out;
  };
  const texteKit = P.texte;
  P.texte = function (s, x, y, o = {}) {
    s = String(s);
    if (!/(^|[^A-Za-zτθΔλωφ])_\{/.test(s) || /\^|[⁻⁰¹²³⁴⁵⁶⁷⁸⁹]/.test(s)) return texteKit.call(this, s, x, y, o);
    let taille = o.taille ?? 18;
    this.ctx.font = `${o.gras ? '700 ' : ''}${taille}px ${T.POLICE}`;
    this._verifierCadre(s.replace(/[_{}]/g, ''), x, y, taille, o.align);
    if (this.echelle && this.tailleMin) taille = Math.max(taille, this.tailleMin / this.echelle);
    return this._texteIndices(s, x, y, o, taille);
  };
  /* Une fois la page chargée (ses propres écritures chimiques installées), la couche la plus haute ajoute les états. */
  function installer() {
    pret = true;
    const avant = P.texte;
    P.texte = function (s, x, y, o = {}) {
      s = String(s);
      if (/^_\{\((?:aq|l|s|g)\)\}$/.test(s)) return avant.call(this, s, x, y, { ...o, duree: .001 });   // un état seul (pages à termes)
      const a = annote(s);
      if (a === s && !/\((?:aq|l|s|g)\)/.test(a)) return avant.call(this, s, x, y, o);
      const o2 = { ...o, duree: o.duree ?? Math.max(.1, plain(ORIG.get(s) ?? s) / 16) };
      const k = this.cadre;
      if (k && a !== s) {   // un texte qui s'allonge avec ses états ne sort pas du cadre
        const t = o.taille ?? 18, w = largeur(this.ctx, a, t), x0 = o.align === 'center' ? x - w / 2 : o.align === 'right' ? x - w : x;
        if (x0 + w > k.w - 4 || x0 < 4) o2.max = Math.min(o.max ?? Infinity, o.align === 'center' ? 2 * Math.min(x - 4, k.w - 4 - x) : o.align === 'right' ? x - 4 : k.w - 4 - x);
      }
      return avant.call(this, marque(a), x, y, o2);
    };
    if (typeof window.chim === 'function') { const chim = window.chim; window.chim = s => chim(marque(annote(s))); }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', installer); else installer();
})();

(function () {
  "use strict";

  const cfg = window.CHEM_LAB_CONFIG;
  if (!cfg) throw new Error("CHEM_LAB_CONFIG manquant");
  const T = window.Tableau;
  if (!T) throw new Error("Tableau manquant : charger /media/simulations/shared/tableau/tableau.js avant chem-lab.js");

  const $ = (s, root = document) => root.querySelector(s);
  const clamp = (v, lo, hi) => Math.min(hi, Math.max(lo, v));
  const log10 = (v) => Math.log(v) / Math.LN10;
  const fmt = (v, digits = 3) => {
    if (typeof v !== "number" || !Number.isFinite(v)) return String(v ?? "—");
    const a = Math.abs(v);
    if ((a > 0 && a < 0.001) || a >= 10000) return v.toExponential(2).replace("e+", "e");
    return Number(v.toFixed(digits)).toLocaleString("fr-FR");
  };
  const graine = T.graine;
  const isotopeData = {
    c14: { name: "Carbone 14", halfLife: 5730, unit: "ans" },
    i131: { name: "Iode 131", halfLife: 8.02, unit: "jours" },
    ir192: { name: "Iridium 192", halfLife: 73.83, unit: "jours" }
  };
  const nucleiData = {
    he4: { name: "Hélium 4", A: 4, z: 2, perNucleon: 7.07 },
    fe56: { name: "Fer 56", A: 56, z: 26, perNucleon: 8.79 },
    u235: { name: "Uranium 235", A: 235, z: 92, perNucleon: 7.59 }
  };

  const requestedMission = new URLSearchParams(window.location.search).get("mission") || new URLSearchParams(window.location.search).get("variant");
  const requestedMissionIndex = cfg.missions.findIndex((item) => item.id === requestedMission);
  const state = {
    missionIndex: requestedMissionIndex >= 0 ? requestedMissionIndex : 0,
    variables: {},
    measurements: [],
    student_prediction: null,
    trial_history: [],
    scientific_observation: "Choisis une prédiction, règle les paramètres puis lance l’essai.",
    status: "ready",
    animation: 1,
    runCount: 0,
    model_limits: cfg.modelLimits || "Modèle scolaire idéal : solutions diluées, température uniforme et pertes négligées."
  };


  const ACCENT = cfg.accent || "#38bdf8";
  document.documentElement.style.setProperty("--accent", ACCENT);
  document.title = cfg.title;
  document.body.innerHTML = `
    <div class="tableau">
      <header class="titre">
        <div><small>Chimie · 2 BAC · ${cfg.chapters.join(" · ")}</small><h1 id="labTitle"></h1><p class="objectif" id="missionGoal"></p></div>
        <nav class="onglets" id="missionTabs" aria-label="Missions"></nav>
      </header>
      <section class="scene chimie">
        <aside class="reglages" data-target="controls" data-professor-control="set_parameters" data-professor-point="reglages" data-professor-label="réglages de l’essai">
          <h3 id="missionTitle"></h3>
          <p class="legende">Je prédis avant de mesurer :</p>
          <div class="choix" id="predictions" data-professor-point="prediction" data-professor-label="ta prédiction"></div>
          <div class="controls" id="controls"></div>
          <p class="legende" id="verdict" data-professor-point="verdict" data-professor-label="verdict de ta prédiction">Le résultat de ta prédiction s’écrira ici.</p>
        </aside>
        <div class="dessin" data-target="scene">
          <canvas id="sceneCanvas" role="img" aria-label="Montage expérimental et courbe de mesures dessinés à la craie" data-target="graph"></canvas>
        </div>
      </section>
      <footer class="barre">
        <button class="craie-btn principal" id="runButton" data-professor-control="start run_trial run">Lancer l’essai</button>
        <button class="craie-btn secondaire" id="resetButton" data-professor-control="reset">Recommencer</button>
        <p class="bulle" id="statusText" role="status" aria-live="polite"></p>
        <span class="lecture" id="progress"></span>
      </footer>
    </div>`;

  function mission() { return cfg.missions[state.missionIndex]; }

  // ── Scène : horloge d'écriture en direct ──────────────────────────────────
  const scene = { ouvert: performance.now(), marque: null, dirty: true, now: 0 };
  const redraw = () => { scene.dirty = true; };
  const rouvrir = () => { scene.ouvert = performance.now(); scene.marque = null; redraw(); };
  const depuisOuverture = () => (performance.now() - scene.ouvert) / 1000;

  function initializeVariables() {
    state.variables = {};
    mission().parameters.forEach((p) => { state.variables[p.key] = p.value; });
    state.measurements = [];
    state.student_prediction = null;
    state.scientific_observation = "Choisis une prédiction, règle les paramètres puis lance l’essai.";
    state.status = "ready";
  }

  function buildMissionTabs() {
    T.onglets($("#missionTabs"), cfg.missions.map((m) => ({ id: m.id, label: `${m.icon} ${m.shortTitle || m.title}` })), mission().id, selectVariant,
      new Set(state.trial_history.map((t) => t.mission_id)));
  }

  function buildMission() {
    const m = mission();
    T.ecrire($("#labTitle"), cfg.title);
    T.ecrire($("#missionTitle"), `${String(state.missionIndex + 1).padStart(2, "0")} · ${m.title}`);
    T.ecrire($("#missionGoal"), m.goal, { vitesse: 60 });
    $("#predictions").innerHTML = m.predictions.map((p, i) => `<label><input type="radio" name="prediction" value="${i}" data-professor-control="set_prediction"> ${p}</label>`).join("");
    $("#predictions").querySelectorAll("input").forEach((b) => b.addEventListener("change", () => setPrediction(Number(b.value))));
    const box = $("#controls"); box.replaceChildren();
    m.parameters.forEach((p) => box.append(controlElement(p)));
    updateControlOutputs();
    updateDisplay();
  }

  function controlElement(p) {
    if (p.type === "select") {
      const el = document.createElement("label"); el.className = "craie-champ";
      el.innerHTML = `<span>${p.label}</span><select class="craie-select" data-key="${p.key}" aria-label="${p.label}">${p.options.map(o => `<option value="${o.value}" ${String(o.value) === String(p.value) ? "selected" : ""}>${o.label}</option>`).join("")}</select>`;
      el.querySelector("select").addEventListener("input", onParameterInput);
      return el;
    }
    const el = T.curseur({ id: `ctl-${p.key}`, label: p.label, min: p.min, max: p.max, step: p.step, valeur: state.variables[p.key], unite: "", decimales: p.digits ?? 2 });
    el.input.dataset.key = p.key;
    el.input.addEventListener("input", onParameterInput);
    el.maj = (v) => { if (v !== undefined) el.input.value = String(v); el.querySelector("b").textContent = displayParam(p, el.input.value); };
    el.maj();
    return el;
  }

  function displayParam(p, value) {
    if (p.type === "select") return p.options.find(o => String(o.value) === String(value))?.label || value;
    if (p.transform === "power10") return `10^${value} ${p.unit || ""}`;
    return `${fmt(Number(value), p.digits ?? 2)} ${p.unit || ""}`.trim();
  }

  function updateControlOutputs() {
    mission().parameters.forEach((p) => {
      const el = $(`[data-key="${p.key}"]`);
      if (el && el.type === "range") el.closest(".curseur").maj();
    });
  }

  function onParameterInput(event) {
    const p = mission().parameters.find(x => x.key === event.target.dataset.key);
    state.variables[p.key] = p.type === "select" ? event.target.value : Number(event.target.value);
    updateControlOutputs();
    state.status = "adjusting";
    T.bulle($("#statusText"), "Paramètre modifié : observe le montage, puis relance pour mesurer son effet.");
    redraw();
    syncState();
  }

  function setPrediction(index) {
    state.student_prediction = index;
    $("#predictions").querySelectorAll("input").forEach((b, i) => { b.checked = i === index; });
    T.ecrire($("#verdict"), "Prédiction notée. Lance maintenant l’essai.");
    syncState();
  }

  function solveEquilibrium(a0, b0, c0, K) {
    let lo = -c0 + 1e-9;
    let hi = Math.min(a0, b0) - 1e-9;
    const f = (x) => (c0 + x) / Math.max(1e-12, (a0 - x) * (b0 - x)) - K;
    for (let i = 0; i < 90; i++) {
      const mid = (lo + hi) / 2;
      if (f(mid) > 0) hi = mid; else lo = mid;
    }
    return (lo + hi) / 2;
  }

  function solveEsterEquilibrium(acid, alcohol, ester, water, K) {
    let lo = -Math.min(ester, water) + 1e-9;
    let hi = Math.min(acid, alcohol) - 1e-9;
    const f = (x) => ((ester + x) * (water + x)) / Math.max(1e-12, (acid - x) * (alcohol - x)) - K;
    for (let i = 0; i < 90; i++) {
      const mid = (lo + hi) / 2;
      if (f(mid) > 0) hi = mid; else lo = mid;
    }
    return (lo + hi) / 2;
  }

  function simulate(model, p) {
    let measurements = [], series = [], observation = "", verdictIndex = null, primary = {}, visual = {};
    if (model === "kinetic_factors") {
      const factor = p.catalyst === "none" ? 1 : p.catalyst === "fe" ? 2.2 : 4;
      const k = .004 * (p.c0 / .1) * Math.exp(.065 * (p.temp - 25)) * factor;
      const half = Math.log(2) / k;
      const a0 = .85 * p.c0 / .1;
      for (let i = 0; i <= 40; i++) { const t = i * half * 4 / 40; series.push({ x: t, y: a0 * Math.exp(-k * t) }); }
      measurements = [{ label: "Constante k", value: fmt(k, 4), unit: "s⁻¹" }, { label: "Temps de demi-réaction", value: fmt(half, 1), unit: "s" }, { label: "Vitesse initiale", value: fmt(k * p.c0, 5), unit: "mol·L⁻¹·s⁻¹" }];
      observation = `À ${fmt(p.temp, 0)} °C, ${p.catalyst === "none" ? "sans catalyseur" : "avec catalyseur"}, t½ vaut ${fmt(half, 1)} s. Une hausse de température ou un catalyseur augmente k sans changer l’état final.`;
      verdictIndex = (p.temp > 25 || factor > 1 || p.c0 > .1) ? 0 : 1;
      primary = { label: "t½ mesuré", value: fmt(half, 1), unit: "secondes" };
      visual = { rate: clamp(k * 30, .2, 4), fraction: .5, kind: "kinetics" };
    } else if (model === "kinetic_monitor") {
      const progress = 1 - Math.exp(-p.k * p.time);
      const absorbance = p.a0 * (1 - progress);
      const half = Math.log(2) / p.k;
      for (let i = 0; i <= 50; i++) { const t = i * p.duration / 50; series.push({ x: t, y: p.a0 * Math.exp(-p.k * t) }); }
      measurements = [{ label: "Absorbance A(t)", value: fmt(absorbance, 3), unit: "" }, { label: "Avancement relatif", value: fmt(progress * 100, 1), unit: "%" }, { label: "t½ graphique", value: fmt(half, 1), unit: "s" }];
      observation = `À t = ${fmt(p.time, 0)} s, l’absorbance a diminué à ${fmt(absorbance, 3)}. Le point A = A₀/2 repère t½ = ${fmt(half, 1)} s.`;
      verdictIndex = p.time >= half ? 0 : 2;
      primary = { label: "Absorbance", value: fmt(absorbance, 3), unit: `à ${fmt(p.time, 0)} s` };
      visual = { rate: clamp(p.k * 50, .2, 3), fraction: progress, kind: "kinetics" };
    } else if (model === "decay_random") {
      const iso = isotopeData[p.isotope], fraction = Math.pow(2, -p.elapsed), remaining = Math.round(p.n0 * fraction);
      for (let i = 0; i <= 50; i++) series.push({ x: i / 10, y: 100 * Math.pow(2, -i / 10) });
      measurements = [{ label: "Noyaux non désintégrés", value: remaining, unit: `/ ${p.n0}` }, { label: "Fraction restante", value: fmt(fraction * 100, 1), unit: "%" }, { label: "Temps écoulé", value: fmt(p.elapsed * iso.halfLife, 1), unit: iso.unit }];
      observation = `Après ${fmt(p.elapsed, 1)} demi-vie(s), le modèle prévoit ${fmt(fraction * 100, 1)} % de ${iso.name} restant. Chaque noyau se désintègre au hasard, mais la population suit une loi exponentielle.`;
      verdictIndex = Math.abs(p.elapsed - 1) < 1e-9 ? 1 : p.elapsed < 1 ? 0 : 2;
      primary = { label: "Noyaux détectés", value: remaining, unit: `${iso.name} restants` };
      visual = { kind: "nuclear", alive: fraction, count: p.n0 };
    } else if (model === "radio_dating") {
      const iso = isotopeData[p.isotope], age = -iso.halfLife * Math.log(p.ratio) / Math.log(2);
      for (let i = 0; i <= 50; i++) series.push({ x: i / 10 * iso.halfLife, y: 100 * Math.pow(2, -i / 10) });
      measurements = [{ label: "Rapport N/N₀", value: fmt(p.ratio, 3), unit: "" }, { label: "Âge calculé", value: fmt(age, 0), unit: iso.unit }, { label: "Demi-vies écoulées", value: fmt(age / iso.halfLife, 2), unit: "" }];
      observation = `Le rapport ${fmt(p.ratio * 100, 1)} % correspond à ${fmt(age / iso.halfLife, 2)} demi-vies, soit un âge de ${fmt(age, 0)} ${iso.unit}.`;
      verdictIndex = Math.abs(p.ratio - .5) < .005 ? 1 : p.ratio < .5 ? 2 : 0;
      primary = { label: "Âge radiométrique", value: fmt(age, 0), unit: iso.unit };
      visual = { kind: "nuclear", alive: p.ratio, count: 180 };
    } else if (model === "binding_energy") {
      const n = nucleiData[p.nucleus], energy = n.A * n.perNucleon, defect = energy / 931.5;
      series = [{x:1,y:0},{x:4,y:7.07},{x:12,y:7.68},{x:56,y:8.79},{x:100,y:8.5},{x:160,y:8.0},{x:235,y:7.59}];
      measurements = [{ label: "Énergie totale", value: fmt(energy, 1), unit: "MeV" }, { label: "Défaut de masse", value: fmt(defect, 4), unit: "u" }, { label: "Énergie / nucléon", value: fmt(n.perNucleon, 2), unit: "MeV" }];
      observation = `${n.name} possède ${fmt(n.perNucleon, 2)} MeV par nucléon. Les transformations qui rapprochent les noyaux du maximum autour du fer libèrent de l’énergie.`;
      verdictIndex = n.A < 56 ? 0 : n.A > 56 ? 2 : 1;
      primary = { label: "Énergie de liaison", value: fmt(energy, 1), unit: "MeV" };
      visual = { kind: "nuclear", alive: .82, count: Math.min(235, n.A * 2) };
    } else if (model === "reversible_equilibrium") {
      const q0 = p.c0 / Math.max(1e-9, p.a0 * p.b0), x = solveEquilibrium(p.a0, p.b0, p.c0, p.K);
      const ae = p.a0 - x, be = p.b0 - x, ce = p.c0 + x;
      series = [{x:0,y:q0},{x:.25,y:q0+(p.K-q0)*.58},{x:.5,y:q0+(p.K-q0)*.83},{x:.75,y:q0+(p.K-q0)*.95},{x:1,y:p.K}];
      measurements = [{ label: "Quotient initial Qᵣ", value: fmt(q0, 3), unit: "" }, { label: "Avancement ξ", value: fmt(x, 4), unit: "mol·L⁻¹" }, { label: "[Produit] équilibre", value: fmt(ce, 3), unit: "mol·L⁻¹" }];
      observation = `Qᵣ,i = ${fmt(q0, 3)} et K = ${fmt(p.K, 2)} : le système évolue ${q0 < p.K ? "dans le sens direct" : q0 > p.K ? "dans le sens inverse" : "sans évolution macroscopique"} jusqu’à Qᵣ = K. Les deux réactions continuent alors à vitesses égales.`;
      verdictIndex = q0 < p.K ? 0 : q0 > p.K ? 2 : 1;
      primary = { label: "Sens d’évolution", value: q0 < p.K ? "→ direct" : q0 > p.K ? "← inverse" : "équilibre", unit: `Qᵣ → ${fmt(p.K, 2)}` };
      visual = { kind: "equilibrium", ratio: clamp(ce / (ae + be + ce), 0, 1), direction: Math.sign(p.K - q0) };
    } else if (model === "weak_acid") {
      const Ka = Number(p.acid), h = (-Ka + Math.sqrt(Ka * Ka + 4 * Ka * p.concentration)) / 2;
      const ph = -log10(h), alpha = h / p.concentration;
      for (let x = 0; x <= 14; x += .25) series.push({x, y: 100 / (1 + Math.pow(10, (-log10(Ka)) - x))});
      measurements = [{ label: "pH", value: fmt(ph, 2), unit: "" }, { label: "Taux final τ", value: fmt(alpha * 100, 2), unit: "%" }, { label: "pKₐ", value: fmt(-log10(Ka), 2), unit: "" }];
      observation = `La solution atteint pH = ${fmt(ph, 2)}. Seuls ${fmt(alpha * 100, 2)} % des molécules d’acide sont dissociées : la transformation avec l’eau est limitée.`;
      verdictIndex = alpha < .1 ? 1 : 0;
      primary = { label: "pH-mètre", value: fmt(ph, 2), unit: `${fmt(alpha * 100, 1)} % ionisé` };
      visual = { kind: "equilibrium", ratio: alpha, direction: 0 };
    } else if (model === "titration") {
      const va = 20, ca = .1, cb = Number(p.cb), veq = ca * va / cb, vb = p.vb;
      const phAt = (vol) => { const acid = ca * va / 1000, base = cb * vol / 1000, total = (va + vol) / 1000; if (Math.abs(acid-base) < 1e-8) return 7; return acid > base ? -log10((acid-base)/total) : 14 + log10((base-acid)/total); };
      const ph = phAt(vb);
      for (let v = 0; v <= Math.max(40, veq * 2); v += .5) series.push({ x: v, y: phAt(v) });
      measurements = [{ label: "pH mesuré", value: fmt(ph, 2), unit: "" }, { label: "Volume équivalent", value: fmt(veq, 1), unit: "mL" }, { label: "Écart à l’équivalence", value: fmt(vb - veq, 1), unit: "mL" }];
      observation = `L’équivalence est à Vᵦ,E = ${fmt(veq, 1)} mL. À ${fmt(vb, 1)} mL, le mélange est ${vb < veq ? "acide" : vb > veq ? "basique" : "à l’équivalence"} et le pH vaut ${fmt(ph, 2)}.`;
      verdictIndex = vb < veq ? 0 : vb > veq ? 2 : 1;
      primary = { label: "Sonde pH", value: fmt(ph, 2), unit: `Vᵦ = ${fmt(vb, 1)} mL` };
      visual = { kind: "titration", ratio: vb / veq, drops: clamp(Math.abs(vb-veq), 1, 20) };
    } else if (model === "precipitation") {
      const cM = Math.pow(10, p.logM), cX = Math.pow(10, p.logX), salt = p.salt;
      const isCaF2 = salt === "caf2", Ksp = isCaF2 ? 3.9e-11 : 1.8e-10;
      const Q = isCaF2 ? cM * cX * cX : cM * cX;
      const ratio = Q / Ksp;
      series = [{x:0,y:Ksp/100},{x:1,y:Ksp/10},{x:2,y:Ksp},{x:3,y:Ksp*10},{x:4,y:Ksp*100}];
      measurements = [{ label: "Produit ionique Q", value: fmt(Q, 3), unit: "" }, { label: "Kₛ", value: fmt(Ksp, 3), unit: "" }, { label: "Sursaturation Q/Kₛ", value: fmt(ratio, 2), unit: "" }];
      observation = `Q = ${fmt(Q, 2)} ${ratio > 1 ? ">" : ratio < 1 ? "<" : "="} Kₛ. ${ratio > 1 ? "Un précipité apparaît jusqu’au retour à la saturation." : "La solution reste non saturée : aucun précipité durable."}`;
      verdictIndex = ratio > 1 ? 0 : 2;
      primary = { label: "Détection", value: ratio > 1 ? "PRÉCIPITÉ" : "LIMPIDE", unit: `Q/Kₛ = ${fmt(ratio, 2)}` };
      visual = { kind: "titration", ratio: clamp(ratio / 4, 0, 2), drops: ratio > 1 ? 22 : 0 };
    } else if (model === "redox_direction") {
      const q = Math.pow(10, p.logZn - p.logCu), E = 1.10 - .0592 / 2 * log10(q);
      measurements = [{ label: "Quotient Qᵣ", value: fmt(q, 3), unit: "" }, { label: "Force électromotrice", value: fmt(E, 3), unit: "V" }, { label: "Sens spontané", value: E > 0 ? "Zn → Cu²⁺" : "inverse", unit: "" }];
      series = [{x:-4,y:1.218},{x:-2,y:1.159},{x:0,y:1.10},{x:2,y:1.041},{x:4,y:.982}];
      observation = `E = ${fmt(E, 3)} V. ${E > 0 ? "Le zinc s’oxyde et Cu²⁺ se réduit : les électrons vont de Zn vers Cu." : "Les conditions imposées inversent le sens spontané."}`;
      verdictIndex = E > 0 ? 0 : 2;
      primary = { label: "Voltmètre", value: fmt(E, 3), unit: "V" };
      visual = { kind: "electrochem", voltage: E, bubbles: 0, speed: clamp(Math.abs(E), .2, 2) };
    } else if (model === "galvanic_cell") {
      const E = 1.10 - .0592 / 2 * (p.logZn - p.logCu), current = Math.max(0, E / p.resistance), charge = current * p.time, zincLoss = charge / 96485 * 65.38 / 2 * 1000;
      for (let i=0;i<=40;i++) series.push({x:i*p.time/40,y:Math.max(0,E-(i/40)*current*.08)});
      measurements = [{ label: "Tension à vide", value: fmt(E, 3), unit: "V" }, { label: "Courant", value: fmt(current * 1000, 1), unit: "mA" }, { label: "Masse Zn consommée", value: fmt(zincLoss, 3), unit: "mg" }];
      observation = `La pile fournit ${fmt(E, 3)} V. Avec R = ${fmt(p.resistance, 0)} Ω, I ≈ ${fmt(current*1000, 1)} mA et l’anode de zinc perd ${fmt(zincLoss, 3)} mg en ${fmt(p.time, 0)} s.`;
      verdictIndex = current * 1000 > 10 ? 0 : current * 1000 >= 3 ? 1 : 2;
      primary = { label: "Voltmètre", value: fmt(E, 3), unit: `${fmt(current*1000, 1)} mA` };
      visual = { kind: "electrochem", voltage: E, bubbles: 0, speed: clamp(current*100, .2, 3) };
    } else if (model === "electrolysis") {
      const F = 96485, charge = p.current * p.time * 60 * p.efficiency / 100;
      const copper = charge / (2 * F) * 63.546, h2 = charge / (2 * F) * 24;
      const product = p.product === "copper" ? { value: copper*1000, unit:"mg", name:"Cu déposé" } : { value:h2, unit:"mL", name:"H₂ produit" };
      for (let i=0;i<=40;i++) series.push({x:i*p.time/40,y:product.value*i/40});
      measurements = [{ label: "Charge utile", value: fmt(charge, 1), unit: "C" }, { label: product.name, value: fmt(product.value, 2), unit: product.unit }, { label: "Quantité d’électrons", value: fmt(charge/F, 5), unit: "mol" }];
      observation = `La charge utile Q = I·t·η vaut ${fmt(charge, 1)} C. La loi de Faraday prévoit ${fmt(product.value, 2)} ${product.unit} de ${product.name}.`;
      verdictIndex = product.value > (p.product === "copper" ? 220 : 45) ? 0 : product.value > (p.product === "copper" ? 60 : 12) ? 1 : 2;
      primary = { label: product.name, value: fmt(product.value, 2), unit: product.unit };
      visual = { kind: "electrochem", voltage: 2, bubbles: p.product === "hydrogen" ? 25 : 6, speed: clamp(p.current, .3, 3) };
    } else if (model === "ester_equilibrium") {
      const x = solveEsterEquilibrium(p.acid, p.alcohol, p.ester, p.water, p.K), yieldPct = x / Math.min(p.acid, p.alcohol) * 100;
      const ae=p.acid-x, al=p.alcohol-x, es=p.ester+x, wa=p.water+x;
      series = [{x:0,y:0},{x:.2,y:yieldPct*.48},{x:.4,y:yieldPct*.73},{x:.6,y:yieldPct*.88},{x:.8,y:yieldPct*.96},{x:1,y:yieldPct}];
      measurements = [{ label: "Avancement final", value: fmt(x, 3), unit: "mol" }, { label: "Rendement", value: fmt(yieldPct, 1), unit: "%" }, { label: "Qᵣ final", value: fmt(es*wa/Math.max(1e-9,ae*al), 2), unit: "" }];
      observation = `L’estérification s’arrête à ${fmt(yieldPct, 1)} % lorsque Qᵣ atteint K = ${fmt(p.K, 1)}. Elle est limitée et réversible.`;
      verdictIndex = yieldPct < 90 ? 1 : 0;
      primary = { label: "Rendement final", value: fmt(yieldPct, 1), unit: "%" };
      visual = { kind: "organic", yield: yieldPct/100, speed: .7 };
    } else if (model === "ester_kinetics") {
      const factor = p.catalyst === "acid" ? 3.2 : 1, k=.018*Math.exp(.045*(p.temp-60))*factor, max=.67, progress=max*(1-Math.exp(-k*p.time));
      for(let i=0;i<=45;i++){const t=i*p.duration/45;series.push({x:t,y:100*max*(1-Math.exp(-k*t))});}
      measurements = [{ label: "Avancement relatif", value: fmt(progress*100,1), unit:"%" }, { label: "Constante apparente", value: fmt(k,4), unit:"min⁻¹" }, { label: "Plateau d’équilibre", value: fmt(max*100,0), unit:"%" }];
      observation = `À ${fmt(p.temp,0)} °C ${p.catalyst === "acid" ? "avec catalyse acide" : "sans catalyseur"}, le mélange atteint ${fmt(progress*100,1)} % à ${fmt(p.time,0)} min. Chauffer et catalyser raccourcit le délai, mais ne déplace pas le plateau.`;
      verdictIndex = (p.temp>60 || factor>1) ? 0 : 2;
      primary = { label:"Conversion", value:fmt(progress*100,1), unit:"%" };
      visual = {kind:"organic",yield:progress,speed:clamp(k*150,.3,3)};
    } else if (model === "synthesis_control") {
      let yieldPct;
      if (p.pathway === "saponification") yieldPct = 96 + 2*p.waterRemoval;
      else { const effectiveAlcohol=p.alcoholRatio, effectiveWater=.05*(1-p.waterRemoval); const x=solveEsterEquilibrium(1,effectiveAlcohol,0,effectiveWater,4); yieldPct=100*x; }
      yieldPct=clamp(yieldPct,0,99.5);
      series=[{x:0,y:0},{x:1,y:yieldPct*.5},{x:2,y:yieldPct*.78},{x:3,y:yieldPct*.92},{x:4,y:yieldPct}];
      measurements=[{label:"Rendement prévu",value:fmt(yieldPct,1),unit:"%"},{label:"Excès d’alcool",value:fmt(p.alcoholRatio,1),unit:"équiv."},{label:"Eau retirée",value:fmt(p.waterRemoval*100,0),unit:"%"}];
      observation=`${p.pathway === "saponification" ? "La saponification consomme l’ester pratiquement totalement." : "L’excès d’alcool et le retrait d’eau déplacent l’équilibre vers l’ester."} Rendement modélisé : ${fmt(yieldPct,1)} %.`;
      verdictIndex=yieldPct>85?0:yieldPct>65?1:2;
      primary={label:"Rendement optimisé",value:fmt(yieldPct,1),unit:"%"};
      visual={kind:"organic",yield:yieldPct/100,speed:1.4};
    } else {
      throw new Error(`Modèle inconnu: ${model}`);
    }
    return { measurements, series, observation, verdictIndex, primary, visual, axis: mission().axis || {} };
  }

  function runTrial(overrides) {
    if (overrides && typeof overrides === "object") setParameters(overrides, false);
    state.status = "running";
    state.animation = 0;
    state.runCount += 1;
    $("#runButton").disabled = true;
    $("#runButton").textContent = "Mesure en cours…";
    const result = simulate(mission().model, state.variables);
    state.measurements = result.measurements;
    state.scientific_observation = result.observation;
    state.last_result = result;
    scene.marque = depuisOuverture() + 1.2;   // les mesures s'écrivent une fois la courbe tracée
    const started = performance.now();
    const animate = (now) => {
      state.animation = clamp((now - started) / 1100, 0, 1);
      redraw();
      if (state.animation < 1) requestAnimationFrame(animate);
      else finishTrial(result);
    };
    requestAnimationFrame(animate);
    return publicState();
  }

  function finishTrial(result) {
    state.status = "completed";
    state.trial_history.push({
      trial: state.runCount,
      mission_id: mission().id,
      variables: { ...state.variables },
      measurements: result.measurements.map(x => ({...x})),
      observation: result.observation,
      timestamp: new Date().toISOString()
    });
    if (state.trial_history.length > 12) state.trial_history.shift();
    $("#runButton").disabled = false;
    $("#runButton").textContent = "Refaire une mesure";
    buildMissionTabs();
    updateDisplay();
    const selected = state.student_prediction;
    const correct = selected !== null && selected === result.verdictIndex;
    const verdict = $("#verdict");
    verdict.dataset.kind = selected === null ? "" : correct ? "good" : "bad";
    T.ecrire(verdict, selected === null ? "Conseil : formule une prédiction avant le prochain essai." : correct ? "✓ Prédiction confirmée par les mesures." : "↻ Les mesures réfutent la prédiction : compare les valeurs et réessaie.");
    syncState();
  }

  function updateDisplay() {
    const result = state.last_result;
    $("#progress").textContent = state.runCount ? `${state.runCount} essai${state.runCount === 1 ? "" : "s"}` : "";
    const status = $("#statusText");
    if (result) { status.dataset.kind = "good"; T.bulle(status, result.observation, "good"); }
    else { delete status.dataset.kind; T.bulle(status, cfg.intro); }
    redraw();
  }

  function resetSimulation() {
    initializeVariables();
    state.last_result = null;
    $("#runButton").disabled = false;
    $("#runButton").textContent = "Lancer l’essai";
    buildMission();
    $("#verdict").dataset.kind = "";
    T.ecrire($("#verdict"), "Le résultat de ta prédiction s’écrira ici.");
    rouvrir();
    syncState();
    return publicState();
  }

  function selectVariant(id) {
    const i = cfg.missions.findIndex(m => m.id === id || m.model === id);
    if (i < 0) return { ok:false, error:`Mission inconnue: ${id}` };
    state.missionIndex = i;
    initializeVariables();
    state.last_result = null;
    $("#runButton").disabled = false;
    $("#runButton").textContent = "Lancer l’essai";
    buildMissionTabs();
    buildMission();
    $("#verdict").dataset.kind = "";
    T.ecrire($("#verdict"), "Nouvelle mission : commence par une prédiction.");
    rouvrir();
    syncState();
    return publicState();
  }

  function setParameters(values, refresh = true) {
    const allowed = new Set(mission().parameters.map(p => p.key));
    Object.entries(values || {}).forEach(([k,v]) => {
      if (!allowed.has(k)) return;
      const def = mission().parameters.find(p => p.key === k);
      state.variables[k] = def.type === "select" ? String(v) : clamp(Number(v), def.min, def.max);
      const el = $(`[data-key="${k}"]`);
      if (el) el.value = state.variables[k];
    });
    updateControlOutputs();
    redraw();
    if (refresh) syncState();
    return publicState();
  }

  function highlight(target) {
    if (T.surligner(target)) return {ok:true,target};   // repère dessiné à la craie ou panneau data-professor-point
    const el = document.querySelector(`[data-target="${target}"]`) || document.querySelector(target);
    if (!el) return {ok:false,error:`Cible inconnue: ${target}`};
    el.classList.remove("highlighted");
    void el.offsetWidth;
    el.classList.add("highlighted");
    setTimeout(() => el.classList.remove("highlighted"), 3200);
    return {ok:true,target};
  }

  function publicState() {
    return {
      simulation_id: cfg.id,
      title: cfg.title,
      status: state.status,
      active_mission: { id: mission().id, title: mission().title, chapter: mission().chapter, learning_goal: mission().goal, model: mission().model },
      current_variant: mission().id,
      variables: { ...state.variables },
      measurements: state.measurements.map(x => ({...x})),
      student_prediction: state.student_prediction === null ? null : mission().predictions[state.student_prediction],
      mission_coverage: cfg.missions.map(m => ({id:m.id, chapter:m.chapter, goal:m.goal})),
      trial_history: state.trial_history.map(x => ({...x})),
      scientific_observation: state.scientific_observation,
      model_limits: state.model_limits,
      available_commands: ["start", "reset", "set_variant", "set_parameters", "run_trial", "highlight", "get_state", "set_prediction"]
    };
  }

  function syncState() {
    window.simulation_state = publicState();
    window.simulationState = { id: cfg.id, ...window.simulation_state };
    const completedMissions = new Set(state.trial_history.map((trial) => trial.mission_id)).size;
    if (window.parent !== window) window.parent.postMessage({
      type: "simulation_state",
      simulation_id: cfg.id,
      simulationId: cfg.id,
      current_state: { ...window.simulation_state, simulation_status: state.status === "completed" ? "finished" : state.status },
      student_actions: state.trial_history.length ? [{ action: state.status === "completed" ? "finish_simulation" : "run_trial", mission_id: mission().id, trial: state.runCount }] : [],
      objective_progress: completedMissions / cfg.missions.length,
      timestamp: new Date().toISOString(),
      state: window.simulation_state
    }, "*");
  }

  function executeAICommand(input, legacyParameters) {
    const payload = typeof input === "string" ? {command:input, parameters:legacyParameters || {}, ...(legacyParameters || {})} : (input || {});
    const command = payload.command || payload.action;
    let result;
    try {
      if (["start","run_trial"].includes(command)) result = runTrial(payload.parameters || payload.params);
      else if (command === "reset") result = resetSimulation();
      else if (command === "set_variant") result = selectVariant(payload.variant || payload.variant_id || payload.mission_id || payload.id);
      else if (command === "set_parameters") result = setParameters(payload.parameters || payload.params || {});
      else if (command === "highlight") result = highlight(payload.target || "scene");
      else if (command === "get_state") result = publicState();
      else if (command === "set_prediction") { setPrediction(Number(payload.index)); result = publicState(); }
      else result = {ok:false,error:`Commande inconnue: ${command}`};
    } catch (error) { result = {ok:false,error:error.message}; }
    return result;
  }

  // ── Dessin à la craie : montage à gauche, courbe et mesures à droite (repère logique 560 × 400) ──
  const canvas = $("#sceneCanvas");
  const craie = new T.Craie(canvas, { onresize: redraw });
  const LW = 560, LH = 400;
  const M = { x: 12, y: 8, w: 290, h: 330 };          // montage
  const G = { x: 352, y: 34, w: 190, h: 130 };         // courbe
  const accent = () => ACCENT;

  /*
   * Le montage PEINT (16 novembre 2026 : « des animations plus réalistes, plus attractives, avec de belles couleurs ») :
   * verre translucide avec reflets, liquides colorés avec ménisque, appareils en boîtier, électrodes métalliques,
   * noyaux et particules en sphères ombrées. La craie garde les légendes, les flèches, les formules et les valeurs.
   * Mêmes places, mêmes tailles, mêmes repères qu'avant.
   */
  const RGB = (s) => {
    if (Array.isArray(s)) return s.slice(0, 3);
    const h = craie.couleur(s);
    if (h.startsWith("#")) { const n = parseInt(h.slice(1), 16); return [n >> 16 & 255, n >> 8 & 255, n & 255]; }
    const m = h.match(/[\d.]+/g); return m ? m.slice(0, 3).map(Number) : [200, 200, 200];
  };
  const rgba = (c, a) => `rgba(${c.map(Math.round).join(",")},${clamp(a, 0, 1).toFixed(3)})`;
  const clair = (c, k) => c.map((v) => v + (255 - v) * k), fonce = (c, k) => c.map((v) => v * k);
  const melange = (a, b, f) => a.map((v, i) => v + (b[i] - v) * clamp(f, 0, 1));
  const doux = (f) => { f = clamp(f, 0, 1); return f * f * (3 - 2 * f); };
  /** Peint sur le contexte de la craie, tout de suite (la craie continue d'écrire par-dessus). */
  function peindre(fn) { craie.direct(() => { const c = craie.ctx; c.save(); try { fn(c); } finally { c.restore(); } }); }
  function ombrePortee(c, cx, yb, rx) { c.fillStyle = "rgba(0,0,0,.3)"; c.beginPath(); c.ellipse(cx + 3, yb + 3, rx, 4, 0, 0, Math.PI * 2); c.fill(); }
  /** Liquide dans la forme (chemin fermé) : plus sombre aux bords, ménisque clair. */
  function liquide(c, forme, x0, x1, ys, yb, col, a, menisque = true) {
    c.save(); forme(); c.clip();
    const g = c.createLinearGradient(x0, 0, x1, 0);
    g.addColorStop(0, rgba(fonce(col, .6), a * 1.35)); g.addColorStop(.42, rgba(clair(col, .15), a)); g.addColorStop(1, rgba(fonce(col, .58), a * 1.35));
    c.fillStyle = g; c.fillRect(x0 - 2, ys, x1 - x0 + 4, yb - ys + 2);
    c.restore();
    if (menisque) { c.fillStyle = rgba(clair(col, .45), a + .12); c.beginPath(); c.ellipse((x0 + x1) / 2, ys, Math.max(1, (x1 - x0) / 2 - 1), 2.6, 0, 0, Math.PI * 2); c.fill(); }
  }
  /** Contour de verre, reflet vertical à gauche, filet clair à droite. */
  function verre(c, forme, x, y, h, o = {}) {
    c.strokeStyle = "rgba(225,240,252,.85)"; c.lineWidth = o.largeur ?? 1.9; c.lineJoin = "round"; c.lineCap = "round"; forme(); c.stroke();
    const g = c.createLinearGradient(x + 3, 0, x + 12, 0); g.addColorStop(0, "rgba(255,255,255,.4)"); g.addColorStop(1, "rgba(255,255,255,0)");
    c.fillStyle = g; c.fillRect(x + 3, y + 8, 9, Math.max(0, h - 20));
  }
  function sphere(c, x, y, r, col, a = 1) {
    col = RGB(col); c.save(); c.globalAlpha *= a;
    c.fillStyle = "rgba(0,0,0,.22)"; c.beginPath(); c.arc(x + r * .2, y + r * .3, r, 0, Math.PI * 2); c.fill();
    const g = c.createRadialGradient(x - r * .38, y - r * .42, r * .08, x, y, r);
    g.addColorStop(0, rgba(clair(col, .8), 1)); g.addColorStop(.3, rgba(clair(col, .22), 1)); g.addColorStop(.72, rgba(col, 1)); g.addColorStop(1, rgba(fonce(col, .42), 1));
    c.fillStyle = g; c.beginPath(); c.arc(x, y, r, 0, Math.PI * 2); c.fill(); c.restore();
  }
  /** Boîtier d'appareil (anthracite, coins arrondis, ombre) ; ecran : { x, y, w, h } en option (écran sombre, la craie y écrit). */
  function boitier(c, x, y, w, h, ecran) {
    c.save(); c.shadowColor = "rgba(0,0,0,.45)"; c.shadowBlur = 8; c.shadowOffsetY = 3;
    const g = c.createLinearGradient(0, y, 0, y + h); g.addColorStop(0, "#5b6673"); g.addColorStop(.5, "#3a434d"); g.addColorStop(1, "#252c33");
    c.fillStyle = g; c.beginPath(); c.roundRect(x, y, w, h, 7); c.fill(); c.restore();
    c.strokeStyle = "rgba(255,255,255,.18)"; c.lineWidth = 1; c.beginPath(); c.roundRect(x + .5, y + .5, w - 1, h - 1, 7); c.stroke();
    if (ecran) {
      const e = ecran, ge = c.createLinearGradient(0, e.y, 0, e.y + e.h); ge.addColorStop(0, "#16301f"); ge.addColorStop(1, "#0b1a12");
      c.fillStyle = ge; c.beginPath(); c.roundRect(e.x, e.y, e.w, e.h, 4); c.fill();
      c.strokeStyle = "rgba(0,0,0,.6)"; c.stroke(); c.fillStyle = "rgba(255,255,255,.06)"; c.fillRect(e.x + 2, e.y + 2, e.w - 4, e.h * .35);
    }
  }
  /** Câble noir souple de (x1, y1) à (x2, y2). */
  function cable(c, x1, y1, x2, y2, creux = 30) {
    c.strokeStyle = "#64748b"; c.lineWidth = 3; c.lineCap = "round"; c.beginPath(); c.moveTo(x1, y1);
    c.bezierCurveTo(x1 + (x2 - x1) * .3, y1 + creux, x2 - (x2 - x1) * .3, y2 - creux * .3, x2, y2); c.stroke();
    c.strokeStyle = "rgba(255,255,255,.25)"; c.lineWidth = 1; c.stroke();
  }
  /** Électrode de pH : corps noir, tige de verre, boule sensible. */
  function sondePH(c, x, yH, yB) {
    const yc = yH + (yB - yH) * .4, g = c.createLinearGradient(x - 5, 0, x + 5, 0); g.addColorStop(0, "#111"); g.addColorStop(.45, "#4a4f55"); g.addColorStop(1, "#111");
    c.fillStyle = g; c.beginPath(); c.roundRect(x - 5, yH, 10, yc - yH, 3); c.fill();
    c.fillStyle = "rgba(200,228,245,.3)"; c.fillRect(x - 3.5, yc, 7, yB - yc - 4); c.strokeStyle = "rgba(230,245,255,.75)"; c.lineWidth = 1; c.strokeRect(x - 3.5, yc, 7, yB - yc - 4);
    const gb = c.createRadialGradient(x - 2, yB - 2, 1, x, yB, 6); gb.addColorStop(0, "rgba(255,255,255,.8)"); gb.addColorStop(1, "rgba(170,210,240,.35)");
    c.fillStyle = gb; c.beginPath(); c.arc(x, yB, 5.5, 0, Math.PI * 2); c.fill(); c.strokeStyle = "rgba(230,245,255,.8)"; c.stroke();
  }
  /** Plaque de métal (électrode) verticale : col = couleur du métal. */
  function plaque(c, x, y0, y1, w, col) {
    col = RGB(col); const g = c.createLinearGradient(x - w / 2, 0, x + w / 2, 0);
    g.addColorStop(0, rgba(fonce(col, .55), 1)); g.addColorStop(.35, rgba(clair(col, .45), 1)); g.addColorStop(.6, rgba(col, 1)); g.addColorStop(1, rgba(fonce(col, .5), 1));
    c.fillStyle = g; c.beginPath(); c.roundRect(x - w / 2, y0, w, y1 - y0, 2); c.fill();
  }

  function becher(x, y, w, h, niveau, liq, o = {}) {
    const r = 7, forme = (d = 0) => { craie.ctx.beginPath(); craie.ctx.moveTo(x + d, y); craie.ctx.lineTo(x + d, y + h - r); craie.ctx.quadraticCurveTo(x + d, y + h - d, x + r, y + h - d); craie.ctx.lineTo(x + w - r, y + h - d); craie.ctx.quadraticCurveTo(x + w - d, y + h - d, x + w - d, y + h - r); craie.ctx.lineTo(x + w - d, y); };
    peindre((c) => {
      ombrePortee(c, x + w / 2, y + h, w * .55);
      forme(); c.fillStyle = "rgba(190,220,240,.08)"; c.fill();
      if (niveau > 0 && liq) {
        const ly = y + h - h * clamp(niveau, 0, 1) - 2, a = o.alpha != null ? clamp(o.alpha * 2.6, .08, .85) : .5;
        liquide(c, () => { forme(2); c.closePath(); }, x + 2, x + w - 2, ly, y + h, RGB(liq), a);
      }
      c.fillStyle = "rgba(220,238,250,.25)"; c.fillRect(x + 6, y + h - 3, w - 12, 3);
      verre(c, () => forme(), x, y, h);
      c.strokeStyle = "rgba(240,248,255,.5)"; c.lineWidth = 1;
      for (let k = 1; k <= 3; k++) { const gy = y + h - k * h / 4.2; c.beginPath(); c.moveTo(x + w - 12, gy); c.lineTo(x + w - 5, gy); c.stroke(); }
      c.strokeStyle = "rgba(240,248,255,.9)"; c.lineWidth = 2; c.beginPath(); c.moveTo(x, y); c.quadraticCurveTo(x - 5, y - 1, x - 6, y - 5); c.stroke();
    });
    if (o.label) craie.texte(o.label, x + w / 2, y + h + 20, { align: "center", taille: 15, couleur: o.labelCouleur || "faible" });
  }
  function thermometre(x, y, h, frac, label) {
    peindre((c) => {
      const yb = y + h + 7, top = y + 4 + (h - 4) * (1 - clamp(frac, 0, 1));
      c.fillStyle = "rgba(215,235,250,.2)"; c.beginPath(); c.roundRect(x - 4, y - 2, 8, h + 6, 4); c.fill();
      c.strokeStyle = "rgba(230,245,255,.8)"; c.lineWidth = 1.2; c.stroke();
      const g = c.createLinearGradient(x - 2, 0, x + 2, 0); g.addColorStop(0, "#8f1010"); g.addColorStop(.5, "#ef4444"); g.addColorStop(1, "#8f1010");
      c.fillStyle = g; c.fillRect(x - 1.6, top, 3.2, yb - top);
      sphere(c, x, yb, 7, [220, 38, 38]);
      c.strokeStyle = "rgba(240,248,255,.5)"; c.lineWidth = .8;
      for (let k = 0; k < 6; k++) { const yy = y + 6 + k * (h - 10) / 5; c.beginPath(); c.moveTo(x + 4, yy); c.lineTo(x + (k % 2 ? 7 : 9), yy); c.stroke(); }
    });
    if (label) craie.texte(label, x + 12, y + 12, { taille: 15, couleur: "rouge" });
  }
  function bulles(x, y, w, h, n, vitesse, couleur) {
    peindre((c) => {
      for (let i = 0; i < n; i++) {
        const f = ((scene.now * .00012 * vitesse) + i * .173) % 1, r = 2 + i % 3, bx = x + w * ((i * 37 % 100) / 100) + Math.sin(f * 9 + i) * 1.5, by = y + h - f * h;
        const g = c.createRadialGradient(bx - r * .35, by - r * .35, r * .1, bx, by, r);
        g.addColorStop(0, "rgba(255,255,255,.85)"); g.addColorStop(.6, "rgba(255,255,255,.12)"); g.addColorStop(1, rgba(RGB(couleur), .7));
        c.globalAlpha = Math.min(1, (1 - f) * 3); c.fillStyle = g; c.beginPath(); c.arc(bx, by, r, 0, Math.PI * 2); c.fill();
      }
    });
  }
  function fiole(x, y, w, h, niveau, liq) {
    // Erlenmeyer : col étroit, corps conique.
    const col = w * .3, xl = x + w / 2 - col / 2, xr = x + w / 2 + col / 2, ye = y + h * .3;
    const forme = () => { const c = craie.ctx; c.beginPath(); c.moveTo(xl, y); c.lineTo(xl, ye); c.lineTo(x + 3, y + h - 6); c.quadraticCurveTo(x, y + h, x + 8, y + h); c.lineTo(x + w - 8, y + h); c.quadraticCurveTo(x + w, y + h, x + w - 3, y + h - 6); c.lineTo(xr, ye); c.lineTo(xr, y); };
    peindre((c) => {
      ombrePortee(c, x + w / 2, y + h, w * .5);
      forme(); c.fillStyle = "rgba(190,220,240,.08)"; c.fill();
      if (niveau > 0) {
        const ly = y + h - h * .7 * niveau, k = (ly - ye) / (h * .7), half = w / 2 - col / 2;
        liquide(c, () => { forme(); c.closePath(); }, x, x + w, ly, y + h, RGB(liq), .5, false);
        c.fillStyle = rgba(clair(RGB(liq), .45), .62); c.beginPath(); c.ellipse(x + w / 2, ly, col / 2 + half * k - 2, 2.6, 0, 0, Math.PI * 2); c.fill();
      }
      c.strokeStyle = "rgba(225,240,252,.85)"; c.lineWidth = 1.9; c.lineJoin = "round"; forme(); c.stroke();
      c.strokeStyle = "rgba(255,255,255,.35)"; c.lineWidth = 3; c.lineCap = "round"; c.beginPath(); c.moveTo(x + w * .22, y + h * .82); c.lineTo(xl - 2, ye + 10); c.stroke();
      c.strokeStyle = "rgba(240,248,255,.9)"; c.lineWidth = 2; c.beginPath(); c.ellipse(x + w / 2, y, col / 2 + 2, 2, 0, 0, Math.PI * 2); c.stroke();
    });
  }
  function ballon(x, y, r, niveau, liq) {
    const lc = r * .32, th = Math.asin(lc / r), yN = y - r * Math.cos(th);
    const forme = () => { const c = craie.ctx; c.beginPath(); c.moveTo(x - lc, y - r * 1.7); c.lineTo(x - lc, yN); c.arc(x, y, r, -Math.PI / 2 - th, -Math.PI / 2 + th - 2 * Math.PI, true); c.lineTo(x + lc, y - r * 1.7); };
    peindre((c) => {
      forme(); c.fillStyle = "rgba(190,220,240,.08)"; c.fill();
      if (niveau > 0) {
        const ly = y + r - 2 * r * clamp(niveau, 0, 1);
        liquide(c, () => { c.beginPath(); c.arc(x, y, r - 1.5, 0, Math.PI * 2); }, x - r, x + r, ly, y + r, RGB(liq), .55, false);
        const hw = Math.sqrt(Math.max(0, r * r - (ly - y) ** 2)) - 2;
        c.fillStyle = rgba(clair(RGB(liq), .45), .65); c.beginPath(); c.ellipse(x, ly, Math.max(1, hw), 3, 0, 0, Math.PI * 2); c.fill();
      }
      c.strokeStyle = "rgba(225,240,252,.85)"; c.lineWidth = 2; forme(); c.stroke();
      c.strokeStyle = "rgba(255,255,255,.38)"; c.lineWidth = 3.5; c.lineCap = "round"; c.beginPath(); c.arc(x, y, r * .76, Math.PI * 1.08, Math.PI * 1.4); c.stroke();
      c.lineWidth = 1.4; c.beginPath(); c.moveTo(x - lc + 2.5, y - r * 1.7 + 4); c.lineTo(x - lc + 2.5, yN - 4); c.stroke();
    });
  }
  function fleches2sens(x, y, l, sens) {
    craie.fleche(x, y - 4, x + l, y - 4, { couleur: sens >= 0 ? "jaune" : "faible", largeur: sens > 0 ? 2.6 : 1.4 });
    craie.fleche(x + l, y + 6, x, y + 6, { couleur: sens <= 0 ? "jaune" : "faible", largeur: sens < 0 ? 2.6 : 1.4 });
  }

  function dessinerMontage(model, p, v, result) {
    const kind = cfg.sceneKind || v.kind, run = state.status === "running", done = !!result;
    const x = M.x, y = M.y, w = M.w, h = M.h, cx = x + w / 2;
    if (kind === "kinetics") {
      if (model === "kinetic_monitor") {
        const reste = 1 - (v.fraction ?? 0);
        // Lampe : boîtier, ampoule qui brille ; faisceau jaune avant la cuve, plus faible après (la solution absorbe).
        peindre((c) => {
          boitier(c, x + 10, y + 70, 80, 60);
          const gl = c.createRadialGradient(x + 50, y + 100, 1, x + 50, y + 100, 24); gl.addColorStop(0, "rgba(255,250,210,1)"); gl.addColorStop(.35, "rgba(250,204,21,.85)"); gl.addColorStop(1, "rgba(250,204,21,0)");
          c.fillStyle = gl; c.beginPath(); c.arc(x + 50, y + 100, 24, 0, Math.PI * 2); c.fill();
          const faisceau = (x0, x1, a) => { const g = c.createLinearGradient(0, y + 92, 0, y + 108); g.addColorStop(0, "rgba(250,204,21,0)"); g.addColorStop(.5, `rgba(253,230,138,${a})`); g.addColorStop(1, "rgba(250,204,21,0)"); c.fillStyle = g; c.fillRect(x0, y + 92, x1 - x0, 16); };
          faisceau(x + 90, x + 154, .7); faisceau(x + 186, x + 242, .7 * (1 - .75 * reste));
          boitier(c, x + 242, y + 70, 44, 60);
          const gd = c.createLinearGradient(x + 244, 0, x + 256, 0); gd.addColorStop(0, "#1e3a5f"); gd.addColorStop(1, "#0b1726"); c.fillStyle = gd; c.fillRect(x + 244, y + 90, 10, 20);
        });
        craie.texte("lampe", x + 50, y + 150, { align: "center", taille: 14, couleur: "faible" });
        craie.fleche(x + 92, y + 100, x + 150, y + 100, { couleur: "jaune", largeur: 2 });
        becher(x + 152, y + 60, 36, 80, 1, RGB(accent()), { label: "cuve", alpha: .06 + .26 * reste });   // la teinte s'efface au fil de la réaction
        craie.fleche(x + 190, y + 100, x + 240, y + 100, { couleur: "jaune", largeur: 1.6, alpha: .6 });
        craie.texte("détecteur", x + 264, y + 150, { align: "center", taille: 14, couleur: "faible" });
        craie.texte("spectrophotomètre", cx, y + 30, { align: "center", taille: 19, couleur: accent() });
        craie.repere('lampe', x + 10, y + 70, 80, 60, 'lampe').repere('cuve', x + 148, y + 56, 44, 90, 'cuve de solution').repere('detecteur', x + 242, y + 70, 44, 60, 'détecteur')
          .repere('spectrophotometre', x + 6, y + 10, w - 12, 150, 'spectrophotomètre').repere('formule', x + 14, y + 240, 240, 32, 'loi A(t)');
        craie.texte(`t = ${fmt(p.time, 0)} s`, x + 20, y + 200, { taille: 17, couleur: "jaune" });
        craie.texte(`A₀ = ${fmt(p.a0, 2)}   k = ${fmt(p.k, 3)} s⁻¹`, x + 20, y + 228, { taille: 16, couleur: "faible" });
        craie.texte("A(t) = A₀ · e^(−k t)", x + 20, y + 262, { taille: 18, couleur: "violet" });
        if (done) { craie.depuis(scene.marque); craie.texte(`A = ${result.primary.value}`, x + 180, y + 200, { taille: 22, couleur: accent() }); }
      } else {
        // Bain thermostaté : cuve de verre et eau bleutée ; le bécher y trempe ; sa teinte s'efface au fil de la réaction.
        peindre((c) => {
          ombrePortee(c, x + 140, y + 230, 110);
          const fb = () => { c.beginPath(); c.moveTo(x + 40, y + 120); c.lineTo(x + 40, y + 222); c.quadraticCurveTo(x + 40, y + 230, x + 48, y + 230); c.lineTo(x + 232, y + 230); c.quadraticCurveTo(x + 240, y + 230, x + 240, y + 222); c.lineTo(x + 240, y + 120); };
          fb(); c.fillStyle = "rgba(190,220,240,.06)"; c.fill();
          liquide(c, () => { fb(); c.closePath(); }, x + 40, x + 240, y + 150, y + 230, [96, 165, 250], .22);
        });
        becher(x + 100, y + 95, 80, 125, .7, RGB(accent()), { label: "", alpha: .06 + .2 * (1 - (v.fraction ?? 0)) });
        peindre((c) => {
          const fb = () => { c.beginPath(); c.moveTo(x + 40, y + 120); c.lineTo(x + 40, y + 222); c.quadraticCurveTo(x + 40, y + 230, x + 48, y + 230); c.lineTo(x + 232, y + 230); c.quadraticCurveTo(x + 240, y + 230, x + 240, y + 222); c.lineTo(x + 240, y + 120); };
          c.fillStyle = "rgba(96,165,250,.1)"; c.fillRect(x + 42, y + 150, 196, 78);   // l'eau du bain passe devant le bas du bécher
          c.strokeStyle = "rgba(255,255,255,.3)"; c.lineWidth = 1.2; c.beginPath(); c.moveTo(x + 42, y + 150); c.lineTo(x + 100, y + 150); c.moveTo(x + 180, y + 150); c.lineTo(x + 238, y + 150); c.stroke();
          verre(c, fb, x + 40, y + 120, 110);
          // Chronomètre : boîtier argenté, cadran blanc.
          const gc = c.createLinearGradient(x + 18, y + 38, x + 62, y + 82); gc.addColorStop(0, "#eef2f5"); gc.addColorStop(.5, "#8d979f"); gc.addColorStop(1, "#4b545c");
          c.fillStyle = gc; c.beginPath(); c.arc(x + 40, y + 60, 24, 0, Math.PI * 2); c.fill(); c.fillRect(x + 36, y + 30, 8, 8);
          c.fillStyle = "#f5f7fa"; c.beginPath(); c.arc(x + 40, y + 60, 19, 0, Math.PI * 2); c.fill();
          c.strokeStyle = "#1f2937"; c.lineWidth = 2; c.beginPath(); c.moveTo(x + 40, y + 60); const an = scene.now * .002 * (run ? 1 : 0); c.lineTo(x + 40 + 13 * Math.sin(an), y + 60 - 13 * Math.cos(an)); c.stroke();
        });
        thermometre(x + 250, y + 100, 110, (p.temp - 10) / 50, `${fmt(p.temp, 0)} °C`);
        craie.texte("bain thermostaté", x + 140, y + 250, { align: "center", taille: 15, couleur: "faible" });
        craie.texte(`c₀ = ${fmt(p.c0, 2)} mol·L⁻¹`, x + 80, y + 50, { taille: 16, couleur: "faible" });
        craie.texte(p.catalyst === "none" ? "sans catalyseur" : p.catalyst === "fe" ? "catalyseur Fe³⁺" : "catalyseur Pt", x + 80, y + 76, { taille: 16, couleur: p.catalyst === "none" ? "faible" : "jaune" });
        if (run || done) bulles(x + 104, y + 140, 72, 76, Math.round(4 + (v.rate || .5) * 4), v.rate || .5, "blanc");
        craie.texte("v = k · c   ;   t½ = ln 2 / k", x + 20, y + 300, { taille: 18, couleur: "violet" });
        craie.repere('bain', x + 40, y + 120, 200, 110, 'bain thermostaté').repere('becher', x + 98, y + 92, 84, 130, 'bécher réactionnel').repere('thermometre', x + 236, y + 96, 30, 126, 'thermomètre')
          .repere('chronometre', x + 16, y + 36, 48, 48, 'chronomètre').repere('catalyseur', x + 76, y + 60, 200, 24, 'catalyseur').repere('formule', x + 14, y + 282, 260, 28, 'vitesse et t½');
      }
    } else if (kind === "nuclear") {
      if (model === "binding_energy") {
        const n = p.nucleus === "he4" ? 4 : p.nucleus === "fe56" ? 56 : 235, z = p.nucleus === "he4" ? 2 : p.nucleus === "fe56" ? 26 : 92;
        craie.cercle(cx, y + 130, 95, { couleur: "faible", largeur: 1.4, pointille: [5, 6] });
        // Le noyau : protons (orangés) et neutrons (gris clair) en sphères ombrées, serrés, dans une lueur.
        peindre((c) => {
          const gl = c.createRadialGradient(cx, y + 130, 10, cx, y + 130, 95); gl.addColorStop(0, rgba(RGB(accent()), .16)); gl.addColorStop(1, rgba(RGB(accent()), 0));
          c.fillStyle = gl; c.beginPath(); c.arc(cx, y + 130, 95, 0, Math.PI * 2); c.fill();
          const r = graine(n), pts = [];
          for (let i = 0; i < Math.min(n, 120); i++) { const a = r() * Math.PI * 2, d = Math.sqrt(r()) * 82; pts.push([cx + d * Math.cos(a), y + 130 + d * Math.sin(a), i < z * Math.min(n, 120) / n]); }
          pts.sort((a, b) => a[1] - b[1]).forEach(([px, py, pro]) => sphere(c, px, py, 7.5, pro ? [245, 158, 11] : [203, 213, 225]));
        });
        craie.texte(`A = ${n}   Z = ${z}   N = ${n - z}`, cx, y + 255, { align: "center", taille: 18, couleur: accent() });
        craie.texte("protons", x + 20, y + 290, { taille: 15, couleur: "jaune" }).texte("neutrons", x + 110, y + 290, { taille: 15, couleur: "blanc" });
        craie.texte("Eₗ = Δm · c²", x + 190, y + 290, { taille: 18, couleur: "violet" });
        craie.repere('noyau', cx - 95, y + 35, 190, 190, 'le noyau').repere('nucleons', x + 14, y + 272, 170, 28, 'protons et neutrons').repere('formule', x + 184, y + 272, 110, 28, 'Eₗ = Δm·c²');
      } else {
        const total = 90, vivants = Math.round(total * (v.alive ?? 1));
        // L'échantillon : une boîte sombre, chaque noyau en sphère lumineuse ; un noyau désintégré devient une petite sphère grise éteinte.
        peindre((c) => {
          c.save(); c.shadowColor = "rgba(0,0,0,.45)"; c.shadowBlur = 8; c.shadowOffsetY = 3;
          const g = c.createLinearGradient(0, y + 30, 0, y + 220); g.addColorStop(0, "rgba(30,41,59,.85)"); g.addColorStop(1, "rgba(15,23,42,.9)");
          c.fillStyle = g; c.beginPath(); c.roundRect(x + 20, y + 30, 250, 190, 8); c.fill(); c.restore();
          c.strokeStyle = "rgba(226,232,240,.35)"; c.lineWidth = 1.5; c.beginPath(); c.roundRect(x + 20, y + 30, 250, 190, 8); c.stroke();
          const r = graine(7);
          for (let i = 0; i < total; i++) {
            const px = x + 32 + (i % 15) * 16.5, py = y + 45 + Math.floor(i / 15) * 29, vif = i < vivants || !done;
            if (vif) {
              const gl = c.createRadialGradient(px, py, 1, px, py, 9); gl.addColorStop(0, rgba(RGB(accent()), .35)); gl.addColorStop(1, rgba(RGB(accent()), 0));
              c.fillStyle = gl; c.beginPath(); c.arc(px, py, 9, 0, Math.PI * 2); c.fill();
              sphere(c, px, py, 5, RGB(accent()));
            } else {
              sphere(c, px, py, 3.6, [100, 110, 122], .8);
              c.strokeStyle = "rgba(248,113,113,.55)"; c.lineWidth = 1.2; c.beginPath(); c.moveTo(px - 4, py - 4); c.lineTo(px + 4, py + 4); c.moveTo(px - 4, py + 4); c.lineTo(px + 4, py - 4); c.stroke();
            }
            if (run && r() < .08) { const ge = c.createLinearGradient(px + 6, py - 6, px + 16, py - 16); ge.addColorStop(0, "rgba(253,224,71,.9)"); ge.addColorStop(1, "rgba(253,224,71,0)"); c.strokeStyle = ge; c.lineWidth = 2; c.beginPath(); c.moveTo(px + 6, py - 6); c.lineTo(px + 16, py - 16); c.stroke(); }
          }
        });
        craie.texte("échantillon", x + 145, y + 240, { align: "center", taille: 15, couleur: "faible" });
        const iso = isotopeData[p.isotope];
        craie.texte(`${iso.name} · t½ = ${fmt(iso.halfLife, 2)} ${iso.unit}`, cx, y + 262, { align: "center", taille: 17, couleur: accent() });
        craie.texte(model === "radio_dating" ? `N / N₀ = ${fmt(p.ratio, 3)}` : `N₀ = ${p.n0}   t = ${fmt(p.elapsed, 1)} t½`, x + 20, y + 292, { taille: 17, couleur: "jaune" });
        craie.texte("N(t) = N₀ · 2^(−t / t½)", x + 20, y + 320, { taille: 18, couleur: "violet" });
        craie.repere('echantillon', x + 20, y + 30, 250, 190, 'échantillon de noyaux').repere('isotope', x + 20, y + 246, 250, 24, 'isotope et demi-vie').repere('formule', x + 14, y + 300, 230, 30, 'loi de décroissance');
        if (done) { craie.depuis(scene.marque); craie.texte(`${result.primary.value} ${result.primary.unit}`, x + 20, y + 348, { taille: 17, couleur: accent(), max: 270 }); }
      }
    } else if (kind === "equilibrium") {
      if (model === "titration") {
        // Burette de verre peinte (la soude bleutée y descend), robinet, goutte qui tombe.
        peindre((c) => {
          const f = clamp(p.vb / 50, 0, 1), forme = () => { c.beginPath(); c.roundRect(cx - 9, y + 10, 18, 120, 2); };
          forme(); c.fillStyle = "rgba(190,220,240,.08)"; c.fill();
          liquide(c, () => { c.beginPath(); c.rect(cx - 8, y + 12, 16, 118); }, cx - 8, cx + 8, y + 12 + 116 * f, y + 130, [96, 165, 250], .5);
          verre(c, forme, cx - 9, y + 10, 120, { largeur: 1.6 });
          c.fillStyle = "rgba(190,220,240,.25)"; c.beginPath(); c.moveTo(cx - 9, y + 130); c.lineTo(cx, y + 145); c.lineTo(cx + 9, y + 130); c.fill();
          c.strokeStyle = "rgba(225,240,252,.85)"; c.lineWidth = 1.6; c.stroke();
          c.fillStyle = "#2b6cb0"; c.beginPath(); c.roundRect(cx - 12, y + 136, 24, 5, 2); c.fill();   // robinet
          c.fillStyle = "rgba(200,228,245,.4)"; c.fillRect(cx - 1.5, y + 145, 3, 15);
        });
        for (let i = 1; i < 6; i++) craie.ligne(cx - 10, y + 10 + i * 20, cx - 2, y + 10 + i * 20, { largeur: 1.2, couleur: "faible", duree: .03 });
        craie.texte("burette : base", cx + 20, y + 40, { taille: 15, couleur: "bleu" }).texte(`Vᵦ = ${fmt(p.vb, 1)} mL`, cx + 20, y + 64, { taille: 16, couleur: "jaune" });
        // Teinte progressive : rose avant l'équivalence, violet autour, bleue après (plus de saut d'une couleur à l'autre).
        const ratio = result?.visual?.ratio ?? 0, teinte = melange(RGB("rose"), RGB("bleu"), doux((ratio - .94) / .12));
        becher(cx - 45, y + 175, 90, 95, .55, teinte, { label: "acide dosé" });
        if (run) peindre((c) => {
          const f = (scene.now * .0015) % 1, gx = cx, gy = y + 162 + f * 40, r = 3;
          const g = c.createRadialGradient(gx - 1, gy, .5, gx, gy + 1, r * 1.3); g.addColorStop(0, "rgba(235,248,255,.95)"); g.addColorStop(1, "rgba(96,165,250,.85)");
          c.fillStyle = g; c.beginPath(); c.moveTo(gx, gy - r * 2); c.quadraticCurveTo(gx + r * 1.1, gy - r * .2, gx + r, gy + r * .3); c.arc(gx, gy + r * .3, r, 0, Math.PI); c.quadraticCurveTo(gx - r * 1.1, gy - r * .2, gx, gy - r * 2); c.fill();
        });
        peindre((c) => { boitier(c, x + 10, y + 180, 70, 44, { x: x + 15, y: y + 185, w: 60, h: 30 }); cable(c, x + 80, y + 202, cx - 20, y + 186, 10); sondePH(c, cx - 20, y + 186, y + 255); });
        craie.texte("pH-mètre", x + 45, y + 240, { align: "center", taille: 14, couleur: "faible" });
        if (done) { craie.depuis(scene.marque); craie.texte(`pH = ${result.measurements[0].value}`, x + 45, y + 208, { align: "center", taille: 18, couleur: accent() }); }
        craie.texte("à l’équivalence : n(H₃O⁺) = n(HO⁻)", x + 10, y + 310, { taille: 16, couleur: "violet", max: 280 });
        craie.repere('burette', cx - 14, y + 6, 28, 158, 'burette graduée').repere('becher', cx - 48, y + 172, 96, 100, 'bécher d’acide dosé').repere('ph_metre', x + 6, y + 176, 78, 52, 'pH-mètre').repere('formule', x + 6, y + 292, 280, 26, 'relation à l’équivalence');
      } else if (model === "weak_acid") {
        becher(cx - 60, y + 90, 120, 150, .65, "rose", { label: "solution d’acide AH", alpha: .1 });
        peindre((c) => { boitier(c, x + 10, y + 20, 110, 50, { x: x + 16, y: y + 26, w: 98, h: 34 }); cable(c, x + 120, y + 45, cx + 20, y + 110, 20); sondePH(c, cx + 20, y + 110, y + 200); });
        craie.texte("pH-mètre", x + 65, y + 90, { align: "center", taille: 14, couleur: "faible" });
        if (done) { craie.depuis(scene.marque); craie.texte(`pH = ${result.measurements[0].value}`, x + 65, y + 52, { align: "center", taille: 20, couleur: accent() }); }
        craie.texte(`c = ${fmt(p.concentration, 3)} mol·L⁻¹`, x + 140, y + 40, { taille: 15, couleur: "jaune", max: 150 });
        craie.texte("AH + H₂O ⇌ A⁻ + H₃O⁺", cx, y + 290, { align: "center", taille: 19, couleur: "violet" });
        craie.repere('becher', cx - 64, y + 86, 128, 158, 'solution d’acide faible').repere('ph_metre', x + 6, y + 16, 118, 58, 'pH-mètre').repere('sonde', cx + 8, y + 104, 24, 100, 'sonde pH').repere('formule', cx - 120, y + 268, 240, 30, 'équation de la réaction');
        craie.direct(() => { const alpha = v.ratio ?? 0; const r = graine(3); for (let i = 0; i < 24; i++) { const px = cx - 50 + r() * 100, py = y + 150 + r() * 80; craie.texte(i / 24 < alpha ? "A⁻" : "AH", px, py, { taille: 12, couleur: i / 24 < alpha ? accent() : "faible", alpha: .8 }); } });
      } else if (model === "precipitation") {
        const precipite = (result?.visual?.drops ?? 0) > 0;
        becher(cx - 70, y + 60, 140, 170, .7, [125, 211, 252], { label: p.salt === "caf2" ? "Ca²⁺ + F⁻" : "Ag⁺ + Cl⁻", alpha: .1 });
        // Le précipité : un trouble blanc laiteux, puis des grains blancs qui se déposent au fond.
        peindre((c) => {
          if (!done || !precipite) return;
          const g = c.createLinearGradient(0, y + 120, 0, y + 228); g.addColorStop(0, "rgba(241,245,249,0)"); g.addColorStop(1, "rgba(241,245,249,.32)");
          c.fillStyle = g; c.fillRect(cx - 68, y + 120, 136, 108);
          for (let i = 0; i < 70; i++) { const r = graine(i + 1)(); sphere(c, cx - 64 + (i * 17 % 128), y + 216 + r * 10 - (i % 3) * 3, 3, [241, 245, 249], .95); }
        });
        craie.texte(`[M] = 10^${p.logM}   [X] = 10^${p.logX}`, cx, y + 40, { align: "center", taille: 16, couleur: "jaune" });
        if (done) { craie.depuis(scene.marque); craie.texte(precipite ? "précipité : Q > Kₛ" : "limpide : Q < Kₛ", cx, y + 270, { align: "center", taille: 19, couleur: precipite ? accent() : "faible" }); }
        craie.texte("Q = [M]·[X]  comparé à  Kₛ", cx, y + 310, { align: "center", taille: 17, couleur: "violet" });
        craie.repere('becher', cx - 74, y + 56, 148, 178, 'bécher').repere('precipite', cx - 70, y + 196, 140, 36, 'fond du bécher : précipité').repere('concentrations', cx - 110, y + 22, 220, 26, 'concentrations').repere('formule', cx - 120, y + 288, 240, 30, 'Q comparé à Kₛ');
      } else {
        fiole(cx - 70, y + 40, 140, 170, .6, accent());
        craie.texte("A + B", x + 30, y + 250, { taille: 20, couleur: "blanc" });
        fleches2sens(x + 100, y + 244, 70, done ? (v.direction ?? 0) : 0);
        craie.texte("C", x + 185, y + 250, { taille: 20, couleur: accent() });
        craie.texte(`K = ${fmt(p.K, 2)}`, x + 220, y + 250, { taille: 17, couleur: "jaune" });
        // Les particules : C (couleur du labo) et A, B (gris clair), en sphères ombrées qui frémissent.
        peindre((c) => { const r = graine(5); const ratio = v.ratio ?? (p.c0 / (p.a0 + p.b0 + p.c0)); for (let i = 0; i < 30; i++) { const px = cx - 50 + r() * 100 + Math.sin(scene.now * .002 + i) * 1.5, py = y + 110 + r() * 85; sphere(c, px, py, 3.6, i / 30 < ratio ? RGB(accent()) : [203, 213, 225]); } });
        craie.texte("Qᵣ évolue vers K, puis les deux sens s’équilibrent", x + 20, y + 300, { taille: 15, couleur: "violet", max: 275 });
        craie.repere('fiole', cx - 74, y + 36, 148, 178, 'erlenmeyer').repere('fleches', x + 96, y + 226, 78, 36, 'les deux sens ⇌').repere('constante_k', x + 214, y + 230, 70, 28, 'constante K').repere('formule', x + 14, y + 282, 280, 26, 'évolution vers K');
      }
    } else if (kind === "electrochem") {
      if (model === "electrolysis") {
        becher(cx - 80, y + 110, 160, 150, .7, p.product === "copper" ? [59, 130, 246] : [125, 211, 252], { label: "électrolyte", alpha: p.product === "copper" ? .16 : .08 });
        // Électrodes : cathode en graphite (−), anode en cuivre (+) ; fils noirs ; dépôt de cuivre sur la cathode.
        peindre((c) => {
          c.strokeStyle = "#94a3b8"; c.lineWidth = 2.6; c.lineJoin = "round";
          c.beginPath(); c.moveTo(cx - 40, y + 60); c.lineTo(cx - 40, y + 30); c.lineTo(cx - 14, y + 30); c.moveTo(cx + 14, y + 30); c.lineTo(cx + 40, y + 30); c.lineTo(cx + 40, y + 60); c.stroke();
          plaque(c, cx - 40, y + 60, y + 240, 9, [80, 86, 96]); plaque(c, cx + 40, y + 60, y + 240, 9, [205, 112, 52]);
          if ((run || done) && p.product === "copper") { const e = done ? 1 : .4; c.fillStyle = `rgba(184,92,40,${.55 * e})`; for (let k = 0; k < 14; k++) { c.beginPath(); c.arc(cx - 45 + (k % 2) * 10, y + 160 + k * 5.5, 2.4, 0, Math.PI * 2); c.fill(); } }
        });
        craie.cercle(cx, y + 30, 14, { couleur: "jaune" }).texte("G", cx, y + 36, { align: "center", taille: 15, couleur: "jaune" });
        craie.texte("−", cx - 40, y + 55, { align: "center", taille: 18, couleur: "cyan" }).texte("+", cx + 40, y + 55, { align: "center", taille: 18, couleur: "orange" });
        craie.texte(`I = ${fmt(p.current, 2)} A   t = ${fmt(p.time, 0)} min`, cx, y + 305, { align: "center", taille: 16, couleur: "jaune" });
        if (run || done) bulles(cx - 56, y + 150, 24, 90, v.bubbles ? 10 : 4, v.speed || 1, "blanc");
        craie.texte("Q = I · t   ;   n(e⁻) = Q / F", x + 20, y + 338, { taille: 17, couleur: "violet" });
        craie.repere('electrolyseur', cx - 84, y + 106, 168, 158, 'électrolyseur').repere('cathode', cx - 52, y + 56, 24, 190, 'cathode (−)').repere('anode', cx + 28, y + 56, 24, 190, 'anode (+)')
          .repere('generateur', cx - 18, y + 12, 36, 36, 'générateur').repere('formule', x + 14, y + 320, 270, 28, 'loi de Faraday');
      } else {
        becher(x + 20, y + 120, 100, 130, .65, [203, 213, 225], { label: "Zn²⁺ / Zn", alpha: .06 });
        becher(x + 170, y + 120, 100, 130, .65, [37, 99, 235], { label: "Cu²⁺ / Cu", alpha: .2 });
        // Lames de zinc (gris bleuté) et de cuivre (orangé), pont salin en verre rempli de gel, électrons en petites sphères.
        peindre((c) => {
          plaque(c, x + 70, y + 60, y + 230, 10, [168, 178, 190]); plaque(c, x + 220, y + 60, y + 230, 10, [205, 112, 52]);
          const u = () => { c.beginPath(); c.moveTo(x + 105, y + 175); c.lineTo(x + 105, y + 116); c.quadraticCurveTo(x + 105, y + 110, x + 111, y + 110); c.lineTo(x + 179, y + 110); c.quadraticCurveTo(x + 185, y + 110, x + 185, y + 116); c.lineTo(x + 185, y + 175); };
          c.lineCap = "round"; c.lineJoin = "round";
          c.strokeStyle = "rgba(225,240,252,.75)"; c.lineWidth = 11; u(); c.stroke();
          c.strokeStyle = "rgba(253,230,138,.75)"; c.lineWidth = 7.5; u(); c.stroke();
          c.strokeStyle = "rgba(255,255,255,.35)"; c.lineWidth = 1.5; c.beginPath(); c.moveTo(x + 102.5, y + 172); c.lineTo(x + 102.5, y + 116); c.stroke();
          c.strokeStyle = "#94a3b8"; c.lineWidth = 2.6; c.beginPath(); c.moveTo(x + 70, y + 60); c.lineTo(x + 70, y + 30); c.lineTo(x + 125, y + 30); c.moveTo(x + 220, y + 60); c.lineTo(x + 220, y + 30); c.lineTo(x + 165, y + 30); c.stroke();
          const gv = c.createRadialGradient(cx - 6, y + 24, 2, cx, y + 30, 22); gv.addColorStop(0, "#f8fafc"); gv.addColorStop(1, "#cbd5e1");
          c.fillStyle = gv; c.beginPath(); c.arc(cx, y + 30, 19, 0, Math.PI * 2); c.fill();
        });
        craie.cercle(cx, y + 30, 20, { couleur: "blanc" }).texte("V", cx, y + 37, { align: "center", taille: 18, couleur: "#1f2937" });
        craie.texte("pont salin", cx, y + 100, { align: "center", taille: 14, couleur: "jaune" });
        craie.texte("Zn", x + 55, y + 55, { taille: 15, couleur: "faible" }).texte("Cu", x + 230, y + 55, { taille: 15, couleur: "orange" });
        if (done) { craie.depuis(scene.marque); craie.texte(`E = ${fmt(v.voltage, 3)} V`, cx, y + 80, { align: "center", taille: 18, couleur: accent() }); }
        if (done) craie.direct(() => { for (let i = 0; i < 8; i++) { const f = ((scene.now * .00025 * (v.speed || 1)) + i / 8) % 1; const qx = f < .25 ? x + 70 : f < .75 ? x + 70 + (f - .25) * 2 * 150 : x + 220; const qy = f < .25 ? y + 60 - f * 4 * 30 : f < .75 ? y + 30 : y + 30 + (f - .75) * 4 * 30; sphere(craie.ctx, qx, qy, 3, [34, 211, 238]); craie.texte("e⁻", qx, qy - 6, { taille: 12, couleur: "cyan" }); } });
        craie.texte("Zn → Zn²⁺ + 2e⁻   ;   Cu²⁺ + 2e⁻ → Cu", x + 15, y + 300, { taille: 15, couleur: "violet", max: 280 });
        craie.texte(`[Zn²⁺] = 10^${p.logZn}   [Cu²⁺] = 10^${p.logCu}`, x + 15, y + 325, { taille: 14, couleur: "jaune", max: 280 });
        craie.repere('demi_pile_zn', x + 16, y + 116, 108, 138, 'demi-pile Zn²⁺/Zn').repere('demi_pile_cu', x + 166, y + 116, 108, 138, 'demi-pile Cu²⁺/Cu')
          .repere('electrode_zn', x + 60, y + 56, 20, 178, 'électrode de zinc').repere('electrode_cu', x + 210, y + 56, 20, 178, 'électrode de cuivre')
          .repere('pont_salin', x + 100, y + 104, 90, 76, 'pont salin').repere('voltmetre', cx - 22, y + 8, 44, 44, 'voltmètre').repere('fil', x + 70, y + 24, 150, 14, 'fil : circulation des électrons')
          .repere('equation', x + 10, y + 282, 284, 26, 'demi-équations').repere('concentrations', x + 10, y + 308, 284, 24, 'concentrations');
      }
    } else if (kind === "organic") {
      const rendement = v.yield ?? 0, chaud = run || done;
      // Chauffe-ballon : coque sombre, cuvette qui rougeoie quand on chauffe.
      peindre((c) => {
        c.save(); c.shadowColor = "rgba(0,0,0,.45)"; c.shadowBlur = 8; c.shadowOffsetY = 3;
        const g = c.createLinearGradient(0, y + 215, 0, y + 255); g.addColorStop(0, "#4b5563"); g.addColorStop(1, "#1f2937");
        c.fillStyle = g; c.beginPath(); c.roundRect(cx - 55, y + 215, 110, 40, 8); c.fill(); c.restore();
        const gl = c.createRadialGradient(cx, y + 222, 4, cx, y + 222, 52); gl.addColorStop(0, chaud ? "rgba(251,146,60,.85)" : "rgba(251,146,60,.25)"); gl.addColorStop(1, "rgba(251,146,60,0)");
        c.fillStyle = gl; c.beginPath(); c.ellipse(cx, y + 222, 52, 12, 0, 0, Math.PI * 2); c.fill();
        c.fillStyle = chaud ? "#ef4444" : "#7f1d1d"; c.beginPath(); c.arc(cx + 40, y + 243, 3, 0, Math.PI * 2); c.fill();
      });
      ballon(cx, y + 185, 48, .55, melange(RGB("jaune"), RGB(accent()), done ? 1 : clamp(rendement, 0, 1)));
      // Réfrigérant à eau : manchon de verre, eau bleue qui circule, tube intérieur, tuyaux.
      peindre((c) => {
        c.fillStyle = "rgba(190,220,240,.1)"; c.beginPath(); c.roundRect(cx - 10, y + 20, 20, 90, 5); c.fill();
        const ge = c.createLinearGradient(cx - 9, 0, cx + 9, 0); ge.addColorStop(0, "rgba(37,99,235,.55)"); ge.addColorStop(.45, "rgba(147,197,253,.4)"); ge.addColorStop(1, "rgba(37,99,235,.55)");
        c.fillStyle = ge; c.fillRect(cx - 8.5, y + 24, 17, 82);
        c.fillStyle = "rgba(225,240,252,.25)"; c.fillRect(cx - 3, y + 14, 6, 98); c.strokeStyle = "rgba(225,240,252,.7)"; c.lineWidth = 1; c.strokeRect(cx - 3, y + 14, 6, 98);
        c.strokeStyle = "rgba(225,240,252,.85)"; c.lineWidth = 1.8; c.beginPath(); c.roundRect(cx - 10, y + 20, 20, 90, 5); c.stroke();
        c.strokeStyle = "#1e40af"; c.lineWidth = 5; c.lineCap = "round"; c.beginPath(); c.moveTo(cx - 10, y + 40); c.lineTo(cx - 30, y + 40); c.moveTo(cx - 10, y + 90); c.lineTo(cx - 30, y + 90); c.stroke();
        if (chaud) for (let k = 0; k < 3; k++) { const f = ((scene.now * .0004) + k / 3) % 1; c.fillStyle = "rgba(255,255,255,.5)"; c.beginPath(); c.arc(cx + 5, y + 104 - f * 80, 1.6, 0, Math.PI * 2); c.fill(); }
      });
      craie.texte("chauffe-ballon", cx, y + 275, { align: "center", taille: 14, couleur: "orange" });
      craie.texte("réfrigérant", cx + 20, y + 50, { taille: 14, couleur: "cyan" });
      craie.texte("eau", cx - 48, y + 94, { taille: 12, couleur: "cyan" });
      if (p.temp !== undefined) thermometre(x + 40, y + 120, 90, (p.temp - 40) / 60, `${fmt(p.temp, 0)} °C`);
      if (run || done) bulles(cx - 30, y + 170, 60, 40, 6, v.speed || .7, "blanc");
      craie.texte("acide + alcool ⇌ ester + eau", cx, y + 310, { align: "center", taille: 18, couleur: "violet" });
      craie.repere('ballon', cx - 52, y + 100, 104, 136, 'ballon réactionnel').repere('refrigerant', cx - 14, y + 16, 28, 98, 'réfrigérant à eau').repere('chauffe_ballon', cx - 58, y + 212, 116, 46, 'chauffe-ballon')
        .repere('equation', cx - 130, y + 290, 260, 28, 'équation d’estérification');
      if (p.temp !== undefined) craie.repere('thermometre', x + 26, y + 116, 30, 108, 'thermomètre');
      if (done) { craie.depuis(scene.marque); craie.texte(`${result.primary.label} : ${result.primary.value} ${result.primary.unit}`, cx, y + 338, { align: "center", taille: 17, couleur: accent(), max: 280 }); }
      else craie.texte(model === "ester_kinetics" ? (p.catalyst === "acid" ? "avec H₂SO₄ (catalyseur)" : "sans catalyseur") : model === "synthesis_control" ? (p.pathway === "saponification" ? "voie : saponification" : "voie : estérification") : `K = ${fmt(p.K, 1)}`, cx, y + 338, { align: "center", taille: 15, couleur: "jaune" });
    }
  }

  function dessinerCourbe(result, axis, progress) {
    const { x, y, w, h } = G;
    craie.repere('courbe', x - 6, y - 16, w + 20, h + 36, 'la courbe');
    craie.texte(axis.y || "mesure", x - 4, y - 10, { taille: 14, couleur: "faible" });
    if (!result) {
      craie.axe(x, y + h, x + w + 10, y + h, [], { couleur: "faible" }).axe(x, y + h, x, y - 4, [], { couleur: "faible", vertical: true });
      craie.texte(axis.x || "", x + w + 10, y + h + 20, { align: "right", taille: 14, couleur: "faible" });
      craie.texte("la courbe se tracera au premier essai", x + w / 2, y + h / 2, { align: "center", taille: 14, couleur: "tresfaible", max: w - 10 });
      return;
    }
    const series = result.series;
    let minX = Math.min(...series.map(q => q.x)), maxX = Math.max(...series.map(q => q.x)), minY = Math.min(...series.map(q => q.y)), maxY = Math.max(...series.map(q => q.y));
    if (maxX === minX) maxX = minX + 1; if (maxY === minY) { maxY += 1; minY -= 1; } const m = (maxY - minY) * .08; minY -= m; maxY += m;
    craie.axe(x, y + h, x + w + 10, y + h, [[0, fmt(minX, 1)], [w / (w + 10), fmt(maxX, 1)]], { couleur: "faible", taille: 12 });
    craie.axe(x, y + h, x, y - 4, [[(maxY - m - minY) / (maxY - minY), fmt(maxY - m, 2)], [(0 + m) / (maxY - minY) * 0 + (minY + m - minY) / (maxY - minY), fmt(minY + m, 2)]], { couleur: "faible", vertical: true, taille: 12 });
    craie.texte(axis.x || "", x + w + 10, y + h + 32, { align: "right", taille: 13, couleur: "faible" });
    const X = q => x + (q - minX) / (maxX - minX) * w, Y = q => y + h - (q - minY) / (maxY - minY) * h;
    const visible = Math.max(2, Math.ceil(series.length * progress)), data = series.slice(0, visible);
    craie.direct(() => {
      craie.trait(data.map(q => [X(q.x), Y(q.y)]), { couleur: accent(), largeur: 2.6, tremble: .5 });
      const last = data[data.length - 1]; craie.cercle(X(last.x), Y(last.y), 4, { couleur: "blanc", fond: "blanc", fondAlpha: .8, largeur: 1.2 });
    });
  }

  function draw() {
    const W = craie.W, H = craie.H; if (W < 1 || H < 1) return true;
    craie.debut(11, depuisOuverture() * 1.8);   // un peu plus vite qu’au tableau : le montage est fourni
    const s = Math.min(W / LW, H / LH); craie.ctx.translate((W - LW * s) / 2, (H - LH * s) / 2); craie.ctx.scale(s, s);
    const result = state.last_result, m = mission(), p = state.variables;
    const v = result?.visual || { kind: cfg.sceneKind || "kinetics", rate: .4, fraction: 0 };
    craie.texte(m.sceneLabel || m.title, M.x + M.w / 2, 22, { align: "center", taille: 16, couleur: "faible", max: M.w });
    dessinerMontage(m.model, p, v, result);
    craie.ligne(322, 20, 322, 380, { couleur: "tresfaible", largeur: 1, pointille: [6, 8] });
    dessinerCourbe(result, m.axis || {}, state.status === "running" ? state.animation : 1);
    craie.repere('carnet', 330, 192, 216, 160, 'carnet de mesures').repere('mesure', 330, 192, 216, 30, 'mesure principale').repere('montage', M.x, M.y, M.w, M.h, 'le montage');
    if (result) {
      craie.depuis(scene.marque);
      craie.texte(`${result.primary.label} : ${result.primary.value} ${result.primary.unit}`, 336, 212, { taille: 19, couleur: accent(), max: 215 });
      result.measurements.forEach((q, i) => craie.texte(`${q.label} = ${q.value} ${q.unit || ""}`, 336, 246 + i * 26, { taille: 15, couleur: "blanc", max: 215 }));
      craie.texte(state.runCount > 1 ? `essai n° ${state.runCount}` : "premier essai", 336, 340, { taille: 14, couleur: "faible" });
    } else {
      craie.texte("carnet de mesures", 336, 212, { taille: 17, couleur: "faible" });
      ["mesure 1", "mesure 2", "mesure 3"].forEach((t, i) => craie.ligne(336, 250 + i * 26, 540, 250 + i * 26, { couleur: "tresfaible", largeur: 1, pointille: [4, 6] }));
    }
    return craie.fin();
  }

  function boucle(now) {
    scene.now = now;
    if (scene.dirty || state.status === "running" || state.last_result) scene.dirty = !draw();
    requestAnimationFrame(boucle);
  }

  window.SIMULATION_CONFIG = {
    protocol_version: "2.0",
    id: cfg.id,
    title: cfg.title,
    subject: "Chimie 2e BAC",
    chapters: cfg.chapters,
    purpose: cfg.intro,
    missions: cfg.missions.map(m => ({id:m.id,title:m.title,chapter:m.chapter,goal:m.goal,model:m.model,parameters:m.parameters.map(p=>({key:p.key,label:p.label,unit:p.unit||"",type:p.type||"range",min:p.min,max:p.max,options:p.options}))})),
    variants: cfg.missions.map(m => ({id:m.id,label:m.title,objective:m.goal})),
    commands: ["start","reset","set_variant","set_parameters","run_trial","highlight","get_state","set_prediction"],
    state_contract: ["variables","measurements","student_prediction","mission_coverage","trial_history","scientific_observation","model_limits"]
  };
  window.executeAICommand = executeAICommand;
  window.getSimulationState = publicState;
  window.runTrial = runTrial;
  window.resetSimulation = resetSimulation;
  window.selectVariant = selectVariant;
  window.addEventListener("message", (event) => {
    const data=event.data;
    if(!data || data.type!=="simulation_control") return;
    event.stopImmediatePropagation();
    if (data.guidance_text) T.bulle($("#statusText"), data.guidance_text);
    const payload = data.payload || data;
    T.appuyer(payload.command || payload.action || data.command);   // le professeur appuie sur le bouton visé
    const result=executeAICommand(data.payload || data.command || data, data.parameters || {});
    event.source?.postMessage?.({type:"simulation_control_result",requestId:data.requestId,simulation_id:cfg.id,simulationId:cfg.id,result},"*");
  });
  // Script d'explication par mission (champ `explication` de la configuration) : une phrase par repère pointable.
  T.explication(Object.fromEntries(cfg.missions.map((m) => [m.id, (m.explication || []).map((e) => ({ repere: e.repere, texte: e.texte }))])));
  $("#runButton").addEventListener("click",()=>runTrial());
  $("#resetButton").addEventListener("click",resetSimulation);
  initializeVariables();
  buildMissionTabs();
  buildMission();
  syncState();
  const explicationParMission = Object.fromEntries(cfg.missions.map((m) => [m.id, (m.explication || []).map((e) => ({ repere: e.repere, texte: e.texte }))]));
  function manifeste() {
    if (window.parent === window) return;
    const reperes = T.listeReperes();
    window.__SIMULATION_MANIFEST_SENT__ = true;
    window.parent.postMessage({
      type:"simulation_manifest",
      simulation_id:cfg.id,
      simulationId:cfg.id,
      capabilities:{
        commands:window.SIMULATION_CONFIG.commands,
        globals:["executeAICommand","getSimulationState","runTrial","resetSimulation","selectVariant"],
        buttons:cfg.missions.map(m=>({id:m.id,text:m.title,className:"onglet"})),
        config:window.SIMULATION_CONFIG,
        command_schema:{ set_variant:{ variant_id: cfg.missions.map(m => m.id).join(" | ") }, highlight:{ target: Object.keys(reperes).join(" | ") || "scene" } },
        reperes,
        explication: explicationParMission
      },
      page_text:`${cfg.title}. ${cfg.intro} Tout est dessiné à la craie au tableau : le montage à gauche, la courbe et le carnet de mesures à droite. Le professeur peut montrer chaque repère du doigt (highlight) en suivant le script d'explication de la mission.`,
      manifest:window.SIMULATION_CONFIG
    },"*");
  }
  manifeste();
  // Les repères dessinés sont connus après la première image : le manifeste est renvoyé une fois complet
  // (et plus tard encore, au cas où l'iframe n'aurait pas été affichée tout de suite).
  setTimeout(manifeste, 1800); setTimeout(manifeste, 6000); setTimeout(manifeste, 15000);
  requestAnimationFrame(boucle);
})();
