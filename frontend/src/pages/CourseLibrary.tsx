import { useEffect, useMemo, useState, type ReactNode } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  BookOpen,
  CheckCircle2,
  Clock3,
  Layers3,
  MessageCircle,
  Play,
  RefreshCw,
  Search,
  X,
} from 'lucide-react';
import MoalimShell from '../components/MoalimShell';
import StudentNavigation from '../components/StudentNavigation';
import MobileBottomNav from '../components/MobileBottomNav';
import {
  getCourseCatalog,
  type CourseCatalog,
  type CourseCatalogCourse,
  type CourseCatalogSubject,
} from '../services/api';

// Bibliothèque des cours (20/11/2026) : des cartes avec image, un filtre par matière, une recherche et un filtre
// d'avancement. Une couleur par matière, la même partout sur la page (pastille, badge, barre d'avancement).

const EMPTY_CATALOG: CourseCatalog = { subjects: [], total_courses: 0 };

type Teinte = { point: string; badge: string; barre: string; fond: string; actif: string };

const TEINTES: Record<string, Teinte> = {
  physique: {
    point: 'bg-sky-400', badge: 'bg-sky-400/90 text-sky-950', barre: 'bg-sky-400',
    fond: 'from-sky-600/60 via-indigo-700/40 to-[#08081c]', actif: 'border-sky-300/60 bg-sky-400/15 text-white',
  },
  chimie: {
    point: 'bg-teal-400', badge: 'bg-teal-300/90 text-teal-950', barre: 'bg-teal-400',
    fond: 'from-teal-600/60 via-cyan-800/40 to-[#08081c]', actif: 'border-teal-300/60 bg-teal-400/15 text-white',
  },
  svt: {
    point: 'bg-lime-400', badge: 'bg-lime-300/90 text-lime-950', barre: 'bg-lime-400',
    fond: 'from-lime-600/55 via-emerald-800/40 to-[#08081c]', actif: 'border-lime-300/60 bg-lime-400/15 text-white',
  },
  maths: {
    point: 'bg-amber-400', badge: 'bg-amber-300/90 text-amber-950', barre: 'bg-amber-400',
    fond: 'from-amber-500/55 via-orange-800/40 to-[#08081c]', actif: 'border-amber-300/60 bg-amber-400/15 text-white',
  },
  autre: {
    point: 'bg-violet-400', badge: 'bg-violet-300/90 text-violet-950', barre: 'bg-violet-400',
    fond: 'from-violet-600/55 via-indigo-800/40 to-[#08081c]', actif: 'border-violet-300/60 bg-violet-400/15 text-white',
  },
};

const sansAccents = (texte: string) =>
  texte.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();

const cleMatiere = (nom: string) => {
  const n = sansAccents(nom);
  if (n.startsWith('phys')) return 'physique';
  if (n.startsWith('chim')) return 'chimie';
  if (n.startsWith('scien') || n.includes('svt') || n.includes('vie')) return 'svt';
  if (n.startsWith('math')) return 'maths';
  return 'autre';
};

const nomCourt = (nom: string) => {
  const cle = cleMatiere(nom);
  if (cle === 'svt') return 'SVT';
  if (cle === 'maths') return 'Maths';
  return nom;
};

// Numéro du chapitre lu dans l'identifiant du cours (phys_ch12_…) : il sert à trier les cartes dans l'ordre du programme.
const numeroChapitre = (course: CourseCatalogCourse) => {
  const m = /_ch(\d+)/.exec(course.stable_id || course.deck_id || '');
  return m ? Number(m[1]) : 999;
};

const formatDuration = (minutes: number) => {
  if (!minutes) return '';
  if (minutes < 60) return `${minutes} min`;
  const hours = Math.floor(minutes / 60);
  const remainder = minutes % 60;
  return remainder ? `${hours} h ${String(remainder).padStart(2, '0')}` : `${hours} h`;
};

type Avancement = 'tous' | 'en_cours' | 'termine' | 'a_faire';
const AVANCEMENTS: { id: Avancement; label: string }[] = [
  { id: 'tous', label: 'Tous' },
  { id: 'en_cours', label: 'En cours' },
  { id: 'a_faire', label: 'À commencer' },
  { id: 'termine', label: 'Terminés' },
];

type Carte = { course: CourseCatalogCourse; subject: CourseCatalogSubject; teinte: Teinte; rang: number };

