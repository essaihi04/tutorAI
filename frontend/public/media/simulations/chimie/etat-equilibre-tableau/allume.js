/*
 * allume.js — allumer ce qu’une étape utilise, et compter en allumant (19 novembre 2026 ; skill simulations-au-tableau
 * règles 16 et 17, professeur règles 44 et 45). Chargé APRÈS tableau.js, sur les pages de ce dossier.
 *
 * Les rectangles viennent des repères que la page déclare déjà (craie.repere(id, …)) : chaque repère est noté, à chaque
 * dessin, avec la transformation courante (tableau large, blocs.js : il suit le dessin). Un calque transparent posé sur
 * le canevas y peint, pour l’étape en cours :
 *   - un HALO jaune autour de ce que l’étape utilise (fort pour l’étape en cours, doux pour ce qui reste allumé) ;
 *   - pour un comptage, le NUMÉRO propre de chaque élément (« 1 », « 2 », « 3 »…) écrit à côté, à la craie, qui reste ;
 *     le total s’écrit une fois, à la fin (`total`).
 * La page donne la règle : Allume.regle(() => [ { id, fort?, num?, cote? }, { total: '3 lignes', id, cote? } ]).
 *   id   : un repère de la page ; fort : halo de l’étape en cours ; num : numéro écrit à côté (cote : 'droite' (défaut),
 *          'gauche', 'haut', 'bas', 'basd' : dessous, à droite) ; total : texte écrit à côté du repère id (jaune).
 * Allume.decrire(liste) : la phrase pour ce_qui_se_voit (« allumé : … ; compté : 1, 2, 3 »).
 */
