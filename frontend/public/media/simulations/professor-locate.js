/*
 * Localisation des boutons d'un laboratoire pour le professeur animé de la page.
 *
 * La page parente envoie `simulation_locate` ({command, parameters, sequence}) ; ce script répond
 * `simulation_control_rect` avec le rectangle (px de l'iframe) de l'élément que la commande actionne,
 * ou `null`. Le professeur vole alors jusqu'à ce bouton et l'appuie avant que la commande ne parte.
 *
 * Priorité : un élément marqué `data-professor-control="cmd1 cmd2"`, puis une variante dont l'identifiant
 * est celui d'un bouton ou d'une option, puis les identifiants habituels des laboratoires, puis le texte
 * des boutons, puis le premier curseur pour `set_parameters`.
 *
 * Pointage (`highlight`, `point`, `montrer` avec `parameters.target`) : le professeur ne presse rien, il vole
 * dans la simulation et montre le repère du doigt. Le repère vient du kit tableau (`Tableau.rectRepere`,
 * dessiné à la craie), d'un élément `data-professor-point="id"` / `data-repere="id"`, ou `#hot-id`. La réponse
 * porte alors `mode: 'point'`.
 */
(function () {
  if (window.__PROFESSOR_LOCATE__) return;
  window.__PROFESSOR_LOCATE__ = true;
  var IDS = {
    start: ['run', 'start', 'startBtn', 'startButton', 'btnStart', 'play'],
    fire_pulse: ['run'], run_trial: ['run'], run_model: ['run'], replay: ['run'],
    pause: ['pause', 'pauseBtn', 'pauseButton', 'btnPause'],
    step: ['step'], next: ['next', 'nextBtn', 'nextButton'], previous: ['previous', 'prev', 'prevBtn'],
    reset: ['reset', 'resetBtn', 'restartButton', 'btnReset', 'restart'],
    check: ['check', 'checkBtn', 'verify'],
    reveal_hint: ['hint', 'hintBtn', 'help'],
    record_measurement: ['record', 'recordBtn', 'recordPt'], record_pt: ['recordPt'],
    run_deformation_test: ['runDeformation'],
  };
  var WORDS = {
    start: /lancer|d[ée]marrer|simuler|animer|observer|stimuler|acqu[ée]rir|start|play/i,
    fire_pulse: /lancer/i, run_trial: /lancer|stimuler|mod[ée]lisation/i, run_model: /simuler|lancer/i, replay: /relancer|rejouer/i,
    pause: /pause/i, step: /pas\b/i, next: /suivant/i, previous: /pr[ée]c[ée]dent/i,
    reset: /r[ée]init|recommencer|relancer|reset|annuler tout/i,
    check: /v[ée]rifier/i, reveal_hint: /indice|aide|\?/i, record_measurement: /enregistrer/i,
  };
  function visible(el) {
    if (!(el instanceof Element)) return null;
    var r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0 ? { x: r.left, y: r.top, width: r.width, height: r.height } : null;
  }
  var POINTAGE = ['highlight', 'point', 'montrer', 'show'];
  function cible(parameters) {
    return parameters && (parameters.target || parameters.repere || parameters.element || parameters.id || parameters.variant_id);
  }
  /** Repère à montrer du doigt : rectangle (px de l'iframe) ou null. */
  function repere(command, parameters) {
    var cmd = String(command || '').replace(/[^a-z_]/g, '');
    if (POINTAGE.indexOf(cmd) < 0) return null;
    var id = String(cible(parameters) || '').replace(/[^\w-]/g, '');
    if (!id) return null;
    if (window.Tableau && typeof window.Tableau.rectRepere === 'function') {
      var r = window.Tableau.rectRepere(id);
      if (r && r.width > 0) return r;
    }
    var el = document.querySelector('[data-professor-point~="' + id + '"], [data-repere="' + id + '"]') || document.getElementById('hot-' + id);
    return visible(el);
  }
  function find(command, parameters) {
    var cmd = String(command || '').replace(/[^a-z_]/g, '');
    if (!cmd) return null;
    var marked = document.querySelector('[data-professor-control~="' + cmd + '"]');
    if (visible(marked)) return marked;
    var variant = parameters && (parameters.variant_id || parameters.variant);
    if ((cmd === 'set_variant' || cmd === 'highlight') && variant) {
      var byId = document.getElementById(String(variant));
      if (visible(byId)) return byId;
      var option = document.querySelector('option[value="' + String(variant).replace(/"/g, '') + '"]');
      if (option && option.closest('select') && visible(option.closest('select'))) return option.closest('select');
      var byData = document.querySelector('[data-variant="' + String(variant).replace(/"/g, '') + '"]');
      if (visible(byData)) return byData;
    }
    if (cmd === 'set_variant' || cmd === 'highlight') {
      var select = document.querySelector('select');
      if (visible(select)) return select;
    }
    var ids = IDS[cmd] || [];
    for (var i = 0; i < ids.length; i++) {
      var el = document.getElementById(ids[i]);
      if (visible(el)) return el;
    }
    var words = WORDS[cmd];
    if (words) {
      var buttons = document.querySelectorAll('button');
      for (var j = 0; j < buttons.length; j++) {
        if (words.test((buttons[j].textContent || '').trim()) && visible(buttons[j])) return buttons[j];
      }
    }
    if (cmd === 'set_parameters' || cmd === 'set_deformation_parameters' || cmd === 'set_pt' || cmd === 'set_speed') {
      var keys = parameters ? Object.keys(parameters) : [];
      for (var k = 0; k < keys.length; k++) {
        var input = document.querySelector('[name="' + keys[k] + '"], #' + keys[k].replace(/[^\w-]/g, ''));
        if (visible(input)) return input.closest('label') || input;
      }
      var range = document.querySelector('input[type="range"]');
      if (visible(range)) return range.closest('label, fieldset, section, div') || range;
    }
    return null;
  }
  window.addEventListener('message', function (event) {
    if (event.source !== window.parent) return;
    var data = event.data;
    if (!data || data.type !== 'simulation_locate') return;
    var pointe = repere(data.command, data.parameters);
    var el = pointe ? null : find(data.command, data.parameters);
    window.parent.postMessage({
      type: 'simulation_control_rect',
      sequence: data.sequence,
      command: data.command,
      rect: pointe || visible(el),
      mode: pointe ? 'point' : 'press',
    }, '*');
  });
})();
