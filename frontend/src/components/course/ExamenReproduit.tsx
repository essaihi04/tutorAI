import { useLayoutEffect, useRef, useState, type CSSProperties } from 'react';
import type { BlocExamen, PageExamen } from './types';
import { Formule } from './Formule';

/**
 * L'exercice d'un sujet du national REPRODUIT en code (19 novembre 2026, demande de l'utilisateur : « si l'exercice est
 * divisé en deux pages, c'est mieux de le lire et de le reproduire avec le code, comme un vrai examen avec en-tête et
 * tout »). Une seule feuille de papier : l'en-tête de l'examen (écrit en code, ou la bande du scan), puis tout l'exercice
 * en police d'examen — titre sur bande grise, énoncé, questions numérotées avec leurs points, propositions A-D, tableau,
 * figure du sujet. La taille est la plus grande qui fait TOUT tenir (une colonne, ou deux sur écran large), jamais sous
 * 15 px ; jamais de défilement. Le bloc que le tuteur lit se surligne au feutre.
 */

const POLICE = "'Times New Roman', 'Liberation Serif', 'Nimbus Roman', Times, serif";
const LARGEUR_MAX = 1120;
const PLUS_PETIT = 15, PLUS_GRAND = 26;
const A4 = { w: 1654, h: 2339 };

