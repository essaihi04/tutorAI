import { Fragment, useId, type ReactNode } from 'react';

/**
 * Les dessins du cahier (14 novembre 2026) : une courbe, un schéma ou un croquis légendé, à recopier sous le texte
 * du cahier. Rendu en SVG, à la craie, lisible sur téléphone. Le cours les porte en données (pas d'image) :
 *  - par diapositive : `slide.concentration.cahier_figures` (bulle « 📓 À écrire dans le cahier ») ;
 *  - par bloc : `seances[].blocs[].cahier_figures` (étape cahier de fin de bloc).
 * Règle des skills `cours-concentration` et `professeur` : seulement l'essentiel, axes nommés avec leurs unités.
 *
 * Coordonnées : celles des données. Avec `axes`, un repère est tracé (flèches, noms, unités, graduations) ;
 * avec `cadre`, la zone va de (0, 0) en bas à gauche à (l, h) en haut à droite, sans axes (schémas, croquis).
 */

export type CouleurCraie = 'blanc' | 'cyan' | 'jaune' | 'vert' | 'orange' | 'rose' | 'rouge' | 'bleu' | 'violet' | 'faible';
export type Pt = [number, number];
type Trait = 'plein' | 'pointille';
type Pos = 'n' | 's' | 'e' | 'o' | 'ne' | 'no' | 'se' | 'so' | 'centre';

export interface AxeFigure {
  min: number; max: number;
  /** « t », « u_C », « [H₃O⁺] » */
  nom: string;
  /** « ms », « V » ; absent si sans unité */
  unite?: string;
  /** graduations : une valeur, ou [valeur, texte] (« τ », « 5τ », « E ») */
  graduations?: (number | [number, string])[];
}

export type ElementFigure =
  /** y = expr(x), x dans [de, a] (par défaut tout l'axe x). Fonctions : exp ln log sqrt sin cos tan abs, pi, ^ */
  | { f: 'courbe'; expr: string; de?: number; a?: number; couleur?: CouleurCraie; trait?: Trait; texte?: string; texte_x?: number; pos?: Pos }
  /** ligne brisée (ou lissée), fermée ou non, flèche au bout */
  | { f: 'ligne'; pts: Pt[]; ferme?: boolean; lisse?: boolean; couleur?: CouleurCraie; trait?: Trait; fleche?: boolean; remplir?: CouleurCraie; epais?: boolean }
  | { f: 'fleche'; de: Pt; a: Pt; couleur?: CouleurCraie; trait?: Trait; texte?: string; pos?: Pos }
  /** double flèche de mesure (λ, T, d) avec son texte au milieu */
  | { f: 'cote'; de: Pt; a: Pt; t: string; couleur?: CouleurCraie; pos?: Pos }
  | { f: 'cercle'; c: Pt; r: number; couleur?: CouleurCraie; remplir?: CouleurCraie; trait?: Trait }
  /** rx, ry en unités de x et de y */
  | { f: 'ellipse'; c: Pt; rx: number; ry: number; couleur?: CouleurCraie; remplir?: CouleurCraie; trait?: Trait }
  | { f: 'rect'; de: Pt; a: Pt; couleur?: CouleurCraie; remplir?: CouleurCraie; trait?: Trait; arrondi?: boolean }
  /** arc de cercle, angles en degrés (0 = droite, sens trigonométrique) ; le rayon en unités de x */
  | { f: 'arc'; c: Pt; r: number; de: number; a: number; couleur?: CouleurCraie; trait?: Trait; fleche?: boolean }
  | { f: 'texte'; at: Pt; t: string; couleur?: CouleurCraie; taille?: 'petit' | 'normal' | 'grand'; ancre?: 'gauche' | 'centre' | 'droite' }
  | { f: 'point'; at: Pt; couleur?: CouleurCraie; t?: string; pos?: Pos; creux?: boolean }
  /** trait pointillé du point (x, y) vers les axes (repère : asymptote si un seul des deux) */
  | { f: 'repere'; x?: number; y?: number; t?: string; couleur?: CouleurCraie };

