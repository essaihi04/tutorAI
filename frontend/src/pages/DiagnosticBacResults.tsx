import { useLocation, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import LatexRenderer from '../components/LatexRenderer';
import {
  Trophy, ArrowRight, CheckCircle, XCircle, RotateCcw,
  BookOpen, Zap, Star, ChevronDown, ChevronUp, Calendar,
} from 'lucide-react';

interface PlanItem {
  day_start: number;
  day_end: number;
  subject: string;
  domain: string;
  emoji: string;
  score_pct: number | null;
  label: string;
  tasks: string[];
}

interface Results {
  score: number;
  total: number;
  bac_note_predicted: number;
  gain_if_subscribed: number;
  by_subject: Record<string, { correct: number; total: number; pct: number }>;
  weak_domains: Array<{ domain: string; subject: string; correct: number; total: number; pct: number }>;
  detailed: Array<{
    position: number;
    subject: string;
    domain: string;
    content: string;
    choices: Array<{ letter: string; text: string }>;
    user_answer: string;
    correct_answer: string;
    is_correct: boolean;
  }>;
  plan: PlanItem[];
}

const NOTE_COLOR = (n: number) => {
  if (n >= 16) return 'text-emerald-400';
  if (n >= 14) return 'text-green-400';
  if (n >= 12) return 'text-yellow-400';
  if (n >= 10) return 'text-orange-400';
  return 'text-red-400';
};

const NOTE_LABEL = (n: number) => {
  if (n >= 16) return { text: 'Excellent 🏆', color: 'emerald' };
  if (n >= 14) return { text: 'Bien 🎯', color: 'green' };
  if (n >= 12) return { text: 'Assez bien 👍', color: 'yellow' };
  if (n >= 10) return { text: 'Passable ⚠️', color: 'orange' };
  return { text: 'À travailler 💪', color: 'red' };
};

// Simple SVG Radar chart — 2 axes: SVT and PC
function RadarChart({ bySubject }: { bySubject: Results['by_subject'] }) {
  const subjects = ['SVT', 'Physique-Chimie'];
  const values = subjects.map(s => (bySubject[s]?.pct ?? 0) / 100);
  const icons = ['🧬', '⚗️'];
  const colors = ['#34d399', '#818cf8'];

  const cx = 100, cy = 100, r = 70;
  // 2 axes at 90° and 270°
  const angles = [270, 90].map(d => (d * Math.PI) / 180);
  const pts = (v: number[]) =>
    v.map((val, i) => {
      const a = angles[i];
      return `${cx + r * val * Math.cos(a)},${cy + r * val * Math.sin(a)}`;
    }).join(' ');

  return (
    <svg viewBox="0 0 200 200" className="w-full max-w-[180px] mx-auto">
      {/* Grid circles */}
      {[0.25, 0.5, 0.75, 1].map(f => (
        <circle key={f} cx={cx} cy={cy} r={r * f} fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth="1" />
      ))}
      {/* Axes */}
      {angles.map((a, i) => (
        <line key={i} x1={cx} y1={cy} x2={cx + r * Math.cos(a)} y2={cy + r * Math.sin(a)}
          stroke="rgba(255,255,255,0.12)" strokeWidth="1" />
      ))}
      {/* Data polygon */}
      <polygon points={pts(values)} fill="rgba(99,102,241,0.25)" stroke="#818cf8" strokeWidth="2" />
      {/* Data dots */}
      {values.map((v, i) => (
        <circle key={i} cx={cx + r * v * Math.cos(angles[i])} cy={cy + r * v * Math.sin(angles[i])}
          r="5" fill={colors[i]} stroke="#070718" strokeWidth="2" />
      ))}
      {/* Labels */}
      {subjects.map((s, i) => {
        const lx = cx + (r + 18) * Math.cos(angles[i]);
        const ly = cy + (r + 18) * Math.sin(angles[i]);
        return (
          <text key={i} x={lx} y={ly} textAnchor="middle" dominantBaseline="middle"
            fill="rgba(255,255,255,0.8)" fontSize="9" fontWeight="600">
            {icons[i]} {Math.round((bySubject[s]?.pct ?? 0))}%
          </text>
        );
      })}
    </svg>
  );
}

export default function DiagnosticBacResults() {
  const location = useLocation();
  const navigate = useNavigate();
  const results: Results | null = location.state?.results ?? null;
  const [showDetails, setShowDetails] = useState(false);

  useEffect(() => {
    window.scrollTo({ top: 0 });
  }, []);

  if (!results) {
    return (
      <div className="min-h-screen bg-[#070718] text-white flex items-center justify-center">
        <div className="text-center">
          <p className="text-white/60 mb-4">Aucun résultat à afficher.</p>
          <button onClick={() => navigate('/bac-diagnostic')}
            className="px-6 py-3 bg-indigo-600 rounded-xl font-bold text-sm">
            Refaire le test
          </button>
        </div>
      </div>
    );
  }

  const { score, total, bac_note_predicted, gain_if_subscribed, by_subject, weak_domains, detailed, plan } = results;
  const label = NOTE_LABEL(bac_note_predicted);
  const noteMax = bac_note_predicted + gain_if_subscribed;

  return (
    <div className="min-h-screen bg-[#070718] text-white">
      {/* Ambient glow */}
      <div className="pointer-events-none fixed inset-0 overflow-hidden">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[700px] h-[400px] bg-indigo-600/15 blur-[120px] rounded-full" />
        <div className="absolute bottom-0 right-0 w-[400px] h-[300px] bg-emerald-600/10 blur-[100px] rounded-full" />
      </div>

      <div className="relative z-10 max-w-2xl mx-auto px-4 py-8 space-y-6">

        {/* ── SCORE CARD ── */}
        <div className="bg-white/[.04] border border-white/10 rounded-3xl p-6 text-center shadow-2xl">
          <div className="flex items-center justify-center gap-2 mb-4">
            <Trophy className="w-5 h-5 text-yellow-400" />
            <span className="text-sm font-bold text-white/70 uppercase tracking-widest">Ton résultat</span>
          </div>

          {/* Big score */}
          <div className="flex items-end justify-center gap-3 mb-2">
            <span className={`text-7xl font-black tabular-nums ${NOTE_COLOR(bac_note_predicted)}`}>
              {bac_note_predicted.toFixed(1)}
            </span>
            <span className="text-2xl text-white/40 mb-3 font-bold">/20</span>
          </div>
          <div className="text-white/60 text-sm mb-1">Note BAC estimée</div>
          <div className={`inline-block px-3 py-1 rounded-full text-sm font-bold mb-4 ${
            label.color === 'emerald' ? 'bg-emerald-500/15 text-emerald-200' :
            label.color === 'green' ? 'bg-green-500/15 text-green-200' :
            label.color === 'yellow' ? 'bg-yellow-500/15 text-yellow-200' :
            label.color === 'orange' ? 'bg-orange-500/15 text-orange-200' :
            'bg-red-500/15 text-red-200'
          }`}>
            {label.text}
          </div>

          {/* Raw score */}
          <div className="text-white/40 text-xs mb-5">
            {score}/{total} réponses correctes ({Math.round(score / total * 100)}%)
          </div>

          {/* Radar */}
          <div className="mb-5">
            <RadarChart bySubject={by_subject} />
            <div className="flex justify-center gap-6 mt-2">
              {Object.entries(by_subject).map(([s, v]) => (
                <div key={s} className="text-center">
                  <div className="text-xs font-semibold text-white/80">{s === 'SVT' ? '🧬 SVT' : '⚗️ PC'}</div>
                  <div className="text-lg font-black text-white">{v.pct}%</div>
                  <div className="text-white/40 text-[10px]">{v.correct}/{v.total}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Gain banner */}
          <div className="bg-gradient-to-r from-indigo-500/20 to-purple-500/20 border border-indigo-400/30 rounded-2xl p-4">
            <div className="flex items-center justify-center gap-2 mb-1">
              <Zap className="w-4 h-4 text-indigo-300" />
              <span className="text-indigo-200 font-bold text-sm">Avec le coaching personnalisé</span>
            </div>
            <div className="text-white text-2xl font-black">
              {bac_note_predicted.toFixed(1)} → <span className="text-indigo-300">{Math.min(noteMax, 20).toFixed(1)}/20</span>
            </div>
            <div className="text-white/50 text-xs mt-1">
              +{gain_if_subscribed} points en {28} jours de travail ciblé
            </div>
          </div>
        </div>

        {/* ── WEAK DOMAINS ── */}
        {weak_domains.length > 0 && (
          <div className="bg-white/[.03] border border-white/10 rounded-2xl p-5">
            <h2 className="text-sm font-bold text-white/80 uppercase tracking-wide mb-4 flex items-center gap-2">
              <XCircle className="w-4 h-4 text-red-400" /> Tes lacunes prioritaires
            </h2>
            <div className="space-y-2.5">
              {weak_domains.slice(0, 5).map((d, i) => (
                <div key={i} className="flex items-center gap-3">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-xs font-semibold text-white truncate">{d.domain}</span>
                      <span className="text-[10px] text-white/40">{d.subject === 'SVT' ? '🧬' : '⚗️'}</span>
                    </div>
                    <div className="w-full bg-white/5 rounded-full h-1.5 overflow-hidden">
                      <div
                        className={`h-full rounded-full transition-all ${
                          d.pct < 40 ? 'bg-red-500' : d.pct < 70 ? 'bg-yellow-500' : 'bg-emerald-500'
                        }`}
                        style={{ width: `${d.pct}%` }}
                      />
                    </div>
                  </div>
                  <span className={`text-sm font-bold flex-shrink-0 ${
                    d.pct < 40 ? 'text-red-400' : d.pct < 70 ? 'text-yellow-400' : 'text-emerald-400'
                  }`}>{d.pct}%</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ── 28-DAY PLAN ── */}
        <div className="bg-white/[.03] border border-white/10 rounded-2xl p-5">
          <h2 className="text-sm font-bold text-white/80 uppercase tracking-wide mb-4 flex items-center gap-2">
            <Calendar className="w-4 h-4 text-indigo-400" /> Ton plan J-28
          </h2>
          <div className="space-y-3">
            {plan.map((item, i) => {
              const dayRange = item.day_start === item.day_end
                ? `Jour ${item.day_start}`
                : `Jours ${item.day_start}–${item.day_end}`;
              return (
                <div key={i} className={`rounded-xl border p-3.5 ${
                  item.label.includes('🔴') ? 'border-red-400/25 bg-red-500/8' :
                  item.label.includes('🟡') ? 'border-yellow-400/25 bg-yellow-500/8' :
                  item.label.includes('🏁') ? 'border-indigo-400/25 bg-indigo-500/10' :
                  'border-emerald-400/20 bg-emerald-500/8'
                }`}>
                  <div className="flex items-start gap-3">
                    <span className="text-2xl flex-shrink-0 mt-0.5">{item.emoji}</span>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 flex-wrap mb-1">
                        <span className="text-white font-bold text-sm">{item.domain}</span>
                        {item.score_pct !== null && (
                          <span className={`text-[10px] font-semibold px-1.5 py-0.5 rounded-full ${
                            item.score_pct < 40 ? 'bg-red-500/20 text-red-300' :
                            item.score_pct < 70 ? 'bg-yellow-500/20 text-yellow-300' :
                            'bg-emerald-500/20 text-emerald-300'
                          }`}>{item.score_pct}% au test</span>
                        )}
                      </div>
                      <div className="text-white/40 text-[10px] mb-2">{dayRange} · {item.label}</div>
                      <ul className="space-y-1">
                        {item.tasks.map((t, j) => (
                          <li key={j} className="flex items-start gap-1.5 text-xs text-white/65">
                            <span className="text-white/30 mt-0.5 flex-shrink-0">→</span>
                            {t}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* ── CTA SUBSCRIPTION ── */}
        <div className="bg-gradient-to-br from-indigo-900/60 to-purple-900/60 border border-indigo-400/30 rounded-3xl p-6 text-center shadow-2xl">
          <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center mx-auto mb-4 shadow-lg">
            <Star className="w-7 h-7 text-white" />
          </div>
          <h3 className="text-xl font-black text-white mb-2">
            Passe de {bac_note_predicted.toFixed(1)} à {Math.min(noteMax, 20).toFixed(1)}/20
          </h3>
          <p className="text-white/60 text-sm mb-4 leading-relaxed">
            Accède au coaching IA personnalisé, aux exercices ciblés sur tes lacunes,
            et à ton plan de révision adaptatif jour par jour.
          </p>
          <div className="flex flex-col gap-3">
            <button
              onClick={() => navigate('/signup')}
              className="w-full py-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl font-black text-base shadow-lg shadow-indigo-500/30 hover:shadow-xl hover:scale-[1.01] active:scale-[0.99] transition-all flex items-center justify-center gap-2"
            >
              <Zap className="w-5 h-5" />
              S'inscrire et commencer le plan — Gratuit
            </button>
            <button
              onClick={() => navigate('/bac-diagnostic')}
              className="w-full py-2.5 bg-white/5 text-white/60 rounded-xl text-sm hover:bg-white/10 flex items-center justify-center gap-2 transition-all"
            >
              <RotateCcw className="w-4 h-4" /> Refaire le test
            </button>
          </div>
          <p className="text-white/25 text-xs mt-3">
            Déjà inscrit ? <button onClick={() => navigate('/login')} className="text-indigo-300 underline">Se connecter</button>
          </p>
        </div>

        {/* ── DETAIL TOGGLE ── */}
        <button
          onClick={() => setShowDetails(v => !v)}
          className="w-full flex items-center justify-center gap-2 py-3 bg-white/[.03] border border-white/8 rounded-xl text-white/50 text-sm hover:bg-white/[.05] hover:text-white/70 transition-all"
        >
          {showDetails ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          {showDetails ? 'Masquer' : 'Voir'} le détail des {total} questions
        </button>

        {showDetails && (
          <div className="space-y-3">
            {detailed.map((q, i) => (
              <div key={i} className={`rounded-xl border p-4 ${
                q.is_correct ? 'border-emerald-400/20 bg-emerald-500/5' : 'border-red-400/20 bg-red-500/5'
              }`}>
                <div className="flex items-start gap-3 mb-3">
                  {q.is_correct
                    ? <CheckCircle className="w-4 h-4 text-emerald-400 mt-0.5 flex-shrink-0" />
                    : <XCircle className="w-4 h-4 text-red-400 mt-0.5 flex-shrink-0" />
                  }
                  <div>
                    <div className="text-[10px] text-white/40 mb-1">{q.domain} · {q.subject}</div>
                    <p className="text-white/80 text-xs leading-relaxed">
                      <LatexRenderer content={q.content} />
                    </p>
                  </div>
                </div>
                {!q.is_correct && (
                  <div className="ml-7 flex flex-col gap-1">
                    {q.user_answer && q.user_answer !== 'skip' && (
                      <div className="text-xs text-red-300">
                        ✗ Ta réponse : <span className="font-bold">{q.user_answer.toUpperCase()}</span>
                      </div>
                    )}
                    {q.user_answer === 'skip' && (
                      <div className="text-xs text-white/40">✗ Non répondu</div>
                    )}
                    <div className="text-xs text-emerald-300">
                      ✓ Bonne réponse : <span className="font-bold">{q.correct_answer.toUpperCase()}</span>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
