import { useLocation, useNavigate } from 'react-router-dom';
import { useEffect, useState, useMemo } from 'react';
import LatexRenderer from '../components/LatexRenderer';
import BacCountdown from '../components/BacCountdown';
import {
  CheckCircle, XCircle, RotateCcw, Zap,
  ChevronDown, ChevronUp, Calendar, Share2,
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

// ── Helpers ──────────────────────────────────────────────────────────────────

const BAC_DATE = new Date('2026-06-04T08:00:00');
function getDaysLeft() {
  return Math.max(0, Math.ceil((BAC_DATE.getTime() - Date.now()) / (1000 * 60 * 60 * 24)));
}

function getMention(avg: number) {
  if (avg >= 16) return { fr: 'Très Bien',  tw: 'text-emerald-400' };
  if (avg >= 14) return { fr: 'Bien',        tw: 'text-blue-400'   };
  if (avg >= 12) return { fr: 'Assez Bien',  tw: 'text-violet-400' };
  if (avg >= 10) return { fr: 'Passable',    tw: 'text-amber-400'  };
  return            { fr: 'Non Admis',   tw: 'text-red-400'    };
}

function subjectNote(pct: number) { return +(pct / 100 * 20).toFixed(2); }
function noteColor(n: number) {
  if (n >= 14) return 'text-emerald-400';
  if (n >= 10) return 'text-amber-400';
  return 'text-red-400';
}

function buildShareImage(avg: number, mentionFr: string, code: string): string {
  const W = 1080, H = 1080;
  const cv = document.createElement('canvas');
  cv.width = W; cv.height = H;
  const ctx = cv.getContext('2d')!;
  const bg = ctx.createLinearGradient(0, 0, W, H);
  bg.addColorStop(0, '#070718'); bg.addColorStop(1, '#0f0f2e');
  ctx.fillStyle = bg; ctx.fillRect(0, 0, W, H);
  const glow = ctx.createRadialGradient(W/2, 0, 0, W/2, 0, 520);
  glow.addColorStop(0, 'rgba(99,102,241,0.28)'); glow.addColorStop(1, 'transparent');
  ctx.fillStyle = glow; ctx.fillRect(0, 0, W, H);
  ctx.textAlign = 'center';
  ctx.font = 'bold 46px Arial'; ctx.fillStyle = 'rgba(255,255,255,0.92)';
  ctx.fillText('MOALIM · موليم', W/2, 92);
  ctx.font = '30px Arial'; ctx.fillStyle = 'rgba(167,139,250,0.85)';
  ctx.fillText('نتائج الباكالوريا 2026 — Session Normale', W/2, 144);
  ctx.strokeStyle = 'rgba(255,255,255,0.08)'; ctx.lineWidth = 1;
  ctx.beginPath(); ctx.moveTo(130, 168); ctx.lineTo(W-130, 168); ctx.stroke();
  ctx.font = '26px monospace'; ctx.fillStyle = 'rgba(255,255,255,0.28)';
  ctx.fillText('رمز مسار: ' + code, W/2, 208);
  const CX = W/2, CY = 435, CR = 168;
  const col = avg >= 10 ? '#4ade80' : '#f87171';
  ctx.strokeStyle = col; ctx.lineWidth = 14;
  ctx.beginPath(); ctx.arc(CX, CY, CR, 0, Math.PI*2); ctx.stroke();
  ctx.fillStyle = 'rgba(255,255,255,0.03)';
  ctx.beginPath(); ctx.arc(CX, CY, CR, 0, Math.PI*2); ctx.fill();
  ctx.font = 'bold 112px Arial'; ctx.fillStyle = col;
  ctx.fillText(avg.toFixed(2), CX, CY + 24);
  ctx.font = 'bold 46px Arial'; ctx.fillStyle = 'rgba(255,255,255,0.42)';
  ctx.fillText('/ 20', CX, CY + 84);
  ctx.font = 'bold 52px Arial'; ctx.fillStyle = col;
  ctx.fillText('Mention : ' + mentionFr, CX, 665);
  ctx.font = 'bold 40px Arial'; ctx.fillStyle = 'rgba(255,255,255,0.88)';
  ctx.fillText('انت كم حصلت في الباكالوريا 2026؟', CX, 768);
  ctx.font = '34px Arial'; ctx.fillStyle = 'rgba(255,255,255,0.52)';
  ctx.fillText('اختبر نتيجتك في 20 سؤال فقط ↓', CX, 822);
  ctx.fillStyle = 'rgba(99,102,241,0.65)';
  ctx.fillRect(210, 866, W-420, 76);
  ctx.font = 'bold 32px Arial'; ctx.fillStyle = 'white';
  ctx.fillText('moalim.online/bac-diagnostic', CX, 913);
  ctx.font = '22px Arial'; ctx.fillStyle = 'rgba(255,255,255,0.18)';
  ctx.fillText('Test diagnostique · Estimation BAC · non officiel', CX, 1004);
  return cv.toDataURL('image/png');
}


export default function DiagnosticBacResults() {
  const location = useLocation();
  const navigate = useNavigate();
  const results: Results | null = location.state?.results ?? null;
  const [showDetails, setShowDetails] = useState(false);
  const [copied, setCopied] = useState(false);
  const daysLeft = getDaysLeft();

  const massarCode = useMemo(() => `B${Math.floor(10000000 + Math.random() * 89999999)}`, []);

  useEffect(() => { window.scrollTo({ top: 0 }); }, []);

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

  const { total, bac_note_predicted, gain_if_subscribed, by_subject, weak_domains, detailed, plan } = results;
  const mention = getMention(bac_note_predicted);
  const noteMax = Math.min(bac_note_predicted + gain_if_subscribed, 20);
  const isAdmis = bac_note_predicted >= 10;

  const SUBJECTS = [
    { key: 'SVT',             ar: 'علوم الحياة والأرض', short: 'SVT'   },
    { key: 'Physique-Chimie', ar: 'الفيزياء والكيمياء',  short: 'PC'    },
    { key: 'Mathématiques',   ar: 'الرياضيات',           short: 'Maths' },
  ];

  const shareText = `🎓 حصلت على ${bac_note_predicted.toFixed(2)}/20 في الباكالوريا 2026!\nMention: ${mention.fr}\n\nأنت كم حصلت؟ اختبر نتيجتك في 20 سؤال 👇\nhttps://moalim.online/bac-diagnostic`;

  function shareWhatsApp() {
    window.open(`https://wa.me/?text=${encodeURIComponent(shareText)}`, '_blank');
  }
  function shareFacebook() {
    window.open(`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent('https://moalim.online/bac-diagnostic')}`, '_blank');
  }
  function downloadImage() {
    const url = buildShareImage(bac_note_predicted, mention.fr, massarCode);
    const a = document.createElement('a');
    a.href = url; a.download = 'bac-2026-resultats.png'; a.click();
  }
  async function copyText() {
    await navigator.clipboard.writeText(shareText);
    setCopied(true); setTimeout(() => setCopied(false), 2200);
  }

  return (
    <div className="min-h-screen bg-[#070718] text-white">
      {/* Ambient */}
      <div className="pointer-events-none fixed inset-0 -z-0 overflow-hidden">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[560px] h-[320px] bg-indigo-600/15 blur-[110px] rounded-full" />
      </div>

      {/* ══════ PRIMARY FOLD — everything fits in one screen ══════ */}
      <div className="relative z-10 flex flex-col items-center justify-center min-h-screen px-3 py-3">
        <div className="w-full max-w-sm space-y-2">

          {/* ── Massar-style result card ── */}
          <div className="bg-[#0d0d24] border border-white/[.12] rounded-2xl overflow-hidden shadow-2xl">

            {/* Header bar */}
            <div className="bg-[#12122e] px-4 py-2.5 border-b border-white/[.08] flex items-center justify-between">
              <div>
                <div className="text-[9px] text-white/30 uppercase tracking-widest">وزارة التربية الوطنية · MASSAR</div>
                <div className="text-[11px] font-bold text-white mt-0.5">نتائج الباكالوريا — Session Normale 2026</div>
              </div>
              <div className="text-right">
                <div className="text-[9px] text-white/30">رمز مسار</div>
                <div className="text-[11px] font-mono font-bold text-white/65 mt-0.5">{massarCode}</div>
              </div>
            </div>

            {/* Info rows — RTL */}
            <div dir="rtl" className="px-4 py-2.5 border-b border-white/[.05] space-y-1.5">
              <div className="flex justify-between items-center">
                <span className="text-white text-xs">الثانية باكالوريا علوم فيزيائية</span>
                <span className="text-white/35 text-[10px]">المستوى</span>
              </div>
              <div className="flex justify-between items-center">
                <span className={`text-[11px] font-bold ${mention.tw}`}>
                  {isAdmis ? 'ناجح(ة)' : 'غير ناجح'} · Mention : {mention.fr}
                </span>
                <span className="text-white/35 text-[10px]">النتيجة</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-white font-black text-2xl tabular-nums">{bac_note_predicted.toFixed(2)} / 20</span>
                <span className="text-white/35 text-[10px]">المعدل العام 2026</span>
              </div>
            </div>

            {/* Scores table — RTL */}
            <div className="px-4 py-2.5">
              <div className="text-[10px] text-red-400 font-bold mb-1.5 text-right">: بيان النقط حسب المادة</div>
              <table className="w-full" dir="rtl">
                <thead>
                  <tr className="border-b border-white/[.06]">
                    <th className="text-right text-white/35 font-medium py-1 text-[10px]">المادة</th>
                    <th className="text-center text-white/35 font-medium py-1 text-[10px]">النقطة</th>
                  </tr>
                </thead>
                <tbody>
                  {SUBJECTS.map(s => {
                    const d = by_subject[s.key];
                    const note = d ? subjectNote(d.pct) : 0;
                    return (
                      <tr key={s.key} className="border-b border-white/[.04] last:border-0">
                        <td className="py-1.5">
                          <div className="text-white text-xs font-medium">{s.ar}</div>
                          <div className="text-white/25 text-[9px]">{s.short}</div>
                        </td>
                        <td className="py-1.5 text-center">
                          <span className={`text-base font-black tabular-nums ${noteColor(note)}`}>{note.toFixed(2)}</span>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
              <div className="text-[8px] text-white/15 text-center mt-1.5">
                Estimation · moalim.online · Résultat non officiel
              </div>
            </div>
          </div>

          {/* ── Countdown strip ── */}
          <div className="bg-white/[.03] border border-white/[.07] rounded-xl px-3 py-1.5 flex items-center justify-between">
            <span className="text-white/30 text-[9px] uppercase tracking-widest">BAC · 4 Juin 2026</span>
            <BacCountdown size="sm" />
          </div>

          {/* ── +4pts upgrade CTA ── */}
          <div className="bg-gradient-to-r from-indigo-600/25 to-purple-600/25 border border-indigo-400/30 rounded-xl p-3 flex items-center justify-between gap-3">
            <div className="min-w-0">
              <div className="text-white/40 text-[10px] mb-0.5">Avec le coaching IA · Moalim</div>
              <div className="flex items-center gap-1.5 flex-wrap">
                <span className="text-white font-black text-lg">{bac_note_predicted.toFixed(1)}</span>
                <span className="text-white/35 text-sm">→</span>
                <span className="text-indigo-300 font-black text-lg">{noteMax.toFixed(1)}</span>
                <span className="text-emerald-400 text-[10px] font-bold bg-emerald-400/10 border border-emerald-400/20 px-1.5 py-0.5 rounded-full">
                  +{gain_if_subscribed} pts
                </span>
              </div>
              <div className="text-white/25 text-[9px] mt-0.5">
                {daysLeft} jours restants · {mention.fr === 'Passable' ? 'Vise Assez Bien' : mention.fr === 'Assez Bien' ? 'Vise Bien' : 'Vise Très Bien'}
              </div>
            </div>
            <button
              onClick={() => navigate('/inscription')}
              className="shrink-0 px-3.5 py-2.5 bg-gradient-to-r from-indigo-600 to-purple-600 text-white text-xs font-bold rounded-xl shadow-lg shadow-indigo-500/25 hover:opacity-90 active:scale-95 transition-all flex items-center gap-1.5"
            >
              <Zap className="w-3.5 h-3.5" />
              Commencer
            </button>
          </div>

          {/* ── Share buttons ── */}
          <div>
            <div className="flex items-center justify-center gap-1.5 mb-1.5">
              <Share2 className="w-3 h-3 text-white/30" />
              <span className="text-white/30 text-[9px] uppercase tracking-widest">Partager · شارك نتيجتك</span>
            </div>
            <div className="grid grid-cols-4 gap-1.5">
              <button onClick={shareWhatsApp}
                className="flex flex-col items-center gap-1 py-2 bg-[#25D366]/10 border border-[#25D366]/25 rounded-xl hover:bg-[#25D366]/20 active:scale-95 transition-all">
                <span className="text-base">💬</span>
                <span className="text-[9px] text-[#25D366] font-semibold">WhatsApp</span>
              </button>
              <button onClick={shareFacebook}
                className="flex flex-col items-center gap-1 py-2 bg-[#1877F2]/10 border border-[#1877F2]/25 rounded-xl hover:bg-[#1877F2]/20 active:scale-95 transition-all">
                <span className="text-base">📘</span>
                <span className="text-[9px] text-[#1877F2] font-semibold">Facebook</span>
              </button>
              <button onClick={downloadImage}
                className="flex flex-col items-center gap-1 py-2 bg-gradient-to-b from-purple-500/10 to-pink-500/10 border border-purple-400/25 rounded-xl hover:opacity-80 active:scale-95 transition-all">
                <span className="text-base">📸</span>
                <span className="text-[9px] text-purple-300 font-semibold">Instagram</span>
              </button>
              <button onClick={downloadImage}
                className="flex flex-col items-center gap-1 py-2 bg-white/[.04] border border-white/10 rounded-xl hover:bg-white/[.08] active:scale-95 transition-all">
                <span className="text-base">🎵</span>
                <span className="text-[9px] text-white/50 font-semibold">TikTok</span>
              </button>
            </div>
            <button onClick={copyText}
              className="w-full mt-1 py-1.5 bg-white/[.03] border border-white/[.06] rounded-xl text-white/35 text-[10px] hover:bg-white/[.06] transition-all">
              {copied ? '✓ Texte copié !' : '📋 Copier le texte pour Instagram / TikTok'}
            </button>
          </div>

          {/* ── Details toggle ── */}
          <button
            onClick={() => setShowDetails(v => !v)}
            className="w-full py-2 bg-white/[.03] border border-white/[.07] rounded-xl text-white/45 text-[11px] flex items-center justify-center gap-2 hover:bg-white/[.06] hover:text-white/65 transition-all"
          >
            {showDetails ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
            {showDetails ? 'Masquer' : 'Voir'} l'analyse détaillée · {total} questions
          </button>

          <button onClick={() => navigate('/bac-diagnostic')}
            className="w-full py-1 text-white/20 text-[10px] flex items-center justify-center gap-1 hover:text-white/40 transition-all">
            <RotateCcw className="w-3 h-3" /> Refaire le test
          </button>
        </div>
      </div>

      {/* ══════ DETAILS ACCORDION ══════ */}
      {showDetails && (
        <div className="relative z-10 max-w-sm mx-auto px-3 pb-10 space-y-4">

          {/* Weak domains */}
          {weak_domains.length > 0 && (
            <div className="bg-white/[.03] border border-white/10 rounded-2xl p-4">
              <h2 className="text-xs font-bold text-white/65 uppercase tracking-wide mb-3 flex items-center gap-2">
                <XCircle className="w-3.5 h-3.5 text-red-400" /> Lacunes prioritaires
              </h2>
              <div className="space-y-2.5">
                {weak_domains.slice(0, 5).map((d, i) => (
                  <div key={i} className="flex items-center gap-3">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-1.5 mb-1">
                        <span className="text-xs font-semibold text-white truncate">{d.domain}</span>
                        <span className="text-[9px] text-white/30">{d.subject}</span>
                      </div>
                      <div className="w-full bg-white/5 rounded-full h-1.5 overflow-hidden">
                        <div className={`h-full rounded-full transition-all ${d.pct < 40 ? 'bg-red-500' : d.pct < 70 ? 'bg-amber-500' : 'bg-emerald-500'}`}
                          style={{ width: `${d.pct}%` }} />
                      </div>
                    </div>
                    <span className={`text-xs font-bold shrink-0 ${d.pct < 40 ? 'text-red-400' : d.pct < 70 ? 'text-amber-400' : 'text-emerald-400'}`}>
                      {d.pct}%
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Study plan */}
          {plan.length > 0 && (
            <div className="bg-white/[.03] border border-white/10 rounded-2xl p-4">
              <h2 className="text-xs font-bold text-white/65 uppercase tracking-wide mb-3 flex items-center gap-2">
                <Calendar className="w-3.5 h-3.5 text-indigo-400" /> Plan de révision · {daysLeft} jours
              </h2>
              <div className="space-y-2">
                {plan.map((item, i) => {
                  const range = item.day_start === item.day_end ? `J${item.day_start}` : `J${item.day_start}–${item.day_end}`;
                  return (
                    <div key={i} className={`rounded-xl border p-3 ${
                      item.label.includes('🔴') ? 'border-red-400/20 bg-red-500/5' :
                      item.label.includes('🟡') ? 'border-amber-400/20 bg-amber-500/5' :
                      item.label.includes('🏁') ? 'border-indigo-400/20 bg-indigo-500/5' :
                      'border-emerald-400/15 bg-emerald-500/5'
                    }`}>
                      <div className="flex items-start gap-2">
                        <span className="text-xl shrink-0">{item.emoji}</span>
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 mb-0.5">
                            <span className="text-white font-bold text-xs">{item.domain}</span>
                            <span className="text-white/30 text-[9px]">{range}</span>
                          </div>
                          {item.tasks.slice(0, 2).map((t, j) => (
                            <div key={j} className="text-[10px] text-white/50 flex gap-1">
                              <span className="text-white/25 shrink-0">→</span>{t}
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* Question review */}
          <div className="bg-white/[.03] border border-white/10 rounded-2xl p-4">
            <h2 className="text-xs font-bold text-white/65 uppercase tracking-wide mb-3">
              Détail des {total} questions
            </h2>
            <div className="space-y-2">
              {detailed.map((q, i) => (
                <div key={i} className={`rounded-xl border p-3 ${q.is_correct ? 'border-emerald-400/15 bg-emerald-500/5' : 'border-red-400/15 bg-red-500/5'}`}>
                  <div className="flex items-start gap-2 mb-1.5">
                    {q.is_correct
                      ? <CheckCircle className="w-3.5 h-3.5 text-emerald-400 mt-0.5 shrink-0" />
                      : <XCircle className="w-3.5 h-3.5 text-red-400 mt-0.5 shrink-0" />
                    }
                    <div>
                      <div className="text-[9px] text-white/30 mb-0.5">{q.domain} · {q.subject}</div>
                      <p className="text-white/75 text-[11px] leading-relaxed">
                        <LatexRenderer content={q.content} />
                      </p>
                    </div>
                  </div>
                  {!q.is_correct && (
                    <div className="ml-5 space-y-0.5">
                      {q.user_answer && q.user_answer !== 'skip'
                        ? <div className="text-[10px] text-red-300">✗ Ta réponse : <b>{q.user_answer.toUpperCase()}</b></div>
                        : <div className="text-[10px] text-white/30">✗ Non répondu</div>
                      }
                      <div className="text-[10px] text-emerald-300">✓ Bonne réponse : <b>{q.correct_answer.toUpperCase()}</b></div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