export interface VariationsFigure {
  /** valeurs de x : ['-∞', '0', '+∞'] */
  x: string[];
  /** signes de f′ entre deux valeurs, un de moins que x : ['−', '+'] ; '0' s'écrit sous la valeur avec `zeros` */
  signe?: string[];
  /** indices dans x où f′ s'annule (le « 0 » écrit sur la ligne de f′) */
  zeros?: number[];
  /** une valeur par x : niveau haut, bas ou milieu ; `v` vide si non écrite ; `barre` : valeur interdite (double barre) */
  /** `barre` au milieu : `v` s'écrit à gauche de la double barre, `v2` (niveau `niveau2`) à droite */
  f: { v: string; niveau: 'haut' | 'bas' | 'milieu'; barre?: boolean; v2?: string; niveau2?: 'haut' | 'bas' | 'milieu' }[];
  nom_x?: string; nom_derivee?: string; nom_f?: string;
}

export interface FigureCahierData {
  type: 'courbe' | 'schema' | 'croquis' | 'variations';
  titre?: string;
  /** une phrase sous le dessin : ce qu'il faut voir */
  legende?: string;
  axes?: { x: AxeFigure; y: AxeFigure };
  cadre?: { l: number; h: number };
  elements?: ElementFigure[];
  variations?: VariationsFigure;
  /** hauteur / largeur du dessin (défaut 0,6 avec axes, h/l avec cadre) */
  ratio?: number;
}

const COULEURS: Record<CouleurCraie, string> = {
  blanc: '#eef2f6', cyan: '#22d3ee', jaune: '#facc15', vert: '#4ade80', violet: '#c084fc',
  orange: '#fb923c', bleu: '#60a5fa', rouge: '#f87171', rose: '#f472b6', faible: 'rgba(226,232,240,.55)',
};
const coul = (c?: CouleurCraie, d: CouleurCraie = 'blanc') => COULEURS[c || d] || COULEURS[d];
const CRAIE = "'Patrick Hand', 'Caveat', cursive";
const W = 400;
const TAILLES = { petit: 13, normal: 16, grand: 20 } as const;

/** « u_C », « 10^{-3} » : indices et exposants en tspan (comme `Formule` dans le texte du cahier). */
function TexteCraie({ t }: { t: string }) {
  const parts: ReactNode[] = [];
  const re = /([_^])(\{[^}]+\}|[A-Za-z0-9+\-−]+)/g;
  let i = 0, m: RegExpExecArray | null, k = 0, decal = 0;
  while ((m = re.exec(t))) {
    if (m.index > i) { parts.push(<tspan key={k++} dy={-decal}>{t.slice(i, m.index)}</tspan>); decal = 0; }
    const sous = m[1] === '_';
    const d = sous ? 4 : -6;
    parts.push(<tspan key={k++} dy={d - decal} fontSize="0.7em">{m[2].replace(/[{}]/g, '')}</tspan>);
    decal = d;
    i = re.lastIndex;
  }
  if (i < t.length || decal) parts.push(<tspan key={k++} dy={-decal}>{t.slice(i)}</tspan>);
  return <>{parts}</>;
}

