/**
 * Les deux tracés de l'évaluation du Tronc Commun (22 novembre 2026), notés dans le navigateur :
 *  - le triangle des textures, DONNÉ comme document (domaines nommés et colorés, titres des axes au-dessus des axes) :
 *    l'élève trace chaque ligne en partant de sa graduation et en choisissant le côté auquel elle est parallèle
 *    (argile ∥ côté du sable, limon ∥ côté de l'argile, sable ∥ côté du limon), puis nomme la texture ;
 *  - l'histogramme : les comptes rangés dans le tableau (IF / nombre d'espèces), les rectangles collés montés à leur
 *    hauteur, puis les points de la courbe de fréquence posés au milieu des sommets.
 * Mêmes domaines que la simulation du cours (`tc_facteurs_edaphiques-tableau/triangle.html`).
 */
import { useState } from 'react';

export type Detail = { element: string; sur: number; obtenu: number; perte?: string };

// ─────────────────────────────── Triangle des textures ───────────────────────────────
/** sommets du triangle (A = % argile en haut, S = % sable en bas à gauche, L = % limon en bas à droite) */
const TOP: [number, number] = [210, 40], BL: [number, number] = [40, 335], BR: [number, number] = [380, 335];
function pt(A: number, S: number): [number, number] {
  const L = 100 - A - S;
  return [(A * TOP[0] + S * BL[0] + L * BR[0]) / 100, (A * TOP[1] + S * BL[1] + L * BR[1]) / 100];
}
const FAMILLES: Record<string, { nom: string; c: string }> = {
  argileuse: { nom: 'Texture argileuse', c: '#cd966e' }, sableuse: { nom: 'Texture sableuse', c: '#f5e15a' },
  limoneuse: { nom: 'Texture limoneuse', c: '#82c864' }, equilibree: { nom: 'Texture équilibrée', c: '#f5af32' },
};
/** domaines en (A, S), comme la simulation du cours */
const ZONES: { nom: string; g: string; p: [number, number][]; ici: [number, number] }[] = [
  { nom: 'Argile', g: 'argileuse', p: [[100, 0], [60, 0], [40, 20], [40, 45], [55, 45]], ici: [66, 15] },
  { nom: 'Argile limoneuse', g: 'argileuse', p: [[60, 0], [40, 0], [40, 20]], ici: [46, 5] },
  { nom: 'Argile sableuse', g: 'argileuse', p: [[55, 45], [35, 45], [35, 65]], ici: [42, 50] },
  { nom: 'Limon argileux fin', g: 'argileuse', p: [[40, 20], [40, 0], [27.5, 0], [27.5, 20]], ici: [34, 7] },
  { nom: 'Limon argileux', g: 'argileuse', p: [[40, 45], [40, 20], [27.5, 20], [27.5, 45]], ici: [34, 32] },
  { nom: 'Limon argilo-sableux', g: 'equilibree', p: [[35, 65], [35, 45], [27.5, 45], [20, 52], [20, 80]], ici: [27, 55] },
  { nom: 'Limon', g: 'equilibree', p: [[27.5, 45], [27.5, 22.5], [7, 43], [7, 52], [20, 52]], ici: [18, 42] },
  { nom: 'Limon fin', g: 'limoneuse', p: [[27.5, 22.5], [27.5, 0], [12, 0], [12, 8], [0, 20], [0, 50]], ici: [14, 18] },
  { nom: 'Limon très fin', g: 'limoneuse', p: [[12, 8], [12, 0], [0, 0], [0, 20]], ici: [5, 6] },
  { nom: 'Limon sableux', g: 'equilibree', p: [[20, 80], [20, 52], [7, 52], [7, 43], [0, 50], [0, 70], [15, 85]], ici: [9, 62] },
  { nom: 'Sable limoneux', g: 'sableuse', p: [[15, 85], [0, 70], [0, 85], [10, 90]], ici: [5, 82] },
  { nom: 'Sable', g: 'sableuse', p: [[10, 90], [0, 85], [0, 100]], ici: [2, 93] },
];

