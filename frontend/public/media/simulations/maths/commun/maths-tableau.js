/*
 * MathsTableau — kit commun des constructions de mathématiques « au tableau » (2ᵉ Bac PC BIOF, 10 novembre 2026).
 *
 * En maths, la « simulation » est une construction à la craie qui s'écrit pas à pas, comme un professeur :
 * repère, courbe tracée en direct, point qui glisse, pointillés de projection, tangente, asymptote, escalier d'une suite,
 * lignes d'un calcul… Chaque page déclare ses VUES (?vue=…) ; chaque vue est une fonction de dessin qui suit l'horloge
 * de la scène (S.tw) et marque ses MOMENTS nommés (`K.marque('nom')`) : le tuteur fige la construction sur un moment
 * (`play_until {moment}`), sur un instant (`set_time {time_s}`), change un paramètre (`set_parameters`), montre un repère
 * (`highlight {target}`, ajouté par le kit). L'élève glisse les poignées dessinées (pas de curseurs).
 *
 * Chargement :  tableau.js (kit commun) → exposants.js → maths-tableau.js, puis la page :
 *   MathsTableau.page({
 *     id: 'lc_traversee', titre: 'Le théorème des valeurs intermédiaires',
 *     texte: 'description pour le tuteur',
 *     vues: {
 *       une: {
 *         titre: 'Une courbe continue qui traverse l’axe',
 *         params: { a: { min: -1, max: 1, pas: 0.1, defaut: 0 } },        // réglables (set_parameters, poignées)
 *         dessiner(c, K) { … K.marque('courbe_tracee') … },               // c = la craie (Tableau.Craie), K = l'aide
 *         decrire: { courbe_tracee: 'phrase de ce qui se voit après ce moment', … },   // ou (K) => ({…})
 *         poignees(K) { return [{ id: 'a', x, y, bouger: (x, y) => ({ a: … }) }]; },  // coordonnées du dessin
 *         lecture(K) { return 'f(a) = …' },                                // une phrase sur les valeurs actuelles (facultatif)
 *         curseurs: ['a'],                                                   // au plus deux curseurs dans la barre (facultatif)
 *       },
 *     },
 *   });
 *
 * Aide K (dans dessiner) :
 *   K.P                         paramètres courants ;  K.vu('nom') : le moment est-il atteint ?
 *   K.marque('nom')             le moment « nom » = l'instant d'écriture courant (la craie a fini ce qui précède)
 *   K.anime(duree, p => …)      réserve `duree` s dans l'écriture ; appelle la fonction avec p de 0 à 1 (dessin direct) :
 *                               un point qui glisse, une courbe qui avance ; figée après, p = 1
 *   K.axes({x0,y0,w,h,xmin,xmax,ymin,ymax,gx,gy,nomx,nomy}) → G : G.X(x), G.Y(y), G.inv(px,py) ; trace le repère
 *   K.grille({…}) / MathsTableau.grille({…})  le même G sans rien dessiner (pour les poignées)
 *   K.courbe(G, f, a, b, o)     trace y = f(x) entre a et b (coupée hors du cadre et aux sauts) ; o.couleur, o.largeur
 *   K.courbePart(G, f, a, b, p, o)  la même, tracée jusqu'à la fraction p (dans K.anime)
 *   K.proj(G, x, y, o)          pointillés de (x ; y) vers les deux axes, avec les libellés o.lx, o.ly
 *   K.rond(G, x, y, plein, couleur)  point plein ou rond vide (borne exclue, trou)
 *   K.lignes(x, y, [ {t, couleur, taille, moment, dx} ], interligne)  lignes d'un calcul écrites l'une après l'autre ;
 *                               une ligne avec `moment` marque ce moment juste après elle
 *   K.titre('texte')            titre de la vue en haut à gauche
 *   K.fr(v, d)                  nombre à la française (virgule), sans zéros inutiles
 */
/* Lexique visuel commun (18 novembre 2026) : les couleurs des rôles (courbe cyan, point jaune, tangente orange, asymptote en
 * pointillé blanc, + vert, − rouge) sont dans /media/simulations/shared/lexique/lexique-maths.js, chargé ici pour toutes les pages. */
if (!(window.Lexique && window.Lexique.maths) && document.readyState === 'loading') document.write('<script src="/media/simulations/shared/lexique/lexique-maths.js"><\/script>');

