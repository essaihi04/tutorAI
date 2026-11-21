// Texte à trous en glisser-déposer (21/11/2026, SVT ch1 et ch2 : « faire pareil » que la traduction du ch4). Équations bilans,
// lieux des étapes, mécanisme de la contraction : chaque trou `[[réponse]]` du texte reçoit une étiquette de la réserve (les
// réponses et des leurres, triés pour ne pas souffler l'ordre). Même geste que GlisserCode : glisser à la souris ou au doigt,
// ou toucher une étiquette puis un trou ; erreur en rouge, bonne réponse en vert ; tous remplis : `onFin`.
import { useMemo, useRef, useState, type PointerEvent as PE } from 'react';
import { Formule } from './Formule';
import type { FinAssociation } from './AssociationDiapo';

const CRAIE = "'Patrick Hand', 'Caveat', cursive";

type Morceau = { texte: string } | { trou: number; attendu: string };

export default function TrousGlisser({ texte, leurres = [], fini, onFin }: {
  texte: string; leurres?: string[]; fini: boolean; onFin: (f: FinAssociation, voix: Promise<unknown>) => void;
}) {
  // « … [[6 O2]] … » → morceaux de texte et trous, ligne par ligne
  const lignes = useMemo(() => {
    let n = 0;
    return texte.split('\n').map(l => l.split(/(\[\[[^\]]+\]\])/).filter(Boolean).map<Morceau>(m => {
      const t = /^\[\[(.+)\]\]$/.exec(m);
      return t ? { trou: n++, attendu: t[1].trim() } : { texte: m };
    }));
  }, [texte]);
  const attendus = useMemo(() => lignes.flat().flatMap(m => ('trou' in m ? [m.attendu] : [])), [lignes]);
  const reserve = useMemo(() => [...new Set([...attendus, ...leurres])].sort((a, b) => a.localeCompare(b, 'fr')), [attendus, leurres]);
  const [poses, setPoses] = useState<(string | null)[]>(() => attendus.map(() => null));
  const [faux, setFaux] = useState<Record<number, string>>({});
  const [choisie, setChoisie] = useState<string | null>(null);
  const [message, setMessage] = useState<{ ok: boolean; t: string } | null>(null);
  const [fantome, setFantome] = useState<{ v: string; x: number; y: number } | null>(null);
  const erreurs = useRef(0), termine = useRef(false);

  const poser = (i: number, v: string) => {
    setChoisie(null);
    if (fini || termine.current || poses[i]) return;
    if (v === attendus[i]) {
      const n = poses.map((p, j) => (j === i ? v : p));
      setPoses(n);
      setMessage({ ok: true, t: v });
      if (n.every(Boolean)) {
        termine.current = true;
        const sans = erreurs.current === 0;
        const complet = lignes.map(l => l.map(m => ('trou' in m ? m.attendu : m.texte)).join('')).join(' ; ');
        window.setTimeout(() => onFin({ correct: sans, tentative: sans ? 1 : 2, reponse: n.join(' | '),
          ecrit: `${complet}${sans ? ' — sans erreur.' : ` — ${erreurs.current} erreur${erreurs.current > 1 ? 's' : ''} corrigée${erreurs.current > 1 ? 's' : ''}.`}` }, Promise.resolve()), 350);
      }
    } else {
      erreurs.current += 1;
      setFaux(f => ({ ...f, [i]: v }));
      setMessage({ ok: false, t: `« ${v} » ne va pas ici.` });
      window.setTimeout(() => setFaux(f => { const g = { ...f }; delete g[i]; return g; }), 900);
    }
  };

  const depart = useRef<{ v: string; x: number; y: number; bouge: boolean } | null>(null);
  const surDown = (v: string) => (e: PE) => { if (fini) return; depart.current = { v, x: e.clientX, y: e.clientY, bouge: false }; (e.target as HTMLElement).setPointerCapture?.(e.pointerId); };
  const surMove = (e: PE) => { const d = depart.current; if (!d) return; if (!d.bouge && Math.hypot(e.clientX - d.x, e.clientY - d.y) > 6) d.bouge = true; if (d.bouge) setFantome({ v: d.v, x: e.clientX, y: e.clientY }); };
  const surUp = (e: PE) => {
    const d = depart.current; depart.current = null; setFantome(null);
    if (!d) return;
    if (!d.bouge) { setChoisie(c => (c === d.v ? null : d.v)); return; }
    const el = document.elementsFromPoint(e.clientX, e.clientY).find(x => (x as HTMLElement).dataset?.trouGlisser !== undefined) as HTMLElement | undefined;
    if (el) poser(Number(el.dataset.trouGlisser), d.v);
  };

  return (
    <div className="mt-3 flex select-none flex-col gap-4 sm:flex-row sm:items-start" style={{ fontFamily: CRAIE }}>
      <div className="flex min-w-0 flex-1 flex-col gap-3">
      <div className="flex flex-col gap-1.5 text-lg leading-relaxed text-white/90">
        {lignes.map((l, k) => (
          <p key={k} className="flex flex-wrap items-center gap-x-1.5 gap-y-2">
            {l.map((m, j) => 'trou' in m ? (
              <button key={j} type="button" data-trou-glisser={m.trou} onClick={() => choisie && poser(m.trou, choisie)}
                className={`inline-flex h-9 min-w-[88px] items-center justify-center rounded-md border-2 border-dashed px-2 text-base transition ${
                  poses[m.trou] ? 'border-solid border-emerald-400 bg-emerald-500/20 text-emerald-100'
                    : faux[m.trou] ? 'border-solid border-rose-400 bg-rose-500/25 text-rose-100'
                      : choisie ? 'border-amber-200/70 bg-amber-200/10 text-white/40' : 'border-white/30 text-white/30'}`}>
                {poses[m.trou] || faux[m.trou] ? <Formule t={(poses[m.trou] || faux[m.trou])!} /> : '?'}
              </button>
            ) : <span key={j}><Formule t={m.texte} /></span>)}
          </p>
        ))}
      </div>
      {message && <p className={`text-base ${message.ok ? 'text-emerald-300' : 'text-rose-300'}`}>{message.ok ? '✔ ' : '✘ '}<Formule t={message.t} /></p>}
      </div>
      {!fini && (
        <div className="sm:w-[42%] sm:shrink-0">
          <p className="mb-1.5 text-sm text-amber-200">Étiquettes à glisser dans les trous</p>
          <div className="flex flex-wrap gap-2">
            {reserve.map(v => (
              <span key={v} onPointerDown={surDown(v)} onPointerMove={surMove} onPointerUp={surUp} onPointerCancel={() => { depart.current = null; setFantome(null); }}
                className={`cursor-grab touch-none rounded-md border px-2.5 py-1 text-base text-white ${choisie === v ? 'border-amber-200 bg-amber-200/25' : 'border-white/30 bg-white/10 hover:bg-white/20'}`}>
                <Formule t={v} />
              </span>
            ))}
          </div>
          <p className="mt-1 text-xs text-white/45">Glisse, ou touche une étiquette puis un trou.</p>
        </div>
      )}
      {fantome && (
        <span className="pointer-events-none fixed z-[100] -translate-x-1/2 -translate-y-1/2 rounded-md border border-amber-200 bg-[#1e293b] px-2 py-1 text-base text-amber-100 shadow-xl"
          style={{ left: fantome.x, top: fantome.y, fontFamily: CRAIE }}><Formule t={fantome.v} /></span>
      )}
    </div>
  );
}
