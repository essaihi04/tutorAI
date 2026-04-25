import { useState, useEffect, useMemo, useRef, forwardRef } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import html2canvas from 'html2canvas';
import { getExamDetail, evaluateExamAnswer, startExam as apiStartExam, saveExamProgress } from '../services/api';
import { useAuthStore } from '../stores/authStore';
import QuestionRenderer from '../components/exam/QuestionRenderer';
import AnswerInput from '../components/exam/AnswerInput';
import LatexRenderer from '../components/exam/LatexRenderer';
import {
  ArrowLeft, ArrowRight, Loader2, Award, BarChart3,
  BookOpen, FlaskConical, Trophy, ChevronDown, ChevronUp, Lightbulb,
  Save, RotateCcw, Target, Sparkles, Share2, X, Copy, Check, Send,
} from 'lucide-react';
import {
  getMention, toScoreOn20, getBacContextMessage,
  autosaveGet, autosaveSet, autosaveClear, autosaveSavedAt, timeAgo,
  extractScoreFromFeedback,
} from '../utils/examGrading';

/* Autosave key per exam (Practice mode) */
const practiceAutosaveKey = (examId: string) => `exam_practice_autosave_v1_${examId}`;

interface PracticeAutosave {
  currentQ: number;
  answers: Record<number, string>;
  feedbacks: Record<number, FeedbackData>;
  /* imageData is intentionally excluded to avoid bloating localStorage */
}

/* ------------------------------------------------------------------ */
/*  Types                                                               */
/* ------------------------------------------------------------------ */

interface Choice { letter: string; text: string; }

interface QuestionData {
  index: number;
  content: string;
  details?: any;
  context?: any[];
  documents?: any[];
  page_context?: string;
  points: number;
  type?: 'open' | 'qcm' | 'vrai_faux' | 'association' | 'schema';
  choices?: Choice[];
  items_left?: string[];
  items_right?: string[];
  correct_answer?: string | boolean;
  correction?: { content: string; details?: any; answers?: any } | null;
  part?: string;
  exercise?: string;
  exercise_context?: string;
  parent_content?: string;
}

interface PartMeta {
  name: string;
  points?: number;
  alternatives?: boolean;
  instruction?: string;
}

interface ExamData {
  id: string;
  subject: string;
  year: number;
  session: string;
  duration_minutes: number;
  coefficient: number;
  total_points: number;
  questions: QuestionData[];
  question_count: number;
  source?: string;
  parts_meta?: PartMeta[];
}

interface FeedbackData {
  feedback: string;
  correction: string;
  points_max: number;
}

interface ParsedFeedbackSection {
  title: string;
  content: string;
}

/* ------------------------------------------------------------------ */
/*  Grouping helper                                                     */
/* ------------------------------------------------------------------ */

interface ExerciseGroup {
  name: string;
  indices: number[];
}

interface PartGroup {
  name: string;
  shortName: string;
  points: number;
  icon: 'book' | 'flask';
  color: string;
  exercises: ExerciseGroup[];
  allIndices: number[];
  alternatives?: boolean;
  instruction?: string;
}

function groupByParts(questions: QuestionData[], partsMeta?: PartMeta[]): PartGroup[] {
  const partsMap = new Map<string, { exercises: Map<string, number[]>; direct: number[] }>();

  questions.forEach((q) => {
    const part = q.part || 'Questions';
    if (!partsMap.has(part)) partsMap.set(part, { exercises: new Map(), direct: [] });
    const entry = partsMap.get(part)!;
    if (q.exercise) {
      if (!entry.exercises.has(q.exercise)) entry.exercises.set(q.exercise, []);
      entry.exercises.get(q.exercise)!.push(q.index);
    } else {
      entry.direct.push(q.index);
    }
  });

  const parts: PartGroup[] = [];
  let idx = 0;
  for (const [name, data] of partsMap) {
    const isKnowledge = name.toLowerCase().includes('connaissance') || name.toLowerCase().includes('restitution');
    const exercises: ExerciseGroup[] = [];
    const allIndices: number[] = [];

    if (data.direct.length > 0) {
      exercises.push({ name: isKnowledge ? 'Questions de cours' : 'Questions', indices: data.direct });
      allIndices.push(...data.direct);
    }
    for (const [exName, exIndices] of data.exercises) {
      exercises.push({ name: exName, indices: exIndices });
      allIndices.push(...exIndices);
    }

    const points = allIndices.reduce((s, i) => s + (questions[i]?.points || 0), 0);

    const meta = partsMeta?.find((m) => m.name === name);
    parts.push({
      name,
      shortName: isKnowledge ? 'Connaissances' : 'Raisonnement',
      points: Math.round(points * 100) / 100,
      icon: isKnowledge ? 'book' : 'flask',
      color: isKnowledge ? 'blue' : 'emerald',
      exercises,
      allIndices,
      alternatives: meta?.alternatives,
      instruction: meta?.instruction,
    });
    idx++;
  }
  return parts;
}

const TYPE_BADGE: Record<string, { label: string; bg: string; text: string }> = {
  qcm: { label: 'QCM', bg: 'bg-violet-500/15', text: 'text-violet-200' },
  vrai_faux: { label: 'V / F', bg: 'bg-amber-500/15', text: 'text-amber-200' },
  open: { label: 'Rédaction', bg: 'bg-red-500', text: 'text-white' },
  schema: { label: 'Schéma', bg: 'bg-rose-500/15', text: 'text-rose-200' },
  association: { label: 'Association', bg: 'bg-yellow-500/15', text: 'text-yellow-200' },
};

