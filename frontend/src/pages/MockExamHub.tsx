import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { listPublishedMockExams } from '../services/api';
// import { useAuthStore } from '../stores/authStore';
import MobileBottomNav from '../components/MobileBottomNav';
import {
  ArrowLeft, Clock, Award, Play, FileText, Loader2,
  Sparkles, GraduationCap, Target, X,
} from 'lucide-react';

interface MockExamMeta {
  id: string;
  title: string;
  subject: string;
  status: string;
  generated_at: string;
  domains_covered: { part1?: string; part2?: string[] };
}

const DOMAIN_LABELS: Record<string, string> = {
  consommation_matiere_organique: 'Consommation de la matière organique',
  genetique_expression: 'Expression du matériel génétique',
  'genetique_expression+transmission': 'Génétique (expression + transmission)',
  genetique_transmission: 'Transmission des caractères',
  geologie: 'Géologie',
  environnement_sante: 'Environnement & Santé',
};

export default function MockExamHub() {
  const navigate = useNavigate();
  const [exams, setExams] = useState<MockExamMeta[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedSubject, setSelectedSubject] = useState('SVT');
  const [selectedExam, setSelectedExam] = useState<MockExamMeta | null>(null);

  useEffect(() => {
    loadExams();
  }, [selectedSubject]);

  const loadExams = async () => {
    setLoading(true);
    try {
      const res = await listPublishedMockExams(selectedSubject);
      setExams(res.data || []);
    } catch {
      setExams([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#070718] text-white pb-24 md:pb-8">
      {/* Header */}
      <div className="sticky top-0 z-30 bg-[#070718]/95 backdrop-blur-md border-b border-white/5">
        <div className="max-w-5xl mx-auto px-4 py-3 flex items-center gap-3">
          <button
            onClick={() => navigate('/dashboard')}
            className="p-2 rounded-xl bg-white/5 hover:bg-white/10 transition"
          >
            <ArrowLeft size={18} />
          </button>
          <div className="flex items-center gap-2">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-violet-500 to-purple-600 flex items-center justify-center">
              <Sparkles size={18} />
            </div>
            <div>
              <h1 className="text-lg font-bold">Examens Blancs</h1>
              <p className="text-xs text-white/40">Entraînement en conditions réelles</p>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-5xl mx-auto px-4 pt-6">
        {/* Info Banner */}
        <div className="mb-6 p-4 rounded-2xl bg-gradient-to-r from-violet-600/20 to-purple-600/20 border border-violet-500/20">
          <div className="flex items-start gap-3">
            <div className="p-2 rounded-xl bg-violet-500/20">
              <Target size={20} className="text-violet-300" />
            </div>
            <div>
              <h3 className="font-semibold text-violet-200 mb-1">Examens générés par IA</h3>
              <p className="text-sm text-white/50 leading-relaxed">
                Ces examens blancs respectent <span className="text-violet-300">le cadre de référence officiel</span> du
                Baccalauréat marocain. Structure, barème et types de questions identiques aux examens nationaux.
              </p>
            </div>
          </div>
        </div>

        {/* Subject Tabs */}
        <div className="flex flex-wrap gap-2 mb-6 -mx-1 px-1 overflow-x-auto sm:overflow-visible">
          {['SVT', 'mathematiques', 'physique'].map(s => (
            <button
              key={s}
              onClick={() => setSelectedSubject(s)}
              className={`flex-shrink-0 px-3 sm:px-4 py-2 rounded-xl text-xs sm:text-sm font-medium transition whitespace-nowrap ${
                selectedSubject === s
                  ? 'bg-gradient-to-r from-emerald-500 to-teal-600 text-white shadow-lg shadow-emerald-500/20'
                  : 'bg-white/5 text-white/50 hover:bg-white/10'
              }`}
            >
              {s === 'SVT' ? '🧬 SVT' : s === 'mathematiques' ? '📐 Maths' : s === 'physique' ? '⚛️ Physique' : s}
            </button>
          ))}
        </div>

        {/* Loading */}
        {loading && (
          <div className="flex items-center justify-center py-20">
            <Loader2 className="w-8 h-8 animate-spin text-violet-400" />
          </div>
        )}

        {/* Empty State */}
        {!loading && exams.length === 0 && (
          <div className="text-center py-20">
            <div className="w-16 h-16 mx-auto mb-4 rounded-2xl bg-white/5 flex items-center justify-center">
              <FileText size={28} className="text-white/20" />
            </div>
            <h3 className="text-lg font-semibold text-white/40 mb-2">Aucun examen blanc disponible</h3>
            <p className="text-sm text-white/25">Les examens blancs seront publiés prochainement.</p>
          </div>
        )}

        {/* Exam Cards */}
        {!loading && exams.length > 0 && (
          <div className="grid gap-4 md:grid-cols-2">
            {exams.map(exam => {
              const domains = exam.domains_covered?.part2 || [];
              const p1Label = DOMAIN_LABELS[exam.domains_covered?.part1 || ''] || 'SVT';
              return (
                <div
                  key={exam.id}
                  className="group relative p-5 rounded-2xl bg-white/[0.03] border border-white/[0.06] hover:border-violet-500/30 hover:bg-white/[0.05] transition-all duration-300 cursor-pointer"
                  onClick={() => setSelectedExam(exam)}
                >
                  {/* Top row */}
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center gap-2">
                      <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-violet-500 to-purple-600 flex items-center justify-center text-lg">
                        🧬
                      </div>
                      <div>
                        <h3 className="font-semibold text-white/90 text-sm leading-tight">{exam.title}</h3>
                        <p className="text-xs text-white/30 mt-0.5">
                          {new Date(exam.generated_at).toLocaleDateString('fr-FR')}
                        </p>
                      </div>
                    </div>
                    <span className="px-2.5 py-1 rounded-lg text-xs font-medium bg-violet-500/15 text-violet-300">
                      P1: {p1Label}
                    </span>
                  </div>

                  {/* Domains */}
                  <div className="flex flex-wrap gap-1.5 mb-4">
                    {domains.map((d: string, i: number) => (
                      <span key={i} className="px-2 py-0.5 rounded-md bg-white/5 text-[11px] text-white/40">
                        {DOMAIN_LABELS[d] || d}
                      </span>
                    ))}
                  </div>

                  {/* Footer */}
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3 text-xs text-white/30">
                      <span className="flex items-center gap-1"><Clock size={12} /> 3h</span>
                      <span className="flex items-center gap-1"><Award size={12} /> 20 pts</span>
                      <span className="flex items-center gap-1"><GraduationCap size={12} /> Coef. 5</span>
                    </div>
                    <div className="flex items-center gap-1.5 text-violet-300 text-xs font-medium opacity-0 group-hover:opacity-100 transition">
                      <Play size={14} /> Commencer
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Mode picker modal — same UX as ExamHub */}
      {selectedExam && (
        <MockModeModal
          exam={selectedExam}
          onClose={() => setSelectedExam(null)}
          onStart={(mode) => {
            const ex = selectedExam;
            setSelectedExam(null);
            navigate(mode === 'practice' ? `/exam/practice/${ex.id}` : `/exam/real/${ex.id}`);
          }}
        />
      )}

      <MobileBottomNav active="mock" />
    </div>
  );
}

/* ─── Mode picker modal (Entraînement / Examen Réel) ─── */
function MockModeModal({
  exam,
  onClose,
  onStart,
}: {
  exam: MockExamMeta;
  onClose: () => void;
  onStart: (mode: 'practice' | 'real') => void;
}) {
  return (
    <div
      className="fixed inset-0 z-50 flex items-end sm:items-center justify-center bg-black/70 backdrop-blur-md p-0 sm:p-4"
      onClick={onClose}
    >
      <div
        className="w-full sm:max-w-lg rounded-t-3xl sm:rounded-3xl overflow-hidden shadow-2xl bg-[#0e0e22] border border-white/10"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="relative bg-gradient-to-br from-violet-600 to-purple-700 p-5 text-white">
          <button
            onClick={onClose}
            className="absolute top-3 right-3 w-8 h-8 rounded-full bg-white/20 hover:bg-white/30 flex items-center justify-center transition-colors"
            aria-label="Fermer"
          >
            <X className="w-4 h-4" />
          </button>
          <p className="text-[10px] font-bold text-white/80 uppercase tracking-widest">
            Examen Blanc — généré par IA
          </p>
          <h3 className="text-lg font-bold mt-0.5 leading-tight">{exam.title}</h3>
          <div className="flex items-center gap-3 mt-3 text-xs text-white/85">
            <span className="inline-flex items-center gap-1"><Clock className="w-3 h-3" /> 3h</span>
            <span className="inline-flex items-center gap-1"><Award className="w-3 h-3" /> /20 pts</span>
            <span className="inline-flex items-center gap-1"><GraduationCap className="w-3 h-3" /> Coef. 5</span>
          </div>
        </div>

        {/* Body */}
        <div className="p-5 space-y-3">
          <p className="text-sm text-white/70 font-medium">Choisissez votre mode :</p>
          <button
            onClick={() => onStart('practice')}
            className="w-full flex items-center gap-4 p-4 rounded-2xl border-2 border-blue-400/30 hover:border-blue-400/60 hover:bg-blue-500/10 transition-all group text-left"
          >
            <div className="w-11 h-11 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 text-white flex items-center justify-center">
              <GraduationCap className="w-5 h-5" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="font-bold text-white">Mode Entraînement</p>
              <p className="text-xs text-white/55">Feedback instantané + corrections IA</p>
            </div>
            <span className="text-blue-300 text-lg transition-transform group-hover:translate-x-0.5">→</span>
          </button>
          <button
            onClick={() => onStart('real')}
            className="w-full flex items-center gap-4 p-4 rounded-2xl border-2 border-rose-400/30 hover:border-rose-400/60 hover:bg-rose-500/10 transition-all group text-left"
          >
            <div className="w-11 h-11 rounded-xl bg-gradient-to-br from-red-500 to-rose-600 text-white flex items-center justify-center">
              <Clock className="w-5 h-5" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="font-bold text-white">Mode Examen Réel</p>
              <p className="text-xs text-white/55">3h chrono — conditions du BAC</p>
            </div>
            <span className="text-rose-300 text-lg transition-transform group-hover:translate-x-0.5">→</span>
          </button>
        </div>
      </div>
    </div>
  );
}
