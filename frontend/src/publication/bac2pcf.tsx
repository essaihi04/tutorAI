/**
 * Le lien libre des révisions de 2ᵉ Bac PC BIOF (23 novembre 2026) : https://moalim.online/2bacpcf/
 *
 * Deux séances de révision assemblées à partir des cours existants (diapositives et voix déjà enregistrées, aucune voix
 * nouvelle), chacune avec les sujets du national et leur solution jouée pas à pas, puis un examen de 30 minutes corrigé :
 *   - `?cours=rev_phys_ondes_radioactivite`   physique : ondes lumineuses + décroissance radioactive ;
 *   - `?cours=rev_chim_deux_sens_equilibre`   chimie : transformations dans les deux sens + état d'équilibre ;
 *   - `?examen=physique` / `?examen=chimie`   deux exercices existants de 15 min, correction et voix comprises.
 *   - `?cours=phys_ch3_ondes_lumineuses`, `phys_ch4_radioactivite`, `phys_ch11_transformations_deux_sens`,
 *     `phys_ch12_etat_equilibre`   les 4 cours complets (23/11/2026), sur la carte de leur matière.
 * Fiche d'inscription comme au Tronc Commun (23/11/2026) : nom, prénom, classe 2BACPCF + numéro, père, téléphone, une
 * seule fois ; temps, diapositives, réponses et examens partent au suivi (`/public/2bacpcf`, onglet admin « 2ᵉ Bac PC »).
 * Le tuteur répond par les routes publiques du cours des ondes, l'identifiant du cours retiré des demandes ; les
 * corrections passent par la route du lien, plafonnées par élève.
 */
import { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import '../index.css';
import '../services/audioUnlock';
import CoursePlayer from '../components/course/CoursePlayer';
import type { CourseDeck } from '../components/course/types';
import Examen, { utiliserSujet } from './tronc-commun/Examen';
import Fiche from './tronc-commun/Fiche';
import Retravailler from './tronc-commun/Retravailler';
import { REVOIR_2BAC } from './tronc-commun/revoir';
import { configurerSuivi, eleveEnregistre, garderEleve, maReprise, suivre, useTempsPasse, type Eleve, type Reprise } from './tronc-commun/suivi';
import { SUJET_CHIMIE, SUJET_PHYSIQUE, VOIX_CHIMIE, VOIX_PHYSIQUE } from './bac2pcf/sujets';

const API_2BAC = '/api/v1/public/2bacpcf';
configurerSuivi({ api: API_2BAC, cle: 'moalim:2bacpcf:eleve' });

const SOURCES = {
  ...import.meta.glob('./bac2pcf/cours/rev_*.json', { import: 'default' }),
  // les cours complets, tels qu'ils sont servis aux élèves du site (chargés à la demande, un par visite)
  ...import.meta.glob([
    '../../../backend/data/courses/phys_ch3_ondes_lumineuses.json', '../../../backend/data/courses/phys_ch4_radioactivite.json',
    '../../../backend/data/courses/phys_ch11_transformations_deux_sens.json', '../../../backend/data/courses/phys_ch12_etat_equilibre.json',
  ], { import: 'default' }),
} as Record<string, () => Promise<CourseDeck>>;
const source = (id: string) => SOURCES[Object.keys(SOURCES).find(f => f.endsWith(`/${id}.json`)) || ''];
const MATIERES = [
  { cle: 'physique', nom: 'Physique', cours: 'rev_phys_ondes_radioactivite', titre: 'Ondes lumineuses et décroissance radioactive',
    sous: 'Diffraction, θ et L, fréquence et indice, dispersion ; noyau, désintégrations, loi de décroissance, activité et datation', couleur: '#2a78d6',
    sujet: SUJET_PHYSIQUE, voix: VOIX_PHYSIQUE,
    complets: [{ id: 'phys_ch3_ondes_lumineuses', titre: 'Propagation d’une onde lumineuse', n: 68 },
      { id: 'phys_ch4_radioactivite', titre: 'Décroissance radioactive', n: 87 }] },
  { cle: 'chimie', nom: 'Chimie', cours: 'rev_chim_deux_sens_equilibre', titre: 'Transformations dans les deux sens et état d’équilibre',
    sous: 'pH, taux d’avancement final, équilibre, conductimétrie ; quotient de réaction Qr, constante K, ce dont dépend τ', couleur: '#eb6834',
    sujet: SUJET_CHIMIE, voix: VOIX_CHIMIE,
    complets: [{ id: 'phys_ch11_transformations_deux_sens', titre: 'Transformations dans les deux sens', n: 56 },
      { id: 'phys_ch12_etat_equilibre', titre: 'État d’équilibre d’un système chimique', n: 58 }] },
];
/** tout ce qui s'ouvre au tableau, dans l'ordre des cartes : la révision puis les cours complets de chaque matière */
const SEANCES = MATIERES.flatMap(m => [{ id: m.cours, nom: `${m.nom} — révision`, m },
  ...m.complets.map(c => ({ id: c.id, nom: `${m.nom} — cours : ${c.titre}`, m }))]);

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
  // une réponse de l'élève dans un cours : elle part au suivi (onglet admin « 2ᵉ Bac PC »)
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
      if (d && typeof d === 'object') { delete d.deck_id; if (!d.matiere) d.matiere = 'physique'; corps = JSON.stringify(d); }
    } catch { /* corps non JSON */ }
  }
  const entetes = new Headers(init?.headers || {});
  entetes.delete('Authorization');
  entetes.set('X-Visiteur', VISITEUR);
  // les corrections passent par la route du lien : plafond compté par élève (une classe partage le même wifi)
  const eleve = eleveEnregistre();
  if (reste === 'answer-reaction' && eleve) {
    entetes.set('X-Eleve', eleve.id);
    return fetchOriginal(`${API_2BAC}/answer-reaction`, { ...init, body: corps, headers: entetes });
  }
  return fetchOriginal(`${PUBLIC}/${reste}`, { ...init, body: corps, headers: entetes });
};
/** le cours ouvert, pour le suivi des réponses */
let coursActuel = '';

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
        <p className="mt-1 text-[15px] text-white/70">Pour chaque matière : une révision au tableau avec le professeur Moalim et le national résolu pas à pas, un examen de 30 minutes corrigé, et les cours complets.</p>
        {eleveEnregistre() && <p className="mt-1 text-sm text-white/60">Élève : <b className="text-white/85">{eleveEnregistre()!.nom}</b> · {eleveEnregistre()!.classe}
          <button onClick={() => { garderEleve(null); window.location.reload(); }} className="ml-2 underline hover:text-white">ce n’est pas moi</button></p>}
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
              {m.complets.some(c => source(c.id)) && <>
                <p className="mt-3 text-xs font-semibold uppercase tracking-wide text-white/50 [@media(max-height:520px)]:mt-2">Les cours complets</p>
                <div className="mt-1 grid gap-1.5">
                  {m.complets.filter(c => source(c.id)).map(c => (
                    <a key={c.id} href={`?cours=${c.id}`} className="flex items-center justify-between gap-2 rounded-lg bg-white/5 px-3 py-1.5 text-sm hover:bg-white/15 [@media(max-height:520px)]:py-1">
                      <span className="font-medium">{c.titre}</span><span className="shrink-0 text-xs text-white/55">{c.n} diapos →</span>
                    </a>))}
                </div>
              </>}
            </div>))}
        </div>
        <Retravailler revoir={(ex, q) => REVOIR_2BAC[ex]?.[q] || []} nomExamen={ex => `Examen de ${ex === 'examen_chimie' ? 'chimie' : 'physique'}`}
          nomCours={c => SEANCES.find(x => x.id === c)?.nom || c} />
      </div>
    </div>
  );
}