(function () {
  'use strict';
  const T = window.Tableau;
  const VW = 760, VH = 420;
  const $ = (id) => document.getElementById(id);

  /* Scène : même cadre que les ondes (760 × 420 mis à l'échelle, rien de coupé) ; boucle d'image à la demande.
   * `ajuster` (12 novembre 2026, « l'écriture est trop petite au milieu d'un grand tableau vide ») : le cadre n'est plus
   * mis à l'échelle en entier, c'est CE QUI EST ÉCRIT qui remplit le tableau. La boîte de l'encre de la construction
   * complète (mesurée une fois, sans rien changer aux moments) est agrandie jusqu'aux bords, avec une marge, et centrée ;
   * l'agrandissement est borné (ZOOM_MAX × le cadre entier) pour qu'une vue d'une ligne ne devienne pas énorme.
   * La boîte ne fait que grandir pendant la vue (un point glissé hors de la boîte l'élargit au lâcher) : rien ne saute. */
  const MARGE = 14, ZOOM_MAX = 2.2;
  /* 15 novembre 2026 (« textes minuscules, grands vides à gauche et à droite ») : texte jamais plus petit que TAILLE_MIN
   * px à l'écran (15 ; c'était 11) ; `large` : le cadre prend le format du tableau, scene.L de 760 à 760 × L_MAX (1596) (hauteur
   * 420), la page place ses blocs avec scene.L (figure à gauche, calculs à droite) au lieu de les empiler. */
  const TAILLE_MIN = 15, L_MAX = 2.1;
  let PLANCHER_BAS = +(new URLSearchParams(location.search).get('plancher_bas') || .8);
  function Scene(canvas, dessiner, options = {}) {
    const scene = { sale: true, boite: null, mesurant: false, L: VW };
    const craie = new T.Craie(canvas, { onresize: () => { scene.sale = true; scene.boite = null; } });   // nouvelle taille : nouvelle mesure (plancher)
    /* Morceaux d'une même ligne (18 novembre 2026) : une page compose souvent une ligne de plusieurs textes posés l'un après
     * l'autre, à l'abscisse calculée avec la taille prévue. Porté au plancher (petit tableau), un morceau s'allonge et
     * mordait sur le suivant (« ① » sur « une somme… », « ) en dessous » sur « (C) »). Pendant chaque image, un texte
     * aligné à gauche qui commence DANS un texte déjà écrit sur la même ligne de base est poussé juste après lui. Seulement
     * quand le plancher agrandit l'écriture : à la taille prévue, rien ne bouge. */
    const ecrits = []; let prof = 0;
    function decaler(c, s, x, y, o) {
      const t0 = o.taille ?? 18, pl = scene.mesurant ? (scene.plancher || 0) : (c.echelle && c.tailleMin ? c.tailleMin / c.echelle : 0);
      if (!(pl > 0) || (o.align && o.align !== 'left') || o.plancher === false) return x;
      const t = Math.max(t0, pl);
      let w = 0; try { w = c.largeurTexte(String(s), t); } catch (e) { return x; }
      if (o.max && w > o.max) w = o.max;
      const m = c.ctx.getTransform(), k = Math.hypot(m.a, m.b) || 1;
      const X = (m.a * x + m.c * y + m.e) / k, Y = (m.b * x + m.d * y + m.f) / k;   // repère commun (même échelle), translations comprises
      for (const b of ecrits) {
        if (Math.abs(b.Y - Y) > .35 * Math.min(b.t, t) || b.k !== k) continue;
        if (X >= b.X0 - 1 && X < b.X1 - .5 && !(b.s === String(s) && Math.abs(b.X0 - X) < 1)) {
          if (!(t > t0 || b.t > b.t0)) continue;     // ni l'un ni l'autre agrandi : la page l'a voulu ainsi
          x += (b.X1 + .18 * t - X); return decaler(c, s, x, y, o);
        }
      }
      ecrits.push({ s: String(s), X0: X, X1: X + w, Y, t, t0, k });
      return x;
    }
    {
      const base = craie.texte;
      craie.texte = function (s, x, y, o = {}) {
        if (prof > 0) return base.call(this, s, x, y, o);
        prof++; try { return base.call(this, s, decaler(this, s, x, y, o), y, o); } finally { prof--; }
      };
    }
    /* La boîte de l'encre (coordonnées du cadre) : la construction complète dessinée une fois, chaque trait et chaque
     * texte relevés au passage. Le dessin de mesure est effacé par l'image suivante. */
    function mesurer() {
      const b = { x0: Infinity, y0: Infinity, x1: -Infinity, y1: -Infinity };
      const pt = (x, y, m = 0) => { if (!Number.isFinite(x) || !Number.isFinite(y)) return; b.x0 = Math.min(b.x0, x - m); b.y0 = Math.min(b.y0, y - m); b.x1 = Math.max(b.x1, x + m); b.y1 = Math.max(b.y1, y + m); };
      const { trait, texte, point } = craie;
      craie.trait = function (pts, o = {}) { const m = (o.largeur ?? 2.4) / 2 + 1; for (const p of pts || []) pt(p[0], p[1], m); return trait.call(this, pts, o); };
      craie.point = function (x, y, r = 4, c) { pt(x, y, r); return point.call(this, x, y, r, c); };
      craie.texte = function (s, x, y, o = {}) {
        let t = o.taille ?? 18; this.ctx.font = `${o.gras ? '700 ' : ''}${t}px ${T.POLICE}`;
        let l = this.ctx.measureText(String(s).replace(/_/g, '')).width; if (o.max && l > o.max) l = o.max;
        if (scene.plancher > t && o.plancher !== false && !(o.max && l >= o.max)) { l *= scene.plancher / t; t = scene.plancher; }
        const x0 = o.align === 'center' ? x - l / 2 : o.align === 'right' ? x - l : x;
        pt(x0, y - t * 0.95); pt(x0 + l, y + t * 0.35);
        return texte.call(this, s, x, y, o);
      };
      const h = scene.horloge, t = scene.ouvert;
      scene.mesurant = true; scene.horloge = null; scene.ouvert = -1e9; craie.__plancher = scene.plancher || 0;
      try { dessiner(craie, scene); } catch (e) { console.warn('[maths] mesure de la boîte', e); }
      finally { craie.trait = trait; craie.texte = texte; craie.point = point; scene.mesurant = false; scene.horloge = h; scene.ouvert = t; scene.plancher = 0; craie.__plancher = undefined; }
      if (!(b.x1 > b.x0 && b.y1 > b.y0)) return null;
      const n = { x0: Math.max(0, b.x0 - MARGE), y0: Math.max(0, b.y0 - MARGE), x1: Math.min(scene.L, b.x1 + MARGE), y1: Math.min(VH, b.y1 + MARGE) };
      const a = scene.boite;
      return a ? { x0: Math.min(a.x0, n.x0), y0: Math.min(a.y0, n.y0), x1: Math.max(a.x1, n.x1), y1: Math.max(a.y1, n.y1) } : n;
    }
    /* Plancher réel (18 novembre 2026, « la simulation d'abord » : à 1366 × 560 le tableau de la simulation n'a que ~290 px
     * de haut, et le kit commun baisse le plancher du texte sous 400 px de haut — les graduations tombaient à 11 px, à 8 px
     * sur un téléphone en paysage). Ici le plancher reste TAILLE_MIN px à l'écran, quelle que soit la taille du tableau : la
     * boîte de l'encre est mesurée AVEC les textes portés au plancher (taille TAILLE_MIN / s), puis l'échelle s recalculée,
     * deux ou trois fois (le plancher grossit quand s baisse) : rien ne sort du cadre, et la figure garde toute la place. */
    /* Le plancher à l'écran : TAILLE_MIN dès que le tableau a 300 px de haut (portable, grand écran) ; sur un très petit
     * tableau (téléphone en paysage, ~250 px de haut) il baisse avec la hauteur, jamais sous PLANCHER_BAS × TAILLE_MIN :
     * à 15 px, un texte y est 1,6 fois plus grand que prévu et les lignes d'un calcul se recouvrent. */
    const plancherEcran = (H) => TAILLE_MIN * Math.min(1, Math.max(PLANCHER_BAS, (H || 400) / 300));
    const f45 = (W, H) => Math.min(1, Math.max(.45, Math.min((W || 900) / 900, (H || 400) / 400)));   // la baisse du kit commun
    function echelleDe(k, W, H) {
      const sCadre = Math.min(W / scene.L, H / VH);
      return Math.min(W / Math.max(1, k.x1 - k.x0), H / Math.max(1, k.y1 - k.y0), sCadre * ZOOM_MAX);
    }
    function mesurerAuPlancher() {
      const W = craie.W, H = craie.H;
      scene.plancher = 0; let b = mesurer();
      for (let i = 0; i < 4 && b; i++) {
        const pl = plancherEcran(H) / echelleDe(b, W, H);
        if (pl <= (scene.plancherMesure || 0) + .25) break;
        scene.plancherMesure = pl; scene.plancher = pl;
        const n = mesurer(); if (!n) break; b = n; scene.boite = b;
      }
      return b;
    }
    Object.assign(scene, {
      craie, ouvert: performance.now(), s: 1, ox: 0, oy: 0, horloge: null,
      cadre(graine = 7) {
        const W = craie.W, H = craie.H;
        const L = options.large ? Math.round(Math.min(VW * L_MAX, Math.max(VW, VH * W / Math.max(1, H)))) : VW;
        if (L !== scene.L) { scene.L = L; scene.boite = null; }
        if (options.ajuster && !scene.mesurant && !scene.boite && W > 1) { scene.plancherMesure = 0; scene.boite = mesurerAuPlancher(); }
        ecrits.length = 0;
        craie.debut(graine, scene.horloge ? scene.horloge() : (performance.now() - scene.ouvert) / 1000);
        if (scene.mesurant) { scene.s = 1; scene.ox = 0; scene.oy = 0; craie.echelle = 1; craie.tailleMin = 0; craie.cadre = null; return craie; }
        const k = scene.boite || { x0: 0, y0: 0, x1: L, y1: VH };
        const sCadre = Math.min(W / L, H / VH), bw = k.x1 - k.x0, bh = k.y1 - k.y0;
        const s = Math.min(W / bw, H / bh, sCadre * ZOOM_MAX);
        scene.s = s; scene.ox = (W - bw * s) / 2 - k.x0 * s; scene.oy = (H - bh * s) / 2 - k.y0 * s;
        craie.ctx.translate(scene.ox, scene.oy); craie.ctx.scale(s, s);
        craie.echelle = s; craie.tailleMin = plancherEcran(H) / f45(W, H); craie.cadre = { w: L, h: VH, haut: 0 };
        return craie;
      },
      /** La construction a changé de forme (réglage, vue) : la boîte sera remesurée (elle ne fait que grandir). */
      remesurer() { if (options.ajuster) { const n = mesurerAuPlancher(); if (n) scene.boite = n; scene.sale = true; } },
      local(x, y) { return [(x - scene.ox) / scene.s, (y - scene.oy) / scene.s]; },
      reecrire() { scene.ouvert = performance.now(); scene.sale = true; },
      image() {
        const h = scene.horloge, t = scene.ouvert; scene.horloge = null; scene.ouvert = -1e9;
        try { dessiner(craie, scene); return canvas.toDataURL('image/png'); } finally { scene.horloge = h; scene.ouvert = t; scene.sale = true; }
      },
    });
    let avant = performance.now();
    requestAnimationFrame(function image(maintenant) {
      const dt = Math.min(0.1, Math.max(0, (maintenant - avant) / 1000)); avant = maintenant;
      const anime = scene.avancer ? scene.avancer(dt) : false;
      if ((scene.sale || anime) && craie.W > 1) scene.sale = !dessiner(craie, scene);
      requestAnimationFrame(image);
    });
    return scene;
  }

  /**
   * Deux colonnes quand elles remplissent mieux le tableau (16 novembre 2026, règle 9 du skill : « une vue qui laisse plus
   * d'un tiers du cadre vide est remise en page »). Un calcul écrit en une longue colonne étroite, dans un cadre large et
   * bas, ne peut pas être agrandi (il touche le haut et le bas) : on le coupe en deux colonnes côte à côte, comme au tableau.
   * boites : les lignes dans l'ordre, [{ x, y (ligne de base), w, t (taille) }] ; L : largeur du cadre (scene.L).
   * Renvoie pour chaque ligne le décalage [dx, dy] à appliquer (tous nuls : une colonne). Coupure seulement entre deux
   * rangées (jamais entre une ligne et sa voisine posée à la même hauteur) ; on ne change que si l'écriture y gagne ≥ 10 %.
   */
  function colonnes(boites, L = VW, o = {}) {
    const n = boites.length, nul = boites.map(() => [0, 0]);
    if (n < (o.min ?? 4)) return nul;
    const bx = (a, b) => { let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity; for (let i = a; i < b; i++) { const q = boites[i]; x0 = Math.min(x0, q.x); x1 = Math.max(x1, q.x + q.w); y0 = Math.min(y0, q.y - q.t * .95); y1 = Math.max(y1, q.y + q.t * .35); } return { x0, x1, y0, y1 }; };
    const note = (w, h) => Math.min(L / (w + 2 * MARGE), VH / (h + 2 * MARGE), ZOOM_MAX);
    const T = bx(0, n), y0 = o.haut ?? T.y0, w0 = T.x1 - Math.min(T.x0, o.gauche ?? T.x0), h0 = T.y1 - y0, n1 = note(w0, h0);
    const rempli = (w, h, s) => Math.min(1, (w + 2 * MARGE) * s / L) * Math.min(1, (h + 2 * MARGE) * s / VH), r1 = rempli(w0, h0, n1);
    let best = null;
    for (let i = 2; i <= n - 2; i++) {
      if (!(boites[i].y > boites[i - 1].y + 1)) continue;
      const A = bx(0, i), B = bx(i, n), dx = A.x1 + (o.ecart ?? 40) - B.x0, dy = A.y0 - B.y0;
      const x1 = B.x1 + dx; if (x1 + MARGE + .04 * (x1 - T.x0) > L) continue;   // une marge : la police définitive est un peu plus large
      const h = Math.max(A.y1, B.y1 + dy) - y0, w = x1 - Math.min(T.x0, o.gauche ?? T.x0), sc = note(w, h);
      const r = rempli(w, h, sc), val = Math.min(sc / n1, 1.25) + r;   // écrire plus grand d'abord, puis remplir le tableau
      if (!best || val > best.val + 1e-6 || (Math.abs(val - best.val) < 1e-6 && Math.abs(i - n / 2) < Math.abs(best.i - n / 2))) best = { i, dx, dy, sc, r, val };
    }
    // deux colonnes si l'écriture y gagne ≥ 10 %, ou si, à taille presque égale (≥ 95 %), le tableau est nettement plus rempli
    if (!best || !(best.sc >= n1 * 1.1 || (best.sc >= n1 * .95 && best.r >= r1 * 1.25))) return nul;
    return boites.map((_, k) => (k >= best.i ? [best.dx, best.dy] : [0, 0]));
  }

  /* Pas de titre en double (règle 9 du skill simulations-au-tableau, 18 novembre 2026 : « la simulation d'abord ») : dans le
   * lecteur du cours, la diapositive écrit déjà son titre au-dessus de la simulation. Le titre d'une vue (K.titre) qui dit la
   * même chose n'est plus écrit (la craie garde son temps d'écriture : les moments ne bougent pas) ; la figure prend sa place.
   * Hors du lecteur (page ouverte seule, aperçu), le titre reste. */
  const norme = (s) => String(s || '').replace(/⟦([^|⟧]*)\|([^⟧]*)⟧/g, '$1 $2').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]+/g, ' ').trim();
  function titreRepete(s) {
    let h = [];
    try { if (window.parent !== window) h = [...window.parent.document.querySelectorAll('h1')].map((e) => norme(e.textContent)).filter(Boolean); } catch (e) { return false; }
    const a = norme(s); if (!a || !h.length) return false;
    const mots = (x) => new Set(x.split(' ').filter((m) => m.length > 1));
    return h.some((b) => {
      if (a === b || (a.length >= 8 && b.includes(a)) || (b.length >= 8 && a.includes(b))) return true;
      const A = mots(a), B = mots(b); let n = 0; for (const m of A) if (B.has(m)) n++;
      return n / Math.max(1, Math.min(A.size, B.size)) >= .75 && n >= 2;
    });
  }
  /** Le temps que la craie aurait pris pour écrire `s` (le titre sauté garde sa place dans le temps). */
  const tempsTitre = (s) => Math.max(.1, String(s || '').length / 16);

  /** La taille vraiment écrite par la craie pour une taille demandée t (le plancher du petit tableau compris) : pour placer
   *  ce qui va dessous ou à côté (« x → a » sous « lim »). */
  const tailleEcrite = (c, t) => Math.max(t, c.__plancher ?? (c.echelle && c.tailleMin ? c.tailleMin / c.echelle : 0));

  const fr = (v, d = 2) => {
    if (!Number.isFinite(v)) return v > 0 ? '+∞' : v < 0 ? '−∞' : '—';
    let s = (+v.toFixed(d)).toString();
    return s.replace('-', '−').replace('.', ',');
  };

  /* Un repère sans dessin : G.X(x), G.Y(y), G.inv(px, py) (pour les poignées). */
  function grille(o) {
    const g = { x0: 60, y0: 60, w: 420, h: 300, xmin: -1, xmax: 5, ymin: -2, ymax: 6, nomx: 'x', nomy: 'y', ...o };
    g.X = (x) => g.x0 + (x - g.xmin) / (g.xmax - g.xmin) * g.w;
    g.Y = (y) => g.y0 + g.h - (y - g.ymin) / (g.ymax - g.ymin) * g.h;
    g.inv = (px, py) => [g.xmin + (px - g.x0) / g.w * (g.xmax - g.xmin), g.ymin + (g.y0 + g.h - py) / g.h * (g.ymax - g.ymin)];
    return g;
  }

  /* L'aide K, refaite à chaque image. */
  function aide(c, S, M) {
    const K = {
      P: S.P, c, fr,
      vu: (nom) => M[nom] !== undefined && S.tw >= M[nom] - 1e-6,
      marque: (nom) => { S._MM[nom] = c.cur; },
      anime(duree, fn) {
        const t = c.t, debut = c.cur;
        let p = 1;
        if (Number.isFinite(t)) { c.cur += duree; p = t <= debut ? 0 : Math.min(1, (t - debut) / duree); if (p < 1) c.complet = false; }
        if (NET.on) p = EASE(p);   // page nette : départ et arrivée en douceur (0 et 1 inchangés)
        if (p > 0) c.direct(() => fn(p));
        return p;
      },
      /** Fondu (0 → 1) d'un élément peint qui apparaît à l'instant d'écriture courant, SANS réserver de temps (les
       *  moments ne bougent pas) ; `retard` (s) le fait venir un peu après, `duree` (s) la durée du fondu. */
      apparait(duree = .7, retard = 0) { return Number.isFinite(c.t) ? doux((c.t - c.cur - retard) / duree) : 1; },
      /** Zone colorée en transparence entre y = f(x) et y = g(x) (g : fonction ou nombre) pour x de a à b ;
       *  o.couleur, o.alpha (.16), o.part (fraction remplie depuis a), o.degrade (plus pâle loin de f). Aucun temps réservé. */
      zone(G, f, g, a, b, o = {}) {
        const cc = (this && this.c) || c, part = o.part ?? 1;
        if (part <= 0 || (o.alpha ?? .16) <= 0) return K;
        remplir(cc, zonePts(G, f, g, a, a + (b - a) * Math.min(1, part), o.n || 120), o);
        return K;
      },
      /** Bande verticale x ∈ [a ; b] (voisinage, intervalle) sur la hauteur du repère (o.y0, o.y1 pour la borner). */
      bande(G, a, b, o = {}) { return K.zone.call(this, G, () => o.y1 ?? G.ymax, () => o.y0 ?? G.ymin, Math.max(a, G.xmin), Math.min(b, G.xmax), { n: 2, ...o }); },
      /** Bande horizontale y ∈ [a ; b] sur la largeur du repère (o.x0, o.x1 pour la borner). */
      bandeH(G, a, b, o = {}) { const lo = Math.min(a, b), hi = Math.max(a, b); return K.zone.call(this, G, () => Math.min(hi, G.ymax), () => Math.max(lo, G.ymin), Math.max(o.x0 ?? G.xmin, G.xmin), Math.min(o.x1 ?? G.xmax, G.xmax), { n: 2, ...o }); },
      titre(s) { if (titreRepete(s)) { c.pause(tempsTitre(s)); return K; } c.texte(s, 20, 30, { couleur: 'cyan', taille: 20, max: 720 }); return K; },
      grille,
      axes(o) {
        const g = grille(o);
        const ax = Math.min(Math.max(0, g.ymin), g.ymax), ay = Math.min(Math.max(0, g.xmin), g.xmax);
        const yA = g.Y(ax), xA = g.X(ay);
        if (g.quadrillage) for (let x = Math.ceil(g.xmin); x <= g.xmax; x++) c.ligne(g.X(x), g.y0, g.X(x), g.y0 + g.h, { couleur: 'tresfaible', largeur: .8, duree: .02 });
        c.fleche(g.x0 - 6, yA, g.x0 + g.w + 14, yA, { couleur: 'faible', largeur: 1.6 });
        c.fleche(xA, g.y0 + g.h + 6, xA, g.y0 - 14, { couleur: 'faible', largeur: 1.6 });
        c.texte(g.nomx, g.x0 + g.w + 18, yA + 18, { couleur: 'faible', taille: 16 });
        c.texte(g.nomy, xA - 18, g.y0 - 6, { couleur: 'faible', taille: 16 });
        for (const v of g.gx || []) { const [x, l] = Array.isArray(v) ? v : [v, fr(v)]; c.ligne(g.X(x), yA - 4, g.X(x), yA + 4, { couleur: 'faible', largeur: 1.2, duree: .02 }); if (l !== '') c.texte(l, g.X(x), yA + 19, { couleur: 'faible', taille: 14, align: 'center', duree: .05 }); }
        for (const v of g.gy || []) { const [y, l] = Array.isArray(v) ? v : [v, fr(v)]; c.ligne(xA - 4, g.Y(y), xA + 4, g.Y(y), { couleur: 'faible', largeur: 1.2, duree: .02 }); if (l !== '') c.texte(l, xA - 8, g.Y(y) + 5, { couleur: 'faible', taille: 14, align: 'right', duree: .05 }); }
        if (g.origine !== false && g.xmin < 0 && g.ymin < 0) c.texte('O', xA - 14, yA + 17, { couleur: 'faible', taille: 14 });
        return g;
      },
      _points(G, f, a, b, n) {
        const morceaux = [[]]; const ymarge = (G.ymax - G.ymin) * .06;
        let prec = null;
        for (let i = 0; i <= n; i++) {
          const x = a + (b - a) * i / n, y = f(x);
          const dedans = Number.isFinite(y) && y >= G.ymin - ymarge && y <= G.ymax + ymarge;
          const saut = prec !== null && Number.isFinite(y) && Math.abs(G.Y(y) - G.Y(prec)) > G.h * .45;
          if (!dedans || saut) { if (morceaux[morceaux.length - 1].length) morceaux.push([]); if (!dedans) { prec = null; continue; } }
          morceaux[morceaux.length - 1].push([G.X(x), G.Y(Math.min(G.ymax + ymarge, Math.max(G.ymin - ymarge, y)))]);
          prec = y;
        }
        return morceaux.filter((m) => m.length > 1);
      },
      courbe(G, f, a, b, o = {}) {
        for (const m of K._points(G, f, a, b, o.n || 160)) trace(c, m, { tremble: .35, couleur: o.couleur || 'cyan', largeur: o.largeur ?? 2.6, pointille: o.pointille, duree: o.duree });
        return K;
      },
      courbePart(G, f, a, b, p, o = {}) {
        if (p <= 0) return K;
        const bb = a + (b - a) * p;
        for (const m of K._points(G, f, a, bb, Math.max(4, Math.round((o.n || 160) * p)))) trace(c, m, { tremble: .35, couleur: o.couleur || 'cyan', largeur: o.largeur ?? 2.6, pointille: o.pointille });
        return K;
      },
      proj(G, x, y, o = {}) {
        const ax = Math.min(Math.max(0, G.ymin), G.ymax), ay = Math.min(Math.max(0, G.xmin), G.xmax);
        const coul = o.couleur || 'faible';
        if (o.versX !== false) c.ligne(G.X(x), G.Y(y), G.X(x), G.Y(ax), { couleur: coul, largeur: 1.3, pointille: [5, 5] });
        if (o.versY !== false) c.ligne(G.X(x), G.Y(y), G.X(ay), G.Y(y), { couleur: coul, largeur: 1.3, pointille: [5, 5] });
        if (o.lx) c.texte(o.lx, G.X(x), G.Y(ax) + (y < ax ? -10 : 20), { couleur: o.couleurTexte || coul, taille: o.taille || 15, align: 'center' });
        if (o.ly) c.texte(o.ly, G.X(ay) - 8, G.Y(y) + 5, { couleur: o.couleurTexte || coul, taille: o.taille || 15, align: 'right' });
        return K;
      },
      rond(G, x, y, plein = true, couleur = 'jaune') {
        const px = G.X(x), py = G.Y(y);
        pastille(c, px, py, plein, couleur);
        return K;
      },
      lignes(x, y, liste, inter = 30) {
        for (const l of liste) {
          if (l.pause) c.pause(l.pause);
          if (l.t) c.texte(l.t, x + (l.dx || 0), y, { couleur: l.couleur || 'blanc', taille: l.taille || 19, max: l.max || (VW - x - 16) });
          if (l.cadre) { const w = c.largeurTexte(l.t, l.taille || 19) + 16; c.rect(x + (l.dx || 0) - 8, y - (l.taille || 19) - 2, w, (l.taille || 19) + 12, { couleur: l.cadre, arrondi: 6, largeur: 1.4 }); }
          if (l.repere) c.repere(l.repere, x + (l.dx || 0) - 4, y - 22, Math.min(VW - x - 10, c.largeurTexte(l.t || '', l.taille || 19) + 10), 30, l.label || l.t);
          if (l.moment) K.marque(l.moment);
          y += l.inter ?? inter;
        }
        return y;
      },
    };
    return K;
  }

  function page(def) {
    const P0 = new URLSearchParams(location.search);
    const noms = Object.keys(def.vues);
    const vue = def.vues[P0.get('vue')] ? P0.get('vue') : (def.defaut || noms[0]);
    const V = def.vues[vue];
    const VITESSE = def.vitesse || 1.5;
    const params0 = {};
    for (const [k, p] of Object.entries(V.params || {})) { const u = P0.get(k); params0[k] = u !== null && Number.isFinite(+u.replace(',', '.')) ? +u.replace(',', '.') : p.defaut; }
    const S = { tw: 0, running: true, pause: false, fait: false, jusqua: null, motif: '', emis: 0, P: { ...params0 }, _MM: {}, glisse: null };
    let M = {};

    document.body.insertAdjacentHTML('afterbegin', '');
    const canvas = $('canvas');
    const scene = Scene(canvas, dessiner, { ajuster: def.ajuster !== false && V.ajuster !== false, large: !!(def.large || V.large) });
    scene.horloge = () => S.tw;
    const craie = scene.craie;
    NET.on = !!def.net;
    if (NET.on) {
      // un point posé (c.point) reçoit un halo de sa couleur et un reflet : il se voit, sans rien changer au temps d'écriture
      const point0 = craie.point;
      craie.point = function (x, y, r = 4, coul) {
        const t = this.t, avant = this.cur, res = point0.call(this, x, y, r, coul);
        if (r >= 2.5 && (!Number.isFinite(t) || t > avant)) halo(this, x, y, r, coul);
        return res;
      };
    }

    function dessiner(c) {
      // la mesure de la boîte (kit) dessine la construction complète : temps, moments et repères gardés tels quels
      const mesure = scene.mesurant, tw = S.tw, MM = S._MM;
      if (mesure) S.tw = 1e6;
      scene.cadre(def.graine || 23);
      S._MM = {};
      const K = aide(c, S, M);
      V.dessiner(c, K);
      if (mesure) { S._MM = MM; S.tw = tw; return true; }
      M = S._MM;
      if (M.fin === undefined) M.fin = c.cur;
      return c.fin() || !S.running;
    }
    const etapes = () => Object.keys(M).sort((a, b) => M[a] - M[b]);
    const etiquette = () => { $('run').textContent = S.running ? 'Pause' : S.pause ? 'Reprendre' : 'Réécrire'; };
    const descr = () => (typeof V.decrire === 'function' ? V.decrire(aide(craie, S, M)) : V.decrire) || {};
    function ceQuiSeVoit() {
      const D = descr(), faites = etapes().filter((n) => S.tw >= M[n] - 1e-6 || S.fait);
      const m = [`${def.titre} — ${V.titre}.`];
      if (!faites.length) m.push(S.running ? 'La construction commence à s’écrire à la craie.' : 'Rien d’écrit encore.');
      for (const n of faites) if (D[n]) m.push(D[n]);
      if (V.lecture) m.push(V.lecture(aide(craie, S, M)));
      if (V.params && Object.keys(V.params).length) m.push('Réglages : ' + Object.entries(S.P).map(([k, v]) => `${k} = ${fr(v, 3)}`).join(', ') + '.');
      m.push(S.running ? 'La craie écrit encore.' : S.pause ? `Arrêt sur image : ${S.motif || (faites.length ? faites[faites.length - 1] : 'début')}.` : 'Construction complète.');
      return m.join(' ');
    }
    scene.avancer = (dt) => {
      if (!S.running) return false;
      S.tw += dt * VITESSE;
      if (S.jusqua != null && S.tw >= S.jusqua) {
        S.tw = S.jusqua; S.jusqua = null; S.running = false;
        if (S.tw >= M.fin - 1e-6) { S.pause = false; S.fait = true; etiquette(); T.bulle($('feedback'), V.finale || 'Construction complète.'); pont.noter('measurement', { vue }); pont.emettre(); return true; }
        S.pause = true; etiquette();
        T.bulle($('feedback'), 'Arrêt sur image : ' + (S.motif || 'instant choisi') + '.'); pont.noter('pause', { moment: S.motif }); pont.emettre();
        return true;
      }
      if (M.fin !== undefined && S.tw >= M.fin + 0.05) {
        S.running = false; S.pause = false; S.fait = true; etiquette(); if (V.finale) T.bulle($('feedback'), V.finale); pont.noter('measurement', { vue }); pont.emettre();
      } else if (performance.now() - S.emis > 500) { S.emis = performance.now(); pont.emettre(); }
      return true;
    };
    function calculer() { const t = S.tw, r = S.running; S.tw = 1e6; dessiner(craie); S.tw = t; S.running = r; scene.sale = true; }
    function start() { S.tw = 0; S.jusqua = null; S.motif = ''; S.running = true; S.pause = false; S.fait = false; etiquette(); T.bulle($('feedback'), ''); pont.noter('start', { vue }); pont.emettre(); }
    function reset() { S.P = { ...params0 }; majCurseurs(); start(); }
    function pause() { if (!S.running) return; S.running = false; S.pause = true; S.jusqua = null; etiquette(); pont.noter('pause'); pont.emettre(); }
    function resume() { if (S.running) return; if (!S.pause) return start(); S.running = true; S.pause = false; etiquette(); pont.noter('resume'); pont.emettre(); }
    function playUntil(p) {
      calculer();
      const nom = p.moment in M ? p.moment : null, cible = nom ? M[nom] : +p.time_s;
      if (!Number.isFinite(cible)) return;
      if (S.fait || !(S.running || S.pause) || S.tw >= cible - 1e-3) { S.tw = 0; S.fait = false; }
      S.jusqua = cible; S.motif = nom ? ((V.motifs || {})[nom] || nom.replace(/_/g, ' ')) : `t = ${fr(cible, 1)} s`;
      S.running = true; S.pause = false; etiquette(); T.bulle($('feedback'), '');
      pont.noter('play_until', { moment: nom }); pont.emettre();
    }
    function setTime(p) {
      calculer(); const t = +p.time_s; if (!Number.isFinite(t)) return;
      S.tw = Math.max(0, Math.min(t, M.fin)); S.running = false; S.pause = S.tw < M.fin; S.fait = !S.pause; S.jusqua = null; etiquette(); scene.sale = true;
      pont.noter('set_time', { time_s: t }); pont.emettre();
    }
    function borne(k, v) { const d = (V.params || {})[k]; if (!d) return null; v = Math.min(d.max, Math.max(d.min, +v)); if (d.pas) v = Math.round((v - d.min) / d.pas) * d.pas + d.min; return +v.toFixed(6); }
    function setParameters(p, par) {
      let change = false;
      for (const [k, v] of Object.entries(p || {})) { const b = borne(k, v); if (b !== null && Number.isFinite(b) && b !== S.P[k]) { S.P[k] = b; change = true; } }
      if (!change) return;
      calculer(); scene.remesurer();
      if (S.fait) S.tw = M.fin;     // construction finie : elle reste entière, avec les nouvelles valeurs
      majCurseurs();
      if (par === 'eleve' && V.lecture) T.bulle($('feedback'), V.lecture(aide(craie, S, M)));
      scene.sale = true; pont.noter('set_parameters', { ...S.P, par }); pont.emettre();
    }
    /* Curseurs (14 novembre 2026, professeur règle 28) : une vue peut déclarer `curseurs: ['k', …]` (au plus deux) ;
     * chaque paramètre listé reçoit un curseur à la craie dans la barre, à côté du bouton. `params.k.label` (texte devant),
     * `params.k.unite`, `params.k.affiche(v)` (texte de la valeur, ex. « 1000 » pour un indice). L'élève le glisse : la
     * construction se réécrit aussitôt avec la nouvelle valeur ; le tuteur, lui, passe par set_parameters (le curseur suit). */
    const curseurs = {};
    function majCurseurs() {
      for (const [k, el] of Object.entries(curseurs)) { el.maj(S.P[k]); const d = V.params[k]; if (d.affiche) el.querySelector('b').textContent = d.affiche(S.P[k]); }
    }
    for (const k of (V.curseurs || []).slice(0, 2)) {
      const d = (V.params || {})[k]; if (!d) continue;
      const el = T.curseur({ id: 'curseur_' + k, label: d.label || (k + ' ='), min: d.min, max: d.max, step: d.pas || 'any', valeur: S.P[k], unite: d.unite || '', decimales: d.decimales, commande: 'set_parameters' });
      el.input.addEventListener('input', () => { setParameters({ [k]: Number(el.input.value) }, 'eleve'); });
      curseurs[k] = el;
      const apres = Object.values(curseurs).length > 1 ? Object.values(curseurs)[Object.values(curseurs).length - 2] : $('run');
      apres.after(el);
    }
    $('run').onclick = () => (S.running ? pause() : S.pause ? resume() : start());

    // Poignées : l'élève glisse un point du dessin (pas de curseur).
    if (V.poignees) {
      T.glisser(canvas, {
        toucher(x, y) {
          const [lx, ly] = scene.local(x, y);
          const hs = V.poignees(aide(craie, S, M)) || [];
          const h = hs.find((q) => Math.hypot(q.x - lx, q.y - ly) < 18);
          return h ? h.id : null;
        },
        bouger(id, x, y) {
          const [lx, ly] = scene.local(x, y);
          const h = (V.poignees(aide(craie, S, M)) || []).find((q) => q.id === id); if (!h) return;
          const nv = h.bouger(lx, ly) || {};
          if (!S.fait) { S.tw = 1e6; S.running = false; S.pause = false; S.fait = true; etiquette(); }
          for (const [k, v] of Object.entries(nv)) { const b = borne(k, v); if (b !== null) S.P[k] = b; }
          calculer(); S.tw = M.fin; scene.sale = true;
        },
        lacher() { scene.remesurer(); majCurseurs(); pont.noter('set_parameters', { ...S.P }); T.bulle($('feedback'), V.lecture ? V.lecture(aide(craie, S, M)) : 'Nouveau réglage.'); pont.emettre(); },
      });
    }

    const commandes = ['start', 'reset', 'pause', 'resume', 'play_until', 'set_time'].concat(V.params && Object.keys(V.params).length ? ['set_parameters'] : []);
    const schema = { play_until: { moment: '(moments de la vue, voir state.moments) — réécrit la construction et s’arrête sur ce moment' }, set_time: { time_s: '0..durée de l’écriture' } };
    if (V.params) schema.set_parameters = Object.fromEntries(Object.entries(V.params).map(([k, d]) => [k, `${d.min}..${d.max}` + (d.pas ? ` (pas ${d.pas})` : '') + (d.sens ? ' : ' + d.sens : '')]));
    const config = { id: def.id + '_' + vue, version: '1.0', title: def.titre + ' — ' + V.titre, variants: noms.map((n) => ({ id: n, label: def.vues[n].titre })), commands: commandes, command_schema: schema };
    if (V.explication) T.explication({ [vue]: V.explication });
    const pont = T.protocole({ id: config.id, commandes, config,
      texte: `${def.texte || def.titre}. Vue « ${vue} » : ${V.titre}.` + (V.texte ? ' ' + V.texte : ''),
      etat: () => ({ simulation_status: S.running ? 'running' : S.pause ? 'paused' : 'finished', ce_qui_se_voit: ceQuiSeVoit(), current_variant: vue,
        parameters: { ...S.P }, time_s: +S.tw.toFixed(2), moments: Object.fromEntries(etapes().map((n) => [n, +M[n].toFixed(2)])),
        moments_atteints: etapes().filter((n) => S.tw >= M[n] - 1e-6) }),
      progression: () => (S.fait ? 1 : M.fin ? Math.min(1, S.tw / M.fin) : 0),
      executer: (cmd, p) => ({ start, reset, pause, resume, play_until: () => playUntil(p), set_time: () => setTime(p), set_parameters: () => setParameters(p, 'tuteur') })[cmd]?.() });
    etiquette(); majCurseurs();
    window.__maths = { S, get M() { return M; }, scene, vue, def };
    return { S, scene, pont };
  }

  /* Peinture (professeur règle 32, 14 novembre 2026 : « toujours chercher le réalisme ») : quand une construction prend
   * un objet concret pour image (des blocs empilés, des morceaux posés bout à bout, des dalles de pierre…), cet objet est
   * PEINT en couleur (dégradé, ombre, veinage) ; la craie garde ce que le professeur écrit : nombres, formules, axes,
   * courbes, flèches. Les graphes et tableaux restent à la craie. */
  const rvb = (s) => { const m = /^#([0-9a-f]{6})$/i.exec(s || ''); return m ? [0, 2, 4].map((i) => parseInt(m[1].slice(i, i + 2), 16)) : [200, 200, 200]; };
  /** Une teinte : k > 0 éclaircit vers le blanc, k < 0 assombrit vers le noir. */
  const nuance = (c, k, a = 1) => `rgba(${c.map((v) => Math.round(k >= 0 ? v + (255 - v) * k : v * (1 + k))).join(',')},${a})`;
  /** Réserve `duree` s dans l'écriture (comme un trait de craie) et peint `fn(ctx, part)` d'un coup, en fondu. */
  function peindre(c, duree, fn) {
    let p = 1;
    if (Number.isFinite(c.t)) { const debut = c.cur; c.cur += duree; p = c.t <= debut ? 0 : Math.min(1, (c.t - debut) / duree); if (p < 1) c.complet = false; }
    if (p > 0) c.direct(() => { const ctx = c.ctx; ctx.save(); ctx.globalAlpha = p; try { fn(ctx, p); } finally { ctx.restore(); } });
    return p;
  }
  /** Un bloc de bois laqué, teinté de la couleur de craie `couleur` (assez sombre pour qu'une écriture de cette couleur
   *  s'y lise) : ombre portée, dégradé, veinage dans le sens de la longueur, arête claire en haut. Dessin direct. */
  function bloc(c, x, y, w, h, couleur, o = {}) {
    if (!(w > 0.3 && h > 0.3)) return;
    const ctx = c.ctx, k = rvb(c.couleur(couleur)), r = Math.min(o.arrondi ?? 3, w / 2, h / 2), debout = h > w;
    const forme = () => { ctx.beginPath(); ctx.roundRect(x, y, w, h, r); };
    ctx.save();
    ctx.shadowColor = 'rgba(0,0,0,.5)'; ctx.shadowBlur = 7; ctx.shadowOffsetX = 2.5; ctx.shadowOffsetY = 3;
    const g = debout ? ctx.createLinearGradient(x, 0, x + w, 0) : ctx.createLinearGradient(0, y, 0, y + h);
    const base = o.clair ? -0.28 : -0.42;
    g.addColorStop(0, nuance(k, base + 0.1)); g.addColorStop(0.28, nuance(k, base + 0.22)); g.addColorStop(0.6, nuance(k, base));
    g.addColorStop(1, nuance(k, base - 0.25));
    forme(); ctx.fillStyle = g; ctx.fill();
    ctx.restore();
    ctx.save(); forme(); ctx.clip();
    // Veinage du bois, dans le sens de la longueur (fixe : il ne tremble pas d'une image à l'autre).
    const L = debout ? h : w, E = debout ? w : h, n = Math.max(2, Math.round(E / 6));
    for (let i = 0; i < n; i++) {
      const e = (i + 0.5) / n * E, ond = 0.8 + ((i * 37) % 5) * 0.25;
      ctx.strokeStyle = i % 2 ? 'rgba(0,0,0,.16)' : 'rgba(255,255,255,.08)'; ctx.lineWidth = 0.8; ctx.beginPath();
      for (let s = 0; s <= L; s += 6) {
        const d = e + Math.sin((s + i * 13) / (9 + i % 3 * 4)) * ond;
        const [px, py] = debout ? [x + d, y + s] : [x + s, y + d];
        s ? ctx.lineTo(px, py) : ctx.moveTo(px, py);
      }
      ctx.stroke();
    }
    // Arête éclairée en haut et à gauche, arête sombre en bas.
    ctx.fillStyle = 'rgba(255,255,255,.22)'; ctx.fillRect(x, y, w, Math.min(2, h / 3)); ctx.fillRect(x, y, Math.min(1.5, w / 3), h);
    ctx.fillStyle = 'rgba(0,0,0,.28)'; ctx.fillRect(x, y + h - Math.min(2, h / 3), w, Math.min(2, h / 3));
    ctx.restore();
    if (w > 3 && h > 3) { ctx.strokeStyle = nuance(k, -0.7, 0.8); ctx.lineWidth = 0.8; forme(); ctx.stroke(); }
  }

  /* ── Netteté et couleur (16 novembre 2026, « animations plus réalistes, plus attractives, belles couleurs, simples ») ──
   * Une page qui déclare `net: true` (MathsTableau.page / LC.page) : les courbes (K.courbe, K.courbePart) sont tracées
   * nettes (tremblement léger) avec une lueur douce de leur couleur ; chaque point posé (c.point, K.rond) a un halo et un
   * reflet, une borne exclue (rond vide) est évidée ; les mouvements de K.anime sont adoucis (départ et arrivée lents).
   * Nouveaux outils (sans temps réservé : les moments ne bougent pas) : K.zone / K.bande / K.bandeH (zones en transparence),
   * K.apparait (fondu), MathsTableau.remplir (polygone coloré), MathsTableau.lueur (un trait qui brille), MathsTableau.halo.
   * Les écritures, axes et flèches restent à la craie. Sans `net`, rien ne change. */
  const NET = { on: false };
  const EASE = (p) => (p <= 0 ? 0 : p >= 1 ? 1 : p * p * (3 - 2 * p));
  const doux = (p) => (p <= 0 ? 0 : p >= 1 ? 1 : (1 - Math.cos(Math.PI * p)) / 2);
  /** La couleur `coul` (nom de craie, #rrggbb, rgb[a](…)) avec l'opacité a. */
  function teinte(c, coul, a) {
    const s = c.couleur(coul), h = /^#([0-9a-f]{6})$/i.exec(s);
    if (h) return `rgba(${rvb(s).join(',')},${a})`;
    const m = /^rgba?\(([^,]+),([^,]+),([^,)]+)/i.exec(s.replace(/\s/g, ''));
    return m ? `rgba(${m[1]},${m[2]},${m[3]},${a})` : s;
  }
  /** Polygone [[x,y],…] rempli en transparence (o.couleur, o.alpha .16, o.dessus : par-dessus le dessin déjà fait ;
   *  sinon il passe DESSOUS, derrière les traits et les textes). Les intermédiaires du tableau large le transforment
   *  comme un trait (c.__remplir). */
  function remplir(c, pts, o = {}) {
    if (!pts || pts.length < 3) return;
    if (c.__remplir) return c.__remplir(pts, o);
    peint(c, c.ctx, pts, o);
  }
  function peint(c, ctx, pts, o = {}) {
    const a = o.alpha ?? .16; if (!(a > .003)) return;
    ctx.save();
    if (!o.dessus) ctx.globalCompositeOperation = 'destination-over';
    ctx.beginPath(); pts.forEach(([x, y], i) => (i ? ctx.lineTo(x, y) : ctx.moveTo(x, y))); ctx.closePath();
    if (o.degrade) {
      let y0 = Infinity, y1 = -Infinity; for (const p of pts) { y0 = Math.min(y0, p[1]); y1 = Math.max(y1, p[1]); }
      const g = ctx.createLinearGradient(0, o.degrade === 'bas' ? y1 : y0, 0, o.degrade === 'bas' ? y0 : y1);
      g.addColorStop(0, teinte(c, o.couleur || 'cyan', a)); g.addColorStop(1, teinte(c, o.couleur || 'cyan', a * .25));
      ctx.fillStyle = g;
    } else ctx.fillStyle = teinte(c, o.couleur || 'cyan', a);
    ctx.fill();
    if (o.bord) { ctx.globalCompositeOperation = 'source-over'; ctx.strokeStyle = teinte(c, o.couleur || 'cyan', Math.min(1, a * 2.5)); ctx.lineWidth = 1; ctx.stroke(); }
    ctx.restore();
  }
  /** Les points (en px du dessin) de la zone entre y = f(x) et y = g(x), x de a à b, bornés au repère. */
  function zonePts(G, f, g, a, b, n = 120) {
    if (!(b > a)) return [];
    const yb = (y) => G.Y(Math.min(G.ymax, Math.max(G.ymin, y))), gg = typeof g === 'function' ? g : () => g;
    const haut = [], bas = [];
    for (let i = 0; i <= n; i++) {
      const x = a + (b - a) * i / n, y1 = f(x), y2 = gg(x);
      if (!Number.isFinite(y1) || !Number.isFinite(y2)) continue;
      haut.push([G.X(x), yb(y1)]); bas.push([G.X(x), yb(y2)]);
    }
    return haut.concat(bas.reverse());
  }
  /** `fn()` trace avec une lueur douce de la couleur `coul` (force k) ; sans `net`, fn() tel quel. */
  function lueur(c, coul, fn, k = 1) {
    if (!NET.on || k <= 0) return fn();
    const ctx = c.ctx, sc = ctx.shadowColor, sb = ctx.shadowBlur;
    ctx.shadowColor = teinte(c, coul, .6); ctx.shadowBlur = 6 * k * (devicePixelRatio || 1) * Math.max(1, c.echelle || 1);
    try { return fn(); } finally { ctx.shadowColor = sc; ctx.shadowBlur = sb; }
  }
  /** Un trait de courbe : net et lumineux avec `net`, à la craie sinon (même temps d'écriture dans les deux cas). */
  function trace(c, pts, o) {
    if (!NET.on) return c.trait(pts, o);
    return lueur(c, o.couleur || 'cyan', () => c.trait(pts, { ...o, tremble: Math.min(o.tremble ?? 1, .12) }), o.pointille ? .5 : 1);
  }
  /** Halo et reflet d'un point déjà posé (dessin direct, sans temps). */
  function halo(c, x, y, r, coul) {
    const ctx = c.ctx, R = r * 2.7;
    ctx.save();
    const g = ctx.createRadialGradient(x, y, r * .5, x, y, R);
    g.addColorStop(0, teinte(c, coul || 'blanc', .36)); g.addColorStop(1, teinte(c, coul || 'blanc', 0));
    ctx.globalCompositeOperation = 'destination-over'; ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, R, 0, Math.PI * 2); ctx.fill();
    ctx.globalCompositeOperation = 'source-over'; ctx.fillStyle = 'rgba(255,255,255,.6)';
    ctx.beginPath(); ctx.arc(x - r * .3, y - r * .3, r * .36, 0, Math.PI * 2); ctx.fill();
    ctx.restore();
  }
  /** Le point d'une courbe (K.rond) : plein avec halo, ou rond vide évidé (borne exclue, trou). */
  function pastille(c, px, py, plein, couleur) {
    if (plein) return c.point(px, py, 5, couleur);
    const t = c.t, avant = c.cur;
    c.cercle(px, py, 5.5, { couleur, largeur: 2 });
    if (NET.on && (!Number.isFinite(t) || t > avant)) {
      const pts = []; for (let i = 0; i < 20; i++) pts.push([px + 4.4 * Math.cos(i / 20 * Math.PI * 2), py + 4.4 * Math.sin(i / 20 * Math.PI * 2)]);
      remplir(c, pts, { couleur: '#0f1d18', alpha: .95, dessus: true });
    }
  }

  window.MathsTableau = { Scene, page, fr, titreRepete, tempsTitre, tailleEcrite, grille, VW, VH, peindre, bloc, nuance, rvb, colonnes,
    NET, EASE, doux, teinte, remplir, peint, zonePts, lueur, trace, halo, pastille };
  window.OndesTableau = window.OndesTableau || { Scene, VW, VH };   // bilan.html / carte.html du kit des ondes s'y appuient
})();