/** expression de x écrite comme au tableau → fonction ; `null` si un mot inconnu (rien d'autre que des maths). */
const FONCTIONS: Record<string, string> = {
  exp: 'Math.exp', ln: 'Math.log', log: 'Math.log10', sqrt: 'Math.sqrt', sin: 'Math.sin', cos: 'Math.cos',
  tan: 'Math.tan', abs: 'Math.abs', atan: 'Math.atan', pi: 'Math.PI', x: 'x', floor: 'Math.floor', sign: 'Math.sign',
};
const cacheExpr = new Map<string, ((x: number) => number) | null>();
export function compilerExpr(expr: string): ((x: number) => number) | null {
  if (cacheExpr.has(expr)) return cacheExpr.get(expr)!;
  let ok = /^[\d\s.+\-*/^(),a-z]*$/i.test(expr.replace(/−/g, '-').replace(/·|×/g, '*'));
  let js = '';
  if (ok) {
    js = expr.replace(/−/g, '-').replace(/·|×/g, '*').replace(/\^/g, '**').replace(/[a-z]+/gi, w => {
      const r = FONCTIONS[w.toLowerCase()];
      if (!r) ok = false;
      return r || '';
    });
  }
  let fn: ((x: number) => number) | null = null;
  if (ok) {
    try {
      // eslint-disable-next-line no-new-func
      const f = new Function('x', `"use strict"; return (${js});`) as (x: number) => number;
      f(1);
      fn = f;
    } catch { fn = null; }
  }
  cacheExpr.set(expr, fn);
  return fn;
}

function lisser(p: [number, number][]): string {
  if (p.length < 3) return p.map((q, i) => `${i ? 'L' : 'M'}${q[0].toFixed(1)},${q[1].toFixed(1)}`).join(' ');
  let d = `M${p[0][0].toFixed(1)},${p[0][1].toFixed(1)}`;
  for (let i = 0; i < p.length - 1; i++) {
    const p0 = p[i - 1] || p[i], p1 = p[i], p2 = p[i + 1], p3 = p[i + 2] || p2;
    const c1 = [p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6];
    const c2 = [p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6];
    d += ` C${c1[0].toFixed(1)},${c1[1].toFixed(1)} ${c2[0].toFixed(1)},${c2[1].toFixed(1)} ${p2[0].toFixed(1)},${p2[1].toFixed(1)}`;
  }
  return d;
}

const DECALAGES: Record<Pos, [number, number, 'start' | 'middle' | 'end']> = {
  n: [0, -9, 'middle'], s: [0, 18, 'middle'], e: [8, 5, 'start'], o: [-8, 5, 'end'],
  ne: [6, -7, 'start'], no: [-6, -7, 'end'], se: [6, 16, 'start'], so: [-6, 16, 'end'], centre: [0, 5, 'middle'],
};

