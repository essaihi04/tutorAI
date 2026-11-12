/**
 * Page publique du cours exemple des ondes (8 novembre 2026) : https://moalim.online/cours-ondes/
 *
 * Elle monte seulement le lecteur de cours, en mode concentration avec le tuteur 3D, sur le cours
 * `phys_ch1_waves_exemple`, sans compte ni connexion. Construite à part (`vite.cours-ondes.config.ts`) et
 * publiée dans son propre dossier par `scripts/publier_cours_ondes.py` : le reste du site n'est pas touché.
 * Sans compte : les appels du lecteur partent vers les routes publiques `/api/v1/public/cours-ondes/…` (questions
 * libres et micro par Gemini 2.5 Flash, réexplication, voix Kaggle réveillée à l'ouverture, suivi des acquis par
 * visiteur), plafonnées côté serveur (`public_cours.py`).
 * `?diapo=<id>` ouvre le cours sur une diapositive.
 *
 * Lien libre des profs (10 novembre 2026) : `?cours=<id>` ouvre n'importe quel cours refait en mode concentration
 * (`backend/data/courses/<matière>_chN_<clé>.json`), `?cours=liste` les liste. Sur chaque diapositive, le prof donne
 * un vote (👍 bon / 👎 à corriger) et un commentaire (`/avis`), que l'admin lit dans l'onglet « Avis des profs ».
 */
