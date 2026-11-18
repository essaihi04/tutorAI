/*
 * LEXIQUE VISUEL COMMUN — PHYSIQUE (18 novembre 2026 ; skill simulations-au-tableau règle 15, professeur règle 43).
 * Fiches : docs/lexique-visuel/ (condensateur, bobine, resistor, generateur, interrupteur, lampe, appareils-de-mesure,
 * oscilloscope, corde, micro, onde-sonore, lumiere, grandeurs-electriques). Chaque dessin est celui qui revenait le plus
 * souvent dans les cours (copié mot pour mot, pour que les pages ne changent pas d'aspect) ; une page ne le redessine plus.
 *
 *   <script src="/media/simulations/shared/lexique/lexique-physique.js"></script>
 *   const Peint = window.Lexique.physique;          // appareils peints (contexte brut, dans craie.direct)
 *   Lexique.physique.symboleBobine(c, …)           // symboles à la craie (objet Craie)
 *   Lexique.physique.ondes.corde(ctx, pts)         // ondes : corde, perle, micro, écran d'oscilloscope, trace, front
 *   Lexique.physique.lumiere.couleurDe(λ)          // la couleur d'une radiation (une seule fonction pour tout le site)
 *   Lexique.physique.GRANDEURS.u_C                 // la couleur de craie d'une grandeur (voir plus bas)
 */
