/*
 * Cours de référence SVT « Consommation de la matière organique et flux d'énergie » (27 novembre 2026) —
 * socle des pages des activités 2 et 3, de la carte du voyage (glycolyse-phases, centrifugation, exao-mitochondries,
 * zoom, composition, voyage). Contrat : docs/reference-svt/ARCHITECTURE.md § 3.
 *
 *   const page = Ref2.page({
 *     id, titre, variante,
 *     moments: [[nom, duree_s, motif], …],      // DANS L'ORDRE ; l'instant d'un moment = la fin de son segment :
 *                                               // ce que dit la voix se joue PENDANT le segment, et la scène se fige dessus.
 *     dessiner(c, t, e),                         // e : voir fabriqueEnv (e.u, e.d, e.vu, e.fait, e.si, e.sx, e.tel…)
 *     phase(t, e),                               // ce que l'on voit, en une ou deux phrases (ce_qui_se_voit)
 *     cadrages: { nom: [x, y, w, h] | (u) => [x, y, w, h] },   // téléphone en paysage : la fenêtre du dessin (cadre 760 × 420)
 *                                               // montrée pendant ce segment (u : part 0..1 du segment) ; rapport w / h ≈ 2,1
 *     comptes(t, e),                             // ce que la scène allume elle-même : [{ id, n, fort }] (compter = allumer)
 *     parametres: { defaut, schema, regler(p, S, page) }, explication, texte, accroche, fini, numero });
 *
 * Ce que le socle fait pour chaque page :
 *   - ligne de temps pilotable (SVTTableau.Chrono) : start, pause, resume, reset, set_time, play_until {moment | time_s} ;
 *     ?depart=<moment> ouvre la page figée sur ce moment (tout ce qui précède est dessiné, rien de ce qui suit) ;
 *   - page PILOTÉE (jamais de lancement automatique, reset = retour figé au départ) dès qu'elle est dans une iframe
 *     (le lecteur du cours) ou que l'URL porte ?depart= ou ?demarche= ; ouverte seule, elle se joue toute seule ;
 *   - mode large : e.L (760 à 1596), e.k = L / 760, e.sx(x) étire les positions sur toute la largeur du tableau ;
 *   - téléphone en paysage (toile de moins de 640 × 290) : une CAMÉRA montre seulement la fenêtre de l'étape en cours
 *     (cadrages), agrandie pour que tout texte fasse au moins 15 px à l'écran ; elle glisse d'une étape à la suivante ;
 *   - le fil de la démarche (demarche.js, écrit par la session de l'activité 1) : window.Demarche.dessiner(c) ;
 *   - set_parameters { vitesse: 0.5..2, legendes: true | false } + les réglages de la page ;
 *   - allume / eteins (SVTTableau.Allumage), repères, ce_qui_se_voit, manifeste.
 *
 * Et quelques peintures communes aux montages (seringue, sonde, nuage : reprises de exao.html du dossier voisin, qui les
 * garde locales), la bande colorée d'une phase, le phosphate lié « P ».
 */
