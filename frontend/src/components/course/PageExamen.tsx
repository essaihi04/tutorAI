import { useLayoutEffect, useMemo, useRef, useState } from 'react';
import type { PageExamen } from './types';
import { Formule } from './Formule';
import ExamenReproduit from './ExamenReproduit';

/**
 * La page d'un sujet du national, telle qu'à l'examen (18 novembre 2026, professeur règles 44-46) : le scan
 * (`/static/exams/<matière>/<année>-<session>/pages/sujet_pN.jpg`) posé sur le tableau comme une feuille (papier, ombre),
 * recadré sur l'exercice (`recadrage`, puis sa `suite` sur les pages suivantes), la bande d'en-tête officielle gardée
 * au-dessus. TOUT l'exercice est visible, sans défiler (demande de l'utilisateur, 19 novembre 2026 : « il doit mettre
 * tout l'exercice ») : la feuille prend la plus grande taille qui le fait tenir, en une colonne, ou en deux feuilles côte
 * à côte quand l'écran est large (l'exercice continue sur la seconde, comme une page qu'on tourne). Le tuteur la lit : la
 * phrase dite se surligne au feutre (sa `zone`) ; sans `zone`, elle s'écrit sous la feuille.
 */

/** Une page A4 scannée (les sujets sont en 1654 × 2339) : la taille avant que l'image soit chargée. */
const A4 = { w: 1654, h: 2339 };
const LARGEUR_MAX = 1040;
const ECART = 14;                                                     // entre deux feuilles côte à côte
const ENTETE_DEFAUT = { haut: 0, bas: 0.115 };

type Morceau = { page: string; haut: number; bas: number };

type Props = {
  e: PageExamen;
  /** le temps de la voix (s) */
  temps: number;
  /** l'instant (s) d'un mot du texte parlé */
  instant: (mot: string) => number;
  /** la voix est en cours : hors lecture, rien n'est surligné */
  lecture: boolean;
};

/** L'exercice reproduit en code s'il est fourni (`reproduction`), sinon les morceaux du scan. */
export default function PageExamenVue(p: Props) {
  return p.e.reproduction?.blocs?.length ? <Reproduit {...p} /> : <PageScan {...p} />;
}

function Reproduit({ e, temps, instant, lecture }: Props) {
  return <ExamenReproduit e={e} actif={useBlocLu(e, temps, instant, lecture)} />;
}

