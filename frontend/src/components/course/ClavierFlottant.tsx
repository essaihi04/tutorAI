import { useCallback, useEffect, useMemo, useRef, useState, useSyncExternalStore, type RefObject } from 'react';
import { insererAuCurseur, Touches, type MatiereClavier } from './ClavierScientifique';

/**
 * Le clavier scientifique flottant du lecteur de cours (12 novembre 2026).
 *  - Il s'ouvre SEUL quand une question à réponse libre (ou le « retrouver » d'un bloc) s'ouvre, avec les touches de la
 *    MATIÈRE du cours (physique-chimie, SVT ou maths) ; le bouton « ⌨ Clavier » de la barre du bas l'ouvre et le ferme.
 *  - Il flotte à DROITE de l'écran, à gauche de la colonne du tuteur 3D, sans couvrir le champ de réponse (le tableau des
 *    questions lui laisse sa place) ; il écrit dans le dernier champ touché ; × , Échap ou un glissé vers la droite le ferme.
 *  - En haut, des suggestions propres à CET exercice : symboles, grandeurs, morceaux de relation, unités — des justes et
 *    des pièges plausibles mêlés, jamais la formule complète ni la réponse. Préparées dans le cours (`question.clavier`),
 *    sinon demandées au serveur (`/course-player/clavier-suggestions`, Claude Haiku, filtrées), gardées dans le navigateur.
 *
 * Un seul état pour tout le lecteur (diapositives, blocs, rappels) : un petit magasin, lu avec `useSyncExternalStore`.
 */

type Champ = HTMLInputElement | HTMLTextAreaElement;

/** Où sont les suggestions de cette question (`slide_id` : la diapositive, le bloc ou la compétence). */
export interface CleSuggestions {
  deck_id?: string; slide_id?: string; cle?: string; enonce?: string;
  /** les suggestions préparées dans le cours, si elle en a */
  clavier?: { aides?: string[]; pieges?: string[] };
}

interface ChampActif {
  id: number;
  ref: RefObject<Champ | null>;
  lire: () => string;
  poser: (v: string) => void;
  suggestions?: CleSuggestions;
}

interface Etat { ouvert: boolean; champ: ChampActif | null; matiere: MatiereClavier; hotes: number }

let etat: Etat = { ouvert: false, champ: null, matiere: '', hotes: 0 };
const abonnes = new Set<() => void>();
const changer = (e: Partial<Etat>) => { etat = { ...etat, ...e }; abonnes.forEach(f => f()); };
const champs = new Map<number, ChampActif>();
let compteur = 0;

export const clavier = {
  ouvrir: () => changer({ ouvert: true }),
  fermer: () => changer({ ouvert: false }),
  basculer: () => changer({ ouvert: !etat.ouvert }),
  matiere: (m: MatiereClavier) => { if (m !== etat.matiere) changer({ matiere: m }); },
  /** Un clavier flottant est-il monté (le lecteur de cours) ? Sinon les champs gardent leur clavier en dessous. */
  present: () => etat.hotes > 0,
};

export function useClavier(): Etat {
  return useSyncExternalStore(cb => { abonnes.add(cb); return () => { abonnes.delete(cb); }; }, () => etat, () => etat);
}

/**
 * Un champ où l'élève écrit se déclare au clavier : il devient le champ actif à son ouverture (et à chaque fois qu'il
 * est touché) ; `auto` : le clavier s'ouvre seul (question à réponse libre, « retrouver »). Rend `toucher`, à poser sur
 * `onFocus`.
 */
export function useChampClavier(ref: RefObject<Champ | null>, valeur: string, poser: (v: string) => void,
  { auto = false, actif = true, suggestions }: { auto?: boolean; actif?: boolean; suggestions?: CleSuggestions } = {}) {
  const id = useRef(0);
  if (!id.current) id.current = ++compteur;
  const v = useRef(valeur); v.current = valeur;
  const p = useRef(poser); p.current = poser;
  const cleSugg = suggestions ? `${suggestions.deck_id}|${suggestions.slide_id}|${suggestions.cle}|${suggestions.enonce}` : '';
  const sugg = useRef(suggestions); sugg.current = suggestions;
  const declarer = useCallback(() => {
    const c: ChampActif = { id: id.current, ref, lire: () => v.current, poser: x => p.current(x), suggestions: sugg.current };
    champs.set(c.id, c);
    if (etat.champ?.id !== c.id || etat.champ.suggestions !== c.suggestions) changer({ champ: c });
  }, [ref]);
  useEffect(() => {
    if (!actif) return;
    declarer();
    if (auto) clavier.ouvrir();
    const moi = id.current;
    return () => {
      champs.delete(moi);
      if (etat.champ?.id === moi) {
        // le champ précédent encore à l'écran redevient actif ; plus aucun : le clavier se ferme
        const reste = [...champs.values()].pop() || null;
        changer({ champ: reste, ouvert: reste ? etat.ouvert : false });
      }
    };
  }, [actif, auto, declarer, cleSugg]);
  return declarer;
}

