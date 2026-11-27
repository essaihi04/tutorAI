/*
 * Le fil de la démarche d'investigation (cours de référence SVT « Consommation de la matière organique », 27 novembre 2026).
 * docs/reference-svt/ARCHITECTURE.md § 1.1 : chaque diapo d'activité porte son étape, visible en haut à droite du tableau.
 *
 *   Problème → Hypothèse → Expérience → Résultats → Analyse → Conclusion
 *
 * Six pastilles sur un fil : celles des étapes déjà faites sont vertes et cochées, celle de l'étape en cours est allumée
 * (jaune, plus grosse) avec son mot écrit à côté, les suivantes sont de simples cercles pâles.
 *
 * Usage (la page charge ce fichier après tableau.js) :
 *   <script src="demarche.js"></script>
 *   Scene(canvas, (c) => { scene.cadre(31); …le dessin de la scène… ; window.Demarche.dessiner(c); return c.fin(); });
 *
 *   - L'étape vient de l'URL : ?demarche=<1..6> (rien n'est dessiné si le paramètre est absent ou hors de 1..6).
 *   - À appeler À LA FIN du dessin, hors de toute découpe (ctx.clip) et de toute mosaïque : le fil est posé dans le coin haut
 *     droit du CANVAS, en pixels de l'écran (il ne dépend ni de l'échelle du cadre ni du zoom du téléphone) : pastilles de
 *     12 px et mot de 15 px sur un ordinateur, pastilles de 9 px et mot de 15 px dans le petit cadre du téléphone.
 *   - Il déclare le repère pointable `demarche` (« la démarche : étape 3 sur 6, Expérience »).
 *   - La page garde libre le coin haut droit : Demarche.reserve(c) renvoie { w, h } en pixels de l'écran (0 × 0 sans étape),
 *     Demarche.boite(c) le même rectangle { x, y, w, h } dans les coordonnées du dessin courant (à appeler dans le dessin).
 *   - Demarche.etape (0 = aucune), Demarche.nom, Demarche.ETAPES, Demarche.texte() (une phrase pour `ce_qui_se_voit`),
 *     Demarche.regler(n) (changer d'étape sans recharger : set_parameters {demarche}).
 */
