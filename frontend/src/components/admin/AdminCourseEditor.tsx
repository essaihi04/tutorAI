import { useCallback, useEffect, useMemo, useState } from 'react';
import {
  AlertTriangle,
  Archive,
  ArrowDown,
  ArrowUp,
  BookOpen,
  Check,
  ChevronDown,
  ChevronRight,
  CirclePlus,
  Clock3,
  Copy,
  Eye,
  FileAudio,
  FileText,
  Image as ImageIcon,
  Languages,
  Layers3,
  Loader2,
  MessageSquareText,
  Plus,
  RefreshCw,
  Save,
  Search,
  Send,
  Settings2,
  Trash2,
  Upload,
  Volume2,
  X,
} from 'lucide-react';
import {
  archiveAdminCourse,
  createAdminCourse,
  deleteAdminCourse,
  duplicateAdminCourse,
  getAdminCourse,
  getAdminCourseOptions,
  listAdminCourses,
  publishAdminCourse,
  saveAdminCourse,
  updateAdminCourseAudio,
  uploadAdminCourseMedia,
} from '../../services/api';
import type { CourseActivity, CourseQuestion, CourseSlide, CourseSlideType } from '../course/types';
import { getSchemaById } from '../session/schemas';
import SVGSchemaViewer from '../session/schemas/SVGSchemaViewer';
import ScientificVisual from '../session/scientific/ScientificVisual';
import type { ScientificVisualSpec } from '../session/scientific/types';

type CourseStatus = 'draft' | 'verified' | 'published' | 'published_fallback' | 'archived';
type EditorPanel = 'content' | 'tts' | 'question' | 'visual' | 'timing';

interface CourseSummary {
  ref: string;
  id: string;
  source: 'database' | 'manifest';
  stable_id: string;
  title: string;
  version: number;
  status: CourseStatus;
  estimated_minutes: number;
  lesson_id: string;
  lesson_title: string;
  chapter_title: string;
  subject_name: string;
  activity_count: number;
  slide_count: number;
  cover_image?: string;
  stale_audio_count: number;
  editable: boolean;
}

interface LessonOption {
  id: string;
  title: string;
  chapter_title: string;
  subject_name: string;
}

interface SchemaOption {
  id: string;
  title: string;
  subject: string;
}

interface AudioAsset {
  id: string;
  language: string;
  version: number;
  file_path: string;
  duration_ms?: number | null;
  status: string;
  voice?: string;
  provider?: string;
}

interface EditorQuestion extends CourseQuestion {
  answer_key?: string | string[];
  accepted_answers?: string[];
  feedback_correct?: string;
  feedback_incorrect?: string;
}

interface EditorSlide extends Omit<CourseSlide, 'question'> {
  stable_id: string;
  metadata?: Record<string, unknown>;
  audio_assets?: AudioAsset[];
  question?: EditorQuestion;
}

interface EditorActivity extends Omit<CourseActivity, 'slides'> {
  stable_id: string;
  metadata?: Record<string, unknown>;
  slides: EditorSlide[];
}

interface EditorDeck {
  id: string;
  ref: string;
  source: 'database' | 'manifest';
  status: CourseStatus;
  editable: boolean;
  lesson_id: string;
  lesson?: LessonOption;
  stable_id: string;
  title: string;
  version: number;
  language: string;
  estimated_minutes: number;
  catalog: {
    summary?: string;
    cover_image?: string;
    cover_alt?: string;
    essential_topics?: string[];
  };
  lesson_match: string[];
  intent_aliases: string[];
  activities: EditorActivity[];
  stale_audio_count?: number;
  validation_issues?: ValidationIssue[];
}

interface EditorOptions {
  lessons: LessonOption[];
  schemas: SchemaOption[];
  media: { images: string[]; simulations: string[] };
}

interface ValidationIssue {
  level: 'error' | 'warning';
  path: string;
  message: string;
}

type Selection =
  | { kind: 'course' }
  | { kind: 'activity'; activityIndex: number }
  | { kind: 'slide'; activityIndex: number; slideIndex: number };

type VisualKind = 'none' | 'image' | 'schema' | 'simulation' | 'scientific';

const fieldClass = 'w-full rounded-xl border border-gray-200 bg-white px-3 py-2.5 text-sm text-gray-900 outline-none transition focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 disabled:bg-gray-50 disabled:text-gray-400';
const labelClass = 'mb-1.5 block text-xs font-semibold uppercase tracking-wide text-gray-500';
const buttonClass = 'inline-flex items-center justify-center gap-2 rounded-xl px-3 py-2 text-sm font-semibold transition disabled:cursor-not-allowed disabled:opacity-50';

const slideTypeLabels: Record<CourseSlideType, string> = {
  diagnostic: 'Diagnostic',
  situation: 'Situation de départ',
  concept: 'Notion',
  image: 'Image',
  schema: 'Schéma',
  simulation: 'Simulation',
  exercise: 'Exercice',
  synthesis: 'Synthèse',
  evaluation: 'Évaluation',
};

const questionTypes = [
  ['qcm', 'QCM'],
  ['prediction', 'Prédiction'],
  ['true_false', 'Vrai / faux'],
  ['select', 'Sélection'],
  ['open', 'Réponse ouverte'],
  ['ordering', 'Mise en ordre'],
  ['association', 'Association'],
] as const;

function copyJson<T>(value: T): T {
  return JSON.parse(JSON.stringify(value)) as T;
}

function parseAnswerKey(value: string, type?: EditorQuestion['type']): string | string[] {
  return type === 'ordering'
    ? value.split(/\r?\n|\s*→\s*/).map(item => item.trim()).filter(Boolean)
    : value;
}

function questionPayload(question?: EditorQuestion): EditorQuestion {
  if (!question) return {};
  return {
    ...question,
    answer_key: typeof question.answer_key === 'string'
      ? parseAnswerKey(question.answer_key, question.type)
      : question.answer_key,
  };
}

function stableToken(prefix: string, kind: 'a' | 's'): string {
  const clean = prefix.toLowerCase().replace(/[^a-z0-9_-]+/g, '_').replace(/^_+|_+$/g, '').slice(0, 80) || 'cours';
  return `${clean}_${kind}_${Date.now().toString(36)}${Math.random().toString(36).slice(2, 6)}`;
}

function normaliseDeck(raw: EditorDeck): EditorDeck {
  return {
    ...raw,
    catalog: raw.catalog || {},
    lesson_match: raw.lesson_match || [],
    intent_aliases: raw.intent_aliases || [],
    activities: (raw.activities || []).map(activity => ({
      ...activity,
      id: String(activity.id || activity.stable_id),
      stable_id: String(activity.stable_id || activity.id),
      objective_ids: activity.objective_ids || [],
      slides: (activity.slides || []).map(slide => ({
        ...slide,
        id: String(slide.id || slide.stable_id),
        stable_id: String(slide.stable_id || slide.id),
        screen_content: slide.screen_content || {},
        visual: slide.visual || { kind: 'none' },
        speech_text: slide.speech_text || {},
        question: questionPayload(slide.question),
        timing: slide.timing || {},
        audio_assets: slide.audio_assets || [],
      })),
    })),
  };
}

function savePayload(deck: EditorDeck) {
  return {
    stable_id: deck.stable_id,
    title: deck.title,
    language: deck.language,
    estimated_minutes: Number(deck.estimated_minutes || 1),
    catalog: deck.catalog || {},
    lesson_match: deck.lesson_match || [],
    intent_aliases: deck.intent_aliases || [],
    activities: deck.activities.map(activity => ({
      id: activity.id,
      stable_id: activity.stable_id,
      title: activity.title,
      phase: activity.phase || 'explanation',
      duration_minutes: Number(activity.duration_minutes || 1),
      objective_ids: activity.objective_ids || [],
      metadata: activity.metadata || {},
      slides: activity.slides.map(slide => ({
        id: slide.id,
        stable_id: slide.stable_id,
        slide_type: slide.slide_type,
        title: slide.title,
        screen_content: slide.screen_content || {},
        visual: slide.visual || {},
        speech_text: slide.speech_text || {},
        question: slide.question || {},
        timing: slide.timing || {},
        metadata: slide.metadata || {},
      })),
    })),
  };
}

function apiMessage(error: unknown): { message: string; issues: ValidationIssue[] } {
  const candidate = error as {
    message?: string;
    response?: { data?: { detail?: string | { message?: string; issues?: ValidationIssue[] } } };
  };
  const detail = candidate?.response?.data?.detail;
  if (typeof detail === 'string') return { message: detail, issues: [] };
  if (detail?.issues) return { message: detail.message || 'Le cours contient des erreurs.', issues: detail.issues };
  return { message: candidate?.message || 'Une erreur est survenue.', issues: [] };
}