function Cours({ id }: { id: string }) {
  const [cours, setCours] = useState<CourseDeck | null>(null);
  const [introuvable, setIntrouvable] = useState(false);
  /** où l'élève s'était arrêté dans ce cours (undefined : pas encore su) */
  const [reprise, setReprise] = useState<Reprise | null | undefined>(undefined);
  useTempsPasse(id, !!cours);
  useEffect(() => { coursActuel = id; }, [id]);
  useEffect(() => {
    const charger = source(id);
    if (!charger) { setIntrouvable(true); return; }
    const diapo = new URLSearchParams(window.location.search).get('diapo');
    // l'avancement de l'élève : le cours reprend à la dernière diapositive ouverte (sauf lien `?diapo=`)
    void Promise.all([charger(), diapo ? Promise.resolve(null) : maReprise(id)])
      .then(([d, r]) => { setReprise(r); setCours(aPartirDe(d, diapo)); }).catch(() => setIntrouvable(true));
  }, [id]);
  if (introuvable) return <Accueil />;
  if (!cours) return <div className="grid h-[100dvh] place-items-center bg-[#0a0a18] text-white/70">Chargement…</div>;
  const m = SEANCES.find(x => x.id === id)?.m;
  return (
    <div className="flex h-[100dvh] w-screen flex-col bg-[#0a0a18] p-1 text-white sm:p-2 [@media(max-height:520px)]:p-0.5">
      <div className="flex h-9 shrink-0 items-center gap-2 px-2 text-sm [@media(max-height:520px)]:h-7 [@media(max-height:520px)]:text-xs">
        <a href="./" className="shrink-0 rounded-lg px-2 py-1 text-white/70 hover:bg-white/10" title="Accueil">☰</a>
        <select value={id} onChange={e => { window.location.search = `cours=${e.target.value}`; }}
          className="min-w-0 flex-1 truncate rounded-lg border border-white/15 bg-[#121a33] px-2 py-1 text-white sm:max-w-md [@media(max-height:520px)]:py-0">
          {SEANCES.filter(x => source(x.id)).map(x => <option key={x.id} value={x.id}>{x.nom}</option>)}
        </select>
        {m && <a href={`?examen=${m.cle}`} className="shrink-0 rounded-lg border border-amber-300/50 px-2 py-1 text-amber-200 hover:bg-amber-300/10 [@media(max-height:520px)]:py-0">Examen</a>}
      </div>
      <div className="min-h-0 w-full flex-1 overflow-hidden rounded-2xl border border-white/10">
        <CoursePlayer deck={cours} language="mixed" mode="concentration" tuteur3D
          progress={reprise ? { current_slide_id: reprise.derniere, completed_slide_ids: reprise.vues, status: 'in_progress' } : null}
          onSlideChange={d => suivre({ type: 'diapo', cours: id, slide_id: d.id, titre: d.title, position: d.position, total: d.total })} />
      </div>
    </div>
  );
}

function Page() {
  const params = new URLSearchParams(window.location.search);
  const ex = MATIERES.find(m => m.cle === params.get('examen'));
  if (ex) {
    utiliserSujet({ sujet: ex.sujet as never, piste: cle => ex.voix[cle], suivi: true, matiere: 'physique', retour: '2ᵉ Bac PC', cle: `examen_${ex.cle}`, revoir: q => REVOIR_2BAC[`examen_${ex.cle}`]?.[q] || [] });
    return <Examen />;
  }
  const id = params.get('cours');
  return id ? <Cours id={id} /> : <Accueil />;
}

/** La fiche d'abord (une seule fois), comme au Tronc Commun. */
function Bac2PCF() {
  const [eleve, setEleve] = useState<Eleve | null>(() => eleveEnregistre());
  if (!eleve) return <Fiche onEntree={setEleve} entete="Moalim · 2ᵉ Bac PC BIOF · physique-chimie" prefixe="2BACPCF" fond="#101826" />;
  return <Page />;
}

createRoot(document.getElementById('root')!).render(<Bac2PCF />);
