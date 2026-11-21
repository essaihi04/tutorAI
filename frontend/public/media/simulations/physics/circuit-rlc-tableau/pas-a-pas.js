/*
 * Un exercice du national JOUÉ pas à pas (18 novembre 2026, 2ᵉ passe de la logique des cours RC, RL, RLC et ch9 :
 * « simple, animé, expliqué ; ne pas tout donner au départ ; laisser à l'élève le temps de trouver seul »).
 * Règles 33, 37 et 41 du professeur, règle 14 de simulations-au-tableau.
 *
 * Une page = un sujet, une diapositive = une étape : `?sujet=<id>&etape=<k>` (k = 1 … N) (une URL par diapositive, l'iframe se
 * recharge, règle 39). À l'étape k :
 *   - `enonce`     : la figure du sujet (circuit peint, graphe ou tableau) et les étapes 1 … k − 2 déjà faites ;
 *   - `courbe`     : la courbe se trace dans le temps (seulement à l'étape qui la découvre : `trace: true`) ;
 *   - `rappel`     : la correction de l'étape k − 1 se construit au tableau (tangente, 63 %, ligne du tableau…) et sa
 *                    ligne s'écrit dans « Ta copie », comme le barème la lit ;
 *   - `question`   : la question de l'étape k s'écrit, SANS sa réponse ;
 *   - `correction` : la réponse de l'étape k (seulement sur `play_until correction` ou `conclusions: true` : rien de
 *                    décisif n'est montré avant la réponse de l'élève ; la diapositive suivante la montre en `rappel`).
 * `?etape=fin` : la copie complète, toutes les étapes faites (la synthèse après la dernière étape).
 * Commandes : start, pause, resume, reset, play_until {moment}, set_parameters {conclusions}. `?depart=<moment>`
 * ouvre la scène figée sur ce moment.
 * Règle 50 du professeur (21 novembre 2026) : une étape peut porter `num`, le numéro de la question tel qu'imprimé dans
 * le sujet (« 2.1.2 ») ; il remplace alors le numéro d'étape (« 2. ») partout où la question et la réponse s'écrivent.
 * Copie identique dans chaque dossier de cours qui l'utilise (dipole-rc, dipole-rl, circuit-rlc, transformations
 * lentes et rapides) : pas de fichier partagé. La page déclare ses sujets puis appelle PasAPas({ id, titre, sujets }).
 */