function StatusBadge({ status }: { status: CourseStatus }) {
  const style: Record<CourseStatus, string> = {
    draft: 'bg-amber-100 text-amber-800',
    verified: 'bg-blue-100 text-blue-800',
    published: 'bg-emerald-100 text-emerald-800',
    published_fallback: 'bg-violet-100 text-violet-800',
    archived: 'bg-gray-200 text-gray-600',
  };
  const label: Record<CourseStatus, string> = {
    draft: 'Brouillon',
    verified: 'Vérifié',
    published: 'Publié',
    published_fallback: 'Manifest actif',
    archived: 'Archivé',
  };
  return <span className={`rounded-full px-2 py-1 text-[10px] font-bold uppercase tracking-wide ${style[status]}`}>{label[status]}</span>;
}

function IconButton({ title, onClick, disabled, children, danger = false }: {
  title: string;
  onClick: () => void;
  disabled?: boolean;
  children: React.ReactNode;
  danger?: boolean;
}) {
  return (
    <button type="button" title={title} aria-label={title} onClick={event => { event.stopPropagation(); onClick(); }} disabled={disabled}
      className={`rounded-lg p-1.5 transition disabled:opacity-30 ${danger ? 'text-red-500 hover:bg-red-50' : 'text-gray-400 hover:bg-gray-100 hover:text-gray-700'}`}>
      {children}
    </button>
  );
}

