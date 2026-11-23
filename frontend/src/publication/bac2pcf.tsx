/**
 * Le lien libre des révisions de 2ᵉ Bac PC BIOF (23 novembre 2026) : https://moalim.online/2bacpcf/
 *
 * Deux séances de révision assemblées à partir des cours existants (diapositives et voix déjà enregistrées, aucune voix
 * nouvelle), chacune avec les sujets du national et leur solution jouée pas à pas, puis un examen de 30 minutes corrigé :
 *   - `?cours=rev_phys_ondes_radioactivite`   physique : ondes lumineuses + décroissance radioactive ;
 *   - `?cours=rev_chim_deux_sens_equilibre`   chimie : transformations dans les deux sens + état d'équilibre ;
 *   - `?examen=physique` / `?examen=chimie`   deux exercices existants de 15 min, correction et voix comprises.
 * Lien simple : ni fiche ni suivi ; rien n'est gardé d'une visite à l'autre. Le tuteur répond par les routes publiques
 * du cours des ondes ; ces cours ne sont pas sur le serveur, l'identifiant du cours est retiré des demandes.
 */
import { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import '../index.css';
import '../services/audioUnlock';
import CoursePlayer from '../components/course/CoursePlayer';
import type { CourseDeck } from '../components/course/types';
import Examen, { utiliserSujet } from './tronc-commun/Examen';
import { SUJET_CHIMIE, SUJET_PHYSIQUE, VOIX_CHIMIE, VOIX_PHYSIQUE } from './bac2pcf/sujets';

const SOURCES = import.meta.glob('./bac2pcf/cours/rev_*.json', { import: 'default' }) as Record<string, () => Promise<CourseDeck>>;
const source = (id: string) => SOURCES[Object.keys(SOURCES).find(f => f.endsWith(`/${id}.json`)) || ''];
const MATIERES = [
  { cle: 'physique', nom: 'Physique', cours: 'rev_phys_ondes_radioactivite', titre: 'Ondes lumineuses et décroissance radioactive',
    sous: 'Diffraction, θ et L, fréquence et indice, dispersion ; noyau, désintégrations, loi de décroissance, activité et datation', couleur: '#2a78d6',
    sujet: SUJET_PHYSIQUE, voix: VOIX_PHYSIQUE },
  { cle: 'chimie', nom: 'Chimie', cours: 'rev_chim_deux_sens_equilibre', titre: 'Transformations dans les deux sens et état d’équilibre',
    sous: 'pH, taux d’avancement final, équilibre, conductimétrie ; quotient de réaction Qr, constante K, ce dont dépend τ', couleur: '#eb6834',
    sujet: SUJET_CHIMIE, voix: VOIX_CHIMIE },
];

// ── Lien libre : rien n'est gardé d'une visite à l'autre.
const PASSAGERES = ['reponse:', 'course-player:'];
const memoireDeVisite = new Map<string, string>();
try {
  const proto = Storage.prototype, lireS = proto.getItem, ecrireS = proto.setItem, oterS = proto.removeItem;
  const passagere = (k: string) => PASSAGERES.some(p => String(k).startsWith(p));
  proto.getItem = function (this: Storage, k: string) { return passagere(k) ? (memoireDeVisite.get(k) ?? null) : lireS.call(this, k); };
  proto.setItem = function (this: Storage, k: string, v: string) { if (passagere(k)) memoireDeVisite.set(k, String(v)); else ecrireS.call(this, k, v); };
  proto.removeItem = function (this: Storage, k: string) { if (passagere(k)) memoireDeVisite.delete(k); else oterS.call(this, k); };
} catch { /* navigation privée */ }

const VISITEUR = crypto.randomUUID?.() || `v-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 12)}`;
const PUBLIC = '/api/v1/public/cours-ondes';
const ROUTES = ['question-eleve', 'transcrire', 'ocr-reponse', 'reexplication', 'answer-reaction', 'sim-reaction', 'clavier-suggestions'];
const VIDE = () => Promise.resolve(new Response('{}', { status: 200, headers: { 'Content-Type': 'application/json' } }));
const fetchOriginal = window.fetch.bind(window);
window.fetch = (entree: RequestInfo | URL, init?: RequestInit) => {
  const url = typeof entree === 'string' ? entree : entree instanceof URL ? entree.href : entree.url;
  const chemin = url.replace(location.origin, '');
  // les pistes sont enregistrées ; pas de voix en direct
  if (chemin.startsWith('/api/v1/tts/')) return Promise.resolve(new Response('', { status: 503 }));
  if (!chemin.startsWith('/api/v1/course-player/')) return fetchOriginal(entree, init);
  const reste = chemin.slice('/api/v1/course-player/'.length);
  if (!ROUTES.some(r => reste === r || reste.startsWith(`${r}/`))) return VIDE();
  let corps = init?.body;
  if (typeof corps === 'string') {
    try {
      const d = JSON.parse(corps);
      if (d && typeof d === 'object') { delete d.deck_id; if (!d.matiere) d.matiere = 'physique'; corps = JSON.stringify(d); }
    } catch { /* corps non JSON */ }
  }
  const entetes = new Headers(init?.headers || {});
  entetes.delete('Authorization');
  entetes.set('X-Visiteur', VISITEUR);
  return fetchOriginal(`${PUBLIC}/${reste}`, { ...init, body: corps, headers: entetes });
};

/** `?diapo=<id>` : la séance s'ouvre sur cette diapositive. */
function aPartirDe(deck: CourseDeck, diapo: string | null): CourseDeck {
  const toutes = deck.activities.flatMap(a => a.slides);
  const debut = diapo ? toutes.findIndex(s => s.id === diapo) : -1;
  if (debut <= 0) return deck;
  const gardees = new Set(toutes.slice(debut).map(s => s.id));
  return { ...deck, activities: deck.activities.map(a => ({ ...a, slides: a.slides.filter(s => gardees.has(s.id)) })).filter(a => a.slides.length) };
}

function Accueil() {
  return (
    <div className="min-h-[100dvh] bg-[#101826] px-4 py-6 text-white sm:px-8 [@media(max-height:520px)]:py-3">
      <div className="mx-auto max-w-4xl">
        <p className="text-sm text-sky-200/80">Moalim · 2ᵉ Bac PC BIOF</p>
        <h1 className="mt-1 text-2xl font-bold sm:text-3xl [@media(max-height:520px)]:text-xl">Révisions de physique-chimie</h1>
        <p className="mt-1 text-[15px] text-white/70">Deux séances au tableau avec le professeur Moalim, le national résolu pas à pas, puis un examen de 30 minutes corrigé.</p>
        <div className="mt-5 grid gap-3 sm:grid-cols-2 [@media(max-height:520px)]:mt-3 [@media(max-height:520px)]:gap-2">
          {MATIERES.filter(m => source(m.cours)).map(m => (
            <div key={m.cle} className="rounded-2xl border border-white/15 bg-white/5 p-4 [@media(max-height:520px)]:p-3">
              <span className="inline-block rounded-full px-2 py-0.5 text-xs font-semibold" style={{ background: m.couleur }}>{m.nom}</span>
              <h2 className="mt-2 text-lg font-semibold">{m.titre}</h2>
              <p className="mt-1 text-[14px] leading-snug text-white/70">{m.sous}</p>
              <div className="mt-3 flex flex-wrap gap-2">
                <a href={`?cours=${m.cours}`} className="rounded-lg bg-white/10 px-3 py-1.5 text-sm font-semibold hover:bg-white/20">① La révision →</a>
                <a href={`?examen=${m.cle}`} className="rounded-lg border border-amber-300/60 px-3 py-1.5 text-sm font-semibold text-amber-200 hover:bg-amber-300/10">② L’examen de 30 min →</a>
              </div>
            </div>))}
        </div>
      </div>
    </div>
  );
}

function Cours({ id }: { id: string }) {
  const [cours, setCours] = useState<CourseDeck | null>(null);
  const [introuvable, setIntrouvable] = useState(false);
  useEffect(() => {
    const charger = source(id);
    if (!charger) { setIntrouvable(true); return; }
    void charger().then(d => setCours(aPartirDe(d, new URLSearchParams(window.location.search).get('diapo')))).catch(() => setIntrouvable(true));
  }, [id]);
  if (introuvable) return <Accueil />;
  if (!cours) return <div className="grid h-[100dvh] place-items-center bg-[#0a0a18] text-white/70">Chargement de la révision…</div>;
  const m = MATIERES.find(x => x.cours === id);
  return (
    <div className="flex h-[100dvh] w-screen flex-col bg-[#0a0a18] p-1 text-white sm:p-2 [@media(max-height:520px)]:p-0.5">
      <div className="flex h-9 shrink-0 items-center gap-2 px-2 text-sm [@media(max-height:520px)]:h-7 [@media(max-height:520px)]:text-xs">
        <a href="./" className="shrink-0 rounded-lg px-2 py-1 text-white/70 hover:bg-white/10" title="Accueil">☰</a>
        <select value={id} onChange={e => { window.location.search = `cours=${e.target.value}`; }}
          className="min-w-0 flex-1 truncate rounded-lg border border-white/15 bg-[#121a33] px-2 py-1 text-white sm:max-w-md [@media(max-height:520px)]:py-0">
          {MATIERES.filter(x => source(x.cours)).map(x => <option key={x.cours} value={x.cours}>{`${x.nom} — ${x.titre}`}</option>)}
        </select>
        {m && <a href={`?examen=${m.cle}`} className="shrink-0 rounded-lg border border-amber-300/50 px-2 py-1 text-amber-200 hover:bg-amber-300/10 [@media(max-height:520px)]:py-0">Examen</a>}
      </div>
      <div className="min-h-0 w-full flex-1 overflow-hidden rounded-2xl border border-white/10">
        <CoursePlayer deck={cours} language="mixed" mode="concentration" tuteur3D />
      </div>
    </div>
  );
}

function Page() {
  const params = new URLSearchParams(window.location.search);
  const ex = MATIERES.find(m => m.cle === params.get('examen'));
  if (ex) {
    utiliserSujet({ sujet: ex.sujet as never, piste: cle => ex.voix[cle], suivi: false, matiere: 'physique', retour: '2ᵉ Bac PC' });
    return <Examen />;
  }
  const id = params.get('cours');
  return id ? <Cours id={id} /> : <Accueil />;
}

createRoot(document.getElementById('root')!).render(<Page />);
