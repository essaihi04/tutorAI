import { useEffect, useMemo } from 'react';
import { BookOpen, ArrowLeft, ArrowRight, Lightbulb, Award, Eye, EyeOff } from 'lucide-react';
import { wsService } from '../../services/websocket';
import { useSessionStore } from '../../stores/sessionStore';
import QuestionRenderer from '../exam/QuestionRenderer';
import AnswerInput from '../exam/AnswerInput';

/** Compress a base64 image before WebSocket send to avoid frame drops. */
async function compressImage(dataUrl: string, maxWidth = 1200, quality = 0.75): Promise<string> {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => {
      let w = img.width;
      let h = img.height;
      if (w > maxWidth) {
        h = Math.round(h * (maxWidth / w));
        w = maxWidth;
      }
      const canvas = document.createElement('canvas');
      canvas.width = w;
      canvas.height = h;
      const ctx = canvas.getContext('2d');
      if (!ctx) return reject(new Error('No 2D context'));
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(0, 0, w, h);
      ctx.drawImage(img, 0, 0, w, h);
      resolve(canvas.toDataURL('image/jpeg', quality));
    };
    img.onerror = reject;
    img.src = dataUrl;
  });
}

interface ExamQuestion {
  question_index: number;
  content: string;
  type: string;
  points: number;
  correction: string;
  choices?: { letter: string; text: string }[];
  correct_answer?: string | boolean;
  documents?: Array<{ id?: string; type: string; title?: string; src: string; description?: string }>;
}

export interface ExamExercise {
  exam_id: string;
  exam_path?: string;
  exam_label: string;
  subject: string;
  year: number;
  session: string;
  part_name?: string;
  exercise_name?: string;
  exercise_context?: string;
  topic?: string;
  all_documents?: Array<{ id?: string; type: string; title?: string; src: string; description?: string }>;
  questions: ExamQuestion[];
  total_points: number;
}

interface ExamExercisePanelProps {
  exercises: ExamExercise[];
  query?: string;
  onClose: () => void;
  onSubmitAnswer?: (exerciseIndex: number, answer: string) => void;
}

