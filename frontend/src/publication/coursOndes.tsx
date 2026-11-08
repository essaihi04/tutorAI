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
 */
import { createRoot } from 'react-dom/client';
import '../index.css';
import '../services/audioUnlock';
import CoursePlayer from '../components/course/CoursePlayer';
import type { CourseDeck } from '../components/course/types';
import source from '../../../backend/data/courses/phys_ch1_waves_exemple.json?raw';

const COURS = JSON.parse(source) as CourseDeck;

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
const ROUTES = ['question-eleve', 'reexplication', 'answer-reaction', 'sim-reaction', 'acquis'];

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

function CoursOndes() {
  const deck = aPartirDe(COURS, new URLSearchParams(window.location.search).get('diapo'));
  return (
    <div className="h-[100dvh] w-screen bg-[#0a0a18] text-white p-1 sm:p-2">
      <div className="h-full w-full overflow-hidden rounded-2xl border border-white/10">
        <CoursePlayer deck={deck} language="mixed" mode="concentration" tuteur3D />
      </div>
    </div>
  );
}

createRoot(document.getElementById('root')!).render(<CoursOndes />);
