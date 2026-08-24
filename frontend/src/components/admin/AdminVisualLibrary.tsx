import { useCallback, useEffect, useMemo, useState } from 'react';
import {
  AlertTriangle,
  Code2,
  Copy,
  Eye,
  FileVideo,
  Image as ImageIcon,
  LibraryBig,
  LoaderCircle,
  Pencil,
  Plus,
  RefreshCw,
  Save,
  Search,
  ShieldCheck,
  Sparkles,
  Trash2,
  Upload,
  X,
} from 'lucide-react';
import type { AxiosError } from 'axios';
import {
  createAdminVisualItem,
  deleteAdminVisualItem,
  generateAdminVisual,
  getAdminVisualLibrary,
  getAdminVisualPreviewContent,
  updateAdminVisualItem,
  uploadAdminVisualMedia,
} from '../../services/api';
import type {
  AdminVisualItemPayload,
  AdminVisualLibraryItem,
  AdminVisualLibraryResponse,
  AdminVisualLesson,
  AdminVisualStatus,
} from '../../services/api';
import SVGSchemaViewer from '../session/schemas/SVGSchemaViewer';
import { getSchemaById } from '../session/schemas';
import ScientificVisual from '../session/scientific/ScientificVisual';
import type { ScientificVisualSpec } from '../session/scientific/types';


const KIND_LABELS: Record<string, string> = {
  all: 'Tous les types',
  schema: 'Schémas validés',
  preset: 'Scènes contrôlables',
  scientific: 'Figures interactives et 3D',
  image: 'Images',
  video: 'Vidéos',
  simulation: 'Simulations HTML',
};

const STATUS_LABELS: Record<string, string> = {
  all: 'Tous les statuts',
  draft: 'Brouillon',
  validated: 'Validé',
  published: 'Publié',
  archived: 'Archivé',
};

const fieldClass = 'w-full rounded-xl border border-gray-300 bg-white px-3 py-2.5 text-sm outline-none transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 disabled:bg-gray-100';
const labelClass = 'mb-1.5 block text-xs font-bold uppercase tracking-wide text-gray-500';

function errorMessage(error: unknown): string {
  const response = (error as AxiosError<{ detail?: string | { message?: string } }>)?.response;
  const detail = response?.data?.detail;
  if (typeof detail === 'string') return detail;
  if (detail && typeof detail === 'object' && typeof detail.message === 'string') return detail.message;
  return error instanceof Error ? error.message : 'Une erreur est survenue.';
}

function kindIcon(kind: string) {
  if (kind === 'image') return <ImageIcon className="h-4 w-4" />;
  if (kind === 'video') return <FileVideo className="h-4 w-4" />;
  if (kind === 'scientific') return <Code2 className="h-4 w-4" />;
  if (kind === 'schema' || kind === 'preset') return <Sparkles className="h-4 w-4" />;
  return <LibraryBig className="h-4 w-4" />;
}

function statusClass(status: string) {
  if (status === 'published') return 'bg-emerald-50 text-emerald-700 ring-emerald-200';
  if (status === 'validated') return 'bg-cyan-50 text-cyan-700 ring-cyan-200';
  if (status === 'archived') return 'bg-gray-100 text-gray-500 ring-gray-200';
  return 'bg-amber-50 text-amber-700 ring-amber-200';
}

