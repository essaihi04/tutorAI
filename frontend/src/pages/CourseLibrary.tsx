import { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  ArrowRight,
  BookOpenCheck,
  CheckCircle2,
  Clock3,
  Folder,
  FolderOpen,
  Layers3,
  MessageCircle,
  Play,
  RefreshCw,
  Sparkles,
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

const EMPTY_CATALOG: CourseCatalog = { subjects: [], total_courses: 0 };

const formatDuration = (minutes: number) => {
  if (minutes < 60) return `${minutes} min`;
  const hours = Math.floor(minutes / 60);
  const remainder = minutes % 60;
  return remainder ? `${hours} h ${remainder}` : `${hours} h`;
};

export default function CourseLibrary() {
  const navigate = useNavigate();
  const [catalog, setCatalog] = useState<CourseCatalog>(EMPTY_CATALOG);
  const [selectedSubjectId, setSelectedSubjectId] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadCatalog = () => {
    setLoading(true);
    setError(null);
    getCourseCatalog()
      .then(({ data }) => {
        setCatalog(data);
        setSelectedSubjectId((current) => {
          if (data.subjects.some((subject) => subject.id === current)) return current;
          return data.subjects.find((subject) => subject.course_count > 0)?.id
            || data.subjects[0]?.id
            || '';
        });
      })
      .catch(() => setError("Impossible de charger les cours pour le moment."))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    let cancelled = false;
    getCourseCatalog()
      .then(({ data }) => {
        if (cancelled) return;
        setCatalog(data);
        setSelectedSubjectId(
          data.subjects.find((subject) => subject.course_count > 0)?.id
            || data.subjects[0]?.id
            || '',
        );
      })
      .catch(() => {
        if (!cancelled) setError("Impossible de charger les cours pour le moment.");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => { cancelled = true; };
  }, []);

  const selectedSubject = useMemo(
    () => catalog.subjects.find((subject) => subject.id === selectedSubjectId) || null,
    [catalog.subjects, selectedSubjectId],
  );

  const openCourse = (course: CourseCatalogCourse) => {
    navigate(
      `/session/${encodeURIComponent(course.chapter_id)}/${encodeURIComponent(course.lesson_id)}`,
      { state: { launchedFromLibrary: true, deckTitle: course.title } },
    );
  };

  const askTutorToOpen = (course: CourseCatalogCourse) => {
    navigate('/tutor', { state: { courseRequest: course.tutor_request } });
  };

  return (
    <MoalimShell>
      <StudentNavigation active="courses" />
      <main className="mx-auto min-h-[calc(100vh-4rem)] max-w-7xl px-4 pb-28 pt-6 sm:px-6 lg:px-8 lg:pb-12 lg:pt-10">
        <section className="relative overflow-hidden rounded-[30px] border border-indigo-400/20 bg-gradient-to-br from-indigo-600/25 via-violet-600/15 to-cyan-500/10 p-6 sm:p-8">
          <div className="pointer-events-none absolute -right-12 -top-16 h-64 w-64 rounded-full bg-cyan-400/15 blur-3xl" />
          <div className="relative max-w-3xl">
            <span className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/[0.07] px-3 py-1 text-xs font-bold text-cyan-200">
              <Sparkles className="h-3.5 w-3.5" /> Bibliothèque avec Moalim
            </span>
            <h1 className="mt-4 text-3xl font-black tracking-tight text-white sm:text-4xl">Mes matières et mes cours</h1>
            <p className="mt-3 max-w-2xl text-sm leading-6 text-white/55 sm:text-base">
              Ouvre un dossier de matière, choisis un cours et Moalim reprend le parcours exactement là où tu en as besoin.
            </p>
          </div>
        </section>

        {loading ? (
          <LibrarySkeleton />
        ) : error ? (
          <section className="mt-8 flex flex-col items-center rounded-3xl border border-rose-400/15 bg-rose-500/[0.05] px-5 py-12 text-center">
            <p className="text-sm font-bold text-rose-200">{error}</p>
            <button onClick={loadCatalog} className="mt-4 inline-flex items-center gap-2 rounded-xl bg-white px-4 py-2 text-xs font-black text-indigo-950">
              <RefreshCw className="h-3.5 w-3.5" /> Réessayer
            </button>
          </section>
        ) : (
          <>
            <section className="mt-8">
              <div className="mb-4 flex items-end justify-between gap-4">
                <div>
                  <p className="text-xs font-bold uppercase tracking-[0.18em] text-white/30">1. Choisis une matière</p>
                  <h2 className="mt-1 text-xl font-black text-white">Dossiers disponibles</h2>
                </div>
                <span className="rounded-full border border-white/[0.08] bg-white/[0.04] px-3 py-1.5 text-xs font-semibold text-white/45">
                  {catalog.total_courses} cours disponible{catalog.total_courses > 1 ? 's' : ''}
                </span>
              </div>

              {catalog.subjects.length > 0 ? (
                <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
                  {catalog.subjects.map((subject) => (
                    <SubjectFolder
                      key={subject.id}
                      subject={subject}
                      selected={subject.id === selectedSubjectId}
                      onSelect={() => setSelectedSubjectId(subject.id)}
                    />
                  ))}
                </div>
              ) : (
                <EmptyLibrary />
              )}
            </section>

            {selectedSubject && (
              <section className="mt-10">
                <div className="mb-4 flex flex-wrap items-end justify-between gap-3">
                  <div>
                    <p className="text-xs font-bold uppercase tracking-[0.18em] text-white/30">2. Entre directement dans un cours</p>
                    <h2 className="mt-1 flex items-center gap-2 text-xl font-black text-white">
                      <span>{selectedSubject.icon || '📚'}</span> {selectedSubject.name_fr}
                    </h2>
                  </div>
                  <button
                    onClick={() => navigate('/tutor')}
                    className="inline-flex items-center gap-2 rounded-xl border border-cyan-300/20 bg-cyan-400/[0.07] px-3 py-2 text-xs font-bold text-cyan-200 transition hover:bg-cyan-400/[0.12]"
                  >
                    <MessageCircle className="h-3.5 w-3.5" /> Demander un autre cours à Moalim
                  </button>
                </div>

                {selectedSubject.courses.length > 0 ? (
                  <div className="grid gap-5 lg:grid-cols-2">
                    {selectedSubject.courses.map((course) => (
                      <CourseCard
                        key={course.stable_id}
                        course={course}
                        onOpen={() => openCourse(course)}
                        onAskTutor={() => askTutorToOpen(course)}
                      />
                    ))}
                  </div>
                ) : (
                  <div className="rounded-3xl border border-dashed border-white/10 bg-white/[0.025] px-6 py-12 text-center">
                    <BookOpenCheck className="mx-auto h-8 w-8 text-white/20" />
                    <p className="mt-3 text-sm font-bold text-white/65">Les cours de cette matière arrivent bientôt</p>
                    <p className="mt-1 text-xs text-white/35">Moalim reste disponible pour expliquer une notion ou faire un exercice.</p>
                    <button onClick={() => navigate('/tutor')} className="mt-4 text-xs font-bold text-cyan-300">Ouvrir le tuteur</button>
                  </div>
                )}
              </section>
            )}
          </>
        )}
      </main>
      <MobileBottomNav active="courses" />
    </MoalimShell>
  );
}

function SubjectFolder({
  subject,
  selected,
  onSelect,
}: {
  subject: CourseCatalogSubject;
  selected: boolean;
  onSelect: () => void;
}) {
  const Icon = selected ? FolderOpen : Folder;
  return (
    <button
      onClick={onSelect}
      className={`group relative overflow-hidden rounded-2xl border p-4 text-left transition-all ${
        selected
          ? 'border-indigo-300/35 bg-indigo-500/15 shadow-lg shadow-indigo-950/25'
          : 'border-white/[0.07] bg-white/[0.035] hover:-translate-y-0.5 hover:border-white/15 hover:bg-white/[0.055]'
      }`}
      aria-pressed={selected}
    >
      <span className={`flex h-11 w-11 items-center justify-center rounded-2xl ${selected ? 'bg-indigo-400 text-indigo-950' : 'bg-white/[0.06] text-white/45'}`}>
        <Icon className="h-5 w-5" />
      </span>
      <span className="mt-4 block truncate text-sm font-black text-white">
        {subject.icon ? `${subject.icon} ` : ''}{subject.name_fr}
      </span>
      <span className="mt-1 block text-xs text-white/40">
        {subject.course_count > 0
          ? `${subject.course_count} cours disponible${subject.course_count > 1 ? 's' : ''}`
          : 'Cours à venir'}
      </span>
      <ArrowRight className={`absolute bottom-4 right-4 h-4 w-4 transition ${selected ? 'text-cyan-300' : 'text-white/15 group-hover:translate-x-0.5 group-hover:text-white/45'}`} />
    </button>
  );
}

function CourseCard({
  course,
  onOpen,
  onAskTutor,
}: {
  course: CourseCatalogCourse;
  onOpen: () => void;
  onAskTutor: () => void;
}) {
  const completed = course.progress_status === 'completed';
  const inProgress = course.progress_status === 'in_progress';
  return (
    <article className="group overflow-hidden rounded-[26px] border border-white/[0.08] bg-white/[0.035] shadow-xl shadow-black/10 transition hover:-translate-y-0.5 hover:border-indigo-300/25 hover:bg-white/[0.05]">
      <button onClick={onOpen} className="relative block aspect-video w-full overflow-hidden text-left">
        {course.cover_image ? (
          <img src={course.cover_image} alt={course.cover_alt} className="h-full w-full object-cover transition duration-500 group-hover:scale-[1.025]" />
        ) : (
          <div className="h-full w-full bg-gradient-to-br from-indigo-600/50 via-violet-600/30 to-cyan-500/25" />
        )}
        <div className="absolute inset-0 bg-gradient-to-t from-[#08081c] via-[#08081c]/15 to-transparent" />
        <span className="absolute left-4 top-4 rounded-full border border-white/15 bg-[#08081c]/65 px-3 py-1 text-[10px] font-black uppercase tracking-wider text-cyan-100 backdrop-blur-md">
          Parcours BAC interactif
        </span>
        {(completed || inProgress) && (
          <span className={`absolute right-4 top-4 inline-flex items-center gap-1 rounded-full px-3 py-1 text-[10px] font-black backdrop-blur-md ${completed ? 'bg-emerald-400 text-emerald-950' : 'bg-amber-300 text-amber-950'}`}>
            {completed && <CheckCircle2 className="h-3 w-3" />}
            {completed ? 'Terminé' : `En cours · ${course.progress_percent}%`}
          </span>
        )}
      </button>

      <div className="p-5">
        <p className="text-[10px] font-bold uppercase tracking-[0.16em] text-indigo-300/70">{course.chapter_title || 'Sciences de la vie et de la Terre'}</p>
        <h3 className="mt-2 text-lg font-black leading-6 text-white">{course.title}</h3>
        <p className="mt-2 text-xs leading-5 text-white/45">{course.summary}</p>

        <div className="mt-4 flex flex-wrap gap-1.5">
          {course.essential_topics.map((topic) => (
            <span key={topic} className="rounded-full border border-white/[0.07] bg-black/15 px-2.5 py-1 text-[10px] font-semibold text-white/55">{topic}</span>
          ))}
        </div>

        <div className="mt-5 flex flex-wrap items-center gap-4 border-t border-white/[0.06] pt-4 text-[11px] font-semibold text-white/35">
          <span className="inline-flex items-center gap-1.5"><Layers3 className="h-3.5 w-3.5" /> {course.activity_count} activités</span>
          <span className="inline-flex items-center gap-1.5"><Clock3 className="h-3.5 w-3.5" /> {formatDuration(course.estimated_minutes)}</span>
        </div>

        <div className="mt-4 grid gap-2 sm:grid-cols-[1fr_auto]">
          <button onClick={onOpen} className="inline-flex items-center justify-center gap-2 rounded-xl bg-white px-4 py-3 text-xs font-black text-indigo-950 transition hover:bg-cyan-50">
            <Play className="h-3.5 w-3.5 fill-current" /> {inProgress ? 'Reprendre le cours' : completed ? 'Revoir depuis le début' : 'Commencer le cours'}
          </button>
          <button onClick={onAskTutor} className="inline-flex items-center justify-center gap-2 rounded-xl border border-white/10 bg-white/[0.04] px-4 py-3 text-xs font-bold text-white/70 transition hover:bg-white/[0.08] hover:text-white" title="Moalim ouvre ce cours à partir de ta demande">
            <MessageCircle className="h-3.5 w-3.5" /> Via Moalim
          </button>
        </div>
      </div>
    </article>
  );
}

function LibrarySkeleton() {
  return (
    <div className="mt-8 space-y-8 animate-pulse">
      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        {[0, 1, 2, 3].map((item) => <div key={item} className="h-32 rounded-2xl bg-white/[0.04]" />)}
      </div>
      <div className="grid gap-5 lg:grid-cols-2">
        {[0, 1].map((item) => <div key={item} className="aspect-[1.35] rounded-[26px] bg-white/[0.04]" />)}
      </div>
    </div>
  );
}

function EmptyLibrary() {
  return (
    <div className="rounded-3xl border border-dashed border-white/10 bg-white/[0.025] px-6 py-12 text-center">
      <Folder className="mx-auto h-8 w-8 text-white/20" />
      <p className="mt-3 text-sm font-bold text-white/65">Aucune matière n'est encore disponible</p>
      <p className="mt-1 text-xs text-white/35">Vérifie les matières attribuées à ton compte.</p>
    </div>
  );
}
