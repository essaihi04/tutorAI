import { useState, useRef, useCallback, useEffect } from 'react';
import * as pdfjsLib from 'pdfjs-dist/legacy/build/pdf.mjs';
import pdfjsWorkerUrl from 'pdfjs-dist/legacy/build/pdf.worker.min.mjs?url';

pdfjsLib.GlobalWorkerOptions.workerSrc = pdfjsWorkerUrl;

const API = '/api/v1/exam-extract';
const SCALE = 2.0;

// ── Types ────────────────────────────────────────────────────

interface DetectedZone {
  name: string;
  type: string;
  description: string;
  box_2d: [number, number, number, number];
}

interface DocItem {
  id: string;
  name: string;
  type: string;
  description: string;
  dataUrl: string;
  width: number;
  height: number;
  pageNumber: number;
  source: 'auto' | 'manual';
  visionDescription?: string;
  describingStatus?: 'pending' | 'loading' | 'done' | 'error';
}

interface PageOcr {
  pageNumber: number;
  text: string;
  markdown: string;
  status: 'pending' | 'active' | 'done' | 'error';
  error?: string;
}

interface PdfData {
  label: string;
  file: File | null;
  ocrPages: PageOcr[];
  totalPages: number;
  pageImages: { pageNumber: number; base64: string; canvas: HTMLCanvasElement; thumb: string }[];
}

type Phase = 'idle' | 'render' | 'ocr' | 'detect' | 'done';

interface PipelineStep {
  id: string;
  label: string;
  detail: string;
  status: 'pending' | 'active' | 'done' | 'error';
  subSteps?: { label: string; status: 'pending' | 'active' | 'done' | 'error' }[];
}

type Step = 'upload' | 'extracting' | 'results';
type ResultTab = 'text' | 'documents' | 'json';
type Subject = 'svt' | 'physique' | 'chimie' | 'math';

// ── Helpers ──────────────────────────────────────────────────

const renderPage = async (pdf: pdfjsLib.PDFDocumentProxy, pageNum: number) => {
  const page = await pdf.getPage(pageNum);
  const vp = page.getViewport({ scale: SCALE });
  const canvas = document.createElement('canvas');
  canvas.width = vp.width;
  canvas.height = vp.height;
  const ctx = canvas.getContext('2d')!;
  ctx.fillStyle = '#ffffff';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  await page.render({ canvasContext: ctx, viewport: vp, canvas } as any).promise;
  // Use PNG for best OCR quality; fallback to JPEG if too large (>4MB base64)
  let b64 = canvas.toDataURL('image/png').split(',')[1];
  if (b64.length > 4 * 1024 * 1024) {
    b64 = canvas.toDataURL('image/jpeg', 0.95).split(',')[1];
  }
  const thumb = canvas.toDataURL('image/jpeg', 0.4);
  return { base64: b64, canvas, thumb };
};

const cropZone = (
  canvas: HTMLCanvasElement,
  zone: DetectedZone,
): { dataUrl: string; w: number; h: number } => {
  const [ymin, xmin, ymax, xmax] = zone.box_2d;
  const x = Math.max(0, Math.round((xmin / 1000) * canvas.width));
  const y = Math.max(0, Math.round((ymin / 1000) * canvas.height));
  const w = Math.min(Math.round(((xmax - xmin) / 1000) * canvas.width), canvas.width - x);
  const h = Math.min(Math.round(((ymax - ymin) / 1000) * canvas.height), canvas.height - y);
  if (w <= 0 || h <= 0) return { dataUrl: '', w: 0, h: 0 };
  const c2 = document.createElement('canvas');
  c2.width = w;
  c2.height = h;
  c2.getContext('2d')!.drawImage(canvas, x, y, w, h, 0, 0, w, h);
  return { dataUrl: c2.toDataURL('image/png'), w, h };
};

let _docCounter = 0;
const nextDocId = () => `doc_${++_docCounter}`;

// ── Component ────────────────────────────────────────────────