(function () {
  'use strict';
  const { fr, bulle, protocole } = window.Tableau;
  const { Scene, Chrono, Apparitions, Allumage, doux, mix } = window.SVTTableau;
  const QS = new URLSearchParams(location.search);
  const TAU = Math.PI * 2;
  const borne = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
  const bool = (v) => (v === true || v === 'true' || v === 1 || v === '1');
  const rgba = (c, a) => `rgba(${c[0]},${c[1]},${c[2]},${a})`;
  const LX = () => window.Lexique;

  /** La taille à laquelle un texte de `taille` est vraiment écrit (le kit ne descend pas sous 15 px à l'écran). */
  const tailleEcrite = (c, taille) => Math.max(taille, c.echelle && c.tailleMin ? c.tailleMin / c.echelle : 0);
  /** La largeur d'un texte de craie tel qu'il est écrit (indices compris). */
  function largeur(c, s, taille = 18) {
    const tt = tailleEcrite(c, taille);
    return window.Tableau.Craie.segments(String(s)).reduce((w, g) => w + c.largeurTexte(g.t, g.sub ? tt * .62 : tt), 0);
  }

  function page(o) {
    const $ = (id) => document.getElementById(id);
    const canvas = $('canvas'), bouton = $('run'), bulleEl = $('feedback');
    const M = {}, DEB = {}, MOTIFS = {}, ORDRE = [];
    let T = 0;
    for (const [nom, duree, motif] of o.moments) { DEB[nom] = +T.toFixed(2); T += duree; M[nom] = +T.toFixed(2); MOTIFS[nom] = motif || nom; ORDRE.push(nom); }
    const FIN = +(T + .5).toFixed(2);
    const S = Object.assign({ vitesse: 1, legendes: true }, (o.parametres && o.parametres.defaut) || {});
    const EMBARQUE = (() => { try { return window.parent !== window; } catch (_) { return true; } })();
    const PILOTE = QS.has('depart') || QS.has('demarche') || QS.has('pilote') || EMBARQUE;
    const instantDepart = () => { const v = QS.get('depart'); if (v == null || v === '') return 0; return v in M ? M[v] : (+v || 0); };
    /** L'étape en cours : le premier moment pas encore dépassé (figé sur un moment : ce moment). */
    const etape = (t) => ORDRE.find((n) => t <= M[n] + 1e-3) || ORDRE[ORDRE.length - 1];
    const seg = (nom, t) => borne((t - DEB[nom]) / Math.max(1e-6, M[nom] - DEB[nom]));

    const CAM = { r: null, snap: true, avant: 0 };
    function cadrage(t) { const n = etape(t); let r = o.cadrages && o.cadrages[n]; if (typeof r === 'function') r = r(seg(n, t), t); return r || [0, 0, 760, 420]; }

    let pont = null, lum = null, chrono = null, ecrit = null;
    function fabriqueEnv(c, t, L, k, tel) {
      return { c, ctx: c.ctx, t, L, k, tel, S, M, DEB, etape: etape(t),
        /** Étire une abscisse du cadre 760 sur la largeur du tableau. */
        sx: (x) => x * k,
        /** Part (0..1) du segment du moment `nom`, entre ses fractions a et b ; d : la même, adoucie. */
        u: (nom, a = 0, b = 1) => borne((seg(nom, t) - a) / Math.max(1e-6, b - a)),
        d: (nom, a = 0, b = 1) => doux(borne((seg(nom, t) - a) / Math.max(1e-6, b - a))),
        /** Le segment de `nom` a commencé (et atteint sa fraction a). Faux tant que la scène est figée sur le moment d'avant. */
        vu: (nom, a = 0) => t > DEB[nom] + 1e-3 && seg(nom, t) >= a,
        /** Le moment `nom` est atteint. */
        fait: (nom) => t >= M[nom] - 1e-3,
        /** Écrit à la craie à partir de l'instant où cela apparaît (Apparitions). */
        ecrire: (cle, fn) => ecrit.ecrire(c, cle, fn),
        /** Écrit `fn` dès la fraction a du segment de `nom`. */
        si: (nom, a, cle, fn) => { if (t > DEB[nom] + 1e-3 && seg(nom, t) >= a) { ecrit.ecrire(c, cle, fn); return true; } return false; },
        larg: (s, taille) => largeur(c, s, taille), taille: (t0) => tailleEcrite(c, t0) };
    }

    const scene = Scene(canvas, (c) => {
      scene.cadre(o.graine || 11);
      const ctx = c.ctx, W = c.W, H = c.H, t = chrono.t;
      const tel = W < 640 || H < 290;
      const L = tel ? 760 : scene.L, k = L / 760;
      let bouge = false;
      // le fil de la démarche (en haut à droite), dans le cadre entier ; au téléphone la caméra le recouvrirait : il est omis
      if (!tel && window.Demarche && window.Demarche.dessiner) { try { c.direct(() => window.Demarche.dessiner(c, scene)); } catch (e) { console.warn('[demarche]', e); } }
      ctx.save();
      if (tel) {
        const cible = cadrage(t), now = performance.now();
        if (!CAM.r || CAM.snap) { CAM.r = cible.slice(); CAM.snap = false; }
        else {
          const a = 1 - Math.exp(-Math.min(.1, (now - CAM.avant) / 1000) * 7);
          for (let i = 0; i < 4; i++) { if (Math.abs(cible[i] - CAM.r[i]) > .6) { CAM.r[i] += (cible[i] - CAM.r[i]) * a; bouge = true; } else CAM.r[i] = cible[i]; }
        }
        CAM.avant = now;
        const [x, y, w, h] = CAM.r, z = Math.min(W / w, H / h, 1.3), d = devicePixelRatio || 1;
        ctx.setTransform(d, 0, 0, d, 0, 0); ctx.translate(W / 2, H / 2); ctx.scale(z, z); ctx.translate(-(x + w / 2), -(y + h / 2));
        c.echelle = z; c.cadre = null;
        c.tailleMin = 15 / Math.min(1, Math.max(.45, Math.min(W / 900, H / 400)));   // 15 px à l'écran, même sur le petit tableau
      }
      const e = fabriqueEnv(c, t, L, k, tel);
      o.dessiner(c, t, e);
      const s0 = scene.s; if (tel) scene.s = c.echelle;            // les numéros des comptes à la taille de la caméra
      lum.lueurs(c, o.comptes ? o.comptes(t, e) : []);
      scene.s = s0;
      const fini = c.fin();
      ctx.restore();
      return fini && !bouge;
    }, { large: true });
    ecrit = Apparitions(scene);
    chrono = Chrono({ fin: () => FIN, moments: () => M, motifs: MOTIFS, bouton, bulle: bulleEl, pont: () => pont,
      depart: o.accroche || 'Observe…', reinit: () => ecrit.oublier(), saut: () => { CAM.snap = true; },
      fini: () => o.fini || 'Terminé.', debut: PILOTE ? instantDepart : undefined });
    scene.avancer = (dt) => chrono.avancer(dt * S.vitesse);
    lum = Allumage(scene, chrono, { moments: () => M, numero: o.numero });

    const etatLeger = (t) => ({ t, M, DEB, S, etape: etape(t), fait: (nom) => t >= M[nom] - 1e-3, vu: (nom, a = 0) => t > DEB[nom] + 1e-3 && seg(nom, t) >= a,
      u: (nom, a = 0, b = 1) => borne((seg(nom, t) - a) / Math.max(1e-6, b - a)) });
    function ceQuiSeVoit() {
      const t = chrono.t;
      return `${o.vueNom ? o.vueNom + '. ' : ''}t = ${fr(t, 1)} s${chrono.running ? ' (ça avance)' : chrono.fait ? ' (fin)' : ' (arrêté)'}. ` +
        `Étape : ${etape(t)}. ${o.phase(t, etatLeger(t))}` + (lum.liste().length ? ' Allumé : ' + lum.liste().join(', ') + '.' : '');
    }
    function setParameters(p) {
      p = p || {};
      if (Number.isFinite(+p.vitesse) && p.vitesse !== '' && p.vitesse != null) S.vitesse = borne(+p.vitesse, .5, 2);
      if ('legendes' in p) S.legendes = bool(p.legendes);
      if (o.parametres && o.parametres.regler) o.parametres.regler(p, S, P);
      scene.sale = true;
      bulle(bulleEl, o.parametres && o.parametres.dit ? o.parametres.dit(S) : `Réglage : vitesse × ${fr(S.vitesse, 1)}, légendes ${S.legendes ? 'affichées' : 'cachées'}.`);
      pont.noter('set_parameters', { ...S }); pont.emettre();
    }

    bouton.onclick = chrono.clic;
    if (o.explication) window.Tableau.explication({ [o.variante || 'vue']: o.explication });
    const commandes = ['start', 'reset', 'pause', 'resume', 'set_time', 'play_until', 'set_parameters', 'allume', 'eteins'];
    const config = { id: o.id, version: '1.0', title: o.titre, variants: [{ id: o.variante || 'vue', label: o.variante || 'vue' }], commands: commandes,
      command_schema: {
        set_time: { time_s: `0..${FIN} (arrêt sur cet instant)`, moment: 'ou le nom d’un moment' },
        play_until: { moment: ORDRE.join(' | ') + ' (joue jusqu’à ce moment et se fige dessus)', time_s: 'ou un instant en s' },
        set_parameters: Object.assign({ vitesse: '0.5..2 (vitesse de l’animation, 1 par défaut)', legendes: 'true | false (les légendes écrites sur la figure)' }, (o.parametres && o.parametres.schema) || {}),
        allume: { cible: 'repère ou moment (ou liste)' }, eteins: {} } };
    pont = protocole({ id: o.id, commandes, config, texte: o.texte || o.titre,
      etat: () => ({ simulation_status: chrono.statut(), ce_qui_se_voit: ceQuiSeVoit(), current_variant: o.variante || 'vue', time_s: +chrono.t.toFixed(2),
        etape: etape(chrono.t), parameters: { ...S }, moments: M, allumes: lum.liste(), ...(o.etat ? o.etat(chrono.t) : {}) }),
      progression: () => chrono.t / FIN,
      executer: (cmd, p) => ({ start: chrono.start, reset: () => { lum.eteins(); chrono.reset(); }, pause: chrono.pause, resume: chrono.resume,
        set_time: () => { chrono.setTime(p); scene.sale = true; }, play_until: () => chrono.playUntil(p), set_parameters: () => setParameters(p),
        allume: () => { lum.allume(p); pont.emettre(); }, eteins: () => { lum.eteins(); pont.emettre(); } })[cmd]?.() });
    bulle(bulleEl, o.accroche || 'Observe…');
    setTimeout(() => { if (!chrono.pilote && !chrono.running && chrono.t === 0) chrono.start(); }, 1600);
    const P = { scene, chrono, ecrit, lum, pont, M, DEB, ORDRE, FIN, S, etape, PILOTE };
    window.__sim = P;
    return P;
  }

  /* ── Peintures communes ───────────────────────────────────────────────────────────────────────── */
  /** La bande colorée d'une phase : fond translucide de sa teinte, liseré à gauche. o.alpha (apparition). */
  function bande(ctx, x, y, w, h, c, o = {}) {
    const a = o.alpha ?? 1; if (a <= .01) return;
    ctx.save(); ctx.globalAlpha = a;
    const g = ctx.createLinearGradient(x, 0, x + w, 0); g.addColorStop(0, rgba(c, o.fort ?? .26)); g.addColorStop(.5, rgba(c, o.doux ?? .13)); g.addColorStop(1, rgba(c, o.fort ?? .26));
    ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(x, y, w, h, o.arrondi ?? 12); ctx.fill();
    ctx.strokeStyle = rgba(c, .55); ctx.lineWidth = 1.4; ctx.stroke();
    ctx.fillStyle = rgba(c, .9); ctx.beginPath(); ctx.roundRect(x, y + 6, 5, h - 12, 3); ctx.fill();
    ctx.restore();
  }
  /** Un phosphate LIÉ à une molécule : la bille orange du Pi (lexique), marquée « P ». */
  function phosphate(ctx, x, y, o = {}) {
    const r = o.r ?? 9, a = o.alpha ?? 1; if (a <= .02) return;
    LX().bille(ctx, x, y, r, LX().C.pi, { alpha: a });
    LX().etiquette(ctx, 'P', x, y, { taille: r * 1.3, couleur: '#2a1400', alpha: a });
  }
  /** Une seringue verticale : corps (yH..yB), aiguille jusqu'à yA ; `enfonce` 0..1 ; teinte du liquide ; o.w largeur. */
  function seringue(ctx, x, yH, yB, yA, enfonce, teinte, o = {}) {
    const w = o.w ?? 14, L = yB - yH, yp = mix(yH + 4, yB - 12, enfonce);
    ctx.save();
    ctx.fillStyle = rgba(teinte, .6); ctx.fillRect(x - w / 2 + 2, yp, w - 4, yB - yp - 1);
    ctx.fillStyle = 'rgba(210,215,225,.95)'; ctx.fillRect(x - w / 2 + 1, yp - 3, w - 2, 4);
    ctx.strokeStyle = 'rgba(210,215,225,.9)'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(x, yp - 3); ctx.lineTo(x, yp - 3 - L * .62); ctx.stroke();
    ctx.lineWidth = 2.4; ctx.beginPath(); ctx.moveTo(x - w * .6, yp - 3 - L * .62); ctx.lineTo(x + w * .6, yp - 3 - L * .62); ctx.stroke();
    const g = ctx.createLinearGradient(x - w / 2, 0, x + w / 2, 0); g.addColorStop(0, 'rgba(255,255,255,.22)'); g.addColorStop(.35, 'rgba(255,255,255,.04)'); g.addColorStop(1, 'rgba(255,255,255,.14)');
    ctx.fillStyle = g; ctx.fillRect(x - w / 2, yH, w, L);
    ctx.strokeStyle = 'rgba(225,238,248,.8)'; ctx.lineWidth = 1.6; ctx.strokeRect(x - w / 2, yH, w, L);
    ctx.beginPath(); ctx.moveTo(x - w / 2 - 4, yH); ctx.lineTo(x + w / 2 + 4, yH); ctx.stroke();
    ctx.strokeStyle = 'rgba(220,235,245,.4)'; ctx.lineWidth = 1;
    for (let i = 1; i < 5; i++) { const y = yH + L * i / 5; ctx.beginPath(); ctx.moveTo(x - w / 2, y); ctx.lineTo(x - w / 2 + 5, y); ctx.stroke(); }
    ctx.fillStyle = 'rgba(220,235,245,.65)'; ctx.beginPath(); ctx.moveTo(x - 4, yB); ctx.lineTo(x + 4, yB); ctx.lineTo(x + 1.5, yB + 7); ctx.lineTo(x - 1.5, yB + 7); ctx.closePath(); ctx.fill();
    ctx.strokeStyle = 'rgba(235,240,245,.9)'; ctx.lineWidth = 1.2; ctx.beginPath(); ctx.moveTo(x, yB + 7); ctx.lineTo(x, yA); ctx.stroke();
    ctx.restore();
  }
  /** Une sonde : tige sombre (ou de verre, o.verre), pointe sensible de la teinte o.pointe, tête. */
  function sonde(ctx, x, yH, yB, o = {}) {
    const w = o.w ?? 12;
    ctx.save();
    const g = ctx.createLinearGradient(x - w / 2, 0, x + w / 2, 0);
    if (o.verre) { g.addColorStop(0, 'rgba(200,225,240,.25)'); g.addColorStop(.5, 'rgba(235,245,255,.55)'); g.addColorStop(1, 'rgba(200,225,240,.25)'); }
    else { g.addColorStop(0, 'rgba(70,74,84,.97)'); g.addColorStop(.45, 'rgba(160,166,180,.97)'); g.addColorStop(1, 'rgba(56,58,68,.97)'); }
    ctx.fillStyle = g; ctx.beginPath(); ctx.roundRect(x - w / 2, yH, w, yB - yH, w * .42); ctx.fill();
    ctx.fillStyle = rgba(o.pointe || [34, 211, 238], .7); ctx.beginPath(); ctx.ellipse(x, yB - 2, w * .42, w * .34, 0, 0, TAU); ctx.fill();
    ctx.fillStyle = 'rgba(36,36,44,.97)'; ctx.fillRect(x - w / 2 - 1, yH, w + 2, 9);
    ctx.restore();
  }
  /** Le nuage du liquide injecté qui se mélange (u : 0 → 1), pour l'œil. */
  function nuage(ctx, x, y, u, teinte, o = {}) {
    if (u <= 0 || u >= 1) return;
    ctx.save(); const r = 6 + (o.r ?? 34) * u, g = ctx.createRadialGradient(x, y, 0, x, y, r);
    g.addColorStop(0, rgba(teinte, .55 * (1 - u))); g.addColorStop(1, rgba(teinte, 0));
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.fill(); ctx.restore();
  }
  /** Une conclusion encadrée (craie verte, fond vert léger), centrée en x ; renvoie sa boîte [x, y, w, h]. */
  function encadre(c, s, x, y, o = {}) {
    const taille = o.taille ?? 18, tt = tailleEcrite(c, taille), w = largeur(c, s, taille) + 22, h = tt * 1.5;
    const bx = x - w / 2, by = y - tt * 1.05;
    c.rect(bx, by, w, h, { couleur: o.couleur || 'vert', fond: o.couleur || 'vert', fondAlpha: .12, arrondi: 8, largeur: 1.8, duree: .3 });
    c.texte(s, x, y, { couleur: o.couleur || 'vert', taille, align: 'center', gras: o.gras });
    return [bx, by, w, h];
  }

  window.Ref2 = { page, bande, phosphate, seringue, sonde, nuage, encadre, largeur, tailleEcrite, borne, bool, rgba, doux, mix, TAU, QS };
})();
