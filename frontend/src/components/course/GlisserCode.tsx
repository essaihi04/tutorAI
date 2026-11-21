// Exercice « glisser-déposer » de la transcription et de la traduction (21/11/2026, demande de l'utilisateur : « un exercice de
// glisser-déposer de plusieurs acides aminés ; le tableau sert à glisser-déposer, soit dans la transcription soit dans la
// traduction »).
//  - traduction : les codons de l'ARNm en haut, une case vide sous chacun ; l'élève glisse l'acide aminé depuis l'extrait du
//    tableau du code génétique (ses lignes sont les étiquettes à glisser), codons de leurre compris ;
//  - transcription : les bases du brin transcrit en haut ; l'élève glisse le nucléotide d'ARN (A, U, G, C, et T en leurre).
// Glisser à la souris ou au doigt, ou toucher une étiquette puis une case. Une erreur rougit la case et dit pourquoi ; la
// bonne réponse s'y pose en vert. Toutes les cases remplies : `onFin` (même forme que la fin d'une association).
import { useEffect, useMemo, useRef, useState, type PointerEvent as PE } from 'react';
import { CODE_GENETIQUE, NOMS_ACIDES } from './TableauCode';
import type { FinAssociation } from './AssociationDiapo';
import TrousGlisser from './TrousGlisser';

export interface GlisserCodeData {
  /** complementaire (SVT ch3) : le brin d'ADN complémentaire, nucléotide par nucléotide (réplication) */
  sens: 'traduction' | 'transcription' | 'complementaire' | 'trous';
  /** traduction : les codons de l'ARNm (« AUG GCU … ») ; transcription : le brin transcrit de l'ADN, par triplets */
  sequence?: string;
  /** traduction : codons de leurre ajoutés au tableau ; trous : étiquettes de leurre */
  leurres?: string[];
  /** trous (SVT ch1, ch2) : le texte, les trous écrits `[[réponse]]`, une ligne par « 
 » */
  texte?: string;
  /** l'orientation écrite au bout des brins (ex. « 3′ » … « 5′ ») */
  bouts?: [string, string];
}

const CRAIE = "'Patrick Hand', 'Caveat', cursive";
const COMP: Record<string, string> = { A: 'U', T: 'A', G: 'C', C: 'G' };          // ADN → ARN (transcription)
const COMP_ADN: Record<string, string> = { A: 'T', T: 'A', G: 'C', C: 'G' };      // ADN → ADN (brin complémentaire)

type Case = { haut: string; attendu: string; pose: string | null; faux: string | null };

type Props = { g: GlisserCodeData; fini: boolean; actif?: boolean; onFin: (f: FinAssociation, voix: Promise<unknown>) => void };

export default function GlisserCode(p: Props) {
  if (p.g.sens === 'trous') return <TrousGlisser texte={p.g.texte || ''} leurres={p.g.leurres} fini={p.fini} onFin={p.onFin} />;
  return <GlisserSequence {...p} />;
}

