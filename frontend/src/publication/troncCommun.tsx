/**
 * Le lien libre du Tronc Commun Sciences BIOF, SVT (22 novembre 2026) : https://moalim.online/tronc-commun/
 *
 * Deux cours tirés des diaporamas d'un professeur et refaits au tableau en mode concentration, et une évaluation
 * formative pour une classe, sans compte. Hors du site : ni dans la base des élèves, ni dans l'application ; la page est
 * construite à part (`vite.tronc-commun.config.ts`) et publiée dans son propre dossier par `scripts/publier_tronc_commun.py`.
 *   - `./`                                  l'accueil : les deux cours et l'évaluation ;
 *   - `?cours=tc_svt_sortie_ecologique`     « La sortie écologique » (cours entier) ;
 *   - `?cours=tc_svt_facteurs_edaphiques`   « Les facteurs édaphiques », jusqu'à l'activité 3 ;
 *   - `?examen`                             l'évaluation formative (50 min au plus, sans chronomètre).
 *
 * Le tuteur répond par les routes publiques déjà en ligne (`/api/v1/public/cours-ondes/…`, plafonnées). Ces cours ne sont
 * pas sur le serveur : l'identifiant du cours est retiré des demandes (le serveur refuserait un cours qu'il ne connaît pas),
 * le contexte part avec la diapositive. Pas de voix en direct ici (la voix Bodi des cours se fera par lot) ; pas de suivi
 * des acquis ni de mémoire : chaque ouverture repart de zéro, comme le lien des ondes.
 */
import { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import '../index.css';
import '../services/audioUnlock';
import CoursePlayer from '../components/course/CoursePlayer';
import type { CourseDeck } from '../components/course/types';
import Examen from './tronc-commun/Examen';
import { API_TC, eleveEnregistre, garderEleve, inscrire, suivre, useTempsPasse, type Eleve } from './tronc-commun/suivi';

const SOURCES = import.meta.glob(['./tronc-commun/cours/tc_*.json', '!./tronc-commun/cours/*_voix.json'], { import: 'default' }) as Record<string, () => Promise<CourseDeck>>;
const COURS = [
  { id: 'tc_svt_sortie_ecologique', titre: 'La sortie écologique', sous: 'Outils et techniques, recensement, exploitation des relevés, notion d’écosystème', couleur: '#2e7d4f' },
  { id: 'tc_svt_facteurs_edaphiques', titre: 'Les facteurs édaphiques', sous: 'Texture et structure, propriétés chimiques et hydriques du sol (activités 1 à 3)', couleur: '#8a5a2b' },
  { id: 'tc_svt_revision', titre: 'Révision avec le tuteur', sous: 'Les deux chapitres en bref ; triangle des textures, perméabilité, histogramme et courbe de fréquence pas à pas', couleur: '#2f5d8a' },
];
const source = (id: string) => SOURCES[Object.keys(SOURCES).find(f => f.endsWith(`/${id}.json`)) || ''];

// ── Lien libre : rien n'est gardé d'une visite à l'autre (même règle que /cours-ondes/).
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
/** Ce que le tuteur sait faire sans compte et sans que le serveur connaisse le cours. */
const ROUTES = ['question-eleve', 'transcrire', 'ocr-reponse', 'reexplication', 'answer-reaction', 'sim-reaction', 'clavier-suggestions'];
const VIDE = () => Promise.resolve(new Response('{}', { status: 200, headers: { 'Content-Type': 'application/json' } }));

const fetchOriginal = window.fetch.bind(window);
window.fetch = (entree: RequestInfo | URL, init?: RequestInit) => {
  const url = typeof entree === 'string' ? entree : entree instanceof URL ? entree.href : entree.url;
  const chemin = url.replace(location.origin, '');
  // pas de voix en direct : le lecteur joue la diapositive au temps de lecture
  if (chemin.startsWith('/api/v1/tts/')) return Promise.resolve(new Response('', { status: 503 }));
  if (!chemin.startsWith('/api/v1/course-player/')) return fetchOriginal(entree, init);
  const reste = chemin.slice('/api/v1/course-player/'.length);
  // une réponse de l'élève dans le cours : elle part au suivi (onglet admin « Tronc Commun »)
  if (reste === 'acquis' && typeof init?.body === 'string') {
    try {
      const a = JSON.parse(init.body);
      if (!a.passee) suivre({ type: 'reponse_cours', cours: coursActuel, slide_id: a.slide_id, titre: a.slide_title, enonce: a.enonce, reponse: a.reponse, correct: a.correct ?? null });
    } catch { /* rien à suivre */ }
    return VIDE();
  }
  if (!ROUTES.some(r => reste === r || reste.startsWith(`${r}/`))) return VIDE();
  let corps = init?.body;
  if (typeof corps === 'string') {
    try {
      const d = JSON.parse(corps);
      if (d && typeof d === 'object') { delete d.deck_id; if (!d.matiere) d.matiere = 'svt'; corps = JSON.stringify(d); }
    } catch { /* corps non JSON : envoyé tel quel */ }
  }
  const entetes = new Headers(init?.headers || {});
  entetes.delete('Authorization');
  entetes.set('X-Visiteur', VISITEUR);
  // les corrections passent par la route du Tronc Commun : plafond compté par élève (une classe partage le même wifi)
  const eleve = eleveEnregistre();
  if (reste === 'answer-reaction' && eleve) {
    entetes.set('X-Eleve', eleve.id);
    return fetchOriginal(`${API_TC}/answer-reaction`, { ...init, body: corps, headers: entetes });
  }
  return fetchOriginal(`${PUBLIC}/${reste}`, { ...init, body: corps, headers: entetes });
};
/** le cours ouvert, pour le suivi des réponses */
let coursActuel = '';

function Accueil() {
  return (
    <div className="min-h-[100dvh] bg-[#0f1a14] px-4 py-6 text-white sm:px-8 [@media(max-height:520px)]:py-3">
      <div className="mx-auto max-w-4xl">
        <p className="text-sm text-emerald-200/80">Moalim · Tronc Commun Sciences BIOF</p>
        <h1 className="mt-1 text-2xl font-bold sm:text-3xl [@media(max-height:520px)]:text-xl">SVT — Sciences de l’environnement</h1>
        <p className="mt-1 text-[15px] text-white/70">Deux cours au tableau avec le professeur Moalim, une révision, puis une évaluation pour se préparer.</p>
        {eleveEnregistre() && <p className="mt-1 text-sm text-white/60">Élève : <b className="text-white/85">{eleveEnregistre()!.nom}</b> · {eleveEnregistre()!.classe}
          <button onClick={() => { garderEleve(null); window.location.reload(); }} className="ml-2 underline hover:text-white">ce n’est pas moi</button></p>}
        <div className="mt-5 grid gap-3 sm:grid-cols-2 lg:grid-cols-4 [@media(max-height:520px)]:mt-3 [@media(max-height:520px)]:grid-cols-4 [@media(max-height:520px)]:gap-2">
          {COURS.filter(c => source(c.id)).map((c, k) => (
            <a key={c.id} href={`?cours=${c.id}`} className="group rounded-2xl border border-white/15 bg-white/5 p-4 hover:bg-white/10 [@media(max-height:520px)]:p-3">
              <span className="inline-block rounded-full px-2 py-0.5 text-xs font-semibold" style={{ background: c.couleur }}>{c.id === 'tc_svt_revision' ? 'Révision' : `Cours ${k + 1}`}</span>
              <h2 className="mt-2 text-lg font-semibold">{c.titre}</h2>
              <p className="mt-1 text-[14px] leading-snug text-white/70">{c.sous}</p>
              <p className="mt-2 text-sm text-emerald-300 group-hover:underline">Ouvrir le cours →</p>
            </a>))}
          <a href="?examen" className="group rounded-2xl border border-amber-300/50 bg-amber-300/10 p-4 hover:bg-amber-300/20 [@media(max-height:520px)]:p-3">
            <span className="inline-block rounded-full bg-amber-500 px-2 py-0.5 text-xs font-semibold text-black">Évaluation</span>
            <h2 className="mt-2 text-lg font-semibold">Évaluation formative</h2>
            <p className="mt-1 text-[14px] leading-snug text-white/70">20 points, 50 minutes au plus, sans chronomètre. Le tuteur corrige et explique chaque réponse.</p>
            <p className="mt-2 text-sm text-amber-300 group-hover:underline">Commencer →</p>
          </a>
        </div>
      </div>
    </div>
  );
}

/** `?diapo=<id>` : le cours s'ouvre sur cette diapositive (comme /cours-ondes/). */
function aPartirDe(deck: CourseDeck, diapo: string | null): CourseDeck {
  const toutes = deck.activities.flatMap(a => a.slides);
  const debut = diapo ? toutes.findIndex(s => s.id === diapo) : -1;
  if (debut <= 0) return deck;
  const gardees = new Set(toutes.slice(debut).map(s => s.id));
  return { ...deck, activities: deck.activities.map(a => ({ ...a, slides: a.slides.filter(s => gardees.has(s.id)) })).filter(a => a.slides.length) };
}

function Cours({ id }: { id: string }) {
  const [cours, setCours] = useState<CourseDeck | null>(null);
  const [introuvable, setIntrouvable] = useState(false);
  useTempsPasse(id, !!cours);
  useEffect(() => { coursActuel = id; }, [id]);
  useEffect(() => {
    const charger = source(id);
    if (!charger) { setIntrouvable(true); return; }
    void charger().then(d => setCours(aPartirDe(d, new URLSearchParams(window.location.search).get('diapo')))).catch(() => setIntrouvable(true));
  }, [id]);
  if (introuvable) return <Accueil />;
  if (!cours) return <div className="grid h-[100dvh] place-items-center bg-[#0a0a18] text-white/70">Chargement du cours…</div>;
  return (
    <div className="flex h-[100dvh] w-screen flex-col bg-[#0a0a18] p-1 text-white sm:p-2 [@media(max-height:520px)]:p-0.5">
      <div className="flex h-9 shrink-0 items-center gap-2 px-2 text-sm [@media(max-height:520px)]:h-7 [@media(max-height:520px)]:text-xs">
        <a href="./" className="shrink-0 rounded-lg px-2 py-1 text-white/70 hover:bg-white/10" title="Tronc Commun">☰</a>
        <select value={id} onChange={e => { window.location.search = `cours=${e.target.value}`; }}
          className="min-w-0 flex-1 truncate rounded-lg border border-white/15 bg-[#121a33] px-2 py-1 text-white sm:max-w-md [@media(max-height:520px)]:py-0">
          {COURS.filter(c => source(c.id)).map((c, k) => <option key={c.id} value={c.id}>{c.id === 'tc_svt_revision' ? c.titre : `Cours ${k + 1} — ${c.titre}`}</option>)}
        </select>
        <a href="?examen" className="shrink-0 rounded-lg border border-amber-300/50 px-2 py-1 text-amber-200 hover:bg-amber-300/10 [@media(max-height:520px)]:py-0">Évaluation</a>
      </div>
      <div className="min-h-0 w-full flex-1 overflow-hidden rounded-2xl border border-white/10">
        <CoursePlayer deck={cours} language="mixed" mode="concentration" tuteur3D
          onSlideChange={d => suivre({ type: 'diapo', cours: id, slide_id: d.id, titre: d.title, position: d.position, total: d.total })} />
      </div>
    </div>
  );
}

/** La fiche d'entrée : remplie une seule fois (le navigateur s'en souvient ; la même fiche redonne le même élève). */
function Fiche({ onEntree }: { onEntree: (e: Eleve) => void }) {
  const [f, setF] = useState({ nom: '', classe: '', pere: '', telephone: '' });
  const [erreur, setErreur] = useState('');
  const [envoi, setEnvoi] = useState(false);
  const pret = f.nom.trim().length >= 2 && f.classe.trim() && f.pere.trim().length >= 2 && f.telephone.replace(/\D/g, '').length >= 9;
  const champ = (cle: keyof typeof f, libelle: string, aide: string, type = 'text') => (
    <label className="block">
      <span className="text-sm text-white/80">{libelle}</span>
      <input type={type} value={f[cle]} placeholder={aide} autoComplete="off" inputMode={type === 'tel' ? 'tel' : undefined}
        onChange={e => { setF(x => ({ ...x, [cle]: e.target.value })); setErreur(''); }}
        className="mt-0.5 w-full rounded-lg border border-white/20 bg-white/10 px-3 py-2 text-[16px] text-white placeholder:text-white/35 [@media(max-height:520px)]:py-1" />
    </label>);
  const entrer = async (ev: React.FormEvent) => {
    ev.preventDefault();
    if (!pret || envoi) return;
    setEnvoi(true);
    try { onEntree(await inscrire({ nom: f.nom.trim(), classe: f.classe.trim(), pere: f.pere.trim(), telephone: f.telephone.trim() })); }
    catch (e) { setErreur(e instanceof Error ? e.message : 'Inscription impossible, réessaie.'); }
    finally { setEnvoi(false); }
  };
  return (
    <div className="grid min-h-[100dvh] place-items-center bg-[#0f1a14] px-4 py-6 text-white [@media(max-height:520px)]:py-2">
      <form onSubmit={e => void entrer(e)} className="w-full max-w-lg rounded-2xl border border-white/15 bg-white/5 p-5 [@media(max-height:520px)]:p-3">
        <p className="text-sm text-emerald-200/80">Moalim · Tronc Commun Sciences BIOF · SVT</p>
        <h1 className="mt-1 text-xl font-bold [@media(max-height:520px)]:text-lg">Avant d’entrer : ta fiche</h1>
        <p className="mt-1 text-[14px] text-white/70">Une seule fois. Ton professeur suit ainsi ton travail : temps passé, évaluation, ce qu’il faut revoir.</p>
        <div className="mt-3 grid gap-2 sm:grid-cols-2 [@media(max-height:520px)]:grid-cols-2">
          {champ('nom', 'Nom et prénom de l’élève', 'ex. Salma El Idrissi')}
          {champ('classe', 'Classe', 'ex. TC 3')}
          {champ('pere', 'Nom du père', 'ex. Ahmed El Idrissi')}
          {champ('telephone', 'Téléphone du père', 'ex. 06 12 34 56 78', 'tel')}
        </div>
        {erreur && <p className="mt-2 text-sm text-rose-300">{erreur}</p>}
        <button disabled={!pret || envoi} className="mt-3 w-full rounded-xl bg-emerald-500 py-2 font-semibold text-black disabled:opacity-40 [@media(max-height:520px)]:mt-2 [@media(max-height:520px)]:py-1.5">
          {envoi ? 'Enregistrement…' : 'Entrer'}</button>
      </form>
    </div>
  );
}

function TroncCommun() {
  const [eleve, setEleve] = useState<Eleve | null>(() => eleveEnregistre());
  if (!eleve) return <Fiche onEntree={setEleve} />;
  return <Pages />;
}

function Pages() {
  const params = new URLSearchParams(window.location.search);
  if (params.has('examen')) return <Examen />;
  const id = params.get('cours');
  return id ? <Cours id={id} /> : <Accueil />;
}

createRoot(document.getElementById('root')!).render(<TroncCommun />);
