/*
 * Schéma à légender (cours « Rôle du muscle strié squelettique », 15 novembre 2026), comme au bac : des étiquettes
 * à glisser sur le schéma ; bien posée (près de sa place), une étiquette s'aimante et devient verte. Même contrat que
 * svt/relation_gene_proteine-tableau/schema_bilan.html (vue construire) : la page expose en lecture seule
 * legende_total, legende_places, legende_erreurs (étiquettes lâchées sur le schéma loin de leur place),
 * legende_mal (leurs noms) ; le réglage `corrige` amène toutes les étiquettes à leur place.
 *
 *   const E = window.Etiquettes({ noms: {id: 'texte'}, ordre: [ids], place: id => [x, y], colonne: i => [x, y],
 *                                 limite: () => x (à gauche : le schéma ; à droite : la colonne des étiquettes) });
 *   E.remise() ; E.noter(P) ; E.cadres(c) ; E.dessiner(c, { t, corrige, tCorr }) ; E.toucher(x, y) ; E.bouger(id, x, y) ;
 *   E.lacher(id) → true si bien posée ; E.places() ; E.voit({ t, corrige, tCorr }) → phrases.
 * Une étiquette est soit dans la colonne, soit à sa place (ok), soit lâchée ailleurs (x, y libres) : la colonne et
 * les places suivent la disposition (largeur du tableau), seules les étiquettes lâchées ailleurs gardent leurs coordonnées.
 */
(function () {
  'use strict';
  const lisse = x => (x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x));
  window.Etiquettes = function ({ noms, ordre, place, colonne, limite, rayon = 40, taille = 16 }) {
    let ET = {}, ERREURS = 0, MAL = new Set();
    const larg = {};                                  // largeurs dessinées (la craie agrandit le texte sur petit écran)
    const largeur = id => larg[id] || 18 + 8.4 * noms[id].length;
    function remise() { ET = {}; ERREURS = 0; MAL = new Set(); ordre.forEach(id => { ET[id] = { etat: 'col' }; }); }
    remise();
    const pos = id => { const e = ET[id]; return e.etat === 'ok' ? place(id) : e.etat === 'col' ? colonne(ordre.indexOf(id)) : [e.x, e.y]; };
    const places = () => ordre.filter(id => ET[id].etat === 'ok').length;
    function noter(P) {
      P.legende_total = ordre.length; P.legende_places = places(); P.legende_erreurs = ERREURS; P.legende_mal = [...MAL].join(', ');
      return P;
    }
    /** Positions affichées : la correction amène chaque étiquette à sa place, l'une après l'autre. */
    function affichees({ t = 0, corrige = false, tCorr = 0 } = {}) {
      const out = {};
      ordre.forEach((id, i) => {
        const [x, y] = pos(id), ok = ET[id].etat === 'ok';
        if (corrige && t >= tCorr) {
          const u = lisse((t - tCorr - .15 * i) / 1.0), [sx, sy] = place(id);
          out[id] = { x: x + (sx - x) * u, y: y + (sy - y) * u, ok: ok || u >= 1 };
        } else out[id] = { x, y, ok };
      });
      return out;
    }
    /** Les cases vides (pointillés) au bout des traits de rappel : là où vont les étiquettes. */
    function cadres(c) {
      const t = Math.max(taille, (c.tailleMin || 0) / (c.echelle || 1));
      for (const id of ordre) {
        const [x, y] = place(id), w = Math.max(54, c.largeurTexte(noms[id], t) * .55 + 24), h = t + 12;
        c.rect(x - w / 2, y - h / 2, w, h, { couleur: 'faible', largeur: 1.2, pointille: [4, 4], fond: '#0f172a', fondAlpha: .85, arrondi: 6, tremble: .2, duree: .2 });
      }
    }
    function dessiner(c, etat) {
      const P = affichees(etat), t = Math.max(taille, (c.tailleMin || 0) / (c.echelle || 1));
      c.direct(() => ordre.forEach(id => {
        const p = P[id], w = c.largeurTexte(noms[id], t) + 18, h = t + 12, coul = p.ok ? 'vert' : 'blanc';
        larg[id] = w;
        c.rect(p.x - w / 2, p.y - h / 2, w, h, { couleur: coul, largeur: 1.6, fond: p.ok ? '#14532d' : '#1e293b', fondAlpha: .9, arrondi: 6 });
        c.texte(noms[id], p.x, p.y + t * .36, { couleur: coul, taille, align: 'center' });
      }));
      return P;
    }
    function toucher(x, y) {
      for (let i = ordre.length - 1; i >= 0; i--) {
        const id = ordre[i], [ex, ey] = pos(id);
        if (Math.abs(x - ex) <= largeur(id) / 2 + 4 && Math.abs(y - ey) <= taille + 2) return id;
      }
      return null;
    }
    function bouger(id, x, y, bornes) {
      const [x0, y0, x1, y1] = bornes || [10, 30, 2000, 410];
      ET[id] = { etat: 'libre', x: Math.min(x1, Math.max(x0, x)), y: Math.min(y1, Math.max(y0, y)) };
    }
    /** Lâchée : près de sa place → aimantée ; dans la colonne → y retourne ; sur le schéma, loin → une erreur. */
    function lacher(id) {
      const e = ET[id]; if (e.etat !== 'libre') return e.etat === 'ok';
      const [sx, sy] = place(id);
      if (Math.hypot(e.x - sx, e.y - sy) <= rayon) { ET[id] = { etat: 'ok' }; return true; }
      if (e.x >= limite()) { ET[id] = { etat: 'col' }; return false; }
      ERREURS += 1; MAL.add(noms[id]);
      return false;
    }
    /** Le plus proche des emplacements (pour dire où l'élève a posé une étiquette). */
    function procheDe(x, y) { let best = null, d = 1e9; for (const s of ordre) { const [sx, sy] = place(s), dd = Math.hypot(x - sx, y - sy); if (dd < d) { d = dd; best = s; } } return best; }
    function voit(etat) {
      const P = affichees(etat), col = [], bien = [], ailleurs = [], m = [];
      ordre.forEach(id => {
        const p = P[id];
        if (p.ok) bien.push(`« ${noms[id]} »`);
        else if (ET[id].etat === 'col' && !(etat && etat.corrige && etat.t >= etat.tCorr)) col.push(`« ${noms[id]} »`);
        else ailleurs.push(`« ${noms[id]} » (posée près de la case de « ${noms[procheDe(p.x, p.y)]} »)`);
      });
      if (col.length) m.push(`Dans la colonne de droite, étiquettes à poser : ${col.join(', ')}.`);
      if (bien.length) m.push(`Bien posées (vertes, aimantées) : ${bien.join(', ')}.`);
      if (ailleurs.length) m.push(`Mal posées (blanches) : ${ailleurs.join(', ')}.`);
      m.push(`Bien posées : ${ordre.filter(id => P[id].ok).length} sur ${ordre.length}.`);
      return m;
    }
    return { remise, noter, cadres, dessiner, toucher, bouger, lacher, places, affichees, voit, get erreurs() { return ERREURS; } };
  };
})();