function canPreviewUrl(url: string, kind: string): boolean {
  if (url.startsWith('/') || /^https?:\/\//i.test(url) || /^blob:/i.test(url)) return true;
  return kind === 'image' && /^data:image\//i.test(url);
}

function UnavailablePreview({ height, message }: { height: string; message: string }) {
  return (
    <div className={`${height} flex flex-col items-center justify-center gap-3 bg-slate-950 px-6 text-center text-slate-300`}>
      <AlertTriangle className="h-8 w-8 text-amber-400" />
      <div>
        <div className="text-sm font-bold text-white">Aperçu indisponible</div>
        <p className="mt-1 max-w-lg text-xs leading-5 text-slate-400">{message}</p>
      </div>
    </div>
  );
}

function VisualPreview({ item, full = false }: { item: AdminVisualLibraryItem; full?: boolean }) {
  const preview = item.preview || { kind: item.kind };
  const schema = preview.schema_id ? getSchemaById(preview.schema_id) : undefined;
  const height = full ? 'min-h-[420px] h-[58vh]' : 'h-44';
  const [failedUrl, setFailedUrl] = useState('');
  const [inlinePreview, setInlinePreview] = useState<{
    itemId: string;
    html?: string;
    error?: string;
  }>({ itemId: item.id });

  useEffect(() => {
    if (!full || preview.kind !== 'simulation' || !preview.inline_html || !item.resource_id) return;
    let active = true;
    void getAdminVisualPreviewContent(item.resource_id)
      .then(response => {
        if (active) setInlinePreview({ itemId: item.id, html: response.data.html });
      })
      .catch(error => {
        if (active) setInlinePreview({ itemId: item.id, error: errorMessage(error) });
      });
    return () => { active = false; };
  }, [full, item.id, item.resource_id, preview.inline_html, preview.kind]);

  if (schema) {
    return (
      <div className={`${height} overflow-hidden bg-[#071323] p-1`}>
        <SVGSchemaViewer schema={schema} autoAnimate={false} handDrawn className="h-full w-full" />
      </div>
    );
  }
  if (preview.kind === 'scientific' && preview.scientific) {
    return (
      <div className={`${height} overflow-hidden bg-[#071323] p-2`}>
        <ScientificVisual spec={preview.scientific as unknown as ScientificVisualSpec} />
      </div>
    );
  }
  if (preview.kind === 'image' && preview.url) {
    if (!canPreviewUrl(preview.url, 'image') || failedUrl === preview.url) {
      return <UnavailablePreview height={height} message="Le fichier image est absent, inaccessible ou utilise une adresse non prise en charge." />;
    }
    return (
      <img
        src={preview.url}
        alt={item.title}
        className={`${height} w-full bg-slate-100 object-contain`}
        loading="lazy"
        onError={() => setFailedUrl(preview.url || '')}
      />
    );
  }
  if (!full && preview.kind === 'simulation' && preview.poster_url) {
    if (!canPreviewUrl(preview.poster_url, 'image') || failedUrl === preview.poster_url) {
      return <UnavailablePreview height={height} message="La miniature de cette simulation est indisponible." />;
    }
    return (
      <div className={`${height} relative overflow-hidden bg-slate-950`}>
        <img
          src={preview.poster_url}
          alt={item.title}
          className="h-full w-full object-contain"
          loading="lazy"
          onError={() => setFailedUrl(preview.poster_url || '')}
        />
        <span className="absolute bottom-3 left-3 rounded-full bg-indigo-600/95 px-3 py-1.5 text-[11px] font-black text-white shadow-lg ring-1 ring-white/30">
          ▶ Animation pas à pas
        </span>
      </div>
    );
  }
  if (full && preview.kind === 'video' && preview.url) {
    if (!canPreviewUrl(preview.url, 'video') || failedUrl === preview.url) {
      return <UnavailablePreview height={height} message="La vidéo est absente ou son adresse ne peut pas être chargée." />;
    }
    return <video src={preview.url} controls className={`${height} w-full bg-black object-contain`} onError={() => setFailedUrl(preview.url || '')} />;
  }
  if (full && preview.kind === 'simulation' && preview.inline_html) {
    if (inlinePreview.itemId === item.id && inlinePreview.error) {
      return <UnavailablePreview height={height} message={inlinePreview.error} />;
    }
    if (inlinePreview.itemId !== item.id || !inlinePreview.html) {
      return <div className={`${height} flex items-center justify-center bg-slate-950 text-sm text-slate-300`}><LoaderCircle className="mr-2 h-5 w-5 animate-spin" /> Chargement de la simulation…</div>;
    }
    return (
      <iframe
        srcDoc={inlinePreview.html}
        title={item.title}
        className={`${height} w-full bg-white`}
        sandbox="allow-scripts"
        referrerPolicy="no-referrer"
      />
    );
  }
  if (full && preview.kind === 'simulation' && preview.url) {
    if (!canPreviewUrl(preview.url, 'simulation')) {
      return <UnavailablePreview height={height} message="Cette simulation ne possède pas d’adresse HTML valide." />;
    }
    return (
      <iframe
        src={preview.url}
        title={item.title}
        className={`${height} w-full bg-white`}
        sandbox="allow-scripts"
        referrerPolicy="no-referrer"
      />
    );
  }
  if (full && preview.available === false) {
    return <UnavailablePreview height={height} message={preview.reason || "Aucun aperçu n'est associé à cette ressource."} />;
  }
  return (
    <div className={`${height} flex flex-col items-center justify-center gap-2 bg-gradient-to-br from-slate-900 to-slate-800 px-5 text-center text-slate-300`}>
      <span className="rounded-2xl bg-white/10 p-3">{kindIcon(item.kind)}</span>
      <span className="text-xs font-semibold">{KIND_LABELS[item.kind] || item.kind}</span>
      {(preview.kind === 'video' || preview.kind === 'simulation') && (
        <span className="text-[11px] text-slate-500">Ouvrir pour lancer la prévisualisation</span>
      )}
    </div>
  );
}

interface EditorSeed {
  item?: AdminVisualLibraryItem;
  ai: boolean;
  copy: boolean;
}

interface VisualTypeGroup {
  kind: string;
  label: string;
  items: AdminVisualLibraryItem[];
}

const VISUAL_TYPE_ORDER = ['image', 'simulation', 'schema', 'preset', 'scientific', 'video'];

interface EditorForm {
  lesson_id: string;
  kind: 'image' | 'video' | 'simulation' | 'scientific';
  title: string;
  description: string;
  section_title: string;
  file_path: string;
  trigger_text: string;
  phase: string;
  difficulty_tier: string;
  concepts: string;
  status: AdminVisualStatus;
}

function initialForm(seed: EditorSeed): EditorForm {
  const item = seed.item;
  const sourceKind = item?.kind;
  const kind = sourceKind === 'image' || sourceKind === 'video' || sourceKind === 'simulation'
    ? sourceKind
    : 'scientific';
  const isCopy = seed.copy || !item?.editable;
  return {
    lesson_id: isCopy ? '' : item?.lesson_id || '',
    kind,
    title: item ? `${item.title}${isCopy ? ' — version personnalisée' : ''}` : '',
    description: item?.description || '',
    section_title: item?.section_title || 'Bibliothèque visuelle',
    file_path: item?.preview?.url || item?.file_path || item?.external_url || '',
    trigger_text: item?.trigger_text || '',
    phase: item?.phase || 'explanation',
    difficulty_tier: item?.difficulty_tier || 'intermediate',
    concepts: (item?.concepts || []).join(', '),
    status: isCopy ? 'draft' : item?.status || 'draft',
  };
}

function VisualEditorModal({
  seed,
  lessons,
  onClose,
  onSaved,
}: {
  seed: EditorSeed;
  lessons: AdminVisualLesson[];
  onClose: () => void;
  onSaved: () => Promise<void>;
}) {
  const [form, setForm] = useState<EditorForm>(() => initialForm(seed));
  const initialScientific = seed.item?.preview?.scientific;
  const [scientificText, setScientificText] = useState(() => JSON.stringify(initialScientific || {}, null, 2));
  const [prompt, setPrompt] = useState(() => seed.item
    ? `Améliore ce visuel sur « ${seed.item.title} ». Garde uniquement les éléments utiles au cours et des légendes françaises courtes.`
    : '');
  const [engine, setEngine] = useState<'auto' | 'roughsvg' | 'jsxgraph' | 'cytoscape' | 'matter' | 'three'>('auto');
  const [quality, setQuality] = useState<{ score: number; issues: string[]; acceptable: boolean } | null>(seed.item?.quality || null);
  const [existingMatch, setExistingMatch] = useState<{ id: string; title: string } | null>(null);
  const [file, setFile] = useState<File | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const editingResource = Boolean(seed.item?.editable && !seed.copy && seed.item.resource_id);
  const selectedLesson = lessons.find(item => item.id === form.lesson_id);

  const generate = async () => {
    if (prompt.trim().length < 8) {
      setError('Décrivez le visuel attendu avec un peu plus de précision.');
      return;
    }
    setBusy(true);
    setError('');
    try {
      let currentSpec: Record<string, unknown> | undefined;
      if (editingResource && seed.item?.kind === 'scientific') {
        currentSpec = JSON.parse(scientificText) as Record<string, unknown>;
      }
      const response = await generateAdminVisual({
        prompt,
        subject: selectedLesson?.subject_name || seed.item?.subject || '',
        lesson_id: form.lesson_id || undefined,
        title: form.title || undefined,
        engine,
        mode: currentSpec ? 'edit' : 'create',
        current_spec: currentSpec,
      });
      setForm(previous => ({
        ...previous,
        kind: 'scientific',
        title: response.data.title || previous.title,
        description: response.data.description || previous.description,
      }));
      setScientificText(JSON.stringify(response.data.scientific, null, 2));
      setQuality(response.data.quality);
      setExistingMatch(response.data.existing_match || null);
    } catch (err) {
      setError(errorMessage(err));
    } finally {
      setBusy(false);
    }
  };

  const save = async () => {
    if (!form.lesson_id || !form.title.trim()) {
      setError('La leçon et le titre sont obligatoires.');
      return;
    }
    setBusy(true);
    setError('');
    try {
      let filePath = form.file_path.trim() || null;
      if (file && (form.kind === 'image' || form.kind === 'video')) {
        const uploaded = await uploadAdminVisualMedia(file, form.kind, form.lesson_id);
        filePath = uploaded.data.file_path;
      }
      const payload: AdminVisualItemPayload = {
        lesson_id: form.lesson_id,
        kind: form.kind,
        title: form.title.trim(),
        description: form.description.trim(),
        section_title: form.section_title.trim() || 'Bibliothèque visuelle',
        file_path: form.kind === 'scientific' ? null : filePath,
        trigger_text: form.trigger_text.trim() || null,
        phase: form.phase,
        difficulty_tier: form.difficulty_tier,
        concepts: form.concepts.split(',').map(value => value.trim()).filter(Boolean),
        status: form.status,
        source: seed.ai ? 'admin_llm' : 'admin',
      };
      if (form.kind === 'scientific') {
        const parsed = JSON.parse(scientificText) as Record<string, unknown>;
        if (!parsed || Array.isArray(parsed)) throw new Error('Le JSON scientifique doit être un objet.');
        payload.scientific = parsed;
      } else if (!filePath) {
        throw new Error('Ajoutez un fichier ou une URL.');
      }
      if (editingResource && seed.item?.resource_id) {
        await updateAdminVisualItem(seed.item.resource_id, payload);
      } else {
        await createAdminVisualItem(payload);
      }
      await onSaved();
      onClose();
    } catch (err) {
      setError(errorMessage(err));
    } finally {
      setBusy(false);
    }
  };

  const parsedPreview = useMemo(() => {
    if (form.kind !== 'scientific') return null;
    try {
      const parsed = JSON.parse(scientificText) as Record<string, unknown>;
      return parsed && typeof parsed === 'object' && !Array.isArray(parsed) ? parsed : null;
    } catch {
      return null;
    }
  }, [form.kind, scientificText]);

  const previewItem: AdminVisualLibraryItem = {
    id: 'draft-preview', kind: form.kind, title: form.title || 'Aperçu', description: form.description,
    subject: selectedLesson?.subject_name || '', subject_key: '', chapter: selectedLesson?.chapter_title || '',
    lesson: selectedLesson?.title || '', lesson_id: form.lesson_id, concepts: [], source: 'admin', status: form.status,
    editable: true, deletable: true,
    preview: form.kind === 'scientific'
      ? { kind: 'scientific', scientific: parsedPreview || undefined }
      : { kind: form.kind, url: form.file_path || undefined },
  };

  return (
    <div className="fixed inset-0 z-[80] flex items-center justify-center bg-slate-950/70 p-3 backdrop-blur-sm" onMouseDown={onClose}>
      <div className="max-h-[96vh] w-full max-w-7xl overflow-hidden rounded-3xl bg-white shadow-2xl" onMouseDown={event => event.stopPropagation()}>
        <div className="flex items-center justify-between border-b px-5 py-4">
          <div>
            <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-indigo-600">
              {seed.ai ? <Sparkles className="h-4 w-4" /> : <Pencil className="h-4 w-4" />}
              {seed.ai ? 'Atelier LLM sécurisé' : editingResource ? 'Modifier la ressource' : 'Nouvelle ressource'}
            </div>
            <h2 className="mt-1 text-xl font-black text-gray-900">{form.title || 'Créer un visuel pédagogique'}</h2>
          </div>
          <button onClick={onClose} className="rounded-xl p-2 text-gray-400 hover:bg-gray-100 hover:text-gray-700" aria-label="Fermer">
            <X className="h-5 w-5" />
          </button>
        </div>

        <div className="grid max-h-[calc(96vh-76px)] grid-cols-1 overflow-y-auto lg:grid-cols-[minmax(0,1fr)_minmax(420px,0.9fr)] lg:overflow-hidden">
          <div className="space-y-5 overflow-y-auto p-5 lg:max-h-[calc(96vh-76px)]">
            {error && <div className="rounded-xl border border-red-200 bg-red-50 p-3 text-sm text-red-700">{error}</div>}

            {seed.ai && (
              <div className="rounded-2xl border border-indigo-200 bg-indigo-50/60 p-4">
                <div className="mb-3 flex items-center gap-2 font-bold text-indigo-900"><Sparkles className="h-4 w-4" /> Demande au LLM</div>
                <textarea value={prompt} onChange={event => setPrompt(event.target.value)} rows={4} className={fieldClass}
                  placeholder="Ex. Crée une simulation de chute libre avec la hauteur, la vitesse et un réglage de g…" />
                <div className="mt-3 grid gap-3 sm:grid-cols-[1fr_auto]">
                  <select value={engine} onChange={event => setEngine(event.target.value as typeof engine)} className={fieldClass}>
                    <option value="auto">Moteur automatique</option>
                    <option value="roughsvg">RoughSVG — schéma/croquis</option>
                    <option value="jsxgraph">JSXGraph — courbe/forces</option>
                    <option value="cytoscape">Cytoscape — réseau/processus</option>
                    <option value="matter">Matter.js — mécanique</option>
                    <option value="three">Modèle 3D réaliste — mitochondrie</option>
                  </select>
                  <button onClick={generate} disabled={busy} className="flex items-center justify-center gap-2 rounded-xl bg-indigo-600 px-5 py-2.5 text-sm font-bold text-white hover:bg-indigo-700 disabled:opacity-50">
                    {busy ? <LoaderCircle className="h-4 w-4 animate-spin" /> : <Sparkles className="h-4 w-4" />} Générer
                  </button>
                </div>
                {existingMatch && (
                  <div className="mt-3 rounded-xl border border-cyan-200 bg-cyan-50 p-3 text-xs text-cyan-900">
                    Un schéma validé couvre peut-être déjà cette demande : <strong>{existingMatch.title}</strong> ({existingMatch.id}).
                  </div>
                )}
              </div>
            )}

            <div className="grid gap-4 sm:grid-cols-2">
              <div className="sm:col-span-2">
                <label className={labelClass}>Leçon de destination *</label>
                <select value={form.lesson_id} onChange={event => setForm(previous => ({ ...previous, lesson_id: event.target.value }))} className={fieldClass}>
                  <option value="">Sélectionner une matière, un chapitre et une leçon</option>
                  {lessons.map(lesson => (
                    <option key={lesson.id} value={lesson.id}>{lesson.subject_name} · {lesson.chapter_title} · {lesson.title}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className={labelClass}>Type</label>
                <select value={form.kind} onChange={event => setForm(previous => ({ ...previous, kind: event.target.value as EditorForm['kind'] }))} className={fieldClass}>
                  <option value="scientific">Visuel scientifique déclaratif</option>
                  <option value="image">Image</option>
                  <option value="video">Vidéo</option>
                  <option value="simulation">Simulation HTML</option>
                </select>
              </div>
              <div>
                <label className={labelClass}>Statut</label>
                <select value={form.status} onChange={event => setForm(previous => ({ ...previous, status: event.target.value as AdminVisualStatus }))} className={fieldClass}>
                  <option value="draft">Brouillon</option>
                  <option value="validated">Validé</option>
                  <option value="published">Publié</option>
                  <option value="archived">Archivé</option>
                </select>
              </div>
              <div className="sm:col-span-2">
                <label className={labelClass}>Titre *</label>
                <input value={form.title} onChange={event => setForm(previous => ({ ...previous, title: event.target.value }))} className={fieldClass} />
              </div>
              <div className="sm:col-span-2">
                <label className={labelClass}>Description pédagogique</label>
                <textarea value={form.description} onChange={event => setForm(previous => ({ ...previous, description: event.target.value }))} rows={3} className={fieldClass} />
              </div>
              <div>
                <label className={labelClass}>Section</label>
                <input value={form.section_title} onChange={event => setForm(previous => ({ ...previous, section_title: event.target.value }))} className={fieldClass} />
              </div>
              <div>
                <label className={labelClass}>Phase pédagogique</label>
                <select value={form.phase} onChange={event => setForm(previous => ({ ...previous, phase: event.target.value }))} className={fieldClass}>
                  <option value="activation">Activation</option><option value="exploration">Exploration</option>
                  <option value="explanation">Explication</option><option value="application">Application</option>
                  <option value="consolidation">Consolidation</option>
                </select>
              </div>
              <div>
                <label className={labelClass}>Niveau</label>
                <select value={form.difficulty_tier} onChange={event => setForm(previous => ({ ...previous, difficulty_tier: event.target.value }))} className={fieldClass}>
                  <option value="beginner">Débutant</option><option value="intermediate">Intermédiaire</option><option value="advanced">Avancé</option>
                </select>
              </div>
              <div>
                <label className={labelClass}>Déclencheur LLM</label>
                <input value={form.trigger_text} onChange={event => setForm(previous => ({ ...previous, trigger_text: event.target.value }))} className={fieldClass} placeholder="Montre la chute libre" />
              </div>
              <div className="sm:col-span-2">
                <label className={labelClass}>Concepts, séparés par des virgules</label>
                <input value={form.concepts} onChange={event => setForm(previous => ({ ...previous, concepts: event.target.value }))} className={fieldClass} />
              </div>
            </div>

            {form.kind === 'scientific' ? (
              <div>
                <div className="mb-2 flex items-center justify-between gap-3">
                  <label className={labelClass}>JSON déclaratif contrôlé</label>
                  {quality && (
                    <span className={`rounded-full px-2.5 py-1 text-xs font-bold ${quality.acceptable ? 'bg-emerald-100 text-emerald-700' : 'bg-amber-100 text-amber-700'}`}>
                      Qualité {quality.score}/100
                    </span>
                  )}
                </div>
                <textarea value={scientificText} onChange={event => { setScientificText(event.target.value); setQuality(null); }} rows={18}
                  className={`${fieldClass} font-mono text-xs`} spellCheck={false} />
                {quality && quality.issues.length > 0 && (
                  <ul className="mt-2 space-y-1 text-xs text-amber-700">
                    {quality.issues.map(issue => <li key={issue}>• {issue}</li>)}
                  </ul>
                )}
                <p className="mt-2 text-xs text-gray-400">JSXGraph, Cytoscape, Matter.js, RoughSVG, Three.js borné ou preset. Aucun code libre, HTML, callback ou URL.</p>
              </div>
            ) : (
              <div className="space-y-3 rounded-2xl border bg-gray-50 p-4">
                <div>
                  <label className={labelClass}>URL ou chemin du média</label>
                  <input value={form.file_path} onChange={event => setForm(previous => ({ ...previous, file_path: event.target.value }))} className={fieldClass} placeholder="/media/… ou https://…" />
                </div>
                {(form.kind === 'image' || form.kind === 'video') && (
                  <label className="flex cursor-pointer items-center justify-center gap-2 rounded-xl border-2 border-dashed border-gray-300 bg-white p-4 text-sm font-semibold text-gray-600 hover:border-indigo-400 hover:text-indigo-600">
                    <Upload className="h-4 w-4" /> {file ? file.name : 'Choisir un fichier (25 Mo max.)'}
                    <input type="file" className="hidden" accept={form.kind === 'image' ? 'image/*' : 'video/*'} onChange={event => setFile(event.target.files?.[0] || null)} />
                  </label>
                )}
              </div>
            )}

            <div className="flex flex-wrap justify-end gap-3 border-t pt-4">
              <button onClick={onClose} className="rounded-xl border px-4 py-2.5 text-sm font-semibold text-gray-600 hover:bg-gray-50">Annuler</button>
              <button onClick={save} disabled={busy || (form.kind === 'scientific' && !parsedPreview)} className="flex items-center gap-2 rounded-xl bg-gray-900 px-5 py-2.5 text-sm font-bold text-white hover:bg-black disabled:opacity-40">
                {busy ? <LoaderCircle className="h-4 w-4 animate-spin" /> : <Save className="h-4 w-4" />} {editingResource ? 'Enregistrer la version' : 'Ajouter à la bibliothèque'}
              </button>
            </div>
          </div>

          <div className="border-l bg-slate-950 p-4 lg:max-h-[calc(96vh-76px)] lg:overflow-y-auto">
            <div className="mb-3 flex items-center justify-between text-xs font-bold uppercase tracking-wider text-slate-400">
              Aperçu réel <Eye className="h-4 w-4" />
            </div>
            <div className="overflow-hidden rounded-2xl border border-slate-700">
              <VisualPreview item={previewItem} full />
            </div>
            <div className="mt-4 rounded-2xl border border-slate-800 bg-slate-900 p-4 text-sm text-slate-300">
              <div className="flex items-center gap-2 font-bold text-white"><ShieldCheck className="h-4 w-4 text-emerald-400" /> Contrat de sécurité</div>
              <p className="mt-2 text-xs leading-5 text-slate-400">La prévisualisation utilise exactement les moteurs du tableau. Le serveur normalise le JSON une seconde fois avant toute sauvegarde.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function DetailModal({ item, onClose, onEdit, onAI, onAttach }: {
  item: AdminVisualLibraryItem;
  onClose: () => void;
  onEdit: () => void;
  onAI: () => void;
  onAttach: () => void;
}) {
  return (
    <div className="fixed inset-0 z-[75] flex items-center justify-center bg-slate-950/75 p-4 backdrop-blur-sm" onMouseDown={onClose}>
      <div className="max-h-[94vh] w-full max-w-6xl overflow-y-auto rounded-3xl bg-white shadow-2xl" onMouseDown={event => event.stopPropagation()}>
        <div className="flex items-start justify-between gap-4 border-b p-5">
          <div>
            <div className="mb-2 flex flex-wrap items-center gap-2">
              <span className="inline-flex items-center gap-1 rounded-full bg-indigo-50 px-2.5 py-1 text-xs font-bold text-indigo-700">{kindIcon(item.kind)} {KIND_LABELS[item.kind] || item.kind}</span>
              <span className={`rounded-full px-2.5 py-1 text-xs font-bold ring-1 ${statusClass(item.status)}`}>{STATUS_LABELS[item.status] || item.status}</span>
              {!item.editable && <span className="inline-flex items-center gap-1 rounded-full bg-gray-100 px-2.5 py-1 text-xs font-bold text-gray-600"><ShieldCheck className="h-3.5 w-3.5" /> Protégé</span>}
            </div>
            <h2 className="text-2xl font-black text-gray-900">{item.title}</h2>
            <p className="mt-1 text-sm text-gray-500">{[item.subject, item.chapter, item.lesson].filter(Boolean).join(' · ') || 'Catalogue transversal'}</p>
          </div>
          <button onClick={onClose} className="rounded-xl p-2 text-gray-400 hover:bg-gray-100"><X className="h-5 w-5" /></button>
        </div>
        <div className="bg-slate-950 p-4"><div className="overflow-hidden rounded-2xl border border-slate-700"><VisualPreview item={item} full /></div></div>
        <div className="space-y-4 p-5">
          {item.description && <p className="text-sm leading-6 text-gray-600">{item.description}</p>}
          {item.concepts.length > 0 && <div className="flex flex-wrap gap-2">{item.concepts.slice(0, 12).map(concept => <span key={concept} className="rounded-full bg-gray-100 px-2.5 py-1 text-xs text-gray-600">{concept}</span>)}</div>}
          <div className="flex flex-wrap justify-end gap-2 border-t pt-4">
            {item.editable && <button onClick={onEdit} className="flex items-center gap-2 rounded-xl border px-4 py-2 text-sm font-bold text-gray-700 hover:bg-gray-50"><Pencil className="h-4 w-4" /> Modifier</button>}
            {(item.kind === 'scientific' || item.kind === 'schema' || item.kind === 'preset') && <button onClick={onAI} className="flex items-center gap-2 rounded-xl bg-indigo-600 px-4 py-2 text-sm font-bold text-white hover:bg-indigo-700"><Sparkles className="h-4 w-4" /> {item.editable ? 'Améliorer avec le LLM' : 'Créer une version avec le LLM'}</button>}
            {!item.editable && (item.kind === 'image' || item.kind === 'simulation') && <button onClick={onAttach} className="flex items-center gap-2 rounded-xl bg-gray-900 px-4 py-2 text-sm font-bold text-white"><Copy className="h-4 w-4" /> Rattacher à une leçon</button>}
          </div>
        </div>
      </div>
    </div>
  );
}

export default function AdminVisualLibrary({ initialLibrary }: { initialLibrary?: AdminVisualLibraryResponse }) {
  const [library, setLibrary] = useState<AdminVisualLibraryResponse | null>(initialLibrary || null);
  const [loading, setLoading] = useState(!initialLibrary);
  const [error, setError] = useState('');
  const [search, setSearch] = useState('');
  const [kind, setKind] = useState('all');
  const [subject, setSubject] = useState('all');
  const [lesson, setLesson] = useState('all');
  const [status, setStatus] = useState('all');
  const [selected, setSelected] = useState<AdminVisualLibraryItem | null>(null);
  const [editor, setEditor] = useState<EditorSeed | null>(null);

  const load = useCallback(async () => {
    if (initialLibrary) {
      setLibrary(initialLibrary);
      setLoading(false);
      return;
    }
    setLoading(true);
    setError('');
    try {
      const response = await getAdminVisualLibrary();
      setLibrary(response.data);
    } catch (err) {
      setError(errorMessage(err));
    } finally {
      setLoading(false);
    }
  }, [initialLibrary]);

  useEffect(() => {
    const timer = window.setTimeout(() => { void load(); }, 0);
    return () => window.clearTimeout(timer);
  }, [load]);

  const subjects = useMemo(() => Array.from(new Set((library?.items || []).map(item => item.subject).filter(Boolean))).sort(), [library]);
  const filtered = useMemo(() => {
    const query = search.trim().toLocaleLowerCase('fr');
    return (library?.items || []).filter(item => {
      if (kind !== 'all' && item.kind !== kind) return false;
      if (subject !== 'all' && item.subject !== subject) return false;
      if (lesson !== 'all' && item.lesson_id !== lesson) return false;
      if (status !== 'all' && item.status !== status) return false;
      if (!query) return true;
      return [item.title, item.description, item.subject, item.chapter, item.lesson, ...item.concepts]
        .join(' ').toLocaleLowerCase('fr').includes(query);
    });
  }, [kind, lesson, library, search, status, subject]);

  const typeGroups = useMemo<VisualTypeGroup[]>(() => {
    const groups = new Map<string, AdminVisualLibraryItem[]>();
    filtered.forEach(item => {
      const items = groups.get(item.kind) || [];
      items.push(item);
      groups.set(item.kind, items);
    });

    return Array.from(groups.entries())
      .map(([groupKind, items]) => ({
        kind: groupKind,
        label: KIND_LABELS[groupKind] || groupKind,
        items: [...items].sort((left, right) => (
          (left.subject || 'zzz').localeCompare(right.subject || 'zzz', 'fr')
          || (left.chapter || 'zzz').localeCompare(right.chapter || 'zzz', 'fr')
          || (left.lesson || 'zzz').localeCompare(right.lesson || 'zzz', 'fr')
          || left.title.localeCompare(right.title, 'fr')
        )),
      }))
      .sort((left, right) => {
        const leftIndex = VISUAL_TYPE_ORDER.indexOf(left.kind);
        const rightIndex = VISUAL_TYPE_ORDER.indexOf(right.kind);
        return (leftIndex < 0 ? VISUAL_TYPE_ORDER.length : leftIndex)
          - (rightIndex < 0 ? VISUAL_TYPE_ORDER.length : rightIndex)
          || left.label.localeCompare(right.label, 'fr');
      });
  }, [filtered]);

  const remove = async (item: AdminVisualLibraryItem) => {
    if (!item.resource_id || !window.confirm(`Supprimer « ${item.title} » de la bibliothèque ? Le fichier média éventuel sera conservé.`)) return;
    try {
      await deleteAdminVisualItem(item.resource_id);
      if (selected?.id === item.id) setSelected(null);
      await load();
    } catch (err) {
      setError(errorMessage(err));
    }
  };

  return (
    <div className="space-y-5">
      <div className="overflow-hidden rounded-3xl bg-gradient-to-br from-slate-950 via-indigo-950 to-slate-900 p-6 text-white shadow-xl">
        <div className="flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-[0.2em] text-cyan-300"><LibraryBig className="h-4 w-4" /> Catalogue transversal</div>
            <h2 className="mt-2 text-2xl font-black sm:text-3xl">Bibliothèque visuelle</h2>
            <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-300">Schémas validés, scènes contrôlables, médias, simulations et créations LLM de toutes les matières — avec le même rendu que dans le tableau de l’élève.</p>
          </div>
          <div className="flex flex-wrap gap-2">
            <button onClick={() => void load()} disabled={loading} className="flex items-center gap-2 rounded-xl border border-white/15 bg-white/5 px-4 py-2.5 text-sm font-bold hover:bg-white/10"><RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} /> Actualiser</button>
            <button onClick={() => setEditor({ ai: false, copy: false })} className="flex items-center gap-2 rounded-xl bg-white px-4 py-2.5 text-sm font-bold text-slate-900 hover:bg-cyan-50"><Plus className="h-4 w-4" /> Ajouter</button>
            <button onClick={() => setEditor({ ai: true, copy: false })} className="flex items-center gap-2 rounded-xl bg-indigo-500 px-4 py-2.5 text-sm font-bold text-white hover:bg-indigo-400"><Sparkles className="h-4 w-4" /> Créer avec le LLM</button>
          </div>
        </div>
        {library && (
          <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-4">
            <div className="rounded-2xl border border-white/10 bg-white/5 p-3"><div className="text-2xl font-black">{library.stats.total}</div><div className="text-xs text-slate-400">ressources visibles</div></div>
            <div className="rounded-2xl border border-white/10 bg-white/5 p-3"><div className="text-2xl font-black">{library.stats.by_kind.schema || 0}</div><div className="text-xs text-slate-400">schémas validés</div></div>
            <div className="rounded-2xl border border-white/10 bg-white/5 p-3"><div className="text-2xl font-black">{library.stats.by_kind.preset || 0}</div><div className="text-xs text-slate-400">scènes contrôlables</div></div>
            <div className="rounded-2xl border border-white/10 bg-white/5 p-3"><div className="text-2xl font-black">{library.stats.editable}</div><div className="text-xs text-slate-400">ressources administrables</div></div>
          </div>
        )}
      </div>

      {error && <div className="rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">{error}</div>}
      {library && !library.database_available && (
        <div className="flex items-start gap-3 rounded-2xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-800"><AlertTriangle className="mt-0.5 h-5 w-5 flex-none" /><div><strong>Catalogue local disponible, base indisponible.</strong><div className="mt-1 text-xs opacity-80">{library.database_error}</div></div></div>
      )}

      <div className="rounded-2xl border bg-white p-4 shadow-sm">
        <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-[minmax(260px,1.5fr)_repeat(4,minmax(150px,1fr))]">
          <label className="relative"><Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" /><input value={search} onChange={event => setSearch(event.target.value)} className={`${fieldClass} pl-9`} placeholder="Rechercher une notion, un chapitre…" /></label>
          <select value={subject} onChange={event => setSubject(event.target.value)} className={fieldClass}><option value="all">Toutes les matières</option>{subjects.map(value => <option key={value}>{value}</option>)}</select>
          <select value={kind} onChange={event => setKind(event.target.value)} className={fieldClass}>{Object.entries(KIND_LABELS).map(([value, label]) => <option key={value} value={value}>{label}</option>)}</select>
          <select value={status} onChange={event => setStatus(event.target.value)} className={fieldClass}>{Object.entries(STATUS_LABELS).map(([value, label]) => <option key={value} value={value}>{label}</option>)}</select>
          <select value={lesson} onChange={event => setLesson(event.target.value)} className={fieldClass}><option value="all">Toutes les leçons</option>{(library?.lessons || []).map(item => <option key={item.id} value={item.id}>{item.subject_name} · {item.title}</option>)}</select>
        </div>
      </div>

      {loading && !library ? (
        <div className="flex min-h-72 items-center justify-center rounded-2xl border bg-white text-gray-500"><LoaderCircle className="mr-2 h-5 w-5 animate-spin" /> Chargement du catalogue…</div>
      ) : filtered.length === 0 ? (
        <div className="rounded-2xl border bg-white py-16 text-center text-sm text-gray-500">Aucun visuel ne correspond aux filtres.</div>
      ) : (
        <div className="space-y-6">
          <div className="flex flex-wrap items-center gap-2 text-xs font-semibold text-gray-500">
            <span>{typeGroups.length} types de ressources</span>
            <span aria-hidden="true">·</span>
            <span>{filtered.length} visuels</span>
          </div>
          {typeGroups.map(group => (
            <section key={group.kind} className="overflow-hidden rounded-3xl border border-gray-200 bg-slate-50/70 shadow-sm">
              <header className="flex flex-col gap-3 border-b border-gray-200 bg-white px-5 py-4 sm:flex-row sm:items-center sm:justify-between">
                <div className="flex items-start gap-3">
                  <span className="mt-0.5 rounded-xl bg-indigo-50 p-2.5 text-indigo-600">{kindIcon(group.kind)}</span>
                  <div>
                    <div className="text-[11px] font-black uppercase tracking-[0.16em] text-indigo-600">Type de ressource</div>
                    <h3 className="mt-1 text-lg font-black text-gray-900">{group.label}</h3>
                    <p className="mt-0.5 text-xs text-gray-500">Triées par matière, chapitre puis cours à l’intérieur de cette catégorie.</p>
                  </div>
                </div>
                <span className="self-start rounded-full bg-gray-100 px-3 py-1.5 text-xs font-bold text-gray-600 sm:self-auto">{group.items.length} visuel{group.items.length > 1 ? 's' : ''}</span>
              </header>
              <div className="grid gap-4 p-4 sm:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4">
                {group.items.map(item => (
                  <article key={item.id} className="group overflow-hidden rounded-2xl border bg-white shadow-sm transition hover:-translate-y-0.5 hover:border-indigo-200 hover:shadow-lg">
                    <div className="block w-full text-left"><VisualPreview item={item} /></div>
                    <div className="p-4">
                      <div className="flex items-start justify-between gap-2">
                        <span className="inline-flex items-center gap-1 rounded-full bg-indigo-50 px-2 py-1 text-[10px] font-bold uppercase text-indigo-700">{kindIcon(item.kind)} {KIND_LABELS[item.kind] || item.kind}</span>
                        <span className={`rounded-full px-2 py-1 text-[10px] font-bold ring-1 ${statusClass(item.status)}`}>{STATUS_LABELS[item.status] || item.status}</span>
                      </div>
                      <h4 className="mt-3 line-clamp-2 min-h-12 font-black leading-6 text-gray-900">{item.title}</h4>
                      <p className="mt-1 line-clamp-2 min-h-8 text-xs leading-4 text-gray-500">{[item.subject, item.chapter, item.lesson].filter(Boolean).join(' · ') || 'Non rattaché à un cours'}</p>
                      <div className="mt-4 flex items-center justify-between border-t pt-3">
                        <button onClick={() => setSelected(item)} className="flex items-center gap-1.5 text-xs font-bold text-indigo-600 hover:text-indigo-800"><Eye className="h-4 w-4" /> Visualiser</button>
                        <div className="flex items-center gap-1">
                          {item.editable && <button onClick={() => setEditor({ item, ai: false, copy: false })} className="rounded-lg p-1.5 text-gray-400 hover:bg-gray-100 hover:text-gray-700" title="Modifier"><Pencil className="h-4 w-4" /></button>}
                          {(item.kind === 'scientific' || item.kind === 'schema' || item.kind === 'preset') && <button onClick={() => setEditor({ item, ai: true, copy: !item.editable })} className="rounded-lg p-1.5 text-indigo-500 hover:bg-indigo-50" title="Modifier avec le LLM"><Sparkles className="h-4 w-4" /></button>}
                          {item.deletable && <button onClick={() => void remove(item)} className="rounded-lg p-1.5 text-red-400 hover:bg-red-50 hover:text-red-600" title="Supprimer"><Trash2 className="h-4 w-4" /></button>}
                          {!item.editable && <ShieldCheck className="mx-1 h-4 w-4 text-emerald-500" aria-label="Ressource protégée" />}
                        </div>
                      </div>
                    </div>
                  </article>
                ))}
              </div>
            </section>
          ))}
        </div>
      )}

      {selected && (
        <DetailModal item={selected} onClose={() => setSelected(null)}
          onEdit={() => { setEditor({ item: selected, ai: false, copy: false }); setSelected(null); }}
          onAI={() => { setEditor({ item: selected, ai: true, copy: !selected.editable }); setSelected(null); }}
          onAttach={() => { setEditor({ item: selected, ai: false, copy: true }); setSelected(null); }} />
      )}
      {editor && <VisualEditorModal seed={editor} lessons={library?.lessons || []} onClose={() => setEditor(null)} onSaved={load} />}
    </div>
  );
}