(function () {
  'use strict';
  window.Lexique = window.Lexique || {};
  if (window.Lexique.physique) return;
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));

  /* ── Appareils et composants peints (règle 32 : ils ressemblent aux vrais ; le peint ne change jamais la physique) ── */
  const Peint = {
    /** Sphère ombrée (électron : bleu). */
    sphere(ctx, x, y, r, [clair, milieu, sombre] = ['#e3f3ff', '#3b9cff', '#0a3a8c'], a = 1) {
      ctx.save(); ctx.globalAlpha = a;
      const g = ctx.createRadialGradient(x - r * .35, y - r * .4, r * .1, x, y, r); g.addColorStop(0, clair); g.addColorStop(.45, milieu); g.addColorStop(1, sombre);
      ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.fill(); ctx.restore();
    },
    /** Borne ronde (rouge ou noire). */
    borne(ctx, x, y, rouge, a = 1) { Peint.sphere(ctx, x, y, 5, rouge ? ['#ffd0d0', '#e0393e', '#6d0f12'] : ['#9aa0a6', '#2b2f33', '#050607'], a); },
    plot(ctx, x, y, a = 1) { Peint.sphere(ctx, x, y, 4.6, ['#fff1c9', '#cfa046', '#5e4210'], a); },
    /** Boîtier d’un générateur (vu de face) : coffret gris, afficheur, deux bornes (rouge +, noire −). */
    generateur(ctx, x, y, w, h, affiche, a = 1) {
      ctx.save(); ctx.globalAlpha = a;
      ctx.fillStyle = 'rgba(0,0,0,.3)'; ctx.beginPath(); ctx.roundRect(x + 3, y + 4, w, h, 7); ctx.fill();
      const g = ctx.createLinearGradient(x, y, x + w, y + h); g.addColorStop(0, '#5b6670'); g.addColorStop(.5, '#3b444c'); g.addColorStop(1, '#262c32');
      ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(x, y, w, h, 7); ctx.fill();
      ctx.strokeStyle = 'rgba(255,255,255,.18)'; ctx.lineWidth = 1; ctx.stroke();
      const ex = x + w * .14, ey = y + h * .3, ew = w * .72, eh = h * .26;
      ctx.fillStyle = '#0d1a10'; ctx.beginPath(); ctx.roundRect(ex, ey, ew, eh, 3); ctx.fill();
      ctx.fillStyle = '#7dfc8a'; ctx.font = `600 ${Math.round(eh * .72)}px monospace`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      ctx.fillText(affiche, ex + ew / 2, ey + eh / 2 + 1);
      ctx.restore();
    },
    /** Appareil à cadran (ampèremètre ou voltmètre) : boîtier, cadran crème, graduations, aiguille (f de 0 à 1). */
    cadran(ctx, cx, cy, r, f, lettre, graduations = null, a = 1) {
      ctx.save(); ctx.globalAlpha = a;
      ctx.fillStyle = 'rgba(0,0,0,.3)'; ctx.beginPath(); ctx.roundRect(cx - r - 4 + 3, cy - r - 4 + 4, 2 * r + 8, 2 * r + 8, 9); ctx.fill();
      const g = ctx.createLinearGradient(cx - r, cy - r, cx + r, cy + r); g.addColorStop(0, '#3a3f45'); g.addColorStop(1, '#1b1e22');
      ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(cx - r - 4, cy - r - 4, 2 * r + 8, 2 * r + 8, 9); ctx.fill();
      const f2 = ctx.createRadialGradient(cx - r * .3, cy - r * .4, r * .1, cx, cy, r); f2.addColorStop(0, '#fffaf0'); f2.addColorStop(1, '#e4dcc8');
      ctx.fillStyle = f2; ctx.beginPath(); ctx.roundRect(cx - r, cy - r, 2 * r, 2 * r * .92, 6); ctx.fill();
      const px = cx, py = cy + r * .55, R = r * 1.05, a0 = -Math.PI * .78, a1 = -Math.PI * .22;
      ctx.strokeStyle = '#333'; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.arc(px, py, R * .82, a0, a1); ctx.stroke();
      const n = graduations ? graduations.length - 1 : 10;
      for (let i = 0; i <= n * 2; i++) {
        const an = a0 + (a1 - a0) * i / (n * 2), l = i % 2 ? .07 : .13;
        ctx.beginPath(); ctx.moveTo(px + Math.cos(an) * R * .82, py + Math.sin(an) * R * .82); ctx.lineTo(px + Math.cos(an) * R * (.82 + l), py + Math.sin(an) * R * (.82 + l)); ctx.stroke();
      }
      ctx.fillStyle = '#c0392b'; ctx.beginPath(); ctx.arc(px + Math.cos(a1) * R * .86, py + Math.sin(a1) * R * .86, 1.6, 0, 7); ctx.fill();
      if (graduations) {
        ctx.fillStyle = '#333'; ctx.font = `${Math.round(r * .2)}px sans-serif`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
        graduations.forEach((s, i) => { const an = a0 + (a1 - a0) * i / n; ctx.fillText(s, px + Math.cos(an) * R * 1.08, py + Math.sin(an) * R * 1.08 + 1); });
      }
      ctx.fillStyle = '#222'; ctx.font = `700 ${Math.round(r * .42)}px serif`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      ctx.fillText(lettre, cx, cy + r * .38);
      const an = a0 + (a1 - a0) * clamp(f, -.02, 1.03);
      ctx.strokeStyle = '#111'; ctx.lineWidth = 1.6; ctx.beginPath(); ctx.moveTo(px, py); ctx.lineTo(px + Math.cos(an) * R * .9, py + Math.sin(an) * R * .9); ctx.stroke();
      ctx.fillStyle = '#111'; ctx.beginPath(); ctx.arc(px, py, 2.6, 0, 7); ctx.fill();
      // Verre : un reflet léger (pour l’œil seulement).
      ctx.fillStyle = 'rgba(255,255,255,.18)'; ctx.beginPath(); ctx.ellipse(cx - r * .35, cy - r * .55, r * .5, r * .16, -.3, 0, 7); ctx.fill();
      ctx.restore();
    },
    /** Condensateur chimique bleu (vu de côté, debout) avec ses deux pattes ; bande claire « − ». */
    chimique(ctx, x, y, w, h, a = 1) {
      ctx.save(); ctx.globalAlpha = a;
      ctx.strokeStyle = '#b8bec6'; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(x + w * .32, y + h); ctx.lineTo(x + w * .32, y + h + 14); ctx.moveTo(x + w * .68, y + h); ctx.lineTo(x + w * .68, y + h + 18); ctx.stroke();
      const g = ctx.createLinearGradient(x, 0, x + w, 0); g.addColorStop(0, '#0b2a6b'); g.addColorStop(.35, '#2f6fe0'); g.addColorStop(.6, '#1d4fb8'); g.addColorStop(1, '#091f52');
      ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(x, y, w, h, [w * .25, w * .25, 4, 4]); ctx.fill();
      ctx.fillStyle = 'rgba(210,225,255,.75)'; ctx.fillRect(x + w * .7, y + 4, w * .16, h - 8);
      ctx.fillStyle = '#0b2a6b'; for (let k = 0; k < 3; k++) ctx.fillRect(x + w * .74, y + 10 + k * (h - 20) / 3, w * .08, 2.4);
      ctx.fillStyle = '#9aa3ad'; ctx.beginPath(); ctx.ellipse(x + w / 2, y + 3, w / 2 - 1, 3.2, 0, 0, 7); ctx.fill();
      ctx.restore();
    },
    /** Armatures métalliques sous le symbole du condensateur ; f (0 → 1) : part de la charge finale, montrée par des charges
     * rouges (+) sur l'armature du haut et bleues (−) sur celle du bas, qui apparaissent une à une en fondu. */
    armatures(ctx, x, yA, yB, f, a = 1) {
      ctx.save(); ctx.globalAlpha = a;
      for (const y of [yA, yB]) {
        ctx.fillStyle = 'rgba(0,0,0,.3)'; ctx.fillRect(x - 25, y - 1, 52, 6);
        const g = ctx.createLinearGradient(0, y - 3, 0, y + 3); g.addColorStop(0, '#f1f5f9'); g.addColorStop(.5, '#94a3b8'); g.addColorStop(1, '#475569');
        ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(x - 26, y - 3, 52, 6, 2); ctx.fill();
      }
      ctx.restore();
      const n = 6, nr = n * Math.min(1, f);
      for (let k = 0; k < Math.ceil(nr - 1e-6); k++) {
        const al = a * Math.min(1, nr - k), xx = x + [-22, -15, -8, 8, 15, 22][k];   // un passage au milieu pour le fil
        Peint.sphere(ctx, xx, yA - 8, 3.4, ['#ffd0d0', '#ef4444', '#7f1d1d'], al);
        Peint.sphere(ctx, xx, yB + 8, 3.4, ['#dbeafe', '#3b82f6', '#1e3a8a'], al);
      }
    },
    /** Résistor : corps beige en cylindre, bandes de couleur lues sur la valeur (Ω). */
    resistor(ctx, x, y, w, h, ohm, a = 1) {
      const COUL = ['#111', '#7b4a1e', '#d32f2f', '#f57c00', '#fbc02d', '#2e7d32', '#1565c0', '#7b1fa2', '#9e9e9e', '#fafafa'];
      const e = Math.floor(Math.log10(ohm) + 1e-9) - 1, m = Math.round(ohm / 10 ** e), d1 = Math.floor(m / 10) % 10, d2 = m % 10;
      ctx.save(); ctx.globalAlpha = a;
      const g = ctx.createLinearGradient(0, y, 0, y + h); g.addColorStop(0, '#f3e1bf'); g.addColorStop(.45, '#d9bf8f'); g.addColorStop(1, '#9c8358');
      ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(x, y, w, h, h / 2.2); ctx.fill();
      [[.24, d1], [.38, d2], [.52, clamp(e, 0, 9)], [.78, -1]].forEach(([f, k]) => {
        ctx.fillStyle = k < 0 ? '#c9a227' : COUL[k]; ctx.fillRect(x + w * f, y + 1, w * .07, h - 2);
      });
      ctx.fillStyle = 'rgba(255,255,255,.35)'; ctx.fillRect(x + h * .3, y + h * .18, w - h * .6, h * .12);
      ctx.restore();
    },
    /** Interrupteur : socle sombre, plots laiton, levier métallique (pivot → bout). */
    levier(ctx, px, py, bx, by, a = 1) {
      ctx.save(); ctx.globalAlpha = a; ctx.lineCap = 'round';
      ctx.strokeStyle = '#4a4f55'; ctx.lineWidth = 6; ctx.beginPath(); ctx.moveTo(px, py); ctx.lineTo(bx, by); ctx.stroke();
      ctx.strokeStyle = '#c8ccd2'; ctx.lineWidth = 3.4; ctx.beginPath(); ctx.moveTo(px, py); ctx.lineTo(bx, by); ctx.stroke();
      ctx.strokeStyle = 'rgba(255,255,255,.7)'; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(px, py - 1); ctx.lineTo(bx, by - 1); ctx.stroke();
      Peint.sphere(ctx, bx, by, 4.2, ['#ffe9c2', '#c98a2a', '#5a3a08']);
      ctx.restore();
    },
    /**
     * Bobine couchée : mandrin clair (deux joues) et fil de cuivre enroulé en spires orangées.
     * Renvoie les deux bornes (bout des fils de sortie, sous les joues). Le noyau se peint AVANT (il passe dans le mandrin).
     */
    bobine(ctx, x, y, w, h, a = 1) {
      const j = Math.max(6, h * .2), n = Math.max(7, Math.round((w - 2 * j) / 6.5));
      ctx.save(); ctx.globalAlpha = a;
      ctx.fillStyle = 'rgba(0,0,0,.28)'; ctx.beginPath(); ctx.ellipse(x + w / 2 + 3, y + h + 9, w / 2, 4.5, 0, 0, 7); ctx.fill();
      // Fils de sortie (cuivre nu) : de chaque joue vers le bas.
      ctx.strokeStyle = '#d98a3d'; ctx.lineWidth = 2; ctx.lineCap = 'round';
      ctx.beginPath(); ctx.moveTo(x + j + 3, y + h - 3); ctx.quadraticCurveTo(x + j - 2, y + h + 8, x + j * .5, y + h + 14);
      ctx.moveTo(x + w - j - 3, y + h - 3); ctx.quadraticCurveTo(x + w - j + 2, y + h + 8, x + w - j * .5, y + h + 14); ctx.stroke();
      // Enroulement : cylindre de cuivre (clair au milieu, sombre aux bords).
      const g = ctx.createLinearGradient(0, y + 3, 0, y + h - 3);
      g.addColorStop(0, '#4a2207'); g.addColorStop(.22, '#b8621f'); g.addColorStop(.45, '#ffbe7a'); g.addColorStop(.62, '#d9802f'); g.addColorStop(1, '#3d1b05');
      ctx.fillStyle = g; ctx.fillRect(x + j, y + 3, w - 2 * j, h - 6);
      // Les spires : un trait sombre légèrement penché, puis un reflet.
      const pas = (w - 2 * j) / n;
      for (let k = 0; k <= n; k++) {
        const sx = x + j + k * pas;
        ctx.strokeStyle = 'rgba(60,25,5,.75)'; ctx.lineWidth = 1.1; ctx.beginPath(); ctx.moveTo(sx, y + 3); ctx.lineTo(sx + pas * .35, y + h - 3); ctx.stroke();
        ctx.strokeStyle = 'rgba(255,225,180,.35)'; ctx.lineWidth = .8; ctx.beginPath(); ctx.moveTo(sx + pas * .45, y + h * .3); ctx.lineTo(sx + pas * .55, y + h * .55); ctx.stroke();
      }
      // Joues du mandrin (plastique clair), avec le trou du mandrin au milieu.
      for (const jx of [x, x + w - j]) {
        const gj = ctx.createLinearGradient(jx, 0, jx + j, 0); gj.addColorStop(0, '#9c9378'); gj.addColorStop(.5, '#e8dfc4'); gj.addColorStop(1, '#a89e82');
        ctx.fillStyle = gj; ctx.beginPath(); ctx.roundRect(jx, y - 4, j, h + 8, 3); ctx.fill();
      }
      ctx.fillStyle = 'rgba(20,20,20,.55)'; ctx.beginPath(); ctx.ellipse(x + w - j / 2, y + h / 2, j * .32, h * .22, 0, 0, 7); ctx.fill();
      ctx.restore();
      return [[x + j * .5, y + h + 14], [x + w - j * .5, y + h + 14]];
    },
    /** Noyau de fer doux : barre grise (dégradé métallique). */
    noyau(ctx, x, y, w, h, a = 1) {
      ctx.save(); ctx.globalAlpha = a;
      ctx.fillStyle = 'rgba(0,0,0,.25)'; ctx.fillRect(x + 3, y + 4, w, h);
      const g = ctx.createLinearGradient(0, y, 0, y + h); g.addColorStop(0, '#5d646b'); g.addColorStop(.35, '#c9cfd4'); g.addColorStop(.6, '#8b9298'); g.addColorStop(1, '#3a3f44');
      ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(x, y, w, h, 2); ctx.fill();
      ctx.strokeStyle = 'rgba(255,255,255,.18)'; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(x + 3, y + h * .3); ctx.lineTo(x + w - 3, y + h * .3); ctx.stroke();
      ctx.restore();
    },
    /**
     * Lampe à incandescence sur son support : socle sombre, deux bornes (à gauche et à droite, à la hauteur `yf` du fil),
     * culot, ampoule de verre ; `eclat` de 0 à 1 (∝ i²) : filament qui rougit puis blanchit, halo.
     */
    lampe(ctx, cx, yf, eclat = 0, a = 1) {
      const e = clamp(eclat, 0, 1), gy = yf - 30, R = 14;
      ctx.save(); ctx.globalAlpha = a;
      if (e > .01) {
        const h = ctx.createRadialGradient(cx, gy, 2, cx, gy, R + 50 * Math.sqrt(e));
        h.addColorStop(0, `rgba(255,236,160,${.75 * e})`); h.addColorStop(.35, `rgba(255,214,110,${.32 * e})`); h.addColorStop(1, 'rgba(255,200,90,0)');
        ctx.fillStyle = h; ctx.beginPath(); ctx.arc(cx, gy, R + 50 * Math.sqrt(e), 0, 7); ctx.fill();
      }
      // Socle et bornes.
      const gs = ctx.createLinearGradient(0, yf - 9, 0, yf + 9); gs.addColorStop(0, '#4a5058'); gs.addColorStop(1, '#1d2125');
      ctx.fillStyle = gs; ctx.beginPath(); ctx.roundRect(cx - 21, yf - 8, 42, 16, 4); ctx.fill();
      Peint.plot(ctx, cx - 21, yf, a); Peint.plot(ctx, cx + 21, yf, a);
      // Culot vissé.
      const gc = ctx.createLinearGradient(cx - 7, 0, cx + 7, 0); gc.addColorStop(0, '#7d7a6e'); gc.addColorStop(.5, '#e4e0d0'); gc.addColorStop(1, '#6c695e');
      ctx.fillStyle = gc; ctx.fillRect(cx - 7, yf - 19, 14, 11);
      ctx.strokeStyle = 'rgba(40,40,40,.5)'; ctx.lineWidth = 1; for (let k = 0; k < 3; k++) { ctx.beginPath(); ctx.moveTo(cx - 7, yf - 17 + k * 3.5); ctx.lineTo(cx + 7, yf - 15.5 + k * 3.5); ctx.stroke(); }
      // Ampoule de verre (plus chaude quand elle brille).
      const gv = ctx.createRadialGradient(cx - 4, gy - 5, 1, cx, gy, R);
      gv.addColorStop(0, `rgba(255,255,255,${.55 + .4 * e})`); gv.addColorStop(.6, `rgba(${200 + 55 * e},${215 + 30 * e},${230 - 70 * e},${.18 + .55 * e})`); gv.addColorStop(1, `rgba(190,205,220,${.28 + .4 * e})`);
      ctx.fillStyle = gv; ctx.beginPath(); ctx.arc(cx, gy, R, 0, 7); ctx.fill();
      ctx.strokeStyle = 'rgba(230,240,255,.55)'; ctx.lineWidth = 1; ctx.stroke();
      // Filament : sombre éteint, rouge puis blanc-jaune.
      const f = e < .3 ? [120 + 400 * e, 70 + 100 * e, 60] : [255, 150 + 105 * Math.min(1, (e - .3) / .7), 60 + 150 * Math.min(1, (e - .3) / .7)];
      ctx.strokeStyle = `rgb(${f.map(Math.round).join(',')})`; ctx.lineWidth = 1.3 + e;
      if (e > .05) { ctx.shadowColor = 'rgba(255,230,150,.9)'; ctx.shadowBlur = 10 * e; }
      ctx.beginPath(); ctx.moveTo(cx - 5, yf - 19); ctx.lineTo(cx - 5, gy + 2);
      for (let k = 0; k <= 6; k++) ctx.lineTo(cx - 5 + k * 10 / 6, gy + (k % 2 ? -3 : 2));
      ctx.lineTo(cx + 5, yf - 19); ctx.stroke(); ctx.shadowBlur = 0;
      ctx.fillStyle = 'rgba(255,255,255,.4)'; ctx.beginPath(); ctx.ellipse(cx - 5, gy - 7, 3.5, 2, -.6, 0, 7); ctx.fill();
      ctx.restore();
    },
    /** Oscilloscope : coffret, écran vert sombre quadrillé (rect `e`), boutons ; prises voie 1, voie 2 et masse (liste de points). */
    oscillo(ctx, x, y, w, h, e, prises, a = 1) {
      ctx.save(); ctx.globalAlpha = a;
      ctx.fillStyle = 'rgba(0,0,0,.35)'; ctx.beginPath(); ctx.roundRect(x + 4, y + 5, w, h, 12); ctx.fill();
      const g = ctx.createLinearGradient(x, y, x + w, y + h); g.addColorStop(0, '#59636d'); g.addColorStop(.5, '#3a424a'); g.addColorStop(1, '#23292f');
      ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(x, y, w, h, 12); ctx.fill();
      ctx.strokeStyle = 'rgba(255,255,255,.16)'; ctx.lineWidth = 1; ctx.stroke();
      const ge = ctx.createRadialGradient(e.x + e.w / 2, e.y + e.h / 2, 10, e.x + e.w / 2, e.y + e.h / 2, e.w * .7);
      ge.addColorStop(0, '#0d3a22'); ge.addColorStop(1, '#03160c');
      ctx.fillStyle = ge; ctx.beginPath(); ctx.roundRect(e.x, e.y, e.w, e.h, 6); ctx.fill();
      ctx.strokeStyle = '#1b2228'; ctx.lineWidth = 3; ctx.stroke();
      ctx.strokeStyle = 'rgba(120,255,170,.09)'; ctx.lineWidth = 1;   // quadrillage de l’écran (pour l’œil)
      for (let k = 1; k < 10; k++) { const gx = e.x + k * e.w / 10; ctx.beginPath(); ctx.moveTo(gx, e.y + 3); ctx.lineTo(gx, e.y + e.h - 3); ctx.stroke(); }
      for (let k = 1; k < 8; k++) { const gy = e.y + k * e.h / 8; ctx.beginPath(); ctx.moveTo(e.x + 3, gy); ctx.lineTo(e.x + e.w - 3, gy); ctx.stroke(); }
      for (const [px, py, noire] of prises) {
        Peint.sphere(ctx, px, py, 6.5, noire ? ['#9aa0a6', '#2b2f33', '#050607'] : ['#fff3c4', '#d8a92e', '#5b4108']);
        ctx.fillStyle = '#111'; ctx.beginPath(); ctx.arc(px, py, 2.2, 0, 7); ctx.fill();
      }
      ctx.restore();
    },
    /** Ohmmètre numérique : coque jaune, afficheur à cristaux liquides, sélecteur, prises Ω (rouge) et COM (noire). */
    ohmmetre(ctx, x, y, w, h, affiche, a = 1) {
      ctx.save(); ctx.globalAlpha = a;
      ctx.fillStyle = 'rgba(0,0,0,.3)'; ctx.beginPath(); ctx.roundRect(x + 4, y + 5, w, h, 12); ctx.fill();
      const g = ctx.createLinearGradient(x, y, x + w, y + h); g.addColorStop(0, '#f6c84a'); g.addColorStop(1, '#b8861a');
      ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(x, y, w, h, 12); ctx.fill();
      ctx.fillStyle = '#2a2d31'; ctx.beginPath(); ctx.roundRect(x + 7, y + 7, w - 14, h - 14, 8); ctx.fill();
      const lx = x + 14, ly = y + 15, lw = w - 28, lh = h * .26;
      const gl = ctx.createLinearGradient(0, ly, 0, ly + lh); gl.addColorStop(0, '#c9d3c0'); gl.addColorStop(1, '#a9b49e');
      ctx.fillStyle = gl; ctx.beginPath(); ctx.roundRect(lx, ly, lw, lh, 3); ctx.fill();
      ctx.fillStyle = '#1b1f1a'; ctx.font = `600 ${Math.round(lh * .62)}px monospace`; ctx.textAlign = 'right'; ctx.textBaseline = 'middle';
      ctx.fillText(affiche, lx + lw - 8, ly + lh / 2 + 1);
      // Sélecteur rotatif (sur Ω).
      const sx = x + w / 2, sy = y + h * .6, sr = w * .17;
      Peint.sphere(ctx, sx, sy, sr, ['#9aa0a6', '#3a3f45', '#0d0f11']);
      ctx.strokeStyle = '#e8e8e8'; ctx.lineWidth = 2.4; ctx.beginPath(); ctx.moveTo(sx, sy); ctx.lineTo(sx + sr * .8 * Math.cos(-2.2), sy + sr * .8 * Math.sin(-2.2)); ctx.stroke();
      ctx.fillStyle = '#e8e8e8'; ctx.font = `700 ${Math.round(w * .12)}px serif`; ctx.textAlign = 'center';
      ctx.fillText('Ω', sx + sr * 1.55 * Math.cos(-2.2), sy + sr * 1.55 * Math.sin(-2.2));
      // Prises.
      const py = y + h - 20;
      Peint.sphere(ctx, x + w * .3, py, 6, ['#9aa0a6', '#2b2f33', '#050607']); Peint.sphere(ctx, x + w * .7, py, 6, ['#ffd0d0', '#e0393e', '#6d0f12']);
      ctx.restore();
      return [[x + w * .3, py], [x + w * .7, py]];
    },
    /** Cordon souple peint (rouge ou noir) entre deux points, qui pend un peu. */
    cordon(ctx, x1, y1, x2, y2, rouge, pend = 30, a = 1) {
      ctx.save(); ctx.globalAlpha = a; ctx.lineCap = 'round';
      const mx = (x1 + x2) / 2, my = Math.max(y1, y2) + pend;
      ctx.strokeStyle = rouge ? '#7a1418' : '#050607'; ctx.lineWidth = 4.2; ctx.beginPath(); ctx.moveTo(x1, y1); ctx.quadraticCurveTo(mx, my, x2, y2); ctx.stroke();
      ctx.strokeStyle = rouge ? '#e0393e' : '#3b4045'; ctx.lineWidth = 2.4; ctx.beginPath(); ctx.moveTo(x1, y1); ctx.quadraticCurveTo(mx, my, x2, y2); ctx.stroke();
      ctx.restore();
    },
    /** GBF : coffret, petit écran où défile un signal triangulaire, deux boutons, bornes de sortie. */
    gbf(ctx, x, y, w, h, a = 1) {
      ctx.save(); ctx.globalAlpha = a;
      ctx.fillStyle = 'rgba(0,0,0,.3)'; ctx.beginPath(); ctx.roundRect(x + 3, y + 4, w, h, 7); ctx.fill();
      const g = ctx.createLinearGradient(x, y, x + w, y + h); g.addColorStop(0, '#4f6a86'); g.addColorStop(.5, '#34495f'); g.addColorStop(1, '#202e3c');
      ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(x, y, w, h, 7); ctx.fill();
      ctx.strokeStyle = 'rgba(255,255,255,.18)'; ctx.lineWidth = 1; ctx.stroke();
      const ex = x + 8, ey = y + 8, ew = w * .55, eh = h * .42;
      ctx.fillStyle = '#0d1a10'; ctx.beginPath(); ctx.roundRect(ex, ey, ew, eh, 3); ctx.fill();
      ctx.strokeStyle = '#7dfc8a'; ctx.lineWidth = 1.4; ctx.beginPath();
      for (let k = 0; k <= 4; k++) { const px = ex + 4 + k * (ew - 8) / 4, py = k % 2 ? ey + 5 : ey + eh - 5; if (k) ctx.lineTo(px, py); else ctx.moveTo(px, py); }
      ctx.stroke();
      Peint.sphere(ctx, x + w * .82, y + h * .25, Math.min(9, w * .09), ['#cfd4d9', '#59616a', '#14181c']);
      Peint.sphere(ctx, x + w * .82, y + h * .58, Math.min(7, w * .07), ['#cfd4d9', '#59616a', '#14181c']);
      ctx.restore();
    },
    /** Boîte « G » (générateur d’entretien) : boîtier sombre, plaque « G », deux bornes ; son fonctionnement interne n’est pas montré. */
    boiteG(ctx, x, y, w, h, a = 1) {
      ctx.save(); ctx.globalAlpha = a;
      ctx.fillStyle = 'rgba(0,0,0,.3)'; ctx.beginPath(); ctx.roundRect(x + 3, y + 4, w, h, 7); ctx.fill();
      const g = ctx.createLinearGradient(x, y, x + w, y + h); g.addColorStop(0, '#6b5a86'); g.addColorStop(.5, '#4a3d63'); g.addColorStop(1, '#2c2440');
      ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(x, y, w, h, 7); ctx.fill();
      ctx.strokeStyle = 'rgba(255,255,255,.2)'; ctx.lineWidth = 1; ctx.stroke();
      ctx.fillStyle = '#efe6ff'; ctx.font = `700 ${Math.round(h * .55)}px serif`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      ctx.fillText('G', x + w / 2, y + h / 2 + 1);
      Peint.borne(ctx, x, y + h / 2, true, a); Peint.borne(ctx, x + w, y + h / 2, false, a);
      ctx.restore();
    }
  };

  /* ── Symboles normalisés, à la craie (objet Craie du kit shared/tableau) ── */
  /** Symbole de la bobine à la craie, couché entre (x1, y) et (x2, y) : fils, puis créneaux arrondis (boucles). */
  function symboleBobine(c, x1, y, x2, o = {}) {
    const n = o.n ?? 4, larg = o.largeur ?? 80, xa = (x1 + x2) / 2 - larg / 2, xb = xa + larg, h = o.h ?? 16, coul = o.couleur ?? 'blanc';
    c.ligne(x1, y, xa, y, { largeur: 2, couleur: o.fil ?? 'blanc' });
    c.courbe(u => { const k = u * n, f = k - Math.floor(k), xx = xa + u * larg; return [xx, y - Math.sin(Math.min(1, f) * Math.PI) * h]; }, n * 14, { net: false, couleur: coul, largeur: 2.4 });
    c.ligne(xb, y, x2, y, { largeur: 2, couleur: o.fil ?? 'blanc' });
    return [xa, xb];
  }
  /** Le même symbole, debout entre (x, y1) en haut et (x, y2) en bas (boucles vers la droite). */
  function symboleBobineV(c, x, y1, y2, o = {}) {
    const n = o.n ?? 4, haut = o.hauteur ?? 76, ya = (y1 + y2) / 2 - haut / 2, yb = ya + haut, h = o.h ?? 15, coul = o.couleur ?? 'blanc';
    c.ligne(x, y1, x, ya, { largeur: 2 });
    c.courbe(u => { const k = u * n, f = k - Math.floor(k); return [x + Math.sin(Math.min(1, f) * Math.PI) * h, ya + u * haut]; }, n * 14, { net: false, couleur: coul, largeur: 2.4 });
    c.ligne(x, yb, x, y2, { largeur: 2 });
    return [ya, yb];
  }
  function symboleCondo(c, x, y1, yA, yB, y2, larg = 40, o = {}) {
    c.ligne(x, y1, x, yA, { largeur: 2 });
    c.ligne(x - larg / 2, yA, x + larg / 2, yA, { largeur: 3.4, couleur: o.couleur ?? 'blanc' });
    c.ligne(x - larg / 2, yB, x + larg / 2, yB, { largeur: 3.4, couleur: o.couleur ?? 'blanc' });
    c.ligne(x, yB, x, y2, { largeur: 2 });
  }
  function rgbDe(l) {
    let r = 0, g = 0, b = 0;
    if (l < 440) { r = Math.max(0, (440 - l) / 60); b = 1; }
    else if (l < 490) { g = (l - 440) / 50; b = 1; }
    else if (l < 510) { g = 1; b = (510 - l) / 20; }
    else if (l < 580) { r = (l - 510) / 70; g = 1; }
    else if (l < 645) { r = 1; g = (645 - l) / 65; }
    else r = 1;
    let k = 0;
    if (l >= 400 && l < 425) k = 0.35 + 0.65 * (l - 400) / 25;
    else if (l >= 425 && l <= 700) k = 1;
    else if (l > 700 && l <= 800) k = 1 - 0.7 * (l - 700) / 100;
    return { r: r ** 0.8, g: g ** 0.8, b: b ** 0.8, k };
  }
  function couleurDe(l, alpha = 1, blanc = 0) {
    const c = rgbDe(l), k = blanc ? 1 : c.k, m = v => Math.round(255 * ((v * k) * (1 - blanc) + blanc));
    return `rgba(${m(c.r)},${m(c.g)},${m(c.b)},${alpha})`;
  }
  function nomCouleur(l) {
    if (l < 400) return null; if (l > 800) return null;
    if (l < 445) return 'violet'; if (l < 490) return 'bleu'; if (l < 570) return 'vert';
    if (l < 590) return 'jaune'; if (l < 620) return 'orange'; return 'rouge';
  }

  /* ── Ondes : objets peints (corde de chanvre, perles, micro, écran d'oscilloscope, trace lumineuse, front sonore) ── */
  const O = {

    lin(ctx, x0, y0, x1, y1, arrets) { const g = ctx.createLinearGradient(x0, y0, x1, y1); arrets.forEach(([o, c]) => g.addColorStop(o, c)); return g; },
    rr(ctx, x, y, w, h, r) { ctx.beginPath(); if (ctx.roundRect) ctx.roundRect(x, y, w, h, r); else ctx.rect(x, y, w, h); },
    /** Corde de chanvre éclairée par le haut, passant par `pts` ([[x,y],…]), avec son ombre portée. */
    corde(ctx, pts, w = 5.5, alpha = 1) {
      const chemin = (dx, dy) => { ctx.beginPath(); pts.forEach(([px, py], i) => (i ? ctx.lineTo(px + dx, py + dy) : ctx.moveTo(px + dx, py + dy))); };
      ctx.save(); ctx.globalAlpha = alpha; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
      chemin(2, 6); ctx.strokeStyle = 'rgba(0,0,0,.28)'; ctx.lineWidth = w + 2; ctx.stroke();
      chemin(0, 1); ctx.strokeStyle = '#6b4521'; ctx.lineWidth = w; ctx.stroke();
      chemin(0, -.4); ctx.strokeStyle = '#c99a5b'; ctx.lineWidth = w - 1.8; ctx.stroke();
      chemin(0, 0); ctx.setLineDash([2, 4]); ctx.strokeStyle = 'rgba(92,58,26,.55)'; ctx.lineWidth = w - 2.4; ctx.stroke(); ctx.setLineDash([]);
      chemin(0, -w * .3); ctx.strokeStyle = 'rgba(255,238,205,.78)'; ctx.lineWidth = 1.1; ctx.stroke();
      ctx.restore();
    },
    /** Perle (sphère ombrée) : orange, jaune, rouge, violet, cyan. */
    perle(ctx, x, y, r, teinte = 'orange') {
      const T = { orange: ['#ffe2c2', '#f97316', '#7c2d12'], jaune: ['#fff7c2', '#facc15', '#854d0e'], rouge: ['#ffd5cc', '#ef4444', '#7f1d1d'],
        violet: ['#ede9fe', '#8b5cf6', '#3b1d7a'], cyan: ['#e0fbff', '#22d3ee', '#155e75'], gris: ['#f1f5f9', '#94a3b8', '#334155'] }[teinte] || ['#ffe2c2', '#f97316', '#7c2d12'];
      ctx.save();
      ctx.fillStyle = 'rgba(0,0,0,.3)'; ctx.beginPath(); ctx.ellipse(x + 2, y + 5, r, r * .7, 0, 0, Math.PI * 2); ctx.fill();
      const g = ctx.createRadialGradient(x - r * .35, y - r * .4, r * .1, x, y, r);
      g.addColorStop(0, T[0]); g.addColorStop(.45, T[1]); g.addColorStop(1, T[2]);
      ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = 'rgba(255,255,255,.7)'; ctx.beginPath(); ctx.ellipse(x - r * .38, y - r * .42, r * .22, r * .14, -.6, 0, Math.PI * 2); ctx.fill();
      ctx.restore();
    },
    /** Poignée en bois tenue en S : elle monte et descend avec le bout de la corde (y). */
    poignee(ctx, x, y) {
      const w = 13, h = 46;
      ctx.save();
      ctx.fillStyle = 'rgba(0,0,0,.3)'; O.rr(ctx, x - w / 2 + 3, y - h / 2 + 5, w, h, 6); ctx.fill();
      ctx.fillStyle = O.lin(ctx, x - w / 2, 0, x + w / 2, 0, [[0, '#5a3216'], [.35, '#c8894a'], [.6, '#b0733b'], [1, '#4a2810']]);
      O.rr(ctx, x - w / 2, y - h / 2, w, h, 6); ctx.fill();
      ctx.strokeStyle = 'rgba(70,35,10,.4)'; ctx.lineWidth = .7;
      for (const d of [-2.5, 1, 3.5]) { ctx.beginPath(); ctx.moveTo(x + d, y - h / 2 + 5); ctx.quadraticCurveTo(x + d + 1, y, x + d - .5, y + h / 2 - 5); ctx.stroke(); }
      ctx.fillStyle = O.lin(ctx, x - w / 2, 0, x + w / 2, 0, [[0, '#4b5563'], [.5, '#e5e7eb'], [1, '#4b5563']]);   // bague de serrage de la corde
      ctx.fillRect(x - w / 2 - 1, y - 3.5, w + 2, 7);
      ctx.restore();
    },
    /** Micro sur pied : grille noire, bague métallique, pied ; `teinte` = couleur de la bague (repère de voie). */
    micro(ctx, x0, y0, teinte = '#22d3ee', k = 1.25) {
      const x = 0, y = 0;
      ctx.save(); ctx.translate(x0, y0); ctx.scale(k, k);
      ctx.fillStyle = 'rgba(0,0,0,.3)'; ctx.beginPath(); ctx.ellipse(x + 2, y + 38, 15, 4, 0, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = O.lin(ctx, x - 2, 0, x + 2, 0, [[0, '#4b5563'], [.5, '#e5e7eb'], [1, '#4b5563']]); ctx.fillRect(x - 2, y + 10, 4, 26);
      ctx.fillStyle = O.lin(ctx, 0, y + 33, 0, y + 38, [[0, '#9ca3af'], [1, '#1f2937']]); O.rr(ctx, x - 13, y + 33, 26, 5, 2.5); ctx.fill();
      ctx.fillStyle = O.lin(ctx, x - 6, 0, x + 6, 0, [[0, '#1f2937'], [.5, '#6b7280'], [1, '#111827']]); O.rr(ctx, x - 5.5, y + 4, 11, 10, 2); ctx.fill();
      ctx.fillStyle = teinte; ctx.fillRect(x - 5.5, y + 7, 11, 2.5);
      const g = ctx.createRadialGradient(x - 3.5, y - 4, 1, x, y, 11);
      g.addColorStop(0, '#6b7280'); g.addColorStop(.6, '#1f2937'); g.addColorStop(1, '#0b0f14');
      ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y - 1, 10, 0, Math.PI * 2); ctx.fill();
      ctx.save(); ctx.beginPath(); ctx.arc(x, y - 1, 10, 0, Math.PI * 2); ctx.clip(); ctx.strokeStyle = 'rgba(160,170,180,.35)'; ctx.lineWidth = .6;
      for (let k = -10; k <= 10; k += 3) { ctx.beginPath(); ctx.moveTo(x + k, y - 11); ctx.lineTo(x + k, y + 9); ctx.stroke(); ctx.beginPath(); ctx.moveTo(x - 10, y - 1 + k); ctx.lineTo(x + 10, y - 1 + k); ctx.stroke(); }
      ctx.restore();
      ctx.fillStyle = 'rgba(255,255,255,.35)'; ctx.beginPath(); ctx.ellipse(x - 4, y - 5, 3, 2, -.6, 0, Math.PI * 2); ctx.fill();
      ctx.restore();
    },
    /** Oscilloscope : boîtier gris, écran vert sombre et sa grille fine (nx × ny divisions) dans (x, y, w, h). */
    oscillo(ctx, x, y, w, h, nx = 10, ny = 6) {
      const m = 9;
      ctx.save();
      ctx.fillStyle = 'rgba(0,0,0,.35)'; O.rr(ctx, x - m + 5, y - m + 7, w + 2 * m, h + 2 * m, 10); ctx.fill();
      ctx.fillStyle = O.lin(ctx, 0, y - m, 0, y + h + m, [[0, '#6b7480'], [.5, '#3b434c'], [1, '#22282e']]);
      O.rr(ctx, x - m, y - m, w + 2 * m, h + 2 * m, 10); ctx.fill();
      ctx.strokeStyle = 'rgba(255,255,255,.18)'; ctx.lineWidth = 1; ctx.stroke();
      const g = ctx.createRadialGradient(x + w / 2, y + h / 2, 10, x + w / 2, y + h / 2, Math.max(w, h) * .7);
      g.addColorStop(0, '#12382a'); g.addColorStop(1, '#06180f');
      ctx.fillStyle = g; O.rr(ctx, x, y, w, h, 5); ctx.fill();
      ctx.strokeStyle = 'rgba(134,239,172,.16)'; ctx.lineWidth = 1;
      for (let i = 1; i < nx; i++) { ctx.beginPath(); ctx.moveTo(x + i * w / nx, y); ctx.lineTo(x + i * w / nx, y + h); ctx.stroke(); }
      for (let j = 1; j < ny; j++) { ctx.beginPath(); ctx.moveTo(x, y + j * h / ny); ctx.lineTo(x + w, y + j * h / ny); ctx.stroke(); }
      ctx.fillStyle = 'rgba(255,255,255,.04)'; ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + w * .55, y); ctx.lineTo(x + w * .3, y + h); ctx.lineTo(x, y + h); ctx.fill();   // reflet de la vitre
      ctx.restore();
    },
    /** Trace lumineuse nette (sur l'écran vert ou un graphe) : un cœur clair et un halo de la couleur. */
    trace(ctx, pts, couleur, w = 2.2) {
      if (pts.length < 2) return;
      ctx.save(); ctx.lineCap = 'round'; ctx.lineJoin = 'round';
      const chemin = () => { ctx.beginPath(); pts.forEach(([px, py], i) => (i ? ctx.lineTo(px, py) : ctx.moveTo(px, py))); };
      ctx.shadowColor = couleur; ctx.shadowBlur = 8; chemin(); ctx.strokeStyle = couleur; ctx.lineWidth = w; ctx.stroke();
      ctx.shadowBlur = 0; chemin(); ctx.strokeStyle = 'rgba(255,255,255,.55)'; ctx.lineWidth = w * .35; ctx.stroke();
      ctx.restore();
    },
    /** Arc de son (ou d'ultrasons) : un front lumineux doux, centré en (x, y), de rayon r, entre les angles a0 et a1. */
    front(ctx, x, y, r, a0, a1, couleur = '250,204,21', alpha = 1) {
      if (r <= 2) return;
      ctx.save(); ctx.lineCap = 'round';
      for (const [w, a] of [[9, .12], [4.5, .3], [1.8, .9]]) { ctx.strokeStyle = `rgba(${couleur},${a * alpha})`; ctx.lineWidth = w; ctx.beginPath(); ctx.arc(x, y, r, a0, a1); ctx.stroke(); }
      ctx.restore();
    },
    };
  O.doux = u => (u <= 0 ? 0 : u >= 1 ? 1 : u * u * (3 - 2 * u));

  /*
   * Le code des couleurs des grandeurs (craie), dit par la voix des cours d'électricité (ch6 à ch8) :
   *   condensateur → ROUGE : u_C, q, E_e (énergie du condensateur) ;
   *   courant → VERT : i, u_R (= R·i, son image), E_m (énergie de la bobine, ∝ i²) ;
   *   bobine → VIOLET : u_b ; générateur et totaux → BLANC : E, u_G, E (énergie totale) ;
   *   voies d'un oscilloscope (ondes) : voie 1 CYAN, voie 2 ORANGE ; électron : bleu ciel (lexique) ; charge + rose, − bleu ciel.
   */
  const GRANDEURS = { u_C: 'rouge', q: 'rouge', E_e: 'rouge', i: 'vert', u_R: 'vert', E_m: 'vert', u_b: 'violet', u_L: 'violet',
    E: 'blanc', u_G: 'blanc', E_tot: 'blanc', voie1: 'cyan', voie2: 'orange', plus: 'rose', moins: 'bleu' };

  window.Lexique.physique = Object.assign(Peint, {
    condensateur: Peint.chimique, interrupteur: Peint.levier, appareilACadran: Peint.cadran,
    symboleBobine, symboleBobineV, symboleCondo,
    ondes: O,
    lumiere: { rgbDe, couleurDe, nomCouleur },
    GRANDEURS,
  });
})();