function Repere2D({ fig, filtre, fleche }: { fig: FigureCahierData; filtre: string; fleche: (c: string) => string }) {
  const axes = fig.axes;
  const cadre = fig.cadre || { l: 10, h: 6 };
  const ratio = fig.ratio || (axes ? 0.6 : cadre.h / cadre.l);
  const H = Math.round(W * Math.min(1.4, Math.max(0.3, ratio)));
  // marges : la place des noms d'axes et des graduations
  const m = axes ? { g: 34, d: 34, h: 22, b: 30 } : { g: 8, d: 8, h: 8, b: 8 };
  const xmin = axes ? axes.x.min : 0, xmax = axes ? axes.x.max : cadre.l;
  const ymin = axes ? axes.y.min : 0, ymax = axes ? axes.y.max : cadre.h;
  const X = (x: number) => m.g + ((x - xmin) / (xmax - xmin || 1)) * (W - m.g - m.d);
  const Y = (y: number) => H - m.b - ((y - ymin) / (ymax - ymin || 1)) * (H - m.h - m.b);
  const sx = (W - m.g - m.d) / (xmax - xmin || 1), sy = (H - m.h - m.b) / (ymax - ymin || 1);
  const P = (p: Pt) => [X(p[0]), Y(p[1])] as [number, number];
  const dash = (t?: Trait) => (t === 'pointille' ? '5 5' : undefined);
  const out: ReactNode[] = [];
  let k = 0;
  const etiquette = (x: number, y: number, t: string, c: string, pos: Pos = 'n', taille = 15) => {
    const [dx, dy, a] = DECALAGES[pos] || DECALAGES.n;
    out.push(<text key={k++} x={x + dx} y={y + dy} fill={c} fontSize={taille} textAnchor={a}><TexteCraie t={t} /></text>);
  };

  if (axes) {
    // les axes passent par 0 s'il est dans l'intervalle, sinon par le bord
    const x0 = X(Math.min(Math.max(0, xmin), xmax)), y0 = Y(Math.min(Math.max(0, ymin), ymax));
    const ca = COULEURS.blanc;
    out.push(<line key={k++} x1={m.g - 4} y1={y0} x2={W - m.d + 14} y2={y0} stroke={ca} strokeWidth={1.6} markerEnd={fleche(ca)} />);
    out.push(<line key={k++} x1={x0} y1={H - m.b + 4} x2={x0} y2={m.h - 12} stroke={ca} strokeWidth={1.6} markerEnd={fleche(ca)} />);
    const nomX = axes.x.unite ? `${axes.x.nom} (${axes.x.unite})` : axes.x.nom;
    const nomY = axes.y.unite ? `${axes.y.nom} (${axes.y.unite})` : axes.y.nom;
    out.push(<text key={k++} x={W - 2} y={y0 + 22} fill={ca} fontSize={15} textAnchor="end"><TexteCraie t={nomX} /></text>);
    out.push(<text key={k++} x={x0 + 8} y={m.h - 6} fill={ca} fontSize={15} textAnchor="start"><TexteCraie t={nomY} /></text>);
    for (const g of axes.x.graduations || []) {
      const [v, t] = Array.isArray(g) ? g : [g, String(g)];
      out.push(<line key={k++} x1={X(v)} y1={y0 - 4} x2={X(v)} y2={y0 + 4} stroke={ca} strokeWidth={1.4} />);
      out.push(<text key={k++} x={X(v)} y={y0 + 17} fill={COULEURS.faible} fontSize={13} textAnchor="middle"><TexteCraie t={t} /></text>);
    }
    for (const g of axes.y.graduations || []) {
      const [v, t] = Array.isArray(g) ? g : [g, String(g)];
      out.push(<line key={k++} x1={x0 - 4} y1={Y(v)} x2={x0 + 4} y2={Y(v)} stroke={ca} strokeWidth={1.4} />);
      out.push(<text key={k++} x={x0 - 7} y={Y(v) + 4} fill={COULEURS.faible} fontSize={13} textAnchor="end"><TexteCraie t={t} /></text>);
    }
  }

  for (const e of fig.elements || []) {
    const c = coul(e.couleur, e.f === 'repere' ? 'faible' : e.f === 'courbe' ? 'cyan' : 'blanc');
    switch (e.f) {
      case 'courbe': {
        const fn = compilerExpr(e.expr);
        if (!fn) break;
        const de = e.de ?? xmin, a = e.a ?? xmax;
        const marge = (ymax - ymin) * 0.08;
        const morceaux: [number, number][][] = [[]];
        const N = 160;
        for (let i = 0; i <= N; i++) {
          const x = de + ((a - de) * i) / N;
          let y: number;
          try { y = fn(x); } catch { y = NaN; }
          if (!Number.isFinite(y) || y > ymax + marge || y < ymin - marge) {
            if (morceaux[morceaux.length - 1].length) morceaux.push([]);
            continue;
          }
          morceaux[morceaux.length - 1].push([X(x), Y(y)]);
        }
        for (const mc of morceaux) if (mc.length > 1) {
          out.push(<path key={k++} d={mc.map((q, i) => `${i ? 'L' : 'M'}${q[0].toFixed(1)},${q[1].toFixed(1)}`).join(' ')} fill="none" stroke={c} strokeWidth={2.4} strokeDasharray={dash(e.trait)} strokeLinecap="round" strokeLinejoin="round" filter={filtre} />);
        }
        if (e.texte) {
          const tx = e.texte_x ?? (de + (a - de) * 0.85);
          let ty = NaN; try { ty = fn(tx); } catch { /* rien */ }
          if (Number.isFinite(ty)) etiquette(X(tx), Y(Math.min(ymax, Math.max(ymin, ty))), e.texte, c, e.pos || 'n');
        }
        break;
      }
      case 'ligne': {
        const p = e.pts.map(P);
        if (p.length < 2) break;
        let d = e.lisse ? lisser(e.ferme ? [...p, p[0]] : p) : p.map((q, i) => `${i ? 'L' : 'M'}${q[0].toFixed(1)},${q[1].toFixed(1)}`).join(' ');
        if (e.ferme && !e.lisse) d += ' Z';
        out.push(<path key={k++} d={d} fill={e.remplir ? coul(e.remplir) : 'none'} fillOpacity={e.remplir ? 0.18 : undefined} stroke={c} strokeWidth={e.epais ? 3.2 : 2.2} strokeDasharray={dash(e.trait)} strokeLinecap="round" strokeLinejoin="round" markerEnd={e.fleche ? fleche(c) : undefined} filter={filtre} />);
        break;
      }
      case 'fleche': {
        const [x1, y1] = P(e.de), [x2, y2] = P(e.a);
        out.push(<line key={k++} x1={x1} y1={y1} x2={x2} y2={y2} stroke={c} strokeWidth={2} strokeDasharray={dash(e.trait)} markerEnd={fleche(c)} filter={filtre} />);
        if (e.texte) etiquette((x1 + x2) / 2, (y1 + y2) / 2, e.texte, c, e.pos || 'n');
        break;
      }
      case 'cote': {
        const [x1, y1] = P(e.de), [x2, y2] = P(e.a);
        out.push(<line key={k++} x1={x1} y1={y1} x2={x2} y2={y2} stroke={c} strokeWidth={1.6} markerStart={fleche(c)} markerEnd={fleche(c)} />);
        etiquette((x1 + x2) / 2, (y1 + y2) / 2, e.t, c, e.pos || 'n');
        break;
      }
      case 'cercle': {
        const [cx, cy] = P(e.c);
        out.push(<ellipse key={k++} cx={cx} cy={cy} rx={Math.abs(e.r * sx)} ry={Math.abs(e.r * sx)} fill={e.remplir ? coul(e.remplir) : 'none'} fillOpacity={e.remplir ? 0.22 : undefined} stroke={c} strokeWidth={2.2} strokeDasharray={dash(e.trait)} filter={filtre} />);
        break;
      }
      case 'ellipse': {
        const [cx, cy] = P(e.c);
        out.push(<ellipse key={k++} cx={cx} cy={cy} rx={Math.abs(e.rx * sx)} ry={Math.abs(e.ry * sy)} fill={e.remplir ? coul(e.remplir) : 'none'} fillOpacity={e.remplir ? 0.22 : undefined} stroke={c} strokeWidth={2.2} strokeDasharray={dash(e.trait)} filter={filtre} />);
        break;
      }
      case 'rect': {
        const [x1, y1] = P(e.de), [x2, y2] = P(e.a);
        out.push(<rect key={k++} x={Math.min(x1, x2)} y={Math.min(y1, y2)} width={Math.abs(x2 - x1)} height={Math.abs(y2 - y1)} rx={e.arrondi ? 8 : 0} fill={e.remplir ? coul(e.remplir) : 'none'} fillOpacity={e.remplir ? 0.22 : undefined} stroke={c} strokeWidth={2.2} strokeDasharray={dash(e.trait)} filter={filtre} />);
        break;
      }
      case 'arc': {
        const [cx, cy] = P(e.c);
        const r = Math.abs(e.r * sx);
        const a1 = (e.de * Math.PI) / 180, a2 = (e.a * Math.PI) / 180;
        const x1 = cx + r * Math.cos(a1), y1 = cy - r * Math.sin(a1), x2 = cx + r * Math.cos(a2), y2 = cy - r * Math.sin(a2);
        const grand = Math.abs(e.a - e.de) > 180 ? 1 : 0, sens = e.a > e.de ? 0 : 1;
        out.push(<path key={k++} d={`M${x1.toFixed(1)},${y1.toFixed(1)} A${r.toFixed(1)},${r.toFixed(1)} 0 ${grand} ${sens} ${x2.toFixed(1)},${y2.toFixed(1)}`} fill="none" stroke={c} strokeWidth={2.2} strokeDasharray={dash(e.trait)} markerEnd={e.fleche ? fleche(c) : undefined} filter={filtre} />);
        break;
      }
      case 'texte': {
        const [x, y] = P(e.at);
        const a = e.ancre === 'gauche' ? 'start' : e.ancre === 'droite' ? 'end' : 'middle';
        out.push(<text key={k++} x={x} y={y + 5} fill={c} fontSize={TAILLES[e.taille || 'normal']} textAnchor={a}><TexteCraie t={e.t} /></text>);
        break;
      }
      case 'point': {
        const [x, y] = P(e.at);
        out.push(<circle key={k++} cx={x} cy={y} r={4} fill={e.creux ? '#1d2b22' : c} stroke={c} strokeWidth={1.8} />);
        if (e.t) etiquette(x, y, e.t, c, e.pos || 'ne');
        break;
      }
      case 'repere': {
        if (!axes) break;
        const x0 = X(Math.min(Math.max(0, xmin), xmax)), y0 = Y(Math.min(Math.max(0, ymin), ymax));
        if (e.x !== undefined && e.y !== undefined) {
          out.push(<path key={k++} d={`M${X(e.x)},${y0} L${X(e.x)},${Y(e.y)} L${x0},${Y(e.y)}`} fill="none" stroke={c} strokeWidth={1.5} strokeDasharray="4 4" />);
          if (e.t) etiquette(X(e.x), Y(e.y), e.t, c, 'ne');
        } else if (e.x !== undefined) {
          out.push(<line key={k++} x1={X(e.x)} y1={Y(ymin)} x2={X(e.x)} y2={Y(ymax)} stroke={c} strokeWidth={1.5} strokeDasharray="5 5" />);
          if (e.t) etiquette(X(e.x), Y(ymax), e.t, c, 'e', 14);
        } else if (e.y !== undefined) {
          out.push(<line key={k++} x1={X(xmin)} y1={Y(e.y)} x2={X(xmax)} y2={Y(e.y)} stroke={c} strokeWidth={1.5} strokeDasharray="5 5" />);
          if (e.t) etiquette(X(xmax), Y(e.y), e.t, c, 'no', 14);
        }
        break;
      }
    }
  }
  return { H, contenu: out };
}