function SlidePreview({ slide }: { slide: EditorSlide }) {
  const visual = slide.visual || {};
  const schema = visual.kind === 'schema' && visual.schema_id ? getSchemaById(visual.schema_id) : undefined;
  return (
    <div className="overflow-hidden rounded-2xl border border-slate-700 bg-[#071323] text-white shadow-xl">
      <div className="border-b border-slate-700/80 bg-slate-900/70 px-4 py-3">
        <div className="flex items-center justify-between gap-3">
          <span className="rounded-full bg-cyan-500/15 px-2 py-1 text-[10px] font-bold uppercase tracking-widest text-cyan-300">
            {slideTypeLabels[slide.slide_type]}
          </span>
          <Eye className="h-4 w-4 text-slate-500" />
        </div>
        <h3 className="mt-2 text-lg font-bold">{slide.title || 'Titre de la diapositive'}</h3>
      </div>
      <div className="space-y-4 p-4">
        {slide.screen_content?.lead && <p className="text-sm leading-6 text-slate-200">{slide.screen_content.lead}</p>}
        {!!slide.screen_content?.bullets?.length && (
          <ul className="space-y-2 text-sm text-slate-200">
            {slide.screen_content.bullets.map((bullet, index) => (
              <li key={`${bullet}-${index}`} className="flex gap-2"><span className="mt-2 h-1.5 w-1.5 flex-none rounded-full bg-cyan-400" />{bullet}</li>
            ))}
          </ul>
        )}
        {slide.screen_content?.essential_text && (
          <div className="rounded-xl border border-cyan-500/30 bg-cyan-500/10 p-3 text-sm font-semibold text-cyan-50">
            {slide.screen_content.essential_text}
          </div>
        )}
        {visual.kind === 'image' && visual.url && (
          <img src={visual.url} alt={visual.alt || slide.title} className="max-h-72 w-full rounded-xl bg-white object-contain" />
        )}
        {visual.kind === 'simulation' && visual.url && (
          <iframe title={slide.title} src={visual.url} className="h-72 w-full rounded-xl bg-white" sandbox="allow-scripts allow-same-origin" />
        )}
        {schema && (
          <div className="overflow-hidden rounded-xl bg-slate-950 p-1">
            <SVGSchemaViewer schema={schema} autoAnimate={false} handDrawn className="h-72 w-full" />
          </div>
        )}
        {visual.kind === 'scientific' && visual.scientific && (
          <div className="min-h-64 overflow-hidden rounded-xl bg-slate-950 p-2">
            <ScientificVisual spec={visual.scientific} />
          </div>
        )}
        {visual.caption && <p className="text-center text-xs italic text-slate-400">{visual.caption}</p>}
        {slide.screen_content?.student_trace && (
          <div className="rounded-xl border border-amber-400/25 bg-amber-400/10 p-3 text-sm text-amber-50">
            <span className="mb-1 block text-[10px] font-bold uppercase tracking-wider text-amber-300">Trace à retenir</span>
            {slide.screen_content.student_trace}
          </div>
        )}
        {slide.question?.prompt && (
          <div className="rounded-xl border border-indigo-400/30 bg-indigo-500/10 p-3">
            <div className="mb-2 flex items-center gap-2 text-xs font-bold text-indigo-200"><MessageSquareText className="h-4 w-4" /> Question</div>
            <p className="text-sm font-medium">{slide.question.prompt}</p>
            {!!slide.question.options?.length && (
              <div className="mt-3 space-y-2">
                {slide.question.options.map(option => <div key={option} className="rounded-lg border border-slate-600 px-3 py-2 text-xs text-slate-200">{option}</div>)}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

function ScientificJsonEditor({ value, disabled, onChange }: {
  value?: ScientificVisualSpec;
  disabled: boolean;
  onChange: (value: ScientificVisualSpec) => void;
}) {
  const [text, setText] = useState(() => JSON.stringify(value || {}, null, 2));
  const [error, setError] = useState('');
  useEffect(() => setText(JSON.stringify(value || {}, null, 2)), [value]);
  const apply = () => {
    try {
      const parsed = JSON.parse(text);
      if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) throw new Error('Objet JSON attendu');
      onChange(parsed as ScientificVisualSpec);
      setError('');
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'JSON invalide');
    }
  };
  return (
    <div>
      <label className={labelClass}>Payload scientifique déclaratif</label>
      <textarea value={text} disabled={disabled} onChange={event => setText(event.target.value)} rows={14}
        className={`${fieldClass} font-mono text-xs`} spellCheck={false} />
      <div className="mt-2 flex items-center justify-between gap-3">
        <span className={`text-xs ${error ? 'text-red-600' : 'text-gray-400'}`}>{error || 'JSXGraph, Cytoscape ou Matter.js — aucun JavaScript libre.'}</span>
        <button type="button" disabled={disabled} onClick={apply} className={`${buttonClass} bg-slate-800 text-white hover:bg-slate-900`}>Appliquer</button>
      </div>
    </div>
  );
}

function CreateCourseModal({ lessons, onClose, onCreate, loading }: {
  lessons: LessonOption[];
  onClose: () => void;
  onCreate: (data: { lesson_id: string; stable_id: string; title: string; language: string; estimated_minutes: number }) => void;
  loading: boolean;
}) {
  const [form, setForm] = useState({ lesson_id: '', stable_id: '', title: '', language: 'fr', estimated_minutes: 60 });
  const setTitle = (title: string) => setForm(previous => ({
    ...previous,
    title,
    stable_id: previous.stable_id || title.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9]+/g, '_').replace(/^_+|_+$/g, '').slice(0, 100),
  }));
  return (
    <div className="fixed inset-0 z-[70] flex items-center justify-center bg-black/55 p-4" onClick={onClose}>
      <div className="w-full max-w-xl rounded-2xl bg-white p-6 shadow-2xl" onClick={event => event.stopPropagation()}>
        <div className="mb-5 flex items-center justify-between">
          <div><h3 className="text-lg font-bold text-gray-900">Créer un cours</h3><p className="text-sm text-gray-500">Un brouillon versionné sera rattaché à une leçon existante.</p></div>
          <button onClick={onClose} className="rounded-lg p-2 hover:bg-gray-100"><X className="h-5 w-5" /></button>
        </div>
        <div className="space-y-4">
          <div><label className={labelClass}>Matière / chapitre / leçon</label><select className={fieldClass} value={form.lesson_id} onChange={event => setForm({ ...form, lesson_id: event.target.value })}><option value="">Choisir une leçon…</option>{lessons.map(lesson => <option key={lesson.id} value={lesson.id}>{lesson.subject_name} · {lesson.chapter_title} · {lesson.title}</option>)}</select></div>
          <div><label className={labelClass}>Titre</label><input className={fieldClass} value={form.title} onChange={event => setTitle(event.target.value)} placeholder="Ex. Ondes mécaniques progressives" /></div>
          <div><label className={labelClass}>Identifiant stable</label><input className={fieldClass} value={form.stable_id} onChange={event => setForm({ ...form, stable_id: event.target.value.toLowerCase().replace(/[^a-z0-9_-]/g, '_') })} placeholder="phys_ondes_progressives" /></div>
          <div className="grid grid-cols-2 gap-3"><div><label className={labelClass}>Langue principale</label><select className={fieldClass} value={form.language} onChange={event => setForm({ ...form, language: event.target.value })}><option value="fr">Français</option><option value="mixed">Darija</option><option value="ar">Arabe</option></select></div><div><label className={labelClass}>Durée estimée</label><input type="number" min={1} className={fieldClass} value={form.estimated_minutes} onChange={event => setForm({ ...form, estimated_minutes: Number(event.target.value) })} /></div></div>
        </div>
        <div className="mt-6 flex justify-end gap-3"><button onClick={onClose} className={`${buttonClass} border border-gray-200 text-gray-700 hover:bg-gray-50`}>Annuler</button><button disabled={loading || !form.lesson_id || !form.title || !form.stable_id} onClick={() => onCreate(form)} className={`${buttonClass} bg-indigo-600 text-white hover:bg-indigo-700`}>{loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Plus className="h-4 w-4" />} Créer le brouillon</button></div>
      </div>
    </div>
  );
}

export default function AdminCourseEditor() {
  const [courses, setCourses] = useState<CourseSummary[]>([]);
  const [options, setOptions] = useState<EditorOptions>({ lessons: [], schemas: [], media: { images: [], simulations: [] } });
  const [deck, setDeck] = useState<EditorDeck | null>(null);
  const [selection, setSelection] = useState<Selection>({ kind: 'course' });
  const [panel, setPanel] = useState<EditorPanel>('content');
  const [expandedActivities, setExpandedActivities] = useState<Set<string>>(new Set());
  const [search, setSearch] = useState('');
  const [subjectFilter, setSubjectFilter] = useState('all');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [dirty, setDirty] = useState(false);
  const [message, setMessage] = useState<{ kind: 'success' | 'error'; text: string } | null>(null);
  const [issues, setIssues] = useState<ValidationIssue[]>([]);
  const [showCreate, setShowCreate] = useState(false);
  const [previewOpen, setPreviewOpen] = useState(false);

  const refreshLibrary = useCallback(async () => {
    const response = await listAdminCourses();
    setCourses(response.data.courses || []);
  }, []);

  const loadInitial = useCallback(async () => {
    setLoading(true);
    setMessage(null);
    try {
      const [coursesResponse, optionsResponse] = await Promise.all([listAdminCourses(), getAdminCourseOptions()]);
      setCourses(coursesResponse.data.courses || []);
      setOptions(optionsResponse.data);
      if (coursesResponse.data.database_available === false) {
        setMessage({ kind: 'error', text: 'Les manifests sont visibles, mais les tables de cours ne sont pas encore disponibles dans la base.' });
      }
    } catch (error) {
      setMessage({ kind: 'error', text: apiMessage(error).message });
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { void loadInitial(); }, [loadInitial]);
  useEffect(() => {
    const beforeUnload = (event: BeforeUnloadEvent) => {
      if (!dirty) return;
      event.preventDefault();
    };
    window.addEventListener('beforeunload', beforeUnload);
    return () => window.removeEventListener('beforeunload', beforeUnload);
  }, [dirty]);

  const selectedActivity = selection.kind !== 'course' && deck ? deck.activities[selection.activityIndex] : undefined;
  const selectedSlide = selection.kind === 'slide' ? selectedActivity?.slides[selection.slideIndex] : undefined;
  const canEdit = Boolean(deck?.editable && deck.source === 'database');

  const mutate = useCallback((recipe: (next: EditorDeck) => void) => {
    setDeck(previous => {
      if (!previous || !previous.editable) return previous;
      const next = copyJson(previous);
      recipe(next);
      return next;
    });
    setDirty(true);
    setMessage(null);
  }, []);

  const loadCourse = async (courseRef: string) => {
    if (dirty && !window.confirm('Abandonner les modifications non enregistrées ?')) return;
    setLoading(true);
    setMessage(null);
    setIssues([]);
    try {
      const response = await getAdminCourse(courseRef);
      const loaded = normaliseDeck(response.data.course);
      setDeck(loaded);
      setSelection({ kind: 'course' });
      setExpandedActivities(new Set(loaded.activities.map(activity => activity.stable_id)));
      setDirty(false);
    } catch (error) {
      setMessage({ kind: 'error', text: apiMessage(error).message });
    } finally {
      setLoading(false);
    }
  };

  const saveDraft = useCallback(async (): Promise<EditorDeck | null> => {
    if (!deck || !canEdit) return deck;
    setSaving(true);
    setMessage(null);
    setIssues([]);
    try {
      const response = await saveAdminCourse(deck.id, savePayload(deck));
      const saved = normaliseDeck(response.data.course);
      setDeck(saved);
      setDirty(false);
      setIssues(saved.validation_issues || []);
      const stale = Number(response.data.course.stale_audio_count || 0);
      setMessage({ kind: 'success', text: stale ? `Brouillon enregistré. ${stale} ancien(s) audio(s) conservé(s) et marqué(s) à régénérer.` : 'Brouillon enregistré.' });
      await refreshLibrary();
      return saved;
    } catch (error) {
      const parsed = apiMessage(error);
      setMessage({ kind: 'error', text: parsed.message });
      setIssues(parsed.issues);
      return null;
    } finally {
      setSaving(false);
    }
  }, [canEdit, deck, refreshLibrary]);

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 's') {
        event.preventDefault();
        if (canEdit && dirty && !saving) void saveDraft();
      }
    };
    window.addEventListener('keydown', onKeyDown);
    return () => window.removeEventListener('keydown', onKeyDown);
  }, [canEdit, dirty, saveDraft, saving]);

  const duplicateVersion = async (courseRef = deck?.ref, lessonId = deck?.lesson_id) => {
    if (!courseRef) return;
    setSaving(true);
    setMessage(null);
    try {
      const response = await duplicateAdminCourse(courseRef, lessonId || undefined);
      const created = normaliseDeck(response.data.course);
      setDeck(created);
      setSelection({ kind: 'course' });
      setExpandedActivities(new Set(created.activities.map(activity => activity.stable_id)));
      setDirty(false);
      setMessage({ kind: 'success', text: `Version ${created.version} créée en brouillon. Vous pouvez maintenant tout modifier.` });
      await refreshLibrary();
    } catch (error) {
      const parsed = apiMessage(error);
      setMessage({ kind: 'error', text: parsed.message });
      setIssues(parsed.issues);
    } finally {
      setSaving(false);
    }
  };

  const publish = async () => {
    if (!deck || !canEdit || !window.confirm('Publier cette version pour les élèves ? La version publiée précédente sera archivée.')) return;
    const current = dirty ? await saveDraft() : deck;
    if (!current) return;
    setSaving(true);
    try {
      const response = await publishAdminCourse(current.id);
      setDeck(normaliseDeck(response.data.course));
      setDirty(false);
      setIssues(response.data.course.validation_issues || []);
      setMessage({ kind: 'success', text: 'Cours publié. Le catalogue et le tuteur utilisent maintenant cette version.' });
      await refreshLibrary();
    } catch (error) {
      const parsed = apiMessage(error);
      setMessage({ kind: 'error', text: parsed.message });
      setIssues(parsed.issues);
    } finally {
      setSaving(false);
    }
  };

  const archive = async () => {
    if (!deck || deck.source !== 'database' || !window.confirm('Archiver cette version ?')) return;
    setSaving(true);
    try {
      const response = await archiveAdminCourse(deck.id);
      setDeck(normaliseDeck(response.data.course));
      setMessage({ kind: 'success', text: 'Version archivée.' });
      await refreshLibrary();
    } catch (error) {
      setMessage({ kind: 'error', text: apiMessage(error).message });
    } finally { setSaving(false); }
  };

  const removeCourse = async () => {
    if (!deck || deck.source !== 'database') return;
    const confirmation = window.prompt(`Tapez SUPPRIMER pour effacer définitivement la version ${deck.version}.`);
    if (confirmation !== 'SUPPRIMER') return;
    setSaving(true);
    try {
      await deleteAdminCourse(deck.id);
      setDeck(null);
      setDirty(false);
      setMessage({ kind: 'success', text: 'Version supprimée.' });
      await refreshLibrary();
    } catch (error) {
      setMessage({ kind: 'error', text: apiMessage(error).message });
    } finally { setSaving(false); }
  };

  const createCourse = async (form: { lesson_id: string; stable_id: string; title: string; language: string; estimated_minutes: number }) => {
    setSaving(true);
    try {
      const response = await createAdminCourse(form);
      const created = normaliseDeck(response.data.course);
      setDeck(created);
      setSelection({ kind: 'course' });
      setExpandedActivities(new Set(created.activities.map(activity => activity.stable_id)));
      setShowCreate(false);
      setDirty(false);
      setMessage({ kind: 'success', text: 'Nouveau brouillon créé.' });
      await refreshLibrary();
    } catch (error) {
      const parsed = apiMessage(error);
      setMessage({ kind: 'error', text: parsed.message });
      setIssues(parsed.issues);
    } finally { setSaving(false); }
  };

  const uploadMedia = async (file: File): Promise<string | null> => {
    setSaving(true);
    try {
      const response = await uploadAdminCourseMedia(file);
      const url = response.data.url as string;
      setOptions(previous => ({ ...previous, media: { ...previous.media, images: [...new Set([...previous.media.images, url])] } }));
      setMessage({ kind: 'success', text: 'Image enregistrée dans la bibliothèque persistante.' });
      return url;
    } catch (error) {
      setMessage({ kind: 'error', text: apiMessage(error).message });
      return null;
    } finally { setSaving(false); }
  };

  const addActivity = () => {
    if (!deck) return;
    const stableId = stableToken(deck.stable_id, 'a');
    mutate(next => next.activities.push({ id: stableId, stable_id: stableId, title: 'Nouvelle activité', phase: 'explanation', duration_minutes: 15, objective_ids: [], slides: [] }));
    const index = deck.activities.length;
    setSelection({ kind: 'activity', activityIndex: index });
    setExpandedActivities(previous => new Set([...previous, stableId]));
  };

  const duplicateActivity = (activityIndex: number) => {
    if (!deck) return;
    mutate(next => {
      const source = copyJson(next.activities[activityIndex]);
      source.stable_id = stableToken(next.stable_id, 'a');
      source.id = source.stable_id;
      source.title = `${source.title} — copie`;
      source.slides = source.slides.map(slide => {
        const stableId = stableToken(next.stable_id, 's');
        return { ...slide, id: stableId, stable_id: stableId, title: `${slide.title} — copie`, audio_assets: [] };
      });
      next.activities.splice(activityIndex + 1, 0, source);
    });
    setSelection({ kind: 'activity', activityIndex: activityIndex + 1 });
  };

  const moveActivity = (activityIndex: number, direction: -1 | 1) => {
    const target = activityIndex + direction;
    if (!deck || target < 0 || target >= deck.activities.length) return;
    mutate(next => { const [item] = next.activities.splice(activityIndex, 1); next.activities.splice(target, 0, item); });
    setSelection(current => current.kind === 'course' ? current : { ...current, activityIndex: target });
  };

  const removeActivity = (activityIndex: number) => {
    if (!deck || !window.confirm('Supprimer cette activité et toutes ses diapositives ?')) return;
    mutate(next => { next.activities.splice(activityIndex, 1); });
    setSelection({ kind: 'course' });
  };

  const addSlide = (activityIndex: number, slideType: CourseSlideType = 'concept') => {
    if (!deck) return;
    const stableId = stableToken(deck.stable_id, 's');
    const slide: EditorSlide = {
      id: stableId,
      stable_id: stableId,
      slide_type: slideType,
      title: 'Nouvelle diapositive',
      screen_content: { lead: '', bullets: [], essential_text: '', student_trace: '' },
      visual: { kind: 'none', caption: '', alt: '' },
      speech_text: { fr: '', mixed: '' },
      question: { type: 'open', prompt: '', options: [], timeout_seconds: 15, advance_on_timeout: true },
      timing: { auto_advance: true, reading_seconds: 12, delay_after_feedback_ms: 900 },
      audio_assets: [],
    };
    mutate(next => next.activities[activityIndex].slides.push(slide));
    setSelection({ kind: 'slide', activityIndex, slideIndex: deck.activities[activityIndex].slides.length });
    setPanel('content');
  };

  const duplicateSlide = (activityIndex: number, slideIndex: number) => {
    if (!deck) return;
    mutate(next => {
      const source = copyJson(next.activities[activityIndex].slides[slideIndex]);
      const stableId = stableToken(next.stable_id, 's');
      source.id = stableId;
      source.stable_id = stableId;
      source.title = `${source.title} — copie`;
      source.audio_assets = [];
      next.activities[activityIndex].slides.splice(slideIndex + 1, 0, source);
    });
    setSelection({ kind: 'slide', activityIndex, slideIndex: slideIndex + 1 });
  };

  const moveSlide = (activityIndex: number, slideIndex: number, direction: -1 | 1) => {
    if (!deck) return;
    const target = slideIndex + direction;
    if (target < 0 || target >= deck.activities[activityIndex].slides.length) return;
    mutate(next => { const slides = next.activities[activityIndex].slides; const [item] = slides.splice(slideIndex, 1); slides.splice(target, 0, item); });
    setSelection({ kind: 'slide', activityIndex, slideIndex: target });
  };

  const removeSlide = (activityIndex: number, slideIndex: number) => {
    if (!window.confirm('Supprimer cette diapositive ? Les audios liés resteront récupérables uniquement via les sauvegardes de base.')) return;
    mutate(next => { next.activities[activityIndex].slides.splice(slideIndex, 1); });
    setSelection({ kind: 'activity', activityIndex });
  };

  const subjects = useMemo(() => [...new Set(courses.map(course => course.subject_name).filter(Boolean))].sort(), [courses]);
  const filteredCourses = useMemo(() => courses.filter(course => {
    const matchesSubject = subjectFilter === 'all' || course.subject_name === subjectFilter;
    const haystack = `${course.title} ${course.subject_name} ${course.chapter_title} ${course.lesson_title}`.toLowerCase();
    return matchesSubject && haystack.includes(search.toLowerCase());
  }), [courses, search, subjectFilter]);

  const totalSlides = deck?.activities.reduce((sum, activity) => sum + activity.slides.length, 0) || 0;
  const lesson = options.lessons.find(item => item.id === deck?.lesson_id) || deck?.lesson;

  if (loading && !courses.length && !deck) {
    return <div className="flex min-h-[520px] items-center justify-center rounded-2xl border bg-white"><Loader2 className="h-8 w-8 animate-spin text-indigo-600" /></div>;
  }

  return (
    <div className="space-y-4">
      <div className="rounded-2xl border border-gray-200 bg-gradient-to-r from-slate-950 via-indigo-950 to-slate-900 p-5 text-white shadow-sm">
        <div className="flex flex-col justify-between gap-4 lg:flex-row lg:items-center">
          <div><div className="mb-2 flex items-center gap-2 text-xs font-bold uppercase tracking-[0.2em] text-indigo-300"><BookOpen className="h-4 w-4" /> Studio pédagogique</div><h2 className="text-2xl font-bold">Éditeur de cours</h2><p className="mt-1 max-w-3xl text-sm text-slate-300">Contrôlez la structure, le contenu, le speech français/Darija, les questions, les schémas, les simulations et la publication.</p></div>
          <div className="flex flex-wrap gap-2"><button onClick={() => void loadInitial()} className={`${buttonClass} bg-white/10 text-white hover:bg-white/20`}><RefreshCw className="h-4 w-4" /> Actualiser</button><button onClick={() => setShowCreate(true)} className={`${buttonClass} bg-indigo-500 text-white hover:bg-indigo-400`}><CirclePlus className="h-4 w-4" /> Nouveau cours</button></div>
        </div>
      </div>

      {message && <div className={`flex items-start gap-3 rounded-xl border p-3 text-sm ${message.kind === 'success' ? 'border-emerald-200 bg-emerald-50 text-emerald-800' : 'border-red-200 bg-red-50 text-red-700'}`}>{message.kind === 'success' ? <Check className="mt-0.5 h-4 w-4 flex-none" /> : <AlertTriangle className="mt-0.5 h-4 w-4 flex-none" />}<span>{message.text}</span><button onClick={() => setMessage(null)} className="ml-auto"><X className="h-4 w-4" /></button></div>}
      {!!issues.length && <div className="rounded-xl border border-amber-200 bg-amber-50 p-3"><div className="mb-2 flex items-center gap-2 text-sm font-bold text-amber-900"><AlertTriangle className="h-4 w-4" /> Contrôles éditoriaux ({issues.length})</div><div className="max-h-40 space-y-1 overflow-auto">{issues.map((issue, index) => <button key={`${issue.path}-${index}`} onClick={() => setMessage({ kind: issue.level === 'error' ? 'error' : 'success', text: `${issue.path} — ${issue.message}` })} className={`block w-full rounded px-2 py-1 text-left text-xs ${issue.level === 'error' ? 'bg-red-50 text-red-700' : 'text-amber-800 hover:bg-amber-100'}`}><strong>{issue.path}</strong> — {issue.message}</button>)}</div></div>}

      <div className="grid min-h-[720px] grid-cols-1 gap-4 xl:grid-cols-[300px_minmax(0,1fr)]">
        <aside className="overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-sm">
          <div className="border-b p-3"><div className="relative"><Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" /><input className={`${fieldClass} pl-9`} value={search} onChange={event => setSearch(event.target.value)} placeholder="Rechercher un cours…" /></div><select className={`${fieldClass} mt-2`} value={subjectFilter} onChange={event => setSubjectFilter(event.target.value)}><option value="all">Toutes les matières</option>{subjects.map(subject => <option key={subject}>{subject}</option>)}</select></div>
          <div className="max-h-[640px] space-y-2 overflow-y-auto p-2">
            {filteredCourses.map(course => (
              <button key={course.ref} onClick={() => void loadCourse(course.ref)} className={`w-full overflow-hidden rounded-xl border text-left transition hover:border-indigo-300 hover:shadow-sm ${deck?.ref === course.ref ? 'border-indigo-400 bg-indigo-50/60' : 'border-gray-100 bg-white'}`}>
                {course.cover_image && <img src={course.cover_image} alt="" className="h-20 w-full object-cover" />}
                <div className="p-3"><div className="mb-2 flex items-center justify-between gap-2"><StatusBadge status={course.status} /><span className="text-[10px] font-bold text-gray-400">v{course.version}</span></div><h3 className="line-clamp-2 text-sm font-bold text-gray-900">{course.title}</h3><p className="mt-1 truncate text-xs text-gray-500">{course.subject_name || 'Matière'} · {course.lesson_title || 'Leçon à relier'}</p><div className="mt-2 flex items-center gap-3 text-[11px] text-gray-400"><span>{course.activity_count} activités</span><span>{course.slide_count} diapos</span>{course.stale_audio_count > 0 && <span className="text-amber-600">{course.stale_audio_count} audio à refaire</span>}</div></div>
              </button>
            ))}
            {!filteredCourses.length && <div className="py-10 text-center text-sm text-gray-400">Aucun cours trouvé.</div>}
          </div>
        </aside>

        {!deck ? (
          <div className="flex min-h-[650px] flex-col items-center justify-center rounded-2xl border border-dashed border-gray-300 bg-white p-8 text-center"><div className="mb-4 rounded-2xl bg-indigo-50 p-4"><Layers3 className="h-9 w-9 text-indigo-600" /></div><h3 className="text-lg font-bold text-gray-900">Choisissez un cours à gauche</h3><p className="mt-2 max-w-lg text-sm text-gray-500">Vous pourrez ouvrir un manifest existant, créer sa prochaine version ou commencer un nouveau cours lié au programme.</p></div>
        ) : (
          <main className="min-w-0 overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-sm">
            <div className="border-b bg-gray-50/80 p-3">
              <div className="flex flex-col justify-between gap-3 lg:flex-row lg:items-center">
                <div className="min-w-0"><div className="flex flex-wrap items-center gap-2"><StatusBadge status={deck.status} /><span className="text-xs font-bold text-gray-400">Version {deck.version}</span>{dirty && <span className="rounded-full bg-amber-100 px-2 py-1 text-[10px] font-bold text-amber-700">Modifications non enregistrées</span>}</div><h3 className="mt-1 truncate text-lg font-bold text-gray-900">{deck.title}</h3><p className="truncate text-xs text-gray-500">{lesson?.subject_name} · {lesson?.chapter_title} · {lesson?.title}</p></div>
                <div className="flex flex-wrap gap-2">
                  {!canEdit && <button disabled={saving} onClick={() => void duplicateVersion()} className={`${buttonClass} bg-indigo-600 text-white hover:bg-indigo-700`}><Copy className="h-4 w-4" /> Créer une version modifiable</button>}
                  {canEdit && <><button disabled={saving || !dirty} onClick={() => void saveDraft()} className={`${buttonClass} border border-gray-200 bg-white text-gray-700 hover:bg-gray-50`}>{saving ? <Loader2 className="h-4 w-4 animate-spin" /> : <Save className="h-4 w-4" />} Enregistrer</button><button disabled={saving} onClick={() => void publish()} className={`${buttonClass} bg-emerald-600 text-white hover:bg-emerald-700`}><Send className="h-4 w-4" /> Publier</button></>}
                  {deck.source === 'database' && deck.status === 'published' && <button disabled={saving} onClick={() => void archive()} className={`${buttonClass} border border-gray-200 bg-white text-gray-700 hover:bg-gray-50`}><Archive className="h-4 w-4" /> Archiver</button>}
                  {deck.source === 'database' && deck.status !== 'published' && <button disabled={saving} onClick={() => void removeCourse()} className={`${buttonClass} border border-red-200 bg-white text-red-600 hover:bg-red-50`}><Trash2 className="h-4 w-4" /> Supprimer</button>}
                </div>
              </div>
            </div>

            <div className="grid min-h-[650px] grid-cols-1 lg:grid-cols-[260px_minmax(0,1fr)] 2xl:grid-cols-[260px_minmax(430px,1fr)_minmax(340px,0.8fr)]">
              <div className="border-b border-gray-200 bg-slate-50 lg:border-b-0 lg:border-r">
                <button onClick={() => setSelection({ kind: 'course' })} className={`flex w-full items-center gap-2 border-b px-3 py-3 text-left text-sm font-bold ${selection.kind === 'course' ? 'bg-indigo-50 text-indigo-700' : 'text-gray-700 hover:bg-gray-100'}`}><Settings2 className="h-4 w-4" /> Paramètres du cours <span className="ml-auto text-[10px] font-normal text-gray-400">{totalSlides} diapos</span></button>
                <div className="max-h-[590px] overflow-y-auto p-2">
                  {deck.activities.map((activity, activityIndex) => {
                    const expanded = expandedActivities.has(activity.stable_id);
                    return <div key={activity.stable_id} className="mb-2 overflow-hidden rounded-xl border border-gray-200 bg-white"><div className={`flex items-center gap-1 ${selection.kind !== 'course' && selection.activityIndex === activityIndex && selection.kind === 'activity' ? 'bg-indigo-50' : ''}`}><button onClick={() => setExpandedActivities(previous => { const next = new Set(previous); if (expanded) next.delete(activity.stable_id); else next.add(activity.stable_id); return next; })} className="p-2 text-gray-400">{expanded ? <ChevronDown className="h-4 w-4" /> : <ChevronRight className="h-4 w-4" />}</button><button onClick={() => setSelection({ kind: 'activity', activityIndex })} className="min-w-0 flex-1 py-2 pr-1 text-left"><span className="block truncate text-xs font-bold text-gray-800">{activityIndex + 1}. {activity.title}</span><span className="text-[10px] text-gray-400">{activity.duration_minutes || 0} min · {activity.slides.length} diapos</span></button>{canEdit && <div className="flex"><IconButton title="Monter" disabled={activityIndex === 0} onClick={() => moveActivity(activityIndex, -1)}><ArrowUp className="h-3.5 w-3.5" /></IconButton><IconButton title="Descendre" disabled={activityIndex === deck.activities.length - 1} onClick={() => moveActivity(activityIndex, 1)}><ArrowDown className="h-3.5 w-3.5" /></IconButton></div>}</div>{expanded && <div className="border-t bg-gray-50/60 p-1.5">{activity.slides.map((slide, slideIndex) => <div key={slide.stable_id} className={`group mb-1 flex items-center rounded-lg ${selection.kind === 'slide' && selection.activityIndex === activityIndex && selection.slideIndex === slideIndex ? 'bg-indigo-600 text-white' : 'text-gray-600 hover:bg-white'}`}><button onClick={() => { setSelection({ kind: 'slide', activityIndex, slideIndex }); setPanel('content'); }} className="min-w-0 flex-1 px-2 py-2 text-left"><span className="block truncate text-xs font-medium">{slideIndex + 1}. {slide.title}</span><span className={`text-[9px] uppercase ${selection.kind === 'slide' && selection.activityIndex === activityIndex && selection.slideIndex === slideIndex ? 'text-indigo-200' : 'text-gray-400'}`}>{slideTypeLabels[slide.slide_type]}</span></button>{canEdit && <div className="hidden pr-1 group-hover:flex"><IconButton title="Dupliquer" onClick={() => duplicateSlide(activityIndex, slideIndex)}><Copy className="h-3 w-3" /></IconButton><IconButton title="Supprimer" danger onClick={() => removeSlide(activityIndex, slideIndex)}><Trash2 className="h-3 w-3" /></IconButton></div>}</div>)}{canEdit && <button onClick={() => addSlide(activityIndex)} className="mt-1 flex w-full items-center justify-center gap-1 rounded-lg border border-dashed border-indigo-200 py-2 text-[11px] font-bold text-indigo-600 hover:bg-indigo-50"><Plus className="h-3.5 w-3.5" /> Ajouter une diapo</button>}</div>}</div>;
                  })}
                  {canEdit && <button onClick={addActivity} className="flex w-full items-center justify-center gap-2 rounded-xl border border-dashed border-indigo-300 py-3 text-xs font-bold text-indigo-600 hover:bg-indigo-50"><Plus className="h-4 w-4" /> Ajouter une activité</button>}
                </div>
              </div>

              <div className="min-w-0 border-gray-200 2xl:border-r">
                <div className="max-h-[650px] overflow-y-auto p-4 sm:p-5">
                  {selection.kind === 'course' && (
                    <div className="space-y-5"><div><h4 className="text-lg font-bold text-gray-900">Paramètres du cours</h4><p className="text-sm text-gray-500">Identité, carte du catalogue et expressions reconnues par le tuteur.</p></div><div><label className={labelClass}>Titre du cours</label><input disabled={!canEdit} className={fieldClass} value={deck.title} onChange={event => mutate(next => { next.title = event.target.value; })} /></div><div className="grid grid-cols-2 gap-3"><div><label className={labelClass}>Langue principale</label><select disabled={!canEdit} className={fieldClass} value={deck.language} onChange={event => mutate(next => { next.language = event.target.value; })}><option value="fr">Français</option><option value="mixed">Darija</option><option value="ar">Arabe</option></select></div><div><label className={labelClass}>Durée totale estimée</label><input disabled={!canEdit} type="number" min={1} className={fieldClass} value={deck.estimated_minutes} onChange={event => mutate(next => { next.estimated_minutes = Number(event.target.value); })} /></div></div><div><label className={labelClass}>Résumé dans le catalogue</label><textarea disabled={!canEdit} rows={3} className={fieldClass} value={deck.catalog.summary || ''} onChange={event => mutate(next => { next.catalog.summary = event.target.value; })} /></div><div><label className={labelClass}>Image de couverture persistante</label><div className="flex gap-2"><input disabled={!canEdit} list="admin-course-images" className={fieldClass} value={deck.catalog.cover_image || ''} onChange={event => mutate(next => { next.catalog.cover_image = event.target.value; })} /><label className={`${buttonClass} cursor-pointer border border-gray-200 bg-white text-gray-700 hover:bg-gray-50 ${!canEdit ? 'pointer-events-none opacity-50' : ''}`}><Upload className="h-4 w-4" /><input type="file" accept="image/png,image/jpeg,image/webp,image/gif" className="hidden" onChange={async event => { const file = event.target.files?.[0]; if (!file) return; const url = await uploadMedia(file); if (url) mutate(next => { next.catalog.cover_image = url; }); event.target.value = ''; }} /></label></div></div><div><label className={labelClass}>Texte alternatif de la couverture</label><input disabled={!canEdit} className={fieldClass} value={deck.catalog.cover_alt || ''} onChange={event => mutate(next => { next.catalog.cover_alt = event.target.value; })} /></div><div><label className={labelClass}>Notions essentielles (une par ligne)</label><textarea disabled={!canEdit} rows={4} className={fieldClass} value={(deck.catalog.essential_topics || []).join('\n')} onChange={event => mutate(next => { next.catalog.essential_topics = event.target.value.split('\n').map(value => value.trim()).filter(Boolean); })} /></div><div><label className={labelClass}>Demandes reconnues par le tuteur (une par ligne)</label><textarea disabled={!canEdit} rows={5} className={fieldClass} value={deck.intent_aliases.join('\n')} onChange={event => mutate(next => { next.intent_aliases = event.target.value.split('\n').map(value => value.trim()).filter(Boolean); })} /><p className="mt-1 text-xs text-gray-400">Ex. « cours sur les ondes », « apprendre la célérité ».</p></div><div><label className={labelClass}>Correspondance avec la leçon (une expression par ligne)</label><textarea disabled={!canEdit} rows={3} className={fieldClass} value={deck.lesson_match.join('\n')} onChange={event => mutate(next => { next.lesson_match = event.target.value.split('\n').map(value => value.trim()).filter(Boolean); })} /></div></div>
                  )}

                  {selection.kind === 'activity' && selectedActivity && (
                    <div className="space-y-5"><div className="flex items-start justify-between gap-3"><div><h4 className="text-lg font-bold text-gray-900">Activité {selection.activityIndex + 1}</h4><p className="text-sm text-gray-500">Durée, phase pédagogique et objectifs.</p></div>{canEdit && <div className="flex"><IconButton title="Dupliquer l'activité" onClick={() => duplicateActivity(selection.activityIndex)}><Copy className="h-4 w-4" /></IconButton><IconButton title="Supprimer l'activité" danger onClick={() => removeActivity(selection.activityIndex)}><Trash2 className="h-4 w-4" /></IconButton></div>}</div><div><label className={labelClass}>Titre</label><input disabled={!canEdit} className={fieldClass} value={selectedActivity.title} onChange={event => mutate(next => { next.activities[selection.activityIndex].title = event.target.value; })} /></div><div className="grid grid-cols-2 gap-3"><div><label className={labelClass}>Phase pédagogique</label><select disabled={!canEdit} className={fieldClass} value={selectedActivity.phase || 'explanation'} onChange={event => mutate(next => { next.activities[selection.activityIndex].phase = event.target.value; })}><option value="diagnostic">Diagnostic</option><option value="investigation">Investigation</option><option value="explanation">Explicitation</option><option value="training">Entraînement</option><option value="synthesis">Synthèse</option><option value="evaluation">Évaluation</option></select></div><div><label className={labelClass}>Durée (minutes)</label><input disabled={!canEdit} type="number" min={1} max={180} className={fieldClass} value={selectedActivity.duration_minutes || 15} onChange={event => mutate(next => { next.activities[selection.activityIndex].duration_minutes = Number(event.target.value); })} /></div></div><div><label className={labelClass}>Objectifs / compétences (un identifiant par ligne)</label><textarea disabled={!canEdit} rows={6} className={fieldClass} value={(selectedActivity.objective_ids || []).join('\n')} onChange={event => mutate(next => { next.activities[selection.activityIndex].objective_ids = event.target.value.split('\n').map(value => value.trim()).filter(Boolean); })} /></div><div className="rounded-xl border border-indigo-100 bg-indigo-50 p-4"><div className="flex items-center justify-between"><div><p className="text-sm font-bold text-indigo-900">{selectedActivity.slides.length} diapositives</p><p className="text-xs text-indigo-600">Ajoutez, dupliquez ou réordonnez depuis la colonne de gauche.</p></div>{canEdit && <button onClick={() => addSlide(selection.activityIndex)} className={`${buttonClass} bg-indigo-600 text-white hover:bg-indigo-700`}><Plus className="h-4 w-4" /> Diapo</button>}</div></div></div>
                  )}

                  {selection.kind === 'slide' && selectedSlide && (
                    <div className="space-y-5"><div><div className="flex items-center justify-between gap-3"><div><h4 className="text-lg font-bold text-gray-900">Diapositive {selection.slideIndex + 1}</h4><p className="text-sm text-gray-500">{selectedActivity?.title}</p></div><div className="flex"><IconButton title="Ouvrir l'aperçu" onClick={() => setPreviewOpen(true)}><Eye className="h-4 w-4" /></IconButton>{canEdit && <><IconButton title="Monter" disabled={selection.slideIndex === 0} onClick={() => moveSlide(selection.activityIndex, selection.slideIndex, -1)}><ArrowUp className="h-4 w-4" /></IconButton><IconButton title="Descendre" disabled={selection.slideIndex === (selectedActivity?.slides.length || 0) - 1} onClick={() => moveSlide(selection.activityIndex, selection.slideIndex, 1)}><ArrowDown className="h-4 w-4" /></IconButton><IconButton title="Dupliquer" onClick={() => duplicateSlide(selection.activityIndex, selection.slideIndex)}><Copy className="h-4 w-4" /></IconButton><IconButton title="Supprimer" danger onClick={() => removeSlide(selection.activityIndex, selection.slideIndex)}><Trash2 className="h-4 w-4" /></IconButton></>}</div></div><div className="mt-4 grid grid-cols-[150px_minmax(0,1fr)] gap-3"><select disabled={!canEdit} className={fieldClass} value={selectedSlide.slide_type} onChange={event => mutate(next => { next.activities[selection.activityIndex].slides[selection.slideIndex].slide_type = event.target.value as CourseSlideType; })}>{Object.entries(slideTypeLabels).map(([value, label]) => <option key={value} value={value}>{label}</option>)}</select><input disabled={!canEdit} className={fieldClass} value={selectedSlide.title} onChange={event => mutate(next => { next.activities[selection.activityIndex].slides[selection.slideIndex].title = event.target.value; })} /></div></div>
                      <div className="flex gap-1 overflow-x-auto rounded-xl bg-gray-100 p-1">{([['content', FileText, 'Contenu'], ['tts', Languages, 'Speech TTS'], ['question', MessageSquareText, 'Question'], ['visual', ImageIcon, 'Visuel'], ['timing', Clock3, 'Timing']] as const).map(([key, Icon, label]) => <button key={key} onClick={() => setPanel(key)} className={`flex min-w-max flex-1 items-center justify-center gap-1.5 rounded-lg px-2 py-2 text-xs font-bold transition ${panel === key ? 'bg-white text-indigo-700 shadow-sm' : 'text-gray-500 hover:text-gray-800'}`}><Icon className="h-3.5 w-3.5" /> {label}</button>)}</div>

                      {panel === 'content' && <div className="space-y-4"><div><label className={labelClass}>Accroche / consigne</label><textarea disabled={!canEdit} rows={3} className={fieldClass} value={selectedSlide.screen_content?.lead || ''} onChange={event => mutate(next => { next.activities[selection.activityIndex].slides[selection.slideIndex].screen_content = { ...next.activities[selection.activityIndex].slides[selection.slideIndex].screen_content, lead: event.target.value }; })} /></div><div><label className={labelClass}>Puces (une par ligne)</label><textarea disabled={!canEdit} rows={5} className={fieldClass} value={(selectedSlide.screen_content?.bullets || []).join('\n')} onChange={event => mutate(next => { const slide = next.activities[selection.activityIndex].slides[selection.slideIndex]; slide.screen_content = { ...slide.screen_content, bullets: event.target.value.split('\n').map(value => value.trim()).filter(Boolean) }; })} /></div><div><label className={labelClass}>Texte essentiel affiché</label><textarea disabled={!canEdit} rows={3} className={fieldClass} value={selectedSlide.screen_content?.essential_text || ''} onChange={event => mutate(next => { const slide = next.activities[selection.activityIndex].slides[selection.slideIndex]; slide.screen_content = { ...slide.screen_content, essential_text: event.target.value }; })} /></div><div><label className={labelClass}>Trace écrite de l’élève</label><textarea disabled={!canEdit} rows={4} className={fieldClass} value={selectedSlide.screen_content?.student_trace || ''} onChange={event => mutate(next => { const slide = next.activities[selection.activityIndex].slides[selection.slideIndex]; slide.screen_content = { ...slide.screen_content, student_trace: event.target.value }; })} /></div></div>}

                      {panel === 'tts' && <div className="space-y-5"><div className="rounded-xl border border-blue-100 bg-blue-50 p-3 text-xs text-blue-800"><div className="flex gap-2"><Volume2 className="h-4 w-4 flex-none" /><p>Le speech est généré seulement lorsque l’élève atteint la diapositive. Une modification crée une nouvelle clé de cache ; l’ancien audio n’est jamais régénéré ni supprimé automatiquement.</p></div></div><div><div className="mb-1.5 flex items-center justify-between"><label className={labelClass.replace('mb-1.5 ', '')}>Speech français</label><span className="text-xs text-gray-400">{(selectedSlide.speech_text?.fr || '').length} caractères</span></div><textarea disabled={!canEdit} rows={8} className={fieldClass} value={selectedSlide.speech_text?.fr || ''} onChange={event => mutate(next => { const slide = next.activities[selection.activityIndex].slides[selection.slideIndex]; slide.speech_text = { ...slide.speech_text, fr: event.target.value }; })} /></div><div><div className="mb-1.5 flex items-center justify-between"><label className={labelClass.replace('mb-1.5 ', '')}>Speech Darija</label><span className="text-xs text-gray-400">{(selectedSlide.speech_text?.mixed || '').length} caractères</span></div><textarea disabled={!canEdit} dir="auto" rows={8} className={`${fieldClass} text-base leading-7`} value={selectedSlide.speech_text?.mixed || ''} onChange={event => mutate(next => { const slide = next.activities[selection.activityIndex].slides[selection.slideIndex]; slide.speech_text = { ...slide.speech_text, mixed: event.target.value }; })} /></div><div><h5 className="mb-2 flex items-center gap-2 text-sm font-bold text-gray-900"><FileAudio className="h-4 w-4" /> Audios batch conservés</h5>{!selectedSlide.audio_assets?.length ? <p className="rounded-xl border border-dashed p-4 text-center text-xs text-gray-400">Aucun audio batch lié. Le TTS à la demande utilisera le cache persistant.</p> : <div className="space-y-2">{selectedSlide.audio_assets.map(audio => <div key={audio.id} className="rounded-xl border p-3"><div className="flex flex-wrap items-center gap-2"><span className="rounded bg-gray-100 px-2 py-1 text-xs font-bold uppercase">{audio.language}</span><span className="text-xs text-gray-500">v{audio.version} · {audio.provider || 'provider'} · {audio.status}</span>{audio.file_path && <audio controls preload="none" src={audio.file_path} className="h-8 min-w-52 flex-1" />}</div>{canEdit && <div className="mt-2 flex gap-2"><button onClick={async () => { await updateAdminCourseAudio(audio.id, 'published'); await loadCourse(deck.ref); }} className="text-xs font-bold text-emerald-700">Publier cet audio</button><button onClick={async () => { await updateAdminCourseAudio(audio.id, 'rejected'); await loadCourse(deck.ref); }} className="text-xs font-bold text-red-600">Rejeter</button></div>}</div>)}</div>}</div></div>}

                      {panel === 'question' && <div className="space-y-4"><div><label className={labelClass}>Type de question</label><select disabled={!canEdit} className={fieldClass} value={selectedSlide.question?.type || 'open'} onChange={event => mutate(next => { const slide = next.activities[selection.activityIndex].slides[selection.slideIndex]; slide.question = { ...slide.question, type: event.target.value as EditorQuestion['type'] }; })}>{questionTypes.map(([value, label]) => <option key={value} value={value}>{label}</option>)}</select></div><div><label className={labelClass}>Question affichée</label><textarea disabled={!canEdit} rows={3} className={fieldClass} value={selectedSlide.question?.prompt || ''} onChange={event => mutate(next => { const slide = next.activities[selection.activityIndex].slides[selection.slideIndex]; slide.question = { ...slide.question, prompt: event.target.value }; })} /></div><div><label className={labelClass}>Choix proposés (un par ligne)</label><textarea disabled={!canEdit} rows={5} className={fieldClass} value={(selectedSlide.question?.options || []).join('\n')} onChange={event => mutate(next => { const slide = next.activities[selection.activityIndex].slides[selection.slideIndex]; slide.question = { ...slide.question, options: event.target.value.split('\n').map(value => value.trim()).filter(Boolean) }; })} /></div><div><label className={labelClass}>Réponse attendue (invisible pour l’élève)</label><input disabled={!canEdit} className={fieldClass} value={typeof selectedSlide.question?.answer_key === 'string' ? selectedSlide.question.answer_key : (selectedSlide.question?.answer_key || []).join(' → ')} onChange={event => mutate(next => { const slide = next.activities[selection.activityIndex].slides[selection.slideIndex]; slide.question = { ...slide.question, answer_key: event.target.value }; })} /></div><div><label className={labelClass}>Réponses ouvertes acceptées (une par ligne)</label><textarea disabled={!canEdit} rows={3} className={fieldClass} value={(selectedSlide.question?.accepted_answers || []).join('\n')} onChange={event => mutate(next => { const slide = next.activities[selection.activityIndex].slides[selection.slideIndex]; slide.question = { ...slide.question, accepted_answers: event.target.value.split('\n').map(value => value.trim()).filter(Boolean) }; })} /></div><div className="grid grid-cols-2 gap-3"><div><label className={labelClass}>Feedback correct</label><textarea disabled={!canEdit} rows={3} className={fieldClass} value={selectedSlide.question?.feedback_correct || ''} onChange={event => mutate(next => { const slide = next.activities[selection.activityIndex].slides[selection.slideIndex]; slide.question = { ...slide.question, feedback_correct: event.target.value }; })} /></div><div><label className={labelClass}>Feedback à reprendre</label><textarea disabled={!canEdit} rows={3} className={fieldClass} value={selectedSlide.question?.feedback_incorrect || ''} onChange={event => mutate(next => { const slide = next.activities[selection.activityIndex].slides[selection.slideIndex]; slide.question = { ...slide.question, feedback_incorrect: event.target.value }; })} /></div></div><div className="grid grid-cols-2 gap-3"><div><label className={labelClass}>Temps de réponse (s)</label><input disabled={!canEdit} type="number" min={5} max={180} className={fieldClass} value={selectedSlide.question?.timeout_seconds || 15} onChange={event => mutate(next => { const slide = next.activities[selection.activityIndex].slides[selection.slideIndex]; slide.question = { ...slide.question, timeout_seconds: Number(event.target.value) }; })} /></div><label className="mt-6 flex items-center gap-2 rounded-xl border p-3 text-sm font-medium text-gray-700"><input disabled={!canEdit} type="checkbox" checked={selectedSlide.question?.advance_on_timeout !== false} onChange={event => mutate(next => { const slide = next.activities[selection.activityIndex].slides[selection.slideIndex]; slide.question = { ...slide.question, advance_on_timeout: event.target.checked }; })} /> Passer automatiquement sans réponse</label></div></div>}

                      {panel === 'visual' && <div className="space-y-4"><div><label className={labelClass}>Type de visuel</label><select disabled={!canEdit} className={fieldClass} value={selectedSlide.visual?.kind || 'none'} onChange={event => mutate(next => { const slide = next.activities[selection.activityIndex].slides[selection.slideIndex]; const kind = event.target.value as VisualKind; slide.visual = { kind, caption: slide.visual?.caption || '', alt: slide.visual?.alt || '', ...(kind === 'scientific' ? { scientific: { engine: 'jsxgraph', title: slide.title, boundingBox: [-5, 5, 5, -5], axis: true, grid: false, elements: [{ type: 'point', points: [{ x: 0, y: 0 }], label: 'A', color: 'cyan' }] } as ScientificVisualSpec } : {}) }; })}><option value="none">Aucun</option><option value="image">Image persistante</option><option value="schema">Schéma validé</option><option value="simulation">Simulation HTML</option><option value="scientific">Figure déclarative</option></select></div>{selectedSlide.visual?.kind === 'image' && <div><label className={labelClass}>Image</label><div className="flex gap-2"><input disabled={!canEdit} list="admin-course-images" className={fieldClass} value={selectedSlide.visual.url || ''} onChange={event => mutate(next => { next.activities[selection.activityIndex].slides[selection.slideIndex].visual = { ...next.activities[selection.activityIndex].slides[selection.slideIndex].visual, url: event.target.value }; })} /><label className={`${buttonClass} cursor-pointer border border-gray-200 bg-white text-gray-700 ${!canEdit ? 'pointer-events-none opacity-50' : ''}`}><Upload className="h-4 w-4" /><input type="file" accept="image/png,image/jpeg,image/webp,image/gif" className="hidden" onChange={async event => { const file = event.target.files?.[0]; if (!file) return; const url = await uploadMedia(file); if (url) mutate(next => { next.activities[selection.activityIndex].slides[selection.slideIndex].visual = { ...next.activities[selection.activityIndex].slides[selection.slideIndex].visual, url }; }); event.target.value = ''; }} /></label></div></div>}{selectedSlide.visual?.kind === 'simulation' && <div><label className={labelClass}>Simulation existante</label><input disabled={!canEdit} list="admin-course-simulations" className={fieldClass} value={selectedSlide.visual.url || ''} onChange={event => mutate(next => { next.activities[selection.activityIndex].slides[selection.slideIndex].visual = { ...next.activities[selection.activityIndex].slides[selection.slideIndex].visual, url: event.target.value }; })} /><p className="mt-1 text-xs text-gray-400">Seules les simulations persistantes sous /media/ sont autorisées.</p></div>}{selectedSlide.visual?.kind === 'schema' && <div><label className={labelClass}>Schéma du registre BAC</label><select disabled={!canEdit} className={fieldClass} value={selectedSlide.visual.schema_id || ''} onChange={event => mutate(next => { next.activities[selection.activityIndex].slides[selection.slideIndex].visual = { ...next.activities[selection.activityIndex].slides[selection.slideIndex].visual, schema_id: event.target.value }; })}><option value="">Choisir un schéma…</option>{options.schemas.map(schemaOption => <option key={schemaOption.id} value={schemaOption.id}>{schemaOption.subject} · {schemaOption.title}</option>)}</select></div>}{selectedSlide.visual?.kind === 'scientific' && <ScientificJsonEditor disabled={!canEdit} value={selectedSlide.visual.scientific} onChange={scientific => mutate(next => { next.activities[selection.activityIndex].slides[selection.slideIndex].visual = { ...next.activities[selection.activityIndex].slides[selection.slideIndex].visual, scientific }; })} />}<div><label className={labelClass}>Légende</label><input disabled={!canEdit} className={fieldClass} value={selectedSlide.visual?.caption || ''} onChange={event => mutate(next => { next.activities[selection.activityIndex].slides[selection.slideIndex].visual = { ...next.activities[selection.activityIndex].slides[selection.slideIndex].visual, caption: event.target.value }; })} /></div><div><label className={labelClass}>Texte alternatif accessible</label><textarea disabled={!canEdit} rows={3} className={fieldClass} value={selectedSlide.visual?.alt || ''} onChange={event => mutate(next => { next.activities[selection.activityIndex].slides[selection.slideIndex].visual = { ...next.activities[selection.activityIndex].slides[selection.slideIndex].visual, alt: event.target.value }; })} /></div><label className="flex items-center gap-2 rounded-xl border p-3 text-sm font-medium text-gray-700"><input disabled={!canEdit} type="checkbox" checked={selectedSlide.visual?.required_interaction === true} onChange={event => mutate(next => { next.activities[selection.activityIndex].slides[selection.slideIndex].visual = { ...next.activities[selection.activityIndex].slides[selection.slideIndex].visual, required_interaction: event.target.checked }; })} /> Interaction obligatoire avant la question</label></div>}

                      {panel === 'timing' && <div className="space-y-4"><div className="grid grid-cols-2 gap-3"><div><label className={labelClass}>Lecture de secours (s)</label><input disabled={!canEdit} type="number" min={1} max={300} className={fieldClass} value={selectedSlide.timing?.reading_seconds || 12} onChange={event => mutate(next => { const slide = next.activities[selection.activityIndex].slides[selection.slideIndex]; slide.timing = { ...slide.timing, reading_seconds: Number(event.target.value) }; })} /></div><div><label className={labelClass}>Délai après feedback (ms)</label><input disabled={!canEdit} type="number" min={0} max={10000} step={100} className={fieldClass} value={selectedSlide.timing?.delay_after_feedback_ms || 900} onChange={event => mutate(next => { const slide = next.activities[selection.activityIndex].slides[selection.slideIndex]; slide.timing = { ...slide.timing, delay_after_feedback_ms: Number(event.target.value) }; })} /></div></div><label className="flex items-center gap-2 rounded-xl border p-3 text-sm font-medium text-gray-700"><input disabled={!canEdit} type="checkbox" checked={selectedSlide.timing?.auto_advance !== false} onChange={event => mutate(next => { const slide = next.activities[selection.activityIndex].slides[selection.slideIndex]; slide.timing = { ...slide.timing, auto_advance: event.target.checked }; })} /> Autoriser l’enchaînement automatique</label><div className="rounded-xl border border-amber-100 bg-amber-50 p-3 text-xs leading-5 text-amber-800">Le temps de réponse à la question est réglé dans l’onglet « Question ». Si l’élève ne répond pas et que « passage automatique » est actif, la diapositive suivante démarre sans bloquer le cours.</div></div>}
                    </div>
                  )}
                </div>
              </div>

              <div className="hidden bg-slate-100/80 p-4 2xl:block"><div className="sticky top-4"><div className="mb-3 flex items-center justify-between"><h4 className="flex items-center gap-2 text-sm font-bold text-gray-800"><Eye className="h-4 w-4" /> Aperçu élève</h4>{selectedSlide && <span className="text-xs text-gray-400">{selection.kind === 'slide' ? `${selection.slideIndex + 1}/${selectedActivity?.slides.length}` : ''}</span>}</div>{selectedSlide ? <SlidePreview slide={selectedSlide} /> : <div className="rounded-2xl border border-dashed border-gray-300 bg-white p-8 text-center text-sm text-gray-400">Sélectionnez une diapositive pour afficher son rendu.</div>}</div></div>
            </div>
          </main>
        )}
      </div>

      <datalist id="admin-course-images">{options.media.images.map(url => <option key={url} value={url} />)}</datalist>
      <datalist id="admin-course-simulations">{options.media.simulations.map(url => <option key={url} value={url} />)}</datalist>
      {previewOpen && selectedSlide && <div className="fixed inset-0 z-[80] flex items-center justify-center bg-slate-950/80 p-3 sm:p-8" onClick={() => setPreviewOpen(false)}><div className="max-h-full w-full max-w-5xl overflow-y-auto" onClick={event => event.stopPropagation()}><div className="mb-3 flex items-center justify-between text-white"><div><p className="text-xs uppercase tracking-widest text-cyan-300">Aperçu élève</p><h3 className="font-bold">{selectedSlide.title}</h3></div><button onClick={() => setPreviewOpen(false)} className="rounded-xl bg-white/10 p-2 hover:bg-white/20"><X className="h-5 w-5" /></button></div><SlidePreview slide={selectedSlide} /></div></div>}
      {showCreate && <CreateCourseModal lessons={options.lessons} loading={saving} onClose={() => setShowCreate(false)} onCreate={data => void createCourse(data)} />}
    </div>
  );
}