(function () {
  'use strict';
  const T = window.Tableau, P = T.Craie.prototype, avant = P.repere;
  const RECTS = {};
  P.repere = function (id, x, y, w, h, label) {
    const r = avant.apply(this, arguments);
    try {
      const m = this.ctx.getTransform(), d = devicePixelRatio || 1;
      const p1 = m.transformPoint(new DOMPoint(x, y)), p2 = m.transformPoint(new DOMPoint(x + w, y + h));
      RECTS[id] = { x: Math.min(p1.x, p2.x) / d, y: Math.min(p1.y, p2.y) / d, w: Math.abs(p2.x - p1.x) / d, h: Math.abs(p2.y - p1.y) / d, cv: this.canvas };
    } catch (e) { /* repère sans transformation : ignoré */ }
    return r;
  };
  let regle = null, calque = null, sig = '';
  function calqueDe(cv) {
    if (calque && calque.__cv === cv) return calque;
    calque = document.createElement('canvas'); calque.__cv = cv;
    Object.assign(calque.style, { position: 'absolute', inset: '0', width: '100%', height: '100%', pointerEvents: 'none', zIndex: 2 });
    calque.setAttribute('aria-hidden', 'true');
    cv.parentElement.appendChild(calque);
    return calque;
  }
  function halo(ctx, r, fort) {
    const pad = 4;
    ctx.save();
    ctx.fillStyle = fort ? 'rgba(250,204,21,.20)' : 'rgba(250,204,21,.09)';
    ctx.strokeStyle = fort ? 'rgba(250,204,21,.95)' : 'rgba(250,204,21,.45)';
    ctx.lineWidth = fort ? 2.6 : 1.4;
    if (fort) { ctx.shadowColor = 'rgba(250,204,21,.7)'; ctx.shadowBlur = 10; }
    ctx.beginPath(); ctx.roundRect(r.x - pad, r.y - pad, r.w + 2 * pad, r.h + 2 * pad, 7); ctx.fill(); ctx.shadowBlur = 0; ctx.stroke();
    ctx.restore();
  }
  function ecrire(ctx, r, texte, cote, taille, W, H) {
    ctx.save();
    ctx.font = `${taille}px ${T.POLICE}`; ctx.textBaseline = 'middle';
    const w = ctx.measureText(texte).width, pad = 9;
    let x, y;
    if (cote === 'gauche') { x = r.x - pad - w; y = r.y + r.h / 2; }
    else if (cote === 'haut') { x = r.x + r.w / 2 - w / 2; y = r.y - pad - taille / 2; }
    else if (cote === 'bas') { x = r.x + r.w / 2 - w / 2; y = r.y + r.h + pad + taille / 2; }
    else if (cote === 'basd') { x = r.x + r.w - w; y = r.y + r.h + pad + taille / 2; }
    else { x = r.x + r.w + pad; y = r.y + r.h / 2; }
    x = Math.max(2, Math.min(W - w - 2, x)); y = Math.max(taille / 2 + 1, Math.min(H - taille / 2 - 1, y));
    ctx.fillStyle = '#ffe36e'; ctx.shadowColor = 'rgba(255,255,255,.25)'; ctx.shadowBlur = 1;
    ctx.fillText(texte, x, y);
    ctx.restore();
  }
  function dessiner(liste) {
    const items = liste.filter(it => RECTS[it.id]);
    const cv = items.length ? RECTS[items[0].id].cv : document.getElementById('canvas');
    if (!cv) return;
    const c = calqueDe(cv), d = devicePixelRatio || 1, b = cv.getBoundingClientRect();
    const W = Math.round(b.width * d), H = Math.round(b.height * d);
    const s = JSON.stringify(items.map(it => [it, RECTS[it.id].x, RECTS[it.id].y, RECTS[it.id].w, RECTS[it.id].h])) + W + 'x' + H;
    if (s === sig) return; sig = s;
    if (c.width !== W || c.height !== H) { c.width = W; c.height = H; }
    const ctx = c.getContext('2d'); ctx.setTransform(d, 0, 0, d, 0, 0); ctx.clearRect(0, 0, b.width, b.height);
    for (const it of items) if (!it.total && it.halo !== false) halo(ctx, RECTS[it.id], !!it.fort);
    const taille = Math.max(17, Math.min(28, b.height * .065));   // même taille pour tous les numéros d’un comptage
    for (const it of items) {
      const r = RECTS[it.id];
      if (it.num != null) ecrire(ctx, r, String(it.num), it.cote, taille, b.width, b.height);
      if (it.total) ecrire(ctx, r, it.total, it.cote, Math.max(17, taille * .9), b.width, b.height);
    }
  }
  function boucle() {
    if (regle) { let l = []; try { l = regle() || []; } catch (e) { l = []; } dessiner(l); }
    requestAnimationFrame(boucle);
  }
  window.Allume = {
    regle(fn) { regle = fn; if (!this.__parti) { this.__parti = true; requestAnimationFrame(boucle); } },
    rect: id => RECTS[id],
    /** L’étape en cours (la dernière commencée) parmi `noms`, selon commence(nom). */
    enCours(noms, commence) { let n = null; for (const x of noms) if (commence(x)) n = x; return n; },
    /**
     * La règle commune des pages à moteur (M.evs, M.commence, M.S.vue, M.S.fait) :
     *   table[vue][étape] = ['id*', 'id'] : pendant l’étape, '*' allumé fort (ce qu’elle écrit), sans '*' doux (ce qu’elle utilise) ;
     *   compte[vue] = { items: [[id, étape où il s’allume], …], total: { apres: étape, id, texte, cote }, cote } :
     *   chaque élément s’allume à son étape avec son numéro, reste allumé ; le total s’écrit à l’étape `apres`.
     * À la fin du déroulé tout reste allumé, doucement.
     */
    standard(M, table, compte) {
      const v = M.S.vue, noms = M.evs().map(e => e.nom), cur = this.enCours(noms, n => M.commence(n));
      if (!cur) return [];
      const l = (((table || {})[v] || {})[cur] || []).map(x => ({ id: x.replace('*', ''), fort: x.endsWith('*') }));
      const C = compte && compte[v];
      if (C) {
        const fini = C.total && M.commence(C.total.apres);
        C.items.forEach(([id, debut], k) => {
          if (!M.commence(debut)) return;
          const suiv = C.items[k + 1] && M.commence(C.items[k + 1][1]);
          l.push({ id, num: k + 1, fort: !suiv && !fini, cote: C.cote });
        });
        if (fini) l.push({ id: C.total.id, total: C.total.texte, cote: C.total.cote, halo: false });
      }
      return M.S.fait ? l.map(it => ({ ...it, fort: false })) : l;
    },
    decrire(liste) {
      const lit = liste.filter(it => !it.total && it.num == null).map(it => it.id), cpt = liste.filter(it => it.num != null).map(it => `${it.num} (${it.id})`);
      const tot = liste.filter(it => it.total).map(it => it.total);
      const m = [];
      if (lit.length) m.push(`allumé en jaune : ${lit.join(', ')}`);
      if (cpt.length) m.push(`compté en allumant : ${cpt.join(', ')}`);
      if (tot.length) m.push(`total écrit : ${tot.join(', ')}`);
      return m.join(' ; ');
    },
  };
})();
