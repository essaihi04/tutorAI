/**
 * Le lien libre du Tronc Commun Sciences, option française, physique-chimie (25 novembre 2026) : https://moalim.online/TCF/
 *
 * Trois cours refaits au tableau en mode concentration, d'après le livre « Cours physique-chimie TCSF » (programme 2020),
 * sans aucune image du livre : chaque figure et chaque expérience est redessinée et animée.
 *   - `./`                                     l'accueil : chimie (2 chapitres) et physique (1 cours) ;
 *   - `?cours=tc_chim_synthese`                « Synthèse d'une espèce chimique » ;
 *   - `?cours=tc_chim_atome`                   « Modèle de l'atome » ;
 *   - `?cours=tc_phys_mouvement_inertie`       « Le mouvement et le principe d'inertie » ;
 *   - `?cours=tc_tcf_revision`                 la révision des trois chapitres (~30 diapos, demande de l'utilisateur) ;
 *   - `?examen`                                l'évaluation formative des trois chapitres (20 points, sans chronomètre) ;
 *   - `?classe` / `?c=<code>`                  le mode classe (écran du prof / téléphone de l'élève), sans fiche ;
 *   - `?t=<code>`                              le téléphone relié au PC de l'élève (« 📱 Avec mon téléphone »).
 * Comme le Tronc Commun SVT (demande de l'utilisateur : « une évaluation englobant tous ces chapitres, comme chez SVT »).
 * Même principe que /tronc-commun et /2bacpcf : hors de la base des élèves et de l'application, page construite à part
 * (`vite.tcf.config.ts`) et publiée dans son propre dossier par `scripts/publier_tcf.py`. Fiche de l'élève remplie une
 * seule fois, suivi par la route `/api/v1/public/tcf` (onglet admin « Tronc Commun PC »). Le tuteur répond par les routes
 * publiques du cours des ondes, l'identifiant du cours retiré des demandes. Pas de voix en direct : les pistes Bodi sont
 * enregistrées.
 */
import { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import '../index.css';
import '../services/audioUnlock';
import CoursePlayer from '../components/course/CoursePlayer';
import type { CourseDeck } from '../components/course/types';
import Fiche from './tronc-commun/Fiche';
import Examen, { utiliserSujet } from './tronc-commun/Examen';
import { ProfClasse, TelephoneClasse } from './tronc-commun/Classe';
import Retravailler from './tronc-commun/Retravailler';
import { SUJET_TCF, VOIX_TCF } from './tcf/sujet';
import { REVOIR_TCF } from './tcf/revoir';
import { activerPhotoTelephone, PageTelephone } from '../components/course/photoTelephone';
import { configurerSuivi, eleveEnregistre, garderEleve, maReprise, suivre, useTempsPasse, type Eleve, type Reprise } from './tronc-commun/suivi';

const API_TCF = '/api/v1/public/tcf';
configurerSuivi({ api: API_TCF, cle: 'moalim:tcf:eleve' });

const SOURCES = import.meta.glob(['./tcf/cours/tc_*.json', '!./tcf/cours/*_voix.json'], { import: 'default' }) as Record<string, () => Promise<CourseDeck>>;
const source = (id: string) => SOURCES[Object.keys(SOURCES).find(f => f.endsWith(`/${id}.json`)) || ''];
const MATIERES = [
  { cle: 'chimie', nom: 'Chimie', couleur: '#c2571a', matiere: 'chimie', cours: [
    { id: 'tc_chim_synthese', titre: 'Synthèse d’une espèce chimique', sous: 'Chimie de synthèse, réactifs et produits, chauffage à reflux, synthèse du savon, identification par CCM' },
    { id: 'tc_chim_atome', titre: 'Modèle de l’atome', sous: 'Histoire du modèle, électrons et noyau, écriture ᴬ_Z X, masse et taille, isotopes, ions, élément, couches K, L, M' },
  ] },
  { cle: 'physique', nom: 'Physique', couleur: '#2a78d6', matiere: 'physique', cours: [
    { id: 'tc_phys_mouvement_inertie', titre: 'Le mouvement et le principe d’inertie', sous: 'Référentiel, repères, trajectoire, vitesses, mouvement rectiligne uniforme et circulaire uniforme, centre d’inertie, principe d’inertie, centre de masse' },
  ] },
  { cle: 'revision', nom: 'Révision', couleur: '#2f5d8a', matiere: 'physique', cours: [
    { id: 'tc_tcf_revision', titre: 'Révision des trois chapitres', sous: 'L’essentiel en une trentaine de diapos : chaque définition, chaque formule et chaque méthode refaite sur un nouvel exemple' },
  ] },
];
const TOUS = MATIERES.flatMap(m => m.cours.map(c => ({ ...c, m })));

/** L'évaluation des trois chapitres ; `suivi` : seulement avec la fiche de l'élève (pas en mode classe). */
function prendreSujet(suivi = true) {
  utiliserSujet({ sujet: SUJET_TCF as never, piste: cle => (VOIX_TCF.includes(cle) ? `/media/audio/courses/tc_tcf_examen/${cle}.mp3` : undefined),
    suivi, matiere: 'physique', retour: 'Tronc Commun PC', cle: 'examen_tcf', revoir: q => REVOIR_TCF[q] || [] });
}

// ── Lien libre : rien n'est gardé d'une visite à l'autre (même règle que /tronc-commun/).
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
/** le cours ouvert, pour le suivi des réponses et la matière envoyée au tuteur */
let coursActuel = '';

const fetchOriginal = window.fetch.bind(window);
window.fetch = (entree: RequestInfo | URL, init?: RequestInit) => {
  const url = typeof entree === 'string' ? entree : entree instanceof URL ? entree.href : entree.url;
  const chemin = url.replace(location.origin, '');
  // pas de voix en direct : les pistes sont enregistrées, le reste se joue au temps de lecture
  if (chemin.startsWith('/api/v1/tts/')) return Promise.resolve(new Response('', { status: 503 }));
  if (!chemin.startsWith('/api/v1/course-player/')) return fetchOriginal(entree, init);
  const reste = chemin.slice('/api/v1/course-player/'.length);
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
      if (d && typeof d === 'object') {
        delete d.deck_id;
        if (!d.matiere) d.matiere = TOUS.find(c => c.id === coursActuel)?.m.matiere || 'physique';
        corps = JSON.stringify(d);
      }
    } catch { /* corps non JSON : envoyé tel quel */ }
  }
  const entetes = new Headers(init?.headers || {});
  entetes.delete('Authorization');
  entetes.set('X-Visiteur', VISITEUR);
  // les corrections passent par la route du lien : plafond compté par élève (une classe partage le même wifi)
  const eleve = eleveEnregistre();
  if (reste === 'answer-reaction' && eleve) {
    entetes.set('X-Eleve', eleve.id);
    return fetchOriginal(`${API_TCF}/answer-reaction`, { ...init, body: corps, headers: entetes });
  }
  return fetchOriginal(`${PUBLIC}/${reste}`, { ...init, body: corps, headers: entetes });
};
// « 📱 Avec mon téléphone » à côté de chaque « 📷 Photo »
activerPhotoTelephone(`${location.origin}${location.pathname}`);