function PageScan({ e, temps, instant, lecture }: {
  e: PageExamen;
  /** le temps de la voix (s) */
  temps: number;
  /** l'instant (s) d'un mot du texte parlé */
  instant: (mot: string) => number;
  /** la voix est en cours : hors lecture, rien n'est surligné */
  lecture: boolean;
}) {
  const cadre = useRef<HTMLDivElement>(null);
  const [place, setPlace] = useState({ w: 0, h: 0 });
  const [dims, setDims] = useState<Record<string, { w: number; h: number }>>({});
  useLayoutEffect(() => {
    const el = cadre.current;
    if (!el) return;
    const lire = () => setPlace({ w: el.clientWidth, h: el.clientHeight });
    lire();
    const ro = new ResizeObserver(lire);
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  const entete = e.entete === false ? null : { page: e.entete?.page || e.page, haut: e.entete?.haut ?? ENTETE_DEFAUT.haut, bas: e.entete?.bas ?? ENTETE_DEFAUT.bas };
  const marge = Math.min(0.2, Math.max(0, e.marge ?? 0.04));
  const morceaux: Morceau[] = useMemo(() => [
    { page: e.page, haut: e.recadrage?.haut ?? 0, bas: e.recadrage?.bas ?? 1 },
    ...(e.suite || []).map(s => ({ page: s.page, haut: s.haut, bas: s.bas })),
  ], [e]);
  const phrases = useMemo(() => e.phrases || [], [e]);
  const sansZone = phrases.some(p => !p.zone);
  const instants = useMemo(() => phrases.map(p => instant(p.mot)), [phrases, instant]);
  const active = lecture ? instants.reduce((k, t, i) => (temps >= t && t > 0 ? i : k), -1) : -1;
  const phrase = active >= 0 ? phrases[active] : null;

  // Hauteurs en « hauteur de feuille par px de largeur montrée » : h(px) = fraction × parLargeur × W.
  const dim = (url: string) => dims[url] || A4;
  const parLargeur = (url: string) => { const p = dim(url); return p.h / (p.w * (1 - 2 * marge)); };
  const hEntete = entete ? (entete.bas - entete.haut) * parLargeur(entete.page) : 0;
  const hMorceaux = morceaux.map(m => (m.bas - m.haut) * parLargeur(m.page));
  const total = hEntete + hMorceaux.reduce((a, b) => a + b, 0);
  const bande = sansZone ? 52 : 0;                                    // la phrase écrite sous la feuille
  const dispoH = Math.max(80, place.h - 8 - bande), dispoW = Math.max(120, place.w - 8);

  // Une feuille, ou deux côte à côte : la disposition qui donne la plus grande largeur (donc le texte le plus grand).
  const plan = useMemo(() => {
    const une = Math.min(dispoW, LARGEUR_MAX, dispoH / Math.max(0.01, total));
    // deux feuilles : la première porte l'en-tête et la moitié de l'exercice, la seconde la suite
    const moitie = total / 2;
    const deux = Math.min((dispoW - ECART) / 2, LARGEUR_MAX, dispoH / Math.max(0.01, Math.max(moitie, hEntete + 0.001)));
    const colonnes: Morceau[][] = [[]];
    if (deux > une * 1.08 && morceaux.length) {
      let reste = moitie - hEntete;
      morceaux.forEach((m, i) => {
        const h = hMorceaux[i];
        if (colonnes.length === 1 && h > reste) {
          // la coupe, au plus près d'une limite de phrase connue (on ne coupe pas une ligne en deux)
          let coupe = m.haut + (reste / h) * (m.bas - m.haut);
          const limites = phrases.flatMap(p => (p.zone && (p.zone.page || e.page) === m.page ? [p.zone.haut, p.zone.bas] : []))
            .filter(y => y > m.haut + 0.01 && y < m.bas - 0.01);
          if (limites.length) coupe = limites.reduce((a, y) => (Math.abs(y - coupe) < Math.abs(a - coupe) ? y : a), limites[0]);
          if (coupe > m.haut + 0.005) colonnes[0].push({ ...m, bas: coupe });
          colonnes.push([{ ...m, haut: coupe }]);
        } else {
          colonnes[colonnes.length - 1].push(m);
          reste -= h;
        }
      });
      const hauteur = (c: Morceau[], avecEntete: boolean) => (avecEntete ? hEntete : 0) + c.reduce((a, m) => a + (m.bas - m.haut) * parLargeur(m.page), 0);
      const W = Math.min((dispoW - ECART) / 2, LARGEUR_MAX, dispoH / Math.max(0.01, hauteur(colonnes[0], true), colonnes[1] ? hauteur(colonnes[1], false) : 0));
      return { W: Math.floor(W), colonnes };
    }
    return { W: Math.floor(une), colonnes: [morceaux] };
  // eslint-disable-next-line react-hooks/exhaustive-deps -- recalculé quand la place, la page ou les tailles changent
  }, [dispoW, dispoH, total, hEntete, morceaux, phrases, dims, marge]);
  const W = plan.W;

  const image = (url: string, haut: number) => {
    const p = dim(url), largeur = W / (1 - 2 * marge);
    return (
      <img src={url} alt="" draggable={false}
        onLoad={ev => { const i = ev.currentTarget; if (!dims[url]) setDims(d => ({ ...d, [url]: { w: i.naturalWidth, h: i.naturalHeight } })); }}
        style={{ position: 'absolute', left: -marge * largeur, top: -haut * (p.h / p.w) * largeur, width: largeur, maxWidth: 'none' }} />
    );
  };
  const feuille = { width: W, background: '#fbf8ef', borderRadius: 3, boxShadow: '0 10px 30px rgba(0,0,0,.45), 0 2px 6px rgba(0,0,0,.3)' } as const;
  const coupe = <div aria-hidden style={{ height: 0, borderTop: '1px dashed rgba(60,60,60,.35)' }} />;

  return (
    <div ref={cadre} data-page-examen className="flex h-full w-full flex-col items-center justify-center" aria-label={e.source ? `Le sujet : ${e.source}` : 'La page du sujet'}>
      {place.w > 0 && (
        <div className="flex items-start justify-center" style={{ gap: ECART }} role="img" aria-label={phrases.map(p => p.texte).join(' ') || e.source || 'La page du sujet'}>
          {plan.colonnes.map((colonne, c) => (
            <div key={c} data-feuille className="relative shrink-0 overflow-hidden" style={feuille}>
              {c === 0 && entete && <div className="relative overflow-hidden" style={{ height: (entete.bas - entete.haut) * parLargeur(entete.page) * W }}>{image(entete.page, entete.haut)}</div>}
              {colonne.map((m, i) => {
                const k = parLargeur(m.page) * W;                       // px par unité de hauteur de page
                const z = phrase?.zone && (phrase.zone.page || e.page) === m.page && phrase.zone.bas > m.haut && phrase.zone.haut < m.bas ? phrase.zone : null;
                return (
                  <div key={i}>
                    {/* une coupe : entre l'en-tête et l'exercice, ou d'une page à la suivante */}
                    {(i > 0 || (c === 0 && entete && (entete.page !== m.page || Math.abs(entete.bas - m.haut) > 0.01))) && coupe}
                    <div className="relative overflow-hidden" style={{ height: (m.bas - m.haut) * k }}>
                      {image(m.page, m.haut)}
                      {z && (
                        <div aria-hidden className="pointer-events-none absolute inset-x-0"
                          style={{ top: (Math.max(z.haut, m.haut) - m.haut) * k, height: (Math.min(z.bas, m.bas) - Math.max(z.haut, m.haut)) * k,
                            background: 'rgba(253,224,71,.38)', mixBlendMode: 'multiply', borderRadius: 4, transition: 'top .5s ease, height .4s ease' }} />
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          ))}
        </div>
      )}
      {sansZone && (
        <p className="mt-2 flex min-h-[44px] max-w-[min(100%,1040px)] items-center px-3 text-center text-[16px] leading-snug md:text-[18px]"
          style={{ fontFamily: "'Patrick Hand', 'Caveat', cursive", color: '#fef3c7' }}>
          {phrase && !phrase.zone ? <span key={active} className="craie-ecrit rounded-md bg-amber-200/15 px-2"><Formule t={phrase.texte} /></span> : null}
        </p>
      )}
    </div>
  );
}

/** Les instants des blocs : le bloc lu est le dernier dont le `mot` est atteint. */
function useBlocLu(e: PageExamen, temps: number, instant: (mot: string) => number, lecture: boolean) {
  const instants = useMemo(() => (e.reproduction?.blocs || []).map(b => (b.mot ? instant(b.mot) : -1)), [e, instant]);
  return lecture ? instants.reduce((k, t, i) => (t > 0 && temps >= t ? i : k), -1) : -1;
}
