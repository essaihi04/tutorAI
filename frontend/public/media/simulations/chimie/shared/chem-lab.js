/*
 * Laboratoires de chimie — moteur partagé, dessiné au tableau.
 * Chaque page fournit window.CHEM_LAB_CONFIG (missions, modèles, paramètres) ; ce script dessine le montage
 * et la courbe à la craie (shared/tableau/tableau.js), écrit en direct, et garde le pont avec le tuteur :
 * manifeste, état (variables, measurements, student_prediction, trial_history…) et commandes
 * start / run_trial / reset / set_variant / set_parameters / highlight / get_state / set_prediction.
 */
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

  function becher(x, y, w, h, niveau, liquide, o = {}) {
    craie.trait([[x, y], [x, y + h], [x + w, y + h], [x + w, y]], { couleur: "blanc", largeur: 2.2 });
    if (niveau > 0) {
      const ly = y + h - h * clamp(niveau, 0, 1) - 2;
      const c = craie.ctx; c.globalAlpha = o.alpha ?? .18; c.fillStyle = craie.couleur(liquide); c.fillRect(x + 2, ly, w - 4, y + h - ly - 2); c.globalAlpha = 1;
      craie.ligne(x + 2, ly, x + w - 2, ly, { couleur: liquide, largeur: 1.6, tremble: .5 });
    }
    if (o.label) craie.texte(o.label, x + w / 2, y + h + 20, { align: "center", taille: 15, couleur: o.labelCouleur || "faible" });
  }
  function thermometre(x, y, h, frac, label) {
    craie.ligne(x, y, x, y + h, { couleur: "blanc", largeur: 5, alpha: .35 }).cercle(x, y + h + 7, 7, { couleur: "rouge", fond: "rouge", fondAlpha: .6 });
    craie.direct(() => craie.ligne(x, y + h - h * clamp(frac, 0, 1), x, y + h, { couleur: "rouge", largeur: 3, tremble: .2 }));
    if (label) craie.texte(label, x + 12, y + 12, { taille: 15, couleur: "rouge" });
  }
  function bulles(x, y, w, h, n, vitesse, couleur) {
    craie.direct(() => { for (let i = 0; i < n; i++) { const f = ((scene.now * .00012 * vitesse) + i * .173) % 1; craie.cercle(x + w * ((i * 37 % 100) / 100), y + h - f * h, 2 + i % 3, { couleur, largeur: 1.2, tremble: .2, alpha: .7 }); } });
  }
  function fiole(x, y, w, h, niveau, liquide) {
    // Erlenmeyer : col étroit, corps conique.
    const col = w * .3;
    craie.trait([[x + w / 2 - col / 2, y], [x + w / 2 - col / 2, y + h * .3], [x, y + h], [x + w, y + h], [x + w / 2 + col / 2, y + h * .3], [x + w / 2 + col / 2, y]], { couleur: "blanc", largeur: 2.2 });
    if (niveau > 0) { const c = craie.ctx; c.globalAlpha = .18; c.fillStyle = craie.couleur(liquide); const ly = y + h - h * .7 * niveau; const k = (ly - (y + h * .3)) / (h * .7); const half = w / 2 - col / 2; const xl = x + w / 2 - col / 2 - half * k, xr = x + w / 2 + col / 2 + half * k; c.beginPath(); c.moveTo(xl, ly); c.lineTo(xr, ly); c.lineTo(x + w - 2, y + h - 2); c.lineTo(x + 2, y + h - 2); c.closePath(); c.fill(); c.globalAlpha = 1; craie.ligne(xl, ly, xr, ly, { couleur: liquide, largeur: 1.6 }); }
  }
  function ballon(x, y, r, niveau, liquide) {
    craie.cercle(x, y, r, { couleur: "blanc", largeur: 2.2, depart: -1.9 });
    craie.trait([[x - r * .32, y - r * .95], [x - r * .32, y - r * 1.7], [x + r * .32, y - r * 1.7], [x + r * .32, y - r * .95]], { couleur: "blanc", largeur: 2.2 });
    if (niveau > 0) { const c = craie.ctx; c.globalAlpha = .2; c.fillStyle = craie.couleur(liquide); c.beginPath(); c.arc(x, y, r - 2, Math.PI * (.5 - .5 * niveau) * 0 + Math.asin(clamp(1 - 2 * niveau, -1, 1)), Math.PI - Math.asin(clamp(1 - 2 * niveau, -1, 1))); c.closePath(); c.fill(); c.globalAlpha = 1; }
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
        craie.rect(x + 10, y + 70, 80, 60, { couleur: "blanc", arrondi: 6 }).texte("lampe", x + 50, y + 150, { align: "center", taille: 14, couleur: "faible" });
        craie.cercle(x + 50, y + 100, 9, { couleur: "jaune", fond: "jaune", fondAlpha: .5 });
        craie.fleche(x + 92, y + 100, x + 150, y + 100, { couleur: "jaune", largeur: 2 });
        becher(x + 152, y + 60, 36, 80, 1, accent(), { label: "cuve" });
        craie.direct(() => { const c = craie.ctx; c.globalAlpha = .25 * (1 - (v.fraction ?? 0)); c.fillStyle = accent(); c.fillRect(x + 154, y + 62, 32, 76); c.globalAlpha = 1; });
        craie.fleche(x + 190, y + 100, x + 240, y + 100, { couleur: "jaune", largeur: 1.6, alpha: .6 });
        craie.rect(x + 242, y + 70, 44, 60, { couleur: "blanc", arrondi: 6 }).texte("détecteur", x + 264, y + 150, { align: "center", taille: 14, couleur: "faible" });
        craie.texte("spectrophotomètre", cx, y + 30, { align: "center", taille: 19, couleur: accent() });
        craie.repere('lampe', x + 10, y + 70, 80, 60, 'lampe').repere('cuve', x + 148, y + 56, 44, 90, 'cuve de solution').repere('detecteur', x + 242, y + 70, 44, 60, 'détecteur')
          .repere('spectrophotometre', x + 6, y + 10, w - 12, 150, 'spectrophotomètre').repere('formule', x + 14, y + 240, 240, 32, 'loi A(t)');
        craie.texte(`t = ${fmt(p.time, 0)} s`, x + 20, y + 200, { taille: 17, couleur: "jaune" });
        craie.texte(`A₀ = ${fmt(p.a0, 2)}   k = ${fmt(p.k, 3)} s⁻¹`, x + 20, y + 228, { taille: 16, couleur: "faible" });
        craie.texte("A(t) = A₀ · e^(−k t)", x + 20, y + 262, { taille: 18, couleur: "violet" });
        if (done) { craie.depuis(scene.marque); craie.texte(`A = ${result.primary.value}`, x + 180, y + 200, { taille: 22, couleur: accent() }); }
      } else {
        craie.rect(x + 40, y + 120, 200, 110, { couleur: "faible", arrondi: 6 }).texte("bain thermostaté", x + 140, y + 250, { align: "center", taille: 15, couleur: "faible" });
        craie.direct(() => { const c = craie.ctx; c.globalAlpha = .08; c.fillStyle = craie.couleur("cyan"); c.fillRect(x + 42, y + 150, 196, 78); c.globalAlpha = 1; });
        becher(x + 100, y + 95, 80, 125, .7, accent(), { label: "" });
        craie.direct(() => { const c = craie.ctx; c.globalAlpha = .2 * (1 - (v.fraction ?? 0)) + .05; c.fillStyle = accent(); c.fillRect(x + 102, y + 134, 76, 84); c.globalAlpha = 1; });
        thermometre(x + 250, y + 100, 110, (p.temp - 10) / 50, `${fmt(p.temp, 0)} °C`);
        craie.cercle(x + 40, y + 60, 22, { couleur: "blanc" }).texte("t", x + 40, y + 66, { align: "center", taille: 16 }).ligne(x + 40, y + 32, x + 40, y + 38, { largeur: 2 });
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
        craie.direct(() => { const r = graine(n); for (let i = 0; i < Math.min(n, 120); i++) { const a = r() * Math.PI * 2, d = Math.sqrt(r()) * 82; craie.cercle(cx + d * Math.cos(a), y + 130 + d * Math.sin(a), 7, { couleur: i < z * Math.min(n, 120) / n ? "jaune" : "blanc", fond: i < z * Math.min(n, 120) / n ? "jaune" : "blanc", fondAlpha: .35, largeur: 1.2, tremble: .3 }); } });
        craie.texte(`A = ${n}   Z = ${z}   N = ${n - z}`, cx, y + 255, { align: "center", taille: 18, couleur: accent() });
        craie.texte("protons", x + 20, y + 290, { taille: 15, couleur: "jaune" }).texte("neutrons", x + 110, y + 290, { taille: 15, couleur: "blanc" });
        craie.texte("Eₗ = Δm · c²", x + 190, y + 290, { taille: 18, couleur: "violet" });
        craie.repere('noyau', cx - 95, y + 35, 190, 190, 'le noyau').repere('nucleons', x + 14, y + 272, 170, 28, 'protons et neutrons').repere('formule', x + 184, y + 272, 110, 28, 'Eₗ = Δm·c²');
      } else {
        craie.rect(x + 20, y + 30, 250, 190, { couleur: "faible", arrondi: 8 }).texte("échantillon", x + 145, y + 240, { align: "center", taille: 15, couleur: "faible" });
        const total = 90, vivants = Math.round(total * (v.alive ?? 1));
        craie.direct(() => { const r = graine(7); for (let i = 0; i < total; i++) { const px = x + 32 + (i % 15) * 16.5, py = y + 45 + Math.floor(i / 15) * 29; const vif = i < vivants || !done; if (vif) craie.cercle(px, py, 4.5, { couleur: accent(), fond: accent(), fondAlpha: .5, largeur: 1.2, tremble: .2 }); else { craie.ligne(px - 4, py - 4, px + 4, py + 4, { couleur: "rouge", largeur: 1.2, alpha: .5, tremble: .2 }); craie.ligne(px - 4, py + 4, px + 4, py - 4, { couleur: "rouge", largeur: 1.2, alpha: .5, tremble: .2 }); } if (run && r() < .08) craie.ligne(px + 6, py - 6, px + 14, py - 14, { couleur: "jaune", largeur: 1, alpha: .6 }); } });
        const iso = isotopeData[p.isotope];
        craie.texte(`${iso.name} · t½ = ${fmt(iso.halfLife, 2)} ${iso.unit}`, cx, y + 262, { align: "center", taille: 17, couleur: accent() });
        craie.texte(model === "radio_dating" ? `N / N₀ = ${fmt(p.ratio, 3)}` : `N₀ = ${p.n0}   t = ${fmt(p.elapsed, 1)} t½`, x + 20, y + 292, { taille: 17, couleur: "jaune" });
        craie.texte("N(t) = N₀ · 2^(−t / t½)", x + 20, y + 320, { taille: 18, couleur: "violet" });
        craie.repere('echantillon', x + 20, y + 30, 250, 190, 'échantillon de noyaux').repere('isotope', x + 20, y + 246, 250, 24, 'isotope et demi-vie').repere('formule', x + 14, y + 300, 230, 30, 'loi de décroissance');
        if (done) { craie.depuis(scene.marque); craie.texte(`${result.primary.value} ${result.primary.unit}`, x + 20, y + 348, { taille: 17, couleur: accent(), max: 270 }); }
      }
    } else if (kind === "equilibrium") {
      if (model === "titration") {
        craie.rect(cx - 10, y + 10, 20, 120, { couleur: "blanc", arrondi: 2 });
        for (let i = 1; i < 6; i++) craie.ligne(cx - 10, y + 10 + i * 20, cx - 2, y + 10 + i * 20, { largeur: 1.2, couleur: "faible", duree: .03 });
        craie.direct(() => { const c = craie.ctx; c.globalAlpha = .25; c.fillStyle = craie.couleur("bleu"); const f = clamp(p.vb / 50, 0, 1); c.fillRect(cx - 8, y + 12 + 116 * f, 16, 116 * (1 - f)); c.globalAlpha = 1; });
        craie.trait([[cx - 10, y + 130], [cx, y + 145], [cx + 10, y + 130]], { couleur: "blanc", largeur: 2 }).ligne(cx, y + 145, cx, y + 160, { largeur: 2 });
        craie.texte("burette : base", cx + 20, y + 40, { taille: 15, couleur: "bleu" }).texte(`Vᵦ = ${fmt(p.vb, 1)} mL`, cx + 20, y + 64, { taille: 16, couleur: "jaune" });
        becher(cx - 45, y + 175, 90, 95, .55, (result?.visual?.ratio ?? 0) > 1 ? "bleu" : "rose", { label: "acide dosé" });
        if (run) craie.direct(() => { const f = (scene.now * .0015) % 1; craie.cercle(cx, y + 162 + f * 40, 2.5, { couleur: "bleu", fond: "bleu", fondAlpha: .6, largeur: 1 }); });
        craie.rect(x + 10, y + 180, 70, 44, { couleur: "blanc", arrondi: 6 }).texte("pH-mètre", x + 45, y + 240, { align: "center", taille: 14, couleur: "faible" });
        craie.ligne(x + 80, y + 202, cx - 20, y + 240, { couleur: "faible", largeur: 1.4 });
        if (done) { craie.depuis(scene.marque); craie.texte(`pH = ${result.measurements[0].value}`, x + 45, y + 208, { align: "center", taille: 18, couleur: accent() }); }
        craie.texte("à l’équivalence : n(H₃O⁺) = n(HO⁻)", x + 10, y + 310, { taille: 16, couleur: "violet", max: 280 });
        craie.repere('burette', cx - 14, y + 6, 28, 158, 'burette graduée').repere('becher', cx - 48, y + 172, 96, 100, 'bécher d’acide dosé').repere('ph_metre', x + 6, y + 176, 78, 52, 'pH-mètre').repere('formule', x + 6, y + 292, 280, 26, 'relation à l’équivalence');
      } else if (model === "weak_acid") {
        becher(cx - 60, y + 90, 120, 150, .65, "rose", { label: "solution d’acide AH" });
        craie.rect(x + 10, y + 20, 110, 50, { couleur: "blanc", arrondi: 6 }).texte("pH-mètre", x + 65, y + 90, { align: "center", taille: 14, couleur: "faible" });
        craie.ligne(x + 120, y + 45, cx + 20, y + 110, { couleur: "faible", largeur: 1.4 }).ligne(cx + 20, y + 110, cx + 20, y + 200, { couleur: "blanc", largeur: 3, alpha: .5 });
        if (done) { craie.depuis(scene.marque); craie.texte(`pH = ${result.measurements[0].value}`, x + 65, y + 52, { align: "center", taille: 20, couleur: accent() }); }
        craie.texte(`c = ${fmt(p.concentration, 3)} mol·L⁻¹`, x + 140, y + 40, { taille: 15, couleur: "jaune", max: 150 });
        craie.texte("AH + H₂O ⇌ A⁻ + H₃O⁺", cx, y + 290, { align: "center", taille: 19, couleur: "violet" });
        craie.repere('becher', cx - 64, y + 86, 128, 158, 'solution d’acide faible').repere('ph_metre', x + 6, y + 16, 118, 58, 'pH-mètre').repere('sonde', cx + 8, y + 104, 24, 100, 'sonde pH').repere('formule', cx - 120, y + 268, 240, 30, 'équation de la réaction');
        craie.direct(() => { const alpha = v.ratio ?? 0; const r = graine(3); for (let i = 0; i < 24; i++) { const px = cx - 50 + r() * 100, py = y + 150 + r() * 80; craie.texte(i / 24 < alpha ? "A⁻" : "AH", px, py, { taille: 12, couleur: i / 24 < alpha ? accent() : "faible", alpha: .8 }); } });
      } else if (model === "precipitation") {
        const precipite = (result?.visual?.drops ?? 0) > 0;
        becher(cx - 70, y + 60, 140, 170, .7, "cyan", { label: p.salt === "caf2" ? "Ca²⁺ + F⁻" : "Ag⁺ + Cl⁻" });
        craie.direct(() => { if (!done) return; const c = craie.ctx; if (precipite) { c.globalAlpha = .5; c.fillStyle = craie.couleur("blanc"); for (let i = 0; i < 40; i++) { const r = graine(i + 1)(); c.fillRect(cx - 66 + (i * 13 % 130), y + 205 + r * 20, 3, 3); } c.globalAlpha = 1; } });
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
        craie.direct(() => { const r = graine(5); const ratio = v.ratio ?? (p.c0 / (p.a0 + p.b0 + p.c0)); for (let i = 0; i < 30; i++) { const px = cx - 50 + r() * 100, py = y + 110 + r() * 85; craie.cercle(px, py, 3, { couleur: i / 30 < ratio ? accent() : "faible", fond: i / 30 < ratio ? accent() : "faible", fondAlpha: .5, largeur: 1, tremble: .2 }); } });
        craie.texte("Qᵣ évolue vers K, puis les deux sens s’équilibrent", x + 20, y + 300, { taille: 15, couleur: "violet", max: 275 });
        craie.repere('fiole', cx - 74, y + 36, 148, 178, 'erlenmeyer').repere('fleches', x + 96, y + 226, 78, 36, 'les deux sens ⇌').repere('constante_k', x + 214, y + 230, 70, 28, 'constante K').repere('formule', x + 14, y + 282, 280, 26, 'évolution vers K');
      }
    } else if (kind === "electrochem") {
      if (model === "electrolysis") {
        becher(cx - 80, y + 110, 160, 150, .7, "cyan", { label: "électrolyte" });
        craie.ligne(cx - 40, y + 60, cx - 40, y + 240, { couleur: "blanc", largeur: 4 }).ligne(cx + 40, y + 60, cx + 40, y + 240, { couleur: "orange", largeur: 4 });
        craie.ligne(cx - 40, y + 60, cx - 40, y + 30, { largeur: 2 }).ligne(cx - 40, y + 30, cx - 14, y + 30, { largeur: 2 }).ligne(cx + 14, y + 30, cx + 40, y + 30, { largeur: 2 }).ligne(cx + 40, y + 30, cx + 40, y + 60, { largeur: 2 });
        craie.cercle(cx, y + 30, 14, { couleur: "jaune" }).texte("G", cx, y + 36, { align: "center", taille: 15, couleur: "jaune" });
        craie.texte("−", cx - 40, y + 55, { align: "center", taille: 18, couleur: "cyan" }).texte("+", cx + 40, y + 55, { align: "center", taille: 18, couleur: "orange" });
        craie.texte(`I = ${fmt(p.current, 2)} A   t = ${fmt(p.time, 0)} min`, cx, y + 305, { align: "center", taille: 16, couleur: "jaune" });
        if (run || done) bulles(cx - 56, y + 150, 24, 90, v.bubbles ? 10 : 4, v.speed || 1, "blanc");
        craie.texte("Q = I · t   ;   n(e⁻) = Q / F", x + 20, y + 338, { taille: 17, couleur: "violet" });
        craie.repere('electrolyseur', cx - 84, y + 106, 168, 158, 'électrolyseur').repere('cathode', cx - 52, y + 56, 24, 190, 'cathode (−)').repere('anode', cx + 28, y + 56, 24, 190, 'anode (+)')
          .repere('generateur', cx - 18, y + 12, 36, 36, 'générateur').repere('formule', x + 14, y + 320, 270, 28, 'loi de Faraday');
      } else {
        becher(x + 20, y + 120, 100, 130, .65, "faible", { label: "Zn²⁺ / Zn" });
        becher(x + 170, y + 120, 100, 130, .65, "bleu", { label: "Cu²⁺ / Cu" });
        craie.ligne(x + 70, y + 60, x + 70, y + 230, { couleur: "faible", largeur: 5 }).ligne(x + 220, y + 60, x + 220, y + 230, { couleur: "orange", largeur: 5 });
        craie.trait([[x + 105, y + 175], [x + 105, y + 110], [x + 185, y + 110], [x + 185, y + 175]], { couleur: "jaune", largeur: 6, alpha: .45 }).texte("pont salin", cx, y + 100, { align: "center", taille: 14, couleur: "jaune" });
        craie.trait([[x + 70, y + 60], [x + 70, y + 30], [x + 125, y + 30]], { largeur: 2 }).trait([[x + 220, y + 60], [x + 220, y + 30], [x + 165, y + 30]], { largeur: 2 });
        craie.cercle(cx, y + 30, 20, { couleur: "blanc" }).texte("V", cx, y + 37, { align: "center", taille: 18 });
        craie.texte("Zn", x + 55, y + 55, { taille: 15, couleur: "faible" }).texte("Cu", x + 230, y + 55, { taille: 15, couleur: "orange" });
        if (done) { craie.depuis(scene.marque); craie.texte(`E = ${fmt(v.voltage, 3)} V`, cx, y + 80, { align: "center", taille: 18, couleur: accent() }); }
        if (done) craie.direct(() => { for (let i = 0; i < 8; i++) { const f = ((scene.now * .00025 * (v.speed || 1)) + i / 8) % 1; const px = f < .5 ? x + 70 : x + 220, py = f < .5 ? y + 60 - (f * 2) * 30 : y + 30 + ((f - .5) * 2) * 30; const qx = f < .25 ? x + 70 : f < .75 ? x + 70 + (f - .25) * 2 * 150 : x + 220; const qy = f < .25 ? y + 60 - f * 4 * 30 : f < .75 ? y + 30 : y + 30 + (f - .75) * 4 * 30; craie.texte("e⁻", qx, qy - 6, { taille: 12, couleur: "cyan" }); void px; void py; } });
        craie.texte("Zn → Zn²⁺ + 2e⁻   ;   Cu²⁺ + 2e⁻ → Cu", x + 15, y + 300, { taille: 15, couleur: "violet", max: 280 });
        craie.texte(`[Zn²⁺] = 10^${p.logZn}   [Cu²⁺] = 10^${p.logCu}`, x + 15, y + 325, { taille: 14, couleur: "jaune", max: 280 });
        craie.repere('demi_pile_zn', x + 16, y + 116, 108, 138, 'demi-pile Zn²⁺/Zn').repere('demi_pile_cu', x + 166, y + 116, 108, 138, 'demi-pile Cu²⁺/Cu')
          .repere('electrode_zn', x + 60, y + 56, 20, 178, 'électrode de zinc').repere('electrode_cu', x + 210, y + 56, 20, 178, 'électrode de cuivre')
          .repere('pont_salin', x + 100, y + 104, 90, 76, 'pont salin').repere('voltmetre', cx - 22, y + 8, 44, 44, 'voltmètre').repere('fil', x + 70, y + 24, 150, 14, 'fil : circulation des électrons')
          .repere('equation', x + 10, y + 282, 284, 26, 'demi-équations').repere('concentrations', x + 10, y + 308, 284, 24, 'concentrations');
      }
    } else if (kind === "organic") {
      const rendement = v.yield ?? 0;
      craie.rect(cx - 55, y + 215, 110, 40, { couleur: "orange", arrondi: 8 }).texte("chauffe-ballon", cx, y + 275, { align: "center", taille: 14, couleur: "orange" });
      ballon(cx, y + 185, 48, .55, done ? accent() : "jaune");
      craie.direct(() => { const c = craie.ctx; c.save(); c.globalAlpha = .22; c.fillStyle = accent(); c.beginPath(); c.arc(cx, y + 185, 44, 0, Math.PI * 2); c.clip(); c.fillRect(cx - 48, y + 185 + 44 - 70 * clamp(rendement, 0, 1), 96, 70); c.restore(); });
      craie.rect(cx - 10, y + 20, 20, 90, { couleur: "cyan", arrondi: 4 }).texte("réfrigérant", cx + 20, y + 50, { taille: 14, couleur: "cyan" });
      craie.ligne(cx - 10, y + 40, cx - 30, y + 40, { couleur: "cyan", largeur: 1.6 }).ligne(cx - 10, y + 90, cx - 30, y + 90, { couleur: "cyan", largeur: 1.6 });
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
