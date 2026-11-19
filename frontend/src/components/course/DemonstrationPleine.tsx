import { useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react';
import type { Demonstration } from './types';
import { Formule, limAvecIndice } from './Formule';

/**
 * La démonstration au tableau. Avec une figure (18 novembre 2026, `figure`) : jouée SUR elle — ce tableau est une colonne
 * à côté de la figure, qui reste en grand ; les cartes déjà écrites sont effacées ; chaque ligne allume sa cible.
 * Sans figure, sur un tableau À PART (12 novembre 2026) : posé par-dessus le tableau de la question, en
 * plein cadre, même craie ; rien d'autre à voir que la démonstration (et le tuteur qui la dit, dans sa colonne). Les
 * lignes s'écrivent quand la voix atteint leur `mot` ; l'écriture est la plus grande qui tient, jamais de défilement.
 * L'élève le ferme à la main (« J'ai compris → » ou ×) ; sinon il se ferme seul après 5 min, jusqu'à 10 min pour une
 * démonstration longue. Le lecteur l'affiche partout où une démonstration s'écrit (diapositives, exercices de bloc) :
 * les cours n'ont rien à changer.
 */

/**
 * La démonstration jouée SUR la figure (18 novembre 2026, simulations-au-tableau règle 17) : donné par le lecteur quand la
 * diapositive a une simulation ou une image. La figure reste en grand ; ce tableau devient une colonne à côté d'elle
 * (`cote`), les cartes déjà écrites sur la scène sont effacées (`ouverte`), et chaque ligne qui a une cible (`allume`)
 * l'allume dans la simulation au moment où elle s'écrit.
 */
export type FigureDemo = {
  /** le tableau est une colonne à côté de la figure (sinon : par-dessus, comme sans figure) */
  cote: boolean;
  /** la démonstration s'ouvre (true : effacer la scène, éteindre la figure) ou se ferme (false) */
  ouverte: (oui: boolean) => void;
  /** la ligne `ligne` vient de s'écrire : allumer sa cible sur la figure */
  allumer: (cible: string | string[], ligne: number, texte: string) => void;
};

/** La lecture d'une démonstration : où en est la voix (en caractères de `parole`), sa fin, et l'arrêt. */
export type LectureDemo = { position: () => number; fin: Promise<void>; arreter: () => void };

/** Combien de temps le tableau reste ouvert sans geste de l'élève : 5 min, plus pour une démonstration longue, 10 min au plus. */
export function dureeOuverteMs(d: Demonstration, dureePisteS = 0): number {
  const lecture = Math.max(dureePisteS, d.parole.length / 14);       // ≈ 14 caractères dits par seconde
  return Math.round(Math.min(10 * 60, Math.max(5 * 60, 4 * 60 + d.lignes.length * 20 + lecture * 2)) * 1000);
}

const CRAIE = "'Patrick Hand', 'Caveat', cursive";

export default function DemonstrationPleine({ d, lecture, complet = false, enonce = '', onFermer, figure }: {
  d: Demonstration;
  /** la voix en cours ; null : le professeur prend la craie (voix pas encore prête) */
  lecture: LectureDemo | null;
  /** déjà dite : toutes les lignes sont là d'emblée (« Revoir la démonstration ») */
  complet?: boolean;
  /** l'énoncé de la question (l'indice de « lim » quand la ligne ne le porte pas) */
  enonce?: string;
  /** fermé : `main` = l'élève (bouton, ×, Échap), sinon le délai */
  onFermer: (main: boolean) => void;
  /** la diapositive a une figure : la démonstration se joue dessus (colonne à côté, allumages) */
  figure?: FigureDemo | null;
}) {
  const cote = !!figure?.cote;
  const positions = useMemo(() => {
    const n = Math.max(1, d.parole.length);
    return d.lignes.map((l, i) => {
      const k = l.mot ? d.parole.indexOf(l.mot) : -1;
      return k >= 0 ? k : (i / Math.max(1, d.lignes.length)) * n;   // un mot introuvable : lignes réparties sur la voix
    });
  }, [d]);
  const lignes = useMemo(() => d.lignes.map(l => limAvecIndice(l.texte, enonce)), [d, enonce]);
  const [vuesLues, setVues] = useState(0);
  const [dite, setDite] = useState(complet);
  const vues = complet || dite ? d.lignes.length : lecture ? vuesLues : 0;
  useEffect(() => {
    if (complet || !lecture) return;
    let frame = 0, vivant = true;
    const suivre = () => {
      setVues(positions.filter(x => lecture.position() >= x - 2).length);
      frame = requestAnimationFrame(suivre);
    };
    frame = requestAnimationFrame(suivre);
    void lecture.fin.then(() => { if (vivant) setDite(true); });
    return () => { vivant = false; cancelAnimationFrame(frame); };
  }, [lecture, positions, complet]);

  // Sur la figure : la scène est effacée à l'ouverture (rendue à la fermeture), et chaque ligne écrite allume sa cible.
  const fig = useRef(figure);
  useEffect(() => { fig.current = figure; }, [figure]);
  const avecFigure = !!figure;
  useEffect(() => {
    if (!avecFigure) return;
    fig.current?.ouverte(true);
    return () => fig.current?.ouverte(false);
  }, [avecFigure]);
  const allumees = useRef(0);
  useEffect(() => {
    if (!avecFigure) return;
    for (let i = allumees.current; i < vues; i++) {
      const l = d.lignes[i];
      if (l?.allume && (typeof l.allume === 'string' || l.allume.length)) fig.current?.allumer(l.allume, i, l.texte);
    }
    allumees.current = Math.max(allumees.current, vues);
  }, [vues, d, avecFigure]);

  // Fermeture seule, sans geste de l'élève : 5 à 10 min selon la longueur.
  const fermer = useRef(onFermer); fermer.current = onFermer;
  useEffect(() => {
    const id = window.setTimeout(() => fermer.current(false), dureeOuverteMs(d));
    const echap = (e: KeyboardEvent) => { if (e.key === 'Escape') fermer.current(true); };
    window.addEventListener('keydown', echap);
    return () => { window.clearTimeout(id); window.removeEventListener('keydown', echap); };
  }, [d]);

  // La plus grande écriture qui tient dans le tableau, sans défiler (calculée sur TOUTES les lignes : rien ne saute
  // quand la suivante arrive).
  const zone = useRef<HTMLDivElement>(null);
  const mesure = useRef<HTMLDivElement>(null);
  const [taille, setTaille] = useState(34);
  /** même à 16 px, tout ne tient pas (colonne étroite, téléphone) : les premières lignes montent hors du tableau */
  const [deborde, setDeborde] = useState(false);
  useLayoutEffect(() => {
    const z = zone.current, m = mesure.current;
    if (!z || !m) return;
    const ajuster = () => {
      let t = cote ? 30 : 46;                                    // à côté de la figure : l'écrit ne la dépasse pas
      const px = cote ? 24 : 48, py = cote ? 16 : 32;
      const w = z.clientWidth - px, h = z.clientHeight - py;     // sans le padding du tableau
      m.style.width = `${w}px`;
      // le plus petit : 16 px ; 18 dans la colonne (une fraction s'écrit à 87 % : jamais sous 15 px)
      const min = cote ? 18 : 16;
      let tient = false;
      while (t >= min) {
        m.style.fontSize = `${t}px`;
        if (m.scrollHeight <= h && m.scrollWidth <= w + 1) { tient = true; break; }
        if (t === min) break;
        t = Math.max(min, t - 2);
      }
      setTaille(t); setDeborde(!tient);
    };
    ajuster();
    const ro = new ResizeObserver(ajuster);
    ro.observe(z);
    return () => ro.disconnect();
  }, [lignes, cote]);

  // les lignes écrites ne tiennent plus (même à 16 px) : on garde la dernière en bas, les premières montent
  const liste = useRef<HTMLDivElement>(null);
  const [enBas, setEnBas] = useState(false);
  useLayoutEffect(() => {
    const z = zone.current, l = liste.current;
    if (!deborde || !z || !l) { setEnBas(false); return; }
    setEnBas(l.scrollHeight > z.clientHeight - (cote ? 16 : 32));
  }, [vues, taille, deborde, cote]);

  // posé en haut du tableau qui le porte : si ce tableau avait défilé, on le ramène en haut (rien de caché)
  const cadre = useRef<HTMLDivElement>(null);
  useEffect(() => { (cadre.current?.offsetParent as HTMLElement | null)?.scrollTo?.({ top: 0 }); }, []);
  const ligne = (texte: string, i: number, anime: boolean) => (
    <p key={i} className={anime ? 'craie-ecrit' : ''} dir="auto" style={{ lineHeight: 1.4, color: /[=→⇒]/.test(texte) ? '#fef9c3' : '#f1f5e9' }}>
      <Formule t={texte} />
    </p>
  );

  return (
    <div ref={cadre} data-demonstration={cote ? 'cote' : 'pleine'} className="question-apparait absolute inset-0 z-40 flex flex-col overflow-hidden rounded-2xl border-2 border-amber-200/40 bg-[#0f2219] shadow-2xl"
      role="dialog" aria-label="La démonstration" style={{ fontFamily: CRAIE }}>
      <div className={`flex shrink-0 items-center justify-between border-b border-amber-200/20 ${cote ? 'px-3 py-1' : 'px-4 py-2'}`}>
        <div className="text-base font-semibold text-emerald-200" style={cote ? { fontSize: 15 } : undefined}>✍️ La démonstration</div>
        <button onClick={() => onFermer(true)} className="text-xl text-white/50 hover:text-white" aria-label="Fermer la démonstration">×</button>
      </div>
      <div ref={zone} className={`relative min-h-0 flex-1 overflow-hidden ${cote ? 'px-3 py-2' : 'px-6 py-4'}`}>
        {/* le gabarit invisible qui mesure la taille d'écriture (toutes les lignes) */}
        <div ref={mesure} aria-hidden className={`pointer-events-none invisible absolute flex flex-col gap-1 ${cote ? 'left-3 top-2' : 'left-6 top-4'}`}>
          {lignes.map((t, i) => ligne(t, i, false))}
        </div>
        {!complet && !lecture && <p className="text-lg text-white/45 animate-pulse">Le professeur prend la craie…</p>}
        {/* trop long même à 16 px : la dernière ligne écrite reste en bas, les premières montent hors du tableau */}
        <div ref={liste} className={`flex flex-col gap-1 ${enBas ? `absolute inset-x-0 bottom-2 ${cote ? 'px-3' : 'px-6'}` : ''}`} style={{ fontSize: taille }}>
          {lignes.slice(0, vues).map((t, i) => ligne(t, i, !complet))}
        </div>
      </div>
      <div className={`flex shrink-0 justify-end ${cote ? 'px-3 pb-2' : 'px-4 pb-3'}`}>
        <button onClick={() => onFermer(true)} style={{ fontFamily: 'system-ui, sans-serif' }}
          className={`rounded-full font-semibold transition-colors ${cote ? 'px-4 py-1.5 text-[15px]' : 'px-6 py-2.5 text-base'} ${dite || complet ? 'bg-emerald-500 text-white hover:bg-emerald-400' : 'bg-white/10 text-white/75 hover:bg-white/20'}`}>
          J’ai compris →
        </button>
      </div>
    </div>
  );
}