function Accueil() {
  const eleve = eleveEnregistre();
  return (
    <div className="min-h-[100dvh] bg-[#14121f] px-4 py-6 text-white sm:px-8 [@media(max-height:520px)]:py-3">
      <div className="mx-auto max-w-4xl">
        <p className="text-sm text-orange-200/80">Moalim · Tronc Commun Sciences · option française</p>
        <h1 className="mt-1 text-2xl font-bold sm:text-3xl [@media(max-height:520px)]:text-xl">Physique-chimie</h1>
        <p className="mt-1 text-[15px] text-white/70">Les cours au tableau avec le professeur Moalim : chaque expérience est dessinée et animée, chaque méthode faite pas à pas.</p>
        {eleve && <p className="mt-1 text-sm text-white/60">Élève : <b className="text-white/85">{eleve.nom}</b> · {eleve.classe}
          <button onClick={() => { garderEleve(null); window.location.reload(); }} className="ml-2 underline hover:text-white">ce n’est pas moi</button></p>}
        <div className="mt-5 grid gap-3 sm:grid-cols-2 [@media(max-height:520px)]:mt-3 [@media(max-height:520px)]:gap-2">
          {MATIERES.map(m => (
            <div key={m.cle} className="rounded-2xl border border-white/15 bg-white/5 p-4 [@media(max-height:520px)]:p-3">
              <span className="inline-block rounded-full px-2 py-0.5 text-xs font-semibold" style={{ background: m.couleur }}>{m.nom}</span>
              <div className="mt-1 grid gap-2">
                {m.cours.filter(c => source(c.id)).map(c => (
                  <a key={c.id} href={`?cours=${c.id}`} className="group block rounded-xl p-2 hover:bg-white/10">
                    <h2 className="text-lg font-semibold [@media(max-height:520px)]:text-base">{c.titre}</h2>
                    <p className="mt-0.5 text-[14px] leading-snug text-white/70 [@media(max-height:520px)]:hidden">{c.sous}</p>
                    <p className="mt-1 text-sm text-orange-300 group-hover:underline">Ouvrir le cours →</p>
                  </a>))}
                {!m.cours.some(c => source(c.id)) && <p className="p-2 text-sm text-white/50">Bientôt.</p>}
              </div>
            </div>))}
          <a href="?examen" className="group rounded-2xl border border-amber-300/50 bg-amber-300/10 p-4 hover:bg-amber-300/20 sm:col-span-2 [@media(max-height:520px)]:p-3">
            <span className="inline-block rounded-full bg-amber-500 px-2 py-0.5 text-xs font-semibold text-black">Évaluation</span>
            <h2 className="mt-2 text-lg font-semibold">Évaluation formative — les trois chapitres</h2>
            <p className="mt-1 text-[14px] leading-snug text-white/70">20 points, environ 50 minutes, sans chronomètre. Le tuteur corrige et explique chaque réponse.</p>
            <p className="mt-2 text-sm text-amber-300 group-hover:underline">Commencer →</p>
          </a>
        </div>
        <p className="mt-4 text-right text-sm [@media(max-height:520px)]:mt-2"><a href="?classe" className="text-white/45 underline hover:text-white/80">Mode classe (professeur)</a></p>
        {eleve && <Retravailler revoir={(_, q) => REVOIR_TCF[q] || []} nomExamen={() => 'Évaluation'} nomCours={c => TOUS.find(x => x.id === c)?.titre || c} />}
      </div>
    </div>
  );
}