export default function ExamExtractor() {
  const [sujet, setSujet] = useState<PdfData>({ label: 'Sujet', file: null, ocrPages: [], totalPages: 0, pageImages: [] });
  const [correction, setCorrection] = useState<PdfData>({ label: 'Correction', file: null, ocrPages: [], totalPages: 0, pageImages: [] });
  const [subject, setSubject] = useState<Subject>('svt');
  const [step, setStep] = useState<Step>('upload');
  const [processing, setProcessing] = useState(false);

  const [documents, setDocuments] = useState<DocItem[]>([]);
  const [resultTab, setResultTab] = useState<ResultTab>('text');

  // Pipeline visual tracker
  const [pipelineSteps, setPipelineSteps] = useState<PipelineStep[]>([]);
  const [currentPhase, setCurrentPhase] = useState<Phase>('idle');
  const [elapsedSec, setElapsedSec] = useState(0);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // Manual add
  const [manualName, setManualName] = useState('');
  const [manualDesc, setManualDesc] = useState('');
  const [manualType, setManualType] = useState('figure');
  const manualFileRef = useRef<HTMLInputElement>(null);
  const [manualPreview, setManualPreview] = useState<string | null>(null);
  const [manualDescLoading, setManualDescLoading] = useState(false);
  const pasteZoneRef = useRef<HTMLDivElement>(null);

  // Page preview (clickable pills)
  const [previewPage, setPreviewPage] = useState<{ pageNum: number; thumb: string } | null>(null);
  const previewPasteRef = useRef<HTMLDivElement>(null);

  // Edit document modal
  const [editDoc, setEditDoc] = useState<DocItem | null>(null);
  const [editName, setEditName] = useState('');
  const [editType, setEditType] = useState('figure');
  const [editDesc, setEditDesc] = useState('');
  const [editPreview, setEditPreview] = useState<string | null>(null);
  const [editDescLoading, setEditDescLoading] = useState(false);
  const editPasteRef = useRef<HTMLDivElement>(null);

  // Structured exam JSON
  const [structuredExam, setStructuredExam] = useState<any>(null);
  const [structuring, setStructuring] = useState(false);
  const [structureError, setStructureError] = useState('');

  // Publish
  const [publishing, setPublishing] = useState(false);
  const [publishResult, setPublishResult] = useState<{ success: boolean; message: string } | null>(null);
  const [pubYear, setPubYear] = useState(new Date().getFullYear());
  const [pubSession, setPubSession] = useState('Normale');
  const [pubTitle, setPubTitle] = useState('');
  const [pubSubjectFull, setPubSubjectFull] = useState('');
  const [pubNote, setPubNote] = useState('');

  const sujetRef = useRef<HTMLInputElement>(null);
  const corrRef = useRef<HTMLInputElement>(null);

  // Published exams admin
  const [publishedExams, setPublishedExams] = useState<any[]>([]);
  const [loadingExams, setLoadingExams] = useState(false);
  const [showPublished, setShowPublished] = useState(false);
  const [editingExam, setEditingExam] = useState<any | null>(null);
  const [editFields, setEditFields] = useState<Record<string, any>>({});
  const [deletingId, setDeletingId] = useState<string | null>(null);

  const fetchPublishedExams = async () => {
    setLoadingExams(true);
    try {
      const r = await fetch(`${API}/published-exams`);
      const d = await r.json();
      setPublishedExams(d.exams || []);
    } catch { /* ignore */ } finally { setLoadingExams(false); }
  };

  const deleteExam = async (id: string) => {
    if (!confirm(`Supprimer l'examen "${id}" ? Cette action est irréversible.`)) return;
    setDeletingId(id);
    try {
      const r = await fetch(`${API}/published-exams/${id}`, { method: 'DELETE' });
      if (r.ok) {
        setPublishedExams(prev => prev.filter(e => e.id !== id));
      }
    } catch { /* ignore */ } finally { setDeletingId(null); }
  };

  const saveEditExam = async () => {
    if (!editingExam) return;
    try {
      const r = await fetch(`${API}/published-exams/${editingExam.id}`, {
        method: 'PUT', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(editFields),
      });
      if (r.ok) {
        const d = await r.json();
        setPublishedExams(prev => prev.map(e => e.id === editingExam.id ? { ...e, ...d.exam } : e));
        setEditingExam(null);
      }
    } catch { /* ignore */ }
  };

  useEffect(() => { fetchPublishedExams(); }, []);

  // ── helpers ───────────────────────────────────────────
  const updateStep = (id: string, u: Partial<PipelineStep>) =>
    setPipelineSteps(prev => prev.map(s => s.id === id ? { ...s, ...u } : s));

  const handleFile = useCallback(
    (which: 'sujet' | 'correction', f: File | null) => {
      const empty: PdfData = { label: which === 'sujet' ? 'Sujet' : 'Correction', file: f, ocrPages: [], totalPages: 0, pageImages: [] };
      if (which === 'sujet') setSujet(empty);
      else setCorrection(empty);
    }, [],
  );

  // ── API calls ─────────────────────────────────────────
  const ocrPage = async (base64: string, pageNum: number): Promise<{ text: string; markdown: string }> => {
    const r = await fetch(`${API}/ocr-page`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ image_base64: base64, page_number: pageNum, subject }),
    });
    if (!r.ok) throw new Error(`OCR error ${r.status}`);
    const d = await r.json();
    return { text: d.text || '', markdown: d.markdown || '' };
  };

  const detectZones = async (base64: string, pageNum: number): Promise<DetectedZone[]> => {
    const r = await fetch(`${API}/detect-zones`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ image_base64: base64, page_number: pageNum }),
    });
    if (!r.ok) throw new Error(`detect-zones error ${r.status}`);
    return (await r.json()).zones || [];
  };

  const describeDoc = async (dataUrl: string, docName: string): Promise<string> => {
    const r = await fetch(`${API}/describe-doc`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ image_base64: dataUrl, doc_name: docName, subject }),
    });
    if (!r.ok) throw new Error(`describe-doc error ${r.status}`);
    return (await r.json()).description || '';
  };

  // ── Auto-detect metadata from OCR text ──────────────
  const autoDetectMeta = (text: string) => {
    const ym = text.match(/\b(20[1-3]\d)\b/);
    if (ym) setPubYear(parseInt(ym[1]));
    if (/rattrapage/i.test(text)) setPubSession('Rattrapage');
    else if (/normale|ordinaire|session\s+normale/i.test(text)) setPubSession('Normale');
    if (/sciences\s+de\s+la\s+vie/i.test(text)) setPubSubjectFull('Sciences de la Vie et de la Terre - Filière Sciences Physiques');
    else if (/physique/i.test(text) && /chimie/i.test(text)) setPubSubjectFull('Physique-Chimie - Filière Sciences Physiques');
    else if (/math[éeè]matiques/i.test(text)) setPubSubjectFull('Mathématiques - Filière Sciences Physiques');
    const yr = ym ? ym[1] : String(pubYear);
    const sess = /rattrapage/i.test(text) ? 'Rattrapage' : 'Normale';
    const subMap: Record<string, string> = { svt: 'SVT', physique: 'Physique', chimie: 'Chimie', math: 'Mathématiques' };
    setPubTitle(`Examen National du Baccalauréat - ${subMap[subject] || subject.toUpperCase()} ${yr} ${sess}`);
    const noteMatch = text.match(/((?:il est|l'usage).*?(?:calculatrice|non programmable)[^.]*\.?)/i);
    if (noteMatch) setPubNote(noteMatch[1].trim());
  };

  // ── Main pipeline ─────────────────────────────────────
  const runExtraction = async () => {
    if (!sujet.file) return;
    setProcessing(true);
    setStep('extracting');
    setDocuments([]);
    setPublishResult(null);
    _docCounter = 0;
    setElapsedSec(0);
    timerRef.current = setInterval(() => setElapsedSec(s => s + 1), 1000);

    // Build pipeline steps
    const steps: PipelineStep[] = [
      { id: 'load', label: 'Chargement des PDF', detail: '', status: 'pending' },
      { id: 'sujet_render', label: 'Rendu pages — Sujet', detail: '', status: 'pending', subSteps: [] },
      { id: 'sujet_ocr', label: 'OCR Mistral — Sujet', detail: '', status: 'pending', subSteps: [] },
      { id: 'sujet_detect', label: 'Détection documents — Sujet', detail: '', status: 'pending', subSteps: [] },
    ];
    if (correction.file) {
      steps.push(
        { id: 'corr_render', label: 'Rendu pages — Correction', detail: '', status: 'pending', subSteps: [] },
        { id: 'corr_ocr', label: 'OCR Mistral — Correction', detail: '', status: 'pending', subSteps: [] },
      );
    }
    // describe step removed — auto-description now only at paste time
    setPipelineSteps(steps);

    try {
      // ── Load PDFs ──
      setCurrentPhase('render');
      updateStep('load', { status: 'active', detail: 'Lecture du fichier Sujet...' });
      const sujetBuf = await sujet.file.arrayBuffer();
      const sujetPdf = await pdfjsLib.getDocument({ data: sujetBuf }).promise;
      let corrPdf: pdfjsLib.PDFDocumentProxy | null = null;
      if (correction.file) {
        updateStep('load', { detail: 'Lecture du fichier Correction...' });
        const corrBuf = await correction.file.arrayBuffer();
        corrPdf = await pdfjsLib.getDocument({ data: corrBuf }).promise;
      }
      updateStep('load', { status: 'done', detail: `${sujetPdf.numPages} pages sujet${corrPdf ? ` + ${corrPdf.numPages} pages correction` : ''}` });

      const allDocs: DocItem[] = [];

      // ── Process sujet ──
      const sn = sujetPdf.numPages;
      const sSubSteps = Array.from({ length: sn }, (_, i) => ({ label: `Page ${i + 1}`, status: 'pending' as const }));
      setSujet(prev => ({ ...prev, totalPages: sn, ocrPages: Array.from({ length: sn }, (_, i) => ({ pageNumber: i + 1, text: '', markdown: '', status: 'pending' as const })), pageImages: [] }));

      // Render sujet
      updateStep('sujet_render', { status: 'active', detail: `0/${sn}`, subSteps: [...sSubSteps] });
      const sujetCanvases: { base64: string; canvas: HTMLCanvasElement }[] = [];
      for (let p = 1; p <= sn; p++) {
        const ss = [...sSubSteps]; ss[p - 1] = { ...ss[p - 1], status: 'active' };
        updateStep('sujet_render', { detail: `${p}/${sn}`, subSteps: ss });
        const { base64, canvas, thumb } = await renderPage(sujetPdf, p);
        sujetCanvases.push({ base64, canvas });
        setSujet(prev => ({ ...prev, pageImages: [...prev.pageImages, { pageNumber: p, base64, canvas, thumb }] }));
        ss[p - 1] = { ...ss[p - 1], status: 'done' };
        updateStep('sujet_render', { subSteps: ss });
      }
      updateStep('sujet_render', { status: 'done', detail: `${sn} pages rendues` });

      // OCR sujet
      setCurrentPhase('ocr');
      const ocrSubSteps = Array.from({ length: sn }, (_, i) => ({ label: `Page ${i + 1}`, status: 'pending' as const }));
      updateStep('sujet_ocr', { status: 'active', detail: `0/${sn}`, subSteps: [...ocrSubSteps] });
      for (let p = 1; p <= sn; p++) {
        const ss = [...ocrSubSteps]; ss[p - 1] = { ...ss[p - 1], status: 'active' };
        updateStep('sujet_ocr', { detail: `${p}/${sn}`, subSteps: ss });
        setSujet(prev => ({ ...prev, ocrPages: prev.ocrPages.map(pg => pg.pageNumber === p ? { ...pg, status: 'active' } : pg) }));
        try {
          const ocr = await ocrPage(sujetCanvases[p - 1].base64, p);
          setSujet(prev => ({ ...prev, ocrPages: prev.ocrPages.map(pg => pg.pageNumber === p ? { ...pg, text: ocr.text, markdown: ocr.markdown, status: 'done' } : pg) }));
          ss[p - 1] = { ...ss[p - 1], status: 'done' };
        } catch {
          setSujet(prev => ({ ...prev, ocrPages: prev.ocrPages.map(pg => pg.pageNumber === p ? { ...pg, status: 'error' } : pg) }));
          ss[p - 1] = { ...ss[p - 1], status: 'error' };
        }
        updateStep('sujet_ocr', { subSteps: ss });
      }
      updateStep('sujet_ocr', { status: 'done', detail: `${sn} pages` });

      // Detect zones sujet
      setCurrentPhase('detect');
      const detSubSteps = Array.from({ length: sn }, (_, i) => ({ label: `Page ${i + 1}`, status: 'pending' as const }));
      updateStep('sujet_detect', { status: 'active', detail: `0/${sn}`, subSteps: [...detSubSteps] });
      for (let p = 1; p <= sn; p++) {
        const ss = [...detSubSteps]; ss[p - 1] = { ...ss[p - 1], status: 'active' };
        updateStep('sujet_detect', { detail: `${p}/${sn}`, subSteps: ss });
        try {
          const zones = await detectZones(sujetCanvases[p - 1].base64, p);
          for (const z of zones) {
            const { dataUrl, w, h } = cropZone(sujetCanvases[p - 1].canvas, z);
            if (dataUrl && w > 0 && h > 0) {
              allDocs.push({ id: nextDocId(), name: z.name, type: z.type, description: z.description, dataUrl, width: w, height: h, pageNumber: p, source: 'auto', describingStatus: 'pending' });
            }
          }
          ss[p - 1] = { ...ss[p - 1], status: 'done' };
        } catch {
          ss[p - 1] = { ...ss[p - 1], status: 'error' };
        }
        updateStep('sujet_detect', { subSteps: ss });
      }
      updateStep('sujet_detect', { status: 'done', detail: `${allDocs.length} document(s) trouvé(s)` });

      // ── Process correction ──
      if (corrPdf) {
        const cn = corrPdf.numPages;
        setCorrection(prev => ({ ...prev, totalPages: cn, ocrPages: Array.from({ length: cn }, (_, i) => ({ pageNumber: i + 1, text: '', markdown: '', status: 'pending' as const })), pageImages: [] }));

        // Render correction
        setCurrentPhase('render');
        const crSubSteps = Array.from({ length: cn }, (_, i) => ({ label: `Page ${i + 1}`, status: 'pending' as const }));
        updateStep('corr_render', { status: 'active', detail: `0/${cn}`, subSteps: [...crSubSteps] });
        const corrCanvases: { base64: string }[] = [];
        for (let p = 1; p <= cn; p++) {
          const ss = [...crSubSteps]; ss[p - 1] = { ...ss[p - 1], status: 'active' };
          updateStep('corr_render', { detail: `${p}/${cn}`, subSteps: ss });
          const { base64, canvas, thumb } = await renderPage(corrPdf, p);
          corrCanvases.push({ base64 });
          setCorrection(prev => ({ ...prev, pageImages: [...prev.pageImages, { pageNumber: p, base64, canvas, thumb }] }));
          ss[p - 1] = { ...ss[p - 1], status: 'done' };
          updateStep('corr_render', { subSteps: ss });
        }
        updateStep('corr_render', { status: 'done', detail: `${cn} pages rendues` });

        // OCR correction
        setCurrentPhase('ocr');
        const coSubSteps = Array.from({ length: cn }, (_, i) => ({ label: `Page ${i + 1}`, status: 'pending' as const }));
        updateStep('corr_ocr', { status: 'active', detail: `0/${cn}`, subSteps: [...coSubSteps] });
        for (let p = 1; p <= cn; p++) {
          const ss = [...coSubSteps]; ss[p - 1] = { ...ss[p - 1], status: 'active' };
          updateStep('corr_ocr', { detail: `${p}/${cn}`, subSteps: ss });
          setCorrection(prev => ({ ...prev, ocrPages: prev.ocrPages.map(pg => pg.pageNumber === p ? { ...pg, status: 'active' } : pg) }));
          try {
            const ocr = await ocrPage(corrCanvases[p - 1].base64, p);
            setCorrection(prev => ({ ...prev, ocrPages: prev.ocrPages.map(pg => pg.pageNumber === p ? { ...pg, text: ocr.text, markdown: ocr.markdown, status: 'done' } : pg) }));
            ss[p - 1] = { ...ss[p - 1], status: 'done' };
          } catch {
            setCorrection(prev => ({ ...prev, ocrPages: prev.ocrPages.map(pg => pg.pageNumber === p ? { ...pg, status: 'error' } : pg) }));
            ss[p - 1] = { ...ss[p - 1], status: 'error' };
          }
          updateStep('corr_ocr', { subSteps: ss });
        }
        updateStep('corr_ocr', { status: 'done', detail: `${cn} pages` });
      }

      // ── Set documents (auto-description removed — done at paste time instead) ──
      setDocuments(allDocs);

      setCurrentPhase('done');
      setStep('results');
      // Auto-detect metadata from first page OCR text (use setTimeout to read latest state)
      setTimeout(() => {
        setSujet(prev => {
          const txt = prev.ocrPages.filter(p => p.text).map(p => p.text).join('\n').slice(0, 2000);
          if (txt) autoDetectMeta(txt);
          return prev;
        });
      }, 100);
    } catch (err: any) {
      console.error('Pipeline error:', err);
    } finally {
      setProcessing(false);
      if (timerRef.current) clearInterval(timerRef.current);
    }
  };

  // ── Manual add document ───────────────────────────────

  const setPreviewAndAutoDescribe = async (dataUrl: string) => {
    setManualPreview(dataUrl);
    setManualDesc('');
    setManualDescLoading(true);
    try {
      const desc = await describeDoc(dataUrl, manualName.trim() || 'Document collé');
      setManualDesc(desc);
    } catch {
      setManualDesc('(Description automatique échouée)');
    } finally {
      setManualDescLoading(false);
    }
  };

  const handleManualFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0];
    if (!f) return;
    const reader = new FileReader();
    reader.onload = () => setPreviewAndAutoDescribe(reader.result as string);
    reader.readAsDataURL(f);
  };

  const handlePaste = (e: React.ClipboardEvent) => {
    const items = e.clipboardData?.items;
    if (!items) return;
    for (const item of Array.from(items)) {
      if (item.type.startsWith('image/')) {
        e.preventDefault();
        const blob = item.getAsFile();
        if (!blob) continue;
        const reader = new FileReader();
        reader.onload = () => setPreviewAndAutoDescribe(reader.result as string);
        reader.readAsDataURL(blob);
        return;
      }
    }
  };

  const addManualDocument = () => {
    if (!manualPreview || !manualName.trim()) return;
    const img = new Image();
    img.onload = () => {
      setDocuments(prev => [...prev, {
        id: nextDocId(), name: manualName.trim(), type: manualType, description: manualDesc.trim(),
        dataUrl: manualPreview!, width: img.width, height: img.height, pageNumber: 0, source: 'manual',
        visionDescription: manualDesc.trim(), describingStatus: 'done',
      }]);
      setManualName(''); setManualDesc(''); setManualPreview(null);
      if (manualFileRef.current) manualFileRef.current.value = '';
    };
    img.src = manualPreview;
  };

  const removeDocument = (id: string) => setDocuments(prev => prev.filter(d => d.id !== id));

  // ── Edit document helpers ──────────────────────────────
  const openEditDoc = (doc: DocItem) => {
    setEditDoc(doc);
    setEditName(doc.name);
    setEditType(doc.type);
    setEditDesc(doc.visionDescription || doc.description);
    setEditPreview(null);
    setEditDescLoading(false);
  };

  const handleEditPaste = async (e: React.ClipboardEvent) => {
    const items = e.clipboardData.items;
    for (const item of items) {
      if (item.type.startsWith('image/')) {
        e.preventDefault();
        const blob = item.getAsFile();
        if (!blob) return;
        const reader = new FileReader();
        reader.onload = async () => {
          const dataUrl = reader.result as string;
          setEditPreview(dataUrl);
          // Auto-describe
          setEditDescLoading(true);
          try {
            const desc = await describeDoc(dataUrl, editName || editDoc?.name || 'Document');
            setEditDesc(desc);
          } catch { /* keep manual */ }
          setEditDescLoading(false);
        };
        reader.readAsDataURL(blob);
        break;
      }
    }
  };

  const saveEditDoc = () => {
    if (!editDoc) return;
    setDocuments(prev => prev.map(d => {
      if (d.id !== editDoc.id) return d;
      const updated = { ...d, name: editName, type: editType, description: editDesc, visionDescription: editDesc };
      if (editPreview) {
        // Replace image: compute new dimensions
        const img = new Image();
        img.onload = () => {
          setDocuments(prev2 => prev2.map(dd => dd.id === editDoc.id ? { ...dd, dataUrl: editPreview!, width: img.naturalWidth, height: img.naturalHeight } : dd));
        };
        img.src = editPreview;
        updated.dataUrl = editPreview;
      }
      return updated;
    }));
    setEditDoc(null);
  };

  // ── Structure exam JSON ────────────────────────────────
  const generateStructuredExam = async () => {
    setStructuring(true);
    setStructureError('');
    setStructuredExam(null);
    try {
      const r = await fetch(`${API}/structure-exam`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sujet_text: sujet.ocrPages.filter(p => p.status === 'done').map(p => p.text).join('\n\n---\n\n'),
          correction_text: correction.ocrPages.filter(p => p.status === 'done').map(p => p.text).join('\n\n---\n\n'),
          subject, year: pubYear, session: pubSession, title: pubTitle || `Examen ${subject.toUpperCase()} ${pubYear}`,
          documents: documents.map(d => ({ name: d.name, type: d.type, description: d.visionDescription || d.description, pageNumber: d.pageNumber })),
        }),
      });
      const data = await r.json();
      if (r.ok && data.success) {
        const ej = data.exam_json;
        setStructuredExam(ej);
        setResultTab('json');
        // Auto-fill publish metadata from structured JSON
        if (ej.title) setPubTitle(ej.title);
        if (ej.year) setPubYear(ej.year);
        if (ej.session) setPubSession(ej.session === 'Rattrapage' ? 'Rattrapage' : 'Normale');
        if (ej.subject_full) setPubSubjectFull(ej.subject_full);
        if (ej.note) setPubNote(ej.note);
      } else {
        setStructureError(data.detail || 'Erreur de structuration');
      }
    } catch (err: any) {
      setStructureError(err.message);
    } finally {
      setStructuring(false);
    }
  };

  // ── Publish ───────────────────────────────────────────
  const handlePublish = async () => {
    if (!pubTitle.trim()) return;
    setPublishing(true);
    setPublishResult(null);
    const sessionSlug = pubSession.toLowerCase().replace(/ /g, '_');
    const examId = `${subject}_${pubYear}_${sessionSlug}`;
    try {
      const r = await fetch(`${API}/publish`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          exam_id: examId, subject, year: pubYear, session: pubSession,
          title: pubTitle, subject_full: pubSubjectFull || pubTitle,
          note: pubNote,
          sujet_text: sujet.ocrPages.filter(p => p.status === 'done').map(p => p.text).join('\n\n---\n\n'),
          correction_text: correction.ocrPages.filter(p => p.status === 'done').map(p => p.text).join('\n\n---\n\n'),
          documents: documents.map(d => ({ name: d.name, type: d.type, description: d.visionDescription || d.description, dataUrl: d.dataUrl })),
          structured_exam: structuredExam || null,
        }),
      });
      const data = await r.json();
      if (r.ok && data.success) {
        setPublishResult({ success: true, message: `✅ Examen "${examId}" publié avec succès ! ${data.documents_saved} document(s) sauvegardés. exam.json ${structuredExam ? '✓' : '✗'} • Chemin: ${data.path}` });
        fetchPublishedExams();
      } else {
        setPublishResult({ success: false, message: data.detail || 'Erreur inconnue' });
      }
    } catch (err: any) {
      setPublishResult({ success: false, message: err.message });
    } finally {
      setPublishing(false);
    }
  };

  // ── Re-OCR single page ─────────────────────────────────
  const reOcrSujetPage = async (pageNum: number) => {
    const img = sujet.pageImages.find(pi => pi.pageNumber === pageNum);
    if (!img) return;
    setSujet(prev => ({ ...prev, ocrPages: prev.ocrPages.map(pg => pg.pageNumber === pageNum ? { ...pg, status: 'active' } : pg) }));
    try {
      const ocr = await ocrPage(img.base64, pageNum);
      setSujet(prev => ({ ...prev, ocrPages: prev.ocrPages.map(pg => pg.pageNumber === pageNum ? { ...pg, text: ocr.text, markdown: ocr.markdown, status: 'done' } : pg) }));
    } catch {
      setSujet(prev => ({ ...prev, ocrPages: prev.ocrPages.map(pg => pg.pageNumber === pageNum ? { ...pg, status: 'error', error: 'Re-OCR échoué' } : pg) }));
    }
  };
  const reOcrCorrPage = async (pageNum: number) => {
    const img = correction.pageImages.find(pi => pi.pageNumber === pageNum);
    if (!img) return;
    setCorrection(prev => ({ ...prev, ocrPages: prev.ocrPages.map(pg => pg.pageNumber === pageNum ? { ...pg, status: 'active' } : pg) }));
    try {
      const ocr = await ocrPage(img.base64, pageNum);
      setCorrection(prev => ({ ...prev, ocrPages: prev.ocrPages.map(pg => pg.pageNumber === pageNum ? { ...pg, text: ocr.text, markdown: ocr.markdown, status: 'done' } : pg) }));
    } catch {
      setCorrection(prev => ({ ...prev, ocrPages: prev.ocrPages.map(pg => pg.pageNumber === pageNum ? { ...pg, status: 'error', error: 'Re-OCR échoué' } : pg) }));
    }
  };

  // ── Computed ──────────────────────────────────────────
  const autoDocCount = documents.filter(d => d.source === 'auto').length;
  const manualDocCount = documents.filter(d => d.source === 'manual').length;
  const canRun = !!sujet.file && !processing;
  const sujetText = sujet.ocrPages.filter(p => p.status === 'done').map(p => p.text).join('\n\n---\n\n');
  const corrText = correction.ocrPages.filter(p => p.status === 'done').map(p => p.text).join('\n\n---\n\n');
  const fmtTime = (s: number) => `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`;

  // ── Render ────────────────────────────────────────────
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Extracteur d'examens</h1>
            <p className="text-sm text-gray-500 mt-1">OCR Mistral + Vision Pixtral — Extraction texte &amp; documents</p>
          </div>
          <a href="/admin" className="text-blue-600 hover:text-blue-800 text-sm font-medium">← Retour Admin</a>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-6 space-y-6">

        {/* ─── PUBLISHED EXAMS PANEL ─── */}
        <div className="bg-white rounded-xl shadow-sm border">
          <button onClick={() => { setShowPublished(v => !v); if (!showPublished) fetchPublishedExams(); }}
            className="w-full flex items-center justify-between px-6 py-4 hover:bg-gray-50 transition">
            <div className="flex items-center gap-3">
              <span className="text-lg">📚</span>
              <h2 className="font-semibold text-gray-900">Examens publiés</h2>
              <span className="px-2 py-0.5 bg-blue-100 text-blue-700 rounded-full text-xs font-medium">{publishedExams.length}</span>
            </div>
            <svg className={`w-5 h-5 text-gray-400 transition-transform ${showPublished ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </button>

          {showPublished && (
            <div className="px-6 pb-5 space-y-3 border-t">
              {loadingExams && <p className="text-sm text-gray-400 py-4 text-center animate-pulse">Chargement...</p>}
              {!loadingExams && publishedExams.length === 0 && (
                <p className="text-sm text-gray-400 py-4 text-center">Aucun examen publié</p>
              )}
              {!loadingExams && publishedExams.length > 0 && (
                <div className="overflow-x-auto mt-3">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="text-left text-xs text-gray-500 uppercase tracking-wider border-b">
                        <th className="pb-2 pr-3">Matière</th>
                        <th className="pb-2 pr-3">Année</th>
                        <th className="pb-2 pr-3">Session</th>
                        <th className="pb-2 pr-3">Titre</th>
                        <th className="pb-2 pr-3 text-center">JSON</th>
                        <th className="pb-2 pr-3 text-center">Docs</th>
                        <th className="pb-2 text-right">Actions</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-100">
                      {publishedExams.map(ex => (
                        <tr key={ex.id} className="hover:bg-gray-50/50">
                          <td className="py-2.5 pr-3">
                            <div className="flex items-center gap-1">
                              <span className={`px-2 py-0.5 rounded text-xs font-semibold ${
                                ex.subject === 'SVT' ? 'bg-green-100 text-green-700' :
                                ex.subject?.toLowerCase() === 'physique' ? 'bg-blue-100 text-blue-700' :
                                ex.subject?.toLowerCase() === 'chimie' ? 'bg-orange-100 text-orange-700' :
                                ex.subject?.toLowerCase().includes('math') ? 'bg-purple-100 text-purple-700' :
                                'bg-gray-100 text-gray-700'
                              }`}>{ex.subject}</span>
                              {ex.source === 'database' && <span className="px-1 py-0.5 rounded text-[9px] bg-sky-100 text-sky-600 font-medium">DB</span>}
                            </div>
                          </td>
                          <td className="py-2.5 pr-3 font-medium text-gray-900">{ex.year}</td>
                          <td className="py-2.5 pr-3 text-gray-600">{ex.session}</td>
                          <td className="py-2.5 pr-3 text-gray-700 max-w-[260px] truncate" title={ex.title}>{ex.title}</td>
                          <td className="py-2.5 pr-3 text-center">
                            {ex.has_exam_json
                              ? <span className="text-green-600 font-bold" title="exam.json présent">✓</span>
                              : <span className="text-red-400" title="exam.json manquant">✗</span>}
                          </td>
                          <td className="py-2.5 pr-3 text-center text-gray-600">{ex.document_count}</td>
                          <td className="py-2.5 text-right">
                            <div className="flex items-center justify-end gap-1.5">
                              <a href={`/exam/practice/${ex.id}`} target="_blank" rel="noreferrer"
                                className="px-2.5 py-1 bg-blue-50 text-blue-700 rounded-md text-xs font-medium hover:bg-blue-100 transition"
                                title="Voir en tant qu'élève">👁 Voir</a>
                              <button onClick={() => { setEditingExam(ex); setEditFields({ subject: ex.subject || '', title: ex.title, year: ex.year, session: ex.session, subject_full: ex.subject_full || '', note: ex.note || '', duration_minutes: ex.duration_minutes || 180, coefficient: ex.coefficient || 5, total_points: ex.total_points || 20 }); }}
                                className="px-2.5 py-1 bg-amber-50 text-amber-700 rounded-md text-xs font-medium hover:bg-amber-100 transition"
                                title="Modifier les métadonnées">✏️ Modifier</button>
                              <button onClick={() => deleteExam(ex.id)} disabled={deletingId === ex.id}
                                className="px-2.5 py-1 bg-red-50 text-red-700 rounded-md text-xs font-medium hover:bg-red-100 transition disabled:opacity-50"
                                title="Supprimer cet examen">{deletingId === ex.id ? '...' : '🗑 Supprimer'}</button>
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          )}
        </div>

        {/* ─── EDIT EXAM MODAL ─── */}
        {editingExam && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40" onClick={() => setEditingExam(null)}>
            <div className="bg-white rounded-2xl shadow-2xl w-full max-w-lg p-6 space-y-4" onClick={e => e.stopPropagation()}>
              <h3 className="font-bold text-gray-900 text-lg">Modifier — {editingExam.id}</h3>
              <div className="space-y-3">
                <div>
                  <label className="block text-xs font-medium text-gray-500 mb-1">Titre</label>
                  <input type="text" value={editFields.title || ''} onChange={e => setEditFields(f => ({ ...f, title: e.target.value }))}
                    className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none" />
                </div>
                <div className="grid grid-cols-4 gap-3">
                  <div>
                    <label className="block text-xs font-medium text-gray-500 mb-1">Matière</label>
                    <select value={editFields.subject || ''} onChange={e => setEditFields(f => ({ ...f, subject: e.target.value }))}
                      className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none">
                      <option value="SVT">SVT</option>
                      <option value="Physique">Physique</option>
                      <option value="Chimie">Chimie</option>
                      <option value="Mathematiques">Maths</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-gray-500 mb-1">Année</label>
                    <input type="number" value={editFields.year || ''} onChange={e => setEditFields(f => ({ ...f, year: Number(e.target.value) }))}
                      className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none" />
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-gray-500 mb-1">Session</label>
                    <select value={editFields.session || 'Normale'} onChange={e => setEditFields(f => ({ ...f, session: e.target.value }))}
                      className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none">
                      <option>Normale</option><option>Rattrapage</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-gray-500 mb-1">Durée (min)</label>
                    <input type="number" value={editFields.duration_minutes || ''} onChange={e => setEditFields(f => ({ ...f, duration_minutes: Number(e.target.value) }))}
                      className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none" />
                  </div>
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-500 mb-1">Matière (complet)</label>
                  <input type="text" value={editFields.subject_full || ''} onChange={e => setEditFields(f => ({ ...f, subject_full: e.target.value }))}
                    className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none" />
                </div>
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-medium text-gray-500 mb-1">Coefficient</label>
                    <input type="number" value={editFields.coefficient || ''} onChange={e => setEditFields(f => ({ ...f, coefficient: Number(e.target.value) }))}
                      className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none" />
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-gray-500 mb-1">Total points</label>
                    <input type="number" value={editFields.total_points || ''} onChange={e => setEditFields(f => ({ ...f, total_points: Number(e.target.value) }))}
                      className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none" />
                  </div>
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-500 mb-1">Note</label>
                  <input type="text" value={editFields.note || ''} onChange={e => setEditFields(f => ({ ...f, note: e.target.value }))}
                    className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none" />
                </div>
              </div>
              <div className="flex justify-end gap-3 pt-2">
                <button onClick={() => setEditingExam(null)}
                  className="px-4 py-2 text-sm text-gray-600 hover:text-gray-800 transition">Annuler</button>
                <button onClick={saveEditExam}
                  className="px-5 py-2 bg-blue-600 text-white rounded-lg text-sm font-semibold hover:bg-blue-700 transition">Sauvegarder</button>
              </div>
            </div>
          </div>
        )}

        {/* ─── UPLOAD SECTION ─── */}
        <div className="bg-white rounded-xl shadow-sm border p-6 space-y-5">
          <h2 className="font-semibold text-gray-900 text-lg">1. Charger les PDF</h2>
          <div className="flex items-center gap-3">
            <span className="text-sm font-medium text-gray-600">Matière :</span>
            {(['svt', 'physique', 'chimie', 'math'] as Subject[]).map(s => (
              <button key={s} onClick={() => setSubject(s)}
                className={`px-3 py-1.5 rounded-lg text-sm font-medium transition ${subject === s ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'}`}>
                {s === 'svt' ? 'SVT' : s.charAt(0).toUpperCase() + s.slice(1)}
              </button>
            ))}
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <UploadBox fileRef={sujetRef} file={sujet.file} label="PDF Sujet" required
              color={sujet.file ? 'border-blue-300 bg-blue-50' : ''} onPick={() => sujetRef.current?.click()}
              onChange={e => handleFile('sujet', e.target.files?.[0] || null)} />
            <UploadBox fileRef={corrRef} file={correction.file} label="PDF Correction"
              color={correction.file ? 'border-green-300 bg-green-50' : ''} onPick={() => corrRef.current?.click()}
              onChange={e => handleFile('correction', e.target.files?.[0] || null)} />
          </div>
          <button onClick={runExtraction} disabled={!canRun}
            className={`px-6 py-2.5 rounded-xl text-sm font-semibold text-white transition ${canRun ? 'bg-blue-600 hover:bg-blue-700' : 'bg-gray-300 cursor-not-allowed'}`}>
            {processing ? 'Extraction en cours...' : 'Lancer l\'extraction'}
          </button>
        </div>

        {/* ─── PIPELINE TRACKER ─── */}
        {pipelineSteps.length > 0 && (
          <div className="bg-white rounded-xl shadow-sm border p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="font-semibold text-gray-900 text-lg">2. Pipeline d'extraction</h2>
              <div className="flex items-center gap-3">
                {processing && <span className="text-xs text-gray-400 animate-pulse">En cours...</span>}
                <span className="px-3 py-1 bg-gray-100 rounded-full text-xs font-mono font-medium text-gray-600">
                  {fmtTime(elapsedSec)}
                </span>
                {currentPhase === 'done' && (
                  <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-xs font-medium">Terminé</span>
                )}
              </div>
            </div>
            <div className="space-y-2">
              {pipelineSteps.map((ps, idx) => (
                <div key={ps.id}>
                  {/* Step row */}
                  <div className="flex items-center gap-3 py-2">
                    <StepIcon status={ps.status} />
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2">
                        <span className={`text-sm font-medium ${ps.status === 'active' ? 'text-blue-700' : ps.status === 'done' ? 'text-gray-700' : 'text-gray-400'}`}>
                          {ps.label}
                        </span>
                        {ps.detail && (
                          <span className="text-xs text-gray-400">{ps.detail}</span>
                        )}
                      </div>
                      {/* Sub-step pills — clickable for page steps */}
                      {ps.subSteps && ps.subSteps.length > 0 && (ps.status === 'active' || ps.status === 'done') && (
                        <div className="flex flex-wrap gap-1 mt-1.5">
                          {ps.subSteps.map((ss, si) => {
                            const isPagePill = ss.label.startsWith('Page ') && (ps.id === 'sujet_detect' || ps.id === 'sujet_render' || ps.id === 'sujet_ocr' || ps.id === 'corr_render' || ps.id === 'corr_ocr');
                            const pageNum = isPagePill ? parseInt(ss.label.replace('Page ', '')) : 0;
                            const thumbSource = ps.id.startsWith('sujet') ? sujet.pageImages : correction.pageImages;
                            const pageImg = isPagePill && pageNum > 0 ? thumbSource.find(p => p.pageNumber === pageNum) : null;
                            return (
                              <button key={si} onClick={() => {
                                if (pageImg) {
                                  setPreviewPage({ pageNum, thumb: pageImg.base64 });
                                }
                              }}
                                className={`px-2 py-0.5 rounded text-[10px] font-medium transition-all ${
                                  ss.status === 'done' ? 'bg-green-100 text-green-700' :
                                  ss.status === 'active' ? 'bg-blue-100 text-blue-700 animate-pulse' :
                                  ss.status === 'error' ? 'bg-red-100 text-red-700' :
                                  'bg-gray-50 text-gray-400'
                                } ${isPagePill ? 'cursor-pointer hover:ring-2 hover:ring-blue-400' : ''}`}>{ss.label}</button>
                            );
                          })}
                        </div>
                      )}
                    </div>
                  </div>
                  {/* Connector line */}
                  {idx < pipelineSteps.length - 1 && (
                    <div className="ml-[11px] w-0.5 h-2 bg-gray-200" />
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ─── PAGE PREVIEW MODAL ─── */}
        {previewPage && (
          <div className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4" onClick={() => setPreviewPage(null)}>
            <div className="bg-white rounded-2xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col" onClick={e => e.stopPropagation()}>
              <div className="flex items-center justify-between p-4 border-b">
                <h3 className="font-semibold text-gray-900">Page {previewPage.pageNum} — Coller un document</h3>
                <button onClick={() => setPreviewPage(null)} className="p-1.5 hover:bg-gray-100 rounded-lg text-gray-500 text-lg">&times;</button>
              </div>
              <div className="flex-1 overflow-y-auto p-4 grid grid-cols-1 lg:grid-cols-2 gap-4">
                {/* Page image */}
                <div className="border rounded-lg overflow-hidden bg-gray-50">
                  <img src={previewPage.thumb} alt={`Page ${previewPage.pageNum}`} className="w-full h-auto" />
                </div>
                {/* Paste zone for this page */}
                <div className="space-y-3">
                  <p className="text-sm text-gray-600">Collez l'image du document correspondant à cette page :</p>
                  <div>
                    <label className="block text-xs font-medium text-gray-600 mb-1">Nom du document</label>
                    <input type="text" value={manualName} onChange={e => setManualName(e.target.value)}
                      className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none"
                      placeholder={`Document ${documents.length + 1}`} />
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-gray-600 mb-1">Type</label>
                    <select value={manualType} onChange={e => setManualType(e.target.value)}
                      className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none">
                      <option value="figure">Figure</option><option value="graphique">Graphique</option>
                      <option value="tableau">Tableau</option><option value="schema">Schéma</option>
                      <option value="courbe">Courbe</option><option value="carte">Carte</option>
                    </select>
                  </div>
                  <div ref={previewPasteRef} onPaste={handlePaste} tabIndex={0}
                    className={`border-2 border-dashed rounded-xl p-4 text-center cursor-pointer focus:ring-2 focus:ring-purple-400 focus:outline-none transition min-h-[120px] flex flex-col items-center justify-center ${
                      manualPreview ? 'border-green-300 bg-green-50' : 'border-purple-300 bg-purple-50 hover:bg-purple-100'
                    }`}
                    onClick={() => previewPasteRef.current?.focus()}>
                    {manualPreview ? (
                      <div className="space-y-2">
                        <img src={manualPreview} alt="preview" className="max-h-32 rounded border mx-auto" />
                        {manualDescLoading && <p className="text-xs text-blue-500 animate-pulse">Description IA...</p>}
                        {!manualDescLoading && manualDesc && <p className="text-xs text-green-600 font-medium">&#10003; {manualDesc.slice(0, 80)}...</p>}
                        <button onClick={(e) => { e.stopPropagation(); setManualPreview(null); setManualDesc(''); }}
                          className="text-xs text-red-500 hover:text-red-700 underline">Supprimer</button>
                      </div>
                    ) : (
                      <div>
                        <p className="text-2xl mb-1 text-purple-300">&#128203;</p>
                        <p className="text-sm text-purple-700 font-medium">Ctrl+V pour coller</p>
                        <p className="text-xs text-purple-400">l'image sera décrite automatiquement</p>
                      </div>
                    )}
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-gray-600 mb-1">Description (auto-remplie)</label>
                    <textarea value={manualDesc} onChange={e => setManualDesc(e.target.value)} rows={3}
                      className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none resize-none" />
                    {manualDescLoading && <p className="text-xs text-blue-500 animate-pulse mt-1">Description IA en cours...</p>}
                  </div>
                  <button onClick={() => { addManualDocument(); setPreviewPage(null); }}
                    disabled={!manualPreview || !manualName.trim() || manualDescLoading}
                    className={`w-full py-2.5 rounded-lg text-sm font-semibold text-white transition ${
                      manualPreview && manualName.trim() && !manualDescLoading ? 'bg-purple-600 hover:bg-purple-700' : 'bg-gray-300 cursor-not-allowed'
                    }`}>
                    + Ajouter ce document (page {previewPage.pageNum})
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ─── EDIT DOCUMENT MODAL ─── */}
        {editDoc && (
          <div className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4" onClick={() => setEditDoc(null)}>
            <div className="bg-white rounded-2xl shadow-2xl max-w-3xl w-full max-h-[90vh] overflow-hidden flex flex-col" onClick={e => e.stopPropagation()}>
              <div className="flex items-center justify-between p-4 border-b">
                <h3 className="font-semibold text-gray-900">Modifier le document — {editDoc.name}</h3>
                <button onClick={() => setEditDoc(null)} className="p-1.5 hover:bg-gray-100 rounded-lg text-gray-500 text-lg">&times;</button>
              </div>
              <div className="flex-1 overflow-y-auto p-5 grid grid-cols-1 lg:grid-cols-2 gap-5">
                {/* Current / New image */}
                <div className="space-y-3">
                  <p className="text-xs font-medium text-gray-600">Image actuelle</p>
                  <div className="border rounded-lg overflow-hidden bg-gray-50">
                    <img src={editPreview || editDoc.dataUrl} alt={editDoc.name} className="w-full h-auto max-h-[300px] object-contain" />
                  </div>
                  {editPreview && (
                    <div className="flex items-center gap-2">
                      <span className="text-xs text-green-600 font-medium">&#10003; Nouvelle image collée</span>
                      <button onClick={() => { setEditPreview(null); setEditDesc(editDoc.visionDescription || editDoc.description); }}
                        className="text-xs text-red-500 hover:text-red-700 underline">Annuler</button>
                    </div>
                  )}
                  <div ref={editPasteRef} onPaste={handleEditPaste} tabIndex={0}
                    className="border-2 border-dashed border-orange-300 bg-orange-50 rounded-xl p-3 text-center cursor-pointer focus:ring-2 focus:ring-orange-400 focus:outline-none transition"
                    onClick={() => editPasteRef.current?.focus()}>
                    <p className="text-sm text-orange-700 font-medium">&#128203; Ctrl+V pour coller le document exact</p>
                    <p className="text-xs text-orange-400 mt-0.5">L'image et la description seront mises à jour</p>
                  </div>
                </div>
                {/* Edit fields */}
                <div className="space-y-3">
                  <div>
                    <label className="block text-xs font-medium text-gray-600 mb-1">Nom du document</label>
                    <input type="text" value={editName} onChange={e => setEditName(e.target.value)}
                      className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none" />
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-gray-600 mb-1">Type</label>
                    <select value={editType} onChange={e => setEditType(e.target.value)}
                      className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none">
                      <option value="figure">Figure</option><option value="graphique">Graphique</option>
                      <option value="tableau">Tableau</option><option value="schema">Schéma</option>
                      <option value="courbe">Courbe</option><option value="carte">Carte</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-gray-600 mb-1">Description</label>
                    <div className="relative">
                      <textarea value={editDesc} onChange={e => setEditDesc(e.target.value)} rows={5}
                        className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none resize-none" />
                      {editDescLoading && (
                        <div className="absolute inset-0 bg-white/80 rounded-lg flex items-center justify-center">
                          <span className="text-xs text-blue-600 font-medium animate-pulse">Description IA en cours...</span>
                        </div>
                      )}
                    </div>
                  </div>
                  <div className="text-xs text-gray-400 space-y-0.5">
                    <p>Source : {editDoc.source === 'auto' ? 'Détection automatique' : 'Ajout manuel'}</p>
                    <p>Dimensions : {editDoc.width}×{editDoc.height}px{editDoc.pageNumber > 0 && ` • page ${editDoc.pageNumber}`}</p>
                  </div>
                  <div className="flex gap-2 pt-2">
                    <button onClick={saveEditDoc} disabled={!editName.trim() || editDescLoading}
                      className={`flex-1 py-2.5 rounded-lg text-sm font-semibold text-white transition ${
                        editName.trim() && !editDescLoading ? 'bg-blue-600 hover:bg-blue-700' : 'bg-gray-300 cursor-not-allowed'
                      }`}>
                      Sauvegarder
                    </button>
                    <button onClick={() => setEditDoc(null)}
                      className="px-4 py-2.5 rounded-lg text-sm font-medium text-gray-600 bg-gray-100 hover:bg-gray-200 transition">
                      Annuler
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ─── DOCUMENTS LIVE SECTION (visible during extraction) ─── */}
        {step === 'extracting' && currentPhase !== 'done' && (documents.length > 0 || currentPhase === 'detect') && (
          <div className="bg-white rounded-xl shadow-sm border p-6 space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="font-semibold text-gray-900 text-lg">Documents détectés ({documents.length})</h2>
              <span className="text-xs text-gray-400">Vous pouvez coller des documents pendant l'extraction</span>
            </div>
            {documents.length > 0 && (
              <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-3">
                {documents.map(doc => (
                  <div key={doc.id} className="bg-gray-50 rounded-lg border overflow-hidden group cursor-pointer hover:ring-2 hover:ring-blue-400 transition" onClick={() => openEditDoc(doc)}>
                    <div className="relative">
                      <img src={doc.dataUrl} alt={doc.name} className="w-full h-32 object-contain bg-white p-1" />
                      <button onClick={(e) => { e.stopPropagation(); removeDocument(doc.id); }}
                        className="absolute top-1 right-1 p-1 bg-red-500 text-white rounded opacity-0 group-hover:opacity-100 transition text-xs">✕</button>
                      <span className={`absolute top-1 left-1 px-1.5 py-0.5 rounded-full text-[10px] font-medium ${doc.source === 'auto' ? 'bg-blue-100 text-blue-700' : 'bg-purple-100 text-purple-700'}`}>
                        {doc.source === 'auto' ? 'Auto' : 'Collé'}
                      </span>
                      <span className="absolute bottom-1 right-1 px-1.5 py-0.5 bg-white/90 rounded text-[10px] text-gray-500 opacity-0 group-hover:opacity-100 transition">✏️ Modifier</span>
                    </div>
                    <div className="p-2">
                      <p className="font-medium text-xs text-gray-900 truncate">{doc.name}</p>
                      {doc.describingStatus === 'loading' && <p className="text-[10px] text-blue-500 animate-pulse">Description IA...</p>}
                      {doc.visionDescription && <p className="text-[10px] text-gray-500 line-clamp-2">{doc.visionDescription}</p>}
                    </div>
                  </div>
                ))}
              </div>
            )}
            {/* Paste zone during extraction */}
            <div ref={pasteZoneRef} onPaste={handlePaste} tabIndex={0}
              className="border-2 border-dashed border-purple-300 bg-purple-50 rounded-xl p-4 text-center cursor-pointer focus:ring-2 focus:ring-purple-400 focus:outline-none transition"
              onClick={() => pasteZoneRef.current?.focus()}>
              <p className="text-sm text-purple-700 font-medium">Cliquez ici puis Ctrl+V pour coller un document</p>
              <p className="text-xs text-purple-400 mt-1">Ou utilisez le formulaire complet après l'extraction</p>
              {manualPreview && (
                <div className="mt-3 space-y-2">
                  <img src={manualPreview} alt="preview" className="max-h-32 mx-auto rounded border" />
                  <div className="flex items-center gap-2 justify-center">
                    <input type="text" value={manualName} onChange={e => setManualName(e.target.value)}
                      className="px-2 py-1 border rounded text-xs w-40" placeholder="Nom du document" />
                    {manualDescLoading ? <span className="text-xs text-blue-500 animate-pulse">Description IA...</span>
                      : <span className="text-xs text-green-600">✓ Décrit</span>}
                    <button onClick={addManualDocument} disabled={!manualName.trim() || manualDescLoading}
                      className={`px-3 py-1 rounded text-xs font-medium text-white ${manualName.trim() && !manualDescLoading ? 'bg-purple-600 hover:bg-purple-700' : 'bg-gray-300'}`}>
                      Ajouter
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* ─── RESULTS SECTION ─── */}
        {(step === 'results' || (step === 'extracting' && currentPhase === 'done')) && (
          <>
            {/* Stats bar */}
            <div className="bg-white rounded-xl shadow-sm border p-4 flex flex-wrap items-center gap-6">
              <Stat label="Pages sujet" value={sujet.totalPages} />
              {correction.file && <Stat label="Pages correction" value={correction.totalPages} />}
              <Stat label="Documents auto" value={autoDocCount} color="text-blue-600" />
              <Stat label="Documents manuels" value={manualDocCount} color="text-purple-600" />
              <Stat label="Total documents" value={documents.length} color="text-green-600" />
              <Stat label="Temps" value={fmtTime(elapsedSec)} color="text-gray-500" />
            </div>

            {/* Tabs */}
            <div className="flex gap-1 bg-white rounded-xl p-1 shadow-sm border">
              {([['text', 'Texte extrait'], ['documents', `Documents (${documents.length})`], ['json', 'Exam JSON']] as [ResultTab, string][]).map(
                ([key, label]) => (
                  <button key={key} onClick={() => setResultTab(key)}
                    className={`flex-1 py-2.5 rounded-lg text-sm font-medium transition ${resultTab === key ? 'bg-gray-900 text-white' : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'}`}>
                    {label}
                  </button>
                ),
              )}
            </div>

            {/* TEXT TAB */}
            {resultTab === 'text' && (
              <div className="space-y-4">
                <TextBlock title="Texte du Sujet" pages={sujet.ocrPages} fullText={sujetText} onReOcr={reOcrSujetPage} />
                {correction.file && <TextBlock title="Texte de la Correction" pages={correction.ocrPages} fullText={corrText} onReOcr={reOcrCorrPage} />}
              </div>
            )}

            {/* DOCUMENTS TAB */}
            {resultTab === 'documents' && (
              <div className="space-y-6">
                {documents.length > 0 && (
                  <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
                    {documents.map(doc => (
                      <div key={doc.id} className="bg-white rounded-xl shadow-sm border overflow-hidden group cursor-pointer hover:ring-2 hover:ring-blue-400 transition" onClick={() => openEditDoc(doc)}>
                        <div className="relative">
                          <img src={doc.dataUrl} alt={doc.name} className="w-full h-48 object-contain bg-gray-50 p-2" />
                          <button onClick={(e) => { e.stopPropagation(); removeDocument(doc.id); }}
                            className="absolute top-2 right-2 p-1.5 bg-red-500 text-white rounded-lg opacity-0 group-hover:opacity-100 transition text-xs">✕</button>
                          <span className={`absolute top-2 left-2 px-2 py-0.5 rounded-full text-xs font-medium ${doc.source === 'auto' ? 'bg-blue-100 text-blue-700' : 'bg-purple-100 text-purple-700'}`}>
                            {doc.source === 'auto' ? 'Auto' : 'Manuel'}
                          </span>
                          <span className="absolute bottom-2 right-2 px-2 py-1 bg-white/90 rounded-lg text-xs text-gray-600 font-medium opacity-0 group-hover:opacity-100 transition shadow">✏️ Modifier / Coller</span>
                        </div>
                        <div className="p-3 space-y-1">
                          <p className="font-semibold text-sm text-gray-900">{doc.name}</p>
                          <p className="text-xs text-gray-500">{doc.type} • {doc.width}×{doc.height}px{doc.pageNumber > 0 && ` • page ${doc.pageNumber}`}</p>
                          {doc.describingStatus === 'loading' && <p className="text-xs text-blue-500 animate-pulse">Description IA en cours...</p>}
                          {doc.visionDescription && <p className="text-xs text-gray-600 mt-1 leading-relaxed">{doc.visionDescription}</p>}
                          {!doc.visionDescription && doc.description && <p className="text-xs text-gray-500 italic">{doc.description}</p>}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
                {documents.length === 0 && !processing && (
                  <div className="text-center py-8 text-gray-400">Aucun document détecté. Ajoutez-en manuellement ci-dessous.</div>
                )}
                {/* Manual add form — paste or upload + auto-describe */}
                <div className="bg-white rounded-xl shadow-sm border p-6">
                  <h3 className="font-semibold text-gray-900 mb-4">Ajouter un document</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-3">
                      <div>
                        <label className="block text-xs font-medium text-gray-600 mb-1">Nom du document</label>
                        <input type="text" value={manualName} onChange={e => setManualName(e.target.value)}
                          className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none" placeholder="ex: Document 3" />
                      </div>
                      <div>
                        <label className="block text-xs font-medium text-gray-600 mb-1">Type</label>
                        <select value={manualType} onChange={e => setManualType(e.target.value)}
                          className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none">
                          <option value="figure">Figure</option><option value="graphique">Graphique</option>
                          <option value="tableau">Tableau</option><option value="schema">Schéma</option>
                          <option value="courbe">Courbe</option><option value="carte">Carte</option>
                        </select>
                      </div>
                      <div>
                        <label className="block text-xs font-medium text-gray-600 mb-1">Description (auto-remplie par Vision IA)</label>
                        <div className="relative">
                          <textarea value={manualDesc} onChange={e => setManualDesc(e.target.value)} rows={3}
                            className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none resize-none" placeholder="Collez ou chargez une image — la description sera générée automatiquement..." />
                          {manualDescLoading && (
                            <div className="absolute inset-0 bg-white/80 rounded-lg flex items-center justify-center">
                              <span className="text-xs text-blue-600 font-medium animate-pulse">Description IA en cours...</span>
                            </div>
                          )}
                        </div>
                      </div>
                      <div>
                        <label className="block text-xs font-medium text-gray-600 mb-1">Image (fichier ou coller)</label>
                        <input ref={manualFileRef} type="file" accept="image/*" onChange={handleManualFile}
                          className="w-full text-sm text-gray-500 file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100" />
                      </div>
                      <button onClick={addManualDocument} disabled={!manualPreview || !manualName.trim() || manualDescLoading}
                        className={`w-full py-2.5 rounded-lg text-sm font-semibold text-white transition ${manualPreview && manualName.trim() && !manualDescLoading ? 'bg-purple-600 hover:bg-purple-700' : 'bg-gray-300 cursor-not-allowed'}`}>
                        + Ajouter le document
                      </button>
                    </div>
                    {/* Paste zone */}
                    <div ref={pasteZoneRef} onPaste={handlePaste} tabIndex={0}
                      className={`border-2 border-dashed rounded-xl p-4 flex flex-col items-center justify-center cursor-pointer focus:ring-2 focus:ring-purple-400 focus:outline-none transition min-h-[220px] ${
                        manualPreview ? 'border-green-300 bg-green-50' : 'border-purple-300 bg-purple-50 hover:bg-purple-100'
                      }`}
                      onClick={() => pasteZoneRef.current?.focus()}>
                      {manualPreview ? (
                        <div className="text-center space-y-2">
                          <img src={manualPreview} alt="preview" className="max-h-44 rounded-lg border shadow-sm mx-auto" />
                          {manualDescLoading && <p className="text-xs text-blue-500 animate-pulse">Analyse IA en cours...</p>}
                          {!manualDescLoading && manualDesc && <p className="text-xs text-green-600 font-medium">✓ Description générée</p>}
                          <button onClick={(e) => { e.stopPropagation(); setManualPreview(null); setManualDesc(''); if (manualFileRef.current) manualFileRef.current.value = ''; }}
                            className="text-xs text-red-500 hover:text-red-700 underline">Supprimer l'image</button>
                        </div>
                      ) : (
                        <div className="text-center">
                          <p className="text-3xl mb-2 text-purple-300">📋</p>
                          <p className="text-sm text-purple-700 font-medium">Cliquez ici puis Ctrl+V</p>
                          <p className="text-xs text-purple-400 mt-1">pour coller une image du presse-papier</p>
                          <p className="text-xs text-purple-400 mt-0.5">La description sera générée automatiquement</p>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* JSON TAB */}
            {resultTab === 'json' && (
              <div className="space-y-4">
                <div className="bg-white rounded-xl shadow-sm border p-6 space-y-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="font-semibold text-gray-900">Structurer en JSON compatible Exam Viewer</h3>
                      <p className="text-xs text-gray-500 mt-1">
                        Combine sujet + correction en un seul JSON structuré avec parties, exercices, questions (QCM, vrai/faux, association, libre...)
                      </p>
                    </div>
                    <button onClick={generateStructuredExam} disabled={structuring || !sujetText}
                      className={`px-5 py-2.5 rounded-lg text-sm font-semibold text-white transition ${
                        structuring || !sujetText ? 'bg-gray-300 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-700'
                      }`}>
                      {structuring ? 'Structuration IA en cours...' : 'Générer le JSON structuré'}
                    </button>
                  </div>
                  {structureError && (
                    <div className="p-3 rounded-lg bg-red-50 text-red-700 text-sm">{structureError}</div>
                  )}
                  {structuring && (
                    <div className="flex items-center gap-3 p-4 bg-indigo-50 rounded-lg">
                      <div className="w-5 h-5 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
                      <span className="text-sm text-indigo-700">DeepSeek analyse le texte et structure l'examen... (peut prendre 30-60s)</span>
                    </div>
                  )}
                  {structuredExam && (
                    <div className="space-y-3">
                      <div className="flex items-center gap-3">
                        <span className="text-sm font-medium text-green-700">&#10003; JSON généré avec succès</span>
                        <span className="text-xs text-gray-500">
                          {structuredExam.parts?.length || 0} partie(s) •{' '}
                          {structuredExam.parts?.reduce((a: number, p: any) =>
                            a + (p.questions?.length || 0) + (p.exercises?.reduce((b: number, ex: any) => b + (ex.questions?.length || 0), 0) || 0), 0) || 0} question(s)
                        </span>
                        <button onClick={() => navigator.clipboard.writeText(JSON.stringify(structuredExam, null, 2))}
                          className="ml-auto px-3 py-1 bg-white border rounded text-xs text-gray-600 hover:bg-gray-50">Copier JSON</button>
                      </div>
                      <textarea readOnly value={JSON.stringify(structuredExam, null, 2)}
                        rows={Math.min(40, JSON.stringify(structuredExam, null, 2).split('\n').length + 2)}
                        className="w-full px-4 py-3 border rounded-lg text-xs font-mono bg-gray-50 text-gray-800 resize-y focus:ring-2 focus:ring-indigo-500 outline-none" />
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* ─── PUBLISH SECTION (only after JSON generation) ─── */}
            {structuredExam && (
            <div className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl shadow-sm border border-green-200 p-6 space-y-4">
              <div className="flex items-center gap-2 mb-1">
                <h2 className="font-semibold text-gray-900 text-lg">3. Publier aux élèves</h2>
                <span className="px-2 py-0.5 bg-green-100 text-green-700 rounded-full text-xs font-medium">Dernière étape</span>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-xs font-medium text-gray-600 mb-1">Titre de l'examen</label>
                  <input type="text" value={pubTitle} onChange={e => setPubTitle(e.target.value)}
                    className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-green-500 outline-none"
                    placeholder="Examen National SVT 2022 - Normale" />
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-600 mb-1">Année</label>
                  <input type="number" value={pubYear} onChange={e => setPubYear(Number(e.target.value))}
                    className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-green-500 outline-none" />
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-600 mb-1">Session</label>
                  <select value={pubSession} onChange={e => setPubSession(e.target.value)}
                    className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-green-500 outline-none">
                    <option>Normale</option><option>Rattrapage</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-600 mb-1">Matière (complet)</label>
                  <input type="text" value={pubSubjectFull} onChange={e => setPubSubjectFull(e.target.value)}
                    className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-green-500 outline-none"
                    placeholder="Sciences de la Vie et de la Terre - Filière Sciences Physiques" />
                </div>
                <div className="md:col-span-2">
                  <label className="block text-xs font-medium text-gray-600 mb-1">Note (optionnel)</label>
                  <input type="text" value={pubNote} onChange={e => setPubNote(e.target.value)}
                    className="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-green-500 outline-none"
                    placeholder="Il est permis d'utiliser la calculatrice non programmable" />
                </div>
              </div>

              {publishResult && (
                <div className={`p-3 rounded-lg text-sm font-medium ${publishResult.success ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                  {publishResult.message}
                </div>
              )}

              <button onClick={handlePublish} disabled={publishing || !pubTitle.trim()}
                className={`px-8 py-3 rounded-xl text-sm font-bold text-white transition shadow-lg ${
                  publishing || !pubTitle.trim() ? 'bg-gray-300 cursor-not-allowed' : 'bg-green-600 hover:bg-green-700 hover:shadow-xl'
                }`}>
                {publishing ? 'Publication en cours...' : '🚀 Publier cet examen aux élèves'}
              </button>
            </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}

// ── Sub-components ───────────────────────────────────────────

function StepIcon({ status }: { status: string }) {
  if (status === 'done') return (
    <div className="w-6 h-6 rounded-full bg-green-500 flex items-center justify-center flex-shrink-0">
      <svg className="w-3.5 h-3.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
      </svg>
    </div>
  );
  if (status === 'active') return (
    <div className="w-6 h-6 rounded-full bg-blue-500 flex items-center justify-center flex-shrink-0 animate-pulse">
      <div className="w-2 h-2 bg-white rounded-full" />
    </div>
  );
  if (status === 'error') return (
    <div className="w-6 h-6 rounded-full bg-red-500 flex items-center justify-center flex-shrink-0">
      <svg className="w-3.5 h-3.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
      </svg>
    </div>
  );
  return <div className="w-6 h-6 rounded-full bg-gray-200 flex-shrink-0" />;
}

function UploadBox({ fileRef, file, label, required, color, onPick, onChange }: {
  fileRef: React.RefObject<HTMLInputElement | null>; file: File | null; label: string; required?: boolean;
  color: string; onPick: () => void; onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
}) {
  return (
    <div className={`border-2 border-dashed rounded-xl p-5 text-center transition ${color || 'border-gray-300 hover:border-gray-400'}`}>
      <input ref={fileRef} type="file" accept=".pdf" className="hidden" onChange={onChange} />
      <p className="text-sm font-semibold text-gray-700 mb-2">{label} {required ? <span className="text-red-500">*</span> : <span className="text-gray-400">(optionnel)</span>}</p>
      {file ? <p className="text-sm text-blue-700">{file.name} ({(file.size / 1024 / 1024).toFixed(1)} Mo)</p>
        : <p className="text-xs text-gray-400">Glissez ou choisissez un fichier</p>}
      <button onClick={onPick} className="mt-3 px-4 py-1.5 bg-white border rounded-lg text-sm hover:bg-gray-50 transition">
        {file ? 'Changer' : 'Choisir un fichier'}
      </button>
    </div>
  );
}

function Stat({ label, value, color }: { label: string; value: number | string; color?: string }) {
  return (
    <div>
      <p className="text-xs text-gray-500">{label}</p>
      <p className={`text-lg font-bold ${color || 'text-gray-900'}`}>{value}</p>
    </div>
  );
}

function TextBlock({ title, pages, fullText, onReOcr }: {
  title: string; pages: PageOcr[]; fullText: string;
  onReOcr?: (pageNum: number) => Promise<void>;
}) {
  const [expanded, setExpanded] = useState(false);
  const [activePage, setActivePage] = useState<number | 'all'>('all');
  const doneCount = pages.filter(p => p.status === 'done').length;
  const loadingCount = pages.filter(p => p.status === 'active').length;

  const displayText = activePage === 'all'
    ? fullText
    : pages.find(p => p.pageNumber === activePage)?.text || '(aucun texte)';

  const activeStatus = activePage !== 'all' ? pages.find(p => p.pageNumber === activePage)?.status : undefined;

  return (
    <div className="bg-white rounded-xl shadow-sm border overflow-hidden">
      <button onClick={() => setExpanded(!expanded)}
        className="w-full px-6 py-4 flex items-center justify-between hover:bg-gray-50 transition">
        <div className="flex items-center gap-3">
          <h3 className="font-semibold text-gray-900">{title}</h3>
          <span className="text-xs text-gray-500">{doneCount}/{pages.length} pages{loadingCount > 0 && ` • ${loadingCount} en cours`}</span>
        </div>
        <span className="text-gray-400 text-lg">{expanded ? '▲' : '▼'}</span>
      </button>
      {expanded && (
        <div className="px-6 pb-6 space-y-3">
          {/* Page navigation tabs */}
          <div className="flex flex-wrap gap-1.5 items-center">
            <button onClick={() => setActivePage('all')}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition ${
                activePage === 'all' ? 'bg-gray-900 text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}>Tout</button>
            {pages.map(p => (
              <button key={p.pageNumber} onClick={() => setActivePage(p.pageNumber)}
                title={p.status === 'error' ? (p.error || 'Erreur OCR') : `${p.text.length} caractères`}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition ${
                  activePage === p.pageNumber
                    ? 'bg-blue-600 text-white'
                    : p.status === 'done' ? 'bg-green-50 text-green-700 hover:bg-green-100 border border-green-200'
                    : p.status === 'active' ? 'bg-yellow-50 text-yellow-700 animate-pulse border border-yellow-200'
                    : p.status === 'error' ? 'bg-red-50 text-red-700 border border-red-200'
                    : 'bg-gray-100 text-gray-500'
                }`}>
                Page {p.pageNumber}
                {p.status === 'done' && <span className="ml-1 opacity-60">({p.text.length}c)</span>}
              </button>
            ))}
          </div>

          {/* Text area */}
          <div className="relative">
            <textarea readOnly value={displayText}
              rows={Math.min(25, displayText.split('\n').length + 2)}
              className="w-full px-4 py-3 border rounded-lg text-sm font-mono bg-gray-50 text-gray-800 resize-y focus:ring-2 focus:ring-blue-500 outline-none" />
            <div className="absolute top-2 right-2 flex gap-1">
              {activePage !== 'all' && onReOcr && (
                <button
                  onClick={() => onReOcr(activePage)}
                  disabled={activeStatus === 'active'}
                  className="px-2 py-1 bg-amber-50 border border-amber-200 rounded text-xs text-amber-700 hover:bg-amber-100 transition disabled:opacity-50"
                  title="Re-extraire cette page">
                  {activeStatus === 'active' ? '⏳' : '🔄'} Re-OCR
                </button>
              )}
              <button onClick={() => navigator.clipboard.writeText(displayText)}
                className="px-2 py-1 bg-white border rounded text-xs text-gray-600 hover:bg-gray-100 transition">Copier</button>
            </div>
          </div>

          {/* Page char count summary */}
          {activePage === 'all' && (
            <div className="text-xs text-gray-400">
              {pages.filter(p => p.status === 'done').map(p =>
                `P${p.pageNumber}: ${p.text.length}c`
              ).join(' • ')}
              {' • Total: '}{fullText.length}c
            </div>
          )}
        </div>
      )}
    </div>
  );
}
