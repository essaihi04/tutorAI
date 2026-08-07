(function () {
  "use strict";

  const cfg = window.CHEM_LAB_CONFIG;
  if (!cfg) throw new Error("CHEM_LAB_CONFIG manquant");

  const $ = (s, root = document) => root.querySelector(s);
  const clamp = (v, lo, hi) => Math.min(hi, Math.max(lo, v));
  const log10 = (v) => Math.log(v) / Math.LN10;
  const fmt = (v, digits = 3) => {
    if (typeof v !== "number" || !Number.isFinite(v)) return String(v ?? "—");
    const a = Math.abs(v);
    if ((a > 0 && a < 0.001) || a >= 10000) return v.toExponential(2).replace("e+", "e");
    return Number(v.toFixed(digits)).toLocaleString("fr-FR");
  };
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

  document.documentElement.style.setProperty("--accent", cfg.accent || "#38bdf8");
  document.documentElement.style.setProperty("--accent-rgb", cfg.accentRgb || "56, 189, 248");
  document.title = cfg.title;
  document.body.innerHTML = `
    <div class="app">
      <header class="topbar">
        <div class="brand">χ</div>
        <div class="titleblock"><div class="eyebrow">Laboratoire virtuel · 2e BAC</div><h1>${cfg.title}</h1></div>
        <div class="chapter-pill">${cfg.chapters.join(" · ")}</div>
      </header>
      <main class="workspace">
        <section class="stage" data-target="scene">
          <div class="photo">
            <img src="${cfg.image}" alt="${cfg.imageAlt || "Montage expérimental de chimie"}">
            <canvas id="sceneCanvas" aria-hidden="true"></canvas>
            <div class="photo-label"><span class="live-dot"></span><span id="sceneLabel">Montage prêt</span></div>
            <div class="instrument" data-target="instrument"><small id="instrumentLabel">Mesure principale</small><strong id="instrumentValue">—</strong><span id="instrumentUnit">Lancer un essai</span></div>
            <div class="status-note"><div class="status-icon">∿</div><p id="statusText">${cfg.intro}</p></div>
          </div>
          <div class="readouts" id="readouts"></div>
        </section>
        <aside class="control-panel" data-target="controls">
          <div class="panel-heading"><h2>Missions expérimentales</h2><span class="progress" id="progress">0 essai</span></div>
          <div class="mission-tabs" id="missionTabs" style="--mission-count:${cfg.missions.length}"></div>
          <div class="goal"><div class="number" id="missionNumber">01</div><div><strong id="missionTitle"></strong><p id="missionGoal"></p></div></div>
          <div><span class="predict-label">Je prédis avant de mesurer</span><div class="prediction-grid" id="predictions"></div></div>
          <span class="controls-title">Variables manipulables</span>
          <div class="controls" id="controls"></div>
          <div class="actions"><button class="run" id="runButton">▶ Lancer l’expérience</button><button class="reset" id="resetButton" title="Réinitialiser">↺</button></div>
        </aside>
        <section class="data-panel" data-target="graph">
          <div class="data-copy"><div class="data-head"><h2>Carnet de mesures</h2><span class="badge">IA lisible</span></div><div class="observation" id="observation"><strong>À vérifier :</strong> ${state.scientific_observation}</div><div class="verdict" id="verdict">Le résultat de ta prédiction apparaîtra ici.</div></div>
          <div class="chart-wrap"><canvas id="chartCanvas"></canvas><span class="axis-caption" id="axisCaption"></span></div>
        </section>
      </main>
    </div>`;

  function mission() { return cfg.missions[state.missionIndex]; }

  function initializeVariables() {
    state.variables = {};
    mission().parameters.forEach((p) => { state.variables[p.key] = p.value; });
    state.measurements = [];
    state.student_prediction = null;
    state.scientific_observation = "Choisis une prédiction, règle les paramètres puis lance l’essai.";
    state.status = "ready";
  }

  function buildMissionTabs() {
    $("#missionTabs").innerHTML = cfg.missions.map((m, i) => `
      <button class="mission-tab ${i === state.missionIndex ? "active" : ""}" data-mission="${m.id}" aria-label="Mission ${i + 1}: ${m.title}">
        <span class="ico">${m.icon}</span><span>${m.shortTitle || m.title}</span>
      </button>`).join("");
    $("#missionTabs").querySelectorAll("button").forEach((b) => b.addEventListener("click", () => selectVariant(b.dataset.mission)));
  }

  function buildMission() {
    const m = mission();
    $("#missionNumber").textContent = String(state.missionIndex + 1).padStart(2, "0");
    $("#missionTitle").textContent = m.title;
    $("#missionGoal").textContent = m.goal;
    $("#sceneLabel").textContent = m.sceneLabel || m.title;
    $("#predictions").innerHTML = m.predictions.map((p, i) => `<button class="prediction" data-prediction="${i}">${p}</button>`).join("");
    $("#predictions").querySelectorAll("button").forEach((b) => b.addEventListener("click", () => setPrediction(Number(b.dataset.prediction))));
    $("#controls").innerHTML = m.parameters.map(controlMarkup).join("");
    $("#controls").querySelectorAll("input,select").forEach((el) => el.addEventListener("input", onParameterInput));
    updateControlOutputs();
    updateDisplay();
  }

  function controlMarkup(p) {
    if (p.type === "select") {
      return `<label class="control"><span class="control-head"><span>${p.label}</span><output id="out-${p.key}"></output></span><select data-key="${p.key}">${p.options.map(o => `<option value="${o.value}" ${String(o.value) === String(p.value) ? "selected" : ""}>${o.label}</option>`).join("")}</select></label>`;
    }
    return `<label class="control"><span class="control-head"><span>${p.label}</span><output id="out-${p.key}"></output></span><input type="range" data-key="${p.key}" min="${p.min}" max="${p.max}" step="${p.step}" value="${p.value}"></label>`;
  }

  function displayParam(p, value) {
    if (p.type === "select") return p.options.find(o => String(o.value) === String(value))?.label || value;
    if (p.transform === "power10") return `10^${value} ${p.unit || ""}`;
    return `${fmt(Number(value), p.digits ?? 2)} ${p.unit || ""}`.trim();
  }

  function updateControlOutputs() {
    mission().parameters.forEach((p) => {
      const out = $("#out-" + p.key);
      if (out) out.textContent = displayParam(p, state.variables[p.key]);
    });
  }

  function onParameterInput(event) {
    const p = mission().parameters.find(x => x.key === event.target.dataset.key);
    state.variables[p.key] = p.type === "select" ? event.target.value : Number(event.target.value);
    updateControlOutputs();
    state.status = "adjusting";
    $("#statusText").textContent = "Paramètre modifié. Observe le montage puis relance pour mesurer son effet.";
    syncState();
  }

  function setPrediction(index) {
    state.student_prediction = index;
    $("#predictions").querySelectorAll("button").forEach((b, i) => b.classList.toggle("selected", i === index));
    $("#verdict").textContent = "Prédiction enregistrée. Lance maintenant l’expérience.";
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
    $(".photo").classList.add("running");
    $("#runButton").disabled = true;
    $("#runButton").textContent = "Mesure en cours…";
    const result = simulate(mission().model, state.variables);
    state.measurements = result.measurements;
    state.scientific_observation = result.observation;
    state.last_result = result;
    const started = performance.now();
    const animate = (now) => {
      state.animation = clamp((now - started) / 780, 0, 1);
      drawChart(result.series, result.axis, state.animation);
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
    $(".photo").classList.remove("running");
    $("#runButton").disabled = false;
    $("#runButton").textContent = "▶ Refaire une mesure";
    updateDisplay();
    const selected = state.student_prediction;
    const correct = selected !== null && selected === result.verdictIndex;
    $("#verdict").textContent = selected === null ? "Conseil : formule une prédiction avant le prochain essai." : correct ? "✓ Prédiction confirmée par les mesures." : "↻ Les mesures réfutent la prédiction : compare les valeurs et réessaie.";
    syncState();
  }

  function updateDisplay() {
    const result = state.last_result;
    const values = state.measurements.length ? state.measurements : [
      {label:"Mesure 1",value:"—",unit:""},{label:"Mesure 2",value:"—",unit:""},{label:"Mesure 3",value:"—",unit:""}
    ];
    $("#readouts").innerHTML = values.slice(0,3).map(x => `<div class="reading"><label>${x.label}</label><b>${x.value}</b><em>${x.unit || "mesure"}</em></div>`).join("");
    $("#observation").innerHTML = `<strong>${state.status === "completed" ? "Observation :" : "À vérifier :"}</strong> ${state.scientific_observation}`;
    $("#progress").textContent = `${state.runCount} essai${state.runCount === 1 ? "" : "s"}`;
    if (result) {
      $("#instrumentLabel").textContent = result.primary.label;
      $("#instrumentValue").textContent = result.primary.value;
      $("#instrumentUnit").textContent = result.primary.unit;
      $("#statusText").textContent = result.observation;
      $("#axisCaption").textContent = result.axis.x ? `${result.axis.x} →` : "mesure →";
      drawChart(result.series, result.axis, 1);
    } else {
      $("#instrumentLabel").textContent = "Mesure principale";
      $("#instrumentValue").textContent = "—";
      $("#instrumentUnit").textContent = "Lancer un essai";
      $("#statusText").textContent = cfg.intro;
      drawChart([], {}, 1);
    }
  }

  function resetSimulation() {
    initializeVariables();
    state.last_result = null;
    $("#runButton").disabled = false;
    $("#runButton").textContent = "▶ Lancer l’expérience";
    buildMission();
    $("#verdict").textContent = "Le résultat de ta prédiction apparaîtra ici.";
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
    $("#runButton").textContent = "▶ Lancer l’expérience";
    buildMissionTabs();
    buildMission();
    $("#verdict").textContent = "Nouvelle mission : commence par une prédiction.";
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
    if (refresh) syncState();
    return publicState();
  }

  function highlight(target) {
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

  function fitCanvas(canvas) {
    const rect = canvas.getBoundingClientRect(), dpr = Math.min(2, window.devicePixelRatio || 1);
    const w = Math.max(1, Math.round(rect.width*dpr)), h = Math.max(1, Math.round(rect.height*dpr));
    if (canvas.width !== w || canvas.height !== h) { canvas.width=w; canvas.height=h; }
    const ctx=canvas.getContext("2d"); ctx.setTransform(dpr,0,0,dpr,0,0); return {ctx,w:rect.width,h:rect.height};
  }

  function drawChart(series, axis, progress) {
    const canvas=$("#chartCanvas"); if(!canvas) return;
    const {ctx,w,h}=fitCanvas(canvas); ctx.clearRect(0,0,w,h);
    const pad={l:42,r:18,t:18,b:28}, cw=w-pad.l-pad.r, ch=h-pad.t-pad.b;
    ctx.strokeStyle="rgba(255,255,255,.08)"; ctx.lineWidth=1;
    for(let i=0;i<=4;i++){const y=pad.t+ch*i/4;ctx.beginPath();ctx.moveTo(pad.l,y);ctx.lineTo(w-pad.r,y);ctx.stroke();}
    if(!series.length){ctx.fillStyle="rgba(167,180,199,.65)";ctx.font="12px system-ui";ctx.textAlign="center";ctx.fillText("La courbe apparaîtra après la première mesure",w/2,h/2);return;}
    const visible=Math.max(2,Math.ceil(series.length*progress)), data=series.slice(0,visible);
    let minX=Math.min(...series.map(p=>p.x)), maxX=Math.max(...series.map(p=>p.x)), minY=Math.min(...series.map(p=>p.y)), maxY=Math.max(...series.map(p=>p.y));
    if(maxX===minX)maxX=minX+1;if(maxY===minY){maxY+=1;minY-=1;} const yMargin=(maxY-minY)*.08;minY-=yMargin;maxY+=yMargin;
    const X=x=>pad.l+(x-minX)/(maxX-minX)*cw, Y=y=>pad.t+ch-(y-minY)/(maxY-minY)*ch;
    const grad=ctx.createLinearGradient(0,pad.t,0,pad.t+ch);grad.addColorStop(0,`rgba(${cfg.accentRgb || "56, 189, 248"},.32)`);grad.addColorStop(1,`rgba(${cfg.accentRgb || "56, 189, 248"},0)`);
    ctx.beginPath();data.forEach((p,i)=>i?ctx.lineTo(X(p.x),Y(p.y)):ctx.moveTo(X(p.x),Y(p.y)));ctx.lineTo(X(data[data.length-1].x),pad.t+ch);ctx.lineTo(X(data[0].x),pad.t+ch);ctx.closePath();ctx.fillStyle=grad;ctx.fill();
    ctx.beginPath();data.forEach((p,i)=>i?ctx.lineTo(X(p.x),Y(p.y)):ctx.moveTo(X(p.x),Y(p.y)));ctx.strokeStyle=cfg.accent || "#38bdf8";ctx.lineWidth=3;ctx.lineJoin="round";ctx.stroke();
    const last=data[data.length-1];ctx.beginPath();ctx.arc(X(last.x),Y(last.y),5,0,Math.PI*2);ctx.fillStyle="#fff";ctx.fill();ctx.strokeStyle=cfg.accent;ctx.lineWidth=3;ctx.stroke();
    ctx.fillStyle="rgba(167,180,199,.9)";ctx.font="9px system-ui";ctx.textAlign="left";ctx.fillText(axis.y || "mesure",pad.l,10);ctx.fillText(fmt(minX,1),pad.l,h-8);ctx.textAlign="right";ctx.fillText(fmt(maxX,1),w-pad.r,h-8);ctx.textAlign="left";ctx.fillText(fmt(maxY,2),5,pad.t+4);ctx.fillText(fmt(minY,2),5,pad.t+ch);
  }

  let particles=[];
  function drawScene(time) {
    const canvas=$("#sceneCanvas");
    if(canvas){
      const {ctx,w,h}=fitCanvas(canvas), result=state.last_result, v=result?.visual || {kind:cfg.sceneKind || "kinetics",rate:.4,fraction:0};
      ctx.clearRect(0,0,w,h);
      const zone={x:w*.52,y:h*.18,w:w*.44,h:h*.56};
      if(particles.length!==72) particles=Array.from({length:72},(_,i)=>({x:((i*47)%97)/97,y:((i*61)%89)/89,s:.6+(i%5)/5,phase:i*.71}));
      if(v.kind==="kinetics"||v.kind==="equilibrium"||v.kind==="organic"){
        particles.forEach((q,i)=>{const speed=(v.rate||v.speed||.5);const x=zone.x+(((q.x+time*.00002*speed*q.s)%1)*zone.w),y=zone.y+(q.y+Math.sin(time*.001*speed+q.phase)*.025)*zone.h;const converted=v.fraction??v.ratio??v.yield??0;ctx.beginPath();ctx.arc(x,y,2.1+q.s,0,Math.PI*2);ctx.fillStyle=i/particles.length<converted?cfg.accent:"rgba(255,255,255,.62)";ctx.fill();});
      } else if(v.kind==="nuclear"){
        particles.forEach((q,i)=>{const x=zone.x+q.x*zone.w,y=zone.y+q.y*zone.h,alive=i/particles.length<(v.alive??1);ctx.beginPath();ctx.arc(x,y,alive?3:1.5,0,Math.PI*2);ctx.fillStyle=alive?cfg.accent:"rgba(251,113,133,.35)";ctx.fill();if(!alive&&i%7===0){ctx.strokeStyle="rgba(251,113,133,.35)";ctx.beginPath();ctx.moveTo(x-5,y);ctx.lineTo(x+5,y);ctx.moveTo(x,y-5);ctx.lineTo(x,y+5);ctx.stroke();}});
      } else if(v.kind==="electrochem"){
        for(let i=0;i<16;i++){const t=(time*.00018*(v.speed||1)+i/16)%1,x=zone.x+t*zone.w,y=zone.y+zone.h*.18+Math.sin(t*Math.PI)*-zone.h*.17;ctx.beginPath();ctx.arc(x,y,3,0,Math.PI*2);ctx.fillStyle=cfg.accent;ctx.fill();}
        for(let i=0;i<(v.bubbles||0);i++){const x=zone.x+zone.w*(.35+(i%6)*.08),y=zone.y+zone.h*(.9-((time*.0001+i*.11)%1)*.65);ctx.beginPath();ctx.arc(x,y,2+i%3,0,Math.PI*2);ctx.strokeStyle="rgba(255,255,255,.55)";ctx.stroke();}
      }
    }
    requestAnimationFrame(drawScene);
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
    if (data.guidance_text) $("#statusText").textContent = data.guidance_text;
    const result=executeAICommand(data.payload || data.command || data, data.parameters || {});
    event.source?.postMessage?.({type:"simulation_control_result",requestId:data.requestId,simulation_id:cfg.id,simulationId:cfg.id,result},"*");
  });
  window.addEventListener("resize",()=>{if(state.last_result)drawChart(state.last_result.series,state.last_result.axis,1);});
  $("#runButton").addEventListener("click",()=>runTrial());
  $("#resetButton").addEventListener("click",resetSimulation);
  initializeVariables();
  buildMissionTabs();
  buildMission();
  syncState();
  if(window.parent!==window) window.parent.postMessage({
    type:"simulation_manifest",
    simulation_id:cfg.id,
    simulationId:cfg.id,
    capabilities:{
      commands:window.SIMULATION_CONFIG.commands,
      globals:["executeAICommand","getSimulationState","runTrial","resetSimulation","selectVariant"],
      buttons:cfg.missions.map(m=>({id:m.id,text:m.title,className:"mission-tab"})),
      config:window.SIMULATION_CONFIG
    },
    page_text:`${cfg.title}. ${cfg.intro}`,
    manifest:window.SIMULATION_CONFIG
  },"*");
  requestAnimationFrame(drawScene);
})();