(function () {
  'use strict';
  const ETAPES = ['Problème', 'Hypothèse', 'Expérience', 'Résultats', 'Analyse', 'Conclusion'];
  const lire = (v) => { const n = Math.round(+v); return n >= 1 && n <= 6 ? n : 0; };
  let etape = 0;
  try { etape = lire(new URLSearchParams(location.search).get('demarche')); } catch (_) { /* pas d'URL */ }
  const POLICE = () => (window.Tableau && window.Tableau.POLICE) || 'sans-serif';
  const TAU = Math.PI * 2;

  /* La géométrie en pixels de l'écran : petit cadre (téléphone en paysage) ou non. */
  function geometrie(c) {
    const W = c.W || 760, H = c.H || 420, petit = W < 560 || H < 300;
    const r = petit ? 4.5 : 6, rc = r + (petit ? 2 : 2.5), pas = petit ? 15 : 19, t = 15, marge = petit ? 5 : 8;
    const ctx = c.ctx; ctx.save(); ctx.font = `700 ${t}px ${POLICE()}`;
    const mot = etape ? ETAPES[etape - 1] : '', lm = mot ? ctx.measureText(mot).width : 0; ctx.restore();
    const lf = 5 * pas + 2 * rc;                         // le fil des six pastilles
    const w = lf + 8 + lm + marge, h = Math.max(2 * rc, t) + 2 * 3;
    return { W, H, petit, r, rc, pas, t, marge, mot, lm, lf, w, h, x: W - w, y: 2 };
  }

  const D = {
    ETAPES,
    get etape() { return etape; },
    get nom() { return etape ? ETAPES[etape - 1] : ''; },
    regler(n) { etape = lire(n); return etape; },
    texte() { return etape ? `Fil de la démarche (en haut à droite) : étape ${etape} sur 6, « ${ETAPES[etape - 1]} »${etape > 1 ? ' ; déjà faites : ' + ETAPES.slice(0, etape - 1).join(', ') : ''}.` : ''; },
    /** La place prise dans le coin haut droit du canvas, en pixels de l'écran. */
    reserve(c) { if (!etape) return { w: 0, h: 0 }; const g = geometrie(c); return { w: g.w, h: g.h + g.y }; },
    /** Le même rectangle dans les coordonnées du dessin courant (transformation du contexte au moment de l'appel). */
    boite(c) {
      if (!etape) return { x: 0, y: 0, w: 0, h: 0 };
      const g = geometrie(c), d = window.devicePixelRatio || 1, inv = c.ctx.getTransform().inverse();
      const a = inv.transformPoint(new DOMPoint(g.x * d, 0)), b = inv.transformPoint(new DOMPoint(g.W * d, (g.y + g.h) * d));
      return { x: a.x, y: a.y, w: b.x - a.x, h: b.y - a.y };
    },
    dessiner(c) {
      if (!etape || !c || !c.ctx || window.__mesureEnCours) return;
      const ctx = c.ctx, d = window.devicePixelRatio || 1, g = geometrie(c);
      ctx.save();
      ctx.setTransform(d, 0, 0, d, 0, 0); ctx.globalAlpha = 1; ctx.shadowBlur = 0; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
      const cy = g.y + g.h / 2, x0 = g.W - g.marge - g.lf + g.rc, xi = (i) => x0 + i * g.pas;
      // le mot de l'étape en cours, à gauche du fil
      ctx.font = `700 ${g.t}px ${POLICE()}`; ctx.textBaseline = 'middle'; ctx.textAlign = 'right';
      ctx.fillStyle = '#facc15'; ctx.shadowColor = 'rgba(250,204,21,.45)'; ctx.shadowBlur = 4;
      ctx.fillText(g.mot, x0 - g.rc - 8, cy + 1); ctx.shadowBlur = 0;
      // le fil : vert jusqu'à l'étape en cours, pâle ensuite
      ctx.lineWidth = 2;
      ctx.strokeStyle = 'rgba(226,232,240,.28)'; ctx.beginPath(); ctx.moveTo(xi(etape - 1), cy); ctx.lineTo(xi(5), cy); ctx.stroke();
      if (etape > 1) { ctx.strokeStyle = 'rgba(74,222,128,.85)'; ctx.beginPath(); ctx.moveTo(xi(0), cy); ctx.lineTo(xi(etape - 1), cy); ctx.stroke(); }
      for (let i = 0; i < 6; i++) {
        const x = xi(i);
        if (i < etape - 1) {              // faite : pastille verte cochée
          ctx.fillStyle = '#22c55e'; ctx.beginPath(); ctx.arc(x, cy, g.r, 0, TAU); ctx.fill();
          ctx.strokeStyle = '#052e16'; ctx.lineWidth = g.petit ? 1.5 : 1.9;
          ctx.beginPath(); ctx.moveTo(x - g.r * .48, cy + g.r * .02); ctx.lineTo(x - g.r * .1, cy + g.r * .42); ctx.lineTo(x + g.r * .52, cy - g.r * .38); ctx.stroke();
        } else if (i === etape - 1) {     // en cours : allumée
          const h = ctx.createRadialGradient(x, cy, 1, x, cy, g.rc * 2.1);
          h.addColorStop(0, 'rgba(250,204,21,.55)'); h.addColorStop(1, 'rgba(250,204,21,0)');
          ctx.fillStyle = h; ctx.beginPath(); ctx.arc(x, cy, g.rc * 2.1, 0, TAU); ctx.fill();
          const f = ctx.createRadialGradient(x - g.rc * .3, cy - g.rc * .3, .5, x, cy, g.rc);
          f.addColorStop(0, '#fff7c2'); f.addColorStop(.55, '#facc15'); f.addColorStop(1, '#d19a06');
          ctx.fillStyle = f; ctx.beginPath(); ctx.arc(x, cy, g.rc, 0, TAU); ctx.fill();
          ctx.strokeStyle = '#fff3b0'; ctx.lineWidth = 1.2; ctx.stroke();
        } else {                          // à venir : cercle pâle
          ctx.fillStyle = 'rgba(15,35,28,.55)'; ctx.beginPath(); ctx.arc(x, cy, g.r - .5, 0, TAU); ctx.fill();
          ctx.strokeStyle = 'rgba(226,232,240,.5)'; ctx.lineWidth = 1.4; ctx.stroke();
        }
      }
      if (c.repere) c.repere('demarche', g.x, g.y, g.w, g.h, `la démarche : étape ${etape} sur 6, ${ETAPES[etape - 1]}`);
      ctx.restore();
    },
  };
  window.Demarche = D;
})();