/** Le tableau de variations dessiné à la craie : x, signe de f′, flèches de f. */
function TableauVariations({ v, fleche }: { v: VariationsFigure; fleche: (c: string) => string }) {
  const n = v.x.length;
  const g = 58; // colonne des noms
  const col = (i: number) => g + 22 + ((W - g - 44) * i) / Math.max(1, n - 1);
  const avecSigne = !!v.signe?.length;
  const hX = 30, hS = avecSigne ? 30 : 0, hF = 84;
  const H = hX + hS + hF + 2;
  const out: ReactNode[] = [];
  let k = 0;
  const cb = COULEURS.blanc, cf = COULEURS.faible;
  out.push(<rect key={k++} x={1} y={1} width={W - 2} height={H - 2} fill="none" stroke={cf} strokeWidth={1.5} />);
  out.push(<line key={k++} x1={g} y1={1} x2={g} y2={H - 1} stroke={cf} strokeWidth={1.5} />);
  out.push(<line key={k++} x1={1} y1={hX} x2={W - 1} y2={hX} stroke={cf} strokeWidth={1.5} />);
  if (avecSigne) out.push(<line key={k++} x1={1} y1={hX + hS} x2={W - 1} y2={hX + hS} stroke={cf} strokeWidth={1.5} />);
  const nom = (t: string, y: number) => out.push(<text key={k++} x={g / 2} y={y} fill={COULEURS.jaune} fontSize={16} textAnchor="middle"><TexteCraie t={t} /></text>);
  nom(v.nom_x || 'x', hX / 2 + 6);
  if (avecSigne) nom(v.nom_derivee || 'f′(x)', hX + hS / 2 + 6);
  nom(v.nom_f || 'f', hX + hS + hF / 2 + 6);
  v.x.forEach((t, i) => out.push(<text key={k++} x={col(i)} y={hX / 2 + 6} fill={cb} fontSize={16} textAnchor="middle"><TexteCraie t={t} /></text>));
  if (avecSigne) {
    v.signe!.forEach((s, i) => out.push(<text key={k++} x={(col(i) + col(i + 1)) / 2} y={hX + hS / 2 + 7} fill={s.includes('+') ? COULEURS.vert : COULEURS.rose} fontSize={19} textAnchor="middle">{s}</text>));
    (v.zeros || []).forEach(i => out.push(<text key={k++} x={col(i)} y={hX + hS / 2 + 6} fill={cb} fontSize={16} textAnchor="middle">0</text>));
  }
  const yNiv = (niv: 'haut' | 'bas' | 'milieu') => hX + hS + (niv === 'haut' ? 18 : niv === 'bas' ? hF - 10 : hF / 2 + 4);
  v.f.forEach((p, i) => {
    if (p.barre) {
      out.push(<line key={k++} x1={col(i) - 2} y1={hX} x2={col(i) - 2} y2={H - 1} stroke={cb} strokeWidth={1.4} />);
      out.push(<line key={k++} x1={col(i) + 2} y1={hX} x2={col(i) + 2} y2={H - 1} stroke={cb} strokeWidth={1.4} />);
    }
    if (p.v) out.push(<text key={k++} x={col(i) + (p.barre ? (i === 0 ? 14 : -14) : 0)} y={yNiv(p.niveau)} fill={cb} fontSize={15} textAnchor={p.barre ? (i === 0 ? 'start' : 'end') : 'middle'}><TexteCraie t={p.v} /></text>);
    if (p.barre && p.v2) out.push(<text key={k++} x={col(i) + 14} y={yNiv(p.niveau2 || p.niveau)} fill={cb} fontSize={15} textAnchor="start"><TexteCraie t={p.v2} /></text>);
  });
  for (let i = 0; i < n - 1; i++) {
    const a = v.f[i], b = v.f[i + 1];
    if (!a || !b) continue;
    const na = a.barre && a.niveau2 ? a.niveau2 : a.niveau; // après une double barre, la flèche part du côté droit
    const y1 = yNiv(na) + (na === 'haut' ? 6 : -14), y2 = yNiv(b.niveau) + (b.niveau === 'haut' ? 6 : -14);
    const x1 = col(i) + 20, x2 = col(i + 1) - 20;
    out.push(<line key={k++} x1={x1} y1={y1} x2={x2} y2={y2} stroke={COULEURS.cyan} strokeWidth={2} markerEnd={fleche(COULEURS.cyan)} />);
  }
  return { H, contenu: out };
}