function parseFeedbackSections(feedback: string): ParsedFeedbackSection[] {
  const normalized = feedback.replace(/\r/g, '').trim();
  if (!normalized) return [];

  const parts = normalized.split(/(?=^##\s+)/gm).map((item) => item.trim()).filter(Boolean);
  if (parts.length === 0) {
    return [{ title: 'Retour', content: normalized }];
  }

  return parts.map((part) => {
    const lines = part.split('\n');
    const firstLine = lines[0] || '';
    const title = firstLine.replace(/^##\s*/, '').trim() || 'Retour';
    const content = lines.slice(1).join('\n').trim();
    return { title, content };
  });
}

function extractNote(sections: ParsedFeedbackSection[]): { score: number; max: number } | null {
  const noteSection = sections.find((s) => s.title.toLowerCase() === 'note');
  if (!noteSection) return null;
  const match = noteSection.content.match(/(\d+(?:[.,]\d+)?)\s*\/\s*(\d+(?:[.,]\d+)?)/);
  if (!match) return null;
  return { score: parseFloat(match[1].replace(',', '.')), max: parseFloat(match[2].replace(',', '.')) };
}

function getSectionContent(sections: ParsedFeedbackSection[], key: string): string {
  return sections.find((s) => s.title.toLowerCase() === key.toLowerCase())?.content || '';
}

function renderBulletList(content: string, dotColor: string, textColor: string = 'text-white/85') {
  const lines = content.split('\n').filter((line) => line.trim() !== '');
  if (lines.length === 0) return null;

  return (
    <ul className="space-y-1.5">
      {lines.map((line, idx) => (
        <li key={idx} className={`flex items-start gap-2 text-[13px] ${textColor} leading-relaxed`}>
          <span className={`mt-[7px] h-1.5 w-1.5 rounded-full ${dotColor} flex-shrink-0`} />
          <LatexRenderer as="span">{line.replace(/^-\s*/, '')}</LatexRenderer>
        </li>
      ))}
    </ul>
  );
}

/** Parse model answer into Part 1 (concept) and Part 2 (answer) */
function parseModelAnswer(content: string): { concept: string; answer: string } {
  // Try to split on "Partie 1" / "Partie 2" markers
  const partie1Match = content.match(/(?:\*\*)?Partie\s*1[\s\-–:]*/i);
  const partie2Match = content.match(/(?:\*\*)?Partie\s*2[\s\-–:]*/i);

  if (partie1Match && partie2Match) {
    const idx1 = content.indexOf(partie1Match[0]);
    const idx2 = content.indexOf(partie2Match[0]);
    if (idx1 !== -1 && idx2 !== -1 && idx2 > idx1) {
      const afterP1 = idx1 + partie1Match[0].length;
      const concept = content.slice(afterP1, idx2).replace(/\*\*/g, '').trim();
      const afterP2 = idx2 + partie2Match[0].length;
      const answer = content.slice(afterP2).replace(/\*\*/g, '').trim();
      return { concept, answer };
    }
  }

  // Fallback: try to split on bold markers or line patterns
  const lines = content.split('\n');
  let conceptLines: string[] = [];
  let answerLines: string[] = [];
  let inAnswer = false;

  for (const line of lines) {
    const lower = line.toLowerCase();
    if (lower.includes('partie 2') || lower.includes('réponse complète') || lower.includes('réponse attendue')) {
      inAnswer = true;
      continue;
    }
    if (lower.includes('partie 1') || lower.includes('explication du concept')) {
      continue;
    }
    if (inAnswer) {
      answerLines.push(line);
    } else {
      conceptLines.push(line);
    }
  }

  // If we couldn't split meaningfully, treat all as concept + answer combined
  if (answerLines.length === 0) {
    return { concept: content, answer: '' };
  }

  return {
    concept: conceptLines.join('\n').trim() || content,
    answer: answerLines.join('\n').trim(),
  };
}

/** Display model answer with concept + answer sections */
function ModelAnswerDisplay({ content }: { content: string }) {
  const { concept, answer } = parseModelAnswer(content);

  return (
    <div className="space-y-3 mt-2">
      {/* Part 1: Concept explanation */}
      {concept && (
        <div className="bg-emerald-500/10 border border-emerald-400/30 rounded-xl px-3.5 py-3">
          <div className="flex items-center gap-1.5 mb-2">
            <span className="text-xs">🎓</span>
            <span className="text-[11px] font-bold text-emerald-200 uppercase tracking-wider">Explication du concept</span>
          </div>
          <LatexRenderer className="text-[13px] text-white/85 leading-[1.7]">{concept}</LatexRenderer>
        </div>
      )}

      {/* Part 2: Model answer */}
      {answer && (
        <div className="relative pl-3.5 border-l-[3px] border-violet-400/50">
          <p className="text-[11px] font-bold text-violet-200 uppercase tracking-wider mb-1">Réponse attendue</p>
          <LatexRenderer className="text-[13px] text-white/85 leading-[1.7]">{answer}</LatexRenderer>
        </div>
      )}

      {/* If parsing failed, show raw content */}
      {!concept && !answer && (
        <div className="relative pl-3.5 border-l-[3px] border-violet-400/50">
          <p className="text-[11px] font-bold text-violet-200 uppercase tracking-wider mb-1">Réponse modèle</p>
          <LatexRenderer className="text-[13px] text-white/85 leading-[1.7]">{content}</LatexRenderer>
        </div>
      )}
    </div>
  );
}

function FeedbackCard({ feedback }: { feedback: string; accentText: string; accentLight: string }) {
  const [showModel, setShowModel] = useState(false);
  const sections = parseFeedbackSections(feedback);
  const note = extractNote(sections);
  const notePercent = note ? Math.round((note.score / note.max) * 100) : 0;

  // Animated score counting up (runs when note changes)
  const [displayScore, setDisplayScore] = useState(0);
  const [displayPercent, setDisplayPercent] = useState(0);
  useEffect(() => {
    if (!note) return;
    setDisplayScore(0);
    setDisplayPercent(0);
    const duration = 900;
    const start = performance.now();
    let raf = 0;
    const step = (t: number) => {
      const p = Math.min(1, (t - start) / duration);
      const eased = 1 - Math.pow(1 - p, 3); // easeOutCubic
      setDisplayScore(+(note.score * eased).toFixed(note.score % 1 === 0 ? 0 : 2));
      setDisplayPercent(notePercent * eased);
      if (p < 1) raf = requestAnimationFrame(step);
    };
    raf = requestAnimationFrame(step);
    return () => cancelAnimationFrame(raf);
  }, [note?.score, note?.max, notePercent]);

  // Score tier — more encouraging labels
  const tier = note
    ? note.score >= note.max * 0.8 ? 'excellent'
    : note.score >= note.max * 0.5 ? 'partial'
    : 'weak'
    : 'unknown';

  const tierConfig = {
    excellent: { color: 'from-emerald-500 to-teal-500', ring: 'text-emerald-500', bg: 'from-emerald-500/10 to-teal-50', border: 'border-emerald-400/30', label: 'Excellent !', emoji: '🏆', msg: 'Tu maîtrises ce point — continue !' },
    partial:   { color: 'from-amber-500 to-orange-500', ring: 'text-amber-500',   bg: 'from-amber-500/10 to-orange-500/15', border: 'border-amber-400/30',   label: 'Bien joué',    emoji: '💪', msg: 'Presque là — quelques détails à peaufiner' },
    weak:      { color: 'from-rose-500 to-pink-500',    ring: 'text-rose-500',    bg: 'from-rose-500/10 to-pink-50',    border: 'border-white/10',    label: 'On s\'accroche', emoji: '🤔', msg: 'Reprends le cours puis retente — tu vas y arriver !' },
    unknown:   { color: 'from-slate-500 text-white',  ring: 'text-white/55',   bg: 'from-slate-500/10 to-white',     border: 'border-white/10',   label: '',             emoji: '📋', msg: '' },
  };
  const tc = tierConfig[tier];

  // Extract sections
  const appreciation = getSectionContent(sections, 'appréciation générale');
  const pointsReussis = getSectionContent(sections, 'points réussis');
  const ameliorer = getSectionContent(sections, "ce qu'il faut améliorer");
  const conseil = getSectionContent(sections, 'conseil méthode');
  const reponseModele = getSectionContent(sections, 'réponse attendue en mieux')
    || getSectionContent(sections, 'réponse modèle');

  const hasAnalysis = appreciation || pointsReussis || ameliorer;
  const hasModelAnswer = conseil || reponseModele;

  // Circle geometry
  const ringRadius = 26;
  const ringCircumference = 2 * Math.PI * ringRadius;
  const ringOffset = ringCircumference * (1 - displayPercent / 100);

  return (
    <div className="space-y-3">

      {/* ── Score card — circular ring, animated count-up ── */}
      {note && (
        <div className={`relative rounded-2xl border overflow-hidden bg-gradient-to-br ${tc.bg} ${tc.border}`}>
          {/* Decorative blur */}
          <div className={`absolute -top-8 -right-8 w-32 h-32 rounded-full bg-gradient-to-br ${tc.color} opacity-10 blur-2xl`} />
          <div className="relative flex items-center gap-4 p-4">
            {/* Circular progress ring */}
            <div className="relative flex-shrink-0">
              <svg width="64" height="64" viewBox="0 0 64 64" className="-rotate-90">
                {/* Track */}
                <circle cx="32" cy="32" r={ringRadius} fill="none" stroke="currentColor" strokeWidth="5" className="text-white/70" />
                {/* Progress */}
                <circle
                  cx="32" cy="32" r={ringRadius}
                  fill="none"
                  strokeWidth="5"
                  strokeLinecap="round"
                  stroke={`url(#grad-${tier})`}
                  strokeDasharray={ringCircumference}
                  strokeDashoffset={ringOffset}
                  style={{ transition: 'stroke-dashoffset 0.1s linear' }}
                />
                <defs>
                  <linearGradient id={`grad-${tier}`} x1="0" y1="0" x2="1" y2="1">
                    <stop offset="0%" stopColor={tier === 'excellent' ? '#10b981' : tier === 'partial' ? '#f59e0b' : tier === 'weak' ? '#f43f5e' : '#64748b'} />
                    <stop offset="100%" stopColor={tier === 'excellent' ? '#14b8a6' : tier === 'partial' ? '#f97316' : tier === 'weak' ? '#ec4899' : '#475569'} />
                  </linearGradient>
                </defs>
              </svg>
              {/* Center number */}
              <div className="absolute inset-0 flex items-center justify-center">
                <span className="text-base font-black text-white tabular-nums">{Math.round(displayPercent)}%</span>
              </div>
            </div>

            {/* Score + tier label + message */}
            <div className="flex-1 min-w-0">
              <div className="flex items-baseline gap-1.5 mb-0.5">
                <span className="text-2xl font-black text-white tabular-nums">{displayScore}</span>
                <span className="text-sm font-bold text-white/55">/{note.max}</span>
                {tc.label && (
                  <span className={`ml-2 text-[10px] font-bold px-2 py-0.5 rounded-full bg-gradient-to-r ${tc.color} text-white shadow-sm`}>
                    {tc.emoji} {tc.label}
                  </span>
                )}
              </div>
              {tc.msg && (
                <p className="text-[11.5px] text-white/70 leading-snug">{tc.msg}</p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* ── Analyse — single card combining feedback ── */}
      {hasAnalysis && (
        <div className="glass rounded-2xl overflow-hidden">
          {/* Appreciation as header */}
          {appreciation && (
            <div className="px-4 py-3 border-b border-white/5 bg-gradient-to-r from-slate-500/10 to-blue-500/10">
              <LatexRenderer className="text-[13px] text-white/85 leading-relaxed">{appreciation}</LatexRenderer>
            </div>
          )}

          <div className="px-4 py-3 space-y-3">
            {/* Points réussis */}
            {pointsReussis && (
              <div>
                <div className="flex items-center gap-1.5 mb-1.5">
                  <span className="text-xs">✅</span>
                  <span className="text-[11px] font-bold text-emerald-200 uppercase tracking-wider">Acquis</span>
                </div>
                {renderBulletList(pointsReussis, 'bg-emerald-500', 'text-white/70')}
              </div>
            )}

            {/* Ce qu'il faut améliorer */}
            {ameliorer && (
              <div>
                <div className="flex items-center gap-1.5 mb-1.5">
                  <span className="text-xs">📝</span>
                  <span className="text-[11px] font-bold text-amber-200 uppercase tracking-wider">À compléter</span>
                </div>
                {renderBulletList(ameliorer, 'bg-amber-500', 'text-white/70')}
              </div>
            )}
          </div>
        </div>
      )}

      {/* ── Réponse modèle — expandable with concept explanation ── */}
      {hasModelAnswer && (
        <div className="rounded-2xl border border-violet-400/30 bg-violet-500/10 overflow-hidden shadow-sm">
          <button
            onClick={() => setShowModel((v) => !v)}
            className="w-full flex items-center gap-2.5 px-4 py-3 hover:bg-violet-500/15 transition-colors"
          >
            <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-purple-500 to-violet-600 flex items-center justify-center flex-shrink-0 shadow-sm">
              <span className="text-white text-[11px]">📖</span>
            </div>
            <div className="flex-1 text-left min-w-0">
              <p className="text-[13px] font-bold text-violet-100">
                {showModel ? 'Réponse modèle & méthode' : 'Voir la réponse modèle'}
              </p>
            </div>
            {showModel
              ? <ChevronUp className="w-4 h-4 text-violet-300 flex-shrink-0" />
              : <ChevronDown className="w-4 h-4 text-violet-300 flex-shrink-0" />
            }
          </button>

          {showModel && (
            <div className="px-4 pb-3.5 space-y-3 border-t border-white/10">
              {/* Conseil méthode */}
              {conseil && (
                <div className="flex items-start gap-2 bg-blue-500 border border-blue-400/30 rounded-xl px-3 py-2.5 mt-3">
                  <span className="text-sm mt-0.5 flex-shrink-0">💡</span>
                  <div>
                    <p className="text-[11px] font-bold text-blue-200 uppercase tracking-wider mb-0.5">Conseil</p>
                    <LatexRenderer className="text-[13px] text-blue-100 leading-relaxed">{conseil}</LatexRenderer>
                  </div>
                </div>
              )}

              {/* Réponse modèle - split into Concept + Answer */}
              {reponseModele && (
                <ModelAnswerDisplay content={reponseModele} />
              )}
            </div>
          )}
        </div>
      )}

      {/* ── Fallback: sections that don't match known keys ── */}
      {sections
        .filter((s) => {
          const k = s.title.toLowerCase();
          return k !== 'note' && k !== 'appréciation générale' && k !== 'points réussis'
            && k !== "ce qu'il faut améliorer" && k !== 'conseil méthode'
            && k !== 'réponse attendue en mieux' && k !== 'réponse modèle';
        })
        .map((section, idx) => (
          <div key={`extra-${idx}`} className="glass rounded-xl p-4">
            <h4 className="text-[13px] font-bold text-white/85 mb-2">{section.title}</h4>
            <p className="text-[13px] text-white/70 leading-relaxed whitespace-pre-line">{section.content}</p>
          </div>
        ))
      }
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  Main component                                                      */
/* ------------------------------------------------------------------ */

export default function ExamPractice() {
  const { examId } = useParams<{ examId: string }>();
  const navigate = useNavigate();

  const [exam, setExam] = useState<ExamData | null>(null);
  const [loading, setLoading] = useState(true);
  const [currentQ, setCurrentQ] = useState(0);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [imageData, setImageData] = useState<Record<number, string | null>>({});
  const [feedbacks, setFeedbacks] = useState<Record<number, FeedbackData>>({});
  const [submitting, setSubmitting] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [activePart, setActivePart] = useState(0);
  const [lastSavedAt, setLastSavedAt] = useState<number | null>(null);
  const [resumeToast, setResumeToast] = useState<{ savedAt: number; answered: number } | null>(null);
  const attemptIdRef = useRef<string | null>(null);

  // Restore state from sessionStorage when returning from explain mode
  useEffect(() => {
    const saved = sessionStorage.getItem(`exam_state_${examId}`);
    if (saved) {
      try {
        const state = JSON.parse(saved);
        if (state.currentQ != null) setCurrentQ(state.currentQ);
        if (state.answers) setAnswers(state.answers);
        if (state.feedbacks) setFeedbacks(state.feedbacks);
        if (state.imageData) setImageData(state.imageData);
      } catch {}
      sessionStorage.removeItem(`exam_state_${examId}`);
      return;
    }

    // Try long-term autosave (localStorage)
    if (examId) {
      const saved = autosaveGet<PracticeAutosave>(practiceAutosaveKey(examId));
      const savedAt = autosaveSavedAt(practiceAutosaveKey(examId));
      if (saved && savedAt) {
        if (saved.currentQ != null) setCurrentQ(saved.currentQ);
        if (saved.answers) setAnswers(saved.answers);
        if (saved.feedbacks) setFeedbacks(saved.feedbacks);
        const answeredCount = Object.values(saved.answers || {}).filter((v) => (v || '').toString().trim()).length;
        if (answeredCount > 0 || Object.keys(saved.feedbacks || {}).length > 0) {
          setResumeToast({ savedAt, answered: answeredCount });
        }
      }
    }
  }, [examId]);

  useEffect(() => { if (examId) loadExam(); }, [examId]);

  // ── Autosave (debounced, 800 ms after last change — local + server) ──
  useEffect(() => {
    if (!examId || loading) return;
    const answerCount = Object.keys(answers).filter((k) => answers[Number(k)]?.trim()).length;
    const fbCount = Object.keys(feedbacks).length;
    if (answerCount === 0 && fbCount === 0) return;
    const t = setTimeout(() => {
      const payload: PracticeAutosave = { currentQ, answers, feedbacks };
      autosaveSet(practiceAutosaveKey(examId), payload);
      setLastSavedAt(Date.now());
      // Sync to server
      if (attemptIdRef.current) {
        const answersStr: Record<string, string> = {};
        Object.entries(answers).forEach(([k, v]) => { if (v?.trim()) answersStr[k] = String(v); });
        saveExamProgress(attemptIdRef.current, {
          answers: answersStr,
          current_question_index: currentQ,
        }).catch(() => {});
      }
    }, 800);
    return () => clearTimeout(t);
  }, [examId, loading, currentQ, answers, feedbacks]);

  // Auto-dismiss the resume toast after a few seconds
  useEffect(() => {
    if (!resumeToast) return;
    const t = setTimeout(() => setResumeToast(null), 8000);
    return () => clearTimeout(t);
  }, [resumeToast]);

  const loadExam = async () => {
    setLoading(true);
    try {
      const res = await getExamDetail(examId!);
      setExam(res.data);
      // Register/resume attempt on server
      if (examId) {
        try {
          const startRes = await apiStartExam(examId, 'practice');
          attemptIdRef.current = startRes.data.attempt_id || null;
        } catch (e) { console.error('Failed to register practice exam start:', e); }
      }
    }
    catch (e) { console.error('Failed to load exam:', e); }
    finally { setLoading(false); }
  };

  const parts = useMemo(() => (exam ? groupByParts(exam.questions, exam.parts_meta) : []), [exam]);

  // When navigating to a question, update the active part
  useEffect(() => {
    if (!exam || parts.length === 0) return;
    const partIdx = parts.findIndex((p) => p.allIndices.includes(currentQ));
    if (partIdx >= 0 && partIdx !== activePart) setActivePart(partIdx);
  }, [currentQ, parts]);

  const handleEvaluate = async () => {
    if (!exam || !examId) return;
    const answer = answers[currentQ];
    const image = imageData[currentQ];
    if (!answer?.trim() && !image) return;
    setSubmitting(true);
    try {
      const res = await evaluateExamAnswer(examId, currentQ, answer || '', image, attemptIdRef.current);
      setFeedbacks((prev) => ({ ...prev, [currentQ]: res.data }));
      // Sync progress after evaluation
      if (attemptIdRef.current) {
        const answersStr: Record<string, string> = {};
        Object.entries(answers).forEach(([k, v]) => { if (v?.trim()) answersStr[k] = String(v); });
        saveExamProgress(attemptIdRef.current, {
          answers: answersStr,
          current_question_index: currentQ,
        }).catch(() => {});
      }
    } catch (e: any) { console.error('Evaluation failed:', e); }
    finally { setSubmitting(false); }
  };

  const handleExplain = () => {
    if (!exam || !examId) return;
    const q = exam.questions[currentQ];
    const hasAnswer = feedbacks[currentQ] != null;
    const correction = q.correction;
    const corrText = typeof correction === 'object' && correction ? (correction.content || '') : '';

    // Save exam state so we can restore it when returning
    sessionStorage.setItem(`exam_state_${examId}`, JSON.stringify({
      currentQ, answers, feedbacks, imageData,
    }));

    // Save explain context for LearningSession
    sessionStorage.setItem('explain_context', JSON.stringify({
      questionContent: q.content,
      questionType: q.type || 'open',
      points: q.points,
      parentContent: q.parent_content || '',
      exerciseContext: q.exercise_context || '',
      correction: corrText,
      hasAnswer,
      subject: exam.subject,
      examTitle: `${exam.subject} ${exam.year} ${exam.session}`,
    }));
    sessionStorage.setItem('explain_return_path', `/exam/practice/${examId}`);

    navigate('/exam-explain');
  };

  const goNext = () => { if (exam && currentQ < exam.questions.length - 1) setCurrentQ(currentQ + 1); };
  const goPrev = () => { if (currentQ > 0) setCurrentQ(currentQ - 1); };

  const evaluatedCount = Object.keys(feedbacks).length;

  /* ---------- Loading ---------- */
  if (loading || !exam) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-[#070718] text-white gap-4">
        <Loader2 className="w-12 h-12 text-indigo-300 animate-spin" />
        <p className="text-sm text-white/60 animate-pulse">Chargement de l'examen…</p>
      </div>
    );
  }

  const question = exam.questions[currentQ];
  const hasFeedback = feedbacks[currentQ] != null;
  const currentPartData = parts[activePart];

  /* ---------- Results ---------- */
  if (showResults) {
    return (
      <ExamPracticeResults
        exam={exam}
        parts={parts}
        feedbacks={feedbacks}
        answers={answers}
        onBack={() => navigate('/exam')}
        onContinue={() => {
          // Jump to the first unevaluated-but-answered question (or the first
          // unanswered one) so the student resumes exactly where it's useful.
          const firstMissing = exam.questions.findIndex((_, i) => !feedbacks[i]);
          if (firstMissing >= 0) setCurrentQ(firstMissing);
          setShowResults(false);
        }}
        onRetry={() => {
          if (examId) autosaveClear(practiceAutosaveKey(examId));
          setAnswers({});
          setFeedbacks({});
          setImageData({});
          setCurrentQ(0);
          setShowResults(false);
        }}
      />
    );
  }

  /* ---------- Color helpers ---------- */
  const c = currentPartData?.color || 'blue';
  const accentMap: Record<string, { bg: string; bgLight: string; border: string; text: string; gradient: string }> = {
    blue: { bg: 'bg-blue-600', bgLight: 'bg-blue-500/15', border: 'border-blue-400/30', text: 'text-blue-200', gradient: 'from-blue-600 to-indigo-600' },
    emerald: { bg: 'bg-emerald-600', bgLight: 'bg-emerald-500/15', border: 'border-emerald-400/30', text: 'text-emerald-200', gradient: 'from-emerald-600 to-teal-600' },
  };
  const accent = accentMap[c] || accentMap.blue;

  const badge = TYPE_BADGE[question.type || 'open'];
  const isExtractedExam = exam.source === 'extracted';

  return (
    <div className="h-screen flex flex-col bg-[#070718] text-white relative">

      {/* Resume toast */}
      {resumeToast && (
        <div className="fixed top-4 right-4 z-50 max-w-sm glass-strong border border-blue-400/30 shadow-xl rounded-2xl overflow-hidden animate-in slide-in-from-top-4">
          <div className="bg-gradient-to-r from-blue-600 to-indigo-600 px-4 py-2.5 flex items-center gap-2">
            <Save className="w-4 h-4 text-white" />
            <span className="text-xs font-bold text-white">Progression restaurée</span>
            <button onClick={() => setResumeToast(null)} className="ml-auto text-white/80 hover:text-white text-lg leading-none">×</button>
          </div>
          <div className="p-3">
            <p className="text-xs text-white/70 leading-relaxed">
              <b>{resumeToast.answered}</b> réponse{resumeToast.answered > 1 ? 's' : ''} retrouvée{resumeToast.answered > 1 ? 's' : ''} —
              sauvegardé {timeAgo(resumeToast.savedAt)}.
            </p>
            <button
              onClick={() => {
                if (examId) autosaveClear(practiceAutosaveKey(examId));
                setAnswers({});
                setFeedbacks({});
                setCurrentQ(0);
                setResumeToast(null);
              }}
              className="mt-2 text-[11px] font-semibold text-rose-300 hover:text-rose-200 flex items-center gap-1"
            >
              <RotateCcw className="w-3 h-3" /> Tout réinitialiser
            </button>
          </div>
        </div>
      )}

      {/* ===================== COMPACT HEADER ===================== */}
      <header className="backdrop-blur-2xl bg-[#070718]/70 border-b border-white/5 flex-shrink-0 z-30">
        <div className="max-w-[1600px] mx-auto px-3 lg:px-5">
          {/* Single row: back + title + question dots + nav + results */}
          <div className="flex items-center gap-2 py-2">
            {/* Back */}
            <button onClick={() => navigate('/exam')} className="p-1.5 rounded-lg hover:bg-white/10 text-white/40 transition-colors flex-shrink-0">
              <ArrowLeft className="w-4 h-4" />
            </button>

            {/* Title */}
            <div className="min-w-0 flex-shrink-0">
              <h1 className="text-sm font-bold text-white truncate">
                {exam.subject} — {(exam.session || '').toLowerCase() === 'rattrapage' ? 'Rattrapage' : 'Normale'} {exam.year}
              </h1>
              {!isExtractedExam && (
                <div className="flex items-center gap-2">
                  <span className="text-[10px] text-white/40">{evaluatedCount}/{exam.questions.length}</span>
                  <div className="w-16 bg-slate-100 rounded-full h-1">
                    <div className={`h-1 rounded-full bg-gradient-to-r ${accent.gradient} transition-all`} style={{ width: `${exam.questions.length > 0 ? Math.round((evaluatedCount / exam.questions.length) * 100) : 0}%` }} />
                  </div>
                </div>
              )}
            </div>

            {/* Separator */}
            {!isExtractedExam && <div className="w-px h-7 bg-white/10 mx-1 hidden lg:block" />}

            {/* Question dots - scrollable */}
            <div className={`flex-1 min-w-0 hidden lg:flex items-center gap-1 overflow-x-auto py-1 scrollbar-none ${isExtractedExam ? 'invisible' : ''}`}>
              {exam.questions.map((_q, qIdx) => {
                const isCurrent = qIdx === currentQ;
                const qBadge = TYPE_BADGE[_q.type || 'open'];
                return (
                  <button
                    key={qIdx}
                    onClick={() => setCurrentQ(qIdx)}
                    title={`Q${qIdx + 1} — ${qBadge.label} (${_q.points} pts)`}
                    className={`relative w-7 h-7 rounded-lg text-[10px] font-bold transition-all flex-shrink-0 ${
                      isCurrent
                        ? `ring-2 ring-offset-1 ${c === 'blue' ? 'ring-blue-400 bg-blue-600' : 'ring-emerald-400 bg-emerald-600'} text-white`
                        : feedbacks[qIdx]
                        ? 'bg-emerald-500 text-white'
                        : answers[qIdx]?.trim()
                        ? 'bg-amber-500/15 text-amber-200'
                        : 'bg-white/5 text-white/55 hover:bg-white/10'
                    }`}
                  >
                    {qIdx + 1}
                  </button>
                );
              })}
            </div>

            {/* Navigation arrows */}
            <div className="flex items-center gap-1 flex-shrink-0">
              <button onClick={goPrev} disabled={currentQ === 0} className="p-1.5 rounded-lg border border-white/10 text-white/55 hover:bg-white/[.06] disabled:opacity-30 transition-colors flex-shrink-0">
                <ArrowLeft className="w-3.5 h-3.5" />
              </button>
              <span className="text-[11px] font-bold text-white/55 min-w-[40px] text-center">{currentQ + 1}/{exam.questions.length}</span>
              <button onClick={goNext} disabled={currentQ >= exam.questions.length - 1} className={`p-1.5 rounded-lg text-white transition-all disabled:opacity-30 bg-gradient-to-r ${accent.gradient}`}>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>

            {/* Autosave indicator */}
            {lastSavedAt && (
              <div
                className="hidden lg:flex items-center gap-1 px-2 py-1 rounded-lg bg-emerald-500/15 border border-emerald-400/30 text-emerald-200 text-[10px] font-semibold flex-shrink-0"
                title={`Sauvegarde : ${timeAgo(lastSavedAt)}`}
              >
                <Save className="w-3 h-3" />
                <span className="hidden lg:inline">Sauvegardé</span>
              </div>
            )}

            {/* Results */}
            <button
              onClick={() => setShowResults(true)}
              className="hidden sm:flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 text-white rounded-lg text-xs font-medium hover:bg-slate-700 transition-colors flex-shrink-0"
            >
              <BarChart3 className="w-3.5 h-3.5" /> <span className="hidden lg:inline">Résultats</span>
            </button>
          </div>
        </div>
      </header>

      {/* ===================== 2-COLUMN BODY ===================== */}
      <div className="flex-1 min-h-0 flex">
        {/* --- LEFT PANEL: Question + Documents (lg+ only — phones use stacked) --- */}
        <div className="hidden lg:block flex-1 min-w-0 overflow-y-auto border-r border-white/10">
          <div className="max-w-2xl mx-auto px-3 lg:px-5 py-3 space-y-2">
            {/* Type badge + exercise name */}
            <div className="flex items-center gap-2 flex-wrap">
              {question.exercise && (
                <span className="text-[11px] font-semibold text-white/55 bg-white/5 px-2 py-0.5 rounded-md">
                  {question.exercise}
                </span>
              )}
              <span className={`text-[11px] font-bold px-2 py-0.5 rounded-md ${badge.bg} ${badge.text}`}>{badge.label}</span>
              {question.part && question.part !== 'Examen' && (
                <span className="text-[10px] text-white/40 ml-auto">
                  {isExtractedExam ? question.part : currentPartData?.shortName}
                </span>
              )}
            </div>

            {/* Question renderer (no children on desktop) */}
            <QuestionRenderer question={question} examId={exam.id} showCorrection={false} />
          </div>
        </div>

        {/* --- RIGHT PANEL: Answer + Feedback (lg+ only) --- */}
        <div className="lg:w-[52%] flex-shrink-0 overflow-y-auto bg-[#070718]/40 hidden lg:block">
          <div className="px-3 lg:px-5 py-3 space-y-3 max-w-2xl">
            {/* Answer input */}
            <AnswerInput
              questionContent={question.content}
              questionType={question.type}
              choices={question.choices}
              itemsLeft={question.items_left}
              itemsRight={question.items_right}
              value={answers[currentQ] || ''}
              onChange={(val) => setAnswers((prev) => ({ ...prev, [currentQ]: val }))}
              onImageChange={(img) => setImageData((prev) => ({ ...prev, [currentQ]: img }))}
              onSubmit={handleEvaluate}
              submitting={submitting}
              disabled={hasFeedback}
              showCorrection={hasFeedback}
              correctAnswer={question.correct_answer}
              subject={exam.subject}
            />

            {/* Feedback */}
            {hasFeedback && feedbacks[currentQ] && (
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <Award className={`w-4 h-4 ${accent.text}`} />
                  <span className={`text-xs font-bold ${accent.text}`}>Correction détaillée</span>
                </div>
                <FeedbackCard
                  feedback={feedbacks[currentQ].feedback}
                  accentText={accent.text}
                  accentLight=""
                />
              </div>
            )}

            {/* Explanation button — opens full tutoring session with whiteboard */}
            <button
              onClick={handleExplain}
              className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-gradient-to-r from-amber-500 to-orange-500 text-white rounded-xl font-semibold text-sm hover:from-amber-600 hover:to-orange-600 transition-all shadow-md shadow-amber-500/20"
            >
              <Lightbulb className="w-4 h-4" />
              {hasFeedback ? 'Explication au tableau' : 'Aide au tableau'}
            </button>
          </div>
        </div>

        {/* --- MOBILE + LANDSCAPE PHONE: stacked layout (<lg) --- */}
        <div className="lg:hidden flex-1 min-w-0 overflow-y-auto">
          <div className="px-3 py-3 space-y-3">
            {/* Type badge */}
            <div className="flex items-center gap-2">
              <span className={`text-[11px] font-bold px-2 py-0.5 rounded-md ${badge.bg} ${badge.text}`}>{badge.label}</span>
              {question.exercise && <span className="text-[11px] text-white/55">{question.exercise}</span>}
            </div>

            {/* Question */}
            <QuestionRenderer question={question} examId={exam.id} showCorrection={false}>
              {/* Answer input inline for mobile */}
              <AnswerInput
                questionContent={question.content}
                questionType={question.type}
                choices={question.choices}
                itemsLeft={question.items_left}
                itemsRight={question.items_right}
                value={answers[currentQ] || ''}
                onChange={(val) => setAnswers((prev) => ({ ...prev, [currentQ]: val }))}
                onImageChange={(img) => setImageData((prev) => ({ ...prev, [currentQ]: img }))}
                onSubmit={handleEvaluate}
                submitting={submitting}
                disabled={hasFeedback}
                showCorrection={hasFeedback}
                correctAnswer={question.correct_answer}
                subject={exam.subject}
              />

              {hasFeedback && feedbacks[currentQ] && (
                <div className="space-y-2 mt-3">
                  <div className="flex items-center gap-2">
                    <Award className={`w-4 h-4 ${accent.text}`} />
                    <span className={`text-xs font-bold ${accent.text}`}>Correction détaillée</span>
                  </div>
                  <FeedbackCard feedback={feedbacks[currentQ].feedback} accentText={accent.text} accentLight="" />
                </div>
              )}

              {/* Mobile explanation button */}
              <button
                onClick={handleExplain}
                className="w-full flex items-center justify-center gap-2 px-4 py-3 mt-3 bg-gradient-to-r from-amber-500 to-orange-500 text-white rounded-xl font-semibold text-sm hover:from-amber-600 hover:to-orange-600 transition-all shadow-md shadow-amber-500/20"
              >
                <Lightbulb className="w-4 h-4" />
                {hasFeedback ? 'Explication au tableau' : 'Aide au tableau'}
              </button>
            </QuestionRenderer>

            {/* Mobile nav */}
            <div className="flex items-center justify-between pt-3 border-t border-white/10">
              <button onClick={goPrev} disabled={currentQ === 0} className="flex items-center gap-1.5 px-3 py-2 glass rounded-lg text-white/70 text-xs font-medium disabled:opacity-30">
                <ArrowLeft className="w-3.5 h-3.5" /> Préc
              </button>
              <div className="flex gap-1 flex-wrap justify-center max-w-[180px]">
                {currentPartData?.allIndices.map((qIdx) => (
                  <button key={qIdx} onClick={() => setCurrentQ(qIdx)} className={`w-6 h-6 rounded-md text-[9px] font-bold ${qIdx === currentQ ? `${accent.bg} text-white` : feedbacks[qIdx] ? 'bg-emerald-500 text-white' : answers[qIdx]?.trim() ? 'bg-amber-500/15 text-amber-200' : 'bg-white/10 text-white/55'}`}>
                    {qIdx + 1}
                  </button>
                ))}
              </div>
              {currentQ < exam.questions.length - 1 ? (
                <button onClick={goNext} className={`flex items-center gap-1.5 px-3 py-2 text-white rounded-lg text-xs font-medium bg-gradient-to-r ${accent.gradient}`}>
                  Suiv <ArrowRight className="w-3.5 h-3.5" />
                </button>
              ) : (
                <button onClick={() => setShowResults(true)} className="flex items-center gap-1.5 px-3 py-2 bg-amber-500 text-white rounded-lg text-xs font-medium">
                  <Trophy className="w-3.5 h-3.5" /> Fin
                </button>
              )}
            </div>
          </div>
        </div>
      </div>

    </div>
  );
}

/* ================================================================== */
/*  Results — rich BAC-style report with mention + BAC context          */
/* ================================================================== */

function ExamPracticeResults({
  exam, parts, feedbacks, answers, onBack, onContinue, onRetry,
}: {
  exam: ExamData;
  parts: PartGroup[];
  feedbacks: Record<number, FeedbackData>;
  answers: Record<number, string>;
  onBack: () => void;
  onContinue?: () => void;
  onRetry?: () => void;
}) {
  const { student } = useAuthStore();
  const firstName = ((student?.full_name || '').trim().split(/\s+/)[0]) || 'Champion';

  const evaluatedCount = Object.keys(feedbacks).length;
  const totalQuestions = exam.questions.length;

  // Compute aggregate score: sum extracted scores / sum max points of evaluated questions
  let earned = 0;
  let evaluatedMax = 0;
  let answeredButNotEvaluated = 0;
  exam.questions.forEach((q, idx) => {
    const fb = feedbacks[idx];
    const qMax = q.points || 0;
    if (fb) {
      const s = extractScoreFromFeedback(fb.feedback, qMax);
      earned += s;
      evaluatedMax += qMax;
    } else if (answers[idx]?.trim()) {
      answeredButNotEvaluated += 1;
    }
  });

  const totalMax = exam.total_points || exam.questions.reduce((s, q) => s + (q.points || 0), 0);
  // Accuracy on what's been evaluated (0..100). Used for mention ONLY if enough points evaluated.
  const accuracyPct = evaluatedMax > 0 ? (earned / evaluatedMax) * 100 : 0;
  // Projected /20 score — only shown when the sample is large enough
  const scoreOn20 = evaluatedMax > 0 ? toScoreOn20(earned, evaluatedMax) : 0;
  // Consider the mention official when at least 50% of the exam's total points have been graded.
  const mentionReliable = evaluatedMax > 0 && evaluatedMax >= totalMax * 0.5;
  const mention = getMention(scoreOn20);
  const bacMsg = getBacContextMessage(scoreOn20);
  const completionPercent = totalQuestions > 0 ? Math.round((evaluatedCount / totalQuestions) * 100) : 0;
  const questionsRemaining = totalQuestions - evaluatedCount;
  const hasAnyEvaluation = evaluatedCount > 0;

  const sessionLabel = (exam.session || '').toLowerCase() === 'rattrapage' ? 'Rattrapage' : 'Normale';
  const [shareOpen, setShareOpen] = useState(false);

  // Tailored encouragement when the student still has questions to answer
  const progressPrompt = (() => {
    if (!hasAnyEvaluation) {
      return `Tu n'as encore évalué aucune réponse. Réponds aux questions puis clique sur "Vérifier ma réponse" pour obtenir une note et une correction détaillée.`;
    }
    if (questionsRemaining === 0) {
      return `Tu as évalué toutes les questions. Bravo ${firstName} !`;
    }
    if (accuracyPct >= 80) {
      return `Excellent départ ${firstName} ! Tu as ${earned.toFixed(1)}/${evaluatedMax.toFixed(0)} pts sur ${evaluatedCount} question${evaluatedCount > 1 ? 's' : ''}. Continue les ${questionsRemaining} question${questionsRemaining > 1 ? 's' : ''} restante${questionsRemaining > 1 ? 's' : ''} pour obtenir ta mention officielle.`;
    }
    if (accuracyPct >= 50) {
      return `Bon début ${firstName}. Il te reste ${questionsRemaining} question${questionsRemaining > 1 ? 's' : ''} — chaque point compte pour ta mention finale.`;
    }
    return `Pas de panique ${firstName}. Reprends calmement, il te reste ${questionsRemaining} question${questionsRemaining > 1 ? 's' : ''} pour remonter ton score.`;
  })();

  return (
    <div className="min-h-screen bg-[#070718] text-white relative overflow-hidden">
      {/* Decorative orbs */}
      <div className="pointer-events-none fixed inset-0 z-0">
        <div className="absolute top-0 left-1/3 w-[600px] h-[600px] rounded-full bg-indigo-600/15 blur-[140px] anim-pulse-glow" />
      </div>
      {/* Header */}
      <header className="relative z-20 backdrop-blur-2xl bg-[#070718]/70 border-b border-white/5">
        <div className="max-w-4xl mx-auto px-4 py-5 flex items-center gap-3">
          <button onClick={onBack} className="p-2 -ml-2 rounded-xl hover:bg-white/10 text-white/55">
            <ArrowLeft className="w-5 h-5" />
          </button>
          <div className="flex-1 min-w-0">
            <h1 className="text-xl font-bold text-white truncate">
              Résultats — {exam.subject} {exam.year}
            </h1>
            <p className="text-sm text-white/55 truncate">
              {firstName} · Mode Entraînement · Session {sessionLabel}
            </p>
          </div>
          {hasAnyEvaluation && (
            <button
              onClick={() => setShareOpen(true)}
              className="hidden sm:inline-flex items-center gap-1.5 px-3 py-2 rounded-xl bg-gradient-to-r from-indigo-600 to-blue-700 text-white text-xs font-semibold shadow-sm hover:shadow-md transition-shadow"
            >
              <Share2 className="w-3.5 h-3.5" /> Partager
            </button>
          )}
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-6 space-y-5">

        {/* ── Main score card ── */}
        {hasAnyEvaluation ? (
          <div className={`rounded-3xl border-2 ${mentionReliable ? mention.border : 'border-indigo-400/30'} ${mentionReliable ? mention.bg : 'bg-indigo-500/10'} overflow-hidden shadow-sm`}>
            <div className="p-6 md:p-8">
              <div className="flex flex-col md:flex-row items-center gap-6">
                {/* Score circle — shows raw earned points, not misleading /20 projection */}
                <div className={`relative w-32 h-32 rounded-full bg-gradient-to-br ${mentionReliable ? mention.gradient : 'from-indigo-500 to-blue-600'} flex flex-col items-center justify-center shadow-lg flex-shrink-0`}>
                  <span className="text-4xl font-black text-white leading-none">{earned.toFixed(2)}</span>
                  <span className="text-xs font-bold text-white/80 mt-1">
                    / {evaluatedMax.toFixed(0)} pts
                  </span>
                </div>

                {/* Right block */}
                <div className="flex-1 text-center md:text-left">
                  {mentionReliable ? (
                    <>
                      <div className="inline-flex items-center gap-2 mb-2">
                        <span className="text-2xl">{mention.emoji}</span>
                        <span className={`text-xl font-black ${mention.text}`}>
                          Mention {mention.label}
                        </span>
                      </div>
                      <p className="text-sm text-white/70 leading-relaxed mb-3">
                        {firstName}, {mention.encouragement.charAt(0).toLowerCase() + mention.encouragement.slice(1)}
                      </p>
                    </>
                  ) : (
                    <>
                      <div className="inline-flex items-center gap-2 mb-2">
                        <Sparkles className="w-5 h-5 text-indigo-300" />
                        <span className="text-lg font-black text-indigo-200">
                          Belle progression, {firstName} !
                        </span>
                      </div>
                      <p className="text-sm text-white/70 leading-relaxed mb-3">
                        {progressPrompt}
                      </p>
                    </>
                  )}
                  <div className="flex items-center gap-2 text-xs text-white/55 flex-wrap justify-center md:justify-start">
                    <Trophy className="w-3.5 h-3.5" />
                    <span>
                      Score : <b>{earned.toFixed(2)} / {evaluatedMax.toFixed(0)}</b> pts
                      {' '}({accuracyPct.toFixed(0)} % de réussite)
                    </span>
                    <span className="text-white/30">·</span>
                    <span>{evaluatedCount}/{totalQuestions} questions</span>
                  </div>
                </div>
              </div>

              {/* BAC context OR continue CTA */}
              {mentionReliable ? (
                <div className="mt-5 pt-5 border-t border-white/10 flex items-start gap-2.5">
                  <Target className={`w-4 h-4 ${mention.text} mt-0.5 flex-shrink-0`} />
                  <p className="text-[13px] text-white/85 leading-relaxed">
                    <span className="font-semibold">Contexte BAC :</span> {bacMsg}
                  </p>
                </div>
              ) : questionsRemaining > 0 && onContinue && (
                <div className="mt-5 pt-5 border-t border-indigo-400/30">
                  <button
                    onClick={onContinue}
                    className="w-full flex items-center justify-center gap-2 px-5 py-3.5 rounded-2xl bg-gradient-to-r from-indigo-600 to-blue-700 text-white text-sm font-semibold shadow-md hover:shadow-lg transition-all"
                  >
                    <Send className="w-4 h-4" />
                    Continuer les {questionsRemaining} question{questionsRemaining > 1 ? 's' : ''} restante{questionsRemaining > 1 ? 's' : ''}
                    <ArrowRight className="w-4 h-4" />
                  </button>
                  <p className="text-[11px] text-center text-white/55 mt-2">
                    Ta mention officielle s'affichera une fois au moins la moitié de l'examen évaluée.
                  </p>
                </div>
              )}
            </div>
          </div>
        ) : (
          <div className="glass-strong rounded-3xl p-6 md:p-8 text-center">
            <Sparkles className="w-10 h-10 text-amber-500 mx-auto mb-3" />
            <h2 className="text-lg font-bold text-white mb-1">Allez {firstName}, c'est parti !</h2>
            <p className="text-sm text-white/55 max-w-md mx-auto mb-4">
              Tu n'as encore évalué aucune réponse. Réponds aux questions puis clique sur "Vérifier ma réponse" pour obtenir une note et une correction détaillée.
            </p>
            {onContinue && (
              <button
                onClick={onContinue}
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 to-blue-700 text-white text-sm font-semibold shadow-sm hover:shadow-md transition-all"
              >
                <Send className="w-4 h-4" /> Commencer l'examen <ArrowRight className="w-4 h-4" />
              </button>
            )}
          </div>
        )}

        {/* Mobile share button (header one is hidden on xs) */}
        {hasAnyEvaluation && (
          <button
            onClick={() => setShareOpen(true)}
            className="sm:hidden w-full inline-flex items-center justify-center gap-1.5 px-3 py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 to-blue-700 text-white text-sm font-semibold shadow-sm"
          >
            <Share2 className="w-4 h-4" /> Partager mes résultats
          </button>
        )}

        {shareOpen && (
          <ExamResultsShareModal
            firstName={firstName}
            exam={exam}
            earned={earned}
            evaluatedMax={evaluatedMax}
            evaluatedCount={evaluatedCount}
            totalQuestions={totalQuestions}
            totalMax={totalMax}
            scoreOn20={scoreOn20}
            mentionReliable={mentionReliable}
            mention={mention}
            sessionLabel={sessionLabel}
            onClose={() => setShareOpen(false)}
          />
        )}

        {/* ── Stats grid ── */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          <div className="glass rounded-2xl p-4 text-center">
            <p className="text-2xl font-black text-blue-300">{evaluatedCount}<span className="text-sm font-bold text-white/40">/{totalQuestions}</span></p>
            <p className="text-[11px] text-white/55 mt-1 font-medium">Questions évaluées</p>
          </div>
          <div className="glass rounded-2xl p-4 text-center">
            <p className="text-2xl font-black text-white/85">{completionPercent}%</p>
            <p className="text-[11px] text-white/55 mt-1 font-medium">Complétion</p>
          </div>
          <div className="glass rounded-2xl p-4 text-center">
            <p className="text-2xl font-black text-amber-300">{answeredButNotEvaluated}</p>
            <p className="text-[11px] text-white/55 mt-1 font-medium">À vérifier</p>
          </div>
          <div className="glass rounded-2xl p-4 text-center">
            <p className={`text-2xl font-black ${hasAnyEvaluation ? mention.text : 'text-white/40'}`}>
              {hasAnyEvaluation ? mention.short : '—'}
            </p>
            <p className="text-[11px] text-white/55 mt-1 font-medium">Mention</p>
          </div>
        </div>

        {/* ── Per-part breakdown ── */}
        {hasAnyEvaluation && parts.length > 1 && (
          <div className="glass rounded-2xl p-5">
            <h2 className="text-sm font-bold text-white mb-4 flex items-center gap-2">
              <BookOpen className="w-4 h-4 text-blue-300" />
              Progression par partie
            </h2>
            <div className="space-y-4">
              {parts.map((part, pi) => {
                let partEarned = 0;
                let partEvaluatedMax = 0;
                part.allIndices.forEach((i) => {
                  const fb = feedbacks[i];
                  if (fb) {
                    const qMax = exam.questions[i]?.points || 0;
                    partEarned += extractScoreFromFeedback(fb.feedback, qMax);
                    partEvaluatedMax += qMax;
                  }
                });
                const partEvaluated = part.allIndices.filter((i) => feedbacks[i]).length;
                const partMention = getMention(partEvaluatedMax > 0 ? toScoreOn20(partEarned, partEvaluatedMax) : 0);
                const pct = partEvaluatedMax > 0 ? Math.round((partEarned / partEvaluatedMax) * 100) : 0;

                return (
                  <div key={pi}>
                    <div className="flex items-center justify-between mb-1.5">
                      <p className="text-[13px] font-semibold text-white/85 flex items-center gap-1.5">
                        {part.icon === 'book'
                          ? <BookOpen className="w-3.5 h-3.5 text-blue-500" />
                          : <FlaskConical className="w-3.5 h-3.5 text-emerald-500" />
                        }
                        {part.name}
                      </p>
                      <div className="flex items-center gap-2 text-xs">
                        <span className="text-white/40">{partEvaluated}/{part.allIndices.length} q.</span>
                        {partEvaluatedMax > 0 ? (
                          <span className={`font-bold ${partMention.text}`}>
                            {partEarned.toFixed(1)}/{partEvaluatedMax} pts
                          </span>
                        ) : (
                          <span className="text-white/30">—</span>
                        )}
                      </div>
                    </div>
                    <div className="w-full h-2.5 bg-slate-100 rounded-full overflow-hidden">
                      {partEvaluatedMax > 0 && (
                        <div
                          className={`h-full bg-gradient-to-r ${partMention.gradient} transition-all duration-700`}
                          style={{ width: `${pct}%` }}
                        />
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* ── Per-question details ── */}
        {parts.map((part, pi) => {
          const isKnowledge = part.icon === 'book';

          return (
            <div key={pi} className="space-y-2">
              <div className="flex items-center gap-2 mb-2 px-1">
                {isKnowledge
                  ? <BookOpen className="w-4 h-4 text-blue-300" />
                  : <FlaskConical className="w-4 h-4 text-emerald-300" />
                }
                <h2 className="text-sm font-bold text-white/85">{part.name}</h2>
              </div>

              {part.exercises.map((ex, ei) => (
                <div key={ei}>
                  {part.exercises.length > 1 && (
                    <p className="text-xs font-semibold text-white/40 uppercase tracking-wider mb-1.5 px-1">{ex.name}</p>
                  )}
                  {ex.indices.map((qIdx) => {
                    const q = exam.questions[qIdx];
                    const fb = feedbacks[qIdx];
                    const ans = answers[qIdx];
                    const badge = TYPE_BADGE[q.type || 'open'];
                    const qScore = fb ? extractScoreFromFeedback(fb.feedback, q.points || 0) : null;
                    const qScoreOn20 = qScore != null && q.points > 0 ? (qScore / q.points) * 20 : null;
                    const qTier = qScoreOn20 != null ? getMention(qScoreOn20) : null;

                    return (
                      <div key={qIdx} className="glass rounded-xl p-4 mb-2">
                        <div className="flex items-center justify-between mb-2 gap-3">
                          <div className="flex items-center gap-2 min-w-0">
                            <span className="text-xs font-black text-white/85 bg-white/5 px-2 py-1 rounded-lg">Q{qIdx + 1}</span>
                            <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${badge.bg} ${badge.text}`}>{badge.label}</span>
                            <span className="text-[10px] text-white/40">{q.points} pt{q.points > 1 ? 's' : ''}</span>
                          </div>
                          {fb && qTier && qScore != null ? (
                            <span className={`text-xs font-bold px-2.5 py-1 rounded-lg ${qTier.bg} ${qTier.text} flex items-center gap-1`}>
                              {qTier.emoji} {qScore.toFixed(1)}/{q.points}
                            </span>
                          ) : ans?.trim() ? (
                            <span className="text-[10px] text-amber-300 flex items-center gap-1">
                              <Lightbulb className="w-3 h-3" /> Non évaluée
                            </span>
                          ) : (
                            <span className="text-[10px] text-white/40">—</span>
                          )}
                        </div>
                        <LatexRenderer as="p" className="text-sm text-white/70 line-clamp-2 mb-2">{q.content}</LatexRenderer>
                        {ans && (
                          <div className="bg-white/[.03] rounded-lg p-2.5 text-[12.5px] text-white/85 mb-2 border border-white/5">
                            <span className="text-[10px] font-bold text-white/40 uppercase tracking-wider">Ta réponse</span>
                            <p className="mt-1 whitespace-pre-line line-clamp-3">{ans}</p>
                          </div>
                        )}
                        {fb && (
                          <div className={`rounded-lg p-2.5 text-[12.5px] text-white/85 ${isKnowledge ? 'bg-blue-500/15' : 'bg-emerald-500/15'}`}>
                            <span className={`text-[10px] font-bold uppercase tracking-wider ${isKnowledge ? 'text-blue-300' : 'text-emerald-300'}`}>Correction</span>
                            <p className="mt-1 whitespace-pre-line">{fb.feedback.length > 300 ? fb.feedback.substring(0, 300) + '…' : fb.feedback}</p>
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              ))}
            </div>
          );
        })}

        {/* Actions */}
        <div className="flex flex-col sm:flex-row gap-3 pt-2">
          <button
            onClick={onBack}
            className="flex-1 px-6 py-3 bg-gradient-to-r from-indigo-500 to-cyan-500 text-white rounded-xl font-bold shadow-lg shadow-indigo-500/30 hover:shadow-indigo-500/50 transition-all flex items-center justify-center gap-2"
          >
            <ArrowLeft className="w-4 h-4" /> Retour aux examens
          </button>
          {onRetry && (
            <button
              onClick={onRetry}
              className="flex-1 px-6 py-3 glass text-white/85 rounded-xl font-semibold hover:bg-white/[.06] transition-colors flex items-center justify-center gap-2"
            >
              <RotateCcw className="w-4 h-4" /> Refaire cet examen
            </button>
          )}
        </div>
      </main>
    </div>
  );
}

/* ================================================================== */
/*  Share modal — per-exam results card (PNG capture + Web Share API)   */
/* ================================================================== */

const MOALIM_URL = 'https://moalim.online';

interface ShareModalProps {
  firstName: string;
  exam: ExamData;
  earned: number;
  evaluatedMax: number;
  evaluatedCount: number;
  totalQuestions: number;
  totalMax: number;
  scoreOn20: number;
  mentionReliable: boolean;
  mention: ReturnType<typeof getMention>;
  sessionLabel: string;
  onClose: () => void;
}

function ExamResultsShareModal(props: ShareModalProps) {
  const {
    firstName, exam, earned, evaluatedMax, evaluatedCount, totalQuestions,
    scoreOn20, mentionReliable, mention, sessionLabel, onClose,
  } = props;

  const cardRef = useRef<HTMLDivElement>(null);
  const [generating, setGenerating] = useState(false);
  const [downloaded, setDownloaded] = useState(false);
  const [copied, setCopied] = useState(false);
  const [fileShareUnsupported, setFileShareUnsupported] = useState(false);

  const accuracyPct = evaluatedMax > 0 ? (earned / evaluatedMax) * 100 : 0;
  const scoreEmoji =
    accuracyPct >= 80 ? '🏆' :
    accuracyPct >= 60 ? '🎯' :
    accuracyPct >= 40 ? '📈' : '💪';

  // Tailored encouragement for the share text
  const encouragement = mentionReliable
    ? `Mention ${mention.label} ${mention.emoji}`
    : `Entraînement en cours — ${evaluatedCount}/${totalQuestions} questions évaluées ${scoreEmoji}`;

  const shareText =
    `🎓 ${firstName} s'entraîne sur le BAC avec معلم (Moalim) ! ${scoreEmoji}\n` +
    `📘 ${exam.subject} ${exam.year} · Session ${sessionLabel}\n` +
    `✅ Score : ${earned.toFixed(2)}/${evaluatedMax.toFixed(0)} pts (${accuracyPct.toFixed(0)}% de réussite)\n` +
    (mentionReliable
      ? `🏅 Mention ${mention.label} ${mention.emoji}\n`
      : `📝 ${evaluatedCount}/${totalQuestions} questions évaluées\n`) +
    `\n👉 Rejoins-moi sur ${MOALIM_URL}`;

  const encodedText = encodeURIComponent(shareText);
  const encodedUrl = encodeURIComponent(MOALIM_URL);

  const generatePng = async (): Promise<Blob | null> => {
    if (!cardRef.current) return null;
    const canvas = await html2canvas(cardRef.current, {
      backgroundColor: null, scale: 2, useCORS: true, logging: false,
    });
    return await new Promise<Blob | null>((resolve) =>
      canvas.toBlob((blob) => resolve(blob), 'image/png', 1)
    );
  };

  const safeName = firstName.replace(/\s+/g, '_').replace(/[^\w-]/g, '');
  const fileName = `resultats-${exam.subject.toLowerCase()}-${exam.year}-${safeName || 'eleve'}.png`;

  const shareNative = async () => {
    setGenerating(true);
    setFileShareUnsupported(false);
    try {
      const blob = await generatePng();
      if (!blob) return;
      const file = new File([blob], fileName, { type: 'image/png' });
      const nav: any = navigator;
      const shareData: any = {
        title: 'معلم — Mes résultats',
        text: shareText,
        url: MOALIM_URL,
        files: [file],
      };
      if (nav.canShare && nav.canShare({ files: [file] })) {
        await nav.share(shareData);
        onClose();
      } else {
        await downloadImage(blob);
        setFileShareUnsupported(true);
      }
    } catch (e) {
      console.warn('Share failed:', e);
    } finally {
      setGenerating(false);
    }
  };

  const downloadImage = async (preBlob?: Blob) => {
    const blob = preBlob ?? (await generatePng());
    if (!blob) return;
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 4000);
    setDownloaded(true);
    setTimeout(() => setDownloaded(false), 2500);
  };

  const handleDownload = async () => {
    setGenerating(true);
    try { await downloadImage(); } finally { setGenerating(false); }
  };

  const copyText = async () => {
    try {
      await navigator.clipboard.writeText(shareText);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      window.prompt('Copie ce message :', shareText);
    }
  };

  const networks = [
    {
      name: 'WhatsApp',
      color: 'bg-[#25D366] hover:bg-[#1ebe5d]',
      url: `https://wa.me/?text=${encodedText}`,
    },
    {
      name: 'X',
      color: 'bg-black hover:bg-zinc-800',
      url: `https://twitter.com/intent/tweet?text=${encodedText}&url=${encodedUrl}`,
    },
    {
      name: 'Facebook',
      color: 'bg-[#1877F2] hover:bg-[#0f63d1]',
      url: `https://www.facebook.com/sharer/sharer.php?u=${encodedUrl}&quote=${encodedText}`,
    },
  ];

  const handleNetworkClick = async (
    e: React.MouseEvent<HTMLAnchorElement>,
    net: { name: string; url: string }
  ) => {
    e.preventDefault();
    try { await navigator.clipboard.writeText(shareText); } catch { /* noop */ }
    await downloadImage();
    window.open(net.url, '_blank', 'noopener,noreferrer');
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4 overflow-y-auto"
      onClick={onClose}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        className="glass-strong rounded-2xl shadow-2xl w-full max-w-md overflow-hidden my-4"
      >
        {/* Header */}
        <div className="bg-gradient-to-br from-slate-900 via-slate-800 to-indigo-900 px-6 py-5 text-white">
          <div className="flex items-start justify-between">
            <div>
              <h3 className="text-xl font-bold">Partager mes résultats</h3>
              <p className="text-sm text-indigo-100 mt-1">
                {exam.subject} {exam.year} · {encouragement}
              </p>
            </div>
            <button
              onClick={onClose}
              className="p-1 text-white/80 hover:text-white hover:bg-white/10 rounded-lg transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Shareable card preview */}
        <div className="px-4 pt-4 pb-2">
          <a
            href={MOALIM_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="block rounded-xl overflow-hidden shadow-md hover:shadow-lg transition-shadow"
            title={`Ouvrir ${MOALIM_URL}`}
          >
            <ShareableExamCard
              ref={cardRef}
              firstName={firstName}
              exam={exam}
              earned={earned}
              evaluatedMax={evaluatedMax}
              evaluatedCount={evaluatedCount}
              totalQuestions={totalQuestions}
              scoreOn20={scoreOn20}
              mentionReliable={mentionReliable}
              mention={mention}
              sessionLabel={sessionLabel}
              scoreEmoji={scoreEmoji}
            />
          </a>
          <p className="text-[10px] text-center text-white/40 mt-2">
            🖼 Aperçu — l'image partagée redirige vers{' '}
            <span className="font-semibold text-indigo-300">moalim.online</span>
          </p>
        </div>

        {/* Primary: native share */}
        <div className="px-6 pt-2 pb-2 space-y-2">
          <button
            onClick={shareNative}
            disabled={generating}
            className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-gradient-to-r from-indigo-600 to-blue-700 text-white rounded-xl text-sm font-bold hover:shadow-lg transition-all disabled:opacity-60"
          >
            {generating ? (
              <><Loader2 className="w-4 h-4 animate-spin" /> Génération…</>
            ) : (
              <><Share2 className="w-4 h-4" /> Partager mon image</>
            )}
          </button>
          <div className="grid grid-cols-2 gap-2">
            <button
              onClick={handleDownload}
              disabled={generating}
              className="flex items-center justify-center gap-1.5 px-3 py-2 glass rounded-xl text-xs font-semibold text-white/85 hover:border-indigo-400 hover:text-indigo-300 transition-colors disabled:opacity-60"
            >
              {downloaded ? (
                <><Check className="w-3.5 h-3.5 text-emerald-300" /><span className="text-emerald-300">Téléchargée</span></>
              ) : (
                <>📥 Télécharger l'image</>
              )}
            </button>
            <button
              onClick={copyText}
              className="flex items-center justify-center gap-1.5 px-3 py-2 glass rounded-xl text-xs font-semibold text-white/85 hover:border-indigo-400 hover:text-indigo-300 transition-colors"
            >
              {copied ? (
                <><Check className="w-3.5 h-3.5 text-emerald-300" /><span className="text-emerald-300">Texte copié</span></>
              ) : (
                <><Copy className="w-3.5 h-3.5" /> Copier le texte</>
              )}
            </button>
          </div>
          {fileShareUnsupported && (
            <p className="text-[11px] text-amber-200 bg-amber-500/15 border border-amber-400/30 rounded-lg px-3 py-2">
              Image téléchargée ! Ton navigateur ne supporte pas le partage de fichier — joins-la manuellement à ton post.
            </p>
          )}
        </div>

        {/* Social networks */}
        <div className="px-6 py-4">
          <p className="text-xs font-semibold text-white/55 uppercase tracking-wider mb-2">
            Ou directement sur un réseau
          </p>
          <div className="grid grid-cols-3 gap-2">
            {networks.map((net) => (
              <a
                key={net.name}
                href={net.url}
                onClick={(e) => handleNetworkClick(e, net)}
                target="_blank"
                rel="noopener noreferrer"
                className={`flex items-center justify-center gap-1.5 px-3 py-2.5 rounded-xl ${net.color} text-white text-xs font-semibold transition-all hover:shadow-md`}
              >
                {net.name}
              </a>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

/* ─────────────────── ShareableExamCard (PNG source) ─────────────────── */

const ShareableExamCard = forwardRef<
  HTMLDivElement,
  {
    firstName: string;
    exam: ExamData;
    earned: number;
    evaluatedMax: number;
    evaluatedCount: number;
    totalQuestions: number;
    scoreOn20: number;
    mentionReliable: boolean;
    mention: ReturnType<typeof getMention>;
    sessionLabel: string;
    scoreEmoji: string;
  }
>(function ShareableExamCardImpl({
  firstName, exam, earned, evaluatedMax, evaluatedCount, totalQuestions,
  mentionReliable, mention, sessionLabel, scoreEmoji,
}, ref) {
  const accuracyPct = evaluatedMax > 0 ? Math.round((earned / evaluatedMax) * 100) : 0;

  return (
    <div
      ref={ref}
      style={{
        width: 480,
        fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
        background: 'linear-gradient(135deg, #0f172a 0%, #1e293b 45%, #3730a3 100%)',
        color: 'white', padding: 28, position: 'relative', overflow: 'hidden',
      }}
    >
      {/* Decorative blobs */}
      <div style={{
        position: 'absolute', top: -40, right: -40, width: 160, height: 160,
        borderRadius: '50%', background: 'rgba(99,102,241,0.25)', filter: 'blur(30px)',
      }} />
      <div style={{
        position: 'absolute', bottom: -50, left: -30, width: 180, height: 180,
        borderRadius: '50%', background: 'rgba(16,185,129,0.18)', filter: 'blur(35px)',
      }} />

      {/* Brand */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 20 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <div style={{
            width: 36, height: 36, borderRadius: 10,
            background: 'linear-gradient(135deg, #6366f1, #3b82f6)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: 18, fontWeight: 900,
          }}>م</div>
          <div>
            <div style={{ fontSize: 14, fontWeight: 800, letterSpacing: 0.2 }}>معلم · Moalim</div>
            <div style={{ fontSize: 10, color: '#94a3b8' }}>Plateforme BAC Maroc</div>
          </div>
        </div>
        <div style={{ fontSize: 26 }}>{scoreEmoji}</div>
      </div>

      {/* Name + exam */}
      <div style={{ marginBottom: 18 }}>
        <div style={{ fontSize: 12, color: '#a5b4fc', textTransform: 'uppercase', letterSpacing: 1, fontWeight: 700 }}>
          Résultats d'examen
        </div>
        <div style={{ fontSize: 22, fontWeight: 900, marginTop: 4 }}>{firstName}</div>
        <div style={{ fontSize: 14, color: '#cbd5e1', marginTop: 2 }}>
          {exam.subject} {exam.year} · Session {sessionLabel}
        </div>
      </div>

      {/* Score block */}
      <div style={{
        display: 'flex', alignItems: 'center', gap: 18,
        background: 'rgba(255,255,255,0.08)', borderRadius: 18, padding: 18,
        border: '1px solid rgba(255,255,255,0.12)', marginBottom: 14,
      }}>
        <div style={{
          width: 110, height: 110, borderRadius: '50%',
          background: mentionReliable
            ? 'linear-gradient(135deg, #10b981, #0d9488)'
            : 'linear-gradient(135deg, #6366f1, #2563eb)',
          display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
          boxShadow: '0 10px 25px rgba(0,0,0,0.35)', flexShrink: 0,
        }}>
          <div style={{ fontSize: 30, fontWeight: 900, lineHeight: 1 }}>{earned.toFixed(2)}</div>
          <div style={{ fontSize: 10, fontWeight: 700, opacity: 0.85, marginTop: 2 }}>
            / {evaluatedMax.toFixed(0)} pts
          </div>
        </div>
        <div style={{ flex: 1 }}>
          {mentionReliable ? (
            <>
              <div style={{ fontSize: 11, color: '#a5b4fc', fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.8 }}>
                Mention obtenue
              </div>
              <div style={{ fontSize: 22, fontWeight: 900, marginTop: 2 }}>
                {mention.emoji} {mention.label}
              </div>
              <div style={{ fontSize: 12, color: '#cbd5e1', marginTop: 6, lineHeight: 1.45 }}>
                {accuracyPct}% de réussite · {evaluatedCount}/{totalQuestions} questions
              </div>
            </>
          ) : (
            <>
              <div style={{ fontSize: 11, color: '#a5b4fc', fontWeight: 700, textTransform: 'uppercase', letterSpacing: 0.8 }}>
                Entraînement en cours
              </div>
              <div style={{ fontSize: 18, fontWeight: 900, marginTop: 2 }}>
                {accuracyPct}% de réussite
              </div>
              <div style={{ fontSize: 12, color: '#cbd5e1', marginTop: 6, lineHeight: 1.45 }}>
                {evaluatedCount}/{totalQuestions} questions évaluées — je progresse !
              </div>
            </>
          )}
        </div>
      </div>

      {/* Encouragement */}
      <div style={{
        background: 'rgba(255,255,255,0.06)', borderRadius: 14, padding: 14,
        fontSize: 12, color: '#e2e8f0', lineHeight: 1.5,
        border: '1px solid rgba(255,255,255,0.08)',
      }}>
        {mentionReliable
          ? (mention.encouragement)
          : `${firstName} continue son entraînement sur les sujets du BAC Maroc. Chaque question corrigée = un pas vers la mention ! 🚀`
        }
      </div>

      {/* Footer */}
      <div style={{
        marginTop: 16, display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        fontSize: 11, color: '#94a3b8',
      }}>
        <div>🎓 Rejoins-moi sur la plateforme</div>
        <div style={{ fontWeight: 800, color: '#a5b4fc' }}>{MOALIM_URL.replace('https://', '')}</div>
      </div>
    </div>
  );
});