function GlisserSequence({ g, fini, actif = true, onFin }: Props) {
  const traduction = g.sens === 'traduction', adn = g.sens === 'complementaire';
  const groupes = (g.sequence || '').trim().toUpperCase().split(/\s+/);
  const init = (): Case[] => traduction
    ? groupes.map(c => ({ haut: c, attendu: NOMS_ACIDES[CODE_GENETIQUE[c.replace(/T/g, 'U')]]?.[0] || '?', pose: null, faux: null }))
    : groupes.join('').split('').map(b => ({ haut: b, attendu: (adn ? COMP_ADN : COMP)[b] || '?', pose: null, faux: null }));
  const [cases, setCases] = useState<Case[]>(init);
  const [choisie, setChoisie] = useState<string | null>(null);
  const [message, setMessage] = useState<{ ok: boolean; t: string } | null>(null);
  const erreurs = useRef(0);
  const termine = useRef(false);
  const [fantome, setFantome] = useState<{ v: string; x: number; y: number } | null>(null);

  // les étiquettes : les lignes du tableau (traduction, triées pour ne pas souffler l'ordre) ou les 5 nucléotides
  const etiquettes = useMemo(() => {
    if (!traduction) return (adn ? ['A', 'T', 'G', 'C', 'U'] : ['A', 'U', 'G', 'C', 'T']).map(n => ({ v: n, codon: '' }));
    const codons = [...new Set([...groupes, ...(g.leurres || [])].map(c => c.replace(/T/g, 'U')))].filter(c => CODE_GENETIQUE[c]).sort();
    return codons.map(c => ({ v: NOMS_ACIDES[CODE_GENETIQUE[c]][0], codon: c }));
  }, [g.sequence, g.leurres]); // eslint-disable-line react-hooks/exhaustive-deps

  // (les effets hors du « setCases » : en mode strict, React rejoue les fonctions de mise à jour)
  const poser = (i: number, v: string) => {
    setChoisie(null);
    const c = cases[i];
    if (fini || termine.current || !c || c.pose) return;
    const juste = v === c.attendu;
    const n = cases.map((x, j) => (j === i ? { ...x, pose: juste ? v : null, faux: juste ? null : v } : x));
    setCases(n);
    if (juste) setMessage({ ok: true, t: traduction ? `${c.haut} → ${v}` : `en face de ${c.haut} : ${v}` });
    else {
      erreurs.current += 1;
      setMessage({ ok: false, t: traduction
        ? `Non : cherche la ligne ${c.haut} dans le tableau.`
        : adn && v === 'U' ? 'Non : U n’existe pas dans l’ADN (c’est la base de l’ARN).'
          : !adn && c.haut === 'A' ? 'Non : en face de A, l’ARN met U (pas de T dans l’ARN).' : `Non : en face de ${c.haut}, la base complémentaire est ${c.attendu}.` });
      window.setTimeout(() => setCases(cc => cc.map((x, j) => (j === i ? { ...x, faux: null } : x))), 900);
    }
    if (n.every(x => x.pose)) {
      termine.current = true;
      const sans = erreurs.current === 0;
      const resultat = traduction ? n.map(x => x.pose).filter(v => v !== 'Stop').join(' – ') + (n.some(x => x.pose === 'Stop') ? ' (codon stop : la chaîne s’arrête)' : '') : (b => (g.bouts ? `${g.bouts[1]} ${b} ${g.bouts[0]}` : b))(n.map(x => x.pose).join('').replace(/(.{3})/g, '$1 ').trim());   // le brin écrit en face a les extrémités inverses
      window.setTimeout(() => onFin({
        correct: sans, tentative: sans ? 1 : 2, reponse: resultat,
        ecrit: `${traduction ? 'Séquence d’acides aminés' : adn ? 'Brin complémentaire' : 'ARNm'} : ${resultat}${sans ? ' — sans erreur.' : ` — ${erreurs.current} erreur${erreurs.current > 1 ? 's' : ''} corrigée${erreurs.current > 1 ? 's' : ''}.`}`,
      }, Promise.resolve()), 350);
    }
  };

  // glisser au doigt ou à la souris : un fantôme suit le pointeur ; au lâcher, la case sous le pointeur reçoit l'étiquette
  const depart = useRef<{ v: string; x: number; y: number; bouge: boolean } | null>(null);
  const surDown = (v: string) => (e: PE) => {
    if (fini) return;
    depart.current = { v, x: e.clientX, y: e.clientY, bouge: false };
    (e.target as HTMLElement).setPointerCapture?.(e.pointerId);
  };
  const surMove = (e: PE) => {
    const d = depart.current; if (!d) return;
    if (!d.bouge && Math.hypot(e.clientX - d.x, e.clientY - d.y) > 6) d.bouge = true;
    if (d.bouge) setFantome({ v: d.v, x: e.clientX, y: e.clientY });
  };
  const surUp = (e: PE) => {
    const d = depart.current; depart.current = null; setFantome(null);
    if (!d) return;
    if (!d.bouge) { setChoisie(c => (c === d.v ? null : d.v)); return; }   // un simple toucher : l'étiquette est choisie
    const el = document.elementsFromPoint(e.clientX, e.clientY).find(x => (x as HTMLElement).dataset?.caseGlisser !== undefined) as HTMLElement | undefined;
    if (el) poser(Number(el.dataset.caseGlisser), d.v);
  };
  useEffect(() => { if (!actif) { depart.current = null; setFantome(null); } }, [actif]);

    return (
    <div className="mt-3 flex flex-col gap-4 select-none sm:flex-row sm:items-start" style={{ fontFamily: CRAIE }}>
      <div className="flex min-w-0 flex-1 flex-col gap-3">
      {/* les brins : en haut la séquence donnée, dessous les cases à remplir */}
      <div className="flex flex-wrap items-end gap-x-1 gap-y-3">
        {g.bouts && <span className="pb-9 text-sm text-emerald-300">{g.bouts[0]}</span>}
        {/* transcription : les bases par triplets, un triplet ne se coupe jamais en fin de ligne */}
        {(traduction ? cases.map((_, i) => [i]) : Array.from({ length: Math.ceil(cases.length / 3) }, (_, t) => [3 * t, 3 * t + 1, 3 * t + 2].filter(i => i < cases.length))).map((ids, t) => (
          <div key={t} className={`flex gap-1 ${traduction ? '' : 'mr-1.5'}`}>
            {ids.map(i => { const c = cases[i]; return (
              <div key={i} className="flex flex-col items-center gap-1">
                <span className={`rounded-md border border-sky-300/40 bg-sky-400/10 text-center tracking-wider text-sky-100 ${traduction ? 'px-2 py-0.5 text-lg' : 'w-7 py-0.5 text-lg sm:w-8'}`}>{c.haut}</span>
                <button
                  type="button" data-case-glisser={i}
                  onClick={() => choisie && poser(i, choisie)}
                  className={`flex items-center justify-center rounded-md border-2 border-dashed text-lg transition ${traduction ? 'h-9 min-w-[60px] px-2' : 'h-9 w-7 sm:w-8'} ${
                    c.pose ? 'border-solid border-emerald-400 bg-emerald-500/20 text-emerald-100'
                      : c.faux ? 'border-solid border-rose-400 bg-rose-500/25 text-rose-100'
                        : choisie ? 'border-amber-200/70 bg-amber-200/10 text-white/40' : 'border-white/30 text-white/30'}`}
                  aria-label={c.pose ? `${c.haut} : ${c.pose}` : `Case sous ${c.haut}`}>
                  {c.pose || c.faux || '?'}
                </button>
              </div>
            ); })}
          </div>
        ))}
        {g.bouts && <span className="pb-9 text-sm text-emerald-300">{g.bouts[1]}</span>}
      </div>

      {message && <p className={`text-base ${message.ok ? 'text-emerald-300' : 'text-rose-300'}`}>{message.ok ? '✔ ' : '✘ '}{message.t}</p>}
      </div>

      {/* la réserve : le tableau du code (traduction) ou les nucléotides (transcription) */}
      {!fini && (
        <div className="shrink-0">
          <p className="mb-1.5 text-sm text-amber-200">
            {traduction ? 'Extrait du tableau du code génétique : glisse l’acide aminé sous son codon' : adn ? 'Nucléotides d’ADN à glisser' : 'Nucléotides d’ARN à glisser'}
          </p>
          {traduction ? (
            <table className="border-collapse text-[15px]">
              <thead><tr className="text-cyan-200"><th className="border border-white/20 px-2 py-0.5 text-left">Codon</th><th className="border border-white/20 px-2 py-0.5 text-left">Acide aminé</th></tr></thead>
              <tbody>
                {etiquettes.map(e => (
                  <tr key={e.codon}>
                    <td className="border border-white/20 px-2 py-0.5 tracking-wider text-white">{e.codon}</td>
                    <td className="border border-white/20 px-1 py-0.5">
                      <span onPointerDown={surDown(e.v)} onPointerMove={surMove} onPointerUp={surUp} onPointerCancel={() => { depart.current = null; setFantome(null); }}
                        className={`inline-block cursor-grab touch-none rounded-md border px-2 py-0.5 text-white ${choisie === e.v ? 'border-amber-200 bg-amber-200/25' : 'border-white/30 bg-white/10 hover:bg-white/20'}`}>{e.v}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <div className="flex gap-2">
              {etiquettes.map(e => (
                <span key={e.v} onPointerDown={surDown(e.v)} onPointerMove={surMove} onPointerUp={surUp} onPointerCancel={() => { depart.current = null; setFantome(null); }}
                  className={`flex h-10 w-10 cursor-grab touch-none items-center justify-center rounded-md border text-xl text-white ${choisie === e.v ? 'border-amber-200 bg-amber-200/25' : 'border-white/30 bg-white/10 hover:bg-white/20'}`}>{e.v}</span>
              ))}
            </div>
          )}
          <p className="mt-1 max-w-[230px] text-xs text-white/45">Glisse, ou touche une étiquette puis une case.</p>
        </div>
      )}
      {fantome && (
        <span className="pointer-events-none fixed z-[100] -translate-x-1/2 -translate-y-1/2 rounded-md border border-amber-200 bg-[#1e293b] px-2 py-1 text-lg text-amber-100 shadow-xl"
          style={{ left: fantome.x, top: fantome.y, fontFamily: CRAIE }}>{fantome.v}</span>
      )}
    </div>
  );
}