export function FigureCahier({ fig, compact = false, remplir = false }: { fig: FigureCahierData; compact?: boolean;
  /** le dessin prend la hauteur qu'on lui donne (écran du cahier de fin de bloc) au lieu de fixer sa largeur */
  remplir?: boolean }) {
  const id = useId().replace(/:/g, '');
  const filtre = `url(#craie-${id})`;
  const fleches = new Set<string>();
  const fleche = (c: string) => { fleches.add(c); return `url(#fl-${id}-${c.replace(/[^a-z0-9]/gi, '')})`; };
  // les marqueurs de flèche sont collectés pendant le dessin : recalculé à chaque rendu (peu d'éléments)
  const { H, contenu } = fig.type === 'variations' && fig.variations
    ? TableauVariations({ v: fig.variations, fleche })
    : Repere2D({ fig, filtre, fleche });
  return (
    <figure className={remplir ? 'flex h-full min-h-0 w-full flex-col' : `mx-auto w-full ${compact ? 'max-w-[360px]' : 'max-w-[440px]'}`} style={{ fontFamily: CRAIE }}>
      {fig.titre && <figcaption className={`mb-1 shrink-0 text-center text-amber-200 underline decoration-amber-200/30 underline-offset-4 ${remplir ? 'text-base' : 'text-lg'}`}><TexteLegende t={fig.titre} /></figcaption>}
      <svg viewBox={`0 0 ${W} ${H}`} className={remplir ? 'block min-h-0 w-full flex-1' : 'block h-auto w-full'} role="img" aria-label={[fig.titre, fig.legende].filter(Boolean).join(' — ')} style={{ fontFamily: CRAIE }}>
        <defs>
          {/* en unités du dessin : un trait seul horizontal ou vertical a une boîte plate et disparaîtrait en % */}
          <filter id={`craie-${id}`} filterUnits="userSpaceOnUse" x={-10} y={-10} width={W + 20} height={H + 20}>
            <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves={1} seed={3} result="b" />
            <feDisplacementMap in="SourceGraphic" in2="b" scale={1.6} />
          </filter>
          {[...fleches].map(c => (
            <marker key={c} id={`fl-${id}-${c.replace(/[^a-z0-9]/gi, '')}`} viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
              <path d="M0,1 L9,5 L0,9" fill="none" stroke={c} strokeWidth={1.6} strokeLinecap="round" />
            </marker>
          ))}
        </defs>
        {contenu.map((c, i) => <Fragment key={i}>{c}</Fragment>)}
      </svg>
      {fig.legende && <p className={`mt-1 shrink-0 text-center italic leading-snug text-[#e7e5c9] ${remplir ? 'line-clamp-2 text-sm' : 'text-base'}`} dir="auto"><TexteLegende t={fig.legende} /></p>}
    </figure>
  );
}