type Axe = 'argile' | 'limon' | 'sable';
/** la grandeur gardée constante le long de la ligne : parallèle au côté du sable = A constant, du limon = S constant, de l'argile = L constant */
type Garde = 'A' | 'S' | 'L';
const COTE_DE: Record<Garde, string> = { A: 'côté du sable', S: 'côté du limon', L: 'côté de l’argile' };
const GARDE_JUSTE: Record<Axe, Garde> = { argile: 'A', limon: 'L', sable: 'S' };
/** les deux directions possibles depuis un axe (les deux autres côtés) */
const DIRECTIONS: Record<Axe, Garde[]> = { argile: ['A', 'S'], limon: ['L', 'A'], sable: ['S', 'L'] };
const COULEUR: Record<Axe, string> = { argile: '#7c2d12', limon: '#c2410c', sable: '#a16207' };
export type Ligne = { v: number; garde: Garde };

/** le point de la graduation v sur l'axe, en (A, S) */
function surAxe(axe: Axe, v: number): [number, number] {
  return axe === 'argile' ? [v, 100 - v] : axe === 'limon' ? [100 - v, 0] : [0, v];
}
/** les deux bouts de la ligne qui garde constante la grandeur `garde` passant par (A, S) */
function bouts(A: number, S: number, garde: Garde): [[number, number], [number, number]] {
  const L = 100 - A - S;
  if (garde === 'A') return [[A, 100 - A], [A, 0]];
  if (garde === 'S') return [[100 - S, S], [0, S]];
  return [[100 - L, 0], [0, 100 - L]];
}

export function noterTriangle(q: { sol: { argile: number; limon: number; sable: number }; zone: string; points: number }, lignes: Partial<Record<Axe, Ligne>>, zone: string) {
  const par = (q.points - 0.5) / 3;
  const details: Detail[] = (['argile', 'limon', 'sable'] as Axe[]).map(axe => {
    const l = lignes[axe];
    const bonV = l?.v === q.sol[axe], bonneDir = l?.garde === GARDE_JUSTE[axe];
    return { element: `Ligne ${axe === 'argile' ? 'de l’argile' : axe === 'limon' ? 'du limon' : 'du sable'} : depuis ${q.sol[axe]} %, parallèle au ${COTE_DE[GARDE_JUSTE[axe]]}`,
      sur: par, obtenu: bonV && bonneDir ? par : 0,
      perte: !l ? 'ligne non tracée' : !bonV ? `partie de ${l.v} % au lieu de ${q.sol[axe]} %` : !bonneDir ? `parallèle au ${COTE_DE[l.garde]} au lieu du ${COTE_DE[GARDE_JUSTE[axe]]}` : '' };
  });
  details.push({ element: `Texture : ${q.zone}`, sur: 0.5, obtenu: zone === q.zone ? 0.5 : 0, perte: zone === q.zone ? '' : zone ? `« ${zone} » au lieu de « ${q.zone} »` : 'texture non donnée' });
  return details;
}

