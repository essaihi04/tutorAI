/*
 * Imprimer / enregistrer en PDF ce qui est écrit au tableau (demande du 8 novembre 2026) : toutes les pages d'une
 * manip (la fiche et la page de l'élève, la carte complète…) deviennent des images sur fond blanc, aux couleurs
 * d'encre (la craie claire sur tableau sombre s'imprime mal), rangées dans un aperçu ; « Imprimer / PDF » ouvre la
 * boîte d'impression du navigateur (où l'on choisit « Enregistrer au format PDF ») ; « Télécharger » donne chaque
 * page en PNG. Tout se passe dans la page de la manip (dans l'iframe du cours : sandbox allow-modals allow-downloads).
 *
 *   window.Tableau.imprimer({ titre, pages: [{ nom, preparer() }], scene, restaurer() })
 *     preparer() met la scène dans l'état de la page (tout écrit) ; scene.image() rend le PNG ; restaurer() remet
 *     l'état d'avant.
 */
(function () {
  'use strict';
  if (!window.Tableau || window.Tableau.imprimer) return;
  const { COULEURS } = window.Tableau;
  // Les couleurs d'encre, pour le papier : mêmes noms que la craie.
  const ENCRE = { blanc: '#1f2937', cyan: '#0e7490', jaune: '#92400e', vert: '#15803d', violet: '#6d28d9', orange: '#c2410c',
    bleu: '#1d4ed8', rouge: '#b91c1c', rose: '#be185d', faible: 'rgba(31,41,55,.6)', tresfaible: 'rgba(31,41,55,.3)' };
  const CSS = `
.impression { position: fixed; inset: 0; z-index: 50; background: #f3f4f6; color: #111; overflow: auto; padding: 1em; font-family: system-ui, sans-serif; font-size: 15px; }
.impression .actions { display: flex; flex-wrap: wrap; gap: .6em; align-items: center; margin-bottom: 1em; }
.impression .actions button, .impression .actions a { font: inherit; padding: .45em 1em; border-radius: 8px; border: 1px solid #9ca3af; background: #fff; color: #111; cursor: pointer; text-decoration: none; }
.impression .actions .principal { background: #1d4ed8; color: #fff; border-color: #1d4ed8; }
.impression .actions .note { color: #4b5563; font-size: .9em; }
.impression figure { margin: 0 0 1.2em; background: #fff; border: 1px solid #d1d5db; border-radius: 10px; padding: .6em; page-break-after: always; break-after: page; }
.impression figure:last-child { page-break-after: auto; break-after: auto; }
.impression img { display: block; width: 100%; height: auto; }
.impression figcaption { color: #4b5563; font-size: .85em; margin-top: .4em; display: flex; justify-content: space-between; }
@media print {
  @page { size: landscape; margin: 10mm; }
  html, body { background: #fff !important; overflow: visible !important; height: auto !important; }
  body > *:not(.impression) { display: none !important; }
  .impression { position: static; padding: 0; background: #fff; }
  .impression .actions { display: none; }
  .impression figure { border: 0; padding: 0; }
}`;

  function surBlanc(dataUrl) {
    return new Promise(resolve => {
      const img = new Image();
      img.onload = () => {
        const c = document.createElement('canvas'); c.width = img.width; c.height = img.height;
        const x = c.getContext('2d'); x.fillStyle = '#fff'; x.fillRect(0, 0, c.width, c.height); x.drawImage(img, 0, 0);
        resolve(c.toDataURL('image/png'));
      };
      img.src = dataUrl;
    });
  }

  async function imprimer({ titre = 'Tableau', pages, scene, restaurer }) {
    if (document.querySelector('.impression')) return;
    const sombre = { ...COULEURS };
    Object.assign(COULEURS, ENCRE);
    const images = [];
    try {
      for (const p of pages) { p.preparer(); images.push({ nom: p.nom, src: await surBlanc(scene.image()) }); }
    } finally {
      Object.assign(COULEURS, sombre);
      if (restaurer) restaurer();
      scene.sale = true;
    }
    if (!document.getElementById('impression-style')) { const st = document.createElement('style'); st.id = 'impression-style'; st.textContent = CSS; document.head.append(st); }
    const el = document.createElement('section'); el.className = 'impression'; el.setAttribute('role', 'dialog'); el.setAttribute('aria-label', 'Aperçu avant impression');
    const propre = titre.replace(/[^\p{L}\p{N}]+/gu, '_').replace(/^_|_$/g, '');
    el.innerHTML = `<div class="actions">
      <button class="principal" id="impression-imprimer">🖨️ Imprimer / PDF</button>
      ${images.map((im, i) => `<a download="${propre}_${i + 1}.png" href="${im.src}">⬇ Télécharger page ${i + 1}</a>`).join('')}
      <button id="impression-fermer">Fermer</button>
      <span class="note">Dans la boîte d'impression, choisis « Enregistrer au format PDF » pour garder toutes les pages.</span>
    </div>` + images.map((im, i) => `<figure><img src="${im.src}" alt="${im.nom}"><figcaption><span>${titre} — ${im.nom}</span><span>page ${i + 1} / ${images.length}</span></figcaption></figure>`).join('');
    document.body.append(el);
    el.querySelector('#impression-fermer').onclick = () => el.remove();
    el.querySelector('#impression-imprimer').onclick = () => { try { window.print(); } catch (_) { /* impression refusée : les téléchargements restent */ } };
    window.addEventListener('afterprint', () => el.remove(), { once: true });
  }
  window.Tableau.imprimer = imprimer;
})();