/** La légende : texte, avec indices (u_C) comme le reste du cahier. */
function TexteLegende({ t }: { t: string }) {
  const parts: ReactNode[] = [];
  const re = /([A-Za-zα-ωΑ-Ω0-9\])])([_^])(\{[^}]+\}|[A-Za-z0-9+\-−]+)/g;
  let i = 0, m: RegExpExecArray | null, k = 0;
  while ((m = re.exec(t))) {
    if (m.index > i) parts.push(t.slice(i, m.index));
    const Tag = m[2] === '_' ? 'sub' : 'sup';
    parts.push(m[1], <Tag key={k++} className="text-[0.7em]">{m[3].replace(/[{}]/g, '')}</Tag>);
    i = re.lastIndex;
  }
  if (i < t.length) parts.push(t.slice(i));
  return <>{parts}</>;
}

/** Les dessins d'un cahier, l'un sous l'autre (ou côte à côte quand la place le permet). Avec `remplir`, ils se partagent
 * la hauteur donnée, chacun réduit à sa part sans déformer : le texte du cahier n'a plus à rétrécir pour leur faire place. */
export default function FiguresCahier({ figures, compact = false, remplir = false, className = '' }: { figures?: FigureCahierData[] | null; compact?: boolean; remplir?: boolean; className?: string }) {
  if (!figures?.length) return null;
  if (remplir) return (
    <div className={`flex min-h-0 flex-col gap-3 ${className}`}>
      {figures.map((f, i) => <div key={i} className="min-h-0 flex-1"><FigureCahier fig={f} remplir /></div>)}
    </div>
  );
  return (
    <div className={`flex flex-wrap items-start justify-center gap-4 ${className}`}>
      {figures.map((f, i) => <div key={i} className="min-w-[240px] flex-1"><FigureCahier fig={f} compact={compact} /></div>)}
    </div>
  );
}
