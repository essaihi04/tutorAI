/**
 * La partie « Exercices » (22 novembre 2026) : les exercices d'application du premier semestre.
 * En haut, la progression de l'élève (cours + exercices) : note sur 20 par matière, points forts, lacunes, points perdus.
 * Puis des filtres (matière, cours, difficulté, statut, recherche) et des cartes animées : miniature de la figure,
 * difficulté, barre de progression et note de chaque exercice.
 */
import { useEffect, useMemo, useState, type CSSProperties } from 'react';
import { useNavigate } from 'react-router-dom';
import MoalimShell from '../components/MoalimShell';
import StudentNavigation from '../components/StudentNavigation';
import MobileBottomNav from '../components/MobileBottomNav';
import { FigureCahier } from '../components/course/FigureCahier';
import { lireProgresLocal, pts, type FicheIndex, type MatiereExercice } from '../components/exercice/types';

type FiltreMatiere = MatiereExercice | 'toutes';
type Statut = 'a_faire' | 'en_cours' | 'reussi' | 'moyen' | 'a_revoir';
interface ProgExo { faites: number; note: number | null; sur: number | null; pourcent: number | null }
interface Progression {
  exercices: Record<string, { statut: Statut; acquis: boolean; questions: number; exercice: ProgExo }>;
  cours: Record<string, { titre: string; matiere: string; pourcent: number | null; note20: number | null; cours_pourcent: number | null;
    exercices_pourcent: number | null; exercices_faits: number; exercices_total: number; lacunes_cours: string[] }>;
  matieres: Record<string, { nom: string; pourcent: number | null; note20: number | null; exercices_faits: number; exercices_total: number }>;
  global: { note20: number | null; pourcent: number | null; exercices_faits: number; exercices_reussis: number; exercices_total: number };
  forces: { cours: string; titre: string; pourcent: number | null }[];
  lacunes: { cours: string; titre: string; pourcent: number | null; competences: string[] }[];
  pertes_frequentes: { perte: string; fois: number }[];
}

const MATIERES: { cle: MatiereExercice; nom: string; icone: string; teinte: string }[] = [
  { cle: 'mathematiques', nom: 'Mathématiques', icone: '∑', teinte: 'from-sky-500/30 to-indigo-500/20' },
  { cle: 'physique', nom: 'Physique-chimie', icone: '⚛', teinte: 'from-amber-500/30 to-orange-500/20' },
  { cle: 'svt', nom: 'SVT', icone: '🧬', teinte: 'from-emerald-500/30 to-teal-500/20' },
];
const NIVEAUX = [
  { cle: 'facile', nom: 'Facile', aide: 'pour s’entraîner', barres: 1, couleur: 'border-emerald-600 bg-emerald-50 text-emerald-800' },
  { cle: 'moyen', nom: 'Moyen', aide: 'le niveau de l’examen', barres: 2, couleur: 'border-amber-600 bg-amber-50 text-amber-800' },
  { cle: 'difficile', nom: 'Supérieur', aide: 'plus exigeant que l’examen', barres: 3, couleur: 'border-rose-600 bg-rose-50 text-rose-800' },
];
const STATUTS: { cle: Statut | 'tous'; nom: string }[] = [
  { cle: 'tous', nom: 'Tous' }, { cle: 'a_faire', nom: 'À faire' }, { cle: 'en_cours', nom: 'En cours' },
  { cle: 'reussi', nom: 'Réussis' }, { cle: 'a_revoir', nom: 'À revoir' },
];
const NOM_STATUT: Record<Statut, string> = { a_faire: 'À faire', en_cours: 'En cours', reussi: 'Réussi', moyen: 'Moyen', a_revoir: 'À revoir' };
const PAGE = 12;
const CLE_FILTRES = 'moalim:exercices:filtres';

const couleurNote = (p: number | null | undefined) => p == null ? '#94a3b8' : p >= 0.75 ? '#10b981' : p >= 0.5 ? '#f59e0b' : '#f43f5e';
const jeton = () => { try { return localStorage.getItem('token') || ''; } catch { return ''; } };