import { useCallback, useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import '../index.css';
import '../services/audioUnlock';
import CoursePlayer from '../components/course/CoursePlayer';
import type { CourseDeck } from '../components/course/types';

const DEFAUT = 'phys_ch1_waves_exemple';
// Chargés à la demande : un seul cours est téléchargé par visite.
const SOURCES = import.meta.glob([
  '../../../backend/data/courses/*_ch*_*.json',
  '!../../../backend/data/courses/*_course_v1.json',
  '!../../../backend/data/courses/*_script_*.json',
], { import: 'default' }) as Record<string, () => Promise<CourseDeck>>;
const COURS_DISPONIBLES = Object.keys(SOURCES).map(f => f.split('/').pop()!.replace(/\.json$/, '')).sort();
const source = (id: string) => SOURCES[Object.keys(SOURCES).find(f => f.endsWith(`/${id}.json`)) || ''];

// Titres des cours (seul le champ `title` est embarqué, pas le cours entier) : la liste déroulante du haut.
const TITRES_BRUTS = import.meta.glob([
  '../../../backend/data/courses/*_ch*_*.json',
  '!../../../backend/data/courses/*_course_v1.json',
  '!../../../backend/data/courses/*_script_*.json',
], { import: 'title', eager: true }) as Record<string, string>;
const TITRES: Record<string, string> = Object.fromEntries(
  Object.entries(TITRES_BRUTS).map(([f, t]) => [f.split('/').pop()!.replace(/\.json$/, ''), t]));

/** Les matières : un lien par matière pour les profs (`?matiere=physique|svt|maths`). */
const MATIERES = [
  { cle: 'physique', nom: 'Physique-chimie', prefixes: ['phys_', 'chem_'] },
  { cle: 'svt', nom: 'SVT', prefixes: ['svt_'] },
  { cle: 'maths', nom: 'Mathématiques', prefixes: ['math_'] },
];
const numero = (id: string) => Number(/_ch(\d+)_/.exec(id)?.[1] || 0);
const matiereDe = (id: string) => MATIERES.find(m => m.prefixes.some(p => id.startsWith(p)));
const coursDe = (cle: string | null) => COURS_DISPONIBLES
  .filter(id => !cle || matiereDe(id)?.cle === cle)
  .sort((a, b) => MATIERES.findIndex(m => m === matiereDe(a)) - MATIERES.findIndex(m => m === matiereDe(b))
    || (a.startsWith('chem_') ? 1 : 0) - (b.startsWith('chem_') ? 1 : 0) || numero(a) - numero(b));
const lienCours = (id: string, matiere: string | null) => `?${matiere ? `matiere=${matiere}&` : ''}cours=${id}`;

/** La barre du haut : la matière et la liste déroulante des cours (de cette matière si le lien en donne une). */
function Navigation({ id, matiere }: { id: string; matiere: string | null }) {
  const liste = coursDe(matiere);
  const m = matiereDe(id);
  return (
    <div className="flex h-10 items-center gap-2 px-2 text-sm">
      <a href={matiere ? `?matiere=${matiere}&cours=liste` : '?cours=liste'} className="shrink-0 rounded-lg px-2 py-1 text-white/70 hover:bg-white/10" title="Tous les cours">☰</a>
      <span className="hidden shrink-0 text-white/50 sm:inline">{m?.nom || ''}</span>
      <select value={id} onChange={e => { window.location.search = lienCours(e.target.value, matiere); }}
        className="min-w-0 flex-1 truncate rounded-lg border border-white/15 bg-[#121a33] px-2 py-1 text-white sm:max-w-xl">
        {MATIERES.filter(x => !matiere || x.cle === matiere).map(x => (
          <optgroup key={x.cle} label={x.nom}>
            {liste.filter(c => matiereDe(c) === x).map(c => (
              <option key={c} value={c}>{`Ch. ${numero(c)} — ${TITRES[c] || c}`}</option>
            ))}
          </optgroup>
        ))}
      </select>
    </div>
  );
}

const lire = (k: string) => { try { return localStorage.getItem(k) || ''; } catch { return ''; } };
const garder = (k: string, v: string) => { try { localStorage.setItem(k, v); } catch { /* navigation privée */ } };

// ── Sans compte : le visiteur a un identifiant tiré au hasard, gardé dans son navigateur (son suivi des acquis). ──
const VISITEUR = (() => {
  try {
    const k = 'cours-ondes:visiteur';
    let v = localStorage.getItem(k);
    if (!v) { v = (crypto.randomUUID?.() || `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 12)}`); localStorage.setItem(k, v); }
    return v;
  } catch { return `v-${Math.random().toString(36).slice(2, 14)}`; }
})();
const PUBLIC = '/api/v1/public/cours-ondes';
/** Les routes publiques qui existent ; les autres appels du lecteur (progression d'un compte…) n'ont pas lieu ici. */
const ROUTES = ['question-eleve', 'transcrire', 'ocr-reponse', 'reexplication', 'answer-reaction', 'sim-reaction', 'acquis', 'memoire'];

// Le lecteur parle au serveur comme pour un élève connecté (/course-player/…, /tts/speak) : ici, les mêmes demandes
// partent vers les routes publiques (plafonnées), avec l'identifiant du visiteur à la place du jeton.
const fetchOriginal = window.fetch.bind(window);
window.fetch = (entree: RequestInfo | URL, init?: RequestInit) => {
  const url = typeof entree === 'string' ? entree : entree instanceof URL ? entree.href : entree.url;
  const chemin = url.replace(location.origin, '');
  let cible: string | null = null;
  if (chemin.startsWith('/api/v1/tts/speak')) cible = `${PUBLIC}/voix`;
  else if (chemin.startsWith('/api/v1/course-player/')) {
    const reste = chemin.slice('/api/v1/course-player/'.length);
    if (ROUTES.some(r => reste === r || reste.startsWith(`${r}/`))) cible = `${PUBLIC}/${reste}`;
    else return Promise.resolve(new Response('{}', { status: 204 }));
  }
  if (!cible) return fetchOriginal(entree, init);
  const entetes = new Headers(init?.headers || {});
  entetes.delete('Authorization');
  entetes.set('X-Visiteur', VISITEUR);
  return fetchOriginal(cible, { ...init, headers: entetes });
};

// La voix Kaggle s'allume dès que le lien est ouvert (démarrage à froid ≈ 2 min 30, pendant la première diapositive),
// puis reste éveillée tant que l'élève travaille ; sans activité depuis 10 min, on la laisse s'endormir (quota GPU).
let derniereActivite = Date.now();
['pointerdown', 'keydown', 'touchstart'].forEach(e => window.addEventListener(e, () => { derniereActivite = Date.now(); }, { passive: true, capture: true }));
const eveiller = () => {
  if (document.visibilityState !== 'visible' || Date.now() - derniereActivite > 10 * 60_000) return;
  void fetchOriginal(`${PUBLIC}/eveil`, { method: 'POST', headers: { 'X-Visiteur': VISITEUR } }).catch(() => { /* la page marche sans voix live */ });
};
eveiller();
window.setInterval(eveiller, 4 * 60_000);
document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'visible') { derniereActivite = Date.now(); eveiller(); } });

function aPartirDe(deck: CourseDeck, diapo: string | null): CourseDeck {
  const toutes = deck.activities.flatMap(a => a.slides);
  const debut = diapo ? toutes.findIndex(s => s.id === diapo) : -1;
  if (debut <= 0) return deck;
  const gardees = new Set(toutes.slice(debut).map(s => s.id));
  return { ...deck, activities: deck.activities.map(a => ({ ...a, slides: a.slides.filter(s => gardees.has(s.id)) })).filter(a => a.slides.length) };
}

type Diapo = { id: string; title: string; position: number; total: number };
type MonAvis = { vote: 'bon' | 'mauvais' | null; commentaire: string };

