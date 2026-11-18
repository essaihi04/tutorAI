/*
 * Fractions ⟦num|dén⟧ ET exposants dans la même phrase (18 novembre 2026, 2ᵉ passe du cours
 * math_ch2_derivation_etude_fonctions — règle 12 des simulations au tableau).
 * exposants.js (commun, lecture seule) remplace Craie.texte dès qu’une phrase contient « ² », « ³ » ou « ^ » et
 * n’écrit pas les fractions : « f′(x) = ⟦g(x)|x²⟧ » sortait avec les crochets. Ici, une phrase qui contient « ⟦ »
 * passe d’abord par l’écriture des fractions du kit ; chaque morceau (numérateur, dénominateur, texte) repasse par
 * Craie.texte, donc ses exposants sont écrits comme avant. Sans « ⟦ » rien ne change (aucune vue du cours en ligne
 * n’en contient). À charger après exposants.js.
 */
(function () {
  'use strict';
  const T = window.Tableau; if (!T) return;
  const P = T.Craie.prototype; if (P.__fractionsExposants) return;
  P.__fractionsExposants = true;
  const texte = P.texte;
  P.texte = function (s, x, y, o = {}) {
    s = String(s);
    if (s.includes('⟦') && typeof this._texteFractions === 'function') return this._texteFractions(s, x, y, o);
    return texte.call(this, s, x, y, o);
  };
})();