/** Anneau de progression, rempli en douceur à l'apparition. */
function Anneau({ p, taille = 64, epais = 7, children }: { p: number | null | undefined; taille?: number; epais?: number; children?: React.ReactNode }) {
  const [vu, setVu] = useState(0);
  useEffect(() => { const t = setTimeout(() => setVu(p ?? 0), 60); return () => clearTimeout(t); }, [p]);
  const r = (taille - epais) / 2, c = 2 * Math.PI * r;
  return (
    <div className="relative shrink-0" style={{ width: taille, height: taille }}>
      <svg width={taille} height={taille} className="-rotate-90">
        <circle cx={taille / 2} cy={taille / 2} r={r} fill="none" stroke="rgba(255,255,255,.12)" strokeWidth={epais} />
        <circle cx={taille / 2} cy={taille / 2} r={r} fill="none" stroke={couleurNote(p)} strokeWidth={epais} strokeLinecap="round"
          strokeDasharray={c} strokeDashoffset={c * (1 - Math.min(1, Math.max(0, vu)))} style={{ transition: 'stroke-dashoffset 1.1s ease-out' }} />
      </svg>
      <div className="absolute inset-0 grid place-items-center text-center leading-tight">{children}</div>
    </div>
  );
}

function Barres({ n }: { n: number }) {
  return (
    <span className="inline-flex items-end gap-[2px]" aria-hidden="true">
      {[1, 2, 3].map(i => <span key={i} className={`w-[4px] rounded-sm ${i <= n ? 'bg-current' : 'bg-current/25 opacity-30'}`} style={{ height: 4 + i * 3 }} />)}
    </span>
  );
}