/** Le panneau du prof qui relit : vote et commentaire de la diapositive affichée, enregistrés sur le serveur. */
function Relecture({ deckId, diapo: vue, ordre }: { deckId: string; diapo: Diapo | null; ordre: string[] }) {
  // La place dans le cours complet, même quand la page s'ouvre sur une diapositive (`?diapo=`).
  const diapo = vue && ordre.includes(vue.id) ? { ...vue, position: ordre.indexOf(vue.id) + 1, total: ordre.length } : vue;
  const [ouvert, setOuvert] = useState(() => lire('cours-ondes:relecture') === 'ouvert');
  const [nom, setNom] = useState(() => lire('cours-ondes:relecteur'));
  const [avis, setAvis] = useState<Record<string, MonAvis>>({});
  const [brouillon, setBrouillon] = useState('');
  const [etat, setEtat] = useState<'' | 'envoi' | 'ok' | 'erreur'>('');

  useEffect(() => {
    void fetchOriginal(`${PUBLIC}/avis/${encodeURIComponent(deckId)}`, { headers: { 'X-Visiteur': VISITEUR } })
      .then(r => (r.ok ? r.json() : { avis: {} })).then(d => setAvis(d.avis || {})).catch(() => { /* hors ligne */ });
  }, [deckId]);
  const idDiapo = diapo?.id || '';
  useEffect(() => { setBrouillon(idDiapo ? avis[idDiapo]?.commentaire || '' : ''); setEtat(''); }, [idDiapo]); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => { if (idDiapo && avis[idDiapo] && !brouillon) setBrouillon(avis[idDiapo].commentaire || ''); }, [avis]); // eslint-disable-line react-hooks/exhaustive-deps

  const envoyer = useCallback(async (vote: MonAvis['vote'], commentaire: string) => {
    if (!diapo) return;
    setEtat('envoi');
    try {
      const r = await fetchOriginal(`${PUBLIC}/avis`, {
        method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Visiteur': VISITEUR },
        body: JSON.stringify({ deck_id: deckId, slide_id: diapo.id, slide_titre: diapo.title, position: diapo.position, vote, commentaire, relecteur: nom }),
      });
      if (!r.ok) throw new Error(String(r.status));
      setAvis(a => ({ ...a, [diapo.id]: { vote, commentaire } }));
      setEtat('ok');
    } catch { setEtat('erreur'); }
  }, [deckId, diapo, nom]);

  if (!diapo) return null;
  const mien = avis[diapo.id];
  const notees = Object.keys(avis).length;
  // Replié : une petite barre en bas à gauche, au-dessus des commandes du lecteur — un clic pour voter, 💬 pour écrire.
  if (!ouvert) {
    return (
      <div className="fixed bottom-[7rem] left-2 z-[300] flex items-center gap-1 rounded-full bg-[#14142a]/90 border border-amber-400/60 shadow-lg px-1.5 py-1 text-xs text-white">
        <span className="px-1.5 text-amber-300 font-semibold" title="Diapositives notées">📝 {notees}/{diapo.total}</span>
        <button onClick={() => void envoyer('bon', mien?.commentaire || '')} title="Diapositive bonne"
          className={`rounded-full px-2 py-0.5 ${mien?.vote === 'bon' ? 'bg-green-500 text-black' : 'hover:bg-green-500/25'}`}>👍</button>
        <button onClick={() => void envoyer('mauvais', mien?.commentaire || '')} title="Diapositive à corriger"
          className={`rounded-full px-2 py-0.5 ${mien?.vote === 'mauvais' ? 'bg-red-500 text-black' : 'hover:bg-red-500/25'}`}>👎</button>
        <button onClick={() => { setOuvert(true); garder('cours-ondes:relecture', 'ouvert'); }} title="Écrire un commentaire"
          className={`rounded-full px-2 py-0.5 hover:bg-amber-400/25 ${mien?.commentaire ? 'text-amber-300' : ''}`}>💬</button>
        {etat === 'ok' && <span className="pr-1 text-green-300">✓</span>}
        {etat === 'erreur' && <span className="pr-1 text-rose-300">!</span>}
      </div>
    );
  }
  return (
    <div className="fixed bottom-[7rem] left-2 z-[300] w-[min(20rem,calc(100vw-1rem))] rounded-xl bg-[#14142a]/95 border border-amber-400/60 shadow-2xl p-3 text-white text-sm space-y-2">
      <div className="flex items-start gap-2">
        <div className="flex-1 min-w-0">
          <div className="text-[11px] text-amber-300">Relecture · diapositive {diapo.position}/{diapo.total} · {notees} notée(s)</div>
          <div className="font-medium truncate">{diapo.title || diapo.id}</div>
        </div>
        <button onClick={() => { setOuvert(false); garder('cours-ondes:relecture', 'ferme'); }} className="text-white/60 hover:text-white px-1" aria-label="Réduire">—</button>
      </div>
      <input value={nom} onChange={e => { setNom(e.target.value); garder('cours-ondes:relecteur', e.target.value); }}
        placeholder="Votre nom (prof)" className="w-full rounded-lg bg-white/10 border border-white/15 px-2 py-1 text-sm placeholder:text-white/40" />
      <div className="flex gap-2">
        <button onClick={() => void envoyer('bon', brouillon)}
          className={`flex-1 rounded-lg py-1.5 border ${mien?.vote === 'bon' ? 'bg-green-500 border-green-400 text-black' : 'border-green-400/60 hover:bg-green-500/20'}`}>👍 Bon</button>
        <button onClick={() => void envoyer('mauvais', brouillon)}
          className={`flex-1 rounded-lg py-1.5 border ${mien?.vote === 'mauvais' ? 'bg-red-500 border-red-400 text-black' : 'border-red-400/60 hover:bg-red-500/20'}`}>👎 À corriger</button>
      </div>
      <textarea value={brouillon} onChange={e => { setBrouillon(e.target.value); setEtat(''); }} rows={3}
        placeholder="Commentaire : ce qui est faux, à dire autrement, à ajouter…"
        className="w-full rounded-lg bg-white/10 border border-white/15 px-2 py-1 text-sm placeholder:text-white/40 resize-y" />
      <div className="flex items-center gap-2">
        <button disabled={!brouillon.trim() || etat === 'envoi'} onClick={() => void envoyer(mien?.vote ?? null, brouillon)}
          className="rounded-lg bg-amber-400 text-black font-semibold px-3 py-1 disabled:opacity-40">Envoyer le commentaire</button>
        <span className="text-xs text-white/60">{etat === 'envoi' ? 'Envoi…' : etat === 'ok' ? '✓ Enregistré' : etat === 'erreur' ? 'Échec, réessayez' : ''}</span>
      </div>
    </div>
  );
}

