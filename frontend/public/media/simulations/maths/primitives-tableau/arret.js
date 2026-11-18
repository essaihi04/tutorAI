/*
 * S’arrêter avant la réponse : `?arret=<moment>` (18 novembre 2026, rejeu après la réponse du cours math_ch4_primitives,
 * format `concentration.apres_reponse` de la skill cours-concentration).
 *
 * Une diapositive qui pose une question sur une construction complète (calculs.html?vue=x2, variations.html?vue=complet…)
 * ne doit pas l’écrire en entier avant la réponse de l’élève : la construction ne court que jusqu’à `arret` (au
 * chargement, au `start` et au `reset` du tuteur) ; les moments d’après restent là pour le rejeu (`play_until`) que le
 * lecteur envoie une fois la réponse donnée. Remplace les vues coupées d’etapes.html pour ces diapositives.
 * Sans `arret` dans l’URL, rien ne change (vues du cours en ligne inchangées). À charger après MathsTableau.page(…).
 */
(function () {
  'use strict';
  const arret = new URLSearchParams(location.search).get('arret');
  if (!arret || !window.__maths || typeof window.executeAICommand !== 'function') return;
  const exec = window.executeAICommand;
  const jusqua = () => exec('play_until', { moment: arret });
  window.executeAICommand = (cmd, p) => {
    if (cmd === 'start' || cmd === 'reset') { exec(cmd, p); jusqua(); return; }
    return exec(cmd, p);
  };
  jusqua();
})();