(function () {
  'use strict';
  const MOMENTS = ['enonce', 'courbe', 'rappel', 'question', 'correction'];
  const PAUSE_AUTO = 2.2;   // s entre deux moments quand la scène court seule (start)

  /* ── Objets peints (règle 32), comme dans tau-rc.html et observer.html ── */
  const Peint = {
    sphere(ctx, x, y, r, [a, b, c]) {
      const g = ctx.createRadialGradient(x - r * .35, y - r * .4, r * .1, x, y, r); g.addColorStop(0, a); g.addColorStop(.45, b); g.addColorStop(1, c);
      ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.fill();
    },
    generateur(ctx, x, y, w, h, affiche) {
      ctx.save();
      ctx.fillStyle = 'rgba(0,0,0,.3)'; ctx.beginPath(); ctx.roundRect(x + 3, y + 4, w, h, 6); ctx.fill();
      const g = ctx.createLinearGradient(x, y, x + w, y + h); g.addColorStop(0, '#5b6670'); g.addColorStop(.5, '#3b444c'); g.addColorStop(1, '#262c32');
      ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(x, y, w, h, 6); ctx.fill();
      const ex = x + w * .12, ey = y + h * .34, ew = w * .76, eh = h * .3;
      ctx.fillStyle = '#0d1a10'; ctx.beginPath(); ctx.roundRect(ex, ey, ew, eh, 3); ctx.fill();
      ctx.fillStyle = '#7dfc8a'; ctx.font = `600 ${Math.round(eh * .72)}px monospace`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      ctx.fillText(affiche, ex + ew / 2, ey + eh / 2 + 1);
      Peint.sphere(ctx, x + w / 2, y, 4.2, ['#ffd0d0', '#e0393e', '#6d0f12']);
      Peint.sphere(ctx, x + w / 2, y + h, 4.2, ['#9aa0a6', '#2b2f33', '#050607']);
      ctx.restore();
    },
    resistor(ctx, x, y, w, h) {
      ctx.save();
      ctx.fillStyle = 'rgba(0,0,0,.28)'; ctx.beginPath(); ctx.roundRect(x + 2, y + 3, w, h, h / 2.2); ctx.fill();
      const g = ctx.createLinearGradient(0, y, 0, y + h); g.addColorStop(0, '#f3e1bf'); g.addColorStop(.45, '#d9bf8f'); g.addColorStop(1, '#9c8358');
      ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(x, y, w, h, h / 2.2); ctx.fill();
      [[.24, '#7b4a1e'], [.38, '#111'], [.52, '#d32f2f'], [.78, '#c9a227']].forEach(([f, k]) => { ctx.fillStyle = k; ctx.fillRect(x + w * f, y + 1, w * .07, h - 2); });
      ctx.restore();
    },
    chimique(ctx, x, y, w, h) {
      ctx.save();
      const g = ctx.createLinearGradient(x, 0, x + w, 0); g.addColorStop(0, '#0b2a6b'); g.addColorStop(.35, '#2f6fe0'); g.addColorStop(.6, '#1d4fb8'); g.addColorStop(1, '#091f52');
      ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(x, y, w, h, [w * .25, w * .25, 4, 4]); ctx.fill();
      ctx.fillStyle = 'rgba(210,225,255,.75)'; ctx.fillRect(x + w * .7, y + 4, w * .16, h - 8);
      ctx.fillStyle = '#9aa3ad'; ctx.beginPath(); ctx.ellipse(x + w / 2, y + 3, w / 2 - 1, 3, 0, 0, 7); ctx.fill();
      ctx.restore();
    },
    bobine(ctx, x, y, w, h, n) {
      ctx.save();
      const g = ctx.createLinearGradient(x, y, x + w, y); g.addColorStop(0, '#3d4247'); g.addColorStop(.5, '#7a8187'); g.addColorStop(1, '#2f3337');
      ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(x + w * .18, y - 4, w * .64, h + 8, 4); ctx.fill();
      for (let k = 0; k < n; k++) {
        const yy = y + (k + .5) * h / n, gc = ctx.createLinearGradient(x, 0, x + w, 0);
        gc.addColorStop(0, '#7a3d12'); gc.addColorStop(.35, '#e59a52'); gc.addColorStop(.6, '#c4672a'); gc.addColorStop(1, '#5e2c0b');
        ctx.strokeStyle = gc; ctx.lineWidth = h / n * .8; ctx.beginPath(); ctx.ellipse(x + w / 2, yy, w / 2, h / n * .42, 0, 0, Math.PI * 2); ctx.stroke();
      }
      ctx.restore();
    },
    levier(ctx, px, py, bx, by, qx, qy) {
      ctx.save(); ctx.lineCap = 'round';
      Peint.sphere(ctx, qx, qy, 4.2, ['#fff1c9', '#cfa046', '#5e4210']);
      ctx.strokeStyle = '#4a4f55'; ctx.lineWidth = 6; ctx.beginPath(); ctx.moveTo(px, py); ctx.lineTo(bx, by); ctx.stroke();
      ctx.strokeStyle = '#c8ccd2'; ctx.lineWidth = 3.4; ctx.beginPath(); ctx.moveTo(px, py); ctx.lineTo(bx, by); ctx.stroke();
      Peint.sphere(ctx, px, py, 4.4, ['#fff1c9', '#cfa046', '#5e4210']);
      ctx.restore();
    },
    becher(ctx, x, y, w, h, teinte, niveau = .62) {
      ctx.save();
      const yl = y + h * (1 - niveau);
      const g = ctx.createLinearGradient(0, yl, 0, y + h); g.addColorStop(0, teinte[0]); g.addColorStop(1, teinte[1]);
      ctx.fillStyle = g; ctx.beginPath(); ctx.moveTo(x + 3, yl); ctx.lineTo(x + w - 3, yl); ctx.lineTo(x + w - 3, y + h - 6); ctx.quadraticCurveTo(x + w - 3, y + h - 2, x + w - 8, y + h - 2); ctx.lineTo(x + 8, y + h - 2); ctx.quadraticCurveTo(x + 3, y + h - 2, x + 3, y + h - 6); ctx.closePath(); ctx.fill();
      ctx.strokeStyle = 'rgba(220,235,245,.85)'; ctx.lineWidth = 2.2; ctx.beginPath(); ctx.moveTo(x - 4, y); ctx.lineTo(x, y + 4); ctx.lineTo(x, y + h - 6); ctx.quadraticCurveTo(x, y + h, x + 6, y + h); ctx.lineTo(x + w - 6, y + h); ctx.quadraticCurveTo(x + w, y + h, x + w, y + h - 6); ctx.lineTo(x + w, y + 4); ctx.lineTo(x + w + 4, y); ctx.stroke();
      ctx.fillStyle = 'rgba(255,255,255,.18)'; ctx.fillRect(x + 6, y + 10, 5, h - 22);
      ctx.restore();
    },
  };

  function PasAPas({ id, titre, sujets }) {
    const T = window.Tableau, $ = k => document.getElementById(k), q = new URLSearchParams(location.search);
    const sujetId = q.get('sujet') && sujets[q.get('sujet')] ? q.get('sujet') : Object.keys(sujets)[0];
    const SJ = sujets[sujetId], N = SJ.etapes.length;
    const brut = q.get('etape');
    const FIN = brut === 'fin', SUJET = brut === 'sujet';
    const K = FIN ? N : SUJET ? 0 : Math.max(0, Math.min(N - 1, (parseInt(brut || '1', 10) || 1) - 1));   // étape courante (?etape=1 → K = 0)
    const ET = FIN || SUJET ? null : SJ.etapes[K];
    const PREC = K > 0 && !FIN ? SJ.etapes[K - 1] : null;
    const vue = FIN ? 'copie' : SUJET ? 'sujet' : (ET.vue || 'graphe');
    const lib = e => (e.num ? `${e.num} :` : `${e.n}.`);   // le numéro du sujet (règle 50), sinon celui de l'étape
    const moments = SUJET ? ['enonce', 'donnees', 'questions'] : FIN ? ['enonce'] : MOMENTS.filter(m => m === 'enonce' || (m === 'courbe' && ET && ET.trace) || (m === 'rappel' && PREC) || ((m === 'question' || m === 'correction') && ET));
    let CONCL = q.get('conclusions') === '1';
    const S = { t0: {}, running: false, pause: false, prochain: 0, emis: 0 };
    const atteint = m => S.t0[m] !== undefined;
    const fx = v => T.fr(v, 2).replace(/(,\d*?)0+$/, '$1').replace(/,$/, '');

    /* ── Texte sur plusieurs lignes, largeur mesurée par le kit (fractions comprises) ── */
    const mesure = (c, s, t) => c.largeurTexte(window.Etats && window.Etats.annote ? window.Etats.annote(s) : s, t);   // chimie : avec les états (aq), (l)…
    function couper(c, s, larg, taille) {
      const mots = String(s).split(' '), lignes = []; let l = '';
      for (const m of mots) { const e = l ? l + ' ' + m : m; if (l && mesure(c, e, taille) > larg) { lignes.push(l); l = m; } else l = e; }
      if (l) lignes.push(l); return lignes;
    }
    const hauteur = (s, t) => (String(s).includes('⟦') ? t * 2.05 : t * 1.38);
    /* Ce qu'une ligne occupe au-dessus et au-dessous de sa ligne de base (une fraction monte et descend plus loin). */
    const haut = (s, t) => (String(s).includes('⟦') ? t * 1.32 : t * .95), bas = (s, t) => (String(s).includes('⟦') ? t * .8 : t * .32);
    const vite = s => Math.min(1.4, Math.max(.25, String(s).length / 30));   // durée d'écriture d'une ligne de la copie

    /* ── Disposition : figure à gauche, « Ta copie » à droite ── */
    function zones(L) {
      const P = Math.max(300, Math.min(560, L * (SJ.largeurCopie || .42)));   // chimie : copie plus large (équations avec leurs états)
      return { fig: { x0: 12, x1: L - P - 18, y0: 50, y1: 408 }, copie: { x0: L - P - 6, x1: L - 8, y0: 50, y1: 408 } };
    }

    /* ── Graphe : un ou plusieurs panneaux ── */
    function panneaux(g, Z) {
      const f = Z.fig, ps = g.panneaux, n = ps.length, col = g.disposition === 'colonnes';
      return ps.map((p, i) => {
        const h = col ? f.y1 - f.y0 : (f.y1 - f.y0 - (n - 1) * 14) / n, w = col ? (f.x1 - f.x0 - (n - 1) * 14) / n : f.x1 - f.x0;
        const x0 = f.x0 + (col ? i * (w + 14) : 0), y0 = f.y0 + (col ? 0 : i * (h + 14));
        const ax = x0 + 52, ay = y0 + h - 30, ax1 = x0 + w - 14, ay1 = y0 + 22;
        const X = t => ax + (t - (g.tmin || 0)) / (g.tmax - (g.tmin || 0)) * (ax1 - ax - 12);
        const Y = v => ay - (v - p.ymin) / (p.ymax - p.ymin) * (ay - ay1 - 6);
        return { ...p, x0, y0, w, h, ax, ay, ax1, ay1, X, Y, zero: Y(Math.max(p.ymin, Math.min(p.ymax, 0))) };
      });
    }
    function dessinerAxes(c, g, P) {
      for (const p of P) {
        c.fleche(p.ax, p.zero, p.ax1, p.zero, { couleur: 'faible', largeur: 1.6 });
        c.fleche(p.ax, p.ay, p.ax, p.ay1 - 4, { couleur: 'faible', largeur: 1.6 });
        for (const t of g.tgrad || []) { const x = p.X(t); c.ligne(x, p.zero - 4, x, p.zero + 4, { couleur: 'faible', largeur: 1.3, duree: .02 }); if (p === P[P.length - 1] || g.disposition === 'colonnes' || p.toutesGrad) c.texte(fx(t), x, Math.min(p.y0 + p.h - 4, p.zero + 20), { couleur: 'blanc', taille: 15, align: 'center', duree: .05 }); }
        for (const v of p.grad || []) { c.ligne(p.ax - 4, p.Y(v), p.ax + 4, p.Y(v), { couleur: 'faible', largeur: 1.3, duree: .02 }); c.texte(fx(v), p.ax - 8, p.Y(v) + 5, { couleur: 'blanc', taille: 15, align: 'right', duree: .05 }); }
        c.texte(p.label, p.ax + 8, p.ay1 + 4, { couleur: 'blanc', taille: 16 });
        c.texte(g.tlabel, p.ax1, p.zero - 8, { couleur: 'blanc', taille: 15, align: 'right' });   // les étiquettes des courbes se placent loin de ce bout d'axe
        c.repere('graphe_' + p.id, p.x0, p.y0, p.w, p.h, p.nom || p.label);
      }
    }
    function dessinerCourbes(c, g, P, anime) {
      for (const p of P) for (const k of p.courbes || []) {
        const n = 160, t0 = g.tmin || 0;
        c.courbe(u => { const t = t0 + u * (g.tmax - t0), v = k.f(t); return [p.X(t), p.Y(Math.max(p.ymin, Math.min(p.ymax, v)))]; }, n,
          { couleur: k.couleur || 'rouge', largeur: 2.8, tremble: 0, net: true, duree: anime ? 2.6 : undefined });
        const [tn, dy] = k.etiquette || [g.tmax * .8, -14];
        c.texte(k.nom, p.X(tn), p.Y(k.f(tn)) + dy, { couleur: k.couleur || 'rouge', taille: 17, align: 'center' });
        c.repere(k.id, p.X(tn) - 30, p.Y(k.f(tn)) + dy - 20, 60, 28, 'la courbe ' + k.nom);
      }
      // Droites données par le sujet (la tangente (T) dessinée sur la figure de l'examen).
      for (const p of P) for (const d of p.droites || []) {
        c.ligne(p.X(d.de[0]), p.Y(d.de[1]), p.X(d.a[0]), p.Y(d.a[1]), { couleur: d.couleur || 'blanc', largeur: 1.8, tremble: 0 });
        c.texte(d.nom, p.X(d.a[0]) + 6, p.Y(d.a[1]) + 4, { couleur: d.couleur || 'blanc', taille: 17 });
        c.repere(d.id || 'droite_T', p.X(d.a[0]) - 20, p.Y(d.a[1]) - 16, 60, 28, 'la droite ' + d.nom);
      }
    }
    /* Constructions de lecture : tangente, niveau (63 %), point lu, période, choix d'une courbe. */
    function construire(c, P, ops) {
      for (const o of ops || []) {
        const p = P.find(x => x.id === o.panneau) || P[0]; if (!p) continue;
        const coul = o.couleur || 'jaune';
        if (o.type === 'asymptote') {
          c.ligne(p.ax, p.Y(o.y), p.ax1 - 8, p.Y(o.y), { couleur: coul, largeur: 1.6, pointille: [7, 6], tremble: 0 });
          c.texte(o.label, p.ax1 - 10, p.Y(o.y) - 8, { couleur: coul, taille: 16, align: 'right' });
          c.repere(o.id || 'asymptote', p.ax, p.Y(o.y) - 24, p.ax1 - p.ax, 32, o.label);
        } else if (o.type === 'tangente') {
          const x1 = p.X(o.t1), y1 = p.Y(o.y1);
          c.ligne(p.X(o.t0 || 0), p.Y(o.y0 || 0), x1 + (x1 - p.X(o.t0 || 0)) * .12, y1 + (y1 - p.Y(o.y0 || 0)) * .12, { couleur: coul, largeur: 2, tremble: 0 });
          c.point(x1, y1, 4.5, coul);
          c.ligne(x1, y1, x1, p.zero, { couleur: coul, largeur: 1.5, pointille: [5, 5], tremble: 0 });
          c.texte(o.label, x1 + 6, p.zero - 10, { couleur: coul, taille: 17 });
          c.repere(o.id || 'tangente', Math.min(p.X(o.t0 || 0), x1) - 6, Math.min(y1, p.zero) - 14, Math.abs(x1 - p.X(o.t0 || 0)) + 70, Math.abs(p.zero - y1) + 22, o.label);
        } else if (o.type === 'niveau') {
          const x = p.X(o.t), y = p.Y(o.y);
          c.ligne(p.ax, y, x, y, { couleur: coul, largeur: 1.5, pointille: [5, 5], tremble: 0 });
          c.texte(o.labelY, p.ax + 6, y - 7, { couleur: coul, taille: 16 });
          if (o.t !== undefined && o.labelT !== undefined) {
            c.ligne(x, y, x, p.zero, { couleur: coul, largeur: 1.5, pointille: [5, 5], tremble: 0 }); c.point(x, y, 4.5, coul);
            c.texte(o.labelT, x + 6, p.zero - 10, { couleur: coul, taille: 17 });
          }
          c.repere(o.id || 'niveau', p.ax, y - 22, Math.max(80, x - p.ax + 70), p.zero - y + 24, o.labelY);
        } else if (o.type === 'point') {
          const x = p.X(o.t), y = p.Y(o.y);
          if (o.guides) { c.ligne(p.ax, y, x, y, { couleur: coul, largeur: 1.3, pointille: [4, 5], tremble: 0 }); c.ligne(x, y, x, p.zero, { couleur: coul, largeur: 1.3, pointille: [4, 5], tremble: 0 }); }
          c.point(x, y, 5, coul);
          const [dx, dy] = o.decalage || [8, -10];
          c.texte(o.label, x + dx, y + dy, { couleur: coul, taille: 17, align: dx < 0 ? 'right' : 'left' });
          c.repere(o.id || 'point', x - 10, y - 26, 140, 40, o.label);
        } else if (o.type === 'periode') {
          const xa = p.X(o.t1), xb = p.X(o.t2), y = p.Y(o.y);
          c.ligne(xa, y, xa, p.zero, { couleur: coul, largeur: 1.3, pointille: [4, 5], tremble: 0 }); c.ligne(xb, y, xb, p.zero, { couleur: coul, largeur: 1.3, pointille: [4, 5], tremble: 0 });
          c.fleche(xa, y - 10, xb, y - 10, { couleur: coul, largeur: 1.8 }); c.fleche(xb, y - 10, xa, y - 10, { couleur: coul, largeur: 1.8 });
          c.texte(o.label, (xa + xb) / 2, y - 18, { couleur: coul, taille: 17, align: 'center' });
          c.repere(o.id || 'periode', xa, y - 40, xb - xa, p.zero - y + 40, o.label);
        } else if (o.type === 'entoure') {
          c.rect(p.x0 + 4, p.y0 + 2, p.w - 8, p.h - 6, { couleur: coul, largeur: 2.4 });
          if (o.label) c.texte(o.label, p.x0 + p.w / 2, p.y0 + p.h - 10, { couleur: coul, taille: 17, align: 'center' });
          c.repere(o.id || 'choix', p.x0, p.y0, p.w, p.h, o.label || 'la courbe choisie');
        }
      }
    }

    /* ── Le circuit du sujet, peint, avec les flèches de la convention récepteur ── */
    function dessinerCircuit(c, Z, ci, fleches) {
      const f = Z.fig, w = f.x1 - f.x0, h = f.y1 - f.y0;
      const x0 = f.x0 + w * .16, x1 = f.x0 + w * .78, y0 = f.y0 + h * .18, y1 = f.y0 + h * .82, xm = (x0 + x1) / 2, ym = (y0 + y1) / 2;
      const gauche = ci.gauche || 'generateur', droite = ci.droite || 'C';
      c.direct(() => {
        const ctx = c.ctx;
        if (gauche === 'generateur') Peint.generateur(ctx, x0 - 26, ym - 38, 52, 76, ci.affiche || 'E');
        else Peint.chimique(ctx, x0 - 70, ym - 30, 28, 52);
        if (ci.K) Peint.levier(ctx, x0 + (xm - x0) * .28, y0, x0 + (xm - x0) * .62, y0, x0 + (xm - x0) * .62, y0);
        if (ci.R) Peint.resistor(ctx, xm - 34 + (x1 - xm) * .2, y0 - 12, 68, 24);
        if (droite === 'C') Peint.chimique(ctx, x1 + 40, ym - 30, 28, 52);
        else Peint.bobine(ctx, x1 - 22, ym - 44, 44, 88, 8);
      });
      // Les fils, coupés là où sont les dipôles ; un condensateur : ses deux armatures à la craie, le vrai peint à côté.
      const coupe = (x, ya, yb, gap) => { c.ligne(x, ya, x, ym - gap); c.ligne(x, ym + gap, x, yb); };
      c.ligne(x0, y0, x1, y0); c.ligne(x0, y1, x1, y1);
      coupe(x0, y0, y1, gauche === 'generateur' ? 38 : 9);
      coupe(x1, y0, y1, droite === 'C' ? 9 : 44);
      const armatures = x => { c.ligne(x - 24, ym - 9, x + 24, ym - 9, { couleur: 'cyan', largeur: 3.4 }); c.ligne(x - 24, ym + 9, x + 24, ym + 9, { couleur: 'cyan', largeur: 3.4 }); };
      if (droite === 'C') armatures(x1);
      if (gauche !== 'generateur') armatures(x0);
      c.texte(ci.nomGauche || 'E', x0 - (gauche === 'generateur' ? 36 : 80), ym + 6, { couleur: gauche === 'generateur' ? 'blanc' : 'cyan', taille: 19, align: 'right' });
      if (ci.K) c.texte('K', x0 + (xm - x0) * .45, y0 - 14, { couleur: 'blanc', taille: 17, align: 'center' });
      if (ci.R) c.texte('R', xm + (x1 - xm) * .2, y0 - 20, { couleur: 'orange', taille: 19, align: 'center' });
      c.texte(ci.nomDroite || (droite === 'C' ? 'C' : '(L, r)'), x1 + (droite === 'C' ? 78 : 30), ym + 6, { couleur: droite === 'C' ? 'cyan' : 'orange', taille: 19 });
      c.repere('circuit', x0 - 40, y0 - 30, x1 - x0 + 110, y1 - y0 + 60, 'le circuit du sujet');
      if (fleches) {
        // i dans le sens de la maille (haut, vers la droite) ; chaque tension en convention récepteur : flèche opposée à i.
        c.fleche(x0 + 14, y0, x0 + 44, y0, { couleur: 'vert', largeur: 2.4 }); c.texte('i', x0 + 30, y0 + 22, { couleur: 'vert', taille: 19, align: 'center' });
        c.repere('fleche_i', x0, y0 - 6, 60, 34, 'le sens du courant i');
        if (ci.R) { const xr = xm + (x1 - xm) * .2; c.fleche(xr + 40, y0 + 24, xr - 40, y0 + 24, { couleur: 'orange', largeur: 2 }); c.texte('u_R', xr, y0 + 48, { couleur: 'orange', taille: 18, align: 'center' }); c.repere('fleche_uR', xr - 44, y0 + 14, 88, 42, 'la tension u_R'); }
        const lab = droite === 'C' ? 'u_C' : (ci.uL || 'u_L');
        c.fleche(x1 - 36, y1 - 26, x1 - 36, y0 + 30, { couleur: droite === 'C' ? 'cyan' : 'orange', largeur: 2 }); c.texte(lab, x1 - 44, ym + 6, { couleur: droite === 'C' ? 'cyan' : 'orange', taille: 18, align: 'right' });
        c.repere(droite === 'C' ? 'fleche_uC' : 'fleche_uL', x1 - 90, y0 + 26, 64, y1 - y0 - 50, 'la tension ' + lab);
        if (gauche !== 'generateur') { c.fleche(x0 + 26, y0 + 30, x0 + 26, y1 - 26, { couleur: 'cyan', largeur: 2 }); c.texte(ci.uGauche || 'u_C', x0 + 34, ym + 6, { couleur: 'cyan', taille: 18 }); c.repere('fleche_uC', x0 + 14, y0 + 26, 64, y1 - y0 - 50, 'la tension ' + (ci.uGauche || 'u_C')); }
      }
    }

    /* ── Tableau d'avancement : les lignes s'ajoutent, une à une ── */
    function dessinerTableau(c, Z, tb, lignesVues, anime, grille = true) {   // grille : tout sauf les lignes `anime` (Set) ; sinon la ligne `anime` seule
      const f = Z.fig, cols = tb.colonnes.length, x0 = f.x0 + 4, x1 = f.x1 - 4, wEtat = (x1 - x0) * .2, wAv = (x1 - x0) * .1;
      const wc = (x1 - x0 - wEtat - wAv) / cols, y0 = f.y0 + 34, hl = 52;
      const xs = [x0, x0 + wEtat, x0 + wEtat + wAv]; for (let k = 1; k <= cols; k++) xs.push(x0 + wEtat + wAv + k * wc);
      if (!grille) {   // une seule ligne, écrite à son instant
        const i = anime, l = tb.lignes[i], yl = y0 + (i + 1) * hl;
        l.cases.forEach((s, k) => c.texte(s, (xs[k + 1] + xs[k + 2]) / 2, yl + hl * .64, { couleur: k === 0 ? 'jaune' : 'vert', taille: 18, align: 'center', max: xs[k + 2] - xs[k + 1] - 6, duree: vite(s) }));
        return;
      }
      c.texte(tb.equation, (x0 + x1) / 2, y0 - 10, { couleur: 'blanc', taille: 19, align: 'center', max: x1 - x0 });
      c.repere('equation', x0, y0 - 34, x1 - x0, 32, 'l’équation de la réaction');
      const nl = tb.lignes.length;
      c.direct(() => { c.rect(x0, y0, x1 - x0, hl * (nl + 1), { couleur: 'faible', largeur: 1.6 }); for (let k = 1; k <= nl; k++) c.ligne(x0, y0 + k * hl, x1, y0 + k * hl, { couleur: 'faible', largeur: 1.2 }); for (const x of xs.slice(1, -1)) c.ligne(x, y0, x, y0 + hl * (nl + 1), { couleur: 'faible', largeur: 1.2 }); });
      const ent = ['État', 'Avanc.', ...tb.colonnes];
      ent.forEach((s, k) => c.texte(s, (xs[k] + xs[k + 1]) / 2, y0 + hl * .64, { couleur: 'blanc', taille: 17, align: 'center', max: xs[k + 1] - xs[k] - 6 }));
      tb.lignes.forEach((l, i) => {
        const yl = y0 + (i + 1) * hl;
        c.texte(l.etat, (xs[0] + xs[1]) / 2, yl + hl * .64, { couleur: 'blanc', taille: 17, align: 'center', max: xs[1] - xs[0] - 6 });
        c.repere('ligne_' + (i + 1), x0, yl, x1 - x0, hl, 'la ligne « ' + l.etat + ' »');
        if (anime.has(i)) return;
        if (!lignesVues.has(i)) { c.texte('?', (xs[2] + x1) / 2, yl + hl * .64, { couleur: 'faible', taille: 20, align: 'center' }); return; }
        l.cases.forEach((s, k) => c.texte(s, (xs[k + 1] + xs[k + 2]) / 2, yl + hl * .64, { couleur: k === 0 ? 'jaune' : 'vert', taille: 18, align: 'center', max: xs[k + 2] - xs[k + 1] - 6 }));
      });
      c.repere('tableau', x0, y0, x1 - x0, hl * (nl + 1), 'le tableau d’avancement');
    }

    /* ── Données du sujet, en grand (vue « donnees ») ── */
    function dessinerDonnees(c, Z, lignes, anime) {
      const f = Z.fig, t = Math.max(19, 15 / (scene.s || 1)); let y = f.y0 + 6;
      for (const s of lignes) {
        for (const l of couper(c, s, f.x1 - f.x0 - 10, t)) { const yb = y + haut(l, t); y = yb + bas(l, t) + 4; const w = () => c.texte(l, f.x0 + 6, yb, { couleur: 'blanc', taille: t, duree: vite(l) }); if (anime) w(); else c.direct(w); }
        y += 6;
      }
      c.repere('donnees', f.x0, f.y0, f.x1 - f.x0, Math.max(40, y - f.y0), 'les données du sujet');
    }

    /* ── « Ta copie » : les réponses déjà faites, puis la question en cours ── */
    function dessinerCopie(c, Z, faites, prec, cour) {
      const z = Z.copie, larg = z.x1 - z.x0 - 20, plancher = 15 / (scene.s || 1), tq = Math.max(19, plancher), tc = Math.max(18, plancher), tt = Math.max(17, plancher), tf = Math.max(16, plancher);
      c.direct(() => c.rect(z.x0, z.y0, z.x1 - z.x0, z.y1 - z.y0, { couleur: 'tresfaible', largeur: 1.4, rayon: 8 }));
      c.direct(() => c.texte('Ta copie', z.x0 + 10, z.y0 - 12, { couleur: 'faible', taille: 16 }));
      // Blocs (de bas en haut on garde ce qui tient) : chaque réponse faite, puis la question en cours.
      const blocs = [];
      for (const e of faites) blocs.push({ e, mode: 'faite' });
      if (prec) blocs.push({ e: prec, mode: atteint('rappel') ? 'rappel' : 'cachee' });
      if (cour) blocs.push({ e: cour, mode: 'question' });
      const mesure = b => {
        const L = [];
        if (b.mode === 'question') {
          if (!atteint('question')) return L;
          for (const l of couper(c, `${lib(b.e)} ${b.e.question}`, larg, tq)) L.push({ s: l, couleur: 'jaune', taille: tq, anime: 'question' });
          if (CONCL || atteint('correction')) for (const s of b.e.copie) for (const l of couper(c, s, larg - 12, tc)) L.push({ s: l, couleur: 'vert', taille: tc, anime: 'correction', retrait: 12 });
          else L.push({ s: '… à toi d’abord.', couleur: 'faible', taille: tf, anime: 'question', retrait: 12 });
        } else if (b.mode !== 'cachee') {
          L.push({ s: `${lib(b.e)} ${b.e.court || b.e.titre}`, couleur: 'blanc', taille: tt, anime: b.mode === 'rappel' ? 'rappel' : null });
          for (const s of b.e.copie) for (const l of couper(c, s, larg - 12, tc)) L.push({ s: l, couleur: 'vert', taille: tc, anime: b.mode === 'rappel' ? 'rappel' : null, retrait: 12 });
        }
        return L;
      };
      const tout = blocs.map(mesure);
      // On garde les derniers blocs qui tiennent dans la hauteur ; les plus anciens se replient en « … ».
      let H = 0; const garde = [];
      for (let i = tout.length - 1; i >= 0; i--) {
        const h = tout[i].reduce((a, l) => a + haut(l.s, l.taille) + bas(l.s, l.taille) + 5, 0) + 10;
        if (H + h > z.y1 - z.y0 - 30 && garde.length) break;
        H += h; garde.unshift(i);
      }
      let y = z.y0 + 8;
      if (garde[0] > 0) { const n = tout.slice(0, garde[0]).filter(b => b.length).length; c.direct(() => c.texte(n > 1 ? `(étapes 1 à ${n} : déjà faites)` : '(étape 1 : déjà faite)', z.x0 + 10, y + 18, { couleur: 'faible', taille: 15 })); y += 26; }
      let groupe = null;
      for (const i of garde) {
        const y0 = y;
        for (const l of tout[i]) {
          const yb = y + haut(l.s, l.taille); y = yb + bas(l.s, l.taille) + 5;
          const w = () => c.texte(l.s, z.x0 + 10 + (l.retrait || 0), yb, { couleur: l.couleur, taille: l.taille, duree: vite(l.s) });
          // chaque groupe animé (rappel, question, correction) part de son propre instant
          if (l.anime) { if (groupe !== l.anime) { groupe = l.anime; c.cur = S.t0[l.anime] ?? c.cur; } w(); } else c.direct(w);
        }
        if (tout[i].length) c.repere(blocs[i].mode === 'question' ? 'question' : 'copie_' + blocs[i].e.n, z.x0, y0 - 4, z.x1 - z.x0, y - y0 + 10, blocs[i].mode === 'question' ? 'la question ' + blocs[i].e.n : 'la réponse ' + blocs[i].e.n);
        y += 10;
      }
      c.repere('copie', z.x0, z.y0, z.x1 - z.x0, z.y1 - z.y0, 'ta copie');
    }

    /* ── La page entière ── */
    function dessiner(c) {
      scene.cadre(11);
      const L = scene.L, Z = zones(L);
      const etiq = FIN ? `${SJ.titre} · la copie complète` : SUJET ? `${SJ.titre} · le sujet` : `${SJ.titre} · étape ${ET.n} sur ${N}`;
      c.texte(etiq, 14, 30, { couleur: 'faible', taille: 17, max: L - 28 });
      SJ.etapes.forEach((e, i) => { e.n = i + 1; });
      const faites = SJ.etapes.slice(0, Math.max(0, K - 1));
      if (FIN) {
        // La copie complète, sur toute la largeur : deux colonnes, trois si elle ne tient pas (téléphone : texte ≥ 15 px).
        const tt = Math.max(17, 15 / (scene.s || 1));
        const placer = (cols, court) => {
          const larg = (L - 40) / cols - 10, pos = []; let col = 0, y = 52;
          for (const e of SJ.etapes) {
            const ls = [`${lib(e)} ${e.court || e.titre}`, ...(court ? e.copie.slice(-1) : e.copie).flatMap(x => couper(c, x, larg - 12, tt))];
            const h = ls.reduce((a, x) => a + haut(x, tt) + bas(x, tt) + 3, 0) + 6;
            if (y + h > 412 && y > 52) { col++; y = 52; }
            pos.push({ e, ls, x: 20 + col * (larg + 20), y, larg }); y += h;
          }
          return col < cols ? pos : null;
        };
        // trop long (petit écran) : chaque étape garde sa ligne de résultat, la dernière de sa correction
        const pos = placer(2) || placer(3) || placer(2, true) || placer(3, true) || placer(4, true) || [];
        for (const { e, ls, x, y: y0, larg } of pos) {
          let y = y0;
          ls.forEach((x2, j) => { const yb = y + haut(x2, tt); y = yb + bas(x2, tt) + 3; c.texte(x2, x + (j ? 12 : 0), yb, { couleur: j ? 'vert' : 'blanc', taille: tt, max: larg - 12 }); });
          c.repere('copie_' + e.n, x - 4, y0, larg, y - y0 + 4, 'la réponse ' + e.n);
        }
        c.repere('copie', 10, 50, L - 20, 360, 'la copie complète');
        return c.fin();
      }
      if (SUJET) {
        // Le sujet, lu deux fois (règle 6) : d'abord les données (et le circuit), puis ce qu'on cherche, question par question.
        const Z = zones(L);
        if (SJ.circuit && !SJ.sansCircuit) {
          const Zc = { fig: { x0: Z.fig.x0, x1: Z.fig.x1, y0: Z.fig.y0, y1: Z.fig.y0 + (Z.fig.y1 - Z.fig.y0) * .55 } };
          c.direct(() => dessinerCircuit(c, Zc, SJ.circuit, false));
          if (atteint('donnees')) { c.depuis(S.t0.donnees); dessinerDonnees(c, { fig: { ...Z.fig, y0: Zc.fig.y1 + 4 } }, SJ.donnees, true); }
        } else if (atteint('donnees')) { c.depuis(S.t0.donnees); dessinerDonnees(c, Z, SJ.donnees, true); }
        const z = Z.copie; c.direct(() => c.rect(z.x0, z.y0, z.x1 - z.x0, z.y1 - z.y0, { couleur: 'tresfaible', largeur: 1.4 }));
        c.texte('Ce qu’on cherche', z.x0 + 10, z.y0 - 12, { couleur: 'faible', taille: 16 });
        if (atteint('questions')) {
          c.cur = S.t0.questions; let y = z.y0 + 8; const tq = Math.max(18, 15 / (scene.s || 1));
          for (const e of SJ.etapes) {
            const y0 = y;
            for (const l of couper(c, `${lib(e)} ${e.titre}`, z.x1 - z.x0 - 20, tq)) { const yb = y + haut(l, tq); y = yb + bas(l, tq) + 2; c.texte(l, z.x0 + 10, yb, { couleur: 'jaune', taille: tq, duree: vite(l) }); }
            c.repere('question_' + e.n, z.x0, y0 - 4, z.x1 - z.x0, y - y0 + 8, 'la question ' + e.n); y += 4;
          }
          c.repere('questions', z.x0, z.y0, z.x1 - z.x0, z.y1 - z.y0, 'ce qu’on cherche');
        }
        return c.fin();
      }
      c.depuis(S.t0.enonce ?? Infinity);
      if (!atteint('enonce')) return c.fin();
      // Figure de l'étape : posée d'emblée (la diapositive s'ouvre sur son état) ; seuls courbe, rappel, question et correction s'écrivent.
      if (vue === 'circuit') c.direct(() => dessinerCircuit(c, Z, SJ.circuit, true));
      else if (vue === 'donnees') dessinerDonnees(c, Z, ET.donnees || SJ.donnees, false);
      else if (vue === 'tableau') {
        const vues = new Set(), enCours = []; const tb = SJ.tableau;
        for (let i = 0; i < tb.lignes.length; i++) {
          const e = tb.lignes[i].etape;   // étape (index 0) qui remplit la ligne
          if (e < K - 1) vues.add(i);
          else if (e === K - 1 && atteint('rappel')) enCours.push([i, 'rappel']);
          else if (e === K && (CONCL || atteint('correction'))) enCours.push([i, atteint('correction') ? 'correction' : null]);
        }
        c.direct(() => dessinerTableau(c, Z, tb, vues, new Set(enCours.map(x => x[0])), true));
        for (const [i, m] of enCours) { if (m) c.cur = Math.max(c.cur, S.t0[m]); else c.cur = 0; dessinerTableau(c, Z, tb, null, i, false); }
      } else {
        const g = SJ.graphes[ET.graphe], P = panneaux(g, Z);
        c.direct(() => dessinerAxes(c, g, P));
        if (ET.trace) { if (atteint('courbe')) { c.cur = S.t0.courbe; dessinerCourbes(c, g, P, true); } }
        else c.direct(() => dessinerCourbes(c, g, P, false));
        // constructions faites (sur le même graphe), puis celle de l'étape d'avant (rappel), puis celle-ci (correction)
        for (const e of faites) if (e.graphe === ET.graphe) c.direct(() => construire(c, P, e.construit));
        if (PREC && PREC.graphe === ET.graphe && atteint('rappel')) { c.cur = Math.max(c.cur, S.t0.rappel); construire(c, P, PREC.construit); }
        if (CONCL || atteint('correction')) { c.cur = Math.max(c.cur, S.t0.correction ?? 0); construire(c, P, ET.construit); }
      }
      dessinerCopie(c, Z, faites, PREC, ET);
      return c.fin();
    }

    const scene = window.OndesTableau.Scene($('canvas'), dessiner, { large: true });
    function maintenant() { return (performance.now() - scene.ouvert) / 1000; }
    function atteindre(m) {
      const i = moments.indexOf(m); if (i < 0) return false;
      let t = maintenant();
      for (const x of moments.slice(0, i + 1)) if (!atteint(x)) { S.t0[x] = t; t += 0.05; }
      if (m === 'correction') CONCL = true;
      scene.sale = true; return true;
    }
    function dernier() { let d = null; for (const m of moments) if (atteint(m)) d = m; return d; }
    scene.avancer = () => {
      if (!S.running) return false;
      if (maintenant() >= S.prochain) {
        const i = moments.indexOf(dernier()), suiv = moments[i + 1];
        if (!suiv || suiv === 'correction') { S.running = false; S.pause = false; $('run').textContent = 'Rejouer'; pont.noter('finished'); pont.emettre(); return true; }
        atteindre(suiv); S.prochain = maintenant() + PAUSE_AUTO; pont.emettre();
      }
      if (performance.now() - S.emis > 500) { S.emis = performance.now(); pont.emettre(); }
      return true;
    };
    function reset(depart) {
      S.t0 = {}; S.running = false; S.pause = false; CONCL = q.get('conclusions') === '1'; scene.reecrire();
      S.t0.enonce = -100;   // la figure du sujet est là dès l'ouverture
      if (depart && moments.includes(depart)) atteindre(depart);
      $('run').textContent = 'Lancer'; scene.sale = true; T.bulle($('feedback'), FIN ? 'La copie complète.' : SUJET ? 'Le sujet : les données, puis ce qu’on cherche.' : `Étape ${ET.n} : ${ET.titre}`); pont && pont.emettre();
    }
    function start() { reset(); S.running = true; S.prochain = maintenant() + .4; $('run').textContent = 'Pause'; pont.noter('start'); pont.emettre(); }
    function pause() { if (!S.running) return; S.running = false; S.pause = true; $('run').textContent = 'Reprendre'; pont.noter('pause'); pont.emettre(); }
    function resume() { if (S.running) return; if (!S.pause) return start(); S.running = true; S.pause = false; S.prochain = maintenant() + .3; $('run').textContent = 'Pause'; pont.noter('resume'); pont.emettre(); }
    function playUntil(p) {
      const m = p && p.moment; if (!atteindre(m)) return;
      S.running = false; S.pause = true; $('run').textContent = 'Reprendre';
      T.bulle($('feedback'), 'Arrêt sur image : ' + ({ enonce: 'le sujet', courbe: 'la courbe tracée', rappel: 'la correction de l’étape d’avant', question: 'la question, à toi', correction: 'la correction' }[m] || m) + '.');
      pont.noter('play_until', { moment: m }); pont.emettre();
    }
    function setParameters(p) {
      const v = p && p.conclusions; if (v === undefined) return;
      CONCL = !(v === false || v === 0 || /^(false|0|non)$/i.test(String(v)));
      if (CONCL && moments.includes('correction') && !atteint('correction')) atteindre('correction');
      scene.sale = true; pont.noter('set_parameters', { conclusions: CONCL }); pont.emettre();
    }
    function ceQuiSeVoit() {
      if (SUJET) return `${SJ.titre} : le sujet. ${atteint('donnees') ? 'Données écrites : ' + SJ.donnees.map(x => (T.lisible || (y => y))(x)).join(' ; ') + '.' : 'Les données ne sont pas encore écrites.'} ${atteint('questions') ? 'Ce qu’on cherche : ' + SJ.etapes.map(e => `${lib(e)} ${e.titre}`).join(' ; ') + '.' : ''}`;
      if (FIN) return `${SJ.titre} : la copie complète, ${N} étapes : ` + SJ.etapes.map(e => `${lib(e)} ${e.copie.map(T.lisible || (x => x)).join(' ; ')}`).join(' | ');
      const m = [`${SJ.titre}, étape ${ET.n} sur ${N} (${ET.titre}). Vue : ${{ circuit: 'le circuit du sujet, flèches de i et des tensions en convention récepteur', graphe: 'le graphe du sujet', donnees: 'les données du sujet', tableau: 'le tableau d’avancement' }[vue]}.`];
      const faites = SJ.etapes.slice(0, Math.max(0, K - 1));
      if (faites.length) m.push('Déjà dans la copie : ' + faites.map(e => `${lib(e)} ${e.copie.map(x => (T.lisible || (y => y))(x)).join(' ; ')}`).join(' | ') + '.');
      if (PREC) m.push(atteint('rappel') ? `La correction de l’étape ${PREC.n} est construite et écrite : ${PREC.copie.map(x => (T.lisible || (y => y))(x)).join(' ; ')}.` : `La correction de l’étape ${PREC.n} n’est pas encore montrée.`);
      if (ET.trace) m.push(atteint('courbe') ? 'La courbe est tracée.' : 'La courbe n’est pas encore tracée.');
      m.push(atteint('question') ? `Question écrite : « ${(T.lisible || (y => y))(ET.question)} ».` : 'La question n’est pas encore écrite.');
      m.push(CONCL || atteint('correction') ? `Correction montrée : ${ET.copie.map(x => (T.lisible || (y => y))(x)).join(' ; ')}.` : 'La réponse est cachée : l’élève répond d’abord.');
      return m.join(' ');
    }
    $('run').onclick = () => (S.running ? pause() : S.pause ? resume() : start());
    SJ.etapes.forEach((e, i) => { e.n = i + 1; });
    T.explication({ [sujetId]: SJ.etapes.map((e, i) => ({ repere: SUJET ? 'question_' + (i + 1) : i === K && !FIN ? 'question' : 'copie_' + (i + 1), texte: `${lib(e)} ${e.titre} : ${e.copie.map(x => (T.lisible || (y => y))(x)).join(' ; ')}` })) });
    const commandes = ['start', 'pause', 'resume', 'reset', 'play_until', 'set_parameters'];
    const config = { id, version: '1.0', title: titre, variants: Object.keys(sujets).map(k => ({ id: k, label: sujets[k].titre })), commands: commandes,
      command_schema: { play_until: { moment: moments.join(' | ') }, set_parameters: { conclusions: 'true | false (false : la réponse de l’étape reste cachée)' } } };
    const pont = T.protocole({ id, commandes, config,
      texte: `${titre}. ${SJ.titre} joué une étape à la fois : la figure, la question, la réponse de l’élève, puis la correction écrite comme le barème la lit.`,
      // « finished » seulement une fois la correction montrée (ou la copie complète) : avant, play_until correction doit passer.
      etat: () => ({ simulation_status: S.running ? 'running' : (FIN || atteint('correction') || (SUJET && atteint('questions'))) ? 'finished' : S.pause ? 'paused' : 'idle', ce_qui_se_voit: ceQuiSeVoit(),
        time_s: dernier() ? +(moments.indexOf(dernier()) * PAUSE_AUTO).toFixed(1) : 0,
        moments: Object.fromEntries(moments.map((x, i) => [x, +(i * PAUSE_AUTO).toFixed(1)])), parameters: { sujet: sujetId, etape: FIN ? 'fin' : SUJET ? 'sujet' : ET.n, conclusions: CONCL },
        moment_atteint: dernier() }),
      progression: () => (moments.length ? moments.filter(atteint).length / moments.length : 1),
      executer: (cmd, p) => ({ start, pause, resume, reset: () => reset(), play_until: () => playUntil(p), set_parameters: () => setParameters(p) })[cmd]?.() });
    reset(q.get('depart'));
    return { scene, S };
  }
  window.PasAPas = PasAPas;
})();