function Liste({ matiere }: { matiere: string | null }) {
  return (
    <div className="min-h-[100dvh] bg-[#0a0a18] text-white p-6">
      <h1 className="text-xl font-semibold mb-1">Cours à relire</h1>
      <p className="mb-5 text-sm text-white/60">Sur chaque diapositive : 👍 / 👎 et un commentaire (barre en bas à gauche).</p>
      {MATIERES.filter(m => !matiere || m.cle === matiere).map(m => (
        <section key={m.cle} className="mb-6">
          <h2 className="mb-2 font-semibold text-amber-200">{m.nom}</h2>
          <ul className="space-y-1.5">
            {coursDe(m.cle).map(id => (
              <li key={id}><a className="text-amber-300 underline" href={lienCours(id, matiere)}>{`Ch. ${numero(id)} — ${TITRES[id] || id}`}</a></li>
            ))}
          </ul>
        </section>
      ))}
    </div>
  );
}

function CoursOndes() {
  const params = new URLSearchParams(window.location.search);
  const matiere = MATIERES.some(m => m.cle === params.get('matiere')) ? params.get('matiere') : null;
  const id = params.get('cours') || (matiere ? coursDe(matiere)[0] : DEFAUT);
  const [cours, setCours] = useState<CourseDeck | null>(null);
  const [ordre, setOrdre] = useState<string[]>([]);
  const [introuvable, setIntrouvable] = useState(false);
  const [diapo, setDiapo] = useState<Diapo | null>(null);
  useEffect(() => {
    const charger = source(id);
    if (!charger) { setIntrouvable(true); return; }
    void charger().then(d => { setOrdre(d.activities.flatMap(a => a.slides.map(sl => sl.id))); setCours(aPartirDe(d, params.get('diapo'))); }).catch(() => setIntrouvable(true));
  }, [id]); // eslint-disable-line react-hooks/exhaustive-deps
  if (id === 'liste' || introuvable) return <Liste matiere={matiere} />;
  if (!cours) return <div className="h-[100dvh] grid place-items-center bg-[#0a0a18] text-white/70">Chargement du cours…</div>;
  return (
    <div className="flex h-[100dvh] w-screen flex-col bg-[#0a0a18] text-white p-1 sm:p-2">
      <Navigation id={id} matiere={matiere} />
      <div className="min-h-0 w-full flex-1 overflow-hidden rounded-2xl border border-white/10">
        <CoursePlayer deck={cours} language="mixed" mode="concentration" tuteur3D onSlideChange={setDiapo} />
      </div>
      <Relecture deckId={cours.id} diapo={diapo} ordre={ordre} />
    </div>
  );
}

createRoot(document.getElementById('root')!).render(<CoursOndes />);