export default function ExercicesHub() {
  const navigate = useNavigate();
  const [fiches, setFiches] = useState<FicheIndex[] | null>(null);
  const [prog, setProg] = useState<Progression | null>(null);
  const local = useMemo(() => lireProgresLocal(), []);
  const init = useMemo(() => { try { return JSON.parse(localStorage.getItem(CLE_FILTRES) || '{}'); } catch { return {}; } }, []);
  const [matiere, setMatiere] = useState<FiltreMatiere>(init.matiere || 'mathematiques');
  const [cours, setCours] = useState<string>(init.cours || '');
  const [niveau, setNiveau] = useState<string>(init.niveau || '');
  const [statut, setStatut] = useState<Statut | 'tous'>(init.statut || 'tous');
  const [cherche, setCherche] = useState('');
  const [page, setPage] = useState(1);

  useEffect(() => {
    fetch('/media/exercices/index.json').then(r => r.json()).then((d: { exercices: FicheIndex[] }) => setFiches(d.exercices)).catch(() => setFiches([]));
    fetch('/api/v1/exercices/progression', { headers: { Authorization: `Bearer ${jeton()}` } })
      .then(r => r.ok ? r.json() : null).then(setProg).catch(() => setProg(null));
  }, []);
  useEffect(() => {
    try { localStorage.setItem(CLE_FILTRES, JSON.stringify({ matiere, cours, niveau, statut })); } catch { /* stockage refusé */ }
    setPage(1);
  }, [matiere, cours, niveau, statut, cherche]);

  // l'état de chaque exercice : celui du serveur, sinon celui gardé dans le navigateur
  const etatDe = (f: FicheIndex): { statut: Statut; faites: number; note: number | null; sur: number | null; p: number | null; acquis: boolean } => {
    const s = prog?.exercices?.[f.id];
    // la couleur suit la réussite sur les questions déjà faites (la note est sur tout l'exercice)
    const reussite = (note: number | null, sur: number | null, faites: number) => note != null && sur ? note / (sur * Math.min(1, faites / (f.questions || 1))) : null;
    if (s && s.exercice.faites) return { statut: s.statut, faites: s.exercice.faites, note: s.exercice.note, sur: s.exercice.sur, p: reussite(s.exercice.note, s.exercice.sur, s.exercice.faites), acquis: s.acquis };
    const l = local[f.id];
    if (l && l.faites) {
      const p = l.sur ? l.note / l.sur : null;
      const st: Statut = l.faites < f.questions ? 'en_cours' : (p ?? 0) >= 0.75 ? 'reussi' : (p ?? 0) < 0.5 ? 'a_revoir' : 'moyen';
      return { statut: st, faites: l.faites, note: l.note, sur: l.sur, p: reussite(l.note, l.sur, l.faites), acquis: false };
    }
    return { statut: 'a_faire', faites: 0, note: null, sur: f.bareme ?? null, p: null, acquis: false };
  };

  const coursDeLaMatiere = useMemo(() => {
    const m = new Map<string, { titre: string; n: number }>();
    (fiches || []).filter(f => matiere === 'toutes' || f.matiere === matiere).forEach(f => {
      const x = m.get(f.cours) || { titre: f.cours_titre || f.cours, n: 0 }; x.n++; m.set(f.cours, x);
    });
    return [...m.entries()];
  }, [fiches, matiere]);

  const liste = useMemo(() => {
    const q = cherche.trim().toLowerCase();
    return (fiches || []).filter(f => (matiere === 'toutes' || f.matiere === matiere) && (!cours || f.cours === cours) && (!niveau || f.niveau === niveau)
      && (statut === 'tous' || etatDe(f).statut === statut || (statut === 'a_revoir' && etatDe(f).statut === 'moyen'))
      && (!q || `${f.titre} ${f.cours_titre || ''}`.toLowerCase().includes(q)));
  }, [fiches, matiere, cours, niveau, statut, cherche, prog]); // eslint-disable-line react-hooks/exhaustive-deps

  const g = prog?.global;
  const puce = (actif: boolean) => `rounded-full border px-3 py-1 text-xs transition ${actif ? 'border-amber-200 bg-amber-200 text-slate-900' : 'border-white/15 bg-white/5 text-white/75 hover:bg-white/10'}`;

  return (
    <MoalimShell>
      <StudentNavigation active="exercices" />
      <style>{`@keyframes exoMonte{from{opacity:0;transform:translateY(14px) scale(.98)}to{opacity:1;transform:none}}
        .exo-carte{animation:exoMonte .45s ease-out both}`}</style>
      <main className="mx-auto min-h-[calc(100vh-4rem)] max-w-7xl px-4 pb-28 pt-6 sm:px-6 lg:px-8 lg:pb-12 lg:pt-8">
        <header className="flex flex-wrap items-end justify-between gap-3">
          <div>
            <h1 className="text-2xl font-bold text-white">Exercices</h1>
            <p className="mt-1 max-w-2xl text-sm text-white/60">Des exercices comme à l’examen, sur les cours du premier semestre : le tuteur t’aide si tu le demandes,
              note chaque réponse et te montre où tu perds des points. Les sujets du national sont dans la partie Examen.</p>
          </div>
        </header>

        {/* Ma progression : cours + exercices */}
        <section className="exo-carte mt-5 grid gap-3 lg:grid-cols-[auto_1fr_1fr]" style={{ animationDelay: '40ms' }}>
          <div className="flex items-center gap-4 rounded-2xl border border-white/10 bg-white/[0.04] p-4">
            <Anneau p={g?.pourcent} taille={92} epais={9}>
              <div><p className="text-xl font-bold text-white">{g?.note20 != null ? pts(g.note20) : '—'}</p><p className="text-[10px] text-white/55">/ 20</p></div>
            </Anneau>
            <div className="text-sm text-white/75">
              <p className="font-semibold text-white">Ma note générale</p>
              <p className="text-xs text-white/55">cours et exercices réunis</p>
              <p className="mt-2">{g ? `${g.exercices_faits} / ${g.exercices_total} exercices faits` : 'Connecte-toi pour suivre ta progression.'}</p>
              {g && <p className="text-emerald-300">{g.exercices_reussis} réussi{g.exercices_reussis > 1 ? 's' : ''}</p>}
            </div>
          </div>
          <div className="grid grid-cols-3 gap-2">
            {MATIERES.map(m => {
              const s = prog?.matieres?.[m.cle];
              return (
                <button key={m.cle} onClick={() => { setMatiere(m.cle); setCours(''); }}
                  className={`flex flex-col items-center gap-1 rounded-2xl border bg-gradient-to-br p-3 text-center transition hover:-translate-y-0.5 ${m.teinte} ${matiere === m.cle ? 'border-amber-200/70' : 'border-white/10'}`}>
                  <Anneau p={s?.pourcent} taille={58} epais={6}><span className="text-sm font-bold text-white">{s?.note20 != null ? pts(s.note20) : m.icone}</span></Anneau>
                  <span className="text-xs font-semibold text-white">{m.nom}</span>
                  <span className="text-[11px] text-white/60">{s ? `${s.exercices_faits} / ${s.exercices_total} exercices` : ''}</span>
                </button>);
            })}
          </div>
          <div className="grid gap-2 rounded-2xl border border-white/10 bg-white/[0.04] p-3 text-xs text-white/80 sm:grid-cols-2">
            <div>
              <p className="mb-1 font-semibold text-emerald-300">💪 Points forts</p>
              {prog?.forces?.length ? prog.forces.map(x => <p key={x.cours} className="truncate">• {x.titre} <span className="text-white/50">{Math.round((x.pourcent || 0) * 100)} %</span></p>)
                : <p className="text-white/45">Fais des exercices pour les voir apparaître.</p>}
            </div>
            <div>
              <p className="mb-1 font-semibold text-rose-300">🎯 À retravailler</p>
              {prog?.lacunes?.length ? prog.lacunes.map(x => (
                <button key={x.cours} onClick={() => { setMatiere(prog.cours[x.cours]?.matiere as MatiereExercice || matiere); setCours(x.cours); }} className="block w-full truncate text-left hover:text-white">
                  • {x.titre} <span className="text-white/50">{Math.round((x.pourcent || 0) * 100)} %</span></button>))
                : <p className="text-white/45">Rien à signaler pour l’instant.</p>}
              {!!prog?.pertes_frequentes?.length && (<>
                <p className="mb-1 mt-2 font-semibold text-amber-200">Où je perds des points</p>
                {prog.pertes_frequentes.slice(0, 3).map(x => <p key={x.perte} className="line-clamp-1">• {x.perte}{x.fois > 1 ? ` (×${x.fois})` : ''}</p>)}
              </>)}
            </div>
          </div>
        </section>

        {/* Filtres */}
        <section className="exo-carte mt-5 space-y-2 rounded-2xl border border-white/10 bg-white/[0.03] p-3" style={{ animationDelay: '90ms' }}>
          <div className="flex flex-wrap items-center gap-2">
            <button onClick={() => { setMatiere('toutes'); setCours(''); }} className={puce(matiere === 'toutes')}>Toutes</button>
            {MATIERES.map(m => <button key={m.cle} onClick={() => { setMatiere(m.cle); setCours(''); }} className={puce(matiere === m.cle)}>{m.icone} {m.nom}</button>)}
            <input value={cherche} onChange={e => setCherche(e.target.value)} placeholder="🔍 Chercher un exercice…"
              className="ml-auto min-w-[180px] flex-1 rounded-full border border-white/15 bg-black/30 px-3 py-1.5 text-sm text-white outline-none placeholder:text-white/40 focus:border-amber-200/60 sm:flex-none" />
          </div>
          <div className="flex flex-wrap items-center gap-2">
            <select value={cours} onChange={e => setCours(e.target.value)} className="max-w-full rounded-full border border-white/15 bg-[#14142a] px-3 py-1.5 text-xs text-white">
              <option value="">Tous les cours</option>
              {coursDeLaMatiere.map(([id, c]) => {
                const n = prog?.cours?.[id]?.note20;
                return <option key={id} value={id}>{c.titre}{n != null ? ` — ${pts(n)}/20` : ''}</option>;
              })}
            </select>
            <span className="mx-1 h-4 w-px bg-white/15" />
            <button onClick={() => setNiveau('')} className={puce(!niveau)}>Toute difficulté</button>
            {NIVEAUX.map(n => <button key={n.cle} onClick={() => setNiveau(n.cle)} className={puce(niveau === n.cle)} title={n.aide}><Barres n={n.barres} /> {n.nom}</button>)}
            <span className="mx-1 h-4 w-px bg-white/15" />
            {STATUTS.map(s => <button key={s.cle} onClick={() => setStatut(s.cle)} className={puce(statut === s.cle)}>{s.nom}</button>)}
          </div>
          {cours && prog?.cours?.[cours] && (() => {
            const c = prog.cours[cours];
            return (
              <div className="flex flex-wrap items-center gap-3 rounded-xl bg-white/5 p-2 text-xs text-white/80">
                <Anneau p={c.pourcent} taille={44} epais={5}><span className="text-[11px] font-bold text-white">{c.note20 != null ? pts(c.note20) : '—'}</span></Anneau>
                <span><b className="text-white">{c.titre}</b> — note du cours : {c.note20 != null ? `${pts(c.note20)} / 20` : 'pas encore'}</span>
                <span>Cours : {c.cours_pourcent != null ? `${Math.round(c.cours_pourcent * 100)} %` : '—'}</span>
                <span>Exercices : {c.exercices_pourcent != null ? `${Math.round(c.exercices_pourcent * 100)} %` : '—'} ({c.exercices_faits}/{c.exercices_total})</span>
                {!!c.lacunes_cours.length && <span className="text-rose-300">À revoir : {c.lacunes_cours.slice(0, 3).join(', ')}</span>}
              </div>);
          })()}
        </section>

        {/* Les cartes */}
        {fiches === null ? <p className="mt-8 text-white/60">Chargement…</p> : (<>
          <p className="mt-4 text-xs text-white/50">{liste.length} exercice{liste.length > 1 ? 's' : ''}</p>
          <div className="mt-2 grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {liste.slice(0, page * PAGE).map((f, i) => {
              const e = etatDe(f);
              const n = NIVEAUX.find(x => x.cle === f.niveau);
              const m = MATIERES.find(x => x.cle === f.matiere);
              const avance = f.questions ? e.faites / f.questions : 0;
              const style: CSSProperties = { animationDelay: `${Math.min(i % PAGE, 11) * 45}ms` };
              return (
                <button key={f.id} onClick={() => navigate(`/exercices/${f.id}`)} style={style}
                  className="exo-carte group flex flex-col overflow-hidden rounded-xl bg-white text-left text-black shadow-lg ring-1 ring-black/10 transition duration-200 hover:-translate-y-1 hover:shadow-2xl hover:ring-2 hover:ring-amber-400">
                  {/* miniature : la figure de l'énoncé, dessinée en noir sur la feuille */}
                  <div className={`relative h-32 w-full overflow-hidden border-b border-slate-200 ${f.figure ? 'bg-white' : `bg-gradient-to-br ${m?.teinte || ''}`}`}>
                    {f.figure
                      ? <div className="pointer-events-none mx-auto w-[86%] origin-top scale-[0.62] transition duration-300 group-hover:scale-[0.66]" style={{ filter: 'invert(1) hue-rotate(180deg)' }}><FigureCahier fig={{ ...f.figure, titre: undefined, legende: undefined }} compact /></div>
                      : <div className="grid h-full place-items-center text-5xl opacity-70">{m?.icone}</div>}
                    <span className={`absolute left-2 top-2 inline-flex items-center gap-1 rounded-full border px-2 py-0.5 text-[11px] font-semibold ${n?.couleur || ''}`}><Barres n={n?.barres || 1} /> {n?.nom}</span>
                    {e.statut !== 'a_faire' && <span className={`absolute right-2 top-2 rounded-full px-2 py-0.5 text-[11px] font-semibold text-white`} style={{ background: couleurNote(e.p) }}>{e.acquis ? '✔ Acquis' : NOM_STATUT[e.statut]}</span>}
                  </div>
                  <div className="flex flex-1 flex-col p-3">
                    <p className="text-[11px] uppercase tracking-wide text-slate-500">{m?.nom} · {f.cours_titre}</p>
                    <p className="mt-0.5 line-clamp-2 font-semibold leading-snug" style={{ fontFamily: "'Times New Roman', Georgia, serif" }}>{f.titre}</p>
                    <p className="mt-1 text-xs text-slate-500">{f.duree_min ? `~${f.duree_min} min · ` : ''}{f.questions} questions · {pts(f.bareme || 0)} pts</p>
                    <div className="mt-auto pt-3">
                      <div className="flex items-center justify-between text-[11px] text-slate-600">
                        <span>{e.faites} / {f.questions} questions</span>
                        <span className="font-semibold" style={{ color: couleurNote(e.p) }}>{e.note != null ? `${pts(e.note)} / ${pts(e.sur || f.bareme || 0)}` : ''}</span>
                      </div>
                      <div className="mt-1 h-2 w-full overflow-hidden rounded-full bg-slate-200">
                        <div className="h-full rounded-full transition-[width] duration-700" style={{ width: `${Math.round(avance * 100)}%`, background: couleurNote(e.p ?? (e.faites ? 0.6 : null)) }} />
                      </div>
                    </div>
                  </div>
                </button>);
            })}
          </div>
          {liste.length === 0 && <p className="mt-6 text-sm text-white/60">Aucun exercice avec ces filtres.</p>}
          {liste.length > page * PAGE && (
            <div className="mt-5 text-center">
              <button onClick={() => setPage(p => p + 1)} className="rounded-full border border-white/20 bg-white/5 px-5 py-2 text-sm text-white hover:bg-white/10">
                Afficher plus ({liste.length - page * PAGE} restant{liste.length - page * PAGE > 1 ? 's' : ''})</button>
            </div>)}
        </>)}
      </main>
      <MobileBottomNav active="exercices" />
    </MoalimShell>
  );
}