export default function ExamenReproduit({ e, actif }: {
  e: PageExamen;
  /** le bloc lu par le tuteur (-1 : aucun) */
  actif: number;
}) {
  const r = e.reproduction!;
  const cadre = useRef<HTMLDivElement>(null);
  const corps = useRef<HTMLDivElement>(null);
  const [place, setPlace] = useState({ w: 0, h: 0 });
  // `figure` : l'échelle des figures (elles rétrécissent avant le texte) ; `defile` : même à 15 px et figures réduites,
  // l'exercice ne tient pas (téléphone en paysage) — seul cas où la feuille défile, plutôt qu'un texte illisible ou coupé
  const [mise, setMise] = useState({ taille: 18, colonnes: 1, figure: 1, defile: false });
  const [dimEntete, setDimEntete] = useState(A4);
  useLayoutEffect(() => {
    const el = cadre.current;
    if (!el) return;
    const lire = () => setPlace({ w: el.clientWidth, h: el.clientHeight });
    lire();
    const ro = new ResizeObserver(lire);
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  const W = Math.floor(Math.min(LARGEUR_MAX, Math.max(200, place.w - 8)));
  const H = Math.floor(Math.max(120, place.h - 8));
  // En-tête du scan (sans en-tête écrit) : une bande de la page, au plus 22 % de la feuille ; le reste est à l'exercice.
  const bandeScan = !r.entete && e.entete !== false ? { page: e.entete?.page || e.page, haut: e.entete?.haut ?? 0, bas: e.entete?.bas ?? 0.115 } : null;
  const hBandeScan = bandeScan ? Math.min(H * 0.22, (bandeScan.bas - bandeScan.haut) * (dimEntete.h / dimEntete.w) * W) : 0;
  const lBandeScan = bandeScan ? hBandeScan / ((bandeScan.bas - bandeScan.haut) * (dimEntete.h / dimEntete.w)) : 0;

  // La plus grande écriture qui fait tout tenir : une colonne, ou deux si la feuille est large.
  useLayoutEffect(() => {
    const c = corps.current;
    if (!c || !place.w) return;
    const ajuster = () => {
    let meilleure: typeof mise | null = null;
    c.style.overflowY = 'hidden';
    for (const figure of [1, 0.8, 0.65, 0.5]) {
      c.style.setProperty('--figure', String(figure));
      for (const colonnes of W >= 640 ? [1, 2] : [1]) {
        c.style.columnCount = String(colonnes);
        for (let t = PLUS_GRAND; t >= PLUS_PETIT; t--) {
          c.style.fontSize = `${t}px`;
          if (c.scrollHeight <= c.clientHeight + 1 && c.scrollWidth <= c.clientWidth + 1) {
            if (!meilleure || t > meilleure.taille) meilleure = { taille: t, colonnes, figure, defile: false };
            break;
          }
        }
      }
      if (meilleure) break;                                          // la figure garde la plus grande taille qui permet de tout tenir
    }
    const m2 = meilleure || { taille: PLUS_PETIT, colonnes: 1, figure: 0.65, defile: true };
    c.style.columnCount = String(m2.colonnes); c.style.fontSize = `${m2.taille}px`; c.style.setProperty('--figure', String(m2.figure));
    c.style.overflowY = m2.defile ? 'auto' : 'hidden';
    setMise(m => (m.taille === m2.taille && m.colonnes === m2.colonnes && m.figure === m2.figure && m.defile === m2.defile ? m : m2));
    };
    ajuster();
  }, [place, W, H, r, hBandeScan]);

  // la feuille défile (petit écran) : elle suit le bloc que le tuteur lit
  useLayoutEffect(() => {
    const c = corps.current;
    if (!mise.defile || !c || actif < 0) return;
    const el = c.querySelector<HTMLElement>(`[data-bloc="${actif}"]`);
    if (el) c.scrollTo({ top: Math.max(0, el.offsetTop - c.offsetTop - 8), behavior: 'smooth' });
  }, [actif, mise.defile]);

  const surligne = (i: number) => (i === actif ? { background: 'rgba(253,224,71,.45)', boxShadow: '0 0 0 3px rgba(253,224,71,.45)', borderRadius: 3 } : {});
  const bloc = (b: BlocExamen, i: number) => {
    const style = { breakInside: 'avoid' as const, transition: 'background .3s', ...surligne(i) };
    switch (b.type) {
      case 'titre':
        return <p key={i} data-bloc={i} style={{ ...style, background: i === actif ? style.background : '#d9d9d9', fontWeight: 700, padding: '.1em .35em', margin: '.2em 0 .35em' }}><Formule t={b.texte} /></p>;
      case 'texte':
        return <p key={i} data-bloc={i} style={{ ...style, textIndent: '1.2em', margin: '0 0 .3em', textAlign: 'justify' }}><Formule t={b.texte} /></p>;
      case 'question':
        return (
          <p key={i} data-bloc={i} style={{ ...style, margin: '.15em 0 .3em' }}>
            <b>{b.numero}</b> <Formule t={b.texte} />{b.points ? <b> ({b.points})</b> : null}
          </p>
        );
      case 'choix':
        return (
          <table key={i} data-bloc={i} style={{ ...style, borderCollapse: 'collapse', margin: '.15em auto .3em', lineHeight: 1.2 }}>
            <tbody>{b.options.map(o => (
              <tr key={o.lettre}><td style={{ border: '1px solid #333', padding: '0 .4em', fontWeight: 700 }}>{o.lettre}</td>
                <td style={{ border: '1px solid #333', padding: '0 .4em' }}><Formule t={o.texte} /></td></tr>
            ))}</tbody>
          </table>
        );
      case 'tableau':
        return (
          <table key={i} data-bloc={i} style={{ ...style, borderCollapse: 'collapse', margin: '.25em auto .45em' }}>
            <tbody>{b.lignes.map((l, j) => (
              <tr key={j}>{l.map((c, k) => <td key={k} style={{ border: '1px solid #333', padding: '.05em .6em', textAlign: 'center', fontWeight: k === 0 ? 700 : 400 }}><Formule t={c} /></td>)}</tr>
            ))}</tbody>
          </table>
        );
      case 'figure':
        return (
          <div key={i} data-bloc={i} style={{ ...style, textAlign: 'center', margin: '.2em 0 .4em' }}>
            <img src={b.src} alt={b.alt || 'Figure du sujet'} style={{ height: `calc(${b.hauteur ?? 8}em * var(--figure, 1))`, maxWidth: '100%', objectFit: 'contain', display: 'inline-block' }} />
          </div>
        );
    }
  };

  return (
    <div ref={cadre} data-page-examen data-reproduit className="flex h-full w-full items-center justify-center" aria-label={e.source ? `Le sujet : ${e.source}` : 'Le sujet'}>
      {place.w > 0 && (
        <div data-feuille className="flex shrink-0 flex-col overflow-hidden"
          style={{ width: W, height: H, background: '#fbf8ef', color: '#111', borderRadius: 3, boxShadow: '0 10px 30px rgba(0,0,0,.45), 0 2px 6px rgba(0,0,0,.3)', fontFamily: POLICE }}>
          {r.entete ? (
            // l'en-tête du sujet, écrit en code : le cadre de la page et du code à gauche, les lignes au centre
            <div data-entete className="mx-[1.2%] mt-[.6%] flex shrink-0 items-stretch gap-[1%]" style={{ fontSize: Math.max(PLUS_PETIT, Math.round(mise.taille * 0.85)) }}>
              <div className="flex flex-col items-center justify-center rounded-[6px] border-2 border-[#222] px-2 leading-tight" style={{ fontWeight: 700 }}>
                {r.entete.page && <span dir="rtl">الصفحة <bdi dir="ltr">{r.entete.page}</bdi></span>}
                {r.entete.code && <span>{r.entete.code}</span>}
              </div>
              <div dir="auto" className="flex flex-1 flex-col items-center justify-center rounded-[10px] border-2 border-[#222] px-3 py-0.5 text-center leading-snug" style={{ fontWeight: 700 }}>
                {r.entete.lignes.map((l, i) => <span key={i} dir="auto">{l}</span>)}
              </div>
            </div>
          ) : bandeScan ? (
            <div className="relative mx-auto shrink-0 overflow-hidden" style={{ width: lBandeScan, height: hBandeScan }}>
              <img src={bandeScan.page} alt="" draggable={false} onLoad={ev => setDimEntete({ w: ev.currentTarget.naturalWidth, h: ev.currentTarget.naturalHeight })}
                style={{ position: 'absolute', left: 0, top: -bandeScan.haut * (dimEntete.h / dimEntete.w) * lBandeScan, width: lBandeScan, maxWidth: 'none' }} />
            </div>
          ) : null}
          <div ref={corps} data-corps className="min-h-0 flex-1 px-[3%] pb-[1%] pt-[.6%]"
            style={{ fontSize: mise.taille, columnCount: mise.colonnes, columnGap: '2.2em', columnRule: mise.colonnes > 1 ? '1px solid rgba(0,0,0,.15)' : undefined, lineHeight: 1.25,
              columnFill: 'auto', overflowY: mise.defile ? 'auto' : 'hidden', overflowX: 'hidden', '--figure': mise.figure } as CSSProperties}>
            {r.blocs.map(bloc)}
          </div>
        </div>
      )}
    </div>
  );
}
