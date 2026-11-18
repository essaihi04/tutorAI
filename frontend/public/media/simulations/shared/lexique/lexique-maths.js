/*
 * LEXIQUE VISUEL COMMUN — MATHS (18 novembre 2026 ; skill simulations-au-tableau règle 15). Fiche : docs/lexique-visuel/maths.md.
 * En maths les « objets » sont des rôles : une couleur de craie par rôle, la même dans les six cours (limites, dérivation,
 * suites, primitives, ln, complexes). La voix des cours de maths ne nomme aucune couleur.
 *
 *   <script src="/media/simulations/shared/lexique/lexique-maths.js"></script>
 *   const R = Lexique.maths.ROLES;                       // R.courbe → 'cyan', R.tangente → 'orange'…
 *   Lexique.maths.tangente(c, G, x0, y0, pente, { demi }) // segment de tangente centré sur le point (craie orange)
 *   Lexique.maths.asymptote(c, G, { x } | { y } | { a, b }) // droite en pointillé blanc sur tout le repère
 *   (G : le repère de MathsTableau, avec G.X(x), G.Y(y), G.xmin, G.xmax, G.ymin, G.ymax, G.w, G.h.)
 */
(function () {
  'use strict';
  window.Lexique = window.Lexique || {};
  if (window.Lexique.maths) return;

  /* Les rôles (couleurs de la craie du kit : blanc, cyan, jaune, vert, violet, orange, bleu, rouge, rose, faible). */
  const ROLES = {
    axes: 'faible',            // repère, graduations, projections (pointillé faible)
    courbe: 'cyan',            // la courbe C_f (une deuxième courbe : violet ; C_g, C_F : vert si on compare)
    courbe2: 'violet',
    point: 'jaune',            // un point placé, M, A, l'image lue (K.rond)
    tangente: 'orange',        // tangente, demi-tangente, triangle de pente (jamais la couleur d'un point)
    asymptote: 'blanc',        // droite asymptote : pointillé blanc [8, 6]
    positif: 'vert',           // signe +, f > 0, croissante (flèche montante), zone au-dessus
    negatif: 'rouge',          // signe −, f < 0, décroissante (flèche descendante), zone au-dessous
    zone: 'cyan',              // aire / bande sous une courbe (remplissage léger, alpha ≈ .16)
    resultat: 'jaune',         // formule ou résultat encadré
    piege: 'orange',           // ce qu'il faut retenir comme piège (fiches bilan)
  };
  const POINTILLE_ASYMPTOTE = [8, 6];

  /** Segment de tangente au point (x0, y0) de pente `pente` (coordonnées du repère), demi-longueur `demi` px (42 par défaut). */
  function tangente(c, G, x0, y0, pente, o = {}) {
    const sx = G.w / (G.xmax - G.xmin), sy = G.h / (G.ymax - G.ymin);
    let dx = 1, dy = -pente * sy / sx; const n = Math.hypot(dx, dy); dx /= n; dy /= n;
    const X = G.X(x0), Y = G.Y(y0), L = o.demi ?? 42, s1 = o.seulementDroite ? 0 : -L, s2 = o.seulementGauche ? 0 : L;
    c.ligne(X + dx * s1, Y + dy * s1, X + dx * s2, Y + dy * s2, { couleur: o.couleur ?? ROLES.tangente, largeur: o.largeur ?? 2.4 });
  }
  /** Asymptote : verticale { x }, horizontale { y } ou oblique { a, b } (y = a·x + b), en pointillé blanc sur tout le repère. */
  function asymptote(c, G, d, o = {}) {
    const st = { couleur: o.couleur ?? ROLES.asymptote, largeur: o.largeur ?? 2, pointille: POINTILLE_ASYMPTOTE };
    if (d.x != null) c.ligne(G.X(d.x), G.Y(G.ymax), G.X(d.x), G.Y(G.ymin), st);
    else if (d.y != null) c.ligne(G.X(G.xmin), G.Y(d.y), G.X(G.xmax), G.Y(d.y), st);
    else c.ligne(G.X(G.xmin), G.Y(d.a * G.xmin + d.b), G.X(G.xmax), G.Y(d.a * G.xmax + d.b), st);
  }
  /** La couleur d'un signe (« + », « − », « 0 ») dans un tableau de signes ou de variations. */
  const couleurSigne = s => (s === '+' ? ROLES.positif : s === '−' || s === '-' ? ROLES.negatif : ROLES.point);

  window.Lexique.maths = { ROLES, POINTILLE_ASYMPTOTE, tangente, asymptote, couleurSigne };
})();