export function Triangle({ lignes, onLigne, correction, sol, actif }: {
  lignes: Partial<Record<Axe, Ligne>>; onLigne?: (axe: Axe, l: Ligne) => void; actif: boolean;
  /** après la réponse : les bonnes lignes en rouge pointillé */
  correction?: boolean; sol: { argile: number; limon: number; sable: number };
}) {
  const [choisi, setChoisi] = useState<{ axe: Axe; v: number } | null>(null);
  const poly = (p: [number, number][]) => p.map(([A, S]) => pt(A, S).join(',')).join(' ');
  const trait = (A: number, S: number, garde: Garde, couleur: string, pointille = false, k = '') => {
    const [[a1, s1], [a2, s2]] = bouts(A, S, garde);
    const [x1, y1] = pt(a1, s1), [x2, y2] = pt(a2, s2);
    return <line key={k} x1={x1} y1={y1} x2={x2} y2={y2} stroke={couleur} strokeWidth={pointille ? 2.5 : 3} strokeDasharray={pointille ? '7 5' : undefined} strokeLinecap="round" />;
  };
  const grad = (axe: Axe) => [10, 20, 30, 40, 50, 60, 70, 80, 90].map(v => {
    const [x, y] = pt(...surAxe(axe, v));
    const dx = axe === 'argile' ? -16 : axe === 'limon' ? 16 : 0, dy = axe === 'sable' ? 18 : 4;
    const vu = choisi?.axe === axe && choisi.v === v, trace = lignes[axe]?.v === v;
    return (
      <g key={`${axe}${v}`} onClick={() => actif && setChoisi({ axe, v })} style={{ cursor: actif ? 'pointer' : 'default' }}>
        <circle cx={x} cy={y} r={vu ? 8 : 5.5} fill={vu ? '#facc15' : trace ? COULEUR[axe] : '#fff'} stroke={COULEUR[axe]} strokeWidth={2} />
        <text x={x + dx} y={y + dy} fontSize={13} textAnchor="middle" fill="#111" fontWeight={trace ? 700 : 400}>{v}</text>
      </g>);
  });
  // les titres des axes, au-dessus de chaque axe, inclinés comme lui (règle de l'utilisateur)
  const ang = (a: [number, number], b: [number, number]) => (Math.atan2(b[1] - a[1], b[0] - a[0]) * 180) / Math.PI;
  const milieu = (a: [number, number], b: [number, number], ox: number, oy: number) => [(a[0] + b[0]) / 2 + ox, (a[1] + b[1]) / 2 + oy];
  const [gx, gy] = milieu(BL, TOP, -40, -12), [dx2, dy2] = milieu(TOP, BR, 40, -12), [bx, by] = milieu(BL, BR, 0, 44);
  return (
    <div>
      <svg viewBox="0 0 420 400" className="mx-auto block w-full max-w-[480px] select-none" style={{ fontFamily: 'system-ui, sans-serif' }}>
        {ZONES.map(z => <polygon key={z.nom} points={poly(z.p)} fill={FAMILLES[z.g].c} fillOpacity={0.35} stroke="#1d4ed8" strokeWidth={1.1} />)}
        {[10, 20, 30, 40, 50, 60, 70, 80, 90].map(v => (['A', 'S', 'L'] as Garde[]).map(g => {
          const [[a1, s1], [a2, s2]] = g === 'A' ? [[v, 100 - v], [v, 0]] : g === 'S' ? [[100 - v, v], [0, v]] : [[100 - v, 0], [0, 100 - v]];
          const [x1, y1] = pt(a1, s1), [x2, y2] = pt(a2, s2);
          return <line key={`${g}${v}`} x1={x1} y1={y1} x2={x2} y2={y2} stroke="#94a3b8" strokeWidth={0.6} />;
        }))}
        {ZONES.map(z => { const [x, y] = pt(...z.ici); return <text key={`n${z.nom}`} x={x} y={y} fontSize={9.5} textAnchor="middle" fill="#1e293b">{z.nom}</text>; })}
        <polygon points={[TOP, BL, BR].map(p => p.join(',')).join(' ')} fill="none" stroke="#111" strokeWidth={2} />
        <text x={gx} y={gy} fontSize={15} fontWeight={700} fill={COULEUR.argile} textAnchor="middle" transform={`rotate(${ang(BL, TOP)} ${gx} ${gy})`}>% argile →</text>
        <text x={dx2} y={dy2} fontSize={15} fontWeight={700} fill={COULEUR.limon} textAnchor="middle" transform={`rotate(${ang(TOP, BR)} ${dx2} ${dy2})`}>% limon →</text>
        <text x={bx} y={by} fontSize={15} fontWeight={700} fill={COULEUR.sable} textAnchor="middle">← % sable</text>
        {correction && (['argile', 'limon', 'sable'] as Axe[]).map(axe => trait(...surAxe(axe, sol[axe]), GARDE_JUSTE[axe], '#dc2626', true, `c${axe}`))}
        {(Object.entries(lignes) as [Axe, Ligne][]).map(([axe, l]) => trait(...surAxe(axe, l.v), l.garde, COULEUR[axe], false, `l${axe}`))}
        {correction && (() => { const [x, y] = pt(sol.argile, sol.sable); return <circle cx={x} cy={y} r={6} fill="#dc2626" />; })()}
        {grad('argile')}{grad('limon')}{grad('sable')}
      </svg>
      <div className="mt-1 flex flex-wrap gap-x-3 gap-y-1 text-[13px]" style={{ fontFamily: 'system-ui, sans-serif' }}>
        {Object.values(FAMILLES).map(f => <span key={f.nom} className="flex items-center gap-1"><span className="inline-block h-3 w-4 rounded-sm" style={{ background: f.c, opacity: 0.6 }} />{f.nom}</span>)}
      </div>
      {actif && (
        <div className="mt-2 rounded-md border border-slate-300 bg-slate-50 p-2 text-[15px]" style={{ fontFamily: 'system-ui, sans-serif' }}>
          {!choisi ? <p className="text-slate-700">① Clique sur une graduation d’un axe (argile, limon ou sable) pour en partir.</p> : (
            <div className="flex flex-wrap items-center gap-2">
              <span>② Depuis <b>{choisi.v} %</b> sur l’axe {choisi.axe === 'argile' ? 'de l’argile' : choisi.axe === 'limon' ? 'du limon' : 'du sable'}, la ligne est parallèle au :</span>
              {DIRECTIONS[choisi.axe].map(g => (
                <button key={g} onClick={() => { onLigne?.(choisi.axe, { v: choisi.v, garde: g }); setChoisi(null); }}
                  className="rounded-md border border-slate-500 bg-white px-2.5 py-1 hover:bg-slate-100">{COTE_DE[g]}</button>))}
              <button onClick={() => setChoisi(null)} className="text-sm text-slate-500 underline">annuler</button>
            </div>)}
        </div>)}
    </div>
  );
}

