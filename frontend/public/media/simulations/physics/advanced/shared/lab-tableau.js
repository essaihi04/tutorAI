/*
 * Moteur commun des laboratoires avancés de physique dessinés au tableau.
 * Chaque page définit `window.LAB` (données, paramètres, modèle, dessins) puis charge ce script.
 *
 * LAB = {
 *   id, eyebrow, DATA: { variant: { label, kicker, title, instruction, goal } }, params, paramMap,
 *   command_schema, state_schema, page_text, globals,
 *   controls(variant, p) → [{ type:'range', key, label, min, max, step, unit, decimales } | { type:'choice', key, label, options:[[valeur, libellé]…] }],
 *   values() → grandeurs dérivées, check(mesures, variant) → { correct, errors },
 *   hints: { variant: [3 indices] }, aliases: { cible: zone },
 *   onVariant(variant) (facultatif), runLabel(variant) (facultatif),
 *   draw(craie, api) : api = { variant, p, d, t (s depuis l'ouverture), zone(nom, x, y, w, h), lignes(x, y, [texte…], o) }
 * }
 * Commandes : start, set_variant, set_parameters, run_model, record_measurement, check, reset, reveal_hint, highlight.
 */
(function () {
  'use strict';
  const LAB = window.LAB; if (!LAB) throw new Error('LAB manquant');
  const { Craie, fr, bulle, ecrire, onglets, curseur, protocole } = window.Tableau;
  const $ = id => document.getElementById(id);
  const DATA = LAB.DATA, ids = Object.keys(DATA), total = ids.length;
  const query = new URLSearchParams(location.search), requested = query.get('variant');
  const S = { variant: DATA[requested] ? requested : ids[0], status: 'idle', completed: [], attempts: 0, hints: 0, measurements: Object.fromEntries(ids.map(k => [k, []])),
    params: { ...LAB.params }, ouvert: performance.now(), marques: { resultat: null, hl: null }, hl: null, ran: false, dirty: true };
  const commands = ['start', 'set_variant', 'set_parameters', 'run_model', 'record_measurement', 'check', 'reset', 'reveal_hint', 'highlight', ...(LAB.commandsExtra || [])];
  const alias = LAB.commandAliases || {};
  const config = { id: LAB.id, version: '3.0', title: LAB.title, variants: ids.map(id => ({ id, label: DATA[id].label, objective: DATA[id].goal })), commands, command_schema: LAB.command_schema, state_schema: LAB.state_schema };

  document.body.innerHTML = `
<div class="tableau">
  <header class="titre"><div><small>${LAB.eyebrow}</small><h1 id="title"></h1><p class="objectif" id="instruction"></p></div><nav class="onglets" id="onglets" aria-label="Expériences"></nav></header>
  <section class="scene">
    <canvas id="canvas" role="img" aria-label="${LAB.title} dessiné à la craie"></canvas>
    <div class="panneau bas-gauche reglages" id="settings" data-professor-control="set_parameters"><div id="controls"></div></div>
    <div class="panneau haut-droite mesures" id="measures"><h3 id="kicker"></h3><table class="lecture-table" id="table"></table><div class="rangee"><button class="craie-btn" id="record" data-professor-control="record_measurement" disabled>Noter l’essai</button><button class="craie-btn attention" id="check" data-professor-control="check">Vérifier</button></div></div>
  </section>
  <footer class="barre">
    <button class="craie-btn principal" id="run" data-professor-control="start run_model">Lancer</button>
    <button class="craie-btn secondaire" id="reset" data-professor-control="reset">Recommencer</button>
    <p class="bulle" id="feedback" role="status" aria-live="polite"></p>
    <button class="craie-btn secondaire" id="hint" data-professor-control="reveal_hint">Un indice</button>
    <span class="lecture" id="progress"></span>
  </footer>
</div>`;

  const scene = () => (performance.now() - S.ouvert) / 1000;
  const redraw = () => { S.dirty = true; };
  const values = () => LAB.values(S.variant, S.params);
  const snap = (extra = {}) => ({ simulation_status: S.status, current_variant: S.variant, skill: DATA[S.variant].goal, parameters: { ...S.params }, derived_values: values(), measurements: [...S.measurements[S.variant]], attempts: S.attempts, hints_used: S.hints, completed_variants: [...S.completed], expected_answer: DATA[S.variant].goal, ...extra });
  const pont = protocole({ id: LAB.id, commandes: commands, config, texte: LAB.page_text, etat: snap, progression: () => S.completed.length / total, executer });
  const act = (a, d = {}) => pont.noter(a, { ...d, variant: S.variant });
  const emit = (extra) => { pont.emettre(extra); $('progress').textContent = `${S.completed.length} / ${total}`; };
  const feedback = (t, kind = '') => bulle($('feedback'), t, kind);

  // ── Réglages à la craie ──────────────────────────────────────────────────
  function renderControls() {
    const box = $('controls'); box.replaceChildren();
    for (const c of LAB.controls(S.variant, S.params)) {
      if (c.type === 'range') {
        box.append(curseur({ id: c.key, label: c.label, min: c.min, max: c.max, step: c.step, valeur: c.get ? c.get(S.params) : S.params[c.key], unite: c.unit, decimales: c.decimales,
          onchange: v => { if (c.set) c.set(S.params, v); else S.params[c.key] = v; if (c.after) c.after(S.params); act('set_parameter', { parameter: c.key, value: v }); S.ran = false; renderControls(); redraw(); emit({ last_manipulation: { parameter: c.key, value: v } }); } }));
      } else if (c.type === 'choice') {
        const w = document.createElement('div'); w.className = 'choix-ligne'; w.id = 'choix-' + c.key;
        if (c.label) { const l = document.createElement('span'); l.className = 'legende'; l.textContent = c.label + ' :'; w.append(l); }
        for (const [v, label] of c.options) {
          const b = document.createElement('button'); b.type = 'button'; b.className = 'onglet'; b.dataset.variant = String(v); b.textContent = label; b.setAttribute('aria-pressed', String(String(S.params[c.key]) === String(v)));
          b.onclick = () => { S.params[c.key] = typeof S.params[c.key] === 'number' ? +v : v; if (c.after) c.after(S.params); act(c.action || 'set_parameter', { parameter: c.key, value: S.params[c.key] }); S.ran = false; renderControls(); redraw(); emit(); };
          w.append(b);
        }
        box.append(w);
      }
    }
    $('settings').hidden = !box.children.length;
  }
  function renderTable() {
    const m = S.measurements[S.variant], cols = LAB.columns ? LAB.columns(S.variant) : [];
    $('table').innerHTML = m.length && cols.length
      ? `<tr><th>#</th>${cols.map(c => `<th>${c.label}</th>`).join('')}</tr>` + m.slice(-4).map(x => `<tr><td>${x.index}</td>${cols.map(c => `<td>${c.get(x)}</td>`).join('')}</tr>`).join('')
      : `<tr><td class="legende">${m.length ? m.length + ' essai(s) noté(s)' : 'aucun essai noté'}</td></tr>`;
  }
  function setVariant(id) {
    if (!DATA[id]) return;
    S.variant = id; S.status = 'running'; S.attempts = 0; S.ran = false; S.hl = null; S.marques = { resultat: null, hl: null }; S.ouvert = performance.now();
    if (LAB.onVariant && LAB.onVariant(id, S.params) === false) return;
    const d = DATA[id]; act('set_variant', { variant_id: id });
    onglets($('onglets'), config.variants, id, setVariant, new Set(S.completed));
    ecrire($('title'), d.title); ecrire($('instruction'), d.instruction, { vitesse: 60 }); ecrire($('kicker'), d.kicker);
    $('run').textContent = LAB.runLabel ? LAB.runLabel(id) : 'Lancer'; $('record').disabled = true;
    renderControls(); renderTable(); feedback(d.goal); redraw(); emit();
  }
  function setParameters(p) {
    Object.entries(p || {}).forEach(([k, v]) => { const key = (LAB.paramMap || {})[k] || k; if (LAB.setParam && LAB.setParam(S.params, key, v)) return; if (key in S.params) S.params[key] = typeof S.params[key] === 'number' ? +v : v; });
    if (LAB.afterParams) LAB.afterParams(S.params, S.variant);
    act('set_parameters', { ...p }); S.ran = false; renderControls(); redraw(); emit({ last_manipulation: { type: 'set_parameters', ...p } });
  }
  function runModel() {
    S.status = 'running'; S.ran = true; S.marques.resultat = scene(); $('record').disabled = false;
    act('run_model', { parameters: { ...S.params }, result: values() });
    feedback(LAB.runFeedback ? LAB.runFeedback(S.variant, values()) : 'Résultat écrit au tableau : note l’essai pour comparer.', 'good');
    redraw(); emit({ last_manipulation: { type: 'run_model', result: values() } });
  }
  function recordMeasurement() {
    if (!S.ran) runModel();
    const item = { ...values(), parameters: { ...S.params }, index: S.measurements[S.variant].length + 1 };
    S.measurements[S.variant].push(item); act('record_measurement', item); renderTable();
    feedback(`Essai ${item.index} noté. Change un réglage, relance et compare.`, 'good'); emit({ last_measurement: item });
  }
  function checkExperiment() {
    S.attempts++; const m = S.measurements[S.variant]; const { correct, errors } = LAB.check(S.variant, m);
    act('check_experiment', { correct, errors });
    if (!correct) { feedback('À compléter : ' + errors.join(' · '), 'bad'); emit({ correct: false, errors }); return; }
    if (!S.completed.includes(S.variant)) S.completed.push(S.variant);
    S.status = 'finished'; onglets($('onglets'), config.variants, S.variant, setVariant, new Set(S.completed));
    feedback('✓ Compétence validée : les essais justifient la loi. Explique-la au tuteur.', 'good'); emit({ correct: true, validated_measurements: m });
  }
  function revealHint(level = ++S.hints) {
    const h = LAB.hints[S.variant], t = h[Math.min(level - 1, h.length - 1)]; S.hints = Math.max(S.hints, level);
    act('request_hint', { level }); feedback('💡 ' + t); emit({ last_hint: t });
  }
  function highlight(target) {
    const zone = (LAB.aliases || {})[target] || target; S.hl = { target: zone, at: scene() };
    act('highlight', { target }); feedback('Regarde : ' + (LAB.labels?.[zone] || target)); redraw(); emit({ last_highlight: target });
  }
  function reset() { S.measurements[S.variant] = []; S.attempts = 0; act('reset'); setVariant(S.variant); }
  function executer(c, p) {
    c = alias[c] || c;
    if (c === 'start') { S.status = 'running'; if (!S.ran) runModel(); }
    else if (c === 'set_variant') setVariant(p.variant_id);
    else if (c === 'set_parameters') setParameters(p);
    else if (c === 'run_model') runModel();
    else if (c === 'record_measurement') recordMeasurement();
    else if (c === 'check') checkExperiment();
    else if (c === 'reset') reset();
    else if (c === 'reveal_hint') revealHint(+p.level || 1);
    else if (c === 'highlight') highlight(p.target);
    emit();
  }

  // ── Dessin ───────────────────────────────────────────────────────────────
  const canvas = $('canvas'), craie = new Craie(canvas, { onresize: redraw }), zones = {};
  function draw() {
    const W = craie.W, H = craie.H; if (W < 1 || H < 1) return true;
    const t = scene(); craie.debut(LAB.seed || 11, t);
    const c = craie.ctx, s = Math.min(W / 760, H / 380); c.translate((W - 760 * s) / 2, (H - 380 * s) / 2); c.scale(s, s);
    for (const k in zones) delete zones[k];
    const api = { variant: S.variant, p: S.params, d: values(), t, ran: S.ran, resultat: S.marques.resultat, S,
      zone: (nom, x, y, w, h) => { zones[nom] = [x, y, w, h]; },
      lignes: (x, y, textes, o = {}) => { textes.forEach((tx, i) => craie.texte(tx, x, y + i * (o.pas ?? 22), { couleur: o.couleur ?? 'jaune', taille: o.taille ?? 16, max: o.max })); } };
    LAB.draw(craie, api);
    if (S.hl && zones[S.hl.target]) {
      const [x, y, w, h] = zones[S.hl.target]; craie.depuis(S.hl.at);
      craie.rect(x - 8, y - 8, w + 16, h + 16, { couleur: 'orange', largeur: 2, arrondi: 12, pointille: [6, 5] });
      craie.texte('ici', x + w + 14, y + 4, { couleur: 'orange', taille: 15 });
    }
    return craie.fin();
  }
  function frame() { if (S.dirty) S.dirty = !draw(); requestAnimationFrame(frame); }

  $('onglets').addEventListener('click', e => { const b = e.target.closest('[data-variant]'); if (b) setVariant(b.dataset.variant); });
  $('run').onclick = runModel; $('record').onclick = recordMeasurement; $('check').onclick = checkExperiment; $('reset').onclick = reset; $('hint').onclick = () => revealHint();
  Object.assign(window, { setVariant, setParameters, runModel, recordMeasurement, checkExperiment });
  setVariant(S.variant); requestAnimationFrame(frame);
})();
