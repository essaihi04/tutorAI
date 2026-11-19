/*
 * Outils des feuilles d'examen SVT du cours « Expression de l'information génétique » (19 novembre 2026, professeur
 * règle 46) : les tableaux et figures des sujets nationaux redessinés en code pour le gabarit commun
 * /media/simulations/shared/examen/feuille.js (fond blanc, texte noir). Chargé AVANT la config window.FEUILLE.
 *   FeuilleSVT.code()                    le tableau du code génétique complet (1re lettre / 2e lettre / 3e lettre),
 *                                        comme le document des sujets 2024 N et 2025 N
 *   FeuilleSVT.sequences(lignes, o)      un tableau de séquences : [[intitulé, [cases…]], …]
 *   FeuilleSVT.svg(w, h, corps, label)   un SVG noir sur blanc, police du sujet
 */
(function () {
  'use strict';
  const B = 'UCAG';
  const AA = {
    UU: ['Phe', 'Phe', 'Leu', 'Leu'], UC: ['Ser', 'Ser', 'Ser', 'Ser'], UA: ['Tyr', 'Tyr', 'STOP', 'STOP'], UG: ['Cys', 'Cys', 'STOP', 'Trp'],
    CU: ['Leu', 'Leu', 'Leu', 'Leu'], CC: ['Pro', 'Pro', 'Pro', 'Pro'], CA: ['His', 'His', 'Gln', 'Gln'], CG: ['Arg', 'Arg', 'Arg', 'Arg'],
    AU: ['Ile', 'Ile', 'Ile', 'Met'], AC: ['Thr', 'Thr', 'Thr', 'Thr'], AA: ['Asn', 'Asn', 'Lys', 'Lys'], AG: ['Ser', 'Ser', 'Arg', 'Arg'],
    GU: ['Val', 'Val', 'Val', 'Val'], GC: ['Ala', 'Ala', 'Ala', 'Ala'], GA: ['Ac.asp', 'Ac.asp', 'Ac.glu', 'Ac.glu'], GG: ['Gly', 'Gly', 'Gly', 'Gly'],
  };
  const CSS = `<style>
    table.code{border-collapse:collapse;margin:.3em auto;font-size:1em;line-height:1.12}
    table.code td,table.code th{border:1px solid #000;padding:0 .3em;text-align:center}
    table.code th{background:#e8e8e8;font-weight:700}
    table.code td.l1{background:#e8e8e8;font-weight:700}
    table.code td.l3{font-weight:700}
    table.seq{border-collapse:collapse;margin:.3em auto}
    table.seq td{border:1px solid #000;padding:.15em .6em;text-align:center;font-weight:700;white-space:nowrap}
    table.seq td.nom{text-align:left}
    table.seq td.n{font-weight:400}
  </style>`;
  function code() {
    let h = CSS + '<table class="code"><tr><th>1<sup>ère</sup> lettre \\ 2<sup>ème</sup> lettre</th>' +
      [...B].map((b) => `<th colspan="2">${b}</th>`).join('') + '<th>3<sup>ème</sup> lettre</th></tr>';
    for (const p of B) {
      for (let k = 0; k < 4; k++) {
        h += '<tr>' + (k === 0 ? `<td class="l1" rowspan="4">${p}</td>` : '');
        for (const s of B) {
          const L = AA[p + s];
          h += `<td>${p}${s}${B[k]}</td>`;
          if (k === 0 || L[k] !== L[k - 1]) { let n = 1; while (k + n < 4 && L[k + n] === L[k]) n++; h += `<td rowspan="${n}"><b>${L[k]}</b></td>`; }
        }
        h += `<td class="l3">${B[k]}</td></tr>`;
      }
    }
    return h + '</table>';
  }
  /** lignes : [[intitulé, [cases]]] ; o.ids : ids de cellules {`ligne,colonne`: id} pour les données pointables. */
  function sequences(lignes, o = {}) {
    return CSS + '<table class="seq">' + lignes.map(([nom, cases], i) => `<tr><td class="nom">${nom}</td>` +
      cases.map((c, j) => { const id = o.ids && o.ids[`${i},${j}`]; return `<td class="${i === 0 && o.entete !== false ? 'n' : ''}"${id ? ` id="${id}" data-repere="${id}"` : ''}>${c}</td>`; }).join('') + '</tr>').join('') + '</table>';
  }
  const svg = (w, h, corps, label) => `<svg viewBox="0 0 ${w} ${h}" role="img" aria-label="${label}" font-family="'Times New Roman',Tinos,'Liberation Serif',serif" font-size="17">` +
    '<defs><marker id="pt" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 1 L10 5 L0 9 z" fill="#000"/></marker></defs>' + corps + '</svg>';
  const t = (x, y, s, o = '') => `<text x="${x}" y="${y}" ${o}>${s}</text>`;
  const tc = (x, y, s, o = '') => t(x, y, s, `text-anchor="middle" ${o}`);
  const fl = (x1, y1, x2, y2, o = '') => `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="#000" stroke-width="1.5" marker-end="url(#pt)" ${o}/>`;
  const boite = (x, y, w, h, lignes, o = {}) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="#fff" stroke="#000" stroke-width="1.3"/>` +
    lignes.map((s, i) => tc(x + w / 2, y + h / 2 + (i - (lignes.length - 1) / 2) * (o.dy || 19) + 6, s, o.gras === false ? '' : 'font-weight="700"')).join('');
  window.FeuilleSVT = { code, sequences, svg, t, tc, fl, boite };
})();