// ─────────────────────────────── Histogramme et courbe ───────────────────────────────
const IF = ['I', 'II', 'III', 'IV', 'V'];
const HX0 = 60, HY0 = 270, LARG = 62, PAS = 34, HMAX = 7;

export type Histo = { tableau: (number | null)[]; barres: (number | null)[]; points: (number | null)[] };
export const histoVide = (): Histo => ({ tableau: IF.map(() => null), barres: IF.map(() => null), points: IF.map(() => null) });

export function noterHisto(q: { comptes: number[]; points: number }, h: Histo) {
  const tiers = q.points / 3;
  const part = (nom: string, val: (number | null)[], quoi: string): Detail => {
    const faux = IF.filter((_, i) => val[i] !== q.comptes[i]);
    const ok = IF.length - faux.length;
    const obtenu = Math.round((tiers * ok) / IF.length * 4) / 4;
    return { element: nom, sur: tiers, obtenu, perte: faux.length ? `${quoi} faux pour ${faux.join(', ')}` : '' };
  };
  return [part('Tableau IF / nombre d’espèces', h.tableau, 'compte'), part('Histogramme : rectangles collés à la bonne hauteur', h.barres, 'rectangle'),
    part('Courbe de fréquence : points au milieu des sommets', h.points, 'point')];
}

