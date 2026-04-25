import { useState } from 'react';
import { Image, Table, ChevronDown, ChevronUp, CheckCircle2, BookOpen, Microscope, Maximize2, X } from 'lucide-react';
import LatexRenderer from './LatexRenderer';

interface ContextBlock {
  type: string;
  content: string;
  details?: any;
  src?: string;
}

interface DocumentBlock {
  id: string;
  type: string;
  title?: string;
  src?: string;
  description?: string;
  image_base64?: string;
}

interface QuestionData {
  index: number;
  content: string;
  details?: any;
  context?: ContextBlock[];
  documents?: DocumentBlock[];
  page_context?: string;
  points: number;
  type?: string;
  part?: string;
  exercise?: string;
  exercise_context?: string;
  parent_content?: string;
  schema?: { src: string; description?: string };
  correction?: { content: string; details?: any; answers?: any } | null;
}

interface Props {
  question: QuestionData;
  examId: string;
  showCorrection?: boolean;
  children?: React.ReactNode;
}

export default function QuestionRenderer({ question, examId, showCorrection = false, children }: Props) {
  const [expandedImages, setExpandedImages] = useState<Set<number>>(new Set());
  const [contextOpen, setContextOpen] = useState(true);
  const [zoomedImage, setZoomedImage] = useState<{ src: string; title: string } | null>(null);

  const toggleImage = (idx: number) => {
    setExpandedImages((prev) => {
      const next = new Set(prev);
      if (next.has(idx)) next.delete(idx);
      else next.add(idx);
      return next;
    });
  };

  const contextBlocks = question.context || [];

  const assetUrl = (src: string) => {
    const filename = src.split('/').pop();
    return `/api/v1/exam/assets/${examId}/${filename}`;
  };

  const documents = question.documents || [];
  const hasExerciseContext = question.exercise_context && question.exercise_context.trim();
  const hasSchema = question.schema && question.schema.src;
  const hasDocuments = documents.length > 0 || hasSchema;

  // Split exercise_context into context text and parent stem (if present)
  const contextParts = hasExerciseContext ? splitContext(question.exercise_context!) : null;

  return (
    <div className="space-y-3">

      {/* ═══════ Exercise Context — collapsible card with nice theme ═══════ */}
      {hasExerciseContext && contextParts && (
        <div className="rounded-2xl border border-slate-200/80 overflow-hidden bg-white shadow-sm">
          {/* Header bar with gradient accent */}
          <button
            onClick={() => setContextOpen((o) => !o)}
            className="w-full flex items-center gap-3 px-4 py-3 bg-gradient-to-r from-slate-50 to-blue-50/40 border-b border-slate-100 hover:from-slate-100/80 hover:to-blue-50/60 transition-colors"
          >
            <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center shadow-sm flex-shrink-0">
              <Microscope className="w-4 h-4 text-white" />
            </div>
            <div className="flex-1 text-left min-w-0">
              <p className="text-[13px] font-bold text-slate-800 truncate">{question.exercise || 'Contexte scientifique'}</p>
              {!contextOpen && (
                <p className="text-[11px] text-slate-400 truncate mt-0.5">Cliquer pour afficher l'énoncé</p>
              )}
            </div>
            {contextOpen
              ? <ChevronUp className="w-4 h-4 text-slate-400 flex-shrink-0" />
              : <ChevronDown className="w-4 h-4 text-slate-400 flex-shrink-0" />
            }
          </button>

          {/* Context body */}
          {contextOpen && (
            <div className="px-4 py-3.5 space-y-3">
              {/* Main context text */}
              {contextParts.mainContext && (
                <div className="relative pl-4 border-l-[3px] border-blue-400/60">
                  <LatexRenderer className="text-[13.5px] text-slate-700 leading-[1.75]">
                    {contextParts.mainContext}
                  </LatexRenderer>
                </div>
              )}
              {/* Parent stem (e.g. "En vous basant sur le document 2 :") */}
              {contextParts.parentStem && (
                <div className="flex items-start gap-2 bg-amber-50/70 border border-amber-200/50 rounded-lg px-3 py-2.5">
                  <BookOpen className="w-4 h-4 text-amber-600 mt-0.5 flex-shrink-0" />
                  <LatexRenderer className="text-[13px] text-amber-900 font-medium leading-relaxed">{contextParts.parentStem}</LatexRenderer>
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* ═══════ Documents — compact responsive grid with click-to-zoom ═══════ */}
      {hasDocuments && (() => {
        // Collect all imgable docs + schema
        const allDocs: Array<{ key: string; title: string; src: string | null; description?: string; type: string }> = [];
        documents.forEach((doc, idx) => {
          const imgSrc = doc.src
            ? (doc.src.startsWith('/api/') ? doc.src : assetUrl(doc.src))
            : doc.image_base64 ? `data:image/png;base64,${doc.image_base64}` : null;
          allDocs.push({ key: doc.id || `d${idx}`, title: doc.title || `Document ${idx + 1}`, src: imgSrc, description: doc.description, type: doc.type });
        });
        if (hasSchema) {
          allDocs.push({ key: 'schema', title: 'Document', src: assetUrl(question.schema!.src), type: 'schema' });
        }

        // Grid layout: single doc = full width ; multiple = 2 cols on md+
        const gridCols = allDocs.length >= 2 ? 'grid-cols-1 sm:grid-cols-2' : 'grid-cols-1';

        return (
          <div className={`grid ${gridCols} gap-2.5`}>
            {allDocs.map((doc) => (
              <div key={doc.key} className="bg-white border border-slate-200/70 rounded-2xl overflow-hidden shadow-sm flex flex-col">
                {/* Compact header */}
                <div className="flex items-center gap-2 px-3 py-2 bg-gradient-to-r from-slate-50/80 to-blue-50/30 border-b border-slate-100/80">
                  <div className={`w-5 h-5 rounded-md flex items-center justify-center flex-shrink-0 ${doc.type === 'schema' ? 'bg-blue-100' : 'bg-emerald-100'}`}>
                    {doc.type === 'schema'
                      ? <Image className="w-3 h-3 text-blue-600" />
                      : <Table className="w-3 h-3 text-emerald-600" />}
                  </div>
                  <span className="text-[11.5px] font-bold text-slate-700 truncate flex-1">{doc.title}</span>
                  {doc.src && (
                    <button
                      onClick={() => setZoomedImage({ src: doc.src!, title: doc.title })}
                      className="p-1 rounded hover:bg-white/70 text-slate-400 hover:text-blue-600 transition-colors"
                      title="Agrandir"
                    >
                      <Maximize2 className="w-3 h-3" />
                    </button>
                  )}
                </div>
                {/* Capped-height image, click to zoom */}
                {doc.src && (
                  <button
                    onClick={() => setZoomedImage({ src: doc.src!, title: doc.title })}
                    className="p-2 bg-slate-50/40 hover:bg-slate-50/80 transition-colors cursor-zoom-in group"
                  >
                    <img
                      src={doc.src}
                      alt={doc.title}
                      loading="lazy"
                      className="w-full max-h-[180px] object-contain rounded-lg border border-slate-100 group-hover:shadow-md transition-shadow"
                    />
                  </button>
                )}
                {doc.description && (
                  <div className="px-3 py-2 bg-slate-50/50 border-t border-slate-100/80 flex-1">
                    <p className="text-[10.5px] text-slate-500 leading-snug italic whitespace-pre-line line-clamp-3">
                      {doc.description}
                    </p>
                  </div>
                )}
              </div>
            ))}
          </div>
        );
      })()}

      {/* Zoom modal */}
      {zoomedImage && (
        <div
          onClick={() => setZoomedImage(null)}
          className="fixed inset-0 z-[100] bg-black/85 backdrop-blur-sm flex items-center justify-center p-4 animate-[fadeSlideIn_0.2s_ease-out]"
        >
          <button
            onClick={(e) => { e.stopPropagation(); setZoomedImage(null); }}
            className="absolute top-4 right-4 w-10 h-10 bg-white/10 hover:bg-white/20 rounded-full text-white flex items-center justify-center transition-colors"
            aria-label="Fermer"
          >
            <X className="w-5 h-5" />
          </button>
          <div className="max-w-6xl max-h-full flex flex-col items-center gap-3" onClick={(e) => e.stopPropagation()}>
            <p className="text-white text-sm font-bold">{zoomedImage.title}</p>
            <img
              src={zoomedImage.src}
              alt={zoomedImage.title}
              className="max-w-full max-h-[85vh] object-contain rounded-xl shadow-2xl"
            />
          </div>
        </div>
      )}

      {/* ═══════ Legacy context blocks ═══════ */}
      {contextBlocks.map((ctx, idx) => (
        <div key={idx}>
          {ctx.type === 'text' && (
            <div className="relative bg-white border border-slate-200/70 rounded-2xl overflow-hidden shadow-sm">
              <div className="absolute top-0 left-0 bottom-0 w-1 bg-gradient-to-b from-blue-400 to-indigo-400" />
              <LatexRenderer className="px-4 pl-5 py-3 text-[12.5px] text-slate-700 leading-[1.7]">
                {ctx.content}
              </LatexRenderer>
            </div>
          )}

          {ctx.type === 'schema' && ctx.src && (
            <div className="bg-white border border-slate-200/70 rounded-2xl overflow-hidden shadow-sm">
              <button onClick={() => toggleImage(idx)} className="w-full flex items-center justify-between px-3.5 py-2.5 hover:bg-slate-50/50 transition-colors">
                <div className="flex items-center gap-2.5 text-[12px] font-bold text-slate-700">
                  <div className="w-6 h-6 rounded-lg bg-blue-100 flex items-center justify-center">
                    <Image className="w-3 h-3 text-blue-600" />
                  </div>
                  {ctx.content || 'Document'}
                </div>
                {expandedImages.has(idx) ? <ChevronUp className="w-4 h-4 text-slate-400" /> : <ChevronDown className="w-4 h-4 text-slate-400" />}
              </button>
              {(expandedImages.has(idx) || true) && (
                <div className="px-2.5 pb-2.5">
                  <img src={assetUrl(ctx.src)} alt={ctx.content || 'Document'} className="w-full rounded-xl border border-slate-100" loading="lazy" />
                </div>
              )}
            </div>
          )}

          {ctx.type === 'table' && (
            <div className="bg-white border border-slate-200/70 rounded-2xl overflow-hidden shadow-sm">
              <div className="flex items-center gap-2.5 px-3.5 py-2.5">
                <div className="w-6 h-6 rounded-lg bg-emerald-100 flex items-center justify-center">
                  <Table className="w-3 h-3 text-emerald-600" />
                </div>
                <span className="text-[12px] font-bold text-slate-700">Tableau</span>
              </div>
              {ctx.src && (
                <div className="px-2.5 pb-2.5">
                  <img src={assetUrl(ctx.src)} alt="Tableau" className="w-full rounded-xl border border-slate-100" loading="lazy" />
                </div>
              )}
              {!ctx.src && ctx.content && (
                <div className="px-2.5 pb-2.5 text-xs text-slate-700 overflow-x-auto">
                  <div className="prose prose-sm max-w-none" dangerouslySetInnerHTML={{ __html: markdownTableToHtml(ctx.content) }} />
                </div>
              )}
            </div>
          )}
        </div>
      ))}

      {/* ═══════ Question content — main question card ═══════ */}
      <div className="relative bg-white border border-slate-200/70 rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition-shadow">
        {/* Animated rainbow accent bar */}
        <div className="absolute top-0 left-0 right-0 h-[3px] bg-gradient-to-r from-blue-500 via-indigo-500 to-violet-500 bg-[length:200%_100%] animate-gradient-shift" />
        <div className="px-4 py-3.5 pt-4">
          <div className="flex items-start justify-between gap-2 mb-2.5">
            <div className="flex items-center gap-2.5 min-w-0">
              <div className="relative flex-shrink-0">
                <div className="w-9 h-9 bg-gradient-to-br from-blue-500 via-indigo-500 to-violet-600 rounded-xl flex items-center justify-center text-white text-sm font-black shadow-lg shadow-indigo-500/30">
                  {question.index + 1}
                </div>
                {/* Subtle ping */}
                <span className="absolute inset-0 rounded-xl bg-indigo-400/30 animate-ping-slow pointer-events-none" />
              </div>
              <div className="min-w-0">
                <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Question</p>
                {question.parent_content && (
                  <LatexRenderer as="p" className="text-[11px] text-slate-400 font-medium truncate">{question.parent_content}</LatexRenderer>
                )}
              </div>
            </div>
            {question.points > 0 && (
              <span className="inline-flex items-center gap-1 text-[11px] font-bold text-white bg-gradient-to-r from-amber-500 to-orange-500 px-2.5 py-1 rounded-lg flex-shrink-0 shadow-sm shadow-amber-500/20">
                <span className="text-[9px]">⚡</span>
                {question.points} pt{question.points > 1 ? 's' : ''}
              </span>
            )}
          </div>
          <LatexRenderer as="div" className="text-slate-800 leading-[1.8] text-[15px] font-medium">{question.content}</LatexRenderer>
        </div>
      </div>

      {/* Children slot (used for mobile stacked layout) */}
      {children}

      {/* Correction (if shown) */}
      {showCorrection && question.correction && (
        <div className="relative bg-emerald-50/60 border border-emerald-200/60 rounded-2xl overflow-hidden">
          <div className="absolute top-0 left-0 bottom-0 w-1 bg-gradient-to-b from-emerald-400 to-teal-400" />
          <div className="px-4 pl-5 py-3">
            <div className="flex items-center gap-2 mb-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              <span className="text-[12px] font-bold text-emerald-700">Correction officielle</span>
            </div>
            <LatexRenderer className="text-slate-700 text-[12.5px] leading-[1.7]">
              {question.correction.content}
            </LatexRenderer>
          </div>
        </div>
      )}
    </div>
  );
}

/** Split exercise_context into main context + parent stem (last paragraph if short) */
function splitContext(text: string): { mainContext: string; parentStem: string | null } {
  const parts = text.split('\n\n');
  if (parts.length >= 2) {
    const last = parts[parts.length - 1].trim();
    // If the last part is a short directive (e.g. "En vous basant sur le document 2 :")
    if (last.length < 120 && (last.includes('document') || last.includes('En ') || last.endsWith(':'))) {
      return {
        mainContext: parts.slice(0, -1).join('\n\n').trim(),
        parentStem: last,
      };
    }
  }
  return { mainContext: text, parentStem: null };
}

function markdownTableToHtml(md: string): string {
  const lines = md.trim().split('\n');
  if (lines.length < 2) return `<p>${md}</p>`;

  let html = '<table class="w-full border-collapse border border-slate-200 text-xs rounded-lg overflow-hidden">';
  lines.forEach((line, i) => {
    if (line.trim().startsWith('|---') || line.trim().match(/^\|[\s-|]+\|$/)) return;
    const cells = line
      .split('|')
      .filter((c) => c.trim() !== '');
    const tag = i === 0 ? 'th' : 'td';
    const bgClass = i === 0 ? 'bg-slate-100 font-semibold text-slate-700' : 'text-slate-600';
    html += '<tr>';
    cells.forEach((cell) => {
      html += `<${tag} class="border border-slate-200 px-3 py-2 ${bgClass}">${cell.trim()}</${tag}>`;
    });
    html += '</tr>';
  });
  html += '</table>';
  return html;
}