export default function ExamExercisePanel({ exercises, query: _query, onClose, onSubmitAnswer }: ExamExercisePanelProps) {
  const { addMessage, examPanelState, setExamPanelState, resetExamPanelIfChanged } = useSessionStore();
  const { currentExIdx, currentQIdx, answers, images, submitted, revealedCorrections } = examPanelState;

  const setCurrentExIdx = (v: number | ((p: number) => number)) =>
    setExamPanelState({ currentExIdx: typeof v === 'function' ? v(currentExIdx) : v });
  const setCurrentQIdx = (v: number | ((p: number) => number)) =>
    setExamPanelState({ currentQIdx: typeof v === 'function' ? v(currentQIdx) : v });
  const setAnswers = (v: Record<string, string> | ((p: Record<string, string>) => Record<string, string>)) =>
    setExamPanelState({ answers: typeof v === 'function' ? v(answers) : v });
  const setImages = (v: Record<string, string | null> | ((p: Record<string, string | null>) => Record<string, string | null>)) =>
    setExamPanelState({ images: typeof v === 'function' ? v(images) : v });
  const setSubmitted = (v: Record<string, boolean> | ((p: Record<string, boolean>) => Record<string, boolean>)) =>
    setExamPanelState({ submitted: typeof v === 'function' ? v(submitted) : v });
  const setRevealedCorrections = (v: Record<string, boolean> | ((p: Record<string, boolean>) => Record<string, boolean>)) =>
    setExamPanelState({ revealedCorrections: typeof v === 'function' ? v(revealedCorrections) : v });

  // Reset state ONLY when a truly different exam is loaded.
  // On re-mount of the panel with the same exam, preserve answers/submissions
  // so the student can return after viewing the correction on the whiteboard.
  const exerciseSignature = useMemo(() => {
    if (!exercises.length) return '';
    const ex0 = exercises[0];
    const qCount = exercises.reduce((sum, e) => sum + (e.questions?.length || 0), 0);
    return `${ex0.exam_id || 'ex'}-${ex0.year || ''}-${exercises.length}-${qCount}`;
  }, [exercises]);
  useEffect(() => {
    if (exerciseSignature) {
      const didReset = resetExamPanelIfChanged(exerciseSignature);
      if (didReset) {
        console.log('[ExamPanel] New exam loaded, state reset. Signature:', exerciseSignature);
      } else {
        console.log('[ExamPanel] Same exam, preserving answers. Signature:', exerciseSignature);
      }
    }
  }, [exerciseSignature, resetExamPanelIfChanged]);

  const ex = exercises[currentExIdx];
  const question = ex?.questions[currentQIdx];

  // Keep the backend in sync with the exam/exercise/question currently
  // displayed, so any free-form chat or voice message (e.g. "Aide au tableau")
  // is grounded in the real metadata. Without this, the LLM hallucinates
  // a different year/session (e.g. says "2025 Rattrapage" while UI shows
  // "Rattrapage 2023").
  useEffect(() => {
    if (!ex || !question) return;
    wsService.sendJson({
      type: 'set_exam_panel_view',
      view: {
        exam_id: ex.exam_id,
        subject: ex.subject,
        year: ex.year,
        session: ex.session,
        exam_title: ex.exam_label,
        exercise_index: currentExIdx,
        exercise_total: exercises.length,
        exercise_name: ex.exercise_name || '',
        part_name: ex.part_name || '',
        topic: ex.topic || '',
        question_number: currentQIdx + 1,
        question_total: ex.questions.length,
        question_content: (question.content || '').substring(0, 1500),
        question_correction: (question.correction || '').substring(0, 1500),
        question_points: question.points || 0,
        question_type: question.type || 'open',
      },
    });
  }, [ex, question, currentExIdx, currentQIdx, exercises.length]);

  // Clear the server-side view when the panel unmounts (closed by user).
  useEffect(() => {
    return () => {
      wsService.sendJson({ type: 'clear_exam_panel_view' });
    };
  }, []);

  if (!ex) return null;
  if (!question) return null;

  const qKey = `${currentExIdx}-${currentQIdx}`;

  // Adapt our ExamQuestion → QuestionData expected by QuestionRenderer
  const adaptedQuestion = useMemo(() => ({
    index: currentQIdx,
    content: question.content || '',
    points: question.points || 0,
    type: (question.type as any) || 'open',
    exercise: ex.exercise_name || '',
    exercise_context: currentQIdx === 0 ? (ex.exercise_context || '') : '', // only show context on first question
    documents: (question.documents || []).map((d, i) => ({
      id: d.id || `doc_${i}`,
      type: d.type || 'figure',
      title: d.title || `Document ${i + 1}`,
      src: d.src,
      description: d.description,
    })),
    correction: question.correction ? { content: question.correction } : null,
  }), [ex, question, currentQIdx]);

  const handleSubmit = async () => {
    const answer = answers[qKey];
    const image = images[qKey];
    // Allow submission with image only (drawing/photo)
    if (!answer?.trim() && !image) return;
    setSubmitted((prev) => ({ ...prev, [qKey]: true }));

    // Send structured exam_answer for proficiency tracking
    wsService.sendJson({
      type: 'exam_answer',
      answer: {
        subject: ex.subject,
        topic: ex.topic || '',
        question_content: question.content?.substring(0, 300) || '',
        student_answer: answer || '',
        correct_answer: question.correct_answer != null ? String(question.correct_answer) : '',
        question_type: question.type || 'open',
        max_points: question.points || 1,
        exam_id: ex.exam_id,
        exercise_name: ex.exercise_name || '',
        part_name: ex.part_name || '',
        year: String(ex.year || ''),
      },
    });

    // Compress image before sending to avoid WebSocket frame drops
    let compressedImage: string | undefined;
    if (image) {
      try {
        compressedImage = await compressImage(image);
      } catch (e) {
        console.warn('[ExamExercisePanel] Image compression failed, using original', e);
        compressedImage = image;
      }
    }

    // Also send as text for LLM discussion.
    // If a drawing/photo is present, include it as student_image so the backend
    // vision service can analyze the drawing and give accurate correction.
    const textPart = answer?.trim()
      ? answer
      : '[Voir mon dessin ci-joint]';
    // Structured message that clearly identifies the exam, exercise, question being answered
    // so the LLM can give a targeted correction, not treat it as free conversation.
    const msg = `[RÉPONSE D'EXAMEN SOUMISE POUR CORRECTION]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 Examen: ${ex.subject} ${ex.year}${ex.session ? ` (${ex.session})` : ''}
📖 Exercice: ${ex.exercise_name || ex.topic || ''}
❓ Question ${currentQIdx + 1}/${ex.questions.length} (${question.points ? question.points + ' pt' : ''})
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ÉNONCÉ DE LA QUESTION ${currentQIdx + 1}:
${question.content}

${question.correction ? `CORRECTION OFFICIELLE ATTENDUE:\n${question.correction}\n\n` : ''}MA RÉPONSE À LA QUESTION ${currentQIdx + 1}:
${textPart}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ CORRIGE SPÉCIFIQUEMENT MA RÉPONSE À CETTE QUESTION ${currentQIdx + 1}. Compare-la à la correction officielle, explique mes erreurs s'il y en a, et donne la bonne méthode.`;
    wsService.sendJson({
      type: 'text_input',
      text: msg,
      exam_context: true,
      exam_question_number: currentQIdx + 1,
      exam_total_questions: ex.questions.length,
      // Keep the correction inside the exam panel/chat — do NOT open the whiteboard.
      // The student will explicitly click "Explication au tableau" if they want it.
      suppress_whiteboard: true,
      ...(compressedImage ? { student_image: compressedImage, question_content: question.content, question_correction: question.correction || '', subject: ex.subject } : {}),
    });
    const displayMsg = `Ma réponse à la question ${currentQIdx + 1}: ${textPart}`;
    addMessage('student', displayMsg);
    onSubmitAnswer?.(currentQIdx, answer || '[dessin]');
  };

  const handleExplain = () => {
    const hasAnswered = submitted[qKey];
    const msg = hasAnswered
      ? `Explique-moi la correction de la question ${currentQIdx + 1} au tableau, étape par étape.`
      : `Explique-moi comment résoudre la question ${currentQIdx + 1} au tableau, donne-moi la méthode.`;
    wsService.sendJson({ type: 'text_input', text: msg, exam_context: true });
    addMessage('student', msg);
  };

  const toggleCorrection = () => {
    setRevealedCorrections((prev) => ({ ...prev, [qKey]: !prev[qKey] }));
  };

  const goPrev = () => setCurrentQIdx((p) => Math.max(0, p - 1));
  const goNext = () => setCurrentQIdx((p) => Math.min(ex.questions.length - 1, p + 1));

  const showCorrection = !!revealedCorrections[qKey];
  const questionTypeForInput = (question.type as any) === 'qcm' || (question.type as any) === 'vrai_faux' || (question.type as any) === 'association' || (question.type as any) === 'schema'
    ? (question.type as any)
    : 'open';

  return (
    <div className="w-full h-full flex flex-col bg-white overflow-hidden">
      {/* ===================== HEADER ===================== */}
      <header className="shrink-0 bg-white border-b border-slate-200/60">
        <div className="px-3 lg:px-5 py-2 flex items-center gap-2">
          {/* Title */}
          <div className="flex items-center gap-2 min-w-0 flex-shrink-0">
            <span className="inline-flex items-center justify-center w-8 h-8 rounded-xl bg-gradient-to-br from-amber-500 to-orange-500 shadow-sm shadow-amber-500/20">
              <BookOpen className="w-4 h-4 text-white" />
            </span>
            <div className="min-w-0">
              <h1 className="text-sm font-bold text-slate-800 truncate">
                {ex.subject} — {(ex.session || '').toLowerCase() === 'rattrapage' ? 'Rattrapage' : 'Normale'} {ex.year}
              </h1>
              <div className="flex items-center gap-1.5 text-[10px] text-slate-400">
                <span>{ex.exercise_name || 'Exercice BAC'}</span>
                {ex.topic && <span className="truncate">· {ex.topic}</span>}
              </div>
            </div>
          </div>

          {/* Separator */}
          <div className="w-px h-7 bg-slate-200 mx-1 hidden lg:block" />

          {/* Question pills — scrollable */}
          <div className="flex-1 min-w-0 hidden lg:flex items-center gap-1 overflow-x-auto py-1 scrollbar-none">
            {ex.questions.map((_q, qIdx) => {
              const key = `${currentExIdx}-${qIdx}`;
              const isCurrent = qIdx === currentQIdx;
              return (
                <button
                  key={qIdx}
                  onClick={() => setCurrentQIdx(qIdx)}
                  title={`Q${qIdx + 1} — ${_q.points} pts`}
                  className={`relative w-7 h-7 rounded-lg text-[10px] font-bold transition-all flex-shrink-0 ${
                    isCurrent
                      ? 'ring-2 ring-offset-1 ring-blue-400 bg-blue-600 text-white'
                      : submitted[key]
                      ? 'bg-emerald-500 text-white'
                      : answers[key]?.trim()
                      ? 'bg-amber-100 text-amber-700'
                      : 'bg-slate-100 text-slate-500 hover:bg-slate-200'
                  }`}
                >
                  {qIdx + 1}
                </button>
              );
            })}
          </div>

          {/* Nav arrows */}
          <div className="flex items-center gap-1 flex-shrink-0">
            <button onClick={goPrev} disabled={currentQIdx === 0} className="p-1.5 rounded-lg border border-slate-200 text-slate-500 hover:bg-slate-50 disabled:opacity-30 transition-all">
              <ArrowLeft className="w-3.5 h-3.5" />
            </button>
            <span className="text-[11px] font-bold text-slate-500 min-w-[40px] text-center">{currentQIdx + 1}/{ex.questions.length}</span>
            <button onClick={goNext} disabled={currentQIdx >= ex.questions.length - 1} className="p-1.5 rounded-lg text-white transition-all disabled:opacity-30 bg-gradient-to-r from-blue-500 to-indigo-500">
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>

          {/* Total points */}
          <div className="hidden lg:flex items-center gap-1 px-2 py-1 rounded-lg bg-amber-50 border border-amber-100 text-amber-700 text-[10px] font-bold flex-shrink-0">
            <Award className="w-3 h-3" />
            {ex.total_points} pts
          </div>

          {/* Close */}
          <button
            onClick={onClose}
            className="text-slate-500 hover:text-slate-800 text-xs px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 transition-all flex-shrink-0"
          >
            Fermer
          </button>
        </div>
      </header>

      {/* ===================== 2-COLUMN BODY (lg+) / stacked (mobile + landscape phones) ===================== */}
      <div className="flex-1 min-h-0 flex">
        {/* LEFT: Question + Documents — visible only on lg+ to avoid duplication on phones (portrait & landscape) */}
        <div className="hidden lg:block flex-1 min-w-0 overflow-y-auto border-r border-slate-200/60">
          <div className="max-w-2xl mx-auto px-3 lg:px-5 py-3 space-y-2">
            {/* Exercise/Part badges */}
            <div className="flex items-center gap-2 flex-wrap">
              {ex.exercise_name && (
                <span className="text-[11px] font-semibold text-slate-500 bg-slate-100 px-2 py-0.5 rounded-md">
                  {ex.exercise_name}
                </span>
              )}
              {ex.part_name && (
                <span className="text-[10px] text-slate-400">{ex.part_name}</span>
              )}
            </div>

            {/* Question (uses same renderer as real exam mode) */}
            <QuestionRenderer
              question={adaptedQuestion as any}
              examId={ex.exam_id}
              showCorrection={showCorrection}
            />
          </div>
        </div>

        {/* RIGHT: Answer input + Aide au tableau — lg+ only (phones use the stacked layout) */}
        <div className="lg:w-[48%] flex-shrink-0 overflow-y-auto bg-white hidden lg:block">
          <div className="px-3 lg:px-4 py-3 space-y-3 max-w-xl">
            {/* Answer input (Texte / Dessin / Photo / Symboles) */}
            <AnswerInput
              questionContent={question.content}
              questionType={questionTypeForInput}
              choices={question.choices}
              value={answers[qKey] || ''}
              onChange={(val) => setAnswers((prev) => ({ ...prev, [qKey]: val }))}
              onImageChange={(img) => setImages((prev) => ({ ...prev, [qKey]: img }))}
              onSubmit={handleSubmit}
              submitting={false}
              disabled={submitted[qKey]}
              showCorrection={submitted[qKey] || showCorrection}
              correctAnswer={question.correct_answer}
              subject={ex.subject}
            />

            {/* Correction toggle (official correction) */}
            {question.correction && (
              <button
                onClick={toggleCorrection}
                className={`w-full flex items-center justify-center gap-2 px-3 py-2 rounded-xl text-[12px] font-medium transition-all border ${
                  showCorrection
                    ? 'bg-emerald-50 text-emerald-700 border-emerald-200 hover:bg-emerald-100'
                    : 'bg-slate-50 text-slate-600 border-slate-200 hover:bg-slate-100'
                }`}
              >
                {showCorrection ? <><EyeOff className="w-3.5 h-3.5" /> Masquer la correction</> : <><Eye className="w-3.5 h-3.5" /> Voir la correction officielle</>}
              </button>
            )}

            {/* Aide au tableau — ask AI to explain on whiteboard */}
            <button
              onClick={handleExplain}
              className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-gradient-to-r from-amber-500 to-orange-500 text-white rounded-xl font-semibold text-sm hover:from-amber-600 hover:to-orange-600 transition-all shadow-md shadow-amber-500/20"
            >
              <Lightbulb className="w-4 h-4" />
              {submitted[qKey] ? 'Explication au tableau' : 'Aide au tableau'}
            </button>
          </div>
        </div>

        {/* MOBILE + LANDSCAPE PHONE stacked layout (<lg) */}
        <div className="lg:hidden flex-1 min-w-0 overflow-y-auto">
          <div className="px-3 py-3 space-y-3">
            <QuestionRenderer
              question={adaptedQuestion as any}
              examId={ex.exam_id}
              showCorrection={showCorrection}
            >
              <AnswerInput
                questionContent={question.content}
                questionType={questionTypeForInput}
                choices={question.choices}
                value={answers[qKey] || ''}
                onChange={(val) => setAnswers((prev) => ({ ...prev, [qKey]: val }))}
                onImageChange={(img) => setImages((prev) => ({ ...prev, [qKey]: img }))}
                onSubmit={handleSubmit}
                submitting={false}
                disabled={submitted[qKey]}
                showCorrection={submitted[qKey] || showCorrection}
                correctAnswer={question.correct_answer}
                subject={ex.subject}
              />

              {question.correction && (
                <button
                  onClick={toggleCorrection}
                  className={`w-full flex items-center justify-center gap-2 px-3 py-2 mt-2 rounded-xl text-[12px] font-medium transition-all border ${
                    showCorrection
                      ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                      : 'bg-slate-50 text-slate-600 border-slate-200'
                  }`}
                >
                  {showCorrection ? <><EyeOff className="w-3.5 h-3.5" /> Masquer</> : <><Eye className="w-3.5 h-3.5" /> Correction</>}
                </button>
              )}

              <button
                onClick={handleExplain}
                className="w-full flex items-center justify-center gap-2 px-4 py-3 mt-3 bg-gradient-to-r from-amber-500 to-orange-500 text-white rounded-xl font-semibold text-sm hover:from-amber-600 hover:to-orange-600 transition-all shadow-md shadow-amber-500/20"
              >
                <Lightbulb className="w-4 h-4" />
                {submitted[qKey] ? 'Explication au tableau' : 'Aide au tableau'}
              </button>

              {/* Mobile nav */}
              <div className="flex items-center justify-between pt-3 border-t border-slate-200/60">
                <button onClick={goPrev} disabled={currentQIdx === 0} className="flex items-center gap-1 px-3 py-1.5 text-xs font-medium text-slate-600 bg-slate-100 rounded-lg disabled:opacity-30">
                  <ArrowLeft className="w-3.5 h-3.5" /> Préc.
                </button>
                <span className="text-[11px] font-bold text-slate-500">{currentQIdx + 1}/{ex.questions.length}</span>
                <button onClick={goNext} disabled={currentQIdx >= ex.questions.length - 1} className="flex items-center gap-1 px-3 py-1.5 text-xs font-medium text-white bg-gradient-to-r from-blue-500 to-indigo-500 rounded-lg disabled:opacity-30">
                  Suiv. <ArrowRight className="w-3.5 h-3.5" />
                </button>
              </div>
            </QuestionRenderer>
          </div>
        </div>
      </div>

      {/* Multi-exercise navigation footer (only when multiple exercises) */}
      {exercises.length > 1 && (
        <div className="shrink-0 border-t border-slate-200/60 bg-slate-50 px-4 py-2 flex items-center justify-between">
          <span className="text-[11px] text-slate-500">
            Exercice {currentExIdx + 1}/{exercises.length}
          </span>
          <div className="flex items-center gap-1">
            <button
              onClick={() => { setCurrentExIdx((p) => Math.max(0, p - 1)); setCurrentQIdx(0); }}
              disabled={currentExIdx === 0}
              className="px-2.5 py-1 rounded-lg text-xs text-slate-600 bg-white border border-slate-200 hover:bg-slate-50 disabled:opacity-30 transition-colors"
            >
              ← Exercice précédent
            </button>
            <button
              onClick={() => { setCurrentExIdx((p) => Math.min(exercises.length - 1, p + 1)); setCurrentQIdx(0); }}
              disabled={currentExIdx === exercises.length - 1}
              className="px-2.5 py-1 rounded-lg text-xs text-white bg-gradient-to-r from-blue-500 to-indigo-500 hover:from-blue-600 hover:to-indigo-600 disabled:opacity-30 transition-colors"
            >
              Exercice suivant →
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