export function Histogramme({ h, onH, actif, correction, comptes }: { h: Histo; onH?: (h: Histo) => void; actif: boolean; correction?: boolean; comptes: number[] }) {
  const [etape, setEtape] = useState<'tableau' | 'barres' | 'courbe'>('tableau');
  const poser = (k: keyof Histo, i: number, v: number | null) => onH?.({ ...h, [k]: h[k].map((x, j) => (j === i ? v : x)) });
  const clic = (e: React.MouseEvent<SVGSVGElement>) => {
    if (!actif || etape === 'tableau') return;
    const s = e.currentTarget, p = s.createSVGPoint(); p.x = e.clientX; p.y = e.clientY;
    const m = p.matrixTransform(s.getScreenCTM()!.inverse());
    const i = Math.floor((m.x - HX0) / LARG), v = Math.max(0, Math.min(HMAX, Math.round((HY0 - m.y) / PAS)));
    if (i < 0 || i >= IF.length) return;
    poser(etape === 'barres' ? 'barres' : 'points', i, v);
  };
  const pts = h.points.map((v, i) => (v == null ? null : [HX0 + LARG * (i + 0.5), HY0 - v * PAS] as [number, number])).filter(Boolean) as [number, number][];
  const bons = comptes.map((v, i) => [HX0 + LARG * (i + 0.5), HY0 - v * PAS]);
  return (
    <div style={{ fontFamily: 'system-ui, sans-serif' }}>
      <table className="mb-2 w-full max-w-[460px] border-collapse text-center text-[15px]">
        <tbody>
          <tr><th className="border border-black bg-slate-100 px-2 py-1 text-left">Indice de fréquence (IF)</th>{IF.map(x => <th key={x} className="border border-black bg-slate-100 px-2 py-1">{x}</th>)}</tr>
          <tr><th className="border border-black px-2 py-1 text-left">Nombre d’espèces</th>{IF.map((x, i) => (
            <td key={x} className="border border-black p-0.5">
              <input inputMode="numeric" disabled={!actif} value={h.tableau[i] ?? ''} aria-label={`Nombre d’espèces d’indice ${x}`}
                onChange={e => { const d = e.target.value.replace(/\D/g, '').slice(0, 2); poser('tableau', i, d === '' ? null : Number(d)); }}
                className={`w-10 rounded border px-1 py-0.5 text-center ${correction ? (h.tableau[i] === comptes[i] ? 'border-emerald-600' : 'border-rose-600 text-rose-700') : 'border-slate-400'}`} />
              {correction && h.tableau[i] !== comptes[i] && <span className="block text-xs text-rose-700">{comptes[i]}</span>}
            </td>))}</tr>
        </tbody>
      </table>
      {actif && (
        <div className="mb-1 flex flex-wrap gap-1.5 text-[14px]">
          {([['tableau', '① Le tableau'], ['barres', '② Les rectangles'], ['courbe', '③ La courbe']] as const).map(([k, n]) => (
            <button key={k} onClick={() => setEtape(k)} className={`rounded-md border px-2.5 py-1 ${etape === k ? 'border-black bg-black text-white' : 'border-slate-400 bg-white'}`}>{n}</button>))}
          <span className="self-center text-slate-600">{etape === 'tableau' ? 'Compte les espèces de chaque indice.' : etape === 'barres' ? 'Clique dans la colonne d’un indice, à la hauteur voulue.' : 'Clique au milieu du sommet de chaque rectangle.'}</span>
        </div>)}
      <svg viewBox="0 0 400 310" onClick={clic} className={`block w-full max-w-[460px] select-none ${actif && etape !== 'tableau' ? 'cursor-crosshair' : ''}`}>
        {Array.from({ length: HMAX + 1 }, (_, v) => (
          <g key={v}><line x1={HX0} x2={HX0 + LARG * 5} y1={HY0 - v * PAS} y2={HY0 - v * PAS} stroke="#e2e8f0" />
            <text x={HX0 - 8} y={HY0 - v * PAS + 4} fontSize={13} textAnchor="end">{v}</text></g>))}
        {correction && comptes.map((v, i) => <rect key={`c${i}`} x={HX0 + LARG * i} y={HY0 - v * PAS} width={LARG} height={v * PAS} fill="none" stroke="#dc2626" strokeWidth={2} strokeDasharray="6 4" />)}
        {/* rectangles collés les uns aux autres (règle de l'utilisateur) */}
        {h.barres.map((v, i) => (v ? <rect key={i} x={HX0 + LARG * i} y={HY0 - v * PAS} width={LARG} height={v * PAS} fill="#60a5fa" fillOpacity={0.55} stroke="#1d4ed8" strokeWidth={1.5} /> : null))}
        {correction && <polyline points={bons.map(p => p.join(',')).join(' ')} fill="none" stroke="#dc2626" strokeWidth={2} strokeDasharray="6 4" />}
        {pts.length > 1 && <polyline points={pts.map(p => p.join(',')).join(' ')} fill="none" stroke="#b91c1c" strokeWidth={2.5} />}
        {pts.map(([x, y], k) => <circle key={k} cx={x} cy={y} r={5} fill="#b91c1c" />)}
        <line x1={HX0} y1={HY0} x2={HX0 + LARG * 5 + 18} y2={HY0} stroke="#111" strokeWidth={2} />
        <line x1={HX0} y1={HY0} x2={HX0} y2={HY0 - HMAX * PAS - 14} stroke="#111" strokeWidth={2} />
        {IF.map((x, i) => <text key={x} x={HX0 + LARG * (i + 0.5)} y={HY0 + 20} fontSize={14} textAnchor="middle" fontWeight={700}>{x}</text>)}
        <text x={HX0 + LARG * 5 + 20} y={HY0 + 20} fontSize={13} textAnchor="end">IF</text>
        <text x={HX0 - 4} y={HY0 - HMAX * PAS - 20} fontSize={13}>Nombre d’espèces</text>
      </svg>
    </div>
  );
}