// ── Suggestions : préparées dans le cours, sinon le serveur ; gardées dans le navigateur ──
const jeton = () => { try { return localStorage.getItem('token') || ''; } catch { return ''; } };
type Sugg = { aides: string[]; pieges: string[] };
const enCours = new Map<string, Promise<Sugg>>();

function cleLocale(s: CleSuggestions) {
  return `clavier-sugg:v1:${s.deck_id || ''}:${s.slide_id || ''}:${s.cle || ''}:${s.slide_id && s.cle ? '' : (s.enonce || '').slice(0, 80)}`;
}

async function chercherSuggestions(s: CleSuggestions, matiere: MatiereClavier): Promise<Sugg> {
  if (s.clavier && ((s.clavier.aides?.length ?? 0) + (s.clavier.pieges?.length ?? 0)) > 0) return { aides: s.clavier.aides || [], pieges: s.clavier.pieges || [] };
  const cle = cleLocale(s);
  try { const x = localStorage.getItem(cle); if (x) return JSON.parse(x) as Sugg; } catch { /* sans mémoire locale */ }
  if (!enCours.has(cle)) {
    enCours.set(cle, (async () => {
      const r = await fetch('/api/v1/course-player/clavier-suggestions', {
        method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${jeton()}` },
        body: JSON.stringify({ deck_id: s.deck_id, slide_id: s.slide_id, cle: s.cle, enonce: (s.enonce || '').slice(0, 800), matiere }),
      });
      if (!r.ok) throw new Error(String(r.status));
      const d = await r.json() as Partial<Sugg> & { source?: string };
      const out = { aides: d.aides || [], pieges: d.pieges || [] };
      if (out.aides.length + out.pieges.length > 0) { try { localStorage.setItem(cle, JSON.stringify(out)); } catch { /* sans mémoire locale */ } }
      return out;
    })().finally(() => window.setTimeout(() => enCours.delete(cle), 1000)));
  }
  return enCours.get(cle)!;
}

/** Aides et pièges mêlés, toujours dans le même ordre pour une question (rien ne bouge d'une ouverture à l'autre). */
function meler(s: Sugg, graine: string): string[] {
  let h = 2166136261;
  for (const ch of graine) h = Math.imul(h ^ ch.charCodeAt(0), 16777619) >>> 0;
  const tous = [...new Set([...s.aides, ...s.pieges].map(x => String(x).trim()).filter(Boolean))].slice(0, 10);
  return tous.map((x, i) => ({ x, k: (Math.imul(h + i * 2654435761, 2246822519) >>> 0) })).sort((a, b) => a.k - b.k).map(o => o.x);
}

function Suggestions({ s, matiere, onTaper }: { s: CleSuggestions; matiere: MatiereClavier; onTaper: (t: string) => void }) {
  const [liste, setListe] = useState<string[] | null>(null);
  const cle = cleLocale(s);
  useEffect(() => {
    let vivant = true;
    setListe(null);
    chercherSuggestions(s, matiere).then(x => { if (vivant) setListe(meler(x, cle)); }).catch(() => { if (vivant) setListe([]); });
    return () => { vivant = false; };
    // eslint-disable-next-line react-hooks/exhaustive-deps -- une demande par question
  }, [cle, matiere]);
  if (liste && !liste.length) return null;
  return (
    <div className="mb-2 rounded-lg border border-amber-200/20 bg-amber-200/[0.04] p-2">
      <div className="mb-1 text-[11px] text-amber-100/70">💡 Pour cet exercice — certaines pistes sont des pièges, choisis bien</div>
      <div className="flex min-h-[40px] flex-wrap gap-1">
        {liste === null
          ? [0, 1, 2, 3].map(i => <span key={i} className="h-9 w-14 animate-pulse rounded-lg bg-white/[0.06]" />)
          : liste.map(t => (
            <button key={t} type="button" onClick={() => onTaper(t)}
              className="min-h-[38px] rounded-lg border border-amber-200/25 bg-white/[0.05] px-2.5 text-[16px] text-amber-50 hover:bg-amber-200/15 active:bg-amber-200/30"
              style={{ touchAction: 'manipulation' }}>{t}</button>
          ))}
      </div>
    </div>
  );
}

/**
 * Le panneau du clavier, à droite. `droite` : la place laissée à la colonne du tuteur 3D (px) ; sur téléphone il se pose
 * en bas, sur toute la largeur. Monté une fois par le lecteur de cours.
 */
export default function ClavierFlottant({ droite = 0, bas = 76 }: { droite?: number; bas?: number }) {
  const e = useClavier();
  useEffect(() => { changer({ hotes: etat.hotes + 1 }); return () => changer({ hotes: Math.max(0, etat.hotes - 1), ouvert: false }); }, []);
  useEffect(() => {
    if (!e.ouvert) return;
    const echap = (ev: KeyboardEvent) => { if (ev.key === 'Escape') clavier.fermer(); };
    window.addEventListener('keydown', echap);
    return () => window.removeEventListener('keydown', echap);
  }, [e.ouvert]);
  const glisse = useRef<{ x: number; y: number } | null>(null);
  const [decale, setDecale] = useState(0);
  const taper = useCallback((t: string) => {
    const c = etat.champ;
    if (!c) return;
    insererAuCurseur(c.ref.current, c.lire(), t, c.poser);
  }, []);
  const etroit = typeof window !== 'undefined' && window.innerWidth < 640;
  // juste au-dessus de la barre du bas du lecteur (elle tient sur une ou deux lignes) : jamais sur ses boutons
  const [basBarre, setBasBarre] = useState(bas);
  useEffect(() => {
    if (!e.ouvert) return;
    const pied = document.querySelector<HTMLElement>('[data-pied-cours]');
    if (!pied || bas < 40) { setBasBarre(bas); return; }
    const mesurer = () => setBasBarre(Math.max(bas, Math.round(window.innerHeight - pied.getBoundingClientRect().top + 8)));
    mesurer();
    const ro = new ResizeObserver(mesurer); ro.observe(pied);
    window.addEventListener('resize', mesurer);
    return () => { ro.disconnect(); window.removeEventListener('resize', mesurer); };
  }, [e.ouvert, bas]);
  const style = useMemo(() => (etroit
    ? { left: 0, right: 0, bottom: 0, height: `${HAUTEUR_TELEPHONE_VH}vh` }
    : { right: droite + 12, bottom: basBarre, width: 'min(340px, 34vw)', maxHeight: `calc(100% - ${basBarre + 64}px)` }), [etroit, droite, basBarre]);
  if (!e.ouvert) return null;
  return (
    <aside role="dialog" aria-label="Clavier scientifique"
      className="question-apparait fixed z-[130] flex flex-col overflow-hidden rounded-2xl border border-amber-200/30 bg-[#0b1912]/97 text-white shadow-2xl backdrop-blur"
      style={{ ...style, transform: decale ? `translateX(${decale}px)` : undefined, opacity: decale ? Math.max(0.3, 1 - decale / 200) : 1,
        fontFamily: 'system-ui, "Segoe UI Symbol", "Cambria Math", sans-serif' }}
      // un appui sur le clavier ne fait jamais perdre le curseur du champ
      onMouseDown={ev => ev.preventDefault()}>
      <div className="flex shrink-0 cursor-grab items-center gap-2 border-b border-white/10 px-3 py-1.5 select-none"
        style={{ touchAction: 'pan-y' }}
        // un glissé vers la droite le range
        onPointerDown={ev => { glisse.current = { x: ev.clientX, y: ev.clientY }; ev.currentTarget.setPointerCapture?.(ev.pointerId); }}
        onPointerMove={ev => { const g = glisse.current; if (g) setDecale(Math.max(0, ev.clientX - g.x)); }}
        onPointerUp={ev => { const g = glisse.current; glisse.current = null; setDecale(0); if (g && ev.clientX - g.x > 70) clavier.fermer(); }}
        onPointerCancel={() => { glisse.current = null; setDecale(0); }}>
        <span className="text-sm text-amber-100">⌨ Clavier</span>
        <span className="text-[11px] text-white/35">glisse → pour ranger</span>
        <button type="button" onClick={clavier.fermer} onPointerDown={ev => ev.stopPropagation()} aria-label="Fermer le clavier"
          className="ml-auto min-h-[36px] min-w-[36px] rounded-lg text-xl text-white/60 hover:bg-white/10">×</button>
      </div>
      <div className="min-h-0 flex-1 overflow-y-auto p-2">
        {e.champ?.suggestions && <Suggestions s={e.champ.suggestions} matiere={e.matiere} onTaper={taper} />}
        {!e.champ && <p className="mb-2 text-xs text-white/55">Touche un champ de réponse : le clavier y écrira.</p>}
        <Touches matiere={e.matiere} onTaper={taper} desactive={!e.champ} />
      </div>
    </aside>
  );
}

/** Sur téléphone, le clavier se pose en bas, sur toute la largeur, sur cette hauteur (vh) : le tableau remonte d'autant. */
export const HAUTEUR_TELEPHONE_VH = 40;
/** La hauteur que le clavier ouvert prend en bas sur téléphone (px), 0 ailleurs. */
export function hauteurClavierTelephone(ouvert: boolean): number {
  if (!ouvert || typeof window === 'undefined' || window.innerWidth >= 640) return 0;
  return Math.round(window.innerHeight * HAUTEUR_TELEPHONE_VH / 100);
}

/** La place que le clavier ouvert prend à droite (px) : le tableau des questions se resserre d'autant. */
export function largeurClavier(ouvert: boolean): number {
  if (!ouvert || typeof window === 'undefined' || window.innerWidth < 640) return 0;
  return Math.min(340, window.innerWidth * 0.34) + 16;
}