// Le résumé du catalogue commence par une formule interne (« Le cours au tableau, en mode concentration : ») :
// l'élève ne lit que la suite, avec une majuscule.
const resumeEleve = (texte: string) => {
  const t = (texte || '').replace(/^.*?mode concentration\s*:\s*/i, '').trim();
  return t ? t.charAt(0).toUpperCase() + t.slice(1) : '';
};

export default function CourseLibrary() {
  const navigate = useNavigate();
  const [catalog, setCatalog] = useState<CourseCatalog>(EMPTY_CATALOG);
  const [matiere, setMatiere] = useState('toutes');
  const [avancement, setAvancement] = useState<Avancement>('tous');
  const [recherche, setRecherche] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadCatalog = () => {
    setLoading(true);
    setError(null);
    getCourseCatalog()
      .then(({ data }) => setCatalog(data))
      .catch(() => setError('Impossible de charger les cours pour le moment.'))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    let cancelled = false;
    getCourseCatalog()
      .then(({ data }) => { if (!cancelled) setCatalog(data); })
      .catch(() => { if (!cancelled) setError('Impossible de charger les cours pour le moment.'); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, []);

  const matieres = useMemo(
    () => catalog.subjects.filter((subject) => subject.courses.length > 0),
    [catalog.subjects],
  );

  const toutes: Carte[] = useMemo(
    () => matieres.flatMap((subject) => {
      const teinte = TEINTES[cleMatiere(subject.name_fr)];
      return [...subject.courses]
        .sort((a, b) => numeroChapitre(a) - numeroChapitre(b))
        .map((course, i) => ({ course, subject, teinte, rang: i + 1 }));
    }),
    [matieres],
  );

  const enCours = useMemo(
    () => toutes.filter(({ course }) => course.progress_status === 'in_progress'),
    [toutes],
  );

  const visibles = useMemo(() => {
    const q = sansAccents(recherche.trim());
    return toutes.filter(({ course, subject }) => {
      if (matiere !== 'toutes' && subject.id !== matiere) return false;
      if (avancement === 'en_cours' && course.progress_status !== 'in_progress') return false;
      if (avancement === 'termine' && course.progress_status !== 'completed') return false;
      if (avancement === 'a_faire' && course.progress_status !== 'not_started') return false;
      if (!q) return true;
      const texte = sansAccents([
        course.title, course.chapter_title, course.lesson_title, subject.name_fr, ...(course.essential_topics || []),
      ].join(' '));
      return q.split(/\s+/).every((mot) => texte.includes(mot));
    });
  }, [toutes, matiere, avancement, recherche]);

  const totalMinutes = toutes.reduce((somme, { course }) => somme + (course.estimated_minutes || 0), 0);
  const termines = toutes.filter(({ course }) => course.progress_status === 'completed').length;
  const filtresActifs = matiere !== 'toutes' || avancement !== 'tous' || recherche.trim() !== '';

  const openCourse = (course: CourseCatalogCourse) => {
    navigate(
      `/session/${encodeURIComponent(course.chapter_id)}/${encodeURIComponent(course.lesson_id)}`,
      { state: { launchedFromLibrary: true, deckTitle: course.title } },
    );
  };

  const askTutorToOpen = (course: CourseCatalogCourse) => {
    navigate('/tutor', { state: { courseRequest: course.tutor_request } });
  };

  const reinitialiser = () => {
    setMatiere('toutes');
    setAvancement('tous');
    setRecherche('');
  };

  return (
    <MoalimShell>
      <StudentNavigation active="courses" />
      <main className="mx-auto min-h-[calc(100vh-4rem)] max-w-7xl px-4 pb-28 pt-6 sm:px-6 lg:px-8 lg:pb-12 lg:pt-8">
        {/* En-tête : titre et trois chiffres, rien de plus */}
        <header className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <p className="text-xs font-bold uppercase tracking-[0.18em] text-cyan-300/70">2ᵉ Bac · Sciences physiques BIOF</p>
            <h1 className="mt-1 text-2xl font-black tracking-tight text-white sm:text-3xl">Bibliothèque des cours</h1>
            <p className="mt-1 text-sm text-white/50">Chaque cours au tableau, avec ses simulations, ses exercices et les sujets du national.</p>
          </div>
          {!loading && !error && toutes.length > 0 && (
            <dl className="flex gap-2 text-center">
              <Chiffre valeur={String(toutes.length)} libelle="cours" />
              <Chiffre valeur={`${Math.round(totalMinutes / 60)} h`} libelle="de contenu" />
              <Chiffre valeur={`${termines}/${toutes.length}`} libelle="terminés" />
            </dl>
          )}
        </header>

        {loading ? (
          <LibrarySkeleton />
        ) : error ? (
          <section className="mt-8 flex flex-col items-center rounded-3xl border border-rose-400/15 bg-rose-500/[0.05] px-5 py-12 text-center">
            <p className="text-sm font-bold text-rose-200">{error}</p>
            <button onClick={loadCatalog} className="mt-4 inline-flex items-center gap-2 rounded-xl bg-white px-4 py-2 text-xs font-black text-indigo-950">
              <RefreshCw className="h-3.5 w-3.5" /> Réessayer
            </button>
          </section>
        ) : toutes.length === 0 ? (
          <EmptyLibrary />
        ) : (
          <>
            {/* Reprendre : les cours commencés, en premier */}
            {enCours.length > 0 && (
              <section className="mt-6">
                <h2 className="mb-3 text-sm font-black text-white/80">Reprendre où tu t'es arrêté</h2>
                <div className="flex gap-3 overflow-x-auto pb-1 [scrollbar-width:thin]">
                  {enCours.map(({ course, subject, teinte }) => (
                    <button
                      key={course.stable_id}
                      onClick={() => openCourse(course)}
                      className="group flex w-72 shrink-0 items-center gap-3 rounded-2xl border border-white/[0.08] bg-white/[0.04] p-2.5 text-left transition hover:border-white/20 hover:bg-white/[0.07]"
                    >
                      <Couverture course={course} teinte={teinte} className="h-16 w-24 shrink-0 rounded-xl" />
                      <span className="min-w-0 flex-1">
                        <span className="block text-[11px] font-bold text-white/45">{nomCourt(subject.name_fr)}</span>
                        <span className="block truncate text-sm font-black text-white">{course.title}</span>
                        <BarreAvancement pourcent={course.progress_percent} teinte={teinte} />
                      </span>
                      <Play className="h-4 w-4 shrink-0 fill-current text-white/40 transition group-hover:text-white" />
                    </button>
                  ))}
                </div>
              </section>
            )}

            {/* Barre de filtres : matières, recherche, avancement */}
            <section className="sticky top-0 z-20 -mx-4 mt-6 border-b border-white/[0.06] bg-[#08081c]/90 px-4 py-3 backdrop-blur-xl sm:-mx-6 sm:px-6 lg:-mx-8 lg:px-8">
              <div className="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
                <div className="-mx-1 flex gap-2 overflow-x-auto px-1 pb-0.5 [scrollbar-width:none]" role="tablist" aria-label="Filtrer par matière">
                  <Puce
                    actif={matiere === 'toutes'}
                    onClick={() => setMatiere('toutes')}
                    classeActive="border-white/40 bg-white text-indigo-950"
                    nombre={toutes.length}
                  >
                    Toutes
                  </Puce>
                  {matieres.map((subject) => {
                    const teinte = TEINTES[cleMatiere(subject.name_fr)];
                    return (
                      <Puce
                        key={subject.id}
                        actif={matiere === subject.id}
                        onClick={() => setMatiere(subject.id)}
                        classeActive={teinte.actif}
                        nombre={subject.courses.length}
                      >
                        <span className={`h-2 w-2 rounded-full ${teinte.point}`} />
                        {nomCourt(subject.name_fr)}
                      </Puce>
                    );
                  })}
                </div>
                <div className="flex gap-2">
                  <label className="relative flex-1 lg:w-64 lg:flex-none">
                    <span className="sr-only">Rechercher un cours</span>
                    <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-white/35" />
                    <input
                      value={recherche}
                      onChange={(e) => setRecherche(e.target.value)}
                      placeholder="Rechercher : dipôle, ADN, limites…"
                      className="h-10 w-full rounded-xl border border-white/10 bg-white/[0.05] pl-9 pr-8 text-sm text-white placeholder:text-white/30 focus:border-cyan-300/50 focus:outline-none"
                    />
                    {recherche && (
                      <button onClick={() => setRecherche('')} className="absolute right-2 top-1/2 -translate-y-1/2 rounded-md p-1 text-white/40 hover:text-white" aria-label="Effacer la recherche">
                        <X className="h-3.5 w-3.5" />
                      </button>
                    )}
                  </label>
                  <select
                    value={avancement}
                    onChange={(e) => setAvancement(e.target.value as Avancement)}
                    className="h-10 rounded-xl border border-white/10 bg-[#11112a] px-3 text-sm font-semibold text-white/80 focus:border-cyan-300/50 focus:outline-none"
                    aria-label="Filtrer par avancement"
                  >
                    {AVANCEMENTS.map((a) => <option key={a.id} value={a.id}>{a.label}</option>)}
                  </select>
                </div>
              </div>
            </section>

            {/* Les cartes */}
            <section className="mt-5">
              <p className="mb-3 text-xs font-semibold text-white/40">
                {visibles.length} cours{filtresActifs && (
                  <button onClick={reinitialiser} className="ml-2 font-bold text-cyan-300 hover:text-cyan-200">Tout afficher</button>
                )}
              </p>
              {visibles.length > 0 ? (
                <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
                  {visibles.map(({ course, subject, teinte, rang }) => (
                    <CourseCard
                      key={course.stable_id}
                      rang={rang}
                      course={course}
                      subject={subject}
                      teinte={teinte}
                      onOpen={() => openCourse(course)}
                      onAskTutor={() => askTutorToOpen(course)}
                    />
                  ))}
                </div>
              ) : (
                <div className="rounded-3xl border border-dashed border-white/10 bg-white/[0.025] px-6 py-12 text-center">
                  <Search className="mx-auto h-7 w-7 text-white/20" />
                  <p className="mt-3 text-sm font-bold text-white/65">Aucun cours ne correspond</p>
                  <button onClick={reinitialiser} className="mt-3 text-xs font-bold text-cyan-300">Effacer les filtres</button>
                </div>
              )}
            </section>
          </>
        )}
      </main>
      <MobileBottomNav active="courses" />
    </MoalimShell>
  );
}

function Chiffre({ valeur, libelle }: { valeur: string; libelle: string }) {
  return (
    <div className="min-w-[78px] rounded-2xl border border-white/[0.07] bg-white/[0.035] px-3 py-2">
      <dd className="text-lg font-black text-white">{valeur}</dd>
      <dt className="text-[11px] font-semibold text-white/40">{libelle}</dt>
    </div>
  );
}

function Puce({
  actif, onClick, classeActive, nombre, children,
}: {
  actif: boolean; onClick: () => void; classeActive: string; nombre: number; children: ReactNode;
}) {
  return (
    <button
      role="tab"
      aria-selected={actif}
      onClick={onClick}
      className={`inline-flex h-10 shrink-0 items-center gap-2 rounded-xl border px-3.5 text-sm font-bold transition ${
        actif ? classeActive : 'border-white/10 bg-white/[0.03] text-white/60 hover:border-white/20 hover:text-white'
      }`}
    >
      {children}
      <span className={`rounded-md px-1.5 text-[11px] ${actif ? 'bg-black/15' : 'bg-white/[0.07] text-white/45'}`}>{nombre}</span>
    </button>
  );
}

function Couverture({ course, teinte, className = '' }: { course: CourseCatalogCourse; teinte: Teinte; className?: string }) {
  if (course.cover_image) {
    return <img src={course.cover_image} alt={course.cover_alt} loading="lazy" className={`object-cover ${className}`} />;
  }
  return (
    <div className={`relative overflow-hidden bg-gradient-to-br ${teinte.fond} ${className}`}>
      <BookOpen className="absolute bottom-2 right-2 h-1/2 w-1/2 text-white/10" />
    </div>
  );
}

function BarreAvancement({ pourcent, teinte }: { pourcent: number; teinte: Teinte }) {
  return (
    <span className="mt-1.5 flex items-center gap-2">
      <span className="h-1.5 flex-1 overflow-hidden rounded-full bg-white/10">
        <span className={`block h-full rounded-full ${teinte.barre}`} style={{ width: `${Math.max(4, pourcent)}%` }} />
      </span>
      <span className="text-[11px] font-bold text-white/50">{pourcent}%</span>
    </span>
  );
}

function CourseCard({
  course, subject, teinte, rang, onOpen, onAskTutor,
}: {
  rang: number;
  course: CourseCatalogCourse;
  subject: CourseCatalogSubject;
  teinte: Teinte;
  onOpen: () => void;
  onAskTutor: () => void;
}) {
  const completed = course.progress_status === 'completed';
  const inProgress = course.progress_status === 'in_progress';
  return (
    <article className="group relative flex flex-col overflow-hidden rounded-2xl border border-white/[0.08] bg-[#0e0e26] shadow-lg shadow-black/20 transition duration-200 hover:-translate-y-1 hover:border-white/20 hover:shadow-2xl hover:shadow-black/40">
      <button onClick={onOpen} className="relative block aspect-[16/10] w-full overflow-hidden text-left" aria-label={`Ouvrir le cours ${course.title}`}>
        <Couverture course={course} teinte={teinte} className="h-full w-full transition duration-500 group-hover:scale-[1.04]" />
        <div className="absolute inset-0 bg-gradient-to-t from-[#0e0e26] via-transparent to-transparent" />
        <span className={`absolute left-3 top-3 rounded-lg px-2 py-0.5 text-[11px] font-black ${teinte.badge}`}>
          {nomCourt(subject.name_fr)}
        </span>
        {completed && (
          <span className="absolute right-3 top-3 inline-flex items-center gap-1 rounded-lg bg-emerald-400 px-2 py-0.5 text-[11px] font-black text-emerald-950">
            <CheckCircle2 className="h-3 w-3" /> Terminé
          </span>
        )}
        <span className="absolute inset-0 flex items-center justify-center opacity-0 transition group-hover:opacity-100">
          <span className="flex h-12 w-12 items-center justify-center rounded-full bg-white/95 text-indigo-950 shadow-xl">
            <Play className="ml-0.5 h-5 w-5 fill-current" />
          </span>
        </span>
      </button>

      <div className="flex flex-1 flex-col p-4 pt-3">
        <p className="text-[11px] font-bold uppercase tracking-wider text-white/40">Chapitre {rang}</p>
        <h3 className="mt-1 line-clamp-2 text-[15px] font-black leading-snug text-white">{course.title}</h3>
        <p className="mt-1.5 line-clamp-2 text-xs leading-5 text-white/45">{resumeEleve(course.summary)}</p>

        <div className="mt-auto pt-3">
          {inProgress ? (
            <BarreAvancement pourcent={course.progress_percent} teinte={teinte} />
          ) : (
            <div className="flex items-center gap-3 text-[11px] font-semibold text-white/40">
              {course.estimated_minutes > 0 && (
                <span className="inline-flex items-center gap-1"><Clock3 className="h-3.5 w-3.5" /> {formatDuration(course.estimated_minutes)}</span>
              )}
              {course.slide_count > 0 && (
                <span className="inline-flex items-center gap-1"><Layers3 className="h-3.5 w-3.5" /> {course.slide_count} étapes</span>
              )}
            </div>
          )}
          <div className="mt-3 flex gap-2">
            <button onClick={onOpen} className="inline-flex h-9 flex-1 items-center justify-center gap-1.5 rounded-xl bg-white text-xs font-black text-indigo-950 transition hover:bg-cyan-50">
              <Play className="h-3.5 w-3.5 fill-current" /> {inProgress ? 'Reprendre' : completed ? 'Revoir' : 'Commencer'}
            </button>
            <button
              onClick={onAskTutor}
              className="inline-flex h-9 w-9 items-center justify-center rounded-xl border border-white/10 bg-white/[0.04] text-white/60 transition hover:bg-white/[0.08] hover:text-white"
              title="Demander ce cours à Moalim"
              aria-label="Demander ce cours à Moalim"
            >
              <MessageCircle className="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>
    </article>
  );
}

function LibrarySkeleton() {
  return (
    <div className="mt-8 animate-pulse">
      <div className="flex gap-2">
        {[0, 1, 2, 3, 4].map((item) => <div key={item} className="h-10 w-28 rounded-xl bg-white/[0.05]" />)}
      </div>
      <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        {[0, 1, 2, 3, 4, 5, 6, 7].map((item) => <div key={item} className="aspect-[4/5] rounded-2xl bg-white/[0.04]" />)}
      </div>
    </div>
  );
}

function EmptyLibrary() {
  return (
    <div className="mt-8 rounded-3xl border border-dashed border-white/10 bg-white/[0.025] px-6 py-12 text-center">
      <BookOpen className="mx-auto h-8 w-8 text-white/20" />
      <p className="mt-3 text-sm font-bold text-white/65">Aucun cours n'est encore disponible</p>
      <p className="mt-1 text-xs text-white/35">Vérifie les matières attribuées à ton compte.</p>
    </div>
  );
}