/** `?diapo=<id>` : le cours s'ouvre sur cette diapositive. */
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
  const [reprise, setReprise] = useState<Reprise | null | undefined>(undefined);
  useTempsPasse(id, !!cours);
  useEffect(() => { coursActuel = id; }, [id]);
  useEffect(() => {
    const charger = source(id);
    if (!charger) { setIntrouvable(true); return; }
    const diapo = new URLSearchParams(window.location.search).get('diapo');
    void Promise.all([charger(), diapo || !eleveEnregistre() ? Promise.resolve(null) : maReprise(id).catch(() => null)])
      .then(([d, r]) => { setReprise(r); setCours(aPartirDe(d, diapo)); }).catch(() => setIntrouvable(true));
  }, [id]);
  if (introuvable) return <Accueil />;
  if (!cours) return <div className="grid h-[100dvh] place-items-center bg-[#0a0a18] text-white/70">Chargement du cours…</div>;
  return (
    <div className="flex h-[100dvh] w-screen flex-col bg-[#0a0a18] p-1 text-white sm:p-2 [@media(max-height:520px)]:p-0.5">
      <div className="flex h-9 shrink-0 items-center gap-2 px-2 text-sm [@media(max-height:520px)]:h-7 [@media(max-height:520px)]:text-xs">
        <a href="./" className="shrink-0 rounded-lg px-2 py-1 text-white/70 hover:bg-white/10" title="Tronc Commun physique-chimie">☰</a>
        <select value={id} onChange={e => { window.location.search = `cours=${e.target.value}`; }}
          className="min-w-0 flex-1 truncate rounded-lg border border-white/15 bg-[#121a33] px-2 py-1 text-white sm:max-w-md [@media(max-height:520px)]:py-0">
          {TOUS.filter(c => source(c.id)).map(c => <option key={c.id} value={c.id}>{c.m.nom} — {c.titre}</option>)}
        </select>
        <a href="?examen" className="shrink-0 rounded-lg border border-amber-300/50 px-2 py-1 text-amber-200 hover:bg-amber-300/10 [@media(max-height:520px)]:py-0">Évaluation</a>
      </div>
      <div className="min-h-0 w-full flex-1 overflow-hidden rounded-2xl border border-white/10">
        <CoursePlayer deck={cours} language="mixed" mode="concentration" tuteur3D
          progress={reprise ? { current_slide_id: reprise.derniere, completed_slide_ids: reprise.vues, status: 'in_progress' } : null}
          onSlideChange={d => suivre({ type: 'diapo', cours: id, slide_id: d.id, titre: d.title, position: d.position, total: d.total })} />
      </div>
    </div>
  );
}

function TCF() {
  const params = new URLSearchParams(window.location.search);
  // mode classe et téléphone relié : sans fiche ni suivi
  if (params.has('classe')) { prendreSujet(false); return <ProfClasse />; }
  if (params.has('c')) { prendreSujet(false); return <TelephoneClasse code={params.get('c') || ''} />; }
  if (params.has('t')) return <PageTelephone code={params.get('t') || ''} titre="Moalim · Tronc Commun PC" />;
  return <AvecFiche />;
}

function AvecFiche() {
  const [eleve, setEleve] = useState<Eleve | null>(() => eleveEnregistre());
  // en local (vite dev) : pas de fiche, la route du lien n'existe pas encore sur le serveur de test
  if (!eleve && !import.meta.env.DEV) return <Fiche onEntree={setEleve} entete="Moalim · Tronc Commun Sciences · option française · physique-chimie" prefixe="TCSF" fond="#14121f" />;
  return <Pages />;
}

function Pages() {
  const params = new URLSearchParams(window.location.search);
  if (params.has('examen')) { prendreSujet(); return <Examen />; }
  const id = params.get('cours');
  return id ? <Cours id={id} /> : <Accueil />;
}

createRoot(document.getElementById('root')!).render(<TCF />);
