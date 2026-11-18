/*
 * Ouvrir une construction figée sur un moment : `?depart=<moment>` (18 novembre 2026, 2ᵉ passe du cours
 * math_ch2_derivation_etude_fonctions — professeur règle 39, « chaque diapositive ouvre sur son propre état »).
 *
 * Le kit des maths (maths-tableau.js, lecture seule) n’a pas de `depart` : une page rechargée réécrit tout depuis le
 * début. Ici, une diapositive qui continue l’étude de la précédente (même vue, URL distincte avec `depart`) s’ouvre
 * avec tout ce qui était déjà au tableau, figé sur ce moment ; ses `play_until` continuent à partir de là.
 *   - au chargement : set_time sur l’instant du moment (la scène est « en pause » sur lui) ;
 *   - `reset` (demarrer de la diapositive, « Réécouter ») : la scène revient figée sur ce moment, pas à zéro.
 * Le bouton « Réécrire » de l’élève (start) recommence toute la construction, comme avant.
 * Sans `depart` dans l’URL, rien ne change (pages et vues du cours en ligne inchangées).
 * À charger après MathsTableau.page(…).
 */
(function () {
  'use strict';
  const dep = new URLSearchParams(location.search).get('depart');
  if (!dep || !window.__maths || typeof window.executeAICommand !== 'function') return;
  const exec = window.executeAICommand;
  function figer() {
    exec('set_time', { time_s: 1e6 });             // la construction calculée en entier : les moments sont connus
    const t = window.__maths.M[dep];
    exec('set_time', { time_s: Number.isFinite(t) ? t : 0 });
  }
  window.executeAICommand = (cmd, p) => {
    if (cmd === 'reset') { exec('reset', p); figer(); return; }
    return exec(cmd, p);
  };
  figer();
})();
